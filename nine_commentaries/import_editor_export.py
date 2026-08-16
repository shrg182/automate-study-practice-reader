#!/usr/bin/env python3
"""
Import an editor TXT export back into the project files.

The browser editor stores live edits in localStorage, which belongs to one
browser on one computer. This script makes the downloaded TXT export portable:
it updates both the chapter's clean-edited text file and the embedded textarea
contents in editor.html.

Usage:
    python3 practice/nine_commentaries/import_editor_export.py \
        practice/nine_commentaries/chapter_01 \
        ~/Downloads/chapter_01_clean_edited.txt

    python3 practice/nine_commentaries/import_editor_export.py \
        practice/nine_commentaries/chapter_01 --latest-download
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


PAGE_HEADER_RE = re.compile(
    r"^===== PDF page (?P<pdf>\d{3}) / printed page (?P<printed>-?\d+) =====\s*$",
    re.MULTILINE,
)


def read_text(path: Path) -> str:
    """Read UTF-8 text, accepting the common UTF-8 BOM if present."""
    return path.read_text(encoding="utf-8-sig")


def parse_export(export_text: str) -> dict[str, str]:
    """Return page text keyed by PDF page number."""
    matches = list(PAGE_HEADER_RE.finditer(export_text))
    if not matches:
        raise ValueError("No PDF page headers found in export text.")

    pages: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(export_text)
        pages[match.group("pdf")] = export_text[start:end].strip("\n")

    return pages


def find_clean_edited_file(chapter_dir: Path) -> Path:
    """Find the chapter clean-edited text file."""
    candidates = sorted(chapter_dir.glob("*_clean_edited.txt"))
    if not candidates:
        raise FileNotFoundError(f"No *_clean_edited.txt file found in {chapter_dir}")
    if len(candidates) > 1:
        names = ", ".join(path.name for path in candidates)
        raise RuntimeError(f"More than one clean-edited file found: {names}")
    return candidates[0]


def find_latest_download(chapter_dir: Path) -> Path:
    """Find the newest matching clean-edited TXT export in ~/Downloads."""
    clean_file = find_clean_edited_file(chapter_dir)
    stem = clean_file.stem
    downloads = Path.home() / "Downloads"
    candidates = list(downloads.glob(f"{stem}*.txt"))
    if not candidates:
        raise FileNotFoundError(f"No {stem}*.txt export found in {downloads}")
    return max(candidates, key=lambda path: path.stat().st_mtime)


def update_editor_html(editor_html: str, pages: dict[str, str]) -> tuple[str, list[str], list[str]]:
    """Replace textarea contents from exported page text."""
    changed: list[str] = []
    missing: list[str] = []
    updated_html = editor_html

    for pdf_page, page_text in pages.items():
        escaped_text = html.escape(page_text, quote=False)
        pattern = re.compile(
            rf'(<textarea\b(?=[^>]*\bdata-page="{re.escape(pdf_page)}")[^>]*>)(.*?)(</textarea>)',
            re.DOTALL,
        )
        def replace(match: re.Match[str]) -> str:
            return f"{match.group(1)}{escaped_text}{match.group(3)}"

        updated_html, count = pattern.subn(replace, updated_html, count=1)
        if count:
            changed.append(pdf_page)
        else:
            missing.append(pdf_page)

    return updated_html, changed, missing


def import_export(chapter_dir: Path, export_path: Path, dry_run: bool = False) -> None:
    """Import one downloaded editor export into project files."""
    chapter_dir = chapter_dir.expanduser().resolve()
    export_path = export_path.expanduser().resolve()
    editor_path = chapter_dir / "editor.html"
    clean_path = find_clean_edited_file(chapter_dir)

    if not chapter_dir.is_dir():
        raise FileNotFoundError(f"Chapter folder does not exist: {chapter_dir}")
    if not editor_path.is_file():
        raise FileNotFoundError(f"editor.html does not exist: {editor_path}")
    if not export_path.is_file():
        raise FileNotFoundError(f"Export TXT does not exist: {export_path}")

    export_text = read_text(export_path).rstrip() + "\n"
    pages = parse_export(export_text)
    editor_text = read_text(editor_path)
    updated_editor, changed_pages, missing_pages = update_editor_html(editor_text, pages)

    print(f"Export: {export_path}")
    print(f"Chapter: {chapter_dir}")
    print(f"Pages in export: {len(pages)}")
    print(f"Textarea pages updated: {len(changed_pages)}")
    if missing_pages:
        print("Pages missing from editor.html: " + ", ".join(missing_pages))

    if dry_run:
        print("Dry run only; no files written.")
        return

    clean_path.write_text(export_text, encoding="utf-8")
    editor_path.write_text(updated_editor, encoding="utf-8")
    print(f"Updated: {clean_path}")
    print(f"Updated: {editor_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import a downloaded editor TXT export into clean text and editor.html."
    )
    parser.add_argument(
        "chapter_dir",
        type=Path,
        help="Chapter folder containing editor.html and *_clean_edited.txt.",
    )
    parser.add_argument(
        "export_txt",
        nargs="?",
        type=Path,
        help="Downloaded TXT export. Omit when using --latest-download.",
    )
    parser.add_argument(
        "--latest-download",
        action="store_true",
        help="Use the newest matching *_clean_edited*.txt file in ~/Downloads.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and report changes without writing files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    chapter_dir = args.chapter_dir.expanduser().resolve()

    if args.latest_download:
        export_path = find_latest_download(chapter_dir)
    elif args.export_txt:
        export_path = args.export_txt
    else:
        raise SystemExit("Provide an export TXT path or use --latest-download.")

    import_export(chapter_dir, export_path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
