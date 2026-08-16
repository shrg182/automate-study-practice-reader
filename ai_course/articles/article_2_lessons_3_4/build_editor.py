#!/usr/bin/env python3
"""Build the independent editor for AI Course Article 2."""

from pathlib import Path
import json
import re
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parents[2] / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))

from build_editor import build_html, load_inline_notes, load_reading_notes, load_review_notes, load_terms  # noqa: E402

if __name__ == "__main__":
    text = (BASE_DIR / "article_2_clean.txt").read_text(encoding="utf-8")
    output = build_html(
        text,
        load_terms(BASE_DIR / "reading_terms.csv"),
        "source.txt",
        chapter_title="How AI Learns · Lessons 3–4",
        editor_title="AI Course Article 2 · Reading Editor",
        storage_key="ai-course-article-2-editor-v1",
        file_stem="ai_course_article_2",
        inline_notes=load_inline_notes(BASE_DIR / "inline_notes.tsv"),
        review_notes=load_review_notes(BASE_DIR / "review_notes.tsv"),
        reading_notes=load_reading_notes(BASE_DIR / "article_2_reading_notes.txt"),
        global_terms=[],
        theme_href="../../../workspace_theme.css",
        home_href="../../../index.html",
    )
    rich = {
        "turns mistakes into directions for improvement": '<span style="background-color:#fff1b8">turns mistakes into directions for improvement</span>',
        "converts the difference between predictions and answers into a number": '<span style="background-color:#e3f0dc">converts the difference between predictions and answers into a number</span>',
        "calculates a small adjustment to many parameters": '<span style="background-color:#dcebf0">calculates a small adjustment to many parameters</span>',
        "balance between learning too slowly and overshooting": '<span style="background-color:#d9c2f0">balance between learning too slowly and overshooting</span>',
        "engineered system of calculations, not a miniature human brain": '<span style="background-color:#fff1b8">engineered system of calculations, not a miniature human brain</span>',
        "weights tell the network which inputs deserve more or less influence": '<span style="background-color:#e3f0dc">weights tell the network which inputs deserve more or less influence</span>',
        "transform it into increasingly useful internal patterns": '<span style="background-color:#dcebf0">transform it into increasingly useful internal patterns</span>',
        "useful behavior emerges from many trained operations working together": '<span style="background-color:#d9c2f0">useful behavior emerges from many trained operations working together</span>',
    }
    seed_path = BASE_DIR / "article_2_editor_seed.json"
    if seed_path.exists():
        seed = json.loads(seed_path.read_text(encoding="utf-8"))
        body_html = str(seed.get("bodyHTML", "")).strip()
        if not body_html:
            raise ValueError(f"Rich editor seed has no bodyHTML: {seed_path}")
        output = re.sub(
            r'(<section id="editor" class="editor"[^>]*>).*?(</section>)',
            lambda match: match.group(1) + body_html + match.group(2),
            output,
            count=1,
            flags=re.DOTALL,
        )
        footnotes = json.dumps(
            seed.get("footnotes") or [], ensure_ascii=False
        ).replace("</", "<\\/")
        output = re.sub(
            r"const INITIAL_FOOTNOTES=.*?; const INITIAL_READING_NOTES=",
            lambda _match: (
                f"const INITIAL_FOOTNOTES={footnotes}; "
                "const INITIAL_READING_NOTES="
            ),
            output,
            count=1,
        )
    else:
        for plain, markup in rich.items():
            output = output.replace(plain, markup, 1)
    output = output.replace("../../../project_dictionary/", "../../../../project_dictionary/")
    (BASE_DIR / "editor.html").write_text(output, encoding="utf-8")
    print(f"Output: {BASE_DIR / 'editor.html'}\nCharacters: {len(text)}")
