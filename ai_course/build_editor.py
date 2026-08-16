#!/usr/bin/env python3
"""Build the shared Shiji editor for the introductory AI course."""

from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parent / "shiji" / "shiji_lisheng_lujia"
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
    text = (BASE_DIR / "ai_course_clean.txt").read_text(encoding="utf-8")
    terms = load_terms(BASE_DIR / "reading_terms.csv")
    global_terms = load_global_terms(
        BASE_DIR.parents[1] / "project_dictionary" / "dictionary.csv", text, terms
    )
    inline_notes = load_inline_notes(BASE_DIR / "inline_notes.tsv")
    review_notes = load_review_notes(BASE_DIR / "review_notes.tsv")
    reading_notes = load_reading_notes(BASE_DIR / "ai_course_reading_notes.txt")
    output = build_html(
        text,
        terms,
        "../../AI_COURSE.md",
        chapter_title="AI Course · How AI Works",
        editor_title="How AI Works · Shiji Reading Editor",
        storage_key="shiji-ai-course-editor-v1",
        file_stem="ai_course",
        inline_notes=inline_notes,
        review_notes=review_notes,
        reading_notes=reading_notes,
        global_terms=global_terms,
        home_href="../index.html",
        theme_href="../workspace_theme.css",
    )
    rich_text_examples = {
        "artificial intelligence quietly helps people": (
            '<strong style="background-color:#fff1b8">'
            "artificial intelligence quietly helps people</strong>"
        ),
        "recognize patterns": "<u>recognize patterns</u>",
        "makes predictions, measures its mistakes, and gradually improves": (
            '<strong><span style="background-color:#dcebf0">'
            "makes predictions, measures its mistakes, and gradually improves"
            "</span></strong>"
        ),
        "human judgment": (
            '<span style="background-color:#d9c2f0">human judgment</span>'
        ),
        "Искусственный интеллект учится на примерах": (
            '<strong style="background-color:#e3f0dc">'
            "Искусственный интеллект учится на примерах</strong>"
        ),
        "learns from examples rather than receiving every rule directly": (
            '<span style="background-color:#fff1b8">'
            "learns from examples rather than receiving every rule directly</span>"
        ),
        "model studies the features and labels together": (
            '<span style="background-color:#e3f0dc">'
            "model studies the features and labels together</span>"
        ),
        "separate examples that were not used to adjust the model": (
            '<span style="background-color:#dcebf0">'
            "separate examples that were not used to adjust the model</span>"
        ),
        "represent the real situations in which the model will be used": (
            '<span style="background-color:#d9c2f0">'
            "represent the real situations in which the model will be used</span>"
        ),
        "turns mistakes into directions for improvement": (
            '<span style="background-color:#fff1b8">'
            "turns mistakes into directions for improvement</span>"
        ),
        "converts the difference between predictions and answers into a number": (
            '<span style="background-color:#e3f0dc">'
            "converts the difference between predictions and answers into a number</span>"
        ),
        "calculates a small adjustment to many parameters": (
            '<span style="background-color:#dcebf0">'
            "calculates a small adjustment to many parameters</span>"
        ),
        "balance between learning too slowly and overshooting": (
            '<span style="background-color:#d9c2f0">'
            "balance between learning too slowly and overshooting</span>"
        ),
        "engineered system of calculations, not a miniature human brain": (
            '<span style="background-color:#fff1b8">'
            "engineered system of calculations, not a miniature human brain</span>"
        ),
        "weights tell the network which inputs deserve more or less influence": (
            '<span style="background-color:#e3f0dc">'
            "weights tell the network which inputs deserve more or less influence</span>"
        ),
        "transform it into increasingly useful internal patterns": (
            '<span style="background-color:#dcebf0">'
            "transform it into increasingly useful internal patterns</span>"
        ),
        "useful behavior emerges from many trained operations working together": (
            '<span style="background-color:#d9c2f0">'
            "useful behavior emerges from many trained operations working together</span>"
        ),
    }
    for plain_text, rich_text in rich_text_examples.items():
        output = output.replace(plain_text, rich_text, 1)
    output = output.replace("../../../project_dictionary/", "../../project_dictionary/")
    output_path = BASE_DIR / "editor.html"
    output_path.write_text(output, encoding="utf-8")
    print(
        f"Output: {output_path}\nCharacters: {len(text)}"
        f"\nArticle terms: {len(terms)}\nGeneral dictionary hints: {len(global_terms)}"
    )
