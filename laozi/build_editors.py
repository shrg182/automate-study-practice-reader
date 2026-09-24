#!/usr/bin/env python3
import csv,json,sys
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent; SHARED=BASE_DIR.parent/"shiji"/"shiji_lisheng_lujia";sys.path.insert(0,str(SHARED))
from build_editor import build_html,load_global_terms,load_terms
rare_terms=load_terms(BASE_DIR/"rare_terms.csv")
with (BASE_DIR/"catalog.csv").open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
for row in rows:
    target=BASE_DIR/f"{int(row['sequence']):02d}_{row['slug']}"; text=(target/"original.txt").read_text(encoding="utf-8"); local_terms=load_terms(target/"reading_terms.csv"); local_names={item["term"] for item in local_terms}; terms=local_terms+[item for item in rare_terms if item["term"] in text and item["term"] not in local_names]
    output=build_html(text,terms,row["source_url"],chapter_title=f"《老子·{row['section']}·{row['title']}》",editor_title=f"《老子·{row['title']}》校读编辑器",storage_key=f"laozi-{row['sequence']}-editor-v1",file_stem=f"laozi_{int(row['sequence']):02d}",global_terms=load_global_terms(BASE_DIR.parent/"project_dictionary"/"dictionary.csv",text,terms),home_href="../../index.html",shared_library_href="",source_site_label="古文岛")
    (target/"editor.html").write_text(output,encoding="utf-8");print(f"Built {target/'editor.html'}")
