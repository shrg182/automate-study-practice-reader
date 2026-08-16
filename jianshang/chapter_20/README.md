# Chapter 20: 第二十章 翦商与《易经》的世界观

This folder contains the working files, generation commands, quality checks, and
manual editorial notes for `chapter_20` of the 《翦商》 study-material project.

## Chapter Status

- Status: `editor prepared`
- Last updated: `2026-07-24`
- Main reviewer/editor: `manual + Codex`
- Output regenerated after latest edits: `yes`
- Remaining risk level: `medium`

Short status note:

```text
第二十章 翦商与《易经》的世界观 has an 18-page manual editor ready for review. Its aligned source notes, ancient-text review table, and reading-notes appendix are preserved.
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_20_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary. Current entries: `38`.
- `oracle_review.tsv`: manual review table for difficult ancient text, oracle-bone text, bronze inscriptions, diagrams, and OCR-resistant passages.
- `chapter_20_shengzibiao.txt`: generated reading-term table.
- `chapter_20_annotated.pdf`: generated annotated PDF.
- `reading_notes.md`: optional reader-supplied personal notes, rendered as the PDF “读书札记” appendix.
- `editor.html`: 18-page manual editor with explicit reader, physical-PDF, printed-page, and annotated-PDF numbering.
- `chapter_20_clean_edited.txt`: page-aligned editor seed and TXT export target.
- `chapter_20_edit_log.txt`: editor activity-log export target.
- `pdf_pages/`: source-page images for physical PDF pages 387–404.

## Source Mapping

- Chapter ID: `chapter_20`
- Title: `第二十章 翦商与《易经》的世界观`
- Original reader pages: `389-406`
- Physical source PDF pages: `387-404`
- Printed pages: `375-392`
- Annotated PDF pages: `1-19` (independently reflowed; not mapped one-to-one to source pages)
- Mapping note: original reader pages are printed pages plus 14; physical source PDF pages are printed pages plus 12.

Source mapping should match `sources/chapter_map.csv`.

### 2026-07-24 — Manual editor preparation

- Generated all 18 source-page images and the Chapter 20 browser editor.
- Seeded the editor with explicit page boundaries from reader page 389 through 406.
- Enabled header shortcuts for 注音、编者注、按语、待核 and 用户札记, plus the full marker composer in 编辑札记.
- Included the synchronized reading terms, bronze terms, two-row ancient-text/OCR review table, reading-notes appendix, user-notes panel, and book-wide reference links.
- Preserved all nine already aligned source-note markers.

### 2026-07-24 — Manual review import

- Imported the matching 01:51 TXT export and 19-entry editor log from `~/Downloads`.
- Preserved six inline 按语, seven user 札记, and one general 编者注.
- Moved the manually entered readings for 戡 and 杞 into `reading_terms.csv` with tone-mark pinyin and removed redundant numeric pinyin from the clean text.
- Kept 按语 as muted inline commentary in the PDF.
- Changed PDF handling for 札记: the prose now carries compact `[札1]`–`[札7]` references, while the complete notes appear in a dedicated 用户札记 appendix with clickable links and cleaned Markdown formatting.
- Kept the general 编者注 in its own PDF section, reflecting that this edition prioritizes pronunciation rather than content discussion.
- Regenerated the vocabulary table, annotated PDF, editor, ancient-text review panel, reading-notes appendix, and shared reference outputs.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_20/chapter_20_clean.txt \
  --dictionary chapter_20/reading_terms.csv \
  -o chapter_20/chapter_20_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 38
```

Use a larger `--min-terms` value when rare ancient-text characters would
otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_20/chapter_20_clean.txt \
  --dictionary chapter_20/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  --ancient-review chapter_20/oracle_review.tsv \
  --reading-notes chapter_20/reading_notes.md \
  -o chapter_20/chapter_20_annotated.pdf \
  --title '《翦商》第20章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 38
```

This chapter currently uses `oracle_review.tsv`.
It also renders `reading_notes.md` as an optional “读书札记” section.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py fix-punctuation chapter_20/chapter_20_clean.txt --check
python3 jianshang_tools.py lint-images chapter_20/chapter_20_clean.txt
python3 jianshang_tools.py check-pdf chapter_20/chapter_20_clean.txt
```

To apply punctuation cleanup:

```bash
python3 jianshang_tools.py fix-punctuation chapter_20/chapter_20_clean.txt --in-place
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_20/chapter_20_clean.txt \
  --pdf 翦商.pdf \
  --start-page 387 \
  --end-page 404
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
- For 周易 material, use standard trigram symbols for clearly identifiable卦象; six-line hexagrams may be represented as `上卦/下卦` trigram pairs when single-codepoint hexagrams render as empty boxes in PDF output. Keep uncertain ancient/numeric inscriptions in `oracle_review.tsv`.
- Put personal interpretive notes in `reading_notes.md`, not in `chapter_20_clean.txt`; they render as a separate PDF appendix and are not treated as source text.

## Manual Editing

Use this section as the active working notebook for chapter-specific edits. Add
new user corrections here first; after they are applied and verified, summarize
them under `Confirmed Corrections` and record the regeneration under
`Regeneration Log`.

### Current Editing Pass

- Date: `2026-07-02`
- Editor: `manual + Codex`
- Scope:
  - `周易卦象 OCR correction`
  - `pinyin/readability term additions`
  - `footnote marker alignment`
  - `manual ancient-text review tracking`
  - `user-supplied OCR corrections for numeric hexagram text and classical citation`
  - `reader note appendix trial`
  - `punctuation spacing normalization`
- Output regenerated after this pass: `yes`

### User Corrections

- `[exact user-provided correction or request]`
- 用甲骨预测，称为“卜”
；用草棍预测，则称为“筮（shì）”。“筮二上面的“竹”字头代表占
算用的草（竹）棍，下面的“巫”字表示只有沟通鬼神的巫师才有占算能力。

用甲骨预测，称为“卜”
；用草棍预测，则称为“筮（shì）”。“筮二上面的“竹”字头代表占
算用的草（竹）棍，下面的“巫”字表示只有沟通鬼神的巫师才有占算能力。[1]

- 其囚美里
- 其囚羑里 （note: OCR error; the original text is “羑里” not “美里”）

- 震下坎上，叫屯卦，卦象是H；坎下艮上，叫蒙卦，卦象是鬓。
- 震下坎上，叫屯卦，卦象是(OCR error)；坎下艮上，叫蒙卦，卦象是(OCR error)。（note: OCR error; the original text is the images of “屯卦” and “蒙卦” ）

- 周易系统中有大量卦象符号；可确认者应使用标准八卦/六十四卦符号，无法确认的古文字或数字卦仍需人工核对。
- Reference supplied for symbol system: https://en.wikipedia.org/wiki/I_Ching
- Additional hexagram reference: https://motheringchange.com/hexagrams/
- Local lookup table: `../sources/hexagram_reference.tsv`

- "六七，I九 六对应“阴阳阴阳阴阴”
- “六七八九六八”对应“阴阳阴阳阴阴” (note: OCR error; the original text is “六七八九六八” not “六七，I九 六”)

- 《易传·系辞》
- 《易传·系辞》 (note: OCR error; the original text is “《易传·系辞》” not “《易传·系辞》”)

- 坎离颐大过中孚小过
- 坎 离 颐 大过 中孚 小过 (note: in case of OCR could identify the individual hexagrams, add spaces for clarity)

- 莫不周备，缰在爻卦之中矣.
- 莫不周备，缊在爻卦之中矣. 
  

### Applied Edits

- `筮二` -> `筮` (PDF annotation renders `shì`)
- `其囚美里` ->  (PDF annotation renders )`其囚羑里`
- `乾三坤三；坎笠离三；震三艮三；巽三兑三` ->  (PDF annotation renders )`乾☰ 坤☷；坎☵ 离☲；震☳ 艮☶；巽☴ 兑☱`
- `卦象是H；卦象是鬓` ->  (PDF annotation renders )`卦象是☵/☳；卦象是☶/☵`
- `同人卦的卦象图案——3o ... 离（王） ... 乾（三）o` ->  (PDF annotation renders )`同人卦的卦象图案——☰/☲ ... 离（☲） ... 乾（☰）`
- `■Hmm / ■MM ■一 / —■ ■■ / 乾坤` ->  (PDF annotation renders )`乾☰/☰ 坤☷/☷`
- `屯卦言 ... 震三 ... 坎三；蒙卦集 ... 艮三` ->  (PDF annotation renders )`屯卦☵/☳ ... 震☳ ... 坎☵；蒙卦☶/☵ ... 艮☶`
- `无妄大言` ->  (PDF annotation renders )`无妄☰/☳ 大畜☶/☰`
- `"六七，I九六` -> `“六七八九六八”`
- `《易传・系辞》` -> `《易传·系辞》`
- `坎离颐大过中孚小过` -> `坎 离 颐 大过 中孚 小过`
- `缰在爻卦之中矣` -> `缊在爻卦之中矣`
- Inline source-note numbers `1-9` ->  (PDF annotation renders )`[[fn:1]]` etc. where verified in body text.

### Editing Notes

- The supplied I Ching reference explains that the system has 64 hexagrams, each corresponding to six-line patterns; this supports replacing clear OCR artifacts with trigram-based symbols rather than roman letters or random glyphs.
- The Mothering Change hexagram reference is useful for lookup because it presents each hexagram as two trigrams; the local `sources/hexagram_reference.tsv` table records this mapping for repeatable editing.
- The generator keeps the main PDF font in the usual Songti style and applies a symbol-font fallback only to trigram glyphs. Single-codepoint hexagrams did not render reliably, so six-line examples are expressed as `上卦/下卦` trigram pairs.
- The digital symbols are used only where the卦名/context clearly identifies the symbol.
- The numeric oracle-bone example was corrected to `六七八九六八` per the user-provided source check and remains in `oracle_review.tsv` as a traceable OCR-sensitive case.
- `缰在爻卦之中矣` was corrected to `缊在爻卦之中矣` per the user-provided source check.

## Confirmed Corrections

Record applied edits here. Keep the old form and the corrected form visible.

### Names and Titles

- `[old form]` ->  (PDF annotation renders )`[corrected form]`

### Terms and Pronunciation

- `[old pinyin or OCR form]` ->  (PDF annotation renders )`[correct form with pinyin if needed]`
- 东周时的学者说，这是宇宙间的八大元素：乾代表天，坤代表地; 坎代表水，离代表火;
震代表雷，艮代表山；巽代表风，兑代表泽（沼泽）o（《周易正义•说卦卷九》） 
-> 东周时的学者说，这是宇宙间的八大元素：乾代表天，坤代表地; 坎代表水，离代表火; 震代表雷，艮代表山；巽代表风，兑代表泽（沼泽）。（《周易正义•说卦卷九》）

### Bronze, Vessel, and Artifact Terms

- `[old form]` ->  (PDF annotation renders )`[corrected form]`

### Image Captions

- `[caption before edit]` ->  (PDF annotation renders )`[caption after edit]（图）`

### Classical or Ancient Text

```text
“六七八九六八”对应“阴阳阴阳阴阴”
《易传·系辞》
莫不周备，缊在爻卦之中矣。
```

Notes:

- Corrected per user-provided source checks in this editing pass.
- The numeric hexagram example remains listed in `oracle_review.tsv` as an OCR-sensitive trace item; the resolved `缊在` citation no longer needs a review row.

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

- Check the source PDF pages `387-404`.
- Check reliable editions, inscription corpora, or oracle-bone references where relevant.
- Decide whether to correct body text or keep the issue in `oracle_review.tsv`.

Status: `resolved for this pass`

## Ancient Text Review Table

Use `oracle_review.tsv` for passages that should appear in the generated
“疑难甲骨文字词校读表”.

Required columns:

```tsv
source	current_text	issue	action
```

Rows currently present: `2`.

Rows added or updated in this chapter:

- `数字卦甲骨刻辞示例`: updated current text to `六七八九六八` and marked the OCR correction as applied.
- Removed the resolved `缰在` review row after correcting the body text to `缊在`.

## Reading-Term Dictionary Notes

Important additions to `reading_terms.csv`:

- `颐`, `yí`, `text`: hexagram name in the self-symmetry list.
- `大过`, `dà guò`, `text`: hexagram name in the self-symmetry list.
- `中孚`, `zhōng fú`, `text`: hexagram name in the self-symmetry list.
- `小过`, `xiǎo guò`, `text`: hexagram name in the self-symmetry list.
- `缊`, `yùn`, `rare_word`: corrected classical citation term.

Terms requiring special care:

- `屯`: chapter dictionary keeps `tún`, following the existing local reading convention.
- `缊`: review against preferred classical reading if a later edition-specific pinyin standard is adopted.

Term-cap note:

- Current generation command uses `--max-terms-percent 0.02 --min-terms 38`; this pass keeps all 38 chapter dictionary entries available in the generated table.

## Image and Caption Review

- Captions checked against PDF: `not in this pass`
- All captions end with `（图）`: `not separately checked in this pass`
- Caption flow check passed: `yes`
- Captions needing manual PDF comparison:
  - `[caption / page / issue]`

## Footnote Review

- Body markers count: `9`
- Source notes count: `9`
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

### 2026-07-02

- Applied user-supplied Chapter 20 OCR corrections for `六七八九六八`, `《易传·系辞》`, `坎 离 颐 大过 中孚 小过`, and `缊在爻卦之中矣`.
- Added reading terms for `颐`, `大过`, `中孚`, `小过`, and `缊`.
- Updated `oracle_review.tsv` to keep only the still trace-worthy OCR-sensitive rows.
- Added `reading_notes.md` and rendered it as the optional PDF “读书札记” section.
- Added optional `记录者`/`记录日期` and `处理者`/`处理日期` metadata fields to the reading note and verified they render as separate note metadata lines.
- Ran `fix-punctuation` to normalize ASCII punctuation in Chinese prose and trim spaces around punctuation.
- Updated PDF rendering to keep Chinese closing punctuation from starting a new visual line; switched to renderer `nobr` markup after invisible joiner characters displayed as square boxes in Preview selection.
- Regenerated outputs in this pass: `yes`.
- Checks run in this pass: `fix-punctuation --check`, `lint-images`, `check-pdf`.
- Check result: punctuation spacing, footnote marker, caption flow, and suspicious OCR-token checks all passed.

## Final Checklist

- [x] `chapter_20_clean.txt` reviewed or available for review.
- [x] PDF page range recorded in `sources/chapter_map.csv`.
- [ ] Image captions end with `（图）`.
- [x] Caption flow check passes.
- [x] Footnotes are aligned and checked.
- [x] `reading_terms.csv` exists.
- [x] Chapter-specific pronunciation conflicts are resolved.
- [x] `oracle_review.tsv` records unresolved ancient text or inscription issues when needed.
- [x] Shengzibiao generated.
- [x] Annotated PDF generated.
- [x] `check-pdf` passes.
- [x] Remaining manual-review items are clearly listed.
