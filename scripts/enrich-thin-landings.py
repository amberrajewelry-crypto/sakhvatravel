#!/usr/bin/env python3
"""Add real, useful content to the last 8 thin indexable landing/contact pages."""
import re, sys, os
APPLY = "--apply" in sys.argv
ROOT = os.path.expanduser("~/sakhva-travel")

DET = ('<details style="border-bottom:1px solid #E5E7EB;padding:14px 0">'
       '<summary style="font-weight:600;color:#111;cursor:pointer;list-style:none">{q}</summary>'
       '<p style="margin-top:8px">{a}</p></details>')
FI = ('<div class="fi"><button class="fq" onclick="toggleFaq(this)"><span>{q}</span>'
      '<span class="fq-ic">+</span></button><div class="fa"><div class="fa-inner">{a}</div></div></div>')

# (path, anchor_type, [(q,a)...])
PAGES = [
("ge/private-guide-tbilisi/index.html", "main", [
  ("როგორ ჯავშნდება კერძო ტური?", "მოგვწერეთ WhatsApp-ში სასურველი თარიღი და მარშრუტი, ჩვენ დავადასტურებთ გიდსა და მანქანას და გამოგიგზავნით გეგმას. გადახდა ხდება ადგილზე ან წინასწარ; გაუქმება უფასოა ტურამდე 24 საათით ადრე."),
  ("რა შედის ფასში?", "ფასში შედის კერძო გიდი-მძღოლი, კომფორტული მანქანა საწვავითურთ და მარშრუტის დაგეგმვა. შესვლის ბილეთები, კვება და დეგუსტაციები იხდება ცალკე — ასე ფასი გამჭვირვალეა და ზედმეტს არ იხდით."),
]),
("ge/wine-tours-georgia/index.html", "main", [
  ("რომელ რეგიონებში მივყავართ ღვინის ტურებზე?", "ძირითადად კახეთში — თელავი, სიღნაღი, წინანდალი და ალავერდი, სადაც ქვევრის ტრადიცია ცოცხალია. ასევე შესაძლებელია ქართლისა და რაჭის მარნები, თუ იშვიათ ჯიშებს ეძებთ."),
  ("რა შედის ღვინის ტურში?", "კერძო გიდი-მძღოლი, მარნების მონახულება და, სურვილისამებრ, დეგუსტაცია ქართული კერძებით. დეგუსტაციისა და სადილის საფასური იხდება ადგილზე, რაც ფასს გამჭვირვალეს ხდის."),
]),
("ge/contacts/index.html", "main", [
  ("რამდენ ხანში მიპასუხებთ?", "WhatsApp-ში ვპასუხობთ ჩვეულებრივ რამდენიმე საათში, დილის 9-დან საღამოს 9-მდე (თბილისის დრო). დაჯავშნის დასადასტურებლად საკმარისია სასურველი თარიღი და მარშრუტი."),
  ("რა ენებზე გელაპარაკებით და როგორ იხდით?", "ვმუშაობთ ინგლისურად და რუსულად. გადახდა შესაძლებელია ნაღდით ადგილზე ან ონლაინ ბარათით/გადარიცხვით წინასწარი დაჯავშნისას."),
]),
("en/contacts/index.html", "main", [
  ("How fast do you reply?", "We usually answer on WhatsApp within a few hours, from 9:00 to 21:00 Tbilisi time. To confirm a booking we just need your preferred date and the route you have in mind."),
  ("Which languages do you speak and how do I pay?", "We guide in English and Russian. You can pay in cash on the day or online by card or bank transfer when you book in advance — whatever is easier for you."),
]),
("contacts/index.html", "main", [
  ("Как быстро вы отвечаете?", "В WhatsApp обычно отвечаем в течение нескольких часов, с 9:00 до 21:00 по Тбилиси. Чтобы подтвердить бронь, достаточно назвать желаемую дату и маршрут — остальное подскажем сами."),
]),
("ge/destinations/index.html", "fi", [
  ("საიდან დავიწყო მარშრუტის არჩევა?", "თუ პირველად ხართ საქართველოში, დაიწყეთ ყაზბეგითა და კახეთით — მთა და ღვინო ერთ შთაბეჭდილებაში. მეორე ვიზიტზე ღირს სვანეთი, რაჭა ან ბათუმი შავ ზღვაზე."),
]),
("en/destinations/index.html", "fi", [
  ("Where should I start when choosing a route?", "If it is your first time in Georgia, start with Kazbegi and Kakheti — mountains and wine in one trip. On a second visit, Svaneti, Racha or Batumi on the Black Sea are worth the extra days."),
]),
]


def main():
    tot = 0
    for path, anchor, items in PAGES:
        f = os.path.join(ROOT, path)
        h = open(f, encoding="utf-8").read()
        if anchor == "fi":
            add = "".join("\n" + FI.format(q=q, a=a) for q, a in items if q not in h)
            m = re.search(r'(</div>)(\s*<div class="other-regions">)', h)
            if not m: print("  ERR anchor", path); continue
            new = h[:m.start(1)] + add + "\n" + h[m.start(1):]
        else:
            add = "".join("\n" + DET.format(q=q, a=a) for q, a in items if q not in h)
            if not add.strip(): print("  skip", path); continue
            i = h.rfind("</main>")
            if i < 0: print("  ERR </main>", path); continue
            new = h[:i] + add + "\n" + h[i:]
        if APPLY:
            open(f, "w", encoding="utf-8").write(new)
        tot += 1
        print("  +", path)
    print(f"\n{'APPLIED' if APPLY else 'DRY'} — {tot}")


if __name__ == "__main__":
    main()
