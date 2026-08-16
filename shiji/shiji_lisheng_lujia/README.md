# 《史记·郦生陆贾列传》阅读材料

本目录把古文岛上的《七十列传·郦生陆贾列传第三十七》处理成适合阅读的本地文本、生字词表和注音 PDF。流程沿用 `jianshang` 与 `nine_commentaries` 的原则：保留来源、建立可编辑清稿、使用聚焦词典、只注真正影响阅读的生僻字词，并让生成物可以重复构建。

## 文件

- `sources/page.html`：下载时保存的原始网页快照。
- `source.txt`：从网页正文容器直接提取的原始段落。
- `lisheng_lujia_clean.txt`：可人工校订的生成依据；首次下载时与 `source.txt` 相同。
- `reading_terms.csv`：精选人名、地名、异体字、古义词与生僻词。
- `lisheng_lujia_shengzibiao.txt`：带次数和原文词例的阅读词表。
- `lisheng_lujia_annotated.pdf`：各词首次出现时加拼音，文末附阅读词表。
- `lisheng_lujia_annotated.txt`：用于检查注音位置的纯文本中间结果。
- `build_editor.py`：把最新清稿和阅读词典嵌入自包含的浏览器编辑器。
- `editor.html`：校读编辑器，可编辑正文、添加注音/简注、脚注、按语和待核标记，并支持浏览器朗读。
- `import_editor_export.py`：导入编辑器 JSON 备份，更新清稿、人工新增词条和待核记录，并保留导入前清稿。

## 使用方法

```bash
cd practice/shiji/shiji_lisheng_lujia
python3 download_article.py
python3 build_editor.py
python3 make_rare_word_table.py
python3 make_annotated_pdf.py --annotated-text-output lisheng_lujia_annotated.txt
```

默认只在每个词第一次出现时标拼音，以免正文过密。需要逐次标注时，在 PDF 命令后加 `--repeat-annotations`。

### HTML 校读编辑器

生成后直接在浏览器中打开 `editor.html`。正文可以直接修改；选择文字后可以：

- 使用工具栏最左侧按钮在“清稿”和“注音稿”之间双向切换；第一次进入注音稿时，阅读词典会自动标注每个词的首次出现位置；
- 添加拼音和简注，或点击右侧词典条目快速套用；
- 插入带编号的脚注；
- 插入独立按语，并给所选原文加评论标记；
- 标记待核文字并记录原因；
- 使用系统中文声音朗读选中文字或全文，调整语速、暂停和继续；
- 自动保存到当前浏览器，导出 TXT、完整 HTML 或 JSON 备份。

浏览器编辑器不会直接覆盖 `lisheng_lujia_clean.txt`。导出的 `lisheng_lujia_clean_edited.txt` 应先与清稿比较并人工审核，再决定是否替换生成依据。修改清稿或词典后，重新运行 `python3 build_editor.py` 更新编辑器的初始内容。

清稿/注音稿切换是同一份正文的两种显示方式：切回清稿只隐藏拼音和黄色注释样式，不会删除注音、脚注、按语或正文编辑；再次切换到注音稿即可恢复显示。

### 把编辑器修改更新到 TXT 和 PDF

点击编辑器的“导出备份”后运行：

```bash
cd practice/shiji/shiji_lisheng_lujia
python3 import_editor_export.py
python3 make_rare_word_table.py
python3 make_annotated_pdf.py --annotated-text-output lisheng_lujia_annotated.txt
python3 build_editor.py
```

导入脚本默认选择 Downloads 中最新的 `lisheng_lujia_editor_backup*.json`。也可以把具体 JSON 路径作为参数。首次导入会把原清稿保存为 `lisheng_lujia_clean_before_editor.txt`，然后更新清稿；编辑器中人工新增的注音会补入 `reading_terms.csv`，待核标记会写入 `review_notes.tsv`。之后三个命令依次更新词表、注音 TXT、PDF 和编辑器初始内容。

## 编辑规则

- 不把 `後、於、彊、畔、籓、轝、硃` 等旧字形自动改成现代简体。
- 人名采用专名读音，例如 `郦食其（lì yì jī）`。
- 优先收录会阻碍断句、读音或理解的项目，而不是罗列所有古汉语常用词。
- 原文中的 `天下之旻` 语义可疑，但下载文本与网页一致，暂不擅改，并在词表中提示核读。
- 修改词典或清稿后，重新运行后两个生成脚本。

## 配额估算

下载、解析、制表和 PDF 生成均在本地完成，不调用模型 API，因此脚本运行本身消耗 **0 API tokens**。

本次实测原文为 4,953 个字符（4,906 个非空白字符）。如另用语言模型复核，可按以下保守范围预留：

- 单次“全文 + 指令”输入：约 6,000–9,000 tokens；
- 57 条结构化词表输出：约 2,500–4,500 tokens；
- 一次简短复核：约 3,000–6,000 tokens；
- 完整三步流程合计：约 12,000–20,000 tokens。

不同模型的中文分词和隐藏推理计费方式可能不同，因此这不是账户账单上限。当前工作区无法读取用户账户的剩余额度；若产品仍按消息数或周额度限制，本地脚本运行不会占用该额度，只有与模型交互的复核步骤会占用。

原文来源：<https://www.guwendao.net/guwen/bookv_2cd08cb40d37.aspx>
