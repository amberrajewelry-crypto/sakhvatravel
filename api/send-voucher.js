// Send booking voucher email via Brevo
// Env vars: BREVO_API_KEY

export const config = { runtime: 'edge' }

const ALLOWED_ORIGIN = 'https://sakhva-travel.com'
function sameOrigin(req) {
  const o = req.headers.get('origin') || ''
  const r = req.headers.get('referer') || ''
  return o === ALLOWED_ORIGIN || r.startsWith(ALLOWED_ORIGIN + '/') || r === ALLOWED_ORIGIN
}

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405, headers: { 'Content-Type': 'application/json' }
    })
  }

  // Only allow calls originating from our own site (blocks abuse of the mailer).
  if (!sameOrigin(req)) {
    return new Response(JSON.stringify({ error: 'Forbidden' }), {
      status: 403, headers: { 'Content-Type': 'application/json' }
    })
  }

  const brevoKey = process.env.BREVO_API_KEY
  if (!brevoKey) {
    return new Response(JSON.stringify({ ok: false, error: 'Email not configured' }), {
      headers: { 'Content-Type': 'application/json' }
    })
  }

  let body
  try { body = await req.json() } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400, headers: { 'Content-Type': 'application/json' } })
  }

  const { email, name, tour, date, guests, prepay, total, orderId } = body
  if (!email || !tour) {
    return new Response(JSON.stringify({ error: 'Missing email or tour' }), { status: 400, headers: { 'Content-Type': 'application/json' } })
  }

  const htmlContent = `
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:'Helvetica Neue',Arial,sans-serif;max-width:560px;margin:0 auto;padding:20px;color:#111827">
  <div style="text-align:center;padding:20px 0;border-bottom:2px solid #1A3D2E">
    <h1 style="color:#1A3D2E;font-size:24px;margin:0">SAKHVA TRAVEL</h1>
    <p style="color:#6B7280;font-size:13px;margin:4px 0 0">Ваучер бронирования</p>
  </div>
  <div style="padding:24px 0">
    <h2 style="color:#1A3D2E;font-size:20px;margin:0 0 16px">Бронь подтверждена!</h2>
    <table style="width:100%;border-collapse:collapse;font-size:15px">
      <tr><td style="padding:10px 0;border-bottom:1px solid #E5E7EB;color:#6B7280;width:140px">Экскурсия</td><td style="padding:10px 0;border-bottom:1px solid #E5E7EB;font-weight:700">${tour}</td></tr>
      <tr><td style="padding:10px 0;border-bottom:1px solid #E5E7EB;color:#6B7280">Дата</td><td style="padding:10px 0;border-bottom:1px solid #E5E7EB;font-weight:700">${date}</td></tr>
      <tr><td style="padding:10px 0;border-bottom:1px solid #E5E7EB;color:#6B7280">Человек</td><td style="padding:10px 0;border-bottom:1px solid #E5E7EB;font-weight:700">${guests}</td></tr>
      <tr><td style="padding:10px 0;border-bottom:1px solid #E5E7EB;color:#6B7280">Предоплата</td><td style="padding:10px 0;border-bottom:1px solid #E5E7EB;font-weight:700;color:#16A34A">${prepay} GEL</td></tr>
      <tr><td style="padding:10px 0;border-bottom:1px solid #E5E7EB;color:#6B7280">Итого</td><td style="padding:10px 0;border-bottom:1px solid #E5E7EB;font-weight:700">${total} GEL</td></tr>
      <tr><td style="padding:10px 0;color:#6B7280">Номер брони</td><td style="padding:10px 0;font-weight:700;font-family:monospace">${orderId}</td></tr>
    </table>
  </div>
  <div style="background:#F0FDF4;border-radius:12px;padding:16px;margin:16px 0">
    <p style="margin:0;font-size:14px;color:#1A3D2E;font-weight:700">Ваш гид: Тимур</p>
    <p style="margin:6px 0 0;font-size:13px;color:#374151">WhatsApp: <a href="https://wa.me/995511272623" style="color:#1A3D2E">+995 511 272 623</a></p>
    <p style="margin:4px 0 0;font-size:13px;color:#374151">Тимур напишет вам за день до экскурсии с деталями маршрута и временем выезда.</p>
  </div>
  <div style="background:#FEF3C7;border-radius:12px;padding:16px;margin:16px 0">
    <p style="margin:0;font-size:13px;color:#92400E"><strong>Остаток ${total - prepay} GEL</strong> — оплачивается гиду в день экскурсии наличными или картой.</p>
  </div>
  <div style="text-align:center;margin:24px 0">
    <a href="https://wa.me/995511272623" style="display:inline-block;background:#1A3D2E;color:#fff;padding:12px 32px;border-radius:9999px;text-decoration:none;font-size:14px;font-weight:700">Написать Тимуру в WhatsApp</a>
  </div>
  <div style="border-top:1px solid #E5E7EB;padding:16px 0 0;text-align:center;font-size:12px;color:#9CA3AF">
    <p style="margin:0">Бесплатная отмена за 48 часов · <a href="https://sakhva-travel.com/policy/" style="color:#6B7280">Политика отмены</a></p>
    <p style="margin:8px 0 0">&copy; 2026 Sakhva Travel · Тбилиси, Грузия</p>
  </div>
</body>
</html>`

  try {
    const res = await fetch('https://api.brevo.com/v3/smtp/email', {
      method: 'POST',
      headers: {
        'api-key': brevoKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        sender: { name: 'Sakhva Travel', email: 'help@sakhva-travel.com' },
        to: [{ email, name: name || '' }],
        subject: `Ваучер: ${tour} — ${date} | Sakhva Travel`,
        htmlContent
      })
    })

    const data = await res.json()
    return new Response(JSON.stringify({ ok: res.ok, messageId: data.messageId }), {
      headers: { 'Content-Type': 'application/json' }
    })
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, error: e.message }), {
      status: 500, headers: { 'Content-Type': 'application/json' }
    })
  }
}
