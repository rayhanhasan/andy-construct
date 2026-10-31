/* Andy Construct v3 : drapeaux de test A/B (source ; minifié et injecté dans le script d'amorçage du <head>).
   S'exécute AVANT le premier rendu : la variante est posée sur <html data-ab-<drapeau>="b"> et la feuille de style
   n'affiche que celle-là (aucun clignotement, aucun décalage). Configuration : tools/build/donnees/config.json → ab,
   injectée par le générateur : window.AC_AB = { drapeau: { v: [variantes], p: [poids], n: version, pg: [pages],
   x: "chargement" | sélecteur, off: 1 si inactif (forçage de recette seulement) } }.
   - attribution stable par visiteur et par version (localStorage « ac_ab » : { drapeau: [variante, version] }) ;
     une nouvelle version d'un drapeau provoque un nouveau tirage ;
   - sans stockage, ou Do Not Track / Global Privacy Control : variante « a », rien n'est stocké ni mesuré ;
   - un drapeau ne s'applique qu'aux pages listées (« * » : toutes) ;
   - forçage pour la recette : ?flag=hero-titre:b (plusieurs : ?flag=a:b,c:b ; ?flag=reset efface tout) ;
     un navigateur forcé ne mesure plus (clé « _f ») jusqu'à « reset » ;
   - mesure (main.js) : « exposition_variante » une fois par visiteur et par drapeau, propriétés f_<drapeau> sur les
     conversions, « intention_contact » dédoublonné (cro-v3 §5.4). */
(function (w, h) {
  var C = w.AC_AB, K = 'ac_ab', A = {}, S = null, F = {}, q, n, N = w.navigator,
    dnt = N.doNotTrack == '1' || w.doNotTrack == '1' || !!N.globalPrivacyControl,
    page = w.location.pathname.split('/').pop() || 'index.html';
  if (!C) return;
  if (!dnt) { try { S = JSON.parse(w.localStorage.getItem(K) || '{}') || {}; } catch (e) { S = null; } }
  q = /[?&]flag=([^&#]*)/.exec(w.location.search);
  if (q) decodeURIComponent(q[1]).split(',').forEach(function (x) {
    var p = x.split(':');
    if (p[0] === 'reset') {
      if (S) S = {};
      try { w.localStorage.removeItem('ac_ab_vus'); w.localStorage.removeItem('ac_ic'); } catch (e) {}
    } else if (p[1]) F[p[0]] = p[1];
  });
  for (n in C) {
    var c = C[n], v = c.v, p = c.p, m = S && S[n], t = 0, k = 0, r;
    if (F[n] && v.indexOf(F[n]) > -1) { A[n] = F[n]; if (S) { S[n] = [F[n], c.n]; S._f = 1; } continue; }
    if (c.off || !S || (c.pg && c.pg.indexOf(page) < 0 && c.pg.indexOf('*') < 0)) continue;
    if (m && m[1] === c.n && v.indexOf(m[0]) > -1) { A[n] = m[0]; continue; }
    r = Math.random() * p.reduce(function (a, b) { return a + b; }, 0);
    for (; k < v.length - 1; k++) { t += p[k]; if (r < t) break; }
    A[n] = v[k]; S[n] = [v[k], c.n];
  }
  if (S) { try { w.localStorage.setItem(K, JSON.stringify(S)); } catch (e) {} }
  for (n in A) h.setAttribute('data-ab-' + n, A[n]);
  w.acAB = { v: A, c: C, force: !S || !!S._f };
})(window, document.documentElement);
