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
/* WhatsApp/Telegram click -> GA4 lead on pages with no other lead tracking.
   chat-widget.js, ui-deferred.js or an inline listener already count it elsewhere: skip there, no doubles. */
document.addEventListener('click',function(e){try{
  var a=e.target.closest&&e.target.closest('a[href*="wa.me"],a[href*="t.me"]');
  if(!a||typeof gtag!=='function')return;
  if(document.querySelector('script[src*="ui-deferred"],script[src*="chat-widget.js"]'))return;
  if([].some.call(document.scripts,function(s){return !s.src&&s.text.indexOf('generate_lead')>-1}))return;
  gtag('event','generate_lead',{event_category:a.href.indexOf('wa.me')>-1?'whatsapp':'telegram',event_label:a.href});
}catch(x){}});
