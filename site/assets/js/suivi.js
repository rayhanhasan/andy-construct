/* Suivi sans cookie (Umami), DNT/GPC respectés. Contrat : docs/v2/contrat-interface.md §9 */
(function(w,d){'use strict';
var n=navigator,L=location,K='ac_src',src=null,
dnt=n.doNotTrack=='1'||w.doNotTrack=='1'||!!n.globalPrivacyControl,
X=/^(nom|prenom|e?-?mail|tel|telephone|message|adresse|commune)$/;
function g(k){try{return JSON.parse(sessionStorage.getItem(k))}catch(e){}}
function m(k,v){try{sessionStorage.setItem(k,JSON.stringify(v))}catch(e){}}
function s(nom,pr,i){if(dnt||!nom)return;var p={},k,v,u=w.umami;
for(k in pr||{}){v=pr[k];if(!X.test(k)&&/^(string|number)$/.test(typeof v))p[k]=(''+v).slice(0,60)}
if(u&&u.track){try{u.track((''+nom).slice(0,50),p)}catch(e){}}else if((i|0)<5)setTimeout(function(){s(nom,pr,(i|0)+1)},800)}
w.acSuivi=function(nom,p){s(nom,p,5)};
w.acUmamiAvantEnvoi=function(t,c){if(dnt)return false;['url','referrer'].forEach(function(k){
if(c&&typeof c[k]=='string')c[k]=c[k].replace(/([?&])(gclid|fbclid|msclkid|e-?mail)=[^&#]*/gi,'$1')});return c};
if(!dnt){var q=new URLSearchParams(L.search),o={},a=0,r='';
'source medium campaign content term'.split(' ').forEach(function(c){var v=q.get('utm_'+c);if(v){o['utm_'+c]=v.slice(0,100);a=1}});
src=g(K);if(a||!src){try{r=new URL(d.referrer).hostname}catch(e){}
o.referent=r==L.hostname?'':r;o.page_entree=L.pathname;
if((w.acConsentAds===true||d.documentElement.getAttribute('data-consent-ads')=='accorde')&&q.get('gclid'))o.gclid=q.get('gclid').slice(0,200);
m(K,src=o);if(o.utm_source=='recommandation')s('recommandation_carte',{})}}
function f(F){var v={page:L.pathname},k,e;for(k in src||{})v[k]=src[k];
for(k in v){e=F.elements[k];if(!e){e=d.createElement('input');e.type='hidden';e.name=k;F.appendChild(e)}
if(e.type=='hidden'&&!e.value)e.value=v[k]||''}}
function init(){[].forEach.call(d.querySelectorAll('form[data-suivi-formulaire],form[action*="api/demande.php"]'),f)}
d.readyState=='loading'?d.addEventListener('DOMContentLoaded',init):init();
d.addEventListener('submit',function(e){if(e.target.tagName=='FORM')f(e.target)},true);
d.addEventListener('focusin',function(e){var F=e.target.closest&&e.target.closest('form[data-suivi-formulaire]'),t;
if(!F||dnt)return;t=F.getAttribute('data-suivi-formulaire');if(!g('ac_debut_'+t)){m('ac_debut_'+t,1);s('formulaire_debut',{formulaire:t})}});
d.addEventListener('click',function(e){var el=e.target.closest&&e.target.closest('[data-suivi],a[href^="tel:"],a[href^="mailto:"],a[href*="wa.me/"],a[href*="maps"]'),
h,nom,p={},i,a,z;if(!el||el.tagName=='FORM')return;h=el.getAttribute('href')||'';
nom=el.getAttribute('data-suivi')||(/^tel:/.test(h)?'appel_clic':/^mailto:/.test(h)?'email_clic':/wa\.me/.test(h)?'whatsapp_clic':'itineraire_clic');
for(i=0;a=el.attributes[i];i++)if(!a.name.indexOf('data-suivi-')&&a.name!='data-suivi-zone')p[a.name.slice(11).replace(/-/g,'_')]=a.value;
if(!p.emplacement&&(z=el.closest('[data-suivi-zone]')))p.emplacement=z.getAttribute('data-suivi-zone');
s(nom,p)},true)})(window,document);
