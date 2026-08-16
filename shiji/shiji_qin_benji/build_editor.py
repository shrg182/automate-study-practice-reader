#!/usr/bin/env python3
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parent / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))
from build_editor import build_html, load_terms

if __name__ == "__main__":
    text = (BASE_DIR / "qin_benji_clean.txt").read_text(encoding="utf-8")
    terms = load_terms(BASE_DIR / "reading_terms.csv")
    output = build_html(
        text,
        terms,
        "https://www.guwendao.net/guwen/bookv_cab5e2fff7da.aspx",
        chapter_title="十二本纪·秦本纪第五",
        editor_title="《史记·秦本纪》校读编辑器",
        storage_key="shiji-qin-benji-editor-v1",
        file_stem="qin_benji",
    )
    (BASE_DIR / "editor.html").write_text(output, encoding="utf-8")
    print(f"Output: {BASE_DIR / 'editor.html'}\nCharacters: {len(text)}\nTerms: {len(terms)}")
