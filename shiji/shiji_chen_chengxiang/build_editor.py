#!/usr/bin/env python3
"""Build the editor for 《史记·陈丞相世家》."""
from pathlib import Path
import json
import sys

from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parent / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))

from build_editor import (  # noqa: E402
    build_html,
    load_global_terms,
    load_inline_notes,
    load_reading_notes,
    load_review_notes,
    load_terms,
)


if __name__ == "__main__":
    text = (BASE_DIR / "chen_chengxiang_clean.txt").read_text(encoding="utf-8")
    terms = load_terms(BASE_DIR / "reading_terms.csv")
    inline_notes = load_inline_notes(BASE_DIR / "inline_notes.tsv")
    review_notes = load_review_notes(BASE_DIR / "review_notes.tsv")
    reading_notes = load_reading_notes(BASE_DIR / "chen_chengxiang_reading_notes.txt")
    seed_path = BASE_DIR / "chen_chengxiang_editor_seed.json"
    body_html = None
    if seed_path.exists():
        seed = json.loads(seed_path.read_text(encoding="utf-8"))
        soup = BeautifulSoup(seed.get("bodyHTML", ""), "html.parser")
        for reference in soup.select(".footnote-ref"):
            reference.replace_with(reference.get_text("", strip=True))
        body_html = str(soup)
    global_terms = load_global_terms(
        BASE_DIR.parents[2] / "project_dictionary" / "dictionary.csv", text, terms
    )
    output = build_html(
        text,
        terms,
        "https://www.guwendao.net/guwen/bookv_f135449a9ab5.aspx",
        chapter_title="三十世家·陈丞相世家第二十六",
        editor_title="《史记·陈丞相世家》校读编辑器",
        storage_key="shiji-chen-chengxiang-editor-v1",
        file_stem="chen_chengxiang",
        inline_notes=inline_notes,
        review_notes=review_notes,
        reading_notes=reading_notes,
        global_terms=global_terms,
        body_html=body_html,
    )
    output_path = BASE_DIR / "editor.html"
    output_path.write_text(output, encoding="utf-8")
    print(
        f"Output: {output_path}\nCharacters: {len(text)}\nTerms: {len(terms)}"
        f"\nGeneral dictionary hints: {len(global_terms)}"
        f"\nInline notes: {len(inline_notes)}\nPending review: {len(review_notes)}"
    )
