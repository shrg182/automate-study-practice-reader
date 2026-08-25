#!/usr/bin/env python3
"""Build an individual Marx–Engels U.S. Civil War Reader project."""
from __future__ import annotations
import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
ENGLISH_INDEX_URL = "https://www.marxists.org/archive/marx/works/1861/us-civil-war/index.htm"
ENGLISH_PDF_URL = "https://www.marxists.org/archive/marx/works/download/Marx_Engels_Writings_on_the_North_American_Civil_War.pdf"
SHARED_DIR = BASE_DIR.parents[1] / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))
from build_editor import build_html, load_global_terms, load_inline_notes, load_reading_notes, load_review_notes, load_terms  # noqa: E402

def build(project_dir: Path) -> Path:
    metadata = json.loads((project_dir / "metadata.json").read_text(encoding="utf-8"))
    text = (project_dir / "clean.txt").read_text(encoding="utf-8")
    terms = load_terms(project_dir / "reading_terms.csv")
    inline_notes = load_inline_notes(project_dir / "inline_notes.tsv")
    review_notes = load_review_notes(project_dir / "review_notes.tsv")
    reading_notes = load_reading_notes(project_dir / "reading_notes.txt")
    global_terms = load_global_terms(BASE_DIR.parents[2] / "project_dictionary" / "dictionary.csv", text, terms)
    title = metadata["title"]
    output = build_html(text, terms, metadata["source_url"], chapter_title=f'{metadata["author"]}·{title}', editor_title=f"《{title}》校读编辑器", storage_key=f'marx-engels-us-civil-war-{metadata["sequence"]}-v1', file_stem=f'marx_engels_{metadata["sequence"]}', inline_notes=inline_notes, review_notes=review_notes, reading_notes=reading_notes, global_terms=global_terms, home_href="../../../../index.html", theme_href="../../../../workspace_theme.css", shared_library_href="", shared_library_label="", source_site_label="中文马克思主义文库")
    resources = f'''<aside style="margin:12px auto;max-width:980px;padding:12px 16px;border:1px solid #d8d0bf;background:#fffdf7;font:14px/1.6 system-ui,sans-serif"><strong>English reading (preferred):</strong> <a href="{ENGLISH_INDEX_URL}" target="_blank" rel="noreferrer">article collection ↗</a> · <a href="{ENGLISH_PDF_URL}" target="_blank" rel="noreferrer">consolidated PDF ↗</a><br><small>This editor contains the Chinese reference text; use the English resources as the leading text.</small></aside>'''
    output = output.replace('<div class="app">', '<div class="app">' + resources, 1)
    output_path = project_dir / "editor.html"
    output_path.write_text(output, encoding="utf-8")
    return output_path
