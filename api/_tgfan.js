// Fan-out for manager alerts: one sendMessage → both bots (whatsapp_manager via
// TELEGRAM_MANAGER_TOKEN and the client bot @SakhvaGuideBot via TELEGRAM_BOT_TOKEN).
// Drop-in for fetch(): returns the primary response, mirrors to the second bot.
export async function tgFan(url, opts) {
  const res = await fetch(url, opts)
  const mgr = process.env.TELEGRAM_MANAGER_TOKEN
  const bot = process.env.TELEGRAM_BOT_TOKEN
  const chat = process.env.TELEGRAM_CHAT_ID
  if (mgr && bot && chat && url.includes(mgr)) {
    try {
      const body = JSON.parse(opts?.body || '{}')
      body.chat_id = chat
      await fetch(url.replace(mgr, bot), { ...opts, body: JSON.stringify(body) })
    } catch (e) { console.error('tgFan mirror error:', e.message) }
  }
  return res
}
