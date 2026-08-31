#!/usr/bin/env python3
"""Build the Russian-wars selector and initial Reader articles."""

from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote

BASE = Path(__file__).resolve().parent
PERIOD = "period_06_1801_1855"

ARTICLES = [
    {
        "id": "01_period_introduction", "type": "Введение", "year": "1801–1855",
        "ru": "Россия и европейская система войн, 1801–1855",
        "en_title": "Russia and the European system of war, 1801–1855",
        "zh_title": "1801—1855年的俄国与欧洲战争体系",
        "ru_text": [
            "Первая половина XIX века связала войны Российской империи с борьбой великих держав в Европе, расширением на Кавказе и соперничеством вокруг Османской империи.",
            "Период начинается участием России в коалициях против наполеоновской Франции. Отечественная война 1812 года стала его центральным событием, но она была частью более широкой цепи кампаний 1805–1814 годов.",
            "После Венского конгресса империя оставалась одной из ведущих европейских держав. Одновременно продолжались войны с Персией и Османской империей и длительная Кавказская война.",
            "Крымская война завершает этот раздел. Она выявила дипломатическую изоляцию России и серьёзные ограничения её военной, транспортной и административной системы.",
        ],
        "en": "This period connects Russia's wars against Napoleonic France with imperial expansion in the Caucasus and rivalry surrounding the Ottoman Empire. The War of 1812 is central but belongs to a wider sequence of campaigns. The Crimean War closes the period and exposed important diplomatic, military, and administrative weaknesses.",
        "zh": "本时期把俄国反对拿破仑法国的战争、在高加索地区的扩张以及围绕奥斯曼帝国的竞争联系在一起。1812年卫国战争是核心事件，但它属于一系列更广泛的战役。克里米亚战争结束了这一时期，并暴露出俄国在外交、军事和行政方面的重要弱点。",
        "source": "https://www.prlib.ru/collections/2087403",
    },
    {
        "id": "02_patriotic_war_1812", "type": "Война", "year": "1812",
        "ru": "Отечественная война 1812 года",
        "en_title": "The Patriotic War of 1812", "zh_title": "1812年俄国卫国战争",
        "ru_text": [
            "В июне 1812 года Великая армия Наполеона перешла западную границу Российской империи. Русские армии отступали, стремясь соединиться и избежать разгрома по отдельности.",
            "После Смоленска главнокомандующим был назначен Михаил Кутузов. Бородинское сражение 7 сентября (26 августа по старому стилю) было чрезвычайно кровопролитным, но не уничтожило русскую армию.",
            "Оставление Москвы лишило Наполеона ожидаемого политического решения. Французская армия начала отступление, испытывая недостаток снабжения, потери в боях и воздействие суровой погоды.",
            "К концу года основные силы вторжения были вытеснены из России. Кампания продолжилась за пределами империи в 1813–1814 годах и закончилась вступлением союзников в Париж.",
        ],
        "en": "Napoleon's Grande Armée invaded in June 1812. Russian forces withdrew and preserved their armies; Borodino was exceptionally costly but indecisive. Napoleon occupied Moscow without obtaining peace, then retreated amid combat losses, supply failure, and severe weather. The campaign continued in Europe in 1813–1814.",
        "zh": "拿破仑的大军于1812年6月入侵俄国。俄军撤退并保存了主力；博罗季诺战役伤亡极大，却没有形成决定性结果。拿破仑占领莫斯科后未能获得和约，随后在战斗损失、补给失败和严寒天气中撤退。战争在1813—1814年继续扩展到欧洲。",
        "source": "https://www.prlib.ru/section/2087411",
    },
    {
        "id": "03_crimean_war", "type": "Война", "year": "1853–1856",
        "ru": "Крымская война",
        "en_title": "The Crimean War", "zh_title": "克里米亚战争",
        "ru_text": [
            "Крымская война выросла из русско-османского конфликта, связанного с вопросами влияния, дипломатии и положения христианских подданных Османской империи.",
            "После уничтожения османской эскадры при Синопе Великобритания и Франция вступили в войну на стороне Османской империи. Главным театром стала осада Севастополя, хотя военные действия шли также на Кавказе, Балтике и Белом море.",
            "Оборона Севастополя продолжалась почти год. Война показала значение парового флота, современной логистики, телеграфной связи и организованной медицинской помощи.",
            "Парижский мир 1856 года ограничил российское военное присутствие на Чёрном море. Поражение усилило понимание необходимости государственных и военных реформ.",
        ],
        "en": "The conflict began as a Russo-Ottoman crisis and widened when Britain and France entered the war. The siege of Sevastopol became its principal theater, while fighting also occurred in the Caucasus, Baltic, and White Sea. The 1856 Treaty of Paris restricted Russian power in the Black Sea and strengthened pressure for reform.",
        "zh": "战争最初是俄国与奥斯曼帝国之间的危机，英国和法国参战后扩大。塞瓦斯托波尔围城成为主要战场，同时高加索、波罗的海和白海也发生战事。1856年《巴黎和约》限制了俄国在黑海的军事力量，并加强了改革压力。",
        "source": "https://www.britannica.com/event/Crimean-War",
    },
    {
        "id": "04_period_summary", "type": "Итоги периода", "year": "1801–1856",
        "ru": "Итоги периода: от победы над Наполеоном к Крымской войне",
        "en_title": "Period summary: from victory over Napoleon to the Crimean War",
        "zh_title": "时期总结：从战胜拿破仑到克里米亚战争",
        "ru_text": [
            "К 1815 году Россия достигла вершины своего влияния в европейской политике и участвовала в создании послевоенного порядка.",
            "Однако продолжительные войны на южных и кавказских границах требовали больших ресурсов и не укладывались в единую простую схему европейского равновесия.",
            "Крымская война не уничтожила статус России как великой державы, но продемонстрировала разрыв между её политическими притязаниями и возможностями инфраструктуры, вооружения и управления.",
            "Поэтому следующий исторический период следует читать через реформы после 1856 года, изменение армии и новые формы имперского и национального соперничества.",
        ],
        "en": "Russia emerged from the Napoleonic Wars with exceptional influence, yet long frontier wars consumed resources. The Crimean defeat exposed a gap between geopolitical ambitions and institutional capacity. Reform after 1856 therefore provides the bridge to the next period.",
        "zh": "俄国在拿破仑战争后取得了显著的欧洲影响力，但长期边疆战争消耗了大量资源。克里米亚战争的失败暴露出地缘政治目标与制度能力之间的差距，因此1856年后的改革构成了通向下一时期的桥梁。",
        "source": "https://historyrussia.org/sobytiya/vpervye-sobrany-i-opisany-vse-vojny-rossii-s-860-do-1914-g.html",
    },
]

PERIODS = {
    "period_05_1689_1801": "Период 5 · 1689–1801",
    "period_06_1801_1855": "Период 6 · 1801–1855",
    "period_07_1855_1917": "Период 7 · 1855–1917",
    "period_08_1917_1922": "Период 8 · 1917–1922",
    "period_09_1922_1941": "Период 9 · 1922–1941",
    "period_10_1939_1945": "Период 10 · 1939–1945",
}

for article in ARTICLES:
    article["period"] = PERIOD

ARTICLES += [
    {
        "id": "01_period_introduction", "period": "period_05_1689_1801", "type": "Введение", "year": "1689–1801",
        "ru": "Россия в войнах XVIII века", "en_title": "Russia in the wars of the eighteenth century", "zh_title": "18世纪战争中的俄国",
        "ru_text": [
            "В XVIII веке Россия создала постоянную армию и военно-морской флот европейского типа и стала активным участником системы великих держав.",
            "Северная война открыла устойчивый выход к Балтийскому морю. Последующие войны были связаны с Польшей, Османской империей, Швецией и общеевропейскими коалициями.",
            "Расширение государства сопровождалось огромными расходами, рекрутскими наборами и перестройкой управления. Военную историю периода поэтому следует читать вместе с историей государства и общества.",
        ],
        "en": "During the eighteenth century Russia built a permanent European-style army and navy and became an active great power. The Great Northern War secured a Baltic position; later conflicts involved Poland, the Ottoman Empire, Sweden, and European coalitions. Expansion depended on extensive fiscal, administrative, and human mobilization.",
        "zh": "18世纪，俄国建立了欧洲式常备军和海军，并成为列强体系中的积极参与者。大北方战争巩固了俄国在波罗的海的地位；此后的战争涉及波兰、奥斯曼帝国、瑞典以及欧洲联盟。国家扩张依赖巨大的财政、行政和人力动员。",
        "source": "https://www.prlib.ru/collections/2087403",
    },
    {
        "id": "02_great_northern_war", "period": "period_05_1689_1801", "type": "Война", "year": "1700–1721",
        "ru": "Северная война", "en_title": "The Great Northern War", "zh_title": "大北方战争",
        "ru_text": [
            "Северная война началась борьбой коалиции России, Дании и Саксонии–Речи Посполитой против господства Швеции в Балтийском регионе.",
            "После поражения под Нарвой Россия перестроила армию и расширила военное производство. Основание Санкт-Петербурга закрепило новую стратегическую ориентацию к Балтике.",
            "Полтавская битва 1709 года стала поворотным моментом, но война продолжалась ещё двенадцать лет. Ништадтский мир 1721 года передал России важные балтийские территории.",
        ],
        "en": "The Great Northern War challenged Swedish predominance in the Baltic. After defeat at Narva, Russia reorganized its army and expanded military production. Poltava was the decisive turning point, while the 1721 Treaty of Nystad confirmed major Russian territorial gains and a new Baltic position.",
        "zh": "大北方战争挑战了瑞典在波罗的海地区的优势。纳尔瓦战败后，俄国重组军队并扩大军事生产。1709年的波尔塔瓦战役成为转折点，1721年《尼斯塔德和约》确认了俄国的重要领土所得和新的波罗的海地位。",
        "source": "https://www.prlib.ru/section/2087411",
    },
    {
        "id": "03_period_summary", "period": "period_05_1689_1801", "type": "Итоги периода", "year": "1689–1801",
        "ru": "Итоги XVIII века: империя и военная мобилизация", "en_title": "Eighteenth-century summary: empire and military mobilization", "zh_title": "18世纪总结：帝国与军事动员",
        "ru_text": [
            "К концу XVIII века Россия стала одной из крупнейших военных и территориальных держав Европы.",
            "Выходы к Балтийскому и Чёрному морям изменили стратегическое положение страны, а разделы Речи Посполитой глубоко изменили политическую карту Восточной Европы.",
            "Эти достижения опирались на постоянную армию, флот, налогообложение и рекрутскую систему, издержки которых неравномерно распределялись в обществе.",
        ],
        "en": "By 1801 Russia was a major European military and territorial power. Baltic and Black Sea access transformed its strategic position, while the partitions of Poland reshaped Eastern Europe. These gains rested on a permanent army, navy, taxation, and conscription whose burdens were unevenly distributed.",
        "zh": "到1801年，俄国已成为欧洲主要军事和领土强国。通往波罗的海和黑海的出入口改变了其战略地位，瓜分波兰则重塑了东欧政治版图。这些成果建立在常备军、海军、税收和征兵制度之上，其社会负担并不均衡。",
        "source": "https://www.prlib.ru/collections/2087403",
    },
    {
        "id": "01_period_introduction", "period": "period_07_1855_1917", "type": "Введение", "year": "1855–1917",
        "ru": "Поздняя Российская империя: реформы и новые войны", "en_title": "Late Imperial Russia: reform and new wars", "zh_title": "晚期俄罗斯帝国：改革与新战争",
        "ru_text": [
            "После Крымской войны правительство приступило к военным и государственным реформам. Всеобщая воинская повинность 1874 года изменила основы комплектования армии.",
            "Русско-турецкая война 1877–1878 годов показала как новые возможности, так и сохранявшиеся проблемы управления и снабжения.",
            "Поражение в Русско-японской войне усилило внутренний кризис. Первая мировая война потребовала мобилизации в масштабе, который имперские институты не смогли устойчиво выдержать.",
        ],
        "en": "After the Crimean War, military and state reforms changed recruitment, command, and administration. The Russo-Turkish War demonstrated both improvement and persistent logistical problems. Defeat by Japan deepened domestic crisis, and the immense demands of the First World War overwhelmed imperial institutions.",
        "zh": "克里米亚战争后，军事和国家改革改变了征兵、指挥和行政制度。俄土战争既显示出改善，也暴露了持续存在的后勤问题。日俄战争的失败加深了国内危机，而第一次世界大战的巨大动员需求最终压垮了帝国制度。",
        "source": "https://www.prlib.ru/collections/2087403",
    },
    {
        "id": "02_russo_japanese_war", "period": "period_07_1855_1917", "type": "Война", "year": "1904–1905",
        "ru": "Русско-японская война", "en_title": "The Russo-Japanese War", "zh_title": "日俄战争",
        "ru_text": [
            "Русско-японская война возникла из соперничества за влияние в Маньчжурии и Корее. Япония начала военные действия нападением на российские корабли у Порт-Артура.",
            "Главные сухопутные сражения произошли в Южной Маньчжурии. Падение Порт-Артура и поражение под Мукденом ухудшили положение России.",
            "В Цусимском сражении японский флот уничтожил большую часть Второй Тихоокеанской эскадры. Портсмутский мир завершил войну и подтвердил усиление Японии в Восточной Азии.",
        ],
        "en": "The war grew from rivalry in Manchuria and Korea. Japan attacked Russian ships near Port Arthur, won major campaigns in southern Manchuria, and destroyed most of the Russian Baltic Fleet at Tsushima. The Treaty of Portsmouth confirmed Japan's rising position in East Asia and intensified political crisis in Russia.",
        "zh": "战争源于俄国与日本在满洲和朝鲜的竞争。日本袭击旅顺附近的俄国军舰，在南满取得主要战役胜利，并在对马海战中摧毁俄国波罗的海舰队主力。《朴次茅斯和约》确认了日本在东亚地位的上升，也加剧了俄国国内政治危机。",
        "source": "https://www.prlib.ru/section/683598",
    },
    {
        "id": "03_period_summary", "period": "period_07_1855_1917", "type": "Итоги периода", "year": "1855–1917",
        "ru": "Итоги позднеимперского периода", "en_title": "Summary of the late imperial period", "zh_title": "晚期帝国时期总结",
        "ru_text": [
            "Военные реформы после 1856 года повысили способность государства мобилизовать массовую армию, но не устранили все проблемы управления, транспорта и снабжения.",
            "Железные дороги, телеграф, скорострельное оружие и индустриальное производство изменили масштаб войны быстрее, чем адаптировались многие учреждения.",
            "К 1917 году военные потери, хозяйственные трудности и политический конфликт соединились в кризис, завершивший историю Российской империи.",
        ],
        "en": "Post-1856 reforms improved mass mobilization but did not eliminate administrative and logistical weaknesses. Industrial warfare changed faster than many institutions could adapt. By 1917 casualties, economic disruption, and political conflict had combined in the crisis that ended the empire.",
        "zh": "1856年后的改革提高了大规模动员能力，却未能消除行政和后勤弱点。工业化战争的变化速度超过了许多制度的适应能力。到1917年，战争伤亡、经济混乱和政治冲突汇合成终结帝国的危机。",
        "source": "https://historyrussia.org/sobytiya/vpervye-sobrany-i-opisany-vse-vojny-rossii-s-860-do-1914-g.html",
    },
]

BATTLES = {
    "02_great_northern_war@period_05_1689_1801": [
        {"date": "1700", "ru": "Битва при Нарве", "en": "Battle of Narva", "zh": "纳尔瓦战役", "note": "Крупное поражение русской армии в начале войны; ускорило военную реорганизацию."},
        {"date": "1709", "ru": "Полтавская битва", "en": "Battle of Poltava", "zh": "波尔塔瓦战役", "note": "Решающая победа России над главной армией Карла XII."},
        {"date": "1714", "ru": "Гангутское сражение", "en": "Battle of Gangut", "zh": "汉科海战", "note": "Первая крупная победа русского галерного флота."},
    ],
    "02_patriotic_war_1812@period_06_1801_1855": [
        {"date": "1812", "ru": "Смоленское сражение", "en": "Battle of Smolensk", "zh": "斯摩棱斯克战役", "note": "Русские армии продолжили организованное отступление после тяжёлых боёв."},
        {"date": "1812", "ru": "Бородинское сражение", "en": "Battle of Borodino", "zh": "博罗季诺战役", "note": "Крайне кровопролитное генеральное сражение без уничтожения русской армии."},
        {"date": "1812", "ru": "Сражение под Малоярославцем", "en": "Battle of Maloyaroslavets", "zh": "小雅罗斯拉韦茨战役", "note": "Повлияло на направление французского отступления из Москвы."},
        {"date": "1812", "ru": "Сражение на Березине", "en": "Battle of Berezina", "zh": "别列津纳河战役", "note": "Французская армия переправилась с большими потерями и продолжила отступление."},
    ],
    "03_crimean_war@period_06_1801_1855": [
        {"date": "1854", "ru": "Сражение на Альме", "en": "Battle of the Alma", "zh": "阿尔马河战役", "note": "Победа союзников открыла путь к осаде Севастополя."},
        {"date": "1854", "ru": "Балаклавское сражение", "en": "Battle of Balaclava", "zh": "巴拉克拉瓦战役", "note": "Неоднозначное сражение, известное кавалерийскими атаками и борьбой за коммуникации."},
        {"date": "1854", "ru": "Инкерманское сражение", "en": "Battle of Inkerman", "zh": "因克尔曼战役", "note": "Неудачная попытка русских войск снять осаду Севастополя."},
        {"date": "1854–1855", "ru": "Оборона Севастополя", "en": "Siege of Sevastopol", "zh": "塞瓦斯托波尔围城战", "note": "Главная и почти годичная кампания войны в Крыму."},
    ],
    "02_russo_japanese_war@period_07_1855_1917": [
        {"date": "1904–1905", "ru": "Оборона Порт-Артура", "en": "Siege of Port Arthur", "zh": "旅顺围攻战", "note": "Длительная осада завершилась капитуляцией российской крепости."},
        {"date": "1904", "ru": "Ляоянское сражение", "en": "Battle of Liaoyang", "zh": "辽阳会战", "note": "Крупное сухопутное сражение, после которого русская армия отступила к Мукдену."},
        {"date": "1905", "ru": "Мукденское сражение", "en": "Battle of Mukden", "zh": "奉天会战", "note": "Одно из крупнейших сухопутных сражений эпохи до Первой мировой войны."},
        {"date": "1905", "ru": "Цусимское сражение", "en": "Battle of Tsushima", "zh": "对马海战", "note": "Решительная победа японского флота над Второй Тихоокеанской эскадрой."},
    ],
    "02_russian_civil_war@period_08_1917_1922": [
        {"date": "1918", "ru": "Казанская операция", "en": "Kazan operation", "zh": "喀山战役", "note": "Взятие Казани Красной армией стало важным поворотом на Восточном фронте."},
        {"date": "1919", "ru": "Орловско-Кромская операция", "en": "Orel–Kromy operation", "zh": "奥廖尔—克罗梅战役", "note": "Красная армия остановила наступление сил Деникина на московском направлении."},
        {"date": "1920", "ru": "Перекопско-Чонгарская операция", "en": "Perekop–Chongar operation", "zh": "彼列科普—琼加尔战役", "note": "Прорыв в Крым привёл к поражению основных сил Русской армии Врангеля."},
    ],
    "02_winter_war@period_09_1922_1941": [
        {"date": "1939", "ru": "Битва при Толваярви", "en": "Battle of Tolvajärvi", "zh": "托尔瓦耶尔维战役", "note": "Заметная финская победа на раннем этапе войны."},
        {"date": "1939–1940", "ru": "Сражение при Суомуссалми", "en": "Battle of Suomussalmi", "zh": "苏奥穆斯萨尔米战役", "note": "Финские силы разгромили несколько советских соединений в сложных зимних условиях."},
        {"date": "1940", "ru": "Бои за Сумму", "en": "Battles of Summa", "zh": "苏马战役", "note": "Ключевые бои при прорыве главной полосы линии Маннергейма."},
    ],
    "02_great_patriotic_war@period_10_1939_1945": [
        {"date": "1941–1942", "ru": "Битва за Москву", "en": "Battle of Moscow", "zh": "莫斯科战役", "note": "Срыв германского плана захвата столицы и первое крупное стратегическое контрнаступление Красной армии."},
        {"date": "1942–1943", "ru": "Сталинградская битва", "en": "Battle of Stalingrad", "zh": "斯大林格勒战役", "note": "Окружение и капитуляция крупной группировки стран Оси изменили стратегическую обстановку."},
        {"date": "1943", "ru": "Курская битва", "en": "Battle of Kursk", "zh": "库尔斯克战役", "note": "После отражения германского наступления стратегическая инициатива закрепилась за Красной армией."},
        {"date": "1944", "ru": "Операция «Багратион»", "en": "Operation Bagration", "zh": "巴格拉季昂行动", "note": "Разгром германской группы армий «Центр» и освобождение Белоруссии."},
        {"date": "1945", "ru": "Берлинская операция", "en": "Battle of Berlin", "zh": "柏林战役", "note": "Заключительная крупная операция в Европе, завершившаяся падением Берлина."},
    ],
}

BATTLE_SUPPORT = {
    "Битва при Нарве": ("A major Russian defeat at the beginning of the war accelerated military reorganization.", "俄军在战争初期遭受重大失败，从而加速了军事重组。"),
    "Полтавская битва": ("A decisive Russian victory over the main army of Charles XII.", "俄军对卡尔十二世主力取得决定性胜利。"),
    "Гангутское сражение": ("The first major victory of Russia's galley fleet.", "俄国桨帆舰队取得的第一次重大胜利。"),
    "Смоленское сражение": ("After heavy fighting, the Russian armies continued their organized withdrawal.", "经过激烈战斗，俄军继续有组织地撤退。"),
    "Бородинское сражение": ("An exceptionally costly general engagement that did not destroy the Russian army.", "这是一场伤亡极大的大会战，但俄军并未被摧毁。"),
    "Сражение под Малоярославцем": ("The battle influenced the route of the French retreat from Moscow.", "这场战役影响了法军从莫斯科撤退的路线。"),
    "Сражение на Березине": ("The French army crossed the river with heavy losses and continued its retreat.", "法军在付出重大损失后渡河并继续撤退。"),
    "Сражение на Альме": ("The Allied victory opened the route toward the siege of Sevastopol.", "盟军的胜利打开了通向塞瓦斯托波尔围城战的道路。"),
    "Балаклавское сражение": ("An inconclusive battle remembered for cavalry attacks and fighting over communications.", "这场结果不明确的战役因骑兵冲锋和交通线争夺而闻名。"),
    "Инкерманское сражение": ("An unsuccessful Russian attempt to break the siege of Sevastopol.", "俄军试图解除塞瓦斯托波尔之围，但未获成功。"),
    "Оборона Севастополя": ("The principal Crimean campaign lasted for almost a year.", "这是克里米亚战场持续近一年的主要战役。"),
    "Оборона Порт-Артура": ("The prolonged siege ended with the surrender of the Russian fortress.", "长期围攻最终以俄国要塞投降告终。"),
    "Ляоянское сражение": ("After this major land battle, the Russian army withdrew toward Mukden.", "这场大规模陆战后，俄军向奉天方向撤退。"),
    "Мукденское сражение": ("One of the largest land battles fought before the First World War.", "这是第一次世界大战前规模最大的陆战之一。"),
    "Цусимское сражение": ("A decisive Japanese naval victory over Russia's Second Pacific Squadron.", "日本海军对俄国第二太平洋舰队取得决定性胜利。"),
    "Казанская операция": ("The Red Army's capture of Kazan marked an important turn on the Eastern Front.", "红军夺取喀山成为东线战局的重要转折。"),
    "Орловско-Кромская операция": ("The Red Army stopped Denikin's advance toward Moscow.", "红军阻止了邓尼金军队向莫斯科方向的推进。"),
    "Перекопско-Чонгарская операция": ("The breakthrough into Crimea led to the defeat of Wrangel's principal forces.", "红军突破进入克里米亚，导致弗兰格尔军主力失败。"),
    "Битва при Толваярви": ("A significant Finnish victory during the early stage of the war.", "芬兰军队在战争初期取得的一次重要胜利。"),
    "Сражение при Суомуссалми": ("Finnish forces defeated several Soviet formations under severe winter conditions.", "芬兰军队在严酷冬季条件下击败数支苏军部队。"),
    "Бои за Сумму": ("Key fighting in the breakthrough of the main Mannerheim Line defenses.", "这是突破曼纳海姆防线主要阵地的关键战斗。"),
    "Битва за Москву": ("The defense of the capital frustrated Germany's rapid-victory plan and led to a major Soviet counteroffensive.", "首都保卫战挫败了德国迅速取胜的计划，并引发苏军大规模反攻。"),
    "Сталинградская битва": ("The encirclement and surrender of a major Axis force transformed the strategic situation.", "大批轴心国军队被包围并投降，改变了战略形势。"),
    "Курская битва": ("After the German offensive was stopped, the Red Army consolidated the strategic initiative.", "德军攻势被阻止后，苏军巩固了战略主动权。"),
    "Операция «Багратион»": ("The operation destroyed Germany's Army Group Centre and liberated Belarus.", "这次行动摧毁了德国中央集团军群并解放白俄罗斯。"),
    "Берлинская операция": ("The final major European operation ended with the fall of Berlin.", "欧洲战场最后一次主要行动以柏林陷落告终。"),
}

ARTICLES += [
    {
        "id": "01_period_introduction", "period": "period_08_1917_1922", "type": "Введение", "year": "1917–1922",
        "ru": "Революция и распад военного пространства империи", "en_title": "Revolution and the fragmentation of the imperial military space", "zh_title": "革命与帝国军事空间的解体",
        "ru_text": [
            "Революции 1917 года произошли во время продолжающейся мировой войны и разрушения прежней системы государственной власти.",
            "После Октябрьской революции конфликт включал борьбу большевиков с различными белыми правительствами и армиями, национальные движения, крестьянские восстания и иностранное военное присутствие.",
            "Границы, участники и хронология Гражданской войны различаются в историографии. Этот раздел использует 1917–1922 годы как широкую учебную рамку и отмечает региональные различия.",
        ],
        "en": "The revolutions of 1917 unfolded during the continuing world war and the collapse of imperial authority. The ensuing conflicts involved Bolshevik and diverse anti-Bolshevik forces, national movements, peasant uprisings, and foreign intervention. Historians define the war's boundaries differently; this Reader uses 1917–1922 as a broad study frame.",
        "zh": "1917年的革命发生在世界大战仍在继续、帝国国家权力瓦解之际。随后的冲突包括布尔什维克与各种反布尔什维克力量、民族运动、农民起义和外国武装干涉。学界对内战的边界界定不一，本读本以1917—1922年作为宽泛的学习框架。",
        "source": "https://www.prlib.ru/collections/2087403",
    },
    {
        "id": "02_russian_civil_war", "period": "period_08_1917_1922", "type": "Война", "year": "1917–1922",
        "ru": "Гражданская война в России", "en_title": "The Russian Civil War", "zh_title": "俄国内战",
        "ru_text": [
            "Гражданская война не была единым фронтом или простой борьбой двух армий. Военные действия происходили одновременно на востоке, юге, северо-западе, севере и в других регионах.",
            "Красная армия постепенно создала централизованное командование и использовала контроль над центральными районами и железнодорожной сетью. Белые армии оставались разделёнными географически и политически.",
            "Война сопровождалась террором, эпидемиями, голодом, массовым перемещением населения и разрушением хозяйства. Эти последствия нельзя отделять от военной хронологии.",
            "К 1922 году основные организованные противники советской власти были разгромлены или вытеснены, а на большей части бывшей империи сложилось новое союзное государство.",
        ],
        "en": "The Civil War consisted of overlapping regional conflicts rather than a single two-army front. The Red Army developed centralized command and benefited from control of central territory and railways, while anti-Bolshevik forces remained geographically and politically divided. Terror, epidemic disease, famine, displacement, and economic collapse formed part of the conflict's history.",
        "zh": "俄国内战由彼此重叠的地区冲突组成，并非两支军队之间的单一战线。红军逐步形成集中指挥，并利用对中央地区和铁路网的控制；反布尔什维克力量在地理和政治上则相互分离。恐怖、疫病、饥荒、人口流离和经济崩溃都是这场战争历史的一部分。",
        "source": "https://www.prlib.ru/collections/2087403",
    },
    {
        "id": "03_period_summary", "period": "period_08_1917_1922", "type": "Итоги периода", "year": "1917–1922",
        "ru": "Итоги революции и Гражданской войны", "en_title": "Summary of revolution and civil war", "zh_title": "革命与内战时期总结",
        "ru_text": [
            "Гражданская война завершила разрушение институтов Российской империи и определила политическую форму нового советского государства.",
            "Она также изменила границы бывшей империи: одни территории вошли в СССР, другие образовали независимые государства или оказались предметом новых конфликтов.",
            "Военный опыт периода повлиял на организацию Красной армии, политический контроль, хозяйственную мобилизацию и представления советского руководства о внешней угрозе.",
        ],
        "en": "The conflict completed the destruction of imperial institutions and shaped the new Soviet state. It transformed borders across the former empire and left a military legacy of centralized command, political supervision, economic mobilization, and acute concern about external threats.",
        "zh": "内战完成了帝国制度的瓦解，并塑造了新的苏维埃国家。它改变了前帝国各地的边界，也留下集中指挥、政治监督、经济动员以及对外部威胁高度警惕的军事遗产。",
        "source": "https://www.prlib.ru/collections/2087403",
    },
    {
        "id": "01_period_introduction", "period": "period_09_1922_1941", "type": "Введение", "year": "1922–1941",
        "ru": "СССР между Гражданской и Великой Отечественной войнами", "en_title": "The USSR between the Civil War and the Great Patriotic War", "zh_title": "从内战到苏德战争之间的苏联",
        "ru_text": [
            "В межвоенные десятилетия СССР преобразовал Красную армию одновременно с индустриализацией страны и быстрым развитием авиации, танковых войск и военной промышленности.",
            "Военные действия происходили на границах и за их пределами: конфликт вокруг Китайско-Восточной железной дороги, бои у озера Хасан и на Халхин-Голе, советско-финляндская война.",
            "Политические репрессии затронули командный состав. Опыт локальных войн дал важные уроки, но их усвоение проходило неравномерно накануне германского вторжения.",
        ],
        "en": "Between the civil war and 1941, the USSR transformed the Red Army alongside industrialization and rapid development of armor, aviation, and military production. Border conflicts and the war with Finland provided operational experience, while political repression disrupted the officer corps. Lessons were absorbed unevenly before the German invasion.",
        "zh": "从内战结束到1941年，苏联在工业化进程中改造红军，并迅速发展装甲兵、航空兵和军事工业。边境冲突及苏芬战争提供了作战经验，而政治清洗冲击了军官队伍。德国入侵前，这些经验并未得到均衡吸收。",
        "source": "https://www.prlib.ru/collections/2087403",
    },
    {
        "id": "02_winter_war", "period": "period_09_1922_1941", "type": "Война", "year": "1939–1940",
        "ru": "Советско-финляндская война", "en_title": "The Soviet-Finnish War (Winter War)", "zh_title": "苏芬战争（冬季战争）",
        "ru_text": [
            "Советско-финляндская война началась 30 ноября 1939 года после неудачи переговоров о границе и безопасности Ленинграда. СССР был исключён из Лиги Наций.",
            "Красная армия первоначально понесла тяжёлые потери, столкнувшись с подготовленной обороной, сложной местностью, зимними условиями и собственными проблемами управления.",
            "После перегруппировки и усиления артиллерии советские войска прорвали главную полосу линии Маннергейма. Московский мир в марте 1940 года передал СССР территории, включая Карельский перешеек.",
            "Финляндия сохранила независимость, но понесла значительные территориальные и человеческие потери. Война повлияла на иностранные оценки боеспособности Красной армии.",
        ],
        "en": "The Soviet Union attacked Finland on 30 November 1939 after failed security and border negotiations. Initial Soviet operations suffered heavy losses against prepared defenses, difficult terrain, winter conditions, and command failures. After reorganization, Soviet forces broke the main defensive line; the March 1940 peace transferred territory while Finland retained independence.",
        "zh": "在边界与列宁格勒安全谈判失败后，苏联于1939年11月30日进攻芬兰。苏军最初面对坚固防御、复杂地形、严寒和指挥问题，伤亡惨重。经过重组后，苏军突破主要防线；1940年3月的和约使苏联获得领土，而芬兰保持独立。",
        "source": "https://www.britannica.com/event/Russo-Finnish-War",
    },
    {
        "id": "03_period_summary", "period": "period_09_1922_1941", "type": "Итоги периода", "year": "1922–1941",
        "ru": "Итоги межвоенного военного развития", "en_title": "Summary of interwar military development", "zh_title": "战间期军事发展总结",
        "ru_text": [
            "К 1941 году СССР располагал огромными вооружёнными силами и крупной военной промышленностью, созданными ценой чрезвычайного напряжения экономики и общества.",
            "Боевой опыт показал возможности современной техники и глубокие проблемы командования, связи, подготовки и снабжения.",
            "Территориальные изменения 1939–1940 годов отодвинули некоторые границы, но не предотвратили стратегическую катастрофу первых месяцев германского вторжения.",
        ],
        "en": "By 1941 the USSR possessed immense armed forces and military industry, built at extraordinary social and economic cost. Recent conflicts exposed both technological strength and serious weaknesses in command, communications, training, and supply. Territorial changes did not prevent the disasters of the first months of the German invasion.",
        "zh": "到1941年，苏联以巨大的社会经济代价建立了庞大武装力量和军事工业。近期战争既显示了技术力量，也暴露出指挥、通信、训练和补给方面的严重弱点。1939—1940年的领土变化未能避免德国入侵初期的灾难。",
        "source": "https://www.prlib.ru/collections/2087403",
    },
    {
        "id": "01_period_introduction", "period": "period_10_1939_1945", "type": "Введение", "year": "1939–1945",
        "ru": "СССР во Второй мировой войне", "en_title": "The USSR in the Second World War", "zh_title": "第二次世界大战中的苏联",
        "ru_text": [
            "Для всемирной хронологии Вторая мировая война началась в сентябре 1939 года. В российской традиции Великая Отечественная война обозначает борьбу СССР против нацистской Германии и её европейских союзников с 22 июня 1941 года.",
            "Различие терминов важно сохранять: они описывают пересекающиеся, но не тождественные временные и географические рамки.",
            "Война на советско-германском фронте отличалась исключительными масштабами мобилизации, разрушений и человеческих потерь. Военные операции следует рассматривать вместе с оккупацией, Холокостом, принудительным трудом, эвакуацией и экономикой тыла.",
        ],
        "en": "The Second World War began in September 1939 in global chronology. In Russian usage, the Great Patriotic War denotes the Soviet war against Nazi Germany and its European allies beginning on 22 June 1941. The distinction matters because the terms overlap but are not identical. Military operations must be studied alongside occupation, the Holocaust, forced labor, evacuation, and the home-front economy.",
        "zh": "按全球时间线，第二次世界大战始于1939年9月。俄罗斯语境中的“伟大卫国战争”特指自1941年6月22日起苏联对纳粹德国及其欧洲盟国的战争。两者相互重叠但并不相同。研究军事行动时还必须考虑占领、犹太人大屠杀、强迫劳动、疏散和后方经济。",
        "source": "https://www.prlib.ru/collections/2087403",
    },
    {
        "id": "02_great_patriotic_war", "period": "period_10_1939_1945", "type": "Война", "year": "1941–1945",
        "ru": "Великая Отечественная война", "en_title": "The Great Patriotic War", "zh_title": "苏联伟大卫国战争",
        "ru_text": [
            "22 июня 1941 года Германия и её союзники напали на СССР. В первые месяцы Красная армия потеряла огромные территории, людей и технику, но государство продолжило мобилизацию и эвакуацию промышленности.",
            "Сражение за Москву сорвало расчёт на быструю победу. Сталинградская битва и последующие операции 1942–1943 годов изменили стратегическую инициативу, а Курская битва закрепила её переход к Красной армии.",
            "В 1944 году советские наступления освободили большую часть оккупированной территории СССР и перенесли войну в Центральную и Юго-Восточную Европу.",
            "Берлинская операция завершилась капитуляцией Германии в мае 1945 года. Победа была достигнута ценой колоссальных военных и гражданских потерь и стала центральным событием советской и постсоветской исторической памяти.",
        ],
        "en": "Germany and its allies invaded the USSR on 22 June 1941. Despite catastrophic early losses, Soviet mobilization and industrial evacuation continued. Moscow prevented a rapid German victory; Stalingrad and subsequent operations shifted the strategic initiative, and Kursk consolidated that change. Soviet offensives reached Central Europe, culminating in Germany's surrender in May 1945 at immense military and civilian cost.",
        "zh": "德国及其盟国于1941年6月22日入侵苏联。尽管初期损失惨重，苏联仍继续动员并疏散工业。莫斯科战役阻止了德国迅速取胜；斯大林格勒战役及随后行动改变了战略主动权，库尔斯克战役则巩固了这一转变。苏军攻入中欧，最终促成德国于1945年5月投降，代价是极其巨大的军民伤亡。",
        "source": "https://www.prlib.ru/collections/2087403",
    },
    {
        "id": "03_period_summary", "period": "period_10_1939_1945", "type": "Итоги периода", "year": "1939–1945",
        "ru": "Итоги Второй мировой войны для СССР", "en_title": "Consequences of the Second World War for the USSR", "zh_title": "第二次世界大战对苏联的影响",
        "ru_text": [
            "СССР вышел из войны одной из двух ведущих мировых держав и сыграл решающую роль в разгроме нацистской Германии.",
            "Одновременно страна понесла огромные демографические, материальные и культурные потери. Миллионы людей погибли, были ранены, перемещены или пережили оккупацию.",
            "Послевоенные границы, военное присутствие СССР в Восточной Европе, создание Организации Объединённых Наций и начало холодной войны определили новый международный порядок.",
            "Изучение итогов требует различать военную победу, человеческую цену, государственную память и опыт разных групп населения.",
        ],
        "en": "The USSR emerged as a leading world power and played a decisive role in defeating Nazi Germany, while suffering immense demographic, material, and cultural losses. Postwar borders, Soviet power in Eastern Europe, the United Nations, and the emerging Cold War shaped a new order. Study of the outcome must distinguish military victory, human cost, state memory, and varied civilian experience.",
        "zh": "苏联成为世界主要强国之一，并在击败纳粹德国中发挥决定性作用，同时承受了巨大的人员、物质和文化损失。战后边界、苏联在东欧的力量、联合国的建立以及冷战的开始塑造了新秩序。研究战争结果时必须区分军事胜利、人类代价、国家记忆以及不同群体的经历。",
        "source": "https://www.prlib.ru/collections/2087403",
    },
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def editing_toolbar() -> str:
    return '''<nav class="toolbar" aria-label="Editing tools"><div class="toolbar-modes" role="group" aria-label="Tool set"><button type="button" data-toolbar-mode="full">Full</button><button type="button" data-toolbar-mode="simple">Simplified</button></div><div class="toolbar-group"><button type="button" data-command="undo">Undo</button><button type="button" data-command="redo">Redo</button><button type="button" data-command="bold"><b>B</b></button><button type="button" data-command="italic"><i>I</i></button><button type="button" data-command="underline"><u>U</u></button><button type="button" data-command="highlight">Highlight</button><button type="button" data-command="removeFormat">Clear</button><button type="button" data-command="save">Save</button></div><div class="toolbar-group full-only"><button type="button" id="wordAnnotation">Word annotation</button><button type="button" id="speakText" class="primary">Read aloud</button><button type="button" id="pauseSpeech" disabled>Pause</button><button type="button" id="stopSpeech" disabled>Stop</button><select id="speechVoice" aria-label="Voice"><option value="">System voice</option></select><label class="speech-rate">Speed <input id="speechRate" type="range" min="0.5" max="1.5" step="0.1" value="0.8"><output id="speechRateValue">0.8×</output></label></div></nav>'''


def toolbar_script() -> str:
    return r'''const toolbar=document.querySelector('.toolbar'),toolbarModeKey='reader-toolbar-mode';
function setToolbarMode(mode){mode=mode==='simple'?'simple':'full';document.body.classList.toggle('toolbar-simple',mode==='simple');toolbar.querySelectorAll('[data-toolbar-mode]').forEach(button=>{const active=button.dataset.toolbarMode===mode;button.classList.toggle('active',active);button.setAttribute('aria-pressed',String(active))});localStorage.setItem(toolbarModeKey,mode)}
setToolbarMode(localStorage.getItem(toolbarModeKey)||'full');
toolbar.addEventListener('click',event=>{const mode=event.target.closest('[data-toolbar-mode]')?.dataset.toolbarMode;if(mode)setToolbarMode(mode)});
const voiceSelect=document.getElementById('speechVoice'),speechRate=document.getElementById('speechRate'),speechRateValue=document.getElementById('speechRateValue'),speakButton=document.getElementById('speakText'),pauseButton=document.getElementById('pauseSpeech'),stopButton=document.getElementById('stopSpeech');
function loadVoices(){const current=voiceSelect.value,voices=speechSynthesis.getVoices();voiceSelect.innerHTML='<option value="">System voice</option>'+voices.map((voice,index)=>`<option value="${index}">${voice.name} · ${voice.lang}</option>`).join('');if([...voiceSelect.options].some(option=>option.value===current))voiceSelect.value=current}
if('speechSynthesis' in window){loadVoices();speechSynthesis.onvoiceschanged=loadVoices}else{speakButton.disabled=true}
function selectedReading(){const selection=getSelection(),text=selection?.toString().trim();if(text){const node=selection.anchorNode?.nodeType===1?selection.anchorNode:selection.anchorNode?.parentElement,explicit=node?.closest('[lang]')?.lang;return{text,lang:explicit||(node?.closest('[data-panel="zh"]')?'zh-CN':node?.closest('[data-panel="en"]')?'en-US':'ru-RU')}}const active=document.querySelector('[data-panel]:not([hidden])');return{text:(active||editor).innerText.trim(),lang:active?.dataset.panel==='zh'?'zh-CN':active?.dataset.panel==='en'?'en-US':'ru-RU'}}
speakButton.onclick=()=>{const reading=selectedReading();if(!reading.text)return;speechSynthesis.cancel();const utterance=new SpeechSynthesisUtterance(reading.text);utterance.lang=reading.lang;utterance.rate=Number(speechRate.value);const voices=speechSynthesis.getVoices(),voice=voices[Number(voiceSelect.value)];if(voice)utterance.voice=voice;utterance.onstart=()=>{pauseButton.disabled=false;stopButton.disabled=false};utterance.onend=utterance.onerror=()=>{pauseButton.disabled=true;stopButton.disabled=true;pauseButton.textContent='Пауза'};speechSynthesis.speak(utterance)};
pauseButton.onclick=()=>{if(speechSynthesis.paused){speechSynthesis.resume();pauseButton.textContent='Пауза'}else{speechSynthesis.pause();pauseButton.textContent='Продолжить'}};stopButton.onclick=()=>speechSynthesis.cancel();speechRate.oninput=()=>speechRateValue.value=`${speechRate.value}×`;
document.getElementById('wordAnnotation').onclick=()=>{const selection=getSelection(),text=selection?.toString().trim();if(!text||!editor.contains(selection.anchorNode))return alert('Выделите слово в русском тексте.');const pronunciation=prompt('Произношение, ударение или пиньинь:',text);if(pronunciation===null)return;const note=prompt('Краткое примечание или перевод:','')||'',safe=value=>value.replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));document.execCommand('insertHTML',false,`<ruby class="word-annotation"${note?` title="${safe(note)}"`:''}>${safe(text)}<rt>${safe(pronunciation)}</rt></ruby>`);editor.dispatchEvent(new Event('input'))};'''


def reader_page(item: dict) -> str:
    paragraphs = "".join(f"<p>{esc(p)}</p>" for p in item["ru_text"])
    battles = BATTLES.get(f"{item['id']}@{item['period']}", [])
    battle_rows = "".join(
        f'''<li><time>{esc(battle["date"])}</time><div><strong>{esc(battle["ru"])}</strong><small>{esc(battle["en"])} · {esc(battle["zh"])}</small><p>{esc(battle["note"])}</p></div></li>'''
        for battle in battles
    )
    battle_section = (
        f'''<section class="battle-section" contenteditable="false"><h2>Крупнейшие сражения</h2><ol>{battle_rows}</ol></section>'''
        if battle_rows else ""
    )
    storage = f"russian-wars-notes-{item['period']}-{item['id']}-v1"
    draft_storage = f"russian-wars-draft-{item['period']}-{item['id']}-v1"
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(item['ru'])} · Reader</title><link rel="stylesheet" href="../../../workspace_theme.css"><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f1f3f4;color:#202124;font-family:Arial,sans-serif}}header{{position:sticky;top:0;z-index:4;display:flex;gap:12px;align-items:center;padding:12px 18px;border-bottom:1px solid #dadce0;background:#fff}}header a{{color:#174ea6;text-decoration:none}}header strong{{flex:1}}.toolbar{{display:none;position:sticky;top:0;z-index:8;gap:8px;align-items:center;flex-wrap:wrap;padding:8px 14px;border-bottom:1px solid #c9d3e1;background:#e8f0fe;box-shadow:0 2px 7px #0002}}body.mobile-edit-mode .toolbar{{display:flex}}.toolbar-group,.toolbar-modes{{display:flex;gap:6px;align-items:center;flex-wrap:wrap}}.toolbar-modes{{padding-right:8px;border-right:1px solid #bdc9da}}.toolbar button,.toolbar select{{min-height:34px;padding:6px 10px;border:1px solid #bdc9da;border-radius:6px;background:#fff;color:#202124;cursor:pointer}}.toolbar button.active,.toolbar button.primary{{background:#d7e6fd;color:#174ea6;font-weight:700}}body.toolbar-simple .toolbar .full-only{{display:none}}.speech-rate{{display:flex;gap:6px;align-items:center;font-size:13px}}.speech-rate input{{width:92px}}ruby.word-annotation rt{{color:#174ea6;font:11px Arial}}main{{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(320px,.8fr);gap:14px;width:min(1440px,calc(100% - 28px));margin:16px auto 90px}}.paper,.study{{border:1px solid #dadce0;border-radius:10px;background:#fff}}.paper{{padding:clamp(22px,5vw,70px)}}h1{{margin:0 0 .2em;font:700 clamp(31px,5vw,55px)/1.1 Georgia,serif}}.meta{{color:#5f6368}}#editor{{font:clamp(18px,1.7vw,23px)/1.85 Georgia,serif}}#editor p{{margin:1em 0}}.battle-section{{margin-top:42px;padding-top:24px;border-top:2px solid #dadce0}}.battle-section h2{{font:700 27px/1.2 Georgia,serif}}.battle-section ol{{display:grid;gap:10px;padding:0;list-style:none}}.battle-section li{{display:grid;grid-template-columns:90px 1fr;gap:14px;padding:13px;border:1px solid #dadce0;border-radius:8px;background:#f8f9fa}}.battle-section time{{color:#174ea6;font-weight:700}}.battle-section strong,.battle-section small{{display:block}}.battle-section small{{margin-top:3px;color:#5f6368;font:13px/1.4 Arial,sans-serif}}.battle-section p{{margin:.5em 0 0!important;font:15px/1.55 Arial,sans-serif}}.study{{position:sticky;top:66px;align-self:start;overflow:hidden}}.tabs{{display:grid;grid-template-columns:repeat(3,1fr);border-bottom:1px solid #dadce0}}.tabs button{{padding:12px 6px;border:0;background:#f8f9fa;cursor:pointer}}.tabs button.active{{background:#e8f0fe;color:#174ea6;font-weight:700}}.support{{padding:18px;font-size:16px;line-height:1.7}}.support[hidden]{{display:none}}textarea{{width:100%;min-height:150px;padding:12px;border:1px solid #dadce0;border-radius:7px;font:15px/1.5 Arial}}.actions{{display:flex;gap:8px;margin-top:8px}}.actions button,.source{{padding:8px 11px;border:1px solid #dadce0;border-radius:17px;background:#fff;color:#174ea6;text-decoration:none;cursor:pointer}}@media(max-width:760px){{main{{display:block;width:100%;margin-top:0}}.paper,.study{{border-radius:0;border-inline:0}}.study{{position:static;margin-top:10px}}header strong{{font-size:13px}}.battle-section li{{grid-template-columns:1fr;gap:4px}}}}
</style></head><body><header><a href="../../../index.html#russian_wars">← Библиотека</a><strong>{esc(item['ru'])}</strong><a href="../../select_articles.html">Выбрать статьи</a></header>{editing_toolbar()}<main><article class="paper"><p class="meta">{esc(item['type'])} · {esc(item['year'])}</p><h1>{esc(item['ru'])}</h1><section id="editor" contenteditable="true">{paragraphs}</section>{battle_section}</article><aside class="study"><div class="tabs"><button class="active" data-tab="en">English</button><button data-tab="zh">中文</button><button data-tab="notes">Заметки</button></div><section class="support" data-panel="en"><h2>{esc(item['en_title'])}</h2><p>{esc(item['en'])}</p></section><section class="support" data-panel="zh" hidden lang="zh-CN"><h2>{esc(item['zh_title'])}</h2><p>{esc(item['zh'])}</p></section><section class="support" data-panel="notes" hidden><h2>Заметки / Notes</h2><textarea id="notes" placeholder="Запишите заметки к чтению…"></textarea><div class="actions"><button id="save">Сохранить</button><button id="export">Экспорт</button><a class="source" href="{esc(item['source'])}" target="_blank" rel="noreferrer">Источник ↗</a></div><p id="status"></p></section></aside></main><script>
const key={json.dumps(storage)},draftKey={json.dumps(draft_storage)},notes=document.getElementById('notes'),editor=document.getElementById('editor');notes.value=localStorage.getItem(key)||'';if(localStorage.getItem(draftKey))editor.innerHTML=localStorage.getItem(draftKey);document.querySelector('.tabs').onclick=e=>{{const tab=e.target.dataset.tab;if(!tab)return;document.querySelectorAll('[data-tab]').forEach(b=>b.classList.toggle('active',b.dataset.tab===tab));document.querySelectorAll('[data-panel]').forEach(p=>p.hidden=p.dataset.panel!==tab)}};document.getElementById('save').onclick=()=>{{localStorage.setItem(key,notes.value);document.getElementById('status').textContent='Сохранено · 已保存'}};document.getElementById('export').onclick=()=>{{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify({{article:{json.dumps(item['id'])},notes:notes.value}},null,2)],{{type:'application/json'}}));a.download={json.dumps(item['id'] + '_notes.json')};a.click()}};document.querySelector('.toolbar').onclick=e=>{{const command=e.target.closest('button')?.dataset.command;if(!command)return;if(command==='save'){{localStorage.setItem(draftKey,editor.innerHTML);return}};document.execCommand(command==='highlight'?'backColor':command,false,command==='highlight'?'#fff2a8':null);editor.focus()}};editor.addEventListener('input',()=>localStorage.setItem(draftKey,editor.innerHTML));{toolbar_script()}
</script><script src="../../../mobile_pwa.js"></script></body></html>'''


def battle_id(parent: dict, index: int) -> str:
    stem = parent["id"].removeprefix("02_").removeprefix("03_")
    return f"battle_{stem}_{index:02d}"


def battle_page(parent: dict, battle: dict, index: int) -> str:
    item_id = battle_id(parent, index)
    storage = f"russian-wars-notes-{parent['period']}-{item_id}-v1"
    draft_storage = f"russian-wars-draft-{parent['period']}-{item_id}-v1"
    support_en, support_zh = BATTLE_SUPPORT[battle["ru"]]
    search_ru = "https://ru.wikipedia.org/w/index.php?search=" + quote(battle["ru"])
    search_en = "https://en.wikipedia.org/w/index.php?search=" + quote(battle["en"])
    search_zh = "https://zh.wikipedia.org/w/index.php?search=" + quote(battle["zh"])
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(battle['ru'])} · Reader</title><link rel="stylesheet" href="../../../workspace_theme.css"><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f1f3f4;color:#202124;font-family:Arial,sans-serif}}header{{display:flex;gap:12px;align-items:center;padding:12px 18px;border-bottom:1px solid #dadce0;background:#fff}}header a{{color:#174ea6;text-decoration:none}}header strong{{flex:1}}.toolbar{{display:none;position:sticky;top:0;z-index:8;gap:8px;align-items:center;flex-wrap:wrap;padding:8px 14px;border-bottom:1px solid #c9d3e1;background:#e8f0fe;box-shadow:0 2px 7px #0002}}body.mobile-edit-mode .toolbar{{display:flex}}.toolbar-group,.toolbar-modes{{display:flex;gap:6px;align-items:center;flex-wrap:wrap}}.toolbar-modes{{padding-right:8px;border-right:1px solid #bdc9da}}.toolbar button,.toolbar select{{min-height:34px;margin:0;padding:6px 10px;border:1px solid #bdc9da;border-radius:6px;background:#fff;color:#202124;cursor:pointer}}.toolbar button.active,.toolbar button.primary{{background:#d7e6fd;color:#174ea6;font-weight:700}}body.toolbar-simple .toolbar .full-only{{display:none}}.speech-rate{{display:flex;gap:6px;align-items:center;font-size:13px}}.speech-rate input{{width:92px}}ruby.word-annotation rt{{color:#174ea6;font:11px Arial}}main{{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(320px,.72fr);gap:14px;width:min(1350px,calc(100% - 28px));margin:16px auto 80px}}article,.study{{border:1px solid #dadce0;border-radius:10px;background:#fff}}article{{padding:clamp(22px,5vw,60px)}}.study{{align-self:start;overflow:hidden}}h1{{margin:.2em 0;font:700 clamp(34px,5vw,56px)/1.1 Georgia,serif}}.meta{{color:#5f6368}}.description{{font:clamp(18px,1.8vw,24px)/1.8 Georgia,serif}}.tabs{{display:grid;grid-template-columns:repeat(3,1fr);border-bottom:1px solid #dadce0}}.tabs button{{margin:0;padding:12px 5px;border:0;border-radius:0;background:#f8f9fa}}.tabs button.active{{background:#e8f0fe;color:#174ea6;font-weight:700}}.panel{{padding:22px;font-size:16px;line-height:1.7}}.panel[hidden]{{display:none}}.panel h2{{margin-top:0}}.references{{display:flex;gap:7px;flex-wrap:wrap;margin-top:20px;padding-top:15px;border-top:1px solid #dadce0}}textarea{{width:100%;min-height:190px;padding:11px;border:1px solid #dadce0;border-radius:7px;font:15px/1.5 Arial}}button,.source{{display:inline-block;margin-top:8px;padding:8px 11px;border:1px solid #dadce0;border-radius:17px;background:#fff;color:#174ea6;text-decoration:none;cursor:pointer}}@media(max-width:720px){{main{{display:block;width:100%;margin-top:0}}article,.study{{border-radius:0;border-inline:0}}.study{{margin-top:10px}}}}
</style></head><body><header><a href="../../../index.html#russian_wars">← Библиотека</a><strong>{esc(parent['ru'])}</strong><a href="../../select_articles.html">Выбрать статьи</a></header>{editing_toolbar()}<main><article><p class="meta">Сражение · {esc(battle['date'])} · {esc(parent['ru'])}</p><section id="editor" contenteditable="true"><h1>{esc(battle['ru'])}</h1><p class="description">{esc(battle['note'])}</p></section></article><aside class="study"><div class="tabs"><button class="active" data-tab="en">English</button><button data-tab="zh">中文</button><button data-tab="notes">Заметки</button></div><section class="panel" data-panel="en"><h2>{esc(battle['en'])}</h2><p>{esc(support_en)}</p><div class="references"><a class="source" href="{esc(parent['source'])}" target="_blank" rel="noreferrer">Основной источник ↗</a><a class="source" href="{esc(search_en)}" target="_blank" rel="noreferrer">English links ↗</a></div></section><section class="panel" data-panel="zh" hidden lang="zh-CN"><h2>{esc(battle['zh'])}</h2><p>{esc(support_zh)}</p><div class="references"><a class="source" href="{esc(search_zh)}" target="_blank" rel="noreferrer">中文资料 ↗</a></div></section><section class="panel" data-panel="notes" hidden><h2>Заметки</h2><textarea id="notes" placeholder="Запишите заметки к чтению…"></textarea><button id="save">Сохранить</button><div class="references"><a class="source" href="{esc(parent['source'])}" target="_blank" rel="noreferrer">Основной источник ↗</a><a class="source" href="{esc(search_ru)}" target="_blank" rel="noreferrer">Русские ссылки ↗</a><a class="source" href="{esc(search_en)}" target="_blank" rel="noreferrer">English links ↗</a><a class="source" href="{esc(search_zh)}" target="_blank" rel="noreferrer">中文资料 ↗</a></div><p id="status"></p></section></aside></main><script>
const key={json.dumps(storage)},draftKey={json.dumps(draft_storage)},notes=document.getElementById('notes'),editor=document.getElementById('editor');notes.value=localStorage.getItem(key)||'';if(localStorage.getItem(draftKey))editor.innerHTML=localStorage.getItem(draftKey);document.querySelector('.tabs').onclick=e=>{{const tab=e.target.dataset.tab;if(!tab)return;document.querySelectorAll('[data-tab]').forEach(button=>button.classList.toggle('active',button.dataset.tab===tab));document.querySelectorAll('[data-panel]').forEach(panel=>panel.hidden=panel.dataset.panel!==tab)}};document.getElementById('save').onclick=()=>{{localStorage.setItem(key,notes.value);document.getElementById('status').textContent='Сохранено'}};document.querySelector('.toolbar').onclick=e=>{{const command=e.target.closest('button')?.dataset.command;if(!command)return;if(command==='save'){{localStorage.setItem(draftKey,editor.innerHTML);return}};document.execCommand(command==='highlight'?'backColor':command,false,command==='highlight'?'#fff2a8':null);editor.focus()}};editor.addEventListener('input',()=>localStorage.setItem(draftKey,editor.innerHTML));{toolbar_script()}
</script><script src="../../../mobile_pwa.js"></script></body></html>'''


def selector_page() -> str:
    data = json.dumps([{k: v for k, v in item.items() if k not in {"ru_text", "en", "zh"}} for item in ARTICLES], ensure_ascii=False)
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Войны России · выбор статей</title><style>*{{box-sizing:border-box}}body{{margin:0;background:#eef1f5;color:#202124;font-family:Arial,sans-serif}}header{{padding:32px max(20px,5vw);background:#253c5a;color:#fff}}header a{{color:#fff}}h1{{margin:.2em 0;font:700 clamp(34px,6vw,62px)/1.05 Georgia,serif}}main{{width:min(1120px,calc(100% - 28px));margin:18px auto 80px}}.controls,.summary{{position:sticky;top:0;z-index:2;display:flex;gap:9px;padding:12px;border:1px solid #dadce0;background:#ffffffed;backdrop-filter:blur(8px)}}input,select,button{{min-height:40px;padding:8px 10px;border:1px solid #cbd1d8;border-radius:6px;background:#fff;font:inherit}}#search{{flex:1}}button{{cursor:pointer}}button.primary{{background:#188038;color:#fff;border-color:#188038}}.summary{{position:static;justify-content:space-between;align-items:center;margin-top:10px}}.period{{margin-top:16px;border:1px solid #dadce0;background:#fff}}.period h2{{margin:0;padding:14px;background:#f4f6f8}}.row{{display:grid;grid-template-columns:34px minmax(0,1fr) auto;gap:12px;align-items:center;padding:13px;border-top:1px solid #e5e8eb}}.row label{{display:flex;gap:10px;align-items:start}}.row small{{display:block;margin-top:4px;color:#5f6368}}.badges{{display:flex;gap:5px;margin-top:6px}}.badges i{{padding:3px 7px;border-radius:10px;background:#e8f0fe;color:#174ea6;font-size:10px;font-style:normal}}.links{{display:flex;gap:7px}}.links a{{padding:7px 9px;border:1px solid #cbd1d8;border-radius:15px;color:#174ea6;text-decoration:none;font-size:12px}}@media(max-width:650px){{.controls,.summary{{align-items:stretch;flex-direction:column}}.row{{grid-template-columns:28px 1fr}}.links{{grid-column:2}}}}</style></head><body><header><a href="../index.html#russian_wars">← Reader library</a><h1>Войны России</h1><p>Выберите статьи для подробного чтения, языковой поддержки и заметок.</p></header><main><div class="controls"><input id="search" type="search" placeholder="Поиск по-русски, English или中文"><select id="type"><option value="">Все типы</option><option>Введение</option><option>Война</option><option>Итоги периода</option></select><button id="visible">Выбрать результаты</button></div><section class="summary"><strong id="count"></strong><span><button id="remove">Очистить</button> <button class="primary" id="import">Импортировать в библиотеку</button></span></section><section class="period"><h2>Период 6 · 1801–1855</h2><div id="rows"></div></section></main><script>
const articles={data},draft=new Set(JSON.parse(localStorage.getItem('russian-wars-selection-draft')||'[]')),rows=document.getElementById('rows');function filtered(){{const q=document.getElementById('search').value.trim().toLocaleLowerCase(),t=document.getElementById('type').value;return articles.filter(x=>(!t||x.type===t)&&(!q||`${{x.ru}} ${{x.en_title}} ${{x.zh_title}} ${{x.year}}`.toLocaleLowerCase().includes(q)))}}function save(){{localStorage.setItem('russian-wars-selection-draft',JSON.stringify([...draft]));document.getElementById('count').textContent=`Выбрано: ${{draft.size}} · 约 ${{Math.max(1,draft.size*12)}} KB`}}function render(){{rows.innerHTML=filtered().map((x,i)=>`<article class="row"><span>${{String(i+1).padStart(2,'0')}}</span><label><input type="checkbox" data-id="${{x.id}}" ${{draft.has(x.id)?'checked':''}}><span><b>${{x.ru}}</b><small>${{x.en_title}} · ${{x.zh_title}}</small><span class="badges"><i>${{x.type}}</i><i>RU</i><i>EN</i><i>中文</i></span></span></label><span class="links"><a href="${{x.source}}" target="_blank" rel="noreferrer">Источник</a><a href="{PERIOD}/${{x.id}}/editor.html?view=annotated">Читать</a></span></article>`).join('');save()}}rows.onchange=e=>{{if(!e.target.dataset.id)return;e.target.checked?draft.add(e.target.dataset.id):draft.delete(e.target.dataset.id);save()}};document.getElementById('search').oninput=render;document.getElementById('type').onchange=render;document.getElementById('visible').onclick=()=>{{const ids=filtered().map(x=>x.id),all=ids.every(id=>draft.has(id));ids.forEach(id=>all?draft.delete(id):draft.add(id));render()}};document.getElementById('remove').onclick=()=>{{draft.clear();render()}};document.getElementById('import').onclick=()=>{{localStorage.setItem('russian-wars-library-ids',JSON.stringify([...draft]));location.href='../index.html#russian_wars'}};render();
</script></body></html>'''


def selector_page_v2() -> str:
    catalog = [
        {k: v for k, v in item.items() if k not in {"ru_text", "en", "zh"}}
        for item in ARTICLES
    ]
    data = json.dumps(catalog, ensure_ascii=False).replace("</", "<\\/")
    period_options = "".join(
        f'<option value="{esc(key)}">{esc(label)}</option>'
        for key, label in PERIODS.items()
    )
    return f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Войны России · выбор статей</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#eef1f5;color:#202124;font-family:Arial,sans-serif}}header{{padding:32px max(20px,5vw);background:#253c5a;color:#fff}}header a{{color:#fff}}h1{{margin:.2em 0;font:700 clamp(34px,6vw,62px)/1.05 Georgia,serif}}main{{width:min(1120px,calc(100% - 28px));margin:18px auto 80px}}.controls,.summary{{display:flex;gap:9px;padding:12px;border:1px solid #dadce0;background:#ffffffed}}.controls{{position:sticky;top:0;z-index:2;backdrop-filter:blur(8px)}}input,select,button{{min-height:40px;padding:8px 10px;border:1px solid #cbd1d8;border-radius:6px;background:#fff;font:inherit}}#search{{min-width:180px;flex:1}}button{{cursor:pointer}}button.primary{{background:#188038;color:#fff;border-color:#188038}}.summary{{justify-content:space-between;align-items:center;margin-top:10px}}.period{{margin-top:16px;border:1px solid #dadce0;background:#fff}}.period h2{{margin:0;padding:14px;background:#f4f6f8;font-size:19px}}.row{{display:grid;grid-template-columns:34px minmax(0,1fr) auto;gap:12px;align-items:center;padding:13px;border-top:1px solid #e5e8eb}}.row label{{display:flex;gap:10px;align-items:start}}.row small{{display:block;margin-top:4px;color:#5f6368}}.badges,.links{{display:flex;gap:5px;flex-wrap:wrap}}.badges{{margin-top:6px}}.badges i{{padding:3px 7px;border-radius:10px;background:#e8f0fe;color:#174ea6;font-size:10px;font-style:normal}}.links a{{padding:7px 9px;border:1px solid #cbd1d8;border-radius:15px;color:#174ea6;text-decoration:none;font-size:12px}}.battle-list{{grid-column:2/-1;width:100%;margin-top:2px;padding:9px 12px;border:1px solid #d7dee8;border-radius:7px;background:#f8faff}}.battle-list summary{{cursor:pointer;color:#174ea6;font-weight:700}}.battle-list ol{{display:grid;gap:7px;margin:10px 0 2px;padding-left:22px}}.battle-list li{{padding-left:5px}}.battle-list time{{display:inline-block;min-width:82px;color:#5f6368;font-size:12px}}.battle-list p{{margin:3px 0;color:#5f6368;font-size:12px;line-height:1.45}}.empty{{padding:28px;text-align:center;color:#5f6368}}@media(max-width:720px){{.controls,.summary{{align-items:stretch;flex-direction:column}}.row{{grid-template-columns:28px 1fr}}.links,.battle-list{{grid-column:2}}}}
</style></head><body>
<header><a href="../index.html#russian_wars">← Библиотека</a><h1>Войны России</h1><p>Выберите статьи для подробного чтения и заметок.</p></header>
<main><div class="controls"><input id="search" type="search" placeholder="Поиск по названию, дате или периоду"><select id="period"><option value="">Все периоды</option>{period_options}</select><select id="type"><option value="">Все типы</option><option>Введение</option><option>Война</option><option>Итоги периода</option></select><button id="visible">Выбрать результаты</button></div><section class="summary"><strong id="count"></strong><span><button id="remove">Очистить</button> <button class="primary" id="import">Импортировать в библиотеку</button></span></section><div id="catalog"></div></main>
<script>
const articles={data};
const periods={json.dumps(PERIODS, ensure_ascii=False)};
const battles={json.dumps(BATTLES, ensure_ascii=False)};
const savedDraft=localStorage.getItem('russian-wars-selection-draft');
const savedLibrary=localStorage.getItem('russian-wars-library-ids');
const initial=savedDraft||savedLibrary||JSON.stringify(articles.map(x=>x.id+'@'+x.period));
const storedIds=JSON.parse(initial).map(key=>key.includes('@')?key:key+'@period_06_1801_1855');
const draft=new Set(storedIds);
const articleKey=x=>x.id+'@'+x.period;
const battleItemId=(x,index)=>'battle_'+x.id.replace(/^0[23]_/, '')+'_'+String(index+1).padStart(2,'0');
const battleKey=(x,index)=>battleItemId(x,index)+'@'+x.period;
const catalog=document.getElementById('catalog');
function filtered(){{const q=document.getElementById('search').value.trim().toLocaleLowerCase(),p=document.getElementById('period').value,t=document.getElementById('type').value;return articles.filter(x=>(!p||x.period===p)&&(!t||x.type===t)&&(!q||`${{x.ru}} ${{x.en_title}} ${{x.zh_title}} ${{x.year}}`.toLocaleLowerCase().includes(q)))}}
function save(){{localStorage.setItem('russian-wars-selection-draft',JSON.stringify([...draft]));document.getElementById('count').textContent=`Выбрано: ${{draft.size}} · около ${{Math.max(1,draft.size*12)}} КБ`}}
function battleMarkup(x){{const list=battles[articleKey(x)]||[];if(!list.length)return'';return `<details class="battle-list"><summary>Крупнейшие сражения · ${{list.length}}</summary><ol>${{list.map((b,index)=>`<li><label><input type="checkbox" data-key="${{battleKey(x,index)}}" ${{draft.has(battleKey(x,index))?'checked':''}}><span><time>${{b.date}}</time><strong>${{b.ru}}</strong><p>${{b.note}}</p><span class="links"><a href="${{x.source}}" target="_blank" rel="noreferrer">Источник</a><a href="${{x.period}}/${{battleItemId(x,index)}}/editor.html?view=annotated">Читать</a></span></span></label></li>`).join('')}}</ol></details>`}}
function render(){{const visible=filtered();catalog.innerHTML=Object.entries(periods).map(([key,label])=>{{const rows=visible.filter(x=>x.period===key);if(!rows.length)return'';return `<section class="period"><h2>${{label}} · ${{rows.length}} статей</h2>${{rows.map((x,i)=>`<article class="row"><span>${{String(i+1).padStart(2,'0')}}</span><label><input type="checkbox" data-key="${{articleKey(x)}}" ${{draft.has(articleKey(x))?'checked':''}}><span><b>${{x.ru}}</b><span class="badges"><i>${{x.type}}</i><i>${{x.year}}</i></span></span></label><span class="links"><a href="${{x.source}}" target="_blank" rel="noreferrer">Источник</a><a href="${{x.period}}/${{x.id}}/editor.html?view=annotated">Читать</a></span>${{battleMarkup(x)}}</article>`).join('')}}</section>`}}).join('')||'<p class="empty">Нет подходящих статей.</p>';save()}}
catalog.onchange=e=>{{if(!e.target.dataset.key)return;e.target.checked?draft.add(e.target.dataset.key):draft.delete(e.target.dataset.key);save()}};
document.getElementById('search').oninput=render;document.getElementById('period').onchange=render;document.getElementById('type').onchange=render;
document.getElementById('visible').onclick=()=>{{const keys=filtered().map(articleKey),all=keys.every(key=>draft.has(key));keys.forEach(key=>all?draft.delete(key):draft.add(key));render()}};
document.getElementById('remove').onclick=()=>{{draft.clear();render()}};
document.getElementById('import').onclick=()=>{{localStorage.setItem('russian-wars-library-ids',JSON.stringify([...draft]));location.href='../index.html#russian_wars'}};
render();
</script></body></html>'''


def main() -> None:
    for item in ARTICLES:
        folder = BASE / item["period"] / item["id"]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "editor.html").write_text(reader_page(item).replace("Выбрать статьи", "Select articles"), encoding="utf-8")
        for index, battle in enumerate(BATTLES.get(f"{item['id']}@{item['period']}", []), 1):
            battle_folder = BASE / item["period"] / battle_id(item, index)
            battle_folder.mkdir(parents=True, exist_ok=True)
            (battle_folder / "editor.html").write_text(battle_page(item, battle, index).replace("Выбрать статьи", "Select articles"), encoding="utf-8")
    catalog = {"articles": ARTICLES, "battles": BATTLES}
    (BASE / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    (BASE / "select_articles.html").write_text(selector_page_v2(), encoding="utf-8")
    print(f"Built {len(ARTICLES)} Russian-wars prototype articles")


if __name__ == "__main__":
    main()
