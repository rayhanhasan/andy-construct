# -*- coding: utf-8 -*-
"""Réalisations v3 (cro-v3 §6.4) : en-tête premium, grille éditoriale de projets (vraies photos uniquement, recadrages
16:9 et 4:5, tailles variées), filtres, avant / après mis en valeur sur fond profond, mur complet des références."""
import ctx
from ctx import e, T, V, definitif, marque, PROD
from common import page, hero_page, ld_page, TEL, TEL_URI, devis_btn, svc_nom, SERVICES
import composants as c
import portfolio as pf

FILTRES = [('tous', 'Tous')] + [(s, None) for s in SERVICES]

# Emplacements de la grille éditoriale (12 colonnes, ordinateur) : recadrage et largeur d'affichage
SLOTS = {'une': ('16x9', '(min-width: 1100px) 860px, 100vw'), 'l': ('16x9', '(min-width: 1100px) 860px, (min-width: 700px) 50vw, 100vw'),
         'p': ('4x5', '(min-width: 1100px) 420px, (min-width: 700px) 50vw, 100vw'), 'm': ('16x9', '(min-width: 1100px) 420px, (min-width: 700px) 50vw, 100vw'),
         'h': ('16x9', '(min-width: 1100px) 640px, (min-width: 700px) 50vw, 100vw')}
RANGEES = [['l', 'p'], ['m', 'm', 'm'], ['p', 'l'], ['h', 'h']]


def composer(projets):
    """Le premier projet est mis à la une ; les suivants remplissent des rangées alternées (grande + portrait,
    trois moyennes, portrait + grande, deux demi) sans laisser de projet seul. Un emplacement portrait reçoit
    de préférence un projet qui a un recadrage 4:5."""
    if not projets:
        return []
    out, reste, k = [(projets[0], 'une')], list(projets[1:]), 0
    while reste:
        n = len(reste)
        choix = None
        for j in range(len(RANGEES)):
            r = RANGEES[(k + j) % len(RANGEES)]
            if len(r) <= n and n - len(r) != 1:
                choix, k = r, (k + j + 1) % len(RANGEES)
                break
        if choix is None:
            choix = ['h', 'h'] if n == 2 else ['l', 'p'] if n > 1 else ['h']
        for slot in choix:
            if slot == 'p':
                i = next((i for i, x in enumerate(reste) if c.RECADRAGES.get(pf.proj_photos(x)[0], {}).get('4x5')), 0)
            else:
                i = 0
            x = reste.pop(i)
            out.append((x, slot))
    return out


def visionneuse():
    return '''  <dialog class="lightbox" id="visionneuse" aria-labelledby="lb-titre">
    <div class="lightbox__bar"><p class="lightbox__count" aria-live="polite"></p><button type="button" class="btn btn--light" data-lb="close">Fermer</button></div>
    <div class="lightbox__stage"><img src="data:," alt="" width="1600" height="1200"></div>
    <div class="lightbox__foot">
      <button type="button" class="btn btn--light" data-lb="prev"><span aria-hidden="true">←</span> Précédente</button>
      <p class="lightbox__caption" id="lb-titre"></p>
      <button type="button" class="btn btn--light" data-lb="next">Suivante <span aria-hidden="true">→</span></button>
    </div>
  </dialog>
'''


def build():
    hero_html, preload = c.hero_image('photo', 'habillage-placo-niches-arrondies-01')
    p = dict(fichier='realisations.html', title='Réalisations : placo, peinture, isolation | Andy Construct', preload=preload,
             desc='Chantiers de placo, de peinture et d\'isolation photographiés par notre équipe : halls, salles, logements, bureaux. Avant / après et références.')
    projets = [x for x in pf.PROJETS if pf.proj_ok(x)]
    paires = pf.PAIRES

    # Compteurs des filtres (projets + paires avant / après) ; un filtre sans projet est masqué
    def compte(s):
        if s == 'tous':
            return len(projets) + len(paires)
        return sum(1 for x in projets if s in pf.proj_tags(x)) + sum(1 for x in paires if s in pf.paire_services(x[0]))
    boutons = ''
    for s, lab in FILTRES:
        n = compte(s)
        if not n:
            continue
        nom = lab or svc_nom(s)
        boutons += ('<button type="button" data-filtre="%s" aria-pressed="%s" data-suivi="galerie_filtre" data-suivi-filtre="%s">%s <span>(%d)</span></button>'
                    % (s, 'true' if s == 'tous' else 'false', s, nom, n))

    cartes = ''
    for x, slot in composer(projets):
        fmt, sizes = SLOTS[slot]
        ph = pf.proj_photos(x)[0]
        cartes += pf.carte_projet(x, sizes, img_html=c.pic_crop(ph, fmt, sizes, pf.alt(ph)), cls='pj pj--' + slot,
                                  niveau='h3', grande=(slot == 'une'))

    # Avant / après : une paire à la une (comparateur), deux paires visibles, les autres repliées (cro-v3 §6.4)
    une, duo = 'aa6', ['aa5', 'aa3']
    autres = [x[0] for x in paires if x[0] not in [une] + duo]
    aa_une = pf.avant_apres(une, grande=True)
    aa_duo = ''.join(pf.avant_apres(x) for x in duo)
    aa_plus = ''.join(pf.avant_apres(x) for x in autres)

    # Données structurées : galerie (légendes exactes, sans lieu non confirmé)
    medias = []
    for x in projets:
        for ph in pf.proj_photos(x):
            big = c.pic_data(ph)[0]
            medias.append({'@type': 'ImageObject', 'contentUrl': PROD + big, 'caption': ctx.fr(pf.legende(ph)), 'creator': {'@id': PROD + '#entreprise'}})
    ld = ld_page('realisations.html', p['title'], 'Réalisations', typ='CollectionPage')
    ld['@graph'].append({'@type': 'ImageGallery', '@id': PROD + 'realisations.html#galerie', 'name': 'Réalisations d\'Andy Construct',
                         'isPartOf': {'@id': PROD + 'realisations.html#page'}, 'associatedMedia': medias})
    p['ld'] = [ld]

    mention = T('C25', 'Toutes les photos sont nos propres réalisations.', '')
    actions = ('%s<a class="btn btn--light" href="#toutes-references">Voir nos références</a>' % devis_btn(p, 'entete_page'))
    corps = hero_page('Réalisations', 'Réalisations et références',
                      'Nos chantiers, photographiés <b>pendant et après</b> les travaux.',
                      actions=actions, media=hero_html, extra=('<p class="hero__note">%s</p>' % mention) if mention else '',
                      badges=c.badges(['B5', 'B1', 'B3'], cls='badges--3'))
    corps += '''    <section class="section section--top" aria-labelledby="projets-titre">
      <div class="container">
        <div class="section-head section-head--row projets-head">
          <h2 id="projets-titre">Projets</h2>
          <div class="filters js-only" role="group" aria-label="Filtrer les projets par type de travaux">%(boutons)s</div>
        </div>
        <p class="filters-status js-only visually-hidden" aria-live="polite" data-compteur>%(n)d projets affichés</p>
        <div class="pjs" data-galerie-zone data-suivi-zone="fiche_projet">%(cartes)s</div>
      </div>
    </section>

    <section class="section section--dark on-dark aa-section" id="avant-apres" aria-labelledby="aa-titre" data-trait>
      <div class="container">
        <div class="section-head">
          <h2 id="aa-titre">Avant, après</h2>
          <span class="laser laser--court" aria-hidden="true"></span>
          <p class="lead">Les mêmes lieux, avant et après nos travaux. Faites glisser le curseur pour comparer.</p>
        </div>
        <div class="aa-grille">
          <div class="aa-une">%(aa_une)s</div>
          <div class="aa-cote">%(aa_duo)s</div>
        </div>
        <details class="aa-plus">
          <summary>Voir les %(n_autres)d autres avant / après</summary>
          <div class="aa-duo">%(aa_plus)s</div>
        </details>
      </div>
    </section>
''' % dict(boutons=boutons, n=compte('tous'), cartes=cartes, aa_une=aa_une, aa_duo=aa_duo, aa_plus=aa_plus, n_autres=len(autres))
    corps += c.temoignages()

    if not ctx.prod():
        # Photos hors offre : visibles en validation seulement, pour que le client tranche (architecture §8.4)
        items = ''
        for pid in pf.RETIREES:
            it = c.MANIFEST[pid]
            items += ('<figure class="hors-offre__item">%s<figcaption><span class="badge badge--grey">Hors offre</span> %s</figcaption></figure>'
                      % (c.pic(pid, '(min-width: 1100px) 270px, (min-width: 700px) 30vw, 50vw', it['titre']), e(it['titre'])))
        corps += '''    <section class="section hors-offre" aria-labelledby="hors-offre-titre">
      <div class="container">
        <h2 id="hors-offre-titre">Photos retirées de la version publiée</h2>
        <p class="lead">Version de validation seulement : ces %d photos montrent des ouvrages hors des quatre métiers (plafonds tendus, métalliques, lumineux, cloisons vitrées). Elles n'apparaissent pas sur le site publié, sauf décision contraire de votre part.</p>
        <div class="hors-offre__grille">%s</div>
      </div>
    </section>
''' % (len(pf.RETIREES), items)

    corps += '''    <section class="section section--mist mur" id="toutes-references" aria-labelledby="mur-titre" data-suivi-zone="references">
      <div class="container">
        <div class="section-head section-head--row">
          <div>
            <h2 id="mur-titre">Ils nous ont confié des travaux</h2>
            <p class="lead">%s</p>
          </div>
          <a class="link-arrow" href="professionnels.html#references">Les références par secteur</a>
        </div>
        %s
      </div>
    </section>

    <section class="section" aria-labelledby="projet-titre">
      <div class="container split">
        <div>
          <h2 id="projet-titre">Un projet semblable aux nôtres ?</h2>
          <span class="laser laser--court" aria-hidden="true"></span>
          <p class="lead">Montrez-nous votre local ou vos plans : nous venons voir et vous remettons une <b>offre écrite</b>.</p>
          <div class="cta-actions">%s<a class="btn btn--ghost" href="%s" data-suivi-numero="fixe" data-suivi-emplacement="fiche_projet">Appeler le %s</a></div>
          %s
        </div>
        <div class="rappel-seul" data-suivi-zone="bloc_demande">%s</div>
      </div>
    </section>
''' % (marque('C22', '<b>%d références</b>, publiques et privées, à Genève et dans le canton de Vaud.' % c.nb_refs()), c.mur_complet(),
       devis_btn(p, 'realisations_fin'), TEL_URI, TEL, c.badges(['B1', 'B3', 'B4'], cls='badges--clair badges--3 badges--cta'),
       c.module_rappel('realisations', seul=True, niveau='h3'))
    corps += visionneuse()
    page(p, corps)
