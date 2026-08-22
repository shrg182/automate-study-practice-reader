#!/usr/bin/env python3
"""Download 《史记·陈丞相世家》 from Guwendao."""
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parent / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))

from download_article import download, extract  # noqa: E402

URL = "https://www.guwendao.net/guwen/bookv_f135449a9ab5.aspx"

if __name__ == "__main__":
    page_html = download(URL)
    title, text = extract(page_html)
    (BASE_DIR / "sources").mkdir(exist_ok=True)
    (BASE_DIR / "sources" / "page.html").write_text(page_html, encoding="utf-8")
    (BASE_DIR / "source.txt").write_text(text, encoding="utf-8")
    clean = BASE_DIR / "chen_chengxiang_clean.txt"
    if not clean.exists():
        clean.write_text(text, encoding="utf-8")
    print(f"Title: {title}\nParagraphs: {text.count(chr(10) + chr(10)) + 1}\nCharacters: {len(text)}")
