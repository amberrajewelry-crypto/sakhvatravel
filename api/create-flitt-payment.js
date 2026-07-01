// Flitt (ex-Fondy) — создание платежа (checkout)
// Docs: https://docs.flitt.com/api/create-order/  https://docs.flitt.com/api/building-signature/
// Endpoint: POST https://pay.flitt.com/api/checkout/url
//
// Env vars (Vercel dashboard + .env.production):
//   FLITT_MERCHANT_ID  — идентификатор продавца (напр. 4056624)
//   FLITT_PAYMENT_KEY  — «Ключ оплаты» (secret key для подписи). НЕ кредитный ключ.
//   SITE_URL           — https://sakhva-travel.com (для return/callback URLs)
//
// amount приходит из формы в лари (GEL, целое). Flitt принимает сумму в тетри → ×100.

export const config = { runtime: 'edge' }

const FLITT_URL = 'https://pay.flitt.com/api/checkout/url'

// SHA1(hex, lowercase) от secret + значений параметров, отсортированных по ключу, через "|".
// Пустые/отсутствующие параметры и signature исключаются.
async function buildSignature(params, secret) {
  const keys = Object.keys(params)
    .filter(k => k !== 'signature' && params[k] !== '' && params[k] != null)
    .sort()
  const base = [secret, ...keys.map(k => String(params[k]))].join('|')
  const digest = await crypto.subtle.digest('SHA-1', new TextEncoder().encode(base))
  return [...new Uint8Array(digest)].map(b => b.toString(16).padStart(2, '0')).join('')
}

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405 })
  }

  const merchantId = process.env.FLITT_MERCHANT_ID
  const paymentKey = process.env.FLITT_PAYMENT_KEY
  if (!merchantId || !paymentKey) {
    return new Response(JSON.stringify({ error: 'Flitt payment not configured' }), { status: 503 })
  }

  let body
  try {
    body = await req.json()
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400 })
  }

  const { amount, description, orderId, email, lang } = body
  if (!amount || !orderId) {
    return new Response(JSON.stringify({ error: 'Missing amount or orderId' }), { status: 400 })
  }

  const siteUrl = process.env.SITE_URL || 'https://sakhva-travel.com'

  // Параметры заказа. amount → тетри (минимальные единицы GEL).
  const params = {
    merchant_id: Number(merchantId),
    order_id: orderId,
    order_desc: description || 'Sakhva Travel Tour',
    amount: Math.round(Number(amount) * 100),
    currency: 'GEL',
    lang: lang === 'en' ? 'en' : 'ka',
    response_url: `${siteUrl}/api/flitt-return/`,
    server_callback_url: `${siteUrl}/api/flitt-callback/`
  }
  if (email) params.sender_email = email

  params.signature = await buildSignature(params, paymentKey)

  try {
    const res = await fetch(FLITT_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ request: params })
    })

    const data = await res.json().catch(() => ({}))
    const r = data.response || {}

    if (r.response_status !== 'success' || !r.checkout_url) {
      return new Response(
        JSON.stringify({ error: r.error_message || 'Flitt order creation failed', code: r.error_code || null }),
        { status: 502, headers: { 'Content-Type': 'application/json' } }
      )
    }

    return new Response(
      JSON.stringify({ checkout_url: r.checkout_url, payment_id: r.payment_id || null }),
      { headers: { 'Content-Type': 'application/json' } }
    )
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 })
  }
}
