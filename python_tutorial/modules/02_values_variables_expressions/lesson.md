# Module 2: Values, Variables, and Expressions

## Purpose

Represent data clearly and combine values safely in a receipt program.

## Learning objectives

- Distinguish basic scalar types.
- Choose meaningful variable names.
- Use arithmetic and conversion deliberately.
- Format results with f-strings.

## Core lesson

Read code as data moving through explicit decisions. Before running the example, identify inputs, predict output, and locate validation. Execute it and use differences between prediction and result to refine your mental model.

Keep each program small enough to explain from top to bottom. Names reveal intent, functions expose inputs and outputs, and demonstrations belong under the main guard. These habits scale to the capstone.

## Runnable example

```python
def make_receipt(price: float, quantity: int, tax_rate: float = 0.06) -> str:
    subtotal = price * quantity
    tax = subtotal * tax_rate
    total = subtotal + tax
    return f"Subtotal: ${subtotal:.2f} | Tax: ${tax:.2f} | Total: ${total:.2f}"

if __name__ == "__main__":
    print(make_receipt(12.50, 3))
```

Run `python3 example.py` from this lesson directory.

## Guided lab

1. Predict every intermediate value.
2. Run and compare the result.
3. Add a discount before tax.
4. Reject a negative quantity.

## Independent practice

1. Return numeric results in a dictionary.
2. Convert a price supplied as text.

## Hints

- Build a dictionary literal.
- Catch `ValueError` from `float`.

## Solution guidance

Validate inputs near the top. Compute `discounted = max(0, subtotal - discount)` and calculate tax from that value.

## 中文学习支持

学习值、变量、表达式和类型转换。关键词：value、variable、expression、conversion、formatted output。

学习方法：先用英文说明输入、处理和输出，再用中文复述；最后修改一个条件并预测结果。

## Textbook cross-reference

Supporting reference: Hans-Petter Halvorsen, *Python Programming*, pp. 21–52. Page numbers refer to the linked PDF edition; this lesson and its exercises are original course material.

[Open the supporting PDF](https://www.halvorsen.blog/documents/programming/python/resources/Python%20Programming.pdf)
