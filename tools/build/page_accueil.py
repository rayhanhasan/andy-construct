# -*- coding: utf-8 -*-
"""Accueil (architecture §4.1, copy deck §B)."""
import ctx
from ctx import e, T, V, definitif, marque, PROD
from common import (page, TEL, TEL_URI, devis_btn, horaires, svc_nom, svc_url, SERVICES, mail, LEGAL, IDE, STREET, MOB,
                    LINKEDIN, LOCALCH, GGE)
import composants as c
import portfolio as pf
from icons import ICONS

HERO = 'faux-plafond-placo-gorge-lumineuse-01'
H = 'assets/img/portfolio/' + HERO


def hero_preload():
    return ('  <link rel="preload" as="image" type="image/webp" fetchpriority="high" imagesrcset="%s-portrait-600.webp 600w, %s-portrait-900.webp 900w" imagesizes="100vw" media="(max-width: 699.98px)">\n'
            '  <link rel="preload" as="image" type="image/webp" fetchpriority="high" imagesrcset="%s-800.webp 800w, %s-1200.webp 1200w, %s-1600.webp 1600w" imagesizes="100vw" media="(min-width: 700px)">\n'
            % (H, H, H, H, H))


def hero_pic():
    return ('<picture><source media="(max-width: 699.98px)" type="image/webp" srcset="%s-portrait-600.webp 600w, %s-portrait-900.webp 900w" sizes="100vw">'
            '<source type="image/webp" srcset="%s-800.webp 800w, %s-1200.webp 1200w, %s-1600.webp 1600w" sizes="100vw">'
            '<img src="%s-800.jpg" width="1600" height="1200" alt="%s" fetchpriority="high"></picture>'
            % (H, H, H, H, H, H, e(pf.alt(HERO))))


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
                       'Isolation acoustique', 'Isolation phonique', 'Correction acoustique', 'Cloisons isolantes', 'Cloisons isothermes'],
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


def carte_service(s, titre, phrase, pour, lien):
    return ('<li class="service"><span class="service__icon">%s</span><h3>%s</h3><p>%s</p><p class="service__pour">%s</p>'
            '<a class="link-arrow service__link" href="%s">%s</a></li>' % (ICONS[s], titre, phrase, pour, svc_url(s), lien))


def carte_accueil(href, img, titre, lieu, contrainte, tags, badge=False):
    return '''<li class="hcard">
            <a class="hcard__link" href="%s">
              <span class="hcard__media">%s%s</span>
              <span class="hcard__body"><span class="hcard__titre">%s</span><span class="hcard__lieu">%s</span><span class="hcard__txt">%s</span></span>
            </a>
            %s
          </li>''' % (href, img, '<span class="badge">Pendant les travaux</span>' if badge else '', titre, lieu, contrainte, tags)


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

    h = horaires()
    fait3 = (marque('C02', '<strong>Visite et devis gratuits</strong><span>Offre écrite, sans engagement</span>') if definitif('C02')
             else '<strong>Particuliers et professionnels</strong><span>Régies, architectes, communes</span>')
    hero = '''    <section class="hero" aria-labelledby="titre-page" data-suivi-zone="heros">
      <div class="hero__media">%s</div>
      <div class="container hero__inner">
        <div class="hero__content">
          <p class="eyebrow">Carouge · depuis 2007</p>
          <h1 id="titre-page">Placo, peinture et isolation en Suisse romande</h1>
          <p class="hero__text">%s</p>
          <div class="hero__actions">%s<a class="btn btn--light" href="%s" data-suivi-numero="fixe">Appeler le %s</a></div>%s
        </div>
        <ul class="hero__facts" aria-label="En bref">
          <li><strong>Depuis 2007</strong><span>Inscrite au registre du commerce</span></li>
          <li><strong>Siège à Carouge</strong><span>Chantiers dans toute la Suisse romande</span></li>
          <li>%s</li>
        </ul>
      </div>
    </section>
''' % (hero_pic(),
       T('C05', 'Cloisons, plafonds, isolation contre le bruit et peinture : un seul interlocuteur, de la pose des plaques à la dernière couche.',
         'Cloisons, plafonds, isolation contre le bruit et peinture, pour les particuliers et les professionnels.'),
       devis_btn(p, 'heros'), TEL_URI, TEL,
       ('\n          <p class="hero__hours">%s</p>' % T('C03', 'Du lundi au vendredi, de 7 h à 18 h.', '')) if definitif('C03') else '',
       fait3)

    isol = svc_nom('cloisons-isothermes')
    services = ''.join([
        carte_service('placo', 'Placo', 'Cloisons, doublages et faux-plafonds en plaques de plâtre.', 'Pour : logements, bureaux, commerces, salles.', 'Voir le placo'),
        carte_service('peinture', 'Peinture', 'Murs et plafonds préparés, peints, et la pièce rendue propre.', 'Pour : appartements, fins de bail, cages d\'escalier, bureaux.', 'Voir la peinture'),
        carte_service('isolation-acoustique', 'Isolation acoustique', 'Vous entendez vos voisins ? Nous isolons murs et plafonds.', 'Pour : logements, bureaux, salles communales.', 'Voir l\'isolation acoustique'),
        carte_service('cloisons-isothermes', isol, 'Une pièce froide contre un garage ou une cave ? Nous l\'isolons.', 'Pour : villas, immeubles, locaux d\'activité.',
                      T('C16', 'Voir les cloisons isolantes', 'Voir les cloisons isothermes')),
    ])

    # Réalisations : P1 (photo n° 9, l'héro montre déjà la n° 6), P2, AA6 (qualité vérifiée)
    sizes = '(min-width: 1100px) 360px, (min-width: 700px) 45vw, 100vw'
    p1, p2 = pf.PROJ['projet-hall-gorge-lumineuse'], pf.PROJ['projet-grande-salle-ossature']
    c1 = carte_accueil('realisations.html#' + p1['id'], c.pic('faux-plafond-placo-gorge-lumineuse-02', sizes, pf.alt('faux-plafond-placo-gorge-lumineuse-02')),
                       p1['titre'], pf._txt(p1['lieu']), pf._txt(p1['contrainte']),
                       pf.tags_html(pf.proj_tags(p1), 'C25' if not ctx.confirme('C25') else None))
    ph2 = pf.proj_photos(p2)[0]
    c2 = carte_accueil('realisations.html#' + p2['id'], c.pic(ph2, sizes, pf.alt(ph2)), p2['titre'], pf._txt(p2['lieu']),
                       pf._txt(p2['contrainte']), pf.tags_html(pf.proj_tags(p2), 'C25' if not ctx.confirme('C25') else None), badge=True)
    split = ('<span class="hcard__split"><span>%s<span class="hcard__lbl">Avant</span></span><span>%s<span class="hcard__lbl">Après</span></span></span>'
             % (c.aa_pic('aa6', 'avant', '(min-width: 1100px) 180px, 50vw', pf.PAIRE['aa6'][4]),
                c.aa_pic('aa6', 'apres', '(min-width: 1100px) 180px, 50vw', pf.PAIRE['aa6'][5])))
    c3 = carte_accueil('realisations.html#avant-apres-aa6', split, 'Séjour : faux-plafond et spots, avant et après',
                       T('C26', 'Appartement', 'Appartement'), T('C26', 'Un plafond redessiné, l\'éclairage intégré.', 'Un plafond redessiné, l\'éclairage intégré.'),
                       pf.tags_html(pf.paire_services('aa6'), 'C26' if not ctx.confirme('C26') else None))

    corps = hero + c.refs_bandeau(p) + '''
    <section class="section" id="prestations" aria-labelledby="prestations-titre">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">Nos quatre métiers</p>
          <h2 id="prestations-titre">Quatre métiers, souvent sur le même chantier</h2>
        </div>
        <ul class="services">%(services)s</ul>
        <div class="section-foot"><p>Vous hésitez ? Décrivez votre besoin : nous vous orientons.</p>%(devis1)s</div>
      </div>
    </section>

    <section class="section section--mist" aria-labelledby="realisations-titre">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">Réalisations</p>
          <h2 id="realisations-titre">Des chantiers réels, photographiés par notre équipe</h2>
        </div>
        <ul class="hcards">%(cartes)s</ul>
        <div class="section-foot"><a class="link-arrow" href="realisations.html">Voir toutes les réalisations</a>%(devis2)s</div>
      </div>
    </section>

    <section class="section" aria-labelledby="methode-titre">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">Comment nous travaillons</p>
          <h2 id="methode-titre">De la visite à la réception, quatre étapes</h2>
        </div>
        %(methode)s
        <p class="section-foot"><a class="link-arrow" href="entreprise.html#methode">Notre méthode en détail</a></p>
      </div>
    </section>
%(temoignages)s
    <section class="section section--mist section--tight" aria-label="Professionnels et zone d'intervention">
      <div class="container duo">
        <div class="duo__item">
          <h3>Régies, architectes, communes</h3>
          <p>Immeubles habités, offres sur plans et descriptifs, dossier de références à télécharger.</p>
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
          <p class="eyebrow">Vos questions</p>
          <h2 id="faq-titre">Questions fréquentes</h2>
          <p>Une autre question ? Appelez le <a href="%(tel_uri)s" data-suivi-numero="fixe" data-suivi-emplacement="faq">%(tel)s</a>.</p>
        </div>
        <div class="faq__list">%(faq)s</div>
      </div>
    </section>
''' % dict(services=services, devis1=devis_btn(p, 'prestations'), cartes=c1 + c2 + c3,
           devis2=devis_btn(p, 'realisations', texte='Un projet semblable ? Demander un devis'),
           methode=c.methode(True), temoignages=c.temoignages(), tel_uri=TEL_URI, tel=TEL, faq=faq_html)
    # Exposition 3 : ligne de références près du formulaire (remplacée par les témoignages quand ils existent)
    corps += c.bloc_demande(p, refs=not ctx.TEMOIGNAGES, source='accueil')
    page(p, corps)
