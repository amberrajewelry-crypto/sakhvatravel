#!/usr/bin/env python3
"""Insert reciprocal inbound-link cards into existing hub articles. Idempotent."""
import re, pathlib
ROOT = pathlib.Path("/Users/vladimir/sakhva-travel")

# localized bits
PILLAR = {
    "ru": ("/perevodchik-i-soprovozhdenie-v-gruzii/", "Услуга", "Переводчик и сопровождение",
           "Врач, банк, нотариус, ВНЖ — переводим и ведём рядом.", "Подробнее →"),
    "en": ("/en/interpreter-and-support-georgia/", "Service", "Interpreter & Support",
           "Doctor, bank, notary, residence — we translate and guide.", "Learn more →"),
    "ge": ("/ge/interpreter-and-support-georgia/", "სერვისი", "თარჯიმანი და თანხლება",
           "ექიმი, ბანკი, ნოტარიუსი, ბინადრობა — ვთარგმნით და თან ვახლავართ.", "ვრცლად →"),
}
TOPIC = {
    ("ru","residence"): ("/blog/vid-na-zhitelstvo-v-gruzii/", "Гид", "Вид на жительство в Грузии", "Типы ВНЖ, документы, сроки.", "Читать →"),
    ("ru","company"):   ("/blog/registratsiya-kompanii-v-gruzii/", "Гид", "Регистрация компании и ИП", "Формы, статус 1%, шаги.", "Читать →"),
    ("ru","documents"): ("/blog/perevod-i-zaverenie-dokumentov-v-gruzii/", "Гид", "Перевод и заверение документов", "Апостиль, нотариус, порядок.", "Читать →"),
    ("ru","psh"):       ("/blog/dom-yustitsii-tbilisi/", "Гид", "Дом юстиции в Тбилиси", "Что подать в одном окне.", "Читать →"),
    ("en","residence"): ("/en/blog/residence-permit-georgia/", "Guide", "Residence Permit in Georgia", "Types, documents, timelines.", "Read →"),
    ("en","company"):   ("/en/blog/company-registration-georgia/", "Guide", "Company Registration", "Forms, 1% status, steps.", "Read →"),
    ("en","documents"): ("/en/blog/document-translation-notary-georgia/", "Guide", "Document Translation & Notary", "Apostille, notary, order.", "Read →"),
    ("en","psh"):       ("/en/blog/public-service-hall-georgia/", "Guide", "Public Service Hall Tbilisi", "What you file in one place.", "Read →"),
    ("ge","residence"): ("/ge/blog/residence-permit-georgia/", "გზამკვლევი", "ბინადრობის ნებართვა", "ტიპები, საბუთები, ვადები.", "ვრცლად →"),
    ("ge","company"):   ("/ge/blog/company-registration-georgia/", "გზამკვლევი", "კომპანიის რეგისტრაცია", "ფორმები, 1% სტატუსი, ნაბიჯები.", "ვრცლად →"),
    ("ge","documents"): ("/ge/blog/document-translation-notary-georgia/", "გზამკვლევი", "საბუთების თარგმანი", "აპოსტილი, ნოტარიუსი, თანმიმდევრობა.", "ვრცლად →"),
    ("ge","psh"):       ("/ge/blog/public-service-hall-georgia/", "გზამკვლევი", "იუსტიციის სახლი", "რას შეიტანთ ერთ სარკმელში.", "ვრცლად →"),
}

# hub file -> (lang, second-topic)
HUBS = [
    ("blog/digital-nomad-tbilisi/index.html", "ru", "company"),
    ("blog/otkryt-schet-v-banke-gruzii/index.html", "ru", "residence"),
    ("en/blog/tbilisi-for-expats/index.html", "en", "residence"),
    ("en/blog/open-bank-account-georgia/index.html", "en", "company"),
    ("en/blog/how-to-get-married-in-georgia/index.html", "en", "psh"),
    ("en/blog/digital-nomad-tbilisi/index.html", "en", "documents"),
    ("ge/blog/tbilisi-for-expats/index.html", "ge", "residence"),
    ("ge/blog/open-bank-account-georgia/index.html", "ge", "company"),
    ("ge/blog/how-to-get-married-in-georgia/index.html", "ge", "psh"),
    ("ge/blog/digital-nomad-tbilisi/index.html", "ge", "documents"),
]

def card(url, label, title, desc, cta):
    return (f'<div class="rc-card"><div class="rc-card-label">{label}</div>'
            f'<h3>{title}</h3><p>{desc}</p><a href="{url}">{cta}</a></div>\n')

done = []
for rel, lang, topic in HUBS:
    p = ROOT / rel
    if not p.exists():
        print(f"SKIP (нет файла): {rel}"); continue
    h = p.read_text(encoding="utf-8")
    pu = PILLAR[lang]; tu = TOPIC[(lang, topic)]
    added = []
    cards = ""
    if pu[0] not in h:
        cards += card(pu[0], pu[1], pu[2], pu[3], pu[4]); added.append("pillar")
    if tu[0] not in h:
        cards += card(tu[0], tu[1], tu[2], tu[3], tu[4]); added.append(topic)
    if not cards:
        print(f"уже есть: {rel}"); continue
    m = re.search(r'<div class="related-grid">\s*', h)
    if not m:
        print(f"НЕТ related-grid: {rel}"); continue
    h = h[:m.end()] + cards + h[m.end():]
    p.write_text(h, encoding="utf-8")
    done.append((rel, added))
    print(f"OK {rel}: +{added}")

print(f"\nИтого изменено: {len(done)} файлов")
