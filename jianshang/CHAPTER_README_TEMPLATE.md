# Chapter XX: [Chapter Title]

This folder contains the working files, generation commands, quality checks,
and manual editorial notes for Chapter XX of the 《翦商》 study-material
project.

## Chapter Status

- Status: `draft | reviewed | generated | needs-manual-review | complete`
- Last updated: `YYYY-MM-DD`
- Main reviewer/editor: `[name or Codex]`
- Output regenerated after latest edits: `yes | no`
- Remaining risk level: `low | medium | high`

Short status note:

```text
[One or two sentences explaining the current state of the chapter.]
```

## Files

- `source.txt`: chapter text split from `sources/136.txt`.
- `chapter_XX_clean.txt`: reviewed chapter text used for generation.
- `reading_terms.csv`: curated pinyin and annotation dictionary.
- `oracle_review.tsv`: optional manual review table for difficult ancient text,
  oracle-bone text, bronze inscriptions, captions, diagrams, and OCR-resistant
  passages.
- `chapter_XX_shengzibiao.txt`: generated reading-term table.
- `chapter_XX_annotated.pdf`: generated annotated PDF.
- `reading_notes.md`: optional reader-supplied personal notes, rendered as the
  PDF “读书札记” appendix when `--reading-notes` is supplied.

## Source Mapping

- Chapter ID: `chapter_XX`
- Title: `[Chinese chapter title]`
- Source PDF pages: `[PDF_START]-[PDF_END]`
- Printed pages: `[PRINT_START]-[PRINT_END]`
- Previous chapter ends: `[optional]`
- Next chapter starts: `[optional]`

Source mapping should match `sources/chapter_map.csv`.

## Generate Outputs

Run from `practice/jianshang/`.

Generate the shengzibiao:

```bash
python3 jianshang_tools.py table \
  chapter_XX/chapter_XX_clean.txt \
  --dictionary chapter_XX/reading_terms.csv \
  -o chapter_XX/chapter_XX_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 20
```

Use a larger `--min-terms` value, such as `30`, when rare ancient-text
characters would otherwise be excluded by the term cap.

Generate the annotated PDF:

```bash
python3 jianshang_tools.py pdf \
  chapter_XX/chapter_XX_clean.txt \
  --dictionary chapter_XX/reading_terms.csv \
  --bronze-dictionary chapter_04/bronze_terms.csv \
  --ancient-review chapter_XX/oracle_review.tsv \
  --reading-notes chapter_XX/reading_notes.md \
  -o chapter_XX/chapter_XX_annotated.pdf \
  --title '《翦商》第XX章注音阅读版' \
  --chapter-map sources/chapter_map.csv \
  --min-terms 20
```

If the chapter does not use `oracle_review.tsv`, remove the
`--ancient-review` line.
If the chapter has no reader notes, `reading_notes.md` may remain as the
comment-only template; it will not render any note entries.

## Quality Checks

Run after every meaningful edit and after regenerating the PDF:

```bash
python3 jianshang_tools.py fix-punctuation chapter_XX/chapter_XX_clean.txt --check
python3 jianshang_tools.py lint-images chapter_XX/chapter_XX_clean.txt
python3 jianshang_tools.py check-pdf chapter_XX/chapter_XX_clean.txt
```

To apply punctuation cleanup:

```bash
python3 jianshang_tools.py fix-punctuation chapter_XX/chapter_XX_clean.txt --in-place
```

Optional PDF/OCR comparison:

```bash
python3 jianshang_tools.py check-pdf \
  chapter_XX/chapter_XX_clean.txt \
  --pdf 翦商.pdf \
  --start-page [PDF_START] \
  --end-page [PDF_END]
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
- Use explicit footnote markers in the body as `[[fn:number]]` only after
  verifying that the number is a true source note.
- Keep generated PDF footnote display consistent with the project convention.
- Add rare or ambiguous readings to `reading_terms.csv`.
- Also add or reconcile each vocabulary entry in the project-wide master
  vocabulary table; chapter dictionaries are chapter-specific working subsets.
- Add or reconcile bronze vessel, weapon, fitting, and related object names in
  the project-wide bronze-item-name master table as well as any chapter subset.
- Add unresolved ancient text, bronze inscriptions, oracle-bone text, and
  difficult OCR cases to `oracle_review.tsv`.
- Put personal interpretive notes in `reading_notes.md`, not in
  `chapter_XX_clean.txt`; they render as a separate PDF appendix and are not
  treated as source text.

## Manual Editing

Use this section as the active working notebook for chapter-specific edits. Add
new user corrections here first; after they are applied and verified, summarize
them under `Confirmed Corrections` and record the regeneration under
`Regeneration Log`.

### Current Editing Pass

- Date: `YYYY-MM-DD`
- Editor: `[manual / Codex / name]`
- Scope:
  - `[OCR correction, pinyin adjustment, caption repair, footnote alignment,
    ancient-text review, etc.]`
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

### [Issue Title]

Current text:

```text
[current uncertain text]
```

Issue:

```text
[what is uncertain: OCR error, missing character, doubtful reading, caption
location, source-note mismatch, etc.]
```

Action needed:

- `[check source PDF page]`
- `[check reliable edition / inscription corpus / oracle-bone reference]`
- `[decide whether to correct body text or keep in oracle_review.tsv]`

Status: `open | resolved | deferred`

## Ancient Text Review Table

Use `oracle_review.tsv` for passages that should appear in the generated
“疑难甲骨文字词校读表”.

Required columns:

```tsv
source	current_text	issue	action
```

Rows added or updated in this chapter:

- `[source or passage]`: `[brief reason]`

## Reading-Term Dictionary Notes

Important additions to `reading_terms.csv`:

- `[term]`, `[pinyin]`, `[type]`: `[reason]`

Master-table synchronization:

- General vocabulary master updated: `yes | no | not applicable`
- Bronze-item-name master updated: `yes | no | not applicable`

Terms requiring special care:

- `[term]`: `[multiple readings, chapter-specific pronunciation, or conflict
with bronze_terms.csv]`

Term-cap note:

- Use `--min-terms [number]` for this chapter because `[reason]`.

## Image and Caption Review

- Captions checked against PDF: `yes | no`
- All captions end with `（图）`: `yes | no`
- Caption flow check passed: `yes | no`
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

### YYYY-MM-DD

- Edited:
  - `[file or passage]`
- Updated:
  - `chapter_XX_clean.txt`
  - `reading_terms.csv`
  - `oracle_review.tsv`
  - `README.md`
- Regenerated:
  - `chapter_XX_shengzibiao.txt`
  - `chapter_XX_annotated.pdf`
- Checks:
  - `lint-images`: `pass/fail`
  - `check-pdf`: `pass/fail`
- Notes:
  - `[any remaining risks or manual follow-up]`

## Final Checklist

- [ ] `chapter_XX_clean.txt` reviewed against source text.
- [ ] PDF page range verified in `sources/chapter_map.csv`.
- [ ] Image captions end with `（图）`.
- [ ] Caption flow check passes.
- [ ] Footnotes are aligned and checked.
- [ ] `reading_terms.csv` covers difficult names, places, artifacts, and rare
      characters.
- [ ] Chapter-specific pronunciation conflicts are resolved.
- [ ] `oracle_review.tsv` records unresolved ancient text or inscription issues.
- [ ] Shengzibiao regenerated.
- [ ] Annotated PDF regenerated.
- [ ] `check-pdf` passes.
- [ ] Remaining manual-review items are clearly listed.
