// Sakhva AI Chat Widget v3 — vanilla JS, isolated module
// Features: tour cards, cross-sell, booking draft, proactive open,
//           session memory, page context, Airtable logging

(function() {
  'use strict';

  // Detect UI language. On /en/ pages <html lang="en"> is set server-side.
  // On the homepage the EN switch (main.js setLang) only writes localStorage['lang']
  // without touching <html lang>, so fall back to it.
  function curLang() {
    // Georgian content is ONLY ever rendered under /ge/ (server sets <html lang="ka">).
    // A stale localStorage['lang']='ka' from an earlier /ge/ visit must NOT make the
    // widget speak Georgian on a Russian/English page (the reported bug).
    const htmlLang = document.documentElement.lang;
    const path = location.pathname;
    if (htmlLang === 'ka' || path === '/ge' || path.indexOf('/ge/') === 0) return 'ka';
    if (htmlLang === 'en' || path.indexOf('/en/') === 0) return 'en';
    // Homepage EN switch (main.js) only writes localStorage['lang'] without touching <html lang>.
    // Only the homepage has that client-side switch; every other RU URL is RU-only, so a stale
    // 'en' left by a /en/ visit must not flip the widget there.
    if (path === '/' || path === '/index.html') {
      try { if (localStorage.getItem('lang') === 'en') return 'en'; } catch (e) {}
    }
    return 'ru';
  }

  // Pick a string by current UI language (ru default, en, ka).
  function L(ru, en, ka) {
    const l = curLang();
    return l === 'ka' ? ka : l === 'en' ? en : ru;
  }

  const CFG = {
    api: '/api/chat/',
    name: 'Sakhva-AI',
    color: '#1A3D2E',
    colorLight: '#86EFAC',
    bgBubbleAI: '#F3F4F6',
    greeting: 'Привет! Я Sakhva-AI, помогу подобрать идеальный тур по Грузии за 30 секунд. Расскажите кратко \u2014 кто едет, сколько дней в Тбилиси и что хотите увидеть?',
    quickReplies: [
      'Пара на 4 дня \u2014 вино и виды',
      'Семья с детьми \u2014 спокойно',
      'Я один \u2014 что посмотреть'
    ],
    waLink: 'https://wa.me/995511272623',
    rateLimit: 30,
    storageKey: 'sakhva_chat',
    sessionKey: 'sakhva_sid',
    visitsKey: 'sakhva_visits',
    dismissKey: 'sakhva_dismissed'
  };

  let isOpen = false;
  let history = [];
  let sessionId = '';
  let currentPage = location.pathname;
  let msgCount = 0;
  let msgTimer = null;
  let els = {};

  // ─── UTILS ───
  function uuid() {
    return 'sc-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 8);
  }

  function getSessionId() {
    let sid = '';
    try { sid = localStorage.getItem(CFG.sessionKey) || ''; } catch {}
    if (!sid) {
      sid = uuid();
      try { localStorage.setItem(CFG.sessionKey, sid); } catch {}
    }
    return sid;
  }

  function detectTourContext() {
    const path = location.pathname;
    const m = path.match(/\/ekskursiya\/([^/]+)\//);
    if (m) return m[1];
    return null;
  }

  // ─── CSS ───
  function injectStyles() {
    if (document.getElementById('sc-styles')) return;
    const s = document.createElement('style');
    s.id = 'sc-styles';
    s.textContent = `
.sc-fab{position:fixed;bottom:20px;right:20px;z-index:99990;width:48px;height:48px;border-radius:50%;background:${CFG.color};border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,.15);transition:transform .2s ease,opacity .15s ease;animation:scPulse 3s ease-in-out infinite}
.sc-fab:hover{transform:scale(1.1);animation:none}
.sc-fab svg{width:24px;height:24px;color:${CFG.color}}
.sc-fab-tip{position:absolute;right:60px;top:50%;transform:translateY(-50%);background:#fff;color:#333;font-size:13px;font-weight:500;padding:8px 14px;border-radius:8px;white-space:nowrap;box-shadow:0 2px 8px rgba(0,0,0,.1);opacity:0;pointer-events:none;transition:opacity .2s}
.sc-fab-tip::after{content:'';position:absolute;right:-6px;top:50%;transform:translateY(-50%);border:6px solid transparent;border-left-color:#fff}
.sc-fab:hover .sc-fab-tip{opacity:1}
/* tour pages: #mobile-sticky-bar toggles body.msb-on; keep floating buttons above it */
body.msb-on .sc-fab,body.msb-on #music-toggle{bottom:calc(84px + env(safe-area-inset-bottom,0px))!important}
@keyframes scPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}
@media(max-width:768px){.sc-fab{width:44px;height:44px;bottom:calc(20px + env(safe-area-inset-bottom,0px));right:16px}body.cookie-up .sc-fab{bottom:calc(76px + env(safe-area-inset-bottom,0px))!important}.sc-fab svg{width:20px;height:20px}.sc-fab-tip{display:none}}

.sc-win{position:fixed;bottom:24px;right:24px;z-index:99991;width:288px;height:462px;background:#fff;border-radius:20px;box-shadow:0 8px 40px rgba(0,0,0,.18);display:flex;flex-direction:column;overflow:hidden;transform:scale(.95);opacity:0;pointer-events:none;transition:transform .25s cubic-bezier(.34,1.56,.64,1),opacity .2s ease}
.sc-win.open{transform:scale(1);opacity:1;pointer-events:auto}
@media(max-width:768px){.sc-win{width:56vw;height:42vh;bottom:72px;right:12px;left:auto;border-radius:16px;touch-action:manipulation}.sc-hon{display:none!important}.sc-bbl{font-size:13px!important;padding:8px 10px!important;max-width:none!important}.sc-qr{justify-content:center!important}.sc-qr button{font-size:12px!important;padding:6px 10px!important}.sc-body{padding:10px!important;align-items:stretch!important}.sc-inp{padding:6px 10px!important}.sc-inp input{font-size:16px!important;padding:6px 0!important}.sc-m-av{display:none!important}.sc-msg.ai,.sc-msg.user{max-width:100%!important}.sc-msg.ai .sc-bbl,.sc-msg.user .sc-bbl{max-width:100%!important}.sc-hdr{gap:8px!important;padding:8px 10px!important;height:50px!important}.sc-av{width:32px!important;height:32px!important}.sc-av svg{width:18px!important;height:18px!important}.sc-nm{font-size:13px!important}.sc-st{font-size:12px!important}.sc-x{width:26px!important;height:26px!important}}

.sc-hdr{display:flex;align-items:center;gap:8px;padding:6px 10px;background:${CFG.color};flex-shrink:0;height:44px}
.sc-av{width:34px;height:34px;border-radius:50%;background:rgba(255,255,255,.15);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.sc-av svg{width:26px;height:26px;fill:none}
.sc-inf{flex:1}
.sc-nm{color:#fff;font-size:13px;font-weight:700;line-height:1.2}
.sc-st{color:${CFG.colorLight};font-size:12px;display:flex;align-items:center;gap:5px}
.sc-st::before{content:'';width:6px;height:6px;border-radius:50%;background:${CFG.colorLight};display:inline-block}
.sc-x{width:32px;height:32px;border-radius:50%;border:none;background:rgba(255,255,255,.1);cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .15s;flex-shrink:0}
.sc-x:hover{background:rgba(255,255,255,.2)}
.sc-x svg{width:16px;height:16px;stroke:#fff;stroke-width:2.5;fill:none}

.sc-body{flex:1;overflow-y:auto;padding:10px;display:flex;flex-direction:column;gap:8px;background:#fff;scroll-behavior:smooth}

.sc-msg{display:flex;gap:8px;max-width:100%;animation:scIn .3s ease}
@keyframes scIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.sc-msg.ai{align-self:flex-start}
.sc-msg.user{align-self:flex-end;flex-direction:row-reverse}
.sc-m-av{width:28px;height:28px;border-radius:50%;background:${CFG.color};display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:4px}
.sc-m-av svg{width:14px;height:14px;fill:#fff}
.sc-bbl{padding:8px 10px;font-size:12px;line-height:1.4;max-width:200px;word-wrap:break-word}
.sc-msg.ai .sc-bbl{background:${CFG.bgBubbleAI};color:#1a1a1a;border-radius:16px 16px 16px 4px}
.sc-msg.user .sc-bbl{background:${CFG.color};color:#fff;border-radius:16px 16px 4px 16px}

.sc-qr{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
.sc-qr button{background:#F3F4F6;border:1px solid #E5E7EB;padding:6px 10px;border-radius:9999px;font-size:12px;color:${CFG.color};font-weight:500;cursor:pointer;transition:background .15s,border-color .15s;font-family:inherit}
.sc-qr button:hover{background:#E8F5EE;border-color:${CFG.color}}

.sc-typ{display:flex;gap:4px;padding:10px 14px;align-items:center}
.sc-typ span{width:8px;height:8px;border-radius:50%;background:#6B7280;animation:scDot .6s ease infinite}
.sc-typ span:nth-child(2){animation-delay:.15s}
.sc-typ span:nth-child(3){animation-delay:.3s}
@keyframes scDot{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}

.sc-cards{display:flex;flex-direction:column;gap:10px;margin-top:8px}
.sc-card{background:#fff;border:1px solid #E5E7EB;border-radius:12px;overflow:hidden;transition:box-shadow .2s}
.sc-card:hover{box-shadow:0 2px 12px rgba(0,0,0,.08)}
.sc-card img{width:100%;height:120px;object-fit:cover;display:block}
.sc-card-b{padding:12px}
.sc-card-t{font-size:14px;font-weight:700;color:#1a1a1a;margin-bottom:4px}
.sc-card-m{font-size:12px;color:#6B7280;margin-bottom:8px}
.sc-card-p{display:flex;align-items:baseline;gap:6px;margin-bottom:10px}
.sc-card-p strong{font-size:18px;color:${CFG.color};font-weight:700}
.sc-card-p span{font-size:12px;color:#6B7280}
.sc-card-btns{display:flex;gap:8px}
.sc-card-btns .btn-b{flex:1;background:${CFG.color};color:#fff;border:none;padding:8px 0;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer;transition:background .15s;font-family:inherit}
.sc-card-btns .btn-b:hover{background:#153326}
.sc-card-btns .btn-d{flex:1;background:#fff;color:${CFG.color};border:1px solid #E5E7EB;padding:8px 0;border-radius:8px;font-size:13px;font-weight:500;cursor:pointer;transition:border-color .15s;font-family:inherit}
.sc-card-btns .btn-d:hover{border-color:${CFG.color}}

.sc-cross{display:flex;gap:10px;padding:10px;border:1px solid #E5E7EB;border-radius:10px;margin-top:4px;align-items:center;transition:box-shadow .2s}
.sc-cross:hover{box-shadow:0 2px 8px rgba(0,0,0,.06)}
.sc-cross-icon{width:36px;height:36px;border-radius:8px;background:#F0F7F4;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:18px}
.sc-cross-body{flex:1;min-width:0}
.sc-cross-t{font-size:13px;font-weight:600;color:#1a1a1a}
.sc-cross-d{font-size:12px;color:#6B7280;margin-top:2px}
.sc-cross-btn{background:${CFG.color};color:#fff;border:none;padding:6px 14px;border-radius:6px;font-size:12px;font-weight:600;cursor:pointer;flex-shrink:0;font-family:inherit}

.sc-booking{background:#F0F7F4;border:1px solid #C6DDD7;border-radius:12px;padding:14px;margin-top:8px}
.sc-booking-t{font-size:15px;font-weight:700;color:${CFG.color};margin-bottom:8px}
.sc-booking-row{display:flex;justify-content:space-between;font-size:13px;color:#374151;padding:3px 0}
.sc-booking-row span:last-child{font-weight:600}
.sc-booking-btn{width:100%;margin-top:10px;background:${CFG.color};color:#fff;border:none;padding:10px;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer;font-family:inherit}

.sc-inp{display:flex;align-items:center;gap:8px;padding:10px 16px;border-top:1px solid #F3F4F6;background:#fff;flex-shrink:0}
.sc-inp input{flex:1;border:none;outline:none;font-size:16px;padding:8px 0;color:#111;background:transparent;font-family:inherit}
.sc-inp input::placeholder{color:#6B7280}
.sc-snd{width:40px;height:40px;border-radius:50%;border:none;background:${CFG.color};cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .15s,transform .1s;flex-shrink:0}
.sc-snd:hover{background:#153326}
.sc-snd:active{transform:scale(.95)}
.sc-snd svg{width:18px;height:18px;fill:#fff}
.sc-snd.off{background:#D1D5DB;pointer-events:none}
.sc-hon{text-align:center;font-size:12px;color:#6B7280;padding:4px 16px 10px;background:#fff;flex-shrink:0}
`;
    document.head.appendChild(s);
  }

  // FAB icon: chat bubble + sparkle
  const CHAT_BUBBLE = '<svg viewBox="0 0 24 24" fill="none"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" fill="#fff" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M14.5 7.5l.5 1.2 1.2.5-1.2.5-.5 1.2-.5-1.2-1.2-.5 1.2-.5z" fill="currentColor" stroke="none" opacity=".85"/><path d="M10 11l.4.8.8.4-.8.4-.4.8-.4-.8-.8-.4.8-.4z" fill="currentColor" stroke="none" opacity=".6"/></svg>';
  // Avatar icon inside chat (small sparkle)
  const SPARKLE = '<svg viewBox="0 0 24 24"><path d="M12 2L9.19 8.63 2 9.24l5.46 4.73L5.82 21 12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61z"/></svg>';
  const CLOSE = '<svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>';
  const SEND = '<svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>';
  const ICONS = { shield: '\u{1F6E1}', car: '\u{1F697}', key: '\u{1F511}' };

  function build() {
    const fab = document.createElement('button');
    fab.className = 'sc-fab';
    fab.id = 'sc-fab';
    fab.setAttribute('aria-label', L('Открыть чат', 'Open chat', 'ჩატის გახსნა'));
    fab.innerHTML = `<span class="sc-fab-tip">${L('Подобрать тур за 30 секунд', 'Find a tour in 30 seconds', 'შეარჩიეთ ტური 30 წამში')}</span>${CHAT_BUBBLE}`;
    fab.addEventListener('click', toggle);

    const win = document.createElement('div');
    win.className = 'sc-win';
    win.id = 'sc-win';
    win.innerHTML = `
<div class="sc-hdr">
  <div class="sc-av"><svg viewBox="0 0 24 24"><rect x="4" y="8" width="16" height="12" rx="3" stroke="#fff" stroke-width="1.5"/><circle cx="9" cy="14" r="1.5" fill="#86EFAC"/><circle cx="15" cy="14" r="1.5" fill="#86EFAC"/><path d="M10 18h4" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/><path d="M12 4v4" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/><circle cx="12" cy="3" r="1.5" fill="#86EFAC"/><path d="M2 13v2" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/><path d="M22 13v2" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/></svg></div>
  <div class="sc-inf"><div class="sc-nm">${CFG.name}</div><div class="sc-st">${L('Онлайн \u00b7 отвечает мгновенно','Online \u00b7 replies instantly','ონლაინ \u00b7 პასუხობს მყისიერად')}</div></div>
  <button class="sc-x" id="sc-close" aria-label="${L('Закрыть чат','Close chat','ჩატის დახურვა')}">${CLOSE}</button>
</div>
<div class="sc-body" id="sc-body"></div>
<div class="sc-inp">
  <input id="sc-input" aria-label="${L('Сообщение чату','Chat message','ჩატის შეტყობინება')}" placeholder="${L('Напишите что хотите...','Type your message...','დაწერეთ, რა გსურთ...')}" autocomplete="off">
  <button class="sc-snd" id="sc-send" aria-label="${L('Отправить сообщение','Send message','შეტყობინების გაგზავნა')}">${SEND}</button>
</div>
<div class="sc-hon">${L(CFG.name+' \u2014 это умный помощник. Хотите живого Тимура? Напишите \u00abТимур\u00bb.', CFG.name+' \u2014 is a smart assistant. Want the real Timur? Type \u00abTimur\u00bb.', CFG.name+' \u2014 ჭკვიანი ასისტენტია. გსურთ ცოცხალი თიმური? დაწერეთ \u00abთიმური\u00bb.')}</div>`;

    document.body.appendChild(fab);
    document.body.appendChild(win);

    els.fab = fab;
    els.win = win;
    els.body = document.getElementById('sc-body');
    els.input = document.getElementById('sc-input');
    els.send = document.getElementById('sc-send');

    document.getElementById('sc-close').addEventListener('click', toggle);
    els.send.addEventListener('click', () => send());
    els.input.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
    });
    els.input.addEventListener('input', () => {
      els.send.classList.toggle('off', !els.input.value.trim());
    });
    els.send.classList.add('off');
    if (curLang() === 'en') {
      els.input.placeholder = 'Type your message...';
    }
    // Fix mobile keyboard: scroll chat and adjust position
    if (window.visualViewport && window.innerWidth <= 768) {
      els.input.addEventListener('focus', () => {
        setTimeout(() => { scroll(); }, 300);
      });
      window.visualViewport.addEventListener('resize', () => {
        if (isOpen) {
          const vvh = window.visualViewport.height;
          const diff = window.innerHeight - vvh;
          if (diff > 100) {
            // Keyboard is open
            els.win.style.bottom = '0px';
            els.win.style.height = vvh + 'px';
            els.win.style.borderRadius = '0';
          } else {
            // Keyboard closed
            els.win.style.bottom = '';
            els.win.style.height = '';
            els.win.style.borderRadius = '';
          }
          scroll();
        }
      });
    }
  }

  function toggle() {
    isOpen = !isOpen;
    els.win.classList.toggle('open', isOpen);
    els.fab.style.opacity = isOpen ? '0' : '1';
    els.fab.style.pointerEvents = isOpen ? 'none' : 'auto';
    // Hide cookie bar when chat open, restore when closed
    const cookieBar = document.getElementById('cookie-bar');
    if (cookieBar) cookieBar.style.display = isOpen ? 'none' : '';
    if (isOpen) {
      els.input.focus();
      if (!els.body.children.length) showGreeting();
    }
    if (!isOpen) {
      try { localStorage.setItem(CFG.dismissKey, Date.now().toString()); } catch {}
    }
  }

  function showGreeting() {
    const tourSlug = detectTourContext();
    const isEN = curLang() === 'en';
    const isKA = curLang() === 'ka';
    const greeting = tourSlug
      ? L('Привет! Вижу вы смотрите этот тур. Хотите узнать подробности, свободные даты или забронировать?', 'Hi! I see you\'re looking at this tour. Want to know details, available dates, or book it?', 'გამარჯობა! ვხედავ, ამ ტურს ათვალიერებთ. გსურთ დეტალები, თავისუფალი თარიღები თუ დაჯავშნა?')
      : L(CFG.greeting, 'Hi! I\'m Sakhva-AI, I\'ll help you find the perfect tour in Georgia in 30 seconds. Tell me briefly \u2014 who\'s traveling, how many days, and what do you want to see?', 'გამარჯობა! მე ვარ Sakhva-AI, დაგეხმარებით იდეალური ტურის შერჩევაში საქართველოში 30 წამში. მოკლედ მითხარით \u2014 ვინ მოგზაურობთ, რამდენი დღით და რისი ნახვა გსურთ?');
    addBubble('ai', greeting);

    const quickRepliesEN = ['Couple, 4 days \u2014 wine & views', 'Family with kids \u2014 relaxed', 'Solo \u2014 what to see'];
    const quickRepliesKA = ['წყვილი, 4 დღე \u2014 ღვინო და ხედები', 'ოჯახი ბავშვებით \u2014 მშვიდად', 'მარტო \u2014 რა ვნახო'];
    const tourQuickEN = ['Available dates', 'Price & discounts', 'Book now'];
    const tourQuickKA = ['თავისუფალი თარიღები', 'ფასი და ფასდაკლებები', 'დაჯავშნა'];
    const tourQuickRU = ['\u0421\u0432\u043e\u0431\u043e\u0434\u043d\u044b\u0435 \u0434\u0430\u0442\u044b', '\u0426\u0435\u043d\u0430 \u0438 \u0441\u043a\u0438\u0434\u043a\u0438', '\u0417\u0430\u0431\u0440\u043e\u043d\u0438\u0440\u043e\u0432\u0430\u0442\u044c'];

    const replies = tourSlug
      ? (isKA ? tourQuickKA : isEN ? tourQuickEN : tourQuickRU)
      : (isKA ? quickRepliesKA : isEN ? quickRepliesEN : CFG.quickReplies);

    const qr = document.createElement('div');
    qr.className = 'sc-qr';
    replies.forEach(text => {
      const btn = document.createElement('button');
      btn.textContent = text;
      btn.addEventListener('click', () => { qr.remove(); send(text); });
      qr.appendChild(btn);
    });
    els.body.appendChild(qr);
    scroll();
  }

  function addBubble(type, text) {
    const msg = document.createElement('div');
    msg.className = 'sc-msg ' + type;
    if (type === 'ai') {
      msg.innerHTML = `<div class="sc-m-av">${SPARKLE}</div><div class="sc-bbl">${formatText(text)}</div>`;
    } else {
      msg.innerHTML = `<div class="sc-bbl">${esc(text)}</div>`;
    }
    els.body.appendChild(msg);
    scroll();
    return msg;
  }

  function formatText(t) {
    return esc(t)
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');
  }

  function esc(t) {
    const d = document.createElement('div');
    d.textContent = t;
    return d.innerHTML;
  }

  function showTyping() {
    const d = document.createElement('div');
    d.className = 'sc-msg ai';
    d.id = 'sc-typing';
    d.innerHTML = `<div class="sc-m-av">${SPARKLE}</div><div class="sc-bbl"><div class="sc-typ"><span></span><span></span><span></span></div></div>`;
    els.body.appendChild(d);
    scroll();
  }

  function removeTyping() {
    const t = document.getElementById('sc-typing');
    if (t) t.remove();
  }

  // ─── TOUR CARDS ───
  function showCards(tours) {
    const wrap = document.createElement('div');
    wrap.className = 'sc-cards';
    tours.forEach(t => {
      const card = document.createElement('div');
      card.className = 'sc-card';
      card.innerHTML = `
<img src="${t.image}" alt="${esc(t.title)}" loading="lazy"
  onerror="this.style.background='linear-gradient(135deg,#1A3D2E,#2d6b4f)';this.style.height='120px';this.alt=''">
<div class="sc-card-b">
  <div class="sc-card-t">${esc(t.title)}</div>
  <div class="sc-card-m">${esc(t.durationText)} \u00b7 ${t.format === 'group' ? 'мини-группа' : 'индивидуальная'}</div>
  <div class="sc-card-p"><strong>от \u20BE${t.price}</strong><span>(${t.price_eur}\u20AC)</span></div>
  <div class="sc-card-btns">
    <button class="btn-d" onclick="window.open('${t.url}','_blank')">Подробнее</button>
    <button class="btn-b" onclick="window.open('${t.url}#booking','_blank')">Забронировать</button>
  </div>
</div>`;
      wrap.appendChild(card);
    });
    els.body.appendChild(wrap);
    scroll();
  }

  // ─── CROSS-SELL CARDS ───
  function showCrossSell(offers) {
    offers.forEach(o => {
      const card = document.createElement('div');
      card.className = 'sc-cross';
      card.innerHTML = `
<div class="sc-cross-icon">${ICONS[o.icon] || '\u2728'}</div>
<div class="sc-cross-body">
  <div class="sc-cross-t">${esc(o.title)}</div>
  <div class="sc-cross-d">${esc(o.description)}</div>
</div>
<button class="sc-cross-btn" onclick="window.open('${o.url}','_blank')">${esc(o.price)}</button>`;
      els.body.appendChild(card);
    });
    scroll();
  }

  // ─── BOOKING DRAFT CARD ───
  function showBookingDraft(b) {
    const card = document.createElement('div');
    card.className = 'sc-booking';
    card.innerHTML = `
<div class="sc-booking-t">Бронирование</div>
<div class="sc-booking-row"><span>Тур</span><span>${esc(b.tour_name)}</span></div>
<div class="sc-booking-row"><span>Дата</span><span>${esc(b.date)}</span></div>
<div class="sc-booking-row"><span>Гостей</span><span>${b.guests}</span></div>
<div class="sc-booking-row"><span>Итого</span><span>\u20BE${b.total} (${b.total_eur}\u20AC)</span></div>
${b.discount_percent ? `<div class="sc-booking-row"><span>Скидка</span><span>-${b.discount_percent}%</span></div>` : ''}
<div class="sc-booking-row"><span>Предоплата (10%)</span><span>\u20BE${b.prepay}</span></div>
<button class="sc-booking-btn" onclick="window.open('${b.booking_url}','_blank')">Подтвердить бронь \u2192</button>`;
    els.body.appendChild(card);
    scroll();
  }

  // ─── SEND ───
  async function send(text) {
    const msg = text || els.input.value.trim();
    if (!msg) return;
    els.input.value = '';
    els.send.classList.add('off');

    msgCount++;
    if (!msgTimer) {
      msgTimer = setTimeout(() => { msgCount = 0; msgTimer = null; }, 60000);
    }
    if (msgCount > CFG.rateLimit) {
      addBubble('ai', 'Слишком много сообщений. Подождите минуту?');
      return;
    }

    const qr = els.body.querySelector('.sc-qr');
    if (qr) qr.remove();

    addBubble('user', msg);
    history.push({ role: 'user', content: msg });

    setTimeout(() => showTyping(), 200);

    try {
      const resp = await fetch(CFG.api, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: msg,
          history: history.slice(-10),
          sessionId,
          page: currentPage,
          lang: curLang()
        })
      });

      const data = await resp.json();
      removeTyping();

      if (data.error === 'no_key' || data.error === 'api_error') {
        addBubble('ai', data.reply || 'Я сейчас не на связи. Напишите Тимуру в WhatsApp: +995 511 272 623');
        return;
      }

      if (data.reply) {
        addBubble('ai', data.reply);
        history.push({ role: 'assistant', content: data.reply });
      }

      if (data.tours?.length) showCards(data.tours);
      if (data.booking) showBookingDraft(data.booking);
      if (data.crossSell?.length) showCrossSell(data.crossSell);

      try {
        localStorage.setItem(CFG.storageKey, JSON.stringify({
          history: history.slice(-20),
          ts: Date.now()
        }));
      } catch {}

    } catch {
      removeTyping();
      addBubble('ai', 'Кажется я сейчас не на связи. Напишите Тимуру напрямую в WhatsApp: +995 511 272 623');
    }
  }

  function scroll() {
    requestAnimationFrame(() => {
      els.body.scrollTop = els.body.scrollHeight;
    });
  }

  // ─── PROACTIVE OPEN ───
  // Disabled by owner request (08.09.2026): the widget must open ONLY when the user
  // clicks the FAB, never on its own. Kept as a no-op so init() stays unchanged.
  function checkProactive() {}

  // ─── INIT ───
  function init() {
    sessionId = getSessionId();
    injectStyles();
    build();

    // Hide ALL old chat/FAB elements — AI widget replaces everything
    function killOldFabs() {
      ['fab-main', 'fab-overlay', 'chat-btn', 'chat-box', 'chat-badge', 'old-chat-widget'].forEach(id => {
        const el = document.getElementById(id);
        if (el) { el.style.cssText = 'display:none!important;visibility:hidden!important'; }
      });
      document.querySelectorAll('.fab-choice, .sticky-wa, [class*="chat-btn"], [class*="chat-box"]').forEach(el => {
        el.style.cssText = 'display:none!important;visibility:hidden!important';
      });
    }
    killOldFabs();
    setInterval(killOldFabs, 2000);

    // Cookie bar must cover FAB until accepted
    const cb = document.getElementById('cookie-bar');
    if (cb) cb.style.zIndex = '999999';

    // Restore history
    try {
      const saved = JSON.parse(localStorage.getItem(CFG.storageKey) || '{}');
      if (saved.history?.length && Date.now() - saved.ts < 86400000) {
        history = saved.history;
      }
    } catch {}

    // Proactive opening on return visits
    checkProactive();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
