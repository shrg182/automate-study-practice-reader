#!/usr/bin/env python3
"""Print Rongzhai editors to image-preserving annotated PDFs."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


BASE_DIR = Path(__file__).resolve().parent

PRINT_CSS = r"""
<style id="pdf-print-overrides">
@page { size: A4; margin: 16mm 18mm 17mm; }
@media print {
  html, body { width: auto; background: #fff !important; }
  body { color: #1f1d19; font-family: "Songti SC", "STSong", serif; }
  .topbar, .toolbar, .sidebar, .inline-media-tools, .annotation-register { display: none !important; }
  .workspace { display: block !important; max-width: none; padding: 0 !important; }
  .paper { min-height: 0; padding: 0 !important; border: 0 !important; box-shadow: none !important; }
  h1 { margin-top: 0; font-size: 22pt; }
  .subtitle { margin-bottom: 20pt; }
  .editor { font-size: 12pt; line-height: 1.92; }
  .editor p { orphans: 3; widows: 3; }
  .clean-view .inline-media, .inline-media { display: block !important; }
  .clean-view .notation rt, .clean-view .interlinear-note rt { display: ruby-text !important; }
  .clean-view .comment-block, .comment-block { display: block !important; }
  .inline-media { max-width: 150mm !important; margin: 12pt auto 16pt; padding: 7pt; break-inside: avoid; }
  .inline-media[data-size="small"] { max-width: 86mm !important; }
  .inline-media[data-size="large"], .inline-media[data-size="full"] { max-width: 174mm !important; }
  .inline-media img { width: 100%; max-height: 218mm; object-fit: contain; }
  .footnotes { margin-top: 16pt; padding: 8pt 10pt; font-size: 9.5pt; }
  .footnotes.long-footnotes { break-before: page; }
  .footnotes h2 { margin-top: 0; }
  #footnoteList { counter-reset: pdf-footnote; }
  .footnote-item { display: block; counter-increment: pdf-footnote; margin: 3pt 0; padding: 4pt 7pt; break-inside: avoid; }
  .footnote-item::before { content: '〔' counter(pdf-footnote) '〕'; float: left; margin-right: 5pt; color: #315b73; font-weight: 700; }
  .footnote-item button, .footnote-media, .footnote-media-actions { display: none !important; }
  .printable-footnote { line-height: 1.4; white-space: pre-wrap; }
}
</style>
"""

PRINT_SCRIPT = r"""
<script>
window.addEventListener('load', () => {
  document.body.classList.remove('clean-view');
  document.body.classList.add('annotated-view');
  const subtitle = document.querySelector('.paper > .subtitle');
  if (subtitle) subtitle.textContent = '原文、来源注释与人工校读版';
  const footnotes = document.getElementById('footnotes');
  const footnoteItems = document.querySelectorAll('.footnote-item');
  if (footnotes && footnoteItems.length === 0) {
    footnotes.style.display = 'none';
  } else if (footnotes && footnoteItems.length > 12) {
    footnotes.classList.add('long-footnotes');
  }
  document.querySelectorAll('.footnote-item textarea').forEach(area => {
    const note = document.createElement('div');
    note.className = 'printable-footnote';
    note.textContent = area.value;
    area.replaceWith(note);
  });
});
</script>
"""


def chrome_path() -> str:
    candidates = [
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise FileNotFoundError("Google Chrome or Chromium is required")


def embed_initial_media(source: str) -> tuple[str, int]:
    match = re.search(r"const INITIAL_MEDIA=(.*?); const STORAGE_KEY=", source, re.DOTALL)
    if not match:
        return source, 0
    try:
        media = json.loads(match.group(1))
    except json.JSONDecodeError:
        return source, 0
    embedded = 0
    for item in media:
        media_id = re.escape(str(item.get("id", "")))
        data_url = item.get("dataUrl")
        if not media_id or not data_url:
            continue
        pattern = re.compile(rf'(<img\b(?=[^>]*data-media-id="{media_id}")[^>]*)(/?>)')

        def add_source(image_match: re.Match[str]) -> str:
            nonlocal embedded
            attributes = re.sub(r'\s+src="[^"]*"', "", image_match.group(1))
            embedded += 1
            return f'{attributes} src="{data_url}"{image_match.group(2)}'

        source = pattern.sub(add_source, source)
    return source, embedded


def print_one(editor: Path, output: Path) -> None:
    source, image_count = embed_initial_media(editor.read_text(encoding="utf-8"))
    printable = source.replace("</head>", PRINT_CSS + "\n</head>", 1)
    printable = printable.replace("</body>", PRINT_SCRIPT + "\n</body>", 1)
    with tempfile.TemporaryDirectory(prefix="rongzhai-pdf-") as temp_dir:
        temp = Path(temp_dir)
        html_path = temp / "print.html"
        html_path.write_text(printable, encoding="utf-8")
        command = [
            chrome_path(), "--headless=new", "--disable-gpu", "--disable-background-networking",
            "--disable-component-update", "--disable-default-apps", "--disable-sync",
            "--allow-file-access-from-files", f"--user-data-dir={temp / 'profile'}",
            "--run-all-compositor-stages-before-draw", "--virtual-time-budget=8000",
            "--print-to-pdf-no-header", "--no-pdf-header-footer",
            f"--print-to-pdf={output.resolve()}", html_path.as_uri(),
        ]
        try:
            subprocess.run(command, check=True, timeout=30, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            if not output.exists() or output.stat().st_size == 0:
                raise
    print(f"Wrote {output} (embedded images: {image_count})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sequence", type=int, action="append")
    args = parser.parse_args()
    with (BASE_DIR / "catalog.csv").open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    if args.sequence:
        wanted = set(args.sequence)
        rows = [row for row in rows if int(row["sequence"]) in wanted]
    for row in rows:
        target = BASE_DIR / f"volume_{int(row['volume']):02d}" / f"{int(row['sequence']):03d}_{row['slug']}"
        print_one(target / "editor.html", target / f"{row['slug']}_annotated.pdf")


if __name__ == "__main__":
    main()
