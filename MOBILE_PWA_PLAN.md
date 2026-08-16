# Mobile Reading App and PWA Development Plan

## Objective

Turn the practice reading workspace into an installable mobile experience without forcing the full desktop editor into a small screen.

The recommended product model is **read-first on mobile**, with lightweight annotation tools available through an explicit editing mode. The desktop editor remains the primary environment for intensive proofreading and document management.

## Recommended mobile modes

### 1. Reading mode — default

The article should not be directly editable in the default mobile mode. This reduces accidental changes caused by scrolling, text selection, and the on-screen keyboard.

Reading mode should provide:

- A full-width, distraction-free article surface.
- Adjustable content font size and line spacing.
- Light, dark, and warm reading-paper themes.
- Previous/next article navigation.
- A compact table of contents.
- Tap-to-open dictionary definitions.
- Footnotes displayed in an expandable panel or bottom sheet.
- Text-to-speech controls.
- Visible reading and editing history.
- An option to save selected articles for offline reading.

### 2. Lightweight editing mode — optional

The reader deliberately enters this mode before making changes.

Suitable mobile editing features include:

- Highlighting selected text.
- Adding user notes.
- Adding short annotations or pending-review markers.
- Adding or editing dictionary entries.
- Attaching a photograph from the phone.
- Viewing and removing existing notes.
- Undoing the most recent annotation action.
- Exporting or sharing one consolidated backup.

### 3. Advanced editing mode — secondary

These functions should remain desktop-oriented or be placed behind an `高级编辑` option:

- Rewriting long passages directly.
- Managing many footnotes simultaneously.
- Complex formatting and source comparison.
- Individual HTML, TXT, CSV, JSON, and log exports.
- Bulk backup import and processing.
- Project-wide dictionary administration.

Advanced editing can remain technically available on mobile, but it should not be the default interface.

## Interface recommendations

### Header

Replace the desktop toolbar with a small mobile header containing:

- Back/home navigation.
- Article title.
- Reading progress.
- Font and theme controls.
- A single overflow menu.

### Bottom navigation

A bottom bar is better suited to frequently used mobile functions:

- `正文`
- `目录`
- `词典`
- `札记`
- `更多`

The bottom bar should disappear while scrolling down and reappear when scrolling upward.

### Notes and footnotes

- Display footnotes in a bottom sheet without moving away from the reading position.
- Keep user notes visible alongside other annotation registers.
- Show a note count and provide a direct jump to saved notes.
- Retain duplicate-note detection.

### Editing safety

- Keep the article non-editable until the user explicitly enables editing.
- Show a visible editing-state indicator.
- Save automatically after meaningful changes.
- Provide immediate undo and clear save confirmation.
- Warn before leaving with an unsaved or unexported change.

## Installable Progressive Web App

The first mobile release should be a Progressive Web App rather than a separate native application.

Required components:

- A web-app manifest containing the app name, colors, icons, and standalone display settings.
- Mobile application icons in the required sizes.
- A service worker for caching the application shell.
- HTTPS hosting.
- An installation-help screen for iPhone, iPad, and Android.
- A clear offline-status indicator.

The current `file:///Users/...` pages cannot be installed directly as a normal mobile PWA. The project must be served through HTTPS, or through a suitable development server during testing.

Reference: [MDN — Making PWAs installable](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable).

## Offline strategy

Do not cache every generated editor and all media by default. The collection can become large.

Recommended approach:

1. Cache the application shell and home page.
2. Let the user choose articles or collections for offline reading.
3. Cache article text, dictionaries, and required images together.
4. Display storage usage and allow removal of offline articles.
5. Update cached articles when a newer generated version is available.

## Data storage and synchronization

The current drafts, notes, dictionaries, and reading history are stored locally in the browser. Mobile and desktop browsers therefore have separate data.

### Initial solution

- Retain local browser storage for fast, offline operation.
- Add a single consolidated export/import package for each article.
- Include article edits, annotations, footnotes, user notes, dictionary changes, media references, reading history, and editing metadata.
- Display the most recent backup time.

### Later solution

Optional cross-device synchronization may be added after the mobile interface is stable. It should include:

- User-controlled sign-in.
- Conflict detection between desktop and mobile edits.
- Version history.
- Selective synchronization.
- Clear privacy and deletion controls.

## Proposed development phases

### Prototype implemented — 2026-08-16

The shared workspace now provides the first working Phase 1/2 prototype:

- The home page and editors receive common PWA metadata through `workspace_skin.js`.
- Phone-width editors open in protected, read-first mode.
- The mobile bottom bar provides home, notes, explicit editing, selective offline saving, and installation help.
- The home page provides a compact directory/install bar.
- `manifest.webmanifest`, application icons, and `service-worker.js` provide the installable application shell.
- Offline saving is selective per article; the entire collection is not downloaded automatically.
- Pages missing a viewport declaration receive one from the shared loader, so older generated editors participate without being rebuilt.

The remaining release step is HTTPS deployment followed by installation testing on an actual iPhone/iPad and Android device. Desktop and mobile local-storage records are still separate until a future synchronization feature is implemented.

### Phase 1 — responsive reading prototype

- Add mobile breakpoints to the shared workspace theme.
- Create the compact header and bottom navigation.
- Make reading mode non-editable by default.
- Adapt footnotes, dictionaries, and notes for small screens.
- Test long Chinese texts, images, and speech controls.

### Phase 2 — installable PWA

- Add the manifest and application icons.
- Add the service worker and application-shell cache.
- Deploy through HTTPS.
- Test installation on iOS/iPadOS and Android.

### Phase 3 — offline article management

- Add `保存离线阅读` to article and collection pages.
- Track cache size and update state.
- Add offline and update indicators.

### Phase 4 — lightweight mobile editing

- Add highlights, notes, pending-review markers, and dictionary editing.
- Add mobile image capture and attachment.
- Add duplicate-note prevention and undo.
- Add a consolidated backup command.

### Phase 5 — advanced editing and synchronization

- Evaluate whether full passage editing is practical on tablets.
- Add optional advanced controls.
- Design and test cross-device synchronization only after local workflows are reliable.

## Initial acceptance criteria

The first useful mobile release should satisfy the following:

- The home page and articles work comfortably at phone width.
- The user can install the workspace from an HTTPS address.
- Selected articles remain readable offline.
- Reading mode cannot accidentally modify the article.
- Dictionary definitions, footnotes, speech, and notes are readily accessible.
- Lightweight annotations are preserved locally.
- The user can create a consolidated backup before changing devices.
- Desktop editors and generated source files remain compatible with the mobile data.

## Recommendation

Begin with the responsive reading prototype and installable PWA. Do not expose the complete desktop toolbar on mobile initially. Preserve the editing engine underneath, then add carefully selected annotation features after reading, navigation, offline use, and backup safety are working reliably.
