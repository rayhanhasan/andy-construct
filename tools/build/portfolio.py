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
# v5 : le document du client confirme ces ouvrages (tissu tendu = spécialité, plafonds métalliques, fibre minérale,
# parois vitrées). Photos de l'ancien site : publiées en production quand leurs accords et lieux sont confirmés (C25).
PHOTOS.update({
    'plafond-tendu-ilots-lumineux-01': ('N', 'C25', 'Tissu tendu : îlots lumineux suspendus au-dessus d\'une grande salle',
                                        'Îlots ovales en tissu tendu sombre, à éclairage indirect, au-dessus d\'une salle à colonnes'),
    'plafond-tendu-ilots-lumineux-02': ('N', 'C25', 'Tissu tendu : îlots à gorge lumineuse autour des colonnes',
                                        'Îlots en tissu tendu sombre bordés d\'une gorge lumineuse, autour de colonnes blanches'),
    'plafond-tendu-ilots-lumineux-03': ('N', 'C25', 'Tissu tendu : îlots superposés, éclairage indirect',
                                        'Îlots superposés en tissu tendu, éclairage indirect entre les niveaux'),
    'plafond-tendu-ilot-eclairage-indirect-01': ('N', 'C25', 'Tissu tendu : îlot à éclairage indirect',
                                                 'Bord d\'un îlot en tissu tendu sombre, lumière indirecte sur le plafond'),
    'plafond-tendu-puits-de-lumiere-01': ('N', 'C25', 'Tissu tendu sombre et puits de lumière circulaire',
                                          'Plafond en tissu tendu sombre percé d\'un puits de lumière circulaire'),
    'plafond-tendu-poutres-apparentes-01': ('N', 'C25', 'Tissu tendu blanc entre des poutres apparentes',
                                            'Plafond en tissu tendu blanc posé entre des poutres en bois apparentes'),
    'plafond-tendu-mat-01': ('N', 'C25', 'Tissu tendu mat : une surface parfaitement lisse',
                             'Plafond en tissu tendu mat, parfaitement lisse, dans une pièce vide'),
    'plafond-couronnes-lumineuses-01': ('N', 'C25', 'Couronnes lumineuses en tissu tendu', 'Deux couronnes lumineuses en tissu tendu au plafond d\'un espace vitré'),
    'plafond-couronnes-lumineuses-02': ('N', 'C25', 'Couronne lumineuse en tissu tendu', 'Couronne lumineuse en tissu tendu, rouge et blanc, au centre d\'un plafond'),
    'plafond-lumineux-circulaire-01': ('N', 'C25', 'Plafond lumineux circulaire en toile imprimée', 'Plafond lumineux circulaire en toile tendue imprimée'),
    'paroi-lumineuse-imprimee-01': ('N', 'C25', 'Paroi lumineuse en toile imprimée', 'Paroi lumineuse en toile tendue imprimée d\'une gravure ancienne'),
    'cadre-acoustique-imprime-01': ('N', 'C25', 'Cadre acoustique imprimé au mur', 'Grand cadre acoustique mural imprimé d\'un insecte'),
    'chantier-pose-plafond-lumineux-01': ('N', 'C25', 'Pendant les travaux : pose d\'un plafond lumineux circulaire',
                                          'Poseur sur un échafaudage, sous l\'ossature d\'un plafond lumineux circulaire'),
    'plafond-dalles-couloir-01': ('N', 'C25', 'Couloir : faux plafond en dalles et gorge lumineuse', 'Couloir au faux plafond en dalles, plafonniers ronds et gorge lumineuse'),
    'plafond-lames-metalliques-01': ('N', 'C25', 'Faux plafond en lames métalliques', 'Faux plafond en lames métalliques, suspensions rouges'),
    'plafond-lames-metalliques-02': ('N', 'C25', 'Lames métalliques et spots encastrés', 'Faux plafond en lames métalliques avec spots encastrés'),
    'plafond-bacs-metalliques-cuisine-01': ('N', 'C25', 'Cuisine professionnelle : plafond en bacs métalliques', 'Plafond en bacs métalliques au-dessus d\'une hotte de cuisine professionnelle'),
    'cloisons-modulaires-vitrees-01': ('N', 'C25', 'Bureaux : cloisons modulaires vitrées', 'Cloisons modulaires blanches avec impostes vitrées, dans des bureaux'),
    'cloisons-modulaires-vitrees-02': ('N', 'C25', 'Bureaux : cloisons modulaires vitrées et stores', 'Cloisons modulaires vitrées avec stores, dans des bureaux'),
})
RETIREES = []


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
# v6 : photos de chantier fournies par le client (novembre 2026), publiées dans toutes les versions
PHOTOS.update({
    'salon-ovales-tissu-tendu-01': ('M', '', 'Salon : îlots ovales en tissu tendu et éclairage indirect',
                                    'Salon aux banquettes bleues sous des îlots ovales en tissu tendu, bordés d\'un éclairage indirect'),
    'piscine-plafond-tendu-lumineux-01': ('M', '', 'Piscine : plafond tendu et cercles lumineux',
                                          'Piscine intérieure sous un plafond tendu blanc percé de cercles lumineux'),
    'restaurant-traitement-acoustique-01': ('M', '', 'Restaurant : traitement acoustique du plafond',
                                            'Salle de restaurant sous un plafond voûté traité en acoustique, retombées blanches'),
    'salle-de-reunion-cadres-acoustiques-01': ('M', '', 'Salle de réunion : cadres acoustiques suspendus',
                                               'Salle de réunion blanche sous de grands cadres acoustiques suspendus, spots encastrés'),
    'tissu-tendu-cadres-espace-vitre-01': ('M', '', 'Tissu tendu et cadres lumineux dans un espace vitré',
                                           'Plafond en tissu tendu à cadres lumineux carrés, dans une salle vitrée sur un parc'),
    'baffles-acoustiques-eclairage-indirect-01': ('M', '', 'Panneaux acoustiques suspendus, éclairage indirect',
                                                  'Panneaux acoustiques gris suspendus sous un plafond en béton, éclairage indirect chaud'),
    'panneaux-acoustiques-sous-charpente-01': ('M', '', 'Panneaux acoustiques suspendus sous une charpente',
                                               'Panneaux acoustiques et luminaires linéaires suspendus sous une charpente en bois'),
    'piece-combles-platrerie-peinture-01': ('M', '', 'Pièce sous combles : plâtrerie, peinture et doublages',
                                            'Pièce sous combles aux rampants en plaques de plâtre peints en blanc, fenêtre de toit'),
    'combles-amenages-charpente-01': ('M', '', 'Combles aménagés : surfaces lisses sous la charpente',
                                      'Grand volume sous combles, rampants lisses et blancs entre les fermes en bois'),
    'couloir-plafond-ligne-lumineuse-01': ('M', '', 'Couloir : plafond en plaques de plâtre et ligne lumineuse',
                                           'Long couloir blanc au plafond en plaques de plâtre, ligne lumineuse encastrée'),
    'tracage-laser-plafond-01': ('M', '', 'Traçage au laser avant la pose d\'un plafond',
                                 'Lignes laser rouge et verte projetées au plafond pour tracer l\'implantation'),
})

PROJETS = [
    # v6 : chantiers photographiés par l'entreprise, en tête du portfolio
    dict(id='projet-salon-ovales', titre='Salon : îlots ovales en tissu tendu',
         photos=['salon-ovales-tissu-tendu-01'], lieu=(None, 'Salon', 'Salon'),
         contrainte=(None, 'Des formes ovales suspendues, bordées de lumière indirecte, qui calment l\'acoustique.', None),
         tags=(None, ['faux-plafonds', 'isolation-acoustique'], ['faux-plafonds', 'isolation-acoustique']), badge=False),
    dict(id='projet-piscine-plafond-tendu', titre='Piscine : plafond tendu et cercles lumineux',
         photos=['piscine-plafond-tendu-lumineux-01'], lieu=(None, 'Piscine intérieure', 'Piscine intérieure'),
         contrainte=(None, 'Un plafond tendu adapté à l\'humidité, percé de cercles lumineux.', None),
         tags=(None, ['faux-plafonds'], ['faux-plafonds']), badge=False),
    dict(id='projet-restaurant-acoustique', titre='Restaurant : traitement acoustique du plafond',
         photos=['restaurant-traitement-acoustique-01'], lieu=(None, 'Restaurant', 'Restaurant'),
         contrainte=(None, 'Une salle pleine qui reste calme : plafond voûté traité en acoustique.', None),
         tags=(None, ['isolation-acoustique', 'faux-plafonds'], ['isolation-acoustique', 'faux-plafonds']), badge=False),
    dict(id='projet-salle-reunion-cadres', titre='Salle de réunion : cadres acoustiques suspendus',
         photos=['salle-de-reunion-cadres-acoustiques-01'], lieu=(None, 'Bureaux', 'Bureaux'),
         contrainte=(None, 'De grands cadres suspendus et des spots intégrés : moins d\'écho, plus de clarté.', None),
         tags=(None, ['isolation-acoustique'], ['isolation-acoustique']), badge=False),
    dict(id='projet-tissu-tendu-cadres', titre='Espace vitré : tissu tendu et cadres lumineux',
         photos=['tissu-tendu-cadres-espace-vitre-01'], lieu=(None, 'Salle vitrée', 'Salle vitrée'),
         contrainte=(None, 'Un plafond en tissu tendu à cadres lumineux, face à une grande baie vitrée.', None),
         tags=(None, ['faux-plafonds', 'isolation-acoustique'], ['faux-plafonds', 'isolation-acoustique']), badge=False),
    dict(id='projet-panneaux-suspendus', titre='Bureaux et combles : panneaux acoustiques suspendus',
         photos=['panneaux-acoustiques-sous-charpente-01', 'baffles-acoustiques-eclairage-indirect-01'], lieu=(None, 'Bureaux', 'Bureaux'),
         contrainte=(None, 'Des panneaux suspendus sous une charpente ou un plafond béton, sans toucher à l\'existant.', None),
         tags=(None, ['isolation-acoustique'], ['isolation-acoustique']), badge=False),
    dict(id='projet-combles-platrerie', titre='Combles : plâtrerie, peinture et doublages',
         photos=['piece-combles-platrerie-peinture-01', 'combles-amenages-charpente-01'], lieu=(None, 'Combles', 'Combles'),
         contrainte=(None, 'Rampants, doublages et angles nets sous la charpente, jusqu\'à la peinture.', None),
         tags=(None, ['platrerie-peinture', 'cloisons'], ['platrerie-peinture', 'cloisons']), badge=False),
    dict(id='projet-couloir-ligne-lumineuse', titre='Couloir : plafond en plâtre et ligne lumineuse',
         photos=['couloir-plafond-ligne-lumineuse-01'], lieu=(None, 'Immeuble', 'Immeuble'),
         contrainte=(None, 'Une ligne lumineuse encastrée sur toute la longueur du couloir.', None),
         tags=(None, ['faux-plafonds', 'platrerie-peinture'], ['faux-plafonds', 'platrerie-peinture']), badge=False),
    dict(id='projet-hall-gorge-lumineuse', titre='Hall et couloirs : faux-plafond à gorge lumineuse',
         photos=['faux-plafond-placo-gorge-lumineuse-01', 'faux-plafond-placo-gorge-lumineuse-02'],
         lieu=('C25', 'Immeuble, canton de Genève', 'Hall d\'immeuble'),
         contrainte=('C25', None, 'Formes courbes, éclairage et spots intégrés au plafond.'),
         tags=('C25', ['faux-plafonds', 'platrerie-peinture'], ['faux-plafonds']), badge=False),
    dict(id='projet-grande-salle-ossature', titre='Grande salle : ossature et isolant avant la fermeture',
         photos=['chantier-ossature-puits-de-lumiere-01', 'chantier-ossature-puits-de-lumiere-02'],
         lieu=('C25', 'Salle publique, canton de Genève', 'Salle publique'),
         contrainte=('C25', None, 'Travail en hauteur, autour de puits de lumière.'),
         tags=('C25', None, ['faux-plafonds']), badge=True),
    dict(id='projet-faux-plafond-dalle-isolee', titre='Faux-plafond suspendu sous une dalle isolée',
         photos=['chantier-suspentes-ossature-01'],
         lieu=('C25', None, 'Grand local'),
         contrainte=('C25', None, 'Suspentes réglées et alignées sur toute la surface, avant la pose des plaques.'),
         tags=(None, ['faux-plafonds'], ['faux-plafonds']), badge=True),
    dict(id='projet-cage-escalier-niches', titre='Cage d\'escalier : habillage à niches arrondies',
         photos=['habillage-placo-niches-arrondies-01'],
         lieu=('C25', None, 'Immeuble'),
         contrainte=('C25', None, 'Formes arrondies, escalier protégé pendant les travaux.'),
         tags=(None, ['platrerie-peinture'], ['platrerie-peinture']), badge=True),
    dict(id='projet-ilot-ovale', titre='Hall : îlot ovale suspendu',
         photos=['plafond-placo-ilot-ovale-01'],
         lieu=('C25', 'Bâtiment d\'entreprise', 'Hall'),
         contrainte=('C25', None, 'Un grand îlot suspendu au-dessus d\'une trémie.'),
         tags=(None, ['faux-plafonds'], ['faux-plafonds']), badge=False),
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
    dict(id='projet-ilots-tissu-tendu', titre='Grande salle : îlots en tissu tendu et éclairage indirect',
         photos=['plafond-tendu-ilots-lumineux-01', 'plafond-tendu-ilots-lumineux-02', 'plafond-tendu-ilots-lumineux-03', 'plafond-tendu-puits-de-lumiere-01'],
         lieu=('C25', None, 'Grande salle'),
         contrainte=('C25', None, 'Des îlots suspendus autour des colonnes, lumière indirecte et puits de lumière.'),
         tags=(None, ['faux-plafonds', 'isolation-acoustique'], ['faux-plafonds', 'isolation-acoustique']), badge=False),
    dict(id='projet-couronnes-lumineuses', titre='Espace d\'accueil : couronnes lumineuses en tissu tendu',
         photos=['plafond-couronnes-lumineuses-01', 'plafond-couronnes-lumineuses-02', 'chantier-pose-plafond-lumineux-01', 'plafond-lumineux-circulaire-01'],
         lieu=('C25', None, 'Espace d\'accueil'),
         contrainte=('C25', None, 'Des formes circulaires lumineuses intégrées au plafond existant.'),
         tags=(None, ['faux-plafonds'], ['faux-plafonds']), badge=False),
    dict(id='projet-plafonds-metalliques', titre='Restaurant et cuisine : plafonds métalliques',
         photos=['plafond-lames-metalliques-01', 'plafond-lames-metalliques-02', 'plafond-bacs-metalliques-cuisine-01'],
         lieu=('C25', None, 'Restaurant'),
         contrainte=('C25', None, 'Des surfaces résistantes et faciles d\'entretien, en salle comme en cuisine.'),
         tags=(None, ['faux-plafonds'], ['faux-plafonds']), badge=False),
    dict(id='projet-cloisons-vitrees', titre='Bureaux : cloisons modulaires vitrées',
         photos=['cloisons-modulaires-vitrees-01', 'cloisons-modulaires-vitrees-02'],
         lieu=('C25', None, 'Bureaux'),
         contrainte=('C25', None, 'Des bureaux cloisonnés qui gardent la lumière.'),
         tags=(None, ['cloisons'], ['cloisons']), badge=False),
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
    ('aa5', 'Couloir : puits de lumière circulaires dans un faux-plafond', ['faux-plafonds'], ['faux-plafonds'],
     'Avant : réservations circulaires dans la dalle d\'un couloir', 'Après : couloir au faux-plafond percé de puits de lumière ronds', True),
    ('aa6', 'Séjour : faux-plafond en périphérie et spots', ['faux-plafonds', 'platrerie-peinture'], ['faux-plafonds'],
     'Avant : séjour avant travaux, devant une grande baie vitrée', 'Après : séjour avec faux-plafond en périphérie et spots', True),
    ('aa3', 'Combles : isolation et rampant fini sous une fenêtre de toit', ['cloisons'], ['cloisons'],
     'Avant : fenêtre de toit, isolant visible et plafond noirci', 'Après : rampant blanc fini autour d\'une fenêtre de toit', False),
    ('aa7', 'Paroi cintrée : de l\'ossature au couloir fini', ['cloisons'], ['cloisons'],
     'Avant : ossature métallique d\'une paroi cintrée', 'Après : couloir fini avec paroi cintrée et spots', False),
    ('aa1', 'Caisson en plaques de plâtre sous une verrière', ['platrerie-peinture'], ['platrerie-peinture'],
     'Avant : caisson en cours, plaques jointoyées sous une verrière', 'Après : caisson en plaques de plâtre fini sous une verrière', False),
    ('aa2', 'Gaine de ventilation cachée dans un couloir', ['faux-plafonds'], ['faux-plafonds'],
     'Avant : gaine de ventilation apparente sous la charpente', 'Après : couloir au plafond lisse, gaine cachée', False),
    ('aa4', 'Appareil de ventilation habillé d\'un caisson', ['platrerie-peinture'], ['platrerie-peinture'],
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
