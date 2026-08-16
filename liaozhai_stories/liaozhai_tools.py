#!/usr/bin/env python3
"""Reusable tools for Liaozhai story study files."""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_FONT_CANDIDATES = [
    Path("/System/Library/Fonts/Supplemental/Songti.ttc"),
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("/System/Library/Fonts/STHeiti Light.ttc"),
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
    Path("/Library/Fonts/Arial Unicode.ttf"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf"),
    Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
]


@dataclass(frozen=True)
class RareEntry:
    """One rare or classical word entry."""

    term: str
    pinyin: str
    annotation: str


class SectionNotFoundError(ValueError):
    """Raised when a requested page section cannot be found."""


def clean_text(text: str) -> str:
    """Normalize whitespace from extracted web page text."""
    text = unicodedata.normalize("NFKC", text)
    lines = []
    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            lines.append(line)
    return "\n".join(lines).strip()


def normalize_story_text(text: str) -> str:
    """Normalize local story text while preserving paragraph breaks."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    protected_urls: dict[str, str] = {}

    def protect_url(match: re.Match[str]) -> str:
        placeholder = f"__URL_{len(protected_urls)}__"
        protected_urls[placeholder] = match.group(0)
        return placeholder

    text = re.sub(r"https?://[^\s，。；：！？]+", protect_url, text)
    text = text.translate(str.maketrans({",": "，", ";": "；", ":": "：", "?": "？", "!": "！"}))
    for placeholder, url in protected_urls.items():
        text = text.replace(placeholder, url)
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def download_html(url: str, timeout: int = 20) -> str:
    """Download HTML with headers friendly to Chinese literature sites."""
    try:
        import requests
    except ImportError as error:
        raise RuntimeError(
            "requests is required for downloading.\n"
            "Install it with: python3 -m pip install requests"
        ) from error

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
        ),
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    if not response.encoding or response.encoding.lower() == "iso-8859-1":
        response.encoding = response.apparent_encoding
    return response.text


def html_to_text(page_html: str) -> str:
    """Convert a Liaozhai HTML page to readable text."""
    try:
        from bs4 import BeautifulSoup
    except ImportError as error:
        raise RuntimeError(
            "beautifulsoup4 is required for parsing HTML.\n"
            "Install it with: python3 -m pip install beautifulsoup4"
        ) from error

    soup = BeautifulSoup(page_html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    content = (
        soup.find("article")
        or soup.find("main")
        or soup.find("div", class_=re.compile(r"article|content|post|entry", re.I))
        or soup.body
        or soup
    )
    return clean_text(content.get_text(separator="\n"))


def html_section_to_text(page_html: str, section: str) -> str | None:
    """Extract explicitly labelled paragraph panels from newer 5000yan pages."""
    if section not in {"original", "translation"}:
        return None
    try:
        from bs4 import BeautifulSoup
    except ImportError as error:
        raise RuntimeError("beautifulsoup4 is required for parsing HTML") from error

    soup = BeautifulSoup(page_html, "html.parser")
    labels = {"original": ("原文", "para-yuanwen"), "translation": ("翻译", "para-fanyi")}
    label, class_name = labels[section]
    paragraphs = soup.select(f'[data-section="{label}"], .{class_name}')
    seen: set[int] = set()
    selected: list[str] = []
    for paragraph in paragraphs:
        identity = id(paragraph)
        if identity in seen:
            continue
        seen.add(identity)
        text = clean_text(paragraph.get_text(" ", strip=True))
        if text:
            selected.append(text)
    return normalize_story_text("\n\n".join(selected)) if selected else None


def marker_span(text: str, label: str, start: int = 0) -> tuple[int, int] | None:
    """Return the start/end span of markers such as 〖原文〗 or 【翻译】."""
    escaped_label = re.escape(label)
    patterns = [
        rf"[〖【\[]\s*{escaped_label}\s*[〗】\]]",
        rf"(?m)^\s*{escaped_label}\s*$",
    ]
    for pattern in patterns:
        match = re.search(pattern, text[start:])
        if match:
            return start + match.start(), start + match.end()
    return None


def extract_section(text: str, section: str) -> str:
    """Extract all, original, translation, or commentary from page text."""
    if section == "all":
        return text

    labels = {
        "original": ("原文", ["翻译", "译文"]),
        "translation": ("翻译", ["异史氏曰"]),
        "commentary": ("异史氏曰", ["翻译", "译文"]),
    }
    if section not in labels:
        raise ValueError(f"Unknown section: {section}")

    start_label, end_labels = labels[section]
    start_span = marker_span(text, start_label)
    if start_span is None and section == "translation":
        start_span = marker_span(text, "译文")
    if start_span is None:
        raise SectionNotFoundError(f"Could not find section marker: {start_label}")

    start_index = start_span[1]
    end_candidates = [
        span[0]
        for label in end_labels
        if (span := marker_span(text, label, start_index)) is not None
    ]
    end_index = min(end_candidates) if end_candidates else len(text)
    return clean_text(text[start_index:end_index])


def download_story(url: str, output_path: Path, section: str, debug_output: Path | None) -> str:
    """Download a story section and write it to disk."""
    page_html = download_html(url)
    page_text = html_to_text(page_html)
    if debug_output is not None:
        debug_output.parent.mkdir(parents=True, exist_ok=True)
        debug_output.write_text(page_text + "\n", encoding="utf-8")

    selected_text = html_section_to_text(page_html, section) or extract_section(page_text, section)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(selected_text + "\n", encoding="utf-8")
    return selected_text


def load_entries(paths: Iterable[Path]) -> list[RareEntry]:
    """Load rare-word CSV files with flexible Chinese or English headers."""
    entries: list[RareEntry] = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Dictionary file not found: {path}")
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames is None:
                raise ValueError(f"Dictionary file has no header row: {path}")
            fields = {name.strip().lower(): name for name in reader.fieldnames}
            term_field = (
                fields.get("term")
                or fields.get("word")
                or fields.get("字")
                or fields.get("词")
                or fields.get("字/词")
            )
            pinyin_field = fields.get("pinyin") or fields.get("拼音")
            note_field = (
                fields.get("annotation")
                or fields.get("note")
                or fields.get("meaning")
                or fields.get("简注")
                or fields.get("注释")
            )
            if not term_field or not pinyin_field or not note_field:
                raise ValueError(f"{path} must contain term,pinyin,annotation columns")
            for row_number, row in enumerate(reader, start=2):
                term = (row.get(term_field) or "").strip()
                pinyin = (row.get(pinyin_field) or "").strip()
                annotation = (row.get(note_field) or "").strip()
                if not term:
                    continue
                if not pinyin or not annotation:
                    raise ValueError(f"Missing pinyin or annotation in {path}:{row_number}")
                entries.append(RareEntry(term, pinyin, annotation))

    merged: dict[str, RareEntry] = {}
    for entry in entries:
        merged[entry.term] = entry
    return sorted(merged.values(), key=lambda item: (-len(item.term), item.term))


def annotate_text(
    text: str,
    entries: list[RareEntry],
    repeat_annotations: bool = False,
) -> tuple[str, dict[str, int]]:
    """Annotate text by longest dictionary match."""
    by_first_char: dict[str, list[RareEntry]] = {}
    for entry in entries:
        by_first_char.setdefault(entry.term[0], []).append(entry)
    for items in by_first_char.values():
        items.sort(key=lambda item: (-len(item.term), item.term))

    result: list[str] = []
    counts: dict[str, int] = {}
    already_annotated: set[str] = set()
    index = 0
    while index < len(text):
        matched = None
        for entry in by_first_char.get(text[index], []):
            if text.startswith(entry.term, index):
                matched = entry
                break
        if matched is None:
            result.append(text[index])
            index += 1
            continue
        if repeat_annotations or matched.term not in already_annotated:
            result.append(f"{matched.term}（{matched.pinyin}）")
            already_annotated.add(matched.term)
        else:
            result.append(matched.term)
        counts[matched.term] = counts.get(matched.term, 0) + 1
        index += len(matched.term)
    return "".join(result), counts


def find_sentence_example(text: str, term: str, max_length: int = 36) -> str:
    """Find a compact source example around a term."""
    index = text.find(term)
    if index == -1:
        return ""

    punctuation = "。！？；\n"
    start = max(text.rfind(mark, 0, index) for mark in punctuation)
    start = 0 if start == -1 else start + 1
    ends = [
        text.find(mark, index + len(term))
        for mark in punctuation
        if text.find(mark, index + len(term)) != -1
    ]
    end = min(ends) + 1 if ends else len(text)
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


def found_entries(text: str, entries: list[RareEntry], max_example_length: int) -> list[dict[str, str | int]]:
    """Return dictionary entries that occur in the story."""
    rows = []
    for entry in entries:
        count = text.count(entry.term)
        if count == 0:
            continue
        rows.append(
            {
                "term": entry.term,
                "pinyin": entry.pinyin,
                "annotation": entry.annotation,
                "count": count,
                "context": find_sentence_example(text, entry.term, max_example_length),
                "position": text.find(entry.term),
            }
        )
    rows.sort(key=lambda row: int(row["position"]))
    return rows


def write_word_table(output_path: Path, rows: list[dict[str, str | int]], source_path: Path) -> None:
    """Write a tab-separated rare-word table."""
    lines = [
        "阅读词表",
        f"来源文件：{source_path}",
        f"检出条目数：{len(rows)}",
        "",
        "序号\t字/词\t拼音\t简注\t出现次数\t原文词例",
    ]
    for number, row in enumerate(rows, start=1):
        lines.append(
            "\t".join(
                [
                    str(number),
                    str(row["term"]),
                    str(row["pinyin"]),
                    str(row["annotation"]),
                    str(row["count"]),
                    str(row["context"]),
                ]
            )
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def find_default_font_path() -> Path | None:
    """Return the first available Chinese-capable system font path."""
    for candidate in DEFAULT_FONT_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


def default_subfont_index(font_path: Path) -> int:
    """Pick a simplified-Chinese face from TTC font collections."""
    if font_path.name == "Songti.ttc":
        return 6
    if font_path.name in {"STHeiti Light.ttc", "STHeiti Medium.ttc"}:
        return 1
    return 0


def register_pdf_font(font_path: Path | None, font_name: str, force_builtin: bool) -> tuple[str, str]:
    """Register a ReportLab font and return its internal name/source."""
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError as error:
        raise RuntimeError(
            "ReportLab is required to create PDF files.\n"
            "Install it with: python3 -m pip install reportlab"
        ) from error

    if font_path is not None:
        if not font_path.exists():
            raise FileNotFoundError(f"Font file not found: {font_path}")
        pdfmetrics.registerFont(TTFont(font_name, str(font_path), subfontIndex=default_subfont_index(font_path)))
        return font_name, str(font_path)

    if not force_builtin:
        auto_font_path = find_default_font_path()
        if auto_font_path is not None:
            try:
                pdfmetrics.registerFont(TTFont(font_name, str(auto_font_path), subfontIndex=default_subfont_index(auto_font_path)))
                return font_name, str(auto_font_path)
            except Exception:
                pass

    default_font = "STSong-Light"
    pdfmetrics.registerFont(UnicodeCIDFont(default_font))
    return default_font, "ReportLab built-in STSong-Light"


def register_pdf_bold_variant(font_path: Path | None, font_name: str) -> bool:
    """Register a genuine bold face for ReportLab paragraph <b> markup."""
    if font_path is None:
        font_path = find_default_font_path()
    if font_path is None or font_path.name != "Songti.ttc":
        return False
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    bold_name = f"{font_name}-Bold"
    pdfmetrics.registerFont(TTFont(bold_name, str(font_path), subfontIndex=1))
    pdfmetrics.registerFontFamily(
        font_name,
        normal=font_name,
        bold=bold_name,
        italic=font_name,
        boldItalic=bold_name,
    )
    return True


def paragraph_from_text(text: str, style):
    """Create a ReportLab paragraph from plain text."""
    from reportlab.platypus import Paragraph

    return Paragraph(html.escape(text), style)


def styled_paragraph_markup(text: str, text_styles: list[dict[str, object]]) -> str:
    """Convert saved editor styles into safe ReportLab paragraph markup."""
    ranges: list[tuple[int, int, dict[str, object]]] = []
    for item in text_styles:
        selected = str(item.get("text", ""))
        if not selected:
            continue
        start = text.find(selected)
        if start < 0:
            continue
        end = start + len(selected)
        if any(start < old_end and end > old_start for old_start, old_end, _ in ranges):
            continue
        ranges.append((start, end, item))
    if not ranges:
        return html.escape(text)

    parts: list[str] = []
    cursor = 0
    for start, end, item in sorted(ranges):
        parts.append(html.escape(text[cursor:start]))
        value = html.escape(text[start:end])
        if item.get("underline"):
            value = f'<u color="#333333" width="0.7" offset="-4">{value}</u>'
        if item.get("bold"):
            value = f"<b>{value}</b>"
        background = str(item.get("background", "")).strip()
        if re.fullmatch(r"#[0-9a-fA-F]{6}", background):
            value = f'<span backColor="{background}">{value}</span>'
        parts.append(value)
        cursor = end
    parts.append(html.escape(text[cursor:]))
    return "".join(parts)


def build_story_elements(
    annotated_text: str,
    body_style,
    spacer_height: int = 8,
    text_styles: list[dict[str, object]] | None = None,
) -> list:
    """Build body paragraphs for the PDF."""
    from reportlab.platypus import Spacer

    elements = []
    for block in re.split(r"\n\s*\n", annotated_text):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        for line in lines:
            if text_styles:
                from reportlab.platypus import Paragraph

                elements.append(Paragraph(styled_paragraph_markup(line, text_styles), body_style))
            else:
                elements.append(paragraph_from_text(line, body_style))
            elements.append(Spacer(1, spacer_height))
    return elements


def build_word_table_elements(
    original_text: str,
    entries: list[RareEntry],
    counts: dict[str, int],
    font_name: str,
    max_example_length: int,
) -> list:
    """Build the rare-word table appended to the PDF."""
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle

    used_entries = [entry for entry in entries if counts.get(entry.term, 0) > 0]
    if not used_entries:
        return []

    title_style = ParagraphStyle("WordTableTitle", fontName=font_name, fontSize=18, leading=24)
    cell_style = ParagraphStyle("WordTableCell", fontName=font_name, fontSize=9, leading=13, wordWrap="CJK")
    data = [[
        paragraph_from_text("字/词", cell_style),
        paragraph_from_text("拼音", cell_style),
        paragraph_from_text("简注", cell_style),
        paragraph_from_text("次数", cell_style),
        paragraph_from_text("原文词例", cell_style),
    ]]
    for entry in sorted(used_entries, key=lambda item: (-counts[item.term], item.term)):
        data.append(
            [
                paragraph_from_text(entry.term, cell_style),
                paragraph_from_text(entry.pinyin, cell_style),
                paragraph_from_text(entry.annotation, cell_style),
                paragraph_from_text(str(counts[entry.term]), cell_style),
                paragraph_from_text(find_sentence_example(original_text, entry.term, max_example_length), cell_style),
            ]
        )

    table = Table(data, colWidths=[50, 65, 145, 35, 160], repeatRows=1, hAlign="LEFT")
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
    return [PageBreak(), Paragraph("阅读词表", title_style), Spacer(1, 8), table]


def build_pdf(
    output_path: Path,
    title: str,
    subtitle: str,
    source_url: str | None,
    original_text: str,
    annotated_text: str,
    entries: list[RareEntry],
    counts: dict[str, int],
    font_name: str,
    font_size: int,
    leading: int,
    include_table: bool,
    max_example_length: int,
    text_styles: list[dict[str, object]] | None = None,
) -> None:
    """Build the annotated PDF."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    except ImportError as error:
        raise RuntimeError(
            "ReportLab is required to create PDF files.\n"
            "Install it with: python3 -m pip install reportlab"
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
        subject=source_url or "",
        author="Generated by liaozhai_tools.py",
    )
    title_style = ParagraphStyle("Title", fontName=font_name, fontSize=22, leading=30, alignment=1, spaceAfter=8)
    subtitle_style = ParagraphStyle("Subtitle", fontName=font_name, fontSize=11, leading=15, alignment=1, spaceAfter=6)
    source_style = ParagraphStyle("Source", fontName=font_name, fontSize=8, leading=11, alignment=1, spaceAfter=16)
    body_style = ParagraphStyle(
        "Body",
        fontName=font_name,
        fontSize=font_size,
        leading=leading,
        firstLineIndent=18,
        wordWrap="CJK",
        spaceAfter=2,
    )
    elements = [
        Paragraph(html.escape(title), title_style),
        Paragraph(html.escape(subtitle), subtitle_style),
    ]
    if source_url:
        elements.append(Paragraph(html.escape(f"原文来源：{source_url}"), source_style))
    elements.append(Spacer(1, 8))
    elements.extend(build_story_elements(annotated_text, body_style, text_styles=text_styles))
    if include_table:
        elements.extend(build_word_table_elements(original_text, entries, counts, font_name, max_example_length))
    doc.build(elements)


def add_common_story_args(parser: argparse.ArgumentParser, default_input: Path, default_dictionary: Path) -> None:
    """Add common input and dictionary arguments."""
    parser.add_argument("input", nargs="?", type=Path, default=default_input, help=f"Input text file. Default: {default_input}")
    parser.add_argument(
        "--dictionary",
        type=Path,
        action="append",
        default=[default_dictionary] if default_dictionary else [],
        help="CSV dictionary with columns: term,pinyin,annotation. Can be repeated.",
    )


def download_main(default_url: str, default_output: Path) -> None:
    """CLI entry point for downloading a story."""
    parser = argparse.ArgumentParser(description="Download readable text from a Liaozhai URL.")
    parser.add_argument("--url", default=default_url, help=f"Page URL. Default: {default_url}")
    parser.add_argument("--output", type=Path, default=default_output, help=f"Output text file. Default: {default_output}")
    parser.add_argument("--section", choices=["all", "original", "translation", "commentary"], default="original")
    parser.add_argument("--debug-output", type=Path, default=None)
    args = parser.parse_args()

    selected_text = download_story(args.url, args.output, args.section, args.debug_output)
    print(f"Downloaded section: {args.section}")
    print(f"Saved to: {args.output}")
    print(f"Characters saved: {len(selected_text)}")


def rare_word_table_main(default_input: Path, default_dictionary: Path, default_output: Path) -> None:
    """CLI entry point for creating a rare-word table."""
    parser = argparse.ArgumentParser(description="Create a rare-word table from a Chinese story text file.")
    add_common_story_args(parser, default_input, default_dictionary)
    parser.add_argument("-o", "--output", type=Path, default=default_output, help=f"Output file. Default: {default_output}")
    parser.add_argument("--max-example-length", type=int, default=36)
    args = parser.parse_args()

    text = normalize_story_text(args.input.read_text(encoding="utf-8"))
    entries = load_entries(args.dictionary)
    rows = found_entries(text, entries, args.max_example_length)
    write_word_table(args.output, rows, args.input)
    print(f"Input file: {args.input}")
    print(f"Output file: {args.output}")
    print(f"Rare entries found: {len(rows)}")


def annotated_pdf_main(
    default_input: Path,
    default_dictionary: Path,
    default_output: Path,
    default_title: str,
    default_source_url: str | None = None,
    default_text_styles_path: Path | None = None,
) -> None:
    """CLI entry point for creating an annotated PDF."""
    parser = argparse.ArgumentParser(description="Generate a pinyin-annotated PDF from a Chinese text file.")
    add_common_story_args(parser, default_input, default_dictionary)
    parser.add_argument("-o", "--output", type=Path, default=default_output, help=f"Output PDF. Default: {default_output}")
    parser.add_argument("--title", default=default_title)
    parser.add_argument("--subtitle", default="精选生僻字与阅读词语")
    parser.add_argument("--source-url", default=default_source_url, help="Original text URL to print in the PDF.")
    parser.add_argument("--font-path", type=Path, default=None)
    parser.add_argument("--use-built-in-cid-font", action="store_true")
    parser.add_argument("--font-name", default="CustomChineseFont")
    parser.add_argument("--font-size", type=int, default=12)
    parser.add_argument("--leading", type=int, default=20)
    parser.add_argument("--annotated-text-output", type=Path, default=None)
    parser.add_argument(
        "--text-styles-json",
        type=Path,
        default=default_text_styles_path,
        help="Optional JSON list of editor text styles to preserve in the PDF.",
    )
    parser.add_argument("--no-table", action="store_true")
    parser.add_argument("--max-example-length", type=int, default=36)
    parser.add_argument(
        "--repeat-annotations",
        action="store_true",
        help="Annotate every occurrence. By default, annotate only the first occurrence of each term.",
    )
    args = parser.parse_args()

    try:
        original_text = normalize_story_text(args.input.read_text(encoding="utf-8"))
        entries = load_entries(args.dictionary)
        if not entries:
            raise ValueError("No dictionary entries available.")
        rows = found_entries(original_text, entries, args.max_example_length)
        active_terms = {str(row["term"]) for row in rows}
        active_entries = [entry for entry in entries if entry.term in active_terms]
        annotated, counts = annotate_text(original_text, active_entries, repeat_annotations=args.repeat_annotations)
        text_styles = []
        if args.text_styles_json is not None and args.text_styles_json.exists():
            import json

            loaded_styles = json.loads(args.text_styles_json.read_text(encoding="utf-8"))
            if not isinstance(loaded_styles, list):
                raise ValueError("Text styles JSON must contain a list.")
            text_styles = loaded_styles
        if args.annotated_text_output is not None:
            args.annotated_text_output.parent.mkdir(parents=True, exist_ok=True)
            args.annotated_text_output.write_text(annotated, encoding="utf-8")

        font_name, font_source = register_pdf_font(args.font_path, args.font_name, args.use_built_in_cid_font)
        bold_registered = register_pdf_bold_variant(args.font_path, font_name)
        build_pdf(
            output_path=args.output,
            title=args.title,
            subtitle=args.subtitle,
            source_url=args.source_url,
            original_text=original_text,
            annotated_text=annotated,
            entries=active_entries,
            counts=counts,
            font_name=font_name,
            font_size=args.font_size,
            leading=args.leading,
            include_table=not args.no_table,
            max_example_length=args.max_example_length,
            text_styles=text_styles,
        )
        print(f"Input text: {args.input}")
        print(f"Output PDF: {args.output}")
        print(f"PDF font source: {font_source}")
        print(f"Annotated rare/new word types: {len(counts)}")
        annotation_total = sum(counts.values()) if args.repeat_annotations else len(counts)
        print(f"Total annotations inserted: {annotation_total}")
        print(f"Editor text styles applied: {len(text_styles)}")
        print(f"True bold font registered: {'yes' if bold_registered else 'no'}")
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
