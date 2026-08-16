#!/usr/bin/env python3
"""Print the finalized 《劳山道士》 editor, including inline images, to PDF."""

from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parent
PDF_TOOLS_DIR = BASE_DIR.parents[1] / "rongzhai_suibi"
sys.path.insert(0, str(PDF_TOOLS_DIR))

from make_pdfs import print_one  # noqa: E402


if __name__ == "__main__":
    print_one(BASE_DIR / "editor.html", BASE_DIR / "laoshan_daoshi_annotated.pdf")
