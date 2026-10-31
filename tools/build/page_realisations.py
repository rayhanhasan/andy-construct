# -*- coding: utf-8 -*-
"""Réalisations (architecture §4.3 et §8, copy deck §G) : projets filtrables, visionneuse, avant / après."""
import ctx
from ctx import e, T, V, definitif, marque, PROD
from common import page, page_head, ld_page, TEL, TEL_URI, devis_btn, svc_nom, SERVICES
import composants as c
import portfolio as pf

FILTRES = [('tous', 'Tous')] + [(s, None) for s in SERVICES]


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
    p = dict(fichier='realisations.html', title='Réalisations : placo, peinture, isolation | Andy Construct',
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

    sizes = '(min-width: 1100px) 360px, (min-width: 700px) 45vw, 100vw'
    cartes = ''.join(pf.carte_projet(x, sizes) for x in projets)
    aa = ''.join(pf.avant_apres(x[0]) for x in paires)

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
    corps = page_head('Réalisations', 'Nos réalisations',
                      'Des chantiers photographiés par notre équipe, pendant et après les travaux. Choisissez un type de travaux.',
                      extra=('<p class="page-head__note">%s</p>' % mention) if mention else '')
    corps += '''    <section class="section section--top" aria-labelledby="projets-titre">
      <div class="container">
        <h2 id="projets-titre" class="visually-hidden">Projets</h2>
        <div class="filters js-only" role="group" aria-label="Filtrer les projets par type de travaux">%(boutons)s</div>
        <p class="filters-status js-only" aria-live="polite" data-compteur>%(n)d projets affichés</p>
        <div class="projets" data-galerie-zone data-suivi-zone="fiche_projet">%(cartes)s</div>
      </div>
    </section>

    <section class="section section--mist" id="avant-apres" aria-labelledby="aa-titre">
      <div class="container">
        <div class="section-head">
          <h2 id="aa-titre">Avant, après</h2>
          <p class="lead">Les mêmes lieux, avant et après nos travaux.</p>
        </div>
        <div class="aa-liste">%(aa)s</div>
      </div>
    </section>
''' % dict(boutons=boutons, n=compte('tous'), cartes=cartes, aa=aa)
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

    corps += '''    <section class="section section--tight" aria-label="Références">
      <div class="container refs-fin">
        %s
        <a class="link-arrow" href="professionnels.html#references">Voir les 18 références, par secteur</a>
      </div>
    </section>

    <section class="section section--mist" aria-labelledby="projet-titre">
      <div class="container split">
        <div>
          <h2 id="projet-titre">Un projet semblable aux nôtres ?</h2>
          <p class="lead">Montrez-nous votre local ou vos plans : nous venons voir et vous remettons une offre écrite.</p>
          <div class="cta-actions">%s<a class="btn btn--ghost" href="%s" data-suivi-numero="fixe" data-suivi-emplacement="fiche_projet">Appeler le %s</a></div>
        </div>
        <div class="rappel-seul" data-suivi-zone="bloc_demande">%s</div>
      </div>
    </section>
''' % (c.refs_ligne(), devis_btn(p, 'realisations_fin'), TEL_URI, TEL, c.module_rappel('realisations', seul=True, niveau='h3'))
    corps += visionneuse()
    page(p, corps)
