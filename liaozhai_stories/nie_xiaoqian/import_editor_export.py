#!/usr/bin/env python3
"""Import the newest 《聂小倩》 editor backup."""

from pathlib import Path
import base64
import csv
import json
import re
import sys

from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parents[1] / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))

import import_editor_export as shared  # noqa: E402


def promote_inline_images(export_path: Path) -> int:
    """Synchronize exported正文/media state into the durable editor seed."""
    data = json.loads(export_path.read_text(encoding="utf-8"))
    seed_path = BASE_DIR / "nie_xiaoqian_editor_seed.json"
    seed = json.loads(seed_path.read_text(encoding="utf-8"))
    exported = BeautifulSoup(data.get("bodyHTML", ""), "html.parser")
    existing_media = {str(item.get("id", "")): item for item in seed.get("media") or []}
    added = 0

    synchronized_media = []
    for item in data.get("media") or []:
        media_id = str(item.get("id", ""))
        if not media_id:
            continue
        if media_id in existing_media and (BASE_DIR / existing_media[media_id]["path"]).exists():
            synchronized_media.append(existing_media[media_id])
            continue
        match = re.fullmatch(r"data:([^;,]+);base64,(.*)", item.get("dataUrl", ""), re.DOTALL)
        if not match:
            raise ValueError(f"Inline image has no usable data URL: {media_id}")
        extension = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}.get(
            match.group(1), ".bin"
        )
        media_path = BASE_DIR / "media" / f"inline_{media_id}{extension}"
        media_path.write_bytes(base64.b64decode(match.group(2)))
        stored = {
            "id": media_id,
            "name": item.get("name") or media_path.name,
            "type": match.group(1),
            "size": media_path.stat().st_size,
            "path": str(media_path.relative_to(BASE_DIR)),
        }
        synchronized_media.append(stored)
        added += 1

    seed["bodyHTML"] = exported.decode_contents()
    seed["savedAt"] = data.get("savedAt") or seed.get("savedAt")
    seed["footnotes"] = data.get("footnotes") or seed.get("footnotes") or []
    seed["notes"] = data.get("notes") or seed.get("notes") or []
    seed["media"] = synchronized_media
    seed_path.write_text(json.dumps(seed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added


def normalize_resolved_placeholders() -> None:
    """Apply glyphs established during manual review and retain unresolved ones."""
    clean_path = BASE_DIR / "nie_xiaoqian.txt"
    clean = clean_path.read_text(encoding="utf-8")
    clean = clean.replace("[黑+曷]", "𪑦").replace("[单人旁+匡]㑌", "㑌")
    clean = re.sub(r"\n\n〔按语：.*?〕\n\n", "\n\n", clean, flags=re.DOTALL)
    clean = re.sub(r"〔\d+〕", "", clean)
    clean = clean.split("\n\n脚注\n\n", 1)[0].rstrip() + "\n"
    clean_path.write_text(clean, encoding="utf-8")

    dictionary_path = BASE_DIR / "nie_xiaoqian_rare_words.csv"
    with dictionary_path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        fields = reader.fieldnames or ["term", "pinyin", "annotation"]
        rows = list(reader)
    aliases = {"黑+曷": "𪑦", "[单人旁+匡]㑌": "㑌"}
    canonical = {row.get("term", "") for row in rows} - set(aliases)
    filtered = []
    for row in rows:
        term = row.get("term", "")
        if term in aliases and aliases[term] in canonical:
            continue
        row["term"] = aliases.get(term, term)
        filtered.append(row)
    with dictionary_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(filtered)

    review_path = BASE_DIR / "review_notes.tsv"
    review_path.write_text(
        "text\tissue\tstatus\n"
        "半年渐啜稀[生僻字]\t源网页未显示该字，人工编辑尚未确定原字\topen\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    supplied = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if supplied is None:
        candidates = list(
            (Path.home() / "Downloads").glob("nie_xiaoqian_editor_backup*.json")
        )
        if not candidates:
            raise SystemExit("No nie_xiaoqian_editor_backup*.json found in Downloads.")
        supplied = max(candidates, key=lambda path: path.stat().st_mtime)
    sys.argv = [
        sys.argv[0],
        str(supplied),
        "--clean",
        str(BASE_DIR / "nie_xiaoqian.txt"),
        "--dictionary",
        str(BASE_DIR / "nie_xiaoqian_rare_words.csv"),
        "--review-notes",
        str(BASE_DIR / "review_notes.tsv"),
        "--inline-notes",
        str(BASE_DIR / "inline_notes.tsv"),
        "--reading-notes",
        str(BASE_DIR / "nie_xiaoqian_reading_notes.txt"),
        "--backup",
        str(BASE_DIR / "nie_xiaoqian_clean_before_editor.txt"),
    ]
    shared.main()
    normalize_resolved_placeholders()
    print(f"New inline images promoted: {promote_inline_images(supplied)}")
