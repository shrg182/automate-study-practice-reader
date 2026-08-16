#!/usr/bin/env python3
"""Shared selector and on-demand processing for structured Guwendao classics."""

from __future__ import annotations
import argparse,base64,csv,json,re,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup

PRACTICE=Path(__file__).resolve().parent

def read_csv(path):
    if not path.exists():return []
    with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))

def parse_contents(text,config):
    soup=BeautifulSoup(text,"html.parser");rows=[];groups=config["groups"]
    if len(groups)==1:
        candidates=soup.select('a[href*="/guwen/bookv_"]');sections=[(groups[0],candidates)]
    else:
        sections=[]
        for group in groups:
            heading=next((x for x in soup.find_all("strong") if x.get_text(" ",strip=True)==group),None)
            links=heading.parent.find_next_sibling().select('a[href*="/guwen/bookv_"]') if heading else []
            sections.append((group,links))
    for group,links in sections:
        for link in links:
            rows.append({"sequence":str(len(rows)+1),"group":group,"title":link.get_text(" ",strip=True),"source_url":requests.compat.urljoin(config["source_url"],link["href"])})
    if len(rows)!=config["expected_count"]:raise ValueError(f"Expected {config['expected_count']} entries, found {len(rows)}")
    return rows

def write_csv(path,rows,fields=None):
    fields=fields or list(rows[0])
    with path.open("w",encoding="utf-8",newline="") as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def build_selector(base,config,source_html=None,refresh=False):
    source_catalog=base/"source_catalog.csv"
    if source_html:rows=parse_contents(source_html.read_text(encoding="utf-8"),config);write_csv(source_catalog,rows)
    elif refresh or not source_catalog.exists():
        r=requests.get(config["source_url"],headers={"User-Agent":"Mozilla/5.0"},timeout=30);r.raise_for_status();rows=parse_contents(r.text,config);write_csv(source_catalog,rows)
    else:rows=read_csv(source_catalog)
    active={x["sequence"]:x for x in read_csv(base/"catalog.csv")};payload=[]
    for row in rows:
        item=active.get(row["sequence"]);editor=""
        if item:
            path=base/f"{int(item['sequence']):02d}_{item['slug']}"/"editor.html"
            if path.exists():editor=path.relative_to(base).as_posix()
        payload.append({**row,"editor":editor})
    html=SELECTOR.replace("__TITLE__",config["title"]).replace("__KEY__",config["key"]).replace("__DATA__",json.dumps(payload,ensure_ascii=False).replace("</","<\\/"))
    (base/"select_entries.html").write_text(html,encoding="utf-8");print(f"Wrote {base/'select_entries.html'} with {len(rows)} entries")

def build_editors(base,config):
    shared=PRACTICE/"shiji"/"shiji_lisheng_lujia";sys.path.insert(0,str(shared));from build_editor import build_html,load_global_terms,load_review_notes,load_terms
    for row in read_csv(base/"catalog.csv"):
        target=base/f"{int(row['sequence']):02d}_{row['slug']}";text=((target/"reading.txt") if (target/"reading.txt").exists() else (target/"original.txt")).read_text(encoding="utf-8");terms=load_terms(target/"reading_terms.csv")
        seed_path=target/f"{config['key']}_{int(row['sequence']):02d}_editor_seed.json";seed=json.loads(seed_path.read_text(encoding="utf-8")) if seed_path.exists() else {};initial_media=[]
        for item in seed.get("media",[]):
            media_path=target/item["path"];initial_media.append({**item,"dataUrl":f"data:{item['type']};base64,{base64.b64encode(media_path.read_bytes()).decode('ascii')}"})
        output=build_html(text,terms,row["source_url"],chapter_title=f"《{config['title']}·{row['title']}》",editor_title=f"《{config['title']}·{row['title']}》校读编辑器",storage_key=f"{config['key']}-{row['sequence']}-editor-v1",file_stem=f"{config['key']}_{int(row['sequence']):02d}",review_notes=load_review_notes(target/"review_notes.tsv"),reading_notes=seed.get("notes") or [],initial_media=initial_media,global_terms=load_global_terms(PRACTICE/"project_dictionary"/"dictionary.csv",text,terms),home_href="../../index.html",shared_library_href="",source_site_label="古文岛")
        if seed.get("bodyHTML"):
            output=re.sub(r'(<section id="editor" class="editor"[^>]*>).*?(</section>)',lambda match:match.group(1)+seed["bodyHTML"]+match.group(2),output,count=1,flags=re.DOTALL)
            footnotes=json.dumps(seed.get("footnotes") or [],ensure_ascii=False).replace("</","<\\/")
            output=re.sub(r"const INITIAL_FOOTNOTES=.*?; const INITIAL_READING_NOTES=",lambda _match:f"const INITIAL_FOOTNOTES={footnotes}; const INITIAL_READING_NOTES=",output,count=1)
        (target/"editor.html").write_text(output,encoding="utf-8");print(f"Built {target/'editor.html'}")

def process_queue(base,config,queue,validate_only=False):
    payload=json.loads(queue.read_text(encoding="utf-8"));wanted={str(x.get("sequence","")) for x in payload.get("entries",[])};sources={x["sequence"]:x for x in read_csv(base/"source_catalog.csv")}
    if payload.get("collection")!=config["key"] or not wanted or wanted-sources.keys():raise ValueError("Queue does not contain valid entries for this collection")
    if validate_only:print(f"Valid queue: {len(wanted)} entries");return
    catalog=read_csv(base/"catalog.csv");by={x["sequence"]:x for x in catalog};selected=[]
    for seq in sorted(wanted,key=int):
        src=sources[seq];row=by.get(seq) or {"sequence":seq,"group":src["group"],"title":src["title"],"slug":f"entry_{int(seq):02d}","source_url":src["source_url"],"status":"downloaded"}
        if seq not in by:catalog.append(row);by[seq]=row
        selected.append(row);target=base/f"{int(seq):02d}_{row['slug']}"
        if not (target/"source.json").exists():
            response=requests.get(row["source_url"],headers={"User-Agent":"Mozilla/5.0"},timeout=30);response.raise_for_status();soup=BeautifulSoup(response.text,"html.parser");body=soup.select_one(".contson")
            if body is None:raise ValueError(f"No original text found: {row['source_url']}")
            paragraphs=[p.get_text("",strip=True) for p in body.find_all("p",recursive=False)];text="\n\n".join(filter(None,paragraphs)) or body.get_text("",strip=True);target.mkdir(exist_ok=True);(target/"original.txt").write_text(text+"\n",encoding="utf-8");(target/"reading_terms.csv").write_text("term,pinyin,annotation,type\n",encoding="utf-8");(target/"review_notes.tsv").write_text("text\tissue\tstatus\n",encoding="utf-8");(target/"source.json").write_text(json.dumps({**row,"retrieved_at":datetime.now(timezone.utc).isoformat(),"source_site":"古文岛","characters":len(text)},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    write_csv(base/"catalog.csv",sorted(catalog,key=lambda x:int(x["sequence"])),["sequence","group","title","slug","source_url","status"]);build_editors(base,config);build_selector(base,config);subprocess.run([sys.executable,str(PRACTICE/"build_index.py")],check=True)
    if payload.get("generatePdfs"):make_pdfs(base,config,{int(x["sequence"]) for x in selected})

def make_pdfs(base,config,sequences=None):
    sys.path.insert(0,str(PRACTICE/"rongzhai_suibi"));from make_pdfs import print_one
    for row in read_csv(base/"catalog.csv"):
        if sequences and int(row["sequence"]) not in sequences:continue
        target=base/f"{int(row['sequence']):02d}_{row['slug']}";print_one(target/"editor.html",target/f"{config['key']}_{int(row['sequence']):02d}_annotated.pdf")

def run(base):
    config=json.loads((base/"collection.json").read_text(encoding="utf-8"));p=argparse.ArgumentParser();sub=p.add_subparsers(dest="command",required=True);b=sub.add_parser("build-selector");b.add_argument("--source-html",type=Path);b.add_argument("--refresh",action="store_true");q=sub.add_parser("process");q.add_argument("queue",nargs="?",type=Path);q.add_argument("--validate-only",action="store_true");m=sub.add_parser("make-pdfs");m.add_argument("--sequence",type=int,action="append");a=p.parse_args()
    if a.command=="build-selector":build_selector(base,config,a.source_html,a.refresh)
    elif a.command=="process":
        queue=a.queue
        if queue is None:
            choices=list((Path.home()/"Downloads").glob(f"{config['key']}_processing_queue*.json"));
            if not choices:raise FileNotFoundError("No processing queue found in Downloads")
            queue=max(choices,key=lambda x:x.stat().st_mtime)
        process_queue(base,config,queue,a.validate_only)
    else:make_pdfs(base,config,set(a.sequence or []))

SELECTOR=r'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>《__TITLE__》篇目选择器</title><style>:root{--ink:#28251f;--paper:#fffdf8;--line:#d8d0c1;--accent:#74402e;--muted:#756f64}*{box-sizing:border-box}body{margin:0;background:#ebe6db;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}header{padding:40px max(24px,6vw);background:#302a24;color:#fff}h1{margin:8px 0;font:700 clamp(34px,6vw,60px)/1.08 "Songti SC",serif}header p{color:#ddd3c7}a{color:inherit}.shell{width:min(1050px,calc(100% - 32px));margin:22px auto}.controls{position:sticky;top:0;z-index:4;display:grid;grid-template-columns:1fr 160px auto;gap:8px;padding:12px;background:#ebe6dbed}input,select,button{min-height:40px;padding:7px 10px;border:1px solid var(--line);border-radius:6px;background:#fff;font:inherit}button{cursor:pointer}.primary{background:var(--accent);color:#fff}.queue{display:flex;gap:9px;flex-wrap:wrap;margin:0 12px 18px;padding:14px;background:var(--paper);border:1px solid var(--line)}.queue input[type=text]{flex:1;min-width:250px}.summary{margin:10px 12px;color:var(--muted)}.group{margin:18px 12px;border:1px solid var(--line);background:var(--paper)}.group h2{display:flex;justify-content:space-between;margin:0;padding:14px 16px;background:#f2ede4;font:700 21px "Songti SC",serif}.entry{display:grid;grid-template-columns:34px minmax(0,1fr) auto;gap:10px;align-items:center;padding:11px 15px;border-top:1px solid #e9e3d8}.entry label{display:flex;gap:10px}.entry input{min-height:0;width:17px;height:17px}.meta,.status{color:var(--muted);font-size:11px}.done{color:#477052;font-weight:700}.links{display:flex;gap:7px}.links a{padding:6px 8px;border:1px solid var(--line);border-radius:5px;text-decoration:none;font-size:12px}@media(max-width:680px){.controls{grid-template-columns:1fr}.entry{grid-template-columns:28px 1fr}.links{grid-column:2}}</style></head><body><header><a href="../index.html">← 返回校读书房</a><h1>《__TITLE__》篇目选择器</h1><p>选择需要整理的篇目，导出处理清单后按需生成编辑器与 PDF。</p></header><main class="shell"><div class="controls"><input id="search" type="search" placeholder="搜索篇目"><select id="group"><option value="">全部分类</option></select><button id="selectVisible">选中当前结果</button></div><div class="queue"><input id="url" type="text" placeholder="粘贴篇目链接"><button id="add">加入选择</button><label><input id="pdf" type="checkbox"> 同时生成 PDF</label><button class="primary" id="export">导出处理清单</button></div><p class="summary" id="summary"></p><div id="catalog"></div></main><script>const DATA=__DATA__,KEY='__KEY__',chosen=new Set(JSON.parse(localStorage.getItem(KEY+'-selected')||'[]')),catalog=document.getElementById('catalog'),search=document.getElementById('search'),group=document.getElementById('group'),summary=document.getElementById('summary'),groups=[...new Set(DATA.map(x=>x.group))];groups.forEach(x=>group.add(new Option(x,x)));function visible(){const q=search.value.trim();return DATA.filter(x=>(!group.value||x.group===group.value)&&(!q||x.title.includes(q)||x.sequence===q))}function save(){localStorage.setItem(KEY+'-selected',JSON.stringify([...chosen]));summary.textContent=`已选 ${chosen.size} 篇 · 共 ${DATA.length} 篇`}function render(){const ids=new Set(visible().map(x=>x.sequence));catalog.innerHTML='';for(const part of groups){const rows=DATA.filter(x=>x.group===part&&ids.has(x.sequence));if(!rows.length)continue;const box=document.createElement('section');box.className='group';box.innerHTML=`<h2><span>${part}</span><small>${rows.length} 篇</small></h2>`;for(const x of rows){const row=document.createElement('div');row.className='entry';row.innerHTML=`<span class="meta">${x.sequence}</span><label><input type="checkbox" data-id="${x.sequence}" ${chosen.has(x.sequence)?'checked':''}><span>${x.title} <small class="status ${x.editor?'done':''}">${x.editor?'已生成编辑器':'未处理'}</small></span></label><span class="links"><a href="${x.source_url}" target="_blank">阅读原文</a>${x.editor?`<a href="${x.editor}" target="_blank">打开编辑器</a>`:''}</span>`;box.append(row)}catalog.append(box)}save()}catalog.onchange=e=>{if(!e.target.dataset.id)return;e.target.checked?chosen.add(e.target.dataset.id):chosen.delete(e.target.dataset.id);save()};search.oninput=render;group.onchange=render;document.getElementById('selectVisible').onclick=()=>{const ids=visible().map(x=>x.sequence),all=ids.every(x=>chosen.has(x));ids.forEach(x=>all?chosen.delete(x):chosen.add(x));render()};document.getElementById('add').onclick=()=>{const value=document.getElementById('url').value,x=DATA.find(x=>value===x.source_url||value.includes(x.source_url.split('/').pop()));if(!x)return alert('请粘贴本书的有效篇目链接。');chosen.add(x.sequence);group.value=x.group;search.value='';render()};document.getElementById('export').onclick=()=>{if(!chosen.size)return alert('请先选择篇目。');const data={version:1,collection:KEY,createdAt:new Date().toISOString(),generatePdfs:document.getElementById('pdf').checked,entries:DATA.filter(x=>chosen.has(x.sequence))},a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));a.download=KEY+'_processing_queue.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};render();</script></body></html>'''
