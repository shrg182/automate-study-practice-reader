#!/usr/bin/env python3
"""Import the newest exported editor backup for each Rongzhai article."""

from __future__ import annotations

import argparse
import base64
import csv
import json
from pathlib import Path
import re
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parent
SHARED_IMPORTER = BASE_DIR.parent / "shiji" / "shiji_lisheng_lujia" / "import_editor_export.py"


def read_catalog() -> dict[str, dict[str, str]]:
    with (BASE_DIR / "catalog.csv").open(encoding="utf-8-sig", newline="") as file:
        return {row["source_id"]: row for row in csv.DictReader(file)}


def entry_dir(row: dict[str, str]) -> Path:
    return BASE_DIR / f"volume_{int(row['volume']):02d}" / f"{int(row['sequence']):03d}_{row['slug']}"


def newest_exports(downloads: Path) -> dict[str, Path]:
    selected: dict[str, Path] = {}
    for path in downloads.glob("article_*_editor_backup*.json"):
        match = re.fullmatch(r"article_(\d+)_editor_backup(?: \(\d+\))?\.json", path.name)
        if not match:
            continue
        source_id = match.group(1)
        current = selected.get(source_id)
        if current is None or path.stat().st_mtime > current.stat().st_mtime:
            selected[source_id] = path
    return selected


def write_seed(target: Path, row: dict[str, str], export_path: Path) -> int:
    data = json.loads(export_path.read_text(encoding="utf-8"))
    media_dir = target / "media"
    stored_media = []
    for item in data.get("media") or []:
        media_id = str(item.get("id", ""))
        match = re.fullmatch(r"data:([^;,]+);base64,(.*)", item.get("dataUrl", ""), re.DOTALL)
        if not media_id or not match:
            continue
        media_dir.mkdir(exist_ok=True)
        extension = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}.get(match.group(1), ".bin")
        media_path = media_dir / f"inline_{media_id}{extension}"
        media_path.write_bytes(base64.b64decode(match.group(2)))
        stored_media.append({
            "id": media_id,
            "name": item.get("name") or media_path.name,
            "type": match.group(1),
            "size": media_path.stat().st_size,
            "path": str(media_path.relative_to(target)),
        })
    seed = {
        "savedAt": data.get("savedAt"),
        "bodyHTML": data.get("bodyHTML", ""),
        "footnotes": data.get("footnotes") or [],
        "notes": data.get("notes") or [],
        "media": stored_media,
    }
    seed_path = target / f"{row['slug']}_editor_seed.json"
    seed_path.write_text(json.dumps(seed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(stored_media)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("exports", nargs="*", type=Path, help="Specific backup JSON files; otherwise use newest files in Downloads")
    parser.add_argument("--downloads", type=Path, default=Path.home() / "Downloads")
    args = parser.parse_args()
    catalog = read_catalog()
    if args.exports:
        exports = {}
        for path in args.exports:
            match = re.search(r"article_(\d+)_editor_backup", path.name)
            if not match:
                raise ValueError(f"Unrecognized Rongzhai backup name: {path}")
            exports[match.group(1)] = path
    else:
        exports = newest_exports(args.downloads)
    unknown = exports.keys() - catalog.keys()
    if unknown:
        raise ValueError(f"Backups are not present in catalog.csv: {', '.join(sorted(unknown))}")
    if not exports:
        raise FileNotFoundError(f"No article_*_editor_backup*.json files found in {args.downloads}")
    for source_id in sorted(exports, key=lambda value: int(catalog[value]["sequence"])):
        row = catalog[source_id]
        target = entry_dir(row)
        command = [
            sys.executable, str(SHARED_IMPORTER), str(exports[source_id]),
            "--clean", str(target / "reading.txt"),
            "--dictionary", str(target / "reading_terms.csv"),
            "--review-notes", str(target / "review_notes.tsv"),
            "--inline-notes", str(target / "inline_notes.tsv"),
            "--reading-notes", str(target / f"{row['slug']}_reading_notes.txt"),
            "--backup", str(target / "reading_before_editor.txt"),
        ]
        subprocess.run(command, check=True)
        media_count = write_seed(target, row, exports[source_id])
        print(f"Persisted editor seed for {source_id} ({media_count} media files)")
    subprocess.run([sys.executable, str(BASE_DIR / "build_editors.py")], check=True)
    subprocess.run([sys.executable, str(BASE_DIR.parent / "build_index.py")], check=True)
    print(f"Processed {len(exports)} Rongzhai editor backup(s)")


if __name__ == "__main__":
    main()
