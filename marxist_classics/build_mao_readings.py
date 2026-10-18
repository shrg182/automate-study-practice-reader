#!/usr/bin/env python3
"""Build the two Mao readings from archived GB18030 source pages."""
from pathlib import Path
import html
import re
import sys
from bs4 import BeautifulSoup
BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent / 'shiji/shiji_lisheng_lujia'))
from build_editor import build_html, load_global_terms

BOOKS = [('on_practice', '实践论', '193707', '1937年7月'),
         ('on_contradiction', '矛盾论', '193708', '1937年8月')]

def build(slug, title, date, label):
    folder = BASE / slug
    soup = BeautifulSoup((folder / 'sources/original.htm').read_bytes().decode('gb18030'), 'html.parser')
    notes = []
    for anchor in soup.select('a[name]'):
        name = anchor['name']
        if not re.fullmatch(r'_ftn\d+', name):
            continue
        parts = []
        for sibling in anchor.next_siblings:
            if getattr(sibling, 'name', None) == 'br':
                break
            parts.append(sibling.get_text() if hasattr(sibling, 'get_text') else str(sibling))
        notes.append({'id': name[1:], 'note': ''.join(parts).strip(), 'mediaIds': []})
    first = soup.select_one('p.title1')
    pieces = []
    for sibling in first.next_siblings:
        if getattr(sibling, 'name', None) == 'hr':
            break
        pieces.append(str(sibling))
    body = BeautifulSoup(''.join(pieces), 'html.parser')
    for anchor in body.select('a[href]'):
        match = re.fullmatch(r'#_ftn(\d+)', anchor['href'])
        if match:
            n = match[1]
            sup = body.new_tag('sup', attrs={'class': 'footnote-ref', 'data-note-id': 'ftn'+n, 'contenteditable': 'false'})
            sup.string = '〔'+n+'〕'
            anchor.replace_with(sup)
    # Source paragraphs are separated by BR, including direct text nodes.
    for br in body.find_all('br'):
        br.replace_with('\n')
    for tag in body.find_all(['p','h3','blockquote']):
        tag.insert_before('\n');tag.insert_after('\n')
    allowed = {'sup'}
    for tag in list(body.find_all(True)):
        if tag.name not in allowed:
            tag.unwrap()
    lines = [line.strip() for line in str(body).splitlines() if line.strip()]
    content = '\n'.join(f'<p data-paragraph="{i}">{line}</p>' for i,line in enumerate(lines,1))
    text = BeautifulSoup(content,'html.parser').get_text('\n')
    global_terms = load_global_terms(BASE.parents[1] / 'project_dictionary/dictionary.csv', text, [])
    url = f'https://www.marxists.org/chinese/maozedong/marxist.org-chinese-mao-{date}.htm'
    output = build_html(text, [], url, chapter_title=f'《{title}》', editor_title=f'《{title}》校读编辑器',
        storage_key=f'mao-{slug.replace("_","-")}-editor-v1', file_stem=slug,
        global_terms=global_terms, shared_library_href='', source_site_label='中文马克思主义文库',
        editor_seed={'bodyHTML':content,'terms':[],'footnotes':notes})
    (folder/'editor.html').write_text(output)
    (folder/'source.txt').write_text(text+'\n\n注释\n'+ '\n'.join(n['id']+': '+n['note'] for n in notes)+'\n')
    (folder/'README.md').write_text(f'# 《{title}》\n\n毛泽东 · {label}\n\n来源：{url}\n\n保留原站正文、编者说明与{len(notes)}条注释。原始网页以 GB18030 保存于 sources/original.htm。\n重新生成：`.venv/bin/python practice/marxist_classics/build_mao_readings.py`。\n')
    assert len(text)>5000 and notes and all(n['note'] for n in notes)
    print(title, len(lines), 'paragraphs,', len(notes), 'notes')

if __name__ == '__main__':
    for book in BOOKS: build(*book)
