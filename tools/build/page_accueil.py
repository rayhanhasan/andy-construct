# -*- coding: utf-8 -*-
"""Accueil (architecture §4.1, copy deck §B)."""
import ctx
from ctx import e, T, V, definitif, marque, PROD
from common import (page, TEL, TEL_URI, devis_btn, horaires, svc_nom, svc_url, SERVICES, mail, LEGAL, IDE, STREET, MOB, AUJOURDHUI, doc, suivi_doc,
                    LINKEDIN, LOCALCH, GGE)
import composants as c
import portfolio as pf
from icons import ICONS

HERO = 'faux-plafond-placo-gorge-lumineuse-01'
H = 'assets/img/portfolio/' + HERO
# Recadrages éditoriaux des vraies photos (docs/v3/credits-images.md §3) : 4:5 pour la moitié droite du héro sur ordinateur,
# 16:9 pour le bandeau photo du mobile (cadre 4:3).
H45, H169 = H + '-4x5', H + '-16x9'
SRC_BUREAU = '%s-800.webp 800w, %s-1600.webp 1600w' % (H45, H45)
SRC_MOBILE = '%s-800.webp 800w, %s-1600.webp 1600w' % (H169, H169)
SIZES_BUREAU, SIZES_MOBILE = '(min-width: 1200px) 50vw, 42vw', '100vw'


def hero_preload():
    return ('  <link rel="preload" as="image" type="image/webp" fetchpriority="high" imagesrcset="%s" imagesizes="%s" media="(min-width: 900px)">\n'
            '  <link rel="preload" as="image" type="image/webp" fetchpriority="high" imagesrcset="%s" imagesizes="%s" media="(max-width: 899.98px)">\n'
            % (SRC_BUREAU, SIZES_BUREAU, SRC_MOBILE, SIZES_MOBILE))


def hero_pic():
    return ('<picture><source media="(min-width: 900px)" type="image/webp" srcset="%s" sizes="%s">'
            '<source type="image/webp" srcset="%s" sizes="%s">'
            '<img src="%s-800.jpg" width="1600" height="900" alt="%s" fetchpriority="high"></picture>'
            % (SRC_BUREAU, SIZES_BUREAU, SRC_MOBILE, SIZES_MOBILE, H169, e(pf.alt(HERO))))


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
    """6 questions (cro-v3 §2.2 H8) ; réponses de 35 mots au plus, mêmes marqueurs que la v2."""
    qs = [
        c.Q('C04', 'Faites-vous aussi les petits travaux ?',
            'Oui. Une pièce à repeindre, une cloison ou un plafond à refaire nous intéressent autant qu\'un grand chantier.'),
        ('Combien coûtent vos travaux ?',
         'Le prix dépend de la surface, de l\'état des supports, de la hauteur, de l\'accès et des finitions. '
         + T('C06', 'Après la visite, vous recevez une offre écrite détaillée, en CHF.', 'Après la visite, vous recevez une offre écrite.'),
         'Le prix dépend de la surface, de l\'état des supports, de la hauteur, de l\'accès et des finitions. '
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
        c.Q('C32 V01', 'Et si un défaut apparaît après les travaux ?',
            'Appelez-nous : nous revenons. Pour les contrats conclus depuis 2026, la loi vous laisse 60 jours, dès que vous le découvrez, pour signaler un défaut d\'un ouvrage.',
            'Appelez-nous : nous venons voir le défaut avec vous.'),
    ]
    return [q for q in qs if q]


# ---------------------------------------------------------------- H1 · héro : panneau anthracite + photo nette, trait laser
def titre_lignes(lignes):
    """Chaque ligne dans un masque : la séquence d'entrée la fait monter (CSS, aucune dépendance au JavaScript)."""
    return ' '.join('<span class="l"><span>%s</span></span>' % x for x in lignes)


def _drapeau(nom):
    ab = ctx.CONFIG.get('ab') or {}
    return ab.get('actif') and nom in (ab.get('drapeaux') or {})


# Un masque par mot (les lignes se forment naturellement à toutes les largeurs ; la ponctuation reste avec son mot)
TITRES = {'a': ['Placo,', 'peinture,', 'acoustique :', 'la', 'rigueur', 'des', 'chantiers', 'publics'],
          'b': ['Du', 'Conservatoire', 'à', 'votre', 'salon :', 'placo,', 'acoustique,', 'peinture']}


def hero_titre():
    """Titre (cro-v3 §2.2 H1). Variantes du drapeau « hero-titre » : toutes dans le HTML, une seule affichée."""
    if not _drapeau('hero-titre'):
        return titre_lignes(TITRES['a'])
    return ''.join('<span data-flag="hero-titre" data-variant="%s">%s</span>' % (v, titre_lignes(TITRES[v])) for v in ('a', 'b'))


VIDEO = 'assets/video/hero-lissage-enduit'


def hero_media():
    """Photo réelle (témoin). Variante B du drapeau « hero-media » (inactif, visible en recette par ?flag=hero-media:b) :
    vidéo d'illustration sous licence, chargée par main.js seulement sur ordinateur, sans mouvement réduit ni économie de
    données ; son affiche est le LCP ; mention « Illustration » et bouton pause."""
    photo = hero_pic()
    if not _drapeau('hero-media'):
        return photo
    return ('<span class="hero__var" data-flag="hero-media" data-variant="a">%s</span>'
            '<span class="hero__var hero__video" data-flag="hero-media" data-variant="b" data-video="%s">'
            '<img src="%s-poster.webp" width="1280" height="720" alt="" loading="lazy" decoding="async">'
            '<span class="ill__tag">Illustration</span>'
            '<button type="button" class="hero__pause" aria-pressed="false" hidden>Mettre la vidéo en pause</button></span>'
            % (photo, VIDEO, VIDEO))


def hero(p):
    """Mobile : titre, phrase et boutons d'abord (premier écran de 390 × 844), puis la photo en bande, puis les badges.
    Ordinateur : la photo sort du flux et occupe les colonnes 8 à 12 jusqu'au bord droit (DA §5)."""
    texte = ('Régies, architectes, communes ou particuliers : nous venons voir, puis remettons une <b>offre écrite</b>%s.'
             % T('C06', ' détaillée', ''))
    return '''    <section class="hero" aria-labelledby="titre-page" data-suivi-zone="heros">
      <div class="container hero__grid">
        <div class="hero__panel">
          <h1 id="titre-page" class="hero__titre">%s</h1>
          <span class="laser" aria-hidden="true"></span>
          <p class="hero__text">%s</p>
          <div class="hero__actions" data-cta-principal>%s<a class="btn btn--light" href="%s" data-suivi-numero="fixe">Appeler le %s</a></div>
          <div class="hero__media">%s</div>
          %s
        </div>
      </div>
    </section>
''' % (hero_titre(), texte, devis_btn(p, 'heros'), TEL_URI, TEL, hero_media(),
       c.badges(['B1', 'B2', 'B3', '|B13|B6|B7|B8']))


# ---------------------------------------------------------------- H3 · prestations : 4 cartes illustrées (image 4:3)
SIZES_SVC = '(min-width: 1100px) 300px, (min-width: 640px) 45vw, 104px'


def svc_media(s):
    """Image d'une prestation (cro-v3 §2.2 H3) : vraie photo d'abord ; illustration signalée sinon ; pictogramme en dernier."""
    import illustrations
    if s == 'placo':
        return c.pic_crop('faux-plafond-placo-gorge-lumineuse-02', '16x9', SIZES_SVC, pf.alt('faux-plafond-placo-gorge-lumineuse-02'))
    if s == 'isolation-acoustique' and pf.photo_ok('panneaux-acoustiques-muraux-01'):
        return c.pic_crop('panneaux-acoustiques-muraux-01', '16x9', SIZES_SVC, pf.alt('panneaux-acoustiques-muraux-01'))
    if s == 'cloisons-isothermes' and definitif('C16'):
        return c.aa_pic('aa3', 'apres', SIZES_SVC, pf.PAIRE['aa3'][5])
    ident = {'peinture': 'peinture-rouleau-mur-blanc', 'isolation-acoustique': 'acoustique-panneaux-muraux',
             'cloisons-isothermes': 'isolation-ossature-metallique-plafond'}.get(s)
    return illustrations.pour_service(s, SIZES_SVC, ident=ident) or '<span class="svc__picto">%s</span>' % ICONS[s]


def carte_service(s, titre, phrase, lien):
    return ('<li class="svc"><a class="svc__link" href="%s"><span class="svc__media">%s</span>'
            '<span class="svc__titre">%s</span><span class="svc__txt">%s</span><span class="visually-hidden">%s</span></a></li>'
            % (svc_url(s), svc_media(s), titre, phrase, lien))


# ---------------------------------------------------------------- H4 · projets de référence : lieux nommés et avant / après
LIEUX = [
    # (id de référence, type, commune, photo rattachée (C25) ou None, ancre réalisations)
    ('conservatoire-musique-geneve', 'École de musique', 'Genève', None, None),
    ('alhambra', 'Salle de spectacle', 'Genève', 'chantier-salle-de-spectacle-01', 'projet-salle-de-spectacle'),
    ('plan-les-ouates', 'Collectivité', 'Plan-les-Ouates', 'chantier-ossature-puits-de-lumiere-02', 'projet-grande-salle-ossature'),
    ('head-geneve', 'Haute école d\'art et de design', 'Genève', None, None),
]


def carte_lieu(rid, typ, commune, photo, ancre, grand=False):
    nom = c.nom_ref(rid) if rid != 'alhambra' else 'Salle de l\'Alhambra'
    a_photo = photo and definitif('C25') and pf.photo_ok(photo) and (not ancre or ancre in pf.PROJ)
    if a_photo:
        media = c.pic_crop(photo, '16x9' if grand else '4x5', '(min-width: 1100px) %s, 100vw' % ('720px' if grand else '300px'), pf.alt(photo))
        corps = ('<span class="lieu__media">%s</span><span class="lieu__body"><span class="lieu__type">%s</span>'
                 '<span class="lieu__nom">%s</span><span class="lieu__commune">%s</span></span>' % (media, typ, c.insec(e(nom)), commune))
        inner = marque('C25', corps) if ctx.MODE == 'verification' else corps
        href = 'realisations.html#' + ancre if ancre else None
        el = ('<a class="lieu__link" href="%s">%s</a>' % (href, inner)) if href else inner
        return '<li class="lieu lieu--photo%s">%s</li>' % (' hcard--grand' if grand else '', el)
    return ('<li class="lieu lieu--typo"><span class="lieu__type">%s</span><span class="lieu__nom">%s</span>'
            '<span class="laser laser--court" aria-hidden="true"></span><span class="lieu__commune">%s</span></li>'
            % (typ, c.insec(e(nom)), commune))


def carte_avant_apres(grand):
    sz = '(min-width: 1100px) %s, 50vw' % ('360px' if grand else '160px')
    split = ('<span class="hcard__split"><span>%s<span class="hcard__lbl">Avant</span></span><span>%s<span class="hcard__lbl">Après</span></span></span>'
             % (c.aa_pic('aa6', 'avant', sz, pf.PAIRE['aa6'][4]), c.aa_pic('aa6', 'apres', sz, pf.PAIRE['aa6'][5])))
    tags = pf.tags_html(pf.paire_services('aa6'), 'C26' if not ctx.confirme('C26') else None)
    return '''<li class="hcard%s">
            <a class="hcard__link" href="realisations.html#avant-apres-aa6">
              <span class="hcard__media">%s</span>
              <span class="hcard__body"><span class="hcard__titre">Séjour : faux-plafond et spots</span><span class="hcard__lieu">Appartement, avant et après</span></span>
            </a>
            %s
          </li>''' % (' hcard--grand' if grand else '', split, tags)


def projets():
    """La grande carte revient au premier lieu qui a une vraie photo rattachée (C25), sinon à l'avant / après."""
    grand = next((x for x in LIEUX if x[3] and definitif('C25') and pf.photo_ok(x[3])), None)
    cartes = []
    if grand:
        cartes.append(carte_lieu(*grand, grand=True))
    else:
        cartes.append(carte_avant_apres(True))
    for x in LIEUX:
        if x is not grand:
            cartes.append(carte_lieu(*x))
    if grand:
        cartes.append(carte_avant_apres(False))
    return ''.join(cartes)


# ---------------------------------------------------------------- H6 · méthode (vraie séquence : numérotée)
def methode():
    etapes = [('Visite', 'Mesures et écoute, sur place.'),
              ('Offre écrite', T('C06', 'Poste par poste, <b>en CHF</b>.', 'Remise après la visite.')),
              ('Chantier protégé', T('C07', 'Sols et meubles couverts, <b>nettoyage chaque soir</b>.', 'Lieux protégés pendant les travaux.')),
              ('Réception', 'Le tour des finitions, <b>ensemble</b>.')]
    eng = T('C06', '<b>Aucun supplément</b> sans votre accord écrit et chiffré.', '')
    photo = 'habillage-placo-niches-arrondies-01'
    return '''    <section class="section" aria-labelledby="methode-titre">
      <div class="container methode">
        <figure class="methode__photo">%s<figcaption>%s</figcaption></figure>
        <div class="methode__texte">
          <h2 id="methode-titre">Un chantier en quatre étapes</h2>
          <ol class="steps steps--2">%s</ol>
          %s
          <a class="link-arrow" href="entreprise.html#methode">Notre méthode en détail</a>
        </div>
      </div>
    </section>
''' % (c.pic_crop(photo, '4x5', '(min-width: 1000px) 400px, 100vw', pf.alt(photo)), pf.legende(photo),
       ''.join('<li><h3>%s</h3><p>%s</p></li>' % x for x in etapes), ('<p class="engagement">%s</p>' % eng) if eng else '')


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
        carte_service('peinture', 'Peinture', 'Murs et plafonds intérieurs, <b>préparés puis peints</b>.', 'Voir la peinture'),
        carte_service('isolation-acoustique', 'Isolation acoustique', 'Vous entendez vos voisins ? Nous <b>isolons murs et plafonds</b>.', 'Voir l\'isolation acoustique'),
        carte_service('cloisons-isothermes', isol, 'Entre une <b>pièce chauffée</b> et une cave, un garage ou des combles.',
                      T('C16', 'Voir les cloisons isolantes', 'Voir les cloisons isothermes')),
    ])
    ref = doc('references')
    lien_pdf = ('<a class="link-arrow" href="%s" %s>Professionnels : dossier de références (%s)</a>' % (ref[0], suivi_doc('references'), ref[1])) if ref else ''
    flag_ordre = ' data-flag="ordre-sections"' if _drapeau('ordre-sections') else ''

    corps = hero(p) + c.mur_logos() + '''
    <section class="section" id="prestations" aria-labelledby="prestations-titre" data-ordre="prestations"%(flag)s>
      <div class="container">
        <div class="section-head">
          <h2 id="prestations-titre">Quatre métiers, souvent sur le même chantier</h2>
        </div>
        <ul class="svcs">%(services)s</ul>
      </div>
    </section>

    <section class="section section--mist" aria-labelledby="realisations-titre" data-ordre="realisations">
      <div class="container">
        <div class="section-head section-head--row">
          <h2 id="realisations-titre">Projets de référence</h2>
          <a class="link-arrow" href="realisations.html">Voir toutes les réalisations</a>
        </div>
        <ul class="lieux" data-reveal="cells">%(cartes)s</ul>
        <div class="section-foot">%(devis2)s%(pdf)s</div>
      </div>
    </section>
%(chiffres)s%(methode)s%(avis)s%(temoignages)s
    <section class="section faq" aria-labelledby="faq-titre">
      <div class="container split split--48">
        <div class="faq__head">
          <h2 id="faq-titre">Questions fréquentes</h2>
          <p>Une autre question ? Appelez le <a href="%(tel_uri)s" data-suivi-numero="fixe" data-suivi-emplacement="faq">%(tel)s</a>.</p>
        </div>
        <div class="faq__list">%(faq)s</div>
      </div>
    </section>
''' % dict(flag=flag_ordre, services=services, cartes=projets(), chiffres=c.chiffres(), methode=methode(),
           devis2=devis_btn(p, 'realisations', cls='btn', texte='Un projet semblable ? Demander un devis'), pdf=lien_pdf,
           avis=(('    <section class="section section--tight"><div class="container">%s</div></section>\n' % c.avis_ligne()) if c.avis_ligne() else ''),
           temoignages=c.temoignages(), tel_uri=TEL_URI, tel=TEL, faq=faq_html)
    # H9 : rappel des références (bande défilante) juste avant la demande, puis le bloc de demande (sans ligne de références)
    corps += c.bande_logos(cls='defile--avant-demande') + c.bloc_demande(p, refs=False, source='accueil')
    page(p, corps)
