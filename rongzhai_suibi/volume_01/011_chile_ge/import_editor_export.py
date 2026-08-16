#!/usr/bin/env python3
"""Import the newest 《容斋随笔·敕勒歌》 editor backup."""

from pathlib import Path
import base64
import json
import re
import sys


BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parents[2] / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))

import import_editor_export as shared  # noqa: E402


def write_seed(export_path: Path) -> int:
    data = json.loads(export_path.read_text(encoding="utf-8"))
    media_dir = BASE_DIR / "media"
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
            "path": str(media_path.relative_to(BASE_DIR)),
        })
    seed = {
        "savedAt": data.get("savedAt"),
        "bodyHTML": data.get("bodyHTML", ""),
        "footnotes": data.get("footnotes") or [],
        "notes": data.get("notes") or [],
        "media": stored_media,
    }
    (BASE_DIR / "chile_ge_editor_seed.json").write_text(
        json.dumps(seed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return len(stored_media)


if __name__ == "__main__":
    supplied = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if supplied is None:
        candidates = list((Path.home() / "Downloads").glob("chile_ge_editor_backup*.json"))
        if not candidates:
            raise SystemExit("No chile_ge_editor_backup*.json found in Downloads.")
        supplied = max(candidates, key=lambda path: path.stat().st_mtime)
    sys.argv = [
        sys.argv[0], str(supplied),
        "--clean", str(BASE_DIR / "reading.txt"),
        "--dictionary", str(BASE_DIR / "reading_terms.csv"),
        "--review-notes", str(BASE_DIR / "review_notes.tsv"),
        "--inline-notes", str(BASE_DIR / "inline_notes.tsv"),
        "--reading-notes", str(BASE_DIR / "chile_ge_reading_notes.txt"),
        "--backup", str(BASE_DIR / "reading_before_editor.txt"),
    ]
    shared.main()
    print(f"Media files persisted: {write_seed(supplied)}")
