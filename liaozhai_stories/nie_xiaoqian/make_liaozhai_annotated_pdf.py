#!/usr/bin/env python3
"""Print the finalized 《聂小倩》 editor, including inline images, to PDF."""

from pathlib import Path
import argparse
import base64
import json
import mimetypes
import re
import shutil
import subprocess
import tempfile


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_EDITOR = BASE_DIR / "editor.html"
DEFAULT_OUTPUT = BASE_DIR / "nie_xiaoqian_annotated.pdf"
MEDIA_MANIFEST = BASE_DIR / "nie_xiaoqian_editor_seed.json"

PRINT_CSS = r"""
<style id="pdf-print-overrides">
@page { size: A4; margin: 16mm 18mm 17mm; }
@media print {
  html, body { width: auto; background: #fff !important; }
  body { color: #1f1d19; font-family: "Songti SC", "STSong", serif; }
  .topbar, .toolbar, .sidebar, .inline-media-tools,
  .annotation-register { display: none !important; }
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
  .inline-media figcaption { min-height: 0; }
  .footnotes { break-before: auto; margin-top: 16pt; padding: 8pt 10pt; font-size: 9.5pt; }
  .footnotes h2 { margin-top: 0; }
  #footnoteList { counter-reset: pdf-footnote; }
  .footnote-item { display: block; counter-increment: pdf-footnote; margin: 3pt 0; padding: 4pt 7pt; }
  .footnote-item::before { content: '〔' counter(pdf-footnote) '〕'; float: left; margin-right: 5pt; color: #315b73; font-weight: 700; }
  .footnote-item button { display: none !important; }
  .footnote-media, .footnote-media-actions { display: none !important; }
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
  if (subtitle) subtitle.textContent = '注音、按语、脚注与插图校读版';
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
    raise FileNotFoundError("Google Chrome or Chromium is required to print the editor PDF.")


def embed_inline_images(source: str) -> tuple[str, int]:
    """Attach seed media as data URLs so printing cannot race IndexedDB loading."""
    manifest = json.loads(MEDIA_MANIFEST.read_text(encoding="utf-8"))
    embedded = 0
    for item in manifest.get("media", []):
        media_id = re.escape(item["id"])
        media_path = BASE_DIR / item["path"]
        mime = item.get("type") or mimetypes.guess_type(media_path.name)[0] or "application/octet-stream"
        data_url = f"data:{mime};base64,{base64.b64encode(media_path.read_bytes()).decode('ascii')}"
        pattern = re.compile(rf'(<img\b(?=[^>]*data-media-id="{media_id}")[^>]*)(/?>)')

        def add_source(match: re.Match[str]) -> str:
            nonlocal embedded
            attributes = re.sub(r'\s+src="[^"]*"', "", match.group(1))
            embedded += 1
            return f'{attributes} src="{data_url}"{match.group(2)}'

        source = pattern.sub(add_source, source)
    return source, embedded


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--editor", type=Path, default=DEFAULT_EDITOR)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    source, embedded_count = embed_inline_images(args.editor.read_text(encoding="utf-8"))
    printable = source.replace("</head>", PRINT_CSS + "\n</head>", 1)
    printable = printable.replace("</body>", PRINT_SCRIPT + "\n</body>", 1)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="nie-xiaoqian-pdf-") as temp_dir:
        temp_path = Path(temp_dir)
        printable_path = temp_path / "nie_xiaoqian_print.html"
        profile_path = temp_path / "chrome-profile"
        printable_path.write_text(printable, encoding="utf-8")
        command = [
            chrome_path(),
            "--headless=new",
            "--disable-gpu",
            "--disable-background-networking",
            "--disable-component-update",
            "--disable-default-apps",
            "--disable-sync",
            "--allow-file-access-from-files",
            f"--user-data-dir={profile_path}",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=8000",
            "--print-to-pdf-no-header",
            "--no-pdf-header-footer",
            f"--print-to-pdf={args.output.resolve()}",
            printable_path.as_uri(),
        ]
        try:
            subprocess.run(
                command,
                check=True,
                timeout=30,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.TimeoutExpired:
            if not args.output.exists() or args.output.stat().st_size == 0:
                raise

    print(f"Editor HTML: {args.editor}")
    print(f"Output PDF: {args.output}")
    print(f"Inline images embedded: {embedded_count}")


if __name__ == "__main__":
    main()
