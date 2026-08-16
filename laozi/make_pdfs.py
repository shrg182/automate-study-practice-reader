#!/usr/bin/env python3
import argparse,csv,sys
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent;sys.path.insert(0,str(BASE_DIR.parent/"rongzhai_suibi"))
from make_pdfs import print_one
p=argparse.ArgumentParser();p.add_argument("--sequence",type=int,action="append");a=p.parse_args()
with (BASE_DIR/"catalog.csv").open(encoding="utf-8-sig",newline="") as f:rows=list(csv.DictReader(f))
if a.sequence:rows=[r for r in rows if int(r["sequence"]) in set(a.sequence)]
for r in rows:
    target=BASE_DIR/f"{int(r['sequence']):02d}_{r['slug']}";print_one(target/"editor.html",target/f"laozi_{int(r['sequence']):02d}_annotated.pdf")
