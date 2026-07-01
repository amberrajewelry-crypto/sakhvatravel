// Сохранение бронирования: Telegram (primary) + Airtable CRM (secondary)
// Env vars: AIRTABLE_TOKEN, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

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

  let body
  try {
    body = await req.json()
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400, headers: corsHeaders })
  }

  const { name, phone, email, tour, tourDate, guests, note, orderId, payMethod, status: reqStatus, prepay, total } = body
  if (!name || !tour) {
    return new Response(JSON.stringify({ error: 'Missing name or tour' }), { status: 400, headers: corsHeaders })
  }

  const results = { telegram: false, airtable: false }

  // 1. Telegram notification — FIRST, always
  const tgToken = process.env.TELEGRAM_BOT_TOKEN
  const tgChat = process.env.TELEGRAM_CHAT_ID
  if (tgToken && tgChat) {
    const payInfo = payMethod ? `\n💳 Оплата: ${payMethod}` : ''
    const amountInfo = prepay ? `\n💰 Предоплата: ${prepay} GEL (из ${total || '?'} GEL)` : ''
    const orderInfo = orderId ? `\n🔖 ${orderId}` : ''
    const statusIcon = reqStatus === 'подтверждена' ? '✅' : reqStatus === 'ожидает_оплаты_спб' ? '⏳' : '🗓'
    const msg = `${statusIcon} Новая бронь с сайта\n\n👤 ${name}\n📱 ${phone || '—'}\n📧 ${email || '—'}\n🚐 ${tour}\n📅 ${tourDate || '—'}\n👥 ${guests || '?'} чел.${payInfo}${amountInfo}${orderInfo}\n💬 ${note || '—'}`
    try {
      const tgRes = await fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: tgChat, text: msg })
      })
      results.telegram = tgRes.ok
    } catch (e) {
      console.error('Telegram error:', e.message)
    }
  }

  // 2. Airtable CRM — secondary, non-blocking
  const token = process.env.AIRTABLE_TOKEN
  if (token) {
    const today = new Date().toISOString().split('T')[0]
    const airtableHeaders = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }

    try {
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

      if (clientRes.ok) {
        const clientData = await clientRes.json()
        const clientRecordId = clientData.id

        const bookingFields = {
          'Тур': tour,
          'Дата тура': tourDate || null,
          'Кол-во человек': parseInt(guests) || 1,
          'Статус': reqStatus || 'новая',
          'Заметки': [note, orderId ? `orderId: ${orderId}` : '', payMethod ? `pay: ${payMethod}` : ''].filter(Boolean).join(' | '),
          'Клиент': [{ id: clientRecordId }]
        }
        await fetch(
          `https://api.airtable.com/v0/${BASE_ID}/${BOOKINGS_TABLE}`,
          {
            method: 'POST',
            headers: airtableHeaders,
            body: JSON.stringify({ fields: bookingFields })
          }
        )
        results.airtable = true
      } else {
        const errData = await clientRes.json().catch(() => ({}))
        console.error('Airtable error:', JSON.stringify(errData))
      }
    } catch (e) {
      console.error('Airtable exception:', e.message)
    }
  }

  // Return 200 if at least Telegram succeeded
  return new Response(
    JSON.stringify({ ok: results.telegram, ...results }),
    { status: results.telegram ? 200 : 503, headers: corsHeaders }
  )
}
