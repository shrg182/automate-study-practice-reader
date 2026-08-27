# 《毛泽东批注二十四史》Reader collection

This collection targets the later 91-volume horizontal simplified edition.

The Reader uses two compatible structures:

- Reader hierarchy: collection → one of the Twenty-Four Histories → traditional divisions and chapters → selected reading.
- Source hierarchy: physical source volume → scanned page → OCR block → annotation anchor.

The separation preserves the printed edition while allowing readers to navigate by historical work. Scans, OCR, and page alignment remain optional offline packages and must not be marked complete until a reliable copy of the 91-volume edition is obtained.

Research records are stored separately from Mao's annotations, editorial notes, and private reader notes. Each record requires a source URL, scope, type, summary, and reliability label.

Run `python3 practice/mao_annotated_24_histories/build_collection.py` after changing the manifest data, followed by `python3 practice/build_index.py`.
