# Module 5: Functions and Program Design

## Purpose

Decompose a problem into focused functions with explicit contracts.

## Learning objectives

- Give functions one responsibility.
- Prefer parameters and returns to globals.
- Document contracts with hints and docstrings.
- Raise useful exceptions.

## Core lesson

Read code as data moving through explicit decisions. Before running the example, identify inputs, predict output, and locate validation. Execute it and use differences between prediction and result to refine your mental model.

Keep each program small enough to explain from top to bottom. Names reveal intent, functions expose inputs and outputs, and demonstrations belong under the main guard. These habits scale to the capstone.

## Runnable example

```python
def summarize(values: list[float]) -> dict[str, float]:
    """Return statistics for a non-empty list."""
    if not values: raise ValueError("values must not be empty")
    return {"minimum": min(values), "maximum": max(values),
            "average": sum(values) / len(values)}

if __name__ == "__main__":
    print(summarize([4.0, 7.5, 8.5]))
```

Run `python3 example.py` from this lesson directory.

## Guided lab

1. Write the contract in one sentence.
2. Test an ordinary case by hand.
3. Test the empty-list error.
4. Separate formatting from calculation.

## Independent practice

1. Add median.
2. Extract reusable validation.

## Hints

- Use `statistics.median`.
- Validate before calculation.

## Solution guidance

Add median to the returned dictionary. Keep printing outside `summarize` so the function stays reusable and testable.

## 中文学习支持

强调函数契约：输入、输出和错误。关键词：parameter、return value、scope、contract、exception。

学习方法：先用英文说明输入、处理和输出，再用中文复述；最后修改一个条件并预测结果。

## Textbook cross-reference

Supporting reference: Hans-Petter Halvorsen, *Python Programming*, pp. 121–154. Page numbers refer to the linked PDF edition; this lesson and its exercises are original course material.

[Open the supporting PDF](https://www.halvorsen.blog/documents/programming/python/resources/Python%20Programming.pdf)
