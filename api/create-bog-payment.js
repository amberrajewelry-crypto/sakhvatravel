// Bank of Georgia (BOG) — создание платежа (ecommerce standard process)
// Docs: https://api.bog.ge/docs/en/payments/standard-process/create-order
//
// Flow:
//   1) POST oauth2.bog.ge/.../token  (Basic base64(client_id:client_secret)) → access_token
//   2) POST api.bog.ge/payments/v1/ecommerce/orders (Bearer) → { id, _links.redirect.href }
//
// Env vars (Vercel dashboard + .env.production):
//   BOG_CLIENT_ID      — Public Key из кабинета BOG (Sandbox или прод)
//   BOG_CLIENT_SECRET  — Secret Key из кабинета BOG
//   SITE_URL           — https://sakhva-travel.com (для callback/redirect URLs)
//
// amount приходит из формы в лари (GEL, целое). BOG принимает total_amount в лари (число), НЕ в тетри.

const BOG_AUTH_URL = 'https://oauth2.bog.ge/auth/realms/bog/protocol/openid-connect/token'
const BOG_ORDERS_URL = 'https://api.bog.ge/payments/v1/ecommerce/orders'

async function getAccessToken(clientId, clientSecret) {
  const basic = Buffer.from(`${clientId}:${clientSecret}`).toString('base64')
  const res = await fetch(BOG_AUTH_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${basic}`,
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'grant_type=client_credentials'
  })
  const text = await res.text()
  if (!res.ok) throw new Error(`BOG token error ${res.status}: ${text.substring(0, 300)}`)
  let data
  try { data = JSON.parse(text) } catch { throw new Error(`BOG token not JSON: ${text.substring(0, 300)}`) }
  if (!data.access_token) throw new Error(`BOG no access_token: ${text.substring(0, 300)}`)
  return data.access_token
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const clientId = process.env.BOG_CLIENT_ID
  const clientSecret = process.env.BOG_CLIENT_SECRET
  if (!clientId || !clientSecret) {
    return res.status(503).json({ error: 'BOG payment not configured' })
  }

  const { amount, description, orderId, email, lang } = req.body || {}
  if (!amount || !orderId) {
    return res.status(400).json({ error: 'Missing amount or orderId' })
  }

  const total = Number(amount)
  if (!(total > 0)) {
    return res.status(400).json({ error: 'Invalid amount' })
  }

  const siteUrl = process.env.SITE_URL || 'https://sakhva-travel.com'
  const desc = description || 'Sakhva Travel Tour'
  // BOG checkout supports only ka/en ("Invalid language ru"); RU users get the EN checkout
  const bogLang = lang === 'ka' ? 'ka' : 'en'
  const uiLang = ['ru', 'en', 'ka'].includes(lang) ? lang : 'en'

  try {
    const token = await getAccessToken(clientId, clientSecret)

    const orderRes = await fetch(BOG_ORDERS_URL, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Accept-Language': bogLang,
        'Idempotency-Key': (globalThis.crypto?.randomUUID?.() || String(orderId))
      },
      body: JSON.stringify({
        callback_url: `${siteUrl}/api/bog-callback/`,
        external_order_id: String(orderId),
        purchase_units: {
          currency: 'GEL',
          total_amount: total,
          basket: [
            { product_id: String(orderId), quantity: 1, unit_price: total, description: desc.substring(0, 100) }
          ]
        },
        redirect_urls: {
          success: `${siteUrl}/payment-success.html?order_id=${encodeURIComponent(orderId)}&amount=${total}&lang=${uiLang}`,
          fail: `${siteUrl}/payment-fail.html?order_id=${encodeURIComponent(orderId)}&amount=${total}&lang=${uiLang}`
        },
        payment_method: ['card', 'google_pay', 'apple_pay']
      })
    })

    const text = await orderRes.text()
    if (!orderRes.ok) {
      return res.status(502).json({ error: 'BOG order creation failed', details: text.substring(0, 400) })
    }

    let data
    try { data = JSON.parse(text) } catch { return res.status(502).json({ error: 'BOG order not JSON', details: text.substring(0, 400) }) }

    const redirect = data?._links?.redirect?.href
    if (!redirect) {
      return res.status(502).json({ error: 'BOG no redirect link', details: text.substring(0, 400) })
    }

    // Возвращаем checkout_url — тем же ключом, что ждёт фронт (payWithCard)
    return res.status(200).json({ checkout_url: redirect, order_id: data.id })
  } catch (e) {
    return res.status(500).json({ error: e.message })
  }
}
