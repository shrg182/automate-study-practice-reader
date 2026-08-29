#!/usr/bin/env python3
"""Build the independent editor for the ChatGPT and Codex follow-up course."""

from pathlib import Path
import json
import re
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parents[2] / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))

from build_editor import build_html, load_inline_notes, load_reading_notes, load_review_notes, load_terms  # noqa: E402


if __name__ == "__main__":
    text = (BASE_DIR / "article_6_clean.txt").read_text(encoding="utf-8")
    output = build_html(
        text,
        load_terms(BASE_DIR / "reading_terms.csv"),
        "source.txt",
        chapter_title="From Conversation to Completed Work: Using ChatGPT and Codex",
        editor_title="AI Course Article 6 · Follow-up Reading Editor",
        storage_key="ai-course-article-6-editor-v2",
        file_stem="ai_course_article_6_chatgpt_codex",
        inline_notes=load_inline_notes(BASE_DIR / "inline_notes.tsv"),
        review_notes=load_review_notes(BASE_DIR / "review_notes.tsv"),
        reading_notes=load_reading_notes(BASE_DIR / "article_6_reading_notes.txt"),
        global_terms=[],
        theme_href="../../../workspace_theme.css",
        home_href="../../../index.html",
    )
    initial_highlights = {
        "choose the environment whose working surface matches that outcome": "#fff1a8",
        "A productive prompt is a compact work brief": "#b7e7a7",
        "The first answer is a starting point, not a verdict": "#b8ddf8",
        "“The command completed” is not the same as “the requested behavior works.”": "#ddb5eb",
        "Verification should increase with consequence, uncertainty, and irreversibility": "#fff1a8",
    }
    seed_path = BASE_DIR / "article_6_editor_seed.json"
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
        for phrase, color in initial_highlights.items():
            output = output.replace(phrase, f'<span style="background-color:{color}">{phrase}</span>', 1)
    output = output.replace("../../../project_dictionary/", "../../../../project_dictionary/")
    (BASE_DIR / "editor.html").write_text(output, encoding="utf-8")
    print(f"Output: {BASE_DIR / 'editor.html'}\nCharacters: {len(text)}")
