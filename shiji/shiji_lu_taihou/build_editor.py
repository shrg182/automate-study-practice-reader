#!/usr/bin/env python3
"""Build the editor for 《史记·吕太后本纪》."""
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parent / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))
from build_editor import build_html, load_global_terms, load_inline_notes, load_reading_notes, load_review_notes, load_terms  # noqa: E402

if __name__ == "__main__":
    text = (BASE_DIR / "lu_taihou_clean.txt").read_text(encoding="utf-8")
    terms = load_terms(BASE_DIR / "reading_terms.csv")
    inline_notes = load_inline_notes(BASE_DIR / "inline_notes.tsv")
    review_notes = load_review_notes(BASE_DIR / "review_notes.tsv")
    reading_notes = load_reading_notes(BASE_DIR / "lu_taihou_reading_notes.txt")
    global_terms = load_global_terms(BASE_DIR.parents[2] / "project_dictionary" / "dictionary.csv", text, terms)
    output = build_html(text, terms, "https://www.guwendao.net/guwen/bookv_18c59fc3f555.aspx", chapter_title="十二本纪·吕太后本纪第九", editor_title="《史记·吕太后本纪》校读编辑器", storage_key="shiji-lu-taihou-editor-v1", file_stem="lu_taihou", inline_notes=inline_notes, review_notes=review_notes, reading_notes=reading_notes, global_terms=global_terms)
    output_path = BASE_DIR / "editor.html"
    output_path.write_text(output, encoding="utf-8")
    print(f"Output: {output_path}\nCharacters: {len(text)}\nTerms: {len(terms)}")
