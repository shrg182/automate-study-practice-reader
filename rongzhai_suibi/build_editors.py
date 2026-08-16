#!/usr/bin/env python3
"""Build Liaozhai-style editors for catalogued Rongzhai entries."""

from __future__ import annotations

import csv
import base64
import json
from pathlib import Path
import re
import sys


BASE_DIR = Path(__file__).resolve().parent
SHARED_EDITOR_DIR = BASE_DIR.parent / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_EDITOR_DIR))

from build_editor import build_html, load_global_terms, load_review_notes, load_terms  # noqa: E402


def main() -> None:
    with (BASE_DIR / "catalog.csv").open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    for row in rows:
        target = BASE_DIR / f"volume_{int(row['volume']):02d}" / f"{int(row['sequence']):03d}_{row['slug']}"
        metadata = json.loads((target / "source.json").read_text(encoding="utf-8"))
        seed_path = target / f"{row['slug']}_editor_seed.json"
        seed = json.loads(seed_path.read_text(encoding="utf-8")) if seed_path.exists() else {}
        initial_media = []
        for item in seed.get("media", []):
            media_path = target / item["path"]
            encoded = base64.b64encode(media_path.read_bytes()).decode("ascii")
            initial_media.append({**item, "dataUrl": f"data:{item['type']};base64,{encoded}"})
        text = (target / "reading.txt").read_text(encoding="utf-8")
        clean_text = (target / "original.txt").read_text(encoding="utf-8")
        terms = load_terms(target / "reading_terms.csv")
        global_terms = load_global_terms(
            BASE_DIR.parent / "project_dictionary" / "dictionary.csv", clean_text, terms
        )
        title = f"《容斋随笔·{metadata['title']}》"
        output = build_html(
            text,
            terms,
            row["source_url"],
            chapter_title=title,
            editor_title=f"{title}校读编辑器",
            storage_key=f"rongzhai-{row['source_id']}-editor-v1",
            file_stem=row["slug"],
            review_notes=load_review_notes(target / "review_notes.tsv"),
            reading_notes=seed.get("notes") or [],
            initial_media=initial_media,
            global_terms=global_terms,
            home_href="../../../index.html",
            theme_href="../../../workspace_theme.css",
            shared_library_href="",
            source_site_label="5000言",
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
        (target / "editor.html").write_text(output, encoding="utf-8")
        print(f"Built {target / 'editor.html'}")


if __name__ == "__main__":
    main()
