# 《老子》校读项目

打开 `select_chapters.html`，按「道经」或「德经」选择章节，然后导出 `laozi_processing_queue.json`。

```bash
python3 practice/laozi/process_queue.py ~/Downloads/laozi_processing_queue.json
```

只有选中的章节会被下载和构建；选择页可要求同时生成 PDF。
