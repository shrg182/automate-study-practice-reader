# Chapter 07: 第七章 人祭繁荣与宗教改革运动

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_07` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manually edited and processed`
- Last updated: `2026-07-20`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `low`

Short status note:

```text
第七章《人祭繁荣与宗教改革运动》的最终手工校订稿已从 Downloads 导入并推广。正文29处脚注标记与29条原注对齐；图注、页面边界和两条参考文献 OCR 问题已核对；生字表、注音 PDF 和 HTML 编辑器已重新生成。
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_07_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `123`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_07_shengzibiao.txt`: generated reading-term table.
- `chapter_07_annotated.pdf`: generated annotated PDF.
- `editor.html`: 28-page manual editor for PDF viewer pages 131-158.
- `chapter_07_clean_edited.txt`: editor export seed; promote only after manual review.
- `chapter_07_edit_log.txt`: editor history export target.

## Source Mapping

- Chapter ID: `chapter_07`
- Title: `第七章 人祭繁荣与宗教改革运动`
- PDF viewer pages: `131-158`
- Printed pages: `117-144`
- PDF extraction pages: `129-156`
- Mapping note: `Verified with rendered PDF pages; notes end on extraction page 155 and extraction page 156 is blank.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_07/chapter_07_clean.txt \
  --dictionary chapter_07/reading_terms.csv \
  -o chapter_07/chapter_07_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_07/chapter_07_clean.txt \
  --dictionary chapter_07/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_07/chapter_07_annotated.pdf \
  --title '《翦商》第7章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_07/chapter_07_clean.txt
python3 jianshang_tools.py check-pdf chapter_07/chapter_07_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_07/chapter_07_clean.txt \
  --pdf 翦商.pdf \
  --start-page 129 \
  --end-page 156
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
  - `imported the 12:59 follow-up manual TXT export and edit log; merged the new inline commentary and editor note while retaining verified corrections; regenerated all outputs`
- Output regenerated after this pass: `yes`

### User Corrections

- `I did editing on Chapter 7 again and entered notation and editor's notation. Please check ~/Downloads and process the updates.`

### Applied Edits

- Restored source-note labels `14-29`, which had been dropped from the web-text extraction.
- Added missing body markers `[[fn:4]]`, `[[fn:11]]`, and `[[fn:16]]`.
- Added `（图）` to the captions associated with notes 4 and 11.
- Rejoined prose and source notes split across editor page boundaries.
- Moved three captions to their correct positions and added missing `（图）` markers.
- Corrected `迁于藏` to `迁于隞` and recorded the reading `隞（áo）`.
- Recorded the reading of `莪（é）` in `刘士莪`.
- Corrected note 20 to `《东方博物》` and repaired the quotation punctuation in note 28 after comparison with extraction page 155.
- Added the inline commentary `〔按语：用俘虏祭祀。〕`.
- Added `〔编者注1〕猪祭，狗祭，人祭，在商中期达到最高峰。人祭多为俘虏。反对人祭派的失败是一个因素。`
- Rejoined two additional prose lines split at editor page boundaries.

### Editing Notes

- Roman numerals `IV` and `VIII` are intentional archaeological area labels.

## Confirmed Corrections

Record applied edits here. Keep the old form and the corrected form visible.

### Names and Titles

- `[old form]` -> `[corrected form]`

### Terms and Pronunciation

- `迁于藏` -> `迁于隞` (`隞`, `áo`)
- `刘士莪` -> retained with reading `莪`, `é`

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

- Body markers verified: `yes (29)`
- Source notes verified: `yes (29)`
- Clustered notes split: `notes 19-21`
- Special handling:
  - `[example: note 18 was split into notes 18-31]`

## Pending Manual Review

Use this section for unresolved items that need human checking.

### Open Items

Current text:

```text
None.
```

Issue:

```text
The previously malformed note 20 and note 28 entries were verified against extraction page 155 and corrected.
```

Action needed:

- Check the source PDF pages `129-156`.
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

- `隞`, `áo`, `place`: Shang capital near modern Xingyang, Henan.
- `莪`, `é`, `rare_word`: reading used in the name `刘士莪`.

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

- Body markers count: `29`
- Source notes count: `29`
- Footnote sequence gaps: `none`
- Notes without body markers: `none`
- Body markers without notes: `none`
- Clustered or merged source-note issues:
  - `Notes 19-21 were separated from one merged extraction paragraph.`

## Regeneration Log

### 2026-07-20

- Imported the 12:59 follow-up manual export and edit log, and inspected the matching backup from Downloads.
- Preserved the new inline `按语` and rendered one editor note in a separate `编者注` PDF section.
- Added PDF-generation support for `[[editor-fn:n]]`, `〔编者注n〕`, and styled inline `〔按语：…〕` content.
- Regenerated the 25-page annotated PDF with 106 annotations and 4 bronze terms; all structural checks passed.
- Imported the final manual export saved to Downloads at 01:16 and its edit log at 01:17.
- Promoted paragraph joins, caption placement, `迁于隞`, and source-note joins from the manual pass.
- Added dictionary readings for `隞（áo）` and `莪（é）`.
- Verified and corrected source notes 20 and 28 against extraction page 155.
- Regenerated the annotated PDF with 106 annotations and 4 bronze terms; all structural checks passed.
- Generated the 28-page manual editing workspace for viewer pages 131-158.
- Rendered source-page JPEGs for extraction pages 129-156.
- Restored note numbering 14-29 and missing body markers 4, 11, and 16.
- Generated the 20-entry focused vocabulary table and annotated PDF with 104 annotations and 4 bronze terms.
- Verified 29 body markers against 29 source notes; caption flow passed.

### 2026-07-01

- Standardized this README using `CHAPTER_README_TEMPLATE.md`.
- Preserved previous README notes below when an earlier README existed.
- Regenerated outputs in this pass: `no`.
- Checks run in this pass: `not run`.
- Notes: use the commands above after future edits.

## Final Checklist

- [x] `chapter_07_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [x] Image captions end with `（图）`.
- [x] Caption flow check passes.
- [x] Footnotes are aligned and checked.
- [x] `reading_terms.csv` exists.
- [x] Chapter-specific pronunciation conflicts are resolved.
- [ ] `oracle_review.tsv` records unresolved ancient text or inscription issues when needed.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [x] `check-pdf` passes (Roman-numeral area-label warnings reviewed).
- [x] Remaining manual-review items are clearly listed.

## Preserved Previous README Notes

The following section preserves the previous README content so no manual editing
history is lost during standardization.

    # Chapter 7

    Chapter: 第七章 人祭繁荣与宗教改革运动

    Source mapping: PDF pages 129-156 / printed pages 117-144. Page 156 is blank; Chapter 8 starts on PDF page 157.

    ## Source Method

    - The web text is the supporting prose source because it preserves Chinese characters more reliably than raw local OCR.
    - The local PDF is used to verify chapter range, image placement, captions, and footnote markers.
    - `chapter_map.csv` keeps the page mapping shared by all chapter folders.

    Regenerate the web support source:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_07 --output chapter_07/source.txt
    ```

    Run structural checks from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py check-pdf chapter_07/chapter_07_clean.txt --pdf 翦商.pdf --start-page 129 --end-page 156
    python3 jianshang_tools.py ocr-captions --pdf 翦商.pdf --start-page 129 --end-page 156 --clean-text chapter_07/chapter_07_clean.txt
    python3 jianshang_tools.py lint-images chapter_07/chapter_07_clean.txt
    ```

    Current clean text:

    - `chapter_07_clean.txt`: cleaned reading text with PDF-confirmed footnotes and image/caption placement where available.

    Generate study files:

    ```bash
    python3 jianshang_tools.py table chapter_07/chapter_07_clean.txt --dictionary chapter_07/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_07/chapter_07_shengzibiao.txt
    python3 jianshang_tools.py pdf chapter_07/chapter_07_clean.txt --dictionary chapter_07/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_07/chapter_07_annotated.pdf --title '《翦商》第七章注音阅读版' --page-note '第七章约对应 PDF 页 129-156 / 印刷页 117-144'
    ```

    Generated files:

    - `reading_terms.csv`: focused reading-term dictionary for this chapter.
    - `chapter_07_shengzibiao.txt`: generated reading-term table.
    - `chapter_07_annotated.pdf`: annotated reading-practice PDF.
