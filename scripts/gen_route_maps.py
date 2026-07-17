#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генератор интерактивных Google Maps JS карт маршрута для туров /ekskursiya/.
Читает route-name из route-grid, маппит на реальные гео-точки (ручной справочник),
вставляет карту после секции «Программа по часам». Только Google Maps (Leaflet запрещён).
DRY-RUN: python3 scripts/gen_route_maps.py            -> отчёт по каждому туру
WRITE:   python3 scripts/gen_route_maps.py --write    -> вставка в файлы
"""
import re, glob, sys, json

MAPS_KEY = "AIzaSyB8lmxnn0XEUQKhPIJZsDw8MRuKURD2RXQ"  # gen-lang-client, referrer sakhva-travel.com

# --- Справочник координат (lat,lng), ручная курация ---
C = {
 'tbilisi': (41.6938, 44.8015),
 'mtskheta': (41.8458, 44.7203), 'jvari_mon': (41.8386, 44.7328),
 'svetitskhoveli': (41.8425, 44.7222), 'samtavro': (41.8470, 44.7196),
 'gori': (41.9847, 44.1086), 'stalin_museum': (41.9835, 44.1120), 'uplistsikhe': (41.9660, 44.2075),
 'ananuri': (42.1642, 44.7069), 'zhinvali': (42.1360, 44.7430), 'pasanauri': (42.3520, 44.6870),
 'gudauri': (42.4780, 44.4802), 'friendship_arch': (42.4906, 44.4530), 'cross_pass': (42.5045, 44.4534),
 'stepantsminda': (42.6577, 44.6415), 'gergeti': (42.6626, 44.6205), 'truso': (42.6050, 44.4800),
 'telavi': (41.9197, 45.4731), 'alaverdi': (42.0330, 45.3770), 'ikalto': (41.9330, 45.3760),
 'tsinandali': (41.8940, 45.5730), 'kvareli': (41.9520, 45.8150),
 'sighnaghi': (41.6197, 45.9214), 'bodbe': (41.6030, 45.9260), 'gombori': (41.8300, 45.1900),
 'sagarejo': (41.7340, 45.3320), 'david_gareja': (41.4470, 45.3770), 'udabno': (41.4440, 45.3800),
 'kutaisi': (42.2679, 42.7180), 'gelati': (42.2955, 42.7670), 'prometheus': (42.3760, 42.6020),
 'martvili': (42.4130, 42.3790), 'okatse': (42.4610, 42.5240), 'kinchkha': (42.4820, 42.5010),
 'zugdidi': (42.5088, 41.8709), 'dadiani': (42.5100, 41.8730),
 'borjomi': (41.8400, 43.3900), 'borjomi_np': (41.8400, 43.4500), 'bakuriani': (41.7480, 43.5320),
 'vardzia': (41.3790, 43.2870), 'rabati': (41.6390, 42.9860),
 'dashbashi': (41.6000, 44.0930), 'tsalka': (41.6000, 44.0900),
 'nikortsminda': (42.4650, 43.0300), 'shaori': (42.6600, 43.1900), 'ambrolauri': (42.5210, 43.1560),
 'mestia': (43.0450, 42.7290), 'ushguli': (42.9160, 43.0230),
 'shatili': (42.6600, 45.1550), 'mutso': (42.6900, 45.1900), 'datvisjvari': (42.5000, 45.0000),
 'omalo': (42.3670, 45.6390), 'abano_pass': (42.3000, 45.5000), 'keselo': (42.3660, 45.6390),
 'shenako': (42.3450, 45.6900), 'dartlo': (42.4270, 45.6700),
 'batumi': (41.6460, 41.6400), 'batumi_boulevard': (41.6510, 41.6350), 'gonio': (41.5730, 41.5720),
 'batumi_botanical': (41.6940, 41.7080), 'machakhela': (41.5500, 41.7500), 'gomis_mta': (41.9000, 42.3000),
 'khulo': (41.6450, 42.3100), 'ureki': (41.9880, 41.7770), 'nasakirali': (41.9700, 42.0000),
 # Ереван / Армения
 'yerevan': (40.1792, 44.4991), 'garni': (40.1120, 44.7300), 'geghard': (40.1400, 44.8180),
 'sevan': (40.5600, 45.0100), 'dilijan': (40.7400, 44.8600),
 # Тбилиси-достопримечательности
 'narikala': (41.6880, 44.8090), 'metekhi': (41.6910, 44.8110), 'abanotubani': (41.6890, 44.8110),
 'bridge_peace': (41.6934, 44.8092), 'rike_park': (41.6930, 44.8100), 'mtatsminda_park': (41.6950, 44.7910),
 'mtatsminda_pantheon': (41.6980, 44.7930), 'funicular': (41.7010, 44.7950), 'mother_georgia': (41.6875, 44.8060),
 'botanical_tbilisi': (41.6840, 44.8040), 'freedom_square': (41.6934, 44.8015), 'shardeni': (41.6905, 44.8085),
 'sioni': (41.6912, 44.8080), 'anchiskhati': (41.6928, 44.8073), 'meidan': (41.6895, 44.8100),
 'legvtakhevi': (41.6875, 44.8115), 'sameba': (41.6975, 44.8175), 'dry_bridge': (41.6980, 44.7960),
 'deserter_bazaar': (41.7095, 44.7920), 'fabrika': (41.7110, 44.7980), 'vera': (41.7080, 44.7850),
 'rustaveli_ave': (41.6980, 44.7990), 'kote_afkhazi': (41.6905, 44.8075), 'kura_embankment': (41.6920, 44.8100),
 'chugureti': (41.7150, 44.8000), 'sololaki': (41.6890, 44.8000), 'saburtalo': (41.7350, 44.7500),
 'highways_ministry': (41.7090, 44.7350), 'chronicle': (41.7900, 44.7770), 'wedding_palace': (41.7120, 44.8320),
 'tbilisi_zoo': (41.7150, 44.7770),
}

# raw route-name (после снятия префикса "День N —") -> список place_keys. Отсутствует => пропуск.
M = {
 'Тбилиси': ['tbilisi'], 'Выезд из Тбилиси': ['tbilisi'], 'Тбилиси → Местиа': ['tbilisi','mestia'],
 'Крепость Ананури': ['ananuri'], 'Жинвальское водохранилище': ['zhinvali'],
 'Жинвальское водохранилище и Ананури': ['zhinvali','ananuri'], 'Пасанаури': ['pasanauri'],
 'Гудаури': ['gudauri'], 'Смотровая Гудаури': ['gudauri'], 'Арка Дружбы народов': ['friendship_arch'],
 'Крестовый перевал': ['cross_pass'], 'Степанцминда': ['stepantsminda'], 'Степанцминда — обед': ['stepantsminda'],
 'Казбеги': ['stepantsminda'], 'Казбеги/Гудаури': ['stepantsminda'], 'Церковь Гергети': ['gergeti'],
 'Ущелье Трусо — старт': ['truso'], 'Минеральные озёра': ['truso'],
 'Мцхета': ['mtskheta'], 'Старый город Мцхеты': ['mtskheta'], 'Монастырь Самтавро': ['samtavro'],
 'Собор Светицховели': ['svetitskhoveli'], 'Монастырь Джвари': ['jvari_mon'],
 'Смотровая над слиянием Куры и Арагви': ['jvari_mon'], 'Мцхета + Гори': ['mtskheta','gori'],
 'Мцхета и Гори': ['mtskheta','gori'], 'Мцхета и Джвари': ['mtskheta','jvari_mon'], 'Мцхета + Казбеги': ['mtskheta','stepantsminda'],
 'Гори': ['gori'], 'Гори — крепость Горисцихе': ['gori'], 'Гори + Уплисцихе': ['gori','uplistsikhe'],
 'Музей Сталина': ['stalin_museum'], 'Уплисцихе': ['uplistsikhe'], 'Уплисцихе — пещерный город': ['uplistsikhe'],
 'Кахетия': ['telavi'], 'Гомборский перевал': ['gombori'], 'Монастырь Бодбе': ['bodbe'],
 'Сигнахи': ['sighnaghi'], 'Музей Чавчавадзе': ['tsinandali'], 'Сагареджо': ['sagarejo'],
 'Телави': ['telavi'], 'Телави — первая винодельня': ['telavi'], 'Телави — крепость Батонисцихе': ['telavi'],
 'Монастырь Алаверди (XI в.)': ['alaverdi'], 'Икалто (VI в.)': ['ikalto'],
 'Цинандали — вторая винодельня': ['tsinandali'], 'Усадьба Цинандали': ['tsinandali'],
 'Кварели — родина Киндзмараули': ['kvareli'], 'Винодельня «Киндзмараули Марани»': ['kvareli'],
 'Лавра Давида': ['david_gareja'], 'Пещеры Удабно': ['udabno'],
 'Кутаиси': ['kutaisi'], 'Кутаиси и каньоны': ['kutaisi'], 'Монастырь Гелати': ['gelati'],
 'Пещера Прометея': ['prometheus'], 'Мартвильский каньон': ['martvili'], 'Каньон Окаце': ['okatse'],
 'Водопад Кинчха': ['kinchkha'], 'Зугдиди': ['zugdidi'], 'Дворец Дадиани': ['dadiani'], 'Музей Дадиани': ['dadiani'],
 'Боржоми': ['borjomi'], 'Боржоми — Центральный парк': ['borjomi'], 'Боржоми и Вардзия': ['borjomi','vardzia'],
 'Национальный парк': ['borjomi_np'], 'Бакуриани': ['bakuriani'],
 'Вардзия': ['vardzia'], 'Крепость Рабати': ['rabati'],
 'Смотровая и стеклянный мост': ['dashbashi'], 'Водопады Дашбаши': ['dashbashi'], 'Озеро Цалка': ['tsalka'],
 'Храм Никорцминда': ['nikortsminda'], 'Озеро Шаори': ['shaori'], 'Амбролаури и деревни': ['ambrolauri'],
 'Сванетия': ['mestia'], 'Местия': ['mestia'], 'Сванские башни': ['mestia'], 'Ушгули': ['ushguli'], 'Зугдиди ': ['zugdidi'],
 'Шатили': ['shatili'], 'Муцо и Анатори': ['mutso'], 'Перевал Датвисджвари': ['datvisjvari'],
 'Прибытие в Омало': ['omalo'], 'Перевал Абано (~2900 м)': ['abano_pass'], 'Крепость Кесело': ['keselo'],
 'Село Шенако': ['shenako'], 'Село Дартло': ['dartlo'], 'Треккинг к Дартло': ['dartlo'],
 'Батуми': ['batumi'], 'Вечерний Батуми': ['batumi'], 'Выезд из Батуми': ['batumi'], 'Батумский бульвар': ['batumi_boulevard'],
 'Крепость Гонио': ['gonio'], 'Ущелье Мачахела': ['machakhela'], 'Вершина Гомис Мта': ['gomis_mta'],
 'Серпантин и Хулойский перевал': ['khulo'], 'Пляж магнитных песков': ['ureki'], 'Парк Насакирали': ['nasakirali'],
 'Дни 5–6 — Батуми + Аджария': ['batumi'], 'Батуми + Аджария': ['batumi'], 'Батуми или Сванетия': ['batumi'],
 # Армения
 'Граница → Ереван': ['yerevan'], 'Гарни + Гегард': ['garni','geghard'], 'Озеро Севан': ['sevan'], 'Дилижан': ['dilijan'],
 # Тбилиси пешие
 'Крепость Нарикала': ['narikala'], 'Канатная дорога на Нарикалу': ['narikala'], 'Нарикала / Метехи': ['narikala','metekhi'],
 'Нарикала и серные бани': ['narikala'], 'Метехи': ['metekhi'], 'Метехский мост': ['metekhi'],
 'Абанотубани': ['abanotubani'], 'Купольные серные бани': ['abanotubani'], 'Серные бани (по желанию)': ['abanotubani'],
 'Водопад Легвтахеви': ['legvtakhevi'], 'Мост Мира': ['bridge_peace'], 'Парк Рике': ['rike_park'],
 'Встреча в парке Рике': ['rike_park'], 'Монумент «Мать Грузия»': ['mother_georgia'],
 'Ботанический сад': ['botanical_tbilisi'], 'Спуск через Ботанический сад': ['botanical_tbilisi'],
 'Площадь Свободы': ['freedom_square'], 'Ул. Шардани': ['shardeni'], 'Сионский собор': ['sioni'], 'Сиони': ['sioni'],
 'Базилика Анчисхати': ['anchiskhati'], 'Анчисхати': ['anchiskhati'], 'Встреча на площади Мейдан': ['meidan'],
 'Самеба (Собор Святой Троицы)': ['sameba'], 'Сухой мост': ['dry_bridge'], 'Дезертирский базар': ['deserter_bazaar'],
 'Фабрика — Creative Hub': ['fabrika'], 'Хаб «Фабрика»': ['fabrika'], 'Район Вера': ['vera'],
 'Проспект Руставели — сталинский ампир': ['rustaveli_ave'], 'Метро «Руставели» и «Площадь Свободы»': ['rustaveli_ave'],
 'Летопись Грузии': ['chronicle'], 'Министерство автодорог Грузии': ['highways_ministry'],
 'Мозаики Сабуртало': ['saburtalo'], 'Дворец торжественных обрядов': ['wedding_palace'],
 'Дворец бракосочетаний': ['wedding_palace'], 'Ул. Котэ Афхази': ['kote_afkhazi'], 'Набережная Куры': ['kura_embankment'],
 'Муралы района Чугурети': ['chugureti'], 'Дворы Сололаки': ['sololaki'], 'Зоопарк': ['tbilisi_zoo'],
 'Пантеон знаменитых грузин': ['mtatsminda_pantheon'], 'Парк и телебашня': ['mtatsminda_park'],
 'Нижняя станция фуникулёра': ['funicular'], 'Подъём на историческом фуникулёре': ['funicular'],
 'Метехи и Старый город': ['metekhi'],
}

# короткие человекочитаемые подписи для маркеров (по place_key)
LABEL = {
 'tbilisi':'Тбилиси','mtskheta':'Мцхета','jvari_mon':'Джвари','svetitskhoveli':'Светицховели','samtavro':'Самтавро',
 'gori':'Гори','stalin_museum':'Музей Сталина','uplistsikhe':'Уплисцихе','ananuri':'Ананури','zhinvali':'Жинвали',
 'pasanauri':'Пасанаури','gudauri':'Гудаури','friendship_arch':'Арка Дружбы','cross_pass':'Крестовый перевал',
 'stepantsminda':'Степанцминда','gergeti':'Гергети','truso':'Ущелье Трусо','telavi':'Телави','alaverdi':'Алаверди',
 'ikalto':'Икалто','tsinandali':'Цинандали','kvareli':'Кварели','sighnaghi':'Сигнахи','bodbe':'Бодбе','gombori':'Гомборский перевал',
 'sagarejo':'Сагареджо','david_gareja':'Давид-Гареджи','udabno':'Удабно','kutaisi':'Кутаиси','gelati':'Гелати',
 'prometheus':'Пещера Прометея','martvili':'Мартвили','okatse':'Окаце','kinchkha':'Кинчха','zugdidi':'Зугдиди','dadiani':'Дворец Дадиани',
 'borjomi':'Боржоми','borjomi_np':'Нац. парк Боржоми','bakuriani':'Бакуриани','vardzia':'Вардзия','rabati':'Рабати',
 'dashbashi':'Дашбаши','tsalka':'Озеро Цалка','nikortsminda':'Никорцминда','shaori':'Озеро Шаори','ambrolauri':'Амбролаури',
 'mestia':'Местия','ushguli':'Ушгули','shatili':'Шатили','mutso':'Муцо','datvisjvari':'Перевал Датвисджвари',
 'omalo':'Омало','abano_pass':'Перевал Абано','keselo':'Кесело','shenako':'Шенако','dartlo':'Дартло',
 'batumi':'Батуми','batumi_boulevard':'Батумский бульвар','gonio':'Гонио','batumi_botanical':'Ботанический сад',
 'machakhela':'Мачахела','gomis_mta':'Гомис Мта','khulo':'Хуло','ureki':'Уреки','nasakirali':'Насакирали',
 'yerevan':'Ереван','garni':'Гарни','geghard':'Гегард','sevan':'Озеро Севан','dilijan':'Дилижан',
 'narikala':'Нарикала','metekhi':'Метехи','abanotubani':'Абанотубани','bridge_peace':'Мост Мира','rike_park':'Парк Рике',
 'mtatsminda_park':'Мтацминда','mtatsminda_pantheon':'Пантеон','funicular':'Фуникулёр','mother_georgia':'Мать Грузия',
 'botanical_tbilisi':'Ботанический сад','freedom_square':'Пл. Свободы','shardeni':'Ул. Шардени','sioni':'Сиони',
 'anchiskhati':'Анчисхати','meidan':'Мейдан','legvtakhevi':'Легвтахеви','sameba':'Самеба','dry_bridge':'Сухой мост',
 'deserter_bazaar':'Дезертирский базар','fabrika':'Фабрика','vera':'Вера','rustaveli_ave':'Пр. Руставели',
 'kote_afkhazi':'Ул. Котэ Афхази','kura_embankment':'Набережная Куры','chugureti':'Чугурети','sololaki':'Сололаки',
 'saburtalo':'Сабуртало','highways_ministry':'Мин. автодорог','chronicle':'Летопись Грузии','wedding_palace':'Дворец обрядов',
 'tbilisi_zoo':'Зоопарк',
}

DAY_PREFIX = re.compile(r'^(Дни?\s+[\d–\-—]+\s*[—-]\s*|День\s+\d+\s*[—-]\s*)')

def resolve(raw, slug):
    raw = re.sub(r'\s+', ' ', raw).strip()
    raw = DAY_PREFIX.sub('', raw).strip()
    keys = M.get(raw)
    if keys is None:
        return []
    # контекст: Ботанический сад в батумских турах = батумский
    if 'batumi' in slug:
        keys = ['batumi_botanical' if k == 'botanical_tbilisi' else k for k in keys]
    return keys

def tour_points(path):
    slug = path.split('/')[1]
    html = open(path, encoding='utf-8').read()
    names = re.findall(r'class="route-name"[^>]*>([^<]+)<', html)
    seq = []
    for n in names:
        for k in resolve(n, slug):
            if not seq or seq[-1] != k:  # dedup соседних
                seq.append(k)
    # схлопнуть повтор Тбилиси в конце (round-trip) — оставить как есть если это единств.
    # убрать дубликаты не-соседние, сохраняя порядок первого появления
    seen=set(); uniq=[]
    for k in seq:
        if k not in seen:
            seen.add(k); uniq.append(k)
    return slug, uniq

BLOCK = '''<div id="tour-route-map" style="margin:18px 0 6px;height:420px;border-radius:12px;overflow:hidden;border:1px solid #E5E7EB;background:#EAEFEA"></div>
<script>
(function(){
  var el=document.getElementById('tour-route-map');if(!el)return;var booted=false;
  window.__tourRouteMapInit=function(){
    var stops=__STOPS__;
    var map=new google.maps.Map(el,{zoom:8,mapTypeControl:false,streetViewControl:false,fullscreenControl:true,gestureHandling:'cooperative',clickableIcons:false});
    new google.maps.Polyline({path:stops.map(function(s){return{lat:s.lat,lng:s.lng};}),strokeColor:'#1A3D2E',strokeOpacity:.85,strokeWeight:4,map:map});
    function Label(pos,text,dir){this.pos=pos;this.text=text;this.dir=dir;this.div=null;}
    Label.prototype=new google.maps.OverlayView();
    Label.prototype.onAdd=function(){var d=document.createElement('div');d.style.cssText='position:absolute;background:#fff;border:1px solid #1A3D2E;color:#14331f;font:600 12px/1.2 Arial,sans-serif;padding:3px 7px;border-radius:6px;box-shadow:0 1px 3px rgba(0,0,0,.3);white-space:nowrap';d.textContent=this.text;this.div=d;this.getPanes().floatPane.appendChild(d);};
    Label.prototype.draw=function(){var p=this.getProjection().fromLatLngToDivPixel(this.pos);if(!p||!this.div)return;var d=this.div;d.style.top=p.y+'px';if(this.dir<0){d.style.left=(p.x-16)+'px';d.style.transform='translate(-100%,-50%)';}else{d.style.left=(p.x+16)+'px';d.style.transform='translate(0,-50%)';}};
    Label.prototype.onRemove=function(){if(this.div&&this.div.parentNode)this.div.parentNode.removeChild(this.div);this.div=null;};
    var b=new google.maps.LatLngBounds();
    stops.forEach(function(s,i){var pos={lat:s.lat,lng:s.lng};
      new google.maps.Marker({position:pos,map:map,label:{text:String(i+1),color:'#fff',fontWeight:'700',fontSize:'12px'},icon:{path:google.maps.SymbolPath.CIRCLE,scale:13,fillColor:'#1A3D2E',fillOpacity:1,strokeColor:'#fff',strokeWeight:2}});
      new Label(new google.maps.LatLng(s.lat,s.lng),(i+1)+'. '+s.name,(i%2===0)?1:-1).setMap(map);
      b.extend(pos);});
    map.fitBounds(b,{top:46,right:120,bottom:30,left:120});
  };
  function boot(){if(booted)return;booted=true;var s=document.createElement('script');s.async=true;s.src='https://maps.googleapis.com/maps/api/js?key=__KEY__&callback=__tourRouteMapInit&language=ru&region=GE';document.head.appendChild(s);}
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){boot();io.disconnect();}});},{rootMargin:'250px'});io.observe(el);}else{boot();}
})();
</script>
<p style="font-size:13px;color:#6B7280;margin:8px 0 0;text-align:center">Маршрут: __CAPTION__</p>'''

def build_block(pts):
    stops=[{'name':LABEL[k],'lat':C[k][0],'lng':C[k][1]} for k in pts]
    js=json.dumps(stops, ensure_ascii=False)
    caption=' → '.join(LABEL[k] for k in pts)
    return BLOCK.replace('__STOPS__', js).replace('__KEY__', MAPS_KEY).replace('__CAPTION__', caption)

def insert_map(path, block):
    html=open(path, encoding='utf-8').read()
    if 'tour-route-map' in html or 'kazbegi-map' in html:
        return 'already'
    m=re.search(r'<div class="route-grid">', html)
    if not m: return 'no-grid'
    end=html.find('</section>', m.end())
    if end<0: return 'no-section-end'
    new=html[:end] + block + '\n' + html[end:]
    open(path,'w',encoding='utf-8').write(new)
    return 'ok'

if __name__ == '__main__':
    write = '--write' in sys.argv
    tours = sorted(glob.glob('ekskursiya/*/index.html'))
    ok=0; skip=0; wrote=0
    for t in tours:
        slug, pts = tour_points(t)
        if slug == 'ekskursiya-kazbegi-iz-tbilisi':
            continue
        if len(pts) < 2:
            skip+=1; continue
        ok+=1
        labels=[LABEL[k] for k in pts]
        status=''
        if write:
            status=insert_map(t, build_block(pts))
            if status=='ok': wrote+=1
        print(f"[{len(pts)}] {slug}: {labels}" + (f"  -> {status}" if write else ''))
    print(f"\nИтого: карта у {ok} туров, пропуск {skip}" + (f", записано {wrote}" if write else ''))
