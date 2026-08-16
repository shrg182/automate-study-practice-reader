# 📑 Front Matter: 封面、版权页、目录

This folder contains the working files for the material before Chapter 1 of
Wu Lengxi's 《十年论战：1956-1966中苏关系回忆录》.

---

## 1️⃣ Unit Status

- Status: `processed-draft`
- Last updated: `2026-07-04`
- Main processor: `Codex`
- Output regenerated after latest edits: `no`
- Remaining risk level: `medium`

Short status note:

```text
PDF pages 1-8 have been OCRed and summarized. The copyright-page bibliographic
fields were manually corrected from the page image. The TOC itself is processed
in `../sources/table_of_contents.csv`.
```

---

## 2️⃣ Files

- `source.txt`: raw OCR for PDF pages 1-8, with PDF page markers.
- `front_matter_clean.txt`: cleaned bibliographic/front-matter summary.
- `reading_terms.csv`: seed terms for front-matter metadata.
- `review_notes.tsv`: review notes for damaged OCR and non-book artifacts.
- `front_matter_shengzibiao.txt`: provisional metadata term table.

Related source files:

- `../sources/ocr_pages/page-001.txt` through `page-008.txt`: page-level OCR.
- `../sources/table_of_contents.csv`: processed table of contents.
---

## 3️⃣`../sources/unit_map.csv`: working extraction map.

## Source Mapping

- Unit ID: `front_matter`
- Title: `封面、版权页、目录`
- Source PDF pages: `1-8`
- Printed pages: none
- Next unit starts: Chapter 1 on PDF page `9`, printed page `1`

Sub-units:

| Unit             | Title  | PDF Pages | Status           |
| ---------------- | ------ | --------: | ---------------- |
| `front_cover`    | 封面   |         1 | processed draft  |
| `copyright_page` | 版权页 |         2 | processed draft  |
| `toc`            | 目录   |       3-8 | processed in CSV |

## Generation Commands Used

Rendered page images:

```bash
pdftoppm -f 1 -l 8 -png -r 300 \
  '吴冷西：十年论战——1956-1966中苏关系回忆录.pdf' \
  /private/tmp/nine_front_ocr/page
```

OCR command pattern:

```bash
tesseract /private/tmp/nine_front_ocr/page-001.png \
  sources/ocr_pages/page-001 \
  -l chi_sim+eng \
  --psm 4
```

## Quality Checks

- Page-level OCR files present for PDF pages `1-8`.
- Copyright-page fields manually corrected from PDF page 2.
- TOC source split:
  - chapter titles: programthink Google Doc entry;
  - section titles and page starts: scanned PDF TOC;
  - structured output: `../sources/table_of_contents.csv`.

## Editing Standards

- Do not include library barcode/stamp noise from the cover in reading text.
- Preserve bibliographic metadata in a compact, human-readable form.
- Treat scanned TOC OCR as unreliable; use the structured CSV instead.
- If exact publisher/copyright fields matter later, re-check PDF page 2
  visually before citing.

## Regeneration Log

### 2026-07-04

- Created:
  - `source.txt`
  - `front_matter_clean.txt`
  - `reading_terms.csv`
  - `review_notes.tsv`
  - `front_matter_shengzibiao.txt`
  - `README.md`
- OCRed:
  - `../sources/ocr_pages/page-001.txt` through `page-008.txt`
- Notes:
  - This unit is bibliographic/front-matter support, not a main reading
    chapter.

## Final Checklist

- [x] Front-matter PDF page range verified.
- [x] Page-level OCR generated.
- [x] Raw OCR concatenated into `source.txt`.
- [x] Clean bibliographic summary created.
- [x] TOC linked to structured CSV.
- [x] Provisional shengzibiao generated.
- [ ] Optional final visual proofread of copyright fields.
