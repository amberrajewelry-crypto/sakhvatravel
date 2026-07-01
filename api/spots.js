// Available spots per tour/date from Airtable CRM
// Returns: { tourId: { 'YYYY-MM-DD': spotsLeft, ... }, ... }

export const config = { runtime: 'edge' }

const BASE_ID = process.env.AIRTABLE_BASE_ID || 'appvP72OjZeVJ0XWh'
const BOOKINGS_TABLE = 'tbl0rlhK4KyAMk8UB'
const TOURS_TABLE = 'tbl7cP11xh2ixHBNo'
const DEFAULT_MAX = 8

// Map Airtable tour names to site tour IDs
const TOUR_NAME_MAP = {
  'Казбеги за 1 день': 'kazbegi',
  'Казбеги': 'kazbegi',
  'Скрытые места Тбилиси': 'tbilisi-hidden',
  'Старый Тбилиси': 'old-tbilisi',
  'Кахетия': 'kakheti',
  'Кахетия — вино и природа': 'kakheti',
  'Тур для эмигрантов': 'emigrant',
  'Ночной Тбилиси': 'night-tbilisi',
  'Тур + ужин у местных': 'dinner',
  'Советский Тбилиси': 'soviet',
  'Slow Travel 3 дня': 'slow-travel',
  'Тур + фотосессия': 'photo',
  'Digital Nomad Tour': 'digital-nomad',
  'Мцхета': 'mtskheta',
  'Мцхета — древняя столица': 'mtskheta'
}

export default async function handler(req) {
  const headers = {
    'Access-Control-Allow-Origin': 'https://sakhva-travel.com',
    'Content-Type': 'application/json',
    'Cache-Control': 'public, max-age=300'
  }

  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers })
  }

  const token = process.env.AIRTABLE_TOKEN
  if (!token) {
    // No Airtable token — return default availability (all open)
    const url = new URL(req.url)
    const qDate = url.searchParams.get('date')
    if (qDate) {
      return new Response(JSON.stringify({ available: true, spotsLeft: DEFAULT_MAX }), { headers })
    }
    return new Response(JSON.stringify({}), { headers })
  }

  // Quick check mode: ?tour=X&date=YYYY-MM-DD
  const url = new URL(req.url)
  const queryTour = url.searchParams.get('tour')
  const queryDate = url.searchParams.get('date')

  const airtableHeaders = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }

  try {
    // Get max capacity per tour
    const toursRes = await fetch(
      `https://api.airtable.com/v0/${BASE_ID}/${TOURS_TABLE}?fields%5B%5D=Название&fields%5B%5D=Макс.+человек`,
      { headers: airtableHeaders }
    )
    const toursData = await toursRes.json()
    const maxPerTour = {}
    if (toursData.records) {
      for (const r of toursData.records) {
        const name = r.fields['Название']
        const max = r.fields['Макс. человек']
        const id = TOUR_NAME_MAP[name]
        if (id && max) maxPerTour[id] = max
      }
    }

    // Get confirmed bookings for future dates
    const today = new Date().toISOString().split('T')[0]
    const formula = encodeURIComponent(
      `AND({Дата тура}>='${today}',OR({Статус}='подтверждена',{Статус}='новая',{Статус}='оплачена'))`
    )
    const bookingsRes = await fetch(
      `https://api.airtable.com/v0/${BASE_ID}/${BOOKINGS_TABLE}?filterByFormula=${formula}&fields%5B%5D=Тур&fields%5B%5D=Дата+тура&fields%5B%5D=Кол-во+человек`,
      { headers: airtableHeaders }
    )
    const bookingsData = await bookingsRes.json()

    // Aggregate booked guests per tour/date
    const booked = {} // { tourId: { 'YYYY-MM-DD': totalGuests } }
    if (bookingsData.records) {
      for (const r of bookingsData.records) {
        const tourName = r.fields['Тур']
        const date = r.fields['Дата тура']
        const guests = r.fields['Кол-во человек'] || 1
        const tourId = TOUR_NAME_MAP[tourName]
        if (!tourId || !date) continue
        if (!booked[tourId]) booked[tourId] = {}
        booked[tourId][date] = (booked[tourId][date] || 0) + guests
      }
    }

    // Calculate remaining spots
    const spots = {}
    for (const [tourId, dates] of Object.entries(booked)) {
      spots[tourId] = {}
      const max = maxPerTour[tourId] || DEFAULT_MAX
      for (const [date, guestsBooked] of Object.entries(dates)) {
        spots[tourId][date] = Math.max(0, max - guestsBooked)
      }
    }

    // Quick check mode: return single tour/date availability
    if (queryTour && queryDate) {
      // Match tour by name (Airtable stores tour names, not IDs)
      // Look up in booked data
      let spotsLeft = DEFAULT_MAX
      let found = false
      for (const [tourId, dates] of Object.entries(spots)) {
        if (tourId === queryTour) {
          if (dates[queryDate] !== undefined) {
            spotsLeft = dates[queryDate]
            found = true
          }
          break
        }
      }
      // Also check by tour name in bookings directly
      if (!found && bookingsData.records) {
        let totalBooked = 0
        for (const r of bookingsData.records) {
          const tn = r.fields['Тур'] || ''
          const d = r.fields['Дата тура']
          const g = r.fields['Кол-во человек'] || 1
          if (d === queryDate && tn.toLowerCase().includes(queryTour.replace(/-/g, ' ').substring(0, 6))) {
            totalBooked += g
          }
        }
        if (totalBooked > 0) {
          spotsLeft = Math.max(0, DEFAULT_MAX - totalBooked)
        }
      }
      return new Response(JSON.stringify({
        available: spotsLeft > 0,
        spotsLeft,
        tour: queryTour,
        date: queryDate
      }), { headers })
    }

    return new Response(JSON.stringify(spots), { headers })
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500, headers })
  }
}
