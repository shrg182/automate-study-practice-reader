# Module 6: Files and Reliable Programs

## Purpose

Persist structured data with pathlib and JSON while validating boundaries.

## Learning objectives

- Use `Path` for filesystem paths.
- Specify text encoding.
- Serialize data as JSON.
- Give malformed input useful errors.

## Core lesson

Read code as data moving through explicit decisions. Before running the example, identify inputs, predict output, and locate validation. Execute it and use differences between prediction and result to refine your mental model.

Keep each program small enough to explain from top to bottom. Names reveal intent, functions expose inputs and outputs, and demonstrations belong under the main guard. These habits scale to the capstone.

## Runnable example

```python
import json
from pathlib import Path
from tempfile import TemporaryDirectory

def save(path: Path, record: dict[str, object]) -> None:
    if "title" not in record: raise ValueError("record requires a title")
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        path = Path(folder) / "study.json"
        save(path, {"title": "Python", "complete": False})
        print(json.loads(path.read_text(encoding="utf-8")))
```

Run `python3 example.py` from this lesson directory.

## Guided lab

1. Trace dictionary-to-file-to-dictionary.
2. Inspect the JSON text.
3. Handle broken JSON.
4. Require a Boolean `complete` field.

## Independent practice

1. Save a list of records.
2. Write a temporary file and replace the target.

## Hints

- Validate every list item.
- Review `Path.replace`.

## Solution guidance

Catch `json.JSONDecodeError` only where you can add path context. Validate types; do not silently invent required data.

## 中文学习支持

处理文件和 JSON。关键词：path、encoding、serialization、validation、exception handling。

学习方法：先用英文说明输入、处理和输出，再用中文复述；最后修改一个条件并预测结果。

## Textbook cross-reference

Supporting reference: Hans-Petter Halvorsen, *Python Programming*, pp. 155–190. Page numbers refer to the linked PDF edition; this lesson and its exercises are original course material.

[Open the supporting PDF](https://www.halvorsen.blog/documents/programming/python/resources/Python%20Programming.pdf)
