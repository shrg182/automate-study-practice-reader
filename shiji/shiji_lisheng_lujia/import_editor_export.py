#!/usr/bin/env python3
"""Promote a Shiji editor JSON backup into clean text and review data."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path

from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DOWNLOADS = Path("/Users/ruixingshi/Downloads")
TONE_MARKS = {
    "a": "āáǎà", "e": "ēéěè", "i": "īíǐì", "o": "ōóǒò",
    "u": "ūúǔù", "ü": "ǖǘǚǜ", "v": "ǖǘǚǜ",
}


def newest_export() -> Path:
    candidates = list(DEFAULT_DOWNLOADS.glob("lisheng_lujia_editor_backup*.json"))
    if not candidates:
        raise FileNotFoundError(f"No editor backup JSON found in {DEFAULT_DOWNLOADS}")
    return max(candidates, key=lambda path: path.stat().st_mtime)


def load_existing_terms(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError(f"Dictionary has no header: {path}")
        return reader.fieldnames, list(reader)


def normalize_pinyin(value: str) -> str:
    """Convert simple numbered pinyin such as shui4 ke4 to shuì kè."""
    def mark_syllable(raw: str) -> str:
        if not raw or raw[-1] not in "1234":
            return raw
        tone = int(raw[-1]) - 1
        syllable = raw[:-1]
        vowel_index = -1
        for preferred in "ae":
            if preferred in syllable:
                vowel_index = syllable.index(preferred)
                break
        if vowel_index == -1 and "ou" in syllable:
            vowel_index = syllable.index("o")
        if vowel_index == -1:
            vowel_index = max(
                (index for index, char in enumerate(syllable) if char in TONE_MARKS),
                default=-1,
            )
        if vowel_index >= 0:
            vowel = syllable[vowel_index]
            syllable = (
                syllable[:vowel_index]
                + TONE_MARKS[vowel][tone]
                + syllable[vowel_index + 1:]
            )
        return syllable

    words = []
    for raw in value.lower().split():
        # The editor also receives compact input such as "lin2zi1".
        compact = re.findall(r"[a-züv]+[1-4]", raw)
        if compact and "".join(compact) == raw:
            words.extend(mark_syllable(syllable) for syllable in compact)
            continue
        words.append(mark_syllable(raw))
    return " ".join(words)


def collect_notations(soup: BeautifulSoup) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for span in soup.select(".notation"):
        ruby = span.find("ruby")
        rt = span.find("rt")
        pinyin = normalize_pinyin(rt.get_text(" ", strip=True)) if rt else ""
        term = span.get("data-term", "").strip()
        if not term and ruby is not None:
            term = "".join(child for child in ruby.find_all(string=True, recursive=False)).strip()
        if not term:
            clone = BeautifulSoup(str(ruby or span), "html.parser")
            clone_rt = clone.find("rt")
            if clone_rt:
                clone_rt.decompose()
            for gloss in clone.select(".inline-gloss"):
                gloss.decompose()
            term = clone.get_text("", strip=True)
        if not term or term in seen:
            continue
        seen.add(term)
        entries.append(
            {
                "term": term,
                "pinyin": pinyin,
                "type": "added",
                "annotation": span.get("data-note", "").strip() or "编辑器中人工添加的阅读注音。",
            }
        )
    return entries


def clean_paragraph_text(paragraph) -> str:
    clone = BeautifulSoup(str(paragraph), "html.parser")
    root = clone.find("p") or clone
    # Interlinear notes are ruby annotations: retain their base text, but do not
    # promote the explanatory <rt> text into the clean article.
    for interlinear in reversed(root.select(".interlinear-note")):
        ruby = interlinear.find("ruby", recursive=False)
        if ruby:
            for rt in ruby.find_all("rt", recursive=False):
                rt.decompose()
            ruby.unwrap()
        interlinear.unwrap()
    for notation in root.select(".notation"):
        ruby = notation.find("ruby")
        if ruby:
            rt = ruby.find("rt")
            if rt:
                rt.decompose()
            notation.replace_with(ruby.get_text("", strip=True))
        else:
            for gloss in notation.select(".inline-gloss"):
                gloss.decompose()
            notation.replace_with(notation.get("data-term", "").strip() or notation.get_text("", strip=True))
    for ref in root.select(".footnote-ref"):
        ref.replace_with(ref.get_text("", strip=True))
    # Strip only the paragraph edges. Using ``strip=True`` here strips every
    # individual text node, which joins words across formatting spans (for
    # example ``Training <span>turns</span>`` became ``Trainingturns``).
    text = root.get_text("", strip=False).strip()
    if "comment-block" in (root.get("class") or []):
        return f"〔按语：{text}〕"
    return text


def interlinear_base_text(span) -> str:
    clone = BeautifulSoup(str(span), "html.parser")
    for rt in clone.select("rt"):
        rt.decompose()
    return clone.get_text("", strip=False).strip()


def write_interlinear_notes(path: Path | None, soup: BeautifulSoup) -> int:
    if path is None:
        return 0
    rows = []
    for span in soup.select(".interlinear-note"):
        # A later annotation may wrap an earlier one. Keep the outer, newer
        # annotation so the same source phrase is not exported twice.
        if span.find_parent(class_="interlinear-note"):
            continue
        text = interlinear_base_text(span)
        note = span.get("data-note", "").strip()
        if text and note:
            rows.append({"text": text, "note": note})
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "note"], delimiter="\t")
        writer.writeheader()
        if rows:
            writer.writerows(rows)
    return len(rows)


def build_clean_text(soup: BeautifulSoup, footnotes: list[dict[str, str]]) -> str:
    paragraphs = [clean_paragraph_text(paragraph) for paragraph in soup.find_all("p", recursive=False)]
    paragraphs = [paragraph for paragraph in paragraphs if paragraph]
    body = "\n\n".join(paragraphs)
    if footnotes:
        for number, item in enumerate(footnotes, 1):
            marker = f"〔{number}〕"
            if marker in body:
                continue
            note = item.get("note", "").strip()
            subject = note.split("：", 1)[0].split(":", 1)[0].strip()
            if subject and subject in body:
                body = body.replace(subject, subject + marker, 1)
        notes = [f"〔{number}〕{item.get('note', '').strip()}" for number, item in enumerate(footnotes, 1)]
        body += "\n\n脚注\n\n" + "\n".join(notes)
    return body.strip() + "\n"


def order_footnotes_by_anchor(soup: BeautifulSoup, footnotes: list[dict[str, str]]) -> list[dict[str, str]]:
    """Return footnotes in their正文 anchor order, retaining unanchored notes last."""
    by_id = {str(item.get("id", "")): item for item in footnotes}
    ordered = []
    seen = set()
    for ref in soup.select(".footnote-ref[data-note-id]"):
        note_id = str(ref.get("data-note-id", ""))
        if note_id in by_id and note_id not in seen:
            ordered.append(by_id[note_id])
            seen.add(note_id)
    ordered.extend(item for item in footnotes if str(item.get("id", "")) not in seen)
    return ordered


def write_review_notes(path: Path, soup: BeautifulSoup) -> int:
    rows = []
    for doubtful in soup.select(".doubt"):
        clone = BeautifulSoup(str(doubtful), "html.parser")
        for rt in clone.select("rt"):
            rt.decompose()
        for gloss in clone.select(".inline-gloss"):
            gloss.decompose()
        rows.append(
            {
                "text": clone.get_text("", strip=False).strip(),
                "issue": doubtful.get("data-issue", "").strip(),
                "status": "open",
            }
        )
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "issue", "status"], delimiter="\t")
        writer.writeheader()
        if rows:
            writer.writerows(rows)
    return len(rows)


def write_reading_notes(path: Path | None, notes: list[dict[str, str]]) -> int:
    if path is None:
        return 0
    rows = []
    for item in notes:
        timestamp = str(item.get("time", "")).strip()
        text = str(item.get("text", "")).strip()
        if timestamp and text:
            rows.append(f"{timestamp}\t{text}")
    if not rows:
        return 0
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Import the newest or specified Shiji editor JSON backup.")
    parser.add_argument("export", nargs="?", type=Path, default=None)
    parser.add_argument("--clean", type=Path, default=BASE_DIR / "lisheng_lujia_clean.txt")
    parser.add_argument("--dictionary", type=Path, default=BASE_DIR / "reading_terms.csv")
    parser.add_argument("--review-notes", type=Path, default=BASE_DIR / "review_notes.tsv")
    parser.add_argument("--inline-notes", type=Path, default=None)
    parser.add_argument("--reading-notes", type=Path, default=None)
    parser.add_argument("--backup", type=Path, default=BASE_DIR / "lisheng_lujia_clean_before_editor.txt")
    args = parser.parse_args()

    export_path = args.export or newest_export()
    data = json.loads(export_path.read_text(encoding="utf-8"))
    body_html = data.get("bodyHTML")
    if not isinstance(body_html, str) or not body_html.strip():
        raise ValueError(f"Editor backup has no bodyHTML: {export_path}")
    soup = BeautifulSoup(body_html, "html.parser")
    footnotes = order_footnotes_by_anchor(soup, data.get("footnotes") or [])
    clean_text = build_clean_text(soup, footnotes)

    if args.clean.exists() and not args.backup.exists():
        shutil.copyfile(args.clean, args.backup)
    args.clean.write_text(clean_text, encoding="utf-8")

    fields, existing = load_existing_terms(args.dictionary)
    by_term = {row.get("term", ""): row for row in existing}
    added = 0
    updated = 0
    for saved in data.get("terms") or []:
        term = str(saved.get("term", "")).strip()
        if not term or term not in by_term:
            continue
        row = by_term[term]
        pinyin = normalize_pinyin(str(saved.get("pinyin", "")).strip())
        annotation = str(saved.get("annotation", "")).strip()
        if row.get("pinyin", "") != pinyin or row.get("annotation", "") != annotation:
            row["pinyin"] = pinyin
            row["annotation"] = annotation
            updated += 1
    for entry in collect_notations(soup):
        if entry["term"] not in by_term:
            existing.append(entry)
            by_term[entry["term"]] = entry
            added += 1
        elif by_term[entry["term"]].get("type") == "added":
            # Do not erase a previously reviewed value when an editor export
            # leaves one of the optional fields blank.
            by_term[entry["term"]]["pinyin"] = (
                by_term[entry["term"]].get("pinyin", "") or entry["pinyin"]
            )
            by_term[entry["term"]]["annotation"] = (
                by_term[entry["term"]].get("annotation", "")
                or entry["annotation"]
            )
    with args.dictionary.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(existing)

    review_count = write_review_notes(args.review_notes, soup)
    interlinear_count = write_interlinear_notes(args.inline_notes, soup)
    reading_note_count = write_reading_notes(args.reading_notes, data.get("notes") or [])
    print(f"Imported editor backup: {export_path}")
    print(f"Updated clean text: {args.clean}")
    print(f"Pre-import backup: {args.backup}")
    print(f"Paragraph blocks: {clean_text.count(chr(10) + chr(10)) + 1}")
    print(f"New dictionary entries: {added}")
    print(f"Updated dictionary entries: {updated}")
    print(f"Open review notes: {review_count}")
    print(f"Interlinear notes: {interlinear_count}")
    print(f"Reader notes: {reading_note_count}")


if __name__ == "__main__":
    main()
