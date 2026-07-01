// NOWPayments invoice creation
// Env vars (Vercel dashboard):
//   NOWPAYMENTS_API_KEY  — ключ NOWPayments
//   SITE_URL             — https://sakhva-travel.com (для redirect URLs)

export const config = { runtime: 'edge' }

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405 })
  }

  const apiKey = process.env.NOWPAYMENTS_API_KEY
  if (!apiKey) {
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

  try {
    const res = await fetch('https://api.nowpayments.io/v1/invoice', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey
      },
      body: JSON.stringify({
        price_amount: amount,
        price_currency: 'usd',
        order_id: orderId,
        order_description: description || 'Sakhva Travel Tour',
        success_url: `${siteUrl}/payment-success.html?order_id=${orderId}&amount=${amount}&tour=${encodeURIComponent(description || '')}`,
        cancel_url: `${siteUrl}/payment-fail.html?order_id=${orderId}`,
        ipn_callback_url: `${siteUrl}/api/nowpayments-callback`
      })
    })

    const data = await res.json()

    if (!res.ok) {
      return new Response(JSON.stringify({ error: data.message || 'NOWPayments error' }), { status: 502 })
    }

    return new Response(JSON.stringify({ invoiceUrl: data.invoice_url }), {
      headers: { 'Content-Type': 'application/json' }
    })
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 })
  }
}
