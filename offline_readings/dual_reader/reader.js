(()=>{'use strict';
const $=s=>document.querySelector(s),remember=$('#remember'),storageStatus=$('#storageStatus'),controllers=[];
function database(){return new Promise((resolve,reject)=>{const request=indexedDB.open('open-books-offline',1);request.onupgradeneeded=()=>request.result.createObjectStore('books');request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error)})}
async function stored(action,key,value){if(action==='put')value={name:value.name,type:value.type,bytes:await value.arrayBuffer()};const db=await database();try{return await new Promise((resolve,reject)=>{const tx=db.transaction('books',action==='get'?'readonly':'readwrite'),store=tx.objectStore('books');const request=action==='get'?store.get(key):action==='put'?store.put(value,key):store.delete(key);tx.oncomplete=()=>{const result=request.result;resolve(action==='get'&&result?.bytes?new File([result.bytes],result.name,{type:result.type}):result)};tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error)})}finally{db.close()}}
function storageError(){storageStatus.textContent='Browser storage is unavailable or full. You can still read; reattach books next time.'}
try{remember.checked=localStorage.getItem('open-books-remember')!=='false'}catch{storageError()}
for(const side of ['left','right']){
 const pane=$('#paneTemplate').content.firstElementChild.cloneNode(true);$('#panes').append(pane);const q=s=>pane.querySelector(s);q('h2').textContent=side==='left'?'Left pane':'Right pane';q('.pdf').title=`${side} PDF reader`;
 let book,rendition,url,file,currentFormat,generation=0,saveQueue=Promise.resolve();
 function save(value){saveQueue=saveQueue.catch(()=>{}).then(()=>stored(value?'put':'delete',side,value)).then(()=>true).catch(()=>{storageError();return false});return saveQueue}
 function cleanup(){rendition?.destroy();book?.destroy();rendition=book=null;if(url)URL.revokeObjectURL(url);url=null;q('.pdf').onload=null;q('.pdf').removeAttribute('src');q('.epub').replaceChildren();q('.toc').replaceChildren();q('.pdf').hidden=q('.epub').hidden=q('.controls').hidden=true;q('.empty').hidden=false;q('.remove').disabled=true}
 function resize(){if(rendition?.manager?.isRendered()&&rendition.location&&q('.epub').clientWidth)rendition.resize(q('.epub').clientWidth,q('.epub').clientHeight)}
 async function open(nextFile,persist=true){
  const format=nextFile.name.toLowerCase().endsWith('.epub')?'epub':nextFile.name.toLowerCase().endsWith('.pdf')?'pdf':null;if(!format){q('.status').textContent='Please choose a PDF or EPUB.';return}
  const version=++generation;cleanup();file=nextFile;currentFormat=format;q('.status').textContent=`Opening ${file.name}…`;q('.page').value=1;
  try{
   q('.empty').hidden=true;q('.controls').hidden=false;q('.pageForm').hidden=format==='epub';q('.tocLabel').hidden=format!=='epub';
   if(format==='pdf'){url=URL.createObjectURL(file);q('.pdf').hidden=false;if(location.protocol==='file:')q('.pdf').src=url+'#page=1&view=FitH';else{q('.pdf').src='pdf-viewer.html'}}
   else{
    q('.epub').hidden=false;const ownBook=ePub();book=ownBook;const bytes=await file.arrayBuffer();if(version!==generation)return;await ownBook.open(bytes,'binary');if(version!==generation)return;
    const navigation=await ownBook.loaded.navigation;if(version!==generation)return;
    function add(items,depth=0){for(const item of items){q('.toc').add(new Option('  '.repeat(depth)+item.label.trim(),item.href));add(item.subitems||[],depth+1)}}add(navigation.toc||[]);
    if(!q('.toc').options.length)ownBook.spine.spineItems.forEach((item,i)=>q('.toc').add(new Option(`Section ${i+1}`,item.href)));
    rendition=ownBook.renderTo(q('.epub'),{width:'100%',height:'100%',manager:'continuous',flow:'scrolled',spread:'none'});
    rendition.themes.default({body:{'font-size':'18px','line-height':'1.6',padding:'20px',color:'#24241f',background:'#fff'},img:{'max-width':'100%'}});
    rendition.on('relocated',location=>{if(version!==generation)return;const section=ownBook.spine.get(location.start.index);if(section){if(![...q('.toc').options].some(option=>option.value===section.href))q('.toc').add(new Option(`Section ${location.start.index+1}`,section.href));q('.toc').value=section.href;}q('.status').textContent=`${nextFile.name} · Section ${location.start.index+1} of ${ownBook.spine.spineItems.length}`});
    await rendition.display();if(version!==generation)return;
   }
   q('.remove').disabled=false;if(format==='pdf')q('.status').textContent=file.name;if(persist){if(remember.checked)await save(nextFile);else await save(null)}
  }catch(error){if(version!==generation)return;cleanup();file=null;q('.status').textContent=`Could not open ${nextFile.name}. Try another file.`;console.warn(error)}
 }
 function go(page){q('.page').value=Math.max(1,Number(page)||1);if(url){if(location.protocol==='file:')q('.pdf').src=url+`#page=${q('.page').value}&view=FitH`;else q('.pdf').contentWindow.postMessage({type:'PDF_PAGE',page:Number(q('.page').value)},location.origin)}}
 q('.file').onchange=event=>{const next=event.target.files[0];event.target.value='';if(next)open(next)};
 q('.pageForm').onsubmit=event=>{event.preventDefault();go(q('.page').value)};
 q('.prev').onclick=()=>currentFormat==='epub'?rendition?.prev():go(Number(q('.page').value)-1);q('.next').onclick=()=>currentFormat==='epub'?rendition?.next():go(Number(q('.page').value)+1);
 q('.toc').onchange=()=>rendition?.display(q('.toc').value);
 q('.remove').onclick=async()=>{++generation;cleanup();file=null;q('.status').textContent='No book attached';await save(null)};
 q('.fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await pane.requestFullscreen();resize()}catch{q('.status').textContent='Full screen is unavailable in this browser.'}};
 window.addEventListener('message',event=>{if(event.origin!==location.origin||event.source!==q('.pdf').contentWindow||currentFormat!=='pdf'||!file)return;const data=event.data;if(data?.type==='PDF_READY')q('.pdf').contentWindow.postMessage({type:'OPEN_PDF',file},location.origin);if(data?.type==='PDF_LOCATION'){q('.page').value=data.page;q('.page').max=data.total;q('.status').textContent=`${file.name} · Page ${data.page} of ${data.total} · Fit to width`}if(data?.type==='PDF_ERROR')q('.status').textContent=data.message});
 new ResizeObserver(resize).observe(q('.epub'));controllers.push({saveCurrent:()=>save(remember.checked?file:null),resize});
 if(remember.checked){const version=generation;stored('get',side).then(value=>{if(value&&version===generation)open(value,false)}).catch(storageError)}
}
remember.onchange=async()=>{try{localStorage.setItem('open-books-remember',String(remember.checked))}catch{storageError()}const results=await Promise.all(controllers.map(c=>c.saveCurrent()));if(results.some(result=>!result))return;storageStatus.textContent=remember.checked?'Books are saved in this browser when storage is available.':'Saved copies cleared. Open books remain available for this session.'};
$('#layout').onchange=event=>{$('#panes').dataset.layout=event.target.value;requestAnimationFrame(()=>controllers.forEach(c=>c.resize()))};
// Cache the reader shell and bundled EPUB libraries; book bytes stay in IndexedDB.
if(location.protocol!=='file:'&&'serviceWorker' in navigator){
 navigator.serviceWorker.addEventListener('message',event=>{if(event.data?.type==='ARTICLE_CACHED')$('#offlineStatus').textContent='Reader available offline';if(event.data?.type==='CACHE_ERROR')$('#offlineStatus').textContent='Open online again to prepare offline reading'});
 navigator.serviceWorker.register(new URL('../../service-worker.js',location.href),{scope:new URL('../../',location.href).pathname}).then(()=>navigator.serviceWorker.ready).then(registration=>{
  const paths=['editor.html','reader.css','reader.js','pdf-viewer.html','pdf-viewer.js','../../vendor/jszip/jszip.min.js','../../vendor/epubjs/epub.min.js'];
  return fetch('../../vendor/pdfjs/assets.json').then(response=>{if(!response.ok)throw Error('PDF assets unavailable');return response.json()}).then(assets=>{paths.push('../../vendor/pdfjs/assets.json',...assets.map(path=>'../../vendor/pdfjs/'+path));
  registration.active?.postMessage({type:'CACHE_ARTICLE',urls:paths.map(path=>new URL(path,location.href).href)});});
 }).catch(()=>{$('#offlineStatus').textContent='Offline setup unavailable; keep this page open to read'});
}
})();
