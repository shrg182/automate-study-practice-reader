#!/usr/bin/env python3
"""
generate_markdown_syntax_guide.py

Create a Markdown reference file that demonstrates common Markdown syntax.

Usage:
    python3 generate_markdown_syntax_guide.py

Output:
    markdown_syntax_guide.md
"""

from __future__ import annotations

from pathlib import Path

OUTPUT_FILE: Path = Path("markdown_syntax_guide.md")

MARKDOWN_CONTENT: str = """# Markdown Syntax Guide

This document demonstrates common Markdown syntax and formatting.

---

## 1. Headings

```md
\\# H1 Heading
\\## H2 Heading
\\### H3 Heading
\\#### H4 Heading

\\---

## 2. Emphasis
```md
\\*Italic text\\*
\\**Bold text\\**
\\***Bold and italic text\\***
\\~~Strikethrough text\\~~
---
## 3. Lists
```md
\\- Unordered list item 1
\\- Unordered list item 2
\\- Unordered list item 3   
\\1. Ordered list item 1
\\2. Ordered list item 2
\\3. Ordered list item 3
---
## 4. Links and Images
```md
\\[Link text\\](https://example.com)
\\![Alt text\\](https://example.com/image.jpg)
---
## 5. Code
```md
\\`Inline code\\`
\\```
\\```
\\Code block content
\\```
\\```
---
## 6. Blockquotes
```md
\\> This is a blockquote.
\\> It can span multiple lines.
---
## 7. Horizontal Rule
```md
\\---
---
## 8. Tables
```md
\\| Header 1 \\| Header 2 \\|
\\| --- \\| --- \\|
\\| Row 1 Col 1 \\| Row 1 Col 2 \\|
\\| Row 2 Col 1 \\| Row 2 Col 2 \\|
"""

def main() -> None:
    """Generate the Markdown syntax guide file."""
    OUTPUT_FILE.write_text(MARKDOWN_CONTENT, encoding="utf-8")
    print(f"Markdown syntax guide generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()