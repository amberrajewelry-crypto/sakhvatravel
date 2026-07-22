# -*- coding: utf-8 -*-
"""Контент блог-статей Sakhva для gen_blog.py.
Ассемблеры воспроизводят точный скелет эталона (gruziya-perviy-raz / georgia-first-time-tips):
head-meta и schema генерирует gen_blog.py, здесь — тело региона (body) + мета-поля.
"""
import json

BASE = "https://sakhva-travel.com"

# ---------- ВЕРБАТИМ-БОИЛЕРПЛЕЙТ (идентичен эталону) ----------
BYLINE_RU = (
    '<div class="author-byline">\n'
    '<img alt="Тимур — автор туров по Грузии" height="40" loading="lazy" src="/images/timur.webp" width="40"/>\n'
    '<div class="author-info">\n'
    '<a class="author-name" href="/about/">Тимур · Sakhva Travel</a>\n'
    '<span class="author-creds">Индивидуальная экскурсия с 2023 · 500+ туров · 4.9/5 рейтинг</span>\n'
    '</div>\n</div>\n'
    '<div class="blog-discount-btn" style="text-align:center;margin:16px 0 8px">\n'
    '<a href="/booking/" style="display:inline-block;padding:12px 28px;font-size:14px;font-weight:600;letter-spacing:0.5px;border-radius:9999px;background:#1A3D2E;color:#fff;text-decoration:none;transition:opacity .2s">Забронировать экскурсию</a>\n'
    '</div>'
)
BYLINE_EN = (
    '<div class="author-byline">\n'
    '<img alt="Timur — Georgia tour author" height="40" loading="lazy" src="/images/timur.webp" width="40"/>\n'
    '<div class="author-info">\n'
    '<a class="author-name" href="/en/about/">Timur · Sakhva Travel</a>\n'
    '<span class="author-creds">Guiding in Georgia since 2023 · 500+ tours · 4.9/5 rating</span>\n'
    '</div>\n</div>\n'
    '<div class="blog-discount-btn" style="text-align:center;margin:16px 0 8px">\n'
    '<a href="/en/booking/" style="display:inline-block;padding:12px 28px;font-size:14px;font-weight:600;letter-spacing:0.5px;border-radius:9999px;background:#1A3D2E;color:#fff;text-decoration:none;transition:opacity .2s">Book a tour</a>\n'
    '</div>'
)
TRIPADV_RU = (
    '<div style="max-width:800px;margin:32px auto;padding:20px 24px;background:#f0fdf4;border-radius:12px;border:1px solid #bbf7d0;display:flex;align-items:center;gap:16px;flex-wrap:wrap">\n'
    '<div style="flex:1;min-width:200px">\n'
    '<p style="margin:0 0 4px;font-size:16px;font-weight:700;color:#111827">Рейтинг 4.9 из 5 на TripAdvisor</p>\n'
    '<p style="margin:0;font-size:13px;color:#6B7280">90+ отзывов от туристов, которые уже побывали на экскурсиях с Тимуром</p>\n'
    '</div>\n'
    '<a href="https://www.tripadvisor.ru/Attraction_Review-g294195-d15318013-Reviews-Sakhva_Travel-Tbilisi.html" rel="noopener" style="display:inline-flex;align-items:center;gap:8px;padding:10px 20px;background:#00AA6C;color:#fff;font-size:13px;font-weight:700;border-radius:9999px;text-decoration:none;white-space:nowrap" target="_blank">Читать отзывы</a>\n'
    '</div>'
)
TRIPADV_EN = (
    '<div style="max-width:800px;margin:32px auto;padding:20px 24px;background:#f0fdf4;border-radius:12px;border:1px solid #bbf7d0;display:flex;align-items:center;gap:16px;flex-wrap:wrap">\n'
    '<div style="flex:1;min-width:200px">\n'
    '<p style="margin:0 0 4px;font-size:16px;font-weight:700;color:#111827">Rated 4.9/5 on TripAdvisor</p>\n'
    '<p style="margin:0;font-size:13px;color:#6B7280">90+ reviews from travelers who have already toured with Timur</p>\n'
    '</div>\n'
    '<a href="https://www.tripadvisor.com/Attraction_Review-g294195-d15318013-Reviews-Sakhva_Travel-Tbilisi.html" rel="noopener" style="display:inline-flex;align-items:center;gap:8px;padding:10px 20px;background:#00AA6C;color:#fff;font-size:13px;font-weight:700;border-radius:9999px;text-decoration:none;white-space:nowrap" target="_blank">Read Reviews</a>\n'
    '</div>'
)


def _t3(headers, rows):
    """Универсальная таблица 3 колонки (price-table)."""
    h = "".join(f"<th>{x}</th>" for x in headers)
    body = "\n".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="price-table">\n<thead><tr>{h}</tr></thead>\n<tbody>\n{body}\n</tbody>\n</table>'


def _toc(title, items):
    """items: list of (anchor, text)"""
    ls = "\n".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in items)
    return f'<nav class="article-toc">\n<p class="toc-hd">{title}</p>\n<ol>\n{ls}\n</ol>\n</nav>'


def _cards(cards):
    """cards: list of (label, h3, p, href, cta)"""
    items = "\n".join(
        f'<div class="rc-card">\n<div class="rc-card-label">{lb}</div>\n'
        f'<h3>{h}</h3>\n<p>{p}</p>\n<a href="{href}">{cta}</a>\n</div>'
        for lb, h, p, href, cta in cards
    )
    return f'<section class="related">\n<div class="related-grid">\n{items}\n</div>\n</section>'


def _readalso(title, links):
    """links: list of (href, text)"""
    ls = "\n".join(
        f'<a href="{href}" style="display:block;color:#1A3D2E;padding:4px 0">{t}</a>'
        for href, t in links
    )
    return (
        '<div style="background:#F9FAFB;border-radius:12px;padding:20px 24px;margin:32px 0">\n'
        f'<p style="font-weight:700;margin-bottom:8px">{title}</p>\n{ls}\n</div>'
    )


def _faq(fid_title, pairs):
    items = "\n".join(
        f'<div class="fi">\n<button class="fq" onclick="toggleFaq(this)">{q}<span class="fq-ic">+</span></button>\n'
        f'<div class="fa"><div class="fa-inner">{a}</div></div>\n</div>'
        for q, a in pairs
    )
    return (
        f'<section id="faq">\n<div class="faq-inner">\n<h2>{fid_title}</h2>\n{items}\n</div>\n</section>'
    )


def ru_region(bc_last, read_min, h1, date_line, lead, toc, body, cta_h3, cta_p,
              cta_url, cta_label, cta_wa_text, planiruete_url, readalso, cards, faq):
    return (
        '<div id="content-ru">\n'
        '<header class="article-hero">\n'
        '<div class="breadcrumb">\n'
        '<a href="/">Главная</a><span>/</span>\n'
        '<a href="/blog/">Блог</a><span>/</span>\n'
        f'<span>{bc_last}</span>\n'
        '</div>\n'
        f'<div class="article-label">Гайд · {read_min} мин чтения</div>\n'
        f'<h1 class="article-h1">{h1}</h1>\n'
        '<div class="article-meta">\n'
        f'<span>{date_line}</span>\n'
        '<span>Тимур · Sakhva Travel</span>\n'
        '</div>\n</header>\n'
        '<article>\n<div class="article-wrap">\n'
        f'{BYLINE_RU}\n'
        f'<p class="article-lead">{lead}</p>\n'
        f'{toc}\n'
        '<div class="article-body">\n'
        f'{body}\n'
        '<div class="article-cta">\n'
        f'<h3>{cta_h3}</h3>\n<p>{cta_p}</p>\n'
        '<div class="cta-btns">\n'
        f'<a class="btn-wa" href="{cta_url}">{cta_label}</a>\n'
        f'<a class="btn-tg" href="https://wa.me/995511272623?text={cta_wa_text}">WhatsApp</a>\n'
        '</div>\n</div>\n'
        '</div>\n'
        '</div>\n'
        f'<p style="margin:20px auto;max-width:720px;padding:14px 18px;background:#f0fdf4;border-radius:8px;font-size:14px;color:#374151">Планируете поездку? Смотрите <a href="{planiruete_url}" style="color:#1A3D2E;font-weight:600">туры в Грузию с гидом →</a></p>\n'
        f'{readalso}\n'
        '</article>\n'
        f'{cards}\n'
        f'{TRIPADV_RU}\n'
        f'{faq}\n'
        '</div>'
    )


def en_region(bc_last, read_min, h1, date_line, lead, toc, body, cta_h3, cta_p,
              cta_url, cta_label, cta_wa_text, planiruete_url, readalso, cards, faq):
    return (
        '<header class="article-hero">\n'
        '<div class="breadcrumb">\n'
        '<a href="/en/">Home</a><span>/</span>\n'
        '<a href="/en/blog/">Blog</a><span>/</span>\n'
        f'<span>{bc_last}</span>\n'
        '</div>\n'
        f'<div class="article-label">Guide · {read_min} min read</div>\n'
        f'<h1 class="article-h1">{h1}</h1>\n'
        '<div class="article-meta">\n'
        f'<span>{date_line}</span>\n'
        '<span>Timur · Sakhva Travel</span>\n'
        '</div>\n</header>\n'
        '<article>\n<div class="article-wrap">\n'
        f'{BYLINE_EN}\n'
        f'<p class="article-lead">{lead}</p>\n'
        f'{toc}\n'
        '<div class="article-body">\n'
        f'{body}\n'
        '<div class="article-cta">\n'
        f'<h3>{cta_h3}</h3>\n<p>{cta_p}</p>\n'
        '<div class="cta-btns">\n'
        f'<a class="btn-wa" href="{cta_url}">{cta_label}</a>\n'
        f'<a class="btn-tg" href="https://wa.me/995511272623?text={cta_wa_text}">WhatsApp</a>\n'
        '</div>\n</div>\n'
        '</div>\n'
        '</div>\n'
        f'<p style="margin:20px auto;max-width:720px;padding:14px 18px;background:#f0fdf4;border-radius:8px;font-size:14px;color:#374151">Planning a trip? See <a href="{planiruete_url}" style="color:#1A3D2E;font-weight:600">Georgia tours with a guide →</a></p>\n'
        f'{readalso}\n'
        f'{cards}\n'
        f'{TRIPADV_EN}\n'
        f'{faq}'
    )


def build_schema(lang, ru_slug, en_slug, headline, desc, hero, pub, mod, bc_last, faq_pairs):
    if lang == "ru":
        url = f"{BASE}/blog/{ru_slug}/"
        home, blog = f"{BASE}/", f"{BASE}/blog/"
        cred = "Лицензия гида Грузии"
        home_n, blog_n = "Главная", "Блог"
        inlang = "ru"
    else:
        url = f"{BASE}/en/blog/{en_slug}/"
        home, blog = f"{BASE}/en/", f"{BASE}/en/blog/"
        cred = "Georgia Tour Guide Licence"
        home_n, blog_n = "Home", "Blog"
        inlang = "en"
    img = f"{BASE}/images/blog/{hero}.webp"
    graph = [
        {
            "@type": "BlogPosting",
            "@id": url + "#article",
            "inLanguage": inlang,
            "image": {"@type": "ImageObject", "url": img, "width": 1200, "height": 630},
            "headline": headline,
            "description": desc,
            "author": {
                "@type": "Person", "name": "Timur Sakhvadze",
                "jobTitle": "Tbilisi Guide", "url": f"{BASE}/about/",
                "@id": f"{BASE}/#guide-timur",
                "image": {"@type": "ImageObject", "url": f"{BASE}/images/timur.webp", "width": 72, "height": 72},
                "hasCredential": {
                    "@type": "EducationalOccupationalCredential",
                    "credentialCategory": "license", "name": cred, "identifier": "8247109128",
                },
            },
            "publisher": {
                "@type": "Organization", "name": "Sakhva Travel", "url": f"{BASE}/",
                "logo": {"@type": "ImageObject", "url": f"{BASE}/images/logo-schema.webp", "width": 300, "height": 60},
                "sameAs": [
                    "https://www.tripadvisor.com/Attraction_Review-g294195-d15318013-Reviews-Sakhva_Travel-Tbilisi.html",
                    "https://www.google.com/maps?cid=14070083063461040701",
                    "https://www.instagram.com/sakhvatravel/",
                ],
            },
            "about": [
                {"@type": "Place", "name": "Georgia", "sameAs": "https://www.wikidata.org/wiki/Q230"},
                {"@type": "Place", "name": "Tbilisi", "sameAs": "https://www.wikidata.org/wiki/Q994"},
            ],
            "datePublished": pub, "dateModified": mod, "url": url,
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1"]},
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": home_n, "item": home},
                {"@type": "ListItem", "position": 2, "name": blog_n, "item": blog},
                {"@type": "ListItem", "position": 3, "name": bc_last, "item": url},
            ],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faq_pairs
            ],
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, separators=(",", ":"))


# ============================================================
#  СТАТЬЯ 1 — Грузинский разговорник
# ============================================================
def _phrase_table(rows):
    body = "\n".join(
        f'<tr><td><strong>{g}</strong></td><td>{tr}</td><td>{ru}</td></tr>'
        for g, tr, ru in rows
    )
    return (
        '<table class="price-table">\n<thead><tr><th>По-грузински</th><th>Транскрипция</th><th>Перевод</th></tr></thead>\n'
        f'<tbody>\n{body}\n</tbody>\n</table>'
    )


def _phrase_table_en(rows):
    body = "\n".join(
        f'<tr><td><strong>{g}</strong></td><td>{tr}</td><td>{en}</td></tr>'
        for g, tr, en in rows
    )
    return (
        '<table class="price-table">\n<thead><tr><th>Georgian</th><th>Pronunciation</th><th>Meaning</th></tr></thead>\n'
        f'<tbody>\n{body}\n</tbody>\n</table>'
    )


# --- RU тело ст.1 ---
_A1_TOC_RU = (
    '<nav class="article-toc">\n<p class="toc-hd">Содержание</p>\n<ol>\n'
    '<li><a href="#privet">Приветствие и знакомство</a></li>\n'
    '<li><a href="#vezhlivost">Спасибо, пожалуйста, извините</a></li>\n'
    '<li><a href="#kafe">В кафе и ресторане</a></li>\n'
    '<li><a href="#taksi">Такси и как пройти</a></li>\n'
    '<li><a href="#pokupki">Покупки, цены, числа</a></li>\n'
    '<li><a href="#ekstrennye">Экстренные фразы</a></li>\n'
    '<li><a href="#proiznoshenie">Как произносить: 5 правил</a></li>\n'
    '</ol>\n</nav>'
)

_A1_BODY_RU = (
    '<h2 id="privet">Приветствие и знакомство</h2>\n'
    '<p>Главное слово, которое стоит выучить перед поездкой, — <strong>гамарджоба</strong>. Это «здравствуйте», и грузины реагируют на него теплее, чем на любое «hello». Дословно оно означает «победа» — так приветствовали воинов. В ответ вам скажут «гагимарджос». Не переживайте за идеальное произношение: сам факт, что турист пытается говорить по-грузински, здесь ценят.</p>\n'
    + _phrase_table([
        ("გამარჯობა", "гамарджо́ба", "здравствуйте"),
        ("გაგიმარჯოს", "гагима́рджос", "и вам здравствуйте (ответ)"),
        ("დილა მშვიდობისა", "ди́ла мшвидоби́са", "доброе утро"),
        ("ღამე მშვიდობისა", "гхаме мшвидоби́са", "спокойной ночи"),
        ("ნახვამდის", "нахвамди́с", "до свидания"),
        ("როგორ ხარ?", "рого́р хар?", "как дела?"),
        ("კარგად", "карга́д", "хорошо"),
        ("მე ვარ ტურისტი", "ме вар тури́сти", "я турист"),
    ]) +
    '\n<div class="info-box"><p>Грузинский язык не похож ни на один из соседних: у него собственный алфавит из 33 букв и нет заглавных. Читать вывески — отдельный навык. Если хотите разбирать надписи на улицах и в меню, посмотрите разбор в статье <a href="/blog/gruzinskiy-alfavit/">грузинский алфавит: 33 буквы с транскрипцией →</a>. Здесь же — только устная речь, которую вы реально используете.</p></div>\n'
    '<h2 id="vezhlivost">Спасибо, пожалуйста, извините</h2>\n'
    '<p>Эти пять слов закрывают 80% бытовых ситуаций. Самое частое — <strong>мадлоба</strong> («спасибо»). Его говорят официанту, таксисту, продавцу. «Пожалуйста» в смысле «прошу вас» — <strong>гэтаква</strong>, а в ответ на спасибо грузины часто говорят «араприс» — «не за что».</p>\n'
    + _phrase_table([
        ("მადლობა", "ма́длоба", "спасибо"),
        ("დიდი მადლობა", "ди́ди ма́длоба", "большое спасибо"),
        ("არაფრის", "арапри́с", "не за что"),
        ("გეთაყვა", "гэта́ква", "пожалуйста (прошу вас)"),
        ("ბოდიში", "боди́ши", "извините"),
        ("კი / დიახ", "ки / диа́х", "да (разг. / вежл.)"),
        ("არა", "а́ра", "нет"),
    ]) +
    '\n<h2 id="kafe">В кафе и ресторане</h2>\n'
    '<p>В Тбилиси в кафе почти везде поймут по-русски или по-английски, но пара фраз по-грузински превращает вас из «ещё одного туриста» в приятного гостя. Попросить счёт — <strong>ангариши</strong>, вкусно — <strong>гемриэли</strong>. О том, куда идти есть, я подробно писал в гайде по <a href="/blog/restorany-tbilisi/">ресторанам Тбилиси →</a>.</p>\n'
    + _phrase_table([
        ("მენიუ", "мени́у", "меню"),
        ("ერთი ყავა", "э́рти ка́ва", "один кофе"),
        ("წყალი", "цка́ли", "вода"),
        ("ღვინო", "гхви́но", "вино"),
        ("გემრიელია", "гемриэ́лиа", "вкусно"),
        ("ანგარიში", "ангари́ши", "счёт, пожалуйста"),
        ("ძალიან გემრიელი იყო", "дза́лиан гемриэ́ли и́ко", "было очень вкусно"),
    ]) +
    '\n<p>Про застолье, тосты и роль тамады — это отдельная большая тема. Если вас позовут на грузинский стол (а такое случается чаще, чем вы думаете), пригодится статья про <a href="/blog/gruzinskie-tosty/">грузинские тосты и тамаду →</a>.</p>\n'
    '<h2 id="taksi">Такси и как пройти</h2>\n'
    '<p>Большинство поездок в городе проще заказывать через приложение — там маршрут и цена уже забиты, и говорить почти не нужно. Как это работает и сколько стоит, я разобрал в отдельном гайде: <a href="/blog/taksi-tbilisi/">такси в Тбилиси: Bolt, Yandex и цены →</a>. Но если ловите машину на улице, эти фразы спасут.</p>\n'
    + _phrase_table([
        ("სად არის...?", "сад ари́с...?", "где находится...?"),
        ("რამდენი ღირს?", "рамде́ни гхи́рс?", "сколько стоит?"),
        ("აქ გავჩერდები", "ак гавчерде́би", "здесь остановите"),
        ("მარცხნივ", "марцхни́в", "налево"),
        ("მარჯვნივ", "марджвни́в", "направо"),
        ("პირდაპირ", "пирдапи́р", "прямо"),
        ("ცენტრი", "це́нтри", "центр"),
    ]) +
    '\n<h2 id="pokupki">Покупки, цены, числа</h2>\n'
    '<p>На рынке (базари) торг уместен и даже ожидаем. Ключевая фраза — «рамдени гхирс?» («сколько стоит?»). Цены называют в лари (ла́ри) и тетри (100 тетри = 1 лари). Несколько чисел лишними не будут:</p>\n'
    + _phrase_table([
        ("ერთი", "э́рти", "1"),
        ("ორი", "о́ри", "2"),
        ("სამი", "са́ми", "3"),
        ("ხუთი", "ху́ти", "5"),
        ("ათი", "а́ти", "10"),
        ("ოცი", "о́ци", "20"),
        ("ასი", "а́си", "100"),
        ("ლარი", "ла́ри", "лари (валюта)"),
    ]) +
    '\n<div class="info-box"><p>Чаевые в Грузии — вопрос отдельный: где-то их уже включают в счёт, где-то оставляют отдельно. Чтобы не переплатить и не показаться скупым, посмотрите разбор <a href="/blog/chaevye-v-gruzii/">чаевые в Грузии: сколько и кому оставлять →</a>.</p></div>\n'
    '<h2 id="ekstrennye">Экстренные фразы</h2>\n'
    '<p>Надеюсь, не пригодятся, но пусть будут. Единый номер экстренных служб в Грузии — <strong>112</strong>, операторы отвечают в том числе по-русски и по-английски.</p>\n'
    + _phrase_table([
        ("დამეხმარეთ!", "дамехмаре́т!", "помогите!"),
        ("მე დავიკარგე", "ме давикарге́", "я потерялся"),
        ("ვიძახებ ექიმს", "видза́хеб эки́мс", "вызовите врача"),
        ("პოლიცია", "поли́циа", "полиция"),
        ("არ მესმის", "ар ме́смис", "я не понимаю"),
        ("ლაპარაკობთ რუსულად?", "лапарако́бт русула́д?", "вы говорите по-русски?"),
    ]) +
    '\n<h2 id="proiznoshenie">Как произносить: 5 правил</h2>\n'
    '<ul>\n'
    '<li>Ударение в грузинском чаще всего на первом слоге в коротких словах и на третьем от конца — в длинных. Строгого правила нет, но эта привычка спасает.</li>\n'
    '<li>Буква <strong>«гх»</strong> (ღ) — это украинское/южнорусское «г», как в слове «ага». Именно она в «гхвино» (вино).</li>\n'
    '<li>Грузинский любит стечения согласных: «мцване» (зелёный), «гвприндавс». Не пытайтесь вставлять гласные — произносите слитно.</li>\n'
    '<li>Есть «твёрдые» и «придыхательные» пары (к/კ, п/პ). Турист их путает — и это нормально, вас поймут по контексту.</li>\n'
    '<li>Главное правило: улыбайтесь и не бойтесь ошибиться. «Гамарджоба» с акцентом ценят гораздо выше, чем идеальный английский.</li>\n'
    '</ul>\n'
    '<p>Хотите, чтобы кто-то показал живой Тбилиси и по дороге научил паре настоящих фраз? На <a href="/ekskursiya/sovetskiy-tur-tbilisi/">обзорной экскурсии с русскоязычным гидом</a> это получается само собой. А если сомневаетесь, <a href="/blog/russkoyazychny-gid-tbilisi/">нужен ли вообще русскоязычный гид в Тбилиси</a>, — есть отдельный разбор.</p>'
)

_A1_FAQ_PAIRS_RU = [
    ("Нужно ли знать грузинский для поездки в Грузию?",
     "Нет. В Тбилиси и туристических местах вас поймут по-русски или по-английски. Но несколько фраз — «гамарджоба» (здравствуйте) и «мадлоба» (спасибо) — сильно располагают местных и делают поездку теплее."),
    ("Как сказать «спасибо» по-грузински?",
     "«Спасибо» — мадлоба (ма́длоба), «большое спасибо» — диди мадлоба. Это самая полезная фраза: её говорят официанту, таксисту, продавцу."),
    ("Как будет «здравствуйте» по-грузински?",
     "Гамарджоба (гамарджо́ба). Дословно — «победа». В ответ говорят «гагимарджос». Универсальное приветствие в любое время суток."),
    ("Понимают ли в Грузии русский язык?",
     "В Тбилиси русский понимают почти все старше 30 лет, в сфере обслуживания — тем более. Молодёжь чаще говорит по-английски. В горных регионах (Сванетия) с русским сложнее — там выручает разговорник."),
    ("Сложно ли выучить грузинский алфавит?",
     "Устная речь и алфавит — разные задачи. Чтобы говорить простые фразы, буквы не нужны. А если хотите читать вывески и меню, разбор письменности есть в статье «грузинский алфавит: 33 буквы с транскрипцией»."),
]
_A1_FAQ_RU = _faq("Частые вопросы", _A1_FAQ_PAIRS_RU)

_A1_CARDS_RU = _cards([
    ("Гайд", "Грузинский алфавит", "33 буквы с транскрипцией и как читать вывески.", "/blog/gruzinskiy-alfavit/", "Читать →"),
    ("Гайд", "Такси в Тбилиси", "Bolt, Yandex Go и уличные машины: цены и лайфхаки.", "/blog/taksi-tbilisi/", "Читать →"),
    ("Тур", "Обзорный тур по Тбилиси", "Все главные точки за 4 часа с русскоязычным гидом.", "/ekskursiya/sovetskiy-tur-tbilisi/", "Подробнее →"),
])

_A1_READALSO_RU = _readalso("Читайте также:", [
    ("/blog/oshibki-turistov-tbilisi/", "10 ошибок туристов в Тбилиси 2026 →"),
    ("/blog/gruzinskaya-kukhnya-chto-poprobovat/", "Грузинская кухня: 15 блюд, что попробовать →"),
    ("/blog/chaevye-v-gruzii/", "Чаевые в Грузии: сколько и кому оставлять →"),
    ("/tury-v-gruziyu/", "Туры в Грузию 2026 — полный гид →"),
])

# --- EN тело ст.1 ---
_A1_TOC_EN = (
    '<nav class="article-toc">\n<p class="toc-hd">Contents</p>\n<ol>\n'
    '<li><a href="#hello">Greetings &amp; introductions</a></li>\n'
    '<li><a href="#polite">Thank you, please, sorry</a></li>\n'
    '<li><a href="#cafe">In a café or restaurant</a></li>\n'
    '<li><a href="#taxi">Taxi &amp; directions</a></li>\n'
    '<li><a href="#shopping">Shopping, prices, numbers</a></li>\n'
    '<li><a href="#emergency">Emergency phrases</a></li>\n'
    '<li><a href="#pronounce">Pronunciation: 5 rules</a></li>\n'
    '</ol>\n</nav>'
)

_A1_BODY_EN = (
    '<h2 id="hello">Greetings &amp; introductions</h2>\n'
    '<p>The one word worth learning before your trip is <strong>gamarjoba</strong> — "hello". Georgians warm up to it far more than to any "hi". Literally it means "victory": it was how warriors were greeted. The reply is "gagimarjos". Don\'t worry about perfect pronunciation — the mere fact that a tourist tries to speak Georgian is genuinely appreciated here.</p>\n'
    + _phrase_table_en([
        ("გამარჯობა", "gah-mar-JO-ba", "hello"),
        ("გაგიმარჯოს", "ga-gi-MAR-jos", "hello back (reply)"),
        ("დილა მშვიდობისა", "DEE-la mshvi-do-BEE-sa", "good morning"),
        ("ღამე მშვიდობისა", "GHA-me mshvi-do-BEE-sa", "good night"),
        ("ნახვამდის", "nakh-VAM-dis", "goodbye"),
        ("როგორ ხარ?", "RO-gor khar?", "how are you?"),
        ("კარგად", "kar-GAD", "good / fine"),
        ("მე ვარ ტურისტი", "me var tu-RIS-ti", "I am a tourist"),
    ]) +
    '\n<div class="info-box"><p>Georgian is unlike any neighbouring language: it has its own 33-letter alphabet and no capital letters. Reading signs is a separate skill. If you want to decode street signs and menus, see <a href="/en/blog/georgian-alphabet/">the Georgian alphabet: 33 letters with transcription →</a>. This guide covers spoken phrases you will actually use.</p></div>\n'
    '<h2 id="polite">Thank you, please, sorry</h2>\n'
    '<p>These five words cover 80% of everyday situations. The most frequent is <strong>madloba</strong> ("thank you") — you say it to a waiter, a driver, a shopkeeper. In reply to "thank you", Georgians often say "arapris" — "you\'re welcome".</p>\n'
    + _phrase_table_en([
        ("მადლობა", "MAD-lo-ba", "thank you"),
        ("დიდი მადლობა", "DEE-di MAD-lo-ba", "thank you very much"),
        ("არაფრის", "a-ra-PRIS", "you're welcome"),
        ("გეთაყვა", "ge-TAK-va", "please (I ask you)"),
        ("ბოდიში", "BO-di-shi", "sorry / excuse me"),
        ("კი / დიახ", "ki / di-AKH", "yes (informal / formal)"),
        ("არა", "A-ra", "no"),
    ]) +
    '\n<h2 id="cafe">In a café or restaurant</h2>\n'
    '<p>In Tbilisi almost every café will understand English, but a couple of Georgian words turn you from "just another tourist" into a welcome guest. "The bill" is <strong>angarishi</strong>, "delicious" is <strong>gemrieli</strong>. For where to actually eat, see my guide to <a href="/en/blog/best-restaurants-tbilisi/">restaurants in Tbilisi →</a>.</p>\n'
    + _phrase_table_en([
        ("მენიუ", "ME-ni-u", "menu"),
        ("ერთი ყავა", "ER-ti KA-va", "one coffee"),
        ("წყალი", "TSKA-li", "water"),
        ("ღვინო", "GHVEE-no", "wine"),
        ("გემრიელია", "gem-ri-E-li-a", "it's delicious"),
        ("ანგარიში", "an-ga-REE-shi", "the bill, please"),
        ("ძალიან გემრიელი იყო", "DZA-li-an gem-ri-E-li i-ko", "it was very tasty"),
    ]) +
    '\n<p>Supra (the Georgian feast), toasts and the role of the tamada are a big topic of their own. If you get invited to a Georgian table — and it happens more often than you\'d expect — read about <a href="/en/blog/georgian-toasts/">Georgian toasts and the tamada →</a>.</p>\n'
    '<h2 id="taxi">Taxi &amp; directions</h2>\n'
    '<p>Most city rides are easier through an app — the route and price are set in advance and you barely need to speak. How it works and what it costs is in my guide: <a href="/en/blog/tbilisi-taxi-guide/">taxi in Tbilisi: Bolt, Yandex and prices →</a>. But if you flag a car on the street, these phrases help.</p>\n'
    + _phrase_table_en([
        ("სად არის...?", "sad A-ris...?", "where is...?"),
        ("რამდენი ღირს?", "ram-DE-ni ghirs?", "how much is it?"),
        ("აქ გავჩერდები", "ak gav-cher-DE-bi", "stop here"),
        ("მარცხნივ", "marts-KHNIV", "left"),
        ("მარჯვნივ", "marj-VNIV", "right"),
        ("პირდაპირ", "pir-da-PIR", "straight ahead"),
        ("ცენტრი", "TSEN-tri", "the centre"),
    ]) +
    '\n<h2 id="shopping">Shopping, prices, numbers</h2>\n'
    '<p>At the market (bazari) haggling is normal and even expected. The key phrase is "ramdeni ghirs?" ("how much?"). Prices are in lari and tetri (100 tetri = 1 lari). A few numbers won\'t hurt:</p>\n'
    + _phrase_table_en([
        ("ერთი", "ER-ti", "1"),
        ("ორი", "O-ri", "2"),
        ("სამი", "SA-mi", "3"),
        ("ხუთი", "KHU-ti", "5"),
        ("ათი", "A-ti", "10"),
        ("ოცი", "O-tsi", "20"),
        ("ასი", "A-si", "100"),
        ("ლარი", "LA-ri", "lari (currency)"),
    ]) +
    '\n<div class="info-box"><p>Tipping in Georgia is its own question: sometimes it\'s already on the bill, sometimes you leave it separately. To avoid overpaying — or looking stingy — see <a href="/en/blog/tipping-in-georgia/">tipping in Georgia: how much and to whom →</a>.</p></div>\n'
    '<h2 id="emergency">Emergency phrases</h2>\n'
    '<p>Hopefully you won\'t need these, but keep them handy. The single emergency number in Georgia is <strong>112</strong>, and operators answer in English too.</p>\n'
    + _phrase_table_en([
        ("დამეხმარეთ!", "da-mekh-MA-ret!", "help!"),
        ("მე დავიკარგე", "me da-vi-KAR-ge", "I'm lost"),
        ("ვიძახებ ექიმს", "vi-DZA-kheb E-kims", "call a doctor"),
        ("პოლიცია", "po-LI-tsi-a", "police"),
        ("არ მესმის", "ar MES-mis", "I don't understand"),
        ("ინგლისურად ლაპარაკობთ?", "in-gli-SU-rad la-pa-ra-KOBT?", "do you speak English?"),
    ]) +
    '\n<h2 id="pronounce">Pronunciation: 5 rules</h2>\n'
    '<ul>\n'
    '<li>Stress usually falls on the first syllable in short words and on the third-from-last in long ones. There\'s no strict rule, but this habit helps.</li>\n'
    '<li>The letter <strong>"gh"</strong> (ღ) is a throaty g, close to the French r. It\'s the sound in "ghvino" (wine).</li>\n'
    '<li>Georgian loves consonant clusters: "mtsvane" (green), "gvprtskvni". Don\'t insert vowels — say them together.</li>\n'
    '<li>There are "ejective" pairs (k/კ, p/პ) that tourists mix up — that\'s fine, context makes you understood.</li>\n'
    '<li>The main rule: smile and don\'t fear mistakes. A "gamarjoba" with an accent is valued far more than perfect English.</li>\n'
    '</ul>\n'
    '<p>Want someone to show you the real Tbilisi and teach you a few genuine phrases on the way? On a <a href="/en/tours-in-georgia/">guided walking tour</a> it happens naturally. And if you\'re not sure <a href="/en/blog/russian-speaking-guide-tbilisi/">whether you even need a guide in Tbilisi</a>, there\'s a separate breakdown.</p>'
)

_A1_FAQ_PAIRS_EN = [
    ("Do I need to speak Georgian to visit Georgia?",
     "No. In Tbilisi and tourist areas English (and often Russian) is enough. But a few phrases — gamarjoba (hello) and madloba (thank you) — go a long way with locals and make the trip warmer."),
    ("How do you say thank you in Georgian?",
     "Thank you is madloba (MAD-lo-ba); thank you very much is didi madloba. It's the most useful phrase — you'll say it to waiters, drivers and shopkeepers all day."),
    ("How do you say hello in Georgian?",
     "Gamarjoba (gah-mar-JO-ba). Literally it means victory. The reply is gagimarjos. It works as a greeting at any time of day."),
    ("Is English widely spoken in Georgia?",
     "In Tbilisi younger people commonly speak English, and so do hotel and restaurant staff. In mountain regions like Svaneti it's less common — that's where a phrasebook really helps."),
    ("Is the Georgian alphabet hard to learn?",
     "Speaking and reading are separate tasks. To say simple phrases you don't need the letters at all. If you want to read signs and menus, see our guide 'the Georgian alphabet: 33 letters with transcription'."),
]
_A1_FAQ_EN = _faq("FAQ", _A1_FAQ_PAIRS_EN)

_A1_CARDS_EN = _cards([
    ("Guide", "Georgian alphabet", "33 letters with transcription and how to read signs.", "/en/blog/georgian-alphabet/", "Read →"),
    ("Guide", "Taxi in Tbilisi", "Bolt, Yandex Go and street cabs: prices and tips.", "/en/blog/tbilisi-taxi-guide/", "Read →"),
    ("Tour", "Tbilisi walking tour", "All the highlights in 4 hours with a local guide.", "/en/tours-in-georgia/", "Details →"),
])

_A1_READALSO_EN = _readalso("Read also:", [
    ("/en/blog/georgia-first-time-tips/", "Georgia first time: 25 tips from a local guide →"),
    ("/en/blog/georgian-food-guide/", "Georgian cuisine: 15 dishes to try →"),
    ("/en/blog/tipping-in-georgia/", "Tipping in Georgia: how much and to whom →"),
    ("/en/tours-in-georgia/", "Georgia tours with a guide →"),
])


# ============================================================
#  СТАТЬЯ 2 — Чаевые в Грузии
# ============================================================
_A2_TOC_RU = _toc("Содержание", [
    ("prinyato", "Приняты ли чаевые в Грузии"),
    ("restoran", "В кафе и ресторане: 10% и service charge"),
    ("taksi", "В такси, Bolt и Yandex"),
    ("otel", "Отель, гид, экскурсия, доставка"),
    ("skolko", "Шпаргалка: сколько и кому"),
])
_A2_BODY_RU = (
    '<h2 id="prinyato">Приняты ли чаевые в Грузии</h2>\n'
    '<p>Короткий ответ: чаевые в Грузии <strong>не обязательны, но культура их быстро развивается</strong>. Ещё лет десять назад оставить «на чай» считалось необязательным, а сегодня в Тбилиси это почти норма в кафе и ресторанах туристического центра. Никто не будет бежать за вами, если вы не оставили ничего, но благодарность за хороший сервис здесь ценят.</p>\n'
    '<p>Главное правило, которое я повторяю туристам: <strong>всегда смотрите в счёт</strong>. Всё чаще заведения сами добавляют «service charge» 10-18%, и тогда отдельные чаевые уже не нужны — иначе заплатите дважды.</p>\n'
    '<h2 id="restoran">В кафе и ресторане: 10% и service charge</h2>\n'
    '<p>Стандарт для ресторана с обслуживанием — <strong>10% от счёта</strong>. Если в чеке уже стоит строка «Service» или «მომსახურება» (обслуживание) — чаевые включены, добавлять сверху не нужно. В быстрых кофейнях и на фудкортах чаевые не ожидаются; там просто округляют или бросают мелочь в баночку у кассы.</p>\n'
    + _t3(["Место", "Сколько принято", "Как оставить"], [
        ["Ресторан с официантом", "10% (если нет service charge)", "наличными или в терминале"],
        ["Кофейня, пекарня", "необязательно, округление", "мелочь в баночку"],
        ["Бар, ночной клуб", "10% или 1-2 лари за коктейль", "наличными бармену"],
        ["Винный погреб, дегустация", "5-10%", "наличными"],
    ]) +
    '\n<div class="info-box"><p>Хотите заранее понимать порядок цен в тбилисских кафе, чтобы прикинуть и чаевые? Смотрите разбор <a href="/blog/restorany-tbilisi/">ресторанов Тбилиси →</a> и актуальные <a href="/blog/tseny-v-tbilisi-2026/">цены в Тбилиси 2026 →</a>.</p></div>\n'
    '<h2 id="taksi">В такси, Bolt и Yandex</h2>\n'
    '<p>В приложениях (Bolt, Yandex Go) чаевые <strong>не приняты</strong> — цена фиксированная, и водитель её видит заранее. Можно округлить сумму вверх, если поездка была приятной, но это по желанию. В уличном такси, где вы договариваетесь о цене заранее, чаевые тоже не нужны — вы и так торгуетесь. Как всё это работает, я разобрал в гайде про <a href="/blog/taksi-tbilisi/">такси в Тбилиси →</a>.</p>\n'
    '<h2 id="otel">Отель, гид, экскурсия, доставка</h2>\n'
    '<p>Здесь чаевые — вопрос личной благодарности за работу, а не обязанность.</p>\n'
    + _t3(["Кому", "Сколько принято", "Комментарий"], [
        ["Гид на экскурсии", "10-15% или 20-50 лари", "за хороший день — жест уважения"],
        ["Носильщик в отеле", "2-5 лари", "за багаж"],
        ["Горничная", "5 лари в день", "по желанию, оставить на тумбе"],
        ["Курьер доставки", "2-3 лари", "необязательно"],
    ]) +
    '\n<p>С гидом всё просто: если день понравился, благодарность всегда приятна, но их никто не ждёт по умолчанию. Наши цены на туры уже включают работу гида — чаевые остаются целиком на ваше усмотрение. Если сомневаетесь, <a href="/blog/russkoyazychny-gid-tbilisi/">нужен ли русскоязычный гид</a>, есть отдельный разбор.</p>\n'
    '<h2 id="skolko">Шпаргалка: сколько и кому</h2>\n'
    '<ul>\n'
    '<li><strong>Ресторан</strong> — 10%, но сначала проверьте «service charge» в счёте.</li>\n'
    '<li><strong>Кофейня/фастфуд</strong> — необязательно, округление.</li>\n'
    '<li><strong>Такси в приложении</strong> — не нужно, цена фиксированная.</li>\n'
    '<li><strong>Гид</strong> — по желанию, 10-15% за хороший день.</li>\n'
    '<li><strong>Отель</strong> — 2-5 лари носильщику, 5 лари в день горничной.</li>\n'
    '<li>Держите немного наличными: терминалы для чаевых есть не везде. Где снять лари и какие карты работают — в статье про <a href="/blog/kurs-lari-k-rublyu/">курс лари и обмен →</a>.</li>\n'
    '</ul>\n'
    '<p>И маленький бонус: одно слово «<a href="/blog/gruzinskie-frazy/">мадлоба</a>» (спасибо по-грузински) официанту или водителю иногда ценится не меньше самих чаевых.</p>'
)
_A2_FAQ_PAIRS_RU = [
    ("Обязательно ли оставлять чаевые в Грузии?",
     "Нет, чаевые в Грузии не обязательны. Но в ресторанах туристического Тбилиси 10% уже почти норма. Главное — проверять счёт: если там есть строка «service charge» (10-18%), отдельные чаевые не нужны."),
    ("Сколько чаевых принято в ресторане в Грузии?",
     "Стандарт — 10% от счёта, если обслуживание не включено. В кофейнях и на фудкортах достаточно округлить сумму или бросить мелочь в баночку у кассы."),
    ("Нужно ли давать чаевые таксисту в Грузии?",
     "В приложениях Bolt и Yandex Go чаевые не приняты — цена фиксированная. Можно округлить вверх по желанию. В уличном такси вы договариваетесь о цене заранее, поэтому чаевые тоже не нужны."),
    ("Что такое service charge в грузинском счёте?",
     "Это плата за обслуживание (10-18%), которую заведение добавляет автоматически. Если она есть в чеке, чаевые уже включены и добавлять сверху не надо. Ищите строку «Service» или «მომსახურება»."),
    ("Сколько дать чаевых гиду в Грузии?",
     "Чаевые гиду не обязательны — цена тура уже включает его работу. Если день понравился, принято благодарить 10-15% от стоимости или 20-50 лари. Это жест уважения, а не обязанность."),
]
_A2_FAQ_RU = _faq("Частые вопросы", _A2_FAQ_PAIRS_RU)
_A2_CARDS_RU = _cards([
    ("Гайд", "Такси в Тбилиси", "Bolt, Yandex Go и цены на поездки по городу.", "/blog/taksi-tbilisi/", "Читать →"),
    ("Гайд", "Цены в Тбилиси 2026", "Сколько стоят еда, транспорт, развлечения.", "/blog/tseny-v-tbilisi-2026/", "Читать →"),
    ("Тур", "Обзорный тур по Тбилиси", "Главные точки за 4 часа с русскоязычным гидом.", "/ekskursiya/sovetskiy-tur-tbilisi/", "Подробнее →"),
])
_A2_READALSO_RU = _readalso("Читайте также:", [
    ("/blog/restorany-tbilisi/", "Рестораны Тбилиси: где вкусно поесть →"),
    ("/blog/kurs-lari-k-rublyu/", "Курс лари к рублю: где менять деньги →"),
    ("/blog/gruzinskie-frazy/", "Грузинский разговорник: 40 фраз туристу →"),
    ("/blog/oshibki-turistov-tbilisi/", "10 ошибок туристов в Тбилиси →"),
])
_A2_TOC_EN = _toc("Contents", [
    ("custom", "Is tipping expected in Georgia"),
    ("restaurant", "Cafés and restaurants: 10% and service charge"),
    ("taxi", "Taxis, Bolt and Yandex"),
    ("hotel", "Hotel, guide, tour, delivery"),
    ("cheatsheet", "Cheat sheet: how much and to whom"),
])
_A2_BODY_EN = (
    '<h2 id="custom">Is tipping expected in Georgia</h2>\n'
    '<p>Short answer: tipping in Georgia is <strong>not mandatory, but the custom is growing fast</strong>. A decade ago tips were optional; today, in tourist-area Tbilisi, 10% in cafés and restaurants is almost the norm. No one will chase you if you leave nothing, but good service is genuinely appreciated here.</p>\n'
    '<p>The one rule I always give travelers: <strong>always check the bill</strong>. More and more venues add a "service charge" of 10-18%, and in that case you don\'t need to tip separately — otherwise you pay twice.</p>\n'
    '<h2 id="restaurant">Cafés and restaurants: 10% and service charge</h2>\n'
    '<p>The standard for a sit-down restaurant is <strong>10% of the bill</strong>. If the receipt already shows a "Service" line (or "მომსახურება"), the tip is included — don\'t add on top. At quick coffee shops and food courts tips aren\'t expected; people just round up or drop change in the jar by the till.</p>\n'
    + _t3(["Place", "Customary tip", "How to leave it"], [
        ["Restaurant with a waiter", "10% (if no service charge)", "cash or on the card terminal"],
        ["Coffee shop, bakery", "optional, round up", "change in the jar"],
        ["Bar, nightclub", "10% or ₾1-2 per cocktail", "cash to the bartender"],
        ["Wine cellar, tasting", "5-10%", "cash"],
    ]) +
    '\n<div class="info-box"><p>Want a feel for café prices in Tbilisi so you can gauge the tip? See our guide to <a href="/en/blog/best-restaurants-tbilisi/">restaurants in Tbilisi →</a>.</p></div>\n'
    '<h2 id="taxi">Taxis, Bolt and Yandex</h2>\n'
    '<p>In apps (Bolt, Yandex Go) tipping is <strong>not customary</strong> — the price is fixed and the driver sees it in advance. You can round up for a pleasant ride, but it\'s optional. In street taxis, where you agree the price beforehand, no tip is expected either. How it all works is in our <a href="/en/blog/tbilisi-taxi-guide/">Tbilisi taxi guide →</a>.</p>\n'
    '<h2 id="hotel">Hotel, guide, tour, delivery</h2>\n'
    '<p>Here a tip is a personal thank-you for the work, not an obligation.</p>\n'
    + _t3(["Who", "Customary tip", "Note"], [
        ["Tour guide", "10-15% or ₾20-50", "for a great day — a gesture of respect"],
        ["Hotel porter", "₾2-5", "for luggage"],
        ["Housekeeper", "₾5 per day", "optional, leave on the nightstand"],
        ["Delivery courier", "₾2-3", "optional"],
    ]) +
    '\n<p>With a guide it\'s simple: if you enjoyed the day, a thank-you is always welcome, but never assumed. Our tour prices already include the guide\'s work, so a tip is entirely up to you. Not sure <a href="/en/blog/russian-speaking-guide-tbilisi/">whether you need a guide</a>? There\'s a separate breakdown.</p>\n'
    '<h2 id="cheatsheet">Cheat sheet: how much and to whom</h2>\n'
    '<ul>\n'
    '<li><strong>Restaurant</strong> — 10%, but check the "service charge" line first.</li>\n'
    '<li><strong>Coffee shop / fast food</strong> — optional, round up.</li>\n'
    '<li><strong>Taxi app</strong> — not needed, price is fixed.</li>\n'
    '<li><strong>Guide</strong> — optional, 10-15% for a great day.</li>\n'
    '<li><strong>Hotel</strong> — ₾2-5 to a porter, ₾5 a day to housekeeping.</li>\n'
    '<li>Keep some cash: tip terminals aren\'t everywhere.</li>\n'
    '</ul>\n'
    '<p>And a small bonus: one word — "<a href="/en/blog/georgian-phrases-tourists/">madloba</a>" (thank you in Georgian) — to a waiter or driver is sometimes valued as much as the tip itself.</p>'
)
_A2_FAQ_PAIRS_EN = [
    ("Do I have to tip in Georgia?",
     "No, tipping in Georgia isn't mandatory. But in tourist-area Tbilisi restaurants, 10% is almost the norm. The key is to check the bill: if there's a service charge (10-18%), you don't need to tip separately."),
    ("How much do you tip in a restaurant in Georgia?",
     "The standard is 10% of the bill if service isn't included. At coffee shops and food courts it's enough to round up or drop change in the jar by the till."),
    ("Should I tip taxi drivers in Georgia?",
     "In the Bolt and Yandex Go apps tipping isn't customary — the price is fixed. You can round up if you like. In street taxis you agree the price in advance, so no tip is expected."),
    ("What is the service charge on a Georgian bill?",
     "It's a service fee (10-18%) that some venues add automatically. If it's on the receipt, the tip is already included — don't add more. Look for a line saying 'Service' or 'მომსახურება'."),
    ("How much should I tip a tour guide in Georgia?",
     "Tipping a guide isn't required — the tour price already covers their work. If you enjoyed the day, 10-15% of the price or ₾20-50 is customary. It's a gesture of respect, not an obligation."),
]
_A2_FAQ_EN = _faq("FAQ", _A2_FAQ_PAIRS_EN)
_A2_CARDS_EN = _cards([
    ("Guide", "Taxi in Tbilisi", "Bolt, Yandex Go and city ride prices.", "/en/blog/tbilisi-taxi-guide/", "Read →"),
    ("Guide", "Georgian phrases", "40 words every tourist needs, with pronunciation.", "/en/blog/georgian-phrases-tourists/", "Read →"),
    ("Tour", "Tbilisi walking tour", "All the highlights in 4 hours with a local guide.", "/en/tours-in-georgia/", "Details →"),
])
_A2_READALSO_EN = _readalso("Read also:", [
    ("/en/blog/best-restaurants-tbilisi/", "Best restaurants in Tbilisi →"),
    ("/en/blog/georgian-phrases-tourists/", "Georgian phrases: 40 words for tourists →"),
    ("/en/blog/georgia-first-time-tips/", "Georgia first time: 25 tips from a guide →"),
    ("/en/tours-in-georgia/", "Georgia tours with a guide →"),
])


# ============================================================
#  СТАТЬЯ 3 — Такси в Тбилиси
# ============================================================
_A3_TOC_RU = _toc("Содержание", [
    ("prilozheniya", "Bolt и Yandex Go — главный способ"),
    ("tseny", "Цены и тарифы по городу"),
    ("aeroport", "Такси из аэропорта Тбилиси"),
    ("ulica", "Уличное такси и торг"),
    ("oplata", "Оплата: карта или наличные"),
    ("sovety", "Безопасность и лайфхаки"),
])
_A3_BODY_RU = (
    '<h2 id="prilozheniya">Bolt и Yandex Go — главный способ</h2>\n'
    '<p>В Тбилиси такси дешёвое и его много, но ловить машину на улице почти никогда не выгодно. <strong>Ставьте приложение</strong> — это решает сразу три проблемы: фиксированная цена без торга, маршрут по навигатору и оплата картой. Работают два основных сервиса: <strong>Bolt</strong> (самый популярный, машин больше всего) и <strong>Yandex Go</strong> (удобен русскоязычным, цены чуть выше в час пик).</p>\n'
    '<p>Оба показывают цену до заказа, водитель её видит и не может изменить. Язык не нужен: адрес забит в приложении, маршрут — на карте. Именно поэтому приложение снимает 90% проблем с общением, о которых я пишу в <a href="/blog/gruzinskie-frazy/">разговорнике для туриста →</a>.</p>\n'
    '<h2 id="tseny">Цены и тарифы по городу</h2>\n'
    '<p>Такси в Тбилиси — одно из самых дешёвых в регионе. Ориентиры на 2026 год (тариф Bolt, обычное время):</p>\n'
    + _t3(["Маршрут", "Расстояние", "Примерная цена"], [
        ["По центру (короткая поездка)", "2-4 км", "4-7 лари"],
        ["Через город", "6-10 км", "8-15 лари"],
        ["Аэропорт → центр", "17 км", "15-25 лари"],
        ["Тбилиси → Мцхета", "25 км", "30-45 лари"],
    ]) +
    '\n<p>В дождь и час пик (18:00-20:00) действует повышающий коэффициент — цена может вырасти в 1.5-2 раза. Проще подождать 10 минут, чем переплачивать. Общие ориентиры по тратам в городе — в статье <a href="/blog/tseny-v-tbilisi-2026/">цены в Тбилиси 2026 →</a>.</p>\n'
    '<h2 id="aeroport">Такси из аэропорта Тбилиси</h2>\n'
    '<p>В зале прилёта вас будут ловить частники и предлагать «такси, такси» за 40-60 лари. <strong>Не соглашайтесь</strong> — это в 2-3 раза дороже приложения. Выйдите из здания, вызовите Bolt (точка посадки обозначена) — поездка до центра обойдётся в 15-25 лари. Есть и <strong>автобус №337</strong> до площади Свободы за 1 лари, но с багажом и после долгого перелёта такси комфортнее. Подробно про прилёт — в гайде по <a href="/blog/aeroport-tbilisi/">аэропорту Тбилиси →</a>.</p>\n'
    '<h2 id="ulica">Уличное такси и торг</h2>\n'
    '<p>Если приложение недоступно (сел телефон, нет интернета), можно поймать машину на улице. Правила простые: <strong>договаривайтесь о цене до посадки</strong>, счётчиков в Грузии нет. Называйте сумму сами — обычно она в 1.5 раза выше цены Bolt, торг уместен. В горных регионах (Казбеги, Сванетия) уличное такси и вовсе основной вариант; про заброски в горы я писал в <a href="/blog/transfer-tbilisi-kazbegi/">трансфере Тбилиси — Казбеги →</a>.</p>\n'
    '<h2 id="oplata">Оплата: карта или наличные</h2>\n'
    '<p>В приложении можно привязать карту (Visa/Mastercard) и платить безналом — удобно и без сдачи. Но <strong>держите и немного наличных лари</strong>: часть водителей просит оплату кэшем, особенно вечером. Российские карты «Мир» в такси не работают — какие карты принимают в Грузии и где снять наличные, разбираю в статье про <a href="/blog/kurs-lari-k-rublyu/">лари и обмен →</a>.</p>\n'
    '<h2 id="sovety">Безопасность и лайфхаки</h2>\n'
    '<ul>\n'
    '<li>Тбилисское такси безопасно, но пристёгивайтесь — водят здесь эмоционально.</li>\n'
    '<li>Проверяйте номер машины в приложении перед посадкой.</li>\n'
    '<li>Чаевые таксисту не нужны — цена фиксированная (подробнее в статье про <a href="/blog/chaevye-v-gruzii/">чаевые в Грузии →</a>).</li>\n'
    '<li>Для загородных поездок дешевле брать машину на весь день с водителем, а не считать по счётчику.</li>\n'
    '<li>Нет интернета для приложения? Купите местную симку — про связь есть <a href="/blog/svyaz-i-internet-v-gruzii/">отдельный гайд →</a>.</li>\n'
    '</ul>'
)
_A3_FAQ_PAIRS_RU = [
    ("Какое приложение такси работает в Тбилиси?",
     "В Тбилиси работают Bolt (самый популярный, машин больше всего) и Yandex Go (удобен русскоязычным). Оба показывают фиксированную цену до заказа, маршрут по навигатору и позволяют платить картой."),
    ("Сколько стоит такси из аэропорта Тбилиси до центра?",
     "Через приложение Bolt — 15-25 лари. Частники в зале прилёта просят 40-60 лари, это в 2-3 раза дороже. Есть также автобус №337 до площади Свободы за 1 лари."),
    ("Есть ли счётчики в такси в Грузии?",
     "Нет, счётчиков в грузинском такси нет. В приложениях цена фиксированная и известна заранее. В уличном такси нужно договариваться о сумме до посадки."),
    ("Можно ли платить картой в такси в Тбилиси?",
     "Да, в Bolt и Yandex Go можно привязать карту Visa или Mastercard. Но держите и наличные лари: часть водителей просит оплату кэшем. Карты «Мир» не работают."),
    ("Сколько стоит такси по Тбилиси?",
     "Короткая поездка по центру — 4-7 лари, через город — 8-15 лари. В час пик и дождь действует повышающий коэффициент (в 1.5-2 раза). Это одно из самых дешёвых такси в регионе."),
]
_A3_FAQ_RU = _faq("Частые вопросы", _A3_FAQ_PAIRS_RU)
_A3_CARDS_RU = _cards([
    ("Гайд", "Аэропорт Тбилиси", "Как добраться до города, автобус и такси.", "/blog/aeroport-tbilisi/", "Читать →"),
    ("Гайд", "Чаевые в Грузии", "Сколько оставлять в кафе, такси и отеле.", "/blog/chaevye-v-gruzii/", "Читать →"),
    ("Тур", "Трансфер Тбилиси — Казбеги", "Комфортная заброска в горы с водителем.", "/blog/transfer-tbilisi-kazbegi/", "Подробнее →"),
])
_A3_READALSO_RU = _readalso("Читайте также:", [
    ("/blog/metro-tbilisi/", "Метро Тбилиси: как пользоваться, карта →"),
    ("/blog/tseny-v-tbilisi-2026/", "Цены в Тбилиси 2026 →"),
    ("/blog/gruzinskie-frazy/", "Грузинский разговорник: 40 фраз →"),
    ("/blog/svyaz-i-internet-v-gruzii/", "Связь и интернет в Грузии →"),
])
_A3_TOC_EN = _toc("Contents", [
    ("apps", "Bolt and Yandex Go — the main way"),
    ("prices", "City prices and fares"),
    ("airport", "Taxi from Tbilisi Airport"),
    ("street", "Street taxis and haggling"),
    ("payment", "Payment: card or cash"),
    ("tips", "Safety and tips"),
])
_A3_BODY_EN = (
    '<h2 id="apps">Bolt and Yandex Go — the main way</h2>\n'
    '<p>Taxis in Tbilisi are cheap and plentiful, but flagging one on the street is almost never worth it. <strong>Get the app</strong> — it solves three problems at once: a fixed price with no haggling, a navigator route, and card payment. Two services dominate: <strong>Bolt</strong> (the most popular, most cars) and <strong>Yandex Go</strong> (slightly higher at peak hours).</p>\n'
    '<p>Both show the price before you book, and the driver can\'t change it. No language needed: the address is in the app, the route is on the map. That\'s why the app removes most of the communication issues I cover in the <a href="/en/blog/georgian-phrases-tourists/">tourist phrasebook →</a>.</p>\n'
    '<h2 id="prices">City prices and fares</h2>\n'
    '<p>Tbilisi taxis are among the cheapest in the region. Rough 2026 figures (Bolt fare, normal hours):</p>\n'
    + _t3(["Route", "Distance", "Approx. price"], [
        ["Around the centre (short ride)", "2-4 km", "₾4-7"],
        ["Across the city", "6-10 km", "₾8-15"],
        ["Airport → centre", "17 km", "₾15-25"],
        ["Tbilisi → Mtskheta", "25 km", "₾30-45"],
    ]) +
    '\n<p>In rain and at rush hour (6-8 pm) a surge multiplier applies — the price can rise 1.5-2×. It\'s easier to wait 10 minutes than overpay. For overall city spending, see <a href="/en/blog/georgia-first-time-tips/">Georgia first-time tips →</a>.</p>\n'
    '<h2 id="airport">Taxi from Tbilisi Airport</h2>\n'
    '<p>In arrivals, private drivers will offer "taxi, taxi" for ₾40-60. <strong>Don\'t take it</strong> — that\'s 2-3× the app price. Step outside, order a Bolt (there\'s a marked pickup point), and the ride to the centre is ₾15-25. There\'s also <strong>bus #337</strong> to Freedom Square for ₾1, but with luggage after a long flight a taxi is comfier. Full arrival details are in the <a href="/en/blog/tbilisi-airport-guide/">Tbilisi airport guide →</a>.</p>\n'
    '<h2 id="street">Street taxis and haggling</h2>\n'
    '<p>If the app isn\'t available (dead phone, no internet), you can flag a car. Simple rules: <strong>agree the price before getting in</strong> — there are no meters in Georgia. Name a figure yourself; it\'s usually 1.5× the Bolt price, and haggling is fine. In mountain regions (Kazbegi, Svaneti) street taxis are the main option; see the <a href="/en/blog/kazbegi-complete-guide/">Kazbegi guide →</a>.</p>\n'
    '<h2 id="payment">Payment: card or cash</h2>\n'
    '<p>In the app you can link a Visa/Mastercard and pay cashless — no change needed. But <strong>keep some lari on you</strong>: some drivers prefer cash, especially in the evening. Mir cards don\'t work in taxis — which cards are accepted in Georgia and where to withdraw cash is covered in our <a href="/en/blog/georgia-first-time-tips/">first-time guide →</a>.</p>\n'
    '<h2 id="tips">Safety and tips</h2>\n'
    '<ul>\n'
    '<li>Tbilisi taxis are safe, but buckle up — driving here is emotional.</li>\n'
    '<li>Check the car\'s plate in the app before getting in.</li>\n'
    '<li>No tip needed — the price is fixed (see <a href="/en/blog/tipping-in-georgia/">tipping in Georgia →</a>).</li>\n'
    '<li>For out-of-town trips, hiring a car with a driver for the whole day is cheaper than metering.</li>\n'
    '<li>No internet for the app? Get a local SIM — there\'s a separate guide on that.</li>\n'
    '</ul>'
)
_A3_FAQ_PAIRS_EN = [
    ("Which taxi app works in Tbilisi?",
     "Tbilisi has Bolt (the most popular, most cars) and Yandex Go. Both show a fixed price before you book, route by navigator, and let you pay by card. Bolt is the default choice for most travelers."),
    ("How much is a taxi from Tbilisi Airport to the centre?",
     "Via the Bolt app it's ₾15-25. Private drivers in arrivals ask ₾40-60, which is 2-3× more. There's also bus #337 to Freedom Square for ₾1."),
    ("Are there meters in Georgian taxis?",
     "No, Georgian taxis have no meters. In the apps the price is fixed and known in advance. In a street taxi you must agree the amount before getting in."),
    ("Can I pay by card in a Tbilisi taxi?",
     "Yes, in Bolt and Yandex Go you can link a Visa or Mastercard. But keep some cash lari too, as some drivers prefer cash. Mir cards do not work."),
    ("How much does a taxi cost in Tbilisi?",
     "A short ride in the centre is ₾4-7, across the city ₾8-15. At rush hour and in rain a surge multiplier applies (1.5-2×). It's one of the cheapest taxi cities in the region."),
]
_A3_FAQ_EN = _faq("FAQ", _A3_FAQ_PAIRS_EN)
_A3_CARDS_EN = _cards([
    ("Guide", "Tbilisi Airport", "How to reach the city — bus and taxi.", "/en/blog/tbilisi-airport-guide/", "Read →"),
    ("Guide", "Tipping in Georgia", "How much to tip in cafés, taxis and hotels.", "/en/blog/tipping-in-georgia/", "Read →"),
    ("Guide", "Tbilisi metro", "How to use it, the map and fares.", "/en/blog/tbilisi-metro-guide/", "Read →"),
])
_A3_READALSO_EN = _readalso("Read also:", [
    ("/en/blog/tbilisi-metro-guide/", "Tbilisi metro: how to use it →"),
    ("/en/blog/georgian-phrases-tourists/", "Georgian phrases: 40 words for tourists →"),
    ("/en/blog/tipping-in-georgia/", "Tipping in Georgia: how much and to whom →"),
    ("/en/tours-in-georgia/", "Georgia tours with a guide →"),
])

# ============================================================
#  СТАТЬЯ 4 — Грузинские сладости
# ============================================================
_A4_TOC_RU = _toc("Содержание", [
    ("churchkhela", "Чурчхела — грузинский «сникерс»"),
    ("pelamushi", "Пеламуши и татара"),
    ("gozinaki", "Козинаки (гозинаки)"),
    ("tklapi", "Тклапи — фруктовая пастила"),
    ("vypechka", "Када, назуки и выпечка"),
    ("gde", "Где попробовать и купить"),
])
_A4_BODY_RU = (
    '<h2 id="churchkhela">Чурчхела — грузинский «сникерс»</h2>\n'
    '<p>Если вы попробуете в Грузии только одну сладость — пусть это будет <strong>чурчхела</strong>. Орехи (грецкий или фундук) нанизывают на нить и несколько раз обмакивают в загущённый виноградный сок — <em>татару</em>. Получается плотная «колбаска», которую сушат неделями. Никакого сахара: сладость даёт виноград. Это древний походный десерт — калорийный, натуральный и невероятно вкусный.</p>\n'
    '<div class="info-box"><p>Не путайте свежую чурчхелу с сувенирной: на рынке для туристов часто продают пересушенную. Настоящая — мягкая внутри, с целыми орехами. Что ещё стоит увезти домой — в гайде <a href="/blog/chto-privezti-iz-gruzii/">что привезти из Грузии →</a>.</p></div>\n'
    '<h2 id="pelamushi">Пеламуши и татара</h2>\n'
    '<p>Из того же виноградного сока (<strong>татары</strong>), что идёт на чурчхелу, делают <strong>пеламуши</strong> — густой пудинг цвета молодого вина. Его подают охлаждённым, иногда посыпают орехами. На грузинском застолье пеламуши — классический десерт; кстати, о самом застолье и тостах я писал в статье про <a href="/blog/gruzinskie-tosty/">грузинские тосты и тамаду →</a>.</p>\n'
    '<h2 id="gozinaki">Козинаки (гозинаки)</h2>\n'
    '<p><strong>Гозинаки</strong> — обжаренные грецкие орехи в горячем мёде, нарезанные ромбиками. Традиционно их готовят к Новому году, но купить можно круглый год. Хрустящие, очень сладкие — идут на ура с чаем. Именно из Грузии козинаки разошлись по всему постсоветскому пространству.</p>\n'
    '<h2 id="tklapi">Тклапи — фруктовая пастила</h2>\n'
    '<p><strong>Тклапи</strong> — тонкие листы высушенного фруктового пюре (чаще из ткемали — кислой сливы). Бывает сладким и кислым; кислый идёт как приправа в супы (харчо), сладкий едят как пастилу. Лёгкий, долго хранится — удобный перекус в дорогу.</p>\n'
    + _t3(["Сладость", "Что это", "Ориентир цены"], [
        ["Чурчхела", "орехи в виноградном соке", "3-6 лари/шт"],
        ["Пеламуши", "виноградный пудинг", "5-8 лари порция"],
        ["Гозинаки", "орехи в мёде", "8-15 лари/кг"],
        ["Тклапи", "фруктовая пастила", "5-10 лари лист"],
        ["Када", "слоёная выпечка", "3-5 лари/шт"],
    ]) +
    '\n<h2 id="vypechka">Када, назуки и выпечка</h2>\n'
    '<p><strong>Када</strong> — слоёная булочка с сахарно-масляной начинкой, её продают у каждой пекарни. <strong>Назуки</strong> — сладкий хлеб с корицей и изюмом; лучший делают в городке Сурами по дороге на Батуми, там его продают прямо у трассы горячим. Эти вещи хорошо идут к грузинскому кофе или вину — о винах есть <a href="/blog/gruzinskoe-vino-gid/">отдельный гид →</a>.</p>\n'
    '<h2 id="gde">Где попробовать и купить</h2>\n'
    '<ul>\n'
    '<li><strong>Рынок Дезертирский (Дезертирка)</strong> в Тбилиси — самый большой выбор чурчхелы и специй.</li>\n'
    '<li><strong>Пекарни и кофейни</strong> старого города — свежая када и назуки.</li>\n'
    '<li><strong>Кахетия</strong> — родина чурчхелы и вина; на дегустационных турах сладости часто дают к вину.</li>\n'
    '<li>В ресторанах пеламуши и мороженое обычно есть в десертном меню — где вкусно поесть, смотрите в гайде по <a href="/blog/restorany-tbilisi/">ресторанам Тбилиси →</a>.</li>\n'
    '</ul>\n'
    '<p>Хотите продегустировать сладости и вино там, где их делают? На выездных турах по <a href="/tury-v-gruziyu/">Грузии с гидом</a> это часть программы — от винного погреба до придорожного назуки.</p>'
)
_A4_FAQ_PAIRS_RU = [
    ("Что такое чурчхела?",
     "Чурчхела — традиционная грузинская сладость: орехи (грецкий или фундук) на нити, многократно обмакнутые в загущённый виноградный сок и высушенные. Без добавления сахара — сладость даёт виноград. Плотная, калорийная, натуральная."),
    ("Какие сладости попробовать в Грузии?",
     "Обязательно чурчхела, пеламуши (виноградный пудинг), гозинаки (орехи в мёде), тклапи (фруктовая пастила) и выпечка — када и назуки. Почти все они основаны на винограде, орехах и мёде, без промышленного сахара."),
    ("Чем чурчхела отличается от козинаки?",
     "Чурчхела — орехи в застывшем виноградном соке, мягкая внутри. Гозинаки (козинаки) — обжаренные орехи в горячем мёде, нарезанные ромбиками, хрустящие. Разные текстуры и основа: виноград против мёда."),
    ("Сколько стоит чурчхела в Грузии?",
     "На рынке в Тбилиси одна чурчхела стоит 3-6 лари в зависимости от орехов и размера. На туристических точках дороже. Берите мягкую с целыми орехами — пересушенная часто идёт как сувенирная."),
    ("Где купить грузинские сладости в Тбилиси?",
     "Лучший выбор — на Дезертирском рынке (Дезертирка): чурчхела, гозинаки, специи. Свежую выпечку (када, назуки) ищите в пекарнях старого города. В Кахетии сладости часто подают к вину на дегустациях."),
]
_A4_FAQ_RU = _faq("Частые вопросы", _A4_FAQ_PAIRS_RU)
_A4_CARDS_RU = _cards([
    ("Гайд", "Грузинская кухня", "15 блюд, которые нужно попробовать в Тбилиси.", "/blog/gruzinskaya-kukhnya-chto-poprobovat/", "Читать →"),
    ("Гайд", "Что привезти из Грузии", "20 идей съедобных и не только сувениров.", "/blog/chto-privezti-iz-gruzii/", "Читать →"),
    ("Гайд", "Грузинское вино", "Квеври, саперави и как выбрать бутылку.", "/blog/gruzinskoe-vino-gid/", "Читать →"),
])
_A4_READALSO_RU = _readalso("Читайте также:", [
    ("/blog/restorany-tbilisi/", "Рестораны Тбилиси: где вкусно поесть →"),
    ("/blog/khachapuri-po-adzharski/", "Хачапури по-аджарски: где лучший →"),
    ("/blog/gruzinskie-tosty/", "Грузинские тосты и тамада →"),
    ("/blog/gruzinskie-frazy/", "Грузинский разговорник: 40 фраз →"),
])
_A4_TOC_EN = _toc("Contents", [
    ("churchkhela", "Churchkhela — the Georgian energy bar"),
    ("pelamushi", "Pelamushi and tatara"),
    ("gozinaki", "Gozinaki (honey nut brittle)"),
    ("tklapi", "Tklapi — fruit leather"),
    ("baking", "Kada, nazuki and pastries"),
    ("where", "Where to try and buy them"),
])
_A4_BODY_EN = (
    '<h2 id="churchkhela">Churchkhela — the Georgian energy bar</h2>\n'
    '<p>If you try only one sweet in Georgia, make it <strong>churchkhela</strong>. Nuts (walnut or hazelnut) are threaded on a string and dipped several times in thickened grape juice — <em>tatara</em>. The result is a dense "sausage" dried for weeks. No sugar: the sweetness comes from the grapes. It\'s an ancient travel snack — calorific, natural and delicious.</p>\n'
    '<div class="info-box"><p>Don\'t confuse fresh churchkhela with the souvenir kind: tourist stalls often sell it over-dried. The real thing is soft inside with whole nuts. For more edible souvenirs, see our guide to <a href="/en/blog/georgian-food-guide/">Georgian food →</a>.</p></div>\n'
    '<h2 id="pelamushi">Pelamushi and tatara</h2>\n'
    '<p>The same grape juice (<strong>tatara</strong>) used for churchkhela becomes <strong>pelamushi</strong> — a thick pudding the colour of young wine, served chilled and sometimes topped with nuts. At a Georgian feast pelamushi is the classic dessert; on the feast itself and its toasts, see <a href="/en/blog/georgian-toasts/">Georgian toasts and the tamada →</a>.</p>\n'
    '<h2 id="gozinaki">Gozinaki (honey nut brittle)</h2>\n'
    '<p><strong>Gozinaki</strong> is roasted walnuts in hot honey, cut into diamonds. Traditionally made for New Year, but sold year-round. Crunchy and very sweet, it\'s perfect with tea. From Georgia it spread across the whole post-Soviet region.</p>\n'
    '<h2 id="tklapi">Tklapi — fruit leather</h2>\n'
    '<p><strong>Tklapi</strong> is thin sheets of dried fruit purée (usually tkemali — sour plum). It comes sweet or sour; the sour kind is used as a seasoning in soups (kharcho), the sweet kind eaten like fruit leather. Light and long-keeping — a handy snack for the road.</p>\n'
    + _t3(["Sweet", "What it is", "Approx. price"], [
        ["Churchkhela", "nuts in grape juice", "₾3-6 each"],
        ["Pelamushi", "grape pudding", "₾5-8 a portion"],
        ["Gozinaki", "nuts in honey", "₾8-15 / kg"],
        ["Tklapi", "fruit leather", "₾5-10 a sheet"],
        ["Kada", "layered pastry", "₾3-5 each"],
    ]) +
    '\n<h2 id="baking">Kada, nazuki and pastries</h2>\n'
    '<p><strong>Kada</strong> is a flaky bun with a sugar-butter filling, sold at every bakery. <strong>Nazuki</strong> is a sweet cinnamon-and-raisin bread; the best comes from the town of Surami on the road to Batumi, sold hot right by the highway. These go beautifully with Georgian coffee or wine — there\'s a separate <a href="/en/blog/georgian-wine-guide/">wine guide →</a>.</p>\n'
    '<h2 id="where">Where to try and buy them</h2>\n'
    '<ul>\n'
    '<li><strong>Dezerter Bazaar</strong> in Tbilisi — the biggest selection of churchkhela and spices.</li>\n'
    '<li><strong>Old-town bakeries and cafés</strong> — fresh kada and nazuki.</li>\n'
    '<li><strong>Kakheti</strong> — the home of churchkhela and wine; on tasting tours sweets often come with the wine.</li>\n'
    '<li>Restaurants usually list pelamushi and ice cream on the dessert menu — for where to eat, see <a href="/en/blog/best-restaurants-tbilisi/">restaurants in Tbilisi →</a>.</li>\n'
    '</ul>\n'
    '<p>Want to taste sweets and wine where they\'re made? On <a href="/en/tours-in-georgia/">guided tours across Georgia</a> it\'s part of the programme — from the wine cellar to roadside nazuki.</p>'
)
_A4_FAQ_PAIRS_EN = [
    ("What is churchkhela?",
     "Churchkhela is a traditional Georgian sweet: nuts (walnut or hazelnut) on a string, dipped repeatedly in thickened grape juice and dried. No added sugar — the sweetness comes from the grapes. It's dense, calorific and completely natural."),
    ("Which sweets should I try in Georgia?",
     "Definitely churchkhela, pelamushi (grape pudding), gozinaki (honey nut brittle), tklapi (fruit leather), and pastries — kada and nazuki. Almost all are based on grapes, nuts and honey, without industrial sugar."),
    ("What's the difference between churchkhela and gozinaki?",
     "Churchkhela is nuts set in grape juice, soft inside. Gozinaki is roasted nuts in hot honey, cut into diamonds and crunchy. Different textures and base: grape versus honey."),
    ("How much does churchkhela cost in Georgia?",
     "At a Tbilisi market one churchkhela is ₾3-6 depending on the nuts and size. Tourist spots charge more. Choose the soft kind with whole nuts — the over-dried version is usually sold as a souvenir."),
    ("Where can I buy Georgian sweets in Tbilisi?",
     "The best choice is at Dezerter Bazaar: churchkhela, gozinaki, spices. For fresh pastries (kada, nazuki) look in old-town bakeries. In Kakheti sweets are often served with wine at tastings."),
]
_A4_FAQ_EN = _faq("FAQ", _A4_FAQ_PAIRS_EN)
_A4_CARDS_EN = _cards([
    ("Guide", "Georgian cuisine", "15 dishes you must try in Tbilisi.", "/en/blog/georgian-food-guide/", "Read →"),
    ("Guide", "Adjarian khachapuri", "The boat-shaped cheese bread and where to find it.", "/en/blog/adjarian-khachapuri-guide/", "Read →"),
    ("Guide", "Georgian wine", "Qvevri, saperavi and how to pick a bottle.", "/en/blog/georgian-wine-guide/", "Read →"),
])
_A4_READALSO_EN = _readalso("Read also:", [
    ("/en/blog/best-restaurants-tbilisi/", "Best restaurants in Tbilisi →"),
    ("/en/blog/georgian-toasts/", "Georgian toasts and the tamada →"),
    ("/en/blog/georgian-phrases-tourists/", "Georgian phrases: 40 words for tourists →"),
    ("/en/tours-in-georgia/", "Georgia tours with a guide →"),
])

# ============================================================
#  СТАТЬЯ 5 — Карты и наличные в Грузии
# ============================================================
_A5_TOC_RU = _toc("Содержание", [
    ("kakie", "Какие карты работают в Грузии"),
    ("bankomaty", "Банкоматы: где и сколько снять"),
    ("nalichnye", "Где нужны наличные"),
    ("komissii", "Комиссии и конвертация"),
    ("schet", "Открывать ли счёт в грузинском банке"),
    ("sovety", "Практические советы"),
])
_A5_BODY_RU = (
    '<h2 id="kakie">Какие карты работают в Грузии</h2>\n'
    '<p>Главный вопрос для многих туристов в 2026 году. Коротко:</p>\n'
    + _t3(["Карта", "Работает?", "Где"], [
        ["Visa / Mastercard (не РФ)", "да", "~90% мест в Тбилиси, банкоматы"],
        ["Карта «Мир» (РФ)", "нет", "не принимается нигде"],
        ["UnionPay", "частично", "некоторые банкоматы и ТЦ"],
        ["Карты банков Грузии/Армении/Казахстана", "да", "везде"],
    ]) +
    '\n<p>Ключевое: <strong>российские Visa/Mastercard и «Мир» в Грузии не работают</strong> из-за санкций. Работают карты, выпущенные вне РФ. Если вы из России, самый частый рабочий вариант — карта другой страны (Армения, Казахстан, ОАЭ) или наличные. Про сам курс и обмен я подробно писал в статье <a href="/blog/kurs-lari-k-rublyu/">курс лари к рублю →</a>.</p>\n'
    '<h2 id="bankomaty">Банкоматы: где и сколько снять</h2>\n'
    '<p>Банкоматов в Тбилиси много: TBC, Bank of Georgia, Liberty — на каждом углу. С карты Visa/Mastercard иностранного банка снять лари не проблема. Нюансы:</p>\n'
    '<ul>\n'
    '<li>Лимит за одну операцию — обычно 2000-3000 лари, но зависит от банкомата.</li>\n'
    '<li>Банкомат может предложить «конвертацию в вашей валюте» (DCC) — <strong>всегда отказывайтесь</strong> и снимайте в лари, курс вашего банка выгоднее.</li>\n'
    '<li>У TBC и Bank of Georgia встречаются банкоматы с выдачей долларов — удобно, если нужен кэш в USD.</li>\n'
    '</ul>\n'
    '<h2 id="nalichnye">Где нужны наличные</h2>\n'
    '<p>Картой в Тбилиси можно платить почти везде, но <strong>немного лари наличными держите всегда</strong>. Кэш нужен в таких местах:</p>\n'
    '<ul>\n'
    '<li>Рынки и маленькие лавки (чурчхела, специи, сувениры).</li>\n'
    '<li>Часть такси, особенно уличное — подробнее в гайде про <a href="/blog/taksi-tbilisi/">такси в Тбилиси →</a>.</li>\n'
    '<li>Маршрутки и сельский транспорт.</li>\n'
    '<li>Небольшие семейные кафе и гестхаусы в регионах (Казбеги, Сванетия).</li>\n'
    '<li>Чаевые, где нет терминала — про это есть статья про <a href="/blog/chaevye-v-gruzii/">чаевые в Грузии →</a>.</li>\n'
    '</ul>\n'
    '<h2 id="komissii">Комиссии и конвертация</h2>\n'
    '<p>При оплате картой вне вашей домашней валюты банк-эмитент берёт конвертацию (обычно 0.5-2%). В самой Грузии магазины и рестораны за оплату картой ничего дополнительно не берут. Главная ловушка — та самая DCC (оплата «в вашей валюте»): терминал предложит зафиксировать сумму в рублях/долларах по своему невыгодному курсу. Всегда выбирайте оплату <strong>в лари</strong>.</p>\n'
    '<h2 id="schet">Открывать ли счёт в грузинском банке</h2>\n'
    '<p>Для короткой поездки — <strong>нет смысла</strong>, хватает наличных и иностранной карты. Счёт в TBC или Bank of Georgia актуален релокантам и тем, кто задерживается надолго: тогда появляется местная карта, которая работает везде. Про жизнь в Тбилиси надолго есть отдельный разбор для <a href="/blog/tbilisi-dlya-relokantov/">релокантов →</a>.</p>\n'
    '<h2 id="sovety">Практические советы</h2>\n'
    '<ul>\n'
    '<li>Везите с собой немного наличных долларов/евро — их легко и выгодно поменять на лари.</li>\n'
    '<li>Не держите все деньги на одной карте; часть — кэшем.</li>\n'
    '<li>Обмен выгоднее в городских обменниках, а не в аэропорту (там курс хуже).</li>\n'
    '<li>Планируя бюджет, сверьтесь со статьёй <a href="/blog/skolko-stoit-otdyh-v-gruzii/">сколько стоит отдых в Грузии →</a>.</li>\n'
    '<li>Не забудьте про <a href="/blog/strahovka-v-gruziyu/">страховку для въезда →</a> — с 2026 она обязательна.</li>\n'
    '</ul>'
)
_A5_FAQ_PAIRS_RU = [
    ("Какие карты работают в Грузии в 2026?",
     "Работают Visa и Mastercard, выпущенные вне России, — их принимают в ~90% мест Тбилиси и в банкоматах. Российские карты «Мир» и российские Visa/Mastercard не работают из-за санкций. UnionPay принимают частично."),
    ("Работает ли карта «Мир» в Грузии?",
     "Нет, карты «Мир» в Грузии не принимаются нигде — ни в магазинах, ни в банкоматах. Туристам из России нужны наличные или карта, выпущенная в другой стране (Армения, Казахстан, ОАЭ)."),
    ("Где снять наличные лари в Тбилиси?",
     "В банкоматах TBC, Bank of Georgia, Liberty — их много по всему городу. С иностранной карты Visa/Mastercard снятие без проблем. При снятии отказывайтесь от конвертации в вашей валюте (DCC) и берите лари."),
    ("Нужны ли наличные в Грузии или хватит карты?",
     "Картой можно платить почти везде в Тбилиси, но немного наличных лари держите всегда: они нужны на рынках, в части такси, в маршрутках и в семейных кафе и гестхаусах в регионах."),
    ("Стоит ли открывать счёт в грузинском банке туристу?",
     "Для короткой поездки смысла нет — хватает наличных и иностранной карты. Счёт в TBC или Bank of Georgia имеет смысл релокантам и тем, кто остаётся надолго: местная карта работает везде без ограничений."),
]
_A5_FAQ_RU = _faq("Частые вопросы", _A5_FAQ_PAIRS_RU)
_A5_CARDS_RU = _cards([
    ("Гайд", "Курс лари к рублю", "Где менять деньги и сколько брать с собой.", "/blog/kurs-lari-k-rublyu/", "Читать →"),
    ("Гайд", "Сколько стоит отдых", "Бюджет на 3, 5 и 7 дней в Грузии.", "/blog/skolko-stoit-otdyh-v-gruzii/", "Читать →"),
    ("Гайд", "Цены в Тбилиси 2026", "Еда, транспорт, развлечения в цифрах.", "/blog/tseny-v-tbilisi-2026/", "Читать →"),
])
_A5_READALSO_RU = _readalso("Читайте также:", [
    ("/blog/chaevye-v-gruzii/", "Чаевые в Грузии: сколько и кому →"),
    ("/blog/taksi-tbilisi/", "Такси в Тбилиси: Bolt, Yandex, цены →"),
    ("/blog/strahovka-v-gruziyu/", "Страховка для въезда в Грузию 2026 →"),
    ("/blog/gruziya-perviy-raz/", "Грузия первый раз: 25 советов →"),
])
_A5_TOC_EN = _toc("Contents", [
    ("which", "Which cards work in Georgia"),
    ("atm", "ATMs: where and how much to withdraw"),
    ("cash", "Where you need cash"),
    ("fees", "Fees and conversion"),
    ("account", "Should you open a Georgian bank account"),
    ("tips", "Practical tips"),
])
_A5_BODY_EN = (
    '<h2 id="which">Which cards work in Georgia</h2>\n'
    '<p>The key question for many travelers in 2026. In short:</p>\n'
    + _t3(["Card", "Works?", "Where"], [
        ["Visa / Mastercard (non-RU)", "yes", "~90% of places in Tbilisi, ATMs"],
        ["Mir card (Russia)", "no", "not accepted anywhere"],
        ["UnionPay", "partly", "some ATMs and malls"],
        ["Georgian / Armenian / Kazakh bank cards", "yes", "everywhere"],
    ]) +
    '\n<p>The key point: <strong>Russian-issued Visa/Mastercard and Mir cards do not work in Georgia</strong> due to sanctions. Cards issued outside Russia work fine. If you\'re coming from Russia, the usual working options are a card from another country (Armenia, Kazakhstan, UAE) or cash. For exchange rates and where to change money, see <a href="/en/blog/georgia-first-time-tips/">our first-time guide →</a>.</p>\n'
    '<h2 id="atm">ATMs: where and how much to withdraw</h2>\n'
    '<p>Tbilisi has plenty of ATMs: TBC, Bank of Georgia, Liberty — on every corner. Withdrawing lari with a foreign Visa/Mastercard is no problem. A few notes:</p>\n'
    '<ul>\n'
    '<li>Per-transaction limit is usually ₾2,000-3,000, depending on the ATM.</li>\n'
    '<li>The ATM may offer "conversion in your currency" (DCC) — <strong>always decline</strong> and withdraw in lari; your bank\'s rate is better.</li>\n'
    '<li>Some TBC and Bank of Georgia ATMs dispense US dollars — handy if you need cash in USD.</li>\n'
    '</ul>\n'
    '<h2 id="cash">Where you need cash</h2>\n'
    '<p>You can pay by card almost everywhere in Tbilisi, but <strong>always keep some lari in cash</strong>. You\'ll need it here:</p>\n'
    '<ul>\n'
    '<li>Markets and small shops (churchkhela, spices, souvenirs).</li>\n'
    '<li>Some taxis, especially street ones — see the <a href="/en/blog/tbilisi-taxi-guide/">Tbilisi taxi guide →</a>.</li>\n'
    '<li>Minibuses (marshrutka) and rural transport.</li>\n'
    '<li>Small family cafés and guesthouses in the regions (Kazbegi, Svaneti).</li>\n'
    '<li>Tips where there\'s no terminal — see <a href="/en/blog/tipping-in-georgia/">tipping in Georgia →</a>.</li>\n'
    '</ul>\n'
    '<h2 id="fees">Fees and conversion</h2>\n'
    '<p>When you pay in a currency other than your home one, your issuing bank charges a conversion fee (usually 0.5-2%). Within Georgia, shops and restaurants add nothing extra for card payment. The main trap is DCC ("pay in your currency"): the terminal offers to lock the amount in your currency at a poor rate. Always choose to pay <strong>in lari</strong>.</p>\n'
    '<h2 id="account">Should you open a Georgian bank account</h2>\n'
    '<p>For a short trip — <strong>no need</strong>; cash and a foreign card are enough. An account at TBC or Bank of Georgia makes sense for expats and long-stayers: you get a local card that works everywhere. For settling in Tbilisi long-term, see our guide to <a href="/en/blog/georgia-guide-or-solo/">exploring Georgia →</a>.</p>\n'
    '<h2 id="tips">Practical tips</h2>\n'
    '<ul>\n'
    '<li>Bring some cash dollars/euros — they\'re easy and cheap to change into lari.</li>\n'
    '<li>Don\'t keep all your money on one card; hold part in cash.</li>\n'
    '<li>Exchange is better at city bureaus than at the airport (worse rate there).</li>\n'
    '<li>Planning a budget? Check <a href="/en/blog/georgia-first-time-tips/">Georgia first-time tips →</a>.</li>\n'
    '<li>Don\'t forget travel insurance — mandatory to enter Georgia since 2026.</li>\n'
    '</ul>'
)
_A5_FAQ_PAIRS_EN = [
    ("Which cards work in Georgia in 2026?",
     "Visa and Mastercard issued outside Russia work — accepted at about 90% of places in Tbilisi and at ATMs. Russian Mir cards and Russian-issued Visa/Mastercard do not work due to sanctions. UnionPay is accepted only in some places."),
    ("Does the Mir card work in Georgia?",
     "No, Mir cards are not accepted anywhere in Georgia — neither in shops nor at ATMs. Travelers from Russia need cash or a card issued in another country (Armenia, Kazakhstan, UAE)."),
    ("Where can I withdraw cash lari in Tbilisi?",
     "At TBC, Bank of Georgia and Liberty ATMs — they're all over the city. Withdrawing with a foreign Visa/Mastercard is easy. Decline the 'conversion in your currency' (DCC) option and take lari for a better rate."),
    ("Do I need cash in Georgia or is a card enough?",
     "You can pay by card almost everywhere in Tbilisi, but always keep some lari in cash: you'll need it at markets, in some taxis, on minibuses, and at family cafés and guesthouses in the regions."),
    ("Should a tourist open a Georgian bank account?",
     "For a short trip there's no need — cash and a foreign card are enough. An account at TBC or Bank of Georgia makes sense for expats and long-stayers: a local card works everywhere without limits."),
]
_A5_FAQ_EN = _faq("FAQ", _A5_FAQ_PAIRS_EN)
_A5_CARDS_EN = _cards([
    ("Guide", "Tipping in Georgia", "How much to tip in cafés, taxis and hotels.", "/en/blog/tipping-in-georgia/", "Read →"),
    ("Guide", "Tbilisi taxi guide", "Bolt, Yandex Go and city ride prices.", "/en/blog/tbilisi-taxi-guide/", "Read →"),
    ("Guide", "Georgia first time", "25 tips from a local guide.", "/en/blog/georgia-first-time-tips/", "Read →"),
])
_A5_READALSO_EN = _readalso("Read also:", [
    ("/en/blog/tipping-in-georgia/", "Tipping in Georgia: how much and to whom →"),
    ("/en/blog/tbilisi-taxi-guide/", "Tbilisi taxi guide: Bolt, Yandex, prices →"),
    ("/en/blog/georgian-phrases-tourists/", "Georgian phrases: 40 words for tourists →"),
    ("/en/tours-in-georgia/", "Georgia tours with a guide →"),
])


ARTICLES = [
    {
        "ru_slug": "gruzinskie-frazy",
        "en_slug": "georgian-phrases-tourists",
        "ru": {
            "title": "Грузинский разговорник 2026: 40 фраз для туриста с переводом",
            "desc": "40 грузинских фраз с транскрипцией: приветствия, в кафе, такси, покупки, экстренное. Как сказать спасибо и попросить счёт по-грузински. От гида из Тбилиси.",
            "keywords": "грузинский разговорник, фразы на грузинском, грузинские фразы для туриста, как сказать спасибо по-грузински, гамарджоба, полезные фразы грузия",
            "hero": "gruzinskie-frazy",
            "pub": "2026-07-18", "mod": "2026-07-18",
            "schema": build_schema(
                "ru", "gruzinskie-frazy", "georgian-phrases-tourists",
                "Грузинский разговорник: 40 фраз для туриста с транскрипцией (2026)",
                "40 грузинских фраз с транскрипцией: приветствия, в кафе, такси, покупки, экстренное. Как сказать спасибо и попросить счёт по-грузински. От гида из Тбилиси.",
                "gruzinskie-frazy", "2026-07-18", "2026-07-18",
                "Грузинский разговорник: 40 фраз", _A1_FAQ_PAIRS_RU),
            "body": ru_region(
                "Грузинский разговорник: 40 фраз", 8,
                "Грузинский разговорник: 40 фраз для туриста с транскрипцией (2026)",
                "18 июля 2026",
                "<strong>Грузинский разговорник</strong> нужен не для того, чтобы заговорить свободно, а чтобы расположить к себе. Я живу в Тбилиси с 2023 года и вижу это каждый день: турист говорит «гамарджоба» и «мадлоба» — и отношение к нему меняется мгновенно. Собрал 40 фраз, которые реально работают в кафе, такси и на рынке. С транскрипцией русскими буквами — читать грузинский алфавит для этого не нужно.",
                _A1_TOC_RU, _A1_BODY_RU,
                "Хотите живой Тбилиси и пару настоящих фраз по дороге?",
                "Обзорный тур по Тбилиси — все главные точки за 4 часа, группа до 7 человек, русскоязычный гид, трансфер от отеля.",
                "/ekskursiya/sovetskiy-tur-tbilisi/", "Подробнее о туре →",
                "Хочу+обзорный+тур+по+Тбилиси", "/tury-v-gruziyu/",
                _A1_READALSO_RU, _A1_CARDS_RU, _A1_FAQ_RU,
            ),
        },
        "en": {
            "title": "Georgian Phrases 2026: 40 Words Every Tourist Needs",
            "desc": "40 Georgian phrases with pronunciation: greetings, café, taxi, emergencies. How to say thank you and ask for the bill in Georgian. From a Tbilisi guide.",
            "keywords": "georgian phrases, useful georgian phrases for tourists, how to say thank you in georgian, gamarjoba meaning, basic georgian words, georgia language tourist",
            "hero": "gruzinskie-frazy",
            "pub": "2026-07-18", "mod": "2026-07-18",
            "schema": build_schema(
                "en", "gruzinskie-frazy", "georgian-phrases-tourists",
                "Georgian Phrases: 40 Words Every Tourist Needs (2026)",
                "40 Georgian phrases with pronunciation: greetings, café, taxi, emergencies. How to say thank you and ask for the bill in Georgian. From a Tbilisi guide.",
                "gruzinskie-frazy", "2026-07-18", "2026-07-18",
                "Georgian Phrases: 40 Words", _A1_FAQ_PAIRS_EN),
            "body": en_region(
                "Georgian Phrases: 40 Words", 8,
                "Georgian Phrases: 40 Words Every Tourist Needs (2026)",
                "July 18, 2026",
                "<strong>A Georgian phrasebook</strong> isn't about speaking fluently — it's about winning people over. I've lived in Tbilisi since 2023 and I see it daily: a tourist says gamarjoba and madloba, and the whole interaction changes. Here are 40 phrases that actually work in cafés, taxis and markets, with simple pronunciation — you don't need to read the Georgian alphabet for any of them.",
                _A1_TOC_EN, _A1_BODY_EN,
                "Want the real Tbilisi and a few genuine phrases along the way?",
                "A Tbilisi walking tour — all the highlights in 4 hours, groups up to 7, a local guide, hotel pickup.",
                "/en/tours-in-georgia/", "Tour details →",
                "I+want+a+Tbilisi+city+tour", "/en/tours-in-georgia/",
                _A1_READALSO_EN, _A1_CARDS_EN, _A1_FAQ_EN,
            ),
        },
    },
    {
        "ru_slug": "chaevye-v-gruzii",
        "en_slug": "tipping-in-georgia",
        "ru": {
            "title": "Чаевые в Грузии 2026: сколько оставлять в кафе, такси, отеле",
            "desc": "Чаевые в Грузии: сколько принято в ресторане (10%), что такое service charge, нужно ли давать таксисту и гиду. Шпаргалка сумм от гида из Тбилиси.",
            "keywords": "чаевые в грузии, сколько чаевых в грузии, чаевые в ресторане грузия, service charge грузия, чаевые таксисту грузия, чаевые гиду",
            "hero": "chaevye-v-gruzii",
            "pub": "2026-07-18", "mod": "2026-07-18",
            "schema": build_schema(
                "ru", "chaevye-v-gruzii", "tipping-in-georgia",
                "Чаевые в Грузии 2026: сколько оставлять в кафе, такси, отеле",
                "Чаевые в Грузии: сколько принято в ресторане (10%), что такое service charge, нужно ли давать таксисту и гиду. Шпаргалка сумм от гида из Тбилиси.",
                "chaevye-v-gruzii", "2026-07-18", "2026-07-18",
                "Чаевые в Грузии 2026", _A2_FAQ_PAIRS_RU),
            "body": ru_region(
                "Чаевые в Грузии", 7,
                "Чаевые в Грузии 2026: сколько оставлять и кому",
                "18 июля 2026",
                "<strong>Чаевые в Грузии</strong> — тема, где легко переплатить или показаться скупым. Я живу в Тбилиси с 2023 года и вижу обе крайности: одни оставляют 20% сверху уже включённого service charge, другие не понимают, что «на чай» тут уже почти норма. Разложил по полочкам: сколько, где и кому — с реальными суммами в лари.",
                _A2_TOC_RU, _A2_BODY_RU,
                "Хотите день в Тбилиси без забот о ценах и чаевых?",
                "Обзорный тур — фиксированная цена, работа гида включена, никаких скрытых доплат. Группа до 7 человек, трансфер от отеля.",
                "/ekskursiya/sovetskiy-tur-tbilisi/", "Подробнее о туре →",
                "Хочу+обзорный+тур+по+Тбилиси", "/tury-v-gruziyu/",
                _A2_READALSO_RU, _A2_CARDS_RU, _A2_FAQ_RU,
            ),
        },
        "en": {
            "title": "Tipping in Georgia 2026: How Much in Cafés, Taxis, Hotels",
            "desc": "Tipping in Georgia: how much in a restaurant (10%), what a service charge is, whether to tip drivers and guides. A cheat sheet of amounts from a Tbilisi guide.",
            "keywords": "tipping in georgia, how much to tip in georgia, restaurant tip georgia, service charge georgia, tipping taxi georgia, tip tour guide georgia",
            "hero": "chaevye-v-gruzii",
            "pub": "2026-07-18", "mod": "2026-07-18",
            "schema": build_schema(
                "en", "chaevye-v-gruzii", "tipping-in-georgia",
                "Tipping in Georgia 2026: How Much in Cafés, Taxis, Hotels",
                "Tipping in Georgia: how much in a restaurant (10%), what a service charge is, whether to tip drivers and guides. A cheat sheet of amounts from a Tbilisi guide.",
                "chaevye-v-gruzii", "2026-07-18", "2026-07-18",
                "Tipping in Georgia 2026", _A2_FAQ_PAIRS_EN),
            "body": en_region(
                "Tipping in Georgia", 7,
                "Tipping in Georgia 2026: How Much and to Whom",
                "July 18, 2026",
                "<strong>Tipping in Georgia</strong> is where it's easy to overpay or look stingy. I've lived in Tbilisi since 2023 and see both extremes: some add 20% on top of an already-included service charge, others don't realize tipping is now almost the norm. Here's the clear breakdown — how much, where and to whom, with real amounts in lari.",
                _A2_TOC_EN, _A2_BODY_EN,
                "Want a day in Tbilisi with no worries about prices or tips?",
                "A city tour — fixed price, guide's work included, no hidden extras. Groups up to 7, hotel pickup.",
                "/en/tours-in-georgia/", "Tour details →",
                "I+want+a+Tbilisi+city+tour", "/en/tours-in-georgia/",
                _A2_READALSO_EN, _A2_CARDS_EN, _A2_FAQ_EN,
            ),
        },
    },
    {
        "ru_slug": "taksi-tbilisi",
        "en_slug": "tbilisi-taxi-guide",
        "ru": {
            "title": "Такси в Тбилиси 2026: Bolt, Yandex, цены и как не переплатить",
            "desc": "Такси в Тбилиси: приложения Bolt и Yandex Go, реальные цены по городу и из аэропорта, оплата картой, уличное такси и торг. Лайфхаки от местного гида.",
            "keywords": "такси в тбилиси, bolt тбилиси, яндекс такси тбилиси, такси из аэропорта тбилиси, цены на такси тбилиси, такси грузия",
            "hero": "taksi-tbilisi",
            "pub": "2026-07-18", "mod": "2026-07-18",
            "schema": build_schema(
                "ru", "taksi-tbilisi", "tbilisi-taxi-guide",
                "Такси в Тбилиси 2026: Bolt, Yandex, цены и как не переплатить",
                "Такси в Тбилиси: приложения Bolt и Yandex Go, реальные цены по городу и из аэропорта, оплата картой, уличное такси и торг. Лайфхаки от местного гида.",
                "taksi-tbilisi", "2026-07-18", "2026-07-18",
                "Такси в Тбилиси 2026", _A3_FAQ_PAIRS_RU),
            "body": ru_region(
                "Такси в Тбилиси", 7,
                "Такси в Тбилиси 2026: Bolt, Yandex и как не переплатить",
                "18 июля 2026",
                "<strong>Такси в Тбилиси</strong> дешёвое, но новичок легко переплачивает в 2-3 раза — особенно в аэропорту. Я живу здесь с 2023 года и езжу на такси каждый день. Главный совет: ставьте приложение и почти никогда не ловите машину на улице. Разложил по полочкам: Bolt против Yandex, реальные цены в лари, аэропорт, оплата и безопасность.",
                _A3_TOC_RU, _A3_BODY_RU,
                "Нужна поездка за город без счётчика и торга?",
                "Индивидуальный трансфер или тур с водителем: фиксированная цена на весь день, комфортное авто, встреча у отеля.",
                "/tury-v-gruziyu/", "Смотреть туры →",
                "Хочу+трансфер+по+Грузии", "/tury-v-gruziyu/",
                _A3_READALSO_RU, _A3_CARDS_RU, _A3_FAQ_RU,
            ),
        },
        "en": {
            "title": "Tbilisi Taxi Guide 2026: Bolt, Yandex, Prices & Tips",
            "desc": "Taxis in Tbilisi: the Bolt and Yandex Go apps, real city and airport prices, paying by card, street taxis and haggling. Practical tips from a local guide.",
            "keywords": "tbilisi taxi, bolt tbilisi, yandex go tbilisi, taxi from tbilisi airport, tbilisi taxi prices, taxi in georgia",
            "hero": "taksi-tbilisi",
            "pub": "2026-07-18", "mod": "2026-07-18",
            "schema": build_schema(
                "en", "taksi-tbilisi", "tbilisi-taxi-guide",
                "Tbilisi Taxi Guide 2026: Bolt, Yandex, Prices & Tips",
                "Taxis in Tbilisi: the Bolt and Yandex Go apps, real city and airport prices, paying by card, street taxis and haggling. Practical tips from a local guide.",
                "taksi-tbilisi", "2026-07-18", "2026-07-18",
                "Tbilisi Taxi Guide 2026", _A3_FAQ_PAIRS_EN),
            "body": en_region(
                "Tbilisi Taxi Guide", 7,
                "Tbilisi Taxi Guide 2026: Bolt, Yandex and How Not to Overpay",
                "July 18, 2026",
                "<strong>Taxis in Tbilisi</strong> are cheap, but a newcomer easily overpays 2-3× — especially at the airport. I've lived here since 2023 and take taxis every day. The main tip: use the app and almost never flag a car on the street. Here's the full breakdown: Bolt vs Yandex, real prices in lari, the airport, payment and safety.",
                _A3_TOC_EN, _A3_BODY_EN,
                "Need an out-of-town trip with no meter or haggling?",
                "A private transfer or tour with a driver: a fixed price for the whole day, a comfortable car, hotel pickup.",
                "/en/tours-in-georgia/", "See tours →",
                "I+want+a+transfer+in+Georgia", "/en/tours-in-georgia/",
                _A3_READALSO_EN, _A3_CARDS_EN, _A3_FAQ_EN,
            ),
        },
    },
    {
        "ru_slug": "gruzinskie-sladosti",
        "en_slug": "georgian-sweets-desserts",
        "ru": {
            "title": "Грузинские сладости 2026: чурчхела, пеламуши и что попробовать",
            "desc": "Грузинские сладости: чурчхела, пеламуши, козинаки, тклапи, када и назуки. Что это, чем отличаются, где попробовать и купить в Тбилиси. Гид от местного.",
            "keywords": "грузинские сладости, чурчхела, пеламуши, козинаки гозинаки, тклапи, грузинские десерты, что попробовать сладкое в грузии",
            "hero": "gruzinskie-sladosti",
            "pub": "2026-07-18", "mod": "2026-07-18",
            "schema": build_schema(
                "ru", "gruzinskie-sladosti", "georgian-sweets-desserts",
                "Грузинские сладости 2026: чурчхела, пеламуши и что попробовать",
                "Грузинские сладости: чурчхела, пеламуши, козинаки, тклапи, када и назуки. Что это, чем отличаются, где попробовать и купить в Тбилиси. Гид от местного.",
                "gruzinskie-sladosti", "2026-07-18", "2026-07-18",
                "Грузинские сладости", _A4_FAQ_PAIRS_RU),
            "body": ru_region(
                "Грузинские сладости", 8,
                "Грузинские сладости: чурчхела, пеламуши и что попробовать",
                "18 июля 2026",
                "<strong>Грузинские сладости</strong> — это не только чурчхела, хотя с неё стоит начать. Почти все они построены на винограде, орехах и мёде, а не на промышленном сахаре — потому и вкус другой. Я живу в Тбилиси с 2023 года и вожу гостей по рынкам и пекарням. Собрал главные десерты: что попробовать, чем они отличаются и где купить настоящие, а не туристические.",
                _A4_TOC_RU, _A4_BODY_RU,
                "Хотите продегустировать сладости и вино там, где их делают?",
                "Гастрономический выезд в Кахетию: винный погреб, чурчхела и обед с видом на виноградники. Группа до 7 человек.",
                "/tury-v-gruziyu/", "Смотреть туры →",
                "Хочу+гастротур+по+Грузии", "/tury-v-gruziyu/",
                _A4_READALSO_RU, _A4_CARDS_RU, _A4_FAQ_RU,
            ),
        },
        "en": {
            "title": "Georgian Sweets 2026: Churchkhela, Pelamushi & What to Try",
            "desc": "Georgian sweets: churchkhela, pelamushi, gozinaki, tklapi, kada and nazuki. What they are, how they differ, and where to try and buy them in Tbilisi.",
            "keywords": "georgian sweets, churchkhela, pelamushi, gozinaki, tklapi, georgian desserts, what sweets to try in georgia",
            "hero": "gruzinskie-sladosti",
            "pub": "2026-07-18", "mod": "2026-07-18",
            "schema": build_schema(
                "en", "gruzinskie-sladosti", "georgian-sweets-desserts",
                "Georgian Sweets 2026: Churchkhela, Pelamushi & What to Try",
                "Georgian sweets: churchkhela, pelamushi, gozinaki, tklapi, kada and nazuki. What they are, how they differ, and where to try and buy them in Tbilisi.",
                "gruzinskie-sladosti", "2026-07-18", "2026-07-18",
                "Georgian Sweets", _A4_FAQ_PAIRS_EN),
            "body": en_region(
                "Georgian Sweets", 8,
                "Georgian Sweets: Churchkhela, Pelamushi and What to Try",
                "July 18, 2026",
                "<strong>Georgian sweets</strong> are more than churchkhela, though that's where to start. Almost all of them are built on grapes, nuts and honey rather than industrial sugar — which is why they taste different. I've lived in Tbilisi since 2023 and take guests around the markets and bakeries. Here are the key desserts: what to try, how they differ, and where to buy the real thing.",
                _A4_TOC_EN, _A4_BODY_EN,
                "Want to taste sweets and wine where they're made?",
                "A food trip to Kakheti: a wine cellar, churchkhela and lunch overlooking the vineyards. Groups up to 7.",
                "/en/tours-in-georgia/", "See tours →",
                "I+want+a+food+tour+in+Georgia", "/en/tours-in-georgia/",
                _A4_READALSO_EN, _A4_CARDS_EN, _A4_FAQ_EN,
            ),
        },
    },
    {
        "ru_slug": "karty-nalichnye-gruziya",
        "en_slug": "money-cards-georgia",
        "ru": {
            "title": "Карты и наличные в Грузии 2026: какие работают, банкоматы",
            "desc": "Какие карты работают в Грузии: Visa/Mastercard да, «Мир» нет, UnionPay частично. Где снять наличные, банкоматы, комиссии и DCC. Гид от местного.",
            "keywords": "карты в грузии, какие карты работают в грузии, наличные в грузии, банкоматы тбилиси, карта мир грузия, снять наличные грузия",
            "hero": "karty-nalichnye-gruziya",
            "pub": "2026-07-18", "mod": "2026-07-18",
            "schema": build_schema(
                "ru", "karty-nalichnye-gruziya", "money-cards-georgia",
                "Карты и наличные в Грузии 2026: какие работают, банкоматы",
                "Какие карты работают в Грузии: Visa/Mastercard да, «Мир» нет, UnionPay частично. Где снять наличные, банкоматы, комиссии и DCC. Гид от местного.",
                "karty-nalichnye-gruziya", "2026-07-18", "2026-07-18",
                "Карты и наличные в Грузии", _A5_FAQ_PAIRS_RU),
            "body": ru_region(
                "Карты и наличные в Грузии", 8,
                "Карты и наличные в Грузии 2026: какие работают и где снять",
                "18 июля 2026",
                "<strong>Карты и наличные в Грузии</strong> — первое, о чём спрашивают перед поездкой в 2026 году. Российские «Мир» и Visa/Mastercard не работают, зарубежные — да. Я живу в Тбилиси с 2023 года и помогаю гостям разобраться с деньгами каждую неделю. Разложил чётко: какие карты принимают, где снять лари, как не попасть на невыгодную конвертацию и сколько держать кэшем.",
                _A5_TOC_RU, _A5_BODY_RU,
                "Планируете поездку и не хотите разбираться с деталями?",
                "Возьмите тур с гидом — подскажем по деньгам, обмену и всему на месте. Группа до 7 человек, трансфер от отеля.",
                "/ekskursiya/sovetskiy-tur-tbilisi/", "Подробнее о туре →",
                "Хочу+обзорный+тур+по+Тбилиси", "/tury-v-gruziyu/",
                _A5_READALSO_RU, _A5_CARDS_RU, _A5_FAQ_RU,
            ),
        },
        "en": {
            "title": "Money & Cards in Georgia 2026: What Works, ATMs, Cash",
            "desc": "Which cards work in Georgia: Visa/Mastercard yes, Mir no, UnionPay partly. Where to withdraw cash, ATMs, fees and DCC. A practical guide from a local.",
            "keywords": "cards in georgia, which cards work in georgia, cash in georgia, atms tbilisi, mir card georgia, withdraw cash georgia",
            "hero": "karty-nalichnye-gruziya",
            "pub": "2026-07-18", "mod": "2026-07-18",
            "schema": build_schema(
                "en", "karty-nalichnye-gruziya", "money-cards-georgia",
                "Money & Cards in Georgia 2026: What Works, ATMs, Cash",
                "Which cards work in Georgia: Visa/Mastercard yes, Mir no, UnionPay partly. Where to withdraw cash, ATMs, fees and DCC. A practical guide from a local.",
                "karty-nalichnye-gruziya", "2026-07-18", "2026-07-18",
                "Money & Cards in Georgia", _A5_FAQ_PAIRS_EN),
            "body": en_region(
                "Money & Cards in Georgia", 8,
                "Money & Cards in Georgia 2026: What Works and Where to Withdraw",
                "July 18, 2026",
                "<strong>Money and cards in Georgia</strong> are the first thing travelers ask about in 2026. Russian Mir and Visa/Mastercard don't work; foreign-issued cards do. I've lived in Tbilisi since 2023 and help guests with money every week. Here's the clear breakdown: which cards are accepted, where to withdraw lari, how to avoid a bad conversion, and how much to keep in cash.",
                _A5_TOC_EN, _A5_BODY_EN,
                "Planning a trip and don't want to deal with the details?",
                "Take a guided tour — we'll help with money, exchange and everything on the ground. Groups up to 7, hotel pickup.",
                "/en/tours-in-georgia/", "Tour details →",
                "I+want+a+Tbilisi+city+tour", "/en/tours-in-georgia/",
                _A5_READALSO_EN, _A5_CARDS_EN, _A5_FAQ_EN,
            ),
        },
    },
]
