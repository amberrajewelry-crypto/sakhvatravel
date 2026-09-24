#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Очистка GE-страниц до ЧИСТО грузинского: остатки RU/EN, которые движок пропустил
(в т.ч. те, что унаследованы из «грязного» EN — русское «от» в ценах, кириллические
инициалы аватаров, англ alt/aria, англоязычный JSON-LD FAQ Аджарии). Якорная замена
со строгим счётчиком. JSON-LD правится как подстрока значения (структура/ключи целы)."""
import sys
from pathlib import Path

# {файл: [(old, new, count)]}
JOBS = {
 "ge/adjara/index.html": [
   ("от ₾350", "₾350-დან", 1),
   ("от ₾400", "₾400-დან", 1),
   ("от ₾200", "₾200-დან", 1),
   ("თბილისი to Batumi is 370 km — about 5 hours 30 minutes by car on the highway. By plane 40 minutes, by train 5 hours, by minibus from Didube 35 lari. With Sakhva Travel guide — კომფორტული ტრანსფერი სასტუმროდან.",
    "თბილისიდან ბათუმამდე 370 კმ — მანქანით დაახლოებით 5 საათი და 30 წუთი ავტომაგისტრალზე. თვითმფრინავით 40 წუთი, მატარებლით 5 საათი, მიკროავტობუსით დიდუბიდან 35 ლარი. Sakhva Travel-ის გიდთან — კომფორტული ტრანსფერი სასტუმროდან.", 1),
   ("For beach holidays — June-September (water +24-26°C). Best month is September: warm sea, fewer people, cheaper accommodation. For mountain აჭარა — May or September. Winter Batumi is mild (+8-12°C), few tourists.",
    "პლაჟის დასვენებისთვის — ივნისი-სექტემბერი (წყალი +24-26°C). საუკეთესო თვე სექტემბერია: თბილი ზღვა, ნაკლები ხალხი, იაფი საცხოვრებელი. მთიანი აჭარისთვის — მაისი ან სექტემბერი. ზამთარში ბათუმი რბილია (+8-12°C), ცოტა ტურისტი.", 1),
   ("What to see in აჭარა besides Batumi?",
    "რა ვნახოთ აჭარაში ბათუმის გარდა?", 1),
   ("Gonio Fortress (1st century), Makhuntseti waterfalls, 12th-century arched bridge, mountain აჭარა (Khulo, Goderdzi Pass), Botanical Garden, Gonio and Ureki beaches with magnetic sand.",
    "გონიოს ციხე (I საუკუნე), მახუნცეთის ჩანჩქერები, XII საუკუნის თაღოვანი ხიდი, მთიანი აჭარა (ხულო, გოდერძის უღელტეხილი), ბოტანიკური ბაღი, გონიოსა და ურეკის პლაჟები მაგნიტური ქვიშით.", 1),
   ("How much does a tour from თბილისი to Batumi cost?",
    "რა ღირს ტური თბილისიდან ბათუმამდე?", 1),
   ("A two-day ტური გიდით includes transfers, key sightseeing, restaurant recommendations. Price depends on route and number of days — message Timur on WhatsApp for a quote.",
    "ორდღიანი ტური გიდით მოიცავს ტრანსფერებს, ძირითად ღირსშესანიშნაობებს, რესტორნების რეკომენდაციებს. ფასი დამოკიდებულია მარშრუტსა და დღეების რაოდენობაზე — მისწერეთ თიმურს WhatsApp-ზე ფასის გასაგებად.", 1),
 ],
 "ge/imereti/index.html": [
   ("от ₾250", "₾250-დან", 1),
   ("от ₾350", "₾350-დან", 1),
 ],
 "ge/index.html": [
   # аватары: кириллический инициал → латиница по имени автора
   (">Т<", ">T<", 1), (">Г<", ">G<", 1), (">М<", ">M<", 1), (">В<", ">V<", 3),
   # квиз-опция
   ("Up to $50</div>", "$50-მდე</div>", 1),
   # alt
   ('alt="Guide Timur with tourists in car — private tours in Georgia"',
    'alt="გიდი თიმური ტურისტებთან მანქანაში — კერძო ტურები საქართველოში"', 1),
   ('alt="Guide Timur — Georgia tour author"',
    'alt="გიდი თიმური — საქართველოს ტურების ავტორი"', 1),
   ('alt="Private tour in Tbilisi and Georgia"',
    'alt="კერძო ტური თბილისსა და საქართველოში"', 1),
   ('alt="QR-QR code for tour payment"', 'alt="QR-კოდი ტურის გადახდისთვის"', 1),
   # aria-label
   ('aria-label="previous"', 'aria-label="წინა"', 1),
   ('aria-label="next"', 'aria-label="შემდეგი"', 1),
   ('aria-label="Chat with guide"', 'aria-label="ჩატი გიდთან"', 2),
   ('aria-label="Tour booking"', 'aria-label="ტურის ჯავშანი"', 1),
   # placeholder / title
   ('placeholder="Amount in USD"', 'placeholder="თანხა USD-ში"', 2),
   ('title="LLM-readable site info"', 'title="LLM-წაკითხვადი საიტის ინფო"', 1),
   # JSON-LD org tagline
   ("Sakhva Travel — Private Tour Georgia", "Sakhva Travel — კერძო ტურები საქართველოში", 1),
 ],
 "ge/kakheti/index.html": [
   ('alt="Kakheti Vineyards and Alazani Valley — Georgia\'s Wine Region"',
    'alt="კახეთის ვენახები და ალაზნის ველი — საქართველოს ღვინის რეგიონი"', 1),
 ],
 "ge/blog/adjarian-khachapuri-guide/index.html": [
   ('alt="Timur — Sakhva Travel guide"', 'alt="თიმური — Sakhva Travel-ის გიდი"', 1),
 ],
 "ge/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/index.html": [
   ('placeholder="+1 or +995..."', 'placeholder="+1 ან +995..."', 1),
 ],
 "ge/tours-from-moscow/index.html": [
   (" (внутренний паспорт)", "", 1),
 ],
}

def run():
    errs, applied = [], 0
    for f, reps in JOBS.items():
        html = Path(f).read_text(encoding="utf-8")
        local = []
        ok = True
        for old, new, n in reps:
            c = html.count(old)
            if c != n:
                errs.append(f"{f}: [{c}!={n}] {old[:50]!r}"); ok = False; continue
            html = html.replace(old, new); local.append(1)
        if ok:
            Path(f).write_text(html, encoding="utf-8"); applied += len(local)
            print(f"  ✅ {f}: {len(local)} замен")
        else:
            print(f"  ⏭ {f}: пропущен (несовпадение)")
    if errs:
        print("\nОШИБКИ:"); print("\n".join(errs)); sys.exit(1)
    print(f"\nВСЕГО применено: {applied}")

if __name__ == "__main__":
    run()
