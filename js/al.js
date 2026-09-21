/* auto-open the locale matching the visitor's device language.
   Runs once per session, on first visit only. Bots and users who have
   already picked a language manually (lang_pref cookie) are excluded so
   SEO indexation of /en/ and /ge/ is never broken. */
(function(){try{
  if(/bot|crawl|spider|slurp|bing|google|yandex|lighthouse|pagespeed|duckduck|baidu|facebookexternalhit|embedly|telegram|whatsapp/i.test(navigator.userAgent||''))return;
  if(navigator.webdriver)return;if(/lang_pref=/.test(document.cookie))return;
  if(sessionStorage.getItem('lredir'))return;
  sessionStorage.setItem('lredir','1');
  var n=(navigator.language||'').slice(0,2).toLowerCase();
  var w=n==='ka'?'ka':n==='ru'?'ru':n==='en'?'en':'';
  if(!w||w===document.documentElement.lang)return;
  var l=document.querySelector('link[rel="alternate"][hreflang="'+w+'"]');
  if(l&&l.href)location.replace(l.href);
}catch(e){}})();
