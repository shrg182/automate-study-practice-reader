# Chapter 10: 第十章 殷都王室的人祭

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_10` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manually edited and processed`
- Last updated: `2026-07-20`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `low; two unencoded ancient glyphs remain marked 待核`

Short status note:

```text
第十章《殷都王室的人祭》的手工校订稿已从 Downloads 导入并推广。31处正文脚注与31条原注全部对齐，缺失图片说明和髋骨、妇妌等字词已修复；两个无法录入的古文字仍标记为待核。全部输出已重新生成并通过结构检查。
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_10_clean.txt`: reviewed chapter text used for generation.
- `editor.html`: manual OCR correction workspace against source PDF pages.
- `chapter_10_clean_edited.txt`: browser-exported manual edition seeded from `chapter_10_clean.txt`.
- `chapter_10_edit_log.txt`: browser-exported editor notes and history log.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `112`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_10_shengzibiao.txt`: generated reading-term table.
- `chapter_10_annotated.pdf`: generated annotated PDF.

## Source Mapping

- Chapter ID: `chapter_10`
- Title: `第十章 殷都王室的人祭`
- PDF viewer pages: `195-222`
- Physical source-PDF pages: `193-220`
- Printed pages: `181-208`
- Mapping note: `Derived from scanned table of contents; PDF pages are printed pages plus 12.`

Source mapping should match `sources/chapter_map.csv`.

## Manual OCR Editor

Open the local editor in a browser:

```text
file:///Users/ruixingshi/Python/automate_study_practices/practice/jianshang/chapter_10/editor.html
```

The editor shows source PDF page images beside editable text seeded from
`chapter_10_clean.txt`. Downloaded text should be treated as the manual-edition
version, `chapter_10_clean_edited.txt`, until it is reviewed and promoted back
into the normal generation workflow.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_10/chapter_10_clean.txt \
  --dictionary chapter_10/reading_terms.csv \
  -o chapter_10/chapter_10_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_10/chapter_10_clean.txt \
  --dictionary chapter_10/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_10/chapter_10_annotated.pdf \
  --title '《翦商》第10章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_10/chapter_10_clean.txt
python3 jianshang_tools.py check-pdf chapter_10/chapter_10_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_10/chapter_10_clean.txt \
  --pdf 翦商.pdf \
  --start-page 193 \
  --end-page 220
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
- Editor: `manual + Codex`
- Scope:
  - `Imported the 23:40 manual TXT export and edit log; promoted 31 footnote alignments, caption repairs, terminology corrections, and ancient-character review notes; regenerated all outputs`
- Output regenerated after this pass: `yes`

### User Corrections

- Aligned source notes 1-30 and corrected several captions and broken paragraphs.
- Corrected `人髓骨` to `人髋骨` and `妇娣` to `妇妌`.
- Marked two untypeable ancient glyphs for later verification.

### Applied Edits

- Added verified `[[fn:1]]` through `[[fn:31]]` markers.
- `人髓骨` -> `人髋骨`; `颌骨` -> `颚骨` in the reviewed anatomical list.
- `妇娣` -> `妇妌`; normalized the reading to `jìng`.
- Verified `妌` as fourth-tone `jìng` (`ㄐㄧㄥˋ`; traditional fanqie `疾政切`) against 汉典 and the Chinese Text Project; imported the supporting note into the edit log.
- Replaced the incorrect vocabulary headword `皴` with the unencoded-glyph placeholder `【奚戌】（xī）`; replaced all corresponding prose occurrences while preserving the quoted note.
- Removed the incorrect vocabulary headword `晟（chéng）`; retained `嵗（suì）` as the “岁” variant used in the passage.
- Restored captions for M1550, 50WGM1, the rows of skulls, the sacrificial-pit plan, and the 1978 horse and elephant pits.

### Editing Notes

- Tone-number input was normalized to marked pinyin: `kuan1`, `jing3`, `sui4`, and `xi1`.
- Note 31 was still a bare number in the export and was aligned during processing to complete the verified 1-31 sequence.

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
甲骨卜辞中有〔待核：异体字，拟读 zhī，字形无法录入。〕祭……
【奚戌】（xī；异体字，待核）
```

Issue:

```text
Two ancient glyphs could not be entered in Unicode during the manual pass. Descriptive placeholders preserve their positions and proposed readings.

`【它攴】` is retained as the book's component-based placeholder. The proposed `tuó` reading is not yet verified: `𢻫` is a different encoded character (`也 + 攴`) whose historical readings do not support transferring `tuó` to this oracle-bone glyph.
```

Action needed:

- Check the relevant glyph images on physical source-PDF pages 207 and 210 during ancient-text review.
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

- Captions checked against PDF: `not yet; manual pass pending`
- All captions end with `（图）`: `not yet verified`
- Caption flow check passed: `no; one warning`
- Captions needing manual PDF comparison:
  - `殷墟苗圃北地的人髓骨卜骨碎片（图）28 / viewer PDF page near 216 / determine whether 28 belongs to the caption or preceding paragraph`

## Footnote Review

- Body markers count: `31`
- Source notes count: `31`
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

### 2026-07-20

- Regenerated the 28-page manual editor and confirmed source images `page-193.jpg` through `page-220.jpg`.
- Regenerated `chapter_10_shengzibiao.txt` and `chapter_10_annotated.pdf` with three-part PDF page footers.
- Checks: suspicious OCR-token check OK; footnote alignment pending; caption-flow warning recorded above.
- Fixed stale browser storage overriding the regenerated first-page text in the editor's annotated view. Editor storage is now versioned from the current clean-text content; the chapter introduction and `盘庚王的训诫` are present on viewer page 195.
- Imported the 23:40 manual export and edit log, promoted all reviewed changes, and completed footnote 31 alignment.
- Regenerated the editor, reading table, annotated PDF, shared references, and navigation.
- Checks: 31 body markers match 31 source notes; caption flow OK; suspicious OCR-token check OK.
- Imported the 23:55 edit-log clarification and revised the `【奚戌】` and `嵗` vocabulary entries accordingly.
- Imported the 00:10 edit log containing the external dictionary verification for `妌 — jìng` and regenerated the annotated PDF.
- Imported the 02:22 text and edit-log research on `【它攴】`; retained the glyph but deferred its pronunciation after distinguishing it from `𢻫`.

## Final Checklist

- [x] `chapter_10_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [x] Image captions end with `（图）`.
- [x] Caption flow check passes.
- [x] Footnotes are aligned and checked.
- [x] `reading_terms.csv` exists.
- [ ] Chapter-specific pronunciation conflicts are resolved.
- [ ] `oracle_review.tsv` records unresolved ancient text or inscription issues when needed.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [x] `check-pdf` passes.
- [x] Remaining manual-review items are clearly listed.

## Preserved Previous README Notes

The following section preserves the previous README content so no manual editing
history is lost during standardization.

    # Chapter 10

    Chapter: 第十章 殷都王室的人祭

    Source mapping: PDF pages 193-220 / printed pages 181-208. Chapter 11 starts on PDF page 221.

    Generate study files from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_10 --output chapter_10/source.txt
    python3 jianshang_tools.py table chapter_10/chapter_10_clean.txt --dictionary chapter_10/reading_terms.csv -o chapter_10/chapter_10_shengzibiao.txt
    python3 jianshang_tools.py pdf chapter_10/chapter_10_clean.txt --dictionary chapter_10/reading_terms.csv --bronze-dictionary chapter_04/bronze_terms.csv -o chapter_10/chapter_10_annotated.pdf --title '《翦商》第10章注音阅读版' --chapter-map sources/chapter_map.csv
    ```

    Generated files:

    - `chapter_10_clean.txt`: reviewed chapter text.
    - `chapter_10_shengzibiao.txt`: generated reading-term table.
    - `chapter_10_annotated.pdf`: annotated reading-practice PDF.

    ## Manual Editing

    Reviewed for recurring OCR issues: 洹/沮 confusion, bronze vessel names, arrowhead terms, jaw-bone terms, image-caption debris, and interrupted prose around captions.

    2026-06-29 review/editing pass:

    - Added `（图）` markers to image captions in `chapter_10_clean.txt`: 洹北商城与殷墟遗址群范围、洹北商城一号宫殿发掘平面图、殷墟宫殿区建筑、刚发掘完的双墓道大墓50WGM1、墓道里成排的人头、部分祭祀坑图例、部分祭祀坑平面图、殷墟苗圃北地的人髓骨卜骨碎片、M259出土的铜甗和里面的人头.
    - Added Chapter 10 ancient-text-focused pinyin entries to `reading_terms.csv`, especially terms from 《盘庚》 and oracle-bone sacrifice vocabulary: 先后、丕、汝、曷、暨、朕、罔、迪、乃、戕、绥、钦念、忱、胥、猷、殄灭、俾、肆、笃敬、燎祭、伐、皴、岁祭、沉祭, plus related ritual and burial terms.
    - Regenerated `chapter_10_shengzibiao.txt` without a term cap so the new ancient-text annotations appear in the reading table.
    - Split the clustered source note 18 into separate notes 18-31 and restored body-side markers 19, 20, 23, 30, and 31 so the PDF notes render individually.


    Unedited:
    ……先后（xiān hòu）丕（pī）降与汝（rǔ）罪疾日：“曷（hé）不暨（jì）朕幼孙有比！
    ”故有爽德,
    自上其罚汝，汝罔（wǎng）能迪（dí）!

    Edited:
    ……先后（xiān hòu）丕（pī）降与汝（rǔ）罪疾日：“曷（hé）不暨（jì）朕幼孙有比！” 故有爽德, 自上其罚汝，汝罔（wǎng）能迪（dí）!


    Unedited:
    兹予有乱（司）政同位，具乃贝玉，乃祖先父，丕乃告我高后日：“作丕刑于朕孙！”迪
    高后丕乃崇降弗祥。

    Edited:
    兹予有乱（司）政同位，具乃贝玉，乃祖先父，丕乃告我高后日：“作丕刑于朕孙！” 迪高后丕乃崇降弗祥。


    Unedited:
    汝不忧朕心之攸困，乃咸大不宣乃心，钦念（qīn niàn）以忱（chén），动予一人，尔
    惟自鞠自苦。若乘舟，汝弗济，臭厥载。尔忱不属，惟胥（xū）以沈。不其或稽，自怒曷
    摩？

    Edited:
    汝不忧朕心之攸困，乃咸大不宣乃心，钦念（qīn niàn）以忱（chén），动予一人，尔惟自鞠自苦。若乘舟，汝弗济，臭厥载。尔忱不属，惟胥（xū）以沈。不其或稽，自怒曷瘳？


    Unedited:
    呜呼！今予告汝不易，永敬大恤，无胥绝远。汝分猷（yóu）念以相从，各设中于乃心。
    乃有不吉不迪、颠越不恭、暂遇奸完，我乃鼻J、殄灭（tiǎn miè）之，无遗育！无俾（bǐ）
    易种于兹新邑！往哉，生生！今予将试以汝迁，永建乃家！

    Edited:
    呜呼！今予告汝不易，永敬大恤，无胥绝远。汝分猷（yóu）念以相从，各设中于乃心。乃有不吉不迪、颠越不恭、暂遇奸宄，我乃劓、殄灭（tiǎn miè）之，无遗育！无俾（bǐ）易种于兹新邑！往哉，生生！今予将试以汝迁，永建乃家！


    ### References

    URL: https://hanyu.baidu.com/shici/detail?from=aladdin&pid=3854ff29f62a8454b3d445acdaa6dd57
