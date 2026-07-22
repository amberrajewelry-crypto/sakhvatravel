#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Перевод интерактивной модалки главной GE (чат/тур-модалка/booking/квиз/оплата).
Отложена спекой как EN-фолбэк; здесь доводим до 100%. Якоря — ТОЛЬКО HTML
(`>текст<`, `placeholder=`, `aria-label=`, `data-label=`), инлайн-JS/CSS не
трогаем (короткие слова from/Back — ловушки для bare-replace). Счётчик: 0 → стоп."""
import re, sys
from pathlib import Path

FILE = "ge/index.html"
R = []
def add(old, new, n=1): R.append((old, new, n))

# --- ЧАТ-ВИДЖЕТ ---
add('aria-label="Close chat"', 'aria-label="ჩატის დახურვა"')
add('>Sakhva Travel — AI assistant<', '>Sakhva Travel — AI-ასისტენტი<')
add('>Online · responds instantly<', '>ონლაინ · პასუხობს მყისვე<')
add('>💰 Prices</button>', '>💰 ფასები</button>')
add('>🗺 Tours</button>', '>🗺 ტურები</button>')
add('>📅 Booking</button>', '>📅 ჯავშანი</button>')
add('>✈️ Visa</button>', '>✈️ ვიზა</button>')
add('placeholder="Type your question..."', 'placeholder="დაწერეთ თქვენი კითხვა..."')
add('aria-label="Your question"', 'aria-label="თქვენი კითხვა"')
add('aria-label="Send message"', 'aria-label="შეტყობინების გაგზავნა"')

# --- МУЗЫКА ---
add('aria-label="Music" data-label="Sound"', 'aria-label="მუსიკა" data-label="ხმა"')

# --- ТУР-МОДАЛКА ---
add('aria-label="Tour details"', 'aria-label="ტურის დეტალები"')
add('>Available</span>', '>ხელმისაწვდომია</span>')
add('>What\'s included</div>', '>რა შედის</div>')
add('>Route / Program</div>', '>მარშრუტი / პროგრამა</div>')
add('>from <span', '>ფასი <span')            # tm-price: "from <span id=tm-gel>"
add('<small>/person</small>', '<small>/ადამიანი</small>')
add('>Write on WhatsApp<', '>მისწერეთ WhatsApp-ზე<')

# --- BOOKING-МОДАЛКА ---
add('>Online booking</div>', '>ონლაინ ჯავშანი</div>')
add('aria-label="←"', 'aria-label="←"', 1)   # без изменения (символ)
add('>Step 1 of 3</div>', '>ნაბიჯი 1 / 3</div>')
add('>Step 2 of 3</div>', '>ნაბიჯი 2 / 3</div>')
add('>Step 3 of 3</div>', '>ნაბიჯი 3 / 3</div>')
add('>Choose date →</button>', '>აირჩიეთ თარიღი →</button>')
add('>Choose a date<', '>აირჩიეთ თარიღი<')
add('>Many spots<', '>ბევრი ადგილი<')
add('>Few spots<', '>რამდენიმე ადგილი<')
add('>Last spots<', '>ბოლო ადგილები<')
add('>No spots<', '>ადგილები არ არის<')
add('>Next →</button>', '>შემდეგი →</button>')
add('>← Back</button>', '>← უკან</button>', 2)   # bm-back шаг1 + шаг2
add('>Your details</div>', '>თქვენი მონაცემები</div>')
add('placeholder="Name"', 'placeholder="სახელი"', 2)   # bm + cm
add('placeholder="your@email.com"', 'placeholder="your@email.com"', 1)
add('placeholder="+7 / +995..."', 'placeholder="+7 / +995..."', 1)
add('>People</label>', '>ადამიანები</label>', 0) if False else None
add('>Book now →</button>', '>დაჯავშნა →</button>')
add('>🔒 Free cancellation 24h · Pay on tour day<', '>🔒 უფასო გაუქმება 24სთ · გადახდა ტურის დღეს<')
add('>Request received!<', '>მოთხოვნა მიღებულია!<')
add('>Prepayment 10% on booking, remainder — on tour day<', '>წინასწარი გადახდა 10% დაჯავშნისას, დანარჩენი — ტურის დღეს<')
add('>Payment: cash, card or Revolut / Wise<', '>გადახდა: ნაღდი, ბარათი ან Revolut / Wise<')
add('>Pay online</', '>გადაიხადეთ ონლაინ</')

# --- ОПЛАТА ---
add('>QR code payment</', '>QR-კოდით გადახდა</')
add('>Fast transfer via QR payment system<', '>სწრაფი გადარიცხვა QR-გადახდის სისტემით<')
add('>Cryptocurrency</', '>კრიპტოვალუტა</')
add('>SWIFT / Wise transfer</', '>SWIFT / Wise გადარიცხვა</', 2)   # pm-opt + pm-screen-title
add('>International transfer in any currency<', '>საერთაშორისო გადარიცხვა ნებისმიერ ვალუტაში<')
add('>QR payment</', '>QR-გადახდა</')
add('>Scan QR code with your phone camera or banking app<', '>დაასკანერეთ QR-კოდი ტელეფონის კამერით ან საბანკო აპლიკაციით<')
add('>After payment send receipt to WhatsApp<', '>გადახდის შემდეგ გამოაგზავნეთ ქვითარი WhatsApp-ზე<')
add(' Send receipt to WhatsApp</a>', ' ქვითრის გაგზავნა WhatsApp-ზე</a>')
add('>Cryptocurrency payment</', '>კრიპტოვალუტით გადახდა</')
add('>We accept: BTC, ETH, USDT<', '>ვიღებთ: BTC, ETH, USDT<')
add('>Note: cryptocurrency payments are non-refundable<', '>გაითვალისწინეთ: კრიპტოგადახდები დაბრუნებას არ ექვემდებარება<')
add('>I understand that cryptocurrency payments are irreversible<', '>ვაცნობიერებ, რომ კრიპტოგადახდები შეუქცევადია<')
add('>Create invoice<', '>ინვოისის შექმნა<')
add('>Rate locked for 20 minutes<', '>კურსი ფიქსირდება 20 წუთით<')
add('>Transfer the amount via Wise — automatic conversion, no hidden fees<', '>გადარიცხეთ თანხა Wise-ით — ავტომატური კონვერტაცია, ფარული საკომისიოს გარეშე<')
add('>Open Wise<', '>Wise-ის გახსნა<')
add('>After payment send confirmation to WhatsApp<', '>გადახდის შემდეგ გამოაგზავნეთ დადასტურება WhatsApp-ზე<')
add(' Send confirmation</a>', ' დადასტურების გაგზავნა</a>')
add('>Choose your payment method<', '>აირჩიეთ გადახდის მეთოდი<')

# --- КОНТАКТ-МОДАЛКА ---
add('aria-label="Contact us"', 'aria-label="დაგვიკავშირდით"')
add('>Contact Timur</', '>დაუკავშირდით თიმურს</')
add('>Leave your contact — Timur will contact you<', '>დატოვეთ კონტაქტი — თიმური დაგიკავშირდებათ<')
add('placeholder="+7 or +995..."', 'placeholder="+7 ან +995..."')
add('placeholder="Dates, number of people, questions..."', 'placeholder="თარიღები, ადამიანების რაოდენობა, კითხვები..."')
add('>Send →</button>', '>გაგზავნა →</button>')
add('>Request sent</', '>მოთხოვნა გაგზავნილია</')
add('>Timur will contact you shortly<', '>თიმური მალე დაგიკავშირდებათ<')

# --- КВИЗ ---
add('aria-label="Quiz"', 'aria-label="ქვიზი"', 0) if False else None
add('>What do you want to see?<', '>რისი ნახვა გსურთ?<')
add('>Choose a direction — we\'ll find the perfect tour<', '>აირჩიეთ მიმართულება — ჩვენ ვიპოვით იდეალურ ტურს<')
add('Mountains & nature</div>', 'მთები და ბუნება</div>')
add('Wine & food</div>', 'ღვინო და საკვები</div>')
add('Old Tbilisi</div>', 'ძველი თბილისი</div>')
add('Active adventure</div>', 'აქტიური თავგადასავალი</div>')
add('A bit of everything — surprise me</div>', 'ცოტა ყველაფრისგან — გამაკვირვეთ</div>')
add('>How much time?<', '>რამდენი დრო?<')
add('>We\'ll adapt the route to your schedule<', '>მარშრუტს თქვენს გრაფიკზე მოვარგებთ<')
add('Half day<br>', 'ნახევარი დღე<br>')
add('>3-5 hours</small>', '>3-5 საათი</small>')
add('Full day<br>', 'სრული დღე<br>')
add('>8-14 hours</small>', '>8-14 საათი</small>')
add('2-3 days</div>', '2-3 დღე</div>')
add('Week+</div>', 'კვირა+</div>')
add('>&larr; Back</button>', '>&larr; უკან</button>', 4)
add('>How many people?<', '>რამდენი ადამიანი?<')
add('>Groups up to 7 people — price per person decreases<', '>ჯგუფები 7 ადამიანამდე — ფასი ერთ ადამიანზე მცირდება<')
add('>Budget per person?<', '>ბიუჯეტი ერთ ადამიანზე?<')
add('>We\'ll help find the best option<', '>დაგეხმარებით საუკეთესო ვარიანტის პოვნაში<')
add('Doesn\'t matter</div>', 'არ აქვს მნიშვნელობა</div>')
add('>Where to send the selection?<', '>სად გამოგიგზავნოთ შერჩევა?<')
add('>Timur will respond within 15 minutes<', '>თიმური უპასუხებს 15 წუთში<')
add('placeholder="Your name"', 'placeholder="თქვენი სახელი"')
add('>Get tour selection</button>', '>მიიღეთ ტურების შერჩევა</button>')
add('>Request sent!<', '>მოთხოვნა გაგზავნილია!<')
add('>Timur will select the best tours and message you<', '>თიმური შეარჩევს საუკეთესო ტურებს და მოგწერთ<')
add('>Back to website<', '>საიტზე დაბრუნება<')

R = [r for r in R if r]

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
    print(f"OK: {len(R)} замен модалки применено")

if __name__ == "__main__":
    run()
