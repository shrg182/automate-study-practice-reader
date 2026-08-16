#!/usr/bin/env python3
"""Build browser OCR/manual-edition editors for 《翦商》 chapters.

The editor is a manual edition workspace: it shows source PDF page images next
to editable text seeded from the processed clean text. Browser exports should
be saved as *_clean_edited.txt and *_edit_log.txt, leaving *_clean.txt as the
processed source.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import jianshang_tools


ROOT = Path(__file__).resolve().parent
DEFAULT_MAP = ROOT / "sources" / "chapter_map.csv"
DEFAULT_PDF = ROOT / "翦商.pdf"
PROJECT_DICTIONARY = ROOT.parent.parent / "project_dictionary" / "dictionary.csv"


def term_metadata(entry_type: str, explicit: str = "") -> tuple[int, str, str]:
    """Return initial difficulty, lexical-unit type, and specialist domain."""
    value = str(explicit).strip()
    if value.isdigit() and 1 <= int(value) <= 5:
        difficulty = int(value)
    else:
        normalized = entry_type.strip().casefold()
        difficulty = 5 if normalized in {"artifact", "bronze_item", "site_or_culture", "person_or_deity"} else 4 if normalized in {"rare_word", "manual", "classical_term", "text"} else 3
    normalized = entry_type.strip().casefold()
    if normalized == "bronze_item":
        return difficulty, "specialist_term", "bronze_vessel"
    if normalized in {"artifact", "site_or_culture"}:
        return difficulty, "specialist_term", "archaeology"
    if normalized in {"person", "place", "person_or_deity", "place_or_group"}:
        return difficulty, "proper_name", "proper_name"
    if normalized in {"phrase", "idiom"}:
        return difficulty, normalized, "phrase"
    return difficulty, "classical_word" if difficulty >= 4 else "word", "general"


@dataclass(frozen=True)
class ChapterMap:
    chapter: str
    title: str
    pdf_start: int
    pdf_end: int
    printed_start: int
    printed_end: int
    source_start: int
    source_end: int
    notes: str

    @property
    def page_count(self) -> int:
        return self.pdf_end - self.pdf_start + 1


def load_chapter_map(path: Path) -> dict[str, ChapterMap]:
    rows: dict[str, ChapterMap] = {}
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            mapping = ChapterMap(
                chapter=row["chapter"],
                title=row["title"],
                pdf_start=int(row["pdf_page_start"]),
                pdf_end=int(row["pdf_page_end"]),
                printed_start=int(row["printed_page_start"]),
                printed_end=int(row["printed_page_end"]),
                source_start=int(row.get("source_page_start") or row["pdf_page_start"]),
                source_end=int(row.get("source_page_end") or row["pdf_page_end"]),
                notes=row.get("notes", ""),
            )
            if not (
                mapping.page_count
                == mapping.printed_end - mapping.printed_start + 1
                == mapping.source_end - mapping.source_start + 1
            ):
                raise ValueError(f"Mismatched page spans for {mapping.chapter}: {path}")
            rows[row["chapter"]] = mapping
    return rows


def chapter_dir(chapter: str) -> Path:
    return ROOT / chapter


def clean_text_path(chapter: str) -> Path:
    if chapter == "intro":
        return chapter_dir(chapter) / "intro_clean.txt"
    return chapter_dir(chapter) / f"{chapter}_clean.txt"


def edited_text_path(chapter: str) -> Path:
    if chapter == "intro":
        return chapter_dir(chapter) / "intro_clean_edited.txt"
    return chapter_dir(chapter) / f"{chapter}_clean_edited.txt"


def edit_log_path(chapter: str) -> Path:
    if chapter == "intro":
        return chapter_dir(chapter) / "intro_edit_log.txt"
    return chapter_dir(chapter) / f"{chapter}_edit_log.txt"


def page_image_name(source_page: int) -> str:
    return f"page-{source_page:03d}.jpg"


def pdf_page_count(path: Path) -> int | None:
    """Return a generated PDF's page count when pdfinfo is available."""
    if not path.exists() or not shutil.which("pdfinfo"):
        return None
    result = subprocess.run(
        ["pdfinfo", str(path)],
        check=False,
        capture_output=True,
        text=True,
    )
    match = re.search(r"^Pages:\s+(\d+)\s*$", result.stdout, re.M)
    return int(match.group(1)) if match else None


def ensure_page_images(mapping: ChapterMap, pdf_path: Path, force: bool = False, dpi: int = 160) -> None:
    """Render source PDF pages to JPEG images for side-by-side review."""
    pages_dir = chapter_dir(mapping.chapter) / "pdf_pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    missing = [
        page
        for page in range(mapping.source_start, mapping.source_end + 1)
        if force or not (pages_dir / page_image_name(page)).exists()
    ]
    if not missing:
        return
    pdftoppm = shutil.which("pdftoppm")
    ghostscript = shutil.which("gs")
    if not pdftoppm and not ghostscript:
        raise RuntimeError(
            "pdftoppm or Ghostscript (gs) is required to render source PDF pages."
        )
    for page in missing:
        prefix = pages_dir / f"page-{page:03d}"
        if pdftoppm:
            command = [
                pdftoppm,
                "-f",
                str(page),
                "-l",
                str(page),
                "-r",
                str(dpi),
                "-jpeg",
                "-singlefile",
                str(pdf_path),
                str(prefix),
            ]
        else:
            command = [
                ghostscript,
                "-q",
                "-dSAFER",
                "-dBATCH",
                "-dNOPAUSE",
                "-sDEVICE=jpeg",
                f"-r{dpi}",
                f"-dFirstPage={page}",
                f"-dLastPage={page}",
                f"-sOutputFile={prefix}.jpg",
                str(pdf_path),
            ]
        subprocess.run(command, check=True)


def paragraph_chunks(text: str, count: int) -> list[str]:
    """Split clean text into approximate page chunks at paragraph boundaries."""
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", text.strip()) if item.strip()]
    if not paragraphs:
        return [""] * count
    target = max(1, len(text) // count)
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0
    remaining_pages = count
    for index, paragraph in enumerate(paragraphs):
        remaining_paragraphs = len(paragraphs) - index
        should_break = (
            current
            and current_len >= target
            and remaining_pages > 1
            and remaining_paragraphs >= remaining_pages
        )
        if should_break:
            chunks.append("\n\n".join(current))
            current = []
            current_len = 0
            remaining_pages -= 1
        current.append(paragraph)
        current_len += len(paragraph)
    if current:
        chunks.append("\n\n".join(current))
    while len(chunks) < count:
        chunks.append("")
    if len(chunks) > count:
        chunks[count - 1] = "\n\n".join(chunks[count - 1 :])
        chunks = chunks[:count]
    return chunks


def load_seed_chunks(mapping: ChapterMap) -> list[str]:
    """Use manual edited text when present; otherwise split the clean text."""
    edited = edited_text_path(mapping.chapter)
    if edited.exists():
        parsed = parse_exported_blocks(edited.read_text(encoding="utf-8"))
        if len(parsed) == mapping.page_count:
            return parsed
        if parsed:
            # Preserve manual edits when a corrected chapter boundary changes
            # the number of page rows; only the paragraph-to-page grouping is
            # recalculated.
            return paragraph_chunks("\n\n".join(parsed), mapping.page_count)
    clean_path = clean_text_path(mapping.chapter)
    return paragraph_chunks(clean_path.read_text(encoding="utf-8"), mapping.page_count)


def parse_exported_blocks(text: str) -> list[str]:
    header_pattern = re.compile(r"^===== PDF page \d+ / printed page \d+ =====\s*$", re.M)
    matches = list(header_pattern.finditer(text))
    blocks: list[str] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append(text[start:end].strip())
    return blocks


def build_export_text(mapping: ChapterMap, chunks: list[str]) -> str:
    blocks = []
    for index, body in enumerate(chunks):
        pdf_page = mapping.pdf_start + index
        printed_page = mapping.printed_start + index
        blocks.append(
            f"===== PDF page {pdf_page:03d} / printed page {printed_page} =====\n\n{body.strip()}"
        )
    return "\n\n".join(blocks).strip() + "\n"


def write_seed_export(mapping: ChapterMap, chunks: list[str]) -> None:
    edited = edited_text_path(mapping.chapter)
    # This file becomes the user's manual-edition artifact as soon as work
    # begins. Editor regeneration must never replace it merely because its
    # page markers no longer resemble a pristine seed export.
    if not edited.exists():
        edited.write_text(build_export_text(mapping, chunks), encoding="utf-8")
    log = edit_log_path(mapping.chapter)
    if not log.exists():
        log.write_text("", encoding="utf-8")


def load_terms(chapter: str, limit: int = 36) -> list[tuple[str, str]]:
    path = chapter_dir(chapter) / "reading_terms.csv"
    if not path.exists():
        return []
    terms: list[tuple[str, str]] = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            term = (row.get("term") or row.get("字词") or row.get("word") or "").strip()
            note = (row.get("pinyin") or row.get("拼音") or row.get("note") or row.get("说明") or "").strip()
            if term:
                terms.append((term, note))
            if len(terms) >= limit:
                break
    return terms


def load_project_dictionary_terms(
    text: str, local_rows: list[dict[str, str]]
) -> list[dict[str, str]]:
    """Return shared Chinese dictionary entries present in this chapter."""
    if not PROJECT_DICTIONARY.exists():
        return []
    local_terms = {row.get("term", "").strip() for row in local_rows}
    matches: list[dict[str, str]] = []
    with PROJECT_DICTIONARY.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            term = row.get("term", "").strip()
            if row.get("language") != "zh" or len(term) < 2 or term in local_terms or term not in text:
                continue
            difficulty, unit_type, domain = term_metadata(row.get("type", ""), row.get("difficulty", ""))
            matches.append({
                "term": term,
                "pinyin": row.get("pinyin", "").strip(),
                "type": "项目词典",
                "annotation": row.get("definition", "").strip(),
                "difficulty": difficulty,
                "unit_type": unit_type,
                "domain": domain,
            })
    return sorted(matches, key=lambda item: (-len(item["term"]), item["term"]))


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    """Load a UTF-8 CSV as trimmed dictionaries."""
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def chapter_bronze_terms_path(chapter: str) -> Path:
    """Return the most relevant bronze-term dictionary for a chapter."""
    chapter_path = chapter_dir(chapter) / "bronze_terms.csv"
    if chapter_path.exists():
        return chapter_path
    return ROOT / "chapter_04" / "bronze_terms.csv"


def chapter_pdf_term_rows(chapter: str, clean_text: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Select the same chapter-specific vocabulary rows used by the PDF."""
    raw_text = jianshang_tools.normalize_text(clean_text)
    raw_text, _editor_notes = jianshang_tools.extract_editor_notes(raw_text)
    reading_text = jianshang_tools.prepare_reading_text(raw_text, include_source_notes=False)
    source_notes = jianshang_tools.prepare_source_notes(raw_text)
    source_notes = jianshang_tools.EDITOR_FOOTNOTE_RE.sub("", source_notes).strip()
    vocabulary_text = "\n".join(part for part in (reading_text, source_notes) if part)

    entries = jianshang_tools.load_entries(chapter_dir(chapter) / "reading_terms.csv")
    counts = jianshang_tools.count_terms(vocabulary_text, entries)
    selected = jianshang_tools.sort_entries_for_table(entries, counts, vocabulary_text)

    bronze_entries = jianshang_tools.load_entries(chapter_bronze_terms_path(chapter))
    bronze_counts = jianshang_tools.count_terms(reading_text, bronze_entries)
    selected_bronze = jianshang_tools.sort_entries_for_table(
        bronze_entries,
        bronze_counts,
        reading_text,
    )

    explicit_by_term = {
        row.get("term", "").strip(): row.get("difficulty", "").strip()
        for row in load_csv_rows(chapter_dir(chapter) / "reading_terms.csv")
    }

    def rows(items: list[jianshang_tools.AnnotationEntry]) -> list[dict[str, object]]:
        return [
            {
                "term": item.term,
                "pinyin": item.pinyin,
                "type": item.entry_type,
                "annotation": item.annotation,
                "difficulty": term_metadata(item.entry_type, explicit_by_term.get(item.term, ""))[0],
                "unit_type": term_metadata(item.entry_type, explicit_by_term.get(item.term, ""))[1],
                "domain": term_metadata(item.entry_type, explicit_by_term.get(item.term, ""))[2],
            }
            for item in items
        ]

    return rows(selected), rows(selected_bronze)


def aggregate_master_terms() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Aggregate current chapter dictionaries into book-wide reference rows."""
    vocabulary: dict[str, dict[str, str]] = {}
    bronze: dict[str, dict[str, str]] = {}

    def merge(target: dict[str, dict[str, str]], row: dict[str, str], chapter: str) -> None:
        term = (row.get("term") or "").strip()
        if not term:
            return
        item = target.setdefault(term, {
            "term": term, "pinyin": "", "type": "", "annotation": "", "chapters": ""
        })
        for field in ("pinyin", "type", "annotation"):
            if not item[field] and row.get(field):
                item[field] = row[field]
        chapters = set(filter(None, item["chapters"].split("、")))
        chapters.add(chapter)
        item["chapters"] = "、".join(sorted(chapters))

    for path in sorted(ROOT.glob("*/reading_terms.csv")):
        chapter = path.parent.name
        for row in load_csv_rows(path):
            merge(vocabulary, row, chapter)
            if row.get("type") == "bronze_item":
                merge(bronze, row, chapter)
    for path in sorted(ROOT.glob("*/bronze_terms.csv")):
        chapter = path.parent.name
        for row in load_csv_rows(path):
            merge(bronze, row, chapter)
    sort_key = lambda row: (row["pinyin"].casefold(), row["term"])
    return sorted(vocabulary.values(), key=sort_key), sorted(bronze.values(), key=sort_key)


def render_master_reference_page() -> str:
    vocabulary, bronze = aggregate_master_terms()

    def rows(items: list[dict[str, str]]) -> str:
        return "".join(
            "<tr>" + "".join(f"<td>{html.escape(item[field])}</td>" for field in
                              ("term", "pinyin", "type", "annotation", "chapters")) + "</tr>"
            for item in items
        ) or '<tr><td colspan="5">暂无条目</td></tr>'

    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>《翦商》总词表</title><style>
:root{{--paper:#fffdfa;--ink:#25221e;--line:#d8d3c7;--accent:#8a1f1f;--soft:#eee8dc}}*{{box-sizing:border-box}}body{{margin:0;background:#f7f5ef;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",sans-serif}}header{{position:sticky;top:0;background:rgba(255,253,250,.97);border-bottom:1px solid var(--line);padding:14px 4vw;z-index:3}}h1{{margin:0 0 10px;font-size:1.3rem}}nav{{display:flex;gap:8px;flex-wrap:wrap;align-items:center}}a{{color:var(--accent)}}nav a{{border:1px solid var(--line);background:white;border-radius:6px;padding:7px 10px;text-decoration:none;color:var(--ink)}}input{{min-width:260px;flex:1;max-width:520px;padding:8px 10px;border:1px solid var(--line);border-radius:6px;font:inherit}}main{{width:min(1280px,92vw);margin:22px auto 60px}}section{{background:var(--paper);border:1px solid var(--line);margin:0 0 24px;scroll-margin-top:110px}}h2{{margin:0;padding:12px 14px;background:var(--soft);border-bottom:1px solid var(--line);font-size:1.05rem}}.count{{color:#666;font-weight:400}}.scroll{{overflow:auto;max-height:72vh}}table{{width:100%;border-collapse:collapse}}th,td{{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}th{{position:sticky;top:0;background:#fff8ec}}td:nth-child(1),td:nth-child(2){{white-space:nowrap}}tr[hidden]{{display:none}}
</style></head><body><header><h1>《翦商》全书参考表</h1><nav><a href="#vocabulary">总词表</a><a href="#bronze">青铜器名总表</a><input id="filter" type="search" placeholder="搜索词条、拼音、说明或章节"></nav></header><main>
<section id="vocabulary"><h2>总词表 <span class="count">（{len(vocabulary)} 条）</span></h2><div class="scroll"><table><thead><tr><th>词条</th><th>拼音</th><th>类型</th><th>说明</th><th>章节</th></tr></thead><tbody>{rows(vocabulary)}</tbody></table></div></section>
<section id="bronze"><h2>青铜器名总表 <span class="count">（{len(bronze)} 条）</span></h2><div class="scroll"><table><thead><tr><th>器名</th><th>拼音</th><th>类型</th><th>说明</th><th>章节</th></tr></thead><tbody>{rows(bronze)}</tbody></table></div></section>
</main><script>const filter=document.getElementById('filter');filter.addEventListener('input',()=>{{const query=filter.value.trim().toLocaleLowerCase();document.querySelectorAll('tbody tr').forEach(row=>row.hidden=query&&!row.textContent.toLocaleLowerCase().includes(query));}});</script></body></html>"""


def build_master_reference_page() -> Path:
    output = ROOT / "reference_tables.html"
    output.write_text(render_master_reference_page(), encoding="utf-8")
    return output


def build_shared_toc_component(mappings: dict[str, ChapterMap]) -> Path:
    """Generate the shared table-of-contents Web Component from chapter_map.csv."""
    chapters = [
        {
            "chapter": item.chapter,
            "title": item.title,
            "printedStart": item.printed_start,
            "printedEnd": item.printed_end,
            "available": (chapter_dir(item.chapter) / "editor.html").exists(),
        }
        for item in mappings.values()
    ]
    source = f"""const JIANSHANG_CHAPTERS = {json.dumps(chapters, ensure_ascii=False, indent=2)};

class JianshangEditorToc extends HTMLElement {{
  connectedCallback() {{
    if (this.dataset.rendered === "true") return;
    this.dataset.rendered = "true";
    const current = this.getAttribute("current-chapter") || "";
    const section = document.createElement("section");
    section.className = "toc-page";
    section.id = "toc";
    section.innerHTML = `<div class="toc-head"><h2>目录</h2><span>手工校订工作台</span></div>
      <div class="toc-body"><div><h3>章节</h3><div class="toc-legend"><span class="legend-current">当前章节</span><span class="legend-available">可打开</span><span class="legend-unavailable">尚未生成</span></div><div class="toc-links"></div></div>
      <div><h3>工作说明</h3><p>左侧文字来自已处理的 clean 文本，并按段落近似切分到 PDF 页。右侧为源 PDF 页面图像。手工修改后请使用“生成文本”或“下载 TXT”，作为 manual edition 输出。</p><p>浏览器自动保存只保存在本机 localStorage；长期保存请下载 TXT 和日志。</p></div></div>`;
    const links = section.querySelector(".toc-links");
    for (const item of JIANSHANG_CHAPTERS) {{
      const link = document.createElement("a");
      const isCurrent = item.chapter === current;
      link.className = `toc-link ${{isCurrent ? "current" : item.available ? "available" : "unavailable"}}`;
      if (item.available) {{
        link.href = isCurrent ? "editor.html" : `../${{item.chapter}}/editor.html`;
      }} else {{
        link.setAttribute("aria-disabled", "true");
        link.title = "此章 editor.html 尚未生成";
      }}
      const title = document.createElement("span");
      title.textContent = item.title;
      const pages = document.createElement("span");
      pages.textContent = `${{item.printedStart}}-${{item.printedEnd}}`;
      link.append(title, pages);
      links.append(link);
    }}
    this.replaceChildren(section);
  }}
}}

if (!customElements.get("jianshang-editor-toc")) {{
  customElements.define("jianshang-editor-toc", JianshangEditorToc);
}}
"""
    output = ROOT / "shared" / "editor_toc.js"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(source, encoding="utf-8")
    return output


def load_reading_notes(chapter: str) -> list[tuple[str, str]]:
    """Parse chapter reading notes from Markdown headings."""
    path = chapter_dir(chapter) / "reading_notes.md"
    if not path.exists():
        return []

    text = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
    sections: list[tuple[str, str]] = []
    current_title: str | None = None
    current_body: list[str] = []

    for line in text.splitlines():
        if line.startswith("## "):
            if current_title and "\n".join(current_body).strip():
                sections.append((current_title, "\n".join(current_body).strip()))
            current_title = line[3:].strip()
            current_body = []
        elif current_title:
            current_body.append(line)

    if current_title and "\n".join(current_body).strip():
        sections.append((current_title, "\n".join(current_body).strip()))

    return sections


def render_data_table(
    section_id: str,
    title: str,
    rows: list[dict[str, str]],
    columns: list[tuple[str, str]],
    empty_text: str,
) -> str:
    """Render a simple reference table for the editor."""
    if rows:
        body = "".join(
            "<tr>"
            + "".join(f"<td>{esc(row.get(key, ''))}</td>" for key, _label in columns)
            + "</tr>"
            for row in rows
        )
    else:
        body = f'<tr><td colspan="{len(columns)}">{esc(empty_text)}</td></tr>'

    headers = "".join(f"<th>{esc(label)}</th>" for _key, label in columns)
    return f"""
        <section class="reference-panel" id="{section_id}">
          <h2>{esc(title)}</h2>
          <div class="table-scroll">
            <table class="data-table">
              <thead><tr>{headers}</tr></thead>
              <tbody>{body}</tbody>
            </table>
          </div>
        </section>"""


def render_reading_notes_table(chapter: str) -> str:
    """Render reading notes as a table."""
    return f"""
        <section class="reference-panel" id="dushuzhaji">
          <h2>章节导读札记</h2>
          <div class="chapter-note-entry">
            <label>主题<input id="chapterNoteTitle" type="text" placeholder="例如：周公改革的沉默"></label>
            <label>札记<textarea id="chapterNoteText" placeholder="记录对本章整体内容的理解、判断或总结"></textarea></label>
            <div class="note-actions">
              <button id="addChapterNoteBtn" type="button">新增章节导读札记</button>
              <button id="downloadChapterNotesBtn" type="button">下载 Markdown</button>
            </div>
            <div class="log-meta">新增内容保存在本浏览器及 JSON 备份中；下载 Markdown 后可作为 reading_notes.md 导入项目。</div>
          </div>
          <div class="table-scroll">
            <table class="data-table note-table">
              <thead><tr><th>主题</th><th>札记</th><th>操作</th></tr></thead>
              <tbody id="chapterNotesBody"><tr><td colspan="3">暂无章节导读札记</td></tr></tbody>
            </table>
          </div>
        </section>"""


def load_ancient_review(chapter: str) -> list[dict[str, str]]:
    """Load the optional chapter ancient-text/OCR review table."""
    path = chapter_dir(chapter) / "oracle_review.tsv"
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def render_editor(mapping: ChapterMap, chunks: list[str]) -> str:
    chapter = mapping.chapter
    clean_text = clean_text_path(chapter).read_text(encoding="utf-8")
    content_version = hashlib.sha256(clean_text.encode("utf-8")).hexdigest()[:12]
    storage_key = f"jianshang:{chapter}:editor:v3:{content_version}"
    log_key = f"jianshang:{chapter}:editor-log:v1"
    output_name = edited_text_path(chapter).name
    log_name = edit_log_path(chapter).name
    backup_name = f"{chapter}_editor_backup.json"
    annotated_pdf_name = f"{chapter}_annotated.pdf"
    annotated_pages = pdf_page_count(chapter_dir(chapter) / annotated_pdf_name)
    annotated_page_label = f"1-{annotated_pages}" if annotated_pages else "独立页码"
    term_rows, bronze_term_rows = chapter_pdf_term_rows(chapter, clean_text)
    term_rows.extend(load_project_dictionary_terms(clean_text, term_rows))
    combined_terms = term_rows + [
        row for row in bronze_term_rows
        if row["term"] not in {item["term"] for item in term_rows}
    ]
    original_chunks = paragraph_chunks(clean_text, mapping.page_count)
    original_texts = {
        f"{mapping.pdf_start + index:03d}": body
        for index, body in enumerate(original_chunks)
    }

    pages = []
    nav_buttons = [
        '<button type="button" class="nav-button" data-target="toc"><span>目录</span><span>top</span></button>',
        '<button type="button" class="nav-button" data-target="notes"><span>编辑札记</span><span>log</span></button>',
    ]
    reference_buttons = [
        '<button type="button" class="nav-button" data-target="yueducibiao"><span>阅读词表</span><span>表</span></button>',
        '<button type="button" class="nav-button" data-target="qingtongqicibiao"><span>青铜器词表</span><span>表</span></button>',
        '<button type="button" class="nav-button" data-target="dushuzhaji"><span>章节导读札记</span><span>表</span></button>',
        '<button type="button" class="nav-button" data-target="user-notes"><span>用户札记</span><span>注</span></button>',
    ]
    ancient_review_rows = load_ancient_review(chapter)
    if ancient_review_rows:
        reference_buttons.insert(
            2,
            '<button type="button" class="nav-button" data-target="ancient-review"><span>古文字校读</span><span>表</span></button>',
        )
    annotated_references = (
        ("shengmin_annotated.md", "《生民》注音注释"),
        ("gongliu_annotated.md", "《公刘》注音注释"),
    )
    for filename, label in annotated_references:
        if (chapter_dir(chapter) / filename).exists():
            reference_buttons.append(
                f'<a class="nav-button action-link" href="{filename}" target="_blank" '
                f'rel="noopener"><span>{label}</span><span>MD ↗</span></a>'
            )
    for index, body in enumerate(chunks):
        pdf_page = mapping.pdf_start + index
        printed_page = mapping.printed_start + index
        source_page = mapping.source_start + index
        page_id = f"page-{pdf_page:03d}"
        image = f"pdf_pages/{page_image_name(source_page)}"
        nav_buttons.append(
            f'<button type="button" class="nav-button" data-target="{page_id}">'
            f"<span>原阅 {pdf_page:03d} · 原PDF {source_page:03d}</span>"
            f"<span>印 {printed_page}</span></button>"
        )
        pages.append(
            f"""
        <section class="page" id="{page_id}">
          <div class="page-head">
            <div class="page-title">原书阅读器页 {pdf_page:03d}<span>原书物理 PDF 页 {source_page:03d}</span><span>印刷页 {printed_page}</span></div>
            <div class="page-tools">
              <button type="button" data-copy-page="{pdf_page:03d}">复制本页</button>
              <button type="button" data-export-page="{pdf_page:03d}">导出本页</button>
            </div>
          </div>
          <div class="workbench">
            <div class="editor-wrap">
              <div class="rich-editor" data-page="{pdf_page:03d}" contenteditable="true" role="textbox" aria-multiline="true" spellcheck="false">{esc(body)}</div>
            </div>
            <div class="scan"><img src="{image}" alt="PDF page {pdf_page:03d}"></div>
          </div>
        </section>"""
        )

    term_items = "".join(
        f'<button type="button" class="term" data-term="{html.escape(row["term"], quote=True)}" '
        f'data-pinyin="{html.escape(row["pinyin"], quote=True)}" '
        f'data-difficulty="{row["difficulty"]}" data-domain="{html.escape(str(row["domain"]), quote=True)}">'
        f'<span>{esc(row["term"])}</span>'
        f'<span>{esc(row["pinyin"])}</span></button>'
        for row in combined_terms
    )
    if not term_items:
        term_items = '<div class="term"><span>暂无术语</span><span></span></div>'

    reading_terms_table = render_data_table(
        "yueducibiao",
        "阅读词表",
        term_rows,
        [
            ("term", "词条"),
            ("pinyin", "拼音"),
            ("type", "类型"),
            ("annotation", "说明"),
        ],
        "暂无阅读词表",
    )
    bronze_terms_table = render_data_table(
        "qingtongqicibiao",
        "青铜器词表",
        bronze_term_rows,
        [
            ("term", "器名"),
            ("pinyin", "拼音"),
            ("type", "类型"),
            ("annotation", "说明"),
        ],
        "暂无青铜器词表",
    )
    reading_notes_table = render_reading_notes_table(chapter)
    ancient_review_table = ""
    if ancient_review_rows:
        ancient_review_table = render_data_table(
            "ancient-review",
            "疑难古文字与 OCR 校读表",
            ancient_review_rows,
            [
                ("source", "来源"),
                ("current_text", "当前文字"),
                ("issue", "问题"),
                ("action", "处理"),
            ],
            "暂无古文字校读项目",
        )
    user_notes_table = """
        <section class="reference-panel" id="user-notes">
          <h2>用户札记</h2>
          <div class="table-scroll">
            <table class="data-table note-table">
              <thead><tr><th>类型</th><th>页</th><th>内容</th></tr></thead>
              <tbody id="userNotesBody"><tr><td colspan="3">暂无用户札记</td></tr></tbody>
            </table>
          </div>
        </section>"""
    reference_tables = (
        reading_terms_table
        + bronze_terms_table
        + ancient_review_table
        + reading_notes_table
        + user_notes_table
    )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>《翦商》{esc(mapping.title)} OCR 手工校订</title>
  <script src="../shared/editor_header.js"></script>
  <script src="../shared/editor_toc.js"></script>
  <style>
    :root {{ --bg:#f7f5ef; --paper:#fffdfa; --ink:#222; --muted:#666; --line:#d8d3c7; --soft:#eee8dc; --accent:#8a1f1f; --accent-ink:#fff; --warn:#9b5d00; --ok:#1f6b40; --shadow:0 8px 24px rgba(30,24,16,.08); }}
    * {{ box-sizing:border-box; }}
    html {{ scroll-behavior:smooth; }}
    body {{ margin:0; background:var(--bg); color:var(--ink); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif; line-height:1.5; }}
    jianshang-editor-header, jianshang-editor-toc {{ display:contents; }}
    button, textarea, input, select, .rich-editor {{ font:inherit; }}
    header {{ position:sticky; top:0; z-index:20; background:rgba(255,253,250,.96); border-bottom:1px solid var(--line); backdrop-filter:blur(10px); }}
    .topbar {{ display:grid; grid-template-columns:minmax(260px,1fr) auto; gap:16px; width:min(1440px,calc(100% - 28px)); margin:0 auto; padding:12px 0; align-items:center; }}
    h1 {{ margin:0; font-size:1.2rem; line-height:1.2; letter-spacing:0; }}
    .subtitle {{ margin-top:3px; color:var(--muted); font-size:.88rem; }}
    .actions {{ display:flex; flex-wrap:wrap; gap:8px; justify-content:flex-end; align-items:center; }}
    button {{ border:1px solid var(--line); background:#fff; color:var(--ink); min-height:34px; padding:6px 10px; border-radius:6px; cursor:pointer; }}
    .import-label, .action-link {{ border:1px solid var(--line); background:#fff; color:var(--ink); min-height:34px; padding:6px 10px; border-radius:6px; cursor:pointer; display:inline-flex; align-items:center; text-decoration:none; }}
    button.primary {{ background:var(--accent); color:var(--accent-ink); border-color:var(--accent); }}
    button:focus-visible, textarea:focus-visible, input:focus-visible, select:focus-visible, .rich-editor:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
    .format-menu {{ position:relative; }}
    .format-menu-trigger {{ display:flex; min-width:45px; align-items:center; justify-content:center; gap:7px; }}
    .marker-icon {{ display:inline-block; width:17px; height:8px; border-bottom:6px solid #f4c542; transform:skew(-12deg); }}
    .format-menu-trigger::after {{ content:"▾"; font-size:10px; color:var(--muted); }}
    .format-popover {{ position:absolute; top:calc(100% + 6px); left:0; z-index:40; display:none; width:178px; padding:5px; background:#fff; border:1px solid #cfc8ba; border-radius:8px; box-shadow:0 10px 30px #2927202e; }}
    .format-menu.open .format-popover {{ display:block; }}
    .format-option {{ display:flex; width:100%; gap:10px; align-items:center; border:0; background:#fff; padding:7px 9px; text-align:left; }}
    .format-option:hover,.format-option:focus {{ background:#edf2f5; color:var(--ink); }}
    .format-dot {{ width:15px; height:15px; flex:0 0 auto; border-radius:50%; box-shadow:inset 0 0 0 1px #00000018; }}
    .format-symbol {{ width:15px; text-align:center; font:600 15px/1 Georgia,serif; }}
    .format-divider {{ height:1px; margin:5px 4px; background:#ddd7cb; }}
    .status {{ color:var(--muted); font-size:.86rem; min-width:132px; text-align:right; }}
    main {{ width:min(1440px,calc(100% - 28px)); margin:18px auto 48px; }}
    .layout {{ display:grid; grid-template-columns:280px minmax(0,1fr); gap:18px; align-items:start; }}
    aside {{ position:sticky; top:calc(var(--editor-header-height, 75px) + 12px); display:grid; gap:14px; max-height:calc(100vh - var(--editor-header-height, 75px) - 24px); overflow:auto; }}
    .panel, .page, .toc-page, .reference-panel, .notes-dock, .export-dock {{ background:var(--paper); border:1px solid var(--line); box-shadow:var(--shadow); }}
    .panel h2, .reference-panel h2, .notes-dock h2, .export-dock h2 {{ margin:0; padding:10px 12px; font-size:.95rem; border-bottom:1px solid var(--line); background:var(--soft); }}
    .page-number-legend {{ padding:8px 11px; font-size:.82rem; color:var(--muted); }}
    .page-number-legend p {{ margin:3px 0; }}
    .page-number-legend strong {{ color:var(--ink); }}
    .nav-list, .term-list {{ padding:8px; display:grid; gap:6px; }}
    .nav-button {{ width:100%; display:flex; justify-content:space-between; gap:8px; text-align:left; }}
    .nav-button span:last-child, .term span:last-child {{ color:var(--muted); font-variant-numeric:tabular-nums; }}
    .term {{ display:flex; justify-content:space-between; gap:8px; border-bottom:1px solid var(--line); padding:4px 0; font-size:.9rem; }}
    button.term {{ width:100%; min-height:0; border-width:0 0 1px; border-radius:0; background:transparent; text-align:left; }}
    button.term:hover {{ color:var(--accent); background:#fff8ec; }}
    .pages {{ display:grid; gap:18px; }}
    .toc-page, .reference-panel, .page {{ scroll-margin-top:86px; }}
    .toc-head {{ display:flex; justify-content:space-between; gap:14px; align-items:baseline; padding:14px 16px; border-bottom:1px solid var(--line); background:#fff; }}
    .toc-head h2 {{ margin:0; font-size:1.15rem; }}
    .toc-body {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(280px,.72fr); gap:18px; padding:14px 16px 16px; }}
    .toc-body h3 {{ margin:0 0 8px; font-size:.95rem; }}
    .toc-links {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:6px; }}
    .toc-link {{ display:flex; justify-content:space-between; gap:10px; border:1px solid var(--line); border-radius:6px; background:#fff; color:var(--ink); text-decoration:none; padding:7px 9px; min-height:34px; align-items:center; }}
    .toc-link.available {{ border-left:4px solid var(--ok); background:#f4fbf6; }}
    .toc-link.current {{ border:2px solid var(--accent); background:#fff0ec; color:var(--accent); font-weight:700; }}
    .toc-link.unavailable {{ background:#f1f0ed; color:#999; cursor:not-allowed; opacity:.72; }}
    .toc-legend {{ display:flex; flex-wrap:wrap; gap:10px; margin:0 0 8px; color:var(--muted); font-size:.8rem; }}
    .toc-legend span::before {{ content:""; display:inline-block; width:10px; height:10px; border-radius:2px; margin-right:4px; }}
    .legend-current::before {{ background:var(--accent); }} .legend-available::before {{ background:var(--ok); }} .legend-unavailable::before {{ background:#aaa; }}
    .toc-link span:first-child {{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
    .toc-link span:last-child {{ color:var(--muted); font-size:.86rem; font-variant-numeric:tabular-nums; white-space:nowrap; }}
    .reference-grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; margin:18px 0; align-items:start; }}
    #user-notes {{ grid-column:1 / -1; }}
    #user-notes .table-scroll {{ max-height:440px; }}
    #user-notes table {{ table-layout:fixed; }}
    #user-notes th:nth-child(1), #user-notes td:nth-child(1) {{ width:110px; }}
    #user-notes th:nth-child(2), #user-notes td:nth-child(2) {{ width:110px; }}
    #user-notes td:nth-child(3) {{ overflow-wrap:anywhere; }}
    .table-scroll {{ overflow:auto; max-height:360px; }}
    #yueducibiao .table-scroll {{ max-height:none; overflow:visible; }}
    .data-table {{ width:100%; border-collapse:collapse; background:#fff; font-size:.9rem; }}
    .data-table th, .data-table td {{ border-bottom:1px solid var(--line); border-right:1px solid var(--line); padding:7px 8px; text-align:left; vertical-align:top; }}
    .data-table th:last-child, .data-table td:last-child {{ border-right:0; }}
    .data-table th {{ position:sticky; top:0; background:#fff8ec; z-index:1; font-weight:700; }}
    .data-table td {{ white-space:pre-wrap; }}
    .note-table td:first-child {{ min-width:150px; font-weight:650; }}
    .chapter-note-entry {{ display:grid; gap:10px; padding:12px; border-bottom:1px solid var(--line); background:#fffdf8; }}
    .chapter-note-entry label {{ display:grid; gap:5px; color:var(--muted); font-size:.88rem; }}
    .chapter-note-entry input, .chapter-note-entry textarea {{ width:100%; border:1px solid var(--line); background:#fff; color:var(--ink); border-radius:6px; padding:8px; font:inherit; }}
    .chapter-note-entry textarea {{ min-height:100px; resize:vertical; }}
    .page-head {{ display:flex; justify-content:space-between; gap:12px; align-items:center; padding:10px 12px; border-bottom:1px solid var(--line); background:#fff; }}
    .page-title {{ font-weight:700; }}
    .page-title span {{ color:var(--muted); font-weight:500; margin-left:8px; }}
    .page-tools {{ display:flex; gap:8px; flex-wrap:wrap; }}
    .workbench {{ display:grid; grid-template-columns:minmax(340px,1fr) minmax(300px,.82fr); gap:0; align-items:stretch; }}
    .editor-wrap {{ padding:12px; border-right:1px solid var(--line); display:flex; min-height:560px; }}
    textarea {{ width:100%; min-height:0; border:1px solid var(--line); background:#fff; color:var(--ink); padding:14px; border-radius:6px; line-height:1.85; font-size:1.02rem; letter-spacing:0; overflow:auto; }}
    .rich-editor {{ width:100%; min-height:536px; border:1px solid var(--line); background:#fff; color:var(--ink); padding:14px; border-radius:6px; line-height:1.85; font-size:1.02rem; letter-spacing:0; overflow:auto; white-space:pre-wrap; overflow-wrap:anywhere; }}
    .rich-editor.annotated-view {{ background:#fff9e8; color:#5b481f; }}
    .rich-editor u,.rich-editor [style*="underline"] {{ text-underline-offset:.2em; text-decoration-thickness:1px; }}
    .mode-badge {{ border-radius:999px; padding:5px 9px; background:var(--soft); color:var(--muted); font-size:.82rem; white-space:nowrap; }}
    .mode-badge.annotated {{ background:#fff0b8; color:#76500e; }}
    .speech-rate {{ display:flex; align-items:center; gap:4px; color:var(--muted); font-size:.82rem; }}
    #speechRate {{ width:82px; }}
    .hidden {{ display:none !important; }}
    .scan {{ padding:12px; background:#fbfaf6; display:flex; }}
    .scan img {{ width:100%; height:auto; display:block; border:1px solid var(--line); background:#fff; align-self:flex-start; }}
    .notes-dock {{ margin-top:18px; scroll-margin-top:86px; }}
    .note-grid {{ display:grid; grid-template-columns:minmax(240px,.75fr) minmax(320px,1fr); gap:12px; padding:12px; }}
    .note-controls {{ display:grid; gap:10px; align-content:start; }}
    .note-controls label {{ display:grid; gap:5px; color:var(--muted); font-size:.88rem; }}
    .note-controls select, .note-controls input {{ width:100%; border:1px solid var(--line); background:#fff; color:var(--ink); border-radius:6px; min-height:34px; padding:6px 8px; }}
    .marker-composer {{ border:1px solid var(--line); border-radius:7px; background:#fffaf0; padding:10px; display:grid; gap:8px; }}
    .marker-composer h3 {{ margin:0; font-size:.92rem; }}
    .marker-help {{ margin:0; color:var(--muted); font-size:.8rem; line-height:1.5; }}
    .note-actions {{ display:flex; gap:8px; flex-wrap:wrap; }}
    #noteText {{ min-height:150px; resize:vertical; }}
    .log-list {{ max-height:260px; overflow:auto; border:1px solid var(--line); background:#fff; border-radius:6px; padding:8px; display:grid; gap:8px; }}
    .log-item {{ border-bottom:1px solid var(--line); padding:0 0 8px; }}
    .log-item:last-child {{ border-bottom:0; padding-bottom:0; }}
    .log-meta {{ color:var(--muted); font-size:.82rem; font-variant-numeric:tabular-nums; }}
    .log-note {{ margin-top:3px; white-space:pre-wrap; }}
    .export-dock {{ margin-top:18px; }}
    #exportText {{ min-height:240px; border:0; border-radius:0; }}
    .quick-note-jump {{ position:fixed; right:18px; bottom:18px; z-index:25; background:var(--accent); color:var(--accent-ink); border-color:var(--accent); box-shadow:0 8px 24px rgba(30,24,16,.18); }}
    @media (max-width:980px) {{ .topbar {{ grid-template-columns:1fr; }} .actions {{ justify-content:flex-start; }} .status {{ text-align:left; }} .layout {{ grid-template-columns:1fr; }} aside {{ position:static; max-height:none; }} .toc-body, .note-grid {{ grid-template-columns:1fr; }} .toc-links {{ grid-template-columns:1fr; }} .reference-grid {{ grid-template-columns:1fr; }} .workbench {{ grid-template-columns:1fr; }} .editor-wrap {{ border-right:0; border-bottom:1px solid var(--line); }} .rich-editor {{ min-height:520px; }} .quick-note-jump {{ right:12px; bottom:12px; }} }}
  </style>
</head>
<body>
  <jianshang-editor-header
    page-title="《翦商》OCR 手工校订：{html.escape(mapping.title, quote=True)}"
    page-subtitle="原书阅读器页 {mapping.pdf_start:03d}-{mapping.pdf_end:03d} · 原书物理 PDF 页 {mapping.source_start:03d}-{mapping.source_end:03d} · 印刷页 {mapping.printed_start}-{mapping.printed_end} · 输出 {html.escape(output_name, quote=True)}"
    reference-href="../reference_tables.html">
    <noscript>此编辑器需要启用 JavaScript。</noscript>
  </jianshang-editor-header>
  <main>
    <div class="layout">
      <aside>
        <section class="panel"><h2>页码说明</h2><div class="page-number-legend"><p><strong>原阅</strong> {mapping.pdf_start:03d}-{mapping.pdf_end:03d}：原书在阅读器中显示的页码</p><p><strong>原PDF</strong> {mapping.source_start:03d}-{mapping.source_end:03d}：原书文件的物理页码</p><p><strong>印</strong> {mapping.printed_start}-{mapping.printed_end}：书页印刷页码</p><p><strong>注音PDF</strong> {annotated_page_label}：独立重排页码，不与原书逐页对应</p></div></section>
        <section class="panel"><h2>页</h2><div class="nav-list">{''.join(nav_buttons)}</div></section>
        <section class="panel"><h2>参考表</h2><div class="nav-list">{''.join(reference_buttons)}</div></section>
        <section class="panel"><h2>术语</h2><div class="term-list">{term_items}</div></section>
      </aside>
      <section>
        <jianshang-editor-toc current-chapter="{chapter}">
          <noscript>目录需要启用 JavaScript。</noscript>
        </jianshang-editor-toc>
        <div class="reference-grid">{reference_tables}</div>
        <div class="pages">{''.join(pages)}</div>
        <section class="notes-dock" id="notes">
          <h2>编辑札记</h2>
          <div class="note-grid">
            <div class="note-controls">
              <label>页<select id="notePage"></select></label>
              <div class="marker-composer" id="markerComposer">
                <h3>标记</h3>
                <label>类型<select id="markerType">
                  <option value="pinyin">注音</option>
                  <option value="editor-note">编者注／脚注</option>
                  <option value="inline-note">按语</option>
                  <option value="pending">待核</option>
                  <option value="user-note">用户札记</option>
                </select></label>
                <label>内容<input id="markerText" type="text" autocomplete="off" placeholder="输入拼音或笔记内容"></label>
                <p class="marker-help" id="markerHelp">先在正文中选择文字，再输入拼音；可用“拼音；简注”。</p>
                <div class="note-actions"><button id="applyMarkerBtn" type="button">应用标记</button></div>
              </div>
              <label>工作日志标签<input id="noteTag" type="text" value="校订" autocomplete="off"></label>
              <textarea id="noteText" spellcheck="false"></textarea>
              <div class="note-actions">
                <button id="addNoteBtn" type="button">记录到编辑日志</button>
                <button id="exportLogBtn" type="button">导出日志</button>
                <button id="downloadLogBtn" type="button">下载日志</button>
                <button id="clearLogBtn" type="button">清空日志</button>
              </div>
            </div>
            <div><div id="logList" class="log-list"></div></div>
          </div>
        </section>
        <section class="export-dock"><h2>导出文本</h2><textarea id="exportText" spellcheck="false"></textarea></section>
      </section>
    </div>
  </main>
  <button class="quick-note-jump" type="button" data-target="notes">札记</button>
  <script>
    const STORAGE_KEY = {json.dumps(storage_key)};
    const LOG_KEY = {json.dumps(log_key)};
    const OUTPUT_NAME = {json.dumps(output_name)};
    const LOG_NAME = {json.dumps(log_name)};
    const BACKUP_NAME = {json.dumps(backup_name)};
    const CHAPTER_NOTES_NAME = {json.dumps(f'{chapter}_reading_notes.md')};
    const CHAPTER_NOTES_KEY = `${{STORAGE_KEY}}:chapter-notes`;
    const DICTIONARY_SETTINGS_KEY = 'jianshang:dictionary-settings:v1';
    const PROJECT_DICTIONARY_OVERRIDES_KEY = 'reading-lexicon-entry-overrides-v1';
    const STATIC_CHAPTER_NOTES = {json.dumps(load_reading_notes(chapter), ensure_ascii=False)};
    const TERMS = {json.dumps(combined_terms, ensure_ascii=False)};
    const ORIGINAL_TEXTS = {json.dumps(original_texts, ensure_ascii=False)};
    const statusEl = document.getElementById('status');
    const exportTextEl = document.getElementById('exportText');
    const notePageEl = document.getElementById('notePage');
    const noteTagEl = document.getElementById('noteTag');
    const noteTextEl = document.getElementById('noteText');
    const markerTypeEl = document.getElementById('markerType');
    const markerTextEl = document.getElementById('markerText');
    const markerHelpEl = document.getElementById('markerHelp');
    const logListEl = document.getElementById('logList');
    const userNotesBodyEl = document.getElementById('userNotesBody');
    const modeBadgeEl = document.getElementById('modeBadge');
    const chapterNotesBodyEl = document.getElementById('chapterNotesBody');
    const chapterNoteTitleEl = document.getElementById('chapterNoteTitle');
    const chapterNoteTextEl = document.getElementById('chapterNoteText');
    let activeArea = null;
    let viewMode = 'clean';
    let cleanViewTexts = {{}};
    let cleanViewHtml = {{}};
    let voices = [];
    let allowSave = true;
    let savedFormatRange = null;
    function setStatus(text, tone = '') {{ statusEl.textContent = text; statusEl.style.color = tone === 'ok' ? 'var(--ok)' : tone === 'warn' ? 'var(--warn)' : 'var(--muted)'; }}
    function textareas() {{ return Array.from(document.querySelectorAll('.rich-editor[data-page]')); }}
    function editorText(area) {{ return area.innerText.replace(/\u00a0/g, ' ').replace(/\\n$/, ''); }}
    function nodeAtOffset(root, wanted) {{
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      let node = walker.nextNode(), remaining = Math.max(0, wanted);
      while (node) {{ if (remaining <= node.data.length) return [node, remaining]; remaining -= node.data.length; node = walker.nextNode(); }}
      return [root, root.childNodes.length];
    }}
    function setEditorSelection(area, start, end = start) {{
      const range = document.createRange();
      const [startNode,startOffset] = nodeAtOffset(area,start), [endNode,endOffset] = nodeAtOffset(area,end);
      range.setStart(startNode,startOffset); range.setEnd(endNode,endOffset);
      const selection = getSelection(); selection.removeAllRanges(); selection.addRange(range);
      area._selectionStart = start; area._selectionEnd = end; savedFormatRange = range.cloneRange();
    }}
    function captureEditorSelection(area) {{
      const selection = getSelection();
      if (!selection?.rangeCount || !area.contains(selection.anchorNode)) return;
      const range = selection.getRangeAt(0), before = range.cloneRange();
      before.selectNodeContents(area); before.setEnd(range.startContainer,range.startOffset);
      area._selectionStart = before.toString().length;
      area._selectionEnd = area._selectionStart + range.toString().length;
      savedFormatRange = range.cloneRange(); activeArea = area; notePageEl.value = area.dataset.page;
    }}
    function initializeRichEditor(area) {{
      area._selectionStart = area._selectionEnd = 0;
      Object.defineProperty(area,'value',{{get:()=>editorText(area),set:value=>{{const projection=area._imageProjection?.items||[];area._imageProjection=null;area.textContent=String(value);[...projection].reverse().forEach(item=>{{const [node,offset]=nodeAtOffset(area,Math.min(item.offset,area.innerText.length)),range=document.createRange();range.setStart(node,offset);range.collapse(true);range.insertNode(item.figure)}});}}}});
      Object.defineProperty(area,'selectionStart',{{get:()=>area._selectionStart||0}});
      Object.defineProperty(area,'selectionEnd',{{get:()=>area._selectionEnd||0}});
      Object.defineProperty(area,'readOnly',{{get:()=>area.contentEditable==='false',set:value=>{{area.contentEditable=value?'false':'true';}}}});
      area.setSelectionRange=(start,end=start)=>setEditorSelection(area,start,end);
      area.setRangeText=(replacement,start=area.selectionStart,end=area.selectionEnd,mode='end')=>{{setEditorSelection(area,start,end);const range=getSelection().getRangeAt(0);range.deleteContents();const node=document.createTextNode(replacement);range.insertNode(node);const position=mode==='select'?start:start+replacement.length;setEditorSelection(area,mode==='select'?start:position,mode==='select'?start+replacement.length:position);}};
    }}
    function getLog() {{ try {{ return JSON.parse(localStorage.getItem(LOG_KEY) || '[]'); }} catch {{ return []; }} }}
    function setLog(items) {{ localStorage.setItem(LOG_KEY, JSON.stringify(items.slice(0, 300))); renderLog(); }}
    function getChapterNotes() {{ try {{ const notes = JSON.parse(localStorage.getItem(CHAPTER_NOTES_KEY) || '[]'); return Array.isArray(notes) ? notes : []; }} catch {{ return []; }} }}
    function setChapterNotes(notes) {{ localStorage.setItem(CHAPTER_NOTES_KEY, JSON.stringify(notes)); renderChapterNotes(); }}
    function allChapterNotes() {{ return [...STATIC_CHAPTER_NOTES.map(([title,note]) => ({{title,note,source:'file'}})), ...getChapterNotes().map(item => ({{...item,source:'browser'}}))]; }}
    function renderChapterNotes() {{
      const notes = allChapterNotes();
      if (!notes.length) {{ chapterNotesBodyEl.innerHTML = '<tr><td colspan="3">暂无章节导读札记</td></tr>'; return; }}
      chapterNotesBodyEl.innerHTML = notes.map((item,index) => `<tr><td>${{escapeHtml(item.title)}}</td><td>${{escapeHtml(item.note)}}</td><td>${{item.source === 'browser' ? `<button type="button" data-delete-chapter-note="${{index - STATIC_CHAPTER_NOTES.length}}">删除</button>` : '<span class="log-meta">文件</span>'}}</td></tr>`).join('');
      chapterNotesBodyEl.querySelectorAll('[data-delete-chapter-note]').forEach(button => button.addEventListener('click', () => {{
        if (!confirm('删除这条浏览器札记？')) return;
        const notes = getChapterNotes();
        notes.splice(Number(button.dataset.deleteChapterNote), 1);
        setChapterNotes(notes);
        addLog('删除章节导读札记', '', currentPage());
      }}));
    }}
    function chapterNotesMarkdown() {{ return allChapterNotes().map(item => `## ${{item.title}}\\n\\n${{item.note}}`).join('\\n\\n') + '\\n'; }}
    function countChars() {{ return textareas().reduce((sum, area) => sum + area.value.length, 0); }}
    function currentPage() {{ const selected = textareas().find(area => {{ const rect = area.getBoundingClientRect(); return rect.top >= 0 && rect.top < window.innerHeight * .65; }}); return selected?.dataset.page || notePageEl.value || {json.dumps(f'{mapping.pdf_start:03d}')}; }}
    function addLog(action, detail = '', page = currentPage()) {{ const items = getLog(); items.unshift({{ at: new Date().toISOString(), action, page, detail, chars: countChars(), pages: textareas().length }}); setLog(items); }}
    function escapeHtml(text) {{ return String(text).replace(/[&<>"']/g, ch => ({{ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }}[ch])); }}
    function renderLog() {{ const items = getLog(); if (!items.length) {{ logListEl.innerHTML = '<div class="log-meta">暂无记录</div>'; return; }} logListEl.innerHTML = items.map(item => {{ const time = new Date(item.at).toLocaleString(); const page = item.page ? `PDF ${{item.page}}` : '全章'; const detail = item.detail ? `<div class="log-note">${{escapeHtml(item.detail)}}</div>` : ''; return `<div class="log-item"><div class="log-meta">${{time}} · ${{escapeHtml(item.action)}} · ${{page}} · ${{item.chars || 0}}字</div>${{detail}}</div>`; }}).join(''); }}
    function populateNotePages() {{ notePageEl.innerHTML = textareas().map(area => `<option value="${{area.dataset.page}}">PDF ${{area.dataset.page}}</option>`).join(''); }}
    function cleanValueFor(area) {{ if(viewMode==='annotated')return cleanViewTexts[area.dataset.page]??area.value;const clone=area.cloneNode(true);clone.querySelectorAll('.editorial-image').forEach(image=>image.remove());return clone.innerText.replace(/\\n$/,''); }}
    function editorText(area) {{ const figures=[...area.querySelectorAll('.editorial-image')],projection=[];figures.forEach(figure=>{{const range=document.createRange();range.selectNodeContents(area);range.setEndBefore(figure);const clone=figure.cloneNode(true);clone.querySelector('.editorial-image-tools')?.remove();projection.push({{offset:range.toString().length,figure:clone}})}});const token={{items:projection}};area._imageProjection=token;queueMicrotask(()=>{{if(area._imageProjection===token)area._imageProjection=null}});const clone=area.cloneNode(true);clone.querySelectorAll('.editorial-image').forEach(image=>image.remove());return clone.innerText.replace(/\\n$/,''); }}
    function collectUserNotes() {{
      const notes = [];
      textareas().forEach(area => {{
        const source = cleanValueFor(area);
        const patterns = [
          ['编者注', /^〔编者注(\\d+)〕\\s*(.*)$/gm, match => `编者注${{match[1]}}`, match => match[2]],
          ['按语', /〔按语：([^〕]*)〕/g, () => '按语', match => match[1]],
          ['待核', /〔待核：([^〕]*)〕/g, () => '待核', match => match[1]],
          ['札记', /〔札记：([^〕]*)〕/g, () => '札记', match => match[1]],
        ];
        patterns.forEach(([_kind, pattern, label, content]) => {{
          for (const match of source.matchAll(pattern)) notes.push({{ page:area.dataset.page, index:match.index, type:label(match), content:content(match).trim() }});
        }});
      }});
      return notes.sort((a,b) => Number(a.page) - Number(b.page) || a.index - b.index);
    }}
    function renderUserNotes() {{
      const notes = collectUserNotes();
      if (!notes.length) {{ userNotesBodyEl.innerHTML = '<tr><td colspan="3">暂无用户札记</td></tr>'; return; }}
      userNotesBodyEl.innerHTML = notes.map(note => `<tr><td>${{escapeHtml(note.type)}}</td><td><button type="button" class="user-note-jump" data-note-page="${{note.page}}">PDF ${{note.page}}</button></td><td>${{escapeHtml(note.content)}}</td></tr>`).join('');
      userNotesBodyEl.querySelectorAll('[data-note-page]').forEach(button => button.addEventListener('click', () => {{
        const area = document.querySelector(`.rich-editor[data-page="${{button.dataset.notePage}}"]`);
        document.getElementById(`page-${{button.dataset.notePage}}`)?.scrollIntoView({{ behavior:'smooth', block:'start' }});
        if (area) {{ activeArea = area; setTimeout(() => area.focus(), 350); }}
      }}));
    }}
    function saveNow(record = true) {{ if (!allowSave) return; const texts = {{}}, html = {{}}; textareas().forEach(area => {{ const page=area.dataset.page;texts[page]=cleanValueFor(area);html[page]=viewMode==='clean'?area.innerHTML:(cleanViewHtml[page]??''); }}); localStorage.setItem(STORAGE_KEY, JSON.stringify({{ version:4, savedAt:new Date().toISOString(), texts, html }})); setStatus('已保存 ' + new Date().toLocaleTimeString(), 'ok'); if (record) addLog('保存', '', currentPage()); }}
    function loadSaved() {{ try {{ const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{}}'); if (!saved.texts && !saved.html) return; textareas().forEach(area => {{ const page=area.dataset.page;if(saved.version>=4&&saved.html?.[page]!==undefined)area.innerHTML=saved.html[page];else if(saved.texts?.[page]!==undefined)area.value=saved.texts[page]; }}); setStatus(saved.version>=4?'已载入富文本保存稿':'已迁移旧版保存稿', 'ok'); }} catch {{}} }}
    let timer = null; function queueSave() {{ setStatus('正在编辑', 'warn'); clearTimeout(timer); timer = setTimeout(() => saveNow(false), 900); }}
    function blockFor(area) {{ return `===== PDF page ${{area.dataset.page}} / printed page ${{Number(area.dataset.page) - {mapping.pdf_start - mapping.printed_start}}} =====\\n\\n${{cleanValueFor(area).trim()}}`; }}
    function buildText() {{ return textareas().map(blockFor).join('\\n\\n'); }}
    function downloadText(filename, text) {{ const blob = new Blob([text + '\\n'], {{ type: 'text/plain;charset=utf-8' }}); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = filename; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url); }}
    function downloadJson(filename, data) {{ const blob = new Blob([JSON.stringify(data, null, 2)], {{ type: 'application/json;charset=utf-8' }}); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = filename; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url); }}
    function requireCleanArea() {{ if (viewMode !== 'clean') {{ setStatus('请先切换回清稿再编辑', 'warn'); return null; }} const area = activeArea || textareas()[0]; if (!area) return null; area.focus(); return area; }}
    function replaceSelection(replacement) {{ const area = requireCleanArea(); if (!area) return; const start = area.selectionStart, end = area.selectionEnd; area.setRangeText(replacement, start, end, 'end'); area.dispatchEvent(new Event('input', {{ bubbles:true }})); }}
    function selectedText(area) {{ return area.value.slice(area.selectionStart, area.selectionEnd); }}
    function nextFootnoteNumber() {{ const matches = buildText().match(/\\[\\[editor-fn:(\\d+)\\]\\]/g) || []; return matches.reduce((max, marker) => Math.max(max, Number(marker.match(/\\d+/)[0])), 0) + 1; }}
    function locateTerm(term) {{ const ordered = activeArea ? [activeArea, ...textareas().filter(area => area !== activeArea)] : textareas(); for (const area of ordered) {{ let index = area.value.indexOf(term, area === activeArea ? area.selectionEnd : 0); if (index < 0) index = area.value.indexOf(term); if (index >= 0) {{ activeArea = area; area.focus(); area.setSelectionRange(index, index + term.length); area.scrollIntoView({{ behavior:'smooth', block:'center' }}); return area; }} }} return null; }}
    function addNotation(term = '', pinyin = '') {{ let area = requireCleanArea(); if (!area) return; if (term) area = locateTerm(term); const selected = area ? selectedText(area) : ''; if (!selected) {{ setStatus(term ? `正文中找不到“${{term}}”` : '请先选择要注音的文字', 'warn'); return; }} const start = area.selectionStart, end = area.selectionEnd; const reading = pinyin || prompt(`“${{selected}}”的拼音：`, '') || ''; if (!reading) return; const note = prompt('简注（可留空）：', '') || ''; area.setRangeText(`${{selected}}（${{reading}}${{note ? '；' + note : ''}}）`, start, end, 'end'); area.dispatchEvent(new Event('input', {{ bubbles:true }})); addLog('添加注音', selected, area.dataset.page); }}
    function addFootnote() {{ const area = requireCleanArea(); if (!area) return; const number = nextFootnoteNumber(); const note = prompt(`编者注 ${{number}} 内容：`, ''); if (!note) return; const selected = selectedText(area); replaceSelection(`${{selected}}[[editor-fn:${{number}}]]`); area.insertAdjacentText('beforeend', `\n\n〔编者注${{number}}〕${{note}}`); area.dispatchEvent(new Event('input', {{ bubbles:true }})); addLog('添加编者注', note, area.dataset.page); }}
    function addComment() {{ const area = requireCleanArea(); if (!area) return; const note = prompt('按语或评论：', ''); if (!note) return; const selected = selectedText(area); replaceSelection(selected ? `${{selected}}\n\n〔按语：${{note}}〕` : `\n\n〔按语：${{note}}〕`); addLog('插入按语', note, area.dataset.page); }}
    function markDoubt() {{ const area = requireCleanArea(); if (!area) return; const selected = selectedText(area); if (!selected) {{ setStatus('请先选择待核文字', 'warn'); return; }} const reason = prompt('待核原因（可留空）：', '') || ''; replaceSelection(`〔待核：${{selected}}${{reason ? '；' + reason : ''}}〕`); addLog('标为待核', `${{selected}} ${{reason}}`.trim(), area.dataset.page); }}
    function addUserNote() {{ const area = requireCleanArea(); if (!area) return; const note = prompt('用户札记：', ''); if (!note) return; const selected = selectedText(area); replaceSelection(`${{selected}}${{selected ? '\\n\\n' : ''}}〔札记：${{note}}〕`); addLog('添加札记', note, area.dataset.page); }}
    const markerGuidance = {{
      'pinyin': ['先在正文中选择文字，再输入拼音；可用“拼音；简注”。', '输入拼音或“拼音；简注”'],
      'editor-note': ['选择关联文字（可选），输入编者注内容；系统会自动编号并建立脚注标记。', '输入编者注内容'],
      'inline-note': ['选择关联文字（可选），输入随文按语。', '输入按语内容'],
      'pending': ['先选择待核文字；内容可填写待核原因。', '输入待核原因（可留空）'],
      'user-note': ['选择关联文字（可选），输入个人札记；札记会出现在“用户札记”表。', '输入用户札记'],
    }};
    function updateMarkerGuidance() {{ const [help, placeholder] = markerGuidance[markerTypeEl.value]; markerHelpEl.textContent = help; markerTextEl.placeholder = placeholder; }}
    function markerArea() {{ const chosen = document.querySelector(`.rich-editor[data-page="${{notePageEl.value}}"]`); return activeArea || chosen || textareas()[0]; }}
    function applyMarker() {{
      const area = markerArea();
      if (!area || viewMode !== 'clean') {{ setStatus('请先切换回清稿再添加标记', 'warn'); return; }}
      activeArea = area;
      const type = markerTypeEl.value;
      const content = markerTextEl.value.trim();
      const selected = selectedText(area);
      const start = area.selectionStart;
      const end = area.selectionEnd;
      let replacement = selected;
      let action = '';
      let detail = content;
      if (type === 'pinyin') {{
        if (!selected) {{ setStatus('请先选择要注音的文字', 'warn'); return; }}
        if (!content) {{ setStatus('请输入拼音', 'warn'); return; }}
        const [reading, ...noteParts] = content.split('；');
        const note = noteParts.join('；').trim();
        replacement = `${{selected}}（${{reading.trim()}}${{note ? '；' + note : ''}}）`;
        action = '添加注音';
        detail = selected;
      }} else if (type === 'editor-note') {{
        if (!content) {{ setStatus('请输入编者注内容', 'warn'); return; }}
        const number = nextFootnoteNumber();
        replacement = `${{selected}}[[editor-fn:${{number}}]]`;
        area.setRangeText(replacement, start, end, 'end');
        area.insertAdjacentText('beforeend', `\n\n〔编者注${{number}}〕${{content}}`);
        action = '添加编者注';
      }} else if (type === 'inline-note') {{
        if (!content) {{ setStatus('请输入按语内容', 'warn'); return; }}
        replacement = `${{selected}}${{selected ? '\\n\\n' : ''}}〔按语：${{content}}〕`;
        action = '插入按语';
      }} else if (type === 'pending') {{
        if (!selected) {{ setStatus('请先选择待核文字', 'warn'); return; }}
        replacement = `〔待核：${{selected}}${{content ? '；' + content : ''}}〕`;
        action = '标为待核';
        detail = `${{selected}} ${{content}}`.trim();
      }} else {{
        if (!content) {{ setStatus('请输入用户札记', 'warn'); return; }}
        replacement = `${{selected}}${{selected ? '\\n\\n' : ''}}〔札记：${{content}}〕`;
        action = '添加札记';
      }}
      if (type !== 'editor-note') area.setRangeText(replacement, start, end, 'end');
      area.dispatchEvent(new Event('input', {{ bubbles:true }}));
      addLog(action, detail, area.dataset.page);
      markerTextEl.value = '';
      setStatus(`${{action}}完成`, 'ok');
      area.focus();
    }}
    function escapeRegExp(text) {{ const specials = new Set([36,40,41,42,43,46,63,91,92,93,94,123,124,125]); return [...text].map(ch => specials.has(ch.charCodeAt(0)) ? String.fromCharCode(92) + ch : ch).join(''); }}
    function dictionarySettings() {{ try {{ return {{ enabled:true, difficulty:3, domain:'all', ...JSON.parse(localStorage.getItem(DICTIONARY_SETTINGS_KEY) || '{{}}') }}; }} catch {{ return {{ enabled:true, difficulty:3, domain:'all' }}; }} }}
    function termIsVisible(item, settings=dictionarySettings()) {{ return settings.enabled && (Number(item.difficulty) || 3) >= Number(settings.difficulty) && (settings.domain === 'all' || item.domain === settings.domain); }}
    function applyDictionarySettings() {{ const settings=dictionarySettings(), button=document.getElementById('dictionaryHintsBtn'), difficulty=document.getElementById('dictionaryDifficulty'), domain=document.getElementById('dictionaryDomain'); button.textContent=settings.enabled?'词典提示：开':'词典提示：关'; button.classList.toggle('active',settings.enabled); button.setAttribute('aria-pressed',String(settings.enabled)); difficulty.value=String(settings.difficulty); domain.value=settings.domain; document.querySelectorAll('button.term').forEach(term=>{{ term.hidden=!termIsVisible({{difficulty:Number(term.dataset.difficulty),domain:term.dataset.domain}},settings); }}); }}
    function saveDictionarySettings(changes) {{ localStorage.setItem(DICTIONARY_SETTINGS_KEY,JSON.stringify({{...dictionarySettings(),...changes}})); applyDictionarySettings(); if(viewMode==='annotated')setView('clean'); }}
    function applyProjectDictionaryOverrides(overrides) {{ TERMS.forEach(item=>{{const saved=overrides[`zh\u0000${{item.term}}`];if(!saved)return;if(saved.pinyin!==undefined)item.pinyin=String(saved.pinyin);if(saved.difficulty!==undefined)item.difficulty=Number(saved.difficulty)||3;if(saved.definition!==undefined)item.annotation=String(saved.definition)}});document.querySelectorAll('button.term').forEach(button=>{{const item=TERMS.find(entry=>entry.term===button.dataset.term);if(!item)return;button.dataset.pinyin=item.pinyin||'';button.dataset.difficulty=String(item.difficulty||3);const parts=button.querySelectorAll('span');if(parts[1])parts[1].textContent=item.pinyin||''}});localStorage.setItem(PROJECT_DICTIONARY_OVERRIDES_KEY,JSON.stringify(overrides));applyDictionarySettings(); }}
    function loadProjectDictionaryOverrides() {{try{{const value=JSON.parse(localStorage.getItem(PROJECT_DICTIONARY_OVERRIDES_KEY)||'{{}}');if(value&&typeof value==='object'&&!Array.isArray(value))applyProjectDictionaryOverrides(value)}}catch{{}}}}
    function annotatedTexts() {{ const result = {{ ...cleanViewTexts }}; const used = new Set(); [...TERMS].filter(item=>termIsVisible(item)).sort((a,b) => (b.term || '').length - (a.term || '').length).forEach(item => {{ const term = (item.term || '').trim(), pinyin = (item.pinyin || '').trim(); if (!term || !pinyin || used.has(term)) return; for (const area of textareas()) {{ const page = area.dataset.page; const pattern = new RegExp(escapeRegExp(term) + '(?:[（(][A-Za-züÜvV:]+[1-5][）)])?'); if (pattern.test(result[page])) {{ result[page] = result[page].replace(pattern, `${{term}}（${{pinyin}}）`); used.add(term); break; }} }} }}); return result; }}
    function setView(mode) {{ if (mode === 'annotated') {{ saveNow(false); cleanViewTexts = Object.fromEntries(textareas().map(area => [area.dataset.page, area.value])); cleanViewHtml = Object.fromEntries(textareas().map(area => [area.dataset.page, area.innerHTML])); const projected = annotatedTexts(); textareas().forEach(area => {{ area.value = projected[area.dataset.page]; area.readOnly = true; area.classList.add('annotated-view'); }}); viewMode = 'annotated'; document.getElementById('viewToggleBtn').textContent = '切换为清稿'; modeBadgeEl.textContent = '当前：注音稿（只读）'; modeBadgeEl.classList.add('annotated'); }} else {{ if (viewMode === 'annotated') textareas().forEach(area => area.innerHTML = cleanViewHtml[area.dataset.page] ?? escapeHtml(cleanViewTexts[area.dataset.page] ?? area.value)); textareas().forEach(area => {{ area.readOnly = false; area.classList.remove('annotated-view'); }}); viewMode = 'clean'; document.getElementById('viewToggleBtn').textContent = '切换为注音稿'; modeBadgeEl.textContent = '当前：清稿'; modeBadgeEl.classList.remove('annotated'); }} sessionStorage.setItem(`${{STORAGE_KEY}}:view`, mode); setStatus(mode === 'annotated' ? '注音稿仅供查看' : '已返回清稿', 'ok'); }}
    function loadVoices() {{ const priority = lang => {{ const code = lang.toLowerCase(); return code.startsWith('en') ? 0 : code.startsWith('zh') ? 1 : code.startsWith('ru') ? 2 : code.startsWith('fr') ? 3 : 4; }}; voices = speechSynthesis.getVoices().sort((a,b) => priority(a.lang) - priority(b.lang) || a.lang.localeCompare(b.lang) || a.name.localeCompare(b.name)); const select = document.getElementById('voiceSelect'); select.innerHTML = '<option value="">系统默认声音</option>' + voices.map((voice,index) => {{ const name = voice.name.length > 24 ? voice.name.slice(0,23) + '…' : voice.name; return `<option value="${{index}}">${{escapeHtml(name)}} — ${{escapeHtml(voice.lang)}}</option>`; }}).join(''); }}
    function speakText() {{ speechSynthesis.cancel(); const area = activeArea || textareas()[0]; if (!area) return; const selection = selectedText(area).trim(); const utterance = new SpeechSynthesisUtterance(selection || area.value); utterance.lang = 'zh-CN'; utterance.rate = Number(document.getElementById('speechRate').value); const index = document.getElementById('voiceSelect').value; if (index !== '') utterance.voice = voices[Number(index)]; utterance.onstart = () => {{ document.getElementById('pauseSpeechBtn').disabled = false; document.getElementById('stopSpeechBtn').disabled = false; setStatus(selection ? '正在朗读所选文字' : `正在朗读 PDF ${{area.dataset.page}}`); }}; utterance.onend = utterance.onerror = () => {{ document.getElementById('pauseSpeechBtn').disabled = true; document.getElementById('stopSpeechBtn').disabled = true; document.getElementById('pauseSpeechBtn').textContent = '暂停'; }}; speechSynthesis.speak(utterance); }}
    function backupState() {{ return {{ version:4, chapter:{json.dumps(chapter)}, savedAt:new Date().toISOString(), texts:Object.fromEntries(textareas().map(area => [area.dataset.page, viewMode === 'clean' ? area.value : cleanViewTexts[area.dataset.page]])), html:Object.fromEntries(textareas().map(area => [area.dataset.page, viewMode === 'clean' ? area.innerHTML : cleanViewHtml[area.dataset.page]])), log:getLog(), chapterNotes:getChapterNotes() }}; }}
    function restoreFormatSelection() {{ if (!savedFormatRange) return false; const selection=getSelection();selection.removeAllRanges();selection.addRange(savedFormatRange);return true; }}
    function applyTextStyle(command,value,label) {{ if(viewMode!=='clean'){{setStatus('请先切换回清稿再设置格式','warn');return}}if(!activeArea||!restoreFormatSelection()||getSelection().isCollapsed){{setStatus('请先选择正文中的文字','warn');return}}document.execCommand('styleWithCSS',false,true);if(!document.execCommand(command,false,value||null)){{setStatus(`浏览器未能应用${{label}}`,'warn');return}}activeArea.dispatchEvent(new Event('input',{{bubbles:true}}));captureEditorSelection(activeArea);addLog(`设置${{label}}`,getSelection().toString(),activeArea.dataset.page);setStatus(`${{label}}已应用`,'ok'); }}
    function prepareImage(file) {{ return new Promise((resolve,reject)=>{{const reader=new FileReader();reader.onerror=()=>reject(new Error('无法读取图片'));reader.onload=()=>{{const image=new Image();image.onerror=()=>reject(new Error('图片格式无法识别'));image.onload=()=>{{const scale=Math.min(1,1800/Math.max(image.width,image.height)),canvas=document.createElement('canvas');canvas.width=Math.max(1,Math.round(image.width*scale));canvas.height=Math.max(1,Math.round(image.height*scale));canvas.getContext('2d').drawImage(image,0,0,canvas.width,canvas.height);const data=canvas.toDataURL('image/jpeg',.86);data.length>2600000?reject(new Error('压缩后的图片仍过大，请选择较小图片')):resolve(data)}};image.src=reader.result}};reader.readAsDataURL(file)}}); }}
    function insertEditorialImage(data,fileName,caption) {{ if(viewMode!=='clean'||!activeArea){{setStatus('请先在清稿正文中放置光标','warn');return}}const figure=document.createElement('figure');figure.className='editorial-image';figure.dataset.size='medium';figure.contentEditable='false';const image=document.createElement('img');image.src=data;image.alt=caption||fileName;const figcaption=document.createElement('figcaption');figcaption.contentEditable='true';figcaption.textContent=caption||fileName;const tools=document.createElement('div');tools.className='editorial-image-tools';tools.innerHTML='<button type="button" data-image-size="small">小</button><button type="button" data-image-size="medium">中</button><button type="button" data-image-size="large">大</button><button type="button" data-image-size="full">通栏</button><button type="button" data-image-remove>删除</button>';figure.append(image,figcaption,tools);let range=savedFormatRange;try{{if(!range||!activeArea.contains(range.commonAncestorContainer))range=null}}catch{{range=null}}if(range){{range.collapse(false);range.insertNode(figure)}}else activeArea.append(figure);activeArea.append(document.createElement('br'));activeArea.dispatchEvent(new Event('input',{{bubbles:true}}));addLog('插入图片',caption||fileName,activeArea.dataset.page);setStatus('图片已插入；可编辑图注并调整大小','ok');}}
    const formatMenu=document.getElementById('formatMenu'),formatMenuBtn=document.getElementById('formatMenuBtn');
    function closeFormatMenu(){{formatMenu.classList.remove('open');formatMenuBtn.setAttribute('aria-expanded','false')}}
    formatMenuBtn.addEventListener('click',event=>{{event.stopPropagation();const opening=!formatMenu.classList.contains('open');closeFormatMenu();if(opening){{formatMenu.classList.add('open');formatMenuBtn.setAttribute('aria-expanded','true')}}}});
    document.getElementById('formatPopover').addEventListener('click',event=>{{const option=event.target.closest('.format-option');if(!option)return;applyTextStyle(option.dataset.command,option.dataset.value||null,option.dataset.label);closeFormatMenu()}});
    document.addEventListener('click',event=>{{if(!formatMenu.contains(event.target))closeFormatMenu()}});
    document.addEventListener('keydown',event=>{{if(event.key==='Escape')closeFormatMenu()}});
    document.getElementById('boldBtn').addEventListener('click',()=>applyTextStyle('bold',null,'粗体'));
    document.getElementById('insertImageBtn').addEventListener('click',()=>{{if(viewMode!=='clean'){{setStatus('请先切换回清稿再插入图片','warn');return}}if(!activeArea){{setStatus('请先在正文中放置光标','warn');return}}document.getElementById('editorImageInput').click();}});
    document.getElementById('editorImageInput').addEventListener('change',async event=>{{const file=event.target.files[0];if(!file)return;try{{const caption=prompt('请输入图片说明和来源（可稍后在正文中修改）：',file.name)||file.name;insertEditorialImage(await prepareImage(file),file.name,caption)}}catch(error){{setStatus(error.message,'warn')}}finally{{event.target.value=''}}}});
    document.addEventListener('click',event=>{{const size=event.target.closest('[data-image-size]'),remove=event.target.closest('[data-image-remove]'),figure=event.target.closest('.editorial-image');if(size&&figure){{figure.dataset.size=size.dataset.imageSize;figure.closest('.rich-editor')?.dispatchEvent(new Event('input',{{bubbles:true}}))}}else if(remove&&figure&&confirm('删除这张插图？')){{const area=figure.closest('.rich-editor'),page=area?.dataset.page;figure.remove();area?.dispatchEvent(new Event('input',{{bubbles:true}}));addLog('删除图片','',page)}}}});
    document.querySelectorAll('[data-target]').forEach(button => button.addEventListener('click', () => document.getElementById(button.dataset.target)?.scrollIntoView({{ behavior: 'smooth', block: 'start' }})));
    textareas().forEach(initializeRichEditor);
    textareas().forEach(area => {{ area.addEventListener('input', () => {{ queueSave(); renderUserNotes(); }}); area.addEventListener('focus', () => {{ activeArea = area; notePageEl.value = area.dataset.page; }}); area.addEventListener('click', () => captureEditorSelection(area)); area.addEventListener('keyup', () => captureEditorSelection(area)); area.addEventListener('mouseup', () => captureEditorSelection(area)); area.addEventListener('keydown',event=>{{if(event.key==='Enter'&&viewMode==='clean'){{event.preventDefault();captureEditorSelection(area);area.setRangeText('\\n');area.dispatchEvent(new Event('input',{{bubbles:true}}));}}}}); area.addEventListener('paste',event=>{{if(viewMode!=='clean')return;event.preventDefault();captureEditorSelection(area);area.setRangeText(event.clipboardData.getData('text/plain'));area.dispatchEvent(new Event('input',{{bubbles:true}}));}}); }});
    document.querySelectorAll('button.term').forEach(button => button.addEventListener('click', () => addNotation(button.dataset.term, button.dataset.pinyin)));
    document.getElementById('viewToggleBtn').addEventListener('click', () => setView(viewMode === 'clean' ? 'annotated' : 'clean'));
    document.getElementById('dictionaryHintsBtn').addEventListener('click', () => saveDictionarySettings({{enabled:!dictionarySettings().enabled}}));
    document.getElementById('dictionaryDifficulty').addEventListener('change', event => saveDictionarySettings({{difficulty:Number(event.target.value)}}));
    document.getElementById('dictionaryDomain').addEventListener('change', event => saveDictionarySettings({{domain:event.target.value}}));
    document.getElementById('dictionaryOverridesInput').addEventListener('change',async event=>{{const file=event.target.files[0];if(!file)return;try{{const data=JSON.parse(await file.text()),overrides=data.overrides||data;if(!overrides||typeof overrides!=='object'||Array.isArray(overrides))throw new Error('修订文件格式不正确');applyProjectDictionaryOverrides(overrides);setStatus('共享项目词典修订已导入','ok')}}catch(error){{setStatus('无法导入词典修订：'+error.message,'warn')}}finally{{event.target.value=''}}}});
    document.getElementById('addNotationBtn').addEventListener('click', () => addNotation());
    document.getElementById('addFootnoteBtn').addEventListener('click', addFootnote);
    document.getElementById('addCommentBtn').addEventListener('click', addComment);
    document.getElementById('markDoubtBtn').addEventListener('click', markDoubt);
    document.getElementById('addUserNoteBtn').addEventListener('click', addUserNote);
    document.getElementById('addChapterNoteBtn').addEventListener('click', () => {{
      const title = chapterNoteTitleEl.value.trim();
      const note = chapterNoteTextEl.value.trim();
      if (!title || !note) {{ setStatus('请填写章节札记的主题和内容', 'warn'); return; }}
      const notes = getChapterNotes();
      notes.push({{ title, note, at:new Date().toISOString() }});
      setChapterNotes(notes);
      chapterNoteTitleEl.value = '';
      chapterNoteTextEl.value = '';
      setStatus('章节导读札记已保存', 'ok');
      addLog('新增章节导读札记', title, currentPage());
    }});
    document.getElementById('downloadChapterNotesBtn').addEventListener('click', () => {{
      downloadText(CHAPTER_NOTES_NAME, chapterNotesMarkdown());
      setStatus('章节导读札记 Markdown 已下载', 'ok');
      addLog('下载章节导读札记', '', currentPage());
    }});
    markerTypeEl.addEventListener('change', updateMarkerGuidance);
    notePageEl.addEventListener('change', () => {{
      const area = document.querySelector(`.rich-editor[data-page="${{notePageEl.value}}"]`);
      if (area) activeArea = area;
    }});
    document.getElementById('applyMarkerBtn').addEventListener('click', applyMarker);
    document.getElementById('speakBtn').addEventListener('click', speakText);
    document.getElementById('pauseSpeechBtn').addEventListener('click', event => {{ if (speechSynthesis.paused) {{ speechSynthesis.resume(); event.currentTarget.textContent = '暂停'; }} else {{ speechSynthesis.pause(); event.currentTarget.textContent = '继续'; }} }});
    document.getElementById('stopSpeechBtn').addEventListener('click', () => {{ speechSynthesis.cancel(); document.getElementById('pauseSpeechBtn').textContent = '暂停'; }});
    document.getElementById('speechRate').addEventListener('input', event => document.getElementById('speechRateValue').textContent = Number(event.target.value).toFixed(1) + '×');
    document.getElementById('backupBtn').addEventListener('click', () => {{ downloadJson(BACKUP_NAME, backupState()); setStatus('JSON 备份已下载', 'ok'); addLog('导出备份', '', currentPage()); }});
    document.getElementById('importBackup').addEventListener('change', async event => {{ const file = event.target.files[0]; if (!file) return; try {{ const data = JSON.parse(await file.text()); if (!data.texts && !data.html) throw new Error('备份缺少 texts/html'); if (viewMode === 'annotated') setView('clean'); textareas().forEach(area => {{ const page=area.dataset.page;if(data.version>=4&&data.html?.[page]!==undefined)area.innerHTML=data.html[page];else if(data.texts?.[page]!==undefined)area.value=data.texts[page]; }}); if (Array.isArray(data.log)) setLog(data.log); if (Array.isArray(data.chapterNotes)) setChapterNotes(data.chapterNotes); saveNow(false); setStatus(data.version>=4?'富文本备份已导入':'旧版备份已迁移', 'ok'); addLog('导入备份', file.name, currentPage()); }} catch (error) {{ setStatus('无法导入备份：' + error.message, 'warn'); }} finally {{ event.target.value = ''; }} }});
    document.querySelectorAll('[data-copy-page]').forEach(button => button.addEventListener('click', async () => {{ const area = document.querySelector(`.rich-editor[data-page="${{button.dataset.copyPage}}"]`); await navigator.clipboard.writeText(area.value); setStatus('本页已复制', 'ok'); }}));
    document.querySelectorAll('[data-export-page]').forEach(button => button.addEventListener('click', () => {{ const area = document.querySelector(`.rich-editor[data-page="${{button.dataset.exportPage}}"]`); exportTextEl.value = blockFor(area); exportTextEl.scrollIntoView({{ behavior: 'smooth', block: 'center' }}); }}));
    document.getElementById('saveBtn').addEventListener('click', saveNow);
    document.getElementById('exportBtn').addEventListener('click', () => {{ exportTextEl.value = buildText(); exportTextEl.scrollIntoView({{ behavior: 'smooth', block: 'center' }}); setStatus('文本已生成', 'ok'); addLog('生成文本', '', currentPage()); }});
    document.getElementById('downloadBtn').addEventListener('click', () => {{ downloadText(OUTPUT_NAME, buildText()); setStatus('TXT 已下载', 'ok'); addLog('下载TXT', '', currentPage()); }});
    document.getElementById('addNoteBtn').addEventListener('click', () => {{ const note = noteTextEl.value.trim(); if (!note) {{ setStatus('笔记为空', 'warn'); return; }} const tag = noteTagEl.value.trim() || '校订'; addLog(tag, note, notePageEl.value); noteTextEl.value = ''; setStatus('笔记已记录', 'ok'); }});
    function buildLogText() {{ return getLog().map(item => {{ const time = new Date(item.at).toLocaleString(); const page = item.page ? `PDF ${{item.page}}` : '全章'; return `[${{time}}] ${{item.action}} · ${{page}} · ${{item.chars || 0}}字\\n${{item.detail || ''}}`.trim(); }}).join('\\n\\n'); }}
    document.getElementById('exportLogBtn').addEventListener('click', () => {{ exportTextEl.value = buildLogText(); exportTextEl.scrollIntoView({{ behavior: 'smooth', block: 'center' }}); setStatus('日志已导出', 'ok'); }});
    document.getElementById('downloadLogBtn').addEventListener('click', () => {{ downloadText(LOG_NAME, buildLogText()); setStatus('日志已下载', 'ok'); }});
    document.getElementById('clearLogBtn').addEventListener('click', () => {{ if (!confirm('清空本浏览器保存的编辑日志？')) return; localStorage.removeItem(LOG_KEY); renderLog(); setStatus('日志已清空', 'ok'); }});
    document.getElementById('resetBtn').addEventListener('click', () => {{ if (!confirm('恢复 chapter clean 原稿会清除本浏览器保存的编辑内容。继续？')) return; clearTimeout(timer); allowSave = false; if (viewMode === 'annotated') setView('clean'); textareas().forEach(area => area.value = ORIGINAL_TEXTS[area.dataset.page] ?? ''); cleanViewTexts = {{ ...ORIGINAL_TEXTS }}; cleanViewHtml = {{}}; localStorage.removeItem(STORAGE_KEY); sessionStorage.removeItem(`${{STORAGE_KEY}}:view`); viewMode = 'clean'; textareas().forEach(area => {{ area.readOnly = false; area.classList.remove('annotated-view'); }}); document.getElementById('viewToggleBtn').textContent = '切换为注音稿'; modeBadgeEl.textContent = '当前：清稿'; modeBadgeEl.classList.remove('annotated'); allowSave = true; setStatus('已恢复 chapter clean 原稿', 'ok'); addLog('恢复 clean 原稿', '', currentPage()); }});
    window.addEventListener('beforeunload', () => {{ if (allowSave) saveNow(false); }});
    populateNotePages();
    updateMarkerGuidance();
    loadSaved();
    renderUserNotes();
    renderChapterNotes();
    activeArea = textareas()[0] || null;
    applyDictionarySettings();
    loadProjectDictionaryOverrides();
    loadVoices();
    if ('onvoiceschanged' in speechSynthesis) speechSynthesis.onvoiceschanged = loadVoices;
    if (sessionStorage.getItem(`${{STORAGE_KEY}}:view`) === 'annotated') setView('annotated');
    renderLog();
  </script>
</body>
</html>
"""


def build_editor(mapping: ChapterMap, extract_pages: bool, force_images: bool, dpi: int) -> Path:
    if extract_pages:
        ensure_page_images(mapping, DEFAULT_PDF, force=force_images, dpi=dpi)
    chunks = load_seed_chunks(mapping)
    write_seed_export(mapping, chunks)
    output = chapter_dir(mapping.chapter) / "editor.html"
    output.write_text(render_editor(mapping, chunks), encoding="utf-8")
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter", default="chapter_01", help="Chapter id such as intro or chapter_01.")
    parser.add_argument("--all", action="store_true", help="Build editors for all mapped chapters.")
    parser.add_argument("--extract-pages", action="store_true", help="Render missing source PDF page images.")
    parser.add_argument("--force-images", action="store_true", help="Re-render page images even when present.")
    parser.add_argument("--dpi", type=int, default=160)
    parser.add_argument("--skip-dictionary-refresh", action="store_true", help="Use the existing generated shared dictionary snapshot.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.skip_dictionary_refresh:
        dictionary_builder = ROOT.parent.parent / "project_dictionary" / "build_dictionary.py"
        subprocess.run([sys.executable, str(dictionary_builder)], check=True, cwd=ROOT.parent.parent)
        print("Refreshed shared project dictionary before building 《翦商》 editors.")
    mappings = load_chapter_map(DEFAULT_MAP)
    reference_output = build_master_reference_page()
    print(f"Wrote {reference_output.relative_to(ROOT)}")
    targets = list(mappings.values()) if args.all else [mappings[args.chapter]]
    for mapping in targets:
        output = build_editor(mapping, args.extract_pages, args.force_images, args.dpi)
        print(f"Wrote {output.relative_to(ROOT)}")
    toc_output = build_shared_toc_component(mappings)
    print(f"Wrote {toc_output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
