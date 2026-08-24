#!/usr/bin/env python3
"""Build and process the complete Chinese historical-wars reading list."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import html
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import quote, urljoin

import requests
from bs4 import BeautifulSoup, Tag


BASE_DIR = Path(__file__).resolve().parent
PRACTICE_DIR = BASE_DIR.parent
SOURCE_URL = "https://bbs.wenxuecity.com/memory/1920809.html"
CANONICAL_URL = "https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9B%BD%E6%88%98%E4%BA%89%E5%88%97%E8%A1%A8"
SOURCE_CATALOG = BASE_DIR / "source_catalog.csv"
CATALOG = BASE_DIR / "catalog.csv"
FIELDS = ["sequence", "period_id", "period_order", "period_title", "date_original", "battle_title", "source_url", "source_note", "reliability", "raw_text"]
PERIODS = {
    "ancient_xia": (1, "史前与夏朝", 26),
    "shang": (2, "商朝（前1600年－前1046年）", 43),
    "western_zhou": (3, "西周（前1046年－前771年）", 42),
    "spring_autumn": (4, "春秋时期（前770年－前476年）", 383),
    "warring_states_qin": (5, "战国时期（前475年－前221年）－秦朝（前221年－前207年）", 57),
    "qin_han": (6, "秦汉（前221－220）", 75),
    "three_kingdoms": (7, "三国（184－280）", 62),
    "jin_sixteen_kingdoms": (8, "晋朝（265－420）与五胡十六国（304－439）", 44),
    "northern_southern": (9, "南北朝时期（420－589）", 61),
    "sui": (10, "隋朝（589－618）", 148),
    "tang": (11, "唐朝（618－907，含武周时期）", 123),
    "five_dynasties": (12, "五代时期（907－979）", 26),
    "northern_song": (13, "北宋（960－1127）", 63),
    "song_jin": (14, "宋金战争（1125－1234）", 34),
    "mongol_conquests": (15, "蒙古征战（1189－1279）", 78),
    "yuan": (16, "元朝（1271－1368）", 15),
    "ming": (17, "明朝（1368－1644）", 64),
    "ming_qing": (18, "明清战争（1618－1659）", 22),
    "qing": (19, "清朝（1644－1911）", 121),
    "republic_of_china": (20, "中华民国大陆时期（1912－1949）", 165),
    "prc": (21, "中华人民共和国参与的战争（1949年10月－至今）", 45),
}
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; StudyPracticeBuilder/1.0)"}
BAIDU_BAIKE_SOURCES = {
    "十三翼之战": "https://baike.baidu.com/item/%E5%8D%81%E4%B8%89%E7%BF%BC%E4%B9%8B%E6%88%98/2559232",
}
sys.path.insert(0, str(PRACTICE_DIR / "shiji" / "shiji_lisheng_lujia"))
from build_editor import build_html, load_global_terms, load_terms  # noqa: E402


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def clean_text(node: Tag) -> str:
    return re.sub(r"\s+", " ", node.get_text(" ", strip=True)).strip()


def classify(raw: str) -> str:
    if re.search(r"存疑|不一定可信|并无.*记载", raw):
        return "存疑"
    if "可信" in raw:
        return "可信"
    return "未分级"


def split_entry(item: Tag) -> tuple[str, str, str, str]:
    raw = clean_text(item)
    link = next((a for a in item.select("a[href]") if "wikipedia.org" in a.get("href", "") or "wikisource.org" in a.get("href", "")), None)
    title = clean_text(link) if link else ""
    match = re.match(r"^(.*?)(?:－|—|：|:)\s*(.+)$", raw)
    date = match.group(1).strip() if match else "年代未详"
    remainder = match.group(2).strip() if match else raw
    if not title:
        title = re.split(r"（|\(", remainder, maxsplit=1)[0].strip()
    note = remainder.replace(title, "", 1).strip(" －—:：") if title in remainder else ""
    source = urljoin("https://zh.wikipedia.org", link.get("href", "")) if link else CANONICAL_URL
    return date, title, source, note


def parse_source(html_text: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html_text, "html.parser")
    root = soup.select_one("#mw-content-text .mw-parser-output")
    if root is None:
        raise ValueError("Could not find the embedded historical-wars list")
    current = "ancient_xia"
    gathered: dict[str, list[Tag]] = {key: [] for key in PERIODS}
    heading_ids = iter(list(PERIODS)[1:])
    for child in root.children:
        if not isinstance(child, Tag):
            continue
        heading = child.select_one(":scope > h2")
        if heading:
            current = next(heading_ids, "done")
            continue
        if current in gathered:
            if child.name == "table" and not child.select("li"):
                gathered[current].extend(tr for tr in child.select("tr") if tr.select(":scope > td"))
            else:
                gathered[current].extend(child.select("li"))
    rows: list[dict[str, str]] = []
    sequence = 0
    for period_id, (period_order, period_title, _) in PERIODS.items():
        for item in gathered[period_id]:
            raw = clean_text(item)
            if not raw:
                continue
            if item.name == "tr":
                cells = item.select(":scope > td")
                if len(cells) < 2:
                    continue
                title, date = clean_text(cells[0]), clean_text(cells[1])
                link = cells[0].select_one("a[href]")
                source = urljoin("https://zh.wikipedia.org", link.get("href", "")) if link else CANONICAL_URL
                note = ""
            else:
                date, title, source, note = split_entry(item)
            sequence += 1
            rows.append({"sequence": str(sequence), "period_id": period_id, "period_order": str(period_order), "period_title": period_title, "date_original": date, "battle_title": title, "source_url": source, "source_note": note, "reliability": classify(raw), "raw_text": raw})
    counts = {key: sum(row["period_id"] == key for row in rows) for key in PERIODS}
    expected = {key: data[2] for key, data in PERIODS.items()}
    if counts != expected:
        raise ValueError(f"Unexpected complete-catalog counts: {counts}")
    return rows


def period_dir(period_id: str) -> Path:
    order, _, _ = PERIODS[period_id]
    return BASE_DIR / "periods" / f"{order:02d}_{period_id}"


def war_table(rows: list[dict[str, str]]) -> str:
    headings = ("年代", "战争／战役", "说明", "中文维基", "百度百科", "人工补充")
    parts = ['<div class="chinese-war-table-wrap"><table class="chinese-war-table"><thead><tr>']
    parts.extend(f'<th scope="col">{heading}</th>' for heading in headings)
    parts.append('</tr></thead><tbody>')
    for number, row in enumerate(rows, 1):
        source = html.escape(row["source_url"], quote=True)
        title = html.escape(row["battle_title"])
        title_link = f'<a href="{source}" target="_blank" rel="noopener" contenteditable="false">{title}</a>'
        baidu_direct = BAIDU_BAIKE_SOURCES.get(row["battle_title"])
        baidu_url = baidu_direct or f'https://baike.baidu.com/search/word?word={quote(row["battle_title"])}'
        baidu_label = "打开条目 ↗" if baidu_direct else "搜索同名条目 ↗"
        cells = (
            html.escape(row["date_original"]), title_link, html.escape(row["source_note"] or "—"),
            f'<a href="{source}" target="_blank" rel="noopener" contenteditable="false">打开条目 ↗</a>',
            f'<a href="{html.escape(baidu_url, quote=True)}" target="_blank" rel="noopener" contenteditable="false" data-baidu-verified="{str(bool(baidu_direct)).lower()}">{baidu_label}</a>',
            "",
        )
        parts.append(f'<tr data-paragraph="{number}" data-entry-id="{html.escape(row["sequence"], quote=True)}">')
        for heading, cell in zip(headings, cells):
            attributes = ' class="reader-editable-cell" contenteditable="true" spellcheck="true" data-field="supplement" data-placeholder="手动添加链接或评论"' if heading == "人工补充" else ""
            parts.append(f'<td data-label="{heading}"{attributes}>{cell}</td>')
        parts.append('</tr>')
    parts.append('</tbody></table></div>')
    return "".join(parts)


def build_period(period_id: str, rows: list[dict[str, str]]) -> None:
    target = period_dir(period_id)
    target.mkdir(parents=True, exist_ok=True)
    _, period_title, _ = PERIODS[period_id]
    lines = [f"中国历代战争·{period_title}", "", "以下日期、名称及存疑说明依来源原貌编排，供阅读、校订与补充。", ""]
    for row in rows:
        suffix = f"（{row['source_note']}）" if row["source_note"] else ""
        lines.extend([f"{row['date_original']}－{row['battle_title']}{suffix}", ""])
    text = "\n".join(lines).strip() + "\n"
    (target / "original.txt").write_text(text, encoding="utf-8")
    (target / "reading.txt").write_text(text, encoding="utf-8")
    write_csv(target / "entries.csv", rows, FIELDS)
    terms_file = target / "reading_terms.csv"
    if not terms_file.exists():
        terms_file.write_text("term,pinyin,annotation,type,difficulty\n", encoding="utf-8")
    review_file = target / "review_notes.tsv"
    if not review_file.exists():
        review_file.write_text("text\tissue\tstatus\n", encoding="utf-8")
    metadata = {"period_id": period_id, "period_title": period_title, "entry_count": len(rows), "source_url": SOURCE_URL, "canonical_source_url": CANONICAL_URL, "retrieved_at": datetime.now(timezone.utc).isoformat(), "editorial_policy": "Original date wording and uncertainty notes are preserved."}
    (target / "source.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    terms = load_terms(terms_file)
    seed_path = target / "editor_seed.json"
    seed = json.loads(seed_path.read_text(encoding="utf-8")) if seed_path.exists() else {}
    output = build_html(text, terms, SOURCE_URL, chapter_title=f"《中国历代战争·{period_title}》", editor_title=f"《中国历代战争·{period_title}》校读编辑器", storage_key=f"chinese-wars-{period_id}-editor-v2", file_stem=f"chinese_wars_{period_id}", global_terms=load_global_terms(PRACTICE_DIR / "project_dictionary" / "dictionary.csv", text, terms), home_href="../../../index.html", theme_href="../../../workspace_theme.css", shared_library_href="", source_site_label="文学城", body_html=seed.get("bodyHTML") or war_table(rows), reading_notes=seed.get("notes") or [], initial_media=seed.get("media") or [])
    table_styles = '''<style>
.chinese-war-table-wrap{width:100%;overflow-x:auto}.chinese-war-table{width:100%;min-width:1180px;border-collapse:collapse;font:14px/1.5 Arial,"PingFang SC",sans-serif}.chinese-war-table th,.chinese-war-table td{padding:9px 10px;border:1px solid #dadce0;text-align:left;vertical-align:top}.chinese-war-table th{position:sticky;top:0;z-index:1;background:#f1f3f4;color:#5f6368;font-size:12px}.chinese-war-table td:nth-child(1){min-width:165px}.chinese-war-table td:nth-child(2){min-width:240px;font-weight:700}.chinese-war-table td:nth-child(3){min-width:260px}.chinese-war-table td:nth-child(4),.chinese-war-table td:nth-child(5){min-width:120px}.chinese-war-table td:nth-child(6){min-width:220px}.chinese-war-table a{color:#174ea6;text-decoration:none}.chinese-war-table a:hover{text-decoration:underline}.chinese-war-table td:nth-child(4) a,.chinese-war-table td:nth-child(5) a{display:inline-block;padding:3px 7px;border:1px solid #c7d5e8;border-radius:12px;background:#f7faff;white-space:nowrap}.chinese-war-table .reader-editable-cell{background:#fffdf4;outline:none}.chinese-war-table .reader-editable-cell:focus{background:#fff;border-color:#1a73e8;box-shadow:inset 0 0 0 2px #d2e3fc}.chinese-war-table .reader-editable-cell:empty::after{content:attr(data-placeholder);color:#9aa0a6;font-style:italic;pointer-events:none}
html[data-workspace-skin="reading"] .chinese-war-table{display:block;min-width:0;font:18px/1.75 "Songti SC","STSong",serif}html[data-workspace-skin="reading"] .chinese-war-table thead{display:none}html[data-workspace-skin="reading"] .chinese-war-table tbody{display:grid;gap:18px}html[data-workspace-skin="reading"] .chinese-war-table tr{display:grid;padding:18px 20px;border:1px solid #ded6c7;border-radius:8px;background:#fffdfa}html[data-workspace-skin="reading"] .chinese-war-table td{display:grid;grid-template-columns:88px minmax(0,1fr);gap:12px;padding:5px 0;border:0}html[data-workspace-skin="reading"] .chinese-war-table td::before{content:attr(data-label);color:#8a8174;font:700 11px/1.5 Arial,"PingFang SC",sans-serif;letter-spacing:.08em}html[data-workspace-skin="reading"] .chinese-war-table td[data-label="战争／战役"]{font-size:22px}html[data-workspace-skin="reading"] .chinese-war-table td[data-label="说明"]{margin-top:4px;padding-top:12px;border-top:1px solid #e8e0d2}
@media(max-width:760px){html[data-workspace-skin="reading"] .chinese-war-table tr{padding:14px}html[data-workspace-skin="reading"] .chinese-war-table td{grid-template-columns:68px minmax(0,1fr);gap:8px}.chinese-war-table{font-size:12px}}
</style>'''
    output = output.replace("</head>", table_styles + "</head>", 1)
    entry_ids = json.dumps([row["sequence"] for row in rows])
    table_storage = f'''<script>
(() => {{
  const editor = document.getElementById("editor"), key = "chinese-wars-{period_id}-table-notes-v1", entryIds = {entry_ids};
  const read = () => {{ try {{ return JSON.parse(localStorage.getItem(key) || "{{}}"); }} catch {{ return {{}}; }} }};
  function normalizeAndRestore() {{
    const saved = read();
    editor.querySelectorAll(".chinese-war-table th").forEach(th => {{ if (th.textContent.trim() === "可靠性") th.remove(); }});
    editor.querySelectorAll(".chinese-war-table tbody tr").forEach((row, index) => {{
      row.dataset.entryId ||= entryIds[index] || String(index + 1);
      row.querySelector('[data-label="可靠性"]')?.remove();
      const cell = row.querySelector('[data-field="supplement"]') || row.querySelector('[data-label="人工补充"]');
      if (!cell) return;
      cell.dataset.field = "supplement"; cell.dataset.placeholder = "手动添加链接或评论";
      cell.className = "reader-editable-cell"; cell.contentEditable = "true"; cell.spellcheck = true;
      if (saved[row.dataset.entryId]?.supplement) cell.innerHTML = saved[row.dataset.entryId].supplement;
    }});
  }}
  editor.addEventListener("input", event => {{
    const cell = event.target.closest('.reader-editable-cell[data-field="supplement"]'); if (!cell) return;
    const row = cell.closest("tr[data-entry-id]"), saved = read(); saved[row.dataset.entryId] ||= {{}};
    saved[row.dataset.entryId].supplement = cell.innerHTML; localStorage.setItem(key, JSON.stringify(saved));
  }});
  normalizeAndRestore();
}})();
</script>'''
    output = output.replace("</body>", table_storage + "</body>", 1)
    (target / "editor.html").write_text(output, encoding="utf-8")


def selector_page(rows: list[dict[str, str]]) -> str:
    selected = {row["sequence"] for row in read_csv(CATALOG)}
    payload = []
    for row in rows:
        editor = period_dir(row["period_id"]) / "editor.html"
        payload.append({**row, "selected": row["sequence"] in selected, "editor": editor.relative_to(BASE_DIR).as_posix() if editor.exists() else ""})
    return SELECTOR.replace("__ENTRIES__", json.dumps(payload, ensure_ascii=False).replace("</", "<\\/"))


def build_selector(refresh: bool = False, source_file: Path | None = None) -> None:
    if source_file:
        rows = parse_source(source_file.read_text(encoding="utf-8", errors="replace"))
        write_csv(SOURCE_CATALOG, rows, FIELDS)
    elif refresh or not SOURCE_CATALOG.exists():
        response = requests.get(SOURCE_URL, headers=HEADERS, timeout=30)
        response.raise_for_status()
        rows = parse_source(response.text)
        write_csv(SOURCE_CATALOG, rows, FIELDS)
    else:
        rows = read_csv(SOURCE_CATALOG)
    (BASE_DIR / "select_entries.html").write_text(selector_page(rows), encoding="utf-8")
    print(f"Wrote selector with {len(rows)} entries")


def process_rows(requested: set[str]) -> None:
    sources = {row["sequence"]: row for row in read_csv(SOURCE_CATALOG)}
    if not requested or requested - sources.keys():
        raise ValueError("Queue contains invalid historical-war entries")
    active = {row["sequence"]: row for row in read_csv(CATALOG)}
    active.update({key: sources[key] for key in requested})
    rows = sorted(active.values(), key=lambda row: int(row["sequence"]))
    write_csv(CATALOG, rows, FIELDS)
    for period_id in PERIODS:
        period_rows = [row for row in rows if row["period_id"] == period_id]
        if period_rows:
            build_period(period_id, period_rows)
    build_selector()
    subprocess.run([sys.executable, str(PRACTICE_DIR / "build_index.py")], check=True)
    print(f"Processed {len(requested)} selection(s); {len(rows)} active entries")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build-selector")
    build.add_argument("--refresh", action="store_true")
    build.add_argument("--source-file", type=Path)
    process = sub.add_parser("process")
    process.add_argument("queue", type=Path)
    sub.add_parser("bootstrap-all", aliases=["bootstrap-prototype"])
    args = parser.parse_args()
    if args.command == "build-selector":
        build_selector(args.refresh, args.source_file)
    elif args.command in {"bootstrap-all", "bootstrap-prototype"}:
        process_rows({row["sequence"] for row in read_csv(SOURCE_CATALOG)})
    else:
        payload = json.loads(args.queue.read_text(encoding="utf-8"))
        process_rows({str(row.get("sequence", "")) for row in payload.get("entries", [])})


SELECTOR = r'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>中国历代战争篇目选择器</title><style>*{box-sizing:border-box}body{margin:0;background:#f8f9fa;color:#202124;font-family:Arial,"PingFang SC",sans-serif}header{padding:18px 24px;background:#fff;border-bottom:1px solid #dadce0}h1{margin:6px 0;font-size:25px}a{color:inherit}.shell{padding:12px 20px 60px}.controls,.queue{position:sticky;z-index:3;display:grid;gap:8px;background:#f8f9faf2}.controls{top:0;grid-template-columns:minmax(240px,1fr) 220px auto;padding:9px 0}.queue{top:56px;grid-template-columns:minmax(280px,1fr) auto auto;padding:8px;border:1px solid #dadce0;background:#fff}input,select,button{min-height:36px;padding:6px 9px;border:1px solid #dadce0;border-radius:5px;background:#fff;font:inherit}button{cursor:pointer}.primary{background:#188038;color:#fff}.period{margin:14px 0;border:1px solid #dadce0;background:#fff}.period h2{display:flex;justify-content:space-between;margin:0;padding:10px 13px;background:#f1f3f4;font-size:16px}.entry{display:grid;grid-template-columns:40px minmax(140px,180px) minmax(0,1fr) 70px 170px;gap:10px;align-items:center;padding:8px 12px;border-top:1px solid #dadce0}.entry small{color:#5f6368}.entry .doubt{color:#b3261e}.links{display:flex;gap:5px}.links a{padding:4px 7px;border:1px solid #dadce0;border-radius:13px;text-decoration:none;font-size:11px}@media(max-width:800px){.controls,.queue{position:static;grid-template-columns:1fr}.entry{grid-template-columns:34px 1fr}.entry>*:nth-child(n+3){grid-column:2}}</style></head><body><header><a href="../index.html">← 返回校读书斋</a><h1>中国历代战争篇目选择器</h1><p>完整目录覆盖史前至当代。可逐项选择，处理后按 21 个历史时期合并为校读编辑器。</p></header><main class="shell"><div class="controls"><input id="search" type="search" placeholder="搜索年代、战争名称或说明"><select id="period"><option value="">全部时期</option></select><button id="selectVisible">选中当前结果</button></div><div class="queue"><input id="url" placeholder="粘贴本页所列的维基百科战争条目链接"><button id="add">加入选择</button><button class="primary" id="export">导出处理清单</button></div><p id="summary"></p><div id="catalog"></div></main><script>const ENTRIES=__ENTRIES__,KEY='chinese-wars-selected',chosen=new Set(JSON.parse(localStorage.getItem(KEY)||'[]')),catalog=document.querySelector('#catalog'),search=document.querySelector('#search'),period=document.querySelector('#period'),summary=document.querySelector('#summary');[...new Map(ENTRIES.map(x=>[x.period_id,x.period_title]))].forEach(([id,title])=>period.add(new Option(title,id)));function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}function visible(){const q=search.value.trim().toLowerCase();return ENTRIES.filter(x=>(!period.value||x.period_id===period.value)&&(!q||`${x.date_original} ${x.battle_title} ${x.source_note}`.toLowerCase().includes(q)))}function save(){localStorage.setItem(KEY,JSON.stringify([...chosen]));summary.textContent=`已选 ${chosen.size} 项 · 完整目录共 ${ENTRIES.length} 项`}function render(){const ids=new Set(visible().map(x=>x.sequence));catalog.innerHTML='';for(const [pid,title] of new Map(ENTRIES.map(x=>[x.period_id,x.period_title]))){const rows=ENTRIES.filter(x=>x.period_id===pid&&ids.has(x.sequence));if(!rows.length)continue;const box=document.createElement('section');box.className='period';box.innerHTML=`<h2><span>${esc(title)}</span><small>${rows.length} 项</small></h2>`;for(const x of rows){const row=document.createElement('div');row.className='entry';row.innerHTML=`<span>${x.sequence}</span><label><input type="checkbox" data-id="${x.sequence}" ${chosen.has(x.sequence)?'checked':''}> ${esc(x.date_original)}</label><strong>${esc(x.battle_title)}</strong><small class="${x.reliability==='存疑'?'doubt':''}">${esc(x.reliability)}</small><span class="links"><a href="${esc(x.source_url)}" target="_blank">条目来源</a>${x.editor?`<a href="${x.editor}" target="_blank">时期编辑器</a>`:''}</span>`;if(x.source_note)row.title=x.source_note;box.append(row)}catalog.append(box)}save()}catalog.onchange=e=>{if(!e.target.dataset.id)return;e.target.checked?chosen.add(e.target.dataset.id):chosen.delete(e.target.dataset.id);save()};search.oninput=render;period.onchange=render;document.querySelector('#selectVisible').onclick=()=>{const ids=visible().map(x=>x.sequence),all=ids.every(x=>chosen.has(x));ids.forEach(x=>all?chosen.delete(x):chosen.add(x));render()};document.querySelector('#add').onclick=()=>{const url=document.querySelector('#url').value.trim(),x=ENTRIES.find(x=>x.source_url===url||decodeURI(x.source_url)===decodeURI(url));if(!x)return alert('此链接不在当前目录中');chosen.add(x.sequence);render()};document.querySelector('#export').onclick=()=>{if(!chosen.size)return alert('请先选择条目');const payload={version:1,collection:'chinese_wars',createdAt:new Date().toISOString(),entries:ENTRIES.filter(x=>chosen.has(x.sequence))},a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));a.download='chinese_wars_processing_queue.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};render()</script></body></html>'''


if __name__ == "__main__":
    main()
