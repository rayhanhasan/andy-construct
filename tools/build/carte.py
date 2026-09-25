# -*- coding: utf-8 -*-
"""Carte « Zone d'intervention » : SVG inline de la Suisse romande, généré sans dépendance.

Données : data/suisse-occidentale.json (préparé par carte_donnees.py, limites swisstopo / OFS).
Projection équirectangulaire locale (cos 46,7°), simplification Douglas-Peucker par arc
(les frontières communes restent identiques), marqueurs = « A » du logo vectorisé depuis le favicon.
"""
import json, math, os
from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(os.path.dirname(ICI)), 'site')

# Emprise affichée (lon/lat) et largeur du viewBox
LON0, LON1, LAT0, LAT1 = 5.90, 7.98, 45.83, 47.52
W = 800
K = W / ((LON1 - LON0) * math.cos(math.radians(46.7)))
H = round((LAT1 - LAT0) * K)

ROMANDS = {25: 'Genève', 22: 'Vaud', 24: 'Neuchâtel', 10: 'Fribourg', 26: 'Jura'}
VALAIS, BERNE = 23, 2  # rendus via leurs districts romands


def proj(lon, lat):
    return ((lon - LON0) * math.cos(math.radians(46.7)) * K, (LAT1 - lat) * K)


def dp(pts, eps):
    """Douglas-Peucker itératif."""
    if len(pts) < 3:
        return pts
    garde = [False] * len(pts)
    garde[0] = garde[-1] = True
    pile = [(0, len(pts) - 1)]
    while pile:
        a, b = pile.pop()
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy) or 1e-9
        dmax, imax = 0, None
        for i in range(a + 1, b):
            x, y = pts[i]
            d = abs(dy * x - dx * y + x2 * y1 - y2 * x1) / n
            if d > dmax:
                dmax, imax = d, i
        if imax is not None and dmax > eps:
            garde[imax] = True
            pile += [(a, imax), (imax, b)]
    return [p for p, k in zip(pts, garde) if k]


def charger(eps=0.7, marge=12):
    data = json.load(open(os.path.join(ICI, 'data', 'suisse-occidentale.json'), encoding='utf-8'))

    def pt(lon, lat):
        # les sommets hors cadre sont ramenés juste au bord (invisible), ce qui allège les tracés
        x, y = proj(lon, lat)
        return (min(max(x, -marge), W + marge), min(max(y, -marge), H + marge))

    arcs = [dp([pt(*p) for p in a], eps) for a in data['arcs']]

    def chemin(polys):
        d = []
        for poly in polys:
            for ring in poly:
                pts = []
                for i in ring:
                    a = arcs[i] if i >= 0 else arcs[~i][::-1]
                    pts.extend(a if not pts else a[1:])
                pts = [(round(x), round(y)) for x, y in pts]
                pts = [p for k, p in enumerate(pts) if k == 0 or p != pts[k - 1]]
                if len(pts) < 3 or all(not (0 <= x <= W and 0 <= y <= H) for x, y in pts):
                    continue
                seg = ['M%d %d' % pts[0]]
                seg += ['l%d %d' % (x - px, y - py) for (px, py), (x, y) in zip(pts, pts[1:])]
                d.append(''.join(seg) + 'z')
        return ''.join(d).replace(' -', '-')

    obj = {}
    for k, v in data['objets'].items():
        obj[k] = {}
        for o in v:
            c = chemin(o['polys'])
            if c:
                obj[k][o['id'] if k == 'country' else int(o['id'])] = c
    return obj


def vectoriser_a(png=os.path.join(SITE, 'assets/img/brand/favicon-192.png'), seuil=128, eps=1.1):
    """Contour du « A » (pixels opaques) en chemin SVG, normalisé dans sa boîte englobante."""
    im = Image.open(png).convert('RGBA')
    w, h = im.size
    alpha = im.getchannel('A').load()
    plein = lambda x, y: 0 <= x < w and 0 <= y < h and alpha[x, y] >= seuil
    aretes = {}
    for y in range(h):
        for x in range(w):
            if not plein(x, y):
                continue
            if not plein(x, y - 1): aretes.setdefault((x, y), []).append((x + 1, y))
            if not plein(x + 1, y): aretes.setdefault((x + 1, y), []).append((x + 1, y + 1))
            if not plein(x, y + 1): aretes.setdefault((x + 1, y + 1), []).append((x, y + 1))
            if not plein(x - 1, y): aretes.setdefault((x, y + 1), []).append((x, y))
    boucles = []
    while aretes:
        depart = next(iter(aretes))
        boucle, p = [depart], depart
        while True:
            suivants = aretes.get(p)
            if not suivants:
                break
            q = suivants.pop()
            if not suivants:
                del aretes[p]
            if q == depart:
                break
            boucle.append(q)
            p = q
        if len(boucle) > 8:
            boucles.append(boucle)
    xs = [x for b in boucles for x, _ in b]
    ys = [y for b in boucles for _, y in b]
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    d = ''
    for b in boucles:
        # boucle fermée : découpée au point le plus éloigné du départ avant simplification
        k = max(range(len(b)), key=lambda i: (b[i][0] - b[0][0]) ** 2 + (b[i][1] - b[0][1]) ** 2)
        s = dp(b[:k + 1], eps) + dp(b[k:] + [b[0]], eps)[1:-1]
        d += 'M' + 'L'.join('%d %d' % (x - x0, y - y0) for x, y in s) + 'Z'
    return d, x1 - x0, y1 - y0


# Villes (lon, lat, côté de l'étiquette : 1 = droite, -1 = gauche)
VILLES = [
    ('Nyon', 6.2396, 46.3833, -1), ('Lausanne', 6.6323, 46.5197, 1), ('Yverdon-les-Bains', 6.6412, 46.7785, -1),
    ('Neuchâtel', 6.9293, 46.9900, 1), ('Fribourg', 7.1610, 46.8065, 1), ('Sion', 7.3606, 46.2331, 1),
    ('Delémont', 7.3435, 47.3649, 1), ('Bienne', 7.2474, 47.1368, 1),
]
SIEGE = ('Carouge', 6.1397, 46.1838)
# Étiquettes des cantons (lon, lat) placées hors des villes
CANTONS_LBL = [('GENÈVE', 5.93, 46.262), ('VAUD', 6.33, 46.63), ('NEUCHÂTEL', 6.40, 47.065), ('FRIBOURG', 7.06, 46.62),
               ('VALAIS', 7.08, 46.07), ('JURA', 7.02, 47.43), ('JURA BERNOIS', 7.18, 47.235)]


def carte_svg():
    obj = charger()
    a_d, a_w, a_h = vectoriser_a()
    autres = ''.join('<path d="%s"/>' % d for cid, d in obj['cantons'].items() if cid not in ROMANDS)
    romands = ''.join('<path d="%s"/>' % obj['cantons'][cid] for cid in ROMANDS)
    districts = ''.join('<path d="%s"/>' % d for d in obj['districts'].values())
    lacs = ''.join('<path d="%s"/>' % d for d in obj['lakes'].values())
    pays = obj['country']['CH']

    def marque(lon, lat, hauteur):
        x, y = proj(lon, lat)
        lw = hauteur * a_w / a_h
        return ('<circle cx="%.1f" cy="%.1f" r="3.2"/>' % (x, y),
                '<use href="#andy-a" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>' % (x - lw * .35, y - hauteur - 2, lw, hauteur),
                x, y, lw)

    points, pins, etiquettes = '', '', ''
    for nom, lon, lat, cote in VILLES:
        c, u, x, y, lw = marque(lon, lat, 26)
        points += c; pins += u
        tx = x + (lw * .75 + 6 if cote > 0 else -lw * .45 - 6)
        etiquettes += '<text class="c-ville" x="%.1f" y="%.1f"%s>%s</text>' % (tx, y - 8, '' if cote > 0 else ' text-anchor="end"', nom)
    c, u, x, y, lw = marque(SIEGE[1], SIEGE[2], 44)
    points += c.replace('r="3.2"', 'r="4.5"'); pins += u
    siege = '<text class="c-siege" x="%.1f" y="%.1f">Siège — Carouge</text>' % (x + lw * .7 + 8, y - 14)
    cantons = ''.join('<text class="c-canton" x="%.1f" y="%.1f">%s</text>' % (proj(lon, lat) + (n,)) for n, lon, lat in CANTONS_LBL)

    return '''<svg class="carte__svg" viewBox="0 0 %(W)d %(H)d" role="img" aria-labelledby="carte-titre carte-desc">
            <title id="carte-titre">Zone d'intervention d'Andy Construct : toute la Suisse romande</title>
            <desc id="carte-desc">Carte de la Suisse occidentale. En gris : cantons de Genève, Vaud, Neuchâtel, Fribourg et Jura, Valais romand et Jura bernois. Le « A » du logo Andy Construct marque le siège à Carouge (Genève) et les villes de Nyon, Lausanne, Yverdon-les-Bains, Neuchâtel, Fribourg, Sion, Delémont et Bienne.</desc>
            <defs><symbol id="andy-a" viewBox="0 0 %(aw)d %(ah)d"><path fill="#E8000F" fill-rule="evenodd" d="%(ad)s"/></symbol></defs>
            <g class="c-autres">%(autres)s</g>
            <g class="c-districts">%(districts)s</g>
            <g class="c-romands">%(romands)s</g>
            <g class="c-lacs">%(lacs)s</g>
            <path class="c-pays" d="%(pays)s"/>
            <g class="c-noms" aria-hidden="true">%(cantons)s</g>
            <g class="c-points">%(points)s</g>
            <g class="c-pins">%(pins)s</g>
            <g class="c-lbl" aria-hidden="true">%(etiquettes)s%(siege)s</g>
            <g class="c-cartouche" aria-hidden="true">
              <rect x="14" y="14" width="228" height="118"/>
              <image href="assets/img/brand/logo-andy-construct.png" x="30" y="28" width="150" height="54"/>
              <text class="c-cart-t" x="30" y="104">Zone d'intervention</text>
              <text class="c-cart-s" x="30" y="122">toute la Suisse romande</text>
            </g>
          </svg>''' % dict(W=W, H=H, aw=a_w, ah=a_h, ad=a_d, autres=autres, districts=districts, romands=romands, lacs=lacs, pays=pays,
                           cantons=cantons, points=points, pins=pins, etiquettes=etiquettes, siege=siege)


if __name__ == '__main__':
    s = carte_svg()
    print(len(s.encode()), 'octets', W, H)
