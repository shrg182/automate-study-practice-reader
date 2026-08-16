#!/usr/bin/env python3
"""Download 《聊斋志异·婴宁》 text."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from liaozhai_tools import download_main


if __name__ == "__main__":
    download_main(
        default_url="https://liaozhai.5000yan.com/19984.html",
        default_output=Path(__file__).with_name("yingning.txt"),
    )
