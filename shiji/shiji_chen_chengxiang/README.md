# 《史记·陈丞相世家》阅读材料

本目录处理古文岛《三十世家·陈丞相世家第二十六》。正文直接从网页正文提取，无 OCR。

## 来源

- <https://www.guwendao.net/guwen/bookv_f135449a9ab5.aspx>

## 生成

```bash
python3 practice/shiji/shiji_chen_chengxiang/download_article.py
python3 practice/shiji/shiji_chen_chengxiang/build_editor.py
```

To promote a Reader JSON backup, run:

```bash
python3 practice/shiji/shiji_chen_chengxiang/import_editor_export.py /path/to/chen_chengxiang_editor_backup.json \
  --clean practice/shiji/shiji_chen_chengxiang/chen_chengxiang_clean.txt \
  --dictionary practice/shiji/shiji_chen_chengxiang/reading_terms.csv \
  --review-notes practice/shiji/shiji_chen_chengxiang/review_notes.tsv \
  --inline-notes practice/shiji/shiji_chen_chengxiang/inline_notes.tsv \
  --backup practice/shiji/shiji_chen_chengxiang/chen_chengxiang_clean_before_editor.txt
```
