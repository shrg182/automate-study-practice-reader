# Module 10: Numerical Python

## Purpose

Build transparent statistics and recognize when numerical libraries add value.

## Learning objectives

- Use `statistics` for small data.
- Separate calculation and display.
- Recognize vectorization use cases.
- Label units and precision.

## Core lesson

Read code as data moving through explicit decisions. Before running the example, identify inputs, predict output, and locate validation. Execute it and use differences between prediction and result to refine your mental model.

Keep each program small enough to explain from top to bottom. Names reveal intent, functions expose inputs and outputs, and demonstrations belong under the main guard. These habits scale to the capstone.

## Runnable example

```python
from statistics import mean, median, pstdev

def reading_report(minutes: list[float]) -> dict[str, float]:
    if not minutes: raise ValueError("at least one session is required")
    return {"sessions": float(len(minutes)), "mean": mean(minutes),
            "median": median(minutes), "spread": pstdev(minutes)}

if __name__ == "__main__":
    for name, value in reading_report([20, 35, 25, 40]).items():
        print(f"{name}: {value:.2f}")
```

Run `python3 example.py` from this lesson directory.

## Guided lab

1. Compute mean and median by hand.
2. Interpret spread.
3. Add minimum and maximum.
4. Sketch a labeled bar chart.

## Independent practice

1. Compare two weeks.
2. Optionally reproduce with NumPy.

## Hints

- Compare matching report keys.
- Keep NumPy optional.

## Solution guidance

Add `min` and `max`. Keep the core standard-library-only; install NumPy or Matplotlib in `.venv` for extensions.

## 中文学习支持

先用标准库统计，再按需要用 NumPy。关键词：mean、median、standard deviation、array、visualization。

学习方法：先用英文说明输入、处理和输出，再用中文复述；最后修改一个条件并预测结果。

## Textbook cross-reference

Supporting reference: Hans-Petter Halvorsen, *Python Programming*, pp. 287–326. Page numbers refer to the linked PDF edition; this lesson and its exercises are original course material.

[Open the supporting PDF](https://www.halvorsen.blog/documents/programming/python/resources/Python%20Programming.pdf)
