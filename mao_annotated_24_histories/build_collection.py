#!/usr/bin/env python3
"""Build the manifest-driven catalog for Mao's annotated Twenty-Four Histories."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path


BASE = Path(__file__).resolve().parent
HISTORIES = [
    ("shiji", "史记", "司马迁", "本纪、表、书、世家、列传"),
    ("hanshu", "汉书", "班固", "纪、表、志、传"),
    ("hou_hanshu", "后汉书", "范晔", "纪、志、传"),
    ("sanguozhi", "三国志", "陈寿", "魏书、蜀书、吴书"),
    ("jinshu", "晋书", "房玄龄等", "帝纪、志、列传、载记"),
    ("songshu", "宋书", "沈约", "本纪、志、列传"),
    ("nan_qishu", "南齐书", "萧子显", "本纪、志、列传"),
    ("liangshu", "梁书", "姚思廉", "本纪、列传"),
    ("chenshu", "陈书", "姚思廉", "本纪、列传"),
    ("weishu", "魏书", "魏收", "帝纪、志、列传"),
    ("bei_qishu", "北齐书", "李百药", "帝纪、列传"),
    ("zhoushu", "周书", "令狐德棻等", "帝纪、列传"),
    ("suishu", "隋书", "魏征等", "帝纪、志、列传"),
    ("nanshi", "南史", "李延寿", "本纪、列传"),
    ("beishi", "北史", "李延寿", "本纪、列传"),
    ("jiu_tangshu", "旧唐书", "刘昫等", "本纪、志、列传"),
    ("xin_tangshu", "新唐书", "欧阳修、宋祁", "本纪、志、表、列传"),
    ("jiu_wudaishi", "旧五代史", "薛居正等", "梁、唐、晋、汉、周书及志"),
    ("xin_wudaishi", "新五代史", "欧阳修", "本纪、家人传、臣传、考"),
    ("songshi", "宋史", "脱脱等", "本纪、志、表、列传"),
    ("liaoshi", "辽史", "脱脱等", "本纪、志、表、列传、国语解"),
    ("jinshi", "金史", "脱脱等", "本纪、志、表、列传"),
    ("yuanshi", "元史", "宋濂等", "本纪、志、表、列传"),
    ("mingshi", "明史", "张廷玉等", "本纪、志、表、列传"),
]

RESEARCH = [
    {
        "id": "publication_2013",
        "type": "版本与出版",
        "title": "《毛泽东批注二十四史》横排简体字本在京出版",
        "author": "新华社",
        "date": "2013-03-21",
        "scope": "全书",
        "reliability": "出版信息／机构来源",
        "url": "https://dangshi.people.com.cn/n/2013/0321/c85037-20862188.html",
        "summary": "说明全书为91册横排简体武英殿本，以及批注、圈画、《三国志集解》和史论资料的来源。",
    },
    {
        "id": "editorial_history",
        "type": "版本与出版",
        "title": "关于《毛泽东批注二十四史》一书的整理与出版",
        "author": "中国出版传媒商报",
        "date": "2019",
        "scope": "全书",
        "reliability": "出版行业资料",
        "url": "https://www.cbbr.com.cn/contents/533/10687.html",
        "summary": "分别介绍批注整理、史论整理和武英殿本《二十四史》整理工作，并说明修订版的校勘增补。",
    },
    {
        "id": "xu_zhongyuan_2023",
        "type": "毛泽东读史研究",
        "title": "新中国成立后毛泽东对《二十四史》的研读和批注",
        "author": "徐中远",
        "date": "2023-09-26",
        "scope": "全书",
        "reliability": "研究机构文章",
        "url": "https://www.dswxyjy.org.cn/n1/2023/0926/c423725-40085727.html",
        "summary": "概述阅读过程，并将批注内容归纳为人物、政论、战争、史书注解、古今评论、方法论等八类。",
    },
    {
        "id": "wang_gang_publication_recollection",
        "type": "版本与出版",
        "title": "宝贵的精神财富 伟大的领袖风范——回忆毛泽东同志藏书和文稿整理保管工作",
        "author": "王刚",
        "date": "2019",
        "scope": "原藏本与影印出版",
        "reliability": "回忆与机构转载",
        "url": "https://www.nju.edu.cn/info/3391/316961.htm",
        "summary": "记述原藏武英殿本、批注校核及1996年影印出版工作，可用于追溯91册本的文献来源。",
    },
]

SHIJI_SCAN_GROUPS = [
    ("卷1", 79498, ("benji",)), ("卷2–5", 79499, ("benji",)),
    ("卷6–7", 79500, ("benji",)), ("卷8–12", 79501, ("benji",)),
    ("卷13–14", 79502, ("biao",)), ("卷15–17", 79503, ("biao",)),
    ("卷18–19", 79504, ("biao",)), ("卷20–22", 79505, ("biao",)),
    ("卷23–26", 79506, ("shu",)), ("卷27–30", 79507, ("shu",)),
    ("卷31–33", 79508, ("shijia",)), ("卷34–39", 79509, ("shijia",)),
    ("卷40–43", 79510, ("shijia",)), ("卷44–48", 79511, ("shijia",)),
    ("卷49–57", 79512, ("shijia",)),
    ("卷58–67", 79513, ("shijia", "liezhuan")),
    ("卷68–74", 79514, ("liezhuan",)), ("卷75–81", 79515, ("liezhuan",)),
    ("卷82–87", 79516, ("liezhuan",)), ("卷88–95", 79517, ("liezhuan",)),
    ("卷96–103", 79518, ("liezhuan",)), ("卷104–109", 79519, ("liezhuan",)),
    ("卷110–115", 79520, ("liezhuan",)), ("卷116–120", 79521, ("liezhuan",)),
    ("卷121–126", 79522, ("liezhuan",)), ("卷127–130", 79523, ("liezhuan",)),
]


def manifest() -> dict:
    return {
        "schema_version": 1,
        "id": "mao_annotated_24_histories",
        "title": "毛泽东批注二十四史",
        "edition": "横排简体字本，91册",
        "source_status": "awaiting_authorized_scans",
        "source_note": "Yale University Library reportedly holds a complete set; catalog and reproduction details remain to be confirmed.",
        "storage_policy": "catalog-first; scans and OCR are optional per-history or per-volume offline packages",
        "histories": [
            {"id": key, "title": title, "author": author, "structure": structure, "scan_status": "awaiting_source", "chapters": []}
            for key, title, author, structure in HISTORIES
        ],
        "research": RESEARCH,
    }


def overview_page() -> str:
    cards = "".join(
        f'<article><span>{i:02d}</span><div><h2>{f"<a href=\"../shiji/index.html\">《{escape(title)}》</a>" if key == "shiji" else f"《{escape(title)}》"}</h2><p>{escape(author)} · {escape(structure)}</p></div><b>{"试点已建立" if key == "shiji" else "待取得扫描件"}</b></article>'
        for i, (key, title, author, structure) in enumerate(HISTORIES, 1)
    )
    refs = "".join(
        f'<li><small>{escape(item["type"])} · {escape(item["reliability"])}</small><a href="{escape(item["url"], quote=True)}" target="_blank" rel="noreferrer">{escape(item["title"])}</a><p>{escape(item["summary"])}</p></li>'
        for item in RESEARCH
    )
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>毛泽东批注二十四史 · 资料总览</title><link rel="stylesheet" href="../workspace_theme.css"><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f5f3ed;color:#26231e;font-family:Arial,"PingFang SC",sans-serif}}header{{padding:34px max(20px,5vw);background:#46372c;color:#fff}}header a{{color:#f6dd9b}}h1{{margin:.25em 0;font:700 clamp(34px,6vw,62px)/1.1 "Songti SC",serif}}header p{{max-width:850px;line-height:1.7}}nav{{position:sticky;top:0;z-index:3;display:flex;gap:8px;padding:10px max(18px,5vw);border-bottom:1px solid #d8d2c6;background:#fffc}}nav a{{padding:7px 11px;border-radius:16px;color:#7b352c;text-decoration:none}}main{{width:min(1180px,calc(100% - 30px));margin:22px auto 95px}}.notice{{padding:16px;border-left:4px solid #b28335;background:#fff8e1;line-height:1.65}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;margin-top:16px}}article{{display:grid;grid-template-columns:36px 1fr auto;gap:12px;align-items:center;padding:14px;border:1px solid #d8d2c6;border-radius:8px;background:#fff}}article h2{{margin:0;font:700 19px/1.3 "Songti SC",serif}}article h2 a{{color:#174ea6}}article p{{margin:5px 0 0;color:#69645c;font-size:12px}}article b{{color:#8a6d3b;font-size:11px}}.research{{margin-top:36px}}.research li{{margin:10px 0;padding:15px;border:1px solid #d8d2c6;background:#fff;list-style:none}}.research small,.research a{{display:block}}.research small{{color:#6b665e}}.research a{{margin-top:5px;color:#174ea6;font-weight:700}}.research p{{margin-bottom:0;line-height:1.6}}@media(max-width:720px){{.grid{{grid-template-columns:1fr}}article{{grid-template-columns:30px 1fr}}article b{{grid-column:2}}}}
</style></head><body><header><a href="../index.html#mao_annotated_24_histories">← Reader library</a><h1>《毛泽东批注二十四史》</h1><p>九十一册横排简体字本的渐进式数字阅读框架：以二十四史为阅读层级，以原书册次保存扫描来源，并把批注、史论、研究资料和私人笔记严格分层。</p></header><nav><a href="#catalog">二十四史</a><a href="#research">研究资料</a><a href="select_histories.html">加入书库</a></nav><main><p class="notice"><strong>资料状态：</strong>目录结构已经建立；扫描页、OCR文字和页码对应关系须在取得可靠的91册本图像后导入。当前不会以普通武英殿本图像冒充毛泽东批注本。</p><section id="catalog" class="grid">{cards}</section><section class="research" id="research"><h2>研究资料</h2><ul>{refs}</ul></section></main><script src="../mobile_pwa.js"></script></body></html>'''


def selector_page() -> str:
    data = json.dumps([{"id": k, "title": t, "author": a, "structure": s} for k, t, a, s in HISTORIES], ensure_ascii=False).replace("</", "<\\/")
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>选择二十四史 · Reader</title><style>*{{box-sizing:border-box}}body{{margin:0;background:#f1f3f4;color:#202124;font-family:Arial,"PingFang SC",sans-serif}}header{{padding:28px max(18px,5vw);background:#46372c;color:#fff}}header a{{color:#f6dd9b}}main{{width:min(960px,calc(100% - 28px));margin:18px auto 80px}}.controls{{position:sticky;top:0;display:flex;gap:8px;padding:10px;background:#f1f3f4}}input[type=search]{{min-width:0;flex:1;padding:10px;border:1px solid #bdc1c6;border-radius:7px}}button{{padding:9px 12px;border:1px solid #bdc1c6;border-radius:7px;background:#fff;cursor:pointer}}button.primary{{background:#188038;color:#fff}}article{{display:grid;grid-template-columns:30px 1fr auto;gap:12px;align-items:center;padding:14px;border:1px solid #dadce0;border-bottom:0;background:#fff}}article:last-child{{border-bottom:1px solid #dadce0}}h2{{margin:0;font-size:17px}}p{{margin:5px 0 0;color:#5f6368;font-size:12px}}small{{color:#8a6d3b}}@media(max-width:600px){{article{{grid-template-columns:26px 1fr}}article small{{grid-column:2}}}}</style></head><body><header><a href="../index.html#mao_annotated_24_histories">← 书库</a><h1>选择二十四史</h1><p>先加入目录；扫描文件将在来源确认后按史、册或篇目单独离线保存。</p></header><main><div class="controls"><input id="q" type="search" placeholder="搜索史名、作者或结构"><button id="all">全选</button><button class="primary" id="save">加入书库</button></div><p id="count"></p><section id="list"></section></main><script>const books={data},key='mao-24-histories-library',selected=new Set(JSON.parse(localStorage.getItem(key)||'[]')),list=document.getElementById('list');function render(){{const q=document.getElementById('q').value.trim().toLowerCase(),shown=books.filter(x=>!q||`${{x.title}} ${{x.author}} ${{x.structure}}`.toLowerCase().includes(q));list.innerHTML=shown.map((x,i)=>`<article><span>${{String(i+1).padStart(2,'0')}}</span><label><input type="checkbox" data-id="${{x.id}}" ${{selected.has(x.id)?'checked':''}}> <span><h2>《${{x.title}}》</h2><p>${{x.author}} · ${{x.structure}}</p></span></label><small>扫描件待导入</small></article>`).join('');document.getElementById('count').textContent=`已选择 ${{selected.size}} / 24 部`}}list.onchange=e=>{{if(!e.target.dataset.id)return;e.target.checked?selected.add(e.target.dataset.id):selected.delete(e.target.dataset.id);render()}};document.getElementById('q').oninput=render;document.getElementById('all').onclick=()=>{{selected.size===books.length?selected.clear():books.forEach(x=>selected.add(x.id));render()}};document.getElementById('save').onclick=()=>{{localStorage.setItem(key,JSON.stringify([...selected]));location.href='overview/editor.html?view=annotated'}};render();</script></body></html>'''


def shiji_manifest() -> dict:
    return {
        "schema_version": 1,
        "id": "shiji",
        "title": "史记",
        "author": "司马迁",
        "source_edition": "毛泽东批注二十四史（91册横排简体字本）",
        "source_volumes": [
            {"id": f"source_volume_{i:02d}", "label": f"《史记》来源册 {i}", "status": "awaiting_scan", "page_count": None, "sha256": None}
            for i in range(1, 4)
        ],
        "reader_divisions": [
            {"id": "benji", "label": "本纪", "juan": "1–12"},
            {"id": "biao", "label": "表", "juan": "13–22"},
            {"id": "shu", "label": "书", "juan": "23–30"},
            {"id": "shijia", "label": "世家", "juan": "31–60"},
            {"id": "liezhuan", "label": "列传", "juan": "61–130"},
        ],
        "comparison_source": {
            "label": "中国哲学书电子化计划《武英殿二十四史》本《史记》",
            "url": "https://ctext.org/library.pl?if=gb&remap=gb&res=77688",
            "role": "unannotated_comparison_only",
        },
        "comparison_scan_groups": [
            {
                "label": label,
                "file_id": file_id,
                "divisions": list(divisions),
                "url": f"https://ctext.org/library.pl?if=gb&file={file_id}&page=1&remap=gb",
                "role": "unannotated_comparison_only",
            }
            for label, file_id, divisions in SHIJI_SCAN_GROUPS
        ],
        "alignment_status": "awaiting_annotated_source_toc",
        "offline_packages": [],
    }


def shiji_page() -> str:
    division_data = shiji_manifest()["reader_divisions"]
    divisions = "".join(
        f'<article><span>{i:02d}</span><div><h2>{escape(item["label"])}</h2><p>卷 {escape(item["juan"])}</p><div class="scan-links">'
        + "".join(
            f'<a href="https://ctext.org/library.pl?if=gb&amp;file={file_id}&amp;page=1&amp;remap=gb" target="_blank" rel="noreferrer">{escape(label)} 图像 ↗</a>'
            for label, file_id, group_divisions in SHIJI_SCAN_GROUPS
            if item["id"] in group_divisions
        )
        + '</div></div><button disabled>批注本待对页</button></article>'
        for i, item in enumerate(division_data, 1)
    )
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>史记 · 毛泽东批注二十四史试点</title><style>*{{box-sizing:border-box}}body{{margin:0;background:#f5f3ed;color:#27231e;font-family:Arial,"PingFang SC",sans-serif}}header{{padding:32px max(18px,5vw);background:#563d2d;color:#fff}}header a{{color:#f7d88a}}h1{{margin:.25em 0;font:700 clamp(38px,7vw,68px)/1 "Songti SC",serif}}main{{width:min(1000px,calc(100% - 28px));margin:20px auto 90px}}.status{{padding:15px;border:1px solid #e1c98f;background:#fff8dd;line-height:1.7}}.sources{{display:flex;gap:8px;flex-wrap:wrap;margin:15px 0}}.sources a,.scan-links a{{padding:8px 11px;border:1px solid #c8c1b4;border-radius:17px;background:#fff;color:#174ea6;text-decoration:none}}.volumes,.divisions{{display:grid;gap:8px}}.volumes{{grid-template-columns:repeat(3,1fr);margin:16px 0 28px}}.volumes div{{padding:18px;border:1px solid #d8d2c6;background:#fff}}.volumes b,.volumes small{{display:block}}.volumes small{{margin-top:6px;color:#8a6d3b}}article{{display:grid;grid-template-columns:35px 1fr auto;gap:12px;align-items:start;padding:15px;border:1px solid #d8d2c6;background:#fff}}article h2,article p{{margin:0}}article p{{margin-top:5px;color:#69645c}}.scan-links{{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}}.scan-links a{{padding:5px 8px;font-size:11px}}button{{padding:8px;border:1px solid #d8d2c6;border-radius:6px}}@media(max-width:650px){{.volumes{{grid-template-columns:1fr}}article{{grid-template-columns:28px 1fr}}article button{{grid-column:2}}}}</style></head><body><header><a href="../overview/editor.html?view=annotated">← 二十四史总览</a><h1>《史记》</h1><p>三册试点 · 本纪、表、书、世家、列传</p></header><main><p class="status"><strong>试点状态：</strong>阅读层级和三个来源册容器已经建立。下列26组图像是未加毛泽东批注的武英殿本比较资料；91册批注本仍等待来源，因此暂不推测三个物理册与130卷之间的准确页码边界。</p><div class="sources"><a href="https://ctext.org/library.pl?if=gb&amp;remap=gb&amp;res=77688" target="_blank" rel="noreferrer">全部比较图像 ↗</a><a href="https://search.library.yale.edu/catalog" target="_blank" rel="noreferrer">Yale Library catalog ↗</a><a href="book.json" target="_blank">《史记》manifest</a></div><section><h2>91册本来源容器</h2><div class="volumes"><div><b>《史记》来源册 1</b><small>等待扫描与页数</small></div><div><b>《史记》来源册 2</b><small>等待扫描与页数</small></div><div><b>《史记》来源册 3</b><small>等待扫描与页数</small></div></div></section><section><h2>阅读结构与比较图像</h2><div class="divisions">{divisions}</div></section></main></body></html>'''


def main() -> None:
    (BASE / "overview").mkdir(parents=True, exist_ok=True)
    (BASE / "shiji").mkdir(parents=True, exist_ok=True)
    (BASE / "collection.json").write_text(json.dumps(manifest(), ensure_ascii=False, indent=2), encoding="utf-8")
    (BASE / "overview" / "editor.html").write_text(overview_page(), encoding="utf-8")
    (BASE / "select_histories.html").write_text(selector_page(), encoding="utf-8")
    (BASE / "shiji" / "book.json").write_text(json.dumps(shiji_manifest(), ensure_ascii=False, indent=2), encoding="utf-8")
    (BASE / "shiji" / "index.html").write_text(shiji_page(), encoding="utf-8")
    print("Built Mao annotated Twenty-Four Histories framework: 24 histories, 4 research records, Shiji pilot")


if __name__ == "__main__":
    main()
