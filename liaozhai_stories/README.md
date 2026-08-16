# 📖 Liaozhai Story Study Tools

This folder contains a small workflow for making study materials from
selected stories in 《聊斋志异》. It can download a story page, extract the
original classical Chinese text, generate a rare-word table, and create an
annotated PDF with inline pinyin.

---

## 1️⃣ What The Program Makes

For each story, the program can produce:

- A clean `.txt` file containing the selected story text.
- A `阅读词表` text file listing focused rare or classical words found in the story.
- An annotated PDF where matching words are shown with inline pinyin, such as
  `醵（jù）`.
- A self-contained rich-text `editor.html` with the shared Preview-style
  highlight/underline menu, bold formatting, annotations, notes, browser
  saving, and JSON export.

The current story folders are:

- `lupan/` for 《陆判》
- `yingning/` for 《婴宁》
- `laoshan_daoshi/` for 《劳山道士》
- `nie_xiaoqian/` for 《聂小倩》

## 2️⃣ How It Is Organized

The reusable logic now lives in:

```text
liaozhai_tools.py
```

Each story folder keeps only lightweight wrapper scripts and story-specific
data:

```text
download_liaozhai_text.py
make_liaozhai_rare_word_table.py
make_liaozhai_annotated_pdf.py
build_editor.py
*_rare_words.csv
*.txt
*_shengzibiao.txt
*_annotated.pdf
editor.html
```

The CSV dictionary files use this format:

```csv
term,pinyin,annotation
醵,jù,众人凑钱；常指凑钱饮酒。
```

---

## 3️⃣ How It Works

1. The downloader fetches a Liaozhai web page with `requests`.
2. `BeautifulSoup` removes scripts, styles, and page chrome, then extracts
   readable text.
3. The section extractor first reads explicitly labelled `data-section="原文"`
   paragraphs on newer pages, then falls back to markers such as `〖原文〗`
   and `〖翻译〗` on older pages.
4. The rare-word table generator loads a CSV dictionary and checks which terms
   appear in the story.
5. The PDF generator scans the story with longest-match logic, annotating
   longer phrases before shorter single-character entries.
6. By default, each term is annotated only on its first occurrence, keeping the
   story readable while preserving the full story dictionary.
7. 4️⃣ `reportlab` builds the final PDF and appends a reading-word table at the end.

## What Was Improved

The original `lupan/` scripts were useful, but much of the logic was duplicated
across several versions. The updated design moves shared behavior into
`liaozhai_tools.py`, so new stories can be added with a small folder, a URL,
and a CSV vocabulary list.

The improvements include:

- One shared downloader, table builder, and PDF builder.
- Story-specific wrapper scripts with clear default paths.
- Flexible section extraction for markers like `原文`, `翻译`, `译文`, and
  `异史氏曰`.
- Flexible CSV headers, including English and Chinese column names.
- Longest-match annotation so multi-character words are handled before
  overlapping shorter entries.
- Automatic Chinese font detection for PDF generation, with a built-in
  ReportLab fallback.
- Compatibility wrappers for the older Lupan script filenames.

## 5️⃣ Example Commands

From the repository root:

```bash
python3 practice/liaozhai_stories/yingning/download_liaozhai_text.py
python3 practice/liaozhai_stories/yingning/make_liaozhai_rare_word_table.py
python3 practice/liaozhai_stories/yingning/make_liaozhai_annotated_pdf.py
python3 practice/liaozhai_stories/yingning/build_editor.py
```

Use `--repeat-annotations` to annotate every occurrence in the PDF.

For editor JSON backups that contain annotations or inserted media, import the
backup before rebuilding the editor and PDF. Story-specific import wrappers
are available for `nie_xiaoqian/` and `laoshan_daoshi/`; when no path is
supplied, each wrapper selects the newest matching backup in Downloads.

The same pattern works for `lupan/`.

## 6️⃣ Adding Another Story

To add another story:

1. Create a new subdirectory under `practice/liaozhai_stories/`.
2. Add wrapper scripts modeled after `yingning/`.
3. Set the story URL and default output names.
4. Create a `*_rare_words.csv` dictionary for that story.
5. Run the downloader, rare-word table script, and PDF script.

This keeps each story self-contained while sharing the program logic in one
place.
