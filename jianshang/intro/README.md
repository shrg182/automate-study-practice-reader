# Intro: 引子

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `intro` of the 《翦商》 study-material project.

## Chapter Status

- Status: `chapter-level editor prepared`
- Last updated: `2026-07-29`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `low`

Short status note:

```text
引子 has a chapter-level browser editor and generated study outputs. No chapter-specific ancient-text review table is currently present.
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `intro_clean.txt`: reviewed chapter text used for generation.
- `intro_clean_edited.txt`: browser-editor export seed; import the reviewed TXT export here before regenerating final outputs.
- `intro_edit_log.txt`: browser-editor activity log.
- `editor.html`: chapter-level manual review workspace.
- `pdf_pages/`: 22 source-page images displayed beside the editable text.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `85`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `intro_shengzibiao.txt`: generated reading-term table.
- `intro_annotated.pdf`: generated annotated PDF.
- `reading_notes.md`: optional reader-supplied personal notes, rendered as the PDF “读书札记” appendix when it contains note sections.

## Source Mapping

- Chapter ID: `intro`
- Title: `引子`
- Source PDF pages: `13-34`
- Printed pages: `1-22`
- Mapping note: `Starts after preface line "2022年8月8日 于京西门头沟"; chapter 1 starts on page 35.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  intro/intro_clean.txt \
  --dictionary intro/reading_terms.csv \
  -o intro/intro_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  intro/intro_clean.txt \
  --dictionary intro/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  --reading-notes intro/reading_notes.md \
  -o intro/intro_annotated.pdf \
  --title '《翦商》引子注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --max-terms-percent 0.02 \
  --min-terms 20
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.
It also supports `reading_notes.md` as an optional “读书札记” section.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images intro/intro_clean.txt
python3 jianshang_tools.py check-pdf intro/intro_clean.txt
python3 jianshang_tools.py fix-punctuation intro/intro_clean.txt --check
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  intro/intro_clean.txt \
  --pdf 翦商.pdf \
  --start-page 13 \
  --end-page 34
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
- Put personal interpretive notes in `reading_notes.md`, not in `intro_clean.txt`; they render as a separate PDF appendix and are not treated as source text.

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

- Check the source PDF pages `13-34`.
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

- [x] `intro_clean.txt` reviewed or available for review.
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

    # 引子

    Chapter: 引子

    Source mapping: PDF pages 13-34 / printed pages 1-22.

    ## Source Method

    - The web text is the supporting prose source because it preserves Chinese characters more reliably than raw local OCR.
    - The local PDF is used to verify chapter range, image placement, captions, and footnote markers.
    - `chapter_map.csv` keeps the page mapping shared by all chapter folders.

    The web text does not list `引子` in the top TOC. The splitter synthesizes this title and starts after `2022年8月8日 于京西门头沟`.

    Regenerate the web support source:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter intro --output intro/source.txt
    ```

    Run structural checks from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py check-pdf intro/intro_clean.txt --pdf 翦商.pdf --start-page 13 --end-page 34
    python3 jianshang_tools.py ocr-captions --pdf 翦商.pdf --start-page 13 --end-page 34 --clean-text intro/intro_clean.txt
    python3 jianshang_tools.py lint-images intro/intro_clean.txt
    ```

    Current clean text:

    - `intro_clean.txt`: cleaned reading text with PDF-confirmed footnotes and image/caption placement where available.

    Generate study files:

    ```bash
    python3 jianshang_tools.py table intro/intro_clean.txt --dictionary intro/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o intro/intro_shengzibiao.txt
    python3 jianshang_tools.py pdf intro/intro_clean.txt --dictionary intro/reading_terms.csv --max-terms-percent 0.8 --min-terms 25 -o intro/intro_annotated.pdf --title '《翦商》引子注音阅读版' --page-note '引子约对应 PDF 页 13-34 / 印刷页 1-22'
    ```

    Generated files:

    - `reading_terms.csv`: focused reading-term dictionary for this chapter.
    - `intro_shengzibiao.txt`: generated reading-term table.
    - `intro_annotated.pdf`: annotated reading-practice PDF.


    ## Manual Editing

    Unedited:
    这层的儿童，除一人缺失下肢外，基本是完整的全躯，有一人乳牙尚未脱落，胸前挂一
    枚玉珠饰。
    后冈H10第一层平面图（图）
    有两名青年，编号为17号和21号，性别不详，姿势相同，伏地，朝东方跪拜，平行相隔

    Edited:
    这层的儿童，除一人缺失下肢外，基本是完整的全躯，有一人乳牙尚未脱落，胸前挂一枚玉珠饰。
    后冈H10第二层平面图（图）
    有两名青年，编号为17号和21号，性别不详，姿势相同，伏地，朝东方跪拜，平行相隔


    Unedited:
    比如，《合集》32093 :“卯（mǎo）三羌（qiāng）二牛。卯五羌三牛“卯”是把人或牲畜对
    半剖开、悬挂的祭祀方式；“羌”是当时的晋陕土著人群，《合集》32093拓片[13]（图）
    商王祭祀最常使用羌人。“羌”的甲骨文造型是头顶羊角的人，有时还写成脖子被捆绑甚
    至拴在木桩上，表示他们已经被俘获。

    Edited:
    比如，《合集》32093: “卯（mǎo）三羌（qiāng）二牛。卯五羌三牛“卯”是把人或牲畜对半剖开、悬挂的祭祀方式；“羌”是当时的晋陕土著人群，商王祭祀最常使用羌人。
    《合集》32093拓片[13]（图）
    “羌”的甲骨文造型是头顶羊角的人，有时还写成脖子被捆绑甚至拴在木桩上，表示他们已经被俘获。


    Unedited:
    先看这一万余名人牲在殷都总人口中的比例。祭祀坑的使用时间跨度约两百年，在这段
    时间，殷都累计总人口约一百万。
    [17] 这样比较，正常死者和人牲的比例是100：1。但需要
    注意，

    Edited:
    先看这一万余名人牲在殷都总人口中的比例。祭祀坑的使用时间跨度约两百年，在这段时间，殷都累计总人口约一百万。[17] 这样比较，正常死者和人牲的比例是100:1。但需要注意，


    Unedited:
    在殷墟范围内，已发现的正常墓葬约6500座，[19] 代表正常死亡的6500人，那么，正常死
    者和人牲的比例是65：100, 也就是说，在65名自由人背后，有100名被杀祭的人牲。当然，
    100：1和65：100代表的是两个极端，真实数值应当在这两者之间。

    Edited:
    在殷墟范围内，已发现的正常墓葬约6500座，[19] 代表正常死亡的6500人，那么，正常死者和人牲的比例是65:100，也就是说，在65名自由人背后，有100名被杀祭的人牲。当然，100:1和65:100代表的是两个极端，真实数值应当在这两者之间。


    Unedited:
     贝，甲骨文作C9, 见《合集》11423正。《尚书•盘庚》：“兹予有乱政同位，具乃贝玉。
    ”孔颖达疏：
    “贝者，水虫。古人取其甲以为货，如今之用钱然贝壳作钱已是习惯，东周以后，贝币才逐渐被各
    种金属货币取代，云南一些少数民族地区更是沿用贝币直到明代。

    Edited:
    贝，甲骨文作（甲骨文），见《合集》11423正。《尚书•盘庚》：“兹予有乱政同位，具乃贝玉。”孔颖达疏：“贝者，水虫。古人取其甲以为货，如今之用钱然贝壳作钱已是习惯，东周以后，贝币才逐渐被各种金属货币取代，云南一些少数民族地区更是沿用贝币直到明代。


    Unedited:
    郭沫若：《甲骨文合集》，中华书局，1999年，32093条，以下简称《合集》。商代甲骨卜辞中的“
    羌「 主要是山西、陕西地区的土著居民，这些人在周代逐渐汇聚成为华夏族。

    Edited:
    郭沫若：《甲骨文合集》，中华书局，1999年，32093条，以下简称《合集》。商代甲骨卜辞中的“羌”主要是山西、陕西地区的土著居民，这些人在周代逐渐汇聚成为华夏族。


    Unedited:
    活过的人口总量约一百万人。参见宋镇豪《商代史论纲》，中国社会科学出版社，2011年，第136
    页。

    Edited:
    活过的人口总量约一百万人。参见宋镇豪《商代史论纲》，中国社会科学出版社，2011年，第136页。
