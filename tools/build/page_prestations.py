# -*- coding: utf-8 -*-
"""Prestations : les 4 services du client (placo, peinture, isolation acoustique, cloisons isothermes)."""
from common import *

TITLE = 'Placo, peinture, isolation · Suisse romande | Andy Construct'
DESC = "Placo (doublages, faux-plafonds, cloisons), peinture intérieure, isolation acoustique et cloisons isothermes, à Genève et dans toute la Suisse romande."
SIZES = '(min-width: 1000px) 360px, (min-width: 760px) 40vw, 100vw'


def ticks(items):
    return '<ul class="ticks">' + ''.join('<li>%s</li>' % i for i in items) + '</ul>'


def figure(pid):
    it = BY[pid]
    return '''
              <figure class="svc__media">
                <span class="media">%s</span>
                <figcaption class="caption">%s</figcaption>
              </figure>''' % (pic(pid, SIZES), e(titre(it)))


def bloc(texte, uses, benef, attention, travaux, cat=None, photo=None, note=''):
    liens = ''
    if cat:
        liens += '\n                  <a class="link-arrow" href="realisations.html?categorie=%s">Voir des réalisations</a>' % cat
    liens += '\n                  <a class="link-arrow" href="contact.html?travaux=%s#devis">Demander une offre</a>' % travaux
    return '''%(note)s
          <div class="svc">
            <div class="svc__grid%(g)s">
              <div>%(texte)s
                <div class="svc__cols">
                  <div><h3 class="label">Pour quels locaux</h3>%(u)s</div>
                  <div><h3 class="label">Avantages</h3>%(b)s</div>
                </div>
                <p class="svc__note"><strong>Point d'attention :</strong> %(att)s</p>
                <p class="svc__links">%(liens)s
                </p>
              </div>%(m)s
            </div>
          </div>''' % dict(note=('\n          <!-- %s -->' % note) if note else '', g='' if photo else ' svc__grid--text',
                           texte=texte, u=ticks(uses), b=ticks(benef), att=attention, liens=liens,
                           m=figure(photo) if photo else '')


def group(gid, eyebrow, title, intro, inner):
    return '''
        <section class="svc-group" id="%(g)s" aria-labelledby="%(g)s-titre">
          <div class="svc-group__head">
            <p class="eyebrow">%(eb)s</p>
            <h2 id="%(g)s-titre">%(t)s</h2>
            <p class="lead">%(i)s</p>
          </div>%(inner)s
        </section>''' % dict(g=gid, eb=eyebrow, t=title, i=intro, inner=inner)


def build():
    h = head(TITLE, DESC, 'prestations.html', ld=[page_ld('prestations.html', TITLE, 'Prestations')])

    placo = group('placo', 'Plâtrerie', 'Placo : doublages, faux-plafonds et cloisons',
                  "Les plaques de plâtre sur ossature métallique permettent de créer, de redresser ou de redistribuer vos espaces, sans maçonnerie et avec une finition prête à peindre.",
                  bloc('''
                <div class="svc__subs">
                  <div id="placo-doublages">
                    <h3 class="svc__title">Doublages</h3>
                    <p>Un parement en plaques de plâtre posé devant un mur existant, collé ou sur ossature. Il redresse le mur, cache les gaines et peut recevoir un isolant.</p>
                  </div>
                  <div id="placo-faux-plafonds">
                    <h3 class="svc__title">Faux-plafonds en plaques de plâtre</h3>
                    <p>Plafonds plats, retombées, gorges lumineuses ou formes courbes, suspendus sous la dalle. Ils cachent les réseaux techniques et intègrent spots et trappes de visite.</p>
                  </div>
                  <div id="placo-cloisons">
                    <h3 class="svc__title">Cloisons en placo</h3>
                    <p>Des cloisons légères pour redistribuer un logement ou un étage de bureaux, rapidement et proprement, sans temps de séchage de maçonnerie.</p>
                  </div>
                </div>''',
                       ['Logements neufs ou en rénovation', 'Bureaux et commerces', "Halls d'entrée, couloirs et cages d'escalier", 'Salles et bâtiments publics'],
                       ['Formes libres : courbes, retombées, gorges lumineuses', 'Passage discret des gaines et des câbles', 'Isolant intégré si nécessaire', "Plaques adaptées aux pièces humides"],
                       "les joints sont enduits puis poncés avant peinture : le local doit être protégé. Les trappes de visite se prévoient dès la conception.",
                       'placo', cat='placo', photo='faux-plafond-placo-gorge-lumineuse-01'))

    peinture = group('peinture', 'Finitions', 'Peinture intérieure',
                     "La finition fait partie du travail : nous vous livrons des pièces terminées.",
                     bloc('''
                <p>Après la pose, nous préparons les supports, réalisons les enduits et les bandes, puis peignons plafonds et murs. Un seul intervenant, du montage des plaques à la dernière couche.</p>''',
                          ['Plafonds et murs après pose de placo', 'Rénovation de logements', 'Bureaux et commerces'],
                          ['Un seul intervenant du début à la fin', 'Préparation soignée des supports', "Peintures adaptées à l'usage des locaux"],
                          "un support neuf en plaques de plâtre se traite avec une impression adaptée avant la peinture de finition.",
                          'peinture', note="PROVISOIRE : à valider avec le client (périmètre exact de l'offre peinture ; photos à fournir)"))

    acoustique = group('isolation-acoustique', 'Confort acoustique', 'Isolation acoustique',
                       "Voix, musique, télévision, pas à l'étage : nous réduisons le bruit qui passe d'une pièce, d'un logement ou d'un étage à l'autre.",
                       bloc('''
                <p>Selon la situation, nous posons un faux-plafond désolidarisé avec isolant, un doublage acoustique ou une cloison à double ossature. Chaque paroi associe plaques de plâtre et laine isolante, sans contact rigide avec la structure pour limiter la transmission du bruit.</p>''',
                            ['Séparations entre logements', 'Salles de réunion et bureaux', 'Chambres et pièces de repos', 'Locaux techniques bruyants'],
                            ['Moins de bruit entre les locaux', 'Plus de confort et de discrétion', 'Solution posée sans gros œuvre', 'Finition prête à peindre'],
                            "un panneau absorbant réduit l'écho dans la pièce, mais pas le bruit qui vient d'un autre logement : pour cela, il faut isoler la paroi.",
                            'isolation-acoustique', cat='isolation-acoustique', photo='panneaux-acoustiques-muraux-01',
                            note="PROVISOIRE : à valider avec le client (la photo montre des panneaux acoustiques muraux : prestation à confirmer)"))

    isothermes = group('cloisons-isothermes', 'Isolation thermique', 'Cloisons isothermes',
                       "Des cloisons et doublages isolants pour séparer un local chauffé d'un local qui ne l'est pas, et limiter les pertes de chaleur.",
                       bloc('''
                <p>Une cloison isotherme associe une ossature métallique, un isolant thermique et des plaques de plâtre. Elle se pose entre un logement et un garage, une cave, des combles ou un dépôt non chauffé. Certaines mesures d'isolation peuvent être subventionnées par les cantons et par le Programme Bâtiments ; la demande se dépose avant le début des travaux.</p>''',
                            ['Garages, caves et dépôts attenants', 'Combles et locaux sous toiture', 'Ateliers et locaux techniques', 'Rénovation énergétique'],
                            ['Moins de pertes de chaleur', 'Confort en hiver comme en été', 'Pose rapide et propre', 'Finition prête à peindre'],
                            "l'épaisseur d'isolant se choisit selon la différence de température entre les deux locaux et les exigences énergétiques du canton.",
                            'cloisons-isothermes', cat='chantier', photo='chantier-ossature-puits-de-lumiere-02',
                            note="PROVISOIRE : à valider avec le client (définition des cloisons isothermes ; photo de chantier d'isolation utilisée en attendant une photo dédiée)"))

    deroulement = group('deroulement', 'Méthode', 'Comment se déroule un chantier',
                        "Six étapes, toujours dans le même ordre, pour savoir à quoi vous attendre.", '''
          <!-- PROVISOIRE : à valider avec le client (déroulé d'un chantier) -->
          <ol class="steps steps--6">
            <li><h3>Visite</h3><p>Relevé des mesures et des contraintes du local, écoute de vos besoins.</p></li>
            <li><h3>Offre écrite</h3><p>Détaillée poste par poste, en CHF, avec la durée prévue.</p></li>
            <li><h3>Planning</h3><p>Dates convenues avec vous et coordination avec les autres corps de métier.</p></li>
            <li><h3>Protection des lieux</h3><p>Sols, mobilier et accès protégés avant le début des travaux.</p></li>
            <li><h3>Nettoyage</h3><p>Évacuation des déchets et nettoyage en fin de chantier.</p></li>
            <li><h3>Réception</h3><p>Contrôle des finitions avec vous, puis remise de l'ouvrage.</p></li>
          </ol>''')

    toc_items = [('placo', 'Placo', [('placo-doublages', 'Doublages'), ('placo-faux-plafonds', 'Faux-plafonds'), ('placo-cloisons', 'Cloisons en placo')]),
                 ('peinture', 'Peinture intérieure', []), ('isolation-acoustique', 'Isolation acoustique', []),
                 ('cloisons-isothermes', 'Cloisons isothermes', []), ('deroulement', "Déroulement d'un chantier", []),
                 ('normes', 'Normes et qualité', [])]
    toc = ''
    for a, t, subs in toc_items:
        sub = ('<ol>' + ''.join('<li><a href="#%s">%s</a></li>' % x for x in subs) + '</ol>') if subs else ''
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
        <!-- PROVISOIRE : à valider avec le client (références normatives ; aucune certification n'est revendiquée) -->
        <div class="norms">
          <article>
            <h3>Acoustique</h3>
            <p>Pour l'isolation acoustique entre locaux, nous nous référons à la norme SIA 181 « Protection contre le bruit dans le bâtiment », selon les exigences définies pour le projet.</p>
          </article>
          <article>
            <h3>Thermique</h3>
            <p>Les cloisons et doublages isolants tiennent compte de la norme SIA 180 et des exigences énergétiques du canton concerné.</p>
          </article>
          <article>
            <h3>Exécution et réception</h3>
            <p>Sauf accord contraire, les travaux sont exécutés selon les conditions générales de la norme SIA 118. Lorsque le projet l'exige, les plaques et systèmes posés respectent les prescriptions de protection incendie de l'AEAI.</p>
          </article>
        </div>
      </div>
    </section>
%(cta)s  </main>
''' % dict(ph=page_head('Prestations', 'Nos prestations : placo, peinture et isolation',
                        "Quatre métiers complémentaires : le placo (doublages, faux-plafonds, cloisons), la peinture intérieure, l'isolation acoustique et les cloisons isothermes. Pour chacun : à quoi il sert, où l'utiliser, ses avantages et les points d'attention.",
                        aside='<p>Une question sur vos travaux ?</p><a href="%s">%s</a>' % (TEL_URI, TEL)),
           toc=toc, groups=placo + peinture + acoustique + isothermes + deroulement,
           cta=cta_band('Demander une offre', "Décrivez-nous votre local et vos besoins : nous vous conseillons la solution adaptée et vous remettons une offre détaillée, partout en Suisse romande."))

    write('prestations.html', h + header('prestations.html') + body + footer(joined=True))
