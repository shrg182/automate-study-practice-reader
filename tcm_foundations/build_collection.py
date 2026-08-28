#!/usr/bin/env python3
"""Build an original Chinese medicine foundations textbook for Reader App."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path


BASE = Path(__file__).resolve().parent

SOURCES = [
    {"title": "中医基础理论（北京中医药大学）", "url": "https://www.icourse163.org/course/BUCM-1206410812", "type": "公开课程"},
    {"title": "中医基础理论（国家高等教育智慧教育平台）", "url": "https://higher.smartedu.cn/course/66cd0d78711dc30c3470e686", "type": "国家级课程"},
    {"title": "中医基础理论课程与十四周大纲", "url": "https://www.icourse163.org/course/detail.htm?cid=1002126013", "type": "公开课程大纲"},
    {"title": "WHO International Standard Terminologies on Traditional Medicine", "url": "https://www.who.int/publications/i/item/9789240042322", "type": "术语参考"},
    {"title": "Traditional Chinese Medicine: What You Need To Know", "url": "https://www.nccih.nih.gov/health/traditional-chinese-medicine-what-you-need-to-know", "type": "疗效与安全参考"},
    {"title": "Acupuncture: Effectiveness and Safety", "url": "https://www.nccih.nih.gov/health/acupuncture-effectiveness-and-safety", "type": "针灸安全参考"},
]

CHAPTERS = [
    {
        "slug": "01_introduction", "title": "导论：怎样学习中医基础理论", "unit": "绪论",
        "lead": "中医基础理论是一套历史形成的医学概念体系。本章先建立学习边界：理解其内部逻辑，同时把传统术语、现代生物医学事实与临床证据分开。",
        "sections": [
            ("一、课程研究什么", ["课程讨论中医学关于生命、健康、疾病及防治原则的基本认识。常见内容包括整体观念、辨证思维、阴阳五行、藏象、气血津液、经络、体质、病因、病机和治则。", "这些概念首先属于传统医学的理论语言。学习目标是准确理解术语如何相互关联，而不是把每个术语直接等同于某个现代解剖结构或实验指标。"]),
            ("二、两条主线", ["整体观念强调人体内部、人与环境以及身心活动之间的联系。辨证思维则关注特定时间、特定个体所呈现的一组症状和体征，并据此形成传统医学中的证候判断。", "“辨证”不同于现代医学的疾病诊断。二者可以描述同一位患者的不同层面，但不能彼此替代。"]),
            ("三、可靠的学习方法", ["先掌握概念定义，再梳理关系，最后用案例检验理解。遇到古代命题时，应追问它在原有语境中的含义、后世如何解释、今天有什么证据，而不是只背结论。", "本教材不提供自我诊断、处方或停药建议。出现持续或严重症状，应接受合格医疗专业人员的评估。"]),
        ],
        "terms": [("整体观念", "从相互联系的层面理解生命活动"), ("辨证", "依据四诊资料分析传统医学证候"), ("证候", "传统理论对某阶段病理状态的概括")],
        "questions": ["为什么不能把传统术语直接翻译成单一现代器官？", "辨证与疾病诊断有什么区别？", "学习古代医学命题时应提出哪三类问题？"],
    },
    {
        "slug": "02_qi_yinyang_wuxing", "title": "精气、阴阳与五行", "unit": "哲学基础",
        "lead": "精气、阴阳、五行构成中医理论常用的解释框架。重点不是把它们物质化，而是理解它们怎样描述生成、对立、平衡和变化。",
        "sections": [
            ("一、精气观", ["传统精气观用“气”的聚散和运动说明事物的生成变化。在中医学中，气既可作为高度概括的生命活动概念，也可在特定语境中指推动、温煦、防御、固摄或气化等功能。", "同一个“气”字在不同句子中的层级可能不同，阅读时必须结合限定词和上下文。"]),
            ("二、阴阳关系", ["阴阳用于概括相互关联又具有相反倾向的两个方面。教材通常从对立制约、互根互用、消长平衡和相互转化四方面说明其关系。", "阴阳是关系范畴，不是固定物质。寒热、动静、内外可以在特定比较中分属阴阳，但分类会随参照对象改变。"]),
            ("三、五行框架", ["木、火、土、金、水用于归纳五类性质及其关系。相生描述支持或促进的次序，相克描述制约的次序；乘、侮则用于说明制约关系出现异常。", "五行配属是一种传统分类模型，不等于化学元素，也不构成现代因果机制的证明。"]),
        ],
        "terms": [("气化", "传统理论中气的运动变化及其产生的功能过程"), ("互根互用", "相反两方面相互依存"), ("相乘", "制约太过"), ("相侮", "反向制约")],
        "questions": ["为什么阴阳分类必须说明参照关系？", "相生与相克为什么不简单等于好与坏？", "“气”在不同语境中可能有哪些层级？"],
    },
    {
        "slug": "03_zangxiang", "title": "藏象：五脏、六腑与奇恒之腑", "unit": "正常生命活动",
        "lead": "藏象学说以功能联系组织人体认识。传统“脏腑”包含解剖经验，但其概念范围通常大于同名现代器官。",
        "sections": [
            ("一、藏象的含义", ["“藏”指藏于体内的脏腑，“象”指其功能表现及外在征象。藏象理论通过症状、体征、情志、感觉器官和组织状态等联系，概括脏腑系统的功能。", "因此，中医“肝”“脾”“肾”等不应直接等同于现代医学的 liver、spleen、kidney。名称相同不代表概念边界相同。"]),
            ("二、五脏与六腑", ["五脏通常指心、肺、脾、肝、肾，侧重化生和贮藏精气；六腑指胆、胃、小肠、大肠、膀胱、三焦，侧重受盛、传化和排泄。", "这种“藏而不泻”“泻而不藏”的概括是传统功能分类，不是绝对的解剖学描述。"]),
            ("三、系统联系", ["传统理论把五脏与情志、五官、形体组织及季节等建立配属关系，用于解释整体表现。学习时应区分：经典配属、临床经验、后世发挥和经过现代研究检验的结论。", "对任何健康问题，都不能仅凭某一配属关系自行判断脏器疾病。现代器质性疾病需要相应的医学检查。"]),
        ],
        "terms": [("藏象", "由内在脏腑及其外在功能表现构成的传统理论"), ("三焦", "传统六腑之一，也用于划分上中下三部功能区域"), ("奇恒之腑", "形态似腑而功能近脏的一类传统归纳")],
        "questions": ["藏象中的“象”包括哪些信息？", "为什么中医“脾”不能直接等同于解剖学脾脏？", "五脏与六腑的传统分类依据是什么？"],
    },
    {
        "slug": "04_essence_qi_blood_fluids_spirit", "title": "精、气、血、津液与神", "unit": "生命物质与活动",
        "lead": "本章梳理五个彼此关联的核心概念，并特别标出传统功能描述与现代生理学术语之间的边界。",
        "sections": [
            ("一、精与气", ["“精”在传统理论中可指禀受于父母并与生长生殖相关的先天之精，也可指饮食化生并不断补充的后天之精。", "“气”侧重生命活动及其动力性表现。常见功能概括为推动、温煦、防御、固摄和气化；具体含义要看语境。"]),
            ("二、血与津液", ["传统“血”具有濡养和作为精神活动物质基础等含义，与现代血液概念有重叠但不完全相同。", "津液是机体正常水液的总称，常以较清稀者为津、较稠厚者为液。其生成、输布和排泄被置于多个脏腑系统的协同关系中。"]),
            ("三、神及相互关系", ["“神”可概括生命活动的总体表现，也可指意识、思维和情志活动。精、气、血、津液与神在传统理论中相互依存。", "这些关系是传统解释框架，不能代替神经系统、内分泌、循环或体液平衡的现代评估。"]),
        ],
        "terms": [("先天之精", "传统理论中禀受于父母的生命基础"), ("固摄", "维持体内物质不致异常流失的功能概括"), ("津液", "传统理论中正常水液的总称"), ("神", "生命状态及精神意识活动的概括")],
        "questions": ["传统“血”与现代血液概念有何关系？", "气的五种常见功能是什么？", "“神”有哪些主要含义？"],
    },
    {
        "slug": "05_meridians", "title": "经络", "unit": "联系与运行",
        "lead": "经络学说描述人体各部分之间的联系和气血运行路径，是针灸与传统辨证的重要理论基础。",
        "sections": [
            ("一、经络系统", ["经络通常分为经脉和络脉。十二经脉是主体，奇经八脉具有调节、联络等传统功能；此外还有经别、经筋、皮部及各级络脉。", "十二经脉通过一定的循行、交接和表里关系构成网络，并与脏腑和体表部位建立联系。"]),
            ("二、主要作用", ["传统教材通常把经络作用概括为沟通内外、运行气血、感应传导和调节功能。病理情况下，经络也用于说明症状沿一定部位出现或相互影响。", "经络不是已经被现代解剖学确认的独立管道。有关针刺效应的研究涉及神经、结缔组织及多种生理机制，但不能据此把所有经络命题视为已获证实。"]),
            ("三、学习循行的方法", ["先掌握十二经脉名称、阴阳属性、手足分组与表里配对，再学习起止、主要循行和交接规律。不要一开始机械背诵所有穴位。", "涉及针刺治疗时，应由受过训练且符合当地资质要求的专业人员操作。"]),
        ],
        "terms": [("十二经脉", "经络系统的十二条主要经脉"), ("奇经八脉", "具有统率、联络和调节作用的八条特殊经脉"), ("表里关系", "六对阴经阳经之间的传统配对关系")],
        "questions": ["经脉与络脉怎样区分？", "学习十二经脉循行的合理顺序是什么？", "为什么不能把经络简单称为已知解剖管道？"],
    },
    {
        "slug": "06_constitution", "title": "体质", "unit": "个体差异",
        "lead": "体质学说关注个体在形态、功能、心理反应和疾病倾向方面相对稳定而又可以变化的特征。",
        "sections": [
            ("一、形成因素", ["传统理论认为体质受先天禀赋、年龄、性别、饮食、劳逸、情志、环境和疾病经历等共同影响。体质具有相对稳定性，也可能随生活环境和健康状态改变。", "体质概念体现个体差异，但不能代替遗传学、营养学、心理学或具体疾病风险评估。"]),
            ("二、分类的用途与限制", ["不同学派和教材采用的分类并不完全一致。分类可帮助整理观察和提出调养思路，但类别边界并非天然固定。", "网络问卷只能作为学习工具。若结果导致严格忌口、大量服用补品或延误就医，就超出了合理用途。"]),
            ("三、动态理解", ["同一个人可以呈现多方面特征，并受到睡眠、压力、感染、药物和慢性疾病影响。应避免把体质标签变成不可改变的身份判断。", "安全的健康管理仍应优先依靠均衡饮食、适量活动、充足睡眠、疫苗接种和循证筛查等一般原则。"]),
        ],
        "terms": [("禀赋", "传统理论中与先天获得有关的个体基础"), ("体质", "相对稳定又可变化的个体身心特征概括"), ("调养", "根据生活状态进行的长期保养与调整")],
        "questions": ["体质为什么既稳定又可变？", "体质问卷不能承担哪些任务？", "哪些因素可能暂时改变一个人的表现？"],
    },
    {
        "slug": "07_causes", "title": "病因", "unit": "疾病认识",
        "lead": "中医病因学按观察到的致病特点分类，包括外感、内伤及病理产物等。传统分类与现代病原学不是同一套体系。",
        "sections": [
            ("一、外感病因", ["六淫指风、寒、暑、湿、燥、火六类外感致病因素，是对气候环境与症状特点的传统归纳。疫疠则用于描述具有较强传染性和流行性的致病因素。", "“风寒”等证候名不等于确认病毒或细菌类型。疑似传染病应依据现代公共卫生和临床检测处理。"]),
            ("二、内伤病因", ["七情指喜、怒、忧、思、悲、恐、惊。正常情绪不是疾病；传统理论关注强烈、持久或突然的情志变化与身心状态之间的影响。", "饮食失宜、劳逸失度也被列为常见因素。现代评估还需考虑营养、职业暴露、睡眠、物质使用和社会环境等具体信息。"]),
            ("三、病理产物及其他因素", ["痰饮、瘀血等既被视为病理结果，也可能在传统解释中成为进一步致病的因素。外伤、寄生虫、药物损伤等也属于病因讨论范围。", "病因判断不能只靠抽象类别，必须联系时间顺序、暴露史、检查结果及危险信号。"]),
        ],
        "terms": [("六淫", "风寒暑湿燥火六类外感致病因素"), ("疫疠", "传统医学对强烈传染性流行性病因的概括"), ("七情", "喜怒忧思悲恐惊"), ("痰饮", "水液代谢异常形成的传统病理概念")],
        "questions": ["为什么“风寒”不能确认感染的病原体？", "正常情绪与情志致病如何区分？", "痰饮和瘀血为什么既是结果又可成为因素？"],
    },
    {
        "slug": "08_onset", "title": "发病", "unit": "疾病认识",
        "lead": "发病理论讨论人体状态、致病因素和环境条件怎样共同促成疾病发生，并解释为什么相似暴露会产生不同结果。",
        "sections": [
            ("一、正邪关系", ["传统理论以“正气”概括机体维持正常功能和抗御疾病的能力，以“邪气”概括致病因素。发病被理解为双方相互作用的结果。", "这一模型强调宿主差异，但“正气”不是某个单一免疫指标，“邪气”也不等于一种病原体。"]),
            ("二、发病类型", ["教材常讨论感邪即发、徐发、伏而后发、继发、复发等类型，用以描述暴露与症状之间不同的时间关系。", "时间关系可以帮助形成假设，却不能单独证明因果。现代诊断还需要病史、体检、实验室或影像等证据。"]),
            ("三、风险与危险信号", ["个体易感性、暴露强度、持续时间和生活环境都会影响发病。传统“治未病”思想可与风险预防对话，但具体措施必须评估收益与危害。", "胸痛、呼吸困难、意识改变、严重出血、突然瘫痪等情况需要紧急医疗评估，不应等待辨证或自行调理。"]),
        ],
        "terms": [("正气", "维持正常功能与抗病能力的传统概括"), ("邪气", "各种致病因素的传统总称"), ("伏而后发", "致病因素进入后经过一段时间才出现表现")],
        "questions": ["正气为什么不能等同于单一免疫指标？", "时间先后为什么不足以证明病因？", "哪些表现要求优先寻求紧急医疗帮助？"],
    },
    {
        "slug": "09_pathogenesis", "title": "病机", "unit": "疾病认识",
        "lead": "病机是传统理论对疾病发生、发展和变化机制的概括。学习重点是掌握关系模型，而不是把术语孤立背诵。",
        "sections": [
            ("一、基本病机", ["常见框架包括邪正盛衰、阴阳失调、气血津液失常以及脏腑经络功能失调。它们可以从不同层次描述同一组临床表现。", "“虚”通常强调不足或功能低下倾向，“实”通常强调邪盛、壅滞或反应亢盛倾向；二者可能夹杂或转化。"]),
            ("二、气血津液失常", ["气的失常常归纳为气虚、气机失调、气陷、气逆、气闭和气脱；血的失常包括血虚、血瘀、血热和出血；津液异常可表现为不足或输布排泄障碍。", "这些术语属于证候机制，不是实验室诊断。贫血、血栓、脱水等现代医学概念必须依靠相应标准确认。"]),
            ("三、内生五邪与传变", ["内风、内寒、内湿、内燥、内火借用外感病因名称，概括由内部功能失调产生的类似表现。疾病还可按表里、上下、脏腑等关系发生传变。", "分析病机要有证据链：观察资料、证候判断和理论解释应分别记录，避免循环论证。"]),
        ],
        "terms": [("邪正盛衰", "致病因素与抗病能力消长的传统关系"), ("气机", "气的升降出入运动"), ("血瘀", "血行不畅或停滞的传统病机"), ("内生五邪", "由内部失调产生的风寒湿燥火样病机")],
        "questions": ["虚实为什么可能同时存在？", "传统“血瘀”与现代血栓有何区别？", "怎样避免用病机解释进行循环论证？"],
    },
    {
        "slug": "10_prevention_treatment", "title": "养生、治未病与防治原则", "unit": "防治原则",
        "lead": "本章讨论传统治疗原则，不提供具体处方。任何治疗选择都应考虑诊断可靠性、证据质量、药物相互作用和个体风险。",
        "sections": [
            ("一、预防与治未病", ["治未病通常包括未病先防、既病防变和病后防复。顺应环境、饮食有节、起居有常、劳逸适度和调节情志是常见概括。", "这些原则可与现代健康促进相互参照，但不能替代疫苗、筛查、感染控制或慢性病规范管理。"]),
            ("二、治则框架", ["传统治则包括治病求本、扶正祛邪、调整阴阳、调理气血津液及因时因地因人制宜。正治与反治、标本缓急等概念用于说明复杂情况下的决策次序。", "“因人制宜”不意味着可以忽略标准化安全要求。个体化治疗同样需要明确适应证、剂量、禁忌和监测。"]),
            ("三、安全使用中药与针灸", ["天然不等于安全。中药可能引起肝肾损伤、过敏、污染、掺假或药物相互作用；孕期、儿童、老年人及肝肾疾病患者尤其需要专业评估。", "针灸存在感染、出血和少见但严重的器官损伤风险。应选择合格专业人员，并把正在使用的所有药物和补充剂如实告知医疗团队。"]),
        ],
        "terms": [("治未病", "未病先防、既病防变与病后防复"), ("治病求本", "针对疾病主要机制处理的传统原则"), ("扶正祛邪", "支持抗病能力并去除致病因素"), ("三因制宜", "因时、因地、因人调整")],
        "questions": ["治未病包括哪三个层次？", "为什么天然药物仍可能有严重风险？", "个体化与标准化安全要求是什么关系？"],
    },
    {
        "slug": "11_review", "title": "综合复习：从概念网络到案例分析", "unit": "复习与方法",
        "lead": "最后一章把全书概念连成网络，并给出一种不会越过诊疗边界的学习型案例分析方法。",
        "sections": [
            ("一、概念网络", ["哲学基础提供关系语言；藏象、精气血津液神和经络描述正常功能联系；体质说明个体差异；病因、发病和病机解释疾病过程；防治原则组织传统决策。", "任何一个术语都应放回这个层级网络中理解。只凭一个症状直接跳到脏腑或病机结论，会丢失必要的信息。"]),
            ("二、学习型案例的五步法", ["第一步记录事实：症状、起始时间、变化和相关背景。第二步识别危险信号并判断是否需要就医。第三步列出传统理论中可能相关的概念。第四步说明支持和反对每种解释的资料。第五步标记未知信息与证据限制。", "这种方法用于训练思维，不生成个人诊断和治疗方案。真实医疗决策应由合格专业人员结合完整评估作出。"]),
            ("三、继续学习", ["完成本课程后，可以依次学习中医诊断学、中药学、方剂学及经典选读，同时补充人体解剖、生理、病理、药理和循证医学基础。", "最有价值的能力不是记住最多术语，而是知道某个说法属于哪套知识体系、证据来自哪里、结论能支持到什么程度。"]),
        ],
        "terms": [("四诊", "望闻问切四类传统诊察资料"), ("证据边界", "现有资料能够支持结论的范围"), ("危险信号", "提示需要及时或紧急医学评估的表现")],
        "questions": ["全书各部分怎样构成一个层级网络？", "学习型案例五步法是什么？", "为什么应同时学习现代基础医学和循证医学？"],
    },
]


def chapter_page(chapter: dict, number: int) -> str:
    sections = "".join(
        f'<section><h2>{escape(title)}</h2>{"".join(f"<p>{escape(p)}</p>" for p in paragraphs)}</section>'
        for title, paragraphs in chapter["sections"]
    )
    terms = "".join(f'<tr><th>{escape(term)}</th><td>{escape(note)}</td></tr>' for term, note in chapter["terms"])
    questions = "".join(f"<li>{escape(question)}</li>" for question in chapter["questions"])
    source_links = "".join(f'<a href="{escape(source["url"], quote=True)}" target="_blank" rel="noreferrer">{escape(source["title"])}</a>' for source in SOURCES)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(chapter['title'])} · 中医基础理论</title><link rel="stylesheet" href="../../../workspace_theme.css"><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f3f1eb;color:#25231f;font-family:Arial,"PingFang SC",sans-serif}}header{{position:sticky;top:0;z-index:5;display:flex;gap:14px;align-items:center;padding:11px 18px;border-bottom:1px solid #d7d1c4;background:#fffdf8ed;backdrop-filter:blur(9px)}}header a{{color:#176b4b;text-decoration:none}}header strong{{flex:1}}.toolbar{{display:none;gap:7px;flex-wrap:wrap;padding:8px 18px;border-bottom:1px solid #d7d1c4;background:#fff}}body.mobile-edit-mode>.toolbar{{display:flex!important;position:sticky;top:0;z-index:210}}.toolbar button{{padding:7px 10px;border:1px solid #cfc8ba;border-radius:5px;background:#fff}}main{{width:min(940px,calc(100% - 28px));margin:24px auto 90px}}article{{padding:clamp(22px,5vw,54px);border:1px solid #d8d2c6;background:#fff;box-shadow:0 2px 12px #322b2010}}.eyebrow{{margin:0;color:#8a5c2c;font-size:12px;font-weight:700;letter-spacing:.12em}}h1{{margin:.25em 0 .45em;font:700 clamp(31px,6vw,53px)/1.16 "Songti SC",serif}}.lead{{padding:14px 16px;border-left:4px solid #27805d;background:#eef7f1;font-size:17px;line-height:1.8}}section{{margin-top:34px}}h2{{padding-bottom:8px;border-bottom:1px solid #ddd7ca;font:700 25px/1.3 "Songti SC",serif}}p{{font:18px/1.9 "Songti SC","STSong",serif}}table{{width:100%;border-collapse:collapse}}th,td{{padding:10px;border:1px solid #ddd7ca;text-align:left}}th{{width:24%;background:#f6f3ec}}li{{margin:.65em 0;line-height:1.7}}.boundary{{padding:14px;border:1px solid #efcf90;background:#fff8df;line-height:1.7}}.sources{{display:flex;gap:7px;flex-wrap:wrap}}.sources a{{padding:6px 9px;border:1px solid #c9d8cf;border-radius:16px;color:#176b4b;text-decoration:none;font-size:12px}}@media(max-width:600px){{article{{padding:21px 17px}}th{{width:32%}}}}@media print{{header,.toolbar{{display:none!important}}body{{background:#fff}}article{{border:0;box-shadow:none}}}}
</style></head><body><header><a href="../../index.html">← 教材目录</a><strong>第 {number} 章 · {escape(chapter['unit'])}</strong><span>原创学习版</span></header><nav class="toolbar"><button data-command="undo">撤销</button><button data-command="redo">重做</button><button data-command="bold"><b>粗体</b></button><button data-command="italic"><i>斜体</i></button><button data-command="hiliteColor">标记</button><button data-command="removeFormat">清除格式</button></nav><main><article id="editor" contenteditable="true"><p class="eyebrow">中医基础理论 · 第 {number} 章</p><h1>{escape(chapter['title'])}</h1><p class="lead">{escape(chapter['lead'])}</p>{sections}<section><h2>核心术语</h2><table>{terms}</table></section><section><h2>复习问题</h2><ol>{questions}</ol></section><section contenteditable="false"><h2>学习边界</h2><p class="boundary">本章用于医学史与理论学习，不构成诊断或治疗建议。传统术语与现代医学概念除非明确说明，不应视为一一对应；健康问题请咨询合格医疗专业人员。</p><div class="sources">{source_links}</div></section></article></main><script>
const key='tcm-foundations-{escape(chapter['slug'])}-v1',editor=document.getElementById('editor'),saved=localStorage.getItem(key);if(saved)editor.innerHTML=saved;editor.addEventListener('input',()=>localStorage.setItem(key,editor.innerHTML));document.querySelector('.toolbar').onclick=e=>{{const command=e.target.closest('button')?.dataset.command;if(!command)return;document.execCommand(command,false,command==='hiliteColor'?'#fff2a8':null);editor.focus()}};
</script><script>window.ReadingWorkspace={{directoryHref:'../../../index.html',bookDirectoryHref:'../../index.html'}};</script><script src="../../../mobile_pwa.js"></script></body></html>'''


def index_page() -> str:
    cards = "".join(f'''<article><span>{number:02d}</span><div><small>{escape(chapter['unit'])}</small><h2>{escape(chapter['title'])}</h2><p>{escape(chapter['lead'])}</p></div><a href="chapters/{chapter['slug']}/editor.html?view=annotated">阅读</a></article>''' for number, chapter in enumerate(CHAPTERS, 1))
    sources = "".join(f'<li><a href="{escape(item["url"], quote=True)}" target="_blank" rel="noreferrer">{escape(item["title"])}</a><small>{escape(item["type"])}</small></li>' for item in SOURCES)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>《中医基础理论》原创学习教材</title><link rel="stylesheet" href="../workspace_theme.css"><style>*{{box-sizing:border-box}}body{{margin:0;background:#f3f1eb;color:#25231f;font-family:Arial,"PingFang SC",sans-serif}}header{{padding:34px max(20px,6vw);background:linear-gradient(135deg,#173e33,#79552c);color:#fff}}header a{{color:#d9f2e6}}h1{{margin:.2em 0;font:700 clamp(39px,7vw,70px)/1.05 "Songti SC",serif}}header p{{max-width:800px;line-height:1.75}}main{{width:min(1050px,calc(100% - 28px));margin:20px auto 90px}}.notice,.sources{{padding:17px;border:1px solid #dfc782;background:#fff8df;line-height:1.7}}.chapters{{display:grid;gap:8px;margin-top:16px}}article{{display:grid;grid-template-columns:42px minmax(0,1fr) auto;gap:13px;align-items:center;padding:15px;border:1px solid #d8d2c6;background:#fff}}article h2{{margin:3px 0;font:700 21px "Songti SC",serif}}article p{{margin:5px 0 0;color:#625e55;line-height:1.55}}article small{{color:#8a5c2c}}article>a{{padding:8px 12px;border:1px solid #b9cfc3;border-radius:18px;color:#176b4b;text-decoration:none;font-weight:700}}.sources{{margin-top:20px;background:#fff}}.sources li{{display:flex;justify-content:space-between;gap:12px;margin:8px 0}}.sources a{{color:#176b4b}}@media(max-width:620px){{article{{grid-template-columns:30px 1fr}}article>a{{grid-column:2;justify-self:start}}.sources li{{display:block}}}}</style></head><body><header><a href="../index.html#tcm_foundations">← Reader library</a><h1>《中医基础理论》</h1><p>原创学习教材 · 依据权威公开课程框架编写。强调概念网络、传统理论与现代医学边界、证据意识和安全学习。</p></header><main><p class="notice"><strong>用途说明：</strong>本教材用于理论学习，不提供个人诊断、处方或停药建议。严重或持续症状应由合格医疗专业人员评估。</p><section class="chapters">{cards}</section><section class="sources"><h2>框架与术语参考</h2><ul>{sources}</ul></section></main><script src="../workspace_skin.js"></script><script src="../mobile_pwa.js"></script></body></html>'''


def build() -> None:
    for number, chapter in enumerate(CHAPTERS, 1):
        folder = BASE / "chapters" / chapter["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "editor.html").write_text(chapter_page(chapter, number), encoding="utf-8")
    (BASE / "index.html").write_text(index_page(), encoding="utf-8")
    chapters = [{"number": number, "slug": chapter["slug"], "title": chapter["title"], "unit": chapter["unit"]} for number, chapter in enumerate(CHAPTERS, 1)]
    manifest = {"schema_version": 1, "id": "tcm_foundations", "title": "中医基础理论", "edition": "原创学习版 v1", "language": "zh-CN", "medical_use": "education_only", "chapters": chapters, "units": [{"path": f"chapters/{chapter['slug']}/editor.html", "title": chapter["title"]} for chapter in CHAPTERS], "sources": SOURCES}
    (BASE / "book_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(CHAPTERS)} Chinese medicine foundations chapters")


if __name__ == "__main__":
    build()
