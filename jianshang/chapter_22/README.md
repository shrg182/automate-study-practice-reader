# Chapter 22: 第二十二章 纣王的东南战争

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_22` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manual edit processed and outputs regenerated`
- Last updated: `2026-07-25`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `low`

Short status note:

```text
The completed 22:12 manual export and edit log have been imported. All 14
source-note markers remain aligned, and the six former glyph-review groups
have been resolved as 夙、梅、甾、艅、肜、敄. One damaged oracle-bone
inscription remains in the review table.
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_22_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `21`.
- `oracle_review.tsv`: manual review table for difficult ancient text, oracle-bone text, bronze inscriptions, diagrams, and OCR-resistant passages.
- `chapter_22_shengzibiao.txt`: generated reading-term table.
- `chapter_22_annotated.pdf`: generated annotated PDF.
- `reading_notes.md`: reader-supplied personal notes displayed in the editor reference panel.
- `editor.html`: 14-page manual editor with explicit reader, physical-PDF, printed-page, and annotated-PDF numbering.
- `chapter_22_clean_edited.txt`: page-aligned editor seed and TXT export target.
- `chapter_22_edit_log.txt`: editor activity-log export target.
- `pdf_pages/`: source-page images for physical PDF pages 427–440.

## Source Mapping

- Chapter ID: `chapter_22`
- Title: `第二十二章 纣王的东南战争`
- Original reader pages: `429-442`
- Source PDF pages: `427-440`
- Printed pages: `415-428`
- Annotated PDF pages: independently reflowed; not mapped one-to-one to source pages.
- Mapping note: original reader pages are printed pages plus 14; physical source PDF pages are printed pages plus 12.

Source mapping should match `sources/chapter_map.csv`.

### 2026-07-24 — Manual editor preparation

- Generated all 14 source-page images and the Chapter 22 browser editor.
- Seeded the editor across reader pages 429–442 from `chapter_22_clean.txt`.
- Enabled shortcuts for 注音、编者注、按语、待核 and 用户札记, plus the full marker composer in 编辑札记.
- Included synchronized reading, bronze-term, ancient-review, reading-notes, and user-notes panels.
- Added page-aligned edited-text and activity-log export targets.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_22/chapter_22_clean.txt \
  --dictionary chapter_22/reading_terms.csv \
  -o chapter_22/chapter_22_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 25
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_22/chapter_22_clean.txt \
  --dictionary chapter_22/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  --ancient-review chapter_22/oracle_review.tsv \
  --reading-notes chapter_22/reading_notes.md \
  -o chapter_22/chapter_22_annotated.pdf \
  --title '《翦商》第22章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 25
```

This chapter currently uses `oracle_review.tsv` and renders `reading_notes.md`
as a “读书札记” appendix.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_22/chapter_22_clean.txt
python3 jianshang_tools.py check-pdf chapter_22/chapter_22_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_22/chapter_22_clean.txt \
  --pdf 翦商.pdf \
  --start-page 427 \
  --end-page 440
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

- Date: `YYYY-MM-DD`
- Editor: `[manual / Codex / name]`
- Scope:
  - `[OCR correction, pinyin adjustment, caption repair, footnote alignment, ancient-text review, etc.]`
- Output regenerated after this pass: `yes | no`

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
18 inline 〔待核：…〕 markers retained in `chapter_22_clean_edited.txt` on
reader pages 429 and 431–433; corresponding positions use `□` in
`chapter_22_clean.txt`.
```

Issue:

```text
Six distinct unresolved ancient/bronze glyph shapes. Repeated occurrences have
inconsistent OCR candidates, so they must not be normalized without a reliable
specialist transcription.
```

Action needed:

- Work from the six grouped rows in `oracle_review.tsv`.
- Check physical PDF pages 427 and 429–431 plus the cited 《合集》/《集成》 records.
- Once a glyph is confirmed, replace every occurrence in both clean and edited
  text, then remove the corresponding inline markers and review-table row.

Status: `open`

## Ancient Text Review Table

Use `oracle_review.tsv` for passages that should appear in the generated
“疑难甲骨文字词校读表”.

Required columns:

```tsv
source	current_text	issue	action
```

Rows currently present: `1`.

Rows added or updated in this chapter:

- Six grouped rows cover the 18 editor 待核 markers by glyph shape and page.
- One residual row covers damaged or incomplete oracle-bone text.

## Reading-Term Dictionary Notes

Important additions to `reading_terms.csv`:

- `甗女`, `yǎn nǚ`, `person`: replaces the earlier OCR-derived `羸女`.
- `龋`, `qǔ`, `reading`: promotes the manual numeric reading `qu3` into the dictionary.

Terms requiring special care:

- `[term]`: `[multiple readings, chapter-specific pronunciation, or conflict with bronze_terms.csv]`

Term-cap note:

- Current generation command uses `--min-terms 25` so all newly confirmed
  uncommon readings, including `肜 / róng`, remain in the generated table.

## Image and Caption Review

- Captions checked against PDF: `yes`
- All detected captions end with `（图）`: `yes`
- Caption flow check passed: `yes`
- Captions needing manual PDF comparison:
  - `[caption / page / issue]`

## Footnote Review

- Body markers count: `14`
- Source notes count: `14`
- Footnote sequence gaps: `none`
- Notes without body markers: `none`
- Body markers without notes: `none`
- Clustered or merged source-note issues:
  - `[details]`

## Regeneration Log

### 2026-07-25

- Imported and reviewed the 22:12 TXT export and activity log.
- Promoted the manual identifications `夙`, `梅`, `甾`, `艅`, `肜`, and `敄`
  throughout the clean and page-aligned editions.
- Added the five uncommon readings `夙 / sù`, `甾 / zāi`, `艅 / yú`,
  `肜 / róng`, and `敄 / wù` to `reading_terms.csv`.
- Removed the six resolved glyph groups from `oracle_review.tsv`; retained the
  one damaged-inscription row.
- Regenerated the reading table, annotated PDF, chapter editor, shared
  reference page, and chapter navigation.
- Checks passed: footnote markers, caption flow, and suspicious OCR tokens.

### 2026-07-24

- Imported the matching 16:32 manual TXT export and 23-entry activity log from
  `~/Downloads`; verified that the TXT and JSON backup contained identical text.
- Promoted all 14 source-note placements and the manual OCR, paragraph, and
  caption corrections.
- Moved `龋（qu3）` into `reading_terms.csv` as `龋 / qǔ` and corrected the
  OCR-derived `羸女` term to `甗女 / yǎn nǚ`.
- Preserved 18 inline 待核 markers in the page-aligned editor export, used `□`
  at the corresponding positions in the clean reading text, and grouped the
  notes into six actionable glyph-review rows in `oracle_review.tsv`.
- Regenerated the reading table, annotated PDF, browser editor, shared
  reference page, and chapter navigation.
- Checks passed: punctuation spacing, footnote alignment, caption flow, and
  suspicious OCR tokens.

### 2026-07-01

- Standardized this README using `CHAPTER_README_TEMPLATE.md`.
- Preserved previous README notes below when an earlier README existed.
- Regenerated outputs in this pass: `no`.
- Checks run in this pass: `not run`.
- Notes: use the commands above after future edits.

## Final Checklist

- [x] `chapter_22_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [x] Image captions end with `（图）`.
- [x] Caption flow check passes.
- [x] Footnotes are aligned and checked.
- [x] `reading_terms.csv` exists.
- [x] Chapter-specific pronunciation conflicts are resolved.
- [x] `oracle_review.tsv` records unresolved ancient text or inscription issues when needed.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [x] `check-pdf` passes.
- [x] Remaining manual-review items are clearly listed.
