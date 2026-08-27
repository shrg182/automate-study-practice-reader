# Module 4: Collections

## Purpose

Choose appropriate collections and build a word-frequency analyzer.

## Learning objectives

- Use lists for ordered mutable items.
- Use tuples for fixed records.
- Use dictionaries for lookup.
- Use sets for uniqueness.

## Core lesson

Read code as data moving through explicit decisions. Before running the example, identify inputs, predict output, and locate validation. Execute it and use differences between prediction and result to refine your mental model.

Keep each program small enough to explain from top to bottom. Names reveal intent, functions expose inputs and outputs, and demonstrations belong under the main guard. These habits scale to the capstone.

## Runnable example

```python
import re

def word_frequencies(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in re.findall(r"[A-Za-z']+", text.lower()):
        counts[word] = counts.get(word, 0) + 1
    return counts

if __name__ == "__main__":
    print(sorted(word_frequencies("Read code, run code, explain code.").items()))
```

Run `python3 example.py` from this lesson directory.

## Guided lab

1. List the extracted words.
2. Explain lowercase normalization.
3. Find the five most frequent words.
4. Report unique vocabulary size.

## Independent practice

1. Exclude common stop words.
2. Group words by first letter.

## Hints

- Test membership in a set.
- Try `setdefault`.

## Solution guidance

Filter before incrementing. For grouping, use `groups.setdefault(word[0], []).append(word)`.

## 中文学习支持

比较 list、tuple、dictionary、set；选择时考虑顺序、修改、查找和去重。

学习方法：先用英文说明输入、处理和输出，再用中文复述；最后修改一个条件并预测结果。

## Textbook cross-reference

Supporting reference: Hans-Petter Halvorsen, *Python Programming*, pp. 87–120. Page numbers refer to the linked PDF edition; this lesson and its exercises are original course material.

[Open the supporting PDF](https://www.halvorsen.blog/documents/programming/python/resources/Python%20Programming.pdf)
