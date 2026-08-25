#!/usr/bin/env python3
"""Generate the Practical Python Foundations lessons and Reader pages."""
from __future__ import annotations
from dataclasses import dataclass
from html import escape
from pathlib import Path
import re, sys

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent / "shiji" / "shiji_lisheng_lujia"))
from build_editor import build_html  # noqa: E402

@dataclass(frozen=True)
class Module:
    slug: str; title: str; pages: str; purpose: str; concepts: tuple[str, ...]
    code: str; lab: tuple[str, ...]; exercises: tuple[str, ...]; hints: tuple[str, ...]; solution: str; chinese: str

MODULES = (
 Module("01_getting_ready","Getting Ready","pp. 1–20","Establish the edit-run-observe cycle and identify the active interpreter.",("Run a script from a terminal.","Inspect the Python version and executable.","Use a project virtual environment.","Recognize a module entry point."),'''import platform
import sys

def environment_summary() -> str:
    return f"Python {platform.python_version()} at {sys.executable}"

if __name__ == "__main__":
    print("Hello, Python learner!")
    print(environment_summary())''',("Predict the two output lines.","Run `python3 example.py`.","Create and activate `.venv`, then run it again.","Explain why the executable path changed."),("Add the operating-system name.","Warn when Python is older than 3.10."),("Try `platform.system()`.","Compare `sys.version_info` with `(3, 10)`."),"Put the warning behind `if sys.version_info < (3, 10):`. Check `sys.executable`, not only the version number.","建立‘编辑—运行—观察’循环。关键词：解释器 interpreter、脚本 script、虚拟环境 virtual environment、入口 entry point。"),
 Module("02_values_variables_expressions","Values, Variables, and Expressions","pp. 21–52","Represent data clearly and combine values safely in a receipt program.",("Distinguish basic scalar types.","Choose meaningful variable names.","Use arithmetic and conversion deliberately.","Format results with f-strings."),'''def make_receipt(price: float, quantity: int, tax_rate: float = 0.06) -> str:
    subtotal = price * quantity
    tax = subtotal * tax_rate
    total = subtotal + tax
    return f"Subtotal: ${subtotal:.2f} | Tax: ${tax:.2f} | Total: ${total:.2f}"

if __name__ == "__main__":
    print(make_receipt(12.50, 3))''',("Predict every intermediate value.","Run and compare the result.","Add a discount before tax.","Reject a negative quantity."),("Return numeric results in a dictionary.","Convert a price supplied as text."),("Build a dictionary literal.","Catch `ValueError` from `float`."),"Validate inputs near the top. Compute `discounted = max(0, subtotal - discount)` and calculate tax from that value.","学习值、变量、表达式和类型转换。关键词：value、variable、expression、conversion、formatted output。"),
 Module("03_decisions_repetition","Decisions and Repetition","pp. 53–86","Use conditions and loops to create an actionable score summary.",("Branch with `if`, `elif`, and `else`.","Repeat with `for`.","Combine Boolean expressions.","Accumulate results explicitly."),'''def classify_scores(scores: list[int]) -> dict[str, int]:
    result = {"mastered": 0, "review": 0, "retry": 0}
    for score in scores:
        if score >= 85: result["mastered"] += 1
        elif score >= 60: result["review"] += 1
        else: result["retry"] += 1
    return result

if __name__ == "__main__":
    print(classify_scores([92, 74, 58, 85, 61]))''',("Trace the dictionary after each score.","Run and check the trace.","Reject scores outside 0–100.","Report the largest category."),("Use named threshold constants.","Write a three-step `while` countdown."),("Constants use uppercase names.","Decrease the counter each pass."),"Define `MASTERY_SCORE` and `REVIEW_SCORE`. Raise `ValueError` before classifying an invalid score.","用条件分支做选择，用循环处理数据。关键词：condition、branch、iteration、accumulator、boundary。"),
 Module("04_collections","Collections","pp. 87–120","Choose appropriate collections and build a word-frequency analyzer.",("Use lists for ordered mutable items.","Use tuples for fixed records.","Use dictionaries for lookup.","Use sets for uniqueness."),'''import re

def word_frequencies(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in re.findall(r"[A-Za-z']+", text.lower()):
        counts[word] = counts.get(word, 0) + 1
    return counts

if __name__ == "__main__":
    print(sorted(word_frequencies("Read code, run code, explain code.").items()))''',("List the extracted words.","Explain lowercase normalization.","Find the five most frequent words.","Report unique vocabulary size."),("Exclude common stop words.","Group words by first letter."),("Test membership in a set.","Try `setdefault`."),"Filter before incrementing. For grouping, use `groups.setdefault(word[0], []).append(word)`.","比较 list、tuple、dictionary、set；选择时考虑顺序、修改、查找和去重。"),
 Module("05_functions_program_design","Functions and Program Design","pp. 121–154","Decompose a problem into focused functions with explicit contracts.",("Give functions one responsibility.","Prefer parameters and returns to globals.","Document contracts with hints and docstrings.","Raise useful exceptions."),'''def summarize(values: list[float]) -> dict[str, float]:
    """Return statistics for a non-empty list."""
    if not values: raise ValueError("values must not be empty")
    return {"minimum": min(values), "maximum": max(values),
            "average": sum(values) / len(values)}

if __name__ == "__main__":
    print(summarize([4.0, 7.5, 8.5]))''',("Write the contract in one sentence.","Test an ordinary case by hand.","Test the empty-list error.","Separate formatting from calculation."),("Add median.","Extract reusable validation."),("Use `statistics.median`.","Validate before calculation."),"Add median to the returned dictionary. Keep printing outside `summarize` so the function stays reusable and testable.","强调函数契约：输入、输出和错误。关键词：parameter、return value、scope、contract、exception。"),
 Module("06_files_reliable_programs","Files and Reliable Programs","pp. 155–190","Persist structured data with pathlib and JSON while validating boundaries.",("Use `Path` for filesystem paths.","Specify text encoding.","Serialize data as JSON.","Give malformed input useful errors."),'''import json
from pathlib import Path
from tempfile import TemporaryDirectory

def save(path: Path, record: dict[str, object]) -> None:
    if "title" not in record: raise ValueError("record requires a title")
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        path = Path(folder) / "study.json"
        save(path, {"title": "Python", "complete": False})
        print(json.loads(path.read_text(encoding="utf-8")))''',("Trace dictionary-to-file-to-dictionary.","Inspect the JSON text.","Handle broken JSON.","Require a Boolean `complete` field."),("Save a list of records.","Write a temporary file and replace the target."),("Validate every list item.","Review `Path.replace`."),"Catch `json.JSONDecodeError` only where you can add path context. Validate types; do not silently invent required data.","处理文件和 JSON。关键词：path、encoding、serialization、validation、exception handling。"),
 Module("07_classes_data_models","Classes and Data Models","pp. 191–224","Model a study item with a dataclass and methods that protect its state.",("Combine related data and behavior.","Reduce boilerplate with `@dataclass`.","Express valid state explicitly.","Prefer composition to deep inheritance."),'''from dataclasses import dataclass

@dataclass
class StudyItem:
    title: str
    minutes: int
    reviewed: bool = False
    def mark_reviewed(self) -> None: self.reviewed = True
    def label(self) -> str:
        return f"[{'done' if self.reviewed else 'next'}] {self.title} ({self.minutes} min)"

if __name__ == "__main__":
    item = StudyItem("Functions", 25)
    print(item.label()); item.mark_reviewed(); print(item.label())''',("Identify state and behavior.","Create three items.","Reject non-positive minutes in `__post_init__`.","Calculate total minutes outside the item."),("Add optional notes.","Compose a `StudyPlan` from items."),("Use `str | None`.","Store `list[StudyItem]`."),"Raise in `__post_init__` when `minutes <= 0`. Put plan-wide calculations in a separate `StudyPlan`.","用数据类组合数据和行为。关键词：class、instance、field、method、dataclass、composition。"),
 Module("08_modules_environments_packages","Modules, Environments, and Packages","pp. 225–254","Organize importable code and make its environment reproducible.",("Separate reusable code from entry behavior.","Understand modules and packages.","Use per-project environments.","Record direct dependencies."),'''import platform
import sys

def runtime_report() -> dict[str, str]:
    return {"python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable}

if __name__ == "__main__":
    for key, value in runtime_report().items(): print(f"{key}: {value}")''',("Run inside and outside `.venv`.","Move the function to another module and import it.","Declare only dependencies actually used.","Explain `python -m pip`."),("Create a package with `__init__.py`.","Add `__main__.py`."),("Use an absolute package import.","Run `python -m package`."),"Keep definitions importable and demonstrations under the main guard. Recreate environments from dependency declarations.","说明 module、package、dependency 和 virtual environment。`python -m pip` 可确保目标解释器一致。"),
 Module("09_debugging_testing","Debugging and Testing","pp. 255–286","Convert specifications into automated tests and treat failures as evidence.",("Reproduce defects minimally.","Read tracebacks from the last line upward.","Test boundaries.","Keep tests deterministic."),'''import unittest

def normalize_score(value: float, maximum: float = 100.0) -> float:
    if maximum <= 0: raise ValueError("maximum must be positive")
    if not 0 <= value <= maximum: raise ValueError("value outside range")
    return value / maximum

class Tests(unittest.TestCase):
    def test_middle(self): self.assertAlmostEqual(normalize_score(75), .75)
    def test_invalid_maximum(self):
        with self.assertRaises(ValueError): normalize_score(1, 0)

if __name__ == "__main__": unittest.main()''',("State the rules.","Run with `-v`.","Test zero, maximum, and out-of-range values.","Introduce and then repair a defect."),("Test a non-100 maximum.","Name a regression test after behavior."),("Five of twenty is 0.25.","Test observable behavior."),"Assert both boundaries and use `assertRaises` for negative and over-maximum values.","把需求变成测试。关键词：debugging、traceback、assertion、boundary test、regression test。"),
 Module("10_numerical_python","Numerical Python","pp. 287–326","Build transparent statistics and recognize when numerical libraries add value.",("Use `statistics` for small data.","Separate calculation and display.","Recognize vectorization use cases.","Label units and precision."),'''from statistics import mean, median, pstdev

def reading_report(minutes: list[float]) -> dict[str, float]:
    if not minutes: raise ValueError("at least one session is required")
    return {"sessions": float(len(minutes)), "mean": mean(minutes),
            "median": median(minutes), "spread": pstdev(minutes)}

if __name__ == "__main__":
    for name, value in reading_report([20, 35, 25, 40]).items():
        print(f"{name}: {value:.2f}")''',("Compute mean and median by hand.","Interpret spread.","Add minimum and maximum.","Sketch a labeled bar chart."),("Compare two weeks.","Optionally reproduce with NumPy."),("Compare matching report keys.","Keep NumPy optional."),"Add `min` and `max`. Keep the core standard-library-only; install NumPy or Matplotlib in `.venv` for extensions.","先用标准库统计，再按需要用 NumPy。关键词：mean、median、standard deviation、array、visualization。"),
 Module("11_capstone_selection_report","Capstone: Reader Selection Report","pp. 327–354","Combine course skills in a report for Reader selection JSON exports.",("Inspect external JSON shapes.","Normalize records.","Aggregate study measures.","Test edge cases and render readable output."),'''from collections import Counter

def build_report(payload: dict[str, object]) -> dict[str, object]:
    raw = payload.get("selections", [])
    if not isinstance(raw, list): raise ValueError("selections must be a list")
    records = [item for item in raw if isinstance(item, dict)]
    colors = Counter(str(item.get("color", "unlabeled")) for item in records)
    words = sum(len(str(item.get("text", "")).split()) for item in records)
    return {"selection_count": len(records), "word_count": words, "colors": dict(colors)}

if __name__ == "__main__":
    sample = {"selections": [{"text": "Functions return values", "color": "yellow"},
                              {"text": "Validate file input", "color": "blue"}]}
    print(build_report(sample))''',("Predict the sample report.","Run and reconcile it.","Load a real export.","Render counts and quotations as Markdown."),("Group by source title.","Add `argparse` paths.","Test missing, empty, and malformed selections."),("Try `defaultdict(list)`.","Separate load, validate, aggregate, and render."),"Build `load_payload`, `validate_records`, `build_report`, and `render_markdown` separately; test pure functions before file I/O.","综合处理 Reader selection JSON。关键词：payload、record、normalize、aggregate、report。先验证，再统计。"),
)

def inline(text: str) -> str:
    text = escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return re.sub(r"\[([^]]+)]\((https?://[^)]+)\)", lambda m: f'<a href="{m.group(2)}" target="_blank" rel="noreferrer">{m.group(1)}</a>', text)

def markdown_html(md: str) -> str:
    out=[]; para=[]; listing=""; code=[]; in_code=False
    def flush():
        if para: out.append(f"<p>{inline(' '.join(para))}</p>"); para.clear()
    def close():
        nonlocal listing
        if listing: out.append(f"</{listing}>"); listing=""
    for line in md.splitlines():
        if line.startswith("```"):
            flush(); close()
            if in_code: out.append(f"<pre><code>{escape(chr(10).join(code))}</code></pre>"); code.clear()
            in_code=not in_code; continue
        if in_code: code.append(line); continue
        if not line.strip(): flush(); close(); continue
        h=re.match(r"^(#{1,3})\s+(.+)",line); b=re.match(r"^-\s+(.+)",line); n=re.match(r"^\d+\.\s+(.+)",line)
        if h: flush(); close(); level=len(h.group(1))+1; out.append(f"<h{level}>{inline(h.group(2))}</h{level}>"); continue
        if b or n:
            flush(); kind="ul" if b else "ol"
            if listing != kind: close(); out.append(f"<{kind}>"); listing=kind
            out.append(f"<li>{inline((b or n).group(1))}</li>"); continue
        close(); para.append(line.strip())
    flush(); close(); return "\n".join(out)

def reader(md: str, title: str, source: str, key: str, stem: str, home: str, theme: str, library: str) -> str:
    plain=re.sub(r"[`#*_\[\]()]","",md)
    page=build_html(plain,[],source,chapter_title=title,editor_title=f"{title} · Reader",storage_key=key,file_stem=stem,inline_notes=[],review_notes=[],reading_notes=[],global_terms=[],home_href=home,theme_href=theme,shared_library_href=library,shared_library_label="Python Course",source_site_label="Source Markdown")
    page,count=re.subn(r'(<section id="editor" class="editor"[^>]*>)[\s\S]*?(</section>)',rf"\1{markdown_html(md)}\2",page,count=1)
    if count != 1: raise RuntimeError("editor body not found")
    css='''<style>#editor{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.75}#editor h2{margin:2em 0 .6em;border-bottom:1px solid var(--line)}#editor h3{color:var(--blue)}#editor p{margin:.75em 0;text-indent:0}#editor li{margin:.35em 0}#editor code{background:#eef1f4;padding:.12em .35em;border-radius:4px}#editor pre{padding:16px;border:1px solid #d4dbe2;border-radius:8px;background:#f6f8fa;overflow:auto;white-space:pre}#editor pre code{padding:0;background:transparent}</style>'''
    return page.replace("</head>",css+"</head>",1)

def lesson(number: int, m: Module) -> str:
    bullets=lambda xs:"\n".join(f"- {x}" for x in xs); steps=lambda xs:"\n".join(f"{i}. {x}" for i,x in enumerate(xs,1))
    return f'''# Module {number}: {m.title}

## Purpose

{m.purpose}

## Learning objectives

{bullets(m.concepts)}

## Core lesson

Read code as data moving through explicit decisions. Before running the example, identify inputs, predict output, and locate validation. Execute it and use differences between prediction and result to refine your mental model.

Keep each program small enough to explain from top to bottom. Names reveal intent, functions expose inputs and outputs, and demonstrations belong under the main guard. These habits scale to the capstone.

## Runnable example

```python
{m.code}
```

Run `python3 example.py` from this lesson directory.

## Guided lab

{steps(m.lab)}

## Independent practice

{steps(m.exercises)}

## Hints

{bullets(m.hints)}

## Solution guidance

{m.solution}

## 中文学习支持

{m.chinese}

学习方法：先用英文说明输入、处理和输出，再用中文复述；最后修改一个条件并预测结果。

## Textbook cross-reference

Supporting reference: Hans-Petter Halvorsen, *Python Programming*, {m.pages}. Page numbers refer to the linked PDF edition; this lesson and its exercises are original course material.

[Open the supporting PDF](https://www.halvorsen.blog/documents/programming/python/resources/Python%20Programming.pdf)
'''

def landing() -> str:
    items="".join(f'<li><b>{i:02d}</b><div><strong>{escape(m.title)}</strong><small>{escape(m.purpose)} · {escape(m.pages)}</small><nav><a href="modules/{m.slug}/editor.html?view=annotated">Open lesson</a> · <a href="modules/{m.slug}/lesson.md">Markdown</a> · <a href="modules/{m.slug}/example.py">Example</a></nav></div></li>' for i,m in enumerate(MODULES,1))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Practical Python Foundations</title><link rel="stylesheet" href="../workspace_theme.css"><script src="../workspace_skin.js"></script><style>*{{box-sizing:border-box}}body{{margin:0;background:#f1f3f4;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#202124}}main{{width:min(1040px,calc(100% - 28px));margin:32px auto}}header,section{{padding:28px;border-radius:14px;background:#fff;margin-bottom:20px}}header{{background:linear-gradient(135deg,#143a56,#176b63);color:white}}h1{{font-size:clamp(30px,5vw,52px);margin:.2em 0}}header p{{max-width:760px;line-height:1.6}}header a{{display:inline-block;background:white;color:#174ea6;padding:9px 13px;border-radius:20px;margin:4px;text-decoration:none;font-weight:700}}.status{{color:#b7f0d4}}ol{{list-style:none;padding:0;display:grid;gap:9px}}li{{display:flex;gap:14px;padding:14px;border:1px solid #dadce0;border-radius:9px}}li>b{{display:grid;place-items:center;flex:0 0 38px;height:38px;border-radius:50%;background:#e8f0fe;color:#174ea6}}li div{{display:grid;gap:5px}}small{{color:#5f6368}}nav a{{color:#174ea6;text-decoration:none}}@media(max-width:600px){{header,section{{padding:20px}}}}</style></head><body><main><header><span class="status">First edition · 11 modules published</span><h1>Practical Python Foundations</h1><p>Original English lessons with Chinese study support, runnable examples, guided labs, exercises, and a Reader Selection Report capstone.</p><a href="modules/01_getting_ready/editor.html?view=annotated">Start Module 1</a><a href="course_proposal/editor.html?view=annotated">Course proposal</a></header><section><h2>How to study</h2><p>Predict, run <code>python3 example.py</code>, explain the result, complete the lab, and attempt independent practice before consulting solution guidance.</p></section><section><h2>Modules</h2><ol>{items}</ol></section></main></body></html>'''

def main() -> None:
    proposal=(BASE/"COURSE_PROPOSAL.md").read_text(encoding="utf-8"); folder=BASE/"course_proposal"; folder.mkdir(exist_ok=True)
    (folder/"editor.html").write_text(reader(proposal,"Practical Python Foundations — Course Proposal","../COURSE_PROPOSAL.md","python-tutorial-course-proposal-v1","python_tutorial_course_proposal","../../index.html","../../workspace_theme.css","../index.html"),encoding="utf-8")
    for i,m in enumerate(MODULES,1):
        folder=BASE/"modules"/m.slug; folder.mkdir(parents=True,exist_ok=True); md=lesson(i,m)
        (folder/"lesson.md").write_text(md,encoding="utf-8"); (folder/"example.py").write_text(m.code+"\n",encoding="utf-8")
        page = reader(md,f"Module {i}: {m.title}","lesson.md",f"python-tutorial-{m.slug}-v1",f"python_tutorial_{m.slug}","../../../index.html","../../../workspace_theme.css","../../index.html")
        page = page.replace('../../../project_dictionary/', '../../../../project_dictionary/')
        (folder/"editor.html").write_text(page,encoding="utf-8")
    (BASE/"index.html").write_text(landing(),encoding="utf-8"); print(f"Built {len(MODULES)} modules")

if __name__ == "__main__": main()
