#!/usr/bin/env python3
"""Import the English-first *Capital* Volume I pilot from MIA."""
from __future__ import annotations

import csv
import argparse
from html import escape
import json
from pathlib import Path
import re
import ssl
import sys
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

import certifi
from bs4 import BeautifulSoup, NavigableString, Tag

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parents[1] / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))
from build_editor import build_html, load_inline_notes, load_reading_notes, load_review_notes, load_terms  # noqa: E402


def download(url: str, encoding: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 CapitalReader/1.0"})
    context = ssl.create_default_context(cafile=certifi.where())
    with urlopen(request, timeout=40, context=context) as response:
        return response.read().decode(encoding, errors="replace")


def clean_text(nodes: list[Tag]) -> str:
    paragraphs: list[str] = []
    for node in nodes:
        clone = BeautifulSoup(str(node), "html.parser")
        for unwanted in clone.select(".note, .enote, script, style"):
            unwanted.decompose()
        text = re.sub(r"\s+", " ", clone.get_text(" ", strip=True)).strip()
        if text and text != "Contents":
            paragraphs.append(text)
    return "\n\n".join(paragraphs)


def extract_english(page: str, anchor: str) -> str:
    soup = BeautifulSoup(page, "html.parser")
    if not anchor:
        nodes = []
        for node in soup.body.find_all(["p", "blockquote"], recursive=False):
            if node.get("class") and any(value in {"title", "skip"} for value in node.get("class", [])):
                continue
            if node.find("a", attrs={"name": "1"}):
                break
            nodes.append(node)
        return clean_text(nodes)
    marker = soup.find("a", attrs={"name": anchor})
    if marker is None:
        raise ValueError(f"Missing section anchor {anchor}")
    nodes = []
    for node in marker.find_all_next():
        if node is not marker and node.name == "a" and re.fullmatch(r"S[1-4]", node.get("name", "")):
            break
        if node.name == "h4" and node.get_text(" ", strip=True).lower() == "footnotes":
            break
        if node.name in {"p", "h5", "h6", "blockquote"} and not node.find_parent(["p", "h5", "h6", "blockquote"]):
            nodes.append(node)
    return clean_text(nodes)


CHINESE_SECTIONS = {
    "00_preface_1867": ("1", "2"),
    "01_commodity_factors": ("1", "2"),
    "02_twofold_labour": ("2", "3"),
    "03_form_of_value": ("3", "20"),
    "04_commodity_fetishism": ("20", "_ftn1"),
}

CHINESE_KEYWORDS = {
    "00_preface_1867": ["资本论 第一版序言", "万事开头难", "商品 价值形式"],
    "01_commodity_factors": ["商品的两个因素", "使用价值", "交换价值 社会必要劳动时间"],
    "02_twofold_labour": ["体现在商品中的劳动的二重性", "具体劳动", "抽象人类劳动"],
    "03_form_of_value": ["价值形式", "相对价值形式", "等价形式 货币形式"],
    "04_commodity_fetishism": ["商品的拜物教性质及其秘密", "商品拜物教", "劳动的社会性质"],
}


def extract_chinese(page: str, slug: str) -> str:
    start_name, end_name = CHINESE_SECTIONS[slug]
    soup = BeautifulSoup(page, "html.parser")
    start = soup.find("a", attrs={"name": start_name})
    if start is None:
        return ""
    parts: list[str] = []
    for sibling in start.next_siblings:
        if isinstance(sibling, Tag) and sibling.find("a", attrs={"name": end_name}) is not None:
            break
        if isinstance(sibling, Tag) and sibling.name == "a" and sibling.get("name") == end_name:
            break
        if isinstance(sibling, NavigableString):
            value = re.sub(r"\s+", " ", str(sibling)).strip()
        elif isinstance(sibling, Tag):
            clone = BeautifulSoup(str(sibling), "html.parser")
            for unwanted in clone.select("script, style, sup"):
                unwanted.decompose()
            value = re.sub(r"\s+", " ", clone.get_text(" ", strip=True)).strip()
        else:
            value = ""
        if value:
            parts.append(value)
    return "\n\n".join(parts)


def add_chinese_support(output: str, chinese_text: str, row: dict[str, str]) -> str:
    keywords = CHINESE_KEYWORDS[row["slug"]]
    keyword_html = "".join(f"<li>{escape(keyword)}</li>" for keyword in keywords)
    search_url = "https://www.google.com/search?q=" + quote_plus(" ".join(keywords))
    if chinese_text:
        paragraphs = "".join(f"<p>{escape(paragraph)}</p>" for paragraph in chinese_text.split("\n\n") if paragraph.strip())
        body = f'<div class="chinese-text">{paragraphs}</div>'
        status = "已从中文版原文提取对应章节；中英文按章节对应，尚未逐句对齐。"
    else:
        body = '<p class="chinese-empty">未能从保存的页面提取对应段落，可使用下列关键词继续查找。</p>'
        status = "暂无可渲染的中文段落。"
    card = f'''<section class="card chinese-support-card"><details><summary><span>中文参考</span><small>{escape(status)}</small></summary>{body}<div class="chinese-support-footer"><strong>检索关键词</strong><ul>{keyword_html}</ul><div><a href="{escape(row['chinese_url'], quote=True)}" target="_blank" rel="noreferrer">打开中文原文 ↗</a><a href="{escape(search_url, quote=True)}" target="_blank" rel="noreferrer">Google 搜索 ↗</a></div></div></details></section>'''
    output = output.replace('<section class="card"><h2>当前选择', card + '<section class="card"><h2>当前选择', 1)
    css = '''
.chinese-support-card details>summary{display:grid;gap:4px;cursor:pointer;list-style:none}.chinese-support-card summary::-webkit-details-marker{display:none}.chinese-support-card summary span{font-size:16px;font-weight:700}.chinese-support-card summary span::after{float:right;content:"▾"}.chinese-support-card details:not([open]) summary span::after{transform:rotate(-90deg)}.chinese-support-card summary small{color:var(--muted);font-size:11px;line-height:1.45}.chinese-text{max-height:55vh;margin-top:12px;padding:10px;overflow:auto;border:1px solid var(--line);background:#fff}.chinese-text p{margin:0 0 10px;color:var(--ink);font-size:14px;line-height:1.8}.chinese-text p:last-child{margin-bottom:0}.chinese-empty{padding:9px;background:var(--panel)}.chinese-support-footer{margin-top:10px;padding-top:10px;border-top:1px solid var(--line)}.chinese-support-footer strong{font-size:12px}.chinese-support-footer ul{margin:7px 0;padding-left:20px}.chinese-support-footer li{font-size:12px;line-height:1.55}.chinese-support-footer div{display:flex;gap:7px;flex-wrap:wrap}.chinese-support-footer a{padding:6px 9px;border:1px solid var(--line);border-radius:5px;color:var(--blue);text-decoration:none;font-size:11px;font-weight:700}
'''
    return output.replace("</style>", css + "</style>", 1)


def ensure_support_files(project: Path) -> None:
    defaults = {
        "reading_terms.csv": "term,pinyin,meaning,level,category,notes\n",
        "inline_notes.tsv": "phrase\tnote\n",
        "review_notes.tsv": "phrase\tnote\n",
        "reading_notes.txt": "",
    }
    for name, content in defaults.items():
        path = project / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-clean", action="store_true", help="replace derived clean text from the source")
    args = parser.parse_args()
    with (BASE_DIR / "pilot_catalog.csv").open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    cache: dict[str, str] = {}
    chinese_cache: dict[str, str] = {}
    for row in rows:
        project = BASE_DIR / "volume_01" / row["slug"]
        sources = project / "sources"
        sources.mkdir(parents=True, exist_ok=True)
        page = cache.setdefault(row["english_url"], download(row["english_url"], "iso-8859-1"))
        chinese = chinese_cache.setdefault(row["chinese_url"], download(row["chinese_url"], "gb18030"))
        text = extract_english(page, row["english_anchor"])
        chinese_text = extract_chinese(chinese, row["slug"])
        if len(text) < 200:
            raise ValueError(f'Extraction too short for {row["slug"]}: {len(text)}')
        (sources / "english_page.html").write_text(page, encoding="utf-8")
        (sources / "chinese_reference_page.html").write_text(chinese, encoding="utf-8")
        (project / "chinese_support.txt").write_text((chinese_text or "\n".join(CHINESE_KEYWORDS[row["slug"]])) + "\n", encoding="utf-8")
        (project / "source.txt").write_text(text + "\n", encoding="utf-8")
        clean = project / "clean.txt"
        if args.refresh_clean or not clean.exists():
            clean.write_text(text + "\n", encoding="utf-8")
        metadata = {**row, "language": "en", "translation": "Samuel Moore and Edward Aveling (1887), edited by Friedrich Engels", "chinese_role": "support-reference-section-aligned" if chinese_text else "support-keywords"}
        (project / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        ensure_support_files(project)
        output = build_html(text, load_terms(project / "reading_terms.csv"), row["english_url"], chapter_title=row["title"], editor_title=f'{row["title"]} · English-First Reader', storage_key=f'capital-v1-{row["slug"]}-v1', file_stem=f'capital_v1_{row["slug"]}', inline_notes=load_inline_notes(project / "inline_notes.tsv"), review_notes=load_review_notes(project / "review_notes.tsv"), reading_notes=load_reading_notes(project / "reading_notes.txt"), global_terms=[], home_href="../../../../index.html", theme_href="../../../../workspace_theme.css", shared_library_href="../../select_readings.html", shared_library_label="Capital Reading Plan", source_site_label="Marxists Internet Archive")
        output = add_chinese_support(output, chinese_text, row)
        (project / "editor.html").write_text(output, encoding="utf-8")
        print(f'{row["sequence"]}. {row["title"]}: {len(text)} characters')


if __name__ == "__main__":
    main()
