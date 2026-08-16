# Chapter 19: 第十九章 羑里牢狱记忆

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_19` of the 《翦商》 study-material project.

## Chapter Status

- Status: `manual export processed`
- Last updated: `2026-07-23`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `low`

Short status note:

```text
The completed 19:34 manual export and 32-entry edit log were imported. All 19
source notes are aligned, OCR and layout corrections are promoted, and two
unresolved glyph readings remain explicitly flagged for review.
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_19_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `80`.
- `oracle_review.tsv`: two unresolved glyph/OCR review items from the manual pass.
- `chapter_19_shengzibiao.txt`: generated reading-term table.
- `chapter_19_annotated.pdf`: generated annotated PDF.
- `editor.html`: 18-page manual editor with explicit reader, physical-PDF, printed-page, and annotated-PDF numbering.
- `chapter_19_clean_edited.txt`: page-aligned editor seed and TXT export target.
- `chapter_19_edit_log.txt`: editor activity-log export target.
- `pdf_pages/`: source-page images for physical PDF pages 369–386.

## Source Mapping

- Chapter ID: `chapter_19`
- Title: `第十九章 羑里牢狱记忆`
- Original reader pages: `371-388`
- Physical source PDF pages: `369-386`
- Printed pages: `357-374`
- Annotated PDF pages: `1-15` (independently reflowed; not mapped one-to-one to source pages)
- Mapping note: original reader pages are printed pages plus 14; physical source PDF pages are printed pages plus 12; chapter 20 starts on reader page 389.

Source mapping should match `sources/chapter_map.csv`.

### 2026-07-23 — Manual editor preparation

- Generated all 18 source-page images and the Chapter 19 browser editor.
- Seeded the editor with explicit page boundaries from reader page 371 through 388.
- Enabled header shortcuts for 注音、编者注、按语、待核 and 用户札记, plus the full marker composer in 编辑札记.
- Included the synchronized chapter reading and bronze-term reference panels and the shared book-wide reference links.
- Left the 19 source-note placements for manual alignment because the baseline text has note definitions but no verified body markers.

### 2026-07-23 — Completed manual export processing

- An initial 16:34 export was empty; a second scan of `~/Downloads` found the
  completed 19:34 TXT export, matching JSON backup, and 32-entry edit log.
- Imported and promoted the completed export, removing editor-only page headers
  and moving 15 numeric pinyin additions into `reading_terms.csv`.
- Aligned all 19 source-note markers and preserved one inline 按语.
- Promoted the reviewed OCR, hexagram-symbol, caption, quotation, and paragraph
  corrections.
- Regenerated the reading table, annotated PDF, chapter editor, shared table of
  contents, and book-wide reference tables.
- Confirmed footnote alignment, clean caption flow, and no suspicious OCR
  tokens.
- Added the three remaining glyph questions to `oracle_review.tsv`.

### 2026-07-23 — Hexagram rendering follow-up

- Imported the completed 19:53 TXT export, matching 42-entry JSON backup, and
  43-entry exported edit log.
- Preserved and normalized six hexagram-name/code-point annotations and the
  revised 句度 note.
- Resolved the 召公 name as `召公奭` and added `奭 shì` to
  `reading_terms.csv`.
- Changed PDF rendering so Unicode hexagrams fall back to upper/lower trigram
  pairs, avoiding missing-glyph boxes in PDF viewers.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_19/chapter_19_clean.txt \
  --dictionary chapter_19/reading_terms.csv \
  -o chapter_19/chapter_19_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_19/chapter_19_clean.txt \
  --dictionary chapter_19/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  --ancient-review chapter_19/oracle_review.tsv \
  -o chapter_19/chapter_19_annotated.pdf \
  --title '《翦商》第19章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

The generated PDF includes the three open items from `oracle_review.tsv`.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py lint-images chapter_19/chapter_19_clean.txt
python3 jianshang_tools.py check-pdf chapter_19/chapter_19_clean.txt
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_19/chapter_19_clean.txt \
  --pdf 翦商.pdf \
  --start-page 369 \
  --end-page 386
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

- Date: `2026-07-23`
- Editor: `manual + Codex`
- Scope:
  - `Review and process the latest manual editor export; regenerate all outputs.`
- Output regenerated after this pass: `yes`

### User Corrections

- Manual review was reported complete; process the latest export and regenerate
  all outputs.

### Applied Edits

- Promoted the completed manual corrections, all 19 footnote markers, one 按语,
  and the corrected 易卦 symbols and quotations.
- Added 15 reviewed pronunciations to `reading_terms.csv`.

### Editing Notes

- The completed edit log contains 32 entries.
- Two unresolved glyph readings remain marked 待核 and are recorded in
  `oracle_review.tsv`.

## Confirmed Corrections

Record applied edits here. Keep the old form and the corrected form visible.

### Names and Titles

- `[old form]` -> `[corrected form]`

### Terms and Pronunciation

- Added: 醢 hǎi, 窞 dàn, 牖 yǒu, 祗 zhī, 纆 mò, 屦 jù, 胏 zǐ, 觌 dí,
  绂 fú, 逋 bū, 眚 shěng, 藟 lěi, 臲卼 niè wù, 矜 jīn, 稊 tí.

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

- Body markers verified: `yes`
- Source notes verified: `yes`
- Clustered notes split: `none`
- Special handling: all 19 markers are aligned in sequence.

## Pending Manual Review

Use this section for unresolved items that need human checking.

### Open Items

Current text:

```text
〔待核：钺；无金字旁〕
〔待核：窥；繁体〕观
```

Issue: unresolved ancient/OCR glyph forms; see `oracle_review.tsv`.

Action needed:

- Check the source PDF pages `369-386`.
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

Rows currently present: `2`.

Rows added or updated in this chapter:

- Reader page 380: “钺” without the metal radical.
- Reader page 383: the traditional form of 窥 in the 观卦 quotation.

## Reading-Term Dictionary Notes

Important additions to `reading_terms.csv`:

- Fifteen manual pronunciation additions were normalized to tone-mark pinyin;
  see `Terms and Pronunciation` above.

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

- Body markers count: `19`
- Source notes count: `19`
- Footnote sequence gaps: `none`
- Notes without body markers: `none`
- Body markers without notes: `none`
- Clustered or merged source-note issues:
  - `[details]`

## Regeneration Log

### 2026-07-23

- Imported and promoted the completed 19:53 manual TXT export and 43-entry log.
- Regenerated `chapter_19_shengzibiao.txt`,
  `chapter_19_annotated.pdf`, `editor.html`, `reference_tables.html`, and
  `shared/editor_toc.js`.
- Checks: footnote markers `OK` (19/19); caption flow `OK`; suspicious OCR
  tokens `OK`.
- Rendered annotated PDF page 2 to PNG and visually confirmed that all six
  listed hexagrams display as trigram pairs instead of missing-glyph boxes.

### 2026-07-01

- Standardized this README using `CHAPTER_README_TEMPLATE.md`.
- Preserved previous README notes below when an earlier README existed.
- Regenerated outputs in this pass: `no`.
- Checks run in this pass: `not run`.
- Notes: use the commands above after future edits.

## Final Checklist

- [x] `chapter_19_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [ ] Image captions end with `（图）`.
- [x] Caption flow check passes.
- [x] Footnotes are aligned and checked.
- [x] `reading_terms.csv` exists.
- [ ] Chapter-specific pronunciation conflicts are resolved.
- [x] `oracle_review.tsv` records unresolved ancient text or inscription issues when needed.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [x] `check-pdf` structural checks pass.
- [x] Remaining manual-review items are clearly listed.

## Preserved Previous README Notes

The following section preserves the previous README content so no manual editing
history is lost during standardization.

    # Chapter 19

    Chapter: 第十九章 羑里牢狱记忆

    Source mapping: PDF pages 369-386 / printed pages 357-374. Chapter 20 starts on PDF page 387.

    Generate study files from `practice/jianshang/`:

    ```bash
    python3 jianshang_tools.py split --source sources/136.txt --chapter chapter_19 --output chapter_19/source.txt
    python3 jianshang_tools.py table chapter_19/chapter_19_clean.txt --dictionary chapter_19/reading_terms.csv -o chapter_19/chapter_19_shengzibiao.txt --max-terms-percent 0.02 --min-terms 20
    python3 jianshang_tools.py pdf chapter_19/chapter_19_clean.txt --dictionary chapter_19/reading_terms.csv --bronze-dictionary chapter_04/bronze_terms.csv -o chapter_19/chapter_19_annotated.pdf --title '《翦商》第19章注音阅读版' --chapter-map sources/chapter_map.csv
    ```

    Generated files:

    - `chapter_19_clean.txt`: reviewed chapter text.
    - `chapter_19_shengzibiao.txt`: generated reading-term table.
    - `chapter_19_annotated.pdf`: annotated reading-practice PDF.

    ## Manual Editing

    Reviewed for recurring OCR issues: 羑里, 谮西伯, 徽纆, 入于坎窞, 簋贰, quote punctuation, and 易经 wording.

    2026-06-30 finetuning pass: added missing `（图）` markers to the 易卦卜甲 caption block, verified source-note sequence, and regenerated study outputs with flush-left subtitle styling.
