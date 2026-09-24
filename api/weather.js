// Live weather for Georgia regions via Open-Meteo (free, no API key).
// Edge-cached 15 min so "now" stays fresh (1h cache made it show stale temps).
// Usage: /api/weather?region=kakheti  → { region, tz, current, daily[] }
// weather_code is WMO; the client maps it to text/emoji per language.

export const config = { runtime: 'edge' }

// Region center points (main city of each region). Kept here, not in the client,
// so pages stay static and one endpoint serves all regions + the hub.
// Coords kept in sync with data/pogoda-geo.json (one source of truth for the cluster).
const REGIONS = {
  // regions
  tbilisi:            { lat: 41.72, lon: 44.79, city: 'Тбилиси' },
  adjara:             { lat: 41.64, lon: 41.64, city: 'Батуми' },
  kakheti:            { lat: 41.92, lon: 45.47, city: 'Телави' },
  imereti:            { lat: 42.27, lon: 42.70, city: 'Кутаиси' },
  'mtskheta-mtianeti':{ lat: 42.66, lon: 44.64, city: 'Степанцминда (Казбеги)' },
  samegrelo:          { lat: 42.51, lon: 41.87, city: 'Зугдиди / Местиа' },
  'samtskhe-javakheti':{ lat: 41.84, lon: 43.40, city: 'Боржоми / Ахалцихе' },
  'shida-kartli':     { lat: 41.98, lon: 44.11, city: 'Гори' },
  'kvemo-kartli':     { lat: 41.55, lon: 45.00, city: 'Дашбаши' },
  guria:              { lat: 41.93, lon: 42.01, city: 'Уреки / Озургети' },
  racha:              { lat: 42.52, lon: 43.15, city: 'Амбролаури' },
  // cities
  batumi:             { lat: 41.64, lon: 41.62, city: 'Батуми' },
  kazbegi:            { lat: 42.66, lon: 44.64, city: 'Степанцминда' },
  kutaisi:            { lat: 42.27, lon: 42.70, city: 'Кутаиси' },
  mestia:             { lat: 43.04, lon: 42.73, city: 'Местиа' },
  gudauri:            { lat: 42.48, lon: 44.48, city: 'Гудаури' },
  bakuriani:          { lat: 41.75, lon: 43.53, city: 'Бакуриани' },
  borjomi:            { lat: 41.84, lon: 43.39, city: 'Боржоми' },
  signagi:            { lat: 41.62, lon: 45.92, city: 'Сигнаги' },
  telavi:             { lat: 41.92, lon: 45.47, city: 'Телави' },
  mtskheta:           { lat: 41.84, lon: 44.72, city: 'Мцхета' },
  // secondary points for region multi-city forecast (not standalone pages)
  _khulo:             { lat: 41.65, lon: 42.31, city: 'Хуло' },
  _chiatura:          { lat: 42.29, lon: 43.28, city: 'Чиатура' },
  _zugdidi:           { lat: 42.51, lon: 41.87, city: 'Зугдиди' },
  _omalo:             { lat: 42.37, lon: 45.63, city: 'Тушети' }
}

export default async function handler(req) {
  const url = new URL(req.url)
  const region = url.searchParams.get('region')
  const r = REGIONS[region]
  if (!r) {
    return json({ error: 'unknown_region', regions: Object.keys(REGIONS) }, 400)
  }

  const api = 'https://api.open-meteo.com/v1/forecast'
    + `?latitude=${r.lat}&longitude=${r.lon}`
    + '&current=temperature_2m,weather_code'
    + '&daily=temperature_2m_max,temperature_2m_min,weather_code,precipitation_probability_max'
    + '&timezone=Asia/Tbilisi&forecast_days=14'

  try {
    const ac = new AbortController()
    const t = setTimeout(() => ac.abort(), 6000)
    const resp = await fetch(api, { signal: ac.signal })
    clearTimeout(t)
    if (!resp.ok) throw new Error('om_' + resp.status)
    const d = await resp.json()

    const daily = (d.daily?.time || []).map((date, i) => ({
      date,
      max: Math.round(d.daily.temperature_2m_max[i]),
      min: Math.round(d.daily.temperature_2m_min[i]),
      code: d.daily.weather_code[i],
      pop: d.daily.precipitation_probability_max?.[i] ?? null
    }))

    return json({
      region, city: r.city, tz: d.timezone,
      current: { temp: Math.round(d.current.temperature_2m), code: d.current.weather_code, time: d.current.time },
      daily
    // success: cache 15 min at the edge; browser gets it fresh.
    }, 200, 's-maxage=900, stale-while-revalidate=1800')
  } catch (e) {
    // Never cache a failure — one transient miss must NOT poison the widget
    // for 15 min. Short s-maxage lets the next call retry Open-Meteo.
    return json({ error: 'weather_unavailable', region }, 200, 's-maxage=15')
  }
}

function json(body, status = 200, cache = 's-maxage=900, stale-while-revalidate=1800') {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': cache
    }
  })
}
