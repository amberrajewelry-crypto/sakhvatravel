import { tgFan } from './_tgfan.js'
// Email subscription: Brevo + Airtable
// Env vars: BREVO_API_KEY, AIRTABLE_TOKEN, AIRTABLE_BASE_ID

import { notifyBot } from './_bot.js'

export const config = { runtime: 'edge' }

const BASE_ID = process.env.AIRTABLE_BASE_ID || 'appvP72OjZeVJ0XWh'
const CLIENTS_TABLE = 'tblI8B0GUqQtGatWp'

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

  const { email, lang, source } = body
  if (!email || !email.includes('@')) {
    return new Response(JSON.stringify({ error: 'Invalid email' }), { status: 400, headers: corsHeaders })
  }

  const src = source || 'lead-magnet'
  const results = { telegram: false, brevo: false, airtable: false }

  // 1. Telegram notification
  const tgToken = (process.env.TELEGRAM_MANAGER_TOKEN || process.env.TELEGRAM_BOT_TOKEN)
  const tgChat = (process.env.TELEGRAM_MANAGER_CHAT || process.env.TELEGRAM_CHAT_ID)
  results.telegram = await notifyBot('subscribe', { email, lang: lang || 'ru', source: src })
  if (!results.telegram && tgToken && tgChat) {
    try {
      const text = `📩 Новый email\n\n${email}\nИсточник: ${src}\nЯзык: ${lang || 'ru'}`
      await tgFan(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: tgChat, text })
      })
      results.telegram = true
    } catch (e) {
      console.error('Telegram error:', e.message)
    }
  }

  // 2. Brevo — add contact + trigger double opt-in
  const brevoKey = process.env.BREVO_API_KEY
  if (brevoKey) {
    try {
      const res = await fetch('https://api.brevo.com/v3/contacts', {
        method: 'POST',
        headers: {
          'api-key': brevoKey,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email,
          attributes: { LANG: lang || 'ru', SOURCE: src },
          listIds: [3], // Sakhva Subscribers
          updateEnabled: true
        })
      })
      results.brevo = res.ok || res.status === 204
      // 409 = contact already exists, still ok
      if (res.status === 409) results.brevo = true
    } catch (e) {
      console.error('Brevo error:', e.message)
    }
  }

  // 2. Airtable — save to Clients table
  const airtableToken = process.env.AIRTABLE_TOKEN
  if (airtableToken) {
    try {
      const today = new Date().toISOString().split('T')[0]
      const res = await fetch(
        `https://api.airtable.com/v0/${BASE_ID}/${CLIENTS_TABLE}`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${airtableToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            fields: {
              'Email': email,
              'Источник': src,
              'Статус': 'подписчик',
              'Дата первого контакта': today
            }
          })
        }
      )
      results.airtable = res.ok
    } catch (e) {
      console.error('Airtable error:', e.message)
    }
  }

  return new Response(
    JSON.stringify({ ok: true, ...results }),
    { status: 200, headers: corsHeaders }
  )
}
