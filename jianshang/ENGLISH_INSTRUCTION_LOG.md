# English Instruction Review Log

This log collects English corrections and reusable wording from the
《翦商》 editing workflow. It focuses on natural instructions, recurring
technical terms, and distinctions that matter in this project.

## Preferred workflow terms

| Term | Recommended meaning and usage |
|---|---|
| manual editing | Editing performed by a person: “I’ve finished the manual editing.” |
| manually edit | Verb phrase: “I manually edited Chapter 8.” |
| editor | The HTML editing interface, or a person who edits; clarify when necessary. |
| annotation | An explanatory note added to the text. Prefer this over `notation` here. |
| inline commentary | A comment embedded in the text, such as `〔按语：…〕`. |
| editor’s note | A numbered note added by the editor, such as `〔编者注1〕`. |
| source note | An original numbered note from the book. |
| edit log | The exported history of actions performed in the editor. |
| editor backup | The JSON backup exported from the editor. |
| clean text | The reviewed text used to generate study outputs. |
| editor export | The manually edited TXT file exported from the editor. |
| promote the edits | Copy reviewed changes from the editor export into the clean text. |
| process the updates | Import, normalize, validate, and promote the latest edits. |
| regenerate the outputs | Rebuild the vocabulary table, annotated PDF, and HTML editor. |
| annotated PDF page | A page in the generated reading PDF; pagination depends on reflow. |
| source PDF page | The physical page index in the original PDF file. |
| printed page | The page number printed on the scanned book page. |
| caption | Text identifying or explaining an image, diagram, photograph, or table. |
| footnote marker | A reference in the body that points to a note. |
| structural check | A check for footnote alignment, caption flow, or related document structure. |

## Corrections from this dialogue

### Completing a chapter

Original:

> Done with the manual editing on Chapter 6.

Natural revision:

> I’ve finished manually editing Chapter 6. Please process it.

Also natural:

> I’ve completed the manual editing for Chapter 6. Please process the updated files.

Notes:

- `I’ve finished manually editing` is concise and conversational.
- Use `editing Chapter 6`, not normally `editing on Chapter 6`.
- `Manual editing for Chapter 6` is correct when `editing` is a noun.

### Asking Codex to check Downloads

Original:

> Have you looked at the Dowloads for the updates?

Natural revision:

> Have you checked `~/Downloads` for the updated files?

Notes:

- The spelling is `Downloads`.
- `Check Downloads for the updated files` is more natural than `look at the Downloads`.
- A folder path normally does not take `the`: use `check ~/Downloads`.

### Processing a completed manual export

Original:

> Done with the manual editing on Chapter 7. Please check ~Downloads and process updats and output.

Natural revision:

> I’ve finished manually editing Chapter 7. Please check `~/Downloads`, process the updates, and regenerate the outputs.

Notes:

- Use `~/Downloads`, with a slash after the tilde.
- The spelling is `updates`.
- Use plural `outputs` when referring to the vocabulary table, PDF, and editor.
- `Regenerate the outputs` is more precise than `process output`.

### Preparing an editor

Original:

> Please prepare the editor for Chapter 8. A commit message afterwards please.

Natural revision:

> Please prepare the Chapter 8 editor and provide a commit message afterward.

Notes:

- `Chapter 8 editor` is a natural compound noun.
- American English usually uses `afterward`; British English also accepts `afterwards`.
- `Provide a commit message` is clearer than the fragment `A commit message…`.

### Asking about page numbering

Original:

> Regarding the page numbering, are the PDF page numbers and print page numbers on the editor the same as the original/source PDF page numbers?

Natural revision:

> Do the PDF-page and printed-page numbers shown in the editor match the original source PDF?

More precise project wording:

> Do the source-PDF and printed-page numbers shown in the editor match the physical PDF pages and the page numbers printed in the book?

Notes:

- Prefer `printed-page number` to `print page number`.
- `Source PDF` is clearer than `original/source PDF` when the document has already been defined.
- The annotated PDF, source PDF, and printed book use three distinct numbering systems.

### Deferring an issue

Original:

> Please make a note on this page numbering issue and we will look at it at the final fine-tuning stage.

Natural revision:

> Please document this page-numbering issue so that we can revisit it during the final fine-tuning stage.

Notes:

- `Document the issue` is concise professional wording.
- `Revisit` naturally means to examine something again later.
- Use the compound modifier `page-numbering issue` before a noun.

### Describing three numbering systems

Original:

> Please note that it will probably apply three page numbers, i.e., the annotated PDF number, the source PDF page number, and, the print page number.

Natural revision:

> Please note that the final design will probably use three page numbers: the annotated-PDF page, the source-PDF page, and the printed book page.

Notes:

- Use `use`, `display`, or `include` rather than `apply` for page numbers.
- A colon is cleaner than `i.e.` before a three-item list.
- Do not place a comma after `and` in this list.

### Adding annotations and editor’s notes

Original:

> I did editing on Chapter 7 again and entered notation and editor's notation.

Natural revision:

> I edited Chapter 7 again and added an inline annotation and an editor’s note.

If there are several:

> I edited Chapter 7 again and added inline annotations and editor’s notes.

Notes:

- Use `I edited`, not `I did editing on`, for a direct and natural sentence.
- In this workflow, `annotation` is the appropriate term; `notation` usually
  means a system of symbols, such as mathematical or musical notation.
- `Editor’s note` is the natural translation of `编者注`.
- `Inline commentary` is a useful translation of `按语`.

### Current Chapter 8 request

Original:

> I have made the manual editing on Chapter 8. Please check it and process updates and output.

Natural revision:

> I’ve finished manually editing Chapter 8. Please check the files in `~/Downloads`, process the updates, and regenerate the outputs.

Alternative:

> I’ve completed the manual edit of Chapter 8. Please review and process the latest export, then regenerate all outputs.

Notes:

- `I have made the manual editing` is understandable but not idiomatic.
- Use `finish editing`, `complete the editing`, or `complete the manual edit`.
- `The latest export` is useful when referring specifically to the TXT file downloaded from the editor.

### Verifying printed-page ranges

Original:

> Please review previous chapters for the corresponding print page numbers.

Natural revision:

> Please review the previous chapters and verify their corresponding printed-page ranges.

Also natural:

> Please check that the previous chapters show the correct printed-page ranges.

Notes:

- Use `the previous chapters` when referring to a known set of chapters.
- `Printed-page range` is more precise than `print page numbers` when each
  chapter covers a starting and ending page.
- `Verify` emphasizes checking the displayed values against the authoritative mapping.

## Reusable instruction templates

### Preparing a chapter editor and requesting pagination changes

Original:

> Please prepare the editor for Chapter 9. Please consider applying three page number rendering system, i.e., annotated PDF page number, source PDF page number and print page number.

Natural revision:

> Please prepare the Chapter 9 editor. Please consider implementing a three-part page-numbering system: the annotated-PDF page number, the source-PDF page number, and the printed book page number.

Notes:

- Use `implement a ... system` for a feature being added to software.
- Use `three-part` as a compound adjective before `page-numbering system`.
- `Printed book page number` clearly means the number physically printed on the scanned page.
- `i.e.` means “that is” and is unnecessary before a complete three-item list introduced with a colon.

### After finishing a manual pass

> I’ve finished manually editing Chapter [number]. Please check `~/Downloads`, import the latest TXT export and edit log, process the updates, and regenerate all outputs.

### When annotations were added

> I’ve added inline commentary and editor’s notes to Chapter [number]. Please preserve them when processing the latest export and verify that they appear correctly in the annotated PDF.

### When requesting an editor

> Please prepare the manual editor for Chapter [number], extract the source-page images, run the structural checks, and regenerate the study outputs.

Follow-up phrasing:

> If you think it would be better to wait until I’ve finished the manual editing, please let me know.

Use `wait until I’ve finished` when the later event determines when work should begin. `Wait for my manual editing` can sound as though the editing itself is something being delivered rather than completed.

### When requesting verification only

> Please review Chapter [number] for footnote alignment, caption placement, page mapping, and suspicious OCR errors. Do not change the text unless I ask you to apply the corrections.

### When requesting a commit message

> After completing the work, please suggest a concise Git commit message.

## Recurring language patterns

- `finish doing something`: “I’ve finished editing Chapter 8.”
- `complete a task`: “I’ve completed the Chapter 8 manual edit.”
- `check a location for something`: “Check `~/Downloads` for the latest export.”
- `compare A with B`: “Compare the editor export with the clean text.”
- `preserve something when doing something`: “Preserve the editor’s notes when promoting the edits.”
- `verify that`: “Verify that the notes appear correctly in the PDF.”
- `regenerate`: rebuild generated artifacts after the source changes.
- `revisit`: return to an issue for further review later.

### Importing the latest chapter edits

Original:

> Please check ~Downloads, improt the latest TXT export and edit log, process the updates, and regenerate all outputs.

Natural revision:

> Please check `~/Downloads`, import the latest TXT export and edit log, process the updates, and regenerate all outputs.

Notes:

- The spelling is `import`, not `improt`.
- Write the home-folder path as `~/Downloads`.
- `Regenerate all outputs` clearly requests rebuilding every derived artifact.

## Style goal

For these project instructions, aim for short sentences with explicit verbs:

1. State what is finished.
2. Identify where the files are.
3. Say what should be imported or checked.
4. Name the outputs that should be regenerated.
5. Mention any special content that must be preserved.

Example:

> I’ve finished manually editing Chapter 8. The latest export and edit log are in `~/Downloads`. Please import them, preserve the inline commentary, regenerate the vocabulary table, annotated PDF, and editor, and run the structural checks.
