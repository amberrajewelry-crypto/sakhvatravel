import { tgFan } from './_tgfan.js'
export const config = { runtime: 'edge' }

// Partner application form → Telegram. Env: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
const esc = (s) => String(s).replace(/[<>&]/g, (c) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;' }[c]))

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405 })
  }

  // Same-site only: legit form is a same-origin fetch from sakhva-travel.com.
  // Blocks external scripted abuse (TG/cost flooding). ponytail: origin check is
  // spoofable by a determined attacker — for hard rate-limiting enable Vercel Firewall.
  const ref = req.headers.get('referer') || req.headers.get('origin') || ''
  if (!ref.startsWith('https://sakhva-travel.com')) {
    return new Response(JSON.stringify({ error: 'Forbidden' }), { status: 403 })
  }

  try {
    const b = await req.json()
    // Honeypot: hidden field no human fills. Bots fill every input → silently drop.
    if (String(b.website || '').trim()) {
      return new Response(JSON.stringify({ ok: true }), { status: 200 })
    }
    const name = String(b.name || '').trim().slice(0, 120)
    const contact = String(b.contact || '').trim().slice(0, 160)
    const company = String(b.company || '').trim().slice(0, 160)
    const note = String(b.note || '').trim().slice(0, 1000)
    const lang = ({ ru: 'RU', en: 'EN', ka: 'GE' })[b.lang] || '—'

    if (!name || !contact) {
      return new Response(JSON.stringify({ error: 'name and contact required' }), { status: 400 })
    }

    const token = (process.env.TELEGRAM_MANAGER_TOKEN || process.env.TELEGRAM_BOT_TOKEN)
    const chatId = (process.env.TELEGRAM_MANAGER_CHAT || process.env.TELEGRAM_CHAT_ID)
    if (!token || !chatId) {
      return new Response(JSON.stringify({ error: 'TG not configured' }), { status: 500 })
    }

    let text = `🤝 <b>Заявка в партнёрку</b> [${lang}]\n\n`
    text += `<b>Имя:</b> ${esc(name)}\n<b>Контакт:</b> ${esc(contact)}\n`
    if (company) text += `<b>Компания:</b> ${esc(company)}\n`
    if (note) text += `<b>О себе:</b> ${esc(note)}\n`

    const tgRes = await tgFan(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: chatId, text, parse_mode: 'HTML' }),
    })
    if (!tgRes.ok) {
      console.error('TG error:', await tgRes.text())
      return new Response(JSON.stringify({ error: 'TG send failed' }), { status: 502 })
    }
    return new Response(JSON.stringify({ ok: true }), {
      status: 200, headers: { 'Content-Type': 'application/json' },
    })
  } catch (e) {
    console.error('Partner application error:', e)
    return new Response(JSON.stringify({ error: 'Server error' }), { status: 500 })
  }
}
