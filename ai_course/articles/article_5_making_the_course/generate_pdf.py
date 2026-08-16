#!/usr/bin/env python3
"""Generate the two-page news-style PDF for the AI-course making story."""

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
OUTPUT = HERE / "ai_course_article_5_making_the_course.pdf"
REGULAR = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
ITALIC = Path("/System/Library/Fonts/Supplemental/Arial Italic.ttf")
NAVY = colors.HexColor("#102A43")
BLUE = colors.HexColor("#1F5F99")
MUTED = colors.HexColor("#627D98")
LINE = colors.HexColor("#BCCCDC")
PALE = colors.HexColor("#F0F4F8")


def build() -> None:
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    regular, bold, italic = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"
    if REGULAR.exists() and BOLD.exists() and ITALIC.exists():
        regular, bold, italic = "StoryArial", "StoryArialBold", "StoryArialItalic"
        pdfmetrics.registerFont(TTFont(regular, str(REGULAR)))
        pdfmetrics.registerFont(TTFont(bold, str(BOLD)))
        pdfmetrics.registerFont(TTFont(italic, str(ITALIC)))
        pdfmetrics.registerFontFamily(regular, normal=regular, bold=bold, italic=italic, boldItalic=bold)

    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle("Title", parent=base["Title"], fontName=bold, fontSize=23, leading=27, textColor=NAVY, alignment=TA_CENTER, spaceAfter=6),
        "dek": ParagraphStyle("Dek", parent=base["BodyText"], fontName=regular, fontSize=10, leading=13, textColor=BLUE, alignment=TA_CENTER, spaceAfter=8),
        "meta": ParagraphStyle("Meta", parent=base["BodyText"], fontName=regular, fontSize=8, textColor=MUTED, alignment=TA_CENTER),
        "h1": ParagraphStyle("H1", parent=base["Heading2"], fontName=bold, fontSize=12.2, leading=14.5, textColor=NAVY, spaceBefore=5, spaceAfter=3.5),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName=regular, fontSize=8.1, leading=11, textColor=colors.HexColor("#1F2933"), spaceAfter=3.5),
        "dialogue": ParagraphStyle("Dialogue", parent=base["BodyText"], fontName=italic, fontSize=8.05, leading=11, textColor=colors.HexColor("#334E68")),
        "cell": ParagraphStyle("Cell", parent=base["BodyText"], fontName=regular, fontSize=7.3, leading=9.2, textColor=colors.HexColor("#243B53")),
        "cell_b": ParagraphStyle("CellB", parent=base["BodyText"], fontName=bold, fontSize=7.3, leading=9.2, textColor=colors.white),
    }
    p = lambda text, style="body": Paragraph(text, styles[style])
    blocks = [part.strip() for part in (HERE / "article_5_clean.txt").read_text(encoding="utf-8").split("\n\n") if part.strip()]
    blocks.pop(0)

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

    rich_blocks: list[dict[str, str]] = []
    seed_path = HERE / "article_5_editor_seed.json"
    if seed_path.exists():
        seed = json.loads(seed_path.read_text(encoding="utf-8"))
        soup = BeautifulSoup(seed.get("bodyHTML", ""), "html.parser")
        removing = False
        for paragraph in soup.find_all("p", recursive=False):
            clone = BeautifulSoup(str(paragraph), "html.parser").find("p")
            for rt in clone.select("rt"):
                rt.decompose()
            for gloss in clone.select(".inline-gloss"):
                gloss.decompose()
            plain = clone.get_text("", strip=False).strip()
            if plain == "From a Private Lesson to Shared Reading":
                removing = True
            if removing and plain == "Editing Became Part of the Lesson":
                removing = False
            elif removing:
                continue
            rich_blocks.append({
                "plain": plain,
                "rich": "".join(render_node(child) for child in paragraph.children),
            })
        if rich_blocks and rich_blocks[0]["plain"] == "How a Question Became an AI Course":
            rich_blocks.pop(0)

    rich_lookup: dict[str, list[str]] = {}
    for item in rich_blocks:
        rich_lookup.setdefault(item["plain"], []).append(item["rich"])

    doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter, leftMargin=.68*inch, rightMargin=.68*inch, topMargin=.5*inch, bottomMargin=.52*inch, title="How a Question Became an AI Course", author="Codex, OpenAI")
    story = [p("How a Question Became an AI Course", "title"), p("A learner–AI dialogue became seven lessons, four study articles, and a collaborative editing process.", "dek"), p("AI course companion article | Dialogue edition", "meta"), Spacer(1, 7), HRFlowable(width="100%", thickness=1, color=LINE), Spacer(1, 7)]
    for block in blocks:
        matches = rich_lookup.get(block, [])
        rendered = matches.pop(0) if matches else html.escape(block)
        if block == "Editing Became Part of the Lesson":
            story.append(p(rendered, "h1"))
        elif block in {"Choosing the Journey", "The Color of Difficulty", "Corrections Became Evidence", "A Course About AI—and With AI", "The Story Turns Back on Itself"}:
            story.append(p(rendered, "h1"))
        elif block.startswith(("Learner:", "Codex:")):
            speaker, _words = block.split(":", 1)
            rendered_words = rendered.split(":", 1)[1].strip()
            box = Table([[p(speaker.upper(), "cell_b"), p(rendered_words, "dialogue")]], colWidths=[.78*inch, 5.85*inch])
            box.setStyle(TableStyle([("BACKGROUND", (0,0),(0,0), BLUE), ("BACKGROUND", (1,0),(1,0), PALE), ("BOX", (0,0),(-1,-1), .45, LINE), ("VALIGN", (0,0),(-1,-1), "MIDDLE"), ("PADDING", (0,0),(-1,-1), 4)]))
            story += [box, Spacer(1, 3)]
        else:
            rendered = rendered.replace(
                "缺对应中文", '<font name="STSong-Light">缺对应中文</font>'
            )
            paragraph = p(rendered)
            story.append(KeepTogether([paragraph]) if block.startswith("That exchange became the rhythm") else paragraph)

    def footer(canvas, document):
        canvas.saveState(); canvas.setFont(regular, 7); canvas.setFillColor(MUTED)
        canvas.drawString(.68*inch, .3*inch, "How a Question Became an AI Course")
        canvas.drawRightString(7.82*inch, .3*inch, f"Page {document.page}"); canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
