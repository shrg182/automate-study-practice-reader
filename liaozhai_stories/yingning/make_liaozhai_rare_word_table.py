#!/usr/bin/env python3
"""Create a rare-word table for 《聊斋志异·婴宁》."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from liaozhai_tools import rare_word_table_main


BASE_DIR = Path(__file__).resolve().parent


if __name__ == "__main__":
    rare_word_table_main(
        default_input=BASE_DIR / "yingning.txt",
        default_dictionary=BASE_DIR / "yingning_rare_words.csv",
        default_output=BASE_DIR / "yingning_shengzibiao.txt",
    )
