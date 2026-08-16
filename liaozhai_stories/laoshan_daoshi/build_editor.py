#!/usr/bin/env python3
"""Build the shared rich-text reading editor for 《聊斋志异·劳山道士》."""

from pathlib import Path
import base64
import json
import re
import sys


BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parents[1] / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))

from build_editor import build_html, load_global_terms, load_reading_notes, load_review_notes, load_terms  # noqa: E402


if __name__ == "__main__":
    text = (BASE_DIR / "laoshan_daoshi.txt").read_text(encoding="utf-8")
    seed_path = BASE_DIR / "laoshan_daoshi_editor_seed.json"
    seed = json.loads(seed_path.read_text(encoding="utf-8")) if seed_path.exists() else {}
    initial_media = []
    for item in seed.get("media", []):
        media_path = BASE_DIR / item["path"]
        encoded = base64.b64encode(media_path.read_bytes()).decode("ascii")
        initial_media.append({**item, "dataUrl": f"data:{item['type']};base64,{encoded}"})
    terms = load_terms(BASE_DIR / "laoshan_daoshi_rare_words.csv")
    for term in terms:
        term.setdefault("type", "rare_word")
    global_terms = load_global_terms(
        BASE_DIR.parents[2] / "project_dictionary" / "dictionary.csv", text, terms
    )
    output = build_html(
        text,
        terms,
        "https://liaozhai.5000yan.com/19951.html",
        chapter_title="《聊斋志异·劳山道士》",
        editor_title="《聊斋志异·劳山道士》校读编辑器",
        storage_key="liaozhai-laoshan-daoshi-editor-v1",
        file_stem="laoshan_daoshi",
        review_notes=load_review_notes(BASE_DIR / "review_notes.tsv"),
        reading_notes=seed.get("notes") or load_reading_notes(BASE_DIR / "laoshan_daoshi_reading_notes.txt"),
        initial_media=initial_media,
        global_terms=global_terms,
        shared_library_href="",
        source_site_label="五千言",
    )
    if seed.get("bodyHTML"):
        output = re.sub(
            r'(<section id="editor" class="editor"[^>]*>).*?(</section>)',
            lambda match: match.group(1) + seed["bodyHTML"] + match.group(2),
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
    output_path = BASE_DIR / "editor.html"
    output_path.write_text(output, encoding="utf-8")
    print(f"Output: {output_path}\nCharacters: {len(text)}\nTerms: {len(terms)}")
