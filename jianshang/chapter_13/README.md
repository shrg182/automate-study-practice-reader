# Chapter 13: 第十三章 大学与王子

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_13` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manual editing complete; outputs regenerated`
- Last updated: `2026-07-22`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `low`

Short status note:

```text
已导入并提升第十三章最终手工校订稿和编辑日志，13条原注已全部对齐，结构检查通过，生字表、注音PDF及编辑器参考表已重新生成。
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_13_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `69`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_13_shengzibiao.txt`: generated reading-term table.
- `chapter_13_annotated.pdf`: generated annotated PDF.
- `editor.html`: 20-page manual editor with three-part page labels.
- `chapter_13_clean_edited.txt`: editor export seed; promote only after manual review.
- `chapter_13_edit_log.txt`: editor history export target.
- `pdf_pages/page-261.jpg` through `page-280.jpg`: physical source-PDF images used by the editor.

## Source Mapping

- Chapter ID: `chapter_13`
- Title: `第十三章 大学与王子`
- PDF viewer pages: `263-282`
- Physical source-PDF pages: `261-280`
- Printed pages: `249-268`
- Mapping note: `The editor renders all three systems: viewer page = printed page + 14; physical source-PDF page = printed page + 12.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_13/chapter_13_clean.txt \
  --dictionary chapter_13/reading_terms.csv \
  -o chapter_13/chapter_13_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_13/chapter_13_clean.txt \
  --dictionary chapter_13/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_13/chapter_13_annotated.pdf \
  --title '《翦商》第13章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_13/chapter_13_clean.txt
python3 jianshang_tools.py check-pdf chapter_13/chapter_13_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_13/chapter_13_clean.txt \
  --pdf 翦商.pdf \
  --start-page 261 \
  --end-page 280
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

- Date: `2026-07-22`
- Editor: `manual + Codex`
- Scope:
  - `Imported the latest TXT export and edit log, promoted the reviewed text, split notes 12-13, normalized pronunciation terms, regenerated all outputs, and ran structural checks.`
- Output regenerated after this pass: `yes`

### User Corrections

- Imported the final manual TXT export and matching edit log from `~/Downloads`.

### Applied Edits

- `有注意〔待核：曾注意〕到` -> `曾注意到`, following the explicit edit-log correction.
- Split the clustered final definition into source notes 12 and 13, matching source page 280.
- Normalized `汭`, `銎`, `鬯`, `跽`, and `禳` into dictionary-backed pinyin.
- Repaired the `《屯南》662（图）` caption and preserved the editor's high-status-sacrifice commentary.

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
No unresolved structural item remains from this editing pass.
```

Issue:

```text
All 13 source notes and captions now pass the automated checks.
```

Action needed:

- Check the source PDF pages `261-280`.
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

- `汭 (ruì)`, `銎 (qióng)`, `鬯 (chàng)`, `跽 (jì)`, `禳 (ráng)`: promoted from inline tone-number notes.

Terms requiring special care:

- `[term]`: `[multiple readings, chapter-specific pronunciation, or conflict with bronze_terms.csv]`

Term-cap note:

- Current generation command uses `--min-terms 20`.

## Image and Caption Review

- Captions checked against PDF: `[yes/no]`
- All captions end with `（图）`: `[yes/no]`
- Caption flow check passed: `yes`
- Captions needing manual PDF comparison:
  - `[caption / page / issue]`

## Footnote Review

- Body markers count: `13`
- Source notes count: `13`
- Footnote sequence gaps: `none`
- Notes without body markers: `none`
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

### 2026-07-22

- Generated the 20-page manual editor and extracted source images `page-261.jpg` through `page-280.jpg`.
- Regenerated the reading table and annotated PDF with three-part page numbering.
- Checks: caption flow OK; suspicious OCR-token check OK; 12 source-note locations pending manual alignment.

### 2026-07-22 — final manual edition

- Imported the 14:33 TXT export and edit log from Downloads.
- Promoted the manual edition, split source notes 12-13 against physical source page 280, and normalized five dictionary-backed pronunciations.
- Regenerated the shengzibiao, annotated PDF, editor, and reference tables.
- Checks: 13/13 source notes aligned; caption flow OK; suspicious OCR-token check OK.

### 2026-07-22 — alignment adjustment

- Imported the 14:43 paragraph-spacing adjustment before the `《屯南》662（图）` caption.
- Regenerated the annotated PDF and editor because the change affects visual layout; the unchanged reading and reference tables were not regenerated.

## Final Checklist

- [x] `chapter_13_clean.txt` reviewed or available for review.
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
- [x] Remaining manual-review items are clearly listed.

## Preserved Previous README Notes

The following section preserves the previous README content so no manual editing
history is lost during standardization.

    # Chapter 13

    Chapter: 第十三章 大学与王子

    Source mapping: PDF pages 261-280 / printed pages 249-268. Chapter 14 starts on PDF page 281.

    Generate study files from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_13 --output chapter_13/source.txt
    python3 jianshang_tools.py table chapter_13/chapter_13_clean.txt --dictionary chapter_13/reading_terms.csv -o chapter_13/chapter_13_shengzibiao.txt --max-terms-percent 0.02 --min-terms 20
    python3 jianshang_tools.py pdf chapter_13/chapter_13_clean.txt --dictionary chapter_13/reading_terms.csv --bronze-dictionary chapter_04/bronze_terms.csv -o chapter_13/chapter_13_annotated.pdf --title '《翦商》第13章注音阅读版' --chapter-map sources/chapter_map.csv
    ```

    Generated files:

    - `chapter_13_clean.txt`: reviewed chapter text.
    - `chapter_13_shengzibiao.txt`: generated reading-term table.
    - `chapter_13_annotated.pdf`: annotated reading-practice PDF.

    ## Manual Editing

    Reviewed for recurring OCR issues: 箭镞/骨镞 terms, 管銎斧, M-number confusion, bronze terms, and interrupted prose around captions.

    2026-06-30 finetuning pass: added missing `（图）` markers, moved one caption out of interrupted prose, split the clustered source notes into separate notes 1-12, and regenerated study outputs with flush-left subtitle styling.
