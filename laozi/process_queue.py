#!/usr/bin/env python3
import argparse,csv,json,re,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup
BASE_DIR=Path(__file__).resolve().parent
def read(path):
    with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def newest():
    files=list((Path.home()/"Downloads").glob("laozi_processing_queue*.json"));
    if not files:raise FileNotFoundError("No laozi_processing_queue*.json found in Downloads")
    return max(files,key=lambda p:p.stat().st_mtime)
def main():
    p=argparse.ArgumentParser();p.add_argument("queue",nargs="?",type=Path);p.add_argument("--validate-only",action="store_true");a=p.parse_args();queue=a.queue or newest();data=json.loads(queue.read_text(encoding="utf-8"));wanted={str(x.get("sequence","")) for x in data.get("chapters",[])};sources={x["sequence"]:x for x in read(BASE_DIR/"source_catalog.csv")}
    if not wanted or wanted-sources.keys():raise ValueError("Queue contains no valid saved 《老子》 chapters")
    if a.validate_only:print(f"Valid queue: {len(wanted)} chapter(s)");return
    catalog=read(BASE_DIR/"catalog.csv");by={x["sequence"]:x for x in catalog};selected=[]
    for seq in sorted(wanted,key=int):
        src=sources[seq];row=by.get(seq) or {"sequence":seq,"section":src["section"],"title":src["title"],"slug":f"chapter_{int(seq):02d}","source_url":src["source_url"],"status":"downloaded"}
        if seq not in by:catalog.append(row);by[seq]=row
        selected.append(row);target=BASE_DIR/f"{int(seq):02d}_{row['slug']}"
        if not (target/"source.json").exists():
            response=requests.get(row["source_url"],headers={"User-Agent":"Mozilla/5.0"},timeout=30);response.raise_for_status();soup=BeautifulSoup(response.text,"html.parser");body=soup.select_one(".contson")
            if body is None:raise ValueError(f"No chapter text found: {row['source_url']}")
            text="\n\n".join(x.get_text("",strip=True) for x in body.find_all("p",recursive=False)) or body.get_text("",strip=True);target.mkdir(exist_ok=True);(target/"original.txt").write_text(text+"\n",encoding="utf-8");(target/"reading_terms.csv").write_text("term,pinyin,annotation,type\n",encoding="utf-8");(target/"review_notes.tsv").write_text("text\tissue\tstatus\n",encoding="utf-8");(target/"source.json").write_text(json.dumps({**row,"retrieved_at":datetime.now(timezone.utc).isoformat(),"source_site":"古文岛","characters":len(text)},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with (BASE_DIR/"catalog.csv").open("w",encoding="utf-8",newline="") as f:w=csv.DictWriter(f,fieldnames=["sequence","section","title","slug","source_url","status"]);w.writeheader();w.writerows(sorted(catalog,key=lambda x:int(x["sequence"])))
    subprocess.run([sys.executable,str(BASE_DIR/"build_editors.py")],check=True);subprocess.run([sys.executable,str(BASE_DIR/"build_selector.py")],check=True);subprocess.run([sys.executable,str(BASE_DIR.parent/"build_index.py")],check=True)
    if data.get("generatePdfs"): subprocess.run([sys.executable,str(BASE_DIR/"make_pdfs.py"),*[v for row in selected for v in ("--sequence",row["sequence"])]],check=True)
if __name__=="__main__":main()
