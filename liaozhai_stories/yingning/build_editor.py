#!/usr/bin/env python3
"""Build the shared rich-text reading editor for 《聊斋志异·婴宁》."""

from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parents[1] / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))

from build_editor import build_html, load_global_terms, load_terms  # noqa: E402


if __name__ == "__main__":
    text = (BASE_DIR / "yingning.txt").read_text(encoding="utf-8")
    terms = load_terms(BASE_DIR / "yingning_rare_words.csv")
    for term in terms:
        term.setdefault("type", "rare_word")
    global_terms = load_global_terms(
        BASE_DIR.parents[2] / "project_dictionary" / "dictionary.csv", text, terms
    )
    output = build_html(
        text,
        terms,
        "https://liaozhai.5000yan.com/19984.html",
        chapter_title="《聊斋志异·婴宁》",
        editor_title="《聊斋志异·婴宁》校读编辑器",
        storage_key="liaozhai-yingning-editor-v1",
        file_stem="yingning",
        global_terms=global_terms,
        shared_library_href="",
        source_site_label="五千言",
    )
    output_path = BASE_DIR / "editor.html"
    output_path.write_text(output, encoding="utf-8")
    print(f"Output: {output_path}\nCharacters: {len(text)}\nTerms: {len(terms)}")
