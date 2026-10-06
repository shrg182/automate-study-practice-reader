#!/usr/bin/env python3
"""Build a linked reading catalog for Qi Benyu's 2016 memoir."""

from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen
import json
import re
import sys

BASE = Path(__file__).resolve().parent
SOURCE = "https://www.marxists.org/chinese/reference-books/qibenyu/index.htm"


class ContentsParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.section = "卷首"; self.in_heading = False; self.link = None; self.text = []; self.entries = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h5": self.in_heading = True; self.text = []
        elif tag == "a" and re.fullmatch(r"(?:00[ab]|[1-5]-\d{2}|6)\.htm", attrs.get("href", "")): self.link = attrs["href"]; self.text = []

    def handle_data(self, data):
        if self.in_heading or self.link: self.text.append(data)

    def handle_endtag(self, tag):
        if tag == "h5" and self.in_heading:
            self.section = re.sub(r"\s+", " ", "".join(self.text)).strip(); self.in_heading = False
        elif tag == "a" and self.link:
            title = re.sub(r"\s+", " ", "".join(self.text)).strip()
            self.entries.append({"section": self.section, "title": title, "path": self.link, "url": urljoin(SOURCE, self.link)}); self.link = None


def build():
    raw = Path(sys.argv[1]).read_bytes() if len(sys.argv) > 1 else urlopen(SOURCE, timeout=30).read()
    parser = ContentsParser(); parser.feed(raw.decode("gb18030", errors="replace")); entries = parser.entries
    groups = []
    for section in dict.fromkeys(item["section"] for item in entries):
        cards = "".join(f'<article class="entry" data-search="{escape(item["title"].casefold(), quote=True)}"><span>{index:02d}</span><div><h2>{escape(item["title"])}</h2><small>{escape(section)}</small><textarea data-note="{escape(item["path"], quote=True)}" placeholder="阅读札记"></textarea></div><a href="reader_editor.html?path={escape(item["path"], quote=True)}&amp;title={escape(item["title"], quote=True)}&amp;section={escape(section, quote=True)}">阅读与编辑</a></article>' for index, item in enumerate(entries, 1) if item["section"] == section)
        groups.append(f'<section class="part"><h1>{escape(section)}</h1>{cards}</section>')
    page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>《戚本禹回忆录》阅读目录</title><link rel="stylesheet" href="../../workspace_theme.css"><style>*{{box-sizing:border-box}}body{{margin:0;background:#f5f3ed;color:#202124;font-family:Arial,"PingFang SC",sans-serif}}.topbar{{display:flex;gap:12px;align-items:center;flex-wrap:wrap;padding:12px 18px;background:#fff;border-bottom:1px solid #dadce0}}.topbar strong{{font-size:19px}}.topbar a{{color:#174ea6}}main{{width:min(1180px,calc(100% - 28px));margin:22px auto 90px}}.notice{{padding:15px;border-left:4px solid #b7791f;background:#fff8df;line-height:1.7}}.controls{{position:sticky;top:0;z-index:4;padding:10px 0;background:#f5f3edf2}}input{{width:100%;padding:12px 16px;border:1px solid #c8ccd0;border-radius:24px;font:inherit}}.part{{margin:24px 0}}.part>h1{{padding:10px 14px;background:#e7e7cd;font:700 20px "Songti SC",serif}}.entry{{display:grid;grid-template-columns:42px minmax(0,1fr) auto;gap:12px;align-items:start;padding:14px;border-bottom:1px solid #ddd;background:#fff}}.entry h2{{margin:0;font:700 17px/1.5 "Songti SC",serif}}.entry small{{color:#5f6368}}.entry>a{{padding:7px 10px;border:1px solid #b8c7df;border-radius:6px;color:#174ea6;text-decoration:none;white-space:nowrap}}textarea{{display:block;width:100%;min-height:58px;margin-top:9px;padding:8px;border:1px solid #dadce0;border-radius:6px;resize:vertical;font:14px/1.5 inherit}}@media(max-width:650px){{.entry{{grid-template-columns:30px 1fr}}.entry>a{{grid-column:2;justify-self:start}}}}</style><script src="../../workspace_skin.js"></script></head><body><header class="topbar"><a href="../../index.html#marxist_classics">← 返回书房</a><strong>《戚本禹回忆录》（2016）</strong><a href="{SOURCE}" target="_blank" rel="noreferrer">原始目录 ↗</a></header><main><p class="notice"><strong>链接阅读版：</strong>本页保存目录、阅读入口和浏览器本地札记，不复制现代出版物全文。原站说明文字版尚有错误，需要与原书核对。书中历史叙述代表作者观点，应与其他史料对读。</p><div class="controls"><input id="search" type="search" placeholder="搜索章节"></div>{''.join(groups)}</main><script>const key="qibenyu-linked-notes-v1";let notes={{}};try{{notes=JSON.parse(localStorage.getItem(key)||"{{}}")}}catch{{}}document.querySelectorAll("[data-note]").forEach(area=>{{area.value=notes[area.dataset.note]||"";area.addEventListener("input",()=>{{notes[area.dataset.note]=area.value;localStorage.setItem(key,JSON.stringify(notes))}})}});document.getElementById("search").addEventListener("input",event=>{{const q=event.target.value.trim().toLowerCase();document.querySelectorAll(".entry").forEach(row=>row.hidden=q&&!row.dataset.search.includes(q));document.querySelectorAll(".part").forEach(part=>part.hidden=![...part.querySelectorAll(".entry")].some(row=>!row.hidden))}});</script><script src="../../mobile_pwa.js"></script></body></html>'''
    (BASE / "index.html").write_text(page, encoding="utf-8"); (BASE / "catalog.json").write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built linked catalog with {len(entries)} pages")


if __name__ == "__main__": build()
