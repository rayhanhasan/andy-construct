# -*- coding: utf-8 -*-
"""Gabarits communs du site v2 : coordonnées (NAP), <head>, en-tête, pied de page, assemblage des pages."""
import datetime, json, os, re
import ctx
from ctx import e, T, V, definitif, marque, PROD

ANNEE = datetime.date.today().year
AUJOURDHUI = datetime.date.today()

# ---------------------------------------------------------------- NAP (même texte partout)
NAME = 'Andy Construct'
LEGAL = 'Andy Construct, Chanton & Cie'
STREET = 'Route des Acacias 48'
CITY = '1227 Carouge (Genève)'
TEL = '+41 22 771 20 15'
TEL_URI = 'tel:+41227712015'
MOB = '+41 78 631 14 34'
MOB_URI = 'tel:+41786311434'
IDE = 'CHE-113.706.162'
ZEFIX = 'https://www.zefix.ch/fr/search/entity/list?name=CHE-113.706.162'
MAPS = 'https://www.google.com/maps/search/?api=1&amp;query=Route+des+Acacias+48%2C+1227+Carouge'
LINKEDIN = 'https://www.linkedin.com/company/andy-construct-chanton-et-cie'
LOCALCH = 'https://www.local.ch/fr/d/carouge-ge/1227/revetement-des-plafonds-et-plafonds-suspendus/andy-construct-chanton-cie-OGrZ5DP4atJqYki9WoTjPg'
GGE = 'https://gge.ch/entreprises-2/andy-construct-chanton-cie/'


def mail():
    return V('C30', 'contact@andyconstruct.ch', 'andy.construct@bluewin.ch')


def mail_html(sujet=None, cls='', emplacement=None):
    m = mail()
    href = 'mailto:' + m + (('?subject=' + sujet.replace(' ', '%20')) if sujet else '')
    attrs = (' class="%s"' % cls if cls else '') + (' data-suivi-emplacement="%s"' % emplacement if emplacement else '')
    return '<a href="%s"%s>%s</a>' % (href, attrs, T('C30', m, m))


def mob_label():
    return T('C30', 'Sur les chantiers', 'Mobile')


def horaires(long=True):
    """« Du lundi au vendredi, 7 h – 18 h » (C03) ; repli : masqué."""
    return T('C03', 'Du lundi au vendredi, 7 h – 18 h' if long else 'Lun-ven, 7 h – 18 h', '')


def tel_link(cls='', emplacement=None, texte=None, numero='fixe'):
    attrs = (' class="%s"' % cls if cls else '') + ' data-suivi-numero="%s"' % numero
    if emplacement:
        attrs += ' data-suivi-emplacement="%s"' % emplacement
    uri, num = (TEL_URI, TEL) if numero == 'fixe' else (MOB_URI, MOB)
    return '<a href="%s"%s>%s</a>' % (uri, attrs, texte or num)


def nap(cls='nap'):
    h = horaires()
    return ('<address class="%s"><strong>%s</strong><br>%s<br>%s<br>Tél. %s<br>%s : %s<br>%s%s</address>'
            % (cls, NAME, STREET, CITY, tel_link(), mob_label(), tel_link(numero='mobile'), mail_html(),
               ('<br>' + h) if h else ''))


# ---------------------------------------------------------------- services
def nom_isolantes():
    return V('C16', 'Cloisons isolantes', 'Cloisons isothermes')


SERVICES = ['placo', 'peinture', 'isolation-acoustique', 'cloisons-isothermes']


def svc_nom(s, html=True):
    if s == 'cloisons-isothermes':
        return T('C16', 'Cloisons isolantes', 'Cloisons isothermes') if html else nom_isolantes()
    return {'placo': 'Placo', 'peinture': 'Peinture', 'isolation-acoustique': 'Isolation acoustique'}[s]


NAV_DESC = {'placo': 'Cloisons, doublages, faux-plafonds', 'peinture': 'Murs et plafonds, à l\'intérieur',
            'isolation-acoustique': 'Contre le bruit et l\'écho', 'cloisons-isothermes': 'Caves, garages, combles'}


def svc_url(s):
    return s + '.html'


# ---------------------------------------------------------------- documents téléchargeables (décision D7)
DOCS = {
    'references': ('assets/docs/andy-construct-references.pdf', 'PDF'),
    'guide-bruit': ('assets/docs/guide-reduire-le-bruit.pdf', 'PDF'),
    'checklist': ('assets/docs/checklist-chantier-site-occupe.pdf', 'PDF'),
    'avis-locataires': ('assets/docs/modele-avis-aux-locataires.docx', 'Word'),
}


def doc(cle):
    """(url, « PDF, 850 Ko ») si le fichier existe dans site/, sinon None : le lien n'est pas publié."""
    chemin, fmt = DOCS[cle]
    src = os.path.join(ctx.SITE, chemin)
    if not os.path.exists(src):
        return None
    o = os.path.getsize(src)
    poids = ('%d Ko' % max(1, round(o / 1024))) if o < 1024 * 1024 else ('%s Mo' % ('%.1f' % (o / 1048576)).replace('.', ','))
    return chemin, '%s, %s' % (fmt, poids)


# ---------------------------------------------------------------- ressources versionnées (remplies par build.py)
ASSETS = {'css': 'assets/css/styles.css', 'js': 'assets/js/main.js', 'suivi': 'assets/js/suivi.js'}

EARLY_JS = ("(function(d){d.className=d.className.replace('no-js','js');"
            "try{if(sessionStorage.getItem('ac-bandeau')==='1')d.classList.add('vbar-off')}catch(e){}})(document.documentElement);")


# ---------------------------------------------------------------- <head>
def jsonld(obj):
    return ('  <script type="application/ld+json">%s</script>\n'
            % json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))


def head(p):
    """p : dict(fichier, title, desc, ld=[], preload='', index=True, og_title=None)."""
    fichier = p['fichier']
    url = PROD + ('' if fichier == 'index.html' else fichier)
    indexable = p.get('index', True) and ctx.prod()
    out = ['<!DOCTYPE html>\n<!-- Généré par tools/build (mode %s) : modifier les sources, pas ce fichier -->\n' % ctx.MODE,
           '<html lang="fr-CH" class="no-js">\n<head>\n',
           '  <meta charset="utf-8">\n',
           '  <meta name="viewport" content="width=device-width, initial-scale=1">\n',
           '  <title>%s</title>\n' % e(p['title']),
           '  <meta name="description" content="%s">\n' % e(p['desc'])]
    if p.get('base'):
        out.append('  <base href="/">\n')
    if not indexable:
        out.append('  <meta name="robots" content="noindex%s">\n' % ('' if ctx.prod() else ', nofollow'))
    if p.get('canonical', True):
        out.append('  <link rel="canonical" href="%s">\n' % url)
    out += ['  <meta name="theme-color" content="#1D1F22">\n',
            '  <meta property="og:type" content="website">\n',
            '  <meta property="og:locale" content="fr_CH">\n',
            '  <meta property="og:site_name" content="Andy Construct">\n',
            '  <meta property="og:title" content="%s">\n' % e(p.get('og_title') or p['title']),
            '  <meta property="og:description" content="%s">\n' % e(p['desc']),
            '  <meta property="og:url" content="%s">\n' % url,
            '  <meta property="og:image" content="%sassets/img/og-andy-construct.jpg">\n' % PROD,
            '  <meta property="og:image:width" content="1200">\n',
            '  <meta property="og:image:height" content="630">\n',
            '  <meta property="og:image:alt" content="Faux-plafond en plaques de plâtre à gorge lumineuse, posé par Andy Construct">\n',
            '  <meta name="twitter:card" content="summary_large_image">\n',
            '  <link rel="icon" href="favicon.ico" sizes="any">\n',
            '  <link rel="icon" type="image/png" sizes="32x32" href="assets/img/brand/favicon-32.png">\n',
            '  <link rel="apple-touch-icon" href="assets/img/brand/apple-touch-icon.png">\n',
            '  <link rel="manifest" href="site.webmanifest">\n',
            p.get('preload', ''),
            '  <link rel="preload" href="assets/fonts/source-sans-3-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>\n',
            '  <link rel="preload" href="assets/fonts/montserrat-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>\n',
            '  <link rel="stylesheet" href="%s">\n' % ASSETS['css'],
            '  <script>%s</script>\n' % EARLY_JS,
            '  <script src="%s" defer></script>\n' % ASSETS['suivi'],
            '  <script src="%s" defer></script>\n' % ASSETS['js']]
    src, wid = ctx.CONFIG.get('umami_src', ''), ctx.CONFIG.get('umami_id', '')
    if src and wid:
        out.append('  <script src="%s" data-website-id="%s" data-before-send="acUmamiAvantEnvoi" data-do-not-track="true" defer></script>\n'
                   % (e(src), e(wid)))
    for obj in p.get('ld', []):
        out.append(jsonld(obj))
    out.append('</head>\n')
    return ''.join(out)


# ---------------------------------------------------------------- bandeau de validation (preview, verification)
def bandeau():
    if ctx.prod():
        return ''
    if ctx.MODE == 'verification':
        txt = 'Version de validation. Les passages soulignés en pointillé attendent votre confirmation.'
        legende = '<!--LEGENDE-->'
    else:
        txt = 'Version de validation. Certains passages attendent encore votre confirmation.'
        legende = ''
    return '''  <div class="vbar" role="region" aria-label="Version de validation">
    <div class="container vbar__inner">
      <p>%s</p>%s
      <button type="button" class="vbar__close">Masquer ce message</button>
    </div>
  </div>
''' % (txt, legende)


def legende_html(codes):
    if not codes:
        return '<p class="vbar__none">Aucun point à confirmer sur cette page.</p>'
    items = ''.join('<li><b>%s</b> %s</li>' % (c, e(ctx.QUESTIONS.get(c, ''))) for c in sorted(codes))
    return ('\n      <details class="vbar__legend"><summary>Points à confirmer sur cette page (%d)</summary><ul>%s</ul></details>'
            % (len(codes), items))


# ---------------------------------------------------------------- en-tête
ICON_PHONE = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.75">'
              '<path d="M6.5 3h3l1.5 4.5-2 1.5a11 11 0 0 0 6 6l1.5-2 4.5 1.5v3a2 2 0 0 1-2 2A17 17 0 0 1 4.5 5a2 2 0 0 1 2-2z"/></svg>')

NAV = [('realisations.html', 'Réalisations'), ('professionnels.html', 'Professionnels'),
       ('entreprise.html', "L'entreprise"), ('contact.html', 'Contact')]


def devis_href(p):
    return '#demande' if p.get('formulaire') else 'contact.html#demande'


def devis_btn(p, emplacement, cls='btn', texte='Demander un devis', service=None):
    s = service or p.get('service')
    return '<a class="%s" href="%s" data-suivi="devis_clic" data-suivi-emplacement="%s"%s>%s</a>' % (
        cls, devis_href(p), emplacement, (' data-suivi-service="%s"' % s) if s else '', texte)


def header(p):
    actif = p['fichier']
    svc_items = ''.join(
        '<li><a href="%s"%s><b>%s</b><span>%s</span></a></li>' % (
            svc_url(s), ' aria-current="page"' if actif == svc_url(s) else '', svc_nom(s), NAV_DESC[s])
        for s in SERVICES)
    svc_actif = ' is-current' if actif in [svc_url(s) for s in SERVICES] else ''
    items = ''.join('<li><a href="%s"%s>%s</a></li>' % (h, ' aria-current="page"' if h == actif else '', l) for h, l in NAV)
    h_small = horaires(long=False) or 'Appelez-nous'
    return '''  <header class="site-header" data-suivi-zone="entete">
    <div class="container site-header__inner">
      <a class="brand" href="index.html"><img src="assets/img/brand/logo-andy-construct-352.png" width="352" height="128" alt="Andy Construct, page d'accueil"></a>
      <nav class="site-nav" id="menu-principal" aria-label="Navigation principale">
        <ul class="nav-list">
          <li class="nav-svc"><details class="nav-drop%(svc_actif)s"><summary>Prestations</summary><ul class="nav-drop__panel">%(svc_items)s</ul></details></li>
          %(items)s
          <li class="nav-extra"><a class="btn btn--ghost" href="%(tel_uri)s" data-suivi-numero="fixe" data-suivi-emplacement="menu">Appeler le %(tel)s</a>%(devis)s</li>
        </ul>
      </nav>
      <a class="header-phone" href="%(tel_uri)s" data-suivi-numero="fixe"><small>%(h_small)s</small><span>%(tel)s</span></a>
      %(cta)s
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu-principal"><span class="nav-toggle__icon" aria-hidden="true"><span></span></span><span class="nav-toggle__label">Menu</span></button>
    </div>
  </header>
''' % dict(svc_items=svc_items, svc_actif=svc_actif, items=items, tel_uri=TEL_URI, tel=TEL, h_small=h_small,
           devis='' if p.get('sans_devis') else devis_btn(p, 'menu'),
           cta='' if p.get('sans_devis') else devis_btn(p, 'entete', cls='btn header-cta'))


# ---------------------------------------------------------------- pied de page
def footer(p):
    import composants
    ref = doc('references')
    pdf = ('<li><a href="%s" data-suivi="plaquette_telechargee">Dossier de références (%s)</a></li>' % ref) if ref else ''
    callbar = '''
  <div class="callbar%s" role="region" aria-label="Contact rapide" data-suivi-zone="barre_mobile">
    <a class="btn btn--ghost" href="%s" data-suivi-numero="fixe">%s Appeler</a>
    %s
  </div>''' % (' callbar--seul' if p.get('sans_devis') else '', TEL_URI, ICON_PHONE, '' if p.get('sans_devis') else devis_btn(p, 'barre_mobile'))
    return '''
  <footer class="site-footer on-dark" data-suivi-zone="pied">
    <div class="container footer-top">
      <div class="footer-brand">
        <img src="assets/img/brand/logo-andy-construct-blanc-380.png" width="380" height="138" alt="Andy Construct" loading="lazy">
        <p>Placo, peinture, isolation acoustique et %(isol)s. Entreprise de Carouge, inscrite au registre du commerce depuis 2007. Toute la Suisse romande.</p>
      </div>
      <div>
        <h2>Nous joindre</h2>
        %(nap)s
        <p class="footer-map"><a href="%(maps)s" rel="noopener">Voir sur la carte</a></p>
      </div>
      <nav aria-label="Prestations">
        <h2>Prestations</h2>
        <ul>%(svc)s</ul>
      </nav>
      <nav aria-label="Andy Construct">
        <h2>Andy Construct</h2>
        <ul>
          <li><a href="realisations.html">Réalisations</a></li>
          <li><a href="professionnels.html">Professionnels</a></li>
          <li><a href="entreprise.html">L'entreprise</a></li>
          <li><a href="contact.html">Contact</a></li>
          %(pdf)s
        </ul>
      </nav>
    </div>
    <div class="container footer-refs">
      %(refs)s
    </div>
    <div class="footer-bottom">
      <div class="container">
        <p>© %(annee)d %(legal)s · <span class="nowrap">IDE %(ide)s</span></p>
        <ul>
          <li><a href="%(zefix)s" rel="noopener">Vérifier au registre du commerce</a></li>
          <li><a href="mentions-legales.html">Mentions légales</a></li>
          <li><a href="confidentialite.html">Protection des données</a></li>
        </ul>
      </div>
    </div>
  </footer>%(callbar)s
''' % dict(isol=V('C16', 'cloisons isolantes', 'cloisons isothermes'), nap=nap(), maps=MAPS, pdf=pdf,
           svc=''.join('<li><a href="%s">%s</a></li>' % (svc_url(s), svc_nom(s)) for s in SERVICES),
           refs=composants.refs_pied(), annee=ANNEE, legal=LEGAL, ide=IDE, zefix=ZEFIX, callbar=callbar)


# ---------------------------------------------------------------- en-tête de page secondaire (composant page-head)
def fil(nom):
    return ('<nav class="breadcrumb" aria-label="Fil d\'Ariane"><ol><li><a href="index.html">Accueil</a></li>'
            '<li aria-current="page">%s</li></ol></nav>' % nom)


def page_head(crumb, h1, lead, extra='', photo='', cls=''):
    media = ('\n        <div class="page-head__media">%s</div>' % photo) if photo else ''
    return '''    <section class="page-head%s" aria-labelledby="titre-page">
      <div class="container page-head__grid">
        <div class="page-head__text">
          %s
          <h1 id="titre-page">%s</h1>
          <p class="lead">%s</p>%s
        </div>%s
      </div>
    </section>
''' % ((' page-head--media' if photo else '') + (' ' + cls if cls else ''), fil(crumb), h1, lead, extra, media)


def ld_page(fichier, nom, crumb, typ='WebPage', extra=None):
    url = PROD + fichier
    page = {'@type': typ, '@id': url + '#page', 'url': url, 'name': nom, 'inLanguage': 'fr-CH',
            'isPartOf': {'@id': PROD + '#site'}, 'publisher': {'@id': PROD + '#entreprise'},
            'breadcrumb': {'@id': url + '#fil'}}
    page.update(extra or {})
    return {'@context': 'https://schema.org', '@graph': [
        page,
        {'@type': 'BreadcrumbList', '@id': url + '#fil', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Accueil', 'item': PROD},
            {'@type': 'ListItem', 'position': 2, 'name': crumb, 'item': url}]}]}


# ---------------------------------------------------------------- assemblage et écriture
PAGES_ECRITES = []


def page(p, corps):
    """Assemble et écrit une page. p : dict(fichier, title, desc, …) ; corps : contenu de <main>."""
    ctx.UTILISES.clear()
    hd = header(p)
    ft = footer(p)
    doc = (head(p) + '<body>\n  <a class="skip-link" href="#contenu">Aller au contenu</a>\n' + bandeau() + hd
           + '  <main id="contenu">\n' + corps + '  </main>\n' + ft + '</body>\n</html>\n')
    doc = doc.replace('<!--LEGENDE-->', legende_html(ctx.UTILISES))
    doc = ctx.typo(doc)
    controler(p['fichier'], doc)
    with open(os.path.join(ctx.OUT, p['fichier']), 'w', encoding='utf-8') as f:
        f.write(doc)
    PAGES_ECRITES.append((p['fichier'], p.get('index', True)))
    print('  %-26s %6d octets' % (p['fichier'], len(doc.encode('utf-8'))))


def controler(nom, doc):
    """Aucun marqueur du copy deck ni variable non remplacée ; en production, aucune marque de vérification."""
    for motif in ('[À CONFIRMER', '[À VÉRIFIER', '{{', '}}', '%(', 'None<', '>None'):
        if motif in doc:
            raise SystemExit('ERREUR %s : « %s » reste dans la page' % (nom, motif))
    if ctx.prod() and ('class="vc"' in doc or 'class="vbar' in doc or 'noindex' in doc and nom not in ('merci.html', '404.html', 'prestations.html')):
        raise SystemExit('ERREUR %s : marque de validation ou noindex en production' % nom)
