#!/usr/bin/env python3
"""Build the Practical Python Foundations proposal reader and course landing page."""

from __future__ import annotations

from html import escape
from pathlib import Path
import re
import sys


BASE_DIR = Path(__file__).resolve().parent
PROJECT = BASE_DIR / "course_proposal"
SHARED_DIR = BASE_DIR.parent / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))
from build_editor import build_html  # noqa: E402


def inline_markup(value: str) -> str:
    text = escape(value)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(
        r"\[([^]]+)]\((https?://[^)]+)\)",
        lambda match: f'<a href="{match.group(2)}" target="_blank" rel="noreferrer">{match.group(1)}</a>',
        text,
    )
    return text


def markdown_to_html(markdown: str) -> str:
    output: list[str] = []
    paragraph: list[str] = []
    list_type = ""
    in_code = False
    code_lines: list[str] = []

    def close_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline_markup(' '.join(paragraph))}</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            output.append(f"</{list_type}>")
            list_type = ""

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if line.startswith("```"):
            close_paragraph()
            close_list()
            if in_code:
                output.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
                code_lines.clear()
            in_code = not in_code
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not line.strip():
            close_paragraph()
            close_list()
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            close_paragraph()
            close_list()
            level = min(4, len(heading.group(1)) + 1)
            output.append(f"<h{level}>{inline_markup(heading.group(2))}</h{level}>")
            continue
        bullet = re.match(r"^-\s+(.+)$", line)
        numbered = re.match(r"^\d+\.\s+(.+)$", line)
        if bullet or numbered:
            close_paragraph()
            kind = "ul" if bullet else "ol"
            if list_type != kind:
                close_list()
                output.append(f"<{kind}>")
                list_type = kind
            output.append(f"<li>{inline_markup((bullet or numbered).group(1))}</li>")
            continue
        close_list()
        paragraph.append(line.strip())
    close_paragraph()
    close_list()
    if code_lines:
        output.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
    return "\n".join(output)


def build_editor(markdown: str) -> str:
    plain_text = re.sub(r"[`#*_\[\]()]", "", markdown)
    output = build_html(
        plain_text,
        [],
        "../COURSE_PROPOSAL.md",
        chapter_title="Practical Python Foundations — Course Proposal",
        editor_title="Practical Python Foundations — Course Proposal · Reader",
        storage_key="python-tutorial-course-proposal-v1",
        file_stem="python_tutorial_course_proposal",
        inline_notes=[],
        review_notes=[],
        reading_notes=[],
        global_terms=[],
        home_href="../../index.html",
        theme_href="../../workspace_theme.css",
        shared_library_href="../index.html",
        shared_library_label="Python Course Plan",
        source_site_label="Source Markdown",
    )
    article = markdown_to_html(markdown)
    output, count = re.subn(
        r'(<section id="editor" class="editor"[^>]*>)[\s\S]*?(</section>)',
        rf"\1{article}\2",
        output,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Could not locate the generated editor body")
    course_css = """
<style>
#editor{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.75}
#editor h2{margin:2.1em 0 .65em;padding-bottom:.3em;border-bottom:1px solid var(--line);font-size:1.65em}
#editor h3{margin:1.7em 0 .55em;color:var(--blue);font-size:1.3em}
#editor h4{margin:1.4em 0 .45em;font-size:1.08em}
#editor p{margin:.75em 0;text-indent:0}
#editor li{margin:.36em 0}
#editor code{padding:.12em .35em;border-radius:4px;background:#eef1f4;font-family:"SFMono-Regular",Consolas,monospace;font-size:.9em}
#editor pre{padding:16px;border:1px solid #d4dbe2;border-radius:8px;background:#f6f8fa;overflow:auto;white-space:pre}
#editor pre code{padding:0;background:transparent}
#editor a{color:#174ea6;text-underline-offset:.16em}
</style>
"""
    return output.replace("</head>", course_css + "</head>", 1)


def build_landing() -> str:
    modules = [
        "Getting Ready", "Values, Variables, and Expressions", "Decisions and Repetition",
        "Collections", "Functions and Program Design", "Files and Reliable Programs",
        "Classes and Data Models", "Modules, Environments, and Packages",
        "Debugging and Testing", "Numerical Python", "Capstone Project",
    ]
    module_html = "".join(
        f'<li><span>{number:02d}</span><div><strong>{escape(title)}</strong><small>Planned module · lessons forthcoming</small></div></li>'
        for number, title in enumerate(modules, 1)
    )
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Practical Python Foundations · Course Plan</title><link rel="stylesheet" href="../workspace_theme.css"><script src="../workspace_skin.js"></script>
<style>
:root{{--ink:#202124;--muted:#5f6368;--line:#dadce0;--blue:#174ea6;--green:#137333}}*{{box-sizing:border-box}}body{{margin:0;background:#f1f3f4;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}main{{width:min(980px,calc(100% - 28px));margin:32px auto 80px}}header{{padding:34px;border-radius:14px;background:linear-gradient(135deg,#143a56,#176b63);color:#fff}}header p{{max-width:700px;line-height:1.65;color:#dbe9e7}}h1{{margin:0;font-size:clamp(30px,5vw,54px)}}.actions{{display:flex;gap:9px;flex-wrap:wrap;margin-top:20px}}.actions a{{padding:10px 13px;border-radius:20px;background:#fff;color:#174ea6;text-decoration:none;font-weight:700}}section{{margin-top:20px;padding:24px;border:1px solid var(--line);border-radius:12px;background:#fff}}h2{{margin-top:0}}.status{{display:inline-block;padding:5px 9px;border-radius:15px;background:#e6f4ea;color:var(--green);font-size:12px;font-weight:700}}ol{{display:grid;gap:8px;padding:0;list-style:none}}li{{display:flex;gap:12px;padding:12px;border:1px solid #e5e8eb;border-radius:8px}}li>span{{display:grid;width:34px;height:34px;place-items:center;border-radius:50%;background:#e8f0fe;color:var(--blue);font-weight:700}}li div{{display:grid;gap:3px}}li small{{color:var(--muted)}}@media(max-width:600px){{header,section{{padding:20px}}}}
</style></head><body><main><header><span class="status">Planning entry published</span><h1>Practical Python Foundations</h1><p>An original, Reader-native Python course planned around modern Python practices, bilingual study support, runnable examples, guided labs, and a Reader Selection Report capstone.</p><div class="actions"><a href="course_proposal/editor.html?view=annotated">Read and annotate the proposal</a><a href="COURSE_PROPOSAL.md">Open source Markdown</a><a href="https://www.halvorsen.blog/documents/programming/python/resources/Python%20Programming.pdf" target="_blank" rel="noreferrer">Reference PDF</a></div></header><section><h2>Course status</h2><p>The proposal is available in the Reader. The instructional modules listed below are planned and have not yet been presented as completed lessons.</p></section><section><h2>Planned modules</h2><ol>{module_html}</ol></section></main></body></html>'''


def main() -> None:
    markdown = (BASE_DIR / "COURSE_PROPOSAL.md").read_text(encoding="utf-8")
    PROJECT.mkdir(parents=True, exist_ok=True)
    (PROJECT / "editor.html").write_text(build_editor(markdown), encoding="utf-8")
    (BASE_DIR / "index.html").write_text(build_landing(), encoding="utf-8")
    print("Built Practical Python Foundations course proposal reader")


if __name__ == "__main__":
    main()
