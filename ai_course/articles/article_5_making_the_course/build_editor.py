#!/usr/bin/env python3
"""Build the independent editor for the AI-course making story."""

from pathlib import Path
import json
import re
import sys

from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parents[2] / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))

from build_editor import build_html, load_inline_notes, load_reading_notes, load_review_notes, load_terms  # noqa: E402


if __name__ == "__main__":
    text = (BASE_DIR / "article_5_clean.txt").read_text(encoding="utf-8")
    output = build_html(
        text,
        load_terms(BASE_DIR / "reading_terms.csv"),
        "source.txt",
        chapter_title="How a Question Became an AI Course",
        editor_title="AI Course Article 5 · Reading Editor",
        storage_key="ai-course-article-5-editor-v1",
        file_stem="ai_course_article_5",
        inline_notes=load_inline_notes(BASE_DIR / "inline_notes.tsv"),
        review_notes=load_review_notes(BASE_DIR / "review_notes.tsv"),
        reading_notes=load_reading_notes(BASE_DIR / "article_5_reading_notes.txt"),
        global_terms=[],
        theme_href="../../../workspace_theme.css",
        home_href="../../../index.html",
    )
    # The legacy seed contains project-specific dialogue and is intentionally not
    # used by this general-audience edition.
    seed_path = BASE_DIR / "article_5_general_editor_seed.json"
    if seed_path.exists():
        seed = json.loads(seed_path.read_text(encoding="utf-8"))
        body_html = str(seed.get("bodyHTML", "")).strip()
        soup = BeautifulSoup(body_html, "html.parser")
        removing = False
        for paragraph in list(soup.find_all("p", recursive=False)):
            plain = paragraph.get_text("", strip=True)
            if plain == "From a Private Lesson to Shared Reading":
                removing = True
            if removing and plain == "Editing Became Part of the Lesson":
                removing = False
                replacement = soup.new_tag("p")
                replacement.string = (
                    "The request for seven lessons was not simply a request for more pages. "
                    "It created a gradual personal learning path. Each article could be studied "
                    "on its own while still belonging to a larger sequence. Headings offered a "
                    "route through the ideas, short checks encouraged reflection, and “Your turn” "
                    "prompts changed passive reading into practice. The structure itself became "
                    "part of the learning."
                )
                paragraph.insert_before(replacement)
            elif removing:
                paragraph.decompose()
        body_html = "\n".join(str(paragraph) for paragraph in soup.find_all("p", recursive=False))
        output = re.sub(
            r'(<section id="editor" class="editor"[^>]*>).*?(</section>)',
            lambda match: match.group(1) + body_html + match.group(2),
            output,
            count=1,
            flags=re.DOTALL,
        )
    output = output.replace("../../../project_dictionary/", "../../../../project_dictionary/")
    (BASE_DIR / "editor.html").write_text(output, encoding="utf-8")
    print(f"Output: {BASE_DIR / 'editor.html'}\nCharacters: {len(text)}")
