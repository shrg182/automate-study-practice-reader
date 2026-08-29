#!/usr/bin/env python3
"""Generate Article 6 in the established AI-course study-edition format."""

import csv
import html
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
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "ai_course_article_6_chatgpt_codex.pdf"
REGULAR = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
ITALIC = Path("/System/Library/Fonts/Supplemental/Arial Italic.ttf")
NAVY, BLUE, MID_BLUE = colors.HexColor("#102A43"), colors.HexColor("#1F5F99"), colors.HexColor("#486581")
MUTED, INK, LINE, PALE = colors.HexColor("#627D98"), colors.HexColor("#1F2933"), colors.HexColor("#BCCCDC"), colors.HexColor("#F0F4F8")


def load_rows(name: str, delimiter: str = ",") -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))


def build() -> None:
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    regular, bold, italic = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"
    if REGULAR.exists() and BOLD.exists() and ITALIC.exists():
        regular, bold, italic = "Article6Arial", "Article6ArialBold", "Article6ArialItalic"
        pdfmetrics.registerFont(TTFont(regular, str(REGULAR)))
        pdfmetrics.registerFont(TTFont(bold, str(BOLD)))
        pdfmetrics.registerFont(TTFont(italic, str(ITALIC)))
        pdfmetrics.registerFontFamily(regular, normal=regular, bold=bold, italic=italic, boldItalic=bold)

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
        "footnote": ParagraphStyle("Footnote", parent=base["BodyText"], fontName=italic, fontSize=7.5, leading=10, textColor=MUTED, leftIndent=8, rightIndent=8, spaceAfter=5),
        "cell": ParagraphStyle("Cell", parent=base["BodyText"], fontName=regular, fontSize=8.1, leading=10.7, textColor=colors.HexColor("#243B53")),
        "cell_b": ParagraphStyle("CellB", parent=base["BodyText"], fontName=bold, fontSize=8.1, leading=10.7, textColor=colors.white, alignment=TA_CENTER),
    }
    p = lambda text, style="body": Paragraph(text, styles[style])

    def report_table(data, widths, *, first_column=False, padding=5, repeat=True):
        table = Table(data, colWidths=widths, repeatRows=1 if repeat else 0)
        commands = [("BOX", (0, 0), (-1, -1), .6, LINE), ("INNERGRID", (0, 0), (-1, -1), .35, colors.HexColor("#D9E2EC")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("PADDING", (0, 0), (-1, -1), padding)]
        commands += [("BACKGROUND", (0, 0), (0, -1), BLUE), ("BACKGROUND", (1, 0), (-1, -1), PALE)] if first_column else [("BACKGROUND", (0, 0), (-1, 0), BLUE), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE])]
        table.setStyle(TableStyle(commands))
        return table

    raw = (HERE / "article_6_clean.txt").read_text(encoding="utf-8")
    body, footnotes = raw.split("\n\n脚注\n\n", 1)
    blocks = [block.strip() for block in body.split("\n\n") if block.strip()]
    title, subtitle = blocks.pop(0), blocks.pop(0)

    doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter, leftMargin=.7*inch, rightMargin=.7*inch, topMargin=.62*inch, bottomMargin=.62*inch, title=title, author="Codex, OpenAI", subject="AI Course Article 6: ChatGPT and Codex in practice")
    story = [p("From Conversation to Completed Work", "title"), p("Using ChatGPT and Codex · Follow-up Course", "dek"), p("AI course article 6 | Practical study edition", "meta"), Spacer(1, 8), HRFlowable(width="100%", thickness=1.1, color=LINE), Spacer(1, 10)]
    overview = [
        [p("Choose", "cell_b"), p("Match conversation-centered work to ChatGPT and artifact-centered work to Codex.", "cell")],
        [p("Brief", "cell_b"), p("Define the outcome, context, inputs, constraints, quality standard, and permission boundary.", "cell")],
        [p("Verify", "cell_b"), p("Check sources, tests, privacy, limitations, and human authority before consequential use.", "cell")],
    ]
    story += [report_table(overview, [1.25*inch, 5.15*inch], first_column=True, repeat=False), Spacer(1, 6)]

    headings = {"Learning Goals", "Final Perspective", "Official Starting Points"}
    for block in blocks:
        rendered = html.escape(block).replace("〔1〕", '<super><font color="#1F5F99">1</font></super>')
        rendered = rendered.replace("https://learn.chatgpt.com/use-cases", '<link href="https://learn.chatgpt.com/use-cases" color="#1F5F99">learn.chatgpt.com/use-cases</link>')
        rendered = rendered.replace("https://developers.openai.com/codex", '<link href="https://developers.openai.com/codex" color="#1F5F99">developers.openai.com/codex</link>')
        if block in headings or block.startswith(("Lesson ", "Capstone:")):
            story.append(p(rendered, "h1"))
        elif block.startswith(("Quick check:", "Your turn:", "Practice workflow:", "Capstone rubric:")):
            label, rest = rendered.split(":", 1)
            story += [p(label, "h2"), p(rest.strip())]
        elif block.startswith("Эффективная "):
            story.append(p(rendered, "russian"))
            for line in footnotes.splitlines():
                match = re.match(r"〔(\d+)〕(.*)", line.strip())
                if match:
                    note = re.sub(r"^\s*Editor[’']s note:\s*", "", match.group(2), flags=re.I)
                    story.append(p(f'<super>{match.group(1)}</super> {html.escape(note)}', "footnote"))
        else:
            story.append(p(rendered))

    inline = load_rows("inline_notes.tsv", "\t")
    reviews = [row for row in load_rows("review_notes.tsv", "\t") if row.get("status") == "open"]
    apparatus = [[p("Type", "cell_b"), p("Text", "cell_b"), p("Explanation", "cell_b")]]
    apparatus += [[p("Inline", "cell"), p(html.escape(row["text"]), "cell"), p(html.escape(row["note"]), "cell")] for row in inline]
    apparatus += [[p("Review", "cell"), p(html.escape(row["text"]), "cell"), p(html.escape(row["issue"]), "cell")] for row in reviews]
    story += [p("Notes and Pending Review", "h1"), report_table(apparatus, [.7*inch, 1.55*inch, 4.15*inch], padding=4)]

    terms = load_rows("reading_terms.csv")
    vocab = [[p("Term", "cell_b"), p("Meaning in this article", "cell_b")]] + [[p(html.escape(row["term"]), "cell"), p(html.escape(row["annotation"]), "cell")] for row in terms]
    story += [KeepTogether([p("Article Vocabulary", "h1"), report_table(vocab, [1.55*inch, 4.85*inch], padding=4)]), Spacer(1, 8), HRFlowable(width="100%", thickness=.7, color=LINE), Spacer(1, 6), p("This course was created by Codex, an AI coding agent from OpenAI.", "small")]

    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont(regular, 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(.7*inch, .34*inch, "Using ChatGPT and Codex · AI Course Follow-up")
        canvas.drawRightString(7.8*inch, .34*inch, f"Page {document.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
