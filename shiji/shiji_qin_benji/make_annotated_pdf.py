#!/usr/bin/env python3
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parents[1] / "liaozhai_stories"))
from liaozhai_tools import annotated_pdf_main

if __name__ == "__main__":
    annotated_pdf_main(BASE_DIR / "qin_benji_clean.txt", BASE_DIR / "reading_terms.csv", BASE_DIR / "qin_benji_annotated.pdf", "《史记·秦本纪》注音阅读版", "https://www.guwendao.net/guwen/bookv_cab5e2fff7da.aspx")
