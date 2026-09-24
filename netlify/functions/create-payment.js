// NOWPayments invoice creation (Netlify Function)
exports.handler = async function(event) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: JSON.stringify({ error: 'Method not allowed' }) }
  }

  const apiKey = process.env.NOWPAYMENTS_API_KEY
  if (!apiKey) {
    return { statusCode: 503, body: JSON.stringify({ error: 'Payment not configured' }) }
  }

  let body
  try {
    body = JSON.parse(event.body)
  } catch {
    return { statusCode: 400, body: JSON.stringify({ error: 'Invalid JSON' }) }
  }

  const { amount, description, orderId } = body
  if (!amount || !orderId) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Missing required fields' }) }
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
        success_url: `${siteUrl}/?payment=success`,
        cancel_url: `${siteUrl}/?payment=cancel`
      })
    })

    const data = await res.json()

    if (!res.ok) {
      return { statusCode: 502, body: JSON.stringify({ error: data.message || 'NOWPayments error' }) }
    }

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ invoiceUrl: data.invoice_url })
    }
  } catch (e) {
    return { statusCode: 500, body: JSON.stringify({ error: e.message }) }
  }
}
