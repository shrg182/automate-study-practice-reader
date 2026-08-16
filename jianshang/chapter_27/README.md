# Chapter 27: 第二十七章 诸神远去之后

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_27` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manual editor prepared`
- Last updated: `2026-07-28`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `medium`

Short status note:

```text
The ten-page Chapter 27 manual editor is ready. Source images, the page-aligned
TXT seed, activity log, reading table, annotated PDF, shared reference page, and
chapter navigation have been generated. Nine source notes still need their body
markers located during manual review.
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_27_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `20`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_27_shengzibiao.txt`: generated reading-term table.
- `chapter_27_annotated.pdf`: generated annotated PDF.
- `editor.html`: ten-page browser editor for manual source comparison.
- `chapter_27_clean_edited.txt`: page-aligned editor seed and TXT export target.
- `chapter_27_edit_log.txt`: editor activity-log export target.
- `pdf_pages/`: source-page images for physical PDF pages 561–570.

## Source Mapping

- Chapter ID: `chapter_27`
- Title: `第二十七章 诸神远去之后`
- Original reader pages: `563-572`
- Source PDF pages: `561-570`
- Printed pages: `549-558`
- Mapping note: `Derived from scanned table of contents; PDF pages are printed pages plus 12; epilogue starts on PDF page 571.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_27/chapter_27_clean.txt \
  --dictionary chapter_27/reading_terms.csv \
  -o chapter_27/chapter_27_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_27/chapter_27_clean.txt \
  --dictionary chapter_27/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_27/chapter_27_annotated.pdf \
  --title '《翦商》第27章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_27/chapter_27_clean.txt
python3 jianshang_tools.py check-pdf chapter_27/chapter_27_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_27/chapter_27_clean.txt \
  --pdf 翦商.pdf \
  --start-page 561 \
  --end-page 570
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
  - Prepared the ten-page manual editor and extracted all source-page images.
  - Added clearer note labels: `章节导读札记` and `记录到编辑日志`.
  - Added an editable `章节导读札记` block with title/content fields, deletion,
    browser persistence, JSON-backup support, and Markdown download.
  - Generated the page-aligned TXT seed and activity log.
  - Regenerated the reading table, annotated PDF, shared reference page, and
    chapter navigation.
  - Recorded the nine unplaced source-note markers for manual review.
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
The source-note section contains notes 1-9, but no corresponding [[fn:number]]
markers have yet been located in the body.
```

Issue:

```text
[OCR error, missing character, doubtful reading, caption location, source-note mismatch, etc.]
```

Action needed:

- Check the source PDF pages `561-570`.
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

Rows currently present: `0`.

Rows added or updated in this chapter:

- `[source or passage]`: `[brief reason]`

## Reading-Term Dictionary Notes

Important additions to `reading_terms.csv`:

- `[term]`, `[pinyin]`, `[type]`: `[reason]`

Terms requiring special care:

- `[term]`: `[multiple readings, chapter-specific pronunciation, or conflict with bronze_terms.csv]`

Term-cap note:

- Current generation command uses `--min-terms 20`.

## Image and Caption Review

- Captions checked against PDF: `[yes/no]`
- All captions end with `（图）`: `[yes/no]`
- Caption flow check passed: `[yes/no]`
- Captions needing manual PDF comparison:
  - `[caption / page / issue]`

## Footnote Review

- Body markers count: `0`
- Source notes count: `9`
- Footnote sequence gaps: `body markers 1-9 not yet placed`
- Notes without body markers: `notes 1-9`
- Body markers without notes: `none`
- Clustered or merged source-note issues:
  - `[details]`

## Regeneration Log

### 2026-07-01

- Standardized this README using `CHAPTER_README_TEMPLATE.md`.
- Preserved previous README notes below when an earlier README existed.
- Regenerated outputs in this pass: `no`.
- Checks run in this pass: `not run`.
- Notes: use the commands above after future edits.

### 2026-07-28 — Manual editor preparation

- Generated `editor.html`, `chapter_27_clean_edited.txt`, and the initial empty
  `chapter_27_edit_log.txt`.
- Extracted all ten source-page images for physical PDF pages 561–570.
- Renamed the static note panel to `章节导读札记` and the log-only action to
  `记录到编辑日志`.
- Added a working chapter-note entry form. Browser-added notes are displayed
  alongside file-based notes, included in JSON backups, and downloadable as
  `chapter_27_reading_notes.md`; the browser cannot directly overwrite the
  repository’s `reading_notes.md`.
- Regenerated all study outputs and shared navigation.
- Caption-flow and suspicious-OCR checks pass; source notes 1-9 remain for
  body-marker placement during manual review.

## Final Checklist

- [x] `chapter_27_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [x] Image captions end with `（图）` where applicable.
- [x] Caption flow check passes.
- [ ] Footnotes are aligned and checked; notes 1-9 need body markers.
- [x] `reading_terms.csv` exists.
- [x] Chapter-specific pronunciation entries are ready for manual review.
- [ ] `oracle_review.tsv` records unresolved ancient text or inscription issues when needed.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [x] `check-pdf` completed; footnote placement remains open.
- [x] Remaining manual-review items are clearly listed.
