#!/usr/bin/env python3
"""Import a Chinese-wars period backup and rebuild that period."""

from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
import re
import subprocess
import sys

import manage


BASE_DIR = Path(__file__).resolve().parent
PRACTICE_DIR = BASE_DIR.parent
SHARED_IMPORTER = PRACTICE_DIR / "shiji" / "shiji_lisheng_lujia" / "import_editor_export.py"


def store_media(target: Path, data: dict[str, object]) -> list[dict[str, object]]:
    stored: list[dict[str, object]] = []
    for item in data.get("media") or []:
        if not isinstance(item, dict):
            continue
        match = re.fullmatch(r"data:([^;,]+);base64,(.*)", str(item.get("dataUrl", "")), re.DOTALL)
        media_id = str(item.get("id", ""))
        if not match or not media_id:
            continue
        media_dir = target / "media"
        media_dir.mkdir(exist_ok=True)
        extension = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}.get(match.group(1), ".bin")
        path = media_dir / f"inline_{media_id}{extension}"
        path.write_bytes(base64.b64decode(match.group(2)))
        stored.append({"id": media_id, "name": item.get("name") or path.name, "type": match.group(1), "size": path.stat().st_size, "path": str(path.relative_to(target))})
    return stored


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("backup", type=Path)
    args = parser.parse_args()
    match = re.search(r"chinese_wars_([a-z_]+)_editor_backup", args.backup.name)
    if not match or match.group(1) not in manage.PERIODS:
        raise ValueError(f"Unrecognized backup filename: {args.backup.name}")
    period_id = match.group(1)
    target = manage.period_dir(period_id)
    data = json.loads(args.backup.read_text(encoding="utf-8"))
    subprocess.run([
        sys.executable, str(SHARED_IMPORTER), str(args.backup),
        "--clean", str(target / "reading.txt"),
        "--dictionary", str(target / "reading_terms.csv"),
        "--review-notes", str(target / "review_notes.tsv"),
        "--inline-notes", str(target / "inline_notes.tsv"),
        "--reading-notes", str(target / "reading_notes.txt"),
        "--backup", str(target / "reading_before_editor.txt"),
    ], check=True)
    seed = {"savedAt": data.get("savedAt"), "bodyHTML": data.get("bodyHTML", ""), "footnotes": data.get("footnotes") or [], "notes": data.get("notes") or [], "media": store_media(target, data)}
    (target / "editor_seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = [row for row in manage.read_csv(manage.CATALOG) if row["period_id"] == period_id]
    if not rows:
        raise ValueError(f"No active catalog entries for {period_id}")
    manage.build_period(period_id, rows)
    subprocess.run([sys.executable, str(PRACTICE_DIR / "build_index.py")], check=True)
    print(f"Imported {args.backup} and rebuilt {period_id} with {len(rows)} entries")


if __name__ == "__main__":
    main()
