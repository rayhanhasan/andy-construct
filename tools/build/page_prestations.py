# -*- coding: utf-8 -*-
"""Prestations : structure H2/H3 et ancres du brief SEO §3.2."""
from common import *

TITLE = 'Plafond tendu, acoustique, cloison à Genève | Andy Construct'
DESC = "Plafonds tendus et acoustiques, placoplâtre, fibre, métal ; cloisons légères et mobiles ; isolation, chape flottante, protection incendie. Genève et Vaud."

SIZES = '(min-width: 1000px) 360px, (min-width: 760px) 40vw, 100vw'


def item(anchor, title, desc, uses, benef, attention, photo, cat, travaux, note=''):
    return dict(anchor=anchor, title=title, desc=desc, uses=uses, benef=benef, attention=attention,
                photo=photo, cat=cat, travaux=travaux, note=note)


PLAFONDS = [
    item('plafonds-tendus', 'Plafonds en tissu tendu à froid',
         "Une toile en tissu est fixée sur des profilés posés au pourtour de la pièce, puis mise en tension sans chauffage, contrairement aux membranes en PVC posées à chaud. Le résultat est un plafond parfaitement lisse, posé proprement, souvent sans déposer l'ancien plafond. La toile accepte spots, caissons lumineux et puits de lumière.",
         ['Logements, même habités', 'Salles communales et de conférence', 'Restaurants et commerces', 'Bâtiments anciens à poutres apparentes'],
         ['Surface lisse, sans fissure ni joint visible', 'Pose rapide, très peu de poussière', "Rénovation sans démolir l'ancien plafond", 'Éclairage intégré possible'],
         "le choix de la toile (aspect, acoustique, comportement au feu) dépend de l'usage du local, et les réservations pour l'éclairage se prévoient avant la pose.",
         'plafond-tendu-poutres-apparentes-01', 'plafonds-tendus', 'plafond-tendu'),
    item('plafonds-acoustiques', 'Plafonds phoniques et acoustiques',
         "Dans une salle de réunion, une classe ou un restaurant, l'écho fatigue et gêne la conversation. Un plafond acoustique absorbe une partie du son et réduit la réverbération. Un plafond phonique, associé à une isolation, limite en plus la transmission du bruit entre deux locaux.",
         ['Salles de réunion et bureaux', 'Écoles, conservatoires, salles de musique', 'Restaurants et cantines', 'Salles communales et polyvalentes'],
         ['Meilleure compréhension de la parole', "Moins d'écho et moins de fatigue", 'Finitions variées : dalles, panneaux, plâtre perforé', 'Compatible avec l\'éclairage et la ventilation'],
         "un plafond absorbant réduit l'écho dans la pièce, pas forcément le bruit qui vient d'un autre logement. Pour cela, il faut une isolation phonique (voir plus bas).",
         'panneaux-acoustiques-muraux-01', 'plafonds-acoustiques', 'plafond-acoustique'),
    item('plafonds-placoplatre', 'Plafonds en plaques de plâtre (placoplâtre)',
         "Le faux-plafond en plaques de plâtre est vissé sur une ossature métallique, puis les joints sont enduits et le plafond est peint. Il permet toutes les formes : plafonds plats, retombées, gorges lumineuses, îlots arrondis. Il cache les gaines techniques et reçoit l'isolation nécessaire.",
         ["Halls d'entrée et couloirs", 'Logements et bureaux', 'Locaux commerciaux', "Cages d'escalier"],
         ['Formes libres : courbes, caissons, gorges lumineuses', 'Passage discret des gaines et des câbles', 'Isolation thermique ou phonique intégrée', "Plaques résistantes au feu ou à l'humidité"],
         "les joints sont enduits puis poncés avant peinture : le local doit être protégé. Les trappes de visite se placent dès la conception.",
         'faux-plafond-placo-gorge-lumineuse-01', 'plafonds-placo', 'faux-plafond'),
    item('plafonds-fibre', 'Plafonds en fibre de bois et en fibre minérale',
         "Deux familles de panneaux posés apparents. La fibre de bois agglomérée allie une bonne correction acoustique à un aspect chaleureux et résiste bien aux chocs. La fibre minérale, en dalles sur ossature apparente, est la solution économique et démontable des bureaux et des bâtiments publics : chaque dalle se retire pour accéder aux installations.",
         ['Bureaux et couloirs', 'Écoles, crèches, salles de sport', 'Cabinets médicaux et laboratoires', 'Parkings et locaux techniques'],
         ['Bonne correction acoustique', 'Accès facile aux installations (dalles)', "Remplacement d'une dalle à l'unité", 'Aspect naturel pour la fibre de bois'],
         "les dalles minérales supportent mal l'humidité et les chocs ; dans ces locaux, nous proposons la fibre de bois ou le métal.",
         'plafond-dalles-couloir-01', 'plafonds-acoustiques', 'faux-plafond',
         'PROVISOIRE : à valider avec le client (matériau exact des dalles de la photo ; photo de fibre de bois à fournir)'),
    item('plafonds-metalliques', 'Plafonds en bacs métalliques',
         "Bacs ou lames en acier ou en aluminium laqué : un plafond résistant, lavable et démontable, adapté aux locaux très fréquentés ou soumis à des exigences d'hygiène.",
         ['Cuisines professionnelles', 'Laboratoires', 'Halls et zones de passage', 'Sanitaires'],
         ["Surface lavable, adaptée à l'hygiène", "Démontable pour l'entretien", 'Perforations acoustiques possibles', 'Longue durée de vie'],
         "le type de perforation et le voile acoustique se choisissent selon l'écho à corriger dans le local.",
         'plafond-bacs-metalliques-cuisine-01', 'plafonds-metalliques', 'faux-plafond'),
    item('cadres-acoustiques', 'Cadres acoustiques',
         "Un cadre en aluminium tendu d'une toile imprimée, avec un absorbant au dos. Il corrige l'acoustique d'une salle tout en servant de décor : paysage, photo, motif ou couleur unie.",
         ['Salles de réunion', 'Accueils et réceptions', 'Restaurants', 'Bureaux ouverts'],
         ['Correction acoustique sans gros travaux', 'Impression sur mesure', 'Pose murale ou suspendue', 'Toile remplaçable'],
         "l'image doit être fournie en haute définition ; nous vous indiquons le format exact à prévoir.",
         'cadre-acoustique-salle-de-reunion-01', 'plafonds-acoustiques', 'cadres-acoustiques'),
]

CLOISONS = [
    item('cloisons-placoplatre', 'Cloisons légères en plaques de plâtre',
         "Montées sur ossature métallique, les cloisons en plaques de plâtre redistribuent un logement ou un étage de bureaux sans maçonnerie. Selon le nombre de plaques et l'isolant choisis, elles isolent du bruit ou résistent au feu. Les mêmes plaques servent aux habillages et aux doublages.",
         ['Aménagement de bureaux', 'Rénovation de logements', 'Locaux techniques', 'Habillages et niches sur mesure'],
         ['Pose rapide, sans temps de séchage de maçonnerie', "Isolation phonique selon l'épaisseur", "Versions résistantes au feu ou à l'humidité", 'Surface prête à peindre'],
         "les performances phoniques et coupe-feu dépendent de la composition de la cloison et de ses raccords : elles sont précisées dans l'offre.",
         'habillage-placo-niches-arrondies-01', 'cloisons', 'cloisons'),
    item('cloisons-mobiles', 'Cloisons mobiles en aluminium',
         "Les cloisons démontables à cadre en aluminium, pleines ou vitrées, suivent l'évolution de vos bureaux. Elles se démontent et se remontent quand l'organisation change.",
         ['Bureaux et plateaux ouverts', 'Salles de réunion', 'Cabinets et agences'],
         ['Espaces modulables et réutilisables', 'Vitrages avec stores intégrés possibles', 'Lumière naturelle préservée', 'Chantier court, possible en site occupé'],
         "les passages de l'électricité et de la ventilation se coordonnent avec les autres corps de métier avant la pose.",
         'cloisons-modulaires-vitrees-01', 'cloisons', 'cloisons',
         'PROVISOIRE : à valider avec le client (système exact des cloisons de la photo)'),
]


def ticks(items):
    return '<ul class="ticks">' + ''.join('<li>%s</li>' % i for i in items) + '</ul>'


def render_item(it):
    media = ''
    if it['photo']:
        m = BY[it['photo']]
        media = '''
              <figure class="svc__media">
                <span class="media">%s</span>
                <figcaption class="caption">%s</figcaption>
              </figure>''' % (pic(it['photo'], SIZES), e(m['titre']))
    note = ('\n            <!-- %s -->' % it['note']) if it['note'] else ''
    return '''
          <article class="svc" id="%(a)s" aria-labelledby="%(a)s-titre">%(note)s
            <div class="svc__grid%(g)s">
              <div>
                <h3 class="svc__title" id="%(a)s-titre">%(t)s</h3>
                <p>%(d)s</p>
                <div class="svc__cols">
                  <div><h4 class="label">Pour quels locaux</h4>%(u)s</div>
                  <div><h4 class="label">Avantages</h4>%(b)s</div>
                </div>
                <p class="svc__note"><strong>Point d'attention :</strong> %(att)s</p>
                <p class="svc__links">
                  <a class="link-arrow" href="realisations.html?categorie=%(cat)s">Voir des réalisations</a>
                  <a class="link-arrow" href="contact.html?travaux=%(tr)s#devis">Demander une offre</a>
                </p>
              </div>%(m)s
            </div>
          </article>''' % dict(a=it['anchor'], note=note, g='' if it['photo'] else ' svc__grid--text', t=it['title'],
                               d=it['desc'], u=ticks(it['uses']), b=ticks(it['benef']), att=it['attention'],
                               cat=it['cat'], tr=it['travaux'], m=media)


def group(gid, title, intro, inner, eyebrow):
    return '''
        <section class="svc-group" id="%(g)s" aria-labelledby="%(g)s-titre">
          <div class="svc-group__head">
            <p class="eyebrow">%(eb)s</p>
            <h2 id="%(g)s-titre">%(t)s</h2>
            <p class="lead">%(i)s</p>
          </div>%(inner)s
        </section>''' % dict(g=gid, t=title, i=intro, inner=inner, eb=eyebrow)


def figure(pid):
    m = BY[pid]
    return '''
              <figure class="svc__media">
                <span class="media">%s</span>
                <figcaption class="caption">%s</figcaption>
              </figure>''' % (pic(pid, SIZES), e(m['titre']))


def build():
    h = head(TITLE, DESC, 'prestations.html', ld=[page_ld('prestations.html', TITLE, 'Prestations')])

    plafonds = group('plafonds', 'Plafonds', "Six familles de plafonds, du plus décoratif au plus technique. Nous vous conseillons celle qui convient à l'usage du local.",
                     ''.join(render_item(i) for i in PLAFONDS), 'Six systèmes')
    cloisons = group('cloisons', 'Cloisons', "Des cloisons fixes ou démontables pour créer, redistribuer ou isoler des espaces, sans maçonnerie.",
                     ''.join(render_item(i) for i in CLOISONS), 'Fixes ou démontables')

    isolation_inner = '''
          <div class="svc svc--flat">
            <div class="svc__grid">
              <div class="svc__subs">
                <div id="isolation-phonique">
                  <h3 class="svc__title">Isolation phonique</h3>
                  <p>Faux-plafond désolidarisé avec isolant, cloisons à double ossature, doublages : pour limiter les bruits aériens (voix, musique, télévision) entre deux locaux ou deux logements.</p>
                </div>
                <div id="isolation-thermique">
                  <h3 class="svc__title">Isolation thermique intérieure</h3>
                  <p>Isolant posé sous une dalle froide, dans les combles ou en doublage des murs : moins de pertes de chaleur et plus de confort en été. Certaines mesures peuvent être subventionnées (programme GEnergie, Programme Bâtiments) ; la demande se dépose avant le début des travaux.</p>
                </div>
                <div id="chape-flottante">
                  <h3 class="svc__title">Chape flottante contre les bruits d'impact</h3>
                  <p>Posée sur une couche isolante souple, sans contact rigide avec la dalle ni avec les murs, la chape flottante réduit les bruits de pas et de chocs transmis aux locaux du dessous. Elle se prévoit lors d'une rénovation de sol ou d'une construction.</p>
                </div>
                <p class="svc__links">
                  <a class="link-arrow" href="realisations.html?categorie=chantier">Voir des chantiers en cours</a>
                  <a class="link-arrow" href="contact.html?travaux=isolation#devis">Demander une offre</a>
                </p>
              </div>%s
            </div>
          </div>''' % figure('chantier-ossature-puits-de-lumiere-02')
    isolation = group('isolation', 'Isolation thermique et phonique',
                      "Nous posons l'isolant dans les faux-plafonds, les cloisons et les doublages. Bien choisi et bien posé, il réduit les pertes de chaleur et limite le bruit.",
                      isolation_inner, 'Chaleur et bruit')

    incendie_inner = '''
          <!-- PROVISOIRE : à valider avec le client (types d'ouvrages coupe-feu réalisés ; aucune certification revendiquée) -->
          <div class="svc svc--flat">
            <div class="svc__grid svc__grid--text">
              <div>
                <p>Nous posons des plafonds, des cloisons et des habillages de protection incendie, par exemple autour des structures ou dans les voies d'évacuation. La résistance au feu exigée (par exemple EI 30) est fixée par le concept de protection incendie du bâtiment, selon les prescriptions de l'AEAI, et le système posé doit y correspondre.</p>
                %s
                <p class="svc__links"><a class="link-arrow" href="contact.html?travaux=protection-incendie#devis">Demander une offre</a></p>
              </div>
            </div>
          </div>''' % ticks(['Plafonds et cloisons résistants au feu', 'Habillage de gaines et de structures', 'Mise en œuvre selon les fiches techniques des fabricants', 'Niveau demandé à indiquer dès la demande d\'offre'])
    incendie = group('protection-incendie', 'Protection incendie',
                     "Des ouvrages coupe-feu posés selon les exigences définies pour le projet.", incendie_inner, 'Sécurité')

    integ_inner = '''
          <div class="svc svc--flat">
            <div class="svc__grid">
              <div>
                <ul class="svc__extra svc__extra--stack">
                  <li><h3>Caissons lumineux</h3><p>Éclairage intégré au plafond, en lumière directe ou indirecte (gorge lumineuse, îlots, plafonds rétroéclairés).</p></li>
                  <li><h3>Trappes de visite</h3><p>Accès discret aux vannes, gaines et installations techniques, dans la finition du plafond.</p></li>
                  <li><h3>Puits de lumière</h3><p>Ouverture dans le faux-plafond pour faire entrer la lumière naturelle d'une verrière ou d'un lanterneau.</p></li>
                </ul>
                <p class="svc__links">
                  <a class="link-arrow" href="realisations.html?categorie=plafonds-tendus">Voir des plafonds lumineux</a>
                  <a class="link-arrow" href="contact.html?travaux=faux-plafond#devis">Demander une offre</a>
                </p>
              </div>%s
            </div>
          </div>''' % figure('plafond-tendu-puits-de-lumiere-01')
    integ = group('integrations', 'Intégrations au plafond',
                  "Autour du plafond, nous réalisons aussi les éléments qui font un ouvrage complet. Les réservations se prévoient avec votre électricien.",
                  integ_inner, 'Autour du plafond')

    peinture_inner = '''
          <!-- PROVISOIRE : à valider avec le client (périmètre exact de l'offre peinture ; photos à fournir) -->
          <div class="svc svc--flat">
            <div class="svc__grid svc__grid--text">
              <div>
                <p>Pour vous livrer des pièces terminées, nous préparons les supports, réalisons les enduits et les bandes, puis peignons plafonds et murs. Un seul intervenant, du plafond à la finition.</p>
                <div class="svc__cols">
                  <div><h3 class="label">Pour quels locaux</h3>%s</div>
                  <div><h3 class="label">Avantages</h3>%s</div>
                </div>
                <p class="svc__links"><a class="link-arrow" href="contact.html?travaux=peinture#devis">Demander une offre</a></p>
              </div>
            </div>
          </div>''' % (ticks(['Plafonds et murs après pose', 'Rénovation de logements', 'Bureaux et commerces']),
                       ticks(['Un seul intervenant', 'Préparation soignée des supports', "Peintures adaptées à l'usage des locaux"]))
    peinture = group('peinture', 'Peinture intérieure', "La finition fait partie du travail.", peinture_inner, 'Finitions')

    deroulement_inner = '''
          <!-- PROVISOIRE : à valider avec le client (déroulé d'un chantier) -->
          <ol class="steps steps--6">
            <li><h3>Visite</h3><p>Relevé des mesures et des contraintes du local, écoute de vos besoins.</p></li>
            <li><h3>Offre écrite</h3><p>Détaillée poste par poste, en CHF, avec la durée prévue.</p></li>
            <li><h3>Planning</h3><p>Dates convenues avec vous et coordination avec les autres corps de métier.</p></li>
            <li><h3>Protection des lieux</h3><p>Sols, mobilier et accès protégés avant le début des travaux.</p></li>
            <li><h3>Nettoyage</h3><p>Évacuation des déchets et nettoyage en fin de chantier.</p></li>
            <li><h3>Réception</h3><p>Contrôle des finitions avec vous, puis remise de l'ouvrage.</p></li>
          </ol>'''
    deroulement = group('deroulement', 'Comment se déroule un chantier',
                        "Six étapes, toujours dans le même ordre, pour savoir à quoi vous attendre.", deroulement_inner, 'Méthode')

    toc_items = [('plafonds', 'Plafonds', [('plafonds-tendus', 'Tissu tendu à froid'), ('plafonds-acoustiques', 'Phoniques et acoustiques'),
                                           ('plafonds-placoplatre', 'Plaques de plâtre'), ('plafonds-fibre', 'Fibre de bois et minérale'),
                                           ('plafonds-metalliques', 'Bacs métalliques'), ('cadres-acoustiques', 'Cadres acoustiques')]),
                 ('cloisons', 'Cloisons', [('cloisons-placoplatre', 'Plaques de plâtre'), ('cloisons-mobiles', 'Mobiles en aluminium')]),
                 ('isolation', 'Isolation et chape flottante', []),
                 ('protection-incendie', 'Protection incendie', []),
                 ('integrations', 'Intégrations au plafond', []),
                 ('peinture', 'Peinture intérieure', []),
                 ('deroulement', 'Déroulement d\'un chantier', []),
                 ('normes', 'Normes et qualité', [])]
    toc = ''
    for a, t, subs in toc_items:
        sub = ''
        if subs:
            sub = '<ol>' + ''.join('<li><a href="#%s">%s</a></li>' % s for s in subs) + '</ol>'
        toc += '<li><a href="#%s">%s</a>%s</li>' % (a, t, sub)

    body = '''
  <main id="contenu">
%(ph)s
    <div class="section section--flush">
      <div class="container svc-layout">
        <nav class="toc" aria-label="Sommaire des prestations">
          <p class="label">Sur cette page</p>
          <ol>%(toc)s</ol>
        </nav>
        <div class="svc-main">%(groups)s
        </div>
      </div>
    </div>

    <section class="section section--mist" id="normes" aria-labelledby="normes-titre">
      <div class="container">
        <div class="section-head section-head--split">
          <div>
            <p class="eyebrow">Qualité</p>
            <h2 id="normes-titre">Normes et qualité</h2>
          </div>
          <p class="lead">Nos travaux suivent les règles de l'art et les normes suisses applicables à chaque ouvrage. Les performances visées sont celles définies pour le projet et précisées dans l'offre.</p>
        </div>
        <!-- PROVISOIRE : à valider avec le client (références normatives, attestations disponibles ; aucune certification n'est revendiquée) -->
        <div class="norms">
          <article>
            <h3>Protection incendie</h3>
            <p>Les plafonds, cloisons et habillages coupe-feu sont mis en œuvre selon les prescriptions de protection incendie de l'AEAI, avec des systèmes dont la classification est attestée par le fabricant.</p>
          </article>
          <article>
            <h3>Acoustique</h3>
            <p>Pour l'isolation phonique entre locaux, nous nous référons à la norme SIA 181 « Protection contre le bruit dans le bâtiment », selon les exigences définies pour le projet.</p>
          </article>
          <article>
            <h3>Exécution et réception</h3>
            <p>Sauf accord contraire, les travaux sont exécutés selon les conditions générales de la norme SIA 118, puis réceptionnés avec vous en fin de chantier.</p>
          </article>
        </div>
      </div>
    </section>
%(cta)s  </main>
''' % dict(ph=page_head('Prestations', 'Nos prestations : plafonds, cloisons, isolation et peinture',
                        "Du plafond tendu à la cloison mobile, nous posons le système adapté à chaque usage. Pour chaque prestation : à quoi elle sert, où l'utiliser, ses avantages et les points d'attention.",
                        aside='<p>Une question sur un système ?</p><a href="%s">%s</a>' % (TEL_URI, TEL)),
           toc=toc, groups=plafonds + cloisons + isolation + incendie + integ + peinture + deroulement,
           cta=cta_band('Demander une offre', "Décrivez-nous votre local et vos besoins : nous vous conseillons le système adapté et vous remettons une offre détaillée."))

    write('prestations.html', h + header('prestations.html') + body + footer(joined=True))
