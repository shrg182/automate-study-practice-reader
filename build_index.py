#!/usr/bin/env python3
"""Generate the practice reading-editor table of contents."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re


BASE_DIR = Path(__file__).resolve().parent
OUTPUT = BASE_DIR / "index.html"
MOBILE_READER_VERSION = "1.3.0"
COPYRIGHT_YEAR = 2026
COPYRIGHT_HOLDER = "Ruixing"


@dataclass(frozen=True)
class Collection:
    key: str
    title: str
    description: str
    eyebrow: str


COLLECTIONS = {
    "rongzhai_suibi": Collection("rongzhai_suibi", "《容斋随笔》", "南宋笔记短札：原文、来源注释与校读材料", "宋代笔记"),
    "guwen_guanzhi": Collection("guwen_guanzhi", "《古文观止》", "十二卷古代散文选本：原文、来源注释与校读材料", "古文选本"),
    "chinese_wars": Collection("chinese_wars", "中国历代战争", "按历史时期整理的战争条目、年代与存疑说明", "历史年表"),
    "american_civil_war": Collection("american_civil_war", "American Civil War", "1861–1865 battles, classifications, outcomes, and reading notes", "World History"),
    "laozi": Collection("laozi", "《老子》", "道经与德经八十一章选读", "先秦道家"),
    "sunzi": Collection("sunzi", "《孙子兵法》", "兵法十三篇选读", "先秦兵家"),
    "thirty_six_stratagems": Collection("thirty_six_stratagems", "《三十六计》", "六套三十六策选读", "兵法策略"),
    "liaozhai_stories": Collection("liaozhai_stories", "《聊斋志异》", "文言小说选篇与注音校读材料", "文言小说"),
    "shiji": Collection("shiji", "《史记》", "本纪、世家与列传选读", "史传经典"),
    "jianshang": Collection("jianshang", "《翦商》", "章节校读、注释与阅读记录", "历史阅读"),
    "nine_commentaries": Collection("nine_commentaries", "九评", "章节阅读与校读材料", "专题阅读"),
    "marxist_classics": Collection("marxist_classics", "马克思主义经典", "经典文本专题摘录与注释", "理论文献"),
    "ai_course": Collection("ai_course", "AI 课程", "课程文章、讲义与学习笔记", "课程资料"),
}

COLLECTION_ORDER = list(COLLECTIONS)


class HeadingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_h1 = False
        self.in_title = False
        self.h1_parts: list[str] = []
        self.title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "h1" and not self.h1_parts:
            self.in_h1 = True
        elif tag == "title" and not self.title_parts:
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1":
            self.in_h1 = False
        elif tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_h1:
            self.h1_parts.append(data)
        if self.in_title:
            self.title_parts.append(data)


def clean_title(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return re.sub(r"校读编辑器$", "", value).strip()


def editor_title(path: Path) -> str:
    parser = HeadingParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    h1 = clean_title("".join(parser.h1_parts))
    if h1:
        return h1
    title = clean_title("".join(parser.title_parts))
    return title or path.parent.name.replace("_", " ")


def natural_key(path: Path) -> tuple[object, ...]:
    return tuple(int(part) if part.isdigit() else part.casefold() for part in re.split(r"(\d+)", path.as_posix()))


def entry_context(path: Path, collection_key: str) -> str:
    relative = path.relative_to(BASE_DIR / collection_key)
    parts = relative.parts[:-1]
    if collection_key == "rongzhai_suibi" and parts:
        volume = next((part for part in parts if part.startswith("volume_")), "")
        if volume:
            return f"卷{int(volume.split('_')[1])}"
    if collection_key == "jianshang" and parts:
        leaf = parts[-1]
        labels = {"intro": "导言", "afterword": "后记", "epilogue": "尾声"}
        if leaf in labels:
            return labels[leaf]
        match = re.fullmatch(r"chapter_(\d+)", leaf)
        if match:
            return f"第{int(match.group(1))}章"
    if collection_key == "chinese_wars" and parts:
        labels = {
            "01_ancient_xia": "史前与夏", "02_shang": "商朝", "03_western_zhou": "西周",
            "04_spring_autumn": "春秋", "05_warring_states_qin": "战国至秦", "06_qin_han": "秦汉",
            "07_three_kingdoms": "三国", "08_jin_sixteen_kingdoms": "晋与十六国", "09_northern_southern": "南北朝",
            "10_sui": "隋朝", "11_tang": "唐朝", "12_five_dynasties": "五代", "13_northern_song": "北宋",
            "14_song_jin": "宋金战争", "15_mongol_conquests": "蒙古征战", "16_yuan": "元朝", "17_ming": "明朝",
            "18_ming_qing": "明清战争", "19_qing": "清朝", "20_republic_of_china": "中华民国大陆时期", "21_prc": "中华人民共和国时期",
        }
        return labels.get(parts[-1], "战争年表")
    if collection_key == "american_civil_war" and parts:
        return parts[-1] if re.fullmatch(r"186[1-5]", parts[-1]) else "Civil War"
    if collection_key == "ai_course" and "articles" in parts:
        return "课程文章"
    return "阅读材料"


def find_pdf(editor: Path) -> Path | None:
    candidates = sorted(editor.parent.glob("*.pdf"), key=natural_key)
    annotated = [path for path in candidates if "annotated" in path.stem or "study" in path.stem]
    return (annotated or candidates)[0] if candidates else None


def collect_entries() -> dict[str, list[dict[str, str | None]]]:
    grouped: dict[str, list[dict[str, str | None]]] = {key: [] for key in COLLECTION_ORDER}
    for editor in sorted(BASE_DIR.rglob("editor.html"), key=natural_key):
        if editor == OUTPUT:
            continue
        relative = editor.relative_to(BASE_DIR)
        collection_key = relative.parts[0]
        if collection_key not in COLLECTIONS:
            continue
        pdf = find_pdf(editor)
        grouped[collection_key].append(
            {
                "title": editor_title(editor),
                "context": entry_context(editor, collection_key),
                "editor": editor.relative_to(BASE_DIR).as_posix(),
                "pdf": pdf.relative_to(BASE_DIR).as_posix() if pdf else None,
                "search": " ".join((editor_title(editor), relative.as_posix(), COLLECTIONS[collection_key].title)),
                "action_label": "打开编辑器",
                "direct_link": None,
            }
        )
    marx_civil_war = BASE_DIR / "marxist_classics" / "american_civil_war" / "select_readings.html"
    if marx_civil_war.exists():
        grouped["marxist_classics"].append(
            {
                "title": "马克思、恩格斯论美国内战（113篇目录）",
                "context": "专题目录",
                "editor": marx_civil_war.relative_to(BASE_DIR).as_posix(),
                "pdf": None,
                "search": "马克思 恩格斯 美国内战 南北战争 论文 通信 专题目录",
                "action_label": "打开目录",
                "direct_link": "yes",
            }
        )
    nine_sources = BASE_DIR / "nine_commentaries" / "source_index" / "select_readings.html"
    nine_book_pdf = BASE_DIR / "nine_commentaries" / "吴冷西：十年论战——1956-1966中苏关系回忆录.pdf"
    if nine_book_pdf.exists():
        for entry in grouped["nine_commentaries"]:
            if entry["editor"] == "nine_commentaries/chapter_01/editor.html":
                entry["pdf"] = nine_book_pdf.relative_to(BASE_DIR).as_posix()
                entry["pdf_label"] = "原书 PDF"
    if nine_sources.exists():
        grouped["nine_commentaries"].append(
            {
                "title": "中苏论战与九评文献目录（49篇）",
                "context": "专题目录",
                "editor": nine_sources.relative_to(BASE_DIR).as_posix(),
                "pdf": "https://www.marxists.org/chinese/reference-books/sino-soviet-debate/index.htm",
                "pdf_label": "原始目录",
                "search": "九评 中苏论战 中方文献 苏方文献 苏共中央公开信 专题目录",
                "action_label": "打开目录",
                "direct_link": "yes",
            }
        )
    grouped["jianshang"].sort(key=lambda entry: (
        0 if "/intro/" in f"/{entry['editor']}" else
        2 if "/epilogue/" in f"/{entry['editor']}" else
        3 if "/afterword/" in f"/{entry['editor']}" else 1,
        natural_key(Path(str(entry["editor"])))
    ))
    return grouped


def entry_card(entry: dict[str, str | None], number: int) -> str:
    pdf = entry["pdf"]
    href = str(entry["editor"])
    if not entry.get("direct_link"):
        href += "?view=annotated"
    action_label = str(entry.get("action_label") or "打开编辑器")
    pdf_link = (
        f'<a class="secondary" href="{escape(str(pdf), quote=True)}" '
        f'target="_blank" rel="noopener">{escape(str(entry.get("pdf_label") or "PDF"))}</a>'
        if pdf
        else '<span class="action-empty" aria-label="暂无 PDF">—</span>'
    )
    return f'''<article class="entry" data-search="{escape(str(entry['search']).casefold(), quote=True)}" data-editor-path="{escape(str(entry['editor']), quote=True)}">
      <div class="entry-number">{number:02d}</div>
      <div class="entry-copy"><span>{escape(str(entry['context']))}</span><h3><a class="entry-title-link" href="{escape(href, quote=True)}" target="_blank" rel="noopener">{escape(str(entry['title']))}</a></h3></div>
      <div class="entry-reading"><strong>未读</strong><time></time></div>
      <div class="entry-editing"><strong>未编辑</strong><time></time></div>
      <div class="entry-action entry-editor"><a class="primary" href="{escape(href, quote=True)}" target="_blank" rel="noopener">{escape(action_label)}</a></div>
      <div class="entry-action entry-pdf">{pdf_link}</div>
    </article>'''


def build_html(grouped: dict[str, list[dict[str, str | None]]]) -> str:
    total = sum(len(entries) for entries in grouped.values())
    active = [(key, entries) for key, entries in grouped.items() if entries or key in {"guwen_guanzhi", "chinese_wars", "american_civil_war", "laozi", "sunzi", "thirty_six_stratagems"}]
    nav = "".join(
        f'<a href="#{key}"><span>{escape(COLLECTIONS[key].title)}</span><b>{len(entries)}</b></a>'
        for key, entries in active
    )
    sections = []
    running_number = 0
    for key, entries in active:
        collection = COLLECTIONS[key]
        selector_links = {"rongzhai_suibi": "rongzhai_suibi/select_articles.html", "guwen_guanzhi": "guwen_guanzhi/select_articles.html", "chinese_wars": "chinese_wars/select_entries.html", "american_civil_war": "american_civil_war/select_battles.html", "laozi": "laozi/select_chapters.html", "sunzi": "sunzi/select_entries.html", "thirty_six_stratagems": "thirty_six_stratagems/select_entries.html", "nine_commentaries": "nine_commentaries/source_index/select_readings.html", "marxist_classics": "marxist_classics/american_civil_war/select_readings.html"}
        selector_link = (f'<a class="collection-tool" href="{selector_links[key]}">选择更多篇目</a>' if key in selector_links else "")
        resource_links = {
            "jianshang": '<a class="collection-resource" href="jianshang/翦商.pdf" target="_blank" rel="noopener">原书 PDF</a>',
        }.get(key, "")
        resources_block = f'<div class="collection-resources">{resource_links}</div>' if resource_links else ""
        cards = []
        for entry in entries:
            running_number += 1
            cards.append(entry_card(entry, running_number))
        sections.append(f'''<section class="collection" id="{key}" data-collection>
  <header class="collection-header">
    <button class="collection-toggle" type="button" aria-expanded="true" aria-controls="{key}-entries"><span class="collection-toggle-copy"><span class="collection-eyebrow">{escape(collection.eyebrow)}</span><span class="collection-title">{escape(collection.title)}</span><span class="collection-description">{escape(collection.description)}</span></span><i aria-hidden="true">▾</i></button>
    <div class="collection-meta">{selector_link}<strong>{len(entries)} 篇</strong></div>
  </header>
{resources_block}
  <div class="entries" id="{key}-entries">{"".join(cards)}</div>
</section>''')
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>校读书斋 · 阅读编辑器目录</title>
<style>
:root{{--ink:#25231f;--muted:#716d64;--paper:#f8f5ed;--panel:#fffdf8;--line:#d9d2c4;--red:#83372f;--blue:#315b73;--gold:#b28335}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:#e9e4d9;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Noto Sans CJK SC",sans-serif}}
a{{color:inherit}}.masthead{{background:#27251f;color:#fff}}.masthead-inner{{width:min(1180px,calc(100% - 36px));margin:auto;padding:64px 0 50px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:40px;align-items:end}}
.kicker{{margin:0 0 12px;color:#d8b775;font-size:12px;font-weight:750;letter-spacing:.22em;text-transform:uppercase}}h1{{margin:0;font:700 clamp(36px,6vw,72px)/1.05 "Songti SC","STSong",serif;letter-spacing:.02em}}.lede{{max-width:650px;margin:18px 0 0;color:#d9d4ca;font-size:16px;line-height:1.75}}
.count{{min-width:150px;padding:20px 22px;border:1px solid #ffffff2d;border-radius:10px;background:#ffffff0b}}.count b{{display:block;font:700 44px/1 Georgia,serif;color:#f1d293}}.count span{{color:#cfc9bd;font-size:13px}}
.shell{{width:min(1180px,calc(100% - 36px));margin:0 auto 70px}}.controls{{position:sticky;top:0;z-index:5;display:grid;grid-template-columns:minmax(240px,1fr) minmax(0,2fr);gap:14px;margin:0 -12px;padding:16px 12px;background:#e9e4d9ed;backdrop-filter:blur(10px)}}
.search{{display:flex;align-items:center;gap:10px;padding:0 14px;background:var(--panel);border:1px solid var(--line);border-radius:8px}}.search svg{{width:18px;color:var(--muted)}}.search input{{width:100%;height:46px;border:0;outline:0;background:transparent;color:var(--ink);font-size:15px}}
.collection-nav{{display:flex;gap:7px;overflow:auto;padding-bottom:1px;scrollbar-width:thin}}.collection-nav a{{display:flex;gap:10px;align-items:center;white-space:nowrap;padding:10px 13px;border:1px solid var(--line);border-radius:8px;background:var(--panel);text-decoration:none;font-size:13px}}.collection-nav a:hover{{border-color:var(--red);color:var(--red)}}.collection-nav b{{display:grid;min-width:24px;height:24px;place-items:center;border-radius:12px;background:#eee8dc;font-size:11px}}
.collection{{margin-top:34px;scroll-margin-top:90px}}.collection-header{{display:flex;justify-content:space-between;gap:25px;align-items:end;padding:0 3px 15px;border-bottom:2px solid var(--ink)}}.collection-eyebrow{{margin:0 0 6px!important;color:var(--red)!important;font-size:11px!important;font-weight:800;letter-spacing:.16em}}.collection-title{{margin:0!important;color:inherit!important;font:700 28px/1.25 "Songti SC","STSong",serif!important}}.collection-description{{display:block;margin-top:7px;color:var(--muted);font-size:13px}}.collection-header strong{{white-space:nowrap;color:var(--muted);font-size:13px}}.collection-toggle{{display:flex;min-width:0;flex:1;align-items:center;justify-content:space-between;gap:16px;padding:0;border:0;background:transparent;color:inherit;text-align:left;cursor:pointer}}.collection-toggle-copy{{display:block;min-width:0}}.collection-toggle i{{font-style:normal;font-size:18px;transition:transform .2s}}.collection.collapsed .collection-toggle i{{transform:rotate(-90deg)}}.collection.collapsed .entries,.collection.collapsed .collection-resources{{display:none}}
.collection-meta{{display:flex;gap:10px;align-items:center}}.collection-tool,.collection-resource{{padding:7px 10px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--red);text-decoration:none;font-size:12px;font-weight:700}}.collection-resources{{padding:8px 12px;border:1px solid var(--line);border-bottom:0;background:#fff}}
.entries{{background:var(--panel);border:1px solid var(--line);border-top:0}}.entry{{display:grid;grid-template-columns:54px minmax(0,1fr) auto;gap:16px;align-items:center;min-height:84px;padding:13px 17px;border-bottom:1px solid #e6e0d5}}.entry:last-child{{border-bottom:0}}.entry:hover{{background:#f7f1e6}}.entry-number{{color:#a49b8c;font:600 12px/1 Georgia,serif}}.entry-copy span{{color:var(--blue);font-size:11px;font-weight:750;letter-spacing:.06em}}.entry-copy h3{{margin:5px 0 0;font:650 18px/1.35 "Songti SC","STSong",serif}}
.entry-actions{{display:flex;gap:7px}}.entry-actions a{{padding:8px 11px;border-radius:6px;text-decoration:none;font-size:12px;font-weight:700}}.entry-actions .primary{{background:var(--red);color:#fff}}.entry-actions .primary:hover{{background:#692a25}}.entry-actions .secondary{{border:1px solid var(--line);background:#fff}}.entry-actions .secondary:hover{{border-color:var(--blue);color:var(--blue)}}
.empty{{display:none;margin:70px 0;padding:28px;text-align:center;color:var(--muted);background:var(--panel);border:1px dashed var(--line)}}footer{{padding:36px 18px;text-align:center;color:var(--muted);font-size:12px}}
@media(max-width:760px){{.masthead-inner{{grid-template-columns:1fr;padding-top:45px}}.count{{display:none}}.controls{{grid-template-columns:1fr}}.entry{{grid-template-columns:38px 1fr}}.entry-actions{{grid-column:2;justify-content:flex-start}}.collection-header span{{display:none}}}}
@media print{{.masthead{{background:#fff;color:#000}}.lede,.controls,.entry-actions,footer{{display:none}}.shell{{width:100%;margin:0}}.collection{{break-inside:avoid}}.entry{{min-height:0;padding:7px 10px}}}}
.collection.collapsed{{display:none}}
/* Google Workspace-inspired catalog shell */
:root{{--ink:#202124;--muted:#5f6368;--paper:#fff;--panel:#fff;--line:#dadce0;--red:#188038;--blue:#1a73e8;--gold:#f9ab00}}
body{{background:#f8f9fa;font-family:Arial,"PingFang SC","Noto Sans CJK SC",sans-serif}}
.masthead{{background:#fff;color:var(--ink);border-bottom:1px solid var(--line)}}
.masthead-inner{{width:100%;padding:14px 24px;grid-template-columns:minmax(0,1fr) auto;gap:24px;align-items:center}}.masthead-books{{grid-column:1/-1;padding-top:8px;border-top:1px solid var(--line)}}.masthead-books .collection-nav{{display:flex;flex-wrap:wrap;overflow:visible}}
.masthead-inner>div:first-child{{position:relative;padding-left:48px}}
.masthead-inner>div:first-child::before{{position:absolute;left:0;top:2px;width:34px;height:34px;border-radius:7px;background:linear-gradient(135deg,#34a853 0 52%,#0f9d58 52%);box-shadow:inset 0 0 0 1px #00000012;content:""}}
.kicker{{margin:0 0 2px;color:#137333;font-size:10px;letter-spacing:.12em}}
h1{{font:500 20px/1.25 Arial,"PingFang SC",sans-serif;letter-spacing:0}}
.lede{{margin:3px 0 0;max-width:none;color:var(--muted);font-size:12px;line-height:1.45}}
.count{{min-width:120px;padding:9px 14px;border:1px solid var(--line);border-radius:18px;background:#e6f4ea}}
.count b{{display:inline;margin-right:6px;color:#137333;font:600 20px/1 Arial,sans-serif}}.count span{{color:#137333;font-size:11px}}
.shell{{width:100%;margin:0 auto 48px;padding:0 18px}}
.controls{{top:0;display:block;margin:0;padding:8px 6px;background:#fff;border-bottom:1px solid var(--line);backdrop-filter:none}}
.search{{height:38px;border-color:var(--line);border-radius:20px;background:#f1f3f4}}.search:focus-within{{background:#fff;box-shadow:0 1px 3px #3c404340}}
.search input{{height:36px;font-size:13px}}.collection-nav{{gap:4px;align-items:center}}
.collection-nav a{{padding:7px 10px;border-color:transparent;border-radius:18px;background:#f1f3f4;font-size:12px}}.collection-nav a:hover{{border-color:#aecbfa;background:#e8f0fe;color:#174ea6}}
.collection-nav b{{height:20px;min-width:20px;background:#fff;font-size:10px}}
.collection{{margin-top:18px;scroll-margin-top:62px}}
.collection-header{{min-height:54px;padding:8px 12px;align-items:center;border:1px solid var(--line);border-bottom:0;background:#f8f9fa}}
.collection-eyebrow{{display:none}}.collection-title{{font:600 16px/1.3 Arial,"PingFang SC",sans-serif!important}}.collection-description{{margin-top:2px;font-size:11px}}
.collection-meta{{gap:8px}}.collection-tool{{padding:7px 11px;border-color:#c4d8f3;border-radius:18px;background:#e8f0fe;color:#174ea6}}
.entries{{border-color:var(--line);box-shadow:0 1px 2px #3c40431a}}
.entry{{grid-template-columns:52px minmax(260px,1fr) 190px;min-height:48px;padding:0;border-color:var(--line);gap:0;background:#fff}}
.entry:hover{{background:#f8fbff}}.entry-number{{align-self:stretch;display:grid;place-items:center;background:#f1f3f4;border-right:1px solid var(--line);color:var(--muted);font:11px Arial,sans-serif}}
.entry-copy{{align-self:stretch;display:grid;grid-template-columns:90px minmax(0,1fr);align-items:center;border-right:1px solid var(--line)}}
.entry-copy span{{margin:0;padding:0 12px;color:#137333;font-size:11px;letter-spacing:0}}.entry-copy h3{{margin:0;padding:9px 12px;border-left:1px solid var(--line);font:500 14px/1.35 Arial,"PingFang SC",sans-serif}}
.entry-title-link{{color:inherit;text-decoration:none}}.entry-title-link:hover{{color:#174ea6;text-decoration:underline;text-underline-offset:3px}}.entry-title-link:focus-visible{{outline:2px solid #1a73e8;outline-offset:3px;border-radius:2px}}
.entry-actions{{padding:6px 9px;justify-content:flex-end;align-items:center}}.entry-actions a{{padding:6px 10px;border-radius:16px;font-size:11px}}.entry-actions .primary{{background:#188038}}.entry-actions .primary:hover{{background:#137333}}
@media(max-width:760px){{.masthead-inner{{padding:12px 16px}}.lede{{display:none}}.shell{{padding:0 8px}}.entry{{grid-template-columns:38px 1fr}}.entry-copy{{grid-template-columns:70px 1fr;border-right:0}}.entry-actions{{grid-column:2;padding:5px 9px;justify-content:flex-start;border-top:1px solid var(--line)}}}}
/* Restore the original book-like catalog when reading mode is selected. */
html[data-workspace-skin="reading"]{{--ink:#25231f;--muted:#716d64;--paper:#f8f5ed;--panel:#fffdf8;--line:#d9d2c4;--red:#83372f;--blue:#315b73;--gold:#b28335}}
html[data-workspace-skin="reading"] body{{background:#e9e4d9;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Noto Sans CJK SC",sans-serif}}
html[data-workspace-skin="reading"] .masthead{{background:#27251f;color:#fff;border:0}}html[data-workspace-skin="reading"] .masthead-inner{{width:min(1180px,calc(100% - 36px));padding:64px 0 50px;align-items:end}}html[data-workspace-skin="reading"] .masthead-inner>div:first-child{{padding-left:0}}html[data-workspace-skin="reading"] .masthead-inner>div:first-child::before{{display:none}}
html[data-workspace-skin="reading"] .kicker{{margin:0 0 12px;color:#d8b775;font-size:12px;letter-spacing:.22em}}html[data-workspace-skin="reading"] h1{{font:700 clamp(36px,6vw,72px)/1.05 "Songti SC","STSong",serif}}html[data-workspace-skin="reading"] .lede{{max-width:650px;margin:18px 0 0;color:#d9d4ca;font-size:16px;line-height:1.75}}
html[data-workspace-skin="reading"] .count{{min-width:150px;padding:20px 22px;border-color:#ffffff2d;border-radius:10px;background:#ffffff0b}}html[data-workspace-skin="reading"] .count b{{display:block;margin:0;color:#f1d293;font:700 44px/1 Georgia,serif}}html[data-workspace-skin="reading"] .count span{{color:#cfc9bd;font-size:13px}}
html[data-workspace-skin="reading"] .shell{{width:min(1180px,calc(100% - 36px));padding:0;margin:0 auto 70px}}html[data-workspace-skin="reading"] .controls{{grid-template-columns:minmax(240px,1fr) minmax(0,2fr);gap:14px;margin:0 -12px;padding:16px 12px;background:#e9e4d9ed;backdrop-filter:blur(10px)}}html[data-workspace-skin="reading"] .search{{height:auto;border-radius:8px;background:var(--panel)}}html[data-workspace-skin="reading"] .search input{{height:46px;font-size:15px}}
html[data-workspace-skin="reading"] .collection-nav{{gap:7px}}html[data-workspace-skin="reading"] .collection-nav a{{padding:10px 13px;border-color:var(--line);border-radius:8px;background:var(--panel);font-size:13px}}html[data-workspace-skin="reading"] .collection-nav b{{height:24px;min-width:24px;background:#eee8dc;font-size:11px}}
html[data-workspace-skin="reading"] .collection{{margin-top:34px;scroll-margin-top:90px}}html[data-workspace-skin="reading"] .collection-header{{padding:0 3px 15px;align-items:end;border:0;border-bottom:2px solid var(--ink);background:transparent}}html[data-workspace-skin="reading"] .collection-eyebrow{{display:block}}html[data-workspace-skin="reading"] .collection-title{{font:700 28px/1.25 "Songti SC","STSong",serif!important}}html[data-workspace-skin="reading"] .collection-description{{margin-top:7px;font-size:13px}}html[data-workspace-skin="reading"] .collection-tool{{border-radius:6px;background:var(--panel);color:var(--red)}}
html[data-workspace-skin="reading"] .entries{{box-shadow:none}}html[data-workspace-skin="reading"] .entry{{grid-template-columns:54px minmax(0,1fr) auto;gap:16px;min-height:84px;padding:13px 17px;border-color:#e6e0d5}}html[data-workspace-skin="reading"] .entry-number{{display:block;align-self:auto;background:transparent;border:0;color:#a49b8c;font:600 12px/1 Georgia,serif}}html[data-workspace-skin="reading"] .entry-copy{{display:block;align-self:auto;border:0}}html[data-workspace-skin="reading"] .entry-copy span{{padding:0;color:var(--blue);font-size:11px;letter-spacing:.06em}}html[data-workspace-skin="reading"] .entry-copy h3{{margin:5px 0 0;padding:0;border:0;font:650 18px/1.35 "Songti SC","STSong",serif}}html[data-workspace-skin="reading"] .entry-actions{{padding:0}}html[data-workspace-skin="reading"] .entry-actions a{{padding:8px 11px;border-radius:6px;font-size:12px}}html[data-workspace-skin="reading"] .entry-actions .primary{{background:var(--red)}}
/* Separate editor and PDF into aligned spreadsheet columns. */
.entry{{grid-template-columns:52px minmax(260px,1fr) 145px 145px 140px 72px}}
.entry-reading,.entry-editing{{align-self:stretch;display:flex;flex-direction:column;justify-content:center;padding:6px 12px;border-right:1px solid var(--line);color:var(--muted);font-size:11px;line-height:1.35}}.entry-reading strong,.entry-editing strong{{color:#5f6368;font-size:12px}}.entry-reading.read strong,.entry-editing.edited strong{{color:#137333}}.entry-reading time,.entry-editing time{{margin-top:2px;white-space:nowrap}}
.entry-action{{display:flex;align-self:stretch;align-items:center;justify-content:center;padding:6px 8px;border-right:1px solid var(--line)}}.entry-pdf{{border-right:0}}.entry-action a{{padding:6px 10px;border-radius:16px;text-decoration:none;font-size:11px;font-weight:700;white-space:nowrap}}.entry-action .primary{{background:#188038;color:#fff}}.entry-action .primary:hover{{background:#137333}}.entry-action .secondary{{border:1px solid var(--line);background:#fff}}.entry-action .secondary:hover{{border-color:var(--blue);color:var(--blue)}}.action-empty{{color:#9aa0a6}}
html[data-workspace-skin="reading"] .entry{{grid-template-columns:54px minmax(0,1fr) 145px 145px 132px 72px}}html[data-workspace-skin="reading"] .entry-action{{padding:0;border-right:1px solid var(--line)}}html[data-workspace-skin="reading"] .entry-pdf{{border-right:0}}html[data-workspace-skin="reading"] .entry-action a{{padding:8px 11px;border-radius:6px;font-size:12px}}html[data-workspace-skin="reading"] .entry-action .primary{{background:var(--red)}}
@media(max-width:760px){{.entry,html[data-workspace-skin="reading"] .entry{{grid-template-columns:38px minmax(180px,1fr) 125px 125px 126px 62px}}.entry-copy{{border-right:1px solid var(--line)}}.entry-reading,.entry-editing{{padding:5px 7px}}.entry-action{{padding:5px 6px}}}}
@media print{{.entry-action{{display:none}}}}
</style>
<script src="workspace_skin.js"></script>
</head>
<body>
<header class="masthead"><div class="masthead-inner"><div><p class="kicker">Reading workspace</p><h1>校读书斋</h1><p class="lede">文章、古籍与课程材料的阅读编辑器目录。搜索篇名，或按系列进入清稿、注音、脚注、按语与札记工作区。</p></div><div class="count"><b>{total}</b><span>个阅读编辑器</span></div><nav class="masthead-books" aria-label="书目分组"><div class="collection-nav">{nav}</div></nav></div></header>
<main class="shell">
  <div class="controls"><label class="search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg><input id="catalogSearch" type="search" placeholder="搜索文章、篇章或系列…" autocomplete="off"></label></div>
  {"".join(sections)}
  <p class="empty" id="emptyState">没有找到匹配的阅读材料。</p>
</main>
<footer><strong>教育用途说明：</strong>本站仅供个人阅读、校读与学习，不隶属于所引用的原文来源网站；原始资料的权利归其相应权利人所有。<br><span>Mobile Reader v{MOBILE_READER_VERSION} · &copy; {COPYRIGHT_YEAR} {escape(COPYRIGHT_HOLDER)}. All rights reserved.</span><br>目录由 <code>practice/build_index.py</code> 自动生成 · 新增编辑器后重新运行即可更新</footer>
<script>
const search=document.getElementById('catalogSearch'),empty=document.getElementById('emptyState');
const readingHistoryKey='reading-workspace-history-v1',editingHistoryKey='reading-workspace-editing-history-v1';
function setCollectionCollapsed(section,collapsed,persist=true){{section.classList.toggle('collapsed',collapsed);section.querySelector('.collection-toggle')?.setAttribute('aria-expanded',String(!collapsed));if(persist){{const state=JSON.parse(localStorage.getItem('reading-workspace-collapsed-collections')||'{{}}');state[section.id]=collapsed;localStorage.setItem('reading-workspace-collapsed-collections',JSON.stringify(state))}}}}
function installCollectionToggles(){{document.querySelectorAll('[data-collection]').forEach(section=>{{setCollectionCollapsed(section,true,false);section.querySelector('.collection-toggle')?.addEventListener('click',()=>setCollectionCollapsed(section,true,false))}});document.querySelectorAll('.masthead-books a[href^="#"]').forEach(link=>link.addEventListener('click',event=>{{event.preventDefault();const section=document.querySelector(link.getAttribute('href')),opening=section?.classList.contains('collapsed');document.querySelectorAll('[data-collection]').forEach(item=>setCollectionCollapsed(item,true,false));if(opening&&section){{setCollectionCollapsed(section,false,false);history.replaceState(null,'',link.getAttribute('href'));section.scrollIntoView({{behavior:'smooth',block:'start'}})}}}}));const linked=location.hash&&document.querySelector(location.hash);if(linked?.matches('[data-collection]'))setCollectionCollapsed(linked,false,false)}}
function filterCatalog(){{const query=search.value.trim().toLocaleLowerCase();let visibleTotal=0;document.querySelectorAll('[data-collection]').forEach(section=>{{let count=0;section.querySelectorAll('.entry').forEach(entry=>{{const show=!query||entry.dataset.search.includes(query);entry.hidden=!show;if(show)count++}});section.hidden=count===0;if(query&&count)setCollectionCollapsed(section,false,false);visibleTotal+=count}});empty.style.display=visibleTotal?'none':'block'}}
function renderReadingHistory(){{let history={{}};try{{history=JSON.parse(localStorage.getItem(readingHistoryKey)||'{{}}')}}catch{{}}const formatter=new Intl.DateTimeFormat('zh-CN',{{year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'}});document.querySelectorAll('.entry[data-editor-path]').forEach(entry=>{{const cell=entry.querySelector('.entry-reading'),record=history[entry.dataset.editorPath];cell.classList.toggle('read',Boolean(record));cell.querySelector('strong').textContent=record?`已读 ${{record.count||1}} 次`:'未读';cell.querySelector('time').textContent=record?.lastRead?formatter.format(new Date(record.lastRead)):''}})}}
function renderEditingHistory(){{let history={{}};try{{history=JSON.parse(localStorage.getItem(editingHistoryKey)||'{{}}')}}catch{{}}const formatter=new Intl.DateTimeFormat('zh-CN',{{year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'}});document.querySelectorAll('.entry[data-editor-path]').forEach(entry=>{{const cell=entry.querySelector('.entry-editing'),record=history[entry.dataset.editorPath];cell.classList.toggle('edited',Boolean(record));cell.querySelector('strong').textContent=record?`已编辑 ${{record.sessions||1}} 次`:'未编辑';cell.querySelector('time').textContent=record?.lastEdited?formatter.format(new Date(record.lastEdited)):'';cell.title=record?`首次编辑：${{formatter.format(new Date(record.firstEdited))}}\n最近编辑：${{formatter.format(new Date(record.lastEdited))}}\n修改批次：${{record.changes||1}}\n内容类型：${{(record.kinds||[]).join('、')||'正文'}}`:''}})}}
function renderHistory(){{renderReadingHistory();renderEditingHistory()}}
search.addEventListener('input',filterCatalog);
document.addEventListener('click',event=>{{if(event.target.closest('.entry-editor a,.entry-title-link'))sessionStorage.setItem('shiji-editor-view','annotated')}});
window.addEventListener('focus',renderHistory);window.addEventListener('storage',renderHistory);installCollectionToggles();renderHistory();
</script>
</body>
</html>'''


def main() -> None:
    grouped = collect_entries()
    OUTPUT.write_text(build_html(grouped), encoding="utf-8")
    total = sum(len(entries) for entries in grouped.values())
    print(f"Wrote {OUTPUT} with {total} editor links")


if __name__ == "__main__":
    main()
