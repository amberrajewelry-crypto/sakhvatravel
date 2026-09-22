// Sakhva AI Chat — Follow-up email for abandoned conversations
// Called by n8n cron or manual trigger
// Finds active conversations >24h old with email, sends Brevo email

export const config = { runtime: 'edge' }

const AIRTABLE_BASE = 'appvP72OjZeVJ0XWh'
const TABLE_NAME = 'AI Conversations'

export default async function handler(req) {
  // Accept GET (cron) or POST (n8n webhook)
  const token = process.env.AIRTABLE_TOKEN
  const brevoKey = process.env.BREVO_API_KEY
  if (!token || !brevoKey) {
    return new Response(JSON.stringify({ error: 'missing_keys' }), {
      status: 200, headers: { 'Content-Type': 'application/json' }
    })
  }

  // Optional auth for cron security
  const url = new URL(req.url)
  const secret = url.searchParams.get('secret')
  if (process.env.FOLLOWUP_SECRET && secret !== process.env.FOLLOWUP_SECRET) {
    return new Response(JSON.stringify({ error: 'unauthorized' }), {
      status: 401, headers: { 'Content-Type': 'application/json' }
    })
  }

  try {
    // Find active conversations older than 24h with email
    const cutoff = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString()
    const formula = encodeURIComponent(
      `AND({Status}="active",{Client Email}!="",IS_BEFORE({Last Message},"${cutoff}"),{Booking Created}=FALSE())`
    )
    const searchUrl = `https://api.airtable.com/v0/${AIRTABLE_BASE}/${encodeURIComponent(TABLE_NAME)}?filterByFormula=${formula}&maxRecords=20`

    const searchResp = await fetch(searchUrl, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const searchData = await searchResp.json()
    const records = searchData.records || []

    if (!records.length) {
      return new Response(JSON.stringify({ sent: 0, message: 'No followups needed' }), {
        status: 200, headers: { 'Content-Type': 'application/json' }
      })
    }

    let sent = 0
    for (const rec of records) {
      const f = rec.fields
      const email = f['Client Email']
      const name = f['Client Name'] || ''
      const tours = f['Tours Recommended'] || ''
      const page = f['Source Page'] || ''

      // Build personalized email
      const tourLine = tours
        ? `Вы интересовались: <strong>${tours.split(',').slice(0, 3).join(', ')}</strong>.`
        : 'Вы начали подбирать тур по Грузии.'

      const html = `
<div style="font-family:Georgia,serif;max-width:560px;margin:0 auto;padding:24px">
  <img src="https://sakhva-travel.com/images/logo-green.svg" alt="Sakhva Travel" width="120" style="margin-bottom:20px">
  <h2 style="color:#1A3D2E;font-size:22px;margin-bottom:12px">${name ? name + ', в' : 'В'}аш тур ждёт!</h2>
  <p style="color:#374151;font-size:15px;line-height:1.6">
    ${tourLine} Бронь ещё доступна, и мы держим для вас лучшие даты.
  </p>
  <p style="color:#374151;font-size:15px;line-height:1.6">
    Скидка 10% при группе от 4 человек. Бесплатная отмена за 48 часов.
  </p>
  <div style="text-align:center;margin:28px 0">
    <a href="https://sakhva-travel.com/ekskursiya/?utm_source=followup&utm_medium=email" style="background:#1A3D2E;color:#fff;padding:14px 32px;border-radius:9999px;text-decoration:none;font-size:15px;font-weight:700;display:inline-block">Выбрать тур</a>
  </div>
  <p style="color:#6B7280;font-size:13px;line-height:1.5">
    Или напишите напрямую гиду Тимуру:<br>
    <a href="https://wa.me/995511272623" style="color:#1A3D2E;font-weight:600">WhatsApp</a> ·
    <a href="https://t.me/SakhvaGuideBot" style="color:#1A3D2E;font-weight:600">Telegram</a>
  </p>
  <hr style="border:none;border-top:1px solid #E5E7EB;margin:24px 0">
  <p style="color:#9CA3AF;font-size:11px">
    Sakhva Travel · Тбилиси, Грузия · help@sakhva-travel.com<br>
    Вы получили это письмо потому что начали подбор тура на sakhva-travel.com
  </p>
</div>`

      // Send via Brevo
      const emailResp = await fetch('https://api.brevo.com/v3/smtp/email', {
        method: 'POST',
        headers: {
          'api-key': brevoKey,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          sender: { name: 'Sakhva Travel', email: 'help@sakhva-travel.com' },
          to: [{ email, name: name || email }],
          subject: name
            ? `${name}, ваш тур по Грузии ждёт!`
            : 'Ваш тур по Грузии ждёт!',
          htmlContent: html
        })
      })

      if (emailResp.ok) {
        // Update Airtable status
        await fetch(`https://api.airtable.com/v0/${AIRTABLE_BASE}/${encodeURIComponent(TABLE_NAME)}/${rec.id}`, {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            fields: { 'Status': 'followup_sent' }
          })
        })
        sent++
      }
    }

    return new Response(JSON.stringify({ sent, total: records.length }), {
      status: 200, headers: { 'Content-Type': 'application/json' }
    })

  } catch (e) {
    return new Response(JSON.stringify({ error: 'followup_error' }), {
      status: 200, headers: { 'Content-Type': 'application/json' }
    })
  }
}
