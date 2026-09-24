import json,re
c=json.load(open('/Users/vladimir/sakhva-travel/data/catalog.json'))
items=next(v for v in c.values() if isinstance(v,list))

def cat_of(i):
    tags=set(i.get('tags',[])); t=i['title'].lower()
    if i.get('days',0)>0: return 'multi'
    if 'Кахетия' in tags or 'Винные' in tags or 'Гастро' in tags: return 'wine'
    if 'Казбеги' in tags or 'Горные' in tags: return 'mountains'
    if 'Батуми' in tags or any(w in t for w in ['кутаиси','сванет','зугдиди','боржоми','гори ']): return 'regions'
    if 'Мастер-классы' in tags or 'Фото' in tags or 'Романтика' in tags or 'Для детей' in tags: return 'experience'
    if 'Старый Тбилиси' in tags or 'Ночные' in tags or 'Пешеходные' in tags or 'Релоканты' in tags or 'тбилиси' in t: return 'tbilisi'
    return 'regions'

def short(title):
    n=title.split(' — ')[0]
    n=re.sub(r'\s*2026$','',n)
    n=n.replace(' из Тбилиси','').replace(' по Тбилиси',' Тбилиси')
    n=re.sub(r'^(Экскурсия|Экскурсии|Тур|Поход)\s+','',n)
    n=re.sub(r'^(в|во|из|по)\s+','',n)
    n=n.strip()
    if n: n=n[0].upper()+n[1:]
    return n[:36]

# order: tbilisi, wine, mountains, regions, experience, multi (matches CATS display)
order=['tbilisi','wine','mountains','regions','experience','multi']
tours=[]
for i in items:
    tours.append({'slug':i['slug'],'name':short(i['title']),'gel':int(i['price']),'cat':cat_of(i)})
# sort by category order then price asc for stable indexing
tours.sort(key=lambda x:(order.index(x['cat']), x['gel']))
tours_js='['+','.join('{name:%s,gel:%d,cat:%s}'%(json.dumps(t['name'],ensure_ascii=False),t['gel'],json.dumps(t['cat'],ensure_ascii=False)) for t in tours)+']'
print("tours:",len(tours))

TEMPLATE=r'''const RATE={EUR:2.95,USD:2.72,RUB_PER_GEL:31};
function fmt(gel,cur){if(cur==='GEL')return '₾'+gel;if(cur==='EUR')return Math.round(gel/RATE.EUR)+'€';if(cur==='USD')return '$'+Math.round(gel/RATE.USD);if(cur==='RUB'){const r=Math.round(gel*RATE.RUB_PER_GEL/100)*100;return r.toLocaleString('ru-RU')+'₽';}return '₾'+gel;}
const CATS=[{id:'tbilisi',label:'🏙 Тбилиси'},{id:'wine',label:'🍷 Кахетия и вино'},{id:'mountains',label:'⛰ Горы и природа'},{id:'regions',label:'🗺 За городом и регионы'},{id:'experience',label:'🎨 Впечатления'},{id:'multi',label:'📅 Многодневные туры'}];
const TOURS=__TOURS__;

const j=$input.item.json;
let type=j.type,chatId=j.chatId||'',userId=j.userId||'',username=j.username||'',firstName=j.firstName||'',text=j.text||'',callbackData=j.callbackData||'',callbackId=j.callbackId||'';
if(!type){const msg=j.message,cb=j.callback_query;if(msg){type=(msg.text&&msg.text.startsWith('/'))?'command':'text';chatId=String(msg.chat.id);userId=String(msg.from.id);username=msg.from.username||'';firstName=msg.from.first_name||'';text=msg.text||'';}else if(cb){type='callback';chatId=String(cb.message.chat.id);userId=String(cb.from.id);username=cb.from.username||'';firstName=cb.from.first_name||'';callbackData=cb.data||'';callbackId=cb.id;}}
chatId=String(chatId||'');

function mkMsg(cid,t,kb){const p={chat_id:cid,text:t,parse_mode:'HTML',disable_web_page_preview:true};if(kb)p.reply_markup={inline_keyboard:kb};return p;}
function currencyKb(src){const s=src?(':'+src):'';return[[{text:'🇷🇺 Рубли ₽',callback_data:'currency:RUB'+s},{text:'🇪🇺 Евро €',callback_data:'currency:EUR'+s}],[{text:'🇺🇸 Доллары $',callback_data:'currency:USD'+s},{text:'🇬🇪 Лари ₾',callback_data:'currency:GEL'+s}]];}
function catsKb(cur,src){const s=src?(':'+src):'';const rows=CATS.map(function(c){const n=TOURS.filter(function(t){return t.cat===c.id;}).length;return [{text:c.label+' ('+n+')',callback_data:'cat:'+c.id+':'+cur+s}];});rows.push([{text:'🔄 Сменить валюту',callback_data:'start'}]);return rows;}
function toursKb(cur,src,catId){const s=src?(':'+src):'';const list=[];TOURS.forEach(function(t,i){if(t.cat===catId)list.push({t:t,i:i});});const rows=[];for(let k=0;k<list.length;k+=2){const row=[{text:list[k].t.name+' · '+fmt(list[k].t.gel,cur),callback_data:'tour:'+list[k].i+':'+cur+s}];if(list[k+1])row.push({text:list[k+1].t.name+' · '+fmt(list[k+1].t.gel,cur),callback_data:'tour:'+list[k+1].i+':'+cur+s});rows.push(row);}rows.push([{text:'← Категории',callback_data:'currency:'+cur+s}]);return rows;}
function datesKb(idx,cur,src){const s=src?(':'+src):'';const rows=[],now=new Date(),wd=['вс','пн','вт','ср','чт','пт','сб'],dates=[];for(let d=1;d<=14;d++){const dt=new Date(now);dt.setDate(now.getDate()+d);const dd=String(dt.getDate()).padStart(2,'0'),mm=String(dt.getMonth()+1).padStart(2,'0'),yyyy=dt.getFullYear();dates.push({label:dd+'.'+mm+' ('+wd[dt.getDay()]+')',val:yyyy+'-'+mm+'-'+dd});}for(let i=0;i<dates.length;i+=2){const row=[{text:dates[i].label,callback_data:'tour:'+idx+':'+cur+s+'|date:'+dates[i].val}];if(dates[i+1])row.push({text:dates[i+1].label,callback_data:'tour:'+idx+':'+cur+s+'|date:'+dates[i+1].val});rows.push(row);}const t=TOURS[idx];rows.push([{text:'← Назад',callback_data:'cat:'+(t?t.cat:'tbilisi')+':'+cur+s}]);return rows;}
function paxKb(idx,cur,date,src){const s=src?(':'+src):'';const r1=[],r2=[];for(let p=1;p<=4;p++)r1.push({text:String(p),callback_data:'tour:'+idx+':'+cur+s+'|date:'+date+'|pax:'+p});for(let p=5;p<=8;p++)r2.push({text:String(p),callback_data:'tour:'+idx+':'+cur+s+'|date:'+date+'|pax:'+p});return[r1,r2,[{text:'← Назад',callback_data:'tour:'+idx+':'+cur+s}]];}
function menuAction(txt){if(!txt)return null;const t=txt.toLowerCase();if(/тур|цен|стоим|брон|заказ|экскурс/.test(t))return 'tours';if(/контакт|связ|телефон|whatsapp|вотс/.test(t))return 'contacts';if(/о гид|об гид/.test(t))return 'about';if(/faq|часто/.test(t))return 'faq';return null;}
function isGreeting(txt){return/^(привет|hello|hi|здравствуй|добрый|хай|хей|start|старт|начать)/i.test((txt||'').trim());}

let startSrc='';if(type==='command'&&text.indexOf('/start')===0){const _sp=text.split(/\s+/);startSrc=_sp[1]||'';}

let cbAction='',tourIdx=-1,tourCur='EUR',tourDate='',pax=0,tourSrc='',catId='';
if(callbackData){const parts=callbackData.split('|');const main=parts[0].split(':');cbAction=main[0];
 if(cbAction==='tour'){tourIdx=parseInt(main[1]);tourCur=main[2]||'EUR';tourSrc=main[3]||'';}
 if(cbAction==='cat'){catId=main[1];tourCur=main[2]||'EUR';tourSrc=main[3]||'';}
 if(cbAction==='currency'){tourCur=main[1];tourSrc=main[2]||'';cbAction='show_cats';}
 for(const part of parts.slice(1)){const kv=part.split(':');if(kv[0]==='date')tourDate=kv[1];if(kv[0]==='pax')pax=parseInt(kv[1]);}}

const src=tourSrc||startSrc||'';
const tourInfo=(tourIdx>=0&&tourIdx<TOURS.length)?TOURS[tourIdx]:null;
const tourName=tourInfo?tourInfo.name:'';
const tourPrice=tourInfo?fmt(tourInfo.gel,tourCur):'';
const name=firstName||username||'друг';
const menu=(!callbackData&&type==='text')?menuAction(text):null;
const greet=(!callbackData&&type==='text')?isGreeting(text):false;

let tgPayload,action='send_only';

if((type==='command'&&(text==='/start'||text.indexOf('/start ')===0||text==='/tours'))||callbackData==='start'||greet){
  tgPayload=mkMsg(chatId,'👋 Привет, <b>'+name+'</b>!\n\nЯ помогу забронировать тур с Тимуром — частным гидом в Грузии 🇬🇪\n\n<b>Выберите валюту:</b>',currencyKb(src));
}else if(cbAction==='show_cats'||menu==='tours'){
  tgPayload=mkMsg(chatId,'🗺 <b>Выберите категорию</b>\n\nВсего '+TOURS.length+' туров и экскурсий',catsKb(tourCur||'EUR',src));
}else if(cbAction==='cat'&&catId){
  const cc=CATS.filter(function(x){return x.id===catId;});const lbl=cc.length?cc[0].label:'Туры';
  tgPayload=mkMsg(chatId,lbl+'\n\nВыберите тур:',toursKb(tourCur,src,catId));
}else if(menu==='contacts'||callbackData==='contacts_inline'){
  tgPayload=mkMsg(chatId,'📱 <b>Контакты гида Тимура</b>\n\n• WhatsApp: <a href="https://wa.me/995511272623">+995 511 272 623</a>\n• Сайт: sakhva-travel.com\n\n<i>Тимур отвечает ежедневно 9:00–22:00</i>');
}else if(menu==='about'){
  tgPayload=mkMsg(chatId,'ℹ️ <b>О гиде Тимуре</b>\n\n8 лет опыта · рейтинг 4.9⭐\n✅ Авторские маршруты\n✅ Личный автомобиль включён',[[{text:'🗺 Смотреть туры',callback_data:'start'}]]);
}else if(menu==='faq'){
  tgPayload=mkMsg(chatId,'❓ <b>FAQ</b>\n\n<b>Оплата?</b> Наличные или перевод\n<b>Отмена?</b> Бесплатно за 24ч',[[{text:'📱 Контакты гида',callback_data:'contacts_inline'}]]);
}else if(cbAction==='tour'&&tourInfo&&!tourDate&&!pax){
  tgPayload=mkMsg(chatId,'📅 <b>'+tourName+'</b>\nЦена: '+tourPrice+'/чел\n\nВыберите дату:',datesKb(tourIdx,tourCur,src));
}else if(cbAction==='tour'&&tourInfo&&tourDate&&!pax){
  tgPayload=mkMsg(chatId,'👥 <b>'+tourName+'</b>\n📅 '+tourDate+' · '+tourPrice+'/чел\n\nСколько человек?',paxKb(tourIdx,tourCur,tourDate,src));
}else if(cbAction==='tour'&&tourInfo&&tourDate&&pax){
  tgPayload=mkMsg(chatId,'✅ Отлично!\n\n🗺 '+tourName+'\n📅 '+tourDate+' · '+pax+' чел. · '+tourPrice+'/чел\n\n<b>Как вас зовут?</b>');
  action='create_pending';
}else if(type==='text'&&text&&!text.startsWith('/')){
  tgPayload=mkMsg(chatId,'⏳ Оформляем бронь...');
  action='complete_booking';
}else{
  tgPayload=mkMsg(chatId,'Нажмите /start чтобы выбрать тур 👇',[[{text:'🚀 Начать',callback_data:'start'}]]);
}

return{type:type,chatId:chatId,userId:userId,username:username,firstName:name,text:text,callbackData:callbackData,callbackId:callbackId,tourIdx:tourIdx,tourCur:tourCur,tourDate:tourDate,pax:pax||1,src:src,tourName:tourName,tourPrice:tourPrice,guestName:action==='complete_booking'?text:'',action:action,tgPayload:tgPayload,tgPayloadAskName:mkMsg(chatId,'✅ <b>'+tourName+'</b> · '+tourDate+' · '+(pax||1)+' чел.\n\nКак вас зовут?'),tgPayloadNotFound:mkMsg(chatId,'Что-то пошло не так. Начните заново:',[[{text:'🚀 /start',callback_data:'start'}]])};'''

js=TEMPLATE.replace('__TOURS__',tours_js)
wf=json.load(open('/tmp/sakhva_wf_final.json'))
next(n for n in wf['nodes'] if n['name']=='Bot Logic')['parameters']['jsCode']=js
json.dump(wf,open('/tmp/sakhva_wf_final.json','w'),ensure_ascii=False)
open('/tmp/bl_full_check.js','w').write("function _(){\n"+js+"\n}\n")
print("Bot Logic rebuilt, jsCode len:",len(js))
