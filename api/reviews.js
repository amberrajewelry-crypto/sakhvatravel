// Vercel Serverless Function — Google Places Reviews proxy
// Env vars (set in Vercel dashboard):
//   GOOGLE_PLACES_API_KEY  — ключ с включённым Places API (New)
//   GOOGLE_PLACE_ID        — Place ID бизнеса (напр. ChIJ...)

export const config = { runtime: 'edge' }

const CACHE_TTL = 6 * 60 * 60 * 1000 // 6 часов
let cache = { data: null, ts: 0 }

export default async function handler(req) {
  const origin = req.headers.get('origin') || ''
  const headers = {
    'Access-Control-Allow-Origin': origin.includes('sakhva-travel.com') ? origin : 'https://sakhva-travel.com',
    'Content-Type': 'application/json',
    'Cache-Control': 'public, s-maxage=21600'
  }

  // Serve from memory cache if fresh
  if (cache.data && Date.now() - cache.ts < CACHE_TTL) {
    return new Response(JSON.stringify(cache.data), { headers })
  }

  const apiKey = process.env.GOOGLE_PLACES_API_KEY
  const placeId = process.env.GOOGLE_PLACE_ID

  if (!apiKey || !placeId) {
    return new Response(JSON.stringify({ error: 'not_configured' }), { status: 503, headers })
  }

  try {
    const url = `https://places.googleapis.com/v1/places/${placeId}?fields=rating,userRatingCount,reviews&languageCode=ru&key=${apiKey}`
    const res = await fetch(url, {
      headers: { 'X-Goog-FieldMask': 'rating,userRatingCount,reviews' }
    })
    if (!res.ok) throw new Error(`Places API ${res.status}`)
    const json = await res.json()

    const reviews = (json.reviews || [])
      .filter(r => r.rating >= 4) // только 4-5 звёзд
      .slice(0, 6)
      .map(r => ({
        name: r.authorAttribution?.displayName || 'Турист',
        avatar: r.authorAttribution?.photoUri || null,
        rating: r.rating,
        text: r.text?.text || '',
        time: r.relativePublishTimeDescription || ''
      }))

    const result = {
      rating: json.rating,
      total: json.userRatingCount,
      reviews
    }

    cache = { data: result, ts: Date.now() }
    return new Response(JSON.stringify(result), { headers })
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500, headers })
  }
}
