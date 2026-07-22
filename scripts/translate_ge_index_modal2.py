#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Второй проход модалки главной GE: label'ы форм bm/cm, pm-back, pm-warning,
music-toast, квиз-хвост. Якоря — точная HTML-разметка (см. grep). Счётчик строгий."""
import sys
from pathlib import Path

FILE = "ge/index.html"
R = []
def add(old, new, n=1): R.append((old, new, n))

add(' Play music</div>', ' მუსიკის ჩართვა</div>')
add('>Choose a tour</div>', '>აირჩიეთ ტური</div>')
add('<label>Name</label>', '<label>სახელი</label>')
add('<label>People</label>', '<label>ადამიანები</label>')
add('<label>Email</label>', '<label>Email</label>')            # keep
add('<label>Phone / WhatsApp</label>', '<label>ტელეფონი / WhatsApp</label>')
add('<label>Preferences (optional)</label>', '<label>სურვილები (არასავალდებულო)</label>')
add('<label>Promo code</label>', '<label>პრომოკოდი</label>', 2)   # bm + cm
add('>Payment</div>', '>გადახდა</div>')
add('Timur will contact you within 2hhours', 'თიმური დაგიკავშირდებათ 2 საათში')
add('>BTC, ETH, USDT — via NOWPayments</div>', '>BTC, ETH, USDT — NOWPayments-ით</div>')
add('<span>Back</span>', '<span>უკან</span>', 3)   # pm-back ×3
add('>Please verify the amount before paying. Once sent, the transaction cannot be reversed.</p>',
    '>გადახდამდე გადაამოწმეთ თანხა. გაგზავნის შემდეგ ტრანზაქცია შეუქცევადია.</p>')
add('<label>Your name</label>', '<label>თქვენი სახელი</label>')
add('<label>Phone or WhatsApp</label>', '<label>ტელეფონი ან WhatsApp</label>')
add('<label>Message (optional)</label>', '<label>შეტყობინება (არასავალდებულო)</label>')
add('within 15 minutes</div>', '15 წუთში</div>')

def run():
    html = Path(FILE).read_text(encoding="utf-8")
    errs = []
    for i, (old, new, n) in enumerate(R):
        c = html.count(old)
        if c != n:
            errs.append(f"[{c}!={n}] #{i} {old[:60]!r}"); continue
        html = html.replace(old, new)
    if errs:
        print("НЕСОВПАДЕНИЕ — запись отменена:"); print("\n".join(errs)); sys.exit(1)
    Path(FILE).write_text(html, encoding="utf-8")
    print(f"OK: {len(R)} замен (проход 2)")

if __name__ == "__main__":
    run()
