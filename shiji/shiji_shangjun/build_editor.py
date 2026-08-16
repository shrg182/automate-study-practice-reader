#!/usr/bin/env python3
"""Build the self-contained editor for 《史记·商君列传》."""
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parent / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))
from build_editor import build_html, load_terms

if __name__ == "__main__":
    text = (BASE_DIR / "shangjun_clean.txt").read_text(encoding="utf-8")
    terms = load_terms(BASE_DIR / "reading_terms.csv")
    output = build_html(
        text,
        terms,
        "https://www.guwendao.net/guwen/bookv_294ca85f5800.aspx",
        chapter_title="七十列传·商君列传第八",
        editor_title="《史记·商君列传》校读编辑器",
        storage_key="shiji-shangjun-editor-v3",
        file_stem="shangjun",
    )
    (BASE_DIR / "editor.html").write_text(output, encoding="utf-8")
    print(f"Output: {BASE_DIR / 'editor.html'}\nCharacters: {len(text)}\nTerms: {len(terms)}")
