# -*- coding: utf-8 -*-
"""Accueil (architecture §4.1, copy deck §B)."""
import os
import ctx
from ctx import e, T, V, definitif, marque, PROD
from common import (page, TEL, TEL_URI, devis_btn, horaires, svc_nom, svc_url, SERVICES, mail, LEGAL, IDE, STREET, MOB, AUJOURDHUI, doc, suivi_doc,
                    LINKEDIN, LOCALCH, GGE)
import composants as c
import portfolio as pf
from icons import ICONS

# v6 : en-tête au format des pages (texte à gauche, photo à droite) ; la photo est un diaporama des chantiers du client
DIAPOS = [
    # (photo, lieu, ouvrage, projet)
    ('salon-ovales-tissu-tendu-01', 'Salon', 'Îlots ovales en tissu tendu', 'projet-salon-ovales'),
    ('piscine-plafond-tendu-lumineux-01', 'Piscine intérieure', 'Plafond tendu et cercles lumineux', 'projet-piscine-plafond-tendu'),
    ('tissu-tendu-cadres-espace-vitre-01', 'Salle vitrée', 'Tissu tendu et cadres lumineux', 'projet-tissu-tendu-cadres'),
    ('restaurant-traitement-acoustique-01', 'Restaurant', 'Plafond traité en acoustique', 'projet-restaurant-acoustique'),
]
SZ_DIAPO = '(min-width: 1440px) 46vw, 42vw'


def diapo_pic(pid, premiere):
    """Ordinateur : photo entière (cadrée par object-position) ; mobile : recadrage 16:9."""
    it = c.MANIFEST[pid]
    b = it['base']
    larg = sorted({it['largeur_%d' % t] for t in (800, 1600, 2400) if it.get('largeur_%d' % t)})
    noms = {it['largeur_%d' % t]: t for t in (2400, 1600, 800) if it.get('largeur_%d' % t)}
    src_b = ', '.join('%s-%d.webp %dw' % (b, noms[w], w) for w in larg)
    b169 = c._srcset_crop(pid, '16x9')
    charge = 'fetchpriority="high"' if premiere else 'fetchpriority="low"'   # pas de chargement différé : la photo suivante est prête au fondu
    return ('<picture><source media="(min-width: 900px)" type="image/webp" srcset="%s" sizes="%s">'
            '<source type="image/webp" srcset="%s" sizes="100vw"><img src="%s-800.jpg" width="1600" height="900" alt="%s" %s decoding="async"></picture>'
            % (src_b, SZ_DIAPO, b169[0], b169[1], e(pf.alt(pid)), charge))


def diaporama():
    vues, pts = '', ''
    n = len(DIAPOS)
    for i, (pid, lieu, ouvrage, projet) in enumerate(DIAPOS):
        on = i == 0
        vues += ('<li class="diapo__vue%s" aria-roledescription="diapositive" aria-label="%d sur %d : %s"%s>%s'
                 '<a class="diapo__legende" href="realisations.html#%s"%s><span class="diapo__lieu">%s</span><span class="diapo__titre">%s</span></a></li>'
                 % (' is-on' if on else '', i + 1, n, e(lieu + ', ' + ouvrage), '' if on else ' aria-hidden="true"', diapo_pic(pid, on),
                    projet, '' if on else ' tabindex="-1"', e(lieu), e(ouvrage)))
        pts += ('<button type="button" class="diapo__pt%s" aria-label="Photo %d : %s"%s><span class="diapo__barre"></span></button>'
                % (' is-on' if on else '', i + 1, e(lieu), ' aria-current="true"' if on else ''))
    return ('<div class="diapo" data-diapo aria-roledescription="carrousel" aria-label="Nos chantiers en photos">'
            '<ul class="diapo__vues">%s</ul><div class="diapo__nav">%s</div>'
            '<p class="diapo__compte" aria-hidden="true"><span data-diapo-n>01</span> / %02d</p></div>' % (vues, pts, n))


def hero_preload():
    return c.hero_image('photo', DIAPOS[0][0])[1]


def business():
    """Entité unique « entreprise », décrite en entier sur l'accueil (architecture §11)."""
    zones = ['Canton de Genève', 'Canton de Vaud', 'Canton de Neuchâtel', 'Canton de Fribourg', 'Valais romand', 'Canton du Jura', 'Jura bernois']
    img = lambda pid: PROD + 'assets/img/portfolio/%s-1600.webp' % pid
    b = {
        '@type': 'HomeAndConstructionBusiness', '@id': PROD + '#entreprise', 'name': 'Andy Construct', 'legalName': LEGAL,
        'description': "Entreprise d'aménagement intérieur de Carouge (Genève), active depuis 2007 : isolation acoustique et phonique (spécialité), "
                       "faux plafonds, cloisons et doublages, panneaux sandwich isothermes, plâtrerie et peinture, dans toute la Suisse romande.",
        'url': PROD, 'logo': PROD + 'assets/img/brand/logo-andy-construct.png',
        'image': [img('salon-ovales-tissu-tendu-01'), img('piscine-plafond-tendu-lumineux-01'), img('restaurant-traitement-acoustique-01')],
        'telephone': TEL, 'email': mail(), 'foundingDate': '2007',
        'foundingLocation': {'@type': 'Place', 'name': 'Perly-Certoux'},
        'identifier': {'@type': 'PropertyValue', 'propertyID': 'IDE', 'value': IDE},
        'address': {'@type': 'PostalAddress', 'streetAddress': STREET, 'postalCode': '1227', 'addressLocality': 'Carouge',
                    'addressRegion': 'GE', 'addressCountry': 'CH'},
        'geo': {'@type': 'GeoCoordinates', 'latitude': 46.18935, 'longitude': 6.13236},
        'contactPoint': [{'@type': 'ContactPoint', 'telephone': TEL, 'contactType': 'customer service', 'areaServed': 'CH', 'availableLanguage': ['fr']},
                         {'@type': 'ContactPoint', 'telephone': MOB, 'contactType': 'sales', 'areaServed': 'CH', 'availableLanguage': ['fr']}],
        'areaServed': [{'@type': 'AdministrativeArea', 'name': z} for z in zones],
        'knowsAbout': ['Isolation acoustique', 'Isolation phonique', 'Correction acoustique', 'Tissu tendu', 'Faux plafonds',
                       'Cloisons en plaques de plâtre', 'Cloisons mobiles', 'Parois vitrées', 'Doublages', 'Panneaux sandwich isothermes',
                       'Plâtrerie', 'Peinture intérieure'],
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
TITRES = {'a': ['Acoustique,', 'plafonds,', 'cloisons :', 'la', 'rigueur', 'des', 'chantiers', 'publics'],
          'b': ['Du', 'Conservatoire', 'à', 'votre', 'salon :', 'acoustique,', 'plafonds,', 'cloisons']}


def hero_titre():
    """Titre (cro-v3 §2.2 H1). Variantes du drapeau « hero-titre » : toutes dans le HTML, une seule affichée."""
    if not _drapeau('hero-titre'):
        return titre_lignes(TITRES['a'])
    return ''.join('<span data-flag="hero-titre" data-variant="%s">%s</span>' % (v, titre_lignes(TITRES[v])) for v in ('a', 'b'))


def hero(p):
    """Héro v6 : même gabarit que les autres pages (panneau anthracite, image à droite jusqu'au bord), mêmes informations ;
    l'image est un diaporama des chantiers photographiés par l'entreprise (fondu, zoom lent, vignettes, glisser au doigt)."""
    texte = ('Régies, architectes, communes ou particuliers : nous venons voir, puis remettons une <b>offre écrite</b>%s.'
             % T('C06', ' détaillée', ''))
    return '''    <section class="hero hero--page hero--accueil" aria-labelledby="titre-page" data-suivi-zone="heros">
      <div class="container hero__grid">
        <div class="hero__panel">
          <p class="hero__slogan">L'expertise de l'aménagement intérieur</p>
          <h1 id="titre-page" class="hero__titre">%s</h1>
          <p class="hero__text">%s</p>
          <div class="hero__actions" data-cta-principal>%s<a class="btn btn--light" href="%s" data-suivi-numero="fixe">Appeler le %s</a></div>
          <div class="hero__media">%s</div>
          %s
        </div>
      </div>
    </section>
''' % (hero_titre(), texte, devis_btn(p, 'heros'), TEL_URI, TEL, diaporama(), c.badges(['B1', 'B2', 'B3'], cls='badges--3'))


# ---------------------------------------------------------------- H3 · prestations : 4 cartes illustrées (image 4:3)
SIZES_SVC = '(min-width: 1100px) 300px, (min-width: 640px) 45vw, 104px'


EXPERTISE = [
    ('isolation-acoustique', 'Isolation acoustique et phonique', 'Îlots acoustiques au plafond ou au mur, tissu tendu, cadres et baffles acoustiques, plafonds et cloisons phoniques.', True),
    ('cloisons', 'Cloisons et isolation thermique', 'Cloisons en plâtre, mobiles et aluminium, parois vitrées, doublages et panneaux sandwich isothermes.', False),
    ('faux-plafonds', 'Faux plafonds', 'Plafonds techniques et décoratifs pour l\'isolation acoustique et phonique : tissu tendu, plaque de plâtre, fibre minérale ou métal, isolant en fibre de bois.', False),
    ('platrerie-peinture', 'Plâtrerie et peinture', 'Plâtrerie, enduits, lissages et peinture intérieure pour des finitions nettes et durables.', False),
]
PHOTO_SVC = {'isolation-acoustique': ['baffles-acoustiques-eclairage-indirect-01'],
             'cloisons': ['piece-combles-platrerie-peinture-01'],
             'faux-plafonds': ['couloir-plafond-ligne-lumineuse-01'],
             'platrerie-peinture': ['combles-amenages-charpente-01']}


def svc_media(s):
    pid = next((x for x in PHOTO_SVC[s] if pf.photo_ok(x)), None)
    if pid:
        return c.pic_crop(pid, '16x9', SIZES_SVC, pf.alt(pid))
    ill = {'cloisons': 'chantier-cloisons-plaques-caissons'}.get(s)
    if ill:
        return c.media('ill', ill, SIZES_SVC)
    return '<span class="svc__picto">%s</span>' % ICONS[s]


def carte_service(s, titre, phrase, spec):
    return ('<li class="svc%s"><a class="svc__link" href="%s"><span class="svc__media">%s</span><span class="svc__body">%s'
            '<span class="svc__titre">%s</span><span class="svc__txt">%s</span><span class="svc__plus" aria-hidden="true">Découvrir</span></span></a></li>'
            % (' svc--spec' if spec else '', svc_url(s), svc_media(s), '<span class="tag-spec">Notre spécialité</span>' if spec else '', titre, phrase))


# ---------------------------------------------------------------- H4 · projets de référence
# v7 : les projets de référence défilent en continu (pause au survol et au focus ; à faire glisser sur mobile ;
# immobiles en mouvement réduit). La seconde copie de la piste assure la boucle et reste invisible aux lecteurs d'écran.
DEFILE_PROJETS = ['projet-salon-ovales', 'projet-piscine-plafond-tendu', 'projet-restaurant-acoustique', 'projet-combles-platrerie',
                  'projet-salle-reunion-cadres', 'projet-tissu-tendu-cadres', 'projet-panneaux-suspendus', 'projet-ilots-tissu-tendu',
                  'projet-couloir-ligne-lumineuse', 'projet-hall-gorge-lumineuse']


def projets():
    items = []
    for pid in DEFILE_PROJETS:
        x = pf.PROJ.get(pid)
        if not x or not pf.proj_ok(x):
            continue
        ph = pf.proj_photos(x)[0]
        items.append((pid, ph, pf._txt(x['lieu']), x['titre']))
    def piste(cache):
        return ''.join('<li class="pdefile__item"><a href="realisations.html#%s"%s><span class="pdefile__media">%s</span>'
                       '<span class="pdefile__txt"><span class="pdefile__lieu">%s</span><span class="pdefile__titre">%s</span></span></a></li>'
                       % (pid, ' tabindex="-1"' if cache else '', c.pic_crop(ph, '4x5', '(min-width: 1100px) 340px, 70vw', '' if cache else pf.alt(ph)),
                          e(lieu), e(titre)) for pid, ph, lieu, titre in items)
    return ('<div class="pdefile" data-pdefile><ul class="pdefile__piste">%s</ul><ul class="pdefile__piste pdefile__copie" aria-hidden="true">%s</ul></div>'
            % (piste(False), piste(True)))


# ---------------------------------------------------------------- H6 · méthode (vraie séquence : numérotée)
def methode():
    etapes = [('Visite', 'Mesures et écoute, sur place.'),
              ('Offre écrite', T('C06', 'Poste par poste, <b>en CHF</b>.', 'Remise après la visite.')),
              ('Chantier protégé', T('C07', 'Sols et meubles couverts, <b>nettoyage chaque soir</b>.', 'Lieux protégés pendant les travaux.')),
              ('Réception', 'Le tour des finitions, <b>ensemble</b>.')]
    eng = T('C06', '<b>Aucun supplément</b> sans votre accord écrit et chiffré.', '')
    photo = 'tracage-laser-plafond-01'
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
             title='Acoustique, faux plafonds, cloisons et peinture à Genève | Andy Construct',
             desc='L\'expertise de l\'aménagement intérieur : isolation acoustique, faux plafonds, cloisons, plâtrerie et peinture. Entreprise de Carouge depuis 2007, toute la Suisse romande.',
             og_title='Andy Construct · L\'expertise de l\'aménagement intérieur', preload=hero_preload())
    questions = faq()
    faq_html, faq_ld = c.faq_items(questions)
    p['ld'] = [{'@context': 'https://schema.org', '@graph': [
        business(),
        {'@type': 'WebSite', '@id': PROD + '#site', 'url': PROD, 'name': 'Andy Construct', 'inLanguage': 'fr-CH', 'publisher': {'@id': PROD + '#entreprise'}},
        {'@type': 'WebPage', '@id': PROD + '#page', 'url': PROD, 'name': p['title'], 'inLanguage': 'fr-CH',
         'isPartOf': {'@id': PROD + '#site'}, 'about': {'@id': PROD + '#entreprise'}}]},
        c.faq_ld(PROD, faq_ld)]

    services = ''.join(carte_service(*x) for x in EXPERTISE)
    ref = doc('references')
    lien_pdf = ('<a class="link-arrow" href="%s" %s>Professionnels : dossier de références (%s)</a>' % (ref[0], suivi_doc('references'), ref[1])) if ref else ''
    flag_ordre = ' data-flag="ordre-sections"' if _drapeau('ordre-sections') else ''

    corps = hero(p) + c.mur_logos() + '''
    <section class="section" id="prestations" aria-labelledby="prestations-titre" data-ordre="prestations"%(flag)s>
      <div class="container">
        <div class="section-head">
          <p class="surtitre">Nos domaines d'expertise</p>
          <h2 id="prestations-titre">Quatre savoir-faire, une même expertise</h2>
          <p class="lead">Des travaux réalisés selon les normes suisses <b>SIA</b> et les prescriptions de protection incendie <b>AEAI</b>.</p>
        </div>
        <ul class="svcs svcs--v5">%(services)s</ul>
      </div>
    </section>

    <section class="section section--mist" aria-labelledby="realisations-titre" data-ordre="realisations">
      <div class="container">
        <div class="section-head section-head--row">
          <h2 id="realisations-titre">Projets de référence</h2>
          <a class="link-arrow" href="realisations.html">Voir toutes les réalisations</a>
        </div>
      </div>
      %(cartes)s
      <div class="container">
        <div class="section-foot">%(devis2)s%(pdf)s</div>
      </div>
    </section>
%(chiffres)s%(normes)s%(methode)s%(avis)s%(temoignages)s
    <section class="section faq" aria-labelledby="faq-titre">
      <div class="container split split--48">
        <div class="faq__head">
          <h2 id="faq-titre">Questions fréquentes</h2>
          <p>Une autre question ? Appelez le <a href="%(tel_uri)s" data-suivi-numero="fixe" data-suivi-emplacement="faq">%(tel)s</a>.</p>
        </div>
        <div class="faq__list">%(faq)s</div>
      </div>
    </section>
''' % dict(flag=flag_ordre, services=services, cartes=projets(), chiffres=c.chiffres(h2='Un partenaire pour vos projets en Suisse romande', surtitre='Des solutions adaptées à chaque projet'),
           normes=__import__('page_services').normes_table(), methode=methode(),
           devis2=devis_btn(p, 'realisations', cls='btn', texte='Un projet semblable ? Demander un devis'), pdf=lien_pdf,
           avis=(('    <section class="section section--tight"><div class="container">%s</div></section>\n' % c.avis_ligne()) if c.avis_ligne() else ''),
           temoignages=c.temoignages(), tel_uri=TEL_URI, tel=TEL, faq=faq_html)
    # v6 : plus de bande de logos avant la demande (doublon avec le pied de page)
    corps += c.bloc_demande(p, refs=False, source='accueil')
    page(p, corps)
