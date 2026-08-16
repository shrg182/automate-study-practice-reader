# 《容斋随笔》校读材料

本目录将 5000言《容斋随笔》整理为与《聊斋志异》故事相同风格的校读材料。项目结构、文本分层、来源归属和扩展方案见 [PLAN.md](PLAN.md)。

当前试点为卷一前三篇：欧率更帖、罗处士志、唐《平蛮碑》。

## 重新生成试点

```bash
python3 practice/rongzhai_suibi/download_rongzhai.py
python3 practice/rongzhai_suibi/build_editors.py
python3 practice/rongzhai_suibi/make_pdfs.py
```

下载器只从 `catalog.csv` 读取目标页面。若已有网页缓存，可使用：

```bash
python3 practice/rongzhai_suibi/download_rongzhai.py --source-dir /path/to/cache
```

## 选择与批处理篇目

打开 `select_articles.html`，可按卷次或篇名筛选 329 篇源站目录，粘贴单篇链接，或勾选多篇。页面会导出 `rongzhai_processing_queue.json`。

```bash
python3 practice/rongzhai_suibi/process_queue.py ~/Downloads/rongzhai_processing_queue.json
```

处理器会核对 `source_catalog.csv`，只将选中篇目加入 `catalog.csv`，然后下载、构建编辑器并更新目录。选择页也可在处理清单中要求同时生成 PDF。

每篇的 `original.txt` 是纯原文；`reading.txt` 带来源脚注；`source_notes.tsv` 和 `translation.txt` 分别保存站点注释与译文。人工内容不要直接写入这些来源文件。
