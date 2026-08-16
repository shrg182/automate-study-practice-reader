# Chapter 16: 第十六章 成为商朝爪牙：去周原

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_16` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manually reviewed and regenerated`
- Last updated: `2026-07-23`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `low`

Short status note:

```text
第十六章 成为商朝爪牙：去周原 has generated study outputs in this folder. No chapter-specific ancient-text review table is currently present.
```

### 2026-07-23 — Review import and poetry annotation pass

- Imported the 02:15 manual-review export and its complete 29-entry edit log.
- Preserved the revised wording of editor notes 6 and 7 while keeping pronunciation in the chapter dictionary rather than inline numeric pinyin.
- Added selective tone-mark pinyin for uncommon words in the quoted passages from 《绵》 and 《诗经·大雅·皇矣》.
- Made web addresses in generated PDF prose and editor notes clickable; editor-note links 5 and 7 are now PDF URI annotations.

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_16_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `104`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_16_shengzibiao.txt`: generated reading-term table.
- `chapter_16_annotated.pdf`: generated annotated PDF.
- `editor.html`: 16-page manual editor with an explicit source/annotated page-number legend.
- `chapter_16_clean_edited.txt`: editor export seed.
- `chapter_16_edit_log.txt`: editor activity-log export target.

## Source Mapping

- Chapter ID: `chapter_16`
- Title: `第十六章 成为商朝爪牙：去周原`
- Original reader pages: `325-340`
- Physical source PDF pages: `323-338`
- Printed pages: `311-326`
- Annotated PDF pages: `1-13` (independently reflowed; not mapped one-to-one to source pages)
- Mapping note: original reader pages are printed pages plus 14; physical source PDF pages are printed pages plus 12.

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_16/chapter_16_clean.txt \
  --dictionary chapter_16/reading_terms.csv \
  -o chapter_16/chapter_16_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_16/chapter_16_clean.txt \
  --dictionary chapter_16/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_16/chapter_16_annotated.pdf \
  --title '《翦商》第16章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_16/chapter_16_clean.txt
python3 jianshang_tools.py check-pdf chapter_16/chapter_16_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_16/chapter_16_clean.txt \
  --pdf 翦商.pdf \
  --start-page 323 \
  --end-page 338
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

### 2026-07-23 manual review import

- Imported the 01:52 TXT export and recovered its 20-entry activity log from the matching editor backup.
- Restored and aligned all 14 printed source-note markers.
- Applied the user's corrections to 《绵》, 《皇矣》, names, quotations, captions, and source notes.
- Moved numeric inline readings for `蹂躏`, `孔伋`, `閟`, `僇`, and `儇` into `reading_terms.csv`.
- Preserved `陶复陶冗` as the selected Wikisource witness rather than silently normalizing the textual variant.

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

- Check the source PDF pages `323-338`.
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

- [x] `chapter_16_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [ ] Image captions end with `（图）`.
- [x] Caption flow check passes.
- [x] Footnotes are aligned and checked.
- [x] `reading_terms.csv` exists.
- [x] Chapter-specific pronunciation conflicts are resolved.
- [ ] `oracle_review.tsv` records unresolved ancient text or inscription issues when needed.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [x] `check-pdf` passes.
- [ ] Remaining manual-review items are clearly listed.

## Preserved Previous README Notes

The following section preserves the previous README content so no manual editing
history is lost during standardization.

    # Chapter 16

    Chapter: 第十六章 成为商朝爪牙：去周原

    Source mapping: PDF pages 323-338 / printed pages 311-326. Chapter 17 starts on PDF page 339.

    Generate study files from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_16 --output chapter_16/source.txt
    python3 jianshang_tools.py table chapter_16/chapter_16_clean.txt --dictionary chapter_16/reading_terms.csv -o chapter_16/chapter_16_shengzibiao.txt --max-terms-percent 0.02 --min-terms 20
    python3 jianshang_tools.py pdf chapter_16/chapter_16_clean.txt --dictionary chapter_16/reading_terms.csv --bronze-dictionary chapter_04/bronze_terms.csv -o chapter_16/chapter_16_annotated.pdf --title '《翦商》第16章注音阅读版' --chapter-map sources/chapter_map.csv
    ```

    Generated files:

    - `chapter_16_clean.txt`: reviewed chapter text.
    - `chapter_16_shengzibiao.txt`: generated reading-term table.
    - `chapter_16_annotated.pdf`: annotated reading-practice PDF.

    ## Manual Editing

    Reviewed for recurring OCR issues: quoted classical text, river/place names, and inherited dictionary coverage.

    2026-06-30 finetuning pass: reviewed source-note and caption flow checks; regenerated study outputs with flush-left subtitle styling.
