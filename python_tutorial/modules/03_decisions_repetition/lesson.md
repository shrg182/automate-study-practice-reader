# Module 3: Decisions and Repetition

## Purpose

Use conditions and loops to create an actionable score summary.

## Learning objectives

- Branch with `if`, `elif`, and `else`.
- Repeat with `for`.
- Combine Boolean expressions.
- Accumulate results explicitly.

## Core lesson

Read code as data moving through explicit decisions. Before running the example, identify inputs, predict output, and locate validation. Execute it and use differences between prediction and result to refine your mental model.

Keep each program small enough to explain from top to bottom. Names reveal intent, functions expose inputs and outputs, and demonstrations belong under the main guard. These habits scale to the capstone.

## Runnable example

```python
def classify_scores(scores: list[int]) -> dict[str, int]:
    result = {"mastered": 0, "review": 0, "retry": 0}
    for score in scores:
        if score >= 85: result["mastered"] += 1
        elif score >= 60: result["review"] += 1
        else: result["retry"] += 1
    return result

if __name__ == "__main__":
    print(classify_scores([92, 74, 58, 85, 61]))
```

Run `python3 example.py` from this lesson directory.

## Guided lab

1. Trace the dictionary after each score.
2. Run and check the trace.
3. Reject scores outside 0–100.
4. Report the largest category.

## Independent practice

1. Use named threshold constants.
2. Write a three-step `while` countdown.

## Hints

- Constants use uppercase names.
- Decrease the counter each pass.

## Solution guidance

Define `MASTERY_SCORE` and `REVIEW_SCORE`. Raise `ValueError` before classifying an invalid score.

## 中文学习支持

用条件分支做选择，用循环处理数据。关键词：condition、branch、iteration、accumulator、boundary。

学习方法：先用英文说明输入、处理和输出，再用中文复述；最后修改一个条件并预测结果。

## Textbook cross-reference

Supporting reference: Hans-Petter Halvorsen, *Python Programming*, pp. 53–86. Page numbers refer to the linked PDF edition; this lesson and its exercises are original course material.

[Open the supporting PDF](https://www.halvorsen.blog/documents/programming/python/resources/Python%20Programming.pdf)
