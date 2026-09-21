// E2E-проверка дашборда на проде: создаёт тестовую бронь в Airtable, гоняет сценарии Полины/Владимира, удаляет её.
// Запуск: cd dashboard && AT_PAT=<AIRTABLE_PAT_CRM> OWNER_KEY=$(cat ~/.sakhva-owner-key) node tests/qa.mjs
import {chromium} from '/Users/vladimir/node_modules/playwright/index.mjs';
const BASE='applRAxP05f367bbN',TBL='tblDlE4EHjy799l18',URL='https://dash.sakhva-travel.com/';
const PAT=process.env.AT_PAT,OWNER=process.env.OWNER_KEY||'';
if(!PAT){console.error('AT_PAT не задан');process.exit(2);}
const AT=async(m,path,body)=>(await fetch(`https://api.airtable.com/v0/${BASE}/${TBL}${path}`,{method:m,headers:{Authorization:'Bearer '+PAT,'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined})).json();
const tmr=new Date(Date.now()+144e5+864e5).toISOString().slice(0,10);
const rec=await AT('POST','',{fields:{'Тур':'QA-тест — не трогать','Дата тура':tmr,'Кол-во человек':2,'Статус':'Подтверждена','Клиент':'QA Тест','Телефон':'+995500000000','Сумма':100,'Валюта':'₾','Время выезда':'09:00'}});
const ID=rec.id;const R=[];let fails=0;const ok=(n,c)=>{R.push((c?'PASS ':'FAIL ')+n);if(!c)fails++;};
const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1600,height:1000}});await ctx.grantPermissions(['clipboard-read','clipboard-write']);
const pg=await ctx.newPage();const errs=[];pg.on('pageerror',e=>errs.push(e.message));const dl=[];pg.on('dialog',async d=>{dl.push(d.message().slice(0,60));await d.accept();});
try{
  await pg.goto(URL+'?v='+Date.now(),{waitUntil:'networkidle'});await pg.waitForTimeout(4000);
  const kinds=()=>pg.$$eval('#todoL .card',e=>e.map(c=>(c.querySelector('.cs-k')?.textContent||'req')+'|'+c.querySelector('.cs-t').textContent.trim()));
  let k=await kinds();
  ok('todo: «Гид не назначен»',k.some(x=>x.startsWith('Гид не назначен|')&&x.includes('QA')));
  ok('todo: «Нет водителя»',k.some(x=>x.startsWith('Нет водителя|')&&x.includes('QA')));
  ok('гид — select',await pg.$eval('#fGui',e=>e.tagName==='SELECT'));
  await pg.evaluate(()=>{WHO='QA-бот';localStorage.setItem('who',WHO);whoSet();});
  await pg.evaluate(id=>openById(id),ID);await pg.waitForTimeout(400);
  ok('чек-лист на карточке',await pg.$$eval('#upL .card',e=>e.some(c=>c.textContent.includes('QA')&&c.querySelector('.ck'))));
  await pg.selectOption('#fGui','Тимур');await pg.fill('#fFee','120');await pg.check('#fGok');await pg.selectOption('#fCh','Сарафан');
  await pg.fill('#fPrice','60');await pg.waitForTimeout(100);
  ok('подсветка смены цены',await pg.$$eval('.price-changed',e=>e.length===2));
  await pg.click('#modal .btn-p');await pg.waitForTimeout(2500);
  ok('confirm на смену цены',dl.some(x=>x.includes('Меняется цена')));
  let f=(await AT('GET','/'+ID)).fields;
  ok('Airtable: гид/гонорар/подтвердил/канал/кем',f['Гид']==='Тимур'&&f['Гонорар гида ₾']===120&&f['Гид подтвердил']===true&&f['Канал']==='Сарафан'&&f['Кем изменено']==='QA-бот');
  ok('Airtable: Изменено',!!f['Изменено']);
  // повторное сохранение — без ложного конфликта
  dl.length=0;await pg.evaluate(id=>openById(id),ID);await pg.waitForTimeout(300);await pg.fill('#fNot','второе сохранение');await pg.click('#modal .btn-p');await pg.waitForTimeout(2500);
  ok('повторное сохранение без «изменили с другого устройства»',!dl.some(x=>x.includes('другого устройства')));
  // карточка гиду
  await pg.evaluate(id=>openById(id),ID);await pg.waitForTimeout(300);
  const popP=pg.waitForEvent('popup',{timeout:4000}).catch(()=>null);await pg.click('text=Карточка гиду');const pop=await popP;
  const clip=await pg.evaluate(()=>navigator.clipboard.readText()).catch(()=>'');
  ok('карточка гиду: текст',clip.includes('QA-тест'));ok('карточка гиду: WhatsApp гида',!!pop&&/phone=995511272623|wa\.me\/995511272623/.test(pop.url()));if(pop)await pop.close();
  ok('заголовок: изм. · кто',await pg.$eval('#mSub',e=>e.textContent.includes('QA-бот')));
  await pg.click('text=Ссылка на оплату');await pg.waitForTimeout(200);
  ok('ссылка на оплату с остатком',await pg.$$eval('#payLinks input',e=>e[0].value.includes('amount=120')&&e[0].value.includes('ref=995500000000')));
  await pg.keyboard.press('Escape');await pg.waitForTimeout(200);
  ok('Esc закрывает только верхнюю модалку',await pg.evaluate(()=>!document.getElementById('payModal').classList.contains('active')&&document.getElementById('modal').classList.contains('active')));
  await pg.evaluate(()=>closeM());
  // выплата: без ключа — 403, с ключом — ок
  await pg.evaluate(()=>{OK='wrong';});await pg.click('text=Гиды');await pg.waitForTimeout(400);
  ok('сводка: к выплате 120',(await pg.$eval('#gdSum',e=>e.textContent)).includes('120'));
  await (await pg.$('#gdList button.qbtn-ok')).click();await pg.waitForTimeout(2500);
  ok('прокси: неверный ключ владельца → выплата не прошла',(await AT('GET','/'+ID)).fields['Гиду выплачено']!==true);
  if(OWNER){await pg.evaluate(k=>{OK=k;},OWNER);await (await pg.$('#gdList button.qbtn-ok')).click();await pg.waitForTimeout(2500);
    ok('прокси: верный ключ → Гиду выплачено=true',(await AT('GET','/'+ID)).fields['Гиду выплачено']===true);
    ok('после выплаты к выплате 0',await pg.$eval('#gdSum',e=>/к выплате\s*0/.test(e.textContent.replace(/\s+/g,' '))));}
  await pg.evaluate(()=>guiClose());
  ok('регламент грузится из md',await pg.evaluate(async()=>{regOpen();await regLoad();return regLoad._done===true;}));
  k=await kinds();ok('после подтверждения карточки гида ушли',!k.some(x=>x.includes('QA')&&/^Гид/.test(x)));
  ok('нет JS-ошибок',errs.length===0);if(errs.length)R.push('  '+errs.join(' | ').slice(0,300));
}finally{await b.close();await AT('DELETE','/'+ID);}
console.log(R.join('\n'));console.log(fails?`\n${fails} FAIL`:'\nALL PASS');process.exit(fails?1:0);
