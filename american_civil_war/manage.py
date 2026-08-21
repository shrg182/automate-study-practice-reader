#!/usr/bin/env python3
"""Build and process the American Civil War battle-reading collection."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import quote, urljoin

import requests
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent
PRACTICE_DIR = BASE_DIR.parent
SOURCE_URL = "https://en.wikipedia.org/wiki/List_of_American_Civil_War_battles"
SOURCE_CATALOG = BASE_DIR / "source_catalog.csv"
CATALOG = BASE_DIR / "catalog.csv"
FIELDS = ["sequence", "year", "date_original", "battle_title", "battle_title_zh", "state", "cwsac", "outcome", "notes", "category", "source_url", "source_url_zh"]
YEARS = ("1861", "1862", "1863", "1864", "1865")
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; StudyPracticeBuilder/1.0)"}
sys.path.insert(0, str(PRACTICE_DIR / "shiji" / "shiji_lisheng_lujia"))
from build_editor import build_html, load_global_terms, load_terms  # noqa: E402


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def text(node) -> str:
    return re.sub(r"\s+", " ", node.get_text(" ", strip=True)).strip()


def parse_source(html_text: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html_text, "html.parser")
    tables = [table for table in soup.select("table") if text(table.select_one("tr") or table).startswith("Date Battle State")]
    if len(tables) != 3:
        raise ValueError(f"Expected three battle tables; found {len(tables)}")
    specs = [(tables[0], "CWSAC-rated"), (tables[1], "Other USA/CSA"), (tables[2], "American Indian Wars")]
    rows: list[dict[str, str]] = []
    for table, category in specs:
        for tr in table.select("tr"):
            cells = tr.select(":scope > td")
            if not cells:
                continue
            date = text(cells[0])
            year_match = re.search(r"186[1-5]", date)
            if not year_match:
                continue
            battle_cell = cells[1]
            link = battle_cell.select_one("a[href]")
            if category == "CWSAC-rated":
                state, cwsac, outcome, notes = text(cells[2]), text(cells[3]), text(cells[4]), text(cells[5])
            elif category == "Other USA/CSA":
                state, cwsac, outcome, notes = text(cells[2]), "", text(cells[3]), text(cells[4])
            else:
                state, cwsac, outcome, notes = text(cells[2]), "", text(cells[3]), ""
            rows.append({"sequence": str(len(rows) + 1), "year": year_match.group(0), "date_original": date, "battle_title": text(battle_cell), "battle_title_zh": "", "state": state, "cwsac": cwsac, "outcome": outcome, "notes": notes, "category": category, "source_url": urljoin(SOURCE_URL, link.get("href", "")) if link else SOURCE_URL, "source_url_zh": ""})
    if len(rows) != 480 or {year: sum(row["year"] == year for row in rows) for year in YEARS} != {"1861": 54, "1862": 117, "1863": 118, "1864": 151, "1865": 40}:
        raise ValueError("Unexpected American Civil War catalog counts")
    return rows


def enrich_chinese_links(rows: list[dict[str, str]]) -> None:
    """Add Chinese Wikipedia titles and links when an interlanguage page exists."""
    endpoint = "https://en.wikipedia.org/w/api.php"
    for start in range(0, len(rows), 40):
        batch = rows[start:start + 40]
        titles = [row["source_url"].split("/wiki/", 1)[-1].replace("_", " ") for row in batch]
        response = requests.get(endpoint, params={"action": "query", "format": "json", "prop": "langlinks", "lllang": "zh", "lllimit": "1", "redirects": "1", "titles": "|".join(titles)}, headers=HEADERS, timeout=30)
        response.raise_for_status()
        query = response.json().get("query", {})
        aliases = {item["from"]: item["to"] for kind in ("normalized", "redirects") for item in query.get(kind, [])}
        pages = {page.get("title", ""): page for page in query.get("pages", {}).values()}
        for row, title in zip(batch, titles):
            resolved = aliases.get(title, title)
            resolved = aliases.get(resolved, resolved)
            links = pages.get(resolved, {}).get("langlinks", [])
            if links:
                chinese_title = links[0]["*"]
                row["battle_title_zh"] = chinese_title
                row["source_url_zh"] = f"https://zh.wikipedia.org/wiki/{quote(chinese_title.replace(' ', '_'))}"


def year_dir(year: str) -> Path:
    return BASE_DIR / "years" / year


def build_year(year: str, rows: list[dict[str, str]]) -> None:
    target = year_dir(year)
    target.mkdir(parents=True, exist_ok=True)
    lines = [f"American Civil War Battles · {year}", "", "Battle names, dates, classifications, outcomes, and notes follow the source catalog.", ""]
    for row in rows:
        details = [row["state"], row["outcome"]]
        if row["cwsac"]:
            details.append(f"CWSAC Class {row['cwsac']}")
        details.append(row["category"])
        lines.extend([f"{row['date_original']} — {row['battle_title']}", " · ".join(value for value in details if value), row["notes"], ""])
    body = "\n".join(lines).strip() + "\n"
    (target / "original.txt").write_text(body, encoding="utf-8")
    (target / "reading.txt").write_text(body, encoding="utf-8")
    write_csv(target / "entries.csv", rows)
    terms_file = target / "reading_terms.csv"
    if not terms_file.exists():
        terms_file.write_text("term,pinyin,annotation,type,difficulty\n", encoding="utf-8")
    review_file = target / "review_notes.tsv"
    if not review_file.exists():
        review_file.write_text("text\tissue\tstatus\n", encoding="utf-8")
    metadata = {"year": int(year), "entry_count": len(rows), "source_url": SOURCE_URL, "retrieved_at": datetime.now(timezone.utc).isoformat(), "source_language": "English", "editorial_policy": "Source dates, names, ratings, outcomes, and notes are preserved."}
    (target / "source.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    terms = load_terms(terms_file)
    output = build_html(body, terms, SOURCE_URL, chapter_title=f"American Civil War Battles · {year}", editor_title=f"American Civil War · {year} Reading Editor", storage_key=f"american-civil-war-{year}-editor-v1", file_stem=f"american_civil_war_{year}", global_terms=load_global_terms(PRACTICE_DIR / "project_dictionary" / "dictionary.csv", body, terms), home_href="../../../index.html", theme_href="../../../workspace_theme.css", shared_library_href="", source_site_label="Wikipedia")
    (target / "editor.html").write_text(output, encoding="utf-8")


def selector_page(rows: list[dict[str, str]]) -> str:
    active = {row["sequence"] for row in read_csv(CATALOG)}
    payload = [{**row, "battle_title_zh": row.get("battle_title_zh", ""), "source_url_zh": row.get("source_url_zh", ""), "processed": row["sequence"] in active, "editor": (year_dir(row["year"]) / "editor.html").relative_to(BASE_DIR).as_posix() if (year_dir(row["year"]) / "editor.html").exists() else ""} for row in rows]
    return SELECTOR.replace("__ENTRIES__", json.dumps(payload, ensure_ascii=False).replace("</", "<\\/"))


def build_selector(source_file: Path | None = None, refresh: bool = False) -> None:
    if source_file:
        rows = parse_source(source_file.read_text(encoding="utf-8", errors="replace"))
        enrich_chinese_links(rows)
        write_csv(SOURCE_CATALOG, rows)
    elif refresh or not SOURCE_CATALOG.exists():
        response = requests.get(SOURCE_URL, headers=HEADERS, timeout=30)
        response.raise_for_status()
        rows = parse_source(response.text)
        enrich_chinese_links(rows)
        write_csv(SOURCE_CATALOG, rows)
    else:
        rows = read_csv(SOURCE_CATALOG)
    (BASE_DIR / "select_battles.html").write_text(selector_page(rows), encoding="utf-8")
    print(f"Wrote selector with {len(rows)} battles")


def process_rows(requested: set[str]) -> None:
    source = {row["sequence"]: row for row in read_csv(SOURCE_CATALOG)}
    if not requested or requested - source.keys():
        raise ValueError("Queue contains invalid American Civil War battles")
    active = {row["sequence"]: row for row in read_csv(CATALOG)}
    active.update({key: source[key] for key in requested})
    rows = sorted(active.values(), key=lambda row: int(row["sequence"]))
    write_csv(CATALOG, rows)
    for year in YEARS:
        selected = [row for row in rows if row["year"] == year]
        if selected:
            build_year(year, selected)
    build_selector()
    subprocess.run([sys.executable, str(PRACTICE_DIR / "build_index.py")], check=True)
    print(f"Processed {len(requested)} selection(s); {len(rows)} active battles")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build-selector")
    build.add_argument("--source-file", type=Path)
    build.add_argument("--refresh", action="store_true")
    process = sub.add_parser("process")
    process.add_argument("queue", type=Path)
    sub.add_parser("bootstrap-all")
    sub.add_parser("enrich-translations")
    args = parser.parse_args()
    if args.command == "build-selector":
        build_selector(args.source_file, args.refresh)
    elif args.command == "enrich-translations":
        rows = read_csv(SOURCE_CATALOG)
        enrich_chinese_links(rows)
        write_csv(SOURCE_CATALOG, rows)
        build_selector()
    elif args.command == "bootstrap-all":
        process_rows({row["sequence"] for row in read_csv(SOURCE_CATALOG)})
    else:
        payload = json.loads(args.queue.read_text(encoding="utf-8"))
        process_rows({str(row.get("sequence", "")) for row in payload.get("battles", [])})


SELECTOR = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>American Civil War Battle Selector</title><style>*{box-sizing:border-box}body{margin:0;background:#f8f9fa;color:#202124;font-family:Arial,sans-serif}header{padding:18px 24px 18px 108px;background:#fff;border-bottom:1px solid #dadce0}h1{margin:6px 0;font-size:25px}a{color:inherit}.home-link{position:fixed;z-index:10;top:12px;left:12px;padding:9px 12px;border:1px solid #dadce0;border-radius:20px;background:#fff;text-decoration:none;box-shadow:0 2px 8px #0002}.companion{display:inline-block;padding:6px 9px;border:1px solid #dadce0;border-radius:6px;text-decoration:none;font-size:12px}.shell{padding:12px 20px 60px}.controls{position:sticky;top:0;z-index:3;display:grid;grid-template-columns:minmax(240px,1fr) 150px auto;gap:8px;padding:9px 0;background:#f8f9faf2}.queue{display:flex;gap:8px;padding:8px;border:1px solid #dadce0;background:#fff}.queue input{flex:1}input,select,button{min-height:36px;padding:6px 9px;border:1px solid #dadce0;border-radius:5px;background:#fff;font:inherit}button{cursor:pointer}.primary{background:#188038;color:#fff}.year{margin:14px 0;border:1px solid #dadce0;background:#fff;overflow:auto}.year h2{display:flex;justify-content:space-between;margin:0;padding:10px 13px;background:#f1f3f4}.battle-table{width:100%;min-width:980px;border-collapse:collapse}.battle-table th,.battle-table td{padding:8px 10px;border-top:1px solid #dadce0;text-align:left;vertical-align:top;font-size:12px}.battle-table th{position:sticky;top:54px;background:#f8f9fa;color:#5f6368}.battle-table td:first-child{width:42px}.battle-table .battle-title{font-weight:700}.battle-table .translation{color:#174ea6}.links{display:flex;flex-wrap:wrap;gap:5px}.links a{padding:4px 7px;border:1px solid #dadce0;border-radius:13px;text-decoration:none;font-size:11px;white-space:nowrap}@media(max-width:800px){header{padding:64px 16px 16px}.controls{position:static;grid-template-columns:1fr}.queue{display:grid}.battle-table th{position:static}}</style></head><body><a class="home-link" href="../index.html">← Home</a><header><h1>American Civil War Battle Selector</h1><p>Browse 480 engagements from 1861–1865. Battle names link to their source pages and available Chinese translations appear in a separate column.</p><a class="companion" href="../marxist_classics/american_civil_war/select_readings.html">马克思、恩格斯论美国内战 ↗</a></header><main class="shell"><div class="controls"><input id="search" type="search" placeholder="Search battle, Chinese title, state, outcome, or notes"><select id="year"><option value="">All years</option></select><button id="selectVisible">Select visible results</button></div><div class="queue"><input id="url" placeholder="Paste a Wikipedia battle link"><button id="add">Add selection</button><button class="primary" id="export">Export processing queue</button></div><p id="summary"></p><div id="catalog"></div></main><script>const ENTRIES=__ENTRIES__,KEY='american-civil-war-selected',chosen=new Set(JSON.parse(localStorage.getItem(KEY)||'[]')),catalog=document.querySelector('#catalog'),search=document.querySelector('#search'),year=document.querySelector('#year'),summary=document.querySelector('#summary');[...new Set(ENTRIES.map(x=>x.year))].forEach(v=>year.add(new Option(v,v)));function esc(s){return String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}function visible(){const q=search.value.trim().toLowerCase();return ENTRIES.filter(x=>(!year.value||x.year===year.value)&&(!q||`${x.battle_title} ${x.battle_title_zh||''} ${x.state} ${x.outcome} ${x.notes}`.toLowerCase().includes(q)))}function save(){localStorage.setItem(KEY,JSON.stringify([...chosen]));summary.textContent=`Selected ${chosen.size} · ${ENTRIES.length} battles total`}function render(){const ids=new Set(visible().map(x=>x.sequence));catalog.innerHTML='';for(const y of [...new Set(ENTRIES.map(x=>x.year))]){const rows=ENTRIES.filter(x=>x.year===y&&ids.has(x.sequence));if(!rows.length)continue;const box=document.createElement('section');box.className='year';box.innerHTML=`<h2><span>${y}</span><small>${rows.length} battles</small></h2><table class="battle-table"><thead><tr><th>#</th><th>Date</th><th>Battle</th><th>中文译名</th><th>State</th><th>Result / class</th><th>Links</th></tr></thead><tbody></tbody></table>`;const body=box.querySelector('tbody');for(const x of rows){const row=document.createElement('tr');row.title=x.notes;row.innerHTML=`<td>${x.sequence}</td><td><label><input type="checkbox" data-id="${x.sequence}" ${chosen.has(x.sequence)?'checked':''}> ${esc(x.date_original)}</label></td><td class="battle-title"><a href="${esc(x.source_url)}" target="_blank" rel="noopener">${esc(x.battle_title)}</a></td><td class="translation">${x.source_url_zh?`<a href="${esc(x.source_url_zh)}" target="_blank" rel="noopener">${esc(x.battle_title_zh)}</a>`:'—'}</td><td>${esc(x.state)}</td><td>${esc(x.outcome)}<br><small>${esc(x.cwsac||x.category)}</small></td><td class="links"><a href="${esc(x.source_url)}" target="_blank" rel="noopener">English ↗</a>${x.source_url_zh?`<a href="${esc(x.source_url_zh)}" target="_blank" rel="noopener">中文 ↗</a>`:''}${x.editor?`<a href="${x.editor}" target="_blank" rel="noopener">Year editor</a>`:''}</td>`;body.append(row)}catalog.append(box)}save()}catalog.onchange=e=>{if(!e.target.dataset.id)return;e.target.checked?chosen.add(e.target.dataset.id):chosen.delete(e.target.dataset.id);save()};search.oninput=render;year.onchange=render;document.querySelector('#selectVisible').onclick=()=>{const ids=visible().map(x=>x.sequence),all=ids.every(x=>chosen.has(x));ids.forEach(x=>all?chosen.delete(x):chosen.add(x));render()};document.querySelector('#add').onclick=()=>{const url=document.querySelector('#url').value.trim(),x=ENTRIES.find(x=>decodeURI(x.source_url)===decodeURI(url));if(!x)return alert('This link is not in the current catalog.');chosen.add(x.sequence);render()};document.querySelector('#export').onclick=()=>{if(!chosen.size)return alert('Select at least one battle.');const payload={version:1,collection:'american_civil_war',createdAt:new Date().toISOString(),battles:ENTRIES.filter(x=>chosen.has(x.sequence))},a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));a.download='american_civil_war_processing_queue.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};render()</script></body></html>'''


if __name__ == "__main__":
    main()
