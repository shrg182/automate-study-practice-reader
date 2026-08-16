# Chapter 23: 第二十三章 姜太公与周方伯

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_23` of the 《翦商》 study-material project.

## Chapter Status

- Status: `second-round manual edit processed and outputs regenerated`
- Last updated: `2026-07-27`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `medium`

Short status note:

```text
The 06:03 second-round manual export and edit log have been imported. Ten rare
readings and confirmed OCR corrections are promoted, all 21 source-note markers
remain aligned, and the ancient-text review table is reduced from 13 rows to
four unresolved glyph groups. All outputs have been regenerated.
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_23_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `34`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_23_shengzibiao.txt`: generated reading-term table.
- `chapter_23_annotated.pdf`: generated annotated PDF.
- `reading_notes.md`: reader-supplied personal notes displayed in the editor reference panel.
- `editor.html`: 22-page manual editor with explicit reader, physical-PDF, printed-page, and annotated-PDF numbering.
- `chapter_23_clean_edited.txt`: page-aligned editor seed and TXT export target.
- `chapter_23_edit_log.txt`: editor activity-log export target.
- `pdf_pages/`: source-page images for physical PDF pages 441–462.

## Source Mapping

- Chapter ID: `chapter_23`
- Title: `第二十三章 姜太公与周方伯`
- Original reader pages: `443-464`
- Source PDF pages: `441-462`
- Printed pages: `429-450`
- Mapping note: original reader pages are printed pages plus 14; physical source PDF pages are printed pages plus 12.

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_23/chapter_23_clean.txt \
  --dictionary chapter_23/reading_terms.csv \
  -o chapter_23/chapter_23_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 34
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_23/chapter_23_clean.txt \
  --dictionary chapter_23/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  --ancient-review chapter_23/oracle_review.tsv \
  --reading-notes chapter_23/reading_notes.md \
  -o chapter_23/chapter_23_annotated.pdf \
  --title '《翦商》第23章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 34
```

This chapter uses `oracle_review.tsv` and renders `reading_notes.md` as a
“读书札记” appendix.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_23/chapter_23_clean.txt
python3 jianshang_tools.py check-pdf chapter_23/chapter_23_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_23/chapter_23_clean.txt \
  --pdf 翦商.pdf \
  --start-page 441 \
  --end-page 462
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

- Date: `2026-07-27`
- Editor: `manual + Codex`
- Scope:
  - Imported the 06:03 TXT export and matching activity log.
  - Promoted ten rare-character readings, several OCR corrections, and four
    linked editor notes.
  - Reduced the ancient-text review table to four unresolved glyph groups.
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
The clean text contains 21 aligned source-note markers and five inline 待核
occurrences belonging to four unresolved glyph groups.
```

Issue:

```text
The remaining uncertainty concerns the normalized forms or readings of four
ancient glyph groups, not source-note placement.
```

Action needed:

- Check the source PDF pages `441-462`.
- Check reliable editions, inscription corpora, or oracle-bone references where relevant.
- Decide whether to correct body text or keep the issue in `oracle_review.tsv`.

Status: `open`

## Ancient Text Review Table

Use `oracle_review.tsv` for passages that should appear in the generated
“疑难甲骨文字词校读表”.

Required columns:

```tsv
source	current_text	issue	action
```

Rows currently present: `4`.

Rows added or updated in this chapter:

- `[source or passage]`: `[brief reason]`

## Reading-Term Dictionary Notes

Important additions to `reading_terms.csv`:

- `[term]`, `[pinyin]`, `[type]`: `[reason]`

Terms requiring special care:

- `[term]`: `[multiple readings, chapter-specific pronunciation, or conflict with bronze_terms.csv]`

Term-cap note:

- Current generation command uses `--min-terms 34` so all manually confirmed
  rare readings present in the chapter remain in the generated table.

## Image and Caption Review

- Captions checked against PDF: `[yes/no]`
- All captions end with `（图）`: `[yes/no]`
- Caption flow check passed: `[yes/no]`
- Captions needing manual PDF comparison:
  - `[caption / page / issue]`

## Footnote Review

- Body markers count: `[number]`
- Source notes count: `[number]`
- Footnote sequence gaps: `[none / details]`
- Notes without body markers: `[none / details]`
- Body markers without notes: `[none / details]`
- Clustered or merged source-note issues:
  - `[details]`

## Regeneration Log

### 2026-07-27 — Second-round manual import

- Imported and verified the 06:03 TXT export and matching 06:03 activity log;
  inspected the matching JSON backup.
- Promoted the manual readings for `氒、膰、菹、脢、戉、鬯、掊、炰烋、奰、枼`
  and added them to `reading_terms.csv`.
- Promoted the `劓` correction, normalized the 《史记·殷本纪》 separator, and
  retained eight numbered editor notes from the manual edition.
- Reduced `oracle_review.tsv` from 13 rows to four unresolved ancient-glyph
  groups: `册口`, the H11.82 上撇下田 glyph, the H11.84 枼-shaped glyph, and
  the 上妻下皿 glyph.
- Regenerated the reading table, annotated PDF, browser editor, shared
  reference page, and chapter navigation.
- Checks passed: 21/21 source-note alignment, caption flow, and suspicious OCR
  tokens.

### 2026-07-26 — First-round manual import

- Imported the matching 16:19 TXT export and activity log.
- Promoted 21 source-note placements, five editor notes, six reader notes, and
  the confirmed OCR and punctuation repairs.
- Corrected the duplicated `[[fn:12]]` callout to `[[fn:21]]`.
- Added `盍 / hé`, `彊 / jiàng`, `谮 / zèn`, `憧憧 / chōng chōng`,
  `矍矍 / jué jué`, and `烝 / zhēng` to `reading_terms.csv`.
- Preserved 29 unresolved inline glyph markers in the editor edition, used
  `□` in the clean edition, and grouped the issues into 13 rows in
  `oracle_review.tsv`.
- Regenerated the reading table, annotated PDF, browser editor, shared
  reference page, and chapter navigation.
- Checks passed: 21/21 source-note alignment, caption flow, and suspicious OCR
  tokens.

### 2026-07-26

- Generated `chapter_23_clean_edited.txt`, `chapter_23_edit_log.txt`, and
  `editor.html`.
- Extracted all 22 source-page images for physical PDF pages 441–462.
- Regenerated `reference_tables.html` and `shared/editor_toc.js`.
- Verified 22 page markers and 22 page images.
- Caption-flow and suspicious-OCR checks passed; source-footnote checking is
  pending manual placement because the body currently has no markers.

### 2026-07-01

- Standardized this README using `CHAPTER_README_TEMPLATE.md`.
- Preserved previous README notes below when an earlier README existed.
- Regenerated outputs in this pass: `no`.
- Checks run in this pass: `not run`.
- Notes: use the commands above after future edits.

## Final Checklist

- [x] `chapter_23_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [ ] Image captions end with `（图）`.
- [x] Caption flow check passes.
- [x] Footnotes are aligned and checked.
- [x] `reading_terms.csv` exists.
- [ ] Chapter-specific pronunciation conflicts are resolved.
- [x] `oracle_review.tsv` records unresolved ancient text or inscription issues when needed.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [x] `check-pdf` passes.
- [x] Remaining manual-review items are clearly listed.
