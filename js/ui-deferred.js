(function(){
  var chatHistory=[]
  var chatOpen=false
  var failCount=0
  var msgCount=0

  setTimeout(function(){
    if(!chatOpen) document.getElementById('chat-badge').style.display='flex'
  },3000)

  window.toggleChat=function(){
    chatOpen=!chatOpen
    var box=document.getElementById('chat-box')
    box.classList.toggle('open',chatOpen)
    document.getElementById('chat-badge').style.display='none'
    if(chatOpen && document.getElementById('chat-msgs').children.length===0){
      var isEn=document.documentElement.lang==='en'||localStorage.getItem('lang')==='en'
      chatAddMsg('bot',isEn?'Hi! 👋 I\'ll help you choose a tour in Tbilisi and Georgia. Ask about routes, prices, visas — or just tell me what you want to see!':'Привет! 👋 Я помогу подобрать тур по Тбилиси и Грузии. Спрашивайте про маршруты, цены, визы — или просто расскажите что хотите увидеть!')
    }
    if(chatOpen) setTimeout(function(){document.getElementById('chat-input').focus()},100)
  }

  window.chatQuick=function(msg){
    document.getElementById('chat-quick').style.display='none'
    chatSendMsg(msg)
  }

  window.chatKeyDown=function(e){
    if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();chatSend()}
  }

  window.chatSend=function(){
    var inp=document.getElementById('chat-input')
    var msg=inp.value.trim()
    if(!msg)return
    inp.value=''
    inp.style.height=''
    chatSendMsg(msg)
  }

  function chatSendMsg(msg){
    msgCount++
    chatAddMsg('user',msg)
    var typing=chatAddMsg('typing','Печатает...')
    fetch('/api/chat/',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({message:msg,history:chatHistory})
    })
    .then(function(r){return r.json()})
    .then(function(d){
      typing.remove()
      if(d.reply){
        failCount=0
        chatAddMsg('bot',d.reply)
        chatHistory.push({role:'user',content:msg})
        chatHistory.push({role:'assistant',content:d.reply})
        // Offer WhatsApp only after 5+ messages as a soft suggestion
        if(msgCount>=5 && msgCount%4===1){
          setTimeout(function(){
            chatAddMsg('bot','Кстати, если хотите — Тимур лично ответит в <a href="https://wa.me/995511272623" target="_blank" style="color:#1A3D2E;font-weight:700">WhatsApp</a> за 15 минут 😊')
          },800)
        }
      } else {
        failCount++
        var fallbacks=[
          'Дайте уточню... Вы имеете в виду какой-то конкретный тур или маршрут?',
          'Не совсем понял вопрос — можете переформулировать? Или спросите про конкретный тур.',
          'Хмм, давайте попробуем иначе — напишите куда хотите поехать или что хотите увидеть.',
        ]
        if(failCount<=3){
          chatAddMsg('bot',fallbacks[Math.min(failCount-1,2)])
        } else {
          chatAddMsg('bot','Кажется, по этому вопросу лучше ответит сам Тимур — напишите ему в <a href="https://wa.me/995511272623" target="_blank" style="color:#1A3D2E;font-weight:700">WhatsApp</a>, он онлайн.')
          failCount=0
        }
      }
    })
    .catch(function(){
      typing.remove()
      failCount++
      var netFallbacks=[
        'Секунду, переподключаюсь... Попробуйте ещё раз.',
        'Небольшие неполадки с соединением — напишите вопрос ещё раз.',
        'Связь немного барахлит. Попробуйте через секунду или напишите Тимуру в <a href="https://wa.me/995511272623" target="_blank" style="color:#1A3D2E;font-weight:700">WhatsApp</a>.'
      ]
      var el=chatAddMsg('bot','')
      el.innerHTML=netFallbacks[Math.min(failCount-1,2)]
    })
  }

  function chatAddMsg(type,text){
    var msgs=document.getElementById('chat-msgs')
    var div=document.createElement('div')
    div.className='chat-msg '+type
    if(type==='user'){div.textContent=text}else{div.innerHTML=text}
    msgs.appendChild(div)
    msgs.scrollTop=msgs.scrollHeight
    return div
  }

  var ci=document.getElementById('chat-input')
  if(ci) ci.addEventListener('input',function(){
    this.style.height='auto'
    this.style.height=Math.min(this.scrollHeight,80)+'px'
  })
})();

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

function openPayment(){if(typeof closeQuiz==='function')closeQuiz();if(typeof closeContact==='function')closeContact();document.getElementById('pay-modal').classList.add('open');document.body.style.overflow='hidden';pmBack()}
function closePayment(){document.getElementById('pay-modal').classList.remove('open');document.body.style.overflow=''}
function pmBack(){document.getElementById('pm-methods').style.display='';document.getElementById('pm-sbp').style.display='none';document.getElementById('pm-crypto').style.display='none';document.getElementById('pm-wise').style.display='none'}
function showSBP(){document.getElementById('pm-methods').style.display='none';document.getElementById('pm-sbp').style.display='block';if(typeof gtag==='function')gtag('event','begin_checkout',{payment_type:'sbp'})}
function showCrypto(){document.getElementById('pm-methods').style.display='none';document.getElementById('pm-crypto').style.display='block';if(typeof gtag==='function')gtag('event','begin_checkout',{payment_type:'crypto'})}
function showWise(){document.getElementById('pm-methods').style.display='none';document.getElementById('pm-wise').style.display='block';if(typeof gtag==='function')gtag('event','begin_checkout',{payment_type:'wise'})}
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