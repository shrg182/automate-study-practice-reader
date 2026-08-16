# 《史记》阅读材料项目指南

本目录用于长期整理《史记》各篇的阅读材料。每篇建立独立子目录，保存网页来源、原始正文、人工校订清稿、聚焦生字词表、注音文本和注音 PDF。

处理原则沿用 `practice/jianshang` 与 `practice/nine_commentaries` 的成熟做法：来源可追溯、原文与清稿分离、疑文不擅改、词表以帮助阅读为目标、生成步骤可以重复执行、最终 PDF 必须经过内容和版面检查。

## 来源登记

- 《史记》目录：<https://www.guwendao.net/guwen/book_7723bfd24ca1.aspx>
- 已处理：`shiji_lisheng_lujia/`——《七十列传·郦生陆贾列传第三十七》
- 已处理：`shiji_qin_benji/`——《十二本纪·秦本纪第五》，正文 <https://www.guwendao.net/guwen/bookv_cab5e2fff7da.aspx>
- 已处理：`shiji_lianpo_linxiangru/`——《七十列传·廉颇蔺相如列传第二十一》，正文 <https://www.guwendao.net/guwen/bookv_fe564cb98c22.aspx>
- 已处理：`shiji_huaiyin_hou/`——《七十列传·淮阴侯列传第三十二》，正文 <https://www.guwendao.net/guwen/bookv_30856b7cc757.aspx>
- 已处理：`shiji_zhao_shijia/`——《三十世家·赵世家第十三》，正文 <https://www.guwendao.net/guwen/bookv_b0999505466b.aspx>
- 已处理：`shiji_fanju_caize/`——《七十列传·范雎蔡泽列传第十九》，正文 <https://www.guwendao.net/guwen/bookv_fc115edcdd90.aspx>
- 初建：`shiji_shangjun/`——《七十列传·商君列传第八》，正文 <https://www.guwendao.net/guwen/bookv_294ca85f5800.aspx>

增加新篇时，应同时在这里登记篇名、子目录和直接正文 URL。目录页用于发现篇章，篇章正文页才是下载脚本的默认来源。

## 推荐目录结构

新篇目录使用稳定、简短的英文或拼音标识：

```text
practice/shiji/
  README.md
  shiji_<article_id>/
    README.md
    download_article.py
    make_rare_word_table.py
    make_annotated_pdf.py
    build_editor.py
    editor.html
    sources/
      page.html
    source.txt
    <article_id>_clean.txt
    reading_terms.csv
    review_notes.tsv              # 有疑文时使用
    <article_id>_shengzibiao.txt
    <article_id>_annotated.txt
    <article_id>_annotated.pdf
```

文件职责：

- `sources/page.html`：下载时保存的原始网页快照，不作人工修改。
- `source.txt`：从指定正文容器提取的原文，作为可重复核对的文本基线。
- `*_clean.txt`：经核查的生成依据。所有文字修订只进入此文件，并在篇章 README 或 `review_notes.tsv` 留痕。
- `reading_terms.csv`：人工筛选的阅读词典，不是自动罗列的全字表。
- `practice/shiji/shared_references.csv`：所有《史记》篇章共用的参考资料库，保存标题、链接、说明、标签和标准脚注文字。
- `review_notes.tsv`：记录版本异文、疑似讹字、无法确定的读音或需要查证的句子。
- `*_shengzibiao.txt`、`*_annotated.txt`、`*_annotated.pdf`：可由脚本重新生成的输出。
- `build_editor.py`、`editor.html`：可选的自包含校读界面，用于正文修改、注音、脚注、按语、疑文标记、浏览器本地保存与朗读。当前共享编辑器已吸收《翦商》工作流的编辑日志、用户札记、JSON 备份和清稿回写设置。

共享编辑器的脚注、行间注、按语、待核记录和用户札记支持粘贴或选择图片与短视频。图片还可以在正文光标所在段落后直接粘贴或插入，并可填写图注、调整显示尺寸；清稿与正文朗读会自动排除这些图片。媒体存入浏览器 IndexedDB，并随 JSON 备份导出；限制为图片每张 2 MB、视频每段 10 MB、每篇合计 25 MB，图片最长边会自动缩至 1600 px。

## 标准处理流程

### 1. 建立篇章目录

复制现有篇章的三个轻量脚本作为起点，修改：

- 默认正文 URL；
- 输出文件前缀；
- PDF 标题；
- 网页正文选择器（仅当网站结构不同）。

脚本从篇章目录运行时，共享工具路径应指向：

```python
BASE_DIR.parents[1] / "liaozhai_stories"
```

当前 PDF 和词表生成逻辑复用 `practice/liaozhai_stories/liaozhai_tools.py`。如果以后多篇《史记》出现共同的特殊需求，再将共享逻辑提取为 `practice/shiji/shiji_tools.py`，避免在篇章脚本中复制大段代码。

`practice/shiji/reference_library/` 是独立的《史记》参考资料库。各篇编辑器工具栏中的“史记资料库”按钮位于“全书词典”旁边，点击后打开资料库页面。页面支持搜索、标签筛选、打开来源、复制标准引用、添加或编辑浏览器副本，以及导出合并后的 CSV。

项目中的规范数据仍保存在 `practice/shiji/shared_references.csv`。修改该 CSV 后运行：

```bash
python3 practice/shiji/reference_library/build_library.py
```

即可更新浏览器数据。浏览器内的编辑不会直接改写项目文件；使用“导出 CSV”取得 `shared_references_edited.csv`，审核后再替换或合并规范数据。

### 2. 下载并保存来源

```bash
cd practice/shiji/shiji_<article_id>
python3 download_article.py
```

下载后确认：

- 标题与目标篇章一致；
- 段落数和首尾句合理；
- 没有导航、广告、译文、赏析或页脚混入正文；
- `sources/page.html`、`source.txt` 和 `*_clean.txt` 均已生成；
- 网页若依赖动态加载，脚本必须在正文为空时明确报错，不得生成空文件冒充成功。

重新下载会覆盖初始清稿。已经开始人工校订后，不应直接重跑下载脚本；先备份或比较 `source.txt` 与 `*_clean.txt` 的差异。

### 3. 校订正文

以网页快照为直接来源，同时参考可靠的《史记》版本处理疑点。遵守以下规则：

- 不自动把 `後、於、彊、畔、籓、轝、硃` 等旧字形转换成现代简体。
- 不因现代习惯擅自改写人名、地名、官名或古代专名。
- 不悄悄修正疑似讹字。确定的修订记录“原文 → 清稿”和依据；不能确定的保留原文并标为待核。
- 区分异体字、通假字、古今字和真正的录入错误；词表简注可以解释，但正文原则上忠于选定底本。
- 标点只在确有助于阅读且不改变句义时调整。
- 保留自然段结构，不把整篇压成单段，也不随意拆散完整语句。
- 人名读音必须按专名核对，例如 `郦食其（lì yì jī）`，不能直接采用逐字常用音。

建议的疑文表：

```tsv
location	source_text	clean_text	issue	action	status
第3段	天下之旻	天下之旻	语义可疑，待查可靠版本	暂保留原文并在词表提示	open
```

### 4. 编写阅读词典

`reading_terms.csv` 使用：

```csv
term,pinyin,type,annotation
郦食其,lì yì jī,person,秦汉之际说客；“食其”在人名中读“异基”。
刓,wán,rare_word,削磨；文中指把印章摩挲把玩而迟迟不授。
```

推荐类型：

- `rare_word`：生僻字、古义词、通假字或难读写法；
- `person`：人名、字、封号；
- `place`：古地名、关塞、山川；
- `office`：官职与制度称谓；
- `artifact`：器物、服饰、车马；
- `concept`：礼制、政治、军事或历史概念；
- `text`：书名、篇名或典籍名称；
- `added`：人工决定必须保留的特殊条目。

筛选标准：

- 优先收录会阻碍读音、断句或理解的词；
- 优先使用完整专名或固定词组，避免只收其中一个字造成误注；
- 多字词与单字重叠时，以能表达上下文意义的多字词为主；
- 简注应短、准、面向当前句义，不写成百科全书条目；
- 普通常用词和一望可知的人名不必大量收录；
- 每个词必须实际出现在清稿中，拼音使用带声调符号的小写形式。

### 5. 生成词表和 PDF

```bash
python3 make_rare_word_table.py
python3 make_annotated_pdf.py \
  --annotated-text-output <article_id>_annotated.txt
```

默认只在每个词第一次出现时加拼音，以免正文过密。确有需要时才使用：

```bash
python3 make_annotated_pdf.py --repeat-annotations
```

每次修改清稿或 `reading_terms.csv` 后，都必须重新生成词表、注音文本和 PDF。

## 审阅清单

### 正文核对

- 标题、首句、末句和段落数与来源相符。
- `source.txt` 保持原始提取状态，人工改动只在清稿中。
- 清稿没有网站菜单、版权文字、译文或赏析残留。
- 异体字和旧字形处理一致，没有无意的简繁混杂。
- 人名、地名、封号和多音字读音已按上下文核对。
- 疑文有记录，未把猜测当作确定修订。

### 词表核对

- CSV 表头为 `term,pinyin,type,annotation`。
- 每条词语确实出现于清稿，且没有重复或不必要的重叠项。
- 拼音声调、轻声、专名读音和古音语境均已检查。
- 注释解释的是当前上下文，而非无关义项。
- 词表数量聚焦于阅读困难，不以数量越多越好。
- 生成的生字表中，出现次数和原文词例合理。

### 注音文本与 PDF 核对

- 注音落在完整词语之后，没有插入重叠词内部。
- 默认情况下每个条目只标第一次，后文不反复干扰阅读。
- PDF 标题、来源 URL、正文和附表均正确。
- 中文字形、拼音声调符号、标点和生僻字没有缺字方框。
- 页面没有文字越界、孤行标题、表格截断或异常大空白。
- 至少渲染检查 PDF 首页、一个正文中间页和词表末页。
- `pdfinfo` 能正常读取页数、标题和文件大小。

建议的本地检查命令：

```bash
python3 -m py_compile download_article.py make_rare_word_table.py make_annotated_pdf.py
pdfinfo <article_id>_annotated.pdf
pdftoppm -f 1 -l 1 -png -r 120 <article_id>_annotated.pdf /tmp/shiji_first_page
```

## 篇章 README 要求

每个子目录的 README 至少记录：

- 正式篇名与直接正文 URL；
- 当前状态和最后生成日期；
- 文件说明和完整生成命令；
- 原文字数、段落数、词表条目数和 PDF 页数；
- 已确认修订及依据；
- 尚未解决的疑文或读音；
- PDF 是否在最新修改后重新生成并完成版面检查；
- 本篇特有的配额估算。

## 配额估算方法

本地下载、HTML 解析、词表匹配和 PDF 生成不调用模型 API，脚本运行本身消耗 **0 API tokens**。

若使用语言模型辅助筛选或复核生词，可用下列保守方法预估：

1. 统计清稿的非空白字符数 `N`；
2. 全文输入按约 `1.2N–1.8N` tokens 预留，并加上指令长度；
3. 每条结构化词表输出按约 `40–80` tokens 预留；
4. 再为一次复核预留约首轮输入的 `40%–70%`；
5. 长篇应分段处理，并保留约 `20%` 的上下文余量。

这是规划范围，不代表账户实际账单。工作区不能读取用户账户的剩余额度；如产品采用消息数、周额度或隐藏推理计费，应以产品界面显示为准。

## 完成标准

一篇《史记》阅读材料只有在以下条件全部满足后才标记为完成：

- 来源快照和原始提取文本均已保存；
- 清稿经过正文与疑文复核；
- 阅读词典聚焦且拼音、释义已检查；
- 生字表、注音文本和 PDF 均由最新文件生成；
- PDF 经过实际渲染检查；
- 篇章 README 的统计、修订、疑点和状态已经更新。

## Sources of the Book

## 藏书网 史记

* 列传 
[https://www.99csw.com/book/9038/322389.htm](https://www.99csw.com/book/9038/322389.htm)

Feature:
1. inline annotation of the words
2. Able to take notes after login
3. dropdown list on the subtitle
4. unable to copy text


## 实修驿站

[史记](http://www.shixiu.net/wenhua/gdss/sj/)

[郦生陆贾列传](http://www.shixiu.net/wenhua/gdss/sj/5476.html)

Features:
1. The text looks clean
2. No annotation
3. No interpretation

## 太极书馆

[史记](https://www.8bei8.com/book/shijiyizhu.html)

[七十列传·郦生陆贾列传第三十七](https://www.8bei8.com/book/shijiyizhu_87.html)
