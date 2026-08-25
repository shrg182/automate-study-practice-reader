# Module 7: Classes and Data Models

## Purpose

Model a study item with a dataclass and methods that protect its state.

## Learning objectives

- Combine related data and behavior.
- Reduce boilerplate with `@dataclass`.
- Express valid state explicitly.
- Prefer composition to deep inheritance.

## Core lesson

Read code as data moving through explicit decisions. Before running the example, identify inputs, predict output, and locate validation. Execute it and use differences between prediction and result to refine your mental model.

Keep each program small enough to explain from top to bottom. Names reveal intent, functions expose inputs and outputs, and demonstrations belong under the main guard. These habits scale to the capstone.

## Runnable example

```python
from dataclasses import dataclass

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
    print(item.label()); item.mark_reviewed(); print(item.label())
```

Run `python3 example.py` from this lesson directory.

## Guided lab

1. Identify state and behavior.
2. Create three items.
3. Reject non-positive minutes in `__post_init__`.
4. Calculate total minutes outside the item.

## Independent practice

1. Add optional notes.
2. Compose a `StudyPlan` from items.

## Hints

- Use `str | None`.
- Store `list[StudyItem]`.

## Solution guidance

Raise in `__post_init__` when `minutes <= 0`. Put plan-wide calculations in a separate `StudyPlan`.

## 中文学习支持

用数据类组合数据和行为。关键词：class、instance、field、method、dataclass、composition。

学习方法：先用英文说明输入、处理和输出，再用中文复述；最后修改一个条件并预测结果。

## Textbook cross-reference

Supporting reference: Hans-Petter Halvorsen, *Python Programming*, pp. 191–224. Page numbers refer to the linked PDF edition; this lesson and its exercises are original course material.

[Open the supporting PDF](https://www.halvorsen.blog/documents/programming/python/resources/Python%20Programming.pdf)
