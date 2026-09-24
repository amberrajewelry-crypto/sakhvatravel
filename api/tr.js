// Machine translation for the phrasebook translators. GET /api/tr?sl=ru&tl=ka&q=... -> {"text": "..."}
// Google (dict-chrome-ex client) first, MyMemory as fallback. Cached on the CDN.
export const config = { runtime: 'edge' }

const LANGS = new Set(['ru', 'en', 'ka'])
const MAX_LEN = 200

async function google(q, sl, tl) {
  const u = `https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=${sl}&tl=${tl}&q=${encodeURIComponent(q)}`
  const r = await fetch(u, { headers: { 'User-Agent': 'Mozilla/5.0' } })
  if (!r.ok) throw new Error(`google ${r.status}`)
  const d = await r.json()
  const t = Array.isArray(d) ? (Array.isArray(d[0]) ? d[0][0] : d[0]) : null
  if (typeof t !== 'string' || !t) throw new Error('google empty')
  return t
}

async function mymemory(q, sl, tl) {
  const r = await fetch(`https://api.mymemory.translated.net/get?q=${encodeURIComponent(q)}&langpair=${sl}|${tl}`)
  const d = await r.json()
  const t = d?.responseData?.translatedText
  if (!r.ok || typeof t !== 'string' || !t) throw new Error('mymemory failed')
  return t
}

export default async function handler(req) {
  const p = new URL(req.url).searchParams
  const sl = p.get('sl'), tl = p.get('tl')
  const q = (p.get('q') || '').replace(/\s+/g, ' ').trim()
  const json = (body, status, cache) => new Response(JSON.stringify(body), {
    status, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': cache },
  })
  if (!LANGS.has(sl) || !LANGS.has(tl) || sl === tl || !q || q.length > MAX_LEN) {
    return json({ error: 'bad request' }, 400, 'no-store')
  }
  for (const fn of [google, mymemory]) {
    try {
      return json({ text: await fn(q, sl, tl) }, 200, 'public, max-age=86400, s-maxage=2592000')
    } catch (e) { /* try next provider */ }
  }
  return json({ error: 'translation unavailable' }, 502, 'no-store')
}
