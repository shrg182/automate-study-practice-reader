# 《翦商》与共享项目词典同步

《翦商》章节词表是共享项目词典的来源之一。运行以下命令时，构建器会先从整个项目重新生成共享词典，再重建全部章节编辑器：

```bash
python3 practice/jianshang/build_ocr_editor.py --all
```

因此，章节编辑器使用的项目词典快照与 `project_dictionary/index.html` 使用同一次生成的数据一致。只有在调试且明确需要旧快照时，才使用 `--skip-dictionary-refresh`。

## 浏览器中的人工修订

直接以 `file://` 打开页面时，不同本地文件的浏览器存储可能彼此隔离。共享词典中的临时修改不会可靠地自动传播到每个章节。

同步步骤：

1. 在共享项目词典点击 `Export local edits`，下载 `reading_lexicon_local_edits.json`。
2. 在《翦商》编辑器点击 `导入词典修订`，选择该 JSON。
3. 编辑器会更新匹配词条的拼音、释义和难度，并在该页面的浏览器存储中保存修订。

共享项目词典也提供 `Import local edits`，用于把先前导出的修订恢复到词典页面。

长期、可提交的修改仍应写入章节 `reading_terms.csv` 或其他结构化词汇源，再重新运行构建器；浏览器 JSON 是传递和备份临时人工修订的机制，不取代源文件。
