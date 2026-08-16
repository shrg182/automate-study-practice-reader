#!/usr/bin/env python3
"""Build browser-ready data for the standalone Shiji reference library."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SOURCE = BASE_DIR.parent / "shared_references.csv"
OUTPUT = BASE_DIR / "references_data.js"


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as file:
        entries = list(csv.DictReader(file))
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    OUTPUT.write_text(f"window.SHIJI_REFERENCES = {payload};\n", encoding="utf-8")
    print(f"Source: {SOURCE}\nOutput: {OUTPUT}\nReferences: {len(entries)}")


if __name__ == "__main__":
    main()
