#!/usr/bin/env python3
"""Import exported Marxist source-index selections as local reading editors."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys

import requests
from bs4 import BeautifulSoup

PRACTICE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PRACTICE_DIR / "shiji" / "shiji_lisheng_lujia"))
from build_editor import build_html, load_global_terms  # noqa: E402

CONFIG = {
    "marx_engels_us_civil_war": {
        "base": PRACTICE_DIR / "marxist_classics" / "american_civil_war",
        "label": "马克思、恩格斯论美国内战",
    },
    "sino_soviet_debate": {
        "base": PRACTICE_DIR / "nine_commentaries" / "source_index",
        "label": "中苏论战资料",
    },
}


def page_text(raw: bytes, expected_title: str) -> str:
    text = raw.decode("gb18030", errors="replace")
    soup = BeautifulSoup(text, "html.parser")
    for node in soup.select("script,style,noscript"):
        node.decompose()
    body = soup.body or soup
    lines = [re.sub(r"\s+", " ", line).strip() for line in body.get_text("\n").splitlines()]
    lines = [line for line in lines if line]
    title_at = next((i for i, line in enumerate(lines) if expected_title[:12] in line), 0)
    lines = lines[title_at:]
    return "\n\n".join(lines).strip() + "\n"


def process(queue: Path) -> list[Path]:
    payload = json.loads(queue.read_text(encoding="utf-8"))
    collection = payload.get("collection")
    if collection not in CONFIG:
        raise ValueError(f"Unsupported collection: {collection}")
    readings = payload.get("readings", [])
    if not readings:
        raise ValueError("The queue contains no selected readings")
    config = CONFIG[collection]
    base: Path = config["base"]
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (compatible; MobileReaderBuilder/1.0)"
    outputs: list[Path] = []
    for item in readings:
        sequence = int(item["sequence"])
        target = base / "readings" / f"{sequence:03d}"
        target.mkdir(parents=True, exist_ok=True)
        response = session.get(item["source_url"], timeout=30)
        response.raise_for_status()
        reading = page_text(response.content, item["title"])
        (target / "reading.txt").write_text(reading, encoding="utf-8")
        (target / "original.txt").write_text(reading, encoding="utf-8")
        (target / "reading_terms.csv").write_text("term,pinyin,annotation,type\n", encoding="utf-8")
        (target / "review_notes.tsv").write_text("text\tissue\tstatus\n", encoding="utf-8")
        metadata = {**item, "collection": collection, "retrieved_at": datetime.now(timezone.utc).isoformat(), "source_site": "中文马克思主义文库", "characters": len(reading)}
        (target / "source.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        html = build_html(
            reading,
            [],
            item["source_url"],
            chapter_title=item["title"],
            editor_title=f"{item['title']} · 校读编辑器",
            storage_key=f"{collection}-{sequence}-editor-v1",
            file_stem=f"{collection}_{sequence}",
            review_notes=[],
            global_terms=load_global_terms(PRACTICE_DIR / "project_dictionary" / "dictionary.csv", reading, []),
            home_href="../../../../index.html",
            theme_href="../../../../workspace_theme.css",
            shared_library_href="",
            source_site_label="中文马克思主义文库",
        )
        output = target / "editor.html"
        output.write_text(html, encoding="utf-8")
        outputs.append(output)
        print(f"Built {output}: {len(reading)} characters")
    subprocess.run([sys.executable, str(PRACTICE_DIR / "build_index.py")], check=True)
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queue", type=Path)
    args = parser.parse_args()
    process(args.queue)


if __name__ == "__main__":
    main()
