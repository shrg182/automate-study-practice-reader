# Chapter 15: 第十五章 周族的起源史诗与考古

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_15` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manual editing workspace prepared`
- Last updated: `2026-07-22`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `medium`

Short status note:

```text
第十五章《周族的起源史诗与考古》的24页手工校订编辑器、源页图像及基线学习材料已生成。《生民》八章已据在线原文校订并加入生僻词注音；8条原注留待手工校订时对齐。
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_15_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `168`.
- `oracle_review.tsv`: not currently present; create when unresolved ancient-text or OCR-sensitive passages need a review table.
- `chapter_15_shengzibiao.txt`: generated reading-term table.
- `chapter_15_annotated.pdf`: generated annotated PDF.
- `shengmin_annotated.md`: verified eight-stanza text of 《生民》 with a reader-facing rare-word glossary and source links.
- `gongliu_annotated.md`: verified six-stanza text of 《公刘》 with a reader-facing rare-word glossary and source links.
- `editor.html`: 24-page manual editor with three-part page labels.
  Its “用户札记” panel groups `编者注`, `按语`, and `待核` annotations separately from Codex-authored `读书札记`.
- `chapter_15_clean_edited.txt`: editor export seed; promote only after manual review.
- `chapter_15_edit_log.txt`: editor history export target.
- `pdf_pages/page-299.jpg` through `page-322.jpg`: physical source-PDF images used by the editor.

## Source Mapping

- Chapter ID: `chapter_15`
- Title: `第十五章 周族的起源史诗与考古`
- PDF viewer pages: `301-324`
- Physical source-PDF pages: `299-322`
- Printed pages: `287-310`
- Mapping note: `The editor renders all three systems: viewer page = printed page + 14; physical source-PDF page = printed page + 12.`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_15/chapter_15_clean.txt \
  --dictionary chapter_15/reading_terms.csv \
  -o chapter_15/chapter_15_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 100
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_15/chapter_15_clean.txt \
  --dictionary chapter_15/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  -o chapter_15/chapter_15_annotated.pdf \
  --title '《翦商》第15章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 100
```

This chapter does not currently use `oracle_review.tsv`; add it if ancient-text review is needed.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_15/chapter_15_clean.txt
python3 jianshang_tools.py check-pdf chapter_15/chapter_15_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_15/chapter_15_clean.txt \
  --pdf 翦商.pdf \
  --start-page 299 \
  --end-page 322
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

- Date: `2026-07-22`
- Editor: `Codex; awaiting manual review`
- Scope:
  - `Prepared the 24-page editor, corrected the OCR-damaged 《生民》 quotation against external text witnesses, added rare-word annotations, regenerated outputs, and ran structural checks.`
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
The source-note section contains 8 notes, while explicit body markers have not yet been aligned.
```

Issue:

```text
The body-note locations require comparison with the source images during manual editing.
```

Action needed:

- Check the source PDF pages `299-322`.
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

- Added 42 context-specific 《生民》 entries, including `禋`, `坼`, `副`, `寘`, `岐嶷`, `穟穟`, `秬秠`, `穈芑`, `軷`, `卬`, and `亶`.

Terms requiring special care:

- `[term]`: `[multiple readings, chapter-specific pronunciation, or conflict with bronze_terms.csv]`

Term-cap note:

- Current generation command uses `--min-terms 100` so both poems' manual annotations are not removed by the normal term cap.

## Image and Caption Review

- Captions checked against PDF: `[yes/no]`
- All captions end with `（图）`: `[yes/no]`
- Caption flow check passed: `yes`
- Captions needing manual PDF comparison:
  - `[caption / page / issue]`

## Footnote Review

- Body markers count: `0`
- Source notes count: `8`
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

### 2026-07-22

- Generated the 24-page manual editor and extracted source images `page-299.jpg` through `page-322.jpg`.
- Regenerated the reading table and annotated PDF with three-part page numbering.
- Checks: caption flow OK; suspicious OCR-token check OK; 8 source-note locations pending manual alignment.

### 2026-07-22 — 《生民》 source correction

- Replaced the eight OCR-damaged stanzas with the text verified against the linked 古文岛 page and the Chinese Text Project witness.
- Added `shengmin_annotated.md` with the extracted poem, source links, and a compact glossary.
- Added 42 rare or context-specific readings to `reading_terms.csv` and raised this chapter's term floor to 50.
- Regenerated the reading table, annotated PDF, editor, and aggregate reference tables.
- Checks: caption flow OK; suspicious OCR-token check OK; 8 source-note locations still pending manual alignment.

### 2026-07-22 — 《生民》 pinyin pass

- Imported the final 16:41 TXT export and preserved its source editor note.
- Expanded phrase-level coverage into individual uncommon-character entries, including contextual readings such as `副 pì`, `嶷 yí`, `褎 yòu`, and `臭 xiù`.
- Kept the clean poem free of parenthetical pinyin; the editor annotated view, PDF, dictionary, and `shengmin_annotated.md` provide the reading layer.
- Raised the chapter term floor to 70 and regenerated all outputs.

### 2026-07-22 — Final Chapter 15 review and 《公刘》 annotation pass

- Imported the final 20:22 TXT export and matching edit log.
- Verified the six stanzas of 《公刘》 against the linked 古文岛 text.
- Added `gongliu_annotated.md`, 38 contextual reading entries, and a persistent editor link.
- Normalized manually entered pinyin and restored the printed eleven-note structure where OCR had merged notes 5–11.
- Raised the chapter term floor to 100 and regenerated all outputs.

## Final Checklist

- [x] `chapter_15_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [ ] Image captions end with `（图）`.
- [x] Caption flow check passes.
- [ ] Footnotes are aligned and checked.
- [x] `reading_terms.csv` exists.
- [ ] Chapter-specific pronunciation conflicts are resolved.
- [ ] `oracle_review.tsv` records unresolved ancient text or inscription issues when needed.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [ ] `check-pdf` fully passes after manual footnote alignment.
- [x] Remaining manual-review items are clearly listed.

## Preserved Previous README Notes

The following section preserves the previous README content so no manual editing
history is lost during standardization.

    # Chapter 15

    Chapter: 第十五章 周族的起源史诗与考古

    Source mapping: PDF pages 299-322 / printed pages 287-310. Chapter 16 starts on PDF page 323.

    Generate study files from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_15 --output chapter_15/source.txt
    python3 jianshang_tools.py table chapter_15/chapter_15_clean.txt --dictionary chapter_15/reading_terms.csv -o chapter_15/chapter_15_shengzibiao.txt --max-terms-percent 0.02 --min-terms 20
    python3 jianshang_tools.py pdf chapter_15/chapter_15_clean.txt --dictionary chapter_15/reading_terms.csv --bronze-dictionary chapter_04/bronze_terms.csv -o chapter_15/chapter_15_annotated.pdf --title '《翦商》第15章注音阅读版' --chapter-map sources/chapter_map.csv
    ```

    Generated files:

    - `chapter_15_clean.txt`: reviewed chapter text.
    - `chapter_15_shengzibiao.txt`: generated reading-term table.
    - `chapter_15_annotated.pdf`: annotated reading-practice PDF.

    ## Manual Editing

    Reviewed for recurring OCR issues: measurement OCR, 区别, 铜镞, M-number confusion, and caption flow.

    2026-06-30 finetuning pass: added missing `（图）` markers, split the clustered source notes into separate notes 1-8, normalized two OCR-renumbered body note markers, and regenerated study outputs with flush-left subtitle styling.
