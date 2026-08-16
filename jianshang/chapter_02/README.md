# Chapter 02: 第二章 大禹治水真相：稻与龙

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_02` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manual-editor-ready`
- Last updated: `2026-07-10`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `low`

Short status note:

```text
第二章 大禹治水真相：稻与龙 now has a page-by-page manual OCR editor seeded from `chapter_02_clean_edited.txt`. The annotated PDF and reading table have been regenerated from the edited text.
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_02_clean.txt`: reviewed chapter text used for generation.
- `chapter_02_clean_edited.txt`: page-by-page manual-edition seed/export for the browser editor.
- `chapter_02_edit_log.txt`: downloaded or pasted editor log storage target.
- `editor.html`: local browser editor with source PDF page images, editable text, reference tables, and editor notes.
- `pdf_pages/`: source PDF page images used by `editor.html`.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `16`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_02_shengzibiao.txt`: generated reading-term table.
- `chapter_02_annotated.pdf`: generated annotated PDF.

## Manual Editor

Open from the local web server:

```text
http://localhost:8000/practice/jianshang/chapter_02/editor.html
```

If the browser shows an older saved draft, click `恢复内置稿` once to reload the current built-in text.

## Source Mapping

- Chapter ID: `chapter_02`
- Title: `第二章 大禹治水真相：稻与龙`
- Source PDF pages: `47-60`
- Printed pages: `35-48`
- Mapping note: `Verified with rendered PDF pages; page 60 is blank and chapter 3 starts on page 61.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_02/chapter_02_clean_edited.txt \
  --dictionary chapter_02/reading_terms.csv \
  -o chapter_02/chapter_02_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_02/chapter_02_clean_edited.txt \
  --dictionary chapter_02/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_02/chapter_02_annotated.pdf \
  --title '《翦商》第2章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_02/chapter_02_clean_edited.txt
python3 jianshang_tools.py check-pdf chapter_02/chapter_02_clean_edited.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_02/chapter_02_clean_edited.txt \
  --pdf 翦商.pdf \
  --start-page 47 \
  --end-page 60
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

### Footnote Alignment

- `从陶器器型看，新砦属于主要分
布在淮河、汉江流域以及长江中游北岸稻作区的煤山文化，且位于煤山文化的最北边，稻
作和旱作农业的杂糅地带。` -> `从陶器器型看，新砦属于主要分布在淮河、汉江流域以及长江中游北岸稻作区的煤山文化，[10] 且位于煤山文化的最北边，稻作和旱作农业的杂糅地带。` (verified)

- 其中最典型的，是一座二期墓葬，编号
2002VM3。墓主上身放着一条绿松石镶嵌的“龙形器”
，-> 其中最典型的，是一座二期墓葬，编号2002VM3。[12] 墓主上身放着一条绿松石镶嵌的“龙形器”，

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

- `二里头出土的粟、黍和稻粒：三者体积差别很大，如果用颗粒数来衡量它们的种植面积
，显然会产生重大偏差。
[4]` -> `二里头出土的粟、黍和稻粒：三者体积差别很大，如果用颗粒数来衡量它们的种植面积，显然会产生重大偏差。[4]（图）`

- 石峁皇城台大台基8号石雕龙拓片（图） -> 石峁皇城台大台基8号石雕龙拓片[16]（图）

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

- Check the source PDF pages `47-60`.
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

- [x] `chapter_02_clean.txt` reviewed or available for review.
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

    # Chapter 2

    Chapter: 第二章 大禹治水真相：稻与龙

    Source mapping: PDF pages 47-60 / printed pages 35-48. PDF page 60 is blank; Chapter 3 starts on PDF page 61.

    ## Source Method

    - The web text is the supporting prose source because it preserves Chinese characters more reliably than raw local OCR.
    - The local PDF is used to verify chapter range, image placement, captions, and footnote markers.
    - `chapter_map.csv` keeps the page mapping shared by all chapter folders.

    Regenerate the web support source:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_02 --output chapter_02/source.txt
    ```

    Run structural checks from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py check-pdf chapter_02/chapter_02_clean.txt --pdf 翦商.pdf --start-page 47 --end-page 60
    python3 jianshang_tools.py ocr-captions --pdf 翦商.pdf --start-page 47 --end-page 60 --clean-text chapter_02/chapter_02_clean.txt
    python3 jianshang_tools.py lint-images chapter_02/chapter_02_clean.txt
    ```

    Current clean text:

    - `chapter_02_clean.txt`: cleaned reading text with PDF-confirmed footnotes and image/caption placement where available.

    Generate study files:

    ```bash
    python3 jianshang_tools.py table chapter_02/chapter_02_clean.txt --dictionary chapter_02/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_02/chapter_02_shengzibiao.txt
    python3 jianshang_tools.py pdf chapter_02/chapter_02_clean.txt --dictionary chapter_02/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_02/chapter_02_annotated.pdf --title '《翦商》第二章注音阅读版' --page-note '第二章约对应 PDF 页 47-60 / 印刷页 35-48'
    ```

    Generated files:

    - `reading_terms.csv`: focused reading-term dictionary for this chapter.
    - `chapter_02_shengzibiao.txt`: generated reading-term table.
    - `chapter_02_annotated.pdf`: annotated reading-practice PDF.


    ## Manual Editing

    Unedited:
    二里头一期（距今约3900—3800年）的聚落规模，继承了新砦遗址，面积约1平方公里，
    尚未发现大型建筑。不过，水稻在二里头
    人的粮食中已占据最重要地位：在这一期地层内，发现水稻953粒、粟155粒、黍36粒。
    [8] 

    Edited:
    二里头一期（距今约3900—3800年）的聚落规模，继承了新砦遗址，面积约1平方公里，尚未发现大型建筑。

    (missing image caption) (图)

    不过，水稻在二里头人的粮食中已占据最重要地位：在这一期地层内，发现水稻953粒、粟155粒、黍36粒。[8]


    Unedited:
    2002VM3绿松石龙形器14
    二里头发现的龙蛇纹饰”

    Edited:
    2002VM3绿松石龙形器[14] (图)
    二里头发现的龙蛇纹饰[15] (图)


    Unedited:
    石峁的龙元素并不多，到二里头则蔚为大观（wèi wéi dà guān）。
    比较起来，二里头的龙的规格更高，出现在最为显赫的墓葬，且俯卧在墓主上半身。

    Edited:
    石峁的龙元素并不多，到二里头则蔚为大观（wèi wéi dà guān）。

    (missing image caption) (图)

    比较起来，二里头的龙的规格更高，出现在最为显赫的墓葬，且俯卧在墓主上半身。
