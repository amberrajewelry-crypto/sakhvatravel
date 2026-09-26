#!/usr/bin/env python3
"""Tbilisoba 2026: official dates/venues/program (Tbilisi City Hall, announced 22.09.2026).

Sources: sputnik-georgia.ru 22.09.2026, sovanews.tv 22.09.2026, newsgeorgia.ge.
- exact dates 3–4 October (Sat–Sun) instead of "City Hall will announce";
- official 5 venues instead of the generic Old Town list;
- 2026 program box + (RU/EN) offer to join an Old Tbilisi walk on the festival days;
- removes the review quote dated "October 2026" (future date, not a real review);
- FAQ (JSON-LD + visible), title/og/meta, dateModified.
Idempotent: pages already carrying data-sk="tbilisoba-2026" are skipped.
Run: python3 scripts/tbilisoba-2026-facts.py
"""
import json
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARK = 'data-sk="tbilisoba-2026"'
TODAY = "2026-09-26"
WA = "995511272623"
BOX = ('<div class="tip-box" ' + MARK + '><div class="tip-box-title">{title}</div>'
       '<ul>{items}</ul><p style="font-size:13px;color:#6B7280;margin:8px 0 0">{src}</p></div>')
OFFER = ('<p style="background:#FFFBEB;border:1px solid #F59E0B;border-radius:12px;padding:14px 18px">'
         '<strong>{head}</strong> {body} <a href="{tour}" style="color:#1A3D2E;font-weight:600">{tour_lbl}</a> · '
         '<a href="https://wa.me/' + WA + '?text={wa}" style="color:#1A3D2E;font-weight:600">{wa_lbl}</a></p>')

L = {
    "ru": dict(
        file="blog/tbilisoba/index.html", h_when="kogda", h_venues="ploshchadki",
        q_when="Когда Тбилисоба в 2026 году?", q_where="Где проходит Тбилисоба?",
        when=('<p>Тбилисоба-2026 пройдёт <strong>3 и 4 октября</strong> (суббота и воскресенье) — '
              'даты официально объявила мэрия Тбилиси 22 сентября. Праздник, как и с 2018 года, '
              'приходится на первые выходные октября, бюджет в этом году — 3,1 млн лари.</p>'),
        box_title="Программа Тбилисобы-2026 (по анонсу мэрии)",
        items=["Днём — детские концерты на всех площадках, спортивные и развлекательные мероприятия",
               "Вечером — театрализованные представления и музыкальные вечера",
               "Открытый кинотеатр, фотозоны и зоны отдыха",
               "Гастрономические зоны: грузинская и зарубежная кухня, кулинарные мастер-классы",
               "Ярмарка традиционных сладостей, мёда и вина",
               "4 октября в 20:00 — церемония награждения почётных граждан Тбилиси (прямая трансляция)"],
        src="Подробная программа по часам публикуется на сайте мэрии Тбилиси.",
        venues_intro="<p>В 2026 году мэрия объявила пять площадок праздника:</p>",
        venues=["<strong>Парк Рике</strong> — главная площадка у Куры, вид на Нарикалу и мост Мира.",
                "<strong>Площадь Орбелиани</strong> — рядом с улицей Шардени и Старым городом.",
                "<strong>Площадь Гудиашвили</strong> — отреставрированный квартал старого Тбилиси.",
                "<strong>Легвтахеви</strong> — ущелье с водопадом рядом с серными банями Абанотубани.",
                "<strong>Площадь Европы и Метехский мост</strong> — левый берег Куры у церкви Метехи."],
        faq_when=("Тбилисоба-2026 пройдёт 3 и 4 октября (суббота и воскресенье) — даты объявила мэрия "
                  "Тбилиси. Днём — детские концерты, ярмарки и гастрономические зоны, вечером — "
                  "представления и музыкальные вечера. 4 октября в 20:00 — церемония награждения "
                  "почётных граждан Тбилиси."),
        faq_where=("В 2026 году — на пяти площадках: парк Рике, площадь Орбелиани, площадь Гудиашвили, "
                   "Легвтахеви, площадь Европы и Метехский мост. Все они в центре, между собой — "
                   "10–15 минут пешком; центр в эти дни частично перекрывают для машин."),
        title="Тбилисоба 2026: 3–4 октября — программа, площадки, советы",
        desc=("Тбилисоба 2026 пройдёт 3–4 октября: пять площадок (Рике, Орбелиани, Гудиашвили, "
              "Легвтахеви, Метехи), программа мэрии, ртвели и советы туристу."),
        offer=dict(head="Будете в Тбилиси 3–4 октября?",
                   body="Гид проведёт по площадкам праздника и дворам Старого города, где давят виноград.",
                   tour="/ekskursiya/ekskursiya-stary-tbilisi/", tour_lbl="Старый Тбилиси с гидом — от ₾135",
                   wa_text="Здравствуйте! Будем в Тбилиси на Тбилисобу 3–4 октября, хотим прогулку с гидом.",
                   wa_lbl="Написать в WhatsApp"),
    ),
    "en": dict(
        file="en/blog/tbilisoba/index.html", h_when="when", h_venues="venues",
        q_when="When is Tbilisoba in 2026?", q_where="Where does Tbilisoba take place?",
        when=('<p>Tbilisoba 2026 takes place on <strong>3 and 4 October</strong> (Saturday and Sunday) — '
              'Tbilisi City Hall officially announced the dates on 22 September. As every year since 2018, '
              'the festival falls on the first weekend of October; this year\'s budget is 3.1 million GEL.</p>'),
        box_title="Tbilisoba 2026 program (City Hall announcement)",
        items=["Daytime — children's concerts at every venue, sports and entertainment events",
               "Evenings — theatre performances and music nights",
               "Open-air cinema, photo zones and chill-out areas",
               "Food zones: Georgian and international cuisine, cooking master classes",
               "Fair of traditional sweets, honey and wine",
               "4 October, 20:00 — Honorary Citizens of Tbilisi award ceremony (broadcast live)"],
        src="The hour-by-hour program is published on the Tbilisi City Hall website.",
        venues_intro="<p>For 2026 City Hall announced five festival venues:</p>",
        venues=["<strong>Rike Park</strong> — the main venue on the Kura, with views of Narikala and the Bridge of Peace.",
                "<strong>Orbeliani Square</strong> — next to Shardeni Street and the Old Town.",
                "<strong>Gudiashvili Square</strong> — a restored quarter of old Tbilisi.",
                "<strong>Leghvtakhevi</strong> — the waterfall gorge beside the Abanotubani sulfur baths.",
                "<strong>Europe Square and Metekhi Bridge</strong> — the left bank of the Kura by Metekhi Church."],
        faq_when=("Tbilisoba 2026 takes place on 3 and 4 October (Saturday and Sunday), as announced by "
                  "Tbilisi City Hall. Daytime brings children's concerts, fairs and food zones; evenings "
                  "bring performances and music nights. On 4 October at 20:00 the Honorary Citizens of "
                  "Tbilisi award ceremony is held."),
        faq_where=("In 2026 it runs at five venues: Rike Park, Orbeliani Square, Gudiashvili Square, "
                   "Leghvtakhevi, and Europe Square with Metekhi Bridge. All are in the center, 10–15 "
                   "minutes' walk apart; parts of the center are closed to cars during the festival."),
        title="Tbilisoba 2026: 3–4 October — Program, Venues &amp; Tips",
        desc=("Tbilisoba 2026 is on 3–4 October: five venues (Rike, Orbeliani, Gudiashvili, "
              "Leghvtakhevi, Metekhi), the City Hall program, Rtveli and visitor tips."),
        offer=dict(head="In Tbilisi on 3–4 October?",
                   body="A local guide will take you through the festival venues and the Old Town courtyards where grapes are pressed.",
                   tour="/en/ekskursiya/ekskursiya-stary-tbilisi/", tour_lbl="Old Tbilisi with a guide — from ₾135",
                   wa_text="Hello! We'll be in Tbilisi for Tbilisoba on 3–4 October and would like a guided walk.",
                   wa_lbl="Message on WhatsApp"),
    ),
    "ka": dict(
        file="ge/blog/tbilisoba/index.html", h_when="when", h_venues="venues",
        q_when="როდის არის თბილისობა 2026 წელს?", q_where="სად ტარდება თბილისობა?",
        when=('<p>თბილისობა 2026 გაიმართება <strong>3 და 4 ოქტომბერს</strong> (შაბათი და კვირა) — '
              'თარიღები თბილისის მერიამ 22 სექტემბერს ოფიციალურად გამოაცხადა. 2018 წლიდან დღესასწაული '
              'ოქტომბრის პირველ შაბათ-კვირას ტარდება, წლევანდელი ბიუჯეტი 3,1 მლნ ლარია.</p>'),
        box_title="თბილისობა 2026-ის პროგრამა (მერიის ანონსით)",
        items=["დღისით — საბავშვო კონცერტები ყველა ლოკაციაზე, სპორტული და გასართობი ღონისძიებები",
               "საღამოს — თეატრალიზებული წარმოდგენები და მუსიკალური საღამოები",
               "ღია კინოთეატრი, ფოტოზონები და დასასვენებელი სივრცეები",
               "გასტრონომიული სივრცეები: ქართული და უცხოური სამზარეულო, კულინარიული მასტერკლასები",
               "ტრადიციული ტკბილეულის, თაფლისა და ღვინის ბაზრობა",
               "4 ოქტომბერს, 20:00 — თბილისის საპატიო მოქალაქეების დაჯილდოების ცერემონია (პირდაპირი ტრანსლაცია)"],
        src="დეტალური პროგრამა საათების მიხედვით ქვეყნდება თბილისის მერიის ვებგვერდზე.",
        venues_intro="<p>2026 წელს მერიამ დღესასწაულის ხუთი ლოკაცია გამოაცხადა:</p>",
        venues=["<strong>რიყის პარკი</strong> — მთავარი ლოკაცია მტკვრის პირას, ხედით ნარიყალასა და მშვიდობის ხიდზე.",
                "<strong>ორბელიანის მოედანი</strong> — შარდენის ქუჩისა და ძველი ქალაქის გვერდით.",
                "<strong>გუდიაშვილის მოედანი</strong> — ძველი თბილისის რესტავრირებული უბანი.",
                "<strong>ლეღვთახევი</strong> — ჩანჩქრიანი ხეობა აბანოთუბნის გოგირდის აბანოებთან.",
                "<strong>ევროპის მოედანი და მეტეხის ხიდი</strong> — მტკვრის მარცხენა სანაპირო მეტეხის ტაძართან."],
        faq_when=("თბილისობა 2026 გაიმართება 3 და 4 ოქტომბერს (შაბათი და კვირა), როგორც თბილისის მერიამ "
                  "გამოაცხადა. დღისით — საბავშვო კონცერტები, ბაზრობები და გასტრონომიული სივრცეები, "
                  "საღამოს — წარმოდგენები და მუსიკალური საღამოები. 4 ოქტომბერს 20:00 საათზე — "
                  "თბილისის საპატიო მოქალაქეების დაჯილდოების ცერემონია."),
        faq_where=("2026 წელს — ხუთ ლოკაციაზე: რიყის პარკი, ორბელიანის მოედანი, გუდიაშვილის მოედანი, "
                   "ლეღვთახევი, ევროპის მოედანი და მეტეხის ხიდი. ყველა ცენტრშია, ერთმანეთისგან 10–15 "
                   "წუთის სავალზე; დღესასწაულის დღეებში ცენტრის ნაწილი მანქანებისთვის დახურულია."),
        title="თბილისობა 2026: 3–4 ოქტომბერი — პროგრამა და ლოკაციები",
        desc=("თბილისობა 2026 — 3–4 ოქტომბერს: ხუთი ლოკაცია (რიყე, ორბელიანი, გუდიაშვილი, "
              "ლეღვთახევი, მეტეხი), მერიის პროგრამა, რთველი და რჩევები."),
        offer=None,  # GE readers are mostly locals: no guided-walk pitch
    ),
}


def sub1(pattern, repl, s, flags=re.S):
    out, n = re.subn(pattern, repl, s, count=1, flags=flags)
    if n != 1:
        sys.exit(f"pattern not found: {pattern[:80]}")
    return out


def set_faq(s, q, a):
    # JSON-LD answer
    jq = re.escape(json.dumps(q, ensure_ascii=False)[1:-1])
    s = sub1(r'("name":\s*"' + jq + r'",\s*"acceptedAnswer":\s*\{[^}]*?"text":\s*")[^"]*(")',
             lambda m: m.group(1) + json.dumps(a, ensure_ascii=False)[1:-1] + m.group(2), s)
    # visible accordion: question text, then the first fa-inner after it
    i = s.find(q, s.find("</script>", s.find('"FAQPage"')))
    if i < 0:
        sys.exit(f"visible FAQ not found: {q}")
    j = s.find('<div class="fa-inner">', i)
    k = s.find("</div>", j)
    return s[:j] + '<div class="fa-inner">' + a + s[k:]


def main():
    for lang, c in L.items():
        f = ROOT / c["file"]
        s = f.read_text()
        if MARK in s:
            print("skip", c["file"])
            continue
        # 1. "when" section: replace the first paragraph, add program box (+ offer)
        extra = BOX.format(title=c["box_title"], src=c["src"],
                           items="".join(f"<li>{x}</li>" for x in c["items"]))
        if c["offer"]:
            o = c["offer"]
            wa = urllib.parse.quote(o["wa_text"] + f"\n[site:{lang}:blog:tbilisoba]")
            extra += OFFER.format(head=o["head"], body=o["body"], tour=o["tour"],
                                  tour_lbl=o["tour_lbl"], wa=wa, wa_lbl=o["wa_lbl"])
        s = sub1(r'(id="' + c["h_when"] + r'"[^>]*>.*?</h2>\s*)<p>.*?</p>',
                 lambda m: m.group(1) + c["when"] + extra, s)
        # 2. venues: intro + list
        s = sub1(r'(id="' + c["h_venues"] + r'"[^>]*>.*?</h2>\s*)<p>.*?</p>\s*<ul>.*?</ul>',
                 lambda m: m.group(1) + c["venues_intro"] + "\n<ul>\n"
                 + "".join(f"<li>{v}</li>\n" for v in c["venues"]) + "</ul>", s)
        # 3. drop the future-dated review quote
        s = sub1(r'<div class="review-quote">.*?</div>\s*</div>\s*', "", s)
        # 4. FAQ
        s = set_faq(s, c["q_when"], c["faq_when"])
        s = set_faq(s, c["q_where"], c["faq_where"])
        # 5. title / og:title / description / og:description / dateModified
        s = sub1(r"<title>.*?</title>", f"<title>{c['title']}</title>", s)
        s = re.sub(r'<meta content="[^"]*" property="og:title"/>',
                   f'<meta content="{c["title"]}" property="og:title"/>', s)
        s = sub1(r'<meta content="[^"]*" name="description"/>',
                 f'<meta content="{c["desc"]}" name="description"/>', s)
        s = re.sub(r'<meta content="[^"]*" property="og:description"/>',
                   f'<meta content="{c["desc"]}" property="og:description"/>', s)
        s = re.sub(r'"dateModified":\s*"[^"]+"', f'"dateModified": "{TODAY}"', s)
        f.write_text(s)
        print("ok", c["file"])


if __name__ == "__main__":
    main()
