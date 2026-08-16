# Chapter 25: 第二十五章 牧野鹰扬

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_25` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manual edit processed and outputs regenerated`
- Last updated: `2026-07-28`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `medium`

Short status note:

```text
The 03:03 editor export and activity log have been imported. The saved source
note for `麈` has been incorporated into its reading-table definition. All 22
source-note markers remain aligned, and all outputs have been regenerated.
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_25_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `33`.
- `oracle_review.tsv`: two unresolved 《商誓解》 placeholder passages.
- `chapter_25_shengzibiao.txt`: generated reading-term table.
- `chapter_25_annotated.pdf`: generated annotated PDF.
- `editor.html`: 28-page manual editor with reader, physical-PDF, printed-page, and annotated-PDF numbering.
- `chapter_25_clean_edited.txt`: page-aligned editor seed and TXT export target.
- `chapter_25_edit_log.txt`: editor activity-log export target.
- `pdf_pages/`: source-page images for physical PDF pages 493–520.

## Source Mapping

- Chapter ID: `chapter_25`
- Title: `第二十五章 牧野鹰扬`
- Original reader pages: `495-522`
- Source PDF pages: `493-520`
- Printed pages: `481-508`
- Mapping note: `Derived from scanned table of contents; PDF pages are printed pages plus 12.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_25/chapter_25_clean.txt \
  --dictionary chapter_25/reading_terms.csv \
  -o chapter_25/chapter_25_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 33
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_25/chapter_25_clean.txt \
  --dictionary chapter_25/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  --ancient-review chapter_25/oracle_review.tsv \
  -o chapter_25/chapter_25_annotated.pdf \
  --title '《翦商》第25章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 33
```

This chapter uses `oracle_review.tsv` for two unresolved 《商誓解》 passages.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_25/chapter_25_clean.txt
python3 jianshang_tools.py check-pdf chapter_25/chapter_25_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_25/chapter_25_clean.txt \
  --pdf 翦商.pdf \
  --start-page 493 \
  --end-page 520
```

Expected clean result:

```text
Footnote marker check: OK
Caption flow check: OK
Suspicious OCR-token check: OK
```

## Editing Standards

- Preserve the source meaning; do not silently guess uncertain ancient text.
- Verify difficult passages against the PDF or reliable editions where possible.
- Use `□` for original unreadable or untranscribed characters.
- Add `（图）` to all image captions and image placeholders.
- Keep subtitles flush-left; do not add paragraph indentation to subtitles.
- Use explicit footnote markers in the body as `[[fn:number]]` only after verifying that the number is a true source note.
- Keep generated PDF footnote display consistent with the project convention.
- Add rare or ambiguous readings to `reading_terms.csv`.
- Add unresolved ancient text, bronze inscriptions, oracle-bone text, and difficult OCR cases to `oracle_review.tsv`.

## Manual Editing

Use this section as the active working notebook for chapter-specific edits. Add
new user corrections here first; after they are applied and verified, summarize
them under `Confirmed Corrections` and record the regeneration under
`Regeneration Log`.

### Current Editing Pass

- Date: `2026-07-28`
- Editor: `manual + Codex`
- Scope:
  - Imported the 02:49 TXT export, matching 46-entry log, and 28-page backup.
  - Promoted OCR, punctuation, paragraph-flow, source-note, and commentary edits.
  - Normalized 15 confirmed readings through `reading_terms.csv`.
  - Verified `麈` against the scan and retained two unresolved placeholder rows.
  - Imported the 03:03 follow-up note and expanded the `麈` definition with its
    《逸周书·世俘解》 hunting-list context.
- Output regenerated after this pass: `yes`

### User Corrections

- `[exact user-provided correction or request]`

### Applied Edits

- `[old form]` -> `[new form]`

### Editing Notes

- `[reason for the edit, source reference, uncertainty, or follow-up needed]`

## Confirmed Corrections

Record applied edits here. Keep the old form and the corrected form visible.

### Names and Titles

- `[old form]` -> `[corrected form]`

### Terms and Pronunciation

- `[old pinyin or OCR form]` -> `[correct form with pinyin if needed]`

### Bronze, Vessel, and Artifact Terms

- `[old form]` -> `[corrected form]`

### Image Captions

- `[caption before edit]` -> `[caption after edit]（图）`

### Classical or Ancient Text

```text
[corrected passage]
```

Notes:

- `[brief explanation, source, or reason for correction]`
- `[whether the passage is also listed in oracle_review.tsv]`

### Footnotes

- Body markers verified: `[yes/no]`
- Source notes verified: `[yes/no]`
- Clustered notes split: `[none / notes X-Y]`
- Special handling:
  - `[example: note 18 was split into notes 18-31]`

## Pending Manual Review

Use this section for unresolved items that need human checking.

### Open Items

Current text:

```text
The clean text contains 22 aligned source-note markers and two unresolved
square-placeholder passages from 《商誓解》.
```

Issue:

```text
The remaining uncertainty is limited to untranscribed or missing text represented
by square placeholders.
```

Action needed:

- Check the source PDF pages `493-520`.
- Check reliable editions, inscription corpora, or oracle-bone references where relevant.
- Decide whether to correct body text or keep the issue in `oracle_review.tsv`.

Status: `deferred`

## Ancient Text Review Table

Use `oracle_review.tsv` for passages that should appear in the generated
“疑难甲骨文字词校读表”.

Required columns:

```tsv
source	current_text	issue	action
```

Rows currently present: `2`.

Rows added or updated in this chapter:

- 《商誓解》 upper passage: four untranscribed characters.
- 《商誓解》 lower passage: a longer missing or untranscribed span.

## Reading-Term Dictionary Notes

Important additions to `reading_terms.csv`:

- `刳、旄、麾、髳、宄、貔、罴、愆、勖、召公奭、氂、麈、俟、慝、嘏`:
  confirmed in the manual pass and normalized into the dictionary.

Terms requiring special care:

- `麈（zhǔ）`: verified against the scanned hunting list; not `塵（chén）`.
- `俟`: read `sì` in `归俟尔命`.

Term-cap note:

- Current generation command uses `--min-terms 33`.

## Image and Caption Review

- Captions checked against PDF: `yes, during the manual pass`
- All captions end with `（图）`: `not applicable; no standalone image caption was retained`
- Caption flow check passed: `yes`
- Captions needing manual PDF comparison:
  - `[caption / page / issue]`

## Footnote Review

- Body markers count: `22`
- Source notes count: `22`
- Footnote sequence gaps: `none`
- Notes without body markers: `none`
- Body markers without notes: `none`
- Clustered or merged source-note issues:
  - `[details]`

## Regeneration Log

### 2026-07-28 — Manual import

- Imported the 03:03 follow-up export and activity log. The text had no
  substantive change; incorporated the saved `麈` definition into
  `reading_terms.csv` and regenerated all outputs.
- Imported the 02:49 TXT export and matching 46-entry activity log from
  `~/Downloads`; inspected the matching JSON backup.
- Aligned all 22 source notes and promoted the manual OCR, punctuation,
  paragraph-flow, and commentary corrections.
- Verified the hunting-list forms `氂、罴、麈`; corrected the dust character
  `塵` to the animal name `麈` against the scan.
- Added 15 confirmed terms to `reading_terms.csv` and removed redundant inline
  tone-number pinyin.
- Added two unresolved 《商誓解》 placeholder passages to `oracle_review.tsv`.
- Regenerated the reading table, annotated PDF, browser editor, shared
  reference page, and chapter navigation.

### 2026-07-27

- Generated `chapter_25_clean_edited.txt`, `chapter_25_edit_log.txt`, and
  `editor.html`.
- Extracted all 28 source-page images for physical PDF pages 493–520.
- Regenerated `reference_tables.html` and `shared/editor_toc.js`.
- Verified page markers, image count, mapping endpoints, and editor export
  targets.

### 2026-07-01

- Standardized this README using `CHAPTER_README_TEMPLATE.md`.
- Preserved previous README notes below when an earlier README existed.
- Regenerated outputs in this pass: `no`.
- Checks run in this pass: `not run`.
- Notes: use the commands above after future edits.

## Final Checklist

- [x] `chapter_25_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [x] No retained standalone image caption requires a `（图）` suffix.
- [x] Caption flow check passes.
- [x] Footnotes are aligned and checked.
- [x] `reading_terms.csv` exists.
- [x] Chapter-specific pronunciation conflicts are resolved.
- [x] `oracle_review.tsv` records unresolved ancient text or inscription issues when needed.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [x] `check-pdf` passes.
- [x] Remaining manual-review items are clearly listed.
