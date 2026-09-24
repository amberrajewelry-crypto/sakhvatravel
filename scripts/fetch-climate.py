#!/usr/bin/env python3
"""Собирает климат-нормали по месяцам из Open-Meteo archive (10 лет) для точек pogoda-geo.json.
Пишет data/climate.json: {slug: {"1": {"tmax": , "tmin": , "rain": }, ... "12": {...}}}.
tmax/tmin — средние дневные макс/мин по месяцу; rain — среднее число дней с осадками >=1 мм.
Resume: точки, уже присутствующие в climate.json, пропускаются. Пауза 1с между запросами.
"""
import json, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEO = ROOT / "data" / "pogoda-geo.json"
OUT = ROOT / "data" / "climate.json"
START, END = "2014-01-01", "2023-12-31"


def fetch(lat, lon):
    url = ("https://archive-api.open-meteo.com/v1/archive"
           f"?latitude={lat}&longitude={lon}"
           f"&start_date={START}&end_date={END}"
           "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
           "&timezone=Asia%2FTbilisi")
    req = urllib.request.Request(url, headers={"User-Agent": "sakhva-climate/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def normals(d):
    """daily arrays -> per-month averages."""
    dates = d["daily"]["time"]
    tmax = d["daily"]["temperature_2m_max"]
    tmin = d["daily"]["temperature_2m_min"]
    prcp = d["daily"]["precipitation_sum"]
    # accumulate per month
    acc = {m: {"tmax": [], "tmin": [], "wet_by_year": {}} for m in range(1, 13)}
    for i, ds in enumerate(dates):
        m = int(ds[5:7]); y = ds[:4]
        if tmax[i] is not None:
            acc[m]["tmax"].append(tmax[i])
        if tmin[i] is not None:
            acc[m]["tmin"].append(tmin[i])
        if prcp[i] and prcp[i] >= 1.0:
            acc[m]["wet_by_year"][y] = acc[m]["wet_by_year"].get(y, 0) + 1
    res = {}
    for m in range(1, 13):
        tx = acc[m]["tmax"]; tn = acc[m]["tmin"]
        wet = acc[m]["wet_by_year"]
        years = len({ds[:4] for ds in dates if int(ds[5:7]) == m}) or 1
        res[str(m)] = {
            "tmax": round(sum(tx) / len(tx)) if tx else None,
            "tmin": round(sum(tn) / len(tn)) if tn else None,
            "rain": round(sum(wet.values()) / years),
        }
    return res


def main():
    geo = json.loads(GEO.read_text(encoding="utf-8"))
    out = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    for p in geo:
        slug = p["slug"]
        if slug in out:
            print(f"= {slug} (уже есть)")
            continue
        try:
            d = fetch(p["lat"], p["lon"])
            out[slug] = normals(d)
            jan, jul = out[slug]["1"], out[slug]["7"]
            print(f"+ {slug}: янв {jan['tmax']}/{jan['tmin']}  июл {jul['tmax']}/{jul['tmin']}")
            OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        except (urllib.error.URLError, KeyError, ValueError) as e:
            print(f"! {slug}: {e}")
        time.sleep(1)
    print(f"Готово: {len(out)}/{len(geo)} точек -> {OUT}")


if __name__ == "__main__":
    main()
