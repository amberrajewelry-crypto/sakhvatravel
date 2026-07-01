// Scroll-reveal video
!function(){'use strict';
if(window.matchMedia('(prefers-reduced-motion:reduce)').matches)return;
if(window.matchMedia('(max-width:768px)').matches)return;
var s=document.querySelector('.scroll-reveal-video'),w=s&&s.querySelector('.reveal-wrapper');
if(!s||!w)return;
var SW=60,EW=100,SH=50,EH=100,SR=24,ticking=false;
function update(){
var r=s.getBoundingClientRect(),sh=s.offsetHeight,wh=window.innerHeight;
var p=Math.max(0,Math.min(1,-r.top/(sh-wh)));
var e=1-Math.pow(1-p,3);
var wi=SW+(EW-SW)*e,hi=SH+(EH-SH)*e,ra=SR*(1-e);
var top=(wh-(wh*hi/100))/2;
w.style.setProperty('--reveal-w',wi+'%');
w.style.setProperty('--reveal-h',hi+'vh');
w.style.setProperty('--reveal-r',ra+'px');
w.style.top=top+'px';
s.classList.toggle('is-fullscreen',p>.85);
ticking=false;
}
function onS(){if(!ticking){requestAnimationFrame(update);ticking=true}}
window.addEventListener('scroll',onS,{passive:true});
window.addEventListener('resize',onS,{passive:true});
update();
}();