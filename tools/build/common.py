# -*- coding: utf-8 -*-
"""Gabarits communs du site Andy Construct (en-tête, pied de page, <head>, images, NAP)."""
import json, html, os

# Racine du dépôt = deux niveaux au-dessus de ce fichier (tools/build/common.py)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = os.path.join(ROOT, 'site')
PROD = 'https://www.andyconstruct.ch/'

# ---------------------------------------------------------------- NAP unique (brief SEO §1 + décisions du chef de projet)
NAME = 'Andy Construct'
LEGAL = 'Andy Construct, Chanton & Cie'
STREET = 'Route des Acacias 48'
CITY = '1227 Carouge (Genève)'
TEL = '+41 22 771 20 15'
TEL_URI = 'tel:+41227712015'
MOB = '+41 78 631 14 34'
MOB_URI = 'tel:+41786311434'
MAIL = 'andy.construct@bluewin.ch'
HOURS = 'Du lundi au vendredi, 7 h 00 – 18 h 00'
IDE = 'CHE-113.706.162'
FB = 'https://www.facebook.com/andyconstruct.bajrami'
MAPS = 'https://www.google.com/maps/search/?api=1&amp;query=Route+des+Acacias+48%2C+1227+Carouge'

e = lambda s: html.escape(s, quote=True)

P_ADDR = '<!-- PROVISOIRE : à valider avec le client (siège de Carouge retenu d\'après le registre du commerce, ancienne adresse Chêne-Bourg ; horaires relevés sur local.ch ; e-mail sur domaine recommandé) -->'

# ---------------------------------------------------------------- photos
MANIFEST_PATH = os.path.join(SITE, 'assets/img/portfolio/manifest.json')
MANIFEST = json.load(open(MANIFEST_PATH, encoding='utf-8')) if os.path.exists(MANIFEST_PATH) else []
BY = {m['id']: m for m in MANIFEST}

CAT = {
    'plafonds-tendus': 'Plafonds tendus',
    'plafonds-acoustiques': 'Acoustique',
    'plafonds-placo': 'Plafonds en plâtre',
    'plafonds-metalliques': 'Plafonds métalliques',
    'cloisons': 'Cloisons',
    'chantier': 'Chantiers en cours',
}


def pic(pid, sizes, eager=False, pos=None, hero=False):
    """<picture> webp (800/1600[/2400]) + repli jpg, largeur/hauteur, lazy sauf héro."""
    it = BY.get(pid)
    if not it:
        return '<!-- ATTENTE-PHOTOS : %s --><span class="ph">Photo à venir</span>' % e(pid)
    b = it['base']
    w16, h16 = it['largeur_1600'], it['hauteur_1600']
    srcset = '%s-800.webp %dw, %s-1600.webp %dw' % (b, it['largeur_800'], b, w16)
    w, h = w16, h16
    if hero and it.get('largeur_2400'):
        srcset += ', %s-2400.webp %dw' % (b, it['largeur_2400'])
        w, h = it['largeur_2400'], it['hauteur_2400']
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    style = ' style="object-position:%s"' % pos if pos else ''
    return ('<picture><source type="image/webp" srcset="%s" sizes="%s">'
            '<img src="%s-800.jpg" width="%d" height="%d" alt="%s" %s decoding="async"%s></picture>'
            % (srcset, sizes, b, w, h, e(it['alt']), load, style))


def hero_preload(pid):
    it = BY.get(pid)
    if not it:
        return ''
    b = it['base']
    return ('  <link rel="preload" as="image" type="image/webp" fetchpriority="high" '
            'imagesrcset="%s-800.webp 800w, %s-1600.webp 1600w, %s-2400.webp 2400w" imagesizes="100vw">\n' % (b, b, b))


# ---------------------------------------------------------------- JSON-LD (brief SEO §6)
def _offer(name, anchor):
    return {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': name, 'url': PROD + 'prestations.html#' + anchor}}


BUSINESS = {
    '@type': 'HomeAndConstructionBusiness',
    '@id': PROD + '#entreprise',
    'name': NAME,
    'legalName': LEGAL,
    'slogan': 'Plafonds · Cloisons · Peinture',
    'description': "Entreprise genevoise spécialisée dans la pose de faux-plafonds (tendus, acoustiques, en plaques de plâtre, en fibre ou métalliques), de cloisons légères et mobiles, d'isolation thermique et phonique, ainsi que dans la peinture intérieure. Intervient dans le canton de Genève et dans l'ouest vaudois pour particuliers, régies, architectes, entreprises et collectivités.",
    'url': PROD,
    'logo': PROD + 'assets/img/brand/logo-andy-construct.png',
    'image': [PROD + 'assets/img/portfolio/plafond-tendu-ilots-lumineux-01-1600.webp',
              PROD + 'assets/img/portfolio/plafond-lumineux-circulaire-01-1600.webp',
              PROD + 'assets/img/portfolio/chantier-ossature-puits-de-lumiere-01-1600.webp'],
    'telephone': TEL,
    'email': MAIL,
    'foundingDate': '2007',
    'identifier': {'@type': 'PropertyValue', 'propertyID': 'IDE', 'value': IDE},
    'address': {'@type': 'PostalAddress', 'streetAddress': STREET, 'postalCode': '1227',
                'addressLocality': 'Carouge', 'addressRegion': 'GE', 'addressCountry': 'CH'},
    'geo': {'@type': 'GeoCoordinates', 'latitude': 46.18935, 'longitude': 6.13236},
    'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification',
                                   'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                                   'opens': '07:00', 'closes': '18:00'}],
    'contactPoint': [
        {'@type': 'ContactPoint', 'telephone': TEL, 'contactType': 'customer service', 'areaServed': 'CH', 'availableLanguage': ['fr']},
        {'@type': 'ContactPoint', 'telephone': MOB, 'contactType': 'sales', 'areaServed': 'CH', 'availableLanguage': ['fr']},
    ],
    'areaServed': [
        {'@type': 'AdministrativeArea', 'name': 'Canton de Genève'},
        {'@type': 'City', 'name': 'Carouge'}, {'@type': 'City', 'name': 'Genève'},
        {'@type': 'City', 'name': 'Chêne-Bourg'}, {'@type': 'City', 'name': 'Collonge-Bellerive'},
        {'@type': 'City', 'name': 'Plan-les-Ouates'}, {'@type': 'AdministrativeArea', 'name': 'District de Nyon'},
        {'@type': 'City', 'name': 'Nyon'}, {'@type': 'City', 'name': 'Coppet'}, {'@type': 'City', 'name': 'Chavannes-de-Bogis'},
    ],
    'knowsAbout': ['Faux-plafonds', 'Plafonds en tissu tendu à froid', 'Plafonds acoustiques et phoniques',
                   'Plafonds en plaques de plâtre', 'Plafonds en fibre de bois et fibre minérale', 'Plafonds en bacs métalliques',
                   'Cadres acoustiques', 'Cloisons légères en plaques de plâtre', 'Cloisons mobiles en aluminium',
                   'Isolation thermique intérieure', 'Isolation phonique', 'Chape flottante', 'Protection incendie', 'Peinture intérieure'],
    'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Prestations Andy Construct', 'itemListElement': [
        {'@type': 'OfferCatalog', 'name': 'Plafonds', 'itemListElement': [
            _offer('Plafonds en tissu tendu à froid', 'plafonds-tendus'),
            _offer('Plafonds phoniques et acoustiques', 'plafonds-acoustiques'),
            _offer('Plafonds en plaques de plâtre', 'plafonds-placoplatre'),
            _offer('Plafonds en fibre de bois et fibre minérale', 'plafonds-fibre'),
            _offer('Plafonds en bacs métalliques', 'plafonds-metalliques'),
            _offer('Cadres acoustiques', 'cadres-acoustiques')]},
        {'@type': 'OfferCatalog', 'name': 'Cloisons', 'itemListElement': [
            _offer('Cloisons légères en plaques de plâtre', 'cloisons-placoplatre'),
            _offer('Cloisons mobiles en aluminium', 'cloisons-mobiles')]},
        {'@type': 'OfferCatalog', 'name': 'Isolation, acoustique et sécurité', 'itemListElement': [
            _offer('Isolation thermique et phonique', 'isolation'),
            _offer("Chape flottante contre les bruits d'impact", 'chape-flottante'),
            _offer('Protection incendie', 'protection-incendie'),
            _offer('Caissons lumineux, trappes de visite et puits de lumière', 'integrations')]},
        {'@type': 'OfferCatalog', 'name': 'Peinture', 'itemListElement': [_offer('Peinture intérieure', 'peinture')]},
    ]},
    'sameAs': [FB,
               'https://www.local.ch/fr/d/carouge-ge/1227/revetement-des-plafonds-et-plafonds-suspendus/andy-construct-chanton-cie-OGrZ5DP4atJqYki9WoTjPg',
               'https://search.ch/tel/chene-bourg/avenue-de-bel-air-57/andy-construct-chanton-cie'],
}


def jsonld(obj, note=''):
    c = ('  <!-- %s -->\n' % note) if note else ''
    return (c + '  <script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2).replace('</', '<\\/')
            + '\n  </script>\n')


def page_ld(file, name, crumb, page_type='WebPage'):
    """JSON-LD minimal des pages secondaires : WebPage (ou ContactPage) + fil d'Ariane, renvoi à l'entité de l'accueil."""
    url = PROD + file
    return {'@context': 'https://schema.org', '@graph': [
        {'@type': page_type, '@id': url + '#page', 'url': url, 'name': name, 'inLanguage': 'fr-CH',
         'isPartOf': {'@id': PROD + '#site'}, 'about': {'@id': PROD + '#entreprise'},
         'publisher': {'@id': PROD + '#entreprise'}, 'breadcrumb': {'@id': url + '#fil'}},
        {'@type': 'BreadcrumbList', '@id': url + '#fil', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Accueil', 'item': PROD},
            {'@type': 'ListItem', 'position': 2, 'name': crumb, 'item': url}]},
    ]}


# ---------------------------------------------------------------- <head>
EARLY_JS = ("<script>(function(d){d.className='js';try{if(sessionStorage.getItem('ac-maquette-masquee')==='1')"
            "d.classList.add('notice-off')}catch(e){}})(document.documentElement);</script>")


def head(title, desc, file, ld=(), preload='', canonical=True):
    url = PROD + ('' if file == 'index.html' else file)
    out = ['<!DOCTYPE html>\n<!-- Généré par tools/build — modifier les sources, pas ce fichier -->\n<html lang="fr-CH" class="no-js">\n<head>\n',
           '  <meta charset="utf-8">\n',
           '  <meta name="viewport" content="width=device-width, initial-scale=1">\n',
           '  <title>%s</title>\n' % e(title),
           '  <meta name="description" content="%s">\n' % e(desc),
           '  <!-- Maquette hébergée sur harbor-digital.fr : retirer en production -->\n',
           '  <meta name="robots" content="noindex, nofollow">\n']
    if canonical:
        out.append('  <link rel="canonical" href="%s">\n' % url)
    out += ['  <meta name="theme-color" content="#1D1F22">\n',
            '  <meta property="og:type" content="website">\n',
            '  <meta property="og:locale" content="fr_CH">\n',
            '  <meta property="og:site_name" content="Andy Construct">\n',
            '  <meta property="og:title" content="%s">\n' % e(title),
            '  <meta property="og:description" content="%s">\n' % e(desc),
            '  <meta property="og:url" content="%s">\n' % url,
            '  <meta property="og:image" content="%sassets/img/og-andy-construct.jpg">\n' % PROD,
            '  <meta property="og:image:width" content="1200">\n',
            '  <meta property="og:image:height" content="630">\n',
            '  <meta property="og:image:alt" content="Plafond tendu et îlots suspendus lumineux posés par Andy Construct">\n',
            '  <meta name="twitter:card" content="summary_large_image">\n',
            '  <link rel="icon" href="favicon.ico" sizes="any">\n',
            '  <link rel="icon" type="image/png" sizes="32x32" href="assets/img/brand/favicon-32.png">\n',
            '  <link rel="apple-touch-icon" href="assets/img/brand/apple-touch-icon.png">\n',
            '  <link rel="manifest" href="site.webmanifest">\n',
            '  <link rel="preload" href="assets/fonts/source-sans-3-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>\n',
            '  <link rel="preload" href="assets/fonts/montserrat-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>\n',
            preload,
            '  <link rel="stylesheet" href="assets/css/styles.css">\n',
            '  ' + EARLY_JS + '\n',
            '  <script src="assets/js/main.js" defer></script>\n']
    for item in ld:
        obj, note = item if isinstance(item, tuple) else (item, '')
        out.append(jsonld(obj, note))
    out.append('</head>\n')
    return ''.join(out)


# ---------------------------------------------------------------- en-tête
NAV = [('prestations.html', 'Prestations'), ('realisations.html', 'Réalisations'),
       ('index.html#entreprise', "L'entreprise"), ('contact.html', 'Contact')]

ICON_PHONE = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.75">'
              '<path d="M6.5 3h3l1.5 4.5-2 1.5a11 11 0 0 0 6 6l1.5-2 4.5 1.5v3a2 2 0 0 1-2 2A17 17 0 0 1 4.5 5a2 2 0 0 1 2-2z"/></svg>')


def header(active, devis='contact.html#devis'):
    items = ''.join('          <li><a href="%s"%s>%s</a></li>\n' % (h, ' aria-current="page"' if h == active else '', l)
                    for h, l in NAV)
    return '''<body>
  <a class="skip-link" href="#contenu">Aller au contenu</a>

  <!-- BANDEAU MAQUETTE : à supprimer en production (bloc .mockup-notice entier) -->
  <div class="mockup-notice" role="region" aria-label="Information sur la maquette">
    <div class="container mockup-notice__inner">
      <p>Maquette de présentation — certains contenus (chiffres, témoignages) sont provisoires.</p>
      <button type="button" class="mockup-notice__close">Masquer<span class="visually-hidden"> ce message</span></button>
    </div>
  </div>

  <header class="site-header">
    <div class="container site-header__inner">
      <a class="brand" href="index.html">
        <picture><source type="image/webp" srcset="assets/img/brand/logo-andy-construct.webp"><img src="assets/img/brand/logo-andy-construct.png" width="640" height="232" alt="Andy Construct, page d'accueil"></picture>
      </a>
      <nav class="site-nav" id="menu-principal" aria-label="Navigation principale">
        <ul>
%(items)s          <li class="nav-extra"><a class="btn" href="%(devis)s">Demander un devis</a></li>
          <li class="nav-extra"><a class="btn btn--ghost" href="%(tel_uri)s">Appeler le %(tel)s</a></li>
        </ul>
      </nav>
      <a class="header-phone" href="%(tel_uri)s"><small>Appelez-nous</small><span>%(tel)s</span></a>
      <a class="btn header-cta" href="%(devis)s">Demander un devis</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu-principal">
        <span class="nav-toggle__icon" aria-hidden="true"><span></span></span><span class="nav-toggle__label">Menu</span>
      </button>
    </div>
  </header>
''' % dict(items=items, devis=devis, tel_uri=TEL_URI, tel=TEL)


def nap(cls='nap'):
    """Bloc NAP identique partout (brief SEO §1)."""
    return '''<address class="%(cls)s">
          <strong>%(name)s</strong><br>
          %(street)s<br>
          %(city)s<br>
          Tél. <a href="%(tel_uri)s">%(tel)s</a><br>
          Mobile <a href="%(mob_uri)s">%(mob)s</a><br>
          <a href="mailto:%(mail)s">%(mail)s</a><br>
          %(hours)s
        </address>''' % dict(cls=cls, name=NAME, street=STREET, city=CITY, tel_uri=TEL_URI, tel=TEL,
                             mob_uri=MOB_URI, mob=MOB, mail=MAIL, hours=HOURS)


# ---------------------------------------------------------------- pied de page
def footer(devis='contact.html#devis', joined=False):
    return '''
  <footer class="site-footer on-dark%(joined)s">
    <div class="container footer-top">
      <div class="footer-brand">
        <picture><source type="image/webp" srcset="assets/img/brand/logo-andy-construct-blanc.webp"><img src="assets/img/brand/logo-andy-construct-blanc.png" width="640" height="232" alt="Andy Construct" loading="lazy"></picture>
        <!-- PROVISOIRE : à confirmer avec le client (inscription au registre du commerce depuis 2007) -->
        <p>Plafonds · Cloisons · Peinture. Entreprise genevoise depuis 2007, active dans tout le canton et dans l'ouest vaudois.</p>
      </div>
      <div>
        <h2>Coordonnées</h2>
        %(p_addr)s
        %(nap)s
      </div>
      <nav aria-label="Plan du site">
        <h2>Plan du site</h2>
        <ul>
          <li><a href="index.html">Accueil</a></li>
          <li><a href="prestations.html">Prestations</a></li>
          <li><a href="realisations.html">Réalisations</a></li>
          <li><a href="index.html#entreprise">L'entreprise</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </nav>
      <div>
        <h2>Nous trouver</h2>
        <ul>
          <li><a href="%(maps)s" rel="noopener">Voir sur la carte</a></li>
          <li><a href="%(fb)s" rel="noopener">Facebook</a></li>
          <li><a href="%(devis)s">Demander un devis</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="container">
        <!-- PROVISOIRE : à valider avec le client (raison sociale et IDE relevés au registre du commerce) -->
        <p>© 2026 %(legal)s · <span class="nowrap">IDE %(ide)s</span></p>
        <ul>
          <li><a href="mentions-legales.html">Mentions légales</a></li>
          <li><a href="mentions-legales.html#donnees">Protection des données</a></li>
        </ul>
      </div>
    </div>
  </footer>

  <div class="callbar" role="region" aria-label="Contact rapide">
    <a class="btn btn--ghost" href="%(tel_uri)s">%(icon)s Appeler</a>
    <!-- PROVISOIRE : « Devis gratuit » à confirmer avec le client -->
    <a class="btn" href="%(devis)s">Devis gratuit</a>
  </div>
</body>
</html>
''' % dict(joined=' site-footer--joined' if joined else '', p_addr=P_ADDR, nap=nap(), maps=MAPS, fb=FB, devis=devis,
           legal=LEGAL, ide=IDE, tel_uri=TEL_URI, icon=ICON_PHONE)


def page_head(crumb, h1, lead, aside=''):
    """En-tête des pages secondaires : fil d'Ariane, H1, chapeau."""
    side = ('        <div class="page-head__aside">%s</div>\n' % aside) if aside else ''
    return '''    <section class="page-head%s" aria-labelledby="titre-page">
      <div class="container">
        <div>
          <nav class="breadcrumb" aria-label="Fil d'Ariane">
            <ol>
              <li><a href="index.html">Accueil</a></li>
              <li aria-current="page">%s</li>
            </ol>
          </nav>
          <h1 id="titre-page">%s</h1>
          <p class="lead">%s</p>
        </div>
%s      </div>
    </section>
''' % (' page-head--split' if aside else '', crumb, h1, lead, side)


# ---------------------------------------------------------------- formulaire
TRAVAUX = [('plafond-tendu', 'Plafond tendu'), ('plafond-acoustique', 'Plafond acoustique ou phonique'),
           ('faux-plafond', 'Faux-plafond (plâtre, fibre, métal)'), ('cloisons', 'Cloisons'),
           ('isolation', 'Isolation thermique ou phonique'), ('protection-incendie', 'Protection incendie'),
           ('cadres-acoustiques', 'Cadres acoustiques'), ('peinture', 'Peinture intérieure'),
           ('autre', 'Autres travaux ou plusieurs prestations')]


def devis_form(fid, title='Demande de devis', hl='h3', title_id=None):
    opts = ''.join('\n                  <option value="%s">%s</option>' % t for t in TRAVAUX)
    tid = title_id or fid + '-titre'
    return '''<div class="form-card">
          <%(hl)s id="%(tid)s">%(title)s</%(hl)s>
          <p>Indiquez au moins un téléphone ou un e-mail pour que nous puissions vous répondre. Les champs sans mention sont facultatifs.</p>
          <!-- MAQUETTE : aucun envoi réel. BRANCHEMENT : remplacer action="#" par l'URL du script d'envoi
               (ex. envoyer-devis.php chez l'hébergeur, en Suisse), ajouter enctype="multipart/form-data" pour la pièce jointe,
               et suivre le commentaire « BRANCHEMENT » dans assets/js/main.js, section 3.
               Le champ « site_web » est un piège à robots (pot de miel) : rejeter côté serveur tout envoi où il est rempli. -->
          <form action="#" method="post" data-devis aria-labelledby="%(tid)s">
            <div class="hp" aria-hidden="true">
              <label for="%(fid)s-site">Ne pas remplir ce champ</label>
              <input id="%(fid)s-site" name="site_web" type="text" tabindex="-1" autocomplete="off">
            </div>
            <div class="form-grid">
              <div class="field field--full">
                <label for="%(fid)s-nom">Nom et prénom <span class="opt">(obligatoire)</span></label>
                <input id="%(fid)s-nom" name="nom" type="text" autocomplete="name" required data-requis="Indiquez votre nom et votre prénom." aria-describedby="%(fid)s-nom-err">
                <span class="error" id="%(fid)s-nom-err" hidden></span>
              </div>
              <div class="field">
                <label for="%(fid)s-tel">Téléphone</label>
                <input id="%(fid)s-tel" name="telephone" type="tel" autocomplete="tel" inputmode="tel" pattern="[0-9+()./ \\-]{9,20}" data-un-des="email" data-format="Indiquez un numéro valable, par exemple 079 123 45 67." aria-describedby="%(fid)s-tel-hint %(fid)s-tel-err">
                <span class="hint" id="%(fid)s-tel-hint">Exemple : 079 123 45 67</span>
                <span class="error" id="%(fid)s-tel-err" hidden></span>
              </div>
              <div class="field">
                <label for="%(fid)s-mail">E-mail</label>
                <input id="%(fid)s-mail" name="email" type="email" autocomplete="email" aria-describedby="%(fid)s-mail-err">
                <span class="error" id="%(fid)s-mail-err" hidden></span>
              </div>
              <div class="field">
                <label for="%(fid)s-commune">Commune du chantier</label>
                <input id="%(fid)s-commune" name="commune" type="text" autocomplete="address-level2">
              </div>
              <div class="field">
                <label for="%(fid)s-travaux">Type de travaux <span class="opt">(obligatoire)</span></label>
                <select id="%(fid)s-travaux" name="travaux" required data-requis="Choisissez le type de travaux." aria-describedby="%(fid)s-travaux-err">
                  <option value="">Choisissez dans la liste</option>%(opts)s
                </select>
                <span class="error" id="%(fid)s-travaux-err" hidden></span>
              </div>
              <div class="field field--full">
                <label for="%(fid)s-msg">Votre projet</label>
                <textarea id="%(fid)s-msg" name="message" rows="5" aria-describedby="%(fid)s-msg-hint"></textarea>
                <span class="hint" id="%(fid)s-msg-hint">Type de local, surface approximative, délai souhaité…</span>
              </div>
              <div class="field field--full file-field">
                <label for="%(fid)s-fichier">Photo ou plan</label>
                <!-- Champ fichier natif masqué visuellement (reste accessible au clavier) ; libellé stylé en bouton, état mis à jour en JS -->
                <input class="visually-hidden file-input" id="%(fid)s-fichier" name="fichier" type="file" accept="image/jpeg,image/png,application/pdf" aria-describedby="%(fid)s-fichier-etat %(fid)s-fichier-hint">
                <div class="file-row">
                  <label class="btn btn--ghost file-btn" for="%(fid)s-fichier">Choisir un fichier</label>
                  <span class="file-state" id="%(fid)s-fichier-etat" aria-live="polite">Aucun fichier sélectionné</span>
                </div>
                <span class="hint" id="%(fid)s-fichier-hint">Formats JPG, PNG ou PDF.</span>
              </div>
              <div class="field field--full">
                <label class="check" for="%(fid)s-rappel">
                  <input id="%(fid)s-rappel" name="rappel" type="checkbox" value="oui">
                  <span>Je préfère être rappelé(e) par téléphone.</span>
                </label>
                <label class="check" for="%(fid)s-accord">
                  <input id="%(fid)s-accord" name="accord" type="checkbox" value="oui" required data-requis="Cochez cette case pour que nous puissions traiter votre demande." aria-describedby="%(fid)s-accord-err">
                  <span>J'accepte que mes données servent uniquement à répondre à ma demande (<a href="mentions-legales.html#donnees">protection des données</a>). <span class="opt">(obligatoire)</span></span>
                </label>
                <span class="error" id="%(fid)s-accord-err" hidden></span>
              </div>
            </div>
            <div class="form-actions">
              <button class="btn" type="submit">Envoyer ma demande</button>
              <p>Vous préférez parler de vive voix ? <a href="%(tel_uri)s">%(tel)s</a></p>
            </div>
          </form>
          <div class="form-success" role="status" tabindex="-1" hidden>
            <p class="form-success__title">Merci <span data-nom></span>, votre demande est bien prête.</p>
            <p>Nous vous recontactons rapidement pour convenir d'une visite. Pour une question urgente : <a href="%(tel_uri)s">%(tel)s</a>.</p>
            <!-- MAQUETTE : aucun message n'est réellement envoyé (voir le commentaire BRANCHEMENT). -->
          </div>
        </div>''' % dict(fid=fid, hl=hl, tid=tid, title=title, opts=opts, tel=TEL, tel_uri=TEL_URI)


# ---------------------------------------------------------------- zone d'intervention (brief SEO §5, Carouge en tête)
ZONES = [
    ('Siège', [('Carouge', True)]),
    ('Ville de Genève', [('Genève', True), ('Eaux-Vives', False), ('Champel', False), ('Plainpalais', False), ('Jonction', False),
                         ('Pâquis', False), ('Servette', False), ('Cité', False)]),
    ('Trois-Chêne', [('Chêne-Bourg', True), ('Chêne-Bougeries', False), ('Thônex', False)]),
    ('Arve-Lac', [('Collonge-Bellerive', True), ('Cologny', False), ('Vandœuvres', False), ('Corsier', False), ('Anières', False),
                  ('Hermance', False), ('Choulex', False), ('Meinier', False), ('Puplinge', False), ('Presinge', False), ('Jussy', False)]),
    ('Sud, Arve et Rhône', [('Plan-les-Ouates', True), ('Lancy', False), ('Veyrier', False), ('Troinex', False), ('Bardonnex', False),
                            ('Onex', False), ('Confignon', False), ('Bernex', False), ('Perly-Certoux', False)]),
    ('Rive droite', [('Vernier', False), ('Meyrin', False), ('Grand-Saconnex', False), ('Pregny-Chambésy', False), ('Bellevue', False),
                     ('Genthod', False), ('Versoix', False), ('Collex-Bossy', False), ('Satigny', False), ('Céligny', False)]),
    ('Vaud : Terre Sainte', [('Coppet', True), ('Chavannes-de-Bogis', True), ('Founex', False), ('Commugny', False), ('Mies', False),
                            ('Tannay', False), ('Chavannes-des-Bois', False)]),
    ('Vaud : Nyon et environs', [('Nyon', True), ('Prangins', False), ('Gland', False), ('Crans', False), ('Rolle', False)]),
]


def zone_block(level='h2', tid='zone-titre', eyebrow=True):
    rows = ''
    for label, communes in ZONES:
        txt = ', '.join(('<strong>%s</strong>' % c) if b else c for c, b in communes)
        note = '\n          <!-- PROVISOIRE : à valider avec le client (jusqu\'où se déplace-t-il : Gland, Rolle ?) -->' if label.endswith('environs') else ''
        rows += '%s\n          <div><dt>%s</dt><dd>%s</dd></div>' % (note, label, txt)
    eb = '<p class="eyebrow">Genève et ouest vaudois</p>\n          ' if eyebrow else ''
    return '''<div class="container split zone">
        <div>
          %(eb)s<%(l)s id="%(tid)s">Zone d'intervention</%(l)s>
          <p class="lead">Nous intervenons dans tout le canton de Genève (Genève-ville, Trois-Chêne, Carouge, Lancy, Arve-Lac, Rive droite) et dans l'ouest vaudois (Terre Sainte, Nyon et environs).</p>
          <p>Pour un chantier situé ailleurs, appelez-nous : nous vous dirons franchement si nous pouvons le prendre en charge.</p>
          <div class="hq">
            <p class="label">Notre siège</p>
            %(p_addr)s
            <address>%(street)s<br>%(city)s</address>
            <a class="link-arrow" href="%(maps)s" rel="noopener">Voir sur la carte</a>
          </div>
        </div>
        <dl class="zones">%(rows)s
        </dl>
      </div>''' % dict(eb=eb, l=level, tid=tid, p_addr=P_ADDR, street=STREET, city=CITY, maps=MAPS, rows=rows)


def cta_band(title, text, hid='cta-titre'):
    return '''    <section class="section section--dark on-dark section--tight" aria-labelledby="%(hid)s">
      <div class="container cta-band">
        <div>
          <h2 id="%(hid)s">%(title)s</h2>
          <p>%(text)s</p>
        </div>
        <div class="cta-band__actions">
          <a class="btn" href="contact.html#devis">Demander un devis</a>
          <a class="btn btn--light" href="%(tel_uri)s">Appeler le %(tel)s</a>
        </div>
      </div>
    </section>
''' % dict(hid=hid, title=title, text=text, tel_uri=TEL_URI, tel=TEL)


import re
NB = '\u00a0'


def fr(t):
    """Typographie française : espaces insécables devant : ; ? ! », après «, dans les numéros et les heures."""
    t = re.sub(r' ([:;?!»])', NB + r'\1', t)
    t = t.replace('« ', '«' + NB)
    t = re.sub(r'\+41 (\d\d) (\d\d\d) (\d\d) (\d\d)', lambda m: NB.join(['+41'] + list(m.groups())), t)
    t = re.sub(r'\b0(\d\d) (\d\d\d) (\d\d) (\d\d)\b', lambda m: NB.join(['0' + m.group(1)] + list(m.groups()[1:])), t)
    t = re.sub(r'(\d+) h (\d\d)', r'\1' + NB + 'h' + NB + r'\2', t)
    t = re.sub(r'(\d+) (ans|photos|références)\b', r'\1' + NB + r'\2', t)
    return t


def typo(doc):
    """Applique fr() aux seuls nœuds texte du <body> (ni attributs, ni commentaires, ni scripts)."""
    head, sep, body = doc.partition('<body>')
    body = re.sub(r'>([^<]+)<', lambda m: '>' + fr(m.group(1)) + '<', body)
    return head + sep + body


def write(name, content):
    content = typo(content)
    with open(os.path.join(SITE, name), 'w', encoding='utf-8') as f:
        f.write(content)
    print('écrit', name, len(content.encode('utf-8')), 'octets')
