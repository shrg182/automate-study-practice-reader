#!/usr/bin/env python3
"""Create an annotated PDF for 《聊斋志异·婴宁》."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from liaozhai_tools import annotated_pdf_main


BASE_DIR = Path(__file__).resolve().parent


if __name__ == "__main__":
    annotated_pdf_main(
        default_input=BASE_DIR / "yingning.txt",
        default_dictionary=BASE_DIR / "yingning_rare_words.csv",
        default_output=BASE_DIR / "yingning_annotated.pdf",
        default_title="《婴宁》注音阅读版",
        default_source_url="https://liaozhai.5000yan.com/19984.html",
    )
