#!/usr/bin/env python3
"""Build the initial Russian-first poetry sampler for the Reader app."""

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


RUVERSes_AUTHORS = {
    "Александр Пушкин": "alexander-pushkin",
    "Михаил Лермонтов": "mikhail-lermontov",
    "Фёдор Тютчев": "fyodor-tyutchev",
    "Афанасий Фет": "afanasy-fet",
    "Иван Крылов": "ivan-krylov",
    "Иван Тургенев": "ivan-turgenev",
    "Александр Блок": "alexander-blok",
    "Сергей Есенин": "sergey-esenin",
    "Гавриил Державин": "gavrila-derzhavin",
    "Константин Батюшков": "konstantin-batyushkov",
    "Николай Некрасов": "nikolay-nekrasov",
    "Владимир Маяковский": "vladimir-mayakovsky",
}

# Direct poem pages verified on RuVerses. Other entries deliberately fall back
# to the author's catalog instead of constructing an unverified URL.
RUVERSes_POEMS = {
    "01_pushkin_ya_vas_lyubil": "i-loved-you",
    "02_pushkin_zimnee_utro": "winter-morning",
    "03_pushkin_uznik": "captive",
    "04_lermontov_parus": "sail",
    "05_tyutchev_silentium": "silentium",
    "06_pushkin_esli_zhizn_tebya_obmanet": "if-by-life-you-were-deceived",
    "07_pushkin_k_chaadaevu": "to-chaadaev",
    "08_lermontov_vykhozhu_odin": "i-come-out-to-the-path-alone",
    "14_blok_noch_ulitsa": "night-street-lamp-drugstore",
    "20_mayakovsky_poslushayte": "listen",
}


POEMS = [
    {
        "slug": "01_pushkin_ya_vas_lyubil",
        "title": "Я вас любил",
        "author": "Александр Пушкин",
        "year": "1829",
        "source": "https://ru.wikisource.org/wiki/Я_вас_любил:_любовь_ещё,_быть_может_(Пушкин)",
        "lines": [
            "Я вас любил: любовь ещё, быть может,", "В душе моей угасла не совсем;",
            "Но пусть она вас больше не тревожит;", "Я не хочу печалить вас ничем.",
            "Я вас любил безмолвно, безнадежно,", "То робостью, то ревностью томим;",
            "Я вас любил так искренно, так нежно,", "Как дай вам Бог любимой быть другим.",
        ],
        "guide": "A compact lyric of renunciation. Notice how the repeated Я вас любил changes from confession to a wish for the beloved's future happiness.",
        "vocab": [("угасла", "faded; went out"), ("тревожит", "troubles"), ("безмолвно", "silently"), ("томим", "tormented"), ("нежно", "tenderly")],
    },
    {
        "slug": "02_pushkin_zimnee_utro",
        "title": "Зимнее утро",
        "author": "Александр Пушкин",
        "year": "1829",
        "source": "https://ru.wikisource.org/wiki/Зимнее_утро_(Пушкин)",
        "lines": [
            "Мороз и солнце; день чудесный!", "Еще ты дремлешь, друг прелестный —", "Пора, красавица, проснись:",
            "Открой сомкнуты негой взоры", "Навстречу северной Авроры,", "Звездою севера явись!", "",
            "Вечор, ты помнишь, вьюга злилась,", "На мутном небе мгла носилась;", "Луна, как бледное пятно,",
            "Сквозь тучи мрачные желтела,", "И ты печальная сидела —", "А нынче… погляди в окно:", "",
            "Под голубыми небесами", "Великолепными коврами,", "Блестя на солнце, снег лежит;",
            "Прозрачный лес один чернеет,", "И ель сквозь иней зеленеет,", "И речка подо льдом блестит.", "",
            "Вся комната янтарным блеском", "Озарена. Веселым треском", "Трещит затопленная печь.",
            "Приятно думать у лежанки.", "Но знаешь: не велеть ли в санки", "Кобылку бурую запречь?", "",
            "Скользя по утреннему снегу,", "Друг милый, предадимся бегу", "Нетерпеливого коня",
            "И навестим поля пустые,", "Леса, недавно столь густые,", "И берег, милый для меня.",
        ],
        "guide": "Read the poem as a movement from yesterday's storm to today's light, then from the warm room into motion outdoors. The old-fashioned words are useful evidence of poetic register.",
        "vocab": [("дремлешь", "you are dozing"), ("вьюга", "snowstorm"), ("мгла", "gloom; haze"), ("иней", "frost"), ("сани", "sleigh"), ("запречь", "to harness")],
    },
    {
        "slug": "03_pushkin_uznik",
        "title": "Узник",
        "author": "Александр Пушкин",
        "year": "1822",
        "source": "https://ru.wikisource.org/wiki/Узник_(Пушкин)",
        "lines": [
            "Сижу за решёткой в темнице сырой.", "Вскормленный в неволе орёл молодой,",
            "Мой грустный товарищ, махая крылом,", "Кровавую пищу клюёт под окном,", "",
            "Клюёт, и бросает, и смотрит в окно,", "Как будто со мною задумал одно.",
            "Зовёт меня взглядом и криком своим", "И вымолвить хочет: «Давай, улетим!", "",
            "Мы вольные птицы; пора, брат, пора!", "Туда, где за тучей белеет гора,",
            "Туда, где синеют морские края,", "Туда, где гуляем лишь ветер… да я!…»",
        ],
        "guide": "The prisoner's eagle becomes a double and an imagined companion. Track the shift from enclosed nouns to the repeated directional word туда and open landscape.",
        "vocab": [("решётка", "bars; grille"), ("темница", "dungeon"), ("неволя", "captivity"), ("клюёт", "pecks"), ("вольные", "free")],
    },
    {
        "slug": "04_lermontov_parus",
        "title": "Парус",
        "author": "Михаил Лермонтов",
        "year": "1832",
        "source": "https://ru.wikisource.org/wiki/Парус_(Лермонтов)",
        "lines": [
            "Белеет парус одинокой", "В тумане моря голубом!..", "Что ищет он в стране далекой?", "Что кинул он в краю родном?..", "",
            "Играют волны — ветер свищет,", "И мачта гнется и скрыпит...", "Увы! он счастия не ищет,", "И не от счастия бежит!", "",
            "Под ним струя светлей лазури,", "Над ним луч солнца золотой...", "А он, мятежный, просит бури,", "Как будто в бурях есть покой!",
        ],
        "guide": "The sail is both a visible object and a figure for restless consciousness. Each stanza balances an outer scene with questions or paradox.",
        "vocab": [("парус", "sail"), ("мачта", "mast"), ("лазурь", "azure"), ("мятежный", "rebellious; restless"), ("буря", "storm")],
    },
    {
        "slug": "05_tyutchev_silentium",
        "title": "Silentium!",
        "author": "Фёдор Тютчев",
        "year": "1830",
        "source": "https://ru.wikisource.org/wiki/Silentium!_(Тютчев)/ПСС_1987_(СО)",
        "lines": [
            "Молчи, скрывайся и таи", "И чувства и мечты свои —", "Пускай в душевной глубине", "Встают и заходят оне",
            "Безмолвно, как звезды в ночи, —", "Любуйся ими — и молчи.", "",
            "Как сердцу высказать себя?", "Другому как понять тебя?", "Поймёт ли он, чем ты живёшь?", "Мысль изреченная есть ложь.",
            "Взрывая, возмутишь ключи, —", "Питайся ими — и молчи.", "",
            "Лишь жить в себе самом умей —", "Есть целый мир в душе твоей", "Таинственно-волшебных дум;", "Их оглушит наружный шум,",
            "Дневные разгонят лучи, —", "Внимай их пенью — и молчи!..",
        ],
        "guide": "Three six-line stanzas turn silence into an argument about inward life and the limits of language. Pay special attention to imperatives and rhetorical questions.",
        "vocab": [("таи", "conceal"), ("душевный", "of the soul; inner"), ("изреченная", "uttered"), ("ключи", "springs; sources"), ("внимай", "heed; listen closely")],
    },
]

POEMS += [
    {
        "slug": "06_pushkin_esli_zhizn_tebya_obmanet", "title": "Если жизнь тебя обманет", "author": "Александр Пушкин", "year": "1825",
        "source": "https://ru.wikisource.org/wiki/Если_жизнь_тебя_обманет_(Пушкин)",
        "lines": ["Если жизнь тебя обманет,", "Не печалься, не сердись!", "В день уныния смирись:", "День веселья, верь, настанет.", "", "Сердце в будущем живет;", "Настоящее уныло:", "Все мгновенно, все пройдет;", "Что пройдет, то будет мило."],
        "guide": "An album poem built from imperatives and balanced opposites: sorrow and joy, present and future. Its simple syntax makes it an approachable first poem to memorize.",
        "vocab": [("обманет", "deceives"), ("печалься", "be sad"), ("уныние", "despondency"), ("смирись", "be reconciled; accept"), ("мгновенно", "momentary")],
    },
    {
        "slug": "07_pushkin_k_chaadaevu", "title": "К Чаадаеву", "author": "Александр Пушкин", "year": "1818",
        "source": "https://ru.wikisource.org/wiki/К_Чедаеву_(Пушкин)",
        "lines": ["Любви, надежды, тихой славы", "Недолго нежил нас обман,", "Исчезли юные забавы,", "Как сон, как утренний туман;", "Но в нас горит еще желанье,", "Под гнетом власти роковой", "Нетерпеливою душой", "Отчизны внемлем призыванье.", "", "Мы ждем с томленьем упованья", "Минуты вольности святой,", "Как ждет любовник молодой", "Минуты верного свиданья.", "Пока свободою горим,", "Пока сердца для чести живы,", "Мой друг, отчизне посвятим", "Души прекрасные порывы!", "", "Товарищ, верь: взойдет она,", "Звезда пленительного счастья,", "Россия вспрянет ото сна,", "И на обломках самовластья", "Напишут наши имена!"],
        "guide": "A civic epistle addressed to a friend. Follow the movement from lost youthful illusions to a shared promise of freedom and public action.",
        "vocab": [("гнет", "oppression; yoke"), ("отчизна", "fatherland"), ("упованье", "hope; trust"), ("вольность", "liberty"), ("самовластье", "autocracy")],
    },
    {
        "slug": "08_lermontov_vykhozhu_odin", "title": "Выхожу один я на дорогу", "author": "Михаил Лермонтов", "year": "1841",
        "source": "https://ru.wikisource.org/wiki/Выхожу_один_я_на_дорогу_(Лермонтов)/ПСС_1936_(СО)",
        "lines": ["Выхожу один я на дорогу;", "Сквозь туман кремнистый путь блестит;", "Ночь тиха. Пустыня внемлет богу,", "И звезда с звездою говорит.", "", "В небесах торжественно и чудно!", "Спит земля в сияньи голубом...", "Что же мне так больно и так трудно?", "Жду ль чего? жалею ли о чем?", "", "Уж не жду от жизни ничего я,", "И не жаль мне прошлого ничуть;", "Я ищу свободы и покоя!", "Я б хотел забыться и заснуть! —", "", "Но не тем холодным сном могилы....", "Я б желал навеки так заснуть,", "Чтоб в груди дремали жизни силы,", "Чтоб дыша вздымалась тихо грудь;", "", "Чтоб всю ночь, весь день мой слух лелея,", "Про любовь мне сладкий голос пел,", "Надо мной чтоб вечно зеленея", "Темный дуб склонялся и шумел."],
        "guide": "A meditative night walk whose cosmic calm contrasts with the speaker's pain. The final stanzas redefine the desired sleep as living peace rather than death.",
        "vocab": [("кремнистый", "flinty; stony"), ("внемлет", "heeds; listens"), ("сиянье", "radiance"), ("могила", "grave"), ("лелея", "caressing; cherishing")],
    },
    {
        "slug": "09_tyutchev_vesennie_vody", "title": "Весенние воды", "author": "Фёдор Тютчев", "year": "1829",
        "source": "https://ru.wikisource.org/wiki/Весенние_воды_(Тютчев)",
        "lines": ["Ещё в полях белеет снег,", "А воды уж весной шумят —", "Бегут и будят сонный брег,", "Бегут и блещут и гласят...", "", "Они гласят во все концы:", "«Весна идёт, весна идёт!", "Мы молодой весны гонцы,", "Она нас выслала вперёд!", "", "Весна идёт, весна идёт!", "И тихих, тёплых майских дней", "Румяный, светлый хоровод", "Толпится весело за ней!..»"],
        "guide": "Nature becomes a speaking procession. Repetition, rushing verbs, and personification make the thaw sound like news arriving before spring itself.",
        "vocab": [("брег", "shore; poetic form of берег"), ("блещут", "gleam"), ("гласят", "proclaim"), ("гонцы", "messengers"), ("хоровод", "round dance")],
    },
    {
        "slug": "10_fet_ya_prishyol_s_privetom", "title": "Я пришёл к тебе с приветом", "author": "Афанасий Фет", "year": "1843",
        "source": "https://ru.wikisource.org/wiki/Я_пришёл_к_тебе_с_приветом_(Фет)",
        "lines": ["Я пришёл к тебе с приветом,", "Рассказать, что солнце встало,", "Что оно горячим светом", "По листам затрепетало;", "", "Рассказать, что лес проснулся,", "Весь проснулся, веткой каждой,", "Каждой птицей встрепенулся", "И весенней полон жаждой;", "", "Рассказать, что с той же страстью,", "Как вчера, пришёл я снова,", "Что душа всё так же счастью", "И тебе служить готова;", "", "Рассказать, что отовсюду", "На меня весельем веет,", "Что не знаю сам, что́ буду", "Петь — но только песня зреет."],
        "guide": "One long grammatical surge connects sunrise, awakening nature, love, and the birth of song. Read it aloud without treating each stanza as a full stop.",
        "vocab": [("привет", "greeting"), ("затрепетало", "began to tremble"), ("встрепенулся", "stirred awake"), ("отовсюду", "from everywhere"), ("зреет", "ripens")],
    },
    {
        "slug": "11_fet_shepot", "title": "Шёпот, робкое дыханье", "author": "Афанасий Фет", "year": "1850",
        "source": "https://ru.wikisource.org/wiki/Шёпот,_робкое_дыханье_(Фет)",
        "lines": ["Шёпот, робкое дыханье,", "Трели соловья,", "Серебро и колыханье", "Сонного ручья,", "", "Свет ночной, ночные тени,", "Тени без конца,", "Ряд волшебных изменений", "Милого лица,", "", "В дымных тучках пурпур розы,", "Отблеск янтаря,", "И лобзания, и слезы,", "И заря, заря!.."],
        "guide": "A celebrated verbless lyric: nouns and sensory fragments accumulate into a complete nocturnal scene. Observe how sound, light, and emotion replace narrative action.",
        "vocab": [("шёпот", "whisper"), ("робкое", "timid"), ("трели", "trills"), ("колыханье", "swaying; rippling"), ("лобзания", "kisses; poetic")],
    },
    {
        "slug": "12_krylov_strekoza_i_muravey", "title": "Стрекоза и Муравей", "author": "Иван Крылов", "year": "1808",
        "source": "https://ru.wikisource.org/wiki/Стрекоза_и_Муравей_(Крылов)",
        "lines": ["Попрыгунья Стрекоза", "Лето красное пропела;", "Оглянуться не успела,", "Как зима катит в глаза.", "Помертвело чисто поле;", "Нет уж дней тех светлых боле,", "Как под каждым ей листком", "Был готов и стол, и дом.", "", "Все прошло: с зимой холодной", "Нужда, голод настает;", "Стрекоза уж не поет:", "И кому же в ум пойдет", "На желудок петь голодный!", "Злой тоской удручена,", "К Муравью ползет она:", "", "«Не оставь меня, кум милый!", "Дай ты мне собраться с силой", "И до вешних только дней", "Прокорми и обогрей!» —", "", "«Кумушка, мне странно это:", "Да работала ль ты в лето?» —", "Говорит ей Муравей.", "", "«До того ль, голубчик, было?", "В мягких муравах у нас", "Песни, резвость всякий час,", "Так, что голову вскружило». —", "", "«А, так ты...» — «Я без души", "Лето целое всё пела». —", "«Ты всё пела? это дело:", "Так поди же, попляши!»"],
        "guide": "A dramatic fable driven by colloquial dialogue and a sharp final retort. Compare the narrator's playful rhythm with the severity of the ant's judgment.",
        "vocab": [("попрыгунья", "frisky jumper"), ("нужда", "privation; need"), ("удручена", "dejected"), ("вешний", "vernal; springtime"), ("прокорми", "feed and sustain")],
    },
    {
        "slug": "13_turgenev_russkiy_yazyk", "title": "Русский язык", "author": "Иван Тургенев", "year": "1882",
        "source": "https://ru.wikisource.org/wiki/Русский_язык_(Тургенев)",
        "lines": ["Во дни сомнений, во дни тягостных раздумий о судьбах моей родины, — ты один мне поддержка и опора, о великий, могучий, правдивый и свободный русский язык!", "", "Не будь тебя — как не впасть в отчаяние при виде всего, что совершается дома?", "", "Но нельзя верить, чтобы такой язык не был дан великому народу!"],
        "guide": "A prose poem in three rhetorical movements: distress, a question at the edge of despair, and confidence grounded in language. Notice the direct address to Russian itself.",
        "vocab": [("тягостный", "oppressive; painful"), ("раздумья", "reflections"), ("судьба", "fate"), ("опора", "support"), ("отчаяние", "despair")],
    },
    {
        "slug": "14_blok_noch_ulitsa", "title": "Ночь, улица, фонарь, аптека", "author": "Александр Блок", "year": "1912",
        "source": "https://ru.wikisource.org/wiki/Ночь,_улица,_фонарь,_аптека_(Блок)",
        "lines": ["Ночь, улица, фонарь, аптека,", "Бессмысленный и тусклый свет.", "Живи еще хоть четверть века —", "Всё будет так. Исхода нет.", "", "Умрешь — начнешь опять сначала", "И повторится всё, как встарь:", "Ночь, ледяная рябь канала,", "Аптека, улица, фонарь."],
        "guide": "A Symbolist urban miniature constructed as a closed loop. The reordered nouns in the final line enact repetition rather than merely describing it.",
        "vocab": [("фонарь", "streetlamp"), ("тусклый", "dim"), ("исход", "way out"), ("встарь", "as before; in old times"), ("рябь", "ripples")],
    },
    {
        "slug": "15_yesenin_beryoza", "title": "Берёза", "author": "Сергей Есенин", "year": "1913",
        "source": "https://ru.wikisource.org/wiki/Берёза_(Есенин)",
        "lines": ["Белая берёза", "Под моим окном", "Принакрылась снегом,", "Точно серебром.", "", "На пушистых ветках", "Снежною каймой", "Распустились кисти", "Белой бахромой.", "", "И стоит берёза", "В сонной тишине,", "И горят снежинки", "В золотом огне.", "", "А заря, лениво", "Обходя кругом,", "Обсыпает ветки", "Новым серебром."],
        "guide": "A clear, image-led landscape lyric suited to early learners. Diminutive textures and repeated instrumental forms turn snow into silver ornament.",
        "vocab": [("берёза", "birch tree"), ("кайма", "border; edging"), ("кисти", "clusters; tassels"), ("бахрома", "fringe"), ("заря", "dawn")],
    },
    {
        "slug": "16_yesenin_do_svidanya", "title": "До свиданья, друг мой, до свиданья", "author": "Сергей Есенин", "year": "1925",
        "source": "https://ru.wikisource.org/wiki/До_свиданья,_друг_мой,_до_свиданья_(Есенин)",
        "lines": ["До свиданья, друг мой, до свиданья.", "Милый мой, ты у меня в груди.", "Предназначенное расставанье", "Обещает встречу впереди.", "", "До свиданья, друг мой, без руки и слова,", "Не грусти и не печаль бровей, —", "В этой жизни умирать не ново,", "Но и жить, конечно, не новей."],
        "guide": "A farewell whose repeated ordinary phrase carries extraordinary weight. The second stanza compresses consolation and fatalism into conversational language.",
        "vocab": [("в груди", "in the heart; literally in the chest"), ("предназначенное", "destined"), ("расставанье", "parting"), ("впереди", "ahead"), ("печаль", "sadden")],
    },
    {
        "slug": "17_derzhavin_reka_vremen", "title": "Река времён", "author": "Гавриил Державин", "year": "1816",
        "source": "https://ru.wikisource.org/wiki/Река_времён_в_своём_стремленьи_(Державин)",
        "lines": ["Река времён в своём стремленьи", "Уносит все дела людей", "И топит в пропасти забвенья", "Народы, царства и царей.", "", "А если что и остаётся", "Чрез звуки лиры и трубы,", "То вечности жерлом пожрётся", "И общей не уйдёт судьбы!"],
        "guide": "Derzhavin's final poem uses monumental abstractions and the image of a devouring river. Even poetic and military fame cannot escape the common fate.",
        "vocab": [("стремленье", "course; striving"), ("забвенье", "oblivion"), ("лира", "lyre; poetry"), ("жерло", "maw; mouth"), ("пожрётся", "will be devoured")],
    },
    {
        "slug": "18_batyushkov_moy_geniy", "title": "Мой гений", "author": "Константин Батюшков", "year": "1815",
        "source": "https://ru.wikisource.org/wiki/Мой_гений_(Батюшков)",
        "lines": ["Память сердца! ты сильней", "Рассудка памяти печальной", "И часто сладостью своей", "Меня в стране пленяешь дальной.", "", "Я помню голос милых слов,", "Я помню очи голубые,", "Я помню локоны златые", "Небрежно вьющихся волос.", "", "Моей пастушки несравненной", "Я помню весь наряд простой,", "И образ милый, незабвенный,", "Повсюду странствует со мной.", "", "Хранитель-гений мой — любовью", "В утеху дан разлуке он:", "Засну ль? приникнет к изголовью", "И усладит печальный сон."],
        "guide": "An elegiac poem about emotional memory. The repeated я помню makes recollection an active companion during distance and separation.",
        "vocab": [("рассудок", "reason"), ("пленяешь", "captivate"), ("локоны", "curls"), ("незабвенный", "unforgettable"), ("изголовье", "head of a bed")],
    },
    {
        "slug": "19_nekrasov_seyatelyam", "title": "Сеятелям", "author": "Николай Некрасов", "year": "1876",
        "source": "https://ru.wikisource.org/wiki/Сеятелям_(Некрасов)",
        "lines": ["Сеятель знанья на ниву народную!", "Почву ты, что ли, находишь бесплодную,", "Худы ль твои семена?", "Робок ли сердцем ты? слаб ли ты силами?", "Труд награждается всходами хилыми,", "Доброго мало зерна!", "", "Где же вы, умелые, с бодрыми лицами,", "Где же вы с полными жита кошницами?", "Труд засевающих робко, крупицами,", "Двиньте вперед!", "Сейте разумное, доброе, вечное,", "Сейте! Спасибо вам скажет сердечное", "Русский народ..."],
        "guide": "A public exhortation that turns education into sowing. Questions challenge timid effort; the closing imperatives give the poem its famous civic cadence.",
        "vocab": [("сеятель", "sower"), ("нива", "field; poetic"), ("всходы", "shoots; seedlings"), ("жито", "grain"), ("крупицы", "tiny grains")],
    },
    {
        "slug": "20_mayakovsky_poslushayte", "title": "Послушайте!", "author": "Владимир Маяковский", "year": "1914",
        "source": "https://ru.wikisource.org/wiki/Послушайте!_(Маяковский)",
        "lines": ["Послушайте!", "Ведь, если звезды зажигают —", "значит — это кому-нибудь нужно?", "Значит — кто-то хочет, чтобы они были?", "Значит — кто-то называет эти плевочки", "жемчужиной?", "", "И, надрываясь", "в метелях полуденной пыли,", "врывается к богу,", "боится, что опоздал,", "плачет,", "целует ему жилистую руку,", "просит —", "чтоб обязательно была звезда! —", "клянется —", "не перенесет эту беззвездную муку!", "", "А после", "ходит тревожный,", "но спокойный наружно.", "Говорит кому-то:", "«Ведь теперь тебе ничего?", "Не страшно?", "Да?!»", "", "Послушайте!", "Ведь, если звезды", "зажигают —", "значит — это кому-нибудь нужно?", "Значит — это необходимо,", "чтобы каждый вечер", "над крышами", "загоралась хоть одна звезда?!"],
        "guide": "A modernist dramatic monologue shaped by speech, broken lines, and repeated questions. Typography and breath units make private need sound like an argument addressed to a crowd.",
        "vocab": [("зажигают", "light; kindle"), ("надрываясь", "straining desperately"), ("жилистый", "sinewy"), ("клянется", "swears"), ("наружно", "outwardly")],
    },
]


def poem_markup(item: dict) -> str:
    stanzas: list[list[str]] = [[]]
    for line in item["lines"]:
        if line:
            stanzas[-1].append(line)
        elif stanzas[-1]:
            stanzas.append([])
    stanzas = [s for s in stanzas if s]
    verses = "".join("<p class=\"stanza\">" + "<br>".join(html.escape(x) for x in stanza) + "</p>" for stanza in stanzas)
    vocab = "".join(f"<li><b>{html.escape(a)}</b><span>{html.escape(b)}</span></li>" for a, b in item["vocab"])
    return f'''<article class="poem-reading" lang="ru"><p class="poet">{html.escape(item['author'])} · {item['year']}</p>{verses}</article>
<section class="study-card" contenteditable="false" lang="en"><h2>Reading guide</h2><p>{html.escape(item['guide'])}</p><h3>Core vocabulary</h3><ul>{vocab}</ul></section>'''


def translation_card(item: dict) -> str:
    query = quote(f'"{item["title"]}" {item["author"]} English translation')
    author_path = RUVERSes_AUTHORS[item["author"]]
    poem_path = RUVERSes_POEMS.get(item["slug"])
    ruverses_url = f"https://ruverses.com/{author_path}/{poem_path}/" if poem_path else f"https://ruverses.com/{author_path}/"
    ruverses_label = "Read translations on RuVerses" if poem_path else "Browse this poet on RuVerses"
    return f'''<section class="card translation-card" lang="en"><h2>English translations</h2><p>External editions are provided for comparison. Wording, lineation, and interpretation may differ from this Russian text; these links are not line-by-line alignments.</p><div class="translation-links"><a class="translation-primary" href="{ruverses_url}" target="_blank" rel="noreferrer">{ruverses_label} <span aria-hidden="true">↗</span></a><a href="https://en.wikisource.org/w/index.php?search={query}" target="_blank" rel="noreferrer">Search English Wikisource <span aria-hidden="true">↗</span></a></div></section>'''


def english_toolbar(page: str) -> str:
    """Apply the English control wording supplied in the diary backup."""
    replacements = {
        "Открыть источник ↗": "View original source ↗",
        "Без изменений": "No changes",
        "Панель редактирования": "Editing toolbar",
        "Вернуться к содержанию": "Return to contents",
        ">Содержание</a>": ">Contents</a>",
        "Свернуть панель и увеличить область текста": "Collapse the toolbar to enlarge the text area",
        ">Свернуть панель</button>": ">Collapse toolbar</button>",
        "Свернуть панель": "Collapse toolbar",
        ">Показать примечания</button>": ">Show annotated text</button>",
        "Режим: чистый текст": "View: Clean",
        "Отменить Ctrl/⌘+Z": "Undo Ctrl/⌘+Z",
        ">Отменить</button>": ">Undo</button>",
        ">Повторить</button>": ">Redo</button>",
        "Поиск по тексту": "Search text",
        "Предыдущее совпадение": "Previous match",
        "Следующее совпадение": "Next match",
        "Форматирование текста": "Text formatting",
        "Выделение и линии": "Highlight and lines",
        "Жёлтое выделение": "Yellow highlight",
        "Зелёное выделение": "Green highlight",
        "Синее выделение": "Blue highlight",
        "Розовое выделение": "Pink highlight",
        "Фиолетовое выделение": "Purple highlight",
        ">Жёлтый</button>": ">Yellow</button>",
        ">Зелёный</button>": ">Green</button>",
        ">Синий</button>": ">Blue</button>",
        ">Розовый</button>": ">Pink</button>",
        ">Фиолетовый</button>": ">Purple</button>",
        "Подчёркивание": "Underline",
        "Зачёркивание": "Strikethrough",
        "Полужирное начертание": "Bold selected text",
        ">Полужирный</span>": ">Bold</span>",
        ">Произношение</button>": ">Pronunciation</button>",
        ">Межстрочное примечание</button>": ">Interlinear note</button>",
        ">Сноска</button>": ">Footnote</button>",
        ">Комментарий</button>": ">Comment</button>",
        ">Изображение</button>": ">Image</button>",
        ">Проверить</button>": ">Check</button>",
        ">Очистить формат</button>": ">Clear format</button>",
        ">Словарь</a>": ">Dictionary</a>",
        ">Русская поэзия</a>": ">Russian poetry</a>",
        ">Читать вслух</button>": ">Read aloud</button>",
        ">Пауза</button>": ">Pause</button>",
        ">Стоп</button>": ">Stop</button>",
        "Голос для чтения": "Reading voice",
        "Голос по умолчанию": "Default voice",
        "Скорость ": "Speed ",
        ">Сохранить</button>": ">Save</button>",
        ">Резервная копия</button>": ">Backup</button>",
        ">Журнал</button>": ">Log</button>",
        ">Импорт копии</label>": ">Import backup</label>",
        ">Подсказки: вкл.</button>": ">Hints: On</button>",
        ">Уровень ": ">Level ",
        "Минимальный уровень словарных подсказок": "Minimum vocabulary hint level",
        ">Исходный текст</button>": ">Original text</button>",
        "Показать чистый текст": "Show clean text",
        "Режим: примечания": "View: Annotated",
        "Развернуть панель редактирования": "Expand the editing toolbar",
        "Развернуть панель": "Expand toolbar",
        "Подсказки: выкл.": "Hints: Off",
        "Продолжить": "Resume",
    }
    for source, target in replacements.items():
        page = page.replace(source, target)
    return page


def build_one(item: dict) -> None:
    folder = BASE / item["slug"]
    folder.mkdir(parents=True, exist_ok=True)
    plain = "\n\n".join("\n".join(s for s in item["lines"] if s))
    page = build_html(
        plain, [], item["source"], chapter_title=item["title"],
        editor_title=f"{item['title']} · {item['author']} · Russian Reader",
        storage_key=f"russian-poetry-{item['slug']}-v1", file_stem=f"russian_poetry_{item['slug']}",
        inline_notes=[], review_notes=[], reading_notes=[], global_terms=[],
        home_href="../../index.html#russian_poetry", theme_href="../../workspace_theme.css",
        shared_library_href="../index.html", shared_library_label="Русская поэзия",
        source_site_label="Викитека",
    )
    page = english_toolbar(page)
    body = poem_markup(item)
    page, count = re.subn(r'(<section id="editor" class="editor"[^>]*>)[\s\S]*?(</section>)', lambda m: m.group(1) + body + m.group(2), page, count=1)
    if count != 1:
        raise RuntimeError("Reader editor body not found")
    page = page.replace('<aside class="sidebar">', '<aside class="sidebar">' + translation_card(item), 1)
    styles = '''<style>
#editor{font-family:Georgia,"Times New Roman",serif;max-width:900px;margin-inline:auto}.poem-reading{font-size:clamp(20px,2.2vw,29px);line-height:1.72}.poet{color:#5f6368;font:600 13px/1.4 Arial,sans-serif;letter-spacing:.04em;text-indent:0!important}.stanza{margin:1.35em 0!important;text-indent:0!important}.study-card{margin:3em 0 1em;padding:20px;border:1px solid #dadce0;border-radius:10px;background:#f8f9fa;font:16px/1.65 Arial,sans-serif}.study-card h2,.study-card h3{margin:.2em 0 .65em}.study-card ul{display:grid;gap:7px;padding:0;list-style:none}.study-card li{display:grid;grid-template-columns:minmax(110px,.35fr) 1fr;gap:12px;padding-top:7px;border-top:1px solid #e1e4e8}.study-card li span{color:#5f6368}.translation-card p{margin:0 0 10px;color:#5f6368;font:12px/1.55 Arial,sans-serif}.translation-links{display:grid;gap:7px}.translation-links a{display:flex;justify-content:space-between;gap:8px;padding:9px 10px;border:1px solid #c7d3e3;border-radius:6px;background:#f8fbff;color:#174ea6;text-decoration:none;font:700 12px/1.35 Arial,sans-serif}.translation-links a:hover{border-color:#174ea6;background:#e8f0fe}@media(max-width:600px){.study-card li{grid-template-columns:1fr;gap:1px}}
</style>'''
    page = page.replace("</head>", styles + "</head>", 1)
    page = page.replace("</body>", '<script src="../../mobile_pwa.js"></script></body>', 1)
    (folder / "editor.html").write_text(page, encoding="utf-8")


def build_index() -> None:
    cards = "".join(f'''<article><span>{n:02d}</span><div><small>{html.escape(p['author'])} · {p['year']}</small><h2>{html.escape(p['title'])}</h2></div><a href="{p['slug']}/editor.html?view=annotated">Читать</a></article>''' for n, p in enumerate(POEMS, 1))
    page = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Русская поэзия · Reader</title><link rel="stylesheet" href="../workspace_theme.css"><style>*{{box-sizing:border-box}}body{{margin:0;background:#f1f3f4;color:#202124;font-family:Arial,sans-serif}}main{{width:min(980px,calc(100% - 28px));margin:28px auto 80px}}header,section{{padding:26px;border:1px solid #dadce0;border-radius:12px;background:#fff}}header{{background:linear-gradient(135deg,#7b1e2b,#273c75);color:#fff}}header a{{color:#fff}}h1{{margin:.15em 0;font:700 clamp(36px,7vw,66px)/1.05 Georgia,serif}}header p{{max-width:720px;line-height:1.6}}section{{display:grid;gap:9px;margin-top:16px}}article{{display:grid;grid-template-columns:42px 1fr auto;gap:12px;align-items:center;padding:14px;border:1px solid #e1e4e8;border-radius:9px}}article h2{{margin:3px 0;font:700 21px Georgia,serif}}article small{{color:#5f6368}}article a{{padding:8px 12px;border:1px solid #b7c5dc;border-radius:18px;color:#174ea6;text-decoration:none;font-weight:700}}@media(max-width:560px){{article{{grid-template-columns:32px 1fr}}article a{{grid-column:2;justify-self:start}}}}</style></head><body><main><header><a href="../index.html#russian_poetry">← Reader library</a><h1>Русская поэзия</h1><p>Russian-first sample readings: Pushkin and poets in the classical tradition. English support is deliberately brief so that the poem remains the center of attention.</p></header><section>{cards}</section></main><script src="../workspace_skin.js"></script><script src="../mobile_pwa.js"></script></body></html>'''
    (BASE / "index.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    for poem in POEMS:
        build_one(poem)
    build_index()
    print(f"Built {len(POEMS)} Russian poetry readings")
