#!/usr/bin/env python3
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parents[1] / "liaozhai_stories"))
from liaozhai_tools import rare_word_table_main

if __name__ == "__main__":
    rare_word_table_main(
        BASE_DIR / "shangjun_clean.txt",
        BASE_DIR / "reading_terms.csv",
        BASE_DIR / "shangjun_shengzibiao.txt",
    )
