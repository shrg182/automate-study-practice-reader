#!/usr/bin/env python3
"""Extend the Capital Volume I pilot into a complete offline Reader package."""
from __future__ import annotations

import argparse
import csv
from html import escape
import json
from pathlib import Path
import re
import sys

from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parent
SHARED = BASE.parents[1] / "shiji" / "shiji_lisheng_lujia"
sys.path[:0] = [str(SHARED), str(BASE)]
from build_editor import build_html, load_inline_notes, load_reading_notes, load_review_notes, load_terms  # noqa: E402
import import_pilot  # noqa: E402

EN_ROOT = "https://www.marxists.org/archive/marx/works/1867-c1"
ZH_ROOT = "https://www.marxists.org/chinese/marx/capital"
EN_PDF = "https://www.marxists.org/archive/marx/works/download/pdf/Capital-Volume-I.pdf"

CHAPTERS = [
    (2,"Part I — Commodities and Money","The Process of Exchange"),(3,"Part I — Commodities and Money","Money, or the Circulation of Commodities"),
    (4,"Part II — Transformation of Money into Capital","The General Formula for Capital"),(5,"Part II — Transformation of Money into Capital","Contradictions in the General Formula of Capital"),(6,"Part II — Transformation of Money into Capital","The Buying and Selling of Labour-Power"),
    (7,"Part III — Production of Absolute Surplus-Value","The Labour-Process and the Process of Producing Surplus-Value"),(8,"Part III — Production of Absolute Surplus-Value","Constant Capital and Variable Capital"),(9,"Part III — Production of Absolute Surplus-Value","The Rate of Surplus-Value"),(10,"Part III — Production of Absolute Surplus-Value","The Working-Day"),(11,"Part III — Production of Absolute Surplus-Value","Rate and Mass of Surplus-Value"),
    (12,"Part IV — Production of Relative Surplus-Value","The Concept of Relative Surplus-Value"),(13,"Part IV — Production of Relative Surplus-Value","Co-operation"),(14,"Part IV — Production of Relative Surplus-Value","Division of Labour and Manufacture"),(15,"Part IV — Production of Relative Surplus-Value","Machinery and Modern Industry"),
    (16,"Part V — Production of Absolute and Relative Surplus-Value","Absolute and Relative Surplus-Value"),(17,"Part V — Production of Absolute and Relative Surplus-Value","Changes of Magnitude in the Price of Labour-Power and in Surplus-Value"),(18,"Part V — Production of Absolute and Relative Surplus-Value","Various Formulae for the Rate of Surplus-Value"),
    (19,"Part VI — Wages","The Transformation of the Value of Labour-Power into Wages"),(20,"Part VI — Wages","Time-Wages"),(21,"Part VI — Wages","Piece-Wages"),(22,"Part VI — Wages","National Differences of Wages"),
    (23,"Part VII — Accumulation of Capital","Simple Reproduction"),(24,"Part VII — Accumulation of Capital","Conversion of Surplus-Value into Capital"),(25,"Part VII — Accumulation of Capital","The General Law of Capitalist Accumulation"),
    (26,"Part VIII — Primitive Accumulation","The Secret of Primitive Accumulation"),(27,"Part VIII — Primitive Accumulation","Expropriation of the Agricultural Population from the Land"),(28,"Part VIII — Primitive Accumulation","Bloody Legislation Against the Expropriated"),(29,"Part VIII — Primitive Accumulation","Genesis of the Capitalist Farmer"),(30,"Part VIII — Primitive Accumulation","Reaction of the Agricultural Revolution on Industry and the Home Market"),(31,"Part VIII — Primitive Accumulation","Genesis of the Industrial Capitalist"),(32,"Part VIII — Primitive Accumulation","Historical Tendency of Capitalist Accumulation"),(33,"Part VIII — Primitive Accumulation","The Modern Theory of Colonisation"),
]

def zh_number(chapter: int) -> int:
    if chapter <= 3: return chapter
    if chapter <= 6: return 4
    if chapter <= 25: return chapter - 2
    if chapter <= 32: return 24
    return 25

def extract(page: str) -> str:
    soup = BeautifulSoup(page, "html.parser")
    for node in soup.select("script,style,nav,header,footer,.skip,.footer,.navbar,sup,.note,.enote"):
        node.decompose()
    root = soup.find("main") or soup.body or soup
    blocks=[]
    for node in root.find_all(["h1","h2","h3","h4","h5","p","blockquote","li"]):
        if node.find_parent(["p","blockquote","li"]): continue
        value=re.sub(r"\s+"," ",node.get_text(" ",strip=True)).strip()
        if value and value not in blocks[-1:]: blocks.append(value)
    result="\n\n".join(blocks)
    if len(result)>=500:
        return result
    raw=root.get_text("\n",strip=True)
    lines=[re.sub(r"\s+"," ",line).strip() for line in raw.splitlines()]
    return "\n\n".join(line for line in lines if line)

def support_files(folder: Path) -> None:
    for name, content in {"reading_terms.csv":"term,pinyin,meaning,level,category,notes\n","inline_notes.tsv":"phrase\tnote\n","review_notes.tsv":"phrase\tnote\n","reading_notes.txt":""}.items():
        path=folder/name
        if not path.exists(): path.write_text(content,encoding="utf-8")

def rows() -> list[dict]:
    with (BASE/"pilot_catalog.csv").open(encoding="utf-8",newline="") as file:
        pilot=list(csv.DictReader(file))
    result=[{**r,"part":"Front Matter" if i==0 else "Part I — Commodities and Money","focus":"Established close-reading unit"} for i,r in enumerate(pilot)]
    for sequence,(number,part,title) in enumerate(CHAPTERS,6):
        slug=f'{sequence-1:02d}_chapter_{number:02d}_{re.sub("[^a-z0-9]+","_",title.lower()).strip("_")[:48]}'
        result.append({"sequence":str(sequence),"slug":slug,"title":f"Chapter {number} — {title}","part":part,"focus":title,"english_url":f"{EN_ROOT}/ch{number:02d}.htm","english_anchor":"","chinese_url":f"{ZH_ROOT}/{zh_number(number):02d}.htm","status":"complete"})
    return result

def selection_page(items: list[dict]) -> str:
    groups=[]
    for part in dict.fromkeys(r["part"] for r in items):
        cards="".join(f'<article><b>{int(r["sequence"]):02d}</b><div><strong>{escape(r["title"])}</strong><small>{escape(r["focus"])}</small></div><a href="volume_01/{escape(r["slug"])}/editor.html">Open</a></article>' for r in items if r["part"]==part)
        groups.append(f'<details open><summary>{escape(part)}</summary><div>{cards}</div></details>')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Capital, Volume I</title><link rel="stylesheet" href="../../workspace_theme.css"><style>body{{margin:0;background:#eee9df;color:#28251f;font-family:Arial,sans-serif}}main{{width:min(1080px,calc(100% - 28px));margin:28px auto 80px}}header,.contents{{padding:26px;background:#fffdf8;border:1px solid #d7cdbd;border-radius:10px}}h1{{font:700 clamp(34px,6vw,58px)/1.05 Georgia,serif;margin:8px 0}}header p{{max-width:800px;line-height:1.65}}.contents{{display:grid;gap:14px;margin-top:16px}}details{{border:1px solid #d7cdbd;border-radius:8px;overflow:hidden}}summary{{padding:14px;background:#f3eee5;font-weight:700;cursor:pointer}}details>div{{display:grid;gap:7px;padding:9px}}article{{display:grid;grid-template-columns:38px 1fr auto;gap:12px;align-items:center;padding:12px;border:1px solid #e2dace;border-radius:7px}}article small{{display:block;margin-top:4px;color:#756f64}}article a{{padding:7px 10px;border:1px solid #b7aa96;border-radius:7px;color:inherit;text-decoration:none}}@media(max-width:650px){{article{{grid-template-columns:32px 1fr}}article a{{grid-column:2;justify-self:start}}}}</style></head><body><main><header><a href="../../index.html">← Reader library</a><h1>Capital, Volume I</h1><p>Karl Marx · Complete English-first Reader edition in {len(items)} reading units. Chinese is a companion reference; the English text remains the leading language.</p><p><a href="assets/capital_volume_1_en.pdf">Offline English PDF</a> · <a href="{EN_ROOT}/" target="_blank">English source ↗</a> · <a href="{ZH_ROOT}/" target="_blank">Chinese reference ↗</a></p></header><section class="contents">{''.join(groups)}</section></main><script src="../../workspace_skin.js"></script><script src="../../mobile_pwa.js"></script></body></html>'''

def main() -> None:
    parser=argparse.ArgumentParser();parser.add_argument("--local",action="store_true");parser.add_argument("--refresh-clean",action="store_true");args=parser.parse_args()
    items=rows();cache={}
    for row in items[5:]:
        folder=BASE/"volume_01"/row["slug"];folder.mkdir(parents=True,exist_ok=True)
        if args.local:
            english=(folder/"source.txt").read_text(encoding="utf-8").strip();chinese=(folder/"chinese_support.txt").read_text(encoding="utf-8").strip()
        else:
            english=extract(cache.setdefault(row["english_url"],import_pilot.download(row["english_url"],"iso-8859-1")))
            chinese=extract(cache.setdefault(row["chinese_url"],import_pilot.download(row["chinese_url"],"gb18030")))
        if len(english)<500: raise ValueError(f'Short extraction: {row["slug"]} {len(english)}')
        keywords=[f'资本论 第{int(row["title"].split()[1])}章',row["focus"]]
        (folder/"source.txt").write_text(english+"\n",encoding="utf-8");(folder/"chinese_support.txt").write_text((chinese or "\n".join(keywords))+"\n",encoding="utf-8")
        clean=folder/"clean.txt"
        if args.refresh_clean or not clean.exists(): clean.write_text(english+"\n",encoding="utf-8")
        support_files(folder);metadata={**row,"author":"Karl Marx","language":"en","translation":"Samuel Moore and Edward Aveling (1887), edited by Friedrich Engels","chinese_role":"chapter-group support reference"}
        (folder/"metadata.json").write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        output=build_html(english,load_terms(folder/"reading_terms.csv"),row["english_url"],chapter_title=row["title"],editor_title=f'{row["title"]} · Capital · English-First Reader',storage_key=f'capital-v1-{row["slug"]}-v1',file_stem=f'capital_v1_{row["slug"]}',inline_notes=load_inline_notes(folder/"inline_notes.tsv"),review_notes=load_review_notes(folder/"review_notes.tsv"),reading_notes=load_reading_notes(folder/"reading_notes.txt"),global_terms=[],home_href="../../../../index.html",theme_href="../../../../workspace_theme.css",shared_library_href="../../select_readings.html",shared_library_label="Capital Reading Plan",source_site_label="Marxists Internet Archive")
        import_pilot.CHINESE_KEYWORDS[row["slug"]]=keywords;output=import_pilot.add_chinese_support(output,chinese,row)
        (folder/"editor.html").write_text(output,encoding="utf-8");print(row["sequence"],row["title"],len(english),len(chinese))
    (BASE/"select_readings.html").write_text(selection_page(items),encoding="utf-8")
    units=[]
    for row in items:
        folder=BASE/"volume_01"/row["slug"];sizes={n:(folder/n).stat().st_size for n in ("source.txt","chinese_support.txt","editor.html","metadata.json") if (folder/n).exists()};units.append({"sequence":int(row["sequence"]),"part":row["part"],"slug":row["slug"],"title":row["title"],"path":f'volume_01/{row["slug"]}/editor.html',"bytes":sizes})
    pdf=BASE/"assets"/"capital_volume_1_en.pdf";manifest={"schema_version":1,"book_id":"capital-volume-1","title":"Capital, Volume I","author":"Karl Marx","leading_language":"en","support_languages":["zh"],"offline_ready":True,"components":{"english_pdf":{"path":"assets/capital_volume_1_en.pdf","source":EN_PDF,"bytes":pdf.stat().st_size if pdf.exists() else 0}},"units":units}
    (BASE/"book_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__": main()
