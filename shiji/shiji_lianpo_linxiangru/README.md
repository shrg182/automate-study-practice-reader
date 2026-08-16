# 《史记·廉颇蔺相如列传》阅读材料

本目录处理古文岛《七十列传·廉颇蔺相如列传第二十一》，沿用
`practice/jianshang` 的新版编辑工作流和 `practice/shiji/README.md`
的来源、清稿、词表与生成规则。

## 来源

- 正文：<https://www.guwendao.net/guwen/bookv_fe564cb98c22.aspx>
- 篇名：七十列传·廉颇蔺相如列传第二十一
- 提取方式：解析网页 `div.contson` 内的直接段落，无 OCR
- 当前规模：人工校订后约 4,900 个正文字符
- 当前输出：27 条阅读词典及注音 PDF
- 校订状态：2026-07-30 浏览器人工校订已导入并重新生成全部输出

## 编辑器

[`editor.html`](editor.html) 支持：

- 清稿/注音稿切换；
- 浏览器自动保存和手动保存；
- 注音、编者注、按语与待核标记；
- 中文朗读与语速选择；
- 编辑日志、JSON 备份、TXT/HTML 导出；
- 阅读词典、统计和用户札记；
- 控制栏中的全书词典入口；
- 可编辑、可导出 CSV 的本篇词典；
- 注音采用拼音、简注两步输入；正文只显示拼音，简注保留在右侧本篇词典；
- 从备份回写清稿、词表和疑文表。

`按语`仍使用独立段落样式；较长说明继续使用脚注。点击正文中的注音可
定位并高亮右侧本篇词典条目，完整简注在词典中查看和编辑。

行间注使用自然宽度并在所选原文上方居中，不拉伸较短的注释文字。若
行间注长于所选原文，编辑器会先询问，再将它转换为编号脚注。

浏览器本地保存不能代替导出。完成一轮人工编辑后，应导出 JSON 备份和
TXT，并运行 `import_editor_export.py`。

本轮导入另保存：

- `lianpo_linxiangru_edit_log.txt`：浏览器编辑日志；
- `lianpo_linxiangru_reading_notes.txt`：编辑器功能反馈札记；
- `lianpo_linxiangru_clean_before_editor.txt`：导入前清稿备份；
- `review_notes.tsv`：仍待核对的文本项目。

## 生成

```bash
cd practice/shiji/shiji_lianpo_linxiangru
python3 download_article.py
python3 make_rare_word_table.py
python3 make_annotated_pdf.py --annotated-text-output lianpo_linxiangru_annotated.txt
python3 build_editor.py
```

开始人工校订后不要直接重跑下载脚本，以免误覆盖清稿。下载脚本只会在
清稿尚不存在时建立初始清稿。
