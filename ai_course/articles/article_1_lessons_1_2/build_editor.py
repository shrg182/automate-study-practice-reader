#!/usr/bin/env python3
"""Build the independent editor for AI Course Article 1."""

from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parents[2] / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))

from build_editor import build_html, load_inline_notes, load_reading_notes, load_review_notes, load_terms  # noqa: E402

if __name__ == "__main__":
    text = (BASE_DIR / "article_1_clean.txt").read_text(encoding="utf-8")
    output = build_html(
        text,
        load_terms(BASE_DIR / "reading_terms.csv"),
        "source.txt",
        chapter_title="How AI Works · Lessons 1–2",
        editor_title="AI Course Article 1 · Reading Editor",
        storage_key="ai-course-article-1-editor-v1",
        file_stem="ai_course_article_1",
        inline_notes=load_inline_notes(BASE_DIR / "inline_notes.tsv"),
        review_notes=load_review_notes(BASE_DIR / "review_notes.tsv"),
        reading_notes=load_reading_notes(BASE_DIR / "article_1_reading_notes.txt"),
        global_terms=[],
        theme_href="../../../workspace_theme.css",
        home_href="../../../index.html",
    )
    rich = {
        "recognize patterns": '<span style="background-color:#fff1b8">recognize patterns</span>',
        "makes predictions, measures its mistakes, and gradually improves": '<span style="background-color:#e3f0dc">makes predictions, measures its mistakes, and gradually improves</span>',
        "next-token prediction": '<span style="background-color:#dcebf0">next-token prediction</span>',
        "human judgment": '<span style="background-color:#d9c2f0">human judgment</span>',
        "learns from examples rather than receiving every rule directly": '<span style="background-color:#fff1b8">learns from examples rather than receiving every rule directly</span>',
        "model studies the features and labels together": '<span style="background-color:#e3f0dc">model studies the features and labels together</span>',
        "separate examples that were not used to adjust the model": '<span style="background-color:#dcebf0">separate examples that were not used to adjust the model</span>',
        "represent the real situations in which the model will be used": '<span style="background-color:#d9c2f0">represent the real situations in which the model will be used</span>',
    }
    for plain, markup in rich.items():
        output = output.replace(plain, markup, 1)
    output = output.replace("../../../project_dictionary/", "../../../../project_dictionary/")
    (BASE_DIR / "editor.html").write_text(output, encoding="utf-8")
    print(f"Output: {BASE_DIR / 'editor.html'}\nCharacters: {len(text)}")
