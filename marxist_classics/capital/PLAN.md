# *Capital* English-First Reader: Design and Implementation Plan

## Purpose

Build a close-reading environment for Karl Marx's *Capital* that develops English reading ability. The English text is primary. Chinese translations are optional aids, and commentary is a separately attributed research layer.

## Editorial principles

1. Never silently alter or summarize Marx's source text.
2. Keep five layers distinct: English source, Chinese correspondence, language assistance, conceptual assistance, and the reader's own notes.
3. Show Chinese only on request; English support comes first.
4. Label every edition, translator, source URL, and imported date.
5. Treat every companion as an interpretation, not an answer key.
6. Preserve exports as the durable record; browser storage is a working copy.

## Source policy

- Initial English base: Marxists Internet Archive's 1887 Samuel Moore and Edward Aveling translation, edited by Engels.
- Initial Chinese aid: the MIA Chinese text based on *Marx–Engels Collected Works*, Chinese first edition, volume 23 (People's Publishing House, 1972).
- Modern translations such as Ben Fowkes or Paul Reitter may be used only as privately owned reference editions unless redistribution permission is established.
- Credit MIA and retain the exact source URL on every unit.

## Information architecture

```text
Capital
└── Volume I
    ├── Prefaces and afterwords
    ├── Part I: Commodities and Money
    │   ├── Chapter 1: Commodities
    │   │   ├── §1 Two Factors of a Commodity
    │   │   ├── §2 Two-fold Character of Labour
    │   │   ├── §3 Form of Value
    │   │   └── §4 Commodity Fetishism
    │   ├── Chapter 2
    │   └── Chapter 3
    └── Parts II–VIII
```

One editor should represent roughly 20–45 minutes of close reading. Long chapters will be split by authored sections; short chapters can remain whole.

## Reading workflow

1. Read the English without translation.
2. Mark a difficulty as **language**, **concept**, or **reference/history**.
3. Use English vocabulary, syntax, and plain-English restatement first.
4. Reveal the corresponding Chinese passage only when needed.
5. Write a short English paraphrase before opening commentary.
6. Consult a named companion and record agreement, disagreement, or an unresolved question.

## Unit interface

- Main pane: immutable English reading view and opt-in editing view.
- Support drawer: vocabulary, clauses, technical senses, and pronunciation.
- Chinese drawer: manually checked paragraph-group correspondence; never automatic sentence replacement.
- Concept register: ordinary meaning versus Marx's technical use, with first occurrence and cross-references.
- Formula register: `C–M–C`, `M–C–M′`, `c`, `v`, `s`, and related transformations.
- Research shelf: primary support, guide, interpretation, historical background, contemporary application, and criticism.
- Reader response: English paraphrase, question, quotation, and source-linked research note.

## Initial companion shelf

- MIA Study Guide: https://www.marxists.org/archive/marx/works/1867-c1/guide/index.htm
- David Harvey's 2019 course and syllabus: https://peoplesforum.org/capitaldavidharvey/
- Harry Cleaver's study guide: https://www.la.utexas.edu/users/hcleaver/357k/357ksg.html
- Marx and Engels's prefaces, letters, and Engels's synopsis, treated as primary documents.

External material is linked and cited. It is not copied into the Reader unless its license permits redistribution.

## Pilot

The first reproducible pilot contains:

1. Preface to the First German Edition
2. Chapter 1 §1
3. Chapter 1 §2
4. Chapter 1 §3
5. Chapter 1 §4

The importer first preserves source HTML, then derives clean English text. Chinese source pages are preserved separately for later manual alignment. Each unit receives stable metadata and a Reader editor.

## Implementation phases

- **Phase 0 — foundation:** this plan, source catalog, reproducible importer, five English editors.
- **Phase 1 — language support:** seed technical vocabulary, difficulty classification, clause notes, and personal English paraphrases.
- **Phase 2 — Chinese alignment (in progress):** the five pilot units now include on-demand, section-aligned Chinese reference text with edition warnings and search-keyword fallbacks; paragraph-group concordance remains to be completed.
- **Phase 3 — research:** source cards, citation capture, saved searches, and companion links.
- **Phase 4 — course:** progress, review queue, concept graph, formula register, and collection-level offline download.
- **Phase 5 — expansion:** evaluate the pilot, then process the rest of Volume I by authored section.

## Decisions to make after actual use

- Whether the 1887 English is productive enough for language study or should serve only as an open reference beside a privately owned modern edition.
- Appropriate session length for Chapter 1 §3.
- How much Chinese is helpful before it begins to displace English reading.
- Whether companion materials should appear before or only after the reader's paraphrase.
- Which annotations belong to a shared collection dictionary and which belong only to one passage.
