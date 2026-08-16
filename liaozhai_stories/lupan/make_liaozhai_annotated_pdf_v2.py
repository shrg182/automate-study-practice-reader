#!/usr/bin/env python3
"""Compatibility wrapper for the generalized annotated PDF builder."""

from make_liaozhai_annotated_pdf import annotated_pdf_main, BASE_DIR


if __name__ == "__main__":
    annotated_pdf_main(
        default_input=BASE_DIR / "lupan.txt",
        default_dictionary=BASE_DIR / "my_rare_words.csv",
        default_output=BASE_DIR / "lupan_annotated.pdf",
        default_title="《陆判》注音阅读版",
        default_source_url="https://liaozhai.5000yan.com/19983.html",
    )
