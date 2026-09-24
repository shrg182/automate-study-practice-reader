#!/usr/bin/env python3
"""Build an evidence-based dementia prevention study collection."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
import json
from pathlib import Path
import sys


BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent / "python_tutorial"))
from build_course import reader  # noqa: E402


@dataclass(frozen=True)
class Chapter:
    slug: str
    title: str
    source_title: str
    source_url: str
    body: str


CHAPTERS = (
    Chapter(
        "01_evidence_and_claims",
        "证据边界：预防、延缓与“逆转”",
        "WHO: Risk reduction of cognitive decline and dementia, second edition",
        "https://www.who.int/publications/i/item/9789240123557",
        """# 证据边界：预防、延缓与“逆转”

## 学习目标

- 区分降低风险、延缓发病、改善可逆因素与逆转阿尔茨海默病。
- 理解群体风险估计不能直接预测个人结局。
- 用证据等级判断饮食、补充剂和综合干预主张。

## 核心认识

痴呆不是正常老化的必然结果，但年龄仍是最重要的已知风险因素。生活方式、心血管和代谢健康、感觉功能、社会环境及空气污染都可能改变风险。改变这些因素的合理目标，是改善整体健康并降低或延缓认知衰退风险，而不是保证某个人不会患病。

“风险降低”描述某种干预与较低发病概率之间的关系；“延缓”表示症状或诊断可能较晚出现；“改善”可能来自纠正抑郁、睡眠障碍、听力损失、药物副作用或营养缺乏等因素。它们都不等同于已经确诊的神经退行性疾病被治愈或逆转。

## 怎样阅读强主张

看到“个性化方案”“代谢修复”或“逆转”时，应追问：研究是否随机对照、样本是否足够、是否设有对照组、结局是否由盲法评估、改善是否持续、是否报告不良反应，以及结果能否在独立团队中重复。病例系列可以提出假设，却不能单独证明疗效。

## 实用结论

应优先处理有明确健康收益的事项：规律活动、不吸烟、避免有害饮酒、均衡饮食、维持社会与认知活动，并与临床人员管理血压、血糖、胆固醇、抑郁、听力及视力问题。若记忆变化影响日常生活，应尽早接受正式评估，而不是自行采用补充剂或极端饮食。

## 复习问题

1. “最多可归因于可改变因素”为什么不等于个人可以消除同样比例的风险？
2. 哪些可逆问题可能表现得像认知衰退？
3. 一项声称“逆转”的研究至少需要报告哪些信息？

[阅读 WHO 完整指南](https://www.who.int/publications/i/item/9789240123557)
""",
    ),
    Chapter(
        "02_life_course_risk_reduction",
        "全生命周期的十四项可改变风险因素",
        "The Lancet Commission: Dementia prevention, intervention, and care (2024)",
        "https://discovery.ucl.ac.uk/id/eprint/10196488/",
        """# 全生命周期的十四项可改变风险因素

## 框架

2024 年 Lancet 委员会把预防放在全生命周期中理解。风险因素彼此重叠，也受教育、收入、医疗可及性和环境影响。因此，清单不是个人责任表，而是个人、医疗系统与公共政策共同作用的框架。

## 十四项因素

- 教育机会不足
- 听力损失
- 高血压
- 吸烟
- 肥胖
- 抑郁
- 缺乏身体活动
- 糖尿病
- 过量饮酒
- 头部损伤
- 空气污染
- 社会隔离
- 未治疗的视力损失
- 较高的低密度脂蛋白胆固醇

## 从清单到行动

优先级应由个人情况决定。血压、糖尿病和胆固醇需要规范检测与治疗；听力或视力下降值得评估和矫正；运动计划应结合身体能力逐步增加；抑郁需要专业支持；戒烟和减少有害饮酒能带来超出脑健康之外的收益。社交和认知活动的重点是持续参与，而非追求某一种“脑力游戏”。

## 多领域干预

风险往往成组出现。例如，听力下降可能减少社交，抑郁可能降低活动，活动减少又影响代谢健康。因此，把运动、饮食、心血管监测、认知参与和社会支持组合起来，通常比只盯住一种营养素更符合现实。

## 复习问题

1. 哪三项因素最适合在中年阶段主动筛查？
2. 听力损失可能通过哪些直接或间接路径影响认知？
3. 为什么公共政策也是痴呆预防的一部分？

[阅读 Lancet 委员会报告](https://discovery.ucl.ac.uk/id/eprint/10196488/)
""",
    ),
    Chapter(
        "03_diet_and_supplements",
        "饮食、代谢与补充剂：我们真正知道什么",
        "US National Institute on Aging: Diet and prevention of Alzheimer's disease",
        "https://www.nia.nih.gov/health/alzheimers-and-dementia/what-do-we-know-about-diet-and-prevention-alzheimers-disease",
        """# 饮食、代谢与补充剂：我们真正知道什么

## 饮食模式比单一“神奇食物”更重要

地中海饮食和 MIND 饮食强调蔬菜、全谷、豆类、坚果、鱼类及不饱和脂肪，并限制高糖、高盐、油炸食品和过多红肉。观察性研究常发现较健康的饮食模式与较好的认知结局相关，但相关性可能同时受到教育、活动、收入和整体健康行为影响。

随机试验的结果更谨慎：健康饮食有充分的一般健康理由，但尚不能据此承诺预防或逆转阿尔茨海默病。饮食的现实价值还包括帮助控制血压、糖尿病、体重和心血管风险。

## 补充剂

没有维生素或膳食补充剂被可靠证明能在一般人群中预防阿尔茨海默病。缺乏维生素时应诊断并纠正，但“有缺乏时治疗”与“人人高剂量补充”是两回事。补充剂可能与处方药相互作用，高剂量也可能造成伤害。

## 生酮与极端饮食

有关生酮饮食的研究仍有限，部分研究规模小、时间短。老年人采用严格饮食可能面临营养不足、体重下降、便秘或药物调整问题。若考虑重大饮食变化，应与熟悉本人疾病和药物的专业人员讨论。

## 可执行原则

选择可以长期坚持的均衡饮食；把重点放在整体模式、食物质量与代谢疾病管理；不依据单一化验或商业方案自行大量补充；记录饮食变化、体重、症状和相关指标，并让医生或营养师帮助解释。

## 复习问题

1. 观察性研究与随机试验分别能回答什么问题？
2. 为什么纠正已诊断缺乏不等于推荐常规补充？
3. 饮食可能通过哪些间接路径影响脑健康？

[阅读 NIA 证据综述](https://www.nia.nih.gov/health/alzheimers-and-dementia/what-do-we-know-about-diet-and-prevention-alzheimers-disease)
""",
    ),
    Chapter(
        "04_practical_chinese_guidance",
        "中国实践指南：早识别、早就医与家庭支持",
        "国家卫生健康委：阿尔茨海默病预防与干预核心信息",
        "https://www.nhc.gov.cn/lljks/c100158/201909/c124c2c91fb74701b11d560aba0ad827.shtml",
        """# 中国实践指南：早识别、早就医与家庭支持

## 日常预防

保持规律作息、均衡饮食、适量运动、认知活动和社会交往，同时控制高血压、糖尿病、高脂血症等慢性病。预防不是某一种产品或一次检测，而是长期管理多个因素。

## 识别需要评估的变化

偶尔忘记名字而稍后想起，与反复遗忘近期事件、熟悉事务处理困难、时间地点混乱、判断力明显下降或性格行为改变并不相同。关键问题是变化是否持续、是否进展、是否影响日常功能。

## 就医评估

认知变化可能来自多种原因。规范评估通常结合病史、家属观察、认知与功能测试、体格检查、药物审查和必要的实验室或影像检查。及早评估有助于发现可治疗因素、明确支持需求并进行安全与照护规划。

## 家庭支持

与患者沟通时避免责备和反复考试式提问；使用稳定日程、清晰提示和安全环境；关注走失、跌倒、用药、驾驶、财务以及照护者负担。照护计划应尊重患者意愿，并在其仍能参与决定时尽早讨论未来安排。

## 学习用行动表

1. 记录变化开始的时间、频率和具体例子。
2. 列出全部处方药、非处方药和补充剂。
3. 记录听力、视力、睡眠、情绪及慢性病控制情况。
4. 由熟悉情况的家属陪同就医。
5. 若出现突然意识混乱、急性神经症状或安全风险，应及时寻求急诊帮助。

## 复习问题

1. 判断“正常健忘”和需要评估的变化时，日常功能为什么重要？
2. 就诊前应准备哪些资料？
3. 家庭环境可以怎样降低风险并保留自主性？

[阅读国家卫生健康委原文](https://www.nhc.gov.cn/lljks/c100158/201909/c124c2c91fb74701b11d560aba0ad827.shtml)
""",
    ),
)


def landing() -> str:
    cards = "".join(
        f'<article><b>{number:02d}</b><div><h2>{escape(chapter.title)}</h2>'
        f'<p>{escape(chapter.source_title)}</p></div>'
        f'<a href="chapters/{chapter.slug}/editor.html?view=annotated">打开</a></article>'
        for number, chapter in enumerate(CHAPTERS, 1)
    )
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>认知健康与痴呆风险降低</title><link rel="stylesheet" href="../workspace_theme.css"><style>*{{box-sizing:border-box}}body{{margin:0;background:#f3f5f2;color:#202124;font-family:Arial,"PingFang SC",sans-serif}}header{{padding:42px max(20px,7vw);background:linear-gradient(135deg,#174b47,#506b3c);color:#fff}}header a{{color:#d5f4ea}}h1{{margin:.25em 0;font:700 clamp(34px,6vw,62px)/1.1 "Songti SC",serif}}header p{{max-width:780px;line-height:1.75}}main{{width:min(960px,calc(100% - 28px));margin:24px auto 80px}}.notice{{padding:16px;border:1px solid #e0c86b;background:#fff8d8;line-height:1.7}}section{{display:grid;gap:10px;margin-top:18px}}article{{display:grid;grid-template-columns:42px minmax(0,1fr) auto;gap:14px;align-items:center;padding:18px;border:1px solid #d8ded8;background:#fff}}article>b{{color:#188038}}article h2{{margin:0;font:700 21px "Songti SC",serif}}article p{{margin:6px 0 0;color:#5f6368}}article>a{{padding:8px 13px;border-radius:18px;background:#e6f4ea;color:#137333;text-decoration:none;font-weight:700}}@media(max-width:620px){{article{{grid-template-columns:32px 1fr}}article>a{{grid-column:2;justify-self:start}}}}</style></head><body><header><a href="../index.html#dementia_prevention">← Reader library</a><h1>认知健康与痴呆风险降低</h1><p>以 WHO、Lancet 委员会、美国国家老龄研究所和中国国家卫生健康委资料为依据的原创学习指南。</p></header><main><p class="notice"><strong>医学边界：</strong>本材料用于学习，不用于诊断或替代个体化医疗。现有证据支持降低风险、延缓部分病例并处理可逆因素，不支持保证预防或逆转已确诊的阿尔茨海默病。</p><section>{cards}</section></main><script src="../workspace_skin.js"></script><script src="../mobile_pwa.js"></script></body></html>'''


def main() -> None:
    units = []
    for number, chapter in enumerate(CHAPTERS, 1):
        folder = BASE / "chapters" / chapter.slug
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "reading.md").write_text(chapter.body, encoding="utf-8")
        page = reader(
            chapter.body,
            chapter.title,
            chapter.source_url,
            f"dementia-prevention-{chapter.slug}-v1",
            f"dementia_prevention_{chapter.slug}",
            "../../../index.html",
            "../../../workspace_theme.css",
            "../../index.html",
        )
        page = page.replace(
            '<a href="https://',
            '<a class="source-reading-link" contenteditable="false" href="https://',
        )
        source_link_support = '''<style>
#editor .source-reading-link{display:inline-block;padding:8px 12px;border:1px solid #a8c7b4;border-radius:18px;background:#e6f4ea;color:#137333!important;cursor:pointer;text-decoration:none;font-weight:700}
#editor .source-reading-link:hover,#editor .source-reading-link:focus{background:#ceead6;outline:2px solid #79a889;outline-offset:2px}
</style><script>
document.getElementById('editor').addEventListener('click',event=>{
  const link=event.target.closest('.source-reading-link[href]');
  if(!link)return;
  event.preventDefault();
  event.stopPropagation();
  window.open(link.href,'_blank','noopener,noreferrer');
});
</script>'''
        page = page.replace("</body>", source_link_support + "</body>", 1)
        page = page.replace("../../../project_dictionary/", "../../../../project_dictionary/")
        (folder / "editor.html").write_text(page, encoding="utf-8")
        (folder / "source.json").write_text(json.dumps({
            "title": chapter.source_title,
            "source_url": chapter.source_url,
            "retrieved_at": "2026-09-24T00:00:00+08:00",
            "medical_use": "education_only",
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        units.append({"number": number, "title": chapter.title, "path": f"chapters/{chapter.slug}/editor.html", "source_url": chapter.source_url})
    (BASE / "book_manifest.json").write_text(json.dumps({
        "schema_version": 1,
        "id": "dementia_prevention",
        "title": "认知健康与痴呆风险降低",
        "edition": "循证学习版 2026",
        "language": "zh-CN",
        "medical_use": "education_only",
        "units": units,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (BASE / "index.html").write_text(landing(), encoding="utf-8")
    print(f"Built {len(CHAPTERS)} dementia-prevention chapters")


if __name__ == "__main__":
    main()
