
// NAV scroll + light/dark detection
window.addEventListener('scroll',()=>{
  var nav=document.getElementById('nav'),h=document.getElementById('hero'),scrolled=window.scrollY>(h?h.offsetHeight-80:60);
  nav.classList.toggle('scrolled',scrolled);
  if(scrolled){
    var y=window.scrollY+36,dark=false;
    var secs=document.querySelectorAll('header,section,.comparison-section,.cta-block,.tours-pinned');
    for(var i=0;i<secs.length;i++){
      var s=secs[i],top=s.offsetTop,bot=top+s.offsetHeight;
      if(y>=top&&y<bot){
        var bg=getComputedStyle(s).backgroundColor;
        if(bg&&bg!=='rgba(0, 0, 0, 0)'&&bg!=='transparent'){
          var m=bg.match(/\d+/g);
          if(m){dark=(parseInt(m[0])*299+parseInt(m[1])*587+parseInt(m[2])*114)/1000<128}
        }else if(s.tagName==='HEADER'){dark=true}
        break
      }
    }
    nav.classList.toggle('nav-light',!dark);nav.classList.toggle('nav-dark',dark)
  }else{nav.classList.remove('nav-light','nav-dark')}
},{passive:true})

// ── TOUR DETAIL MODAL ──
const TOURS={
  'night-tbilisi':{
    badge:'live',img:'/images/night-tbilisi-tour.webp',
    cat:'Ноктуризм · 2.5 ч',name:'Ночной Тбилиси',gel:'₾110',usd:'$42',
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
    cat:'Премиум · 4–5 ч',name:'Тур + ужин у местных',gel:'₾250',usd:'$95',
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
    cat:'Нишевый · 3 ч',name:'Советский Тбилиси',gel:'₾155',usd:'$59',
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
    cat:'Премиум · 3 дня',name:'Slow Travel пакет',gel:'₾700',usd:'$266',
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
    cat:'Премиум · Фото · 4 ч',name:'Тур + фотосессия',gel:'₾270',usd:'$103',
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
    cat:'Выезд · 12–14 ч',name:'Казбеги за 1 день',gel:'₾205',usd:'$78',
    cat_en:'Day trip · 12–14 h',name_en:'Kazbegi in 1 day',
    desc:'Военно-Грузинская дорога, крепость Ананури, Гергетская Троица с видом на Казбек 5047м. Один из лучших однодневных маршрутов в мире. Выезд на рассвете — возвращение вечером.',
    desc_en:'Georgian Military Highway, Ananuri fortress, Gergeti Trinity with views of Mt. Kazbek 5047m. One of the world\'s best day trips. Leave at dawn — back in the evening.',
    includes:['Комфортный трансфер туда-обратно','Гид Тимур на весь маршрут','Остановки для фото','Рекомендации по ресторанам в Казбеги'],
    includes_en:['Comfortable round-trip transfer','Guide Timur throughout','Photo stops along the way','Restaurant tips in Kazbegi'],
    route:['07:00 — Выезд из Тбилиси','09:00 — Крепость Ананури: вид на водохранилище','10:30 — Гудаури: панорама Кавказского хребта','12:00 — Казбеги: обед (по выбору)','14:00 — Гергетская Троица (пешком или джип)','16:30 — Свободное время в горах','19:30 — Возвращение в Тбилиси'],
    route_en:['07:00 — Departure from Tbilisi','09:00 — Ananuri fortress &amp; reservoir views','10:30 — Gudauri: Caucasus panorama','12:00 — Kazbegi: lunch (your choice)','14:00 — Gergeti Trinity Church (hike or jeep)','16:30 — Free time in the mountains','19:30 — Return to Tbilisi'],
    wa:'Хочу+забронировать+Казбеги+за+1+день',wa_en:'I+want+to+book+Kazbegi+in+1+day'
  },
  'tbilisi-hidden':{
    badge:'live',img:'/images/tbilisi-hidden.webp',
    cat:'По городу · 5–6 ч',name:'Скрытые места Тбилиси',gel:'от ₾165',usd:'from $63',
    cat_en:'City tour · 5–6 h',name_en:'Hidden Tbilisi',
    desc:'Дворы-колодцы, серные бани, армянский квартал. Тбилиси, которого нет в путеводителе. Покажем кофейню в подворотне, галерею без вывески, хинкали не для туристов.',
    desc_en:'Hidden courtyards, sulfur baths, Armenian quarter. The Tbilisi not in any guidebook. We\'ll show you the coffee shop in the alley, the unmarked gallery, the real khinkali spot.',
    includes:['Гид Тимур 5–6 часов','Маршрут по нетуристическому Тбилиси','Кофе в местном кафе включён','Трансфер между локациями','Список мест для самостоятельного посещения'],
    includes_en:['Guide Timur for 5–6 hours','Off-the-beaten-path Tbilisi route','Coffee at a local café included','Transfer between locations','Spot list to revisit on your own'],
    route:['Сололаки: балконы, дворы, истории домов','Абанотубани: серные бани изнутри и снаружи','Армянский квартал: церкви, тишина, фрески','Улица Шарден: местный арт без вывески','Нарикала: панорама без толпы'],
    route_en:['Sololaki: balconies, courtyards, house stories','Abanotubani: sulfur baths inside &amp; out','Armenian quarter: churches, silence, frescoes','Sharden St: local art off the tourist trail','Narikala: panorama without the crowds'],
    wa:'Хочу+забронировать+Скрытые+места+Тбилиси',wa_en:'I+want+to+book+Hidden+Tbilisi+tour'
  },
  kutaisi:{
    badge:'live',img:'/images/kutaisi-tour.webp',
    cat:'Выезд · 12–13 ч',name:'Кутаиси за 1 день',gel:'₾215',usd:'$70',
    cat_en:'Day trip · 12–13 h',name_en:'Kutaisi in 1 day',
    desc:'Храм Баграти, каньон Окаце, пещера Прометея и водопад Кинчха. Один из красивейших маршрутов Грузии — архитектура, природа и горный воздух за один день.',
    desc_en:'Bagrati Cathedral, Okatse Canyon, Prometheus Cave and Kinchkha Waterfall. One of Georgia\'s most scenic routes — architecture, nature and mountain air in one day.',
    includes:['Комфортный трансфер туда-обратно','Гид Тимур на весь маршрут','Входные билеты в пещеру','Остановки для фото'],
    includes_en:['Comfortable round-trip transfer','Guide Timur throughout','Cave entrance tickets','Photo stops along the way'],
    route:['07:00 — Выезд из Тбилиси','10:30 — Храм Баграти: панорама Кутаиси','12:00 — Каньон Окаце: подвесной мост','13:30 — Обед в местном ресторане','15:00 — Пещера Прометея','17:00 — Водопад Кинчха','20:00 — Возвращение в Тбилиси'],
    route_en:['07:00 — Departure from Tbilisi','10:30 — Bagrati Cathedral: Kutaisi panorama','12:00 — Okatse Canyon: suspension bridge','13:30 — Lunch at a local restaurant','15:00 — Prometheus Cave','17:00 — Kinchkha Waterfall','20:00 — Return to Tbilisi'],
    wa:'Хочу+забронировать+Кутаиси+за+1+день',wa_en:'I+want+to+book+Kutaisi+in+1+day'
  },
  kakheti:{
    badge:'live',img:'/images/kakheti-tour.webp',
    cat:'Выезд · 10–12 ч',name:'Сигнаги и Кахетия',gel:'₾195',usd:'$74',
    cat_en:'Day trip · 10–12 h',name_en:'Signagi & Kakheti',
    desc:'Город любви Сигнаги, монастырь Бодбе, дегустация квеври-вина в семейном марани и обед у хозяйки. Самый живописный регион Грузии — виноградники, горы, золотая осень круглый год.',
    desc_en:'City of love Signagi, Bodbe monastery, qvevri wine tasting at a family winery, and lunch at a local home. Georgia\'s most scenic region — vineyards, mountains, golden landscapes.',
    includes:['Трансфер Тбилиси ↔ Кахетия','Гид Тимур на весь день','Дегустация вин в семейном марани','Домашний обед включён'],
    includes_en:['Transfer Tbilisi ↔ Kakheti','Guide Timur for the full day','Wine tasting at a family winery','Home-cooked lunch included'],
    route:['09:00 — Выезд из Тбилиси','11:00 — Монастырь Бодбе: история и виноградники','12:30 — Сигнаги: город-крепость, виды на Алазанскую долину','14:00 — Обед в семейном доме + дегустация вин','16:00 — Телави или Греми (по выбору)','19:30 — Возвращение в Тбилиси'],
    route_en:['09:00 — Departure from Tbilisi','11:00 — Bodbe monastery: history &amp; vineyards','12:30 — Signagi: fortress-town, Alazani valley views','14:00 — Lunch at a family home + wine tasting','16:00 — Telavi or Gremi (your choice)','19:30 — Return to Tbilisi'],
    wa:'Хочу+забронировать+Кахетия+тур',wa_en:'I+want+to+book+Kakheti+tour'
  },
  batumi:{
    badge:'hot',img:'/images/batumi-tour.webp',
    cat:'Выезд · 15 ч',name:'Батуми за 1 день',gel:'₾237',usd:'$85',
    cat_en:'Day trip · 15 h',name_en:'Batumi in 1 day',
    desc:'Батумский бульвар, Старый город, канатная дорога и набережная с башнями. Черноморская жемчужина Грузии — архитектура, море и закат за один насыщенный день.',
    desc_en:'Batumi Boulevard, Old Town, cable car and the seafront with towers. Georgia\'s Black Sea pearl — architecture, sea and sunset in one packed day.',
    includes:['Комфортный трансфер туда-обратно','Гид Тимур на весь маршрут','Остановки для фото','Свободное время на набережной'],
    includes_en:['Comfortable round-trip transfer','Guide Timur throughout','Photo stops along the way','Free time on the promenade'],
    route:['06:00 — Выезд из Тбилиси','11:00 — Старый Батуми: мечеть, церковь, площадь Пьяцца','12:30 — Батумский бульвар и набережная','13:30 — Обед с видом на море','15:00 — Канатная дорога: панорама города','16:30 — Свободное время','21:00 — Возвращение в Тбилиси'],
    route_en:['06:00 — Departure from Tbilisi','11:00 — Old Batumi: mosque, church, Piazza Square','12:30 — Batumi Boulevard &amp; promenade','13:30 — Lunch with sea view','15:00 — Cable car: city panorama','16:30 — Free time','21:00 — Return to Tbilisi'],
    wa:'Хочу+забронировать+Батуми+за+1+день',wa_en:'I+want+to+book+Batumi+in+1+day'
  },
  'digital-nomad':{
    badge:'live',img:'/images/digital-nomad-tbilisi.jpg',
    cat:'Digital Nomad · 3 ч',name:'Digital Nomad Welcome Tour',gel:'₾145',usd:'$55',
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
const hv=document.getElementById('hero-vid')
if(hv){
  const playBtn=document.getElementById('hero-play-btn')
  const tap=document.getElementById('hero-tap')
  const hvHide=()=>{if(tap)tap.style.display='none'}
  const hvPlay=()=>hv.play().then(hvHide).catch(()=>{})
  hv.addEventListener('playing',hvHide,{once:true})
  hv.addEventListener('canplay',hvPlay,{once:true})
  hvPlay()
  setTimeout(hvPlay,500)
  if(tap){
    tap.addEventListener('touchstart',function(){hvPlay();hvHide()},{once:true,passive:true})
    tap.addEventListener('click',function(){hvPlay();hvHide()},{once:true})
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

// Scroll reveal (all directions)
const ro=new IntersectionObserver(e=>{
  e.forEach(x=>{if(x.isIntersecting)x.target.classList.add('on')})
},{threshold:.05,rootMargin:'0px 0px 60px 0px'})
document.querySelectorAll('.reveal,.reveal-left,.reveal-right,.reveal-scale').forEach(el=>ro.observe(el))
setTimeout(()=>document.querySelectorAll('.reveal:not(.on),.reveal-left:not(.on),.reveal-right:not(.on),.reveal-scale:not(.on)').forEach(el=>el.classList.add('on')),800)

// Progress bar
;(function(){
  const bar=document.getElementById('scroll-progress')
  if(!bar)return
  let ticking=false
  window.addEventListener('scroll',function(){
    if(!ticking){requestAnimationFrame(function(){
      const h=document.documentElement.scrollHeight-window.innerHeight
      bar.style.width=(h>0?(window.scrollY/h)*100:0)+'%'
      ticking=false
    });ticking=true}
  },{passive:true})
})()

// Parallax hero
;(function(){
  const bg=document.getElementById('hero-bg')
  if(!bg||window.innerWidth<768)return
  let ticking=false
  window.addEventListener('scroll',function(){
    if(!ticking){requestAnimationFrame(function(){
      const y=window.scrollY
      if(y<900)bg.style.transform='translate3d(0,'+y*.35+'px,0)'
      ticking=false
    });ticking=true}
  },{passive:true})
})()

// Image zoom on scroll — handled by CSS hover in new overlay cards

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
const burger=document.getElementById('burger'),drawer=document.getElementById('drawer'),cbar=document.getElementById('cookie-bar')
burger.addEventListener('click',()=>{
  const o=drawer.classList.toggle('on')
  burger.classList.toggle('on',o)
  document.body.style.overflow=o?'hidden':''
  if(o&&cbar)cbar.style.display='none'
  else if(cbar&&!localStorage.getItem('cookies_v4'))cbar.style.display=''
})
function closeDrawer(){drawer.classList.remove('on');burger.classList.remove('on');document.body.style.overflow='';if(cbar&&!localStorage.getItem('cookies_v4'))cbar.style.display=''}

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
  var GEL_RUB=28
  var GEL_EUR=0.32
  var curr=lang==='en'?'usd':(localStorage.getItem('curr_v1')||(lang==='ru'?'rub':'gel'))
  if(lang==='en') localStorage.setItem('curr_v1','usd')
  document.querySelectorAll('.price-main[data-gel]').forEach(function(el){
    var gel=+(el.dataset.gel||'0').replace(/[^\d]/g,'')
    var usdNum=+(el.dataset.usd||'0').replace(/[^\d]/g,'')
    if(curr==='gel') el.textContent=el.dataset.gel
    else if(curr==='usd') el.textContent='$'+usdNum
    else if(curr==='eur') el.textContent='€'+Math.round(gel*GEL_EUR)
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
  if(dRu){dRu.style.background=lang==='ru'?'#1A3D2E':'#fff';dRu.style.color=lang==='ru'?'#fff':'#1A3D2E'}
  if(dEn){dEn.style.background=lang==='en'?'#1A3D2E':'#fff';dEn.style.color=lang==='en'?'#fff':'#1A3D2E'}
  document.documentElement.lang=lang==='en'?'en':'ru'
  localStorage.setItem('lang',lang)
}
// Keyboard: Alt+L toggles RU/EN
document.addEventListener('keydown',function(e){
  if(e.altKey&&e.key==='l'||e.altKey&&e.key==='L'||e.altKey&&e.key==='д'||e.altKey&&e.key==='Д'){
    setLang(document.documentElement.lang==='en'?'ru':'en')
  }
})
// Restore saved language — redirect if on wrong version
var savedLang=localStorage.getItem('lang')
if(savedLang==='en'&&location.pathname.indexOf('/en/')!==0){location.replace('/en'+location.pathname)}
else if(savedLang&&savedLang!=='ru') setLang(savedLang)

// ── COOKIE ──
function acceptCookies(){
  localStorage.setItem('cookies_v4','1');
  gtag('consent','update',{analytics_storage:'granted',ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted'});
  document.getElementById('cookie-bar').classList.remove('show')
}
function declineCookies(){
  localStorage.setItem('cookies_v4','0');
  gtag('consent','update',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});
  document.getElementById('cookie-bar').classList.remove('show')
}
if(!localStorage.getItem('cookies_v4'))setTimeout(()=>{document.getElementById('cookie-bar').classList.add('show')},1500)

// ── CONTACT MODAL ──

function openContact(){
  if(typeof closeQuiz==='function')closeQuiz();if(typeof closePayment==='function')closePayment()
  document.getElementById('contact-modal').classList.add('open');document.body.style.overflow='hidden'
  const f=document.getElementById('cm-form'),s=document.getElementById('cm-success')
  if(f)f.style.display='';if(s)s.style.display='none'
}
function closeContact(){document.getElementById('contact-modal').classList.remove('open');document.body.style.overflow=''}
function sendContact(){
  const name=document.getElementById('cm-name').value.trim()
  const phone=document.getElementById('cm-phone').value.trim()
  const msg=document.getElementById('cm-msg').value.trim()
  const btn=document.querySelector('.cm-submit')
  if(!phone){document.getElementById('cm-phone').focus();return}
  if(btn){btn.disabled=true;btn.textContent=document.documentElement.lang==='en'?'Sending...':'Отправка...'}
  // Save to Airtable CRM + Telegram via API
  fetch('/api/booking/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:name||'(сайт)',phone,tour:'Связаться',note:msg||'Форма связи с сайта'})}).then(function(r){return r.json()}).then(function(){
    document.getElementById('cm-form').style.display='none'
    document.getElementById('cm-success').style.display='block'
    setTimeout(closeContact,3000)
  }).catch(function(){
    document.getElementById('cm-form').style.display='none'
    document.getElementById('cm-success').style.display='block'
    setTimeout(closeContact,3000)
  })
  // Save to Formspree (email)
  if(typeof FORMSPREE_ID!=='undefined'&&FORMSPREE_ID){
    try{fetch('https://formspree.io/f/'+FORMSPREE_ID,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify({type:'contact',name,phone,message:msg})})}catch(e){}
  }
  // GA4
  if(typeof gtag==='function'){
    gtag('event','generate_lead',{event_category:'contact',event_label:'hero_contact',value:5,currency:'USD'})
  }
}

// ── BOOKING MODAL ──
// === Config: add booked dates as 'YYYY-MM-DD' strings ===
const BOOKING_BUSY=[]  // e.g. ['2026-04-10','2026-04-15']
// Spots per date: {tourId: {'YYYY-MM-DD': spotsLeft}}. 0 = sold out, omitted = default (7)
const BOOKING_SPOTS_DEFAULT=7
let BOOKING_SPOTS={}
let _spotsLoaded=false
function loadSpots(){
  if(_spotsLoaded)return
  _spotsLoaded=true
  fetch('/api/spots').then(r=>r.json()).then(d=>{
    if(d&&!d.error){BOOKING_SPOTS=d;if(document.querySelector('#booking-modal.open'))bmRenderCal()}
  }).catch(()=>{})
}
const FORMSPREE_ID='mzdkyywe'

const BK_TOURS=[
  {id:'kazbegi',      icon:'🏔️',name:'Казбеги за 1 день',         name_en:'Kazbegi in 1 day',           price:'₾205 / чел.', price_en:'$78 / person',  price_usd:78,  price_rub:7200},
  {id:'tbilisi-hidden',icon:'🏙️',name:'Скрытые места Тбилиси',  name_en:'Hidden Tbilisi',              price:'от ₾165 / чел.',price_en:'from $63 / person',price_usd:63,price_rub:5800},
  {id:'kutaisi',      icon:'🏛️',name:'Кутаиси за 1 день',        name_en:'Kutaisi in 1 day',            price:'₾215 / чел.',  price_en:'$70 / person',  price_usd:70,  price_rub:7500},
  {id:'kakheti',      icon:'🍷',name:'Кахетия — вино и природа', name_en:'Kakheti — wine & nature',     price:'₾195 / чел.', price_en:'$74 / person',  price_usd:74,  price_rub:6900},
  {id:'batumi',       icon:'🌊',name:'Батуми за 1 день',          name_en:'Batumi in 1 day',             price:'₾237 / чел.',  price_en:'$85 / person',  price_usd:85,  price_rub:8300},
  {id:'night-tbilisi',icon:'🌙',name:'Ночной Тбилиси',          name_en:'Night Tbilisi',                price:'₾110 / чел.',  price_en:'$42 / person',  price_usd:42,  price_rub:3900},
  {id:'dinner',       icon:'🍽️',name:'Тур + ужин у местных',    name_en:'Tour + dinner with locals',   price:'₾250 / чел.', price_en:'$95 / person',  price_usd:95,  price_rub:8800},
  {id:'soviet',       icon:'🎭',name:'Советский Тбилиси',        name_en:'Soviet Tbilisi',              price:'₾155 / чел.',  price_en:'$59 / person',  price_usd:59,  price_rub:5500},
  {id:'slow-travel',  icon:'✈️',name:'Slow Travel 3 дня',       name_en:'Slow Travel 3 days',          price:'₾700 / чел.', price_en:'$266 / person', price_usd:266, price_rub:24900},
  {id:'photo',        icon:'📸',name:'Тур + фотосессия',         name_en:'Tour + photo session',        price:'₾270 / чел.', price_en:'$103 / person',  price_usd:103,  price_rub:9500},
  {id:'digital-nomad',icon:'💻',name:'Digital Nomad Tour',      name_en:'Digital Nomad Tour',           price:'₾145 / чел.',  price_en:'$55 / person',  price_usd:55,  price_rub:5100},
  {id:'mtskheta',     icon:'⛪',name:'Мцхета — древняя столица',name_en:'Mtskheta — Ancient Capital',  price:'₾90 / чел.',  price_en:'$34 / person',  price_usd:34,  price_rub:3200},
  {id:'other',        icon:'💬',name:'Другой маршрут / обсудить',name_en:'Custom route / discuss',      price:'',            price_en:'',               price_usd:0,   price_rub:0}
]
const BK_TOP5=['kazbegi','kakheti','tbilisi-hidden','kutaisi','night-tbilisi']
const bkSt={tour:'',tourName:'',date:'',calY:0,calM:0}

function openBooking(tourId){
  loadSpots()
  const isEn=document.documentElement.lang==='en'
  const modal=document.getElementById('booking-modal')
  modal.classList.add('open')
  document.body.style.overflow='hidden'
  const now=new Date()
  bkSt.calY=now.getFullYear();bkSt.calM=now.getMonth()
  bkSt.date='';bkSt.tour=tourId||'';bkSt.tourName=''
  // render tour list — all tours
  const list=document.getElementById('bm-tour-list')
  list.innerHTML=''
  BK_TOURS.forEach(t=>{
    const div=document.createElement('div')
    div.className='bm-tour'+(bkSt.tour===t.id?' sel':'')
    div.dataset.tid=t.id
    div.onclick=()=>bmPickTour(t.id,isEn?t.name_en:t.name)
    div.innerHTML='<span class="bm-tour-icon">'+t.icon+'</span><div class="bm-tour-name">'+(isEn?t.name_en:t.name)+'</div>'+(t.price?'<div class="bm-tour-price">'+(isEn?t.price_en:(t.price_rub?'₽'+t.price_rub.toLocaleString('ru-RU'):t.price))+'</div>':'')
    list.appendChild(div)
  })
  const n1=document.getElementById('bm-next1')
  if(tourId){
    const t=BK_TOURS.find(x=>x.id===tourId)
    if(t){bkSt.tourName=isEn?t.name_en:t.name;list.querySelectorAll('.bm-tour').forEach(el=>{el.classList.toggle('sel',el.dataset.tid===tourId)})}
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
  const step=document.querySelector('.bm-step[data-bstep="'+n+'"]')
  step.classList.add('active')
  document.getElementById('bm-bar').style.width=(n/4*100)+'%'
  // reset scroll to top of step
  step.scrollTop=0
  document.querySelector('.bm-box').scrollTop=0
  // blur any focused input to dismiss keyboard
  if(document.activeElement)document.activeElement.blur()
  if(n===2)bmRenderCal()
}
function bmStep(n){bmShowStep(n)}
function bmPickTour(id,name){
  bkSt.tour=id;bkSt.tourName=name
  document.querySelectorAll('.bm-tour').forEach(el=>{
    const tid=el.dataset.tid
    el.classList.toggle('sel',tid===id)
  })
  document.getElementById('bm-next1').disabled=false
}
function bmScroll(dir){
  const list=document.getElementById('bm-tour-list')
  list.scrollBy({left:dir*130,behavior:'smooth'})
}
function bmCalNav(dir){
  bkSt.calM+=dir
  if(bkSt.calM>11){bkSt.calM=0;bkSt.calY++}
  if(bkSt.calM<0){bkSt.calM=11;bkSt.calY--}
  bmRenderCal()
}
function bmGetSpots(tourId,ds){
  const tourSpots=BOOKING_SPOTS[tourId]
  if(!tourSpots)return BOOKING_SPOTS_DEFAULT
  return tourSpots[ds]!==undefined?tourSpots[ds]:BOOKING_SPOTS_DEFAULT
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
    const spots=bmGetSpots(bkSt.tour,ds)
    const d=document.createElement('div')
    if(date<today){d.className='bcal-day past';d.textContent=day}
    else if(BOOKING_BUSY.includes(ds)||spots===0){d.className='bcal-day busy';d.innerHTML=day+'<span class="bcal-spots sold">—</span>';d.title=isEn?'Sold out':'Мест нет'}
    else{
      d.className='bcal-day avail'+(bkSt.date===ds?' selected':'')
      const spotsClass=spots<=2?'few':spots<=4?'some':''
      d.innerHTML=day+'<span class="bcal-spots '+spotsClass+'">'+spots+'</span>'
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
  // Сохраняем в Airtable CRM
  try{fetch('/api/booking/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,phone,email,tour:bkSt.tourName,tourDate:bkSt.date,guests:parseInt(guests)||1,note})})}catch(e){}
  // Дублируем в Formspree (email Тимуру)
  if(FORMSPREE_ID){
    try{fetch('https://formspree.io/f/'+FORMSPREE_ID,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify({tour:bkSt.tourName,date:dateFmt,guests,name,email,phone,note})})}catch(e){}
  }
  // Conversion tracking
  if(typeof gtag==='function'){
    gtag('event','generate_lead',{event_category:'booking',event_label:bkSt.tourName,value:5,currency:'USD'})
    gtag('event','form_submit',{event_category:'booking',event_label:bkSt.tourName,value:1})
  }
  if(typeof posthog!=='undefined'){posthog.capture('form_submit',{tour:bkSt.tourName,page:location.pathname})}
  document.getElementById('bm-success-meta').textContent=bkSt.tourName+' · '+dateFmt+' · '+guests+(isEn?' pax':' чел.')
  bmShowStep(4)
}

// ── QUIZ ──
const qAns={}
function openQuiz(){if(typeof closePayment==='function')closePayment();if(typeof closeContact==='function')closeContact();Object.keys(qAns).forEach(k=>delete qAns[k]);document.querySelectorAll('.qm-opt.sel').forEach(o=>o.classList.remove('sel'));document.getElementById('quiz-modal').classList.add('open');document.body.style.overflow='hidden';showStep(1)}
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
  if(a2==='mountains'){icon='🏔️';title=isEn?'Kazbegi in 1 day':'Казбеги за 1 день';sub=isEn?'Mountains, Gergeti church, Military Highway. From ₾175/person.':'Горы, Гергетская Троица, ВГД. От ₾175 с человека.';waText=isEn?'I want to book Kazbegi tour':'Хочу тур Казбеги'}
  else if(a2==='wine'){icon='🍷';title=isEn?'Kakheti — wine & gastronomy':'Кахетия — вино и гастрономия';sub=isEn?'Monasteries, vineyards, tastings. From ₾170/person.':'Монастыри, виноградники, дегустации. От ₾170 с человека.';waText=isEn?'I want to book Kakheti tour':'Хочу тур Кахетия'}
  else if(a2==='city'){icon='🏙️';title=isEn?'Hidden Tbilisi':'Скрытые места Тбилиси';sub=isEn?'Courtyards, sulfur baths, local cafes. From ₾135/person.':'Дворики, серные бани, кафе без вывески. От ₾135 с человека.';waText=isEn?'I want to book Hidden Tbilisi tour':'Хочу тур Скрытые места Тбилиси'}
  else{icon='🌊';title=isEn?'Batumi in 1 day':'Батуми за 1 день';sub=isEn?'Black Sea coast, Old Town, botanical garden. From ₾201/person.':'Черноморское побережье, Старый город, ботсад. От ₾201 с человека.';waText=isEn?'I want to book Batumi tour':'Хочу тур Батуми'}
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
  // Set quiz CTA: open contact form with pre-filled message
  var qmLink=document.getElementById('qm-wa-link')
  qmLink.href='#'
  qmLink.onclick=function(e){e.preventDefault();closeQuiz();if(typeof openContact==='function'){openContact();var msgEl=document.getElementById('cm-msg');if(msgEl)msgEl.value=waFull}}
  document.getElementById('qm-bar').style.width='100%'
  showStep(5)
}
function restartQuiz(){Object.keys(qAns).forEach(k=>delete qAns[k]);showStep(1)}

// ── TOUR FILTER ──
function filterTours(tab,cat){
  document.querySelectorAll('.ftab').forEach(t=>t.classList.remove('on'))
  tab.classList.add('on')
  document.querySelectorAll('#allGrid [data-cat]').forEach(c=>{
    c.classList.toggle('hidden',cat!=='все'&&c.dataset.cat!==cat)
  })
  document.getElementById('allGrid').scrollLeft=0
}
function scrollTours(dir){
  var g=document.getElementById('allGrid')
  var card=g.querySelector('.tc:not(.hidden)')
  if(!card)return
  var gap=parseInt(getComputedStyle(g).gap)||24
  g.scrollBy({left:dir*(card.offsetWidth+gap),behavior:'smooth'})
}

// ── TOURS SWIPE — нативный CSS scroll-snap обрабатывает touch, JS не нужен ──

// ── TRIPADVISOR RATING на карточках туров ──
;(function(){
  var ratingHtml='<div class="tc-rating"><span class="tc-rating-stars">★★★★★</span><span class="tc-rating-text">4.9 <span>TripAdvisor</span></span></div>';
  document.querySelectorAll('#allGrid .tc-name').forEach(function(el){
    // Только если ещё не добавлено (для первой карточки — уже в HTML)
    if(!el.nextElementSibling||!el.nextElementSibling.classList.contains('tc-rating')){
      el.insertAdjacentHTML('afterend',ratingHtml);
    }
  });
})();

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
  // Duck background music when Timur speaks
  if(_bgAudio){
    if(!v.muted){
      _bgAudio.volume=0.05
    } else {
      _bgAudio.volume=0.25
    }
  }
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
  const GEL_EUR=0.32
  const sw=document.getElementById('cs-main')
  if(!sw)return
  function updateAll(curr){
    document.querySelectorAll('.price-main[data-gel]').forEach(function(el){
      var gel=+(el.dataset.gel||'0').replace(/[^\d]/g,'')
      var usd=el.dataset.usd||(''+(Math.round(gel*0.37)))
      var usdNum=+(usd).replace(/[^\d]/g,'')
      if(curr==='gel')el.textContent=el.dataset.gel
      else if(curr==='usd')el.textContent='$'+usdNum
      else if(curr==='eur')el.textContent='€'+Math.round(gel*GEL_EUR)
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
    const colors=['#1A3D2E','#7C3AED','#059669','#DC2626','#D97706','#0891B2']
    const av=r.avatar
      ?`<img src="${r.avatar}" alt="${r.name}" width="40" height="40" style="width:40px;height:40px;border-radius:50%;object-fit:cover;flex-shrink:0;display:block">`
      :`<div class="rc-av" style="background:${colors[i%colors.length]}">${r.name.charAt(0).toUpperCase()}</div>`
    const delay=i>0?` style="transition-delay:${i*.1}s"`:''
    return`<div class="rc reveal"${delay}><div class="rc-source">${GOOGLE_SVG} Google</div><div class="rc-top">${av}<div><div class="rc-name">${r.name}</div><div class="rc-meta">${r.time}</div></div></div><div class="rc-stars" style="color:#F59E0B;font-size:12px;letter-spacing:1px;margin-bottom:10px">${stars(r.rating)}</div><p class="rc-text">${r.text}</p></div>`
  }
  fetch('/api/reviews').then(r=>r.ok?r.json():null).then(data=>{
    if(!data||data.error||!data.reviews||!data.reviews.length)return
    const grid=document.getElementById('rev-grid')
    if(grid){grid.innerHTML=data.reviews.slice(0,3).map(renderCard).join('');requestAnimationFrame(()=>{grid.querySelectorAll('.rc.reveal').forEach(el=>el.classList.add('on'))})}
    const sc=document.getElementById('rev-score')
    if(sc&&data.rating)sc.textContent=data.rating.toFixed(1)
  }).catch(()=>{})
})()




!function(){
  var tours=[
    {name:'Скрытые места Тбилиси',gel:100,img:'/images/tbilisi-hidden.webp',url:'/tour/tbilisi-hidden/'},
    {name:'Казбеги за 1 день',gel:128,img:'/images/kazbegi-tour.webp',url:'/tour/kazbegi/'},
    {name:'Сигнаги и Кахетия',gel:128,img:'/images/kakheti-tour.webp',url:'/tour/kakheti/'},
    {name:'Кутаиси за 1 день',gel:215,img:'/images/kutaisi-tour.webp',url:'/tour/kutaisi/'},
    {name:'Батуми за 1 день',gel:237,img:'/images/batumi-tour.webp',url:'/tour/batumi/'},
    {name:'Ночной Тбилиси',gel:71,img:'/images/night-tbilisi-tour.webp',url:'/tour/night-tbilisi/'},
    {name:'Тур + ужин у местных',gel:185,img:'/images/dinner-tour.webp',url:'/tour/dinner/'},
    {name:'Советский Тбилиси',gel:86,img:'/images/soviet-tour.webp',url:'/tour/soviet/'},
    {name:'Тур + фотосессия',gel:196,img:'/images/photo-tour.webp',url:'/tour/photo/'}
  ]
}()

// ── FORTUNE CARD ──
!function(){
  var tours=[
    {name:'Скрытые места Тбилиси',gel:100,rub:3500,img:'/images/tbilisi-hidden.webp',url:'/tour/tbilisi-hidden/'},
    {name:'Казбеги за 1 день',gel:128,rub:4500,img:'/images/kazbegi-tour.webp',url:'/tour/kazbegi/'},
    {name:'Сигнаги и Кахетия',gel:128,rub:4500,img:'/images/kakheti-tour.webp',url:'/tour/kakheti/'},
    {name:'Кутаиси за 1 день',gel:215,rub:7500,img:'/images/kutaisi-tour.webp',url:'/tour/kutaisi/'},
    {name:'Батуми за 1 день',gel:237,rub:8300,img:'/images/batumi-tour.webp',url:'/tour/batumi/'},
    {name:'Ночной Тбилиси',gel:71,rub:2500,img:'/images/night-tbilisi-tour.webp',url:'/tour/night-tbilisi/'},
    {name:'Тур + ужин у местных',gel:185,rub:6500,img:'/images/dinner-tour.webp',url:'/tour/dinner/'},
    {name:'Советский Тбилиси',gel:86,rub:2900,img:'/images/soviet-tour.webp',url:'/tour/soviet/'},
    {name:'Тур + фотосессия',gel:196,rub:6900,img:'/images/photo-tour.webp',url:'/tour/photo/'}
  ]
  var card=document.getElementById('fortuneCard')
  if(!card) return
  var front=document.getElementById('tcard-front-inner')
  function go(e){
    if(e.type==='touchend') e.preventDefault()
    if(card.dataset.done) return
    card.dataset.done='1'
    var t=tours[Math.floor(Math.random()*tours.length)]
    var isEn=document.documentElement.lang==='en'
    var discGel=Math.round(t.gel*0.95)
    var discRub=Math.round(t.rub*0.95)
    var priceOld=isEn?'$'+Math.round(t.gel*0.37):'₽'+Math.round(t.gel*28).toLocaleString('ru-RU')
    var priceNew=isEn?'$'+Math.round(discGel*0.37):'₽'+Math.round(discGel*28).toLocaleString('ru-RU')
    var wa=encodeURIComponent((isEn?'I want to book "'+t.name+'" with 5% off (promo LUCKY5)':'Хочу забронировать "'+t.name+'" со скидкой 5% (промокод СУДЬБА5)'))
    front.innerHTML=
      '<img src="'+t.img+'" alt="'+t.name+'" style="width:100%;height:130px;object-fit:cover;display:block">'
      +'<div style="padding:8px 10px;display:flex;flex-direction:column;align-items:center;gap:4px;flex:1;justify-content:center">'
      +'<span style="background:#EEF2FF;color:#1A3D2E;font-size:9px;font-weight:700;padding:2px 8px;border-radius:9999px">−5%</span>'
      +'<div style="font-size:11px;font-weight:700;color:#111;text-align:center;line-height:1.3">'+t.name+'</div>'
      +'<div style="display:flex;gap:6px;align-items:center">'
      +'<s style="font-size:10px;color:#9CA3AF">'+priceOld+'</s>'
      +'<b style="font-size:14px;color:#16A34A">'+priceNew+'</b>'
      +'</div>'
      +'<div style="font-size:8px;color:#9CA3AF">промокод <b style="color:#374151">СУДЬБА5</b></div>'
      +'<a href="https://wa.me/995511272623?text='+wa+'" target="_blank" rel="noopener" style="display:block;background:#1A3D2E;color:#fff;font-size:10px;font-weight:700;padding:6px 16px;border-radius:9999px;text-decoration:none;margin-top:2px">'+(isEn?'Book now':'Забронировать')+'</a>'
      +'</div>'
    card.classList.add('flipped')
  }
  card.addEventListener('touchend',go,{passive:false})
  card.addEventListener('click',go)
}()

// ── FAVORITES ──
function toggleFav(id,btn){
  var favs=JSON.parse(localStorage.getItem('fav_tours')||'[]')
  var idx=favs.indexOf(id)
  if(idx===-1){favs.push(id)}else{favs.splice(idx,1)}
  localStorage.setItem('fav_tours',JSON.stringify(favs))
  btn.textContent=idx===-1?'❤️':'🤍'
}
;(function initFavs(){
  var favs=JSON.parse(localStorage.getItem('fav_tours')||'[]')
  if(!favs.length) return
  document.querySelectorAll('.tc-fav').forEach(function(btn){
    var id=btn.getAttribute('onclick').match(/'([^']+)'/)?.[1]
    if(id&&favs.includes(id)) btn.textContent='❤️'
  })
})()

function gadsWhatsApp(){
  if(typeof gtag==='function'){
    gtag('event','generate_lead',{event_category:'contact',event_label:'whatsapp_click'})
  }
}
function gadsTelegram(){
  if(typeof gtag==='function'){
    gtag('event','generate_lead',{event_category:'contact',event_label:'telegram_click'})
  }
}


;(function(){var f=document.getElementById('fab-main');if(f)f.classList.add('show')})()


// ── PARALLAX HERO ──
;(function(){
  var bg=document.getElementById('hero-bg')
  if(!bg||window.matchMedia('(prefers-reduced-motion:reduce)').matches) return
  var ticking=false
  window.addEventListener('scroll',function(){
    if(!ticking){
      ticking=true
      requestAnimationFrame(function(){
        var y=window.scrollY
        if(y<window.innerHeight) bg.style.transform='translate3d(0,'+y*0.35+'px,0)'
        ticking=false
      })
    }
  },{passive:true})
})()

// ── BACKGROUND MUSIC (persists across pages via sessionStorage) ──
var _bgAudio=document.getElementById('bg-music')
var _musicToggle=document.getElementById('music-toggle')
var _musicPlaying=false

;(function(){
  if(!_bgAudio) return
  // Restore position from previous page
  var savedTime=parseFloat(sessionStorage.getItem('music_time')||'0')
  var wasMuted=sessionStorage.getItem('music_muted')==='1'
  if(wasMuted){
    _musicToggle.textContent='🔇'
    return
  }
  function startMusic(){
    _bgAudio.volume=0.25
    if(savedTime>0) _bgAudio.currentTime=savedTime
    _bgAudio.play().then(function(){
      _musicPlaying=true
      _musicToggle.textContent='🔊'
    }).catch(function(){})
  }
  // Save position before leaving page
  window.addEventListener('beforeunload',function(){
    if(_bgAudio&&_musicPlaying){
      sessionStorage.setItem('music_time',String(_bgAudio.currentTime))
    }
  })
  // Try autoplay immediately
  _bgAudio.volume=0.25
  if(savedTime>0) _bgAudio.currentTime=savedTime
  var p=_bgAudio.play()
  if(p!==undefined){
    p.then(function(){
      _musicPlaying=true
      _musicToggle.textContent='🔊'
    }).catch(function(){
      // Autoplay blocked — start on first user gesture
      var started=false
      var events=['touchstart','touchend','click','pointerdown','keydown','scroll']
      function onInteract(){
        if(started) return
        started=true
        _bgAudio.volume=0.25
        _bgAudio.load()
        if(savedTime>0) _bgAudio.currentTime=savedTime
        var pp=_bgAudio.play()
        if(pp) pp.then(function(){
          _musicPlaying=true
          _musicToggle.textContent='🔊'
        }).catch(function(){started=false})
      }
      function cleanup(){
        events.forEach(function(e){
          document.removeEventListener(e,onInteract)
          window.removeEventListener(e,onInteract)
        })
      }
      // Re-check periodically if music started
      var checkId=setInterval(function(){
        if(_musicPlaying){cleanup();clearInterval(checkId)}
      },500)
      events.forEach(function(e){
        if(e==='scroll'){
          window.addEventListener(e,onInteract,{passive:true})
        } else {
          document.addEventListener(e,onInteract,{passive:true})
        }
      })
    })
  }
})()
function toggleMusic(){
  if(!_bgAudio) return
  if(_musicPlaying){
    _bgAudio.pause()
    _musicPlaying=false
    _musicToggle.textContent='🔇'
    sessionStorage.setItem('music_muted','1')
    sessionStorage.removeItem('music_time')
  } else {
    _bgAudio.play().catch(function(){})
    _musicPlaying=true
    _musicToggle.textContent='🔊'
    sessionStorage.removeItem('music_muted')
  }
}

// ── POSTHOG CTA TRACKING (funnel: pageview → cta_click → contact) ──

;(function(){
  document.addEventListener('click',function(e){
    if(typeof posthog==='undefined') return
    var wa=e.target.closest('a[href*="wa.me"]')
    var tg=e.target.closest('a[href*="t.me"]')
    var tel=e.target.closest('a[href*="tel:"]')
    var book=e.target.closest('.btn-book,#fab-main,[data-action="book"]')
    if(wa){
      posthog.capture('cta_click',{channel:'whatsapp',page:location.pathname})
      posthog.capture('whatsapp_click')
      if(typeof gtag==='function'){gtag('event','generate_lead',{event_category:'booking',event_label:'whatsapp',value:1});gtag('event','whatsapp_click',{event_category:'contact',event_label:'whatsapp'})}
    }
    else if(tg){
      posthog.capture('cta_click',{channel:'telegram',page:location.pathname})
      if(typeof gtag==='function'){gtag('event','generate_lead',{event_category:'booking',event_label:'telegram',value:1})}
    }
    else if(tel){
      posthog.capture('cta_click',{channel:'phone',page:location.pathname})
      if(typeof gtag==='function'){gtag('event','generate_lead',{event_category:'booking',event_label:'phone',value:1})}
    }
    else if(book){
      posthog.capture('cta_click',{channel:'book_button',page:location.pathname})
      if(typeof gtag==='function'){gtag('event','generate_lead',{event_category:'booking',event_label:document.title||'unknown',value:1})}
    }
  })
})()

// ── CLICK FRAUD PROTECTION ──

;(function(){
  var KEY='_cf_clicks'
  var BLOCK_KEY='_cf_blocked'
  var MAX_CLICKS=4
  var WINDOW_SEC=60
  var BLOCK_MIN=30

  // Check if already blocked
  var blockedUntil=parseInt(sessionStorage.getItem(BLOCK_KEY)||'0')
  if(blockedUntil>Date.now()){
    markSuspect()
    return
  }

  function getClicks(){
    try{return JSON.parse(sessionStorage.getItem(KEY)||'[]')}catch(e){return[]}
  }

  function markSuspect(){
    // Send fraud event to GA4
    if(typeof gtag==='function'){
      gtag('event','fraud_suspect',{
        event_category:'security',
        event_label:location.pathname,
        non_interaction:true
      })
    }
    // Send fraud event to PostHog
    if(typeof posthog!=='undefined'){
      posthog.capture('fraud_suspect',{
        page:location.pathname,
        referrer:document.referrer
      })
    }
    // Hide WhatsApp/Telegram CTA buttons to prevent fake conversions
    document.querySelectorAll('a[href*="wa.me"],a[href*="t.me"]').forEach(function(a){
      a.style.pointerEvents='none'
      a.style.opacity='0.3'
    })
  }

  // Monitor clicks on ad-landing conversion elements
  document.addEventListener('click',function(e){
    var link=e.target.closest('a[href*="wa.me"],a[href*="t.me"],a[href*="tel:"],.btn-tg,.btn-wa')
    if(!link) return

    var now=Date.now()
    var clicks=getClicks()
    clicks.push(now)
    // Keep only clicks within window
    clicks=clicks.filter(function(t){return now-t<WINDOW_SEC*1000})
    sessionStorage.setItem(KEY,JSON.stringify(clicks))

    if(clicks.length>=MAX_CLICKS){
      // Block for BLOCK_MIN minutes
      sessionStorage.setItem(BLOCK_KEY,String(now+BLOCK_MIN*60*1000))
      markSuspect()
      e.preventDefault()
    }
  },true)
})()