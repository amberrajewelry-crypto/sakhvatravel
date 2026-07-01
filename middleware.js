// Vercel Edge Middleware — server-side language detection
// Replaces client-side JS redirect, saves LCP + bandwidth

const BOT_UA_RE = /googlebot|yandexbot|bingbot|baiduspider|duckduckbot|slurp|msnbot|ia_archiver|applebot|facebot|twitterbot|linkedinbot|semrushbot|ahrefsbot|dotbot|petalbot|gptbot|chatgpt|claudebot|anthropic|bytespider|amazonbot/i

// Static asset extensions — no redirect needed
const STATIC_EXT_RE = /\.(webp|jpg|jpeg|png|gif|svg|ico|mp4|mp3|woff|woff2|ttf|eot|css|js|txt|xml|json|pdf|gz|map|avif)$/i

// Paths to skip entirely (static dirs, API, verification files, SEO files)
const SKIP_PATH_RE = /^\/(?:en\/|api\/|_vercel\/|images\/|css\/|js\/|fonts\/|\.well-known\/)/i
const SKIP_FILES = new Set([
  '/sitemap.xml',
  '/robots.txt',
  '/llms.txt',
  '/llms-full.txt',
  '/favicon.ico',
  '/favicon.svg',
  '/manifest.json',
  '/sw.js',
])

export function middleware(request) {
  const url = new URL(request.url)
  const { pathname } = url

  // 0. Redirect /ru/ paths to root (ghost URLs in Yandex index)
  if (pathname.startsWith('/ru/')) {
    const newPath = pathname.replace(/^\/ru/, '')
    return Response.redirect(new URL(newPath || '/', request.url), 301)
  }

  // 1. Skip /en/ pages — already on EN version
  // 2. Skip static asset directories
  // 3. Skip known static files (sitemap, robots, etc.)
  // 4. Skip static asset extensions
  if (SKIP_PATH_RE.test(pathname) ||
      SKIP_FILES.has(pathname) ||
      STATIC_EXT_RE.test(pathname)) {
    return
  }

  // 5. Skip crawlers/bots — let them see both versions for indexing
  const ua = request.headers.get('user-agent') || ''
  if (BOT_UA_RE.test(ua)) {
    return
  }

  // 6. Check explicit lang_pref cookie (set by JS language switcher)
  const langCookie = request.cookies.get('lang_pref')?.value
  if (langCookie === 'ru') return
  if (langCookie === 'en') {
    const enPath = '/en' + (pathname === '/' ? '/' : pathname)
    return Response.redirect(new URL(enPath, request.url), 302)
  }

  // 7. No cookie — parse Accept-Language header
  const acceptLang = (request.headers.get('accept-language') || '').trim()

  // Empty or wildcard = unknown = default to RU (safe default, covers curl etc.)
  if (!acceptLang || acceptLang === '*') return

  // Primary language tag: "en-US,en;q=0.9,ru;q=0.8" -> "en"
  const primary = acceptLang.split(',')[0].split(';')[0].split('-')[0].toLowerCase()

  // Russian primary -> serve RU version as-is
  if (primary === 'ru') return

  // Everything else -> 302 redirect to /en/ version
  const enPath = '/en' + (pathname === '/' ? '/' : pathname)
  const response = Response.redirect(new URL(enPath, request.url), 302)
  // Set cookie so we don't redirect again on next visit
  response.headers.append('Set-Cookie', 'lang_pref=en; Path=/; Max-Age=31536000; SameSite=Lax')
  return response
}

export const config = {
  // Matcher excludes static dirs upfront for performance (Vercel skips middleware entirely)
  matcher: ['/((?!en/|api/|images/|fonts/|js/|css/|_vercel/).*)']
}
