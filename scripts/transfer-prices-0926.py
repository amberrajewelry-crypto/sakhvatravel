#!/usr/bin/env python3
"""Transfer prices (Vladimir, 26.09.2026): the "from" price is PER PERSON, the whole car is fixed.
Kazbegi: from ₾190 per person, whole car ₾450. Batumi: from ₾280 per person, whole car ₾650.
Pages said "per car / за автомобиль" for ₾190/₾280, capacity was inconsistent (4 vs 7) and
round-trip "from ₾340" was below the car price — rewritten. Idempotent (exact-string replace).
Run: python3 scripts/transfer-prices-0926.py
"""
import glob
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KZ = ROOT / "en/ekskursiya/kazbegi-transfer-from-tbilisi/index.html"
BT = ROOT / "ekskursiya/transfer-tbilisi-batumi/index.html"

PAGE = {KZ: [
    ("Tbilisi–Kazbegi Transfer 2026 — from ₾190 | Sakhva Travel</title>",
     "Tbilisi–Kazbegi Transfer 2026 — from ₾190 per person | Sakhva Travel</title>"),
    ("Tbilisi to Kazbegi transfer from ₾190. Private car &amp; driver on the Georgian Military Highway, 2.5–3h, up to 4 pax. One-way or round-trip.",
     "Tbilisi to Kazbegi transfer from ₾190 per person or ₾450 for the whole car with driver. Georgian Military Highway, 2.5–3h, door-to-door."),
    ("Tbilisi to Kazbegi Transfer 2026 — Private from ₾190 | Sakhva Travel",
     "Tbilisi to Kazbegi Transfer 2026 — from ₾190 per person | Sakhva Travel"),
    ("Private transfer Tbilisi to Kazbegi (Stepantsminda) from ₾190. Door-to-door, 2.5–3 hours, up to 4 passengers, optional stops. One-way or round-trip.",
     "Transfer Tbilisi to Kazbegi (Stepantsminda) from ₾190 per person, whole car ₾450. Door-to-door, 2.5–3 hours, optional stops."),
    ("Private transfer from Tbilisi to Kazbegi (Stepantsminda) from ₾190 one-way. Door-to-door in a comfortable car, 2.5–3 hours along the Georgian Military Highway, up to 4 passengers, optional photo stops",
     "Transfer from Tbilisi to Kazbegi (Stepantsminda): from ₾190 per person one-way, or ₾450 for the whole car. Door-to-door, 2.5–3 hours along the Georgian Military Highway, optional photo stops"),
    ("A private transfer costs from ₾190 per car one-way (up to 4 passengers) — not per person. Round-trip is from ₾340. A seat",
     "The transfer costs from ₾190 per person one-way, or ₾450 for the whole car with driver. A seat"),
    ("₾190 is one-way Tbilisi to Kazbegi or the reverse. Round-trip with waiting time, or a full day trip with the driver staying, starts from ₾340. Tell us your plan and we quote a fixed price in advance.",
     "₾190 per person and ₾450 per car are one-way prices, Tbilisi to Kazbegi or the reverse. Round-trip with waiting time or a full day with the driver is quoted on request — tell us your plan and we fix the price in advance."),
    ("₾190 is one-way Tbilisi → Kazbegi (or the reverse direction). Round-trip with waiting time, or a full day trip with the driver staying, starts from ₾340 — tell us your plan and we quote a fixed price in advance",
     "₾190 per person and ₾450 per car are one-way prices, Tbilisi → Kazbegi or the reverse. Round-trip with waiting time or a full day with the driver is quoted on request — tell us your plan and we fix the price in advance"),
    ('<span class="stat-lab">private, one-way</span>', '<span class="stat-lab">per person, one-way</span>'),
    ("From ₾190 per car for up to 4 passengers.", "From ₾190 per person, or ₾450 for the whole car."),
    ("from ₾190 per person, up to 4 people. Private guide from Sakhva Travel, direct booking with no agency fees.",
     "from ₾190 per person, or ₾450 for the whole car with a driver. Direct booking with Sakhva Travel, no agency fees."),
    ('color:#6B7280">per car · up to 4</span>', 'color:#6B7280">per person</span>'),
    ("margin-bottom:16px\">Round-trip &amp; airport pickup available</div>",
     "margin-bottom:16px\">Whole car with driver — ₾450 · round-trip on request</div>"),
    ("from ₾190 / car</td>", "from ₾190 / person · ₾450 / car</td>"),
    ("Door-to-door, any time, up to 4 passengers, free stops", "Door-to-door, any time, free stops"),
    ("Our private transfer is a fixed <strong>₾190 per car one-way</strong> — not per person. Up to 4 passengers travel for the same price.",
     "Our transfer is <strong>from ₾190 per person or ₾450 for the whole car</strong>, one-way."),
], BT: [
    ("Трансфер Тбилиси — Батуми 2026: от ₾280 за авто, 5 часов</title>",
     "Трансфер Тбилиси — Батуми 2026: от ₾280 с человека, 5 часов</title>"),
    ("Трансфер Тбилиси — Батуми от ₾280 за машину до 7 человек: 315 км",
     "Трансфер Тбилиси — Батуми от ₾280 с человека или ₾650 за всю машину: 315 км"),
    ("от ₾280 за авто, 5 ч, дверь в дверь", "от ₾280 с человека, 5 ч, дверь в дверь"),
    ("Трансфер Тбилиси — Батуми от ₾280 за машину: 315 км",
     "Трансфер Тбилиси — Батуми от ₾280 с человека или ₾650 за всю машину: 315 км"),
    ("От ₾280 за автомобиль (до 4 человек), а не за человека. Цена фиксируется при бронировании",
     "От ₾280 с человека или ₾650 за всю машину с водителем. Цена фиксируется при бронировании"),
    ("От ₾280 за автомобиль (до 4 человек), а не за человека. Цена фиксированная",
     "От ₾280 с человека или ₾650 за всю машину с водителем. Цена фиксированная"),
    ("цена от ₾280 за автомобиль, 5 часов</h1>", "от ₾280 с человека, ₾650 за машину</h1>"),
    ('color:#6B7280">за авто, до 4 чел</span>', 'color:#6B7280">с человека · машина целиком ₾650</span>'),
    ("<strong>от ₾280 за автомобиль</strong> (до 7 человек, 315 км",
     "<strong>от ₾280 с человека или ₾650 за всю машину</strong> (315 км"),
    ("Трансфер стоит <strong>от 280 лари за автомобиль</strong> (до 4 человек), а не за каждого пассажира — это ключевое отличие от поезда и маршрутки. Для компании или семьи в пересчёте на человека выходит выгодно.",
     "Трансфер стоит <strong>от 280 лари с человека</strong>, машина целиком с водителем — <strong>650 лари</strong>. Для компании из 3–4 человек выгоднее брать машину целиком: 160–220 лари на каждого."),
    ("Дороже в пересчёте на одного при поездке в одиночку, но для семьи или компании из 3–4 человек цена за авто делает его выгоднее поезда — плюс",
     "Дороже поезда: от ₾280 с человека или ₾650 за всю машину (для компании из 3–4 человек — 160–220 лари на каждого), зато"),
    ("от <strong>280 лари</strong> за авто ·", "от <strong>280 лари</strong> с человека · ₾650 за машину ·"),
]}
GLOBAL = [  # repeated snippets across the site
    ("Трансфер Тбилиси — Батуми от ₾280 за автомобиль", "Трансфер Тбилиси — Батуми от ₾280 с человека или ₾650 за всю машину"),
    ("private car with a driver: from ₾190,", "transfer with a driver: from ₾190 per person or ₾450 for the whole car,"),
    ('">private car with a driver</a>: from ₾190, door-to-door pickup, any departure time, up to 4 passengers, free photo stops.',
     '">transfer with a driver</a>: from ₾190 per person or ₾450 for the whole car, door-to-door pickup, any departure time, free photo stops.'),
]


def main():
    missing = []
    for f, pairs in PAGE.items():
        s = f.read_text()
        for old, new in pairs:
            if old in s:
                s = s.replace(old, new)
            elif new not in s:
                missing.append((f.name, old[:60]))
        f.write_text(s)
    n = 0
    for p in glob.glob(str(ROOT / "**/*.html"), recursive=True):
        if "/_archive/" in p or "/node_modules/" in p:
            continue
        s = Path(p).read_text()
        s2 = s
        for old, new in GLOBAL:
            s2 = s2.replace(old, new)
        if s2 != s:
            Path(p).write_text(s2); n += 1
    print("страниц с общими фразами:", n)
    if missing:
        sys.exit(f"не найдено: {missing}")


if __name__ == "__main__":
    main()
