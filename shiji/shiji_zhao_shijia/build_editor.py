#!/usr/bin/env python3
"""Build the shared Shiji editor for 《赵世家》."""
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parent / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))
from build_editor import build_html, load_global_terms, load_inline_notes, load_reading_notes, load_review_notes, load_terms

if __name__ == "__main__":
    text = (BASE_DIR / "zhao_shijia_clean.txt").read_text(encoding="utf-8")
    terms = load_terms(BASE_DIR / "reading_terms.csv")
    global_terms = load_global_terms(
        BASE_DIR.parents[2] / "project_dictionary" / "dictionary.csv", text, terms
    )
    inline_notes = load_inline_notes(BASE_DIR / "inline_notes.tsv")
    review_notes = load_review_notes(BASE_DIR / "review_notes.tsv")
    reading_notes = load_reading_notes(BASE_DIR / "zhao_shijia_reading_notes.txt")
    output = build_html(
        text,
        terms,
        "https://www.guwendao.net/guwen/bookv_b0999505466b.aspx",
        chapter_title="三十世家·赵世家第十三",
        editor_title="《史记·赵世家》校读编辑器",
        storage_key="shiji-zhao-shijia-editor-v1",
        file_stem="zhao_shijia",
        inline_notes=inline_notes,
        review_notes=review_notes,
        reading_notes=reading_notes,
        global_terms=global_terms,
    )
    (BASE_DIR / "editor.html").write_text(output, encoding="utf-8")
    print(
        f"Output: {BASE_DIR / 'editor.html'}\nCharacters: {len(text)}"
        f"\nArticle terms: {len(terms)}\nGeneral dictionary hints: {len(global_terms)}"
    )
