# Chapter 09: 第九章 3300年前的军营：台西

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_09` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manually edited and processed`
- Last updated: `2026-07-20`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `low`

Short status note:

```text
第九章《3300年前的军营：台西》的手工校订稿已从 Downloads 导入并推广。滹沱河的字形和读音、M103图片标记、按语及原注断行均已处理；正文4处脚注与4条原注对齐，全部输出已重新生成。
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_09_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `65`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_09_shengzibiao.txt`: generated reading-term table.
- `chapter_09_annotated.pdf`: generated annotated PDF.
- `editor.html`: 20-page manual editor for PDF viewer pages 175-194.
- `chapter_09_clean_edited.txt`: editor export seed; promote only after manual review.
- `chapter_09_edit_log.txt`: editor history export target.
- `pdf_pages/page-173.jpg` through `page-192.jpg`: physical source-PDF images used by the editor.

## Source Mapping

- Chapter ID: `chapter_09`
- Title: `第九章 3300年前的军营：台西`
- PDF viewer pages: `175-194`
- Physical source-PDF pages: `173-192`
- Printed pages: `161-180`
- Mapping note: `Verified with OCR/rendered PDF pages; chapter 10 starts on PDF page 193.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_09/chapter_09_clean.txt \
  --dictionary chapter_09/reading_terms.csv \
  -o chapter_09/chapter_09_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_09/chapter_09_clean.txt \
  --dictionary chapter_09/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_09/chapter_09_annotated.pdf \
  --title '《翦商》第9章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_09/chapter_09_clean.txt
python3 jianshang_tools.py check-pdf chapter_09/chapter_09_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_09/chapter_09_clean.txt \
  --pdf 翦商.pdf \
  --start-page 173 \
  --end-page 192
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
  - `Imported the 22:11 manual TXT export and edit log; promoted notation, editor commentary, caption repair, and source-note cleanup; regenerated all outputs`
- Output regenerated after this pass: `yes`

### User Corrections

- Added pronunciation to `滹` in `滹沱河`.
- Added an editor's note comparing `穀` and `榖`, marked `待核`.
- Marked the missing `M103墓穴照片` as an image caption.
- Joined the split bibliography text in source note 3.

### Applied Edits

- `渡沱河` -> `滹（hū）沱河`
- `M103墓穴照片` -> `M103墓穴照片（图）`
- Added `滹沱河（hū tuó hé）` to `reading_terms.csv`.
- Normalized the accidental export forms `hu1` -> `hū` and `107o` -> `107。`.
- Preserved the complete `M14和M17平面图（图）` caption after the exported copy lost its closing parenthesis.

### Editing Notes

- The `穀/榖` question remains deliberately unresolved in the editor's note; do not silently change the body text before source verification.
- Source notes 1 and 3 were joined in the processed clean text so bibliographic entries render continuously.

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
随葬铜器用丝织品包裹着，其中还有一种特制皱纹绢——“穀”。
```

Issue:

```text
The manual note records that the original appears to use the wood-component form `榖`, while the silk context suggests a different character. Verify the scan and the correct textile term during final review.
```

Action needed:

- Check the source PDF pages `173-192`.
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

### 2026-07-20

- Imported `chapter_09_clean_edited.txt` and `chapter_09_edit_log.txt` from the 22:11 Downloads export.
- Promoted the reviewed changes to `chapter_09_clean.txt` and updated `reading_terms.csv`.
- Regenerated `chapter_09_shengzibiao.txt`, `chapter_09_annotated.pdf`, `editor.html`, and shared reference/navigation files.
- Checks: caption flow OK; 4 body footnote markers match 4 source notes; suspicious OCR-token check OK; `git diff --check` clean.

## Final Checklist

- [x] `chapter_09_clean.txt` reviewed or available for review.
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

    # Chapter 9

    Chapter: 第九章 3300年前的军营：台西

    Source mapping: PDF pages 173-192 / printed pages 161-180. Chapter 10 starts on PDF page 193.

    ## Source Method

    This chapter follows the hybrid source workflow:

    - PDF/local OCR is the structural source for chapter range, image placement, captions, and footnote markers.
    - The web text is the prose source because it preserves Chinese characters more reliably than raw local OCR.
    - `pdf_ocr.txt` keeps the local OCR output for review and comparison.

    Regenerate the web support source:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_09 --output chapter_09/source.txt
    ```

    Run structure and caption checks from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py check-pdf chapter_09/chapter_09_clean.txt --pdf 翦商.pdf --start-page 173 --end-page 192
    python3 jianshang_tools.py ocr-captions --pdf 翦商.pdf --start-page 173 --end-page 192 --clean-text chapter_09/chapter_09_clean.txt
    python3 jianshang_tools.py lint-images chapter_09/chapter_09_clean.txt
    ```

    Use `--min-confidence 3` only for a broader manual OCR review.

    Current clean text:

    - `chapter_09_clean.txt`: hybrid clean text with PDF-confirmed footnotes and image placeholders.
    - `pdf_ocr.txt`: page-by-page local OCR review output.

    Generate study files:

    ```bash
    python3 jianshang_tools.py table chapter_09/chapter_09_clean.txt --dictionary chapter_09/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_09/chapter_09_shengzibiao.txt
    python3 jianshang_tools.py pdf chapter_09/chapter_09_clean.txt --dictionary chapter_09/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_09/chapter_09_annotated.pdf --title '《翦商》第九章注音阅读版' --page-note '第九章约对应 PDF 页 173-192 / 印刷页 161-180'
    ```

    Generated files:

    - `reading_terms.csv`: focused reading-term dictionary for this chapter.
    - `chapter_09_shengzibiao.txt`: generated reading-term table.
    - `chapter_09_annotated.pdf`: annotated reading-practice PDF.


    ## Manual Editing

    Unedited:
    钺是军事首长的身份标志，也是献祭时砍头的工具。商代铜钺的刃部，多数并不左右对
    称，但砍剁时更便于用力。M14主人的铜钺形制威猛，钺体用朱红色装饰，造型酷似张开血
    盆大口的兽头，嘴里还有一对尖利的獴牙。
    在台西墓葬中，还有一座随葬三片牛肩胛骨的M103。墓主高约1.7米，用了两名矮小的
    男仆殉葬, 其中一名是十五岁左右的少年，双腿在膝盖以下被砍去，似乎生前就已经残疾。
    在甲骨文中，砍掉小腿是“刖（yuè）”:对那些有可能逃跑的奴隶，砍掉小腿是最好的预防手
    段，但死亡率也高。据殷墟（yīn xū）卜辞，商王会一次对多名奴隶（仆）实施刖，还要卜
    问在哪天砍腿的死亡率会比较低。

    Edited:
    钺是军事首长的身份标志，也是献祭时砍头的工具。商代铜钺的刃部，多数并不左右对称，但砍剁时更便于用力。M14主人的铜钺形制威猛，钺体用朱红色装饰，造型酷似张开血盆大口的兽头，嘴里还有一对尖利的獴牙。

    (missing image and caption) (图)

    在台西墓葬中，还有一座随葬三片牛肩胛骨的M103。墓主高约1.7米，用了两名矮小的男仆殉葬，其中一名是十五岁左右的少年，双腿在膝盖以下被砍去，似乎生前就已经残疾。在甲骨文中，砍掉小腿是“刖（yuè）”: 对那些有可能逃跑的奴隶，砍掉小腿是最好的预防手段，但死亡率也高。据殷墟（yīn xū）卜辞，商王会一次对多名奴隶（仆）实施刖，还要卜问在哪天砍腿的死亡率会比较低。


    Unedited:
    墓主的棺材中随葬了几件铜器：酒器有铜艇和铜爵（tóng jué）各一件，但缺少铜肆，无
    法构成完整的“三件套”。随葬铜器用丝织品包裹着，其中还有一种特制皱纹绢（zhòu wén
    juàn）——
    “毂”。兵器有铜镶和铜戈各一件，戈刃纤巧，长约22厘米，最宽处约5厘米。这
    在台西遗址乃至在整个商周青铜时代，都算是比较短小的，有可能是为女性武士特制的兵
    器。

    Edited:
    墓主的棺材中随葬了几件铜器：酒器有铜觚和铜爵（tóng jué）各一件，但缺少铜斝，无法构成完整的“三件套”。随葬铜器用丝织品包裹着，其中还有一种特制皱纹绢（zhòu wén juàn）——“穀”。兵器有铜镞和铜戈各一件，戈刃纤巧，长约22厘米，最宽处约5厘米。这在台西遗址乃至在整个商周青铜时代，都算是比较短小的，有可能是为女性武士特制的兵器。


    Unedited:
    此外，M112的随葬品中有铁刃铜钺和铜甑（tóng zèng）各一件。铜钺较小，接近成年人
    的手掌，主体为青铜，刃部是铁质，已经失落，但断口处还保留了较多铁质。为什么用这
    把没有刃部的钺随葬，毕竟碳化的铁远比青铜坚硬和锋利？这不好解释。可能是铁刃过于
    珍贵，后人敲了下来继续使用，只用青铜钺体给先人随葬。铜甑则比较精致，做工比台西
    其他墓葬中的铜器都要好。

    Edited:
    此外，M112的随葬品中有铁刃铜钺和铜瓿（tóng bù）各一件。铜钺较小，接近成年人的手掌，主体为青铜，刃部是铁质，已经失落，但断口处还保留了较多铁质。为什么用这把没有刃部的钺随葬，毕竟碳化的铁远比青铜坚硬和锋利？这不好解释。可能是铁刃过于珍贵，后人敲了下来继续使用，只用青铜钺体给先人随葬。铜瓿则比较精致，做工比台西其他墓葬中的铜器都要好。


    Unedited:
    台西遗址还出土了大量用石头和骨头磨制的箭头（镶），有些是底层农民的捕猎工具，
    有些则属于青铜武士。这些贵族一般只用三四枚青铜镶随葬，看来再多就负担不起了。

    Edited:
    台西遗址还出土了大量用石头和骨头磨制的箭头（镞），有些是底层农民的捕猎工具，有些则属于青铜武士。这些贵族一般只用三四枚青铜镶随葬，看来再多就负担不起了。


    Unedited:
    石斧32件，石铲13件，石镰56件，石刀23件，石饼10件，
    石镶10件，石磨盘11件，石磨棒14件。

    Edited:
    石斧32件，石铲13件，石镰56件，石刀23件，石锛10件，石镞10件，石磨盘11件，石磨棒14件。
