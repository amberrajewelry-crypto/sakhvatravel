// TBC Bank payment callback
// Called by TBC after payment completion
// Env vars: AIRTABLE_TOKEN, AIRTABLE_BASE_ID, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

const BASE_ID = process.env.AIRTABLE_BASE_ID || 'appvP72OjZeVJ0XWh'
const BOOKINGS_TABLE = 'tbl0rlhK4KyAMk8UB'

export default async function handler(req, res) {
  let body
  if (req.method === 'POST') {
    body = req.body || {}
  } else {
    body = req.query || {}
  }

  const { PaymentId, Status, Amount, Currency, MerchantPaymentId } = body
  const orderId = MerchantPaymentId || PaymentId || ''
  const isSuccess = Status === 'Succeeded' || Status === 'Confirmed'

  if (!isSuccess || !orderId) {
    return res.status(200).json({ ok: true })
  }

  const token = process.env.AIRTABLE_TOKEN
  if (!token) {
    return res.status(200).json({ ok: true })
  }

  try {
    const formula = encodeURIComponent(`SEARCH("${orderId}",{Заметки})`)
    const searchRes = await fetch(
      `https://api.airtable.com/v0/${BASE_ID}/${BOOKINGS_TABLE}?filterByFormula=${formula}&maxRecords=1`,
      { headers: { 'Authorization': `Bearer ${token}` } }
    )
    const searchData = await searchRes.json()

    if (searchData.records && searchData.records.length > 0) {
      const record = searchData.records[0]

      await fetch(
        `https://api.airtable.com/v0/${BASE_ID}/${BOOKINGS_TABLE}/${record.id}`,
        {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            fields: {
              'Статус': 'оплачена',
              'Заметки': (record.fields['Заметки'] || '') + ` | PAID ${Amount || ''} ${Currency || 'GEL'} via TBC card`
            }
          })
        }
      )

      const tgToken = process.env.TELEGRAM_BOT_TOKEN
      const tgChat = process.env.TELEGRAM_CHAT_ID
      if (tgToken && tgChat) {
        const tourName = record.fields['Тур'] || ''
        const msg = `Оплата картой TBC!\n\n${orderId}\n${tourName}\n${Amount || '?'} ${Currency || 'GEL'}\nСтатус: оплачена`
        await fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ chat_id: tgChat, text: msg })
        }).catch(() => {})
      }
    }
  } catch (e) {
    // Silent
  }

  return res.status(200).json({ ok: true })
}
