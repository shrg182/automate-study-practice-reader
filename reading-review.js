/* Read-only review of saved article records. Source HTML is parsed inertly. */
(function () {
  'use strict';
  if(window.ReadingReview)return;
  const root = new URL('.', document.currentScript.src), registryKey = 'reading-review-books-v1';
  const labels = {annotation:'注音与注释',inline:'行间注',comment:'按语',footnote:'脚注',note:'札记',highlight:'高亮与划线',doubt:'待核',vocabulary:'词汇',edit:'编辑记录'};
  const selectors = {annotation:'.notation',inline:'.interlinear-note',comment:'.comment-block',footnote:'.footnote-ref',highlight:'mark,[style*="background-color"],u,[style*="underline"]',doubt:'.doubt,.review-resolved'};
  let current = null, dialog, items = [], returnFocus;
  const read = (key, fallback) => { try { const value=JSON.parse(localStorage.getItem(key));return value===null?fallback:value; } catch { return fallback; } };
  const arr = value => Array.isArray(value)?value:[];
  const node = (tag, text) => { const el=document.createElement(tag);if(text!==undefined)el.textContent=text;return el; };
  const plain = element => { const clone=element.cloneNode(true);clone.querySelectorAll('rt,script,style').forEach(el=>el.remove());return clone.textContent.trim(); };
  function records(book, data) {
    const template=document.createElement('template');template.innerHTML=typeof data.bodyHTML==='string'?data.bodyHTML:'';
    const content=template.content, result=[];
    const add=(type,text,source='',index=0,time='',media=[])=>result.push({book,type,text:String(text||''),source:String(source||''),index,time,media:arr(media).length});
    for(const [type,selector] of Object.entries(selectors)) {
      if(type==='footnote')continue;
      [...content.querySelectorAll(selector)].forEach((el,index)=>{
        const source=plain(el),text=type==='comment'?source:el.dataset.note||el.dataset.issue||el.querySelector('rt')?.textContent||'';
        add(type,text,source,index);
      });
    }
    arr(data.footnotes).forEach((item,index)=>{const anchor=[...content.querySelectorAll('.footnote-ref')].find(el=>el.dataset.noteId===item.id);add('footnote',item.note,anchor?.parentElement?plain(anchor.parentElement):'',index,'',item.mediaIds);});
    const separateNotes=read(book.notesKey,null),suppressed=new Set(arr(read(book.notesKey+'-suppressed-v1',[])));
    arr(separateNotes===null?data.notes:separateNotes).filter(item=>!suppressed.has(`${item.time}\u0000${item.text}`)).forEach((item,index)=>add('note',item.text,'',index,item.editedAt||item.time,item.mediaIds));
    arr(data.terms).forEach((item,index)=>add('vocabulary',[item.pinyin,item.annotation].filter(Boolean).join(' · '),item.term,index));
    const separateLog=read(book.logKey,null);
    arr(separateLog===null?data.log:separateLog).forEach((item,index)=>add('edit',[item.action,item.detail].filter(Boolean).join(' · '),'',index,item.time));
    const ordered=[...content.querySelectorAll('*')];
    for(const item of result){
      let target=selectors[item.type]?content.querySelectorAll(selectors[item.type])[item.index]:null;
      if(item.type==='footnote'){const id=arr(data.footnotes)[item.index]?.id;target=[...content.querySelectorAll('.footnote-ref')].find(el=>el.dataset.noteId===id);}
      item.order=target?ordered.indexOf(target):ordered.length+item.index;
    }
    result.sort((a,b)=>a.order-b.order);
    return result;
  }
  function identifyCurrent() {
    try {
      if(typeof STORAGE_KEY==='undefined'||typeof state!=='function'||!document.querySelector('#editor'))return null;
      return {key:STORAGE_KEY,notesKey:typeof NOTES_KEY==='string'?NOTES_KEY:STORAGE_KEY+'-notes-v1',logKey:typeof LOG_KEY==='string'?LOG_KEY:STORAGE_KEY+'-log-v1',title:document.querySelector('h1')?.textContent.trim()||document.title,path:location.href.split('?')[0].split('#')[0]};
    } catch { return null; }
  }
  function books() {
    const map=new Map();
    for(const book of [...arr(window.ReadingReviewCatalog),...arr(read(registryKey,[]))])if(book&&typeof book.key==='string')map.set(book.key,book);
    if(current)map.set(current.key,current);
    return [...map.values()];
  }
  function collect() {
    const result=[];
    for(const book of books()) {
      let data=read(book.key,null);
      if(current?.key===book.key){try{data=state();}catch{}}
      if(!data&&(localStorage.getItem(book.notesKey)||localStorage.getItem(book.logKey)))data={};
      if(data&&typeof data==='object')result.push(...records(book,data));
    }
    return result;
  }
  function locate(item) {
    const elRoot=document.querySelector('#editor');let target;
    if(selectors[item.type])target=elRoot?.querySelectorAll(selectors[item.type])[item.index];
    if(item.type==='footnote')target=document.querySelectorAll('#footnoteList .footnote-item')[item.index];
    if(item.type==='note')target=document.querySelectorAll('#userNoteList .note-item, #notesList .note-item, #readingNotesList .note-item')[item.index];
    if(item.type==='vocabulary')target=[...(elRoot?.querySelectorAll('.notation')||[])].find(el=>(el.dataset.term||plain(el))===item.source);
    if(item.type==='edit')target=document.querySelector('#editLogList');
    target ||= elRoot;
    if(target){target.scrollIntoView({block:'center'});target.animate([{outline:'3px solid #d28a16'},{outline:'3px solid transparent'}],{duration:2200});}
  }
  function openOriginal(item) {
    if(current?.key===item.book.key){dialog.close();locate(item);return;}
    const url=new URL(item.book.path,root);if(!['http:','https:','file:'].includes(url.protocol))return;
    if(url.origin!==root.origin||!url.pathname.startsWith(root.pathname))return;
    url.searchParams.set('view','annotated');url.searchParams.set('reviewType',item.type);url.searchParams.set('reviewIndex',item.index);url.searchParams.set('reviewSource',item.source);location.href=url.href;
  }
  function render() {
    const q=dialog.querySelector('[data-search]').value.trim().toLowerCase(),book=dialog.querySelector('[data-book]').value,type=dialog.querySelector('[data-type]').value,from=dialog.querySelector('[data-from]').value,to=dialog.querySelector('[data-to]').value;
    let filtered=items.filter(item=>(!book||item.book.key===book)&&(!type||item.type===type)&&(!q||[item.text,item.source,item.book.title].join(' ').toLowerCase().includes(q))&&(!from||item.time&&item.time.slice(0,10)>=from)&&(!to||item.time&&item.time.slice(0,10)<=to));
    if(dialog.querySelector('[data-sort]').value==='recent')filtered.sort((a,b)=>(b.time||'').localeCompare(a.time||''));
    const list=dialog.querySelector('[data-results]');list.replaceChildren();dialog.querySelector('[data-count]').textContent=`${filtered.length} 条记录`;
    for(const item of filtered){const row=node('article');row.className='review-item';row.append(node('h3',`${labels[item.type]} · ${item.book.title}`));if(item.source)row.append(node('blockquote',item.source));row.append(node('p',item.text||'仅标记，未填写说明'));const valid=item.time&&!Number.isNaN(Date.parse(item.time));row.append(node('small',valid?new Date(item.time).toLocaleString():'日期不详'));if(item.media)row.append(node('p',`${item.media} 个附件 · 在原文中查看`));const link=node('button','打开原文');link.type='button';link.onclick=()=>openOriginal(item);row.append(link);list.append(row);}
    if(!filtered.length)list.append(node('p','没有符合条件的记录。打开并保存文章后，可在这里回顾其笔记。'));
  }
  function open(all) {
    returnFocus=document.activeElement;
    if(!dialog){
      dialog=node('dialog');dialog.className='reading-review';dialog.setAttribute('aria-labelledby','readingReviewTitle');
      dialog.innerHTML='<header><h2 id="readingReviewTitle">阅读回顾 · Reading review</h2><button type="button" data-close aria-label="关闭阅读回顾">关闭</button></header><p>此浏览器保存的文章记录；未保存的其他书籍不在此列表中。附件请在原文中查看。日期筛选只包含有日期的记录。</p><div class="review-filters"><input data-search type="search" placeholder="搜索笔记、原文或书名" aria-label="搜索回顾"><select data-book aria-label="书籍"><option value="">全部书籍</option></select><select data-type aria-label="笔记类型"><option value="">全部类型</option></select><label>从 <input type="date" data-from></label><label>至 <input type="date" data-to></label><select data-sort aria-label="排序"><option value="book">按书籍与原文顺序</option><option value="recent">最新记录优先</option></select><button type="button" data-refresh>刷新</button></div><p data-count role="status"></p><div data-results></div>';
      dialog.querySelector('[data-close]').onclick=()=>dialog.close();dialog.addEventListener('close',()=>returnFocus?.focus());dialog.querySelectorAll('input,select').forEach(el=>el.addEventListener('input',render));dialog.querySelector('[data-refresh]').onclick=()=>{items=collect();render();};
      for(const [value,label] of Object.entries(labels)){const opt=node('option',label);opt.value=value;dialog.querySelector('[data-type]').append(opt);}document.body.append(dialog);
    }
    if(!dialog.querySelector('[data-published-reading]')){const link=node('a','载入 iMac 最新发布数据');link.dataset.publishedReading='';link.href=new URL('sync/index.html?published=1',root).href;dialog.querySelector('header').after(link);}
    items=collect();const select=dialog.querySelector('[data-book]');select.replaceChildren(new Option('全部书籍',''));const unique=new Map(items.map(item=>[item.book.key,item.book]));for(const book of unique.values())select.add(new Option(book.title,book.key));select.value=!all&&current?current.key:'';render();dialog.showModal();dialog.querySelector('[data-search]').focus();
  }
  function init() {
    current=identifyCurrent();
    const css=node('link');css.rel='stylesheet';css.href=new URL('reading-review.css',root);document.head.append(css);
    const host=document.querySelector('.toolbar,.topbar,.masthead-inner')||document.querySelector('header');if(!host)return;
    const button=node('button','阅读回顾');button.type='button';button.dataset.readingReview='';button.onclick=()=>open(!current);host.append(button);
    if(current){try{const registered=arr(read(registryKey,[])).filter(book=>book.key!==current.key);registered.push(current);localStorage.setItem(registryKey,JSON.stringify(registered));}catch{}
      const params=new URLSearchParams(location.search),type=params.get('reviewType'),index=Number(params.get('reviewIndex'));if(labels[type]&&Number.isInteger(index)&&index>=0)setTimeout(()=>locate({type,index,source:params.get('reviewSource')||''}),100);
    }
  }
  window.ReadingReview={open,records,collect};if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
