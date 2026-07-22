// Sakhva AI Chat — Airtable conversation logger
// POST: { sessionId, page, messages, clientName?, clientEmail?,
//         clientPhone?, toursRecommended?, booked?, escalated? }
// Upserts into AI Conversations table

export const config = { runtime: 'edge' }

const AIRTABLE_BASE = 'appvP72OjZeVJ0XWh'
const TABLE_NAME = 'AI Conversations'

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response('', { status: 405 })
  }

  // Same-site only (blocks external spam of the conversations table)
  const _o = req.headers.get('origin') || ''
  const _r = req.headers.get('referer') || ''
  if (_o !== 'https://sakhva-travel.com' && !_r.startsWith('https://sakhva-travel.com')) {
    return new Response(JSON.stringify({ error: 'forbidden' }), { status: 403 })
  }

  const token = process.env.AIRTABLE_TOKEN
  if (!token) {
    return new Response(JSON.stringify({ error: 'no_token' }), { status: 200 })
  }

  let body
  try {
    body = await req.json()
  } catch {
    return new Response(JSON.stringify({ error: 'invalid_json' }), { status: 400 })
  }

  const { sessionId, page, messages, clientName, clientEmail,
    clientPhone, toursRecommended, booked, escalated } = body

  if (!sessionId) {
    return new Response(JSON.stringify({ error: 'no_session' }), { status: 400 })
  }

  const now = new Date().toISOString()
  const msgJson = JSON.stringify((messages || []).slice(-30))

  try {
    // Check if session exists
    const searchUrl = `https://api.airtable.com/v0/${AIRTABLE_BASE}/${encodeURIComponent(TABLE_NAME)}?filterByFormula={Session ID}="${sessionId}"&maxRecords=1`
    const searchResp = await fetch(searchUrl, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const searchData = await searchResp.json()
    const existing = searchData.records?.[0]

    const fields = {
      'Session ID': sessionId,
      'Messages': msgJson,
      'Last Message': now
    }
    if (page) fields['Source Page'] = page
    if (clientName) fields['Client Name'] = clientName
    if (clientEmail) fields['Client Email'] = clientEmail
    if (clientPhone) fields['Client Phone'] = clientPhone
    if (toursRecommended) fields['Tours Recommended'] = toursRecommended
    if (booked) fields['Booking Created'] = true
    if (escalated) {
      fields['Escalated'] = true
      fields['Status'] = 'escalated'
    }

    if (existing) {
      // Update existing record
      await fetch(`https://api.airtable.com/v0/${AIRTABLE_BASE}/${encodeURIComponent(TABLE_NAME)}/${existing.id}`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ fields })
      })
    } else {
      // Create new record
      fields['Created'] = now
      fields['Status'] = 'active'
      await fetch(`https://api.airtable.com/v0/${AIRTABLE_BASE}/${encodeURIComponent(TABLE_NAME)}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ fields })
      })
    }

    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })
  } catch (e) {
    return new Response(JSON.stringify({ error: 'airtable_error' }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })
  }
}
