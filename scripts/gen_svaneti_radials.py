# -*- coding: utf-8 -*-
"""Генератор 4 радиальных экскурсий из Местии (Сванетия) на 3 языках: ru/en/ka.
Каркас (style/nav/footer/reviews/modal) берётся ДОСЛОВНО из языковых svaneti-шаблонов,
уникальным делается переведённый контент каждого тура. Полный hreflang-mesh ru<->en<->ka.
Запуск: python3 scripts/gen_svaneti_radials.py
"""
import re, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://sakhva-travel.com"
MAPKEY = "AIzaSyB8lmxnn0XEUQKhPIJZsDw8MRuKURD2RXQ"
WA = "995511272623"
# путь-префикс языка и код hreflang
LANGS = {"ru": ("", "ru"), "en": ("/en", "en"), "ka": ("/ge", "ka")}
TPL_PATH = {
    "ru": "ekskursiya/ekskursiya-svaneti-iz-tbilisi/index.html",
    "en": "en/ekskursiya/ekskursiya-svaneti-iz-tbilisi/index.html",
    "ka": "ge/ekskursiya/ekskursiya-svaneti-iz-tbilisi/index.html",
}

def _j(s): return json.dumps(s, ensure_ascii=False)

def grab(txt, pattern):
    m = re.search(pattern, txt, re.DOTALL)
    if not m: raise SystemExit("не найден блок: " + pattern[:50])
    return m.group(0)

# --- извлекаем языковые каркасы ---
FRAME = {}
for lg, path in TPL_PATH.items():
    T = (ROOT / path).read_text(encoding="utf-8")
    FRAME[lg] = dict(
        STYLE=grab(T, r"<style>.*?</style>"),
        NAV=grab(T, r"<nav id=\"nav\">.*?</nav>"),
        DRAWER=grab(T, r"<div class=\"drawer\" id=\"drawer\">.*?</a>\s*</div>"),
        REVIEWS=grab(T, r"<section id=\"reviews\".*?</section>"),
        FOOTER=grab(T, r"<footer id=\"footer\">.*?</footer>"),
        TAIL=grab(T, r"<script>\nconst burger.*?</body>"),
    )

# фикс видимости шапки: тень текста на светлом верху hero + активатор .scrolled (штатный, как на главной)
NAVFIX_CSS = ('<style>'
  '#nav:not(.scrolled) .nav-logo,#nav:not(.scrolled) .nav-links a,#nav:not(.scrolled) .nav-btn,'
  '#nav:not(.scrolled) .lang-btn,#nav:not(.scrolled) .lang-sep,#nav:not(.scrolled) .burger span'
  '{text-shadow:0 1px 6px rgba(0,0,0,.55)}'
  '.page-hero::after{background:linear-gradient(180deg,rgba(0,0,0,.5) 0%,rgba(0,0,0,.18) 22%,rgba(0,0,0,.34) 100%)!important}'
  '</style>')
NAVFIX_JS = ('<script>(function(){var n=document.getElementById("nav");if(!n)return;'
  'function u(){n.classList.toggle("scrolled",(window.scrollY||window.pageYOffset||0)>60)}'
  'u();window.addEventListener("scroll",u,{passive:true})})();</script>')

WA_SVG = ('<svg fill="currentColor" height="18" viewbox="0 0 24 24" width="18">'
    '<path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"></path></svg>')

# --- UI-строки интерфейса по языкам ---
L = {
 "ru": dict(
    price_from="от", lari="лари",
    per_car_note="Цена за машину, а не за человека — выгодно для компании",
    lbl_dur="Длительность", lbl_group="Группа", lbl_start="Старт", lbl_cancel="Отмена",
    from_mestia="из Местии", people="чел", cancel24="за 24 ч",
    book_from="Забронировать от {p} лари", discount="Скидка 10% — оставить заявку",
    rating="★ 4.8/5 · ответ за 15 мин", book_online="Забронировать онлайн",
    short="Коротко:", route_label="Маршрут", route_title="Программа экскурсии по часам",
    route_prefix="Маршрут:", faq_title="Часто задаваемые вопросы", tip_title="Совет от Тимура",
    map_open="Открыть маршрут в Google Maps",
    author_creds="Гид по Сванетии · родом из Местии · 10 лет по региону · 4.9/5",
    ready_q="Готовы забронировать?",
    ready_p="Саба — лицензированный гид по Сванетии (лиц. №9332412411), родом из Местии, 10 лет по региону. Джип-туры из Местии, группы до 6 человек, гибкий график под ваш день в Сванетии.",
    more_about="Подробнее о гиде Сабе →",
    cta_h="Готовы к приключению?", cta_p="Саба · Sakhva Travel · гид по Сванетии · рейтинг 4.9",
    others="Другие экскурсии из Местии и Сванетии:", all_exc="← Все экскурсии",
    parent_link='Едете в Сванетию из Тбилиси? Смотрите <a href="{u}" style="color:#1A3D2E;font-weight:600">многодневную экскурсию в Сванетию →</a> — эти радиалки из Местии входят в программу как дни на выбор.',
    short_tpl="{h1} — {dur} ({dh}), {pf} ₾{p} {unit}, старт из Местии, русскоязычный гид Sakhva Travel. Прямое бронирование без комиссии агрегаторов.",
    parent_slug="ekskursiya-svaneti-iz-tbilisi", exc_dir="/ekskursiya/",
 ),
 "en": dict(
    price_from="from", lari="GEL",
    per_car_note="Price is per vehicle, not per person — great value for a group",
    lbl_dur="Duration", lbl_group="Group", lbl_start="Start", lbl_cancel="Cancellation",
    from_mestia="from Mestia", people="pax", cancel24="24 h free",
    book_from="Book from ₾{p}", discount="Get 10% off — leave a request",
    rating="★ 4.8/5 · reply in 15 min", book_online="Book online",
    short="In short:", route_label="Route", route_title="Hour-by-hour itinerary",
    route_prefix="Route:", faq_title="Frequently asked questions", tip_title="Timur's tip",
    map_open="Open the route in Google Maps",
    author_creds="Svaneti guide · Mestia native · 10 years in the region · 4.9/5",
    ready_q="Ready to book?",
    ready_p="Saba is a licensed Svaneti guide (lic. #9332412411), a Mestia native with 10 years in the region. Jeep tours from Mestia, groups up to 6, a flexible schedule for your day in Svaneti.",
    more_about="More about guide Saba →",
    cta_h="Ready for the adventure?", cta_p="Saba · Sakhva Travel · Svaneti guide · rated 4.9",
    others="Other tours from Mestia and Svaneti:", all_exc="← All tours",
    parent_link='Coming to Svaneti from Tbilisi? See the <a href="{u}" style="color:#1A3D2E;font-weight:600">multi-day Svaneti tour →</a> — these day trips from Mestia are included as optional days.',
    short_tpl="{h1} — {dur} ({dh}), {pf} ₾{p} {unit}, starts in Mestia, English-speaking Sakhva Travel guide. Direct booking with no aggregator fees.",
    parent_slug="ekskursiya-svaneti-iz-tbilisi", exc_dir="/en/ekskursiya/",
 ),
 "ka": dict(
    price_from="დან", lari="ლარი",
    per_car_note="ფასი მანქანაზეა და არა ერთ ადამიანზე — მომგებიანია ჯგუფისთვის",
    lbl_dur="ხანგრძლივობა", lbl_group="ჯგუფი", lbl_start="დაწყება", lbl_cancel="გაუქმება",
    from_mestia="მესტიიდან", people="კაცი", cancel24="24 სთ",
    book_from="დაჯავშნა {p} ლარიდან", discount="10% ფასდაკლება — დატოვეთ განაცხადი",
    rating="★ 4.8/5 · პასუხი 15 წუთში", book_online="ონლაინ დაჯავშნა",
    short="მოკლედ:", route_label="მარშრუტი", route_title="მარშრუტი საათობრივად",
    route_prefix="მარშრუტი:", faq_title="ხშირად დასმული კითხვები", tip_title="თიმურის რჩევა",
    map_open="მარშრუტის გახსნა Google Maps-ში",
    author_creds="სვანეთის გიდი · მესტიელი · 10 წელი რეგიონში · 4.9/5",
    ready_q="მზად ხართ დასაჯავშნად?",
    ready_p="საბა ლიცენზირებული სვანეთის გიდია (ლიც. №9332412411), მესტიელი, 10 წელი რეგიონში. ჯიპ-ტურები მესტიიდან, ჯგუფი 6 კაცამდე, მოქნილი გრაფიკი თქვენი დღისთვის სვანეთში.",
    more_about="მეტი გიდ საბაზე →",
    cta_h="მზად ხართ თავგადასავლისთვის?", cta_p="საბა · Sakhva Travel · სვანეთის გიდი · რეიტინგი 4.9",
    others="სხვა ტურები მესტიიდან და სვანეთიდან:", all_exc="← ყველა ტური",
    parent_link='მოდიხართ სვანეთში თბილისიდან? იხილეთ <a href="{u}" style="color:#1A3D2E;font-weight:600">მრავალდღიანი ტური სვანეთში →</a> — ეს ერთდღიანი მარშრუტები მესტიიდან შედის პროგრამაში არჩევით დღეებად.',
    short_tpl="{h1} — {dur} ({dh}), {pf} ₾{p} {unit}, დაწყება მესტიიდან, Sakhva Travel-ის გიდი. პირდაპირი დაჯავშნა აგრეგატორების საკომისიოს გარეშე.",
    parent_slug="ekskursiya-svaneti-iz-tbilisi", exc_dir="/ge/ekskursiya/",
 ),
}

# короткие названия для взаимных перелинковок (per lang)
LINK_TITLES = {
 "ru": {"lednik-chalaadi-mestia":"Ледник Чалаади","ushguli-iz-mestii":"Ушгули из Местии",
        "ushguli-shkhara-lednik":"Ушгули и ледник Шхара","ozero-koruldi-mestia":"Озёра Корульди",
        "_svaneti":"Сванетия из Тбилиси","_svaneti4":"Тур в Сванетию 4 дня"},
 "en": {"lednik-chalaadi-mestia":"Chalaadi Glacier","ushguli-iz-mestii":"Ushguli from Mestia",
        "ushguli-shkhara-lednik":"Ushguli & Shkhara Glacier","ozero-koruldi-mestia":"Koruldi Lakes",
        "_svaneti":"Svaneti from Tbilisi","_svaneti4":"Svaneti 4-day tour"},
 "ka": {"lednik-chalaadi-mestia":"ჭალაადის მყინვარი","ushguli-iz-mestii":"უშგული მესტიიდან",
        "ushguli-shkhara-lednik":"უშგული და შხარას მყინვარი","ozero-koruldi-mestia":"კორულდის ტბები",
        "_svaneti":"სვანეთი თბილისიდან","_svaneti4":"სვანეთის 4-დღიანი ტური"},
}

# ============ ДАННЫЕ ТУРОВ ============
# общие (нейтральные) поля + i18n тексты по языкам
TOURS = [
 dict(slug="lednik-chalaadi-mestia", price="400", img="chalaadi-tour-600",
   stops=[("Mestia",43.045,42.729),("Chalaadi bridge",43.075,42.746),("Chalaadi Glacier",43.105,42.758)],
   route_times=["09:00","09:40","10:00","11:30","12:30","13:30"],
   i18n=dict(
     ru=dict(
       h1="Экскурсия к леднику Чалаади из Местии",
       title="Экскурсия к леднику Чалаади из Местии — от ₾400 за джип",
       desc="Ледник Чалаади из Местии за полдня: джип до моста, 2 часа пешком по лесу к языку ледника. От ₾400 за джип до 6 человек, гид, 3.5–4 часа.",
       price_unit="за джип до 6 чел", dur="полдня", dur_hours="3.5–4 ч",
       stats=[("от ₾400","за джип"),("полдня","3.5–4 ч"),("до 6","человек"),("30 мин","джип до старта"),("лёгкий","уровень")],
       route=[("Выезд из Местии","Джип 4×4, 8 км грунтовки вдоль Местиачалы, ~30 минут."),
              ("Мост через Местиачалу","Старт пешего маршрута, инструктаж гида."),
              ("Хвойный лес вдоль реки","Пологий подъём ~1.5 ч, набор высоты около 300 м."),
              ("Язык ледника Чалаади","Голубой лёд у самой тропы, фото, отдых 30 минут."),
              ("Спуск к мосту","Обратно той же тропой, легче и быстрее."),
              ("Возвращение в Местию","Джип назад в центр Местии.")],
       map_line="Местия → мост Местиачала → ледник Чалаади",
       body=[("Чалаади — самый доступный ледник Сванетии","Ледник Чалаади спускается с массива Ушбы и заканчивается всего в часе ходьбы от Местии. Это делает его самой лёгкой ледниковой тропой региона: сюда идут семьи с детьми, новички без опыта треккинга и все, у кого есть только полдня. Язык ледника лежит на высоте около 2000 метров, и подойти к голубому льду можно вплотную."),
             ("Как проходит маршрут","Первые 8 километров от Местии до моста через реку Местиачалу мы проезжаем на внедорожнике — грунтовку разбивает талой водой, обычная машина не пройдёт. От моста начинается пеший участок: тропа идёт через густой хвойный лес вдоль ледниковой реки, набор высоты плавный. Через полтора часа лес расступается, и перед вами открывается серо-голубая стена льда."),
             ("Для кого подходит","Маршрут относят к лёгкому-среднему уровню. Специальной подготовки не нужно — достаточно удобной обуви с протектором и куртки: у ледника даже летом заметно холоднее, чем в Местии. Дети от 8 лет проходят тропу спокойно. Общее время на земле — 3.5–4 часа, поэтому Чалаади легко совместить с обедом в Местии и второй активностью в тот же день — например, с джип-подъёмом к <a href=\"../ozero-koruldi-mestia/\">озёрам Корульди</a>.")],
       faq=[("Сколько длится экскурсия к леднику Чалаади?","Полдня — 3.5–4 часа от выезда до возвращения в Местию. Из них около 30 минут занимает джип до моста, а сам пеший маршрут туда-обратно — примерно 3 часа в спокойном темпе с остановками на фото."),
            ("Насколько сложная тропа и нужна ли подготовка?","Тропа лёгкая-средняя: пологий подъём по лесу с набором высоты около 300 метров. Специальная физическая подготовка не нужна, маршрут проходят дети от 8 лет и люди без опыта треккинга. Нужна удобная обувь с протектором и тёплая куртка."),
            ("Что входит в цену ₾400?","Цена ₾400 — за джип до 6 человек: внедорожник с водителем до моста и обратно и русскоязычный гид на маршруте. То есть на компанию из 4–6 человек выходит совсем недорого. Обед и личные расходы оплачиваются отдельно."),
            ("Можно ли дойти до Чалаади пешком без джипа?","Да, можно идти пешком прямо из Местии, но тогда прибавляется около 8 км грунтовки в одну сторону и день становится полным. Джип экономит 2–3 часа и силы для самой красивой, лесной части маршрута."),
            ("В какое время года доступен ледник?","С мая по октябрь. Летом тропа сухая и комфортная, в межсезонье возможны снежники на подходе. Зимой маршрут закрыт из-за лавинной опасности — в это время предлагаем другие зимние активности Сванетии.")],
       tip="Выходите к Чалаади в первой половине дня: после обеда с ледника нередко натягивает облака и тянет холодный ветер по долине реки. Возьмите перекус — у языка ледника хочется задержаться дольше, чем кажется на старте. И не подходите к самому льду вплотную снизу: ледник живой, с него срываются камни и куски льда, безопасная точка для фото — сбоку, её покажет гид.",
     ),
     en=dict(
       h1="Chalaadi Glacier Tour from Mestia",
       title="Chalaadi Glacier Tour from Mestia — from ₾400 per jeep",
       desc="Chalaadi Glacier from Mestia in half a day: jeep to the bridge, then a 2-hour forest walk to the glacier tongue. From ₾400 per jeep for up to 6, 3.5–4 hours.",
       price_unit="per jeep, up to 6", dur="half day", dur_hours="3.5–4 h",
       stats=[("from ₾400","per jeep"),("half day","3.5–4 h"),("up to 6","people"),("30 min","jeep to trailhead"),("easy","level")],
       route=[("Departure from Mestia","4×4 jeep, 8 km of gravel along the Mestiachala, ~30 minutes."),
              ("Bridge over the Mestiachala","Start of the walk, briefing with the guide."),
              ("Pine forest along the river","Gentle climb ~1.5 h, about 300 m of ascent."),
              ("Chalaadi glacier tongue","Blue ice right by the trail, photos, a 30-minute rest."),
              ("Descent to the bridge","Back along the same trail, easier and quicker."),
              ("Return to Mestia","Jeep back to the centre of Mestia.")],
       map_line="Mestia → Mestiachala bridge → Chalaadi Glacier",
       body=[("Chalaadi — the most accessible glacier in Svaneti","The Chalaadi Glacier descends from the Ushba massif and ends just an hour's walk from Mestia. That makes it the easiest glacier trail in the region: families with children, first-time trekkers and anyone with only half a day come here. The glacier tongue sits at around 2,000 metres, and you can walk right up to the blue ice."),
             ("How the route works","The first 8 kilometres from Mestia to the bridge over the Mestiachala river we drive by 4×4 — meltwater breaks up the gravel and an ordinary car won't make it. From the bridge the walking section begins: the trail runs through dense pine forest along the glacial river with a gentle climb. After about ninety minutes the forest opens up and a grey-blue wall of ice appears before you."),
             ("Who it suits","The route is rated easy to moderate. No special preparation is needed — sturdy shoes with grip and a jacket are enough, as it is noticeably colder at the glacier than in Mestia even in summer. Children from 8 handle the trail easily. Total time on the ground is 3.5–4 hours, so Chalaadi pairs neatly with lunch in Mestia and a second activity the same day, such as a jeep climb to the <a href=\"../ozero-koruldi-mestia/\">Koruldi Lakes</a>.")],
       faq=[("How long is the Chalaadi Glacier tour?","Half a day — 3.5–4 hours from departure to your return to Mestia. About 30 minutes of that is the jeep to the bridge, and the walk itself, there and back, is roughly 3 hours at an easy pace with photo stops."),
            ("How hard is the trail and do I need to prepare?","The trail is easy to moderate: a gentle forest climb of about 300 metres. No special fitness is required — children from 8 and people with no trekking experience complete it. You need shoes with grip and a warm jacket."),
            ("What does the ₾400 price include?","₾400 is for the jeep for up to 6 people: a 4×4 with driver to the bridge and back plus an English-speaking guide on the trail. For a group of 4–6 it works out very cheap per person. Lunch and personal expenses are extra."),
            ("Can I reach Chalaadi on foot without a jeep?","Yes, you can walk straight from Mestia, but that adds about 8 km of gravel each way and turns it into a full day. The jeep saves 2–3 hours and your energy for the prettiest, forest part of the walk."),
            ("What season is the glacier open?","May to October. In summer the trail is dry and comfortable; in the shoulder season there may be snow patches on the approach. In winter the route is closed due to avalanche risk — we offer other winter activities in Svaneti then.")],
       tip="Head to Chalaadi in the first half of the day: in the afternoon clouds often roll off the glacier and a cold wind picks up along the river valley. Bring a snack — you'll want to linger at the glacier tongue longer than you expect. And don't walk right up under the ice: the glacier is alive and drops rocks and ice, so the safe spot for photos is off to the side, which the guide will show you.",
     ),
     ka=dict(
       h1="ჭალაადის მყინვარის ტური მესტიიდან",
       title="ჭალაადის მყინვარის ტური მესტიიდან — 400 ₾-დან ჯიპზე",
       desc="ჭალაადის მყინვარი მესტიიდან ნახევარ დღეში: ჯიპი ხიდამდე, შემდეგ 2 საათი ფეხით ტყეში მყინვარამდე. 400 ₾-დან ჯიპზე 6 კაცამდე, გიდი, 3.5–4 საათი.",
       price_unit="ჯიპზე, 6 კაცამდე", dur="ნახევარი დღე", dur_hours="3.5–4 სთ",
       stats=[("400 ₾-დან","ჯიპზე"),("ნახევარი დღე","3.5–4 სთ"),("6-მდე","კაცი"),("30 წთ","ჯიპით დაწყებამდე"),("მარტივი","დონე")],
       route=[("გამგზავრება მესტიიდან","ჯიპი 4×4, 8 კმ გრუნტი მესტიაჩალას გასწვრივ, ~30 წუთი."),
              ("ხიდი მესტიაჩალაზე","ფეხით მარშრუტის დაწყება, გიდის ინსტრუქტაჟი."),
              ("წიწვოვანი ტყე მდინარის გასწვრივ","მსუბუქი აღმართი ~1.5 სთ, აღმასვლა დაახლ. 300 მ."),
              ("ჭალაადის მყინვარის ბოლო","ცისფერი ყინული ბილიკთან, ფოტო, დასვენება 30 წუთი."),
              ("დაშვება ხიდამდე","იმავე ბილიკით უკან, უფრო მარტივი და სწრაფი."),
              ("დაბრუნება მესტიაში","ჯიპით უკან მესტიის ცენტრში.")],
       map_line="მესტია → მესტიაჩალას ხიდი → ჭალაადის მყინვარი",
       body=[("ჭალაადი — სვანეთის ყველაზე ხელმისაწვდომი მყინვარი","ჭალაადის მყინვარი ეშვება უშბის მასივიდან და მთავრდება მესტიიდან სულ ერთი საათის სავალზე. ეს მას რეგიონის ყველაზე მარტივ მყინვარულ ბილიკად აქცევს: აქ მოდიან ოჯახები ბავშვებით, დამწყები მოლაშქრეები და ყველა, ვისაც მხოლოდ ნახევარი დღე აქვს. მყინვარის ბოლო დაახლოებით 2000 მეტრზეა და ცისფერ ყინულთან ახლოს მისვლა შესაძლებელია."),
             ("როგორ მიმდინარეობს მარშრუტი","პირველ 8 კილომეტრს მესტიიდან ხიდამდე მდინარე მესტიაჩალაზე ჯიპით გავდივართ — გრუნტს დნობის წყალი არღვევს და ჩვეულებრივი მანქანა ვერ გაივლის. ხიდიდან იწყება ფეხით მონაკვეთი: ბილიკი მიდის ხშირ წიწვოვან ტყეში მდინარის გასწვრივ, აღმართი მშვიდია. დაახლოებით საათნახევარში ტყე იშლება და თქვენ წინ რუხ-ცისფერი ყინულის კედელი იშლება."),
             ("ვისთვის არის შესაფერისი","მარშრუტი მარტივი-საშუალო დონისაა. სპეციალური მომზადება არ სჭირდება — საკმარისია მოსახერხებელი ფეხსაცმელი და ქურთუკი: მყინვართან ზაფხულშიც კი უფრო ცივა, ვიდრე მესტიაში. 8 წლიდან ბავშვები ბილიკს მშვიდად გადიან. მიწაზე მთლიანი დრო 3.5–4 საათია, ამიტომ ჭალაადი ადვილად ერწყმის მესტიაში სადილს და მეორე აქტივობას იმავე დღეს, მაგალითად, ჯიპით ასვლას <a href=\"../ozero-koruldi-mestia/\">კორულდის ტბებამდე</a>.")],
       faq=[("რამდენ ხანს გრძელდება ჭალაადის მყინვარის ტური?","ნახევარი დღე — 3.5–4 საათი გამგზავრებიდან მესტიაში დაბრუნებამდე. აქედან დაახლოებით 30 წუთი ჯიპია ხიდამდე, თავად ფეხით სვლა კი წინ და უკან — დაახლოებით 3 საათი მშვიდი ტემპით ფოტო-გაჩერებებით."),
            ("რამდენად რთულია ბილიკი და საჭიროა თუ არა მომზადება?","ბილიკი მარტივი-საშუალოა: მშვიდი აღმართი ტყეში დაახლ. 300 მ აღმასვლით. სპეციალური ფიზიკური მომზადება არ სჭირდება, მარშრუტს გადიან 8 წლიდან ბავშვები და ლაშქრობის გამოცდილების გარეშე ადამიანები. საჭიროა მოსახერხებელი ფეხსაცმელი და თბილი ქურთუკი."),
            ("რა შედის 400 ₾ ფასში?","400 ₾ არის ჯიპზე 6 კაცამდე: 4×4 მძღოლით ხიდამდე და უკან და გიდი მარშრუტზე. ანუ 4–6 კაციან ჯგუფზე ძალიან იაფი გამოდის. სადილი და პირადი ხარჯები ცალკე იხდება."),
            ("შესაძლებელია თუ არა ჭალაადამდე ფეხით მისვლა ჯიპის გარეშე?","დიახ, შესაძლებელია ფეხით პირდაპირ მესტიიდან, მაგრამ მაშინ ემატება დაახლოებით 8 კმ გრუნტი ცალ მხარეს და დღე სრული ხდება. ჯიპი ზოგავს 2–3 საათს და ძალას მარშრუტის ყველაზე ლამაზი, ტყის ნაწილისთვის."),
            ("წლის რომელ დროს არის მყინვარი ხელმისაწვდომი?","მაისიდან ოქტომბრამდე. ზაფხულში ბილიკი მშრალი და კომფორტულია, შუალედურ სეზონზე შესაძლოა თოვლის ლაქები იყოს. ზამთარში მარშრუტი დახურულია ზვავის საფრთხის გამო — ამ დროს ვთავაზობთ სვანეთის სხვა ზამთრის აქტივობებს.")],
       tip="ჭალაადში დღის პირველ ნახევარში წადით: შუადღის შემდეგ მყინვარიდან ხშირად ღრუბლები ჩამოდის და ცივი ქარი უბერავს ხეობაში. აიღეთ საჭმელი — მყინვარის ბოლოსთან იმაზე მეტხანს გინდებათ დარჩენა, ვიდრე თავიდან გგონიათ. და ნუ მიხვალთ ყინულთან ძალიან ახლოს ქვემოდან: მყინვარი ცოცხალია, ცვივა ქვები და ყინული, ფოტოსთვის უსაფრთხო ადგილი გვერდზეა — გიდი გაჩვენებთ.",
     ),
   )),
 dict(slug="ushguli-iz-mestii", price="650", img="ushguli-tour-600",
   stops=[("Mestia",43.045,42.729),("Ipari",42.955,42.905),("Ushguli",42.9186,43.0117)],
   route_times=["09:00","10:30","11:30","12:30","13:30","15:00","16:00","18:00"],
   i18n=dict(
     ru=dict(
       h1="Экскурсия в Ушгули из Местии на джипе",
       title="Экскурсия в Ушгули из Местии — от ₾650 за джип",
       desc="Ушгули из Местии на весь день: джип по Ингури до высочайшего села Европы (2200 м) — башни ЮНЕСКО, храм Ламария, вид на Шхару. От ₾650 за машину.",
       price_unit="за джип до 6 чел", dur="весь день", dur_hours="8–9 ч",
       stats=[("от ₾650","за джип"),("весь день","8–9 ч"),("до 6","человек"),("2200 м","высота села"),("ЮНЕСКО","наследие")],
       route=[("Выезд из Местии","Внедорожник 4×4, 45 км грунтовки по Ингурскому ущелью."),
              ("Башни по дороге","Остановки в сёлах Ипари и Кала, сванские башни XII века."),
              ("Ушгули — община Чажаши","Самое высокое жилое село Европы, объект ЮНЕСКО."),
              ("Храм Ламария","Церковь XII века на холме, панорама вершины Шхара (5193 м)."),
              ("Обед в гостевом доме","Сванская кухня — кубдари, ташмиджаби, местная чача."),
              ("Свободное время","Прогулка среди башен, фото, музей."),
              ("Обратный путь","45 км обратно по ущелью."),
              ("Возвращение в Местию","")],
       map_line="Местия → Ипари → Ушгули",
       body=[("Ушгули — самое высокое жилое село Европы","Ушгули — это община из четырёх деревень на высоте 2200 метров, у самого подножия Шхары, высшей точки Грузии (5193 м). Люди живут здесь круглый год уже больше тысячи лет, а квартал Чажаши с его сванскими башнями внесён в список Всемирного наследия ЮНЕСКО. Это не музей под открытым небом, а настоящее горное село, где башни XI–XII веков стоят прямо во дворах жилых домов."),
             ("Дорога — половина впечатления","От Местии до Ушгули всего 45 километров, но по грунтовой дороге вдоль реки Ингури они занимают около двух часов в одну сторону. Обычная машина здесь не пройдёт, особенно после дождя, поэтому едем на подготовленном внедорожнике с опытным водителем. По пути — башенные сёла Ипари и Кала, где мы делаем остановки для фото. Именно из-за дороги Ушгули не получается посмотреть наскоком: это полноценный день."),
             ("Что смотрим в Ушгули","Главные точки — квартал Чажаши с самой плотной группой башен, храм Ламария XII века на холме над селом с открыточным видом на ледяную стену Шхары, и небольшой этнографический музей. Обед организуем в гостевом доме у местных: сванская кухня заметно отличается от остальной Грузии — кубдари с мясом и горными травами, ташмиджаби из сыра и картофеля, мягкая ячменная чача. Если хотите не только село, но и выйти пешком к большому леднику, берите <a href=\"../ushguli-shkhara-lednik/\">расширенный маршрут к Шхаре</a>.")],
       faq=[("Почему экскурсия в Ушгули занимает весь день, а не полдня?","Из-за дороги. От Местии до Ушгули всего 45 км, но по горной грунтовке вдоль Ингури это около 2 часов в одну сторону. Плюс время на осмотр села, храм Ламария и обед. Полдня физически не хватает — за это время едва успеешь доехать и вернуться, не увидев самого Ушгули."),
            ("Нужен ли внедорожник до Ушгули?","Да, обязательно. Дорога от Местии — это 45 км грунтовки, которую размывает после дождя. Мы подаём подготовленный 4×4 с опытным водителем — на обычной легковой машине этот участок не проехать безопасно."),
            ("Что входит в цену ₾650?","Цена ₾650 — за внедорожник до 6 человек с водителем и русскоязычным гидом на весь день. Обед в гостевом доме (₾25–35 с человека) и входные билеты в музей оплачиваются отдельно, точную смету пришлю при бронировании."),
            ("Можно ли увидеть ледник Шхара в этой поездке?","Издалека — да, вершина и ледяная стена Шхары прекрасно видны от храма Ламария. Но если хотите подойти к самому леднику пешком, выбирайте расширенный вариант «Ушгули и ледник Шхара» на весь день с треккингом к подножию."),
            ("В какое время года доступен Ушгули?","Оптимально с июня по октябрь, когда грунтовка сухая. Зимой и ранней весной дорогу нередко перекрывает снег и лавинная опасность, доступ бывает закрыт на несколько дней — поездку планируем по прогнозу.")],
       tip="Выезжайте в Ушгули пораньше: к середине дня грунтовка оживает, встречные джипы приходится пропускать на узких участках, и дорога затягивается. На высоте 2200 метров солнце обманчивое — сгораешь быстро даже в облачную погоду, берите крем и головной убор. И обязательно поднимитесь к храму Ламария: именно оттуда, а не из центра села, открывается тот самый вид на Шхару, ради которого сюда едут.",
     ),
     en=dict(
       h1="Ushguli Jeep Tour from Mestia",
       title="Ushguli Tour from Mestia — from ₾650 per jeep",
       desc="Ushguli from Mestia, full day: 4×4 up the Enguri to Europe's highest village (2,200 m) — UNESCO towers, Lamaria church, Shkhara views. From ₾650 per jeep.",
       price_unit="per jeep, up to 6", dur="full day", dur_hours="8–9 h",
       stats=[("from ₾650","per jeep"),("full day","8–9 h"),("up to 6","people"),("2,200 m","village altitude"),("UNESCO","heritage")],
       route=[("Departure from Mestia","4×4 jeep, 45 km of gravel up the Enguri gorge."),
              ("Towers along the way","Stops in Ipari and Kala, Svan towers from the 12th c."),
              ("Ushguli — Chazhashi","Highest inhabited village in Europe, a UNESCO site."),
              ("Lamaria church","12th-c. church on the hill, panorama of Shkhara (5,193 m)."),
              ("Lunch in a guesthouse","Svan cuisine — kubdari, tashmijabi, local chacha."),
              ("Free time","A walk among the towers, photos, the museum."),
              ("Return drive","45 km back down the gorge."),
              ("Return to Mestia","")],
       map_line="Mestia → Ipari → Ushguli",
       body=[("Ushguli — the highest inhabited village in Europe","Ushguli is a community of four villages at 2,200 metres, at the very foot of Shkhara, the highest peak in Georgia (5,193 m). People have lived here year-round for over a thousand years, and the Chazhashi quarter with its Svan towers is on the UNESCO World Heritage list. It is not an open-air museum but a real mountain village, where 11th–12th-century towers stand right in the yards of lived-in houses."),
             ("The road is half the experience","It is only 45 kilometres from Mestia to Ushguli, but along the gravel road beside the Enguri river they take about two hours each way. An ordinary car won't make it, especially after rain, so we travel in a prepared 4×4 with an experienced driver. Along the way are the tower villages of Ipari and Kala, where we stop for photos. Because of the road, Ushguli can't be seen in a rush — it is a full day."),
             ("What we see in Ushguli","The highlights are the Chazhashi quarter with the densest cluster of towers, the 12th-century Lamaria church on the hill above the village with its postcard view of Shkhara's ice wall, and a small ethnographic museum. Lunch is arranged in a local guesthouse: Svan cuisine differs noticeably from the rest of Georgia — kubdari with meat and mountain herbs, tashmijabi of cheese and potato, and a mild barley chacha. If you want not just the village but a walk out to the big glacier, take the <a href=\"../ushguli-shkhara-lednik/\">extended Shkhara route</a>.")],
       faq=[("Why does the Ushguli tour take a full day rather than half?","Because of the road. It is only 45 km from Mestia to Ushguli, but along the mountain gravel road beside the Enguri that is about 2 hours each way. Add time to see the village, the Lamaria church and lunch. Half a day simply isn't enough — you'd barely get there and back without seeing Ushguli itself."),
            ("Do I need a 4×4 to reach Ushguli?","Yes, definitely. The road from Mestia is 45 km of gravel that washes out after rain. We provide a prepared 4×4 with an experienced driver — an ordinary car cannot drive this section safely."),
            ("What does the ₾650 price include?","₾650 is for the 4×4 for up to 6 people with driver and an English-speaking guide for the whole day. Lunch in a guesthouse (₾25–35 per person) and museum tickets are extra; I'll send an exact estimate when you book."),
            ("Can I see the Shkhara glacier on this trip?","From a distance, yes — the peak and ice wall of Shkhara are clearly visible from the Lamaria church. But if you want to walk up to the glacier itself, choose the extended 'Ushguli & Shkhara Glacier' full-day option with a trek to its foot."),
            ("What season is Ushguli open?","Best from June to October, when the gravel is dry. In winter and early spring snow and avalanche risk often close the road for several days — we plan the trip around the forecast.")],
       tip="Set off for Ushguli early: by midday the gravel road gets busy, you have to give way to oncoming jeeps on the narrow stretches, and the drive drags out. At 2,200 metres the sun is deceptive — you burn quickly even in cloud, so bring cream and a hat. And be sure to climb up to the Lamaria church: it is from there, not the village centre, that the famous view of Shkhara opens up that people come here for.",
     ),
     ka=dict(
       h1="უშგულის ჯიპ-ტური მესტიიდან",
       title="უშგულის ტური მესტიიდან — 650 ₾-დან ჯიპზე",
       desc="უშგული მესტიიდან მთელი დღე: ჯიპით ენგურის ხეობაში ევროპის უმაღლეს სოფლამდე (2200 მ) — იუნესკოს კოშკები, ლამარიას ტაძარი, შხარას ხედი. 650 ₾-დან.",
       price_unit="ჯიპზე, 6 კაცამდე", dur="მთელი დღე", dur_hours="8–9 სთ",
       stats=[("650 ₾-დან","ჯიპზე"),("მთელი დღე","8–9 სთ"),("6-მდე","კაცი"),("2200 მ","სოფლის სიმაღლე"),("იუნესკო","მემკვიდრეობა")],
       route=[("გამგზავრება მესტიიდან","ჯიპი 4×4, 45 კმ გრუნტი ენგურის ხეობაში."),
              ("კოშკები გზაზე","გაჩერებები სოფლებში იფარი და კალა, XII საუკუნის სვანური კოშკები."),
              ("უშგული — ჩაჟაში","ევროპის ყველაზე მაღალი დასახლებული სოფელი, იუნესკოს ობიექტი."),
              ("ლამარიას ტაძარი","XII საუკუნის ეკლესია გორაზე, შხარას მწვერვალის პანორამა (5193 მ)."),
              ("სადილი სასტუმრო სახლში","სვანური სამზარეულო — კუბდარი, ტაშმიჯაბი, ადგილობრივი ჭაჭა."),
              ("თავისუფალი დრო","სეირნობა კოშკებს შორის, ფოტო, მუზეუმი."),
              ("უკან გზა","45 კმ უკან ხეობაში."),
              ("დაბრუნება მესტიაში","")],
       map_line="მესტია → იფარი → უშგული",
       body=[("უშგული — ევროპის ყველაზე მაღალი დასახლებული სოფელი","უშგული ოთხი სოფლის თემია 2200 მეტრზე, შხარას, საქართველოს უმაღლესი მწვერვალის (5193 მ) ძირში. აქ ხალხი მთელი წელი ცხოვრობს უკვე ათას წელზე მეტია, ხოლო ჩაჟაშის უბანი თავისი სვანური კოშკებით იუნესკოს მსოფლიო მემკვიდრეობის ნუსხაშია. ეს ღია ცის ქვეშ მუზეუმი კი არა, ნამდვილი მთის სოფელია, სადაც XI–XII საუკუნის კოშკები დგას საცხოვრებელი სახლების ეზოებში."),
             ("გზა — შთაბეჭდილების ნახევარი","მესტიიდან უშგულამდე სულ 45 კილომეტრია, მაგრამ გრუნტის გზით მდინარე ენგურის გასწვრივ ისინი დაახლოებით ორ საათს იკავებს ცალ მხარეს. ჩვეულებრივი მანქანა აქ ვერ გაივლის, განსაკუთრებით წვიმის შემდეგ, ამიტომ მივდივართ მომზადებული ჯიპით გამოცდილი მძღოლით. გზად — კოშკებიანი სოფლები იფარი და კალა, სადაც ვჩერდებით ფოტოსთვის. სწორედ გზის გამო უშგულის ნაჩქარევად ნახვა არ გამოდის: ეს სრული დღეა."),
             ("რას ვათვალიერებთ უშგულში","მთავარი წერტილებია ჩაჟაშის უბანი კოშკების ყველაზე მჭიდრო ჯგუფით, XII საუკუნის ლამარიას ტაძარი გორაზე სოფლის ზემოთ შხარას ყინულის კედლის სახოტბო ხედით, და პატარა ეთნოგრაფიული მუზეუმი. სადილს ვაწყობთ ადგილობრივების სასტუმრო სახლში: სვანური სამზარეულო შესამჩნევად განსხვავდება დანარჩენი საქართველოსგან — კუბდარი ხორცითა და მთის მწვანილით, ტაშმიჯაბი ყველითა და კარტოფილით, რბილი ქერის ჭაჭა. თუ გინდათ არა მხოლოდ სოფელი, არამედ ფეხით გასვლა დიდ მყინვართან, აირჩიეთ <a href=\"../ushguli-shkhara-lednik/\">გაფართოებული მარშრუტი შხარამდე</a>.")],
       faq=[("რატომ იკავებს უშგულის ტური მთელ დღეს და არა ნახევარს?","გზის გამო. მესტიიდან უშგულამდე სულ 45 კმ-ია, მაგრამ მთის გრუნტის გზით ენგურის გასწვრივ ეს დაახლოებით 2 საათია ცალ მხარეს. პლუს დრო სოფლის დათვალიერებაზე, ლამარიას ტაძარსა და სადილზე. ნახევარი დღე უბრალოდ არ ჰყოფნის — ამ დროში ძლივს მიხვალ და დაბრუნდები თავად უშგულის ნახვის გარეშე."),
            ("საჭიროა თუ არა ჯიპი უშგულამდე?","დიახ, აუცილებლად. გზა მესტიიდან არის 45 კმ გრუნტი, რომელსაც წვიმის შემდეგ რეცხავს. ჩვენ ვაწვდით მომზადებულ 4×4-ს გამოცდილი მძღოლით — ჩვეულებრივი მანქანით ეს მონაკვეთი უსაფრთხოდ ვერ გაივლი."),
            ("რა შედის 650 ₾ ფასში?","650 ₾ არის 4×4-ზე 6 კაცამდე მძღოლითა და გიდით მთელი დღით. სადილი სასტუმრო სახლში (25–35 ₾ ერთ კაცზე) და მუზეუმის ბილეთები ცალკე იხდება; ზუსტ ხარჯთაღრიცხვას დაჯავშნისას გამოგიგზავნით."),
            ("შესაძლებელია თუ არა შხარას მყინვარის ნახვა ამ მოგზაურობაში?","შორიდან — დიახ, შხარას მწვერვალი და ყინულის კედელი კარგად ჩანს ლამარიას ტაძრიდან. მაგრამ თუ გინდათ თავად მყინვართან ფეხით მისვლა, აირჩიეთ გაფართოებული ვარიანტი «უშგული და შხარას მყინვარი» მთელი დღით და ლაშქრობით ძირამდე."),
            ("წლის რომელ დროს არის უშგული ხელმისაწვდომი?","ოპტიმალურია ივნისიდან ოქტომბრამდე, როცა გრუნტი მშრალია. ზამთარსა და ადრე გაზაფხულზე გზას ხშირად კეტავს თოვლი და ზვავის საფრთხე, წვდომა შესაძლოა რამდენიმე დღით დაიხუროს — მოგზაურობას ვგეგმავთ ამინდის პროგნოზით.")],
       tip="უშგულში ადრე გაემგზავრეთ: შუადღისთვის გრუნტის გზა ცოცხლდება, შემხვედრ ჯიპებს ვიწრო მონაკვეთებზე უნდა დაუთმო და გზა იწელება. 2200 მეტრზე მზე მაცდურია — სწრაფად იწვები ღრუბლიან ამინდშიც, აიღეთ კრემი და თავსაბურავი. და აუცილებლად ავიდეთ ლამარიას ტაძართან: სწორედ იქიდან, და არა სოფლის ცენტრიდან, იშლება ის შხარას ხედი, რისთვისაც აქ მოდიან.",
     ),
   )),
 dict(slug="ushguli-shkhara-lednik", price="750", img="shkhara-tour-600",
   stops=[("Mestia",43.045,42.729),("Ushguli",42.9186,43.0117),("Shkhara Glacier",42.966,43.108)],
   route_times=["08:30","10:30","11:30","13:30","14:00","16:00","17:00","19:00"],
   i18n=dict(
     ru=dict(
       h1="Ушгули и ледник Шхара — тур на весь день из Местии",
       title="Ушгули и ледник Шхара из Местии — тур на весь день, от ₾750",
       desc="Ушгули и ледник Шхара за день из Местии: село-ЮНЕСКО 2200 м и треккинг к подножию высшей вершины Грузии Шхара (5193 м). От ₾750 за джип, гид.",
       price_unit="за джип до 6 чел", dur="весь день", dur_hours="9–10 ч",
       stats=[("от ₾750","за джип"),("весь день","9–10 ч"),("до 6","человек"),("6 км","трек к леднику"),("средний","уровень")],
       route=[("Выезд из Местии","Ранний старт на внедорожнике, 45 км по Ингурскому ущелью."),
              ("Ушгули","Башни Чажаши (ЮНЕСКО), храм Ламария XII века."),
              ("Старт треккинга к Шхаре","Пеший маршрут 6 км от Ушгули вверх вдоль Ингури."),
              ("Подножие ледника Шхара","Высота ~2200 м, панорама стены Шхара (5193 м)."),
              ("Пикник и обратный путь","Спуск обратно к Ушгули."),
              ("Обед в Ушгули","Сванская кухня в гостевом доме."),
              ("Обратный путь в Местию",""),
              ("Возвращение в Местию","")],
       map_line="Местия → Ушгули → ледник Шхара",
       body=[("Два главных вида Сванетии за один день","Это расширенный вариант поездки в Ушгули для тех, кто хочет не просто увидеть село, а дойти пешком до подножия Шхары — высочайшей вершины Грузии (5193 м). Сначала едем в Ушгули, самое высокое жилое село Европы под защитой ЮНЕСКО, а затем выходим на треккинг вверх по долине Ингури к языку ледника Шхара. За один насыщенный день — и средневековые башни, и большой кавказский лёд."),
             ("Треккинг к леднику Шхара","От Ушгули к подножию ледника ведёт около 6 километров тропы вдоль реки Ингури — это её исток. Маршрут пологий по меркам гор, но небыстрый: подъём к точке ~2200 метров и обратно занимает 3–4 часа. В конце тропа выводит к морене, за которой поднимается ледяная стена Безенги и Шхары. Уровень — средний: нужна нормальная физическая форма и обувь для треккинга, но альпинистских навыков не требуется."),
             ("Логистика дня","Стартуем из Местии раньше обычного — в 8:30, потому что день длинный: 2 часа дороги до Ушгули, осмотр села, 3–4 часа на треккинг, обед и обратный путь. Внедорожник с водителем ждёт нас в Ушгули, пока мы на тропе. В самом Ушгули на входе к Башне Любви берут символические 2 лари. Возвращение в Местию — к 19:00, поэтому вечер лучше оставить свободным. Если треккинг не входит в планы, подойдёт <a href=\"../ushguli-iz-mestii/\">обычная поездка в Ушгули</a> без выхода к леднику.")],
       faq=[("Чем этот тур отличается от обычной поездки в Ушгули?","Здесь добавлен треккинг: помимо осмотра села Ушгули вы пешком доходите до подножия ледника Шхара — 6 км тропы вдоль Ингури в одну сторону. Обычная экскурсия в Ушгули ограничивается селом и видом на Шхару издалека, без пешего выхода к леднику."),
            ("Насколько тяжёлый треккинг к Шхаре?","Средний уровень. Тропа пологая, без опасных участков, но длинная — 6 км в одну сторону и 3–4 часа на весь пеший отрезок. Нужна нормальная физическая форма и треккинговая обувь. Альпинистского снаряжения и опыта не требуется."),
            ("Сколько длится весь день?","9–10 часов: выезд из Местии в 8:30, возвращение около 19:00. В это входят 2 часа дороги в каждую сторону, осмотр Ушгули, треккинг к леднику и обед. День насыщенный, поэтому вечер стоит оставить свободным."),
            ("Что входит в цену ₾750?","Цена ₾750 — за внедорожник до 6 человек с водителем и русскоязычным гидом на весь день, включая сопровождение на треккинге. Обед в Ушгули, входной сбор к Башне Любви (2 ₾) и личные расходы — отдельно."),
            ("Когда лучше ехать?","С июня по сентябрь, когда тропа к Шхаре свободна от снега и река спокойна для бродов. В межсезонье возможны снежники и высокая вода, поэтому маршрут подбираем по состоянию тропы и прогнозу.")],
       tip="Ледник Шхара — это исток Ингури, и брод через ручьи в начале лета бывает выше, чем хочется. Возьмите треккинговые палки и не поленитесь про запасные носки. Выходите на тропу сразу после Ушгули, не затягивая обед на потом: во второй половине дня с ледника тянет облака, и панорама стены Шхары закрывается. Лучший свет на вершину — до полудня.",
     ),
     en=dict(
       h1="Ushguli & Shkhara Glacier — Full-Day Tour from Mestia",
       title="Ushguli & Shkhara Glacier from Mestia — full day, from ₾750",
       desc="Ushguli plus a trek to the Shkhara glacier from Mestia: UNESCO village at 2,200 m and the foot of Georgia's highest peak (5,193 m). From ₾750 per jeep.",
       price_unit="per jeep, up to 6", dur="full day", dur_hours="9–10 h",
       stats=[("from ₾750","per jeep"),("full day","9–10 h"),("up to 6","people"),("6 km","trek to glacier"),("moderate","level")],
       route=[("Departure from Mestia","Early start by 4×4, 45 km up the Enguri gorge."),
              ("Ushguli","Chazhashi towers (UNESCO), 12th-c. Lamaria church."),
              ("Start of the Shkhara trek","6 km on foot from Ushguli up along the Enguri."),
              ("Foot of the Shkhara glacier","About 2,200 m, panorama of the Shkhara wall (5,193 m)."),
              ("Picnic and return","Descent back to Ushguli."),
              ("Lunch in Ushguli","Svan cuisine in a guesthouse."),
              ("Return drive to Mestia",""),
              ("Return to Mestia","")],
       map_line="Mestia → Ushguli → Shkhara Glacier",
       body=[("Two of Svaneti's best views in one day","This is the extended version of the Ushguli trip for those who want not just to see the village but to walk to the foot of Shkhara — the highest peak in Georgia (5,193 m). First we drive to Ushguli, the highest inhabited village in Europe under UNESCO protection, then set out on a trek up the Enguri valley to the tongue of the Shkhara glacier. In one full day — both medieval towers and big Caucasus ice."),
             ("The trek to the Shkhara glacier","From Ushguli to the foot of the glacier runs about 6 kilometres of trail along the Enguri river — this is its source. The route is gentle by mountain standards but not quick: the climb to about 2,200 metres and back takes 3–4 hours. At the end the trail reaches a moraine, beyond which the ice wall of Bezengi and Shkhara rises. The level is moderate: you need reasonable fitness and trekking shoes, but no mountaineering skills."),
             ("The logistics of the day","We leave Mestia earlier than usual — at 8:30 — because the day is long: 2 hours to Ushguli, seeing the village, 3–4 hours of trekking, lunch and the return. The 4×4 with driver waits for us in Ushguli while we are on the trail. In Ushguli there is a token 2 GEL fee at the Tower of Love. We're back in Mestia by 19:00, so it's best to keep the evening free. If a trek isn't for you, the <a href=\"../ushguli-iz-mestii/\">standard Ushguli tour</a> without the glacier walk is a gentler option.")],
       faq=[("How is this tour different from the regular Ushguli trip?","It adds a trek: besides seeing the village of Ushguli you walk to the foot of the Shkhara glacier — 6 km of trail along the Enguri each way. The regular Ushguli tour is limited to the village and a distant view of Shkhara, with no walk out to the glacier."),
            ("How hard is the trek to Shkhara?","Moderate. The trail is gentle with no dangerous sections, but long — 6 km each way and 3–4 hours for the whole walking part. You need reasonable fitness and trekking shoes. No mountaineering gear or experience is required."),
            ("How long is the whole day?","9–10 hours: departure from Mestia at 8:30, return around 19:00. That includes 2 hours of driving each way, seeing Ushguli, the trek to the glacier and lunch. It's a full day, so keep the evening free."),
            ("What does the ₾750 price include?","₾750 is for the 4×4 for up to 6 people with driver and an English-speaking guide for the whole day, including on the trek. Lunch in Ushguli, the Tower of Love fee (2 ₾) and personal expenses are extra."),
            ("When is the best time to go?","June to September, when the trail to Shkhara is free of snow and the river is calm for the fords. In the shoulder season there may be snow patches and high water, so we adjust the route to trail conditions and the forecast.")],
       tip="The Shkhara glacier is the source of the Enguri, and in early summer the stream fords can be higher than you'd like. Bring trekking poles and don't skip a spare pair of socks. Set out on the trail right after Ushguli, without dragging lunch out: in the afternoon clouds roll off the glacier and the panorama of the Shkhara wall closes in. The best light on the peak is before noon.",
     ),
     ka=dict(
       h1="უშგული და შხარას მყინვარი — მთელი დღის ტური მესტიიდან",
       title="უშგული და შხარას მყინვარი მესტიიდან — მთელი დღე, 750 ₾-დან",
       desc="უშგული და შხარას მყინვარი ერთ დღეში მესტიიდან: იუნესკოს სოფელი 2200 მ და ლაშქრობა საქართველოს უმაღლესი მწვერვალის ძირამდე (5193 მ). 750 ₾-დან ჯიპზე.",
       price_unit="ჯიპზე, 6 კაცამდე", dur="მთელი დღე", dur_hours="9–10 სთ",
       stats=[("750 ₾-დან","ჯიპზე"),("მთელი დღე","9–10 სთ"),("6-მდე","კაცი"),("6 კმ","ტრეკი მყინვარამდე"),("საშუალო","დონე")],
       route=[("გამგზავრება მესტიიდან","ადრეული დაწყება ჯიპით, 45 კმ ენგურის ხეობაში."),
              ("უშგული","ჩაჟაშის კოშკები (იუნესკო), XII საუკუნის ლამარიას ტაძარი."),
              ("შხარას ტრეკის დაწყება","6 კმ ფეხით უშგულიდან ზემოთ ენგურის გასწვრივ."),
              ("შხარას მყინვარის ძირი","სიმაღლე ~2200 მ, შხარას კედლის პანორამა (5193 მ)."),
              ("პიკნიკი და უკან გზა","დაშვება უკან უშგულამდე."),
              ("სადილი უშგულში","სვანური სამზარეულო სასტუმრო სახლში."),
              ("უკან გზა მესტიაში",""),
              ("დაბრუნება მესტიაში","")],
       map_line="მესტია → უშგული → შხარას მყინვარი",
       body=[("სვანეთის ორი მთავარი ხედი ერთ დღეში","ეს არის უშგულის მოგზაურობის გაფართოებული ვარიანტი მათთვის, ვისაც უნდა არა უბრალოდ სოფლის ნახვა, არამედ ფეხით მისვლა შხარას — საქართველოს უმაღლესი მწვერვალის (5193 მ) ძირამდე. ჯერ მივდივართ უშგულში, ევროპის ყველაზე მაღალ დასახლებულ სოფელში იუნესკოს დაცვით, შემდეგ გავდივართ ლაშქრობაზე ენგურის ხეობაში შხარას მყინვარის ბოლომდე. ერთ დატვირთულ დღეში — შუა საუკუნეების კოშკებიც და დიდი კავკასიური ყინულიც."),
             ("ლაშქრობა შხარას მყინვარამდე","უშგულიდან მყინვარის ძირამდე მიდის დაახლოებით 6 კილომეტრი ბილიკი მდინარე ენგურის გასწვრივ — ეს მისი სათავეა. მარშრუტი მთის საზომით მშვიდია, მაგრამ არა სწრაფი: აღმართი ~2200 მეტრამდე და უკან 3–4 საათს იკავებს. ბოლოს ბილიკი გამოდის მორენასთან, რომლის მიღმა იმართება ბეზენგისა და შხარას ყინულის კედელი. დონე საშუალოა: საჭიროა ნორმალური ფიზიკური ფორმა და სალაშქრო ფეხსაცმელი, მაგრამ ალპინისტური უნარები არ სჭირდება."),
             ("დღის ლოგისტიკა","მესტიიდან ჩვეულებრივზე ადრე ვიწყებთ — 8:30-ზე, რადგან დღე გრძელია: 2 საათი გზა უშგულამდე, სოფლის დათვალიერება, 3–4 საათი ლაშქრობა, სადილი და უკან გზა. ჯიპი მძღოლით გველოდება უშგულში, სანამ ბილიკზე ვართ. თავად უშგულში სიყვარულის კოშკთან შესვლისას იღებენ სიმბოლურ 2 ლარს. მესტიაში დაბრუნება — 19:00-სთვის, ამიტომ საღამო სჯობს თავისუფალი დატოვოთ. თუ ლაშქრობა გეგმებში არ არის, გამოდგება <a href=\"../ushguli-iz-mestii/\">ჩვეულებრივი უშგულის ტური</a> მყინვართან გასვლის გარეშე.")],
       faq=[("რით განსხვავდება ეს ტური ჩვეულებრივი უშგულის მოგზაურობისგან?","აქ დამატებულია ლაშქრობა: უშგულის სოფლის დათვალიერების გარდა ფეხით მიდიხართ შხარას მყინვარის ძირამდე — 6 კმ ბილიკი ენგურის გასწვრივ ცალ მხარეს. ჩვეულებრივი უშგულის ტური სოფლითა და შხარას შორეული ხედით შემოიფარგლება, მყინვარამდე ფეხით გასვლის გარეშე."),
            ("რამდენად რთულია ლაშქრობა შხარამდე?","საშუალო დონე. ბილიკი მშვიდია, საშიში მონაკვეთების გარეშე, მაგრამ გრძელი — 6 კმ ცალ მხარეს და 3–4 საათი მთელ ფეხით მონაკვეთზე. საჭიროა ნორმალური ფიზიკური ფორმა და სალაშქრო ფეხსაცმელი. ალპინისტური აღჭურვილობა და გამოცდილება არ სჭირდება."),
            ("რამდენ ხანს გრძელდება მთელი დღე?","9–10 საათი: გამგზავრება მესტიიდან 8:30-ზე, დაბრუნება დაახლოებით 19:00-ზე. ეს მოიცავს 2 საათ გზას ცალ მხარეს, უშგულის დათვალიერებას, ლაშქრობას მყინვარამდე და სადილს. დღე დატვირთულია, ამიტომ საღამო ღირს თავისუფალი დატოვოთ."),
            ("რა შედის 750 ₾ ფასში?","750 ₾ არის 4×4-ზე 6 კაცამდე მძღოლითა და გიდით მთელი დღით, ლაშქრობაზე თანხლების ჩათვლით. სადილი უშგულში, სიყვარულის კოშკის შესვლა (2 ₾) და პირადი ხარჯები — ცალკე."),
            ("როდის სჯობს წასვლა?","ივნისიდან სექტემბრამდე, როცა შხარას ბილიკი თოვლისგან თავისუფალია და მდინარე მშვიდია ფონისთვის. შუალედურ სეზონზე შესაძლოა თოვლის ლაქები და მაღალი წყალი, ამიტომ მარშრუტს ბილიკის მდგომარეობითა და პროგნოზით ვარჩევთ.")],
       tip="შხარას მყინვარი ენგურის სათავეა, და ზაფხულის დასაწყისში ნაკადულების ფონი შესაძლოა იმაზე მაღალი იყოს, ვიდრე გინდათ. აიღეთ სალაშქრო ჯოხები და ნუ დაიზარებთ სათადარიგო წინდებს. ბილიკზე გადით უშგულის შემდეგ მაშინვე, სადილის გადავადების გარეშე: შუადღის შემდეგ მყინვარიდან ღრუბლები ჩამოდის და შხარას კედლის პანორამა იხურება. საუკეთესო შუქი მწვერვალზე — შუადღემდე.",
     ),
   )),
 dict(slug="ozero-koruldi-mestia", price="400", img="koruldi-tour-600",
   stops=[("Mestia",43.045,42.729),("Cross above Mestia",43.058,42.719),("Koruldi Lakes",43.068,42.706)],
   route_times=["09:00","09:45","10:15","11:00","12:00","13:00"],
   i18n=dict(
     ru=dict(
       h1="Озёра Корульди из Местии на джипе",
       title="Озёра Корульди из Местии на джипе — от ₾400",
       desc="Озёра Корульди над Местией за полдня: подъём на 4×4 к кресту 2160 м и трек к альпийским озёрам 2750 м с видом на Ушбу. От ₾400 за джип, 3.5–4 часа.",
       price_unit="за джип до 6 чел", dur="полдня", dur_hours="3.5–4 ч",
       stats=[("от ₾400","за джип"),("полдня","3.5–4 ч"),("до 6","человек"),("2750 м","высота озёр"),("Ушба","главный вид")],
       route=[("Выезд из Местии","Внедорожник 4×4, крутой серпантин вверх над городом."),
              ("Крест над Местией (2160 м)","Смотровая площадка, панорама Ушбы (4710 м) и долины."),
              ("Подъём к озёрам","Джип по бездорожью или короткий трек — по погоде и состоянию дороги."),
              ("Озёра Корульди (2750 м)","Альпийские озёра с отражением вершин, фото."),
              ("Обратный путь","Спуск на джипе в Местию."),
              ("Возвращение в Местию","")],
       map_line="Местия → крест 2160 м → озёра Корульди",
       body=[("Корульди — лучшая смотровая Сванетии","Озёра Корульди лежат на альпийском плато на высоте 2750 метров прямо над Местией. Отсюда открывается, пожалуй, самый эффектный вид региона: двуглавая Ушба (4710 м), пирамида Тетнульди и вся долина Местии как на ладони. В спокойную погоду вершины отражаются в озёрах — это визитная карточка Сванетии, которую вы видели на всех открытках."),
             ("Дорога — приключение само по себе","Подъём к Корульди — один из самых крутых джиповых маршрутов Грузии. Внедорожник карабкается серпантином от Местии до креста на высоте 2160 метров, а выше начинается настоящее бездорожье. В зависимости от погоды и состояния грунта до самих озёр мы либо доезжаем на джипе, либо оставляем машину у креста и проходим последний отрезок пешком (30–40 минут). Обычная машина сюда не поднимается в принципе."),
             ("Полдня с максимальной отдачей","Весь маршрут занимает 3.5–4 часа, поэтому Корульди идеально берут либо утром, либо после обеда — а вторую половину дня оставляют на <a href=\"../lednik-chalaadi-mestia/\">ледник Чалаади</a> или прогулку по Местии. Наверху заметно холоднее и ветренее, чем в городе, даже в разгар лета: тёплая куртка обязательна. Крест над Местией — отдельная точка притяжения: многие остаются здесь встречать закат с видом на Ушбу.")],
       faq=[("Сколько длится поездка к озёрам Корульди?","Полдня — 3.5–4 часа от Местии и обратно. Основное время занимает крутой подъём на джипе; наверху у озёр и на смотровой проводим около часа. Маршрут легко совместить со второй активностью в тот же день."),
            ("Нужно ли идти пешком или всё на джипе?","Зависит от погоды и состояния дороги. В сухую погоду внедорожник доезжает почти до самых озёр. После дождя последний участок проходят пешком от креста — это 30–40 минут по несложной тропе. Гид решает на месте, что безопаснее."),
            ("Что входит в цену ₾400?","Цена ₾400 — за джип 4×4 до 6 человек с водителем и русскоязычным гидом. Это один из самых экономных вариантов на компанию: на 4–6 человек выходит совсем недорого за такой вид. Личные расходы — отдельно."),
            ("Почему нельзя доехать на обычной машине?","Дорога к Корульди — крутой каменистый серпантин с бездорожьем выше креста. Легковая машина такой подъём не осилит, а после дождя он опасен даже для неподготовленного внедорожника. Едем только на подготовленном 4×4 с опытным водителем."),
            ("Когда лучший вид на Ушбу?","Ушба чаще открыта утром и на закате — днём вершину нередко затягивает облаками. Для лучших кадров берём либо ранний выезд, либо предзакатный: свет на Ушбе в это время самый выразительный.")],
       tip="Корульди — про виды, а виды про погоду. Ушба капризна: утром чистая, к полудню в облаках. Если небо ясное — не откладывайте, поднимайтесь сразу. Наверху на 2750 метрах ветер пронизывает даже в июле, тёплая куртка и шапка не будут лишними. И заложите лишние 20 минут на кресте над Местией: многие считают вид оттуда сильнее самих озёр.",
     ),
     en=dict(
       h1="Koruldi Lakes Jeep Tour from Mestia",
       title="Koruldi Lakes from Mestia by Jeep — from ₾400",
       desc="Koruldi Lakes above Mestia in half a day: a steep 4×4 climb to the cross at 2,160 m, then a trek to alpine lakes at 2,750 m with Ushba views. From ₾400 per jeep.",
       price_unit="per jeep, up to 6", dur="half day", dur_hours="3.5–4 h",
       stats=[("from ₾400","per jeep"),("half day","3.5–4 h"),("up to 6","people"),("2,750 m","lakes altitude"),("Ushba","main view")],
       route=[("Departure from Mestia","4×4 jeep, a steep switchback climb above the town."),
              ("Cross above Mestia (2,160 m)","Viewpoint, panorama of Ushba (4,710 m) and the valley."),
              ("Climb to the lakes","Jeep off-road or a short trek — depending on weather and road."),
              ("Koruldi Lakes (2,750 m)","Alpine lakes reflecting the peaks, photos."),
              ("Return drive","Descent by jeep to Mestia."),
              ("Return to Mestia","")],
       map_line="Mestia → cross at 2,160 m → Koruldi Lakes",
       body=[("Koruldi — the best viewpoint in Svaneti","The Koruldi Lakes lie on an alpine plateau at 2,750 metres right above Mestia. From here opens perhaps the most striking view in the region: the twin-headed Ushba (4,710 m), the pyramid of Tetnuldi and the whole Mestia valley at your feet. In calm weather the peaks reflect in the lakes — the postcard image of Svaneti you've seen everywhere."),
             ("The road is an adventure in itself","The climb to Koruldi is one of the steepest jeep routes in Georgia. The 4×4 crawls up the switchbacks from Mestia to the cross at 2,160 metres, and above that real off-road begins. Depending on weather and ground conditions we either drive all the way to the lakes or leave the car at the cross and walk the last stretch (30–40 minutes). An ordinary car simply cannot make this climb."),
             ("Half a day, maximum reward","The whole route takes 3.5–4 hours, so Koruldi is best taken either in the morning or the afternoon, leaving the other half of the day for the <a href=\"../lednik-chalaadi-mestia/\">Chalaadi glacier</a> or a walk around Mestia. It is noticeably colder and windier up top than in town, even at the height of summer: a warm jacket is a must. The cross above Mestia is a draw in itself — many stay to watch the sunset with a view of Ushba.")],
       faq=[("How long is the trip to the Koruldi Lakes?","Half a day — 3.5–4 hours from Mestia and back. Most of the time is the steep jeep climb; up at the lakes and the viewpoint we spend about an hour. The route pairs easily with a second activity the same day."),
            ("Do I have to walk, or is it all by jeep?","It depends on weather and road conditions. In dry weather the 4×4 reaches almost to the lakes. After rain the last stretch is walked from the cross — 30–40 minutes on an easy trail. The guide decides on the spot what is safer."),
            ("What does the ₾400 price include?","₾400 is for the 4×4 for up to 6 people with driver and an English-speaking guide. It's one of the best-value options for a group: for 4–6 people it works out very cheap for a view like this. Personal expenses are extra."),
            ("Why can't we drive up in an ordinary car?","The road to Koruldi is a steep, rocky switchback with off-road above the cross. A regular car can't handle the climb, and after rain it's dangerous even for an unprepared 4×4. We only go in a prepared 4×4 with an experienced driver."),
            ("When is the best view of Ushba?","Ushba is more often clear in the morning and at sunset — during the day the peak is frequently wrapped in cloud. For the best shots we take either an early start or a pre-sunset run: the light on Ushba is at its most expressive then.")],
       tip="Koruldi is about the views, and the views are about the weather. Ushba is temperamental: clear in the morning, in cloud by noon. If the sky is clear, don't wait — go straight up. At 2,750 metres the wind cuts through even in July, so a warm jacket and hat won't go amiss. And allow an extra 20 minutes at the cross above Mestia: many find the view from there stronger than the lakes themselves.",
     ),
     ka=dict(
       h1="კორულდის ტბები მესტიიდან ჯიპით",
       title="კორულდის ტბები მესტიიდან ჯიპით — 400 ₾-დან",
       desc="კორულდის ტბები მესტიის ზემოთ ნახევარ დღეში: 4×4 აღმართი ჯვრამდე 2160 მ და ტრეკი ალპურ ტბებამდე 2750 მ უშბას ხედით. 400 ₾-დან ჯიპზე.",
       price_unit="ჯიპზე, 6 კაცამდე", dur="ნახევარი დღე", dur_hours="3.5–4 სთ",
       stats=[("400 ₾-დან","ჯიპზე"),("ნახევარი დღე","3.5–4 სთ"),("6-მდე","კაცი"),("2750 მ","ტბების სიმაღლე"),("უშბა","მთავარი ხედი")],
       route=[("გამგზავრება მესტიიდან","ჯიპი 4×4, ციცაბო სერპანტინი ქალაქის ზემოთ."),
              ("ჯვარი მესტიის ზემოთ (2160 მ)","სახედავი მოედანი, უშბას (4710 მ) და ხეობის პანორამა."),
              ("აღმართი ტბებამდე","ჯიპი უგზოობაზე ან მოკლე ტრეკი — ამინდისა და გზის მიხედვით."),
              ("კორულდის ტბები (2750 მ)","ალპური ტბები მწვერვალების ანარეკლით, ფოტო."),
              ("უკან გზა","დაშვება ჯიპით მესტიაში."),
              ("დაბრუნება მესტიაში","")],
       map_line="მესტია → ჯვარი 2160 მ → კორულდის ტბები",
       body=[("კორულდი — სვანეთის საუკეთესო სახედავი","კორულდის ტბები დევს ალპურ პლატოზე 2750 მეტრზე პირდაპირ მესტიის ზემოთ. აქედან იშლება, ალბათ, რეგიონის ყველაზე შთამბეჭდავი ხედი: ორთავიანი უშბა (4710 მ), თეთნულდის პირამიდა და მთელი მესტიის ხეობა ხელისგულზე. მშვიდ ამინდში მწვერვალები აირეკლება ტბებში — ეს სვანეთის სავიზიტო ბარათია, რომელიც ყველა ღია ბარათზე გინახავთ."),
             ("გზა — თავად თავგადასავალი","კორულდისკენ აღმართი საქართველოს ერთ-ერთი ყველაზე ციცაბო ჯიპ-მარშრუტია. ჯიპი სერპანტინით ადის მესტიიდან ჯვრამდე 2160 მეტრზე, ხოლო ზემოთ იწყება ნამდვილი უგზოობა. ამინდისა და გრუნტის მდგომარეობის მიხედვით თავად ტბებამდე ან ჯიპით მივდივართ, ან მანქანას ჯვართან ვტოვებთ და ბოლო მონაკვეთს ფეხით გავდივართ (30–40 წუთი). ჩვეულებრივი მანქანა აქ საერთოდ ვერ ადის."),
             ("ნახევარი დღე მაქსიმალური სარგებლით","მთელი მარშრუტი 3.5–4 საათს იკავებს, ამიტომ კორულდის იდეალურად იღებენ ან დილით, ან შუადღის შემდეგ — დღის მეორე ნახევარს კი <a href=\"../lednik-chalaadi-mestia/\">ჭალაადს</a> ან მესტიაში სეირნობას უტოვებენ. ზემოთ შესამჩნევად უფრო ცივა და ქარიანია, ვიდრე ქალაქში, ზაფხულის შუაგულშიც კი: თბილი ქურთუკი აუცილებელია. ჯვარი მესტიის ზემოთ ცალკე მიმზიდველი წერტილია: ბევრი რჩება აქ მზის ჩასვლის შესახვედრად უშბას ხედით.")],
       faq=[("რამდენ ხანს გრძელდება კორულდის ტბებამდე მოგზაურობა?","ნახევარი დღე — 3.5–4 საათი მესტიიდან და უკან. მთავარ დროს იკავებს ციცაბო აღმართი ჯიპით; ზემოთ ტბებთან და სახედავზე დაახლოებით ერთ საათს ვატარებთ. მარშრუტი ადვილად ერწყმის მეორე აქტივობას იმავე დღეს."),
            ("საჭიროა თუ არა ფეხით სვლა თუ ყველაფერი ჯიპითაა?","დამოკიდებულია ამინდსა და გზის მდგომარეობაზე. მშრალ ამინდში ჯიპი თითქმის ტბებამდე ადის. წვიმის შემდეგ ბოლო მონაკვეთს ჯვრიდან ფეხით გადიან — ეს 30–40 წუთია მარტივ ბილიკზე. გიდი ადგილზე წყვეტს რა არის უფრო უსაფრთხო."),
            ("რა შედის 400 ₾ ფასში?","400 ₾ არის ჯიპ 4×4-ზე 6 კაცამდე მძღოლითა და გიდით. ეს ჯგუფისთვის ერთ-ერთი ყველაზე ეკონომიური ვარიანტია: 4–6 კაცზე ძალიან იაფი გამოდის ასეთ ხედში. პირადი ხარჯები — ცალკე."),
            ("რატომ არ შეიძლება ჩვეულებრივი მანქანით ასვლა?","გზა კორულდისკენ ციცაბო, ქვიანი სერპანტინია ჯვრის ზემოთ უგზოობით. მსუბუქი მანქანა ასეთ აღმართს ვერ ძლევს, ხოლო წვიმის შემდეგ ის საშიშია მოუმზადებელი ჯიპისთვისაც. მივდივართ მხოლოდ მომზადებული 4×4-ით გამოცდილი მძღოლით."),
            ("როდისაა უშბას საუკეთესო ხედი?","უშბა უფრო ხშირად ღიაა დილითა და მზის ჩასვლისას — დღისით მწვერვალს ხშირად ღრუბლები ფარავს. საუკეთესო კადრებისთვის ვიღებთ ან ადრეულ გამგზავრებას, ან ჩასვლისწინას: შუქი უშბაზე ამ დროს ყველაზე გამომსახველია.")],
       tip="კორულდი ხედებზეა, ხედები კი ამინდზე. უშბა ახირებულია: დილით სუფთა, შუადღისთვის ღრუბლებში. თუ ცა ნათელია — ნუ გადადებთ, მაშინვე ავიდეთ. ზემოთ 2750 მეტრზე ქარი ატანს ივლისშიც, თბილი ქურთუკი და ქუდი არ დააშავებს. და გაითვალისწინეთ დამატებითი 20 წუთი ჯვართან მესტიის ზემოთ: ბევრი თვლის, რომ ხედი იქიდან თავად ტბებზე ძლიერია.",
     ),
   )),
]

# ============ СБОРКА ============
def stats_html(stats):
    return "".join(f'<div class="stat-item"><span class="stat-val">{v}</span><span class="stat-lab">{l}</span></div>' for v,l in stats)

def route_html(times, route):
    out=[]
    for (name,desc),tm in zip(route, times):
        out.append(f'<div class="route-item"><div class="route-time">{tm}</div>'
                   f'<div><div class="route-name">{name}</div><div class="route-desc">{desc}</div></div></div>')
    return "\n".join(out)

def body_html(body):
    return "\n".join(f'<h2>{h}</h2>\n<p>{p}</p>' for h,p in body)

def faq_html(faq):
    return "\n".join(f'<h3>{q}</h3>\n<p>{a}</p>' for q,a in faq)

def faq_schema(faq):
    items=",".join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'%(_j(q),_j(a)) for q,a in faq)
    return '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}'%items

def stops_json(stops):
    return "["+",".join('{"name": %s, "lat": %s, "lng": %s}'%(_j(n),lat,lng) for n,lat,lng in stops)+"]"

def hreflang_block(slug, canon):
    # полный mesh + x-default -> ru
    ru=f"{BASE}/ekskursiya/{slug}/"
    en=f"{BASE}/en/ekskursiya/{slug}/"
    ka=f"{BASE}/ge/ekskursiya/{slug}/"
    return (f'<link href="{canon}" rel="canonical"/>\n'
            f'<link href="{en}" hreflang="en" rel="alternate"/>'
            f'<link href="{ka}" hreflang="ka" rel="alternate"/>\n'
            f'<link href="{ru}" hreflang="ru" rel="alternate"/>\n'
            f'<link href="{ru}" hreflang="x-default" rel="alternate"/>')

def related_html(slug, lang):
    lt=LINK_TITLES[lang]; ed=L[lang]["exc_dir"]
    chips=[]
    for s in ["lednik-chalaadi-mestia","ushguli-iz-mestii","ushguli-shkhara-lednik","ozero-koruldi-mestia"]:
        if s!=slug:
            chips.append(f'<a href="{ed}{s}/" style="padding:10px 22px;border:1px solid #E5E7EB;border-radius:9999px;font-size:13px;font-weight:600;color:#1A3D2E">{lt[s]}</a>')
    chips.append(f'<a href="{ed}{L[lang]["parent_slug"]}/" style="padding:10px 22px;border:1px solid #E5E7EB;border-radius:9999px;font-size:13px;font-weight:600;color:#1A3D2E">{lt["_svaneti"]}</a>')
    chips.append(f'<a href="{ed}tur-svaneti-4-dnya/" style="padding:10px 22px;border:1px solid #E5E7EB;border-radius:9999px;font-size:13px;font-weight:600;color:#4B5563">{lt["_svaneti4"]}</a>')
    chips.append(f'<a href="{ed}" style="padding:10px 22px;border:1px solid #E5E7EB;border-radius:9999px;font-size:13px;font-weight:600;color:#4B5563">{L[lang]["all_exc"]}</a>')
    return "\n".join(chips)

def build(tour, lang):
    slug=tour["slug"]; d=tour["i18n"][lang]; ui=L[lang]; fr=FRAME[lang]
    prefix, code = LANGS[lang]
    url=f"{BASE}{prefix}/ekskursiya/{slug}/"
    og_locale={"ru":"ru_RU","en":"en_US","ka":"ka_GE"}[lang]
    parent_url=f"{ui['exc_dir']}{ui['parent_slug']}/"
    ge_font=('<link rel="preload" href="/fonts/noto-sans-georgian.woff2" as="font" type="font/woff2" crossorigin>\n'
             '<link rel="stylesheet" href="/css/ge.css">\n' if lang=="ka" else "")
    nav=fr["NAV"].replace("ekskursiya-svaneti-iz-tbilisi", slug)
    tail=fr["TAIL"].replace("ekskursiya-svaneti-iz-tbilisi", slug).replace("от 345 лари", f"{ui['price_from']} {tour['price']} {ui['lari']}")
    schema_webpage='{"@context":"https://schema.org","@type":"WebPage","@id":"%s#webpage","url":"%s","datePublished":"2026-09-01","dateModified":"2026-09-01","inLanguage":"%s","isPartOf":{"@id":"https://sakhva-travel.com/#website"}}'%(url,url,code)
    schema_trip=('{"@context":"https://schema.org","@type":"TouristTrip","inLanguage":"%s","@id":"%s#tour",'
      '"author":{"@type":"Person","name":"Саба","url":"https://sakhva-travel.com/about/saba/","jobTitle":"Гид по Сванетии","knowsAbout":["Сванетия","Местия","Ушгули","треккинг в Грузии"],'
      '"hasCredential":{"@type":"EducationalOccupationalCredential","credentialCategory":"license","name":"Лицензия гида №9332412411",'
      '"recognizedBy":{"@type":"GovernmentOrganization","name":"Georgian National Tourism Administration"}}},'
      '"name":%s,"description":%s,"url":"%s",'
      '"provider":{"@type":"TravelAgency","name":"Sakhva Travel","url":"https://sakhva-travel.com","telephone":"+995511272623"},'
      '"image":"https://sakhva-travel.com/images/%s.jpg","speakable":{"@type":"SpeakableSpecification","cssSelector":["h1","h2"]}}'
      )%(code,url,_j(d["h1"]),_j(d["desc"]),url,tour["img"])
    schema_bc=('{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ['
      '{"@type": "ListItem", "position": 1, "name": "Sakhva Travel", "item": "%s%s/"}, '
      '{"@type": "ListItem", "position": 2, "name": "Excursions", "item": "%s%s/ekskursiya/"}, '
      '{"@type": "ListItem", "position": 3, "name": %s, "item": "%s"}]}')%(BASE,prefix,BASE,prefix,_j(d["h1"]),url)
    schema_product=('{"@context":"https://schema.org","@type":"Product","@id":"%s#product","name":%s,"description":%s,'
      '"brand":{"@type":"Brand","name":"Sakhva Travel"},'
      '"aggregateRating":{"@type":"AggregateRating","ratingValue":4.8,"reviewCount":16,"bestRating":5,"worstRating":1},'
      '"image":"https://sakhva-travel.com/images/%s.jpg","url":"%s",'
      '"offers":{"@type":"Offer","seller":{"@type":"Organization","name":"Sakhva Travel","url":"https://sakhva-travel.com/"},'
      '"price":"%s","priceCurrency":"GEL","availability":"https://schema.org/InStock","priceValidUntil":"2027-12-31","url":"%s","termsOfService":"https://sakhva-travel.com/terms/"}}'
      )%(url,_j(d["h1"]),_j(d["desc"]),tour["img"],url,tour["price"],url)
    short=ui["short_tpl"].format(h1=d["h1"],dur=d["dur"],dh=d["dur_hours"],pf=ui["price_from"],p=tour["price"],unit=d["price_unit"])

    html=f"""<!DOCTYPE html>

<html lang="{code}">
<head><script>window.posthog={{capture:function(){{}},init:function(){{}}}};</script>
<meta charset="utf-8"/>
<link href="/images/favicon-32.png" rel="icon" sizes="32x32" type="image/png"/>
<link href="/images/apple-touch-icon.png" rel="apple-touch-icon" sizes="180x180"/>
<meta content="width=device-width, initial-scale=1.0, viewport-fit=cover" name="viewport"/>
<title>{d['title']}</title>
<meta name="description" content="{d['desc']}"/>
<meta content="Саба — гид по Сванетии, Sakhva Travel" name="author"/>
<meta content="2026-09-01" property="article:published_time"/>
<meta content="2026-09-01" property="article:modified_time"/>
{hreflang_block(slug, url)}
<script src="/js/al.js"></script>
<meta content="website" property="og:type"/>
<meta content="{d['title']}" property="og:title"/>
<meta content="{d['desc']}" property="og:description"/>
<meta content="{url}" property="og:url"/>
<meta content="{og_locale}" property="og:locale"/>
<meta content="Sakhva Travel" property="og:site_name"/>
<meta content="https://sakhva-travel.com/images/{tour['img']}.jpg" property="og:image"/>
<meta content="1200" property="og:image:width"/>
<meta content="630" property="og:image:height"/>
<meta content="Sakhva Travel" property="og:image:alt"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="{d['title']}" name="twitter:title"/>
<meta content="{d['desc']}" name="twitter:description"/>
<meta content="https://sakhva-travel.com/images/{tour['img']}.webp" name="twitter:image"/>
<meta content="index,follow,max-image-preview:large,max-snippet:-1" name="robots"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/><link rel="preconnect" href="https://www.googletagmanager.com" crossorigin><link rel="preconnect" href="https://mc.yandex.ru" crossorigin>
<link as="style" href="/fonts/lora.css?v=2" onload="this.onload=null;this.rel='stylesheet'" rel="preload"/><noscript><link href="/fonts/lora.css?v=2" rel="stylesheet"/></noscript>
{ge_font}
<script>
window.dataLayer=window.dataLayer||[];
function gtag(){{dataLayer.push(arguments)}}
gtag('consent','default',{{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500}})
var _ck=localStorage.getItem('cookies_v4')==='1',_gc=location.search.indexOf('gclid')>-1;
if(_ck||_gc){{
gtag('consent','update',{{analytics_storage:_ck?'granted':'denied',ad_storage:'granted',ad_user_data:'granted',ad_personalization:_ck?'granted':'denied'}})
}}
</script>
<script>(function(){{function loadGA(){{if(window._gaLoaded)return;window._gaLoaded=true;var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-3X83YZHY6S';s.onload=function(){{gtag('js',new Date());gtag('config','G-3X83YZHY6S');gtag('config','AW-8133499399')}};document.head.appendChild(s)}}['scroll','touchstart','mousemove','keydown','click'].forEach(function(e){{document.addEventListener(e,loadGA,{{once:true,passive:true}})}});setTimeout(loadGA,8000)}})()</script>
<script type="application/ld+json">{schema_webpage}</script>
<script type="application/ld+json">{schema_trip}</script>
<script type="application/ld+json">{schema_bc}</script>
{fr['STYLE']}
{NAVFIX_CSS}
<script type="application/ld+json">
{faq_schema(d['faq'])}
</script><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link as="image" fetchpriority="high" href="/images/{tour['img']}.webp?v=2" rel="preload"/>
<link as="image" fetchpriority="high" href="/images/{tour['img']}.webp" rel="preload" type="image/webp"/>
<link as="image" href="/images/geo-hero-kazbegi-1200.webp" media="(min-width:769px)" rel="preload"/>
<link as="image" href="/images/geo-hero-kazbegi-640.webp" media="(max-width:768px)" rel="preload"/>
<script type="application/ld+json">{schema_product}</script>
</head>
<body>
{nav}
<main>
{fr['DRAWER']}
<section class="page-hero">
<img alt="{d['h1']}" fetchpriority="high" height="400" src="/images/{tour['img']}.webp?v=2" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0" width="600"/>
<div class="hero-inner">
<h1 class="hero-h1">{d['h1']}</h1>
<div class="hero-stats">
{stats_html(d['stats'])}
</div>
<div class="hero-btns" style="margin-top:20px;display:flex;gap:12px;flex-wrap:wrap;justify-content:center">
<a class="btn-wa" href="https://wa.me/{WA}?text={slug}" style="padding:14px 28px;font-size:16px;border-radius:9999px;text-decoration:none;box-shadow:0 4px 14px rgba(37,211,102,.35)">{WA_SVG}
        {ui['book_from'].format(p=tour['price'])}</a>
<a class="btn-primary" href="#" onclick="event.preventDefault();openContact()" style="padding:14px 28px;font-size:14px;border-radius:9999px;background:rgba(255,255,255,.15);border:1.5px solid rgba(255,255,255,.5);color:#fff;text-decoration:none;backdrop-filter:blur(8px)">{ui['discount']}</a>
</div>
<div style="margin-top:12px;font-size:13px;color:rgba(255,255,255,.7)">{ui['rating']}</div>
</div></section>
<div class="article-wrap">
<div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:16px;padding:24px;margin:28px 0;text-align:center">
<div style="font-size:32px;font-weight:700;color:#1A3D2E;margin-bottom:4px">{ui['price_from']} {tour['price']} {ui['lari']} <span style="font-size:14px;font-weight:400;color:#6B7280">{d['price_unit']}</span></div>
<div style="font-size:13px;color:#B45309;font-weight:600;margin-bottom:16px">{ui['per_car_note']}</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px">
<div style="background:#fff;border:1px solid #D1FAE5;border-radius:8px;padding:10px 8px;text-align:center"><div style="font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#6B7280;margin-bottom:3px">{ui['lbl_dur']}</div><div style="font-size:13px;font-weight:700;color:#111827">{d['dur_hours']}</div></div>
<div style="background:#fff;border:1px solid #D1FAE5;border-radius:8px;padding:10px 8px;text-align:center"><div style="font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#6B7280;margin-bottom:3px">{ui['lbl_group']}</div><div style="font-size:13px;font-weight:700;color:#111827">6 {ui['people']}</div></div>
<div style="background:#fff;border:1px solid #D1FAE5;border-radius:8px;padding:10px 8px;text-align:center"><div style="font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#6B7280;margin-bottom:3px">{ui['lbl_start']}</div><div style="font-size:13px;font-weight:700;color:#111827">{ui['from_mestia']}</div></div>
<div style="background:#fff;border:1px solid #D1FAE5;border-radius:8px;padding:10px 8px;text-align:center"><div style="font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#6B7280;margin-bottom:3px">{ui['lbl_cancel']}</div><div style="font-size:13px;font-weight:700;color:#111827">{ui['cancel24']}</div></div>
</div>
<a href="/booking/?tour={slug}" style="display:inline-flex;align-items:center;justify-content:center;gap:8px;background:#1A3D2E;color:#fff;padding:16px 40px;border-radius:9999px;font-size:16px;font-weight:700;text-decoration:none;box-shadow:0 4px 14px rgba(26,61,46,.35)">
<svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="18"><rect height="18" rx="2" width="18" x="3" y="4"></rect><line x1="16" x2="16" y1="2" y2="6"></line><line x1="8" x2="8" y1="2" y2="6"></line><line x1="3" x2="21" y1="10" y2="10"></line></svg>
    {ui['book_online']}</a>
<div style="margin-top:10px;font-size:12px;color:#6B7280">{ui['rating']}</div>
</div>
<div class="article-body">
<p>{d['desc']}</p>
<div class="key-fact" style="background:#f0f7f4;border-left:4px solid #2E7D32;padding:16px 20px;margin:20px 0;border-radius:0 8px 8px 0;font-size:16px;line-height:1.6">
<strong>{ui['short']}</strong> {short}
</div></div></div>

<div class="author-byline" style="max-width:800px;margin:0 auto 24px;padding:0 20px">
<img alt="Саба — гид по Сванетии, Sakhva Travel" height="40" loading="lazy" src="/images/saba.webp" width="40"/>
<div class="author-info">
<a class="author-name" href="/about/saba/">Саба · Sakhva Travel</a>
<span class="author-creds">{ui['author_creds']}</span>
</div>
</div>
<section class="section" style="background:#fff">
<div class="sec-inner">
<div class="sec-label">{ui['route_label']}</div>
<h2 class="sec-title">{ui['route_title']}</h2>
<div class="route-grid">
{route_html(tour['route_times'], d['route'])}
</div>
</div>
<div id="tour-route-map" style="margin:18px 0 6px;height:420px;border-radius:12px;overflow:hidden;border:1px solid #E5E7EB;background:#EAEFEA"></div>
<script>
(function(){{
  var el=document.getElementById('tour-route-map');if(!el)return;var booted=false,rendered=false;
  var stops={stops_json(tour['stops'])};
  var dir='https://www.google.com/maps/dir/'+stops.map(function(s){{return s.lat+','+s.lng;}}).join('/');
  function fallback(force){{
    if(rendered&&!force)return;rendered=true;
    el.innerHTML='<a href="'+dir+'" target="_blank" rel="noopener" style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;height:100%;text-decoration:none;color:#1A3D2E;background:#EAEFEA;font-weight:700;font-size:15px;text-align:center;padding:16px">'
      +'<span style="font-size:34px;line-height:1">🗺️</span><span>{ui['map_open']} ↗</span></a>';
  }}
  window.gm_authFailure=function(){{fallback(true);}};
  window.__tourRouteMapInit=function(){{
    try{{
      var map=new google.maps.Map(el,{{zoom:11,mapTypeControl:false,streetViewControl:false,fullscreenControl:true,gestureHandling:'cooperative',clickableIcons:false}});
      new google.maps.Polyline({{path:stops.map(function(s){{return{{lat:s.lat,lng:s.lng}};}}),strokeColor:'#1A3D2E',strokeOpacity:.85,strokeWeight:4,map:map}});
      stops.forEach(function(s,i){{
        new google.maps.Marker({{position:{{lat:s.lat,lng:s.lng}},map:map,label:{{text:String(i+1),color:'#fff',fontWeight:'700',fontSize:'12px'}},icon:{{path:google.maps.SymbolPath.CIRCLE,scale:13,fillColor:'#1A3D2E',fillOpacity:1,strokeColor:'#fff',strokeWeight:2}},zIndex:20+i}});
      }});
      var b=new google.maps.LatLngBounds();stops.forEach(function(s){{b.extend({{lat:s.lat,lng:s.lng}});}});
      map.fitBounds(b,{{top:52,right:80,bottom:36,left:80}});
      rendered=true;
    }}catch(e){{fallback();}}
  }};
  function boot(){{if(booted)return;booted=true;var s=document.createElement('script');s.async=true;s.src='https://maps.googleapis.com/maps/api/js?key={MAPKEY}&callback=__tourRouteMapInit&language={code}&region=GE';s.onerror=fallback;document.head.appendChild(s);setTimeout(fallback,8000);}}
  if('IntersectionObserver' in window){{var io=new IntersectionObserver(function(e){{e.forEach(function(x){{if(x.isIntersecting){{boot();io.disconnect();}}}});}},{{rootMargin:'250px'}});io.observe(el);}}else{{boot();}}
}})();
</script>
<p style="font-size:13px;color:#6B7280;margin:8px 0 0;text-align:center">{ui['route_prefix']} {d['map_line']}</p>
</section>
<div class="article-wrap"><div class="article-body">
{body_html(d['body'])}
<div class="article-body" style="max-width:760px;margin-left:auto;margin-right:auto;padding:0 clamp(16px,3.5vw,32px)">
<h2 class="sec-title" style="text-align:left">{ui['faq_title']}</h2>
{faq_html(d['faq'])}
</div>
<h2>{ui['tip_title']}</h2>
<p>{d['tip']}</p>
<div class="cta-link-box">
<p style="font-size:16px;font-weight:700;color:#111827;margin-bottom:8px">{ui['ready_q']}</p>
<p>{ui['ready_p']}</p>
<a href="/about/">{ui['more_about']}</a>
</div>
</div></div>
<div class="article-cta">
<h3>{ui['cta_h']}</h3>
<p>{ui['cta_p']}</p>
<div class="cta-btns">
<button class="btn-primary" onclick="openContact()" style="cursor:pointer;border:none;font-family:inherit;background:#F59E0B;color:#111;padding:13px 24px;border-radius:9999px;font-size:13px;font-weight:700;color:#111">{ui['discount']}</button>
<a class="btn-wa" href="/booking/?tour={slug}">WhatsApp</a>
<a class="btn-tg" href="https://t.me/SakhvaGuideBot?start=site">Telegram</a>
</div>
</div>
<div style="max-width:720px;margin:40px auto;padding:0 20px;text-align:center">
<p style="font-size:14px;color:#6B7280;margin-bottom:12px">{ui['others']}</p>
<div style="display:flex;flex-wrap:wrap;justify-content:center;gap:10px">
{related_html(slug, lang)}
</div>
</div>
<p style="margin:20px auto;max-width:720px;padding:14px 18px;background:#f0fdf4;border-radius:8px;font-size:14px;color:#374151">{ui['parent_link'].format(u=parent_url)}</p>
{fr['REVIEWS']}
</main>
{fr['FOOTER']}
{tail}
{NAVFIX_JS}
</html>"""
    return html

count=0
for tour in TOURS:
    for lang,(prefix,code) in LANGS.items():
        d = ROOT / (prefix.strip("/") if prefix else "") / "ekskursiya" / tour["slug"]
        d.mkdir(parents=True, exist_ok=True)
        html=build(tour, lang)
        (d/"index.html").write_text(html, encoding="utf-8")
        count+=1
    print(f"OK {tour['slug']}  (ru/en/ka)")
print(f"готово: {count} страниц (4 тура × 3 языка)")
