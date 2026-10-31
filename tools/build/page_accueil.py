# -*- coding: utf-8 -*-
"""Accueil (architecture §4.1, copy deck §B)."""
import ctx
from ctx import e, T, V, definitif, marque, PROD
from common import (page, TEL, TEL_URI, devis_btn, horaires, svc_nom, svc_url, SERVICES, mail, LEGAL, IDE, STREET, MOB, AUJOURDHUI,
                    LINKEDIN, LOCALCH, GGE)
import composants as c
import portfolio as pf
from icons import ICONS

HERO = 'faux-plafond-placo-gorge-lumineuse-01'
H = 'assets/img/portfolio/' + HERO


HERO_SIZES = '(min-width: 900px) 50vw, 100vw'      # bureau : moitié droite de l'écran ; mobile : pleine largeur, 4:3


def hero_preload():
    return ('  <link rel="preload" as="image" type="image/webp" fetchpriority="high" imagesrcset="%s-800.webp 800w, %s-1200.webp 1200w, %s-1600.webp 1600w" imagesizes="%s">\n'
            % (H, H, H, HERO_SIZES))


def hero_pic():
    return ('<picture><source type="image/webp" srcset="%s-800.webp 800w, %s-1200.webp 1200w, %s-1600.webp 1600w" sizes="%s">'
            '<img src="%s-800.jpg" width="1600" height="1200" alt="%s" fetchpriority="high"></picture>'
            % (H, H, H, HERO_SIZES, H, e(pf.alt(HERO))))


def business():
    """Entité unique « entreprise », décrite en entier sur l'accueil (architecture §11)."""
    zones = ['Canton de Genève', 'Canton de Vaud', 'Canton de Neuchâtel', 'Canton de Fribourg', 'Valais romand', 'Canton du Jura', 'Jura bernois']
    img = lambda pid: PROD + 'assets/img/portfolio/%s-1600.webp' % pid
    b = {
        '@type': 'HomeAndConstructionBusiness', '@id': PROD + '#entreprise', 'name': 'Andy Construct', 'legalName': LEGAL,
        'description': V('C16', "Entreprise de Carouge (Genève) active depuis 2007 : placo (cloisons, doublages et faux-plafonds en plaques de plâtre), "
                         "peinture intérieure, isolation acoustique et cloisons isolantes (isothermes), dans toute la Suisse romande.",
                         "Entreprise de Carouge (Genève) active depuis 2007 : placo (cloisons, doublages et faux-plafonds en plaques de plâtre), "
                         "peinture intérieure, isolation acoustique et cloisons isothermes, dans toute la Suisse romande."),
        'url': PROD, 'logo': PROD + 'assets/img/brand/logo-andy-construct.png',
        'image': [img('faux-plafond-placo-gorge-lumineuse-01'), img('faux-plafond-placo-gorge-lumineuse-02'), img('chantier-suspentes-ossature-01')],
        'telephone': TEL, 'email': mail(), 'foundingDate': '2007',
        'foundingLocation': {'@type': 'Place', 'name': 'Perly-Certoux'},
        'identifier': {'@type': 'PropertyValue', 'propertyID': 'IDE', 'value': IDE},
        'address': {'@type': 'PostalAddress', 'streetAddress': STREET, 'postalCode': '1227', 'addressLocality': 'Carouge',
                    'addressRegion': 'GE', 'addressCountry': 'CH'},
        'geo': {'@type': 'GeoCoordinates', 'latitude': 46.18935, 'longitude': 6.13236},
        'contactPoint': [{'@type': 'ContactPoint', 'telephone': TEL, 'contactType': 'customer service', 'areaServed': 'CH', 'availableLanguage': ['fr']},
                         {'@type': 'ContactPoint', 'telephone': MOB, 'contactType': 'sales', 'areaServed': 'CH', 'availableLanguage': ['fr']}],
        'areaServed': [{'@type': 'AdministrativeArea', 'name': z} for z in zones],
        'knowsAbout': ['Placo', 'Plâtrerie', 'Cloisons en plaques de plâtre', 'Doublages', 'Faux-plafonds', 'Peinture intérieure',
                       'Isolation acoustique', 'Isolation phonique'] + (['Correction acoustique'] if definitif('C18') else [])
                      + (['Cloisons isolantes'] if definitif('C16') else []) + ['Cloisons isothermes'],
        'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Prestations', 'itemListElement': [
            {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': svc_nom(s, html=False), 'url': PROD + svc_url(s)}} for s in SERVICES]},
        'sameAs': [LOCALCH, LINKEDIN] + ([GGE] if definitif('C11') else []),
    }
    if definitif('C03'):
        b['openingHoursSpecification'] = [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                                           'opens': '07:00', 'closes': '18:00'}]
    return b


def faq():
    qs = [
        c.Q('C04', 'Faites-vous aussi les petits travaux ?',
            'Oui. Une pièce à repeindre, une cloison ou un plafond à refaire nous intéressent autant qu\'un grand chantier.'),
        ('Combien coûtent vos travaux ?',
         'Le prix dépend de la surface, de l\'état des murs et des plafonds, de la hauteur, de l\'accès et des finitions. '
         + T('C06', 'Après la visite, vous recevez une offre écrite détaillée, en CHF.', 'Après la visite, vous recevez une offre écrite.'),
         'Le prix dépend de la surface, de l\'état des murs et des plafonds, de la hauteur, de l\'accès et des finitions. '
         + V('C06', 'Après la visite, vous recevez une offre écrite détaillée, en CHF.', 'Après la visite, vous recevez une offre écrite.')),
        c.Q('C02', 'La visite et le devis sont-ils payants ?',
            'Non. La visite et le devis sont gratuits et sans engagement. Vous décidez une fois l\'offre écrite reçue.'),
        c.Q('C01 C41', 'En combien de temps pouvez-vous venir ?',
            'Nous vous rappelons le jour même ou le jour ouvrable suivant, et proposons une visite en général dans la semaine. Le délai des travaux figure dans l\'offre.',
            'Nous vous rappelons pour convenir d\'une date de visite. Le délai des travaux figure dans l\'offre écrite.'),
        ('Intervenez-vous hors de Genève ?',
         'Oui, dans toute la Suisse romande : Vaud, Neuchâtel, Fribourg, Valais romand, Jura et Jura bernois. '
         + T('C22', 'Nous avons par exemple travaillé à Coppet, à Nyon et à Chavannes-de-Bogis.', ''),
         'Oui, dans toute la Suisse romande : Vaud, Neuchâtel, Fribourg, Valais romand, Jura et Jura bernois. '
         + V('C22', 'Nous avons par exemple travaillé à Coppet, à Nyon et à Chavannes-de-Bogis.', '')),
        c.Q('C07', 'Comment protégez-vous mon logement pendant les travaux ?',
            'Nous couvrons les sols et les meubles, fermons la zone de travail par des bâches si nécessaire et nettoyons chaque soir. Le dernier jour, nous rendons les lieux propres.'),
        c.Q(None, 'Travaillez-vous pour les régies, les architectes et les communes ?',
            'Oui. La Ville de Genève, des salles communales, le Conservatoire de musique et la HEAD nous ont confié des travaux. '
            'Les professionnels trouvent nos documents sur une <a href="professionnels.html">page dédiée</a>.'),
        c.Q('C32 V01', 'Et si un défaut apparaît après les travaux ?',
            'Appelez-nous : nous revenons. Pour les contrats conclus depuis 2026, la loi vous laisse 60 jours, dès que vous le découvrez, pour signaler un défaut d\'un ouvrage.',
            'Appelez-nous : nous venons voir le défaut avec vous.'),
    ]
    return [q for q in qs if q]




# ---------------------------------------------------------------- héro v3 : panneau anthracite + photo nette, trait laser
def titre_lignes(lignes):
    """Chaque ligne dans un masque : la séquence d'entrée la fait monter (CSS, aucune dépendance au JavaScript)."""
    return ''.join('<span class="l"><span>%s</span></span>' % x for x in lignes)


def hero_titre():
    """Titre du héro ; variantes du drapeau « hero-titre » (une seule visible, choisie avant le premier rendu)."""
    a = titre_lignes(['Placo, peinture', 'et isolation', 'en Suisse romande'])
    b = titre_lignes(['De la plaque', 'de plâtre à la', 'dernière couche'])
    dr = ((ctx.CONFIG.get('ab') or {}).get('drapeaux') or {}).get('hero-titre') or {}
    if not (ctx.CONFIG.get('ab') or {}).get('actif') or not dr.get('actif', True):
        return a
    return '<span data-flag="hero-titre" data-variant="a">%s</span><span data-flag="hero-titre" data-variant="b">%s</span>' % (a, b)


I_BADGE = {
    'registre': '<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5"/><path class="accent" d="M9 14l2.5 2.5L16 12"/>',
    'lieu': '<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z"/><circle class="accent" cx="12" cy="10" r="2.2"/>',
    'visite': '<path d="M4 11l8-7 8 7"/><path d="M6 9.5V20h12V9.5"/><path class="accent" d="M10 20v-5h4v5"/>',
    'assurance': '<path d="M12 3l7 3v5c0 4.5-3 8.2-7 10-4-1.8-7-5.5-7-10V6z"/><path class="accent" d="M9 12l2 2 4-4"/>',
    'groupe': '<path d="M4 20V9l5-3 5 3v11"/><path d="M14 20v-8h6v8M3 20h18"/><path class="accent" d="M7 12h4M7 16h4"/>',
    'pros': '<path d="M4 8h16v12H4z"/><path d="M9 8V5h6v3"/><path class="accent" d="M4 13h16"/>',
}


def badge(icone, titre, sous):
    return ('<li><svg class="badge__i" viewBox="0 0 24 24" aria-hidden="true" focusable="false">%s</svg>'
            '<span><b>%s</b> %s</span></li>' % (I_BADGE[icone], titre, sous))


def badges():
    """Badges de confiance (brief v3 §2) : faits vérifiables, et badges à confirmer rendus selon confirmations.json."""
    out = [badge('registre', 'Depuis 2007', 'inscrite au registre du commerce'),
           badge('lieu', 'Siège à Carouge', 'chantiers dans toute la Suisse romande')]
    if definitif('C02'):
        out.append(marque('C02', badge('visite', 'Visite et devis gratuits', 'sans engagement')))
    else:
        out.append(badge('pros', 'Particuliers et professionnels', 'régies, architectes, communes'))
    if definitif('C11'):
        out.append(marque('C11', badge('groupe', 'Membre du GGE', 'entreprises genevoises du bâtiment')))
    elif definitif('C12'):
        out.append(marque('C12', badge('assurance', 'Assurée en RC', 'attestation sur demande')))
    else:
        out.append(badge('groupe', 'Références publiques', 'Ville de Genève, Conservatoire, HEAD'))
    return '<ul class="badges" aria-label="En bref">%s</ul>' % ''.join(out)


def hero(p):
    texte = T('C05', 'Cloisons, plafonds, isolation contre le bruit et peinture : <b>un seul interlocuteur</b>, de la pose des plaques à la dernière couche.',
              'Cloisons, plafonds, isolation contre le bruit et peinture, pour les <b>particuliers</b> et les <b>professionnels</b>.')
    return '''    <section class="hero" aria-labelledby="titre-page" data-suivi-zone="heros">
      <div class="hero__media">%s</div>
      <div class="container hero__grid">
        <div class="hero__panel">
          <h1 id="titre-page" class="hero__titre">%s</h1>
          <span class="laser" aria-hidden="true"></span>
          <p class="hero__text">%s</p>
          <div class="hero__actions">%s<a class="btn btn--light" href="%s" data-suivi-numero="fixe">Appeler le %s</a></div>
          %s
        </div>
      </div>
    </section>
''' % (hero_pic(), hero_titre(), texte, devis_btn(p, 'heros'), TEL_URI, TEL, badges())


# ---------------------------------------------------------------- prestations : 4 cartes avec image
SVC_PHOTO = {'placo': 'habillage-placo-niches-arrondies-01', 'isolation-acoustique': 'panneaux-acoustiques-muraux-01'}


def svc_media(s):
    """Image d'une prestation : illustration sous licence (signalée), sinon vraie photo publiable, sinon pictogramme."""
    import illustrations
    ill = illustrations.pour_service(s, '(min-width: 1100px) 300px, (min-width: 700px) 45vw, 100vw')
    if ill:
        return ill
    pid = SVC_PHOTO.get(s)
    if pid and pf.photo_ok(pid):
        return c.pic(pid, '(min-width: 1100px) 300px, (min-width: 700px) 45vw, 100vw', pf.alt(pid))
    return '<span class="svc__picto">%s</span>' % ICONS[s]


def carte_service(s, titre, phrase, lien):
    return ('<li class="svc"><a class="svc__link" href="%s"><span class="svc__media">%s</span>'
            '<span class="svc__titre">%s</span><span class="svc__txt">%s</span><span class="svc__more link-arrow">%s</span></a></li>'
            % (svc_url(s), svc_media(s), titre, phrase, lien))


def carte_accueil(href, img, titre, lieu, contrainte, tags, badge=False, cls=''):
    return '''<li class="hcard%s">
            <a class="hcard__link" href="%s">
              <span class="hcard__media">%s%s</span>
              <span class="hcard__body"><span class="hcard__titre">%s</span><span class="hcard__lieu">%s</span><span class="hcard__txt">%s</span></span>
            </a>
            %s
          </li>''' % ((' ' + cls) if cls else '', href, img, '<span class="badge">Pendant les travaux</span>' if badge else '', titre, lieu, contrainte, tags)


def chiffres():
    """Bande des chiffres : valeurs finales dans le HTML (lues sans JavaScript), comptées une fois à l'apparition."""
    nb_refs = len(c.LOGOS) - (0 if definitif('C22') else 1)      # OMC citée seulement avec l'accord (D4)
    ans = AUJOURDHUI.year - 2007 - (1 if (AUJOURDHUI.month, AUJOURDHUI.day) < (6, 1) else 0)
    items = [(ans, 'ans d\'activité, depuis le 1<sup>er</sup> juin 2007'),
             (nb_refs, 'maîtres d\'ouvrage publics et privés cités en référence'),
             (4, 'métiers : placo, peinture, isolation acoustique, %s' % svc_nom('cloisons-isothermes').lower()),
             (7, 'cantons et régions de Suisse romande')]
    lis = ''.join('<li><span class="chiffre" aria-hidden="true" data-count="%d">%d</span><span class="chiffre__lbl">'
                  '<span class="visually-hidden">%d </span>%s</span></li>' % (n, n, n, l) for n, l in items)
    return '''    <section class="section section--dark on-dark chiffres" aria-labelledby="chiffres-titre">
      <div class="container">
        <h2 id="chiffres-titre" class="chiffres__titre">Une entreprise de Carouge, inscrite au registre du commerce depuis 2007</h2>
        <ul class="chiffres__list" data-reveal="cells">%s</ul>
      </div>
    </section>
''' % lis


def build():
    p = dict(fichier='index.html', formulaire=True,
             title='Plâtrerie, peinture et isolation à Genève | Andy Construct',
             desc=V('C16', 'Placo, peinture, isolation acoustique et cloisons isolantes. Entreprise de Carouge depuis 2007, active dans toute la Suisse romande. Tél. +41 22 771 20 15.',
                    'Placo, peinture, isolation acoustique et cloisons isothermes. Entreprise de Carouge depuis 2007, active dans toute la Suisse romande. Tél. +41 22 771 20 15.'),
             og_title='Andy Construct · Placo, peinture et isolation en Suisse romande', preload=hero_preload())
    questions = faq()
    faq_html, faq_ld = c.faq_items(questions)
    p['ld'] = [{'@context': 'https://schema.org', '@graph': [
        business(),
        {'@type': 'WebSite', '@id': PROD + '#site', 'url': PROD, 'name': 'Andy Construct', 'inLanguage': 'fr-CH', 'publisher': {'@id': PROD + '#entreprise'}},
        {'@type': 'WebPage', '@id': PROD + '#page', 'url': PROD, 'name': p['title'], 'inLanguage': 'fr-CH',
         'isPartOf': {'@id': PROD + '#site'}, 'about': {'@id': PROD + '#entreprise'}}]},
        c.faq_ld(PROD, faq_ld)]

    isol = svc_nom('cloisons-isothermes')
    services = ''.join([
        carte_service('placo', 'Placo', 'Cloisons, doublages et <b>faux-plafonds</b> en plaques de plâtre.', 'Voir le placo'),
        carte_service('peinture', 'Peinture', 'Murs et plafonds préparés, peints, et la pièce <b>rendue propre</b>.', 'Voir la peinture'),
        carte_service('isolation-acoustique', 'Isolation acoustique', 'Vous entendez vos voisins ? Nous isolons <b>murs et plafonds</b>.', 'Voir l\'isolation acoustique'),
        carte_service('cloisons-isothermes', isol, 'Une pièce froide contre un garage ou une cave ? <b>Nous l\'isolons.</b>',
                      T('C16', 'Voir les cloisons isolantes', 'Voir les cloisons isothermes')),
    ])

    # Réalisations : une grande carte (hall, gorge lumineuse) et deux cartes empilées
    p1, p2 = pf.PROJ['projet-hall-gorge-lumineuse'], pf.PROJ['projet-grande-salle-ossature']
    tag = lambda codes: codes if not ctx.confirme(codes) else None
    c1 = carte_accueil('realisations.html#' + p1['id'],
                       c.pic('faux-plafond-placo-gorge-lumineuse-02', '(min-width: 1100px) 720px, 100vw', pf.alt('faux-plafond-placo-gorge-lumineuse-02')),
                       p1['titre'], pf._txt(p1['lieu']), pf._txt(p1['contrainte']), pf.tags_html(pf.proj_tags(p1), tag('C25')), cls='hcard--grand')
    ph2 = pf.proj_photos(p2)[0]
    c2 = carte_accueil('realisations.html#' + p2['id'], c.pic(ph2, '(min-width: 1100px) 260px, (min-width: 700px) 45vw, 100vw', pf.alt(ph2)),
                       p2['titre'], pf._txt(p2['lieu']), pf._txt(p2['contrainte']), pf.tags_html(pf.proj_tags(p2), tag('C25')), badge=True)
    split = ('<span class="hcard__split"><span>%s<span class="hcard__lbl">Avant</span></span><span>%s<span class="hcard__lbl">Après</span></span></span>'
             % (c.aa_pic('aa6', 'avant', '(min-width: 1100px) 160px, 50vw', pf.PAIRE['aa6'][4]),
                c.aa_pic('aa6', 'apres', '(min-width: 1100px) 160px, 50vw', pf.PAIRE['aa6'][5])))
    c3 = carte_accueil('realisations.html#avant-apres-aa6', split, 'Séjour : faux-plafond et spots, avant et après',
                       T('C26', 'Appartement', 'Appartement'), T('C26', 'Un plafond redessiné, l\'éclairage intégré.', 'Un plafond redessiné, l\'éclairage intégré.'),
                       pf.tags_html(pf.paire_services('aa6'), tag('C26')))

    ordre = (ctx.CONFIG.get('ab') or {}).get('actif') and (((ctx.CONFIG.get('ab') or {}).get('drapeaux') or {}).get('ordre-sections') or {}).get('actif', True)
    flag_ordre = ' data-flag="ordre-sections"' if ordre else ''
    corps = hero(p) + c.mur_logos() + '''
    <section class="section" id="prestations" aria-labelledby="prestations-titre" data-ordre="prestations"%(flag)s>
      <div class="container">
        <div class="section-head section-head--row">
          <h2 id="prestations-titre">Quatre métiers, souvent sur le même chantier</h2>
          <p>Vous hésitez ? Décrivez votre besoin : nous vous orientons.</p>
        </div>
        <ul class="svcs">%(services)s</ul>
      </div>
    </section>

    <section class="section section--mist" aria-labelledby="realisations-titre" data-ordre="realisations">
      <div class="container">
        <div class="section-head section-head--row">
          <h2 id="realisations-titre">Des chantiers réels, photographiés par notre équipe</h2>
          <a class="link-arrow" href="realisations.html">Toutes les réalisations</a>
        </div>
        <ul class="hcards hcards--asym" data-reveal="cells">%(cartes)s</ul>
        <div class="section-foot">%(devis2)s</div>
      </div>
    </section>
%(chiffres)s
    <section class="section" aria-labelledby="methode-titre">
      <div class="container">
        <div class="section-head section-head--row">
          <h2 id="methode-titre">De la visite à la réception, quatre étapes</h2>
          <a class="link-arrow" href="entreprise.html#methode">Notre méthode en détail</a>
        </div>
        %(methode)s
      </div>
    </section>
%(temoignages)s
    <section class="section section--tight duo-band" aria-label="Professionnels et zone d'intervention">
      <div class="container duo">
        <div class="duo__item">
          <h3>Régies, architectes, communes</h3>
          <p>Immeubles habités, offres sur plans et descriptifs, <b>dossier de références</b> à télécharger.</p>
          <a class="link-arrow" href="professionnels.html">Espace professionnels</a>
        </div>
        <div class="duo__item">
          <h3>Toute la Suisse romande</h3>
          <p>Depuis Carouge : Genève, Vaud, Neuchâtel, Fribourg, Valais romand, Jura et Jura bernois.</p>
          <a class="link-arrow" href="contact.html#zone">Voir la carte</a>
        </div>
      </div>
    </section>

    <section class="section faq" aria-labelledby="faq-titre">
      <div class="container split split--48">
        <div class="faq__head">
          <h2 id="faq-titre">Questions fréquentes</h2>
          <p>Une autre question ? Appelez le <a href="%(tel_uri)s" data-suivi-numero="fixe" data-suivi-emplacement="faq">%(tel)s</a>.</p>
        </div>
        <div class="faq__list">%(faq)s</div>
      </div>
    </section>
''' % dict(flag=flag_ordre, services=services, cartes=c1 + c2 + c3, chiffres=chiffres(),
           devis2=devis_btn(p, 'realisations', cls='btn btn--ghost', texte='Un projet semblable ? Demander un devis'),
           methode=c.methode(True), temoignages=c.temoignages(), tel_uri=TEL_URI, tel=TEL, faq=faq_html)
    # Rappel des références juste avant la demande (bande défilante), puis le bloc de demande
    corps += c.bande_logos(cls='defile--avant-demande') + c.bloc_demande(p, refs=False, source='accueil', surtitre=False)
    page(p, corps)
