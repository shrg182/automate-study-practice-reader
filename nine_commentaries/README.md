# 📚 Nine Commentaries Study Materials

Related online source catalog: [中苏论战与九评文献目录](source_index/README.md), containing 49 Chinese-side, Nine Commentaries, and Soviet-side documents.

This directory is for processing Wu Lengxi's 《十年论战：1956-1966中苏关系回忆录》
in the same general style as the `practice/jianshang` workflow: extract text,
split it into stable reading units, clean and verify the text, build a focused
reading-term dictionary, generate a `shengzibiao`, and produce an annotated
reading PDF.

The important difference is that this source appears to be an image-based scan.
`pdftotext` does not return usable embedded text, so OCR must be treated as the
primary extraction step. The PDF remains the canonical visual reference for
page ranges, headings, section boundaries, unclear characters, punctuation,
footnotes, and scan artifacts.

---

## 1️⃣ Source

Primary PDF:

```text
吴冷西：十年论战——1956-1966中苏关系回忆录.pdf
```

Observed PDF facts:

- Title metadata: `十年论战（1956--1966）中苏关系回忆录(上、下册）`
- Pages: `950`
- Producer: `FreePic2Pdf - 1.05`
- Embedded text: none detected in the first pages
- Table of contents starts around PDF page 3

## 2️⃣ Search for a Better Source

Status as of 2026-07-04: no clearly better public PDF was found in a web search.
The available local PDF appears to be a low-quality photocopy with watermarks
and no embedded text, so OCR will need human correction.

Searches tried:

- `吴冷西 十年论战 1956 1966 中苏关系回忆录 PDF`
- `十年论战 1956-1966 中苏关系回忆录 吴冷西 pdf`
- `吴冷西 十年论战 下载`
- `十年论战 中苏关系回忆录 下载`
- `site:archive.org 十年论战 吴冷西`
- `site:books.google.com 十年论战 吴冷西`
- `site:worldcat.org 十年论战 吴冷西`
- Marxists.org Chinese index and site/PDF-library checks:
  - `https://www.marxists.org/chinese/index.html`
  - `https://www.marxists.org/chinese/pdf/marxism-library.htm`
  - `site:marxists.org/chinese 吴冷西 十年论战`
  - `site:marxists.org/chinese 十年论战`

Useful references found, but not a better OCR-ready PDF:

| Source                                 | What It Confirms                                                                                                 | Link                                                                                                                                  | Usefulness                                                                                                         |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| NodeBE mirror of programthink post     | Lists the book under political books / China / diplomacy and points to the current `programthink/books` catalog. | <https://nodebe4.github.io/opinion/2013-03-17/%E5%88%86%E4%BA%AB%E6%94%BF%E6%B2%BB%E7%B1%BB%E7%94%B5%E5%AD%90%E4%B9%A6-26%E6%9C%AC/>  | Confirms the programthink catalog source; not a direct cleaner text.                                               |
| `programthink/books` README.wiki       | Catalog entry for `十年论战——1956-1966中苏关系回忆录`, marked `简体PDF(扫描版)`.                                 | <https://github.com/programthink/books>                                                                                               | Confirms the available programthink version is also a scanned PDF, not an OCR-ready text.                          |
| Programthink Google Doc entry          | Provides a clean 17-chapter Chinese table of contents.                                                           | <https://docs.google.com/document/d/1n2oFDdH07nkL00akwA1xQU04hL3FVaza9PNfgU-vWBg/>                                                    | Used as the authoritative clean chapter-title list for `sources/unit_map.csv` and `sources/table_of_contents.csv`. |
| Wikipedia: 吴冷西                      | Lists 《十年论战--中苏关系回忆录》 among Wu Lengxi's works.                                                      | <https://zh.wikipedia.org/wiki/%E5%90%B4%E5%86%B7%E8%A5%BF>                                                                           | Bibliographic confirmation only.                                                                                   |
| Wikipedia: 九评苏共                    | Mentions the book as a memoir about the Sino-Soviet polemic.                                                     | <https://zh.wikipedia.org/wiki/%E4%B9%9D%E8%AF%84%E8%8B%8F%E5%85%B1>                                                                  | Historical context and title confirmation.                                                                         |
| Wikipedia: 中华人民共和国宪法 (1954年) | Cites `吴冷西. 十年论战: 1956-1966 中苏关系回忆录. 中央文献出版社. 2014.`                                        | <https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E5%AE%AA%E6%B3%95_%281954%E5%B9%B4%29> | Suggests a 2014 Central Party Literature Press edition to look for in libraries or book databases.                 |
| Wikipedia: 中苏交恶                    | Uses the book in references/context for Sino-Soviet relations.                                                   | <https://zh.wikipedia.org/wiki/%E4%B8%AD%E8%8B%8F%E4%BA%A4%E6%81%B6>                                                                  | Context and cross-checking names/events.                                                                           |
| Marxists.org Chinese index             | Provides a Chinese Marxist text/PDF library and a site search entry point.                                       | <https://www.marxists.org/chinese/index.html>                                                                                         | Checked as a possible source; no clear copy of Wu Lengxi's 《十年论战》 found.                                     |
| Marxists.org PDF library               | Lists core Marx/Engels/Lenin PDF collections.                                                                    | <https://www.marxists.org/chinese/pdf/marxism-library.htm>                                                                            | Checked for the book; no matching item found.                                                                      |

Next places to check manually:

- university library catalogs;
- WorldCat or Chinese library catalogs by title and author;
- used-book listings for a cleaner 2014 Central Party Literature Press edition;
- CNKI/Duxiu/Chaoxing access if available through a library account.

## Target Output Shape

Use a directory layout close to JianShang, but name units by chapter and section
because this book is long and already divided into sections.

```text
practice/nine_commentaries/
  README.md
  nine_commentaries_tools.py
  吴冷西：十年论战——1956-1966中苏关系回忆录.pdf
  sources/
    unit_map.csv
    table_of_contents.csv
    ocr_pages/
      page_0001.txt
      page_0001.png
    full_ocr_raw.txt
    full_ocr_clean.txt
    confusing_terms.tsv
  front_matter/
    source.txt
    front_matter_clean.txt
    reading_terms.csv
    review_notes.tsv
    front_matter_shengzibiao.txt
    README.md
  table_of_contents/
    README.md
    index.html
    table_of_contents.txt
  chapter_01/
    source.txt
    chapter_01_clean.txt
    editor.html
    pdf_pages/
    reading_terms.csv
    review_notes.tsv
    chapter_01_shengzibiao.txt
    chapter_01_annotated.pdf
    README.md
  chapter_01_section_01/
    source.txt
    chapter_01_section_01_clean.txt
    reading_terms.csv
    review_notes.tsv
    chapter_01_section_01_shengzibiao.txt
    chapter_01_section_01_annotated.pdf
```

Recommended unit rule:

- Use whole chapters when the chapter is short enough for one reading packet.
- Use sections for long chapters, especially if a chapter has many named
  sections in the table of contents.
- Keep each generated packet to a manageable size for review and annotation.

## Processing Scheme

Run commands from:

```bash
cd practice/nine_commentaries
```

### 1. Build Page Images

Render every PDF page to a stable image folder before OCR. Keep these images so
manual review can always cite a PDF page and inspect the original scan.

```bash
mkdir -p sources/page_images
pdftoppm -png -r 300 \
  '吴冷西：十年论战——1956-1966中苏关系回忆录.pdf' \
  sources/page_images/page
```

Use `300` DPI as the default. If OCR is poor on dense pages, test `400` DPI on a
small range before rerunning the whole book.

### 2. OCR Each Page

Use Tesseract with simplified Chinese and English because the book mixes
Chinese prose, Russian/Soviet names, dates, abbreviations, and page headers.

```bash
mkdir -p sources/ocr_pages
for image in sources/page_images/page-*.png; do
  base=$(basename "$image" .png)
  tesseract "$image" "sources/ocr_pages/$base" -l chi_sim+eng --psm 6
done
```

For pages with unusual layout, retry individually:

```bash
tesseract sources/page_images/page-0003.png stdout -l chi_sim+eng --psm 4
tesseract sources/page_images/page-0003.png stdout -l chi_sim+eng --psm 11
```

Keep raw OCR unchanged. Corrections belong in clean files, not in the raw OCR
archive.

### 3. Create the Unit Map

Create `sources/unit_map.csv` from the table of contents and verified PDF page
positions.

Suggested columns:

```csv
unit_id,chapter,section,title,pdf_start,pdf_end,printed_start,printed_end,status,notes
chapter_01,1,,苏共“20大”的震动,3,,1,33,draft,
chapter_01_section_01,1,1,“破题”,,,"1","6",draft,
```

The table of contents gives printed page numbers in parentheses. Verify the
corresponding PDF page numbers manually because front matter and scan pages
shift the count.

Current mapping convention:

- `sources/table_of_contents.csv` preserves the processed chapter/section TOC.
- `sources/unit_map.csv` is the working extraction map.
- Clean chapter titles come from the programthink Google Doc entry.
- Section titles and printed page starts come from the scanned PDF TOC.
- For the body text, the confirmed offset is `PDF page = printed page + 8`.
- PDF pages `949-950` are metadata/bookmark pages; the final body page is PDF
  page `948`, corresponding to printed page `940`.

### 4. Split Source Text

Concatenate raw OCR into `sources/full_ocr_raw.txt`, then split by `unit_map.csv`
into unit folders.

Each unit should start with:

```text
source.txt
chapter_XX_clean.txt
reading_terms.csv
review_notes.tsv
README.md
```

`source.txt` is the raw unit extract. `*_clean.txt` is the reviewed reading text
used for output generation.

### 5. Clean and Verify OCR

Follow the JianShang editing discipline, but tune the checks for modern
political memoir prose rather than ancient-text artifacts.

Clean text rules:

- Remove running headers, scan page numbers, library stamps, barcode noise, and
  OCR debris.
- Normalize Chinese punctuation and line wrapping.
- Preserve chapter and section headings as flush-left lines.
- Preserve quoted document titles, speech titles, party names, and date ranges.
- Verify suspicious names against the PDF before correcting them.
- Do not silently guess unreadable text; mark it with `〔待核：...〕`.
- Use `□` only when the original scan is visibly unreadable.

Common OCR risk areas:

| Difficulty                              | Likely OCR Symptom                                                                       | Examples to Review                                                       | Human Editing Action                                                                    |
| --------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| Watermarks and library marks            | Random dark blocks, stamps, barcode text, or unrelated numbers enter the OCR body.       | Cover page barcode; page-top library marks; large watermark shadows.     | Delete non-book artifacts from clean text; keep only if it is part of the printed page. |
| Low-contrast photocopy text             | Characters drop strokes or merge with neighboring marks.                                 | `赫` read as `郝`; `晓` read as unrelated characters; `论` read as `伦`. | Compare against page image before correcting names or titles.                           |
| Page headers and page numbers           | Running title `十年论战`, chapter headers, or printed page numbers appear mid-paragraph. | `十年论战`, isolated `1`, `2`, etc.                                      | Remove from body; retain page mapping in `unit_map.csv`.                                |
| Table-of-contents dotted leaders        | Dots become Latin letters, punctuation noise, or fake words.                             | `...... (34)` becoming `eee C34)` or similar.                            | Do not OCR-split units from raw TOC alone; manually transcribe TOC rows.                |
| Soviet and Eastern European names       | Personal and place names become plausible but wrong Chinese words.                       | 赫鲁晓夫, 米高扬, 苏斯洛夫, 莫洛托夫, 匈牙利, 南斯拉夫, 莫斯科.          | Maintain `sources/confusing_terms.tsv`; verify every new name once.                     |
| Political terms                         | Repeated ideological terms are misread in ways that still look grammatical.              | 教条主义, 修正主义, 反修, 反苏, 兄弟党, 总路线, 和平共处.                | Add canonical terms to `reading_terms.csv` and use search checks for variants.          |
| Quotation marks and book/article titles | Chinese quotes are lost or converted to ASCII marks; title boundaries blur.              | 《人民日报》, 《红旗》, “九评”, “破题”.                                  | Normalize punctuation after verifying the original title boundary.                      |
| Dates and meeting numbers               | Years, session numbers, and article numbers are mistaken for footnotes or page numbers.  | 1956, 1966, 苏共二十大, 二十二大, 81国会议.                              | Preserve dates and meeting numbers in body; do not treat them as notes unless verified. |
| Section headings                        | Headings are merged into the preceding paragraph or broken across lines.                 | `第一节 “破题”`; `第二节 评论赫鲁晓夫报告`.                              | Keep headings flush-left and map them in `unit_map.csv`.                                |
| Mixed Chinese/Latin OCR debris          | Tesseract inserts English-looking fragments into Chinese text.                           | `eee`, `Decne`, `nna`, random capitals.                                  | Flag with automated regex and review against page images.                               |
| Footnotes or source notes               | Note markers, page references, and citation numbers become ordinary body text.           | Parenthesized numbers, superscripts, source-note blocks.                 | Mark explicit source notes only after checking the scan.                                |
| Long dense paragraphs                   | Line wraps produce missing punctuation, duplicated fragments, or joined sentences.       | Diplomatic narrative paragraphs and quoted reports.                      | Clean paragraph by paragraph; avoid bulk substitutions without review.                  |

### 6. Review Table

Use `review_notes.tsv` for uncertain OCR and historical-name checks.

Required columns:

```tsv
source	current_text	issue	action
PDF p.003 / printed p.1	苏共“20大”的震动	TOC heading; verify exact punctuation	checked against PDF before final split
```

This replaces JianShang's `oracle_review.tsv`. The function is the same:
visible uncertainty should be tracked instead of hidden.

### 7. Reading-Term Dictionary

Use the same dictionary structure as JianShang:

```csv
term,pinyin,type,annotation
```

Recommended `type` values:

- `person`: political figures, diplomats, party leaders.
- `place`: countries, cities, regions.
- `organization`: parties, ministries, newspapers, conferences.
- `event`: major meetings, crises, speeches, campaigns.
- `concept`: ideological and diplomatic concepts.
- `text`: articles, reports, declarations, speeches, books.
- `rare_word`: uncommon characters or difficult written forms.
- `added`: manually retained term that should survive generation caps.

Example rows:

```csv
赫鲁晓夫,hè lǔ xiǎo fū,person,苏联领导人，1950年代中苏关系中的核心人物。
苏共二十大,sū gòng èr shí dà,event,1956年苏联共产党第二十次代表大会。
修正主义,xiū zhèng zhǔ yì,concept,中苏论战中的核心政治批判词。
```

### 8. Generate Shengzibiao and Annotated PDF

Reuse or adapt `practice/jianshang/jianshang_tools.py`.

Recommended implementation path:

1. Copy `jianshang_tools.py` to `nine_commentaries_tools.py`.
2. Rename project defaults and titles.
3. Replace the bronze/ancient-text specific labels with modern-history review
   labels.
4. Keep the useful shared commands: `table`, `pdf`, `fix-punctuation`,
   `check-pdf`.
5. Add OCR-specific commands: `render-pages`, `ocr-pages`, `split-units`.

Expected commands after adaptation:

```bash
python3 nine_commentaries_tools.py table \
  chapter_01/chapter_01_clean.txt \
  --dictionary chapter_01/reading_terms.csv \
  -o chapter_01/chapter_01_shengzibiao.txt \
  --max-terms-percent 0.02 \
  --min-terms 25

python3 nine_commentaries_tools.py pdf \
  chapter_01/chapter_01_clean.txt \
  --dictionary chapter_01/reading_terms.csv \
  --review-notes chapter_01/review_notes.tsv \
  -o chapter_01/chapter_01_annotated.pdf \
  --title '《十年论战》第一章注音阅读版' \
  --unit-map sources/unit_map.csv
```

### 9. Quality Checks

Run after each meaningful edit:

```bash
python3 nine_commentaries_tools.py fix-punctuation chapter_01/chapter_01_clean.txt --check
python3 nine_commentaries_tools.py check-pdf \
  chapter_01/chapter_01_clean.txt \
  --pdf '吴冷西：十年论战——1956-1966中苏关系回忆录.pdf' \
  --start-page START_PAGE \
  --end-page END_PAGE
```

Checks should cover:

- page range exists in `sources/unit_map.csv`;
- headings match the table of contents;
- OCR debris has been removed;
- suspicious mixed Latin/CJK fragments are reviewed;
- dates and meeting numbers are preserved;
- `review_notes.tsv` contains unresolved uncertain readings;
- generated `shengzibiao` and annotated PDF complete without errors.

## Chapter README Template

Each unit README should mirror the JianShang chapter template, with these
section names:

```text
# [Unit ID]: [Title]

## Unit Status
## Files
## Source Mapping
## Generate Outputs
## Quality Checks
## Editing Standards
## Current Editing Pass
## Confirmed Corrections
## Pending Manual Review
## Review Notes Table
## Reading-Term Dictionary Notes
## Regeneration Log
## Final Checklist
```

## Pilot Pass

Start with Chapter 1 because the contents page clearly shows its printed page
range and section structure:

- 第一章 苏共“20大”的震动
- 第一节 “破题”
- 第二节 评论赫鲁晓夫报告
- 第三节 怎样看待斯大林
- 第四节 探索正确道路
- 第五节 文章的要点
- 第六节 必要的说明

Pilot goals:

- confirm the PDF-to-printed-page offset;
- compare OCR quality at 300 and 400 DPI;
- define `unit_map.csv` conventions;
- adapt the JianShang tool only as much as needed;
- generate one complete annotated reading packet before scaling to the full
  950-page PDF.

Current pilot status:

- Front matter has been processed as a support unit: PDF pages `1-8`.
- Chapter 1 has been OCRed as a high-risk draft.
- Confirmed Chapter 1 range: PDF pages `9-41`, printed pages `1-33`.
- Chapter 2 starts on PDF page `42`.
- All 17 chapter-level ranges have been mapped in `sources/unit_map.csv`.
- The full chapter/section table of contents has been processed into
  `sources/table_of_contents.csv`.
- A browser-readable table of contents page has been generated at
  `table_of_contents/index.html`.
- Page-level OCR files are in `sources/ocr_pages/page-009.txt` through
  `page-041.txt`.
- Chapter working files are in `chapter_01/`.
- Chapter 1 browser editor is available at `chapter_01/editor.html`.
- Annotated PDF generation is deferred until human OCR correction is complete.

## Copyright

Use the PDF and generated materials for personal study processing only. Do not
redistribute OCR text, cleaned chapter text, or generated annotated PDFs.

