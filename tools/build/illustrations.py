# -*- coding: utf-8 -*-
"""Images d'illustration sous licence (site/assets/img/illustrations/illustrations.json, fourni par l'agent images).

Règle du brief v3 : jamais présentées comme des réalisations d'Andy Construct. Chaque image porte une mention
« Illustration » visible et un texte alternatif générique. Tant que le manifeste n'existe pas, rien n'est rendu
(les cartes retombent sur une vraie photo ou un pictogramme).

Champs lus (tolérants) : id, fichier | base, largeur, hauteur, alt, service(s) | usage, credit, licence, variantes.
"""
import json, os
import ctx
from ctx import e

DIR = os.path.join(ctx.SITE, 'assets/img/illustrations')
MANIFESTE = os.path.join(DIR, 'illustrations.json')


def _charger():
    if not os.path.exists(MANIFESTE):
        return []
    d = json.load(open(MANIFESTE, encoding='utf-8'))
    if isinstance(d, dict):
        d = d.get('images') or d.get('illustrations') or list(d.values())
    return [x for x in d if isinstance(x, dict)]


ITEMS = _charger()


def _services(it):
    s = it.get('services') or it.get('service') or it.get('usage') or []
    return [s] if isinstance(s, str) else list(s)


def trouver(service=None, usage=None):
    for it in ITEMS:
        if it.get('statut') in ('retirer', 'refuse'):
            continue
        if service and service in _services(it):
            return it
        if usage and usage in _services(it):
            return it
    return None


def _src(it):
    """(srcset webp, src de repli, largeur, hauteur) selon les champs disponibles."""
    base = it.get('base')
    w, h = it.get('largeur') or it.get('width') or 1200, it.get('hauteur') or it.get('height') or 800
    if base:
        larg = it.get('largeurs') or [400, 800, 1200]
        dispo = [x for x in larg if os.path.exists(os.path.join(ctx.SITE, '%s-%d.webp' % (base, x)))
                 or os.path.exists(os.path.join(DIR, '%s-%d.webp' % (os.path.basename(base), x)))]
        b = base if base.startswith('assets/') else 'assets/img/illustrations/' + base
        srcset = ', '.join('%s-%d.webp %dw' % (b, x, x) for x in (dispo or larg))
        jpg = '%s-%d.jpg' % (b, (dispo or larg)[min(1, len(dispo or larg) - 1)])
        if not os.path.exists(os.path.join(ctx.SITE, jpg)):
            jpg = '%s-%d.webp' % (b, (dispo or larg)[-1])
        return srcset, jpg, w, h
    f = it.get('fichier') or it.get('file')
    f = f if f.startswith('assets/') else 'assets/img/illustrations/' + f
    return None, f, w, h


def picture(it, sizes, cls='', lazy=True):
    srcset, src, w, h = _src(it)
    source = ('<source type="image/webp" srcset="%s" sizes="%s">' % (srcset, sizes)) if srcset else ''
    return ('<span class="ill%s"><picture>%s<img src="%s" width="%d" height="%d" alt="%s"%s decoding="async"></picture>'
            '<span class="ill__tag">Illustration</span></span>'
            % ((' ' + cls) if cls else '', source, src, w, h, e(it.get('alt') or ''), ' loading="lazy"' if lazy else ''))


def pour_service(service, sizes):
    it = trouver(service=service)
    return picture(it, sizes) if it else None
