#!/usr/bin/env python3
"""Build the project-wide reading dictionary from structured vocabulary sources."""

from __future__ import annotations

import argparse
import ast
import csv
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = Path(__file__).with_name("dictionary.csv")
SOURCE_OUTPUT = Path(__file__).with_name("sources.csv")
WEB_OUTPUT = Path(__file__).with_name("dictionary_data.js")


@dataclass(frozen=True)
class Occurrence:
    term: str
    language: str
    pinyin: str
    entry_type: str
    definition: str
    example: str
    source: str
    source_detail: str
    source_target: str
    source_format: str
    entry_time: str
    difficulty: int


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def language_for(term: str, pinyin: str = "") -> str:
    if re.search(r"[\u3400-\u9fff]", term) or pinyin:
        return "zh"
    if re.search(r"[А-Яа-яЁё]", term):
        return "ru"
    return "en"


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def entry_time_for(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(
        timespec="seconds"
    )


def source_target_for(path: Path, root: Path) -> str:
    """Prefer the reading text beside a vocabulary file, then the file itself."""
    candidates = [
        path.parent / "source.txt",
        path.parent / "editor.html",
    ]
    candidates.extend(sorted(path.parent.glob("*_clean.txt")))
    target = next((candidate for candidate in candidates if candidate.is_file()), path)
    return relative(target, root)


def difficulty_for(entry_type: str, explicit: object = "") -> int:
    """Return a five-level review score derived from the reference-table types."""
    value = clean(explicit).casefold()
    labels = {
        "common": 1,
        "everyday": 1,
        "intermediate": 2,
        "advanced": 3,
        "rare": 4,
        "specialist": 5,
        "specialized": 5,
    }
    if value.isdigit() and 1 <= int(value) <= 5:
        return int(value)
    if value in labels:
        return labels[value]
    normalized = clean(entry_type).casefold()
    if normalized == "common_word":
        return 1
    if normalized in {"word", "phrase", "idiom", "added"}:
        return 2
    if normalized in {
        "concept",
        "person",
        "place",
        "organization",
        "event",
        "reading",
        "place_or_group",
    }:
        return 3
    if normalized in {"rare_word", "manual", "classical_term", "text"}:
        return 4
    if normalized in {
        "artifact",
        "bronze_item",
        "site_or_culture",
        "person_or_deity",
    }:
        return 5
    return 3


def csv_occurrences(path: Path, root: Path) -> list[Occurrence]:
    name = path.name.lower()
    if not (
        name == "reading_terms.csv"
        or "rare_words" in name
        or name == "my_rare_words.csv"
        or "vocab" in name
        or "vocabulary" in name
    ):
        return []

    rows: list[Occurrence] = []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            term = clean(row.get("term") or row.get("word") or row.get("phrase"))
            if not term:
                continue
            pinyin = clean(row.get("pinyin"))
            entry_type = clean(row.get("type")) or "rare_word"
            rows.append(
                Occurrence(
                    term=term,
                    language=language_for(term, pinyin),
                    pinyin=pinyin,
                    entry_type=entry_type,
                    definition=clean(
                        row.get("annotation")
                        or row.get("definition")
                        or row.get("meaning")
                        or row.get("reader_note")
                    ),
                    example=clean(row.get("example") or row.get("example_sentence")),
                    source=relative(path, root),
                    source_detail=clean(
                        row.get("page")
                        or row.get("page_number")
                        or row.get("pages")
                        or row.get("location")
                        or row.get("source_detail")
                    ),
                    source_target=source_target_for(path, root),
                    source_format="csv",
                    entry_time=entry_time_for(path),
                    difficulty=difficulty_for(
                        entry_type, row.get("difficulty") or row.get("difficulty_level")
                    ),
                )
            )
    return rows


def json_occurrences(path: Path, root: Path) -> list[Occurrence]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return []
    if not isinstance(payload, dict) or not isinstance(payload.get("vocabulary"), list):
        return []

    rows: list[Occurrence] = []
    for item in payload["vocabulary"]:
        if not isinstance(item, dict):
            continue
        term = clean(item.get("term") or item.get("word") or item.get("phrase"))
        if not term:
            continue
        pinyin = clean(item.get("pinyin"))
        entry_type = clean(item.get("type")) or "word"
        rows.append(
            Occurrence(
                term=term,
                language=clean(item.get("language")) or language_for(term, pinyin),
                pinyin=pinyin,
                entry_type=entry_type,
                definition=clean(
                    item.get("definition") or item.get("meaning") or item.get("annotation")
                ),
                example=clean(item.get("example") or item.get("example_sentence")),
                source=relative(path, root),
                source_detail=clean(
                    item.get("page")
                    or item.get("page_number")
                    or item.get("pages")
                    or item.get("location")
                    or item.get("source_detail")
                ),
                source_target=source_target_for(path, root),
                source_format="json",
                entry_time=entry_time_for(path),
                difficulty=difficulty_for(
                    entry_type, item.get("difficulty") or item.get("difficulty_level")
                ),
            )
        )
    return rows


def literal(node: ast.AST | None) -> str:
    if node is None:
        return ""
    try:
        value = ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError):
        return ""
    return clean(value) if isinstance(value, (str, int, float)) else ""


def python_occurrences(path: Path, root: Path) -> list[Occurrence]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return []

    rows: list[Occurrence] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        function_name = ""
        if isinstance(node.func, ast.Name):
            function_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            function_name = node.func.attr
        if function_name != "VocabularyItem":
            continue

        keywords = {item.arg: literal(item.value) for item in node.keywords if item.arg}
        term = keywords.get("term") or (literal(node.args[0]) if node.args else "")
        definition = keywords.get("definition") or (
            literal(node.args[1]) if len(node.args) > 1 else ""
        )
        if not term:
            continue
        pinyin = keywords.get("pinyin", "")
        entry_type = keywords.get("type") or "word"
        rows.append(
            Occurrence(
                term=term,
                language=keywords.get("language") or language_for(term, pinyin),
                pinyin=pinyin,
                entry_type=entry_type,
                definition=definition,
                example=keywords.get("example", ""),
                source=relative(path, root),
                source_detail=(
                    keywords.get("page")
                    or keywords.get("page_number")
                    or keywords.get("location")
                    or keywords.get("source_detail")
                    or ""
                ),
                source_target=source_target_for(path, root),
                source_format="python_ast",
                entry_time=entry_time_for(path),
                difficulty=difficulty_for(
                    entry_type,
                    keywords.get("difficulty") or keywords.get("difficulty_level"),
                ),
            )
        )
    return rows


def discover(root: Path) -> list[Occurrence]:
    rows: list[Occurrence] = []
    for top_level in ("news_reports", "practice"):
        base = root / top_level
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix.lower() == ".csv":
                rows.extend(csv_occurrences(path, root))
            elif path.suffix.lower() == ".json":
                rows.extend(json_occurrences(path, root))
            elif path.suffix.lower() == ".py":
                rows.extend(python_occurrences(path, root))
    return rows


def unique_join(values: list[str], separator: str = " | ") -> str:
    return separator.join(dict.fromkeys(value for value in values if value))


def merge(rows: list[Occurrence]) -> list[dict[str, str | int]]:
    groups: dict[tuple[str, str], list[Occurrence]] = {}
    for row in rows:
        key = (row.language.casefold(), row.term.casefold())
        groups.setdefault(key, []).append(row)

    result: list[dict[str, str | int]] = []
    for (_, _), occurrences in sorted(groups.items()):
        result.append(
            {
                "term": occurrences[0].term,
                "language": occurrences[0].language,
                "pinyin": unique_join([row.pinyin for row in occurrences]),
                "type": unique_join([row.entry_type for row in occurrences]),
                "definition": unique_join([row.definition for row in occurrences]),
                "example": unique_join([row.example for row in occurrences]),
                "occurrence_count": len(occurrences),
                "sources": unique_join([row.source for row in occurrences], "; "),
                "source_details": unique_join(
                    [
                        f"{row.source} · {row.source_detail}"
                        if row.source_detail
                        else row.source
                        for row in occurrences
                    ],
                    "; ",
                ),
                "source_targets": unique_join(
                    [row.source_target for row in occurrences], "; "
                ),
                "entry_time": max(row.entry_time for row in occurrences),
                "difficulty": max(row.difficulty for row in occurrences),
            }
        )
    return result


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build(
    root: Path, output: Path, source_output: Path, web_output: Path | None = None
) -> tuple[int, int]:
    occurrences = discover(root)
    entries = merge(occurrences)
    write_csv(
        output,
        [
            "term",
            "language",
            "pinyin",
            "type",
            "definition",
            "example",
            "occurrence_count",
            "sources",
            "source_details",
            "source_targets",
            "entry_time",
            "difficulty",
        ],
        entries,
    )
    write_csv(
        source_output,
        [
            "term",
            "language",
            "pinyin",
            "entry_type",
            "definition",
            "example",
            "source",
            "source_detail",
            "source_target",
            "source_format",
            "entry_time",
            "difficulty",
        ],
        [row.__dict__ for row in occurrences],
    )
    if web_output is not None:
        web_output.write_text(
            "window.DICTIONARY_ENTRIES = "
            + json.dumps(entries, ensure_ascii=False, separators=(",", ":"))
            + ";\n",
            encoding="utf-8",
        )
    return len(entries), len(occurrences)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--source-output", type=Path, default=SOURCE_OUTPUT)
    parser.add_argument("--web-output", type=Path, default=WEB_OUTPUT)
    args = parser.parse_args()
    entries, occurrences = build(
        args.root, args.output, args.source_output, args.web_output
    )
    print(f"Wrote {entries} dictionary entries from {occurrences} source occurrences.")


if __name__ == "__main__":
    main()
