# Markdown Syntax Guide

This document demonstrates common Markdown syntax and formatting.

---

## 1. Headings

```md
\# H1 Heading
\## H2 Heading
\### H3 Heading
\#### H4 Heading

\---
```

## 2. Text Formatting

- *Italic text*
- **Bold text**
- ***Bold and italic***
- ~~Strikethrough~~

---

## 3. Lists

### Unordered List
- Item 1
- Item 2
  - Sub-item 2.1
  - Sub-item 2.2

### Ordered List
1. First item
2. Second item
3. Third item

---

## 4. Links

[OpenAI](https://openai.com)

---

## 5. Images

![Sample Image](https://via.placeholder.com/150)

---

## 6. Code

### Inline Code
Use `print()` in Python.

### Code Block

```python
def hello() -> None:
    """Print a greeting."""
    print("Hello, world!")


if __name__ == "__main__":
    hello()
```

## 7. Blockquotes

> This is a blockquote.
> It can span multiple lines.

## 📊 8. Tables

| Name | Age |
|------|-----|
| Alice | 25 |
| Bob   | 30 |


## 🔲 9. Checkboxes (Great for To-Do Lists)
- [x] Task done
- [ ] Task pending

## 🔥 10. Horizontal Line
---


## 11. Combined Example (Project Style) 

````md
📁 11. Markdown in Your Project (Very Useful for You)

# Chapter 11 - Organizing Files

## Scripts
- move_files.py → Move selected files
- rename_files.py → Batch rename

## Usage
...
```bash
python move_files.py --source ./downloads --target ./docs
```
...

---

# ⚡ Pro Tips (Especially for Your Workflow)
````

## 12. Nested Elements Example
- Main Task
  - Subtask with `inline code`
  - Subtask with a link: [Python](https://python.org)


## 13. Escaping Characters

To display special characters:

\* Not italic
\# Not a heading

## 14. End of Document

This file serves as a quick reference for Markdown syntax.


---

If you want to integrate this into your automation workflow, I can next:

- turn this into a **template generator script (Python)**
- or auto-populate it across your project folders (like your `populate_readme_usage.py` tool)

Which direction do you want to go?