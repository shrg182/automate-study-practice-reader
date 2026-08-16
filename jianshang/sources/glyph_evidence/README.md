# Printed-Glyph Evidence

This folder preserves small crops from the printed book that were used to
identify uncommon, ambiguous, or OCR-damaged characters during manual editing.
The crops are editorial evidence; pronunciation and reader-facing definitions
remain in each chapter's `reading_terms.csv`.

Use `glyph_evidence.tsv` as the index. Page fields distinguish the three page
systems used by this project:

- `viewer_page`: page number shown by a PDF reader;
- `physical_pdf_page`: one-based page number in the source PDF file;
- `printed_page`: page number printed in the book.

When adding evidence:

1. Put the crop in the matching `chapter_XX` folder.
2. Name it `chXX_pPRINT_vVIEW_term.jpg` when practical.
3. Add a manifest row with the reading, context, source file, and review status.
4. Keep uncertain identifications marked `pending`; do not treat a visual guess
   as a confirmed dictionary reading.

The complete source pages remain in each chapter's `pdf_pages/` folder. These
small crops are retained because they show exactly which printed form prompted
the editorial decision.
