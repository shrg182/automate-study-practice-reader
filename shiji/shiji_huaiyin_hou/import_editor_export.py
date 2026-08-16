#!/usr/bin/env python3
"""Import the newest Huaiyin Hou editor backup."""
from pathlib import Path
import shutil
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parent / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))
import import_editor_export as shared

if __name__ == "__main__":
    downloads = Path.home() / "Downloads"
    supplied = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if supplied is None:
        candidates = list(
            downloads.glob(
                "huaiyin_hou_editor_backup*.json"
            )
        )
        if not candidates:
            raise SystemExit("No huaiyin_hou_editor_backup*.json found in Downloads.")
        supplied = max(candidates, key=lambda path: path.stat().st_mtime)
    sys.argv = [
        sys.argv[0],
        str(supplied),
        "--clean",
        str(BASE_DIR / "huaiyin_hou_clean.txt"),
        "--dictionary",
        str(BASE_DIR / "reading_terms.csv"),
        "--review-notes",
        str(BASE_DIR / "review_notes.tsv"),
        "--inline-notes",
        str(BASE_DIR / "inline_notes.tsv"),
        "--backup",
        str(BASE_DIR / "huaiyin_hou_clean_before_editor.txt"),
    ]
    shared.main()

    supplemental_exports = {
        "huaiyin_hou_reading_notes*.txt": BASE_DIR / "huaiyin_hou_reading_notes.txt",
        "huaiyin_hou_edit_log*.txt": BASE_DIR / "huaiyin_hou_edit_log.txt",
    }
    for pattern, destination in supplemental_exports.items():
        matches = list(downloads.glob(pattern))
        if not matches:
            continue
        newest = max(matches, key=lambda path: path.stat().st_mtime)
        shutil.copyfile(newest, destination)
        content = destination.read_text(encoding="utf-8")
        destination.write_text(
            "\n".join(line.rstrip() for line in content.splitlines()) + "\n",
            encoding="utf-8",
        )
        print(f"Imported supplemental export: {newest} -> {destination}")
