# Module 8: Modules, Environments, and Packages

## Purpose

Organize importable code and make its environment reproducible.

## Learning objectives

- Separate reusable code from entry behavior.
- Understand modules and packages.
- Use per-project environments.
- Record direct dependencies.

## Core lesson

Read code as data moving through explicit decisions. Before running the example, identify inputs, predict output, and locate validation. Execute it and use differences between prediction and result to refine your mental model.

Keep each program small enough to explain from top to bottom. Names reveal intent, functions expose inputs and outputs, and demonstrations belong under the main guard. These habits scale to the capstone.

## Runnable example

```python
import platform
import sys

def runtime_report() -> dict[str, str]:
    return {"python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable}

if __name__ == "__main__":
    for key, value in runtime_report().items(): print(f"{key}: {value}")
```

Run `python3 example.py` from this lesson directory.

## Guided lab

1. Run inside and outside `.venv`.
2. Move the function to another module and import it.
3. Declare only dependencies actually used.
4. Explain `python -m pip`.

## Independent practice

1. Create a package with `__init__.py`.
2. Add `__main__.py`.

## Hints

- Use an absolute package import.
- Run `python -m package`.

## Solution guidance

Keep definitions importable and demonstrations under the main guard. Recreate environments from dependency declarations.

## 中文学习支持

说明 module、package、dependency 和 virtual environment。`python -m pip` 可确保目标解释器一致。

学习方法：先用英文说明输入、处理和输出，再用中文复述；最后修改一个条件并预测结果。

## Textbook cross-reference

Supporting reference: Hans-Petter Halvorsen, *Python Programming*, pp. 225–254. Page numbers refer to the linked PDF edition; this lesson and its exercises are original course material.

[Open the supporting PDF](https://www.halvorsen.blog/documents/programming/python/resources/Python%20Programming.pdf)
