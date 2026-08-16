# Chapter 12: 第十二章 王后的社交圈

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_12` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manual editing complete; outputs regenerated`
- Last updated: `2026-07-22`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `low`

Short status note:

```text
已导入并提升第十二章最终手工校订稿和编辑日志，20条原注已全部对齐，结构检查通过，生字表和注音PDF已重新生成。两条疑难甲骨文字词仍保留在人工复核表中。
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_12_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `68`.
- `oracle_review.tsv`: manual review table for difficult ancient text, oracle-bone text, bronze inscriptions, diagrams, and OCR-resistant passages.
- `chapter_12_shengzibiao.txt`: generated reading-term table.
- `chapter_12_annotated.pdf`: generated annotated PDF.
- `editor.html`: 20-page manual editor with three-part page labels.
- `chapter_12_clean_edited.txt`: editor export seed; promote only after manual review.
- `chapter_12_edit_log.txt`: editor history export target.
- `pdf_pages/page-241.jpg` through `page-260.jpg`: physical source-PDF images used by the editor.

## Source Mapping

- Chapter ID: `chapter_12`
- Title: `第十二章 王后的社交圈`
- PDF viewer pages: `243-262`
- Physical source-PDF pages: `241-260`
- Printed pages: `229-248`
- Mapping note: `The editor renders all three systems: viewer page = printed page + 14; physical source-PDF page = printed page + 12.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_12/chapter_12_clean.txt \
  --dictionary chapter_12/reading_terms.csv \
  -o chapter_12/chapter_12_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20 \
  --include-source-notes
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_12/chapter_12_clean.txt \
  --dictionary chapter_12/reading_terms.csv \
  --ancient-review chapter_12/oracle_review.tsv \
  -o chapter_12/chapter_12_annotated.pdf \
  --title '《翦商》第12章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

This chapter currently uses `oracle_review.tsv`.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_12/chapter_12_clean.txt
python3 jianshang_tools.py check-pdf chapter_12/chapter_12_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_12/chapter_12_clean.txt \
  --pdf 翦商.pdf \
  --start-page 241 \
  --end-page 260
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
  - `Imported the latest TXT export and edit log, promoted the reviewed text, repaired note numbering and caption flow, updated reading terms, regenerated all outputs, and ran structural checks.`
- Output regenerated after this pass: `yes`

### User Corrections

- Imported the final manual TXT export and edit log from `~/Downloads`.

### Applied Edits

- Restored source-note definitions 18-20 from source page 260 and aligned all 20 body markers.
- Preserved the editor's inline commentary and one editor note.
- Moved pinyin for `谧`, `絜`, and `禦` into `reading_terms.csv`; added `妌`.
- Moved `（图）` from two inscription transcriptions to their caption lines.

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
Two difficult oracle-bone/ancient-text readings remain explicitly unresolved in `oracle_review.tsv`.
```

Issue:

```text
The manual edition is complete and all source notes are aligned; only the two documented specialist-review rows remain open.
```

Action needed:

- Consult original plates or specialist references for the two unresolved ancient-text rows.
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

Rows currently present: `2`.

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

- Body markers count: `20`
- Source notes count: `20`
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

- Imported the 12:14 final TXT export and the 12:12 edit log from Downloads.
- Promoted the manual edition, restored the source-note 18-20 split from source page 260, and normalized dictionary-backed pinyin.
- Regenerated the shengzibiao and annotated PDF.
- Checks: 20/20 source notes aligned; caption flow OK; suspicious OCR-token check OK.

## Final Checklist

- [x] `chapter_12_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [ ] Image captions end with `（图）`.
- [x] Caption flow check passes.
- [x] Footnotes are aligned and checked.
- [x] `reading_terms.csv` exists.
- [x] Chapter-specific pronunciation conflicts are resolved.
- [x] `oracle_review.tsv` records unresolved ancient text or inscription issues when needed.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [x] `check-pdf` passes.
- [x] Remaining manual-review items are clearly listed.

## Preserved Previous README Notes

The following section preserves the previous README content so no manual editing
history is lost during standardization.

    # Chapter 12

    Chapter: 第十二章 王后的社交圈

    Source mapping: PDF pages 241-260 / printed pages 229-248. Chapter 13 starts on PDF page 261.

    Generate study files from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_12 --output chapter_12/source.txt
    python3 jianshang_tools.py table chapter_12/chapter_12_clean.txt --dictionary chapter_12/reading_terms.csv -o chapter_12/chapter_12_shengzibiao.txt --max-terms-percent 0.02 --min-terms 20
    python3 jianshang_tools.py pdf chapter_12/chapter_12_clean.txt --dictionary chapter_12/reading_terms.csv --bronze-dictionary chapter_04/bronze_terms.csv --ancient-review chapter_12/oracle_review.tsv -o chapter_12/chapter_12_annotated.pdf --title '《翦商》第12章注音阅读版' --chapter-map sources/chapter_map.csv
    ```

    Generated files:

    - `chapter_12_clean.txt`: reviewed chapter text.
    - `chapter_12_shengzibiao.txt`: generated reading-term table.
    - `oracle_review.tsv`: ancient/oracle text rows that need manual review.
    - `chapter_12_annotated.pdf`: annotated reading-practice PDF.

    ## Manual Editing

    Reviewed for recurring OCR issues: 洹河 terms, jaw-bone terms, bronze vessel names, and quoted oracle-bone wording.

    2026-06-30 finetuning pass: added missing `（图）` markers, split the clustered source notes after note 6 into separate notes 7-18, restored OCR-lost body note markers, and regenerated study outputs with flush-left subtitle styling.


    ### Oracle-bone text OCR issues
    贞：惠妇好呼燎（禀）伐。（图）
    The OCR is still not correct. But it is hard to search the corresponding text online for the oracle characters and text.

    It might be better to make a table beneath the table of bronze items, that list those hard to OCR ancient oracle characters and text.

    2026-07-01 oracle-text review: added `oracle_review.tsv` and updated the PDF command with `--ancient-review`. The uncertain `《合集》2631` transcription is now marked `待核` in the body and listed in the new “疑难甲骨文字词校读表” after the bronze-item table. Manual editing is necessary before assigning a final reading to this line.
