#!/usr/bin/env python3
"""Build the selectable 81-chapter 《老子》 catalog."""

import argparse, csv, json, re
from pathlib import Path
import requests
from bs4 import BeautifulSoup

BASE_DIR=Path(__file__).resolve().parent
SOURCE_URL="https://www.guwendao.net/guwen/book_db8fe8b5a11f.aspx"
SOURCE_CATALOG=BASE_DIR/"source_catalog.csv"; CATALOG=BASE_DIR/"catalog.csv"; OUTPUT=BASE_DIR/"select_chapters.html"

def read_csv(path):
    if not path.exists(): return []
    with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))

def parse(text):
    soup=BeautifulSoup(text,"html.parser"); rows=[]
    for strong in soup.find_all("strong"):
        section=strong.get_text(" ",strip=True)
        if section not in {"道经","德经"}: continue
        links=strong.parent.find_next_sibling("div").find_all("a")
        for link in links:
            href=requests.compat.urljoin(SOURCE_URL,link.get("href",""))
            if "/guwen/bookv_" not in href: continue
            rows.append({"sequence":str(len(rows)+1),"section":section,"title":link.get_text(" ",strip=True),"source_url":href})
    if len(rows)!=81: raise ValueError(f"Expected 81 chapters, found {len(rows)}")
    return rows

def write(rows):
    with SOURCE_CATALOG.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def page(rows):
    active={r["sequence"]:r for r in read_csv(CATALOG)}; payload=[]
    for row in rows:
        item=active.get(row["sequence"]); editor=""
        if item:
            path=BASE_DIR/f"{int(item['sequence']):02d}_{item['slug']}"/"editor.html"
            if path.exists(): editor=path.relative_to(BASE_DIR).as_posix()
        payload.append({**row,"editor":editor})
    return HTML.replace("__DATA__",json.dumps(payload,ensure_ascii=False).replace("</","<\\/"))

def main():
    p=argparse.ArgumentParser();p.add_argument("--source-html",type=Path);p.add_argument("--refresh",action="store_true");a=p.parse_args()
    if a.source_html: rows=parse(a.source_html.read_text(encoding="utf-8"));write(rows)
    elif a.refresh or not SOURCE_CATALOG.exists():
        r=requests.get(SOURCE_URL,headers={"User-Agent":"Mozilla/5.0"},timeout=30);r.raise_for_status();rows=parse(r.text);write(rows)
    else: rows=read_csv(SOURCE_CATALOG)
    OUTPUT.write_text(page(rows),encoding="utf-8");print(f"Wrote {OUTPUT} with {len(rows)} chapters")

HTML=r'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>《老子》章节选择器</title><style>
:root{--ink:#26241f;--muted:#756f64;--paper:#fffdf8;--line:#d8d0c1;--jade:#315b53;--gold:#aa7b2e}*{box-sizing:border-box}body{margin:0;background:#e9e5da;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}header{padding:40px max(24px,6vw);background:#27332f;color:#fff}h1{margin:8px 0;font:700 clamp(34px,6vw,62px)/1.08 "Songti SC",serif}header p{max-width:720px;color:#d7dfda;line-height:1.7}a{color:inherit}.shell{width:min(1050px,calc(100% - 32px));margin:22px auto 70px}.controls{position:sticky;top:0;z-index:4;display:grid;grid-template-columns:1fr 150px auto;gap:8px;padding:12px;background:#e9e5daf2}input,select,button{min-height:40px;padding:7px 10px;border:1px solid var(--line);border-radius:6px;background:#fff;font:inherit}button{cursor:pointer}.primary{background:var(--jade);border-color:var(--jade);color:#fff}.queue{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin:0 12px 18px;padding:14px;background:var(--paper);border:1px solid var(--line)}.queue input[type=text]{flex:1;min-width:260px}.summary{margin:10px 12px;color:var(--muted);font-size:13px}.section{margin:18px 12px;border:1px solid var(--line);background:var(--paper)}.section h2{display:flex;justify-content:space-between;margin:0;padding:14px 16px;background:#eef1eb;font:700 22px "Songti SC",serif}.chapter{display:grid;grid-template-columns:34px minmax(0,1fr) auto;gap:10px;align-items:center;padding:11px 15px;border-top:1px solid #e9e3d8}.chapter label{display:flex;gap:10px;align-items:center}.chapter input{min-height:0;width:17px;height:17px}.meta,.status{color:var(--muted);font-size:11px}.done{color:var(--jade);font-weight:700}.links{display:flex;gap:7px}.links a{padding:6px 8px;border:1px solid var(--line);border-radius:5px;text-decoration:none;font-size:12px}@media(max-width:680px){.controls{grid-template-columns:1fr}.chapter{grid-template-columns:28px 1fr}.links{grid-column:2}}
</style></head><body><header><a href="../index.html">← 返回校读书房</a><h1>《老子》章节选择器</h1><p>按道经、德经浏览八十一章，只将选中章节加入本地校读项目。</p></header><main class="shell"><div class="controls"><input id="search" type="search" placeholder="搜索章节"><select id="section"><option value="">全部</option><option>道经</option><option>德经</option></select><button id="selectVisible">选中当前结果</button></div><div class="queue"><input id="url" type="text" placeholder="粘贴《老子》章节链接"><button id="add">加入选择</button><label><input id="pdf" type="checkbox"> 同时生成 PDF</label><button class="primary" id="export">导出处理清单</button></div><p class="summary" id="summary"></p><div id="catalog"></div></main><script>
const DATA=__DATA__,chosen=new Set(JSON.parse(localStorage.getItem('laozi-selected')||'[]')),catalog=document.getElementById('catalog'),search=document.getElementById('search'),section=document.getElementById('section'),summary=document.getElementById('summary');function visible(){const q=search.value.trim();return DATA.filter(x=>(!section.value||x.section===section.value)&&(!q||x.title.includes(q)||x.sequence===q))}function save(){localStorage.setItem('laozi-selected',JSON.stringify([...chosen]));summary.textContent=`已选 ${chosen.size} 章 · 共 ${DATA.length} 章`}function render(){const ids=new Set(visible().map(x=>x.sequence));catalog.innerHTML='';for(const part of ['道经','德经']){const rows=DATA.filter(x=>x.section===part&&ids.has(x.sequence));if(!rows.length)continue;const box=document.createElement('section');box.className='section';box.innerHTML=`<h2><span>${part}</span><small>${rows.length} 章</small></h2>`;for(const x of rows){const row=document.createElement('div');row.className='chapter';row.innerHTML=`<span class="meta">${x.sequence}</span><label><input type="checkbox" data-id="${x.sequence}" ${chosen.has(x.sequence)?'checked':''}><span>${x.title} <small class="status ${x.editor?'done':''}">${x.editor?'已生成编辑器':'未处理'}</small></span></label><span class="links"><a href="${x.source_url}" target="_blank" rel="noreferrer">阅读原文</a>${x.editor?`<a href="${x.editor}" target="_blank">打开编辑器</a>`:''}</span>`;box.append(row)}catalog.append(box)}save()}catalog.onchange=e=>{if(!e.target.dataset.id)return;e.target.checked?chosen.add(e.target.dataset.id):chosen.delete(e.target.dataset.id);save()};search.oninput=render;section.onchange=render;document.getElementById('selectVisible').onclick=()=>{const ids=visible().map(x=>x.sequence),all=ids.every(x=>chosen.has(x));ids.forEach(x=>all?chosen.delete(x):chosen.add(x));render()};document.getElementById('add').onclick=()=>{const value=document.getElementById('url').value,x=DATA.find(x=>value===x.source_url||value.includes(x.source_url.split('/').pop()));if(!x)return alert('请粘贴本书的有效章节链接。');chosen.add(x.sequence);section.value=x.section;search.value='';render()};document.getElementById('export').onclick=()=>{if(!chosen.size)return alert('请先选择章节。');const data={version:1,createdAt:new Date().toISOString(),generatePdfs:document.getElementById('pdf').checked,chapters:DATA.filter(x=>chosen.has(x.sequence))},a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));a.download='laozi_processing_queue.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};render();
</script></body></html>'''
if __name__=="__main__":main()
