#!/usr/bin/env python3
"""Build the Sino-Soviet debate and Nine Commentaries source selector."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent
SOURCE_URL = "https://www.marxists.org/chinese/reference-books/sino-soviet-debate/index.htm"
CATALOG = BASE_DIR / "catalog.csv"
FIELDS = ["sequence", "section", "year", "title", "format", "source_url", "status"]


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def document_year(label: str, href: str) -> str:
    match = re.search(r"(?:19|20)\d{2}", f"{label} {href}")
    if match:
        return match.group(0)
    number = re.fullmatch(r"1-0([1-9])\.htm", href)
    if number:
        return "1963" if int(number.group(1)) <= 6 else "1964"
    return ""


def parse_source(raw: bytes) -> list[dict[str, str]]:
    soup = BeautifulSoup(raw.decode("gb18030"), "html.parser")
    rows: list[dict[str, str]] = []
    section = ""
    for node in soup.find_all(["h3", "a"]):
        if node.name == "h3":
            section = clean(node.get_text(" ", strip=True))
            continue
        if section not in {"中方文献", "九评苏共中央的公开信", "苏方文献"}:
            continue
        href = node.get("href", "")
        if not href or href.startswith("../../index") or "index-class-struggling" in href:
            continue
        title = clean(node.get_text(" ", strip=True))
        rows.append({
            "sequence": str(len(rows) + 1), "section": section,
            "year": document_year(title, href), "title": title,
            "format": "PDF" if href.lower().endswith(".pdf") else "HTML",
            "source_url": urljoin(SOURCE_URL, href), "status": "available",
        })
    if len(rows) != 49:
        raise ValueError(f"Expected 49 documents; found {len(rows)}")
    return rows


def write_catalog(rows: list[dict[str, str]]) -> None:
    with CATALOG.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def read_catalog() -> list[dict[str, str]]:
    with CATALOG.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def build_selector(rows: list[dict[str, str]]) -> None:
    payload = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    html = SELECTOR.replace("__ENTRIES__", payload)
    pdf_link = '<a href="../吴冷西：十年论战——1956-1966中苏关系回忆录.pdf" target="_blank" rel="noopener">打开《十年论战》原书 PDF ↗</a>'
    html = html.replace('<a href="https://www.marxists.org/chinese/reference-books/sino-soviet-debate/index.htm"', pdf_link + '<a href="https://www.marxists.org/chinese/reference-books/sino-soviet-debate/index.htm"')
    (BASE_DIR / "select_readings.html").write_text(html, encoding="utf-8")
    print(f"Wrote selector with {len(rows)} Sino-Soviet debate documents")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-file", type=Path)
    args = parser.parse_args()
    if args.source_file:
        rows = parse_source(args.source_file.read_bytes())
        write_catalog(rows)
    else:
        rows = read_catalog()
    build_selector(rows)


SELECTOR = r'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>中苏论战与九评 · 文献目录</title><style>*{box-sizing:border-box}body{margin:0;background:#f8f9fa;color:#202124;font-family:Arial,"PingFang SC",sans-serif}a{color:inherit}header{padding:28px max(20px,5vw);background:#fff;border-bottom:1px solid #dadce0}header h1{margin:8px 0;font:700 clamp(28px,5vw,44px)/1.2 "Songti SC",serif}header p{max-width:800px;color:#5f6368;line-height:1.7}.header-links{display:flex;gap:8px;flex-wrap:wrap}.header-links a,.links a{padding:6px 9px;border:1px solid #dadce0;border-radius:6px;text-decoration:none;font-size:12px}.shell{width:min(1100px,calc(100% - 32px));margin:18px auto 60px}.controls{position:sticky;top:0;z-index:3;display:grid;grid-template-columns:1fr 220px auto;gap:8px;padding:10px 0;background:#f8f9faf2}input,select,button{min-height:40px;padding:7px 10px;border:1px solid #dadce0;border-radius:6px;background:#fff;font:inherit}button{cursor:pointer}.primary{background:#188038;color:#fff}.summary{color:#5f6368}.section{margin:18px 0;border:1px solid #dadce0;background:#fff}.section h2{display:flex;justify-content:space-between;margin:0;padding:13px 16px;background:#f1f3f4;font:700 20px "Songti SC",serif}.entry{display:grid;grid-template-columns:40px 26px 70px minmax(0,1fr) auto;gap:10px;align-items:center;padding:10px 14px;border-top:1px solid #e8eaed}.entry small{color:#5f6368}.nine{font-weight:700;color:#8b342d}.links{display:flex;gap:6px}@media(max-width:720px){.controls{position:static;grid-template-columns:1fr}.entry{grid-template-columns:34px 24px 1fr}.entry>small{grid-column:3}.entry>.links{grid-column:3}.section h2 small{display:none}}</style></head><body><header><div class="header-links"><a href="../../index.html#nine_commentaries">← 《九评》</a><a href="https://www.marxists.org/chinese/reference-books/sino-soviet-debate/index.htm" target="_blank" rel="noreferrer">专题原始目录 ↗</a></div><h1>中苏论战与九评文献目录</h1><p>按中文马克思主义文库原目录整理，共 49 篇中方文献、九评文本和苏方文献。选择条目后可导出后续处理清单。</p></header><main class="shell"><div class="controls"><input id="search" type="search" placeholder="搜索标题或年份"><select id="section"><option value="">全部分组</option></select><button id="selectVisible">选中当前结果</button></div><p class="summary" id="summary"></p><button class="primary" id="export">导出处理清单</button><div id="catalog"></div></main><script>const ENTRIES=__ENTRIES__,KEY='sino-soviet-debate-selected',chosen=new Set(JSON.parse(localStorage.getItem(KEY)||'[]')),catalog=document.querySelector('#catalog'),search=document.querySelector('#search'),section=document.querySelector('#section'),summary=document.querySelector('#summary'),sections=[...new Set(ENTRIES.map(x=>x.section))];sections.forEach(x=>section.add(new Option(x,x)));function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}function visible(){const q=search.value.trim().toLowerCase();return ENTRIES.filter(x=>(!section.value||x.section===section.value)&&(!q||`${x.title} ${x.year}`.toLowerCase().includes(q)))}function save(){localStorage.setItem(KEY,JSON.stringify([...chosen]));summary.textContent=`已选 ${chosen.size} 篇 · 目录共 ${ENTRIES.length} 篇`}function render(){const ids=new Set(visible().map(x=>x.sequence));catalog.innerHTML='';for(const name of sections){const rows=ENTRIES.filter(x=>x.section===name&&ids.has(x.sequence));if(!rows.length)continue;const box=document.createElement('section');box.className='section';box.innerHTML=`<h2><span>${esc(name)}</span><small>${rows.length} 篇</small></h2>`;for(const x of rows){const row=document.createElement('div');row.className='entry';row.innerHTML=`<span>${x.sequence}</span><input type="checkbox" data-id="${x.sequence}" ${chosen.has(x.sequence)?'checked':''}><small>${esc(x.year)}</small><span class="${x.section.startsWith('九评')?'nine':''}">${esc(x.title)}</span><span class="links"><a href="${esc(x.source_url)}" target="_blank" rel="noreferrer">${x.format==='PDF'?'打开 PDF':'阅读原文'}</a></span>`;box.append(row)}catalog.append(box)}save()}catalog.onchange=e=>{if(!e.target.dataset.id)return;e.target.checked?chosen.add(e.target.dataset.id):chosen.delete(e.target.dataset.id);save()};search.oninput=render;section.onchange=render;document.querySelector('#selectVisible').onclick=()=>{const ids=visible().map(x=>x.sequence),all=ids.every(x=>chosen.has(x));ids.forEach(x=>all?chosen.delete(x):chosen.add(x));render()};document.querySelector('#export').onclick=()=>{if(!chosen.size)return alert('请先选择篇目。');const payload={version:1,collection:'sino_soviet_debate',createdAt:new Date().toISOString(),readings:ENTRIES.filter(x=>chosen.has(x.sequence))},a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));a.download='sino_soviet_debate_processing_queue.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};render()</script></body></html>'''

if __name__ == "__main__":
    main()
