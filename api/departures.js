// Ближайшие подтверждённые выезды по направлениям (из базы броней бота) для карточек
// «мини-группа» на главной. Прокси к боту, кэш на edge 10 мин; при сбое — {}.
export const config = { runtime: 'edge' }

export default async function handler() {
  const headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'public, max-age=300, s-maxage=600, stale-while-revalidate=3600'
  }
  try {
    const base = (process.env.BOT_EVENT_URL || 'https://api.sakhva-travel.com/greenwh/site').replace(/\/site$/, '')
    const r = await fetch(`${base}/departures`, { signal: AbortSignal.timeout(8000) })
    const j = await r.json()
    return new Response(JSON.stringify(j.error ? {} : j), { headers })
  } catch {
    return new Response('{}', { headers })
  }
}
