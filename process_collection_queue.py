#!/usr/bin/env python3
"""Process queues exported by the Shiji and Liaozhai full-catalog selectors."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent
CONFIG = {
    "shiji": {"directory": "shiji", "site": "古文岛"},
    "liaozhai_stories": {"directory": "liaozhai_stories", "site": "五千言"},
}


def read_catalog(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def canonical_entries(payload: dict, catalog: list[dict[str, str]]) -> list[dict[str, str]]:
    by_id = {row["id"]: row for row in catalog}
    by_url = {row["source_url"].rstrip("/"): row for row in catalog}
    entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for requested in payload.get("entries", []):
        source = by_id.get(str(requested.get("id", ""))) or by_url.get(str(requested.get("source_url", "")).rstrip("/"))
        if source is None:
            raise ValueError(f"Queue entry is not in the source catalog: {requested.get('source_url', '')}")
        if source["id"] not in seen:
            entries.append(source)
            seen.add(source["id"])
    if not entries:
        raise ValueError("Queue contains no valid entries")
    return entries


def extract_text(collection: str, page_html: str) -> str:
    if collection == "liaozhai_stories":
        sys.path.insert(0, str(BASE_DIR / "liaozhai_stories"))
        from liaozhai_tools import extract_section, html_section_to_text, html_to_text

        text = html_section_to_text(page_html, "original")
        if text is None:
            text = extract_section(html_to_text(page_html), "original")
        return text.strip()
    soup = BeautifulSoup(page_html, "html.parser")
    body = soup.select_one("div.contson[id^=contson]")
    if body is None:
        raise ValueError("Expected Shiji article container was not found")
    paragraphs = [re.sub(r"[ \t\u3000]+", "", p.get_text("", strip=True)) for p in body.find_all("p", recursive=False)]
    text = "\n\n".join(filter(None, paragraphs)) or body.get_text("", strip=True)
    return text.strip()


def target_for(root: Path, row: dict[str, str]) -> Path:
    if row["id"].startswith("shiji-"):
        return root / row["id"].replace("-", "_", 1)
    return root / f"story_{row['id'].removeprefix('liaozhai-')}"


def build_editor(collection: str, row: dict[str, str], target: Path, text: str) -> None:
    shared = BASE_DIR / "shiji" / "shiji_lisheng_lujia"
    sys.path.insert(0, str(shared))
    from build_editor import build_html, load_global_terms, load_review_notes, load_terms

    terms = load_terms(target / "reading_terms.csv")
    title = row["title"]
    if collection == "shiji":
        title = f"《史记·{title.split('·', 1)[-1]}》"
    output = build_html(
        text,
        terms,
        row["source_url"],
        chapter_title=title,
        editor_title=f"{title}校读编辑器",
        storage_key=f"{row['id']}-editor-v1",
        file_stem=row["id"].replace("-", "_"),
        review_notes=load_review_notes(target / "review_notes.tsv"),
        global_terms=load_global_terms(BASE_DIR.parent / "project_dictionary" / "dictionary.csv", text, terms),
        home_href="../../index.html",
        shared_library_href="",
        source_site_label=CONFIG[collection]["site"],
    )
    (target / "editor.html").write_text(output, encoding="utf-8")


def process(queue: Path) -> None:
    payload = json.loads(queue.read_text(encoding="utf-8"))
    collection = payload.get("collection")
    if collection not in CONFIG:
        raise ValueError(f"Unsupported collection: {collection}")
    root = BASE_DIR / CONFIG[collection]["directory"]
    entries = canonical_entries(payload, read_catalog(root / "source_catalog.csv"))
    import build_collection_selectors

    existing_by_url = {
        build_collection_selectors.editor_data(path, root)["source_url"].rstrip("/"): path
        for path in root.glob("*/editor.html")
    }
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (personal study-material downloader)", "Accept-Language": "zh-CN,zh;q=0.9"})
    for row in entries:
        target = target_for(root, row)
        existing = existing_by_url.get(row["source_url"].rstrip("/"))
        if existing is not None and existing.parent != target:
            print(f"Kept existing {existing}")
            continue
        if (target / "editor.html").exists():
            print(f"Kept existing {target / 'editor.html'}")
            continue
        response = session.get(row["source_url"], timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or "utf-8"
        text = extract_text(collection, response.text)
        target.mkdir(parents=True, exist_ok=True)
        (target / "source.txt").write_text(text + "\n", encoding="utf-8")
        (target / "reading_terms.csv").write_text("term,pinyin,annotation,type\n", encoding="utf-8")
        (target / "review_notes.tsv").write_text("text\tissue\tstatus\n", encoding="utf-8")
        (target / "source.json").write_text(json.dumps({**row, "retrieved_at": datetime.now(timezone.utc).isoformat(), "source_site": CONFIG[collection]["site"], "characters": len(text)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        build_editor(collection, row, target, text)
        print(f"Built {target / 'editor.html'}")
    import build_index

    for collection_key, values in build_collection_selectors.COLLECTIONS.items():
        build_collection_selectors.build(collection_key, *values)
    build_index.main()
    print(f"Processed {len(entries)} {collection} queue entries")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queue", type=Path)
    args = parser.parse_args()
    process(args.queue)


if __name__ == "__main__":
    main()
