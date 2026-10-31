/* Andy Construct v3 : drapeaux de test A/B (source ; minifié et injecté dans le script d'amorçage du <head>).
   S'exécute AVANT le premier rendu : la variante est posée sur <html data-ab-<drapeau>="b"> et la feuille de style
   n'affiche que celle-là (aucun clignotement, aucun décalage). Configuration : tools/build/donnees/config.json → ab,
   injectée par le générateur dans window.AC_AB = { drapeau: { v: [variantes], p: [poids] } }.
   - attribution stable par visiteur (localStorage « ac_ab ») ; sans stockage : variante « a » et aucune mesure ;
   - forçage pour la recette : ?flag=hero-titre:b (plusieurs : ?flag=a:b,c:b ; ?flag=reset efface tout) ;
     un navigateur forcé n'envoie plus de mesure (clé « _f ») jusqu'à « reset » ;
   - mesure : main.js envoie « exposition_variante » {flag, variante} pour chaque drapeau présent sur la page. */
(function (w, h) {
  var C = w.AC_AB, K = 'ac_ab', A = {}, S = null, F = {}, q, n;
  if (!C) return;
  try { S = JSON.parse(w.localStorage.getItem(K) || '{}') || {}; } catch (e) { S = null; }
  q = /[?&]flag=([^&#]*)/.exec(w.location.search);
  if (q) decodeURIComponent(q[1]).split(',').forEach(function (x) {
    var p = x.split(':');
    if (p[0] === 'reset') { if (S) S = {}; } else if (p[1]) F[p[0]] = p[1];
  });
  for (n in C) {
    var c = C[n], v = c.v, p = c.p, t = 0, k = 0, r;
    if (F[n] && v.indexOf(F[n]) > -1) { A[n] = F[n]; if (S) { S[n] = F[n]; S._f = 1; } continue; }
    if (!S) continue;
    if (S[n] && v.indexOf(S[n]) > -1) { A[n] = S[n]; continue; }
    r = Math.random() * p.reduce(function (a, b) { return a + b; }, 0);
    for (; k < v.length - 1; k++) { t += p[k]; if (r < t) break; }
    A[n] = S[n] = v[k];
  }
  if (S) { try { w.localStorage.setItem(K, JSON.stringify(S)); } catch (e) {} }
  for (n in A) h.setAttribute('data-ab-' + n, A[n]);
  w.acAB = { v: A, force: !!(S && S._f) || !S };
})(window, document.documentElement);
