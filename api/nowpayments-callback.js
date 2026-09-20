// NOWPayments IPN callback
// Webhook URL: https://sakhva-travel.com/api/nowpayments-callback
// Configure in NOWPayments dashboard → Settings → IPN callback URL
// Env vars: NOWPAYMENTS_IPN_SECRET, AIRTABLE_TOKEN, AIRTABLE_BASE_ID, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

import { notifyBot } from './_bot.js'

export const config = { runtime: 'edge' }

const BASE_ID = process.env.AIRTABLE_BASE_ID || 'appvP72OjZeVJ0XWh'
const BOOKINGS_TABLE = 'tbl0rlhK4KyAMk8UB'

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response('OK', { status: 200 })
  }

  let body
  try {
    body = await req.json()
  } catch {
    return new Response('Invalid JSON', { status: 400 })
  }

  // --- Authoritative verification (no shared secret / dashboard step needed) ---
  // Never trust the callback body. Re-fetch the payment straight from the
  // NOWPayments API with our server-side API key and act only on THAT status.
  // A forged callback carries a bogus/absent payment_id or a not-yet-finished
  // payment — both rejected here.
  const apiKey = process.env.NOWPAYMENTS_API_KEY
  if (!apiKey) {
    return new Response('Not configured', { status: 500 })
  }
  const paymentId = body.payment_id || body.paymentId
  if (!paymentId) {
    return new Response('No payment_id', { status: 200 })
  }
  let vp
  try {
    const vr = await fetch(`https://api.nowpayments.io/v1/payment/${encodeURIComponent(paymentId)}`, {
      headers: { 'x-api-key': apiKey }
    })
    if (!vr.ok) {
      return new Response('Verification failed', { status: 401 })
    }
    vp = await vr.json()
  } catch {
    return new Response('Verification error', { status: 502 })
  }

  // Bind the verified payment to the booking; trust API values only.
  if (body.order_id && vp.order_id && String(vp.order_id) !== String(body.order_id)) {
    return new Response('Order mismatch', { status: 401 })
  }
  const payment_status = vp.payment_status
  const order_id = vp.order_id || body.order_id
  const pay_amount = vp.pay_amount
  const pay_currency = vp.pay_currency
  const actually_paid = vp.actually_paid
  const price_amount = vp.price_amount
  const price_currency = vp.price_currency

  // Only process finished payments
  if (payment_status !== 'finished' && payment_status !== 'confirmed') {
    return new Response('OK', { status: 200 })
  }

  if (!order_id) {
    return new Response('No order_id', { status: 200 })
  }

  // бот-менеджер: карточка + WhatsApp-ваучер клиенту (привязка к брони по orderId)
  await notifyBot('payment', { orderId: order_id, amount: price_amount, currency: price_currency,
    note: `crypto ${actually_paid || pay_amount} ${pay_currency || ''}` })

  const token = process.env.AIRTABLE_TOKEN
  if (!token) {
    return new Response('OK', { status: 200 })
  }

  try {
    // Find booking by orderId in notes
    const formula = encodeURIComponent(`SEARCH("${order_id}",{Заметки})`)
    const searchRes = await fetch(
      `https://api.airtable.com/v0/${BASE_ID}/${BOOKINGS_TABLE}?filterByFormula=${formula}&maxRecords=1`,
      { headers: { 'Authorization': `Bearer ${token}` } }
    )
    const searchData = await searchRes.json()

    if (searchData.records && searchData.records.length > 0) {
      const record = searchData.records[0]
      const recordId = record.id
      const tourName = record.fields['Тур'] || 'Unknown'

      // Update booking status to "оплачена"
      await fetch(
        `https://api.airtable.com/v0/${BASE_ID}/${BOOKINGS_TABLE}/${recordId}`,
        {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            fields: {
              'Статус': 'оплачена',
              'Заметки': (record.fields['Заметки'] || '') + ` | PAID ${actually_paid || pay_amount} ${pay_currency || price_currency} via crypto`
            }
          })
        }
      )

      // Telegram notification
      const tgToken = (process.env.TELEGRAM_MANAGER_TOKEN || process.env.TELEGRAM_BOT_TOKEN)
      const tgChat = (process.env.TELEGRAM_MANAGER_CHAT || process.env.TELEGRAM_CHAT_ID)
      if (tgToken && tgChat) {
        const msg = `💰 Крипто-оплата получена!\n\n🔖 ${order_id}\n🚐 ${tourName}\n💵 ${actually_paid || pay_amount} ${pay_currency || price_currency}\n💲 Сумма: ${price_amount} ${price_currency}\n✅ Статус: оплачена`
        await fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ chat_id: tgChat, text: msg })
        }).catch(() => {})
      }
    }
  } catch (e) {
    // Silent fail — NOWPayments will retry
  }

  return new Response('OK', { status: 200 })
}
