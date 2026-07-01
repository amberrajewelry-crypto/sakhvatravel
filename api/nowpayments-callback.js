// NOWPayments IPN callback
// Webhook URL: https://sakhva-travel.com/api/nowpayments-callback
// Configure in NOWPayments dashboard → Settings → IPN callback URL
// Env vars: NOWPAYMENTS_IPN_SECRET, AIRTABLE_TOKEN, AIRTABLE_BASE_ID, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

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

  const { payment_status, order_id, pay_amount, pay_currency, actually_paid, price_amount, price_currency } = body

  // Only process finished payments
  if (payment_status !== 'finished' && payment_status !== 'confirmed') {
    return new Response('OK', { status: 200 })
  }

  if (!order_id) {
    return new Response('No order_id', { status: 200 })
  }

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
      const tgToken = process.env.TELEGRAM_BOT_TOKEN
      const tgChat = process.env.TELEGRAM_CHAT_ID
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
