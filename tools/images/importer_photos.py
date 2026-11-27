# -*- coding: utf-8 -*-
"""Import des photos de chantier fournies par le client : tailles web, recadrages éditoriaux, manifeste.

    python3 tools/images/importer_photos.py DOSSIER_SOURCE

- redressement selon l'orientation de l'appareil, métadonnées supprimées (GPS, appareil) ;
- tailles 400 / 800 / 1600 / 2400 en WebP (+ 800 en JPEG), jamais au-delà de la définition d'origine ;
- recadrages 4:5 (en-têtes sur ordinateur) et 16:9 (mobile, bandeaux) centrés sur le sujet ;
- mise à jour de site/assets/img/portfolio/manifest.json et recadrages.json.
Nécessite ImageMagick (convert, identify).
"""
import json, math, os, subprocess, sys

ICI = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(ICI))
DEST = os.path.join(ROOT, 'site', 'assets', 'img', 'portfolio')
REL = 'assets/img/portfolio/'
TAILLES = (400, 800, 1600, 2400)
NET = ['-filter', 'Lanczos', '-unsharp', '0x0.6+0.6+0.01']

# fichier source (préfixe) : id, titre, alt, catégorie, (fx 4:5, fy 4:5), (fx 16:9, fy 16:9)
PHOTOS = [
    ('IMG_9161', 'couloir-plafond-ligne-lumineuse-01', 'Couloir : plafond en plaques de plâtre et ligne lumineuse',
     'Long couloir blanc, plafond en plaques de plâtre parcouru d\'une ligne lumineuse encastrée', 'faux-plafonds', (.5, .5), (.5, .5)),
    ('IMG_9162', 'baffles-acoustiques-eclairage-indirect-01', 'Panneaux acoustiques suspendus et éclairage indirect',
     'Panneaux acoustiques gris suspendus sous un plafond en béton, éclairage indirect chaud', 'acoustique', (.5, .45), (.5, .38)),
    ('IMG_9169', 'panneaux-acoustiques-sous-charpente-01', 'Panneaux acoustiques suspendus sous une charpente',
     'Panneaux acoustiques suspendus et luminaires linéaires sous une charpente en bois', 'acoustique', (.5, .45), (.5, .42)),
    ('Plafond_tissu_tendu', 'piscine-plafond-tendu-lumineux-01', 'Piscine : plafond tendu et cercles lumineux',
     'Piscine intérieure sous un plafond tendu blanc percé de cercles lumineux, mur éclairé en lumière rasante', 'faux-plafonds', (.5, .5), (.5, .3)),
    ('Tissu_tendu_cadres', 'tissu-tendu-cadres-espace-vitre-01', 'Tissu tendu et cadres lumineux dans un espace vitré',
     'Plafond en tissu tendu à cadres lumineux carrés, dans une salle largement vitrée sur un parc', 'faux-plafonds', (.5, .5), (.5, .42)),
    ('Tissu_tendu_faux_plafond', 'combles-amenages-charpente-01', 'Combles aménagés : surfaces lisses sous la charpente',
     'Grand volume sous combles : rampants lisses et blancs entre les fermes de la charpente en bois', 'platrerie-peinture', (.5, .42), (.5, .32)),
    ('Tissu_tendu_faux_plafonds_acoustiques', 'salon-ovales-tissu-tendu-01', 'Salon : îlots ovales en tissu tendu et éclairage indirect',
     'Salon aux banquettes bleues sous des îlots ovales en tissu tendu, bordés d\'un éclairage indirect', 'faux-plafonds', (.42, .5), (.5, .45)),
    ('platrerie_peinture', 'piece-combles-platrerie-peinture-01', 'Pièce sous combles : plâtrerie, peinture et doublages',
     'Pièce sous combles : rampants et doublages en plaques de plâtre peints en blanc, fenêtre de toit sur le lac', 'platrerie-peinture', (.55, .5), (.5, .5)),
    ('technique_de_tracage', 'tracage-laser-plafond-01', 'Traçage au laser avant la pose d\'un plafond',
     'Lignes laser rouge et verte projetées au plafond pour tracer l\'implantation avant la pose', 'methode', (.42, .5), (.5, .4)),
    ('traitement_acoustique_restaurant', 'restaurant-traitement-acoustique-01', 'Restaurant : traitement acoustique du plafond',
     'Salle de restaurant sous un plafond voûté traité en acoustique, retombées blanches et éclairage intégré', 'acoustique', (.5, .5), (.5, .62)),
    ('traitement_cadre_acoustique', 'salle-de-reunion-cadres-acoustiques-01', 'Salle de réunion : cadres acoustiques au plafond',
     'Salle de réunion blanche sous de grands cadres acoustiques suspendus, spots encastrés', 'acoustique', (.5, .45), (.5, .58)),
]


def dims(f):
    w, h = subprocess.check_output(['identify', '-format', '%w %h', f]).decode().split()
    return int(w), int(h)


def ecrire(src, sortie, largeur, crop=None):
    cmd = ['convert', src, '-auto-orient', '-strip']
    if crop:
        x, y, w, h = crop
        cmd += ['-crop', '%dx%d+%d+%d' % (w, h, x, y), '+repage']
    cmd += NET + ['-resize', '%dx>' % largeur]
    for ext, q in (('webp', 80), ('jpg', 84)):
        if ext == 'jpg' and not sortie.endswith('-800'):
            continue
        subprocess.check_call(cmd + ['-quality', str(q)] + (['-interlace', 'Plane', '-sampling-factor', '4:2:0'] if ext == 'jpg' else
                                                           ['-define', 'webp:method=6']) + ['%s.%s' % (sortie, ext)])


# Étalonnage commun (v8) : toutes les photos ramenées à la même lumière, pour un ensemble cohérent.
CIBLE_LUM = 0.52                       # luminance moyenne visée
TEINTE = (1.015, 1.0, 0.975)           # neutre légèrement chaud, identique pour toutes les photos
FORCE_BALANCE = 0.75                   # part de la dominante corrigée (0 = rien, 1 = gris neutre strict)


def mesures(f):
    v = subprocess.check_output(['convert', f, '-resize', '1024x1024>', '-format',
                                 '%[fx:mean.r] %[fx:mean.g] %[fx:mean.b] %[fx:standard_deviation]', 'info:']).decode().split()
    return [float(x) for x in v]


def etalonner(src, dst):
    """Balance des blancs (gris neutre légèrement chaud), exposition par gamma, contraste relevé si l'image est plate,
    hautes lumières protégées. Renvoie les réglages appliqués."""
    r, g, b, sd = mesures(src)
    m = (r + g + b) / 3
    gains = [1 + FORCE_BALANCE * (m * t / c - 1) for c, t in zip((r, g, b), TEINTE)]
    m2 = sum(c * k for c, k in zip((r, g, b), gains)) / 3
    gamma = min(1.35, max(0.8, math.log(m2) / math.log(CIBLE_LUM)))
    contraste = 4 if sd < 0.12 else 2.5 if sd < 0.17 else 0
    cmd = ['convert', src, '-color-matrix', '%.4f 0 0 0 %.4f 0 0 0 %.4f' % tuple(gains), '-gamma', '%.3f' % gamma]
    if contraste:
        cmd += ['-sigmoidal-contrast', '%gx50%%' % contraste]
    cmd += ['-level', '0%,99.4%', dst]
    subprocess.check_call(cmd)
    return dict(gains=[round(x, 3) for x in gains], gamma=round(gamma, 3), contraste=contraste)


def cadre(w, h, ratio, fx, fy):
    """Plus grand cadre au ratio donné, centré au mieux sur (fx, fy)."""
    cw, ch = (w, round(w / ratio)) if w / h < ratio else (round(h * ratio), h)
    cw, ch = min(cw, w), min(ch, h)
    x = min(max(round(fx * w - cw / 2), 0), w - cw)
    y = min(max(round(fy * h - ch / 2), 0), h - ch)
    return x, y, cw, ch


def main():
    src_dir = sys.argv[1]
    fichiers = sorted(os.listdir(src_dir))
    man_p = os.path.join(DEST, 'manifest.json')
    rec_p = os.path.join(DEST, 'recadrages.json')
    manifest = [m for m in json.load(open(man_p, encoding='utf-8')) if m['id'] not in {p[1] for p in PHOTOS}]
    recs = [r for r in json.load(open(rec_p, encoding='utf-8')) if r['id'] not in {p[1] for p in PHOTOS}]
    for prefixe, pid, titre, alt, cat, f45, f169 in PHOTOS:
        src = os.path.join(src_dir, next(f for f in fichiers if prefixe in f))
        tmp = '/tmp/_redresse.png'
        subprocess.check_call(['convert', src, '-auto-orient', '-strip', '/tmp/_brut.png'])
        reglages = etalonner('/tmp/_brut.png', tmp)
        w, h = dims(tmp)
        base = os.path.join(DEST, pid)
        it = dict(id=pid, fichier_source=os.path.basename(src), base=REL + pid, titre=titre, alt=alt, categorie=cat,
                  orientation='portrait' if h > w else 'paysage', qualite=5, role='client-v6', etalonnage=reglages)
        for t in TAILLES:
            lw = min(t, w)
            ecrire(tmp, '%s-%d' % (base, t), lw)
            it['largeur_%d' % t], it['hauteur_%d' % t] = lw, round(h * lw / w)
        manifest.append(it)
        r = {'id': pid, 'fichier_source': it['fichier_source'], 'recadrages': {}}
        for nom, ratio, (fx, fy) in (('4x5', 4 / 5, f45), ('16x9', 16 / 9, f169)):
            x, y, cw, ch = cadre(w, h, ratio, fx, fy)
            larg = [t for t in (800, 1600, 2400) if t <= cw]
            if not larg or cw > max(larg) * 1.1:     # garder la définition d'origine
                larg.append(cw)
            b = '%s-%s' % (base, nom)
            for t in larg:
                ecrire(tmp, '%s-%d' % (b, t), t, (x, y, cw, ch))
            if 800 not in larg:          # le JPEG de repli est toujours nommé -800
                ecrire(tmp, '%s-800' % b, cw, (x, y, cw, ch))
            top = max(larg)
            r['recadrages'][nom] = dict(base=REL + pid + '-' + nom, largeurs=larg, largeur=top, hauteur=round(top * ch / cw),
                                        cadre_source_px=[x, y, x + cw, y + ch])
        recs.append(r)
        print('%-44s %4dx%-4d  4:5 %s  16:9 %s' % (pid, w, h, r['recadrages']['4x5']['largeurs'], r['recadrages']['16x9']['largeurs']))
    json.dump(manifest, open(man_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(recs, open(rec_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
