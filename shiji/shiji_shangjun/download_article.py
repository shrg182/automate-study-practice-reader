#!/usr/bin/env python3
"""Download 《史记·商君列传》 from Guwendao."""
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parent / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))
from download_article import download, extract

URL = "https://www.guwendao.net/guwen/bookv_294ca85f5800.aspx"

if __name__ == "__main__":
    page_html = download(URL)
    title, text = extract(page_html)
    if title != "七十列传·商君列传第八":
        raise RuntimeError(f"Unexpected article title: {title}")
    (BASE_DIR / "sources").mkdir(exist_ok=True)
    (BASE_DIR / "sources" / "page.html").write_text(page_html, encoding="utf-8")
    (BASE_DIR / "source.txt").write_text(text, encoding="utf-8")
    clean = BASE_DIR / "shangjun_clean.txt"
    if not clean.exists():
        clean.write_text(text, encoding="utf-8")
    print(
        f"Title: {title}\n"
        f"Paragraphs: {text.count(chr(10) + chr(10)) + 1}\n"
        f"Characters: {len(text)}"
    )
