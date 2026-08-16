#!/usr/bin/env python3
"""
make_liaozhai_annotated_pdf_v2.py

Create a PDF from a Liaozhai text file. Rare/new words are annotated inline
with Chinese pinyin, for example:

    醵（jù）作筵

The script can use:
    1. a built-in rare-word list, and/or
    2. a custom CSV dictionary.

Recommended workflow:
    python3 download_liaozhai_text_v2.py --section original --output lupan.txt

    python3 make_liaozhai_annotated_pdf.py lupan.txt \
        --dictionary my_rare_words.csv \
        --source-url https://liaozhai.5000yan.com/19983.html \
        --output lupan_annotated.pdf

Install dependency:
    python3 -m pip install reportlab

Custom dictionary CSV format:
    term,pinyin,annotation
    醵,jù,众人凑钱；常指凑钱饮酒。
    畛畦,zhěn qí,田间界限；引申为隔阂、成见。

Notes:
    - This script uses inline parenthetical pinyin, not true ruby/furigana
      above characters.
    - The PDF appends a final source section with the original URL and a
      rare/new word table based on the words found in the input text.
    - For Chinese PDF rendering, the default built-in ReportLab CID font is
      STSong-Light. You can provide a custom .ttf/.otf font with --font-path.
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_INPUT = Path("lupan.txt")
DEFAULT_OUTPUT = Path("lupan_annotated.pdf")
DEFAULT_SOURCE_URL = "https://liaozhai.5000yan.com/19983.html"

# Common Chinese-capable fonts. The script tries these before falling back to
# ReportLab's built-in STSong-Light CID font. Do not copy font files into your
# project; just point to the font path on your own computer when needed.
DEFAULT_FONT_CANDIDATES = [
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("/System/Library/Fonts/STHeiti Light.ttc"),
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/System/Library/Fonts/Supplemental/Songti.ttc"),
    Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
    Path("/Library/Fonts/Arial Unicode.ttf"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf"),
    Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
]


@dataclass(frozen=True)
class RareEntry:
    """A rare/new word entry used for inline pinyin annotation."""

    term: str
    pinyin: str
    annotation: str


# Built-in starter dictionary for Liaozhai / 陆判.
# You can expand this list or use --dictionary my_rare_words.csv.
BUILT_IN_ENTRIES: list[RareEntry] = [
    RareEntry("陵阳", "líng yáng", "地名；文中为朱尔旦籍贯。"),
    RareEntry("尔旦", "ěr dàn", "人名用字；文中朱尔旦。"),
    RareEntry("笃", "dǔ", "专一、厚实；文中指学习用功。"),
    RareEntry("邑", "yì", "县、地方。"),
    RareEntry("庙", "miào", "供奉神灵或先人的建筑。"),
    RareEntry("醵", "jù", "众人凑钱；常指凑钱饮酒。"),
    RareEntry("筵", "yán", "酒席、宴席。"),
    RareEntry("庑", "wǔ", "堂下周围的廊屋、厢房。"),
    RareEntry("判官", "pàn guān", "旧时官名；也指阴司审判鬼魂的官。"),
    RareEntry("髯", "rán", "两腮的胡子，也泛指大胡子。"),
    RareEntry("觞", "shāng", "古代酒杯；也指敬酒、饮酒。"),
    RareEntry("酹", "lèi", "把酒洒在地上祭奠。"),
    RareEntry("畛畦", "zhěn qí", "田间界限；引申为隔阂、成见。"),
    RareEntry("搴", "qiān", "揭起、掀开。"),
    RareEntry("殆", "dài", "大概、恐怕；也有危险之义。"),
    RareEntry("锧", "zhì", "古代刑具，常与斧连用。"),
    RareEntry("斧锧", "fǔ zhì", "古代刑具；借指刑罚。"),
    RareEntry("爇", "ruò", "点燃、焚烧。"),
    RareEntry("妍媸", "yán chī", "美与丑。"),
    RareEntry("媸", "chī", "丑。"),
    RareEntry("觥", "gōng", "古代酒器；也泛指大酒杯。"),
    RareEntry("揶揄", "yé yú", "嘲笑、戏弄。"),
    RareEntry("湔", "jiān", "洗；文中可理解为清洗、整治。"),
    RareEntry("曩", "nǎng", "从前、过去。"),
    RareEntry("嘱", "zhǔ", "嘱咐、托付。"),
    RareEntry("扃", "jiōng", "门闩；也指关门。"),
    RareEntry("瘗", "yì", "埋葬。"),
    RareEntry("靥", "yè", "酒窝；也指面颊上的笑纹。"),
    RareEntry("醮", "jiào", "古代婚礼；女子出嫁。"),
    RareEntry("鞫", "jū", "审问、审讯。"),
    RareEntry("拷掠", "kǎo lüè", "拷打、刑讯。"),
    RareEntry("椁", "guǒ", "套在棺材外面的大棺。"),
    RareEntry("柩", "jiù", "装着尸体的棺材；灵柩。"),
    RareEntry("棺椁", "guān guǒ", "棺材和套在外面的椁。"),
    RareEntry("馔", "zhuàn", "饭食、酒食。"),
    RareEntry("缱绻", "qiǎn quǎn", "情意缠绵，难舍难分。"),
    RareEntry("卤簿", "lǔ bù", "古代帝王或官员出行的仪仗。"),
    RareEntry("镌", "juān", "雕刻。"),
    RareEntry("沕", "wù", "古字；有潜藏、隐没义；文中作人名用字。"),
    RareEntry("闱", "wéi", "科举时代的考场；也可指宫中小门。"),
    RareEntry("闼", "tà", "门、小门。"),
    RareEntry("辟", "pì", "打开；文中如“扉自辟”。"),
    RareEntry("榻", "tà", "狭长而较矮的床。"),
    RareEntry("夙", "sù", "早；旧时、平素。"),
    RareEntry("盥", "guàn", "洗手、洗脸。"),
    RareEntry("逡巡", "qūn xún", "迟疑不前；有所顾忌。"),
    RareEntry("踉跄", "liàng qiàng", "走路不稳。"),
    RareEntry("惶遽", "huáng jù", "惊慌急迫。"),
    RareEntry("遽", "jù", "急、仓促。"),
    RareEntry("赍", "jī", "携带；怀着。"),
    RareEntry("赍恨", "jī hèn", "怀恨。"),
    RareEntry("颡", "sǎng", "额头。"),
    RareEntry("拊", "fǔ", "拍、轻击。"),
    RareEntry("胫", "jìng", "小腿。"),
    RareEntry("诘", "jié", "责问、追问。"),
    RareEntry("诡", "guǐ", "欺诈、怪异。"),
    RareEntry("俨", "yǎn", "庄重、整齐的样子。"),
    RareEntry("旌", "jīng", "旗帜；也指表彰。"),
    RareEntry("麾", "huī", "古代指挥用的旗；也指指挥。"),
    RareEntry("舆", "yú", "车；轿。"),
    RareEntry("辇", "niǎn", "古代人拉的车，后常指帝王车驾。"),
    RareEntry("谒", "yè", "拜见。"),
    RareEntry("谬", "miù", "错误、荒谬。"),
    RareEntry("绐", "dài", "欺骗。"),
    RareEntry("怃然", "wǔ rán", "失意、惆怅的样子。"),
    RareEntry("恻然", "cè rán", "悲伤、同情的样子。"),
    RareEntry("踞", "jù", "蹲坐；占据。"),
    RareEntry("嗔", "chēn", "生气、责怪。"),
    RareEntry("颔", "hàn", "下巴；也指点头。"),
]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Generate a PDF from a Chinese text file, annotating rare/new words "
            "with pinyin inline."
        )
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT,
        help="Input text file. Default: lupan.txt",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output PDF file. Default: lupan_annotated.pdf",
    )
    parser.add_argument(
        "--dictionary",
        type=Path,
        default=None,
        help=(
            "Optional CSV dictionary with columns: term,pinyin,annotation. "
            "Custom entries override built-in entries with the same term."
        ),
    )
    parser.add_argument(
        "--no-built-in",
        action="store_true",
        help="Use only the custom CSV dictionary; ignore the built-in list.",
    )
    parser.add_argument(
        "--title",
        default="《陆判》注音阅读版",
        help="PDF title. Default: 《陆判》注音阅读版",
    )
    parser.add_argument(
        "--subtitle",
        default="生僻字词用括号标注拼音",
        help="PDF subtitle.",
    )
    parser.add_argument(
        "--source-url",
        default=DEFAULT_SOURCE_URL,
        help=(
            "Original text URL to print at the end of the PDF. "
            f"Default: {DEFAULT_SOURCE_URL}"
        ),
    )
    parser.add_argument(
        "--no-source-section",
        action="store_true",
        help="Do not append the original text URL/source section.",
    )
    parser.add_argument(
        "--font-path",
        type=Path,
        default=None,
        help=(
            "Optional path to a .ttf/.otf/.ttc font file. If omitted, the "
            "script tries common macOS/Linux Chinese fonts, then falls back to "
            "ReportLab's built-in STSong-Light Chinese font."
        ),
    )
    parser.add_argument(
        "--use-built-in-cid-font",
        action="store_true",
        help=(
            "Skip system font auto-detection and force ReportLab's built-in "
            "STSong-Light CID font. This works, but pinyin spacing may look "
            "less natural on some systems."
        ),
    )
    parser.add_argument(
        "--font-name",
        default="CustomChineseFont",
        help="Internal font name when --font-path is used.",
    )
    parser.add_argument(
        "--font-size",
        type=int,
        default=12,
        help="Main body font size. Default: 12",
    )
    parser.add_argument(
        "--leading",
        type=int,
        default=20,
        help="Line spacing. Default: 20",
    )
    parser.add_argument(
        "--annotated-text-output",
        type=Path,
        default=None,
        help="Optional path to also save the annotated text as .txt.",
    )
    parser.add_argument(
        "--no-table",
        action="store_true",
        help="Do not append a rare-word table at the end of the PDF.",
    )
    parser.add_argument(
        "--max-example-length",
        type=int,
        default=36,
        help="Maximum length of examples in the rare-word table. Default: 36",
    )
    return parser.parse_args()


def load_text(path: Path) -> str:
    """Load UTF-8 text from a file."""
    if not path.exists():
        raise FileNotFoundError(f"Input text file not found: {path}")
    return path.read_text(encoding="utf-8")


def load_custom_entries(path: Path) -> list[RareEntry]:
    """Load rare-word entries from a CSV file."""
    if not path.exists():
        raise FileNotFoundError(f"Dictionary file not found: {path}")

    entries: list[RareEntry] = []

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError(f"Dictionary file has no header row: {path}")

        fieldnames = {name.strip().lower(): name for name in reader.fieldnames}

        term_field = (
            fieldnames.get("term")
            or fieldnames.get("word")
            or fieldnames.get("字")
            or fieldnames.get("词")
            or fieldnames.get("字/词")
        )
        pinyin_field = fieldnames.get("pinyin") or fieldnames.get("拼音")
        annotation_field = (
            fieldnames.get("annotation")
            or fieldnames.get("note")
            or fieldnames.get("meaning")
            or fieldnames.get("简注")
            or fieldnames.get("注释")
        )

        if not term_field or not pinyin_field or not annotation_field:
            raise ValueError(
                "Dictionary CSV must contain columns like: "
                "term,pinyin,annotation"
            )

        for row_number, row in enumerate(reader, start=2):
            term = (row.get(term_field) or "").strip()
            pinyin = (row.get(pinyin_field) or "").strip()
            annotation = (row.get(annotation_field) or "").strip()

            if not term:
                continue

            if not pinyin or not annotation:
                raise ValueError(
                    f"Missing pinyin or annotation in {path} at row {row_number}."
                )

            entries.append(RareEntry(term, pinyin, annotation))

    return entries


def merge_entries(
    built_in_entries: Iterable[RareEntry],
    custom_entries: Iterable[RareEntry],
) -> list[RareEntry]:
    """
    Merge built-in and custom entries.

    Custom entries with the same term override built-in entries.
    """
    merged: dict[str, RareEntry] = {}

    for entry in built_in_entries:
        merged[entry.term] = entry

    for entry in custom_entries:
        merged[entry.term] = entry

    return sorted(
        merged.values(),
        key=lambda item: (-len(item.term), item.term),
    )


def normalize_text(text: str) -> str:
    """Normalize line endings and remove excessive trailing spaces."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def find_sentence_example(text: str, term: str, max_length: int = 36) -> str:
    """
    Find a short example around the first occurrence of a term.

    This does not try to do perfect classical Chinese sentence segmentation.
    It simply looks around nearby punctuation.
    """
    index = text.find(term)
    if index == -1:
        return ""

    punctuation = "。！？；\n"
    start = max(text.rfind(mark, 0, index) for mark in punctuation)
    start = 0 if start == -1 else start + 1

    end_candidates = [
        text.find(mark, index + len(term))
        for mark in punctuation
        if text.find(mark, index + len(term)) != -1
    ]
    end = min(end_candidates) + 1 if end_candidates else len(text)

    example = text[start:end].strip()

    if len(example) <= max_length:
        return example

    center_start = max(0, index - max_length // 2)
    center_end = min(len(text), center_start + max_length)
    snippet = text[center_start:center_end].strip()

    if center_start > 0:
        snippet = "……" + snippet
    if center_end < len(text):
        snippet += "……"

    return snippet


def annotate_text(
    text: str,
    entries: list[RareEntry],
) -> tuple[str, dict[str, int]]:
    """
    Annotate rare words with pinyin.

    Uses a longest-match scan so that longer entries like “畛畦” are matched
    before single-character entries.
    """
    entries_by_first_char: dict[str, list[RareEntry]] = {}

    for entry in entries:
        if not entry.term:
            continue
        first_char = entry.term[0]
        entries_by_first_char.setdefault(first_char, []).append(entry)

    for first_char in entries_by_first_char:
        entries_by_first_char[first_char].sort(
            key=lambda item: (-len(item.term), item.term)
        )

    result: list[str] = []
    counts: dict[str, int] = {}
    index = 0

    while index < len(text):
        char = text[index]
        candidates = entries_by_first_char.get(char, [])
        matched_entry: RareEntry | None = None

        for entry in candidates:
            if text.startswith(entry.term, index):
                matched_entry = entry
                break

        if matched_entry is None:
            result.append(char)
            index += 1
            continue

        result.append(f"{matched_entry.term}（{matched_entry.pinyin}）")
        counts[matched_entry.term] = counts.get(matched_entry.term, 0) + 1
        index += len(matched_entry.term)

    return "".join(result), counts


def find_default_font_path() -> Path | None:
    """Return the first available default Chinese-capable font path."""
    for candidate in DEFAULT_FONT_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


def register_pdf_font(
    font_path: Path | None,
    font_name: str,
    force_builtin_cid_font: bool = False,
) -> tuple[str, str]:
    """
    Register and return the font name and a human-readable font source.

    Best result:
        Use a TrueType/OpenType Chinese-capable font such as PingFang.ttc.

    Fallback:
        Use ReportLab's built-in STSong-Light CID font. It usually renders
        Chinese, but pinyin with tone marks may have less natural spacing.
    """
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError as error:
        raise RuntimeError(
            "ReportLab is required to create PDF files.\n"
            "Install it with:\n"
            "    python3 -m pip install reportlab"
        ) from error

    if font_path is not None:
        if not font_path.exists():
            raise FileNotFoundError(f"Font file not found: {font_path}")
        pdfmetrics.registerFont(
            TTFont(font_name, str(font_path), subfontIndex=0)
        )
        return font_name, str(font_path)

    if not force_builtin_cid_font:
        auto_font_path = find_default_font_path()
        if auto_font_path is not None:
            try:
                pdfmetrics.registerFont(
                    TTFont(font_name, str(auto_font_path), subfontIndex=0)
                )
                return font_name, str(auto_font_path)
            except Exception:
                # Continue to the built-in fallback below.
                pass

    default_font = "STSong-Light"
    pdfmetrics.registerFont(UnicodeCIDFont(default_font))
    return default_font, "ReportLab built-in STSong-Light"

def paragraph_from_text(text: str, style):
    """Create a ReportLab Paragraph safely from plain text."""
    from reportlab.platypus import Paragraph

    escaped = html.escape(text)
    return Paragraph(escaped, style)


def build_story_elements(
    annotated_text: str,
    body_style,
    spacer_height: int = 8,
) -> list:
    """Build ReportLab elements for the annotated story text."""
    from reportlab.platypus import Spacer

    elements: list = []

    # Split on blank lines first; if the source has no blank lines, keep lines
    # as manageable Paragraph objects.
    blocks = re.split(r"\n\s*\n", annotated_text)

    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]

        if not lines:
            elements.append(Spacer(1, spacer_height))
            continue

        for line in lines:
            elements.append(paragraph_from_text(line, body_style))
            elements.append(Spacer(1, spacer_height))

    return elements



def build_source_section_elements(
    source_url: str,
    font_name: str,
    title: str = "原文来源",
) -> list:
    """Build a source information section for the end of the PDF."""
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Paragraph, Spacer

    title_style = ParagraphStyle(
        name="SourceTitle",
        fontName=font_name,
        fontSize=16,
        leading=22,
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        name="SourceBody",
        fontName=font_name,
        fontSize=10,
        leading=15,
        wordWrap="CJK",
    )

    if not source_url.strip():
        source_url = "未提供"

    elements = [
        Paragraph(html.escape(title), title_style),
        Spacer(1, 6),
        Paragraph(html.escape(f"原文网址：{source_url}"), body_style),
        Spacer(1, 6),
        Paragraph(
            html.escape(
                "说明：本文正文中的生僻字词按脚本词典自动匹配，并以括号形式标注拼音。"
            ),
            body_style,
        ),
        Spacer(1, 14),
    ]
    return elements


def build_word_table_elements(
    original_text: str,
    entries: list[RareEntry],
    counts: dict[str, int],
    font_name: str,
    max_example_length: int,
    start_new_page: bool = True,
) -> list:
    """Build a rare-word table for the end of the PDF."""
    from reportlab.lib import colors
    from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import ParagraphStyle

    used_entries = [entry for entry in entries if counts.get(entry.term, 0) > 0]

    if not used_entries:
        return []

    title_style = ParagraphStyle(
        name="WordTableTitle",
        fontName=font_name,
        fontSize=16,
        leading=22,
        spaceAfter=10,
    )
    cell_style = ParagraphStyle(
        name="WordTableCell",
        fontName=font_name,
        fontSize=9,
        leading=13,
        wordWrap="CJK",
    )

    data: list[list] = [
        [
            paragraph_from_text("字/词", cell_style),
            paragraph_from_text("拼音", cell_style),
            paragraph_from_text("简注", cell_style),
            paragraph_from_text("次数", cell_style),
            paragraph_from_text("原文词例", cell_style),
        ]
    ]

    for entry in sorted(used_entries, key=lambda item: (-counts[item.term], item.term)):
        example = find_sentence_example(
            original_text,
            entry.term,
            max_length=max_example_length,
        )
        data.append(
            [
                paragraph_from_text(entry.term, cell_style),
                paragraph_from_text(entry.pinyin, cell_style),
                paragraph_from_text(entry.annotation, cell_style),
                paragraph_from_text(str(counts[entry.term]), cell_style),
                paragraph_from_text(example, cell_style),
            ]
        )

    table = Table(
        data,
        colWidths=[50, 65, 145, 35, 160],
        repeatRows=1,
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.grey),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )

    elements: list = [
        Paragraph("生字表 / Rare and New Words", title_style),
        Spacer(1, 8),
        table,
    ]

    if start_new_page:
        elements.insert(0, PageBreak())

    return elements


def build_pdf(
    output_path: Path,
    title: str,
    subtitle: str,
    original_text: str,
    annotated_text: str,
    entries: list[RareEntry],
    counts: dict[str, int],
    font_name: str,
    font_size: int,
    leading: int,
    include_source_section: bool,
    source_url: str,
    include_table: bool,
    max_example_length: int,
) -> None:
    """Build the annotated PDF."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    except ImportError as error:
        raise RuntimeError(
            "ReportLab is required to create PDF files.\n"
            "Install it with:\n"
            "    python3 -m pip install reportlab"
        ) from error

    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=title,
        author="Generated by make_liaozhai_annotated_pdf.py",
    )

    title_style = ParagraphStyle(
        name="Title",
        fontName=font_name,
        fontSize=20,
        leading=28,
        alignment=1,
        spaceAfter=8,
    )
    subtitle_style = ParagraphStyle(
        name="Subtitle",
        fontName=font_name,
        fontSize=10,
        leading=14,
        alignment=1,
        spaceAfter=16,
    )
    body_style = ParagraphStyle(
        name="Body",
        fontName=font_name,
        fontSize=font_size,
        leading=leading,
        firstLineIndent=18,
        wordWrap="CJK",
        spaceAfter=2,
    )

    elements: list = [
        Paragraph(html.escape(title), title_style),
        Paragraph(html.escape(subtitle), subtitle_style),
        Spacer(1, 8),
    ]

    elements.extend(build_story_elements(annotated_text, body_style))

    if include_source_section or include_table:
        from reportlab.platypus import PageBreak

        elements.append(PageBreak())

    if include_source_section:
        elements.extend(
            build_source_section_elements(
                source_url=source_url,
                font_name=font_name,
            )
        )

    if include_table:
        elements.extend(
            build_word_table_elements(
                original_text=original_text,
                entries=entries,
                counts=counts,
                font_name=font_name,
                max_example_length=max_example_length,
                start_new_page=False,
            )
        )

    doc.build(elements)


def print_summary(
    input_path: Path,
    output_path: Path,
    annotated_text_path: Path | None,
    counts: dict[str, int],
    font_source: str,
    source_url: str,
) -> None:
    """Print a short terminal summary."""
    total_matches = sum(counts.values())
    unique_terms = len(counts)

    print(f"Input text: {input_path}")
    print(f"Output PDF: {output_path}")
    if annotated_text_path:
        print(f"Output annotated text: {annotated_text_path}")
    print(f"PDF font source: {font_source}")
    print(f"Original text URL: {source_url}")
    print(f"Annotated rare/new word types: {unique_terms}")
    print(f"Total annotations inserted: {total_matches}")


def main() -> None:
    """Run the command-line program."""
    args = parse_args()

    try:
        original_text = normalize_text(load_text(args.input))

        custom_entries: list[RareEntry] = []
        if args.dictionary is not None:
            custom_entries = load_custom_entries(args.dictionary)

        built_in_entries = [] if args.no_built_in else BUILT_IN_ENTRIES
        entries = merge_entries(built_in_entries, custom_entries)

        if not entries:
            raise ValueError(
                "No dictionary entries available. Use the built-in list or "
                "provide --dictionary my_rare_words.csv."
            )

        annotated_text, counts = annotate_text(original_text, entries)

        if args.annotated_text_output is not None:
            args.annotated_text_output.parent.mkdir(parents=True, exist_ok=True)
            args.annotated_text_output.write_text(annotated_text, encoding="utf-8")

        font_name, font_source = register_pdf_font(
            args.font_path,
            args.font_name,
            force_builtin_cid_font=args.use_built_in_cid_font,
        )

        build_pdf(
            output_path=args.output,
            title=args.title,
            subtitle=args.subtitle,
            original_text=original_text,
            annotated_text=annotated_text,
            entries=entries,
            counts=counts,
            font_name=font_name,
            font_size=args.font_size,
            leading=args.leading,
            include_source_section=not args.no_source_section,
            source_url=args.source_url,
            include_table=not args.no_table,
            max_example_length=args.max_example_length,
        )

        print_summary(
            input_path=args.input,
            output_path=args.output,
            annotated_text_path=args.annotated_text_output,
            counts=counts,
            font_source=font_source,
            source_url=args.source_url,
        )

    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
