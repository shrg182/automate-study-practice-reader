#!/usr/bin/env python3
"""Build selector pages for collections that accept reader-supplied article URLs."""

from __future__ import annotations

from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re


BASE_DIR = Path(__file__).resolve().parent
COLLECTIONS = {
    "liaozhai_stories": ("《聊斋志异》", "篇目", "文言小说"),
    "shiji": ("《史记》", "篇目", "本纪、世家与列传"),
}


class HeadingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_h1 = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "h1" and not self.parts:
            self.in_h1 = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1":
            self.in_h1 = False

    def handle_data(self, data: str) -> None:
        if self.in_h1:
            self.parts.append(data)


def editor_data(editor: Path, root: Path) -> dict[str, str]:
    text = editor.read_text(encoding="utf-8", errors="replace")
    parser = HeadingParser()
    parser.feed(text)
    title = re.sub(r"\s+", " ", "".join(parser.parts)).strip() or editor.parent.name.replace("_", " ")
    source = re.search(r'const SOURCE_URL=(?:"([^"]*)"|\'([^\']*)\')', text)
    return {
        "id": editor.parent.name,
        "title": title,
        "source_url": next((value for value in source.groups() if value), "") if source else "",
        "editor": editor.relative_to(root).as_posix(),
    }


def build(key: str, title: str, unit: str, description: str) -> None:
    root = BASE_DIR / key
    rows = [editor_data(path, root) for path in sorted(root.glob("*/editor.html"))]
    data = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    output = root / "select_articles.html"
    output.write_text(
        TEMPLATE.replace("__TITLE__", escape(title)).replace("__UNIT__", unit)
        .replace("__DESCRIPTION__", description).replace("__KEY__", key).replace("__DATA__", data),
        encoding="utf-8",
    )
    print(f"Wrote {output} with {len(rows)} existing entries")


TEMPLATE = r'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>__TITLE____UNIT__选择器</title><style>
:root{--ink:#28251f;--paper:#fffdf8;--line:#d8d0c1;--accent:#74402e;--muted:#756f64}*{box-sizing:border-box}body{margin:0;background:#ebe6db;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}header{padding:40px max(24px,6vw);background:#302a24;color:#fff}h1{margin:8px 0;font:700 clamp(34px,6vw,60px)/1.08 "Songti SC",serif}header p{max-width:760px;color:#ddd3c7;line-height:1.7}a{color:inherit}.shell{width:min(1050px,calc(100% - 32px));margin:22px auto 70px}.controls{position:sticky;top:0;z-index:4;display:flex;gap:8px;padding:12px;background:#ebe6dbed}.controls input{flex:1}input,button{min-height:40px;padding:7px 10px;border:1px solid var(--line);border-radius:6px;background:#fff;font:inherit}button{cursor:pointer}.primary{border-color:var(--accent);background:var(--accent);color:#fff}.queue{display:grid;grid-template-columns:1fr 1fr auto;gap:9px;margin:0 12px 18px;padding:14px;background:var(--paper);border:1px solid var(--line)}.queue p{grid-column:1/-1;margin:0;color:var(--muted);font-size:13px}.summary{margin:10px 12px;color:var(--muted)}.group{margin:18px 12px;border:1px solid var(--line);background:var(--paper)}.group h2{display:flex;justify-content:space-between;margin:0;padding:14px 16px;background:#f2ede4;font:700 21px "Songti SC",serif}.entry{display:grid;grid-template-columns:34px minmax(0,1fr) auto;gap:10px;align-items:center;padding:11px 15px;border-top:1px solid #e9e3d8}.entry label{display:flex;gap:10px}.entry input{min-height:0;width:17px;height:17px}.meta,.status{color:var(--muted);font-size:11px}.done{color:#477052;font-weight:700}.links{display:flex;gap:7px}.links a{padding:6px 8px;border:1px solid var(--line);border-radius:5px;text-decoration:none;font-size:12px}@media(max-width:680px){.controls{position:static;flex-direction:column}.queue{grid-template-columns:1fr}.queue p{grid-column:auto}.entry{grid-template-columns:28px 1fr}.links{grid-column:2}}</style></head><body><header><a href="../index.html">← 返回校读书斋</a><h1>__TITLE____UNIT__选择器</h1><p>浏览已有的__DESCRIPTION__，也可粘贴新的原文链接并导出处理清单。</p></header><main class="shell"><div class="controls"><input id="search" type="search" placeholder="搜索__UNIT__"><button id="selectVisible">选中当前结果</button><button class="primary" id="export">导出处理清单</button></div><div class="queue"><p>添加尚未收录的__UNIT__</p><input id="newTitle" type="text" placeholder="__UNIT__标题"><input id="newUrl" type="url" placeholder="原文网址（https://…）"><button id="add">加入选择</button></div><p class="summary" id="summary"></p><section class="group"><h2><span>__TITLE__</span><small id="visibleCount"></small></h2><div id="catalog"></div></section></main><script>
const DATA=__DATA__,KEY='__KEY__',CUSTOM_KEY=KEY+'-custom-selection',chosen=new Set(JSON.parse(localStorage.getItem(KEY+'-selected')||'[]')),custom=JSON.parse(localStorage.getItem(CUSTOM_KEY)||'[]'),catalog=document.getElementById('catalog'),search=document.getElementById('search'),summary=document.getElementById('summary');function all(){return [...DATA,...custom]}function visible(){const q=search.value.trim().toLocaleLowerCase();return all().filter(x=>!q||x.title.toLocaleLowerCase().includes(q)||x.source_url.toLocaleLowerCase().includes(q))}function save(){localStorage.setItem(KEY+'-selected',JSON.stringify([...chosen]));localStorage.setItem(CUSTOM_KEY,JSON.stringify(custom));summary.textContent=`已选 ${chosen.size} __UNIT__ · 已有 ${DATA.length} __UNIT__ · 待处理 ${custom.length} __UNIT__`}function render(){const rows=visible();document.getElementById('visibleCount').textContent=`${rows.length} __UNIT__`;catalog.innerHTML='';rows.forEach((x,index)=>{const row=document.createElement('div');row.className='entry';row.innerHTML=`<span class="meta">${String(index+1).padStart(2,'0')}</span><label><input type="checkbox" data-id="${x.id}" ${chosen.has(x.id)?'checked':''}><span>${x.title} <small class="status ${x.editor?'done':''}">${x.editor?'已生成编辑器':'待处理'}</small></span></label><span class="links">${x.source_url?`<a href="${x.source_url}" target="_blank" rel="noreferrer">阅读原文</a>`:''}${x.editor?`<a href="${x.editor}?view=annotated" target="_blank">打开编辑器</a>`:''}</span>`;catalog.append(row)});save()}catalog.onchange=e=>{if(!e.target.dataset.id)return;e.target.checked?chosen.add(e.target.dataset.id):chosen.delete(e.target.dataset.id);save()};search.oninput=render;document.getElementById('selectVisible').onclick=()=>{const ids=visible().map(x=>x.id),selected=ids.length&&ids.every(x=>chosen.has(x));ids.forEach(x=>selected?chosen.delete(x):chosen.add(x));render()};document.getElementById('add').onclick=()=>{const title=document.getElementById('newTitle').value.trim(),source_url=document.getElementById('newUrl').value.trim();if(!title||!/^https?:\/\//i.test(source_url))return alert('请填写标题和有效的原文网址。');const id='custom-'+Date.now();custom.push({id,title,source_url,editor:''});chosen.add(id);document.getElementById('newTitle').value='';document.getElementById('newUrl').value='';search.value='';render()};document.getElementById('export').onclick=()=>{const entries=all().filter(x=>chosen.has(x.id));if(!entries.length)return alert('请先选择__UNIT__。');const payload={version:1,collection:KEY,createdAt:new Date().toISOString(),entries},a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));a.download=KEY+'_processing_queue.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};render();
</script></body></html>'''


if __name__ == "__main__":
    for collection_key, values in COLLECTIONS.items():
        build(collection_key, *values)
