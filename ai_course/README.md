# “How AI Works” reading project

This directory treats the introductory AI course as a Shiji-style reading article and uses the shared Shiji proofreading editor.

## Source

- Source draft: [`../../AI_COURSE.md`](../../AI_COURSE.md)
- Working text: `ai_course_clean.txt`
- Article dictionary: `reading_terms.csv`

## Build

```bash
cd practice/ai_course
python3 build_editor.py
```

Open [`editor.html`](editor.html) to edit the clean text, annotations, footnotes, interlinear notes, review items, reader notes, and edit log. The editor also supports browser autosave and TXT, HTML, JSON, log, notes, and article-dictionary exports.

To restore an exported editor backup into the project files, place it in `~/Downloads` or pass its path explicitly:

```bash
python3 import_editor_export.py ~/Downloads/ai_course_editor_backup.json
```

The editor uses the browser storage key `shiji-ai-course-editor-v1`.

## PDF

Generate the news-report-style annotated study edition with:

```bash
python3 generate_ai_course_pdf.py
```

Output: `ai_course_study_report.pdf`.
