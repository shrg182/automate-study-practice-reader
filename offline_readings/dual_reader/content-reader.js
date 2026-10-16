/* Local reading views: literal text, basic Markdown, and allowlisted static HTML. */
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
  function html(source) {
    // Template contents are inert: source resources never enter the live document.
    const template = document.createElement('template'); template.innerHTML = source;
    const root = element('article'), anchors = new Map(), pending = [];
    const allowed = new Set('article section main header footer nav aside div span p h1 h2 h3 h4 h5 h6 ul ol li dl dt dd blockquote pre code strong b em i u s del ins mark small sub sup br hr table caption thead tbody tfoot tr th td colgroup col figure figcaption a img abbr time address'.split(' '));
    const discard = new Set('script style link meta base title iframe frame frameset object embed template noscript svg math canvas audio video source track input textarea select button option'.split(' '));
    const copy = (node, parent) => {
      if (node.nodeType === Node.TEXT_NODE) { parent.append(document.createTextNode(node.textContent)); return; }
      if (node.nodeType !== Node.ELEMENT_NODE) return;
      const tag = node.localName.toLowerCase();
      if (discard.has(tag)) return;
      if (!allowed.has(tag)) { for (const child of node.childNodes) copy(child, parent); return; }
      if (tag === 'img') {
        const src = node.getAttribute('src') || '', alt = node.getAttribute('alt') || 'Image';
        if (/^data:image\/(png|jpe?g|webp|gif);base64,[a-z0-9+/=\s]+$/i.test(src)) {
          const image = element('img'); image.alt = alt; image.src = src; parent.append(image);
        } else parent.append(element('span', `[${alt} — image not embedded in this file]`));
        return;
      }
      const target = element(tag);
      const id = node.getAttribute('id');
      if (id && !anchors.has(id)) anchors.set(id, target);
      for (const attr of ['title', 'lang']) if (node.hasAttribute(attr)) target.setAttribute(attr, node.getAttribute(attr));
      const dir = node.getAttribute('dir'); if (['ltr', 'rtl', 'auto'].includes(dir)) target.dir = dir;
      for (const attr of ['colspan', 'rowspan']) if (/^\d{1,2}$/.test(node.getAttribute(attr) || '')) target.setAttribute(attr, node.getAttribute(attr));
      if (tag === 'a') {
        const href = (node.getAttribute('href') || '').trim();
        if (/^(https?:\/\/|mailto:)/i.test(href)) { target.href = href; target.target = '_blank'; target.rel = 'noopener noreferrer'; }
        else if (href.startsWith('#')) pending.push({target, fragment: href.slice(1)});
      }
      for (const child of node.childNodes) copy(child, target);
      parent.append(target);
    };
    for (const child of template.content.childNodes) copy(child, root);
    for (const {target, fragment} of pending) {
      let key; try { key = decodeURIComponent(fragment); } catch { continue; }
      const destination = anchors.get(key);
      if (destination) { target.href = '#'; target.onclick = event => { event.preventDefault(); destination.scrollIntoView({block: 'start'}); }; }
    }
    return root;
  }
  window.OpenBooksContent = {markdown, html};
})();
