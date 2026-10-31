# -*- coding: utf-8 -*-
"""Pages services v3 (cro-v3 §6.1, DA « le trait de niveau ») : un gabarit, quatre jeux de textes.

Ordre : en-tête premium (panneau anthracite + grande image) · bande de logos · damier « ce que nous posons » ·
rangée « ce qu'il faut savoir » · bloc propre au service (guide, subventions) · mini-cas sur fond profond (vraies photos)
et projets liés · chantier en 4 étapes · FAQ courte · demande. Un message par bloc, mots clés en gras.
Images : vraies photos d'abord ; sinon illustrations sous licence, toujours signalées « Illustration ».
"""
import re
import ctx
from ctx import e, T, V, definitif, marque, M, PROD
from common import page, hero_page, ld_page, TEL, TEL_URI, devis_btn, svc_nom, svc_url, doc, suivi_doc
import composants as c
import portfolio as pf

ZONES = ['Canton de Genève', 'Canton de Vaud', 'Canton de Neuchâtel', 'Canton de Fribourg', 'Valais romand', 'Canton du Jura', 'Jura bernois']
SZ_DAMIER = '(min-width: 1000px) 330px, (min-width: 640px) 46vw, 100vw'
SZ_FEAT = '(min-width: 1440px) 660px, (min-width: 1000px) 46vw, 100vw'


def prix_q(question, repli):
    """Questions de prix : la fourchette (C31) n'est pas fournie ; le repli s'affiche, signalé en vérification."""
    M('C31')
    return (question, marque('C31', repli), repli)


def img(kind, ident, sizes=SZ_DAMIER, fmt='16x9'):
    return c.media(kind, ident, sizes, fmt=fmt)


def lien_filtre(service, texte_filtre, texte_tous):
    """Lien vers les réalisations filtrées, seulement si le filtre a au moins un projet dans ce mode."""
    n = sum(1 for p in pf.PROJETS if pf.proj_ok(p) and service in pf.proj_tags(p))
    n += sum(1 for x in pf.PAIRES if service in pf.paire_services(x[0]))
    if n:
        return '<a class="link-arrow" href="realisations.html?filtre=%s">%s</a>' % (service, texte_filtre)
    return '<a class="link-arrow" href="realisations.html">%s</a>' % texte_tous


def pro_ligne(texte):
    return '<p class="pro-ligne"><span>%s</span> <a class="link-arrow" href="professionnels.html">Espace professionnels</a></p>' % texte


# ---------------------------------------------------------------- mini-cas et projets liés (vraies photos uniquement)
def cas(p, d):
    """d : titre, media (HTML), lignes [(terme, définition)], tags, codes (marque de vérification), lies (ids de projets)."""
    if not d:
        return ''
    lignes = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % x for x in d['lignes'] if x[1])
    corps = ('<h3 class="cas__titre">%s</h3><span class="laser laser--court" aria-hidden="true"></span><dl class="cas__dl">%s</dl>%s'
             % (d['titre'], lignes, d.get('tags', '')))
    if d.get('codes'):
        corps = marque(d['codes'], corps, bloc=True)
    lies = ''
    for pid in d.get('lies', []):
        x = pf.PROJ[pid]
        if not pf.proj_ok(x):
            continue
        ph = pf.proj_photos(x)[0]
        lies += ('<li class="lie"><a href="realisations.html#%s"><span class="lie__media">%s</span><span class="lie__titre">%s</span></a></li>'
                 % (pid, c.pic_crop(ph, '16x9', '(min-width: 1000px) 400px, (min-width: 640px) 31vw, 100vw', pf.alt(ph)), x['titre']))
    lies = ('<div class="cas__lies"><h3 class="cas__sous">Projets liés</h3><ul class="lies">%s</ul></div>' % lies) if lies else ''
    return '''    <section class="section section--dark on-dark cas" aria-labelledby="cas-titre" data-trait>
      <div class="container">
        <div class="section-head section-head--row">
          <h2 id="cas-titre">%s</h2>
          %s
        </div>
        <div class="cas__main">
          <div class="cas__media">%s</div>
          <div class="cas__txt">
            %s
            <p class="cas__cta">%s</p>
          </div>
        </div>
        %s
      </div>
    </section>
''' % (d['h2'], d.get('lien', ''), d['media'], corps,
       devis_btn(p, 'mini_cas', texte='Un projet semblable ? Demander un devis'), lies)


def cas_projet(pid, h2, fait, lien, lies=(), fmt='16x9'):
    """Mini-cas tiré d'un projet du portfolio (cro-v3 §6.1) : rien d'inventé, « Demande » masquée tant que C25 manque."""
    x = pf.PROJ[pid]
    if not pf.proj_ok(x):
        return None
    ph = pf.proj_photos(x)[0]
    tags = pf.proj_tags(x)
    codes_tags = x['tags'][0] if (x['tags'][0] and not ctx.confirme(x['tags'][0])) else None
    return dict(h2=h2, titre=x['titre'], media=c.pic_crop(ph, fmt, '(min-width: 1000px) 720px, 100vw', pf.alt(ph)),
                lignes=[('Lieu', pf._txt(x['lieu'])), ('Ce que nous avons fait', fait)],
                tags=pf.tags_html(tags, codes_tags), lien=lien, lies=list(lies))


def cas_aa(paire, h2, titre, lieu, fait, lien, codes=None):
    """Mini-cas avant / après (paire réelle) : comparateur sur fond profond."""
    return dict(h2=h2, titre=titre, media=pf.avant_apres(paire, grande=True, sans_legende=True),
                lignes=[('Lieu', lieu), ('Ce que nous avons fait', fait)],
                tags=pf.tags_html(pf.paire_services(paire), 'C26' if (pf.PAIRE[paire][2] != pf.PAIRE[paire][3] and not ctx.confirme('C26')) else None),
                lien=lien, codes=codes)


# ---------------------------------------------------------------- données des quatre pages
def placo():
    s = 'placo'
    return dict(
        service=s, crumb='Placo', title='Placo, cloisons et faux-plafonds à Genève | Andy Construct',
        desc=V('C05', 'Cloisons, doublages et faux-plafonds en plaques de plâtre, posés puis peints. Logements, bureaux et bâtiments publics, à Genève et en Suisse romande.',
               'Cloisons, doublages et faux-plafonds en plaques de plâtre, prêts à peindre. Logements, bureaux et bâtiments publics, à Genève et en Suisse romande.'),
        h1='Placo : cloisons, doublages et faux-plafonds',
        chapeau='Diviser une pièce, redresser un mur, abaisser un plafond : les <b>plaques de plâtre</b> le font sans maçonnerie.',
        btn='Demander un devis pour du placo',
        hero=('photo', 'faux-plafond-placo-gorge-lumineuse-02'),
        faire_h2='Ce que nous posons en plaques de plâtre',
        faire=[('cloisons', 'Cloisons', 'Une chambre, un bureau, une salle de réunion, montés en quelques jours. <b>Portes et renforts</b> prévus dès la pose.',
                img('ill', 'chantier-cloisons-plaques-caissons')),
               ('doublages', 'Doublages', 'Un parement devant un mur abîmé, qui cache les gaines et peut recevoir un isolant contre le '
                '<a href="cloisons-isothermes.html"><b>froid</b></a> ou le <a href="isolation-acoustique.html"><b>bruit</b></a>.',
                img('ill', 'placo-lissage-enduit-mur')),
               ('faux-plafonds', 'Faux-plafonds', 'Il cache conduites et ventilation, reçoit <b>spots et gorges lumineuses</b>, et remplace un plafond abîmé.',
                img('photo', 'plafond-placo-ilot-ovale-01')),
               ('caissons', 'Caissons et habillages', 'Une poutre ou une gaine à cacher : un <b>caisson</b> ajusté, avec trappe de visite si besoin.',
                img('aa', ('aa1', 'apres')))],
        pro=T('C14', 'Professionnels : lots <b>CFC 271 et 283</b>, offres sur plans et descriptifs.',
              'Professionnels : lots <b>CFC 271</b>, offres sur plans et descriptifs.'),
        savoir=[T('C07', 'Poncer les joints fait une poussière fine : zone fermée, passages protégés, <b>nettoyage chaque soir</b>.',
                  'Poncer les joints fait une poussière fine : la zone de travail est <b>fermée et protégée</b>.'),
                'Câbles et gaines passent avant la fermeture : nous <b>coordonnons la pose</b> avec votre électricien.',
                'Sur un grand mur éclairé de côté, les joints se voient : le <b>niveau de finition</b> se choisit à la visite.'],
        savoir_img=img('ill', 'placo-chant-plaque-detail', SZ_FEAT),
        cas=lambda p: cas_projet('projet-hall-gorge-lumineuse', 'Références en placo',
                                 'Faux-plafond en plaques de plâtre aux <b>formes courbes</b>, éclairage et spots intégrés.',
                                 lien_filtre('placo', 'Toutes les réalisations en placo', 'Toutes les réalisations'),
                                 lies=['projet-cage-escalier-niches', 'projet-faux-plafond-dalle-isolee', 'projet-grande-salle-ossature']),
        faq_titre='Questions fréquentes sur le placo',
        faq=[prix_q('Combien coûte une cloison ou un faux-plafond en placo ?',
                    'Le prix dépend de la surface, de la hauteur, de l\'isolant, des portes et des spots. Après la visite, vous recevez une offre écrite.'),
             ('Combien de temps dure la pose ?', 'Pour une cloison ou le plafond d\'une pièce, comptez quelques jours, séchage des joints compris. Le délai figure dans l\'offre.', None),
             ('Une cloison en placo isole-t-elle du bruit ?', 'Une cloison simple atténue les voix. Avec un isolant et deux plaques de chaque côté, elle isole nettement mieux. Voyez <a href="isolation-acoustique.html">l\'isolation acoustique</a>.', None),
             ('Faut-il l\'accord de la régie ou de la copropriété ?', 'Locataire : oui, l\'accord écrit du bailleur. En PPE, une cloison dans votre lot est en général possible ; vérifiez le règlement si elle touche une partie commune.', None)],
        h2_demande='Demander un devis pour du placo',
        ld_desc='Cloisons, doublages, faux-plafonds et caissons en plaques de plâtre, posés puis peints, à Genève et en Suisse romande.',
        service_type='Plâtrerie et faux-plafonds en plaques de plâtre',
    )


def peinture():
    s = 'peinture'
    return dict(
        service=s, crumb='Peinture', title='Entreprise de peinture intérieure à Genève | Andy Construct',
        desc='Peinture des murs et plafonds : appartements, fins de bail, cages d\'escalier, bureaux. Supports préparés, chantier protégé. Genève et Suisse romande.',
        h1='Peinture intérieure : murs, plafonds, cages d\'escalier',
        chapeau='Un appartement à rafraîchir, une fin de bail, une cage d\'escalier : nous <b>préparons les supports</b>, protégeons les lieux, puis peignons.',
        btn='Demander un devis pour de la peinture',
        # Aucune vraie photo de peinture à ce jour (shooting C40) : illustration signalée
        hero=('ill', 'peinture-sejour-murs-blancs'),
        faire_h2='Ce que nous peignons',
        faire=[(None, 'Logements', 'Une pièce ou tout l\'appartement, habité ou vide. Trous et fissures rebouchés <b>avant</b> la peinture.',
                img('ill', 'interieur-appartement-murs-blancs')),
               (None, 'Fins de bail', T('C17', 'Remise en état entre deux locataires, prête pour l\'<b>état des lieux d\'entrée</b>.', ''),
                img('ill', 'peinture-preparation-piece', fmt=None)),
               (None, 'Cages d\'escalier', T('C20', 'Par étages, <b>passage libre</b> pour les habitants.', 'Par étages, dans les <b>parties communes</b>.'),
                img('ill', 'peinture-rouleau-detail')),
               (None, 'Bureaux et commerces', T('C19', '<b>Le soir ou le week-end</b>, pour ne pas fermer.', '<b>Zone par zone</b>, pour limiter la gêne.'),
                img('ill', 'bureaux-plateau-vide'))],
        pro='Professionnels : lot <b>CFC 285</b>, remises en état et parties communes, offres sur descriptif.',
        savoir=[T('C06', 'La préparation figure <b>sur une ligne à part</b> de l\'offre : vous voyez ce que vous payez.',
                  'La <b>préparation des supports</b> compte autant que la peinture.'),
                'Une fissure revient si sa <b>cause</b> n\'est pas traitée : nous vous le disons à la visite.',
                'Nous peignons <b>à l\'intérieur</b> seulement : pas de façades.'],
        savoir_img=img('ill', 'peinture-rouleau-mur-blanc', SZ_FEAT),
        # Mini-cas : la paire AA6 seulement si la prestation peinture est confirmée (C26) ; sinon masqué (règle v2)
        cas=lambda p: cas_aa('aa6', 'Référence en peinture', 'Séjour : faux-plafond en périphérie et spots', 'Appartement',
                             'Faux-plafond en périphérie avec spots, puis <b>peinture</b>.',
                             '<a class="link-arrow" href="realisations.html#avant-apres">Tous les avant / après</a>', codes='C26') if definitif('C26') else None,
        faq_titre='Questions fréquentes sur la peinture',
        faq=[prix_q('Combien coûte la peinture d\'un appartement ?',
                    'Le prix dépend de la surface des murs et des plafonds, de leur état, de la hauteur et des meubles à déplacer.'),
             c.Q('C20', 'Peut-on rester chez soi pendant les travaux ?', 'Oui. Nous travaillons pièce par pièce, couvrons les meubles et gardons un passage libre.'),
             c.Q('C17', 'Faut-il vider les pièces ?', 'Non. Retirez les objets fragiles et ce qui est accroché aux murs ; nous déplaçons et couvrons les meubles.',
                 'Retirez au moins les objets fragiles et ce qui est accroché aux murs. Le reste se décide à la visite.'),
             ('Peignez-vous aussi les façades ?', 'Non. Nous travaillons à l\'intérieur : murs, plafonds, cages d\'escalier et parties communes.', None)],
        h2_demande='Demander un devis pour de la peinture',
        ld_desc='Peinture intérieure des murs et plafonds : logements, fins de bail, cages d\'escalier et bureaux, à Genève et en Suisse romande.',
        service_type='Peinture intérieure',
    )


def acoustique():
    s = 'isolation-acoustique'
    reelle = pf.photo_ok('panneaux-acoustiques-muraux-01')          # C18 en production
    salle = pf.photo_ok('cadre-acoustique-salle-de-reunion-01')
    guide = doc('guide-bruit')
    specifique = ''
    if guide:
        couv = ('<picture><source type="image/webp" srcset="assets/img/docs/guide-reduire-le-bruit-couverture-320.webp 320w, '
                'assets/img/docs/guide-reduire-le-bruit-couverture-640.webp 640w" sizes="(min-width: 1000px) 300px, 60vw">'
                '<img src="assets/img/docs/guide-reduire-le-bruit-couverture-640.jpg" width="640" height="906" alt="Couverture du guide « Réduire le bruit chez soi »" loading="lazy" decoding="async"></picture>')
        specifique = c.feat('guide-titre', 'Guide : réduire le bruit chez soi',
                            '<p>Ce qui marche, ce qui ne marche pas, et les <b>questions à poser</b> à toute entreprise. %d pages.</p>'
                            '<p><a class="btn" href="%s" %s>Télécharger le guide (%s)</a></p>%s'
                            % (guide[2], guide[0], suivi_doc('guide-bruit'), guide[1], c.form_guide_poste('guide-reduire-le-bruit')),
                            '<span class="couv">%s</span>' % couv, inverse=True, cls='feat--doc')
    return dict(
        service=s, crumb='Isolation acoustique', title='Isolation phonique et acoustique à Genève | Andy Construct',
        desc='Vous entendez vos voisins ? Doublages, faux-plafonds et cloisons acoustiques, correction de l\'écho dans les salles. Genève et Suisse romande.',
        h1='Isolation phonique et acoustique : moins de bruit chez vous',
        chapeau='Voisins, télévision, pas à l\'étage, voix en réunion : nous isolons <b>murs et plafonds</b> pour que le bruit passe moins.',
        btn='Demander un devis pour une isolation acoustique',
        hero=('photo', 'panneaux-acoustiques-muraux-01') if reelle else ('ill', 'acoustique-couloir-panneaux-plafond'),
        avant='''    <section class="section section--tight duo-mots" aria-labelledby="isoler-titre">
      <div class="container">
        <h2 id="isoler-titre" class="visually-hidden">Isoler ou corriger : deux problèmes différents</h2>
        <div class="duo-mots__grid">
          <div><p class="duo-mots__mot">Isoler</p><p>Empêcher le bruit de <b>passer d'un local à l'autre</b> : voisin, étage, pièce d'à côté.</p></div>
          <div><p class="duo-mots__mot">Corriger</p><p>Réduire <b>l'écho dans la pièce</b> : salle de réunion, réfectoire, salle communale.</p></div>
        </div>
        <p class="duo-mots__pied">À la visite, nous commençons par identifier ce que vous entendez.</p>
      </div>
    </section>
''',
        faire_h2='Ce que nous posons contre le bruit',
        faire=[(None, 'Doublage acoustique', 'Ossature indépendante, laine minérale et plaques : contre les <b>voix et la télévision</b> du voisin.',
                img('ill', 'placo-lissage-enduit-mur')),
               (None, 'Faux-plafond acoustique', 'Suspendu par des attaches qui <b>amortissent les vibrations</b>, avec un isolant : moins de voix venant d\'en haut.',
                img('ill', 'isolation-ossature-metallique-plafond')),
               (None, 'Cloison acoustique', 'Deux ossatures séparées et des plaques doublées, pour une chambre, un bureau ou un cabinet <b>confidentiel</b>.',
                img('ill', 'chantier-cloisons-plaques-caissons')),
               ('correction', 'Correction des salles', T('C18', 'Plafonds perforés et panneaux qui <b>absorbent l\'écho</b> : salles de réunion, salles communales, classes.', ''),
                img('ill', 'acoustique-panneaux-muraux'))],
        pro=T('C14', 'Professionnels : lots <b>CFC 271 et 283</b>.', 'Professionnels : lot <b>CFC 271</b>.'),
        savoir=['Les <b>bruits de pas</b> se traitent le mieux à la source, dans le sol du voisin.',
                'Le bruit passe aussi <b>par les côtés</b> : prises, gaines, portes, murs voisins.',
                'Personne ne peut promettre un résultat <b>en décibels</b> sans mesure.' + T('C15', ' Une exigence SIA 181 est fixée par le projet.', '')],
        savoir_img=img('ill', 'acoustique-couloir-panneaux-plafond' if reelle else 'plafond-retombees-courbes-bureaux', SZ_FEAT),
        specifique=specifique,
        cas=lambda p: cas_projet('projet-salle-de-reunion', 'Référence en acoustique',
                                 'Un grand <b>panneau mural absorbant</b> réduit l\'écho de la salle.',
                                 lien_filtre('isolation-acoustique', 'Toutes les réalisations en acoustique', 'Toutes les réalisations')) if salle else None,
        faq_titre='Questions fréquentes sur le bruit',
        faq=[('Comment réduire le bruit des voisins du dessus ?', 'Pour les voix, un faux-plafond acoustique sur attaches antivibratiles. Pour les pas, il faut agir sur le sol du voisin.', None),
             ('Les panneaux en mousse isolent-ils du bruit ?', 'Non. Ils réduisent un peu l\'écho, sans empêcher le bruit de passer.', None),
             prix_q('Combien coûte une isolation phonique ?', 'Le prix dépend de la surface, du type de travaux et des points faibles à traiter.'),
             c.Q('C18', 'Combien de place perd-on ?', 'Un doublage acoustique prend en général 7 à 10 cm. Nous mesurons avant de proposer.',
                 'Quelques centimètres. Nous mesurons avant de proposer.')],
        h2_demande='Demander un devis pour une isolation acoustique',
        ld_desc='Isolation phonique des murs et plafonds (doublages, faux-plafonds et cloisons acoustiques) et correction de l\'écho des salles, à Genève et en Suisse romande.',
        service_type='Isolation acoustique',
    )


def isolantes():
    s = 'cloisons-isothermes'
    sing = T('C16', 'une cloison isolante', 'une cloison isotherme')
    return dict(
        service=s, crumb=svc_nom(s), title=V('C16', 'Cloisons isolantes, cave et garage à Genève | Andy Construct', 'Cloisons isothermes, cave et garage à Genève | Andy Construct'),
        desc='Cloisons isolantes (isothermes) entre pièces chauffées et caves, garages ou combles, en plaques de plâtre. Genève et Suisse romande.',
        h1='Cloisons isothermes et isolantes : caves, garages et combles',
        chapeau='Une chambre au-dessus du garage, un bureau contre une cave, des combles : %s garde la chaleur <b>côté chauffé</b>.'
                % T('C16', 'la cloison isolante', 'la cloison isotherme'),
        precision=T('C16', 'Nous ne posons pas de chambres froides.', ''),
        btn='Demander un devis pour ' + sing,
        hero=('photo', 'chantier-ossature-puits-de-lumiere-02'),
        faire_h2='Ce que nous posons pour garder la chaleur',
        faire=[(None, T('C16', 'Cloison isolante', 'Cloison isotherme'), 'Entre une pièce chauffée et un garage, une cave ou un atelier : ossature, <b>isolant thermique</b>, plaques.',
                img('ill', 'isolation-ossature-metallique-plafond')),
               (None, 'Doublage d\'un mur froid', 'Un mur contre la terre ou l\'extérieur reste froid ? Un doublage isolant, <b>côté pièce</b>, améliore le confort.',
                img('ill', 'placo-lissage-enduit-mur')),
               (None, 'Plafond de cave ou de garage', 'Le sol du dessus est froid ? Un isolant <b>sous la dalle</b>, fermé par des plaques si le local le demande.',
                img('photo', 'chantier-suspentes-ossature-01')),
               (None, 'Combles et rampants', T('C16', 'Isolant entre ou sous les chevrons, puis plaques : les combles deviennent une <b>pièce habitable</b>.', ''),
                img('ill', 'combles-amenages-fenetres-de-toit'))],
        pro='Professionnels : caves, parkings et locaux techniques d\'immeubles, sur plans.',
        savoir=['Sur un mur enterré, on vérifie <b>l\'humidité</b> d\'abord : un isolant sur un mur mouillé crée des problèmes.',
                'Le <b>pare-vapeur</b> se pose du côté chauffé ; mal placé, il fait condenser l\'humidité.',
                'Entre garage et logement, des exigences de <b>protection incendie</b> peuvent s\'appliquer.' + T('C15', ' Nous choisissons les plaques en conséquence.', '')],
        savoir_img=img('ill', 'ambiance-plans-blancs-lumiere', SZ_FEAT),
        specifique='''    <section class="section section--tight" aria-labelledby="subv-titre">
      <div class="container">
        <div class="encadre encadre--large">
          <h2 id="subv-titre">Des subventions sont-elles possibles ?</h2>
          <p>Certaines isolations thermiques sont subventionnables : la demande se dépose <b>avant</b> les travaux, auprès du service de l'énergie du canton%s</p>
        </div>
      </div>
    </section>
''' % T('C43', ' ; nous fournissons les informations techniques.', '.'),
        cas=lambda p: dict(cas_aa('aa3', 'Référence en isolation', 'Combles : isolation et rampant fini sous une fenêtre de toit', '',
                                  'Isolation des combles et <b>rampant fini</b> autour d\'une fenêtre de toit.',
                                  lien_filtre('cloisons-isothermes', 'Toutes les réalisations', 'Toutes les réalisations'), codes='C26'),
                           lies=[]),   # la grande salle (puits de lumière) est déjà la photo de l'en-tête
        faq_titre='Questions fréquentes sur l\'isolation intérieure',
        faq=[c.Q('C16', 'Qu\'est-ce qu\'une cloison isotherme ?',
                 'Une cloison isolante, entre une pièce chauffée et un local qui ne l\'est pas. Ce n\'est pas une chambre froide.',
                 'Une cloison isolante, entre une pièce chauffée et un local qui ne l\'est pas.'),
             c.Q('C16', 'Faut-il une autorisation pour aménager des combles ?', 'Parfois une autorisation de construire, selon le canton et la commune : renseignez-vous avant.'),
             ('Quelle épaisseur d\'isolant faut-il ?', 'Elle dépend des températures et des exigences du canton ; nous la proposons dans l\'offre.', None),
             prix_q('Combien coûte une cloison isolante ?', 'Le prix dépend de la surface, de l\'épaisseur d\'isolant, des portes et de la finition.')],
        h2_demande='Demander un devis pour ' + sing,
        ld_desc='Cloisons et doublages isolants (isothermes) entre pièces chauffées et caves, garages ou combles, en plaques de plâtre, à Genève et en Suisse romande.',
        service_type=V('C16', 'Cloisons isolantes et isolation intérieure', 'Cloisons isothermes et isolation intérieure'),
        alternate=V('C16', 'Cloisons isothermes', 'Cloisons isolantes'),
    )


# ---------------------------------------------------------------- gabarit
def methode_courte():
    etapes = [('Visite', 'Mesures et conseils, sur place.'),
              ('Offre écrite', T('C06', 'Poste par poste, <b>en CHF</b>.', 'Remise après la visite.')),
              ('Chantier protégé', T('C07', 'Lieux protégés, <b>nettoyés chaque soir</b>.', 'Lieux protégés pendant les travaux.')),
              ('Réception', 'Le tour des finitions, <b>ensemble</b>.')]
    return '''    <section class="section section--tight" aria-labelledby="chantier-titre">
      <div class="container">
        <div class="section-head section-head--row">
          <h2 id="chantier-titre">Un chantier en quatre étapes</h2>
          <a class="link-arrow" href="entreprise.html#methode">Notre méthode en détail</a>
        </div>
        <ol class="steps steps--court">%s</ol>
      </div>
    </section>
''' % ''.join('<li><h3>%s</h3><p>%s</p></li>' % x for x in etapes)


def rendre(d):
    s = d['service']
    fichier = svc_url(s)
    hero_html, preload = c.hero_image(*d['hero'])
    p = dict(fichier=fichier, formulaire=True, service=s, title=d['title'], desc=d['desc'], preload=preload)
    faq = [q if len(q) == 3 and q[2] is not None else (q[0], q[1], q[1]) for q in d['faq'] if q]
    faq = [(q, a, re.sub(r'<[^>]+>', '', t)) for q, a, t in faq]
    faq_html, faq_ld = c.faq_items(faq)
    url = PROD + fichier
    service_ld = {'@type': 'Service', '@id': url + '#service', 'name': ctx.fr(svc_nom(s, html=False)), 'serviceType': d['service_type'],
                  'description': d['ld_desc'], 'provider': {'@id': PROD + '#entreprise'}, 'url': url,
                  'areaServed': [{'@type': 'AdministrativeArea', 'name': z} for z in ZONES]}
    if d.get('alternate'):
        service_ld['alternateName'] = d['alternate']
    ld = ld_page(fichier, d['title'], svc_nom(s, html=False), extra={'about': {'@id': url + '#service'}})
    ld['@graph'].append(service_ld)
    p['ld'] = [ld, c.faq_ld(url, faq_ld)]

    precision = ('<p class="hero__note">%s</p>' % d['precision']) if d.get('precision') else ''
    actions = '%s<a class="btn btn--light" href="%s" data-suivi-numero="fixe" data-suivi-emplacement="entete_page">Appeler le %s</a>' % (
        devis_btn(p, 'entete_page', texte=d['btn']), TEL_URI, TEL)
    corps = hero_page(d['crumb'], d['h1'], d['chapeau'], actions=actions, media=hero_html, extra=precision,
                      badges=c.badges(['|B11|B4', '|B6|B3', 'B1'], cls='badges--3'))
    corps += c.bande_refs(service=s)
    corps += d.get('avant', '')
    corps += '''    <section class="section" aria-labelledby="faire-titre">
      <div class="container">
        <div class="section-head"><h2 id="faire-titre">%s</h2></div>
        %s
        %s
      </div>
    </section>
''' % (d['faire_h2'], c.damier(d['faire']), pro_ligne(d['pro']))
    corps += c.feat('savoir-titre', 'Ce qu\'il faut savoir avant de commencer', c.points(d['savoir']), d['savoir_img'], cls='section--mist')
    corps += d.get('specifique', '')
    corps += cas(p, d['cas'](p))
    corps += methode_courte()
    corps += '''    <section class="section faq" aria-labelledby="faq-titre">
      <div class="container split split--48">
        <div class="faq__head"><h2 id="faq-titre">%s</h2><p>Une autre question ? Appelez le <a href="%s" data-suivi-numero="fixe" data-suivi-emplacement="faq">%s</a>.</p></div>
        <div class="faq__list">%s</div>
      </div>
    </section>
''' % (d['faq_titre'], TEL_URI, TEL, faq_html)
    corps += c.bloc_demande(p, service=s, h2=d['h2_demande'], source='page-' + s, surtitre=False)
    page(p, corps)


def build():
    for f in (placo, peinture, acoustique, isolantes):
        rendre(f())
