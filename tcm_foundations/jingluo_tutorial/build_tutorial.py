#!/usr/bin/env python3
"""Build the 十二正经与奇经八脉 study tutorial."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path
import re
from urllib.parse import quote_plus


BASE = Path(__file__).resolve().parent

COMMONS_SOURCES = {
    "15_chong": "https://commons.wikimedia.org/wiki/File:Acu-moxa_chart%3B_chongmai_(Penetrating_Vessel),_Chinese_Wellcome_L0037939.jpg",
    "16_dai": "https://commons.wikimedia.org/wiki/File:Acu-moxa_chart%3B_daimai_(Belt_Vessel),_Chinese_woodcut_Wellcome_L0037940.jpg",
    "17_yinqiao": "https://commons.wikimedia.org/wiki/File:Acu-moxa_chart%3B_yinqiao_mai_(Yin_Heel_Vessel),_Chinese_Wellcome_L0037942.jpg",
    "18_yangqiao": "https://commons.wikimedia.org/wiki/File:Acu-moxa_chart%3B_yangqiao_mai,_Chinese_woodcut_Wellcome_L0037941.jpg",
    "19_yinwei": "https://commons.wikimedia.org/wiki/File:Acu-moxa_chart%3B_yinwei_mai_(Yin_Tie_Vessel),_Chinese_Wellcome_L0037944.jpg",
    "20_yangwei": "https://commons.wikimedia.org/wiki/File:Acu-moxa_chart%3B_yangwei_mai_(Yang_Tie_Vessel),_Chinese_Wellcome_L0037943.jpg",
}

# Points are a curated set of commonly taught landmarks, not treatment prescriptions.
CHANNELS = [
    ("01_lung", "手太阴肺经", "LU", "十二正经 · 手三阴", "起于中焦，下络大肠，返循胃口，上膈属肺；从肺系横出腋下，沿上肢内侧前缘至拇指桡侧端，并由列缺处分支至食指，与大肠经相接。", "传统上属肺、络大肠，联系肺系、胸、喉及上肢内侧前缘；常用于记忆呼吸系统、咽喉与经脉所过部位的传统主治归类。", "中府 LU1、云门 LU2、天府 LU3、侠白 LU4、尺泽 LU5、孔最 LU6、列缺 LU7、经渠 LU8、太渊 LU9、鱼际 LU10、少商 LU11"),
    ("02_large_intestine", "手阳明大肠经", "LI", "十二正经 · 手三阳", "起于食指桡侧端，沿上肢外侧前缘上肩，经颈入下齿、绕口唇、止于对侧鼻旁；内行入缺盆，络肺、属大肠，并与胃经相接。", "传统上属大肠、络肺，联系下齿、口鼻、肩臂及上肢外侧前缘。", "商阳 LI1、二间 LI2、三间 LI3、合谷 LI4、阳溪 LI5、偏历 LI6、温溜 LI7、手三里 LI10、曲池 LI11、臂臑 LI14、肩髃 LI15、扶突 LI18、迎香 LI20"),
    ("03_stomach", "足阳明胃经", "ST", "十二正经 · 足三阳", "起于鼻旁，上行鼻根并入上齿，环口唇、沿面颊下颈；经胸腹下行至足背第二趾外侧端。内行入缺盆、属胃络脾，支脉在足部与脾经相接。", "传统上属胃、络脾，联系面、口齿、咽喉、胸腹和下肢前外侧。", "承泣 ST1、四白 ST2、地仓 ST4、颊车 ST6、下关 ST7、头维 ST8、人迎 ST9、梁门 ST21、天枢 ST25、水道 ST28、归来 ST29、髀关 ST31、梁丘 ST34、犊鼻 ST35、足三里 ST36、上巨虚 ST37、条口 ST38、丰隆 ST40、解溪 ST41、冲阳 ST42、内庭 ST44、厉兑 ST45"),
    ("04_spleen", "足太阴脾经", "SP", "十二正经 · 足三阴", "起于大趾内侧端，沿足内侧、下肢内侧前缘上行，经腹入属脾、络胃，上膈挟咽、连舌根、散舌下；支脉从胃上膈注心中，与心经相接。", "传统上属脾、络胃，联系舌、胸腹和下肢内侧前缘。", "隐白 SP1、大都 SP2、太白 SP3、公孙 SP4、商丘 SP5、三阴交 SP6、漏谷 SP7、地机 SP8、阴陵泉 SP9、血海 SP10、冲门 SP12、府舍 SP13、大横 SP15、大包 SP21"),
    ("05_heart", "手少阴心经", "HT", "十二正经 · 手三阴", "起于心中，出属心系，下膈络小肠；上行挟咽、系目系。体表支从心系出肺，下腋，沿上肢内侧后缘至小指桡侧端，与小肠经相接。", "传统上属心、络小肠，联系心系、咽、目系和上肢内侧后缘。", "极泉 HT1、青灵 HT2、少海 HT3、灵道 HT4、通里 HT5、阴郄 HT6、神门 HT7、少府 HT8、少冲 HT9"),
    ("06_small_intestine", "手太阳小肠经", "SI", "十二正经 · 手三阳", "起于小指尺侧端，沿上肢外侧后缘上肩，交会大椎，入缺盆；内行络心、属小肠。支脉循颈上颊至耳前，另支至目内眦，与膀胱经相接。", "传统上属小肠、络心，联系肩胛、颈、颊、耳、目及上肢外侧后缘。", "少泽 SI1、前谷 SI2、后溪 SI3、腕骨 SI4、阳谷 SI5、养老 SI6、支正 SI7、小海 SI8、肩贞 SI9、臑俞 SI10、天宗 SI11、秉风 SI12、肩外俞 SI14、肩中俞 SI15、天窗 SI16、颧髎 SI18、听宫 SI19"),
    ("07_bladder", "足太阳膀胱经", "BL", "十二正经 · 足三阳", "起于目内眦，上额交巅、入络脑，分支下项；背部两行沿脊柱两旁和肩胛内侧下行，经臀、大腿后侧、腘窝、小腿后外侧至小趾外侧端，与肾经相接。内行络肾、属膀胱。", "传统上属膀胱、络肾，联系眼、头项、脑、背腰、臀及下肢后侧；背俞穴是本经学习重点。", "睛明 BL1、攒竹 BL2、天柱 BL10、大杼 BL11、风门 BL12、肺俞 BL13、心俞 BL15、膈俞 BL17、肝俞 BL18、胆俞 BL19、脾俞 BL20、胃俞 BL21、肾俞 BL23、大肠俞 BL25、膀胱俞 BL28、次髎 BL32、委中 BL40、膏肓 BL43、志室 BL52、承山 BL57、昆仑 BL60、申脉 BL62、至阴 BL67"),
    ("08_kidney", "足少阴肾经", "KI", "十二正经 · 足三阴", "起于小趾下，斜走足心，绕内踝后上行下肢内侧后缘，贯脊属肾、络膀胱，再经腹胸至锁骨下；支脉从肾上贯肝膈、入肺、循喉挟舌根，并从肺络心注胸中。", "传统上属肾、络膀胱，联系脊柱、肝肺心、喉舌、胸腹与下肢内侧后缘。", "涌泉 KI1、然谷 KI2、太溪 KI3、大钟 KI4、水泉 KI5、照海 KI6、复溜 KI7、交信 KI8、筑宾 KI9、阴谷 KI10、横骨 KI11、肓俞 KI16、商曲 KI17、石关 KI18、阴都 KI19、通谷 KI20、幽门 KI21、俞府 KI27"),
    ("09_pericardium", "手厥阴心包经", "PC", "十二正经 · 手三阴", "起于胸中，出属心包络，下膈历络三焦；胸中支出胁，经腋下，沿上肢内侧中线入掌中，至中指端；掌中支至无名指，与三焦经相接。", "传统上属心包、络三焦，联系胸、胁、心包和上肢内侧中线。", "天池 PC1、天泉 PC2、曲泽 PC3、郄门 PC4、间使 PC5、内关 PC6、大陵 PC7、劳宫 PC8、中冲 PC9"),
    ("10_sanjiao", "手少阳三焦经", "TE", "十二正经 · 手三阳", "起于无名指尺侧端，经手背沿上肢外侧中线上肩，入缺盆、布膻中、络心包、下膈属三焦；支脉上项绕耳，至眉梢，与胆经相接。", "传统上属三焦、络心包，联系耳、目外眦、颊、颈肩和上肢外侧中线。代码也常写 SJ 或 TB。", "关冲 TE1、液门 TE2、中渚 TE3、阳池 TE4、外关 TE5、支沟 TE6、会宗 TE7、三阳络 TE8、天井 TE10、肩髎 TE14、翳风 TE17、瘈脉 TE18、角孙 TE20、耳门 TE21、丝竹空 TE23"),
    ("11_gallbladder", "足少阳胆经", "GB", "十二正经 · 足三阳", "起于目外眦，多次曲折于头侧，绕耳后下肩；入缺盆后内行络肝属胆，体表支沿胁肋、髋外侧、下肢外侧至第四趾外侧端，足背支至大趾与肝经相接。", "传统上属胆、络肝，联系目、耳、头侧、胁肋、髋和下肢外侧。", "瞳子髎 GB1、听会 GB2、上关 GB3、率谷 GB8、完骨 GB12、阳白 GB14、风池 GB20、肩井 GB21、日月 GB24、带脉 GB26、环跳 GB30、风市 GB31、阳陵泉 GB34、光明 GB37、悬钟 GB39、丘墟 GB40、足临泣 GB41、侠溪 GB43、足窍阴 GB44"),
    ("12_liver", "足厥阴肝经", "LR", "十二正经 · 足三阴", "起于大趾背侧，沿足背、下肢内侧上行，绕阴器、抵小腹，挟胃属肝络胆，上贯膈、布胁肋，循喉后连目系，上额会督脉；支脉从肝贯膈注肺，与肺经循环相接。", "传统上属肝、络胆，联系阴器、小腹、胁肋、咽喉、目系与下肢内侧。", "大敦 LR1、行间 LR2、太冲 LR3、中封 LR4、蠡沟 LR5、中都 LR6、膝关 LR7、曲泉 LR8、足五里 LR10、阴廉 LR11、急脉 LR12、章门 LR13、期门 LR14"),
    ("13_du", "督脉", "GV", "奇经八脉", "起于小腹内，下出会阴，沿脊柱内部和后正中线上行至项、入脑，上巅，沿额鼻至上唇系带。传统文献另述与肾、心和生殖系统相关的分支。", "总督诸阳经，调节阳经经气；联系脊柱、脑、头项和后正中线。督脉有独立穴位序列。", "长强 GV1、腰俞 GV2、命门 GV4、至阳 GV9、身柱 GV12、大椎 GV14、哑门 GV15、风府 GV16、脑户 GV17、百会 GV20、上星 GV23、神庭 GV24、水沟 GV26、龈交 GV28"),
    ("14_ren", "任脉", "CV", "奇经八脉", "起于小腹内，下出会阴，沿腹、胸前正中线上行，经咽喉至下颌；面部支环绕口唇并联系目下。", "总任诸阴经，调节阴经经气；联系生殖、腹胸、咽喉及前正中线。任脉有独立穴位序列。", "会阴 CV1、曲骨 CV2、中极 CV3、关元 CV4、石门 CV5、气海 CV6、神阙 CV8、下脘 CV10、中脘 CV12、上脘 CV13、巨阙 CV14、鸠尾 CV15、膻中 CV17、天突 CV22、廉泉 CV23、承浆 CV24"),
    ("15_chong", "冲脉", "TV", "奇经八脉", "起于胞中（传统表述），出会阴，与肾经并行上腹胸；另有支脉沿脊柱内、下肢内侧及足部循行。具体支路在经典与教材间有表述差异。", "称“十二经脉之海”或“血海”，传统上调节十二经气血，并联系生殖、月经及腹胸。无独立穴位序列。", "公孙 SP4（八脉交会穴）、内关 PC6（配穴）；会阴 CV1、气冲 ST30、横骨 KI11、大赫 KI12、气穴 KI13、四满 KI14、中注 KI15、肓俞 KI16、商曲 KI17、石关 KI18、阴都 KI19、通谷 KI20、幽门 KI21（代表性交会穴）"),
    ("16_dai", "带脉", "BV", "奇经八脉", "起于季胁附近，斜向下行至带脉穴，横行环绕腰腹，如束带状；是奇经中主要横向循行者。", "约束纵行诸经，传统上联系腰腹、带下与下肢经气。无独立穴位序列。", "足临泣 GB41（八脉交会穴）、外关 TE5（配穴）；带脉 GB26、五枢 GB27、维道 GB28（主要交会穴）"),
    ("17_yinqiao", "阴跷脉", "YinHV", "奇经八脉", "起于足舟骨后方，循内踝后上行下肢内侧，经阴部、胸、咽喉，至目内眦与阳跷脉会合。", "传统上调节下肢运动、阴阳开合与睡眠，并联系目内眦。无独立穴位序列。", "照海 KI6（八脉交会穴）、列缺 LU7（配穴）；交信 KI8、睛明 BL1（代表性交会穴）"),
    ("18_yangqiao", "阳跷脉", "YangHV", "奇经八脉", "起于足跟外侧，循外踝后上行下肢外侧，经胁、肩、颈、口角至目内眦，再上额至项后。", "传统上调节下肢运动、左右张力、眼睑开合与睡眠。无独立穴位序列。", "申脉 BL62（八脉交会穴）、后溪 SI3（配穴）；仆参 BL61、跗阳 BL59、居髎 GB29、臑俞 SI10、肩髃 LI15、巨骨 LI16、地仓 ST4、巨髎 ST3、承泣 ST1、睛明 BL1、风池 GB20（代表性交会穴）"),
    ("19_yinwei", "阴维脉", "YinLV", "奇经八脉", "起于小腿内侧，沿下肢内侧上行至腹、胸，与脾经、肝经及任脉相会，止于咽喉附近。", "“维络诸阴”，传统上联络阴经，重点联系胸腹与心胸。无独立穴位序列。", "内关 PC6（八脉交会穴）、公孙 SP4（配穴）；筑宾 KI9、府舍 SP13、大横 SP15、腹哀 SP16、期门 LR14、天突 CV22、廉泉 CV23（代表性交会穴）"),
    ("20_yangwei", "阳维脉", "YangLV", "奇经八脉", "起于足跟外侧，沿下肢外侧、躯干侧面上肩，经颈至耳后、额侧，最后与督脉会于项后。", "“维络诸阳”，传统上联络阳经，重点联系身体外侧、肩项和头部。无独立穴位序列。", "外关 TE5（八脉交会穴）、足临泣 GB41（配穴）；金门 BL63、阳交 GB35、臑俞 SI10、天髎 TE15、肩井 GB21、头临泣 GB15、目窗 GB16、正营 GB17、承灵 GB18、脑空 GB19、风池 GB20、风府 GV16、哑门 GV15（代表性交会穴）"),
]


def inline_markdown(text: str) -> str:
    """Escape text while retaining ordinary Markdown links."""
    output: list[str] = []
    cursor = 0
    for match in re.finditer(r"\[([^\]]+)\]\((https?://[^)]+)\)", text):
        output.append(escape(text[cursor:match.start()]))
        output.append(
            f'<a href="{escape(match.group(2), quote=True)}" target="_blank" '
            f'rel="noreferrer">{escape(match.group(1))}</a>'
        )
        cursor = match.end()
    output.append(escape(text[cursor:]))
    return "".join(output)


def overview_markdown_to_html(markdown_text: str) -> str:
    """Convert the limited Markdown used by the collected AI Overviews."""
    output: list[str] = []
    list_type: str | None = None

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            output.append(f"</{list_type}>")
            list_type = None

    for raw_line in markdown_text.splitlines():
        line = raw_line.strip()
        if not line:
            close_list()
            continue
        if re.fullmatch(r"-{3,}", line):
            close_list()
            output.append("<hr>")
            continue
        heading = re.match(r"^#{2,6}\s+(.+)$", line)
        if heading:
            close_list()
            output.append(f"<h3>{inline_markdown(heading.group(1))}</h3>")
            continue
        unordered = re.match(r"^[*+-]\s+(.+)$", line)
        ordered = re.match(r"^\d+\.\s+(.+)$", line)
        if unordered or ordered:
            wanted = "ul" if unordered else "ol"
            if list_type != wanted:
                close_list()
                list_type = wanted
                output.append(f"<{wanted}>")
            output.append(f"<li>{inline_markdown((unordered or ordered).group(1))}</li>")
            continue
        close_list()
        output.append(f"<p>{inline_markdown(line)}</p>")
    close_list()
    return "".join(output)


def load_ai_overviews() -> dict[str, str]:
    source = (BASE / "google_ai_overviews.md").read_text(encoding="utf-8")
    sections = re.split(r"^={20,}\s*$", source, flags=re.MULTILINE)[1:]
    if len(sections) != len(CHANNELS):
        raise ValueError(f"Expected {len(CHANNELS)} AI Overview sections, found {len(sections)}")
    overviews: dict[str, str] = {}
    for expected, section in zip(CHANNELS, sections):
        match = re.match(r"\s*#\s*(\d+)\s*\n([^\n]+)\n(.*)", section, flags=re.DOTALL)
        if not match:
            raise ValueError("Invalid AI Overview section header")
        number, name, body = match.groups()
        expected_number = int(expected[0].split("_", 1)[0])
        if int(number) != expected_number or name.strip() != expected[1]:
            raise ValueError(
                f"AI Overview mismatch: expected {expected_number:02d} {expected[1]}, "
                f"found {number} {name.strip()}"
            )
        overviews[expected[0]] = overview_markdown_to_html(body.strip())
    return overviews


AI_OVERVIEWS = load_ai_overviews()


STYLE = """
*{box-sizing:border-box}:root{--ink:#25231f;--green:#176b4b;--gold:#9a692f;--line:#d8d2c6;--paper:#fff;--wash:#f3f1eb}body{margin:0;background:var(--wash);color:var(--ink);font-family:Arial,"PingFang SC",sans-serif}header{position:sticky;top:0;z-index:5;display:flex;gap:14px;align-items:center;padding:11px 18px;border-bottom:1px solid var(--line);background:#fffdf8ed;backdrop-filter:blur(9px)}header a{color:var(--green);text-decoration:none}header strong{flex:1}.toolbar{display:flex;gap:7px;flex-wrap:wrap;padding:8px 18px;border-bottom:1px solid var(--line);background:#fff}body.mobile-edit-mode>.toolbar{display:flex!important;position:sticky;top:0;z-index:210}.toolbar button{padding:7px 10px;border:1px solid #cfc8ba;border-radius:5px;background:#fff;cursor:pointer}.toolbar .annotation-tool{border-color:#9fc7b4;background:#eef7f1;color:var(--green)}main{width:min(1000px,calc(100% - 28px));margin:24px auto 90px}.paper{padding:clamp(22px,5vw,52px);border:1px solid var(--line);background:var(--paper);box-shadow:0 2px 12px #322b2010}.paper:focus{outline:2px solid #9fc7b4;outline-offset:3px}.eyebrow{color:var(--gold);font-size:12px;font-weight:700;letter-spacing:.1em}h1{margin:.2em 0;font:700 clamp(32px,6vw,54px)/1.15 "Songti SC",serif}.lead,.safety{padding:14px 16px;border-left:4px solid #27805d;background:#eef7f1;line-height:1.75}.safety{border-color:#d59b32;background:#fff8df}section{margin-top:32px}h2{padding-bottom:8px;border-bottom:1px solid var(--line);font:700 25px/1.3 "Songti SC",serif}h3{margin-top:24px;font:700 20px/1.4 "Songti SC",serif}p,li{font:17px/1.8 "Songti SC","STSong",serif}.meta{display:flex;gap:8px;flex-wrap:wrap}.pill,.search{display:inline-block;padding:7px 11px;border:1px solid #b9cfc3;border-radius:20px;color:var(--green);text-decoration:none}.channel-figure{margin:28px auto;max-width:680px;text-align:center}.channel-figure img{display:block;width:auto;max-width:100%;max-height:900px;margin:auto;border:1px solid var(--line);background:#f7f4ea;object-fit:contain}.channel-figure figcaption{margin-top:8px;color:#625e55;font-size:12px;line-height:1.55}.channel-figure a{color:var(--green)}.points{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:8px;padding:0;list-style:none}.points li{padding:10px 12px;border:1px solid var(--line);border-radius:7px;background:#faf9f5}.google-ai-overview{padding:20px;border:1px solid #cad5e5;border-radius:10px;background:#f7faff}.google-ai-overview>h2{color:#315b8a}.ai-overview-note{padding:10px 12px;border-left:4px solid #d59b32;background:#fff8df;color:#594318;font:14px/1.6 Arial,"PingFang SC",sans-serif}.google-ai-overview a{color:#176b4b;overflow-wrap:anywhere}.google-ai-overview hr{border:0;border-top:1px solid var(--line)}.notation{border-bottom:1px dotted var(--green);background:#eef7f1}.interlinear-note ruby>rt{color:var(--green);font:12px/1.2 Arial,sans-serif}.footnote-ref{margin:0 2px;color:var(--green);font-weight:700}.comment-anchor{border-bottom:2px solid #d59b32}.comment-block{padding:10px 13px;border-left:4px solid #d59b32;background:#fff8df;color:#594318}.doubt{text-decoration:underline wavy #c0392b;text-decoration-thickness:1.5px}.reader-footnotes{padding:14px 18px;border:1px solid var(--line);background:#f8f7f3}.pager{display:flex;justify-content:space-between;gap:12px;margin-top:38px}.pager a{color:var(--green)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(275px,1fr));gap:12px}.card{padding:18px;border:1px solid var(--line);background:#fff}.card h2{margin:4px 0 8px;border:0;font-size:21px}.card p{margin:4px 0;color:#625e55;font-size:14px}.card a{color:var(--green);font-weight:700;text-decoration:none}@media(max-width:600px){.paper{padding:21px 17px}header span{display:none}}@media print{header,.toolbar{display:none!important}body{background:#fff}.paper{border:0;box-shadow:none}}
"""

TOOLBAR = '''<nav class="toolbar" aria-label="编辑与批注工具"><button type="button" data-command="undo">撤销</button><button type="button" data-command="redo">重做</button><button type="button" data-command="bold"><b>粗体</b></button><button type="button" data-command="italic"><i>斜体</i></button><button type="button" data-command="hiliteColor">标记</button><button type="button" data-command="removeFormat">清除格式</button><button type="button" class="annotation-tool" data-action="notation">注音/简注</button><button type="button" class="annotation-tool" data-action="interlinear">行间注</button><button type="button" class="annotation-tool" data-action="footnote">脚注</button><button type="button" class="annotation-tool" data-action="comment">按语</button><button type="button" class="annotation-tool" data-action="doubt">存疑</button></nav>'''


def page(item: tuple[str, ...], index: int) -> str:
    slug, name, code, group, route, function, points = item
    point_items = "".join(f"<li>{escape(point.strip())}</li>" for point in points.split("、"))
    search = "https://www.google.com/search?q=" + quote_plus(name)
    previous = CHANNELS[index - 1] if index else None
    following = CHANNELS[index + 1] if index + 1 < len(CHANNELS) else None
    prev_link = f'<a href="../{previous[0]}/editor.html?view=annotated">← {escape(previous[1])}</a>' if previous else "<span></span>"
    next_link = f'<a href="../{following[0]}/editor.html?view=annotated">{escape(following[1])} →</a>' if following else "<span></span>"
    source = COMMONS_SOURCES.get(slug)
    caption = (f'历史经脉图，Wellcome Collection；经 Wikimedia Commons 提供，<a href="{escape(source, quote=True)}" target="_blank" rel="noreferrer">CC BY 4.0 来源与完整署名</a>。' if source else "本地课程图像；原文件未附来源或许可信息，仅在此学习工作区使用。")
    figure = f'<figure class="channel-figure"><img src="../../assets/{escape(slug)}.jpg" alt="{escape(name)}循行与穴位示意图" loading="lazy" decoding="async"><figcaption>{caption} 图示属于传统经脉模型，不是现代解剖图。</figcaption></figure>'
    overview = f'''<section id="google-ai-overview-{escape(slug)}" class="google-ai-overview"><h2>Google AI Overview（用户整理）</h2><p class="ai-overview-note">以下内容由用户于 2026-10-03 从 Google AI Overview 整理粘贴，保留原链接与编号。它可能包含错误、来源质量差异或未经充分验证的医疗主张；仅供对照学习，不作为诊断、治疗或自我针灸建议。</p>{AI_OVERVIEWS[slug]}</section>'''
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(name)} · 经络教程</title><link rel="stylesheet" href="../../../../workspace_theme.css"><style>{STYLE}</style></head><body data-editor-key="jingluo-{escape(slug)}-v1" data-channel-name="{escape(name, quote=True)}"><header><a href="../../index.html">← 经络教程</a><strong>{index + 1:02d} / 20 · {escape(group)}</strong><span>{escape(code)}</span></header>{TOOLBAR}<main><article id="editor" class="paper" contenteditable="true"><p class="eyebrow">十二正经与奇经八脉</p><h1>{escape(name)}</h1><div class="meta"><span class="pill">国际/常用代码：{escape(code)}</span><span class="pill">{escape(group)}</span><a class="search" href="{escape(search, quote=True)}" target="_blank" rel="noreferrer">Google 搜索：{escape(name)}</a></div>{figure}<section><h2>循行概述</h2><p>{escape(route)}</p></section><section><h2>传统功能与联系</h2><p>{escape(function)}</p></section><section><h2>主要穴位（学习清单）</h2><ul class="points">{point_items}</ul><p><small>此清单收录常用或定位意义突出的穴位，并非该经全部穴位，也不是处方。穴名、代码及定位应以采用的国家标准或教材版本核对。</small></p></section>{overview}<section><h2>记忆任务</h2><ol><li>用一句话复述起点、主干方向和终点。</li><li>在人体轮廓上标出经脉所在的前、中、后或内、外侧。</li><li>从清单中先记原穴、络穴、郄穴、五输穴和常见交会穴，再补充其他穴位。</li></ol></section><p class="safety"><strong>学习与安全边界：</strong>经络、功能和主治均按传统理论表述，不等同于现代解剖结构或已证实机制。穴位列表用于识记，不提供自我针刺指导；针刺可能导致感染、出血、气胸或其他损伤，应由符合当地资质要求的专业人员实施。</p><nav class="pager" contenteditable="false">{prev_link}{next_link}</nav></article></main><script src="../../editor_tools.js"></script><script>window.ReadingWorkspace={{directoryHref:'../../../../index.html',bookDirectoryHref:'../../index.html'}};</script><script src="../../../../mobile_pwa.js"></script></body></html>'''


def index_page() -> str:
    cards = "".join(f'''<article class="card"><span class="eyebrow">{escape(group)} · {escape(code)}</span><h2>{escape(name)}</h2><p>{escape(route.split("；")[0])}</p><a href="chapters/{escape(slug)}/editor.html?view=annotated">开始学习 →</a></article>''' for slug, name, code, group, route, _function, _points in CHANNELS)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>十二正经与奇经八脉 · 经络教程</title><link rel="stylesheet" href="../../workspace_theme.css"><style>{STYLE}</style></head><body><header><a href="../index.html">← 中医基础理论</a><strong>经络专题教程</strong><a href="gallery.html">经络图总览</a><span>20 讲</span></header><main><section class="paper"><p class="eyebrow">JINGLUO TUTORIAL</p><h1>十二正经与奇经八脉</h1><p class="lead">按统一格式学习每条经脉：循行概述、传统功能与联系、主要穴位，以及可继续检索的名称链接。建议先学十二正经的交接循环，再学奇经八脉。</p><p class="safety"><strong>范围说明：</strong>“主要穴位”是常用与定位意义突出的学习清单，不声称是唯一标准。十二正经共包含数百个标准穴位；本教程重在建立结构，不替代完整腧穴学教材、定位训练或临床资质。</p><p><a class="search" href="gallery.html">在一页中查看全部 20 幅经络图 →</a></p><section><h2>十二正经</h2><div class="grid">{cards[:cards.find('<article class="card"><span class="eyebrow">奇经八脉')]}</div></section><section><h2>奇经八脉</h2><div class="grid">{cards[cards.find('<article class="card"><span class="eyebrow">奇经八脉'):]}</div></section><section><h2>术语与编码参考</h2><p><a class="search" href="https://www.who.int/publications/i/item/9789240042322" target="_blank" rel="noreferrer">WHO 中医药国际标准术语</a> <a class="search" href="https://www.who.int/publications/i/item/9290611057" target="_blank" rel="noreferrer">WHO 标准针灸命名（361 个经典穴）</a></p></section></section></main><script src="../../workspace_skin.js"></script><script src="../../mobile_pwa.js"></script></body></html>'''


def gallery_page() -> str:
    figures = "".join(
        f'''<figure class="gallery-card"><a href="chapters/{escape(slug)}/editor.html?view=annotated" aria-label="打开{escape(name)}学习页"><img src="assets/{escape(slug)}.jpg" alt="{escape(name)}循行与穴位示意图" loading="lazy" decoding="async"></a><figcaption><strong>{index:02d} · {escape(name)}</strong><span>{escape(group)} · {escape(code)}</span><small>点击图像打开原学习页</small></figcaption></figure>'''
        for index, (slug, name, code, group, _route, _function, _points)
        in enumerate(CHANNELS, 1)
    )
    style = '''*{box-sizing:border-box}:root{--ink:#25231f;--green:#176b4b;--gold:#9a692f;--line:#d8d2c6;--paper:#fff;--wash:#f3f1eb}body{margin:0;background:var(--wash);color:var(--ink);font-family:Arial,"PingFang SC",sans-serif}.topbar{position:sticky;top:0;z-index:5;display:flex;gap:16px;align-items:center;padding:12px max(18px,calc((100vw - 1420px)/2));border-bottom:1px solid var(--line);background:#fffdf8f2;backdrop-filter:blur(9px)}.topbar a{color:var(--green);text-decoration:none}.topbar strong{flex:1}.hero{width:min(1420px,calc(100% - 32px));margin:34px auto 22px}.eyebrow{margin:0;color:var(--gold);font-size:12px;font-weight:700;letter-spacing:.1em}h1{margin:5px 0 9px;font:700 clamp(30px,5vw,52px)/1.12 "Songti SC",serif}.hero p:last-child{max-width:820px;color:#625e55;font-size:16px;line-height:1.7}.gallery{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;width:min(1420px,calc(100% - 32px));margin:0 auto 80px}.gallery-card{margin:0;overflow:hidden;border:1px solid var(--line);border-radius:12px;background:var(--paper);box-shadow:0 2px 10px #322b2012}.gallery-card>a{display:block;padding:12px;background:#f8f5ed}.gallery-card>a:focus-visible{outline:3px solid #27805d;outline-offset:-3px}.gallery-card img{display:block;width:100%;height:auto;max-height:690px;margin:auto;object-fit:contain;transition:transform .18s ease}.gallery-card a:hover img{transform:scale(1.015)}figcaption{display:grid;gap:3px;padding:13px 15px 15px}figcaption strong{font:700 19px/1.35 "Songti SC",serif}figcaption span{color:var(--green);font-size:13px}figcaption small{color:#736d62}@media(max-width:980px){.gallery{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:600px){.topbar{padding:11px 14px}.topbar span{display:none}.hero,.gallery{width:min(100% - 20px,560px)}.hero{margin-top:24px}.gallery{grid-template-columns:1fr;gap:14px}.gallery-card>a{padding:8px}.gallery-card img{max-height:none}}@media print{.topbar{display:none}.gallery{grid-template-columns:repeat(3,1fr);gap:8px}.gallery-card{break-inside:avoid;box-shadow:none}.gallery-card>a{padding:3px}figcaption{padding:6px}}'''
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>经络图总览 · 十二正经与奇经八脉</title><link rel="stylesheet" href="../../workspace_theme.css"><style>{style}</style></head><body><header class="topbar"><a href="index.html">← 经络教程</a><strong>经络图总览</strong><span>20 幅</span></header><section class="hero"><p class="eyebrow">JINGLUO IMAGE GALLERY</p><h1>十二正经与奇经八脉图</h1><p>全部 20 幅图集中在本页。图像按比例缩小，并保持足够宽度以便辨认文字；点击任一图像可进入对应的完整学习页。</p></section><main class="gallery">{figures}</main><script src="../../workspace_skin.js"></script><script src="../../mobile_pwa.js"></script></body></html>'''


def build() -> None:
    for index, item in enumerate(CHANNELS):
        folder = BASE / "chapters" / item[0]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "editor.html").write_text(page(item, index), encoding="utf-8")
    (BASE / "index.html").write_text(index_page(), encoding="utf-8")
    (BASE / "gallery.html").write_text(gallery_page(), encoding="utf-8")
    manifest = {
        "schema_version": 1,
        "id": "jingluo_tutorial",
        "title": "十二正经与奇经八脉",
        "language": "zh-CN",
        "medical_use": "education_only",
        "components": {"image_gallery": {"path": "gallery.html"}},
        "assets": [{"path": f"assets/{item[0]}.jpg", "title": f"{item[1]}循行与穴位示意图"} for item in CHANNELS],
        "units": [{"path": f"chapters/{item[0]}/editor.html", "title": item[1]} for item in CHANNELS],
    }
    (BASE / "book_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(CHANNELS)} JingLuo lessons")


if __name__ == "__main__":
    build()
