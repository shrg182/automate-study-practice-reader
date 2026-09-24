#!/usr/bin/env python3
"""Build the three-part meridian reading tutorial for Reader Articles."""

from __future__ import annotations

from datetime import date
from html import escape
import json
from pathlib import Path
import re
import uuid


BASE = Path(__file__).resolve().parent
ENTRIES = BASE / "entries"
SOURCE_URL = "https://chat.deepseek.com/share/km6zn4kmhm71ody7cp"
PUBLISHED = "2026-09-20"
BYLINE = "Reader tutorial · assembled from user-provided material"


POINTS = [
    ("手太阴肺经", 11, "中府、云门、天府、侠白、尺泽、孔最、列缺、经渠、太渊、鱼际、少商"),
    ("手厥阴心包经", 9, "天池、天泉、曲泽、郄门、间使、内关、大陵、劳宫、中冲"),
    ("手少阴心经", 9, "极泉、青灵、少海、灵道、通里、阴郄、神门、少府、少冲"),
    ("手阳明大肠经", 20, "商阳、二间、三间、合谷、阳溪、偏历、温溜、下廉、上廉、手三里、曲池、肘髎、手五里、臂臑、肩髃、巨骨、天鼎、扶突、口禾髎、迎香"),
    ("手少阳三焦经", 23, "关冲、液门、中渚、阳池、外关、支沟、会宗、三阳络、四渎、天井、清冷渊、消泺、臑会、肩髎、天髎、天牖、翳风、瘈脉、颅息、角孙、耳门、耳和髎、丝竹空"),
    ("手太阳小肠经", 19, "少泽、前谷、后溪、腕骨、阳谷、养老、支正、小海、肩贞、臑俞、天宗、秉风、曲垣、肩外俞、肩中俞、天窗、天容、颧髎、听宫"),
    ("足阳明胃经", 45, "承泣、四白、巨髎、地仓、大迎、颊车、下关、头维、人迎、水突、气舍、缺盆、气户、库房、屋翳、膺窗、乳中、乳根、不容、承满、梁门、关门、太乙、滑肉门、天枢、外陵、大巨、水道、归来、气冲、髀关、伏兔、阴市、梁丘、犊鼻、足三里、上巨虚、条口、下巨虚、丰隆、解溪、冲阳、陷谷、内庭、厉兑"),
    ("足少阳胆经", 44, "瞳子髎、听会、上关、颔厌、悬颅、悬厘、曲鬓、率谷、天冲、浮白、头窍阴、完骨、本神、阳白、头临泣、目窗、正营、承灵、脑空、风池、肩井、渊腋、辄筋、日月、京门、带脉、五枢、维道、居髎、环跳、风市、中渎、膝阳关、阳陵泉、阳交、外丘、光明、阳辅、悬钟、丘墟、足临泣、地五会、侠溪、足窍阴"),
    ("足太阳膀胱经", 67, "睛明、攒竹、眉冲、曲差、五处、承光、通天、络却、玉枕、天柱、大杼、风门、肺俞、厥阴俞、心俞、督俞、膈俞、肝俞、胆俞、脾俞、胃俞、三焦俞、肾俞、气海俞、大肠俞、关元俞、小肠俞、膀胱俞、中膂俞、白环俞、上髎、次髎、中髎、下髎、会阳、承扶、殷门、浮郄、委阳、委中、附分、魄户、膏肓、神堂、譩譆、膈关、魂门、阳纲、意舍、胃仓、肓门、志室、胞肓、秩边、合阳、承筋、承山、飞扬、跗阳、昆仑、仆参、申脉、金门、京骨、束骨、足通谷、至阴"),
    ("足太阴脾经", 21, "隐白、大都、太白、公孙、商丘、三阴交、漏谷、地机、阴陵泉、血海、箕门、冲门、府舍、腹结、大横、腹哀、食窦、天溪、胸乡、周荣、大包"),
    ("足厥阴肝经", 14, "大敦、行间、太冲、中封、蠡沟、中都、膝关、曲泉、阴包、足五里、阴廉、急脉、章门、期门"),
    ("足少阴肾经", 27, "涌泉、然谷、太溪、大钟、水泉、照海、复溜、交信、筑宾、阴谷、横骨、大赫、气穴、四满、中注、肓俞、商曲、石关、阴都、腹通谷、幽门、步廊、神封、灵墟、神藏、彧中、俞府"),
]

REN = "会阴、曲骨、中极、关元、石门、气海、阴交、神阙、水分、下脘、建里、中脘、上脘、巨阙、鸠尾、中庭、膻中、玉堂、紫宫、华盖、璇玑、天突、廉泉、承浆"
DU = "长强、腰俞、腰阳关、命门、悬枢、脊中、中枢、筋缩、至阳、灵台、神道、身柱、陶道、大椎、哑门、风府、脑户、强间、后顶、百会、前顶、囟会、上星、神庭、素髎、水沟、兑端、龈交"


def point_rows() -> str:
    return "".join(
        f"<tr><th>{escape(name)}</th><td>{count}</td><td>{escape(names)}</td></tr>"
        for name, count, names in POINTS
    )


def series_navigation(index: int) -> str:
    links = []
    if index:
        previous = ARTICLES[index - 1]
        links.append(f'<a href="../{previous["slug"]}/editor.html">← 上一篇：{escape(previous["title"])}</a>')
    links.append('<a href="../../../index.html#reader_articles">返回 Reader Articles</a>')
    if index + 1 < len(ARTICLES):
        following = ARTICLES[index + 1]
        links.append(f'<a href="../{following["slug"]}/editor.html">下一篇：{escape(following["title"])} →</a>')
    return '<nav class="series-navigation" aria-label="教程导航">' + "".join(links) + "</nav>"


ARTICLES = [
    {
        "slug": "meridian_tutorial_01_framework",
        "title": "经络阅读教程（一）：先建立十二经脉的框架",
        "body": """
<p><strong>学习目标：</strong>读完本文，能够区分“经络”与“经脉”，按手足、阴阳和脏腑说出十二经脉，并用四句走向规律和一条流注链组织记忆。</p>
<p class="callout"><strong>安全说明：</strong>本文是传统医学知识阅读材料，不提供诊断或自行针刺指导。穴位定位与针刺操作应由受过训练、符合当地资质要求的专业人员完成。</p>
<h2>一、先把名称说准确</h2>
<p>“经络”是经脉与络脉的总称。日常所说的“十二经络”，更准确的名称是<strong>十二经脉</strong>或<strong>十二正经</strong>。可以先把经脉理解为系统中的主干，把络脉理解为由主干分出的网络。这是一种传统理论模型，不应直接等同于现代解剖中的神经或血管。</p>
<h2>二、十二经脉的四组分类</h2>
<table><thead><tr><th>类别</th><th>三条经脉</th></tr></thead><tbody>
<tr><th>手三阴</th><td>手太阴肺经、手厥阴心包经、手少阴心经</td></tr>
<tr><th>手三阳</th><td>手阳明大肠经、手少阳三焦经、手太阳小肠经</td></tr>
<tr><th>足三阳</th><td>足阳明胃经、足少阳胆经、足太阳膀胱经</td></tr>
<tr><th>足三阴</th><td>足太阴脾经、足厥阴肝经、足少阴肾经</td></tr>
</tbody></table>
<p><strong>读名方法：</strong>每个名称依次给出三条信息：在手还是在足、属于哪一种阴阳层次、联系哪个传统脏腑系统。例如“足少阴肾经”可拆为“足—少阴—肾”。</p>
<h2>三、六组表里配对</h2>
<p>肺—大肠，心包—三焦，心—小肠，脾—胃，肝—胆，肾—膀胱。配对属于传统功能联系，不表示两个现代解剖器官直接相连。</p>
<h2>四、用四句话掌握走向</h2>
<ul><li>手三阴：从胸走手。</li><li>手三阳：从手走头。</li><li>足三阳：从头走足。</li><li>足三阴：从足走腹胸。</li></ul>
<p>阅读具体循行前，先判断它属于哪一组，再检查起止的大方向。这个框架比一开始逐字背诵长路线更稳固。</p>
<h2>五、把流注读成一条闭环</h2>
<p><strong>肺 → 大肠 → 胃 → 脾 → 心 → 小肠 → 膀胱 → 肾 → 心包 → 三焦 → 胆 → 肝 → 肺。</strong></p>
<p>第一遍只记顺序；第二遍标出每一次“阴—阳”或“阳—阴”的转换；第三遍再把手足与表里配对叠加进去。这样形成的是可解释的结构，而不是孤立名单。</p>
<h2>六、自测</h2>
<ol><li>“十二经络”为什么不是最严谨的名称？</li><li>不看正文，写出四类经脉及每类的走向。</li><li>找出肝经的表里经，并指出它在流注链中的前后两经。</li><li>为什么不能把经脉直接称为神经或血管？</li></ol>
""",
    },
    {
        "slug": "meridian_tutorial_02_extraordinary_vessels",
        "title": "经络阅读教程（二）：奇经八脉与八脉交会穴",
        "body": """
<p><strong>学习目标：</strong>说出奇经八脉的名称，理解它们与十二经脉的区别，并识别八脉交会穴的配属关系。</p>
<p class="callout"><strong>学习边界：</strong>下文描述传统理论中的功能关系，不等同于现代临床疗效证明，也不构成针灸处方。</p>
<h2>一、“奇”是什么意思</h2>
<p>奇经八脉是不同于十二正经的一组特殊经脉。它们不参加十二经脉的循环流注，没有十二正经那样的阴阳表里配对。传统教材常用“联络、统率、调节、蓄溢”概括其作用。</p>
<h2>二、八脉总览</h2>
<table><thead><tr><th>名称</th><th>阅读抓手</th></tr></thead><tbody>
<tr><th>督脉</th><td>行于后正中线；传统称“阳脉之海”。</td></tr>
<tr><th>任脉</th><td>行于前正中线；传统称“阴脉之海”，并与胞胎、生殖相关。</td></tr>
<tr><th>冲脉</th><td>传统称“十二经之海”和“血海”。</td></tr>
<tr><th>带脉</th><td>横向环腰，用“约束纵行诸经”帮助记忆。</td></tr>
<tr><th>阴维脉</th><td>维系一身阴经。</td></tr>
<tr><th>阳维脉</th><td>维系一身阳经。</td></tr>
<tr><th>阴跷脉</th><td>传统上联系下肢内侧运动、眼睑开合与睡眠。</td></tr>
<tr><th>阳跷脉</th><td>传统上联系下肢外侧运动、眼睑开合与睡眠。</td></tr>
</tbody></table>
<h2>三、为什么常把它们比作湖泊</h2>
<p>一种常见比喻是：十二经脉如江河，奇经八脉如湖泊水库。十二经气血充盛时，奇经可以蓄存；十二经不足时，奇经可以调节。这个比喻用于理解传统体系内部的关系，不是对人体存在实体“气血水库”的解剖声明。</p>
<h2>四、任督与“十四经”</h2>
<p>任脉与督脉具有本经穴位。十二正经加任、督二脉，合称<strong>十四经</strong>。其余六条奇经没有本经专属穴位，而是借助与十二经相通的穴位建立联系。</p>
<h2>五、八脉交会穴</h2>
<table><thead><tr><th>穴位</th><th>所属正经</th><th>所通奇经</th></tr></thead><tbody>
<tr><td>公孙</td><td>足太阴脾经</td><td>冲脉</td></tr><tr><td>内关</td><td>手厥阴心包经</td><td>阴维脉</td></tr>
<tr><td>后溪</td><td>手太阳小肠经</td><td>督脉</td></tr><tr><td>申脉</td><td>足太阳膀胱经</td><td>阳跷脉</td></tr>
<tr><td>足临泣</td><td>足少阳胆经</td><td>带脉</td></tr><tr><td>外关</td><td>手少阳三焦经</td><td>阳维脉</td></tr>
<tr><td>列缺</td><td>手太阴肺经</td><td>任脉</td></tr><tr><td>照海</td><td>足少阴肾经</td><td>阴跷脉</td></tr>
</tbody></table>
<h2>六、自测</h2>
<ol><li>奇经八脉与十二经脉在流注和表里关系上有何不同？</li><li>为什么“十四经”只从奇经八脉中加入任、督二脉？</li><li>分别找出通于带脉、任脉和督脉的交会穴。</li><li>“江河—湖泊”比喻能够说明什么，又不能证明什么？</li></ol>
""",
    },
    {
        "slug": "meridian_tutorial_03_point_reference",
        "title": "经络阅读教程（三）：十四经穴名称检索表",
        "body": f"""
<p><strong>使用方法：</strong>本篇是配合前两篇使用的名称索引。先确认经脉分类和走向，再按“首穴 → 末穴”的顺序阅读。穴名表不包含定位、针刺深度、禁忌或治疗建议。</p>
<p class="callout"><strong>安全说明：</strong>请勿仅凭名称表自行针刺。错误定位、深度或方向可能造成感染、出血、气胸或其他严重损伤。</p>
<h2>一、数量框架</h2>
<p>十二正经左右对称，共309对（618个双侧穴位）；任脉24穴、督脉28穴位于正中线，为52个单穴。按标准穴名计数，十二正经与任督二脉合计<strong>361个十四经穴</strong>。</p>
<h2>二、十二正经</h2>
<table class="point-table"><thead><tr><th>经脉</th><th>穴数</th><th>穴位（首穴 → 末穴）</th></tr></thead><tbody>{point_rows()}</tbody></table>
<h2>三、任脉与督脉</h2>
<h3>任脉（24穴）</h3><p>{REN}</p>
<h3>督脉（28穴）</h3><p>{DU}</p>
<h2>四、检索练习</h2>
<ol><li>找出十二正经中穴数最多与最少的经脉。</li><li>查找列缺、后溪、公孙、内关分别属于哪条正经。</li><li>把任脉与督脉的首穴、末穴分别写出。</li><li>任选一条经，只按每五个穴为一组朗读；合上页面后复述组间顺序。</li></ol>
<h2>五、下一步需要什么资料</h2>
<p>名称表适合检索，却不足以学习准确定位。后续篇章若要加入体表定位、骨度分寸、解剖层次、针刺风险或主治证据，需要采用权威教材或标准，并对图像版权与医学安全进行单独审核。</p>
""",
    },
]


PRINT_CSS = """
@page{size:A4;margin:17mm}*{box-sizing:border-box}body{margin:0;color:#242522;font:11pt/1.72 Georgia,"Songti SC",serif}article{max-width:185mm;margin:auto}header{text-align:center;border-bottom:2px solid #365f4d;padding-bottom:14px}.type{color:#176b4b;font:700 9pt Arial,sans-serif;letter-spacing:.1em;text-transform:uppercase}h1{margin:8px 0 6px;font-size:24pt;line-height:1.25}.meta{color:#626861;font:9pt Arial,sans-serif}.body{padding-top:18px}.body p{margin:0 0 10pt}.callout{padding:10px 12px;border-left:4px solid #b47d2e;background:#fff7df}table{width:100%;margin:14px 0;border-collapse:collapse;font:9.2pt/1.5 Arial,"PingFang SC",sans-serif}th,td{padding:7px;border:1px solid #cbd2cb;text-align:left;vertical-align:top}th{background:#edf4ef;color:#244c3a}.point-table th:first-child{width:6em;min-width:6em;white-space:nowrap}.point-table th:nth-child(2),.point-table td:nth-child(2){width:3em;min-width:3em;white-space:nowrap}.point-table td:last-child{line-height:1.75}a{color:#176b4b}.series-navigation{display:flex;justify-content:space-between;gap:12px;margin:0 0 20px;padding:10px 0;border-bottom:1px solid #ccd2cc;font:9.5pt Arial,"PingFang SC",sans-serif}.series-navigation a{text-decoration:none}.sources{margin-top:24px;padding-top:12px;border-top:1px solid #ccd2cc;color:#59625c;font-size:9.5pt}@media(max-width:650px){.series-navigation{align-items:flex-start;flex-direction:column}}
"""


def standalone_page(article: dict[str, str], index: int) -> str:
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(article['title'])}</title><style>{PRINT_CSS}</style></head><body><article><header><div class="type">阅读教程 · 第 {index + 1} 篇，共 {len(ARTICLES)} 篇</div><h1>{escape(article['title'])}</h1><div class="meta">{PUBLISHED} · {escape(BYLINE)}</div></header><main class="body">{series_navigation(index)}{article['body']}<section class="sources"><h2>资料说明</h2><p>本教程根据读者提供的 <a href="{SOURCE_URL}">DeepSeek 共享对话</a>重组，并结合 Reader App《中医基础理论》现有的经络章节进行教学化改写。共享对话为 AI 生成材料，名称与数量仍应在用于教学、出版或临床前对照权威标准复核。</p></section>{series_navigation(index)}</main></article></body></html>'''


def editor_page(article: dict[str, str], seed: dict[str, object]) -> str:
    template = (ENTRIES / "reader_app" / "editor.html").read_text(encoding="utf-8")
    template = re.sub(r"<title>.*?</title>", f"<title>{escape(article['title'])} · Reader Editor</title>", template, count=1)
    seed_json = json.dumps(seed, ensure_ascii=False).replace("</", "<\\/")
    template = re.sub(
        r'<script id="readerArticleSeed" type="application/json">.*?</script>',
        lambda _: f'<script id="readerArticleSeed" type="application/json">{seed_json}</script>',
        template,
        count=1,
        flags=re.DOTALL,
    )
    return template


def build() -> None:
    for index, article in enumerate(ARTICLES):
        target = ENTRIES / article["slug"]
        target.mkdir(parents=True, exist_ok=True)
        stable_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"reader:{article['slug']}"))
        seed = {
            "schema": "reader-article-v1",
            "id": stable_id,
            "savedAt": f"{PUBLISHED}T12:00:00+08:00",
            "metadata": {"type": "Reading material", "date": PUBLISHED, "title": article["title"], "byline": BYLINE},
            "bodyHTML": series_navigation(index) + article["body"] + series_navigation(index),
            "footnotes": [],
            "notes": f"Source conversation: {SOURCE_URL}\nEducational use only; not medical advice or self-needling instruction.",
            "splitPercent": 50,
        }
        (target / f"{article['slug']}_backup.json").write_text(json.dumps(seed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (target / f"{article['slug']}.html").write_text(standalone_page(article, index), encoding="utf-8")
        (target / "editor.html").write_text(editor_page(article, seed), encoding="utf-8")


if __name__ == "__main__":
    build()
