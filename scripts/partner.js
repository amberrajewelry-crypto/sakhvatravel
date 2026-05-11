// Partner promo — works on all pages (tours, blog, main)
;(function(){
var p=new URLSearchParams(location.search).get('utm_campaign');
if(p){localStorage.setItem('partner',p);localStorage.setItem('partner_ts',Date.now())}
var s=localStorage.getItem('partner');
var ts=parseInt(localStorage.getItem('partner_ts')||'0');
if(!s||Date.now()-ts>30*86400000){localStorage.removeItem('partner');localStorage.removeItem('partner_ts');return}
var code=s.toUpperCase()+'10';
function patch(){
document.querySelectorAll('a[href*="wa.me"]').forEach(function(a){
if(a.href.indexOf(code)===-1){
a.href=a.href+(a.href.indexOf('text=')>-1?'+Промокод+'+code:'?text=Промокод+'+code)}});
document.querySelectorAll('a[href*="t.me/SakhvaGuideBot"]').forEach(function(a){
if(a.href.indexOf('start=')>-1){a.href=a.href.replace(/start=[^&]*/,'start='+code)}
else{a.href=a.href+(a.href.indexOf('?')>-1?'&':'?')+'start='+code}});
['bm-promo','cm-promo'].forEach(function(id){
var w=document.getElementById(id+'-wrap'),i=document.getElementById(id);
if(w&&i){w.style.display='';i.value=code}});}
patch();
new MutationObserver(function(){patch()}).observe(document.body,{attributes:true,subtree:true,attributeFilter:['class']});
})();
