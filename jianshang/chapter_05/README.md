# Chapter 05: 第五章 商族来源之谜

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_05` of the 《翦商》 study-material project.

## Chapter Status

- Status: `generated`
- Last updated: `2026-07-19`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `medium`

Short status note:

```text
第五章商族来源之谜 has incorporated the July 19 manual editor export and regenerated all study outputs. All 14 source notes now have body markers; the reading of `胲` remains explicitly documented as an editorial question.
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_05_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `90`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_05_shengzibiao.txt`: generated reading-term table.
- `chapter_05_annotated.pdf`: generated annotated PDF.
- `editor.html`: browser editor with shared header, shared chapter TOC, source
  page images, annotations, notes, backup, and read-aloud controls.
- `chapter_05_clean_edited.txt`: manual-edition export seeded from the current
  clean text; promote it only after review.

## Source Mapping

- Chapter ID: `chapter_05`
- Title: `第五章 商族来源之谜`
- PDF viewer pages: `103-116`
- Printed pages: `89-102`
- PDF extraction pages: `101-114`
- Mapping note: `Verified against the chapter boundary scan; chapter 6 starts on viewer page 117, printed page 103, extraction page 115.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_05/chapter_05_clean.txt \
  --dictionary chapter_05/reading_terms.csv \
  -o chapter_05/chapter_05_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20 \
  --include-source-notes
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_05/chapter_05_clean.txt \
  --dictionary chapter_05/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_05/chapter_05_annotated.pdf \
  --title '《翦商》第5章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_05/chapter_05_clean.txt
python3 jianshang_tools.py check-pdf chapter_05/chapter_05_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_05/chapter_05_clean.txt \
  --pdf 翦商.pdf \
  --start-page 101 \
  --end-page 114
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

- Date: `2026-07-19`
- Editor: `manual + Codex`
- Scope:
  - Imported four successive 18-page manual TXT exports downloaded on July 19;
    the fourth export at 03:40 is the current edition.
  - Applied OCR, punctuation, ancient-character placeholder, caption, and
    source-note-marker corrections plus one editorial commentary.
  - Normalized numeric pinyin to tone marks and synchronized new rare words.
  - Regenerated the reading table, annotated PDF, editor, and master references.
- Output regenerated after this pass: `yes`

### User Corrections

- Corrected `绘鱼` to `鲶鱼`, `民` to `兕`, `郑国` to `郯国`, and `少嗥氏`
  to `少皞氏` in the affected passages.
- Restored missing punctuation, source note 12, the `玄鸟妇` image marker,
  and several unreadable ancient glyphs as `（甲骨文）` placeholders.
- Added readings for `託`, `兕`, `胲`, `郯`, `少皞`, `帝喾`, and `杼`, plus
  an editorial comment about the reading of `胲`.
- The second editing pass removed inline pronunciation from `託`, `少皞`, and
  `帝喾`; their readings remain available in the chapter/master vocabulary
  tables. Retained numeric readings were normalized back to tone marks.
- Replaced unsupported Japanese middle dots (`・`) in `《山海经·大荒东经》`
  and `《左传·昭公十七年》` with the PDF-safe Chinese middle dot (`·`).
- Extended automatic pinyin annotation to the source-note section so `帝喾`
  receives its dictionary reading there without restoring an inline source edit.
- The latest pass removed the inline explanation after `杼`; its dictionary row
  is now marked `manual` so the focused 20-entry vocabulary table always keeps
  `杼（zhù）：织布机上的梭子；亦为夏代帝王名。`
- The fourth pass restored the inline reading as `杼（zhù）`. PDF vocabulary
  selection now includes terms found in source notes, so 杼 also appears in the
  PDF vocabulary section rather than only in the editor and annotated note text.

### Applied Edits

- `託（tuō；托）` -> `託`
- `少皞（hào）氏` -> `少皞氏`
- `帝喾（kù）` -> `帝喾`

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
- Source notes verified: `14 source notes detected`
- Clustered notes split: `none`
- Special handling:
  - All 14 source notes now have corresponding body markers.

## Pending Manual Review

Use this section for unresolved items that need human checking.

### Open Items

Current text:

```text
The reading of `胲` in “胲作服牛”
```

Issue:

```text
The main text records `hǎi`; the editor's commentary notes a possible reading
as `亥（hài）`. Retain the question unless checked against a reliable edition.
```

Action needed:

- Check the source PDF pages `101-118`.
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

- [x] `chapter_05_clean.txt` reviewed or available for review.
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

    # Chapter 5

    Chapter: 第五章 商族来源之谜

    Source mapping: PDF pages 101-118 / printed pages 89-106. Chapter 6 starts on PDF page 119.

    ## Source Method

    - The web text is the supporting prose source because it preserves Chinese characters more reliably than raw local OCR.
    - The local PDF is used to verify chapter range, image placement, captions, and footnote markers.
    - `chapter_map.csv` keeps the page mapping shared by all chapter folders.

    Regenerate the web support source:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_05 --output chapter_05/source.txt
    ```

    Run structural checks from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py check-pdf chapter_05/chapter_05_clean.txt --pdf 翦商.pdf --start-page 101 --end-page 114
    python3 jianshang_tools.py ocr-captions --pdf 翦商.pdf --start-page 101 --end-page 114 --clean-text chapter_05/chapter_05_clean.txt
    python3 jianshang_tools.py lint-images chapter_05/chapter_05_clean.txt
    ```

    Current clean text:

    - `chapter_05_clean.txt`: cleaned reading text with PDF-confirmed footnotes and image/caption placement where available.

    Generate study files:

    ```bash
    python3 jianshang_tools.py table chapter_05/chapter_05_clean.txt --dictionary chapter_05/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_05/chapter_05_shengzibiao.txt
    python3 jianshang_tools.py pdf chapter_05/chapter_05_clean.txt --dictionary chapter_05/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_05/chapter_05_annotated.pdf --title '《翦商》第五章注音阅读版' --page-note '第五章约对应 PDF 页 101-118 / 印刷页 89-106'
    ```

    Generated files:

    - `reading_terms.csv`: focused reading-term dictionary for this chapter.
    - `chapter_05_shengzibiao.txt`: generated reading-term table.
    - `chapter_05_annotated.pdf`: annotated reading-practice PDF.

    ## Review Notes

    - `editor_review_notes.tsv` records disputed characters, readings, and OCR corrections.
    - Before changing a disputed reading, check `../sources/confusing_terms.tsv`.
