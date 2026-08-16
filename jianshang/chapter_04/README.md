# Chapter 04: 第四章 异族占领二里头

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_04` of the 《翦商》 study-material project.

## Chapter Status

- Status: `generated`
- Last updated: `2026-07-18`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `medium`

Short status note:

```text
第四章异族占领二里头 has regenerated study outputs and the current shared-component editor. Source notes 6, 13, 15, and 16 still require body-marker review.
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_04_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `47`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_04_shengzibiao.txt`: generated reading-term table.
- `chapter_04_annotated.pdf`: generated annotated PDF.

## Source Mapping

- Chapter ID: `chapter_04`
- Title: `第四章 异族占领二里头`
- Source PDF pages: `87-100`
- Printed pages: `75-88`
- Mapping note: `Verified with rendered PDF pages; page 100 is blank and chapter 5 starts on page 101.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_04/chapter_04_clean.txt \
  --dictionary chapter_04/reading_terms.csv \
  -o chapter_04/chapter_04_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_04/chapter_04_clean.txt \
  --dictionary chapter_04/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_04/chapter_04_annotated.pdf \
  --title '《翦商》第4章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_04/chapter_04_clean.txt
python3 jianshang_tools.py check-pdf chapter_04/chapter_04_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_04/chapter_04_clean.txt \
  --pdf 翦商.pdf \
  --start-page 87 \
  --end-page 100
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

- Date: `2026-07-18`
- Editor: `manual + Codex`
- Scope:
  - Promoted the manual editor export's trailing-space cleanup.
  - Regenerated the reading table, annotated PDF, master reference page, and editor.
  - Rechecked images, captions, OCR-like tokens, and footnote alignment.
- Output regenerated after this pass: `yes`

### User Corrections

- Manual editor pass completed; process Chapter 4 with the current editor version.

### Applied Edits

- Removed trailing spaces following source-footnote markers 1, 2, 4, 7, 9,
  10, 11, 14, 17, and 18; no wording changes were present in the export.
- Removed stray map-OCR lines `东卜冯文化` and `Q 50 ]pkm` from the reading
  text while retaining the complete map caption and source-page image.
- Restored the caption-ending image marker for `夏末商初中原主要考古文化分布图6` as `（图）`.

### Editing Notes

- `[reason for the edit, source reference, uncertainty, or follow-up needed]`

## Confirmed Corrections

Record applied edits here. Keep the old form and the corrected form visible.

### Names and Titles

- `[old form]` -> `[corrected form]`

### Terms and Pronunciation

- `菹` -> `zū`: 水草丛生的沼泽地。
- `汭` -> `ruì`: 河流汇合的地方或河流弯曲的地方。

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

- Body markers verified: `partial`
- Source notes verified: `18 source notes detected`
- Clustered notes split: `none`
- Special handling:
  - Body markers exist for 14 notes; source notes 6, 13, 15, and 16 have no
    corresponding body markers and remain pending manual placement.

## Pending Manual Review

Use this section for unresolved items that need human checking.

### Open Items

Current text:

```text
Source notes 6, 13, 15, and 16
```

Issue:

```text
The notes are present in the source-note section but their body marker locations
have not been established.
```

Action needed:

- Check the source PDF pages `87-100`.
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

- [x] `chapter_04_clean.txt` reviewed or available for review.
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

    # Chapter 4

    Chapter: 第四章 异族占领二里头

    Source mapping: PDF pages 87-100 / printed pages 75-88. PDF page 100 is blank; Chapter 5 starts on PDF page 101.

    ## Source Method

    - The web text is the supporting prose source because it preserves Chinese characters more reliably than raw local OCR.
    - The local PDF is used to verify chapter range, image placement, captions, and footnote markers.
    - `chapter_map.csv` keeps the page mapping shared by all chapter folders.

    Regenerate the web support source:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_04 --output chapter_04/source.txt
    ```

    Run structural checks from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py check-pdf chapter_04/chapter_04_clean.txt --pdf 翦商.pdf --start-page 87 --end-page 100
    python3 jianshang_tools.py ocr-captions --pdf 翦商.pdf --start-page 87 --end-page 100 --clean-text chapter_04/chapter_04_clean.txt
    python3 jianshang_tools.py lint-images chapter_04/chapter_04_clean.txt
    ```

    Current clean text:

    - `chapter_04_clean.txt`: cleaned reading text with PDF-confirmed footnotes and image/caption placement where available.

    Generate study files:

    ```bash
    python3 jianshang_tools.py table chapter_04/chapter_04_clean.txt --dictionary chapter_04/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_04/chapter_04_shengzibiao.txt
    python3 jianshang_tools.py pdf chapter_04/chapter_04_clean.txt --dictionary chapter_04/reading_terms.csv --bronze-dictionary chapter_04/bronze_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_04/chapter_04_annotated.pdf --title '《翦商》第四章注音阅读版' --page-note '第四章约对应 PDF 页 87-100 / 印刷页 75-88'
    ```

    Generated files:

    - `reading_terms.csv`: focused reading-term dictionary for this chapter.
    - `chapter_04_shengzibiao.txt`: generated reading-term table.
    - `chapter_04_annotated.pdf`: annotated reading-practice PDF.

    ## Review Notes

    - `bronze_terms.csv` supplements the reading dictionary with bronze-object names.
    - Bronze-object names in the web text are prone to character-conversion errors. When the PDF is unclear, keep the best reading in `chapter_04_clean.txt` and mark it inline with `〔待核〕` or `〔校疑：...〕`.
