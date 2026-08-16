#!/usr/bin/env python3
"""Download and split catalogued 《容斋随笔》 entries from 5000言."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import time

import requests
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent
CATALOG = BASE_DIR / "catalog.csv"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; RongzhaiStudyBuilder/1.0)"}


def response_text(response: requests.Response) -> str:
    """Decode source pages using their declared UTF-8 charset.

    The server currently omits a charset from its HTTP Content-Type header, so
    Requests otherwise falls back to ISO-8859-1 despite the UTF-8 meta tag.
    """
    return response.content.decode("utf-8-sig")


def normalize(text: str) -> str:
    text = text.replace("\u3000", " ").replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r" {2,}", " ", text)
    text = text.replace("一一卷", "一卷")
    return text.strip()


def entry_dir(row: dict[str, str]) -> Path:
    return BASE_DIR / f"volume_{int(row['volume']):02d}" / f"{int(row['sequence']):03d}_{row['slug']}"


def add_source_markers(original: str, notes: list[dict[str, str]]) -> tuple[str, list[dict[str, str]]]:
    occurrences: list[tuple[int, int, dict[str, str]]] = []
    for note in notes:
        term = note["term"]
        start = original.find(term) if term else -1
        if start >= 0:
            occurrences.append((start, start + len(term), note))
    occurrences.sort(key=lambda item: (item[0], -item[1], item[2]["order"]))
    active = [item[2] for item in occurrences]
    insertions = [(end, number) for number, (_, end, _) in enumerate(occurrences, 1)]
    marked = original
    for end, number in sorted(insertions, reverse=True):
        marked = marked[:end] + f"〔{number}〕" + marked[end:]
    footnotes = "\n\n脚注\n\n" + "\n\n".join(
        f"〔{index}〕【来源注释】{item['term']}：{item['annotation']}"
        for index, item in enumerate(active, 1)
    )
    return marked + footnotes, active


def parse_page(html_text: str, row: dict[str, str]) -> dict[str, object]:
    soup = BeautifulSoup(html_text, "html.parser")
    article = soup.select_one("article.reading-content")
    if article is None:
        raise ValueError("No article.reading-content element found")
    title_tag = soup.find("h1")
    title = normalize(title_tag.get_text(" ", strip=True)) if title_tag else row["title"]
    if title.startswith("《") and title.endswith("》"):
        title = title[1:-1].strip()
    originals = [normalize(tag.get_text("", strip=True)) for tag in article.select('[data-section="原文"]')]
    translations = [normalize(tag.get_text("", strip=True)) for tag in article.select('[data-section="翻译"]')]
    if not originals:
        raise ValueError("No data-section=原文 content found")
    note_script = article.select_one("#article-notes")
    raw_notes = json.loads(note_script.string or "{}") if note_script else {}
    notes = [
        {
            "order": index,
            "source_key": key,
            "term": normalize(str(value.get("w", ""))),
            "annotation": normalize(str(value.get("e", ""))),
        }
        for index, (key, value) in enumerate(raw_notes.items(), 1)
        if isinstance(value, dict) and value.get("w") and value.get("e")
    ]
    original = "\n\n".join(originals)
    reading, active_notes = add_source_markers(original, notes)
    return {
        "title": title,
        "original": original,
        "translation": "\n\n".join(translations),
        "notes": notes,
        "reading": reading,
        "active_note_count": len(active_notes),
    }


def write_entry(row: dict[str, str], html_text: str) -> None:
    parsed = parse_page(html_text, row)
    target = entry_dir(row)
    target.mkdir(parents=True, exist_ok=True)
    (target / "original.txt").write_text(str(parsed["original"]) + "\n", encoding="utf-8")
    (target / "reading.txt").write_text(str(parsed["reading"]) + "\n", encoding="utf-8")
    (target / "translation.txt").write_text(str(parsed["translation"]) + "\n", encoding="utf-8")
    with (target / "source_notes.tsv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["order", "source_key", "term", "annotation"], delimiter="\t")
        writer.writeheader()
        writer.writerows(parsed["notes"])
    with (target / "reading_terms.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["term", "pinyin", "annotation", "type"])
        writer.writeheader()
        for note in parsed["notes"]:
            writer.writerow({"term": note["term"], "pinyin": "", "annotation": note["annotation"], "type": "source_note"})
    (target / "review_notes.tsv").write_text("text\tissue\tstatus\n", encoding="utf-8")
    metadata = {
        "sequence": int(row["sequence"]),
        "volume": int(row["volume"]),
        "title": parsed["title"],
        "slug": row["slug"],
        "source_id": int(row["source_id"]),
        "source_url": row["source_url"],
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "source_site": "5000言",
        "original_characters": len(str(parsed["original"])),
        "source_note_count": len(parsed["notes"]),
        "active_source_note_count": parsed["active_note_count"],
    }
    (target / "source.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {target}: {metadata['original_characters']} chars, {metadata['source_note_count']} notes")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, help="Read cached files named rongzhai_<source_id>.html")
    parser.add_argument("--sequence", type=int, action="append", help="Only process selected sequence numbers")
    parser.add_argument("--delay", type=float, default=1.0)
    args = parser.parse_args()
    with CATALOG.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    if args.sequence:
        wanted = set(args.sequence)
        rows = [row for row in rows if int(row["sequence"]) in wanted]
    session = requests.Session()
    session.headers.update(HEADERS)
    for index, row in enumerate(rows):
        if args.source_dir:
            html_text = (args.source_dir / f"rongzhai_{row['source_id']}.html").read_text(encoding="utf-8")
        else:
            response = session.get(row["source_url"], timeout=30)
            response.raise_for_status()
            html_text = response_text(response)
        write_entry(row, html_text)
        if not args.source_dir and index + 1 < len(rows):
            time.sleep(args.delay)


if __name__ == "__main__":
    main()
