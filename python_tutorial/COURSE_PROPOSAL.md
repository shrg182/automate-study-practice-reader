# Practical Python Foundations — Course Proposal

## Purpose

This document proposes an original Python tutorial course for the Reader app,
using Hans-Petter Halvorsen's *Python Programming* as a reference and sequencing
aid rather than reproducing the textbook.

- Reference PDF: [Python Programming](https://www.halvorsen.blog/documents/programming/python/resources/Python%20Programming.pdf)
- Author: Hans-Petter Halvorsen
- Examined edition: June 12, 2026
- Length: 143 pages
- Proposed course title: **Practical Python Foundations**
- Intended audience: beginning Python learners, including readers who benefit
  from English–Chinese study support

## Overall Recommendation

The PDF is suitable as a supporting textbook, but it should not be imported
verbatim or used as the sole curriculum.

The Reader course should:

1. Link to the original PDF and identify relevant page ranges.
2. Present original explanations, code examples, exercises, and solutions.
3. Preserve the useful beginner progression found in the PDF.
4. Reorganize topics into a clearer modern learning sequence.
5. Add current Python practices that receive little or no treatment in the PDF.
6. Use the Reader app's bilingual study pane for Chinese support, code, exercises,
   hints, notes, and references.

## Evaluation of the PDF

### Strengths

- Introduces Python gradually for beginners.
- Covers installation and running Python on common operating systems.
- Introduces variables, strings, functions, conditions, loops, classes, modules,
  files, exceptions, packages, mathematics, statistics, and plotting.
- Contains many short examples and self-paced exercises.
- Includes solutions to exercises near the end of the book.
- Provides companion source code, web resources, and videos through the
  author's website.
- Gives useful attention to numerical and scientific applications.
- Can serve as a stable external reading reference for each course lesson.

### Limitations

- Some material remains historically dated despite the 2026 edition. Examples
  include 2018 popularity surveys, the Windows 10 Store, Enthought Canopy, and
  Microsoft Azure Notebooks.
- A large portion of the book discusses distributions and individual editors.
  Beginners need some setup guidance, but not this much tool-specific material.
- Plotting is introduced before control flow, which is not the clearest sequence
  for a foundations course.
- Classes, exception handling, modules, and file handling are comparatively
  brief.
- The book emphasizes syntax examples more than problem decomposition, program
  design, testing, and complete projects.
- Some terminology and English prose would benefit from clarification for
  language learners.

### Modern Material to Add

The Reader course should add or strengthen:

- f-strings
- list, dictionary, and set comprehensions
- dictionaries and sets as core collection types
- `pathlib`
- `with open(...)` and context management
- structured CSV and JSON processing
- type hints
- dataclasses as an optional introduction
- automated tests
- assertions and debugging from tracebacks
- Git fundamentals
- project structure
- `.venv` virtual environments
- `python -m pip`
- dependency records such as `requirements.txt`
- separation of program logic from user input and output
- incremental development and refactoring

For environment and package guidance, the course should follow the
[Python Packaging User Guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/),
which recommends isolated project environments when using third-party packages.

## Proposed Course Structure

### Module 1 — Getting Ready

Topics:

- What Python is and where it is useful
- Installing a current Python 3 release
- Choosing one simple editor
- Terminal and command-prompt fundamentals
- Running the interactive interpreter
- Running a `.py` file
- Creating and activating `.venv`
- Reading errors without fear

Outcome: the learner can create a project folder and run a small Python program.

### Module 2 — Values, Variables, and Expressions

Topics:

- Integers and floating-point numbers
- Strings and Boolean values
- Variables and assignment
- Arithmetic and comparison operators
- Type conversion
- `input()` and `print()`
- f-strings
- Naming and formatting conventions

Outcome: the learner can write a small interactive calculation program.

### Module 3 — Decisions and Repetition

Topics:

- Boolean expressions
- `if`, `elif`, and `else`
- `for` loops
- `while` loops
- `range()`
- `break` and `continue`
- Nested control flow
- Avoiding infinite loops

Outcome: the learner can express conditional and repeated behavior clearly.

### Module 4 — Collections

Topics:

- Lists
- Tuples
- Dictionaries
- Sets
- Indexing and slicing
- Adding, updating, and removing values
- Iterating through collections
- Comprehensions
- Choosing the correct collection type

Outcome: the learner can organize and process groups of related values.

### Module 5 — Functions and Program Design

Topics:

- Defining and calling functions
- Parameters and arguments
- Return values
- Local and global scope
- Default and keyword arguments
- Docstrings
- Type hints
- Breaking a problem into smaller functions
- Separating calculations from input and display

Outcome: the learner can divide a program into reusable, testable components.

### Module 6 — Files and Reliable Programs

Topics:

- Paths and `pathlib`
- Reading and writing text with `with open(...)`
- CSV files
- JSON files
- Data validation
- Syntax errors and exceptions
- `try`, `except`, `else`, and `finally`
- Basic logging

Outcome: the learner can safely load, validate, transform, and save data.

### Module 7 — Classes and Data Models

Topics:

- Objects and classes
- Attributes and methods
- `__init__`
- Instance behavior
- Composition
- Choosing between a function, dictionary, and class
- Optional introduction to dataclasses

Outcome: the learner can represent a small real-world concept as a Python data
model without overusing classes.

### Module 8 — Modules, Environments, and Packages

Topics:

- Importing standard-library modules
- Creating a local module
- `if __name__ == "__main__"`
- Packages versus modules
- Virtual environments
- Installing packages with `python -m pip`
- Recording dependencies
- Reproducing a project environment

Outcome: the learner can organize a multi-file program and manage its
dependencies safely.

### Module 9 — Debugging and Testing

Topics:

- Reading tracebacks
- Reproducing a defect
- Strategic diagnostic output
- Editor debugger fundamentals
- Assertions
- Unit tests
- Testing ordinary cases and boundary cases
- Refactoring after tests pass

Outcome: the learner can investigate defects systematically and protect working
behavior with tests.

### Module 10 — Numerical Python

Topics:

- Standard-library mathematics
- NumPy arrays
- Basic descriptive statistics
- Matplotlib charts
- Separating data preparation from visualization
- Interpreting results rather than merely producing a graph

Outcome: the learner can perform and explain a small numerical analysis.

### Module 11 — Capstone Project

Recommended project: **Reader Selection Report**.

The learner builds a program that:

1. Opens a Reader selection JSON file.
2. Validates its required fields.
3. Counts selections, notes, terms, and source articles.
4. Groups results by collection or difficulty.
5. Writes a Markdown or CSV study report.
6. Handles missing or malformed data gracefully.
7. Includes automated tests for its core transformations.

This project connects Python instruction to the learner's existing Reader app
workflow while exercising files, JSON, collections, functions, validation,
exceptions, reporting, and tests.

## Reader App Information Architecture

Use three navigational levels:

```text
Practical Python Foundations
├── Module
│   ├── Lesson
│   ├── Guided lab
│   └── Exercises
└── Capstone project
```

The collection page should show modules first. Opening a module should reveal
its table of contents. The table of contents should then link to individual
lessons, labs, exercises, and project checkpoints.

## Recommended Lesson Template

Every lesson should include:

1. **Learning objectives** — two to four observable outcomes.
2. **Original English explanation** — concise and written for the Reader course.
3. **Chinese support** — explanatory support rather than an unreviewed literal
   translation.
4. **Vocabulary** — important Python and general English terms.
5. **Code examples** — small examples that can be copied and run.
6. **Prediction questions** — ask what the program will do before it is run.
7. **Guided lab** — a task completed in small verified steps.
8. **Independent exercise** — a related task without a complete walkthrough.
9. **Common mistakes** — likely errors and how to read their tracebacks.
10. **Checkpoint** — a short self-assessment.
11. **Hints and solutions** — separated from the exercise so they are not shown
    prematurely.
12. **References** — precise PDF pages and current official documentation.

## Study Pane Design

The bilingual study pane can be adapted for programming lessons with these tabs:

- **中文** — Chinese explanations and terminology support
- **代码** — copyable complete examples
- **练习** — the current guided or independent task
- **提示** — progressive hints
- **札记** — the learner's saved notes
- **参考** — PDF page ranges and official documentation

The existing five layout modes remain useful:

- English only
- English focus
- Balanced
- Study-pane focus
- Study pane only

For programming lessons, “study pane only” can be used to concentrate on code,
an exercise, or Chinese support. The slider should continue to allow custom
proportions and remember the learner's choice.

## Exercise Design Principles

- Exercises should be newly written for this course.
- Each exercise should concentrate on one main skill before combining skills.
- Examples should use meaningful names rather than unexplained single letters.
- Early exercises should provide sample input and expected output.
- Later exercises should require the learner to identify requirements and edge
  cases.
- Hints should be progressive: conceptual hint, structural hint, then partial
  code only when necessary.
- Complete solutions should explain decisions, not merely display code.
- More than one correct solution should be acknowledged when appropriate.
- Every module should end with a small usable program.

## Technical Baseline

- Target a current supported Python 3 release.
- Prefer standard-library solutions during the foundations modules.
- Use `.venv` for lessons that require third-party packages.
- Use UTF-8 consistently.
- Provide commands for both macOS/Linux and Windows when they differ.
- Keep code examples in separate `.py` files as well as displaying them in the
  Reader.
- Run every published example and automated test before release.
- Avoid depending on one editor except where an editor-specific lesson is
  explicitly identified.

## Copyright and Attribution

The examined PDF displays the author's copyright, and no open-content license
was identified during the evaluation. The public Reader course should therefore
not reproduce full chapters, illustrations, or exercise sets without permission.

The course should instead:

- Credit Hans-Petter Halvorsen and link to the original PDF.
- Reference relevant page ranges.
- Write original lesson explanations.
- Create original code examples, exercises, hints, and solutions.
- Use only brief quotations when necessary for commentary.
- Link to current official Python documentation for authoritative technical
  guidance.
- Record the source and purpose of every external image or substantial excerpt.

## Suggested Implementation Phases

### Phase 1 — Pilot

Build Modules 1 and 2 with:

- one collection page
- two module tables of contents
- four to six short lessons
- runnable example files
- bilingual study-pane tabs
- exercises and separate solutions
- local progress and notes

### Phase 2 — Core Programming

Add Modules 3 through 6 and validate the workflow with actual learner notes and
exported backups.

### Phase 3 — Program Structure

Add Modules 7 through 9, including modules, classes, environments, debugging,
and tests.

### Phase 4 — Applications

Add numerical Python and the Reader Selection Report capstone.

### Phase 5 — Review and Publication

- Run every example and test.
- Verify desktop and mobile layouts.
- Check English and Chinese terminology.
- Confirm source attribution and copyright compliance.
- Generate the course index.
- Publish the completed modules to the online Reader app.

## Acceptance Criteria for the Pilot

The pilot is ready for publication when:

- A new learner can install or locate Python and run the first program.
- Every displayed code example has been executed successfully.
- Exercises can be understood without consulting unpublished instructions.
- English-only, bilingual, and study-pane-only layouts work.
- Notes and progress survive a reload and an export/import cycle.
- Mobile controls do not obscure code or exercise text.
- PDF references link to the original source and identify page ranges.
- No copyrighted chapter or exercise has been reproduced wholesale.

## Final Recommendation

Proceed with an original Reader-native companion course rather than a direct PDF
conversion. The PDF should provide background, selected reading assignments, and
one perspective on sequencing. The Reader course should supply the modern
technical baseline, bilingual support, interactive study structure, original
practice, testing discipline, and capstone project.
