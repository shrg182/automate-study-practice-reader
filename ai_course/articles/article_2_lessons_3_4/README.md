# Article 2: Lessons 3–4

This article explains model training and neural networks.

```bash
python3 build_editor.py
python3 generate_pdf.py
```

Open `editor.html`. Browser storage key: `ai-course-article-2-editor-v1`.

## Process an editor backup

```bash
python3 import_editor_export.py ~/Downloads/ai_course_article_2_editor_backup.json
python3 build_editor.py
python3 generate_pdf.py
```

The import updates the clean text, dictionary, inline/review notes, and reader
notes. It also saves `article_2_editor_seed.json`, which preserves manual rich
formatting, comments, and footnote anchors for subsequent editor and PDF builds.
