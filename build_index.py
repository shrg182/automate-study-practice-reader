#!/usr/bin/env python3
"""Generate the practice reading-editor table of contents."""

from __future__ import annotations

from dataclasses import dataclass
import csv
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re


BASE_DIR = Path(__file__).resolve().parent
OUTPUT = BASE_DIR / "index.html"
MOBILE_READER_VERSION = "1.15.0"
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
    "news_reports": Collection("news_reports", "News Reports", "English-language news reports, transcripts, and study editions", "Current affairs reading"),
    "reader_articles": Collection("reader_articles", "Reader Articles", "Write, annotate, preview, back up, and export original articles", "Personal authoring workspace"),
    "python": Collection("python", "Python", "Beginning, Intermediate, and Advanced courses by Codex (OpenAI)", "Programming"),
    "russian_poetry": Collection("russian_poetry", "Русская поэзия", "Russian-first poetry readings with concise English study support", "Russian literature"),
    "russian_short_stories": Collection("russian_short_stories", "Русские рассказы", "Short Russian prose: humor, fable, prose miniature, and philosophical sketch", "Russian prose"),
    "russian_wars": Collection("russian_wars", "Войны России", "Russian-first chronicle with selectable English and Chinese study support", "Russian history"),
    "mao_annotated_24_histories": Collection("mao_annotated_24_histories", "《毛泽东批注二十四史》", "九十一册横排简体字本：二十四史、批注、史论与研究资料", "历史典籍"),
    "tcm_foundations": Collection("tcm_foundations", "《中医基础理论》", "原创学习教材：传统理论、现代医学边界、术语与复习", "中医基础课程"),
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
    if collection_key == "russian_short_stories" and parts:
        authors = {
            "01_chekhov_radost": "Антон Чехов · юмористический рассказ",
            "02_turgenev_vorobey": "Иван Тургенев · стихотворение в прозе",
            "03_tolstoy_lev_i_mysh": "Лев Толстой · басня",
            "04_korolenko_ogonki": "Владимир Короленко · философская миниатюра",
        }
        return authors.get(parts[-1], "Русская проза")
    if collection_key == "russian_poetry" and parts:
        authors = {
            "01_pushkin_ya_vas_lyubil": "Александр Пушкин · 1829",
            "02_pushkin_zimnee_utro": "Александр Пушкин · 1829",
            "03_pushkin_uznik": "Александр Пушкин · 1822",
            "04_lermontov_parus": "Михаил Лермонтов · 1832",
            "05_tyutchev_silentium": "Фёдор Тютчев · 1830",
            "06_pushkin_esli_zhizn_tebya_obmanet": "Александр Пушкин · 1825",
            "07_pushkin_k_chaadaevu": "Александр Пушкин · 1818",
            "08_lermontov_vykhozhu_odin": "Михаил Лермонтов · 1841",
            "09_tyutchev_vesennie_vody": "Фёдор Тютчев · 1829",
            "10_fet_ya_prishyol_s_privetom": "Афанасий Фет · 1843",
            "11_fet_shepot": "Афанасий Фет · 1850",
            "12_krylov_strekoza_i_muravey": "Иван Крылов · 1808",
            "13_turgenev_russkiy_yazyk": "Иван Тургенев · 1882",
            "14_blok_noch_ulitsa": "Александр Блок · 1912",
            "15_yesenin_beryoza": "Сергей Есенин · 1913",
            "16_yesenin_do_svidanya": "Сергей Есенин · 1925",
            "17_derzhavin_reka_vremen": "Гавриил Державин · 1816",
            "18_batyushkov_moy_geniy": "Константин Батюшков · 1815",
            "19_nekrasov_seyatelyam": "Николай Некрасов · 1876",
            "20_mayakovsky_poslushayte": "Владимир Маяковский · 1914",
        }
        return authors.get(parts[-1], "Русская поэзия")
    if collection_key == "russian_wars" and parts:
        periods = {
            "period_05_1689_1801": "Период 5 · 1689–1801",
            "period_06_1801_1855": "Период 6 · 1801–1855",
            "period_07_1855_1917": "Период 7 · 1855–1917",
            "period_08_1917_1922": "Период 8 · 1917–1922",
            "period_09_1922_1941": "Период 9 · 1922–1941",
            "period_10_1939_1945": "Период 10 · 1939–1945",
        }
        return periods.get(parts[0], "Хроника войн")
    if collection_key == "python" and parts:
        levels = {"beginning": "Beginning", "intermediate": "Intermediate", "advanced": "Advanced"}
        level = next((levels[part] for part in parts if part in levels), "Python")
        match = re.match(r"(\d+)_", parts[-1])
        return f"{level} · Module {int(match.group(1))}" if match else level
    if collection_key == "tcm_foundations" and parts:
        match = re.match(r"(\d+)_", parts[-1])
        return f"原创教材 · 第{int(match.group(1))}章" if match else "原创教材"
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


def editor_content_search_terms(editor: Path) -> str:
    entries = editor.parent / "entries.csv"
    if not entries.exists():
        return ""
    with entries.open(encoding="utf-8-sig", newline="") as file:
        rows = csv.DictReader(file)
        searchable_fields = ("battle_title", "battle_title_zh", "date_original", "source_note", "notes")
        return " ".join(
            str(row.get(field) or "").strip()
            for row in rows
            for field in searchable_fields
            if str(row.get(field) or "").strip()
        )


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
                "search": " ".join((editor_title(editor), relative.as_posix(), COLLECTIONS[collection_key].title, editor_content_search_terms(editor))),
                "action_label": "打开编辑器",
                "direct_link": None,
            }
        )
    news_items = [
        ("cuba_crisis/cuba_crisis_report_20260520.pdf", "Historical report", "May 20, 2026", "The Cuban Missile Crisis"),
        ("putin_visit_to_china_3/putin_china_visit_report_20260520.pdf", "News report", "May 20, 2026", "Putin’s Visit to China"),
        ("trump_visit_to_china/trump_china_visit_report.pdf", "News report", "May 9, 2026", "Trump’s Visit to China"),
        ("trump_visit_to_china_2/trump_china_visit_report_20260513.pdf", "News report", "May 13, 2026", "Trump’s Visit to China"),
        ("trump_visit_to_china_3/trump_china_visit_report_20260514.pdf", "News report", "May 14, 2026", "Trump’s Visit to China"),
        ("trump_visit_to_china_4/trump_china_visit_report_20260517.pdf", "News report", "May 17, 2026", "Trump’s Visit to China"),
        ("white_house_dinner_security_incident/report.pdf", "News report", "Undated", "White House Dinner Security Incident"),
        ("trump_speech_20260701/trump_speech_reading_packet_20260701.pdf", "Reading packet", "July 1, 2026", "Trump Speech Reading Packet"),
        ("trump_speech_20260701/sectioned_learning_units/trump_speech_learning_units_20260701.pdf", "Learning units", "July 1, 2026", "Trump Speech Learning Units"),
        ("trump_250_speech_20260704/trump_salute_to_america_2026_study_guide.pdf", "Study guide", "July 4, 2026", "Salute to America Speech"),
        ("trump_at_press_conference_20260708/trump_press_conference_20260708_study_report.pdf", "Study report", "July 8, 2026", "Trump Press Conference"),
        ("trump_at_press_conference_20260708/trump_press_conference_20260708_short_5000.pdf", "Reading edition", "July 8, 2026", "Trump Press Conference"),
        ("trump_at_press_conference_20260708/trump_press_conference_20260708_full_transcript.pdf", "Full transcript", "July 8, 2026", "Trump Press Conference"),
        ("trump_iran_live_pdf_20260711/trump_iran_live_study_report_time_under_subtitle.pdf", "Timed study report", "July 11, 2026", "Trump and Iran Live Report"),
        ("trump_recent_news_20260712/trump_recent_news_english_study_20260712.pdf", "Study edition", "July 12, 2026", "Recent Trump News"),
    ]
    for relative, report_type, report_date, title in news_items:
        path = BASE_DIR / "news_reports" / relative
        if not path.exists():
            continue
        href = path.relative_to(BASE_DIR).as_posix()
        grouped["news_reports"].append({
            "title": title,
            "context": f"{report_type} · {report_date}",
            "report_type": report_type,
            "report_date": report_date,
            "editor": href,
            "pdf": None,
            "search": f"{title} {report_type} {report_date} news report transcript study English {relative}",
            "action_label": "Open report",
            "direct_link": "yes",
        })
    studio = BASE_DIR / "reader_articles" / "index.html"
    if studio.exists():
        grouped["reader_articles"].append({
            "title": "Reader Articles Studio",
            "context": "Two-pane writing and PDF workspace",
            "editor": studio.relative_to(BASE_DIR).as_posix(),
            "pdf": None,
            "search": "reader articles studio write author edit two pane PDF backup footnotes annotations",
            "action_label": "Open studio",
            "direct_link": "yes",
        })
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
    if entry.get("report_type"):
        return f'''<article class="entry news-entry" data-search="{escape(str(entry['search']).casefold(), quote=True)}" data-editor-path="{escape(str(entry['editor']), quote=True)}">
      <div class="entry-number">{number:02d}</div>
      <div class="news-type">{escape(str(entry['report_type']))}</div>
      <div class="news-date">{escape(str(entry['report_date']))}</div>
      <div class="news-title"><a class="entry-title-link" href="{escape(href, quote=True)}" target="_blank" rel="noopener">{escape(str(entry['title']))}</a></div>
      <div class="entry-reading"><strong>未读</strong><time></time></div>
      <div class="entry-editing"><strong>未编辑</strong><time></time></div>
      <div class="entry-action entry-editor"><a class="primary" href="{escape(href, quote=True)}" target="_blank" rel="noopener">{escape(action_label)}</a></div>
    </article>'''
    return f'''<article class="entry" data-search="{escape(str(entry['search']).casefold(), quote=True)}" data-editor-path="{escape(str(entry['editor']), quote=True)}">
      <div class="entry-number">{number:02d}</div>
      <div class="entry-copy"><span>{escape(str(entry['context']))}</span><h3><a class="entry-title-link" href="{escape(href, quote=True)}" target="_blank" rel="noopener">{escape(str(entry['title']))}</a></h3></div>
      <div class="entry-reading"><strong>未读</strong><time></time></div>
      <div class="entry-editing"><strong>未编辑</strong><time></time></div>
      <div class="entry-action entry-editor"><a class="primary" href="{escape(href, quote=True)}" target="_blank" rel="noopener">{escape(action_label)}</a></div>
      <div class="entry-action entry-pdf">{pdf_link}</div>
    </article>'''


def marxist_book_groups(entries: list[dict[str, str | None]]) -> list[dict[str, object]]:
    """Arrange Marxist readings as book -> contents -> selected article."""
    groups: list[dict[str, object]] = [
        {
            "key": "american-civil-war",
            "title": "《马克思恩格斯论美国内战》",
            "meta": "马克思、恩格斯 · 1861–1865",
            "contents": "文献目录",
            "catalog_total": 113,
            "tool": "marxist_classics/american_civil_war/select_readings.html",
            "tool_label": "浏览完整目录",
            "prefix": "marxist_classics/american_civil_war/",
        },
        {
            "key": "capital-volume-one",
            "title": "《资本论》第一卷",
            "meta": "卡尔·马克思 · English-first reader",
            "contents": "第一卷完整目录：序言、八篇及三十三章",
            "catalog_total": 37,
            "tool": "marxist_classics/capital/select_readings.html",
            "tool_label": "浏览阅读计划",
            "offline_manifest": "marxist_classics/capital/book_manifest.json",
            "prefix": "marxist_classics/capital/",
        },
        {
            "key": "anti-duhring",
            "title": "《反杜林论》",
            "meta": "弗里德里希·恩格斯 · English-first reader",
            "contents": "完整目录：序言、引论、三编正文及补充材料",
            "catalog_total": 34,
            "tool": "marxist_classics/anti_duhring/select_readings.html",
            "tool_label": "浏览阅读计划",
            "offline_manifest": "marxist_classics/anti_duhring/book_manifest.json",
            "prefix": "marxist_classics/anti_duhring/",
        },
        {
            "key": "proletarian-dictatorship",
            "title": "《马克思恩格斯列宁论无产阶级专政》",
            "meta": "理论语录与注释",
            "contents": "33条语录及注释",
            "prefix": "marxist_classics/proletarian_dictatorship_33_quotes/",
        },
    ]
    for group in groups:
        prefix = str(group.pop("prefix"))
        group["entries"] = [entry for entry in entries if str(entry["editor"]).startswith(prefix)]
    return groups


def marxist_books_html(entries: list[dict[str, str | None]], start_number: int) -> str:
    books = []
    next_number = start_number
    for group in marxist_book_groups(entries):
        selected = list(group["entries"])
        cards = []
        for entry in selected:
            next_number += 1
            cards.append(entry_card(entry, next_number))
        total = group.get("catalog_total")
        count_label = f'已选 {len(selected)} / 全部 {total} 篇' if total else f'已选 {len(selected)} 篇'
        tool = (
            f'<a class="book-tool" href="{escape(str(group["tool"]), quote=True)}">{escape(str(group["tool_label"]))}</a>'
            if group.get("tool") else ""
        )
        tool_line = f"\n      {tool}" if tool else ""
        offline_tools = (
            f'<span class="book-offline-tools"><button type="button" data-offline-manifest="{escape(str(group["offline_manifest"]), quote=True)}" data-offline-book="{escape(str(group["title"]), quote=True)}">保存离线</button>'
            f'<button type="button" data-offline-manifest="{escape(str(group["offline_manifest"]), quote=True)}" data-offline-book="{escape(str(group["title"]), quote=True)}" data-offline-remove="true">移除离线</button></span>'
            if group.get("offline_manifest") else ""
        )
        offline_line = f"\n      {offline_tools}" if offline_tools else ""
        book_search = f"{group['title']} {group['meta']} {group['contents']}".casefold()
        books.append(f'''<section class="book-group" data-book data-search="{escape(book_search, quote=True)}">
    <input class="book-state" id="{group['key']}-book-state" type="checkbox">
    <header class="book-header">
      <label class="book-toggle" for="{group['key']}-book-state"><span><span class="book-level">01 · 书名</span><strong>{escape(str(group['title']))}</strong><small>{escape(str(group['meta']))}</small></span><i aria-hidden="true">▾</i></label>{tool_line}{offline_line}
    </header>
    <div class="book-contents" id="{group['key']}-contents">
      <input class="contents-state" id="{group['key']}-contents-state" type="checkbox" checked>
      <label class="contents-toggle" for="{group['key']}-contents-state"><span><span class="book-level">02 · 本书目录</span><strong>{escape(str(group['contents']))}</strong></span><b>{count_label}</b><i aria-hidden="true">▾</i></label>
      <div class="selected-articles"><div class="articles-label"><span>03 · 已选篇目</span><small>阅读与校读工作区</small></div>{''.join(cards)}</div>
    </div>
  </section>''')
    return '<div class="book-library">' + "".join(books) + '</div>'


def build_html(grouped: dict[str, list[dict[str, str | None]]]) -> str:
    total = sum(len(entries) for entries in grouped.values())
    active = [(key, entries) for key, entries in grouped.items() if entries or key in {"guwen_guanzhi", "chinese_wars", "american_civil_war", "laozi", "sunzi", "thirty_six_stratagems", "russian_wars", "mao_annotated_24_histories"}]
    nav = "".join(
        f'<a href="#{key}"><span>{escape(COLLECTIONS[key].title)}</span><b>{len(entries)}</b></a>'
        for key, entries in active
    )
    sections = []
    running_number = 0
    for key, entries in active:
        collection = COLLECTIONS[key]
        selector_links = {"rongzhai_suibi": "rongzhai_suibi/select_articles.html", "guwen_guanzhi": "guwen_guanzhi/select_articles.html", "chinese_wars": "chinese_wars/select_entries.html", "american_civil_war": "american_civil_war/select_battles.html", "laozi": "laozi/select_chapters.html", "sunzi": "sunzi/select_entries.html", "thirty_six_stratagems": "thirty_six_stratagems/select_entries.html", "liaozhai_stories": "liaozhai_stories/select_articles.html", "shiji": "shiji/select_articles.html", "nine_commentaries": "nine_commentaries/source_index/select_readings.html", "python": "python/index.html", "russian_wars": "russian_wars/select_articles.html", "mao_annotated_24_histories": "mao_annotated_24_histories/select_histories.html", "tcm_foundations": "tcm_foundations/index.html"}
        selector_link = (f'<a class="collection-tool" href="{selector_links[key]}">选择更多篇目</a>' if key in selector_links else "")
        resource_links = {
            "jianshang": '<a class="collection-resource" href="jianshang/翦商.pdf" target="_blank" rel="noopener">原书 PDF</a>',
            "tcm_foundations": '<a class="collection-resource" href="tcm_foundations/source_reader.html">PDF 与页边札记</a><a class="collection-resource" href="tcm_foundations/中医基础理论.pdf" target="_blank" rel="noopener">原书 PDF</a>',
        }.get(key, "")
        resources_block = f'<div class="collection-resources">{resource_links}</div>' if resource_links else ""
        if key == "marxist_classics":
            cards_html = marxist_books_html(entries, running_number)
            running_number += len(entries)
        else:
            cards = []
            for entry in entries:
                running_number += 1
                cards.append(entry_card(entry, running_number))
            heading = '<div class="news-columns" aria-hidden="true"><span>No.</span><span>Type</span><span>Date</span><span>Title</span><span>Reading</span><span>Editing</span><span>Report</span></div>' if key == "news_reports" else ""
            cards_html = heading + "".join(cards)
        sections.append(f'''<section class="collection" id="{key}" data-collection>
  <header class="collection-header">
    <button class="collection-toggle" type="button" aria-expanded="true" aria-controls="{key}-entries"><span class="collection-toggle-copy"><span class="collection-eyebrow">{escape(collection.eyebrow)}</span><span class="collection-title">{escape(collection.title)}</span><span class="collection-description">{escape(collection.description)}</span></span><i aria-hidden="true">▾</i></button>
    <div class="collection-meta">{selector_link}<strong>{len(entries)} 篇</strong></div>
  </header>
{resources_block}
  <div class="entries{' hierarchical-entries' if key == 'marxist_classics' else ''}" id="{key}-entries">{cards_html}</div>
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
.hierarchical-entries{{border:0;background:transparent;box-shadow:none}}.book-library{{display:grid;gap:12px}}.book-group{{border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#fff;box-shadow:0 1px 2px #3c40431a}}.book-state,.contents-state{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap}}.book-header{{display:flex;align-items:center;gap:12px;padding:0 12px;background:#f8f9fa}}.book-toggle{{display:flex;min-width:0;flex:1;align-items:center;justify-content:space-between;padding:13px 0;border:0;background:transparent;text-align:left;cursor:pointer;touch-action:manipulation}}.book-toggle>span,.contents-toggle>span{{display:grid;gap:3px}}.book-toggle strong{{font-size:15px;font-weight:600}}.book-toggle small{{color:var(--muted);font-size:11px}}.book-level{{color:#137333;font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}}.book-toggle i,.contents-toggle i{{font-style:normal;transition:transform .2s}}.book-tool{{padding:7px 11px;border:1px solid #c4d8f3;border-radius:18px;background:#e8f0fe;color:#174ea6;text-decoration:none;font-size:11px;font-weight:700;white-space:nowrap}}.book-contents{{border-top:1px solid var(--line)}}.contents-toggle{{display:grid;width:100%;grid-template-columns:minmax(0,1fr) auto 20px;gap:14px;align-items:center;padding:10px 16px;border:0;border-bottom:1px solid var(--line);background:#f1f3f4;text-align:left;cursor:pointer;touch-action:manipulation}}.contents-toggle strong{{font-size:13px}}.contents-toggle b{{color:var(--muted);font-size:11px}}.articles-label{{display:flex;justify-content:space-between;padding:8px 16px;border-bottom:1px solid var(--line);color:#174ea6;font-size:10px;font-weight:700;letter-spacing:.06em}}.articles-label small{{color:var(--muted);font-weight:400;letter-spacing:0}}.book-state:not(:checked)~.book-contents,.contents-state:not(:checked)~.selected-articles{{display:none}}.book-state:not(:checked)~.book-header .book-toggle i,.contents-state:not(:checked)+.contents-toggle i{{transform:rotate(-90deg)}}.book-state:focus-visible~.book-header .book-toggle,.contents-state:focus-visible+.contents-toggle{{outline:2px solid #1a73e8;outline-offset:-2px}}.selected-articles .entry:last-child{{border-bottom:0}}
.book-offline-tools{{display:flex;gap:5px}}.book-offline-tools button{{min-height:30px;padding:6px 9px;border:1px solid #b7d8c1;border-radius:16px;background:#e6f4ea;color:#137333;cursor:pointer;font-size:11px;font-weight:700;white-space:nowrap}}.book-offline-tools button[data-offline-remove]{{border-color:#dadce0;background:#fff;color:#5f6368}}
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
html[data-workspace-skin="reading"] .collection-nav{{gap:7px}}html[data-workspace-skin="reading"] .collection-nav a{{padding:10px 13px;border-color:var(--line);border-radius:8px;background:var(--panel);color:var(--ink);font-size:13px}}html[data-workspace-skin="reading"] .collection-nav a:hover,html[data-workspace-skin="reading"] .collection-nav a:focus-visible{{border-color:var(--red);background:#f7f1e6;color:var(--red)}}html[data-workspace-skin="reading"] .collection-nav b{{height:24px;min-width:24px;background:#eee8dc;color:var(--ink);font-size:11px}}
html[data-workspace-skin="reading"] .collection{{margin-top:34px;scroll-margin-top:90px}}html[data-workspace-skin="reading"] .collection-header{{padding:0 3px 15px;align-items:end;border:0;border-bottom:2px solid var(--ink);background:transparent}}html[data-workspace-skin="reading"] .collection-eyebrow{{display:block}}html[data-workspace-skin="reading"] .collection-title{{font:700 28px/1.25 "Songti SC","STSong",serif!important}}html[data-workspace-skin="reading"] .collection-description{{margin-top:7px;font-size:13px}}html[data-workspace-skin="reading"] .collection-tool{{border-radius:6px;background:var(--panel);color:var(--red)}}
html[data-workspace-skin="reading"] .entries{{box-shadow:none}}html[data-workspace-skin="reading"] .entry{{grid-template-columns:54px minmax(0,1fr) auto;gap:16px;min-height:84px;padding:13px 17px;border-color:#e6e0d5}}html[data-workspace-skin="reading"] .entry-number{{display:block;align-self:auto;background:transparent;border:0;color:#a49b8c;font:600 12px/1 Georgia,serif}}html[data-workspace-skin="reading"] .entry-copy{{display:block;align-self:auto;border:0}}html[data-workspace-skin="reading"] .entry-copy span{{padding:0;color:var(--blue);font-size:11px;letter-spacing:.06em}}html[data-workspace-skin="reading"] .entry-copy h3{{margin:5px 0 0;padding:0;border:0;font:650 18px/1.35 "Songti SC","STSong",serif}}html[data-workspace-skin="reading"] .entry-actions{{padding:0}}html[data-workspace-skin="reading"] .entry-actions a{{padding:8px 11px;border-radius:6px;font-size:12px}}html[data-workspace-skin="reading"] .entry-actions .primary{{background:var(--red)}}
/* Separate editor and PDF into aligned spreadsheet columns. */
.entry{{grid-template-columns:52px minmax(260px,1fr) 145px 145px 140px 72px}}
.entry-reading,.entry-editing{{align-self:stretch;display:flex;flex-direction:column;justify-content:center;padding:6px 12px;border-right:1px solid var(--line);color:var(--muted);font-size:11px;line-height:1.35}}.entry-reading strong,.entry-editing strong{{color:#5f6368;font-size:12px}}.entry-reading.read strong,.entry-editing.edited strong{{color:#137333}}.entry-reading time,.entry-editing time{{margin-top:2px;white-space:nowrap}}
.entry-action{{display:flex;align-self:stretch;align-items:center;justify-content:center;padding:6px 8px;border-right:1px solid var(--line)}}.entry-pdf{{border-right:0}}.entry-action a{{padding:6px 10px;border-radius:16px;text-decoration:none;font-size:11px;font-weight:700;white-space:nowrap}}.entry-action .primary{{background:#188038;color:#fff}}.entry-action .primary:hover{{background:#137333}}.entry-action .secondary{{border:1px solid var(--line);background:#fff}}.entry-action .secondary:hover{{border-color:var(--blue);color:var(--blue)}}.action-empty{{color:#9aa0a6}}
html[data-workspace-skin="reading"] .entry{{grid-template-columns:54px minmax(0,1fr) 145px 145px 132px 72px}}html[data-workspace-skin="reading"] .entry-action{{padding:0;border-right:1px solid var(--line)}}html[data-workspace-skin="reading"] .entry-pdf{{border-right:0}}html[data-workspace-skin="reading"] .entry-action a{{padding:8px 11px;border-radius:6px;font-size:12px}}html[data-workspace-skin="reading"] .entry-action .primary{{background:var(--red)}}
.news-columns,.news-entry,html[data-workspace-skin="reading"] .news-columns,html[data-workspace-skin="reading"] .news-entry{{grid-template-columns:52px 130px 118px minmax(250px,1fr) 112px 112px 140px}}
.news-columns{{display:grid;min-height:34px;border-bottom:1px solid var(--line);background:#f1f3f4;color:#5f6368;font-size:10px;font-weight:700;letter-spacing:.04em;text-transform:uppercase}}.news-columns span{{display:flex;align-items:center;padding:6px 10px;border-right:1px solid var(--line)}}.news-columns span:last-child{{border-right:0}}
.news-type,.news-date,.news-title{{align-self:stretch;display:flex;align-items:center;padding:8px 12px;border-right:1px solid var(--line)}}.news-type{{color:#137333;font-size:11px;font-weight:700}}.news-date{{color:var(--muted);font-size:11px;white-space:nowrap}}.news-title{{font:500 14px/1.35 Arial,"PingFang SC",sans-serif}}
html[data-workspace-skin="reading"] .news-columns{{background:#eee8dc;color:var(--muted)}}html[data-workspace-skin="reading"] .news-entry{{gap:0;min-height:58px;padding:0}}html[data-workspace-skin="reading"] .news-type{{color:var(--blue)}}html[data-workspace-skin="reading"] .news-title{{font:650 17px/1.35 "Songti SC","STSong",serif}}
@media(max-width:760px){{.entry,html[data-workspace-skin="reading"] .entry{{grid-template-columns:38px minmax(180px,1fr) 125px 125px 126px 62px}}.entry-copy{{border-right:1px solid var(--line)}}.entry-reading,.entry-editing{{padding:5px 7px}}.entry-action{{padding:5px 6px}}}}
@media(max-width:760px){{#news_reports .entries{{overflow-x:auto}}.news-columns,.news-entry,html[data-workspace-skin="reading"] .news-columns,html[data-workspace-skin="reading"] .news-entry{{min-width:840px;grid-template-columns:42px 116px 106px minmax(220px,1fr) 105px 105px 126px}}}}
@media(max-width:760px){{.book-header{{align-items:stretch;flex-direction:column;padding-bottom:10px;gap:7px}}.book-tool{{margin-left:0;align-self:flex-start}}.book-offline-tools{{width:100%}}.book-offline-tools button{{flex:1;min-height:38px}}.contents-toggle{{grid-template-columns:minmax(0,1fr) auto}}.contents-toggle i{{display:none}}}}
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
function installCollectionToggles(){{document.querySelectorAll('[data-collection]').forEach(section=>{{setCollectionCollapsed(section,true,false);section.querySelector('.collection-toggle')?.addEventListener('click',()=>{{const closing=!section.classList.contains('collapsed');setCollectionCollapsed(section,closing,false);if(closing)history.replaceState(null,'',location.pathname+location.search)}})}});document.querySelectorAll('.masthead-books a[href^="#"]').forEach(link=>link.addEventListener('click',event=>{{event.preventDefault();const section=document.querySelector(link.getAttribute('href')),opening=section?.classList.contains('collapsed');document.querySelectorAll('[data-collection]').forEach(item=>setCollectionCollapsed(item,true,false));if(opening&&section){{setCollectionCollapsed(section,false,false);history.replaceState(null,'',link.getAttribute('href'));section.scrollIntoView({{behavior:'smooth',block:'start'}})}}}}));const linked=location.hash&&document.querySelector(location.hash);if(linked?.matches('[data-collection]'))setCollectionCollapsed(linked,false,false)}}
function installBookToggles(){{}}
function filterCatalog(){{const query=search.value.trim().toLocaleLowerCase();let visibleTotal=0;document.querySelectorAll('[data-collection]').forEach(section=>{{let count=0;const books=section.querySelectorAll('[data-book]');if(books.length){{books.forEach(book=>{{const bookMatch=query&&book.dataset.search.includes(query);let bookCount=0;book.querySelectorAll('.entry').forEach(entry=>{{const show=entry.dataset.libraryHidden!=='true'&&(!query||bookMatch||entry.dataset.search.includes(query));entry.hidden=!show;if(show)bookCount++}});book.hidden=bookCount===0;if(query&&bookCount){{const bookState=book.querySelector('.book-state'),contentsState=book.querySelector('.contents-state');if(bookState)bookState.checked=true;if(contentsState)contentsState.checked=true}}count+=bookCount}})}}else{{section.querySelectorAll('.entry').forEach(entry=>{{const show=entry.dataset.libraryHidden!=='true'&&(!query||entry.dataset.search.includes(query));entry.hidden=!show;if(show)count++}})}}section.hidden=count===0;if(query&&count)setCollectionCollapsed(section,false,false);visibleTotal+=count}});empty.style.display=visibleTotal?'none':'block'}}
function applyRussianWarsLibrary(){{let selected;try{{selected=JSON.parse(localStorage.getItem('russian-wars-library-ids')||'null')}}catch{{selected=null}}const entries=[...document.querySelectorAll('#russian_wars-entries .entry')],allowed=Array.isArray(selected)?new Set(selected):null;entries.forEach(entry=>{{const parts=entry.dataset.editorPath?.split('/')||[],key=`${{parts.at(-2)}}@${{parts.at(-3)}}`,legacy=parts.at(-2),isBattle=legacy?.startsWith('battle_'),included=allowed?(allowed.has(key)||allowed.has(legacy)):!isBattle;entry.dataset.libraryHidden=included?'false':'true';entry.hidden=!included}});const count=entries.filter(entry=>!entry.hidden).length;const label=document.querySelector('#russian_wars .collection-meta strong');if(label)label.textContent=`${{count}} 篇已导入`}}
function renderReadingHistory(){{let history={{}};try{{history=JSON.parse(localStorage.getItem(readingHistoryKey)||'{{}}')}}catch{{}}const formatter=new Intl.DateTimeFormat('zh-CN',{{year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'}});document.querySelectorAll('.entry[data-editor-path]').forEach(entry=>{{const cell=entry.querySelector('.entry-reading'),record=history[entry.dataset.editorPath];cell.classList.toggle('read',Boolean(record));cell.querySelector('strong').textContent=record?`已读 ${{record.count||1}} 次`:'未读';cell.querySelector('time').textContent=record?.lastRead?formatter.format(new Date(record.lastRead)):''}})}}
function renderEditingHistory(){{let history={{}};try{{history=JSON.parse(localStorage.getItem(editingHistoryKey)||'{{}}')}}catch{{}}const formatter=new Intl.DateTimeFormat('zh-CN',{{year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'}});document.querySelectorAll('.entry[data-editor-path]').forEach(entry=>{{const cell=entry.querySelector('.entry-editing'),record=history[entry.dataset.editorPath];cell.classList.toggle('edited',Boolean(record));cell.querySelector('strong').textContent=record?`已编辑 ${{record.sessions||1}} 次`:'未编辑';cell.querySelector('time').textContent=record?.lastEdited?formatter.format(new Date(record.lastEdited)):'';cell.title=record?`首次编辑：${{formatter.format(new Date(record.firstEdited))}}\n最近编辑：${{formatter.format(new Date(record.lastEdited))}}\n修改批次：${{record.changes||1}}\n内容类型：${{(record.kinds||[]).join('、')||'正文'}}`:''}})}}
function renderHistory(){{renderReadingHistory();renderEditingHistory()}}
search.addEventListener('input',filterCatalog);
document.addEventListener('click',event=>{{if(event.target.closest('.entry-editor a,.entry-title-link'))sessionStorage.setItem('shiji-editor-view','annotated')}});
window.addEventListener('focus',()=>{{renderHistory();applyRussianWarsLibrary()}});window.addEventListener('storage',()=>{{renderHistory();applyRussianWarsLibrary()}});installCollectionToggles();installBookToggles();renderHistory();applyRussianWarsLibrary();
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
