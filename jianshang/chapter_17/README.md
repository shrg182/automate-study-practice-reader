# Chapter 17: 第十七章 周文王地窖里的秘密

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_17` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manually reviewed and regenerated`
- Last updated: `2026-07-23`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `low`

Short status note:

```text
第十七章 周文王地窖里的秘密 has generated study outputs in this folder. No chapter-specific ancient-text review table is currently present.
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_17_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `70`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_17_shengzibiao.txt`: generated reading-term table.
- `chapter_17_annotated.pdf`: generated annotated PDF.
- `editor.html`: 14-page manual editor with explicit reader, physical-PDF, printed-page, and annotated-PDF numbering.
- `chapter_17_clean_edited.txt`: page-aligned editor seed and TXT export target.
- `chapter_17_edit_log.txt`: editor activity-log export target.
- `pdf_pages/`: source-page images for physical PDF pages 339–352.

## Source Mapping

- Chapter ID: `chapter_17`
- Title: `第十七章 周文王地窖里的秘密`
- Original reader pages: `341-354`
- Physical source PDF pages: `339-352`
- Printed pages: `327-340`
- Annotated PDF pages: `1-11` (independently reflowed; not mapped one-to-one to source pages)
- Mapping note: original reader pages are printed pages plus 14; physical source PDF pages are printed pages plus 12.

Source mapping should match `sources/chapter_map.csv`.

### 2026-07-23 — Manual editor preparation

- Generated all 14 source-page images and the Chapter 17 browser editor.
- Seeded the editor with explicit page boundaries from reader page 341 through 354.
- Enabled separate user-note handling for 编者注、按语、待核 and inherited clickable-link support.
- Left the 11 source-note placements for manual alignment because the baseline text has note definitions but no verified body markers.

### 2026-07-23 — Manual review import

- Imported the 11:50 TXT export and its matching 13-entry edit log.
- Aligned all 11 source-note markers and retained one 编者注 and one 按语 as user notes.
- Applied the manual corrections for 缵、召公奭、燮、鬻 and related OCR errors.
- Moved numeric inline readings into `reading_terms.csv` and added six tone-mark dictionary entries.
- Archived the Desktop crops for 缵 and 奭 in `sources/glyph_evidence/chapter_17/`.
- Synchronized the editor reference panels with the generated PDF: both now show the same 12 chapter-reading terms and the single matched bronze term, 彝.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_17/chapter_17_clean.txt \
  --dictionary chapter_17/reading_terms.csv \
  -o chapter_17/chapter_17_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_17/chapter_17_clean.txt \
  --dictionary chapter_17/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_17/chapter_17_annotated.pdf \
  --title '《翦商》第17章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_17/chapter_17_clean.txt
python3 jianshang_tools.py check-pdf chapter_17/chapter_17_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_17/chapter_17_clean.txt \
  --pdf 翦商.pdf \
  --start-page 339 \
  --end-page 352
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
[add unresolved text here]
```

Issue:

```text
[OCR error, missing character, doubtful reading, caption location, source-note mismatch, etc.]
```

Action needed:

- Check the source PDF pages `339-352`.
- Check reliable editions, inscription corpora, or oracle-bone references where relevant.
- Decide whether to correct body text or keep the issue in `oracle_review.tsv`.

Status: `open | resolved | deferred`

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

- Body markers count: `[number]`
- Source notes count: `[number]`
- Footnote sequence gaps: `[none / details]`
- Notes without body markers: `[none / details]`
- Body markers without notes: `[none / details]`
- Clustered or merged source-note issues:
  - `[details]`

## Regeneration Log

### 2026-07-01

- Standardized this README using `CHAPTER_README_TEMPLATE.md`.
- Preserved previous README notes below when an earlier README existed.
- Regenerated outputs in this pass: `no`.
- Checks run in this pass: `not run`.
- Notes: use the commands above after future edits.

## Final Checklist

- [x] `chapter_17_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [ ] Image captions end with `（图）`.
- [ ] Caption flow check passes.
- [ ] Footnotes are aligned and checked.
- [x] `reading_terms.csv` exists.
- [ ] Chapter-specific pronunciation conflicts are resolved.
- [ ] `oracle_review.tsv` records unresolved ancient text or inscription issues when needed.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [ ] `check-pdf` passes.
- [ ] Remaining manual-review items are clearly listed.

## Preserved Previous README Notes

The following section preserves the previous README content so no manual editing
history is lost during standardization.

    # Chapter 17

    Chapter: 第十七章 周文王地窖里的秘密

    Source mapping: PDF pages 339-352 / printed pages 327-340. Chapter 18 starts on PDF page 353.

    Generate study files from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_17 --output chapter_17/source.txt
    python3 jianshang_tools.py table chapter_17/chapter_17_clean.txt --dictionary chapter_17/reading_terms.csv -o chapter_17/chapter_17_shengzibiao.txt --max-terms-percent 0.02 --min-terms 20
    python3 jianshang_tools.py pdf chapter_17/chapter_17_clean.txt --dictionary chapter_17/reading_terms.csv --bronze-dictionary chapter_04/bronze_terms.csv -o chapter_17/chapter_17_annotated.pdf --title '《翦商》第17章注音阅读版' --chapter-map sources/chapter_map.csv
    ```

    Generated files:

    - `chapter_17_clean.txt`: reviewed chapter text.
    - `chapter_17_shengzibiao.txt`: generated reading-term table.
    - `chapter_17_annotated.pdf`: annotated reading-practice PDF.

    ## Manual Editing

    Reviewed for recurring OCR issues: H-number confusion, measurement OCR, 闳夭, quotation punctuation, and caption/legend flow.

    2026-06-30 finetuning pass: added missing `（图）` markers to captions and figure legends, verified source-note sequence, and regenerated study outputs with flush-left subtitle styling.
