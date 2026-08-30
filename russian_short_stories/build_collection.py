#!/usr/bin/env python3
"""Build a separate Russian-first short-prose collection."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from urllib.parse import quote

BASE = Path(__file__).resolve().parent
PRACTICE = BASE.parent
sys.path.insert(0, str(PRACTICE / "shiji" / "shiji_lisheng_lujia"))
from build_editor import build_html  # noqa: E402

STORIES = [
    {
        "slug": "01_chekhov_radost", "title": "Радость", "author": "Антон Чехов", "year": "1883", "form": "Юмористический рассказ",
        "source": "https://ru.wikisource.org/wiki/Радость_(Чехов)",
        "paragraphs": [
            "Было двенадцать часов ночи.",
            "Митя Кулдаров, возбужденный, взъерошенный, влетел в квартиру своих родителей и быстро заходил по всем комнатам. Родители уже ложились спать. Сестра лежала в постели и дочитывала последнюю страничку романа. Братья-гимназисты спали.",
            "— Откуда ты? — удивились родители. — Что с тобой?",
            "— Ох, не спрашивайте! Я никак не ожидал! Нет, я никак не ожидал! Это… это даже невероятно!",
            "Митя захохотал и сел в кресло, будучи не в силах держаться на ногах от счастья.",
            "— Это невероятно! Вы не можете себе представить! Вы поглядите!",
            "Сестра спрыгнула с постели и, накинув на себя одеяло, подошла к брату. Гимназисты проснулись.",
            "— Что с тобой? На тебе лица нет!",
            "— Это я от радости, мамаша! Ведь теперь меня знает вся Россия! Вся! Раньше только вы одни знали, что на этом свете существует коллежский регистратор Дмитрий Кулдаров, а теперь вся Россия знает об этом! Мамаша! О, господи!",
            "Митя вскочил, побегал по всем комнатам и опять сел.",
            "— Да что такое случилось? Говори толком!",
            "— Вы живете, как дикие звери, газет не читаете, не обращаете никакого внимания на гласность, а в газетах так много замечательного! Ежели что случится, сейчас всё известно, ничего не укроется! Как я счастлив! О, господи! Ведь только про знаменитых людей в газетах печатают, а тут взяли да про меня напечатали!",
            "— Что ты? Где?",
            "Папаша побледнел. Мамаша взглянула на образ и перекрестилась. Гимназисты вскочили и, как были, в одних коротких ночных сорочках, подошли к своему старшему брату.",
            "— Да-с! Про меня напечатали! Теперь обо мне вся Россия знает! Вы, мамаша, спрячьте этот нумер на память! Будем читать иногда. Поглядите!",
            "Митя вытащил из кармана нумер газеты, подал отцу и ткнул пальцем в место, обведенное синим карандашом.",
            "— Читайте!",
            "Отец надел очки.",
            "— Читайте же!",
            "Мамаша взглянула на образ и перекрестилась. Папаша кашлянул и начал читать:",
            "«29-го декабря, в одиннадцать часов вечера, коллежский регистратор Дмитрий Кулдаров…",
            "— Видите, видите? Дальше!",
            "…коллежский регистратор Дмитрий Кулдаров, выходя из портерной, что на Малой Бронной, в доме Козихина, и находясь в нетрезвом состоянии…",
            "— Это я с Семеном Петровичем… Всё до тонкостей описано! Продолжайте! Дальше! Слушайте!",
            "…и находясь в нетрезвом состоянии, поскользнулся и упал под лошадь стоявшего здесь извозчика, крестьянина дер. Дурыкиной, Юхновского уезда, Ивана Дротова. Испуганная лошадь, перешагнув через Кулдарова и протащив через него сани с находившимся в них второй гильдии московским купцом Степаном Луковым, помчалась по улице и была задержана дворниками. Кулдаров, вначале находясь в бесчувственном состоянии, был отведен в полицейский участок и освидетельствован врачом. Удар, который он получил по затылку…",
            "— Это я об оглоблю, папаша. Дальше! Вы дальше читайте!",
            "…который он получил по затылку, отнесен к легким. О случившемся составлен протокол. Потерпевшему подана медицинская помощь»…",
            "— Велели затылок холодной водой примачивать. Читали теперь? А? То-то вот! Теперь по всей России пошло! Дайте сюда!",
            "Митя схватил газету, сложил ее и сунул в карман.",
            "— Побегу к Макаровым, им покажу… Надо еще Иваницким показать, Наталии Ивановне, Анисиму Васильичу… Побегу! Прощайте!",
            "Митя надел фуражку с кокардой и, торжествующий, радостный, выбежал на улицу.",
        ],
        "guide": "Chekhov turns a minor newspaper accident into a comedy about fame. Notice the gap between Mitya's excited repetitions and the humiliating content his father reads aloud.",
        "vocab": [("взъерошенный", "disheveled"), ("гласность", "publicity; openness"), ("коллежский регистратор", "a low civil-service rank"), ("извозчик", "cab driver"), ("затылок", "back of the head")],
    },
    {
        "slug": "02_turgenev_vorobey", "title": "Воробей", "author": "Иван Тургенев", "year": "1878", "form": "Стихотворение в прозе",
        "source": "https://ru.wikisource.org/wiki/Воробей_(Тургенев)",
        "paragraphs": [
            "Я возвращался с охоты и шел по аллее сада. Собака бежала впереди меня.",
            "Вдруг она уменьшила свои шаги и начала красться, как бы зачуяв перед собою дичь.",
            "Я глянул вдоль аллеи и увидел молодого воробья с желтизной около клюва и пухом на голове. Он упал из гнезда (ветер сильно качал березы аллеи) и сидел неподвижно, беспомощно растопырив едва прораставшие крылышки.",
            "Моя собака медленно приближалась к нему, как вдруг, сорвавшись с близкого дерева, старый черногрудый воробей камнем упал перед самой ее мордой — и весь взъерошенный, искаженный, с отчаянным и жалким писком прыгнул раза два в направлении зубастой раскрытой пасти.",
            "Он ринулся спасать, он заслонил собою свое детище… но все его маленькое тело трепетало от ужаса, голосок одичал и охрип, он замирал, он жертвовал собою!",
            "Каким громадным чудовищем должна была ему казаться собака! И всё-таки он не мог усидеть на своей высокой, безопасной ветке… Сила, сильнее его воли, сбросила его оттуда.",
            "Мой Трезор остановился, попятился… Видно, и он признал эту силу.",
            "Я поспешил отозвать смущенного пса — и удалился, благоговея.",
            "Да; не смейтесь. Я благоговел перед той маленькой, героической птицей, перед любовным ее порывом.",
            "Любовь, думал я, сильнее смерти и страха смерти. Только ею, только любовью держится и движется жизнь.",
        ],
        "guide": "A brief observed incident expands into a prose poem about sacrificial love. Track how the scale changes: the sparrow is physically tiny but morally immense.",
        "vocab": [("зачуяв", "having scented"), ("дичь", "game animal"), ("взъерошенный", "ruffled"), ("попятился", "backed away"), ("благоговея", "with reverence")],
    },
    {
        "slug": "03_tolstoy_lev_i_mysh", "title": "Лев и мышь", "author": "Лев Толстой", "year": "1875", "form": "Басня в прозе",
        "source": "https://ru.wikisource.org/wiki/Лев_и_мышь_(Эзоп;_Лев_Толстой)",
        "paragraphs": [
            "Лев спал. Мышь пробежала ему по телу. Он проснулся и поймал её. Мышь стала просить, чтобы он пустил её; она сказала:",
            "— Если ты меня пустишь, и я тебе добро сделаю.",
            "Лев засмеялся, что мышь обещает ему добро сделать, и пустил её.",
            "Потом охотники поймали льва и привязали верёвкой к дереву. Мышь услыхала львиный рёв, прибежала, перегрызла верёвку и сказала:",
            "— Помнишь, ты смеялся, не думал, чтобы я могла тебе добро сделать, а теперь видишь, — бывает и от мыши добро.",
        ],
        "guide": "Tolstoy's plain retelling is designed for beginning readers. Short clauses and repeated words carry a complete reversal of power.",
        "vocab": [("пустил", "let go"), ("добро", "good; a good deed"), ("охотники", "hunters"), ("привязали", "tied"), ("перегрызла", "gnawed through")],
    },
    {
        "slug": "04_korolenko_ogonki", "title": "Огоньки", "author": "Владимир Короленко", "year": "1900", "form": "Философская миниатюра",
        "source": "https://ru.wikisource.org/wiki/Огоньки_(Короленко)/Версия_2",
        "paragraphs": [
            "Как-то давно, темным осенним вечером, случилось мне плыть по угрюмой сибирской реке. Вдруг на повороте реки, впереди, под темными горами мелькнул огонек.",
            "Мелькнул ярко, сильно, совсем близко…",
            "— Ну, слава богу! — сказал я с радостью, — близко ночлег!",
            "Гребец повернулся, посмотрел через плечо на огонь и опять апатично налег на весла.",
            "— Далече!",
            "Я не поверил: огонек так и стоял, выступая вперед из неопределенной тьмы. Но гребец был прав: оказалось, действительно, далеко.",
            "Свойство этих ночных огней — приближаться, побеждая тьму, и сверкать, и обещать, и манить своею близостью. Кажется, вот-вот еще два-три удара веслом, — и путь кончен… А между тем — далеко!..",
            "И долго мы еще плыли по темной, как чернила, реке. Ущелья и скалы выплывали, надвигались и уплывали, оставаясь назади и теряясь, казалось, в бесконечной дали, а огонек всё стоял впереди, переливаясь и маня, — всё так же близко, и всё так же далеко…",
            "Мне часто вспоминается теперь и эта темная река, затененная скалистыми горами, и этот живой огонек. Много огней и раньше и после манили не одного меня своею близостью. Но жизнь течет всё в тех же угрюмых берегах, а огни еще далеко. И опять приходится налегать на весла…",
            "Но всё-таки… всё-таки впереди — огни!..",
        ],
        "guide": "A river journey becomes an extended metaphor for hope. Repeated contrasts—near/far, darkness/light—transform a physical light into an ethical orientation.",
        "vocab": [("угрюмый", "gloomy"), ("огонек", "little light"), ("гребец", "rower"), ("далече", "far away; colloquial/archaic"), ("ущелье", "gorge")],
    },
]

def story_markup(item: dict) -> str:
    body = "".join(f'<p>{html.escape(p)}</p>' for p in item["paragraphs"])
    vocab = "".join(f'<li><b>{html.escape(a)}</b><span>{html.escape(b)}</span></li>' for a, b in item["vocab"])
    return f'''<article class="prose-reading" lang="ru"><p class="byline">{html.escape(item['author'])} · {item['year']} · {html.escape(item['form'])}</p>{body}</article><section class="study-card" contenteditable="false" lang="en"><h2>Reading guide</h2><p>{html.escape(item['guide'])}</p><h3>Core vocabulary</h3><ul>{vocab}</ul></section>'''


def translation_card(item: dict) -> str:
    query = quote(f'"{item["title"]}" {item["author"]} English translation')
    return f'''<section class="card translation-card" lang="en"><h2>English translations</h2><p>External editions are provided for comparison. Wording and paragraph divisions may differ from this Russian text; these links are not paragraph-by-paragraph alignments.</p><div class="translation-links"><a href="https://en.wikisource.org/w/index.php?search={query}" target="_blank" rel="noreferrer">Search English Wikisource <span aria-hidden="true">↗</span></a><a href="https://archive.org/search?query={query}" target="_blank" rel="noreferrer">Search Internet Archive <span aria-hidden="true">↗</span></a></div></section>'''

def build_one(item: dict) -> None:
    folder = BASE / item["slug"]
    folder.mkdir(parents=True, exist_ok=True)
    plain = "\n\n".join(item["paragraphs"])
    page = build_html(plain, [], item["source"], chapter_title=item["title"], editor_title=f"{item['title']} · {item['author']} · Russian Prose Reader", storage_key=f"russian-prose-{item['slug']}-v1", file_stem=f"russian_prose_{item['slug']}", inline_notes=[], review_notes=[], reading_notes=[], global_terms=[], home_href="../../../index.html#russian_short_stories", theme_href="../../../workspace_theme.css", shared_library_href="../index.html", shared_library_label="Русские рассказы", source_site_label="Викитека")
    page, count = re.subn(r'(<section id="editor" class="editor"[^>]*>)[\s\S]*?(</section>)', lambda m: m.group(1) + story_markup(item) + m.group(2), page, count=1)
    if count != 1: raise RuntimeError("Reader editor body not found")
    page = page.replace('<aside class="sidebar">', '<aside class="sidebar">' + translation_card(item), 1)
    styles = '''<style>#editor{max-width:920px;margin-inline:auto;font-family:Georgia,"Times New Roman",serif;font-size:clamp(18px,1.7vw,23px);line-height:1.85}.byline{color:#5f6368;font:600 13px/1.4 Arial,sans-serif;text-indent:0!important}.prose-reading>p:not(.byline){margin:.85em 0}.study-card{margin:3em 0 1em;padding:20px;border:1px solid #dadce0;border-radius:10px;background:#f8f9fa;font:16px/1.65 Arial,sans-serif}.study-card h2,.study-card h3{margin:.2em 0 .65em}.study-card ul{display:grid;gap:7px;padding:0;list-style:none}.study-card li{display:grid;grid-template-columns:minmax(140px,.35fr) 1fr;gap:12px;padding-top:7px;border-top:1px solid #e1e4e8}.study-card li span{color:#5f6368}.translation-card p{margin:0 0 10px;color:#5f6368;font:12px/1.55 Arial,sans-serif}.translation-links{display:grid;gap:7px}.translation-links a{display:flex;justify-content:space-between;gap:8px;padding:9px 10px;border:1px solid #c7d3e3;border-radius:6px;background:#f8fbff;color:#174ea6;text-decoration:none;font:700 12px/1.35 Arial,sans-serif}.translation-links a:hover{border-color:#174ea6;background:#e8f0fe}@media(max-width:600px){.study-card li{grid-template-columns:1fr;gap:1px}}</style>'''
    page = page.replace("</head>", styles + "</head>", 1).replace("</body>", '<script src="../../../mobile_pwa.js"></script></body>', 1)
    (folder / "editor.html").write_text(page, encoding="utf-8")

def build_landing() -> None:
    cards = "".join(f'<article><span>{n:02d}</span><div><small>{html.escape(s["author"])} · {html.escape(s["form"])}</small><h2>{html.escape(s["title"])}</h2></div><a href="{s["slug"]}/editor.html?view=annotated">Читать</a></article>' for n, s in enumerate(STORIES, 1))
    page = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Русские рассказы · Reader</title><link rel="stylesheet" href="../workspace_theme.css"><style>*{{box-sizing:border-box}}body{{margin:0;background:#f1f3f4;color:#202124;font-family:Arial,sans-serif}}main{{width:min(980px,calc(100% - 28px));margin:28px auto 80px}}header,section{{padding:26px;border:1px solid #dadce0;border-radius:12px;background:#fff}}header{{background:linear-gradient(135deg,#254b45,#70452d);color:#fff}}header a{{color:#fff}}h1{{margin:.15em 0;font:700 clamp(36px,7vw,66px)/1.05 Georgia,serif}}header p{{max-width:720px;line-height:1.6}}section{{display:grid;gap:9px;margin-top:16px}}article{{display:grid;grid-template-columns:42px 1fr auto;gap:12px;align-items:center;padding:14px;border:1px solid #e1e4e8;border-radius:9px}}article h2{{margin:3px 0;font:700 21px Georgia,serif}}article small{{color:#5f6368}}article a{{padding:8px 12px;border:1px solid #b7c5dc;border-radius:18px;color:#174ea6;text-decoration:none;font-weight:700}}@media(max-width:560px){{article{{grid-template-columns:32px 1fr}}article a{{grid-column:2;justify-self:start}}}}</style></head><body><main><header><a href="../index.html#russian_short_stories">← Reader library</a><h1>Русские рассказы</h1><p>Complete short prose readings in contrasting forms, presented in Russian with concise English study support.</p></header><section>{cards}</section></main><script src="../workspace_skin.js"></script><script src="../mobile_pwa.js"></script></body></html>'''
    (BASE / "index.html").write_text(page, encoding="utf-8")

if __name__ == "__main__":
    for story in STORIES: build_one(story)
    build_landing()
    print(f"Built {len(STORIES)} Russian short-prose readings")
