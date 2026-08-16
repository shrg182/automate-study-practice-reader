# 📖 Chapter 01: 苏共"20大"的震动

This folder contains the first OCR pass and review scaffolding for Chapter 1 of
Wu Lengxi's 《十年论战：1956-1966中苏关系回忆录》.

---

## 1️⃣ Unit Status

- Status: `ocr-draft`
- Last updated: `2026-07-04`
- Main processor: `Codex`
- Output regenerated after latest edits: `partial`
- Remaining risk level: `high`

Short status note:

```text
PDF pages 9-41 were rendered at 300 DPI and OCRed with Tesseract
`chi_sim+eng --psm 4`. The raw OCR is preserved, but the chapter is not yet
human-corrected enough for reliable annotated PDF generation.
```

---

## 2️⃣ Files

- `source.txt`: concatenated raw OCR for PDF pages 9-41, with PDF page markers.
- `chapter_01_clean.txt`: lightly punctuation-normalized OCR draft.
- `reading_terms.csv`: seed dictionary of names, organizations, events, and
  concepts for Chapter 1.
- `review_notes.tsv`: human editing queue for damaged OCR passages.
- `chapter_01_shengzibiao.txt`: provisional reading-term table generated from
  the OCR draft; examples still contain OCR errors.
- `editor.html`: static browser editor for correcting OCR while viewing the
  scanned PDF page image.
- `pdf_pages/`: JPEG page images for PDF pages 9-41 used by `editor.html`.

Related source files:

- `../sources/unit_map.csv`: chapter and section page ranges.
- `../sources/ocr_pages/page-009.txt` through `page-041.txt`: page-level raw
  OCR files.
- `../sources/confusing_terms.tsv`: recurring OCR traps for names and terms.

---

## 3️⃣ Source Mapping

- Chapter ID: `chapter_01`
- Title: `苏共“20大”的震动`
- Source PDF pages: `9-41`
- Printed pages: `1-33`
- Previous front matter ends: PDF page `8`
- Next chapter starts: PDF page `42`

Section map:

| Unit                    | Title            | PDF Pages | Printed Pages | Status    |
| ----------------------- | ---------------- | --------: | ------------: | --------- |
| `chapter_01_section_01` | “破题”           |      9-14 |           1-6 | OCR draft |
| `chapter_01_section_02` | 评论赫鲁晓夫报告 |     15-19 |          7-11 | OCR draft |
| `chapter_01_section_03` | 怎样看待斯大林   |     20-27 |         12-19 | OCR draft |
| `chapter_01_section_04` | 探索正确道路     |     28-31 |         20-23 | OCR draft |
| `chapter_01_section_05` | 文章的要点       |     32-37 |         24-29 | OCR draft |
| `chapter_01_section_06` | 必要的说明       |     38-41 |         30-33 | OCR draft |

## Generation Commands Used

Rendered Chapter 1 page images to `/private/tmp/nine_ch1_ocr`:

```bash
pdftoppm -f 9 -l 41 -png -r 300 \
  '吴冷西：十年论战——1956-1966中苏关系回忆录.pdf' \
  /private/tmp/nine_ch1_ocr/page
```

OCR command pattern:

```bash
tesseract /private/tmp/nine_ch1_ocr/page-009.png \
  sources/ocr_pages/page-009 \
  -l chi_sim+eng \
  --psm 4
```

Punctuation normalization:

```bash
python3 ../jianshang/jianshang_tools.py fix-punctuation \
  chapter_01/source.txt \
  -o chapter_01/chapter_01_clean.txt
```

## Quality Checks

Current checks:

- Page count: `33` OCR files for PDF pages `9-41`.
- Editor page: `editor.html` loads `33` editable page panels, `15` review
  notes, and `30` terms.
- Page images: `33` JPEG files in `pdf_pages/`.
- PDF page 42 starts Chapter 2, confirming Chapter 1 ends at PDF page 41.
- OCR quality: high risk; many mixed Latin/CJK fragments remain.
- Annotated PDF generation: deferred until human correction pass.

## Browser Editing

Open `editor.html` in a browser to edit the OCR draft page by page while viewing
the scanned PDF page image. Edits are saved in the browser's local storage and
can be exported or downloaded as `chapter_01_clean_edited.txt`.

Important: browser storage belongs to one browser on one computer. After editing
on another machine, download the TXT export and import it back into the project
files before committing:

```bash
python3 practice/nine_commentaries/import_editor_export.py \
  practice/nine_commentaries/chapter_01 \
  --latest-download
```

This updates both `chapter_01_clean_edited.txt` and the embedded textareas in
`editor.html`, making the edits visible to Git and to other computers after
`git pull`.

## Editing Standards

- Preserve `source.txt` as raw OCR evidence.
- Edit only `chapter_01_clean.txt` during human correction.
- Use `review_notes.tsv` for uncertain lines instead of guessing.
- Check every personal name against the PDF image at least once.
- Remove running headers and printed page numbers from final clean text.
- Keep chapter and section headings flush-left.
- Normalize `苏共“20大”`, `赫鲁晓夫`, `斯大林`, and other recurring terms
  consistently after verification.

## Current Editing Pass

- Date: `2026-07-04`
- Editor: `Codex`
- Scope: OCR generation, source mapping, first review scaffolding.
- Output regenerated after this pass: `partial`

## Pending Manual Review

Priority items:

- Correct the opening paragraphs on PDF pages 9-11.
- Manually transcribe mixed Latin/CJK debris blocks, especially PDF pages 11
  and 37.
- Verify section headings on PDF pages 15, 20, 28, 32, and 38.
- Confirm all central names in `sources/confusing_terms.tsv`.
- Remove page headers and printed page numbers after text correction.

## Review Notes Table

See `review_notes.tsv`.

## Reading-Term Dictionary Notes

The initial `reading_terms.csv` focuses on:

- major people in the chapter;
- party and state organizations;
- article and newspaper titles;
- political concepts that recur in the discussion.

This file should be refined after the human correction pass, because OCR errors
currently hide or distort many term occurrences.

## Regeneration Log

### 2026-07-04

- Created:
  - `source.txt`
  - `chapter_01_clean.txt`
  - `reading_terms.csv`
  - `review_notes.tsv`
  - `README.md`
  - `chapter_01_shengzibiao.txt`
  - `editor.html`
  - `pdf_pages/page-009.jpg` through `page-041.jpg`
- Updated:
  - `../sources/unit_map.csv`
  - `../sources/confusing_terms.tsv`
- OCRed:
  - `../sources/ocr_pages/page-009.txt` through `page-041.txt`
- Generated:
  - provisional `chapter_01_shengzibiao.txt` from the OCR draft
- Checks:
  - Page range: confirmed
  - OCR completeness: 33 page files present
  - Shengzibiao generation: pass, 20 entries found
  - OCR quality: high risk
- Notes:
  - Do not generate final annotated PDF until the clean text has been human
    corrected.

## Final Checklist

- [x] Chapter 1 PDF page range verified.
- [x] Page-level OCR files generated.
- [x] Raw OCR concatenated into `source.txt`.
- [x] First-pass clean draft created.
- [x] `unit_map.csv` seeded.
- [x] `reading_terms.csv` seeded.
- [x] `review_notes.tsv` seeded.
- [x] Provisional shengzibiao generated.
- [x] Browser editing page generated.
- [ ] OCR text human-corrected against PDF images.
- [ ] Page headers and printed page numbers removed from final clean text.
- [ ] Section headings verified.
- [ ] Names and political terms verified.
- [ ] Final shengzibiao regenerated after human correction.
- [ ] Annotated PDF generated.

## Editor

### Editor for Chapter 1 OCR Draft

[`editor.html`](file:///Users/ruixingshi/Python/automate_study_hub3e22/practice/nine_commentaries/chapter_01/editor.html#chapter-01-section-02) 

(file:///Users/macbookpro15/Python/automate_study_hub3e22/practice/nine_commentaries/chapter_01/editor.html#chapter-01-section-02) 



is a static HTML page that loads the OCR draft and scanned PDF images for
Chapter 1. It allows you to edit the OCR text while viewing the corresponding
PDF page image. Edits are saved in the browser's local storage and can be exported
or downloaded as `chapter_01_clean_edited.txt`.
