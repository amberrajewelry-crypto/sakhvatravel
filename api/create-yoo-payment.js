// YooKassa payment creation
// Env vars (Vercel dashboard):
//   YOOKASSA_SHOP_ID    — shopId из личного кабинета ЮKassa
//   YOOKASSA_SECRET_KEY — секретный ключ
//   SITE_URL            — https://sakhva-travel.com

export const config = { runtime: 'edge' }

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405 })
  }

  const shopId = process.env.YOOKASSA_SHOP_ID
  const secretKey = process.env.YOOKASSA_SECRET_KEY
  if (!shopId || !secretKey) {
    return new Response(JSON.stringify({ error: 'Payment not configured' }), { status: 503 })
  }

  let body
  try {
    body = await req.json()
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400 })
  }

  const { amount, description, orderId } = body
  if (!amount || !orderId) {
    return new Response(JSON.stringify({ error: 'Missing required fields' }), { status: 400 })
  }

  const siteUrl = process.env.SITE_URL || 'https://sakhva-travel.com'
  const credentials = btoa(`${shopId}:${secretKey}`)
  // Идемпотентный ключ — уникальный на каждый запрос
  const idempotenceKey = `${orderId}-${Date.now()}`

  try {
    const res = await fetch('https://api.yookassa.ru/v2/payments', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Basic ${credentials}`,
        'Idempotence-Key': idempotenceKey
      },
      body: JSON.stringify({
        amount: {
          value: String(Number(amount).toFixed(2)),
          currency: 'RUB'
        },
        confirmation: {
          type: 'redirect',
          return_url: `${siteUrl}/?payment=success`
        },
        description: description || 'Тур Sakhva Travel',
        metadata: { order_id: orderId }
      })
    })

    const data = await res.json()

    if (!res.ok) {
      return new Response(JSON.stringify({ error: data.description || 'YooKassa error' }), { status: 502 })
    }

    const confirmationUrl = data.confirmation?.confirmation_url
    if (!confirmationUrl) {
      return new Response(JSON.stringify({ error: 'No confirmation URL returned' }), { status: 502 })
    }

    return new Response(JSON.stringify({ confirmationUrl }), {
      headers: { 'Content-Type': 'application/json' }
    })
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 })
  }
}
