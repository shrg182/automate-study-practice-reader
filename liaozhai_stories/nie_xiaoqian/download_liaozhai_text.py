#!/usr/bin/env python3
"""Download only the 原文 paragraphs of 《聊斋志异·聂小倩》."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from liaozhai_tools import download_main  # noqa: E402


if __name__ == "__main__":
    download_main(
        default_url="https://liaozhai.5000yan.com/19985.html",
        default_output=Path(__file__).with_name("nie_xiaoqian.txt"),
    )
