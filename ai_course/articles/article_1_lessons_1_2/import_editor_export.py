#!/usr/bin/env python3
"""Import an Article 1 editor JSON backup."""

from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parents[2] / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))
import import_editor_export as shared  # noqa: E402

if __name__ == "__main__":
    supplied = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if supplied is None:
        candidates = list((Path.home() / "Downloads").glob("ai_course_article_1_editor_backup*.json"))
        if not candidates:
            raise SystemExit("No Article 1 editor backup found in Downloads.")
        supplied = max(candidates, key=lambda path: path.stat().st_mtime)
    sys.argv = [sys.argv[0], str(supplied), "--clean", str(BASE_DIR / "article_1_clean.txt"), "--dictionary", str(BASE_DIR / "reading_terms.csv"), "--review-notes", str(BASE_DIR / "review_notes.tsv"), "--inline-notes", str(BASE_DIR / "inline_notes.tsv"), "--reading-notes", str(BASE_DIR / "article_1_reading_notes.txt"), "--backup", str(BASE_DIR / "article_1_clean_before_editor.txt")]
    shared.main()
