#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Standalone-генератор статьи «Что подарить из Тбилиси» (RU) / gifts-from-tbilisi (EN).
Отдельный интент от пиллара chto-privezti-iz-gruzii: подарки ПО ПОЛУЧАТЕЛЮ и БЮДЖЕТУ.
Переиспользует ассемблеры blog_content.py и build() из gen_blog.py. Без деплоя.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).parent.parent

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

bc = _load("blog_content", ROOT / "scripts/blog_content.py")
gb = _load("gen_blog", ROOT / "scripts/gen_blog.py")

RU_SLUG = "chto-podarit-iz-tbilisi"
EN_SLUG = "gifts-from-tbilisi"
HERO = "chto-podarit-iz-tbilisi"
PUB = MOD = "2026-07-20"

# ============================ RU ============================
_TOC_RU = bc._toc("Содержание", [
    ("kak-vybrat", "Как выбрать подарок из Грузии"),
    ("zhenshchine", "Что подарить женщине и маме"),
    ("muzhchine", "Что подарить мужчине и папе"),
    ("detyam", "Детям, друзьям и коллегам"),
    ("gurmanu", "Гурману и ценителю вина"),
    ("po-byudzhetu", "Подарки по бюджету: до 20, до 50, премиум"),
    ("gde-kupit", "Где купить подарки в Тбилиси"),
    ("upakovat", "Как упаковать и довезти"),
    ("oshibki", "Каких подарков избегать"),
])

_BODY_RU = (
    '<h2 id="kak-vybrat">Как выбрать подарок из Грузии</h2>\n'
    '<p>За три года в Тбилиси я проводил через сувенирные ряды сотни гостей и заметил простую вещь: хороший подарок из Грузии — это не «магнитик на холодильник», а что-то с историей вкуса или ремесла. Все удачные грузинские подарки делятся на две группы: <strong>съедобные</strong> (вино, чача, чурчхела, специи, чай) и <strong>памятные</strong> (эмаль-минанкари, шёлк, керамика, рог для вина). Съедобное дарят тем, кто любит пробовать; памятное — тем, у кого «всё есть».</p>\n'
    '<p>Разница с обычным списком «что привезти» одна: подарок выбирают <strong>под конкретного человека</strong>, а не просто набирают сувениры себе. Ниже — гид по получателям и бюджету. А если нужен полный каталог всего съедобного и несъедобного, что стоит увезти из страны, он в отдельной статье про <a href="/blog/chto-privezti-iz-gruzii/">что привезти из Грузии →</a>.</p>\n'

    '<h2 id="zhenshchine">Что подарить женщине и маме</h2>\n'
    '<p>Беспроигрышный грузинский подарок женщине — <strong>минанкари</strong> (перегородчатая эмаль). Это украшения ручной работы с ярким рисунком по эмали: кулоны, серьги, браслеты. Выглядят дорого, весят мало, довезти легко. Второй вариант — <strong>палантин</strong> из шёлка или тонкой шерсти с грузинским орнаментом. Мамам обычно заходит съедобно-уютное: варенье из лепестков розы, горный чай из Гурии, косметика на виноградных косточках.</p>\n'
    + bc._t3(["Подарок", "Цена (₾)", "Кому и почему"], [
        ["Украшение минанкари", "40–150", "жене, девушке — эффектно и лаконично"],
        ["Шёлковый палантин / войлок", "30–120", "маме, свекрови — тепло и с орнаментом"],
        ["Косметика с виноградом", "15–40", "уход, натуральный состав"],
        ["Варенье из розы, горный чай", "10–30", "уютный «съедобный» подарок"],
    ]) +
    '\n<div class="info-box"><p>Минанкари продают и в галереях Старого города, и на развес у метро — качество и цена гуляют вдвое. Как отличить ручную работу от штамповки, проще всего понять рядом с тем, кто в этом живёт: на <a href="/ekskursiya/shopping-tur-tbilisi/">шоппинг-туре по Тбилиси</a> я показываю проверенные точки.</p></div>\n'

    '<h2 id="muzhchine">Что подарить мужчине и папе</h2>\n'
    '<p>Мужской грузинский подарок почти всегда крутится вокруг стола. Самое очевидное и самое верное — <strong>чача</strong> (грузинский виноградный самогон) в дизайнерской бутылке или <strong>квеври-вино</strong> красных сортов Саперави. Для любителя застолья — <strong>канци</strong>, рог для вина: настоящий, из рога, а не лакированный сувенир. Папам и старшим часто дарят нарды ручной работы или грузинский нож.</p>\n'
    + bc._t3(["Подарок", "Цена (₾)", "Кому и почему"], [
        ["Чача в подарочной бутылке", "25–80", "крепкий сувенир с характером"],
        ["Квеври-вино Саперави", "20–60", "ценителю красного, довезти в чемодане"],
        ["Рог для вина канци", "20–90", "любителю застолья и тостов"],
        ["Нарды ручной работы", "40–150", "папе, тестю — надолго"],
    ]) +
    '\n<p>Про чачу — что это, как выбрать и не купить крашеный спирт — есть отдельный разбор: <a href="/blog/chacha-gruzinskaya/">грузинская чача →</a>. А как читаются этикетки вина и чем квеври отличается от обычного — в гиде по <a href="/blog/gruzinskoe-vino-gid/">грузинскому вину →</a>.</p>\n'

    '<h2 id="detyam">Детям, друзьям и коллегам</h2>\n'
    '<p>Детям почти всегда дарят вкусное и яркое: <strong>чурчхелу</strong> (орехи в загустевшем виноградном соке), пастилу тклапи, деревянные игрушки. Друзьям и коллегам, когда нужно много и недорого, идеальны <strong>наборы специй</strong> (сванская соль, хмели-сунели, аджика) и мини-бутылочки вина или чачи — компактно, съедобно, у всех разное. Магнит-эмаль вместо китайского пластика тоже читается как «подумали».</p>\n'
    + bc._t3(["Кому", "Что подарить", "Цена (₾)"], [
        ["Детям", "чурчхела, тклапи, деревянные игрушки", "5–30"],
        ["Коллегам (много)", "наборы специй, мини-вино", "5–20 за шт."],
        ["Друзьям", "чача-мини, магнит-минанкари, чай", "10–35"],
    ]) +
    '\n<div class="info-box"><p>Чурчхела бывает свежая и «резиновая» — на рынке легко попасть на несвежую. Как выбрать и чем грузинские сладости отличаются друг от друга, разобрал тут: <a href="/blog/gruzinskie-sladosti/">грузинские сладости →</a>.</p></div>\n'

    '<h2 id="gurmanu">Гурману и ценителю вина</h2>\n'
    '<p>Если человек разбирается, обычная бутылка из супермаркета не впечатлит. Дарите <strong>квеври-вино в деревянном боксе</strong> или мини-набор для дегустации из 3–4 сортов (Саперави, Ркацители, Киси, Оджалеши). К вину хорошо идёт <strong>ткемали</strong> (кислый сливовый соус) и грузинское оливковое или ореховое масло. Гурману-коллекционеру — керамическая мини-квеври или глиняный кувшин.</p>\n'
    '<p>Такой подарок лучше выбирать в винотеке, а не в сувенирной лавке: там подскажут регион и год. Ещё вернее — привезти впечатление: <a href="/ekskursiya/gastronomicheskiy-tur-tbilisi/">гастрономический тур</a> с дегустацией у винодела, откуда человек увозит бутылку с историей, а не просто этикетку.</p>\n'

    '<h2 id="po-byudzhetu">Подарки по бюджету: до 20, до 50, премиум</h2>\n'
    '<p>Быстрая шпаргалка, если ориентируетесь на сумму, а не на человека. Цены здесь и во всех таблицах — ориентир на 2026 год в лари (₾); на рынках торг сбивает 10–20%, в туристических лавках Старого города дороже.</p>\n'
    + bc._t3(["Бюджет", "Что взять", "Кому"], [
        ["до 20 ₾", "специи, чай, чурчхела, магнит-эмаль", "коллегам, друзьям, «на всех»"],
        ["20–50 ₾", "чача, вино, косметика, палантин", "родителям, друзьям поближе"],
        ["50 ₾ и выше", "минанкари, нарды, рог, вино-бокс", "жене, мужу, важному человеку"],
    ]) +
    '\n<p>Общее правило: <strong>лучше один осмысленный подарок, чем пять магнитиков</strong>. Грузинское съедобное стоит недорого, поэтому даже в бюджете до 20 ₾ можно собрать красивый набор.</p>\n'

    '<h2 id="gde-kupit">Где купить подарки в Тбилиси</h2>\n'
    '<p>Место решает не меньше, чем сам подарок — цена и качество на одну и ту же вещь гуляют в разы.</p>\n'
    + bc._t3(["Место", "За чем идти", "Нюанс"], [
        ["Сухой мост (блошиный рынок)", "винтаж, антиквариат, «памятное»", "торг обязателен"],
        ["Дезертирский базар", "специи, чурчхела, сыр, орехи", "съедобное, свежее, дёшево"],
        ["Галереи Старого города / Шардени", "минанкари, керамика, шёлк", "качество выше, цена тоже"],
        ["Винотеки (ул. Эрекле II)", "подарочное вино и чача", "подскажут регион и год"],
    ]) +
    '\n<p>Если времени в обрез, а подарков нужно много, удобнее пройти всё за один заход с тем, кто знает точки. По дороге заодно посмотрите сам город — маршрут пересекается с <a href="/blog/chto-posmotret-v-tbilisi/">главными местами Тбилиси →</a>.</p>\n'

    '<h2 id="upakovat">Как упаковать и довезти</h2>\n'
    '<p>Три вещи, из-за которых подарки чаще всего страдают в дороге:</p>\n'
    '<ul>\n'
    '<li><strong>Вино и чача — только в багаж.</strong> В ручную кладь жидкости свыше 100 мл не пустят. Бутылки обмотайте одеждой или купите пузырчатую плёнку на рынке.</li>\n'
    '<li><strong>Чурчхела и сыр — в вакуум или плотный пакет.</strong> Чурчхела не тает, но пачкается; сыр лучше сулугуни в вакуумной упаковке.</li>\n'
    '<li><strong>Минанкари и керамика — в ручную кладь.</strong> Хрупкое лучше держать при себе, эмаль почти невесома.</li>\n'
    '</ul>\n'
    '<p>Сколько бутылок вина можно вывозить без пошлины и какие есть таможенные нюансы — это подробно в разделе про вывоз в статье <a href="/blog/chto-privezti-iz-gruzii/">что привезти из Грузии →</a>.</p>\n'

    '<h2 id="oshibki">Каких подарков избегать</h2>\n'
    '<ul>\n'
    '<li><strong>Пластиковые магниты «made in China».</strong> Их продают у любой достопримечательности — это не грузинский подарок. Берите магнит-минанкари.</li>\n'
    '<li><strong>Вино из супермаркета в подарок ценителю.</strong> Массовое полусладкое — не то, чем стоит представлять Грузию. Идите в винотеку.</li>\n'
    '<li><strong>Безымянная «сванская соль» из туристической лавки.</strong> Часто это обычная соль с красителем. Специи берите на Дезертирском рынке.</li>\n'
    '<li><strong>Лакированный «рог».</strong> Настоящий канци — из рога и без глянцевого лака; сувенирная пластиковая имитация выдаёт себя весом.</li>\n'
    '</ul>\n'
    '<p>И последнее: самый ценный подарок из Тбилиси — это впечатление. Часто гости увозят не только чемодан вкусного, но и день, проведённый в городе с гидом. Как это устроить — ниже.</p>'
)

_FAQ_PAIRS_RU = [
    ("Что подарить мужчине из Грузии?",
     "Беспроигрышно — чача в дизайнерской бутылке (25–80 ₾) или квеври-вино Саперави (20–60 ₾). Любителю застолья — настоящий рог для вина канци, папе — нарды ручной работы или грузинский нож."),
    ("Что недорого подарить из Тбилиси?",
     "До 20 ₾ отлично заходят наборы специй (сванская соль, хмели-сунели, аджика), горный чай, чурчхела и магнит-минанкари вместо китайского пластика. Идеально для коллег и друзей «на всех»."),
    ("Что подарить женщине из Грузии?",
     "Украшения минанкари (перегородчатая эмаль, 40–150 ₾) — эффектно и легко везти. Также шёлковый палантин с орнаментом, косметика на виноградных косточках, варенье из лепестков розы."),
    ("Можно ли вывозить вино и чачу в подарок?",
     "Да, но только в багаже — в ручную кладь жидкости свыше 100 мл не пропустят. Есть беспошлинные нормы на вывоз алкоголя; детали и таможенные лимиты — в статье «что привезти из Грузии»."),
    ("Где в Тбилиси купить подарки?",
     "Съедобное (специи, чурчхела, сыр) — на Дезертирском базаре; минанкари и керамику — в галереях Старого города и на Шардени; винтаж и антиквариат — на блошином рынке у Сухого моста; подарочное вино — в винотеках на улице Эрекле II."),
]
_FAQ_RU = bc._faq("Частые вопросы", _FAQ_PAIRS_RU)

_CARDS_RU = bc._cards([
    ("Гайд", "Что привезти из Грузии", "Полный каталог сувениров: еда, вино, вещи, таможня.", "/blog/chto-privezti-iz-gruzii/", "Читать →"),
    ("Гайд", "Грузинские сладости", "Чурчхела, пеламуши, козинаки — что и где брать.", "/blog/gruzinskie-sladosti/", "Читать →"),
    ("Тур", "Шоппинг-тур по Тбилиси", "Проверенные точки за подарками и сувенирами с гидом.", "/ekskursiya/shopping-tur-tbilisi/", "Подробнее →"),
])

_READALSO_RU = bc._readalso("Читайте также:", [
    ("/blog/chto-privezti-iz-gruzii/", "Что привезти из Грузии: 20 идей и таможня →"),
    ("/blog/gruzinskoe-vino-gid/", "Грузинское вино: как выбрать и не ошибиться →"),
    ("/blog/chacha-gruzinskaya/", "Грузинская чача: что это и как выбрать →"),
    ("/tury-v-gruziyu/", "Туры в Грузию 2026 — полный гид →"),
])

# ============================ EN ============================
_TOC_EN = bc._toc("Contents", [
    ("how-to-pick", "How to pick a gift from Georgia"),
    ("for-her", "Gifts for her and mum"),
    ("for-him", "Gifts for him and dad"),
    ("kids-friends", "Kids, friends and colleagues"),
    ("foodie", "For a foodie or wine lover"),
    ("by-budget", "Gifts by budget: under 20, under 50, premium"),
    ("where", "Where to buy gifts in Tbilisi"),
    ("pack", "How to pack and carry them home"),
    ("avoid", "Gifts to avoid"),
])

_BODY_EN = (
    '<h2 id="how-to-pick">How to pick a gift from Georgia</h2>\n'
    '<p>After three years in Tbilisi and hundreds of guests walked through the souvenir rows, I noticed one thing: a good Georgian gift isn\'t a fridge magnet — it\'s something with a story of taste or craft. Every worthwhile Georgian gift falls into two groups: <strong>edible</strong> (wine, chacha, churchkhela, spices, tea) and <strong>keepsake</strong> (minankari enamel, silk, ceramics, a wine horn). Edible suits people who love to try things; keepsakes suit those who "have everything".</p>\n'
    '<p>The difference from a plain "what to bring back" list is simple: a gift is chosen <strong>for a specific person</strong>, not just piled up for yourself. Below is a guide by recipient and by budget. If you want the full catalogue of everything worth taking out of the country, see the separate guide on <a href="/en/blog/what-to-buy-in-georgia/">what to buy in Georgia →</a>.</p>\n'

    '<h2 id="for-her">Gifts for her and mum</h2>\n'
    '<p>The safe Georgian gift for a woman is <strong>minankari</strong> — cloisonné enamel jewellery. Handmade pendants, earrings and bracelets with bright enamel patterns: they look expensive, weigh almost nothing and travel easily. A close second is a <strong>silk or fine-wool scarf</strong> with a Georgian ornament. For mums, cosy-edible usually wins: rose-petal jam, mountain tea from Guria, grape-seed cosmetics.</p>\n'
    + bc._t3(["Gift", "Price (₾)", "Who and why"], [
        ["Minankari jewellery", "40–150", "wife, girlfriend — striking yet simple"],
        ["Silk scarf / felt", "30–120", "mum — warm, with an ornament"],
        ["Grape-seed cosmetics", "15–40", "natural skincare"],
        ["Rose jam, mountain tea", "10–30", "a cosy edible gift"],
    ]) +
    '\n<div class="info-box"><p>Minankari is sold both in Old Town galleries and loose near the metro — quality and price can differ twofold. The easiest way to tell handmade from stamped is beside someone who lives here: on a <a href="/en/tours-in-georgia/">Tbilisi tour</a> I point out the trusted spots.</p></div>\n'

    '<h2 id="for-him">Gifts for him and dad</h2>\n'
    '<p>A men\'s Georgian gift almost always revolves around the table. The obvious and reliable choice is <strong>chacha</strong> (Georgian grape spirit) in a designer bottle, or <strong>qvevri wine</strong> made from red Saperavi. For a lover of feasts — a <strong>kantsi</strong>, a real drinking horn made of horn, not a lacquered souvenir. For dads, handmade backgammon or a Georgian knife go a long way.</p>\n'
    + bc._t3(["Gift", "Price (₾)", "Who and why"], [
        ["Chacha in a gift bottle", "25–80", "a strong souvenir with character"],
        ["Qvevri Saperavi wine", "20–60", "for a red-wine lover, packs in a case"],
        ["Kantsi drinking horn", "20–90", "for someone who loves a toast"],
        ["Handmade backgammon", "40–150", "for dad, father-in-law — lasting"],
    ]) +
    '\n<p>What chacha actually is and how to avoid dyed spirit is covered here: <a href="/en/blog/georgian-wine-guide/">Georgian wine and spirits guide →</a>, where you\'ll also learn how qvevri wine differs from the usual bottle.</p>\n'

    '<h2 id="kids-friends">Kids, friends and colleagues</h2>\n'
    '<p>For kids, go tasty and colourful: <strong>churchkhela</strong> (nuts in thickened grape juice), tklapi fruit leather, wooden toys. For friends and colleagues, when you need a lot for a little, <strong>spice sets</strong> (Svan salt, khmeli-suneli, ajika) and mini bottles of wine or chacha are ideal — compact, edible, and different for everyone. An enamel magnet instead of Chinese plastic also reads as "they thought about it".</p>\n'
    + bc._t3(["For", "Gift", "Price (₾)"], [
        ["Kids", "churchkhela, tklapi, wooden toys", "5–30"],
        ["Colleagues (many)", "spice sets, mini wine", "5–20 each"],
        ["Friends", "mini chacha, enamel magnet, tea", "10–35"],
    ]) +
    '\n<div class="info-box"><p>Churchkhela can be fresh or "rubbery" — it\'s easy to get a stale one at the market. How to choose it and how Georgian sweets differ is here: <a href="/en/blog/georgian-sweets-desserts/">Georgian sweets and desserts →</a>.</p></div>\n'

    '<h2 id="foodie">For a foodie or wine lover</h2>\n'
    '<p>If the person knows their stuff, a supermarket bottle won\'t impress. Give <strong>qvevri wine in a wooden box</strong> or a mini tasting set of 3–4 varieties (Saperavi, Rkatsiteli, Kisi, Ojaleshi). Wine pairs well with <strong>tkemali</strong> (sour plum sauce) and Georgian olive or walnut oil. For a collector — a ceramic mini-qvevri or a clay jug.</p>\n'
    '<p>Buy this at a wine shop rather than a souvenir stall: they\'ll advise on region and vintage. Better still, bring back an experience — a <a href="/en/tours-in-georgia/">food tour</a> with a tasting at the winery, so the person leaves with a bottle that has a story, not just a label.</p>\n'

    '<h2 id="by-budget">Gifts by budget: under 20, under 50, premium</h2>\n'
    '<p>A quick cheat sheet if you\'re working to a sum rather than a person. Prices here and in every table are a 2026 guide in Georgian lari (₾); haggling at markets knocks off 10–20%, and tourist stalls in the Old Town run higher.</p>\n'
    + bc._t3(["Budget", "What to get", "For whom"], [
        ["under 20 ₾", "spices, tea, churchkhela, enamel magnet", "colleagues, friends, \"for everyone\""],
        ["20–50 ₾", "chacha, wine, cosmetics, scarf", "parents, closer friends"],
        ["50 ₾ and up", "minankari, backgammon, horn, wine box", "wife, husband, someone important"],
    ]) +
    '\n<p>The general rule: <strong>one meaningful gift beats five magnets</strong>. Georgian edibles are cheap, so even under 20 ₾ you can put together a nice set.</p>\n'

    '<h2 id="where">Where to buy gifts in Tbilisi</h2>\n'
    '<p>The place matters as much as the gift — price and quality for the same item can differ several times over.</p>\n'
    + bc._t3(["Place", "What for", "Note"], [
        ["Dry Bridge flea market", "vintage, antiques, keepsakes", "haggling expected"],
        ["Dezerter Bazaar", "spices, churchkhela, cheese, nuts", "edible, fresh, cheap"],
        ["Old Town / Shardeni galleries", "minankari, ceramics, silk", "higher quality, higher price"],
        ["Wine shops (Erekle II St.)", "gift wine and chacha", "advice on region and vintage"],
    ]) +
    '\n<p>Short on time and long on gift lists? It\'s easier to cover everything in one pass with someone who knows the spots. Fresh food and produce are best bought last, on your way out — see the <a href="/en/blog/what-to-buy-in-georgia/">full souvenir list</a> for what keeps and what doesn\'t.</p>\n'

    '<h2 id="pack">How to pack and carry them home</h2>\n'
    '<ul>\n'
    '<li><strong>Wine and chacha go in checked luggage only.</strong> Liquids over 100 ml aren\'t allowed in carry-on. Wrap bottles in clothes or buy bubble wrap at the market.</li>\n'
    '<li><strong>Churchkhela and cheese — vacuum-pack or seal them.</strong> Churchkhela doesn\'t melt but does stain; go for vacuum-packed sulguni cheese.</li>\n'
    '<li><strong>Minankari and ceramics — in your carry-on.</strong> Keep fragile things with you; enamel weighs almost nothing.</li>\n'
    '</ul>\n'
    '<p>How many bottles of wine you can take out duty-free and the customs details are covered in the <a href="/en/blog/what-to-buy-in-georgia/">what to buy in Georgia guide →</a>.</p>\n'

    '<h2 id="avoid">Gifts to avoid</h2>\n'
    '<ul>\n'
    '<li><strong>Plastic "made in China" magnets.</strong> Sold at every landmark — that\'s not a Georgian gift. Get an enamel magnet instead.</li>\n'
    '<li><strong>Supermarket wine for a connoisseur.</strong> Mass semi-sweet isn\'t how you want to represent Georgia. Go to a wine shop.</li>\n'
    '<li><strong>Nameless "Svan salt" from a tourist stall.</strong> Often just salt with dye. Buy spices at Dezerter Bazaar.</li>\n'
    '<li><strong>A lacquered "horn".</strong> A real kantsi is made of horn without glossy varnish; a plastic imitation gives itself away by weight.</li>\n'
    '</ul>\n'
    '<p>One last thing: the most valuable gift from Tbilisi is an experience. Guests often take home not just a suitcase of food but a day spent in the city with a guide. Here\'s how to arrange it.</p>'
)

_FAQ_PAIRS_EN = [
    ("What gift to bring a man from Georgia?",
     "A safe pick is chacha in a designer bottle (25–80 ₾) or qvevri Saperavi wine (20–60 ₾). For a feast lover — a real kantsi drinking horn; for dad — handmade backgammon or a Georgian knife."),
    ("What is a cheap gift from Tbilisi?",
     "Under 20 ₾, spice sets (Svan salt, khmeli-suneli, ajika), mountain tea, churchkhela and an enamel magnet instead of Chinese plastic work well. Ideal for colleagues and friends \"for everyone\"."),
    ("What gift to bring a woman from Georgia?",
     "Minankari jewellery (cloisonné enamel, 40–150 ₾) — striking and easy to carry. Also a silk scarf with an ornament, grape-seed cosmetics, or rose-petal jam."),
    ("Can I take wine and chacha as a gift?",
     "Yes, but in checked luggage only — liquids over 100 ml aren't allowed in carry-on. There are duty-free allowances for alcohol; details and limits are in the what to buy in Georgia guide."),
    ("Where can I buy gifts in Tbilisi?",
     "Edibles (spices, churchkhela, cheese) at Dezerter Bazaar; minankari and ceramics in Old Town and Shardeni galleries; vintage and antiques at the Dry Bridge flea market; gift wine in the wine shops on Erekle II Street."),
]
_FAQ_EN = bc._faq("FAQ", _FAQ_PAIRS_EN)

_CARDS_EN = bc._cards([
    ("Guide", "What to buy in Georgia", "The full catalogue of souvenirs — food, wine, crafts and customs.", "/en/blog/what-to-buy-in-georgia/", "Read →"),
    ("Guide", "Georgian sweets", "Churchkhela, pelamushi, kozinaki — what to buy and where.", "/en/blog/georgian-sweets-desserts/", "Read →"),
    ("Tour", "Tbilisi tour", "Cover the trusted gift spots and the city with a local guide.", "/en/tours-in-georgia/", "Details →"),
])

_READALSO_EN = bc._readalso("Read also:", [
    ("/en/blog/what-to-buy-in-georgia/", "What to buy in Georgia: 20 souvenir ideas →"),
    ("/en/blog/georgian-wine-guide/", "Georgian wine: how to choose and not go wrong →"),
    ("/en/blog/georgian-sweets-desserts/", "Georgian sweets and desserts →"),
    ("/en/tours-in-georgia/", "Georgia tours with a guide →"),
])

# ============================ ARTICLE ============================
ART = {
    "ru_slug": RU_SLUG, "en_slug": EN_SLUG,
    "ru": {
        "title": "Что подарить из Тбилиси 2026: подарки родным и друзьям",
        "desc": "Что подарить из Тбилиси: гид по подаркам по получателю и бюджету — женщине, мужчине, детям, коллегам. Идеи, цены в лари и где купить в Тбилиси.",
        "keywords": "что подарить из тбилиси, подарок из грузии, что подарить из грузии, грузинские подарки, подарок из тбилиси женщине, подарок мужчине грузия, сувениры тбилиси",
        "hero": HERO, "pub": PUB, "mod": MOD,
        "schema": bc.build_schema(
            "ru", RU_SLUG, EN_SLUG,
            "Что подарить из Тбилиси 2026: подарки родным и друзьям",
            "Что подарить из Тбилиси: гид по подаркам по получателю и бюджету — женщине, мужчине, детям, коллегам. Идеи, цены в лари и где купить в Тбилиси.",
            HERO, PUB, MOD, "Что подарить из Тбилиси", _FAQ_PAIRS_RU),
        "body": bc.ru_region(
            "Что подарить из Тбилиси", 9,
            "Что подарить из Тбилиси: гид по подаркам — кому, что и за сколько",
            "20 июля 2026",
            "<strong>Что подарить из Тбилиси</strong> — вопрос сложнее, чем «что привезти себе»: подарок выбирают под конкретного человека. Я живу в Тбилиси с 2023 года и каждую неделю провожу гостей по сувенирным рядам. Собрал гид по получателям и бюджету: что подарить женщине, мужчине, детям и коллегам, сколько это стоит в лари и где в Тбилиси купить, чтобы не переплатить и не нарваться на штамповку.",
            _TOC_RU, _BODY_RU,
            "Хотите выбрать подарки за один заход и увидеть город?",
            "Пройдём проверенные точки за сувенирами и посмотрим Тбилиси. Группа до 7 человек, трансфер от отеля.",
            "/ekskursiya/shopping-tur-tbilisi/", "Подробнее о туре →",
            "Хочу+шоппинг-тур+по+Тбилиси", "/tury-v-gruziyu/",
            _READALSO_RU, _CARDS_RU, _FAQ_RU,
        ),
    },
    "en": {
        "title": "Gifts from Tbilisi 2026: Ideas for Family & Friends",
        "desc": "What to bring home from Tbilisi: a Georgian gift guide by recipient and budget — for her, him, kids and colleagues. Ideas, prices in lari and where to buy.",
        "keywords": "gifts from tbilisi, georgian gifts, what to bring from georgia, gift from georgia, souvenirs tbilisi, georgian souvenirs, present from tbilisi",
        "hero": HERO, "pub": PUB, "mod": MOD,
        "schema": bc.build_schema(
            "en", RU_SLUG, EN_SLUG,
            "Gifts from Tbilisi 2026: Ideas for Family & Friends",
            "What to bring home from Tbilisi: a Georgian gift guide by recipient and budget — for her, him, kids and colleagues. Ideas, prices in lari and where to buy.",
            HERO, PUB, MOD, "Gifts from Tbilisi", _FAQ_PAIRS_EN),
        "body": bc.en_region(
            "Gifts from Tbilisi", 9,
            "Gifts from Tbilisi: A Georgian Gift Guide by Recipient & Budget",
            "July 20, 2026",
            "<strong>Gifts from Tbilisi</strong> are a trickier question than \"what to bring back for yourself\" — a gift is chosen for a specific person. I've lived in Tbilisi since 2023 and walk guests through the souvenir rows every week. Here's a guide by recipient and budget: what to bring for her, him, kids and colleagues, what it costs in lari, and where to buy in Tbilisi so you don't overpay or end up with stamped-out kitsch.",
            _TOC_EN, _BODY_EN,
            "Want to pick your gifts in one pass and see the city?",
            "We'll cover the trusted souvenir spots and explore Tbilisi. Groups up to 7, hotel pickup.",
            "/en/tours-in-georgia/", "Tour details →",
            "I+want+a+Tbilisi+shopping+tour", "/en/booking/",
            _READALSO_EN, _CARDS_EN, _FAQ_EN,
        ),
    },
}

if __name__ == "__main__":
    for lg in ("ru", "en"):
        ART[lg]["ru_slug"] = RU_SLUG
        ART[lg]["en_slug"] = EN_SLUG
    n_ru = gb.build(gb.TPL_RU, ROOT / f"blog/{RU_SLUG}/index.html", ART["ru"], "ru")
    n_en = gb.build(gb.TPL_EN, ROOT / f"en/blog/{EN_SLUG}/index.html", ART["en"], "en")
    print(f"RU blog/{RU_SLUG}: {n_ru}b")
    print(f"EN en/blog/{EN_SLUG}: {n_en}b")
