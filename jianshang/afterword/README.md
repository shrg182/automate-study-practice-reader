# 后记

## Status

- Status: `manual review imported; outputs regenerated`
- Last updated: `2026-07-28`
- Viewer pages: `589-593`
- Physical PDF pages: `587-591`
- Printed pages: `575-579`

The book’s 后记 is treated as a chapter-level project unit. It has its own
clean text, reading dictionary, annotated PDF, source images, browser editor,
TXT export seed, activity log, and chapter-level reading notes.

## Generate

Run from `practice/jianshang/`:

```bash
python3 jianshang_tools.py table afterword/afterword_clean.txt \
  --dictionary afterword/reading_terms.csv \
  -o afterword/afterword_shengzibiao.txt \
  --min-terms 15

python3 jianshang_tools.py pdf afterword/afterword_clean.txt \
  --dictionary afterword/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o afterword/afterword_annotated.pdf \
  --title '《翦商》后记注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 15

python3 build_ocr_editor.py --chapter afterword --extract-pages
```

## Review status

- Caption-flow check: passed after final manual review.
- Footnotes: none in the 后记.
- Editor notes: 3 markers and 3 notes, aligned.
- Chapter reading notes: 1.
- The editor includes the editable `章节导读札记` block.
