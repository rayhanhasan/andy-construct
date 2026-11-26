# -*- coding: utf-8 -*-
"""Pages services v5 (document « Contenu site web » du client, mis en page selon la DA « le trait de niveau ») : un gabarit, quatre jeux de textes.

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


# ---------------------------------------------------------------- blocs v5 (document « Contenu site web » du client)
import schemas as sch
from icons import ICONS

# Normes et prescriptions par service (tableau du document client ; SIA 256 et 257 vérifiées : faux-plafonds, peinture)
NORMES = [
    ('isolation-acoustique', 'Isolation acoustique et phonique', 'SIA 181 · SIA 242 · AEAI',
     'Protection contre le bruit entre locaux, construction à sec, sécurité incendie des matériaux.'),
    ('faux-plafonds', 'Faux plafonds', 'SIA 256 · SN EN 13964 · SIA 181 · AEAI',
     'Conception et exécution des plafonds suspendus, performances phoniques, résistance au feu (EI 30, EI 60, EI 90).'),
    ('cloisons', 'Cloisons et doublages', 'SIA 242 · SIA 181 · SIA 180 · AEAI',
     'Construction à sec, isolation phonique et thermique, cloisons coupe-feu (EI 30, EI 60, EI 90).'),
    ('cloisons.html#panneaux-sandwich', 'Panneaux sandwich isothermes', 'SN EN 14509 · SIA 180 · AEAI · OHyg',
     'Panneaux certifiés, isolation thermique, âme isolante adaptée aux exigences incendie, hygiène des locaux alimentaires.'),
    ('platrerie-peinture', 'Plâtrerie et peinture', 'SIA 242 · SIA 257 · SIA 118',
     'Classes de qualité des enduits, préparation des supports et peinture, conditions générales des travaux.'),
]


def normes_table(seulement=None, titre_id='normes-titre', h2='Des solutions qui répondent aux normes suisses', cls=''):
    """Tableau des normes (accueil : toutes les lignes ; page service : ses lignes, sans titre de colonne « Service » redondant)."""
    lignes = [n for n in NORMES if not seulement or n[0].split('.')[0] in seulement]
    trs = ''.join('<tr><th scope="row"><a href="%s">%s</a></th><td class="normes__codes">%s</td><td>%s</td></tr>'
                  % (k if k.endswith('.html') or '#' in k else k + '.html', nom, codes, quoi) for k, nom, codes, quoi in lignes)
    return '''    <section class="section normes%s" aria-labelledby="%s">
      <div class="container">
        <div class="section-head">
          <p class="surtitre">Normes et conformité</p>
          <h2 id="%s">%s</h2>
          <p class="lead">Pour chacun de nos services, nous mettons en œuvre des systèmes certifiés, dans le respect des normes et prescriptions en vigueur.</p>
        </div>
        <div class="normes__wrap"><table class="normes__table">
          <thead><tr><th scope="col">Service</th><th scope="col">Normes et prescriptions</th><th scope="col">Ce qu'elles encadrent</th></tr></thead>
          <tbody>%s</tbody>
        </table></div>
        <p class="normes__pied">Les performances exigées sont définies pour chaque projet avec le maître d'ouvrage et ses mandataires.</p>
      </div>
    </section>
''' % ((' ' + cls) if cls else '', titre_id, titre_id, h2, trs)


def atouts(items, titre_id, h2, cls=''):
    """Trois bénéfices côte à côte : pictogramme, titre, une phrase."""
    lis = ''.join('<li class="atout"><span class="atout__ico">%s</span><div><h3>%s</h3><p>%s</p></div></li>' % (ICONS[i], t, x) for i, t, x in items)
    return '''    <section class="section section--tight atouts-s%s" aria-labelledby="%s">
      <div class="container">
        <h2 id="%s" class="visually-hidden">%s</h2>
        <ul class="atouts">%s</ul>
      </div>
    </section>
''' % ((' ' + cls) if cls else '', titre_id, titre_id, h2, lis)


def media_type(photo, schema):
    """Vraie photo si publiable dans ce mode, sinon le schéma en coupe."""
    if photo and pf.photo_ok(photo):
        return '<span class="type__media type__media--photo">%s</span>' % c.pic_crop(photo, '16x9', '(min-width: 1100px) 400px, (min-width: 700px) 46vw, 100vw', pf.alt(photo))
    return '<span class="type__media">%s</span>' % schema


def types(p, items, titre_id, surtitre, h2, lead, cta, cls=''):
    """Grille de solutions : chaque carte = image (photo ou schéma) + titre (+ « Notre spécialité ») + texte ; la dernière
    carte est un appel à l'action sur fond anthracite. items : (ancre, titre, texte, photo, schéma, spécialité)."""
    lis = ''
    for ancre, titre, texte, photo, schema, spec in items:
        lis += ('<li class="type%s" id="%s">%s<div class="type__txt"><h3>%s%s</h3><p>%s</p></div></li>'
                % (' type--spec' if spec else '', ancre, media_type(photo, schema), titre,
                   ' <span class="tag-spec">Notre spécialité</span>' if spec else '', texte))
    ct, cx, cb = cta
    n = len(items) + 1
    large = (' type--cta-3' if n % 3 == 2 else '') + (' type--cta-2' if n % 2 == 1 else '')
    lis += ('<li class="type type--cta%s"><div class="type__txt"><h3>%s</h3><p>%s</p>%s</div></li>'
            % (large, ct, cx, devis_btn(p, 'carte_conseil', cls='btn btn--light', texte=cb)))
    return '''    <section class="section%s" aria-labelledby="%s">
      <div class="container">
        <div class="section-head">
          <p class="surtitre">%s</p>
          <h2 id="%s">%s</h2>
          %s
        </div>
        <ul class="types" data-reveal="cells">%s</ul>
      </div>
    </section>
''' % ((' ' + cls) if cls else '', titre_id, surtitre, titre_id, h2, ('<p class="lead">%s</p>' % lead) if lead else '', lis)


def bande(titre_id, surtitre, h2, paras, visuel, puces=None, action='', ancre=None):
    """Bande « spécialité » sur fond anthracite : visuel à gauche (schéma et usages), texte à droite."""
    puces_html = ('<ul class="bande__puces">%s</ul>' % ''.join('<li>%s</li>' % x for x in puces)) if puces else ''
    return '''    <section class="section section--dark on-dark bande"%s aria-labelledby="%s">
      <div class="container bande__grid">
        <div class="bande__visuel" data-reveal>%s%s</div>
        <div class="bande__txt">
          <p class="surtitre surtitre--clair">%s</p>
          <h2 id="%s">%s</h2>
          %s
          %s
        </div>
      </div>
    </section>
''' % ((' id="%s"' % ancre) if ancre else '', titre_id, visuel, puces_html, surtitre, titre_id, h2,
       ''.join('<p%s>%s</p>' % (' class="lead"' if i == 0 else '', x) for i, x in enumerate(paras)), action)


def intro(titre_id, h2, paras, img=''):
    """Texte d'introduction (2 à 3 paragraphes) à côté d'une image."""
    return c.feat(titre_id, h2, ''.join('<p>%s</p>' % x for x in paras), img) if img else '''    <section class="section section--tight" aria-labelledby="%s">
      <div class="container intro-s"><h2 id="%s">%s</h2>%s</div>
    </section>
''' % (titre_id, titre_id, h2, ''.join('<p>%s</p>' % x for x in paras))


def photo_ou(pid, repli_kind, repli_ident, sizes=SZ_FEAT):
    if pf.photo_ok(pid):
        return c.pic(pid, sizes, pf.alt(pid))
    return img(repli_kind, repli_ident, sizes)


BENEFICES = [('echo', 'Correction acoustique', 'Moins d\'écho et de résonance à l\'intérieur de la pièce.'),
             ('phonique', 'Isolation phonique', 'Le bruit ne passe plus d\'un étage ou d\'une pièce à l\'autre.'),
             ('feu', 'Coupe-feu', 'Des solutions conformes aux exigences de sécurité incendie.')]


# ---------------------------------------------------------------- données des quatre pages
def faux_plafonds():
    s = 'faux-plafonds'
    hero = 'piscine-plafond-tendu-lumineux-01'
    return dict(
        service=s, crumb='Faux plafonds', title='Faux plafonds à Genève : tissu tendu, plâtre, métal | Andy Construct',
        desc='Faux plafonds acoustiques, phoniques et coupe-feu : tissu tendu, plaque de plâtre, fibre minérale, métal, fibre de bois. Bureaux, restaurants, écoles, logements. Suisse romande.',
        h1='Des plafonds qui transforment le confort de vos espaces',
        chapeau='Le plafond structure l\'espace, améliore le <b>confort sonore</b> et participe à l\'identité de votre lieu.',
        btn='Demander un devis pour un faux plafond',
        hero=('photo', hero),
        apres_refs=intro('fp-intro', 'Performance technique et rendu esthétique', [
            'Nous concevons et posons des plafonds qui allient <b>performance technique</b> et <b>rendu esthétique</b>.',
            'Nos plafonds réduisent la résonance dans une pièce et limitent la transmission du bruit entre les espaces : <b>bureaux, restaurants, salles de réunion, écoles ou logements</b>.'],
            img('photo', 'combles-amenages-charpente-01', SZ_FEAT, fmt='4x5'))
        + atouts(BENEFICES, 'fp-atouts', 'Ce que nos plafonds apportent'),
        blocs=lambda p: types(p, [
            ('tissu-tendu', 'Tissu tendu', 'Une surface parfaitement lisse et sur mesure, posée à froid. En version acoustique, elle absorbe le son tout en restant élégante. Idéale pour les bureaux, restaurants et salles de réunion.',
             'tissu-tendu-cadres-espace-vitre-01', sch.tissu_tendu(), True),
            ('plaque-de-platre', 'Plaque de plâtre', 'Polyvalente, elle permet des plafonds lisses, des caissons, des jeux de niveaux et l\'éclairage intégré. Elle existe en versions phoniques et coupe-feu.',
             'couloir-plafond-ligne-lumineuse-01', sch.plaque_platre(), False),
            ('fibre-de-bois', 'Isolation en fibre de bois', 'Un isolant naturel posé au-dessus du faux plafond, invisible une fois les travaux terminés. Il renforce l\'isolation thermique et phonique, quelle que soit la finition choisie.',
             None, sch.fibre_bois(), False),
            ('fibre-minerale', 'Fibre minérale', 'Des dalles démontables qui gardent les réseaux techniques accessibles. Une solution efficace et économique pour les bureaux et les locaux professionnels.',
             'plafond-dalles-couloir-01', sch.fibre_minerale(), False),
            ('metallique', 'Métallique', 'Des bacs métalliques résistants, faciles d\'entretien, et acoustiques en version perforée. Pour les commerces, couloirs, cuisines professionnelles et espaces très fréquentés.',
             'plafond-bacs-metalliques-cuisine-01', sch.metallique(), False)],
            'fp-types', 'Nos plafonds', 'Cinq solutions, un plafond adapté à chaque usage', '',
            ('Vous hésitez entre plusieurs solutions ?', 'Nous analysons votre espace et vous conseillons le plafond le plus adapté à votre usage, à vos contraintes et à votre budget.', 'Demander conseil')),
        normes=['faux-plafonds'],
        cas=lambda p: cas_projet('projet-salon-ovales', 'Références en faux plafonds',
                                 'Îlots ovales en <b>tissu tendu</b>, bordés d\'un éclairage indirect.',
                                 lien_filtre('faux-plafonds', 'Toutes les réalisations en faux plafonds', 'Toutes les réalisations'),
                                 lies=['projet-ilots-tissu-tendu', 'projet-couronnes-lumineuses', 'projet-plafonds-metalliques']),
        faq_titre='Questions fréquentes sur les faux plafonds',
        faq=[('Quel faux plafond choisir pour réduire l\'écho ?', 'Un plafond absorbant : tissu tendu acoustique, plaques perforées ou dalles en fibre minérale. Nous le choisissons selon l\'usage de la pièce.', None),
             ('Peut-on garder l\'accès aux réseaux techniques ?', 'Oui : les dalles en fibre minérale ou les bacs métalliques se démontent. En plaque de plâtre, nous prévoyons des trappes de visite.', None),
             prix_q('Combien coûte un faux plafond ?', 'Le prix dépend de la surface, de la hauteur, du système choisi et des exigences acoustiques ou incendie. Après la visite, vous recevez une offre écrite.'),
             ('Un faux plafond peut-il être coupe-feu ?', 'Oui. Plaques et systèmes certifiés existent en EI 30, EI 60 ou EI 90, selon les exigences du projet.', None)],
        h2_demande='Demander un devis pour un faux plafond',
        ld_desc='Faux plafonds acoustiques, phoniques et coupe-feu en tissu tendu, plaque de plâtre, fibre minérale, métal, avec isolant en fibre de bois, à Genève et en Suisse romande.',
        service_type='Faux plafonds',
    )


def cloisons():
    s = 'cloisons'
    hero = 'piece-combles-platrerie-peinture-01'
    return dict(
        service=s, crumb='Cloisons', title='Cloisons et doublages à Genève : plâtre, vitrées, isothermes | Andy Construct',
        desc='Cloisons en plaques de plâtre, mobiles, vitrées et aluminium, doublages thermiques et phoniques, panneaux sandwich isothermes. Bureaux et bâtiments professionnels, Suisse romande.',
        h1='Cloisons et doublages',
        chapeau='Créer de nouveaux espaces, réorganiser des surfaces, améliorer les performances <b>thermiques et acoustiques</b> d\'un bâtiment.',
        btn='Demander un devis pour des cloisons',
        hero=('photo', hero),
        apres_refs=intro('cl-intro', 'Des solutions adaptées à chaque projet', [
            'Andy Construct conçoit et réalise des solutions de <b>cloisonnement</b> et de <b>doublage</b> adaptées aux exigences de chaque projet.',
            'Qu\'il s\'agisse de créer de nouveaux espaces, de réorganiser des surfaces existantes ou d\'améliorer les performances d\'un bâtiment, nous proposons des solutions techniques et esthétiques adaptées aux <b>environnements professionnels</b>.']),
        blocs=lambda p: types(p, [
            ('plaques-de-platre', 'Cloisons en plaques de plâtre', 'Pour aménager et redistribuer les espaces intérieurs : des séparations fonctionnelles, en version acoustique, thermique ou coupe-feu selon les exigences du projet.',
             'couloir-plafond-ligne-lumineuse-01', sch.cloison_platre(), False),
            ('mobiles', 'Cloisons mobiles et amovibles', 'Des solutions flexibles pour faire évoluer les espaces : moduler les volumes, créer des zones de travail indépendantes ou transformer rapidement la configuration des locaux.',
             None, sch.cloison_mobile(), False),
            ('vitrees', 'Parois vitrées', 'Luminosité, transparence et élégance : elles délimitent les bureaux et les salles de réunion tout en préservant une sensation d\'ouverture.',
             'cloisons-modulaires-vitrees-02', sch.paroi_vitree(), False),
            ('aluminium', 'Cloisons aluminium', 'Des systèmes pleins, vitrés ou mixtes. Leur modularité et leur finition soignée répondent aux exigences des bureaux, espaces commerciaux et bâtiments professionnels.',
             None, sch.cloison_alu(), False),
            ('doublages', 'Doublages thermiques et phoniques', 'Adaptés au confort du bâtiment : ils limitent les déperditions thermiques, améliorent le confort acoustique et contribuent à la performance globale des espaces.',
             'combles-amenages-charpente-01', sch.doublage(), False)],
            'cl-types', 'Nos solutions de cloisonnement', 'Créer, moduler, isoler', '',
            ('Quelle solution pour votre projet ?', 'Nous étudions vos contraintes et vous orientons vers le système le plus adapté.', 'Nous contacter'))
        + bande('sandwich-titre', 'Notre spécialité', 'Panneaux sandwich isothermes', [
            'Andy Construct développe un savoir-faire particulier dans la mise en œuvre de <b>panneaux sandwich isothermes</b>.',
            'Ces panneaux sont une solution performante pour les parois et les plafonds qui demandent une isolation thermique et une finition adaptée aux contraintes des environnements professionnels.',
            'Nous accompagnons chaque projet dans le choix des solutions et leur mise en œuvre, en tenant compte des contraintes techniques, des dimensions et de l\'utilisation des locaux.'],
            sch.sandwich(), puces=['Locaux techniques', 'Espaces de stockage', 'Zones de préparation', 'Environnements à température maîtrisée'],
            ancre='panneaux-sandwich'),
        normes=['cloisons'],
        cas=lambda p: cas_projet('projet-cloisons-vitrees', 'Référence en cloisons', 'Cloisons <b>modulaires vitrées</b> : des bureaux séparés qui gardent la lumière.',
                                 lien_filtre('cloisons', 'Toutes les réalisations en cloisons', 'Toutes les réalisations'), lies=[])
                        if pf.proj_ok(pf.PROJ['projet-cloisons-vitrees']) else
                        cas_aa('aa7', 'Référence en cloisons', 'Paroi cintrée : de l\'ossature au couloir fini', '',
                               'Ossature métallique cintrée, puis <b>plaques et finitions</b>.', lien_filtre('cloisons', 'Toutes les réalisations', 'Toutes les réalisations')),
        faq_titre='Questions fréquentes sur les cloisons',
        faq=[('Une cloison en plaques de plâtre isole-t-elle du bruit ?', 'Une cloison simple atténue les voix. Avec un isolant et des plaques doublées, elle isole nettement mieux. Voyez <a href="isolation-acoustique.html">l\'acoustique</a>.', None),
             ('Peut-on déplacer une cloison mobile soi-même ?', 'Les cloisons mobiles se manœuvrent sans outils. Les cloisons amovibles se démontent et se remontent ailleurs : nous nous en chargeons.', None),
             ('Les panneaux sandwich conviennent-ils aux locaux alimentaires ?', 'Oui, avec des panneaux certifiés adaptés aux exigences d\'hygiène et d\'incendie du local, choisis avec vous.', None),
             prix_q('Combien coûte une cloison ?', 'Le prix dépend du système, de la surface, de la hauteur, des portes et vitrages, et des exigences acoustiques ou incendie.')],
        h2_demande='Demander un devis pour des cloisons',
        ld_desc='Cloisons en plaques de plâtre, mobiles, vitrées et aluminium, doublages thermiques et phoniques, panneaux sandwich isothermes, à Genève et en Suisse romande.',
        service_type='Cloisons et doublages', alternate='Panneaux sandwich isothermes',
    )


def platrerie_peinture():
    s = 'platrerie-peinture'
    return dict(
        service=s, crumb='Plâtrerie & peinture', title='Plâtrerie et peinture intérieure à Genève | Andy Construct',
        desc='Plâtrerie, enduits et lissages, peinture intérieure et conseil couleur : du support brut à la dernière couche. Construction, rénovation, transformation. Suisse romande.',
        h1='Plâtrerie et peinture',
        chapeau='Du support brut à la dernière couche de peinture : des <b>surfaces impeccables</b> pour vos projets neufs et vos rénovations.',
        btn='Demander un devis pour de la plâtrerie ou de la peinture',
        hero=('photo', 'combles-amenages-charpente-01'),
        apres_refs=intro('pp-intro', 'Le savoir-faire qui fait la différence', [
            'Nous réalisons des travaux de plâtrerie et de peinture dans le cadre de projets de <b>construction</b>, de <b>rénovation</b> et de <b>transformation</b> des espaces professionnels.',
            'Ce sont les finitions qui donnent à un espace son caractère et révèlent la qualité de tout le travail réalisé en amont.']),
        blocs=lambda p: types(p, [
            ('platrerie', 'Plâtrerie', 'Pose de plaques de plâtre, traitement des joints et des angles, réparation des murs et plafonds. Des supports droits et sains, prêts à recevoir la finition.',
             'couloir-plafond-ligne-lumineuse-01', sch.platrerie(), False),
            ('enduits', 'Enduits et lissages', 'Ils effacent les défauts et donnent une surface parfaitement plane : l\'étape clé pour une peinture sans imperfections, même en lumière rasante.',
             None, sch.enduit(), False),
            ('peinture', 'Peinture intérieure', 'Murs, plafonds, portes et boiseries : des peintures de qualité, adaptées à l\'usage de chaque pièce, pour un rendu homogène et durable.',
             None, sch.peinture(), False),
            ('finitions', 'Finitions et conseil couleur', 'Mat, satiné ou brillant : nous vous conseillons sur les teintes et les finitions selon la lumière, l\'usage et l\'entretien souhaité.',
             None, sch.finitions(), False)],
            'pp-types', 'Plâtrerie et peinture', 'De la préparation à la dernière couche', '',
            ('Un projet de rénovation ?', 'Nous venons voir les supports et vous proposons la préparation et la finition adaptées.', 'Demander un devis'))
        + '''    <section class="section section--tight" aria-labelledby="prepa-titre">
      <div class="container prepa">
        <h2 id="prepa-titre">La préparation fait le résultat</h2>
        <ol class="prepa__etapes"><li>Analyse des supports</li><li>Choix des techniques adaptées</li><li>Préparation minutieuse</li><li>Exécution dans les règles de l'art</li></ol>
        <p class="prepa__but">Notre objectif : des surfaces <b>régulières</b>, des finitions <b>homogènes</b> et un résultat <b>durable</b>.</p>
      </div>
    </section>
'''
        + bande('espaces-titre', 'Création d\'espaces', 'Redessinez vos espaces en plaques de plâtre', [
            'Un bureau supplémentaire, une salle de réunion, une chambre ou un rangement : grâce aux cloisons en plaques de plâtre, nous créons de nouveaux espaces <b>rapidement, proprement</b> et avec la finition de votre choix. Elles peuvent aussi être phoniques, thermiques ou coupe-feu.',
            'Besoin de plus de lumière ou de modularité ? Découvrez aussi nos cloisons mobiles, parois vitrées, cloisons aluminium et panneaux sandwich isothermes.'],
            sch.plan_espaces(), action='<a class="btn btn--light" href="cloisons.html">Voir nos solutions de cloisons</a>'),
        normes=['platrerie-peinture'],
        cas=lambda p: cas_projet('projet-combles-platrerie', 'Référence en plâtrerie',
                                 'Rampants et doublages en plaques de plâtre, <b>angles nets</b>, jusqu\'à la peinture.',
                                 lien_filtre('platrerie-peinture', 'Toutes les réalisations en plâtrerie', 'Toutes les réalisations'),
                                 lies=['projet-cage-escalier-niches', 'projet-hall-gorge-lumineuse']),
        faq_titre='Questions fréquentes sur la plâtrerie et la peinture',
        faq=[('Pourquoi la préparation est-elle si importante ?', 'Une peinture révèle chaque défaut du support. Enduits et ponçage donnent une surface plane : le rendu reste net, même en lumière rasante.', None),
             ('Quelle finition choisir : mat, satiné ou brillant ?', 'Le mat cache les défauts, le satiné se lave facilement, le brillant résiste le mieux. Nous vous conseillons selon la pièce.', None),
             prix_q('Combien coûtent des travaux de peinture ?', 'Le prix dépend de la surface des murs et des plafonds, de leur état, de la hauteur et des finitions choisies.'),
             ('Peignez-vous aussi les façades ?', 'Non. Nous travaillons à l\'intérieur : murs, plafonds, portes, boiseries et parties communes.', None)],
        h2_demande='Demander un devis pour de la plâtrerie ou de la peinture',
        ld_desc='Plâtrerie, enduits et lissages, peinture intérieure, finitions et conseil couleur, à Genève et en Suisse romande.',
        service_type='Plâtrerie et peinture intérieure',
    )


def acoustique():
    s = 'isolation-acoustique'
    reelle = pf.photo_ok('panneaux-acoustiques-muraux-01')
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
    duo = '''    <section class="section section--tight duo-mots" aria-labelledby="isoler-titre">
      <div class="container">
        <h2 id="isoler-titre" class="visually-hidden">Isoler ou corriger : deux problèmes différents</h2>
        <div class="duo-mots__grid">
          <div><p class="duo-mots__mot">Corriger</p><p>Réduire <b>l'écho dans la pièce</b> : salle de réunion, restaurant, réfectoire, salle communale.</p></div>
          <div><p class="duo-mots__mot">Isoler</p><p>Empêcher le bruit de <b>passer d'un local à l'autre</b> : étage, bureau voisin, pièce d'à côté.</p></div>
        </div>
        <p class="duo-mots__pied">À la visite, nous commençons par identifier ce que vous entendez.</p>
      </div>
    </section>
'''
    return dict(
        service=s, crumb='Acoustique', title='Isolation acoustique et phonique à Genève | Andy Construct',
        desc='Notre spécialité : correction acoustique et isolation phonique. Îlots et baffles acoustiques, tissu tendu, cadres, plafonds et cloisons phoniques. Suisse romande.',
        h1='Isolation acoustique et phonique',
        chapeau='Notre spécialité : <b>moins d\'écho</b> dans vos salles, <b>moins de bruit</b> entre vos espaces.',
        btn='Demander un devis pour une isolation acoustique',
        hero=('photo', 'salle-de-reunion-cadres-acoustiques-01'),
        apres_refs=atouts(BENEFICES, 'ac-atouts', 'Ce que nous traitons') + duo,
        blocs=lambda p: types(p, [
            ('ilots', 'Îlots acoustiques', 'Suspendus au plafond ou fixés au mur, ils absorbent le son là où il rebondit, sans toucher au plafond existant.',
             'panneaux-acoustiques-sous-charpente-01', sch.tissu_tendu(), False),
            ('tissu-tendu', 'Tissu tendu acoustique', 'Une toile lisse et sur mesure qui absorbe le son tout en restant élégante : bureaux, restaurants, salles de réunion.',
             'salon-ovales-tissu-tendu-01', sch.tissu_tendu(), True),
            ('correction', 'Cadres et baffles acoustiques', 'Des panneaux muraux, imprimés ou unis, et des baffles verticaux qui réduisent la réverbération des grandes salles.',
             'baffles-acoustiques-eclairage-indirect-01', sch.metallique(), False),
            ('plafonds-cloisons', 'Plafonds et cloisons phoniques', 'Faux plafonds sur suspentes antivibratiles, cloisons à ossatures séparées et plaques doublées : le bruit ne passe plus.',
             'restaurant-traitement-acoustique-01', sch.cloison_platre(), False),
            ('doublages', 'Doublages acoustiques', 'Ossature indépendante, laine minérale et plaques : contre les voix et les bruits du local voisin.',
             None, sch.doublage(), False)],
            'ac-types', 'Nos solutions acoustiques', 'Corriger l\'écho, isoler du bruit', '',
            ('Un problème de bruit ?', 'Nous venons écouter votre espace et vous proposons la solution la plus efficace pour votre usage et votre budget.', 'Demander conseil')),
        specifique=specifique,
        normes=['isolation-acoustique'],
        cas=lambda p: cas_projet('projet-restaurant-acoustique', 'Référence en acoustique',
                                 'Un plafond voûté <b>traité en acoustique</b> : la salle pleine reste calme.',
                                 lien_filtre('isolation-acoustique', 'Toutes les réalisations en acoustique', 'Toutes les réalisations'),
                                 lies=['projet-ilots-tissu-tendu', 'projet-correction-acoustique', 'projet-salle-de-reunion']),
        faq_titre='Questions fréquentes sur l\'acoustique',
        faq=[('Quelle différence entre correction acoustique et isolation phonique ?', 'La correction réduit l\'écho dans une pièce. L\'isolation empêche le bruit de passer d\'un local à l\'autre. Les deux se traitent différemment.', None),
             ('Les panneaux en mousse isolent-ils du bruit ?', 'Non. Ils réduisent un peu l\'écho, sans empêcher le bruit de passer.', None),
             prix_q('Combien coûte une isolation phonique ?', 'Le prix dépend de la surface, du type de travaux et des points faibles à traiter.'),
             ('Peut-on promettre un résultat en décibels ?', 'Pas sans mesure. Les exigences (SIA 181) sont fixées par le projet ; nous choisissons les systèmes en conséquence.', None)],
        h2_demande='Demander un devis pour une isolation acoustique',
        ld_desc='Correction acoustique et isolation phonique : îlots et baffles acoustiques, tissu tendu, cadres, plafonds et cloisons phoniques, doublages, à Genève et en Suisse romande.',
        service_type='Isolation acoustique et phonique',
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
        devis_btn(p, 'entete_page', texte='Demander un devis'), TEL_URI, TEL)
    corps = hero_page(d['crumb'], d['h1'], d['chapeau'], actions=actions, media=hero_html, extra=precision,
                      badges=c.badges(['|B11|B4', '|B6|B3', 'B1'], cls='badges--3'))
    corps += c.bande_refs(service=s)
    corps += d.get('apres_refs', '')
    corps += d['blocs'](p)
    corps += d.get('specifique', '')
    corps += normes_table(seulement=d['normes'], titre_id='normes-titre', h2='Normes et prescriptions', cls='normes--page section--mist')
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
    for f in (acoustique, faux_plafonds, cloisons, platrerie_peinture):
        rendre(f())
