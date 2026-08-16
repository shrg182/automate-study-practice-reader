# Chapter 26: 第二十六章 周公新时代

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_26` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manual edit processed and outputs regenerated`
- Last updated: `2026-07-28`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `medium`

Short status note:

```text
The 18:28 follow-up export, activity log, and backup have been imported and
promoted. The new “孺子牛” note, the reading of `奄`, and the simplified form
`骍牛` are incorporated. All 24 source-note markers align; seven difficult
passages remain visible in `oracle_review.tsv`, and all outputs have been
regenerated.
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_26_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `56`.
- `oracle_review.tsv`: manual review table for difficult ancient text, oracle-bone text, bronze inscriptions, diagrams, and OCR-resistant passages.
- `chapter_26_shengzibiao.txt`: generated reading-term table.
- `chapter_26_annotated.pdf`: generated annotated PDF.
- `editor.html`: 40-page manual editor with source and annotated-PDF views.
- `chapter_26_clean_edited.txt`: page-aligned editor seed and TXT export target.
- `chapter_26_edit_log.txt`: editor activity-log export target.
- `pdf_pages/`: source-page images for physical PDF pages 521–560.

## Source Mapping

- Chapter ID: `chapter_26`
- Title: `第二十六章 周公新时代`
- Original reader pages: `523-562`
- Source PDF pages: `521-560`
- Printed pages: `509-548`
- Mapping note: `Derived from scanned table of contents; PDF pages are printed pages plus 12.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_26/chapter_26_clean.txt \
  --dictionary chapter_26/reading_terms.csv \
  -o chapter_26/chapter_26_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 56
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_26/chapter_26_clean.txt \
  --dictionary chapter_26/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  --ancient-review chapter_26/oracle_review.tsv \
  -o chapter_26/chapter_26_annotated.pdf \
  --title '《翦商》第26章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 56
```

This chapter currently uses `oracle_review.tsv`.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_26/chapter_26_clean.txt
python3 jianshang_tools.py check-pdf chapter_26/chapter_26_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_26/chapter_26_clean.txt \
  --pdf 翦商.pdf \
  --start-page 521 \
  --end-page 560
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

- Date: `2026-07-28`
- Editor: `manual + Codex`
- Scope:
  - Imported the 18:06 TXT export, matching activity log, and 40-page backup.
  - Promoted OCR, punctuation, caption, paragraph-flow, editorial-footnote, and
    commentary changes.
  - Normalized the manually confirmed readings into `reading_terms.csv`.
  - Verified the ancient state-name lists and corrected `铖` to `郕`.
  - Verified all 24 source-note markers and retained seven difficult passages.
  - Imported the 18:28 follow-up review, preserving the “孺子牛” note and
    normalizing `奄（yǎn）` and `骍牛`.
- Output regenerated after this pass: `yes`

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
Seven OCR-sensitive classical or inscription passages remain recorded in
oracle_review.tsv for comparison during manual review.
```

Issue:

```text
[OCR error, missing character, doubtful reading, caption location, source-note mismatch, etc.]
```

Action needed:

- Check the source PDF pages `521-560`.
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

Rows currently present: `7`.

Rows added or updated in this chapter:

- `[source or passage]`: `[brief reason]`

## Reading-Term Dictionary Notes

Important additions to `reading_terms.csv`:

- `敉、矧、厎、菑、斨、畀、揆、瀍、畋、忱、锜`: classical readings
  confirmed during the manual pass.
- `郕、郜、郇、邗、胙、姞、邘、郐、妘`: names of states or ancient
  surnames in the enfeoffment section.
- `辐辏、崧、雒`: OCR repairs and confirmed readings.

Terms requiring special care:

- `郇`: read `xún` here as the Zhou state name.
- `郕`: the state name in the eastern-state list; not `铖`.
- `崧`: the source title is 《崧高》; `崧` is an old variant of `嵩`.

Term-cap note:

- Current generation command uses `--min-terms 56`.

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

### 2026-07-28 — Manual editor preparation

- Generated `editor.html`, `chapter_26_clean_edited.txt`, and the initial empty
  `chapter_26_edit_log.txt`.
- Extracted 40 source-page images for physical PDF pages 521–560.
- Regenerated the reading table, annotated PDF, shared reference page, and
  chapter navigation.
- Confirmed 24 body markers against 24 source notes; all structural checks pass.
- Added a Ghostscript fallback to the editor builder for systems without
  `pdftoppm`.

### 2026-07-28 — Completed manual import

- Imported the 18:06 reviewed TXT export and activity log from `~/Downloads`;
  inspected the matching JSON backup.
- Promoted the corrected forms `斨、瀍、甗、斝、罍、锜、郕、郜、郇、邗、
  胙、姞、邘、郐、妘、辐辏、崧、雒` and the related punctuation and
  caption repairs.
- Preserved three editor-added source links and the user’s inline notes.
- Moved tone-number readings out of the prose and into the 55-entry reading
  dictionary.
- Regenerated the reading table, annotated PDF, browser editor, shared
  reference page, and chapter navigation; all structural checks pass.

### 2026-07-28 — Follow-up review

- Imported the 18:28 TXT export and matching activity log; inspected the JSON
  backup.
- Preserved the new `〔按语：孺子牛〕`.
- Added `奄（yǎn）` to the reading dictionary and removed tone-number pinyin
  from the prose.
- Normalized `騂牛` to the simplified form `骍牛` in the body and dictionary.
- Regenerated all outputs and reran the structural checks.

## Final Checklist

- [x] `chapter_26_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [x] Image captions end with `（图）` where applicable.
- [x] Caption flow check passes.
- [x] Footnotes are aligned and checked.
- [x] `reading_terms.csv` exists.
- [x] Chapter-specific pronunciation conflicts are ready for manual review.
- [x] `oracle_review.tsv` records unresolved ancient text or inscription issues when needed.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [x] `check-pdf` passes.
- [x] Remaining manual-review items are clearly listed.

## Preserved Previous README Notes

The following section preserves the previous README content so no manual editing
history is lost during standardization.

    # Chapter 26: 周公新时代

    This folder contains the working files and manual editorial notes for Chapter
    26 of the 《翦商》 study-material project.

    ## Files

    - `source.txt`: chapter text split from `sources/136.txt`.
    - `chapter_26_clean.txt`: reviewed chapter text used for generation.
    - `reading_terms.csv`: curated reading-term dictionary.
    - `oracle_review.tsv`: manual review table for difficult classical text,
      inscription text, and OCR-resistant passages.
    - `chapter_26_shengzibiao.txt`: generated reading-term table.
    - `chapter_26_annotated.pdf`: generated annotated PDF.

    ## Source Mapping

    - Chapter: `chapter_26`
    - Title: `第二十六章 周公新时代`
    - Source PDF pages: `521-560`
    - Printed pages: `509-548`

    ## Generate Outputs

    Run from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py table \
      chapter_26/chapter_26_clean.txt \
      --dictionary chapter_26/reading_terms.csv \
      -o chapter_26/chapter_26_shengzibiao.txt \
      --max-terms-percent 0.02 \
      --min-terms 30
    ```

    ```bash
    python3 jianshang_tools.py pdf \
      chapter_26/chapter_26_clean.txt \
      --dictionary chapter_26/reading_terms.csv \
      --bronze-dictionary chapter_04/bronze_terms.csv \
      --ancient-review chapter_26/oracle_review.tsv \
      -o chapter_26/chapter_26_annotated.pdf \
      --title '《翦商》第26章注音阅读版' \
      --chapter-map sources/chapter_map.csv \
      --min-terms 30
    ```

    Quality checks:

    ```bash
    python3 jianshang_tools.py lint-images chapter_26/chapter_26_clean.txt
    python3 jianshang_tools.py check-pdf chapter_26/chapter_26_clean.txt
    ```

    ## Manual Editing Summary

    The chapter contains several OCR-sensitive passages, especially names,
    classical quotations from 《尚书》, bronze-vessel terms, and figure captions.
    Confirmed corrections should be applied to `chapter_26_clean.txt`; uncertain
    classical or inscription text should also be recorded in `oracle_review.tsv`.

    ## Confirmed Corrections

    ### Names and Titles

    - `召公爽` -> `召公奭（shì）`
    - Repeated OCR variants such as `召公责` should also be normalized to
      `召公奭`.
    - `《尚书•君爽》` -> `《尚书•君奭》`

    ### Source Titles and Punctuation

    - `（《史记·管蔡世家》）` should use the middle dot form shown here.
    - `《诗经·破斧》这样歌唱：` should use `·`.
    - Classical quotation punctuation should use Chinese quotation marks consistently:
      `曰‘予复！’ 反鄙我周邦。`

    ### 《尚书》 Quotations

    The following corrections have been applied or should be preserved in the clean
    text and review table:

    ```text
    予惟小子，不敢替上帝命。天休于宁王，兴我小邦周，宁王惟卜用，
    克绥受兹命。今天其相民，矧亦惟卜用！
    ```

    ```text
    王曰：“若考作室，既厎法，厥子乃弗肯堂，矧肯构？厥父菑，
    厥子乃弗肯播，矧肯穫？”
    ```

    ```text
    王曰：猷，告尔多士。予惟时其迁居西尔。非我一人奉德不康宁。
    时惟天命。无违。朕不敢有後。无我怨！……肆予敢求尔于天邑商？
    予惟率肆矜尔！非予罪，时惟天命！
    ```

    These passages include rare or variant forms such as `矧`, `厎`, `菑`, `穫`,
    and `後`. Keep them in `oracle_review.tsv` so later manual verification remains
    visible.

    ### Vocabulary

    - `新兴的蕤尔小邦` -> `新兴的蕞尔小邦（蕞尔：小而弱的国家）`

    ### Bronze and Caption Text

    - `铜器窖藏坑H326` should not contain stray OCR replacement characters.
    - `鼎、草、卤各一件` -> `鼎、斝、卣各一件`
    - `1.铜提梁卤;2,铜鼎;3.铜分裆肆` ->
      `1. 铜提梁卣；2. 铜鼎；3. 铜分裆斝`
    - `编号H25。I?` -> `编号H25。`
    - `长度10—70厘米,单片重量5-40公斤o` ->
      `长度10—70厘米，单片重量5-40公斤。`
    - `红色的牛（驿牛）` -> `红色的牛（騂牛）`
    - Source note 16: `文王骅牛一，武王骅牛一` ->
      `文王騂牛一，武王騂牛一`
    - `非汝封又日制剂人，无或剥削人` ->
      `非汝封又曰劓刵（èr）人，无或劓刵人`
    - `“日钦剿割夏邑”“乃胥惟虐于民” “殄戮多罪”等` ->
      `“日钦劓割夏邑” “乃胥惟虐于民” “殄戮多罪”等`
    - `寇攘奸完，杀越人于货，瞥不畏死，罔弗憨` ->
      `寇攘奸宄，杀越人于货，暋不畏死，罔弗憝`
    - `敦（duì）促` -> `敦促（dūn cù）`
    - `即使比邻而居，也泾渭分明。2。` ->
      `即使比邻而居，也泾渭分明。[[fn:20]]`
    - `这也是目前发现的“中国”一 词的最早记录，它在当时的意思是
      “中原之地”。22。` ->
      `这也是目前发现的“中国”一词的最早记录，它在当时的意思是
      “中原之地”。[[fn:22]]`

    ### Footnote Section

    - Source notes 11-24 were restored after OCR removed their leading numbers.
    - The combined 洛诰/童恩正 note was split into notes 16 and 17 to match the
      body references.
    - Bare body note numbers were converted to the project format
      `[[fn:number]]`.
    - `chapter_26_clean.txt` now has 24 body markers and 24 source notes; the
      footnote check passes.

    ## Pending Manual Review

    The following notes are not final readings. They identify places that need
    checking against the source PDF, a reliable edition of 《尚书》, or a specialist
    bronze-inscription reference.

    ### Hydronym in the 洛邑 Passage

    Current note:

    ```text
    “新大邑”分布在(OCR error)水的东西两侧，
    ```

    Action:

    - Verify the character before `水` against the PDF or a reliable source.
    - Replace `(OCR error)` with the confirmed hydronym only after verification.

    ### Red Ox Term

    Resolved:

    ```text
    奉献给文王和武王各一头红色的牛（騂牛）。[[fn:16]]
    ```

    Note 16 now reads:

    ```text
    《尚书•洛诰》：“戊辰，王在新邑烝，祭岁，文王騂牛一，武王騂牛一。”
    ```

    `騂` is read `xīng` and means reddish or red-coated, especially of sacrificial
    animals in classical usage.

    ### 《尚书·康诰》 Punishment Passage

    Resolved:

    ```text
    非汝封刑人杀人，无或刑人杀人；非汝封又曰劓刵（èr）人，
    无或劓刵人。（《尚书·康诰》）
    ```

    `劓` is read `yì`, meaning to cut off the nose as a punishment; `刵` is read
    `èr`, meaning to cut off the ears.

    ### 《尚书·康诰》 寇攘 Passage

    Resolved:

    ```text
    寇攘奸宄，杀越人于货，暋不畏死，罔弗憝。（《尚书·康诰》）
    ```

    Rare characters in this line are retained in `oracle_review.tsv` for future
    manual comparison with a reliable 《尚书》 edition.

    ### “劓割” Passage

    Correction note:

    ```text
    “日钦劓割夏邑” “乃胥惟虐于民” “殄戮多罪”等，
    ```

    Resolved in `chapter_26_clean.txt`.

    ## Completed by Codex

    2026-07-01:

    - Applied the first group of confirmed corrections to `chapter_26_clean.txt`.
    - Normalized repeated `召公爽` and `召公责` OCR errors to `召公奭`.
    - Added `召公奭（shì）` to `reading_terms.csv`.
    - Added difficult 《尚书》 passages to `oracle_review.tsv`.
    - Restored and aligned the Chapter 26 source-note section, including notes
      11-24.
    - Corrected the red-ox OCR error from `驿牛`/`骅牛` to `騂牛`, and added
      `騂（xīng）` to the reading-term dictionary.
    - Corrected the 《康诰》 punishment passage to `劓刵（èr）`, and added
      `劓（yì）` to the reading-term dictionary.
    - Corrected the 《多方》 line to `日钦劓割夏邑`.
    - Corrected the 《康诰》 寇攘 line to `寇攘奸宄，杀越人于货，暋不畏死，罔弗憝`.
    - Restored bracketed superscript footnote numbers in generated PDFs.
    - Added `敦促（dūn cù）` so it is not misannotated as bronze `敦（duì）`.
    - Regenerated `chapter_26_shengzibiao.txt` and `chapter_26_annotated.pdf`.

    ## Next Editing Pass

    1. Verify the pending `(OCR error)` placeholders above.
    2. Apply confirmed corrections to `chapter_26_clean.txt`.
    3. Add unresolved passages to `oracle_review.tsv`.
    4. Regenerate the shengzibiao and PDF.
    5. Run `lint-images` and `check-pdf`.


    ### 斨
    Unedited:
    既破我斧，又缺我折。周公东征，四国是皇。

    Edited:
    既破我斧，又缺我斨(qiang1)。周公东征，四国是皇。


    ### Punctuation
    Unedited:
    周
    文王在位长达五十年（包括受命称王之前担任周邦族长的时间）o

    Edited:
    周文王在位长达五十年（包括受命称王之前担任周邦族长的时间）。


    Unedited:
    《史记宋微子世家》

    Edited:
    《史记·宋微子世家》
