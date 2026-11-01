/*
 * Maquette du tableau de bord d'administration Andy Construct.
 * JavaScript sans dépendance, ouvrable en file://. Rien n'est envoyé ni enregistré.
 * Les calculs suivent docs/v4/admin/plan-dashboard-admin.md §5 (dictionnaire des indicateurs).
 */
(function () {
  'use strict';
  var M = window.MAQ;

  /* ================= Outils ================= */
  function esc(v) {
    return String(v == null ? '' : v).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  /* Heure « murale » de Zurich, comptée en minutes (sans fuseau : la maquette ne dépend pas de celui de l'ordinateur). */
  function t(s) { var p = s.split(/[- :]/); return Date.UTC(+p[0], +p[1] - 1, +p[2], +(p[3] || 0), +(p[4] || 0)) / 60000; }
  function parts(min) { var d = new Date(min * 60000); return { y: d.getUTCFullYear(), m: d.getUTCMonth() + 1, j: d.getUTCDate(), h: d.getUTCHours(), mi: d.getUTCMinutes(), w: d.getUTCDay() }; }
  function cleJour(min) { var p = parts(min); return p.y + '-' + pad(p.m) + '-' + pad(p.j); }
  var NOW = t(M.MAINTENANT);
  var AUJ = t(cleJour(NOW));
  var JOURS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
  var JC = ['dim.', 'lun.', 'mar.', 'mer.', 'jeu.', 'ven.', 'sam.'];
  var MOISN = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
  var MOISC = ['nov.', 'déc.', 'janv.', 'févr.', 'mars', 'avr.'];
  function heure(min) { var p = parts(min); return p.h + ' h' + (p.mi ? ' ' + pad(p.mi) : ''); }
  function dateC(min) { var p = parts(min); return pad(p.j) + '.' + pad(p.m); }
  function dateA(min) { var p = parts(min); return pad(p.j) + '.' + pad(p.m) + '.' + p.y; }
  function dateH(min) { return JC[parts(min).w] + ' ' + dateC(min) + ', ' + heure(min); }
  function dateL(min) { var p = parts(min); return JOURS[p.w] + ' ' + p.j + ' ' + MOISN[p.m - 1] + ' ' + p.y; }
  function moisL(mk) { var p = mk.split('-'); return MOISN[+p[1] - 1] + ' ' + p[0]; }
  function moisCourt(mk) { return MOISC[M.MOIS.indexOf(mk)] || moisL(mk); }
  function nb(n, dec) {
    var s = dec ? Number(n).toFixed(dec) : String(Math.round(n));
    var a = s.split('.'); a[0] = a[0].replace(/\B(?=(\d{3})+(?!\d))/g, "'");
    return a.join(',');
  }
  function chf(n) { return 'CHF ' + nb(n); }
  function pct(x, dec) { return (x == null || isNaN(x) || !isFinite(x)) ? '—' : nb(x * 100, dec || 0) + ' %'; }
  function duree(minutes) {
    minutes = Math.round(minutes);
    var h = Math.floor(minutes / 60), m = minutes % 60;
    return h === 0 ? m + ' min' : h + ' h' + (m ? ' ' + pad(m) : '');
  }
  function mediane(v) { if (!v.length) return null; v = v.slice().sort(function (a, b) { return a - b; }); var k = Math.floor(v.length / 2); return v.length % 2 ? v[k] : (v[k - 1] + v[k]) / 2; }
  function somme(v) { return v.reduce(function (a, b) { return a + b; }, 0); }
  function finMois(mk) { var p = mk.split('-'); var d = Date.UTC(+p[0], +p[1], 1) / 60000; return d - 1; }
  function moisPrec(mk) { var i = M.MOIS.indexOf(mk); return i > 0 ? M.MOIS[i - 1] : null; }
  function ascii(s) { return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z]+/g, '.').replace(/^\.|\.$/g, ''); }

  /* ================= Heures ouvrables (comme HeuresOuvrables.php) ================= */
  var FERIES = { '2026-12-25': 1, '2026-12-31': 1, '2027-01-01': 1, '2027-03-26': 1, '2027-03-29': 1, '2027-05-06': 1, '2027-05-17': 1, '2027-08-01': 1, '2027-09-09': 1, '2027-12-25': 1, '2027-12-31': 1 };
  var H_DEB = 7 * 60, H_FIN = 18 * 60;
  function debutJour(min) { return Math.floor(min / 1440) * 1440; }
  function jourOuvrable(min) { var w = parts(min).w; return w !== 0 && w !== 6 && !FERIES[cleJour(min)]; }
  function prochainOuvrable(min) {
    for (var i = 0; i < 40; i++) {
      var j = debutJour(min);
      if (jourOuvrable(min)) { if (min < j + H_DEB) return j + H_DEB; if (min < j + H_FIN) return min; }
      min = j + 1440 + H_DEB;
    }
    return min;
  }
  function ajouterOuvrables(min, minutes) {
    var c = prochainOuvrable(min), r = minutes;
    for (var i = 0; i < 80 && r > 0; i++) {
      var fer = debutJour(c) + H_FIN, dispo = fer - c;
      if (r <= dispo) return c + r;
      r -= dispo; c = prochainOuvrable(fer + 1);
    }
    return c;
  }
  function minutesOuvrables(a, b) {
    var total = 0, c = a;
    for (var i = 0; i < 400 && c < b; i++) {
      var j = debutJour(c);
      if (jourOuvrable(c)) { var s = Math.max(c, j + H_DEB), e = Math.min(b, j + H_FIN); if (e > s) total += e - s; }
      c = j + 1440;
    }
    return total;
  }
  function jourOuvrableSuivant(min, h) { var j = debutJour(min) + 1440; for (var i = 0; i < 30 && !jourOuvrable(j); i++) j += 1440; return j + h * 60; }
  function echeance(prio, recu) {
    if (prio === 'A') return ajouterOuvrables(recu, 120);
    if (prio === 'B') return (jourOuvrable(recu) && parts(recu).h < 14) ? debutJour(recu) + H_FIN : jourOuvrableSuivant(recu, 10);
    if (prio === 'C') return ajouterOuvrables(recu, 2 * 11 * 60);
    return ajouterOuvrables(recu, 11 * 60);
  }
  function joursOuvrablesMois(mk) {
    var p = mk.split('-'), d = Date.UTC(+p[0], +p[1] - 1, 1) / 60000, n = 0;
    while (cleJour(d).slice(0, 7) === mk) { if (jourOuvrable(d)) n++; d += 1440; }
    return n;
  }
  function joursOuvrablesEcoules(mk) {
    var p = mk.split('-'), d = Date.UTC(+p[0], +p[1] - 1, 1) / 60000, n = 0;
    while (d < AUJ) { if (jourOuvrable(d)) n++; d += 1440; }
    if (jourOuvrable(NOW)) n += Math.max(0, Math.min(1, (NOW - AUJ - H_DEB) / (H_FIN - H_DEB)));
    return n;
  }
  function ouvrableApres(dateStr, jours) { var d = t(dateStr) + jours * 1440 + 9 * 60 + 15; return jourOuvrable(d) ? d : jourOuvrableSuivant(d, 9) + 15; }

  /* ================= Libellés ================= */
  var L = {
    type: { proprietaire: 'Propriétaire', locataire: 'Locataire', regie: 'Régie', architecte: 'Architecte', commune: 'Commune', entreprise: 'Entreprise', '': 'Non précisé' },
    trav: { placo: 'Placo', peinture: 'Peinture', 'isolation-acoustique': 'Isolation acoustique', 'cloisons-isothermes': 'Cloisons isolantes', 'ne-sait-pas': 'À préciser', autre: 'Hors métiers', plusieurs: 'Plusieurs prestations' },
    surface: { 'moins-15': 'Moins de 15 m²', '15-50': '15 à 50 m²', '50-200': '50 à 200 m²', 'plus-200': 'Plus de 200 m²', 'ne-sait-pas': 'Ne sait pas', '': 'Non précisée' },
    delai: { 'moins-1-mois': 'Moins d’un mois', '1-3-mois': '1 à 3 mois', '3-6-mois': '3 à 6 mois', 'non-defini': 'Pas défini', '': 'Non précisé' },
    statut: { nouvelle: 'Nouvelle', contact_etabli: 'Contact établi', visite_planifiee: 'Visite planifiée', offre_envoyee: 'Offre envoyée', signee: 'Signée', perdue: 'Perdue', hors_cible: 'Hors cible' },
    critere: { type_client: 'Type de client', service: 'Travaux', surface: 'Surface', zone: 'Zone', delai: 'Délai', source: 'Source', bonus: 'Bonus', malus: 'Malus' },
    cat: { 'google-ads': 'Google Ads', 'recherche-google': 'recherche Google', 'carte-google': 'fiche Google', recommandation: 'recommandation', partenaire: 'partenaire', b2b: 'prospection B2B', meta: 'Meta', linkedin: 'LinkedIn', 'appel-direct': 'appel direct', 'direct-inconnu': 'direct ou inconnu', autre: 'autre' },
    connu: { recommandation: 'Recommandation d’un proche', 'regie-architecte': 'Une régie ou un architecte', 'carte-google': 'Carte Google', 'recherche-google': 'Recherche Google', autre: 'Autre', '': '—' },
    chantier: { a_planifier: 'À planifier', planifie: 'Planifié', en_cours: 'En cours', termine: 'Terminé', clos: 'Clos' }
  };
  var CANAUX = [
    { id: 'google-ads', nom: 'Google Ads', court: 'Google Ads', cats: ['google-ads'], payant: true },
    { id: 'meta', nom: 'Meta', court: 'Meta', cats: ['meta'], payant: true },
    { id: 'b2b', nom: 'Prospection B2B', court: 'B2B', cats: ['b2b'], payant: true },
    { id: 'recherche', nom: 'Recherche Google', court: 'Recherche', cats: ['recherche-google'] },
    { id: 'fiche', nom: 'Fiche Google', court: 'Fiche Google', cats: ['carte-google'] },
    { id: 'recommandation', nom: 'Recommandation et partenaires', court: 'Recommandation', cats: ['recommandation', 'partenaire'] },
    { id: 'autres', nom: 'Autres et inconnu', court: 'Autres', cats: ['appel-direct', 'direct-inconnu', 'site-referent', 'autre'] }
  ];
  var CANAL_PAR_ID = {}; CANAUX.forEach(function (c) { CANAL_PAR_ID[c.id] = c; });
  var USERS = {}; M.UTILISATEURS.forEach(function (u) { USERS[u.id] = u; });
  var PRESTATIONS = ['placo', 'peinture', 'isolation-acoustique', 'cloisons-isothermes'];
  var B2B = ['regie', 'architecte', 'commune', 'entreprise'];

  /* ================= Scoring (comme Scoring.php) ================= */
  function serviceDe(trav) {
    var p = trav.filter(function (x) { return PRESTATIONS.indexOf(x) >= 0; });
    if (p.length >= 2) return 'plusieurs';
    if (p.length === 1) return p[0];
    return trav[0] || '';
  }
  function calculer(r) {
    var g = M.GRILLE, detail = [], regles = [], hc = [];
    function aj(c, v, p) { detail.push({ critere: c, valeur: v, points: p }); }
    var type = r.type || '';
    aj('type_client', L.type[type] || type, g.type_client[type] != null ? g.type_client[type] : g.type_client['']);
    var s = r.service, ps = Object.prototype.hasOwnProperty.call(g.service, s) ? g.service[s] : g.service[''];
    if (ps === null) { hc.push('service hors des 4 prestations'); ps = 0; }
    aj('service', L.trav[s] || s || 'Non précisé', ps);
    var surf = r.surf || '';
    aj('surface', L.surface[surf], g.surface[surf] != null ? g.surface[surf] : g.surface['']);
    var zone = String(r.zone || 'inconnue'), pz = Object.prototype.hasOwnProperty.call(g.zone, zone) ? g.zone[zone] : g.zone.inconnue;
    if (pz === null) { hc.push('hors Suisse romande'); pz = 0; }
    else if (zone === '3' && (g.regles.zone3_sans_penalite_types_client.indexOf(type) >= 0 || g.regles.zone3_sans_penalite_surfaces.indexOf(surf) >= 0)) {
      pz = g.zone['2']; regles.push('zone 3 sans pénalité (B2B ou plus de 50 m²)');
    }
    aj('zone', 'zone ' + zone, pz);
    var delai = r.delai || '';
    aj('delai', L.delai[delai], g.delai[delai] != null ? g.delai[delai] : g.delai['']);
    var cat = r.src, psrc = g.source[cat] != null ? g.source[cat] : g.source.autre, lsrc = L.cat[cat] || cat;
    if (r.connu && g.connu_par[r.connu]) {
      var dec = g.connu_par[r.connu];
      if ((g.source[dec] || 0) > psrc) { psrc = g.source[dec]; lsrc = (L.cat[dec] || dec) + ' (déclaré)'; }
    }
    aj('source', lsrc, psrc);
    var tel = !!r.tel, msg = (r.msg || '').trim();
    if ((r.fic || 0) > 0) aj('bonus', 'photo ou plan joint', g.bonus.fichier_joint);
    if (tel && r.canal === 'site') aj('bonus', 'téléphone fourni', g.bonus.telephone_fourni);
    if (msg === '' && !tel) aj('malus', 'message vide et aucun téléphone', g.bonus.message_vide_sans_telephone);
    var score = somme(detail.map(function (d) { return d.points; }));
    var prio = score >= g.seuils.A ? 'A' : (score >= g.seuils.B ? 'B' : 'C');
    if (prio === 'C' && g.regles.plancher_B_types_client.indexOf(type) >= 0) { prio = 'B'; regles.push('commune, régie ou architecte : jamais en dessous de B'); }
    if (prio !== 'A' && delai === g.regles.urgence_delai && g.regles.urgence_mots.some(function (m) { return msg.toLowerCase().indexOf(m) >= 0; })) { prio = 'A'; regles.push('dégât ou fin de bail imminente : A'); }
    if (hc.length) prio = 'hors-cible';
    return { score: score, priorite: prio, detail: detail, regles: regles, hors_cible: hc };
  }

  /* ================= Préparation des demandes fictives ================= */
  var D = M.DEMANDES.slice().sort(function (a, b) { return t(a.d) - t(b.d); });
  var numero = 10;
  D.forEach(function (r, i) {
    if (!r.ref) { r.ref = 'AC-2027-' + ('000' + numero).slice(-4); numero++; }
    r.recu = t(r.d); r.mois = r.d.slice(0, 7);
    r.service = serviceDe(r.trav);
    r.sc = calculer(r); r.prio = r.sc.priorite;
    r.ech = echeance(r.prio, r.recu);
    r.premier = r.canal === 'telephone' ? r.recu : (r.contact ? t(r.contact) : null);
    r.tents = (r.tent || []).map(t);
    r.statut = r.perdue ? 'perdue' : r.signee ? 'signee' : r.offre ? 'offre_envoyee' : r.visite ? 'visite_planifiee' : r.premier ? 'contact_etabli' : 'nouvelle';
    var cat = r.src, declare = false;
    if ((cat === 'appel-direct' || cat === 'direct-inconnu') && r.connu && r.connu !== 'autre' && M.GRILLE.connu_par[r.connu]) { cat = M.GRILLE.connu_par[r.connu]; declare = true; }
    r.canalM = CANAUX.filter(function (c) { return c.cats.indexOf(cat) >= 0; })[0] || CANAL_PAR_ID.autres;
    r.canalDeclare = declare;
    r.telAff = r.tel ? '079 000 00 ' + pad(i + 1) : '';
    r.email = r.mail ? ascii(r.nom) + '@example.com' : '';
    r.b2b = B2B.indexOf(r.type) >= 0;
    if (r.offre) r.offre.t = t(r.offre.le);
    if (r.signee) r.signee.t = t(r.signee.le);
    if (r.perdue) r.perdue.t = t(r.perdue.le);
    if (r.visite) r.visite.t = t(r.visite.le);
  });
  var PAR_REF = {}; D.forEach(function (r) { PAR_REF[r.ref] = r; });

  function ouverte(r) { return ['nouvelle', 'contact_etabli', 'visite_planifiee', 'offre_envoyee'].indexOf(r.statut) >= 0; }
  function prochaineEch(r) { return r.tents.length ? jourOuvrableSuivant(r.tents[r.tents.length - 1], 10) : r.ech; }
  function enRetard(r) { return r.statut === 'nouvelle' && NOW > prochaineEch(r); }
  function relance(r) {
    if (r.statut !== 'offre_envoyee') return null;
    var j = Math.floor((AUJ - t(r.offre.le)) / 1440);
    var appel = r.prio === 'A' || r.b2b;
    var etape = j >= 21 ? 3 : j >= 10 ? 2 : j >= 3 ? 1 : 0;
    var txt;
    if (j < 3) txt = 'J+3 : e-mail « bien reçue ? » ' + dateH(ouvrableApres(r.offre.le, 3));
    else if (j === 10 && appel) txt = 'Appeler aujourd’hui (J+10)';
    else if (j < 10) txt = (appel ? 'J+10 : appel ' : 'J+10 : e-mail ') + dateC(ouvrableApres(r.offre.le, 10));
    else if (j < 21) txt = 'J+21 : e-mail « où en êtes-vous ? » ' + dateC(ouvrableApres(r.offre.le, 21));
    else if (j < 35) txt = 'J+35 : décision ' + dateC(ouvrableApres(r.offre.le, 35));
    else txt = 'Clore cette offre ? Clôture automatique le ' + dateC(ouvrableApres(r.offre.le, 45));
    return { jours: j, etape: etape, texte: txt, decision: j >= 35, appelAujourdhui: j === 10 && appel };
  }
  function prochaineAction(r) {
    if (r.statut === 'nouvelle') return r.prio === 'hors-cible' ? 'Valider la réorientation' : (r.tents.length ? 'Nouvel essai (' + (r.tents.length + 1) + 'e)' : 'Premier appel');
    if (r.statut === 'contact_etabli') return 'Planifier la visite';
    if (r.statut === 'visite_planifiee') return r.visite.faite ? 'Envoyer l’offre' : 'Visite ' + dateH(r.visite.t);
    if (r.statut === 'offre_envoyee') return relance(r).texte;
    if (r.statut === 'signee') return r.chantier ? 'Chantier : ' + L.chantier[r.chantier.statut].toLowerCase() : '—';
    return '—';
  }

  /* ================= Indicateurs (plan §5) ================= */
  function demandesMois(mk) { return D.filter(function (r) { return r.mois === mk; }); }
  function comptes(mk) {
    if (M.HISTORIQUE[mk]) { var h = M.HISTORIQUE[mk]; return { demandes: h.demandes, A: h.A, B: h.B, C: h.C, HC: h.HC }; }
    var c = { demandes: 0, A: 0, B: 0, C: 0, HC: 0 };
    demandesMois(mk).forEach(function (r) { c.demandes++; c[r.prio === 'hors-cible' ? 'HC' : r.prio]++; });
    return c;
  }
  function partAB(c) { var q = c.A + c.B + c.C; return q ? (c.A + c.B) / q : null; }
  function offresEnvoyees(mk) {
    if (M.HISTORIQUE[mk]) return M.HISTORIQUE[mk].offres;
    return D.filter(function (r) { return r.offre && r.offre.le.slice(0, 7) === mk; }).length;
  }
  function toutesOffres() {
    var l = D.filter(function (r) { return r.offre; }).map(function (r) { return { le: r.offre.le, signee: r.signee ? r.signee.le : null, m: r.signee ? r.signee.m : 0, ref: r.ref, canal: r.canalM.id }; });
    return l.concat(M.OFFRES_ANCIENNES.map(function (o) { return { le: o.le, signee: o.signee || null, m: o.m || 0, ref: null, canal: null }; }));
  }
  function signees(mk) { return toutesOffres().filter(function (o) { return o.signee && o.signee.slice(0, 7) === mk; }); }
  function tauxDemandeOffre(mk) { var p = moisPrec(mk); if (!p) return null; var d = comptes(p).demandes; return d ? { taux: offresEnvoyees(mk) / d, offres: offresEnvoyees(mk), demandes: d, moisDemandes: p } : null; }
  function cohorte(asOf) {
    var debut = asOf - 180 * 1440, fin = asOf - 60 * 1440;
    var l = toutesOffres().filter(function (o) { var x = t(o.le); return x >= debut && x <= fin; });
    var s = l.filter(function (o) { return o.signee && t(o.signee) <= asOf; }).length;
    return { taux: l.length ? s / l.length : null, signees: s, offres: l.length };
  }
  function panierMoyen(asOf) {
    var l = toutesOffres().filter(function (o) { return o.signee && t(o.signee) <= asOf && t(o.signee) > asOf - 182 * 1440; });
    return l.length ? somme(l.map(function (o) { return o.m; })) / l.length : null;
  }
  function delaiPremierContact(mk, prio) {
    var l = demandesMois(mk).filter(function (r) { return r.canal !== 'telephone' && r.premier && (!prio || r.prio === prio); });
    return { mediane: mediane(l.map(function (r) { return minutesOuvrables(r.recu, r.premier); })), n: l.length };
  }
  function rappeleesDansDelai(mk, prio, asOf) {
    var l = demandesMois(mk).filter(function (r) { return r.canal !== 'telephone' && r.prio === prio && r.ech <= asOf; });
    var ok = l.filter(function (r) { var premierAppel = Math.min(r.premier || Infinity, r.tents[0] || Infinity); return premierAppel <= r.ech; });
    return { ok: ok.length, total: l.length };
  }
  function depense(mk, canalId) { var d = M.DEPENSES[canalId]; return d ? (d[mk] || 0) : 0; }
  function depensePayante(mk) { return depense(mk, 'google-ads') + depense(mk, 'meta') + depense(mk, 'b2b'); }
  function demandesPayantes(mk) { return demandesMois(mk).filter(function (r) { return r.canalM.payant; }).length; }
  function objectif(cle, mk) {
    var o = M.OBJECTIFS[cle], m = M.MOIS_M[mk];
    if (!o || !m || m < 3) return null;
    return m <= 6 ? o.M3 + (o.M6 - o.M3) * (m - 3) / 3 : o.M6 + (o.M12 - o.M6) * (m - 6) / 6;
  }
  function etiquetteM(mk) { return 'M' + M.MOIS_M[mk]; }
  function projectionDemandes(mk, valeur) { var e = joursOuvrablesEcoules(mk); return e > 0 ? valeur * joursOuvrablesMois(mk) / e : null; }
  function projectionVisites(mk, valeur) { var p = parts(NOW), jours = new Date(Date.UTC(p.y, p.m, 0)).getUTCDate(); var ecoules = p.j - 1 + (p.h * 60 + p.mi) / 1440; return valeur * jours / ecoules; }
  function cplMax(asOf) {
    var pm = panierMoyen(asOf), co = cohorte(asOf);
    var taux = co.offres >= 10 ? co.taux : M.OBJECTIFS.offreSignee.M6 / 100;
    // Taux de signature par demande = demande→offre × offre→signée (plan d'acquisition v4 §2.5, qui corrige v2 §1.3)
    var tdo = M.OBJECTIFS.demandeOffre.M6 / 100;
    return pm ? { max: pm * M.PARAMETRES.margeBrute * tdo * taux, panier: pm, taux: taux, tdo: tdo } : null;
  }
  function chantiers() { return D.filter(function (r) { return r.chantier; }); }
  function carnet() {
    var j = somme(chantiers().filter(function (r) { return ['a_planifier', 'planifie', 'en_cours'].indexOf(r.chantier.statut) >= 0; })
      .map(function (r) { return r.chantier.restant != null ? r.chantier.restant : r.chantier.jours; }));
    var total = j + M.PARAMETRES.horsAcquisitionJours;
    return { joursAcquisition: j, total: total, semaines: total / (M.PARAMETRES.equipes * 5) };
  }
  function avisSansReponse() { return M.AVIS.liste.filter(function (a) { return a.reponse !== 'publiee'; }); }

  /* ================= Petits composants ================= */
  function prio(r) {
    if (r.prio === 'hors-cible') return '<span class="prio prio-HC">Hors cible</span>';
    return '<span class="prio prio-' + r.prio + '"><span class="sr">Priorité </span>' + r.prio + '</span>';
  }
  function prioScore(r) { return '<span class="prio-score">' + prio(r) + '<span class="discret">' + r.sc.score + '</span></span>'; }
  function statut(r) {
    var s = (r.prio === 'hors-cible' && r.statut === 'nouvelle') ? 'hors_cible' : r.statut;
    return '<span class="statut statut-' + s + '">' + esc(s === 'hors_cible' ? 'Hors cible à valider' : L.statut[s]) + '</span>';
  }
  function travaux(r) { return r.trav.map(function (x) { return L.trav[x] || x; }).join(', '); }
  function nomLien(r) { return '<a href="#/demandes/' + r.ref + '">' + esc(r.nom) + '</a>' + (r.org ? '<span class="org">' + esc(r.org) + '</span>' : ''); }
  function echeanceHTML(r) {
    var e = prochaineEch(r);
    if (NOW > e) return '<div class="echeance retard"><span class="texte"><span class="icone-alerte" aria-hidden="true">!</span>En retard</span><span class="petit">depuis ' + esc(dateH(e)) + '</span><span class="reglet" aria-hidden="true"><span></span></span></div>';
    var debut = r.tents.length ? r.tents[r.tents.length - 1] : r.recu;
    var frac = Math.max(0.04, Math.min(1, (e - NOW) / Math.max(1, e - debut)));
    var reste = e - NOW;
    var txt = reste < 60 ? 'dans ' + reste + ' min' : (cleJour(e) === cleJour(NOW) ? 'aujourd’hui ' + heure(e) : dateH(e));
    return '<div class="echeance"><span class="texte">Rappeler ' + esc(txt) + '</span><span class="reglet" aria-hidden="true"><span style="width:' + Math.round(frac * 100) + '%"></span></span></div>';
  }
  function montant(r) { if (r.signee) return chf(r.signee.m); if (r.offre) return chf(r.offre.m); return '—'; }
  function aide(id, texte) {
    return '<button class="aide" type="button" aria-expanded="false" aria-controls="' + id + '" title="Définition">?</button>' +
      '';
  }
  function definition(id, texte) { return '<p class="definition" id="' + id + '" hidden>' + esc(texte) + '</p>'; }
  function metre(valeur, max, cible, etiquette) {
    var w = Math.max(0, Math.min(100, valeur / max * 100)), c = Math.max(0, Math.min(100, cible / max * 100));
    return '<div class="metre" role="img" aria-label="' + esc(etiquette) + '"><span class="rempli" style="width:' + w.toFixed(1) + '%"></span><span class="cible" style="left:calc(' + c.toFixed(1) + '% - 1px)"></span></div>';
  }
  function etat(ok, texteOk, texteKo, neutre) {
    if (neutre) return '<div class="etat"><span class="icone-ok" aria-hidden="true">~</span>' + esc(neutre) + '</div>';
    return ok ? '<div class="etat"><span class="icone-ok" aria-hidden="true">✓</span>' + esc(texteOk) + '</div>'
      : '<div class="etat ko"><span class="icone-alerte" aria-hidden="true">!</span>' + esc(texteKo) + '</div>';
  }
  function tableDonnees(titre, entetes, lignes) {
    return '<details class="donnees"><summary>Voir les données</summary><div class="defile"><table class="tableau"><caption class="sr">' + esc(titre) + '</caption><thead><tr>' +
      entetes.map(function (h, i) { return '<th scope="col"' + (i ? ' class="num"' : '') + '>' + esc(h) + '</th>'; }).join('') + '</tr></thead><tbody>' +
      lignes.map(function (l) { return '<tr>' + l.map(function (c, i) { return i ? '<td class="num">' + esc(c) + '</td>' : '<th scope="row">' + esc(c) + '</th>'; }).join('') + '</tr>'; }).join('') +
      '</tbody></table></div></details>';
  }

  /* ================= Graphiques (SVG, une teinte ou une rampe de gris ordonnée) ================= */
  function pasNet(max, n) {
    var brut = max / (n || 4), p = Math.pow(10, Math.floor(Math.log10(brut))), f = brut / p;
    return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * p;
  }
  function barreHaut(x, y, w, h, r) {
    if (h <= 0) return '';
    r = Math.min(r, h, w / 2);
    return 'M' + x + ',' + (y + h) + 'V' + (y + r) + 'Q' + x + ',' + y + ' ' + (x + r) + ',' + y + 'H' + (x + w - r) + 'Q' + (x + w) + ',' + y + ' ' + (x + w) + ',' + (y + r) + 'V' + (y + h) + 'Z';
  }
  function barreDroite(x, y, w, h, r) {
    if (w <= 0) return '';
    r = Math.min(r, w, h / 2);
    return 'M' + x + ',' + y + 'H' + (x + w - r) + 'Q' + (x + w) + ',' + y + ' ' + (x + w) + ',' + (y + r) + 'V' + (y + h - r) + 'Q' + (x + w) + ',' + (y + h) + ' ' + (x + w - r) + ',' + (y + h) + 'H' + x + 'Z';
  }
  function tip(lignes) { return ' role="img" tabindex="0" aria-label="' + esc(lignes.join(', ')) + '" data-tip="' + esc(lignes.join('|')) + '"'; }

  /* Demandes par mois, empilées par priorité (A en bas, la plus foncée), objectif du mois en trait. */
  function graphiqueDemandesMois() {
    var W = 560, H = 230, ml = 34, mr = 10, mt = 18, mb = 30;
    var data = M.MOIS.map(function (mk) {
      var c = comptes(mk), courant = mk === cleJour(NOW).slice(0, 7);
      return { mk: mk, c: c, obj: objectif('demandes', mk), proj: courant ? projectionDemandes(mk, c.demandes) : null };
    });
    var max = Math.max.apply(null, data.map(function (d) { return Math.max(d.c.demandes, d.obj || 0, d.proj || 0); }));
    var pas = pasNet(max, 4), ymax = Math.ceil(max / pas) * pas;
    var ph = H - mt - mb, pw = W - ml - mr, bw = 24, slot = pw / data.length;
    function y(v) { return mt + ph - v / ymax * ph; }
    var s = '<svg class="graphique" viewBox="0 0 ' + W + ' ' + H + '" role="group" aria-label="Demandes enregistrées par mois et par priorité, avec l’objectif du mois">';
    for (var v = 0; v <= ymax; v += pas) s += '<line class="grille" x1="' + ml + '" x2="' + (W - mr) + '" y1="' + y(v) + '" y2="' + y(v) + '"/><text x="' + (ml - 6) + '" y="' + (y(v) + 4) + '" text-anchor="end">' + v + '</text>';
    s += '<line class="axe" x1="' + ml + '" x2="' + (W - mr) + '" y1="' + y(0) + '" y2="' + y(0) + '"/>';
    data.forEach(function (d, i) {
      var x = ml + slot * i + (slot - bw) / 2, base = 0, segs = [['A', 'ord-5'], ['B', 'ord-3'], ['C', 'ord-1']];
      var dernier = segs.filter(function (sg) { return d.c[sg[0]] > 0; }).pop();
      segs.forEach(function (sg) {
        var n = d.c[sg[0]]; if (!n) return;
        var y0 = y(base + n), h = y(base) - y0 - (base > 0 ? 2 : 0);
        var path = sg === dernier && !d.c.HC ? barreHaut(x, y0, bw, h, 4) : 'M' + x + ',' + y0 + 'h' + bw + 'v' + h + 'h' + (-bw) + 'Z';
        s += '<path class="' + sg[1] + '" d="' + path + '"' + tip([n + ' demande' + (n > 1 ? 's' : '') + ' ' + sg[0], moisL(d.mk)]) + '/>';
        base += n;
      });
      if (d.c.HC) {
        var yh = y(base + d.c.HC), hh = y(base) - yh - 2;
        s += '<rect x="' + (x + 1) + '" y="' + (yh + 1) + '" width="' + (bw - 2) + '" height="' + Math.max(1, hh - 2) + '" fill="none" stroke="currentColor" style="color:var(--texte-3)" stroke-width="1.5"' + tip([d.c.HC + ' hors cible', moisL(d.mk)]) + '/>';
        base += d.c.HC;
      }
      if (d.proj && d.proj > d.c.demandes) {
        s += '<rect class="projection" x="' + x + '" y="' + y(d.proj) + '" width="' + bw + '" height="' + (y(d.c.demandes) - y(d.proj) - 2) + '"' + tip(['Projection ≈ ' + nb(d.proj), 'fin ' + moisL(d.mk)]) + '/>';
      }
      s += '<text class="t-fort" x="' + (x + bw / 2) + '" y="' + (y(Math.max(d.c.demandes, d.proj || 0, d.obj || 0)) - 7) + '" text-anchor="middle">' + d.c.demandes + '</text>';
      if (d.obj) s += '<line class="objectif" x1="' + (x - 6) + '" x2="' + (x + bw + 6) + '" y1="' + y(d.obj) + '" y2="' + y(d.obj) + '"' + tip(['Objectif ' + nb(d.obj), etiquetteM(d.mk) + ', ' + moisL(d.mk)]) + '/>';
      s += '<text x="' + (x + bw / 2) + '" y="' + (H - 10) + '" text-anchor="middle">' + moisCourt(d.mk) + (d.proj ? ' *' : '') + '</text>';
    });
    s += '</svg>';
    var leg = '<ul class="legende"><li><i style="background:var(--ord-5)"></i>A</li><li><i style="background:var(--ord-3)"></i>B</li><li><i style="background:var(--ord-1)"></i>C</li><li><i style="border:1.5px solid var(--texte-3)"></i>Hors cible</li><li><i class="trait"></i>Objectif du mois (v2, interpolé)</li></ul>';
    var tab = tableDonnees('Demandes par mois', ['Mois', 'Demandes', 'A', 'B', 'C', 'Hors cible', 'Objectif'], data.map(function (d) { return [moisL(d.mk), d.c.demandes, d.c.A, d.c.B, d.c.C, d.c.HC, d.obj ? nb(d.obj) : '—']; }));
    return leg + s + '<p class="petit discret">* avril au 22 ; le contour en pointillé est la projection de fin de mois.</p>' + tab;
  }

  /* Entonnoir des 3 derniers mois (février à avril) : rampe de gris ordonnée, la plus foncée = signée. */
  function graphiqueEntonnoir() {
    var cohorteD = D.filter(function (r) { return r.mois >= '2027-02'; });
    var etapes = [
      ['Demandes enregistrées', cohorteD.length, 'ord-1'],
      ['Qualifiées (A, B, C)', cohorteD.filter(function (r) { return r.prio !== 'hors-cible'; }).length, 'ord-2'],
      ['Visite planifiée', cohorteD.filter(function (r) { return r.visite; }).length, 'ord-3'],
      ['Offre envoyée', cohorteD.filter(function (r) { return r.offre; }).length, 'ord-4'],
      ['Signée', cohorteD.filter(function (r) { return r.signee; }).length, 'ord-5']
    ];
    var W = 560, lab = 168, val = 92, rh = 34, H = etapes.length * rh + 6, max = etapes[0][1];
    var s = '<svg class="graphique" viewBox="0 0 ' + W + ' ' + H + '" role="group" aria-label="Entonnoir des demandes reçues de février à avril">';
    etapes.forEach(function (e, i) {
      var y = i * rh + 4, w = Math.max(2, (W - lab - val) * e[1] / max);
      var taux = i ? (etapes[i - 1][1] ? e[1] / etapes[i - 1][1] : 0) : null;
      s += '<text x="0" y="' + (y + 17) + '" class="t-fort">' + e[0] + '</text>';
      s += '<path class="' + e[2] + '" d="' + barreDroite(lab, y + 4, w, 20, 4) + '"' + tip([e[1] + ' demandes', e[0] + (taux != null ? ', ' + pct(taux) + ' de l’étape précédente' : '')]) + '/>';
      s += '<text x="' + (lab + w + 6) + '" y="' + (y + 18) + '" class="t-fort">' + e[1] + '</text>';
      if (taux != null) s += '<text x="' + (W) + '" y="' + (y + 18) + '" text-anchor="end">' + pct(taux) + '</text>';
    });
    s += '</svg>';
    var perdues = cohorteD.filter(function (r) { return r.statut === 'perdue'; }), motifs = {};
    perdues.forEach(function (r) { motifs[r.perdue.motif] = (motifs[r.perdue.motif] || 0) + 1; });
    var enCours = cohorteD.filter(function (r) { return r.statut === 'offre_envoyee'; }).length;
    var txt = '<p class="petit discret">À droite : passage depuis l’étape précédente. Offres encore en attente : ' + enCours + '. Perdues : ' + perdues.length + ' (' +
      Object.keys(motifs).sort(function (a, b) { return motifs[b] - motifs[a]; }).map(function (k) { return M.MOTIFS[k].toLowerCase() + ' ' + motifs[k]; }).join(', ') + ').</p>';
    return s + txt + tableDonnees('Entonnoir', ['Étape', 'Demandes', 'Passage'], etapes.map(function (e, i) { return [e[0], e[1], i ? pct(e[1] / etapes[i - 1][1]) : '—']; }));
  }

  /* Barres horizontales classées, une seule teinte. */
  function barresClassees(titre, items, format, cible) {
    items = items.slice().sort(function (a, b) { return b.v - a.v; });
    var W = 360, lab = 112, val = 84, rh = 28, H = items.length * rh + (cible ? 22 : 6);
    var max = Math.max.apply(null, items.map(function (i) { return i.v; }).concat([cible ? cible.v : 0, 1]));
    function x(v) { return lab + (W - lab - val) * v / max; }
    var s = '<svg class="graphique" viewBox="0 0 ' + W + ' ' + H + '" role="group" aria-label="' + esc(titre) + '">';
    if (cible) {
      s += '<line class="objectif" x1="' + x(cible.v) + '" x2="' + x(cible.v) + '" y1="0" y2="' + (H - 18) + '"/>';
      s += '<text x="' + x(cible.v) + '" y="' + (H - 4) + '" text-anchor="middle">' + esc(cible.lib) + '</text>';
    }
    items.forEach(function (it, i) {
      var y = i * rh + 4;
      s += '<text x="0" y="' + (y + 16) + '">' + esc(it.lib) + '</text>';
      if (it.v > 0) s += '<path class="serie" d="' + barreDroite(lab, y + 4, x(it.v) - lab, 18, 4) + '"' + tip([format(it.v), it.lib]) + '/>';
      s += '<text class="t-fort" x="' + (x(it.v) + 6) + '" y="' + (y + 17) + '">' + esc(it.v > 0 ? format(it.v) : (it.vide || '0')) + '</text>';
    });
    return s + '</svg>';
  }

  /* Courbe avec curseur (survol et flèches du clavier). */
  function courbe(id, points, opts) {
    var W = 560, H = 210, ml = 34, mr = 16, mt = 14, mb = 28;
    var vals = points.map(function (p) { return p[1]; }), cibles = opts.cibles || [];
    var max = Math.max.apply(null, vals.concat(cibles.map(function (c) { return c.v; })));
    var pas = pasNet(max, 4), ymax = Math.ceil(max / pas) * pas, n = opts.n || points.length;
    function x(i) { return ml + (W - ml - mr) * i / (n - 1); }
    function y(v) { return mt + (H - mt - mb) * (1 - v / ymax); }
    var s = '<svg class="graphique courbe" id="' + id + '" viewBox="0 0 ' + W + ' ' + H + '" role="group" aria-label="' + esc(opts.titre) + '">';
    for (var v = 0; v <= ymax; v += pas) s += '<line class="grille" x1="' + ml + '" x2="' + (W - mr) + '" y1="' + y(v) + '" y2="' + y(v) + '"/><text x="' + (ml - 6) + '" y="' + (y(v) + 4) + '" text-anchor="end">' + nb(v) + '</text>';
    s += '<line class="axe" x1="' + ml + '" x2="' + (W - mr) + '" y1="' + y(0) + '" y2="' + y(0) + '"/>';
    var d = points.map(function (p, i) { return (i ? 'L' : 'M') + x(i).toFixed(1) + ',' + y(p[1]).toFixed(1); }).join('');
    s += '<path class="aire" d="' + d + 'L' + x(points.length - 1).toFixed(1) + ',' + y(0) + 'L' + x(0) + ',' + y(0) + 'Z"/>';
    s += '<path class="ligne" d="' + d + '"/>';
    points.forEach(function (p, i) { if (i % (opts.pasEtiquette || 1) === 0 || i === points.length - 1) s += '<text x="' + x(i) + '" y="' + (H - 8) + '" text-anchor="middle">' + esc(p[0]) + '</text>'; });
    cibles.forEach(function (c) {
      s += '<circle class="cible-pt" cx="' + x(c.i) + '" cy="' + y(c.v) + '" r="5"/><text x="' + (x(c.i) - 8) + '" y="' + (y(c.v) - 9) + '" text-anchor="end">' + esc(c.lib) + '</text>';
    });
    var last = points.length - 1;
    s += '<circle class="point" cx="' + x(last) + '" cy="' + y(points[last][1]) + '" r="4.5"/>';
    s += '<text class="t-fort" x="' + (x(last) + 8) + '" y="' + (y(points[last][1]) + 4) + '">' + nb(points[last][1]) + '</text>';
    s += '<g class="survol" style="display:none"><line class="curseur" y1="' + mt + '" y2="' + y(0) + '"/><circle class="point" r="5"/></g>';
    s += '<rect class="zone-curseur" x="' + ml + '" y="' + mt + '" width="' + (W - ml - mr) + '" height="' + (H - mt - mb) + '" fill="transparent" tabindex="0" role="img" aria-label="Courbe interactive : flèches gauche et droite pour lire chaque point"/>';
    s += '</svg>';
    COURBES[id] = { points: points, x: x, y: y, unite: opts.unite || '' };
    return s;
  }
  var COURBES = {};

  function sparkline(vals) {
    var W = 64, H = 20, max = Math.max.apply(null, vals.concat([1]));
    var pts = vals.map(function (v, i) { return (2 + (W - 6) * i / (vals.length - 1)).toFixed(1) + ',' + (H - 3 - (H - 6) * v / max).toFixed(1); });
    var last = pts[pts.length - 1].split(',');
    return '<svg class="graphique" width="' + W + '" height="' + H + '" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Demandes par mois : ' + vals.join(', ') + '"><polyline class="ligne" style="stroke-width:1.5" points="' + pts.join(' ') + '"/><circle class="point" cx="' + last[0] + '" cy="' + last[1] + '" r="3"/></svg>';
  }

  /* ================= Écrans ================= */
  var ECRANS = {};

  /* ---------- Vue d'ensemble ---------- */
  ECRANS.vue = function (q) {
    var mk = q.mois || '2027-04', courant = mk === '2027-04', asOf = courant ? NOW : finMois(mk), prec = moisPrec(mk);
    var c = comptes(mk), cp = comptes(prec);
    var dmd = c.demandes, objD = objectif('demandes', mk), proj = courant ? projectionDemandes(mk, dmd) : null;
    var pab = partAB(c), objPab = objectif('partAB', mk) / 100;
    var del = delaiPremierContact(mk, 'A'), objDel = objectif('delaiA', mk) * 60, delTous = delaiPremierContact(mk);
    var dd = rappeleesDansDelai(mk, 'A', asOf);
    var tdo = tauxDemandeOffre(mk), tdoP = tauxDemandeOffre(prec), objTdo = objectif('demandeOffre', mk) / 100;
    var sig = signees(mk), ca = somme(sig.map(function (o) { return o.m; })), objCa = objectif('chantiers', mk) * M.PARAMETRES.panierReference;
    var co = cohorte(asOf), objCo = objectif('offreSignee', mk) / 100;
    var dep = depensePayante(mk), dp = demandesPayantes(mk), cpl = dp ? dep / dp : null, cm = cplMax(asOf), cible = cm ? cm.max / 3 : null;

    var retards = D.filter(enRetard);
    var retA = retards.filter(function (r) { return r.prio === 'A'; }), retAutres = retards.filter(function (r) { return r.prio !== 'A'; });
    var decisions = D.filter(function (r) { var x = relance(r); return x && x.decision; });
    var visitesJour = D.filter(function (r) { return r.visite && !r.visite.faite && cleJour(r.visite.t) === cleJour(NOW); });
    var avisSR = avisSansReponse().filter(function (a) { return (AUJ - t(a.le)) / 1440 >= 2; });
    var cn = carnet();

    function alerte(n, lib, detail, lien, critique) {
      return '<a class="alerte' + (critique && n ? ' critique' : '') + '" href="' + lien + '"><span class="valeur">' + n + '</span><span class="libelle">' + esc(lib) + '</span><span class="detail">' + esc(detail) + '</span></a>';
    }
    var alertes = '<section aria-labelledby="t-alertes"><h2 class="sr" id="t-alertes">Alertes</h2><div class="alertes">' +
      alerte(retA.length, 'Demandes A non rappelées', retA.length ? retA.map(function (r) { return r.nom; }).join(', ') : 'Aucune hors délai', '#/a-traiter', true) +
      alerte(retAutres.length, 'Autres demandes en retard', retAutres.length ? retAutres.map(function (r) { return r.nom; }).join(', ') : 'Aucune', '#/a-traiter', true) +
      alerte(decisions.length, 'Offres sans suite à J+35', decisions.map(function (r) { return r.nom; }).join(', ') || 'Aucune', '#/offres', false) +
      alerte(visitesJour.length, 'Visites aujourd’hui', visitesJour.map(function (r) { return heure(r.visite.t) + ', ' + r.commune; }).join(' ; ') || 'Aucune', '#/a-traiter', false) +
      alerte(avisSR.length, 'Avis sans réponse depuis 48 h', 'Brouillons prêts : ' + avisSansReponse().filter(function (a) { return a.reponse === 'brouillon'; }).length, '#/avis', false) +
      '<a class="alerte" href="#/offres"><span class="valeur">' + nb(cn.semaines, 1) + '</span><span class="libelle">Semaines de carnet</span><span class="detail">Seuil d’alerte : ' + M.PARAMETRES.seuilCarnetSemaines + ' semaines (v2 §1.3)</span></a>' +
      '</div></section>';

    var t1ok = (proj || dmd) >= objD;
    var tuiles = [
      '<div class="tuile"><div class="tete"><span class="libelle">Demandes/mois</span>' + aide('def-1') + '</div>' + definition('def-1', 'Demandes enregistrées dont la date de réception tombe dans le mois, tous canaux, hors spam, doublons et tests. Part A+B = (A + B) / (A + B + C).') +
      '<span class="valeur">' + dmd + (courant ? ' <small>au ' + dateC(NOW) + '</small>' : '') + '</span>' +
      '<span class="objectif">Objectif ' + etiquetteM(mk) + ' : ' + nb(objD) + (proj ? ', projection ≈ ' + nb(proj) : '') + '</span>' +
      metre(proj || dmd, Math.max(objD, proj || dmd) * 1.15, objD, 'Demandes ' + dmd + ' sur un objectif de ' + nb(objD)) +
      '<span class="compl">Part A+B : <b>' + pct(pab) + '</b> (objectif ≥ ' + pct(objPab) + '). Mois précédent : ' + cp.demandes + '</span>' +
      etat(t1ok, courant ? 'En avance sur l’objectif' : 'Objectif atteint', 'En dessous de l’objectif') + '</div>',

      '<div class="tuile"><div class="tete"><span class="libelle">Délai de premier contact, demandes A</span>' + aide('def-2') + '</div>' + definition('def-2', 'Médiane, en heures ouvrables (lu-ve 7 h-18 h, fériés genevois), entre la réception et le premier contact établi, sur les demandes A du mois. Les appels entrants sont exclus.') +
      '<span class="valeur">' + (del.mediane != null ? esc(duree(del.mediane)) : '—') + '</span>' +
      '<span class="objectif">Objectif ' + etiquetteM(mk) + ' : moins de ' + duree(objDel) + ' ouvrables</span>' +
      (del.mediane != null ? metre(del.mediane, objDel * 2, objDel, 'Délai médian ' + duree(del.mediane) + ', objectif ' + duree(objDel)) : '') +
      '<span class="compl">Rappelées dans le délai : <b>' + dd.ok + ' sur ' + dd.total + '</b>, toutes priorités : ' + (delTous.mediane != null ? duree(delTous.mediane) : '—') + '</span>' +
      etat(del.mediane != null && del.mediane <= objDel, 'Dans l’objectif', 'Au-dessus de l’objectif') + '</div>',

      '<div class="tuile"><div class="tete"><span class="libelle">Taux demande→offre</span>' + aide('def-3') + '</div>' + definition('def-3', 'Offres envoyées pendant le mois / demandes enregistrées pendant le mois précédent (définition v2 §1.1).') +
      '<span class="valeur">' + (tdo ? pct(tdo.taux) : '—') + '</span>' +
      '<span class="objectif">Objectif ' + etiquetteM(mk) + ' : ' + pct(objTdo) + '</span>' +
      (tdo ? metre(tdo.taux, Math.max(1, tdo.taux), objTdo, 'Taux ' + pct(tdo.taux) + ', objectif ' + pct(objTdo)) : '') +
      '<span class="compl">' + (tdo ? tdo.offres + ' offres pour ' + tdo.demandes + ' demandes en ' + moisL(tdo.moisDemandes) : '') + (tdoP ? '. Mois précédent : ' + pct(tdoP.taux) : '') + '</span>' +
      etat(tdo && tdo.taux >= objTdo, 'Dans l’objectif', courant ? 'En dessous (mois en cours)' : 'En dessous de l’objectif') + '</div>',

      '<div class="tuile"><div class="tete"><span class="libelle">CA signé</span>' + aide('def-4') + '</div>' + definition('def-4', 'Somme des montants signés (HT) des offres signées pendant le mois. Taux offre→signée : offres signées / offres envoyées entre J−180 et J−60. Objectif de CA : chantiers visés × panier de référence (paramètre fictif, décision G4).') +
      '<span class="valeur">' + chf(ca) + '</span>' +
      '<span class="objectif">' + sig.length + ' chantier' + (sig.length > 1 ? 's' : '') + ' signé' + (sig.length > 1 ? 's' : '') + ', objectif indicatif ' + chf(objCa) + '</span>' +
      metre(ca, Math.max(ca, objCa) * 1.1, objCa, 'CA signé ' + chf(ca) + ', objectif ' + chf(objCa)) +
      '<span class="compl">Taux offre→signée : <b>' + pct(co.taux) + '</b> (' + co.signees + ' sur ' + co.offres + ', objectif ' + pct(objCo) + ')</span>' +
      etat(ca >= objCa, 'Objectif atteint', 'En dessous', courant && ca < objCa ? 'Mois en cours, signatures irrégulières' : null) + '</div>',

      '<div class="tuile"><div class="tete"><span class="libelle">CPL, canaux payants</span>' + aide('def-5') + '</div>' + definition('def-5', 'CPL = dépense / demandes, sur Google Ads, Meta et la prospection B2B. Cible : un tiers du CPL max = panier moyen × marge brute × taux demande→offre × taux offre→signée (plan d’acquisition v4 §2.5). Marge brute : 30 %, paramètre fictif.') +
      '<span class="valeur">' + (cpl != null ? chf(cpl) : '—') + '</span>' +
      '<span class="objectif">Cible ≤ ' + (cible ? chf(cible) : '—') + ' (CPL max ' + (cm ? chf(cm.max) : '—') + ')</span>' +
      (cpl != null && cible ? metre(cpl, Math.max(cpl, cible) * 1.4, cible, 'CPL ' + chf(cpl) + ', cible ' + chf(cible)) : '') +
      '<span class="compl">' + chf(dep) + ' / ' + dp + ' demandes payantes' + (prec && !M.HISTORIQUE[prec] ? '. Mois précédent : ' + chf(depensePayante(prec) / Math.max(1, demandesPayantes(prec))) : '') + '</span>' +
      etat(cpl != null && cible && cpl <= cible, 'Sous la cible', 'Au-dessus de la cible') + '</div>'
    ].join('');

    var vis = M.SITE.visites[mk], cw = M.SITE.contactsWeb[mk], projV = courant ? projectionVisites(mk, vis) : null;
    var avis = M.AVIS.cumul[mk], ia = M.IA.historique[mk];
    var bande = '<div class="bande mt">' +
      '<div><span class="libelle">Visites</span><div class="valeur">' + nb(vis) + '</div><span class="petit discret">Objectif ' + nb(objectif('visites', mk)) + (projV ? ', projection ≈ ' + nb(projV) : '') + '</span></div>' +
      '<div><span class="libelle">Taux visite→contact</span><div class="valeur">' + pct(cw / vis, 1) + '</div><span class="petit discret">' + cw + ' contacts web, objectif ' + pct(objectif('tauxVisiteContact', mk) / 100, 1) + '</span></div>' +
      '<div><span class="libelle">Avis Google</span><div class="valeur">' + avis + ' <small class="petit">note ' + nb(M.AVIS.note, 1) + '</small></div><span class="petit discret">Objectif ' + nb(objectif('avis', mk)) + ' au cumul</span></div>' +
      '<div><span class="libelle">Citations IA</span><div class="valeur">' + (ia != null ? ia + '/10' : '—') + '</div><span class="petit discret">Test du 1er du mois, objectif ' + nb(objectif('citationsIA', mk)) + '/10</span></div>' +
      '</div>';

    var options = ['2027-04', '2027-03', '2027-02'].map(function (m) { return '<option value="' + m + '"' + (m === mk ? ' selected' : '') + '>' + moisL(m) + (m === '2027-04' ? ' (en cours)' : '') + '</option>'; }).join('');
    return '<div class="entete-page"><div><h1 tabindex="-1">Vue d’ensemble</h1><p class="sous-titre">' + esc(courant ? 'Avril 2027, arrêté au ' + dateL(NOW) + ' à ' + heure(NOW) + ' (' + etiquetteM(mk) + ', 16e jour ouvrable sur ' + joursOuvrablesMois(mk) + ')' : moisL(mk) + ', mois complet (' + etiquetteM(mk) + ')') + '</p></div>' +
      '<div class="actions filtres" style="margin-bottom:0"><label>Mois<select id="choix-mois">' + options + '</select></label></div></div>' +
      alertes +
      '<section class="mt" aria-labelledby="t-ind"><h2 class="sr" id="t-ind">Cinq indicateurs du mois</h2><div class="tuiles">' + tuiles + '</div></section>' + bande +
      '<div class="grille-2 mt"><section class="panneau" aria-labelledby="t-ent"><div class="panneau-entete"><h2 id="t-ent">Entonnoir</h2><span class="discret">demandes reçues de février au 22 avril, état aujourd’hui</span></div>' + graphiqueEntonnoir() + '</section>' +
      '<section class="panneau" aria-labelledby="t-dm"><div class="panneau-entete"><h2 id="t-dm">Demandes par mois</h2><span class="discret">6 mois, par priorité</span></div>' + graphiqueDemandesMois() + '</section></div>';
  };

  /* ---------- À traiter ---------- */
  var etatTraiter = { toutes: false };
  ECRANS['a-traiter'] = function () {
    var moi = M.MOI;
    function mien(r) { return etatTraiter.toutes || r.who === moi; }
    var retards = D.filter(enRetard).sort(function (a, b) { return prochaineEch(a) - prochaineEch(b); });
    var aRappeler = D.filter(function (r) { return r.statut === 'nouvelle' && !enRetard(r) && r.prio !== 'hors-cible' && !r.tents.length && mien(r); }).sort(function (a, b) { return a.ech - b.ech; });
    var tentatives = D.filter(function (r) { return r.statut === 'nouvelle' && !enRetard(r) && r.tents.length && mien(r); });
    var demain = jourOuvrableSuivant(NOW, 0);
    var visites = D.filter(function (r) { return r.visite && !r.visite.faite && (cleJour(r.visite.t) === cleJour(NOW) || cleJour(r.visite.t) === cleJour(demain)) && mien(r); }).sort(function (a, b) { return a.visite.t - b.visite.t; });
    var offres = D.filter(function (r) { var x = relance(r); return x && (x.appelAujourdhui || x.decision) && mien(r); });
    var horsCible = D.filter(function (r) { return r.statut === 'nouvelle' && r.prio === 'hors-cible' && !enRetard(r) && mien(r); });

    function ligne(r, quoi, echeance, boutons, retard) {
      return '<li class="ligne-travail' + (retard ? ' retard' : '') + '">' +
        '<div class="qui">' + prio(r) + '<div>' + nomLien(r) + '</div></div><div class="quoi">' + quoi + '</div><div class="echeance-cel">' + echeance + '</div><div class="boutons">' + boutons + '</div></li>';
    }
    function quoiStd(r) { return esc(travaux(r) + ', ' + r.commune) + '<span class="org">' + esc(r.canalM.nom + (r.canal === 'telephone' ? ' (appel)' : '')) + ', ' + esc(USERS[r.who].nom) + '</span>'; }
    function bAppel(r, principal) { return r.tel ? '<button class="btn btn-petit ' + (principal ? 'btn-principal' : '') + '" type="button" data-appeler="' + r.ref + '">Appeler</button>' : '<button class="btn btn-petit" type="button" data-maquette="Répondre par e-mail à ' + esc(r.email) + '">Répondre par e-mail</button>'; }
    function bResultat(r) { return '<button class="btn btn-petit btn-discret" type="button" data-resultat="' + r.ref + '">Résultat</button>'; }
    function section(id, titre, items, rendu, vide) {
      return '<section class="section-travail" aria-labelledby="' + id + '"><h2 id="' + id + '">' + titre + ' <span class="compte">' + items.length + '</span></h2>' +
        (items.length ? '<ul class="liste-travail">' + items.map(rendu).join('') + '</ul>' : '<p class="vide">' + vide + '</p>') + '</section>';
    }
    var prochaine = D.filter(function (r) { return r.statut === 'nouvelle' && !enRetard(r); }).map(prochaineEch).sort(function (a, b) { return a - b; })[0];
    return '<div class="entete-page"><div><h1 tabindex="-1">À traiter</h1><p class="sous-titre">Jeudi 22 avril, ' + heure(NOW) + '. Les retards de tous les associés restent en tête (escalade).</p></div>' +
      '<div class="actions"><div class="bascule" role="group" aria-label="Demandes affichées"><button type="button" data-toutes="0" aria-pressed="' + !etatTraiter.toutes + '">Mes demandes</button><button type="button" data-toutes="1" aria-pressed="' + etatTraiter.toutes + '">Toutes</button></div></div></div>' +
      section('s-retard', 'En retard', retards, function (r) { return ligne(r, quoiStd(r), echeanceHTML(r), bAppel(r, true) + bResultat(r), true); }, 'Aucun retard.') +
      section('s-rappel', 'À rappeler', aRappeler, function (r) { return ligne(r, quoiStd(r), echeanceHTML(r), bAppel(r) + bResultat(r)); }, 'Rien à rappeler pour l’instant.' + (prochaine ? ' Prochaine échéance : ' + esc(dateH(prochaine)) + '.' : '')) +
      section('s-tent', 'Tentatives à refaire', tentatives, function (r) { return ligne(r, quoiStd(r) + '<span class="org">' + r.tents.length + ' appel sans réponse (' + esc(dateH(r.tents[0])) + '), SMS envoyé au prospect</span>', echeanceHTML(r), bAppel(r) + bResultat(r)); }, 'Aucune tentative en attente.') +
      section('s-visites', 'Visites aujourd’hui et demain', visites, function (r) { return ligne(r, esc(travaux(r)) + '<span class="org">' + esc(r.commune + ', ' + USERS[r.who].nom) + '</span>', '<span class="gras">' + esc(dateH(r.visite.t)) + '</span>', '<button class="btn btn-petit btn-discret" type="button" data-maquette="La visite est marquée faite ; l’offre devient la prochaine action.">Visite faite</button>'); }, 'Aucune visite prévue.') +
      section('s-offres', 'Offres : appels et décisions', offres, function (r) { var x = relance(r); return ligne(r, esc('Offre ' + chf(r.offre.m) + ' du ' + dateC(r.offre.t) + ', J+' + x.jours) + '<span class="org">' + esc(x.etape + ' relance' + (x.etape > 1 ? 's' : '') + ' envoyée' + (x.etape > 1 ? 's' : '') + ', aucune réponse') + '</span>', '<span class="' + (x.decision ? 'gras' : '') + '">' + esc(x.texte) + '</span>', x.decision ? '<button class="btn btn-petit btn-discret" type="button" data-action="perdue" data-ref="' + r.ref + '">Clore</button><button class="btn btn-petit btn-discret" type="button" data-maquette="Relances prolongées de 14 jours.">Garder</button>' : bAppel(r) + bResultat(r)); }, 'Aucune offre à traiter aujourd’hui.') +
      section('s-hc', 'Hors cible à valider', horsCible, function (r) { return ligne(r, quoiStd(r) + '<span class="org">' + esc(r.sc.hors_cible.join(', ')) + '</span>', echeanceHTML(r), '<button class="btn btn-petit btn-discret" type="button" data-action="reorientation" data-ref="' + r.ref + '">Voir la réponse</button>'); }, 'Aucune demande hors cible.') +
      '<section class="section-travail" aria-labelledby="s-avis"><h2 id="s-avis">Avis à répondre <span class="compte">' + avisSansReponse().length + '</span></h2><ul class="liste-travail">' +
      avisSansReponse().map(function (a) { return '<li class="ligne-travail"><div class="qui"><span class="prio prio-HC">' + a.note + '/5</span><div><a href="#/avis">' + esc(a.auteur) + '</a></div></div><div class="quoi">' + esc(a.texte.slice(0, 70)) + '…</div><div class="echeance-cel">' + esc('Publié le ' + dateC(t(a.le))) + '</div><div class="boutons"><a class="btn btn-petit btn-discret" href="#/avis">' + (a.reponse === 'brouillon' ? 'Valider le brouillon' : 'Rédiger') + '</a></div></li>'; }).join('') + '</ul></section>';
  };

  /* ---------- Demandes : liste ---------- */
  var filtres = { q: '', periode: 'tout', statut: 'ouvertes', prio: '', canal: '', who: '', retard: false, tri: 'echeance', sens: 1 };
  function filtrer() {
    var q = filtres.q.trim().toLowerCase(), qn = q.replace(/\D/g, '');
    return D.filter(function (r) {
      if (q && !((r.nom + ' ' + (r.org || '') + ' ' + r.ref + ' ' + r.commune).toLowerCase().indexOf(q) >= 0 || (qn.length >= 3 && r.telAff.replace(/\D/g, '').indexOf(qn) >= 0))) return false;
      if (filtres.periode === 'mois' && r.mois !== '2027-04') return false;
      if (filtres.periode === '30j' && r.recu < NOW - 30 * 1440) return false;
      if (filtres.periode === '3m' && r.mois < '2027-02') return false;
      if (filtres.statut === 'ouvertes' && !ouverte(r)) return false;
      if (filtres.statut && filtres.statut !== 'ouvertes' && filtres.statut !== 'toutes' && r.statut !== filtres.statut) return false;
      if (filtres.prio && (filtres.prio === 'HC' ? r.prio !== 'hors-cible' : r.prio !== filtres.prio)) return false;
      if (filtres.canal && r.canalM.id !== filtres.canal) return false;
      if (filtres.who && r.who !== filtres.who) return false;
      if (filtres.retard && !enRetard(r)) return false;
      return true;
    }).sort(function (a, b) {
      var s = filtres.sens;
      if (filtres.tri === 'recu') return (b.recu - a.recu) * s;
      if (filtres.tri === 'score') return (b.sc.score - a.sc.score) * s;
      if (filtres.tri === 'montant') return ((b.signee ? b.signee.m : b.offre ? b.offre.m : 0) - (a.signee ? a.signee.m : a.offre ? a.offre.m : 0)) * s;
      var ka = a.statut === 'nouvelle' ? prochaineEch(a) : 1e12 - a.recu, kb = b.statut === 'nouvelle' ? prochaineEch(b) : 1e12 - b.recu;
      return (ka - kb) * s;
    });
  }
  function selectHTML(id, lib, valeur, options) {
    return '<label>' + esc(lib) + '<select id="' + id + '">' + options.map(function (o) { return '<option value="' + esc(o[0]) + '"' + (o[0] === valeur ? ' selected' : '') + '>' + esc(o[1]) + '</option>'; }).join('') + '</select></label>';
  }
  function filtresHTML() {
    return '<div class="filtres" role="search" aria-label="Filtrer les demandes">' +
      '<label>Recherche<input type="search" id="f-q" value="' + esc(filtres.q) + '" placeholder="Nom, réf., téléphone"></label>' +
      selectHTML('f-periode', 'Période', filtres.periode, [['tout', 'Tout'], ['30j', '30 derniers jours'], ['mois', 'Avril 2027'], ['3m', '3 derniers mois']]) +
      selectHTML('f-statut', 'Statut', filtres.statut, [['ouvertes', 'Ouvertes'], ['toutes', 'Toutes'], ['nouvelle', 'Nouvelle'], ['contact_etabli', 'Contact établi'], ['visite_planifiee', 'Visite planifiée'], ['offre_envoyee', 'Offre envoyée'], ['signee', 'Signée'], ['perdue', 'Perdue']]) +
      selectHTML('f-prio', 'Priorité', filtres.prio, [['', 'Toutes'], ['A', 'A'], ['B', 'B'], ['C', 'C'], ['HC', 'Hors cible']]) +
      selectHTML('f-canal', 'Canal', filtres.canal, [['', 'Tous']].concat(CANAUX.map(function (c) { return [c.id, c.nom]; }))) +
      selectHTML('f-who', 'Associé', filtres.who, [['', 'Tous'], ['u1', 'Camille Exemple'], ['u2', 'Alex Modèle']]) +
      '<label class="case"><input type="checkbox" id="f-retard"' + (filtres.retard ? ' checked' : '') + '> En retard seulement</label></div>';
  }
  function th(cle, lib, num) {
    var actif = filtres.tri === cle;
    return '<th scope="col"' + (num ? ' class="num"' : '') + (actif ? ' aria-sort="' + (filtres.sens > 0 ? 'descending' : 'ascending') + '"' : '') + '><button class="tri" type="button" data-tri="' + cle + '">' + esc(lib) + (actif ? (filtres.sens > 0 ? ' ↓' : ' ↑') : '') + '</button></th>';
  }
  function resultatsListe() {
    var l = filtrer();
    var tab = '<div class="defile tableau-liste"><table class="tableau compact"><caption class="sr">Demandes filtrées</caption><thead><tr>' +
      '<th scope="col">Réf.</th>' + th('recu', 'Reçue') + '<th scope="col" style="min-width:132px">Nom</th><th scope="col" style="min-width:132px">Projet</th>' + th('score', 'Priorité') +
      '<th scope="col">Canal</th><th scope="col">Statut</th>' + th('echeance', 'Prochaine action') + th('montant', 'Montant', true) + '</tr></thead><tbody>' +
      l.map(function (r) {
        return '<tr' + (enRetard(r) ? ' class="retard"' : '') + '><td class="ref"><a href="#/demandes/' + r.ref + '">' + r.ref + '</a></td><td>' + esc(dateC(r.recu)) + '</td><td>' + esc(r.nom) + '<span class="org">' + esc(r.org ? r.org : L.type[r.type]) + '</span></td>' +
          '<td>' + esc(travaux(r)) + '<span class="org">' + esc(r.commune + ', zone ' + r.zone) + '</span></td><td>' + prioScore(r) + '</td>' +
          '<td>' + esc(r.canalM.court) + (r.canalDeclare ? '<span class="org">déclaré</span>' : '') + '</td><td>' + statut(r) + '<span class="org">' + esc(USERS[r.who].nom) + '</span></td><td>' + (r.statut === 'nouvelle' ? echeanceHTML(r) : esc(prochaineAction(r))) + '</td>' +
          '<td class="num">' + esc(montant(r)) + '</td></tr>';
      }).join('') + '</tbody></table></div>';
    var cartes = '<ul class="cartes-liste">' + l.map(function (r) {
      return '<li' + (enRetard(r) ? ' class="retard"' : '') + '><div style="display:flex;gap:8px;align-items:center">' + prio(r) + '<a href="#/demandes/' + r.ref + '">' + esc(r.nom) + '</a><span class="discret petit" style="margin-left:auto">' + r.ref + '</span></div>' +
        '<span class="petit">' + esc(travaux(r) + ', ' + r.commune) + '</span><div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">' + statut(r) + '<span class="petit discret">' + esc(r.statut === 'nouvelle' ? 'Rappeler avant ' + dateH(prochaineEch(r)) : prochaineAction(r)) + '</span></div></li>';
    }).join('') + '</ul>';
    return '<p class="petit discret" aria-live="polite">' + l.length + ' demande' + (l.length > 1 ? 's' : '') + '</p>' + (l.length ? tab + cartes : '<p class="vide">Aucune demande pour ces filtres. <button class="btn btn-petit btn-discret" type="button" id="f-effacer">Effacer les filtres</button></p>');
  }
  ECRANS.demandes = function () {
    return '<div class="entete-page"><div><h1 tabindex="-1">Demandes</h1><p class="sous-titre">Toutes les demandes, tous canaux. Les filtres sont gardés dans l’adresse de la page dans l’admin réel.</p></div>' +
      '<div class="actions"><nav class="bascule" aria-label="Affichage"><a href="#/demandes" aria-current="page">Liste</a><a href="#/demandes/colonnes">Colonnes</a></nav><button class="btn btn-discret" type="button" data-maquette="Export CSV des demandes filtrées (associés seulement, journalisé).">Exporter</button></div></div>' +
      filtresHTML() + '<div id="resultats-liste">' + resultatsListe() + '</div>';
  };

  /* ---------- Demandes : colonnes ---------- */
  var etatColonnes = { active: 0 };
  var TRANSITIONS = {
    nouvelle: [['contact_etabli', 'Contact établi'], ['hors_cible', 'Hors cible'], ['perdue', 'Perdue (motif)']],
    contact_etabli: [['visite_planifiee', 'Visite planifiée'], ['offre_envoyee', 'Offre envoyée (montant)'], ['perdue', 'Perdue (motif)']],
    visite_planifiee: [['offre_envoyee', 'Offre envoyée (montant)'], ['contact_etabli', 'Visite annulée'], ['perdue', 'Perdue (motif)']],
    offre_envoyee: [['signee', 'Signée (montant)'], ['perdue', 'Perdue (motif)']],
    signee: [], perdue: [['nouvelle', 'Rouvrir']]
  };
  ECRANS.colonnes = function () {
    var cols = [
      ['nouvelle', 'Nouvelle', D.filter(function (r) { return r.statut === 'nouvelle'; })],
      ['contact_etabli', 'Contact établi', D.filter(function (r) { return r.statut === 'contact_etabli'; })],
      ['visite_planifiee', 'Visite planifiée', D.filter(function (r) { return r.statut === 'visite_planifiee'; })],
      ['offre_envoyee', 'Offre envoyée', D.filter(function (r) { return r.statut === 'offre_envoyee'; })],
      ['signee', 'Signée (30 jours)', D.filter(function (r) { return r.statut === 'signee' && r.signee.t >= AUJ - 30 * 1440; })],
      ['perdue', 'Perdue (30 jours)', D.filter(function (r) { return r.statut === 'perdue' && r.perdue.t >= AUJ - 30 * 1440; })]
    ];
    function jours(r) {
      var depuis = r.statut === 'offre_envoyee' ? r.offre.t : r.statut === 'visite_planifiee' ? (r.premier || r.recu) : r.statut === 'signee' ? r.signee.t : r.statut === 'perdue' ? r.perdue.t : r.statut === 'contact_etabli' ? r.premier : r.recu;
      return Math.max(0, Math.floor((NOW - depuis) / 1440));
    }
    var onglets = '<div class="onglets-colonnes" role="tablist" aria-label="Étapes">' + cols.map(function (c, i) { return '<button type="button" role="tab" aria-selected="' + (i === etatColonnes.active) + '" data-col="' + i + '">' + esc(c[1]) + ' (' + c[2].length + ')</button>'; }).join('') + '</div>';
    return '<div class="entete-page"><div><h1 tabindex="-1">Demandes par étape</h1><p class="sous-titre">Seules les transitions autorisées sont proposées (plan §4.5). Le menu « Déplacer vers » remplace le glisser-déposer au clavier.</p></div>' +
      '<div class="actions"><nav class="bascule" aria-label="Affichage"><a href="#/demandes">Liste</a><a href="#/demandes/colonnes" aria-current="page">Colonnes</a></nav></div></div>' + onglets +
      '<div class="colonnes">' + cols.map(function (c, i) {
        var total = somme(c[2].map(function (r) { return r.signee ? r.signee.m : r.offre ? r.offre.m : 0; }));
        return '<section class="colonne' + (i === etatColonnes.active ? ' active' : '') + '" aria-labelledby="col-' + i + '"><div class="colonne-tete"><h2 id="col-' + i + '">' + esc(c[1]) + ' <span class="discret">' + c[2].length + '</span></h2><span class="discret">' + (total ? chf(total) : '&nbsp;') + '</span></div>' +
          (c[2].length ? '' : '<p class="petit discret" style="padding:10px 12px;margin:0">Aucune demande à cette étape.</p>') + '<ul class="cartes">' + c[2].map(function (r) {
            var tr = TRANSITIONS[r.statut] || [];
            return '<li class="carte"><div class="haut-carte">' + prio(r) + '<div>' + nomLien(r) + '</div></div><span class="meta">' + esc(travaux(r) + ', ' + r.commune) + '</span>' +
              '<span class="meta">' + esc(jours(r) + ' j dans l’étape') + (r.offre ? ', ' + esc(chf(r.signee ? r.signee.m : r.offre.m)) : '') + (enRetard(r) ? ', <span class="alerte-texte">en retard</span>' : '') + '</span>' +
              (tr.length ? '<details><summary>Déplacer vers…</summary><ul>' + tr.map(function (x) { return '<li><button class="btn btn-petit btn-discret" type="button" data-action="' + x[0] + '" data-ref="' + r.ref + '">' + esc(x[1]) + '</button></li>'; }).join('') + '</ul></details>' : '') + '</li>';
          }).join('') + '</ul></section>';
      }).join('') + '</div>';
  };

  /* ---------- Fiche demande ---------- */
  function historique(r) {
    var ev = [], assoc = USERS[r.who].nom;
    function e(min, txt, qui) { if (min <= NOW) ev.push([min, txt, qui]); }
    e(r.recu, r.canal === 'telephone' ? 'Appel reçu, demande saisie (saisie express)' : 'Demande reçue par le formulaire de devis', r.canal === 'telephone' ? assoc : 'Site');
    if (r.mail && r.canal === 'site') e(r.recu + 1, 'Accusé de réception envoyé par e-mail (« ' + (r.prio === 'hors-cible' ? 'nous l’examinons' : 'rappel ' + dateH(r.ech)) + ' »)', 'Site');
    if (!r.mail && r.tel && r.canal === 'site') e(r.recu + 1, 'Accusé de réception envoyé par SMS', 'n8n');
    if ((r.prio === 'A' || r.prio === 'B') && r.canal === 'site') e(r.recu + 2, 'SMS « Demande ' + r.prio + ' » envoyé à ' + assoc, 'n8n');
    if (r.statut === 'nouvelle' && NOW > r.ech && !r.tents.length) { e(r.ech, 'Échéance dépassée : SMS de rappel à ' + assoc, 'n8n'); e(r.ech + 60, 'Escalade : SMS et e-mail à l’autre associé', 'n8n'); }
    r.tents.forEach(function (x, i) { e(x, 'Appel sans réponse (tentative ' + (i + 1) + ')', r.canal === 'site' && i === 0 ? assoc + ' (lien en un clic)' : assoc); if (i === 0) e(x + 2, 'SMS et e-mail « Nous avons essayé de vous joindre » envoyés', 'n8n'); });
    if (r.premier && r.canal !== 'telephone') e(r.premier, 'Contact établi (« J’ai eu la personne »)', assoc + ' (lien en un clic)');
    if (r.visite) { e((r.premier || r.recu) + 5, 'Visite planifiée le ' + dateH(r.visite.t), assoc); if (r.visite.faite) e(r.visite.t + 60, 'Visite faite', assoc); }
    if (r.offre) {
      e(r.offre.t + 17 * 60, 'Offre envoyée : ' + chf(r.offre.m) + ' HT', assoc);
      var fin = r.signee ? r.signee.t : r.perdue ? r.perdue.t : NOW;
      [[3, 'Relance J+3 envoyée (e-mail « bien reçue ? »)'], [10, (r.prio === 'A' || r.b2b) ? 'Tâche J+10 : appeler le client' : 'Relance J+10 envoyée (e-mail)'], [21, 'Relance J+21 envoyée (e-mail avec 3 réponses en un clic)']].forEach(function (x) {
        var d = ouvrableApres(r.offre.le, x[0]); if (d <= fin) e(d, x[1], 'n8n');
      });
    }
    if (r.signee) { e(r.signee.t + 16 * 60, 'Offre signée : ' + chf(r.signee.m) + ' HT', assoc); e(r.signee.t + 16 * 60 + 1, 'Chantier créé (à planifier)', 'Admin'); }
    if (r.perdue) e(r.perdue.t + 16 * 60, 'Marquée perdue : ' + M.MOTIFS[r.perdue.motif].toLowerCase() + (r.perdue.recontact ? ', recontact autorisé à 6 mois' : '') + (r.perdue.auto ? ' (clôture automatique)' : r.perdue.lien ? ' (réponse du client par le lien J+21)' : ''), r.perdue.auto || r.perdue.lien ? 'n8n' : assoc);
    if (r.chantier) {
      var c = r.chantier;
      if (c.debut) e(t(c.debut) + 7 * 60, 'Chantier ' + (c.statut === 'planifie' ? 'planifié du ' + dateC(t(c.debut)) + ' au ' + dateC(t(c.fin)) : 'commencé'), assoc);
      if (c.reception) e(t(c.reception) + 16 * 60, 'Réception faite', assoc);
      if (c.reserves) e(t(c.reserves) + 16 * 60, 'Réserves levées', assoc);
      if (c.avisDemande) e(t(c.avisDemande) + 10 * 60, 'Demande d’avis envoyée (e-mail et SMS)', 'n8n');
      if (c.avisRelance) e(t(c.avisRelance) + 10 * 60, 'Relance unique de la demande d’avis', 'n8n');
      if (c.avisRecu) e(t(c.avisRecu) + 9 * 60, 'Avis Google reçu et rapproché', 'Camille Exemple');
    }
    ev.sort(function (a, b) { return b[0] - a[0]; });
    return '<ol class="historique">' + ev.map(function (x) { return '<li><time>' + esc(dateC(x[0]) + ', ' + heure(x[0])) + '</time><div>' + esc(x[1]) + '<div class="auteur">' + esc(x[2]) + '</div></div></li>'; }).join('') + '</ol>';
  }
  function actionsFiche(r) {
    var b = [];
    function bt(cl, act, lib) { b.push('<button class="btn ' + cl + '" type="button" data-action="' + act + '" data-ref="' + r.ref + '">' + esc(lib) + '</button>'); }
    if (r.statut === 'nouvelle' && r.prio === 'hors-cible') { bt('btn-principal', 'reorientation', 'Voir et envoyer la réponse de réorientation'); bt('btn-discret', 'pas-hors-cible', 'Ce n’est pas hors cible'); }
    else if (r.statut === 'nouvelle') { b.push(r.tel ? '<button class="btn btn-principal" type="button" data-appeler="' + r.ref + '">Appeler ' + esc(r.telAff) + '</button>' : ''); bt('btn-discret', 'contact_etabli', 'J’ai eu la personne'); bt('btn-discret', 'pas-de-reponse', 'Pas de réponse (tentative ' + (r.tents.length + 1) + ')'); bt('btn-discret', 'hors_cible', 'Hors cible'); }
    else if (r.statut === 'contact_etabli') { bt('btn-principal', 'visite_planifiee', 'Planifier la visite'); bt('btn-discret', 'offre_envoyee', 'Envoyer l’offre'); bt('btn-discret', 'perdue', 'Marquer perdue'); }
    else if (r.statut === 'visite_planifiee') { bt('btn-principal', 'offre_envoyee', 'Envoyer l’offre'); if (!r.visite.faite) bt('btn-discret', 'visite-faite', 'Visite faite'); bt('btn-discret', 'perdue', 'Marquer perdue'); }
    else if (r.statut === 'offre_envoyee') { bt('btn-principal', 'signee', 'Marquer signée'); bt('btn-discret', 'relancer', 'Relancer maintenant'); bt('btn-discret', 'ne-plus-relancer', 'Ne plus relancer'); bt('btn-discret', 'nouvelle-version', 'Nouvelle version de l’offre'); bt('btn-discret', 'perdue', 'Marquer perdue'); }
    else if (r.statut === 'signee') { bt('btn-principal', 'planifier-chantier', 'Planifier le chantier'); bt('btn-discret', 'reception', 'Réception faite'); bt('btn-discret', 'demander-avis', 'Demander un avis'); }
    else if (r.statut === 'perdue') { bt('btn-discret', 'nouvelle', 'Rouvrir'); }
    bt('btn-discret', 'reattribuer', 'Réattribuer');
    return b.join('');
  }
  ECRANS.fiche = function (q, ref) {
    var r = PAR_REF[ref];
    if (!r) return '<h1 tabindex="-1">Demande introuvable</h1><p>Aucune demande ne porte la référence « ' + esc(ref) + ' ». <a href="#/demandes">Retour aux demandes</a></p>';
    var sc = r.sc, x = relance(r);
    var entete = '<div class="fiche-entete"><div><p class="petit discret" style="margin:0"><a href="#/demandes">Demandes</a> / ' + r.ref + '</p><h1 tabindex="-1">' + esc(r.nom) + (r.org ? ', <span style="font-weight:600">' + esc(r.org) + '</span>' : '') + '</h1>' +
      '<div class="ligne-meta">' + prioScore(r) + statut(r) + (r.statut === 'nouvelle' ? echeanceHTML(r) : '<span>' + esc(prochaineAction(r)) + '</span>') + '<span>Associé : ' + esc(USERS[r.who].nom) + '</span></div></div>' +
      '<div class="groupe-btn boutons-entete">' + (r.tel ? '<button class="btn ' + (r.statut === 'nouvelle' ? 'btn-principal' : '') + '" type="button" data-appeler="' + r.ref + '">Appeler</button>' : '') + (r.email ? '<button class="btn btn-discret" type="button" data-maquette="Ouvre un e-mail à ' + esc(r.email) + ' depuis la boîte de l’associé.">E-mail</button>' : '') + '<button class="btn btn-discret" type="button" data-resultat="' + r.ref + '">Résultat de l’appel</button></div></div>';
    var projet = '<details class="bloc" open><summary>Projet <span class="discret">' + esc(L.type[r.type]) + '</span></summary><div class="bloc-corps"><dl class="dl">' +
      '<dt>Travaux</dt><dd>' + esc(travaux(r)) + '</dd><dt>Type de client</dt><dd>' + esc(L.type[r.type]) + (r.org ? ' (' + esc(r.org) + ')' : '') + '</dd><dt>Surface</dt><dd>' + esc(L.surface[r.surf]) + '</dd><dt>Délai</dt><dd>' + esc(L.delai[r.delai]) + '</dd>' +
      '<dt>Commune</dt><dd>' + esc(r.npa + ' ' + r.commune + ' (' + r.canton + '), zone ' + r.zone) + '</dd>' + (r.recommandePar ? '<dt>Recommandé par</dt><dd>' + esc(r.recommandePar) + '</dd>' : '') + '</dl>' +
      '<div class="message">' + (r.msg ? esc(r.msg) : '<span class="discret">Message vide.</span>') + '</div>' +
      (r.fic ? '<div class="fichiers">' + Array.apply(null, { length: r.fic }).map(function (_, i) { return '<button class="fichier" type="button" data-maquette="Téléchargement authentifié, jamais par une adresse publique."><i aria-hidden="true"></i>' + (i === 0 && r.fic > 1 ? 'plan-' + (i + 1) + '.pdf, 1,2 Mo' : 'photo-' + (i + 1) + '.heic, 2,8 Mo') + '</button>'; }).join('') + '</div>' : '') + '</div></details>';
    var score = '<details class="bloc" open><summary>Score détaillé <span class="discret">' + sc.score + ' points, priorité ' + (r.prio === 'hors-cible' ? 'hors cible' : r.prio) + ', grille ' + M.GRILLE.version + '</span></summary><div class="bloc-corps"><table class="tableau"><caption class="sr">Détail du score</caption><thead><tr><th scope="col">Critère</th><th scope="col">Valeur</th><th scope="col" class="num">Points</th></tr></thead><tbody>' +
      sc.detail.map(function (d) { return '<tr><th scope="row">' + esc(L.critere[d.critere]) + '</th><td>' + esc(d.valeur) + '</td><td class="num">' + (d.points > 0 ? '+' : '') + d.points + '</td></tr>'; }).join('') +
      '</tbody><tfoot><tr><th scope="row" colspan="2">Total</th><td class="num">' + sc.score + '</td></tr></tfoot></table>' +
      (sc.regles.length || sc.hors_cible.length ? '<p class="petit mt">Règles appliquées : ' + esc(sc.regles.concat(sc.hors_cible).join(' ; ')) + '.</p>' : '') +
      '<p class="petit discret">Seuils : A dès ' + M.GRILLE.seuils.A + ', B dès ' + M.GRILLE.seuils.B + '. Un associé peut corriger la priorité (motif obligatoire, journalisé). <button class="btn btn-petit btn-discret" type="button" data-maquette="Correction de la priorité : choix A, B, C ou hors cible, motif obligatoire.">Corriger la priorité</button></p></div></details>';
    var attrib = '<details class="bloc"><summary>Source et attribution <span class="discret">' + esc(r.canalM.nom) + '</span></summary><div class="bloc-corps"><dl class="dl">' +
      '<dt>Canal</dt><dd>' + esc(r.canalM.nom) + (r.canalDeclare ? ' (déclaré au téléphone ou dans le formulaire)' : '') + '</dd><dt>Catégorie</dt><dd><code>' + esc(r.src) + '</code></dd><dt>Détail</dt><dd>' + esc(r.utm || '—') + '</dd>' +
      '<dt>Arrivée</dt><dd>' + esc(r.canal === 'telephone' ? 'appel téléphonique' : '/' + (r.service === 'plusieurs' || r.service === 'autre' ? '' : r.service + '.html') + ' puis /contact.html') + '</dd>' +
      '<dt>« Connu par »</dt><dd>' + esc(L.connu[r.connu || ''] || r.connu) + '</dd>' +
      '<dt>gclid</dt><dd>' + (r.src !== 'google-ads' ? '—' : r.gclid ? 'présent (mesure publicitaire acceptée) : importable dans Google Ads (V3)' : 'absent : la personne a refusé la mesure publicitaire') + '</dd></dl>' +
      '<p class="mt"><button class="btn btn-petit btn-discret" type="button" data-maquette="Correction du canal : journalisée, le canal corrigé fait foi dans Acquisition.">Corriger le canal</button></p></div></details>';
    var hist = '<details class="bloc" open><summary>Historique</summary><div class="bloc-corps">' + historique(r) + '</div></details>';
    var notes = '<details class="bloc"><summary>Notes <span class="discret">invisibles pour l’agence</span></summary><div class="bloc-corps"><label class="champ"><span class="sr">Ajouter une note</span><textarea placeholder="Ajouter une note"></textarea></label><p class="mt"><button class="btn btn-petit" type="button" data-maquette="Note ajoutée à l’historique.">Ajouter la note</button></p></div></details>';
    var coord = '<section class="panneau panneau-coord"><h2>Coordonnées</h2><dl class="dl">' +
      '<dt>Téléphone</dt><dd>' + (r.tel ? esc(r.telAff) + ' <span class="etiquette">fictif</span>' : '<span class="discret">non donné</span>') + '</dd>' +
      '<dt>E-mail</dt><dd>' + (r.email ? esc(r.email) : '<span class="discret">non donné</span>') + '</dd><dt>Préférence</dt><dd>' + (r.tel ? 'Par téléphone, le matin' : 'Par e-mail') + '</dd>' +
      '<dt>Reçue</dt><dd>' + esc(dateH(r.recu)) + '</dd>' + (r.premier ? '<dt>1er contact</dt><dd>' + esc(dateH(r.premier)) + (r.canal !== 'telephone' ? ' (' + duree(minutesOuvrables(r.recu, r.premier)) + ' ouvrables)' : ' (appel entrant)') + '</dd>' : '') + '</dl></section>';
    var offre = r.offre ? '<section class="panneau"><h2>Offre</h2><dl class="dl"><dt>N°</dt><dd>O-' + r.ref.slice(3) + '-1</dd><dt>Montant</dt><dd>' + chf(r.offre.m) + ' HT</dd><dt>Envoyée</dt><dd>' + esc(dateC(r.offre.t)) + (x ? ', J+' + x.jours : '') + '</dd>' +
      (x ? '<dt>Relances</dt><dd>' + x.etape + ' sur 3</dd><dt>Ensuite</dt><dd>' + esc(x.texte) + '</dd>' : '') +
      (r.signee ? '<dt>Signée</dt><dd>' + esc(dateC(r.signee.t)) + ', ' + chf(r.signee.m) + '</dd>' : '') + (r.perdue ? '<dt>Perdue</dt><dd>' + esc(dateC(r.perdue.t) + ', ' + M.MOTIFS[r.perdue.motif].toLowerCase()) + '</dd>' : '') + '</dl></section>' : '';
    var chant = r.chantier ? '<section class="panneau"><h2>Chantier</h2><dl class="dl"><dt>Statut</dt><dd>' + esc(L.chantier[r.chantier.statut]) + '</dd>' + (r.chantier.debut ? '<dt>Dates</dt><dd>' + esc(dateC(t(r.chantier.debut)) + ' au ' + dateC(t(r.chantier.fin))) + '</dd>' : '') + '<dt>Jours-équipe</dt><dd>' + r.chantier.jours + '</dd>' +
      (r.chantier.avisDemande ? '<dt>Avis</dt><dd>' + esc(r.chantier.avisRecu ? 'reçu le ' + dateC(t(r.chantier.avisRecu)) : 'demandé le ' + dateC(t(r.chantier.avisDemande)) + (r.chantier.avisRelance ? ', relancé le ' + dateC(t(r.chantier.avisRelance)) : '')) + '</dd>' : '') + '</dl></section>' : '';
    var actions = '<section class="panneau panneau-actions"><h2>Actions</h2><div class="actions-fiche">' + actionsFiche(r) + '</div></section>';
    var barre = '<div class="barre-action-mobile">' + (r.tel ? '<button class="btn btn-principal" type="button" data-appeler="' + r.ref + '">Appeler</button>' : '<button class="btn btn-principal" type="button" data-maquette="Répondre par e-mail.">E-mail</button>') + '<button class="btn" type="button" data-resultat="' + r.ref + '">Résultat</button><button class="btn btn-icone" type="button" data-plus-actions="' + r.ref + '" aria-label="Autres actions">⋯</button></div>';
    return entete + '<div class="fiche-corps"><div class="pile">' + projet + score + attrib + hist + notes + '</div><div class="pile colonne-actions">' + actions + coord + offre + chant + '</div></div>' + barre;
  };

  /* ---------- Saisie d'un appel ---------- */
  ECRANS.saisie = function () {
    function radios(nom, opts, def) { return '<div class="choix">' + opts.map(function (o) { return '<label><input type="radio" name="' + nom + '" value="' + o[0] + '"' + (o[0] === def ? ' checked' : '') + '><span>' + esc(o[1]) + '</span></label>'; }).join('') + '</div>'; }
    function cases(nom, opts) { return '<div class="choix">' + opts.map(function (o) { return '<label><input type="checkbox" name="' + nom + '" value="' + o[0] + '"><span>' + esc(o[1]) + '</span></label>'; }).join('') + '</div>'; }
    return '<div class="entete-page"><div><h1 tabindex="-1">Saisir un appel</h1><p class="sous-titre">30 secondes. Le score, la priorité et l’échéance sont calculés comme pour le site.</p></div></div>' +
      '<form class="grille-2" id="form-saisie" novalidate style="align-items:start"><div class="panneau formulaire">' +
      '<label class="champ"><span>Téléphone</span><input id="s-tel" name="telephone" type="tel" inputmode="tel" autocomplete="off" placeholder="079 000 00 00"><span class="aide-champ" id="s-doublon" aria-live="polite">En premier : on retrouve un contact existant.</span></label>' +
      '<label class="champ"><span>Nom et prénom</span><input name="nom" autocomplete="off"></label>' +
      '<label class="champ"><span>Commune ou NPA</span><input id="s-commune" name="commune" autocomplete="off" placeholder="1227 Carouge"></label>' +
      '<fieldset class="champ"><legend>Travaux</legend>' + cases('travaux', [['placo', 'Placo'], ['peinture', 'Peinture'], ['isolation-acoustique', 'Isolation acoustique'], ['cloisons-isothermes', 'Cloisons isolantes'], ['autre', 'Autre']]) + '</fieldset>' +
      '<fieldset class="champ"><legend>Type de client</legend>' + radios('type', [['proprietaire', 'Propriétaire'], ['locataire', 'Locataire'], ['regie', 'Régie'], ['architecte', 'Architecte'], ['commune', 'Commune'], ['entreprise', 'Entreprise']]) + '</fieldset>' +
      '<fieldset class="champ"><legend>Surface</legend>' + radios('surf', [['moins-15', '< 15 m²'], ['15-50', '15-50 m²'], ['50-200', '50-200 m²'], ['plus-200', '> 200 m²'], ['ne-sait-pas', 'Ne sait pas']]) + '</fieldset>' +
      '<fieldset class="champ"><legend>Délai</legend>' + radios('delai', [['moins-1-mois', '< 1 mois'], ['1-3-mois', '1-3 mois'], ['3-6-mois', '3-6 mois'], ['non-defini', 'Pas défini']]) + '</fieldset>' +
      '<label class="champ"><span>Comment nous avez-vous connus ? <span class="aide-champ">obligatoire : c’est l’attribution des appels</span></span><select name="connu" required><option value="">Choisir</option><option value="recherche-google">Recherche Google</option><option value="carte-google">Carte Google</option><option value="recommandation">Recommandation d’un proche</option><option value="regie-architecte">Une régie ou un architecte</option><option value="panneau-vehicule">Panneau de chantier ou véhicule</option><option value="facebook">Facebook</option><option value="linkedin">LinkedIn</option><option value="autre">Autre</option></select></label>' +
      '<label class="champ"><span>Note</span><textarea name="note" placeholder="Ce que la personne a dit"></textarea></label>' +
      '<label class="champ"><span>E-mail <span class="aide-champ">facultatif</span></span><input name="email" type="email" autocomplete="off"></label>' +
      '<label class="case" style="display:flex;gap:8px;align-items:center"><input type="checkbox" name="confirmation"> Envoyer une confirmation écrite au client</label>' +
      '<div class="groupe-btn"><button class="btn btn-principal" type="submit">Enregistrer, contact établi</button><button class="btn btn-discret" type="button" data-maquette="Demande enregistrée sans contact établi : elle apparaît dans À rappeler.">Enregistrer seulement</button></div>' +
      '<p class="petit discret" id="s-erreurs" aria-live="assertive"></p></div>' +
      '<aside class="panneau score-direct" aria-live="polite" aria-labelledby="t-score"><h2 id="t-score">Priorité calculée</h2><div id="s-score"></div></aside></form>';
  };
  function zoneDeNpa(npa) { var n = +npa; if (!n) return null; if ((n >= 1200 && n <= 1299) || (n >= 1180 && n <= 1199 && n !== 1187 && n !== 1188 && n !== 1189)) return 1; if ((n >= 1000 && n <= 1037) || (n >= 1066 && n <= 1179) || (n >= 1800 && n <= 1843) || (n >= 1300 && n <= 1318) || (n >= 1600 && n <= 1613)) return 2; if (n >= 1000 && n <= 2999) return 3; return 'hors'; }
  function majScoreSaisie() {
    var f = document.getElementById('form-saisie'); if (!f) return;
    var fd = new FormData(f), trav = fd.getAll('travaux');
    var npa = ((fd.get('commune') || '').match(/\b[1-9]\d{3}\b/) || [])[0] || '';
    var r = { type: fd.get('type') || '', trav: trav, surf: fd.get('surf') || '', delai: fd.get('delai') || '', zone: npa ? zoneDeNpa(npa) : 'inconnue', src: 'appel-direct', connu: fd.get('connu') || '', canal: 'telephone', tel: true, msg: fd.get('note') || '', fic: 0 };
    r.service = serviceDe(trav);
    var sc = calculer(r), ech = echeance(sc.priorite, NOW);
    var bad = sc.priorite === 'hors-cible' ? '<span class="prio prio-HC">Hors cible</span>' : '<span class="prio prio-' + sc.priorite + '" style="width:40px;height:40px;font-size:20px">' + sc.priorite + '</span>';
    document.getElementById('s-score').innerHTML = '<div style="display:flex;gap:14px;align-items:center">' + bad + '<span class="gros">' + sc.score + '</span><span class="discret">points</span></div>' +
      '<p class="mt petit">Échéance si le contact n’est pas établi maintenant : <b>' + esc(dateH(ech)) + '</b>.' + (npa ? ' Zone ' + r.zone + ' (NPA ' + npa + ').' : ' Indiquez le NPA pour la zone.') + '</p>' +
      '<table class="tableau mt"><caption class="sr">Détail</caption><tbody>' + sc.detail.map(function (d) { return '<tr><th scope="row">' + esc(L.critere[d.critere]) + '</th><td>' + esc(d.valeur) + '</td><td class="num">' + d.points + '</td></tr>'; }).join('') + '</tbody></table>' +
      (sc.regles.length || sc.hors_cible.length ? '<p class="petit">' + esc(sc.regles.concat(sc.hors_cible).join(' ; ')) + '</p>' : '') +
      '<p class="petit discret">Pas de bonus « téléphone » pour une saisie : le numéro est toujours connu (comme Scoring.php).</p>';
  }

  /* ---------- Offres et chantiers ---------- */
  ECRANS.offres = function () {
    var ouvertes = D.filter(function (r) { return r.statut === 'offre_envoyee'; }).sort(function (a, b) { return a.offre.t - b.offre.t; });
    var attente = somme(ouvertes.map(function (r) { return r.offre.m; })), co = cohorte(NOW);
    var delais = D.filter(function (r) { return r.signee; }).map(function (r) { return (r.signee.t - r.offre.t) / 1440; });
    var cn = carnet();
    var tabOffres = '<div class="defile"><table class="tableau"><caption class="sr">Offres ouvertes</caption><thead><tr><th scope="col">Réf.</th><th scope="col">Client</th><th scope="col" class="num">Montant</th><th scope="col">Envoyée</th><th scope="col" class="num">Jours</th><th scope="col" class="num">Relances</th><th scope="col">Prochaine étape</th><th scope="col">Associé</th></tr></thead><tbody>' +
      ouvertes.map(function (r) { var x = relance(r); return '<tr' + (x.decision ? ' class="retard"' : '') + '><td class="ref"><a href="#/demandes/' + r.ref + '">' + r.ref + '</a></td><td>' + esc(r.nom) + (r.org ? '<span class="org">' + esc(r.org) + '</span>' : '') + '</td><td class="num">' + chf(r.offre.m) + '</td><td>' + esc(dateC(r.offre.t)) + '</td><td class="num">' + x.jours + '</td><td class="num">' + x.etape + '/3</td><td>' + (x.decision ? '<span class="alerte-texte">' + esc(x.texte) + '</span>' : esc(x.texte)) + '</td><td>' + esc(USERS[r.who].nom.split(' ')[0]) + '</td></tr>'; }).join('') +
      '</tbody><tfoot><tr><th scope="row" colspan="2">' + ouvertes.length + ' offres ouvertes</th><td class="num">' + chf(attente) + '</td><td colspan="5"></td></tr></tfoot></table></div>';
    var ch = chantiers().sort(function (a, b) { return (a.chantier.debut || '9') < (b.chantier.debut || '9') ? -1 : 1; });
    var tabCh = '<div class="defile"><table class="tableau"><caption class="sr">Chantiers</caption><thead><tr><th scope="col">Réf.</th><th scope="col">Client</th><th scope="col" class="num">Montant signé</th><th scope="col">Statut</th><th scope="col">Dates</th><th scope="col" class="num">Jours-équipe</th><th scope="col">Avis</th></tr></thead><tbody>' +
      ch.map(function (r) { var c = r.chantier; return '<tr><td class="ref"><a href="#/demandes/' + r.ref + '">' + r.ref + '</a></td><td>' + esc(r.nom) + (r.org ? '<span class="org">' + esc(r.org) + '</span>' : '') + '</td><td class="num">' + chf(r.signee.m) + '</td><td>' + esc(L.chantier[c.statut]) + '</td><td>' + (c.debut ? esc(dateC(t(c.debut)) + ' au ' + dateC(t(c.fin))) : '<span class="discret">à fixer</span>') + '</td><td class="num">' + (c.restant != null ? c.restant + ' sur ' + c.jours : c.jours) + '</td><td>' + esc(c.avisRecu ? 'reçu ' + dateC(t(c.avisRecu)) : c.avisDemande ? 'demandé ' + dateC(t(c.avisDemande)) + (c.avisRelance ? ', relancé' : '') : '—') + '</td></tr>'; }).join('') + '</tbody></table></div>';
    return '<div class="entete-page"><div><h1 tabindex="-1">Offres et chantiers</h1><p class="sous-titre">Où en sont les offres envoyées, et combien de travail est déjà signé.</p></div></div>' +
      '<div class="bande"><div><span class="libelle">Montant en attente</span><div class="valeur">' + chf(attente) + '</div><span class="petit discret">' + ouvertes.length + ' offres ouvertes</span></div>' +
      '<div><span class="libelle">Taux offre→signée</span><div class="valeur">' + pct(co.taux) + '</div><span class="petit discret">' + co.signees + ' sur ' + co.offres + ', offres envoyées entre J−180 et J−60, objectif 28 %</span></div>' +
      '<div><span class="libelle">Délai médian offre→signature</span><div class="valeur">' + nb(mediane(delais)) + ' jours</div><span class="petit discret">sur ' + delais.length + ' signatures</span></div>' +
      '<div><span class="libelle">Carnet</span><div class="valeur">' + nb(cn.semaines, 1) + ' semaines</div>' + metre(cn.semaines, 12, M.PARAMETRES.seuilCarnetSemaines, 'Carnet ' + nb(cn.semaines, 1) + ' semaines, seuil 8') + '<span class="petit discret">' + cn.total + ' jours-équipe / ' + M.PARAMETRES.equipes + ' équipes ; seuil 8 semaines (fictif)</span></div></div>' +
      '<section class="panneau mt" aria-labelledby="t-oo"><div class="panneau-entete"><h2 id="t-oo">Offres ouvertes</h2><span class="discret">relances J+3, J+10, J+21 automatiques ; décision à J+35 ; clôture à J+45</span></div>' + tabOffres + '</section>' +
      '<section class="panneau mt" aria-labelledby="t-ch"><div class="panneau-entete"><h2 id="t-ch">Chantiers signés</h2><span class="discret">dont ' + cn.joursAcquisition + ' jours-équipe issus de l’acquisition ; ' + M.PARAMETRES.horsAcquisitionJours + ' jours hors acquisition (clients existants)</span></div>' + tabCh + '</section>';
  };

  /* ---------- Acquisition ---------- */
  var etatAcq = { periode: '3m' };
  function moisPeriode(p) { return p === '3m' ? ['2027-02', '2027-03', '2027-04'] : [p]; }
  ECRANS.acquisition = function () {
    var mois = moisPeriode(etatAcq.periode);
    var Dp = D.filter(function (r) { return mois.indexOf(r.mois) >= 0; });
    var sigP = D.filter(function (r) { return r.signee && mois.indexOf(r.signee.le.slice(0, 7)) >= 0; });
    var marge = M.PARAMETRES.margeBrute;
    var lignes = CANAUX.map(function (c) {
      var dm = Dp.filter(function (r) { return r.canalM.id === c.id; });
      var q = dm.filter(function (r) { return r.prio !== 'hors-cible'; }), ab = q.filter(function (r) { return r.prio === 'A' || r.prio === 'B'; });
      var s = sigP.filter(function (r) { return r.canalM.id === c.id; }), ca = somme(s.map(function (r) { return r.signee.m; }));
      var dep = somme(mois.map(function (m) { return depense(m, c.id); }));
      var tend = (M.HISTORIQUE_CANAUX[c.id] || [0, 0, 0]).concat(['2027-02', '2027-03', '2027-04'].map(function (m) { return D.filter(function (r) { return r.mois === m && r.canalM.id === c.id; }).length; }));
      return { c: c, dem: dm.length, q: q.length, ab: ab.length, sig: s.length, ca: ca, dep: dep, cpl: dep && dm.length ? dep / dm.length : null, cac: dep && s.length ? dep / s.length : null, roas: dep ? ca / dep : null, roi: dep ? (ca * marge - dep) / dep : null, tend: tend };
    });
    var total = Dp.length;
    function totalDe(l) { var o = { dem: 0, q: 0, ab: 0, sig: 0, ca: 0, dep: 0 }; l.forEach(function (x) { o.dem += x.dem; o.q += x.q; o.ab += x.ab; o.sig += x.sig; o.ca += x.ca; o.dep += x.dep; }); o.cpl = o.dep && o.dem ? o.dep / o.dem : null; o.cac = o.dep && o.sig ? o.dep / o.sig : null; o.roas = o.dep ? o.ca / o.dep : null; o.roi = o.dep ? (o.ca * marge - o.dep) / o.dep : null; return o; }
    var payants = lignes.filter(function (l) { return l.c.payant; }), tp = totalDe(payants), tt = totalDe(lignes);
    function indicatif(l) { return l.dep && l.sig < 3 ? '<sup title="Moins de 3 chantiers signés : indicatif">*</sup>' : ''; }
    function cell(v, f) { return v == null ? '<span class="discret" title="' + 'aucune dépense ou aucun chantier signé' + '">—</span>' : esc(f(v)); }
    function ligneHTML(l, tete) {
      return '<tr><th scope="row">' + esc(tete || l.c.nom) + '</th><td class="num">' + (l.dep ? chf(l.dep) : '<span class="discret">—</span>') + '</td><td class="num">' + l.dem + ' <span class="discret">(' + pct(total ? l.dem / total : null) + ')</span></td><td class="num">' + l.q + ' <span class="discret">(' + pct(l.q ? l.ab / l.q : null) + ')</span></td><td class="num">' + l.sig + '</td><td class="num">' + chf(l.ca) + '</td>' +
        '<td class="num">' + cell(l.cpl, chf) + '</td><td class="num">' + cell(l.cac, chf) + indicatif(l) + '</td><td class="num">' + cell(l.roas, function (v) { return nb(v, 1); }) + '</td><td class="num">' + cell(l.roi, function (v) { return pct(v); }) + '</td>' +
        '<td>' + (l.tend ? sparkline(l.tend) : '') + '</td></tr>';
    }
    var tab = '<div class="defile"><table class="tableau compact"><caption class="sr">Indicateurs par canal</caption><thead><tr><th scope="col">Canal</th><th scope="col" class="num">Dépense</th><th scope="col" class="num">Demandes (part)</th><th scope="col" class="num">Qualifiées (A+B)</th><th scope="col" class="num">Signées</th><th scope="col" class="num">CA signé</th><th scope="col" class="num">CPL</th><th scope="col" class="num">CAC</th><th scope="col" class="num">ROAS</th><th scope="col" class="num">ROI</th><th scope="col">Tendance, 6 mois</th></tr></thead><tbody>' +
      payants.map(function (l) { return ligneHTML(l); }).join('') + '<tr><th scope="row" class="discret" colspan="11" style="font-weight:600;padding-top:14px">Canaux sans dépense directe</th></tr>' + lignes.filter(function (l) { return !l.c.payant; }).map(function (l) { return ligneHTML(l); }).join('') +
      '</tbody><tfoot>' + ligneHTML(Object.assign({ tend: null }, tp), 'Total des canaux payants') + ligneHTML(Object.assign({ tend: null }, tt), 'Total, tous canaux') + '</tfoot></table></div>';
    var cm = cplMax(NOW), cible = cm.max / 3;
    var bDem = barresClassees('Demandes par canal', lignes.map(function (l) { return { lib: l.c.court, v: l.dem }; }), function (v) { return nb(v); });
    var bCa = barresClassees('CA signé par canal', lignes.map(function (l) { return { lib: l.c.court, v: l.ca, vide: 'CHF 0' }; }), function (v) { return chf(v); });
    var bCpl = barresClassees('CPL des canaux payants face à la cible', payants.filter(function (l) { return l.cpl; }).map(function (l) { return { lib: l.c.court, v: l.cpl }; }), function (v) { return chf(v); }, { v: cible, lib: 'cible ' + chf(cible) });
    var ga = M.GOOGLE_ADS['2027-04'], gaM = M.GOOGLE_ADS['2027-03'];
    var gaDem = D.filter(function (r) { return r.src === 'google-ads' && mois.indexOf(r.mois) >= 0; }), avecG = gaDem.filter(function (r) { return r.gclid; });
    var sigGA = D.filter(function (r) { return r.signee && r.src === 'google-ads'; });
    var periodes = [['3m', 'Février à avril (3 mois)'], ['2027-04', 'Avril 2027 (au 22)'], ['2027-03', 'Mars 2027'], ['2027-02', 'Février 2027']];
    return '<div class="entete-page"><div><h1 tabindex="-1">Acquisition</h1><p class="sous-titre">Quel canal amène des chantiers signés, et à quel coût. Trois mois par défaut : les petits nombres d’un seul mois trompent.</p></div>' +
      '<div class="actions filtres" style="margin-bottom:0">' + selectHTML('acq-periode', 'Période', etatAcq.periode, periodes) + '<a class="btn btn-discret" href="#/parametres/depenses">Saisir les dépenses</a></div></div>' +
      '<section class="panneau" aria-labelledby="t-can"><div class="panneau-entete"><h2 id="t-can">Par canal</h2><span class="discret">CPL = dépense / demandes ; CAC = dépense / chantiers signés ; ROAS = CA signé / dépense ; ROI = (marge brute − dépense) / dépense, marge 30 % (fictive)</span></div>' + tab +
      '<p class="petit discret mt">* Moins de 3 chantiers signés : CAC, ROAS et ROI indicatifs. Dépense : médias et courrier, hors honoraires d’agence (décision G5). CA et signatures rattachés au canal d’origine de la demande, à la date de signature : une demande de janvier signée en février compte en février. Les appels saisis prennent le canal déclaré.</p></section>' +
      '<div class="grille-3 mt"><section class="panneau" aria-labelledby="t-b1"><h2 id="t-b1">Demandes par canal</h2>' + bDem + '</section><section class="panneau" aria-labelledby="t-b2"><h2 id="t-b2">CA signé par canal</h2>' + bCa + '</section><section class="panneau" aria-labelledby="t-b3"><h2 id="t-b3">CPL, canaux payants</h2>' + bCpl +
      '<p class="petit discret">Cible = 1/3 du CPL max (' + chf(cm.max) + ' = panier ' + chf(cm.panier) + ' × marge 30 % × demande→offre ' + pct(cm.tdo) + ' × offre→signée ' + pct(cm.taux) + ').</p></section></div>' +
      '<section class="panneau mt" aria-labelledby="t-ga"><div class="panneau-entete"><h2 id="t-ga">Google Ads</h2><span class="discret">coûts importés chaque jour (rapport programmé) ; conversions hors ligne en V3</span></div><div class="grille-2"><div><table class="tableau"><caption class="sr">Google Ads par mois</caption><thead><tr><th scope="col">Mois</th><th scope="col" class="num">Dépense</th><th scope="col" class="num">Clics</th><th scope="col" class="num">CPC</th><th scope="col" class="num">Part d’impressions</th></tr></thead><tbody>' +
      '<tr><th scope="row">Mars</th><td class="num">' + chf(depense('2027-03', 'google-ads')) + '</td><td class="num">' + gaM.clics + '</td><td class="num">CHF ' + nb(gaM.cpc, 2) + '</td><td class="num">' + gaM.partImpr + ' %</td></tr>' +
      '<tr><th scope="row">Avril (au 21)</th><td class="num">' + chf(depense('2027-04', 'google-ads')) + '</td><td class="num">' + ga.clics + '</td><td class="num">CHF ' + nb(ga.cpc, 2) + '</td><td class="num">' + ga.partImpr + ' %</td></tr></tbody></table>' +
      '<p class="petit mt">Demandes Google Ads sur la période : <b>' + gaDem.length + '</b>, dont <b>' + avecG.length + '</b> avec un gclid (mesure publicitaire acceptée). Les autres restent comptées par UTM.</p></div>' +
      '<div><h3>Chantiers signés à importer (aperçu V3)</h3><table class="tableau"><caption class="sr">Conversions hors ligne</caption><thead><tr><th scope="col">Réf.</th><th scope="col" class="num">Valeur</th><th scope="col">Clic</th><th scope="col">État</th></tr></thead><tbody>' +
      sigGA.map(function (r) { var age = Math.floor((r.signee.t - r.recu) / 1440); return '<tr><td class="ref"><a href="#/demandes/' + r.ref + '">' + r.ref + '</a></td><td class="num">' + chf(r.signee.m) + '</td><td>' + esc(dateC(r.recu) + ' (' + age + ' j avant la signature)') + '</td><td>' + (r.gclid ? (age <= 90 ? 'À envoyer, prochain envoi le 23.04 à 6 h' : 'Clic de plus de 90 jours : refusé') : 'Sans gclid : rien n’est envoyé') + '</td></tr>'; }).join('') +
      '</tbody></table><p class="petit discret">Envoyé : gclid, date, montant. Aucun nom, e-mail ni téléphone. Actions créées en secondaires (volume trop faible pour l’enchère).</p></div></div></section>';
  };

  /* ---------- SEO et visibilité ---------- */
  ECRANS.visibilite = function () {
    var g = M.SITE.gsc28, f = M.SITE.fiche;
    var c = courbe('courbe-gsc', M.SITE.gscClicsSemaine, { titre: 'Clics Search Console par semaine, 12 semaines', unite: 'clics', pasEtiquette: 2 });
    var req = '<div class="defile"><table class="tableau"><caption class="sr">Requêtes cibles</caption><thead><tr><th scope="col">Requête (fictive)</th><th scope="col" class="num">Clics</th><th scope="col" class="num">Impressions</th><th scope="col" class="num">CTR</th><th scope="col" class="num">Position</th><th scope="col" class="num">28 j avant</th></tr></thead><tbody>' +
      M.SITE.requetes.map(function (q) { return '<tr><th scope="row" style="font-weight:400">' + esc(q[0]) + '</th><td class="num">' + q[1] + '</td><td class="num">' + nb(q[2]) + '</td><td class="num">' + pct(q[1] / q[2], 1) + '</td><td class="num">' + nb(q[3], 1) + '</td><td class="num">' + nb(q[4], 1) + (q[3] < q[4] ? ' <span class="discret">(mieux)</span>' : '') + '</td></tr>'; }).join('') + '</tbody></table></div>';
    var fiche = '<table class="tableau"><caption class="sr">Fiche Google par mois</caption><thead><tr><th scope="col">Mois</th><th scope="col" class="num">Appels</th><th scope="col" class="num">Itinéraires</th><th scope="col" class="num">Clics vers le site</th></tr></thead><tbody>' +
      M.MOIS.map(function (mk) { return '<tr><th scope="row">' + moisL(mk) + (mk === '2027-04' ? ' (au 22)' : '') + '</th><td class="num">' + f.appels[mk] + '</td><td class="num">' + f.itineraires[mk] + '</td><td class="num">' + f.clicsSite[mk] + '</td></tr>'; }).join('') + '</tbody></table>';
    var ia = '<div class="defile"><table class="tableau"><caption class="sr">Citations dans les IA, test d’avril</caption><thead><tr><th scope="col">Question (test mensuel)</th>' + M.IA.assistants.map(function (a) { return '<th scope="col">' + esc(a) + '</th>'; }).join('') + '</tr></thead><tbody>' +
      M.IA.questions.map(function (q) { return '<tr><th scope="row" style="font-weight:400">' + esc(q[0]) + '</th>' + q[1].map(function (v) { return '<td>' + (v ? '<b>Cité</b>' : '<span class="discret">—</span>') + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table></div>';
    var cites = M.IA.questions.filter(function (q) { return q[1].some(Boolean); }).length;
    return '<div class="entete-page"><div><h1 tabindex="-1">SEO et visibilité</h1><p class="sous-titre">Ce qui fait venir sans payer : la recherche Google, la fiche Google et les assistants IA. Agrégats seulement, aucune donnée personnelle.</p></div></div>' +
      '<div class="bande"><div><span class="libelle">Clics, 28 jours</span><div class="valeur">' + g.clics + '</div><span class="petit discret">' + g.clicsAvant + ' les 28 jours précédents (+' + pct((g.clics - g.clicsAvant) / g.clicsAvant) + ')</span></div>' +
      '<div><span class="libelle">Impressions, 28 jours</span><div class="valeur">' + nb(g.impressions) + '</div><span class="petit discret">CTR ' + pct(g.clics / g.impressions, 1) + '</span></div>' +
      '<div><span class="libelle">Position moyenne</span><div class="valeur">' + nb(g.position, 1) + '</div><span class="petit discret">' + nb(g.positionAvant, 1) + ' avant (plus bas = mieux)</span></div>' +
      '<div><span class="libelle">Citations IA</span><div class="valeur">' + cites + '/10</div><span class="petit discret">test du 1er avril, objectif M6 : 3/10</span></div></div>' +
      '<div class="grille-2 mt"><section class="panneau" aria-labelledby="t-gsc"><div class="panneau-entete"><h2 id="t-gsc">Clics par semaine</h2><span class="discret">Search Console, données à J−3 ; date du lundi de chaque semaine</span></div>' + c +
      tableDonnees('Clics par semaine', ['Semaine du', 'Clics'], M.SITE.gscClicsSemaine.map(function (p) { return [p[0], p[1]]; })) + '</section>' +
      '<section class="panneau" aria-labelledby="t-fiche"><div class="panneau-entete"><h2 id="t-fiche">Fiche Google</h2><span class="discret">saisie mensuelle en attendant l’accès à l’API (V3)</span></div>' + fiche + '</section></div>' +
      '<section class="panneau mt" aria-labelledby="t-req"><div class="panneau-entete"><h2 id="t-req">Requêtes cibles</h2><span class="discret">8 des 30 requêtes suivies, 28 derniers jours</span></div>' + req + '</section>' +
      '<section class="panneau mt" aria-labelledby="t-ia"><div class="panneau-entete"><h2 id="t-ia">Citations IA</h2><span class="discret">10 questions fixes, posées le 1er du mois ; saisie par l’agence</span><span class="droite"><button class="btn btn-petit btn-discret" type="button" data-maquette="Formulaire de saisie du test de mai : 10 questions × 3 assistants.">Saisir le test de mai</button></span></div>' + ia + '</section>';
  };

  /* ---------- Avis ---------- */
  ECRANS.avis = function () {
    var cum = M.MOIS.map(function (mk) { return [moisCourt(mk), M.AVIS.cumul[mk]]; });
    var c = courbe('courbe-avis', cum, { titre: 'Avis Google cumulés par mois, avec les objectifs M3 et M6', unite: 'avis', n: 6, cibles: [{ i: 2, v: 15, lib: 'objectif M3 : 15' }, { i: 5, v: 30, lib: 'objectif M6 : 30' }] });
    var ch = chantiers().filter(function (r) { return r.chantier.avisDemande; });
    var liste = '<ul class="liste-travail">' + M.AVIS.liste.map(function (a) {
      var etatRep = a.reponse === 'publiee' ? 'Réponse publiée' : a.reponse === 'brouillon' ? 'Brouillon de l’agence prêt' : 'Sans réponse';
      return '<li class="ligne-travail' + (a.reponse == null && (AUJ - t(a.le)) / 1440 >= 2 ? ' retard' : '') + '"><div class="qui"><span class="prio prio-HC">' + a.note + '/5</span><div><b>' + esc(a.auteur) + '</b><span class="org">' + esc(dateA(t(a.le))) + '</span></div></div><div class="quoi">' + esc(a.texte) + '</div>' +
        '<div class="echeance-cel petit">' + esc(etatRep) + '<span class="org">' + (a.rapproche ? 'Chantier ' + esc(a.rapproche) : a.suggestion ? 'Chantier probable : ' + esc(a.suggestion) : 'Non rapproché') + '</span></div>' +
        '<div class="boutons">' + (a.reponse === 'brouillon' ? '<button class="btn btn-petit" type="button" data-maquette="Brouillon validé, copié pour publication sur la fiche Google.">Valider la réponse</button>' : a.reponse == null ? '<button class="btn btn-petit" type="button" data-maquette="Éditeur de réponse avec le modèle v2 §5.7 (d).">Rédiger</button>' : '') +
        (!a.rapproche && a.suggestion ? '<button class="btn btn-petit btn-discret" type="button" data-maquette="Avis rapproché de ' + esc(a.suggestion) + ' : « avis reçu » coché, plus de relance.">Rapprocher</button>' : '') + '</div></li>';
    }).join('') + '</ul>';
    return '<div class="entete-page"><div><h1 tabindex="-1">Avis</h1><p class="sous-titre">Une demande à chaque client, sans tri ; une réponse à chaque avis. Textes et auteurs fictifs.</p></div></div>' +
      '<div class="bande"><div><span class="libelle">Avis Google</span><div class="valeur">' + M.AVIS.cumul['2027-04'] + '</div><span class="petit discret">Objectif M6 : 30, M12 : 50</span></div>' +
      '<div><span class="libelle">Note moyenne</span><div class="valeur">' + nb(M.AVIS.note, 1) + '</div><span class="petit discret">Suivie, jamais pilotée</span></div>' +
      '<div><span class="libelle">Avis ce mois</span><div class="valeur">+' + (M.AVIS.cumul['2027-04'] - M.AVIS.cumul['2027-03']) + '</div><span class="petit discret">mars : +' + (M.AVIS.cumul['2027-03'] - M.AVIS.cumul['2027-02']) + '</span></div>' +
      '<div><span class="libelle">Demandes d’avis en cours</span><div class="valeur">' + ch.filter(function (r) { return !r.chantier.avisRecu; }).length + '</div><span class="petit discret">' + ch.length + ' chantiers terminés depuis mars</span></div></div>' +
      '<div class="grille-2 mt"><section class="panneau" aria-labelledby="t-cum"><div class="panneau-entete"><h2 id="t-cum">Avis cumulés</h2><span class="discret">fiche Google, fin de mois (avril : au 22)</span></div>' + c + tableDonnees('Avis cumulés', ['Mois', 'Avis'], M.MOIS.map(function (mk) { return [moisL(mk), M.AVIS.cumul[mk]]; })) + '</section>' +
      '<section class="panneau" aria-labelledby="t-dem"><div class="panneau-entete"><h2 id="t-dem">Demandes d’avis</h2><span class="discret">J+2 après les réserves levées, relance unique à J+9</span></div><table class="tableau"><caption class="sr">Demandes d’avis</caption><thead><tr><th scope="col">Chantier</th><th scope="col">Demandé</th><th scope="col">Relance</th><th scope="col">Avis</th></tr></thead><tbody>' +
      ch.map(function (r) { var k = r.chantier; return '<tr><td class="ref"><a href="#/demandes/' + r.ref + '">' + r.ref + '</a><span class="org">' + esc(r.nom) + '</span></td><td>' + esc(dateC(t(k.avisDemande))) + '</td><td>' + (k.avisRelance ? esc(dateC(t(k.avisRelance))) : '—') + '</td><td>' + (k.avisRecu ? 'Reçu ' + esc(dateC(t(k.avisRecu))) : 'Pas encore') + '</td></tr>'; }).join('') + '</tbody></table></section></div>' +
      '<section class="mt" aria-labelledby="t-liste"><h2 id="t-liste" style="margin-bottom:8px">Derniers avis</h2>' + liste + '</section>';
  };

  /* ---------- Rapport mensuel ---------- */
  ECRANS.rapport = function () {
    var mk = '2027-03', fin = finMois(mk), c = comptes(mk), del = delaiPremierContact(mk, 'A'), dd = rappeleesDansDelai(mk, 'A', fin);
    var tdo = tauxDemandeOffre(mk), sig = signees(mk), ca = somme(sig.map(function (o) { return o.m; })), co = cohorte(fin);
    var dep = depensePayante(mk), dp = demandesPayantes(mk);
    var dm = demandesMois(mk);
    var parCanal = CANAUX.map(function (cn) { var l = dm.filter(function (r) { return r.canalM.id === cn.id; }); var s = D.filter(function (r) { return r.signee && r.signee.le.slice(0, 7) === mk && r.canalM.id === cn.id; }); var d = depense(mk, cn.id); return [cn.nom, l.length, s.length, chf(somme(s.map(function (r) { return r.signee.m; }))), d ? chf(d) : '—', d && l.length ? chf(d / l.length) : '—']; });
    function tab(titre, entetes, lignes) { return '<table class="tableau"><caption class="sr">' + esc(titre) + '</caption><thead><tr>' + entetes.map(function (h, i) { return '<th scope="col"' + (i ? ' class="num"' : '') + '>' + esc(h) + '</th>'; }).join('') + '</tr></thead><tbody>' + lignes.map(function (l) { return '<tr>' + l.map(function (v, i) { return i ? '<td class="num">' + esc(v) + '</td>' : '<th scope="row">' + esc(v) + '</th>'; }).join('') + '</tr>'; }).join('') + '</tbody></table>'; }
    return '<div class="entete-page"><div><h1 tabindex="-1">Rapport mensuel</h1><p class="sous-titre">Produit le 1er jour ouvrable à 7 h et figé. Sans donnée personnelle : partageable avec l’agence.</p></div>' +
      '<div class="actions filtres" style="margin-bottom:0"><label>Mois<select disabled><option>Mars 2027</option></select></label><button class="btn btn-sombre" type="button" id="bouton-pdf">Exporter en PDF</button></div></div>' +
      '<article class="rapport" aria-labelledby="t-rap"><h2 id="t-rap" style="font-size:24px">Andy Construct, mars 2027 (M5)</h2><p class="discret">Produit le jeudi 1er avril 2027 à 7 h. Validé par Camille Exemple le 06.04.2027. Données fictives.</p>' +
      '<div class="chiffres-tete"><div><b>' + c.demandes + '</b>demandes (A ' + c.A + ', B ' + c.B + ', C ' + c.C + ')</div><div><b>' + duree(del.mediane) + '</b>délai médian, A</div><div><b>' + pct(tdo.taux) + '</b>demande→offre</div><div><b>' + chf(ca) + '</b>' + sig.length + ' chantiers signés</div><div><b>' + chf(dep / dp) + '</b>CPL, canaux payants</div></div>' +
      '<h2>Résultats</h2>' + tab('Résultats', ['Indicateur', 'Mars', 'Objectif M5'], [['Demandes/mois', c.demandes, nb(objectif('demandes', mk))], ['Part A+B', pct(partAB(c)), '≥ ' + pct(objectif('partAB', mk) / 100)], ['Offres envoyées', offresEnvoyees(mk), '—'], ['Taux demande→offre', pct(tdo.taux), pct(objectif('demandeOffre', mk) / 100)], ['Taux offre→signée (cohorte au 31.03)', pct(co.taux) + ' (' + co.signees + '/' + co.offres + ')', pct(objectif('offreSignee', mk) / 100)], ['CA signé', chf(ca), chf(objectif('chantiers', mk) * M.PARAMETRES.panierReference) + ' (indicatif)']]) +
      '<h2>Réactivité</h2>' + tab('Réactivité', ['Indicateur', 'Mars', 'Objectif M5'], [['Délai de premier contact, médiane A', duree(del.mediane), 'moins de ' + duree(objectif('delaiA', mk) * 60)], ['Demandes A rappelées dans le délai', dd.ok + ' sur ' + dd.total, '—'], ['Délai, toutes priorités', duree(delaiPremierContact(mk).mediane), '—']]) +
      '<h2>Sources</h2>' + tab('Sources', ['Canal', 'Demandes', 'Signées', 'CA signé', 'Dépense', 'CPL'], parCanal) +
      '<h2>Site</h2>' + tab('Site', ['Indicateur', 'Mars', 'Objectif M5'], [['Visites', nb(M.SITE.visites[mk]), nb(objectif('visites', mk))], ['Contacts web', M.SITE.contactsWeb[mk], nb(objectif('contactsWeb', mk))], ['Taux visite→contact', pct(M.SITE.contactsWeb[mk] / M.SITE.visites[mk], 1), pct(objectif('tauxVisiteContact', mk) / 100, 1)]]) +
      '<p class="petit discret">Pages d’entrée : ' + M.SITE.pagesEntree.map(function (p) { return p[0] + ' (' + p[1] + ')'; }).join(', ') + '.</p>' +
      '<h2>Google Ads</h2>' + tab('Google Ads', ['Indicateur', 'Mars'], [['Dépense', chf(depense(mk, 'google-ads'))], ['Clics', M.GOOGLE_ADS[mk].clics], ['CPC', 'CHF ' + nb(M.GOOGLE_ADS[mk].cpc, 2)], ['Part d’impressions', M.GOOGLE_ADS[mk].partImpr + ' %'], ['Demandes', dm.filter(function (r) { return r.canalM.id === 'google-ads'; }).length]]) +
      '<h2>Réputation</h2>' + tab('Réputation', ['Indicateur', 'Mars', 'Objectif M5'], [['Avis Google (cumul)', M.AVIS.cumul[mk], nb(objectif('avis', mk))], ['Note moyenne', nb(M.AVIS.note, 1), 'suivie'], ['Citations IA', M.IA.historique[mk] + '/10', nb(objectif('citationsIA', mk)) + '/10']]) +
      '<h2>B2B et appels d’offres</h2>' + tab('B2B', ['Indicateur', 'Cumul à fin mars', 'Objectif M6'], [['Comptes B2B contactés', 55, 90], ['Appels d’offres étudiés / déposés', '12 / 2', '18 / 4']]) +
      '<h2>Automatisation</h2>' + tab('Automatisation', ['Indicateur', 'Mars'], [['SMS envoyés aux associés', 31], ['Erreurs de workflow', 0], ['Désinscriptions', 0], ['File d’attente du site', 'vide']]) +
      '<h2>Trois actions pour avril (commentaire de l’agence, fictif)</h2><ol><li>Google Ads : couper les termes « réparation fissure » (2 demandes trop petites en mars).</li><li>Rappeler les demandes A arrivées après 15 h 30 avant 9 h le lendemain : 1 retard en mars.</li><li>Fiche Google : publier 2 réalisations avec photos (les appels montent depuis février).</li></ol>' +
      '</article>';
  };

  /* ---------- Paramètres ---------- */
  var ONGLETS_PARAM = [['utilisateurs', 'Utilisateurs et rôles'], ['objectifs', 'Objectifs'], ['depenses', 'Dépenses'], ['economie', 'Économie'], ['motifs', 'Motifs de perte'], ['zones', 'Zones'], ['scoring', 'Scoring'], ['integrations', 'Intégrations']];
  ECRANS.parametres = function (q, onglet) {
    onglet = onglet || 'utilisateurs';
    var corps = '';
    if (onglet === 'utilisateurs') {
      corps = '<table class="tableau"><caption class="sr">Utilisateurs</caption><thead><tr><th scope="col">Nom</th><th scope="col">Rôle</th><th scope="col">Rôle métier</th><th scope="col">Double authentification</th><th scope="col">Dernière connexion</th><th scope="col"><span class="sr">Actions</span></th></tr></thead><tbody>' +
        M.UTILISATEURS.map(function (u) { return '<tr><th scope="row">' + esc(u.nom) + '</th><td>' + esc(u.role) + '</td><td>' + esc(u.metier || '—') + '</td><td>' + esc(u.deuxFa) + '</td><td>' + esc(dateH(t(u.derniere))) + '</td><td><button class="btn btn-petit btn-discret" type="button" data-maquette="Modifier, désactiver ou réinitialiser la double authentification.">Modifier</button></td></tr>'; }).join('') +
        '</tbody></table><p class="petit discret mt">Les rôles « Agence » ne voient aucune donnée personnelle de prospect. Droits détaillés : plan §6.5.</p><p class="mt"><button class="btn btn-principal" type="button" data-maquette="Invitation par e-mail ; la double authentification est demandée à la première connexion.">Ajouter un utilisateur</button></p>';
    } else if (onglet === 'objectifs') {
      var ind = [['demandes', 'Demandes/mois', ''], ['partAB', 'Part A+B', ' %'], ['delaiA', 'Délai de premier contact A (h ouvrables, maximum)', ' h'], ['demandeOffre', 'Taux demande→offre', ' %'], ['offreSignee', 'Taux offre→signée', ' %'], ['visites', 'Visites', ''], ['tauxVisiteContact', 'Taux visite→contact', ' %'], ['avis', 'Avis Google (cumul)', ''], ['citationsIA', 'Citations IA (sur 10)', '']];
      corps = '<p class="petit discret">Jalons de la stratégie v2 §1.1, scénario M. Entre deux jalons : interpolation linéaire (décision G6), modifiable mois par mois.</p><div class="defile"><table class="tableau"><caption class="sr">Objectifs</caption><thead><tr><th scope="col">Indicateur</th><th scope="col" class="num">M3 (janv.)</th><th scope="col" class="num">M4</th><th scope="col" class="num">M5</th><th scope="col" class="num">M6 (avr.)</th><th scope="col" class="num">M12 (oct.)</th></tr></thead><tbody>' +
        ind.map(function (i) { var o = M.OBJECTIFS[i[0]]; return '<tr><th scope="row">' + esc(i[1]) + '</th><td class="num">' + nb(o.M3, o.M3 % 1 ? 1 : 0) + i[2] + '</td><td class="num">' + nb(objectif(i[0], '2027-02'), 1) + '</td><td class="num">' + nb(objectif(i[0], '2027-03'), 1) + '</td><td class="num">' + nb(o.M6, o.M6 % 1 ? 1 : 0) + i[2] + '</td><td class="num">' + nb(o.M12, o.M12 % 1 ? 1 : 0) + i[2] + '</td></tr>'; }).join('') + '</tbody></table></div>' +
        '<p class="mt"><label class="filtres" style="display:inline-grid">Scénario <select><option>M « Croissance »</option><option>S « Fondations »</option><option>L « Accélération romande »</option></select></label></p>';
    } else if (onglet === 'depenses') {
      var canauxDep = [['google-ads', 'Google Ads (importé)'], ['meta', 'Meta Ads'], ['b2b', 'Courrier B2B']];
      corps = '<p class="petit discret">Montants HT par mois. Google Ads est importé chaque jour (verrouillé). Meta et le courrier sont saisis par l’agence ou un associé.</p><div class="defile"><table class="tableau"><caption class="sr">Dépenses par mois</caption><thead><tr><th scope="col">Canal</th>' + M.MOIS.map(function (mk) { return '<th scope="col" class="num">' + esc(moisCourt(mk)) + '</th>'; }).join('') + '</tr></thead><tbody>' +
        canauxDep.map(function (c) { return '<tr><th scope="row">' + esc(c[1]) + '</th>' + M.MOIS.map(function (mk) { var v = depense(mk, c[0]); return '<td class="num">' + (c[0] === 'google-ads' ? nb(v) : '<label class="sr" for="dep-' + c[0] + mk + '">' + esc(c[1] + ', ' + moisL(mk)) + '</label><input id="dep-' + c[0] + mk + '" style="width:72px;text-align:right;height:30px;border:1px solid var(--bord-fort);border-radius:2px;background:var(--panneau)" value="' + v + '" inputmode="decimal">') + '</td>'; }).join('') + '</tr>'; }).join('') +
        '</tbody></table></div><p class="mt"><button class="btn btn-principal" type="button" data-maquette="Dépenses enregistrées ; CPL, CAC, ROAS et ROI recalculés (journalisé).">Enregistrer</button></p>';
    } else if (onglet === 'economie') {
      var cm = cplMax(NOW);
      corps = '<div class="grille-2"><div class="formulaire panneau"><label class="champ"><span>Taux de marge brute de référence <span class="aide-champ">décision G4 ; valeur fictive</span></span><input value="30 %"></label><label class="champ"><span>Panier de référence (objectif de CA)</span><input value="CHF 10\'000"></label><label class="champ"><span>Honoraires d’agence dans la dépense</span><select><option>Non (médias, courrier, impression)</option><option>Oui (coût complet)</option></select></label><label class="champ"><span>Équipes</span><input value="2" inputmode="numeric"></label><label class="champ"><span>Seuil d’alerte du carnet</span><input value="8 semaines"></label><button class="btn btn-principal" type="button" data-maquette="Paramètres enregistrés.">Enregistrer</button></div>' +
        '<div class="panneau"><h2>Ce que ces paramètres donnent aujourd’hui</h2><dl class="dl mt"><dt>Panier moyen, 6 mois</dt><dd>' + chf(cm.panier) + '</dd><dt>Taux demande→offre</dt><dd>' + pct(cm.tdo) + ' (objectif M6)</dd><dt>Taux offre→signée</dt><dd>' + pct(cm.taux) + ' (cohorte)</dd><dt>CPL max</dt><dd>' + chf(cm.max) + '</dd><dt>Cible de CPL</dt><dd>' + chf(cm.max / 3) + '</dd><dt>ROAS d’équilibre</dt><dd>' + nb(1 / M.PARAMETRES.margeBrute, 1) + '</dd></dl><p class="petit discret mt">CPL max = panier moyen × marge brute × taux demande→offre × taux offre→signée (plan d’acquisition v4 §2.5).</p></div></div>';
    } else if (onglet === 'motifs') {
      var cpt = {}; D.forEach(function (r) { if (r.perdue) cpt[r.perdue.motif] = (cpt[r.perdue.motif] || 0) + 1; });
      corps = '<table class="tableau"><caption class="sr">Motifs de perte</caption><thead><tr><th scope="col">Motif</th><th scope="col">Relance à 6 mois</th><th scope="col" class="num">Utilisé (3 mois)</th></tr></thead><tbody>' +
        Object.keys(M.MOTIFS).map(function (k) { return '<tr><th scope="row">' + esc(M.MOTIFS[k]) + '</th><td>' + (['prix', 'delai', 'reporte'].indexOf(k) >= 0 ? 'Autorisée si la personne l’a acceptée' : 'Jamais') + '</td><td class="num">' + (cpt[k] || 0) + '</td></tr>'; }).join('') + '</tbody></table>';
    } else if (onglet === 'zones') {
      corps = '<p class="petit discret">Table NPA → zone de <code>site/api/data/zones.json</code>. Une correction crée une nouvelle version datée.</p><table class="tableau"><caption class="sr">Zones</caption><thead><tr><th scope="col">Zone</th><th scope="col">Territoire</th><th scope="col" class="num">Points</th></tr></thead><tbody>' +
        '<tr><th scope="row">1</th><td>Canton de Genève, district de Nyon</td><td class="num">15</td></tr><tr><th scope="row">2</th><td>Districts de Morges, Lausanne, Ouest lausannois, Lavaux-Oron, Riviera-Pays-d’Enhaut</td><td class="num">10</td></tr><tr><th scope="row">3</th><td>Reste de la Suisse romande</td><td class="num">5</td></tr><tr><th scope="row">Hors</th><td>Hors Suisse romande (hors cible, validé par un associé)</td><td class="num">—</td></tr></tbody></table>' +
        '<div class="filtres mt"><label>Tester un NPA<input type="search" id="test-npa" inputmode="numeric" placeholder="1800"></label><p id="test-npa-res" class="petit" aria-live="polite" style="margin:0 0 8px"></p></div>';
    } else if (onglet === 'scoring') {
      var g = M.GRILLE;
      function bloc(titre, obj, lib) { return '<tr><th scope="rowgroup" colspan="2" style="padding-top:14px">' + esc(titre) + '</th></tr>' + Object.keys(obj).filter(function (k) { return k !== ''; }).map(function (k) { return '<tr><td>' + esc((lib && lib[k]) || k) + '</td><td class="num">' + (obj[k] === null ? 'hors cible' : obj[k]) + '</td></tr>'; }).join(''); }
      corps = '<p class="petit discret">Grille ' + esc(g.version) + ' (<code>scoring.json</code>). Seuils : A dès ' + g.seuils.A + ', B dès ' + g.seuils.B + '. Modification par un associé seulement ; recalibrage trimestriel (v2 §2.7). Dans cette maquette, ' + D.filter(function (r) { return r.prio === 'A'; }).length + ' demandes sur ' + D.length + ' sont classées A : à surveiller (plan §7.3).</p>' +
        '<div class="grille-2"><table class="tableau"><caption class="sr">Grille, partie 1</caption><tbody>' + bloc('Type de client', g.type_client, L.type) + bloc('Travaux', g.service, L.trav) + bloc('Surface', g.surface, L.surface) + '</tbody></table>' +
        '<table class="tableau"><caption class="sr">Grille, partie 2</caption><tbody>' + bloc('Zone', g.zone) + bloc('Délai', g.delai, L.delai) + bloc('Source', g.source, L.cat) + '</tbody></table></div>';
    } else if (onglet === 'integrations') {
      var ints = [['Site (formulaires)', 'Temps réel', 'Dernière demande : 22.04, 8 h 12', 'OK'], ['n8n (API interne)', 'Toutes les 15 min', 'Dernier appel : 22.04, 9 h 30', 'OK'], ['Umami', 'Quotidienne, 6 h', 'Données au 21.04', 'OK'], ['Search Console', 'Quotidienne, 6 h', 'Données au 19.04 (délai normal)', 'OK'], ['Google Places (note, avis)', 'Quotidienne, 6 h', '22.04, 6 h 02', 'OK'], ['Google Ads (coûts)', 'Quotidienne, rapport programmé', 'Rapport du 22.04, 6 h', 'OK'], ['Business Profile (appels, itinéraires)', 'Mensuelle', 'Accès à l’API demandé ; saisie manuelle', 'Saisie'], ['Sauvegarde chiffrée vers le VPS', 'Quotidienne, 2 h', '22.04, 2 h 04 ; restauration testée le 01.04', 'OK']];
      corps = '<table class="tableau"><caption class="sr">Intégrations</caption><thead><tr><th scope="col">Source</th><th scope="col">Fréquence</th><th scope="col">Dernière lecture</th><th scope="col">État</th></tr></thead><tbody>' + ints.map(function (i) { return '<tr><th scope="row">' + esc(i[0]) + '</th><td>' + esc(i[1]) + '</td><td>' + esc(i[2]) + '</td><td>' + (i[3] === 'OK' ? '<span class="icone-ok" aria-hidden="true">✓</span> OK' : esc(i[3])) + '</td></tr>'; }).join('') + '</tbody></table><p class="petit discret mt">Aucune clé n’est affichée : elles restent sur le serveur et dans n8n.</p>';
    }
    return '<div class="entete-page"><div><h1 tabindex="-1">Paramètres</h1><p class="sous-titre">Réservés aux associés, sauf la saisie des dépenses (agence). Chaque modification est journalisée.</p></div></div>' +
      '<div class="onglets" role="tablist" aria-label="Paramètres">' + ONGLETS_PARAM.map(function (o) { return '<a role="tab" href="#/parametres/' + o[0] + '" aria-selected="' + (o[0] === onglet) + '" style="text-decoration:none;padding:10px 14px;font-weight:600;border-bottom:2px solid ' + (o[0] === onglet ? 'var(--rouge)' : 'transparent') + ';margin-bottom:-1px;color:' + (o[0] === onglet ? 'var(--texte)' : 'var(--texte-2)') + '">' + esc(o[1]) + '</a>'; }).join('') + '</div>' +
      '<section class="panneau" role="tabpanel" aria-label="' + esc(ONGLETS_PARAM.filter(function (o) { return o[0] === onglet; })[0][1]) + '">' + corps + '</section>';
  };

  /* ---------- Journal et données personnelles ---------- */
  ECRANS.donnees = function () {
    var perdues = D.filter(function (r) { return r.perdue; }).sort(function (a, b) { return a.perdue.t - b.perdue.t; }).slice(0, 3);
    var journal = [
      ['2027-04-22 09:33', 'Alex Modèle', 'Consultation de fiche', 'AC-2027-0049'], ['2027-04-22 09:31', 'Alex Modèle', 'Connexion (appareil de confiance)', '—'],
      ['2027-04-22 08:12', 'Site', 'Demande créée', 'AC-2027-0052'], ['2027-04-22 08:12', 'n8n', 'SMS envoyé (demande A)', 'AC-2027-0052'],
      ['2027-04-21 16:02', 'Secrétariat (démo)', 'Modification (champ : visite.prevue_le)', 'AC-2027-0046'], ['2027-04-21 12:40', 'Alex Modèle (lien en un clic)', 'Pas de réponse (tentative 1)', 'AC-2027-0049'],
      ['2027-04-20 17:05', 'Camille Exemple', 'Export CSV (12 lignes)', 'Demandes'], ['2027-04-19 10:15', 'Agence, marketing (démo)', 'Dépense saisie (Meta, avril)', 'Paramètres'],
      ['2027-04-19 09:02', 'Agence, technique (démo)', 'Connexion échouée (1)', '—'], ['2027-04-13 11:20', 'Camille Exemple', 'Effacement (demande d’une personne)', 'AC-2026-0004']
    ];
    return '<div class="entete-page"><div><h1 tabindex="-1">Journal et données personnelles</h1><p class="sous-titre">Accès, export et effacement sur demande (nLPD), purge, et trace de chaque action. Associés seulement.</p></div></div>' +
      '<div class="grille-2"><section class="panneau" aria-labelledby="t-droits"><h2 id="t-droits">Trouver une personne</h2><div class="filtres"><label style="flex:1">E-mail ou téléphone<input type="search" id="d-recherche" placeholder="lina.untel@example.com"></label></div><div id="d-resultat" aria-live="polite"><p class="petit discret">Essayez « lina.untel@example.com » ou « 079 000 00 06 ».</p></div></section>' +
      '<section class="panneau" aria-labelledby="t-reg"><h2 id="t-reg">Demandes d’exercice des droits</h2><table class="tableau"><caption class="sr">Registre</caption><thead><tr><th scope="col">Reçue</th><th scope="col">Type</th><th scope="col">Échéance</th><th scope="col">État</th></tr></thead><tbody>' +
      '<tr><td>12.04.2027</td><td>Effacement, par e-mail</td><td>12.05.2027</td><td>Traitée le 13.04 (identité vérifiée)</td></tr><tr><td>02.03.2027</td><td>Accès, par courrier</td><td>01.04.2027</td><td>Export envoyé le 05.03</td></tr></tbody></table>' +
      '<h3 class="mt">Purge automatique</h3><p class="petit">Demandes sans suite anonymisées 24 mois après le dernier contact. Aucune dans les 30 prochains jours. Prochaines : ' +
      perdues.map(function (r) { var d = parts(r.perdue.t); return esc(r.ref) + ' le ' + pad(d.j) + '.' + pad(d.m) + '.' + (d.y + 2); }).join(', ') + '.</p></section></div>' +
      '<section class="panneau mt" aria-labelledby="t-jr"><div class="panneau-entete"><h2 id="t-jr">Journal d’audit</h2><span class="discret">12 mois ; jamais de valeur personnelle, seulement les noms des champs</span><span class="droite"><button class="btn btn-petit btn-discret" type="button" data-maquette="Export du journal (CSV), lui-même journalisé.">Exporter</button></span></div>' +
      '<div class="defile"><table class="tableau"><caption class="sr">Journal d’audit</caption><thead><tr><th scope="col">Quand</th><th scope="col">Qui</th><th scope="col">Action</th><th scope="col">Objet</th></tr></thead><tbody>' +
      journal.map(function (j) { return '<tr><td>' + esc(dateH(t(j[0]))) + '</td><td>' + esc(j[1]) + '</td><td>' + esc(j[2]) + '</td><td class="ref">' + esc(j[3]) + '</td></tr>'; }).join('') + '</tbody></table></div></section>';
  };
  function resultatPersonne(q) {
    var qn = q.replace(/\D/g, ''), ql = q.trim().toLowerCase();
    var l = D.filter(function (r) { return (ql.length > 3 && r.email && r.email === ql) || (qn.length >= 9 && r.telAff.replace(/\D/g, '') === qn); });
    if (!q.trim()) return '<p class="petit discret">Essayez « lina.untel@example.com » ou « 079 000 00 06 ».</p>';
    if (!l.length) return '<p class="vide">Aucune personne avec ces coordonnées. Vérifiez l’orthographe, ou cherchez par l’autre moyen de contact.</p>';
    var r = l[0];
    return '<p><b>' + esc(r.nom) + '</b> : ' + l.length + ' demande(s) : ' + l.map(function (x) { return '<a href="#/demandes/' + x.ref + '">' + x.ref + '</a> (' + esc(L.statut[x.statut]) + ')'; }).join(', ') + '.</p>' +
      '<div class="groupe-btn"><button class="btn btn-discret" type="button" data-maquette="Export ZIP : JSON, PDF lisible et fichiers ; journalisé.">Exporter les données</button><button class="btn btn-danger" type="button" data-effacer="' + r.ref + '">Effacer…</button></div>';
  }

  /* ================= Routeur ================= */
  var TITRES = { vue: 'Vue d’ensemble', 'a-traiter': 'À traiter', demandes: 'Demandes', colonnes: 'Demandes par étape', fiche: 'Fiche demande', saisie: 'Saisir un appel', offres: 'Offres et chantiers', acquisition: 'Acquisition', visibilite: 'SEO et visibilité', avis: 'Avis', rapport: 'Rapport mensuel', parametres: 'Paramètres', donnees: 'Journal et données personnelles' };
  function lireRoute() {
    var h = location.hash.replace(/^#\/?/, ''), q = {}, i = h.indexOf('?');
    if (i >= 0) { h.slice(i + 1).split('&').forEach(function (kv) { var p = kv.split('='); q[decodeURIComponent(p[0])] = decodeURIComponent(p[1] || ''); }); h = h.slice(0, i); }
    var seg = h.split('/').filter(Boolean);
    if (!seg.length) return { nom: 'vue', nav: 'vue', q: q };
    if (seg[0] === 'demandes' && seg[1] === 'colonnes') return { nom: 'colonnes', nav: 'demandes', q: q };
    if (seg[0] === 'demandes' && seg[1]) return { nom: 'fiche', nav: 'demandes', q: q, arg: seg[1] };
    if (seg[0] === 'parametres') return { nom: 'parametres', nav: 'parametres', q: q, arg: seg[1] };
    return { nom: ECRANS[seg[0]] ? seg[0] : 'vue', nav: seg[0], q: q };
  }
  var routePrec = null;
  function rendre() {
    var r = lireRoute(), main = document.getElementById('contenu');
    main.innerHTML = ECRANS[r.nom](r.q, r.arg);
    document.title = (r.nom === 'fiche' && PAR_REF[r.arg] ? PAR_REF[r.arg].nom + ', ' + r.arg : TITRES[r.nom]) + ', Gestion Andy Construct (maquette)';
    Array.prototype.forEach.call(document.querySelectorAll('[data-route]'), function (a) { if (a.getAttribute('data-route') === r.nav) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
    if (r.nom === 'saisie') majScoreSaisie();
    brancherCourbes();
    var cle = r.nom + '/' + (r.arg || '');
    if (routePrec !== null && routePrec !== cle) { var h1 = main.querySelector('h1'); window.scrollTo(0, 0); if (h1) h1.focus({ preventScroll: true }); }
    routePrec = cle;
    cacherInfobulle();
  }

  /* ================= Interactions ================= */
  function message(txt, annuler) {
    var box = document.getElementById('messages'), el = document.createElement('div');
    el.className = 'message-flash'; el.setAttribute('role', 'status');
    var sp = document.createElement('span'); sp.textContent = txt; el.appendChild(sp);
    if (annuler) { var b = document.createElement('button'); b.type = 'button'; b.textContent = 'Annuler'; b.addEventListener('click', function () { el.remove(); message('Action annulée.'); }); el.appendChild(b); }
    box.appendChild(el);
    setTimeout(function () { el.remove(); }, 6000);
  }
  var dialogue = document.getElementById('dialogue');
  function ouvrirDialogue(titre, corps, boutons) {
    dialogue.innerHTML = '<form method="dialog"><div class="dialogue-corps"><h2 id="dialogue-titre">' + esc(titre) + '</h2>' + corps + '</div><div class="dialogue-pied">' + boutons + '</div></form>';
    if (typeof dialogue.showModal === 'function') dialogue.showModal(); else dialogue.setAttribute('open', '');
    var premier = dialogue.querySelector('input, select, textarea, .choix-appel button, .dialogue-pied button');
    if (premier) premier.focus();
  }
  function fermerDialogue() { if (dialogue.open) dialogue.close(); else dialogue.removeAttribute('open'); }
  function dialogueResultat(ref) {
    var r = PAR_REF[ref];
    ouvrirDialogue('Résultat de l’appel', '<p class="discret" style="margin:0">' + esc(r.nom + ', ' + (r.telAff || 'sans téléphone')) + '</p><div class="choix-appel">' +
      '<button class="btn" type="button" data-res="J’ai eu la personne : contact établi, escalade arrêtée.">J’ai eu la personne</button>' +
      '<button class="btn" type="button" data-res="Pas de réponse : tentative ' + (r.tents.length + 1) + ' notée ; SMS « Nous avons essayé de vous joindre » ; nouvel essai demain à 10 h.">Pas de réponse</button>' +
      '<button class="btn" type="button" data-res="Message laissé : tentative notée, nouvel essai demain à 10 h.">Message laissé</button>' +
      '<button class="btn" type="button" data-res="Numéro erroné : la demande passe en réponse par e-mail.">Numéro erroné</button></div>', '<button class="btn btn-discret" value="annuler">Plus tard</button>');
  }
  function dialogueAction(action, ref) {
    var r = PAR_REF[ref], nom = r ? r.nom : '';
    var motifs = '<label class="champ"><span>Motif <span class="aide-champ">obligatoire</span></span><select required id="dlg-motif"><option value="">Choisir</option>' + Object.keys(M.MOTIFS).map(function (k) { return '<option value="' + k + '">' + esc(M.MOTIFS[k]) + '</option>'; }).join('') + '</select></label><label class="case" style="display:flex;gap:8px"><input type="checkbox"> La personne accepte d’être recontactée dans 6 mois</label>';
    var formes = {
      perdue: ['Marquer perdue', motifs, 'Marquée perdue (maquette).'],
      signee: ['Marquer signée', '<label class="champ"><span>Date de signature</span><input type="date" value="2027-04-22"></label><label class="champ"><span>Montant signé (CHF, HT)</span><input inputmode="decimal" value="' + (r && r.offre ? r.offre.m : '') + '"></label>', 'Signée : le chantier est créé « à planifier » (maquette).'],
      offre_envoyee: ['Envoyer l’offre', '<label class="champ"><span>N° de l’offre</span><input value="O-' + (r ? r.ref.slice(3) : '') + '-1"></label><label class="champ"><span>Montant (CHF, HT)</span><input inputmode="decimal" required></label><label class="champ"><span>Date d’envoi</span><input type="date" value="2027-04-22"></label><label class="champ"><span>PDF de l’offre <span class="aide-champ">facultatif</span></span><input type="file"></label>', 'Offre enregistrée : relances J+3, J+10 et J+21 programmées (maquette).'],
      visite_planifiee: ['Planifier la visite', '<label class="champ"><span>Date et heure</span><input type="datetime-local" value="2027-04-26T08:00"></label><label class="champ"><span>Adresse</span><input value="' + esc(r ? r.npa + ' ' + r.commune : '') + '"></label><label class="champ"><span>Associé</span><select><option>Alex Modèle</option><option>Camille Exemple</option></select></label>', 'Visite planifiée ; invitation de calendrier envoyée à l’associé (maquette).'],
      reorientation: ['Réponse de réorientation', '<p>Bonjour Monsieur ' + esc(nom.split(' ').slice(-1)[0]) + ', merci pour votre demande. La rénovation de façade ne fait pas partie de nos métiers (placo, peinture intérieure, isolation acoustique, cloisons isolantes). Nous vous conseillons de vous adresser à une entreprise de façades. Avec nos meilleures salutations, Alex Modèle, Andy Construct.</p><p class="petit discret">Rien ne part sans ce clic (v2 §2.4).</p>', 'Réponse de réorientation envoyée (maquette).'],
      hors_cible: ['Hors cible', '<p>La demande sera classée hors cible et la réponse de réorientation vous sera proposée.</p>', 'Classée hors cible (maquette).'],
      reattribuer: ['Réattribuer', '<label class="champ"><span>Associé</span><select><option>Camille Exemple</option><option>Alex Modèle</option></select></label><label class="champ"><span>Motif</span><input></label>', 'Réattribuée (maquette).']
    };
    var f = formes[action];
    if (!f) { message('Maquette : « ' + action.replace(/[-_]/g, ' ') + ' » serait enregistré et journalisé.', true); return; }
    ouvrirDialogue(f[0] + (nom ? ', ' + nom : ''), f[1], '<button class="btn btn-discret" value="annuler" type="submit">Annuler</button><button class="btn btn-principal" type="button" data-valider="' + esc(f[2]) + '">' + esc(f[0] === 'Réponse de réorientation' ? 'Envoyer la réponse' : 'Enregistrer') + '</button>');
  }
  function dialogueEffacer(ref) {
    var r = PAR_REF[ref];
    ouvrirDialogue('Effacer les données de ' + r.nom, '<p><b>Effacé :</b> nom, téléphone, e-mail, message, commune exacte, notes, fichiers, gclid.</p><p><b>Gardé :</b> date, canal, priorité, statut et montants, anonymisés, pour que les indicateurs ne changent pas ; une empreinte de l’e-mail sur la liste d’opposition si la personne refuse tout contact. Les pièces comptables sont hors de l’admin.</p>' +
      '<label class="champ"><span>Tapez la référence ' + esc(r.ref) + ' pour confirmer</span><input id="dlg-confirmer" autocomplete="off"></label>', '<button class="btn btn-discret" value="annuler" type="submit">Annuler</button><button class="btn btn-principal" type="button" id="dlg-effacer" disabled data-valider="Données effacées et action journalisée (maquette).">Effacer définitivement</button>');
    dialogue.querySelector('#dlg-confirmer').addEventListener('input', function (e) { dialogue.querySelector('#dlg-effacer').disabled = e.target.value.trim().toUpperCase() !== r.ref; });
  }

  document.addEventListener('click', function (e) {
    var el = e.target.closest('button, a');
    if (!el) return;
    var d = el.dataset;
    if (d.appeler) { e.preventDefault(); message('Maquette : aucun appel n’est lancé. Dans l’admin, le téléphone compose le numéro ; au retour, la fenêtre « Résultat de l’appel » s’ouvre.'); setTimeout(function () { dialogueResultat(d.appeler); }, 500); return; }
    if (d.resultat) { dialogueResultat(d.resultat); return; }
    if (d.res) { fermerDialogue(); message('Enregistré (maquette) : ' + d.res, true); return; }
    if (d.valider) { var m = dialogue.querySelector('#dlg-motif'); if (m && !m.value) { m.focus(); m.setAttribute('aria-invalid', 'true'); message('Choisissez un motif : il est obligatoire pour une demande perdue.'); return; } fermerDialogue(); message(d.valider, true); return; }
    if (d.action) { dialogueAction(d.action, d.ref); return; }
    if (d.effacer) { dialogueEffacer(d.effacer); return; }
    if (d.maquette) { message('Maquette : ' + d.maquette, false); return; }
    if (d.plusActions) { var r = PAR_REF[d.plusActions]; ouvrirDialogue('Actions', '<div class="actions-fiche">' + actionsFiche(r) + '</div>', '<button class="btn btn-discret" value="annuler">Fermer</button>'); return; }
    if (d.toutes != null) { etatTraiter.toutes = d.toutes === '1'; rendre(); return; }
    if (d.tri) { if (filtres.tri === d.tri) filtres.sens = -filtres.sens; else { filtres.tri = d.tri; filtres.sens = 1; } majListe(); return; }
    if (d.col != null) { etatColonnes.active = +d.col; rendre(); return; }
    if (el.id === 'f-effacer') { filtres.q = ''; filtres.periode = 'tout'; filtres.statut = 'toutes'; filtres.prio = ''; filtres.canal = ''; filtres.who = ''; filtres.retard = false; rendre(); return; }
    if (el.id === 'bouton-pdf') { window.print(); return; }
    if (el.id === 'bouton-plus') {
      ouvrirDialogue('Plus', '<ul class="plus-menu">' + [['#/offres', 'Offres et chantiers'], ['#/acquisition', 'Acquisition'], ['#/visibilite', 'SEO et visibilité'], ['#/avis', 'Avis'], ['#/rapport', 'Rapport mensuel'], ['#/parametres', 'Paramètres'], ['#/donnees', 'Journal et données personnelles']].map(function (l) { return '<li><a href="' + l[0] + '" data-fermer="1">' + esc(l[1]) + '</a></li>'; }).join('') + '</ul>', '<button class="btn btn-discret" value="annuler">Fermer</button>');
      return;
    }
    if (d.fermer) { fermerDialogue(); return; }
    if (el.classList.contains('aide')) { var id = el.getAttribute('aria-controls'), p = document.getElementById(id); var ouvert = el.getAttribute('aria-expanded') === 'true'; el.setAttribute('aria-expanded', String(!ouvert)); p.hidden = ouvert; return; }
  });
  function majListe() { var z = document.getElementById('resultats-liste'); if (z) z.innerHTML = resultatsListe(); }
  document.addEventListener('input', function (e) {
    var id = e.target.id;
    if (id === 'f-q') { filtres.q = e.target.value; majListe(); }
    if (e.target.closest && e.target.closest('#form-saisie')) majScoreSaisie();
    if (id === 's-tel') {
      var qn = e.target.value.replace(/\D/g, ''), z = document.getElementById('s-doublon');
      var trouve = qn.length >= 9 ? D.filter(function (r) { return r.telAff.replace(/\D/g, '') === qn; })[0] : null;
      z.innerHTML = trouve ? '<b>Ce numéro existe :</b> <a href="#/demandes/' + trouve.ref + '">' + trouve.ref + '</a>, ' + esc(trouve.nom) + ' (' + esc(L.statut[trouve.statut]) + '). La nouvelle demande lui sera rattachée.' : 'En premier : on retrouve un contact existant.';
    }
    if (id === 'd-recherche') document.getElementById('d-resultat').innerHTML = resultatPersonne(e.target.value);
    if (id === 'test-npa') { var n = e.target.value.trim(), zz = zoneDeNpa(n); document.getElementById('test-npa-res').textContent = /^[1-9]\d{3}$/.test(n) ? 'NPA ' + n + ' : ' + (zz === 'hors' ? 'hors Suisse romande' : 'zone ' + zz) + ' (approximation de la maquette).' : ''; }
    if (id === 'recherche-globale') rechercher(e.target.value);
  });
  document.addEventListener('change', function (e) {
    var id = e.target.id, v = e.target.value;
    if (id === 'choix-mois') { location.hash = '#/' + (v === '2027-04' ? '' : '?mois=' + v); return; }
    if (id === 'acq-periode') { etatAcq.periode = v; rendre(); return; }
    var map = { 'f-periode': 'periode', 'f-statut': 'statut', 'f-prio': 'prio', 'f-canal': 'canal', 'f-who': 'who' };
    if (map[id]) { filtres[map[id]] = v; majListe(); }
    if (id === 'f-retard') { filtres.retard = e.target.checked; majListe(); }
  });
  document.addEventListener('submit', function (e) {
    if (e.target.id === 'form-saisie') {
      e.preventDefault();
      var fd = new FormData(e.target), err = [];
      if (!fd.get('telephone')) err.push('le téléphone');
      if (!fd.get('nom')) err.push('le nom');
      if (!fd.get('connu')) err.push('« Comment nous avez-vous connus ? »');
      var z = document.getElementById('s-erreurs');
      if (err.length) { z.innerHTML = '<span class="alerte-texte">Il manque ' + esc(err.join(', ')) + '.</span>'; return; }
      z.textContent = '';
      message('Demande AC-2027-0053 enregistrée, contact établi (maquette : rien n’est gardé).', true);
    }
  });

  /* Recherche globale */
  function rechercher(v) {
    var ul = document.getElementById('resultats-recherche'), inp = document.getElementById('recherche-globale');
    var q = v.trim().toLowerCase(), qn = q.replace(/\D/g, '');
    if (q.length < 3) { ul.hidden = true; inp.setAttribute('aria-expanded', 'false'); return; }
    var l = D.filter(function (r) { return (r.nom + ' ' + (r.org || '') + ' ' + r.ref + ' ' + r.commune).toLowerCase().indexOf(q) >= 0 || (qn.length >= 3 && r.telAff.replace(/\D/g, '').indexOf(qn) >= 0); }).slice(0, 6);
    ul.innerHTML = l.length ? l.map(function (r) { return '<li><a href="#/demandes/' + r.ref + '"><b>' + esc(r.nom) + '</b> <span class="discret">' + r.ref + ', ' + esc(r.commune) + ', ' + esc(L.statut[r.statut]) + '</span></a></li>'; }).join('') : '<li class="discret" style="padding:8px 12px">Aucun résultat.</li>';
    ul.hidden = false; inp.setAttribute('aria-expanded', 'true');
  }
  document.addEventListener('click', function (e) { if (!e.target.closest('.recherche')) { var ul = document.getElementById('resultats-recherche'); ul.hidden = true; document.getElementById('recherche-globale').setAttribute('aria-expanded', 'false'); } });
  window.addEventListener('hashchange', function () { var ul = document.getElementById('resultats-recherche'); ul.hidden = true; var inp = document.getElementById('recherche-globale'); inp.value = ''; if (dialogue.open) fermerDialogue(); });

  /* Info-bulles (survol et clavier) : texte inséré avec textContent */
  var bulle = document.getElementById('infobulle');
  function montrerInfobulle(el, x, y) {
    var l = (el.getAttribute('data-tip') || '').split('|');
    bulle.textContent = '';
    var s = document.createElement('strong'); s.textContent = l[0]; bulle.appendChild(s);
    if (l[1]) { var p = document.createElement('span'); p.textContent = l[1]; bulle.appendChild(p); }
    bulle.style.display = 'block';
    var w = bulle.offsetWidth, h = bulle.offsetHeight;
    bulle.style.left = Math.min(window.innerWidth - w - 8, Math.max(8, x + 12)) + 'px';
    bulle.style.top = Math.max(8, y - h - 12) + 'px';
  }
  function cacherInfobulle() { bulle.style.display = 'none'; }
  document.addEventListener('pointermove', function (e) { var el = e.target.closest && e.target.closest('[data-tip]'); if (el) montrerInfobulle(el, e.clientX, e.clientY); else if (!e.target.closest || !e.target.closest('.zone-curseur')) cacherInfobulle(); });
  document.addEventListener('focusin', function (e) { var el = e.target.closest && e.target.closest('[data-tip]'); if (el) { var b = el.getBoundingClientRect(); montrerInfobulle(el, b.left + b.width / 2, b.top); } });
  document.addEventListener('focusout', function () { cacherInfobulle(); });

  /* Curseur des courbes */
  function brancherCourbes() {
    Object.keys(COURBES).forEach(function (id) {
      var svg = document.getElementById(id); if (!svg) { delete COURBES[id]; return; }
      var C = COURBES[id], zone = svg.querySelector('.zone-curseur'), g = svg.querySelector('.survol'), ligne = g.querySelector('line'), pt = g.querySelector('circle'), idx = C.points.length - 1;
      function placer(i, clientX, clientY) {
        idx = Math.max(0, Math.min(C.points.length - 1, i));
        var x = C.x(idx), y = C.y(C.points[idx][1]);
        g.style.display = ''; ligne.setAttribute('x1', x); ligne.setAttribute('x2', x); pt.setAttribute('cx', x); pt.setAttribute('cy', y);
        var b = svg.getBoundingClientRect(), vb = svg.viewBox.baseVal, k = b.width / vb.width;
        bulle.textContent = '';
        var s = document.createElement('strong'); s.textContent = nb(C.points[idx][1]) + ' ' + C.unite; bulle.appendChild(s);
        var p = document.createElement('span'); p.textContent = C.points[idx][0]; bulle.appendChild(p);
        bulle.style.display = 'block';
        bulle.style.left = Math.min(window.innerWidth - bulle.offsetWidth - 8, b.left + x * k + 12) + 'px';
        bulle.style.top = Math.max(8, b.top + y * k - bulle.offsetHeight - 12) + 'px';
      }
      zone.addEventListener('pointermove', function (e) {
        var b = svg.getBoundingClientRect(), vb = svg.viewBox.baseVal, xv = (e.clientX - b.left) * vb.width / b.width, best = 0, dist = Infinity;
        C.points.forEach(function (_, i) { var dd = Math.abs(C.x(i) - xv); if (dd < dist) { dist = dd; best = i; } });
        placer(best);
      });
      zone.addEventListener('pointerleave', function () { g.style.display = 'none'; cacherInfobulle(); });
      zone.addEventListener('focus', function () { placer(idx); });
      zone.addEventListener('blur', function () { g.style.display = 'none'; cacherInfobulle(); });
      zone.addEventListener('keydown', function (e) { if (e.key === 'ArrowLeft') { placer(idx - 1); e.preventDefault(); } if (e.key === 'ArrowRight') { placer(idx + 1); e.preventDefault(); } });
    });
  }

  /* Thème */
  var bTheme = document.getElementById('bouton-theme');
  function themeActuel() { var a = document.documentElement.getAttribute('data-theme'); if (a) return a; return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'; }
  function majBoutonTheme() { var s = themeActuel() === 'dark'; bTheme.setAttribute('aria-pressed', String(s)); bTheme.title = s ? 'Thème clair' : 'Thème sombre'; bTheme.querySelector('.sr').textContent = 'Thème sombre'; }
  bTheme.addEventListener('click', function () { var n = themeActuel() === 'dark' ? 'light' : 'dark'; document.documentElement.setAttribute('data-theme', n); try { localStorage.setItem('ac-maquette-theme', n); } catch (e) { /* stockage indisponible : le thème vaut pour la page */ } majBoutonTheme(); });
  majBoutonTheme();

  /* Pastilles : retards et rappels du jour */
  var nPast = D.filter(function (r) { return r.statut === 'nouvelle' && (enRetard(r) || cleJour(prochaineEch(r)) === cleJour(NOW)); }).length;
  ['pastille-lateral', 'pastille-bas'].forEach(function (id) { var p = document.getElementById(id); p.textContent = nPast; p.setAttribute('aria-label', nPast + ' demandes à rappeler aujourd’hui ou en retard'); });

  window.addEventListener('hashchange', rendre);
  rendre();

  /* Pour la vérification automatique (Playwright) : quelques valeurs calculées. */
  window.__maquette = { demandes: D.length, avril: comptes('2027-04'), mars: comptes('2027-03'), retards: D.filter(enRetard).map(function (r) { return r.ref; }) };
})();
