#!/usr/bin/env python3
"""Build the editor for 《史记·陈丞相世家》."""
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parent / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))

from build_editor import build_html, load_global_terms, load_terms  # noqa: E402


if __name__ == "__main__":
    text = (BASE_DIR / "chen_chengxiang_clean.txt").read_text(encoding="utf-8")
    terms = load_terms(BASE_DIR / "reading_terms.csv")
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
        global_terms=global_terms,
    )
    output_path = BASE_DIR / "editor.html"
    output_path.write_text(output, encoding="utf-8")
    print(
        f"Output: {output_path}\nCharacters: {len(text)}\nTerms: {len(terms)}"
        f"\nGeneral dictionary hints: {len(global_terms)}"
    )
