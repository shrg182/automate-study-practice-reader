#!/usr/bin/env python3
"""Build the independent editor for AI Course Article 3."""

from pathlib import Path
import json
import re
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parents[2] / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))

from build_editor import build_html, load_inline_notes, load_reading_notes, load_review_notes, load_terms  # noqa: E402


if __name__ == "__main__":
    text = (BASE_DIR / "article_3_clean.txt").read_text(encoding="utf-8")
    output = build_html(
        text,
        load_terms(BASE_DIR / "reading_terms.csv"),
        "source.txt",
        chapter_title="How AI Uses Language · Lessons 5–6",
        editor_title="AI Course Article 3 · Reading Editor",
        storage_key="ai-course-article-3-editor-v1",
        file_stem="ai_course_article_3",
        inline_notes=load_inline_notes(BASE_DIR / "inline_notes.tsv"),
        review_notes=load_review_notes(BASE_DIR / "review_notes.tsv"),
        reading_notes=load_reading_notes(BASE_DIR / "article_3_reading_notes.txt"),
        global_terms=[],
        theme_href="../../../workspace_theme.css",
        home_href="../../../index.html",
    )
    rich = {
        "predicts one token at a time": '<span style="background-color:#fff1a8">predicts one token at a time</span>',
        "Context changes which continuation is likely": '<span style="background-color:#b7e7a7">Context changes which continuation is likely</span>',
        "attention mechanism helps the model compare relevant parts of the context": '<span style="background-color:#b8ddf8">attention mechanism helps the model compare relevant parts of the context</span>',
        "plausible language is not the same as verified truth": '<span style="background-color:#ddb5eb">plausible language is not the same as verified truth</span>',
        "small labeled collection of example messages": '<span style="background-color:#fff1a8">small labeled collection of example messages</span>',
        "counts how often each word appears in each category": '<span style="background-color:#b7e7a7">counts how often each word appears in each category</span>',
        "combines many small pieces of evidence": '<span style="background-color:#b8ddf8">combines many small pieces of evidence</span>',
        "evaluation on new messages is essential": '<span style="background-color:#ddb5eb">evaluation on new messages is essential</span>',
    }
    seed_path = BASE_DIR / "article_3_editor_seed.json"
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
