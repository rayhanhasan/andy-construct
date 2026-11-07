/* Pilotage Andy Construct : logique du tableau de bord (vanilla, sans dépendance).
   Les données viennent de donnees.js (window.PROJET). Les changements de statut faits
   dans l'interface sont gardés dans le navigateur (localStorage) jusqu'à l'export. */
(function () {
  'use strict';

  var BASE = window.PROJET;
  if (!BASE) {
    document.getElementById('contenu').innerHTML = '<p class="vide">donnees.js est introuvable ou contient une erreur de syntaxe. Ouvrez-le dans un éditeur et vérifiez les virgules et les guillemets.</p>';
    return;
  }

  var CLE = 'andy-projet-v1';
  var EDITABLES = ['taches', 'questionnaire', 'decisions', 'assets'];

  /* ---------- Libellés ---------- */
  var L = {
    taches: { 'a-faire': 'À faire', 'en-cours': 'En cours', 'attente-client': 'En attente client', 'fait': 'Fait' },
    questionnaire: { 'a-envoyer': 'À envoyer', 'envoye': 'Envoyé', 'repondu': 'Répondu' },
    decisions: { 'a-prendre': 'À prendre', 'prise': 'Prise' },
    assets: { 'a-demander': 'À demander', 'demande': 'Demandé', 'recu': 'Reçu' },
    infos: { 'verifie': 'Vérifié', 'a-confirmer': 'À confirmer', 'manquant': 'Manquant' },
    juridique: { 'pret': 'Prêt', 'a-completer': 'À compléter', 'a-faire': 'À faire', 'bloque': 'Bloqué' }
  };
  var ICO = { 'verifie': '✓', 'pret': '✓', 'recu': '✓', 'repondu': '✓', 'prise': '✓', 'a-confirmer': '?', 'a-completer': '?', 'envoye': '…', 'demande': '…', 'manquant': '×', 'bloque': '×', 'a-faire': '', 'a-envoyer': '', 'a-demander': '', 'a-prendre': '' };
  var ORDRE_COL = ['a-faire', 'en-cours', 'attente-client', 'fait'];
  var ORDRE_EMPILE = ['fait', 'en-cours', 'attente-client', 'a-faire'];
  var PRIO = { haute: 0, moyenne: 1, basse: 2 };
  var VUES = [
    ['apercu', "Vue d'ensemble"], ['taches', 'Tâches'], ['decisions', 'Décisions'], ['questionnaire', 'Questionnaire client'],
    ['infos', 'Infos à compléter'], ['assets', 'Assets à fournir'], ['juridique', 'Juridique'], ['strategie', 'Stratégie'],
    ['livrables', 'Livrables et liens'], ['journal', 'Journal']
  ];

  /* ---------- Stockage local (toujours protégé) ---------- */
  function lire() {
    try { var s = JSON.parse(localStorage.getItem(CLE) || '{}'); return (s && typeof s === 'object') ? s : {}; } catch (e) { return {}; }
  }
  function ecrire() {
    try { localStorage.setItem(CLE, JSON.stringify(etat)); } catch (e) { /* stockage indisponible : l'interface marche quand même */ }
  }
  var etat = lire();
  etat.modifs = etat.modifs || {};
  EDITABLES.forEach(function (k) { etat.modifs[k] = etat.modifs[k] || {}; });

  /* Retire les modifications déjà présentes dans donnees.js (après un export remplacé). */
  function nettoyer() {
    EDITABLES.forEach(function (k) {
      var m = etat.modifs[k];
      Object.keys(m).forEach(function (id) {
        var it = (BASE[k] || []).find(function (x) { return x.id === id; });
        if (!it || it.statut === m[id]) delete m[id];
      });
    });
  }
  nettoyer();
  ecrire();

  function statut(type, it) { var m = etat.modifs[type] && etat.modifs[type][it.id]; return m || it.statut; }
  function nbModifs() { return EDITABLES.reduce(function (n, k) { return n + Object.keys(etat.modifs[k]).length; }, 0); }
  function changer(type, id, val) {
    var it = BASE[type].find(function (x) { return x.id === id; });
    if (!it) return;
    if (it.statut === val) delete etat.modifs[type][id]; else etat.modifs[type][id] = val;
    etat.exporte = false;
    ecrire();
    rendreTout();
  }

  /* ---------- Outils ---------- */
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function $(id) { return document.getElementById(id); }
  function aujourdhui() { var d = new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  var MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
  function dateFr(iso, court) {
    if (!iso) return '';
    var p = iso.split('-'); var j = +p[2];
    return (j === 1 ? '1er' : j) + ' ' + MOIS[+p[1] - 1] + (court ? '' : ' ' + p[0]);
  }
  function lien(chemin, texte) {
    if (!chemin) return esc(texte || '');
    var href = /^https?:/.test(chemin) ? chemin : (chemin.indexOf('projet/') === 0 ? chemin.slice(7) || './' : '../' + chemin);
    return '<a href="' + esc(href) + '"' + (/^https?:/.test(chemin) ? ' rel="noopener"' : '') + '>' + esc(texte || chemin) + '</a>';
  }
  function badge(type, s) {
    return '<span class="etat e-' + esc(s) + '"><span class="etat__ico" aria-hidden="true">' + (ICO[s] || '') + '</span>' + esc(L[type][s] || s) + '</span>';
  }
  function chantierNom(id) { var c = BASE.chantiers.find(function (x) { return x.id === id; }); return c ? c.nom : id; }
  function texteDe(o) { return Object.keys(o).map(function (k) { var v = o[k]; return Array.isArray(v) ? v.join(' ') : (typeof v === 'object' ? '' : v); }).join(' ').toLowerCase(); }
  function filtreTexte(liste) { var q = recherche.trim().toLowerCase(); return q ? liste.filter(function (x) { return texteDe(x).indexOf(q) !== -1; }) : liste; }
  function selectStatut(type, it, etiquette) {
    var s = statut(type, it);
    return '<label class="vh" for="s-' + type + '-' + esc(it.id) + '">' + esc(etiquette) + '</label>' +
      '<select id="s-' + type + '-' + esc(it.id) + '" data-type="' + type + '" data-id="' + esc(it.id) + '">' +
      Object.keys(L[type]).map(function (k) { return '<option value="' + k + '"' + (k === s ? ' selected' : '') + '>' + L[type][k] + '</option>'; }).join('') +
      '</select>' + (etat.modifs[type][it.id] ? ' <span class="modifie-marque">modifié</span>' : '');
  }

  /* ---------- Filtres de vue ---------- */
  var recherche = '';
  var filtres = { tResp: '', tChantier: '', tPrio: '', iStatut: '', qStatut: '', dStatut: '', aStatut: '' };

  /* ---------- Cartouche ---------- */
  function rendreMeta() {
    var m = BASE.meta;
    $('meta').innerHTML = [['Client', m.client], ['Agence', m.agence], ['Données du', dateFr(m.maj)]].map(function (x) {
      return '<div><dt>' + esc(x[0]) + '</dt><dd>' + esc(x[1]) + '</dd></div>';
    }).join('');
  }
  function rendreLocal() {
    var n = nbModifs();
    var box = $('local');
    box.classList.toggle('local--modifie', n > 0);
    $('local-etat').textContent = n === 0 ? 'Aucune modification locale' :
      (etat.exporte ? n + ' modification' + (n > 1 ? 's' : '') + ' exportée' + (n > 1 ? 's' : '') + ' : remplacez donnees.js'
        : n + ' modification' + (n > 1 ? 's' : '') + ' locale' + (n > 1 ? 's' : '') + ' non exportée' + (n > 1 ? 's' : ''));
    $('annuler').hidden = n === 0;
  }

  /* ---------- Navigation ---------- */
  function vueCourante() { var h = location.hash.replace('#', ''); return VUES.some(function (v) { return v[0] === h; }) ? h : 'apercu'; }
  function comptes() {
    var t = BASE.taches.filter(function (x) { return statut('taches', x) !== 'fait'; }).length;
    return {
      taches: t,
      decisions: BASE.decisions.filter(function (x) { return statut('decisions', x) === 'a-prendre'; }).length,
      questionnaire: BASE.questionnaire.filter(function (x) { return statut('questionnaire', x) !== 'repondu'; }).length,
      infos: BASE.infos.filter(function (x) { return x.statut !== 'verifie'; }).length,
      assets: BASE.assets.filter(function (x) { return statut('assets', x) !== 'recu'; }).length,
      juridique: BASE.juridique.filter(function (x) { return x.statut !== 'pret'; }).length
    };
  }
  function rendreNav() {
    var c = comptes(), v = vueCourante();
    $('nav').innerHTML = VUES.map(function (x) {
      var n = c[x[0]];
      return '<li><a href="#' + x[0] + '"' + (x[0] === v ? ' aria-current="page"' : '') + '><span>' + esc(x[1]) + '</span>' +
        (n != null ? '<span class="compte" aria-label="' + n + ' ouverts">' + n + '</span>' : '') + '</a></li>';
    }).join('');
  }
  function montrerVue() {
    var v = vueCourante();
    document.querySelectorAll('.vue').forEach(function (s) { s.hidden = s.getAttribute('data-vue') !== v; });
    rendreNav();
    // Mobile : faire défiler la barre d'onglets jusqu'à l'onglet actif, sans bouger la page
    var ul = $('nav'), cur = ul.querySelector('[aria-current="page"]');
    if (cur && ul.scrollWidth > ul.clientWidth) ul.scrollLeft = cur.parentNode.offsetLeft - (ul.clientWidth - cur.offsetWidth) / 2;
  }

  /* ---------- Vue d'ensemble ---------- */
  function rendreApercu() {
    var T = BASE.taches, total = T.length;
    var faits = T.filter(function (x) { return statut('taches', x) === 'fait'; }).length;
    var pc = total ? Math.round(faits / total * 100) : 0;
    var attente = T.filter(function (x) { return statut('taches', x) === 'attente-client'; }).length;
    var decs = BASE.decisions.filter(function (x) { return statut('decisions', x) === 'a-prendre'; }).length;
    $('niveau').innerHTML =
      '<div class="niveau__ligne"><p class="niveau__pc">' + pc + '&nbsp;%</p>' +
      '<p class="niveau__legende">du projet est fait : <b>' + faits + ' tâches sur ' + total + '</b>. ' + esc(BASE.meta.etat) + '</p></div>' +
      '<div class="niveau__piste" role="img" aria-label="Avancement global : ' + pc + ' %"><span class="niveau__laser" style="width:' + pc + '%"></span><span class="niveau__repere" style="left:calc(' + pc + '% - 1px)"></span></div>' +
      '<div class="niveau__graduations" aria-hidden="true"><span>0</span><span>25</span><span>50</span><span>75</span><span>100 %</span></div>' +
      '<p class="niveau__faits"><span><b>' + attente + '</b> tâches en attente du client</span><span><b>' + decs + '</b> décisions à prendre</span><span><b>' +
      BASE.questionnaire.filter(function (x) { return statut('questionnaire', x) === 'a-envoyer'; }).length + '</b> questions à envoyer</span></p>';

    // Avancement par chantier
    $('chantiers').innerHTML = BASE.chantiers.map(function (c) {
      var ts = T.filter(function (x) { return x.chantier === c.id; });
      var f = ts.filter(function (x) { return statut('taches', x) === 'fait'; }).length;
      var p = ts.length ? Math.round(f / ts.length * 100) : 0;
      var tip = c.nom + ' : ' + f + ' tâche' + (f > 1 ? 's' : '') + ' faite' + (f > 1 ? 's' : '') + ' sur ' + ts.length + ' (' + p + ' %). ' + c.description + '.';
      return '<li><button class="chantier" type="button" data-chantier="' + esc(c.id) + '" data-tip="' + esc(tip) + '" aria-label="' + esc(tip + ' Voir les tâches.') + '">' +
        '<span class="chantier__nom">' + esc(c.nom) + '</span>' +
        '<span class="chantier__piste" aria-hidden="true"><span class="chantier__barre" style="width:' + p + '%"></span></span>' +
        '<span class="chantier__val" aria-hidden="true">' + f + '/' + ts.length + '</span></button></li>';
    }).join('');

    // Prochaine échéance
    var auj = aujourdhui();
    var ouvertes = T.filter(function (x) { return statut('taches', x) !== 'fait' && x.echeance; })
      .sort(function (a, b) { return a.echeance < b.echeance ? -1 : a.echeance > b.echeance ? 1 : PRIO[a.priorite] - PRIO[b.priorite]; });
    if (!ouvertes.length) {
      $('echeance').innerHTML = '<p class="vide">Aucune échéance datée. Ajoutez un champ « echeance » dans donnees.js.</p>';
    } else {
      var p0 = ouvertes[0], retard = p0.echeance < auj;
      $('echeance').innerHTML = '<p class="echeance__date">' + esc(dateFr(p0.echeance)) + '</p>' +
        (retard ? '<p class="retard">En retard</p>' : '') +
        '<p class="echeance__titre">' + esc(p0.titre) + '</p><p class="carte__meta"><span class="resp">' + esc(p0.responsable) + '</span><span>' + esc(chantierNom(p0.chantier)) + '</span></p>' +
        '<div class="echeance__suite">' + ouvertes.slice(1, 4).map(function (x) {
          return '<p><b>' + esc(dateFr(x.echeance, true)) + '</b> ' + esc(x.titre) + (x.echeance < auj ? ' <span class="retard">(en retard)</span>' : '') + '</p>';
        }).join('') + '</div>';
    }

    // Répartition (barre empilée + légende = étiquettes directes)
    var cnt = {}; ORDRE_EMPILE.forEach(function (s) { cnt[s] = 0; });
    T.forEach(function (x) { cnt[statut('taches', x)]++; });
    $('repartition').innerHTML = '<div class="empile" role="img" aria-label="' + esc(ORDRE_EMPILE.map(function (s) { return L.taches[s] + ' ' + cnt[s]; }).join(', ')) + '">' +
      ORDRE_EMPILE.filter(function (s) { return cnt[s]; }).map(function (s) {
        return '<span class="empile__seg p-' + s + '" style="flex:' + cnt[s] + '" tabindex="0" data-tip="' + esc(L.taches[s] + ' : ' + cnt[s] + ' tâches (' + Math.round(cnt[s] / total * 100) + ' %)') + '"></span>';
      }).join('') + '</div>' +
      '<ul class="legende">' + ORDRE_EMPILE.map(function (s) {
        return '<li><span class="pastille p-' + s + '" aria-hidden="true"></span>' + L.taches[s] + '<span class="val">' + cnt[s] + '</span></li>';
      }).join('') + '</ul>';

    // Blocages (les plus urgents ; le reste dans Tâches et Décisions)
    var bt = T.filter(function (x) { return statut('taches', x) === 'attente-client' && x.priorite === 'haute'; });
    var bd = BASE.decisions.filter(function (d) { return statut('decisions', d) === 'a-prendre' && d.bloque && d.bloque !== 'Rien'; });
    var bloc = bt.slice(0, 5).map(function (x) {
      return '<li><span class="type">Tâche ' + esc(x.id) + '</span><div><b>' + esc(x.titre) + '</b><p class="detail">' + esc(x.note) + '</p></div></li>';
    });
    bd.slice(0, 4).forEach(function (d) {
      bloc.push('<li><span class="type">Décision</span><div><b>' + esc(d.titre) + '</b><p class="detail">Bloque : ' + esc(d.bloque) + '</p></div></li>');
    });
    if (bt.length > 5 || bd.length > 4) {
      bloc.push('<li class="plus"><p>Et aussi ' + (bt.length > 5 ? '<a href="#taches">' + (bt.length - 5) + ' autres tâches prioritaires en attente</a>' : '') +
        (bt.length > 5 && bd.length > 4 ? ', ' : '') + (bd.length > 4 ? '<a href="#decisions">' + (bd.length - 4) + ' autres décisions bloquantes</a>' : '') + '.</p></li>');
    }
    $('blocages').innerHTML = bloc.join('') || '<li class="vide">Aucun blocage.</li>';

    // Infos
    var ci = { verifie: 0, 'a-confirmer': 0, manquant: 0 };
    BASE.infos.forEach(function (x) { ci[x.statut]++; });
    $('infos-resume').innerHTML = '<div class="etats">' + Object.keys(ci).map(function (s) {
      return '<p class="etat-ligne">' + badge('infos', s) + '<span class="val">' + ci[s] + '</span></p>';
    }).join('') + '<a href="#infos">Voir le détail</a></div>';

    $('ecarts').innerHTML = (BASE.ecarts || []).map(function (e) { return '<li>' + esc(e) + '</li>'; }).join('');
  }

  /* ---------- Tâches ---------- */
  function options(liste, val, tout) {
    return '<option value="">' + tout + '</option>' + liste.map(function (o) { return '<option value="' + esc(o[0]) + '"' + (o[0] === val ? ' selected' : '') + '>' + esc(o[1]) + '</option>'; }).join('');
  }
  function rendreFiltresTaches(nb) {
    $('filtres-taches').innerHTML =
      '<label>Responsable <select data-filtre="tResp">' + options([['Agence', 'Agence'], ['Claude', 'Claude'], ['Client', 'Client']], filtres.tResp, 'Tous') + '</select></label>' +
      '<label>Chantier <select data-filtre="tChantier">' + options(BASE.chantiers.map(function (c) { return [c.id, c.nom]; }), filtres.tChantier, 'Tous') + '</select></label>' +
      '<label>Priorité <select data-filtre="tPrio">' + options([['haute', 'Haute'], ['moyenne', 'Moyenne'], ['basse', 'Basse']], filtres.tPrio, 'Toutes') + '</select></label>' +
      '<span class="filtres__total">' + nb + ' tâche' + (nb > 1 ? 's' : '') + ' affichée' + (nb > 1 ? 's' : '') + '</span>';
  }
  function rendreTaches() {
    var auj = aujourdhui();
    var liste = filtreTexte(BASE.taches).filter(function (x) {
      return (!filtres.tResp || x.responsable === filtres.tResp) && (!filtres.tChantier || x.chantier === filtres.tChantier) && (!filtres.tPrio || x.priorite === filtres.tPrio);
    });
    rendreFiltresTaches(liste.length);
    $('kanban').innerHTML = ORDRE_COL.map(function (col) {
      var cs = liste.filter(function (x) { return statut('taches', x) === col; }).sort(function (a, b) {
        return PRIO[a.priorite] - PRIO[b.priorite] || (a.echeance || '9') .localeCompare(b.echeance || '9');
      });
      return '<section class="colonne" aria-labelledby="col-' + col + '"><div class="colonne__tete"><span class="pastille p-' + col + '" aria-hidden="true"></span><h3 id="col-' + col + '">' + L.taches[col] + '</h3><span class="n">' + cs.length + '</span></div>' +
        (cs.length ? '<ul class="cartes">' + cs.map(function (x) {
          var ech = x.echeance ? (col === 'fait' ? 'Fait le ' + dateFr(x.echeance, true) : 'Échéance ' + dateFr(x.echeance, true)) : '';
          var retard = col !== 'fait' && x.echeance && x.echeance < auj;
          return '<li class="carte' + (x.priorite === 'haute' && col !== 'fait' ? ' carte--haute' : '') + '">' +
            '<p class="carte__titre">' + esc(x.titre) + '</p>' +
            '<p class="carte__meta"><span class="resp">' + esc(x.responsable) + '</span><span>' + esc(chantierNom(x.chantier)) + '</span>' +
            '<span class="prio' + (x.priorite === 'haute' ? ' prio--haute' : '') + '">Priorité ' + esc(x.priorite) + '</span>' +
            (ech ? '<span' + (retard ? ' class="retard"' : '') + '>' + esc(ech) + (retard ? ' (en retard)' : '') + '</span>' : '') + '</p>' +
            (x.note ? '<p class="carte__note">' + esc(x.note) + '</p>' : '') +
            '<div class="carte__pied"><span class="carte__fichier">' + (x.fichier ? lien(x.fichier, x.fichier.split('/').filter(Boolean).pop()) : '') + '</span>' +
            '<span>' + selectStatut('taches', x, 'Statut de la tâche ' + x.id + ' : ' + x.titre) + '</span></div></li>';
        }).join('') + '</ul>' : '<p class="colonne__vide">Rien ici.</p>') + '</section>';
    }).join('');
  }

  /* ---------- Décisions ---------- */
  function puces(cle, type, liste) {
    var c = {}; liste.forEach(function (x) { var s = statut(type, x); c[s] = (c[s] || 0) + 1; });
    return '<div class="puces" role="group" aria-label="Filtrer par statut">' +
      '<button class="puce" type="button" data-puce="' + cle + '" data-val="" aria-pressed="' + (!filtres[cle]) + '">Tous<span class="n">' + liste.length + '</span></button>' +
      Object.keys(L[type]).map(function (s) {
        return '<button class="puce" type="button" data-puce="' + cle + '" data-val="' + s + '" aria-pressed="' + (filtres[cle] === s) + '">' + L[type][s] + '<span class="n">' + (c[s] || 0) + '</span></button>';
      }).join('') + '</div>';
  }
  function rendreDecisions() {
    $('filtres-decisions').innerHTML = puces('dStatut', 'decisions', BASE.decisions);
    var liste = filtreTexte(BASE.decisions).filter(function (d) { return !filtres.dStatut || statut('decisions', d) === filtres.dStatut; });
    $('decisions').innerHTML = liste.map(function (d) {
      return '<article class="decision"><div><h3>' + esc(d.titre) + '</h3><p class="decision__contexte">' + esc(d.contexte) + '</p>' +
        '<ul class="options" aria-label="Options">' + d.options.map(function (o, i) {
          var estReco = d.reco === i;
          return '<li' + (estReco ? ' class="reco"' : '') + '>' + esc(o) + (estReco ? ' <span class="tag-reco">Recommandé</span>' : '') + '</li>';
        }).join('') + '</ul></div>' +
        '<dl class="decision__cote"><div><dt>Notre recommandation</dt><dd class="decision__reco">' + esc(d.recommandation) + '</dd></div>' +
        '<div><dt>Bloque</dt><dd>' + esc(d.bloque) + '</dd></div><div><dt>Source</dt><dd>' + lien(d.source, d.source.split('/').pop()) + '</dd></div>' +
        '<div class="ligne-statut"><dt>Statut</dt><dd>' + selectStatut('decisions', d, 'Statut de la décision ' + d.titre) + '</dd></div></dl></article>';
    }).join('') || '<p class="vide">Aucune décision ne correspond.</p>';
  }

  /* ---------- Questionnaire ---------- */
  function themes(liste) { var t = []; liste.forEach(function (q) { if (t.indexOf(q.theme) === -1) t.push(q.theme); }); return t; }
  function texteQuestionnaire() {
    var qs = BASE.questionnaire.filter(function (q) { return statut('questionnaire', q) !== 'repondu'; });
    var out = ['Bonjour,', '',
      'Pour finaliser votre nouveau site, nous avons besoin de quelques validations.',
      'Pour chaque point, nous indiquons ce que nous proposons : il vous suffit de confirmer ou de corriger, directement sous la question.', ''];
    themes(qs).forEach(function (th, i) {
      out.push((i + 1) + '. ' + th.toUpperCase(), '');
      qs.filter(function (q) { return q.theme === th; }).forEach(function (q, j) {
        out.push((i + 1) + '.' + (j + 1) + ' ' + q.question, '    Nous proposons : ' + q.proposition, '    Votre réponse : ', '');
      });
    });
    out.push('Merci d\'avance pour vos réponses. Nous restons à votre disposition pour en parler de vive voix.', '', 'Avec nos meilleures salutations,', BASE.meta.agence);
    return out.join('\n');
  }
  function rendreQuestionnaire() {
    $('filtres-questionnaire').innerHTML = puces('qStatut', 'questionnaire', BASE.questionnaire);
    var liste = filtreTexte(BASE.questionnaire).filter(function (q) { return !filtres.qStatut || statut('questionnaire', q) === filtres.qStatut; });
    var n = 0;
    $('questionnaire').innerHTML = themes(liste).map(function (th) {
      return '<section class="theme-q"><h3>' + esc(th) + '</h3>' + liste.filter(function (q) { return q.theme === th; }).map(function (q) {
        n++;
        return '<article class="question"><span class="question__n">' + esc(q.id.replace('Q', '')) + '</span><div>' +
          '<p class="question__q">' + esc(q.question) + '</p>' +
          '<p class="question__prop"><b>Nous proposons :</b> ' + esc(q.proposition) + '</p>' +
          '<p class="question__src">Source : ' + esc(q.source) + (q.ref ? '. Code ' + esc(q.ref) : '') + '</p></div>' +
          '<div class="ligne-statut">' + badge('questionnaire', statut('questionnaire', q)) + selectStatut('questionnaire', q, 'Statut de la question ' + q.id) + '</div></article>';
      }).join('') + '</section>';
    }).join('') || '<p class="vide">Aucune question ne correspond.</p>';
    $('texte-q').value = texteQuestionnaire();
  }
  function copier(texte) {
    function repli() {
      var ta = $('texte-q'); ta.closest('details').open = true; ta.focus(); ta.select();
      var ok = false; try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
      return ok;
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(texte).then(function () { return true; }, function () { return repli(); });
    }
    return Promise.resolve(repli());
  }

  /* ---------- Infos ---------- */
  function rendreInfos() {
    var c = { verifie: 0, 'a-confirmer': 0, manquant: 0 };
    BASE.infos.forEach(function (x) { c[x.statut]++; });
    $('filtres-infos').innerHTML = '<div class="puces" role="group" aria-label="Filtrer par statut">' +
      '<button class="puce" type="button" data-puce="iStatut" data-val="" aria-pressed="' + (!filtres.iStatut) + '">Toutes<span class="n">' + BASE.infos.length + '</span></button>' +
      Object.keys(c).map(function (s) { return '<button class="puce" type="button" data-puce="iStatut" data-val="' + s + '" aria-pressed="' + (filtres.iStatut === s) + '">' + L.infos[s] + '<span class="n">' + c[s] + '</span></button>'; }).join('') + '</div>';
    var liste = filtreTexte(BASE.infos).filter(function (x) { return !filtres.iStatut || x.statut === filtres.iStatut; });
    var sections = []; liste.forEach(function (x) { if (sections.indexOf(x.section) === -1) sections.push(x.section); });
    $('infos').innerHTML = sections.map(function (s) {
      return '<section class="groupe"><h3>' + esc(s) + '</h3><table class="tableau"><thead><tr><th scope="col">Information</th><th scope="col">Ce qu\'on a</th><th scope="col">Statut</th><th scope="col">Où elle sert</th><th scope="col">Qui la fournit</th></tr></thead><tbody>' +
        liste.filter(function (x) { return x.section === s; }).map(function (x) {
          return '<tr><td class="td-titre">' + esc(x.info) + '</td><td data-l="Ce qu\'on a">' + (esc(x.valeur) || '<span class="sec">Rien</span>') +
            (x.source ? '<span class="sec">' + esc(x.source) + '</span>' : '') + (x.ecart ? '<span class="ecart">Écart : ' + esc(x.ecart) + '</span>' : '') + '</td>' +
            '<td data-l="Statut">' + badge('infos', x.statut) + '</td><td data-l="Où elle sert">' + esc(x.usage) + '</td><td data-l="Qui la fournit">' + esc(x.fournisseur) + '</td></tr>';
        }).join('') + '</tbody></table></section>';
    }).join('') || '<p class="vide">Aucune information ne correspond.</p>';
  }

  /* ---------- Assets ---------- */
  function rendreAssets() {
    $('filtres-assets').innerHTML = puces('aStatut', 'assets', BASE.assets);
    var liste = filtreTexte(BASE.assets).filter(function (x) { return !filtres.aStatut || statut('assets', x) === filtres.aStatut; })
      .sort(function (a, b) { return PRIO[a.priorite] - PRIO[b.priorite]; });
    $('assets').innerHTML = liste.length ? '<table class="tableau"><thead><tr><th scope="col">Asset</th><th scope="col">Détail</th><th scope="col">Sert à</th><th scope="col">Qui</th><th scope="col">Priorité</th><th scope="col">Statut</th></tr></thead><tbody>' +
      liste.map(function (x) {
        return '<tr><td class="td-titre">' + esc(x.asset) + '</td><td data-l="Détail">' + esc(x.detail) + '</td><td data-l="Sert à">' + esc(x.usage) + '</td><td data-l="Qui">' + esc(x.fournisseur) + '</td>' +
          '<td data-l="Priorité"><span class="prio' + (x.priorite === 'haute' ? ' prio--haute' : '') + '">' + esc(x.priorite) + '</span></td>' +
          '<td data-l="Statut" class="ligne-statut">' + selectStatut('assets', x, 'Statut de l\'asset ' + x.asset) + '</td></tr>';
      }).join('') + '</tbody></table>' : '<p class="vide">Aucun asset ne correspond.</p>';
  }

  /* ---------- Juridique ---------- */
  function rendreJuridique() {
    var liste = filtreTexte(BASE.juridique);
    $('juridique').innerHTML = liste.length ? '<table class="tableau"><thead><tr><th scope="col">Sujet</th><th scope="col">Base</th><th scope="col">Statut</th><th scope="col">Ce qu\'il reste à faire</th><th scope="col">Fichier</th></tr></thead><tbody>' +
      liste.map(function (x) {
        return '<tr><td class="td-titre">' + esc(x.sujet) + '</td><td data-l="Base">' + esc(x.base) + '</td><td data-l="Statut">' + badge('juridique', x.statut) + '</td>' +
          '<td data-l="Ce qu\'il reste à faire">' + esc(x.action) + '</td><td data-l="Fichier">' + lien(x.fichier, x.fichier.split('/').pop()) + '</td></tr>';
      }).join('') + '</tbody></table>' : '<p class="vide">Aucun point ne correspond.</p>';
  }

  /* ---------- Stratégie ---------- */
  function chf(n) { return 'CHF ' + String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '\''); }
  function rendreStrategie() {
    var S = BASE.strategie;
    var max = Math.max.apply(null, S.budgets.map(function (b) { return b.mensuel; }));
    var ymax = 60, ticks = [0, 20, 40, 60];
    var html = '<div class="strat-tete"><section class="bloc"><h3>Recommandation : combinaison C</h3><p>' + esc(S.recommandation) + '</p><p><b>Contrainte :</b> ' + esc(S.contrainte) + '</p>' +
      '<div class="liens-strat">' + S.liens.map(function (l) { return '<p>' + lien(l.chemin, l.titre) + '</p>'; }).join('') +
      '<p>Figma : ' + (S.figma ? lien(S.figma, 'maquettes Figma') : 'aucun lien dans le dépôt (docs/v4/figma.md absent). Ajoutez-le dans strategie.figma.') + '</p></div></section>' +
      '<section class="bloc"><h3>Repères</h3><dl class="reperes">' + S.reperes.map(function (r) { return '<div class="repere"><dt>' + esc(r.nom) + '</dt><dd>' + esc(r.valeur) + '</dd></div>'; }).join('') + '</dl></section></div>';

    html += '<div class="strat-graph"><section class="bloc"><h3>Budget mensuel par combinaison</h3><p class="bloc__aide">Dépense tout compris, valeurs centrales du plan de mix.</p><ul class="hbarres">' +
      S.budgets.map(function (b) {
        var tip = b.id + ', ' + b.nom + ' : ' + chf(b.mensuel) + ' par mois, ' + chf(b.annuel) + ' sur 12 mois' + (b.recommande ? ' (recommandée)' : '') + '.';
        return '<li class="hbarre' + (b.recommande ? ' hbarre--reco' : '') + '"><span class="hbarre__nom"><b>' + esc(b.id) + '</b> ' + esc(b.nom) + (b.recommande ? ' <span class="tag-reco">Recommandée</span>' : '') + '</span>' +
          '<span class="hbarre__piste" tabindex="0" data-tip="' + esc(tip) + '" aria-label="' + esc(tip) + '"><span class="hbarre__barre" style="width:calc((100% - 5.5rem) * ' + (b.mensuel / max).toFixed(3) + ')"></span>' +
          '<span class="hbarre__val">' + chf(b.mensuel) + '</span></span></li>';
      }).join('') + '</ul>' +
      '<details class="donnees"><summary>Données en tableau</summary><table class="tableau"><thead><tr><th scope="col">Combinaison</th><th scope="col">Par mois</th><th scope="col">Sur 12 mois</th></tr></thead><tbody>' +
      S.budgets.map(function (b) { return '<tr><td>' + esc(b.id + ', ' + b.nom) + '</td><td>' + chf(b.mensuel) + '</td><td>' + chf(b.annuel) + '</td></tr>'; }).join('') + '</tbody></table></details></section>';

    html += '<section class="bloc"><h3>Demandes par mois attendues (combinaison C)</h3><p class="bloc__aide">Barre : valeur centrale. Trait : fourchette basse à haute.</p>' +
      '<div class="colonnes-graph" role="img" aria-label="' + esc(S.objectifs.map(function (o) { return o.jalon + ' : ' + o.demandes + ' demandes (' + o.bas + ' à ' + o.haut + ')'; }).join(', ')) + '">' +
      '<div class="axe-y" aria-hidden="true">' + ticks.map(function (t) { return '<span style="bottom:' + (t / ymax * 100) + '%">' + t + '</span>'; }).join('') + '</div>' +
      '<div class="zone-graph">' + ticks.slice(1).map(function (t) { return '<span class="grille" style="bottom:' + (t / ymax * 100) + '%" aria-hidden="true"></span>'; }).join('') +
      S.objectifs.map(function (o) {
        var tip = o.jalon + ' : ' + String(o.demandes).replace('.', ',') + ' demandes par mois (' + String(o.bas).replace('.', ',') + ' à ' + String(o.haut).replace('.', ',') + '), ' + String(o.signes).replace('.', ',') + ' chantiers signés, objectif ' + o.avis + ' avis.';
        return '<div class="col-graph" tabindex="0" data-tip="' + esc(tip) + '"><span class="col-graph__barre" style="height:' + (o.demandes / ymax * 100) + '%"></span>' +
          '<span class="col-graph__plage" style="bottom:' + (o.bas / ymax * 100) + '%;height:' + ((o.haut - o.bas) / ymax * 100) + '%"></span>' +
          '<span class="col-graph__val" style="bottom:calc(' + (o.demandes / ymax * 100) + '% - .55rem)">' + String(o.demandes).replace('.', ',') + '</span></div>';
      }).join('') + '</div></div>' +
      '<div class="axe-x" aria-hidden="true">' + S.objectifs.map(function (o) { return '<span>' + esc(o.jalon) + '</span>'; }).join('') + '</div>' +
      '<details class="donnees"><summary>Données en tableau</summary><table class="tableau"><thead><tr><th scope="col">Jalon</th><th scope="col">Demandes/mois</th><th scope="col">Fourchette</th><th scope="col">Chantiers signés/mois</th><th scope="col">Avis visés</th></tr></thead><tbody>' +
      S.objectifs.map(function (o) { return '<tr><td>' + o.jalon + '</td><td>' + String(o.demandes).replace('.', ',') + '</td><td>' + String(o.bas).replace('.', ',') + ' à ' + String(o.haut).replace('.', ',') + '</td><td>' + String(o.signes).replace('.', ',') + '</td><td>' + o.avis + '</td></tr>'; }).join('') +
      '</tbody></table></details></section></div>';

    html += '<section class="bloc"><h3>Indicateurs suivis</h3><p class="bloc__aide">Mêmes noms et formules dans le simulateur, le plan et l\'admin.</p><ul class="kpis">' +
      S.kpi.map(function (k) { return '<li>' + esc(k) + '</li>'; }).join('') + '</ul></section>';
    $('strategie').innerHTML = html;
  }

  /* ---------- Livrables et journal ---------- */
  function rendreLivrables() {
    var liste = filtreTexte(BASE.livrables), groupes = [];
    liste.forEach(function (l) { if (groupes.indexOf(l.groupe) === -1) groupes.push(l.groupe); });
    $('livrables').innerHTML = groupes.map(function (g) {
      return '<section class="groupe"><h3>' + esc(g) + '</h3><div class="livrables">' + liste.filter(function (l) { return l.groupe === g; }).map(function (l) {
        return '<div class="livrable">' + lien(l.chemin, l.titre) + '<code>' + esc(l.chemin) + '</code>' + (l.note ? '<p>' + esc(l.note) + '</p>' : '') + '</div>';
      }).join('') + '</div></section>';
    }).join('') || '<p class="vide">Aucun livrable ne correspond.</p>';
  }
  function rendreJournal() {
    var liste = filtreTexte(BASE.journal).slice().sort(function (a, b) { return a.date < b.date ? 1 : a.date > b.date ? -1 : 0; });
    var plusRecent = liste.length ? liste[0].date : '';
    $('journal').innerHTML = liste.map(function (j) {
      return '<li' + (j.date === plusRecent ? ' class="recent"' : '') + '><time datetime="' + esc(j.date) + '">' + esc(dateFr(j.date)) + '</time><div><p>' + esc(j.titre) + '</p>' +
        (j.commit ? '<p class="commit">Commit ' + esc(j.commit) + '</p>' : '') + '</div></li>';
    }).join('') || '<li class="vide">Aucune entrée ne correspond.</li>';
  }

  /* ---------- Export ---------- */
  var ENTETE = (function () {
    return [
      '/* ==========================================================================',
      '   Pilotage du projet Andy Construct : données du tableau de bord',
      '   --------------------------------------------------------------------------',
      '   Fichier PRIVÉ (agence Harbor Digital et Claude). À modifier à la main dans',
      '   un éditeur, ou depuis le tableau de bord (bouton « Exporter donnees.js »).',
      '',
      '   Règles',
      '   - Un seul objet : window.PROJET. Pas de fetch : tout marche en file://.',
      '   - Garder des guillemets doubles et une virgule après chaque élément.',
      '   - Dates au format AAAA-MM-JJ. Laisser "" si inconnue.',
      '   - Chemins de fichiers relatifs à la racine du dépôt (ex. "docs/v4/seo/audit-seo.md").',
      '   - Aucun chiffre inventé : tout montant ou volume vient d\'un document cité.',
      '',
      '   Statuts autorisés',
      '   - taches.statut          : "a-faire" | "en-cours" | "attente-client" | "fait"',
      '   - taches.responsable     : "Agence" | "Claude" | "Client"',
      '   - taches.priorite        : "haute" | "moyenne" | "basse"',
      '   - decisions.statut       : "a-prendre" | "prise"',
      '   - decisions.reco         : rang de l\'option recommandée (0 = la première), -1 si aucune',
      '   - questionnaire.statut   : "a-envoyer" | "envoye" | "repondu"',
      '   - infos.statut           : "verifie" | "a-confirmer" | "manquant"',
      '   - assets.statut          : "a-demander" | "demande" | "recu"',
      '   - juridique.statut       : "pret" | "a-completer" | "a-faire" | "bloque"',
      '',
      '   Les échéances des tâches ouvertes sont des propositions de l\'agence, à ajuster.',
      '   ========================================================================== */',
      ''
    ].join('\n');
  })();
  function exporter() {
    var copie = JSON.parse(JSON.stringify(BASE));
    EDITABLES.forEach(function (k) { (copie[k] || []).forEach(function (it) { if (etat.modifs[k][it.id]) it.statut = etat.modifs[k][it.id]; }); });
    copie.meta.maj = aujourdhui();
    var contenu = ENTETE + '\nwindow.PROJET = ' + JSON.stringify(copie, null, 2) + ';\n';
    try {
      var blob = new Blob([contenu], { type: 'text/javascript;charset=utf-8' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = 'donnees.js';
      document.body.appendChild(a); a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
      etat.exporte = true; ecrire(); rendreLocal();
    } catch (e) {
      $('local-etat').textContent = 'Export impossible dans ce navigateur.';
    }
  }

  /* ---------- Rendu global ---------- */
  function rendreTout() {
    rendreMeta(); rendreLocal(); rendreNav();
    rendreApercu(); rendreTaches(); rendreDecisions(); rendreQuestionnaire(); rendreInfos(); rendreAssets(); rendreJuridique(); rendreStrategie(); rendreLivrables(); rendreJournal();
  }

  /* ---------- Thème ---------- */
  var THEMES = ['', 'light', 'dark'], NOMS_THEME = { '': 'système', light: 'clair', dark: 'sombre' };
  function appliquerTheme() {
    var t = etat.theme || '';
    if (t) document.documentElement.setAttribute('data-theme', t); else document.documentElement.removeAttribute('data-theme');
    $('theme').textContent = 'Thème : ' + NOMS_THEME[t];
  }

  /* ---------- Infobulle ---------- */
  var bulle = $('bulle');
  function montrerBulle(el, x, y) {
    bulle.textContent = el.getAttribute('data-tip'); bulle.hidden = false;
    var r = bulle.getBoundingClientRect();
    if (x == null) { var b = el.getBoundingClientRect(); x = b.left + b.width / 2; y = b.top; }
    var left = Math.min(Math.max(8, x - r.width / 2), window.innerWidth - r.width - 8);
    var top = y - r.height - 10; if (top < 8) top = y + 18;
    bulle.style.left = left + 'px'; bulle.style.top = top + 'px';
  }
  document.addEventListener('mousemove', function (ev) {
    var el = ev.target.closest && ev.target.closest('[data-tip]');
    if (el) montrerBulle(el, ev.clientX, ev.clientY); else if (!bulle.hidden && document.activeElement && !document.activeElement.hasAttribute('data-tip')) bulle.hidden = true;
  });
  document.addEventListener('focusin', function (ev) { var el = ev.target.closest('[data-tip]'); if (el) montrerBulle(el); else bulle.hidden = true; });
  document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') bulle.hidden = true; });
  window.addEventListener('scroll', function () { bulle.hidden = true; }, { passive: true });

  /* ---------- Événements ---------- */
  document.addEventListener('change', function (ev) {
    var t = ev.target;
    if (t.matches('select[data-type]')) { var id = t.id; changer(t.getAttribute('data-type'), t.getAttribute('data-id'), t.value); var n = $(id); if (n) n.focus(); }
    else if (t.matches('select[data-filtre]')) { filtres[t.getAttribute('data-filtre')] = t.value; var f = t.getAttribute('data-filtre'); rendreTaches(); var s = document.querySelector('select[data-filtre="' + f + '"]'); if (s) s.focus(); }
  });
  document.addEventListener('click', function (ev) {
    var p = ev.target.closest('[data-puce]');
    if (p) {
      var cle = p.getAttribute('data-puce'), val = p.getAttribute('data-val');
      filtres[cle] = val; rendreTout();
      var b = document.querySelector('[data-puce="' + cle + '"][data-val="' + val + '"]'); if (b) b.focus();
      return;
    }
    var c = ev.target.closest('[data-chantier]');
    if (c) { filtres.tChantier = c.getAttribute('data-chantier'); filtres.tResp = ''; filtres.tPrio = ''; location.hash = 'taches'; }
  });
  $('recherche').addEventListener('input', function (ev) { recherche = ev.target.value; rendreTout(); });
  $('exporter').addEventListener('click', exporter);
  $('annuler').addEventListener('click', function () {
    if (!window.confirm('Annuler toutes les modifications locales non exportées ?')) return;
    EDITABLES.forEach(function (k) { etat.modifs[k] = {}; }); etat.exporte = false; ecrire(); rendreTout();
  });
  $('theme').addEventListener('click', function () {
    etat.theme = THEMES[(THEMES.indexOf(etat.theme || '') + 1) % THEMES.length]; ecrire(); appliquerTheme();
  });
  $('copier-q').addEventListener('click', function () {
    var n = BASE.questionnaire.filter(function (q) { return statut('questionnaire', q) !== 'repondu'; }).length;
    copier(texteQuestionnaire()).then(function (ok) {
      $('retour-q').textContent = ok ? 'Questionnaire copié (' + n + ' questions). Collez-le dans votre e-mail.' : 'Copie bloquée par le navigateur : le texte est sélectionné ci-dessous, copiez-le à la main.';
    });
  });
  $('envoyer-q').addEventListener('click', function () {
    var n = 0;
    BASE.questionnaire.forEach(function (q) { if (statut('questionnaire', q) === 'a-envoyer') { if (q.statut === 'envoye') delete etat.modifs.questionnaire[q.id]; else etat.modifs.questionnaire[q.id] = 'envoye'; n++; } });
    etat.exporte = false; ecrire(); rendreTout();
    $('retour-q').textContent = n ? n + ' question' + (n > 1 ? 's' : '') + ' marquée' + (n > 1 ? 's' : '') + ' comme envoyée' + (n > 1 ? 's' : '') + '.' : 'Aucune question à envoyer.';
  });
  window.addEventListener('hashchange', function () {
    montrerVue(); rendreTaches();
    $('contenu').focus({ preventScroll: true }); window.scrollTo(0, 0);
  });

  appliquerTheme();
  rendreTout();
  montrerVue();
})();
