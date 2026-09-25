/* Andy Construct : scripts du site (vanilla, sans dépendance). */
(function () {
  'use strict';
  var d = document;
  var root = d.documentElement;
  root.classList.remove('no-js');
  root.classList.add('js');

  function each(sel, fn, ctx) { Array.prototype.forEach.call((ctx || d).querySelectorAll(sel), fn); }

  /* 1. Bandeau « maquette » : fermable, mémorisé le temps de la session.
        Pour le supprimer en production : retirer le bloc .mockup-notice des pages. */
  var notice = d.querySelector('.mockup-notice');
  if (notice) {
    var KEY = 'ac-maquette-masquee';
    var hide = false;
    try { hide = sessionStorage.getItem(KEY) === '1'; } catch (e) {}
    if (hide) {
      notice.remove();
    } else {
      var close = notice.querySelector('.mockup-notice__close');
      if (close) {
        close.addEventListener('click', function () {
          notice.remove();
          try { sessionStorage.setItem(KEY, '1'); } catch (e) {}
          var main = d.getElementById('contenu');
          if (main) { main.setAttribute('tabindex', '-1'); main.focus({ preventScroll: true }); }
        });
      }
    }
  }

  /* 2. Menu principal (mobile et tablette) */
  var toggle = d.querySelector('.nav-toggle');
  var nav = d.getElementById('menu-principal');
  if (toggle && nav) {
    var label = toggle.querySelector('.nav-toggle__label');
    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      nav.classList.toggle('is-open', open);
      root.classList.toggle('menu-open', open);
      if (label) label.textContent = open ? 'Fermer' : 'Menu';
    };
    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    d.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        toggle.focus();
      }
    });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    d.addEventListener('click', function (e) {
      if (nav.classList.contains('is-open') && !nav.contains(e.target) && !toggle.contains(e.target)) setOpen(false);
    });
    var mq = window.matchMedia('(min-width: 1240px)');
    var onMq = function () { if (mq.matches) setOpen(false); };
    if (mq.addEventListener) mq.addEventListener('change', onMq); else if (mq.addListener) mq.addListener(onMq);
  }

  /* 3. Formulaire de demande de devis (maquette : aucun envoi réel)
        BRANCHEMENT EN PRODUCTION : remplacer le bloc « Confirmation » ci-dessous par
          fetch(form.action, { method: 'POST', body: new FormData(form) })
        vers un script d'envoi hébergé en Suisse (ex. PHP mail() chez l'hébergeur),
        puis afficher la confirmation seulement si la réponse est positive (res.ok). */
  var params = new URLSearchParams(window.location.search);
  each('form[data-devis]', function (form) {
    form.noValidate = true; // validation HTML5 conservée, messages affichés dans la page
    var type = params.get('travaux');
    var select = form.querySelector('select[name="travaux"]');
    if (type && select && select.querySelector('option[value="' + type + '"]')) select.value = type;

    var showError = function (field) {
      var box = field.closest('.field');
      var err = box && box.querySelector('.error');
      if (!err) return;
      var msg = '';
      if (!field.validity.valid) {
        if (field.validity.valueMissing) msg = field.getAttribute('data-requis') || 'Ce champ est obligatoire.';
        else if (field.validity.typeMismatch) msg = 'Vérifiez le format de l’adresse e-mail (exemple : nom@domaine.ch).';
        else if (field.validity.patternMismatch) msg = field.getAttribute('data-format') || 'Le format saisi n’est pas valide.';
        else msg = field.validationMessage;
      }
      err.textContent = msg;
      err.hidden = !msg;
      box.classList.toggle('has-error', !!msg);
      field.setAttribute('aria-invalid', msg ? 'true' : 'false');
    };

    each('input, select, textarea', function (field) {
      field.addEventListener('blur', function () { if (field.value || field.closest('.has-error')) showError(field); });
      field.addEventListener('input', function () { if (field.closest('.has-error')) showError(field); });
    }, form);

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var first = null;
      each('input, select, textarea', function (field) {
        showError(field);
        if (!first && !field.validity.valid) first = field;
      }, form);
      if (first) { first.focus(); return; }

      /* Confirmation (maquette) */
      var ok = form.parentNode.querySelector('.form-success');
      var name = form.querySelector('[name="nom"]');
      var who = ok && ok.querySelector('[data-nom]');
      if (who && name) who.textContent = name.value.trim().split(/\s+/)[0] || '';
      form.hidden = true;
      if (ok) { ok.hidden = false; ok.focus(); }
    });
  });

  /* 4. Galerie : filtres par catégorie */
  var gallery = d.querySelector('[data-gallery]');
  var status = d.querySelector('.gallery-status');
  var filterBtns = d.querySelectorAll('[data-filter]');
  var applyFilter = function (cat, btn) {
    var n = 0;
    each('[data-filter]', function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
    each('[data-cat]', function (item) {
      var show = cat === 'toutes' || item.getAttribute('data-cat') === cat;
      item.hidden = !show;
      if (show) n++;
    }, gallery);
    if (status) status.textContent = n + (n > 1 ? ' photos affichées' : ' photo affichée') + (cat === 'toutes' ? '' : ' – ' + btn.getAttribute('data-label'));
  };
  if (gallery && filterBtns.length) {
    each('[data-filter]', function (b) {
      b.addEventListener('click', function () { applyFilter(b.getAttribute('data-filter'), b); });
    });
    var wanted = params.get('categorie');
    var pre = wanted && d.querySelector('[data-filter="' + wanted + '"]');
    if (pre) applyFilter(wanted, pre);
  }

  /* 5. Visionneuse accessible (<dialog>) : flèches, Échap, focus piégé, légende */
  var dlg = d.getElementById('visionneuse');
  if (gallery && dlg && typeof dlg.showModal === 'function') {
    var img = dlg.querySelector('img');
    var source = dlg.querySelector('source');
    var title = dlg.querySelector('.lightbox__caption b');
    var sub = dlg.querySelector('.lightbox__caption span');
    var count = dlg.querySelector('.lightbox__count');
    var list = [];
    var cur = 0;
    var opener = null;

    var visible = function () {
      return Array.prototype.filter.call(gallery.querySelectorAll('.gallery__btn'), function (b) { return !b.closest('[hidden]'); });
    };
    var show = function (i) {
      if (!list.length) return;
      cur = (i + list.length) % list.length;
      var b = list[cur];
      var thumb = b.querySelector('img');
      img.removeAttribute('src');
      if (source) source.srcset = b.getAttribute('data-webp') || '';
      img.width = +b.getAttribute('data-w') || 1600;
      img.height = +b.getAttribute('data-h') || 1200;
      img.src = b.getAttribute('data-jpg') || (thumb && thumb.currentSrc) || '';
      img.alt = thumb ? thumb.alt : '';
      title.textContent = b.getAttribute('data-title') || '';
      sub.textContent = b.getAttribute('data-label') || '';
      count.textContent = 'Photo ' + (cur + 1) + ' sur ' + list.length;
    };

    gallery.addEventListener('click', function (e) {
      var b = e.target.closest('.gallery__btn');
      if (!b) return;
      opener = b;
      list = visible();
      show(list.indexOf(b));
      dlg.showModal();
      root.style.overflow = 'hidden';
      dlg.querySelector('[data-lb="close"]').focus();
    });
    dlg.addEventListener('click', function (e) {
      var act = e.target.closest('[data-lb]');
      if (act) {
        var a = act.getAttribute('data-lb');
        if (a === 'close') dlg.close();
        else show(cur + (a === 'next' ? 1 : -1));
      } else if (e.target === dlg) {
        dlg.close();
      }
    });
    dlg.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); show(cur + 1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); show(cur - 1); }
      else if (e.key === 'Tab') {
        var f = dlg.querySelectorAll('button');
        var firstB = f[0];
        var lastB = f[f.length - 1];
        if (e.shiftKey && d.activeElement === firstB) { e.preventDefault(); lastB.focus(); }
        else if (!e.shiftKey && d.activeElement === lastB) { e.preventDefault(); firstB.focus(); }
      }
    });
    dlg.addEventListener('close', function () {
      root.style.overflow = '';
      if (opener) opener.focus();
    });
  }

  /* 6. Prestations : repère de la section en cours dans le sommaire */
  var toc = d.querySelectorAll('.toc a[href^="#"]');
  if (toc.length && 'IntersectionObserver' in window) {
    var links = {};
    each('.toc a[href^="#"]', function (a) { links[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && links[en.target.id]) {
          each('.toc a.is-active', function (a) { a.classList.remove('is-active'); a.removeAttribute('aria-current'); });
          links[en.target.id].classList.add('is-active');
          links[en.target.id].setAttribute('aria-current', 'true');
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    Object.keys(links).forEach(function (id) { var s = d.getElementById(id); if (s) io.observe(s); });
  }
})();
