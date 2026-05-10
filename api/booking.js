// Сохранение бронирования в Airtable CRM
// Env vars: AIRTABLE_TOKEN, AIRTABLE_BASE_ID

export const config = { runtime: 'edge' }

const BASE_ID = process.env.AIRTABLE_BASE_ID || 'appvP72OjZeVJ0XWh'
const CLIENTS_TABLE = 'tblI8B0GUqQtGatWp'   // Клиенты
const BOOKINGS_TABLE = 'tbl0rlhK4KyAMk8UB'  // Бронирования

export default async function handler(req) {
  const corsHeaders = {
    'Access-Control-Allow-Origin': 'https://sakhva-travel.com',
    'Content-Type': 'application/json'
  }

  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders })
  }

  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405, headers: corsHeaders })
  }

  const token = process.env.AIRTABLE_TOKEN
  if (!token) {
    return new Response(JSON.stringify({ error: 'Not configured' }), { status: 503, headers: corsHeaders })
  }

  let body
  try {
    body = await req.json()
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400, headers: corsHeaders })
  }

  const { name, phone, email, tour, tourDate, guests, note } = body
  if (!name || !tour) {
    return new Response(JSON.stringify({ error: 'Missing name or tour' }), { status: 400, headers: corsHeaders })
  }

  const today = new Date().toISOString().split('T')[0]
  const airtableHeaders = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }

  try {
    // 1. Создаём запись в Клиенты
    const clientRes = await fetch(
      `https://api.airtable.com/v0/${BASE_ID}/${CLIENTS_TABLE}`,
      {
        method: 'POST',
        headers: airtableHeaders,
        body: JSON.stringify({
          fields: {
            'Имя': name,
            'Телефон/WhatsApp': phone || '',
            'Email': email || '',
            'Источник': 'Сайт',
            'Маршрут': tour,
            'Дата': tourDate || null,
            'Кол-во': parseInt(guests) || 1,
            'Статус': 'новый',
            'Дата первого контакта': today
          }
        })
      }
    )

    const clientData = await clientRes.json()
    if (!clientRes.ok) {
      console.error('Airtable client error:', JSON.stringify(clientData))
      return new Response(JSON.stringify({ error: 'Airtable error', detail: clientData }), { status: 502, headers: corsHeaders })
    }

    const clientRecordId = clientData.id

    // 2. Создаём запись в Бронирования и связываем с клиентом
    await fetch(
      `https://api.airtable.com/v0/${BASE_ID}/${BOOKINGS_TABLE}`,
      {
        method: 'POST',
        headers: airtableHeaders,
        body: JSON.stringify({
          fields: {
            'Тур': tour,
            'Дата тура': tourDate || null,
            'Кол-во человек': parseInt(guests) || 1,
            'Статус': 'новая',
            'Заметки': note || '',
            'Клиент': [{ id: clientRecordId }]
          }
        })
      }
    )

    // 3. Telegram notification
    const tgToken = process.env.TELEGRAM_BOT_TOKEN
    const tgChat = process.env.TELEGRAM_CHAT_ID
    if (tgToken && tgChat) {
      const msg = `🗓 Новая бронь с сайта\n\n👤 ${name}\n📱 ${phone || '—'}\n📧 ${email || '—'}\n🚐 ${tour}\n📅 ${tourDate || '—'}\n👥 ${guests} чел.\n💬 ${note || '—'}`
      try {
        await fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ chat_id: tgChat, text: msg, parse_mode: 'HTML' })
        })
      } catch (e) { /* silent */ }
    }

    return new Response(JSON.stringify({ ok: true, clientId: clientRecordId }), { headers: corsHeaders })

  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500, headers: corsHeaders })
  }
}
