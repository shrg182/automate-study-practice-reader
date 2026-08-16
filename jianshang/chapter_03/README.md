# Chapter 03: 第三章 二里头：青铜铸造王权

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_03` of the 《翦商》 study-material project.

## Chapter Status

- Status: `generated`
- Last updated: `2026-07-01`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `low`

Short status note:

```text
第三章 二里头：青铜铸造王权 has generated study outputs in this folder. No chapter-specific ancient-text review table is currently present.
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_03_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `27`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_03_shengzibiao.txt`: generated reading-term table.
- `chapter_03_annotated.pdf`: generated annotated PDF.

## Source Mapping

- Chapter ID: `chapter_03`
- Title: `第三章 二里头：青铜铸造王权`
- Source PDF pages: `61-86`
- Printed pages: `49-74`
- Mapping note: `Verified with rendered PDF pages; chapter 4 starts on page 87.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_03/chapter_03_clean.txt \
  --dictionary chapter_03/reading_terms.csv \
  -o chapter_03/chapter_03_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_03/chapter_03_clean.txt \
  --dictionary chapter_03/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_03/chapter_03_annotated.pdf \
  --title '《翦商》第3章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_03/chapter_03_clean.txt
python3 jianshang_tools.py check-pdf chapter_03/chapter_03_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_03/chapter_03_clean.txt \
  --pdf 翦商.pdf \
  --start-page 61 \
  --end-page 86
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


### Footnote Number

- 《竹书纪年》记载，夏朝共有471年。
  - `《竹书纪年》记载，夏朝共有471年。` -> `《竹书纪年》记载，夏朝共有471年。[1]` 

### Textual Alignment

- `此外，殿堂西侧还有人祭坑M57，坑穴也极为窄小，宽度仅有
30多厘米，死者仰身直肢，身体微扭曲，发掘报告推测，这应该也是被捆绑后勉强填塞
进去的。`
 -> `此外，殿堂西侧还有人祭坑M57，坑穴也极为窄小，宽度仅有30多厘米，死者仰身直肢，身体微扭曲，发掘报告推测，这应该也是被捆绑后勉强填塞进去的。` (verified)

- 及禹崩，虽授益，益之佐禹日浅，天下未洽。故诸侯皆去益

而朝启，日：
“吾君帝禹之子也。
”于是启遂即天子之位，是为夏后帝启。

-> 及禹崩，虽授益，益之佐禹日浅，天下未洽。故诸侯皆去益而朝启，曰：“吾君帝禹之子也。”于是启遂即天子之位，是为夏后帝启。

### 菹
- 禹掘地而注之海，驱蛇龙而放之范，水由地中行，江、淮、河、汉是也。
- -> 禹掘地而注之海，驱蛇龙而放之菹(zū)，水由地中行，江、淮、河、汉是也。

### Image Caption Alignment

- 夏末商初中原主要考古文化分布图6：郑州（大师姑）和新郑望京楼处在二里头文化的
东部边疆，其中的二里岗（冈）文化兴起较晚，和二里头是前后承接关系。
  -> 夏末商初中原主要考古文化分布图[6]：郑州（大师姑）和新郑望京楼处在二里头文化的东部边疆，其中的二里岗（冈）文化兴起较晚，和二里头是前后承接关系。（图）


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

Current tex:

```text
- 东卜冯文化
Q 50 ]pkm
```

Issue:
```text
[不知从何而来的文字和符号。OCR artifact, misread, or unrecognized character sequence]
```
  


Action needed:

- Check the source PDF pages `61-86`.
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

- [x] `chapter_03_clean.txt` reviewed or available for review.
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

    # Chapter 3

    Chapter: 第三章 二里头：青铜铸造王权

    Source mapping: PDF pages 61-86 / printed pages 49-74. Chapter 4 starts on PDF page 87.

    ## Source Method

    - The web text is the supporting prose source because it preserves Chinese characters more reliably than raw local OCR.
    - The local PDF is used to verify chapter range, image placement, captions, and footnote markers.
    - `chapter_map.csv` keeps the page mapping shared by all chapter folders.

    Regenerate the web support source:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_03 --output chapter_03/source.txt
    ```

    Run structural checks from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py check-pdf chapter_03/chapter_03_clean.txt --pdf 翦商.pdf --start-page 61 --end-page 86
    python3 jianshang_tools.py ocr-captions --pdf 翦商.pdf --start-page 61 --end-page 86 --clean-text chapter_03/chapter_03_clean.txt
    python3 jianshang_tools.py lint-images chapter_03/chapter_03_clean.txt
    ```

    Current clean text:

    - `chapter_03_clean.txt`: cleaned reading text with PDF-confirmed footnotes and image/caption placement where available.

    Generate study files:

    ```bash
    python3 jianshang_tools.py table chapter_03/chapter_03_clean.txt --dictionary chapter_03/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_03/chapter_03_shengzibiao.txt
    python3 jianshang_tools.py pdf chapter_03/chapter_03_clean.txt --dictionary chapter_03/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_03/chapter_03_annotated.pdf --title '《翦商》第三章注音阅读版' --page-note '第三章约对应 PDF 页 61-86 / 印刷页 49-74'
    ```

    Generated files:

    - `reading_terms.csv`: focused reading-term dictionary for this chapter.
    - `chapter_03_shengzibiao.txt`: generated reading-term table.
    - `chapter_03_annotated.pdf`: annotated reading-practice PDF.
