#!/usr/bin/env python3
"""Extract the reading text from a saved source-page snapshot."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent
SOURCE_URL = "https://m.wyzxwk.com/Article/shushe/2011/08/250089.html"


def normalize(text: str) -> str:
    text = text.replace("\xa0", " ").replace("\u3000", " ")
    return re.sub(r"[ \t]+", " ", text).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="saved HTML page")
    args = parser.parse_args()

    html = args.html.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    article = soup.select_one("section#article")
    if article is None:
        raise SystemExit("Could not find section#article in the source page")

    paragraphs = [normalize(p.get_text(" ", strip=True)) for p in article.find_all("p", recursive=False)]
    paragraphs = [p for p in paragraphs if p]
    text = "\n\n".join(paragraphs) + "\n"
    title_node = soup.select_one(".article-body h1")
    info_node = soup.select_one(".article-info")
    title = normalize(title_node.get_text(" ", strip=True)) if title_node else ""
    info = normalize(info_node.get_text(" ", strip=True)) if info_node else ""
    compact_characters = len(re.sub(r"\s+", "", text))

    sources = BASE_DIR / "sources"
    sources.mkdir(exist_ok=True)
    (sources / "page.html").write_text(html, encoding="utf-8")
    (BASE_DIR / "source.txt").write_text(text, encoding="utf-8")
    clean_path = BASE_DIR / "proletarian_dictatorship_33_quotes_clean.txt"
    if not clean_path.exists():
        clean_path.write_text(text, encoding="utf-8")

    metadata = {
        "title": title,
        "page_information": info,
        "source_url": SOURCE_URL,
        "paragraphs": len(paragraphs),
        "non_whitespace_characters": compact_characters,
        "recommended_review_batches": 8,
    }
    (BASE_DIR / "source_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
