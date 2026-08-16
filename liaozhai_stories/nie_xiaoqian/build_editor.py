#!/usr/bin/env python3
"""Build the shared editor for 《聊斋志异·聂小倩》."""

from pathlib import Path
import base64
import json
import re
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parents[1] / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))

from build_editor import build_html, load_global_terms, load_review_notes, load_terms  # noqa: E402


if __name__ == "__main__":
    text = (BASE_DIR / "nie_xiaoqian.txt").read_text(encoding="utf-8")
    seed = json.loads(
        (BASE_DIR / "nie_xiaoqian_editor_seed.json").read_text(encoding="utf-8")
    )
    seed_body_html = re.sub(
        r'\[(<span class="notation"[^>]*data-term="黑\+曷".*?</ruby></span></span>)\]',
        r"\1",
        seed["bodyHTML"],
        count=1,
    )
    seed_body_html = seed_body_html.replace("黑+曷", "𪑦").replace(
        "[单人旁+匡]㑌", "㑌"
    )
    initial_media = []
    for item in seed.get("media", []):
        media_path = BASE_DIR / item["path"]
        encoded = base64.b64encode(media_path.read_bytes()).decode("ascii")
        initial_media.append(
            {
                "id": item["id"],
                "name": item["name"],
                "type": item["type"],
                "size": media_path.stat().st_size,
                "dataUrl": f"data:{item['type']};base64,{encoded}",
            }
        )
    terms = load_terms(BASE_DIR / "nie_xiaoqian_rare_words.csv")
    for term in terms:
        term.setdefault("type", "rare_word")
    global_terms = load_global_terms(
        BASE_DIR.parents[2] / "project_dictionary" / "dictionary.csv", text, terms
    )
    output = build_html(
        text,
        terms,
        "https://liaozhai.5000yan.com/19985.html",
        chapter_title="《聊斋志异·聂小倩》",
        editor_title="《聊斋志异·聂小倩》校读编辑器",
        storage_key="liaozhai-nie-xiaoqian-editor-v1",
        file_stem="nie_xiaoqian",
        review_notes=load_review_notes(BASE_DIR / "review_notes.tsv"),
        reading_notes=seed.get("notes") or [],
        initial_media=initial_media,
        global_terms=global_terms,
        shared_library_href="",
        source_site_label="五千言",
    )
    output = re.sub(
        r'(<section id="editor" class="editor"[^>]*>).*?(</section>)',
        lambda match: (
            match.group(1)
            + seed_body_html
            + match.group(2)
        ),
        output,
        count=1,
        flags=re.DOTALL,
    )
    footnotes = json.dumps(seed.get("footnotes") or [], ensure_ascii=False).replace(
        "</", "<\\/"
    )
    output = re.sub(
        r"const INITIAL_FOOTNOTES=.*?; const INITIAL_READING_NOTES=",
        lambda _match: f"const INITIAL_FOOTNOTES={footnotes}; const INITIAL_READING_NOTES=",
        output,
        count=1,
    )
    output_path = BASE_DIR / "editor.html"
    output_path.write_text(output, encoding="utf-8")
    print(f"Output: {output_path}\nCharacters: {len(text)}\nTerms: {len(terms)}")
