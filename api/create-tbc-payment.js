// TBC Bank E-Commerce payment creation
// Docs: https://developers.tbcbank.ge/reference/tbc-checkout-api-overview
// Production base: https://api.tbcbank.ge/v1/tpay/
//
// Env vars (Vercel dashboard):
//   TBC_CLIENT_ID     — merchant credentials from TBC Checkout Dashboard
//   TBC_CLIENT_SECRET — merchant credentials from TBC Checkout Dashboard
//   TBC_API_KEY       — developer app key from myapps.tbcbank.ge

const TBC_BASE = 'https://api.tbcbank.ge/v1/tpay'

async function getAccessToken(clientId, clientSecret, apiKey) {
  const res = await fetch(`${TBC_BASE}/access-token`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'apikey': apiKey
    },
    body: `client_id=${clientId}&client_secret=${clientSecret}`
  })
  const text = await res.text()
  if (!res.ok) {
    throw new Error(`TBC token error ${res.status}: ${text.substring(0, 300)}`)
  }
  let data
  try { data = JSON.parse(text) } catch { throw new Error(`TBC token not JSON: ${text.substring(0, 300)}`) }
  if (!data.access_token) throw new Error(`TBC no token in response: ${text.substring(0, 300)}`)
  return data.access_token
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const clientId = process.env.TBC_CLIENT_ID
  const clientSecret = process.env.TBC_CLIENT_SECRET
  const apiKey = process.env.TBC_API_KEY

  if (!clientId || !clientSecret || !apiKey) {
    return res.status(503).json({ error: 'TBC payment not configured' })
  }

  const { amount, description, orderId, email } = req.body || {}
  if (!amount || !orderId) {
    return res.status(400).json({ error: 'Missing amount or orderId' })
  }

  const siteUrl = process.env.SITE_URL || 'https://sakhva-travel.com'

  try {
    const token = await getAccessToken(clientId, clientSecret, apiKey)

    const paymentRes = await fetch(`${TBC_BASE}/payments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'apikey': apiKey,
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        amount: {
          currency: 'GEL',
          total: amount,
          subTotal: amount,
          tax: 0,
          shipping: 0
        },
        returnurl: `${siteUrl}/payment-success.html?order_id=${orderId}&amount=${amount}&tour=${encodeURIComponent(description || '')}`,
        extra: orderId,
        expirationMinutes: 30,
        methods: [5],
        installmentProducts: [],
        callbackUrl: `${siteUrl}/api/tbc-callback/`,
        preAuth: false,
        language: 'KA',
        merchantPaymentId: orderId,
        saveCard: false
      })
    })

    if (!paymentRes.ok) {
      const errText = await paymentRes.text()
      return res.status(502).json({ error: 'TBC payment creation failed', details: errText })
    }

    const paymentData = await paymentRes.json()
    const redirectUrl = paymentData.links
      ? paymentData.links.find(l => l.rel === 'redirect')?.uri
      : null

    return res.status(200).json({
      payId: paymentData.payId,
      httpStatusCode: paymentData.httpStatusCode,
      links: paymentData.links,
      redirectUrl
    })

  } catch (err) {
    return res.status(500).json({ error: err.message })
  }
}
