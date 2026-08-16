# Chapter 24: 第二十四章 西土之人

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_24` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manual edit processed and outputs regenerated`
- Last updated: `2026-07-27`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `medium`

Short status note:

```text
The 07:44 follow-up export and matching edit log have been imported and
promoted. `羑里` and `邘（yú）国` are now resolved, the incorrect pinyin split
in `商人祭祀先王` is absent, and all 24 source-note markers remain aligned.
All outputs have been regenerated.
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_24_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `27`.
- `oracle_review.tsv`: not currently needed after the `羑里` review was resolved.
- `chapter_24_shengzibiao.txt`: generated reading-term table.
- `chapter_24_annotated.pdf`: generated annotated PDF.
- `editor.html`: 30-page manual editor with explicit reader, physical-PDF, printed-page, and annotated-PDF numbering.
- `chapter_24_clean_edited.txt`: page-aligned editor seed and TXT export target.
- `chapter_24_edit_log.txt`: editor activity-log export target.
- `pdf_pages/`: source-page images for physical PDF pages 463–492.

## Source Mapping

- Chapter ID: `chapter_24`
- Title: `第二十四章 西土之人`
- Original reader pages: `465-494`
- Source PDF pages: `463-492`
- Printed pages: `451-480`
- Mapping note: original reader pages are printed pages plus 14; physical source PDF pages are printed pages plus 12.

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_24/chapter_24_clean.txt \
  --dictionary chapter_24/reading_terms.csv \
  -o chapter_24/chapter_24_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 27
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_24/chapter_24_clean.txt \
  --dictionary chapter_24/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_24/chapter_24_annotated.pdf \
  --title '《翦商》第24章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 27
```

This chapter does not currently require `oracle_review.tsv`.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_24/chapter_24_clean.txt
python3 jianshang_tools.py check-pdf chapter_24/chapter_24_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_24/chapter_24_clean.txt \
  --pdf 翦商.pdf \
  --start-page 463 \
  --end-page 492
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
  - Imported the 07:44 follow-up TXT export and matching 26-entry activity log.
  - Resolved `〔待核：羡〕里` as `羑里`.
  - Corrected the ancient state name `邛` to `邘（yú）` throughout the chapter.
  - Confirmed `商人祭祀先王` without the erroneous `rén jì` insertion.
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
The clean text contains 24 aligned source-note markers and no inline 待核
markers.
```

Issue:

```text
The previous place-name uncertainty has been resolved as `羑里`.
```

Action needed:

- Check the source PDF pages `463-492`.
- Check reliable editions, inscription corpora, or oracle-bone references where relevant.
- No further action is required for this item.

Status: `resolved`

## Ancient Text Review Table

Use `oracle_review.tsv` for passages that should appear in the generated
“疑难甲骨文字词校读表”.

Required columns:

```tsv
source	current_text	issue	action
```

Rows currently present: `0`; the file is not needed.

Rows added or updated in this chapter:

- None.

## Reading-Term Dictionary Notes

Important additions to `reading_terms.csv`:

- `髳、咷、麀、翯、箧、槃`: confirmed in the first manual pass.
- `羑里、邘`: confirmed in the follow-up review.

Terms requiring special care:

- `咷`: read `táo` in `号咷`; another reading `tiào` exists.

Term-cap note:

- Current generation command uses `--min-terms 27`.

## Image and Caption Review

- Captions checked against PDF: `yes, during the manual pass`
- All captions end with `（图）`: `no; M44平面图 remains an unmarked source label`
- Caption flow check passed: `yes`
- Captions needing manual PDF comparison:
  - `M44平面图 / PDF 485 / confirm whether to retain as a standalone caption`

## Footnote Review

- Body markers count: `24`
- Source notes count: `24`
- Footnote sequence gaps: `none`
- Notes without body markers: `none`
- Body markers without notes: `none`
- Clustered or merged source-note issues:
  - `[details]`

## Regeneration Log

### 2026-07-27 — Pinyin deduplication

- Removed hard-coded numeric pinyin from `髳、咷、邘、麀、翯、箧、槃`;
  their readings now come exclusively from `reading_terms.csv`.
- Regenerated the reading table, annotated PDF, browser editor, shared
  reference page, and chapter navigation.
- Confirmed `髳` is rendered from the dictionary as `髳（máo）`, without a
  second `（mao2）` annotation.

### 2026-07-27 — Follow-up manual import

- Imported the 07:44 TXT export and matching 26-entry activity log; inspected
  the matching 30-page JSON backup.
- Promoted `羑里`, corrected all four contextual uses of `邛` to `邘`, and
  added `羑里、邘` to `reading_terms.csv`.
- Confirmed the sentence reads `文王曾经记录商人祭祀先王的仪式` with no
  incorrect `rén jì` annotation.
- Regenerated the reading table, annotated PDF, browser editor, shared
  reference page, and chapter navigation.

### 2026-07-27 — Manual import

- Imported the 07:23 TXT export and matching activity log from `~/Downloads`;
  inspected the matching JSON backup and its 30 page records.
- Promoted all 24 source-note placements, two editor notes, repaired captions
  and paragraph flow, and the confirmed readings `髳、咷、麀、翯、箧、槃`.
- Added the unresolved `羡` glyph to `oracle_review.tsv`.
- Regenerated the reading table, annotated PDF, browser editor, shared
  reference page, and chapter navigation.

### 2026-07-26

- Generated `chapter_24_clean_edited.txt`, `chapter_24_edit_log.txt`, and
  `editor.html`.
- Extracted all 30 source-page images for physical PDF pages 463–492.
- Regenerated `reference_tables.html` and `shared/editor_toc.js`.
- Verified page markers, image count, and editor export targets.

### 2026-07-01

- Standardized this README using `CHAPTER_README_TEMPLATE.md`.
- Preserved previous README notes below when an earlier README existed.
- Regenerated outputs in this pass: `no`.
- Checks run in this pass: `not run`.
- Notes: use the commands above after future edits.

## Final Checklist

- [x] `chapter_24_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [ ] Image captions end with `（图）`.
- [x] Caption flow check passes.
- [x] Footnotes are aligned and checked.
- [x] `reading_terms.csv` exists.
- [ ] Chapter-specific pronunciation conflicts are resolved.
- [x] No unresolved passage currently requires `oracle_review.tsv`.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [x] `check-pdf` passes.
- [x] Remaining manual-review items are clearly listed.
