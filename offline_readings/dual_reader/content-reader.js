/* Local text/Markdown rendering. Source HTML stays literal; no source scripts run. */
(() => {
  'use strict';
  const element = (tag, text) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    return node;
  };
  function inline(parent, source) {
    const pattern = /(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*|\[[^\]]+\]\([^\s)]+\))/g;
    let previous = 0;
    for (const match of source.matchAll(pattern)) {
      parent.append(document.createTextNode(source.slice(previous, match.index)));
      const token = match[0];
      if (token.startsWith('`')) parent.append(element('code', token.slice(1, -1)));
      else if (token.startsWith('**')) parent.append(element('strong', token.slice(2, -2)));
      else if (token.startsWith('*')) parent.append(element('em', token.slice(1, -1)));
      else {
        const [, label, href] = token.match(/^\[([^\]]+)\]\((.+)\)$/);
        if (/^(https?:\/\/|mailto:)/i.test(href)) {
          const link = element('a', label);
          link.href = href; link.target = '_blank'; link.rel = 'noopener noreferrer';
          parent.append(link);
        } else parent.append(document.createTextNode(label));
      }
      previous = match.index + token.length;
    }
    parent.append(document.createTextNode(source.slice(previous)));
  }
  function markdown(source) {
    const root = element('article');
    let paragraph = [], list = null, code = null;
    const flush = () => {
      if (!paragraph.length) return;
      const p = element('p'); inline(p, paragraph.join(' ')); root.append(p); paragraph = [];
    };
    for (const line of source.replace(/\r\n?/g, '\n').split('\n')) {
      if (/^\s*```/.test(line)) {
        flush(); list = null;
        if (code) code = null;
        else { const pre = element('pre'); code = element('code'); pre.append(code); root.append(pre); }
        continue;
      }
      if (code) { code.append(document.createTextNode(line + '\n')); continue; }
      const heading = line.match(/^(#{1,6})\s+(.+)$/), item = line.match(/^\s*(?:([-+*])|\d+\.)\s+(.+)$/);
      if (!line.trim()) { flush(); list = null; }
      else if (heading) { flush(); list = null; const h = element('h' + heading[1].length); inline(h, heading[2]); root.append(h); }
      else if (item) {
        flush(); const tag = item[1] ? 'UL' : 'OL';
        if (!list || list.tagName !== tag) { list = element(tag.toLowerCase()); root.append(list); }
        const li = element('li'); inline(li, item[2]); list.append(li);
      } else if (/^>\s?/.test(line)) { flush(); list = null; const q = element('blockquote'); inline(q, line.replace(/^>\s?/, '')); root.append(q); }
      else if (/^\s*(---+|\*\*\*+)\s*$/.test(line)) { flush(); list = null; root.append(element('hr')); }
      else { list = null; paragraph.push(line); }
    }
    flush(); return root;
  }
  window.OpenBooksContent = {markdown};
})();
