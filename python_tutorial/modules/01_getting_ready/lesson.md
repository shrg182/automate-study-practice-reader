# Module 1: Getting Ready

## Purpose

Establish the edit-run-observe cycle and identify the active interpreter.

## Learning objectives

- Run a script from a terminal.
- Inspect the Python version and executable.
- Use a project virtual environment.
- Recognize a module entry point.

## Core lesson

Read code as data moving through explicit decisions. Before running the example, identify inputs, predict output, and locate validation. Execute it and use differences between prediction and result to refine your mental model.

Keep each program small enough to explain from top to bottom. Names reveal intent, functions expose inputs and outputs, and demonstrations belong under the main guard. These habits scale to the capstone.

## Runnable example

```python
import platform
import sys

def environment_summary() -> str:
    return f"Python {platform.python_version()} at {sys.executable}"

if __name__ == "__main__":
    print("Hello, Python learner!")
    print(environment_summary())
```

Run `python3 example.py` from this lesson directory.

## Guided lab

1. Predict the two output lines.
2. Run `python3 example.py`.
3. Create and activate `.venv`, then run it again.
4. Explain why the executable path changed.

## Independent practice

1. Add the operating-system name.
2. Warn when Python is older than 3.10.

## Hints

- Try `platform.system()`.
- Compare `sys.version_info` with `(3, 10)`.

## Solution guidance

Put the warning behind `if sys.version_info < (3, 10):`. Check `sys.executable`, not only the version number.

## 中文学习支持

建立‘编辑—运行—观察’循环。关键词：解释器 interpreter、脚本 script、虚拟环境 virtual environment、入口 entry point。

学习方法：先用英文说明输入、处理和输出，再用中文复述；最后修改一个条件并预测结果。

## Textbook cross-reference

Supporting reference: Hans-Petter Halvorsen, *Python Programming*, pp. 1–20. Page numbers refer to the linked PDF edition; this lesson and its exercises are original course material.

[Open the supporting PDF](https://www.halvorsen.blog/documents/programming/python/resources/Python%20Programming.pdf)
