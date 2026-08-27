# Mobile Reader Library Capacity and Book-Import Plan

Date: August 27, 2026

## Purpose

This document considers:

1. How many complete books the Reader App could hold offline on a mobile device.
2. The difference between a working book directory and an optimized mobile reading package.
3. How *Capital, Volume I* and *Anti-Dühring* should be organized.
4. What storage controls should be added before importing the complete works.

No complete-book import or restructuring is authorized by this document. It is a plan for review before implementation.

## Final goal: a mobile library

The final goal is to build a practical mobile library for the reader.

The Reader App should eventually support a personal collection in which the reader can:

- browse collections, books, parts, chapters, and selected readings;
- install complete books or selected components for offline use;
- retain approximately ten large books when the device has sufficient capacity;
- read leading-language and supporting-language texts;
- open original PDFs when they have been installed;
- maintain notes, annotations, dictionaries, and reading records;
- see exactly how much space each book and accessory component uses;
- remove a PDF or supporting language without removing the main text;
- update books without losing personal study data;
- export and restore the personal library's notes and records.

The system should not impose an arbitrary ten-book maximum. Ten large books are the initial planning target. A device with more safe storage should be allowed to hold more, while a device with less space should offer partial packages and selective installation.

## Online and offline private-library model

The reader should be able to manage one personal reading list in two complementary modes:

1. **Online library** — books and components remain available from the Reader website and are opened over the network.
2. **Offline private library** — selected books and components are installed in storage controlled by the reader's device and remain readable without a network connection.

Online and offline status should be independent of reading-list membership. Adding a title to the reading list should not automatically download a large book. Removing an offline copy should not automatically remove the title from the reading list or delete the reader's notes.

Each reading-list entry should therefore have separate states such as:

```text
In reading list: Yes
Online source: Available
Offline text: Installed
Supporting language: Installed
PDF: Online only
Personal notes: Stored locally
Last content update: Available
```

### Recommended library views

The mobile library should provide filters for:

- All books;
- Reading list;
- Available online;
- Installed offline;
- Partially installed;
- Update available;
- Recently read;
- Finished;
- Archived.

The interface should clearly distinguish:

- **Add to reading list**;
- **Install offline**;
- **Change offline components**;
- **Remove offline copy**;
- **Remove from reading list**;
- **Delete personal study data**.

These actions must not be combined into one ambiguous delete button.

### Privacy boundary

The offline library should be private by default. Personal information should remain on the device unless the reader explicitly exports or synchronizes it.

Private local data includes:

- the personal reading list;
- reading progress and history;
- highlights and annotations;
- inline, editorial, and pending-review notes;
- dictionary history and saved terms;
- attached images or media;
- offline-installation records.

The public Reader deployment should contain published book materials and manifests, but it should not receive the reader's private notes merely because a book is installed or updated.

If synchronization is later enabled, the Reader should let the user choose separately whether to synchronize:

- reading-list membership;
- progress;
- notes and highlights;
- attached media;
- only backup files.

### Offline storage choices

The private library may use two related forms of offline storage:

1. **Browser-managed storage**
   - Cache Storage for book files and PDFs.
   - IndexedDB for manifests, reading lists, annotations, and structured study data.
   - Convenient for direct offline use inside the installed Reader App.

2. **User-managed backup storage**
   - Exported book-package manifests and personal-library backup files.
   - Saved to a folder, external drive, or private cloud location selected by the reader.
   - Used to restore the library if browser storage is cleared or the device is replaced.

Browser-managed offline storage alone should not be considered a permanent backup because browsers and operating systems can remove website data under some conditions.

### Online/offline reconciliation

When the Reader returns online, it should compare local book manifests with published manifests and report:

- no update required;
- text update available;
- PDF update available;
- metadata or index update available;
- local package incomplete;
- source no longer available online.

An update should replace only changed components. It should not download the entire private library again, and it must not overwrite personal notes.

When a book is offline and the network is unavailable, the Reader should use the installed manifest to build its table of contents, search index, source information, and component-status display.

## Main conclusion

There is no single reliable number for the Reader App's "full capacity."

The available space depends on:

- the phone's total and currently free storage;
- the browser and operating-system version;
- whether the Reader is installed as a home-screen web app;
- storage already used by other websites and applications;
- whether the browser grants persistent storage;
- whether a book contains optimized text or duplicated page images.

The Reader should therefore calculate capacity separately on each device. It can use `navigator.storage.estimate()` to obtain the browser's estimated usage and quota, and `navigator.storage.persist()` to request more durable storage where supported.

The practical recommendation is:

> Measure the available quota on the device, reserve a safety margin, calculate each book package before downloading it, and let the reader choose which parts of the book to keep offline.

## Measurements from the current project

The following measurements were taken from the Reader project on August 27, 2026.

| Content | Current size | Meaning |
|---|---:|---|
| Entire deployed Reader, excluding Git history | approximately 338 MiB | All currently deployed files; a phone does not automatically cache all of them |
| 《翦商》 working directory | approximately 257 MiB | Includes the original PDF, text, editors, notes, and extracted page images |
| 《翦商》 optimized deployable package | approximately 102 MiB | Excludes extracted page images, build caches, and development artifacts |
| Generated *Capital, Volume I* package | approximately 13.15 MiB | 37 English reading units, mapped Chinese companion text, metadata, editors, and English PDF |
| Generated *Anti-Dühring* package | approximately 9.03 MiB | 34 English reading units, 29 aligned Chinese units, five keyword fallbacks, metadata, editors, and English PDF |
| Complete English *Capital, Volume I* PDF | approximately 4.13 MiB | Source PDF only |
| Complete English *Anti-Dühring* PDF | approximately 2.88 MiB | Source PDF only |

The complete English *Capital* PDF size was measured as 4,332,746 bytes. The complete English *Anti-Dühring* PDF size was measured as 3,022,106 bytes.

The first complete package build produced these more useful measurements:

| Package component | *Capital, Volume I* | *Anti-Dühring* |
|---|---:|---:|
| Reading units, companion text, editors, and metadata | 9,450,582 bytes | 6,443,226 bytes |
| One book-level English PDF | 4,332,746 bytes | 3,022,106 bytes |
| Measured package total | 13,783,328 bytes (13.15 MiB) | 9,465,332 bytes (9.03 MiB) |

These totals include the accessory data already present in each generated unit: metadata, annotation files, reading-note storage files, terminology files, and the Reader editor. They exclude build caches and downloaded source-page snapshots. User-created media attachments and future search indexes will require additional space.

## Why 《翦商》 is large

The current 《翦商》 working directory is approximately 257 MiB. Its main components are:

| File category | Approximate size |
|---|---:|
| JPG images | 136 MiB |
| PDF files | 91 MiB |
| PNG images | 19 MiB |
| HTML files | 5.8 MiB |
| Text files | 4.3 MiB |
| Markdown, CSV, TSV, scripts, and other files | less than 2 MiB combined |

The original complete PDF alone is approximately 79 MiB. Many additional JPG and PNG files are extracted PDF pages used during preparation and checking.

These extracted page images are valuable working materials, but they should not normally be part of the mobile offline package. Keeping both the original PDF and hundreds of extracted page images duplicates the same visual information.

After excluding extracted page images, build caches, and development artifacts, the practical 《翦商》 reading package is approximately 102 MiB.

## Working directory versus mobile package

Each book should have two different concepts.

### 1. Working directory

The working directory may contain:

- downloaded source pages;
- OCR intermediates;
- extracted PDF page images;
- diagnostic screenshots;
- temporary conversion files;
- scripts and caches;
- alternate source versions;
- proofreading reports.

This directory supports preparation and editing. It does not need to be downloaded to a phone.

### 2. Mobile reading package

The mobile package should contain only:

- the reading text;
- the supporting-language text;
- annotations and notes;
- terminology and dictionary data;
- compact metadata and search indexes;
- the original PDF, if the reader selects it;
- essential images actually used by the book;
- an offline manifest.

This separation is the most important storage improvement.

## Estimated completed-book sizes

The following estimates assume:

- English and Chinese text are stored as compact text or HTML;
- the source PDF is stored once at book level;
- chapter files do not contain duplicated PDFs;
- extracted PDF page images are excluded from production;
- approximately 20% extra space is reserved for indexes, metadata, annotations, dictionaries, cache bookkeeping, and future notes.

| Complete offline package | Planning estimate |
|---|---:|
| 《翦商》 with text and original PDF | 110–130 MiB |
| *Capital, Volume I*, current measured package | 13.15 MiB |
| *Anti-Dühring*, current measured package | 9.03 MiB |
| Both measured packages together | 22.18 MiB |
| Both packages with a 25% reserve for indexes, notes, and growth | approximately 27.7 MiB |
| 《翦商》 plus both measured packages | approximately 125–155 MiB, depending on the chosen 《翦商》 package |

The Marx/Engels figures are measured from the generated packages. They may increase when richer Chinese editions, user media, or additional book-level PDFs are added. The larger 30–45 MiB and 15–25 MiB figures remain useful conservative allowances when planning before an import.

A scanned Chinese PDF may be much larger than a text-based PDF. If a Chinese source PDF is image-based, it should be optional rather than part of the default package.

## Capacity examples

The following table uses the optimized estimates above. "Offline allowance" means the portion of browser storage deliberately assigned to the Reader, not the phone's advertised total storage.

| Reader offline allowance | Optimized 《翦商》-sized books | Bilingual *Capital*-sized books | Three-book sets |
|---:|---:|---:|---:|
| 500 MiB | 3–4 | 11–16 | about 2 |
| 1 GiB | 7–8 | 22–34 | about 5–6 |
| 2 GiB | 15–17 | 45–68 | about 10–12 |
| 5 GiB | 39–43 | 110–170 | about 25–30 |

If all books were stored like the current 257 MiB 《翦商》 working directory, only about three such books would fit in one GiB. If they are packaged like the optimized 110–130 MiB version, approximately seven or eight would fit.

Optimization therefore has a greater effect than the number of chapters.

## Ten-large-book planning measure

Approximately ten large books may eventually be imported. This should be treated as a formal design target for the mobile library.

If each large book is packaged at approximately the optimized 《翦商》 size:

| Component | Estimated space for ten books |
|---|---:|
| Ten optimized book packages at 110–130 MiB each | 1.1–1.3 GiB |
| Shared Reader application and common indexes | 50–150 MiB |
| Book manifests, annotations, and dictionaries | 100–250 MiB |
| User notes and small attachments | 100–250 MiB reserved |
| Temporary update and download space | 150–300 MiB reserved |
| **Recommended total safe allowance** | **approximately 1.6–2.0 GiB** |

The recommended mobile-library design target is therefore:

> The Reader should be able to install and manage ten optimized large books within a safe offline allowance of approximately 2 GiB.

This is a planning target rather than a guarantee. Before installation, the Reader must compare the exact selected-package size with the quota reported by the device.

For comparison, ten books stored like the current unoptimized 257 MiB 《翦商》 working directory would require at least 2.5 GiB before adding notes, indexes, shared application data, and update space. The practical requirement could exceed 3 GiB. This is why working images, OCR intermediates, caches, and duplicated PDF pages must be excluded from mobile packages.

The installation screen should present a calculation similar to:

```text
Mobile library target: 10 books
Selected package size: 1.42 GiB
Notes and media reserve: 200 MiB
Update reserve: 250 MiB
Total planned use: 1.87 GiB
Safe available space: 2.46 GiB
Status: Installation can proceed
```

If there is insufficient space, the Reader should recommend one or more of the following:

1. Install text without PDFs.
2. Install only the leading language.
3. Install selected volumes, parts, or chapters.
4. Remove PDFs from books already installed.
5. Remove temporary caches while retaining texts and personal notes.
6. Keep some books online-only.

### Suggested acceptance criteria

The mobile-library storage system should be considered successful when it can:

1. Calculate the exact byte size of every book before downloading it.
2. Install ten optimized large-book packages within a 2 GiB test allowance.
3. Maintain at least a 20% safety margin whenever the device permits it.
4. Complete an individual book update without requiring a second full copy of the entire library.
5. Remove one book or component without affecting other books.
6. Preserve and restore all user notes after book removal, update, or reinstallation.
7. Recover cleanly from an interrupted or failed download.
8. Explain storage problems in clear language rather than exposing only a browser error.
9. Add or remove a book from the reading list without automatically changing its offline files.
10. Remove an offline book copy while preserving its reading-list entry and private notes.
11. Manage the reading list both online and offline.
12. Restore the private library's reading list and study data from a user-managed backup.

## A safer capacity formula

The Reader should calculate a safe download allowance rather than using the full reported quota.

Suggested conceptual formula:

```text
reported remaining space = estimated quota - estimated usage

safe downloadable space = reported remaining space × safety factor

estimated number of books = floor(safe downloadable space / book package size)
```

A safety factor between 0.70 and 0.80 is reasonable. At least 20% should remain unused for:

- browser bookkeeping;
- updates;
- user notes and attached media;
- temporary download space;
- quota-estimation error;
- other origin data.

The browser cannot always report the phone's actual free physical space. A large reported quota does not guarantee that the device has enough free storage to fill it.

## Browser-storage considerations

Browser data is normally stored in best-effort mode. It can be removed when:

- the device is under storage pressure;
- the browser's overall quota is exceeded;
- the user clears website data;
- the origin has not been used for a long time;
- private-browsing mode ends.

Modern browsers may provide a theoretical origin quota based on a percentage of total disk space. That theoretical quota should not be treated as a promise that all of the space is physically available.

Important references:

- [MDN: Storage quotas and eviction criteria](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria)
- [WebKit: Updates to Storage Policy](https://webkit.org/blog/14403/updates-to-storage-policy/)

The Reader should request persistent storage where supported, but it must still maintain backup and export features. Persistent storage reduces automatic eviction risk; it does not protect data from device failure or deliberate deletion.

## Recommended general book hierarchy

The Reader's three-layer structure should be retained and extended where necessary:

```text
Collection
└── Book
    ├── Book information and sources
    ├── Original PDFs
    ├── Part or major division
    │   └── Chapter
    │       └── Reading unit or section
    ├── Notes and annotations
    ├── Dictionary and terminology
    └── Offline manifest
```

For short books, a chapter can be one Reader page. For long chapters, each natural source section should become a separate reading unit.

The home page can continue to display only collection titles initially. Opening a collection shows books; opening a book shows its parts and contents; opening a chapter or section launches the Reader.

## Proposed structure for *Capital, Volume I*

The complete English source contains front matter, eight parts, 33 chapters, and an appendix. The Chinese source uses a different chapter grouping and displays 25 chapters.

Recommended Reader structure:

```text
Capital, Volume I
├── Front Matter
│   ├── Dedication
│   ├── Prefaces
│   └── Afterwords
├── Part I — Commodities and Money
├── Part II — Transformation of Money into Capital
├── Part III — Production of Absolute Surplus-Value
├── Part IV — Production of Relative Surplus-Value
├── Part V — Absolute and Relative Surplus-Value
├── Part VI — Wages
├── Part VII — Accumulation of Capital
├── Part VIII — Primitive Accumulation
└── Appendix — The Value-Form
```

English should remain the leading language. Chinese should be aligned by source section or paragraph group rather than solely by chapter number, because the English and Chinese editions do not use identical chapter divisions.

Very long chapters should be divided into their natural sections. Examples include:

- Chapter 10, "The Working-Day";
- Chapter 15, "Machinery and Modern Industry";
- Chapter 24, "Conversion of Surplus-Value into Capital";
- Chapter 25, "The General Law of Capitalist Accumulation."

This produces smaller pages, faster mobile rendering, more precise English–Chinese alignment, and more useful annotations.

Sources examined:

- [English *Capital, Volume I* contents](https://www.marxists.org/archive/marx/works/1867-c1/)
- [Chinese 《资本论》第一卷 contents](https://www.marxists.org/chinese/marx/capital/index.htm)
- [English *Capital, Volume I* PDF](https://www.marxists.org/archive/marx/works/download/pdf/Capital-Volume-I.pdf)

## Proposed structure for *Anti-Dühring*

Recommended Reader structure:

```text
Anti-Dühring
├── Prefaces
│   ├── Preface of 1878
│   ├── Preface of 1885
│   └── Preface of 1894
├── Introduction
│   ├── I — General
│   └── II — What Herr Dühring Promises
├── Part I — Philosophy
│   ├── General philosophical chapters
│   ├── Philosophy of Nature
│   ├── Morality and Law
│   └── Dialectics
├── Part II — Political Economy
├── Part III — Socialism
└── Supplementary Material
    ├── Notes from collected works
    ├── Notes by Engels
    ├── Fragment on Ireland
    └── Fragment on Thomas More
```

The complete work contains:

- three prefaces;
- two introductory chapters;
- Part I, Chapters 3–14;
- Part II, ten chapters;
- Part III, five chapters;
- notes and supplementary fragments.

English should lead, with Chinese support aligned at chapter or natural subsection level.

Sources examined:

- [English *Anti-Dühring* contents](https://www.marxists.org/archive/marx/works/1877/anti-duhring/index.htm)
- [English *Anti-Dühring* PDF](https://www.marxists.org/archive/marx/works/download/pdf/anti_duhring.pdf)

## Recommended package contents

Each complete book should have a manifest similar to:

```text
book-manifest.json
metadata.json
contents.json
search-index.json
sources/
pdf/
parts/
chapters/
notes/
dictionary/
```

The manifest should record:

- book identifier and version;
- title and author;
- languages;
- parts, chapters, and reading units;
- source attribution;
- file list;
- exact byte size of every optional component;
- total package size;
- checksum for each downloaded file;
- last update date;
- offline installation status.

## Recommended download choices

The reader should not be forced to download the largest package. Each book should offer:

1. **Text only**
   - Leading-language text and essential metadata.

2. **Bilingual text**
   - Leading-language text plus the supporting-language text.

3. **Text and PDF**
   - Text package plus the selected source PDF.

4. **Complete offline package**
   - Bilingual text, PDF, notes, dictionaries, indexes, and required media.

5. **Read online only**
   - No permanent book download beyond normal browser caching.

The storage estimate should be displayed before confirmation, for example:

```text
Capital, Volume I
Bilingual text: 21 MiB
English PDF: 4.13 MiB
Chinese PDF: 12 MiB
Indexes and notes: 4 MiB
Estimated total: 41.13 MiB
Available safe space: 836 MiB
```

## Storage dashboard recommendation

The existing storage indicator should be expanded into a book-storage dashboard showing:

- estimated browser quota;
- current Reader usage;
- safety reserve;
- safe available space;
- installed books;
- size of each installed component;
- notes and attached-media usage;
- temporary cache usage;
- buttons to update, remove, or partially remove a book;
- whether persistent storage has been granted.

Removing a PDF should not remove the text or notes. Removing a supporting language should not remove the leading language. User-created notes should require a separate explicit action before deletion.

## Recommended storage technologies

Use:

- **Cache Storage** for HTML, PDFs, styles, scripts, and static media;
- **IndexedDB** for manifests, structured annotations, download records, and larger user data;
- **localStorage** only for small preferences such as layout mode and the currently selected tab;
- exportable JSON or backup packages for user notes and reading records.

`localStorage` is generally limited to approximately 5 MiB per origin and should not hold complete books, PDFs, large notes, or images.

## Accessory-data allowance

The storage calculation should include more than the source text and PDF.

Recommended allowance:

| Accessory category | Suggested allowance |
|---|---:|
| Search indexes and manifests | 3–5% of book text size |
| Annotations, footnotes, and dictionaries | 5–15% |
| Cache and update bookkeeping | 5% |
| User notes without media | at least 10 MiB per large book |
| User images and videos | separate configurable reserve |
| Temporary update/download space | at least the size of the largest file being replaced |

For simple planning, adding 20% to the static package and reserving a separate 100–250 MiB user-data area is reasonable.

Videos should not be included in the default offline package. They should be separately downloadable because a few videos can exceed the size of many text-based books.

## Files that should not be deployed by default

Production packaging should exclude:

```text
__pycache__/
*.pyc
.DS_Store
pdf_pages/
diagnostic screenshots
OCR test images
temporary exports
conversion intermediates
development-only source snapshots
```

Source snapshots that are required for attribution or recovery may remain in the development repository without being placed in the mobile offline manifest.

## Suggested implementation sequence

### Phase 1 — Storage framework

1. Add a device-specific storage dashboard.
2. Add persistent-storage detection and requests.
3. Define the offline book-manifest format.
4. Add component-level download and removal.
5. Add storage-error and incomplete-download recovery.
6. Protect user notes from book-cache removal.

### Phase 2 — Complete *Anti-Dühring*

This is the smaller and structurally simpler test book.

1. Import all English chapters.
2. Import and align Chinese support.
3. Add the complete English PDF at book level.
4. Create the hierarchical table of contents.
5. Measure exact text, PDF, index, and annotation sizes.
6. Test full and partial offline installation on a phone.

### Phase 3 — Complete *Capital, Volume I*

1. Import the English front matter, parts, chapters, and appendix.
2. Divide long chapters into natural reading units.
3. Import the Chinese source.
4. Create a cross-edition alignment map.
5. Add the original PDFs as optional book-level components.
6. Measure and test the complete bilingual package.

### Phase 4 — Optimize 《翦商》

1. Keep the original PDF.
2. Exclude extracted page images from the default mobile package.
3. Retain only images actually needed by the text or annotations.
4. Generate its manifest and exact component sizes.
5. Compare its measured installation size with Capital and Anti-Dühring.

### Phase 5 — Capacity report

After the three packages are complete, test them on representative devices and report:

- actual package size;
- actual Cache Storage and IndexedDB usage;
- installation time;
- update overhead;
- phone storage estimate before and after installation;
- behavior under low-storage conditions;
- number of comparable books supported with a safe reserve.

## Final recommendation before implementation

The Reader can probably hold many text-based bilingual classics. The practical limitation will be PDFs, duplicated page images, user-attached media, and browser eviction—not plain text.

The best first implementation is therefore:

1. Build the storage and package-management framework.
2. Complete *Anti-Dühring* as the smaller pilot.
3. Complete *Capital, Volume I* with section-level bilingual alignment.
4. Repackage 《翦商》 without production copies of extracted PDF pages.
5. Measure the three real packages on the target phone before establishing a formal library-capacity number.

6. Use those measurements to validate the ten-large-book, approximately 2 GiB mobile-library target.

This sequence will produce a trustworthy capacity figure and a reusable structure for later books. The result should be a maintainable personal mobile library in which books, PDFs, supporting languages, and study data can be installed and managed independently.
