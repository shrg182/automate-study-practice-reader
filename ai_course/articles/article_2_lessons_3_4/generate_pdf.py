#!/usr/bin/env python3
"""Generate the standalone news-style PDF for AI Course Article 2."""

import csv
import html
import json
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from bs4 import BeautifulSoup, NavigableString, Tag


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "ai_course_article_2_lessons_3_4.pdf"
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
        pdfmetrics.registerFont(TTFont("ArticleArial", str(REGULAR_FONT)))
        pdfmetrics.registerFont(TTFont("ArticleArialBold", str(BOLD_FONT)))
        pdfmetrics.registerFont(TTFont("ArticleArialItalic", str(ITALIC_FONT)))
        return "ArticleArial", "ArticleArialBold", "ArticleArialItalic"
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
        "note_cjk": ParagraphStyle("NoteCJK", parent=base["BodyText"], fontName="STSong-Light", fontSize=8.2, leading=11.5, textColor=MID_BLUE),
        "footnote": ParagraphStyle("Footnote", parent=base["BodyText"], fontName=italic, fontSize=7.5, leading=10, textColor=MUTED, leftIndent=8, rightIndent=8, spaceAfter=5),
        "cell": ParagraphStyle("Cell", parent=base["BodyText"], fontName=regular, fontSize=8.1, leading=10.7, textColor=colors.HexColor("#243B53")),
        "cell_cjk": ParagraphStyle("CellCJK", parent=base["BodyText"], fontName="STSong-Light", fontSize=8.1, leading=10.7, textColor=colors.HexColor("#243B53")),
        "cell_b": ParagraphStyle("CellB", parent=base["BodyText"], fontName=bold, fontSize=8.1, leading=10.7, textColor=colors.white, alignment=TA_CENTER),
    }

    def p(text: str, style: str = "body") -> Paragraph:
        return Paragraph(text, styles[style])

    def cell_p(text: str, *, escaped=False) -> Paragraph:
        style = "cell_cjk" if re.search(r"[\u3400-\u9fff]", text) else "cell"
        return p(text if escaped else html.escape(text), style)

    def note_p(text: str, *, escaped=False) -> Paragraph:
        style = "note_cjk" if re.search(r"[\u3400-\u9fff]", text) else "note"
        return p(text if escaped else html.escape(text), style)

    def report_table(data, widths, *, first_column=False, padding=6, repeat=True) -> Table:
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

    raw = (HERE / "article_2_clean.txt").read_text(encoding="utf-8")
    body, footnotes = raw.split("\n\n脚注\n\n", 1)
    plain_blocks = [block.strip() for block in body.split("\n\n") if block.strip()]
    title = plain_blocks.pop(0)
    footnote_text = re.sub(r"^〔1〕", "", footnotes.strip()).strip()

    highlights = {
        "turns mistakes into directions for improvement": "#FFF1B8",
        "converts the difference between predictions and answers into a number": "#E3F0DC",
        "calculates a small adjustment to many parameters": "#DCEBF0",
        "balance between learning too slowly and overshooting": "#D9C2F0",
        "engineered system of calculations, not a miniature human brain": "#FFF1B8",
        "weights tell the network which inputs deserve more or less influence": "#E3F0DC",
        "transform it into increasingly useful internal patterns": "#DCEBF0",
        "useful behavior emerges from many trained operations working together": "#D9C2F0",
    }

    def rich(text: str) -> str:
        rendered = html.escape(text)
        for phrase, color in highlights.items():
            escaped = html.escape(phrase)
            rendered = rendered.replace(escaped, f'<font backColor="{color}">{escaped}</font>', 1)
        rendered = rendered.replace("〔1〕", '<super><font color="#1F5F99">1</font></super>')
        return rendered

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
        if "interlinear-note" in classes:
            source = "".join(render_node(child) for child in node.children)
            note = html.escape(node.get("data-note", "").strip())
            if note:
                note_font = "STSong-Light" if re.search(r"[\u3400-\u9fff]", note) else italic
                source += (
                    f' <font name="{note_font}" size="7" color="#486581" '
                    f'backColor="#E8F1F4">({note})</font>'
                )
            return source
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

    seed_path = HERE / "article_2_editor_seed.json"
    if seed_path.exists():
        seed = json.loads(seed_path.read_text(encoding="utf-8"))
        soup = BeautifulSoup(seed["bodyHTML"], "html.parser")
        blocks = []
        for paragraph in soup.find_all("p", recursive=False):
            clone = BeautifulSoup(str(paragraph), "html.parser").find("p")
            for rt in clone.select("rt"):
                rt.decompose()
            for gloss in clone.select(".inline-gloss"):
                gloss.decompose()
            plain = clone.get_text("", strip=False).strip()
            blocks.append(
                {
                    "plain": plain,
                    "rich": "".join(render_node(child) for child in paragraph.children),
                    "comment": "comment-block" in (paragraph.get("class") or []),
                }
            )
        if blocks and blocks[0]["plain"] == title:
            blocks.pop(0)
    else:
        blocks = [
            {"plain": block, "rich": rich(block), "comment": False}
            for block in plain_blocks
        ]

    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=letter, leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.62 * inch, bottomMargin=0.62 * inch,
        title=title, author="Codex, OpenAI",
        subject="AI Course Article 2: model training and neural networks",
    )
    story = [
        p("How AI Learns", "title"),
        p("Training and Neural Networks · Lessons 3–4", "dek"),
        p("AI course article 2 | Study edition", "meta"),
        Spacer(1, 8), HRFlowable(width="100%", thickness=1.1, color=LINE), Spacer(1, 10),
    ]
    overview = [
        [p("Lesson 3", "cell_b"), p("How prediction errors, loss, gradient descent, learning rates, and epochs improve a model.", "cell")],
        [p("Lesson 4", "cell_b"), p("How artificial neurons, layers, activation functions, and backpropagation form a neural network.", "cell")],
        [p("Central idea", "cell_b"), p("Useful behavior emerges from repeated numerical transformations and parameter updates—not from a miniature human mind.", "cell")],
    ]
    story += [report_table(overview, [1.1 * inch, 5.3 * inch], first_column=True, repeat=False), Spacer(1, 6)]

    for block in blocks:
        plain = block["plain"]
        rendered = block["rich"]
        if block["comment"]:
            callout = Table(
                [[note_p(rendered, escaped=True)]],
                colWidths=[6.4 * inch],
            )
            callout.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EDF4F6")),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]))
            story += [callout, Spacer(1, 5)]
        elif plain.startswith("Lesson "):
            if plain.startswith("Lesson 4:"):
                story.append(PageBreak())
            story.append(p(rendered, "h1"))
        elif plain.startswith("Quick check:"):
            _, rest = rendered.split(":", 1)
            story += [p("Quick Check", "h2"), p(rest.strip())]
        elif plain.startswith("Обучение "):
            story.append(p(rendered, "russian"))
            for line in footnotes.splitlines():
                match = re.match(r"〔(\d+)〕(.*)", line.strip())
                if match:
                    note_text = re.sub(r"^\s*Editor[’']s note:\s*", "", match.group(2), flags=re.I)
                    story.append(p(f"<super>{match.group(1)}</super> {html.escape(note_text)}", "footnote"))
        else:
            story.append(p(rendered))

    reviews = [row for row in load_rows("review_notes.tsv", "\t") if row.get("status") == "open"]
    if reviews:
        apparatus = [[p("Type", "cell_b"), p("Text", "cell_b"), p("Explanation", "cell_b")]]
        apparatus += [[p("Review", "cell"), cell_p(row["text"]), cell_p(row["issue"])] for row in reviews]
        story += [p("Notes and Pending Review", "h1"), report_table(apparatus, [0.7 * inch, 1.55 * inch, 4.15 * inch], padding=4)]

    reading_notes = []
    for line in (HERE / "article_2_reading_notes.txt").read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            _, note = line.split("\t", 1)
            reading_notes.append([note_p(note)])
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
    story += [Spacer(1, 8), HRFlowable(width="100%", thickness=0.7, color=LINE), Spacer(1, 6), p("This course article was created by Codex, an AI coding agent from OpenAI.", "small")]

    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont(regular, 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(0.7 * inch, 0.34 * inch, "How AI Learns · Lessons 3–4")
        canvas.drawRightString(7.8 * inch, 0.34 * inch, f"Page {document.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
