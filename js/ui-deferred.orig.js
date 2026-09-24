// Old chat removed — replaced by /js/chat-widget.js
// Keep toggleChat stub for FAB overlay compatibility
window.toggleChat=function(){
  var sc=document.getElementById('sc-fab');
  if(sc) sc.click();
};

(function(){
  // FAB toggle WA/TG
  window.toggleFab=function(){
    var btn=document.getElementById('fab-main');
    var ov=document.getElementById('fab-overlay');
    if(!btn||!ov)return;
    var open=ov.classList.toggle('open');
    btn.classList.toggle('open',open);
    if(open){
      document.addEventListener('click',function h(e){
        if(!btn.contains(e.target)&&!ov.contains(e.target)){
          ov.classList.remove('open');btn.classList.remove('open');
          document.removeEventListener('click',h);
        }
      });
    }
  };
})();

/* ── Conversion tracking: WhatsApp, Telegram, forms ── */
(function(){
  if(typeof gtag!=='function')return;
  // WhatsApp click
  document.addEventListener('click',function(e){
    var a=e.target.closest('a[href*="wa.me"]');
    if(a){
      gtag('event','generate_lead',{event_category:'whatsapp',event_label:a.href});
      gtag('event','whatsapp_click',{event_category:'contact',event_label:'whatsapp'});
      if(typeof posthog!=='undefined'){posthog.capture('whatsapp_click')}
    }
  });
  // Telegram click
  document.addEventListener('click',function(e){
    var a=e.target.closest('a[href*="t.me"]');
    if(a){
      gtag('event','generate_lead',{event_category:'telegram',event_label:a.href});
    }
  });
  // Booking form submit (bmSubmit)
  var bmBtn=document.querySelector('.bm-next');
  if(bmBtn){
    bmBtn.addEventListener('click',function(){
      gtag('event','generate_lead',{event_category:'booking',event_label:'form_submit'});
    });
  }
  // Contact form submit (sendContact)
  var cmBtn=document.querySelector('.cm-submit');
  if(cmBtn){
    cmBtn.addEventListener('click',function(){
      gtag('event','generate_lead',{event_category:'contact',event_label:'form_submit'});
    });
  }
  // Phone link click
  document.addEventListener('click',function(e){
    var a=e.target.closest('a[href^="tel:"]');
    if(a){
      }
  });
})();

function openPayment(){if(typeof closeQuiz==='function')closeQuiz();if(typeof closeContact==='function')closeContact();var m=document.getElementById('pay-modal');if(m){m.style.display='flex';m.classList.add('open')}document.body.style.overflow='hidden';pmBack()}
function closePayment(){var m=document.getElementById('pay-modal');if(m){m.style.display='none';m.classList.remove('open')}document.body.style.overflow=''}
function pmBack(){document.getElementById('pm-methods').style.display='';document.getElementById('pm-sbp').style.display='none';document.getElementById('pm-crypto').style.display='none';document.getElementById('pm-wise').style.display='none'}
function showSBP(){document.getElementById('pm-methods').style.display='none';document.getElementById('pm-sbp').style.display='block';if(typeof gtag==='function')gtag('event','begin_checkout',{payment_type:'sbp'})}
function showCrypto(){document.getElementById('pm-methods').style.display='none';document.getElementById('pm-crypto').style.display='block';if(typeof gtag==='function')gtag('event','begin_checkout',{payment_type:'crypto'})}
function showWise(){document.getElementById('pm-methods').style.display='none';document.getElementById('pm-wise').style.display='block';if(typeof gtag==='function')gtag('event','begin_checkout',{payment_type:'wise'})}
function showCardPay(){var name=document.getElementById('pm-name')?document.getElementById('pm-name').value:'';var phone=document.getElementById('pm-phone')?document.getElementById('pm-phone').value:'';var amt=document.getElementById('pm-amount-input')?document.getElementById('pm-amount-input').value:'';var comment=document.getElementById('pm-comment')?document.getElementById('pm-comment').value:'';if(!amt||isNaN(amt)||Number(amt)<1){var inp=document.getElementById('pm-amount-input');if(inp){inp.style.borderColor='#EF4444';inp.focus()}return}if(typeof gtag==='function')gtag('event','begin_checkout',{payment_type:'card'});fetch('/api/booking/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:name||'(card)',phone:phone,tour:comment||'Card payment',note:'BOG Card '+amt+' GEL'})}).catch(function(){});fetch('/api/create-bog-payment/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({amount:Number(amt),orderId:'SK-'+Date.now(),description:comment||'Sakhva Travel payment',email:''})}).then(function(r){return r.json()}).then(function(j){var url=j.checkout_url;if(url)window.location.href=url;else alert('Оплата картой временно недоступна. Используйте СБП или криптовалюту.')}).catch(function(){alert('Ошибка соединения. Попробуйте СБП или криптовалюту.')})}
function payCrypto(){
  var inp=document.getElementById('pm-crypto-amount');var amount=inp?inp.value:'';
  if(!amount||isNaN(amount)||Number(amount)<1){inp.style.borderColor='#EF4444';return}
  inp.style.borderColor='#1A3D2E';
  if(typeof gtag==='function')fetch('/api/create-payment',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({amount:Number(amount),description:'Sakhva Travel Tour',orderId:'ST-'+Date.now()})})
  .then(function(r){return r.json()}).then(function(d){if(d.invoiceUrl)window.location.href=d.invoiceUrl;else alert(d.error||'Ошибка')}).catch(function(){alert('Ошибка соединения')})
}
function updateWiseLink(){
  var inp=document.getElementById('pm-wise-amount');var amt=inp?inp.value:'';
  var btn=document.getElementById('pm-wise-btn');
  var url='https://wise.com/pay/business/amberra';
  if(amt&&!isNaN(amt)&&Number(amt)>0)url+='?amount='+amt+'&currency=USD&description=Sakhva+Travel+Tour';
  btn.href=url;
  btn.onclick=function(){if(typeof gtag==='function'){gtag('event','begin_checkout',{payment_type:'wise'})}};
}

// Instagram hearts animation
(function(){
  var cells=document.querySelectorAll('#instagram a[style*="aspect-ratio"]');
  if(!cells.length)return;
  var sizes=[20,24,28,22,26];
  var colors=['#E1306C','#FF6B6B','#FF4757','#FD79A8','#E84393','#ff3b5c'];
  function spawnHeart(){
    var cell=cells[Math.floor(Math.random()*cells.length)];
    var h=document.createElementNS('http://www.w3.org/2000/svg','svg');
    var s=sizes[Math.floor(Math.random()*sizes.length)];
    var c=colors[Math.floor(Math.random()*colors.length)];
    h.setAttribute('viewBox','0 0 24 24');h.setAttribute('width',s);h.setAttribute('height',s);
    h.innerHTML='<path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" fill="'+c+'"/>';
    h.classList.add('ig-heart');
    h.style.right=(5+Math.random()*12)+'%';
    h.style.bottom=(3+Math.random()*10)+'%';
    cell.appendChild(h);
    setTimeout(function(){h.remove()},1700);
  }
  function loop(){
    spawnHeart();
    if(Math.random()>.4)setTimeout(spawnHeart,80+Math.random()*150);
    if(Math.random()>.7)setTimeout(spawnHeart,200+Math.random()*200);
    setTimeout(loop,300+Math.random()*500);
  }
  var started=false;
  function startHearts(){if(started)return;started=true;for(var i=0;i<5;i++)setTimeout(spawnHeart,i*120);setTimeout(loop,500)}
  var sec=document.getElementById('instagram');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(e){if(e[0].isIntersecting){io.disconnect();startHearts()}},{threshold:0.1});
    io.observe(sec);
  }
  // Fallback: start on scroll near section or after 5s
  window.addEventListener('scroll',function chk(){
    if(sec.getBoundingClientRect().top<window.innerHeight+200){window.removeEventListener('scroll',chk);startHearts()}
  });
  setTimeout(startHearts,5000);
})();