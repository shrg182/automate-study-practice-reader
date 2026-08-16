#!/usr/bin/env python3
"""Import exported 《三十六计》 editor backups and rebuild the collection."""

from __future__ import annotations

import base64
import csv
import json
from pathlib import Path
import re
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parent
PRACTICE_DIR = BASE_DIR.parent
SHARED_IMPORTER = PRACTICE_DIR / "shiji" / "shiji_lisheng_lujia" / "import_editor_export.py"
sys.path.insert(0, str(PRACTICE_DIR))


def catalog() -> dict[str, dict[str, str]]:
    with (BASE_DIR / "catalog.csv").open(encoding="utf-8-sig", newline="") as file:
        return {row["sequence"]: row for row in csv.DictReader(file)}


def write_seed(target: Path, sequence: int, export_path: Path) -> int:
    data = json.loads(export_path.read_text(encoding="utf-8"))
    stored_media = []
    for item in data.get("media") or []:
        media_id = str(item.get("id", ""))
        match = re.fullmatch(r"data:([^;,]+);base64,(.*)", item.get("dataUrl", ""), re.DOTALL)
        if not media_id or not match:
            continue
        media_dir = target / "media"
        media_dir.mkdir(exist_ok=True)
        extension = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}.get(match.group(1), ".bin")
        media_path = media_dir / f"inline_{media_id}{extension}"
        media_path.write_bytes(base64.b64decode(match.group(2)))
        stored_media.append({"id": media_id, "name": item.get("name") or media_path.name, "type": match.group(1), "size": media_path.stat().st_size, "path": str(media_path.relative_to(target))})
    seed = {"savedAt": data.get("savedAt"), "bodyHTML": data.get("bodyHTML", ""), "footnotes": data.get("footnotes") or [], "notes": data.get("notes") or [], "media": stored_media}
    (target / f"thirty_six_stratagems_{sequence:02d}_editor_seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(stored_media)


def main() -> None:
    exports = [Path(value) for value in sys.argv[1:]]
    if not exports:
        exports = sorted((Path.home() / "Downloads").glob("thirty_six_stratagems_*_editor_backup*.json"))
    rows = catalog()
    if not exports:
        raise FileNotFoundError("No 《三十六计》 editor backups found")
    for export_path in exports:
        match = re.search(r"thirty_six_stratagems_(\d+)_editor_backup", export_path.name)
        if not match or str(int(match.group(1))) not in rows:
            raise ValueError(f"Unrecognized backup: {export_path}")
        sequence = int(match.group(1))
        row = rows[str(sequence)]
        target = BASE_DIR / f"{sequence:02d}_{row['slug']}"
        command = [sys.executable, str(SHARED_IMPORTER), str(export_path), "--clean", str(target / "reading.txt"), "--dictionary", str(target / "reading_terms.csv"), "--review-notes", str(target / "review_notes.tsv"), "--inline-notes", str(target / "inline_notes.tsv"), "--reading-notes", str(target / f"thirty_six_stratagems_{sequence:02d}_reading_notes.txt"), "--backup", str(target / "reading_before_editor.txt")]
        subprocess.run(command, check=True)
        print(f"Persisted editor seed for entry {sequence} ({write_seed(target, sequence, export_path)} media files)")
    subprocess.run([sys.executable, str(BASE_DIR / "manage.py"), "build-selector"], check=True)
    from guwendao_collection import build_editors
    build_editors(BASE_DIR, json.loads((BASE_DIR / "collection.json").read_text(encoding="utf-8")))
    subprocess.run([sys.executable, str(PRACTICE_DIR / "build_index.py")], check=True)
    print(f"Processed {len(exports)} 《三十六计》 backup(s)")


if __name__ == "__main__":
    main()
