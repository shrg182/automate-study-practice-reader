#!/usr/bin/env python3
"""Refresh the complete source catalogs used by the Shiji and Liaozhai selectors."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import re
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent
SHIJI_URL = "https://www.guwendao.net/guwen/book_7723bfd24ca1.aspx"
LIAOZHAI_URL = "https://liaozhai.5000yan.com/"


def fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; ReadingRoomCatalog/1.0)"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_shiji(html: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    boundaries = [(12, "十二本纪"), (22, "十表"), (30, "八书"), (60, "三十世家"), (130, "七十列传")]
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for anchor in soup.find_all("a", href=True):
        match = re.search(r"/guwen/(bookv_([0-9a-f]+)\.aspx)", anchor["href"], re.I)
        if not match:
            continue
        source_url = urljoin(SHIJI_URL, anchor["href"])
        if source_url in seen:
            continue
        seen.add(source_url)
        position = len(rows) + 1
        section = next(label for end, label in boundaries if position <= end)
        chapter = anchor.get_text(" ", strip=True)
        rows.append({"id": f"shiji-{match.group(2)}", "title": f"{section}·{chapter}", "source_url": source_url, "section": section})
    if len(rows) != 130:
        raise ValueError(f"Expected 130 Shiji chapters, found {len(rows)}")
    return rows


def parse_liaozhai(html: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    section = ""
    for element in soup.find_all(["h3", "a"]):
        classes = element.get("class", [])
        if element.name == "h3" and "category-block-title" in classes:
            section = element.get_text(" ", strip=True)
            continue
        if element.name != "a" or "category-link" not in classes:
            continue
        source_url = element.get("href", "")
        match = re.fullmatch(r"https?://liaozhai\.5000yan\.com/(\d+)\.html", source_url)
        if not match or source_url in seen:
            continue
        seen.add(source_url)
        title = element.get_text(" ", strip=True)
        rows.append({"id": f"liaozhai-{match.group(1)}", "title": f"《聊斋志异·{title}》", "source_url": source_url, "section": section})
    sections = {row["section"] for row in rows}
    if len(rows) < 490 or len(sections) != 12:
        raise ValueError(f"Expected at least 490 Liaozhai stories in 12 volumes, found {len(rows)} in {len(sections)}")
    return rows


def write_catalog(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "title", "source_url", "section"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {path} with {len(rows)} entries")


def load(path: Path | None, url: str) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path else fetch(url)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shiji-html", type=Path, help="Parse a saved Shiji index instead of downloading it")
    parser.add_argument("--liaozhai-html", type=Path, help="Parse a saved Liaozhai index instead of downloading it")
    args = parser.parse_args()
    write_catalog(BASE_DIR / "shiji/source_catalog.csv", parse_shiji(load(args.shiji_html, SHIJI_URL)))
    write_catalog(BASE_DIR / "liaozhai_stories/source_catalog.csv", parse_liaozhai(load(args.liaozhai_html, LIAOZHAI_URL)))


if __name__ == "__main__":
    main()
