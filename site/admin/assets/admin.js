/* Gestion Andy Construct : comportements légers (le HTML fonctionne sans JavaScript).
   Aucune donnée personnelle n'est gardée dans le navigateur, sauf le brouillon de la
   saisie d'un appel dans la mémoire de l'onglet (sessionStorage, effacé à l'envoi). */
(function () {
  'use strict';
  document.documentElement.classList.add('js');

  function tous(sel, racine) { return Array.prototype.slice.call((racine || document).querySelectorAll(sel)); }
  function texte(el, t) { el.textContent = t; return el; }
  function creer(tag, classe, contenu) { var e = document.createElement(tag); if (classe) e.className = classe; if (contenu != null) e.textContent = contenu; return e; }

  document.addEventListener('DOMContentLoaded', function () {
    // Filtres : envoi automatique au changement d'une liste.
    tous('form[data-auto] select, form[data-auto] input[type="checkbox"]').forEach(function (el) {
      el.addEventListener('change', function () { el.form.submit(); });
    });

    // Définitions des indicateurs (bouton « ? »).
    tous('button.aide[aria-controls]').forEach(function (b) {
      b.addEventListener('click', function () {
        var d = document.getElementById(b.getAttribute('aria-controls'));
        if (!d) return;
        var ouvert = b.getAttribute('aria-expanded') === 'true';
        b.setAttribute('aria-expanded', ouvert ? 'false' : 'true');
        d.hidden = ouvert;
      });
    });

    // Colonnes sur téléphone : une étape à la fois (onglets).
    var onglets = tous('.onglets-colonnes [role="tab"]');
    function activer(tab, focus) {
      onglets.forEach(function (t) {
        var actif = t === tab;
        t.setAttribute('aria-selected', actif ? 'true' : 'false');
        t.tabIndex = actif ? 0 : -1;
        var p = document.getElementById(t.getAttribute('aria-controls'));
        if (p) p.classList.toggle('active', actif);
      });
      if (focus) tab.focus();
    }
    onglets.forEach(function (t, i) {
      t.addEventListener('click', function () { activer(t, false); });
      t.addEventListener('keydown', function (ev) {
        if (ev.key === 'ArrowRight' || ev.key === 'ArrowLeft') {
          ev.preventDefault();
          activer(onglets[(i + (ev.key === 'ArrowRight' ? 1 : onglets.length - 1)) % onglets.length], true);
        }
      });
    });

    // Un seul menu « Résultat » ouvert à la fois ; Échap le ferme.
    document.addEventListener('click', function (ev) {
      tous('details.menu-resultat[open]').forEach(function (d) { if (!d.contains(ev.target)) d.open = false; });
    });
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') tous('details.menu-resultat[open]').forEach(function (d) { d.open = false; d.querySelector('summary').focus(); });
    });

    // Après un appel (lien tel:), la feuille « Résultat de l'appel » s'ouvre au retour dans l'onglet.
    var feuille = document.getElementById('feuille-appel');
    tous('a[data-appel]').forEach(function (a) {
      a.addEventListener('click', function () {
        try { sessionStorage.setItem('ac-appel', JSON.stringify({ ref: a.getAttribute('data-appel'), t: Date.now() })); } catch (e) { /* mémoire indisponible */ }
      });
    });
    function ouvrirFeuille() {
      var appel = null;
      try { appel = JSON.parse(sessionStorage.getItem('ac-appel') || 'null'); sessionStorage.removeItem('ac-appel'); } catch (e) { appel = null; }
      if (!appel || Date.now() - appel.t > 2 * 3600 * 1000) return;
      var menu = document.querySelector('details.menu-resultat[data-ref="' + String(appel.ref).replace(/[^A-Z0-9-]/g, '') + '"]');
      if (feuille && menu && typeof feuille.showModal === 'function') {
        var choix = document.getElementById('feuille-appel-choix');
        choix.textContent = '';
        tous('.menu-resultat-corps > *', menu).forEach(function (n) { choix.appendChild(n.cloneNode(true)); });
        tous('.btn', choix).forEach(function (b) { b.classList.remove('btn-petit'); });
        texte(document.getElementById('feuille-appel-qui'), appel.ref);
        feuille.showModal();
      } else if (document.getElementById('t-actions')) {
        document.getElementById('t-actions').scrollIntoView();
      }
    }
    document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'visible') ouvrirFeuille(); });
    tous('dialog [data-fermer]').forEach(function (b) { b.addEventListener('click', function () { b.closest('dialog').close(); }); });

    // Saisie d'un appel : brouillon dans l'onglet et score calculé par le serveur pendant la saisie.
    var form = document.getElementById('form-saisie');
    if (form) {
      var cle = 'ac-brouillon-' + form.getAttribute('data-brouillon');
      var champs = tous('input:not([type="hidden"]), select, textarea', form);
      try {
        var brouillon = JSON.parse(sessionStorage.getItem(cle) || 'null');
        var vierge = champs.every(function (c) { return (c.type === 'checkbox' || c.type === 'radio') ? !c.checked : !c.value || c.tagName === 'SELECT' && c.selectedIndex === 0 || c.id === 's-canal'; });
        if (brouillon && vierge) {
          champs.forEach(function (c) {
            var v = brouillon[c.name];
            if (v == null) return;
            if (c.type === 'checkbox' || c.type === 'radio') c.checked = [].concat(v).indexOf(c.value) >= 0;
            else c.value = v;
          });
        }
      } catch (e) { /* mémoire indisponible */ }
      var minuterie = null;
      var zone = document.getElementById('s-score');
      var doublon = document.getElementById('s-doublon');
      function sauver() {
        var o = {};
        champs.forEach(function (c) {
          if (c.type === 'checkbox') { if (c.checked) (o[c.name] = o[c.name] || []).push(c.value); }
          else if (c.type === 'radio') { if (c.checked) o[c.name] = c.value; }
          else o[c.name] = c.value;
        });
        try { sessionStorage.setItem(cle, JSON.stringify(o)); } catch (e) { /* rien */ }
      }
      function afficher(r) {
        zone.textContent = '';
        var tete = creer('div', 'score-gros');
        var p = creer('span', 'prio ' + (r.priorite === 'hors-cible' ? 'prio-HC' : 'prio-' + r.priorite), r.priorite === 'hors-cible' ? 'Hors cible' : r.priorite);
        tete.appendChild(p);
        tete.appendChild(creer('span', 'gros', String(r.score)));
        tete.appendChild(creer('span', 'discret', 'points'));
        zone.appendChild(tete);
        var ech = creer('p', 'mt petit', 'Échéance si le contact n’est pas établi maintenant : ' + r.echeance + '. ' + (r.zone && r.zone !== 'inconnue' ? 'Zone ' + r.zone + (r.npa ? ' (NPA ' + r.npa + ').' : '.') : 'Indiquez le NPA pour la zone.'));
        zone.appendChild(ech);
        var t = creer('table', 'tableau mt');
        var cap = creer('caption', 'sr', 'Détail du score'); t.appendChild(cap);
        var tb = document.createElement('tbody');
        r.detail.forEach(function (l) {
          var tr = document.createElement('tr');
          var th = creer('th', '', l.critere); th.scope = 'row';
          tr.appendChild(th); tr.appendChild(creer('td', '', l.valeur)); tr.appendChild(creer('td', 'num', String(l.points)));
          tb.appendChild(tr);
        });
        t.appendChild(tb); zone.appendChild(t);
        if (r.regles && r.regles.length) zone.appendChild(creer('p', 'petit', r.regles.join(' ; ')));
        if (doublon) texte(doublon, r.existant ? 'Contact existant : ' + (r.existant.nom || 'sans nom') + ' (' + r.existant.ref + '). La nouvelle demande lui sera rattachée.' : 'En premier : on retrouve un contact existant.');
      }
      function calculer() {
        var fd = new FormData(form);
        fetch(form.getAttribute('data-score'), { method: 'POST', body: fd, credentials: 'same-origin', headers: { Accept: 'application/json' } })
          .then(function (rep) { return rep.ok ? rep.json() : null; })
          .then(function (r) { if (r && r.ok) afficher(r); })
          .catch(function () { /* hors connexion : le serveur calcule à l'enregistrement */ });
      }
      form.addEventListener('input', function () { sauver(); clearTimeout(minuterie); minuterie = setTimeout(calculer, 250); });
      form.addEventListener('change', function () { sauver(); clearTimeout(minuterie); minuterie = setTimeout(calculer, 100); });
      form.addEventListener('submit', function () { try { sessionStorage.removeItem(cle); } catch (e) { /* rien */ } });
      calculer();
    }
  });
})();
