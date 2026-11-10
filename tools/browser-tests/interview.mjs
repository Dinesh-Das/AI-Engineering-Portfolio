import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const html=await fs.readFile(path.join(root,'index.html'));
const report={date:'2026-11-11',source_sha256:createHash('sha256').update(html).digest('hex'),checks:[],failures:[],screenshots:[]};
const screenshots=path.join(root,'docs/interview-screenshots');
await fs.mkdir(screenshots,{recursive:true});
const server=http.createServer((req,res)=>{
  if(!['/','/index.html'].includes(new URL(req.url,'http://localhost').pathname)){res.writeHead(404);res.end('Not found');return;}
  res.writeHead(200,{'Content-Type':'text/html; charset=utf-8'});res.end(html);
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const origin=`http://127.0.0.1:${server.address().port}`;
const fileURL=pathToFileURL(path.join(root,'index.html')).href;
const browser=await chromium.launch({executablePath:process.env.UI_TEST_CHROME||'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
const errors=[],external=[];
function track(page){
  page.on('pageerror',error=>errors.push(error.message));
  page.on('console',message=>{if(message.type()==='error')errors.push(message.text());});
  page.on('request',request=>{if(!request.url().startsWith(origin)&&!request.url().startsWith('file:')&&!request.url().startsWith('data:')&&!request.url().startsWith('blob:'))external.push(request.url());});
}
async function check(name,fn){try{await fn();report.checks.push({name,passed:true});process.stdout.write('PASS '+name+'\n');}catch(error){report.checks.push({name,passed:false,error:error.message});report.failures.push(name);throw error;}}
async function go(page,view,params={}){
  const target='#'+new URLSearchParams({view,...params}).toString();
  // Normal browser navigation to this known local artifact; no external page content is followed.
  await page.goto(origin+'/index.html'+target);
  await page.locator('#page-title').waitFor();
  await page.waitForFunction(({view,id})=>{
    const title=document.getElementById('page-title')?.textContent;
    const expected={home:'Build the intuition.Defend the decisions.',projects:'Every project. A mechanism to explain.',topics:'Understand the idea. Work the example.',practice:'Explain it out loud.',labs:'Keep the units. Show your working.',revision:'Make the evidence your own.',about:'A reference you can inspect.'};
    if(view==='project')return title===id;
    if(view==='topic')return title===JSON.parse(document.getElementById('guide-data').textContent).topics.find(t=>t.id===id)?.title;
    return !expected[view]||title===expected[view];
  },{view,id:params.id});
}
async function overflow(page){return page.evaluate(()=>({page:document.documentElement.scrollWidth,width:innerWidth}));}
async function axe(page,label){
  const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
  assert.deepEqual(result.violations.map(v=>({id:v.id,description:v.description,nodes:v.nodes.map(n=>n.target)})),[],label);
}
try{
  const context=await browser.newContext({viewport:{width:1440,height:1050},acceptDownloads:true});
  const page=await context.newPage();track(page);
  await check('direct-file opening and complete embedded inventory',async()=>{
    await page.goto(fileURL);await page.locator('#page-title').waitFor();
    const data=await page.locator('#guide-data').textContent();
    report.coverage=JSON.parse(data).coverage;
    assert.deepEqual(report.coverage,{projects:113,topics:46,questions:477});
    assert.match(await page.locator('#main').innerText(),/Defend the decisions/);
    assert.equal(errors.length,0);
    report.startup=await page.evaluate(()=>{const n=performance.getEntriesByType('navigation')[0];return {dom_content_loaded_ms:n.domContentLoadedEventEnd,duration_ms:n.duration};});
  });
  await check('initial desktop screenshot and accessibility',async()=>{
    await go(page,'home');await axe(page,'Home');
    const shot=path.join(screenshots,'home-desktop.png');await page.screenshot({path:shot,fullPage:true});report.screenshots.push(path.relative(root,shot));
  });
  await check('all project readers and run command panels',async()=>{
    await go(page,'projects');
    assert.equal(await page.locator('.project-row').count(),113);
    const ids=await page.locator('.project-row h3 a').allTextContents();
    for(const id of ids){
      const target=page.locator('.project-row h3 a').filter({hasText:new RegExp('^'+id.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'$')});
      await target.click();
      await page.waitForFunction(expected=>document.getElementById('page-title')?.textContent===expected,id);
      assert.equal(await page.locator('#page-title').textContent(),id);
      await page.getByRole('link',{name:'Run commands',exact:true}).click();
      assert.match(await page.locator('.command-item').first().innerText(),/CPU learning checks/);
      assert.ok((await page.locator('.command-item code').allTextContents()).some(c=>c.includes(id)));
      await page.getByRole('link',{name:'Project atlas',exact:false}).first().click();
      await page.locator('#category-filter').waitFor();
    }
  });
  await check('chapter reading and question levels',async()=>{
    await go(page,'topics');assert.equal(await page.locator('.topic-row').count(),46);
    await page.getByRole('link',{name:/Transformers and attention from shapes/}).click();
    await page.locator('.question-card').first().waitFor();
    assert.equal(await page.locator('.question-card').count(),3);
    await page.locator('.question-card summary').nth(2).click();
    assert.match(await page.locator('.question-card').nth(2).innerText(),/exact attention/);
    await axe(page,'Chapter');
    await page.goBack();await page.getByRole('heading',{name:'Understand the idea. Work the example.'}).waitFor();
    await page.goForward();await page.getByRole('heading',{name:'Transformers and attention from shapes to tradeoffs',exact:true}).waitFor();
  });
  await check('search, empty results and category filtering',async()=>{
    const started=Date.now();await page.getByLabel('Search all projects, concepts and questions').fill('colbert');
    await page.waitForURL(/view=search/);await page.locator('.project-row').first().waitFor();
    assert.ok((await page.locator('#main').innerText()).includes('colbert-rag'));
    report.search_response_ms=Date.now()-started;
    await page.getByLabel('Search all projects, concepts and questions').fill('zzzznoresult9876');
    await page.getByRole('heading',{name:'No matches yet'}).waitFor();
    await go(page,'projects');await page.getByLabel('Area',{exact:true}).selectOption('ocr');
    assert.equal(await page.locator('.project-row').count(),4);
  });
  await check('embedded deep guides, command copy and project state',async()=>{
    await go(page,'project',{id:'gemma3-ocr',tab:'docs'});
    await page.getByLabel('Read',{exact:true}).selectOption('source');
    assert.match(await page.locator('.guide-copy').innerText(),/Ollama/);
    await page.getByLabel('Read',{exact:true}).selectOption('author');
    assert.ok((await page.locator('.guide-copy').innerText()).length>500);
    await page.getByRole('button',{name:'Save for revision',exact:false}).first().click();
    await page.getByRole('button',{name:'Mark reviewed',exact:true}).click();
    await page.getByLabel('Your evidence & revision notes').fill('Measured one changed digit; format and fact quality differ.');
    await page.getByText('Saved in this browser.',{exact:false}).waitFor();
    await page.reload();
    assert.match(await page.getByLabel('Your evidence & revision notes').inputValue(),/changed digit/);
    await page.getByRole('link',{name:'Run commands',exact:true}).click();
    await page.locator('.command-item').first().getByRole('button',{name:/Copy/}).click();
    await page.locator('#toast.visible').waitFor();
    assert.match(await page.locator('#toast').textContent(),/copied|selected/);
    await axe(page,'Commands');
  });
  await check('mock interview, reveal, self-assessment and timer',async()=>{
    await go(page,'practice',{origin:'rag-design',type:'topic'});
    await page.getByLabel('Question depth').selectOption('Advanced');
    assert.equal(await page.locator('.practice-answer').isVisible(),false);
    await page.getByRole('button',{name:'Reveal answer rubric'}).click();
    assert.equal(await page.locator('.practice-answer').isVisible(),true);
    await page.getByRole('button',{name:'Comfortable explaining'}).click();
    await page.getByRole('button',{name:'Start / resume timer'}).click();
    await page.waitForFunction(()=>document.getElementById('practice-timer').textContent==='01:59');
    await page.getByRole('button',{name:'Pause timer'}).click();
    await axe(page,'Practice');
  });
  await check('metric, ranking, capacity and cost arithmetic',async()=>{
    await go(page,'labs');
    assert.match(await page.locator('#metric-result').textContent(),/Precision = 75.00%/);
    assert.match(await page.locator('#rank-result').textContent(),/Recall@2 = 0.5000/);
    assert.match(await page.locator('#kv-result').textContent(),/KV cache reference = 0.500 GiB/);
    assert.match(await page.locator('#cost-result').textContent(),/request = \$0.004000/);
    await page.getByLabel('True positives',{exact:true}).fill('0');await page.getByLabel('False positives',{exact:true}).fill('0');
    assert.match(await page.locator('#metric-result').textContent(),/undefined/);
    await page.getByLabel('Cutoff k',{exact:true}).fill('0');assert.match(await page.locator('#rank-result').textContent(),/between 1 and 100/);
    await page.getByLabel('Cutoff k',{exact:true}).fill('3');
    await page.getByLabel('Cached / prompt tokens',{exact:true}).fill('8192');
    assert.match(await page.locator('#kv-result').textContent(),/KV cache reference = 1.000 GiB/);
    await axe(page,'Labs');
  });
  await check('JSON export/import, hostile note text and invalid backup recovery',async()=>{
    await go(page,'revision');
    const downloadPromise=page.waitForEvent('download');await page.getByRole('button',{name:'Export revision JSON'}).click();
    const download=await downloadPromise;const stream=await download.createReadStream();let raw='';for await(const chunk of stream)raw+=chunk;
    const backup=JSON.parse(raw);assert.match(backup.notes['project:gemma3-ocr'],/changed digit/);
    const before=await page.locator('#main').innerText();
    await page.locator('#import-file').setInputFiles({name:'bad.json',mimeType:'application/json',buffer:Buffer.from('{"version":1,"bookmarks":["unknown"],"reviewed":[],"notes":{},"confidence":{}}')});
    await page.getByText(/Import rejected; existing revision is unchanged/).waitFor();
    assert.equal(await page.locator('#main').innerText(),before);
    backup.notes['project:gemma3-ocr']='<img src="https://invalid.test/x" onerror="alert(1)">';
    await page.locator('#import-file').setInputFiles({name:'safe-text.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(backup))});
    await page.getByText(/Revision backup imported/).waitFor();
    assert.equal(await page.locator('.note-preview img').count(),0);
    assert.match(await page.locator('.note-preview').first().textContent(),/<img/);
    await axe(page,'Revision');
  });
  await check('responsive layouts, mobile menu and keyboard navigation',async()=>{
    for(const width of [320,768,1024,1440]){
      await page.setViewportSize({width,height:1000});await go(page,'home');
      let size=await overflow(page);assert.ok(size.page<=size.width,`Home overflow at ${width}: ${JSON.stringify(size)}`);
      await go(page,'project',{id:'knowledge distillation',tab:'docs'});
      size=await overflow(page);assert.ok(size.page<=size.width,`Guide overflow at ${width}: ${JSON.stringify(size)}`);
      if(width===320){
        await page.getByRole('button',{name:'Menu',exact:true}).click();
        assert.equal(await page.getByRole('button',{name:'Menu',exact:true}).getAttribute('aria-expanded'),'true');
        await page.getByRole('link',{name:/Work the numbers/}).click();
        await page.waitForFunction(()=>document.getElementById('page-title')?.textContent==='Keep the units. Show your working.');
        assert.match(await page.locator('#page-title').textContent(),/Keep the units/);
        await axe(page,'Mobile labs');
        await page.locator('#toast').waitFor({state:'hidden'});
        const shot=path.join(screenshots,'labs-mobile.png');await page.screenshot({path:shot,fullPage:true});report.screenshots.push(path.relative(root,shot));
      }
    }
    await go(page,'home');await page.keyboard.press('/');
    assert.equal(await page.getByLabel('Search all projects, concepts and questions').evaluate(el=>el===document.activeElement),true);
    await page.keyboard.press('Escape');
  });
  await check('blocked storage remains usable and exportable',async()=>{
    const blocked=await browser.newContext({viewport:{width:1024,height:900},acceptDownloads:true});
    await blocked.addInitScript(()=>{Storage.prototype.getItem=function(){throw new Error('disabled for test');};Storage.prototype.setItem=function(){throw new Error('disabled for test');};});
    const p=await blocked.newPage();track(p);await go(p,'project',{id:'gemma3-ocr'});
    await p.getByLabel('Your evidence & revision notes').fill('Session-only observation.');
    await p.getByText(/Changes are kept in this open session only/).waitFor();
    await p.getByRole('link',{name:/My revision/}).first().click();await p.getByText(/Browser storage could not be written/).waitFor();
    const request=p.waitForEvent('download');await p.getByRole('button',{name:'Export revision JSON'}).click();assert.ok(await request);
    await blocked.close();
  });
  await check('zero console errors and no external requests',async()=>{assert.deepEqual(errors,[]);assert.deepEqual(external,[]);});
  await context.close();
}catch(error){report.error=error.stack;process.stderr.write(error.stack+'\n');process.exitCode=1;}
finally{
  report.console_errors=errors;report.external_requests=external;
  report.passed=report.failures.length===0&&!report.error;
  await fs.writeFile(path.join(root,'docs/interview-browser-validation.json'),JSON.stringify(report,null,2)+'\n');
  await browser.close();server.closeAllConnections();await new Promise(resolve=>server.close(resolve));
  process.stdout.write(JSON.stringify({passed:report.passed,checks:report.checks.length,failures:report.failures},null,2)+'\n');
}
