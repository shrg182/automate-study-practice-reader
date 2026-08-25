#!/usr/bin/env python3
"""Build the single three-level Python book."""
from __future__ import annotations
from dataclasses import dataclass
from html import escape
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
OLD = BASE.parent / "python_tutorial"
sys.path.insert(0, str(OLD))
from build_course import MODULES as BEGINNING  # noqa: E402

AUTHOR = "Codex (OpenAI)"

@dataclass(frozen=True)
class Lesson:
    slug: str
    title: str
    focus: str
    code: str


INTERMEDIATE = (
 Lesson("01_iterators_generators", "Iterators and Generators", "Build lazy, composable pipelines and understand the iterator protocol.", '''def batched(source, size):
    batch = []
    for item in source:
        batch.append(item)
        if len(batch) == size:
            yield tuple(batch); batch.clear()
    if batch: yield tuple(batch)

if __name__ == "__main__": print(list(batched(range(7), 3)))'''),
 Lesson("02_context_managers", "Context Managers and Resource Safety", "Express setup and cleanup as a reliable protocol.", '''from contextlib import contextmanager

@contextmanager
def study_session(name):
    print(f"start: {name}")
    try: yield
    finally: print(f"finish: {name}")

if __name__ == "__main__":
    with study_session("typing"): print("practice")'''),
 Lesson("03_type_driven_design", "Type-Driven Design", "Use dataclasses, unions, and protocols to make boundaries explicit.", '''from dataclasses import dataclass
from typing import Protocol

class Renderable(Protocol):
    def render(self) -> str: ...

@dataclass
class Note:
    text: str
    def render(self) -> str: return f"- {self.text}"

def publish(item: Renderable) -> str: return item.render()
if __name__ == "__main__": print(publish(Note("Review protocols")))'''),
 Lesson("04_command_line_apps", "Command-Line Applications", "Design testable commands with parsing separated from execution.", '''import argparse

def parser():
    value = argparse.ArgumentParser()
    value.add_argument("--minutes", type=int, default=25)
    return value

def run(minutes): return f"Study for {minutes} minutes"
if __name__ == "__main__": print(run(parser().parse_args().minutes))'''),
 Lesson("05_http_apis", "HTTP APIs and Defensive Clients", "Construct requests, validate responses, and plan for timeouts and retries.", '''from urllib.request import Request

def make_request(url, token=None):
    headers = {"Accept": "application/json"}
    if token: headers["Authorization"] = f"Bearer {token}"
    return Request(url, headers=headers)

if __name__ == "__main__": print(dict(make_request("https://example.com/data").header_items()))'''),
 Lesson("06_sqlite", "Relational Data and SQLite", "Use schemas, parameters, transactions, and queries safely.", '''import sqlite3

def demo():
    db = sqlite3.connect(":memory:")
    db.execute("create table note(id integer primary key, text text not null)")
    db.execute("insert into note(text) values (?)", ("Read transactions",))
    return db.execute("select text from note").fetchone()[0]
if __name__ == "__main__": print(demo())'''),
 Lesson("07_data_analysis", "Data Analysis Pipelines", "Clean, aggregate, and explain tabular data before adding third-party tools.", '''from collections import defaultdict

def totals(rows):
    result = defaultdict(int)
    for row in rows: result[row["topic"]] += row["minutes"]
    return dict(result)

if __name__ == "__main__": print(totals([{"topic":"Python","minutes":20},{"topic":"Python","minutes":15}]))'''),
 Lesson("08_visual_reporting", "Visualization and Reporting", "Choose encodings that communicate comparisons without distorting them.", '''def bars(values, width=20):
    largest = max(values.values(), default=1)
    return "\n".join(f"{name:10} {'#' * round(value/largest*width)} {value}" for name, value in values.items())
if __name__ == "__main__": print(bars({"reading": 30, "coding": 45, "testing": 15}))'''),
 Lesson("09_architecture_refactoring", "Application Architecture and Refactoring", "Separate domain rules, adapters, and presentation.", '''def completion(done, total):
    if total <= 0: raise ValueError("total must be positive")
    return done / total

def format_completion(value): return f"{value:.0%} complete"
if __name__ == "__main__": print(format_completion(completion(7, 10)))'''),
 Lesson("10_testing_systems", "Testing Systems", "Combine unit, integration, fixture, and mock-based tests deliberately.", '''import unittest
from unittest.mock import Mock

def notify(sender, message): sender(message)
class Tests(unittest.TestCase):
    def test_notify(self):
        sender = Mock(); notify(sender, "done"); sender.assert_called_once_with("done")
if __name__ == "__main__": unittest.main()'''),
 Lesson("11_capstone_reader_analytics", "Capstone: Reader Analytics CLI", "Build a typed, tested CLI that validates exports, stores SQLite data, and renders reports.", '''import json

def summarize(raw):
    data = json.loads(raw); rows = data.get("selections", [])
    if not isinstance(rows, list): raise ValueError("selections must be a list")
    return {"count": len(rows), "characters": sum(len(str(x.get("text", ""))) for x in rows if isinstance(x, dict))}
if __name__ == "__main__": print(summarize('{"selections":[{"text":"Python"}]}'))'''),
)

ADVANCED = (
 Lesson("01_python_data_model", "Python's Data Model", "Use protocols, special methods, descriptors, and decorators with restraint.", '''class Positive:
    def __set_name__(self, owner, name): self.name = "_" + name
    def __get__(self, obj, owner): return getattr(obj, self.name)
    def __set__(self, obj, value):
        if value <= 0: raise ValueError("must be positive")
        setattr(obj, self.name, value)
class Task:
    minutes = Positive()
    def __init__(self, minutes): self.minutes = minutes
if __name__ == "__main__": print(Task(25).minutes)'''),
 Lesson("02_advanced_typing", "Advanced Typing", "Model reusable interfaces with generics, protocols, and type-safe boundaries.", '''from typing import Generic, TypeVar
T = TypeVar("T")
class Stack(Generic[T]):
    def __init__(self): self._items: list[T] = []
    def push(self, item: T) -> None: self._items.append(item)
    def pop(self) -> T: return self._items.pop()
if __name__ == "__main__":
    stack = Stack[str](); stack.push("types"); print(stack.pop())'''),
 Lesson("03_asyncio", "Async I/O and Cancellation", "Manage task lifecycles, timeouts, cancellation, and structured concurrency.", '''import asyncio

async def fetch(name, delay):
    await asyncio.sleep(delay); return name
async def main():
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(fetch(str(i), .01)) for i in range(3)]
    print([task.result() for task in tasks])
if __name__ == "__main__": asyncio.run(main())'''),
 Lesson("04_parallelism", "Threads, Processes, and Workloads", "Match concurrency mechanisms to blocking I/O and CPU-bound work.", '''from concurrent.futures import ThreadPoolExecutor

def square(value): return value * value
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=3) as pool: print(list(pool.map(square, range(6))))'''),
 Lesson("05_performance", "Profiling and Performance", "Measure before optimizing and connect profiles to algorithmic cost.", '''from cProfile import Profile

def workload(): return sum(i * i for i in range(10000))
if __name__ == "__main__":
    with Profile() as profile: print(workload())
    profile.print_stats(sort="cumulative")'''),
 Lesson("06_streaming", "Streaming and Bounded Memory", "Process large inputs incrementally with backpressure-aware stages.", '''def nonempty(lines):
    for line in lines:
        value = line.strip()
        if value: yield value
if __name__ == "__main__": print(list(nonempty([" alpha ", "", " beta"])))'''),
 Lesson("07_service_design", "Service Design and Schemas", "Define stable service boundaries, schemas, errors, and operational signals.", '''from dataclasses import dataclass

@dataclass(frozen=True)
class Request:
    text: str
def handle(request):
    if not request.text.strip(): return {"status": 400, "error": "text required"}
    return {"status": 200, "words": len(request.text.split())}
if __name__ == "__main__": print(handle(Request("typed service boundary")))'''),
 Lesson("08_resilience", "Resilience and Idempotency", "Design retries, caching, idempotency, and recovery as explicit policies.", '''def retry(operation, attempts=3):
    error = None
    for _ in range(attempts):
        try: return operation()
        except RuntimeError as caught: error = caught
    raise error
if __name__ == "__main__": print(retry(lambda: "completed"))'''),
 Lesson("09_security", "Secure Python Boundaries", "Treat input, secrets, dependencies, and serialization as trust boundaries.", '''import hmac
from hashlib import sha256

def sign(message, secret): return hmac.new(secret, message, sha256).hexdigest()
if __name__ == "__main__": print(sign(b"reader-export", b"demo-only-secret"))'''),
 Lesson("10_plugins", "Plugin Architecture", "Discover extensions through explicit contracts and controlled loading.", '''from typing import Protocol
class Plugin(Protocol):
    name: str
    def transform(self, text: str) -> str: ...
class Uppercase:
    name = "uppercase"
    def transform(self, text): return text.upper()
def apply(plugin: Plugin, text): return plugin.transform(text)
if __name__ == "__main__": print(apply(Uppercase(), "plugin contract"))'''),
 Lesson("11_capstone_reader_service", "Capstone: Reader Study-Data Service", "Build a typed, observable, resilient service with bounded concurrent ingestion.", '''import asyncio

async def normalize(queue, output):
    while (item := await queue.get()) is not None:
        output.append(str(item).strip()); queue.task_done()
async def main():
    queue = asyncio.Queue(maxsize=2); output = []
    worker = asyncio.create_task(normalize(queue, output))
    for item in [" notes ", " highlights "]: await queue.put(item)
    await queue.put(None); await worker; print(output)
if __name__ == "__main__": asyncio.run(main())'''),
)

def markdown(level: str, number: int, title: str, focus: str, code: str) -> str:
    return f'''# {level} {number}: {title}

**Author: {AUTHOR}**

## Purpose

{focus}

## Learning objectives

- Explain the central abstraction and its tradeoffs.
- Run, trace, test, and modify the example.
- Separate domain logic from input, output, and infrastructure.
- Recognize failure modes and validate boundaries.

## Lesson

Begin with a precise contract: identify the input, result, side effects, and possible failures. Read the example before running it. Trace the state changes, predict the output, and then use execution as evidence. Prefer the simplest design that preserves clarity, testability, and explicit ownership of resources.

The feature in this module is useful only when it reduces complexity at the system boundary. Keep the core calculation small, isolate external effects, and make cleanup and error behavior visible. Add abstractions after repeated concrete cases demonstrate a need.

## Runnable example

```python
{code}
```

Run `python3 example.py` from this module directory.

## Guided lab

1. Predict the output and identify every state transition.
2. Run the example and explain any difference from the prediction.
3. Add validation for one invalid or boundary input.
4. Extract one pure function and write a focused test for it.
5. Record one design tradeoff and one alternative implementation.

## Independent practice

1. Adapt the example to Reader study data.
2. Add structured error reporting without hiding the original cause.
3. Measure or test the property that matters most for this module.

## Hints

- Keep computation independent from display and file access.
- Prefer deterministic inputs in tests.
- Document why an abstraction exists, not merely how it is written.

## Solution guidance

A sound solution has a narrow public interface, validates data once at the boundary, and leaves the central transformation easy to test. Confirm ordinary, empty, boundary, and malformed cases. For extensions involving external services or optional packages, keep the standard-library example runnable and isolate the adapter.

## Completion check

You can complete this module when you can explain the design without reading the code, reproduce it in a smaller example, and justify where errors, cleanup, and tests belong.
'''

def beginning_markdown(number, module):
    base = markdown("Beginning", number, module.title, module.purpose, module.code)
    return base.replace("## Lesson\n", "## Lesson\n\n" + "\n".join(f"- {item}" for item in module.concepts) + "\n\n")

def build_module(level, number, slug, title, focus, code):
    folder = BASE / "levels" / level.lower() / slug; folder.mkdir(parents=True, exist_ok=True)
    text = markdown(level, number, title, focus, code) if level != "Beginning" else focus
    (folder / "lesson.md").write_text(text, encoding="utf-8")
    (folder / "example.py").write_text(code + "\n", encoding="utf-8")
    body = escape(text)
    key = f"python-{level.lower()}-{slug}-v1"
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(level)} {number}: {escape(title)}</title><style>*{{box-sizing:border-box}}body{{margin:0;background:#f1f3f4;color:#202124;font-family:system-ui}}header{{position:sticky;top:0;z-index:2;display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:10px 16px;background:#fff;border-bottom:1px solid #dadce0}}header strong{{margin-right:auto}}a,button{{padding:7px 10px;border:1px solid #c8ccd0;border-radius:7px;background:#fff;color:#174ea6;text-decoration:none;font:inherit;cursor:pointer}}main{{width:min(980px,calc(100% - 24px));margin:18px auto;background:#fff;border:1px solid #dadce0;border-radius:12px;overflow:hidden}}h1{{margin:0;padding:24px 28px 0}}.byline{{padding:0 28px;color:#5f6368}}textarea{{display:block;width:100%;min-height:calc(100vh - 180px);padding:28px;border:0;border-top:1px solid #e5e7e9;resize:vertical;color:#202124;background:#fff;font:17px/1.75 ui-monospace,SFMono-Regular,Menlo,monospace}}@media(max-width:600px){{h1,.byline,textarea{{padding-left:16px;padding-right:16px}}}}</style></head><body><header><strong>Python · {escape(level)}</strong><a href="../../../index.html">Course contents</a><a href="../../../../index.html">Reader library</a><button id="save">Save</button><button id="download">Download Markdown</button></header><main><h1>{escape(level)} {number}: {escape(title)}</h1><p class="byline">Author: {AUTHOR}</p><textarea id="lesson" spellcheck="false">{body}</textarea></main><script>const area=document.querySelector('#lesson'),key={key!r};area.value=localStorage.getItem(key)||area.value;document.querySelector('#save').onclick=()=>localStorage.setItem(key,area.value);document.querySelector('#download').onclick=()=>{{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([area.value],{{type:'text/markdown'}}));a.download='lesson.md';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),500)}};area.addEventListener('input',()=>localStorage.setItem(key,area.value));</script></body></html>'''
    (folder / "editor.html").write_text(page, encoding="utf-8")

def landing():
    def cards(level, lessons):
        return "".join(f'<li><b>{i:02d}</b><div><strong>{escape(m.title)}</strong><small>{escape(m.purpose if hasattr(m,"purpose") else m.focus)}</small><a href="levels/{level}/{m.slug}/editor.html?view=annotated">Open module</a></div></li>' for i,m in enumerate(lessons,1))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Python</title><link rel="stylesheet" href="../workspace_theme.css"><script src="../workspace_skin.js"></script><style>*{{box-sizing:border-box}}body{{margin:0;background:#f1f3f4;font-family:system-ui;color:#202124}}main{{width:min(1100px,calc(100% - 28px));margin:30px auto}}header,section{{padding:28px;margin-bottom:18px;border-radius:14px;background:#fff}}header{{color:#fff;background:linear-gradient(135deg,#30245f,#176b63)}}h1{{margin:.1em 0;font-size:clamp(38px,7vw,70px)}}header p{{max-width:760px;line-height:1.6}}.author{{font-weight:700;color:#c9f3e1}}details{{margin:12px 0;border:1px solid #dadce0;border-radius:10px}}summary{{padding:16px;cursor:pointer;font-size:22px;font-weight:750}}ol{{display:grid;gap:8px;padding:0 16px 16px;list-style:none}}li{{display:flex;gap:12px;padding:12px;border:1px solid #e1e5e9;border-radius:8px}}li>b{{display:grid;place-items:center;width:35px;height:35px;border-radius:50%;background:#e8f0fe;color:#174ea6}}li div{{display:grid;gap:4px}}small{{color:#5f6368}}a{{color:#174ea6;font-weight:700;text-decoration:none}}</style></head><body><main><header><p class="author">Author: {AUTHOR}</p><h1>Python</h1><p>A complete three-level course: 33 modules from first programs to maintainable applications and advanced Python systems.</p></header><section><details open><summary>Beginning · 11 modules</summary><ol>{cards('beginning',BEGINNING)}</ol></details><details><summary>Intermediate · 11 modules</summary><ol>{cards('intermediate',INTERMEDIATE)}</ol></details><details><summary>Advanced · 11 modules</summary><ol>{cards('advanced',ADVANCED)}</ol></details></section></main></body></html>'''

def main():
    for i,m in enumerate(BEGINNING,1): build_module("Beginning",i,m.slug,m.title,beginning_markdown(i,m),m.code)
    for level,items in (("Intermediate",INTERMEDIATE),("Advanced",ADVANCED)):
        for i,m in enumerate(items,1): build_module(level,i,m.slug,m.title,m.focus,m.code)
    (BASE/"index.html").write_text(landing(),encoding="utf-8")
    print("Built Python: 3 levels, 33 modules")

if __name__ == "__main__": main()
