#!/usr/bin/env python3
"""Generate the two-page news-style PDF for the AI-course making story."""

import base64
import csv
import html
import io
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
from reportlab.platypus import HRFlowable, Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "ai_course_article_5_making_the_course.pdf"
REGULAR = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
ITALIC = Path("/System/Library/Fonts/Supplemental/Arial Italic.ttf")
UNICODE = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")
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
    mixed = "STSong-Light"
    if UNICODE.exists():
        mixed = "StoryArialUnicode"
        pdfmetrics.registerFont(TTFont(mixed, str(UNICODE)))

    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle("Title", parent=base["Title"], fontName=bold, fontSize=23, leading=27, textColor=NAVY, alignment=TA_CENTER, spaceAfter=6),
        "dek": ParagraphStyle("Dek", parent=base["BodyText"], fontName=regular, fontSize=10, leading=13, textColor=BLUE, alignment=TA_CENTER, spaceAfter=8),
        "meta": ParagraphStyle("Meta", parent=base["BodyText"], fontName=regular, fontSize=8, textColor=MUTED, alignment=TA_CENTER),
        "h1": ParagraphStyle("H1", parent=base["Heading2"], fontName=bold, fontSize=12.2, leading=14.5, textColor=NAVY, spaceBefore=5, spaceAfter=3.5),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName=regular, fontSize=8.1, leading=11, textColor=colors.HexColor("#1F2933"), spaceAfter=3.5),
        "dialogue": ParagraphStyle("Dialogue", parent=base["BodyText"], fontName=italic, fontSize=8.05, leading=11, textColor=colors.HexColor("#334E68")),
        "footnote": ParagraphStyle("Footnote", parent=base["BodyText"], fontName=italic, fontSize=7.5, leading=10, textColor=MUTED, leftIndent=8, rightIndent=8, spaceAfter=5),
        "footnote_cjk": ParagraphStyle("FootnoteCJK", parent=base["BodyText"], fontName=mixed, fontSize=7.5, leading=10, textColor=MUTED, leftIndent=8, rightIndent=8, spaceAfter=5),
        "cell": ParagraphStyle("Cell", parent=base["BodyText"], fontName=regular, fontSize=7.3, leading=9.2, textColor=colors.HexColor("#243B53")),
        "cell_cjk": ParagraphStyle("CellCJK", parent=base["BodyText"], fontName=mixed, fontSize=7.3, leading=9.2, textColor=colors.HexColor("#243B53")),
        "cell_b": ParagraphStyle("CellB", parent=base["BodyText"], fontName=bold, fontSize=7.3, leading=9.2, textColor=colors.white),
        "note": ParagraphStyle("Note", parent=base["BodyText"], fontName=italic, fontSize=8.2, leading=11.5, textColor=colors.HexColor("#486581")),
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
    # Prefer the learner's latest rich backup; retain the general seed as a fallback.
    seed_path = HERE / "article_5_editor_seed.json"
    if not seed_path.exists():
        seed_path = HERE / "article_5_general_editor_seed.json"
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
    story = [p("How a Question Became an AI Course", "title"), p("From an initial question to a general, reviewable learning sequence.", "dek"), p("AI course companion article | General education edition", "meta"), Spacer(1, 7), HRFlowable(width="100%", thickness=1, color=LINE), Spacer(1, 7)]
    for block in blocks:
        matches = rich_lookup.get(block, [])
        rendered = matches.pop(0) if matches else html.escape(block)
        if block == "Editing Became Part of the Lesson":
            story.append(p(rendered, "h1"))
        elif block in {"Choosing the Journey", "The Color of Difficulty", "Corrections Became Evidence", "A Course About AI—and With AI", "The Story Turns Back on Itself", "Sources"}:
            story.append(p(rendered, "h1"))
        elif block == "脚注":
            continue
        elif re.match(r"^〔\d+〕", block):
            for line in block.splitlines():
                match = re.match(r"^〔(\d+)〕\s*(.*)", line.strip())
                if not match:
                    continue
                number, note = match.groups()
                note = re.sub(r"^Editor[’']s note:\s*", "", note, flags=re.I)
                style = "footnote_cjk" if re.search(r"[\u3400-\u9fff]", note) else "footnote"
                story.append(p(f"<super>{number}</super> {html.escape(note)}", style))
        elif block.startswith(("Learner:", "Codex:")):
            speaker, _words = block.split(":", 1)
            rendered_words = rendered.split(":", 1)[1].strip()
            box = Table([[p(speaker.upper(), "cell_b"), p(rendered_words, "dialogue")]], colWidths=[.78*inch, 5.85*inch])
            box.setStyle(TableStyle([("BACKGROUND", (0,0),(0,0), BLUE), ("BACKGROUND", (1,0),(1,0), PALE), ("BOX", (0,0),(-1,-1), .45, LINE), ("VALIGN", (0,0),(-1,-1), "MIDDLE"), ("PADDING", (0,0),(-1,-1), 4)]))
            story += [box, Spacer(1, 3)]
        else:
            rendered = rendered.replace("〔1〕", '<super><font color="#1F5F99">1</font></super>')
            rendered = rendered.replace("https://learn.chatgpt.com/use-cases", '<link href="https://learn.chatgpt.com/use-cases" color="#1F5F99">learn.chatgpt.com/use-cases</link>')
            rendered = rendered.replace("https://unesdoc.unesco.org/ark:/48223/pf0000386693", '<link href="https://unesdoc.unesco.org/ark:/48223/pf0000386693" color="#1F5F99">unesdoc.unesco.org/ark:/48223/pf0000386693</link>')
            rendered = rendered.replace(
                "缺对应中文", '<font name="STSong-Light">缺对应中文</font>'
            )
            paragraph = p(rendered)
            story.append(KeepTogether([paragraph]) if block.startswith("That exchange became the rhythm") else paragraph)

    def load_rows(name: str, delimiter: str = ",") -> list[dict[str, str]]:
        with (HERE / name).open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle, delimiter=delimiter))

    def cell_p(text: str) -> Paragraph:
        style = "cell_cjk" if re.search(r"[\u3400-\u9fff]", text) else "cell"
        return p(html.escape(text), style)

    def report_table(data, widths, padding=4) -> Table:
        table = Table(data, colWidths=widths, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BLUE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
            ("BOX", (0, 0), (-1, -1), .6, LINE),
            ("INNERGRID", (0, 0), (-1, -1), .35, colors.HexColor("#D9E2EC")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), padding),
        ]))
        return table

    inline = load_rows("inline_notes.tsv", "\t")
    reviews = [row for row in load_rows("review_notes.tsv", "\t") if row.get("status") == "open"]
    apparatus = [[p("Type", "cell_b"), p("Text", "cell_b"), p("Explanation", "cell_b")]]
    apparatus += [[p("Inline", "cell"), cell_p(row["text"]), cell_p(row["note"])] for row in inline]
    apparatus += [[p("Review", "cell"), cell_p(row["text"]), cell_p(row["issue"])] for row in reviews]
    if len(apparatus) > 1:
        story += [p("Notes and Pending Review", "h1"), report_table(apparatus, [.7*inch, 1.55*inch, 4.15*inch])]

    reading_notes = []
    for line in (HERE / "article_5_reading_notes.txt").read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            _, note = line.split("\t", 1)
            reading_notes.append([p(html.escape(note), "note")])
    if reading_notes:
        notes_table = Table(reading_notes, colWidths=[6.4*inch])
        notes_table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),PALE),("BOX",(0,0),(-1,-1),.5,LINE),("PADDING",(0,0),(-1,-1),8)]))
        story += [p("Reader Notes", "h1"), notes_table]

    if seed_path.exists():
        seed = json.loads(seed_path.read_text(encoding="utf-8"))
        media_by_id = {item["id"]: item for item in seed.get("media", [])}
        attached_ids = [media_id for note in seed.get("footnotes", []) for media_id in note.get("mediaIds", [])]
        for media_id in attached_ids:
            item = media_by_id.get(media_id)
            if not item or not item.get("dataUrl", "").startswith("data:image/"):
                continue
            encoded = item["dataUrl"].split(",", 1)[1]
            figure = Image(io.BytesIO(base64.b64decode(encoded)))
            scale = min(1, 3.5*inch/figure.imageWidth, 1.8*inch/figure.imageHeight)
            figure.drawWidth = figure.imageWidth * scale
            figure.drawHeight = figure.imageHeight * scale
            story.append(KeepTogether([
                p("Footnote Reference Image", "h1"),
                figure,
                p(html.escape(item.get("name", "Attached image")), "meta"),
            ]))

    terms = load_rows("reading_terms.csv")
    vocab = [[p("Term", "cell_b"), p("Meaning in this article", "cell_b")]]
    vocab += [[cell_p(row["term"]), cell_p(row["annotation"])] for row in terms]
    story += [KeepTogether([p("Article Vocabulary", "h1"), report_table(vocab, [1.55*inch, 4.85*inch])])]
    story += [Spacer(1,8), HRFlowable(width="100%",thickness=.7,color=LINE), Spacer(1,6), p("This course was created by Codex, an AI coding agent from OpenAI.", "cell")]

    def footer(canvas, document):
        canvas.saveState(); canvas.setFont(regular, 7); canvas.setFillColor(MUTED)
        canvas.drawString(.68*inch, .3*inch, "How a Question Became an AI Course")
        canvas.drawRightString(7.82*inch, .3*inch, f"Page {document.page}"); canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
