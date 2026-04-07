
// NAV scroll
window.addEventListener('scroll',()=>{
  document.getElementById('nav').classList.toggle('scrolled',window.scrollY>60)
},{passive:true})

// ── TOUR DETAIL MODAL ──
const TOURS={
  'night-tbilisi':{
    badge:'live',img:'/images/night-tbilisi-tour.webp',
    cat:'Ноктуризм · 2.5 ч',name:'Ночной Тбилиси',gel:'₾71',usd:'$27',
    cat_en:'Night tour · 2.5 h',name_en:'Night Tbilisi',
    desc:'Тбилиси после заката — совсем другой город. Серные бани в темноте, атмосферные дворики, рестораны куда не попасть без местного. Старт в 20:00.',
    desc_en:'Tbilisi after dark is a completely different city. Sulfur baths at night, atmospheric courtyards, restaurants you can only find with a local. Starts at 20:00.',
    includes:['Личный гид Тимур на всём маршруте','Трансфер между точками','Рекомендации по ресторанам и баням','Маршрут в мессенджере после тура'],
    includes_en:['Guide Timur throughout the tour','Transfer between stops','Restaurant &amp; bath recommendations','Route sent to your messenger after the tour'],
    route:['20:00 — Встреча у Моста Мира','20:30 — Серные бани: история и атмосфера ночью','21:15 — Старый Тбилиси: дворики, балконы, тишина','22:00 — Ужин в ресторане у местных (за счёт гостей)','23:00 — Конец маршрута'],
    route_en:['20:00 — Meet at Bridge of Peace','20:30 — Sulfur baths: history &amp; night atmosphere','21:15 — Old Tbilisi: courtyards, balconies, silence','22:00 — Dinner at a local restaurant (guests\' expense)','23:00 — End of tour'],
    wa:'Хочу+забронировать+Ночной+Тбилиси',wa_en:'I+want+to+book+Night+Tbilisi+tour'
  },
  dinner:{
    badge:'hot',img:'/images/dinner-tour.webp',
    cat:'Премиум · 4–5 ч',name:'Тур + ужин у местных',gel:'₾185',usd:'$70',
    cat_en:'Premium · 4–5 h',name_en:'Tour + dinner with locals',
    desc:'Днём — прогулка по Старому Тбилиси с Тимуром. Вечером — домашний ужин у грузинской семьи: хинкали лепим вместе, вино из квеври, живые истории. Самый популярный премиум-тур.',
    desc_en:'Daytime — walk through Old Tbilisi with Timur. Evening — home dinner with a Georgian family: we make khinkali together, qvevri wine, real stories. Our most popular premium tour.',
    includes:['Экскурсия 2.5 ч по Старому Тбилиси','Домашний ужин у грузинской семьи (3 часа)','Все напитки на ужине включены','Трансфер от ужина до отеля','Фото на память от Тимура'],
    includes_en:['2.5 h tour of Old Tbilisi','Home dinner with Georgian family (3 hours)','All drinks at dinner included','Transfer from dinner to hotel','Memorable photos from Timur'],
    route:['10:00 — Старый Тбилиси: серные бани, армянский квартал','11:30 — Нарикала, вид на город','13:00 — Свободное время','19:00 — Ужин у семьи Нино и Гиорги','22:00 — Трансфер в отель'],
    route_en:['10:00 — Old Tbilisi: sulfur baths, Armenian quarter','11:30 — Narikala, city view','13:00 — Free time','19:00 — Dinner with Nino &amp; Giorgi\'s family','22:00 — Transfer to hotel'],
    wa:'Хочу+забронировать+Тур+ужин+у+местных',wa_en:'I+want+to+book+Tour+Dinner+with+Locals'
  },
  soviet:{
    badge:'live',img:'/images/soviet-tour.webp',
    cat:'Нишевый · 3 ч',name:'Советский Тбилиси',gel:'₾86',usd:'$32',
    cat_en:'Niche · 3 h',name_en:'Soviet Tbilisi',
    desc:'Конструктивизм, панельные кварталы, советские мозаики и истории о жизни при СССР. Для тех, кто вырос в СНГ — волна ностальгии гарантирована.',
    desc_en:'Constructivism, Soviet-era blocks, iconic mosaics and stories of life under the USSR. A wave of nostalgia for those who grew up in the post-Soviet space.',
    includes:['Гид Тимур (вырос в Тбилиси в 90-е)','Трансфер по маршруту','Фото советских мозаик и архитектуры'],
    includes_en:['Guide Timur (grew up in Tbilisi in the 90s)','Transfer along the route','Photos of Soviet mosaics &amp; architecture'],
    route:['Район Варкетили: панельный Тбилиси','Советские мозаики на стенах домов','Заброшенный НИИ: конструктивизм изнутри','Рынок Дезертирка: советская торговля жива','Кафе-советская столовая с аутентичным меню'],
    route_en:['Varketili district: Soviet-era Tbilisi','Soviet mosaics on apartment building walls','Abandoned research institute: constructivism inside','Dezerter Bazaar: Soviet trading lives on','Soviet-style canteen café with authentic menu'],
    wa:'Хочу+забронировать+Советский+Тбилиси',wa_en:'I+want+to+book+Soviet+Tbilisi+tour'
  },
  'slow-travel':{
    badge:'hot',img:'/images/slow-travel-tour.webp',
    cat:'Премиум · 3 дня',name:'Slow Travel пакет',gel:'₾424',usd:'$161',
    cat_en:'Premium · 3 days',name_en:'Slow Travel package',
    desc:'Три дня с Тимуром — три разных маршрута. Без спешки, без толпы, с трансфером из аэропорта. Идеально для первого раза в Грузии.',
    desc_en:'Three days with Timur — three different routes. No rush, no crowds, with airport transfer. Perfect for your first time in Georgia.',
    includes:['Трансфер аэропорт → отель','3 экскурсии (Тбилиси, Казбеги, Кахетия)','Все трансферы включены','Рекомендации по отелям и кафе','Поддержка в мессенджере весь визит'],
    includes_en:['Airport → hotel transfer','3 tours (Tbilisi, Kazbegi, Kakheti)','All transfers included','Hotel &amp; café recommendations','Messenger support throughout your stay'],
    route:['День 1 — Прилёт + Старый Тбилиси вечером','День 2 — Казбеги: Гергетская Троица, Казбек','День 3 — Кахетия: Сигнаги, вино, обед у хозяйки'],
    route_en:['Day 1 — Arrival + Old Tbilisi in the evening','Day 2 — Kazbegi: Gergeti Trinity, Mt. Kazbek','Day 3 — Kakheti: Signagi, wine, lunch at a local home'],
    wa:'Хочу+забронировать+Slow+Travel+пакет',wa_en:'I+want+to+book+Slow+Travel+package'
  },
  photo:{
    badge:'live',img:'/images/photo-tour.webp',
    cat:'Премиум · Фото · 4 ч',name:'Тур + фотосессия',gel:'₾196',usd:'$75',
    cat_en:'Premium · Photo · 4 h',name_en:'Tour + photo session',
    desc:'Тур по лучшим локациям Тбилиси + профессиональный фотограф рядом весь день. 30–50 обработанных снимков. Особенно популярно у пар и в медовый месяц.',
    desc_en:'Tour of Tbilisi\'s best spots + a professional photographer by your side all day. 30–50 edited photos. Especially popular with couples and honeymooners.',
    includes:['Гид Тимур + профессиональный фотограф','4 часа съёмки на маршруте','30–50 обработанных фото в течение 48 часов','Трансфер по маршруту','Рекомендации по лучшим локациям для фото'],
    includes_en:['Guide Timur + professional photographer','4 hours of shooting on the route','30–50 edited photos within 48 hours','Transfer along the route','Recommendations for the best photo spots'],
    route:['Балконы Старого Тбилиси на рассвете','Мост Мира и набережная','Нарикала: панорама города','Серные бани (Абанотубани)','Метехи и вид на старый город'],
    route_en:['Old Tbilisi balconies at dawn','Bridge of Peace &amp; embankment','Narikala: panorama of the city','Sulfur baths (Abanotubani)','Metekhi and old city view'],
    wa:'Хочу+забронировать+Тур+фотосессия',wa_en:'I+want+to+book+Tour+Photo+Session'
  },
  kazbegi:{
    badge:'live',img:'/images/kazbegi-tour.webp',
    cat:'Выезд · 12–14 ч',name:'Казбеги за 1 день',gel:'₾128',usd:'$49',
    cat_en:'Day trip · 12–14 h',name_en:'Kazbegi in 1 day',
    desc:'Военно-Грузинская дорога, крепость Ананури, Гергетская Троица с видом на Казбек 5047м. Один из лучших однодневных маршрутов в мире. Выезд на рассвете — возвращение вечером.',
    desc_en:'Georgian Military Highway, Ananuri fortress, Gergeti Trinity with views of Mt. Kazbek 5047m. One of the world\'s best day trips. Leave at dawn — back in the evening.',
    includes:['Комфортный трансфер туда-обратно','Гид Тимур на весь маршрут','Входные билеты включены','Остановки для фото','Рекомендации по ресторанам в Казбеги'],
    includes_en:['Comfortable round-trip transfer','Guide Timur throughout','Entrance tickets included','Photo stops along the way','Restaurant tips in Kazbegi'],
    route:['07:00 — Выезд из Тбилиси','09:00 — Крепость Ананури: вид на водохранилище','10:30 — Гудаури: панорама Кавказского хребта','12:00 — Казбеги: обед (по выбору)','14:00 — Гергетская Троица (пешком или джип)','16:30 — Свободное время в горах','19:30 — Возвращение в Тбилиси'],
    route_en:['07:00 — Departure from Tbilisi','09:00 — Ananuri fortress &amp; reservoir views','10:30 — Gudauri: Caucasus panorama','12:00 — Kazbegi: lunch (your choice)','14:00 — Gergeti Trinity Church (hike or jeep)','16:30 — Free time in the mountains','19:30 — Return to Tbilisi'],
    wa:'Хочу+забронировать+Казбеги+за+1+день',wa_en:'I+want+to+book+Kazbegi+in+1+day'
  },
  'tbilisi-hidden':{
    badge:'live',img:'/images/tbilisi-hidden.webp',
    cat:'По городу · 5–6 ч',name:'Скрытые места Тбилиси',gel:'от ₾100',usd:'from $38',
    cat_en:'City tour · 5–6 h',name_en:'Hidden Tbilisi',
    desc:'Дворы-колодцы, серные бани, армянский квартал. Тбилиси, которого нет в путеводителе. Покажем кофейню в подворотне, галерею без вывески, хинкали не для туристов.',
    desc_en:'Hidden courtyards, sulfur baths, Armenian quarter. The Tbilisi not in any guidebook. We\'ll show you the coffee shop in the alley, the unmarked gallery, the real khinkali spot.',
    includes:['Гид Тимур 5–6 часов','Маршрут по нетуристическому Тбилиси','Кофе в местном кафе включён','Трансфер между локациями','Список мест для самостоятельного посещения'],
    includes_en:['Guide Timur for 5–6 hours','Off-the-beaten-path Tbilisi route','Coffee at a local café included','Transfer between locations','Spot list to revisit on your own'],
    route:['Сололаки: балконы, дворы, истории домов','Абанотубани: серные бани изнутри и снаружи','Армянский квартал: церкви, тишина, фрески','Улица Шарден: местный арт без вывески','Нарикала: панорама без толпы'],
    route_en:['Sololaki: balconies, courtyards, house stories','Abanotubani: sulfur baths inside &amp; out','Armenian quarter: churches, silence, frescoes','Sharden St: local art off the tourist trail','Narikala: panorama without the crowds'],
    wa:'Хочу+забронировать+Скрытые+места+Тбилиси',wa_en:'I+want+to+book+Hidden+Tbilisi+tour'
  },
  'old-tbilisi':{
    badge:'live',img:'/images/old-tbilisi-tour.webp',
    cat:'По городу · 3–4 ч',name:'Старый Тбилиси',gel:'₾71',usd:'$27',
    cat_en:'City tour · 3–4 h',name_en:'Old Tbilisi',
    desc:'Классический маршрут по историческому центру — для тех, кто в Тбилиси впервые или хочет понять город. Серные бани, Нарикала, Мецехи, главные легенды и истории.',
    desc_en:'Classic route through the historic center — for first-timers or anyone who wants to truly understand the city. Sulfur baths, Narikala, Metekhi, key legends and stories.',
    includes:['Гид Тимур 3–4 часа','Все главные точки Старого города','Истории и легенды каждого места','Трансфер включён'],
    includes_en:['Guide Timur for 3–4 hours','All key Old Town landmarks','Stories &amp; legends of each place','Transfer included'],
    route:['Мост Мира и набережная','Абанотубани (серные бани)','Нарикала: крепость и вид на город','Метехи: церковь над Курой','Старый базар: специи, сладости, атмосфера'],
    route_en:['Bridge of Peace &amp; embankment','Abanotubani (sulfur baths)','Narikala: fortress &amp; city views','Metekhi: church above the Mtkvari','Old Bazaar: spices, sweets, atmosphere'],
    wa:'Хочу+забронировать+Старый+Тбилиси',wa_en:'I+want+to+book+Old+Tbilisi+tour'
  },
  kakheti:{
    badge:'live',img:'/images/kakheti-tour.webp',
    cat:'Выезд · 10–12 ч',name:'Сигнаги и Кахетия',gel:'₾128',usd:'$49',
    cat_en:'Day trip · 10–12 h',name_en:'Signagi & Kakheti',
    desc:'Город любви Сигнаги, монастырь Бодбе, дегустация квеври-вина в семейном марани и обед у хозяйки. Самый живописный регион Грузии — виноградники, горы, золотая осень круглый год.',
    desc_en:'City of love Signagi, Bodbe monastery, qvevri wine tasting at a family winery, and lunch at a local home. Georgia\'s most scenic region — vineyards, mountains, golden landscapes.',
    includes:['Трансфер Тбилиси ↔ Кахетия','Гид Тимур на весь день','Дегустация вин в семейном марани','Домашний обед включён','Входные билеты в монастырь'],
    includes_en:['Transfer Tbilisi ↔ Kakheti','Guide Timur for the full day','Wine tasting at a family winery','Home-cooked lunch included','Monastery entrance tickets'],
    route:['09:00 — Выезд из Тбилиси','11:00 — Монастырь Бодбе: история и виноградники','12:30 — Сигнаги: город-крепость, виды на Алазанскую долину','14:00 — Обед в семейном доме + дегустация вин','16:00 — Телави или Греми (по выбору)','19:30 — Возвращение в Тбилиси'],
    route_en:['09:00 — Departure from Tbilisi','11:00 — Bodbe monastery: history &amp; vineyards','12:30 — Signagi: fortress-town, Alazani valley views','14:00 — Lunch at a family home + wine tasting','16:00 — Telavi or Gremi (your choice)','19:30 — Return to Tbilisi'],
    wa:'Хочу+забронировать+Кахетия+тур',wa_en:'I+want+to+book+Kakheti+tour'
  },
  emigrant:{
    badge:'hot',img:'/images/emigrant-tour.webp',
    cat:'Для своих · 3–4 ч',name:'Тур для эмигрантов',gel:'₾83',usd:'$31',
    cat_en:'For expats · 3–4 h',name_en:'Expat Tour',
    desc:'Тайные бары, местные рынки, районы где живут грузины. Для тех, кто переехал в Тбилиси надолго. Покажем город без туристического фасада — где снимать квартиру, где есть, как жить.',
    desc_en:'Hidden bars, local markets, neighborhoods where Georgians actually live. For those who\'ve moved to Tbilisi long-term. We show the city without the tourist facade — where to rent, eat, live.',
    includes:['Гид Тимур — сам релокант','Маршрут по районам Тбилиси для жизни','Список локальных заведений','Практические советы по жизни в Грузии'],
    includes_en:['Guide Timur — a fellow expat','Route through Tbilisi\'s liveable neighborhoods','List of local spots','Practical tips for life in Georgia'],
    route:['Ваке: лучший район для жизни — плюсы и минусы','Рынок Дезертирка: как покупают местные','Районы Глдани и Сабуртало: настоящий Тбилиси','Тайный бар без вывески','Кафе и коворкинги для удалёнщиков'],
    route_en:['Vake: best neighborhood for living — pros &amp; cons','Dezerter Bazaar: how locals shop','Gldani &amp; Saburtalo: the real Tbilisi','Hidden bar with no sign','Cafés &amp; coworking for remote workers'],
    wa:'Хочу+забронировать+Тур+для+эмигрантов',wa_en:'I+want+to+book+Expat+Tour'
  },
  'digital-nomad':{
    badge:'live',img:'/images/digital-nomad-tour.webp',
    cat:'Digital Nomad · 3 ч',name:'Digital Nomad Welcome Tour',gel:'₾83',usd:'$31',
    cat_en:'Digital Nomad · 3 h',name_en:'Digital Nomad Welcome Tour',
    desc:'3 часа на английском: лучшие коворкинги, кафе с быстрым WiFi, районы для удалёнщиков. Идеально для первой недели в Тбилиси. Покажем где работать, жить и тусоваться.',
    desc_en:'3 hours in English: best coworking spaces, fast-WiFi cafés, nomad-friendly neighborhoods. Perfect for your first week in Tbilisi. We show you where to work, live, and hang out.',
    includes:['Гид на английском языке','Топ коворкингов с ценами и скоростью WiFi','Список кафе для работы','Районы для аренды жилья','Nomad-сообщества в Тбилиси'],
    includes_en:['English-speaking guide','Top coworking spaces with prices &amp; WiFi speeds','Best cafés for working','Neighborhoods for renting','Nomad communities in Tbilisi'],
    route:['Коворкинги центра: обзор и демо','Районы с хорошим интернетом и жильём','Кафе для работы с ноутбуком','SIM-карта, банки, лайфхаки для первой недели','Q&amp;A — все вопросы про жизнь в Тбилиси'],
    route_en:['Central coworking spaces: overview &amp; demo','Best neighborhoods for WiFi &amp; renting','Laptop-friendly cafés','SIM card, banks, tips for week one','Q&amp;A — all questions about living in Tbilisi'],
    wa:'Хочу+забронировать+Digital+Nomad+Tour',wa_en:'I+want+to+book+Digital+Nomad+Tour'
  }
}

function openTourModal(id){
  const t=TOURS[id]; if(!t)return
  const el=n=>document.getElementById(n)
  const isEn=document.documentElement.lang==='en'
  el('tm-img').src=t.img; el('tm-img').alt=isEn&&t.name_en?t.name_en:t.name
  el('tm-badge').className=t.badge; el('tm-badge').textContent=t.badge==='hot'?(isEn?'Hit':'Хит'):(isEn?'Available':'Доступно')
  el('tm-cat').textContent=isEn&&t.cat_en?t.cat_en:t.cat
  el('tm-name').textContent=isEn&&t.name_en?t.name_en:t.name
  el('tm-desc').textContent=isEn&&t.desc_en?t.desc_en:t.desc
  el('tm-gel').textContent=isEn?t.usd:t.gel
  const inc=isEn&&t.includes_en?t.includes_en:t.includes
  const rte=isEn&&t.route_en?t.route_en:t.route
  el('tm-includes').innerHTML=inc.map(s=>`<div class="tm-item">${s}</div>`).join('')
  el('tm-route').innerHTML=rte.map(s=>`<div class="tm-item">${s}</div>`).join('')
  el('tm-wa').href=`https://wa.me/995511272623?text=${isEn&&t.wa_en?t.wa_en:t.wa}`
  el('tm').classList.add('open')
  document.body.style.overflow='hidden'
}
function closeTourModal(){
  document.getElementById('tm').classList.remove('open')
  document.body.style.overflow=''
}
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeTourModal()})

// Hero video: play immediately, retry on canplay
const hv=document.getElementById('hero-video')
if(hv){
  const hvPlay=()=>hv.play().catch(()=>{})
  hv.addEventListener('canplay',hvPlay,{once:true})
  hvPlay()
  setTimeout(hvPlay,300)
  const tap=document.getElementById('hero-tap')
  if(tap){
    tap.addEventListener('touchstart',function(){hvPlay();tap.style.display='none'},{once:true,passive:true})
    tap.addEventListener('click',function(){hvPlay();tap.style.display='none'},{once:true})
  }
}

// CTA video: lazy load when near viewport (saves 13MB on initial load)
const ctaVid=document.getElementById('cta-video')
if(ctaVid){
  const ctaObs=new IntersectionObserver(entries=>{
    if(entries[0].isIntersecting){
      if(!ctaVid.src){
        ctaVid.src=ctaVid.dataset.src
        ctaVid.load()
      }
      ctaVid.play().catch(()=>{})
      ctaObs.disconnect()
    }
  },{rootMargin:'200px'})
  ctaObs.observe(ctaVid)
}

// Scroll reveal
const ro=new IntersectionObserver(e=>{
  e.forEach(x=>{if(x.isIntersecting)x.target.classList.add('on')})
},{threshold:.05,rootMargin:'0px 0px 60px 0px'})
document.querySelectorAll('.reveal').forEach(el=>ro.observe(el))
// Fallback: если через 3с ещё не показано — показываем всё
setTimeout(()=>document.querySelectorAll('.reveal:not(.on)').forEach(el=>el.classList.add('on')),3000)

// Counter
const co=new IntersectionObserver(e=>{
  e.forEach(x=>{
    if(x.isIntersecting&&!x.target.dataset.done){
      x.target.dataset.done=1
      const t=+x.target.dataset.target,d=1600,s=performance.now()
      const run=n=>{
        const p=Math.min((n-s)/d,1)
        x.target.textContent=Math.round(p*p*t)+(t>=500?'+':'')
        if(p<1)requestAnimationFrame(run)
      }
      requestAnimationFrame(run)
    }
  })
},{threshold:.5})
document.querySelectorAll('.counter').forEach(el=>co.observe(el))

// Burger
const burger=document.getElementById('burger'),drawer=document.getElementById('drawer')
burger.addEventListener('click',()=>{
  const o=drawer.classList.toggle('on')
  burger.classList.toggle('on',o)
  document.body.style.overflow=o?'hidden':''
})
function closeDrawer(){drawer.classList.remove('on');burger.classList.remove('on');document.body.style.overflow=''}

// FAQ
function toggleFaq(btn){
  const item=btn.closest('.fi'),isOpen=item.classList.contains('open')
  document.querySelectorAll('.fi.open').forEach(i=>{
    i.classList.remove('open');i.querySelector('.fa').style.maxHeight=null
  })
  if(!isOpen){
    item.classList.add('open')
    const ans=item.querySelector('.fa')
    ans.style.maxHeight=ans.scrollHeight+'px'
  }
}

// Language switcher
function setLang(lang){
  document.querySelectorAll('[data-ru],[data-en]').forEach(function(el){
    var val=el.dataset[lang]
    if(val!==undefined){
      if(el.tagName==='INPUT'||el.tagName==='TEXTAREA') el.placeholder=val
      else el.innerHTML=val
    }
  })
  // ── Sync currency with language ──
  var GEL_RUB=35
  var curr=lang==='en'?'usd':(localStorage.getItem('curr_v1')||'gel')
  if(lang==='en') localStorage.setItem('curr_v1','usd')
  document.querySelectorAll('.price-main[data-gel]').forEach(function(el){
    var gel=+(el.dataset.gel||'0').replace(/[^\d]/g,'')
    var usdNum=+(el.dataset.usd||'0').replace(/[^\d]/g,'')
    if(curr==='gel') el.textContent=el.dataset.gel
    else if(curr==='usd') el.textContent='$'+usdNum
    else el.textContent='₽'+(gel*GEL_RUB).toLocaleString('ru-RU')
  })
  var sw=document.getElementById('cs-main')
  if(sw) sw.querySelectorAll('.curr-btn').forEach(function(b){b.classList.toggle('active',b.dataset.curr===curr)})
  document.querySelectorAll('[data-wa-ru]').forEach(function(el){
    var txt=lang==='en'?el.dataset.waEn:el.dataset.waRu
    if(txt) el.href='https://wa.me/995511272623?text='+txt
  })
  // nav buttons
  var bRu=document.getElementById('btnRu'),bEn=document.getElementById('btnEn')
  if(bRu) bRu.classList.toggle('on',lang==='ru')
  if(bEn) bEn.classList.toggle('on',lang==='en')
  // drawer buttons
  var dRu=document.getElementById('dBtnRu'),dEn=document.getElementById('dBtnEn')
  if(dRu){dRu.style.background=lang==='ru'?'#1A56DB':'#fff';dRu.style.color=lang==='ru'?'#fff':'#1A56DB'}
  if(dEn){dEn.style.background=lang==='en'?'#1A56DB':'#fff';dEn.style.color=lang==='en'?'#fff':'#1A56DB'}
  document.documentElement.lang=lang==='en'?'en':'ru'
  localStorage.setItem('lang',lang)
}
// Keyboard: Alt+L toggles RU/EN
document.addEventListener('keydown',function(e){
  if(e.altKey&&e.key==='l'||e.altKey&&e.key==='L'||e.altKey&&e.key==='д'||e.altKey&&e.key==='Д'){
    setLang(document.documentElement.lang==='en'?'ru':'en')
  }
})
// Restore saved language
var savedLang=localStorage.getItem('lang')
if(savedLang&&savedLang!=='ru') setLang(savedLang)

// ── COOKIE ──
function acceptCookies(){
  localStorage.setItem('cookies_v4','1');
  gtag('consent','update',{analytics_storage:'granted',ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted'});
  document.getElementById('cookie-bar').classList.remove('show');document.body.classList.remove('cookie-visible')
}
function declineCookies(){
  localStorage.setItem('cookies_v4','0');
  gtag('consent','update',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});
  document.getElementById('cookie-bar').classList.remove('show');document.body.classList.remove('cookie-visible')
}
if(!localStorage.getItem('cookies_v4'))setTimeout(()=>{document.getElementById('cookie-bar').classList.add('show');document.body.classList.add('cookie-visible')},1500)

// ── CONTACT MODAL ──
// ── PAYMENT MODAL ──
// Payment state
var pmSt={tourId:'',tourName:'',guests:1,amtUsd:0,amtRub:0}

function openPayment(tourId,tourName,guests,amtUsd,amtRub){
  var sel=document.getElementById('pm-tour-sel')
  var info=document.getElementById('pm-amount-info')
  if(tourId&&amtUsd){
    pmSt={tourId:tourId,tourName:tourName,guests:guests||1,amtUsd:amtUsd,amtRub:amtRub||Math.round(amtUsd*90)}
    if(sel)sel.style.display='none'
    if(info){info.style.display='block';info.textContent=tourName+' · '+guests+' чел. · $'+amtUsd+' / ₽'+pmSt.amtRub}
  } else {
    pmSt={tourId:'',tourName:'',guests:1,amtUsd:0,amtRub:0}
    if(sel)sel.style.display='block'
    if(info)info.style.display='none'
    pmBuildTourSelect()
  }
  document.getElementById('pm-modal').classList.add('open')
  document.body.style.overflow='hidden'
}
function closePayment(){document.getElementById('pm-modal').classList.remove('open');document.body.style.overflow=''}
function pmBuildTourSelect(){
  var s=document.getElementById('pm-tour-pick')
  if(!s)return
  s.innerHTML='<option value="">— выберите тур —</option>'
  BK_TOURS.filter(t=>t.price_usd>0).forEach(function(t){
    var o=document.createElement('option')
    o.value=t.id;o.textContent=t.name+' — $'+t.price_usd
    s.appendChild(o)
  })
}
function pmCalcAmount(){
  var s=document.getElementById('pm-tour-pick')
  var g=parseInt(document.getElementById('pm-guests-pick').value)||1
  var t=s?BK_TOURS.find(function(x){return x.id===s.value}):null
  var info=document.getElementById('pm-amount-info')
  if(t&&t.price_usd){
    pmSt={tourId:t.id,tourName:t.name,guests:g,amtUsd:t.price_usd*g,amtRub:t.price_rub*g}
    if(info){info.style.display='block';info.textContent=t.name+' · '+g+' чел. · $'+pmSt.amtUsd+' / ₽'+pmSt.amtRub}
  } else {
    if(info)info.style.display='none'
    pmSt.amtUsd=0
  }
}
async function pmSelect(type){
  const isEn=document.documentElement.lang==='en'
  if(type==='card'){
    const msg=isEn
      ?'I want to pay by Visa/Mastercard for a tour'
      :'Хочу оплатить картой Visa/Mastercard'+(pmSt.tourName?' — '+pmSt.tourName:'')
    window.open('https://wa.me/995511272623?text='+encodeURIComponent(msg),'_blank')
    closePayment()
    return
  }
  if(!pmSt.amtUsd){
    alert(isEn?'Please select a tour':'Выберите тур')
    return
  }
  var btns=document.querySelectorAll('.pm-opt')
  btns.forEach(function(b){b.disabled=true;b.style.opacity='0.55'})
  try{
    if(type==='crypto'){
      var r=await fetch('/api/create-payment/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({amount:pmSt.amtUsd,description:pmSt.tourName+' · '+pmSt.guests+' pax',orderId:'SAKHVA-'+Date.now()})})
      var d=await r.json()
      if(d.invoiceUrl){window.open(d.invoiceUrl,'_blank');closePayment()}
      else alert('Ошибка: '+(d.error||'попробуйте позже'))
    } else if(type==='yoo'){
      var r=await fetch('/api/create-yoo-payment/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({amount:pmSt.amtRub,description:pmSt.tourName+' · '+pmSt.guests+' чел.',orderId:'SAKHVA-'+Date.now()})})
      var d=await r.json()
      if(d.confirmationUrl){window.location.href=d.confirmationUrl}
      else alert('Ошибка: '+(d.error||'попробуйте позже'))
    }
  }catch(e){alert(isEn?'Network error, try again':'Ошибка сети, попробуйте ещё раз')}
  finally{btns.forEach(function(b){b.disabled=false;b.style.opacity=''})}
}
document.addEventListener('keydown',function(e){if(e.key==='Escape')closePayment()})

function openContact(){document.getElementById('contact-modal').classList.add('open');document.body.style.overflow='hidden'}
function closeContact(){document.getElementById('contact-modal').classList.remove('open');document.body.style.overflow=''}
function sendContact(){
  const name=document.getElementById('cm-name').value.trim()
  const phone=document.getElementById('cm-phone').value.trim()
  const tour=document.getElementById('cm-tour').value
  const msg=document.getElementById('cm-msg').value.trim()
  let text=`Привет Тимур!`
  if(name) text+=` Меня зовут ${name}.`
  if(tour) text+=` Интересует: ${tour}.`
  if(msg) text+=` ${msg}`
  if(phone) text+=` Мой номер: ${phone}`
  window.open(`https://wa.me/995511272623?text=${encodeURIComponent(text)}`)
  closeContact()
}

// ── BOOKING MODAL ──
// === Config: add booked dates as 'YYYY-MM-DD' strings ===
const BOOKING_BUSY=[]  // e.g. ['2026-04-10','2026-04-15']
const FORMSPREE_ID='mzdkyywe'

const BK_TOURS=[
  {id:'kazbegi',      icon:'🏔️',name:'Казбеги за 1 день',         name_en:'Kazbegi in 1 day',           price:'₾128 / чел.', price_en:'$49 / person',  price_usd:49,  price_rub:4500},
  {id:'tbilisi-hidden',icon:'🏙️',name:'Скрытые места Тбилиси',  name_en:'Hidden Tbilisi',              price:'от ₾100 / чел.',price_en:'from $38 / person',price_usd:38,price_rub:3500},
  {id:'old-tbilisi',  icon:'🕌',name:'Старый Тбилиси',           name_en:'Old Tbilisi',                 price:'₾71 / чел.',  price_en:'$27 / person',  price_usd:27,  price_rub:2500},
  {id:'kakheti',      icon:'🍷',name:'Кахетия — вино и природа', name_en:'Kakheti — wine & nature',     price:'₾128 / чел.', price_en:'$49 / person',  price_usd:49,  price_rub:4500},
  {id:'emigrant',     icon:'🛖',name:'Тур для эмигрантов',       name_en:'Expat Tour',                  price:'₾83 / чел.',  price_en:'$31 / person',  price_usd:31,  price_rub:2900},
  {id:'night-tbilisi',icon:'🌙',name:'Ночной Тбилиси',          name_en:'Night Tbilisi',                price:'₾71 / чел.',  price_en:'$27 / person',  price_usd:27,  price_rub:2500},
  {id:'dinner',       icon:'🍽️',name:'Тур + ужин у местных',    name_en:'Tour + dinner with locals',   price:'₾185 / чел.', price_en:'$71 / person',  price_usd:71,  price_rub:6500},
  {id:'soviet',       icon:'🎭',name:'Советский Тбилиси',        name_en:'Soviet Tbilisi',              price:'₾86 / чел.',  price_en:'$32 / person',  price_usd:32,  price_rub:2900},
  {id:'slow-travel',  icon:'✈️',name:'Slow Travel 3 дня',       name_en:'Slow Travel 3 days',          price:'₾424 / чел.', price_en:'$161 / person', price_usd:161, price_rub:14900},
  {id:'photo',        icon:'📸',name:'Тур + фотосессия',         name_en:'Tour + photo session',        price:'₾196 / чел.', price_en:'$75 / person',  price_usd:75,  price_rub:6900},
  {id:'digital-nomad',icon:'💻',name:'Digital Nomad Tour',      name_en:'Digital Nomad Tour',           price:'₾83 / чел.',  price_en:'$31 / person',  price_usd:31,  price_rub:2900},
  {id:'mtskheta',     icon:'⛪',name:'Мцхета — древняя столица',name_en:'Mtskheta — Ancient Capital',  price:'₾40 / чел.',  price_en:'$15 / person',  price_usd:15,  price_rub:1390},
  {id:'other',        icon:'💬',name:'Другой маршрут / обсудить',name_en:'Custom route / discuss',      price:'',            price_en:'',               price_usd:0,   price_rub:0}
]
const bkSt={tour:'',tourName:'',date:'',calY:0,calM:0}

function openBooking(tourId){
  const isEn=document.documentElement.lang==='en'
  const modal=document.getElementById('booking-modal')
  modal.classList.add('open')
  document.body.style.overflow='hidden'
  const now=new Date()
  bkSt.calY=now.getFullYear();bkSt.calM=now.getMonth()
  bkSt.date='';bkSt.tour=tourId||'';bkSt.tourName=''
  // render tour list
  const list=document.getElementById('bm-tour-list')
  list.innerHTML=''
  BK_TOURS.forEach(t=>{
    const div=document.createElement('div')
    div.className='bm-tour'+(bkSt.tour===t.id?' sel':'')
    div.onclick=()=>bmPickTour(t.id,isEn?t.name_en:t.name)
    div.innerHTML='<span class="bm-tour-icon">'+t.icon+'</span><div><div class="bm-tour-name">'+(isEn?t.name_en:t.name)+'</div>'+(t.price?'<div class="bm-tour-price">'+(isEn?t.price_en:t.price)+'</div>':'')+'</div>'
    list.appendChild(div)
  })
  const n1=document.getElementById('bm-next1')
  if(tourId){
    const t=BK_TOURS.find(x=>x.id===tourId)
    if(t){bkSt.tourName=isEn?t.name_en:t.name;list.querySelectorAll('.bm-tour').forEach((el,i)=>{el.classList.toggle('sel',BK_TOURS[i].id===tourId)})}
    n1.disabled=false
  } else {n1.disabled=true}
  bmShowStep(1)
}
function closeBooking(){
  document.getElementById('booking-modal').classList.remove('open')
  document.body.style.overflow=''
}
function bmShowStep(n){
  document.querySelectorAll('.bm-step').forEach(s=>s.classList.remove('active'))
  document.querySelector('.bm-step[data-bstep="'+n+'"]').classList.add('active')
  document.getElementById('bm-bar').style.width=(n/4*100)+'%'
  if(n===2)bmRenderCal()
}
function bmStep(n){bmShowStep(n)}
function bmPickTour(id,name){
  bkSt.tour=id;bkSt.tourName=name
  document.querySelectorAll('.bm-tour').forEach((el,i)=>el.classList.toggle('sel',BK_TOURS[i].id===id))
  document.getElementById('bm-next1').disabled=false
}
function bmCalNav(dir){
  bkSt.calM+=dir
  if(bkSt.calM>11){bkSt.calM=0;bkSt.calY++}
  if(bkSt.calM<0){bkSt.calM=11;bkSt.calY--}
  bmRenderCal()
}
function bmRenderCal(){
  const isEn=document.documentElement.lang==='en'
  const MN_RU=['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
  const MN_EN=['January','February','March','April','May','June','July','August','September','October','November','December']
  const y=bkSt.calY,m=bkSt.calM
  document.getElementById('bcal-month-label').textContent=(isEn?MN_EN:MN_RU)[m]+' '+y
  const grid=document.getElementById('bcal-grid')
  grid.innerHTML=''
  const today=new Date();today.setHours(0,0,0,0)
  let startDay=new Date(y,m,1).getDay()-1;if(startDay<0)startDay=6
  const days=new Date(y,m+1,0).getDate()
  for(let i=0;i<startDay;i++){const d=document.createElement('div');d.className='bcal-day empty';grid.appendChild(d)}
  for(let day=1;day<=days;day++){
    const date=new Date(y,m,day)
    const ds=y+'-'+String(m+1).padStart(2,'0')+'-'+String(day).padStart(2,'0')
    const d=document.createElement('div');d.textContent=day
    if(date<today){d.className='bcal-day past'}
    else if(BOOKING_BUSY.includes(ds)){d.className='bcal-day busy';d.title=isEn?'Booked':'Занято'}
    else{
      d.className='bcal-day avail'+(bkSt.date===ds?' selected':'')
      d.onclick=()=>{
        bkSt.date=ds
        grid.querySelectorAll('.bcal-day').forEach(el=>el.classList.remove('selected'))
        d.classList.add('selected')
        document.getElementById('bm-next2').disabled=false
      }
    }
    grid.appendChild(d)
  }
}
async function bmSubmit(){
  const name=document.getElementById('bm-name').value.trim()
  const email=document.getElementById('bm-email').value.trim()
  const phone=document.getElementById('bm-phone').value.trim()
  const guests=document.getElementById('bm-guests').value
  const note=document.getElementById('bm-note').value.trim()
  if(!name){document.getElementById('bm-name').focus();return}
  const isEn=document.documentElement.lang==='en'
  const [dy,dm,dd]=bkSt.date.split('-')
  const MO_RU=['янв','фев','мар','апр','май','июн','июл','авг','сен','окт','ноя','дек']
  const MO_EN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  const dateFmt=dd+' '+(isEn?MO_EN:MO_RU)[parseInt(dm)-1]+' '+dy
  if(FORMSPREE_ID){
    try{await fetch('https://formspree.io/f/'+FORMSPREE_ID,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify({tour:bkSt.tourName,date:dateFmt,guests,name,email,phone,note})})}catch(e){}
  }
  document.getElementById('bm-success-meta').textContent=bkSt.tourName+' · '+dateFmt+' · '+guests+(isEn?' pax':' чел.')
  // Pre-fill payment state from booking
  var t=BK_TOURS.find(function(x){return x.id===bkSt.tour})
  if(t&&t.price_usd){
    var gNum=parseInt(guests)||1
    pmSt={tourId:t.id,tourName:t.name,guests:gNum,amtUsd:t.price_usd*gNum,amtRub:t.price_rub*gNum}
  }
  bmShowStep(4)
}

function bmPayOnline(type){
  closeBooking()
  if(pmSt.amtUsd>0){
    var info=document.getElementById('pm-amount-info')
    var sel=document.getElementById('pm-tour-sel')
    if(sel)sel.style.display='none'
    if(info){info.style.display='block';info.textContent=pmSt.tourName+' · '+pmSt.guests+' чел. · $'+pmSt.amtUsd+' / ₽'+pmSt.amtRub}
    document.getElementById('pm-modal').classList.add('open')
    document.body.style.overflow='hidden'
    pmSelect(type)
  } else {
    openPayment()
  }
}

// ── QUIZ ──
const qAns={}
function openQuiz(){document.getElementById('quiz-modal').classList.add('open');document.body.style.overflow='hidden';showStep(1)}
function closeQuiz(){document.getElementById('quiz-modal').classList.remove('open');document.body.style.overflow=''}
function showStep(n){
  document.querySelectorAll('.qm-step').forEach(s=>s.classList.remove('active'))
  document.querySelector(`.qm-step[data-step="${n}"]`).classList.add('active')
  document.getElementById('qm-bar').style.width=Math.min((n-1)/4*100,100)+'%'
}
function quizPick(step,val,label){
  qAns[step]=val
  if(step<4){showStep(step+1)}
  else{showResult()}
}
function showResult(){
  const a2=qAns[2],a3=qAns[3],a4=qAns[4]
  let icon='🏔️',title='',sub='',waText=''
  const isEn=document.documentElement.lang==='en'
  // Base tour by destination
  if(a2==='mountains'){icon='🏔️';title=isEn?'Kazbegi in 1 day':'Казбеги за 1 день';sub=isEn?'Mountains, waterfalls, Gergeti fortress. From $49/person.':'Горы, водопады, крепость Гергети. От ₾128 с человека.';waText='Хочу тур Казбеги'}
  else if(a2==='wine'){icon='🍷';title=isEn?'Kakheti — wine & gastronomy':'Кахетия — вино и гастрономия';sub=isEn?'Monasteries, vineyards, tastings. From $49.':'Монастыри, виноградники, дегустации. От ₾128.';waText='Хочу тур Кахетия'}
  else if(a2==='city'){icon='🏙️';title=isEn?'Hidden Tbilisi':'Скрытые места Тбилиси';sub=isEn?'Courtyards, sulfur baths, local cafes. From $38.':'Дворики, серные бани, кафе без вывески. От ₾100.';waText='Хочу тур Скрытые места Тбилиси'}
  else{icon='🛖';title=isEn?'Expat Tour':'Тур для эмигрантов';sub=isEn?'Local life, markets, secret bars. From $31.':'Местная жизнь, рынки, тайные бары. От ₾83.';waText='Хочу Тур для эмигрантов'}
  document.getElementById('qm-icon').textContent=icon
  document.getElementById('qm-rtitle').textContent=title
  document.getElementById('qm-rsub').textContent=sub
  // Features based on format (a3) and budget (a4)
  const featMap={
    max:isEn?'⚡ Packed itinerary — maximum sights in one day':'⚡ Насыщенный маршрут — максимум мест за день',
    slow:isEn?'🧘 Relaxed pace — no rush, time to absorb':'🧘 Неспешный темп — без суеты, всё прочувствуем',
    photo:isEn?'📸 Instagram spots + photographer tips included':'📸 Фотолокации + советы по съёмке включены',
    food:isEn?'🍽️ Local tastings & restaurant stops included':'🍽️ Дегустации и остановки в местных заведениях',
    local:isEn?'🛖 Off the tourist trail — real local experience':'🛖 В стороне от туристических троп — настоящая жизнь'
  }
  const budgetMap={
    low:isEn?'💚 Best value option available':'💚 Оптимальный вариант по цене',
    mid:isEn?'💛 Includes private transport & lunch stop':'💛 Включает трансфер и обед',
    high:isEn?'💎 Premium: small group, all meals, priority stops':'💎 Премиум: малая группа, питание, лучшие места',
    any:isEn?'✨ Full experience — we\'ll match you perfectly':'✨ Полное погружение — подберём идеально'
  }
  const feats=document.getElementById('qm-features')
  feats.innerHTML=''
  if(a3&&featMap[a3]){const d=document.createElement('div');d.style.cssText='display:flex;align-items:flex-start;gap:8px;font-size:13px;color:#374151;background:#F3F4F6;padding:8px 12px;border-radius:8px';d.textContent=featMap[a3];feats.appendChild(d)}
  if(a4&&budgetMap[a4]){const d=document.createElement('div');d.style.cssText='display:flex;align-items:flex-start;gap:8px;font-size:13px;color:#374151;background:#F3F4F6;padding:8px 12px;border-radius:8px';d.textContent=budgetMap[a4];feats.appendChild(d)}
  const waFull=waText+(a3?(' | '+featMap[a3].replace(/[^\w\sА-яЁё,—]/gu,'').trim()):'')
  document.getElementById('qm-wa-link').href=`https://wa.me/995511272623?text=${encodeURIComponent(waFull)}`
  document.getElementById('qm-bar').style.width='100%'
  showStep(5)
}
function restartQuiz(){Object.keys(qAns).forEach(k=>delete qAns[k]);showStep(1)}

// ── TOUR FILTER ──
function filterTours(tab,cat){
  document.querySelectorAll('.ftab').forEach(t=>t.classList.remove('on'))
  tab.classList.add('on')
  document.querySelectorAll('#allGrid .atc').forEach(c=>{
    c.classList.toggle('hidden',cat!=='все'&&c.dataset.cat!==cat)
  })
}

// ── SMOOTH SCROLL (anchor links) ──
;(function(){
  function easeInOutQuart(t){return t<.5?8*t*t*t*t:1-Math.pow(-2*t+2,4)/2}
  function smoothScrollTo(y,dur){
    const s=window.scrollY,d=y-s;let t0=null
    function step(ts){
      if(!t0)t0=ts
      const p=Math.min((ts-t0)/dur,1)
      window.scrollTo(0,s+d*easeInOutQuart(p))
      if(p<1)requestAnimationFrame(step)
    }
    requestAnimationFrame(step)
  }
  document.addEventListener('click',e=>{
    const a=e.target.closest('a[href^="#"]')
    if(!a)return
    const id=a.getAttribute('href').slice(1)
    if(!id)return
    const el=document.getElementById(id)
    if(!el)return
    e.preventDefault()
    smoothScrollTo(el.getBoundingClientRect().top+window.scrollY-80,680)
  })
})()

// ── TOUR SCROLL ── (arrows only, native CSS scroll)


// ── FORTUNE CARD (handled by IIFE below) ──
// ── Video sound toggle ──
function toggleSound(){
  var v=document.getElementById('timurVideo')
  var b=document.getElementById('soundBtn')
  if(!v||!b)return
  v.muted=!v.muted
  const isEn=document.documentElement.lang==='en'
  b.textContent=v.muted?(isEn?'🔇 Sound':'🔇 Звук'):(isEn?'🔊 Sound on':'🔊 Звук вкл')
  b.style.background=v.muted?'rgba(0,0,0,.55)':'rgba(26,86,219,.8)'
}



// ── Load timurVideo with IntersectionObserver (mobile = smaller file) ──
(function(){
  var tv = document.getElementById('timurVideo');
  if(!tv) return;
  var src = window.innerWidth <= 768 ? '/images/timur-video-mobile.mp4' : '/images/timur-video.mp4';
  var obs = new IntersectionObserver(function(entries){
    if(entries[0].isIntersecting){
      if(!tv.src || tv.src === window.location.href){
        tv.src = src;
        tv.load();
        tv.play().catch(function(){});
      }
      obs.disconnect();
    }
  }, {threshold: 0.1});
  obs.observe(tv);
})();
// ── Scroll progress ──
const sp=document.getElementById('scroll-progress')
let _spH=document.body.scrollHeight-window.innerHeight
window.addEventListener('resize',()=>{_spH=document.body.scrollHeight-window.innerHeight},{passive:true})
let _rafPending=false
window.addEventListener('scroll',()=>{
  if(!_rafPending){_rafPending=true;requestAnimationFrame(()=>{if(_spH>0)sp.style.width=Math.min(window.scrollY/_spH*100,100)+'%';_rafPending=false})}
},{passive:true})

// ── Water ripple cursor ──
if(window.matchMedia('(pointer:fine)').matches){
  let _t=0
  document.addEventListener('mousemove',e=>{
    const now=Date.now()
    if(now-_t<200)return
    _t=now
    const r=document.createElement('div')
    r.className='wripple'
    r.style.cssText='left:'+e.clientX+'px;top:'+e.clientY+'px'
    const r2=document.createElement('div')
    r2.className='wripple wripple2'
    r2.style.cssText='left:'+e.clientX+'px;top:'+e.clientY+'px'
    document.body.appendChild(r)
    document.body.appendChild(r2)
    setTimeout(()=>{r.remove();r2.remove()},1300)
  },{passive:true})
}

// ── Button ripple ──
document.querySelectorAll('.btn-primary,.btn-wa,.btn-tg,.nav-btn').forEach(btn=>{
  btn.style.position='relative';btn.style.overflow='hidden'
  btn.addEventListener('click',e=>{
    const r=document.createElement('span')
    const d=Math.max(btn.offsetWidth,btn.offsetHeight)
    const rect=btn.getBoundingClientRect()
    r.className='ripple';r.style.cssText=`width:${d}px;height:${d}px;left:${e.clientX-rect.left-d/2}px;top:${e.clientY-rect.top-d/2}px`
    btn.appendChild(r);setTimeout(()=>r.remove(),600)
  })
})

// ── Card 3D tilt (desktop) ──
if(window.matchMedia('(pointer:fine)').matches){
  document.querySelectorAll('.tc,.atc').forEach(card=>{
    card.addEventListener('mousemove',e=>{
      const rect=card.getBoundingClientRect()
      const x=((e.clientX-rect.left)/rect.width-.5)*10
      const y=-((e.clientY-rect.top)/rect.height-.5)*8
      card.style.transform=`perspective(900px) rotateY(${x}deg) rotateX(${y}deg) translateY(-6px)`
    })
    card.addEventListener('mouseleave',()=>{card.style.transform=''})
  })
}

// ── Why cards tilt ──
if(window.matchMedia('(pointer:fine)').matches){
  document.querySelectorAll('.wc,.rc,.hw').forEach(card=>{
    card.addEventListener('mousemove',e=>{
      const rect=card.getBoundingClientRect()
      const x=((e.clientX-rect.left)/rect.width-.5)*6
      const y=-((e.clientY-rect.top)/rect.height-.5)*5
      card.style.transform=`perspective(600px) rotateY(${x}deg) rotateX(${y}deg) translateY(-3px)`
    })
    card.addEventListener('mouseleave',()=>{card.style.transform=''})
  })
}

// ── Magnetic CTA buttons ──
document.querySelectorAll('.btn-primary,.btn-wa').forEach(btn=>{
  if(btn.id==='quiz-btn')return
  btn.addEventListener('mousemove',e=>{
    const rect=btn.getBoundingClientRect()
    const x=(e.clientX-rect.left-rect.width/2)*.2
    const y=(e.clientY-rect.top-rect.height/2)*.2
    btn.style.transform=`translate(${x}px,${y}px) translateY(-2px)`
  })
  btn.addEventListener('mouseleave',()=>{btn.style.transform=''})
})



// ── Currency Switcher ──
;(function(){
  const GEL_RUB=35
  const sw=document.getElementById('cs-main')
  if(!sw)return
  function updateAll(curr){
    document.querySelectorAll('.price-main[data-gel]').forEach(function(el){
      var gel=+(el.dataset.gel||'0').replace(/[^\d]/g,'')
      var usd=el.dataset.usd||(''+(Math.round(gel*0.37)))
      var usdNum=+(usd).replace(/[^\d]/g,'')
      if(curr==='gel')el.textContent=el.dataset.gel
      else if(curr==='usd')el.textContent='$'+usdNum
      else el.textContent='₽'+(gel*GEL_RUB).toLocaleString('ru-RU')
    })
  }
  sw.querySelectorAll('.curr-btn').forEach(function(btn){
    btn.addEventListener('click',function(){
      sw.querySelectorAll('.curr-btn').forEach(function(b){b.classList.remove('active')})
      btn.classList.add('active')
      localStorage.setItem('curr_v1',btn.dataset.curr)
      updateAll(btn.dataset.curr)
    })
  })
  var saved=localStorage.getItem('curr_v1')||'gel'
  if(saved!=='gel'){
    sw.querySelectorAll('.curr-btn').forEach(function(b){b.classList.toggle('active',b.dataset.curr===saved)})
    updateAll(saved)
  }
})()

// ── Google Reviews (live) ──
;(function(){
  const GOOGLE_SVG='<svg width="14" height="14" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>'
  function stars(n){return'★'.repeat(n)+'☆'.repeat(5-n)}
  function renderCard(r,i){
    const colors=['#1A56DB','#7C3AED','#059669','#DC2626','#D97706','#0891B2']
    const av=r.avatar
      ?`<img src="${r.avatar}" alt="${r.name}" width="40" height="40" style="width:40px;height:40px;border-radius:50%;object-fit:cover;flex-shrink:0;display:block">`
      :`<div class="rc-av" style="background:${colors[i%colors.length]}">${r.name.charAt(0).toUpperCase()}</div>`
    const delay=i>0?` style="transition-delay:${i*.1}s"`:''
    return`<div class="rc reveal"${delay}><div class="rc-source">${GOOGLE_SVG} Google</div><div class="rc-top">${av}<div><div class="rc-name">${r.name}</div><div class="rc-meta">${r.time}</div></div></div><div class="rc-stars" style="color:#F59E0B;font-size:12px;letter-spacing:1px;margin-bottom:10px">${stars(r.rating)}</div><p class="rc-text">${r.text}</p></div>`
  }
  fetch('/api/reviews').then(r=>r.ok?r.json():null).then(data=>{
    if(!data||data.error||!data.reviews||!data.reviews.length)return
    const grid=document.getElementById('rev-grid')
    if(grid){grid.innerHTML=data.reviews.map(renderCard).join('');requestAnimationFrame(()=>{grid.querySelectorAll('.rc.reveal').forEach(el=>el.classList.add('on'))})}
    const sc=document.getElementById('rev-score')
    if(sc&&data.rating)sc.textContent=data.rating.toFixed(1)
    const cnt=document.getElementById('rev-count')
    const total=data.total||0
    if(cnt&&total){
      const isEn=document.documentElement.lang==='en'
      cnt.textContent=isEn?`${total} reviews · Google`:`${total} отзывов · Google`
      cnt.removeAttribute('data-ru');cnt.removeAttribute('data-en')
    }
  }).catch(()=>{})
})()




!function(){
  var tours=[
    {name:'Скрытые места Тбилиси',gel:100,img:'/images/tbilisi-hidden.webp',url:'/tour/tbilisi-hidden/'},
    {name:'Казбеги за 1 день',gel:128,img:'/images/kazbegi-tour.webp',url:'/tour/kazbegi/'},
    {name:'Сигнаги и Кахетия',gel:128,img:'/images/kakheti-tour.webp',url:'/tour/kakheti/'},
    {name:'Старый Тбилиси',gel:71,img:'/images/old-tbilisi-tour.webp',url:'/tour/old-tbilisi/'},
    {name:'Тур для эмигрантов',gel:83,img:'/images/emigrant-tour.webp',url:'/tour/emigrant/'},
    {name:'Ночной Тбилиси',gel:71,img:'/images/night-tbilisi-tour.webp',url:'/tour/night-tbilisi/'},
    {name:'Тур + ужин у местных',gel:185,img:'/images/dinner-tour.webp',url:'/tour/dinner/'},
    {name:'Советский Тбилиси',gel:86,img:'/images/soviet-tour.webp',url:'/tour/soviet/'},
    {name:'Тур + фотосессия',gel:196,img:'/images/photo-tour.webp',url:'/tour/photo/'}
  ]
  var card=document.getElementById('fortuneCard')
  if(!card) return
  function go(e){
    if(e.type==='touchend') e.preventDefault()
    if(card.dataset.done) return
    card.dataset.done='1'
    var t=tours[Math.floor(Math.random()*tours.length)]
    var disc=Math.round(t.gel*0.95)
    var wa=encodeURIComponent('Хочу забронировать "'+t.name+'" со скидкой 5% (промокод СУДЬБА5)')
    card.style.cssText='width:180px;height:300px;border-radius:18px;overflow:hidden;box-shadow:0 12px 40px rgba(0,0,0,.3);background:#fff;display:flex;flex-direction:column;cursor:default'
    card.innerHTML=
      '<img src="'+t.img+'" alt="'+t.name+'" style="width:100%;height:150px;object-fit:cover;display:block">'
      +'<div style="padding:10px 12px;display:flex;flex-direction:column;align-items:center;gap:5px">'
      +'<span style="background:#EEF2FF;color:#1A56DB;font-size:9px;font-weight:700;padding:2px 8px;border-radius:9999px">−5% скидка</span>'
      +'<div style="font-size:12px;font-weight:700;color:#111;text-align:center;line-height:1.3">'+t.name+'</div>'
      +'<div style="display:flex;gap:8px;align-items:center">'
      +'<s style="font-size:11px;color:#9CA3AF">₾'+t.gel+'</s>'
      +'<b style="font-size:15px;color:#16A34A">₾'+disc+'</b>'
      +'</div>'
      +'<div style="font-size:9px;color:#9CA3AF">промокод <b style="color:#374151">СУДЬБА5</b></div>'
      +'<a href="https://wa.me/995511272623?text='+wa+'" target="_blank" rel="noopener" style="display:block;background:#1A56DB;color:#fff;font-size:11px;font-weight:700;padding:7px 18px;border-radius:9999px;text-decoration:none;margin-top:3px">Забронировать</a>'
      +'</div>'
  }
  card.addEventListener('touchend', go, {passive:false})
  card.addEventListener('click', go)
}()

function gadsWhatsApp(){
  if(typeof gtag==='function') gtag('event','conversion',{send_to:'AW-8133499399/whatsapp_click'})
}
function gadsTelegram(){
  if(typeof gtag==='function') gtag('event','conversion',{send_to:'AW-8133499399/telegram_click'})
}


;['waf','tgf'].forEach(id=>document.getElementById(id)?.classList.add('show'))