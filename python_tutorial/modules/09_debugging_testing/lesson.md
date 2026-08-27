# Module 9: Debugging and Testing

## Purpose

Convert specifications into automated tests and treat failures as evidence.

## Learning objectives

- Reproduce defects minimally.
- Read tracebacks from the last line upward.
- Test boundaries.
- Keep tests deterministic.

## Core lesson

Read code as data moving through explicit decisions. Before running the example, identify inputs, predict output, and locate validation. Execute it and use differences between prediction and result to refine your mental model.

Keep each program small enough to explain from top to bottom. Names reveal intent, functions expose inputs and outputs, and demonstrations belong under the main guard. These habits scale to the capstone.

## Runnable example

```python
import unittest

def normalize_score(value: float, maximum: float = 100.0) -> float:
    if maximum <= 0: raise ValueError("maximum must be positive")
    if not 0 <= value <= maximum: raise ValueError("value outside range")
    return value / maximum

class Tests(unittest.TestCase):
    def test_middle(self): self.assertAlmostEqual(normalize_score(75), .75)
    def test_invalid_maximum(self):
        with self.assertRaises(ValueError): normalize_score(1, 0)

if __name__ == "__main__": unittest.main()
```

Run `python3 example.py` from this lesson directory.

## Guided lab

1. State the rules.
2. Run with `-v`.
3. Test zero, maximum, and out-of-range values.
4. Introduce and then repair a defect.

## Independent practice

1. Test a non-100 maximum.
2. Name a regression test after behavior.

## Hints

- Five of twenty is 0.25.
- Test observable behavior.

## Solution guidance

Assert both boundaries and use `assertRaises` for negative and over-maximum values.

## 中文学习支持

把需求变成测试。关键词：debugging、traceback、assertion、boundary test、regression test。

学习方法：先用英文说明输入、处理和输出，再用中文复述；最后修改一个条件并预测结果。

## Textbook cross-reference

Supporting reference: Hans-Petter Halvorsen, *Python Programming*, pp. 255–286. Page numbers refer to the linked PDF edition; this lesson and its exercises are original course material.

[Open the supporting PDF](https://www.halvorsen.blog/documents/programming/python/resources/Python%20Programming.pdf)
