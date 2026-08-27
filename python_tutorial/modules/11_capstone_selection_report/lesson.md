# Module 11: Capstone: Reader Selection Report

## Purpose

Combine course skills in a report for Reader selection JSON exports.

## Learning objectives

- Inspect external JSON shapes.
- Normalize records.
- Aggregate study measures.
- Test edge cases and render readable output.

## Core lesson

Read code as data moving through explicit decisions. Before running the example, identify inputs, predict output, and locate validation. Execute it and use differences between prediction and result to refine your mental model.

Keep each program small enough to explain from top to bottom. Names reveal intent, functions expose inputs and outputs, and demonstrations belong under the main guard. These habits scale to the capstone.

## Runnable example

```python
from collections import Counter

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
    print(build_report(sample))
```

Run `python3 example.py` from this lesson directory.

## Guided lab

1. Predict the sample report.
2. Run and reconcile it.
3. Load a real export.
4. Render counts and quotations as Markdown.

## Independent practice

1. Group by source title.
2. Add `argparse` paths.
3. Test missing, empty, and malformed selections.

## Hints

- Try `defaultdict(list)`.
- Separate load, validate, aggregate, and render.

## Solution guidance

Build `load_payload`, `validate_records`, `build_report`, and `render_markdown` separately; test pure functions before file I/O.

## 中文学习支持

综合处理 Reader selection JSON。关键词：payload、record、normalize、aggregate、report。先验证，再统计。

学习方法：先用英文说明输入、处理和输出，再用中文复述；最后修改一个条件并预测结果。

## Textbook cross-reference

Supporting reference: Hans-Petter Halvorsen, *Python Programming*, pp. 327–354. Page numbers refer to the linked PDF edition; this lesson and its exercises are original course material.

[Open the supporting PDF](https://www.halvorsen.blog/documents/programming/python/resources/Python%20Programming.pdf)
