# 《史记·秦本纪》阅读材料

本目录处理古文岛《十二本纪·秦本纪第五》，遵循 `practice/shiji/README.md` 的来源保存、清稿复核、聚焦词表、注音输出和编辑器往返规则。

## 来源与规模

- 正文：<https://www.guwendao.net/guwen/bookv_cab5e2fff7da.aspx>
- 篇名：十二本纪·秦本纪第五
- 原文：71 个自然段，约 10,551 个字符
- 提取方式：直接解析网页正文 HTML，无 OCR

## 文件

- `sources/page.html`：原始网页快照。
- `source.txt`：网页正文的原始提取文本。
- `qin_benji_clean.txt`：生成依据和人工校订清稿。
- `reading_terms.csv`：生僻字、古义词、人名、地名、礼制和官制词典。
- `qin_benji_shengzibiao.txt`：阅读词表。
- `qin_benji_annotated.txt`、`qin_benji_annotated.pdf`：注音阅读输出。
- `editor.html`：清稿/注音稿双向切换的校读编辑器，支持注音、脚注、按语、待核标记、导出和朗读。
- `import_editor_export.py`：从 Downloads 导入最新 `qin_benji_editor_backup*.json`。

## 打开 HTML 编辑器

- 仓库内链接：[打开 `editor.html`](editor.html)
- 本机完整链接：<file:///Users/ruixingshi/Python/automate_study_practices/practice/shiji/shiji_qin_benji/editor.html>

如果 Markdown 查看器禁止打开 `file://` 链接，请复制本机完整链接到浏览器地址栏，或直接双击目录中的 `editor.html`。

## 生成

```bash
cd practice/shiji/shiji_qin_benji
python3 download_article.py
python3 make_rare_word_table.py
python3 make_annotated_pdf.py --annotated-text-output qin_benji_annotated.txt
python3 build_editor.py
```

开始人工编辑后不要随意重跑下载脚本，因为它会重置清稿。词典或清稿改变后，只需重跑后三个命令。

## 编辑器修改回写

```bash
python3 import_editor_export.py
python3 make_rare_word_table.py
python3 make_annotated_pdf.py --annotated-text-output qin_benji_annotated.txt
python3 build_editor.py
```

首次导入会保留 `qin_benji_clean_before_editor.txt`。人工新增注音会进入词典，待核标记会进入 `review_notes.tsv`。

## 本篇校读重点

- `缪公`、`周缪王` 中“缪”依专名分别按穆公、穆王处理。
- 保留网页底本的旧字和通假形式，如 `適、蚤、详、罢、髪`，不自动现代化。
- 人名和地名优先按完整专名标注，避免单字注音误伤普通语境。
- 年表段落人名、地名密集，词表以真正妨碍阅读的项目为主，不追求收录全部地名。
- `皂游、黄髪番番、马騺、獂王` 等罕见写法宜在进一步版本校勘时重点复核。

已确认的网页标点清理：

- `赎之。”。楚人遂许与之` → `赎之。”楚人遂许与之`

当前生成状态：词表 109 条，注音 PDF 15 页；首页、正文中间页和末尾词表页已经渲染检查。

## 配额估算

本地下载、制表、PDF 和编辑器生成消耗 0 API tokens。若用模型进行一次全文词表审查和一次复核，本篇按约 10,551 字估计需要约 24,000–38,000 tokens；分两段处理会更稳妥。
