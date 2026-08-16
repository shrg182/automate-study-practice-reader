# 《史记·淮阴侯列传》阅读材料

本目录处理古文岛《七十列传·淮阴侯列传第三十二》，使用 Shiji
共享编辑器以及从 `practice/jianshang` 沿用的保存、日志、札记、注音、
脚注、按语、待核和导出工作流。

## 来源

- 正文：<https://www.guwendao.net/guwen/bookv_30856b7cc757.aspx>
- 篇名：七十列传·淮阴侯列传第三十二
- 提取方式：解析网页 `div.contson` 内的直接段落，无 OCR
- 当前规模：2026-07-31 最新人工校订已导入，8,318 个字符
- 注音词条：52 条
- 行间注：7 条
- 按语：5 条
- 脚注：4 条，正文标记与注释一一对应
- 待核：0 条
- 注音 PDF：A4，共 12 页，已按最新校订重新生成

## 编辑器

打开 [`editor.html`](editor.html)。正文中的注音词以原词作为锚点；点击
原词会在固定右侧栏显示并定位对应的拼音和简注。添加注音采用“拼音、
简注”两步输入，正文只显示拼音，简注保留在本篇词典中且不限制为
60 字。编辑器另支持脚注块、
词典编辑与导出、浏览器自动保存、编辑日志、用户札记、朗读和 JSON 备份。

行间注以自然宽度居中显示在所选原文上方，不拉伸较短注释。若行间注
长于所选原文，编辑器会询问是否将其转换为编号脚注。`按语`保持独立
段落样式，不参与自动转换。

脚注、行间注、按语和待核登记表均可点击来源文字返回正文；脚注标记与
脚注编号支持双向跳转。待核原因为空时显示“未填写待核原因”，来源文字
仍可定位。

## 生成

```bash
cd practice/shiji/shiji_huaiyin_hou
python3 download_article.py
python3 make_rare_word_table.py
python3 make_annotated_pdf.py --annotated-text-output huaiyin_hou_annotated.txt
python3 build_editor.py
```

下载脚本只在清稿不存在时建立初始清稿，避免覆盖已经开始的人工校订。
