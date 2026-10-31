# -*- coding: utf-8 -*-
"""Portfolio par projets (architecture §8) : classement des 30 photos, projets P1-P8, paires avant / après.

Décision par photo : M = montrer · N = montrer si les codes de condition sont confirmés (en production) ·
R = retirer en production (visible en preview et verification, sous un titre « hors offre », pour que le client tranche).
"""
import ctx
from ctx import e, T, V, definitif, marque, M as compter
from common import svc_nom, devis_btn
from composants import pic, pic_data, aa_pic, MANIFEST

# id : (décision, codes de condition, légende, texte alternatif) — légendes §8.4, alt §O
PHOTOS = {
    'faux-plafond-placo-gorge-lumineuse-01': ('M', '', 'Faux-plafond en plaques de plâtre à gorge lumineuse',
                                              'Faux-plafond en plaques de plâtre à gorge lumineuse et spots, dans un hall'),
    'faux-plafond-placo-gorge-lumineuse-02': ('M', '', 'Faux-plafond arrondi en plaques de plâtre, éclairage intégré',
                                              'Faux-plafond arrondi en plaques de plâtre, éclairage intégré, au bout d\'un couloir'),
    'habillage-placo-niches-arrondies-01': ('M', '', 'Pendant les travaux : habillage en plaques de plâtre à niches arrondies, escalier protégé',
                                            'Mur d\'escalier habillé de plaques de plâtre à niches arrondies, avant peinture'),
    'chantier-suspentes-ossature-01': ('M', '', 'Pendant les travaux : suspentes et ossature d\'un faux-plafond, sous une dalle isolée',
                                       'Suspentes et ossature métallique d\'un faux-plafond, sous une dalle isolée'),
    'panneaux-acoustiques-muraux-01': ('N', 'C18', 'Correction acoustique : panneaux muraux et plafond perforé',
                                       'Panneaux acoustiques muraux et plafond perforé contre l\'écho d\'une salle'),
    'chantier-ossature-puits-de-lumiere-01': ('N', 'C25', 'Pendant les travaux : ossature métallique et isolant, avant la fermeture du plafond',
                                              'Poseur fixant une ossature métallique garnie d\'isolant, près d\'un puits de lumière'),
    'cadre-acoustique-salle-de-reunion-01': ('N', 'C18', 'Salle de réunion : panneau acoustique mural contre l\'écho',
                                             'Panneau acoustique mural imprimé d\'un paysage, dans une salle de réunion'),
    'plafond-placo-ilot-ovale-01': ('N', '', 'Hall : îlot ovale suspendu en plaques de plâtre',
                                    'Îlot ovale suspendu en plaques de plâtre au-dessus d\'un hall vitré'),
    'chantier-ossature-puits-de-lumiere-02': ('N', '', 'Pendant les travaux : ossature et isolant autour d\'un puits de lumière',
                                              'Ossature métallique et isolant autour d\'un puits de lumière, avant fermeture'),
    'chantier-salle-de-spectacle-01': ('N', 'C25', 'Salle de spectacle : intervention dans une salle protégée',
                                       'Salle de spectacle à balcons, vue de la scène pendant des travaux'),
    'chantier-salle-de-spectacle-02': ('N', 'C25', 'Salle de spectacle : fauteuils protégés pendant les travaux',
                                       'Intervention sur un balcon de salle de spectacle, fauteuils protégés sous bâche'),
}
# Photos retirées en production (« R ») : légende exacte, sans réécriture
RETIREES = ['plafond-tendu-ilots-lumineux-01', 'plafond-tendu-ilots-lumineux-02', 'plafond-lumineux-circulaire-01',
            'paroi-lumineuse-imprimee-01', 'plafond-tendu-ilot-eclairage-indirect-01', 'plafond-couronnes-lumineuses-01',
            'plafond-tendu-puits-de-lumiere-01', 'plafond-tendu-ilots-lumineux-03', 'plafond-couronnes-lumineuses-02',
            'plafond-tendu-poutres-apparentes-01', 'cadre-acoustique-imprime-01', 'plafond-dalles-couloir-01',
            'plafond-lames-metalliques-01', 'chantier-pose-plafond-lumineux-01', 'plafond-tendu-mat-01',
            'plafond-lames-metalliques-02', 'plafond-bacs-metalliques-cuisine-01', 'cloisons-modulaires-vitrees-01',
            'cloisons-modulaires-vitrees-02']


def photo_ok(pid):
    """Publiable dans ce mode ? (production : M, ou N dont les conditions sont confirmées)."""
    d, codes, _, _ = PHOTOS[pid]
    if not ctx.prod():
        return True
    return d == 'M' or (d == 'N' and (not codes or ctx.confirme(codes)))


def legende(pid):
    return PHOTOS[pid][2]


def alt(pid):
    return PHOTOS[pid][3]


# ---------------------------------------------------------------- projets (architecture §8.6, copy deck §G.3)
# lieu / contrainte / étiquettes : (codes, définitif, repli). Définitif None : rien de fourni, le repli s'affiche (marqué).
PROJETS = [
    dict(id='projet-hall-gorge-lumineuse', titre='Hall et couloirs : faux-plafond à gorge lumineuse',
         photos=['faux-plafond-placo-gorge-lumineuse-01', 'faux-plafond-placo-gorge-lumineuse-02'],
         lieu=('C25', 'Immeuble, canton de Genève', 'Hall d\'immeuble'),
         contrainte=('C25', None, 'Formes courbes, éclairage et spots intégrés au plafond.'),
         tags=('C25', ['placo', 'peinture'], ['placo']), badge=False),
    dict(id='projet-grande-salle-ossature', titre='Grande salle : ossature et isolant avant la fermeture',
         photos=['chantier-ossature-puits-de-lumiere-01', 'chantier-ossature-puits-de-lumiere-02'],
         lieu=('C25', 'Salle publique, canton de Genève', 'Salle publique'),
         contrainte=('C25', None, 'Travail en hauteur, autour de puits de lumière.'),
         tags=('C25', None, ['placo']), badge=True),
    dict(id='projet-faux-plafond-dalle-isolee', titre='Faux-plafond suspendu sous une dalle isolée',
         photos=['chantier-suspentes-ossature-01'],
         lieu=('C25', None, 'Grand local'),
         contrainte=('C25', None, 'Suspentes réglées et alignées sur toute la surface, avant la pose des plaques.'),
         tags=(None, ['placo'], ['placo']), badge=True),
    dict(id='projet-cage-escalier-niches', titre='Cage d\'escalier : habillage à niches arrondies',
         photos=['habillage-placo-niches-arrondies-01'],
         lieu=('C25', None, 'Immeuble'),
         contrainte=('C25', None, 'Formes arrondies, escalier protégé pendant les travaux.'),
         tags=(None, ['placo'], ['placo']), badge=True),
    dict(id='projet-ilot-ovale', titre='Hall : îlot ovale suspendu',
         photos=['plafond-placo-ilot-ovale-01'],
         lieu=('C25', 'Bâtiment d\'entreprise', 'Hall'),
         contrainte=('C25', None, 'Un grand îlot suspendu au-dessus d\'une trémie.'),
         tags=(None, ['placo'], ['placo']), badge=False),
    dict(id='projet-correction-acoustique', titre='Correction acoustique d\'une salle',
         photos=['panneaux-acoustiques-muraux-01'],
         lieu=('C25', None, 'Salle'),
         contrainte=('C25', None, 'Réduire l\'écho, sans gros travaux.'),
         tags=(None, ['isolation-acoustique'], ['isolation-acoustique']), badge=False),
    dict(id='projet-salle-de-reunion', titre='Salle de réunion : moins d\'écho',
         photos=['cadre-acoustique-salle-de-reunion-01'],
         lieu=(None, 'Bureaux', 'Bureaux'),
         contrainte=('C25', None, 'Un grand panneau mural absorbe l\'écho de la salle.'),
         tags=(None, ['isolation-acoustique'], ['isolation-acoustique']), badge=False),
    dict(id='projet-salle-de-spectacle', titre='Salle de spectacle : intervention en salle protégée',
         photos=['chantier-salle-de-spectacle-01', 'chantier-salle-de-spectacle-02'],
         lieu=(None, 'Salle de spectacle', 'Salle de spectacle'),
         contrainte=('C25', None, 'Travail en hauteur, fauteuils protégés sous bâche.'),
         tags=('C25', None, []), badge=True),
]
PROJ = {p['id']: p for p in PROJETS}


def proj_photos(p):
    return [x for x in p['photos'] if photo_ok(x)]


def proj_ok(p):
    return bool(proj_photos(p))


def _txt(triple):
    codes, d, r = triple
    if not codes:
        return d if d is not None else r
    if d is None:          # aucun texte définitif fourni : repli, signalé en vérification
        compter(codes)
        return marque(codes, r) if ctx.MODE == 'verification' else r
    return T(codes, d, r)


def proj_tags(p):
    codes, d, r = p['tags']
    if not codes:
        return d
    if d is None or not definitif(codes):
        if d is None:
            compter(codes)
        return r
    return d


def tags_html(services, marque_codes=None):
    if not services:
        return ''
    h = '<ul class="tags">%s</ul>' % ''.join('<li><a href="%s.html">%s</a></li>' % (s, svc_nom(s)) for s in services)
    return marque(marque_codes, h) if marque_codes else h


def carte_projet(p, sizes, niveau='h3', cta=True, p_page=None, eager=False, ancre=True, grande=False, img_html=None, cls=''):
    """Fiche projet (§8.2) : photo 3:2, titre, type de lieu, contrainte, étiquettes, badge, bouton contextuel."""
    photos = proj_photos(p)
    tags = proj_tags(p)
    codes_tags = p['tags'][0] if (p['tags'][0] and not ctx.confirme(p['tags'][0])) else None
    n = len(photos)
    big, jpg, w, h = pic_data(photos[0])
    autres = ''.join('<li data-src="%s" data-jpg="%s" data-w="%d" data-h="%d" data-alt="%s" data-legende="%s"></li>'
                     % (pic_data(x) + (e(alt(x)), e(legende(x)))) for x in photos)
    badge = '<span class="badge">Pendant les travaux</span>' if p['badge'] else ''
    service = tags[0] if tags else None
    bouton = ''
    if cta:
        bouton = ('<p class="projet__cta"><a class="link-arrow" href="contact.html%s#demande" data-suivi="devis_clic" data-suivi-emplacement="fiche_projet"%s>Un projet semblable ? Demander un devis</a></p>'
                  % (('?travaux=' + service) if service else '', (' data-suivi-service="%s"' % service) if service else ''))
    voir = ('Voir les %d photos du projet' % n) if n > 1 else 'Agrandir la photo'
    return '''<article class="projet%(gr)s%(cls)s"%(id)s data-services="%(svc)s">
            <div class="projet__media">
              %(img)s<button type="button" class="projet__btn" data-galerie aria-describedby="%(pid)s-t"><span class="projet__voir">%(voir)s</span></button>%(badge)s
              <ul class="projet__photos" hidden>%(autres)s</ul>
            </div>
            <div class="projet__body">
              <span class="laser laser--court" aria-hidden="true"></span>
              <%(n)s class="projet__titre" id="%(pid)s-t">%(titre)s</%(n)s>
              <p class="projet__lieu">%(lieu)s</p>
              <p class="projet__contrainte">%(contrainte)s</p>
              %(tags)s
              %(bouton)s
            </div>
          </article>''' % dict(
        gr=' projet--grand' if grande else '', cls=(' ' + cls) if cls else '', id=(' id="%s"' % p['id']) if ancre else '', svc=' '.join(tags), pid=p['id'],
        img=img_html or pic(photos[0], sizes, alt(photos[0]), eager=eager), voir=voir, badge=badge, autres=autres, n=niveau,
        titre=p['titre'], lieu=_txt(p['lieu']), contrainte=_txt(p['contrainte']), tags=tags_html(tags, codes_tags), bouton=bouton)


# ---------------------------------------------------------------- avant / après (architecture §8.5, copy deck §G.4)
# (id, légende, services définitifs, services de repli (C26), alt avant, alt après, comparateur)
PAIRES = [
    ('aa5', 'Couloir : puits de lumière circulaires dans un faux-plafond', ['placo'], ['placo'],
     'Avant : réservations circulaires dans la dalle d\'un couloir', 'Après : couloir au faux-plafond percé de puits de lumière ronds', True),
    ('aa6', 'Séjour : faux-plafond en périphérie et spots', ['placo', 'peinture'], ['placo'],
     'Avant : séjour avant travaux, devant une grande baie vitrée', 'Après : séjour avec faux-plafond en périphérie et spots', True),
    ('aa3', 'Combles : isolation et rampant fini sous une fenêtre de toit', ['cloisons-isothermes'], ['cloisons-isothermes'],
     'Avant : fenêtre de toit, isolant visible et plafond noirci', 'Après : rampant blanc fini autour d\'une fenêtre de toit', False),
    ('aa7', 'Paroi cintrée : de l\'ossature au couloir fini', ['placo'], ['placo'],
     'Avant : ossature métallique d\'une paroi cintrée', 'Après : couloir fini avec paroi cintrée et spots', False),
    ('aa1', 'Caisson en plaques de plâtre sous une verrière', ['placo'], ['placo'],
     'Avant : caisson en cours, plaques jointoyées sous une verrière', 'Après : caisson en plaques de plâtre fini sous une verrière', False),
    ('aa2', 'Gaine de ventilation cachée dans un couloir', ['placo'], ['placo'],
     'Avant : gaine de ventilation apparente sous la charpente', 'Après : couloir au plafond lisse, gaine cachée', False),
    ('aa4', 'Appareil de ventilation habillé d\'un caisson', ['placo'], ['placo'],
     'Avant : appareil de ventilation entre les chevrons', 'Après : appareil habillé d\'un caisson près d\'une fenêtre cintrée', False),
]
PAIRE = {x[0]: x for x in PAIRES}


def paire_services(pid):
    _, _, d, r, _, _, _ = PAIRE[pid]
    return d if definitif('C26') else r


def avant_apres(pid, niveau='h3', grande=False, legende_txt=None, sans_legende=False):
    """Deux photos avec les étiquettes « Avant » et « Après » en texte. Les paires au même format
    deviennent, avec JavaScript, un comparateur accessible (curseur et boutons) ; sinon côte à côte."""
    _, leg, _, _, alt_av, alt_ap, comp = PAIRE[pid]
    svcs = paire_services(pid)
    sizes = '(min-width: 1000px) 560px, (min-width: 640px) 45vw, 100vw' if not grande else '(min-width: 1000px) 800px, 100vw'
    tags = tags_html(svcs, 'C26' if (PAIRE[pid][2] != PAIRE[pid][3] and not ctx.confirme('C26')) else None)
    return '''<figure class="aa%(cmp)s%(gr)s" id="avant-apres-%(id)s" data-services="%(svc)s"%(data)s>
            <div class="aa__pair">
              <div class="aa__img aa__img--avant"><p class="aa__lbl">Avant</p>%(av)s</div>
              <div class="aa__img aa__img--apres"><p class="aa__lbl">Après</p>%(ap)s</div>
            </div>
            <figcaption%(fc)s><%(n)s class="aa__titre">%(leg)s</%(n)s>%(tags)s</figcaption>
          </figure>''' % dict(fc=' class="visually-hidden"' if sans_legende else '',
        cmp=' aa--comparable' if comp else '', gr=' aa--grand' if grande else '', id=pid, svc=' '.join(svcs),
        data=' data-comparateur' if comp else '', av=aa_pic(pid, 'avant', sizes, alt_av), ap=aa_pic(pid, 'apres', sizes, alt_ap),
        n='p' if sans_legende else niveau, leg=marque('C26', legende_txt or leg), tags='' if sans_legende else tags)
