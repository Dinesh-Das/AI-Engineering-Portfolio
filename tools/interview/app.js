const main = document.getElementById('main');
function closeMenu() {
  document.getElementById('sidebar').classList.remove('is-open');
  document.getElementById('menu-toggle').setAttribute('aria-expanded','false');
  main.inert=false;
}
function render(moveFocus=false, focusID='') {
  const views={home:homeView,projects:projectsView,topics:topicsView,project:()=>projectView(projects.get(route.id)),topic:()=>topicView(topics.get(route.id)),search:searchView,practice:practiceView,labs:labsView,revision:revisionView,about:aboutView};
  main.innerHTML=(views[route.view]||notFound)();
  const sectionNames={home:'START HERE',projects:'PROJECT ATLAS',project:'PROJECT ATLAS',topics:'INTERVIEW HANDBOOK',topic:'INTERVIEW HANDBOOK',practice:'PRACTICE ROOM',labs:'WORK THE NUMBERS',revision:'MY REVISION',search:'SEARCH',about:'ABOUT'};
  document.getElementById('current-section').textContent=sectionNames[route.view]||'REFERENCE';
  document.querySelectorAll('[data-nav]').forEach(a=>{
    const active=a.dataset.nav===(route.view==='project'?'projects':route.view==='topic'?'topics':route.view);
    if(active)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');
  });
  progress();
  if(route.view==='labs') updateLabs();
  document.title=(route.view==='project'&&projects.has(route.id)?route.id:route.view==='topic'&&topics.has(route.id)?topics.get(route.id).title:sectionNames[route.view]||'The Field Manual')+' · AI Engineer';
  if(focusID) document.getElementById(focusID)?.focus({preventScroll:true});
  else if(moveFocus){document.getElementById('page-title')?.focus({preventScroll:true});window.scrollTo({top:0,behavior:'instant'});}
}
function readRoute(moveFocus=true) {
  const previous=route.view;
  route=Object.fromEntries(new URLSearchParams(location.hash.slice(1)));
  route.view=route.view||'home';
  if(previous==='practice'&&route.view!=='practice')stopTimer();
  if(route.view==='practice'&&previous!=='practice'){practice.index=0;practice.revealed=false;practice.remaining=120;}
  document.getElementById('global-search').value=route.view==='search'?(route.q||''):'';
  closeMenu();
  render(moveFocus);
}
function navigate(view,options={},replace=false,moveFocus=true) {
  const hash=href(view,options);
  if(replace||location.hash===hash){history.replaceState(null,'',hash);readRoute(moveFocus);}
  else location.hash=hash;
}
window.addEventListener('hashchange',()=>readRoute(true));
document.getElementById('project-count').textContent=DATA.projects.length;
document.getElementById('menu-toggle').addEventListener('click',()=>{
  const opening=document.getElementById('menu-toggle').getAttribute('aria-expanded')!=='true';
  document.getElementById('menu-toggle').setAttribute('aria-expanded',String(opening));
  document.getElementById('sidebar').classList.toggle('is-open',opening);
  main.inert=opening;
});
window.addEventListener('resize',()=>{if(window.innerWidth>720)closeMenu();});
document.addEventListener('keydown',event=>{
  if(event.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(event.target.tagName)&&!event.target.isContentEditable){event.preventDefault();document.getElementById('global-search').focus();}
  if(event.key==='Escape'){
    if(document.getElementById('sidebar').classList.contains('is-open')){closeMenu();document.getElementById('menu-toggle').focus();}
    else if(event.target.id==='global-search'&&event.target.value){event.target.value='';clearTimeout(searchTimer);navigate('home',{},true,false);event.target.focus();}
  }
});
document.getElementById('global-search').addEventListener('input',event=>{
  if(event.isComposing)return;
  const query=event.target.value.slice(0,500);
  clearTimeout(searchTimer);
  searchTimer=setTimeout(()=>navigate(query.trim()?'search':'home',query.trim()?{q:query}:{},true,false),120);
});
function localFilter(options,focusID) {
  route={...route,...options};
  history.replaceState(null,'',href(route.view,Object.fromEntries(Object.entries(route).filter(([key])=>key!=='view'))));
  render(false,focusID);
  const count=document.querySelector('.result-count');
  if(count)announce(count.textContent);
}
document.addEventListener('change',event=>{
  const element=event.target;
  if(element.id==='category-filter')localFilter({category:element.value},element.id);
  if(element.id==='project-status-filter')localFilter({status:element.value},element.id);
  if(element.id==='topic-group-filter')localFilter({group:element.value},element.id);
  if(element.id==='guide-select')localFilter({doc:element.value},element.id);
  if(['practice-level','practice-source'].includes(element.id)){
    stopTimer();practice.index=0;practice.revealed=false;practice.remaining=120;
    if(element.id==='practice-level')practice.level=element.value;else practice.source=element.value;
    render(false,element.id);announce(`${questionPool().length} questions in this selection.`);
  }
});
document.addEventListener('input',event=>{
  const element=event.target;
  if(element.dataset.noteKey){
    const key=element.dataset.noteKey;
    const others=Object.entries(study.notes).reduce((sum,[id,value])=>sum+(id===key?0:value.length),0);
    const allowed=Math.max(0,Math.min(20000,2000000-others));
    if(element.value.length>allowed){element.value=element.value.slice(0,allowed);announce('The note budget has been reached. Export a backup and shorten an earlier note.');}
    study.notes[key]=element.value;
    clearTimeout(noteTimer);
    const status=document.getElementById('note-status');
    if(status)status.textContent='Saving…';
    noteTimer=setTimeout(()=>{const saved=persist();const current=document.getElementById('note-status');if(current)current.textContent=saved?'Saved in this browser. Export a backup from My revision.':storageMessage;},250);
  }
  if(element.closest('.lab-panel'))updateLabs();
});
async function copyCode(button) {
  const code=button.closest('.code-block')?.querySelector('pre code');
  if(!code)return;
  try {
    if(!navigator.clipboard?.writeText)throw new Error('Clipboard unavailable');
    await navigator.clipboard.writeText(code.textContent);
    announce('Command/code copied. Read its working directory and prerequisites before running.');
  } catch(error) {
    const selection=window.getSelection(),range=document.createRange();
    range.selectNodeContents(code);selection.removeAllRanges();selection.addRange(range);code.closest('pre').focus();
    announce('Clipboard permission is unavailable. The code is selected; press Ctrl+C or Command+C to copy.');
  }
}
function focusAction(action,key) {
  [...main.querySelectorAll('[data-action]')].find(el=>el.dataset.action===action&&el.dataset.key===key)?.focus({preventScroll:true});
}
function exportStudy() {
  const data=JSON.stringify({...study,exportedAt:new Date().toISOString()},null,2);
  const url=URL.createObjectURL(new Blob([data],{type:'application/json'}));
  const anchor=document.createElement('a');anchor.href=url;anchor.download='ai-engineer-revision.json';document.body.append(anchor);anchor.click();anchor.remove();
  setTimeout(()=>URL.revokeObjectURL(url),1000);announce('Revision JSON exported. Keep it as your portable backup.');
}
document.getElementById('import-file').addEventListener('change',async event=>{
  const file=event.target.files[0];
  if(!file)return;
  try {
    if(file.size>16*1024*1024)throw new Error('Backup is too large (16 MiB limit).');
    const next=validateStudy(JSON.parse(await file.text()));
    study=next;const saved=persist();render(false);announce(saved?'Revision backup imported and saved locally.':storageMessage);
  } catch(error) {announce('Import rejected; existing revision is unchanged. '+error.message);}
  event.target.value='';
});
document.addEventListener('click',event=>{
  const skip=event.target.closest('.skip-link');
  if(skip){event.preventDefault();main.focus();return;}
  const button=event.target.closest('button[data-action]');
  if(!button)return;
  const action=button.dataset.action,key=button.dataset.key;
  if(action==='copy'){copyCode(button);return;}
  if(action==='print'){window.print();return;}
  if(action==='path'){
    route.path=button.dataset.path;
    document.querySelectorAll('[data-action=path]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
    document.getElementById('path-content').innerHTML=homePath(route.path);
    history.replaceState(null,'',href('home',{path:route.path}));return;
  }
  if(action==='bookmark'||action==='reviewed'){
    if(!itemIDs.has(key))return;
    const field=action==='bookmark'?'bookmarks':'reviewed';
    const exists=study[field].includes(key);
    study[field]=exists?study[field].filter(id=>id!==key):[...study[field],key];
    const saved=persist();render(false);focusAction(action,key);
    announce((action==='bookmark'?(exists?'Removed from saved revision.':'Saved for revision.'):(exists?'Review mark removed.':'Marked reviewed. This is a self-assessment.'))+(saved?'':' '+storageMessage));return;
  }
  if(action==='clear-search'){navigate('home');return;}
  if(action==='export'){exportStudy();return;}
  if(action==='import'){document.getElementById('import-file').click();return;}
  if(action==='reveal'){
    practice.revealed=!practice.revealed;render(false);
    main.querySelector('[data-action=reveal]')?.focus({preventScroll:true});
    announce(practice.revealed?'Answer rubric revealed. Compare your explanation before self-assessing.':'Answer hidden.');return;
  }
  if(action==='next-question'||action==='random-question'){
    const pool=questionPool();
    if(!pool.length)return;
    stopTimer();practice.remaining=120;practice.revealed=false;
    const previous=practice.index;
    practice.index=action==='next-question'?(previous+1)%pool.length:Math.floor(Math.random()*pool.length);
    if(pool.length>1&&practice.index===previous)practice.index=(previous+1)%pool.length;
    render(false);const heading=main.querySelector('.practice-card h2');heading?.setAttribute('tabindex','-1');heading?.focus({preventScroll:true});return;
  }
  if(action==='confidence'&&practice.revealed&&currentPractice){
    const id=currentPractice.type+':'+currentPractice.id;
    study.confidence[id]=button.dataset.value;
    if(practice.source==='review'&&button.dataset.value==='comfortable')practice.revealed=false;
    const saved=persist();render(false);announce('Self-assessment recorded.'+(saved?'':' '+storageMessage));return;
  }
  if(action==='reset-timer'){stopTimer();practice.remaining=120;render(false);main.querySelector('[data-action=reset-timer]')?.focus({preventScroll:true});return;}
  if(action==='timer'){
    if(practice.timer){stopTimer();render(false);return;}
    if(practice.remaining<=0)practice.remaining=120;
    practice.timer=setInterval(()=>{
      practice.remaining=Math.max(0,practice.remaining-1);
      const label=document.getElementById('practice-timer');if(label)label.textContent=formatTime(practice.remaining);
      if(practice.remaining===0){stopTimer();const control=main.querySelector('[data-action=timer]');if(control)control.textContent='Restart timer';announce('Two minutes are complete. Compare your answer with the rubric.');}
    },1000);
    render(false);main.querySelector('[data-action=timer]')?.focus({preventScroll:true});
  }
});
let printDetails=[];
window.addEventListener('beforeprint',()=>{printDetails=[...main.querySelectorAll('details:not([open])')];printDetails.forEach(d=>d.open=true);});
window.addEventListener('afterprint',()=>{printDetails.forEach(d=>d.open=false);printDetails=[];});
function updateLabs() {
  function result(id,calculate){
    const output=document.getElementById(id);if(!output)return;
    try{output.textContent=calculate();output.classList.remove('lab-error');}
    catch(error){output.textContent=error.message;output.classList.add('lab-error');}
  }
  result('metric-result',()=>{
    const [tp,fp,fn,tn]=['tp','fp','fn','tn'].map(n=>finiteField('metric-'+n,0,1e9,true));
    return `Precision = ${percent(ratio(tp,tp+fp))}\nRecall = ${percent(ratio(tp,tp+fn))}\nF1 = ${percent(ratio(2*tp,2*tp+fp+fn))}\nAccuracy = ${percent(ratio(tp+tn,tp+fp+fn+tn))}`;
  });
  result('rank-result',()=>{
    const ids=id=>[...new Set(document.getElementById(id).value.split(',').map(s=>s.trim()).filter(Boolean))];
    const gold=new Set(ids('rank-gold')),ranked=ids('rank-predicted');
    if(gold.size>100||ranked.length>100)throw new Error('Use at most 100 unique IDs in this worked example.');
    const k=finiteField('rank-k',1,100,true),cut=ranked.slice(0,k);
    const found=cut.filter(id=>gold.has(id)).length,first=cut.findIndex(id=>gold.has(id));
    const dcg=cut.reduce((sum,id,i)=>sum+(gold.has(id)?1/Math.log2(i+2):0),0);
    const ideal=Array.from({length:Math.min(k,gold.size)},(_,i)=>1/Math.log2(i+2)).reduce((a,b)=>a+b,0);
    const format=value=>value===null?'undefined (no relevant reference IDs)':value.toFixed(4);
    return `Recall@${k} = ${format(ratio(found,gold.size))}\nReciprocal rank@${k} = ${format(gold.size?(first<0?0:1/(first+1)):null)}\nBinary nDCG@${k} = ${format(ratio(dcg,ideal))}\nUnique relevant found = ${found} / ${gold.size}`;
  });
  result('kv-result',()=>{
    const l=finiteField('kv-layers',1,512,true),h=finiteField('kv-heads',1,1024,true),q=finiteField('kv-query-heads',1,1024,true),d=finiteField('kv-dimension',1,8192,true),t=finiteField('kv-tokens',1,1048576,true),b=finiteField('kv-bytes',.125,16),n=finiteField('kv-sequences',1,10000,true);
    const kv=2*l*h*d*t*b*n,score=q*t*t*b*n;
    return `KV cache reference = ${(kv/2**30).toFixed(3)} GiB\nMaterialized dense scores = ${(score/2**30).toFixed(3)} GiB\nAt 2× tokens: KV ${(2*kv/2**30).toFixed(3)} GiB; scores ${(4*score/2**30).toFixed(3)} GiB\nThese are separate quantities, not a total-memory sum.`;
  });
  result('cost-result',()=>{
    const input=finiteField('cost-input',0,1e8,true),output=finiteField('cost-output',0,1e8,true),ip=finiteField('cost-in-price',0,1e6),op=finiteField('cost-out-price',0,1e6),rps=finiteField('cost-rps',0,1e6),seconds=finiteField('cost-time',0,86400);
    const cost=(input*ip+output*op)/1e6;
    return `Illustrative USD / request = $${cost.toFixed(6)}\nUSD / day at constant arrival rate = $${(cost*rps*86400).toFixed(2)}\nAverage in-flight work = ${(rps*seconds).toFixed(2)}\nNo retry, tool or storage charges included.`;
  });
}
readRoute(false);
