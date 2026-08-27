# Python Learning Path — Three-Level Book Plan

## Purpose

This book provides one continuous Python study path at three levels: Beginning,
Intermediate, and Advanced. Each level is a course in its own right, with a clear
entry point, completion standard, and project. Learners may stop after any level
or continue through the complete path.

The existing eleven-module **Practical Python Foundations** course is preserved
unchanged as the complete Beginning level. Its lesson URLs and Reader storage
keys remain stable, so existing annotations and study records are not disrupted.

## Level 1 — Beginning

**Published course:** Practical Python Foundations  
**Status:** Complete first edition — 11 modules

### Outcome

The learner can write, explain, test, and organize small Python programs; work
with files and JSON; model data; and complete a Reader selection-report project.

### Curriculum

1. Getting Ready
2. Values, Variables, and Expressions
3. Decisions and Repetition
4. Collections
5. Functions and Program Design
6. Files and Reliable Programs
7. Classes and Data Models
8. Modules, Environments, and Packages
9. Debugging and Testing
10. Numerical Python
11. Capstone: Reader Selection Report

[Open the complete Beginning course](../python_tutorial/index.html)

### Completion standard

- Run and modify every module example.
- Complete at least one independent exercise per module.
- Explain inputs, transformations, outputs, and failure cases.
- Produce and test the Reader Selection Report capstone.

## Level 2 — Intermediate

**Working title:** Practical Python Applications  
**Status:** Curriculum started; lesson production is the next phase

### Prerequisite

Completion of Level 1 or equivalent confidence with functions, collections,
files, classes, imports, exceptions, and basic tests.

### Outcome

The learner can design maintainable multi-module applications, interact with
web services and databases, process realistic datasets, and distribute a
tested command-line tool.

### Planned modules

1. Deeper Python: iterators, generators, comprehensions, and context managers
2. Type-driven design with modern annotations and static checking
3. Command-line applications with `argparse`, configuration, and logging
4. HTTP, APIs, serialization, timeouts, retries, and responsible data access
5. Relational data and SQLite transactions
6. Data analysis with NumPy and pandas
7. Visualization and evidence-based reporting
8. Application architecture, dependency boundaries, and refactoring
9. Testing systems: fixtures, mocks, integration tests, and coverage
10. Packaging, dependency management, documentation, and releases
11. Capstone: a tested Reader export analysis application

### Completion project

Create a packaged command-line application that imports Reader exports,
validates records, stores normalized data in SQLite, produces a Markdown or
HTML study report, and includes unit and integration tests.

## Level 3 — Advanced

**Working title:** Advanced Python Systems  
**Status:** Curriculum started; it follows the Intermediate course

### Prerequisite

Level 2 or equivalent experience building and testing multi-module Python
applications with APIs, databases, packaging, and typed interfaces.

### Outcome

The learner can reason about Python runtime behavior, concurrency, performance,
large-system boundaries, production reliability, and extensible architecture.

### Planned modules

1. Python's data model: protocols, descriptors, decorators, and metaclasses
2. Advanced typing: protocols, generics, overloads, and type-safe boundaries
3. Async I/O, task lifecycles, cancellation, and structured concurrency
4. Threads, processes, queues, and workload selection
5. Performance measurement, profiling, memory, and algorithmic tradeoffs
6. Streaming data and bounded-memory pipelines
7. Service design, schemas, authentication boundaries, and observability
8. Resilience: idempotency, retries, caching, and failure recovery
9. Secure Python: untrusted input, secrets, dependencies, and supply chains
10. Plugin architecture and extensible Reader tooling
11. Capstone: a production-grade Reader study-data service

### Completion project

Design an extensible service that ingests Reader study data, processes work in
bounded concurrent pipelines, exposes a typed interface, records operational
signals, survives repeat submissions, and includes performance and failure tests.

## Production sequence

1. Keep the Beginning course stable and improve it only through compatible revisions.
2. Produce the Intermediate modules and capstone as a separate course collection.
3. Pilot the Intermediate course before writing the complete Advanced course.
4. Build Advanced examples around measured constraints rather than artificial complexity.
5. Maintain this three-level book as the common table of contents and progression guide.

## 中文说明

本书采用三级学习路线：初级、 中级和高级。现有十一模块课程完整保留，作为初级课程；原有网址、批注和学习记录不受影响。中级课程着重实际应用、数据库、API、数据分析、测试与发布；高级课程着重并发、性能、类型系统、可靠性、安全性和可扩展架构。

建议学习者完成每一级的结业项目后再进入下一级。课程状态会明确区分“已发布”和“规划中”，避免把课程提纲误认为已经完成的教学内容。
