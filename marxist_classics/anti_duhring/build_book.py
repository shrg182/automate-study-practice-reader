#!/usr/bin/env python3
"""Build the English-first Anti-Dühring Reader pilot."""
from __future__ import annotations

import argparse
import csv
from html import escape
import json
from pathlib import Path
import re
import ssl
import sys
from urllib.request import Request, urlopen

import certifi
from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parent
SHARED = BASE.parents[1] / "shiji" / "shiji_lisheng_lujia"
CAPITAL = BASE.parent / "capital"
sys.path[:0] = [str(SHARED), str(CAPITAL)]
from build_editor import build_html, load_inline_notes, load_reading_notes, load_review_notes, load_terms  # noqa: E402
from import_pilot import add_chinese_support  # noqa: E402

ENGLISH_INDEX = "https://www.marxists.org/archive/marx/works/1877/anti-duhring/index.htm"
ENGLISH_PDF = "https://www.marxists.org/archive/marx/works/download/pdf/anti_duhring.pdf"
CHINESE_INDEX = "https://www.marxists.org/chinese/marx-engels/20/index.htm"
CHINESE_PDF = "https://www.marxists.org/chinese/pdf/marx-engels/me20.pdf"

KEYWORDS = {
    "00_prefaces": ["反杜林论 三版序言", "辩证方法", "共产主义世界观"],
    "01_introduction_general": ["反杜林论 引论 概论", "现代社会主义", "辩证法"],
    "02_what_duhring_promises": ["杜林先生许下了什么诺言", "体系", "终极真理"],
    "03_classification_apriorism": ["分类 先验主义", "现实和思维", "原则"],
    "04_world_schematism": ["世界模式论", "数学 抽象", "世界的统一性"],
}
CHINESE_RANGES = {
    "00_prefaces": ("三版序言", None),
    "01_introduction_general": ("一、概论", "二、杜林先生许下了什么诺言"),
    "02_what_duhring_promises": ("二、杜林先生许下了什么诺言", None),
    "03_classification_apriorism": ("三、分类。先验主义", "四、世界模式论"),
    "04_world_schematism": ("四、世界模式论", "五、自然哲学。时间和空间"),
}


def download(url: str, encoding: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 AntiDuhringReader/1.0"})
    with urlopen(request, timeout=45, context=ssl.create_default_context(cafile=certifi.where())) as response:
        return response.read().decode(encoding, errors="replace")


def extract(page: str) -> str:
    soup = BeautifulSoup(page, "html.parser")
    for node in soup.select("script,style,nav,header,footer,.skip,.footer,.navbar,sup"):
        node.decompose()
    root = soup.find("main") or soup.body or soup
    blocks = []
    for node in root.find_all(["h1", "h2", "h3", "h4", "p", "blockquote", "li"]):
        if node.find_parent(["p", "blockquote", "li"]):
            continue
        text = re.sub(r"\s+", " ", node.get_text(" ", strip=True)).strip()
        if text and text not in blocks[-1:]:
            blocks.append(text)
    result = "\n\n".join(blocks)
    if len(result) >= 200:
        return result
    # Older Chinese MIA pages use table cells, bare text, and BR elements
    # rather than semantic paragraphs.
    raw = root.get_text("\n", strip=True)
    lines = [re.sub(r"\s+", " ", line).strip() for line in raw.splitlines()]
    return "\n\n".join(line for line in lines if line)


def support_files(folder: Path) -> None:
    defaults = {
        "reading_terms.csv": "term,pinyin,meaning,level,category,notes\n",
        "inline_notes.tsv": "phrase\tnote\n",
        "review_notes.tsv": "phrase\tnote\n",
        "reading_notes.txt": "",
    }
    for name, content in defaults.items():
        path = folder / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")


def chapter_aligned_chinese(text: str, slug: str) -> str:
    bounds = CHINESE_RANGES.get(slug)
    if not bounds:
        return text
    start_label, end_label = bounds
    start = text.rfind(start_label)
    if start < 0:
        return text
    end = text.find(end_label, start + len(start_label)) if end_label else -1
    return text[start:end if end >= 0 else None].strip()


def selection_page(rows: list[dict[str, str]]) -> str:
    cards = "".join(
        f'<article><b>{int(row["sequence"]):02d}</b><div><strong>{escape(row["title"])}</strong><small>{escape(row["focus"])}</small></div><a href="readings/{escape(row["slug"])}/editor.html">Open Reader</a></article>'
        for row in rows
    )
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Anti-Dühring · English-First Reader</title><link rel="stylesheet" href="../../workspace_theme.css"><style>body{{margin:0;background:#f1f3f4;color:#202124;font-family:Arial,sans-serif}}main{{width:min(980px,calc(100% - 28px));margin:28px auto}}header,section{{padding:26px;background:#fff;border:1px solid #dadce0;border-radius:12px}}header h1{{margin:8px 0;font:700 clamp(34px,6vw,58px)/1.1 Georgia,serif}}header p{{max-width:780px;line-height:1.65;color:#5f6368}}header a,article a{{color:#174ea6}}section{{display:grid;gap:9px;margin-top:16px}}article{{display:grid;grid-template-columns:38px 1fr auto;gap:12px;align-items:center;padding:13px;border:1px solid #e0e3e7;border-radius:8px}}article small{{display:block;margin-top:4px;color:#5f6368}}article a{{padding:7px 10px;border:1px solid #c5d4ed;border-radius:7px;text-decoration:none}}@media(max-width:650px){{article{{grid-template-columns:32px 1fr}}article a{{grid-column:2;justify-self:start}}}}</style></head><body><main><header><a href="../../index.html">← Reader library</a><h1>Anti-Dühring</h1><p>Frederick Engels · English-first close reading, with section-aligned Chinese reference support. The complete work contains prefaces, an introduction, Part I: Philosophy, Part II: Political Economy, and Part III: Socialism.</p><p><a href="{ENGLISH_INDEX}" target="_blank" rel="noreferrer">Complete English contents ↗</a> · <a href="{ENGLISH_PDF}" target="_blank" rel="noreferrer">English PDF ↗</a> · <a href="{CHINESE_INDEX}" target="_blank" rel="noreferrer">Chinese contents ↗</a> · <a href="{CHINESE_PDF}" target="_blank" rel="noreferrer">Chinese PDF ↗</a></p></header><section>{cards}</section></main><script src="../../workspace_skin.js"></script><script src="../../mobile_pwa.js"></script></body></html>'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local", action="store_true")
    parser.add_argument("--refresh-clean", action="store_true")
    args = parser.parse_args()
    with (BASE / "pilot_catalog.csv").open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    cache: dict[tuple[str, str], str] = {}
    def cached_page(url: str, encoding: str) -> str:
        key = (url, encoding)
        if key not in cache:
            cache[key] = download(url, encoding)
        return cache[key]
    for row in rows:
        folder = BASE / "readings" / row["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        if args.local:
            english = (folder / "source.txt").read_text(encoding="utf-8").strip()
            chinese = (folder / "chinese_support.txt").read_text(encoding="utf-8").strip()
        else:
            english = extract(cached_page(row["english_url"], "iso-8859-1"))
            chinese = extract(cached_page(row["chinese_url"], "gb18030"))
        chinese = chapter_aligned_chinese(chinese, row["slug"])
        if len(english) < 500 or len(chinese) < 200:
            raise ValueError(f'Extraction too short for {row["slug"]}: {len(english)} / {len(chinese)}')
        (folder / "source.txt").write_text(english + "\n", encoding="utf-8")
        (folder / "chinese_support.txt").write_text(chinese + "\n", encoding="utf-8")
        clean = folder / "clean.txt"
        if args.refresh_clean or not clean.exists():
            clean.write_text(english + "\n", encoding="utf-8")
        support_files(folder)
        metadata = {**row, "author": "Frederick Engels", "language": "en", "english_index": ENGLISH_INDEX, "english_pdf": ENGLISH_PDF, "chinese_role": "section-aligned support reference"}
        (folder / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        output = build_html(english, load_terms(folder / "reading_terms.csv"), row["english_url"], chapter_title=row["title"], editor_title=f'{row["title"]} · Anti-Dühring · English-First Reader', storage_key=f'anti-duhring-{row["slug"]}-v1', file_stem=f'anti_duhring_{row["slug"]}', inline_notes=load_inline_notes(folder / "inline_notes.tsv"), review_notes=load_review_notes(folder / "review_notes.tsv"), reading_notes=load_reading_notes(folder / "reading_notes.txt"), global_terms=[], home_href="../../../../index.html", theme_href="../../../../workspace_theme.css", shared_library_href="../../select_readings.html", shared_library_label="Anti-Dühring Reading Plan", source_site_label="Marxists Internet Archive")
        import_pilot_row = {**row, "chinese_url": row["chinese_url"]}
        import import_pilot
        import_pilot.CHINESE_KEYWORDS[row["slug"]] = KEYWORDS[row["slug"]]
        output = add_chinese_support(output, chinese, import_pilot_row).replace("capital-bilingual-", "anti-duhring-bilingual-").replace("Capital Reading Plan", "Anti-Dühring Reading Plan")
        (folder / "editor.html").write_text(output, encoding="utf-8")
        print(f'{row["sequence"]}. {row["title"]}: {len(english)} English / {len(chinese)} Chinese characters')
    (BASE / "select_readings.html").write_text(selection_page(rows), encoding="utf-8")


if __name__ == "__main__":
    main()
