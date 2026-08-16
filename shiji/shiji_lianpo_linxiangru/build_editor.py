#!/usr/bin/env python3
"""Build the Shiji editor using the shared Jianshang-derived settings."""
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parent / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))
from build_editor import build_html, load_terms

if __name__ == "__main__":
    text = (BASE_DIR / "lianpo_linxiangru_clean.txt").read_text(encoding="utf-8")
    terms = load_terms(BASE_DIR / "reading_terms.csv")
    output = build_html(
        text,
        terms,
        "https://www.guwendao.net/guwen/bookv_fe564cb98c22.aspx",
        chapter_title="七十列传·廉颇蔺相如列传第二十一",
        editor_title="《史记·廉颇蔺相如列传》校读编辑器",
        storage_key="shiji-lianpo-linxiangru-editor-v3",
        file_stem="lianpo_linxiangru",
    )
    (BASE_DIR / "editor.html").write_text(output, encoding="utf-8")
    print(
        f"Output: {BASE_DIR / 'editor.html'}\n"
        f"Characters: {len(text)}\nTerms: {len(terms)}"
    )
