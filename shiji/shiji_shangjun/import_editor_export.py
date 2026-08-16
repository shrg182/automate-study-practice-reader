#!/usr/bin/env python3
"""Import a Shangjun editor JSON backup."""
from pathlib import Path
import json
import re
import shutil
import sys

from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parent / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))
import import_editor_export as shared


def visible_text(element) -> str:
    clone = BeautifulSoup(str(element), "html.parser")
    for node in clone.select("rt,.inline-gloss"):
        node.decompose()
    return clone.get_text("", strip=True)


def export_text_styles(body_html: str, output: Path) -> int:
    soup = BeautifulSoup(body_html, "html.parser")
    styles = []
    for element in soup.select("[style]"):
        declarations = {}
        for declaration in element.get("style", "").split(";"):
            if ":" not in declaration:
                continue
            name, value = declaration.split(":", 1)
            declarations[name.strip().lower()] = value.strip().lower()
        background = declarations.get("background-color", "")
        rgb_match = re.fullmatch(
            r"rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)",
            background,
        )
        if rgb_match:
            channels = [min(255, int(value)) for value in rgb_match.groups()]
            background = "#" + "".join(f"{value:02x}" for value in channels)
        elif not re.fullmatch(r"#[0-9a-f]{6}", background):
            background = ""
        bold = declarations.get("font-weight", "") in {"bold", "600", "700", "800", "900"}
        underline = "underline" in declarations.get("text-decoration", "") or "underline" in declarations.get("text-decoration-line", "")
        text = visible_text(element)
        if text and (background or bold or underline):
            styles.append({"text": text, "background": background, "bold": bold, "underline": underline})
    output.write_text(json.dumps(styles, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(styles)

if __name__ == "__main__":
    supplied = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if supplied is None:
        candidates = list((Path.home() / "Downloads").glob("shangjun_editor_backup*.json"))
        if not candidates:
            raise SystemExit("No shangjun_editor_backup*.json found in Downloads.")
        supplied = max(candidates, key=lambda path: path.stat().st_mtime)
    sys.argv = [
        sys.argv[0], str(supplied),
        "--clean", str(BASE_DIR / "shangjun_clean.txt"),
        "--dictionary", str(BASE_DIR / "reading_terms.csv"),
        "--review-notes", str(BASE_DIR / "review_notes.tsv"),
        "--inline-notes", str(BASE_DIR / "inline_notes.tsv"),
        "--backup", str(BASE_DIR / "shangjun_clean_before_editor.txt"),
    ]
    shared.main()

    data = json.loads(supplied.read_text(encoding="utf-8"))
    style_count = export_text_styles(data.get("bodyHTML", ""), BASE_DIR / "text_styles.json")
    export_dir = supplied.parent
    suffix_match = re.fullmatch(r"shangjun_editor_backup(.*)", supplied.stem)
    export_suffix = suffix_match.group(1) if suffix_match else ""
    exported_log = export_dir / f"shangjun_edit_log{export_suffix}.txt"
    exported_notes = export_dir / f"shangjun_reading_notes{export_suffix}.txt"
    local_log = BASE_DIR / "shangjun_edit_log.txt"
    local_notes = BASE_DIR / "shangjun_reading_notes.txt"

    if exported_log.exists():
        shutil.copyfile(exported_log, local_log)
    else:
        local_log.write_text(
            "".join(
                f"{item.get('time', '')}\t{item.get('action', '')}\t{item.get('detail', '')}\n"
                for item in data.get("log") or []
            ),
            encoding="utf-8",
        )
    if exported_notes.exists():
        shutil.copyfile(exported_notes, local_notes)
    else:
        local_notes.write_text(
            "".join(
                f"{item.get('time', '')}\t{item.get('text', '')}\n"
                for item in data.get("notes") or []
            ),
            encoding="utf-8",
        )
    print(f"Imported edit log: {local_log}")
    print(f"Imported reading notes: {local_notes}")
    print(f"Imported editor text styles: {style_count}")
