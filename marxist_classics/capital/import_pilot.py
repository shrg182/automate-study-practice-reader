#!/usr/bin/env python3
"""Import the English-first *Capital* Volume I pilot from MIA."""
from __future__ import annotations

import csv
import argparse
from html import escape
import json
from pathlib import Path
import re
import ssl
import sys
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

import certifi
from bs4 import BeautifulSoup, NavigableString, Tag

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parents[1] / "shiji" / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))
from build_editor import build_html, load_inline_notes, load_reading_notes, load_review_notes, load_terms  # noqa: E402


def download(url: str, encoding: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 CapitalReader/1.0"})
    context = ssl.create_default_context(cafile=certifi.where())
    with urlopen(request, timeout=40, context=context) as response:
        return response.read().decode(encoding, errors="replace")


def clean_text(nodes: list[Tag]) -> str:
    paragraphs: list[str] = []
    for node in nodes:
        clone = BeautifulSoup(str(node), "html.parser")
        for unwanted in clone.select(".note, .enote, script, style"):
            unwanted.decompose()
        text = re.sub(r"\s+", " ", clone.get_text(" ", strip=True)).strip()
        if text and text != "Contents":
            paragraphs.append(text)
    return "\n\n".join(paragraphs)


def extract_english(page: str, anchor: str) -> str:
    soup = BeautifulSoup(page, "html.parser")
    if not anchor:
        nodes = []
        for node in soup.body.find_all(["p", "blockquote"], recursive=False):
            if node.get("class") and any(value in {"title", "skip"} for value in node.get("class", [])):
                continue
            if node.find("a", attrs={"name": "1"}):
                break
            nodes.append(node)
        return clean_text(nodes)
    marker = soup.find("a", attrs={"name": anchor})
    if marker is None:
        raise ValueError(f"Missing section anchor {anchor}")
    nodes = []
    for node in marker.find_all_next():
        if node is not marker and node.name == "a" and re.fullmatch(r"S[1-4]", node.get("name", "")):
            break
        if node.name == "h4" and node.get_text(" ", strip=True).lower() == "footnotes":
            break
        if node.name in {"p", "h5", "h6", "blockquote"} and not node.find_parent(["p", "h5", "h6", "blockquote"]):
            nodes.append(node)
    return clean_text(nodes)


CHINESE_SECTIONS = {
    "00_preface_1867": ("1", "2"),
    "01_commodity_factors": ("1", "2"),
    "02_twofold_labour": ("2", "3"),
    "03_form_of_value": ("3", "20"),
    "04_commodity_fetishism": ("20", "_ftn1"),
}

CHINESE_KEYWORDS = {
    "00_preface_1867": ["资本论 第一版序言", "万事开头难", "商品 价值形式"],
    "01_commodity_factors": ["商品的两个因素", "使用价值", "交换价值 社会必要劳动时间"],
    "02_twofold_labour": ["体现在商品中的劳动的二重性", "具体劳动", "抽象人类劳动"],
    "03_form_of_value": ["价值形式", "相对价值形式", "等价形式 货币形式"],
    "04_commodity_fetishism": ["商品的拜物教性质及其秘密", "商品拜物教", "劳动的社会性质"],
}


def extract_chinese(page: str, slug: str) -> str:
    start_name, end_name = CHINESE_SECTIONS[slug]
    soup = BeautifulSoup(page, "html.parser")
    start = soup.find("a", attrs={"name": start_name})
    if start is None:
        return ""
    parts: list[str] = []
    for sibling in start.next_siblings:
        if isinstance(sibling, Tag) and sibling.find("a", attrs={"name": end_name}) is not None:
            break
        if isinstance(sibling, Tag) and sibling.name == "a" and sibling.get("name") == end_name:
            break
        if isinstance(sibling, NavigableString):
            value = re.sub(r"\s+", " ", str(sibling)).strip()
        elif isinstance(sibling, Tag):
            clone = BeautifulSoup(str(sibling), "html.parser")
            for unwanted in clone.select("script, style, sup"):
                unwanted.decompose()
            value = re.sub(r"\s+", " ", clone.get_text(" ", strip=True)).strip()
        else:
            value = ""
        if value:
            parts.append(value)
    return "\n\n".join(parts)


def add_chinese_support(output: str, chinese_text: str, row: dict[str, str]) -> str:
    keywords = CHINESE_KEYWORDS[row["slug"]]
    keyword_html = "".join(f"<li>{escape(keyword)}</li>" for keyword in keywords)
    search_url = "https://www.google.com/search?q=" + quote_plus(" ".join(keywords))
    if chinese_text:
        paragraphs = "".join(f"<p>{escape(paragraph)}</p>" for paragraph in chinese_text.split("\n\n") if paragraph.strip())
        body = f'<div class="chinese-text">{paragraphs}</div>'
        status = "已从中文版原文提取对应章节；中英文按章节对应，尚未逐句对齐。"
    else:
        body = '<p class="chinese-empty">未能从保存的页面提取对应段落，可使用下列关键词继续查找。</p>'
        status = "暂无可渲染的中文段落。"
    card = f'''<section class="card chinese-support-card"><details><summary><span>中文参考</span><small>{escape(status)}</small></summary>{body}<div class="chinese-support-footer"><strong>检索关键词</strong><ul>{keyword_html}</ul><div><a href="{escape(row['chinese_url'], quote=True)}" target="_blank" rel="noreferrer">打开中文原文 ↗</a><a href="{escape(search_url, quote=True)}" target="_blank" rel="noreferrer">Google 搜索 ↗</a></div></div></details></section>'''
    output = output.replace('<section class="card"><h2>当前选择', card + '<section class="card"><h2>当前选择', 1)
    css = '''
.chinese-support-card details>summary{display:grid;gap:4px;cursor:pointer;list-style:none}.chinese-support-card summary::-webkit-details-marker{display:none}.chinese-support-card summary span{font-size:16px;font-weight:700}.chinese-support-card summary span::after{float:right;content:"▾"}.chinese-support-card details:not([open]) summary span::after{transform:rotate(-90deg)}.chinese-support-card summary small{color:var(--muted);font-size:11px;line-height:1.45}.chinese-text{max-height:55vh;margin-top:12px;padding:10px;overflow:auto;border:1px solid var(--line);background:#fff}.chinese-text p{margin:0 0 10px;color:var(--ink);font-size:14px;line-height:1.8}.chinese-text p:last-child{margin-bottom:0}.chinese-empty{padding:9px;background:var(--panel)}.chinese-support-footer{margin-top:10px;padding-top:10px;border-top:1px solid var(--line)}.chinese-support-footer strong{font-size:12px}.chinese-support-footer ul{margin:7px 0;padding-left:20px}.chinese-support-footer li{font-size:12px;line-height:1.55}.chinese-support-footer div{display:flex;gap:7px;flex-wrap:wrap}.chinese-support-footer a{padding:6px 9px;border:1px solid var(--line);border-radius:5px;color:var(--blue);text-decoration:none;font-size:11px;font-weight:700}
.bilingual-layout-control{position:relative;display:inline-flex}.bilingual-layout-trigger{white-space:nowrap}.bilingual-layout-popover{position:absolute;z-index:360;top:calc(100% + 6px);left:0;display:none;width:min(330px,calc(100vw - 24px));padding:12px;border:1px solid #c9d2df;border-radius:10px;background:#fff;box-shadow:0 10px 30px #0003}.bilingual-layout-control.open .bilingual-layout-popover{display:grid;gap:11px}.bilingual-presets{display:grid;grid-template-columns:repeat(5,1fr);gap:4px}.bilingual-presets button{min-width:0!important;padding:6px 3px!important;font-size:11px!important}.bilingual-presets button.active{background:#e6f4ea!important;color:#137333!important;font-weight:700}.bilingual-slider-label{display:grid;grid-template-columns:auto 1fr auto;gap:8px;align-items:center;color:var(--muted);font:12px/1.3 system-ui,sans-serif}.bilingual-slider-label input{width:100%;min-width:80px}.bilingual-layout-output{color:var(--ink);font-weight:700;white-space:nowrap}
.workspace.study-layout{max-width:1800px;align-items:start}.study-layout.study-english-only{grid-template-columns:minmax(0,1fr)}.study-layout.study-chinese-only{grid-template-columns:minmax(0,1fr)}.study-layout.study-english-only .study-pane,.study-layout.study-chinese-only .paper{display:none!important}.study-pane{min-width:0}.study-pane-header{position:sticky;z-index:3;top:0;padding:10px 10px 0;border:1px solid var(--line);border-bottom:0;background:var(--paper)}.study-pane-title{display:flex;justify-content:space-between;gap:10px;align-items:center;margin:0 0 8px;font:700 14px/1.3 system-ui,sans-serif}.study-pane-tabs{display:flex;gap:3px;overflow-x:auto}.study-pane-tab{flex:1 0 auto;min-height:32px!important;padding:5px 8px!important;border:0!important;border-radius:7px 7px 0 0!important;background:transparent!important;color:var(--muted)!important}.study-pane-tab.active{background:#e8f0fe!important;color:#174ea6!important;font-weight:700!important}.study-pane-body{min-height:220px}.study-panel{display:none}.study-panel.active{display:flex;flex-direction:column;gap:12px}.study-panel>.card,.study-panel>.footnotes{margin:0!important}.study-panel .chinese-support-card details{display:block}.study-panel .chinese-support-card summary{display:none}.study-panel .chinese-text{max-height:none;margin-top:0;font-size:16px}.study-panel .footnotes{border-radius:0;background:var(--paper)}.footnote-return{margin:0 0 10px}.study-panel-empty{padding:18px;color:var(--muted);background:var(--paper);border:1px solid var(--line)}
@media(min-width:901px){.workspace.study-layout:not(.study-english-only):not(.study-chinese-only){grid-template-columns:minmax(0,var(--english-share,70fr)) minmax(320px,var(--study-share,30fr))}.study-pane{position:sticky;top:calc(var(--toolbar-height,64px) + 12px);max-height:calc(100vh - var(--toolbar-height,64px) - 24px);overflow:auto}.study-pane .sidebar{position:static;max-height:none;overflow:visible}.study-chinese-only .study-pane{position:static;max-height:none;width:min(980px,100%);margin:0 auto}.study-chinese-only .chinese-text p{font-size:18px;line-height:2}}
@media(max-width:900px){.workspace.study-layout{display:grid;grid-template-columns:1fr}.workspace.study-layout.study-pane-first .study-pane{grid-row:1}.workspace.study-layout.study-pane-first .paper{grid-row:2}.study-pane{position:static;max-height:none}.bilingual-presets{grid-template-columns:repeat(3,1fr)}.bilingual-slider-label{grid-template-columns:auto 1fr}.bilingual-layout-output{grid-column:1/-1}.study-pane .chinese-text{max-height:70vh}.study-chinese-only .study-pane{width:100%}}
@media print{.bilingual-layout-control,.study-pane-header{display:none!important}.workspace.study-layout{display:block}.study-layout .paper{display:block!important}.study-pane{display:none!important}}
'''
    script = r'''
<script>
(function installBilingualStudyPane(){
  const workspace=document.querySelector('.workspace'),paper=workspace?.querySelector('.paper'),sidebar=workspace?.querySelector('.sidebar'),toolbar=document.querySelector('.toolbar');
  const chineseCard=sidebar?.querySelector('.chinese-support-card');
  if(!workspace||!paper||!sidebar||!toolbar||!chineseCard||document.querySelector('.study-pane'))return;
  const layoutKey='capital-bilingual-layout-v1',tabKey='capital-study-pane-tab-v1';
  const findCard=title=>[...sidebar.querySelectorAll(':scope > .card')].find(card=>card.querySelector(':scope > h2')?.textContent.trim()===title);
  const sourceCard=findCard('原文来源'),selectionCard=findCard('当前选择'),globalCard=document.getElementById('globalDictionaryCard'),termCard=document.getElementById('termList')?.closest('.card'),notesCard=findCard('用户札记'),footnotes=document.getElementById('footnotes');
  const pane=document.createElement('aside');pane.className='study-pane sidebar';pane.setAttribute('aria-label','双语学习窗格');
  pane.innerHTML='<div class="study-pane-header"><div class="study-pane-title"><span>学习窗格</span><small id="studyLayoutSummary"></small></div><div class="study-pane-tabs" role="tablist"><button type="button" class="study-pane-tab" data-study-tab="chinese">中文</button><button type="button" class="study-pane-tab" data-study-tab="footnotes">脚注</button><button type="button" class="study-pane-tab" data-study-tab="notes">札记</button><button type="button" class="study-pane-tab" data-study-tab="dictionary">词典</button><button type="button" class="study-pane-tab" data-study-tab="source">来源</button></div></div><div class="study-pane-body"></div>';
  const body=pane.querySelector('.study-pane-body'),panels={};
  ['chinese','footnotes','notes','dictionary','source'].forEach(name=>{const panel=document.createElement('section');panel.className='study-panel';panel.dataset.studyPanel=name;panel.setAttribute('role','tabpanel');body.append(panel);panels[name]=panel});
  panels.chinese.append(chineseCard);
  if(footnotes){const back=document.createElement('button');back.type='button';back.className='footnote-return';back.textContent='返回正文';footnotes.insertBefore(back,footnotes.firstChild);panels.footnotes.append(footnotes)}else panels.footnotes.innerHTML='<p class="study-panel-empty">本篇暂无脚注。</p>';
  if(notesCard)panels.notes.append(notesCard);else panels.notes.innerHTML='<p class="study-panel-empty">本篇暂无札记工具。</p>';
  [selectionCard,globalCard,termCard].filter(Boolean).forEach(card=>panels.dictionary.append(card));
  if(sourceCard)panels.source.append(sourceCard);
  [...sidebar.children].forEach(node=>panels.source.append(node));
  sidebar.replaceWith(pane);workspace.classList.add('study-layout');
  const tabNames={chinese:'中文',footnotes:'脚注',notes:'札记',dictionary:'词典',source:'来源'};
  function activateTab(name,persist=true){if(!panels[name])name='chinese';pane.querySelectorAll('.study-pane-tab').forEach(button=>{const active=button.dataset.studyTab===name;button.classList.toggle('active',active);button.setAttribute('aria-selected',String(active))});Object.entries(panels).forEach(([key,panel])=>panel.classList.toggle('active',key===name));if(persist)localStorage.setItem(tabKey,name)}
  pane.querySelector('.study-pane-tabs').addEventListener('click',event=>{const button=event.target.closest('[data-study-tab]');if(button)activateTab(button.dataset.studyTab)});
  activateTab(localStorage.getItem(tabKey)||'chinese',false);
  const control=document.createElement('div');control.className='bilingual-layout-control';
  control.innerHTML='<button type="button" class="bilingual-layout-trigger" aria-expanded="false">中英布局</button><div class="bilingual-layout-popover"><div class="bilingual-presets"><button type="button" data-share="0">仅英文</button><button type="button" data-share="30">英文优先</button><button type="button" data-share="50">均衡</button><button type="button" data-share="65">中文优先</button><button type="button" data-share="100">仅中文</button></div><label class="bilingual-slider-label"><span>英文</span><input type="range" min="0" max="100" step="1" value="30" aria-label="中文和学习窗格所占比例"><span>中文／学习窗格</span><output class="bilingual-layout-output"></output></label></div>';
  const trigger=control.querySelector('.bilingual-layout-trigger'),popover=control.querySelector('.bilingual-layout-popover'),slider=control.querySelector('input'),output=control.querySelector('output');
  (document.querySelector('.reading-environment')||toolbar.lastElementChild)?.insertAdjacentElement('afterend',control);
  const presetNames={0:'仅英文',30:'英文优先',50:'均衡',65:'中文优先',100:'仅中文'};
  function applyShare(raw,persist=true){const share=Math.max(0,Math.min(100,Number(raw)||0));workspace.classList.toggle('study-english-only',share===0);workspace.classList.toggle('study-chinese-only',share===100);workspace.classList.toggle('study-pane-first',share>50&&share<100);workspace.style.setProperty('--english-share',`${100-share}fr`);workspace.style.setProperty('--study-share',`${share}fr`);slider.value=String(share);output.textContent=share===0?'仅英文':share===100?'仅中文':`英文 ${100-share}% · 学习窗格 ${share}%`;pane.querySelector('#studyLayoutSummary').textContent=presetNames[share]||`${share}%`;control.querySelectorAll('[data-share]').forEach(button=>button.classList.toggle('active',Number(button.dataset.share)===share));if(persist)localStorage.setItem(layoutKey,String(share))}
  applyShare(localStorage.getItem(layoutKey)??'30',false);
  trigger.addEventListener('click',event=>{event.stopPropagation();const open=control.classList.toggle('open');trigger.setAttribute('aria-expanded',String(open));if(open){popover.style.left='0px';requestAnimationFrame(()=>{const rect=popover.getBoundingClientRect(),offset=Math.max(12-rect.left,Math.min(0,innerWidth-12-rect.right));popover.style.left=`${offset}px`})}});
  control.querySelector('.bilingual-presets').addEventListener('click',event=>{const button=event.target.closest('[data-share]');if(button)applyShare(button.dataset.share)});
  slider.addEventListener('input',event=>applyShare(event.target.value));
  document.addEventListener('click',event=>{if(!control.contains(event.target)){control.classList.remove('open');trigger.setAttribute('aria-expanded','false')}});
  let returnTarget=null;
  document.addEventListener('click',event=>{const reference=event.target.closest('.footnote-ref');if(reference){returnTarget=reference;activateTab('footnotes');if(workspace.classList.contains('study-english-only'))applyShare(30)}},true);
  document.addEventListener('click',event=>{if(event.target.closest('.global-term-anchor,.term-anchor')){activateTab('dictionary');if(workspace.classList.contains('study-english-only'))applyShare(30)}},true);
  footnotes?.querySelector('.footnote-return')?.addEventListener('click',()=>{if(returnTarget?.isConnected){returnTarget.scrollIntoView({behavior:'smooth',block:'center'});returnTarget.focus?.({preventScroll:true})}});
  window.BilingualStudyPane={activateTab,applyShare};
})();
</script>
'''
    return output.replace("</style>", css + "</style>", 1).replace("</body>", script + "</body>", 1)


def ensure_support_files(project: Path) -> None:
    defaults = {
        "reading_terms.csv": "term,pinyin,meaning,level,category,notes\n",
        "inline_notes.tsv": "phrase\tnote\n",
        "review_notes.tsv": "phrase\tnote\n",
        "reading_notes.txt": "",
    }
    for name, content in defaults.items():
        path = project / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-clean", action="store_true", help="replace derived clean text from the source")
    parser.add_argument("--local", action="store_true", help="rebuild editors from saved English and Chinese text without downloading")
    args = parser.parse_args()
    with (BASE_DIR / "pilot_catalog.csv").open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    cache: dict[str, str] = {}
    chinese_cache: dict[str, str] = {}
    for row in rows:
        project = BASE_DIR / "volume_01" / row["slug"]
        sources = project / "sources"
        sources.mkdir(parents=True, exist_ok=True)
        if args.local:
            text = (project / "source.txt").read_text(encoding="utf-8").strip()
            chinese_text = (project / "chinese_support.txt").read_text(encoding="utf-8").strip()
            page = chinese = ""
        else:
            page = cache.setdefault(row["english_url"], download(row["english_url"], "iso-8859-1"))
            chinese = chinese_cache.setdefault(row["chinese_url"], download(row["chinese_url"], "gb18030"))
            text = extract_english(page, row["english_anchor"])
            chinese_text = extract_chinese(chinese, row["slug"])
        if len(text) < 200:
            raise ValueError(f'Extraction too short for {row["slug"]}: {len(text)}')
        if not args.local:
            (sources / "english_page.html").write_text(page, encoding="utf-8")
            (sources / "chinese_reference_page.html").write_text(chinese, encoding="utf-8")
        (project / "chinese_support.txt").write_text((chinese_text or "\n".join(CHINESE_KEYWORDS[row["slug"]])) + "\n", encoding="utf-8")
        (project / "source.txt").write_text(text + "\n", encoding="utf-8")
        clean = project / "clean.txt"
        if args.refresh_clean or not clean.exists():
            clean.write_text(text + "\n", encoding="utf-8")
        metadata = {**row, "language": "en", "translation": "Samuel Moore and Edward Aveling (1887), edited by Friedrich Engels", "chinese_role": "support-reference-section-aligned" if chinese_text else "support-keywords"}
        (project / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        ensure_support_files(project)
        output = build_html(text, load_terms(project / "reading_terms.csv"), row["english_url"], chapter_title=row["title"], editor_title=f'{row["title"]} · English-First Reader', storage_key=f'capital-v1-{row["slug"]}-v1', file_stem=f'capital_v1_{row["slug"]}', inline_notes=load_inline_notes(project / "inline_notes.tsv"), review_notes=load_review_notes(project / "review_notes.tsv"), reading_notes=load_reading_notes(project / "reading_notes.txt"), global_terms=[], home_href="../../../../index.html", theme_href="../../../../workspace_theme.css", shared_library_href="../../select_readings.html", shared_library_label="Capital Reading Plan", source_site_label="Marxists Internet Archive")
        output = add_chinese_support(output, chinese_text, row)
        (project / "editor.html").write_text(output, encoding="utf-8")
        print(f'{row["sequence"]}. {row["title"]}: {len(text)} characters')


if __name__ == "__main__":
    main()
