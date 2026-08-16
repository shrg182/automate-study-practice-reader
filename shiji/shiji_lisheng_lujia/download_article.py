#!/usr/bin/env python3
"""Download the original text of 《史记·郦生陆贾列传》 from Guwendao."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

import requests
from bs4 import BeautifulSoup

DEFAULT_URL = "https://www.guwendao.net/guwen/bookv_2cd08cb40d37.aspx"
BASE_DIR = Path(__file__).resolve().parent


def download(url: str, timeout: int = 30) -> str:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (personal study-material downloader)", "Accept-Language": "zh-CN,zh;q=0.9"}, timeout=timeout)
    response.raise_for_status()
    response.encoding = response.apparent_encoding or "utf-8"
    return response.text


def extract(page_html: str) -> tuple[str, str]:
    soup = BeautifulSoup(page_html, "html.parser")
    container = soup.select_one("div.contson[id^=contson]")
    heading = soup.select_one("div[id^=zhengwen] h1")
    if container is None or heading is None:
        raise RuntimeError("Expected article container not found; the page layout may have changed.")
    paragraphs = []
    for paragraph in container.find_all("p", recursive=False):
        text = re.sub(r"[ \t\u3000]+", "", paragraph.get_text("", strip=True))
        if text:
            paragraphs.append(text)
    if not paragraphs:
        raise RuntimeError("Article container found, but it contained no paragraphs.")
    return heading.get_text(" ", strip=True), "\n\n".join(paragraphs).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Download and extract a Guwendao classical-Chinese article.")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--source", type=Path, default=BASE_DIR / "source.txt")
    parser.add_argument("--clean", type=Path, default=BASE_DIR / "lisheng_lujia_clean.txt")
    parser.add_argument("--raw-html", type=Path, default=BASE_DIR / "sources" / "page.html")
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()
    page_html = download(args.url, args.timeout)
    title, text = extract(page_html)
    args.raw_html.parent.mkdir(parents=True, exist_ok=True)
    args.source.parent.mkdir(parents=True, exist_ok=True)
    args.raw_html.write_text(page_html, encoding="utf-8")
    args.source.write_text(text, encoding="utf-8")
    if args.clean.resolve() != args.source.resolve():
        shutil.copyfile(args.source, args.clean)
    print(f"Title: {title}")
    print(f"Paragraphs: {text.count(chr(10) + chr(10)) + 1}")
    print(f"Characters (including whitespace): {len(text)}")
    print(f"Saved source: {args.source}")
    print(f"Saved editable clean copy: {args.clean}")


if __name__ == "__main__":
    main()
