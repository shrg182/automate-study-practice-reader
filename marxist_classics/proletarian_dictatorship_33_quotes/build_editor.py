#!/usr/bin/env python3
"""Build the reading editor for the 33-quotation supplementary article."""

from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parent
SHARED_EDITOR_DIR = BASE_DIR.parents[1] / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_EDITOR_DIR))

from build_editor import build_html, load_global_terms, load_terms


if __name__ == "__main__":
    text_path = BASE_DIR / "proletarian_dictatorship_33_quotes_clean.txt"
    terms_path = BASE_DIR / "reading_terms.csv"
    text = text_path.read_text(encoding="utf-8")
    terms = load_terms(terms_path)
    global_terms = load_global_terms(
        BASE_DIR.parents[2] / "project_dictionary" / "dictionary.csv", text, terms
    )
    output = build_html(
        text,
        terms,
        "https://m.wyzxwk.com/Article/shushe/2011/08/250089.html",
        chapter_title="马克思恩格斯列宁论无产阶级专政（33条语录及注释）",
        editor_title="《马克思恩格斯列宁论无产阶级专政》校读编辑器",
        storage_key="marxist-proletarian-dictatorship-33-quotes-editor-v1",
        file_stem="proletarian_dictatorship_33_quotes",
        global_terms=global_terms,
        shared_library_href="",
        source_site_label="乌有之乡",
    )
    output_path = BASE_DIR / "editor.html"
    output_path.write_text(output, encoding="utf-8")
    print(f"Output: {output_path}")
    print(f"Characters: {len(text)}")
    print(f"Article terms: {len(terms)}")
    print(f"General dictionary hints: {len(global_terms)}")
