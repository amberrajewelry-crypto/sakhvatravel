// Available dates from Airtable "Расписание" table
// Returns: [{ tour, date, time, spotsLeft, status }, ...]

export const config = { runtime: 'edge' }

const BASE_ID = process.env.AIRTABLE_BASE_ID || 'appvP72OjZeVJ0XWh'
const TABLE_ID = 'tblayYXVuLu2GpmKc'

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
    return new Response(JSON.stringify([]), { headers })
  }

  try {
    const today = new Date().toISOString().split('T')[0]
    const formula = encodeURIComponent(
      `AND({Дата}>='${today}',{Статус}!='закрыта')`
    )
    const res = await fetch(
      `https://api.airtable.com/v0/${BASE_ID}/${TABLE_ID}?filterByFormula=${formula}&sort%5B0%5D%5Bfield%5D=Дата&sort%5B0%5D%5Bdirection%5D=asc`,
      { headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' } }
    )
    const data = await res.json()

    const schedule = (data.records || []).map(r => ({
      tour: r.fields['Экскурсия'] || '',
      date: r.fields['Дата'] || '',
      time: r.fields['Время'] || '',
      spotsTotal: r.fields['Мест всего'] || 0,
      spotsBooked: r.fields['Мест занято'] || 0,
      spotsLeft: (r.fields['Мест всего'] || 0) - (r.fields['Мест занято'] || 0),
      status: r.fields['Статус'] || 'открыта'
    }))

    return new Response(JSON.stringify(schedule), { headers })
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500, headers })
  }
}
