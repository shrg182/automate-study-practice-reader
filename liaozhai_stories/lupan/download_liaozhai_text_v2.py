#!/usr/bin/env python3
"""Compatibility wrapper for the generalized Liaozhai downloader."""

from download_liaozhai_text import download_main, Path


if __name__ == "__main__":
    download_main(
        default_url="https://liaozhai.5000yan.com/19983.html",
        default_output=Path(__file__).with_name("lupan.txt"),
    )
