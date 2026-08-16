# Chapter 08: 第八章 武德沦丧南土：盘龙城

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_08` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manually edited and processed`
- Last updated: `2026-07-20`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `low; one inline historical claim remains marked 待核`

Short status note:

```text
第八章《武德沦丧南土：盘龙城》的手工校订稿已从 Downloads 导入并推广。两条按语已保留，张煜珧姓名已与原书扫描页核对并加入读音词典。正文10处脚注与10条原注对齐，生字表、注音 PDF 和 HTML 编辑器已重新生成。
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_08_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `64`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_08_shengzibiao.txt`: generated reading-term table.
- `chapter_08_annotated.pdf`: generated annotated PDF.
- `editor.html`: 16-page manual editor for PDF viewer pages 159-174.
- `chapter_08_clean_edited.txt`: editor export seed; promote only after manual review.
- `chapter_08_edit_log.txt`: editor history export target.
- `pdf_pages/page-157.jpg` through `page-172.jpg`: source-page images used by the editor.

## Source Mapping

- Chapter ID: `chapter_08`
- Title: `第八章 武德沦丧南土：盘龙城`
- PDF viewer pages: `159-174`
- Printed pages: `145-160`
- PDF extraction pages: `157-172`
- Mapping note: `Verified with OCR/rendered PDF pages; chapter 9 starts on viewer page 175.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_08/chapter_08_clean.txt \
  --dictionary chapter_08/reading_terms.csv \
  -o chapter_08/chapter_08_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_08/chapter_08_clean.txt \
  --dictionary chapter_08/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_08/chapter_08_annotated.pdf \
  --title '《翦商》第8章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_08/chapter_08_clean.txt
python3 jianshang_tools.py check-pdf chapter_08/chapter_08_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_08/chapter_08_clean.txt \
  --pdf 翦商.pdf \
  --start-page 157 \
  --end-page 172
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

- Date: `2026-07-20`
- Editor: `Codex`
- Scope:
  - `imported the 17:25 manual TXT export and edit log; promoted inline commentary, source-note joins, and the corrected name 张煜珧; regenerated all outputs`
- Output regenerated after this pass: `yes`

### User Corrections

- `I’ve finished manually editing Chapter 8. Please check the files in ~/Downloads, process the updates, and regenerate the outputs.`

### Applied Edits

- `张煜跳` / `张煜珠` -> `张煜珧` (verified against extraction page 172)
- Rejoined source notes 2, 5, and 8 where editor page boundaries had split their lines.
- Added two inline `按语` comments from the manual export.

### Editing Notes

- The comment about Shang and Zhou sacrificial practices remains explicitly marked `（待核）` and is not treated as a verified historical correction.

## Confirmed Corrections

Record applied edits here. Keep the old form and the corrected form visible.

### Names and Titles

- `张煜跳` / `张煜珠` -> `张煜珧`

### Terms and Pronunciation

- `张煜珧（yu4yao2）` -> dictionary entry `张煜珧`, `zhāng yù yáo`

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

- Body markers verified: `yes (10)`
- Source notes verified: `yes (10)`
- Clustered notes split: `none`
- Special handling:
  - `[example: note 18 was split into notes 18-31]`

## Pending Manual Review

Use this section for unresolved items that need human checking.

### Open Items

Current text:

```text
〔按语：人祭，人殉。商纣王废除人祭，周仍保留人殉。（待核）〕
```

Issue:

```text
The historical claim was added as personal commentary and intentionally marked for later verification.
```

Action needed:

- Check the source PDF pages `157-172`.
- Check reliable editions, inscription corpora, or oracle-bone references where relevant.
- Decide whether to correct body text or keep the issue in `oracle_review.tsv`.

Status: `deferred`

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

- `张煜珧`, `zhāng yù yáo`, `person`: verified author name and pronunciation.

Terms requiring special care:

- `[term]`: `[multiple readings, chapter-specific pronunciation, or conflict with bronze_terms.csv]`

Term-cap note:

- Current generation command uses `--min-terms 20`.

## Image and Caption Review

- Captions checked against PDF: `yes`
- All current captions end with `（图）`: `yes`
- Caption flow check passed: `yes`
- Captions needing manual PDF comparison:
  - `[caption / page / issue]`

## Footnote Review

- Body markers count: `10`
- Source notes count: `10`
- Footnote sequence gaps: `none`
- Notes without body markers: `none`
- Body markers without notes: `none`
- Clustered or merged source-note issues:
  - `none detected`

## Regeneration Log

### 2026-07-20

- Imported the 17:25 manual TXT export and edit log, and inspected the matching JSON backup.
- Preserved two inline `按语` comments and rejoined source notes split across editor pages.
- Verified `张煜珧` against extraction page 172 and added its reading to the chapter dictionary.
- Regenerated the annotated PDF with 68 annotations and 9 bronze terms; structural checks passed.
- Generated the 16-page manual editing workspace for viewer pages 159-174.
- Rendered source-page JPEGs for extraction pages 157-172.
- Regenerated the 20-entry focused vocabulary table and annotated PDF with 67 annotations and 9 bronze terms.
- Verified 10 body markers against 10 source notes; caption flow and suspicious OCR checks passed.

### 2026-07-01

- Standardized this README using `CHAPTER_README_TEMPLATE.md`.
- Preserved previous README notes below when an earlier README existed.
- Regenerated outputs in this pass: `no`.
- Checks run in this pass: `not run`.
- Notes: use the commands above after future edits.

## Final Checklist

- [x] `chapter_08_clean.txt` reviewed or available for review.
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

## Preserved Previous README Notes

The following section preserves the previous README content so no manual editing
history is lost during standardization.

    # Chapter 8

    Chapter: 第八章 武德沦丧南土：盘龙城

    Source mapping: PDF pages 157-172 / printed pages 145-160. Chapter 9 starts on PDF page 173.

    ## Source Method

    This chapter is a pilot for a hybrid source workflow:

    - PDF/local OCR is the structural source for chapter range, image placement, captions, and footnote markers.
    - The web text is the supporting prose source because it preserves Chinese characters more reliably than raw local OCR.
    - `pdf_ocr.txt` keeps the local OCR output for review and comparison.

    Regenerate the web support source:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_08 --output chapter_08/source.txt
    ```

    Run OCR/caption checks from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py check-pdf chapter_08/chapter_08_clean.txt --pdf 翦商.pdf --start-page 157 --end-page 172
    python3 jianshang_tools.py ocr-captions --pdf 翦商.pdf --start-page 157 --end-page 172 --clean-text chapter_08/chapter_08_clean.txt
    python3 jianshang_tools.py lint-images chapter_08/chapter_08_clean.txt
    ```

    Use `--min-confidence 3` only when a broad OCR review is useful; the default is
    stricter so body text with words such as “复原图” is less likely to appear as a
    false caption warning.

    Current clean text:

    - `chapter_08_clean.txt`: hybrid clean text with PDF-confirmed footnotes and image placeholders.
    - `pdf_ocr.txt`: page-by-page local OCR review output.

    Generate study files:

    ```bash
    python3 jianshang_tools.py table chapter_08/chapter_08_clean.txt --dictionary chapter_08/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_08/chapter_08_shengzibiao.txt
    python3 jianshang_tools.py pdf chapter_08/chapter_08_clean.txt --dictionary chapter_08/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_08/chapter_08_annotated.pdf --title '《翦商》第八章注音阅读版' --page-note '第八章约对应 PDF 页 157-172 / 印刷页 145-160'
    ```

    Generated files:

    - `reading_terms.csv`: focused reading-term dictionary for this chapter.
    - `chapter_08_shengzibiao.txt`: generated reading-term table.
    - `chapter_08_annotated.pdf`: annotated reading-practice PDF.
