(()=>{
  const editor=document.getElementById('editor'),status=document.getElementById('saveStatus');
  if(!editor)return;
  const key=`news-report-editor-v1:${location.pathname}`;let timer,voices=[];
  const setStatus=text=>{if(status)status.textContent=text};
  const save=()=>{localStorage.setItem(key,JSON.stringify({html:editor.innerHTML,updated:new Date().toISOString()}));setStatus('Saved in this browser')};
  try{const saved=JSON.parse(localStorage.getItem(key)||'null');if(saved?.html){editor.innerHTML=saved.html;setStatus('Browser draft restored')}}catch{}
  editor.addEventListener('input',()=>{setStatus('Editing…');clearTimeout(timer);timer=setTimeout(save,500)});
  document.querySelectorAll('[data-command]').forEach(button=>button.addEventListener('click',()=>{editor.focus();document.execCommand(button.dataset.command,false,button.dataset.command==='hiliteColor'?'#ffe36e':null);editor.dispatchEvent(new Event('input',{bubbles:true}))}));
  toolbarToggle.onclick=()=>{const collapsed=toolbarToggle.closest('.toolbar').classList.toggle('collapsed');toolbarToggle.textContent=collapsed?'Expand toolbar':'Collapse toolbar';toolbarToggle.setAttribute('aria-expanded',String(!collapsed))};
  const selectionInEditor=()=>{const selection=getSelection();return selection?.rangeCount&&editor.contains(selection.anchorNode)?selection:null};
  const markSelection=(className,title='')=>{const selection=selectionInEditor();if(!selection||selection.isCollapsed){setStatus('Select text first');return}const range=selection.getRangeAt(0),span=document.createElement('span');span.className=className;if(title)span.title=title;try{range.surroundContents(span)}catch{span.append(range.extractContents());range.insertNode(span)}selection.removeAllRanges();save()};
  commentBtn.onclick=()=>{const note=prompt('Comment:','');if(note?.trim())markSelection('comment-anchor',note.trim())};
  doubtBtn.onclick=()=>markSelection('doubt','Check this passage');
  footnoteBtn.onclick=()=>{const note=prompt('Footnote:','');if(!note?.trim())return;const selection=selectionInEditor();if(!selection){setStatus('Place the cursor in the text');return}const sup=document.createElement('sup');sup.className='footnote-ref';sup.textContent='[note]';sup.title=note.trim();const range=selection.getRangeAt(0);range.collapse(false);range.insertNode(sup);save()};
  clearBtn.onclick=()=>{editor.focus();document.execCommand('removeFormat');editor.dispatchEvent(new Event('input',{bubbles:true}))};
  let matches=[],matchIndex=-1;const collect=()=>{matches=[];matchIndex=-1;const query=contentSearch.value.trim().toLowerCase();if(!query){searchStatus.textContent='';return}const walker=document.createTreeWalker(editor,NodeFilter.SHOW_TEXT);let node;while(node=walker.nextNode()){const value=node.nodeValue.toLowerCase();let start=0,index;while((index=value.indexOf(query,start))!==-1){const range=document.createRange();range.setStart(node,index);range.setEnd(node,index+query.length);matches.push(range);start=index+Math.max(1,query.length)}}searchStatus.textContent=matches.length?`${matches.length} matches`:'No matches'};
  const show=step=>{if(!matches.length)collect();if(!matches.length)return;matchIndex=(matchIndex+step+matches.length)%matches.length;const selection=getSelection();selection.removeAllRanges();selection.addRange(matches[matchIndex]);matches[matchIndex].startContainer.parentElement?.scrollIntoView({block:'center'});searchStatus.textContent=`${matchIndex+1}/${matches.length}`};
  contentSearch.oninput=collect;searchPrevBtn.onclick=()=>show(-1);searchNextBtn.onclick=()=>show(1);
  const loadVoices=()=>{voices=speechSynthesis.getVoices();const chosen=voiceSelect.value;voiceSelect.innerHTML='<option value="">System default voice</option>';voices.forEach((voice,index)=>voiceSelect.add(new Option(`${voice.name} (${voice.lang})`,String(index))));voiceSelect.value=chosen};loadVoices();speechSynthesis.addEventListener?.('voiceschanged',loadVoices);
  rate.oninput=()=>rateValue.textContent=`${Number(rate.value).toFixed(1)}×`;
  speakBtn.onclick=()=>{speechSynthesis.cancel();const utterance=new SpeechSynthesisUtterance(getSelection().toString().trim()||editor.innerText);utterance.lang='en-US';utterance.rate=Number(rate.value);utterance.voice=voices[Number(voiceSelect.value)]||null;speechSynthesis.speak(utterance)};
  pauseBtn.onclick=()=>speechSynthesis.paused?speechSynthesis.resume():speechSynthesis.pause();stopBtn.onclick=()=>speechSynthesis.cancel();
  const download=(name,text,type='text/plain;charset=utf-8')=>{const link=document.createElement('a');link.href=URL.createObjectURL(new Blob([text],{type}));link.download=name;link.click();setTimeout(()=>URL.revokeObjectURL(link.href),1000)};
  saveBtn.onclick=save;exportTxtBtn.onclick=()=>download(`${document.body.dataset.reportId}-edited.txt`,editor.innerText);exportJsonBtn.onclick=()=>download(`${document.body.dataset.reportId}-backup.json`,JSON.stringify({html:editor.innerHTML,pdf:document.body.dataset.pdf,savedAt:new Date().toISOString()},null,2),'application/json');
  importJson.onchange=async event=>{const file=event.target.files[0];if(!file)return;try{const data=JSON.parse(await file.text());if(typeof data.html!=='string')throw Error();editor.innerHTML=data.html;save()}catch{setStatus('Invalid backup file')}finally{event.target.value=''}};
})();
