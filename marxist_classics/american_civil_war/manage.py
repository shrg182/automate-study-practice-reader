#!/usr/bin/env python3
"""Build the Marx and Engels American Civil War reading selector."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

BASE_DIR = Path(__file__).resolve().parent
SOURCE_URL = "https://www.marxists.org/chinese/marx-engels/subject/us-civilwar.htm"
CATALOG = BASE_DIR / "catalog.csv"
FIELDS = ["sequence", "section", "year", "author", "title", "featured", "source_url", "status"]


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().lstrip("*").strip()


def parse_source(raw: bytes) -> list[dict[str, str]]:
    soup = BeautifulSoup(raw.decode("gb18030"), "html.parser")
    rows: list[dict[str, str]] = []
    section = year = ""
    for node in soup.find_all(["h3", "h4", "a"]):
        if node.name == "h3":
            heading = clean(node.get_text(" ", strip=True))
            if heading.startswith("第一部分"):
                section = "《纽约每日论坛报》论文"
            elif heading.startswith("第二部分"):
                section = "《维也纳新闻》论文"
            elif heading.startswith("第三部分"):
                section = "马克思和恩格斯的通信"
            elif "附" in heading and "录" in heading:
                section = "附录"
            year = ""
            continue
        if node.name == "h4":
            match = re.search(r"18\d{2}", node.get_text(" ", strip=True))
            year = match.group(0) if match else ""
            continue
        if not section or not isinstance(node, Tag):
            continue
        href = node.get("href", "")
        if not (re.fullmatch(r"\.\./(?:15|16|30|31)/\d{3}\.htm", href) or href == "us-civilwar-4-2.htm"):
            continue
        raw_label = node.get_text(" ", strip=True)
        label = clean(raw_label)
        featured = "yes" if raw_label.startswith("*") or "*" in str(node.previous_sibling or "") else "no"
        if "。" in label and section != "马克思和恩格斯的通信":
            author, title = label.split("。", 1)
        else:
            author, title = "马克思、恩格斯", label
        if section == "马克思和恩格斯的通信":
            title = re.sub(r"^\d+．", "", title)
            author = title.split("致", 1)[0] if "致" in title else "马克思、恩格斯"
        rows.append({"sequence": str(len(rows) + 1), "section": section, "year": year, "author": author, "title": title, "featured": featured, "source_url": urljoin(SOURCE_URL, href), "status": "available"})
    if len(rows) != 113:
        raise ValueError(f"Expected 113 documents; found {len(rows)}")
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
    (BASE_DIR / "select_readings.html").write_text(SELECTOR.replace("__ENTRIES__", payload), encoding="utf-8")
    print(f"Wrote selector with {len(rows)} Marx–Engels readings")


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


SELECTOR = r'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>马克思、恩格斯论美国内战 · 阅读目录</title><style>*{box-sizing:border-box}body{margin:0;background:#f8f9fa;color:#202124;font-family:Arial,"PingFang SC",sans-serif}a{color:inherit}header{padding:28px max(20px,5vw);background:#fff;border-bottom:1px solid #dadce0}header h1{margin:8px 0;font:700 clamp(28px,5vw,44px)/1.2 "Songti SC",serif}header p{max-width:900px;color:#5f6368;line-height:1.7}.header-links{display:flex;gap:8px;flex-wrap:wrap}.header-links a,.links a{padding:6px 9px;border:1px solid #dadce0;border-radius:6px;text-decoration:none;font-size:12px}.shell{width:min(1320px,calc(100% - 32px));margin:18px auto 60px}.controls{position:sticky;top:0;z-index:3;display:grid;grid-template-columns:1fr 220px auto;gap:8px;padding:10px 0;background:#f8f9faf2}input,select,button,textarea{font:inherit}input,select,button{min-height:40px;padding:7px 10px;border:1px solid #dadce0;border-radius:6px;background:#fff}button{cursor:pointer}.primary,.save-comment{background:#188038;color:#fff}.summary{color:#5f6368}.section{margin:18px 0;border:1px solid #dadce0;background:#fff}.section h2{display:flex;justify-content:space-between;margin:0;padding:13px 16px;background:#f1f3f4;font:700 20px "Songti SC",serif}.entry,.column-head{display:grid;grid-template-columns:40px 26px 90px minmax(220px,1fr) minmax(220px,.8fr) 86px;gap:10px;align-items:center;padding:10px 14px}.column-head{color:#5f6368;background:#fafafa;font-size:12px;font-weight:700}.entry{border-top:1px solid #e8eaed}.entry small{color:#5f6368}.featured{color:#b06000;font-weight:700}.comment-box{display:grid;gap:6px}.commentary{width:100%;min-height:72px;padding:7px 9px;resize:vertical;border:1px solid #dadce0;border-radius:6px;background:#fff;line-height:1.45}.commentary:focus{border-color:#1a73e8;outline:2px solid #d2e3fc}.comment-actions{display:flex;align-items:center;gap:8px}.save-comment{min-height:32px;padding:4px 10px}.save-confirmation{color:#188038;font-size:12px}.links{display:flex;gap:6px}@media(max-width:800px){.controls{position:static;grid-template-columns:1fr}.column-head{display:none}.entry{grid-template-columns:34px 24px 1fr}.entry>small,.entry>.comment-box,.entry>.links{grid-column:3}.commentary{min-height:90px}.section h2 small{display:none}}</style></head><body><header><div class="header-links"><a href="../../index.html">← 校读书斋</a><a href="../../american_civil_war/select_battles.html">美国内战战役目录</a><a href="https://www.marxists.org/chinese/marx-engels/subject/us-civilwar.htm" target="_blank" rel="noreferrer">专题原始目录 ↗</a></div><h1>马克思、恩格斯论美国内战</h1><p>无需先把文章导入编辑器：打开原文阅读时，可直接在同一目录行撰写独立的按语或帖子。内容会自动保存，也可点击“保存按语”确认，并随处理清单一同导出。</p></header><main class="shell"><div class="controls"><input id="search" type="search" placeholder="搜索标题、作者、年份或按语"><select id="section"><option value="">全部部分</option></select><button id="selectVisible">选中当前结果</button></div><p class="summary" id="summary"></p><button class="primary" id="export">导出处理清单</button><div id="catalog"></div></main><script>const ENTRIES=__ENTRIES__,KEY='marx-engels-us-civil-war-selected',COMMENTARY_KEY='marx-engels-us-civil-war-commentary-v1',chosen=new Set(JSON.parse(localStorage.getItem(KEY)||'[]')),commentary=JSON.parse(localStorage.getItem(COMMENTARY_KEY)||'{}'),catalog=document.querySelector('#catalog'),search=document.querySelector('#search'),section=document.querySelector('#section'),summary=document.querySelector('#summary'),sections=[...new Set(ENTRIES.map(x=>x.section))];sections.forEach(x=>section.add(new Option(x,x)));function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}function visible(){const q=search.value.trim().toLowerCase();return ENTRIES.filter(x=>(!section.value||x.section===section.value)&&(!q||`${x.title} ${x.author} ${x.year} ${commentary[x.sequence]||''}`.toLowerCase().includes(q)))}function save(){localStorage.setItem(KEY,JSON.stringify([...chosen]));localStorage.setItem(COMMENTARY_KEY,JSON.stringify(commentary));const noteCount=Object.values(commentary).filter(x=>x.trim()).length;summary.textContent=`已选 ${chosen.size} 篇 · 已写按语 ${noteCount} 篇 · 目录共 ${ENTRIES.length} 篇`}function render(){const ids=new Set(visible().map(x=>x.sequence));catalog.innerHTML='';for(const name of sections){const rows=ENTRIES.filter(x=>x.section===name&&ids.has(x.sequence));if(!rows.length)continue;const box=document.createElement('section');box.className='section';box.innerHTML=`<h2><span>${esc(name)}</span><small>${rows.length} 篇</small></h2><div class="column-head"><span>序号</span><span>选择</span><span>年份／作者</span><span>篇名</span><span>按语／帖子</span><span>原文</span></div>`;for(const x of rows){const row=document.createElement('div');row.className='entry';row.innerHTML=`<span>${x.sequence}</span><input type="checkbox" data-id="${x.sequence}" ${chosen.has(x.sequence)?'checked':''} aria-label="选择第 ${x.sequence} 篇"><small>${esc(x.year||x.author)}</small><span class="${x.featured==='yes'?'featured':''}">${x.featured==='yes'?'★ ':''}${esc(x.title)}</span><div class="comment-box"><textarea class="commentary" data-commentary-id="${x.sequence}" aria-label="第 ${x.sequence} 篇按语" placeholder="一边阅读原文，一边在这里写按语或帖子…">${esc(commentary[x.sequence]||'')}</textarea><div class="comment-actions"><button type="button" class="save-comment" data-save-comment="${x.sequence}">保存按语</button><span class="save-confirmation" data-save-status="${x.sequence}" aria-live="polite"></span></div></div><span class="links"><a href="${esc(x.source_url)}" target="_blank" rel="noreferrer">阅读原文</a></span>`;box.append(row)}catalog.append(box)}save()}catalog.onchange=e=>{if(!e.target.dataset.id)return;e.target.checked?chosen.add(e.target.dataset.id):chosen.delete(e.target.dataset.id);save()};catalog.oninput=e=>{const id=e.target.dataset.commentaryId;if(!id)return;commentary[id]=e.target.value;if(!commentary[id])delete commentary[id];save();const status=catalog.querySelector(`[data-save-status="${id}"]`);if(status)status.textContent='自动保存中…'};catalog.onclick=e=>{const id=e.target.dataset.saveComment;if(!id)return;save();const status=catalog.querySelector(`[data-save-status="${id}"]`);if(status){status.textContent=`已保存 ${new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}`;setTimeout(()=>status.textContent='',3000)}};search.oninput=render;section.onchange=render;document.querySelector('#selectVisible').onclick=()=>{const ids=visible().map(x=>x.sequence),all=ids.every(x=>chosen.has(x));ids.forEach(x=>all?chosen.delete(x):chosen.add(x));render()};document.querySelector('#export').onclick=()=>{if(!chosen.size)return alert('请先选择篇目。');const readings=ENTRIES.filter(x=>chosen.has(x.sequence)).map(x=>({...x,commentary:commentary[x.sequence]||''})),payload={version:2,collection:'marx_engels_us_civil_war',createdAt:new Date().toISOString(),readings},a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));a.download='marx_engels_us_civil_war_processing_queue.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};render()</script></body></html>'''

if __name__ == "__main__":
    main()
