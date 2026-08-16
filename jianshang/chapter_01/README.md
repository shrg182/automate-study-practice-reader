# Chapter 01: 第一章 新石器时代的社会升级

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_01` of the 《翦商》 study-material project.

## Chapter Status

- Status: `generated`
- Last updated: `2026-07-01`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `low`

Short status note:

```text
第一章 新石器时代的社会升级 has generated study outputs in this folder. No chapter-specific ancient-text review table is currently present.
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_01_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `8`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_01_shengzibiao.txt`: generated reading-term table.
- `chapter_01_annotated.pdf`: generated annotated PDF.

## Source Mapping

- Chapter ID: `chapter_01`
- Title: `第一章 新石器时代的社会升级`
- Source PDF pages: `35-46`
- Printed pages: `23-34`
- Mapping note: `Verified with rendered PDF start/end pages.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_01/chapter_01_clean.txt \
  --dictionary chapter_01/reading_terms.csv \
  -o chapter_01/chapter_01_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_01/chapter_01_clean.txt \
  --dictionary chapter_01/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_01/chapter_01_annotated.pdf \
  --title '《翦商》第1章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_01/chapter_01_clean.txt
python3 jianshang_tools.py check-pdf chapter_01/chapter_01_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_01/chapter_01_clean.txt \
  --pdf 翦商.pdf \
  --start-page 35 \
  --end-page 46
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

Action needed:

- Check the source PDF pages `35-46`.
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

- [x] `chapter_01_clean.txt` reviewed or available for review.
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

    # Chapter 1

    Chapter: 第一章 新石器时代的社会升级

    Source mapping: PDF pages 35-46 / printed pages 23-34. Chapter 2 starts on PDF page 47.

    ## Source Method

    - The web text is the supporting prose source because it preserves Chinese characters more reliably than raw local OCR.
    - The local PDF is used to verify chapter range, image placement, captions, and footnote markers.
    - `chapter_map.csv` keeps the page mapping shared by all chapter folders.

    Regenerate the web support source:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_01 --output chapter_01/source.txt
    ```

    Run structural checks from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py check-pdf chapter_01/chapter_01_clean.txt --pdf 翦商.pdf --start-page 35 --end-page 46
    python3 jianshang_tools.py ocr-captions --pdf 翦商.pdf --start-page 35 --end-page 46 --clean-text chapter_01/chapter_01_clean.txt
    python3 jianshang_tools.py lint-images chapter_01/chapter_01_clean.txt
    ```

    Current clean text:

    - `chapter_01_clean.txt`: cleaned reading text with PDF-confirmed footnotes and image/caption placement where available.

    Generate study files:

    ```bash
    python3 jianshang_tools.py table chapter_01/chapter_01_clean.txt --dictionary chapter_01/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_01/chapter_01_shengzibiao.txt
    python3 jianshang_tools.py pdf chapter_01/chapter_01_clean.txt --dictionary chapter_01/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o chapter_01/chapter_01_annotated.pdf --title '《翦商》第一章注音阅读版' --page-note '第一章约对应 PDF 页 35-46 / 印刷页 23-34'
    ```

    Generated files:

    - `reading_terms.csv`: focused reading-term dictionary for this chapter.
    - `chapter_01_shengzibiao.txt`: generated reading-term table.
    - `chapter_01_annotated.pdf`: annotated reading-practice PDF.


## Manual Editing

    Unedited:
    村落外，是成片的农田，谷穗在风中摇曳（yáo yè），它们产出的粟米（sù mǐ）（小米）
    是村民的主粮。几个男人正在给一只马鹿剥皮，用石头小刀分割皮肉，再用木柄石斧把骨
    头砍开，骨渣飞溅，引来几条狗围观争抢。
    穿越而来的访客发现，有一条四五米宽的壕沟包围着村寨（考古报告一般称之为“环壕”）
    ，沟底有积水和尖木桩防范入侵者，内侧还有一道木头栅栏，只有一座原木搭成的小桥可
    以进入村落。这群访客已经饿了，想从村里交换一餐午饭——在“原始人”眼里，他们携带的
    小镜子和打火机等是高价值宝物。

    Edited:
    村落外，是成片的农田，谷穗在风中摇曳（yáo yè），它们产出的粟米（sù mǐ）（小米）是村民的主粮。几个男人正在给一只马鹿�剥皮，用石头小刀分割皮肉，再用木柄石斧把骨头砍开，骨渣飞溅，引来几条狗围观争抢。

    (missing image caption) (图)

    穿越而来的访客发现，有一条四五米宽的壕沟包围着村寨（考古报告一般称之为“环壕”），沟底有积水和尖木桩防范入侵者，内侧还有一道木头栅栏，只有一座原木搭成的小桥可以进入村落。这群访客已经饿了，想从村里交换一餐午饭——在“原始人”眼里，他们携带的小镜子和打火机等是高价值宝物。


    Unedited:
    比如，宝鸡北首岭77M17, 仰韶文化半坡阶段，距今6000年，墓主是一名成年男子，可能
    在对外械斗中被砍掉了头颅，族人特意用一个造型奇特、有黑色花纹的陶罐代替，以示哀
    悼。随葬器物比较多，还有骨镞等兵器。

    Edited:
    比如，宝鸡北首岭77M17, 仰韶文化半坡阶段，距今6000年，墓主是一名成年男子，可能在对外械斗中被砍掉了头颅，族人特意用一个造型奇特、有黑色花纹的陶罐代替，以示哀悼。随�葬器物比较多，还有骨镞等兵器。

    (missing image caption) (图)


    Unedited:
    以上，是距今6000—5000年间（仰韶文化中期）发生的最明显变迁。

    Edited:
    (missing image caption) (图)

    以上，是距今6000—5000年间（仰韶文化中期）发生的最明显变迁。


    Unedited:
    再到下一个千年，距今5000—4000年之间（仰韶文化末期与龙山文化期），有些地区的
    人群共同体则变得更大，几个或十几个部落汇聚成了早期国家，如陕西石峁古城、山西陶
    寺古城，能统治一两万甚至三五万人口，面积相当于今天的一个或两三个县。其中，统治
    中心已经形成城市，面积有两三平方公里，周围环绕着数米高的夯土或石砌城墙，城内有
    数百平方米的大型宫殿，上层贵族开始使用精美器物，死后的墓葬里也堆满了豪华随葬品
    ，而且经常用人殉葬。

    Edited:
    再到下一个千年，距今5000—4000年之间（仰韶文化末期与龙山文化期），有些地区的人群共同体则变得更大，几个或十几个部落汇聚成了早期国家，如陕西石峁古城、山西陶寺古城，能统治一两万甚至三五万人口，面积相当于今天的一个或两三个县。其中，统治中心已经形成城市，面积有两三平方公里，周围环绕着数米高的夯土或石砌城墙，城内有数百平方米的大型宫殿，上层贵族开始使用精美器物，死后的墓葬里也堆满了豪华随葬品，而且经常用人殉葬。

    (missing image caption) (图)


    Unedited:
    王城岗古城宫殿区的一号奠基坑（二期）照片及平面图：埋两名女性青年、三名儿童、
    两名男性壮年10

    Edited:
    王城岗古城宫殿区的一号奠基坑（二期）照片及平面图：埋两名女性青年、三名儿童、两名男性壮年[10] （图）


    Unedited:
    遂公盘

    Edited:
    遂公盨


    ### Missing Images 

    There are three images of the tables of calculations in this chapter that are missing from the web version. They are present in the PDF version.

    If it is easy to detect the missing images, please add them to the web version. If not, skip them since the focus of this project is on reading practice, not on image completeness.


### Footnote Number

- 地穴式大房屋F1的地基中埋了一颗人头6：
- 地穴式大房屋F1的地基中埋了一颗人头[6]：


## Editor

[`editor.html`]

file:///Users/ruixingshi/Python/automate_study_hub3e22/practice/jianshang/chapter_01/editor.html#chapter-01-section-02