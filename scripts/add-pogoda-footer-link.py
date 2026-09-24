"""Site-wide footer link to the /pogoda/ hub (ru/en/ge) — 17 pogoda URLs
stayed out of Google's index for 2 weeks; hub was linked from 23 RU pages only."""
import re, glob

LABEL = {"ru": ("/pogoda/", "Погода в Грузии"),
         "en": ("/en/pogoda/", "Weather in Georgia"),
         "ge": ("/ge/pogoda/", "ამინდი საქართველოში")}
SKIP = ("node_modules", "scripts/", ".vercel", "dashboard/", ".bak")

n = miss = 0
for f in glob.glob("**/*.html", recursive=True):
    if any(k in f for k in SKIP):
        continue
    s = open(f).read()
    lang = "en" if f.startswith("en/") else "ge" if f.startswith("ge/") else "ru"
    href, text = LABEL[lang]
    i = s.rfind("<footer")
    if i < 0:
        continue
    j = s.find("</footer>", i)
    ft = s[i:j]
    if f'href="{href}"' in ft:
        continue
    home = "/" if lang == "ru" else f"/{lang}/"
    m = (re.search(rf'<a href="{re.escape(home)}"[^>]*>', ft)
         or re.search(r'<a href="/privacy/"[^>]*>', ft))
    if not m:
        miss += 1; print("no home link:", f); continue
    a = m.group(0)
    link = re.sub(r'href="[^"]*"', f'href="{href}"', a) + text + "</a>"
    s = s[:i] + ft[:m.start()] + link + ft[m.start():] + s[j:]
    open(f, "w").write(s); n += 1
print("added", n, "missed", miss)
