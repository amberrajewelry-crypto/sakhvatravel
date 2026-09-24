// Text-to-speech for the phrasebooks (/razgovornik/, /ge/inglisuri-sasaubro/, /en/georgian-phrasebook/).
// Same Microsoft neural voices as the pre-recorded clips (Edge read-aloud endpoint, protocol as in edge-tts).
// GET /api/say?lang=ka|en|ru&text=... -> audio/mpeg, cached on the CDN for a year.
import { createHash, randomBytes, randomUUID } from 'node:crypto'

const TOKEN = '6A5AA1D4EAFF4E9FB37E23D68491D6F4'
const CHROMIUM = '143.0.3650.75'
const MAJOR = CHROMIUM.split('.')[0]
const VOICES = { ka: 'ka-GE-EkaNeural', en: 'en-US-JennyNeural', ru: 'ru-RU-SvetlanaNeural' }
const MAX_LEN = 200
const WIN_EPOCH = 11644473600
const TIMEOUT_MS = 12000

function secMsGec() {
  let t = Math.floor(Date.now() / 1000) + WIN_EPOCH
  t -= t % 300
  return createHash('sha256').update(`${BigInt(t) * 10000000n}${TOKEN}`).digest('hex').toUpperCase()
}

const esc = s => s.replace(/[<>&'"]/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', "'": '&apos;', '"': '&quot;' }[c]))

export function synth(text, voice) {
  const url = 'wss://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1'
    + `?TrustedClientToken=${TOKEN}&Sec-MS-GEC=${secMsGec()}&Sec-MS-GEC-Version=1-${CHROMIUM}`
    + `&ConnectionId=${randomUUID().replace(/-/g, '')}`
  const ws = new WebSocket(url, {
    headers: {
      Pragma: 'no-cache', 'Cache-Control': 'no-cache',
      Origin: 'chrome-extension://jdiccldimpdaibmpdkjnbmckianbfold',
      'User-Agent': `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${MAJOR}.0.0.0 Safari/537.36 Edg/${MAJOR}.0.0.0`,
      'Accept-Language': 'en-US,en;q=0.9',
      Cookie: `muid=${randomBytes(16).toString('hex').toUpperCase()};`,
    },
  })
  ws.binaryType = 'arraybuffer'
  const chunks = []
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => { ws.close(); reject(new Error('tts timeout')) }, TIMEOUT_MS)
    ws.onerror = () => { clearTimeout(timer); reject(new Error('tts socket error')) }
    ws.onopen = () => {
      const ts = new Date().toUTCString()
      ws.send(`X-Timestamp:${ts}\r\nContent-Type:application/json; charset=utf-8\r\nPath:speech.config\r\n\r\n`
        + '{"context":{"synthesis":{"audio":{"metadataoptions":{"sentenceBoundaryEnabled":"false",'
        + '"wordBoundaryEnabled":"false"},"outputFormat":"audio-24khz-48kbitrate-mono-mp3"}}}}\r\n')
      ws.send(`X-RequestId:${randomUUID().replace(/-/g, '')}\r\nContent-Type:application/ssml+xml\r\n`
        + `X-Timestamp:${ts}Z\r\nPath:ssml\r\n\r\n`
        + "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>"
        + `<voice name='${voice}'><prosody pitch='+0Hz' rate='-10%' volume='+0%'>${esc(text)}`
        + '</prosody></voice></speak>')
    }
    ws.onmessage = ({ data }) => {
      if (typeof data === 'string') {
        if (data.includes('Path:turn.end')) {
          clearTimeout(timer); ws.close()
          chunks.length ? resolve(Buffer.concat(chunks)) : reject(new Error('tts empty'))
        }
        return
      }
      const buf = Buffer.from(data)
      const headLen = buf.readUInt16BE(0)
      if (buf.subarray(2, 2 + headLen).toString().includes('Path:audio')) chunks.push(buf.subarray(2 + headLen))
    }
  })
}

export default async function handler(req, res) {
  const { lang = '', text = '' } = req.query
  const voice = VOICES[lang]
  const clean = String(text).replace(/\s+/g, ' ').trim()
  if (!voice || !clean || clean.length > MAX_LEN) return res.status(400).json({ error: 'bad request' })
  try {
    const mp3 = await synth(clean, voice)
    res.setHeader('Content-Type', 'audio/mpeg')
    res.setHeader('Cache-Control', 'public, max-age=86400, s-maxage=31536000, immutable')
    return res.status(200).send(mp3)
  } catch (e) {
    return res.status(502).json({ error: 'tts unavailable' })
  }
}
