#!/usr/bin/env python3
"""Build the independent editor for AI Course Article 4."""

from pathlib import Path
import json
import re
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parents[2] / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))

from build_editor import build_html, load_inline_notes, load_reading_notes, load_review_notes, load_terms  # noqa: E402


if __name__ == "__main__":
    text = (BASE_DIR / "article_4_clean.txt").read_text(encoding="utf-8")
    output = build_html(
        text,
        load_terms(BASE_DIR / "reading_terms.csv"),
        "source.txt",
        chapter_title="Using AI Responsibly · Lesson 7 and Summary",
        editor_title="AI Course Article 4 · Reading Editor",
        storage_key="ai-course-article-4-editor-v1",
        file_stem="ai_course_article_4",
        inline_notes=load_inline_notes(BASE_DIR / "inline_notes.tsv"),
        review_notes=load_review_notes(BASE_DIR / "review_notes.tsv"),
        reading_notes=load_reading_notes(BASE_DIR / "article_4_reading_notes.txt"),
        global_terms=[],
        theme_href="../../../workspace_theme.css",
        home_href="../../../index.html",
    )
    rich = {
        "model can learn an incomplete pattern": '<span style="background-color:#fff1a8">model can learn an incomplete pattern</span>',
        "Fairness therefore requires examining outcomes": '<span style="background-color:#b7e7a7">Fairness therefore requires examining outcomes</span>',
        "The higher the possible harm, the stronger the verification should be": '<span style="background-color:#b8ddf8">The higher the possible harm, the stronger the verification should be</span>',
        "Confidence in the wording is not evidence of correctness": '<span style="background-color:#ddb5eb">Confidence in the wording is not evidence of correctness</span>',
    }
    seed_path = BASE_DIR / "article_4_editor_seed.json"
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
        footnotes = json.dumps(seed.get("footnotes") or [], ensure_ascii=False).replace("</", "<\\/")
        output = re.sub(
            r"const INITIAL_FOOTNOTES=.*?; const INITIAL_READING_NOTES=",
            lambda _match: f"const INITIAL_FOOTNOTES={footnotes}; const INITIAL_READING_NOTES=",
            output,
            count=1,
        )
    else:
        for plain, markup in rich.items():
            output = output.replace(plain, markup, 1)
    output = output.replace("../../../project_dictionary/", "../../../../project_dictionary/")
    (BASE_DIR / "editor.html").write_text(output, encoding="utf-8")
    print(f"Output: {BASE_DIR / 'editor.html'}\nCharacters: {len(text)}")
