#!/usr/bin/env python3
"""Build the shared Shiji editor for 《淮阴侯列传》."""
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parent / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))
from build_editor import (
    build_html,
    load_inline_notes,
    load_reading_notes,
    load_review_notes,
    load_terms,
)

if __name__ == "__main__":
    text = (BASE_DIR / "huaiyin_hou_clean.txt").read_text(encoding="utf-8")
    terms = load_terms(BASE_DIR / "reading_terms.csv")
    inline_notes = load_inline_notes(BASE_DIR / "inline_notes.tsv")
    review_notes = load_review_notes(BASE_DIR / "review_notes.tsv")
    reading_notes = load_reading_notes(BASE_DIR / "huaiyin_hou_reading_notes.txt")
    output = build_html(
        text,
        terms,
        "https://www.guwendao.net/guwen/bookv_30856b7cc757.aspx",
        chapter_title="七十列传·淮阴侯列传第三十二",
        editor_title="《史记·淮阴侯列传》校读编辑器",
        storage_key="shiji-huaiyin-hou-editor-v5",
        file_stem="huaiyin_hou",
        inline_notes=inline_notes,
        review_notes=review_notes,
        reading_notes=reading_notes,
    )
    (BASE_DIR / "editor.html").write_text(output, encoding="utf-8")
    print(
        f"Output: {BASE_DIR / 'editor.html'}\n"
        f"Characters: {len(text)}\nTerms: {len(terms)}\nInline notes: {len(inline_notes)}\n"
        f"Pending review: {len(review_notes)}"
        f"\nReading notes: {len(reading_notes)}"
    )
