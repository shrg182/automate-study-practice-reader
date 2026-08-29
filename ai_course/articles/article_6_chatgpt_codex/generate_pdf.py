#!/usr/bin/env python3
"""Generate a readable PDF edition of the ChatGPT and Codex follow-up course."""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "ai_course_article_6_chatgpt_codex.pdf"
REGULAR = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
NAVY = colors.HexColor("#102A43")
BLUE = colors.HexColor("#1F5F99")
MUTED = colors.HexColor("#627D98")
LINE = colors.HexColor("#BCCCDC")


def build() -> None:
    regular, bold = "Helvetica", "Helvetica-Bold"
    if REGULAR.exists() and BOLD.exists():
        regular, bold = "CourseArial", "CourseArialBold"
        pdfmetrics.registerFont(TTFont(regular, str(REGULAR)))
        pdfmetrics.registerFont(TTFont(bold, str(BOLD)))
        pdfmetrics.registerFontFamily(regular, normal=regular, bold=bold)

    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle("Title", parent=base["Title"], fontName=bold, fontSize=24, leading=29, textColor=NAVY, alignment=TA_CENTER, spaceAfter=8),
        "dek": ParagraphStyle("Dek", parent=base["BodyText"], fontName=regular, fontSize=10.5, leading=14, textColor=BLUE, alignment=TA_CENTER, spaceAfter=10),
        "h1": ParagraphStyle("H1", parent=base["Heading2"], fontName=bold, fontSize=14, leading=17, textColor=NAVY, spaceBefore=13, spaceAfter=6),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName=regular, fontSize=9.5, leading=14, textColor=colors.HexColor("#1F2933"), spaceAfter=7),
        "exercise": ParagraphStyle("Exercise", parent=base["BodyText"], fontName=regular, fontSize=9.3, leading=13.5, leftIndent=12, rightIndent=12, borderColor=LINE, borderWidth=.5, borderPadding=8, backColor=colors.HexColor("#F0F4F8"), textColor=colors.HexColor("#243B53"), spaceBefore=4, spaceAfter=8),
        "source": ParagraphStyle("Source", parent=base["BodyText"], fontName=regular, fontSize=8, leading=11, textColor=MUTED, spaceAfter=4),
    }
    blocks = [block.strip() for block in (HERE / "article_6_clean.txt").read_text(encoding="utf-8").split("\n\n") if block.strip()]
    title = blocks.pop(0)
    subtitle = blocks.pop(0)
    story = [Paragraph(escape(title), styles["title"]), Paragraph(escape(subtitle), styles["dek"]), HRFlowable(width="100%", thickness=1, color=LINE), Spacer(1, 8)]
    headings = {block for block in blocks if block in {"Learning Goals", "Official Starting Points", "Final Perspective"} or block.startswith(("Lesson ", "Capstone:"))}
    for block in blocks:
        safe = escape(block).replace("https://learn.chatgpt.com/use-cases", '<link href="https://learn.chatgpt.com/use-cases" color="#1F5F99">learn.chatgpt.com/use-cases</link>').replace("https://developers.openai.com/codex", '<link href="https://developers.openai.com/codex" color="#1F5F99">developers.openai.com/codex</link>')
        if block in headings:
            story.append(Paragraph(safe, styles["h1"]))
            story.append(Spacer(1, 3))
        elif block.startswith(("Quick check:", "Your turn:", "Practice workflow:", "Capstone rubric:")):
            story.append(Paragraph(safe, styles["exercise"]))
        elif block.startswith("OpenAI’s current") or block.startswith("Official Codex") or block.startswith("Because interfaces"):
            story.append(Paragraph(safe, styles["source"]))
        else:
            story.append(Paragraph(safe, styles["body"]))

    doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter, leftMargin=.72*inch, rightMargin=.72*inch, topMargin=.62*inch, bottomMargin=.58*inch, title=title, author="Codex, OpenAI")

    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont(regular, 7)
        canvas.setFillColor(MUTED)
        canvas.drawString(.72*inch, .34*inch, "AI Course Follow-up · ChatGPT and Codex in Practice")
        canvas.drawRightString(7.78*inch, .34*inch, f"Page {document.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
