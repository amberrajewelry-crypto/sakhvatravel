export function middleware(request) {
  const { pathname } = new URL(request.url)

  // Skip EN pages, static assets, API, Vercel internals
  if (pathname.startsWith('/en/') ||
      pathname.startsWith('/api/') ||
      pathname.startsWith('/_vercel/') ||
      /\.(webp|jpg|jpeg|png|svg|ico|mp4|mp3|woff|woff2|css|js|txt|xml|json|pdf|gz)$/i.test(pathname)) {
    return
  }

  // Check explicit lang cookie (set by JS when user picks language)
  const langCookie = request.cookies.get('lang_pref')?.value
  if (langCookie === 'ru') return
  if (langCookie === 'en') {
    return Response.redirect(
      new URL('/en' + (pathname === '/' ? '/' : pathname), request.url), 302
    )
  }

  // No cookie — parse Accept-Language header
  const acceptLang = (request.headers.get('accept-language') || '').trim()

  // Empty or wildcard = unknown = default to RU (covers Googlebot, bots, curl)
  if (!acceptLang || acceptLang === '*') return

  // Primary language tag: "en-US,en;q=0.9" → "en"
  const primary = acceptLang.split(',')[0].split(';')[0].split('-')[0].toLowerCase()

  // Russian primary → serve RU
  if (primary === 'ru') return

  // Everything else → redirect to EN version
  const enPath = '/en' + (pathname === '/' ? '/' : pathname)
  return Response.redirect(new URL(enPath, request.url), 302)
}

export const config = {
  matcher: ['/((?!en/|api/|images/|fonts/|js/|css/|_vercel/).*)']
}
