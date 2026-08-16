#!/usr/bin/env python3
"""Chapter study-material tools for 《翦商》."""

from __future__ import annotations

import argparse
import csv
import html
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


DEFAULT_TEXT_SOURCE_URL = "https://raw.githubusercontent.com/dooshu/shu/main/cn/136.txt"
DEFAULT_WEB_SOURCE_URL = "https://doosho.com/cn/136"
DEFAULT_PDF_NAME = "翦商.pdf"

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

DEFAULT_HEADING_FONT_CANDIDATES = [
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("/System/Library/Fonts/STHeiti Light.ttc"),
    Path("/System/Library/Fonts/Supplemental/Songti.ttc"),
]

SYMBOL_FONT_CANDIDATES = [
    Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
    Path("/Library/Fonts/Arial Unicode.ttf"),
    Path("/System/Library/Fonts/Apple Symbols.ttf"),
]
TRIGRAM_SYMBOL_RE = re.compile(r"([☰☱☲☳☴☵☶☷]+)")
HEXAGRAM_SYMBOL_RE = re.compile(r"[䷀-䷿]")
PDF_LINE_START_FORBIDDEN_RE = re.compile(r"([^\s<>])([，。！？；：、）】》」』”’])")
READING_NOTE_META_RE = re.compile(r"^(状态|记录者|记录日期|处理者|处理日期|关联原文|来源线索)：")
PDF_SYMBOL_FONT_NAME: str | None = None


def load_hexagram_display_map() -> dict[str, str]:
    """Map single hexagram characters to broadly supported trigram pairs."""
    reference_path = Path(__file__).parent / "sources" / "hexagram_reference.tsv"
    if not reference_path.exists():
        return {}
    with reference_path.open(encoding="utf-8", newline="") as handle:
        rows = csv.DictReader(handle, delimiter="\t")
        return {
            row["unicode_hexagram"].strip(): row["display_note"].strip()
            for row in rows
            if row.get("unicode_hexagram") and row.get("display_note")
        }


HEXAGRAM_DISPLAY_MAP = load_hexagram_display_map()

CHAPTER_HEADINGS = [
    ("intro", "引子"),
    ("chapter_01", "第一章 新石器时代的社会升级"),
    ("chapter_02", "第二章 大禹治水真相：稻与龙"),
    ("chapter_03", "第三章 二里头：青铜铸造王权"),
    ("chapter_04", "第四章 异族占领二里头"),
    ("chapter_05", "第五章 商族来源之谜"),
    ("chapter_06", "第六章 早商：仓城奇观"),
    ("chapter_07", "第七章 人祭繁荣与宗教改革运动"),
    ("chapter_08", "第八章 武德沦丧南土：盘龙城"),
    ("chapter_09", "第九章 3300年前的军营：台西"),
    ("chapter_10", "第十章 殷都王室的人祭"),
    ("chapter_11", "第十一章 商人的思维与国家"),
    ("chapter_12", "第十二章 王后的社交圈"),
    ("chapter_13", "第十三章 大学与王子"),
    ("chapter_14", "第十四章 西土拉锯战：老牛坡"),
    ("chapter_15", "第十五章 周族的起源史诗与考古"),
    ("chapter_16", "第十六章 成为商朝爪牙：去周原"),
    ("chapter_17", "第十七章 周文王地窖里的秘密"),
    ("chapter_18", "第十八章 《易经》里的猎俘与献俘"),
    ("chapter_19", "第十九章 羡里牢狱记忆"),
    ("chapter_20", "第二十章 翦商与《易经》的世界观"),
    ("chapter_21", "第二十一章 殷都民间的人祭"),
    ("chapter_22", "第二十二章 纣王的东南战争"),
    ("chapter_23", "第二十三章 姜太公与周方伯"),
    ("chapter_24", "第二十四章 西土之人"),
    ("chapter_25", "第二十五章 牧野鹰扬"),
    ("chapter_26", "第二十六章 周公新时代"),
    ("chapter_27", "第二十七章 诸神远去之后"),
    ("epilogue", "尾声：周公到孔子"),
    ("afterword", "后记"),
]


@dataclass(frozen=True)
class AnnotationEntry:
    """One annotation target."""

    term: str
    pinyin: str
    entry_type: str
    annotation: str


@dataclass(frozen=True)
class SourcePageRange:
    """PDF-viewer, physical source-PDF, and printed page ranges."""

    pdf_start: int
    pdf_end: int
    source_start: int
    source_end: int
    printed_start: int
    printed_end: int


@dataclass(frozen=True)
class AncientReviewEntry:
    """One ancient-text transcription that needs manual review."""

    source: str
    current_text: str
    issue: str
    action: str


@dataclass(frozen=True)
class ReadingNote:
    """One reader-supplied interpretive note."""

    title: str
    paragraphs: tuple[str, ...]


def compact_heading(text: str) -> str:
    """Normalize a heading for robust matching."""
    return re.sub(r"\s+", "", text).replace(":", "：")


def normalize_heading_text(text: str) -> str:
    """Normalize a heading while preserving readable punctuation."""
    normalized = compact_heading(text.strip())
    return normalized.replace("疽北商城", "洹北商城")


def parse_chapter_subtitles(source_text: str) -> dict[str, set[str]]:
    """Parse chapter subtitles from the full web-text table of contents."""
    subtitles: dict[str, set[str]] = {}
    current_chapter: str | None = None
    heading_to_id = {normalize_heading_text(title): chapter_id for chapter_id, title in CHAPTER_HEADINGS}

    for raw_line in source_text.splitlines():
        if not raw_line.startswith("　"):
            if current_chapter is not None:
                break
            continue
        if raw_line.startswith("　　"):
            if current_chapter is not None:
                subtitle = raw_line.strip()
                if subtitle and subtitle != "注释":
                    subtitles.setdefault(current_chapter, set()).add(normalize_heading_text(subtitle))
            continue

        heading = normalize_heading_text(raw_line.strip())
        current_chapter = heading_to_id.get(heading)
        if current_chapter is not None:
            subtitles.setdefault(current_chapter, set())

    return subtitles


def load_chapter_subtitles(chapter_id: str | None, source_path: Path = Path("sources/136.txt")) -> set[str]:
    """Load known subtitles for a chapter from the web-text TOC."""
    if chapter_id is None:
        return set()
    if chapter_id == "intro":
        return {
            normalize_heading_text("殷商最后的人祭"),
            normalize_heading_text("打捞失落的文明"),
            normalize_heading_text("人祭场之外"),
            normalize_heading_text("附录：上古人祭行为的分类"),
        }
    if not source_path.exists():
        fallback_path = Path(__file__).resolve().parent / source_path
        source_path = fallback_path if fallback_path.exists() else source_path
    if not source_path.exists():
        return set()
    return parse_chapter_subtitles(load_text(source_path)).get(chapter_id, set())


def load_chapter_heading(chapter_id: str | None) -> str | None:
    """Return the known chapter title for a chapter id."""
    for known_id, title in CHAPTER_HEADINGS:
        if known_id == chapter_id:
            return title
    return None


def normalize_text(text: str) -> str:
    """Normalize basic web-text whitespace."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = remove_export_page_headers(text)
    text = normalize_punctuation_spacing(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = compact_cjk_spacing(text)
    return text.strip()


def remove_export_page_headers(text: str) -> str:
    """Remove browser-editor export headers from all generated outputs."""
    return re.sub(
        r"=+\s*PDF page \d{3} / printed page \d+\s*=+",
        "",
        text,
    )


def normalize_punctuation_spacing(text: str) -> str:
    """Normalize common CJK punctuation spacing and OCR line-wrap artifacts."""
    protected: dict[str, str] = {}

    def protect(match: re.Match[str]) -> str:
        key = f"@@JIANGSHANG_PROTECTED_{len(protected)}@@"
        protected[key] = match.group(0)
        return key

    text = re.sub(r"\[\[(?:editor-)?fn:\d{1,2}\]\]", protect, text)
    cjk = r"\u3400-\u9fff"
    cjk_or_close = rf"{cjk}A-Za-z0-9）》】」』”’"
    cjk_or_open = rf"{cjk}A-Za-z0-9（《【「『“‘"
    ascii_to_cjk = {
        ",": "，",
        ";": "；",
        ":": "：",
    }
    for ascii_mark, cjk_mark in ascii_to_cjk.items():
        escaped = re.escape(ascii_mark)
        text = re.sub(rf"(?<=[{cjk_or_close}]){escaped}(?=[{cjk_or_open}])", cjk_mark, text)
        text = re.sub(rf"(?<=[{cjk_or_close}]){escaped}(?=[ \t]*[{cjk_or_open}])", cjk_mark, text)
    text = re.sub(rf"(?<=[{cjk_or_close}])[ \t\r\n]+([，。！？；：、）】》」』”’])", r"\1", text)
    text = re.sub(r"([（《【「『“‘])[ \t\r\n]+", r"\1", text)
    text = re.sub(rf"([，。！？；：、])[ \t]+(?=[{cjk_or_open}])", r"\1", text)
    text = re.sub(rf"(?<=[{cjk_or_close}]) [ ]*(?=[，。！？；：、）】》」』”’])", "", text)
    for key, value in protected.items():
        text = text.replace(key, value)
    return text


def compact_cjk_spacing(text: str) -> str:
    """Remove web/PDF line-wrap spaces inside Chinese prose."""
    cjk = r"\u3400-\u9fff"
    cjk_punctuation = r"，。！？；：、“”‘’（）《》"
    text = re.sub(rf"(?<=[{cjk}])[ \t]+(?=[{cjk}])", "", text)
    text = re.sub(rf"(?<=[{cjk}])[ \t]+(?=[A-Za-z0-9])", "", text)
    text = re.sub(rf"(?<=[A-Za-z0-9])[ \t]+(?=[{cjk}])", "", text)
    text = re.sub(rf"(?<=[{cjk_punctuation}])[ \t]+(?=[{cjk}A-Za-z0-9])", "", text)
    text = re.sub(rf"(?<=[{cjk}A-Za-z0-9])[ \t]+(?=[{cjk_punctuation}])", "", text)
    return text


def is_nonreading_line(line: str) -> bool:
    """Return True for source artifacts that make read-aloud choppy."""
    if not line:
        return False
    if re.match(r"^=+\s*PDF page \d{3} / printed page \d+\s*=+$", line):
        return True
    if re.search(r"\[\[fn:\d{1,2}\]\]", line):
        return False
    if "（图）" in line or "(Image)" in line or "(图)" in line:
        return False
    if line.startswith("|") or re.match(r"^\|.*\|$", line):
        return True
    if re.match(r"^表[一二三四五六七八九十\d]+[：:]", line):
        return True
    if re.match(r"^[A-Za-z0-9•·._\-\s]+$", line):
        return True

    caption_words = (
        "图",
        "照片",
        "拓片",
        "平面图",
        "复原图",
        "分布图",
        "方位",
        "占比",
        "出土",
    )
    if len(line) <= 42 and any(word in line for word in caption_words):
        sentence_punctuation = "。！？；"
        if not any(mark in line for mark in sentence_punctuation):
            return True
    return False


def is_image_or_caption_line(line: str) -> bool:
    """Return whether a line appears to be an image placeholder or caption."""
    line = line.strip()
    if not line:
        return False
    if "（图）" in line or "(Image)" in line or "(图)" in line:
        return True
    if re.search(r"[。！？；]", line):
        return False
    caption_words = ("照片", "拓片", "平面图", "复原图", "分布图", "示意图", "剖面图")
    if len(line) <= 56 and any(word in line for word in caption_words):
        return True
    return len(line) <= 30 and line.endswith("图")


def previous_nonblank(lines: list[str], index: int) -> tuple[int, str] | None:
    """Return the previous nonblank line before index."""
    for current in range(index - 1, -1, -1):
        line = lines[current].strip()
        if line:
            return current, line
    return None


def next_nonblank(lines: list[str], index: int) -> tuple[int, str] | None:
    """Return the next nonblank line after index."""
    for current in range(index + 1, len(lines)):
        line = lines[current].strip()
        if line:
            return current, line
    return None


def find_caption_flow_warnings(text: str) -> list[tuple[int, str, str, str]]:
    """Find image/caption lines that appear to split a prose sentence."""
    body, _notes = split_source_notes(text)
    lines = body.splitlines()
    warnings: list[tuple[int, str, str, str]] = []
    sentence_end = "。！？；：”’）》）】]"
    for index, raw_line in enumerate(lines):
        line = raw_line.strip()
        if not is_image_or_caption_line(line):
            continue
        previous = previous_nonblank(lines, index)
        following = next_nonblank(lines, index)
        if not previous or not following:
            continue
        _previous_index, previous_line = previous
        _following_index, following_line = following
        if previous_line.endswith(tuple(sentence_end)):
            continue
        if is_image_or_caption_line(previous_line) or is_image_or_caption_line(following_line):
            continue
        warnings.append((index + 1, previous_line, line, following_line))
    return warnings


def normalize_caption_for_match(text: str) -> str:
    """Normalize caption text for fuzzy presence checks."""
    text = re.sub(r"\[\[fn:\d{1,2}\]\]|\[\d{1,2}\]", "", text)
    text = re.sub(r"[（(](?:图|Image)[）)]", "", text, flags=re.IGNORECASE)
    text = text.replace("箭链", "箭镞").replace("箭镁", "箭镞").replace("箭微", "箭镞")
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[：:，,。；;、·•\-—_()（）《》“”\"'‘’\[\]【】]", "", text)
    return text


def cjk_count(text: str) -> int:
    """Count CJK characters in a string."""
    return len(re.findall(r"[\u3400-\u9fff]", text))


def ascii_letter_count(text: str) -> int:
    """Count ASCII letters in a string."""
    return len(re.findall(r"[A-Za-z]", text))


def caption_confidence(line: str) -> int:
    """Score whether an OCR line is likely to be an image caption."""
    compact = re.sub(r"\s+", "", line.strip())
    if not compact or len(compact) > 64:
        return 0
    if re.fullmatch(r"[\d.\-—_]+", compact):
        return 0

    cjk = cjk_count(compact)
    ascii_letters = ascii_letter_count(compact)
    if cjk < 2:
        return 0
    if ascii_letters > max(8, cjk * 2):
        return 0
    if re.search(r"[。！？；;]", compact):
        return 0

    score = 0
    strong_caption_words = ("平面图", "复原图", "分布图", "示意图", "剖面图")
    caption_words = ("照片", "拓片", "出土", "比例尺", "遗迹", "遗址", "铜", "陶", "墓", "坑")
    if any(word in compact for word in strong_caption_words):
        score += 3
    if "图" in compact:
        score += 2
    if any(word in compact for word in caption_words):
        score += 1
    if re.search(r"[A-Z]{1,4}\d{1,4}", compact):
        score += 1
    if len(compact) <= 36:
        score += 1
    prose_endings = ("了", "的", "是", "有", "和", "与", "而", "但", "将", "在", "为")
    if len(compact) > 28 and compact.endswith(prose_endings):
        score -= 2
    if len(compact) > 36 and "图" not in compact:
        score -= 1
    return max(score, 0)


def likely_ocr_caption(line: str, min_confidence: int = 5) -> bool:
    """Return whether an OCR line looks like an image caption."""
    return caption_confidence(line) >= min_confidence


def extract_ocr_captions_from_pdf(
    pdf_path: Path,
    start_page: int,
    end_page: int,
    dpi: int = 200,
    lang: str = "chi_sim+eng",
    min_confidence: int = 5,
) -> list[tuple[int, str]]:
    """OCR a PDF page range and return likely caption lines."""
    captions: list[tuple[int, str]] = []
    with tempfile.TemporaryDirectory(prefix="jianshang_ocr_") as tmpdir:
        output_prefix = Path(tmpdir) / "page"
        subprocess.run(
            [
                "pdftoppm",
                "-f",
                str(start_page),
                "-l",
                str(end_page),
                "-r",
                str(dpi),
                "-png",
                str(pdf_path),
                str(output_prefix),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        for image_path in sorted(Path(tmpdir).glob("page-*.png")):
            match = re.search(r"-(\d+)\.png$", image_path.name)
            if not match:
                continue
            page_number = int(match.group(1))
            result = subprocess.run(
                ["tesseract", str(image_path), "stdout", "-l", lang, "--psm", "6"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            for raw_line in result.stdout.splitlines():
                line = raw_line.strip()
                if likely_ocr_caption(line, min_confidence=min_confidence):
                    captions.append((page_number, line))
    return captions


def find_missing_ocr_captions(
    clean_text: str,
    captions: list[tuple[int, str]],
) -> list[tuple[int, str]]:
    """Return OCR captions that do not appear to be represented in clean text."""
    clean_normalized = normalize_caption_for_match(clean_text)
    seen: set[str] = set()
    missing: list[tuple[int, str]] = []
    for page_number, caption in captions:
        normalized = normalize_caption_for_match(caption)
        if len(normalized) < 4 or normalized in seen:
            continue
        seen.add(normalized)
        if normalized not in clean_normalized:
            missing.append((page_number, caption))
    return missing


def extract_explicit_footnote_markers(text: str) -> list[int]:
    """Return explicit body footnote markers."""
    body, _notes = split_source_notes(text)
    return [int(number) for number in EXPLICIT_FOOTNOTE_RE.findall(body)]


def extract_source_note_numbers(text: str) -> list[int]:
    """Return parsed source-note numbers."""
    _body, notes = split_source_notes(text)
    numbers: list[int] = []
    for number, content in parse_numbered_source_notes(notes):
        if number.isdigit() and content:
            numbers.append(int(number))
    return numbers


def find_sequence_gaps(numbers: list[int]) -> list[int]:
    """Return missing values inside a numbered sequence."""
    if not numbers:
        return []
    seen = set(numbers)
    return [number for number in range(min(seen), max(seen) + 1) if number not in seen]


def find_suspicious_ocr_tokens(text: str) -> list[tuple[int, str, str]]:
    """Find tokens that often come from PDF/OCR confusion."""
    body, _notes = split_source_notes(text)
    patterns = [
        re.compile(r"\b[A-Z][05]\s*米\b"),
        re.compile(r"\bJ[O0]\s*厘米\b", re.IGNORECASE),
        re.compile(r"\bM[iIl]{1,2}\b"),
        re.compile(r"(?<=[\u4e00-\u9fff])[A-Za-z]{2,}(?=[\u4e00-\u9fff])"),
    ]
    findings: list[tuple[int, str, str]] = []
    for line_number, line in enumerate(body.splitlines(), start=1):
        for pattern in patterns:
            for match in pattern.finditer(line):
                token = match.group(0)
                if token in {"II", "III"} and line[match.end() : match.end() + 2] == "墓区":
                    continue
                findings.append((line_number, match.group(0), line.strip()))
    return findings


def prepare_reading_text(text: str, include_source_notes: bool = False) -> str:
    """Remove captions, tables, and source notes from narrated chapter text."""
    if not include_source_notes:
        text, _source_notes = split_source_notes(text)

    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if is_nonreading_line(line):
            continue
        lines.append(raw_line)

    cleaned = "\n".join(lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def split_source_notes(text: str) -> tuple[str, str]:
    """Split chapter body text from the source note block marked by 注释."""
    body_lines: list[str] = []
    note_lines: list[str] = []
    in_notes = False
    for raw_line in text.splitlines():
        if raw_line.strip() == "注释" and not in_notes:
            in_notes = True
            continue
        if in_notes:
            note_lines.append(raw_line)
        else:
            body_lines.append(raw_line)
    body = "\n".join(body_lines).strip()
    notes = "\n".join(note_lines).strip()
    notes = re.sub(r"\n{3,}", "\n\n", notes)
    return body, notes


def prepare_source_notes(text: str) -> str:
    """Return the chapter source notes without adding them to reading text."""
    _body, notes = split_source_notes(text)
    return notes.strip()


def parse_numbered_source_notes(notes: str) -> list[tuple[str, str]]:
    """Parse source notes into number/content pairs."""
    parsed: list[tuple[str, str]] = []
    current_number: str | None = None
    current_lines: list[str] = []
    expected_number = 1
    for raw_line in notes.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = re.match(r"^(\d{1,2})\s*(.+)$", line)
        if match and int(match.group(1)) == expected_number:
            if current_number is not None:
                parsed.append((current_number, "".join(current_lines).strip()))
            current_number = match.group(1)
            current_lines = [match.group(2).strip()]
            expected_number += 1
            continue
        if current_number is None:
            current_number = ""
        current_lines.append(line)
    if current_number is not None:
        parsed.append((current_number, "".join(current_lines).strip()))
    return parsed


def load_text(path: Path) -> str:
    """Read a UTF-8 text file."""
    if not path.exists():
        raise FileNotFoundError(f"Text file not found: {path}")
    return path.read_text(encoding="utf-8")


def find_heading_matches(text: str, heading: str, start: int = 0) -> list[int]:
    """Find heading positions, allowing optional whitespace inside it."""
    normalized_heading = compact_heading(heading)
    pattern = r"\s*".join(re.escape(char) for char in normalized_heading)
    return [start + match.start() for match in re.finditer(pattern, text[start:])]


def find_heading(text: str, heading: str, start: int = 0) -> int:
    """Find a chapter heading, allowing optional whitespace inside it."""
    matches = find_heading_matches(text, heading, start)
    if not matches:
        raise ValueError(f"Could not find heading: {heading}")
    return matches[0]


def split_chapter(source_text: str, chapter_id: str) -> tuple[str, str]:
    """Extract one chapter by known heading."""
    ids = [item[0] for item in CHAPTER_HEADINGS]
    if chapter_id not in ids:
        raise ValueError(f"Unknown chapter id: {chapter_id}")

    index = ids.index(chapter_id)
    title = CHAPTER_HEADINGS[index][1]

    if chapter_id == "intro":
        intro_start_marker = "2022年8月8日 于京西门头沟"
        marker_index = source_text.find(intro_start_marker)
        if marker_index == -1:
            raise ValueError(f"Could not find intro start marker: {intro_start_marker}")
        start = marker_index + len(intro_start_marker)
        end = find_heading(source_text, CHAPTER_HEADINGS[index + 1][1], start)
        return title, f"{title}\n\n{source_text[start:end].strip()}"

    final_section_markers = {
        "epilogue": (
            "自五千年前的仰韶文化晚期以来",
            "这本书的内容，也许会让人觉得有些陌生",
        ),
        "afterword": (
            "这本书的内容，也许会让人觉得有些陌生",
            "始于一页，抵达世界",
        ),
    }
    if chapter_id in final_section_markers:
        start_marker, end_marker = final_section_markers[chapter_id]
        start = source_text.find(start_marker)
        end = source_text.find(end_marker, start + len(start_marker))
        if start == -1 or end == -1:
            raise ValueError(f"Could not locate final section markers for {chapter_id}")
        return title, f"{title}\n\n{normalize_text(source_text[start:end]).strip()}"

    # The web text begins with a generated table of contents, which contains
    # every chapter title once before the actual book body. Prefer the first
    # occurrence after that front matter.
    body_start_hint = source_text.find("本书是关于中国上古时代")
    if body_start_hint == -1:
        body_start_hint = 0

    title_matches = find_heading_matches(source_text, title)
    body_matches = [position for position in title_matches if position >= body_start_hint]
    if not body_matches:
        raise ValueError(f"Could not find body heading: {title}")
    start = body_matches[0]

    if index + 1 < len(CHAPTER_HEADINGS):
        next_title = CHAPTER_HEADINGS[index + 1][1]
        end = find_heading(source_text, next_title, start + 1)
    else:
        end = len(source_text)

    return title, normalize_text(source_text[start:end])


def load_entries(path: Path) -> list[AnnotationEntry]:
    """Load a typed annotation CSV."""
    if not path.exists():
        raise FileNotFoundError(f"Annotation CSV not found: {path}")

    entries = []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"term", "pinyin", "type", "annotation"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path} is missing column(s): {', '.join(sorted(missing))}")

        for row_number, row in enumerate(reader, start=2):
            term = (row.get("term") or "").strip()
            pinyin = (row.get("pinyin") or "").strip()
            entry_type = (row.get("type") or "").strip()
            annotation = (row.get("annotation") or "").strip()
            if not term:
                continue
            if not pinyin or not entry_type or not annotation:
                raise ValueError(f"Incomplete entry in {path}:{row_number}")
            entries.append(AnnotationEntry(term, pinyin, entry_type, annotation))

    merged = {entry.term: entry for entry in entries}
    return sorted(merged.values(), key=lambda item: (-len(item.term), item.term))


def count_terms(text: str, entries: list[AnnotationEntry]) -> dict[str, int]:
    """Count all dictionary terms in the text."""
    return {entry.term: text.count(entry.term) for entry in entries if text.count(entry.term)}


def annotate_text(
    text: str,
    entries: list[AnnotationEntry],
    repeat_annotations: bool = False,
    skip_headings: set[str] | None = None,
    already_annotated: set[str] | None = None,
) -> tuple[str, dict[str, int]]:
    """Annotate text by longest match."""
    if skip_headings:
        annotated_blocks: list[str] = []
        total_counts: dict[str, int] = {}
        shared_annotated = already_annotated if already_annotated is not None else set()
        for block in re.split(r"(\n\s*\n)", text):
            if re.fullmatch(r"\n\s*\n", block):
                annotated_blocks.append(block)
                continue
            lines = [line.strip() for line in block.splitlines() if line.strip()]
            block_text = "".join(lines)
            if normalize_heading_text(block_text) in skip_headings:
                annotated_blocks.append(block)
                continue
            annotated_block, block_counts = annotate_text(
                block,
                entries,
                repeat_annotations=repeat_annotations,
                skip_headings=None,
                already_annotated=shared_annotated,
            )
            annotated_blocks.append(annotated_block)
            for term, count in block_counts.items():
                total_counts[term] = total_counts.get(term, 0) + count
        return "".join(annotated_blocks), total_counts

    by_first_char: dict[str, list[AnnotationEntry]] = {}
    for entry in entries:
        by_first_char.setdefault(entry.term[0], []).append(entry)
    for candidates in by_first_char.values():
        candidates.sort(key=lambda item: (-len(item.term), item.term))

    result = []
    counts: dict[str, int] = {}
    already_annotated = already_annotated if already_annotated is not None else set()
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

        if source_already_has_annotation(text, index, matched):
            result.append(matched.term)
            already_annotated.add(matched.term)
        elif repeat_annotations or matched.term not in already_annotated:
            result.append(f"{matched.term}（{matched.pinyin}）")
            counts[matched.term] = counts.get(matched.term, 0) + 1
            already_annotated.add(matched.term)
        else:
            result.append(matched.term)
        index += len(matched.term)
    return "".join(result), counts


def source_already_has_annotation(text: str, index: int, entry: AnnotationEntry) -> bool:
    """Return True when the source already writes term plus pinyin in parentheses."""
    suffix = text[index + len(entry.term) :]
    compact_pinyin = re.sub(r"\s+", "", entry.pinyin).lower()
    if not compact_pinyin or not suffix.startswith(("（", "(")):
        return False

    close_char = "）" if suffix.startswith("（") else ")"
    close_index = suffix.find(close_char)
    if close_index == -1:
        return False

    parenthetical = re.sub(r"\s+", "", suffix[1:close_index]).lower()
    if parenthetical == compact_pinyin:
        return True

    # Treat tone-number spellings such as ``yu2`` and ``tao2`` as existing
    # pinyin too. This prevents a normalized dictionary reading from producing
    # duplicates such as ``邘（yú）（yu2）``.
    return bool(
        re.fullmatch(r"[a-züv:]+[1-5](?:['’·-]?[a-züv:]+[1-5])*", parenthetical)
    )


def find_example(text: str, term: str, max_length: int = 42) -> str:
    """Find a short source example."""
    index = text.find(term)
    if index < 0:
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
    def compact_example(value: str) -> str:
        value = re.sub(r"\s+", "", value.strip())
        value = EXPLICIT_FOOTNOTE_RE.sub(r"[\1] ", value)
        value = re.sub(r"\s+([,，。！？；：、）)”》])", r"\1", value)
        return re.sub(r"([,，])(?=[\u4e00-\u9fff])", r"\1 ", value).strip()

    example = compact_example(text[start:end])
    if len(example) <= max_length:
        return example

    snippet_start = max(0, index - max_length // 2)
    snippet_end = min(len(text), snippet_start + max_length)
    snippet = compact_example(text[snippet_start:snippet_end])
    if snippet_start > 0:
        snippet = "..." + snippet
    if snippet_end < len(text):
        snippet += "..."
    return snippet


TERM_TYPE_PRIORITY = {
    # Reader/editor-requested entries should be easy to find in capped tables,
    # rather than being retained but sorted onto the final vocabulary page.
    "manual": -1,
    "forced": -1,
    "keep": -1,
    "person": 0,
    "person_or_deity": 0,
    "place": 1,
    "place_or_group": 1,
    "site_or_culture": 1,
    "text": 2,
    "added": 2,
    "rare_word": 3,
    "idiom": 3,
    "artifact": 4,
    "bronze_item": 4,
    "concept": 5,
}


def term_type_priority(entry_type: str) -> int:
    """Return a stable display priority for vocabulary types."""
    return TERM_TYPE_PRIORITY.get(entry_type, 9)


def is_forced_term_type(entry_type: str) -> bool:
    """Return whether a term type should be kept even past table caps."""
    normalized = entry_type.strip().lower()
    return normalized in {"added", "manual", "forced", "keep"}


def limit_rows(rows: list[dict[str, str | int]], max_terms: int | None) -> list[dict[str, str | int]]:
    """Limit term rows to the highest-signal entries."""
    if max_terms is None or max_terms <= 0 or len(rows) <= max_terms:
        return rows
    forced_terms = {str(row["term"]) for row in rows if is_forced_term_type(str(row["type"]))}
    normal_rows = [row for row in rows if str(row["term"]) not in forced_terms]
    normal_cap = max(0, max_terms - len(forced_terms))
    ranked = sorted(
        normal_rows,
        key=lambda row: (
            -int(row["count"]),
            term_type_priority(str(row["type"])),
            int(row["position"]),
            str(row["term"]),
        ),
    )
    limited_terms = forced_terms | {str(row["term"]) for row in ranked[:normal_cap]}
    return [row for row in rows if str(row["term"]) in limited_terms]


def max_terms_from_text_length(text: str, max_terms_percent: float | None, min_terms: int) -> int | None:
    """Calculate an optional term cap from source text length."""
    if max_terms_percent is None:
        return None
    if max_terms_percent <= 0:
        raise ValueError("--max-terms-percent must be greater than 0")
    readable_length = len(re.sub(r"\s+", "", text))
    return max(min_terms, round(readable_length * max_terms_percent / 100))


def effective_max_terms(
    text: str,
    max_terms: int | None,
    max_terms_percent: float | None,
    min_terms: int,
) -> int | None:
    """Resolve fixed and percentage-based term caps."""
    percent_cap = max_terms_from_text_length(text, max_terms_percent, min_terms)
    caps = [cap for cap in (max_terms, percent_cap) if cap is not None and cap > 0]
    return min(caps) if caps else None


def sort_entries_for_table(
    entries: list[AnnotationEntry],
    counts: dict[str, int],
    original_text: str,
    max_terms: int | None = None,
) -> list[AnnotationEntry]:
    """Sort and optionally limit entries for vocabulary tables."""
    used_entries = [entry for entry in entries if counts.get(entry.term, 0)]
    used_entries.sort(
        key=lambda entry: (
            -counts[entry.term],
            term_type_priority(entry.entry_type),
            original_text.find(entry.term),
            entry.term,
        )
    )
    if max_terms is not None and max_terms > 0:
        forced_entries = [entry for entry in used_entries if is_forced_term_type(entry.entry_type)]
        forced_terms = {entry.term for entry in forced_entries}
        normal_entries = [entry for entry in used_entries if entry.term not in forced_terms]
        normal_cap = max(0, max_terms - len(forced_entries))
        used_entries = normal_entries[:normal_cap] + forced_entries
        used_entries.sort(
            key=lambda entry: (
                -counts[entry.term],
                term_type_priority(entry.entry_type),
                original_text.find(entry.term),
                entry.term,
            )
        )
    return used_entries


def found_rows(text: str, entries: list[AnnotationEntry], max_example_length: int) -> list[dict[str, str | int]]:
    """Return annotation entries found in the text."""
    rows = []
    for entry in entries:
        count = text.count(entry.term)
        if count == 0:
            continue
        rows.append(
            {
                "term": entry.term,
                "pinyin": entry.pinyin,
                "type": entry.entry_type,
                "annotation": entry.annotation,
                "count": count,
                "context": find_example(text, entry.term, max_example_length),
                "position": text.find(entry.term),
            }
        )
    rows.sort(key=lambda row: int(row["position"]))
    return rows


def write_table(output_path: Path, rows: list[dict[str, str | int]], source_path: Path) -> None:
    """Write the annotation table as tab-separated text."""
    lines = [
        "阅读词表",
        f"来源文件：{source_path}",
        f"检出条目数：{len(rows)}",
        "",
        "序号\t字/词\t拼音\t类型\t简注\t出现次数\t原文词例",
    ]
    for number, row in enumerate(rows, start=1):
        lines.append(
            "\t".join(
                [
                    str(number),
                    str(row["term"]),
                    str(row["pinyin"]),
                    str(row["type"]),
                    str(row["annotation"]),
                    str(row["count"]),
                    str(row["context"]),
                ]
            )
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def find_default_font_path() -> Path | None:
    """Return the first available Chinese-capable font."""
    for candidate in DEFAULT_FONT_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


def find_default_heading_font_path() -> Path | None:
    """Return the first available heavier Chinese-capable font."""
    for candidate in DEFAULT_HEADING_FONT_CANDIDATES:
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


def register_songti_bold_font(font_name: str) -> str | None:
    """Register the Simplified Chinese Songti bold face for section headings."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    songti_path = Path("/System/Library/Fonts/Supplemental/Songti.ttc")
    if not songti_path.exists():
        return None
    try:
        pdfmetrics.registerFont(TTFont(font_name, str(songti_path), subfontIndex=1))
    except Exception:
        return None
    return font_name


def register_symbol_font(font_name: str) -> str | None:
    """Register a symbol font for trigram glyphs if one is available."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    for font_path in SYMBOL_FONT_CANDIDATES:
        if not font_path.exists():
            continue
        try:
            pdfmetrics.registerFont(TTFont(font_name, str(font_path), subfontIndex=0))
            return font_name
        except Exception:
            continue
    return None


def register_pdf_fonts(font_path: Path | None, font_name: str) -> tuple[str, str, str]:
    """Register a font for ReportLab."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    from reportlab.pdfbase.ttfonts import TTFont

    if font_path is not None:
        pdfmetrics.registerFont(TTFont(font_name, str(font_path), subfontIndex=default_subfont_index(font_path)))
        return font_name, font_name, str(font_path)

    auto_font_path = find_default_font_path()
    if auto_font_path is not None:
        try:
            pdfmetrics.registerFont(TTFont(font_name, str(auto_font_path), subfontIndex=default_subfont_index(auto_font_path)))
            heading_font_name = f"{font_name}-Heading"
            heading_font_path = find_default_heading_font_path()
            if heading_font_path is not None:
                try:
                    pdfmetrics.registerFont(TTFont(heading_font_name, str(heading_font_path), subfontIndex=default_subfont_index(heading_font_path)))
                    return font_name, heading_font_name, (
                        f"{auto_font_path}; headings: {heading_font_path}"
                    )
                except Exception:
                    pass
            return font_name, font_name, str(auto_font_path)
        except Exception:
            pass

    default_font = "STSong-Light"
    pdfmetrics.registerFont(UnicodeCIDFont(default_font))
    return default_font, default_font, "ReportLab built-in STSong-Light"


EXPLICIT_FOOTNOTE_RE = re.compile(r"\[\[fn:(\d{1,2})\]\]")
EDITOR_FOOTNOTE_RE = re.compile(r"\[\[editor-fn:(\d{1,2})\]\]")
USER_NOTE_MARKER_RE = re.compile(r"\[\[user-note:(\d{1,3})\]\]")
FOOTNOTE_MARKER_RE = re.compile(
    r"(?<=[。！？；，、）)”》])"
    r"(\d{1,2})"
    r"(?![号枚字只座具件人米厘年层轮名条块处个])"
    r"(?=($|\s|[\u4e00-\u9fff《“]))"
)
INLINE_REVIEW_NOTE_RE = re.compile(r"(〔(?:待核|校疑：[^〕]+|按语：[^〕]+|札记：[^〕]+)〕)")
USER_NOTE_RE = re.compile(r"〔札记：(.*?)〕", re.S)
READING_NOTE_SOURCE_PREFIX = "::source::"
URL_RE = re.compile(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&'*+,;=%-]+")


def extract_editor_notes(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Remove editor-note definitions and return them in numeric order."""
    notes: dict[str, str] = {}
    kept_lines: list[str] = []
    for raw_line in text.splitlines():
        match = re.match(r"^\s*〔编者注(\d{1,2})〕\s*(.*)$", raw_line)
        if match:
            notes[match.group(1)] = match.group(2).strip()
            continue
        kept_lines.append(raw_line)
    cleaned = "\n".join(kept_lines)
    return cleaned, sorted(notes.items(), key=lambda item: int(item[0]))


def extract_user_notes(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Replace inline user notes with numbered markers and return their contents."""
    notes: list[tuple[str, str]] = []

    def replace(match: re.Match[str]) -> str:
        number = str(len(notes) + 1)
        notes.append((number, match.group(1).strip()))
        return f"[[user-note:{number}]]"

    return USER_NOTE_RE.sub(replace, text), notes


def escape_paragraph_text(text: str, render_footnotes: bool = False) -> str:
    """Escape paragraph text, optionally styling prose notes and footnote markers."""
    escaped = html.escape(text)
    escaped = HEXAGRAM_SYMBOL_RE.sub(
        lambda match: HEXAGRAM_DISPLAY_MAP.get(match.group(0), match.group(0)),
        escaped,
    )
    escaped = URL_RE.sub(
        lambda match: f'<link href="{match.group(0)}" color="#1A5FB4">{match.group(0)}</link>',
        escaped,
    )
    if PDF_SYMBOL_FONT_NAME:
        escaped = TRIGRAM_SYMBOL_RE.sub(
            rf'<font name="{PDF_SYMBOL_FONT_NAME}">\1</font>',
            escaped,
        )
    if not render_footnotes:
        return keep_pdf_punctuation_together(escaped)
    escaped = EXPLICIT_FOOTNOTE_RE.sub(r"<super>[\1]</super>", escaped)
    escaped = EDITOR_FOOTNOTE_RE.sub(r"<super>[编\1]</super>", escaped)
    escaped = USER_NOTE_MARKER_RE.sub(r"<super>[札\1]</super>", escaped)
    escaped = FOOTNOTE_MARKER_RE.sub(r"<super>[\1]</super>", escaped)
    escaped = INLINE_REVIEW_NOTE_RE.sub(r'<font size="8" color="#666666">\1</font>', escaped)
    return keep_pdf_punctuation_together(escaped)


def keep_pdf_punctuation_together(escaped_text: str) -> str:
    """Discourage PDF line breaks before closing Chinese punctuation."""
    return PDF_LINE_START_FORBIDDEN_RE.sub(r"<nobr>\1\2</nobr>", escaped_text)


def paragraph_from_text(text: str, style, render_footnotes: bool = False):
    """Create a paragraph from plain text."""
    from reportlab.platypus import Paragraph

    return Paragraph(escape_paragraph_text(text, render_footnotes), style)


def is_section_heading(text: str) -> bool:
    """Return whether a short block should be styled as a section heading."""
    compact = text.strip()
    if not compact or len(compact) > 18:
        return False
    if re.search(r"[。！？；：,.，、()（）]", compact):
        return False
    if re.search(r"\d", compact):
        return False
    return True


def format_chapter_title(text: str) -> str:
    """Add book-like spacing between the chapter number and title."""
    compact = text.strip()
    match = re.fullmatch(r"(第[一二三四五六七八九十百]+章)(.+)", compact)
    if match:
        return f"{match.group(1)}　　{match.group(2).strip()}"
    return compact


def chapter_id_from_path(path: Path) -> str | None:
    """Infer a chapter id like chapter_03 from an input or output path."""
    for part in path.parts:
        if part in {"intro", "epilogue", "afterword"}:
            return part
        if re.fullmatch(r"chapter_\d{2}", part):
            return part
    return None


def load_source_page_range(chapter_map: Path, chapter_id: str | None) -> SourcePageRange | None:
    """Load original source page mapping for a chapter."""
    if chapter_id is None:
        return None
    if not chapter_map.exists():
        fallback_map = Path(__file__).resolve().parent / chapter_map
        if fallback_map.exists():
            chapter_map = fallback_map
        else:
            return None

    with chapter_map.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            if row.get("chapter") != chapter_id:
                continue
            try:
                return SourcePageRange(
                    pdf_start=int(row["pdf_page_start"]),
                    pdf_end=int(row["pdf_page_end"]),
                    source_start=int(row.get("source_page_start") or row["pdf_page_start"]),
                    source_end=int(row.get("source_page_end") or row["pdf_page_end"]),
                    printed_start=int(row["printed_page_start"]),
                    printed_end=int(row["printed_page_end"]),
                )
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(f"Invalid page mapping for {chapter_id}: {chapter_map}") from error
    return None


def manual_source_page_range(args: argparse.Namespace) -> SourcePageRange | None:
    """Return a complete manual source-page override, if one was supplied."""
    values = (
        args.pdf_page_start,
        args.pdf_page_end,
        args.printed_page_start,
        args.printed_page_end,
    )
    if not any(value is not None for value in values):
        return None
    if not all(value is not None for value in values):
        raise ValueError(
            "Manual page overrides require --pdf-page-start, --pdf-page-end, "
            "--printed-page-start, and --printed-page-end."
        )
    return SourcePageRange(
        pdf_start=args.pdf_page_start,
        pdf_end=args.pdf_page_end,
        source_start=args.pdf_page_start,
        source_end=args.pdf_page_end,
        printed_start=args.printed_page_start,
        printed_end=args.printed_page_end,
    )


def page_in_range(start: int, end: int, fraction: float) -> int:
    """Pick a 1-based source page within an inclusive page range."""
    if end <= start:
        return start
    fraction = min(max(fraction, 0.0), 1.0)
    return start + round((end - start) * fraction)


def source_page_position(page_range: SourcePageRange | None, fraction: float) -> tuple[int, int] | None:
    """Return the physical source-PDF and printed page for a source position."""
    if page_range is None:
        return None
    pdf_page = page_in_range(page_range.source_start, page_range.source_end, fraction)
    printed_page = page_in_range(page_range.printed_start, page_range.printed_end, fraction)
    return pdf_page, printed_page


def build_term_table_elements(
    original_text: str,
    entries: list[AnnotationEntry],
    counts: dict[str, int],
    font_name: str,
    max_example_length: int,
    table_title: str = "阅读词表",
    max_terms: int | None = None,
) -> list:
    """Build the term table for the PDF."""
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle

    used_entries = sort_entries_for_table(entries, counts, original_text, max_terms)
    if not used_entries:
        return []

    title_style = ParagraphStyle("TermTableTitle", fontName=font_name, fontSize=16, leading=22)
    cell_style = ParagraphStyle("TermTableCell", fontName=font_name, fontSize=8.5, leading=12, wordWrap="CJK")
    data = [[
        paragraph_from_text("字/词", cell_style),
        paragraph_from_text("拼音", cell_style),
        paragraph_from_text("类型", cell_style),
        paragraph_from_text("简注", cell_style),
        paragraph_from_text("次数", cell_style),
        paragraph_from_text("原文词例", cell_style),
    ]]
    for entry in used_entries:
        data.append(
            [
                paragraph_from_text(entry.term, cell_style),
                paragraph_from_text(entry.pinyin, cell_style),
                paragraph_from_text(entry.entry_type, cell_style),
                paragraph_from_text(entry.annotation, cell_style),
                paragraph_from_text(str(counts[entry.term]), cell_style),
                paragraph_from_text(find_example(original_text, entry.term, max_example_length), cell_style),
            ]
        )

    table = Table(data, colWidths=[45, 58, 62, 130, 32, 128], repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.grey),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return [PageBreak(), Paragraph(table_title, title_style), Spacer(1, 8), table]


def load_ancient_review_entries(path: Path | None) -> list[AncientReviewEntry]:
    """Load ancient/oracle text review rows from a TSV file."""
    if path is None:
        return []
    rows: list[AncientReviewEntry] = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        required = {"source", "current_text", "issue", "action"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise ValueError(f"{path} is missing required column(s): {missing_list}")
        for row in reader:
            source = (row.get("source") or "").strip()
            current_text = (row.get("current_text") or "").strip()
            issue = (row.get("issue") or "").strip()
            action = (row.get("action") or "").strip()
            if source or current_text or issue or action:
                rows.append(AncientReviewEntry(source, current_text, issue, action))
    return rows


def build_ancient_review_table_elements(
    entries: list[AncientReviewEntry],
    font_name: str,
) -> list:
    """Build a PDF table for difficult ancient/oracle transcriptions."""
    if not entries:
        return []

    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle

    title_style = ParagraphStyle("AncientReviewTitle", fontName=font_name, fontSize=16, leading=22)
    note_style = ParagraphStyle(
        "AncientReviewNote",
        fontName=font_name,
        fontSize=8.2,
        leading=11.5,
        textColor="#555555",
        wordWrap="CJK",
    )
    cell_style = ParagraphStyle("AncientReviewCell", fontName=font_name, fontSize=8.5, leading=12, wordWrap="CJK")
    data = [[
        paragraph_from_text("来源/位置", cell_style),
        paragraph_from_text("当前处理", cell_style),
        paragraph_from_text("问题", cell_style),
        paragraph_from_text("后续动作", cell_style),
    ]]
    for entry in entries:
        data.append(
            [
                paragraph_from_text(entry.source, cell_style),
                paragraph_from_text(entry.current_text, cell_style),
                paragraph_from_text(entry.issue, cell_style),
                paragraph_from_text(entry.action, cell_style),
            ]
        )

    table = Table(data, colWidths=[86, 142, 118, 110], repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.grey),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    note = "说明：本表用于保留甲骨文字形、残字、释读或 OCR 无法可靠确定的古文字文本；需要人工据原版图或专业释文校读。"
    return [
        PageBreak(),
        Paragraph("疑难甲骨文字词校读表", title_style),
        Spacer(1, 6),
        paragraph_from_text(note, note_style),
        Spacer(1, 8),
        table,
    ]


def load_reading_notes(path: Path | None) -> list[ReadingNote]:
    """Load reader notes from a small Markdown file."""
    if path is None:
        return []
    text = re.sub(r"<!--.*?-->", "", load_text(path), flags=re.DOTALL).strip()
    if not text:
        return []

    notes: list[ReadingNote] = []
    current_title = ""
    current_paragraphs: list[str] = []

    def flush_note() -> None:
        nonlocal current_title, current_paragraphs
        if current_title or current_paragraphs:
            title = current_title.strip() or "读书札记"
            paragraphs = tuple(paragraph.strip() for paragraph in current_paragraphs if paragraph.strip())
            if paragraphs:
                notes.append(ReadingNote(title, paragraphs))
        current_title = ""
        current_paragraphs = []

    for raw_block in re.split(r"\n\s*\n", text):
        block = raw_block.strip()
        if not block:
            continue
        if block.startswith("# "):
            continue
        if block.startswith("## "):
            flush_note()
            lines = block.splitlines()
            current_title = lines[0].removeprefix("## ").strip()
            remainder = "\n".join(line.strip() for line in lines[1:] if line.strip())
            if remainder:
                current_paragraphs.append(remainder)
            continue
        if block.startswith("### "):
            lines = block.splitlines()
            subheading = lines[0].removeprefix("### ").strip()
            if subheading:
                current_paragraphs.append(f"{READING_NOTE_SOURCE_PREFIX}{subheading}")
            remainder = "".join(line.strip() for line in lines[1:] if line.strip())
            if remainder:
                current_paragraphs.append(remainder)
            continue
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if lines and all(READING_NOTE_META_RE.match(line) for line in lines):
            current_paragraphs.extend(lines)
        else:
            current_paragraphs.append("".join(lines))

    flush_note()
    return notes


def build_reading_notes_elements(
    notes: list[ReadingNote],
    font_name: str,
    heading_font_name: str,
) -> list:
    """Build a PDF section for reader-supplied interpretive notes."""
    if not notes:
        return []

    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle

    title_style = ParagraphStyle("ReadingNotesTitle", fontName=font_name, fontSize=16, leading=22)
    note_title_style = ParagraphStyle(
        "ReadingNoteTitle",
        fontName=heading_font_name,
        fontSize=11.5,
        leading=16,
        wordWrap="CJK",
        spaceAfter=3,
    )
    comment_label_style = ParagraphStyle(
        "ReadingNoteCommentLabel",
        fontName=font_name,
        fontSize=7.6,
        leading=10,
        textColor="#666666",
        wordWrap="CJK",
    )
    body_style = ParagraphStyle(
        "ReadingNoteBody",
        fontName=font_name,
        fontSize=9.8,
        leading=14.5,
        firstLineIndent=0,
        wordWrap="CJK",
        spaceAfter=4,
    )
    subtopic_style = ParagraphStyle(
        "ReadingNoteSubtopic",
        fontName=heading_font_name,
        fontSize=10.2,
        leading=14,
        textColor="#333333",
        wordWrap="CJK",
        spaceBefore=2,
        spaceAfter=2,
    )
    meta_style = ParagraphStyle(
        "ReadingNoteMeta",
        fontName=font_name,
        fontSize=7.8,
        leading=10.5,
        firstLineIndent=0,
        textColor="#555555",
        wordWrap="CJK",
    )
    intro_style = ParagraphStyle(
        "ReadingNotesIntro",
        fontName=font_name,
        fontSize=8.5,
        leading=12,
        textColor="#555555",
        wordWrap="CJK",
    )

    elements: list = [
        PageBreak(),
        Paragraph("读书札记", title_style),
        Spacer(1, 6),
        paragraph_from_text("说明：本节收录读者个人理解、联想和待考资料线索，不作为原文校勘或作者原注。", intro_style),
        Spacer(1, 10),
    ]
    for note in notes:
        block_rows = [[paragraph_from_text(note.title, note_title_style)]]
        source_row_indexes: list[int] = []
        meta_lines = []
        needs_comment_label = True
        for paragraph in note.paragraphs:
            if READING_NOTE_META_RE.match(paragraph):
                meta_lines.append(paragraph.rstrip("。"))
                continue
            if paragraph.startswith(READING_NOTE_SOURCE_PREFIX):
                source_text = paragraph.removeprefix(READING_NOTE_SOURCE_PREFIX)
                source_row_indexes.append(len(block_rows))
                block_rows.append([paragraph_from_text(source_text, subtopic_style)])
                needs_comment_label = True
                continue
            if needs_comment_label:
                block_rows.append([paragraph_from_text("读者按", comment_label_style)])
                needs_comment_label = False
            block_rows.append([paragraph_from_text(paragraph, body_style)])
        if meta_lines:
            block_rows.append([paragraph_from_text("；".join(meta_lines) + "。", meta_style)])
        table = Table(block_rows, colWidths=[430], hAlign="LEFT")
        table_styles = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]
        for row_index in source_row_indexes:
            table_styles.append(("BACKGROUND", (0, row_index), (-1, row_index), colors.HexColor("#F7F7F7")))
        table.setStyle(
            TableStyle(table_styles)
        )
        elements.append(table)
        elements.append(Spacer(1, 8))
    return elements


def build_pdf(
    output_path: Path,
    title: str,
    subtitle: str,
    source_note: str,
    original_text: str,
    annotated_text: str,
    entries: list[AnnotationEntry],
    counts: dict[str, int],
    bronze_entries: list[AnnotationEntry],
    bronze_counts: dict[str, int],
    ancient_review_entries: list[AncientReviewEntry],
    reading_notes: list[ReadingNote],
    font_path: Path | None,
    max_example_length: int,
    source_page_range: SourcePageRange | None,
    section_headings: set[str],
    max_terms: int | None,
    source_notes: str = "",
    editor_notes: list[tuple[str, str]] | None = None,
    user_notes: list[tuple[str, str]] | None = None,
) -> tuple[str, str]:
    """Build an annotated PDF."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Flowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    class SourcePageMarker(Flowable):
        """Attach an original source-page label to the generated PDF page."""

        def __init__(self, marker: tuple[int, int] | str | None):
            super().__init__()
            self.marker = marker

        def wrap(self, _available_width, _available_height):
            return 0, 0

        def draw(self):
            if isinstance(self.marker, tuple):
                self.canv._source_page_label = None
                self.canv._source_page_last_position = self.marker
                positions = getattr(self.canv, "_source_page_positions", [])
                positions.append(self.marker)
                self.canv._source_page_positions = positions
            else:
                self.canv._source_page_label = self.marker
                self.canv._source_page_positions = []

    class FooterCanvas(canvas.Canvas):
        """Canvas that prints annotated, source-PDF, and print page identities."""

        def showPage(self):
            self.draw_footer()
            super().showPage()
            self._source_page_positions = []

        def draw_footer(self):
            section_label = getattr(self, "_source_page_label", None)
            positions = getattr(self, "_source_page_positions", [])
            if not section_label and not positions:
                last_position = getattr(self, "_source_page_last_position", None)
                if last_position:
                    positions = [last_position]
            source_label = None
            printed_label = None
            if not section_label and positions:
                pdf_pages = [position[0] for position in positions]
                printed_pages = [position[1] for position in positions]
                source_label = self.format_page_range(min(pdf_pages), max(pdf_pages))
                printed_label = self.format_page_range(min(printed_pages), max(printed_pages))
            width, _height = self._pagesize
            self.saveState()
            self.setFont(font_name, 7.5)
            self.setFillGray(0.35)
            self.drawString(20 * mm, 8 * mm, f"注音 PDF 第 {self.getPageNumber()} 页")
            if source_label is not None:
                self.drawCentredString(width / 2, 8 * mm, f"源 PDF 第 {source_label} 页")
            elif section_label:
                self.drawCentredString(width / 2, 8 * mm, f"内容：{section_label}")
            if printed_label is not None:
                self.drawRightString(width - 20 * mm, 8 * mm, f"印刷第 {printed_label} 页")
            self.restoreState()

        @staticmethod
        def format_page_range(start: int, end: int) -> str:
            if start == end:
                return str(start)
            return f"{start}-{end}"

    global PDF_SYMBOL_FONT_NAME
    font_name, heading_font_name, font_source = register_pdf_fonts(font_path, "JianshangChineseFont")
    section_heading_font_name = register_songti_bold_font(f"{font_name}-SectionHeading") or heading_font_name
    PDF_SYMBOL_FONT_NAME = register_symbol_font(f"{font_name}-Symbols")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=title,
        subject=source_note,
        author="Generated by jianshang_tools.py",
    )

    chapter_title_style = ParagraphStyle(
        "ChapterTitle",
        fontName=heading_font_name,
        fontSize=17,
        leading=24,
        alignment=1,
        wordWrap="CJK",
    )
    title_annotation_style = ParagraphStyle(
        "TitleAnnotation",
        fontName=font_name,
        fontSize=7.5,
        leading=10.5,
        alignment=0,
        textColor="#666666",
        wordWrap="CJK",
        spaceBefore=12,
        spaceAfter=12,
    )
    notes_title_style = ParagraphStyle("SourceNotesTitle", fontName=font_name, fontSize=16, leading=22)
    notes_body_style = ParagraphStyle(
        "SourceNotesBody",
        fontName=font_name,
        fontSize=9.5,
        leading=14.5,
        firstLineIndent=0,
        wordWrap="CJK",
        spaceAfter=4,
    )
    notes_number_style = ParagraphStyle(
        "SourceNotesNumber",
        fontName=font_name,
        fontSize=9.5,
        leading=14.5,
        alignment=2,
    )
    section_heading_style = ParagraphStyle(
        "SectionHeading",
        fontName=section_heading_font_name,
        fontSize=13,
        leading=19,
        leftIndent=0,
        firstLineIndent=0,
        alignment=0,
        wordWrap="CJK",
        spaceBefore=22,
        spaceAfter=12,
    )
    body_style = ParagraphStyle(
        "Body",
        fontName=font_name,
        fontSize=11.8,
        leading=20,
        firstLineIndent=18,
        wordWrap="CJK",
        spaceAfter=5,
    )

    elements = []
    text_length = max(len(annotated_text), 1)
    consumed_length = 0
    first_block = True
    for block in re.split(r"\n\s*\n", annotated_text):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        block_text = "".join(lines)
        elements.append(SourcePageMarker(source_page_position(source_page_range, consumed_length / text_length)))
        if first_block:
            elements.append(Spacer(1, 32 * mm))
            elements.append(paragraph_from_text(format_chapter_title(block_text), chapter_title_style))
            elements.append(Spacer(1, 54 * mm))
            first_block = False
        elif normalize_heading_text(block_text) in section_headings or (not section_headings and is_section_heading(block_text)):
            elements.append(paragraph_from_text(block_text, section_heading_style, render_footnotes=True))
        else:
            elements.append(paragraph_from_text(block_text, body_style, render_footnotes=True))
        consumed_length += len(block) + 2

    if source_notes.strip():
        elements.append(PageBreak())
        elements.append(SourcePageMarker("注释"))
        elements.append(paragraph_from_text("注释", notes_title_style))
        elements.append(Spacer(1, 12))
        note_rows = [
            [
                paragraph_from_text(number, notes_number_style),
                paragraph_from_text(content, notes_body_style),
            ]
            for number, content in parse_numbered_source_notes(source_notes)
        ]
        if note_rows:
            notes_table = Table(note_rows, colWidths=[26, 410], hAlign="LEFT")
            notes_table.setStyle(
                TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (0, -1), 8),
                        ("RIGHTPADDING", (1, 0), (1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 2),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ]
                )
            )
            elements.append(notes_table)

    if editor_notes:
        elements.append(PageBreak())
        elements.append(SourcePageMarker("编者注"))
        elements.append(paragraph_from_text("编者注", notes_title_style))
        elements.append(Spacer(1, 12))
        editor_note_rows = [
            [
                paragraph_from_text(f"编{number}", notes_number_style),
                paragraph_from_text(content, notes_body_style, render_footnotes=True),
            ]
            for number, content in editor_notes
        ]
        editor_notes_table = Table(editor_note_rows, colWidths=[34, 402], hAlign="LEFT")
        editor_notes_table.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (0, -1), 8),
                    ("RIGHTPADDING", (1, 0), (1, -1), 0),
                ]
            )
        )
        elements.append(editor_notes_table)

    if user_notes:
        elements.append(PageBreak())
        elements.append(SourcePageMarker("用户札记"))
        elements.append(paragraph_from_text("用户札记", notes_title_style))
        elements.append(Spacer(1, 12))

        def user_note_paragraphs(content: str):
            lines = []
            for raw_line in content.splitlines():
                line = raw_line.strip()
                if not line or line.startswith("```"):
                    continue
                line = line.replace("**", "")
                if re.fullmatch(r"\|?\s*:?-+.*", line):
                    continue
                if line.startswith("|") and line.endswith("|"):
                    cells = [cell.strip() for cell in line.strip("|").split("|")]
                    line = "｜".join(cell for cell in cells if cell)
                lines.append(paragraph_from_text(line, notes_body_style, render_footnotes=True))
            return lines or [paragraph_from_text(content, notes_body_style, render_footnotes=True)]

        user_note_rows = [
            [
                paragraph_from_text(f"札{number}", notes_number_style),
                user_note_paragraphs(content),
            ]
            for number, content in user_notes
        ]
        user_notes_table = Table(user_note_rows, colWidths=[34, 402], hAlign="LEFT")
        user_notes_table.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (0, -1), 8),
                    ("RIGHTPADDING", (1, 0), (1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        elements.append(user_notes_table)

    term_elements = build_term_table_elements(
        original_text,
        entries,
        counts,
        font_name,
        max_example_length,
        max_terms=max_terms,
    )
    if term_elements:
        annotation_text = f"注：{title}；{subtitle}；{source_note}"
        term_elements.insert(1, SourcePageMarker("阅读词表"))
        term_elements.insert(3, paragraph_from_text(annotation_text, title_annotation_style))
        elements.extend(term_elements)

    bronze_elements = build_term_table_elements(
        original_text,
        bronze_entries,
        bronze_counts,
        font_name,
        max_example_length,
        table_title="青铜器词表",
    )
    if bronze_elements:
        bronze_elements.insert(1, SourcePageMarker("青铜器词表"))
        elements.extend(bronze_elements)

    ancient_review_elements = build_ancient_review_table_elements(ancient_review_entries, font_name)
    if ancient_review_elements:
        ancient_review_elements.insert(1, SourcePageMarker("疑难甲骨文字词校读表"))
        elements.extend(ancient_review_elements)

    reading_note_elements = build_reading_notes_elements(reading_notes, font_name, section_heading_font_name)
    if reading_note_elements:
        reading_note_elements.insert(1, SourcePageMarker("读书札记"))
        elements.extend(reading_note_elements)
    doc.build(elements, canvasmaker=FooterCanvas)
    return font_name, font_source


def cmd_split(args: argparse.Namespace) -> None:
    """Split one chapter from the web text."""
    text = load_text(args.source)
    title, chapter_text = split_chapter(text, args.chapter)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(chapter_text + "\n", encoding="utf-8")
    print(f"Chapter: {args.chapter}")
    print(f"Title: {title}")
    print(f"Output: {args.output}")
    print(f"Characters: {len(chapter_text)}")


def cmd_table(args: argparse.Namespace) -> None:
    """Generate a reading-term table."""
    text = prepare_reading_text(
        normalize_text(load_text(args.input)),
        include_source_notes=args.include_source_notes,
    )
    entries = load_entries(args.dictionary)
    rows = found_rows(text, entries, args.max_example_length)
    resolved_max_terms = effective_max_terms(text, args.max_terms, args.max_terms_percent, args.min_terms)
    rows = limit_rows(rows, resolved_max_terms)
    write_table(args.output, rows, args.input)
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Entries found: {len(rows)}")
    if resolved_max_terms:
        print(f"Term cap: {resolved_max_terms}")


def cmd_lint_images(args: argparse.Namespace) -> None:
    """Find image/caption lines that may split prose."""
    warnings = find_caption_flow_warnings(normalize_text(load_text(args.input)))
    if not warnings:
        print(f"No caption flow warnings: {args.input}")
        return
    print(f"Caption flow warnings: {args.input}")
    for line_number, previous_line, caption_line, following_line in warnings:
        print(f"\nLine {line_number}: {caption_line}")
        print(f"  Previous: {previous_line}")
        print(f"  Next: {following_line}")
    raise SystemExit(1)


def cmd_fix_punctuation(args: argparse.Namespace) -> None:
    """Normalize punctuation spacing in a text file."""
    original = load_text(args.input)
    fixed = normalize_punctuation_spacing(original)
    changed = fixed != original
    if args.check:
        if changed:
            print(f"Punctuation spacing changes needed: {args.input}")
            raise SystemExit(1)
        print(f"Punctuation spacing check: OK ({args.input})")
        return
    if args.in_place:
        args.input.write_text(fixed, encoding="utf-8")
        output = args.input
    elif args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(fixed, encoding="utf-8")
        output = args.output
    else:
        sys.stdout.write(fixed)
        return
    status = "updated" if changed else "unchanged"
    print(f"Punctuation spacing {status}: {output}")


def cmd_ocr_captions(args: argparse.Namespace) -> None:
    """OCR PDF pages and report likely image captions."""
    captions = extract_ocr_captions_from_pdf(
        args.pdf,
        args.start_page,
        args.end_page,
        dpi=args.dpi,
        lang=args.lang,
        min_confidence=args.min_confidence,
    )
    print(f"OCR caption candidates: {args.pdf} pages {args.start_page}-{args.end_page}")
    if not captions:
        print("No likely captions found.")
        return
    for page_number, caption in captions:
        print(f"PDF {page_number} [score {caption_confidence(caption)}]: {caption}")
    if args.clean_text:
        clean_text = load_text(args.clean_text)
        missing = find_missing_ocr_captions(clean_text, captions)
        print(f"\nMissing from clean text: {args.clean_text}")
        if not missing:
            print("No missing caption candidates found.")
            return
        for page_number, caption in missing:
            print(f"PDF {page_number} [score {caption_confidence(caption)}]: {caption}")
        raise SystemExit(1)


def cmd_check_pdf(args: argparse.Namespace) -> None:
    """Run structural checks against the clean text and optional PDF OCR."""
    if args.pdf and (args.start_page is None or args.end_page is None):
        raise ValueError("--pdf requires --start-page and --end-page")
    if (args.start_page is not None or args.end_page is not None) and not args.pdf:
        raise ValueError("--start-page/--end-page require --pdf")

    clean_text = normalize_text(load_text(args.clean_text))
    had_warning = False

    body_markers = extract_explicit_footnote_markers(clean_text)
    note_numbers = extract_source_note_numbers(clean_text)
    print(f"Clean text: {args.clean_text}")
    print(f"Body footnote markers: {len(body_markers)}")
    print(f"Source notes: {len(note_numbers)}")
    if body_markers and note_numbers:
        body_set = set(body_markers)
        note_set = set(note_numbers)
        missing_in_body = sorted(note_set - body_set)
        missing_in_notes = sorted(body_set - note_set)
        body_gaps = find_sequence_gaps(body_markers)
        note_gaps = find_sequence_gaps(note_numbers)
        if missing_in_body or missing_in_notes or body_gaps or note_gaps:
            had_warning = True
            if missing_in_body:
                print(f"Notes without body markers: {missing_in_body}")
            if missing_in_notes:
                print(f"Body markers without notes: {missing_in_notes}")
            if body_gaps:
                print(f"Body marker sequence gaps: {body_gaps}")
            if note_gaps:
                print(f"Note sequence gaps: {note_gaps}")
        else:
            print("Footnote marker check: OK")
    else:
        print("Footnote marker check: skipped because body markers or notes are empty.")

    caption_warnings = find_caption_flow_warnings(clean_text)
    if caption_warnings:
        had_warning = True
        print("\nCaption flow warnings:")
        for line_number, previous_line, caption_line, following_line in caption_warnings:
            print(f"Line {line_number}: {caption_line}")
            print(f"  Previous: {previous_line}")
            print(f"  Next: {following_line}")
    else:
        print("Caption flow check: OK")

    suspicious_tokens = find_suspicious_ocr_tokens(clean_text)
    if suspicious_tokens:
        had_warning = True
        print("\nSuspicious OCR-like tokens:")
        for line_number, token, line in suspicious_tokens:
            print(f"Line {line_number}: {token}  |  {line}")
    else:
        print("Suspicious OCR-token check: OK")

    if args.pdf and args.start_page is not None and args.end_page is not None:
        captions = extract_ocr_captions_from_pdf(
            args.pdf,
            args.start_page,
            args.end_page,
            dpi=args.dpi,
            lang=args.lang,
            min_confidence=args.min_confidence,
        )
        missing = find_missing_ocr_captions(clean_text, captions)
        print(f"\nOCR caption candidates: {len(captions)}")
        if missing:
            had_warning = True
            print("Missing or not clearly represented in clean text:")
            for page_number, caption in missing:
                print(f"PDF {page_number} [score {caption_confidence(caption)}]: {caption}")
        else:
            print("OCR caption check: OK")

    if had_warning:
        raise SystemExit(1)


def cmd_pdf(args: argparse.Namespace) -> None:
    """Generate an annotated PDF."""
    raw_text = normalize_text(load_text(args.input))
    raw_text, editor_notes = extract_editor_notes(raw_text)
    raw_text, user_notes = extract_user_notes(raw_text)
    text = prepare_reading_text(
        raw_text,
        include_source_notes=args.include_source_notes,
    )
    source_notes = "" if args.include_source_notes or args.no_source_note_section else prepare_source_notes(raw_text)
    source_notes = EDITOR_FOOTNOTE_RE.sub("", source_notes).strip()
    entries = load_entries(args.dictionary)
    bronze_entries = load_entries(args.bronze_dictionary) if args.bronze_dictionary else []
    ancient_review_entries = load_ancient_review_entries(args.ancient_review)
    reading_notes = load_reading_notes(args.reading_notes)
    # The PDF prints source notes as part of the reading edition, so its
    # vocabulary list must also consider terms that occur only in those notes.
    # Otherwise a note-only reader aid can be annotated in the prose but remain
    # missing from the PDF vocabulary table.
    vocabulary_text = "\n".join(part for part in (text, source_notes) if part)
    term_counts = count_terms(vocabulary_text, entries)
    resolved_max_terms = effective_max_terms(text, args.max_terms, args.max_terms_percent, args.min_terms)
    display_entries = sort_entries_for_table(entries, term_counts, vocabulary_text, resolved_max_terms)
    annotated_entries = entries + [
        entry for entry in bronze_entries if entry.term not in {main_entry.term for main_entry in display_entries}
    ]
    if resolved_max_terms is not None and resolved_max_terms > 0:
        annotated_entries = display_entries + [
            entry for entry in bronze_entries if entry.term not in {main_entry.term for main_entry in display_entries}
        ]
    chapter_id = chapter_id_from_path(args.input) or chapter_id_from_path(args.output)
    section_headings = load_chapter_subtitles(chapter_id)
    skip_headings = set(section_headings)
    chapter_heading = load_chapter_heading(chapter_id)
    if chapter_heading:
        skip_headings.add(normalize_heading_text(chapter_heading))
    annotated_terms: set[str] = set()
    annotated, annotation_counts = annotate_text(
        text,
        annotated_entries,
        repeat_annotations=args.repeat_annotations,
        skip_headings=skip_headings,
        already_annotated=annotated_terms,
    )
    annotated_source_notes = source_notes
    if source_notes:
        annotated_source_notes, source_note_annotation_counts = annotate_text(
            source_notes,
            annotated_entries,
            repeat_annotations=args.repeat_annotations,
            already_annotated=annotated_terms,
        )
        for term, count in source_note_annotation_counts.items():
            annotation_counts[term] = annotation_counts.get(term, 0) + count
    bronze_counts = count_terms(text, bronze_entries)
    source_page_range = load_source_page_range(args.chapter_map, chapter_id)
    source_page_range = manual_source_page_range(args) or source_page_range
    page_note = args.page_note
    if not page_note and source_page_range is not None:
        if chapter_id == "intro":
            chapter_label = "引子"
        elif chapter_id and re.fullmatch(r"chapter_\d{2}", chapter_id):
            chapter_label = f"第{int(chapter_id[-2:])}章"
        else:
            chapter_label = "本章"
        page_note = (
            f"{chapter_label}约对应印刷页 "
            f"{source_page_range.printed_start}-{source_page_range.printed_end}"
        )
    page_note = page_note or "页码范围未指定"
    source_note = (
        f"文本来源：{args.web_source_url}；"
        f"PDF：{args.pdf_name}，{page_note}"
    )
    _, font_source = build_pdf(
        output_path=args.output,
        title=args.title,
        subtitle=args.subtitle,
        source_note=source_note,
        original_text=text,
        annotated_text=annotated,
        entries=entries,
        counts=term_counts,
        bronze_entries=bronze_entries,
        bronze_counts=bronze_counts,
        ancient_review_entries=ancient_review_entries,
        reading_notes=reading_notes,
        font_path=args.font_path,
        max_example_length=args.max_example_length,
        source_page_range=source_page_range,
        section_headings=section_headings,
        max_terms=resolved_max_terms,
        source_notes=annotated_source_notes,
        editor_notes=editor_notes,
        user_notes=user_notes,
    )
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"PDF font source: {font_source}")
    if source_page_range is not None:
        print(
            "Source pages: "
            f"viewer PDF {source_page_range.pdf_start}-{source_page_range.pdf_end}, "
            f"physical PDF {source_page_range.source_start}-{source_page_range.source_end}, "
            f"printed {source_page_range.printed_start}-{source_page_range.printed_end}"
        )
    print(f"Annotated types: {len(annotation_counts)}")
    print(f"Total annotations inserted: {sum(annotation_counts.values())}")
    if resolved_max_terms:
        print(f"Term cap: {resolved_max_terms}")
    if source_notes:
        print("Source note section: included")
    if editor_notes:
        print(f"Editor note section: included ({len(editor_notes)})")
    if user_notes:
        print(f"User note section: included ({len(user_notes)})")
    if section_headings:
        print(f"TOC section headings: {len(section_headings)}")
    if bronze_entries:
        print(f"Bronze terms found: {sum(1 for entry in bronze_entries if bronze_counts.get(entry.term, 0))}")
    if ancient_review_entries:
        print(f"Ancient text review rows: {len(ancient_review_entries)}")
    if reading_notes:
        print(f"Reading notes: {len(reading_notes)}")


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI parser."""
    parser = argparse.ArgumentParser(description="Build Jianshang chapter study materials.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    split_parser = subparsers.add_parser("split", help="Split a chapter from the full web text.")
    split_parser.add_argument("--source", type=Path, default=Path("sources/136.txt"))
    split_parser.add_argument("--chapter", default="chapter_01")
    split_parser.add_argument("--output", type=Path, default=Path("chapter_01/source.txt"))
    split_parser.set_defaults(func=cmd_split)

    table_parser = subparsers.add_parser("table", help="Generate a typed reading-term table.")
    table_parser.add_argument("input", type=Path)
    table_parser.add_argument("--dictionary", type=Path, required=True)
    table_parser.add_argument("-o", "--output", type=Path, required=True)
    table_parser.add_argument("--max-example-length", type=int, default=42)
    table_parser.add_argument("--max-terms", type=int, default=None)
    table_parser.add_argument("--max-terms-percent", type=float, default=None)
    table_parser.add_argument("--min-terms", type=int, default=20)
    table_parser.add_argument("--include-source-notes", action="store_true")
    table_parser.set_defaults(func=cmd_table)

    lint_images_parser = subparsers.add_parser(
        "lint-images",
        help="Find image/caption placeholders that may split prose sentences.",
    )
    lint_images_parser.add_argument("input", type=Path)
    lint_images_parser.set_defaults(func=cmd_lint_images)

    fix_punctuation_parser = subparsers.add_parser(
        "fix-punctuation",
        help="Normalize common CJK punctuation spacing and OCR line-wrap artifacts.",
    )
    fix_punctuation_parser.add_argument("input", type=Path)
    fix_punctuation_parser.add_argument("-o", "--output", type=Path, default=None)
    fix_punctuation_parser.add_argument("--in-place", action="store_true")
    fix_punctuation_parser.add_argument("--check", action="store_true")
    fix_punctuation_parser.set_defaults(func=cmd_fix_punctuation)

    ocr_captions_parser = subparsers.add_parser(
        "ocr-captions",
        help="OCR original PDF pages and report likely image captions.",
    )
    ocr_captions_parser.add_argument("--pdf", type=Path, default=Path(DEFAULT_PDF_NAME))
    ocr_captions_parser.add_argument("--start-page", type=int, required=True)
    ocr_captions_parser.add_argument("--end-page", type=int, required=True)
    ocr_captions_parser.add_argument("--clean-text", type=Path, default=None)
    ocr_captions_parser.add_argument("--dpi", type=int, default=200)
    ocr_captions_parser.add_argument("--lang", default="chi_sim+eng")
    ocr_captions_parser.add_argument("--min-confidence", type=int, default=5)
    ocr_captions_parser.set_defaults(func=cmd_ocr_captions)

    check_pdf_parser = subparsers.add_parser(
        "check-pdf",
        help="Compare clean text with PDF/OCR structural signals.",
    )
    check_pdf_parser.add_argument("clean_text", type=Path)
    check_pdf_parser.add_argument("--pdf", type=Path, default=None)
    check_pdf_parser.add_argument("--start-page", type=int, default=None)
    check_pdf_parser.add_argument("--end-page", type=int, default=None)
    check_pdf_parser.add_argument("--dpi", type=int, default=200)
    check_pdf_parser.add_argument("--lang", default="chi_sim+eng")
    check_pdf_parser.add_argument("--min-confidence", type=int, default=5)
    check_pdf_parser.set_defaults(func=cmd_check_pdf)

    pdf_parser = subparsers.add_parser("pdf", help="Generate an annotated PDF.")
    pdf_parser.add_argument("input", type=Path)
    pdf_parser.add_argument("--dictionary", type=Path, required=True)
    pdf_parser.add_argument("--bronze-dictionary", type=Path, default=None)
    pdf_parser.add_argument("--ancient-review", type=Path, default=None)
    pdf_parser.add_argument("--reading-notes", type=Path, default=None)
    pdf_parser.add_argument("-o", "--output", type=Path, required=True)
    pdf_parser.add_argument("--title", default="《翦商》第一章注音阅读版")
    pdf_parser.add_argument("--subtitle", default="精选生僻字与阅读术语")
    pdf_parser.add_argument("--web-source-url", default=DEFAULT_WEB_SOURCE_URL)
    pdf_parser.add_argument("--pdf-name", default=DEFAULT_PDF_NAME)
    pdf_parser.add_argument(
        "--page-note",
        default=None,
        help="Override the generated chapter/printed-page note.",
    )
    pdf_parser.add_argument("--chapter-map", type=Path, default=Path("sources/chapter_map.csv"))
    pdf_parser.add_argument("--pdf-page-start", type=int, default=None)
    pdf_parser.add_argument("--pdf-page-end", type=int, default=None)
    pdf_parser.add_argument("--printed-page-start", type=int, default=None)
    pdf_parser.add_argument("--printed-page-end", type=int, default=None)
    pdf_parser.add_argument("--font-path", type=Path, default=None)
    pdf_parser.add_argument("--max-example-length", type=int, default=42)
    pdf_parser.add_argument("--max-terms", type=int, default=None)
    pdf_parser.add_argument("--max-terms-percent", type=float, default=None)
    pdf_parser.add_argument("--min-terms", type=int, default=20)
    pdf_parser.add_argument("--include-source-notes", action="store_true")
    pdf_parser.add_argument("--no-source-note-section", action="store_true")
    pdf_parser.add_argument(
        "--repeat-annotations",
        action="store_true",
        help="Annotate every occurrence. By default, annotate only the first occurrence of each term.",
    )
    pdf_parser.set_defaults(func=cmd_pdf)

    return parser


def main() -> None:
    """Run the command-line interface."""
    try:
        args = build_parser().parse_args()
        args.func(args)
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
