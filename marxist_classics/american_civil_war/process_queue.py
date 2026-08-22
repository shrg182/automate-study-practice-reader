#!/usr/bin/env python3
"""Process an exported Marx–Engels U.S. Civil War selection queue."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import ssl
from urllib.request import Request, urlopen
import certifi
from bs4 import BeautifulSoup, NavigableString, Tag
from build_reading import build

BASE_DIR = Path(__file__).resolve().parent
READINGS_DIR = BASE_DIR / "readings"
SLUGS = {"16": "lessons_of_the_american_war", "18": "trent_affair_controversy", "19": "crisis_of_slavery", "20": "recent_events_in_america", "39": "ironclads_rams_and_civil_war", "42": "russell_protest_grain_prices_italy"}

def download(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 ReaderProject/1.0"})
    context = ssl.create_default_context(cafile=certifi.where())
    with urlopen(request, timeout=30, context=context) as response:
        return response.read().decode("gb18030")

def extract(page_html: str) -> str:
    soup = BeautifulSoup(page_html, "html.parser")
    title = soup.select_one(".title1")
    if title is None:
        raise ValueError("Could not find the article title")
    pieces: list[str] = []
    for node in title.next_siblings:
        if isinstance(node, Tag) and node.name == "div" and node.get("align", "").lower() == "right":
            break
        if isinstance(node, NavigableString):
            pieces.append(str(node))
        elif isinstance(node, Tag) and node.name == "br":
            pieces.append("\n")
        elif isinstance(node, Tag):
            pieces.append(node.get_text(" ", strip=False))
    lines = [re.sub(r"[ \t\xa0]+", " ", line).strip() for line in "".join(pieces).splitlines()]
    paragraphs = [line for line in lines if line]
    if not paragraphs:
        raise ValueError("Could not extract article text")
    return "\n\n".join(paragraphs)

def ensure_project(item: dict[str, str]) -> Path:
    sequence = str(item["sequence"])
    project = READINGS_DIR / f"{int(sequence):03d}_{SLUGS.get(sequence, f'reading_{sequence}')}"
    (project / "sources").mkdir(parents=True, exist_ok=True)
    page_html = download(item["source_url"])
    text = extract(page_html)
    metadata = {key: item.get(key, "") for key in ("sequence", "section", "year", "author", "title", "source_url")}
    (project / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (project / "sources" / "page.html").write_text(page_html, encoding="utf-8")
    (project / "source.txt").write_text(text + "\n", encoding="utf-8")
    clean = project / "clean.txt"
    if not clean.exists(): clean.write_text(text + "\n", encoding="utf-8")
    for name, content in {"reading_terms.csv": "term,pinyin,meaning,level,category,notes\n", "inline_notes.tsv": "phrase\tnote\n", "review_notes.tsv": "phrase\tnote\n", "reading_notes.txt": ""}.items():
        path = project / name
        if not path.exists(): path.write_text(content, encoding="utf-8")
    wrapper = '#!/usr/bin/env python3\nfrom pathlib import Path\nimport sys\nPROJECT = Path(__file__).resolve().parent\nsys.path.insert(0, str(PROJECT.parents[1]))\nfrom build_reading import build  # noqa: E402\nif __name__ == "__main__": print(f"Output: {build(PROJECT)}")\n'
    (project / "build_editor.py").write_text(wrapper, encoding="utf-8")
    (project / "README.md").write_text(f'# {item["title"]}\n\n作者：{item["author"]}\n\n原文：{item["source_url"]}\n', encoding="utf-8")
    build(project)
    print(f'Processed {sequence}: {item["title"]} ({len(text)} characters)')
    return project

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queue", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.queue.read_text(encoding="utf-8"))
    for item in payload.get("readings", []): ensure_project(item)

if __name__ == "__main__": main()
