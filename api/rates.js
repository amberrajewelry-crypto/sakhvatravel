// GEL exchange rates from National Bank of Georgia (official, free, no key).
// Edge-cached so NBG is hit at most ~once per 6h; clients read from cache instantly.
// Returns GEL-per-unit for USD/EUR/RUB. Price in target currency = priceGEL / gel_per[CUR].
// Fallback to last-known rates if NBG is down — a slightly stale rate beats an error.

export const config = { runtime: 'edge' }

const NBG_URL = 'https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json/'
const WANT = ['USD', 'EUR', 'RUB']

// Last-known snapshot (NBG 2026-09-03) — used only if NBG is unreachable.
const FALLBACK = { date: '2026-09-03', gel_per: { USD: 2.6205, EUR: 3.0314, RUB: 0.0302 } }

export default async function handler() {
  try {
    const ac = new AbortController()
    const t = setTimeout(() => ac.abort(), 4000) // never hang the edge on NBG
    const resp = await fetch(NBG_URL, { signal: ac.signal, headers: { 'Accept': 'application/json' } })
    clearTimeout(t)
    if (!resp.ok) throw new Error('nbg_' + resp.status)

    const data = await resp.json()
    const list = data?.[0]?.currencies || []
    const gel_per = {}
    for (const c of list) {
      if (WANT.includes(c.code) && c.rate && c.quantity) {
        gel_per[c.code] = +(c.rate / c.quantity).toFixed(4)
      }
    }
    if (WANT.some(k => !gel_per[k])) throw new Error('nbg_incomplete')

    return json({ ok: true, source: 'nbg', date: (data[0].date || '').slice(0, 10), gel_per })
  } catch (e) {
    // Stale-but-safe: return fallback, flagged so the client can tell.
    return json({ ok: true, source: 'fallback', stale: true, ...FALLBACK })
  }
}

function json(body) {
  return new Response(JSON.stringify(body), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      // Edge/CDN caches 6h, serves stale up to 24h while revalidating in background.
      'Cache-Control': 's-maxage=21600, stale-while-revalidate=86400'
    }
  })
}
