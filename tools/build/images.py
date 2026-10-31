# -*- coding: utf-8 -*-
"""Préparation des images du site v2 (à lancer à la main, pas à chaque génération).

Usage, depuis la racine du dépôt (Pillow requis) :
    python3 tools/build/images.py [--avant-apres <dossier des 14 JPG de l'ancien site>]

Ce script :
- crée les variantes 400 px des photos du portfolio (vignettes, audit n° 27) ;
- recadre l'héro pour le mobile (portrait 3:4) et ajoute une variante 1200 px ;
- recadre `plafond-placo-ilot-ovale-01` pour masquer le slogan visible au mur (architecture §8.4, n° 18) ;
- refait l'image Open Graph (1200 × 630) à partir de l'héro ;
- réduit les logos de l'en-tête et du pied de page à leur taille d'affichage (× 2) ;
- optimise les paires avant / après (WebP + JPG, 400 px et taille d'origine, sans métadonnées EXIF).
Aucune image n'est agrandie : les originaux de l'ancien site font 800 px au plus.
"""
import json, os, sys
from PIL import Image, ImageOps

ICI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(os.path.dirname(ICI)), 'site')
PORT = os.path.join(SITE, 'assets/img/portfolio')
AA_DIR = os.path.join(SITE, 'assets/img/avant-apres')

# Paires avant / après de l'ancien site (architecture §8.5, copy deck §G.4 et §O)
PAIRES = [
    ('aa1', 'caisson-verriere', '01', '02'),
    ('aa2', 'gaine-ventilation-couloir', '03', '04'),
    ('aa3', 'combles-fenetre-de-toit', '05', '06'),
    ('aa4', 'caisson-ventilation', '07', '08'),
    ('aa5', 'couloir-puits-de-lumiere', '09', '10'),
    ('aa6', 'sejour-faux-plafond', '11', '12'),
    ('aa7', 'paroi-cintree', '13', '14'),
]


def ouvrir(chemin):
    im = Image.open(chemin)
    im = ImageOps.exif_transpose(im)  # orientation appliquée, puis EXIF abandonné à l'enregistrement
    return im.convert('RGB')


def enregistrer(im, base, largeur, jpg=True, q_webp=78, q_jpg=80):
    """Enregistre <base>-<largeur>.webp (et .jpg) sans métadonnées, sans agrandir."""
    if im.width > largeur:
        im = im.resize((largeur, round(im.height * largeur / im.width)), Image.LANCZOS)
    im.save('%s-%d.webp' % (base, largeur), 'WEBP', quality=q_webp, method=6)
    if jpg:
        im.save('%s-%d.jpg' % (base, largeur), 'JPEG', quality=q_jpg, optimize=True, progressive=True)
    return im.size


def portfolio():
    manifest = json.load(open(os.path.join(PORT, 'manifest.json'), encoding='utf-8'))
    for it in manifest:
        src = os.path.join(SITE, it['base'] + '-1600.webp')
        im = ouvrir(src)
        it['largeur_400'], it['hauteur_400'] = enregistrer(im, os.path.join(SITE, it['base']), 400, jpg=False)
    # Héro : variante 1200 px et recadrage portrait pour le mobile
    hero = 'faux-plafond-placo-gorge-lumineuse-01'
    im = ouvrir(os.path.join(PORT, hero + '-1600.webp'))
    enregistrer(im, os.path.join(PORT, hero), 1200, jpg=False, q_webp=74)
    x0 = 330  # garde l'ellipse lumineuse et les spots, le mur clair de gauche passe sous le voile
    portrait = im.crop((x0, 0, x0 + 900, 1200))
    for w in (600, 900):
        enregistrer(portrait, os.path.join(PORT, hero + '-portrait'), w, jpg=False, q_webp=70)
    # Open Graph 1200 × 630
    og = im.crop((0, 150, 1600, 150 + 840)).resize((1200, 630), Image.LANCZOS)
    og.save(os.path.join(SITE, 'assets/img/og-andy-construct.jpg'), 'JPEG', quality=82, optimize=True, progressive=True)
    # Îlot ovale : recadrage qui exclut le slogan du client (bas gauche de la photo)
    ilot = ouvrir(os.path.join(PORT, 'plafond-placo-ilot-ovale-01-1600.webp')).crop((0, 0, 1380, 920))
    base = os.path.join(PORT, 'plafond-placo-ilot-ovale-01-recadre')
    for w in (1200, 800, 400):
        enregistrer(ilot, base, w, jpg=(w == 800))
    entree = next(x for x in manifest if x['id'] == 'plafond-placo-ilot-ovale-01')
    entree['recadre'] = {'base': 'assets/img/portfolio/plafond-placo-ilot-ovale-01-recadre',
                         'largeur_1200': 1200, 'hauteur_1200': 800, 'largeur_800': 800, 'hauteur_800': 533,
                         'largeur_400': 400, 'hauteur_400': 267}
    with open(os.path.join(PORT, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write('\n')


def logos():
    brand = os.path.join(SITE, 'assets/img/brand')
    for nom, w in (('logo-andy-construct', 352), ('logo-andy-construct-blanc', 380)):
        im = Image.open(os.path.join(brand, nom + '.png')).convert('RGBA')
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        # PNG à palette de 48 couleurs : ≈ 6 Ko, plus léger que le WebP pour un logo en aplats
        im.quantize(48, method=Image.Quantize.FASTOCTREE).save(os.path.join(brand, '%s-%d.png' % (nom, w)), 'PNG', optimize=True)


def avant_apres(dossier):
    os.makedirs(AA_DIR, exist_ok=True)
    sortie = []
    for code, slug, a, b in PAIRES:
        paire = {'id': code, 'slug': slug}
        for etat, num in (('avant', a), ('apres', b)):
            im = ouvrir(os.path.join(dossier, num + '.jpg'))
            base = os.path.join(AA_DIR, '%s-%s-%s' % (code, slug, etat))
            w0 = im.width
            tailles = {}
            for w in sorted({400, w0}):
                tailles[w] = enregistrer(im, base, w, q_webp=80, q_jpg=82)
            paire[etat] = {'base': 'assets/img/avant-apres/%s-%s-%s' % (code, slug, etat),
                           'largeurs': sorted(tailles), 'largeur': im.width, 'hauteur': im.height}
        sortie.append(paire)
    with open(os.path.join(AA_DIR, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(sortie, f, ensure_ascii=False, indent=2)
        f.write('\n')


if __name__ == '__main__':
    portfolio()
    logos()
    if '--avant-apres' in sys.argv:
        avant_apres(sys.argv[sys.argv.index('--avant-apres') + 1])
    print('images prêtes')
