# «Хроника крупнейших войн в истории России»

## Collection implementation plan

**Status:** Phase 0 prototype implemented; future periods remain to be populated
**Primary language:** Russian
**Supporting languages:** English and/or Chinese, recorded per article
**Intended application:** Reader App, including its mobile and offline modes

## 1. Purpose

Build a structured Russian-language chronicle of the major wars in the history
of Russia and its predecessor states. The collection should help a reader first
understand a historical period, then examine its principal wars and selected
battles, and finally review the period's larger military, political, territorial,
and social consequences.

This is a curated reading collection, not an exhaustive list of every raid,
uprising, border incident, or engagement. Minor conflicts may be added when they
are necessary to explain a major war, a territorial transition, or the evolution
of the state and its armed forces.

The current prototype covers Periods 5–10 (1689–1945) with nineteen readings:
period introductions, selected wars, and period summaries. It includes a
period-aware persistent article selector, import-to-library behavior, Russian
primary text, English and Chinese support tabs, editable reading text, and
locally saved/exportable notes. Stable selection IDs combine period and article
IDs so similarly named units in different periods do not collide.

The seven implemented war readings now contain 26 subordinate battle records.
Their lists are collapsible beneath each war in the selector and are rendered
after the overview on the individual war page. Every battle also has an
independent checkbox, source link, Reader page, stable library ID, and local note
storage. Battles are not imported by default: the reader explicitly chooses
which ones should appear alongside the 19 period and war readings.

## 2. Working title and catalog placement

- Russian title: **«Хроника крупнейших войн в истории России»**
- Short navigation title: **Войны России**
- English supporting title: **Chronicle of the Major Wars in Russian History**
- Reader catalog level: first-layer collection
- Suggested directory: `practice/russian_wars/`
- Suggested catalog key: `russian_wars`
- Interaction model: follow the existing `rongzhai_suibi/select_articles.html`
  browse–select–import workflow

The collection must remain separate from `chinese_wars`. It may reuse the
Chinese-wars interface and data concepts, but its sources, periodization,
terminology, and editorial notes must be independently maintained.

## 3. Reader hierarchy

The target hierarchy is:

```text
Collection
├── Complete catalog and article selector
│   └── Historical period
│       ├── Introduction
│       ├── Period brief
│       ├── Individual-war articles
│       ├── Selected-battle articles
│       └── Period summary
└── Personal Reader library
    └── Imported articles selected by the reader
        └── Full editor, annotations, notes, language support, and offline state
```

On the Reader home page, only the first-layer collection title should be shown
until opened. Historical periods should initially be collapsed. Within an open
period, the introduction, wars, and summary should be easy to distinguish.

The complete historical catalog and the personal reading library are different
layers. The catalog may list hundreds of available items without placing all of
them on the Reader home page. Only articles already prepared as defaults or
explicitly selected by the reader are imported into the personal library for
detailed reading and note-taking.

### 3.1 Selection and import workflow

The workflow should closely follow 《容斋随笔》:

1. Open the collection and choose **选择更多篇目 / Select articles**.
2. Browse available items grouped by historical period.
3. Search Russian titles, English titles, Chinese titles, dates, participants,
   places, and source identifiers.
4. Filter by period, article type, language support, preparation status, or
   offline availability.
5. Select individual articles or select all currently visible results.
6. Review a selection counter and estimated download/storage size.
7. Choose **Import into library** to add prepared articles to the Reader catalog.
8. Open an imported article in the full Reader to read, annotate, add inline or
   editorial notes, mark pending review, consult sources, and manage offline use.

Selection state should persist locally. It must be possible to add or remove an
article later without deleting the reader's saved notes. Importing a selection
should be idempotent: repeating it must not create duplicate catalog entries.

For administrative population, retain the existing JSON queue pattern used by
《容斋随笔》. The selector may export a processing queue containing selected
catalog records, requested supporting languages, PDF/offline choices, and
generation status. This queue is separate from the reader-facing **Import into
library** action.

## 4. Historical periods

The initial collection should end in 1945. Later Soviet and post-Soviet conflicts
should be planned as a separately reviewed extension because terminology,
boundaries, causal descriptions, and assessments may be disputed or politically
sensitive.

### Period 1 — Early Rus and princely warfare, c. 860–1237

- Formation and expansion of Rus
- Byzantine, steppe, and neighboring-polity conflicts
- Internal princely warfare only when historically consequential
- End point: Mongol invasion

### Period 2 — Mongol invasions and the Rus principalities, 1237–1462

- Mongol invasion and the Golden Horde
- Conflicts involving Novgorod, Lithuania, Sweden, and the Teutonic Order
- Growth of Moscow and conflicts among Rus principalities

### Period 3 — Formation of the centralized Russian state, 1462–1613

- Muscovite expansion and consolidation
- Russo-Lithuanian wars
- Kazan and Astrakhan campaigns
- Livonian War
- Time of Troubles and foreign interventions

### Period 4 — Russian Tsardom and early Romanovs, 1613–1689

- Polish–Muscovite and Russo-Swedish conflicts
- Smolensk War
- Russo-Polish War of 1654–1667
- Russo-Turkish and Crimean campaigns
- Expansion into Siberia and border conflicts where appropriate

### Period 5 — Peter the Great and the eighteenth-century empire, 1689–1801

- Azov campaigns
- Great Northern War
- Russo-Persian campaigns
- Russo-Turkish wars
- Seven Years' War
- Partitions of Poland and related campaigns

### Period 6 — Napoleonic and early nineteenth-century wars, 1801–1855

- Coalition wars against Napoleonic France
- Finnish War
- Russo-Persian and Russo-Turkish wars
- Patriotic War of 1812 and campaigns of 1813–1814
- Caucasian War
- Crimean War as the transition to the next period

### Period 7 — Late Russian Empire, 1855–1917

- Final phases of the Caucasian War
- Central Asian campaigns
- Russo-Turkish War of 1877–1878
- Russo-Japanese War
- First World War through 1917

### Period 8 — Revolution and Russian Civil War, 1917–1922

- Revolutionary armed conflict
- Principal Civil War fronts
- Foreign intervention
- Polish–Soviet War
- Regional conflicts and independence wars where needed for context

### Period 9 — Early USSR and interwar conflicts, 1922–1941

- Border conflicts in Central Asia and the Far East
- Soviet involvement in the Spanish Civil War as a supporting topic
- Battles of Lake Khasan and Khalkhin Gol
- Soviet–Finnish War
- Soviet entry into Poland and other operations preceding June 1941, with
  careful terminology and multiple sources

### Period 10 — Second World War and the Great Patriotic War, 1939–1945

- Relationship between the Second World War and the Great Patriotic War
- German invasion of the USSR
- Major defensive and offensive campaigns
- Selected decisive battles
- War against Japan in 1945
- Military, demographic, territorial, and political consequences

## 5. Standard section structure

Every historical period will contain the following components.

### 5.1 Introduction — `Введение`

The introduction should be a readable Russian article, normally 800–1,500
words, explaining:

- Political geography and state formation
- Principal neighboring powers and recurring alliances
- Military organization and important technological changes
- Common causes and theaters of war
- The period's place in the longer chronology
- Important terminology needed by the reader

An English support pane should provide a concise structured synopsis rather
than a complete line-by-line translation unless a full translation is available
from a reliable source.

### 5.2 Period brief — `Краткая характеристика периода`

Use a table with these fields:

| Field | Content |
| --- | --- |
| Период | Conventional Russian period name |
| Даты | Approximate beginning and ending years |
| Государство | Rus, principality, Tsardom, Empire, RSFSR, or USSR |
| Основные противники | Recurring opposing powers |
| Союзники | Important recurring allies |
| Театры военных действий | Principal geographical theaters |
| Особенности | Organization, weapons, logistics, or strategic changes |
| Русские источники | Direct links |
| English references | Direct links |

### 5.3 Major-wars list — `Крупнейшие войны`

The list is chronological. Each item must display at least:

- Russian title
- English title
- Date range
- Principal participants
- Region or theater
- One-sentence Russian characterization
- Outcome label
- Link to the complete war entry
- Russian and English reference links

### 5.4 Period summary — `Итоги периода`

The summary should synthesize rather than repeat the entries. It should discuss:

- Changes in borders and political authority
- Changes in military institutions and strategic priorities
- Demographic, economic, and social consequences
- Diplomatic realignment
- Unresolved conflicts inherited by the next period
- A short transition to the following period

## 6. Individual-war article template

Each major war should use a consistent data model and reading layout.

```yaml
id: stable_ascii_identifier
period_id: period_identifier
title_ru: Russian title
title_en: English title
alternate_names: []
date_start: YYYY-MM-DD or YYYY
date_end: YYYY-MM-DD or YYYY
participants: []
allies: []
opponents: []
regions: []
result_ru: concise neutral result
result_en: concise English support
territorial_changes: []
source_links_ru: []
source_links_en: []
status: drafted | sourced | reviewed | published
```

The visible article should contain:

1. **Кратко / At a glance**
2. **Предыстория и причины / Background and causes**
3. **Участники и цели / Participants and objectives**
4. **Ход войны / Course of the war**
5. **Основные кампании / Major campaigns**
6. **Избранные сражения / Selected battles**
7. **Итоги / Outcome**
8. **Территориальные и политические последствия / Consequences**
9. **Историографические и терминологические замечания / Editorial notes**
10. **Русские источники / Russian sources**
11. **English references**

## 7. Selected-battle records

Battles are subordinate to wars rather than independent first-layer entries.
Only decisive, representative, or unusually well-documented battles should be
selected initially.

Suggested fields:

- Russian and English names
- Date
- Location and modern geographical identification
- War and campaign
- Commanders
- Forces, with uncertainty explicitly noted
- Outcome
- Strategic importance
- Map link
- Russian source links
- English source links

Conflicting casualty or force estimates must not be silently combined. Present
attributed ranges or mark the field as disputed.

## 8. Language policy

### Russian

- Russian is the leading reading language.
- Main narrative, tables, labels, and editorial notes are written in Russian.
- Use contemporary Russian orthography except when quoting a historical source.
- Historical quotations retain their original wording, with modernization or
  explanatory notes clearly marked.

### Supporting-language choice

- Russian remains the primary source and reading language, but an article may
  offer **English support**, **Chinese support**, **English and Chinese support**,
  or **Russian only**.
- Supporting-language availability must be visible in the selector before the
  article is imported.
- Provide supporting titles, concise summaries, important terminology, and
  source links where reliable material is available.
- A complete English translation may be included only when it is reliable,
  appropriately licensed, or independently written for the Reader.
- Chinese support may contain a full reliable translation, a concise Chinese
  guide, terminology, notes, and source links. Label partial support clearly; do
  not present a summary as a translation.
- Reuse the Reader's adjustable comparison layout. The secondary pane should
  switch between English and Chinese when both exist, and retain the familiar
  primary-only, primary-leading, balanced, support-leading, and support-only
  views.
- On mobile, Russian text remains the default focus; English support is opened
  through the study pane. The same behavior applies to Chinese support.
- Notes belong to the article, not to a particular display language, while a
  note may record which passage and language it references.

## 9. Source hierarchy

Sources should be recorded at item level. A war entry should normally use more
than one source, particularly where dates, participants, outcomes, or terminology
are disputed.

### Tier 1 — Archival and institutional sources

- Presidential Library of the Russian Federation
  - <https://www.prlib.ru/collections/2087403>
  - <https://www.prlib.ru/collections_all>
- Russian State Military Archive
  - <https://opisi.rgvarchive.ru/>
  - <https://rgvarchive.ru/ellib>
- Other national archives, libraries, museums, and published document collections

Use these for primary documents, catalog descriptions, maps, photographs,
official records, and digitized historical publications. Many items should be
linked rather than copied.

### Tier 2 — Scholarly reference works and curated historical projects

- Runivers reference project, *Военные конфликты, кампании и боевые действия
  русских войск 860–1914 гг.*
- Russian Historical Society description:
  <https://historyrussia.org/sobytiya/vpervye-sobrany-i-opisany-vse-vojny-rossii-s-860-do-1914-g.html>
- Academic histories, peer-reviewed articles, military encyclopedias, and
  university publications

The Runivers chronology is the preferred discovery backbone for 860–1914, but
individual Reader articles should still cite accessible supporting sources.

### Tier 3 — Discovery and cross-checking sources

- Russian chronological list:
  <https://ru.wikipedia.org/wiki/Список_войн_и_вооружённых_конфликтов_России>
- English chronological list:
  <https://en.wikipedia.org/wiki/List_of_wars_involving_Russia>
- Wars.ru chronology:
  <https://www.wars.ru/timeline>

These may seed names and dates but should not be the sole authority for a
published Reader entry.

## 10. Neutrality and editorial standards

- Distinguish contemporary names from later historiographical names.
- Record important alternative names in Russian and English.
- Avoid presenting national memory terminology as universally accepted fact.
- Separate factual chronology from interpretation.
- Attribute contested causes, outcomes, casualty estimates, and territorial
  descriptions.
- Clearly distinguish Rus, Muscovy, the Russian Tsardom, the Russian Empire,
  the RSFSR, the USSR, and the Russian Federation.
- Explain when a conflict's inclusion as a “Russian war” depends on how the
  predecessor state is defined.
- Do not silently project modern borders or national identities backward.
- For translated passages, record translator and edition where known.

## 11. Reader interface requirements

- First-layer collection title only on the closed home page.
- Historical periods collapsed by default.
- A collection-level **Select articles** button matching 《容斋随笔》.
- Searchable, filterable checkboxes grouped by historical period.
- Selection persistence, selected-count display, select-visible toggle, and
  estimated import/offline size.
- Clear states for **available**, **prepared**, **in library**, **stored
  offline**, and **update available**.
- Import and remove-from-library actions must not erase annotations by default.
- Each period opens to its introduction, brief, wars list, and summary.
- Individual war titles open their complete entries.
- Selected battles appear under their parent war.
- Russian/English or Russian/Chinese layout control available when supporting
  text exists; a support-language chooser appears when both exist.
- Russian-only mode must use the full available width.
- On mobile, the principal Russian text remains visible by default.
- English support, notes, glossary, sources, and maps remain accessible through
  the mobile study pane.
- Source links open separately and identify the source institution.
- All annotations appear in the unified notes pane while remaining visible at
  the bottom of the article where appropriate.

## 12. Offline-library requirements

The collection should support book- or period-level offline storage without
caching the entire war library automatically.

Offline storage is independent of library membership. An article may be listed
in the personal library without being downloaded, and a reader may later choose
**Store offline**. Conversely, removing an offline copy should not remove the
article from the library or erase notes.

An offline package for one selected article or period should contain:

- Period landing page
- Introduction and period brief
- Major-wars list
- Published individual-war articles
- Period summary
- Local dictionaries and selected English and/or Chinese support data
- Required interface assets
- Selected small maps or images explicitly approved for offline inclusion

Large PDFs, archival scans, films, and external collections should normally
remain linked resources. The package manifest should record estimated and actual
storage size, version, source revision, and removal status.

## 13. Proposed files and generators

```text
practice/russian_wars/
├── README.md
├── catalog.csv
├── build_collection.py
├── select_articles.html
├── selection_schema.json
├── index.html
├── shared_terms.csv
├── source_registry.csv
├── period_01_early_rus/
│   ├── period.json
│   ├── introduction/
│   │   └── editor.html
│   ├── wars.csv
│   ├── wars/
│   │   └── <war_slug>/
│   │       ├── metadata.json
│   │       ├── support_en.md
│   │       ├── support_zh.md
│   │       ├── source.md
│   │       └── editor.html
│   └── summary/
│       └── editor.html
└── ...
```

Prefer structured source files plus generated Reader pages. Do not make generated
HTML the only surviving source of historical content.

The central catalog should include, at minimum, article ID, period ID, article
type, Russian/English/Chinese titles, date range, source URL, prepared editor
path, English-support status, Chinese-support status, estimated base size,
estimated support size, and version. The selection JSON should store stable IDs,
not titles or generated paths.

## 14. Phased implementation

### Phase 0 — Prototype and schema

- Finalize `catalog.csv`, period metadata, war metadata, and source registry.
- Adapt the browse, search, checkbox, persistent-selection, and processing-queue
  behavior from `rongzhai_suibi/select_articles.html`.
- Add a reader-facing import action and library membership state rather than
  treating the selector only as an editorial queue exporter.
- Reuse appropriate bilingual layout behavior from `chinese_wars` and the
  English-first Marxist readers, generalized for Russian plus English or Chinese.
- Build one complete sample period with introduction, three to five wars, and a
  summary.
- Test Russian-only, bilingual, mobile study-pane, backup, and offline behavior.

Recommended prototype: **Period 6, 1801–1855**, because it offers recognizable
wars, strong Russian and English sources, clear campaigns, and useful variation
between European, Caucasian, Persian, Ottoman, and naval theaters.

### Phase 1 — Core chronology through 1914

- Populate periods 1–7.
- Select approximately 30–40 major wars in total.
- Add only the most important battles during the first pass.
- Use the Runivers chronology as a discovery backbone and institutional sources
  for verification and supplementary documents.

### Phase 2 — Revolution, Civil War, and interwar USSR

- Populate periods 8–9.
- Establish stricter terminology and attribution review.
- Add archival links from RGVA and the Presidential Library.

### Phase 3 — Second World War

- Populate period 10 as a larger, internally grouped section.
- Distinguish Second World War chronology from Great Patriotic War chronology.
- Organize major campaigns before adding individual battles.
- Control map and media sizes for mobile storage.

### Phase 4 — Post-1945 extension

- Create a separate review plan before implementation.
- Require multiple Russian and English sources for every conflict.
- Document naming, boundary, and participant disputes explicitly.
- Keep current conflicts outside the initial historical release.

## 15. Initial content target

The first complete edition should aim for:

- 10 historical periods
- 10 introductions
- 10 period briefs
- 30–40 major-war entries
- 10 period summaries
- Approximately 40–70 selected battle records
- At least one Russian and one English supporting link per major war
- Multiple sources for disputed or complex wars

This target is substantial enough to function as a historical survey while
remaining practical for review and mobile publication.

## 16. Verification checklist

### Historical verification

- Dates and names checked against at least one strong source
- Participants and predecessor states named accurately
- Causes distinguished from triggers
- Outcome and territorial change independently checked
- Uncertain estimates attributed
- Alternative terminology recorded
- Russian and English links tested

### Reader verification

- Collection count and search terms correct
- Periods collapsed on initial load
- Selector groups articles correctly by period
- Search and all filters work together
- Select-visible and individual checkboxes persist after reload
- Importing adds only selected prepared articles and creates no duplicates
- Removing a library item preserves notes unless deletion is explicitly chosen
- Selector correctly reports English, Chinese, both, or no supporting text
- Introduction, war list, and summary visibly distinct
- War and battle dropdowns work without fragile JavaScript dependencies
- Russian-only mode fills the reading area
- English and Chinese support, when present, are reachable on desktop and mobile
- Source, notes, glossary, and backup functions work
- Offline package saves, opens, reports size, and removes correctly
- Regenerated pages preserve imported annotations and source data

### Publication verification

- Private repository clean after commit
- Public mobile snapshot contains all intended files
- GitHub Pages deployment succeeds
- Live collection count matches local catalog
- At least one introduction, one war entry, one summary, and one mobile/offline
  path are checked online after deployment

## 17. Decisions recorded for future work

1. The collection is Russian-first, with English as optional support.
2. Historical periods are sections, each framed by an introduction and summary.
3. Wars are the main reading units; battles are subordinate records.
4. The first edition ends in 1945.
5. Post-1945 conflicts require a separate review plan.
6. The initial scope is curated major wars, not all 997 conflicts recorded by
   the Runivers reference project.
7. Archival scans and large PDFs are normally linked rather than automatically
   stored offline.
8. Structured source files must be retained so the collection can be rebuilt,
   reviewed, translated, and expanded safely.
9. The collection follows the 《容斋随笔》 catalog-selection model: the complete
   catalog remains browsable, while the reader imports chosen articles into a
   smaller personal library for detailed reading and notes.
10. English and Chinese are optional supporting languages. Their availability is
    recorded per article, and neither is required when reliable support does not
    exist.
11. Library membership, offline storage, and annotation data are separate states
    so the reader can manage each without accidental data loss.
