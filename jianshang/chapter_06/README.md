# Chapter 06: 第六章 早商：仓城奇观

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_06` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manually edited and processed`
- Last updated: `2026-07-20`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `low`

Short status note:

```text
第六章《早商：仓城奇观》的手工校订稿已导入，生字表、注音 PDF 和逐页 HTML 编辑器已重新生成。九处正文脚注均与九条原注对应；图注流检查通过。自动检查提示的 II、III、VIII 均为考古区域编号，并非 OCR 错误。
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_06_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `51`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_06_shengzibiao.txt`: generated reading-term table.
- `chapter_06_annotated.pdf`: generated annotated PDF.
- `editor.html`: manual editor with clean/annotated switching, notes, read-aloud, backup, and export controls.
- `chapter_06_clean_edited.txt`: editor output target; initially copied from the reviewed clean text.
- `editor_review_notes.tsv`: decisions and pending checks for OCR-sensitive terms and inscription text.
- `pdf_pages/page-115.jpg` through `page-128.jpg`: extracted source-page images used by the editor.

## Source Mapping

- Chapter ID: `chapter_06`
- Title: `第六章 早商：仓城奇观`
- PDF viewer pages: `117-130`
- Printed pages: `103-116`
- PDF extraction pages: `115-128`
- Mapping note: `Verified against Chapter 5 and the boundary scan; chapter 7 starts on viewer page 131, printed page 117, extraction page 129.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_06/chapter_06_clean.txt \
  --dictionary chapter_06/reading_terms.csv \
  -o chapter_06/chapter_06_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20 \
  --include-source-notes
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_06/chapter_06_clean.txt \
  --dictionary chapter_06/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_06/chapter_06_annotated.pdf \
  --title '《翦商》第6章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

Generate or refresh the editor and its source-page images:

```bash
python3 build_ocr_editor.py --chapter chapter_06 --extract-pages
```

This chapter uses `editor_review_notes.tsv` for its current inscription/OCR review. Add `oracle_review.tsv` if a future pass needs entries in the generated ancient-text review table.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_06/chapter_06_clean.txt
python3 jianshang_tools.py check-pdf chapter_06/chapter_06_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_06/chapter_06_clean.txt \
  --pdf 翦商.pdf \
  --start-page 115 \
  --end-page 128
```

Expected result for this chapter:

```text
Footnote marker check: OK
Caption flow check: OK
Suspicious OCR tokens: II, III, VIII (verified archaeological area labels)
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
  - `imported the final 00:24 manual TXT export from Downloads; promoted the two newly marked warehouse-plan captions and regenerated all study outputs`
- Output regenerated after this pass: `yes`

### User Corrections

- `Chapter 6 is done with manual editing; process the completed edition.`

### Applied Edits

- Moved `早商部分城址示意图[[fn:2]]` to its correct page and added `（图）`.
- Added `（图）` to `东下冯仓储区F501、F502圆形建筑发掘照片[[fn:6]]`.
- Added `（图）` to the `偃师商城II区` and `偃师商城III区` warehouse-plan captions from the final export.
- Separated the `乇土羊` 校疑 note from the quoted inscription line.
- Rejoined source notes 2, 4, and 9 where PDF page splitting had broken lines.
- Normalized `《晋书・食货志》` to the PDF-safe `《晋书·食货志》`.

### Editing Notes

- `The VIII-area label in the clean text is intentional; the older review row saying VII/vni was stale and has been reconciled.`
- `The inscription reading 乇土羊 remains explicitly marked 校疑 pending comparison with the original rubbing or specialist publication.`

## Confirmed Corrections

Record applied edits here. Keep the old form and the corrected form visible.

### Names and Titles

- `[old form]` -> `[corrected form]`

### Terms and Pronunciation

- `[old pinyin or OCR form]` -> `[correct form with pinyin if needed]`

### Bronze, Vessel, and Artifact Terms

- `[old form]` -> `[corrected form]`

### Image Captions

- `偃师商城II区长方形仓储建筑分布平面图` -> `偃师商城II区长方形仓储建筑分布平面图（图）`
- `偃师商城III区长方形仓储建筑分布平面图[[fn:8]]` -> `偃师商城III区长方形仓储建筑分布平面图[[fn:8]]（图）`

### Classical or Ancient Text

```text
[corrected passage]
```

Notes:

- `[brief explanation, source, or reason for correction]`
- `[whether the passage is also listed in oracle_review.tsv]`

### Footnotes

- Body markers verified: `yes (9)`
- Source notes verified: `yes (9)`
- Clustered notes split: `none`
- Special handling:
  - `[example: note 18 was split into notes 18-31]`

## Pending Manual Review

Use this section for unresolved items that need human checking.

### Open Items

Current text:

```text
乇土羊〔校疑：原书字形近“乇”，网页文本误作“毛”；此处为骨刻释文，含义仍需核对拓片/李维明文〕
```

Issue:

```text
Specialist inscription reading still needs comparison with the original rubbing or cited publication; it is not a structural PDF-generation blocker.
```

Action needed:

- Check the PDF viewer pages `117-130` (extraction pages `115-128`).
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

- `乇`, `tuō`, `rare_word`: rare graph used in the disputed bone-inscription reading.
- `镞`, `zú`, `rare_word`: arrowhead; corrects the earlier OCR-like form 铜镁 to 铜镞.

Terms requiring special care:

- `[term]`: `[multiple readings, chapter-specific pronunciation, or conflict with bronze_terms.csv]`

Term-cap note:

- Current generation command uses `--min-terms 20`.

## Image and Caption Review

- Captions checked against PDF: `yes`
- All image captions/placeholders follow the project marker convention: `yes`
- Caption flow check passed: `yes`
- Captions needing manual PDF comparison:
  - `[caption / page / issue]`

## Footnote Review

- Body markers count: `9`
- Source notes count: `9`
- Footnote sequence gaps: `none`
- Notes without body markers: `none`
- Body markers without notes: `none`
- Clustered or merged source-note issues:
  - `[details]`

## Regeneration Log

### 2026-07-20

- Imported the final manual TXT export saved to Downloads at 00:24.
- Promoted `（图）` markers for the II- and III-area warehouse-plan captions.
- Preserved the PDF-safe `《晋书·食货志》` punctuation normalization in the processed clean text.
- Regenerated the 20-entry vocabulary table, 13-page annotated PDF, and HTML editor.
- Verified 9 body footnote markers against 9 source notes; caption flow passed.

### 2026-07-19

- Imported the completed 14-page manual edition exported at 12:08.
- Generated a 20-entry focused vocabulary table.
- Generated the 13-page annotated PDF with 49 inserted annotations and 3 bronze terms.
- Generated the 14-page HTML editing workspace for viewer pages 117-130.
- Verified footnote alignment and caption flow; reviewed II, III, and VIII as intentional archaeological labels.

### 2026-07-01

- Standardized this README using `CHAPTER_README_TEMPLATE.md`.
- Preserved previous README notes below when an earlier README existed.
- Regenerated outputs in this pass: `no`.
- Checks run in this pass: `not run`.
- Notes: use the commands above after future edits.

## Final Checklist

- [x] `chapter_06_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [x] Image captions/placeholders follow the project marker convention.
- [x] Caption flow check passes.
- [x] Footnotes are aligned and checked.
- [x] `reading_terms.csv` exists.
- [ ] Chapter-specific pronunciation conflicts are resolved.
- [ ] `oracle_review.tsv` records unresolved ancient text or inscription issues when needed.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [x] `check-pdf` passes (Roman-numeral area-label warnings reviewed).
- [x] Remaining manual-review items are clearly listed.

## Preserved Previous README Notes

The following section preserves the previous README content so no manual editing
history is lost during standardization.

    # Chapter 6

    Chapter: 第六章 早商：仓城奇观

    Source mapping: PDF pages 119-128 / printed pages 107-116. Chapter 7 starts on PDF page 129.

    ## Source Method

    - The web text is the supporting prose source because it preserves Chinese characters more reliably than raw local OCR.
    - The local PDF is used to verify chapter range, image placement, captions, and footnote markers.
    - `chapter_map.csv` keeps the page mapping shared by all chapter folders.

    Regenerate the web support source:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_06 --output chapter_06/source.txt
    ```

    Run structural checks from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py check-pdf chapter_06/chapter_06_clean.txt --pdf 翦商.pdf --start-page 115 --end-page 128
    python3 jianshang_tools.py ocr-captions --pdf 翦商.pdf --start-page 115 --end-page 128 --clean-text chapter_06/chapter_06_clean.txt
    python3 jianshang_tools.py lint-images chapter_06/chapter_06_clean.txt
    ```

    Current clean text:

    - `chapter_06_clean.txt`: cleaned reading text with PDF-confirmed footnotes and image/caption placement where available.

    Generate study files:

    ```bash
    python3 jianshang_tools.py table chapter_06/chapter_06_clean.txt --dictionary chapter_06/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_06/chapter_06_shengzibiao.txt
    python3 jianshang_tools.py pdf chapter_06/chapter_06_clean.txt --dictionary chapter_06/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_06/chapter_06_annotated.pdf --title '《翦商》第六章注音阅读版' --page-note '第六章约对应 PDF 页 119-128 / 印刷页 107-116'
    ```

    Generated files:

    - `reading_terms.csv`: focused reading-term dictionary for this chapter.
    - `chapter_06_shengzibiao.txt`: generated reading-term table.
    - `chapter_06_annotated.pdf`: annotated reading-practice PDF.

    ## Review Notes

    - `editor_review_notes.tsv` records disputed characters, readings, and OCR corrections.
    - Before changing a disputed reading, check `../sources/confusing_terms.tsv`.
