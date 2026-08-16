#!/usr/bin/env python3
"""Create a rare-word table for 《聊斋志异·劳山道士》."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from liaozhai_tools import rare_word_table_main


BASE_DIR = Path(__file__).resolve().parent


if __name__ == "__main__":
    rare_word_table_main(
        default_input=BASE_DIR / "laoshan_daoshi.txt",
        default_dictionary=BASE_DIR / "laoshan_daoshi_rare_words.csv",
        default_output=BASE_DIR / "laoshan_daoshi_shengzibiao.txt",
    )
