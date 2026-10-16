# Open Books: workspace foundation

This is the first implementation phase of the offline reading workspace proposal.
It accepts PDF, EPUB, UTF-8 TXT, basic Markdown, and PNG/JPG/WebP images; existing article editors are not converted by this change.

## Available now

- Add any number of views; split beside or below, duplicate a book view, reorder views,
  resize dividers, maximize/restore, and close views without deleting their books.
- Drag handles with edge drop previews to move a pane beside, above, or below another.
  Escape cancels; Move earlier/later remains available for keyboard movement.
- Fit-to-window mode with tab fallback, plus a vertically scrollable workspace that grows
  with its panes. Default minimums are 400 px high and 320 px wide; narrow screens stack
  panes at the available width. These settings are saved and included in backups.
- Distant PDF panes release their rendering resources. Opened EPUB views retain their
  text renderer to avoid interrupting initialization or losing position.
- One shared ribbon with an explicit active-pane target and Read, View, Layout,
  and Library tabs. One panel opens at a time; the Read panel includes the active-book name, file opening, and navigation.
  Keep ribbon open replaces individual group pins. Arrow keys switch tabs; Escape collapses.
  Primary shows Read/View, Intermediate adds Layout, and Advanced includes Library.
- Library-wide toolbar defaults with file-type and book-specific overrides.
- Independent PDF page, scroll offset, zoom, and rotation per view; independent EPUB
  reading position and text size per view.
- A saved-book library, workspace naming, automatic local saving, and portable backup
  and import, optionally including the original book files.
- Migration of the previous reader's saved left/right files without removing its old
  records. Book identities are SHA-256 content hashes, so duplicate views share a source
  and renamed copies retain identity.
- Offline shell caching, including the PDF and EPUB rendering dependencies.

Annotation tools, pinyin, footnotes, OCR, linked scrolling, and conversion
of other library editors remain subsequent phases. Their buttons are not presented as
working tools in this phase.

## Use

Open `editor.html` through the hosted reader or local administrator service for the PDF
workspace controls. Direct `file://` opening retains a native PDF fallback; that fallback
cannot provide all saved view controls.

Click a pane or its tab to make it active. Use **Open file** to replace its document,
**Add pane** for another empty view, or **Duplicate view** for another position in the
same book. **Saved books** reopens sources without uploading them again.

The **Ribbon settings** dialog changes tab visibility, presets, and the preference scope.
**Keep ribbon open** retains the selected panel. When unchecked, tabs open temporarily;
click outside or use Previous/Next to collapse. **Collapse ribbon** retains the tab strip and hides panel controls.

**Export workspace** normally exports layout, book identities, positions, and toolbar
preferences. Check **Include book files in backup** for a package that can be restored on
another device without reattaching sources. It includes only books referenced by the
current workspace, not every closed book in the saved library. JSON backups containing
books can be larger than the original files because their bytes are base64 encoded.

Import validates the complete arrangement and verifies included source hashes before
replacing the current workspace. Other saved books remain in the library. A metadata-only
backup asks for missing sources; reattaching the same book preserves its view position.

Unchecking **Keep book files on this device** clears stored book bytes, including legacy
slots, but retains layout and source identities. Open books remain available until the
session ends. Local browser storage is not a substitute for a portable backup.

## Pane arrangement and workspace length

In **Panes & layout**, choose **Scrollable workspace** to keep pane minimum heights and
extend the workspace downward. The outer workspace scrolls between panes; PDF and EPUB
scrolling inside each pane remains independent. There is no fixed application-imposed
vertical workspace length. Existing workspaces retain Fit-to-window mode, while new
empty workspaces default to Scrollable mode.

Use a pane's dotted header handle to relocate it. Drag toward another pane's left, right,
top, or bottom edge; the shaded preview shows the result before dropping. Dragging near
the workspace's upper/lower edge scrolls it. Drop outside the workspace or press Escape
to cancel. Document text selection and drawing areas are not drag handles.

Divider dragging and arrow keys respect minimum pane sizes. In Scrollable mode, expanding
rows can extend the workspace instead of squeezing other panes. On narrow screens,
columns stack without overwriting their saved desktop arrangement. Maximizing remains a
temporary focused view; restore returns to the arrangement.

Relocation updates pane geometry while keeping each live document iframe attached to the
same canvas. Book identities, saved page/section positions, zoom, and edits are not
replaced when a pane moves.

## Code and records

- `workspace-store.js`: IndexedDB access, content identity, versioned workspace validation.
- `workspace-toolbar.js`: toolbar-group registry behavior and layered preferences.
- `reader-pane.js`: per-view PDF/EPUB lifecycle and active-pane notifications.
- `workspace-layout.js`: responsive split geometry and pane minimums.
- `workspace-drag.js`: pointer handles, drop previews, cancellation, and edge scrolling.
- `reader.js`: layout tree, library, restoration, backup/import, migration, and orchestration.
- `pdf-viewer.js`: PDF rendering and bidirectional view-state messages.

IndexedDB `open-books-offline` version 2 keeps the legacy `books` store and adds
`documents` and `workspaces`. Source bytes belong to document records, and each pane
references a document ID with separate view settings. Toolbar preferences live in the
versioned `open-books-toolbar-v1` localStorage record and are included in workspace exports.
The backup format is `open-books-workspace`, version 1. Optional `canvas` settings and
per-node height overrides are additive, so previous backups still load in Fit-to-window mode.

## Verification

`tests/test_open_books_workspace.cjs` generates its own small PDF and EPUB fixtures in
memory. It exercises migration, source identity, independent views, layout changes,
preferences, source-inclusive and metadata-only backups, invalid imports, missing-source
recovery, numeric zoom and rotation, active-pane targeting, closing during source saves,
reading positions, mobile tabs, and offline restoration.

Run with an installed Playwright package; set `PLAYWRIGHT_PATH` if it is outside Node's
module search path. Set `TEST_ENGINE=webkit` to test WebKit. Chrome defaults to its macOS
application path, overridable with `CHROME_PATH`.

## Saved source files and recovery

Keep book files on this device saves newly opened sources and, when enabled, files
currently open in this session. Turning it off stops saving new files; it does not
remove copies already saved. Metadata-only updates and workspace imports also retain
existing saved source bytes. Remove saved files… is a separate, confirmed action.

The save status distinguishes a saved workspace from session-only files and missing
sources. Reattach the exact original PDF/EPUB to restore a missing view and its position.
Keeping the retention checkbox checked cannot reconstruct bytes already absent from
browser storage. Book source bytes remain private in local IndexedDB.

`tests/test_open_books_file_persistence.cjs` checks direct-file PDF reopening across
complete Chrome shutdowns, retention toggles, metadata writes/imports, and missing-file
status using an isolated profile and generated fixtures.

The Read ribbon consolidates the active-pane name, Open file, Previous/Next,
and EPUB contents. There is no separate active-book bar or shared page-number/Go
form. Direct-file PDFs retain native viewer page controls; hosted PDFs support
scrolling and Read-tab Previous/Next.

## Multiple named workspaces

Use the header’s Workspace selector to switch and Workspace actions… to create,
duplicate, rename, or delete an arrangement. New workspaces start with one empty
pane. Switching saves the current arrangement first. Each workspace owns its panes,
layout, active view, and reading positions; documents and retained book bytes remain
shared, so duplication does not duplicate PDF/EPUB storage.

Existing single-workspace records are migrated automatically. The last-used
workspace reopens. Deletion requires confirmation, keeps shared books, and creates
an empty replacement if the final workspace is deleted. Export covers the selected
workspace; import replaces that selected workspace while retaining its identity and
leaving other named workspaces intact. Toolbar visibility/preferences remain shared
at their existing library, file-type, and book scopes.

Named snapshots use UUID keys in the existing IndexedDB workspaces store. The
current key retains the active snapshot for compatibility with existing records.
Workspace version 1 accepts the additive id field and still accepts older backups.
Switching waits for source imports/attachments to finish; in-flight book-list actions
are invalidated when changing workspaces.

## Text, Markdown, images, and Read aloud

- TXT opens as wrapped UTF-8 text. Markdown supports headings, paragraphs, ordered/
  unordered lists, blockquotes, fences, inline code, bold/italic, rules, and links.
  Raw HTML stays literal; only HTTP(S)/mailto links become clickable. Remote inline
  images and arbitrary embedded HTML/scripts are not rendered. This is a basic
  Markdown reader, not a complete CommonMark implementation.
- Text and Markdown retain font size and scroll position. Previous/Next scrolls the
  active text pane. PNG, JPG/JPEG, and WebP use fit-width/fit-page/actual-size or
  percentage zoom and rotation; image view settings survive reopening.
- Read aloud in Read provides voice, speed, Read aloud, Pause/Resume, and Stop.
  It reads the entire TXT/Markdown document, the current EPUB section, or the
  current hosted PDF page. Scanned PDFs without a text layer and images need OCR,
  which is not included. Native file:// PDF viewers do not expose text to this
  toolbar; use the hosted reader for PDF speech. Text, Markdown, and EPUB speech
  work in direct-file mode as well.
- Speech follows one active pane and stops on page/section changes, source/pane
  replacement, workspace switches/imports, and page exit. Voice/rate settings are
  saved locally; available voices come from the browser/OS. Voice options identify
  device and online services, so offline availability depends on the chosen voice.
  Speech uses short sequential chunks. There is no automatic reading on reopen.

Browser API reference: [SpeechSynthesis](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis).

`content-reader.js` implements safe DOM-based Markdown rendering;
`workspace-speech.js` manages voice settings, chunking, and speech lifecycle.
`tests/test_open_books_formats.cjs` uses generated documents and mocked speech to
verify rendering safety, restored positions/transforms, backup imports, PDF/EPUB
text extraction, controls, cancellation, and narrow layouts. It does not verify
OS voice quality or audible playback.
