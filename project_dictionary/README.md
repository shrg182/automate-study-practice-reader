# Project Reading Dictionary

This directory contains the unified dictionary of new words used by readings
under `news_reports/` and `practice/`.

The source-of-truth vocabulary remains beside each reading. Run:

```bash
python3 project_dictionary/build_dictionary.py
```

This produces:

- `dictionary.csv`: one merged row per language and term.
- `sources.csv`: one row per source occurrence, for auditing and tracing a term
  back to the reading where it appeared.
- `dictionary_data.js`: browser-ready data consumed by the local UI.

Open `index.html` directly in a browser to search and browse the dictionary.
These three generated artifacts are intentionally ignored by Git because their
large machine-generated diffs can overwhelm code-review views. Regenerate them
after cloning or whenever the source vocabulary changes.

## Sources currently recognized

- Chinese `reading_terms.csv` files.
- Liaozhai `*rare_words.csv` and `my_rare_words.csv` files.
- English vocabulary CSV files (`*vocab*.csv` and `*vocabulary*.csv`).
- JSON files with a top-level `vocabulary` list.
- Python report models that construct `VocabularyItem(...)` objects with literal
  term and definition values.

Generated `*_shengzibiao.txt` files are deliberately not re-imported because
they are derived from the nearby structured CSV and would double-count terms.
Raw reading prose is also not mined automatically: deciding whether every
ordinary word is “new” requires learner-specific judgment.

## Adding vocabulary

Prefer a local structured file beside the reading. For Chinese readings:

```csv
term,pinyin,type,annotation
觅食,mì shí,rare_word,寻找食物。
```

For English readings:

```csv
term,type,definition,example
annihilation,word,complete destruction,The policy risked annihilation.
```

Rebuild after adding or editing terms. The dictionary merges repeated terms,
preserves distinct definitions, counts occurrences, and lists every source.
It also stores a hidden `entry_time` based on the most recently modified
contributing vocabulary source, which powers the UI's “Newest entries” sort.
Optional `page`, `page_number`, `pages`, `location`, or `source_detail` fields
are appended to the source path in the spreadsheet and entry detail drawer.
The UI assigns a five-level review difficulty from the vocabulary `type`:
Common, Intermediate, Advanced, Rare, and Specialist. A source row can override
this heuristic with `difficulty` or `difficulty_level` (number 1–5 or a label).
The Difficulty column dropdown acts as a minimum-level filter: for example,
“3+ Advanced” includes Advanced, Rare, and Specialist entries.
The Open column targets a nearby `source.txt`, `editor.html`, or clean reading
text when present, and otherwise opens the structured vocabulary source.

Each detail card has an Edit entry mode for term, reading, type, difficulty,
definition, example, and displayed source details. These overrides are stored
in browser `localStorage`; they persist across refreshes on the same browser
but do not rewrite the generated CSV or its original vocabulary sources.
