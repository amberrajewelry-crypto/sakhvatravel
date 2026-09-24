#!/usr/bin/env python3
"""Локальный preview кластера погоды: статика + /api/weather (реальный Open-Meteo).
Повторяет логику api/weather.js, чтобы виджет работал без vercel dev.
Запуск: python3 scripts/serve-preview.py [port]  → http://localhost:8890/pogoda/
"""
import json, sys, urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEO = {p["slug"]: p for p in json.loads((ROOT / "data" / "pogoda-geo.json").read_text(encoding="utf-8"))}
# опорные точки для прогноза по городам региона (как в api/weather.js, не отдельные страницы)
for k, (nm, la, lo) in {"_khulo": ("Хуло", 41.65, 42.31), "_chiatura": ("Чиатура", 42.29, 43.28),
                        "_zugdidi": ("Зугдиди", 42.51, 41.87), "_omalo": ("Тушети", 42.37, 45.63)}.items():
    GEO[k] = {"slug": k, "name": nm, "lat": la, "lon": lo}
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8890


class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(ROOT), **k)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/api/weather":
            return self.weather(parse_qs(u.query).get("region", [""])[0])
        # чистые URL вида /pogoda/kazbegi/ -> index.html
        if u.path.endswith("/"):
            self.path = u.path + "index.html"
        return super().do_GET()

    def weather(self, region):
        p = GEO.get(region)
        if not p:
            return self.send_json({"error": "unknown_region"}, 400)
        api = ("https://api.open-meteo.com/v1/forecast"
               f"?latitude={p['lat']}&longitude={p['lon']}"
               "&current=temperature_2m,weather_code"
               "&daily=temperature_2m_max,temperature_2m_min,weather_code,precipitation_probability_max"
               "&timezone=Asia%2FTbilisi&forecast_days=14")
        try:
            d = json.load(urllib.request.urlopen(api, timeout=8))
            pp = d["daily"].get("precipitation_probability_max") or []
            daily = [{"date": t, "max": round(d["daily"]["temperature_2m_max"][i]),
                      "min": round(d["daily"]["temperature_2m_min"][i]),
                      "code": d["daily"]["weather_code"][i],
                      "pop": pp[i] if i < len(pp) else None}
                     for i, t in enumerate(d["daily"]["time"])]
            self.send_json({"region": region, "city": p["name"],
                            "current": {"temp": round(d["current"]["temperature_2m"]),
                                        "code": d["current"]["weather_code"],
                                        "time": d["current"].get("time")},
                            "daily": daily})
        except Exception as e:
            self.send_json({"error": "weather_unavailable", "detail": str(e)}, 200)

    def send_json(self, obj, status=200):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def log_message(self, *a):
        pass


print(f"Preview: http://localhost:{PORT}/pogoda/  (Ctrl+C для остановки)")
ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
