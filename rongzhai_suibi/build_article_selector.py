#!/usr/bin/env python3
"""Build a local selector for the complete 《容斋随笔》 contents."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent
SOURCE_URL = "https://rongzhai.5000yan.com/"
SOURCE_CATALOG = BASE_DIR / "source_catalog.csv"
PROJECT_CATALOG = BASE_DIR / "catalog.csv"
OUTPUT = BASE_DIR / "select_articles.html"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; RongzhaiStudyBuilder/1.0)"}
NUMBERS = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}


def chinese_number(value: str) -> int:
    if value == "十":
        return 10
    if value.startswith("十"):
        return 10 + NUMBERS[value[1:]]
    return NUMBERS[value]


def parse_contents(text: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(text, "html.parser")
    rows = []
    for heading in soup.select(".category-block-title"):
        match = re.search(r"卷([一二三四五六七八九十]+)", heading.get_text(" ", strip=True))
        if not match:
            continue
        volume = chinese_number(match.group(1))
        article_list = heading.find_next_sibling("ul")
        if article_list is None:
            continue
        for volume_sequence, link in enumerate(article_list.select("a.category-link"), 1):
            source = re.search(r"/(\d+)\.html", link.get("href", ""))
            if source:
                rows.append({"sequence": str(len(rows) + 1), "volume": str(volume),
                             "volume_sequence": str(volume_sequence), "title": link.get_text(" ", strip=True),
                             "source_id": source.group(1), "source_url": link["href"]})
    if len(rows) < 300:
        raise ValueError(f"Incomplete contents page: only {len(rows)} articles found")
    return rows


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_catalog(rows: list[dict[str, str]]) -> None:
    with SOURCE_CATALOG.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def page(rows: list[dict[str, str]]) -> str:
    active = {row["source_id"]: row for row in read_csv(PROJECT_CATALOG)}
    payload = []
    for row in rows:
        project = active.get(row["source_id"])
        editor = ""
        if project:
            target = BASE_DIR / f"volume_{int(project['volume']):02d}" / f"{int(project['sequence']):03d}_{project['slug']}" / "editor.html"
            if target.exists():
                editor = target.relative_to(BASE_DIR).as_posix()
        payload.append({**row, "editor": editor})
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    return SELECTOR_HTML.replace("__ARTICLES__", data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-html", type=Path)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    if args.source_html:
        rows = parse_contents(args.source_html.read_text(encoding="utf-8")); write_catalog(rows)
    elif args.refresh or not SOURCE_CATALOG.exists():
        response = requests.get(SOURCE_URL, headers=HEADERS, timeout=30); response.raise_for_status()
        rows = parse_contents(response.text); write_catalog(rows)
    else:
        rows = read_csv(SOURCE_CATALOG)
    OUTPUT.write_text(page(rows), encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(rows)} selectable articles")


SELECTOR_HTML = r'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>《容斋随笔》篇目选择器</title><style>
:root{--ink:#27241f;--muted:#746e63;--paper:#fffdf8;--line:#d9d1c2;--red:#84372f;--green:#477052}*{box-sizing:border-box}body{margin:0;background:#ece7dc;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}header{padding:36px max(22px,5vw);background:#292720;color:#fff}h1{margin:8px 0;font:700 clamp(30px,5vw,54px)/1.1 "Songti SC",serif}header p{max-width:760px;color:#d8d1c5;line-height:1.7}a{color:inherit}.shell{width:min(1180px,calc(100% - 32px));margin:20px auto 70px}.controls{position:sticky;top:0;z-index:5;display:grid;grid-template-columns:1fr 170px auto;gap:9px;padding:12px;background:#ece7dcf2;backdrop-filter:blur(8px)}input,select,button{min-height:40px;padding:7px 10px;border:1px solid var(--line);border-radius:6px;background:#fff;font:inherit}button{cursor:pointer}button.primary{background:var(--red);border-color:var(--red);color:#fff}.queue{display:grid;grid-template-columns:1fr auto;gap:10px;margin:0 12px 18px;padding:14px;background:var(--paper);border:1px solid var(--line)}.queue-entry,.actions,.links{display:flex;gap:7px;flex-wrap:wrap}.queue-entry input{flex:1}.summary{margin:0 12px 10px;color:var(--muted);font-size:13px}.volume{margin:18px 12px;background:var(--paper);border:1px solid var(--line)}.volume h2{display:flex;justify-content:space-between;margin:0;padding:13px 16px;background:#f4efe5;font:700 20px "Songti SC",serif}.article{display:grid;grid-template-columns:35px minmax(0,1fr) auto;gap:11px;align-items:center;padding:10px 15px;border-top:1px solid #ebe5da}.article:hover{background:#faf5ea}.article label{display:flex;gap:10px;align-items:center}.article input[type=checkbox]{min-height:0;width:17px;height:17px}.meta,.status{color:var(--muted);font-size:11px}.status.done{color:var(--green);font-weight:700}.links a{padding:6px 8px;border:1px solid var(--line);border-radius:5px;text-decoration:none;font-size:12px}@media(max-width:720px){.controls,.queue{grid-template-columns:1fr}.article{grid-template-columns:25px 1fr}.links{grid-column:2}}
</style></head><body><header><a href="../index.html">← 返回校读书房</a><h1>《容斋随笔》篇目选择器</h1><p>按卷浏览、搜索并选择希望整理的短篇。只有选中的文章会进入处理清单。</p></header><main class="shell"><div class="controls"><input id="search" type="search" placeholder="搜索篇名或网页编号"><select id="volume"><option value="">全部卷次</option></select><button id="selectVisible">选中当前结果</button></div><section class="queue"><div class="queue-entry"><input id="urlInput" placeholder="粘贴 Rongzhai 文章链接"><button id="addUrl">加入选择</button></div><div class="actions"><label><input id="pdfOption" type="checkbox"> 同时生成 PDF</label><button id="copyUrls">复制链接</button><button class="primary" id="exportQueue">导出处理清单</button></div></section><p class="summary" id="summary"></p><div id="catalog"></div></main><script>
const ARTICLES=__ARTICLES__,selected=new Set(JSON.parse(localStorage.getItem('rongzhai-selected-ids')||'[]')),catalog=document.getElementById('catalog'),search=document.getElementById('search'),volume=document.getElementById('volume'),summary=document.getElementById('summary');for(const v of [...new Set(ARTICLES.map(x=>x.volume))])volume.add(new Option(`卷${v}`,v));function esc(s){return s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}function save(){localStorage.setItem('rongzhai-selected-ids',JSON.stringify([...selected]));summary.textContent=`已选 ${selected.size} 篇 · 目录共 ${ARTICLES.length} 篇`}function filtered(){const q=search.value.trim().toLocaleLowerCase(),v=volume.value;return ARTICLES.filter(x=>(!v||x.volume===v)&&(!q||`${x.title} ${x.source_id}`.toLocaleLowerCase().includes(q)))}function render(){const visible=new Set(filtered().map(x=>x.source_id));catalog.innerHTML='';for(const v of [...new Set(ARTICLES.map(x=>x.volume))]){const rows=ARTICLES.filter(x=>x.volume===v&&visible.has(x.source_id));if(!rows.length)continue;const section=document.createElement('section');section.className='volume';section.innerHTML=`<h2><span>卷${v}</span><small>${rows.length} 篇</small></h2>`;for(const x of rows){const item=document.createElement('div');item.className='article';item.innerHTML=`<span class="meta">${x.sequence}</span><label><input type="checkbox" data-id="${x.source_id}" ${selected.has(x.source_id)?'checked':''}><span>${esc(x.title)} <small class="status ${x.editor?'done':''}">${x.editor?'已生成编辑器':'未处理'}</small></span></label><span class="links"><a href="${x.source_url}" target="_blank" rel="noreferrer">阅读原文</a>${x.editor?`<a href="${x.editor}" target="_blank">打开编辑器</a>`:''}</span>`;section.append(item)}catalog.append(section)}save()}catalog.onchange=e=>{if(!e.target.dataset.id)return;e.target.checked?selected.add(e.target.dataset.id):selected.delete(e.target.dataset.id);save()};search.oninput=render;volume.onchange=render;document.getElementById('selectVisible').onclick=()=>{const ids=filtered().map(x=>x.source_id),all=ids.every(id=>selected.has(id));ids.forEach(id=>all?selected.delete(id):selected.add(id));render()};document.getElementById('addUrl').onclick=()=>{const m=document.getElementById('urlInput').value.match(/\/(\d+)\.html/),x=m&&ARTICLES.find(a=>a.source_id===m[1]);if(!x)return alert('请粘贴目录中的有效文章链接。');selected.add(x.source_id);volume.value=x.volume;search.value='';render()};function chosen(){return ARTICLES.filter(x=>selected.has(x.source_id))}document.getElementById('copyUrls').onclick=async()=>{await navigator.clipboard.writeText(chosen().map(x=>x.source_url).join('\n'));alert('已复制选中链接。')};document.getElementById('exportQueue').onclick=()=>{if(!selected.size)return alert('请先选择文章。');const payload={version:1,createdAt:new Date().toISOString(),generatePdfs:document.getElementById('pdfOption').checked,articles:chosen()},a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));a.download='rongzhai_processing_queue.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};render();
</script></body></html>'''

if __name__ == "__main__":
    main()
