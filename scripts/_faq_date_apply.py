#!/usr/bin/env python3
"""Механическая часть карточной задачи (контент вопросов пишется вручную для каждой карточки).
Usage: python3 scripts/_faq_date_apply.py <file> <questions.json>
questions.json: [{"name":"...","text":"..."}, ...]  (обычно 3 новых вопроса)
Делает: синхронизирует schema FAQPage (добавляет вопросы), добавляет поле cm-date, правит sendContact.
Видимый HTML-FAQ вставляется вручную заранее (Edit), этот скрипт его НЕ трогает.
"""
import re, json, sys

f = sys.argv[1]
new_q = json.load(open(sys.argv[2]))
h = open(f).read()

def qobj(q):
    return {"@type": "Question", "name": q["name"],
            "acceptedAnswer": {"@type": "Answer", "text": q["text"]}}

m = re.search(r'(\{"@context":"https://schema\.org","@type":"FAQPage","mainEntity":\[)(.*?)(\]\})', h, re.S)
if not m:
    sys.exit("FAQPage schema not found")
cnt = m.group(2).count('"@type":"Question"')
add = ",".join(json.dumps(qobj(q), ensure_ascii=False) for q in new_q)
h = h[:m.start()] + m.group(1) + m.group(2) + "," + add + m.group(3) + h[m.end():]

phone_div = '<div style="display:flex;flex-direction:column;gap:6px;margin-bottom:16px"><label style="font-size:13px;font-weight:600;color:#374151">Телефон или WhatsApp</label><input id="cm-phone" placeholder="+7 или +995..." required="" style="padding:12px 16px;border:1px solid #E5E7EB;border-radius:12px;font-size:16px;font-family:inherit;outline:none" type="tel"/></div>'
date_div = '<div style="display:flex;flex-direction:column;gap:6px;margin-bottom:16px"><label style="font-size:13px;font-weight:600;color:#374151">Желаемая дата</label><input id="cm-date" style="padding:12px 16px;border:1px solid #E5E7EB;border-radius:12px;font-size:16px;font-family:inherit;outline:none" type="date"/></div>'
if phone_div not in h:
    sys.exit("cm-phone div not found")
if date_div in h:
    sys.exit("cm-date already present")
h = h.replace(phone_div, phone_div + date_div, 1)

old = "var msg=document.getElementById('cm-msg').value.trim();"
if old not in h:
    sys.exit("sendContact msg var not found")
h = h.replace(old, old + "var dEl=document.getElementById('cm-date');var d=dEl&&dEl.value?dEl.value:'';", 1)
h = h.replace("note:msg||'Tour discount form'", "note:(d?'Желаемая дата: '+d+'. ':'')+(msg||'Tour discount form')", 1)
h = h.replace("message:msg})", "message:msg,date:d})", 1)

open(f, "w").write(h)
print(f"OK schema {cnt}->{cnt+len(new_q)}")
