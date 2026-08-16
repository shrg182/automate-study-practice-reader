# Chapter 11: 第十一章 商人的思维与国家

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_11` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manual edits imported, processed, and validated`
- Last updated: `2026-07-21`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `medium-low; unresolved oracle-script glyph placeholders remain for specialist review`

Short status note:

```text
已导入2026-07-21 09:21的TXT导出和09:22的编辑日志，处理手工校订、按语、编者注及词表条目，并重新生成词表、注音PDF和编辑器。10条原注已对齐；图片说明、脚注和可疑OCR检查全部通过。
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_11_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `71`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_11_shengzibiao.txt`: generated reading-term table.
- `chapter_11_annotated.pdf`: generated annotated PDF.
- `editor.html`: 20-page manual editor for PDF viewer pages 223-242.
- `chapter_11_clean_edited.txt`: editor export seed; promote only after manual review.
- `chapter_11_edit_log.txt`: editor history export target.
- `pdf_pages/page-221.jpg` through `page-240.jpg`: physical source-PDF images used by the editor.

## Source Mapping

- Chapter ID: `chapter_11`
- Title: `第十一章 商人的思维与国家`
- PDF viewer pages: `223-242`
- Physical source-PDF pages: `221-240`
- Printed pages: `209-228`
- Mapping note: `Derived from scanned table of contents; PDF pages are printed pages plus 12.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_11/chapter_11_clean.txt \
  --dictionary chapter_11/reading_terms.csv \
  -o chapter_11/chapter_11_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20 \
  --include-source-notes
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_11/chapter_11_clean.txt \
  --dictionary chapter_11/reading_terms.csv \
  -o chapter_11/chapter_11_annotated.pdf \
  --title '《翦商》第11章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_11/chapter_11_clean.txt
python3 jianshang_tools.py check-pdf chapter_11/chapter_11_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_11/chapter_11_clean.txt \
  --pdf 翦商.pdf \
  --start-page 221 \
  --end-page 240
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

- Date: `2026-07-21`
- Editor: `manual + Codex`
- Scope:
  - `Imported the latest TXT export and edit log, promoted the reviewed text, aligned notes 1-10, updated reading terms, regenerated all outputs, and ran structural checks`
- Output regenerated after this pass: `yes`

### User Corrections

- Imported the manually reviewed text, inline commentary, editor's note, and edit log from `~/Downloads`.

### Applied Edits

- Preserved five inline `按语` entries and one `编者注`.
- Normalized tone-number annotations into dictionary-backed pinyin for `戀`, `彐`, `笤帚`, `斫`, and `廪`.
- Corrected `逐兜` -> `逐兕` in the quoted divination text.
- Moved `（图）` to the two inscription captions so caption flow remains structurally valid.
- Aligned all ten source-note definitions with explicit body markers.

### Editing Notes

- Source note 10 cites the same E181 excavation report and page as note 8; it is anchored to the detailed E181 inventory ending with `金花`.
- Unrenderable oracle-script forms remain as explicit `甲骨文` or `异体字，待查` placeholders rather than guessed Unicode characters.

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

- Body markers verified: `yes (1-10)`
- Source notes verified: `yes (1-10)`
- Clustered notes split: `none`
- Special handling:
  - `[example: note 18 was split into notes 18-31]`

## Pending Manual Review

Use this section for unresolved items that need human checking.

### Open Items

Current text:

```text
Several oracle-bone glyphs cannot be represented reliably and remain explicit review placeholders.
```

Issue:

```text
These specialist glyph readings should not be silently inferred from OCR.
```

Action needed:

- Check reliable editions, inscription corpora, or oracle-bone references where relevant.
- Replace a placeholder only when a defensible transcription is available, and record it in `oracle_review.tsv` if needed.

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

- Captions checked against PDF: `baseline structural check only; manual comparison pending`
- All captions end with `（图）`: `baseline check passed`
- Caption flow check passed: `yes`
- Captions needing manual PDF comparison:
  - `[caption / page / issue]`

## Footnote Review

- Body markers count: `0 verified explicit markers`
- Source notes count: `10`
- Footnote sequence gaps: `body locations not yet aligned`
- Notes without body markers: `1-10`
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

### 2026-07-21

- Generated the 20-page manual editor and extracted source images `page-221.jpg` through `page-240.jpg`.
- Regenerated the reading table and annotated PDF with three-part page numbering.
- Checks: caption flow OK; suspicious OCR-token check OK; 10 source-note locations pending manual alignment.

## Final Checklist

- [x] `chapter_11_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [ ] Image captions end with `（图）`.
- [x] Caption flow check passes.
- [ ] Footnotes are aligned and checked.
- [x] `reading_terms.csv` exists.
- [ ] Chapter-specific pronunciation conflicts are resolved.
- [ ] `oracle_review.tsv` records unresolved ancient text or inscription issues when needed.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [ ] `check-pdf` fully passes after manual footnote alignment.
- [x] Remaining manual-review items are clearly listed.

## Preserved Previous README Notes

The following section preserves the previous README content so no manual editing
history is lost during standardization.

    # Chapter 11

    Chapter: 第十一章 商人的思维与国家

    Source mapping: PDF pages 221-240 / printed pages 209-228. Chapter 12 starts on PDF page 241.

    Generate study files from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_11 --output chapter_11/source.txt
    python3 jianshang_tools.py table chapter_11/chapter_11_clean.txt --dictionary chapter_11/reading_terms.csv -o chapter_11/chapter_11_shengzibiao.txt --max-terms-percent 0.02 --min-terms 20
    python3 jianshang_tools.py pdf chapter_11/chapter_11_clean.txt --dictionary chapter_11/reading_terms.csv --bronze-dictionary chapter_04/bronze_terms.csv -o chapter_11/chapter_11_annotated.pdf --title '《翦商》第11章注音阅读版' --chapter-map sources/chapter_map.csv
    ```

    Generated files:

    - `chapter_11_clean.txt`: reviewed chapter text.
    - `chapter_11_shengzibiao.txt`: generated reading-term table.
    - `chapter_11_annotated.pdf`: annotated reading-practice PDF.

    ## Manual Editing

    Reviewed for recurring OCR issues: 曰/日 confusion in quoted text, caption debris, proper names, bronze terms, and interrupted prose around captions.

    2026-06-30 finetuning pass: added missing `（图）` markers to image captions and regenerated study outputs with flush-left subtitle styling.
