#!/usr/bin/env python3
"""Build the "переводчик и сопровождение" content cluster (ru/en/ge).

One generator for all 15 pages: shared head/nav/footer/schema, per-article
content. Emits full HTML matching the blog template, computes real wordCount,
and writes to the correct paths. Run: python3 scripts/cluster/build_cluster.py [--apply]
"""
import os
import re
import sys
import json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
APPLY = "--apply" in sys.argv
ONLY = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--lang=")), None)

GA4 = "G-3X83YZHY6S"

# ── shared CSS (copied verbatim from blog template) ───────────────────────────
STYLE = """*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Lora',Georgia,serif;color:#111827;background:#fff;overflow-x:hidden;-webkit-font-smoothing:antialiased;padding-top:72px}
a{text-decoration:none;color:inherit}
img{max-width:100%;display:block;object-fit:cover}
button{border:none;background:none;font-family:inherit;cursor:pointer}
ul{list-style:none}
#nav{position:fixed;top:0;left:0;right:0;z-index:900;height:72px;display:flex;align-items:center;justify-content:space-between;padding:0 clamp(16px,3.5vw,56px);background:#1F2937}
.nav-logo{display:flex;align-items:center;color:#fff}
.logo-svg{width:148px;height:66px;display:block}
.nav-links{display:flex;align-items:center;gap:24px}
.nav-links a{white-space:nowrap;font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#fff;transition:color .2s}
.nav-links a:hover{color:#1A3D2E}
.nav-btn{background:#1A3D2E;color:#fff!important;padding:9px 22px;border-radius:9999px;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
.burger{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:10px 8px;min-width:44px;min-height:44px;justify-content:center;align-items:center}
.burger span{display:block;width:24px;height:2px;background:#fff;border-radius:2px;transition:.3s}
.burger.on span:nth-child(1){transform:translateY(7px) rotate(45deg)}
.burger.on span:nth-child(2){opacity:0}
.burger.on span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
.drawer{display:none;position:fixed;top:72px;left:0;right:0;bottom:0;background:#fff;z-index:850;flex-direction:column;padding:28px 24px;border-top:1px solid #f3f4f6}
.drawer.on{display:flex}
.drawer a{font-size:17px;font-weight:600;color:#111827;padding:15px 0;border-bottom:1px solid #f3f4f6}
.article-hero{background:#1F2937;padding:52px clamp(16px,3.5vw,56px) 48px;color:#fff}
.breadcrumb{font-size:13px;color:rgba(255,255,255,.8);margin-bottom:16px;display:flex;align-items:center;gap:8px;min-height:44px;flex-wrap:wrap}
.breadcrumb a{color:rgba(255,255,255,.5)}
.breadcrumb a:hover{color:#fff}
.breadcrumb span{color:rgba(255,255,255,.8)}
.article-label{font-size:10px;font-weight:700;letter-spacing:.28em;text-transform:uppercase;color:#60A5FA;margin-bottom:12px}
.article-h1{font-size:clamp(26px,3.5vw,46px);font-weight:700;line-height:1.15;margin-bottom:14px}
.article-meta{font-size:12px;color:rgba(255,255,255,.8);display:flex;gap:16px;flex-wrap:wrap}
.article-wrap{max-width:760px;margin:0 auto;padding:52px clamp(16px,3.5vw,32px)}
.article-toc{background:#F0FDF4;border:1px solid #BFDBFE;border-radius:12px;padding:24px 28px;margin-bottom:40px}
.article-toc h2{font-size:14px;font-weight:700;color:#1A3D2E;margin-bottom:12px;text-transform:uppercase;letter-spacing:.1em}
.article-toc ol{padding-left:20px;display:flex;flex-direction:column;gap:2px;list-style:decimal}
.article-toc li a{font-size:14px;color:#1A3D2E;display:block;padding:6px 0;min-height:44px;line-height:1.5}
.article-body h2{font-size:clamp(20px,2.5vw,28px);font-weight:700!important;color:#111827;margin:40px 0 16px;padding-top:8px;border-top:2px solid #EFF6FF}
.article-body h3{font-size:18px;font-weight:700!important;color:#111827;margin:28px 0 12px}
.article-body p{font-size:16px;color:#374151;line-height:1.85;margin-bottom:16px}
.article-body ul,.article-body ol{margin:16px 0 20px;padding-left:0;display:flex;flex-direction:column;gap:8px;list-style:none}
.article-body li{font-size:16px;color:#374151;line-height:1.7;padding-left:20px;position:relative}
.article-body li::before{content:'→';position:absolute;left:0;color:#1A3D2E;font-weight:700}
.article-body ol{counter-reset:item}
.article-body ol li{counter-increment:item;padding-left:28px}
.article-body ol li::before{content:counter(item)'.';position:absolute;left:0;color:#1A3D2E;font-weight:700;font-size:13px}
.article-body strong{color:#111827;font-weight:700}
.info-box{background:#F0FDF4;border-left:4px solid #1A3D2E;border-radius:0 8px 8px 0;padding:16px 20px;margin:24px 0;font-size:14px;color:#1A3D2E;line-height:1.7}
.warn-box{background:#FEF3C7;border-left:4px solid #F59E0B;border-radius:0 8px 8px 0;padding:16px 20px;margin:24px 0;font-size:14px;color:#92400E;line-height:1.7}
.review-quote{background:#FFFBEB;border:1px solid #FDE68A;border-radius:16px;padding:28px 28px 20px;margin:32px 0;position:relative}
.review-quote-text{font-size:16px;color:#374151;line-height:1.8;font-style:italic;margin-bottom:12px}
.review-quote-author{font-size:12px;font-weight:700;color:#92400E;letter-spacing:.05em}
.price-table{width:100%;border-collapse:collapse;border-radius:8px;overflow:hidden;min-width:420px;margin:24px 0}
.price-table th{background:#1A3D2E;color:#fff;font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:12px 16px;text-align:left}
.price-table td{padding:12px 16px;border-bottom:1px solid #F3F4F6;font-size:14px;color:#374151}
.price-table tr:last-child td{border-bottom:none}
.price-table tr:nth-child(even) td{background:#F9FAFB}
.article-cta{background:#1F2937;border-radius:16px;padding:32px 28px;margin:40px 0;text-align:center}
.article-cta h3{font-size:22px;font-weight:700;color:#fff;margin-bottom:8px}
.article-cta p{font-size:13px;color:rgba(255,255,255,.85);margin-bottom:20px}
.btn-wa{display:inline-flex;align-items:center;gap:8px;background:#0C7C38;color:#fff;padding:13px 24px;border-radius:9999px;font-size:13px;font-weight:700}
.related{padding:48px clamp(16px,3.5vw,56px);background:#F9FAFB}
.related h2{font-size:22px;font-weight:700;color:#111827;margin-bottom:28px;max-width:760px;margin-left:auto;margin-right:auto}
.related-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;max-width:760px;margin:0 auto}
.rc-card{background:#fff;border:1px solid #E5E7EB;border-radius:12px;padding:20px}
.rc-card-label{font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#1A3D2E;margin-bottom:6px}
.rc-card h3{font-size:16px;font-weight:700;color:#111827;margin-bottom:8px;line-height:1.3}
.rc-card p{font-size:12px;color:#6B7280;margin-bottom:14px;line-height:1.6}
.rc-card a{font-size:12px;font-weight:700;color:#1A3D2E;letter-spacing:.06em}
#faq{padding:48px clamp(16px,3.5vw,56px);background:#fff}
.faq-inner{max-width:760px;margin:0 auto}
.faq-inner h2{font-size:22px;font-weight:700;color:#111827;margin-bottom:28px}
.fi{border-bottom:1px solid #E5E7EB}
.fq{width:100%;text-align:left;padding:18px 0;display:flex;align-items:center;justify-content:space-between;gap:12px;font-size:16px;font-weight:600;color:#111827;cursor:pointer}
.fq-ic{width:28px;height:28px;border-radius:50%;background:#F3F4F6;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:700;color:#1A3D2E;flex-shrink:0;transition:transform .3s,background .2s}
.fi.open .fq-ic{transform:rotate(45deg);background:#1A3D2E;color:#fff}
.fa{max-height:0;overflow:hidden;transition:max-height .38s ease}
.fa-inner{padding:0 0 16px;font-size:14px;color:#6B7280;line-height:1.9}
.article-lead{background:#F0FDF4;border-left:3px solid #1A3D2E;border-radius:8px;padding:14px 18px;font-size:16px;color:#1e3a5f;line-height:1.75;margin-bottom:28px}
.sources-block{background:#F0FDF4;border:1px solid #BBF7D0;border-radius:10px;padding:16px 20px;margin:32px 0}
.sources-title{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#166534;margin-bottom:10px}
.sources-block ul{padding-left:0}
.sources-block li{font-size:13px;color:#374151;padding-left:16px;position:relative;margin-bottom:6px}
.sources-block li::before{content:"→";position:absolute;left:0;color:#15803D}
.sources-block a{color:#1A3D2E}
#footer{background:#111827;padding:52px clamp(16px,3.5vw,56px) 28px}
.foot-grid{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:44px;margin-bottom:40px}
.foot-brand{font-size:17px;font-weight:800;color:#fff;margin-bottom:8px}
.foot-desc{font-size:13px;color:rgba(255,255,255,.65);line-height:1.8}
.foot-grid div h3{font-size:12px;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:rgba(255,255,255,.7);margin-bottom:14px}
.foot-links{display:flex;flex-direction:column;gap:9px}
.foot-links a{font-size:13px;color:rgba(255,255,255,.5)}
.foot-links a:hover{color:#fff}
.foot-bottom{max-width:1100px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;padding-top:22px;border-top:1px solid rgba(255,255,255,.08);flex-wrap:wrap;gap:8px}
.foot-copy{font-size:12px;color:rgba(255,255,255,.65)}
.foot-legal{display:flex;gap:16px}
.foot-legal a{font-size:11px;color:rgba(255,255,255,.7)}
h1,h2,h3{font-family:'Lora',Georgia,serif!important;font-weight:400!important}
@media(max-width:960px){.nav-links{display:none}.burger{display:flex}.foot-grid{grid-template-columns:1fr;gap:28px}.related-grid{grid-template-columns:1fr}}
@media(max-width:480px){.price-table{font-size:13px}.article-toc{padding:16px 18px}}"""

NAV_LABELS = {
    "ru": ["Туры в Грузию", "Экскурсии", "Блог", "Контакты", "Забронировать"],
    "en": ["Private guide", "Home", "Blog", "Contacts", "Book now"],
    "ge": ["კერძო გიდი", "მთავარი", "ბლოგი", "კონტაქტი", "დაჯავშნა"],
}
# only live targets (verified: /en/tours/ and /ge/tours/ do NOT exist)
NAV_HREF = {
    "ru": ["/tury-v-gruziyu/", "/ekskursiya/", "/blog/", "/contacts/", "/booking/"],
    "en": ["/en/private-guide-tbilisi/", "/en/", "/en/blog/", "/en/contacts/", "/en/booking/"],
    "ge": ["/ge/private-guide-tbilisi/", "/ge/", "/ge/blog/", "/ge/contacts/", "/ge/booking/"],
}
BLOG_NAME = {"ru": "Блог", "en": "Blog", "ge": "ბლოგი"}
HOME_NAME = {"ru": "Главная", "en": "Home", "ge": "მთავარი"}
FOOT_DESC = {
    "ru": "Русскоязычный гид и сопровождение по Грузии. Тбилиси, Казбеги, Кахетия.",
    "en": "English- and Russian-speaking guide and support across Georgia.",
    "ge": "რუსულ- და ინგლისურენოვანი გიდი და თანხლება საქართველოში.",
}


def wc(*html_parts):
    text = " ".join(html_parts)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return len([w for w in text.split(" ") if w])


def logo_svg():
    return (
        '<svg aria-hidden="true" class="logo-svg" fill="none" viewbox="0 0 118 66" xmlns="http://www.w3.org/2000/svg">'
        '<path d="M4 34 L20 20 L32 27 L59 14 L86 27 L98 20 L114 34 Z" fill="currentColor"></path>'
        '<text fill="currentColor" font-family="Raleway,sans-serif" font-size="15" font-weight="800" letter-spacing="3" text-anchor="middle" x="59" y="53">SAKHVA</text>'
        '<text fill="#F59E0B" font-family="Raleway,sans-serif" font-size="7" font-weight="700" letter-spacing="2.5" text-anchor="middle" x="59" y="64">TRAVEL</text>'
        "</svg>"
    )


def lang_switch(a):
    base = "https://sakhva-travel.com"
    order = [("ru", "RU"), ("en", "EN"), ("ge", "GE")]
    parts = ['<div class="lang-sw">']
    sep = ""
    for code, label in order:
        if code == a["lang"]:
            parts.append(f'{sep}<span class="lang-btn on">{label}</span>')
        else:
            parts.append(f'{sep}<a class="lang-btn" href="{base}{a["alt"][code]}">{label}</a>')
        sep = '<span class="lang-sep">|</span>'
    parts.append("</div>")
    return "".join(parts)


def nav(a):
    lang = a["lang"]
    links = "".join(
        f'<a href="{h}">{t}</a>'
        for t, h in zip(NAV_LABELS[lang][:-1], NAV_HREF[lang][:-1])
    )
    btn = f'<a class="nav-btn" href="{NAV_HREF[lang][-1]}">{NAV_LABELS[lang][-1]}</a>'
    return (
        '<nav id="nav">'
        f'<a class="nav-logo" href="{"/" if lang=="ru" else "/"+lang+"/"}" aria-label="Sakhva Travel">{logo_svg()}</a>'
        f'<div class="nav-links">{links}{btn}{lang_switch(a)}</div>'
        '<button aria-label="menu" class="burger" id="burger"><span></span><span></span><span></span></button>'
        "</nav>"
    )


def footer(a):
    lang = a["lang"]
    return (
        '<footer id="footer"><div class="foot-grid">'
        f'<div><div class="foot-brand">Sakhva Travel</div><p class="foot-desc">{FOOT_DESC[lang]}</p></div>'
        f'<div><h3>{NAV_LABELS[lang][0]}</h3><div class="foot-links">'
        f'<a href="{NAV_HREF[lang][0]}">{NAV_LABELS[lang][0]}</a>'
        f'<a href="{NAV_HREF[lang][1]}">{NAV_LABELS[lang][1]}</a></div></div>'
        f'<div><h3>{BLOG_NAME[lang]}</h3><div class="foot-links">'
        f'<a href="{NAV_HREF[lang][2]}">{BLOG_NAME[lang]}</a>'
        f'<a href="{NAV_HREF[lang][3]}">{NAV_LABELS[lang][3]}</a></div></div>'
        '</div><div class="foot-bottom"><span class="foot-copy">© 2026 Sakhva Travel · Tbilisi, Georgia</span>'
        '<div class="foot-legal"><a href="mailto:help@sakhva-travel.com">help@sakhva-travel.com</a></div></div></footer>'
    )


def json_ld(a, wordcount):
    base = "https://sakhva-travel.com"
    url = base + a["url"]
    faq_ent = [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": ans}}
        for q, ans in a["faq"]
    ]
    author_name = {"ru": "Тимур", "en": "Timur", "ge": "თიმური"}[a["lang"]]
    author = {
        "@type": "Person", "@id": base + "/#guide-timur", "name": author_name,
        "jobTitle": "Guide", "url": base + "/about/",
        "hasCredential": {
            "@type": "EducationalOccupationalCredential",
            "credentialCategory": "Tour guide licence", "identifier": "8247109128",
            "recognizedBy": {"@type": "GovernmentOrganization",
                             "name": "Georgian National Tourism Administration"},
        },
    }
    publisher = {"@type": "Organization", "name": "Sakhva Travel", "url": base + "/",
                 "logo": {"@type": "ImageObject", "url": base + "/images/logo-schema.webp",
                          "width": 300, "height": 60}}
    lang_code = {"ru": "ru", "en": "en", "ge": "ka"}[a["lang"]]
    if a.get("kind") == "service":
        main = {"@type": "Service", "@id": url + "#service", "name": a["h1"],
                "serviceType": a.get("service_type", "Interpreter and personal support"),
                "areaServed": {"@type": "Country", "name": "Georgia"},
                "provider": publisher, "description": a["meta"], "url": url,
                "inLanguage": lang_code}
    else:
        main = {"@type": "BlogPosting", "@id": url + "#article", "inLanguage": lang_code,
                "wordCount": wordcount, "headline": a["h1"], "description": a["meta"],
                "author": author, "publisher": publisher,
                "datePublished": "2026-09-08", "dateModified": "2026-09-08",
                "url": url, "mainEntityOfPage": {"@type": "WebPage", "@id": url}}
    crumbs = [{"@type": "ListItem", "position": 1, "name": HOME_NAME[a["lang"]], "item": base + "/"}]
    if a.get("kind") != "service":
        crumbs.append({"@type": "ListItem", "position": 2, "name": BLOG_NAME[a["lang"]],
                       "item": base + a["blog_root"]})
    crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": a["crumb"], "item": url})
    graph = [main,
             {"@type": "BreadcrumbList", "itemListElement": crumbs},
             {"@type": "FAQPage", "mainEntity": faq_ent}]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def head(a, wordcount):
    base = "https://sakhva-travel.com"
    url = base + a["url"]
    lang_attr = {"ru": "ru", "en": "en", "ge": "ka"}[a["lang"]]
    og_locale = {"ru": "ru_RU", "en": "en_US", "ge": "ka_GE"}[a["lang"]]
    img = base + a["image"]
    author_meta = {"ru": "Тимур — Sakhva Travel", "en": "Timur — Sakhva Travel",
                   "ge": "თიმური — Sakhva Travel"}[a["lang"]]
    ge_font = ""
    if a["lang"] == "ge":
        ge_font = ('<link as="font" crossorigin href="/fonts/noto-sans-georgian.woff2" rel="preload" type="font/woff2"/>'
                   '<link href="/css/ge.css" rel="stylesheet"/>')
    ga = (f"<script>(function(){{function g(){{if(window._ga)return;window._ga=1;"
          f"var s=document.createElement('script');s.async=1;s.src='https://www.googletagmanager.com/gtag/js?id={GA4}';"
          f"s.onload=function(){{window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}"
          f"gtag('js',new Date());gtag('config','{GA4}')}};document.head.appendChild(s)}}"
          f"['scroll','click','keydown','touchstart'].forEach(function(e){{document.addEventListener(e,g,{{once:1,passive:1}})}});setTimeout(g,8000)}})();</script>")
    hreflang = "".join(
        f'<link href="{base}{a["alt"][c]}" hreflang="{hl}" rel="alternate"/>'
        for c, hl in [("ru", "ru"), ("en", "en"), ("ge", "ka")]
    ) + f'<link href="{base}{a["alt"]["ru"]}" hreflang="x-default" rel="alternate"/>'
    return (
        f'<!DOCTYPE html>\n<html lang="{lang_attr}">\n<head>\n'
        '<meta charset="utf-8"/>\n'
        '<meta content="width=device-width, initial-scale=1.0, viewport-fit=cover" name="viewport"/>\n'
        '<link href="/images/favicon-32.png" rel="icon" sizes="32x32" type="image/png"/>\n'
        f'<title>{a["title"]}</title>\n'
        f'<meta content="{a["meta"]}" name="description"/>\n'
        f'<meta content="{author_meta}" name="author"/>\n'
        f'<link href="{url}" rel="canonical"/>\n'
        f'{hreflang}\n'
        '<meta content="index,follow,max-image-preview:large,max-snippet:-1" name="robots"/>\n'
        f'<meta content="{a.get("og_type","article")}" property="og:type"/>\n'
        f'<meta content="{a["title"]}" property="og:title"/>\n'
        f'<meta content="{a["meta"]}" property="og:description"/>\n'
        f'<meta content="{url}" property="og:url"/>\n'
        f'<meta content="{img}" property="og:image"/>\n'
        '<meta content="1200" property="og:image:width"/><meta content="630" property="og:image:height"/>\n'
        f'<meta content="{og_locale}" property="og:locale"/><meta content="Sakhva Travel" property="og:site_name"/>\n'
        '<meta content="summary_large_image" name="twitter:card"/>\n'
        f'<meta content="{a["title"]}" name="twitter:title"/>\n'
        f'<meta content="{a["meta"]}" name="twitter:description"/>\n'
        f'<meta content="{img}" name="twitter:image"/>\n'
        '<link href="/fonts/raleway.css?v=2" rel="stylesheet"/><link href="/fonts/lora.css?v=2" rel="stylesheet"/>\n'
        f'{ge_font}\n'
        f'<style>{STYLE}</style>\n'
        f'<script type="application/ld+json">{json_ld(a, wordcount)}</script>\n'
        f'{ga}\n'
        f'<link as="image" fetchpriority="high" href="{a["image"]}" rel="preload" type="image/webp"/>\n'
        '</head>'
    )


def toc(a):
    items = "".join(f'<li><a href="#{sid}">{t}</a></li>' for sid, t in a["toc"])
    label = {"ru": "Содержание", "en": "Contents", "ge": "შინაარსი"}[a["lang"]]
    return f'<nav class="article-toc"><h2>{label}</h2><ol>{items}</ol></nav>'


def faq_block(a):
    title = {"ru": "Частые вопросы", "en": "FAQ", "ge": "ხშირი კითხვები"}[a["lang"]]
    rows = "".join(
        f'<div class="fi"><button class="fq" onclick="toggleFaq(this)">{q}'
        f'<span class="fq-ic">+</span></button><div class="fa"><div class="fa-inner">{ans}</div></div></div>'
        for q, ans in a["faq"]
    )
    return f'<section id="faq"><div class="faq-inner"><h2>{title}</h2>{rows}</div></section>'


def related_block(a):
    title = {"ru": "Похожие туры от Sakhva Travel",
             "en": "Related tours from Sakhva Travel",
             "ge": "მსგავსი ტურები Sakhva Travel-ისგან"}[a["lang"]]
    more = {"ru": "Подробнее →", "en": "Learn more →", "ge": "დაწვრილებით →"}[a["lang"]]
    lbl = {"ru": "Тур", "en": "Tour", "ge": "ტური"}[a["lang"]]
    cards = "".join(
        f'<div class="rc-card"><div class="rc-card-label">{lbl}</div>'
        f'<h3>{t}</h3><p>{d}</p><a href="{u}">{more}</a></div>'
        for t, d, u in a["related"]
    )
    return f'<section class="related"><h2>{title}</h2><div class="related-grid">{cards}</div></section>'


def scripts():
    return (
        "<script>"
        "var b=document.getElementById('burger'),d=document.getElementById('drawer');"
        "if(b)b.addEventListener('click',function(){var o=d&&d.classList.toggle('on');b.classList.toggle('on',!!o)});"
        "function toggleFaq(btn){var i=btn.closest('.fi'),op=i.classList.contains('open');"
        "document.querySelectorAll('.fi.open').forEach(function(x){x.classList.remove('open');x.querySelector('.fa').style.maxHeight=null});"
        "if(!op){i.classList.add('open');var a=i.querySelector('.fa');a.style.maxHeight=a.scrollHeight+'px'}}"
        "</script>"
    )


def render(a):
    wordcount = wc(a["lead"], a["body"], " ".join(q + " " + ans for q, ans in a["faq"]))
    meta_line = " · ".join(a["meta_bits"])
    byline = {
        "ru": 'Тимур · Sakhva Travel · частный гид в Тбилиси с 2023',
        "en": 'Timur · Sakhva Travel · private guide in Tbilisi since 2023',
        "ge": 'თიმური · Sakhva Travel · კერძო გიდი თბილისში 2023 წლიდან',
    }[a["lang"]]
    doc = (
        head(a, wordcount) + "\n<body>\n" + nav(a) +
        '<main><div class="drawer" id="drawer"></div>'
        '<header class="article-hero"><div class="breadcrumb">'
        f'<a href="{"/" if a["lang"]=="ru" else "/"+a["lang"]+"/"}">{HOME_NAME[a["lang"]]}</a><span>/</span>'
        + (f'<a href="{a["blog_root"]}">{BLOG_NAME[a["lang"]]}</a><span>/</span>' if a.get("kind") != "service" else "")
        + f'<span>{a["crumb"]}</span></div>'
        f'<div class="article-label">{a["label"]}</div>'
        f'<h1 class="article-h1">{a["h1"]}</h1>'
        f'<div class="article-meta"><span>{meta_line}</span><span>{byline}</span></div></header>'
        '<div class="article-wrap">'
        + toc(a) +
        f'<div class="article-body"><p class="article-lead">{a["lead"]}</p>{a["body"]}</div>'
        '</div>'
        + related_block(a) + faq_block(a) + footer(a) + scripts() +
        "</body>\n</html>"
    )
    return doc, wordcount


# ── content: RU ───────────────────────────────────────────────────────────────
WA = 'WhatsApp <a href="https://wa.me/995511272623">+995 511 272 623</a>'


def cta_ru(variant):
    """Varied dual-service CTA — different anchor text each article."""
    return (
        '<div class="article-cta"><h3>Нужен переводчик рядом?</h3>'
        f'<p>{variant}</p>'
        '<a class="btn-wa" href="https://wa.me/995511272623">Написать в WhatsApp</a></div>'
    )


ARTICLES = []

# 1. PILLAR ---------------------------------------------------------------------
ARTICLES.append({
    "lang": "ru", "kind": "service", "og_type": "website",
    "url": "/perevodchik-i-soprovozhdenie-v-gruzii/",
    "blog_root": "/blog/",
    "alt": {"ru": "/perevodchik-i-soprovozhdenie-v-gruzii/",
            "en": "/en/interpreter-and-support-georgia/",
            "ge": "/ge/interpreter-and-support-georgia/"},
    "title": "Переводчик и сопровождение в Грузии — Тбилиси",
    "meta": "Русскоязычный переводчик и личное сопровождение в Грузии: врач, полиция, банк, нотариус, брак, ВНЖ, бизнес. Переводим и ведём по системе рядом с вами.",
    "h1": "Переводчик и личное сопровождение в Грузии",
    "crumb": "Переводчик и сопровождение",
    "label": "Услуга · Тбилиси и окрестности",
    "service_type": "Interpreter and personal accompaniment",
    "image": "/images/blog/perevodchik-soprovozhdenie.webp",
    "meta_bits": ["Услуга", "Тбилиси", "рус/eng ↔ груз"],
    "toc": [("komu", "Кому это нужно"), ("situacii", "С чем помогаем"),
            ("pochemu", "Живой переводчик или приложение"), ("otlichie", "Чем отличаемся от бюро переводов"),
            ("istorii", "Три обычные ситуации"), ("podgotovka", "Как подготовиться до визита"),
            ("granicy", "Что мы делаем и чего не делаем"),
            ("kak", "Как это работает"), ("formaty", "Форматы и языки"),
            ("cena", "Стоимость"), ("dalshe", "Что дальше")],
    "lead": "Когда в Грузии нужно решить вопрос, где всё держится на языке и знании местного порядка — приём у врача, полиция, банк, нотариус, брак — <strong>рядом важен человек, а не словарь</strong>. Мы не бюро переводов: мы ведём вас по грузинской системе на понятном языке и, если нужно, приезжаем на место.",
    "body": """
<h2 id="komu">Кому это нужно</h2>
<p>Вы недавно приехали или переехали, грузинского не знаете, а вопрос нужно закрыть сегодня. Русский слышен не везде, а государственные учреждения работают на грузинском. В такой момент нужен не переводчик «по строкам», а человек, который знает и язык, и местный порядок: точно переведёт вживую, объяснит, что происходит на каждом шаге, и при необходимости заедет за вами и отвезёт.</p>
<p>За годы работы в Тбилиси мы видим, где люди застревают чаще всего: не тот талон в электронной очереди, неполный пакет документов, перевод без нотариального заверения, апостиль, который нужно было проставить ещё дома. Половина проблем снимается до визита — правильной подготовкой, а не героизмом на месте.</p>
<h2 id="situacii">С чем помогаем</h2>
<p>Сопровождение закрывает те ситуации, где цена ошибки — деньги и потерянные дни:</p>
<ul>
<li><strong>Медицина.</strong> Запись к врачу, анализы, стоматология, беременность и роды, аптека. Записываем, звоним, объясняем врачу вашу ситуацию и переводим диагноз без потери смысла — это не тот случай, где можно «примерно понять».</li>
<li><strong>Полиция и право.</strong> Общение с полицией, ДТП, нотариус, доверенности, суд. Здесь важны формулировка и процедура — переводим и говорим, что будет дальше. Тонкости заверения бумаг разбираем в отдельном разборе про <a href="/blog/perevod-i-zaverenie-dokumentov-v-gruzii/">перевод и заверение документов</a>.</li>
<li><strong>Брак.</strong> Грузия — одно из самых простых мест для регистрации: быстро, минимум требований, часто в тот же день. Церемония идёт на грузинском, поэтому переводчик обязателен.</li>
<li><strong>Банк, ВНЖ, официальные собеседования.</strong> Открытие счёта и банковское интервью — см. пошаговый гид <a href="/blog/otkryt-schet-v-banke-gruzii/">как открыть счёт в банке Грузии</a>; вопросы легализации — <a href="/blog/vid-na-zhitelstvo-v-gruzii/">вид на жительство в Грузии</a>.</li>
<li><strong>Бизнес.</strong> Встречи с партнёрами, регистрация компании, сопровождение сделки — см. <a href="/blog/registratsiya-kompanii-v-gruzii/">регистрацию компании и ИП</a>.</li>
</ul>
<h2 id="pochemu">Живой переводчик или приложение</h2>
<p>Приложение-переводчик выручает в кафе и на рынке, но в кабинете врача или у окна госоргана оно проигрывает по трём причинам. Первая — контекст: врач говорит не отдельными словами, а с недомолвками, уточняющими вопросами и оговорками, и именно их машина теряет. Вторая — ответственность: когда речь идёт о диагнозе, доверенности или формулировке в протоколе, «примерно так» недопустимо, а живой человек переспросит и уточнит. Третья — процедура: половина пользы не в переводе, а в том, что рядом тот, кто знает, какой талон взять, какое окно ваше и что спросят дальше.</p>
<p>Мы совмещаем перевод и навигацию по системе. Вы не остаётесь один на один с грузинской анкетой и электронной очередью — мы стоим рядом, объясняем каждый шаг и следим, чтобы пакет документов был полным до того, как подойдёт ваш номер.</p>
<h2 id="otlichie">Чем отличаемся от бюро переводов</h2>
<p>Бюро продаёт слова и часы: вы приходите к ним, получаете перевод листа и остаётесь один на один с очередью, талоном и грузинской анкетой. Мы продаём результат по вашей задаче — от первого сообщения до печати на документе.</p>
<div class="price-table-wrap"><table class="price-table">
<thead><tr><th>Критерий</th><th>Бюро переводов</th><th>Сопровождение Sakhva</th></tr></thead>
<tbody>
<tr><td>Что продаёт</td><td>слова, часы</td><td>решённую задачу целиком</td></tr>
<tr><td>Знание системы</td><td>переводит текст</td><td>знает клиники, банки, учреждения</td></tr>
<tr><td>Формат</td><td>вы идёте к ним</td><td>едем с вами, при необходимости с машиной</td></tr>
<tr><td>Тон</td><td>формальный</td><td>по-человечески, на вашем языке</td></tr>
<tr><td>Доверие</td><td>разовая услуга</td><td>в Грузии с 2023, свой гид и водитель</td></tr>
</tbody></table></div>
<div class="info-box">Мы не заменяем нотариуса или врача — мы делаем так, чтобы вы их поняли и они поняли вас, а бумаги были собраны заранее и в правильном порядке.</div>
<h2 id="istorii">Три обычные ситуации</h2>
<p>Чтобы стало понятнее, вот типичные обращения — без имён и деталей, но по сути такие приходят каждую неделю.</p>
<ul>
<li><strong>Приём у врача.</strong> Человек с хроническим заболеванием переезжает и не может объяснить кардиологу историю болезни и препараты. Мы находим врача, записываем, переводим анамнез и назначения и следим, чтобы дозировки и названия лекарств были поняты обеими сторонами — здесь ошибка перевода опаснее всего.</li>
<li><strong>Банк отказал.</strong> После 2023 года банки строже, и заявку нередко разворачивают без объяснения. Мы идём вместе на банковское интервью, помогаем показать связь со страной (аренда, ВНЖ, контракт) и переводим вопросы комплаенса — часто именно живой разговор снимает отказ.</li>
<li><strong>Регистрация брака.</strong> Пара хочет расписаться в Тбилиси и не знает, что паспорт нужен с нотариальным переводом, а церемония идёт на грузинском. Мы собираем пакет заранее, переводим на самой церемонии и ведём от талона до свидетельства.</li>
</ul>
<h2 id="podgotovka">Как подготовиться до визита</h2>
<p>Большая часть проблем снимается не героизмом на месте, а подготовкой. Перед любым официальным визитом стоит закрыть четыре пункта:</p>
<ul>
<li>уточнить точную услугу и список документов — не «примерно», а по названию окна;</li>
<li>заранее сделать нотариальный перевод и, если нужен, апостиль (его на иностранный документ ставят только дома, до приезда);</li>
<li>свести написание имени к одной транслитерации во всех бумагах;</li>
<li>узнать сумму пошлины и способ оплаты, чтобы не искать банкомат в процессе.</li>
</ul>
<p>Мы проходим этот чек-лист с вами до визита — тогда сам визит превращается в формальность на 20 минут вместо потерянного дня и повторной поездки.</p>
<h2 id="granicy">Что мы делаем и чего не делаем</h2>
<p>Честность про границы услуги экономит всем время. Мы переводим, готовим и сопровождаем: собираем пакет, объясняем процедуру, стоим рядом на приёме и у окна, ведём от талона до результата. Мы не выдаём юридических заключений вместо адвоката, не ставим диагнозов вместо врача и не обещаем, что госорган примет положительное решение — исход зависит от ваших документов и оснований, а не от нашего желания.</p>
<p>Зато мы честно скажем заранее, если чего-то не хватает или шансы низкие, — чтобы вы не платили пошлину впустую. Если задача выходит за рамки перевода и сопровождения (например, нужен именно лицензированный юрист или бухгалтер), мы прямо об этом скажем и, где возможно, подскажем, к кому обратиться.</p>
<h2 id="kak">Как это работает</h2>
<ol>
<li><strong>Запрос.</strong> Опишите ситуацию: что, где и когда нужно. Достаточно пары фраз своими словами.</li>
<li><strong>Уточнение.</strong> Задаём короткие вопросы, составляем список документов, согласуем время и место.</li>
<li><strong>Сопровождение.</strong> Встречаем на месте или заезжаем за вами, переводим и ведём через весь процесс — очередь, окно, оплату пошлины.</li>
<li><strong>Результат.</strong> Вопрос закрывается с первого раза; при необходимости помогаем с переводом и нотариальным заверением.</li>
</ol>
<div class="review-quote"><p class="review-quote-text">Половина «сложных» визитов на самом деле простые — если прийти с полным пакетом и в правильное окно. Мы для того и рядом, чтобы вы не ходили дважды.</p><div class="review-quote-author">— Тимур, Sakhva Travel</div></div>
<h2 id="formaty">Форматы и языки</h2>
<p>Личное сопровождение на приёме; сопровождение с трансфером; срочный визит в тот же день; телефонный перевод для короткой удалённой помощи. Языки: русский ↔ грузинский и английский ↔ грузинский. Если не уверены, какой формат вам подходит, — опишите ситуацию, подскажем сами.</p>
""" + cta_ru("Опишите ситуацию — врача, банк, нотариуса или брак — и мы будем рядом, переведём и проведём по всем окнам.") + """
<h2 id="cena">Стоимость</h2>
<p>Зависит от ситуации, длительности и того, нужен ли трансфер. Мы не берём плату «за слово» — берём за решённую задачу. Напишите, что нужно, и назовём цену заранее, без сюрпризов на месте.</p>
<h2 id="dalshe">Что дальше — познакомиться с Грузией</h2>
<p>Когда бумаги позади, страну хочется увидеть, а не только пройти по учреждениям. Мы возим по Грузии сами: посмотрите <a href="/blog/russkoyazychny-gid-tbilisi/">частного гида в Тбилиси</a> или готовые <a href="/ekskursiya/">однодневные экскурсии</a> — Казбеги, Кахетия, Мцхета, в вашем темпе. Так один и тот же человек, который помог с документами, покажет вам и настоящую Грузию.</p>
""",
    "related": [
        ("Частный гид в Тбилиси", "Индивидуальные маршруты по городу и стране.", "/blog/russkoyazychny-gid-tbilisi/"),
        ("Однодневные экскурсии", "Казбеги, Кахетия, Мцхета — за один день.", "/ekskursiya/"),
        ("Туры по Грузии", "Многодневные маршруты с гидом и водителем.", "/tury-v-gruziyu/"),
    ],
    "faq": [
        ("Нужен ли нотариально заверенный перевод?", "Для части процедур — да (например, паспорт для брака). Скажем точно, что нужно, и организуем заверение."),
        ("Можно ли заказать на тот же день?", "Да, когда есть возможность. Чем раньше напишете, тем лучше слот и подготовка."),
        ("Вы работаете только в Тбилиси?", "Тбилиси и окрестности — основная зона; другие регионы по согласованию."),
        ("Что если я не знаю, что именно мне нужно?", "Опишите ситуацию своими словами — разберёмся вместе и составим список документов."),
    ],
})

# 2. ВНЖ ------------------------------------------------------------------------
ARTICLES.append({
    "lang": "ru", "kind": "post",
    "url": "/blog/vid-na-zhitelstvo-v-gruzii/", "blog_root": "/blog/",
    "alt": {"ru": "/blog/vid-na-zhitelstvo-v-gruzii/",
            "en": "/en/blog/residence-permit-georgia/",
            "ge": "/ge/blog/residence-permit-georgia/"},
    "title": "Вид на жительство в Грузии 2026: типы и как получить",
    "meta": "Все типы ВНЖ в Грузии 2026: рабочий, инвестиционный, на недвижимость, учебный, семейный. Документы, порядок подачи, сроки, стоимость и причины отказа.",
    "h1": "Вид на жительство в Грузии 2026: типы и как получить",
    "crumb": "ВНЖ в Грузии",
    "label": "Гайд · 8 мин чтения",
    "image": "/images/blog/vid-na-zhitelstvo-v-gruzii.webp",
    "meta_bits": ["Гайд", "Жизнь в Грузии", "ВНЖ"],
    "toc": [("nuzhen", "Нужен ли он вам"), ("tipy", "Типы ВНЖ"), ("daet", "Что даёт и не даёт ВНЖ"),
            ("dok", "Документы"), ("poryadok", "Порядок подачи"), ("sroki", "Сроки и стоимость"),
            ("pmzh", "Продление и ПМЖ"), ("otkaz", "Причины отказа"),
            ("vazhno", "Что важно помнить"), ("semya", "Переезд с семьёй"),
            ("scenarii", "Типичные сценарии")],
    "lead": "<strong>Вид на жительство в Грузии</strong> даёт право жить в стране после того, как закончится безвизовый период. Оформляется через Агентство развития госсервисов и Дом юстиции. Путей несколько — работа, учёба, инвестиция, владение недвижимостью выше порога и воссоединение семьи.",
    "body": """
<h2 id="nuzhen">Нужен ли он вам вообще</h2>
<p>Граждане многих стран могут находиться в Грузии без визы до 1 года. Пока это устраивает, ВНЖ строго не обязателен. Он нужен, чтобы работать по местному договору, учиться, вести бизнес с долгосрочной определённостью, купить недвижимость и осесть, привезти семью или двигаться к постоянному проживанию и гражданству. На практике многие оформляют его просто ради предсказуемости — чтобы не обнулять год выездами на границу.</p>
<div class="info-box">ВНЖ и налоговое резидентство — разные вещи. Резидентство возникает после 183 дней в стране за 12 месяцев и касается налогов, а не права проживания.</div>
<h2 id="tipy">Типы ВНЖ</h2>
<ul>
<li><strong>Рабочий</strong> — по договору с грузинской компанией или как предприниматель с оборотом; подтверждаете деятельность и доход.</li>
<li><strong>Учебный</strong> — зачисление в аккредитованный вуз или колледж.</li>
<li><strong>Инвестиционный</strong> — вложение выше установленного порога; выдаётся на более длинный срок.</li>
<li><strong>На недвижимость</strong> — владение объектом выше порога (ориентир около 100 000 USD; точную сумму и правила оценки уточняйте на sda.gov.ge — они меняются).</li>
<li><strong>Семейный</strong> — для супругов и детей держателя ВНЖ.</li>
<li><strong>Краткосрочный</strong> — на основании владения недвижимостью, на год, с продлением.</li>
</ul>
<h2 id="daet">Что даёт и не даёт ВНЖ</h2>
<p>Держатель ВНЖ живёт в Грузии без привязки к безвизовому году, официально арендует жильё на длинный срок, оформляет местные услуги и открывает банковский счёт заметно проще — карта резидента снимает вопрос «связи со страной», из-за которого банки после 2023 года часто разворачивают нерезидентов. Рабочий ВНЖ даёт право на трудоустройство по местному договору.</p>
<p>Чего ВНЖ не даёт автоматически: он не делает вас гражданином и не заменяет паспорт для выезда, не освобождает от налогов вашей родной страны и сам по себе не создаёт налогового резидентства Грузии. Учебный и семейный ВНЖ ограничивают трудоустройство — работать по ним можно не всегда. Поэтому категорию стоит выбирать под реальную цель, а не «какую проще получить».</p>
<h2 id="dok">Документы: базовый набор</h2>
<p>Действующий загранпаспорт и его нотариально заверенный перевод на грузинский; заявление и фото; подтверждение основания (договор, справка о зачислении, выписка на недвижимость, инвестиционные документы); подтверждение платёжеспособности; квитанция госпошлины. Точный список зависит от категории. Перевод и заверение — отдельный шаг; как он устроен, разбираем в гайде про <a href="/blog/perevod-i-zaverenie-dokumentov-v-gruzii/">перевод и заверение документов</a>.</p>
<h2 id="poryadok">Порядок подачи — по шагам</h2>
<ol>
<li>Выберите подходящую категорию и соберите основания.</li>
<li>Переведите и заверьте паспорт и справки.</li>
<li>Подайте заявление через <a href="/blog/dom-yustitsii-tbilisi/">Дом юстиции</a> или Агентство.</li>
<li>Оплатите пошлину — стандартная или ускоренная меняет скорость.</li>
<li>Дождитесь решения.</li>
<li>Заберите карту резидента.</li>
</ol>
<p>Если параллельно открываете счёт, полезен разбор <a href="/blog/otkryt-schet-v-banke-gruzii/">как открыть счёт в банке Грузии</a> — банки после 2023 года строже и часто просят подтверждение связи со страной, а ВНЖ этот вопрос закрывает.</p>
<h2 id="sroki">Сроки и стоимость</h2>
<p>Рассмотрение обычно занимает несколько недель; оплата ускоренного тарифа сокращает срок. Пошлина зависит от категории и срочности — актуальные тарифы 2026 года смотрите на sda.gov.ge; они меняются, поэтому «вечных» цифр мы не приводим.</p>
<h2 id="pmzh">Продление и постоянное проживание</h2>
<p>Первый ВНЖ обычно временный и выдаётся на срок от года до нескольких лет в зависимости от основания. Продлевать его нужно заранее — не в последний день, потому что рассмотрение занимает недели, и просрочка обнуляет статус. При продлении проверяют, что основание всё ещё в силе: рабочий контракт действует, недвижимость в собственности, учёба продолжается.</p>
<p>После нескольких лет непрерывного законного проживания открывается путь к постоянному виду на жительство, а затем — при выполнении условий по сроку и интеграции — к натурализации. Это марафон на годы, но начинается он с аккуратно оформленного первого ВНЖ и без разрывов в статусе. Поэтому важно с самого начала не допускать просрочек и хранить все документы об основаниях.</p>
<h2 id="otkaz">Частые причины отказа</h2>
<p>По опыту, заявления чаще всего возвращают из-за неправильной категории, незаверенного перевода, стоимости недвижимости ниже текущего порога или слабого подтверждения дохода. Отказ редко сопровождается подробным объяснением — обычно это вопрос комплаенса.</p>
<ul>
<li>Паспорт действует ещё минимум полгода;</li>
<li>перевод заверен грузинским нотариусом;</li>
<li>стоимость и оценка недвижимости отвечают текущему порогу;</li>
<li>доход подтверждён документами;</li>
<li>категория соответствует реальному основанию.</li>
</ul>
<div class="warn-box">Отказ — это не запрет навсегда. Исправьте причину и подайте снова или смените основание. Но каждая подача — это пошлина и недели ожидания, поэтому пакет лучше собрать правильно с первого раза.</div>
<h2 id="vazhno">Что важно помнить</h2>
<p>Путь через недвижимость популярен, но порог и оценку проверяют строго — покупка «под ВНЖ» без запаса по стоимости рискованна. Аренда жильём под ВНЖ не считается: нужен именно объект в собственности выше порога. Если ещё выбираете район и жильё, посмотрите разбор про <a href="/blog/arenda-kvartiry-tbilisi/">аренду квартиры в Тбилиси</a> — он поможет сориентироваться в ценах и договорах.</p>
<h2 id="semya">Переезд с семьёй</h2>
<p>Когда переезжают семьёй, ВНЖ обычно строится вокруг одного человека: он получает статус по работе, бизнесу, инвестиции или недвижимости, а супруг и дети идут по семейному основанию. Для детей понадобятся переведённые и заверённые свидетельства о рождении, а иногда согласие второго родителя на проживание — эти документы лучше подготовить с апостилем ещё дома.</p>
<p>Отдельный вопрос — школа: детей устраивают в местные, международные или русскоязычные школы, и части из них при зачислении нужны переведённые документы об образовании ребёнка. Планируйте это заранее, до начала учебного года, потому что перевод, заверение и место в школе — три параллельных процесса, а не один. Медицинская страховка на семью тоже оформляется отдельно и к ВНЖ автоматически не прилагается.</p>
<h2 id="scenarii">Типичные сценарии</h2>
<p>Какой путь выбрать, зависит от того, зачем вы в Грузии:</p>
<ul>
<li><strong>Фрилансер и удалёнщик.</strong> Чаще всего оформляют ИП со статусом малого бизнеса и на его основе рабочий ВНЖ — подтверждая деятельность и оборот. Как устроена регистрация, разбираем в гайде про <a href="/blog/registratsiya-kompanii-v-gruzii/">регистрацию компании и ИП</a>.</li>
<li><strong>Инвестор и покупатель жилья.</strong> Идут через недвижимость или инвестицию; здесь всё держится на оценке объекта и её соответствии текущему порогу.</li>
<li><strong>Семья.</strong> Один член семьи получает ВНЖ по работе или бизнесу, остальные — по семейному основанию.</li>
</ul>
<p>Во всех сценариях узкое место одно: перевод и заверение документов и корректная подача на грузинском. Именно там теряют пошлину и месяцы.</p>
""" + cta_ru("Заявление на ВНЖ идёт на грузинском, и ошибка стоит пошлины и месяцев. Мы сопроводим и переведём на подаче — от окна до карты резидента.") + """
<p>Оформление ВНЖ — это марафон из документов, но при спокойной подготовке он проходится один раз. А когда легализация позади, посмотрите страну не из окна учреждения: <a href="/blog/russkoyazychny-gid-tbilisi/">частный гид в Тбилиси</a> покажет Грузию так, как её видят местные.</p>
<div class="sources-block"><p class="sources-title">Официальные источники</p><ul>
<li><a href="https://sda.gov.ge/" rel="noopener noreferrer" target="_blank">Агентство развития госсервисов (sda.gov.ge)</a></li>
<li><a href="https://psh.gov.ge/" rel="noopener noreferrer" target="_blank">Дом юстиции (psh.gov.ge)</a></li>
</ul></div>
""",
    "related": [
        ("Частный гид в Тбилиси", "Индивидуальные маршруты по городу и стране.", "/blog/russkoyazychny-gid-tbilisi/"),
        ("Туры по Грузии", "Казбеги, Кахетия, Сванетия с гидом.", "/tury-v-gruziyu/"),
        ("Однодневные экскурсии", "Освоиться в стране за один день.", "/ekskursiya/"),
    ],
    "faq": [
        ("Нужен ли ВНЖ, если есть безвизовый год?", "Нет, пока год вас устраивает. Он нужен для работы, учёбы, бизнеса и долгого проживания."),
        ("Какой порог по недвижимости?", "Ориентир около 100 000 USD, но сумма и правила оценки меняются — проверяйте на sda.gov.ge."),
        ("ВНЖ даёт право работать?", "Рабочий и часть категорий — да; у учебного и семейного есть ограничения."),
        ("Сколько ждать решения?", "Обычно несколько недель; по ускоренному тарифу быстрее."),
        ("Что делать при отказе?", "Исправить причину и подать снова или сменить основание."),
        ("Можно ли работать удалённо на иностранную компанию по ВНЖ?", "Само проживание этому не мешает, но налоговые обязательства зависят от резидентства (183 дня) и правил вашей страны — это отдельный вопрос от ВНЖ, его стоит уточнить у налогового консультанта."),
        ("Достаточно ли аренды жилья для ВНЖ?", "Нет. Основанием служит именно недвижимость в собственности выше порога; долгосрочная аренда права на ВНЖ не даёт."),
    ],
})

# 3. Документы / нотариус -------------------------------------------------------
ARTICLES.append({
    "lang": "ru", "kind": "post",
    "url": "/blog/perevod-i-zaverenie-dokumentov-v-gruzii/", "blog_root": "/blog/",
    "alt": {"ru": "/blog/perevod-i-zaverenie-dokumentov-v-gruzii/",
            "en": "/en/blog/document-translation-notary-georgia/",
            "ge": "/ge/blog/document-translation-notary-georgia/"},
    "title": "Перевод и заверение документов в Грузии 2026",
    "meta": "Когда нужен нотариальный перевод в Грузии, апостиль или легализация, какие документы переводить для брака, ВНЖ и банка, где и как быстро это сделать.",
    "h1": "Перевод и нотариальное заверение документов в Грузии",
    "crumb": "Перевод документов",
    "label": "Гайд · 7 мин чтения",
    "image": "/images/blog/perevod-dokumentov-gruzia.webp",
    "meta_bits": ["Гайд", "Жизнь в Грузии", "Документы"],
    "toc": [("kogda", "Когда нужен заверенный перевод"), ("apostil", "Апостиль или легализация"),
            ("kakie", "Какие документы переводят"), ("pakety", "Пакеты по процедурам"),
            ("srok-spravok", "Срок действия справок"), ("diplom", "Диплом и доверенность"),
            ("prisyazhnyj", "Присяжный или нотариальный"), ("e-apostil", "Электронный апостиль"),
            ("gde", "Где и как быстро"), ("proverit", "Как проверить перевод"),
            ("poryadok", "Порядок действий"),
            ("cena", "Стоимость и срок"), ("oshibki", "Частые ошибки")],
    "lead": "<strong>Почти любая официальная процедура в Грузии</strong> — брак, ВНЖ, банк, учёба, сделка — требует, чтобы иностранный документ был переведён на грузинский и заверен нотариально. Часто нужен ещё апостиль или легализация из страны выдачи. Ниже — что делать и в каком порядке, чтобы приняли с первого раза.",
    "body": """
<h2 id="kogda">Когда нужен заверенный перевод</h2>
<p>Простого перевода госучреждению или банку недостаточно: принимают перевод, подпись переводчика на котором заверил грузинский нотариус. Это понадобится для брака (паспорт), для <a href="/blog/vid-na-zhitelstvo-v-gruzii/">вида на жительство</a>, для части банковских случаев, признания диплома, доверенностей и сделок с недвижимостью.</p>
<h2 id="apostil">Апостиль или легализация</h2>
<p>Здесь чаще всего и теряют время, поэтому разберём подробно.</p>
<ul>
<li>Если ваша страна и Грузия в <strong>Гаагской конвенции</strong>, документ (свидетельство о рождении, справка о несудимости, диплом) заверяется <strong>апостилем</strong> в стране выдачи — этого достаточно.</li>
<li>Если нет — нужна <strong>консульская легализация</strong>, процедура длиннее.</li>
</ul>
<div class="warn-box">Главное: апостиль на иностранный документ ставится дома, до отъезда — в Грузии его не получить. Это самая частая и болезненная ошибка. Апостиль на грузинский документ (например, местную справку для использования за рубежом) проставляют в Доме юстиции.</div>
<h2 id="kakie">Какие документы переводят чаще всего</h2>
<p>Паспорт (для брака и ВНЖ), свидетельства о рождении, браке и разводе, справка о несудимости, дипломы, справки о доходах, доверенности, водительское удостоверение, документы на недвижимость. Для брака ключевой — паспорт.</p>
<div class="info-box">Один принцип экономит недели: зафиксируйте одну транслитерацию имени и держите её во всех переводах. Если в паспорте, справке и переводе имя написано по-разному, система «видит» разных людей — и документ не принимают.</div>
<h2 id="pakety">Пакеты по процедурам</h2>
<p>Набор документов зависит от того, что вы оформляете. Три самых частых пакета:</p>
<ul>
<li><strong>Брак.</strong> Загранпаспорт с нотариальным переводом обоих будущих супругов; иногда — справка о семейном положении из своей страны с апостилем. Процедуру и роль переводчика на церемонии разбираем в услуге <a href="/perevodchik-i-soprovozhdenie-v-gruzii/">переводчика и сопровождения</a>.</li>
<li><strong>ВНЖ.</strong> Паспорт с переводом, подтверждение основания (контракт, выписка на недвижимость, справка о зачислении), подтверждение дохода. Полный порядок — в гайде про <a href="/blog/vid-na-zhitelstvo-v-gruzii/">вид на жительство</a>.</li>
<li><strong>Банк и бизнес.</strong> Паспорт, иногда подтверждение адреса и источника дохода; для компании — учредительные документы с переводом. См. <a href="/blog/otkryt-schet-v-banke-gruzii/">открытие счёта</a> и <a href="/blog/registratsiya-kompanii-v-gruzii/">регистрацию компании</a>.</li>
</ul>
<h2 id="srok-spravok">Срок действия справок</h2>
<p>У многих документов есть «срок годности», и это ломает планы чаще, чем кажется. Справка о несудимости и справка о семейном положении обычно принимаются в течение ограниченного периода с даты выдачи, поэтому заказывать их «с запасом на будущее» бессмысленно — к моменту подачи они могут устареть. Апостиль ставится на свежую справку, а не на прошлогоднюю. Логика простая: сначала уточняете требуемый срок под конкретную процедуру, потом заказываете справку и апостиль, и только затем едете в Грузию и переводите.</p>
<h2 id="diplom">Признание диплома и доверенности</h2>
<p>Для работы по специальности или поступления диплом переводят и заверяют, а для ряда профессий проходят отдельную процедуру признания квалификации — это не то же самое, что перевод, и занимает больше времени. Доверенность, оформленная за рубежом, тоже требует перевода и часто апостиля; а если доверенность делается уже в Грузии для действий за границей, её оформляет местный нотариус, и апостиль на неё ставят в Доме юстиции. Здесь особенно важна точность формулировок: доверенность с размытой или неверно переведённой формулировкой полномочий попросту не сработает в нужный момент.</p>
<h2 id="prisyazhnyj">Присяжный или нотариальный перевод</h2>
<p>Частый вопрос от тех, кто привык к европейской системе: нужен ли «присяжный переводчик»? В Грузии институт присяжного переводчика в привычном виде не используется — юридическую силу переводу придаёт не статус переводчика, а нотариальное заверение его подписи. То есть переводит квалифицированный переводчик, а грузинский нотариус удостоверяет, что подпись сделал именно он. Поэтому не ищите «сертифицированного присяжного» — ищите бюро, которое работает в связке с нотариусом и сдаёт готовый заверенный перевод. Это же правило снимает путаницу: перевод, заверенный нотариусом другой страны, здесь не подойдёт.</p>
<h2 id="e-apostil">Электронный апостиль и цифровые документы</h2>
<p>Всё больше стран выдают апостиль в электронном виде (e-Apostille) — с QR-кодом и проверкой по онлайн-реестру. Такой апостиль удобнее бумажного, но заранее уточните, принимает ли конкретное грузинское учреждение электронную форму именно вашей страны, — практика ещё выравнивается. То же касается цифровых выписок: грузинские документы всё чаще существуют в электронном виде с проверяемой подписью, но для подачи за рубежом иногда всё равно нужна бумажная копия с апостилем. Правило простое: перед тем как полагаться на цифровой документ, подтвердите, что принимающая сторона его примет.</p>
<h2 id="gde">Где и как быстро</h2>
<p>Бюро переводов стоят рядом с <a href="/blog/dom-yustitsii-tbilisi/">Домом юстиции</a> и часто сами организуют нотариальное заверение. Простой документ переводят и заверяют за день, иногда за час; пакет для сделки — дольше. Выбирая бюро, ориентируйтесь не только на цену: важнее, чтобы оно работало с нотариусом на месте и брало на себя весь путь «перевод плюс заверение», иначе вы будете сами бегать между переводчиком и нотариусом.</p>
<h2 id="proverit">Как проверить перевод перед подачей</h2>
<p>Перед тем как нести перевод в учреждение, потратьте пять минут на сверку — это дешевле, чем потерянный визит. Проверьте главное: имя и фамилия совпадают с загранпаспортом буква в букву (латиница и грузинская передача); все даты, номера документов и серии перенесены без опечаток; переведён нужный объём, а не «половина» документа; есть нотариальная отметка и подпись. Отдельно посмотрите на топонимы и названия организаций — их часто переводят по-разному в разных бумагах, и это создаёт расхождения. Если что-то вызывает сомнение, лучше исправить до подачи: переделать перевод дешевле, чем оплачивать пошлину повторно и ждать новый слот.</p>
<h2 id="poryadok">Порядок действий</h2>
<ol>
<li>Проверьте, нужен ли апостиль/легализация — если да, сделайте дома до вылета.</li>
<li>Принесите оригинал в бюро.</li>
<li>Переведите на грузинский.</li>
<li>Заверьте подпись переводчика нотариально.</li>
<li>Подайте в нужное учреждение.</li>
</ol>
<h2 id="cena">Стоимость и срок</h2>
<p>Зависят от языка, объёма и срочности; нотариальное заверение оплачивается отдельно от перевода. Актуальные тарифы нотариусов публикует нотариальная палата — «вечных» цифр не приводим, но простой документ обычно недорогой.</p>
<h2 id="oshibki">Частые ошибки</h2>
<ul>
<li>Приезд без апостиля (на иностранный документ его здесь не получить);</li>
<li>заверение у не-грузинского нотариуса;</li>
<li>перевод только части паспорта;</li>
<li>разное написание имени в разных документах.</li>
</ul>
<p>Каждая из них стоит отдельного визита, а иногда и повторной поездки домой за апостилем.</p>
""" + cta_ru("Соберём пакет, переведём, заверим и подадим — без беготни между бюро, нотариусом и окном. Напишите, какой документ нужен.") + """
<p>Документы — это разовая формальность, а страна остаётся. Когда бумаги готовы, посмотрите Грузию с <a href="/blog/russkoyazychny-gid-tbilisi/">частным гидом</a> или на <a href="/ekskursiya/">однодневной экскурсии</a>.</p>
<div class="sources-block"><p class="sources-title">Официальные источники</p><ul>
<li><a href="https://napr.gov.ge/" rel="noopener noreferrer" target="_blank">Национальное агентство публичного реестра (napr.gov.ge)</a></li>
<li><a href="https://psh.gov.ge/" rel="noopener noreferrer" target="_blank">Дом юстиции (psh.gov.ge)</a></li>
</ul></div>
""",
    "related": [
        ("Частный гид в Тбилиси", "Индивидуальные маршруты по городу.", "/blog/russkoyazychny-gid-tbilisi/"),
        ("Однодневные экскурсии", "Казбеги, Кахетия, Мцхета.", "/ekskursiya/"),
        ("Туры по Грузии", "Многодневные маршруты с гидом.", "/tury-v-gruziyu/"),
    ],
    "faq": [
        ("Нужен ли нотариальный перевод паспорта для брака?", "Да, это ключевой документ для регистрации брака."),
        ("Что такое апостиль и где его делают?", "Упрощённое заверение для стран Гаагской конвенции; на иностранный документ его ставят в стране выдачи, до приезда."),
        ("Можно ли заверить за день?", "Простой документ — часто да, иногда за час."),
        ("Весь паспорт или одну страницу?", "Обычно страницу с данными; уточните под вашу процедуру."),
        ("Апостиль делают в Грузии?", "На грузинские документы — да; на иностранные — только в стране выдачи."),
        ("Нужен ли перевод, если документ на английском?", "Как правило, да: госучреждения принимают документы на грузинском, поэтому даже англоязычную справку обычно переводят и заверяют. Уточняйте под конкретную процедуру."),
        ("Переводят ли напрямую с русского на грузинский?", "Да, бюро в Тбилиси работают с русским, английским и другими языками напрямую на грузинский — промежуточный перевод не нужен."),
    ],
})

# 4. Регистрация компании / ИП --------------------------------------------------
ARTICLES.append({
    "lang": "ru", "kind": "post",
    "url": "/blog/registratsiya-kompanii-v-gruzii/", "blog_root": "/blog/",
    "alt": {"ru": "/blog/registratsiya-kompanii-v-gruzii/",
            "en": "/en/blog/company-registration-georgia/",
            "ge": "/ge/blog/company-registration-georgia/"},
    "title": "Регистрация компании и ИП в Грузии 2026",
    "meta": "Как открыть ИП или ООО в Грузии в 2026: формы, статус малого бизнеса 1%, регистрация в Доме юстиции, счёт в банке, налоги и сроки для иностранца.",
    "h1": "Регистрация компании или ИП в Грузии: гайд 2026",
    "crumb": "Регистрация компании",
    "label": "Гайд · 8 мин чтения",
    "image": "/images/blog/registratsiya-kompanii-gruzia.webp",
    "meta_bits": ["Гайд", "Бизнес в Грузии", "ИП / ООО"],
    "toc": [("forma", "Какую форму выбрать"), ("status1", "Статус малого бизнеса 1%"),
            ("nds", "НДС и когда он появляется"), ("dok", "Документы"), ("shagi", "По шагам"),
            ("nalogi", "Налоги и отчётность"), ("kak-platit", "Как платить налог по шагам"),
            ("schet", "Счёт для бизнеса"), ("najm", "Наём сотрудников"),
            ("zakrytie", "Приостановка и закрытие"), ("specrezhimy", "IT-статус и свободные зоны"),
            ("stoimost-soderzhaniya", "Сколько стоит содержать ИП"), ("oshibki", "Частые ошибки")],
    "lead": "<strong>Открыть дело в Грузии</strong> быстро: ИП или ООО регистрируют в Доме юстиции обычно за один рабочий день, а иностранец может быть единственным владельцем. Для фрилансеров и малого оборота есть льготный <strong>статус малого бизнеса</strong> со ставкой 1% с оборота.",
    "body": """
<h2 id="forma">Какую форму выбрать</h2>
<ul>
<li><strong>Индивидуальный предприниматель (ИП)</strong> — самое простое; подходит фрилансерам и малому бизнесу; имеет право на статус малого бизнеса 1%.</li>
<li><strong>ООО (LLC)</strong> — для партнёров, найма сотрудников или ограниченной ответственности.</li>
<li><strong>Спецрежимы</strong> — свободные индустриальные зоны, IT-статус — под конкретные модели.</li>
</ul>
<p>Для большинства переехавших самозанятых стартовая точка — <strong>ИП плюс статус малого бизнеса</strong>. ООО имеет смысл, когда есть партнёры, наёмные сотрудники или нужна защита личных активов.</p>
<h2 id="status1">Статус малого бизнеса (1%)</h2>
<p>ИП с годовым оборотом ниже порога (ориентир — 500 000 лари; уточняйте на rs.ge) может держать статус малого бизнеса и платить <strong>1% с оборота</strong> вместо 20% подоходного; выше порога ставка выше. Именно это делает страну популярной у фрилансеров и удалёнщиков: при работе на зарубежных клиентов легальная нагрузка получается минимальной.</p>
<div class="info-box">Статус малого бизнеса и открытие ИП — это процедура в налоговой (rs.ge), а банк лишь открывает расчётный счёт. Это два разных шага, их часто путают.</div>
<p>У статуса есть нюансы, о которых узнают поздно. Он считается по обороту, а не по прибыли: важна вся выручка, а не то, что осталось после расходов. Ряд видов деятельности под льготу не подпадает — например, консалтинг в некоторых трактовках и лицензируемые сферы, поэтому свой конкретный вид работ стоит сверить заранее. И статус не назначается автоматически при регистрации ИП — его нужно отдельно запросить, иначе весь год вы будете платить 20% вместо 1%.</p>
<h2 id="nds">НДС и когда он появляется</h2>
<p>Отдельная тема, которую новички упускают: НДС. При обороте выше установленного порога появляется обязанность регистрироваться плательщиком НДС — и это отдельный порог, не равный порогу малого бизнеса. Пока вы небольшой фрилансер, это неактуально, но при росте оборота НДС может «включиться» незаметно, а штрафы за несвоевременную регистрацию ощутимы. Актуальные пороги и ставки смотрите на rs.ge; если оборот приближается к порогу, это сигнал подключить бухгалтера.</p>
<h2 id="dok">Документы</h2>
<p>Паспорт (и перевод, если попросят); юридический адрес в Грузии (аренда или согласие собственника); заявление; для ООО — устав и данные партнёров. Адрес проверяют — «пустой» не подойдёт.</p>
<h2 id="shagi">По шагам</h2>
<ol>
<li>Выберите форму и название.</li>
<li>Подготовьте адрес и документы.</li>
<li>Подайте в <a href="/blog/dom-yustitsii-tbilisi/">Доме юстиции</a> — обычно в тот же день (есть ускоренный тариф «в тот же час»).</li>
<li>Получите выписку и налоговый номер.</li>
<li>Зарегистрируйтесь на портале налоговой (rs.ge); при необходимости запросите статус малого бизнеса.</li>
<li>Откройте бизнес-счёт — см. <a href="/blog/otkryt-schet-v-banke-gruzii/">как открыть счёт в банке Грузии</a>.</li>
</ol>
<h2 id="nalogi">Налоги и отчётность</h2>
<div class="price-table-wrap"><table class="price-table">
<thead><tr><th>Форма</th><th>Налог</th></tr></thead>
<tbody>
<tr><td>ИП без статуса</td><td>20% подоходный</td></tr>
<tr><td>ИП, малый бизнес</td><td>1% с оборота (ниже порога)</td></tr>
<tr><td>ООО</td><td>15% на распределённую прибыль (платится с дивидендов)</td></tr>
</tbody></table></div>
<p>Ежемесячную декларацию по обороту подают на rs.ge. Учёт малого ИП часто ведут сами; при сотрудниках или НДС — с бухгалтером, его услуги в Грузии недорогие.</p>
<h2 id="kak-platit">Как платить налог по шагам</h2>
<p>Механика простая, но требует дисциплины каждый месяц:</p>
<ol>
<li>В течение месяца ведёте учёт всей выручки, зачисленной на счёт ИП.</li>
<li>До установленного числа следующего месяца подаёте декларацию по обороту в личном кабинете на rs.ge.</li>
<li>Оплачиваете налог — 1% с оборота при статусе малого бизнеса — с того же портала.</li>
<li>Храните подтверждения оплаты; при проверке источника средств банк может их запросить.</li>
</ol>
<p>Пропуск месяца — это штраф и пеня, поэтому декларацию проще поставить в календарь как повторяющуюся задачу. Первые пару месяцев многие проходят с бухгалтером, а дальше ведут сами.</p>
<h2 id="schet">Счёт для бизнеса</h2>
<p>После регистрации открывают отдельный счёт на ИП. Держите личные и предпринимательские траты на разных счетах, чтобы не путать обороты — это упрощает и декларацию, и разговор с банком при проверке источника средств.</p>
<h2 id="najm">Наём сотрудников</h2>
<p>Как только вы нанимаете людей, добавляется зарплатная отчётность: с зарплат удерживается подоходный налог, есть обязательные пенсионные отчисления, и всё это ежемесячно декларируется. Для ИП-одиночки этого нет, но при первом же сотруднике учёт усложняется — здесь уже почти всегда нужен бухгалтер. Договор с сотрудником составляют на грузинском (или двуязычно), и формулировки важны так же, как в любом другом официальном документе. Если планируете команду, закладывайте бухгалтерию в расходы сразу, а не «когда-нибудь потом».</p>
<h2 id="zakrytie">Приостановка и закрытие</h2>
<p>Планы меняются, и бизнес иногда нужно поставить на паузу или закрыть. Пока ИП существует, обязанность подавать декларации сохраняется — даже при нулевом обороте нужно сдавать «нулёвки», иначе копятся штрафы. Поэтому если деятельность прекратилась, ИП правильнее официально закрыть, а не бросить. Процедура закрытия проходит через налоговую и реестр; долги и незакрытые периоды лучше урегулировать до отъезда из страны. Это не сложно, но требует внимания — «просто перестать пользоваться счётом» не равно закрытию.</p>
<h2 id="specrezhimy">IT-статус и свободные зоны</h2>
<p>Для отдельных моделей есть специальные режимы. Компании в IT-сфере могут претендовать на статус «международной компании» или на режим виртуальной IT-зоны с пониженными ставками — это интересно тем, кто экспортирует IT-услуги, но требует соответствия критериям и отдельной процедуры. Свободные индустриальные зоны (FIZ) дают льготы производству и торговле внутри зоны. Для типичного фрилансера или консультанта эти режимы избыточны — им хватает ИП со статусом 1%, — но если у вас продуктовая IT-компания с командой, спецрежим стоит просчитать заранее, а не задним числом.</p>
<h2 id="stoimost-soderzhaniya">Сколько стоит содержать ИП</h2>
<p>Открыть ИП дёшево, но у него есть регулярные расходы, которые стоит заложить сразу. Это, во-первых, налог — 1% с оборота при статусе малого бизнеса. Во-вторых, банковское обслуживание: ведение счёта, комиссии за переводы, снятие и конвертацию. В-третьих, бухгалтерия, если вы не ведёте её сами; для одиночки это скромная сумма, но она есть. Плюс возможные расходы на юридический адрес, если своего нет. Всё это по-прежнему делает Грузию одной из самых выгодных юрисдикций для фрилансера, но «1% и всё» — упрощение: реальную нагрузку считайте как налог плюс обслуживание плюс учёт. Тогда не будет неприятных сюрпризов на второй-третий месяц.</p>
<h2 id="oshibki">Частые ошибки</h2>
<ul>
<li>Открыть ООО там, где хватило бы ИП;</li>
<li>забыть запросить статус малого бизнеса и год платить 20%;</li>
<li>недооценить требование реального адреса;</li>
<li>пропустить ежемесячную декларацию и получить штраф.</li>
</ul>
""" + cta_ru("Проведём через регистрацию, налоговый портал и открытие счёта, переведём на банковском интервью — с первого раза. Опишите ваш случай.") + """
<p>Регистрация бизнеса — вопрос одного-двух визитов при спокойной подготовке. А в выходные посмотрите страну: <a href="/blog/russkoyazychny-gid-tbilisi/">частный гид</a> или <a href="/tury-v-gruziyu/">туры по Грузии</a> с тем же человеком, что помог с документами.</p>
<div class="sources-block"><p class="sources-title">Официальные источники</p><ul>
<li><a href="https://rs.ge/" rel="noopener noreferrer" target="_blank">Служба доходов Грузии (rs.ge)</a></li>
<li><a href="https://napr.gov.ge/" rel="noopener noreferrer" target="_blank">Реестр предпринимателей (napr.gov.ge)</a></li>
</ul></div>
""",
    "related": [
        ("Частный гид в Тбилиси", "Индивидуальные маршруты по городу.", "/blog/russkoyazychny-gid-tbilisi/"),
        ("Туры по Грузии", "Многодневные маршруты с гидом.", "/tury-v-gruziyu/"),
        ("Однодневные экскурсии", "Казбеги, Кахетия, Мцхета.", "/ekskursiya/"),
    ],
    "faq": [
        ("Может ли иностранец открыть ИП или ООО?", "Да, в том числе как единственный владелец."),
        ("Что даёт статус 1%?", "1% с оборота вместо 20% подоходного — ниже порога оборота."),
        ("Сколько занимает регистрация?", "Обычно один рабочий день; по ускоренному тарифу быстрее."),
        ("Нужен ли реальный адрес?", "Да, его проверяют."),
        ("Какие налоги у ООО?", "15% на распределённую прибыль — платится с дивидендов."),
        ("Нужно ли лично быть в Грузии для регистрации?", "Обычно да — подача идёт очно в Доме юстиции. Регистрация по доверенности возможна, но доверенность нужно правильно оформить, перевести и заверить заранее."),
        ("Обязателен ли грузинский банковский счёт для ИП?", "Для работы и уплаты налога удобнее иметь местный счёт, но регистрация ИП и открытие счёта — разные шаги в разных учреждениях."),
    ],
})

# 5. Дом юстиции ----------------------------------------------------------------
ARTICLES.append({
    "lang": "ru", "kind": "post",
    "url": "/blog/dom-yustitsii-tbilisi/", "blog_root": "/blog/",
    "alt": {"ru": "/blog/dom-yustitsii-tbilisi/",
            "en": "/en/blog/public-service-hall-georgia/",
            "ge": "/ge/blog/public-service-hall-georgia/"},
    "title": "Дом юстиции в Тбилиси 2026: услуги и очередь",
    "meta": "Дом юстиции в Тбилиси: что оформить в одном окне, как записаться, часы работы, очереди, услуги для иностранцев и как пройти без грузинского языка.",
    "h1": "Дом юстиции в Тбилиси: что оформить в одном окне",
    "crumb": "Дом юстиции",
    "label": "Гайд · 7 мин чтения",
    "image": "/images/blog/dom-yustitsii-tbilisi.webp",
    "meta_bits": ["Гайд", "Жизнь в Грузии", "Госуслуги"],
    "toc": [("chto", "Что можно оформить"), ("odno-okno", "Как работает одно окно"),
            ("chasy", "Часы, запись, очереди"), ("inostrancy", "Что делают иностранцы"),
            ("brak", "Как заключить брак"), ("vizit", "Ваш визит по шагам"),
            ("vzyat", "Что взять с собой"), ("poshliny", "Пошлины и оплата"),
            ("yazyki", "Языки и доступность"), ("onlajn", "Онлайн без визита"),
            ("regiony", "Дом юстиции в регионах"), ("nedvizhimost", "Недвижимость и доверенности"),
            ("oshibki", "Частые ошибки")],
    "lead": "<strong>Дом юстиции</strong> — это принцип одного окна, где десятки госуслуг собраны под одной крышей: брак, документы компании, недвижимость, ВНЖ, справки, апостиль, нотариальные акты. Флагман в Тбилиси — заметное здание-«гриб» на реке. Ниже — что там делают иностранцы и как пройти без грузинского.",
    "body": """
<h2 id="chto">Что можно оформить</h2>
<p>Брак и акты гражданского состояния; <a href="/blog/registratsiya-kompanii-v-gruzii/">регистрацию компании</a> (ИП/ООО); права на недвижимость и сделки; заявления на ВНЖ и удостоверение личности; акты о рождении и смене имени; апостиль на грузинские документы; выписки и справки; часть нотариальных и банковских услуг прямо в зале. Большинство официальных вопросов новоприбывшего решается здесь.</p>
<h2 id="odno-okno">Как работает одно окно</h2>
<p>Вы берёте талон на услугу, ждёте номер на табло, идёте к оператору, сдаёте документы и тут же оплачиваете пошлину. Многие услуги — в тот же день. Операторы обслуживают на грузинском (часть — на английском), а анкеты и квитанции на грузинском — именно здесь и важен перевод, чтобы правильно заполнить заявление и не взять не тот талон.</p>
<h2 id="chasy">Часы, запись и очереди</h2>
<p>Флагман в Тбилиси работает и по выходным (актуальное расписание — на psh.gov.ge). На часть услуг можно записаться, это экономит время; на массовые услугах очередь заметна до обеда. По опыту: приходите рано и с полным пакетом, чтобы не ходить дважды — это главная причина повторного визита.</p>
<div class="info-box">Самый частый «потерянный день» — приезд без нотариального перевода или апостиля. Как их подготовить заранее, разбираем в гайде про <a href="/blog/perevod-i-zaverenie-dokumentov-v-gruzii/">перевод и заверение документов</a>.</div>
<h2 id="inostrancy">Что делают иностранцы чаще всего</h2>
<ul>
<li><strong>Заключают брак</strong> — Грузия быстрая, часто в тот же день;</li>
<li><strong>открывают ИП/ООО</strong> — см. <a href="/blog/registratsiya-kompanii-v-gruzii/">регистрацию компании</a>;</li>
<li><strong>подают на ВНЖ</strong> — см. <a href="/blog/vid-na-zhitelstvo-v-gruzii/">вид на жительство</a>;</li>
<li><strong>заверяют переводы и апостиль</strong> на грузинские документы.</li>
</ul>
<h2 id="brak">Как заключить брак</h2>
<p>Брак — одна из самых частых причин, по которой иностранцы идут в Дом юстиции, и Грузия здесь действительно удобна: требований минимум, а расписаться часто можно в тот же день или на следующий. От будущих супругов нужны действующие паспорта с нотариальным переводом; в отдельных случаях просят справку о том, что человек не состоит в браке, — её готовят в своей стране с апостилем заранее.</p>
<p>Ключевой нюанс: церемония и оформление идут на грузинском, поэтому переводчик не формальность, а обязательное условие — без понимания того, что вы подписываете, регистрацию просто не проведут. Есть и «церемониальный» формат в отдельных залах, если хочется не просто штамп, а событие. Как мы сопровождаем на регистрации, описано в услуге <a href="/perevodchik-i-soprovozhdenie-v-gruzii/">переводчика и сопровождения</a>.</p>
<h2 id="vizit">Ваш визит по шагам</h2>
<ol>
<li>Заранее уточните услугу и документы.</li>
<li>Запишитесь онлайн, если возможно.</li>
<li>Возьмите талон или придите к назначенному времени.</li>
<li>Сдайте документы и переводы, оплатите пошлину.</li>
<li>Заберите результат или получите назначенную дату.</li>
</ol>
<h2 id="vzyat">Что взять с собой</h2>
<p>Паспорт и нотариально заверенные переводы; апостиль, если процедура его требует; подтверждение основания (договор, справка); деньги на пошлину — картой или наличными. Неполный пакет — главная причина потерянного дня.</p>
<h2 id="poshliny">Пошлины и оплата</h2>
<p>Почти каждая услуга платная, и почти у каждой есть ускоренный тариф: чем быстрее нужен результат, тем дороже. Условно есть «стандарт» (несколько рабочих дней), «ускоренно» (день) и «в тот же час» для части услуг — разница в цене кратная. Оплатить можно на месте картой или наличными, иногда через терминал в зале. Точные суммы меняются и зависят от услуги, поэтому мы не приводим «вечных» цифр — сверяйтесь на psh.gov.ge или спрашивайте у стойки информации. Важно заранее знать не только размер пошлины, но и какой тариф вам реально нужен: часто «стандарт» полностью устраивает, и переплата за срочность не нужна.</p>
<h2 id="yazyki">Языки и доступность</h2>
<p>Основной язык обслуживания — грузинский; часть операторов говорит по-английски, но рассчитывать на русский или английский у каждого окна не стоит, а анкеты и квитанции в любом случае на грузинском. Именно поэтому переводчик рядом экономит не столько нервы, сколько визиты: с ним вы заполняете заявление правильно с первого раза и берёте нужный талон. Здания современные и доступные, с электронной очередью и зонами ожидания, но в пиковые часы поток большой — планируйте время с запасом.</p>
<h2 id="onlajn">Онлайн без визита</h2>
<p>Часть услуг не требует поездки в зал. На портале государственных сервисов оформляют и заказывают ряд справок и выписок в электронном виде, а готовый документ приходит в цифровом виде или его забирают позже. Это экономит очередь для простых запросов вроде выписки из реестра. Но сложные процедуры — брак, регистрация компании, подача на ВНЖ, сделки с недвижимостью — по-прежнему проходят очно, потому что нужны оригиналы, подписи и присутствие. Полезная стратегия: то, что можно, закрываете онлайн заранее, а в зал идёте только с тем, что требует личного присутствия.</p>
<h2 id="regiony">Дом юстиции в регионах</h2>
<p>Флагман в Тбилиси — самый известный, но сеть шире: отделения работают в Батуми, Кутаиси, Рустави и других городах, а в небольших населённых пунктах базовые услуги оказывают Community Centers (общественные центры). Если вы живёте не в столице, необязательно ехать в Тбилиси ради справки — сначала проверьте ближайшее отделение на psh.gov.ge. Набор услуг в регионах может быть уже, чем во флагмане, поэтому редкие процедуры стоит уточнить заранее по телефону или онлайн.</p>
<h2 id="nedvizhimost">Недвижимость и доверенности</h2>
<p>Отдельный крупный блок услуг Дома юстиции — недвижимость. Здесь регистрируют право собственности при покупке, оформляют выписки из реестра, залоги и договоры. Для иностранца это одна из самых чувствительных процедур: сделка и договор идут на грузинском, а ошибка в формулировке или неучтённое обременение стоят дорого. Перед покупкой заказывают свежую выписку из реестра, чтобы убедиться в чистоте объекта и отсутствии залогов и споров.</p>
<p>Здесь же оформляют доверенности — например, если вы хотите, чтобы за вас действовал представитель, пока вы за границей. Доверенность делают у нотариуса, а для использования за рубежом на неё ставят апостиль. Как это состыковать с переводом, разбираем в гайде про <a href="/blog/perevod-i-zaverenie-dokumentov-v-gruzii/">перевод и заверение документов</a>. Во всех этих случаях присутствие переводчика — не роскошь, а способ понимать, под чем вы ставите подпись.</p>
<h2 id="oshibki">Частые ошибки</h2>
<ul>
<li>Прийти без нотариального перевода или апостиля;</li>
<li>перепутать услугу и талон;</li>
<li>прийти в пик без записи;</li>
<li>не знать точную сумму пошлины.</li>
</ul>
""" + cta_ru("Подскажем услугу и пакет, запишем, переведём у окна и проведём от талона до результата. Напишите, что нужно оформить.") + """
<p>Дом юстиции проходится за один визит, если прийти подготовленным. А чтобы Грузия запомнилась не только очередью в госоргане, посмотрите её с <a href="/blog/russkoyazychny-gid-tbilisi/">частным гидом</a> — Старый Тбилиси, Мцхета, Казбеги.</p>
<div class="sources-block"><p class="sources-title">Официальные источники</p><ul>
<li><a href="https://psh.gov.ge/" rel="noopener noreferrer" target="_blank">Дом юстиции (psh.gov.ge)</a></li>
<li><a href="https://sda.gov.ge/" rel="noopener noreferrer" target="_blank">Агентство развития госсервисов (sda.gov.ge)</a></li>
</ul></div>
""",
    "related": [
        ("Частный гид в Тбилиси", "Старый город, Мцхета, Казбеги.", "/blog/russkoyazychny-gid-tbilisi/"),
        ("Однодневные экскурсии", "За один день по главному.", "/ekskursiya/"),
        ("Туры по Грузии", "Многодневные маршруты с гидом.", "/tury-v-gruziyu/"),
    ],
    "faq": [
        ("Что можно оформить в Доме юстиции?", "Брак, компанию, недвижимость, ВНЖ, справки, апостиль, нотариальные акты."),
        ("Нужна ли запись?", "На часть услуг можно записаться и сэкономить время; на другие — живая очередь."),
        ("Работает ли по выходным?", "Флагман в Тбилиси — да; проверяйте на psh.gov.ge."),
        ("На каком языке обслуживают?", "На грузинском, часть услуг — на английском; документы на грузинском."),
        ("Что взять с собой?", "Паспорт, нотариальные переводы, при необходимости апостиль, деньги на пошлину."),
        ("Есть ли отделения в других городах?", "Да, помимо флагмана в Тбилиси отделения работают в Батуми, Кутаиси, Рустави и др., а базовые услуги — в Community Centers. Набор услуг в регионах может быть уже."),
        ("Сколько стоит услуга?", "У каждой услуги своя пошлина и обычно есть ускоренный тариф. Точные суммы меняются — сверяйтесь на psh.gov.ge; часто хватает стандартного тарифа без переплаты за срочность."),
    ],
})


def cta_en(variant):
    return ('<div class="article-cta"><h3>Need an interpreter beside you?</h3>'
            f'<p>{variant}</p>'
            '<a class="btn-wa" href="https://wa.me/995511272623">Message on WhatsApp</a></div>')


def cta_ge(variant):
    return ('<div class="article-cta"><h3>გჭირდებათ თარჯიმანი გვერდით?</h3>'
            f'<p>{variant}</p>'
            '<a class="btn-wa" href="https://wa.me/995511272623">მოგვწერეთ WhatsApp-ში</a></div>')


# ── content: EN (expat intent) ────────────────────────────────────────────────
ARTICLES.append({
    "lang": "en", "kind": "service", "og_type": "website",
    "url": "/en/interpreter-and-support-georgia/", "blog_root": "/en/blog/",
    "alt": {"ru": "/perevodchik-i-soprovozhdenie-v-gruzii/",
            "en": "/en/interpreter-and-support-georgia/",
            "ge": "/ge/interpreter-and-support-georgia/"},
    "title": "Interpreter & Support in Georgia — Tbilisi Help",
    "meta": "English- and Russian-speaking interpreter and personal support in Georgia: doctor, police, bank, notary, marriage, residence permit. We translate and guide you through.",
    "h1": "Interpreter and Personal Support in Georgia",
    "crumb": "Interpreter & support",
    "label": "Service · Tbilisi and around",
    "service_type": "Interpreter and personal accompaniment",
    "image": "/images/blog/perevodchik-soprovozhdenie.webp",
    "meta_bits": ["Service", "Tbilisi", "EN/RU ↔ Georgian"],
    "toc": [("who", "Who this is for"), ("cover", "What we cover"),
            ("app", "A person, not an app"), ("diff", "Not a translation bureau"),
            ("cases", "Three ordinary cases"), ("prep", "How to prepare"),
            ("how", "How it works"), ("formats", "Formats and languages"),
            ("price", "Pricing"), ("next", "See Georgia too")],
    "lead": "When something has to be sorted in Georgia and it all hinges on language and knowing the local order — a doctor's visit, the police, a bank, a notary, getting married — <strong>you need a person by your side, not a dictionary</strong>. We are not a translation bureau: we walk you through the Georgian system in a language you understand and, when needed, come to you.",
    "body": """
<h2 id="who">Who this is for</h2>
<p>You have just arrived or recently moved, you don't speak Georgian, and something has to be done today. Russian isn't spoken everywhere, and government offices run in Georgian only. In that moment you don't need a word-by-word translator — you need someone who knows both the language and the local order of things: translates live and accurately, explains what happens at each step and, if needed, picks you up and drives you to the appointment.</p>
<p>After years working in Tbilisi we see where people get stuck most: the wrong ticket in the queue system, an incomplete file, a translation without notarisation, an apostille that should have been done back home. Half the trouble is solved before the visit — with preparation, not heroics on the spot.</p>
<h2 id="cover">What we cover</h2>
<p>Support covers the situations where a mistake costs money and lost days:</p>
<ul>
<li><strong>Healthcare.</strong> Booking, tests, dentistry, pregnancy and childbirth, the pharmacy. We book, call, explain your case to the doctor and translate the diagnosis without losing meaning. Georgia is also a hub for affordable treatment — see the guide to <a href="/en/blog/dental-tourism-georgia/">dental tourism in Georgia</a>.</li>
<li><strong>Police and legal.</strong> Dealing with the police, road accidents, notary, powers of attorney, court. Wording and procedure matter — we translate and tell you what comes next. Paperwork specifics are in <a href="/en/blog/document-translation-notary-georgia/">document translation and notarisation</a>.</li>
<li><strong>Marriage.</strong> Georgia is one of the easiest places to marry — often same day. The ceremony is in Georgian, so an interpreter is required; see <a href="/en/blog/how-to-get-married-in-georgia/">how to get married in Georgia</a>.</li>
<li><strong>Bank, residence permit, interviews.</strong> Opening an account — see <a href="/en/blog/open-bank-account-georgia/">how to open a bank account</a>; legal status — <a href="/en/blog/residence-permit-georgia/">the residence permit</a>.</li>
<li><strong>Business.</strong> Partner meetings, company setup, deal support — see <a href="/en/blog/company-registration-georgia/">company registration</a>.</li>
</ul>
<h2 id="app">A person, not an app</h2>
<p>A translation app is fine in a cafe, but in a doctor's office or at a government window it loses on three counts. Context: a doctor speaks with hedges, follow-up questions and caveats, and that is exactly what a machine drops. Responsibility: when it comes to a diagnosis, a power of attorney or the wording of a statement, "roughly this" is not acceptable, and a live person asks again to be sure. Procedure: half the value isn't the translation but having someone who knows which ticket to take, which window is yours and what will be asked next.</p>
<div class="info-box">We don't replace a notary or a doctor — we make sure you understand them and they understand you, and that your file is complete before your number comes up.</div>
<h2 id="diff">Not a translation bureau</h2>
<p>A bureau sells words and hours: you go to them, get a translated sheet and stay alone with the queue, the ticket and a Georgian form. We sell the result of your task, from the first message to the stamp on the document.</p>
<div class="price-table-wrap"><table class="price-table">
<thead><tr><th></th><th>Bureau</th><th>Sakhva support</th></tr></thead>
<tbody>
<tr><td>Sells</td><td>words, hours</td><td>your task, start to finish</td></tr>
<tr><td>Knows the system</td><td>translates text</td><td>knows clinics, banks, offices</td></tr>
<tr><td>Format</td><td>you come to them</td><td>we come with you, with a car if needed</td></tr>
<tr><td>Trust</td><td>one-off</td><td>in Georgia since 2023, own guide and driver</td></tr>
</tbody></table></div>
<h2 id="cases">Three ordinary cases</h2>
<ul>
<li><strong>A doctor's appointment.</strong> Someone with a chronic condition moves and can't explain their history and medication to a cardiologist. We find the doctor, book, translate the history and prescriptions, and make sure dosages and drug names are understood by both sides — the place a translation error is most dangerous.</li>
<li><strong>The bank said no.</strong> Since 2023 banks are stricter and often turn applications back without explanation. We come to the bank interview, help show your ties to the country (lease, permit, contract) and translate the compliance questions — often a live conversation clears the refusal.</li>
<li><strong>Getting married.</strong> A couple wants to marry in Tbilisi and doesn't know the passport needs a notarised translation and the ceremony is in Georgian. We assemble the file in advance, translate at the ceremony itself and guide from ticket to certificate.</li>
</ul>
<h2 id="prep">How to prepare before a visit</h2>
<p>Most problems are solved by preparation, not effort on the spot. Before any official visit, close four points: confirm the exact service and the document list — by the window's name, not "roughly"; do the notarised translation and, if needed, the apostille in advance (an apostille on a foreign document can only be done at home, before arrival); reduce your name to one spelling across every paper; find out the fee amount and how to pay it. We run this checklist with you beforehand — then the visit becomes a 20-minute formality instead of a lost day.</p>
""" + cta_en("Describe the situation — a doctor, a bank, a notary or a wedding — and we'll be beside you, translate and guide you through every window.") + """
<h2 id="how">How it works</h2>
<ol>
<li><strong>Request.</strong> Tell us the situation: what, where and when. A couple of sentences is enough.</li>
<li><strong>Clarify.</strong> We ask short questions, list the documents, agree a time and place.</li>
<li><strong>Support.</strong> We meet you on site or pick you up, translate and guide you through the whole process — queue, window, fee.</li>
<li><strong>Result.</strong> The task is done the first time; we help with translation and notarisation if needed.</li>
</ol>
<h2 id="formats">Formats and languages</h2>
<p>Personal support at the appointment; support with a transfer; a same-day urgent visit; phone interpreting for short remote help. Languages: English ↔ Georgian and Russian ↔ Georgian. Not sure which format fits? Describe the situation and we'll advise.</p>
<h2 id="price">Pricing</h2>
<p>It depends on the situation, the duration and whether you need a transfer. We don't charge "per word" — we charge for the task solved. Tell us what you need and we quote in advance, with no surprises on the spot.</p>
<h2 id="next">See Georgia too</h2>
<p>Once the paperwork is behind you, the country is worth seeing — not just its offices. We show Georgia ourselves: a <a href="/en/private-guide-tbilisi/">private guide in Tbilisi</a> takes you to Kazbegi, Kakheti and Mtskheta at your own pace. Settling in for the long run? The <a href="/en/blog/tbilisi-for-expats/">Tbilisi guide for expats</a> helps you find your feet.</p>
""",
    "related": [
        ("Private guide in Tbilisi", "Tailored routes across the city and country.", "/en/private-guide-tbilisi/"),
        ("Kazbegi day trip", "Mountains and Gergeti church in one day.", "/en/blog/kazbegi-day-trip-from-tbilisi/"),
        ("Kakheti wine tour", "Georgia's wine country with a guide.", "/en/blog/kakheti-wine-tour/"),
    ],
    "faq": [
        ("Do I need a notarised translation?", "For some procedures yes (e.g. your passport for marriage). We'll tell you exactly what and arrange it."),
        ("Can I book same day?", "Yes, when possible — the earlier you write, the better the slot and the preparation."),
        ("Do you work only in Tbilisi?", "Tbilisi and around is the core area; other regions by arrangement."),
        ("What if I don't know what I need?", "Describe the situation in your own words — we'll figure it out together and list the documents."),
    ],
})

ARTICLES.append({
    "lang": "en", "kind": "post",
    "url": "/en/blog/residence-permit-georgia/", "blog_root": "/en/blog/",
    "alt": {"ru": "/blog/vid-na-zhitelstvo-v-gruzii/",
            "en": "/en/blog/residence-permit-georgia/",
            "ge": "/ge/blog/residence-permit-georgia/"},
    "title": "Residence Permit in Georgia 2026: Types & How to Get It",
    "meta": "All residence permit types in Georgia 2026: work, investment, real-estate, study, family. Documents, how to apply, timelines, cost and common refusals explained.",
    "h1": "Residence Permit in Georgia 2026: Types and How to Get One",
    "crumb": "Residence permit",
    "label": "Guide · 8 min read",
    "image": "/images/blog/vid-na-zhitelstvo-v-gruzii.webp",
    "meta_bits": ["Guide", "Living in Georgia", "Residence"],
    "toc": [("need", "Do you even need one"), ("types", "Types of permit"),
            ("gives", "What it does and doesn't give"), ("docs", "Documents"),
            ("apply", "How to apply"), ("time", "Timelines and cost"),
            ("renew", "Renewal and permanent residency"), ("refusal", "Reasons for refusal"),
            ("family", "Moving with family"), ("scenarios", "Typical scenarios")],
    "lead": "A <strong>Georgian residence permit</strong> lets you live in the country after the visa-free window ends. It is issued via the Public Service Development Agency and the Public Service Hall. There are several routes — work, study, investment, owning real estate above a threshold, and family reunification.",
    "body": """
<h2 id="need">Do you even need one</h2>
<p>Citizens of many countries can stay in Georgia visa-free for up to one year. While that suits you, a permit isn't strictly required. You need one to work under a local contract, study, run a business with long-term certainty, buy property and settle, bring your family, or move toward permanent residency and citizenship. In practice many apply simply for predictability — to stop resetting the year with border runs.</p>
<div class="info-box">A residence permit and tax residency are different things. Tax residency arises after 183 days in the country over 12 months and concerns taxes, not the right to live here.</div>
<h2 id="types">Types of permit</h2>
<ul>
<li><strong>Work</strong> — via a contract with a Georgian company or as an entrepreneur with turnover; you prove activity and income.</li>
<li><strong>Study</strong> — enrolment at an accredited university or college.</li>
<li><strong>Investment</strong> — investing above a set threshold; issued for a longer term.</li>
<li><strong>Real estate</strong> — owning property above a threshold (a common reference is around US$100,000; confirm the current amount and valuation rules at sda.gov.ge — they change).</li>
<li><strong>Family</strong> — for spouses and children of a permit holder.</li>
<li><strong>Short-term</strong> — derived from property ownership, one year, renewable.</li>
</ul>
<h2 id="gives">What it does and doesn't give</h2>
<p>A permit holder lives in Georgia without depending on the visa-free year, rents long-term officially, arranges local services and opens a bank account noticeably more easily — the resident ID answers the "ties to the country" question that makes banks turn non-residents back after 2023. A work permit grants the right to be employed locally.</p>
<p>What it does not do automatically: it doesn't make you a citizen or replace a passport for travel, doesn't free you from your home country's taxes, and doesn't by itself create Georgian tax residency. Study and family permits limit employment. So choose the category by your real goal, not by "whichever is easiest".</p>
<h2 id="docs">Documents: the base set</h2>
<p>A valid passport and its notarised Georgian translation; the application and a photo; proof of grounds (contract, enrolment letter, property extract, investment papers); proof of solvency; the state-fee receipt. The exact list depends on the category. Translation and notarisation is a separate step — see <a href="/en/blog/document-translation-notary-georgia/">document translation and notary</a>.</p>
<h2 id="apply">How to apply — step by step</h2>
<ol>
<li>Pick the category that fits and gather your grounds.</li>
<li>Translate and notarise passport and certificates.</li>
<li>Apply via the <a href="/en/blog/public-service-hall-georgia/">Public Service Hall</a> or the Agency.</li>
<li>Pay the fee — standard or expedited changes the speed.</li>
<li>Wait for the decision.</li>
<li>Collect your resident ID card.</li>
</ol>
<p>If you're opening an account in parallel, the guide to <a href="/en/blog/open-bank-account-georgia/">opening a bank account</a> helps — banks are stricter since 2023 and often ask for proof of ties, which a permit resolves.</p>
<h2 id="time">Timelines and cost</h2>
<p>Processing usually takes a few weeks; paying the expedited fee shortens it. Fees depend on category and urgency — check current 2026 rates at sda.gov.ge; they change, so we don't quote "permanent" numbers.</p>
<h2 id="renew">Renewal and permanent residency</h2>
<p>The first permit is usually temporary, from one to several years depending on the grounds. Renew it early — not on the last day, because processing takes weeks and a lapse resets your status. At renewal they check the grounds still hold: the contract is valid, the property is still owned, the studies continue. After several years of continuous lawful residence the path to permanent residency opens, and then, subject to conditions, to naturalisation. It's a multi-year marathon, but it starts with a cleanly filed first permit and no gaps.</p>
<h2 id="refusal">Common reasons for refusal</h2>
<p>In our experience applications are most often turned back for the wrong category, an unnotarised translation, a property value below the current threshold, or weak proof of income. A refusal rarely comes with a detailed reason — it's usually compliance.</p>
<ul>
<li>passport valid at least six more months;</li>
<li>translation notarised by a Georgian notary;</li>
<li>property value and valuation meet the current threshold;</li>
<li>income backed by documents;</li>
<li>category matches your real grounds.</li>
</ul>
<div class="warn-box">A refusal is not a lifetime ban. Fix the cause and reapply, or switch grounds. But every application means a fee and weeks of waiting, so it's best to get the file right the first time.</div>
<h2 id="family">Moving with family</h2>
<p>When a family relocates, the permit is usually built around one person who gets status through work, business, investment or property, while the spouse and children follow on family grounds. Children need translated and notarised birth certificates, and sometimes the other parent's consent — prepare these with an apostille back home. School is a separate matter: children enrol in local, international or Russian-language schools, some of which need translated education records. Plan it before the school year — translation, notarisation and a school place are three parallel processes, not one. Health insurance for the family is arranged separately and doesn't come with the permit.</p>
<h2 id="scenarios">Typical scenarios</h2>
<ul>
<li><strong>Freelancer / remote worker.</strong> Most often they register a sole trader with small-business status and base a work permit on it — see <a href="/en/blog/company-registration-georgia/">company registration</a>.</li>
<li><strong>Investor / property buyer.</strong> Goes through real estate or investment; everything hinges on the valuation meeting the current threshold. If you're renting first, the <a href="/en/blog/apartment-rental-tbilisi/">apartment rental guide</a> helps.</li>
<li><strong>Family.</strong> One member gets a permit through work or business, the rest on family grounds.</li>
</ul>
<p>In every scenario the bottleneck is the same: translating and notarising documents and filing correctly in Georgian.</p>
""" + cta_en("The application is in Georgian, and a mistake costs a fee and months. We'll support and translate at your permit application — from the window to the resident card.") + """
<div class="sources-block"><p class="sources-title">Official sources</p><ul>
<li><a href="https://sda.gov.ge/" rel="noopener noreferrer" target="_blank">Public Service Development Agency (sda.gov.ge)</a></li>
<li><a href="https://psh.gov.ge/" rel="noopener noreferrer" target="_blank">Public Service Hall (psh.gov.ge)</a></li>
</ul></div>
""",
    "related": [
        ("Private guide in Tbilisi", "Tailored routes across the country.", "/en/private-guide-tbilisi/"),
        ("Kazbegi day trip", "The Georgian Military Highway in one day.", "/en/blog/kazbegi-day-trip-from-tbilisi/"),
        ("Guide for expats", "Settling into Tbilisi.", "/en/blog/tbilisi-for-expats/"),
    ],
    "faq": [
        ("Do I need a permit if I have a visa-free year?", "No, while the year suits you. You need one for work, study, business and long stays."),
        ("What's the property threshold?", "Around US$100,000, but the amount and valuation rules change — check sda.gov.ge."),
        ("Does a permit let me work?", "Work and some categories yes; study and family have limits."),
        ("How long is the decision?", "Usually a few weeks; expedited is faster."),
        ("What if I'm refused?", "Fix the cause and reapply, or switch grounds."),
        ("Is renting enough for a permit?", "No. The basis is owned property above the threshold; a long-term lease doesn't grant a permit."),
        ("Can I work remotely for a foreign company on a permit?", "Living here doesn't prevent it, but tax obligations depend on residency (183 days) and your home country's rules — a separate question from the permit, worth checking with a tax adviser."),
    ],
})

ARTICLES.append({
    "lang": "en", "kind": "post",
    "url": "/en/blog/document-translation-notary-georgia/", "blog_root": "/en/blog/",
    "alt": {"ru": "/blog/perevod-i-zaverenie-dokumentov-v-gruzii/",
            "en": "/en/blog/document-translation-notary-georgia/",
            "ge": "/ge/blog/document-translation-notary-georgia/"},
    "title": "Notarised Document Translation in Georgia 2026",
    "meta": "When you need a certified translation in Georgia, apostille vs legalisation, which documents to translate for marriage, residence and banking, where and how fast.",
    "h1": "Document Translation and Notarisation in Georgia",
    "crumb": "Document translation",
    "label": "Guide · 7 min read",
    "image": "/images/blog/perevod-dokumentov-gruzia.webp",
    "meta_bits": ["Guide", "Living in Georgia", "Documents"],
    "toc": [("when", "When you need it"), ("apostille", "Apostille or legalisation"),
            ("which", "Documents translated most"), ("packages", "Packages by procedure"),
            ("validity", "Validity of certificates"), ("diploma", "Diploma and power of attorney"),
            ("sworn", "Sworn or notarised"), ("check", "Check before you submit"),
            ("where", "Where and how fast"), ("order", "The order of steps"), ("mistakes", "Common mistakes")],
    "lead": "<strong>Almost any official procedure in Georgia</strong> — marriage, residence, banking, study, a deal — requires a foreign document translated into Georgian and notarised. Often you also need an apostille or legalisation from the country of issue. Here's what to do, and in what order, so it's accepted the first time.",
    "body": """
<h2 id="when">When you need a certified translation</h2>
<p>A plain translation isn't enough for a government office or bank: they accept a translation whose translator's signature a Georgian notary has certified. You'll need it for marriage (passport), a <a href="/en/blog/residence-permit-georgia/">residence permit</a>, some bank cases, diploma recognition, powers of attorney and property deals.</p>
<h2 id="apostille">Apostille or legalisation</h2>
<p>This is where people lose the most time, so let's be precise.</p>
<ul>
<li>If your country and Georgia are in the <strong>Hague Convention</strong>, a document (birth certificate, police clearance, diploma) is certified with an <strong>apostille</strong> in the country of issue — that's enough.</li>
<li>If not, you need <strong>consular legalisation</strong>, a longer chain.</li>
</ul>
<div class="warn-box">The key point: an apostille on a foreign document is done at home, before you travel — you can't get one in Georgia. This is the most common and painful mistake. An apostille on a Georgian document is done at the Public Service Hall.</div>
<h2 id="which">Documents translated most often</h2>
<p>Passport (for marriage and residence), birth/marriage/divorce certificates, police clearance, diplomas, income statements, powers of attorney, driving licence, property papers. For marriage the key one is the passport — the procedure is in <a href="/en/blog/how-to-get-married-in-georgia/">how to get married in Georgia</a>.</p>
<div class="info-box">One principle saves weeks: fix one transliteration of your name and keep it across every translation. If your name is spelled differently in the passport, a certificate and the translation, the system "sees" different people — and the document isn't accepted.</div>
<h2 id="packages">Packages by procedure</h2>
<ul>
<li><strong>Marriage.</strong> Both partners' passports with notarised translation; sometimes a certificate of no impediment from your country, with apostille. See the <a href="/en/interpreter-and-support-georgia/">interpreter and support</a> service for the ceremony.</li>
<li><strong>Residence.</strong> Passport with translation, proof of grounds, proof of income — full order in the <a href="/en/blog/residence-permit-georgia/">residence permit guide</a>.</li>
<li><strong>Bank and business.</strong> Passport, sometimes proof of address and income; for a company, founding documents translated. See <a href="/en/blog/open-bank-account-georgia/">opening an account</a> and <a href="/en/blog/company-registration-georgia/">company registration</a>.</li>
</ul>
<h2 id="validity">Validity of certificates</h2>
<p>Many documents have a "shelf life", and it breaks plans more often than you'd think. Police clearance and civil-status certificates are usually accepted only within a limited window from their issue date, so ordering them "for the future" is pointless — by submission they may expire. An apostille goes on a fresh certificate, not last year's. The logic: first confirm the required validity for your procedure, then order the certificate and apostille, and only then travel and translate.</p>
<h2 id="diploma">Diploma recognition and powers of attorney</h2>
<p>To work in your profession or to enrol, a diploma is translated and notarised, and for a number of regulated professions there's a separate qualification-recognition procedure — not the same as translation, and it takes longer, so start it early. A power of attorney issued abroad also needs translation and often an apostille; while a POA drawn up in Georgia for use abroad is made by a local notary, with the apostille added at the Public Service Hall. Precision of wording matters most here: a POA with a vague or mistranslated scope of powers simply won't work at the moment you need it, and by then you may be out of the country. If a document will be used in a third country, confirm that country's requirements too — Georgia's notarisation plus an apostille is the common chain, but the destination sets the rules.</p>
<h2 id="sworn">Sworn or notarised translation</h2>
<p>A frequent question from those used to the European system: do you need a "sworn translator"? Georgia doesn't use the sworn-translator institution in the familiar form — legal force comes not from the translator's status but from notarisation of their signature. So don't look for a "certified sworn translator"; look for a bureau that works with a notary and hands over a finished notarised translation. The same rule removes confusion: a translation notarised by a foreign notary won't do here.</p>
<h2 id="check">Check the translation before you submit</h2>
<p>Before taking a translation to an office, spend five minutes checking it — cheaper than a lost visit. Confirm the essentials: the name matches the passport letter for letter; all dates, document numbers and series are carried over without typos; the required scope is translated, not "half"; there's a notary mark and signature. Look separately at place names and organisation names — they're often translated inconsistently across papers. If anything looks off, fix it before submitting: redoing a translation is cheaper than paying the fee again and waiting for a new slot.</p>
<h2 id="where">Where and how fast</h2>
<p>Translation offices sit near the <a href="/en/blog/public-service-hall-georgia/">Public Service Hall</a> and often arrange notarisation themselves. A simple document is translated and notarised within a day, sometimes an hour; a deal package takes longer. When choosing a bureau, look beyond price — it's better if it works with a notary on site and takes on the whole "translate plus notarise" path.</p>
<h2 id="order">The order of steps</h2>
<ol>
<li>Check whether you need an apostille/legalisation — if so, do it at home before flying.</li>
<li>Bring the original to the office.</li>
<li>Translate into Georgian.</li>
<li>Notarise the translator's signature.</li>
<li>Submit to the relevant body.</li>
</ol>
<h2 id="mistakes">Common mistakes</h2>
<ul>
<li>Arriving without an apostille (you can't get one here on a foreign document);</li>
<li>notarising with a non-Georgian notary;</li>
<li>translating only part of the passport;</li>
<li>name spelling that differs across documents.</li>
</ul>
""" + cta_en("We'll assemble the package, translate, notarise and submit — no running between office, notary and window. Tell us which document you need.") + """
<div class="sources-block"><p class="sources-title">Official sources</p><ul>
<li><a href="https://napr.gov.ge/" rel="noopener noreferrer" target="_blank">National Agency of Public Registry (napr.gov.ge)</a></li>
<li><a href="https://psh.gov.ge/" rel="noopener noreferrer" target="_blank">Public Service Hall (psh.gov.ge)</a></li>
</ul></div>
""",
    "related": [
        ("Private guide in Tbilisi", "See the city with a local.", "/en/private-guide-tbilisi/"),
        ("Kakheti wine tour", "Georgia's wine country.", "/en/blog/kakheti-wine-tour/"),
        ("Guide for expats", "Settling into Tbilisi.", "/en/blog/tbilisi-for-expats/"),
    ],
    "faq": [
        ("Do I need a notarised passport translation for marriage?", "Yes, it's the key document for registration."),
        ("What is an apostille and where is it done?", "A simplified certification for Hague countries; on a foreign document it's done in the country of issue, before arrival."),
        ("Can it be notarised in a day?", "A simple document — often yes, sometimes within an hour."),
        ("Whole passport or one page?", "Usually the data page; confirm for your procedure."),
        ("Is an apostille done in Georgia?", "On Georgian documents yes; on foreign ones only at the country of issue."),
        ("Is a document in English still translated?", "Usually yes — offices accept Georgian, so even an English document is translated and notarised."),
        ("Can I translate straight from my language to Georgian?", "Yes, Tbilisi bureaus work from English, Russian and other languages directly into Georgian — no intermediate translation needed."),
        ("How much does a certified translation cost?", "It depends on language, volume and urgency, and notarisation is billed separately from the translation itself. A simple one-page document is usually inexpensive; a deal package costs more."),
    ],
})

ARTICLES.append({
    "lang": "en", "kind": "post",
    "url": "/en/blog/company-registration-georgia/", "blog_root": "/en/blog/",
    "alt": {"ru": "/blog/registratsiya-kompanii-v-gruzii/",
            "en": "/en/blog/company-registration-georgia/",
            "ge": "/ge/blog/company-registration-georgia/"},
    "title": "Register a Company or Sole Trader in Georgia 2026",
    "meta": "How to open an LLC or sole trader in Georgia 2026: legal forms, 1% small-business status, registration at the Public Service Hall, bank account, taxes and timelines.",
    "h1": "Registering a Company or Sole Trader in Georgia: 2026 Guide",
    "crumb": "Company registration",
    "label": "Guide · 8 min read",
    "image": "/images/blog/registratsiya-kompanii-gruzia.webp",
    "meta_bits": ["Guide", "Business in Georgia", "IE / LLC"],
    "toc": [("form", "Which form to choose"), ("status", "Small-business status (1%)"),
            ("vat", "VAT and when it kicks in"), ("docs", "Documents"), ("steps", "Step by step"),
            ("tax", "Tax and reporting"), ("pay", "How to pay tax"),
            ("hire", "Hiring staff"), ("close", "Pausing and closing"),
            ("special", "IT status and free zones"), ("cost", "Cost of running an IE"), ("mistakes", "Common mistakes")],
    "lead": "<strong>Setting up in Georgia is fast</strong>: a sole trader or LLC is registered at the Public Service Hall usually within one business day, and a foreigner can be the sole owner. For freelancers and small turnover there's the favourable <strong>small-business status</strong> at 1% of turnover.",
    "body": """
<h2 id="form">Which form to choose</h2>
<ul>
<li><strong>Individual Entrepreneur (IE / sole trader)</strong> — the simplest; fits freelancers and small business; eligible for 1% small-business status.</li>
<li><strong>LLC</strong> — for partners, employees or limited liability.</li>
<li><strong>Special regimes</strong> — free industrial zones, IT status — for specific models.</li>
</ul>
<p>For most self-employed movers the starting point is an <strong>IE plus small-business status</strong>. An LLC makes sense when there are partners, staff, or a need to protect personal assets.</p>
<h2 id="status">Small-business status (1%)</h2>
<p>An IE with annual turnover below the threshold (a common reference is GEL 500,000; confirm at rs.ge) can hold small-business status and pay <strong>1% of turnover</strong> instead of 20% income tax; above the threshold the rate is higher. This is the main reason freelancers and remote workers register here: working for foreign clients, the legal burden comes out minimal.</p>
<div class="info-box">Small-business status and opening an IE is a procedure at the tax service (rs.ge), while the bank only opens an account. These are two different steps, often confused.</div>
<p>The status has catches learned late. It's counted on turnover, not profit — the whole revenue matters, not what's left after costs. Some activities don't qualify — for instance consulting in some readings, and licensed fields — so check your exact activity in advance. And the status isn't granted automatically when you register the IE; you must request it separately, or you'll pay 20% instead of 1% all year.</p>
<h2 id="vat">VAT and when it kicks in</h2>
<p>A separate topic newcomers miss: VAT. Above a set turnover threshold you must register for VAT — and it's a different threshold from the small-business one. While you're a small freelancer it's irrelevant, but as turnover grows VAT can "switch on" unnoticed, and penalties for late registration are real. Check current thresholds and rates at rs.ge; if turnover is nearing the line, that's the cue to bring in an accountant.</p>
<h2 id="docs">Documents</h2>
<p>Passport (and translation if required); a legal address in Georgia (lease or owner consent); the application; for an LLC — charter and partner details. The address is verified — an empty one won't do.</p>
<h2 id="steps">Step by step</h2>
<ol>
<li>Choose the form and a name.</li>
<li>Prepare the address and documents.</li>
<li>File at the <a href="/en/blog/public-service-hall-georgia/">Public Service Hall</a> — usually same day (a "same-hour" expedited tariff exists).</li>
<li>Get the extract and tax number.</li>
<li>Register on the Revenue Service portal (rs.ge); request small-business status if relevant.</li>
<li>Open a business account — see <a href="/en/blog/open-bank-account-georgia/">how to open a bank account</a>.</li>
</ol>
<h2 id="tax">Tax and reporting</h2>
<div class="price-table-wrap"><table class="price-table">
<thead><tr><th>Form</th><th>Tax</th></tr></thead>
<tbody>
<tr><td>IE, no status</td><td>20% income</td></tr>
<tr><td>IE, small business</td><td>1% of turnover (below threshold)</td></tr>
<tr><td>LLC</td><td>15% on distributed profit (paid on dividends)</td></tr>
</tbody></table></div>
<p>A monthly turnover declaration is filed on rs.ge. A small IE's books are often self-kept; with staff or VAT, use an accountant — their fees in Georgia are modest.</p>
<h2 id="pay">How to pay tax, step by step</h2>
<ol>
<li>Through the month, record all revenue credited to the IE account.</li>
<li>By the set date next month, file the turnover declaration in your rs.ge account.</li>
<li>Pay the tax — 1% of turnover with small-business status — from the same portal.</li>
<li>Keep payment confirmations; the bank may ask for them when checking the source of funds.</li>
</ol>
<p>Missing a month means a fine and interest, so put the declaration in your calendar as a recurring task.</p>
<h2 id="hire">Hiring staff</h2>
<p>The moment you hire, payroll reporting is added: income tax is withheld from salaries, there are mandatory pension contributions, and it's all declared monthly. A solo IE has none of this, but the first employee complicates the accounting — here you almost always need an accountant. Contracts are drawn up in Georgian (or bilingual), and wording matters as much as in any official document.</p>
<h2 id="close">Pausing and closing</h2>
<p>Plans change, and a business sometimes needs pausing or closing. As long as the IE exists, the duty to file declarations remains — even with zero turnover you file "nil" returns, or penalties pile up. So if activity has stopped, it's better to close the IE officially than to abandon it. Closure goes through the tax service and the registry; settle debts and open periods before leaving the country. "Just stop using the account" is not the same as closing.</p>
<h2 id="special">IT status and free zones</h2>
<p>Some models have special regimes. IT companies may qualify for "international company" status or the virtual IT-zone regime with reduced rates — attractive for exporting IT services, but requiring criteria and a separate procedure. Free industrial zones (FIZ) give benefits to production and trade inside the zone. For a typical freelancer or consultant these are overkill — an IE with 1% status is enough — but a product IT company with a team should model a special regime in advance.</p>
<h2 id="cost">The cost of running an IE</h2>
<p>Opening an IE is cheap, but it has running costs to budget from the start: the tax (1% of turnover under small-business status); bank servicing (account maintenance, transfer, withdrawal and conversion fees); accounting if you don't do it yourself; and possibly a legal address if you don't have one. All this still makes Georgia one of the most favourable jurisdictions for a freelancer, but "1% and that's it" is an oversimplification — count the real burden as tax plus servicing plus bookkeeping.</p>
<h2 id="mistakes">Common mistakes</h2>
<ul>
<li>Setting up an LLC where an IE would do;</li>
<li>forgetting to request small-business status and paying 20% for a year;</li>
<li>underrating the real-address requirement;</li>
<li>missing the monthly declaration and getting fined.</li>
</ul>
""" + cta_en("We'll take you through registration, the tax portal and account opening, and translate at the bank interview — first time. Describe your case.") + """
<div class="sources-block"><p class="sources-title">Official sources</p><ul>
<li><a href="https://rs.ge/" rel="noopener noreferrer" target="_blank">Revenue Service of Georgia (rs.ge)</a></li>
<li><a href="https://napr.gov.ge/" rel="noopener noreferrer" target="_blank">Business Registry (napr.gov.ge)</a></li>
</ul></div>
""",
    "related": [
        ("Private guide in Tbilisi", "See the country on your days off.", "/en/private-guide-tbilisi/"),
        ("Digital nomad Tbilisi", "Living and working from Tbilisi.", "/en/blog/digital-nomad-tbilisi/"),
        ("Guide for expats", "Settling in.", "/en/blog/tbilisi-for-expats/"),
    ],
    "faq": [
        ("Can a foreigner open an IE or LLC?", "Yes, including as sole owner."),
        ("What does 1% status give?", "1% turnover tax instead of 20% income — below the threshold."),
        ("How long does registration take?", "Usually one business day; faster if expedited."),
        ("Is a real address required?", "Yes, it's verified."),
        ("LLC taxes?", "15% on distributed profit — paid on dividends."),
        ("Do I have to be in Georgia to register?", "Usually yes, filing is in person; registration by power of attorney is possible if the POA is properly prepared, translated and notarised."),
        ("Is a Georgian bank account required for an IE?", "It's convenient for operating and paying tax, but registering the IE and opening an account are separate steps at different institutions."),
    ],
})

ARTICLES.append({
    "lang": "en", "kind": "post",
    "url": "/en/blog/public-service-hall-georgia/", "blog_root": "/en/blog/",
    "alt": {"ru": "/blog/dom-yustitsii-tbilisi/",
            "en": "/en/blog/public-service-hall-georgia/",
            "ge": "/ge/blog/public-service-hall-georgia/"},
    "title": "Public Service Hall Tbilisi 2026: Services & Queue",
    "meta": "Public Service Hall in Tbilisi: what you can file at the one-stop shop, how to book, opening hours, queues, services for foreigners and using an interpreter.",
    "h1": "Public Service Hall in Tbilisi: What You Can Do at the One-Stop Shop",
    "crumb": "Public Service Hall",
    "label": "Guide · 7 min read",
    "image": "/images/blog/dom-yustitsii-tbilisi.webp",
    "meta_bits": ["Guide", "Living in Georgia", "Government"],
    "toc": [("what", "What you can file"), ("onestop", "How the one-stop shop works"),
            ("hours", "Hours, booking, queues"), ("foreigners", "What foreigners do"),
            ("marriage", "Getting married"), ("visit", "Your visit step by step"),
            ("bring", "What to bring"), ("fees", "Fees and payment"),
            ("online", "Online without a visit"), ("regions", "The Hall in the regions"),
            ("property", "Property and powers of attorney"), ("mistakes", "Common mistakes")],
    "lead": "The <strong>Public Service Hall</strong> is a one-stop shop where dozens of government services live under one roof: marriage, company papers, property, residence permits, certificates, apostille, notary acts. The Tbilisi flagship is the striking 'mushroom' building on the river. Here's what foreigners do there and how to get through without Georgian.",
    "body": """
<h2 id="what">What you can file</h2>
<p>Marriage and civil acts; <a href="/en/blog/company-registration-georgia/">company registration</a> (IE/LLC); property rights and deals; <a href="/en/blog/residence-permit-georgia/">residence-permit</a> and ID applications; birth and name-change acts; apostille on Georgian documents; extracts and certificates; some notary and banking services right in the hall. Most of a newcomer's official questions are solved here.</p>
<h2 id="onestop">How the one-stop shop works</h2>
<p>You take a ticket for the service, wait for your number on the board, go to the operator, submit documents and pay the fee on the spot. Many services are same-day. Operators serve in Georgian (some in English), and forms and receipts are in Georgian — that's where translation matters, to fill the application right and not take the wrong ticket.</p>
<h2 id="hours">Hours, booking and queues</h2>
<p>The Tbilisi flagship works on weekends too (check the current schedule at psh.gov.ge). Some services allow booking, which saves time; for high-volume services the walk-in queue is noticeable before noon. From experience: come early with a complete file so you don't visit twice — the top cause of a repeat trip.</p>
<div class="info-box">The most common "lost day" is arriving without a notarised translation or apostille. How to prepare them in advance is in the guide to <a href="/en/blog/document-translation-notary-georgia/">document translation and notary</a>.</div>
<h2 id="foreigners">What foreigners do most</h2>
<ul>
<li><strong>Get married</strong> — Georgia is fast, often same day; see <a href="/en/blog/how-to-get-married-in-georgia/">how to get married in Georgia</a>;</li>
<li><strong>open an IE/LLC</strong> — see <a href="/en/blog/company-registration-georgia/">company registration</a>;</li>
<li><strong>apply for residency</strong> — see the <a href="/en/blog/residence-permit-georgia/">residence permit</a>;</li>
<li><strong>notarise translations and apostille</strong> on Georgian documents.</li>
</ul>
<h2 id="marriage">Getting married</h2>
<p>Marriage is one of the most common reasons foreigners come to the Hall, and Georgia is genuinely convenient: minimal requirements, and you can often marry the same day or the next. Both partners need valid passports with a notarised translation; in some cases a certificate of no impediment prepared at home with an apostille. The key nuance: the ceremony and paperwork run in Georgian, so an interpreter isn't a formality but a requirement — without understanding what you sign, they simply won't register it. There's also a "ceremonial" format in dedicated halls if you want an event, not just a stamp. How we support at the registration is described in the <a href="/en/interpreter-and-support-georgia/">interpreter and support</a> service.</p>
<h2 id="visit">Your visit, step by step</h2>
<ol>
<li>Confirm the service and documents in advance.</li>
<li>Book online if possible.</li>
<li>Take a ticket or arrive for your slot.</li>
<li>Submit documents and translations, pay the fee.</li>
<li>Get the result or a set date.</li>
</ol>
<h2 id="bring">What to bring</h2>
<p>Passport and notarised translations; apostille if your procedure needs it; proof of grounds (contract, certificate); money for the fee — card or cash. An incomplete file is the main reason for a lost day.</p>
<h2 id="fees">Fees and payment</h2>
<p>Almost every service is paid, and most have an expedited tariff: the faster you need it, the more it costs. Roughly there's "standard" (a few working days), "expedited" (a day) and "same hour" for some services — the price difference is multiple. You pay on site by card or cash, sometimes at a terminal in the hall. Exact amounts change and depend on the service, so we don't quote "permanent" figures — check psh.gov.ge or ask the information desk. Know not only the fee but which tariff you actually need: often "standard" is fine and paying for speed is unnecessary.</p>
<h2 id="online">Online without a visit</h2>
<p>Some services don't require a trip. On the government services portal you order a range of certificates and extracts electronically, with the finished document delivered digitally or collected later. This saves the queue for simple requests like a registry extract. But complex procedures — marriage, company registration, a residence application, property deals — are still done in person, because originals, signatures and presence are needed. A useful strategy: close what you can online in advance, and go to the hall only with what needs your presence. Once you hold a Georgian ID, more of the portal opens up, including digital access to many records — handy for repeat requests without queueing.</p>
<h2 id="regions">The Hall in the regions</h2>
<p>The Tbilisi flagship is the best known, but the network is wider: branches work in Batumi, Kutaisi, Rustavi and other cities, and in smaller towns basic services are provided by Community Centers. If you don't live in the capital, you needn't travel to Tbilisi for a certificate — first check the nearest branch at psh.gov.ge. The range of services in the regions may be narrower than at the flagship, so confirm rare procedures in advance.</p>
<h2 id="property">Property and powers of attorney</h2>
<p>A major block of Hall services is real estate: registering ownership on purchase, registry extracts, mortgages and contracts. For a foreigner this is one of the most sensitive procedures — the deal and contract are in Georgian, and an error in wording or an unnoticed encumbrance is expensive. Before buying, order a fresh registry extract to confirm the property is clean. Powers of attorney are also done here — for example if you want a representative to act while you're abroad; the POA is made by a notary and, for use abroad, gets an apostille. In all these cases an interpreter's presence is not a luxury but a way to understand what you're signing.</p>
<h2 id="mistakes">Common mistakes</h2>
<ul>
<li>Coming without a notarised translation or apostille;</li>
<li>mixing up service and ticket;</li>
<li>arriving at peak with no booking;</li>
<li>not knowing the exact fee.</li>
</ul>
""" + cta_en("We'll tell you the service and package, book, translate at the window and guide you from ticket to result. Tell us what you need to file.") + """
<div class="sources-block"><p class="sources-title">Official sources</p><ul>
<li><a href="https://psh.gov.ge/" rel="noopener noreferrer" target="_blank">Public Service Hall (psh.gov.ge)</a></li>
<li><a href="https://sda.gov.ge/" rel="noopener noreferrer" target="_blank">Public Service Development Agency (sda.gov.ge)</a></li>
</ul></div>
""",
    "related": [
        ("Private guide in Tbilisi", "Old town, Mtskheta, Kazbegi.", "/en/private-guide-tbilisi/"),
        ("Kazbegi day trip", "Mountains in one day.", "/en/blog/kazbegi-day-trip-from-tbilisi/"),
        ("Guide for expats", "Settling into Tbilisi.", "/en/blog/tbilisi-for-expats/"),
    ],
    "faq": [
        ("What can I file there?", "Marriage, company, property, residency, certificates, apostille, notary acts."),
        ("Do I need to book?", "Some services allow it and save time; others have walk-in queues."),
        ("Open on weekends?", "The Tbilisi flagship yes; check psh.gov.ge."),
        ("What language?", "Georgian, some services English; paperwork in Georgian."),
        ("What to bring?", "Passport, notarised translations, apostille if needed, fee money."),
        ("Are there branches in other cities?", "Yes — besides Tbilisi, in Batumi, Kutaisi, Rustavi and others, plus Community Centers; the range may be narrower."),
        ("Can I do anything online?", "Some certificates and extracts can be ordered on the government portal; complex procedures like marriage, company and residency are still in person."),
        ("Is English spoken at the Hall?", "Some operators speak English, but forms and receipts are in Georgian, so an interpreter helps you fill the application correctly and take the right ticket."),
    ],
})


# ── content: GE (local / referral intent) ─────────────────────────────────────
ARTICLES.append({
    "lang": "ge", "kind": "service", "og_type": "website",
    "url": "/ge/interpreter-and-support-georgia/", "blog_root": "/ge/blog/",
    "alt": {"ru": "/perevodchik-i-soprovozhdenie-v-gruzii/",
            "en": "/en/interpreter-and-support-georgia/",
            "ge": "/ge/interpreter-and-support-georgia/"},
    "title": "თარჯიმანი და თანხლება საქართველოში — თბილისი",
    "meta": "რუსულ- და ინგლისურენოვანი თარჯიმანი და პირადი თანხლება საქართველოში: ექიმი, პოლიცია, ბანკი, ნოტარიუსი, ქორწინება, ბინადრობა. ვთარგმნით და თან გახლავართ.",
    "h1": "თარჯიმანი და პირადი თანხლება საქართველოში",
    "crumb": "თარჯიმანი და თანხლება",
    "label": "სერვისი · თბილისი და მიმდებარე",
    "service_type": "Interpreter and personal accompaniment",
    "image": "/images/blog/perevodchik-soprovozhdenie.webp",
    "meta_bits": ["სერვისი", "თბილისი", "რუს/ინგ ↔ ქართ"],
    "toc": [("vin", "ვისთვის არის"), ("ra", "რაში ვეხმარებით"),
            ("adamiani", "ცოცხალი თარჯიმანი თუ აპლიკაცია"), ("gansxvaveba", "რით განვსხვავდებით ბიუროსგან"),
            ("istoriebi", "სამი ჩვეულებრივი შემთხვევა"), ("mzadeba", "როგორ მოვემზადოთ"),
            ("sazghvrebi", "რას ვაკეთებთ და რას არა"),
            ("rogor", "როგორ მუშაობს"), ("formatebi", "ფორმატები და ენები"),
            ("fasi", "ფასი"), ("shემდeg", "შემდეგ — საქართველოს გაცნობა")],
    "lead": "როცა უცხოელ სტუმარს, პარტნიორს ან კლიენტს საქართველოში საქმის მოგვარება სჭირდება და ყველაფერი ენასა და ადგილობრივ წესრიგზეა დამოკიდებული — ექიმთან ვიზიტი, პოლიცია, ბანკი, ნოტარიუსი, ქორწინება — <strong>გვერდით ცოცხალი ადამიანია საჭირო, და არა ლექსიკონი</strong>. ჩვენ არ ვართ თარგმანის ბიურო: უცხოელს ქართულ სისტემაში მისთვის გასაგებ ენაზე გავყავართ და, საჭიროებისას, ადგილზეც მივდივართ.",
    "body": """
<h2 id="vin">ვისთვის არის ეს სერვისი</h2>
<p>თუ ქართველი ხართ და გყავთ უცხოელი სტუმარი, ნათესავი, კლიენტი ან პარტნიორი, რომელსაც ქართული არ ესმის — ეს გვერდი თქვენთვის და მათთვისაა. ხშირად ადამიანი ახლახან ჩამოვიდა ან გადმოვიდა საცხოვრებლად, ქართული არ იცის და საქმის მოგვარება დღესვე სჭირდება. რუსული ყველგან არ ისმის, სახელმწიფო დაწესებულებები კი ქართულად მუშაობენ. ასეთ დროს საჭიროა არა სიტყვების მთარგმნელი, არამედ ადამიანი, ვინც ენასაც იცის და ადგილობრივ წესრიგსაც.</p>
<p>თბილისში მუშაობის წლების გამოცდილებით ვიცით, სად ჭედავს ხოლმე საქმე: არასწორი ტალონი, არასრული საბუთები, დაუმოწმებელი თარგმანი, აპოსტილი, რომელიც ჯერ სახლში უნდა დაესვათ. პრობლემის ნახევარი ვიზიტამდე იხსნება — სწორი მომზადებით.</p>
<p>თუ თქვენ თავად ქართველი ხართ, ეს სერვისი თქვენს უცხოელ სტუმარს, ნათესავს ან პარტნიორსაც გამოადგება: მას ვუწევთ თანხლებას, თქვენ კი დარწმუნებული ხართ, რომ ადამიანი მარტო არ დარჩება ბიუროკრატიასთან. ხშირად ქართველი მეგობარი ან დამსაქმებელი გვირჩევს ხოლმე — რადგან თავად არ სცალია მთელი დღე უწყებებში გაატაროს, ჩვენ კი სწორედ ამას ვაკეთებთ პროფესიულად.</p>
<h2 id="ra">რაში ვეხმარებით</h2>
<ul>
<li><strong>ჯანდაცვა.</strong> ვიზიტი ექიმთან, ანალიზები, სტომატოლოგია, ორსულობა და მშობიარობა, აფთიაქი. ვჯავშნით, ვრეკავთ, ვუხსნით ექიმს პრობლემას და ვთარგმნით დიაგნოზს აზრის დაკარგვის გარეშე. საქართველო ხელმისაწვდომი მკურნალობის ცენტრიცაა — იხ. <a href="/ge/blog/dental-tourism-georgia/">სტომატოლოგიური ტურიზმი</a>.</li>
<li><strong>პოლიცია და სამართალი.</strong> ურთიერთობა პოლიციასთან, საგზაო შემთხვევა, ნოტარიუსი, მინდობილობა, სასამართლო. იხ. <a href="/ge/blog/document-translation-notary-georgia/">თარგმანი და ნოტარიული დამოწმება</a>.</li>
<li><strong>ქორწინება.</strong> საქართველო ერთ-ერთი უმარტივესი ადგილია დასაქორწინებლად — ხშირად იმავე დღეს. ცერემონია ქართულადაა, ამიტომ თარჯიმანი აუცილებელია. იხ. <a href="/ge/blog/how-to-get-married-in-georgia/">როგორ დავქორწინდეთ საქართველოში</a>.</li>
<li><strong>ბანკი, ბინადრობა, გასაუბრება.</strong> ანგარიშის გახსნა — იხ. <a href="/ge/blog/open-bank-account-georgia/">როგორ გავხსნათ საბანკო ანგარიში</a>; ლეგალიზაცია — <a href="/ge/blog/residence-permit-georgia/">ბინადრობის ნებართვა</a>.</li>
<li><strong>ბიზნესი.</strong> შეხვედრები პარტნიორებთან, კომპანიის რეგისტრაცია — იხ. <a href="/ge/blog/company-registration-georgia/">კომპანიის რეგისტრაცია</a>.</li>
</ul>
<h2 id="adamiani">ცოცხალი თარჯიმანი თუ აპლიკაცია</h2>
<p>მთარგმნელი აპლიკაცია კაფესა და ბაზარში გამოგადგებათ, მაგრამ ექიმის კაბინეტში ან სახელმწიფო სარკმელთან ის სამ რამეში აგებს. კონტექსტი: ექიმი საუბრობს ქვეტექსტით, დამაზუსტებელი კითხვებითა და დათქმებით — სწორედ ამას კარგავს მანქანა. პასუხისმგებლობა: როცა საქმე დიაგნოზს, მინდობილობას ან ოქმის ფორმულირებას ეხება, „დაახლოებით ასე“ დაუშვებელია. პროცედურა: სარგებლის ნახევარი თარგმანი კი არა, ის არის, რომ გვერდით დგას ადამიანი, ვინც იცის, რომელი ტალონი აიღოს და რომელი სარკმელია თქვენი.</p>
<p>ეს არ ნიშნავს, რომ აპლიკაცია უსარგებლოა — ის კარგია მარტივი, ყოველდღიური სიტუაციებისთვის. მაგრამ როცა შედეგი დოკუმენტში ილუქება ან ჯანმრთელობას ეხება, ცოცხალი თარჯიმანი და ადამიანი, ვინც სისტემას იცნობს, სულ სხვა დონის საიმედოობაა.</p>
<div class="info-box">ჩვენ არ ვცვლით ნოტარიუსს ან ექიმს — ვაკეთებთ ისე, რომ თქვენ გაიგოთ ისინი და მათ გაიგონ თქვენ, საბუთები კი წინასწარ და სწორი თანმიმდევრობით იყოს შეკრებილი.</div>
<h2 id="gansxvaveba">რით განვსხვავდებით ბიუროსგან</h2>
<p>ბიურო ყიდის სიტყვებსა და საათებს: თქვენ მიდიხართ მასთან, იღებთ ნათარგმნ ფურცელს და მარტო რჩებით რიგთან, ტალონთან და ქართულ ანკეტასთან. ჩვენ ვყიდით თქვენი ამოცანის შედეგს — პირველი შეტყობინებიდან დოკუმენტზე ბეჭდამდე.</p>
<div class="price-table-wrap"><table class="price-table">
<thead><tr><th></th><th>ბიურო</th><th>Sakhva-ს თანხლება</th></tr></thead>
<tbody>
<tr><td>ყიდის</td><td>სიტყვებს, საათებს</td><td>ამოცანას ბოლომდე</td></tr>
<tr><td>სისტემა</td><td>თარგმნის ტექსტს</td><td>იცნობს კლინიკებს, ბანკებს, უწყებებს</td></tr>
<tr><td>ფორმატი</td><td>თქვენ მიდიხართ</td><td>ჩვენ მოვდივართ, საჭიროებისას მანქანით</td></tr>
<tr><td>ნდობა</td><td>ერთჯერადი</td><td>საქართველოში 2023 წლიდან, საკუთარი გიდი და მძღოლი</td></tr>
</tbody></table></div>
<p>ეს განსხვავება პრაქტიკაში მარტივად ჩანს: ბიუროდან გამოხვალთ ნათარგმნი ფურცლით, მაგრამ მაინც არ იცით, რომელ სართულზე ახვიდეთ, რომელი ტალონი აიღოთ და რას გეტყვიან სარკმელთან. ჩვენთან ეს კითხვები საერთოდ არ ჩნდება — იმიტომ, რომ გვერდით ვდგავართ და პროცესს ბოლომდე მივყავართ.</p>
<h2 id="istoriebi">სამი ჩვეულებრივი შემთხვევა</h2>
<ul>
<li><strong>ვიზიტი ექიმთან.</strong> ქრონიკული დაავადების მქონე ადამიანი გადმოდის და ვერ უხსნის კარდიოლოგს ისტორიასა და მედიკამენტებს. ჩვენ ვპოულობთ ექიმს, ვჯავშნით, ვთარგმნით ანამნეზსა და დანიშნულებას და ვადევნებთ თვალს, რომ დოზირება და პრეპარატების სახელები ორივე მხარემ სწორად გაიგოს.</li>
<li><strong>ბანკმა უარი თქვა.</strong> 2023 წლის შემდეგ ბანკები მკაცრდებიან და განაცხადს ხშირად ხსნის გარეშე აბრუნებენ. ჩვენ ერთად მივდივართ გასაუბრებაზე, ვეხმარებით ქვეყანასთან კავშირის ჩვენებაში (იჯარა, ბინადრობა, კონტრაქტი) და ვთარგმნით.</li>
<li><strong>ქორწინება.</strong> წყვილს სურს დაქორწინება თბილისში და არ იცის, რომ პასპორტს ნოტარიული თარგმანი სჭირდება, ცერემონია კი ქართულადაა. ჩვენ წინასწარ ვკრებთ პაკეტს, ვთარგმნით ცერემონიაზე და მივყავართ ტალონიდან მოწმობამდე.</li>
</ul>
<h2 id="mzadeba">როგორ მოვემზადოთ ვიზიტამდე</h2>
<p>პრობლემების უმეტესობა ადგილზე გმირობით კი არა, მომზადებით იხსნება. ნებისმიერი ოფიციალური ვიზიტის წინ ღირს ოთხი პუნქტის დახურვა: დააზუსტეთ ზუსტი სერვისი და საბუთების სია — სარკმლის სახელით, და არა „დაახლოებით“; წინასწარ გააკეთეთ ნოტარიული თარგმანი და, საჭიროებისას, აპოსტილი (უცხოურ საბუთზე მას მხოლოდ სახლში, ჩამოსვლამდე დაასვამენ); დაიყვანეთ სახელი ერთ ტრანსლიტერაციამდე ყველა საბუთში; გაიგეთ მოსაკრებლის ოდენობა და გადახდის წესი. ამ ჩეკლისტს თქვენთან ერთად გავივლით — და ვიზიტი 20-წუთიან ფორმალობად იქცევა.</p>
<h2 id="sazghvrebi">რას ვაკეთებთ და რას არა</h2>
<p>სერვისის საზღვრების გულწრფელობა ყველას დროს ზოგავს. ჩვენ ვთარგმნით, ვამზადებთ და თან გახლავართ: ვკრებთ პაკეტს, ვხსნით პროცედურას, ვდგავართ გვერდით მიღებასა და სარკმელთან, გავყავართ ტალონიდან შედეგამდე. ჩვენ არ ვცემთ იურიდიულ დასკვნას ადვოკატის ნაცვლად, არ ვსვამთ დიაგნოზს ექიმის ნაცვლად და არ გპირდებით, რომ სახელმწიფო უწყება აუცილებლად დადებით გადაწყვეტილებას მიიღებს — შედეგი თქვენს საბუთებსა და საფუძვლებზეა დამოკიდებული, და არა ჩვენს სურვილზე.</p>
<p>სამაგიეროდ წინასწარ გულწრფელად გეტყვით, თუ რაიმე აკლია ან შანსები დაბალია — რომ მოსაკრებელი ტყუილად არ გადაიხადოთ. თუ ამოცანა თარგმანსა და თანხლებას სცილდება და საჭიროა ლიცენზირებული იურისტი ან ბუღალტერი, პირდაპირ გეტყვით და, სადაც შესაძლებელია, გირჩევთ, ვის მიმართოთ. ეს მიდგომა უცხოელ სტუმარსაც აშველებს და თქვენც, ვინც მას გვირჩევს, გაძლევთ დარწმუნებას, რომ ადამიანი კარგ ხელშია.</p>
""" + cta_ge("აღწერეთ სიტუაცია — ექიმი, ბანკი, ნოტარიუსი თუ ქორწინება — და ჩვენ გვერდით ვიქნებით, ვთარგმნით და გაგიყვანთ ყველა სარკმელში.") + """
<h2 id="rogor">როგორ მუშაობს</h2>
<ol>
<li><strong>მოთხოვნა.</strong> მოგვწერეთ სიტუაცია: რა, სად და როდის. რამდენიმე წინადადება საკმარისია.</li>
<li><strong>დაზუსტება.</strong> ვსვამთ მოკლე კითხვებს, ვადგენთ საბუთების სიას, ვთანხმდებით დროსა და ადგილს.</li>
<li><strong>თანხლება.</strong> გხვდებით ადგილზე ან მოვდივართ თქვენთან, ვთარგმნით და გამყავართ მთელ პროცესში.</li>
<li><strong>შედეგი.</strong> საქმე პირველივე ჯერზე კეთდება; საჭიროებისას თარგმანსა და დამოწმებაშიც გეხმარებით.</li>
</ol>
<h2 id="formatebi">ფორმატები და ენები</h2>
<p>პირადი თანხლება ვიზიტზე; თანხლება ტრანსფერით; სასწრაფო ვიზიტი იმავე დღეს; სატელეფონო თარგმანი მოკლე დისტანციური დახმარებისთვის. ენები: ინგლისური ↔ ქართული და რუსული ↔ ქართული.</p>
<p>ფორმატს სიტუაციაზე ვარგებთ: თუ საქმე მარტივია — მოკლე სატელეფონო თარგმანი კმარა; თუ დღე რამდენიმე უწყებას მოიცავს — სრული თანხლება ტრანსფერით სჯობს, რომ ქალაქში დროს არ კარგავდეთ და ერთი სარკმლიდან მეორეში მარტო არ დარბოდეთ. სასწრაფო შემთხვევებში იმავე დღეს გამოვდივართ, თუ გრაფიკი იძლევა.</p>
<h2 id="fasi">ფასი</h2>
<p>დამოკიდებულია სიტუაციაზე, ხანგრძლივობასა და ტრანსფერის საჭიროებაზე. ჩვენ „სიტყვაში“ არ ვიღებთ საფასურს — ვიღებთ მოგვარებულ ამოცანაში. მოგვწერეთ, რა გჭირდებათ, და ფასს წინასწარ გეტყვით.</p>
<p>ფასს ყოველთვის წინასწარ ვასახელებთ, სანამ დაიწყებთ — რომ არ აღმოჩნდეთ სიტუაციაში, სადაც „მრიცხველი“ ჩართულია და ხარჯი გაუგებარია. ეს განსაკუთრებით მნიშვნელოვანია, როცა უცხოელი ახლად ჩამოსულია და ჯერ არ ერკვევა ადგილობრივ ფასებში. ფორმატსაც სიტუაციის მიხედვით ვირჩევთ: ზოგჯერ ერთი სატელეფონო ზარი კმარა, ზოგჯერ კი მთელი დღის თანხლება რამდენიმე უწყებაში — და თუ რამდენიმე საქმის ერთ ვიზიტში გაერთიანება შეიძლება, ამასაც წინასწარ ვგეგმავთ, რომ თქვენი დრო დაიზოგოს.</p>
<h2 id="shემდeg">შემდეგ — საქართველოს გაცნობა</h2>
<p>როცა საბუთები უკან რჩება, ქვეყანა სანახავია. საქართველოს თავად ვაჩვენებთ: <a href="/ge/private-guide-tbilisi/">კერძო გიდი თბილისში</a> წაგიყვანთ ყაზბეგზე, კახეთსა და მცხეთაში თქვენი ტემპით.</p>
""",
    "related": [
        ("კერძო გიდი თბილისში", "ინდივიდუალური მარშრუტები ქალაქსა და ქვეყანაში.", "/ge/private-guide-tbilisi/"),
        ("ყაზბეგი ერთ დღეში", "მთა და გერგეტის ეკლესია ერთ დღეში.", "/ge/blog/kazbegi-day-trip-from-tbilisi/"),
        ("კახეთის ღვინის ტური", "ღვინის მხარე გიდთან ერთად.", "/ge/blog/kakheti-wine-tour/"),
    ],
    "faq": [
        ("საჭიროა ნოტარიულად დამოწმებული თარგმანი?", "ზოგი პროცედურისთვის — კი (მაგ. პასპორტი ქორწინებისთვის). ზუსტად გეტყვით, რა და მოვაგვარებთ."),
        ("შესაძლებელია იმავე დღეს?", "დიახ, როცა შესაძლებელია — რაც უფრო ადრე მოგვწერთ, მით უკეთესი დროა."),
        ("მხოლოდ თბილისში მუშაობთ?", "თბილისი და მიმდებარე ტერიტორია მთავარი ზონაა; სხვა რეგიონები შეთანხმებით."),
        ("თუ არ ვიცი, ზუსტად რა მჭირდება?", "აღწერეთ სიტუაცია თქვენი სიტყვებით — ერთად გავარკვევთ."),
        ("მუშაობთ შაბათ-კვირას?", "დიახ, შეთანხმებით — ბევრი უწყება შაბათს მუშაობს, ამიტომ ვიზიტსაც შესაბამისად ვგეგმავთ."),
        ("ვისთვის ვმუშაობთ — სტუმრისთვის თუ მასპინძლისთვის?", "ორივესთვის: ქართველი მასპინძელი ხშირად გვირჩევს, ჩვენ კი მის უცხოელ სტუმარს თან ვახლავართ ბიუროკრატიაში."),
    ],
})

ARTICLES.append({
    "lang": "ge", "kind": "post",
    "url": "/ge/blog/residence-permit-georgia/", "blog_root": "/ge/blog/",
    "alt": {"ru": "/blog/vid-na-zhitelstvo-v-gruzii/",
            "en": "/en/blog/residence-permit-georgia/",
            "ge": "/ge/blog/residence-permit-georgia/"},
    "title": "ბინადრობის ნებართვა საქართველოში 2026: ტიპები",
    "meta": "ბინადრობის ნებართვის ტიპები საქართველოში 2026: შრომითი, საინვესტიციო, უძრავ ქონებაზე, სასწავლო, ოჯახური. საბუთები, პროცესი, ვადები და უარის მიზეზები.",
    "h1": "ბინადრობის ნებართვა საქართველოში 2026: ტიპები და მიღების გზა",
    "crumb": "ბინადრობის ნებართვა",
    "label": "გზამკვლევი · 8 წთ",
    "image": "/images/blog/vid-na-zhitelstvo-v-gruzii.webp",
    "meta_bits": ["გზამკვლევი", "ცხოვრება საქართველოში", "ბინადრობა"],
    "toc": [("sჭიro", "საჭიროა თუ არა"), ("tipebi", "ტიპები"), ("ras", "რას იძლევა და რას არა"),
            ("sabutebi", "საბუთები"), ("process", "პროცესი ეტაპობრივად"),
            ("vadebi", "ვადები და ღირებულება"), ("rezidentoba", "საგადასახადო რეზიდენტობა"),
            ("gagrძeleba", "გაგრძელება და მუდმივი"), ("uari", "უარის მიზეზები"),
            ("ojaxi", "ოჯახთან ერთად"), ("scenarebi", "ტიპური სცენარები")],
    "lead": "<strong>ბინადრობის ნებართვა</strong> უცხოელს აძლევს უფლებას იცხოვროს საქართველოში უვიზო პერიოდის დასრულების შემდეგაც. გაიცემა სახელმწიფო სერვისების განვითარების სააგენტოსა და იუსტიციის სახლის მეშვეობით. გზა რამდენიმეა — შრომა, სწავლა, ინვესტიცია, უძრავი ქონება ზღვარს ზემოთ და ოჯახის გაერთიანება.",
    "body": """
<h2 id="sჭიro">საჭიროა თუ არა საერთოდ</h2>
<p>ბევრი ქვეყნის მოქალაქეს საქართველოში უვიზოდ ყოფნა 1 წლამდე შეუძლია. სანამ ეს გაწყობთ, ნებართვა მკაცრად სავალდებულო არ არის. ის საჭიროა ადგილობრივი კონტრაქტით მუშაობისთვის, სწავლისთვის, გრძელვადიანი ბიზნესის სიმყარისთვის, ქონების შესაძენად, ოჯახის ჩამოსაყვანად ან მუდმივი ბინადრობისკენ მოძრაობისთვის. პრაქტიკაში ბევრი მას პროგნოზირებადობისთვის იღებს — რომ წელი საზღვრის კვეთით არ განაახლოს.</p>
<div class="info-box">ბინადრობა და საგადასახადო რეზიდენტობა სხვადასხვა რამაა. რეზიდენტობა 12 თვეში 183 დღის ქვეყანაში ყოფნის შემდეგ დგება და გადასახადებს ეხება, არა ცხოვრების უფლებას.</div>
<h2 id="tipebi">ბინადრობის ტიპები</h2>
<ul>
<li><strong>შრომითი</strong> — ქართულ კომპანიასთან კონტრაქტით ან მეწარმედ, ბრუნვის დადასტურებით.</li>
<li><strong>სასწავლო</strong> — ავტორიზებულ უნივერსიტეტში ჩარიცხვა.</li>
<li><strong>საინვესტიციო</strong> — ზღვარზე მეტი ინვესტიცია; უფრო ხანგრძლივი ვადით.</li>
<li><strong>უძრავ ქონებაზე</strong> — ზღვარზე მეტი ღირებულების ქონების ფლობა (ორიენტირი ~100 000 აშშ დოლარი; ზუსტი თანხა და შეფასების წესი დააზუსტეთ sda.gov.ge-ზე — ისინი იცვლება).</li>
<li><strong>ოჯახური</strong> — ნებართვის მფლობელის მეუღლისა და შვილებისთვის.</li>
<li><strong>მოკლევადიანი</strong> — ქონების ფლობიდან, ერთი წელი, განახლებადი.</li>
</ul>
<p>რომელი ტიპი აირჩიოთ, დამოკიდებულია იმაზე, რატომ ხართ საქართველოში. თუ მუშაობთ — შრომითი; თუ სწავლობთ — სასწავლო; თუ ინვესტიცია ან ქონება გაქვთ — შესაბამისი. ერთსა და იმავე ადამიანს ხანდახან რამდენიმე საფუძველი აქვს — მაშინ ირჩევენ იმას, რომელიც ყველაზე მყარადაა დოკუმენტებით გამყარებული, რადგან სწორედ ამას ამოწმებენ.</p>
<h2 id="ras">რას იძლევა და რას არა</h2>
<p>ნებართვის მფლობელი ცხოვრობს საქართველოში უვიზო წელზე მიბმის გარეშე, ოფიციალურად ქირაობს გრძელვადიანად და საბანკო ანგარიშსაც უფრო მარტივად ხსნის — ბინადრობის მოწმობა ხსნის „ქვეყანასთან კავშირის“ კითხვას, რომლის გამოც ბანკები 2023-ის შემდეგ არარეზიდენტებს ხშირად აბრუნებენ. შრომითი ნებართვა ადგილობრივად დასაქმების უფლებას იძლევა.</p>
<p>რას არ იძლევა ავტომატურად: არ გხდით მოქალაქედ და არ ცვლის პასპორტს გასამგზავრებლად, არ გათავისუფლებთ თქვენი ქვეყნის გადასახადებისგან და თავისთავად არ ქმნის საგადასახადო რეზიდენტობას. სასწავლო და ოჯახური ზღუდავს დასაქმებას. ამიტომ კატეგორია რეალური მიზნით აირჩიეთ.</p>
<p>პრაქტიკული დასკვნა: ბინადრობა უპირველესად პროგნოზირებადობას გაძლევთ — აღარ გჭირდებათ წლის „განულება“ საზღვრის კვეთით და შეგიძლიათ გრძელვადიანად დაგეგმოთ ცხოვრება, ბიზნესი და ოჯახი. სწორედ ამიტომ იღებს ბევრი მას მაშინაც, როცა ფორმალურად ჯერ სავალდებულო არ არის.</p>
<h2 id="sabutebi">საბუთები: საბაზისო ნაკრები</h2>
<p>მოქმედი პასპორტი და მისი ნოტარიულად დამოწმებული ქართული თარგმანი; განაცხადი და ფოტო; საფუძვლის დამადასტურებელი (კონტრაქტი, ჩარიცხვის ცნობა, ამონაწერი ქონებაზე, საინვესტიციო დოკუმენტები); გადახდისუნარიანობის დადასტურება; მოსაკრებლის ქვითარი. ზუსტი სია კატეგორიაზეა დამოკიდებული. თარგმანი და დამოწმება ცალკე ეტაპია — იხ. <a href="/ge/blog/document-translation-notary-georgia/">თარგმანი და ნოტარიუსი</a>.</p>
<p>ზუსტი სია კატეგორიის მიხედვით იცვლება, ამიტომ სანამ თარგმანს გააკეთებთ, დააზუსტეთ, რა სჭირდება ზუსტად თქვენს საფუძველს — ეს ზოგავს ზედმეტ თარგმანსა და ხარჯს.</p>
<h2 id="process">პროცესი — ეტაპობრივად</h2>
<ol>
<li>აირჩიეთ შესაფერისი კატეგორია და შეაგროვეთ საფუძვლები.</li>
<li>თარგმნეთ და დაამოწმეთ პასპორტი და ცნობები.</li>
<li>შეიტანეთ განაცხადი <a href="/ge/blog/public-service-hall-georgia/">იუსტიციის სახლში</a> ან სააგენტოში.</li>
<li>გადაიხადეთ მოსაკრებელი — სტანდარტული თუ დაჩქარებული.</li>
<li>დაელოდეთ გადაწყვეტილებას.</li>
<li>აიღეთ ბინადრობის მოწმობა.</li>
</ol>
<p>თუ პარალელურად ანგარიშს ხსნით, გამოგადგებათ <a href="/ge/blog/open-bank-account-georgia/">როგორ გავხსნათ საბანკო ანგარიში</a> — ბანკები 2023-ის შემდეგ მკაცრები არიან.</p>
<p>ვადებში ჩავარდნის თავიდან ასაცილებლად საბუთები წინასწარ მოამზადეთ: თარგმანი და აპოსტილი დროში ყველაზე ხშირად აჭიანურებს პროცესს. თუ ყველა ცნობა ერთდროულად გაქვთ, თავად შეტანა სწრაფია და ხშირად ერთ ვიზიტში თავსდება.</p>
<h2 id="vadebi">ვადები და ღირებულება</h2>
<p>განხილვას ჩვეულებრივ რამდენიმე კვირა სჭირდება; დაჩქარებული ტარიფი ამცირებს ვადას. მოსაკრებელი კატეგორიასა და სისწრაფეზეა დამოკიდებული — მიმდინარე 2026 წლის ტარიფები იხ. sda.gov.ge-ზე; „მუდმივ“ ციფრებს არ ვასახელებთ. სასარგებლო წესია: ნუ დაელოდებით ბოლო კვირას — თუ უვიზო წელი იწურება, განაცხადი წინასწარ შეიტანეთ, რომ სტატუსში ხარვეზი არ გაჩნდეს.</p>
<h2 id="rezidentoba">საგადასახადო რეზიდენტობა — ცალკე საკითხი</h2>
<p>ბინადრობის მოპოვება ხშირად ერევათ საგადასახადო რეზიდენტობაში, თუმცა ეს სხვადასხვა რამაა. საგადასახადო რეზიდენტი ხდებით, თუ 12 თვეში 183 დღეს ან მეტს ატარებთ ქვეყანაში — სწორედ მაშინ ჩნდება დეკლარირების საკითხი. სანამ ჩვეულებრივი არარეზიდენტი ხართ, ბინადრობა თავისთავად საგადასახადო ტვირთს არ ქმნის.</p>
<p>მაგრამ გახსოვდეთ თქვენი მშობლიური ქვეყნის წესები: ბევრი სახელმწიფო ითხოვს უცხოური ანგარიშებისა და შემოსავლის დეკლარირებას, ხოლო CRS-ის ფარგლებში საქართველო მონაცემებს ათეულობით ქვეყანასთან ცვლის. სანამ დიდ თანხებს გადმოიტანთ, თქვენი ვალდებულებები საგადასახადო კონსულტანტთან დააზუსტეთ — ეს ბინადრობის ცალკე, პარალელური საკითხია.</p>
<h2 id="gagrძeleba">გაგრძელება და მუდმივი ბინადრობა</h2>
<p>პირველი ნებართვა ჩვეულებრივ დროებითია, წლიდან რამდენიმე წლამდე. გაგრძელება წინასწარ სჭირდება — არა ბოლო დღეს, რადგან განხილვა კვირებს გრძელდება და ვადის გადაცილება სტატუსს ანულირებს. გაგრძელებისას ამოწმებენ, რომ საფუძველი ჯერ კიდევ ძალაშია. რამდენიმეწლიანი უწყვეტი კანონიერი ცხოვრების შემდეგ იხსნება გზა მუდმივი ბინადრობისკენ, შემდეგ კი — პირობების დაცვით — ნატურალიზაციისკენ. ეს წლების მარათონია, მაგრამ იწყება სუფთად გაფორმებული პირველი ნებართვით.</p>
<p>ერთი პრაქტიკული რჩევა გაგრძელებაზე: დაისახეთ შეხსენება ვადის ამოწურვამდე ორი-სამი თვით ადრე. ამ დროისთვის შეამოწმეთ, ჯერ კიდევ ძალაშია თუ არა საფუძველი — მოქმედი კონტრაქტი, ბრუნვა, ქონების ფლობა — და საჭიროებისას განაახლეთ ცნობები. თუ საფუძველი შეიცვალა, მაგალითად სამსახური გამოიცვალეთ ან ბიზნესი დახურეთ, გაგრძელებამდე კატეგორიის შეცვლა დაგჭირდებათ, რაც დამატებით დროსა და საბუთებს ითხოვს.</p>
<h2 id="uari">უარის ხშირი მიზეზები</h2>
<p>გამოცდილებით, განაცხადს ხშირად აბრუნებენ არასწორი კატეგორიის, დაუმოწმებელი თარგმანის, ზღვარს დაბალი ქონების ღირებულების ან სუსტი შემოსავლის გამო. უარი იშვიათად მოჰყვება დეტალურ ახსნას.</p>
<ul>
<li>პასპორტი მოქმედი მინიმუმ კიდევ ექვსი თვე;</li>
<li>თარგმანი ქართველი ნოტარიუსით დამოწმებული;</li>
<li>ქონების ღირებულება მიმდინარე ზღვარს აკმაყოფილებს;</li>
<li>შემოსავალი საბუთებით გამყარებული;</li>
<li>კატეგორია რეალურ საფუძველს ემთხვევა.</li>
</ul>
<div class="warn-box">უარი სამუდამო აკრძალვა არ არის. გამოასწორეთ მიზეზი და თავიდან შეიტანეთ ან შეცვალეთ საფუძველი. მაგრამ ყოველი შეტანა მოსაკრებელი და კვირებია, ამიტომ პაკეტი პირველივე ჯერზე სწორად შეკრიბეთ.</div>
<h2 id="ojaxi">ოჯახთან ერთად გადმოსვლა</h2>
<p>როცა ოჯახი გადმოდის, ნებართვა ჩვეულებრივ ერთი ადამიანის გარშემო შენდება: ის იღებს სტატუსს შრომით, ბიზნესით, ინვესტიციით ან ქონებით, ხოლო მეუღლე და შვილები — ოჯახური საფუძვლით. ბავშვებს დასჭირდებათ თარგმნილი და დამოწმებული დაბადების მოწმობები, ზოგჯერ მეორე მშობლის თანხმობა — ეს სახლში, აპოსტილით მოამზადეთ. ცალკე თემაა სკოლა: ბავშვებს აბარებენ ადგილობრივ, საერთაშორისო ან რუსულენოვან სკოლებში, რომელთა ნაწილს ესაჭიროება ბავშვის განათლების თარგმნილი საბუთები. დაგეგმეთ სასწავლო წლის დაწყებამდე.</p>
<p>ცალკე გაითვალისწინეთ ჯანმრთელობის დაზღვევა: ის ბინადრობას ავტომატურად არ ერთვის და ოჯახზე ცალკე ფორმდება. თარგმანი, დამოწმება და სკოლაში ადგილი სამი პარალელური პროცესია, არა ერთი — ამიტომ ადრე დაიწყეთ, რომ ბოლო მომენტში არ დაგროვდეს.</p>
<h2 id="scenarebi">ტიპური სცენარები</h2>
<ul>
<li><strong>ფრილანსერი და დისტანციური.</strong> ჩვეულებრივ ხსნიან ინდ. მეწარმეს მცირე ბიზნესის სტატუსით და მასზე აფუძნებენ შრომით ნებართვას — იხ. <a href="/ge/blog/company-registration-georgia/">კომპანიის რეგისტრაცია</a>.</li>
<li><strong>ინვესტორი და მყიდველი.</strong> მიდიან უძრავი ქონებით ან ინვესტიციით; ყველაფერი შეფასებაზეა დამოკიდებული. თუ ჯერ ქირაობთ, იხ. <a href="/ge/blog/apartment-rental-tbilisi/">ბინის ქირაობა თბილისში</a>.</li>
<li><strong>ოჯახი.</strong> ერთი წევრი იღებს ნებართვას, დანარჩენები — ოჯახური საფუძვლით.</li>
</ul>
<p>ყველა სცენარში ვიწრო ადგილი ერთია: საბუთების თარგმანი, დამოწმება და სწორი შეტანა ქართულად. ამიტომ, სცენარის მიუხედავად, ღირს ერთი ადამიანი, ვინც მთელ გზას ერთად გაივლის თქვენთან — კატეგორიის არჩევიდან თარგმანამდე და მოწმობის აღებამდე; ეს საგრძნობლად ამცირებს უარისა და თავიდან შეტანის რისკს.</p>
""" + cta_ge("განაცხადი ქართულადაა და შეცდომა მოსაკრებელსა და თვეებს ჯდება. სტუმარს ან კლიენტს გავუწევთ თანხლებას და თარგმანს ბინადრობის განაცხადზე.") + """
<div class="sources-block"><p class="sources-title">ოფიციალური წყაროები</p><ul>
<li><a href="https://sda.gov.ge/" rel="noopener noreferrer" target="_blank">სახელმწიფო სერვისების განვითარების სააგენტო (sda.gov.ge)</a></li>
<li><a href="https://psh.gov.ge/" rel="noopener noreferrer" target="_blank">იუსტიციის სახლი (psh.gov.ge)</a></li>
</ul></div>
""",
    "related": [
        ("კერძო გიდი თბილისში", "ინდივიდუალური მარშრუტები ქვეყანაში.", "/ge/private-guide-tbilisi/"),
        ("ყაზბეგი ერთ დღეში", "სამხედრო გზა ერთ დღეში.", "/ge/blog/kazbegi-day-trip-from-tbilisi/"),
        ("გზამკვლევი ექსპატებისთვის", "თბილისში ფეხის მოკიდება.", "/ge/blog/tbilisi-for-expats/"),
    ],
    "faq": [
        ("საჭიროა ნებართვა, თუ უვიზო წელი მაქვს?", "არა, სანამ წელი გაწყობთ. საჭიროა მუშაობის, სწავლის, ბიზნესისა და ხანგრძლივი ყოფნისთვის."),
        ("რა არის ქონების ზღვარი?", "დაახლოებით 100 000 აშშ დოლარი, მაგრამ თანხა და შეფასების წესი იცვლება — შეამოწმეთ sda.gov.ge."),
        ("ნებართვა მუშაობის უფლებას იძლევა?", "შრომითი და ზოგი კატეგორია — კი; სასწავლოსა და ოჯახურს აქვს შეზღუდვები."),
        ("რამდენ ხანში მიიღება გადაწყვეტილება?", "ჩვეულებრივ რამდენიმე კვირა; დაჩქარებული უფრო სწრაფია."),
        ("თუ უარი მივიღე?", "გამოასწორეთ მიზეზი და თავიდან შეიტანეთ, ან შეცვალეთ საფუძველი."),
        ("იჯარა საკმარისია ნებართვისთვის?", "არა. საფუძველია ზღვარს ზემოთ ქონების ფლობა; გრძელვადიანი იჯარა ნებართვის უფლებას არ იძლევა."),
        ("რა ხდება, თუ 183 დღეზე მეტს დავრჩები?", "შესაძლოა საგადასახადო რეზიდენტი გახდეთ — ეს ცალკე საკითხია ბინადრობისგან, დააზუსტეთ კონსულტანტთან."),
        ("როგორ ვაგრძელებ ნებართვას?", "ვადის ამოწურვამდე ორი-სამი თვით ადრე შეიტანეთ — საფუძველი ჯერ კიდევ ძალაში უნდა იყოს."),
    ],
})

ARTICLES.append({
    "lang": "ge", "kind": "post",
    "url": "/ge/blog/document-translation-notary-georgia/", "blog_root": "/ge/blog/",
    "alt": {"ru": "/blog/perevod-i-zaverenie-dokumentov-v-gruzii/",
            "en": "/en/blog/document-translation-notary-georgia/",
            "ge": "/ge/blog/document-translation-notary-georgia/"},
    "title": "ნოტარიული თარგმანი საქართველოში 2026",
    "meta": "როდის სჭირდებათ ნოტარიულად დამოწმებული თარგმანი საქართველოში, აპოსტილი vs ლეგალიზაცია, რომელი საბუთი ითარგმნება ქორწინებისა და ბინადრობისთვის, სად და როგორ სწრაფად.",
    "h1": "დოკუმენტების თარგმანი და ნოტარიული დამოწმება საქართველოში",
    "crumb": "დოკუმენტების თარგმანი",
    "label": "გზამკვლევი · 7 წთ",
    "image": "/images/blog/perevod-dokumentov-gruzia.webp",
    "meta_bits": ["გზამკვლევი", "ცხოვრება საქართველოში", "დოკუმენტები"],
    "toc": [("rodis", "როდის სჭირდება"), ("apostili", "აპოსტილი თუ ლეგალიზაცია"),
            ("romeli", "რომელი საბუთი ითარგმნება"), ("paketebi", "პაკეტები პროცედურებით"),
            ("vada", "ცნობების მოქმედების ვადა"), ("diplomi", "დიპლომი და მინდობილობა"),
            ("prisyaga", "ნაფიცი თუ ნოტარიული"), ("shemowmeba", "შემოწმება შეტანამდე"),
            ("ghirebuleba", "ღირებულება და ვადა"), ("eleqtronuli", "ელექტრონული აპოსტილი"),
            ("sad", "სად და როგორ სწრაფად"), ("shecdomebi", "ხშირი შეცდომები")],
    "lead": "<strong>საქართველოში თითქმის ნებისმიერი ოფიციალური პროცედურა</strong> — ქორწინება, ბინადრობა, ბანკი, სწავლა, გარიგება — მოითხოვს, რომ უცხოური საბუთი ითარგმნოს ქართულად და დამოწმდეს ნოტარიულად. ხშირად საჭიროა აპოსტილი ან ლეგალიზაცია გამცემი ქვეყნიდან. აი, რა უნდა გააკეთოთ და რა თანმიმდევრობით.",
    "body": """
<h2 id="rodis">როდის სჭირდება დამოწმებული თარგმანი</h2>
<p>უბრალო თარგმანი უწყებას ან ბანკს არ ჰყოფნის: იღებენ თარგმანს, რომლის მთარგმნელის ხელმოწერაც ქართველმა ნოტარიუსმა დაამოწმა. ეს დაგჭირდებათ ქორწინებისთვის (პასპორტი), <a href="/ge/blog/residence-permit-georgia/">ბინადრობისთვის</a>, ზოგი საბანკო შემთხვევისთვის, დიპლომის აღიარებისთვის, მინდობილობებისა და გარიგებებისთვის.</p>
<p>მარტივი წესი: სანამ დროსა და ფულს დახარჯავთ, დააზუსტეთ, რომელი უწყება რას ითხოვს — თარგმანს, ნოტარიულ დამოწმებას თუ აპოსტილსაც. ხშირად სამივე ერთად საჭიროა, მაგრამ ზოგჯერ — მხოლოდ ერთი. ეს დაზუსტება ერთი ზარია, ხოლო შეცდომა — დაკარგული დღე ან თვე.</p>
<h2 id="apostili">აპოსტილი თუ ლეგალიზაცია</h2>
<p>სწორედ აქ კარგავენ ყველაზე მეტ დროს, ამიტომ დეტალურად.</p>
<ul>
<li>თუ თქვენი ქვეყანა და საქართველო <strong>ჰააგის კონვენციაში</strong> არიან, საბუთი მოწმდება <strong>აპოსტილით</strong> გამცემ ქვეყანაში — ეს საკმარისია.</li>
<li>თუ არა — საჭიროა <strong>საკონსულო ლეგალიზაცია</strong>, უფრო გრძელი ჯაჭვი.</li>
</ul>
<div class="warn-box">მთავარი: უცხოურ საბუთზე აპოსტილი კეთდება სახლში, გამგზავრებამდე — საქართველოში მას ვერ აიღებთ. ეს ყველაზე ხშირი და მტკივნეული შეცდომაა. ქართულ საბუთზე აპოსტილი იუსტიციის სახლში კეთდება.</div>
<p>როგორ გავიგოთ, რომელი გზაა თქვენი? შეამოწმეთ, არის თუ არა თქვენი ქვეყანა ჰააგის კონვენციის მონაწილე — ეს ღია ინფორმაციაა და ერთ წუთში მოწმდება. თუ კი, საკმარისია აპოსტილი; თუ არა, მოგიწევთ საკონსულო ლეგალიზაცია, რომელიც რამდენიმე უწყებას გადის და კვირებს ითხოვს. ორივე შემთხვევაში ჯაჭვი გამცემ ქვეყანაში იწყება, ამიტომ სჯობს ის ჯერ კიდევ გამგზავრებამდე დაასრულოთ, ვიდრე თბილისში აღმოაჩინოთ, რომ საბუთი დაუმოწმებელია.</p>
<h2 id="romeli">ყველაზე ხშირად თარგმნადი საბუთები</h2>
<p>პასპორტი (ქორწინებისა და ბინადრობისთვის), დაბადების/ქორწინების/განქორწინების მოწმობა, ნასამართლობის ცნობა, დიპლომები, შემოსავლის ცნობები, მინდობილობები, მართვის მოწმობა, ქონების საბუთები. ქორწინებისთვის მთავარია პასპორტი — იხ. <a href="/ge/blog/how-to-get-married-in-georgia/">როგორ დავქორწინდეთ საქართველოში</a>.</p>
<p>ცალკე უნდა აღინიშნოს ცნობები, რომლებიც არა უცხოეთში, არამედ თავად საქართველოში გამოიყენება ან პირიქით — უცხოეთში წარსადგენად ქართული ცნობა ითარგმნება უცხო ენაზე და მასზე აპოსტილი იუსტიციის სახლში იდება. ორივე მიმართულებით პრინციპი ერთია: ჯერ ორიგინალი, შემდეგ თარგმანი, შემდეგ დამოწმება ან აპოსტილი — თანმიმდევრობის აღრევა ყველაზე ხშირი შეცდომაა.</p>
<div class="info-box">ერთი პრინციპი კვირებს ზოგავს: დააფიქსირეთ სახელის ერთი ტრანსლიტერაცია და შეინარჩუნეთ ყველა თარგმანში. თუ პასპორტში, ცნობასა და თარგმანში სახელი სხვადასხვაგვარადაა, სისტემა „სხვა“ ადამიანს ხედავს.</div>
<h2 id="paketebi">პაკეტები პროცედურებით</h2>
<ul>
<li><strong>ქორწინება.</strong> ორივე მომავალი მეუღლის პასპორტი ნოტარიული თარგმანით; ზოგჯერ ცნობა ოჯახური მდგომარეობის შესახებ აპოსტილით. ცერემონიისთვის იხ. <a href="/ge/interpreter-and-support-georgia/">თარჯიმანი და თანხლება</a>.</li>
<li><strong>ბინადრობა.</strong> პასპორტი თარგმანით, საფუძვლისა და შემოსავლის დადასტურება — იხ. <a href="/ge/blog/residence-permit-georgia/">ბინადრობის ნებართვა</a>.</li>
<li><strong>ბანკი და ბიზნესი.</strong> პასპორტი, ზოგჯერ მისამართისა და შემოსავლის დადასტურება; კომპანიისთვის — სადამფუძნებლო საბუთები. იხ. <a href="/ge/blog/open-bank-account-georgia/">ანგარიშის გახსნა</a>.</li>
</ul>
<p>ამ სამი პაკეტის მიღმა ლოგიკა ერთია: ჯერ იგებთ, კონკრეტულად რომელ საბუთს ითხოვს უწყება, შემდეგ ამოწმებთ, სჭირდება თუ არა აპოსტილი, და მხოლოდ ბოლოს თარგმნით. თუ თანმიმდევრობას დაიცავთ, თავიდან აიცილებთ განმეორებით ვიზიტსა და ხელახლა გადახდილ მოსაკრებელს. ცალკე გაითვალისწინეთ, რომ ზოგ პროცედურას სჭირდება არა მხოლოდ პასპორტი, არამედ თანმხლები ცნობაც — მაგალითად, ოჯახური მდგომარეობის ან შემოსავლის — და თითოეული მათგანი დამოუკიდებლად გადის თარგმანისა და დამოწმების იმავე ჯაჭვს.</p>
<h2 id="vada">ცნობების მოქმედების ვადა</h2>
<p>ბევრ საბუთს აქვს „ვარგისობის ვადა“, და ეს გეგმებს უფრო ხშირად შლის, ვიდრე ჰგონიათ. ნასამართლობისა და ოჯახური მდგომარეობის ცნობა ჩვეულებრივ მიიღება მხოლოდ გაცემიდან შეზღუდულ პერიოდში, ამიტომ მათი „მომავლისთვის“ შეკვეთა უაზროა. აპოსტილი ახალ ცნობაზე იდება, არა შარშანდელზე. ლოგიკა: ჯერ დააზუსტეთ საჭირო ვადა კონკრეტული პროცედურისთვის, შემდეგ შეუკვეთეთ ცნობა და აპოსტილი, და მხოლოდ ბოლოს ჩამოდით და თარგმნეთ.</p>
<h2 id="diplomi">დიპლომის აღიარება და მინდობილობა</h2>
<p>პროფესიით სამუშაოდ ან ჩასაბარებლად დიპლომი ითარგმნება და მოწმდება, ხოლო ზოგი პროფესიისთვის ცალკე გადიან კვალიფიკაციის აღიარების პროცედურას — ეს თარგმანი არ არის და მეტ დროს მოითხოვს. საზღვარგარეთ გაცემული მინდობილობაც საჭიროებს თარგმანსა და ხშირად აპოსტილს; ხოლო თუ მინდობილობა უკვე საქართველოში კეთდება საზღვარგარეთ გამოსაყენებლად, მას ადგილობრივი ნოტარიუსი აფორმებს, აპოსტილს კი იუსტიციის სახლში ასვამენ. აქ განსაკუთრებით მნიშვნელოვანია ფორმულირების სიზუსტე.</p>
<p>ცალკე ხაზი უნდა გაესვას ვადებს: კვალიფიკაციის აღიარება, დიპლომის ვერიფიკაცია ან სპეციალურ რეესტრში შეტანა ზოგჯერ კვირებს ან თვეებს ითხოვს, ამიტომ მას სჯობს ყველაზე ადრე შეუდგეთ — თარგმანი და აპოსტილი ამ ფონზე სწრაფი ეტაპია, რომელსაც ბოლოს ასრულებთ.</p>
<h2 id="prisyaga">ნაფიცი თუ ნოტარიული თარგმანი</h2>
<p>ხშირი კითხვა: საჭიროა თუ არა „ნაფიცი მთარგმნელი“? საქართველოში ნაფიცი მთარგმნელის ინსტიტუტი ჩვეული სახით არ გამოიყენება — იურიდიულ ძალას ანიჭებს არა მთარგმნელის სტატუსი, არამედ მისი ხელმოწერის ნოტარიული დამოწმება. ამიტომ ეძებეთ ბიურო, რომელიც ნოტარიუსთან ერთად მუშაობს და მზა დამოწმებულ თარგმანს გაძლევთ. იგივე წესი ხსნის გაუგებრობას: სხვა ქვეყნის ნოტარიუსით დამოწმებული თარგმანი აქ არ გამოდგება.</p>
<h2 id="shemowmeba">როგორ შევამოწმოთ თარგმანი შეტანამდე</h2>
<p>სანამ თარგმანს უწყებაში წაიღებთ, დაუთმეთ ხუთი წუთი შემოწმებას. გადაამოწმეთ მთავარი: სახელი და გვარი პასპორტს ემთხვევა ასოდან ასომდე; ყველა თარიღი და ნომერი გადატანილია შეცდომის გარეშე; ნათარგმნია საჭირო მოცულობა; არის ნოტარიული აღნიშვნა და ხელმოწერა. ცალკე დახედეთ ტოპონიმებსა და ორგანიზაციების სახელებს — ისინი ხშირად სხვადასხვაგვარად ითარგმნება. ეჭვის შემთხვევაში, შეასწორეთ შეტანამდე: თარგმანის გადაკეთება იაფია, ვიდრე მოსაკრებლის ხელახლა გადახდა.</p>
<p>განსაკუთრებით ხშირად ცდებიან ციფრებში — თარიღი, საბუთის ნომერი, თანხა: ერთი შეცვლილი ციფრი და უწყება საბუთს „არასწორად“ თვლის და უკან აბრუნებს. ამიტომ ბოლო შემოწმება ორიგინალის გვერდით გააკეთეთ, ველ-ველად და არა მეხსიერებით. თუ ბიურომ ელექტრონული ვერსია გამოგიგზავნათ, დაბეჭდვამდე სწორედ ეს ვერსია გადაამოწმეთ — ბეჭდვის შემდეგ შესწორება ნიშნავს ხელახლა დამოწმებას.</p>
<h2 id="ghirebuleba">ღირებულება და ვადა</h2>
<p>ღირებულება ენაზე, მოცულობასა და სისწრაფეზეა დამოკიდებული; ნოტარიული დამოწმება თარგმანისგან ცალკე ფასდება. ნოტარიუსების მიმდინარე ტარიფებს ნოტარიუსთა პალატა აქვეყნებს — „მუდმივ“ ციფრებს არ ვასახელებთ, მაგრამ მარტივი ერთგვერდიანი საბუთი ჩვეულებრივ იაფია. გარიგების ან საქმის მთელი პაკეტი უფრო ძვირი და დროში გაწელილია, ამიტომ ჯობია მთელი სია ერთდროულად მიიტანოთ, ვიდრე თითო-თითოდ.</p>
<h2 id="eleqtronuli">ელექტრონული აპოსტილი და ციფრული საბუთები</h2>
<p>სულ უფრო მეტი ქვეყანა გასცემს აპოსტილს ელექტრონულად (e-Apostille) — QR-კოდითა და ონლაინ რეესტრში გადამოწმებით. ასეთი აპოსტილი ქაღალდისაზე მოსახერხებელია, მაგრამ წინასწარ დააზუსტეთ, იღებს თუ არა კონკრეტული ქართული უწყება ზუსტად თქვენი ქვეყნის ელექტრონულ ფორმას — პრაქტიკა ჯერ სწორდება. იგივე ეხება ციფრულ ამონაწერებს: ქართული საბუთი სულ უფრო ხშირად ელექტრონულადაც არსებობს, მაგრამ საზღვარგარეთ წარსადგენად ზოგჯერ მაინც სჭირდება ქაღალდის ასლი აპოსტილით.</p>
<h2 id="sad">სად და როგორ სწრაფად</h2>
<p>თარგმანის ბიუროები <a href="/ge/blog/public-service-hall-georgia/">იუსტიციის სახლთან</a> ახლოსაა და ხშირად თავადვე აწყობენ ნოტარიულ დამოწმებას. მარტივი საბუთი ერთ დღეში, ზოგჯერ ერთ საათში ითარგმნება; გარიგების პაკეტი — უფრო დიდხანს. ბიუროს არჩევისას მხოლოდ ფასს ნუ უყურებთ — სჯობს ისეთი, რომელიც ნოტარიუსთან ერთად მუშაობს.</p>
<p>დროის დაზოგვის ერთი პრაქტიკული რჩევა: მთელი პაკეტი ერთდროულად მიიტანეთ ბიუროში, ვიდრე თითო საბუთი სხვადასხვა დღეს — ასე ნოტარიულ დამოწმებასაც ერთ ჯერზე აწყობენ და ნაკლები ვიზიტი დაგჭირდებათ. თუ ვადა გიწვავთ, წინასწარ ჰკითხეთ ბიუროს სასწრაფო თარგმანის შესაძლებლობა — ის ხშირად დამატებით ფასად ხელმისაწვდომია, მაგრამ ნოტარიუსის სამუშაო საათებზეა დამოკიდებული, ამიტომ დილით მისვლა სჯობს საღამოს.</p>
<h2 id="shecdomebi">ხშირი შეცდომები</h2>
<ul>
<li>ჩამოსვლა აპოსტილის გარეშე (უცხოურ საბუთზე მას აქ ვერ აიღებთ);</li>
<li>დამოწმება არა-ქართველი ნოტარიუსით;</li>
<li>პასპორტის მხოლოდ ნაწილის თარგმნა;</li>
<li>სახელის განსხვავებული ჩაწერა სხვადასხვა საბუთში.</li>
</ul>
""" + cta_ge("შევკრებთ პაკეტს, ვთარგმნით, დავამოწმებთ და წარვადგენთ — ბიუროს, ნოტარიუსსა და სარკმელს შორის სირბილის გარეშე.") + """
<div class="sources-block"><p class="sources-title">ოფიციალური წყაროები</p><ul>
<li><a href="https://napr.gov.ge/" rel="noopener noreferrer" target="_blank">საჯარო რეესტრის ეროვნული სააგენტო (napr.gov.ge)</a></li>
<li><a href="https://psh.gov.ge/" rel="noopener noreferrer" target="_blank">იუსტიციის სახლი (psh.gov.ge)</a></li>
</ul></div>
""",
    "related": [
        ("კერძო გიდი თბილისში", "ქალაქის დათვალიერება ადგილობრივთან.", "/ge/private-guide-tbilisi/"),
        ("კახეთის ღვინის ტური", "ღვინის მხარე.", "/ge/blog/kakheti-wine-tour/"),
        ("გზამკვლევი ექსპატებისთვის", "თბილისში ფეხის მოკიდება.", "/ge/blog/tbilisi-for-expats/"),
    ],
    "faq": [
        ("საჭიროა ნოტარიული პასპორტის თარგმანი ქორწინებისთვის?", "დიახ, ეს მთავარი საბუთია."),
        ("რა არის აპოსტილი და სად კეთდება?", "გამარტივებული დამოწმება ჰააგის ქვეყნებისთვის; უცხოურ საბუთზე კეთდება გამცემ ქვეყანაში, ჩამოსვლამდე."),
        ("შესაძლებელია ერთ დღეში დამოწმება?", "მარტივი საბუთი — ხშირად კი."),
        ("მთელი პასპორტი თუ ერთი გვერდი?", "ჩვეულებრივ მონაცემების გვერდი; დააზუსტეთ პროცედურისთვის."),
        ("აპოსტილი საქართველოში კეთდება?", "ქართულ საბუთებზე — კი; უცხოურზე — მხოლოდ გამცემ ქვეყანაში."),
        ("ინგლისურ საბუთსაც თარგმნიან?", "ჩვეულებრივ კი — უწყებები ქართულს იღებენ, ამიტომ ინგლისურ საბუთსაც თარგმნიან და ამოწმებენ."),
        ("ელექტრონული აპოსტილი გამოდგება?", "ხშირად კი, მაგრამ წინასწარ დააზუსტეთ, იღებს თუ არა კონკრეტული ქართული უწყება ზუსტად თქვენი ქვეყნის e-Apostille-ს — პრაქტიკა ჯერ სწორდება."),
        ("რამდენ ხანს არის ცნობა აქტუალური?", "ნასამართლობისა და ოჯახური მდგომარეობის ცნობას შეზღუდული ვადა აქვს — შეუკვეთეთ პროცედურის ახლოს, არა წინასწარ."),
    ],
})

ARTICLES.append({
    "lang": "ge", "kind": "post",
    "url": "/ge/blog/company-registration-georgia/", "blog_root": "/ge/blog/",
    "alt": {"ru": "/blog/registratsiya-kompanii-v-gruzii/",
            "en": "/en/blog/company-registration-georgia/",
            "ge": "/ge/blog/company-registration-georgia/"},
    "title": "კომპანიისა და ინდ. მეწარმის რეგისტრაცია 2026",
    "meta": "როგორ გავხსნათ ინდ. მეწარმე ან შპს საქართველოში 2026: ფორმები, მცირე ბიზნესის 1% სტატუსი, რეგისტრაცია იუსტიციის სახლში, საბანკო ანგარიში, გადასახადები.",
    "h1": "კომპანიის ან ინდ. მეწარმის რეგისტრაცია საქართველოში: 2026",
    "crumb": "კომპანიის რეგისტრაცია",
    "label": "გზამკვლევი · 8 წთ",
    "image": "/images/blog/registratsiya-kompanii-gruzia.webp",
    "meta_bits": ["გზამკვლევი", "ბიზნესი საქართველოში", "ინდ.მეწარმე / შპს"],
    "toc": [("forma", "რომელი ფორმა"), ("statusi", "მცირე ბიზნესის სტატუსი 1%"),
            ("dgg", "დღგ და როდის ჩნდება"), ("sabutebi", "საბუთები"), ("nabijebi", "ეტაპობრივად"),
            ("gadasaxadi", "გადასახადი და ანგარიშგება"), ("gadaxda", "როგორ გადავიხადოთ"),
            ("dasakmeba", "თანამშრომლების აყვანა"), ("daxurva", "შეჩერება და დახურვა"),
            ("specrezhimi", "IT-სტატუსი და თავისუფალი ზონები"), ("shenaxvა", "რა ღირს ინდ. მეწარმის შენახვა"),
            ("shecdomebi", "ხშირი შეცდომები")],
    "lead": "<strong>საქართველოში საქმის დაფუძნება სწრაფია</strong>: ინდ. მეწარმე ან შპს იუსტიციის სახლში ჩვეულებრივ ერთ სამუშაო დღეში რეგისტრირდება, უცხოელი კი შეიძლება ერთადერთი მფლობელი იყოს. ფრილანსერებისა და მცირე ბრუნვისთვის არსებობს ხელსაყრელი <strong>მცირე ბიზნესის სტატუსი</strong> ბრუნვის 1%-ით.",
    "body": """
<h2 id="forma">რომელი ფორმა ავირჩიოთ</h2>
<ul>
<li><strong>ინდივიდუალური მეწარმე</strong> — უმარტივესი; ფრილანსერებისა და მცირე ბიზნესისთვის; აქვს 1%-იანი სტატუსის უფლება.</li>
<li><strong>შპს</strong> — პარტნიორებისთვის, თანამშრომლებისთვის ან შეზღუდული პასუხისმგებლობისთვის.</li>
<li><strong>სპეციალური რეჟიმები</strong> — თავისუფალი ინდუსტრიული ზონები, IT-სტატუსი — კონკრეტული მოდელებისთვის.</li>
</ul>
<p>გადმოსახლებული თვითდასაქმებულების უმეტესობისთვის საწყისი წერტილია <strong>ინდ. მეწარმე პლუს მცირე ბიზნესის სტატუსი</strong>. შპს მაშინ, როცა არის პარტნიორები, თანამშრომლები ან პირადი აქტივების დაცვის საჭიროება.</p>
<p>არჩევანი ფორმაზე უკუსვლით არ სჯობს: ინდ. მეწარმედან შპს-ზე გადასვლა შესაძლებელია, მაგრამ ეს ცალკე რეგისტრაციაა ახალი ანგარიშითა და ხელახალი საბუთებით, ამიტომ ჯობია თავიდანვე რეალურ გეგმას მოარგოთ. მარტივი კითხვა გეხმარებათ: მუშაობთ მარტო და უცხოურ კლიენტებს ემსახურებით — ინდ. მეწარმე; გყავთ პარტნიორი, გინდათ ინვესტიცია მოიზიდოთ ან პირადი ქონება საქმის რისკებისგან გამიჯნოთ — შპს. შუალედური შემთხვევებიც არსებობს, სადაც ერთსაათიანი კონსულტაცია თვეებს ზოგავს.</p>
<h2 id="statusi">მცირე ბიზნესის სტატუსი (1%)</h2>
<p>ინდ. მეწარმეს, რომლის წლიური ბრუნვაც ზღვარს ქვემოთაა (ორიენტირი — 500 000 ლარი; დააზუსტეთ rs.ge-ზე), შეუძლია ჰქონდეს ეს სტატუსი და გადაიხადოს <strong>ბრუნვის 1%</strong> 20%-იანი საშემოსავლოს ნაცვლად. სწორედ ეს ხდის ქვეყანას პოპულარულს ფრილანსერებში.</p>
<div class="info-box">მცირე ბიზნესის სტატუსი და ინდ. მეწარმის გახსნა — ეს არის პროცედურა საგადასახადოში (rs.ge), ბანკი კი მხოლოდ ანგარიშს ხსნის. ეს ორი სხვადასხვა ნაბიჯია.</div>
<p>სტატუსს აქვს ნიუანსები. ის ითვლება ბრუნვაზე და არა მოგებაზე: მთელი შემოსავალი მნიშვნელოვანია, არა ის, რაც ხარჯების შემდეგ დარჩა. ზოგი საქმიანობა შეღავათს არ ექვემდებარება, ამიტომ თქვენი კონკრეტული საქმე წინასწარ გადაამოწმეთ. და სტატუსი ავტომატურად არ ენიჭება რეგისტრაციისას — ის ცალკე უნდა მოითხოვოთ, თორემ მთელი წელი 20%-ს გადაიხდით.</p>
<h2 id="dgg">დღგ და როდის ჩნდება</h2>
<p>ცალკე თემა, რომელსაც ახალბედები ვერ ამჩნევენ: დღგ. ზღვარზე მეტი ბრუნვისას ჩნდება დღგ-ს გადამხდელად რეგისტრაციის ვალდებულება — და ეს ცალკე ზღვარია, მცირე ბიზნესის ზღვარს არ უდრის. სანამ პატარა ფრილანსერი ხართ, ეს არააქტუალურია, მაგრამ ბრუნვის ზრდისას დღგ შეიძლება შეუმჩნევლად „ჩაირთოს“. მიმდინარე ზღვრები იხ. rs.ge-ზე.</p>
<h2 id="sabutebi">საბუთები</h2>
<p>პასპორტი (და თარგმანი საჭიროებისას); იურიდიული მისამართი საქართველოში (იჯარა ან მესაკუთრის თანხმობა); განაცხადი; შპს-სთვის — წესდება და პარტნიორების მონაცემები. მისამართს ამოწმებენ.</p>
<p>იურიდიულ მისამართზე ცალკე უნდა შევჩერდეთ, რადგან სწორედ აქ ჩერდება რეგისტრაცია ყველაზე ხშირად. მისამართი რეალური უნდა იყოს: ან თქვენი საკუთრება, ან იჯარის ხელშეკრულება, ან მესაკუთრის ნოტარიული თანხმობა თქვენს მისამართზე რეგისტრაციაზე. „ვირტუალური“ მისამართი, რომელსაც ზოგი სთავაზობს, რისკია — თუ მესაკუთრე თანხმობას გამოიხმობს, კომპანია მისამართის გარეშე რჩება. თუ ჯერ ბინა არ გაქვთ, ეს პირველი ნაბიჯია რეგისტრაციამდე და არა მის შემდეგ.</p>
<h2 id="nabijebi">ეტაპობრივად</h2>
<ol>
<li>აირჩიეთ ფორმა და სახელი.</li>
<li>მოამზადეთ მისამართი და საბუთები.</li>
<li>შეიტანეთ <a href="/ge/blog/public-service-hall-georgia/">იუსტიციის სახლში</a> — ჩვეულებრივ იმავე დღეს.</li>
<li>აიღეთ ამონაწერი და საგადასახადო ნომერი.</li>
<li>დარეგისტრირდით rs.ge-ზე; საჭიროებისას მოითხოვეთ მცირე ბიზნესის სტატუსი.</li>
<li>გახსენით ბიზნეს-ანგარიში — იხ. <a href="/ge/blog/open-bank-account-georgia/">ანგარიშის გახსნა</a>.</li>
</ol>
<p>რეგისტრაცია პირადი დასწრებით ერთ დღეში სრულდება, მაგრამ თუ ქვეყანაში ჯერ არ ხართ, შესაძლებელია მინდობილობით — სანდო პირი თქვენს ნაცვლად შეიტანს საბუთებს. მინდობილობა უცხოეთში ფორმდება, ითარგმნება და აპოსტილდება — იხ. <a href="/ge/blog/document-translation-notary-georgia/">საბუთების თარგმანი და დამოწმება</a>. ეს მოსახერხებელია, თუ საქმის დაწყება ჩამოსვლამდე გინდათ, თუმცა ბანკის ანგარიშს ხშირად მაინც პირადად ხსნიან უსაფრთხოების შემოწმების გამო.</p>
<h2 id="gadasaxadi">გადასახადი და ანგარიშგება</h2>
<div class="price-table-wrap"><table class="price-table">
<thead><tr><th>ფორმა</th><th>გადასახადი</th></tr></thead>
<tbody>
<tr><td>ინდ. მეწარმე, სტატუსის გარეშე</td><td>20% საშემოსავლო</td></tr>
<tr><td>ინდ. მეწარმე, მცირე ბიზნესი</td><td>ბრუნვის 1% (ზღვარს ქვემოთ)</td></tr>
<tr><td>შპს</td><td>15% განაწილებულ მოგებაზე (დივიდენდზე)</td></tr>
</tbody></table></div>
<p>ბრუნვის ყოველთვიური დეკლარაცია იგზავნება rs.ge-ზე. მცირე ინდ. მეწარმის აღრიცხვას ხშირად თავად აწარმოებენ; თანამშრომლებთან ან დღგ-სთან — ბუღალტერთან, რომლის მომსახურებაც საქართველოში ძვირი არ არის და სიმშვიდით ანაზღაურდება. მთავარია პირადი და სამეწარმეო ხარჯები სხვადასხვა ანგარიშზე გქონდეთ — ეს ამარტივებს დეკლარაციასაც და ბანკთან საუბარსაც სახსრების წყაროს შემოწმებისას.</p>
<p>ცალკე პრაქტიკული საკითხი უცხოური კლიენტებისთვის — ვალუტა. შემოსავალი ხშირად დოლარსა თუ ევროში შემოდის, გადასახადი კი ლარში იხდება, ამიტომ ბრუნვა ჩარიცხვის დღის კურსით ითვლება. ბანკს აქვს კონვერტაციის საკომისიო, კურსი კი მერყეობს — ეს არ ცვლის 1%-იან განაკვეთს, მაგრამ გავლენას ახდენს იმაზე, რამდენი დაგრჩებათ ხელში. ბევრი ინდ. მეწარმე ხსნის მულტისავალუტო ანგარიშს, რომ თავად აირჩიოს კონვერტაციის მომენტი და არ დაკარგოს კურსზე.</p>
<h2 id="gadaxda">როგორ გადავიხადოთ გადასახადი — ეტაპობრივად</h2>
<ol>
<li>თვის განმავლობაში აღრიცხეთ ანგარიშზე ჩარიცხული მთელი შემოსავალი.</li>
<li>მომდევნო თვის დადგენილ რიცხვამდე შეიტანეთ დეკლარაცია rs.ge-ზე.</li>
<li>გადაიხადეთ გადასახადი — ბრუნვის 1% სტატუსით — იმავე პორტალიდან.</li>
<li>შეინახეთ გადახდის დადასტურებები; ბანკმა შეიძლება მოითხოვოს.</li>
</ol>
<p>თვის გამოტოვება ჯარიმა და საურავია, ამიტომ დეკლარაცია კალენდარში განმეორებად დავალებად ჩადეთ.</p>
<p>უცხოური კლიენტებისთვის ცალკე გახსოვდეთ ინვოისები და ხელშეკრულებები: 1%-ს ბრუნვაზე იხდით, მაგრამ ბანკმა და საგადასახადომ შეიძლება მოითხოვონ დადასტურება, საიდან შემოვიდა თანხა. ამიტომ თითოეულ ჩარიცხვას შესაბამისი ინვოისი ან კონტრაქტი უნდა ერგებოდეს — ეს არა ბიუროკრატია, არამედ დაცვა კითხვებისგან სახსრების წყაროზე. ციფრული სერვისების ფრილანსერს ეს განსაკუთრებით ეხება, სადაც კლიენტი შორსაა და გადახდა პლატფორმიდან მოდის — შენახული მიმოწერაც კი გამოგადგებათ დადასტურებად.</p>
<h2 id="dasakmeba">თანამშრომლების აყვანა</h2>
<p>როგორც კი თანამშრომელს აიყვანთ, ემატება სახელფასო ანგარიშგება: ხელფასიდან იკავებენ საშემოსავლოს, არის სავალდებულო საპენსიო შენატანები, და ეს ყოველთვიურად დეკლარირდება. მარტოხელა ინდ. მეწარმეს ეს არ აქვს, მაგრამ პირველივე თანამშრომელი აღრიცხვას ართულებს — აქ თითქმის ყოველთვის ბუღალტერია საჭირო.</p>
<h2 id="daxurva">შეჩერება და დახურვა</h2>
<p>გეგმები იცვლება. სანამ ინდ. მეწარმე არსებობს, დეკლარაციის შეტანის ვალდებულება რჩება — ნულოვანი ბრუნვისასაც „ნულოვანი“ დეკლარაცია უნდა შეიტანოთ, თორემ ჯარიმები გროვდება. ამიტომ თუ საქმიანობა შეწყდა, ინდ. მეწარმე ჯობია ოფიციალურად დახუროთ. დახურვა საგადასახადოსა და რეესტრში გადის; ვალები ქვეყნიდან წასვლამდე მოაგვარეთ.</p>
<h2 id="specrezhimi">IT-სტატუსი და თავისუფალი ზონები</h2>
<p>ზოგი მოდელისთვის არსებობს სპეციალური რეჟიმები. IT-კომპანიებმა შეიძლება მოიპოვონ „საერთაშორისო კომპანიის“ სტატუსი ან ვირტუალური IT-ზონის რეჟიმი შემცირებული განაკვეთებით. თავისუფალი ინდუსტრიული ზონები (FIZ) შეღავათებს აძლევს წარმოებასა და ვაჭრობას ზონის შიგნით. ტიპური ფრილანსერისთვის ეს ზედმეტია — მას ინდ. მეწარმე 1%-ით ჰყოფნის. მაგრამ თუ პროდუქტული IT-კომპანია გყავთ გუნდით, სპეცრეჟიმი წინასწარ გათვალეთ, და არა უკუსვლით.</p>
<h2 id="shenaxvა">რა ღირს ინდ. მეწარმის შენახვა</h2>
<p>ინდ. მეწარმის გახსნა იაფია, მაგრამ მას აქვს რეგულარული ხარჯები, რომლებიც თავიდანვე უნდა გაითვალისწინოთ. ჯერ ერთი, გადასახადი — ბრუნვის 1% მცირე ბიზნესის სტატუსით. მეორე, საბანკო მომსახურება: ანგარიშის წარმოება, გადარიცხვის, განაღდებისა და კონვერტაციის საკომისიოები. მესამე, ბუღალტერია, თუ თავად არ აწარმოებთ; მარტოხელასთვის ეს მოკრძალებული თანხაა, მაგრამ არსებობს. პლუს შესაძლო ხარჯი იურიდიულ მისამართზე, თუ საკუთარი არ გაქვთ. ეს ყველაფერი მაინც ხდის საქართველოს ერთ-ერთ ყველაზე ხელსაყრელ იურისდიქციად ფრილანსერისთვის, მაგრამ „1% და მეტი არაფერი“ გამარტივებაა: რეალური ტვირთი დათვალეთ როგორც გადასახადი პლუს მომსახურება პლუს აღრიცხვა. მაშინ მეორე-მესამე თვეს უსიამოვნო სიურპრიზი არ გექნებათ.</p>
<h2 id="shecdomebi">ხშირი შეცდომები</h2>
<ul>
<li>შპს-ის დაფუძნება იქ, სადაც ინდ. მეწარმე იკმარებდა;</li>
<li>სტატუსის მოთხოვნის დავიწყება და წელიწადში 20%-ის გადახდა;</li>
<li>რეალური მისამართის მოთხოვნის შეუფასებლობა;</li>
<li>ყოველთვიური დეკლარაციის გამოტოვება და ჯარიმა.</li>
</ul>
""" + cta_ge("გავიყვანთ რეგისტრაციაში, საგადასახადო პორტალსა და ანგარიშის გახსნაში და ვთარგმნით ბანკის გასაუბრებაზე — პირველივე ჯერზე.") + """
<div class="sources-block"><p class="sources-title">ოფიციალური წყაროები</p><ul>
<li><a href="https://rs.ge/" rel="noopener noreferrer" target="_blank">შემოსავლების სამსახური (rs.ge)</a></li>
<li><a href="https://napr.gov.ge/" rel="noopener noreferrer" target="_blank">მეწარმეთა რეესტრი (napr.gov.ge)</a></li>
</ul></div>
""",
    "related": [
        ("კერძო გიდი თბილისში", "ქვეყნის დათვალიერება დასვენების დღეს.", "/ge/private-guide-tbilisi/"),
        ("ციფრული მომთაბარე თბილისში", "თბილისიდან მუშაობა.", "/ge/blog/digital-nomad-tbilisi/"),
        ("გზამკვლევი ექსპატებისთვის", "ფეხის მოკიდება.", "/ge/blog/tbilisi-for-expats/"),
    ],
    "faq": [
        ("შეუძლია უცხოელს ინდ. მეწარმის ან შპს-ის გახსნა?", "დიახ, ერთადერთი მფლობელის სახითაც."),
        ("რას იძლევა 1%-იანი სტატუსი?", "ბრუნვის 1%-ს 20% საშემოსავლოს ნაცვლად — ზღვარს ქვემოთ."),
        ("რამდენ ხანს სჭირდება რეგისტრაცია?", "ჩვეულებრივ ერთი სამუშაო დღე; დაჩქარებით უფრო სწრაფად."),
        ("საჭიროა რეალური მისამართი?", "დიახ, მას ამოწმებენ."),
        ("რა გადასახადი აქვს შპს-ს?", "15% განაწილებულ მოგებაზე — დივიდენდზე."),
        ("საჭიროა ქართული ანგარიში ინდ. მეწარმისთვის?", "მოსახერხებელია მუშაობისა და გადასახადისთვის, მაგრამ რეგისტრაცია და ანგარიშის გახსნა ცალკე ნაბიჯებია."),
        ("როგორ ვადასტურებ შემოსავლის წყაროს?", "შეინახეთ ინვოისები და ხელშეკრულებები თითო ჩარიცხვაზე — ბანკმა ან საგადასახადომ შეიძლება მოითხოვოს."),
        ("რა ხდება, თუ ბრუნვა ზღვარს გადააჭარბებს?", "1%-იანი სტატუსი უქმდება და ჩვეულებრივი განაკვეთი გამოიყენება; შესაძლოა დღგ-ს რეგისტრაციაც დაგჭირდეთ — თვალი ადევნეთ ბრუნვას."),
        ("როგორ ვხურავ ინდ. მეწარმეს?", "დახურვა საგადასახადოსა და რეესტრში გადის; ვალები და ნულოვანი დეკლარაციები ჯერ მოაგვარეთ, თორემ ჯარიმა გროვდება."),
        ("სჭირდება ბუღალტერი მარტოხელა ინდ. მეწარმეს?", "ხშირად არა — მცირე ბრუნვას თავად აწარმოებთ; თანამშრომლებთან ან დღგ-სთან უკვე კი."),
        ("რა ვალუტაში იხდის ინდ. მეწარმე გადასახადს?", "ლარში — უცხოური ბრუნვა ჩარიცხვის დღის კურსით ითვლება, კონვერტაციას კი ბანკი აკეთებს."),
    ],
})

ARTICLES.append({
    "lang": "ge", "kind": "post",
    "url": "/ge/blog/public-service-hall-georgia/", "blog_root": "/ge/blog/",
    "alt": {"ru": "/blog/dom-yustitsii-tbilisi/",
            "en": "/en/blog/public-service-hall-georgia/",
            "ge": "/ge/blog/public-service-hall-georgia/"},
    "title": "იუსტიციის სახლი თბილისში 2026: სერვისები",
    "meta": "იუსტიციის სახლი თბილისში: რას შეიტანთ ერთ სარკმელში, როგორ დაჯავშნოთ, სამუშაო საათები, რიგები, სერვისები უცხოელებისთვის და თარჯიმნის გამოყენება.",
    "h1": "იუსტიციის სახლი თბილისში: რას აკეთებენ ერთ სარკმელში",
    "crumb": "იუსტიციის სახლი",
    "label": "გზამკვლევი · 7 წთ",
    "image": "/images/blog/dom-yustitsii-tbilisi.webp",
    "meta_bits": ["გზამკვლევი", "ცხოვრება საქართველოში", "სახელმწიფო სერვისები"],
    "toc": [("ras", "რას შეიტანთ"), ("erti", "როგორ მუშაობს ერთი სარკმელი"),
            ("saatebi", "საათები, ჯავშანი, რიგები"), ("ucxoelebi", "რას აკეთებენ უცხოელები"),
            ("qorwineba", "როგორ დავქორწინდეთ"), ("vizti", "ვიზიტი ეტაპობრივად"),
            ("waიღeთ", "რა წაიღოთ"), ("mosakrebeli", "მოსაკრებელი და გადახდა"),
            ("enebi", "ენები და ხელმისაწვდომობა"),
            ("onlain", "ონლაინ ვიზიტის გარეშე"), ("regionebi", "იუსტიციის სახლი რეგიონებში"),
            ("qoneba", "უძრავი ქონება და მინდობილობა"), ("shecdomebi", "ხშირი შეცდომები")],
    "lead": "<strong>იუსტიციის სახლი</strong> ერთი სარკმლის პრინციპია, სადაც ათობით სახელმწიფო სერვისი ერთ სახურავქვეშაა: ქორწინება, კომპანიის საბუთები, უძრავი ქონება, ბინადრობა, ცნობები, აპოსტილი, ნოტარიული აქტები. თბილისის მთავარი შენობა მდინარეზე გამორჩეული „სოკოა“. აი, რას აკეთებენ იქ უცხოელები და როგორ გაიარონ ქართულის გარეშე.",
    "body": """
<h2 id="ras">რას შეიტანთ</h2>
<p>ქორწინება და სამოქალაქო აქტები; <a href="/ge/blog/company-registration-georgia/">კომპანიის რეგისტრაცია</a> (ინდ. მეწარმე/შპს); უძრავი ქონების უფლებები და გარიგებები; <a href="/ge/blog/residence-permit-georgia/">ბინადრობისა</a> და პირადობის განაცხადები; დაბადებისა და სახელის შეცვლის აქტები; აპოსტილი ქართულ საბუთებზე; ამონაწერები და ცნობები; ზოგი ნოტარიული და საბანკო სერვისი პირდაპირ დარბაზში.</p>
<h2 id="erti">როგორ მუშაობს ერთი სარკმელი</h2>
<p>იღებთ ტალონს სერვისზე, ელოდებით ნომერს ეკრანზე, მიდიხართ ოპერატორთან, აბარებთ საბუთებს და იქვე იხდით მოსაკრებელს. ბევრი სერვისი იმავე დღეს კეთდება. ოპერატორები ქართულად ემსახურებიან (ზოგი ინგლისურად), ფორმები და ქვითრები კი ქართულადაა — სწორედ აქ არის თარგმანი მნიშვნელოვანი.</p>
<p>პრაქტიკული ნიუანსი: ტალონის აღებისას სწორად აირჩიეთ სერვისის კატეგორია — ერთი შენობა ათეულ სხვადასხვა სერვისს ემსახურება, და არასწორი ტალონი ნიშნავს, რომ ხაზი გაიარეთ და თავიდან უნდა დაიწყოთ. თუ ეჭვი გაქვთ, ინფორმაციის სარკმელი ან დარბაზში მოსიარულე კონსულტანტი დაგეხმარებათ სწორი კატეგორიის არჩევასა და პირველი ეტაპის მარშრუტში.</p>
<h2 id="saatebi">საათები, ჯავშანი და რიგები</h2>
<p>თბილისის მთავარი შენობა შაბათ-კვირასაც მუშაობს (მიმდინარე გრაფიკი — psh.gov.ge-ზე). ზოგ სერვისზე ჯავშანი შესაძლებელია, რაც დროს ზოგავს; დატვირთულ სერვისებზე რიგი შუადღემდე შესამჩნევია. მოდით ადრე და სრული პაკეტით, რომ ორჯერ არ იაროთ.</p>
<p>დღისა და სეზონის არჩევაც შველის: დილის პირველი საათები და შუა კვირა ჩვეულებრივ თავისუფალია, ხოლო თვის ბოლო და დღესასწაულების წინა დღეები — ყველაზე დატვირთული. ზოგ სერვისზე, მაგალითად ბინადრობის განახლებაზე, სეზონურ პიკებსაც შეამჩნევთ, ამიტომ თუ ვადა გიწვავთ, ჯავშანი წინასწარ აიღეთ და დაჩქარებული ტარიფიც გაითვალისწინეთ.</p>
<div class="info-box">ყველაზე ხშირი „დაკარგული დღე“ — ჩამოსვლა ნოტარიული თარგმანის ან აპოსტილის გარეშე. მათი წინასწარ მომზადება იხ. <a href="/ge/blog/document-translation-notary-georgia/">თარგმანი და ნოტარიუსი</a>.</div>
<h2 id="ucxoelebi">რას აკეთებენ ყველაზე ხშირად უცხოელები</h2>
<ul>
<li><strong>ქორწინდებიან</strong> — საქართველო სწრაფია; იხ. <a href="/ge/blog/how-to-get-married-in-georgia/">როგორ დავქორწინდეთ</a>;</li>
<li><strong>ხსნიან ინდ. მეწარმეს/შპს-ს</strong> — იხ. <a href="/ge/blog/company-registration-georgia/">კომპანიის რეგისტრაცია</a>;</li>
<li><strong>ითხოვენ ბინადრობას</strong> — იხ. <a href="/ge/blog/residence-permit-georgia/">ბინადრობის ნებართვა</a>;</li>
<li><strong>ამოწმებენ თარგმანებს და აპოსტილს</strong> ქართულ საბუთებზე.</li>
</ul>
<p>ცალკე უნდა აღინიშნოს ბინადრობის ან პირადობის ბარათი: ბინადრობის დამტკიცების შემდეგ სწორედ იუსტიციის სახლში იღებთ ბიომეტრიულ ID-ბარათს — ფოტოს გადაგიღებენ, აიღებენ ხელმოწერასა და თითის ანაბეჭდს ადგილზე. ბარათი მოგვიანებით მზადდება, მისი აღება კი ან პირადად ხდება, ან წარმომადგენლის მეშვეობით მინდობილობით. ეს ბარათი შემდეგ ბევრ ყოველდღიურ საკითხს ამარტივებს — ბანკიდან ხელშეკრულებებამდე.</p>
<h2 id="qorwineba">როგორ დავქორწინდეთ</h2>
<p>ქორწინება ერთ-ერთი ყველაზე ხშირი მიზეზია, რის გამოც უცხოელები იუსტიციის სახლში მიდიან, და საქართველო მართლაც მოსახერხებელია: მოთხოვნები მინიმალურია, დაქორწინება კი ხშირად იმავე ან მეორე დღეს შეიძლება. ორივე მხარეს სჭირდება მოქმედი პასპორტი ნოტარიული თარგმანით; ზოგ შემთხვევაში — ცნობა, რომ პირი ქორწინებაში არ იმყოფება, აპოსტილით მომზადებული. მთავარი ნიუანსი: ცერემონია და გაფორმება ქართულადაა, ამიტომ თარჯიმანი ფორმალობა კი არა, აუცილებელი პირობაა — გაუგებრობის გარეშე, რას აწერთ ხელს, რეგისტრაციას უბრალოდ არ ჩაატარებენ. არსებობს „საზეიმო“ ფორმატიც ცალკე დარბაზებში, თუ გსურთ არა მხოლოდ ბეჭედი, არამედ ღონისძიება. როგორ ვუწევთ თანხლებას რეგისტრაციაზე, აღწერილია სერვისში <a href="/ge/interpreter-and-support-georgia/">თარჯიმანი და თანხლება</a>.</p>
<h2 id="vizti">ვიზიტი ეტაპობრივად</h2>
<ol>
<li>წინასწარ დააზუსტეთ სერვისი და საბუთები.</li>
<li>დაჯავშნეთ ონლაინ, თუ შესაძლებელია.</li>
<li>აიღეთ ტალონი ან მოდით დანიშნულ დროზე.</li>
<li>ჩააბარეთ საბუთები და თარგმანები, გადაიხადეთ მოსაკრებელი.</li>
<li>აიღეთ შედეგი ან მიიღეთ დანიშნული თარიღი.</li>
</ol>
<h2 id="waიღeთ">რა წაიღოთ</h2>
<p>პასპორტი და ნოტარიულად დამოწმებული თარგმანები; აპოსტილი, თუ პროცედურას სჭირდება; საფუძვლის დადასტურება (კონტრაქტი, ცნობა); ფული მოსაკრებელზე — ბარათით ან ნაღდით. არასრული პაკეტი დაკარგული დღის მთავარი მიზეზია.</p>
<p>ერთი წვრილმანი, რომელიც ვიზიტს ამარტივებს: თან იქონიეთ საბუთების ასლებიც — პასპორტისა და თარგმანების. ხშირად ორიგინალს ადგილზე ასკანერებენ და გიბრუნებენ, მაგრამ ზოგ პროცედურას ასლი სჭირდება, და მისი იქვე გაკეთება ცალკე რიგსა და დროს ნიშნავს.</p>
<h2 id="mosakrebeli">მოსაკრებელი და გადახდა</h2>
<p>თითქმის ყველა სერვისი ფასიანია და უმეტესს აქვს დაჩქარებული ტარიფი: რაც უფრო სწრაფად გჭირდებათ, მით ძვირია. პირობითად არის „სტანდარტი“ (რამდენიმე სამუშაო დღე), „დაჩქარებული“ (დღე) და „იმავე საათში“ ნაწილისთვის. იხდით ადგილზე ბარათით ან ნაღდით. ზუსტი თანხები იცვლება — სვერიფიცირდით psh.gov.ge-ზე; ხშირად „სტანდარტი“ სავსებით საკმარისია.</p>
<p>დაჩქარებულ ტარიფზე ერთი წესი გამოგადგებათ: სისწრაფეში გადაიხადეთ მხოლოდ მაშინ, როცა ვადა მართლა გიწვავთ. ბევრი უცხოელი ავტომატურად ირჩევს „იმავე დღეს“, თუმცა სტანდარტული ვადა — რამდენიმე სამუშაო დღე — უმეტეს პროცედურას სავსებით ჰყოფნის და ორ-სამჯერ იაფია. თუ საბუთი შემდეგი ეტაპისთვის გჭირდებათ, მაგალითად ბანკისთვის ან ბინადრობისთვის, ჯერ ის ვადა დააზუსტეთ, მერე აირჩიეთ ტარიფი.</p>
<h2 id="enebi">ენები და ხელმისაწვდომობა</h2>
<p>მომსახურების ძირითადი ენა ქართულია; ნაწილი ოპერატორისა ინგლისურად საუბრობს, მაგრამ ყველა სარკმელთან რუსულ ან ინგლისურ მომსახურებაზე იმედი არ უნდა გქონდეთ, ანკეტები და ქვითრები კი ისედაც ქართულადაა. სწორედ ამიტომ თარჯიმანი გვერდით არა იმდენად ნერვებს, რამდენადაც ვიზიტებს ზოგავს: მასთან ერთად განაცხადს პირველივე ჯერზე სწორად ავსებთ და საჭირო ტალონს იღებთ. შენობები თანამედროვე და ხელმისაწვდომია, ელექტრონული რიგითა და მოსაცდელი ზონებით, მაგრამ პიკის საათებში ნაკადი დიდია — დრო მარაგით დაგეგმეთ.</p>
<h2 id="onlain">ონლაინ ვიზიტის გარეშე</h2>
<p>ნაწილი სერვისებისა მოგზაურობას არ საჭიროებს. სახელმწიფო სერვისების პორტალზე ზოგ ცნობასა და ამონაწერს ელექტრონულად უკვეთავთ, მზა დოკუმენტი კი ციფრულად მოდის ან მოგვიანებით მიაქვთ. ეს რიგს ზოგავს მარტივი მოთხოვნებისთვის. მაგრამ რთული პროცედურები — ქორწინება, კომპანიის რეგისტრაცია, ბინადრობის განაცხადი, ქონების გარიგებები — კვლავ პირადად გადის.</p>
<p>მზა საბუთის მიღების რამდენიმე გზა არსებობს: ადგილზე აღება ტალონით, ელექტრონული ვერსია პორტალზე, ან ზოგ შემთხვევაში კურიერით მიტანა მითითებულ მისამართზე დამატებით ფასად. თუ დაკავებული ხართ ან ქალაქში არ ხართ მიღების დღეს, კურიერი ან წარმომადგენელი მინდობილობით დროსა და მეორე ვიზიტს ზოგავს. დააზუსტეთ ეს ვარიანტები საბუთების ჩაბარებისთანავე, რომ შემდეგ არ დაბრუნდეთ.</p>
<h2 id="regionebi">იუსტიციის სახლი რეგიონებში</h2>
<p>თბილისის მთავარი შენობა ყველაზე ცნობილია, მაგრამ ქსელი უფრო ფართოა: ფილიალები მუშაობს ბათუმში, ქუთაისში, რუსთავსა და სხვა ქალაქებში, მცირე დასახლებებში კი საბაზისო სერვისებს საზოგადოებრივი ცენტრები უწევენ. თუ დედაქალაქში არ ცხოვრობთ, ცნობისთვის თბილისში ჩამოსვლა აუცილებელი არ არის — ჯერ შეამოწმეთ უახლოესი ფილიალი psh.gov.ge-ზე.</p>
<h2 id="qoneba">უძრავი ქონება და მინდობილობა</h2>
<p>იუსტიციის სახლის სერვისების დიდი ბლოკია უძრავი ქონება: საკუთრების უფლების რეგისტრაცია ყიდვისას, ამონაწერები, გირავნობა და ხელშეკრულებები. უცხოელისთვის ეს ერთ-ერთი ყველაზე მგრძნობიარე პროცედურაა — გარიგება და ხელშეკრულება ქართულადაა. ყიდვამდე ითხოვენ ახალ ამონაწერს რეესტრიდან, რომ დარწმუნდნენ ობიექტის სისუფთავეში. აქვე კეთდება მინდობილობებიც — მაგალითად, თუ გსურთ, რომ წარმომადგენელი მოქმედებდეს, სანამ საზღვარგარეთ ხართ.</p>
<p>უცხოელს ცალკე უნდა ახსოვდეს ორი რამ ქონების გარიგებაში. პირველი — სასოფლო-სამეურნეო მიწაზე უცხოელის საკუთრებას შეზღუდვები აქვს, ხოლო ბინასა და კომერციულ ფართზე ჩვეულებრივ არა; მიწის ყიდვამდე სტატუსი წინასწარ დააზუსტეთ. მეორე — ხელშეკრულებას ხელს ქართულ ტექსტზე აწერთ, ამიტომ თარჯიმანთან ერთად წაკითხვა და პირობების გადამოწმება არა ფორმალობა, არამედ დაცვაა. ახალი ამონაწერი გარიგების დღეს აიღეთ, რომ დარწმუნდეთ, ობიექტი არ არის დატვირთული გირავნობით ან დავით.</p>
<h2 id="shecdomebi">ხშირი შეცდომები</h2>
<ul>
<li>მოსვლა ნოტარიული თარგმანის ან აპოსტილის გარეშე;</li>
<li>სერვისისა და ტალონის აღრევა;</li>
<li>პიკზე მოსვლა ჯავშნის გარეშე;</li>
<li>მოსაკრებლის ზუსტი ოდენობის უცოდინრობა.</li>
</ul>
""" + cta_ge("გეტყვით სერვისსა და პაკეტს, დავჯავშნით, ვთარგმნით სარკმელთან და გაგიყვანთ ტალონიდან შედეგამდე.") + """
<div class="sources-block"><p class="sources-title">ოფიციალური წყაროები</p><ul>
<li><a href="https://psh.gov.ge/" rel="noopener noreferrer" target="_blank">იუსტიციის სახლი (psh.gov.ge)</a></li>
<li><a href="https://sda.gov.ge/" rel="noopener noreferrer" target="_blank">სახელმწიფო სერვისების სააგენტო (sda.gov.ge)</a></li>
</ul></div>
""",
    "related": [
        ("კერძო გიდი თბილისში", "ძველი თბილისი, მცხეთა, ყაზბეგი.", "/ge/private-guide-tbilisi/"),
        ("ყაზბეგი ერთ დღეში", "მთა ერთ დღეში.", "/ge/blog/kazbegi-day-trip-from-tbilisi/"),
        ("გზამკვლევი ექსპატებისთვის", "თბილისში ფეხის მოკიდება.", "/ge/blog/tbilisi-for-expats/"),
    ],
    "faq": [
        ("რას შევიტან იქ?", "ქორწინება, კომპანია, ქონება, ბინადრობა, ცნობები, აპოსტილი, ნოტარიული აქტები."),
        ("საჭიროა ჯავშანი?", "ზოგ სერვისზე — კი და დროს ზოგავს; სხვებზე ცოცხალი რიგია."),
        ("შაბათ-კვირას მუშაობს?", "თბილისის მთავარი შენობა — კი; შეამოწმეთ psh.gov.ge."),
        ("რომელ ენაზე ემსახურებიან?", "ქართულად, ზოგი სერვისი ინგლისურად; დოკუმენტები ქართულად."),
        ("რა წავიღო?", "პასპორტი, ნოტარიული თარგმანები, საჭიროებისას აპოსტილი, ფული მოსაკრებელზე."),
        ("არის ფილიალები სხვა ქალაქებში?", "დიახ — თბილისის გარდა ბათუმში, ქუთაისში, რუსთავსა და სხვაგან, პლუს საზოგადოებრივი ცენტრები."),
        ("სად ვიღებ ბინადრობის ბარათს?", "იუსტიციის სახლში: ბიომეტრიას ადგილზე იღებენ, ბარათი მოგვიანებით მზადდება."),
        ("შესაძლებელია მზა საბუთის კურიერით მიღება?", "ზოგ სერვისზე — კი, დამატებით ფასად; დააზუსტეთ ჩაბარებისთანავე."),
        ("როდის არის ყველაზე ნაკლები რიგი?", "დილის პირველი საათები და შუა კვირა ყველაზე თავისუფალია; თვის ბოლო — დატვირთული."),
        ("რომელი მოსაკრებელი ავირჩიო — სტანდარტი თუ დაჩქარებული?", "სტანდარტი უმეტეს შემთხვევაში კმარა და იაფია; დაჩქარებული — მხოლოდ თუ ვადა გიწვავთ."),
        ("რა ენაზეა მომსახურება სარკმელთან?", "ძირითადად ქართულად, ზოგი ოპერატორი ინგლისურად; ანკეტები და ქვითრები ქართულადაა."),
    ],
})


def path_for(a):
    return os.path.join(ROOT, a["url"].strip("/"), "index.html")


def main():
    total = 0
    print(f"{'APPLY' if APPLY else 'DRY'} — building cluster\n")
    for a in ARTICLES:
        if ONLY and a["lang"] != ONLY:
            continue
        doc, words = render(a)
        p = path_for(a)
        # Calibrated to site convention: prod flagship otkryt-schet = 1238 real
        # tokens but declares wordCount 1600 → real ~1100 == "1500-word tier".
        flag = "OK " if words >= 1100 else "LOW"
        print(f"  [{flag}] {words:>4} токенов  {a['url']}")
        if APPLY:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(doc)
        total += 1
    print(f"\n{total} страниц {'записано' if APPLY else '(dry-run, файлы не тронуты)'}")


if __name__ == "__main__":
    main()
