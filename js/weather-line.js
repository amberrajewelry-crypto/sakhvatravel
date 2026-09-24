// Погода по направлению тура (Open-Meteo через /api/weather). Одна строка в hero тура
// и под выбранной датой в форме брони. Кэш 15 мин в sessionStorage, без ключей.
(function(){
  var L={
    ru:{now:'Сейчас в {c}: {t}°, {w}',day:'{d} в {c}: {lo}…{hi}°, {w}',rain:'дождь {p}%',
        w:['ясно','малооблачно','облачно','пасмурно','туман','морось','дождь','снег','ливень','снегопад','гроза'],
        m:['янв','фев','мар','апр','мая','июн','июл','авг','сен','окт','ноя','дек']},
    en:{now:'Now in {c}: {t}°, {w}',day:'{d} in {c}: {lo}…{hi}°, {w}',rain:'rain {p}%',
        w:['clear','mostly clear','partly cloudy','overcast','fog','drizzle','rain','snow','showers','snowfall','thunderstorm'],
        m:['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']},
    ka:{now:'ახლა {c}: {t}°, {w}',day:'{d} {c}: {lo}…{hi}°, {w}',rain:'წვიმა {p}%',
        w:['მოწმენდილი','ნაწილობრივ მოღრუბლული','ღრუბლიანი','მოღრუბლული','ნისლი','ჟინჟღლი','წვიმა','თოვლი','თავსხმა','თოვა','ჭექა-ქუხილი'],
        m:['იან','თებ','მარ','აპრ','მაი','ივნ','ივლ','აგვ','სექ','ოქტ','ნოე','დეკ']}
  };
  var CITY={ru:{'Степанцминда':'Степанцминде','Мцхета':'Мцхете','Местиа':'Местии','Боржоми / Ахалцихе':'Боржоми'},en:{'Степанцминда':'Stepantsminda','Телави':'Telavi','Тбилиси':'Tbilisi','Батуми':'Batumi','Кутаиси':'Kutaisi','Местиа':'Mestia','Гудаури':'Gudauri','Бакуриани':'Bakuriani','Боржоми':'Borjomi','Сигнахи':'Sighnaghi','Мцхета':'Mtskheta','Гори':'Gori','Дашбаши':'Dashbashi','Амбролаури':'Ambrolauri','Боржоми / Ахалцихе':'Borjomi'},
    ka:{'Степанцминда':'სტეფანწმინდაში','Телави':'თელავში','Тбилиси':'თბილისში','Батуми':'ბათუმში','Кутаиси':'ქუთაისში','Местиа':'მესტიაში','Гудаури':'გუდაურში','Бакуриани':'ბაკურიანში','Боржоми':'ბორჯომში','Сигнахи':'სიღნაღში','Мцхета':'მცხეთაში','Гори':'გორში','Дашбаши':'დაშბაშში','Амбролаури':'ამბროლაურში','Боржоми / Ахалцихе':'ბორჯომში'}};
  function wi(c){return c===0?0:c<=2?(c===1?1:2):c===3?3:c<=48?4:c<=57?5:c<=67?6:c<=77?7:c<=82?8:c<=86?9:10}
  function ico(c){return c===0?'☀':c<=2?'🌤':c===3?'☁':c<=48?'🌫':c<=67?'🌧':c<=77?'🌨':c<=82?'🌧':c<=86?'🌨':'⛈'}
  function city(d,lang){var c=d.city.split(' /')[0].replace(/ \(.*\)/,'');var m=CITY[lang]||{};return m[d.city]||m[c]||c}
  function get(region,cb){
    var k='sw:'+region,now=Date.now();
    try{var c=JSON.parse(sessionStorage.getItem(k)||'null');if(c&&now-c.ts<9e5){cb(c.d);return}}catch(e){}
    fetch('/api/weather/?region='+region).then(function(r){return r.json()}).then(function(d){
      if(!d||!d.daily)return;try{sessionStorage.setItem(k,JSON.stringify({ts:now,d:d}))}catch(e){}cb(d)}).catch(function(){});
  }
  function fmt(tpl,o){return tpl.replace(/\{(\w+)\}/g,function(_,k){return o[k]})}
  // Строка на конкретную дату (форма брони); null — если даты нет в 14-дневном прогнозе
  window.swWeatherDay=function(d,date,lang){
    var t=L[lang]||L.ru,x=null;for(var i=0;i<d.daily.length;i++)if(d.daily[i].date===date)x=d.daily[i];
    if(!x)return null;var p=date.split('-');
    var s=ico(x.code)+' '+fmt(t.day,{d:parseInt(p[2],10)+' '+t.m[parseInt(p[1],10)-1],c:city(d,lang),lo:x.min,hi:x.max,w:t.w[wi(x.code)]});
    if(x.pop>=40)s+=' · '+fmt(t.rain,{p:x.pop});return s;
  };
  window.swWeatherNow=function(d,lang){var t=L[lang]||L.ru;return ico(d.current.code)+' '+fmt(t.now,{c:city(d,lang),t:(d.current.temp>0?'+':'')+d.current.temp,w:t.w[wi(d.current.code)]})};
  window.swWeather=get;
  // Авто: <div class="hero-weather" data-region="kazbegi" data-lang="ru">
  document.querySelectorAll('.hero-weather[data-region]').forEach(function(el){
    get(el.getAttribute('data-region'),function(d){
      var lang=el.getAttribute('data-lang')||'ru',s=window.swWeatherNow(d,lang);
      var tmr=d.daily[1];if(tmr){var t=L[lang]||L.ru;s+=' · '+(lang==='ru'?'завтра':lang==='en'?'tomorrow':'ხვალ')+' '+tmr.min+'…'+tmr.max+'°, '+t.w[wi(tmr.code)]}
      el.textContent=s;el.style.display='';el.style.maxWidth='100%';el.style.whiteSpace='normal';el.style.overflowWrap='anywhere';
    });
  });
})();
