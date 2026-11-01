# -*- coding: utf-8 -*-
"""Composants partagés (architecture §3) : références, méthode, FAQ, formulaire en 3 étapes, rappel,
bloc de demande, bande d'appel, cartes projets, avant / après, témoignages."""
import json, os, re, struct
import ctx
from ctx import e, T, V, definitif, marque, insec, M
from common import (TEL, TEL_URI, MOB, MOB_URI, tel_link, horaires, mob_label, mail, svc_nom, svc_url, SERVICES,
                    devis_btn, ICON_PHONE, ZEFIX, GGE, AUJOURDHUI, libelle_devis)
from icons import ICONS, INFO

# ---------------------------------------------------------------- références et logos (v3 : logos officiels en couleur)
# Ordre de préférence d'un fichier : fichier_couleur (assets/img/references/couleur/) → fichier (version sombre) ; aucun
# fichier, ou logo non autorisé dans ce mode → nom en « wordmark » typographique homogène (Archivo élargie).
LOGOS_DIR = os.path.join(ctx.SITE, 'assets/img/references')
LOGOS = {l['id']: l for l in json.load(open(os.path.join(LOGOS_DIR, 'logos.json'), encoding='utf-8'))}
TEXTE_SEUL = set()   # v3 : décision du client, de vrais logos partout (de Grisogono compris, statut a_autoriser)


def _chemin_logo(nom):
    """Chemin relatif à assets/img/references/ d'un fichier déclaré (« ubs.svg » ou « couleur/ubs.svg »), ou None."""
    if not nom:
        return None
    for rel in (nom, 'couleur/' + os.path.basename(nom)):
        if os.path.exists(os.path.join(LOGOS_DIR, rel)):
            return rel
    return None


def _dims(fichier):
    chemin = os.path.join(LOGOS_DIR, fichier)
    if fichier.endswith('.png'):
        with open(chemin, 'rb') as f:
            w, h = struct.unpack('>II', f.read(24)[16:24])
        return w, h
    if fichier.endswith('.webp'):
        b = open(chemin, 'rb').read(30)
        if b[12:16] == b'VP8X':
            return 1 + int.from_bytes(b[24:27], 'little'), 1 + int.from_bytes(b[27:30], 'little')
        return 400, 200
    svg = open(chemin, encoding='utf-8').read(4000)
    vb = re.search(r'viewBox="\s*([\d.eE+-]+)[\s,]+([\d.eE+-]+)[\s,]+([\d.eE+-]+)[\s,]+([\d.eE+-]+)', svg)
    if vb:
        w, h = float(vb.group(3)), float(vb.group(4))
    else:
        w = float(re.search(r'\swidth="([\d.]+)', svg).group(1))
        h = float(re.search(r'\sheight="([\d.]+)', svg).group(1))
    return round(w * 100 / h), 100


def echelle_cls(v):
    return 'e%03d' % round(v * 100)


def echelles():
    """Classes CSS des échelles optiques (pas d'attribut style : CSP stricte)."""
    vals = sorted({l.get('echelle', 1) or 1 for l in LOGOS.values()})
    return ''.join('.%s{--e:%s}' % (echelle_cls(v), ('%g' % v)) for v in vals)


def fichier_logo(rid, fond='clair'):
    """Fichier à afficher : en couleur d'abord (sur fond clair ou sur pastille blanche), sinon la version sombre.
    fond='sombre' (sans pastille) : version blanche. None si aucun fichier n'existe."""
    l = LOGOS[rid]
    if fond == 'sombre':
        return _chemin_logo(l.get('fichier_blanc'))
    return _chemin_logo(l.get('fichier_couleur')) or _chemin_logo(l.get('fichier'))


def logo_affiche(rid):
    l = LOGOS[rid]
    if rid in TEXTE_SEUL or not fichier_logo(rid):
        return False
    if l['statut'] == 'autorise':
        return True
    return l['statut'] == 'a_autoriser' and not ctx.prod()


# Noms en wordmark (cro-v3 §2.3) : générique en maigre au-dessus, nom propre en demi-gras ; noms longs coupés dans les données
# (deux lignes au plus). Champs facultatifs de logos.json qui priment : « generique », « nom_lignes ».
WORDMARKS = {
    'ville-de-geneve': ('Ville de', ['Genève']),
    'collonge-bellerive': ('Salle communale de', ['Collonge-Bellerive']),
    'plan-les-ouates': ('Salle communale de', ['Plan-les-Ouates']),
    'alhambra': ('Salle de', ['l\'Alhambra']),
    'conservatoire-musique-geneve': (None, ['Conservatoire de', 'musique de Genève']),
    'harmonie-nautique': (None, ['Harmonie Nautique', 'de Genève']),
    'everness': (None, ['Everness', 'Hotel & Resort']),
    'domaine-des-perrieres': ('Domaine des', ['Perrières']),
    'labcorp': (None, ['Labcorp']),
}


def nom_ref(rid):
    """Nom affiché, avec les replis d'exactitude (cro-v3 §2.2 H2) : Plan-les-Ouates « salle communale » à valider (C22),
    Everness nommé seulement si C22 confirme qu'il s'agit bien de l'hôtel de Chavannes-de-Bogis."""
    if rid == 'plan-les-ouates':
        return V('C22', 'Salle communale de Plan-les-Ouates', LOGOS[rid]['nom_affiche'])
    if rid == 'everness' and not definitif('C22'):
        return 'Hôtel à Chavannes-de-Bogis'
    return LOGOS[rid]['nom_affiche']


def wordmark(rid, nom=None):
    l = LOGOS[rid]
    if nom is None and rid == 'everness' and not definitif('C22'):
        gen, lignes = 'Hôtel à', ['Chavannes-de-Bogis']
    elif nom is None and rid == 'plan-les-ouates' and not definitif('C22'):
        gen, lignes = 'Mairie de', ['Plan-les-Ouates']
    elif nom is None and (l.get('nom_lignes') or rid in WORDMARKS):
        gen, lignes = (l.get('generique'), l['nom_lignes']) if l.get('nom_lignes') else WORDMARKS[rid]
    else:
        gen, lignes = None, [nom or l['nom_affiche']]
    g = ('<span class="wordmark__gen">%s</span>' % e(gen)) if gen else ''
    return '<span class="wordmark">%s%s</span>' % (g, '<span class="wordmark__nom">%s</span>' % '<br>'.join(insec(e(x)) for x in lignes))


def logo_img(rid, nom=None, alt=None, lazy=True, fond='clair'):
    """<img> du logo (classe d'échelle optique), ou wordmark si le logo n'est pas affichable dans ce mode."""
    l = LOGOS[rid]
    f = fichier_logo(rid, fond) if logo_affiche(rid) else None
    if f:
        w, h = _dims(f)
        # Logos très allongés (≥ 4,5 : 1) ou très aérés (Ville de Genève) : toute la largeur utile de la cellule
        large = ' logo--large' if (w / h >= 4.5 or rid == 'ville-de-geneve') else ''
        return ('<img class="logo %s%s" src="assets/img/references/%s" width="%d" height="%d" alt="%s"%s decoding="async">'
                % (echelle_cls(l.get('echelle', 1) or 1), large, f, w, h, e((nom or nom_ref(rid)) if alt is None else alt), ' loading="lazy"' if lazy else ''))
    return wordmark(rid, nom)


def _sub(rid):
    """OMC : remplacée par l'Alhambra tant que l'accord pour le nom n'est pas confirmé (décision D4)."""
    return 'alhambra' if rid == 'omc' and not definitif('C22') else rid


# Mur de logos de l'accueil (12, du plus fort au moins connu) et bande défilante (toutes les références)
# Ordre canonique (cro-v3 §2.2 H2 et H9) : public en tête, communes au début de la 2e rangée, puis public et privé alternés.
# En preview, l'OMC occupe la 4e cellule (D4) ; en production sans accord écrit, c'est la Salle de l'Alhambra.
MUR = ['ville-de-geneve', 'conservatoire-musique-geneve', 'head-geneve', 'omc', 'ubs', 'piaget',
       'plan-les-ouates', 'collonge-bellerive', 'j-safra-sarasin', 'labcorp', 'everness', 'celgene']
DEFILE = MUR[:4] + ['alhambra'] + MUR[4:] + ['energestion', 'dipan', 'harmonie-nautique', 'domaine-des-perrieres', 'de-grisogono']


def nb_refs():
    """Nombre de noms publiables dans ce mode (17 en production tant que l'accord écrit de l'OMC manque)."""
    return len(LOGOS) - (0 if definitif('C22') else 1)


def _ids(ids):
    vus, out = set(), []
    for rid in ids:
        r = _sub(rid)
        if r not in vus:
            vus.add(r)
            out.append(r)
    return out


def mur_logos(titre_id='refs-titre', h2='Ils nous ont confié des travaux'):
    """Mur de références juste sous le héro (cro-v3 §2.2 H2) : cellules blanches identiques séparées par des filets ;
    6 × 2 (ordinateur), 3 × 4 (tablette), 2 × 4 (mobile) ; logos en couleur ou wordmarks selon le mode."""
    part = T('C04', 'Et des <b>particuliers</b>, pour une cloison, un plafond ou une pièce à repeindre.',
             'Et des <b>particuliers</b>, à Genève et dans toute la région.')
    # Sur mobile, la première cellule (Ville de Genève) occupe toute la rangée : son texte reste lisible (chef de projet)
    cells = ''.join('<li class="logo-cell%s">%s</li>' % (' logo-cell--une' if i == 0 else '', logo_img(rid)) for i, rid in enumerate(_ids(MUR)))
    accords = ('<p class="logos__accord">Références citées avec l\'accord des maîtres d\'ouvrage.</p>'
               if ctx.prod() and ctx.confirme('C22') else '')
    return '''    <section class="logos" aria-labelledby="%s" data-suivi-zone="references">
      <div class="container">
        <h2 id="%s" class="logos__titre">%s</h2>
        %s
        <div class="logos__foot"><p>%s</p><a class="link-arrow" href="professionnels.html#references">Voir les %d références</a></div>%s
      </div>
    </section>
''' % (titre_id, titre_id, h2, marque('C22', '<ul class="logo-wall" data-reveal="cells">%s</ul>' % cells, bloc=True), part, nb_refs(), accords)


def bande_logos(titre='Ils nous ont confié des travaux', titre_id='defile-titre', cls=''):
    """Bande défilante (rappel avant un appel à l'action) : logos en couleur, pause au survol, au focus et au bouton.
    Sans JavaScript ou en mouvement réduit : une rangée statique. La copie qui assure la boucle est créée par main.js."""
    items = ''.join('<li class="mq__item">%s</li>' % logo_img(rid) for rid in _ids(DEFILE))
    return '''    <div class="defile%s" role="group" aria-labelledby="%s">
      <div class="container defile__head">
        <h2 id="%s" class="defile__titre">%s</h2>
        <button type="button" class="defile__pause js-only" aria-pressed="false" data-mq-pause>Mettre en pause</button>
      </div>
      <div class="mq" data-mq><ul class="mq__track">%s</ul></div>
    </div>
''' % ((' ' + cls) if cls else '', titre_id, titre_id, titre, items)


def refs_ligne(cls=''):
    """Rappel compact près des formulaires : 6 logos en couleur, puis « et des particuliers »."""
    items = ''.join('<li>%s</li>' % logo_img(rid) for rid in _ids(['ville-de-geneve', 'conservatoire-musique-geneve', 'head-geneve', 'ubs', 'piaget', 'plan-les-ouates']))
    return ('<div class="refs-line%s"><p><b>Ils nous ont confié des travaux</b></p><ul class="refs-line__logos">%s</ul>'
            '<p class="refs-line__part">et des particuliers de toute la région.</p></div>' % ((' ' + cls) if cls else '', items))


def refs_pied():
    """Pied de page sombre : logos en couleur sur pastilles blanches."""
    items = ''.join('<li class="pill">%s</li>' % logo_img(rid) for rid in _ids(MUR[:10]))
    return ('<p class="footer-refs__title">Ils nous ont confié des travaux</p>'
            '<ul class="pills">%s</ul><p class="footer-refs__part">et des particuliers de toute la région. '
            '<a href="professionnels.html#references">Toutes nos références</a></p>' % items)


# Liste canonique moyenne (cro-v3 §2.3, règle 7) : pages services sans C23, contact, entreprise
MOYENNE = ['ville-de-geneve', 'conservatoire-musique-geneve', 'head-geneve', 'alhambra', 'plan-les-ouates', 'collonge-bellerive']
# Références à citer par service (proposées pour C23, cro-v3 §6.1) : présentées comme propres au service seulement si C23
PAR_SERVICE = {'placo': ['ville-de-geneve', 'conservatoire-musique-geneve', 'energestion'],
               'isolation-acoustique': ['conservatoire-musique-geneve', 'head-geneve', 'collonge-bellerive']}


def bande_refs(service=None, titre='Ils nous ont confié des travaux', titre_id='bande-refs-titre', cls=''):
    """Bande de 6 logos en couleur (cellules du mur) sous un en-tête de page. Titre générique et liste canonique moyenne
    (honnête dans tous les modes) ; si C23 confirme les références d'un service, elles passent en tête, avec une ligne
    « En placo, notamment pour… » (marquée en vérification)."""
    ids = list(MOYENNE)
    propre = ''
    if service in PAR_SERVICE and definitif('C23'):
        sp = PAR_SERVICE[service]
        ids = (sp + [x for x in MOYENNE if x not in sp])[:6]
        noms = [nom_ref(x) for x in sp]
        propre = marque('C23', 'En %s, notamment pour %s et %s.' % (
            ctx.fr(svc_nom(service, html=False)).lower(), ', '.join(noms[:-1]), noms[-1]))
    cells = ''.join('<li class="logo-cell">%s</li>' % logo_img(rid) for rid in _ids(ids))
    pied = (propre + ' ' if propre else '') + 'Et des <b>particuliers</b> de toute la région.'
    return '''    <section class="rband%s" aria-labelledby="%s" data-suivi-zone="references">
      <div class="container">
        <div class="rband__head"><h2 id="%s">%s</h2><a class="link-arrow" href="professionnels.html#references">Voir les %d références</a></div>
        <ul class="logo-wall logo-wall--bande" data-reveal="cells">%s</ul>
        <p class="rband__pied">%s</p>
      </div>
    </section>
''' % ((' ' + cls) if cls else '', titre_id, titre_id, titre, nb_refs(), cells, pied)


def mur_complet(par_secteur=False):
    """Mur complet des références (réalisations, professionnels) : toutes en cellules, logos en couleur (wordmarks en
    production tant que l'accord manque). par_secteur : ordre par secteur, secteur écrit sous chaque cellule."""
    if par_secteur:
        ordre = [(rid, titre) for titre, ids in SECTEURS for rid in ids]
        ordre = [(_sub(r), t) for r, t in ordre if not (r == 'omc' and not definitif('C22'))]
        vus, cells = set(), ''
        for rid, t in ordre:
            if rid in vus:
                continue
            vus.add(rid)
            inner = logo_img(rid)
            if rid == 'omc':
                inner = marque('C22', inner)
            cells += '<li class="logo-cell logo-cell--leg">%s<span class="logo-cell__sec">%s</span></li>' % (inner, SECTEUR_COURT[t])
        n = len(vus)
    else:
        ids = _ids(DEFILE)
        cells = ''.join('<li class="logo-cell">%s</li>' % logo_img(rid) for rid in ids)
        n = len(ids)
    if n % 6:
        cells += ('<li class="logo-cell logo-cell--part"><span>Et des <b>particuliers</b>, à Genève et dans toute la région</span></li>')
    return '<ul class="logo-wall logo-wall--complet" data-reveal="cells">%s</ul>' % cells


SECTEURS = [
    ('Collectivités et institutions', ['ville-de-geneve', 'plan-les-ouates', 'collonge-bellerive', 'omc']),
    ('Culture et formation', ['conservatoire-musique-geneve', 'head-geneve', 'alhambra', 'harmonie-nautique']),
    ('Entreprises', ['piaget', 'ubs', 'j-safra-sarasin', 'de-grisogono', 'celgene', 'labcorp', 'dipan', 'energestion']),
    ('Hôtellerie et domaines', ['everness', 'domaine-des-perrieres']),
]
SECTEUR_COURT = {'Collectivités et institutions': 'Collectivité', 'Culture et formation': 'Culture et formation',
                 'Entreprises': 'Entreprise', 'Hôtellerie et domaines': 'Hôtellerie'}
# ---------------------------------------------------------------- badges de confiance (cro-v3 §4) : rendus selon confirmations.json
def ans_activite():
    """Années révolues depuis l'inscription au registre du commerce (1.6.2007)."""
    return AUJOURDHUI.year - 2007 - (1 if (AUJOURDHUI.month, AUJOURDHUI.day) < (6, 1) else 0)


I_BADGE = {
    'registre': '<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5"/><path class="accent" d="M9 14l2.5 2.5L16 12"/>',
    'calendrier': '<path d="M4 6h16v14H4z"/><path d="M4 10h16M8 3v5M16 3v5"/><path class="accent" d="M8 15h3"/>',
    'lieu': '<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z"/><circle class="accent" cx="12" cy="10" r="2.2"/>',
    'offre': '<path d="M6 3h12v18H6z"/><path d="M9 8h6M9 12h6"/><path class="accent" d="M9 16h4"/>',
    'facade': '<path d="M3 21h18M4 9h16M12 3l9 6H3z"/><path d="M6 9v9M10 9v9M14 9v9M18 9v9"/><path class="accent" d="M3 21h18"/>',
    'visite': '<path d="M7 4h10v17H7z"/><path d="M10 3h4v3h-4z"/><path class="accent" d="M9.5 13l2 2 3.5-4"/>',
    'groupe': '<path d="M12 3l7 3v5c0 4.5-3 8.2-7 10-4-1.8-7-5.5-7-10V6z"/><path class="accent" d="M9 11h6"/>',
    'assurance': '<path d="M12 3l7 3v5c0 4.5-3 8.2-7 10-4-1.8-7-5.5-7-10V6z"/><path class="accent" d="M9 12l2 2 4-4"/>',
    'rappel': '<path d="M6.5 3h3l1.5 4.5-2 1.5a11 11 0 0 0 6 6l1.5-2 4.5 1.5v3a2 2 0 0 1-2 2A17 17 0 0 1 4.5 5a2 2 0 0 1 2-2z"/><path class="accent" d="M15 3.5a5.5 5.5 0 0 1 5.5 5.5"/>',
    'personne': '<circle cx="12" cy="8" r="3.6"/><path d="M5 20.5c.8-3.9 3.6-6.2 7-6.2s6.2 2.3 7 6.2"/><path class="accent" d="M9 20.5h6"/>',
    'etoile': '<path class="accent" d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
}


def _badge(icone, titre, sous, href=None, ext=False, codes=None):
    t = ('<a href="%s"%s>%s</a>' % (href, ' rel="noopener"' if ext else '', titre)) if href else titre
    txt = '<span><b>%s</b> %s</span>' % (t, sous)
    return ('<li><svg class="badge__i" viewBox="0 0 24 24" aria-hidden="true" focusable="false">%s</svg>%s</li>'
            % (I_BADGE[icone], marque(codes, txt) if codes else txt))


def badge(cle):
    """Un badge (li) ou '' s'il n'est pas publiable dans ce mode."""
    a = ctx.AVIS or {}
    if cle == 'B1':
        return _badge('registre', 'Registre du commerce', 'Inscrite, vérifiable sur Zefix', ZEFIX, ext=True)
    if cle == 'B2':
        return _badge('calendrier', 'Depuis 2007', '%d ans d\'activité' % ans_activite())
    if cle == 'B3':
        return _badge('lieu', 'Siège à Carouge', 'Toute la Suisse romande', 'contact.html#zone')
    if cle == 'B4':
        return _badge('offre', 'Offre écrite', 'Après visite sur place')
    if cle == 'B5':
        return _badge('facade', '%d références' % nb_refs(), 'Dont la Ville de Genève', 'professionnels.html#references')
    if cle == 'B6':
        return _badge('visite', 'Visite et devis gratuits', 'Sans engagement', codes='C02') if definitif('C02') else ''
    if cle == 'B7':
        return _badge('groupe', 'Membre du GGE', 'Entreprises genevoises du bâtiment', GGE, ext=True, codes='C11') if definitif('C11') else ''
    if cle == 'B8':
        return _badge('assurance', 'Assurance responsabilité civile', 'Attestation sur demande', codes='C12') if definitif('C12') else ''
    if cle == 'B9':
        return _badge('rappel', 'Rappel le jour même', 'Ou le jour ouvrable suivant', codes='C01') if definitif('C01') else ''
    if cle == 'B11':
        return _badge('personne', 'Un seul interlocuteur', 'De la pose à la peinture', codes='C05') if definitif('C05') else ''
    if cle == 'B10':
        return _badge('offre', 'Attestations à jour', 'AVS, LPP, impôts, sur demande', codes='C13') if definitif('C13') else ''
    if cle == 'B13':
        if (a.get('nombre') or 0) >= 5 and a.get('note'):
            return _badge('etoile', '%s sur 5' % str(a['note']).replace('.', ','), '%d avis Google' % a['nombre'], a.get('url') or None, ext=True)
        return ''
    raise KeyError(cle)


def premier(*cles):
    for k in cles:
        b = badge(k)
        if b:
            return b
    return ''


def badges(cles, cls='', label='En bref'):
    items = ''.join(badge(k) if not k.startswith('|') else premier(*k[1:].split('|')) for k in cles)
    return '<ul class="badges%s" aria-label="%s">%s</ul>' % ((' ' + cls) if cls else '', label, items) if items else ''



# ---------------------------------------------------------------- chiffres clés (accueil, professionnels, entreprise)
def chiffres(titre_id='chiffres-titre'):
    """Bande anthracite (cro-v3 §2.2 H5) : valeurs finales dans le HTML (lues sans JavaScript, jamais « 0 »),
    comptées une fois à l'apparition."""
    items = [(ans_activite(), 'ans d\'activité'), (nb_refs(), 'références, publiques et privées'), (4, 'métiers intérieurs')]
    items.append((1, marque('C01', 'jour ouvrable, au plus, pour vous rappeler')) if definitif('C01') else (7, 'cantons et régions romands'))
    lis = ''.join('<li><span class="chiffre" aria-hidden="true" data-count="%d">%d</span><span class="chiffre__lbl">'
                  '<span class="visually-hidden">%d </span>%s</span></li>' % (n, n, n, l) for n, l in items)
    return '''    <section class="section section--dark on-dark chiffres" aria-labelledby="%s">
      <div class="container">
        <h2 id="%s" class="visually-hidden">Andy Construct en chiffres</h2>
        <ul class="chiffres__list" data-reveal="cells">%s</ul>
      </div>
    </section>
''' % (titre_id, titre_id, lis)


# ---------------------------------------------------------------- images des pages v3 : vraies photos, illustrations signalées
def media(kind, ident, sizes, fmt='16x9', eager=False, alt=None):
    """Image d'un bloc. kind : « photo » (vraie photo, recadrage fmt), « ill » (illustration sous licence, mention
    « Illustration » toujours visible), « aa » (ident = (paire, état), photo avant / après réelle)."""
    if kind == 'photo':
        import portfolio as pf
        return pic_crop(ident, fmt, sizes, alt or pf.alt(ident), eager=eager)
    if kind == 'aa':
        import portfolio as pf
        paire, etat = ident
        return aa_pic(paire, etat, sizes, alt or pf.PAIRE[paire][5 if etat == 'apres' else 4])
    import illustrations
    it = illustrations.trouver(ident=ident)
    return illustrations.picture(it, sizes, lazy=not eager) if it else ''


def _srcset_crop(pid, fmt):
    r = RECADRAGES.get(pid, {}).get(fmt)
    if not r:
        return None
    return ', '.join('%s-%d.webp %dw' % (r['base'], x, x) for x in r['largeurs'] if x <= 1600), r['base']


def hero_image(kind, ident, alt=None):
    """Image de l'en-tête de page (grande, à droite sur ordinateur ; sous les boutons sur mobile) et son préchargement.
    Vraie photo : recadrage 4:5 sur ordinateur, 16:9 sur mobile. Illustration : un seul fichier, mention « Illustration »."""
    sz_b, sz_m = '(min-width: 1440px) 600px, 42vw', '100vw'
    if kind == 'photo':
        import portfolio as pf
        b45, b169 = _srcset_crop(ident, '4x5') or _srcset_crop(ident, '16x9'), _srcset_crop(ident, '16x9')
        html = ('<picture><source media="(min-width: 900px)" type="image/webp" srcset="%s" sizes="%s">'
                '<source type="image/webp" srcset="%s" sizes="%s"><img src="%s-800.jpg" width="1600" height="900" alt="%s" fetchpriority="high"></picture>'
                % (b45[0], sz_b, b169[0], sz_m, b169[1], e(alt or pf.alt(ident))))
        pre = ('  <link rel="preload" as="image" type="image/webp" fetchpriority="high" imagesrcset="%s" imagesizes="%s" media="(min-width: 900px)">\n'
               '  <link rel="preload" as="image" type="image/webp" fetchpriority="high" imagesrcset="%s" imagesizes="%s" media="(max-width: 899.98px)">\n'
               % (b45[0], sz_b, b169[0], sz_m))
        return html, pre
    if kind == 'aa':
        import portfolio as pf
        paire, etat = ident
        m = AA[paire][etat]
        srcset = ', '.join('%s-%d.webp %dw' % (m['base'], w, w) for w in m['largeurs'])
        html = ('<picture><source type="image/webp" srcset="%s" sizes="(min-width: 900px) 42vw, 100vw"><img src="%s-%d.jpg" width="%d" height="%d" alt="%s" fetchpriority="high"></picture>'
                % (srcset, m['base'], m['largeurs'][-1], m['largeur'], m['hauteur'], e(alt or pf.PAIRE[paire][5 if etat == 'apres' else 4])))
        pre = '  <link rel="preload" as="image" type="image/webp" fetchpriority="high" imagesrcset="%s" imagesizes="(min-width: 900px) 42vw, 100vw">\n' % srcset
        return html, pre
    import illustrations
    it = illustrations.trouver(ident=ident)
    srcset, src, w, h = illustrations._src(it)
    html = ('<picture><source type="image/webp" srcset="%s" sizes="(min-width: 1440px) 600px, (min-width: 900px) 42vw, 100vw">'
            '<img src="%s" width="%d" height="%d" alt="%s" fetchpriority="high"></picture><span class="ill__tag">Illustration</span>'
            % (srcset, src, w, h, e(it.get('alt') or '')))
    pre = ('  <link rel="preload" as="image" type="image/webp" fetchpriority="high" imagesrcset="%s" imagesizes="(min-width: 1440px) 600px, (min-width: 900px) 42vw, 100vw">\n' % srcset)
    return html, pre


# ---------------------------------------------------------------- blocs v3 : damier texte / image, rangée texte + grande image
def damier(items, cls=''):
    """Damier (pages services) : chaque élément = image + texte court ; sur ordinateur, deux par rangée, l'image passe
    à droite une rangée sur deux. items : (ancre ou None, titre, texte HTML, image HTML). Un texte vide masque l'élément
    (repli de production) ; son ancre reste dans la page (cible des redirections 301)."""
    lis, ancres = '', ''
    for ancre, titre, texte, img in items:
        if not texte:
            if ancre:
                ancres += '<span id="%s"></span>' % ancre
            continue
        lis += ('<li class="damier__item"%s><div class="damier__media">%s</div><div class="damier__txt"><h3>%s</h3><p>%s</p></div></li>'
                % ((' id="%s"' % ancre) if ancre else '', img, titre, texte))
    return '%s<ul class="damier%s" data-trait>%s</ul>' % (ancres, (' ' + cls) if cls else '', lis)


def feat(titre_id, h2, contenu, img, inverse=False, cls='', legende=''):
    """Rangée texte + grande image (alternance) ; le trait de niveau part du titre et entre dans l'image."""
    fig = '<figure class="feat__media">%s%s</figure>' % (img, ('<figcaption>%s</figcaption>' % legende) if legende else '')
    return '''    <section class="section feat%s%s" aria-labelledby="%s" data-trait>
      <div class="container feat__grid">
        <div class="feat__txt">
          <h2 id="%s">%s</h2>
          <span class="laser laser--feat" aria-hidden="true"></span>
          %s
        </div>
        %s
      </div>
    </section>
''' % (' feat--inverse' if inverse else '', (' ' + cls) if cls else '', titre_id, titre_id, h2, contenu, fig)


def points(items):
    """Liste courte (3 points au plus), mots clés en gras."""
    return '<ul class="ticks ticks--filets">%s</ul>' % ''.join('<li>%s</li>' % x for x in items if x)


# ---------------------------------------------------------------- méthode en 4 étapes (texte unique)
def methode(complete=True, titre_id='methode-titre', h2=None, lien=True, surtitre=True):
    """Méthode complète en 4 étapes (entreprise.html#methode) ; les pages services ont leur version courte."""
    etapes = [
        ('Visite', 'Nous venons voir les lieux, prenons les mesures et écoutons votre besoin.'),
        ('Offre écrite', T('C06', 'Détaillée poste par poste, en CHF, avec la durée des travaux et ce qui n\'est pas compris.',
                           'Nous vous remettons une offre écrite.')),
        ('Chantier protégé', T('C07', 'Sols, meubles et passages protégés. Nettoyage chaque soir, et à fond le dernier jour.',
                               'Les lieux sont protégés pendant les travaux.')),
        ('Réception', T('C32', 'Nous faisons le tour des finitions avec vous. Une retouche ? Nous revenons.',
                        'Nous contrôlons les finitions avec vous.')),
    ]
    lis = ''.join('<li><h3>%s</h3><p>%s</p></li>' % (t, d) for t, d in etapes)
    eng = T('C06', 'Aucun travail supplémentaire sans votre accord écrit et chiffré.', '')
    eng = ('<p class="engagement">%s</p>' % eng) if eng else ''
    return '<ol class="steps">%s</ol>%s' % (lis, eng)


# ---------------------------------------------------------------- FAQ
def faq_items(questions):
    """questions : liste de (question, réponse_html, réponse_texte). Renvoie (html, entités JSON-LD)."""
    html = ''.join('<details><summary>%s</summary><div><p>%s</p></div></details>' % (q, a) for q, a, _ in questions)
    ld = [{'@type': 'Question', 'name': ctx.fr(q.strip()), 'acceptedAnswer': {'@type': 'Answer', 'text': ctx.fr(t.strip())}} for q, _, t in questions]
    return html, ld


def faq_ld(url, ld):
    return {'@context': 'https://schema.org', '@type': 'FAQPage', '@id': url + '#faq', 'inLanguage': 'fr-CH', 'mainEntity': ld}


def Q(codes, question, definitive, repli=None):
    """Question de FAQ soumise à confirmation. repli None : question masquée en production."""
    if codes is None:
        return (question, definitive, re.sub(r'<[^>]+>', '', definitive))
    if definitif(codes):
        return (question, marque(codes, definitive), re.sub(r'<[^>]+>', '', definitive))
    if repli is None:
        return None
    return (question, repli, re.sub(r'<[^>]+>', '', repli))


# ---------------------------------------------------------------- photos (manifeste du portfolio)
MANIFEST = {m['id']: m for m in json.load(open(os.path.join(ctx.SITE, 'assets/img/portfolio/manifest.json'), encoding='utf-8'))}
AA = {m['id']: m for m in json.load(open(os.path.join(ctx.SITE, 'assets/img/avant-apres/manifest.json'), encoding='utf-8'))}


def pic(pid, sizes, alt, eager=False, cls=''):
    it = MANIFEST[pid]
    if it.get('recadre'):
        r = it['recadre']
        b, w, h = r['base'], r['largeur_1200'], r['hauteur_1200']
        srcset = '%s-400.webp 400w, %s-800.webp 800w, %s-1200.webp 1200w' % (b, b, b)
    else:
        b, w, h = it['base'], it['largeur_1600'], it['hauteur_1600']
        srcset = '%s-400.webp %dw, %s-800.webp %dw, %s-1600.webp %dw' % (b, it['largeur_400'], b, it['largeur_800'], b, it['largeur_1600'])
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return ('<picture%s><source type="image/webp" srcset="%s" sizes="%s"><img src="%s-800.jpg" width="%d" height="%d" alt="%s" %s decoding="async"></picture>'
            % ((' class="%s"' % cls) if cls else '', srcset, sizes, b, w, h, e(alt), load))


_REC = os.path.join(ctx.SITE, 'assets/img/portfolio/recadrages.json')
RECADRAGES = {r['id']: r.get('recadrages', {}) for r in (json.load(open(_REC, encoding='utf-8')) if os.path.exists(_REC) else [])}


def pic_crop(pid, fmt, sizes, alt, eager=False, cls=''):
    """Recadrage éditorial d'une vraie photo (« 16x9 » ou « 4x5 », credits-images.md §3) ; repli : photo d'origine."""
    r = RECADRAGES.get(pid, {}).get(fmt)
    if not r:
        return pic(pid, sizes, alt, eager=eager, cls=cls)
    b = r['base']
    larg = [x for x in r['largeurs'] if x <= 1600]
    srcset = ', '.join('%s-%d.webp %dw' % (b, x, x) for x in larg)
    w, h = (1600, round(1600 * r['hauteur'] / r['largeur']))
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return ('<picture%s><source type="image/webp" srcset="%s" sizes="%s"><img src="%s-800.jpg" width="%d" height="%d" alt="%s" %s decoding="async"></picture>'
            % ((' class="%s"' % cls) if cls else '', srcset, sizes, b, w, h, e(alt), load))


def pic_data(pid):
    """Attributs de la visionneuse (grande image) pour une photo."""
    it = MANIFEST[pid]
    if it.get('recadre'):
        r = it['recadre']
        return r['base'] + '-1200.webp', r['base'] + '-800.jpg', r['largeur_1200'], r['hauteur_1200']
    return it['base'] + '-1600.webp', it['base'] + '-800.jpg', it['largeur_1600'], it['hauteur_1600']


def aa_pic(paire, etat, sizes, alt):
    m = AA[paire][etat]
    b = m['base']
    srcset = ', '.join('%s-%d.webp %dw' % (b, w, w) for w in m['largeurs'])
    return ('<picture><source type="image/webp" srcset="%s" sizes="%s"><img src="%s-%d.jpg" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"></picture>'
            % (srcset, sizes, b, m['largeurs'][-1], m['largeur'], m['hauteur'], e(alt)))


# ---------------------------------------------------------------- formulaire de demande en 3 étapes (architecture §6)
TRAVAUX = [('placo', 'Placo', 'Cloisons, doublages, faux-plafonds'),
           ('peinture', 'Peinture', 'Murs et plafonds, à l\'intérieur'),
           ('isolation-acoustique', 'Isolation acoustique', 'Contre le bruit ou l\'écho'),
           ('cloisons-isothermes', None, 'Caves, garages, combles'),
           ('ne-sait-pas', 'Autre chose, ou je ne sais pas encore', 'Décrivez-le à l\'étape 3')]
TYPE_CLIENT = [('proprietaire', 'Propriétaire (maison, appartement, PPE)'), ('locataire', 'Locataire'),
               ('regie', 'Régie, gérance ou coopérative'), ('architecte', 'Architecte, bureau d\'études ou entreprise générale'),
               ('commune', 'Commune ou institution'), ('entreprise', 'Entreprise, bureau ou commerce')]
DELAI = [('moins-1-mois', 'Dès que possible (moins d\'un mois)'), ('1-3-mois', 'Dans 1 à 3 mois'),
         ('3-6-mois', 'Dans 3 à 6 mois'), ('non-defini', 'Pas encore défini')]
SURFACE = [('moins-15', 'Moins de 15 m² (une réparation)'), ('15-50', '15 à 50 m² (une ou deux pièces)'),
           ('50-200', '50 à 200 m² (un appartement, un étage)'), ('plus-200', 'Plus de 200 m², ou plusieurs logements'),
           ('ne-sait-pas', 'Je ne sais pas')]
PREF = [('appel', 'Par téléphone'), ('email', 'Par e-mail'), ('indifferent', 'Peu importe')]
CRENEAU = [('matin', 'Le matin'), ('apres-midi', 'L\'après-midi'), ('indifferent', 'Peu importe')]
CONNU = [('recherche-google', 'Recherche sur Google'), ('carte-google', 'Carte Google'),
         ('recommandation', 'Recommandation d\'un proche ou d\'un voisin'), ('regie-architecte', 'Une régie ou un architecte'),
         ('panneau-vehicule', 'Un panneau de chantier ou un véhicule'), ('facebook', 'Facebook'), ('linkedin', 'LinkedIn'),
         ('autre', 'Autre')]
OBL = ' <span class="req">(obligatoire)</span>'
FAC = ' <span class="opt">(facultatif)</span>'


def cachés(formulaire, source):
    champs = ['page', 'page_entree', 'referent', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term']
    return ('<input type="hidden" name="formulaire" value="%s"><input type="hidden" name="canal" value="site">'
            '<input type="hidden" name="source" value="%s"><input type="hidden" name="form_t0" value="">%s'
            '<div class="hp" aria-hidden="true"><label>Ne pas remplir ce champ <input name="site_web" type="text" tabindex="-1" autocomplete="off"></label></div>'
            % (formulaire, source, ''.join('<input type="hidden" name="%s" value="">' % c for c in champs)))


def erreur(fid):
    return '<p class="error" id="%s-err" hidden></p>' % fid


def radios(fid, name, options, legend, statut, aide='', cls='', required=False, describedby=True):
    aide_html = ('<p class="hint" id="%s-aide">%s</p>' % (fid, aide)) if aide else ''
    desc = ' '.join(x for x in [('%s-aide' % fid) if aide else '', '%s-err' % fid] if x)
    opts = ''.join(
        '<label class="choice" for="%s-%s"><input type="radio" id="%s-%s" name="%s" value="%s"%s><span>%s</span></label>'
        % (fid, v, fid, v, name, v, ' required' if required and i == 0 else '', l)
        for i, (v, l) in enumerate(options))
    return ('<fieldset class="group%s" id="%s" aria-describedby="%s" data-champ="%s"><legend>%s%s</legend>%s<div class="choices">%s</div>%s</fieldset>'
            % ((' ' + cls) if cls else '', fid, desc, name, legend, statut, aide_html, opts, erreur(fid)))


def radios_groupes(fid, name, groupes, legend, statut):
    """Un seul groupe de boutons radio, présenté en sous-groupes titrés (mêmes name et valeurs : API inchangée)."""
    blocs, i = '', 0
    for k, (titre, options) in enumerate(groupes):
        opts = ''
        for v, l in options:
            opts += ('<label class="choice" for="%s-%s"><input type="radio" id="%s-%s" name="%s" value="%s"%s><span>%s</span></label>'
                     % (fid, v, fid, v, name, v, ' required' if i == 0 else '', l))
            i += 1
        blocs += ('<p class="choices__titre" id="%s-g%d">%s</p><div class="choices" role="group" aria-labelledby="%s-g%d">%s</div>'
                  % (fid, k, titre, fid, k, opts))
    return ('<fieldset class="group" id="%s" aria-describedby="%s-err" data-champ="%s"><legend>%s%s</legend>%s%s</fieldset>'
            % (fid, fid, name, legend, statut, blocs, erreur(fid)))


def champ(fid, name, label, statut, typ='text', aide='', attrs='', cls=''):
    desc = ' '.join(x for x in [('%s-aide' % fid) if aide else '', '%s-err' % fid] if x)
    aide_html = ('<p class="hint" id="%s-aide">%s</p>' % (fid, aide)) if aide else ''
    if typ == 'textarea':
        inp = '<textarea id="%s" name="%s" rows="5" aria-describedby="%s"%s></textarea>' % (fid, name, desc, attrs)
    else:
        inp = '<input id="%s" name="%s" type="%s" aria-describedby="%s"%s>' % (fid, name, typ, desc, attrs)
    return ('<div class="field%s" data-champ="%s"><label for="%s">%s%s</label>%s%s%s</div>'
            % ((' ' + cls) if cls else '', name, fid, label, statut, aide_html, inp, erreur(fid)))


def rappel_lien(etape):
    return ('<p class="dform__rappel"><a href="#rappel" data-vers-rappel data-suivi="rappel_ouvert" data-suivi-etape="%d">'
            'Vous préférez qu\'on vous rappelle ?</a></p>' % etape)


def form_devis(source, service=None):
    """Formulaire de devis en 3 étapes. Sans JavaScript : les 3 étapes l'une sous l'autre, un seul envoi."""
    cartes = ''
    for v, nom, ligne in TRAVAUX:
        nom = nom or svc_nom('cloisons-isothermes')
        chk = ' checked' if service == v else ''
        cartes += ('<label class="choice choice--card" for="d-travaux-%s"><input type="checkbox" id="d-travaux-%s" name="travaux[]" value="%s"%s>'
                   '%s<span class="choice__text"><b>%s</b><span>%s</span></span></label>'
                   % (v, v, v, chk, ICONS[v].replace('class="icon"', 'class="icon choice__icon"'), nom, ligne))
    etape1 = '''<fieldset class="dform__step" data-step="1" data-titre="vos travaux">
            <legend class="dform__legend" tabindex="-1"><span class="dform__num">Étape 1 sur 3</span> Quels travaux souhaitez-vous ?</legend>
            <div class="group" id="d-travaux" data-champ="travaux" aria-describedby="d-travaux-aide d-travaux-err">
              <p class="hint" id="d-travaux-aide">Plusieurs choix possibles.</p>
              <div class="cards">%s</div>
              %s
            </div>
            <div class="dform__actions js-only"><button type="button" class="btn" data-suivant>Continuer : votre projet</button></div>
            <p class="dform__rassure">%s</p>
            %s
          </fieldset>''' % (cartes, erreur('d-travaux'),
                            T('C02', 'La visite et le devis sont gratuits et sans engagement.', 'Vous décidez une fois l\'offre écrite reçue.'), rappel_lien(1))

    etape2 = '''<fieldset class="dform__step" data-step="2" data-titre="votre projet">
            <legend class="dform__legend" tabindex="-1"><span class="dform__num">Étape 2 sur 3</span> Votre projet</legend>
            <p class="dform__oblig">Les champs obligatoires sont indiqués.</p>
            %s
            %s
            <input type="hidden" name="npa" value="">
            %s
            %s
            <div class="dform__actions js-only"><button type="button" class="btn btn--ghost" data-retour>Retour</button><button type="button" class="btn" data-suivant>Continuer : vos coordonnées</button></div>
            <p class="dform__rassure">Ces réponses nous aident à préparer la visite.</p>
            %s
          </fieldset>''' % (
        radios_groupes('d-type', 'type_client', [('Particulier', TYPE_CLIENT[:2]), ('Professionnel', TYPE_CLIENT[2:])], 'Vous êtes', OBL),
        champ('d-commune', 'commune', 'Commune des travaux', OBL, aide='Commune ou NPA, par exemple Lancy ou 1212.',
              attrs=' autocomplete="address-level2" required maxlength="80"'),
        radios('d-delai', 'delai', DELAI, 'Quand souhaitez-vous faire les travaux ?', FAC),
        radios('d-surface', 'surface', SURFACE, 'Quelle surface, à peu près ?', FAC, aide='Une estimation suffit.'),
        rappel_lien(2))

    creneau_aide = T('C03', 'Nous appelons du lundi au vendredi, de 7 h à 18 h.', '')
    connu = ''.join('<option value="%s">%s</option>' % c for c in CONNU)
    etape3 = '''<fieldset class="dform__step" data-step="3" data-titre="vos coordonnées">
            <legend class="dform__legend" tabindex="-1"><span class="dform__num">Étape 3 sur 3</span> Vos coordonnées</legend>
            <p class="dform__oblig">Les champs obligatoires sont indiqués.</p>
            %(civ)s
            %(nom)s
            <fieldset class="group group--joindre"><legend>Comment vous joindre ?</legend><p class="hint">Un des deux suffit.</p>
            %(tel)s
            %(mail)s
            </fieldset>
            %(pref)s
            %(creneau)s
            <p class="dform__sous">Si vous le souhaitez</p>
            %(msg)s
            <div class="field file-field" data-champ="fichiers">
              <span class="label" id="d-fichiers-label">Photos ou plans%(fac)s</span>
              <p class="hint" id="d-fichiers-aide">JPG, PNG, HEIC ou PDF, 3 fichiers de 8 Mo au plus. Trop lourd ? Envoyez-les par e-mail après notre appel.</p>
              <input class="file-input" id="d-fichiers" name="fichiers[]" type="file" multiple accept="image/jpeg,image/png,image/heic,image/heif,.heic,application/pdf" aria-labelledby="d-fichiers-label" aria-describedby="d-fichiers-aide d-fichiers-etat d-fichiers-err">
              <div class="file-row js-only"><button type="button" class="btn btn--ghost file-btn" aria-describedby="d-fichiers-aide d-fichiers-etat" data-fichiers>Choisir des fichiers</button><span class="file-state" id="d-fichiers-etat" aria-live="polite">Aucun fichier choisi</span></div>
              <ul class="file-list js-only"></ul>
              %(err_f)s
            </div>
            <div class="field" data-champ="connu_par"><label for="d-connu">Comment nous avez-vous connus ?%(fac)s</label><select id="d-connu" name="connu_par" aria-describedby="d-connu-err"><option value="">Choisissez dans la liste</option>%(connu)s</select>%(err_c)s</div>
            %(reco)s
            <div class="dform__actions"><button type="button" class="btn btn--ghost js-only" data-retour>Retour</button><button type="submit" class="btn" data-envoi>Envoyer ma demande</button></div>
            <p class="dform__rassure">%(rappel)s</p>
            <p class="dform__info">En envoyant ce formulaire, vous nous transmettez vos coordonnées pour traiter votre demande. Elles ne servent à rien d'autre. <a href="confidentialite.html">Protection des données</a></p>
            %(rap)s
          </fieldset>''' % dict(
        civ=radios('d-civ', 'civilite', [('madame', 'Madame'), ('monsieur', 'Monsieur')], 'Civilité', FAC, cls='group--inline'),
        nom=champ('d-nom', 'nom', 'Nom et prénom', OBL, attrs=' autocomplete="name" required maxlength="100"'),
        tel=champ('d-tel', 'telephone', 'Téléphone', '', typ='tel',
                  aide='Pour vous rappeler et convenir de la visite. Exemple : 079 123 45 67.', attrs=' inputmode="tel" autocomplete="tel" maxlength="30"'),
        mail=champ('d-mail', 'email', 'E-mail', '', typ='email',
                   aide='Pour la confirmation et l\'offre écrite.', attrs=' autocomplete="email" maxlength="254"'),
        rappel=T('C01', 'Nous vous rappelons le jour même ou le jour ouvrable suivant.', 'Nous vous rappelons pendant nos heures de bureau.'),
        pref=radios('d-pref', 'preference_contact', PREF, 'Comment préférez-vous être recontacté(e) ?', FAC),
        creneau=radios('d-creneau', 'creneau', CRENEAU, 'Plutôt…', FAC, aide=creneau_aide, cls='group--inline js-cond'),
        msg=champ('d-msg', 'message', 'Votre projet en quelques mots', FAC, typ='textarea',
                  aide='Par exemple : logement habité ou vide, délai impératif, accès, étage. Professionnels : date de remise des offres.',
                  attrs=' maxlength="3000"'),
        fac=FAC, err_f=erreur('d-fichiers'), err_c=erreur('d-connu'), connu=connu,
        reco=champ('d-reco', 'recommande_par', 'Qui vous a recommandé Andy Construct ?', FAC, aide='Pour pouvoir remercier cette personne.',
                   attrs=' maxlength="100"', cls='js-cond'),
        rap=rappel_lien(3))

    return '''<form class="dform" id="d-form" action="api/demande.php" method="post" enctype="multipart/form-data" data-form="devis" data-suivi-formulaire="devis" aria-labelledby="demande-titre"%s>
          %s
          <div class="dform__head js-only" aria-hidden="true"><p class="dform__etape">Étape 1 sur 3</p><div class="dform__bar"><span></span></div></div>
          <p class="visually-hidden" aria-live="polite" data-annonce></p>
          <p class="dform__recap js-only" hidden>Travaux : <b data-recap></b> · <button type="button" class="linklike" data-modifier>Modifier<span class="visually-hidden"> les travaux</span></button></p>
          <div class="dform__erreurs" tabindex="-1" hidden></div>
          %s
          %s
          %s
          <div class="dform__alerte" role="alert" hidden><p data-alerte-texte></p><button type="button" class="btn btn--ghost" data-reessayer>Réessayer</button></div>
        </form>''' % ((' data-service="%s"' % service) if service else '', cachés('devis', source), etape1, etape2, etape3)


def module_rappel(source, seul=False, niveau='h3', service=None):
    sous = (T('C01', 'Nous vous rappelons le jour même ou le jour ouvrable suivant. Votre numéro ne sert qu\'à ce rappel.',
              'Nous vous rappelons pendant nos heures de bureau. Votre numéro ne sert qu\'à ce rappel.')
            if seul else 'Votre numéro ne sert qu\'à ce rappel.')
    return '''<div class="rappel" id="rappel">
          <%(n)s id="rappel-titre">Vous préférez qu'on vous rappelle ?</%(n)s>
          <p>Laissez simplement votre numéro.</p>
          <form class="rform" id="r-form" action="api/demande.php" method="post" enctype="multipart/form-data" data-form="rappel" data-suivi-formulaire="rappel" aria-labelledby="rappel-titre">
            %(caches)s%(travaux)s
            %(tel)s
            %(nom)s
            %(cren)s
            <div class="dform__alerte" role="alert" hidden><p data-alerte-texte></p><button type="button" class="btn btn--ghost" data-reessayer>Réessayer</button></div>
            <button type="submit" class="btn" data-envoi>Être rappelé(e)</button>
            <p class="rform__note">%(sous)s</p>
          </form>
        </div>''' % dict(n=niveau, caches=cachés('rappel', source), sous=sous,
                         travaux=('<input type="hidden" name="travaux[]" value="%s">' % service) if service else '',
                         tel=champ('r-tel', 'telephone', 'Votre numéro de téléphone', OBL, typ='tel', aide='Exemple : 079 123 45 67',
                                   attrs=' inputmode="tel" autocomplete="tel" required maxlength="30"'),
                         nom=champ('r-nom', 'nom', 'Votre nom', FAC, attrs=' autocomplete="name" maxlength="100"'),
                         cren=radios('r-creneau', 'creneau', CRENEAU, 'Plutôt…', FAC, cls='group--inline'))


def par_telephone():
    h = horaires(long=False)
    return ('<div class="appel-box" data-suivi-zone="bloc_demande"><p class="appel-box__t">Ou appelez le</p>'
            '<p class="appel-box__n">%s</p>%s</div>' % (tel_link(cls='big', emplacement='bloc_demande'), ('<p class="appel-box__h">%s</p>' % h) if h else ''))


def temoignage_court():
    if not ctx.TEMOIGNAGES:
        return ''
    t = ctx.TEMOIGNAGES[0]
    qui = ', '.join(x for x in [t.get('auteur'), t.get('organisation'), t.get('commune')] if x)
    return '<figure class="quote quote--court"><blockquote><p>« %s »</p></blockquote><figcaption>%s</figcaption></figure>' % (e(t['texte']), e(qui))


def bloc_demande(p, service=None, h2=None, intro=None, refs=True, source='accueil', surtitre=False):
    """Bloc de demande v3 : formulaire en 3 étapes ; colonne = téléphone, badges B1 B3 B4 (B9 si C01), premier témoignage,
    rappel replié (ouvert d'office en variante B du drapeau entree-demande). refs : liste courte de références en colonne
    (pages sans bande défilante juste au-dessus). source : champ caché (contrat d'interface §3)."""
    if intro is None:
        intro = ('Encore <b>2 étapes</b>, moins d\'une minute.' if service else '<b>3 étapes</b>, environ <b>une minute</b>.')
    return '''    <section class="section section--mist demande" id="demande" aria-labelledby="demande-titre" data-suivi-zone="bloc_demande">
      <div class="container">
        <div class="demande__head">
          <h2 id="demande-titre">%s</h2>
          <p class="lead">%s</p>
        </div>
        <div class="demande__grid">
          <div class="demande__form">
        %s
          </div>
          <div class="demande__aside">
        %s
        %s
        %s
        <details class="rappel-repli" data-entree-demande><summary>Vous préférez qu'on vous rappelle ?</summary>%s</details>
        %s
          </div>
        </div>
      </div>
    </section>
''' % (h2 or libelle_devis(), intro, form_devis(source, service), par_telephone(),
       badges(['B1', 'B3', '|B9|B4'], cls='badges--clair badges--col', label='Garanties'), temoignage_court(),
       module_rappel('rappel-colonne', service=service), refs_ligne('refs-line--aside') if refs else '')


def cta_band(p, h2='Vous avez un projet ?', texte='Décrivez-le en trois étapes ou appelez-nous : nous convenons d\'une visite.'):
    return '''    <section class="section section--dark on-dark section--tight" aria-labelledby="cta-titre" data-suivi-zone="bande_appel">
      <div class="container cta-band">
        <div>
          <h2 id="cta-titre">%s</h2>
          <p>%s</p>
        </div>
        <div class="cta-band__actions">
          %s
          <a class="btn btn--light" href="%s" data-suivi-numero="fixe">Appeler le %s</a>
        </div>
      </div>
    </section>
''' % (h2, texte, devis_btn(p, 'bande_appel'), TEL_URI, TEL)


# ---------------------------------------------------------------- témoignages et avis (masqués tant qu'ils sont vides)
def temoignages():
    if not ctx.TEMOIGNAGES:
        return ''
    items = ''
    for t in ctx.TEMOIGNAGES[:3]:
        qui = ', '.join(x for x in [t.get('auteur'), t.get('organisation'), t.get('commune')] if x)
        quoi = ', '.join(x for x in [t.get('travaux'), str(t.get('annee') or '')] if x)
        items += ('<figure class="quote"><blockquote><p>« %s »</p></blockquote><figcaption><b>%s</b>%s</figcaption></figure>'
                  % (e(t['texte']), e(qui), (' · ' + e(quoi)) if quoi else ''))
    return '''    <section class="section" aria-labelledby="temoignages-titre">
      <div class="container">
        <h2 id="temoignages-titre">Ce qu'en disent nos clients</h2>
        <div class="quotes">%s</div>
        <p class="muted">Témoignages publiés tels quels, avec l'accord écrit de leurs auteurs.</p>
      </div>
    </section>
''' % items


def avis_ligne():
    a = ctx.AVIS
    if not a or (a.get('nombre') or 0) < 5 or not a.get('note'):
        return ''
    return ('<p class="avis">Avis Google : %s sur 5, %d avis (relevé le %s). <a href="%s" rel="noopener">Lire les avis sur Google</a></p>'
            % (str(a['note']).replace('.', ','), a['nombre'], e(a.get('date_releve', '')), e(a.get('url', ''))))


def form_guide_poste(guide):
    """Guide imprimé par la poste (contrat d'interface §6, copy deck §Q.4) : le PDF reste en libre téléchargement."""
    return '''<details class="poste">
          <summary>Le recevoir imprimé, par la poste</summary>
          <form class="gform" id="g-form" action="api/demande.php" method="post" enctype="multipart/form-data" data-form="envoi_postal_guide" data-suivi-formulaire="envoi_postal_guide" aria-labelledby="g-titre">
            %(caches)s<input type="hidden" name="guide" value="%(guide)s">
            <h3 id="g-titre">Recevoir le guide imprimé</h3>
            %(nom)s
            %(adresse)s
            <div class="gform__ligne">%(npa)s%(localite)s</div>
            %(profil)s
            %(mail)s
            <div class="field js-cond" data-champ="conseils_email" hidden><label class="choice" for="g-conseils"><input type="checkbox" id="g-conseils" name="conseils_email" value="oui"><span>Recevoir aussi deux conseils par e-mail sur ce sujet (puis plus rien ; désinscription en un clic)</span></label></div>
            <div class="dform__alerte" role="alert" hidden><p data-alerte-texte></p><button type="button" class="btn btn--ghost" data-reessayer>Réessayer</button></div>
            <button type="submit" class="btn" data-envoi>Recevoir le guide par la poste</button>
            <p class="rform__note">Envoi sous quelques jours ouvrables. Pas de publicité. Votre adresse sert uniquement à cet envoi. <a href="confidentialite.html">Protection des données</a></p>
          </form>
          <p class="gform__ok" role="status" tabindex="-1" hidden>Merci. Le guide part par la poste dans les prochains jours.</p>
        </details>''' % dict(
        caches=cachés('envoi_postal_guide', 'page-isolation-acoustique'), guide=guide,
        nom=champ('g-nom', 'nom', 'Votre nom', OBL, attrs=' autocomplete="name" required maxlength="100"'),
        adresse=champ('g-adresse', 'adresse', 'Rue et numéro', OBL, attrs=' autocomplete="street-address" required maxlength="150"'),
        npa=champ('g-npa', 'npa', 'NPA', OBL, attrs=' inputmode="numeric" autocomplete="postal-code" required maxlength="4" pattern="[1-9][0-9]{3}"', cls='gform__npa'),
        localite=champ('g-localite', 'localite', 'Localité', OBL, attrs=' autocomplete="address-level2" required maxlength="80"'),
        profil=radios('g-profil', 'profil', [('proprietaire', 'Propriétaire'), ('locataire', 'Locataire'), ('autre', 'Autre')], 'Vous êtes', FAC, cls='group--inline'),
        mail=champ('g-mail', 'email', 'Votre e-mail', ' <span class="opt">(facultatif), pour une confirmation</span>', typ='email', attrs=' autocomplete="email" maxlength="254"'))
