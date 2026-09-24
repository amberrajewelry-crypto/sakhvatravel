#!/usr/bin/env python3
"""Генерирует кластер /pogoda/ на 3 языках (ru, en=/en/pogoda, ka=/ge/pogoda).
Каждая спица: живой прогноз-виджет + статичная климат-таблица/сравнение (indexable)
+ текст гида + CTA на тур + FAQ (schema) + перелинковка + hreflang×3.
Usage: python3 scripts/gen-pogoda.py [--only slug] [--lang ru,en,ka]
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEO = json.loads((ROOT / "data" / "pogoda-geo.json").read_text(encoding="utf-8"))
CLIM = json.loads((ROOT / "data" / "climate.json").read_text(encoding="utf-8"))
I18N = json.loads((ROOT / "data" / "pogoda-i18n.json").read_text(encoding="utf-8"))
BY = {p["slug"]: p for p in GEO}
V = "20260907b"

LANGS = ["ru", "en", "ka"]
PREFIX = {"ru": "", "en": "/en", "ka": "/ge"}          # URL prefix
OUTDIR = {"ru": "pogoda", "en": "en/pogoda", "ka": "ge/pogoda"}
HREF = {"ru": "ru", "en": "en", "ka": "ka"}

MON_GEN = {  # родительный/для даты «5 сентября»
    "ru": ["", "января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"],
    "en": ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "ka": ["", "იანვარი", "თებერვალი", "მარტი", "აპრილი", "მაისი", "ივნისი", "ივლისი", "აგვისტო", "სექტემბერი", "ოქტომბერი", "ნოემბერი", "დეკემბერი"],
}
MON_NOM = {  # именительный, для таблицы/заголовков
    "ru": ["", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
    "en": MON_GEN["en"],
    "ka": MON_GEN["ka"],
}
MON_SHORT = {
    "ru": ["", "янв", "фев", "мар", "апр", "мая", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"],
    "en": ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "ka": ["", "იან", "თებ", "მარ", "აპრ", "მაი", "ივნ", "ივლ", "აგვ", "სექ", "ოქტ", "ნოე", "დეკ"],
}
DOW = {
    "ru": ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"],
    "en": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    "ka": ["კვ", "ორ", "სამ", "ოთხ", "ხუ", "პარ", "შაბ"],
}
SEASON_MONTHS = [("wint", [12, 1, 2]), ("spr", [3, 4, 5]), ("sum", [6, 7, 8]), ("aut", [9, 10, 11])]
WLABELS = {  # ключи погоды для JS meta() -> подпись
    "ru": {"clear": "Ясно", "pcloud": "Малооблачно", "cloud": "Облачно", "fog": "Туман", "drizzle": "Морось", "rain": "Дождь", "snow": "Снег", "shower": "Ливень", "snowfall": "Снегопад", "storm": "Гроза"},
    "en": {"clear": "Clear", "pcloud": "Partly cloudy", "cloud": "Cloudy", "fog": "Fog", "drizzle": "Drizzle", "rain": "Rain", "snow": "Snow", "shower": "Showers", "snowfall": "Snowfall", "storm": "Thunderstorm"},
    "ka": {"clear": "მოწმენდილი", "pcloud": "მცირე ღრუბლიანი", "cloud": "ღრუბლიანი", "fog": "ნისლი", "drizzle": "ბანწვა", "rain": "წვიმა", "snow": "თოვლი", "shower": "თქეში", "snowfall": "თოვა", "storm": "ჭექა-ქუხილი"},
}
SEASON_NAME = {
    "ru": {"wint": "Зима", "spr": "Весна", "sum": "Лето", "aut": "Осень"},
    "en": {"wint": "Winter", "spr": "Spring", "sum": "Summer", "aut": "Autumn"},
    "ka": {"wint": "ზამთარი", "spr": "გაზაფხული", "sum": "ზაფხული", "aut": "შემოდგომა"},
}
GE_FONT_LINKS = ('<link rel="preload" href="/fonts/noto-sans-georgian.woff2" as="font" '
                 'type="font/woff2" crossorigin><link rel="stylesheet" href="/css/ge.css">')
NAV_TOURS = {"ru": "/tury-v-gruziyu/", "en": "/en/tours-in-georgia/", "ka": "/ge/ekskursionnye-tury-v-gruziyu/"}
PRIVACY = {"ru": "/privacy/", "en": "/en/policy/", "ka": "/ge/privacy/"}
EXTRA_NAMES = {
    "ru": {"_khulo": "Хуло", "_chiatura": "Чиатура", "_zugdidi": "Зугдиди", "_omalo": "Тушети (Омало)"},
    "en": {"_khulo": "Khulo", "_chiatura": "Chiatura", "_zugdidi": "Zugdidi", "_omalo": "Tusheti (Omalo)"},
    "ka": {"_khulo": "ხულო", "_chiatura": "ჭიათურა", "_zugdidi": "ზუგდიდი", "_omalo": "თუშეთი (ომალო)"},
}

# UI-строки шаблона и генератора
L = {
"ru": {
  "nav_tours": "Туры в Грузию", "nav_exc": "Экскурсии", "nav_prices": "Цены", "nav_about": "О нас",
  "nav_blog": "Блог", "nav_weather": "Погода", "nav_contacts": "Контакты", "nav_pay": "Оплатить онлайн",
  "weather_ge": "Погода в Грузии", "book": "Забронировать", "home": "Главная",
  "kicker": "Прогноз погоды по дням", "forecast_week": "Прогноз на неделю", "today": "Сегодня",
  "loading": "Загрузка прогноза…", "unavail": "Прогноз временно недоступен", "no_data": "нет данных",
  "day_to": "Днём до", "night": "ночью", "updated": "обновлено", "h1_pre": "Погода в",
  "lede": "Прогноз на неделю вперёд и климат по месяцам. Лучшее время для поездки — {best}.",
  "bridge": "Погода в {np} — не помеха: тур с гидом Тимуром от ₾80",
  "cta_h": "Спланировать поездку под погоду",
  "cta_p": "Гид Тимур подберёт лучшие даты и составит маршрут. Ответ в WhatsApp за 15 минут.",
  "cta_wa": "Написать гиду", "wa_text": "Хочу спланировать поездку в {np}",
  "guide_h": "Когда лучше ехать в {np}", "near_h": "Погода рядом", "near_p": "Сравните с соседними направлениями.",
  "faq_h": "Частые вопросы", "privacy": "Политика конфиденциальности", "guide": "Гид Тимур",
  "all_regions": "Все регионы Грузии", "weather_in": "Погода в {np}",
  "fc_city_h": "Погода в {np}: прогноз по дням",
  "fc_city_p": "Прогноз на неделю вперёд и тренд на 2 недели: температура днём и ночью, вероятность осадков. Обновляется каждый час.",
  "fc_note_city": "Ближайшие 7 дней — точный прогноз, дни 8–14 — ориентир (Open-Meteo).",
  "fc_reg_h": "Погода в {np} по городам на неделю",
  "fc_reg_p": "Прогноз по дням для ключевых городов региона — климат {np} различается по высоте. Обновляется каждый час.",
  "fc_note_reg": "Прогноз Open-Meteo. Погода сейчас — в виджете вверху.",
  "sum_city_h": "Климат {np}: когда планировать поездку",
  "sum_city": "В {np} по сезонам держится: зимой около {w}° днём, весной {sp}°, летом {su}°, осенью {au}°. Самый тёплый месяц — {warm} (до {wt}° днём), самый прохладный — {cold} ({ct}°). Больше всего осадков в {wet}. Подробные нормали по месяцам — в таблице ниже.",
  "sum_reg_h": "Климат {np}: чем отличаются города",
  "sum_reg": "Климат {np} меняется по высоте. Летом теплее всего в {wl} — около {ws}° днём, прохладнее в {cl} ({cs}°). Зимой в {wl} держится {wz}°, а в {cl} — {cz}°. Прогноз по каждому городу — в таблице выше, помесячные нормали — на страницах городов.",
  "mon_h": "Климат {np} по месяцам",
  "mon_p": "Средние температуры днём и ночью и число дней с осадками. Зелёным — самые комфортные для поездки месяцы.",
  "th_month": "Месяц", "th_day": "Днём", "th_night": "Ночью", "th_rain": "Дней с осадками",
  "mon_note": "Нормали по данным Open-Meteo (среднее за 2014–2023). Живой прогноз — в виджете вверху.",
  "cmp_h": "Климат {np}: сравнение по городам",
  "cmp_p": "Средняя дневная температура по сезонам в ключевых точках региона — климат {np} заметно меняется по высоте.{links}",
  "cmp_links": " Подробный прогноз по городам: {cities}.",
  "th_city": "Город", "th_best": "Лучшее время",
  "cmp_note": "Днём, средние по сезонам (Open-Meteo 2014–2023). Помесячные данные — на страницах городов.",
  "faq_when_q": "Когда лучше ехать в {np}?",
  "faq_when_a": "Самое комфортное время — {best}: тепло, но без изнуряющей жары, и меньше дождей. Точные цифры по месяцам смотрите в таблице климата выше.",
  "faq_now_q": "Какая погода в {np} сейчас?",
  "faq_now_a": "Актуальную температуру и прогноз на неделю показывает живой виджет вверху страницы — данные обновляются автоматически.",
  "faq_wint_q": "Холодно ли зимой в {np}?",
  "zima_cold": "Да, зима настоящая: в январе днём около {tx}°, ночью до {tn}°, лежит снег. Это зимний сезон для гор и лыж.",
  "zima_mild": "Зима мягкая: в январе днём около {tx}°, ночью {tn}°. Снег бывает, но быстро сходит.",
  "zima_warm": "Зима тёплая: в январе днём около {tx}°, ночью {tn}° — снега почти не бывает.",
  "title_city": "Погода в {np}: прогноз и климат по месяцам 2026",
  "desc_city": "Погода в {np}: прогноз на неделю вперёд по дням и климат по месяцам — температура, осадки. Когда лучше ехать: {best}. Советы гида.",
  "title_reg": "Погода в {np}: прогноз и климат по сезонам 2026",
  "desc_reg": "Погода в {np}: прогноз по дням для городов региона ({cnames}) и климат по сезонам. Когда лучше ехать, советы местного гида.",
  "default_best": "весна и осень", "best_fallback": "май и сентябрь",
  "pack": "Летом днём до {su}°, ночью около {sn}°: днём — лёгкая одежда, к вечеру пригодится кофта. Зимой днём {w}°, ночью до {wn}° — нужна тёплая куртка{snow}.",
  "pack_snow": " и обувь для снега", "pack_nosnow": "",
  "dry_line": "Меньше всего дождей — в {dry}: это самые ясные месяцы для прогулок и панорамных видов.",
  "elev_line": " {name} лежит на высоте {em} м над уровнем моря — вечера здесь заметно свежее, чем на равнине.",
  "reg_spread": " Летом разница между городами региона доходит до {diff}°, поэтому одежду берите с запасом — на тёплые долины и прохладные горы.",
  "faq_pack_q": "Что взять с собой в {np}?",
  "act_h": "Чем заняться в {np} по сезонам",
  "act_ski": "Главный сезон в {np} — зима: с декабря по март лежит снег, днём держится около {w}°, работают подъёмники и трассы. Летом ({su}° днём) сюда поднимаются за прохладой, альпийскими лугами и хайкингом. Подобрать даты и склоны поможет {tour}.",
  "act_beach": "Пляжный сезон в {np} — с июня по сентябрь: днём около {su}°, море прогрето, оживают набережная и кафе. Весной и осенью ({bt}) тише и дешевле — купаться прохладно, зато удобно осматривать окрестности. Маршрут к морю — {tour}.",
  "act_wine": "Кульминация года в {np} — ртвели в сентябре и октябре: сбор винограда и дегустации в семейных погребах, тёплые дни без летнего зноя. Летом жарко (до {su}° днём), зимой тихо и малолюдно ({w}°). Спланировать дегустации поможет {tour}.",
  "act_spa": "В {np} едут за минеральной водой и хвойным воздухом парка круглый год. Летом ({su}° днём) приятно гулять по терренкурам, зимой ({w}°) в получасе работает горнолыжный курорт. Собрать поездку под погоду поможет {tour}.",
  "act_alpine": "Горный сезон в {np} — с июня по сентябрь: днём около {su}°, открыты тропы, перевалы и виды на ледники. Зимой ({w}° днём) дороги в снегу и часть маршрутов закрыта. Комфортнее всего ехать в {bt}. Маршрут в горы — {tour}.",
  "act_heritage": "Древние памятники {npg} осматривают круглый год, но комфортнее в {bt}: летом на открытых площадках жарко (до {su}° днём), зимой ({w}°) малолюдно и прохладно. Пройти по крепостям и храмам удобнее всего с {tour}.",
  "act_canyon": "Каньоны и водопады {npg} полноводнее весной и в начале лета; купаться в бирюзовой воде приятно в июле и августе ({su}° днём). Зимой ({w}°) тропы скользкие, часть маршрутов закрыта. Лучшее время — {bt}. Маршрут — {tour}.",
  "act_city": "{np} открыт круглый год: музеи, серные бани и рестораны работают всегда. Комфортнее всего в {bt} — летом днём до {su}° и брусчатка раскаляется, зимой {w}° и малолюдно. Прогулка по старому городу — {tour}.",
},
"en": {
  "nav_tours": "Georgia tours", "nav_exc": "Excursions", "nav_prices": "Prices", "nav_about": "About",
  "nav_blog": "Blog", "nav_weather": "Weather", "nav_contacts": "Contacts", "nav_pay": "Pay online",
  "weather_ge": "Weather in Georgia", "book": "Book now", "home": "Home",
  "kicker": "Daily weather forecast", "forecast_week": "7-day forecast", "today": "Today",
  "loading": "Loading forecast…", "unavail": "Forecast temporarily unavailable", "no_data": "no data",
  "day_to": "Day up to", "night": "night", "updated": "updated", "h1_pre": "Weather in",
  "lede": "Forecast for the week ahead and climate by month. Best time to visit — {best}.",
  "bridge": "Weather in {np} is no obstacle: tours with guide Timur from ₾80",
  "cta_h": "Plan your trip around the weather",
  "cta_p": "Guide Timur will pick the best dates and plan the route. Reply on WhatsApp within 15 minutes.",
  "cta_wa": "Message the guide", "wa_text": "I want to plan a trip to {np}",
  "guide_h": "When to visit {np}", "near_h": "Weather nearby", "near_p": "Compare with neighbouring destinations.",
  "faq_h": "Frequently asked questions", "privacy": "Privacy policy", "guide": "Guide Timur",
  "all_regions": "All regions of Georgia", "weather_in": "Weather in {np}",
  "fc_city_h": "Weather in {np}: daily forecast",
  "fc_city_p": "Forecast for the week ahead and a 2-week trend: day and night temperature, chance of precipitation. Updated hourly.",
  "fc_note_city": "The next 7 days are an accurate forecast; days 8–14 are a guide (Open-Meteo).",
  "fc_reg_h": "Weather in {np} by city for the week",
  "fc_reg_p": "Daily forecast for the region's key towns — the climate of {np} varies with altitude. Updated hourly.",
  "fc_note_reg": "Open-Meteo forecast. Current weather is in the widget above.",
  "sum_city_h": "{np} climate: when to plan your trip",
  "sum_city": "In {np} the seasons run: about {w}° by day in winter, {sp}° in spring, {su}° in summer, {au}° in autumn. The warmest month is {warm} (up to {wt}° by day), the coolest is {cold} ({ct}°). Most rainfall is in {wet}. Detailed monthly normals are in the table below.",
  "sum_reg_h": "{np} climate: how the towns differ",
  "sum_reg": "The climate of {np} changes with altitude. In summer it's warmest in {wl} — about {ws}° by day, cooler in {cl} ({cs}°). In winter {wl} holds {wz}°, while {cl} sits at {cz}°. The forecast for each town is in the table above; monthly normals are on the town pages.",
  "mon_h": "{np} climate by month",
  "mon_p": "Average day and night temperatures and the number of days with precipitation. The most comfortable months to visit are in green.",
  "th_month": "Month", "th_day": "Day", "th_night": "Night", "th_rain": "Days with precip.",
  "mon_note": "Normals from Open-Meteo data (2014–2023 average). Live forecast is in the widget above.",
  "cmp_h": "{np} climate: comparison by town",
  "cmp_p": "Average daytime temperature by season at the region's key points — the climate of {np} varies noticeably with altitude.{links}",
  "cmp_links": " Detailed forecast by town: {cities}.",
  "th_city": "Town", "th_best": "Best time",
  "cmp_note": "Daytime, seasonal averages (Open-Meteo 2014–2023). Monthly data is on the town pages.",
  "faq_when_q": "When is the best time to visit {np}?",
  "faq_when_a": "The most comfortable time is {best}: warm but without exhausting heat, and less rain. See the exact monthly figures in the climate table above.",
  "faq_now_q": "What's the weather in {np} right now?",
  "faq_now_a": "The current temperature and the 7-day forecast are shown by the live widget at the top of the page — the data updates automatically.",
  "faq_wint_q": "Is it cold in {np} in winter?",
  "zima_cold": "Yes, winter is real here: around {tx}° by day in January, down to {tn}° at night, with snow. This is the winter season for mountains and skiing.",
  "zima_mild": "The winter is mild: around {tx}° by day in January, {tn}° at night. Snow falls but melts quickly.",
  "zima_warm": "The winter is warm: around {tx}° by day in January, {tn}° at night — snow is rare.",
  "title_city": "Weather in {np}: forecast and climate by month 2026",
  "desc_city": "Weather in {np}: forecast for the week ahead by day and climate by month — temperature, precipitation. Best time to visit: {best}.",
  "title_reg": "Weather in {np}: forecast & climate by season",
  "desc_reg": "Weather in {np}: daily forecast for the region's towns ({cnames}) and climate by season. When to visit, local guide's tips.",
  "default_best": "spring and autumn", "best_fallback": "May and September",
  "pack": "In summer it's up to {su}° by day and about {sn}° at night: light clothes for the day, a jumper for the evening. In winter it's {w}° by day and down to {wn}° at night — bring a warm coat{snow}.",
  "pack_snow": " and snow-proof shoes", "pack_nosnow": "",
  "dry_line": "The driest month is {dry} — the clearest time for walks and wide-open views.",
  "elev_line": " {name} sits at {em} m above sea level, so the evenings are noticeably cooler here than on the plains.",
  "reg_spread": " In summer the gap between the region's towns reaches {diff}°, so pack for both warm valleys and cool highlands.",
  "faq_pack_q": "What should I pack for {np}?",
  "act_h": "What to do in {np} by season",
  "act_ski": "The main season in {np} is winter: snow lies from December to March, around {w}° by day, with lifts and pistes open. In summer ({su}° by day) people come up for cool air, alpine meadows and hiking. {tour} helps you pick the dates and slopes.",
  "act_beach": "The beach season in {np} runs June to September: about {su}° by day, a warm sea and a lively promenade. Spring and autumn ({bt}) are quieter and cheaper — too cool to swim, but easy for sightseeing. The seaside route is {tour}.",
  "act_wine": "The year peaks in {np} with rtveli, the grape harvest in September and October: tastings in family cellars and warm days without the summer heat. Summers are hot (up to {su}° by day), winters quiet ({w}°). {tour} helps plan the tastings.",
  "act_spa": "People come to {np} for mineral water and pine-forest air year-round. In summer ({su}° by day) it's pleasant to walk the trails; in winter ({w}°) a ski resort runs half an hour away. {tour} builds the trip around the weather.",
  "act_alpine": "The mountain season in {np} is June to September: about {su}° by day, with open trails, passes and glacier views. In winter ({w}° by day) roads are snowed in and some routes close. The best months are {bt}. The mountain route is {tour}.",
  "act_heritage": "The ancient sites of {np} can be seen year-round, but {bt} are most comfortable: summers are hot on the open ruins (up to {su}° by day), winters ({w}°) quiet and cool. It's easiest to explore the fortresses and churches with {tour}.",
  "act_canyon": "The canyons and waterfalls of {np} run fullest in spring and early summer; the turquoise water is pleasant to swim in July and August ({su}° by day). In winter ({w}°) trails are slippery and some close. Best time — {bt}. The route is {tour}.",
  "act_city": "{np} is open year-round: museums, sulphur baths and restaurants never close. The most comfortable months are {bt} — summer days reach {su}° and the cobblestones bake, winters ({w}°) are quiet. The old-town walk is {tour}.",
},
"ka": {
  "nav_tours": "ტურები საქართველოში", "nav_exc": "ექსკურსიები", "nav_prices": "ფასები", "nav_about": "ჩვენ შესახებ",
  "nav_blog": "ბლოგი", "nav_weather": "ამინდი", "nav_contacts": "კონტაქტი", "nav_pay": "ონლაინ გადახდა",
  "weather_ge": "ამინდი საქართველოში", "book": "დაჯავშნა", "home": "მთავარი",
  "kicker": "ამინდის დღიური პროგნოზი", "forecast_week": "პროგნოზი კვირით", "today": "დღეს",
  "loading": "პროგნოზი იტვირთება…", "unavail": "პროგნოზი დროებით მიუწვდომელია", "no_data": "მონაცემები არ არის",
  "day_to": "დღისით", "night": "ღამით", "updated": "განახლდა", "h1_pre": "ამინდი —",
  "lede": "პროგნოზი კვირით წინ და კლიმატი თვეების მიხედვით. საუკეთესო დროა — {best}.",
  "bridge": "ამინდი — {np} — არ არის დაბრკოლება: ტური გიდ თიმურთან ₾80-დან",
  "cta_h": "დაგეგმეთ მოგზაურობა ამინდის მიხედვით",
  "cta_p": "გიდი თიმური შეარჩევს საუკეთესო თარიღებს და შეადგენს მარშრუტს. პასუხი WhatsApp-ში 15 წუთში.",
  "cta_wa": "მისწერეთ გიდს", "wa_text": "მინდა დავგეგმო მოგზაურობა — {np}",
  "guide_h": "როდის ჯობია {np} ჩასვლა", "near_h": "ამინდი ახლოს", "near_p": "შეადარეთ მეზობელ მიმართულებებს.",
  "faq_h": "ხშირად დასმული კითხვები", "privacy": "კონფიდენციალურობის პოლიტიკა", "guide": "გიდი თიმური",
  "all_regions": "საქართველოს ყველა რეგიონი", "weather_in": "ამინდი — {np}",
  "fc_city_h": "ამინდი — {np}: დღიური პროგნოზი",
  "fc_city_p": "პროგნოზი კვირით წინ და ტენდენცია 2 კვირით: ტემპერატურა დღისით და ღამით, ნალექის ალბათობა. ახლდება ყოველ საათს.",
  "fc_note_city": "უახლოესი 7 დღე — ზუსტი პროგნოზი, დღეები 8–14 — ორიენტირი (Open-Meteo).",
  "fc_reg_h": "ამინდი — {np} ქალაქების მიხედვით კვირით",
  "fc_reg_p": "დღიური პროგნოზი რეგიონის მთავარი ქალაქებისთვის — {npg} კლიმატი სიმაღლის მიხედვით იცვლება. ახლდება ყოველ საათს.",
  "fc_note_reg": "Open-Meteo-ს პროგნოზი. ამინდი ახლა — ზემოთ ვიჯეტში.",
  "sum_city_h": "{npg} კლიმატი: როდის დაგეგმოთ მოგზაურობა",
  "sum_city": "{np} სეზონების მიხედვით: ზამთარში დაახლოებით {w}° დღისით, გაზაფხულზე {sp}°, ზაფხულში {su}°, შემოდგომაზე {au}°. ყველაზე თბილი თვეა {warm} (დღისით {wt}°-მდე), ყველაზე გრილი — {cold} ({ct}°). ყველაზე მეტი ნალექი {wet}. დეტალური ნორმები თვეების მიხედვით — ქვემოთ ცხრილში.",
  "sum_reg_h": "{npg} კლიმატი: რით განსხვავდება ქალაქები",
  "sum_reg": "{npg} კლიმატი სიმაღლის მიხედვით იცვლება. ზაფხულში ყველაზე თბილია {wl} — დაახლოებით {ws}° დღისით, უფრო გრილი {cl} ({cs}°). ზამთარში {wl} — {wz}°, {cl} კი {cz}°. თითოეული ქალაქის პროგნოზი — ზემოთ ცხრილში, თვიური ნორმები — ქალაქების გვერდებზე.",
  "mon_h": "{npg} კლიმატი თვეების მიხედვით",
  "mon_p": "საშუალო ტემპერატურა დღისით და ღამით და ნალექიანი დღეების რაოდენობა. მწვანედ — ვიზიტისთვის ყველაზე კომფორტული თვეები.",
  "th_month": "თვე", "th_day": "დღისით", "th_night": "ღამით", "th_rain": "ნალექიანი დღეები",
  "mon_note": "ნორმები Open-Meteo-ს მონაცემებით (2014–2023 საშუალო). ცოცხალი პროგნოზი — ზემოთ ვიჯეტში.",
  "cmp_h": "{npg} კლიმატი: ქალაქების შედარება",
  "cmp_p": "საშუალო დღის ტემპერატურა სეზონების მიხედვით რეგიონის მთავარ წერტილებში — {npg} კლიმატი სიმაღლის მიხედვით საგრძნობლად იცვლება.{links}",
  "cmp_links": " დეტალური პროგნოზი ქალაქებით: {cities}.",
  "th_city": "ქალაქი", "th_best": "საუკეთესო დრო",
  "cmp_note": "დღისით, სეზონური საშუალო (Open-Meteo 2014–2023). თვიური მონაცემები — ქალაქების გვერდებზე.",
  "faq_when_q": "როდის ჯობია {np} ჩასვლა?",
  "faq_when_a": "ყველაზე კომფორტული დროა {best}: თბილა, მაგრამ დამქანცველი სიცხის გარეშე, და ნაკლები წვიმა. ზუსტი ციფრები თვეების მიხედვით — ზემოთ კლიმატის ცხრილში.",
  "faq_now_q": "როგორია ამინდი {np} ახლა?",
  "faq_now_a": "მიმდინარე ტემპერატურას და კვირის პროგნოზს აჩვენებს ცოცხალი ვიჯეტი გვერდის ზემოთ — მონაცემები ავტომატურად ახლდება.",
  "faq_wint_q": "ცივა {np} ზამთარში?",
  "zima_cold": "დიახ, ზამთარი ნამდვილია: იანვარში დღისით დაახლოებით {tx}°, ღამით {tn}°-მდე, თოვლი დევს. ეს მთისა და თხილამურების ზამთრის სეზონია.",
  "zima_mild": "ზამთარი რბილია: იანვარში დღისით დაახლოებით {tx}°, ღამით {tn}°. თოვლი მოდის, მაგრამ სწრაფად დნება.",
  "zima_warm": "ზამთარი თბილია: იანვარში დღისით დაახლოებით {tx}°, ღამით {tn}° — თოვლი თითქმის არ არის.",
  "title_city": "ამინდი — {np}: პროგნოზი და კლიმატი თვეებით",
  "desc_city": "ამინდი — {np}: პროგნოზი კვირით წინ დღეების მიხედვით და კლიმატი თვეებით — ტემპერატურა, ნალექი. საუკეთესო დროა: {best}.",
  "title_reg": "ამინდი — {np}: პროგნოზი და კლიმატი სეზონებით",
  "desc_reg": "ამინდი — {np}: დღიური პროგნოზი რეგიონის ქალაქებისთვის ({cnames}) და კლიმატი სეზონების მიხედვით. ადგილობრივი გიდის რჩევები.",
  "default_best": "გაზაფხული და შემოდგომა", "best_fallback": "მაისი და სექტემბერი",
  "pack": "ზაფხულში დღისით {su}°-მდე, ღამით დაახლოებით {sn}°: დღისით — მსუბუქი ტანსაცმელი, საღამოს გამოგადგებათ სვიტერი. ზამთარში დღისით {w}°, ღამით {wn}°-მდე — დაგჭირდებათ თბილი ქურთუკი{snow}.",
  "pack_snow": " და თოვლის ფეხსაცმელი", "pack_nosnow": "",
  "dry_line": "ყველაზე ცოტა წვიმა — {dry}: ყველაზე მოწმენდილი თვეებია სასეირნოდ და პანორამული ხედებისთვის.",
  "elev_line": " {name} მდებარეობს {em} მ სიმაღლეზე ზღვის დონიდან — საღამოები აქ შესამჩნევად უფრო გრილია, ვიდრე დაბლობზე.",
  "reg_spread": " ზაფხულში რეგიონის ქალაქებს შორის სხვაობა {diff}°-მდე აღწევს, ამიტომ თან იქონიეთ ტანსაცმელი როგორც თბილი ველებისთვის, ისე გრილი მთებისთვის.",
  "faq_pack_q": "რა წავიღოთ თან — {np}?",
  "act_h": "რით დაკავდეთ {np} სეზონების მიხედვით",
  "act_ski": "მთავარი სეზონი {np} — ზამთარი: დეკემბრიდან მარტამდე თოვლი დევს, დღისით დაახლოებით {w}°, მუშაობს საბაგიროები და ტრასები. ზაფხულში ({su}° დღისით) აქ ადიან სიგრილის, ალპური მდელოებისა და ლაშქრობის გამო. თარიღების შერჩევაში დაგეხმარებათ {tour}.",
  "act_beach": "სანაპირო სეზონი {np} — ივნისიდან სექტემბრამდე: დღისით დაახლოებით {su}°, ზღვა თბება, ცოცხლდება ბულვარი და კაფეები. გაზაფხულსა და შემოდგომაზე ({bt}) უფრო წყნარია — საბანაოდ გრილა, სამაგიეროდ მოსახერხებელია ღირსშესანიშნაობების დათვალიერება. ზღვის მარშრუტი — {tour}.",
  "act_wine": "წლის კულმინაცია {np} — რთველი სექტემბერსა და ოქტომბერში: ყურძნის კრეფა და დეგუსტაციები საოჯახო მარნებში, თბილი დღეები ზაფხულის სიცხის გარეშე. ზაფხულში ცხელა (დღისით {su}°-მდე), ზამთარში წყნარია ({w}°). დეგუსტაციების დაგეგმვაში დაგეხმარებათ {tour}.",
  "act_spa": "{np} ჩადიან მინერალური წყლისა და წიწვოვანი ჰაერისთვის მთელი წლის განმავლობაში. ზაფხულში ({su}° დღისით) სასიამოვნოა ტერენკურებზე სეირნობა, ზამთარში ({w}°) ნახევარ საათში მუშაობს სათხილამურო კურორტი. მოგზაურობის აწყობაში დაგეხმარებათ {tour}.",
  "act_alpine": "მთის სეზონი {np} — ივნისიდან სექტემბრამდე: დღისით დაახლოებით {su}°, ღიაა ბილიკები, უღელტეხილები და ხედები მყინვარებზე. ზამთარში ({w}° დღისით) გზები თოვლშია და მარშრუტების ნაწილი დაკეტილია. ყველაზე კომფორტულია {bt}. მთის მარშრუტი — {tour}.",
  "act_heritage": "{npg} უძველესი ძეგლების დათვალიერება მთელი წლის განმავლობაშია შესაძლებელი, მაგრამ ყველაზე კომფორტულია {bt}: ზაფხულში ღია მოედნებზე ცხელა (დღისით {su}°-მდე), ზამთარში ({w}°) ხალხი ცოტაა. ციხე-სიმაგრეებისა და ტაძრების დათვალიერებაში დაგეხმარებათ {tour}.",
  "act_canyon": "{npg} კანიონები და ჩანჩქერები ყველაზე წყალუხვია გაზაფხულსა და ზაფხულის დასაწყისში; ფირუზისფერ წყალში ბანაობა სასიამოვნოა ივლის-აგვისტოში ({su}° დღისით). ზამთარში ({w}°) ბილიკები მოლიპულია, ნაწილი დაკეტილია. საუკეთესო დროა {bt}. მარშრუტი — {tour}.",
  "act_city": "{np} ღიაა მთელი წელი: მუზეუმები, გოგირდის აბანოები და რესტორნები ყოველთვის მუშაობს. ყველაზე კომფორტულია {bt} — ზაფხულში დღისით {su}°-მდე და ქვაფენილი ხურდება, ზამთარში ({w}°) ხალხი ცოტაა. ძველ ქალაქში სეირნობა — {tour}.",
},
}


def sgn(x):
    return ("+" if x > 0 else "") + str(x)


def loc(p, lang):
    """Локализованные поля точки: name, prep, sub, guide, tour_title."""
    if lang == "ru":
        return {"name": p["name"], "prep": p["name_prep"], "sub": p["sub"],
                "guide": p["guide_text"], "tour_title": p["tour_title"]}
    t = I18N[p["slug"]][lang]
    return {"name": t["name"], "prep": t["prep"], "sub": t["sub"],
            "guide": t["guide"], "tour_title": t["tour_title"]}


def season_day(c, months):
    vals = [c[str(m)]["tmax"] for m in months if c.get(str(m)) and c[str(m)]["tmax"] is not None]
    return round(sum(vals) / len(vals)) if vals else None


def np_gen(prep, lang):
    """Родительный падеж названия для ka: prep = name+'ში' (локатив) → name+'ის'.
    Для ru/en возвращает исходную форму (шаблоны падежей не добавляют)."""
    return prep[:-2] + "ის" if lang == "ka" and prep.endswith("ში") else prep


MON_LOC_RU = ["", "январе", "феврале", "марте", "апреле", "мае", "июне", "июле",
              "августе", "сентябре", "октябре", "ноябре", "декабре"]
MON_LOC_KA = ["", "იანვარში", "თებერვალში", "მარტში", "აპრილში", "მაისში", "ივნისში",
              "ივლისში", "აგვისტოში", "სექტემბერში", "ოქტომბერში", "ნოემბერში", "დეკემბერში"]


def elev_m(p):
    """'450 м' -> 450; None если не число."""
    tok = str(p.get("elev", "")).split()
    return int(tok[0]) if tok and tok[0].lstrip("-").isdigit() else None


def season_night(c, months):
    vals = [c[str(m)]["tmin"] for m in months if c.get(str(m)) and c[str(m)]["tmin"] is not None]
    return round(sum(vals) / len(vals)) if vals else None


def dry_month_name(c, lang):
    valid = {m: c[str(m)] for m in range(1, 13) if c.get(str(m)) and c[str(m)]["tmax"] is not None}
    if not valid:
        return None
    m = min(valid, key=lambda m: valid[m]["rain"])
    if lang == "ru":
        return MON_LOC_RU[m]
    if lang == "ka":
        return MON_LOC_KA[m]
    return MON_NOM[lang][m]


def packing_line(p, lang):
    """Фактическая строка «что взять»: из летних/зимних дневных и ночных нормалей."""
    c = CLIM.get(p["slug"], {})
    if not c or not c.get("7"):
        return ""
    T = L[lang]
    su, sn = season_day(c, [6, 7, 8]), season_night(c, [6, 7, 8])
    w, wn = season_day(c, [12, 1, 2]), season_night(c, [12, 1, 2])
    if None in (su, sn, w, wn):
        return ""
    snow = T["pack_snow"] if w <= 3 else T["pack_nosnow"]
    return T["pack"].format(su=sgn(su), sn=sgn(sn), w=sgn(w), wn=sgn(wn), snow=snow)


def best_months(slug, lang, n=2):
    c = CLIM.get(slug, {}); sc = {}
    for m in range(1, 13):
        d = c.get(str(m))
        if not d or d["tmax"] is None:
            continue
        sc[m] = -abs(d["tmax"] - 24) - (5 if d["tmin"] < 6 else 0) - d["rain"] * 0.3
    return [MON_NOM[lang][m] for m in sorted(sc, key=sc.get, reverse=True)[:n]]


def climate_rows(slug, lang):
    c = CLIM.get(slug, {}); scores = {}
    for m in range(1, 13):
        d = c.get(str(m))
        if not d or d["tmax"] is None:
            continue
        scores[m] = -abs(d["tmax"] - 24) - (5 if d["tmin"] < 6 else 0) - d["rain"] * 0.3
    order = sorted(scores, key=scores.get, reverse=True)[:3]
    rows = []
    for m in range(1, 13):
        d = c.get(str(m))
        if not d or d["tmax"] is None:
            continue
        cls = ' class="best"' if m in order else ""
        rows.append(f'<tr><th scope="row"{cls}>{MON_NOM[lang][m]}</th>'
                    f'<td>{sgn(d["tmax"])}°</td><td>{sgn(d["tmin"])}°</td><td>{d["rain"]}</td></tr>')
    return "\n".join(rows), [MON_NOM[lang][m] for m in order]


def cmp_name(key, lang):
    if key in BY:
        return loc(BY[key], lang)["name"]
    return EXTRA_NAMES[lang].get(key, key)


def cmp_link(key, lang):
    if key in BY:
        return f'<a href="{PREFIX[lang]}/pogoda/{key}/">{cmp_name(key, lang)}</a>'
    return cmp_name(key, lang)


def climate_summary(p, lang):
    if p.get("cmp"):
        return region_summary(p, lang)
    c = CLIM.get(p["slug"], {})
    if not c or not c.get("7"):
        return ""
    T = L[lang]; np = loc(p, lang)["prep"]
    seas = {k: season_day(c, ms) for k, ms in SEASON_MONTHS}
    valid = {m: c[str(m)] for m in range(1, 13) if c.get(str(m)) and c[str(m)]["tmax"] is not None}
    warm = max(valid, key=lambda m: valid[m]["tmax"])
    cold = min(valid, key=lambda m: valid[m]["tmax"])
    wet = max(valid, key=lambda m: valid[m]["rain"])
    txt = T["sum_city"].format(
        np=np, w=sgn(seas["wint"]), sp=sgn(seas["spr"]), su=sgn(seas["sum"]), au=sgn(seas["aut"]),
        warm=MON_NOM[lang][warm].lower(), wt=sgn(valid[warm]["tmax"]),
        cold=MON_NOM[lang][cold].lower(), ct=sgn(valid[cold]["tmax"]),
        wet=(MON_LOC_RU[wet] if lang == "ru" else MON_LOC_KA[wet] if lang == "ka" else MON_GEN[lang][wet]))
    # Второй абзац: фактические блоки (сборы/сухие месяцы/высота) — данные из CLIM/GEO.
    extra = packing_line(p, lang)
    dry = dry_month_name(c, lang)
    if dry:
        extra += " " + T["dry_line"].format(dry=dry)
    em = elev_m(p)
    if em and em >= 900:
        extra += T["elev_line"].format(name=loc(p, lang)["name"], em=em)
    p2 = f"<p>{extra.strip()}</p>" if extra.strip() else ""
    return ('<section class="wx-sec wx-prose"><div class="wx-sec-head">'
            f'<h2>{T["sum_city_h"].format(np=np, npg=np_gen(np, lang))}</h2></div><p>{txt}</p>{p2}</section>')


def region_summary(p, lang):
    T = L[lang]; np = loc(p, lang)["prep"]
    pts = [(cmp_name(k, lang), CLIM.get(k, {})) for k in p["cmp"]]
    pts = [(nm, c) for nm, c in pts if c and c.get("7")]
    if len(pts) < 2:
        return ""
    warm = max(pts, key=lambda x: season_day(x[1], [6, 7, 8]))
    cold = min(pts, key=lambda x: season_day(x[1], [6, 7, 8]))
    ws_v, cs_v = season_day(warm[1], [6, 7, 8]), season_day(cold[1], [6, 7, 8])
    txt = T["sum_reg"].format(np=np, npg=np_gen(np, lang), wl=warm[0], ws=sgn(ws_v),
                              cl=cold[0], cs=sgn(cs_v),
                              wz=sgn(season_day(warm[1], [12, 1, 2])), cz=sgn(season_day(cold[1], [12, 1, 2])))
    diff = ws_v - cs_v
    if diff >= 3:
        txt += T["reg_spread"].format(diff=diff)
    return ('<section class="wx-sec wx-prose"><div class="wx-sec-head">'
            f'<h2>{T["sum_reg_h"].format(np=np, npg=np_gen(np, lang))}</h2></div><p>{txt}</p></section>')


# signature draw per region -> seasonal "what to do" paragraph (unique numbers + tour link)
ACT = {
    "gudauri": "ski", "bakuriani": "ski",
    "batumi": "beach", "adjara": "beach", "guria": "beach",
    "kakheti": "wine", "telavi": "wine", "signagi": "wine",
    "borjomi": "spa",
    "kazbegi": "alpine", "mestia": "alpine", "racha": "alpine",
    "mtskheta-mtianeti": "alpine", "samegrelo": "alpine",
    "mtskheta": "heritage", "shida-kartli": "heritage", "samtskhe-javakheti": "heritage",
    "imereti": "canyon", "kutaisi": "canyon", "kvemo-kartli": "canyon",
    "tbilisi": "city",
}


def activity_section(p, lang, best):
    key = ACT.get(p["slug"])
    if not key:
        return ""
    c = CLIM.get(p["slug"], {})
    if not c or not c.get("7"):
        return ""
    T = L[lang]; np = loc(p, lang)["prep"]
    su, w = season_day(c, [6, 7, 8]), season_day(c, [12, 1, 2])
    if su is None or w is None:
        return ""
    lp = loc(p, lang)
    tour = f'<a href="{tour_href(p, lang)}">{lp["tour_title"]}</a>'
    bt = ", ".join(best).lower() if best else T["default_best"]
    para = T["act_" + key].format(np=np, npg=np_gen(np, lang), su=sgn(su), w=sgn(w), bt=bt, tour=tour)
    return ('<section class="wx-sec wx-prose"><div class="wx-sec-head">'
            f'<h2>{T["act_h"].format(np=np, npg=np_gen(np, lang))}</h2></div><p>{para}</p></section>')


def monthly_section(p, lang):
    T = L[lang]; np = loc(p, lang)["prep"]
    rows, _ = climate_rows(p["slug"], lang)
    return ('<section class="wx-sec"><div class="wx-sec-head">'
            f'<h2>{T["mon_h"].format(np=np, npg=np_gen(np, lang))}</h2><p>{T["mon_p"]}</p></div>'
            '<div class="clim-wrap"><table class="clim"><thead><tr>'
            f'<th scope="col">{T["th_month"]}</th><th scope="col">{T["th_day"]}</th>'
            f'<th scope="col">{T["th_night"]}</th><th scope="col">{T["th_rain"]}</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>'
            f'<p class="clim-note">{T["mon_note"]}</p></section>')


def compare_section(p, lang):
    T = L[lang]; np = loc(p, lang)["prep"]; rows = []
    for key in p["cmp"]:
        c = CLIM.get(key, {})
        if not c:
            continue
        cells = "".join(f"<td>{sgn(season_day(c, ms))}°</td>" for _, ms in SEASON_MONTHS)
        bt = ", ".join(best_months(key, lang, 2)).lower()
        rows.append(f'<tr><th scope="row">{cmp_link(key, lang)}</th>{cells}<td>{bt}</td></tr>')
    head = "".join(f'<th scope="col">{SEASON_NAME[lang][k]}</th>' for k, _ in SEASON_MONTHS)
    city_links = [cmp_link(k, lang) for k in p["cmp"] if k in BY]
    links = T["cmp_links"].format(cities=" · ".join(city_links)) if city_links else ""
    return ('<section class="wx-sec"><div class="wx-sec-head">'
            f'<h2>{T["cmp_h"].format(np=np, npg=np_gen(np, lang))}</h2><p>{T["cmp_p"].format(np=np, npg=np_gen(np, lang), links=links)}</p></div>'
            '<div class="clim-wrap"><table class="clim"><thead><tr>'
            f'<th scope="col">{T["th_city"]}</th>{head}<th scope="col">{T["th_best"]}</th></tr></thead>'
            f'<tbody>{chr(10).join(rows)}</tbody></table></div>'
            f'<p class="clim-note">{T["cmp_note"]}</p></section>')


def neighbor_cards(p, lang):
    out = []
    for ns in p["neighbors"]:
        n = BY.get(ns)
        if not n:
            continue
        ln = loc(n, lang)
        out.append(
            f'<a class="wx-card load" data-region="{n["slug"]}" href="{PREFIX[lang]}/pogoda/{n["slug"]}/">'
            f'<div class="wx-card-top"><div><div class="wx-card-name">{ln["name"]}</div>'
            f'<div class="wx-card-sub">{ln["sub"]}</div></div><div class="wx-card-ic"></div></div>'
            f'<div class="wx-card-bot"><div class="wx-card-temp">--<sup>°</sup></div>'
            f'<div class="wx-card-mm">—</div></div></a>')
    return "\n".join(out)


def zima(p, lang):
    T = L[lang]; c = CLIM.get(p["slug"], {}); jan = c.get("1", {})
    tx, tn = jan.get("tmax"), jan.get("tmin")
    if tx is None:
        return T["zima_mild"].format(tx="0", tn="-5")
    key = "zima_cold" if tx <= 3 else "zima_mild" if tx <= 10 else "zima_warm"
    return T[key].format(tx=sgn(tx), tn=sgn(tn))


def faq_items(p, lang, best):
    T = L[lang]; np = loc(p, lang)["prep"]
    bt = ", ".join(best[:2]).lower() if best else T["best_fallback"]
    items = [
        (T["faq_when_q"].format(np=np), T["faq_when_a"].format(np=np, best=bt)),
        (T["faq_now_q"].format(np=np), T["faq_now_a"].format(np=np)),
        (T["faq_wint_q"].format(np=np), zima(p, lang)),
    ]
    pack = packing_line(p, lang)  # только города (у регионов нет единой CLIM)
    if pack and not p.get("cmp"):
        items.append((T["faq_pack_q"].format(np=np), pack))
    return items


def faq_html(qs):
    return "\n".join(
        f'<div class="fi"><button class="fq" onclick="toggleFaq(this)"><span>{q}</span>'
        f'<span class="fq-ic">+</span></button><div class="fa"><div class="fa-inner">{a}</div></div></div>'
        for q, a in qs)


def faq_ld(qs):
    ents = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ents}, ensure_ascii=False)


def tour_href(p, lang):
    """Ссылка на тур в нужном языке; фолбэк на языковой хаб экскурсий, если перевода тура нет."""
    tour = p["tour"]
    if lang == "ru":
        return f"/ekskursiya/{tour}/" if (ROOT / "ekskursiya" / tour).is_dir() else "/ekskursiya/"
    base = "en" if lang == "en" else "ge"
    if (ROOT / base / "ekskursiya" / tour).is_dir():
        return f"/{base}/ekskursiya/{tour}/"
    if (ROOT / base / tour).is_dir():
        return f"/{base}/{tour}/"
    return f"/{base}/ekskursiya/" if (ROOT / base / "ekskursiya").is_dir() else f"/{base}/"


def hreflang_block(slug):
    out = []
    for lg in LANGS:
        out.append(f'<link rel="alternate" hreflang="{HREF[lg]}" href="https://sakhva-travel.com{PREFIX[lg]}/pogoda/{slug}/">')
    out.append(f'<link rel="alternate" hreflang="x-default" href="https://sakhva-travel.com/pogoda/{slug}/">')
    return "\n".join(out)


def lang_switch(slug, lang):
    labels = {"ru": "RU", "en": "EN", "ka": "GE"}
    out = []
    for lg in LANGS:
        cls = " active" if lg == lang else ""
        out.append(f'<a class="ls{cls}" href="https://sakhva-travel.com{PREFIX[lg]}/pogoda/{slug}/">{labels[lg]}</a>')
    return "".join(out)


def render(p, lang):
    T = L[lang]; slug = p["slug"]; pfx = PREFIX[lang]
    lp = loc(p, lang)
    np = lp["prep"]
    rows, best = climate_rows(slug, lang)
    qs = faq_items(p, lang, best)
    parent = BY.get(p.get("region")) if p.get("region") else None
    best_txt = ", ".join(best).lower() if best else T["default_best"]

    # first-screen bridge to the tour catalogue (weather traffic -> booking)
    bridge = (f'<a class="wx-bridge" href="{tour_href(p, lang)}">'
              f'<span>{T["bridge"].format(np=np)}</span><span class="wx-bridge-arr">→</span></a>')
    if p.get("cmp"):
        mode = "region"
        cmp_js = json.dumps([{"slug": k, "name": cmp_name(k, lang),
                              "link": (f"{pfx}/pogoda/{k}/" if k in BY else None)} for k in p["cmp"]], ensure_ascii=False)
        cnames = ", ".join(cmp_name(k, lang) for k in p["cmp"])
        forecast = ('<section class="wx-sec"><div class="wx-sec-head">'
                    f'<h2>{T["fc_reg_h"].format(np=np)}</h2><p>{T["fc_reg_p"].format(np=np, npg=np_gen(np, lang))}</p></div>'
                    '<div id="multi" class="mc-wrap"></div>'
                    f'<p class="clim-note">{T["fc_note_reg"]}</p></section>')
        climate_section = (bridge + forecast + climate_summary(p, lang) + activity_section(p, lang, best)
                           + compare_section(p, lang) + monthly_section(p, lang))
        title = T["title_reg"].format(np=np)
        desc = T["desc_reg"].format(np=np, cnames=cnames)
    else:
        mode = "city"; cmp_js = "[]"
        forecast = ('<section class="wx-sec"><div class="wx-sec-head">'
                    f'<h2>{T["fc_city_h"].format(np=np)}</h2><p>{T["fc_city_p"]}</p></div>'
                    '<div id="cal" class="cal-grid"></div>'
                    f'<p class="clim-note">{T["fc_note_city"]}</p></section>')
        climate_section = bridge + forecast + climate_summary(p, lang) + activity_section(p, lang, best) + monthly_section(p, lang)
        title = T["title_city"].format(np=np)
        desc = T["desc_city"].format(np=np, best=best_txt)

    crumb_parent = (f'<a href="{pfx}/pogoda/{parent["slug"]}/">{loc(parent, lang)["name"]}</a><span>›</span>'
                    if parent else "")
    rel = []
    if parent:
        rel.append(f'<a href="{pfx}/pogoda/{parent["slug"]}/">{T["weather_in"].format(np=loc(parent, lang)["prep"])}</a>')
    for ns in p["neighbors"]:
        n = BY.get(ns)
        if n:
            rel.append(f'<a href="{pfx}/pogoda/{n["slug"]}/">{T["weather_in"].format(np=loc(n, lang)["prep"])}</a>')
    rel.append(f'<a href="{pfx}/pogoda/">{T["all_regions"]}</a>')
    rel_html = " · ".join(rel)

    ld_web = json.dumps({"@context": "https://schema.org", "@type": "WebPage",
        "url": f"https://sakhva-travel.com{pfx}/pogoda/{slug}/", "name": title.split(" | ")[0],
        "description": desc, "inLanguage": HREF[lang],
        "dateModified": __import__("datetime").date.today().isoformat(),
        "isPartOf": {"@id": "https://sakhva-travel.com/#website"}}, ensure_ascii=False)
    crumb_ld = [{"@type": "ListItem", "position": 1, "name": T["home"], "item": f"https://sakhva-travel.com{pfx}/"},
                {"@type": "ListItem", "position": 2, "name": T["weather_ge"], "item": f"https://sakhva-travel.com{pfx}/pogoda/"}]
    if parent:
        crumb_ld.append({"@type": "ListItem", "position": 3, "name": T["weather_in"].format(np=loc(parent, lang)["prep"]),
                         "item": f"https://sakhva-travel.com{pfx}/pogoda/{parent['slug']}/"})
    crumb_ld.append({"@type": "ListItem", "position": len(crumb_ld) + 1, "name": T["weather_in"].format(np=np),
                     "item": f"https://sakhva-travel.com{pfx}/pogoda/{slug}/"})
    ld_crumb = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumb_ld}, ensure_ascii=False)

    sub = {
        "LANG": HREF[lang], "PFX": pfx, "SLUG": slug, "TITLE": title, "DESC": desc,
        "CANONICAL": f"https://sakhva-travel.com{pfx}/pogoda/{slug}/",
        "HREFLANG": hreflang_block(slug), "LANGSWITCH": lang_switch(slug, lang),
        "OG_LOCALE": {"ru": "ru_RU", "en": "en_US", "ka": "ka_GE"}[lang],
        "OG_TITLE": T["weather_in"].format(np=np),
        "GE_FONT": GE_FONT_LINKS if lang == "ka" else "",
        "NAME": lp["name"], "H1": f'{T["h1_pre"]} <em>{lp["prep"]}</em>' if lang != "ka" else f'{T["h1_pre"]} <em>{lp["name"]}</em>',
        "LEDE": T["lede"].format(best=best_txt), "V": V,
        "ELEV_KICKER": (" · " + p["elev"]) if p.get("elev") else "",
        "KICKER": T["kicker"], "CRUMB_PARENT": crumb_parent, "GUIDE": lp["guide"],
        "CLIMATE_SECTION": climate_section, "MODE": mode, "CMP_JS": cmp_js,
        "NEIGHBORS": neighbor_cards(p, lang), "TOUR_HREF": tour_href(p, lang), "TOUR_TITLE": lp["tour_title"],
        "REL_HTML": rel_html, "FAQ": faq_html(qs), "FAQ_LD": faq_ld(qs), "LD_WEB": ld_web, "LD_CRUMB": ld_crumb,
        "WA_TEXT": T["wa_text"].format(np=np).replace(" ", "+"),
        # UI
        "T_NAV_TOURS": T["nav_tours"], "T_NAV_EXC": T["nav_exc"], "T_NAV_PRICES": T["nav_prices"],
        "T_NAV_ABOUT": T["nav_about"], "T_NAV_BLOG": T["nav_blog"], "T_NAV_WEATHER": T["nav_weather"],
        "T_NAV_CONTACTS": T["nav_contacts"], "T_NAV_PAY": T["nav_pay"], "T_WEATHER_GE": T["weather_ge"],
        "T_BOOK": T["book"], "T_HOME": T["home"], "T_FORECAST_WEEK": T["forecast_week"],
        "T_TODAY": T["today"], "T_LOADING": T["loading"], "T_UNAVAIL": T["unavail"], "T_NO_DATA": T["no_data"],
        "T_DAY_TO": T["day_to"], "T_NIGHT": T["night"], "T_UPDATED": T["updated"], "T_CTA_H": T["cta_h"], "T_CTA_P": T["cta_p"],
        "T_CTA_WA": T["cta_wa"], "T_NEAR_H": T["near_h"], "T_NEAR_P": T["near_p"], "T_FAQ_H": T["faq_h"],
        "T_PRIVACY": T["privacy"], "T_GUIDE": T["guide"],
        "NAV_TOURS_HREF": NAV_TOURS[lang], "PRIVACY_HREF": PRIVACY[lang],
        "CTA_H_GUIDE": T["guide_h"].format(np=np),
        "JS_DOW": json.dumps(DOW[lang], ensure_ascii=False),
        "JS_MONG": json.dumps(MON_GEN[lang], ensure_ascii=False),
        "JS_MONS": json.dumps(MON_SHORT[lang], ensure_ascii=False),
        "JS_WL": json.dumps(WLABELS[lang], ensure_ascii=False),
    }
    html = TEMPLATE
    for k, val in sub.items():
        html = html.replace("%%" + k + "%%", str(val))
    return html


TEMPLATE = open(Path(__file__).resolve().parent / "pogoda-template.html", encoding="utf-8").read()
HUB_TEMPLATE = open(Path(__file__).resolve().parent / "pogoda-hub-template.html", encoding="utf-8").read()

# Строки хаба «Погода в Грузии» (весь текст — статичный, Georgia-wide)
HUB = {
"ru": {
  "title": "Погода в Грузии по регионам и месяцам 2026 — когда ехать",
  "desc": "Погода в Грузии: прогноз на неделю и климат по месяцам для всех регионов и городов — Тбилиси, Батуми, Казбеги, Кахетия. Когда лучше ехать, советы гида.",
  "kicker": "Прогноз · климат · когда ехать", "h1_pre": "Погода в", "h1_em": "Грузии",
  "lede": "Актуальный прогноз и климат по месяцам для каждого региона: море Батуми, горы Казбеги, вино Кахетии. Планируйте поездку с местным гидом.",
  "featlink": "Погода в %NAME%: прогноз и климат по месяцам →",
  "regions_h": "Погода в регионах Грузии сейчас",
  "regions_p": "Нажмите на регион — прогноз на неделю, климат по месяцам и что смотреть в это время года.",
  "cities_h": "Погода в популярных городах и курортах",
  "cities_p": "Точечный прогноз и климат по месяцам для конкретных направлений.",
  "note": "Обновляется автоматически · источник Open-Meteo и национальные метеослужбы",
  "season_h": "Когда ехать в Грузию — по сезонам", "season_p": "Быстрая шпаргалка: что выбрать под погоду в каждый сезон.",
  "season_head": ["Направление", "Весна · III–V", "Лето · VI–VIII", "Осень · IX–XI", "Зима · XII–II"],
  "season_rows": [
    ("Тбилиси", [("Идеально: +15–24°C", 1), ("Жарко: +30–35°C", 0), ("Идеально: +15–25°C", 1), ("Мягко: +2–8°C", 0)]),
    ("Батуми · море", [("Прохладно, дожди", 0), ("Пляж: вода +24–26°C", 1), ("Бархат: до сентября", 1), ("Тепло, влажно: +8–12°C", 0)]),
    ("Кахетия · вино", [("Цветение, мало людей", 1), ("Жарко: +30–38°C", 0), ("Ртвели — сбор урожая", 1), ("Тихо: +2–8°C", 0)]),
    ("Казбеги · Сванети", [("Снег на перевалах", 0), ("Сезон: зелень, ясно", 1), ("Золотая осень, до октября", 1), ("Мороз, снег, виды", 0)]),
    ("Гудаури · Бакуриани", [("Конец сезона до апреля", 0), ("Зелёные горы, хайкинг", 0), ("Межсезонье", 0), ("Горнолыжный сезон", 1)]),
  ],
  "prose_h": "Как пользоваться прогнозом перед туром",
  "prose": "<p>Погода в Грузии сильно зависит от высоты: пока в Тбилиси +30°C, на Гергетской Троице у Казбеги может быть +8°C и ветер. Поэтому на страницах туров есть ссылка «Проверить погоду» — она ведёт на прогноз нужного региона.</p><p><strong>Совет от гида:</strong> для горных маршрутов (Казбеги, Сванети, Гудаури) смотрите прогноз за 1–2 дня. Если вершины закрыты облаками — дату лучше сдвинуть. Для тура в Казбеги мы переносим поездку бесплатно, если горы не открылись.</p>",
  "cta_h": "Не знаете, когда лучше приехать?",
  "cta_p": "Напишите Тимуру — подберём даты под погоду и составим маршрут. Ответ за 15 минут.",
  "wa_text": "Когда+лучше+приехать+в+Грузию", "tg_text": "Когда+лучше+в+Грузию",
  "faq_h": "Частые вопросы о погоде в Грузии",
  "faq": [
    ("Когда лучшая погода в Грузии?", "Универсально лучшие месяцы — май-июнь и сентябрь-октябрь: тепло, но не жарко, ясно, мало дождей. Летом (июль-август) жарко на равнине (+32–38°C), но это сезон моря в Батуми и гор в Казбеги. Зимой мягко в Тбилиси (+2–8°C) и снежно на курортах Гудаури и Бакуриани."),
    ("Где в Грузии теплее всего зимой?", "Зимой теплее всего на Черноморском побережье — в Батуми и Кобулети (+8–12°C), там субтропики. В Тбилиси мягко (+2–8°C). В горах (Казбеги, Гудаури, Местиа) — мороз и снег, это зона зимних видов спорта."),
    ("Когда ехать на море в Батуми?", "Пляжный сезон в Батуми — с июня по сентябрь. Вода прогревается до +24–26°C в июле-августе. Сентябрь — бархатный сезон: море ещё тёплое, а туристов и жары меньше."),
    ("Когда открыт сезон в горах Казбеги и Сванети?", "Летний сезон в высокогорье (Казбеги, Местиа, Ушгули) — с июня по октябрь: перевалы открыты, склоны зелёные, ясные виды на вершины. Зимой дороги через перевалы могут закрываться из-за снега — для тура в Казбеги предусмотрен бесплатный перенос при закрытых горах."),
  ],
},
"en": {
  "title": "Weather in Georgia by region and month 2026 — when to go",
  "desc": "Weather in Georgia: 7-day forecast and climate by month for every region and city — Tbilisi, Batumi, Kazbegi, Kakheti. When to visit, guide's tips.",
  "kicker": "Forecast · climate · when to go", "h1_pre": "Weather in", "h1_em": "Georgia",
  "lede": "Live forecast and monthly climate for every region: the Batumi seaside, the Kazbegi mountains, the wine of Kakheti. Plan your trip with a local guide.",
  "featlink": "Weather in %NAME%: forecast and climate by month →",
  "regions_h": "Weather in Georgia's regions right now",
  "regions_p": "Tap a region — 7-day forecast, climate by month and what to see this time of year.",
  "cities_h": "Weather in popular towns and resorts",
  "cities_p": "Pinpoint forecast and monthly climate for specific destinations.",
  "note": "Updated automatically · source Open-Meteo and national weather services",
  "season_h": "When to visit Georgia — by season", "season_p": "A quick cheat sheet: what to pick for the weather in each season.",
  "season_head": ["Destination", "Spring · III–V", "Summer · VI–VIII", "Autumn · IX–XI", "Winter · XII–II"],
  "season_rows": [
    ("Tbilisi", [("Ideal: +15–24°C", 1), ("Hot: +30–35°C", 0), ("Ideal: +15–25°C", 1), ("Mild: +2–8°C", 0)]),
    ("Batumi · sea", [("Cool, rainy", 0), ("Beach: sea +24–26°C", 1), ("Indian summer: to September", 1), ("Warm, humid: +8–12°C", 0)]),
    ("Kakheti · wine", [("Blossom, few crowds", 1), ("Hot: +30–38°C", 0), ("Rtveli — the grape harvest", 1), ("Quiet: +2–8°C", 0)]),
    ("Kazbegi · Svaneti", [("Snow on the passes", 0), ("Season: green, clear", 1), ("Golden autumn, to October", 1), ("Frost, snow, views", 0)]),
    ("Gudauri · Bakuriani", [("Season ends by April", 0), ("Green mountains, hiking", 0), ("Off-season", 0), ("Ski season", 1)]),
  ],
  "prose_h": "How to use the forecast before your tour",
  "prose": "<p>Weather in Georgia depends heavily on altitude: while it's +30°C in Tbilisi, at Gergeti Trinity near Kazbegi it can be +8°C and windy. That's why every tour page has a “Check the weather” link that leads to the forecast for that region.</p><p><strong>Guide's tip:</strong> for mountain routes (Kazbegi, Svaneti, Gudauri) check the forecast 1–2 days ahead. If the peaks are hidden in cloud, it's better to shift the date. For the Kazbegi tour we reschedule free of charge if the mountains stay closed.</p>",
  "cta_h": "Not sure when to come?",
  "cta_p": "Message Timur — we'll pick dates around the weather and plan your route. Reply within 15 minutes.",
  "wa_text": "When+is+the+best+time+to+visit+Georgia", "tg_text": "When+is+the+best+time+in+Georgia",
  "faq_h": "Frequently asked questions about the weather in Georgia",
  "faq": [
    ("When is the best weather in Georgia?", "The universally best months are May–June and September–October: warm but not hot, clear, with little rain. In summer (July–August) it's hot on the plains (+32–38°C), but that's the season for the Batumi seaside and the Kazbegi mountains. Winter is mild in Tbilisi (+2–8°C) and snowy at the Gudauri and Bakuriani resorts."),
    ("Where is it warmest in Georgia in winter?", "In winter it's warmest on the Black Sea coast — in Batumi and Kobuleti (+8–12°C), which are subtropical. Tbilisi is mild (+2–8°C). In the mountains (Kazbegi, Gudauri, Mestia) it's frost and snow — the zone for winter sports."),
    ("When to go to the sea in Batumi?", "The beach season in Batumi runs from June to September. The water warms to +24–26°C in July–August. September is the Indian summer: the sea is still warm, with fewer tourists and less heat."),
    ("When is the season open in the Kazbegi and Svaneti mountains?", "The summer season in the highlands (Kazbegi, Mestia, Ushguli) runs from June to October: the passes are open, the slopes green, the peak views clear. In winter the mountain-pass roads can close due to snow — the Kazbegi tour includes a free reschedule if the mountains are closed."),
  ],
},
"ka": {
  "title": "ამინდი საქართველოში რეგიონების მიხედვით 2026 — როდის",
  "desc": "ამინდი საქართველოში: კვირის პროგნოზი და კლიმატი თვეების მიხედვით ყველა რეგიონისა და ქალაქისთვის — თბილისი, ბათუმი, ყაზბეგი, კახეთი. როდის ჩახვიდეთ, გიდის რჩევები.",
  "kicker": "პროგნოზი · კლიმატი · როდის ჩახვიდეთ", "h1_pre": "ამინდი —", "h1_em": "საქართველო",
  "lede": "მიმდინარე პროგნოზი და კლიმატი თვეების მიხედვით თითოეული რეგიონისთვის: ბათუმის ზღვა, ყაზბეგის მთები, კახეთის ღვინო. დაგეგმეთ მოგზაურობა ადგილობრივ გიდთან.",
  "featlink": "ამინდი — %NAME%: პროგნოზი და კლიმატი თვეებით →",
  "regions_h": "ამინდი საქართველოს რეგიონებში ახლა",
  "regions_p": "დააჭირეთ რეგიონს — კვირის პროგნოზი, კლიმატი თვეებით და რა ვნახოთ ამ სეზონზე.",
  "cities_h": "ამინდი პოპულარულ ქალაქებსა და კურორტებზე",
  "cities_p": "ზუსტი პროგნოზი და კლიმატი თვეებით კონკრეტული მიმართულებებისთვის.",
  "note": "ახლდება ავტომატურად · წყარო Open-Meteo და ეროვნული მეტეოსამსახურები",
  "season_h": "როდის ჩახვიდეთ საქართველოში — სეზონების მიხედვით", "season_p": "სწრაფი მემორანდუმი: რა ავირჩიოთ ამინდის მიხედვით თითოეულ სეზონზე.",
  "season_head": ["მიმართულება", "გაზაფხული · III–V", "ზაფხული · VI–VIII", "შემოდგომა · IX–XI", "ზამთარი · XII–II"],
  "season_rows": [
    ("თბილისი", [("იდეალური: +15–24°C", 1), ("ცხელა: +30–35°C", 0), ("იდეალური: +15–25°C", 1), ("რბილი: +2–8°C", 0)]),
    ("ბათუმი · ზღვა", [("გრილი, წვიმიანი", 0), ("პლაჟი: წყალი +24–26°C", 1), ("ხავერდის სეზონი: სექტემბრამდე", 1), ("თბილი, ნოტიო: +8–12°C", 0)]),
    ("კახეთი · ღვინო", [("ყვავილობა, ცოტა ხალხი", 1), ("ცხელა: +30–38°C", 0), ("რთველი — მოსავალი", 1), ("მშვიდი: +2–8°C", 0)]),
    ("ყაზბეგი · სვანეთი", [("თოვლი უღელტეხილებზე", 0), ("სეზონი: მწვანე, მოწმენდილი", 1), ("ოქროს შემოდგომა, ოქტომბრამდე", 1), ("ყინვა, თოვლი, ხედები", 0)]),
    ("გუდაური · ბაკურიანი", [("სეზონი მთავრდება აპრილისთვის", 0), ("მწვანე მთები, ლაშქრობა", 0), ("შუალედური სეზონი", 0), ("სათხილამურო სეზონი", 1)]),
  ],
  "prose_h": "როგორ გამოვიყენოთ პროგნოზი ტურამდე",
  "prose": "<p>ამინდი საქართველოში დიდად არის დამოკიდებული სიმაღლეზე: სანამ თბილისში +30°C-ია, ყაზბეგთან გერგეტის სამებაზე შეიძლება იყოს +8°C და ქარი. ამიტომ ტურის გვერდებზე არის ბმული „ამინდის შემოწმება“ — ის მიგიყვანთ საჭირო რეგიონის პროგნოზზე.</p><p><strong>გიდის რჩევა:</strong> მთის მარშრუტებისთვის (ყაზბეგი, სვანეთი, გუდაური) ნახეთ პროგნოზი 1–2 დღით ადრე. თუ მწვერვალები ღრუბლებშია — თარიღი სჯობს გადაიწიოს. ყაზბეგის ტურს უფასოდ ვანაცვლებთ, თუ მთები არ გაიხსნა.</p>",
  "cta_h": "არ იცით, როდის ჩამოხვიდეთ?",
  "cta_p": "მისწერეთ თიმურს — შევარჩევთ თარიღებს ამინდის მიხედვით და შევადგენთ მარშრუტს. პასუხი 15 წუთში.",
  "wa_text": "როდის+ჯობია+საქართველოში+ჩამოსვლა", "tg_text": "როდის+ჯობია+საქართველოში",
  "faq_h": "ხშირად დასმული კითხვები ამინდზე საქართველოში",
  "faq": [
    ("როდის არის საუკეთესო ამინდი საქართველოში?", "საყოველთაოდ საუკეთესო თვეებია მაისი-ივნისი და სექტემბერი-ოქტომბერი: თბილა, მაგრამ არა ცხელა, მოწმენდილი, ცოტა წვიმა. ზაფხულში (ივლისი-აგვისტო) ცხელა დაბლობზე (+32–38°C), მაგრამ ეს ბათუმის ზღვისა და ყაზბეგის მთების სეზონია. ზამთარში რბილია თბილისში (+2–8°C) და თოვლიანი გუდაურისა და ბაკურიანის კურორტებზე."),
    ("სად არის ყველაზე თბილი საქართველოში ზამთარში?", "ზამთარში ყველაზე თბილია შავი ზღვის სანაპიროზე — ბათუმსა და ქობულეთში (+8–12°C), იქ სუბტროპიკებია. თბილისში რბილია (+2–8°C). მთებში (ყაზბეგი, გუდაური, მესტია) — ყინვა და თოვლი, ეს ზამთრის სპორტის ზონაა."),
    ("როდის წავიდეთ ზღვაზე ბათუმში?", "პლაჟის სეზონი ბათუმში — ივნისიდან სექტემბრამდე. წყალი თბება +24–26°C-მდე ივლის-აგვისტოში. სექტემბერი ხავერდის სეზონია: ზღვა ჯერ თბილია, ტურისტი და სიცხე კი ნაკლები."),
    ("როდის იხსნება სეზონი ყაზბეგისა და სვანეთის მთებში?", "ზაფხულის სეზონი მაღალმთიანეთში (ყაზბეგი, მესტია, უშგული) — ივნისიდან ოქტომბრამდე: უღელტეხილები ღიაა, ფერდობები მწვანე, ხედები მწვერვალებზე მოწმენდილი. ზამთარში უღელტეხილების გზები შეიძლება დაიხუროს თოვლის გამო — ყაზბეგის ტური მოიცავს უფასო გადანაცვლებას, თუ მთები დახურულია."),
  ],
},
}


def hub_cards(lang, ptype):
    out = []
    for p in GEO:
        if p["type"] != ptype:
            continue
        lp = loc(p, lang)
        out.append(
            f'<a class="wx-card load" data-region="{p["slug"]}" data-name="{lp["name"]}" '
            f'href="{PREFIX[lang]}/pogoda/{p["slug"]}/"><div class="wx-card-top"><div>'
            f'<div class="wx-card-name">{lp["name"]}</div><div class="wx-card-sub">{lp["sub"]}</div></div>'
            f'<div class="wx-card-ic"></div></div><div class="wx-card-bot">'
            f'<div class="wx-card-temp">--<sup>°</sup></div><div class="wx-card-mm">—</div></div></a>')
    return "\n".join(out)


def season_table(lang):
    h = HUB[lang]
    head = "".join(f"<th>{x}</th>" for x in h["season_head"])
    rows = []
    for place, cells in h["season_rows"]:
        tds = "".join(f'<td class="best">{t}</td>' if b else f"<td>{t}</td>" for t, b in cells)
        rows.append(f'<tr><th>{place}</th>{tds}</tr>')
    return (f'<table class="season-table"><thead><tr>{head}</tr></thead>'
            f'<tbody>{chr(10).join(rows)}</tbody></table>')


def render_hub(lang):
    h = HUB[lang]; T = L[lang]; pfx = PREFIX[lang]
    tb = loc(BY["tbilisi"], lang)["name"]
    qs = h["faq"]
    ld_web = json.dumps({"@context": "https://schema.org", "@type": "WebPage",
        "url": f"https://sakhva-travel.com{pfx}/pogoda/", "name": h["title"].split(" | ")[0],
        "description": h["desc"], "inLanguage": HREF[lang],
        "isPartOf": {"@id": "https://sakhva-travel.com/#website"}}, ensure_ascii=False)
    ld_crumb = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": T["home"], "item": f"https://sakhva-travel.com{pfx}/"},
        {"@type": "ListItem", "position": 2, "name": T["weather_ge"], "item": f"https://sakhva-travel.com{pfx}/pogoda/"}]}, ensure_ascii=False)
    faq_ld_s = faq_ld(qs)
    hreflang = "\n".join(
        [f'<link rel="alternate" hreflang="{HREF[lg]}" href="https://sakhva-travel.com{PREFIX[lg]}/pogoda/">' for lg in LANGS]
        + ['<link rel="alternate" hreflang="x-default" href="https://sakhva-travel.com/pogoda/">'])
    _lbl = {"ru": "RU", "en": "EN", "ka": "GE"}
    langsw = "".join(
        f'<a class="ls{" active" if lg == lang else ""}" '
        f'href="https://sakhva-travel.com{PREFIX[lg]}/pogoda/">{_lbl[lg]}</a>' for lg in LANGS)
    sub = {
        "LANG": HREF[lang], "PFX": pfx, "TITLE": h["title"], "DESC": h["desc"],
        "CANONICAL": f"https://sakhva-travel.com{pfx}/pogoda/", "HREFLANG": hreflang,
        "OG_LOCALE": {"ru": "ru_RU", "en": "en_US", "ka": "ka_GE"}[lang], "OG_TITLE": h["title"].split(" | ")[0],
        "GE_FONT": GE_FONT_LINKS if lang == "ka" else "",
        "LANGSWITCH": langsw, "NAV_TOURS_HREF": NAV_TOURS[lang], "PRIVACY_HREF": PRIVACY[lang],
        "KICKER": h["kicker"], "H1": f'{h["h1_pre"]} <em>{h["h1_em"]}</em>', "LEDE": h["lede"],
        "FEAT_NAME": tb, "FEAT_LINK": f'{pfx}/pogoda/tbilisi/', "JS_FEATLINK": h["featlink"],
        "REGIONS_H": h["regions_h"], "REGIONS_P": h["regions_p"], "REGION_CARDS": hub_cards(lang, "region"),
        "CITIES_H": h["cities_h"], "CITIES_P": h["cities_p"], "CITY_CARDS": hub_cards(lang, "city"),
        "NOTE": h["note"], "SEASON_H": h["season_h"], "SEASON_P": h["season_p"], "SEASON_TABLE": season_table(lang),
        "PROSE_H": h["prose_h"], "PROSE": h["prose"], "CTA_H": h["cta_h"], "CTA_P": h["cta_p"],
        "WA_TEXT": h["wa_text"], "TG_TEXT": h["tg_text"], "FAQ_H": h["faq_h"], "FAQ": faq_html(qs),
        "LD_WEB": ld_web, "LD_CRUMB": ld_crumb, "FAQ_LD": faq_ld_s,
        "T_NAV_TOURS": T["nav_tours"], "T_NAV_EXC": T["nav_exc"], "T_NAV_PRICES": T["nav_prices"],
        "T_NAV_ABOUT": T["nav_about"], "T_NAV_BLOG": T["nav_blog"], "T_NAV_WEATHER": T["nav_weather"],
        "T_NAV_CONTACTS": T["nav_contacts"], "T_NAV_PAY": T["nav_pay"], "T_WEATHER_GE": T["weather_ge"],
        "T_BOOK": T["book"], "T_HOME": T["home"], "T_FORECAST_WEEK": T["forecast_week"],
        "T_TODAY": T["today"], "T_LOADING": T["loading"], "T_UNAVAIL": T["unavail"],
        "T_DAY_TO": T["day_to"], "T_NIGHT": T["night"], "T_UPDATED": T["updated"], "T_PRIVACY": T["privacy"], "T_GUIDE": T["guide"],
        "JS_DOW": json.dumps(DOW[lang], ensure_ascii=False),
        "JS_MONG": json.dumps(MON_GEN[lang], ensure_ascii=False),
        "JS_WL": json.dumps(WLABELS[lang], ensure_ascii=False),
    }
    html = HUB_TEMPLATE
    for k, val in sub.items():
        html = html.replace("%%" + k + "%%", str(val))
    return html


LASTMOD = "2026-09-07"


def gen_sitemap():
    """sitemap-pogoda.xml: хаб + 21 спица × 3 языка, с hreflang-альтернативами."""
    slugs = [""] + [p["slug"] for p in GEO]
    alts = lambda s: "".join(
        f'\n    <xhtml:link rel="alternate" hreflang="{HREF[lg]}" '
        f'href="https://sakhva-travel.com{PREFIX[lg]}/pogoda/{s + "/" if s else ""}"/>'
        for lg in LANGS) + (
        f'\n    <xhtml:link rel="alternate" hreflang="x-default" '
        f'href="https://sakhva-travel.com/pogoda/{s + "/" if s else ""}"/>')
    urls = []
    for lang in LANGS:
        for s in slugs:
            loc = f"https://sakhva-travel.com{PREFIX[lang]}/pogoda/{s + '/' if s else ''}"
            urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{LASTMOD}</lastmod>{alts(s)}\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")


def main():
    only = None; langs = LANGS
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    if "--lang" in sys.argv:
        langs = sys.argv[sys.argv.index("--lang") + 1].split(",")
    n = 0
    for lang in langs:
        for p in GEO:
            if only and p["slug"] != only:
                continue
            out = ROOT / OUTDIR[lang] / p["slug"] / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(render(p, lang), encoding="utf-8")
            n += 1
        if not only:
            hub = ROOT / OUTDIR[lang] / "index.html"
            hub.write_text(render_hub(lang), encoding="utf-8")
            n += 1
        print(f"+ {lang}: {OUTDIR[lang]}/")
    if not only:
        (ROOT / "sitemap-pogoda.xml").write_text(gen_sitemap(), encoding="utf-8")
        print("+ sitemap-pogoda.xml")
    print(f"Готово: {n} страниц ({', '.join(langs)})")


if __name__ == "__main__":
    main()
