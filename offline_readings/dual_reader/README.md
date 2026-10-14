# Open Books: workspace foundation

This is the first implementation phase of the offline reading workspace proposal.
It accepts PDF and EPUB files; existing article editors are not converted by this change.

## Available now

- Add any number of views; split beside or below, duplicate a book view, reorder views,
  resize dividers, maximize/restore, and close views without deleting their books.
- Preset layouts and an automatic tab layout when the proposed splits are too narrow
  or short. Tabs retain all views; hidden views release their renderers.
- One shared toolbar with an explicit active-pane target. Read, View, Panes, and Save
  groups can be opened, closed, pinned, or hidden. Primary, Intermediate, and Advanced
  presets control these currently implemented groups.
- Library-wide toolbar defaults with file-type and book-specific overrides.
- Independent PDF page, scroll offset, zoom, and rotation per view; independent EPUB
  reading position and text size per view.
- A saved-book library, workspace naming, automatic local saving, and portable backup
  and import, optionally including the original book files.
- Migration of the previous reader's saved left/right files without removing its old
  records. Book identities are SHA-256 content hashes, so duplicate views share a source
  and renamed copies retain identity.
- Offline shell caching, including the PDF and EPUB rendering dependencies.

Annotation tools, pinyin, footnotes, images, speech, OCR, linked scrolling, and conversion
of other library editors remain subsequent phases. Their buttons are not presented as
working tools in this phase.

## Use

Open `editor.html` through the hosted reader or local administrator service for the PDF
workspace controls. Direct `file://` opening retains a native PDF fallback; that fallback
cannot provide all saved view controls.

Click a pane or its tab to make it active. Use **Open PDF / EPUB** to replace its document,
**Add pane** for another empty view, or **Duplicate view** for another position in the
same book. **Saved books** reopens sources without uploading them again.

The **Tool groups** dialog changes group visibility, presets, and the preference scope.
**Pin** keeps a group open when transient tool groups are closed by navigation. **Reading
mode** temporarily hides the toolbar without changing its settings.

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

## Code and records

- `workspace-store.js`: IndexedDB access, content identity, versioned workspace validation.
- `workspace-toolbar.js`: toolbar-group registry behavior and layered preferences.
- `reader-pane.js`: per-view PDF/EPUB lifecycle and active-pane notifications.
- `reader.js`: layout tree, library, restoration, backup/import, migration, and orchestration.
- `pdf-viewer.js`: PDF rendering and bidirectional view-state messages.

IndexedDB `open-books-offline` version 2 keeps the legacy `books` store and adds
`documents` and `workspaces`. Source bytes belong to document records, and each pane
references a document ID with separate view settings. Toolbar preferences live in the
versioned `open-books-toolbar-v1` localStorage record and are included in workspace exports.
The backup format is `open-books-workspace`, version 1.

## Verification

`tests/test_open_books_workspace.cjs` generates its own small PDF and EPUB fixtures in
memory. It exercises migration, source identity, independent views, layout changes,
preferences, source-inclusive and metadata-only backups, invalid imports, missing-source
recovery, numeric zoom and rotation, active-pane targeting, closing during source saves,
reading positions, mobile tabs, and offline restoration.

Run with an installed Playwright package; set `PLAYWRIGHT_PATH` if it is outside Node's
module search path. Set `TEST_ENGINE=webkit` to test WebKit. Chrome defaults to its macOS
application path, overridable with `CHROME_PATH`.
