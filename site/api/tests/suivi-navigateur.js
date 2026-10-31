/*
 * Test de site/assets/js/suivi.js dans Chromium (Playwright), sans réseau :
 *   node site/api/tests/suivi-navigateur.js
 * Prérequis : npm i -g playwright && npx playwright install chromium
 * Vérifie : UTM en sessionStorage, champs cachés, événements data-suivi et liens,
 * propriétés personnelles filtrées, gclid seulement avec consentement, Do Not Track.
 */
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node-tools/node_modules/playwright')); }
const http = require('http'), fs = require('fs'), path = require('path');
const suivi = fs.readFileSync(path.join(__dirname, '../../assets/js/suivi.js'));
const PAGE = '<!doctype html><html><head><meta charset="utf-8">\n<script>document.addEventListener("click",function(e){e.preventDefault()});window.evts=[];window.umami={track:function(n,p){evts.push([n,p])}};</script>\n<script src="suivi.js" defer></script></head><body>\n<header data-suivi-zone="entete"><a id="tel" href="tel:+41227712015" data-suivi-numero="fixe">Appeler</a></header>\n<a id="devis" href="#demande" data-suivi="devis_clic" data-suivi-emplacement="heros">Demander un devis</a>\n<a id="mail" href="mailto:contact@andyconstruct.ch">Écrire</a>\n<a id="wa" href="https://wa.me/41786311434">WhatsApp</a>\n<a id="carte" href="https://maps.app.goo.gl/xyz" data-suivi-zone="contact">Itinéraire</a>\n<form id="f" action="/api/demande.php" method="post" data-suivi-formulaire="devis"><input name="nom" id="nom"><input type="hidden" name="utm_source"></form>\n<form id="r" action="/api/demande.php" method="post"><input name="telephone"></form>\n</body></html>\n';
const srv = http.createServer((q, r) => {
  const chemin = q.url.split('?')[0];
  r.setHeader('Content-Type', chemin.endsWith('.js') ? 'text/javascript' : 'text/html; charset=utf-8');
  r.end(chemin.endsWith('suivi.js') ? suivi : PAGE);
}).listen(0);
(async () => {
  const port = srv.address().port, b = await chromium.launch(); let ok = 0, ko = 0;
  const t = (c, m, x) => { if (c) { ok++; console.log('  ✔ ' + m) } else { ko++; console.log('  ✘ ' + m + (x ? ' → ' + JSON.stringify(x) : '')) } };
  // 1. Visite avec UTM puis navigation interne
  let ctx = await b.newContext(), p = await ctx.newPage();
  await p.goto(`http://localhost:${port}/?utm_source=google&utm_medium=cpc&utm_campaign=2026-11_acoustique&gclid=ABC123456789`, { referer: 'https://www.google.ch/' });
  await p.waitForTimeout(300);
  const st = await p.evaluate(() => JSON.parse(sessionStorage.getItem('ac_src')));
  t(st.utm_source === 'google' && st.utm_campaign === '2026-11_acoustique', 'UTM gardés en sessionStorage', st);
  t(st.referent === 'www.google.ch', 'référent externe = nom d\'hôte seul', st.referent);
  t(!st.gclid, 'gclid ignoré sans consentement');
  t(await p.evaluate(() => document.cookie) === '', 'aucun cookie');
  const champs = await p.evaluate(() => Object.fromEntries(new FormData(document.getElementById('f'))));
  t(champs.utm_source === 'google' && champs.utm_medium === 'cpc' && champs.page === '/' && champs.page_entree === '/' && champs.referent === 'www.google.ch', 'champs cachés remplis (existants et créés)', champs);
  const champsR = await p.evaluate(() => Object.fromEntries(new FormData(document.getElementById('r'))));
  t(champsR.utm_campaign === '2026-11_acoustique', 'formulaire sans data-suivi-formulaire (action api/demande.php) aussi rempli');
  await p.click('#tel'); await p.click('#devis'); await p.click('#mail'); await p.click('#wa'); await p.click('#carte');
  await p.focus('#nom'); await p.focus('#nom'); await p.evaluate(() => document.getElementById('nom').blur()); await p.focus('#nom');
  await p.evaluate(() => acSuivi('formulaire_envoye', { formulaire: 'devis', service: 'placo', email: 'x@y.ch', nom: 'Dupont' }));
  const ev = await p.evaluate(() => evts);
  const noms = ev.map(e => e[0]);
  t(JSON.stringify(ev[0]) === JSON.stringify(['appel_clic', { numero: 'fixe', emplacement: 'entete' }]), 'clic tel: → appel_clic {numero, emplacement}', ev[0]);
  t(JSON.stringify(ev[1]) === JSON.stringify(['devis_clic', { emplacement: 'heros' }]), 'data-suivi="devis_clic" + data-suivi-emplacement', ev[1]);
  t(noms.includes('email_clic') && noms.includes('whatsapp_clic'), 'mailto: → email_clic, wa.me → whatsapp_clic');
  t(JSON.stringify(ev[4]) === JSON.stringify(['itineraire_clic', { emplacement: 'contact' }]), 'carte → itineraire_clic', ev[4]);
  t(noms.filter(n => n === 'formulaire_debut').length === 1, 'formulaire_debut envoyé une seule fois');
  const env = ev.find(e => e[0] === 'formulaire_envoye');
  t(env && !env[1].email && !env[1].nom && env[1].service === 'placo', 'acSuivi() : propriétés personnelles retirées', env);
  const avant = await p.evaluate(() => acUmamiAvantEnvoi('event', { url: '/?utm_source=google&gclid=ABC&x=1', referrer: 'https://www.google.ch/?fbclid=Z' }));
  t(!avant.url.includes('gclid') && avant.url.includes('utm_source=google') && !avant.referrer.includes('fbclid'), 'before-send : gclid/fbclid retirés, UTM conservés', avant);
  // 2. Page suivante sans UTM : la source d'origine est conservée
  await p.goto(`http://localhost:${port}/?x=1`, { referer: `http://localhost:${port}/` }); await p.waitForTimeout(200);
  const st2 = await p.evaluate(() => JSON.parse(sessionStorage.getItem('ac_src')));
  t(st2.utm_source === 'google' && st2.referent === 'www.google.ch', 'navigation interne : source d\'origine conservée', st2);
  // 3. Consentement publicitaire : gclid conservé
  ctx = await b.newContext(); p = await ctx.newPage();
  await p.addInitScript(() => { window.acConsentAds = true });
  await p.goto(`http://localhost:${port}/?gclid=Cj0KCQjwABCDEF`); await p.waitForTimeout(200);
  t((await p.evaluate(() => JSON.parse(sessionStorage.getItem('ac_src')))).gclid === 'Cj0KCQjwABCDEF', 'gclid conservé avec consentement');
  // 4. Do Not Track
  ctx = await b.newContext(); p = await ctx.newPage();
  await p.addInitScript(() => { Object.defineProperty(navigator, 'doNotTrack', { get: () => '1' }) });
  await p.goto(`http://localhost:${port}/?utm_source=meta`); await p.waitForTimeout(300);
  await p.click('#tel'); await p.focus('#nom'); await p.evaluate(() => acSuivi('formulaire_envoye', {}));
  t((await p.evaluate(() => evts.length)) === 0, 'Do Not Track : aucun événement');
  t((await p.evaluate(() => sessionStorage.getItem('ac_src'))) === null, 'Do Not Track : rien en sessionStorage');
  t((await p.evaluate(() => acUmamiAvantEnvoi('x', { url: '/' }))) === false, 'Do Not Track : before-send annule la mesure Umami');
  // 5. Umami absent : aucune erreur
  ctx = await b.newContext(); p = await ctx.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(e.message));
    await p.goto(`http://localhost:${port}/`); await p.evaluate(() => { delete window.umami }); await p.click('#tel'); await p.waitForTimeout(500);
  t(errs.length === 0, 'Umami absent : aucune erreur JavaScript', errs);
  await b.close(); srv.close(); console.log(`\n${ok} réussies, ${ko} échec(s)`); process.exit(ko ? 1 : 0);
})();
