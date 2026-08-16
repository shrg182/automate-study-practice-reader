#!/usr/bin/env python3
"""Process selected Rongzhai articles exported by select_articles.html."""

import argparse
import csv
import json
from pathlib import Path
import subprocess
import sys

import requests
import download_rongzhai

BASE_DIR = Path(__file__).resolve().parent
CATALOG = BASE_DIR / "catalog.csv"
SOURCE_CATALOG = BASE_DIR / "source_catalog.csv"

def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))

def newest_queue():
    choices = list((Path.home() / "Downloads").glob("rongzhai_processing_queue*.json"))
    if not choices:
        raise FileNotFoundError("No rongzhai_processing_queue*.json found in Downloads")
    return max(choices, key=lambda path: path.stat().st_mtime)

def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("queue", nargs="?", type=Path); parser.add_argument("--pdf", action="store_true"); parser.add_argument("--refresh", action="store_true", help="Redownload entries that already have source files"); parser.add_argument("--validate-only", action="store_true"); args = parser.parse_args()
    queue = args.queue or newest_queue(); payload = json.loads(queue.read_text(encoding="utf-8"))
    requested = {str(item.get("source_id", "")) for item in payload.get("articles", [])}
    sources = {row["source_id"]: row for row in read_csv(SOURCE_CATALOG)}
    if requested - sources.keys():
        raise ValueError("Queue contains URLs outside the saved Rongzhai contents catalog")
    if not requested:
        raise ValueError("Queue contains no selected articles")
    if args.validate_only:
        print(f"Valid queue: {len(requested)} selected article(s) in {queue}"); return
    project = read_csv(CATALOG); by_id = {row["source_id"]: row for row in project}; selected = []
    for source_id in sorted(requested, key=lambda value: int(sources[value]["sequence"])):
        source = sources[source_id]; row = by_id.get(source_id)
        if row is None:
            row = {"sequence": source["sequence"], "volume": source["volume"], "title": source["title"], "slug": f"article_{source_id}", "source_id": source_id, "source_url": source["source_url"], "status": "downloaded"}; project.append(row); by_id[source_id] = row
        selected.append(row)
    with CATALOG.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["sequence", "volume", "title", "slug", "source_id", "source_url", "status"]); writer.writeheader(); writer.writerows(sorted(project, key=lambda row: int(row["sequence"])))
    session = requests.Session(); session.headers.update(download_rongzhai.HEADERS)
    for row in selected:
        target = download_rongzhai.entry_dir(row)
        if (target / "source.json").exists() and not args.refresh:
            print(f"Keeping existing source files: {target}")
            continue
        last_error = None
        for _attempt in range(3):
            try:
                response = session.get(row["source_url"], timeout=30); response.raise_for_status()
                html_text = download_rongzhai.response_text(response)
                download_rongzhai.parse_page(html_text, row)
                download_rongzhai.write_entry(row, html_text); last_error = None; break
            except (requests.RequestException, ValueError) as error:
                last_error = error
        if last_error:
            raise last_error
    subprocess.run([sys.executable, str(BASE_DIR / "build_editors.py")], check=True)
    subprocess.run([sys.executable, str(BASE_DIR.parent / "build_index.py")], check=True)
    subprocess.run([sys.executable, str(BASE_DIR / "build_article_selector.py")], check=True)
    if args.pdf or payload.get("generatePdfs"):
        command = [sys.executable, str(BASE_DIR / "make_pdfs.py")]
        for row in selected: command.extend(["--sequence", row["sequence"]])
        subprocess.run(command, check=True)
    print(f"Processed {len(selected)} selected article(s) from {queue}")

if __name__ == "__main__":
    main()
