# Chapter 21: 第二十一章 殷都民间的人祭

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_21` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manual edit processed and outputs regenerated`
- Last updated: `2026-07-25`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `low`

Short status note:

```text
The completed 22:02 manual export and 22:04 edit log have been reviewed and
promoted. All 19 source-note markers remain aligned; the new reader notes,
editor note, and 箙 pronunciation confirmation are incorporated, and all
outputs have been regenerated.
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_21_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `25`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_21_shengzibiao.txt`: generated reading-term table.
- `chapter_21_annotated.pdf`: generated annotated PDF.
- `reading_notes.md`: reader-supplied personal notes displayed in the editor reference panel.
- `editor.html`: 22-page manual editor with explicit reader, physical-PDF, printed-page, and annotated-PDF numbering.
- `chapter_21_clean_edited.txt`: page-aligned editor seed and TXT export target.
- `chapter_21_edit_log.txt`: editor activity-log export target.
- `pdf_pages/`: source-page images for physical PDF pages 405–426.

## Source Mapping

- Chapter ID: `chapter_21`
- Title: `第二十一章 殷都民间的人祭`
- Original reader pages: `407-428`
- Physical source PDF pages: `405-426`
- Printed pages: `393-414`
- Annotated PDF pages: `1-15` (independently reflowed; not mapped one-to-one to source pages)
- Mapping note: original reader pages are printed pages plus 14; physical source PDF pages are printed pages plus 12.

Source mapping should match `sources/chapter_map.csv`.

### 2026-07-24 — Manual editor preparation

- Generated all 22 source-page images and the Chapter 21 browser editor.
- Seeded the editor with explicit page boundaries from reader page 407 through 428.
- Enabled header shortcuts for 注音、编者注、按语、待核 and 用户札记, plus the full marker composer in 编辑札记.
- Included synchronized reading and bronze-term tables, the existing reading-notes panel, the user-notes panel, and book-wide reference links.
- Left the 19 source-note placements for manual alignment because the baseline text has note definitions but no verified body markers.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_21/chapter_21_clean.txt \
  --dictionary chapter_21/reading_terms.csv \
  -o chapter_21/chapter_21_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_21/chapter_21_clean.txt \
  --dictionary chapter_21/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_21/chapter_21_annotated.pdf \
  --title '《翦商》第21章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_21/chapter_21_clean.txt
python3 jianshang_tools.py check-pdf chapter_21/chapter_21_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_21/chapter_21_clean.txt \
  --pdf 翦商.pdf \
  --start-page 405 \
  --end-page 426
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

- Date: `2026-07-24`
- Editor: `manual + Codex`
- Scope:
  - Imported the 04:06 TXT export, edit log, and backup.
  - Promoted all 19 verified source-note placements.
  - Reviewed and repaired residual OCR, punctuation, vessel-name, weapon-name,
    river-name, and caption-flow issues against the source pages.
  - Updated the reading-term dictionary and regenerated all outputs.
- Output regenerated after this pass: `yes`

### User Corrections

- Review and process the latest Chapter 21 manual export, then regenerate all outputs.

### Applied Edits

- `渔河 / 河河` -> `洹河`
- `铜殡 / 铜筑 / 铜镁 / 骨镀` -> `铜戣 / 铜镞 / 铜镞 / 骨镞`
- `鼾、蜃、篌、壁、卤、触、解` and related OCR forms -> verified vessel
  names `甗、罍、簋、斝、卣、觚、觯`
- `服 / 籥` -> `箙`
- Aligned body markers `[[fn:1]]` through `[[fn:19]]`.

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

- Body markers verified: `yes`
- Source notes verified: `yes`
- Clustered notes split: `none`
- Special handling:
  - Note 19 was placed after the claim identifying the settlement as a
    jade-working group.

## Pending Manual Review

Use this section for unresolved items that need human checking.

### Open Items

Current text:

```text
[add unresolved text here]
```

Issue:

```text
[OCR error, missing character, doubtful reading, caption location, source-note mismatch, etc.]
```

Action needed:

- Check the source PDF pages `405-426`.
- Check reliable editions, inscription corpora, or oracle-bone references where relevant.
- Decide whether to correct body text or keep the issue in `oracle_review.tsv`.

Status: `resolved`

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

- `戣`, `kuí`, `rare_word`: manually added pronunciation for the ancient
  weapon name; the chapter's `铜戣` is described as a triangular ge.
- `箙`, `fú`, `rare_word`: verified arrow-container term and clan emblem.

Terms requiring special care:

- `[term]`: `[multiple readings, chapter-specific pronunciation, or conflict with bronze_terms.csv]`

Term-cap note:

- Current generation command uses `--min-terms 20`.

## Image and Caption Review

- Captions checked against PDF: `yes`
- All captions end with `（图）`: `yes`
- Caption flow check passed: `yes`
- Captions needing manual PDF comparison:
  - `[caption / page / issue]`

## Footnote Review

- Body markers count: `19`
- Source notes count: `19`
- Footnote sequence gaps: `none`
- Notes without body markers: `none`
- Body markers without notes: `none`
- Clustered or merged source-note issues:
  - `[details]`

## Regeneration Log

### 2026-07-25

- Imported and reviewed the 22:02 TXT export and 22:04 activity log.
- Promoted one editor note, one commentary, and three reader notes.
- Confirmed `箙 / fú` against the manual dictionary note.
- Regenerated the reading table, annotated PDF, chapter editor, shared
  reference page, and chapter navigation.
- Checks passed: footnote markers, caption flow, and suspicious OCR tokens.

### 2026-07-24

- Imported and reviewed the completed 04:06 manual editor export and its
  seven-entry activity log.
- Promoted 19 source-note placements and the manual OCR corrections.
- Added source-verified cleanup for `洹河`, `铜戣`, `铜镞`, `骨镞`, the M269
  vessel list, and `箙`.
- Regenerated `chapter_21_shengzibiao.txt`,
  `chapter_21_annotated.pdf`, `editor.html`, `reference_tables.html`, and
  `shared/editor_toc.js`.
- Checks passed: footnote markers, caption flow, and suspicious OCR tokens.

### 2026-07-24 — 04:18 pronunciation pass

- Reviewed the newer 04:18 export and imported its updated activity log.
- Promoted the new manual pronunciation `戣 (kuí)` into
  `reading_terms.csv`.
- Added `戣 (kuí)` to the shared bronze-item dictionary so it appears in both
  the 阅读词表 and 青铜器词表.
- Did not promote the export wholesale because stale browser autosave content
  reintroduced previously repaired OCR and punctuation errors.
- Regenerated the reading table, annotated PDF, chapter editor, and reference
  tables; all structural checks passed.

### 2026-07-01

- Standardized this README using `CHAPTER_README_TEMPLATE.md`.
- Preserved previous README notes below when an earlier README existed.
- Regenerated outputs in this pass: `no`.
- Checks run in this pass: `not run`.
- Notes: use the commands above after future edits.

## Final Checklist

- [x] `chapter_21_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [x] Image captions end with `（图）`.
- [x] Caption flow check passes.
- [x] Footnotes are aligned and checked.
- [x] `reading_terms.csv` exists.
- [x] Chapter-specific pronunciation conflicts are resolved.
- [ ] `oracle_review.tsv` records unresolved ancient text or inscription issues when needed.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [x] `check-pdf` passes.
- [x] Remaining manual-review items are clearly listed.
