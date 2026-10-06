#!/usr/bin/env python3
"""Import user-downloaded memoir pages into the local reader-editor bundle."""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / "book_content.js"

def decode_page(raw: bytes) -> str:
    head = raw[:8192].decode("latin-1", errors="ignore")
    match = re.search(r"charset\s*=\s*[\"']?\s*([\w.-]+)", head, re.I)
    encodings = ([match.group(1)] if match else []) + ["utf-8-sig", "gb18030"]
    for encoding in encodings:
        try: return raw.decode(encoding)
        except (LookupError, UnicodeDecodeError): pass
    raise UnicodeError("Could not determine source page encoding")

def extract_content(raw: bytes, source_url: str) -> str:
    soup = BeautifulSoup(decode_page(raw), "html.parser")
    if soup.body is None: raise ValueError("Downloaded page has no body")
    children = list(soup.body.children)
    dividers = [i for i, child in enumerate(children) if getattr(child, "name", None) == "hr"]
    if len(dividers) >= 2: children = children[dividers[0] + 1:dividers[-1]]
    fragment = BeautifulSoup("<article></article>", "html.parser").article
    for child in children: fragment.append(child)
    for node in fragment.select("script,style,link,meta,base,noscript,iframe,object,embed,form"): node.decompose()
    for node in fragment.find_all(True):
        for attribute in list(node.attrs):
            if attribute.lower().startswith("on"): del node.attrs[attribute]
        if node.name == "a" and node.get("href"):
            node["href"], node["target"], node["rel"] = urljoin(source_url, node["href"]), "_blank", "noreferrer"
        if node.name == "img" and node.get("src"): node["src"] = urljoin(source_url, node["src"])
    return fragment.decode_contents().strip()

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("download_folder", type=Path)
    folder = parser.parse_args().download_folder.expanduser().resolve()
    with (folder / "download_manifest.csv").open(encoding="utf-8-sig", newline="") as stream: rows = list(csv.DictReader(stream))
    bundle = {}
    for row in rows:
        page = folder / row["file"]
        if not page.is_file(): raise FileNotFoundError(page)
        path = row["source_url"].rsplit("/", 1)[-1]
        section = "第五部分 继续革命" if path.startswith("5-") or path == "6.htm" else row["section"]
        bundle[path] = {"title":row["title"], "section":section, "sourceUrl":row["source_url"], "html":extract_content(page.read_bytes(), row["source_url"])}
    if len(bundle) != 62: raise ValueError(f"Expected 62 pages, found {len(bundle)}")
    OUTPUT.write_text("window.QIBENYU_BOOK_CONTENT = " + json.dumps(bundle, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print(f"Imported {len(bundle)} pages into {OUTPUT}")
    return 0

if __name__ == "__main__": raise SystemExit(main())
