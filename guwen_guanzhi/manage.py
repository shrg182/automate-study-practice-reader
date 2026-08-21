#!/usr/bin/env python3
"""Build the 《古文观止》 selector and process selected 5000言 articles."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys

import requests
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent
PRACTICE_DIR = BASE_DIR.parent
SOURCE_URL = "https://gwgz.5000yan.com/"
SOURCE_CATALOG = BASE_DIR / "source_catalog.csv"
CATALOG = BASE_DIR / "catalog.csv"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; GuwenGuanzhiStudyBuilder/1.0)"}
NUMBERS = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
sys.path.insert(0, str(PRACTICE_DIR / "rongzhai_suibi"))
sys.path.insert(0, str(PRACTICE_DIR / "shiji" / "shiji_lisheng_lujia"))
import download_rongzhai as source_tools  # noqa: E402
from build_editor import build_html, load_global_terms, load_review_notes, load_terms  # noqa: E402


def chinese_number(value: str) -> int:
    if value == "十": return 10
    if value.startswith("十"): return 10 + NUMBERS[value[1:]]
    return NUMBERS[value]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists(): return []
    with path.open(encoding="utf-8-sig", newline="") as file: return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields); writer.writeheader(); writer.writerows(rows)


def parse_contents(text: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(text, "html.parser"); rows = []
    for heading in soup.select(".category-block-title"):
        match = re.search(r"卷([一二三四五六七八九十]+)", heading.get_text(" ", strip=True))
        article_list = heading.find_next_sibling("ul")
        if not match or article_list is None: continue
        volume = chinese_number(match.group(1))
        for volume_sequence, link in enumerate(article_list.select("a.category-link"), 1):
            source = re.search(r"/(\d+)\.html", link.get("href", ""))
            if source: rows.append({"sequence": str(len(rows)+1), "volume": str(volume), "volume_sequence": str(volume_sequence), "title": link.get_text(" ", strip=True), "source_id": source.group(1), "source_url": link["href"]})
    if len(rows) < 200: raise ValueError(f"Incomplete contents page: only {len(rows)} articles found")
    return rows


def entry_dir(row: dict[str, str]) -> Path:
    return BASE_DIR / f"volume_{int(row['volume']):02d}" / f"{int(row['sequence']):03d}_{row['slug']}"


def write_entry(row: dict[str, str], html_text: str) -> None:
    parsed = source_tools.parse_page(html_text, row); target = entry_dir(row); target.mkdir(parents=True, exist_ok=True)
    (target / "original.txt").write_text(str(parsed["original"]) + "\n", encoding="utf-8")
    (target / "reading.txt").write_text(str(parsed["reading"]) + "\n", encoding="utf-8")
    (target / "translation.txt").write_text(str(parsed["translation"]) + "\n", encoding="utf-8")
    with (target / "source_notes.tsv").open("w", encoding="utf-8", newline="") as file:
        writer=csv.DictWriter(file,fieldnames=["order","source_key","term","annotation"],delimiter="\t");writer.writeheader();writer.writerows(parsed["notes"])
    with (target / "reading_terms.csv").open("w", encoding="utf-8", newline="") as file:
        writer=csv.DictWriter(file,fieldnames=["term","pinyin","annotation","type"]);writer.writeheader()
        for note in parsed["notes"]: writer.writerow({"term":note["term"],"pinyin":"","annotation":note["annotation"],"type":"source_note"})
    (target / "review_notes.tsv").write_text("text\tissue\tstatus\n", encoding="utf-8")
    metadata={"sequence":int(row["sequence"]),"volume":int(row["volume"]),"title":parsed["title"],"slug":row["slug"],"source_id":int(row["source_id"]),"source_url":row["source_url"],"retrieved_at":datetime.now(timezone.utc).isoformat(),"source_site":"5000言","original_characters":len(str(parsed["original"])),"source_note_count":len(parsed["notes"]),"active_source_note_count":parsed["active_note_count"]}
    (target / "source.json").write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"Wrote {target}: {metadata['original_characters']} chars, {metadata['source_note_count']} notes")


def build_editors() -> None:
    for row in read_csv(CATALOG):
        target = entry_dir(row); text = (target / "reading.txt").read_text(encoding="utf-8"); original = (target / "original.txt").read_text(encoding="utf-8"); terms = load_terms(target / "reading_terms.csv")
        output = build_html(text, terms, row["source_url"], chapter_title=f"《古文观止·{row['title']}》", editor_title=f"《古文观止·{row['title']}》校读编辑器", storage_key=f"guwen-guanzhi-{row['source_id']}-editor-v1", file_stem=f"guwen_guanzhi_{row['source_id']}", review_notes=load_review_notes(target / "review_notes.tsv"), global_terms=load_global_terms(PRACTICE_DIR / "project_dictionary" / "dictionary.csv", original, terms), home_href="../../../index.html", theme_href="../../../workspace_theme.css", shared_library_href="", source_site_label="5000言")
        (target / "editor.html").write_text(output, encoding="utf-8"); print(f"Built {target/'editor.html'}")


def selector_page(rows: list[dict[str, str]]) -> str:
    active = {row["source_id"]: row for row in read_csv(CATALOG)}; payload = []
    for row in rows:
        project = active.get(row["source_id"]); editor = ""
        if project:
            path = entry_dir(project) / "editor.html"
            if path.exists(): editor = path.relative_to(BASE_DIR).as_posix()
        payload.append({**row, "editor": editor})
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    return SELECTOR.replace("__ARTICLES__", data)


def build_selector(refresh: bool = False) -> None:
    if refresh or not SOURCE_CATALOG.exists():
        response = requests.get(SOURCE_URL, headers=HEADERS, timeout=30); response.raise_for_status(); rows = parse_contents(source_tools.response_text(response)); write_csv(SOURCE_CATALOG, rows, list(rows[0]))
    else: rows = read_csv(SOURCE_CATALOG)
    (BASE_DIR / "select_articles.html").write_text(selector_page(rows), encoding="utf-8"); print(f"Wrote selector with {len(rows)} articles")


def process_queue(queue: Path) -> None:
    payload = json.loads(queue.read_text(encoding="utf-8")); requested = {str(item.get("source_id", "")) for item in payload.get("articles", [])}; sources = {row["source_id"]: row for row in read_csv(SOURCE_CATALOG)}
    if not requested or requested - sources.keys(): raise ValueError("Queue contains invalid 《古文观止》 articles")
    project = read_csv(CATALOG); by_id = {row["source_id"]: row for row in project}; selected = []
    for source_id in sorted(requested, key=lambda value: int(sources[value]["sequence"])):
        source = sources[source_id]; row = by_id.get(source_id)
        if row is None:
            row = {"sequence": source["sequence"], "volume": source["volume"], "title": source["title"], "slug": f"article_{source_id}", "source_id": source_id, "source_url": source["source_url"], "status": "downloaded"}; project.append(row); by_id[source_id] = row
        selected.append(row)
    write_csv(CATALOG, sorted(project, key=lambda row:int(row["sequence"])), ["sequence","volume","title","slug","source_id","source_url","status"])
    session = requests.Session(); session.headers.update(HEADERS)
    for row in selected:
        target = entry_dir(row)
        if (target / "source.json").exists(): continue
        response = session.get(row["source_url"], timeout=30); response.raise_for_status(); write_entry(row, source_tools.response_text(response))
    build_editors(); build_selector(); subprocess.run([sys.executable, str(PRACTICE_DIR / "build_index.py")], check=True)
    print(f"Processed {len(selected)} selected 《古文观止》 article(s)")


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__); sub=parser.add_subparsers(dest="command",required=True); build=sub.add_parser("build-selector"); build.add_argument("--refresh",action="store_true"); process=sub.add_parser("process"); process.add_argument("queue",type=Path); args=parser.parse_args()
    if args.command=="build-selector": build_selector(args.refresh)
    else: process_queue(args.queue)


SELECTOR='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>《古文观止》篇目选择器</title><style>*{box-sizing:border-box}body{margin:0;background:#f8f9fa;color:#202124;font-family:Arial,"PingFang SC",sans-serif}header{padding:22px 28px;background:#fff;border-bottom:1px solid #dadce0}h1{margin:7px 0;font-size:28px}a{color:inherit}.shell{width:100%;padding:12px 20px 60px}.controls{position:sticky;top:0;z-index:4;display:grid;grid-template-columns:minmax(250px,1fr) 150px auto;gap:8px;padding:9px 0;background:#f8f9faf2}.queue{display:flex;gap:9px;align-items:center;padding:10px;background:#fff;border:1px solid #dadce0}.queue input[type=text]{flex:1}input,select,button{min-height:38px;padding:7px 10px;border:1px solid #dadce0;border-radius:5px;background:#fff;font:inherit}button{cursor:pointer}.primary{background:#188038;color:#fff}.summary{color:#5f6368}.volume{margin:14px 0;border:1px solid #dadce0;background:#fff}.volume h2{display:flex;justify-content:space-between;margin:0;padding:11px 14px;background:#f1f3f4;font-size:16px}.article{display:grid;grid-template-columns:45px minmax(0,1fr) auto;gap:10px;padding:9px 13px;border-top:1px solid #dadce0}.article label{display:flex;gap:9px}.links{display:flex;gap:6px}.links a{padding:5px 8px;border:1px solid #dadce0;border-radius:14px;text-decoration:none;font-size:12px}.done{color:#137333;font-weight:700}@media(max-width:700px){.controls{grid-template-columns:1fr}.article{grid-template-columns:35px 1fr}.links{grid-column:2}}</style></head><body><header><a href="../index.html">← 返回校读书斋</a><h1>《古文观止》篇目选择器</h1><p>按十二卷浏览、搜索并选择需要生成校读编辑器的文章。</p></header><main class="shell"><div class="controls"><input id="search" type="search" placeholder="搜索篇名或网页编号"><select id="volume"><option value="">全部卷次</option></select><button id="selectVisible">选中当前结果</button></div><div class="queue"><input id="url" type="text" placeholder="粘贴古文观止文章链接"><button id="add">加入选择</button><label><input id="pdf" type="checkbox"> 同时生成 PDF</label><button class="primary" id="export">导出处理清单</button></div><p id="summary" class="summary"></p><div id="catalog"></div></main><script>const ARTICLES=__ARTICLES__,KEY='guwen-guanzhi-selected',chosen=new Set(JSON.parse(localStorage.getItem(KEY)||'[]')),catalog=document.getElementById('catalog'),search=document.getElementById('search'),volume=document.getElementById('volume'),summary=document.getElementById('summary');[...new Set(ARTICLES.map(x=>x.volume))].forEach(v=>volume.add(new Option(`卷${v}`,v)));function esc(s){return s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}function filtered(){const q=search.value.trim().toLowerCase();return ARTICLES.filter(x=>(!volume.value||x.volume===volume.value)&&(!q||`${x.title} ${x.source_id}`.toLowerCase().includes(q)))}function save(){localStorage.setItem(KEY,JSON.stringify([...chosen]));summary.textContent=`已选 ${chosen.size} 篇 · 共 ${ARTICLES.length} 篇`}function render(){const visible=new Set(filtered().map(x=>x.source_id));catalog.innerHTML='';for(const v of [...new Set(ARTICLES.map(x=>x.volume))]){const rows=ARTICLES.filter(x=>x.volume===v&&visible.has(x.source_id));if(!rows.length)continue;const box=document.createElement('section');box.className='volume';box.innerHTML=`<h2><span>卷${v}</span><small>${rows.length} 篇</small></h2>`;for(const x of rows){const row=document.createElement('div');row.className='article';row.innerHTML=`<span>${x.sequence}</span><label><input type="checkbox" data-id="${x.source_id}" ${chosen.has(x.source_id)?'checked':''}><span>${esc(x.title)} <small class="${x.editor?'done':''}">${x.editor?'已生成编辑器':'未处理'}</small></span></label><span class="links"><a href="${x.source_url}" target="_blank">阅读原文</a>${x.editor?`<a href="${x.editor}" target="_blank">打开编辑器</a>`:''}</span>`;box.append(row)}catalog.append(box)}save()}catalog.onchange=e=>{if(!e.target.dataset.id)return;e.target.checked?chosen.add(e.target.dataset.id):chosen.delete(e.target.dataset.id);save()};search.oninput=render;volume.onchange=render;document.getElementById('selectVisible').onclick=()=>{const ids=filtered().map(x=>x.source_id),all=ids.every(x=>chosen.has(x));ids.forEach(x=>all?chosen.delete(x):chosen.add(x));render()};document.getElementById('add').onclick=()=>{const m=document.getElementById('url').value.match(/\/(\d+)\.html/),x=m&&ARTICLES.find(a=>a.source_id===m[1]);if(!x)return alert('链接不在古文观止目录中');chosen.add(x.source_id);render()};document.getElementById('export').onclick=()=>{if(!chosen.size)return alert('请先选择文章');const payload={version:1,collection:'guwen_guanzhi',createdAt:new Date().toISOString(),generatePdfs:document.getElementById('pdf').checked,articles:ARTICLES.filter(x=>chosen.has(x.source_id))},a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));a.download='guwen_guanzhi_processing_queue.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};render()</script></body></html>'''


if __name__ == "__main__": main()
