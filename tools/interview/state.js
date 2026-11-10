const DATA = JSON.parse(document.getElementById('guide-data').textContent);
const projects = new Map(DATA.projects.map(p => [p.id, p]));
const topics = new Map(DATA.topics.map(t => [t.id, t]));
const labels = {agents:'Agents & orchestration',rag:'RAG systems',retrieval:'Retrieval engineering',memory:'Memory & knowledge',mcp:'MCP integrations',training:'Training & adaptation',evaluation:'Evaluation',voice:'Speech & voice',media:'Media pipelines',structured:'Structured extraction',interfaces:'AI interfaces',operations:'Operations',recipe:'Deployment recipes',ocr:'OCR & documents'};
const allQuestions = [...DATA.projects.flatMap(p => p.questions.map(q => ({...q, origin:p.id, type:'project', category:p.category}))), ...DATA.topics.flatMap(t => t.questions.map(q => ({...q, origin:t.id, type:'topic', category:t.group})))];
const itemIDs = new Set([...DATA.projects.map(p => 'project:'+p.id), ...DATA.topics.map(t => 'topic:'+t.id)]);
const questionIDs = new Set(allQuestions.map(q => q.type+':'+q.id));
const storageKey = 'ai-engineer-field-manual-v1';
let storageAvailable = true;
let storageMessage = '';
const freshStudy = () => ({version:1, bookmarks:[], reviewed:[], notes:{}, confidence:{}});
function validateStudy(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value) || value.version !== 1) throw new Error('This is not a supported revision backup.');
  const output = freshStudy();
  for (const name of ['bookmarks','reviewed']) {
    if (!Array.isArray(value[name]) || value[name].length > itemIDs.size || value[name].some(id => typeof id !== 'string' || !itemIDs.has(id))) throw new Error('Backup contains an unknown project/topic or invalid progress list.');
    output[name] = [...new Set(value[name])];
  }
  let total = 0;
  for (const name of ['notes','confidence']) {
    const record = value[name];
    if (!record || typeof record !== 'object' || Array.isArray(record)) throw new Error('Backup contains an invalid '+name+' object.');
    for (const [id, entry] of Object.entries(record)) {
      if (name === 'notes') {
        if (!itemIDs.has(id) || typeof entry !== 'string' || entry.length > 20000) throw new Error('Notes must belong to a known item and contain at most 20,000 characters each.');
        total += entry.length;
        if (total > 2000000) throw new Error('The combined note budget is two million characters.');
      } else if (!questionIDs.has(id) || !['review','comfortable'].includes(entry)) throw new Error('Backup has an unknown question or confidence value.');
      output[name][id] = entry;
    }
  }
  return output;
}
let study = freshStudy();
try {
  const saved = localStorage.getItem(storageKey);
  if (saved) study = validateStudy(JSON.parse(saved));
} catch (error) {
  storageAvailable = false;
  storageMessage = 'Browser storage is unavailable or the saved revision data could not be read. You can study and export this session; no stored data has been deleted.';
}
function persist() {
  try {
    localStorage.setItem(storageKey, JSON.stringify(study));
    storageAvailable = true;
    storageMessage = '';
    return true;
  } catch (error) {
    storageAvailable = false;
    storageMessage = 'Changes are kept in this open session only. Browser storage could not be written; export a JSON backup before closing.';
    return false;
  }
}
const escapeHTML = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const href = (view, options={}) => '#'+new URLSearchParams({view,...options}).toString();
const link = (view, options, text, cls='') => `<a href="${escapeHTML(href(view,options))}"${cls ? ` class="${cls}"` : ''}>${escapeHTML(text)}</a>`;
const projectLink = id => link('project',{id},id);
const topicLink = id => topics.has(id) ? link('topic',{id},topics.get(id).title) : '';
const itemKey = (type,id) => type+':'+id;
let route = {};
let searchTimer, toastTimer, noteTimer;
let practice = {index:0,level:'all',source:'all',revealed:false,remaining:120,timer:null};
let currentPractice = null;
function announce(message) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.add('visible');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('visible'), 4500);
}
function stopTimer() {
  if (practice.timer) clearInterval(practice.timer);
  practice.timer = null;
}
function progress() {
  const count = study.reviewed.filter(id => id.startsWith('project:')).length;
  document.getElementById('side-progress-label').textContent = `${count} of ${DATA.projects.length} reviewed`;
  document.getElementById('side-progress').max = DATA.projects.length;
  document.getElementById('side-progress').value = count;
}
for (const p of DATA.projects) p.search = [p.id,p.category,p.purpose,p.mechanism,p.experiment,p.production,p.models.join(' '),p.imports.join(' '),p.commands.map(c=>c.command).join(' '),p.questions.map(q=>q.question+' '+q.answer).join(' '),...Object.values(p.docs).map(s=>s.replace(/<[^>]*>/g,' '))].join(' ').toLowerCase();
for (const t of DATA.topics) t.search = (t.title+' '+t.group+' '+t.body).toLowerCase();
function matchSearch(item, query) {
  return query.trim().toLowerCase().split(/\s+/).filter(Boolean).every(term => item.search.includes(term));
}
function ratio(top,bottom) {return bottom ? top/bottom : null;}
function percent(value) {return value === null ? 'undefined (zero denominator)' : (value*100).toFixed(2)+'%';}
function finiteField(id,min=0,max=1e12,integer=false) {
  const field=document.getElementById(id);
  if (!field || field.value.trim()==='') throw new Error('Complete every field with a finite value.');
  const value=Number(field.value);
  if(!Number.isFinite(value)||value<min||value>max||(integer&&!Number.isInteger(value))) throw new Error(`Use ${integer?'whole numbers':'finite numbers'} between ${min} and ${max}.`);
  return value;
}
