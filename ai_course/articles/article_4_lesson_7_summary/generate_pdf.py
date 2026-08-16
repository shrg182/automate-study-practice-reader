#!/usr/bin/env python3
"""Generate the final AI-course article as a news-style study PDF."""

import csv
import html
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "ai_course_article_4_lesson_7_summary.pdf"
REGULAR_FONT = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
BOLD_FONT = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
ITALIC_FONT = Path("/System/Library/Fonts/Supplemental/Arial Italic.ttf")
NAVY = colors.HexColor("#102A43")
BLUE = colors.HexColor("#1F5F99")
MID_BLUE = colors.HexColor("#486581")
MUTED = colors.HexColor("#627D98")
INK = colors.HexColor("#1F2933")
LINE = colors.HexColor("#BCCCDC")
PALE_BLUE = colors.HexColor("#F0F4F8")


def fonts() -> tuple[str, str, str]:
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    if REGULAR_FONT.exists() and BOLD_FONT.exists() and ITALIC_FONT.exists():
        pdfmetrics.registerFont(TTFont("Article4Arial", str(REGULAR_FONT)))
        pdfmetrics.registerFont(TTFont("Article4ArialBold", str(BOLD_FONT)))
        pdfmetrics.registerFont(TTFont("Article4ArialItalic", str(ITALIC_FONT)))
        pdfmetrics.registerFontFamily(
            "Article4Arial",
            normal="Article4Arial",
            bold="Article4ArialBold",
            italic="Article4ArialItalic",
            boldItalic="Article4ArialBold",
        )
        return "Article4Arial", "Article4ArialBold", "Article4ArialItalic"
    return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"


def load_rows(name: str, delimiter: str = ",") -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))


def build() -> None:
    regular, bold, italic = fonts()
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle("Title", parent=base["Title"], fontName=bold, fontSize=24, leading=29, textColor=NAVY, alignment=TA_CENTER, spaceAfter=8),
        "dek": ParagraphStyle("Dek", parent=base["BodyText"], fontName=regular, fontSize=10.5, leading=15, textColor=MID_BLUE, alignment=TA_CENTER, spaceAfter=10),
        "meta": ParagraphStyle("Meta", parent=base["BodyText"], fontName=regular, fontSize=8.5, leading=11, textColor=MUTED, alignment=TA_CENTER),
        "h1": ParagraphStyle("H1", parent=base["Heading2"], fontName=bold, fontSize=14, leading=18, textColor=colors.HexColor("#12355B"), spaceBefore=12, spaceAfter=7),
        "h2": ParagraphStyle("H2", parent=base["Heading3"], fontName=bold, fontSize=11, leading=14, textColor=BLUE, spaceBefore=8, spaceAfter=4),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName=regular, fontSize=9.5, leading=14, textColor=INK, spaceAfter=7),
        "russian": ParagraphStyle("Russian", parent=base["BodyText"], fontName=regular, fontSize=10, leading=15, textColor=INK, spaceAfter=7),
        "small": ParagraphStyle("Small", parent=base["BodyText"], fontName=regular, fontSize=7.8, leading=10.5, textColor=colors.HexColor("#334E68")),
        "note": ParagraphStyle("Note", parent=base["BodyText"], fontName=italic, fontSize=8.2, leading=11.5, textColor=MID_BLUE),
        "footnote": ParagraphStyle("Footnote", parent=base["BodyText"], fontName=italic, fontSize=7.5, leading=10, textColor=MUTED, leftIndent=8, rightIndent=8, spaceAfter=5),
        "footnote_cjk": ParagraphStyle("FootnoteCJK", parent=base["BodyText"], fontName="STSong-Light", fontSize=7.5, leading=10, textColor=MUTED, leftIndent=8, rightIndent=8, spaceAfter=5),
        "cell": ParagraphStyle("Cell", parent=base["BodyText"], fontName=regular, fontSize=8.1, leading=10.7, textColor=colors.HexColor("#243B53")),
        "cell_cjk": ParagraphStyle("CellCJK", parent=base["BodyText"], fontName="STSong-Light", fontSize=8.1, leading=10.7, textColor=colors.HexColor("#243B53")),
        "cell_b": ParagraphStyle("CellB", parent=base["BodyText"], fontName=bold, fontSize=8.1, leading=10.7, textColor=colors.white, alignment=TA_CENTER),
    }

    def p(text: str, style: str = "body") -> Paragraph:
        return Paragraph(text, styles[style])

    def cell_p(text: str, *, escaped=False) -> Paragraph:
        style = "cell_cjk" if re.search(r"[\u3400-\u9fff]", text) else "cell"
        return p(text if escaped else html.escape(text), style)

    def footnote_p(number: str, text: str) -> Paragraph:
        style = "footnote_cjk" if re.search(r"[\u3400-\u9fff]", text) else "footnote"
        return p(f"<super>{number}</super> {html.escape(text)}", style)

    def report_table(data, widths, *, first_column=False, padding=5, repeat=True) -> Table:
        item = Table(data, colWidths=widths, repeatRows=1 if repeat else 0)
        commands = [
            ("BOX", (0, 0), (-1, -1), 0.6, LINE),
            ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D9E2EC")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), padding),
        ]
        if first_column:
            commands += [("BACKGROUND", (0, 0), (0, -1), BLUE), ("BACKGROUND", (1, 0), (-1, -1), PALE_BLUE)]
        else:
            commands += [("BACKGROUND", (0, 0), (-1, 0), BLUE), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE_BLUE])]
        item.setStyle(TableStyle(commands))
        return item

    raw = (HERE / "article_4_clean.txt").read_text(encoding="utf-8")
    body, footnotes = raw.split("\n\n脚注\n\n", 1)
    plain_blocks = [block.strip() for block in body.split("\n\n") if block.strip()]
    title = plain_blocks.pop(0)
    highlights = {
        "model can learn an incomplete pattern": "#FFF1A8",
        "Fairness therefore requires examining outcomes": "#B7E7A7",
        "The higher the possible harm, the stronger the verification should be": "#B8DDF8",
        "Confidence in the wording is not evidence of correctness": "#DDB5EB",
    }

    def default_rich(text: str) -> str:
        rendered = html.escape(text)
        for phrase, color in highlights.items():
            escaped = html.escape(phrase)
            rendered = rendered.replace(escaped, f'<font backColor="{color}">{escaped}</font>', 1)
        return rendered.replace("〔1〕", '<super><font color="#1F5F99">1</font></super>')

    def css_color(style: str) -> str | None:
        match = re.search(r"background-color\s*:\s*([^;]+)", style, re.I)
        if not match:
            return None
        value = match.group(1).strip()
        rgb = re.fullmatch(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", value)
        if rgb:
            return "#" + "".join(f"{int(part):02x}" for part in rgb.groups())
        return value if re.fullmatch(r"#[0-9a-fA-F]{6}", value) else None

    def render_node(node) -> str:
        if isinstance(node, NavigableString):
            return html.escape(str(node))
        if not isinstance(node, Tag) or node.name in {"rt", "script", "style"}:
            return ""
        classes = set(node.get("class") or [])
        if "inline-gloss" in classes:
            return ""
        if "footnote-ref" in classes:
            number = re.sub(r"\D", "", node.get_text("", strip=True)) or "*"
            return f'<super><font color="#1F5F99">{number}</font></super>'
        content = "".join(render_node(child) for child in node.children)
        style = node.get("style", "")
        background = css_color(style)
        if background:
            content = f'<font backColor="{background}">{content}</font>'
        if node.name in {"b", "strong"} or re.search(r"font-weight\s*:\s*(bold|[6-9]00)", style, re.I):
            content = f"<b>{content}</b>"
        if node.name == "u" or "underline" in style:
            content = f"<u>{content}</u>"
        if node.name in {"s", "strike"} or "line-through" in style:
            content = f"<strike>{content}</strike>"
        return content

    seed_path = HERE / "article_4_editor_seed.json"
    if seed_path.exists():
        seed = json.loads(seed_path.read_text(encoding="utf-8"))
        soup = BeautifulSoup(seed["bodyHTML"], "html.parser")
        blocks = []
        for paragraph in soup.find_all("p", recursive=False):
            clone = BeautifulSoup(str(paragraph), "html.parser").find("p")
            for item in clone.select("rt,.inline-gloss"):
                item.decompose()
            blocks.append({
                "plain": clone.get_text("", strip=False).strip(),
                "rich": "".join(render_node(child) for child in paragraph.children),
                "comment": "comment-block" in (paragraph.get("class") or []),
            })
        if blocks and blocks[0]["plain"] == title:
            blocks.pop(0)
    else:
        blocks = [{"plain": block, "rich": default_rich(block), "comment": False} for block in plain_blocks]

    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=letter, leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.62 * inch, bottomMargin=0.62 * inch,
        title=title, author="Codex, OpenAI",
        subject="AI Course Article 4: responsible use and course summary",
    )
    story = [
        p("Using AI Responsibly", "title"),
        p("Bias, Privacy, Reliability, and the Complete Course · Lesson 7", "dek"),
        p("AI course article 4 | Final study edition", "meta"),
        Spacer(1, 8), HRFlowable(width="100%", thickness=1.1, color=LINE), Spacer(1, 10),
    ]
    overview = [
        [p("Evaluate", "cell_b"), p("Examine bias, privacy, reliability, security, and task-specific evidence.", "cell")],
        [p("Verify", "cell_b"), p("Increase independent checking as uncertainty and potential harm increase.", "cell")],
        [p("Remain accountable", "cell_b"), p("Keep human responsibility explicit before, during, and after deployment.", "cell")],
    ]
    story += [report_table(overview, [1.25 * inch, 5.15 * inch], first_column=True, repeat=False), Spacer(1, 6)]

    for block in blocks:
        plain, rendered = block["plain"], block["rich"]
        if block["comment"]:
            callout = Table([[p(rendered, "note")]], colWidths=[6.4 * inch])
            callout.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EDF4F6")),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]))
            story += [callout, Spacer(1, 5)]
        elif plain.startswith("Lesson 7:"):
            story.append(p(rendered, "h1"))
        elif plain.startswith("Course Summary:"):
            story.append(p(rendered, "h1"))
        elif plain.startswith("Quick check:"):
            _, rest = rendered.split(":", 1)
            story += [p("Quick Check", "h2"), p(rest.strip())]
        elif plain.startswith("Ответственное "):
            story.append(p(rendered, "russian"))
            for line in footnotes.splitlines():
                match = re.match(r"〔(\d+)〕(.*)", line.strip())
                if match:
                    note_text = re.sub(r"^\s*Editor[’']s note:\s*", "", match.group(2), flags=re.I)
                    story.append(footnote_p(match.group(1), note_text))
        else:
            story.append(p(rendered))

    inline = load_rows("inline_notes.tsv", "\t")
    reviews = [row for row in load_rows("review_notes.tsv", "\t") if row.get("status") == "open"]
    apparatus = [[p("Type", "cell_b"), p("Text", "cell_b"), p("Explanation", "cell_b")]]
    apparatus += [[p("Inline", "cell"), cell_p(row["text"]), cell_p(row["note"])] for row in inline]
    apparatus += [[p("Review", "cell"), cell_p(row["text"]), cell_p(row["issue"])] for row in reviews]
    story += [p("Notes and Pending Review", "h1"), report_table(apparatus, [0.7 * inch, 1.55 * inch, 4.15 * inch], padding=4)]

    reading_notes = []
    for line in (HERE / "article_4_reading_notes.txt").read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            _, note = line.split("\t", 1)
            reading_notes.append([p(html.escape(note), "note")])
    if reading_notes:
        notes_table = Table(reading_notes, colWidths=[6.4 * inch])
        notes_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
            ("BOX", (0, 0), (-1, -1), 0.5, LINE),
            ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story += [Spacer(1, 8), notes_table]

    terms = load_rows("reading_terms.csv")
    vocab = [[p("Term", "cell_b"), p("Meaning in this article", "cell_b")]]
    vocab += [[cell_p(row["term"]), cell_p(row["annotation"])] for row in terms]
    story += [KeepTogether([p("Article Vocabulary", "h1"), report_table(vocab, [1.55 * inch, 4.85 * inch], padding=4)])]
    story += [Spacer(1, 8), HRFlowable(width="100%", thickness=0.7, color=LINE), Spacer(1, 6), p("This course was created by Codex, an AI coding agent from OpenAI.", "small")]

    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont(regular, 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(0.7 * inch, 0.34 * inch, "Using AI Responsibly · Lesson 7 and Summary")
        canvas.drawRightString(7.8 * inch, 0.34 * inch, f"Page {document.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
