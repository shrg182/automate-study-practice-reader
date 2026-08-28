#!/usr/bin/env python3
"""Build an original Chinese medicine foundations textbook for Reader App."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path


BASE = Path(__file__).resolve().parent
PDF_NAME = "中医基础理论.pdf"
PDF_SOURCE_URL = "https://cjrjy.sdmpu.edu.cn/_upload/article/files/b6/78/0c1514014d6886af2888bbaa55f0/2ad29a5d-4340-464a-9a1e-c4b08b95ab3f.pdf"

SOURCES = [
    {"title": "中医基础理论（北京中医药大学）", "url": "https://www.icourse163.org/course/BUCM-1206410812", "type": "公开课程"},
    {"title": "中医基础理论（国家高等教育智慧教育平台）", "url": "https://higher.smartedu.cn/course/66cd0d78711dc30c3470e686", "type": "国家级课程"},
    {"title": "中医基础理论课程与十四周大纲", "url": "https://www.icourse163.org/course/detail.htm?cid=1002126013", "type": "公开课程大纲"},
    {"title": "WHO International Standard Terminologies on Traditional Medicine", "url": "https://www.who.int/publications/i/item/9789240042322", "type": "术语参考"},
    {"title": "Traditional Chinese Medicine: What You Need To Know", "url": "https://www.nccih.nih.gov/health/traditional-chinese-medicine-what-you-need-to-know", "type": "疗效与安全参考"},
    {"title": "Acupuncture: Effectiveness and Safety", "url": "https://www.nccih.nih.gov/health/acupuncture-effectiveness-and-safety", "type": "针灸安全参考"},
    {"title": "上海中医药大学《中医基础理论》教学大纲", "url": "https://jwc.shutcm.edu.cn/_upload/article/files/0f/7f/b8921e0b4db4af1d5d52f2801232/c9328800-969d-42b5-aad5-d79a8b775a14.pdf", "type": "112学时课程大纲"},
    {"title": "精讲精学中医基础理论（广州中医药大学）", "url": "https://higher.smartedu.cn/course/64befd74d190d2a6beef0042", "type": "国家级公开课程"},
    {"title": "中医基础理论（北京中医药大学，国家平台）", "url": "https://higher.smartedu.cn/course/68d5aee1a9f4619f8f6b707e", "type": "国家级公开课程"},
]

EXPANSIONS = {
    "01_introduction": {
        "objectives": ["说明中医基础理论的知识层级与课程范围", "辨析整体观念、辨证、辨病和循证评价", "运用司外揣内、援物比类等方法分析概念", "识别学习资料的版权、证据和安全边界"],
        "sections": [
            ("四、中医理论体系的形成线索", ["先秦至两汉的哲学、天文历法和医疗经验为理论形成提供背景。《黄帝内经》《难经》《伤寒杂病论》《神农本草经》等经典逐步确立生命观、疾病观与诊疗框架。后世医家围绕脏腑、病因、温病、体质等不断补充和争论，因此“中医理论”并非一次完成、始终不变的单一体系。", "学习学术史时应区分成书年代、作者归属、后世注释和现代教材整理。古代权威性能够说明思想影响，却不能自动证明现代临床有效性。"]),
            ("五、主要思维方法", ["司外揣内是由可观察表现推测内部状态；援物比类是借助自然或社会事物的相似性组织认识；取象运数则通过象与数建立秩序。它们有助于理解传统模型的形成，也可能产生过度类比，因此需要用反例和独立证据检查。", "系统思维关注关系和变化，分析思维则拆分变量、检验机制。成熟学习不是二选一，而是知道何时使用哪种方法、每种方法能得出多强的结论。"]),
        ],
        "compare": [("传统理论陈述", "说明体系内部的概念与关系", "可用文献与理论一致性考察"), ("现代机制假说", "提出可检验的生物学解释", "需要实验和可重复证据"), ("临床疗效主张", "声称干预改善健康结局", "需要合适对照、风险评估与证据综合")],
        "case": "某文章把“整体观念”解释为任何中医疗法都能同时改善全身。请分别指出其中的理论陈述、疗效主张和缺失证据。",
    },
    "02_qi_yinyang_wuxing": {
        "objectives": ["解释精气、阴阳和五行的基本内涵", "分析阴阳四种关系与五行生克乘侮", "区分关系模型、分类模型与物质实体", "在具体语境中判断术语层级"],
        "sections": [
            ("四、阴阳偏胜、偏衰与互损", ["在传统病机语言中，阴阳偏胜强调一方相对亢盛，偏衰强调一方不足。由于双方互根，长期或严重不足还可能出现阴损及阳、阳损及阴的描述。分析时要先说明比较对象、部位和阶段。", "“阴虚”“阳虚”是证候概念，不能凭单一怕冷、口干或疲劳自行确定。相同表现可以来自多种疾病、药物或生活因素。"]),
            ("五、五行归类的操作规则", ["归类常依据性质、功能、方位、季节等相似性，再以生克关系解释系统协调。配属表是学习工具，不应把所有事物强行归入唯一类别。不同文献出现差异时，应记录版本和语境。", "五行推演若只用结果反证前提，容易形成循环解释。较好的做法是先写出预测，再寻找可能推翻它的观察。"]),
        ],
        "compare": [("阴阳", "描述成对方面的关系与变化", "不是两种固定物质"), ("五行", "五类性质及生克关系的分类模型", "不是现代化学元素"), ("精气", "生成变化与生命活动的传统概括", "不是可直接测量的单一能量")],
        "case": "同一杯温水相对于冰水可称为阳，相对于沸水又可称为阴。用此例说明阴阳属性为何具有相对性。",
    },
    "03_zangxiang": {
        "objectives": ["说明藏象学说的形成、特点与分类", "概述五脏六腑的主要传统功能", "分析脏腑之间的相互关系", "避免把传统脏腑直接等同现代器官"],
        "sections": [
            ("四、五脏功能纲要", ["心的传统功能围绕主血脉、藏神；肺围绕主气、司呼吸、宣发肃降和通调水道；脾围绕运化、升清、统血；肝围绕疏泄、藏血；肾围绕藏精、主水、纳气。每一项都应继续追问其定义、表现和与其他脏腑的联系。", "这些功能构成的是系统概念。例如“脾主运化”涉及饮食物转化和输布的传统解释，不等于现代脾脏承担消化吸收。"]),
            ("五、脏腑关系", ["脏与脏的关系常围绕气血、津液、精神活动及先后天之本展开；脏与腑通过表里配对及功能协作联系；腑与腑强调受纳、传化和排泄过程的衔接。", "关系分析应避免单向化。传统模型往往同时包含相互资生、相互制约和病理影响，需说明当前讨论的是正常生理还是疾病状态。"]),
        ],
        "compare": [("中医“心”", "血脉与神志等功能系统", "范围超过解剖心脏"), ("中医“脾”", "运化、升清、统血等功能系统", "不可等同现代脾脏"), ("中医“肾”", "藏精、生长生殖、水液与纳气等系统", "不可据此判断肾功能指标")],
        "case": "学习者看到注意力下降便断言“心脏有病，因为心藏神”。请分析概念跨越发生在哪里，并列出需要补充的现代医学信息。",
    },
    "04_essence_qi_blood_fluids_spirit": {
        "objectives": ["概述精气血津液神的来源、功能与运行", "解释气的分类和升降出入", "分析各概念之间的相互关系", "辨析传统术语与实验室指标"],
        "sections": [
            ("四、气的分类与运动", ["元气、宗气、营气、卫气从来源、分布和功能角度区分。元气与先天之精密切相关；宗气聚于胸中；营气行于脉中并与营养相关；卫气行于脉外并与防御、温煦相关。", "升、降、出、入概括气机运动。正常功能依赖方向协调，异常可用气滞、气逆、气陷等概念描述。分类之间存在层级关系，不应把每一种气想象成独立可见物质。"]),
            ("五、相互化生与约束", ["传统理论以精能化气、气能生血行血摄血、津血同源等命题连接各概念。神的活动又以精气血为基础，并反映整体生命状态。", "关系命题可用于建立概念图：箭头应标明是生成、推动、固摄、承载还是外在表现。标明关系类型比单纯画双向箭头更能检验理解。"]),
        ],
        "compare": [("气虚", "传统证候中的功能不足倾向", "不是氧气不足的同义词"), ("血虚", "传统濡养不足的证候概括", "不必然等于贫血"), ("津液不足", "传统水液亏少状态", "脱水需按现代标准评估")],
        "case": "某人把“血虚”直接翻译为缺铁性贫血。请说明两者可能重叠的表现，以及为何仍需血常规、铁代谢和病因评估。",
    },
    "05_meridians": {
        "objectives": ["列出经络系统主要组成", "掌握十二经脉命名、表里和交接规律", "概述奇经八脉及经络作用", "客观表述经络与针刺研究证据"],
        "sections": [
            ("四、十二经脉的组织法", ["命名由手足、阴阳和脏腑三部分组成。手三阴从胸走手，手三阳从手走头，足三阳从头走足，足三阴从足走腹胸；相互交接形成循环。先掌握这一框架，再添加具体循行与病候。", "表里配对为肺与大肠、脾与胃、心与小肠、肾与膀胱、心包与三焦、肝与胆。配对属于传统功能联系，不代表解剖结构直接相连。"]),
            ("五、奇经八脉与网络层次", ["督、任、冲、带、阴跷、阳跷、阴维、阳维合称奇经八脉。教材常以蓄溢十二经气血、联络纵横和调节特定功能概括其意义。", "经别加强表里经与深部的联系，经筋侧重筋肉关节，皮部反映经脉在体表的区域。层次化学习可避免把经络系统缩减成十二条线。"]),
        ],
        "compare": [("经脉", "系统中的主要纵向通路", "传统功能路径"), ("络脉", "由经脉分出的网络", "大小深浅层次多样"), ("神经/血管", "现代解剖结构", "不能与经络简单一一对应")],
        "case": "一项研究发现针刺某穴会改变脑成像信号。这个结果能支持什么？不能单独证明哪些更广泛的经络主张？",
    },
    "06_constitution": {
        "objectives": ["解释体质概念、形成因素和基本特点", "比较分类工具的用途与限制", "分析体质、证候和疾病的关系", "设计不造成标签化的健康记录"],
        "sections": [
            ("四、体质、证候与疾病", ["体质描述较长期的倾向，证候概括疾病某阶段的状态，疾病诊断则按特定标准识别病理实体。体质可能影响易感性和反应，但不能由体质直接推出某种疾病。", "同一疾病可见不同证候，同一证候也可出现于不同疾病；体质又可能与当前证候不完全一致。这三层需要分别记录。"]),
            ("五、观察与再评估", ["较好的体质记录包括评估日期、近期疾病、睡眠、饮食、药物、压力和环境变化，并允许多种特征共存。经过一段时间后重新评估，能区分暂时状态与相对稳定倾向。", "分类工具应说明来源、适用人群和测量误差。未经过验证的网络测试不宜用于决定治疗或排除疾病。"]),
        ],
        "compare": [("体质", "相对稳定的个体倾向", "可随年龄环境改变"), ("证候", "疾病过程中阶段性病理概括", "动态变化较明显"), ("疾病", "按诊断标准识别的健康问题", "需相应临床证据")],
        "case": "某问卷把学习者归为“湿热体质”，于是其停止多种食物。请列出应核对的测量、营养和健康风险问题。",
    },
    "07_causes": {
        "objectives": ["分类外感、内伤和其他病因", "概括六淫各自的传统致病特点", "说明七情、饮食和劳逸的作用边界", "建立病因假说与证据链"],
        "sections": [
            ("四、六淫特点的比较", ["风常概括善动、变化和游走；寒与收引凝滞相关；湿与重浊黏滞相关；燥与津液受损相关；火热与炎上、耗气伤津相关；暑具有明显季节性并常夹湿。", "这些是症候模式的传统归纳，不是病原鉴定。实际临床还要考虑感染、过敏、毒物、环境温度及基础疾病。"]),
            ("五、因果推理", ["判断可能病因要记录暴露是否先于结果、关联是否稳定、是否存在替代解释、停止或再次暴露后如何变化，以及是否有独立检测支持。", "“情绪之后出现不适”并不自动说明七情是唯一病因。情绪、睡眠、药物、内分泌、感染和社会处境可能共同作用。"]),
        ],
        "compare": [("六气", "正常自然气候变化", "不必致病"), ("六淫", "异常或超过适应能力的外感因素", "传统病因分类"), ("病原体", "可识别的病毒细菌等", "现代病原学概念")],
        "case": "多人在同一聚会后发热咳嗽。比较用“风热”描述症候与用实验室检测识别病原体所回答的不同问题。",
    },
    "08_onset": {
        "objectives": ["说明发病的正邪关系", "比较主要发病类型", "分析体质、环境和暴露的共同作用", "优先识别需要现代急诊评估的危险信号"],
        "sections": [
            ("四、发病条件的多层模型", ["可把发病条件分为个体基础、具体暴露、时间过程和社会环境四层。传统正邪关系主要概括前两层互动，现代公共卫生还会系统考察住房、职业、资源和传播网络。", "多层模型有助于避免责备患者。患病不能简单归因于“正气不足”或意志薄弱。"]),
            ("五、复发与继发", ["复发指原有疾病在一定条件下再次出现，诱因可包括劳累、饮食、情志、治疗不彻底等传统因素。继发则强调在原有疾病基础上产生新的问题。", "现代随访应同时确认是否真为同一疾病、是否耐药或出现并发症、治疗依从性如何。传统分类可以整理现象，但不能替代这些判断。"]),
        ],
        "compare": [("即发", "暴露后较快出现", "时间短不等于因果已证实"), ("徐发", "缓慢形成", "常需长期资料"), ("伏而后发", "潜伏后出现", "需与现代潜伏期等概念区分")],
        "case": "患者突然出现单侧无力和言语不清。说明为何此时首先处理危险信号，而不是花时间完成传统证候分类。",
    },
    "09_pathogenesis": {
        "objectives": ["构建基本病机的层级框架", "比较虚实、寒热和升降出入异常", "解释气血津液与脏腑病机的联系", "用可反驳的证据链分析病机"],
        "sections": [
            ("四、从现象到病机的层级", ["第一层是可观察资料，第二层是证候归纳，第三层是气血津液或阴阳层面的机制解释，第四层才可能进一步联系脏腑经络。跳过中间层会使结论缺少依据。", "同一资料可能支持多个病机假说。应列出每个假说预期出现却尚未观察到的信息，并通过继续询问或检查区分。"]),
            ("五、病机转化", ["疾病可在虚实、寒热、表里等方面发生转化，也可出现虚实夹杂、寒热错杂。转化强调时间轴，因此一次静态观察不足以代表全过程。", "记录“何时出现、何时改变、什么事件在前”比堆叠术语更重要。动态资料也能减少事后把任何变化都解释成理论正确的倾向。"]),
        ],
        "compare": [("观察", "患者报告或检查所得资料", "应尽量具体记录"), ("证候", "对资料模式的传统归纳", "可能有多个候选"), ("病机", "解释证候形成变化的理论", "需避免循环论证")],
        "case": "“因为有血瘀，所以出现疼痛；因为疼痛，所以证明血瘀。”指出循环论证，并提出可增加区分度的信息。",
    },
    "10_prevention_treatment": {
        "objectives": ["解释治未病、治病求本和标本缓急", "比较扶正祛邪、正治反治和三因制宜", "把传统原则置于风险收益框架", "识别中药针灸的关键安全问题"],
        "sections": [
            ("四、标本与缓急", ["“本”常指主要或较深层机制，“标”常指继发或表面表现，但划分会随讨论层次而变。急则治标强调先处理危急表现，缓则治本强调条件允许时针对主要机制。", "现代急救中的气道、呼吸、循环优先原则可以帮助理解“急则治其标”的决策逻辑，但两者属于不同知识体系，不能借类比替代临床规范。"]),
            ("五、风险收益与共同决策", ["选择干预应明确目标、已知获益、证据不确定性、常见和严重风险、替代方案及不治疗的后果。患者偏好很重要，但知情选择需要准确资料。", "使用中药或针灸时，应核对产品来源、成分、剂量、疗程、资质、无菌操作、妊娠及肝肾功能，并监测不良反应。不要擅自停用已经处方的有效治疗。"]),
        ],
        "compare": [("正治", "采用与证候性质相反的治法", "常规逆向处理"), ("反治", "表面顺从假象、实质针对本质", "须建立在准确判断上"), ("三因制宜", "结合时间地点个体", "不豁免安全标准")],
        "case": "患者准备同时使用多种中药、抗凝药和针灸。列出开始前必须与医生和合格从业者共同核对的事项。",
    },
    "11_review": {
        "objectives": ["整合全书概念层级", "执行学习型案例五步法", "区分描述、解释、预测与治疗主张", "设计后续中医与现代医学并行学习路径"],
        "sections": [
            ("四、四类命题", ["描述命题回答看到了什么；分类命题回答归入什么模式；解释命题回答为什么发生；干预命题回答做什么会改善结果。每向后一层，都需要更多证据。", "传统文献可以有力支持某概念在历史上如何定义，却不能仅凭年代久远支持现代疗效。现代实验可能支持某个局部机制，也不能自动验证整套理论。"]),
            ("五、自我测评与学习档案", ["每章完成后可用四栏记录：我能准确复述什么、我能建立哪些关系、我仍混淆什么、哪些说法需要查证。复习时优先解决关系和边界，而不是继续增加孤立术语。", "学习档案应保存资料来源、访问日期和自己的修改。Reader 的标记与札记适合记录推理过程，但不应保存他人可识别的敏感医疗信息。"]),
        ],
        "compare": [("课程掌握", "能定义、比较、应用并说明边界", "不只背诵"), ("临床能力", "需诊断训练、监督实践与资质", "本教材不能授予"), ("研究判断", "评估设计、偏倚与证据综合", "需循证方法训练")],
        "case": "选取一个常见健康说法，分别写出它的传统理论依据、现代机制证据、临床疗效证据和安全信息；若某栏为空，要明确标注未知。",
    },
}

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
    expansion = EXPANSIONS[chapter["slug"]]
    objectives = "".join(f"<li>{escape(item)}</li>" for item in expansion["objectives"])
    sections = "".join(
        f'<section><h2>{escape(title)}</h2>{"".join(f"<p>{escape(p)}</p>" for p in paragraphs)}</section>'
        for title, paragraphs in chapter["sections"] + expansion["sections"]
    )
    terms = "".join(f'<tr><th>{escape(term)}</th><td>{escape(note)}</td></tr>' for term, note in chapter["terms"])
    comparison = "".join(f'<tr><th>{escape(item)}</th><td>{escape(meaning)}</td><td>{escape(boundary)}</td></tr>' for item, meaning, boundary in expansion["compare"])
    questions = "".join(f"<li>{escape(question)}</li>" for question in chapter["questions"])
    source_links = "".join(f'<a href="{escape(source["url"], quote=True)}" target="_blank" rel="noreferrer">{escape(source["title"])}</a>' for source in SOURCES)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(chapter['title'])} · 中医基础理论</title><link rel="stylesheet" href="../../../workspace_theme.css"><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f3f1eb;color:#25231f;font-family:Arial,"PingFang SC",sans-serif}}header{{position:sticky;top:0;z-index:5;display:flex;gap:14px;align-items:center;padding:11px 18px;border-bottom:1px solid #d7d1c4;background:#fffdf8ed;backdrop-filter:blur(9px)}}header a{{color:#176b4b;text-decoration:none}}header strong{{flex:1}}.toolbar{{display:none;gap:7px;flex-wrap:wrap;padding:8px 18px;border-bottom:1px solid #d7d1c4;background:#fff}}body.mobile-edit-mode>.toolbar{{display:flex!important;position:sticky;top:0;z-index:210}}.toolbar button{{padding:7px 10px;border:1px solid #cfc8ba;border-radius:5px;background:#fff}}.toolbar .annotation-tool{{border-color:#9fc7b4;background:#eef7f1;color:#176b4b}}main{{width:min(940px,calc(100% - 28px));margin:24px auto 90px}}article{{padding:clamp(22px,5vw,54px);border:1px solid #d8d2c6;background:#fff;box-shadow:0 2px 12px #322b2010}}.eyebrow{{margin:0;color:#8a5c2c;font-size:12px;font-weight:700;letter-spacing:.12em}}h1{{margin:.25em 0 .45em;font:700 clamp(31px,6vw,53px)/1.16 "Songti SC",serif}}.lead{{padding:14px 16px;border-left:4px solid #27805d;background:#eef7f1;font-size:17px;line-height:1.8}}.objectives,.case{{padding:16px 20px;border:1px solid #c9d8cf;background:#f2f8f4}}.objectives h2,.case h2{{margin-top:0}}section{{margin-top:34px}}h2{{padding-bottom:8px;border-bottom:1px solid #ddd7ca;font:700 25px/1.3 "Songti SC",serif}}p{{font:18px/1.9 "Songti SC","STSong",serif}}table{{width:100%;border-collapse:collapse}}th,td{{padding:10px;border:1px solid #ddd7ca;text-align:left;vertical-align:top}}th{{width:24%;background:#f6f3ec}}.comparison th{{width:auto}}li{{margin:.65em 0;line-height:1.7}}.notation{{border-bottom:1px dotted #176b4b;background:#eef7f1}}.interlinear-note ruby>rt{{color:#176b4b;font:12px/1.2 Arial,sans-serif}}.footnote-ref{{margin:0 2px;color:#176b4b;font-weight:700}}.comment-anchor{{border-bottom:2px solid #d59b32}}.comment-block{{padding:10px 13px;border-left:4px solid #d59b32;background:#fff8df;color:#594318}}.doubt{{text-decoration:underline wavy #c0392b;text-decoration-thickness:1.5px}}.reader-footnotes{{padding:14px 18px;border:1px solid #d8d2c6;background:#f8f7f3}}.reader-footnotes li{{padding-left:5px}}.boundary{{padding:14px;border:1px solid #efcf90;background:#fff8df;line-height:1.7}}.sources{{display:flex;gap:7px;flex-wrap:wrap}}.sources a{{padding:6px 9px;border:1px solid #c9d8cf;border-radius:16px;color:#176b4b;text-decoration:none;font-size:12px}}@media(max-width:600px){{article{{padding:21px 17px}}th{{width:32%}}.comparison{{font-size:13px}}}}@media print{{header,.toolbar{{display:none!important}}body{{background:#fff}}article{{border:0;box-shadow:none}}}}
</style></head><body><header><a href="../../index.html">← 教材目录</a><strong>第 {number} 章 · {escape(chapter['unit'])}</strong><span>原创学习版 · 第2版</span></header><nav class="toolbar"><button data-command="undo">撤销</button><button data-command="redo">重做</button><button data-command="bold"><b>粗体</b></button><button data-command="italic"><i>斜体</i></button><button data-command="hiliteColor">标记</button><button data-command="removeFormat">清除格式</button><button class="annotation-tool" data-action="notation">注音/简注</button><button class="annotation-tool" data-action="interlinear">行间注</button><button class="annotation-tool" data-action="footnote">脚注</button><button class="annotation-tool" data-action="comment">按语</button><button class="annotation-tool" data-action="doubt">存疑</button></nav><main><article id="editor" contenteditable="true"><p class="eyebrow">中医基础理论 · 第 {number} 章</p><h1>{escape(chapter['title'])}</h1><p class="lead">{escape(chapter['lead'])}</p><section class="objectives"><h2>学习目标</h2><ul>{objectives}</ul></section>{sections}<section><h2>核心术语</h2><table>{terms}</table></section><section><h2>概念辨析</h2><table class="comparison"><thead><tr><th>概念</th><th>本章含义</th><th>边界提醒</th></tr></thead><tbody>{comparison}</tbody></table></section><section class="case"><h2>思考练习</h2><p>{escape(expansion['case'])}</p></section><section><h2>复习问题</h2><ol>{questions}</ol></section><section contenteditable="false"><h2>学习边界</h2><p class="boundary">本章用于医学史与理论学习，不构成诊断或治疗建议。传统术语与现代医学概念除非明确说明，不应视为一一对应；健康问题请咨询合格医疗专业人员。</p><div class="sources">{source_links}</div></section></article></main><script>
const key='tcm-foundations-{escape(chapter['slug'])}-v2',editor=document.getElementById('editor'),saved=localStorage.getItem(key);if(saved)editor.innerHTML=saved;function persist(){{localStorage.setItem(key,editor.innerHTML)}}editor.addEventListener('input',persist);
function selectedRange(requireText=true){{const selection=getSelection();if(!selection?.rangeCount)return null;const range=selection.getRangeAt(0).cloneRange(),container=range.commonAncestorContainer.nodeType===1?range.commonAncestorContainer:range.commonAncestorContainer.parentElement;if(!editor.contains(container)||(requireText&&!range.toString().trim()))return null;return range}}
function wrapRange(range,node){{try{{range.surroundContents(node)}}catch{{node.append(range.extractContents());range.insertNode(node)}}persist()}}
function addNotation(){{const range=selectedRange();if(!range)return alert('请先选择需要注音或简注的文字。');const text=range.toString(),reading=prompt(`“${{text}}”的拼音或读音（可留空）：`,'');if(reading===null)return;const note=prompt('简注（可留空）：','');if(note===null)return;const span=document.createElement('span'),ruby=document.createElement('ruby'),rt=document.createElement('rt');span.className='notation';span.dataset.term=text;span.dataset.note=note.trim();span.title=note.trim();ruby.textContent=text;rt.textContent=reading.trim();ruby.append(rt);span.append(ruby);range.deleteContents();range.insertNode(span);persist()}}
function addInterlinear(){{const range=selectedRange();if(!range)return alert('请先选择需要行间注的文字。');const note=prompt('行间注（显示在原文上方）：','');if(!note?.trim())return;const ruby=document.createElement('ruby'),rt=document.createElement('rt');ruby.className='interlinear-note';ruby.append(range.extractContents());rt.textContent=note.trim();ruby.append(rt);range.insertNode(ruby);persist()}}
function footnoteList(){{let section=editor.querySelector('.reader-footnotes');if(!section){{section=document.createElement('section');section.className='reader-footnotes';section.innerHTML='<h2>脚注</h2><ol></ol>';editor.append(section)}}return section.querySelector('ol')}}
function addFootnote(){{const range=selectedRange(false);if(!range)return alert('请把光标放在正文中，或选择需要脚注的文字。');const note=prompt('脚注内容：','');if(!note?.trim())return;const list=footnoteList(),number=list.children.length+1,item=document.createElement('li'),ref=document.createElement('sup');item.textContent=note.trim();ref.className='footnote-ref';ref.textContent=`〔${{number}}〕`;ref.title=note.trim();if(!range.collapsed){{const anchor=document.createElement('span');anchor.className='comment-anchor';anchor.append(range.extractContents());anchor.append(ref);range.insertNode(anchor)}}else range.insertNode(ref);list.append(item);persist()}}
function addComment(){{const range=selectedRange(false);if(!range)return alert('请把光标放在正文中。');const note=prompt('按语或评论：','');if(!note?.trim())return;if(!range.collapsed){{const anchor=document.createElement('span');anchor.className='comment-anchor';anchor.title=note.trim();wrapRange(range,anchor)}}const block=document.createElement('p');block.className='comment-block';block.textContent=note.trim();const start=range.startContainer.nodeType===1?range.startContainer:range.startContainer.parentElement,paragraph=start?.closest?.('p');(paragraph||editor.lastElementChild).after(block);persist()}}
function addDoubt(){{const range=selectedRange();if(!range)return alert('请先选择需要标记存疑的文字。');const note=prompt('存疑原因（可留空）：','');if(note===null)return;const span=document.createElement('span');span.className='doubt';span.dataset.issue=note.trim();span.title=note.trim()||'存疑';wrapRange(range,span)}}
document.querySelector('.toolbar').onclick=e=>{{const button=e.target.closest('button');if(!button)return;const command=button.dataset.command,action=button.dataset.action;if(command){{document.execCommand(command,false,command==='hiliteColor'?'#fff2a8':null);editor.focus();persist()}}if(action==='notation')addNotation();if(action==='interlinear')addInterlinear();if(action==='footnote')addFootnote();if(action==='comment')addComment();if(action==='doubt')addDoubt()}};
</script><script>window.ReadingWorkspace={{directoryHref:'../../../index.html',bookDirectoryHref:'../../index.html'}};</script><script src="../../../mobile_pwa.js"></script></body></html>'''


def source_reader_page() -> str:
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>《中医基础理论》原书 PDF 工作台</title><style>
*{{box-sizing:border-box}}:root{{--line:#d8d2c6;--green:#176b4b;--paper:#fff;--muted:#625e55}}body{{margin:0;background:#ebe8e0;color:#25231f;font-family:Arial,"PingFang SC",sans-serif;overflow:hidden}}header{{height:56px;display:flex;gap:12px;align-items:center;padding:8px 14px;border-bottom:1px solid var(--line);background:#fff}}header a{{color:var(--green);text-decoration:none}}header strong{{flex:1}}header input{{width:78px;padding:7px;border:1px solid var(--line);border-radius:5px}}button,.button{{padding:7px 10px;border:1px solid var(--line);border-radius:6px;background:#fff;color:inherit;cursor:pointer;text-decoration:none}}button.primary{{border-color:var(--green);background:var(--green);color:#fff}}main{{height:calc(100vh - 56px);display:grid;grid-template-columns:minmax(420px,1fr) minmax(330px,420px)}}.pdf-pane{{min-width:0;background:#525659}}iframe{{width:100%;height:100%;border:0}}aside{{display:flex;min-width:0;flex-direction:column;border-left:1px solid var(--line);background:#f7f5ef}}.aside-head{{padding:13px;border-bottom:1px solid var(--line);background:#fff}}.aside-head h1{{margin:0;font-size:18px}}.aside-head p{{margin:5px 0 0;color:var(--muted);font-size:12px}}.composer{{display:grid;grid-template-columns:90px 1fr;gap:7px;padding:10px;border-bottom:1px solid var(--line)}}select,textarea{{width:100%;padding:8px;border:1px solid var(--line);border-radius:5px;background:#fff;font:inherit}}textarea{{grid-column:1/-1;min-height:88px;resize:vertical}}.composer .actions{{grid-column:1/-1;display:flex;gap:7px;align-items:center}}.composer label{{padding:7px 10px;border:1px solid var(--line);border-radius:6px;background:#fff;cursor:pointer}}.composer input[type=file]{{display:none}}#notes{{flex:1;overflow:auto;padding:10px}}.note{{margin-bottom:9px;padding:11px;border:1px solid var(--line);border-radius:7px;background:#fff}}.note header{{height:auto;padding:0 0 7px;border:0;background:transparent}}.note header b{{color:var(--green)}}.note header time{{margin-left:auto;color:var(--muted);font-size:10px}}.note p{{margin:4px 0;white-space:pre-wrap;line-height:1.55}}.note img{{max-width:100%;max-height:260px;margin-top:7px;border:1px solid var(--line)}}.note button{{padding:3px 7px;color:#a22;font-size:11px}}.empty{{padding:30px 12px;text-align:center;color:var(--muted)}}@media(max-width:850px){{body{{overflow:auto}}header{{height:auto;flex-wrap:wrap}}main{{height:auto;display:flex;flex-direction:column}}.pdf-pane{{height:65vh}}aside{{min-height:65vh;border-left:0;border-top:1px solid var(--line)}}}}@media print{{header,.composer{{display:none}}main{{display:block}}.pdf-pane{{display:none}}aside{{border:0}}}}
</style><style>
.pane-balance{{position:relative}}.pane-balance-popover{{position:absolute;z-index:30;top:calc(100% + 7px);right:0;display:none;width:min(350px,calc(100vw - 24px));padding:12px;border:1px solid #c9d2df;border-radius:10px;background:#fff;box-shadow:0 10px 30px #0003}}.pane-balance.open .pane-balance-popover{{display:grid;gap:11px}}.pane-presets{{display:grid;grid-template-columns:repeat(5,1fr);gap:4px}}.pane-presets button{{min-width:0;padding:6px 3px;font-size:11px}}.pane-presets button.active{{background:#e6f4ea;color:#137333;font-weight:700}}.pane-slider{{display:grid;grid-template-columns:auto 1fr auto;gap:8px;align-items:center;color:var(--muted);font-size:12px}}.pane-slider input{{width:100%;min-width:90px}}.pane-output{{grid-column:1/-1;color:#25231f;font-weight:700}}main{{grid-template-columns:minmax(0,var(--pdf-share,75fr)) minmax(0,var(--notes-share,25fr))}}main.pdf-only,main.notes-only{{grid-template-columns:1fr}}main.pdf-only aside,main.notes-only .pdf-pane{{display:none}}@media(max-width:850px){{main:not(.pdf-only):not(.notes-only){{display:flex}}.pane-balance-popover{{position:fixed;top:70px;right:12px}}}}
</style></head><body><header><a href="index.html">← 教材目录</a><strong>原书 PDF · 629 页</strong><label>页码 <input id="page" type="number" min="1" max="629" value="1"></label><button id="jump">跳转</button><a class="button" href="{PDF_NAME}" target="_blank">单独打开 PDF</a><a class="button" href="{PDF_SOURCE_URL}" target="_blank" rel="noreferrer">大学来源页</a></header><main><section class="pdf-pane"><iframe id="pdf" title="中医基础理论原书 PDF" src="{PDF_NAME}#page=1&view=FitH"></iframe></section><aside><div class="aside-head"><h1>页边札记</h1><p>按 PDF 页码保存笔记、批注、存疑和图片；资料只保存在当前浏览器。</p></div><div class="composer"><select id="kind"><option>笔记</option><option>批注</option><option>存疑</option><option>图片</option></select><input id="notePage" type="number" min="1" max="629" value="1" aria-label="笔记页码"><textarea id="text" placeholder="记录本页内容、术语、问题或图像说明…"></textarea><div class="actions"><label>选择图片<input id="image" type="file" accept="image/*"></label><span id="imageName"></span><button class="primary" id="save">保存札记</button><button id="export">导出</button></div></div><div id="notes"></div></aside></main><script>
const PDF='{PDF_NAME}',storeKey='tcm-foundations-pdf-notes-v1',page=document.getElementById('page'),notePage=document.getElementById('notePage'),pdf=document.getElementById('pdf'),notes=document.getElementById('notes');
let records=[],pendingImage='';
const workspace=document.querySelector('main'),layoutKey='tcm-foundations-pdf-layout-v1',balance=document.createElement('div');
balance.className='pane-balance';balance.innerHTML='<button type="button" class="pane-balance-trigger" aria-expanded="false">分栏布局</button><div class="pane-balance-popover"><div class="pane-presets"><button type="button" data-share="0">仅 PDF</button><button type="button" data-share="25">PDF 优先</button><button type="button" data-share="50">均衡</button><button type="button" data-share="65">札记优先</button><button type="button" data-share="100">仅札记</button></div><label class="pane-slider"><span>PDF</span><input type="range" min="0" max="100" step="1" value="25" aria-label="札记窗格所占比例"><span>札记</span><output class="pane-output"></output></label></div>';document.querySelector('header strong').insertAdjacentElement('afterend',balance);
const balanceTrigger=balance.querySelector('.pane-balance-trigger'),balanceSlider=balance.querySelector('input'),balanceOutput=balance.querySelector('output');
function applyPaneShare(raw,persist=true){{const share=Math.max(0,Math.min(100,Number(raw)||0));workspace.classList.toggle('pdf-only',share===0);workspace.classList.toggle('notes-only',share===100);workspace.style.setProperty('--pdf-share',`${{100-share}}fr`);workspace.style.setProperty('--notes-share',`${{share}}fr`);balanceSlider.value=String(share);balanceOutput.textContent=share===0?'仅 PDF':share===100?'仅札记':`PDF ${{100-share}}% · 札记 ${{share}}%`;balance.querySelectorAll('[data-share]').forEach(button=>button.classList.toggle('active',Number(button.dataset.share)===share));if(persist)localStorage.setItem(layoutKey,String(share))}}
applyPaneShare(localStorage.getItem(layoutKey)??'25',false);balanceTrigger.onclick=e=>{{e.stopPropagation();const open=balance.classList.toggle('open');balanceTrigger.setAttribute('aria-expanded',String(open))}};balance.querySelector('.pane-presets').onclick=e=>{{const button=e.target.closest('[data-share]');if(button)applyPaneShare(button.dataset.share)}};balanceSlider.oninput=e=>applyPaneShare(e.target.value);document.addEventListener('click',e=>{{if(!balance.contains(e.target)){{balance.classList.remove('open');balanceTrigger.setAttribute('aria-expanded','false')}}}});
try{{records=JSON.parse(localStorage.getItem(storeKey)||'[]')}}catch{{records=[]}}
function go(n){{const value=Math.max(1,Math.min(629,Number(n)||1));page.value=value;notePage.value=value;pdf.src=`${{PDF}}#page=${{value}}&view=FitH`;render()}}
function saveAll(){{try{{localStorage.setItem(storeKey,JSON.stringify(records));return true}}catch(error){{alert('本机札记空间已满。请先导出札记并删除部分图片后重试。');return false}}}}
function render(){{const current=Number(page.value),shown=records.filter(x=>x.page===current).sort((a,b)=>b.created.localeCompare(a.created));notes.innerHTML=shown.length?shown.map(x=>`<article class="note" data-id="${{x.id}}"><header><b>第 ${{x.page}} 页 · ${{x.kind}}</b><time>${{new Date(x.created).toLocaleString('zh-CN')}}</time><button data-delete="${{x.id}}">删除</button></header>${{x.text?`<p>${{escapeHtml(x.text)}}</p>`:''}}${{x.image?`<img src="${{x.image}}" alt="第 ${{x.page}} 页附图">`:''}}</article>`).join(''):'<p class="empty">本页暂无札记。</p>'}}
function escapeHtml(value){{const node=document.createElement('div');node.textContent=value;return node.innerHTML}}
function prepareImage(file){{const reader=new FileReader();reader.onload=()=>{{const image=new Image();image.onload=()=>{{const limit=1400,scale=Math.min(1,limit/Math.max(image.width,image.height)),canvas=document.createElement('canvas');canvas.width=Math.round(image.width*scale);canvas.height=Math.round(image.height*scale);canvas.getContext('2d').drawImage(image,0,0,canvas.width,canvas.height);pendingImage=canvas.toDataURL('image/jpeg',.82);document.getElementById('imageName').textContent=`${{file.name}} · 已压缩`}};image.onerror=()=>alert('无法读取所选图片。');image.src=reader.result}};reader.onerror=()=>alert('无法读取所选图片。');reader.readAsDataURL(file)}}
document.getElementById('jump').onclick=()=>go(page.value);page.onchange=()=>go(page.value);
document.getElementById('image').onchange=e=>{{const file=e.target.files[0];if(file){{document.getElementById('imageName').textContent=`${{file.name}} · 处理中…`;prepareImage(file)}}}};
document.getElementById('save').onclick=()=>{{const text=document.getElementById('text').value.trim(),kind=document.getElementById('kind').value,p=Number(notePage.value);if(!text&&!pendingImage)return alert('请填写札记或选择图片。');records.push({{id:crypto.randomUUID?.()||String(Date.now()),page:Math.max(1,Math.min(629,p||1)),kind,text,image:pendingImage,created:new Date().toISOString()}});if(!saveAll()){{records.pop();return}}document.getElementById('text').value='';document.getElementById('image').value='';document.getElementById('imageName').textContent='';pendingImage='';go(p)}};
notes.onclick=e=>{{const id=e.target.dataset.delete;if(!id)return;if(confirm('删除这条札记？')){{const previous=records;records=records.filter(x=>x.id!==id);if(!saveAll())records=previous;render()}}}};
document.getElementById('export').onclick=()=>{{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify({{version:1,book:'中医基础理论',exportedAt:new Date().toISOString(),notes:records}},null,2)],{{type:'application/json'}}));a.download='中医基础理论_PDF札记.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)}};go(1);
</script><script>window.ReadingWorkspace={{directoryHref:'../index.html',bookDirectoryHref:'index.html'}};</script><script src="../mobile_pwa.js"></script></body></html>'''


def index_page() -> str:
    cards = "".join(f'''<article><span>{number:02d}</span><div><small>{escape(chapter['unit'])}</small><h2>{escape(chapter['title'])}</h2><p>{escape(chapter['lead'])}</p></div><a href="chapters/{chapter['slug']}/editor.html?view=annotated">阅读</a></article>''' for number, chapter in enumerate(CHAPTERS, 1))
    sources = "".join(f'<li><a href="{escape(item["url"], quote=True)}" target="_blank" rel="noreferrer">{escape(item["title"])}</a><small>{escape(item["type"])}</small></li>' for item in SOURCES)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>《中医基础理论》原创学习教材</title><link rel="stylesheet" href="../workspace_theme.css"><style>*{{box-sizing:border-box}}body{{margin:0;background:#f3f1eb;color:#25231f;font-family:Arial,"PingFang SC",sans-serif}}header{{padding:34px max(20px,6vw);background:linear-gradient(135deg,#173e33,#79552c);color:#fff}}header a{{color:#d9f2e6}}h1{{margin:.2em 0;font:700 clamp(39px,7vw,70px)/1.05 "Songti SC",serif}}header p{{max-width:800px;line-height:1.75}}.header-actions{{display:flex;gap:8px;flex-wrap:wrap}}.header-actions a{{padding:8px 11px;border:1px solid #ffffff66;border-radius:18px;text-decoration:none}}main{{width:min(1050px,calc(100% - 28px));margin:20px auto 90px}}.notice,.sources{{padding:17px;border:1px solid #dfc782;background:#fff8df;line-height:1.7}}.chapters{{display:grid;gap:8px;margin-top:16px}}article{{display:grid;grid-template-columns:42px minmax(0,1fr) auto;gap:13px;align-items:center;padding:15px;border:1px solid #d8d2c6;background:#fff}}article h2{{margin:3px 0;font:700 21px "Songti SC",serif}}article p{{margin:5px 0 0;color:#625e55;line-height:1.55}}article small{{color:#8a5c2c}}article>a{{padding:8px 12px;border:1px solid #b9cfc3;border-radius:18px;color:#176b4b;text-decoration:none;font-weight:700}}.sources{{margin-top:20px;background:#fff}}.sources li{{display:flex;justify-content:space-between;gap:12px;margin:8px 0}}.sources a{{color:#176b4b}}@media(max-width:620px){{article{{grid-template-columns:30px 1fr}}article>a{{grid-column:2;justify-self:start}}.sources li{{display:block}}}}</style></head><body><header><a href="../index.html#tcm_foundations">← Reader library</a><h1>《中医基础理论》</h1><p>官方完整 PDF 为主教材；原创学习版用于概念解释、证据边界和复习，不重复转录 629 页原书正文。</p><div class="header-actions"><a href="source_reader.html">打开 PDF 与页边札记</a><a href="{PDF_NAME}" target="_blank">单独打开原书 PDF</a><a href="{PDF_SOURCE_URL}" target="_blank" rel="noreferrer">山东医学高等专科学校来源</a></div></header><main><p class="notice"><strong>阅读方式：</strong>以原书 PDF 保留完整文字、表格和图像；在 PDF 工作台右栏按页记录笔记、批注、存疑和图片。下列 11 章是原创学习指南，可检索、编辑和复习，但不替代原书。</p><section class="chapters">{cards}</section><section class="sources"><h2>框架与术语参考</h2><ul>{sources}</ul></section></main><script src="../workspace_skin.js"></script><script src="../mobile_pwa.js"></script></body></html>'''


def build() -> None:
    for number, chapter in enumerate(CHAPTERS, 1):
        folder = BASE / "chapters" / chapter["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "editor.html").write_text(chapter_page(chapter, number), encoding="utf-8")
    (BASE / "index.html").write_text(index_page(), encoding="utf-8")
    (BASE / "source_reader.html").write_text(source_reader_page(), encoding="utf-8")
    chapters = [{"number": number, "slug": chapter["slug"], "title": chapter["title"], "unit": chapter["unit"]} for number, chapter in enumerate(CHAPTERS, 1)]
    manifest = {"schema_version": 1, "id": "tcm_foundations", "title": "中医基础理论", "edition": "官方 PDF + 原创学习版 v2", "language": "zh-CN", "medical_use": "education_only", "source_pdf": {"path": PDF_NAME, "url": PDF_SOURCE_URL, "pages": 629, "text_selectable": True}, "chapters": chapters, "units": [{"path": f"chapters/{chapter['slug']}/editor.html", "title": chapter["title"]} for chapter in CHAPTERS], "components": {"pdf_workbench": {"path": "source_reader.html"}, "source_pdf": {"path": PDF_NAME}}, "sources": SOURCES}
    (BASE / "book_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(CHAPTERS)} Chinese medicine foundations chapters")


if __name__ == "__main__":
    build()
