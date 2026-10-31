#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Supports PDF d'Andy Construct (copy-deck.md §Q, décisions D3 et D7).

Produit, à partir des textes du copy deck, de la charte (brief-design.md), des photos du
portfolio et des logos de références :

  site/assets/docs/andy-construct-references.pdf          plaquette, version production
  livrables/andy-construct-references-preview.pdf         plaquette, version de validation
  site/assets/docs/guide-reduire-le-bruit.pdf             guide pour les propriétaires
  site/assets/docs/checklist-chantier-site-occupe.pdf     liste de contrôle pour les régies

Production : texte de repli pour tout code Cxx non confirmé, logos « autorise » seulement.
Preview : texte définitif, codes Cxx signalés en exposant, logos « a_autoriser » affichés.
Les confirmations sont lues dans tools/build/donnees/confirmations.json (décision D6), si le
fichier existe ; sinon rien n'est considéré comme confirmé. Les valeurs à fournir par le client
(effectif, interlocuteurs, années des références) sont dans valeurs-supports.json.

Usage : python3 livrables/sources/generer_supports.py [--apercus DOSSIER] [--date AAAA-MM-JJ]
Dépendances : reportlab, svglib, fonttools, brotli, Pillow, pypdf ; pdftoppm pour les aperçus.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ICI = Path(__file__).resolve().parent
RACINE = ICI.parents[1]
SITE = RACINE / 'site'
IMG = SITE / 'assets' / 'img'
DOCS_SITE = SITE / 'assets' / 'docs'
LIVRABLES = RACINE / 'livrables'
CONFIRMATIONS = RACINE / 'tools' / 'build' / 'donnees' / 'confirmations.json'
VALEURS = ICI / 'valeurs-supports.json'

# Charte (brief-design.md §3)
ROUGE = HexColor('#E8000F')
ROUGE_F = HexColor('#C4000D')
ANTH = HexColor('#1D1F22')
GRAPH = HexColor('#44494F')
ACIER = HexColor('#B9BDC2')
BRUME = HexColor('#F4F4F5')
TRAIT = HexColor('#E2E3E5')
GRIS_M = HexColor('#D4D6D9')   # gris moyen des schémas (dérivé de Trait et Acier)

W, H = A4
ML, MR = 20 * mm, 20 * mm
CW = W - ML - MR
BAS = 22 * mm
NB = ' '
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août',
        'septembre', 'octobre', 'novembre', 'décembre']
URL_PRO_QR = 'https://www.andyconstruct.ch/professionnels.html?utm_source=plaquette&utm_medium=print&utm_campaign=dossier-references'


class Debordement(Exception):
    pass


TOLERANT = False   # --brouillon : signale les débordements sans s'arrêter (mise au point)


def debordement(msg):
    if TOLERANT:
        print('DÉBORDEMENT :', msg)
    else:
        debordement(msg)


# --------------------------------------------------------------------------------------------
# Polices, typographie, styles
# --------------------------------------------------------------------------------------------

def enregistrer_polices(cache: Path):
    """Convertit les woff2 du site en TTF (même dessin, même licence OFL) et les enregistre."""
    from fontTools.ttLib import TTFont as FTFont
    noms = {
        'Mont-600': 'montserrat-latin-600-normal', 'Mont-700': 'montserrat-latin-700-normal',
        'Sans': 'source-sans-3-latin-400-normal', 'Sans-600': 'source-sans-3-latin-600-normal',
        'Sans-It': 'source-sans-3-latin-400-italic',
    }
    ps = {'Mont-600': 'Montserrat-SemiBold', 'Mont-700': 'Montserrat-Bold', 'Sans': 'SourceSans3-Regular',
          'Sans-600': 'SourceSans3-SemiBold', 'Sans-It': 'SourceSans3-Italic'}
    for nom, f in noms.items():
        ttf = cache / (f + '.ttf')
        if not ttf.exists():
            t = FTFont(str(SITE / 'assets' / 'fonts' / (f + '.woff2')))
            t.flavor = None
            t['name'].setName(ps[nom], 6, 3, 1, 0x409)       # nom PostScript lisible dans le PDF
            t['name'].setName(ps[nom], 6, 1, 0, 0)
            t.save(str(ttf))
        pdfmetrics.registerFont(TTFont(nom, str(ttf)))
    # Les dessins (code QR, logos SVG) partent d'une police par défaut : on prend une police incorporée.
    from reportlab.graphics import shapes
    shapes.STATE_DEFAULTS['fontName'] = 'Sans'
    registerFontFamily('Sans', normal='Sans', bold='Sans-600', italic='Sans-It', boldItalic='Sans-600')
    registerFontFamily('Mont-600', normal='Mont-600', bold='Mont-700', italic='Mont-600', boldItalic='Mont-700')
    registerFontFamily('Mont-700', normal='Mont-700', bold='Mont-700', italic='Mont-700', boldItalic='Mont-700')


def fr(t: str) -> str:
    """Espaces insécables à la française (même règle que tools/build/common.py, fr())."""
    t = re.sub(r' ([:;?!»])', NB + r'\1', t)
    t = t.replace('« ', '«' + NB)
    t = re.sub(r'\+41 (\d\d) (\d\d\d) (\d\d) (\d\d)', lambda m: NB.join(['+41'] + list(m.groups())), t)
    t = re.sub(r'\b0(\d\d) (\d\d\d) (\d\d) (\d\d)\b', lambda m: NB.join(['0' + m.group(1)] + list(m.groups()[1:])), t)
    t = re.sub(r'(\d+) (h|cm|mm|m²|jours|minutes|pages|personnes|ans)\b', r'\1' + NB + r'\2', t)
    t = re.sub(r'\b(CFC|SIA|art\.|IDE|CHF|AEAI) (\w)', r'\1' + NB + r'\2', t)
    t = re.sub(r'(\d) (h|juin)\b', r'\1' + NB + r'\2', t)
    t = t.replace(' – ', NB + '– ').replace(' · ', NB + '· ')
    return t


def S(nom, police='Sans', taille=12.5, interligne=None, couleur=ANTH, align=TA_LEFT, **kw):
    return ParagraphStyle(nom, fontName=police, fontSize=taille, leading=interligne or round(taille * 1.42, 1),
                          textColor=couleur, alignment=align, **kw)


def e(t) -> str:
    return escape(str(t))


def date_longue(d: dt.date) -> str:
    return f'{"1er" if d.day == 1 else d.day} {MOIS[d.month - 1]} {d.year}'


# --------------------------------------------------------------------------------------------
# Contexte : mode et confirmations
# --------------------------------------------------------------------------------------------

def charger_confirmations(chemin: Path) -> dict:
    """Lit confirmations.json sans en imposer la forme : {"C06": true}, {"C06": {"confirme": true}},
    ou {"confirmations": {...}}. Toute autre clé est ignorée."""
    if not chemin.exists():
        return {}
    d = json.loads(chemin.read_text(encoding='utf-8'))
    if isinstance(d, dict) and isinstance(d.get('confirmations'), dict):
        d = d['confirmations']
    res = {}
    for k, v in (d.items() if isinstance(d, dict) else []):
        if not re.fullmatch(r'C\d\d', str(k)):
            continue
        if isinstance(v, bool):
            res[k] = v
        elif isinstance(v, dict):
            res[k] = bool(v.get('confirme', v.get('confirmé', v.get('valide', v.get('ok', False)))))
        elif isinstance(v, str):
            res[k] = v.strip().lower() in ('oui', 'confirme', 'confirmé', 'ok', 'true', 'valide')
    return res


class Ctx:
    def __init__(self, mode: str, conf: dict, valeurs: dict, date: dt.date):
        self.mode, self.conf, self.v, self.date = mode, conf, valeurs, date

    @property
    def preview(self) -> bool:
        return self.mode == 'preview'

    def confirme(self, *codes) -> bool:
        return all(self.conf.get(c, False) for c in codes)

    def ok(self, *codes) -> bool:
        """Texte définitif ? (preview : toujours ; production : seulement si tout est confirmé)."""
        return self.preview or self.confirme(*codes)

    def tag(self, *codes) -> str:
        manquants = [c for c in codes if not self.conf.get(c, False)]
        if not self.preview or not manquants:
            return ''
        return ('<font name="Mont-600" size="6.5" color="#C4000D"><super>' + NB
                + ' '.join(manquants) + '</super></font>')

    def manque(self, libelle: str) -> str:
        """Emplacement d'une valeur que le client doit fournir (preview seulement)."""
        return f'<font name="Sans-It" color="#44494F">[{e(libelle)}]</font>'

    @property
    def edition(self) -> str:
        return f'{MOIS[self.date.month - 1]} {self.date.year}'


# --------------------------------------------------------------------------------------------
# Images
# --------------------------------------------------------------------------------------------

class Images:
    def __init__(self, cache: Path):
        self.cache = cache

    def photo(self, ident, largeur_mm, hauteur_mm, focus=(0.5, 0.5), dpi=230, qualite=80) -> str:
        """Recadre une photo du portfolio au format voulu et l'enregistre en JPEG (inclus tel quel)."""
        src = IMG / 'portfolio' / f'{ident}-1600.webp'
        im = Image.open(src).convert('RGB')
        sw, sh = im.size
        ratio = largeur_mm / hauteur_mm
        if sw / sh > ratio:
            cw, ch = round(sh * ratio), sh
        else:
            cw, ch = sw, round(sw / ratio)
        x0 = min(max(round(focus[0] * sw - cw / 2), 0), sw - cw)
        y0 = min(max(round(focus[1] * sh - ch / 2), 0), sh - ch)
        im = im.crop((x0, y0, x0 + cw, y0 + ch))
        cible = (round(largeur_mm / 25.4 * dpi), round(hauteur_mm / 25.4 * dpi))
        if cible[0] < cw:
            im = im.resize(cible, Image.LANCZOS)
        nom = self.cache / f'{ident}-{round(largeur_mm)}x{round(hauteur_mm)}-{dpi}.jpg'
        im.save(nom, 'JPEG', quality=qualite, optimize=True, progressive=False, subsampling='4:2:0')
        return str(nom)


def dessiner_logo(c, fichier: Path, x, y, hmax, wmax):
    """Logo graphite (SVG vectoriel ou PNG transparent), centré dans la case (x, y, wmax, hmax)."""
    if fichier.suffix == '.svg':
        from svglib.svglib import svg2rlg
        d = svg2rlg(str(fichier))
        s = min(hmax / d.height, wmax / d.width)
        w, h = d.width * s, d.height * s
        d.width, d.height = w, h
        d.scale(s, s)
        renderPDF.draw(d, c, x + (wmax - w) / 2, y + (hmax - h) / 2)
    else:
        iw, ih = Image.open(fichier).size
        s = min(hmax / ih, wmax / iw)
        w, h = iw * s, ih * s
        c.drawImage(str(fichier), x + (wmax - w) / 2, y + (hmax - h) / 2, w, h, mask='auto')


# --------------------------------------------------------------------------------------------
# Document : page, en-tête, pied, blocs de texte
# --------------------------------------------------------------------------------------------

class Doc:
    def __init__(self, chemin: Path, ctx: Ctx, titre, sujet, mots, entete_droite, pied_gauche, total):
        chemin.parent.mkdir(parents=True, exist_ok=True)
        self.chemin = chemin
        self.c = canvas.Canvas(str(chemin), pagesize=A4, pageCompression=1, initialFontName='Sans',
                               initialFontSize=12)
        self.c.setTitle(titre)
        self.c.setAuthor('Andy Construct')
        self.c.setSubject(sujet)
        self.c.setKeywords(mots)
        self.c.setCreator('Andy Construct, Chanton & Cie, Carouge')
        self.ctx, self.entete_droite, self.pied_gauche, self.total = ctx, entete_droite, pied_gauche, total
        self.no = 0
        self.y = H
        self.bas = BAS

    # -- page
    def debut(self, entete=True):
        self.no += 1
        if self.ctx.preview:
            self.bande_validation()
        if entete:
            y = H - 15 * mm
            self.lettres('ANDY CONSTRUCT', ML, y, 'Mont-600', 7.5, GRAPH, 0.18)
            self.lettres(self.entete_droite.upper(), W - MR, y, 'Mont-600', 7.5, GRAPH, 0.18, droite=True)
            self.biseau(ML - 0.2 * mm, y + 4.2 * mm, 6 * mm, 1.3 * mm)
            self.filet(ML, W - MR, H - 18 * mm)
        self.y = H - 28 * mm

    def fin(self, pied=True):
        if pied:
            self.filet(ML, W - MR, 15.5 * mm)
            st = S('pied', 'Sans', 9, 11, GRAPH)
            p = Paragraph(fr(self.pied_gauche), st)
            _, h = p.wrap(CW - 25 * mm, 50 * mm)
            p.drawOn(self.c, ML, 13 * mm - h)
            self.c.setFont('Mont-600', 9)
            self.c.setFillColor(GRAPH)
            self.c.drawRightString(W - MR, 13 * mm - 9, f'{self.no} / {self.total}')
        self.c.showPage()

    def bande_validation(self):
        c = self.c
        c.setFillColor(BRUME)
        c.rect(0, H - 7.5 * mm, W, 7.5 * mm, stroke=0, fill=1)
        c.setFillColor(ROUGE)
        c.rect(0, H - 7.5 * mm, 2.5 * mm, 7.5 * mm, stroke=0, fill=1)
        txt = ('VERSION DE VALIDATION · NE PAS DIFFUSER · les codes C01 à C44 signalent un point à confirmer'
               ' · logos soumis à l\'accord écrit des maîtres d\'ouvrage')
        self.lettres(txt, W / 2, H - 4.9 * mm, 'Mont-600', 6.3, ROUGE_F, 0.06, centre=True)

    # -- primitives
    def lettres(self, txt, x, y, police, taille, couleur, espacement_em, droite=False, centre=False):
        c = self.c
        cs = espacement_em * taille
        larg = pdfmetrics.stringWidth(txt, police, taille) + cs * (len(txt) - 1)
        if droite:
            x -= larg
        elif centre:
            x -= larg / 2
        c.saveState()             # l'espacement (Tc) ne doit pas déborder sur les textes suivants
        t = c.beginText(x, y)
        t.setFont(police, taille)
        t.setCharSpace(cs)
        t.setFillColor(couleur)
        t.textOut(txt)
        c.drawText(t)
        c.restoreState()
        return larg

    def biseau(self, x, y, w=7.2 * mm, h=1.7 * mm, couleur=ROUGE):
        """Trait oblique rouge du logo (parallélogramme incliné à -20°)."""
        off = h * math.tan(math.radians(20))
        p = self.c.beginPath()
        p.moveTo(x, y)
        p.lineTo(x + w, y)
        p.lineTo(x + w + off, y + h)
        p.lineTo(x + off, y + h)
        p.close()
        self.c.setFillColor(couleur)
        self.c.drawPath(p, stroke=0, fill=1)

    def filet(self, x1, x2, y, couleur=TRAIT, ep=0.75):
        self.c.setStrokeColor(couleur)
        self.c.setLineWidth(ep)
        self.c.line(x1, y, x2, y)

    def surtitre(self, txt, x=ML, couleur=GRAPH, taille=8.8):
        """Surtitre de section : biseau rouge + capitales espacées (Montserrat 600, 0,18 em)."""
        y = self.y - taille
        self.biseau(x, y + 0.6, 7.2 * mm, 1.7 * mm)
        self.lettres(txt.upper(), x + 10.5 * mm, y, 'Mont-600', taille, couleur, 0.18)
        self.y = y - 4 * mm

    def espace(self, v):
        self.y -= v

    def para(self, texte, style, x=ML, largeur=CW, y=None, avancer=True, verifier=True):
        y = self.y if y is None else y
        p = Paragraph(fr(texte), style)
        _, h = p.wrap(largeur, 2000)
        if verifier and y - h < self.bas - 0.5:
            debordement(f'{self.chemin.name}, page {self.no} : « {texte[:60]} » déborde de {(self.bas - (y - h)) / mm:.1f} mm')
        p.drawOn(self.c, x, y - h)
        if avancer:
            self.y = y - h
        return h

    def hauteur(self, texte, style, largeur=CW):
        p = Paragraph(fr(texte), style)
        return p.wrap(largeur, 2000)[1]

    def lien(self, url, x, y, w, h):
        self.c.linkURL(url, (x, y, x + w, y + h), relative=0, thickness=0)

    def controle(self, marge_mm=0):
        if self.y < self.bas - 0.5:
            debordement(f'{self.chemin.name}, page {self.no} : contenu sous la marge ({(self.bas - self.y) / mm:.1f} mm)')

    def save(self):
        self.c.save()


# Styles communs
ST = {}


def styles():
    ST.update({
        'h1': S('h1', 'Mont-700', 27, 32),
        'h1c': S('h1c', 'Mont-700', 24, 29),
        'h2': S('h2', 'Mont-700', 17, 21),
        'h3': S('h3', 'Mont-600', 13, 17),
        'corps': S('corps', 'Sans', 12.5, 18),
        'corps_g': S('corps_g', 'Sans', 12.5, 18, GRAPH),
        'corps12': S('corps12', 'Sans', 12, 16.5),
        'corps12_g': S('corps12_g', 'Sans', 12, 16.5, GRAPH),
        'lead': S('lead', 'Sans', 14, 20.5),
        'guide': S('guide', 'Sans', 13, 19),
        'guide_g': S('guide_g', 'Sans', 13, 19, GRAPH),
        'petit': S('petit', 'Sans', 10, 13, GRAPH),
        'leg': S('leg', 'Sans', 9.5, 12, GRAPH),
        'nom': S('nom', 'Sans-600', 11.5, 13.5, GRAPH, TA_CENTER),
        'label': S('label', 'Sans-600', 12, 16.5, GRAPH),
        'schema': S('schema', 'Sans', 9.5, 11.5, GRAPH),
        'schema_c': S('schema_c', 'Sans', 9.5, 11.5, GRAPH, TA_CENTER),
    })


# --------------------------------------------------------------------------------------------
# Plaquette de références (copy-deck §Q.1)
# --------------------------------------------------------------------------------------------

SECTEURS = [
    ('Collectivités et institutions', [
        ('ville-de-geneve', 'Ville de Genève'),
        ('plan-les-ouates', 'Mairie de Plan-les-Ouates'),
        ('collonge-bellerive', 'Salle communale de Collonge-Bellerive'),
        ('omc', 'OMC'),
    ]),
    ('Culture et formation', [
        ('conservatoire-musique-geneve', 'Conservatoire de musique de Genève'),
        ('head-geneve', 'HEAD – Genève'),
        ('alhambra', "Salle de l'Alhambra"),
        ('harmonie-nautique', 'Harmonie Nautique de Genève'),
    ]),
    ('Entreprises', [
        ('piaget', 'Piaget'),
        ('ubs', 'UBS'),
        ('j-safra-sarasin', 'J. Safra Sarasin (anciennement Bank Sarasin)'),
        ('de-grisogono', 'de Grisogono'),
        ('celgene', 'Celgene'),
        ('labcorp', 'Labcorp (anciennement Covance), Meyrin'),
        ('dipan', 'Dipan, Nyon'),
        ('energestion', 'Energestion, ingénieurs-conseils, Les Acacias'),
    ]),
    ('Hôtellerie et domaines', [
        ('everness', 'Everness Hotel & Resort, Chavannes-de-Bogis'),
        ('domaine-des-perrieres', 'Domaine des Perrières, Coppet'),
    ]),
]
# Marque rachetée par un tiers qui n'a jamais été client : nom en texte seulement (logos-references.md).
TEXTE_SEUL = {'de-grisogono'}


def references_affichees(ctx: Ctx, logos: dict):
    """Liste par secteur : (id, nom affiché, codes à confirmer, fichier logo ou None)."""
    res = []
    for secteur, items in SECTEURS:
        lignes = []
        for ident, nom in items:
            codes = []
            if ident == 'omc':
                codes = ['C22']
                if not ctx.ok('C22'):
                    continue                       # repli : nom retiré (D4)
            if ident == 'everness':
                codes = ['C22']
                if not ctx.ok('C22'):
                    nom = 'Hôtel à Chavannes-de-Bogis'
            info = logos.get(ident, {})
            fichier = None
            statut = info.get('statut')
            definitif = not (ident == 'everness' and not ctx.ok('C22'))
            if info.get('fichier') and ident not in TEXTE_SEUL and definitif:
                if statut == 'autorise' or (ctx.preview and statut == 'a_autoriser'):
                    fichier = IMG / 'references' / info['fichier']
            lignes.append((ident, nom, codes, fichier, info.get('echelle', 1.0)))
        res.append((secteur, lignes))
    return res


def detail_reference(ctx: Ctx, ident) -> str:
    r = (ctx.v.get('references') or {}).get(ident) or {}
    if r.get('annee') and r.get('travaux') and ctx.ok('C22'):
        return f'{e(r["annee"])} · {e(r["travaux"])}'
    return ''


def plaquette(ctx: Ctx, chemin: Path, logos: dict, imgs: Images):
    # Points de la méthode en site occupé (copy-deck §H.3) et codes de confirmation de chacun.
    points = [
        ("Un avis aux locataires ou aux usagers, préparé avec vous et affiché quelques jours avant.", ['C20']),
        ("Des horaires de travail convenus, communiqués aux habitants.", ['C20']),
        ("Parties communes, ascenseur et sols protégés avant le premier jour.", ['C20', 'C07']),
        ("La poussière contenue : zone fermée par des bâches, aspiration.", ['C20', 'C07']),
        ("Un responsable de chantier nommé, joignable pendant toute la durée des travaux.", ['C20', 'C09']),
        ("Nettoyage chaque soir, passages libres pour les habitants.", ['C20', 'C07']),
        ("Un imprévu ? Nous le signalons avec son prix, avant de l'exécuter.", ['C20', 'C06']),
        ("Réception avec photos et liste des retouches, levées dans le délai convenu.", ['C20', 'C32']),
    ]
    points = [(t, c) for t, c in points if ctx.ok(*c)]
    offre_ok = ctx.ok('C06', 'C28')

    pages = [p_couverture, p_qui, p_references]
    if points or offre_ok:
        pages.append(lambda d: p_site_occupe(d, points, offre_ok))
    pages += [p_lots, p_contact]

    titre = 'Andy Construct · Dossier de références' + (' (version de validation)' if ctx.preview else '')
    d = Doc(chemin, ctx, titre,
            'Plâtrerie, faux-plafonds, peinture et isolation intérieure en Suisse romande : identité, références, méthode, lots CFC, contacts.',
            'Andy Construct, plâtrerie, placo, faux-plafonds, peinture, isolation acoustique, cloisons, Carouge, Genève, Suisse romande, références',
            'Dossier de références', '+41 22 771 20 15 · www.andyconstruct.ch', len(pages))
    d.imgs = imgs
    d.logos = logos
    for p in pages:
        p(d)
    d.save()
    return len(pages)


def p_couverture(d: Doc):
    c, ctx = d.c, d.ctx
    d.debut(entete=False)
    # Logo, version pour fond clair
    lw = 62 * mm
    lh = lw * 232 / 640
    c.drawImage(str(IMG / 'brand' / 'logo-andy-construct.png'), ML - 1.5 * mm, H - 16 * mm - lh, lw, lh, mask='auto')
    # Photo forte : faux-plafond en plaques de plâtre à gorge lumineuse (architecture-cro §8.4 n° 6, « M »)
    haut, bas = H - 50 * mm, H - 50 * mm - 148 * mm
    ph = d.imgs.photo('faux-plafond-placo-gorge-lumineuse-01', 210, 148, focus=(0.55, 0.45), dpi=200, qualite=78)
    c.saveState()
    p = c.beginPath()
    p.moveTo(0, haut)
    p.lineTo(W, haut)
    p.lineTo(W, bas + 24 * mm)
    p.lineTo(W - 13 * mm, bas)
    p.lineTo(0, bas)
    p.close()
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(ph, 0, bas, W, haut - bas)
    c.restoreState()
    # Titre
    d.y = bas - 15 * mm
    d.surtitre('Andy Construct')
    d.espace(1 * mm)
    d.para('Dossier de références', S('t', 'Mont-700', 38, 42))
    d.espace(4 * mm)
    d.para('Plâtrerie, faux-plafonds, peinture et isolation intérieure · Suisse' + NB + 'romande',
           S('st', 'Sans', 16, 21, GRAPH), largeur=150 * mm)
    # Bas de page
    d.filet(ML, W - MR, 27 * mm)
    st = S('cb', 'Sans', 11.5, 15, GRAPH)
    d.para('Carouge · inscrite au registre du commerce depuis 2007', st, y=23 * mm, verifier=False)
    d.para(f'Édition {ctx.edition}', S('cb2', 'Sans', 11.5, 15, GRAPH, TA_RIGHT), y=23 * mm, verifier=False)
    d.fin(pied=False)


def p_qui(d: Doc):
    ctx = d.ctx
    d.debut()
    d.surtitre('Qui nous sommes')
    d.para('En bref', ST['h2'])
    d.espace(3 * mm)
    d.para("Andy Construct est une entreprise genevoise de plâtrerie, de peinture et d'isolation intérieure, "
           "basée à Carouge. Elle pose des cloisons, des doublages et des faux-plafonds en plaques de plâtre, "
           "isole contre le bruit et contre le froid, et peint murs et plafonds. Elle travaille pour des communes, "
           "des institutions, des régies, des architectes, des entreprises et des particuliers, dans toute la "
           "Suisse romande.", ST['lead'], largeur=160 * mm)
    d.espace(7 * mm)

    # Identité (tableau)
    d.para('Identité', ST['h2'])
    d.espace(3 * mm)
    lignes = [
        ('Raison sociale', 'Andy Construct, Chanton &amp; Cie (société en nom collectif)'),
        ('IDE', 'CHE-113.706.162 · registre du commerce du canton de Genève'),
        ('Activité', 'depuis le 1<super>er</super> juin 2007'),
        ('Siège', 'Route des Acacias 48, 1227 Carouge'),
    ]
    if ctx.ok('C10'):
        lignes.append(('Associés', 'Adnan Bajrami, Caroline Chanton Bajrami' + ctx.tag('C10')))
    eff = ctx.v.get('effectif')
    if ctx.preview or (ctx.confirme('C24') and eff):
        n = e(eff) if eff else ctx.manque('nombre')
        lignes.append(('Effectif', f'{n} personnes' + ctx.tag('C24')))
    if ctx.ok('C11'):
        lignes.append(('Association professionnelle', 'membre du GGE' + ctx.tag('C11')))
    if ctx.ok('C12'):
        lignes.append(('Assurance responsabilité civile', 'attestation sur demande' + ctx.tag('C12')))
    if ctx.ok('C13'):
        lignes.append(('Attestations AVS, LPP, impôts, convention collective', 'sur demande' + ctx.tag('C13')))
    lab_w = 66 * mm
    pad = 1.9 * mm
    d.filet(ML, W - MR, d.y)
    for lab, val in lignes:
        y0 = d.y - pad
        h1 = d.para(lab, ST['label'], x=ML, largeur=lab_w - 4 * mm, y=y0, avancer=False)
        h2 = d.para(val, ST['corps12'], x=ML + lab_w, largeur=CW - lab_w, y=y0, avancer=False)
        d.y = y0 - max(h1, h2) - pad
        d.filet(ML, W - MR, d.y)
    d.espace(8 * mm)

    # Quatre métiers (grille 2 × 2)
    d.para('Quatre métiers', ST['h2'])
    d.espace(3 * mm)
    acou = 'doublages et faux-plafonds acoustiques' + (', correction de l\'écho des salles' + ctx.tag('C18') if ctx.ok('C18') else '')
    metiers = [
        ('Placo', 'cloisons, doublages, faux-plafonds, caissons'),
        ('Peinture intérieure', 'logements, fins de bail, cages d\'escalier, bureaux'),
        ('Isolation acoustique', acou),
        (('Cloisons isolantes' + ctx.tag('C16')) if ctx.ok('C16') else 'Cloisons isothermes',
         'séparation des locaux chauffés et non chauffés, plafonds de caves et de garages'),
    ]
    gout = 10 * mm
    cw2 = (CW - gout) / 2
    for k in (0, 2):
        y0 = d.y
        bas = y0
        for j in (0, 1):
            nom, desc = metiers[k + j]
            x = ML + j * (cw2 + gout)
            d.filet(x, x + cw2, y0, ANTH, 0.9)
            d.c.setFont('Mont-700', 11)
            d.c.setFillColor(ROUGE_F)
            d.c.drawString(x, y0 - 2.4 * mm - 11.5, f'0{k + j + 1}')
            h = d.para(f'<font name="Sans-600">{nom}</font> : {desc}', ST['corps12'], x=x + 9 * mm,
                       largeur=cw2 - 9 * mm, y=y0 - 2.4 * mm, avancer=False)
            bas = min(bas, y0 - 2.4 * mm - h)
        d.y = bas - 3.5 * mm
    d.espace(2 * mm)
    # Zone (la carte est en dernière page, à côté des contacts)
    y0 = d.y
    h1 = d.para('Zone', ST['h2'], largeur=40 * mm, avancer=False)
    h2 = d.para('Toute la Suisse romande, depuis Carouge.', ST['lead'], x=ML + 32 * mm, largeur=CW - 32 * mm,
                y=y0 - 0.6 * mm, avancer=False)
    d.y = y0 - max(h1, h2)
    d.controle()
    d.fin()


def carte_romandie(d: Doc, x, y_haut, largeur):
    """Carte de la Suisse romande à partir des données du site (tools/build/carte.py, lecture seule)."""
    try:
        sys.path.insert(0, str(RACINE / 'tools' / 'build'))
        import carte  # noqa: E402
        obj = carte.charger(eps=1.2)
    except Exception as exc:  # carte facultative
        print('carte non dessinée :', exc)
        return 0
    finally:
        if sys.path and sys.path[0] == str(RACINE / 'tools' / 'build'):
            sys.path.pop(0)
    s = largeur / carte.W
    hauteur = carte.H * s
    c = d.c

    def tracer(chemin_d):
        p = c.beginPath()
        cx = cy = 0.0
        for cmd, args in re.findall(r'([MlLz])([^MlLz]*)', chemin_d):
            nums = [float(n) for n in re.findall(r'-?\d+(?:\.\d+)?', args)]
            if cmd == 'M':
                cx, cy = nums[0], nums[1]
                p.moveTo(x + cx * s, y_haut - cy * s)
            elif cmd == 'l':
                for i in range(0, len(nums) - 1, 2):
                    cx += nums[i]
                    cy += nums[i + 1]
                    p.lineTo(x + cx * s, y_haut - cy * s)
            elif cmd == 'z':
                p.close()
        return p

    c.saveState()
    clip = c.beginPath()
    clip.rect(x, y_haut - hauteur, largeur, hauteur)
    c.clipPath(clip, stroke=0, fill=0)
    c.setLineJoin(1)
    c.setStrokeColor(white)
    c.setLineWidth(0.5)
    c.setFillColor(BRUME)
    for cid, chem in obj['cantons'].items():
        if cid not in carte.ROMANDS:
            c.drawPath(tracer(chem), stroke=1, fill=1)
    c.setFillColor(GRIS_M)
    for chem in obj['districts'].values():
        c.drawPath(tracer(chem), stroke=1, fill=1)
    for cid in carte.ROMANDS:
        c.drawPath(tracer(obj['cantons'][cid]), stroke=1, fill=1)
    c.setFillColor(white)
    c.setLineWidth(0.3)
    for chem in obj['lakes'].values():
        c.drawPath(tracer(chem), stroke=0, fill=1)
    c.setStrokeColor(GRAPH)
    c.setLineWidth(0.6)
    c.drawPath(tracer(obj['country']['CH']), stroke=1, fill=0)
    c.restoreState()
    c.setStrokeColor(TRAIT)
    c.setLineWidth(0.5)
    c.rect(x, y_haut - hauteur, largeur, hauteur, stroke=1, fill=0)
    # Siège
    px, py = carte.proj(*carte.SIEGE[1:])
    X, Y = x + px * s, y_haut - py * s
    c.setFillColor(ROUGE)
    c.setStrokeColor(white)
    c.setLineWidth(1)
    c.circle(X, Y, 1.6 * mm, stroke=1, fill=1)
    c.setFillColor(ANTH)
    c.setFont('Sans-600', 9.5)
    c.drawString(X + 2.6 * mm, Y - 1.2 * mm, 'Carouge')
    for nom, lon, lat, cote in carte.VILLES:
        if nom not in ('Lausanne', 'Neuchâtel', 'Fribourg', 'Sion', 'Delémont'):
            continue
        px, py = carte.proj(lon, lat)
        X, Y = x + px * s, y_haut - py * s
        c.setFillColor(GRAPH)
        c.circle(X, Y, 0.7 * mm, stroke=0, fill=1)
        c.setFont('Sans', 8.5)
        if cote > 0:
            c.drawString(X + 1.6 * mm, Y - 1 * mm, nom)
        else:
            c.drawRightString(X - 1.6 * mm, Y - 1 * mm, nom)
    return hauteur


def p_references(d: Doc):
    ctx = d.ctx
    d.debut()
    d.surtitre('Références')
    d.para('Ils nous ont confié des travaux' + ctx.tag('C22'), ST['h1c'])
    d.espace(5.5 * mm)
    secteurs = references_affichees(ctx, d.logos)
    avec_logos = any(f for _, l in secteurs for (_, _, _, f, _) in l)
    if avec_logos:
        refs_tuiles(d, secteurs)
    else:
        refs_liste(d, secteurs)

    # Trois chantiers (textes du §G.3 ; production : textes de repli, C25)
    d.espace(6 * mm)
    d.para('Trois chantiers', ST['h2'])
    d.espace(3.5 * mm)
    projets = [
        dict(photo='faux-plafond-placo-gorge-lumineuse-02', focus=(0.5, 0.45),
             titre='Hall et couloirs : faux-plafond à gorge lumineuse',
             lieu=('Immeuble, canton de Genève' + ctx.tag('C25')) if ctx.ok('C25') else "Hall d'immeuble",
             contrainte='Formes courbes, éclairage et spots intégrés au plafond.',
             presta=('Placo · Peinture' + ctx.tag('C25')) if ctx.ok('C25') else 'Placo', badge=False),
        dict(photo='chantier-ossature-puits-de-lumiere-02', focus=(0.5, 0.33),
             titre='Grande salle : ossature et isolant avant la fermeture',
             lieu=('Salle publique, canton de Genève' + ctx.tag('C25')) if ctx.ok('C25') else 'Salle publique',
             contrainte='Travail en hauteur, autour de puits de lumière.',
             presta='Placo' + ctx.tag('C25'), badge=True),
        dict(photo='habillage-placo-niches-arrondies-01', focus=(0.55, 0.5),
             titre="Cage d'escalier : habillage à niches arrondies",
             lieu='Immeuble' + ctx.tag('C25'),
             contrainte='Formes arrondies, escalier protégé pendant les travaux.',
             presta='Placo', badge=True),
    ]
    gout = 6 * mm
    cw3 = (CW - 2 * gout) / 3
    ph_h = cw3 * (0.58 if ctx.preview else 0.7)
    y0 = d.y
    bas_max = y0
    for i, pj in enumerate(projets):
        x = ML + i * (cw3 + gout)
        f = d.imgs.photo(pj['photo'], cw3 / mm, ph_h / mm, focus=pj['focus'], dpi=260)
        d.c.drawImage(f, x, y0 - ph_h, cw3, ph_h)
        if pj['badge']:
            lab = 'PENDANT LES TRAVAUX'
            tw = pdfmetrics.stringWidth(lab, 'Mont-600', 6.8) + 0.1 * 6.8 * (len(lab) - 1)
            d.c.setFillColor(ANTH)
            d.c.rect(x, y0 - 6.2 * mm, tw + 5 * mm, 6.2 * mm, stroke=0, fill=1)
            d.lettres(lab, x + 2.5 * mm, y0 - 4.1 * mm, 'Mont-600', 6.8, white, 0.1)
        yy = y0 - ph_h - 3 * mm
        yy -= d.para(pj['titre'], S('pt', 'Mont-600', 12, 14.5), x=x, largeur=cw3, y=yy, avancer=False) + 1.6 * mm
        yy -= d.para(pj['lieu'], ST['corps12_g'], x=x, largeur=cw3, y=yy, avancer=False) + 0.6 * mm
        yy -= d.para(pj['contrainte'], ST['corps12'], x=x, largeur=cw3, y=yy, avancer=False) + 0.6 * mm
        yy -= d.para(f'<font name="Sans-600" color="#C4000D">{pj["presta"]}</font>', ST['corps12'], x=x, largeur=cw3, y=yy, avancer=False)
        bas_max = min(bas_max, yy)
    d.y = bas_max
    if ctx.ok('C22'):
        d.espace(4 * mm)
        d.filet(ML, W - MR, d.y)
        d.espace(2 * mm)
        d.para('Références citées avec l\'accord des maîtres d\'ouvrage. Contacts de référence sur demande.' + ctx.tag('C22'),
               ST['corps12_g'])
    d.controle()
    d.fin()


def refs_liste(d: Doc, secteurs):
    """Production : noms en texte, par secteur, sur deux colonnes."""
    gout = 10 * mm
    cw2 = (CW - gout) / 2
    colonnes = [secteurs[:2], secteurs[2:]]
    y0 = d.y
    bas = y0
    for k, col in enumerate(colonnes):
        x = ML + k * (cw2 + gout)
        d.y = y0
        for j, (secteur, lignes) in enumerate(col):
            if j:
                d.espace(6 * mm)
            d.lettres(secteur.upper(), x, d.y - 8.5, 'Mont-600', 8.5, GRAPH, 0.16)
            d.y -= 8.5 + 2.8 * mm
            d.filet(x, x + cw2, d.y, ANTH, 0.9)
            for ident, nom, codes, _, _ in lignes:
                d.espace(1.9 * mm)
                det = detail_reference(d.ctx, ident)
                d.para(e(nom) + d.ctx.tag(*codes), ST['corps12'], x=x, largeur=cw2)
                if det:
                    d.para(det, ST['petit'], x=x, largeur=cw2)
                d.espace(1.9 * mm)
                d.filet(x, x + cw2, d.y)
        bas = min(bas, d.y)
    d.y = bas


def refs_tuiles(d: Doc, secteurs):
    """Preview : logos graphite (a_autoriser) ou nom typographique (armoiries, emblèmes), par secteur."""
    n = 4
    gout = 3.5 * mm
    tw = (CW - (n - 1) * gout) / n
    th = 14.5 * mm
    c = d.c
    for j, (secteur, lignes) in enumerate(secteurs):
        if j:
            d.espace(3.5 * mm)
        d.lettres(secteur.upper(), ML, d.y - 8.5, 'Mont-600', 8.5, GRAPH, 0.16)
        d.y -= 8.5 + 2.3 * mm
        for i, (ident, nom, codes, fichier, echelle) in enumerate(lignes):
            col = i % n
            if col == 0 and i:
                d.y -= th + gout
            x = ML + col * (tw + gout)
            y = d.y - th
            c.setStrokeColor(TRAIT)
            c.setLineWidth(0.75)
            c.setFillColor(white)
            c.roundRect(x, y, tw, th, 0.8 * mm, stroke=1, fill=1)
            if fichier:
                hmax = min(7.8 * mm * echelle, th - 4.5 * mm)
                dessiner_logo(c, fichier, x + 3 * mm, y + (th - hmax) / 2, hmax, tw - 6 * mm)
                if codes:
                    d.para(d.ctx.tag(*codes), S('tg', 'Sans', 8, 9), x=x + tw - 9 * mm, largeur=9 * mm, y=y + th - 0.5 * mm, avancer=False, verifier=False)
            else:
                st = ST['nom']
                txt = e(nom) + d.ctx.tag(*codes)
                hh = d.hauteur(txt, st, tw - 4 * mm)
                d.para(txt, st, x=x + 2 * mm, largeur=tw - 4 * mm, y=y + (th + hh) / 2, avancer=False)
        d.y -= th
        d.controle()


def p_site_occupe(d: Doc, points, offre_ok):
    ctx = d.ctx
    d.debut()
    d.surtitre('Immeubles habités et lieux publics')
    if points:
        d.para('Travailler dans un bâtiment habité ou ouvert au public', ST['h1c'], largeur=150 * mm)
        d.espace(5 * mm)
        d.para("Les plaintes et les retards naissent presque toujours d'un manque d'organisation. "
               "Voici ce que nous faisons à chaque chantier.", ST['lead'], largeur=150 * mm)
        d.espace(8 * mm)
        gout = 10 * mm
        cw2 = (CW - gout) / 2
        lignes = [points[i:i + 2] for i in range(0, len(points), 2)]
        for k, ligne in enumerate(lignes):
            y0 = d.y
            bas = y0
            for j, (txt, codes) in enumerate(ligne):
                x = ML + j * (cw2 + gout)
                d.filet(x, x + cw2, y0, ANTH, 0.9)
                no = 2 * k + j + 1
                d.c.setFont('Mont-700', 20)
                d.c.setFillColor(ANTH)
                d.c.drawString(x, y0 - 3.5 * mm - 17, f'{no:02d}')
                h = d.para(txt + ctx.tag(*codes), ST['corps'], x=x + 15 * mm, largeur=cw2 - 15 * mm, y=y0 - 3.5 * mm, avancer=False)
                bas = min(bas, y0 - 3.5 * mm - max(h, 9 * mm))
            d.y = bas - 5 * mm
    if offre_ok:
        d.espace(3 * mm)
        items = ['les postes et les quantités ;', 'les prix unitaires et le total en CHF, TVA indiquée ;',
                 'la durée des travaux et les dates possibles ;', 'ce qui n\'est pas compris ;',
                 'les conditions de paiement ;', 'la durée de validité de l\'offre.']
        puce = '<font name="Mont-700" color="#C4000D">›</font>' + NB + NB
        encadre(d, [('Ce que contient notre offre' + ctx.tag('C06', 'C28'), ST['h2'], 3 * mm)]
                + [(puce + t, ST['corps'], 1 * mm) for t in items[:-1]] + [(puce + items[-1], ST['corps'], 0)],
                pad=6 * mm, largeur=CW)
    d.controle()
    d.fin()


def p_lots(d: Doc):
    ctx = d.ctx
    d.debut()
    d.surtitre('Lots et normes')
    titre = ('Quatre métiers, trois lots' + ctx.tag('C14')) if ctx.ok('C14') else 'Lots et normes'
    d.para(titre, ST['h1c'])
    d.espace(7 * mm)
    lots = [('CFC 271 Plâtrerie', 'cloisons, doublages, caissons, isolation intégrée (thermique et acoustique)')]
    if ctx.ok('C14'):
        lots.append(('CFC 283 Faux-plafonds', 'plafonds en plaques de plâtre, acoustiques, gorges lumineuses, trappes de visite' + ctx.tag('C14')))
        lots.append(('CFC 285 Traitement des surfaces intérieures', 'peinture des murs, plafonds et cages d\'escalier'))
    else:
        lots.append(('CFC 285 Peinture', 'peinture des murs, plafonds et cages d\'escalier'))
    lab_w = 70 * mm
    d.filet(ML, W - MR, d.y, ANTH, 0.9)
    for lab, val in lots:
        y0 = d.y - 3.2 * mm
        h1 = d.para(lab, S('lot', 'Mont-600', 12.5, 16.5), x=ML, largeur=lab_w - 5 * mm, y=y0, avancer=False)
        h2 = d.para(val, ST['corps'], x=ML + lab_w, largeur=CW - lab_w, y=y0, avancer=False)
        d.y = y0 - max(h1, h2) - 3.2 * mm
        d.filet(ML, W - MR, d.y)
    d.espace(11 * mm)
    d.para('Normes', ST['h2'])
    d.espace(3 * mm)
    if ctx.ok('C15', 'C33'):
        txt = ('Exécution selon la norme SIA 118 lorsque le contrat s\'y réfère. Isolation acoustique et thermique '
               'selon les exigences du projet (SIA 181, SIA 180). Protection incendie selon les prescriptions AEAI '
               'lorsque le projet l\'exige.' + ctx.tag('C15', 'C33'))
    else:
        txt = 'Les performances visées sont celles du projet, précisées dans l\'offre.'
    d.para(txt, ST['corps'], largeur=150 * mm)
    d.espace(4 * mm)
    d.para('Nous ne promettons pas de performance chiffrée sans mesure : elle est fixée par le projet, '
           'et nous posons un système qui y répond.', ST['corps'], largeur=150 * mm)
    # Photo de chantier (architecture-cro §8.4 n° 29, « M ») : occupe la place restante
    d.espace(11 * mm)
    ph_h = min(112 * mm, d.y - d.bas - 9 * mm)
    f = d.imgs.photo('chantier-suspentes-ossature-01', CW / mm, ph_h / mm, focus=(0.5, 0.55), dpi=210)
    d.c.drawImage(f, ML, d.y - ph_h, CW, ph_h)
    d.y -= ph_h + 2.5 * mm
    d.para("Pendant les travaux : suspentes et ossature d'un faux-plafond, sous une dalle isolée", ST['leg'])
    d.controle()
    d.fin()


def p_contact(d: Doc):
    ctx, c = d.ctx, d.c
    d.debut()
    d.surtitre('Contact')
    d.para('Nous consulter', ST['h1c'])
    d.espace(7 * mm)
    inter = [i for i in (ctx.v.get('interlocuteurs') or []) if i and i.get('nom')]
    if ctx.preview or (ctx.confirme('C09', 'C38') and inter):
        if not inter:
            inter = [None]
        for i in inter:
            if i:
                t = f'{e(i["nom"])}, {e(i.get("role") or "")} · {e(i.get("email") or "")} · {e(i.get("mobile") or "")}'
            else:
                t = f'{ctx.manque("Prénom Nom")}, {ctx.manque("rôle")} · {ctx.manque("e-mail direct")} · {ctx.manque("mobile")}'
            d.para(t + ctx.tag('C09', 'C38'), ST['corps'])
            d.espace(2 * mm)
        d.espace(3 * mm)
    # Coordonnées générales (C30 : e-mail sur le domaine, mobile « sur les chantiers »)
    if ctx.ok('C30'):
        lignes = [('Bureau', '+41 22 771 20 15', 'tel:+41227712015'),
                  ('Sur les chantiers', '+41 78 631 14 34', 'tel:+41786311434'),
                  (None, 'contact@andyconstruct.ch', 'mailto:contact@andyconstruct.ch')]
    else:
        lignes = [('Bureau', '+41 22 771 20 15', 'tel:+41227712015'),
                  ('Mobile', '+41 78 631 14 34', 'tel:+41786311434'),
                  (None, 'andy.construct@bluewin.ch', 'mailto:andy.construct@bluewin.ch')]
    for lab, val, url in lignes:
        txt = (f'<font name="Sans" size="13" color="#44494F">{lab} :</font> ' if lab else '') + val
        if url.startswith('mailto') and ctx.preview and not ctx.confirme('C30'):
            txt += ctx.tag('C30')
        y0 = d.y
        h = d.para(txt, S('co', 'Mont-700', 17, 23))
        d.lien(url, ML, y0 - h, 140 * mm, h)
        d.espace(1.2 * mm)
    d.espace(9 * mm)

    # Actions à gauche ; code QR et carte de la zone à droite
    colw = 104 * mm
    y_top = d.y
    blocs = [('Envoyer un dossier de soumission',
              'Descriptif ou série de prix, plans, date de remise des offres. Fichiers lourds : un lien de transfert convient.', [])]
    if ctx.ok('C13'):
        blocs.append(('Nous inscrire comme entreprise à consulter',
                      'Communes et institutions : nous vous transmettons nos attestations pour vos procédures de gré à gré et sur invitation.', ['C13']))
    if ctx.ok('C40'):
        blocs.append(('Visiter un chantier en cours', 'Sur rendez-vous, 20 minutes.', ['C40']))
    for titre, txt, codes in blocs:
        d.filet(ML, ML + colw, d.y, ANTH, 0.9)
        d.espace(3.5 * mm)
        d.para(titre + ctx.tag(*codes), ST['h3'], largeur=colw)
        d.espace(1.8 * mm)
        d.para(txt, ST['corps'], largeur=colw)
        d.espace(7 * mm)
    y_g = d.y

    x2 = ML + colw + 12 * mm
    w2 = W - MR - x2
    q = 34 * mm
    xq = x2 + (w2 - q) / 2
    w = QrCodeWidget(URL_PRO_QR, barLevel='M', barBorder=0)
    b = w.getBounds()
    dr = Drawing(q, q, transform=[q / (b[2] - b[0]), 0, 0, q / (b[3] - b[1]), 0, 0])
    dr.add(w)
    renderPDF.draw(dr, c, xq, y_top - q)
    d.lien(URL_PRO_QR, xq, y_top - q, q, q)
    yq = y_top - q - 2.5 * mm
    st = S('qr', 'Sans', 10, 12.5, GRAPH, TA_CENTER)
    hq = d.para('www.andyconstruct.ch/<br/>professionnels.html', st, x=x2, largeur=w2, y=yq, avancer=False)
    d.lien(URL_PRO_QR, x2, yq - hq, w2, hq)
    ym = yq - hq - 8 * mm
    hc = carte_romandie(d, x2, ym, w2)
    d.para('Toute la Suisse romande, depuis Carouge.', S('cz', 'Sans', 10, 12.5, GRAPH, TA_CENTER), x=x2, largeur=w2,
           y=ym - hc - 2 * mm, avancer=False)
    d.y = min(y_g, ym - hc - 8 * mm)

    # Bande anthracite : logo blanc et pied du document (hauteur selon la place restante)
    bh = min(max(d.y - 10 * mm, 40 * mm), 72 * mm)
    if d.y - 6 * mm < bh:
        debordement(f'plaquette, page contact : {(bh - d.y + 6 * mm) / mm:.1f} mm de trop')
    c.setFillColor(ANTH)
    c.rect(0, 0, W, bh, stroke=0, fill=1)
    lw = 54 * mm
    lh = lw * 232 / 640
    c.drawImage(str(IMG / 'brand' / 'logo-andy-construct-blanc.png'), ML - 1 * mm, bh - 12 * mm - lh, lw, lh, mask='auto')
    maj = f'Document mis à jour le {date_longue(ctx.date)}'.replace(' ', NB)
    pied = f'Andy Construct, Chanton &amp; Cie · Route des Acacias 48 · 1227 Carouge · IDE CHE-113.706.162 · {maj}'
    d.para(pied, S('pa', 'Sans', 10.5, 14.5, ACIER), x=ML, largeur=CW, y=21 * mm, verifier=False)
    c.setFont('Mont-600', 9)
    c.setFillColor(ACIER)
    c.drawRightString(W - MR, bh - 12 * mm - 9, f'{d.no} / {d.total}')
    d.fin(pied=False)


# --------------------------------------------------------------------------------------------
# Guide « Réduire le bruit chez soi » (copy-deck §Q.2)
# --------------------------------------------------------------------------------------------

TXT_W = 150 * mm   # mesure du texte courant du guide (~ 70 caractères)


def guide(ctx: Ctx, chemin: Path):
    pages = [g_couverture, g_p2, g_p3, g_p4, g_p5, g_p6, g_p7, g_p8]
    d = Doc(chemin, ctx, 'Réduire le bruit chez soi : ce qui marche vraiment',
            "Guide pour les propriétaires et les locataires : bruit aérien ou d'impact, isoler ou corriger, ce qui marche, ce qui ne marche pas, questions à poser à une entreprise.",
            'bruit, isolation phonique, isolation acoustique, voisin, doublage, faux-plafond, PPE, locataire, Genève, Andy Construct',
            'Réduire le bruit chez soi', 'Réduire le bruit chez soi · un guide d\'Andy Construct', len(pages))
    for p in pages:
        p(d)
    d.save()
    return len(pages)


def titre_page(d: Doc, surtitre, titre):
    d.surtitre(surtitre)
    d.para(titre, ST['h1'], largeur=TXT_W)
    d.espace(6 * mm)


def arcs(c, cx, cy, rayons, a0, etendue, couleur, ep=1.3, tirets=None):
    c.setStrokeColor(couleur)
    c.setLineWidth(ep)
    c.setDash(*(tirets or ([], 0)))
    for r in rayons:
        p = c.beginPath()
        p.arc(cx - r, cy - r, cx + r, cy + r, startAng=a0, extent=etendue)
        c.drawPath(p, stroke=1, fill=0)
    c.setDash([], 0)


def hachures(c, x, y, w, h, pas=2.2 * mm, couleur=GRAPH, ep=0.5, fond=GRIS_M):
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, w, h)
    c.clipPath(p, stroke=0, fill=0)
    c.setFillColor(fond)
    c.rect(x, y, w, h, stroke=0, fill=1)
    c.setStrokeColor(couleur)
    c.setLineWidth(ep)
    k = -h
    while k < w:
        c.line(x + k, y, x + k + h, y + h)
        k += pas
    c.restoreState()
    c.setStrokeColor(couleur)
    c.setLineWidth(0.8)
    c.rect(x, y, w, h, stroke=1, fill=0)


def laine(c, x, y, w, h, couleur=GRAPH):
    """Isolant souple : boucles régulières (convention de dessin des laines minérales)."""
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, w, h)
    c.clipPath(p, stroke=0, fill=0)
    c.setStrokeColor(couleur)
    c.setLineWidth(0.55)
    amp = w / 2 - 0.6 * mm
    pas = 2.6 * mm
    q = c.beginPath()
    yy = y - pas
    q.moveTo(x + w / 2, yy)
    sens = 1
    while yy < y + h + pas:
        q.curveTo(x + w / 2 + sens * amp, yy + pas * 0.2, x + w / 2 + sens * amp, yy + pas * 0.8, x + w / 2, yy + pas)
        yy += pas
        sens = -sens
    c.drawPath(q, stroke=1, fill=0)
    c.restoreState()


def fleche(c, x1, y1, x2, y2, couleur, ep=1.3, tete=2.4 * mm):
    c.setStrokeColor(couleur)
    c.setFillColor(couleur)
    c.setLineWidth(ep)
    ang = math.atan2(y2 - y1, x2 - x1)
    xb, yb = x2 - tete * 0.8 * math.cos(ang), y2 - tete * 0.8 * math.sin(ang)
    c.line(x1, y1, xb, yb)
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(x2 - tete * math.cos(ang - 0.42), y2 - tete * math.sin(ang - 0.42))
    p.lineTo(x2 - tete * math.cos(ang + 0.42), y2 - tete * math.sin(ang + 0.42))
    p.close()
    c.drawPath(p, stroke=0, fill=1)


def croix(c, x, y, r=3.4 * mm):
    """Pastille « ne marche pas » : cercle et croix (lisible en noir et blanc)."""
    c.setStrokeColor(ANTH)
    c.setLineWidth(1.1)
    c.circle(x, y, r, stroke=1, fill=0)
    c.setStrokeColor(ROUGE)
    c.setLineWidth(1.6)
    k = r * 0.45
    c.line(x - k, y - k, x + k, y + k)
    c.line(x - k, y + k, x + k, y - k)


def tv(c, x, y):
    c.setStrokeColor(ANTH)
    c.setLineWidth(1)
    c.setFillColor(white)
    c.roundRect(x, y + 3 * mm, 15 * mm, 10 * mm, 0.8 * mm, stroke=1, fill=1)
    c.line(x + 7.5 * mm, y + 3 * mm, x + 7.5 * mm, y + 1 * mm)
    c.line(x + 4 * mm, y + 1 * mm, x + 11 * mm, y + 1 * mm)


def schema_aerien(d: Doc, x, y, w, h):
    c = d.c
    sol = y + 4 * mm
    c.setStrokeColor(GRAPH)
    c.setLineWidth(0.8)
    c.line(x, sol, x + w, sol)
    mx = x + w * 0.56
    hachures(c, mx, sol, 5 * mm, h - 6 * mm)
    tv(c, x + 6 * mm, sol)
    arcs(c, x + 21 * mm, sol + 8 * mm, [5 * mm, 9.5 * mm, 14 * mm, 18.5 * mm], -38, 76, ROUGE, 1.4)
    arcs(c, mx + 5 * mm, sol + 8 * mm, [5 * mm, 9.5 * mm], -32, 64, ROUGE, 0.8, ([2, 2], 0))
    d.para('Voix, télévision, musique', ST['schema'], x=x + 2 * mm, largeur=40 * mm, y=y + h, avancer=False, verifier=False)
    d.para('Chez vous', ST['schema'], x=mx + 8 * mm, largeur=w - (mx - x) - 8 * mm, y=y + h, avancer=False, verifier=False)


def schema_impact(d: Doc, x, y, w, h):
    c = d.c
    dalle_y = y + h * 0.5
    ep = 6 * mm
    hachures(c, x, dalle_y, w, ep)
    # Chaussure stylisée et chocs
    sx = x + w * 0.3
    c.setFillColor(ANTH)
    p = c.beginPath()
    p.moveTo(sx, dalle_y + ep)
    p.lineTo(sx + 16 * mm, dalle_y + ep)
    p.curveTo(sx + 18 * mm, dalle_y + ep, sx + 18 * mm, dalle_y + ep + 5 * mm, sx + 14 * mm, dalle_y + ep + 5.5 * mm)
    p.lineTo(sx + 7 * mm, dalle_y + ep + 7 * mm)
    p.lineTo(sx + 5 * mm, dalle_y + ep + 12 * mm)
    p.lineTo(sx, dalle_y + ep + 12 * mm)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.setStrokeColor(ROUGE)
    c.setLineWidth(1.4)
    for dx, dy, l in ((-3, 2, 3.2), (-3.5, 6, 3.2), (21, 2, 3)):
        xx = sx + dx * mm
        yy = dalle_y + ep + dy * mm
        c.line(xx, yy, xx + (l * mm if dx > 0 else -l * mm), yy + 1.2 * mm)
    # Vibration dans la dalle, puis bruit dans la pièce du dessous
    c.setLineWidth(1.2)
    pz = c.beginPath()
    xx = x + 3 * mm
    pz.moveTo(xx, dalle_y + ep / 2)
    k = 0
    while xx < x + w - 4 * mm:
        xx += 2.2 * mm
        k += 1
        pz.lineTo(xx, dalle_y + ep / 2 + (1.3 * mm if k % 2 else -1.3 * mm))
    c.drawPath(pz, stroke=1, fill=0)
    arcs(c, sx + 8 * mm, dalle_y, [5 * mm, 9.5 * mm, 14 * mm], 222, 96, ROUGE, 1.4)
    d.para('Pas, talons, chaises', ST['schema'], x=x + w * 0.62, largeur=w * 0.38, y=dalle_y + ep + 10 * mm, avancer=False, verifier=False)
    d.para('Chez vous', ST['schema'], x=x + w * 0.62, largeur=w * 0.38, y=dalle_y - 4 * mm, avancer=False, verifier=False)


def schema_isoler(d: Doc, x, y, w, h):
    c = d.c
    sol = y + 4 * mm
    c.setStrokeColor(GRAPH)
    c.setLineWidth(0.8)
    c.line(x, sol, x + w, sol)
    mx = x + w * 0.5
    hachures(c, mx - 4 * mm, sol, 4 * mm, h - 6 * mm)
    laine(c, mx + 0.8 * mm, sol, 4.2 * mm, h - 6 * mm)
    c.setFillColor(GRIS_M)
    c.setStrokeColor(GRAPH)
    c.setLineWidth(0.8)
    c.rect(mx + 5 * mm, sol, 2.2 * mm, h - 6 * mm, stroke=1, fill=1)
    arcs(c, mx - 22 * mm, sol + h * 0.42, [5 * mm, 10 * mm, 15 * mm], -35, 70, ROUGE, 1.4)
    c.setStrokeColor(ANTH)
    c.setLineWidth(2.2)
    c.line(mx - 6.5 * mm, sol + h * 0.42 - 5 * mm, mx - 6.5 * mm, sol + h * 0.42 + 5 * mm)
    d.para('Le voisin', ST['schema'], x=x + 2 * mm, largeur=w * 0.4, y=y + h, avancer=False, verifier=False)
    d.para('Chez vous', ST['schema'], x=mx + 10 * mm, largeur=w * 0.4, y=y + h, avancer=False, verifier=False)


def schema_corriger(d: Doc, x, y, w, h):
    c = d.c
    sol = y + 4 * mm
    bx, bw, bh = x + 4 * mm, w - 8 * mm, h - 9 * mm
    c.setStrokeColor(GRAPH)
    c.setLineWidth(1.6)
    c.rect(bx, sol, bw, bh, stroke=1, fill=0)
    # Panneaux absorbants (mur de gauche et plafond)
    for (px, py, pw, ph) in ((bx + 1 * mm, sol + bh * 0.3, 2.6 * mm, bh * 0.45),
                             (bx + bw * 0.38, sol + bh - 3.6 * mm, bw * 0.3, 2.6 * mm)):
        c.setFillColor(GRIS_M)
        c.setStrokeColor(GRAPH)
        c.setLineWidth(0.7)
        c.rect(px, py, pw, ph, stroke=1, fill=1)
    # Trajet du son qui se réfléchit (écho)
    pts = [(bx + bw * 0.78, sol + bh * 0.25), (bx + bw, sol + bh * 0.55), (bx + bw * 0.6, sol + bh),
           (bx + bw * 0.2, sol + bh * 0.62), (bx + bw * 0.45, sol)]
    c.setStrokeColor(ROUGE)
    c.setLineWidth(1.2)
    c.setDash([3, 2], 0)
    for (x1, y1), (x2, y2) in zip(pts, pts[1:-1]):
        c.line(x1, y1, x2, y2)
    c.setDash([], 0)
    fleche(c, pts[-2][0], pts[-2][1], pts[-1][0] + 1, pts[-1][1] + 1.5 * mm, ROUGE, 1.2)
    c.setFillColor(ROUGE)
    c.circle(pts[0][0], pts[0][1], 1.2 * mm, stroke=0, fill=1)
    d.para('Une seule pièce', ST['schema'], x=bx, largeur=bw, y=y + h + 1 * mm, avancer=False, verifier=False)


def schema_doublage(d: Doc, x, y, w, h_couches):
    """Coupe d'un doublage acoustique : mur existant | écart | ossature + laine | plaques."""
    c = d.c
    yb = y
    mur_w, ecart, oss_w, pl = 44 * mm, 4 * mm, 38 * mm, 3.2 * mm
    xm = x + 29 * mm
    hachures(c, xm, yb, mur_w, h_couches)
    xo = xm + mur_w + ecart
    laine(c, xo, yb, oss_w, h_couches)
    c.setStrokeColor(ANTH)
    c.setLineWidth(1)
    for yy in (yb + h_couches * 0.16, yb + h_couches * 0.7):          # montants métalliques (profils en C)
        p = c.beginPath()
        p.moveTo(xo + 5 * mm, yy)
        p.lineTo(xo, yy)
        p.lineTo(xo, yy + 4.5 * mm)
        p.lineTo(xo + oss_w, yy + 4.5 * mm)
        p.lineTo(xo + oss_w, yy)
        p.lineTo(xo + oss_w - 5 * mm, yy)
        c.drawPath(p, stroke=1, fill=0)
    xp = xo + oss_w
    for k in range(2):
        c.setFillColor(GRIS_M if k == 0 else BRUME)
        c.setStrokeColor(GRAPH)
        c.setLineWidth(0.8)
        c.rect(xp + k * pl, yb, pl, h_couches, stroke=1, fill=1)
    fin = xp + 2 * pl

    def accolade(x1, x2, txt):
        ya = yb + h_couches + 3 * mm
        c.setStrokeColor(ROUGE_F)
        c.setLineWidth(0.9)
        c.line(x1, ya - 1.4 * mm, x1, ya)
        c.line(x1, ya, x2, ya)
        c.line(x2, ya, x2, ya - 1.4 * mm)
        d.lettres(txt, (x1 + x2) / 2, ya + 2.4 * mm, 'Mont-600', 9, ROUGE_F, 0.14, centre=True)
    accolade(xm, xm + mur_w, 'MASSE')
    accolade(xm + mur_w + 0.8 * mm, xp - 0.8 * mm, 'RESSORT')
    accolade(xp, fin, 'MASSE')

    def dessous(xa, txt, rang, larg):
        yl = yb - 4 * mm - rang * 9.5 * mm
        c.setStrokeColor(GRAPH)
        c.setLineWidth(0.5)
        c.line(xa, yb, xa, yl)
        d.para(txt, ST['schema'], x=xa + 1.4 * mm, largeur=larg, y=yl + 2.6 * mm, avancer=False, verifier=False)
    dessous(xm + mur_w * 0.3, 'Mur existant', 0, 38 * mm)
    dessous(xm + mur_w + ecart / 2, 'Quelques millimètres d\'écart', 1, 50 * mm)
    dessous(xo + oss_w * 0.5, 'Ossature indépendante et laine minérale', 0, 44 * mm)
    # À droite : les plaques, puis la pièce
    xl = fin + 7 * mm
    yh = yb + h_couches * 0.78
    c.setStrokeColor(GRAPH)
    c.setLineWidth(0.5)
    c.line(fin, yh, xl - 1.2 * mm, yh)
    d.para('Une ou deux plaques de plâtre', ST['schema'], x=xl, largeur=x + w - xl, y=yh + 1.6 * mm, avancer=False, verifier=False)
    d.lettres('VOTRE PIÈCE', xl, yb + h_couches * 0.25, 'Mont-600', 8, GRAPH, 0.14)
    d.lettres('CÔTÉ VOISIN', x, yb + h_couches * 0.25, 'Mont-600', 8, GRAPH, 0.14)
    return fin


def schema_contourne(d: Doc, x, y, w, h):
    """Isolation d'un seul côté : le bruit passe par le plafond et par le sol (transmissions latérales)."""
    c = d.c
    ep = 7 * mm
    hachures(c, x, y + h - ep, w, ep)
    hachures(c, x, y, w, ep)
    mx = x + w / 2
    hachures(c, mx - 3 * mm, y + ep, 6 * mm, h - 2 * ep)
    laine(c, mx + 3.2 * mm, y + ep, 5 * mm, h - 2 * ep)
    c.setFillColor(GRIS_M)
    c.setStrokeColor(GRAPH)
    c.setLineWidth(0.8)
    c.rect(mx + 8.4 * mm, y + ep, 2.6 * mm, h - 2 * ep, stroke=1, fill=1)
    tv(c, x + 6 * mm, y + ep)
    arcs(c, x + 21 * mm, y + ep + 8 * mm, [5 * mm, 9.5 * mm, 14 * mm], -40, 80, ROUGE, 1.4)
    # Le chemin direct est arrêté
    yd = y + h / 2
    fleche(c, x + 46 * mm, yd, mx - 4.2 * mm, yd, ROUGE, 1.3)
    c.setStrokeColor(ANTH)
    c.setLineWidth(2.4)
    c.line(mx - 3.6 * mm, yd - 4 * mm, mx - 3.6 * mm, yd + 4 * mm)
    # Les chemins latéraux contournent par la dalle du haut et par celle du bas
    c.setDash([3, 2], 0)
    for haut in (True, False):
        ys = y + h - ep / 2 if haut else y + ep / 2
        y1 = y + h - ep - 9 * mm if haut else y + ep + 16 * mm
        y2 = y + h - ep - 12 * mm if haut else y + ep + 10 * mm
        c.setStrokeColor(ROUGE)
        c.setLineWidth(1.3)
        p = c.beginPath()
        p.moveTo(x + 38 * mm, y1)
        p.lineTo(x + 44 * mm, ys)
        p.lineTo(mx + 22 * mm, ys)
        c.drawPath(p, stroke=1, fill=0)
        c.setDash([], 0)
        fleche(c, mx + 22 * mm, ys, mx + 29 * mm, y2, ROUGE, 1.3)
        c.setDash([3, 2], 0)
    c.setDash([], 0)
    d.lettres('LE VOISIN', x + 4 * mm, y + h - ep - 6 * mm, 'Mont-600', 8, GRAPH, 0.14)
    d.lettres('CHEZ VOUS', x + w - 4 * mm, y + h - ep - 6 * mm, 'Mont-600', 8, GRAPH, 0.14, droite=True)
    d.para('Isolation d\'un seul côté', ST['schema'], x=mx + 13 * mm, largeur=40 * mm, y=y + h / 2 + 2.5 * mm, avancer=False, verifier=False)


def schema_immeuble(d: Doc, x, y, w, h):
    """Coupe d'un petit immeuble en PPE : lot privé, mur mitoyen, structure, partie commune."""
    c = d.c
    yb = y + 9 * mm                     # place pour l'étiquette du mur mitoyen, sous le dessin
    h = h - 9 * mm
    bw = w * 0.58
    ep = 2.6 * mm
    et = (h - ep) / 3
    cage = bw * 0.2
    lot_w = (bw - cage - 3 * ep) / 2
    xc = x + bw - ep - cage
    # Lot privé mis en évidence (étage du milieu, à gauche)
    c.setFillColor(GRIS_M)
    c.rect(x + ep, yb + ep + et, lot_w, et - ep, stroke=0, fill=1)
    # Cage d'escalier (partie commune) : volées stylisées
    c.setStrokeColor(GRAPH)
    c.setLineWidth(0.6)
    for k in range(3):
        y0 = yb + ep + k * et
        n = 6
        for s in range(n):
            xs = xc + 1.5 * mm + s * (cage - 3 * mm) / n
            ys = y0 + s * (et - ep) / n
            c.line(xs, ys, xs + (cage - 3 * mm) / n, ys)
            c.line(xs + (cage - 3 * mm) / n, ys, xs + (cage - 3 * mm) / n, ys + (et - ep) / n)
    # Structure : dalles et murs porteurs (hachurés)
    for k in range(4):
        hachures(c, x, yb + k * et, bw, ep, pas=1.6 * mm)
    hachures(c, x, yb, ep, h, pas=1.6 * mm)
    hachures(c, x + bw - ep, yb, ep, h, pas=1.6 * mm)
    hachures(c, x + ep + lot_w, yb, ep, h, pas=1.6 * mm)           # mur mitoyen entre les deux logements
    c.setStrokeColor(GRAPH)
    c.setLineWidth(0.8)
    c.line(xc, yb, xc, yb + h)                                      # cloison de la cage d'escalier
    c.setStrokeColor(ROUGE)
    c.setLineWidth(1.8)
    c.rect(x + ep, yb + ep + et, lot_w, et - ep, stroke=1, fill=0)
    d.para('<font name="Sans-600" color="#1D1F22">Votre lot</font>', ST['schema_c'], x=x + ep, largeur=lot_w,
           y=yb + ep + et + (et - ep) / 2 + 5, avancer=False, verifier=False)
    # Mur mitoyen : étiquette sous le dessin
    xm = x + ep + lot_w + ep / 2
    c.setStrokeColor(GRAPH)
    c.setLineWidth(0.5)
    c.line(xm, yb + 3 * mm, xm, yb - 4 * mm)
    d.para('Mur mitoyen', ST['schema_c'], x=xm - 20 * mm, largeur=40 * mm, y=yb - 4.6 * mm, avancer=False, verifier=False)
    # Étiquettes à droite, sans croiser le dessin
    xl = x + bw + 9 * mm

    def etiquette(xa, ya, txt):
        c.setStrokeColor(GRAPH)
        c.setLineWidth(0.5)
        c.setFillColor(GRAPH)
        c.circle(xa, ya, 0.6 * mm, stroke=0, fill=1)
        c.line(xa, ya, xl - 1.5 * mm, ya)
        d.para(txt, ST['schema'], x=xl, largeur=x + w - xl, y=ya + 5.2, avancer=False, verifier=False)
    etiquette(x + bw - ep / 2, yb + h - ep / 2, 'Structure : dalles, murs porteurs')
    etiquette(xc + cage * 0.62, yb + ep + et * 1.5, 'Partie commune : cage d\'escalier')


def encadre(d: Doc, contenu, pad=6 * mm, barre=True, fond=BRUME, largeur=TXT_W, x=ML):
    """contenu : liste de (texte, style, espace_apres). Encadré gris clair à filet rouge."""
    hs = [d.hauteur(t, s, largeur - 2 * pad) for t, s, _ in contenu]
    hb = pad * 2 + sum(hs) + sum(a for _, _, a in contenu[:-1])
    if d.y - hb < d.bas:
        debordement(f'{d.chemin.name}, page {d.no} : encadré trop haut')
    d.c.setFillColor(fond)
    d.c.rect(x, d.y - hb, largeur, hb, stroke=0, fill=1)
    if barre:
        d.c.setFillColor(ROUGE)
        d.c.rect(x, d.y - hb, 1.6 * mm, hb, stroke=0, fill=1)
    d.y -= pad
    for (t, s, a) in contenu:
        d.para(t, s, x=x + pad, largeur=largeur - 2 * pad)
        d.y -= a
    d.y += contenu[-1][2]
    d.y -= pad


def g_couverture(d: Doc):
    c = d.c
    d.debut(entete=False)
    lw = 50 * mm
    c.drawImage(str(IMG / 'brand' / 'logo-andy-construct.png'), ML - 1.2 * mm, H - 16 * mm - lw * 232 / 640, lw, lw * 232 / 640, mask='auto')
    d.y = H - 72 * mm
    d.biseau(ML, d.y, 12 * mm, 2.6 * mm)
    d.espace(9 * mm)
    d.para('Réduire le bruit chez soi', S('gt', 'Mont-700', 42, 47), largeur=150 * mm)
    d.espace(7 * mm)
    d.para('Ce qui marche vraiment, ce qui ne marche pas, et les questions à poser avant de signer.',
           S('gst', 'Sans', 18, 25, GRAPH), largeur=135 * mm)
    # Illustration : le son traverse une paroi légère, la paroi désolidarisée l'arrête
    yb, hh = 52 * mm, 92 * mm
    mx = 128 * mm
    arcs(c, 52 * mm, yb + hh / 2, [10 * mm, 22 * mm, 34 * mm, 46 * mm, 58 * mm], -34, 68, ROUGE, 2.2)
    hachures(c, mx, yb, 9 * mm, hh, pas=2.6 * mm)
    laine(c, mx + 10.5 * mm, yb, 9 * mm, hh)
    c.setFillColor(GRIS_M)
    c.setStrokeColor(GRAPH)
    c.setLineWidth(0.8)
    c.rect(mx + 21 * mm, yb, 3 * mm, hh, stroke=1, fill=1)
    c.rect(mx + 24 * mm, yb, 3 * mm, hh, stroke=1, fill=1)
    arcs(c, mx + 27 * mm, yb + hh / 2, [8 * mm, 15 * mm], -30, 60, ACIER, 1.2, ([3, 3], 0))
    d.filet(ML, W - MR, 34 * mm)
    d.para(f"Un guide d'Andy Construct, entreprise de plâtrerie, de peinture et d'isolation à Carouge. Édition {d.ctx.edition}.",
           S('gb', 'Sans', 12, 16, GRAPH), y=29 * mm, largeur=150 * mm, verifier=False)
    d.fin(pied=False)


def g_p2(d: Doc):
    d.debut()
    titre_page(d, 'Avant tout', 'Quel bruit entendez-vous ?')
    d.para("Avant de commander des travaux, il faut savoir d'où vient le bruit. Il en existe deux sortes, "
           "qui ne se traitent pas de la même façon.", ST['guide'], largeur=TXT_W)
    d.espace(8 * mm)
    gout = 10 * mm
    cw2 = (CW - gout) / 2
    hs = 50 * mm
    y0 = d.y
    schema_aerien(d, ML, y0 - hs, cw2, hs)
    schema_impact(d, ML + cw2 + gout, y0 - hs, cw2, hs)
    d.y = y0 - hs - 6 * mm
    y1 = d.y
    h1 = d.para("<b>Le bruit aérien</b> voyage dans l'air : voix, télévision, musique, chien qui aboie. Il traverse "
                "les murs et les plafonds trop légers, et passe par les moindres ouvertures.", ST['guide'], x=ML, largeur=cw2, avancer=False)
    h2 = d.para("<b>Le bruit d'impact</b> naît d'un choc sur la structure : pas, talons, chaises qu'on tire, objets "
                "qui tombent. Il se propage dans le béton, puis ressort dans les pièces voisines.", ST['guide'],
                x=ML + cw2 + gout, largeur=cw2, avancer=False)
    d.y = y1 - max(h1, h2) - 10 * mm
    puce = '<font name="Mont-700" color="#C4000D">›</font>' + NB + NB
    encadre(d, [
        ('<b>Un test simple.</b> Pendant une semaine, notez ce que vous entendez, d\'où et à quelle heure.', ST['guide'], 3 * mm),
        (puce + "Vous entendez surtout des voix ou la télévision : c'est du bruit aérien. Une isolation chez vous peut nettement l'améliorer.", ST['guide'], 2.5 * mm),
        (puce + "Vous entendez surtout des pas ou des chocs au-dessus : c'est du bruit d'impact. Le plus efficace est d'agir sur le sol du voisin. Chez vous, on peut l'atténuer, pas le supprimer.", ST['guide'], 0),
    ], largeur=CW)
    d.controle()
    d.fin()


def g_p3(d: Doc):
    d.debut()
    titre_page(d, 'Une confusion fréquente', 'Isoler ou corriger')
    d.para("Deux problèmes se ressemblent, et c'est la source de beaucoup de déceptions.", ST['guide'], largeur=TXT_W)
    d.espace(9 * mm)
    gout = 10 * mm
    cw2 = (CW - gout) / 2
    hs = 48 * mm
    y0 = d.y
    schema_isoler(d, ML, y0 - hs, cw2, hs)
    schema_corriger(d, ML + cw2 + gout, y0 - hs, cw2, hs)
    d.y = y0 - hs - 6 * mm
    y1 = d.y
    h1 = d.para("<b>Isoler</b>, c'est empêcher le bruit de passer d'un local à l'autre. On a besoin d'une paroi "
                "lourde, désolidarisée de la structure et étanche à l'air.", ST['guide'], x=ML, largeur=cw2, avancer=False)
    h2 = d.para("<b>Corriger</b>, c'est réduire l'écho à l'intérieur d'une pièce : une salle à manger qui résonne, "
                "un séjour au carrelage et aux grandes baies vitrées. On ajoute des matériaux qui absorbent le son : "
                "rideaux épais, tapis, meubles, panneaux absorbants.", ST['guide'], x=ML + cw2 + gout, largeur=cw2, avancer=False)
    d.y = y1 - max(h1, h2) - 11 * mm
    encadre(d, [('<b>À retenir.</b> Un panneau absorbant rend une pièce plus agréable, mais il ne vous protège pas du '
                 'bruit du voisin. Une bonne isolation ne réduit pas l\'écho de votre séjour. Si une entreprise vous '
                 'propose l\'un pour régler l\'autre, demandez-lui pourquoi.', ST['guide'], 0)], largeur=CW)
    d.controle()
    d.fin()


def g_p4(d: Doc):
    ctx = d.ctx
    d.debut()
    titre_page(d, 'Les bonnes techniques', 'Ce qui marche')
    d.para("Le principe est toujours le même : une paroi lourde, posée sans contact rigide avec la structure, avec "
           "un isolant souple à l'intérieur. Les spécialistes parlent du principe « masse, ressort, masse ».",
           ST['guide'], largeur=TXT_W)
    d.espace(17 * mm)
    hc = 32 * mm
    schema_doublage(d, ML, d.y - hc, CW, hc)
    d.y -= hc + 27 * mm
    perte = ('La pièce perd en général 7 à 10 cm' + ctx.tag('C18') + '.') if ctx.ok('C18') else 'La pièce perd en général quelques centimètres.'
    for t in [
        "<b>Le doublage acoustique d'un mur.</b> Une ossature indépendante, posée à quelques millimètres du mur "
        "existant, une laine minérale, puis une ou deux plaques de plâtre. Efficace contre les voix et la "
        "télévision du voisin. " + perte,
        "<b>Le faux-plafond acoustique.</b> Il est suspendu par des suspentes qui amortissent les vibrations, avec "
        "un isolant au-dessus. Il réduit les voix venant d'en haut, et en partie les bruits de pas.",
        "<b>La cloison acoustique.</b> Deux ossatures séparées, un isolant, des plaques doublées. Pour une chambre, "
        "un bureau à domicile ou une pièce de musique.",
    ]:
        d.para(t, ST['guide'], largeur=TXT_W)
        d.espace(4 * mm)
    d.espace(3 * mm)
    encadre(d, [('<b>Les points faibles.</b> Le bruit passe là où l\'on ne regarde pas : prises électriques placées dos '
                 'à dos, gaines, portes creuses, bas de porte, joints autour des fenêtres, conduits. Une bonne isolation '
                 'les traite tous. Sinon, le résultat déçoit.', ST['guide'], 0)], largeur=CW)
    d.controle()
    d.fin()


def g_p5(d: Doc):
    d.debut()
    titre_page(d, 'Idées reçues', 'Ce qui ne marche pas')
    d.espace(1 * mm)
    items = [
        ("Les boîtes à œufs et la mousse collée au mur.", "Elles réduisent un peu l'écho, mais n'arrêtent pas le bruit qui traverse."),
        ("La « peinture isolante ».", "Une couche de quelques dixièmes de millimètre ne change presque rien au bruit qui traverse un mur."),
        ("Une plaque collée directement sur le mur.", "Sans désolidarisation, elle peut même transmettre certains bruits."),
        ("Le liège mince ou le papier peint épais.", "Agréables au toucher, sans effet sur le bruit du voisin."),
        ("Une isolation d'un seul côté de la pièce, quand le bruit vient d'ailleurs.", "Le bruit contourne : il passe par le plafond, le sol ou le mur voisin."),
    ]
    d.filet(ML, ML + TXT_W + 10 * mm, d.y, ANTH, 0.9)
    for tit, txt in items:
        y0 = d.y - 5 * mm
        croix(d.c, ML + 4 * mm, y0 - 3.4 * mm)
        h = d.para(f'<b>{tit}</b> {txt}', ST['guide'], x=ML + 14 * mm, largeur=TXT_W - 4 * mm, y=y0, avancer=False)
        d.y = y0 - h - 5 * mm
        d.filet(ML, ML + TXT_W + 10 * mm, d.y)
    d.espace(12 * mm)
    hs = 62 * mm
    schema_contourne(d, ML + 8 * mm, d.y - hs, CW - 16 * mm, hs)
    d.y -= hs
    d.controle()
    d.fin()


def g_p6(d: Doc):
    d.debut()
    titre_page(d, 'Avant les travaux', 'Locataire ou copropriétaire ?')
    blocs = [
        "<b>Vous êtes locataire.</b> Avant de transformer le logement, il vous faut l'accord écrit de votre bailleur "
        "ou de votre régie. Demandez-le avant de signer quoi que ce soit avec une entreprise. Une entreprise sérieuse "
        "peut vous remettre un descriptif des travaux à joindre à votre demande.",
        "<b>Vous êtes en PPE (propriété par étages).</b> Les travaux dans votre lot sont en général possibles. Ceux "
        "qui touchent un mur mitoyen, la structure ou une partie commune peuvent demander l'accord de l'administrateur "
        "ou de l'assemblée. Lisez votre règlement et posez la question avant de commencer.",
        "<b>Parlez à votre voisin.</b> Si vous entendez surtout des pas, un tapis ou une sous-couche chez lui peut "
        "faire plus qu'un faux-plafond chez vous. Une conversation calme, une lettre courtoise : cela règle parfois "
        "plus vite le problème que des travaux.",
    ]
    for i, t in enumerate(blocs):
        d.filet(ML, ML + TXT_W, d.y, ANTH, 0.9)
        d.espace(4.5 * mm)
        d.para(t, ST['guide'], largeur=TXT_W)
        d.espace(7 * mm)
        if i == 1:
            hs = 58 * mm
            schema_immeuble(d, ML + 6 * mm, d.y - hs, CW - 6 * mm, hs)
            d.y -= hs + 9 * mm
    d.para('<i>Ces informations sont générales et ne remplacent pas un conseil juridique.</i>', ST['guide_g'], largeur=TXT_W)
    d.controle()
    d.fin()


def g_p7(d: Doc):
    d.debut()
    titre_page(d, 'Pour comparer les offres', 'Huit questions à poser à une entreprise')
    d.para('Valables pour nous comme pour les autres.', ST['guide_g'], largeur=TXT_W)
    d.espace(7 * mm)
    qs = ["Êtes-vous venu voir les lieux avant de chiffrer ?",
          "Quel type de bruit avez-vous identifié, et pourquoi proposez-vous ces travaux ?",
          "Que traitez-vous en plus de la paroi : prises, gaines, portes, raccords ?",
          "Combien de centimètres la pièce va-t-elle perdre ?",
          "Que contient l'offre, et qu'est-ce qui n'y est pas compris ?",
          "Qui vient faire les travaux, et qui est mon interlocuteur ?",
          "Comment la poussière et les meubles sont-ils protégés ?",
          "Que se passe-t-il si le résultat n'est pas celui annoncé ?"]
    # Trois colonnes à cocher pour comparer jusqu'à trois entreprises sur papier
    colw = 14 * mm
    xcols = [W - MR - (3 - k) * colw for k in range(3)]
    tw = xcols[0] - (ML + 10 * mm) - 6 * mm
    d.lettres('ENTREPRISE', xcols[0] + 1.5 * colw, d.y + 1.5 * mm, 'Mont-600', 7.5, GRAPH, 0.16, centre=True)
    for k, xc in enumerate(xcols):
        d.lettres('ABC'[k], xc + colw / 2, d.y - 4.2 * mm, 'Mont-700', 10, ANTH, 0, centre=True)
    d.y -= 7 * mm
    d.filet(ML, W - MR, d.y, ANTH, 0.9)
    for i, q in enumerate(qs, 1):
        y0 = d.y - 3.4 * mm
        d.c.setFont('Mont-700', 13)
        d.c.setFillColor(ROUGE_F)
        d.c.drawString(ML, y0 - 13, f'{i}.')
        h = d.para(q, ST['guide'], x=ML + 10 * mm, largeur=tw, y=y0, avancer=False)
        s = 4.6 * mm
        for xc in xcols:
            d.c.setStrokeColor(ANTH)
            d.c.setLineWidth(1)
            d.c.rect(xc + (colw - s) / 2, y0 - s - 0.6 * mm, s, s, stroke=1, fill=0)
        d.y = y0 - max(h, s + 0.6 * mm) - 3.4 * mm
        d.filet(ML, W - MR, d.y)
    d.espace(10 * mm)
    encadre(d, [('<b>Méfiez-vous</b> d\'une promesse de résultat en décibels sans aucune mesure, d\'un prix donné au '
                 'téléphone sans visite, ou d\'un acompte demandé en liquide.', ST['guide'], 0)], largeur=CW)
    d.controle()
    d.fin()


def g_p8(d: Doc):
    ctx, c = d.ctx, d.c
    d.debut()
    titre_page(d, 'Et après ce guide', 'Et ensuite ?')
    d.para("Chaque logement est différent : le bon remède dépend du bruit, de la construction et de l'usage de la pièce.",
           ST['guide'], largeur=TXT_W)
    d.espace(3 * mm)
    d.para('Nous travaillons ainsi :', ST['guide'], largeur=TXT_W)
    d.espace(6 * mm)
    etapes = [('Visite', ' : nous écoutons, nous mesurons, nous regardons d\'où vient le bruit.')]
    etapes.append(('Offre écrite', (' : poste par poste, en CHF, avec la place perdue et ce qui n\'est pas compris.' + ctx.tag('C06')) if ctx.ok('C06') else '.'))
    etapes.append(('Chantier protégé', (' : sols et meubles couverts, nettoyage chaque soir.' + ctx.tag('C07')) if ctx.ok('C07') else '.'))
    etapes.append(('Réception', ' : nous faisons le tour des finitions avec vous.'))
    d.filet(ML, ML + TXT_W + 10 * mm, d.y, ANTH, 0.9)
    for i, (t, suite) in enumerate(etapes, 1):
        y0 = d.y - 4 * mm
        c.setFont('Mont-700', 18)
        c.setFillColor(ANTH)
        c.drawString(ML, y0 - 16, f'{i:02d}')
        h = d.para(f'<b>{t}</b>{suite}', ST['guide'], x=ML + 15 * mm, largeur=TXT_W - 5 * mm, y=y0, avancer=False)
        d.y = y0 - max(h, 7 * mm) - 4 * mm
        d.filet(ML, ML + TXT_W + 10 * mm, d.y)
    d.espace(12 * mm)
    horaires = ' (du lundi au vendredi, 7 h – 18 h' + ctx.tag('C03') + ')' if ctx.ok('C03') else ''
    hb = 44 * mm
    y0 = d.y
    c.setFillColor(ANTH)
    c.rect(ML, y0 - hb, CW, hb, stroke=0, fill=1)
    d.y = y0 - 8 * mm
    d.lettres('DEMANDER UNE VISITE', ML + 8 * mm, d.y - 8.5, 'Mont-600', 8.8, ACIER, 0.18)
    d.biseau(ML + 8 * mm, d.y + 2.2 * mm, 7.2 * mm, 1.7 * mm)
    d.y -= 8.5 + 5 * mm
    yt = d.y
    ht = d.para(f'+41 22 771 20 15<font name="Sans" size="12.5" color="#B9BDC2">{horaires}</font>',
                S('gtel', 'Mont-700', 22, 27, white), x=ML + 8 * mm, largeur=CW - 16 * mm)
    d.lien('tel:+41227712015', ML + 8 * mm, yt - ht, 80 * mm, ht)
    d.espace(2.5 * mm)
    yt = d.y
    hu = d.para('ou www.andyconstruct.ch/isolation-acoustique.html', S('gurl', 'Sans', 13, 18, white), x=ML + 8 * mm, largeur=CW - 16 * mm)
    d.lien('https://www.andyconstruct.ch/isolation-acoustique.html?utm_source=guide-bruit&utm_medium=pdf&utm_campaign=aimant',
           ML + 8 * mm, yt - hu, CW - 16 * mm, hu)
    d.y = y0 - hb - 8 * mm
    d.para('Andy Construct, Chanton &amp; Cie · Route des Acacias 48 · 1227 Carouge · IDE CHE-113.706.162',
           S('gid', 'Sans', 11, 15, GRAPH), largeur=CW)
    lw = 40 * mm
    c.drawImage(str(IMG / 'brand' / 'logo-andy-construct.png'), W - MR - lw, 24 * mm, lw, lw * 232 / 640, mask='auto')
    d.controle()
    d.fin()


# --------------------------------------------------------------------------------------------
# Liste de contrôle « Travaux en immeuble habité » (copy-deck §Q.3)
# --------------------------------------------------------------------------------------------

PIED_REGIE = ('Andy Construct : plâtrerie, faux-plafonds, peinture et isolation en immeuble habité. '
              '+41 22 771 20 15 · www.andyconstruct.ch/professionnels.html · '
              'Andy Construct, Chanton &amp; Cie, Carouge, IDE CHE-113.706.162')


def checklist(ctx: Ctx, chemin: Path):
    pages = [k_p1, k_p2, k_p3]
    d = Doc(chemin, ctx, 'Travaux en immeuble habité : la liste de contrôle de la régie',
            'Liste de contrôle imprimable pour préparer, suivre et réceptionner un chantier dans un immeuble habité, avec un modèle d\'avis aux locataires.',
            'régie, gérance, immeuble habité, site occupé, travaux, avis aux locataires, liste de contrôle, Andy Construct',
            'Travaux en immeuble habité', PIED_REGIE, len(pages))
    d.bas = 26 * mm
    for p in pages:
        p(d)
    d.save()
    return len(pages)


def k_section(d: Doc, titre, items):
    d.surtitre(titre, couleur=ANTH, taille=10)
    d.lettres('FAIT LE', W - MR, d.y + 4 * mm + 1, 'Mont-600', 7.5, GRAPH, 0.16, droite=True)
    d.filet(ML, W - MR, d.y, ANTH, 0.9)
    tx = ML + 10 * mm
    tw = CW - 10 * mm - 30 * mm
    for t in items:
        y0 = d.y - 2.6 * mm
        h = d.para(t, ST['corps12'], x=tx, largeur=tw, y=y0, avancer=False)
        s = 4.8 * mm
        d.c.setStrokeColor(ANTH)
        d.c.setLineWidth(1.1)
        d.c.setFillColor(white)
        d.c.rect(ML + 0.5 * mm, y0 - s - 0.2 * mm, s, s, stroke=1, fill=1)
        d.c.setStrokeColor(ACIER)
        d.c.setLineWidth(0.6)
        d.c.setDash([1, 2], 0)
        d.c.line(W - MR - 24 * mm, y0 - 4.6 * mm, W - MR, y0 - 4.6 * mm)
        d.c.setDash([], 0)
        d.y = y0 - max(h, s + 0.2 * mm) - 2.6 * mm
        d.filet(ML, W - MR, d.y)
    d.controle()


def k_p1(d: Doc):
    d.debut()
    d.para('Travaux en immeuble habité : la liste de contrôle de la régie', S('kt', 'Mont-700', 22, 27), largeur=155 * mm)
    d.espace(5 * mm)
    d.para("Peinture d'une cage d'escalier, plafond après un dégât d'eau, remise en état d'un appartement voisin : "
           "les plaintes et les retards viennent presque toujours d'un manque d'information ou d'organisation. Cette "
           "liste vous aide à préparer le chantier, quelle que soit l'entreprise.", ST['corps'], largeur=CW)
    d.espace(6 * mm)
    # Champs à remplir à la main
    champs = [('Immeuble', ML, 82 * mm), ('Travaux', ML + 88 * mm, CW - 88 * mm),
              ('Entreprise', ML, 82 * mm), ('Responsable de chantier', ML + 88 * mm, CW - 88 * mm)]
    for k, (lab, x, w) in enumerate(champs):
        if k % 2 == 0 and k:
            d.y -= 12 * mm
        d.lettres(lab.upper(), x, d.y - 7.5, 'Mont-600', 7.5, GRAPH, 0.16)
        d.filet(x, x + w, d.y - 10.5 * mm, GRAPH, 0.6)
    d.y -= 10.5 * mm + 9 * mm
    k_section(d, 'Avant les travaux', [
        'Le périmètre est écrit : logements, parties communes, étages concernés.',
        'Les dates de début et de fin sont fixées, avec une marge pour les imprévus.',
        'Le propriétaire ou le mandant a validé l\'offre et le calendrier des travaux.',
        'Les locataires sont informés par écrit au moins 10 jours avant (modèle en page 3).',
        'Le concierge connaît les dates, les horaires et le nom du responsable du chantier.',
        'L\'accès est réglé : clés, badges, horaires d\'ouverture, présence nécessaire ou non des locataires.',
        'L\'ascenseur, les sols et les murs des parties communes seront protégés.',
        'Un emplacement est prévu pour le matériel et l\'évacuation des déchets.',
        'Le stationnement du véhicule de l\'entreprise est prévu.',
        'Vous avez le nom et le portable du responsable de chantier.',
    ])
    d.fin()


def k_p2(d: Doc):
    d.debut()
    k_section(d, 'Pendant les travaux', [
        'Les horaires annoncés sont respectés.',
        'La poussière est contenue : zones fermées, aspiration.',
        'Les passages restent libres et propres chaque soir.',
        'Les locataires savent qui appeler en cas de question.',
        'Tout imprévu est signalé avec son prix <b>avant</b> d\'être exécuté.',
        'Un point rapide est fait en fin de semaine (téléphone ou e-mail).',
        'Les éventuelles plaintes sont notées et traitées le jour même.',
    ])
    d.espace(11 * mm)
    k_section(d, 'Après les travaux', [
        'Le nettoyage final est fait.',
        'La réception a lieu avec l\'entreprise, avec un procès-verbal.',
        'Les retouches sont listées, avec un délai pour les lever.',
        'Des photos avant / après sont jointes au dossier, pour le propriétaire.',
        'La facture correspond à l\'offre, plus-values validées comprises.',
        'Les locataires sont informés de la fin des travaux.',
    ])
    d.espace(11 * mm)
    d.surtitre('Notes', couleur=ANTH, taille=10)
    d.espace(2 * mm)
    while d.y - 10 * mm > d.bas + 2 * mm:
        d.y -= 10 * mm
        d.filet(ML, W - MR, d.y, ACIER, 0.6)
    d.fin()


def k_p3(d: Doc):
    c = d.c
    d.debut()
    d.surtitre('Modèle d\'avis aux locataires', couleur=ANTH, taille=10)
    d.espace(1 * mm)
    d.para('À compléter, puis à afficher dans l\'immeuble et à remettre aux locataires concernés.', ST['corps12_g'])
    d.espace(5 * mm)
    ch = lambda t: f'<font name="Sans-It" color="#44494F">[{t}]</font>'
    pad = 9 * mm
    lw = CW - 2 * pad
    st = S('av', 'Sans', 12, 17)
    contenu = [
        ('<font name="Mont-700" size="16">Travaux dans votre immeuble</font>', S('avt', 'Mont-700', 16, 21), 6 * mm),
        ('Madame, Monsieur,', st, 4 * mm),
        (f'Des travaux de {ch("nature des travaux")} auront lieu dans l\'immeuble {ch("adresse")}, du {ch("date de début")} au {ch("date de fin")}.', st, 5 * mm),
        (f'<b>Où</b> : {ch("parties communes, étages, logements concernés")}', st, 2 * mm),
        (f'<b>Horaires</b> : du lundi au vendredi, de {ch("heure")} à {ch("heure")}', st, 2 * mm),
        (f'<b>Ce qui change pour vous</b> : {ch("accès, ascenseur, bruit, poussière, présence nécessaire dans le logement")}', st, 5 * mm),
        (f'L\'entreprise {ch("nom de l\'entreprise")} protège les parties communes et nettoie chaque soir. Pour toute question sur le chantier : {ch("nom du responsable")}, {ch("téléphone")}. Pour toute autre question : {ch("régie")}, {ch("téléphone de la régie")}.', st, 4 * mm),
        ('Nous vous remercions de votre compréhension.', st, 6 * mm),
        (f'{ch("Régie")}, le {ch("date")}', st, 0),
    ]
    hs = [d.hauteur(t, s, lw) for t, s, _ in contenu]
    hb = 2 * pad + sum(hs) + sum(a for _, _, a in contenu)
    y0 = d.y
    c.setStrokeColor(GRAPH)
    c.setLineWidth(0.9)
    c.setDash([4, 3], 0)
    c.rect(ML, y0 - hb, CW, hb, stroke=1, fill=0)
    c.setDash([], 0)
    d.y = y0 - pad
    for t, s, a in contenu:
        d.para(t, s, x=ML + pad, largeur=lw)
        d.y -= a
    d.y = y0 - hb - 10 * mm
    encadre(d, [('<b>Bon à savoir</b> : pendant des travaux de rénovation, le locataire peut, selon les cas, demander une '
                 'réduction de loyer (art. 259d et 260 du Code des obligations). Une information claire et des nuisances '
                 'limitées réduisent ce risque. <i>Information générale, qui ne remplace pas un conseil juridique.</i>',
                 ST['corps12'], 0)], largeur=CW)
    d.controle()
    d.fin()


# --------------------------------------------------------------------------------------------
# Finitions : langue du document, contrôle, aperçus
# --------------------------------------------------------------------------------------------

def finaliser(chemin: Path):
    """Ajoute la langue (fr-CH) et l'affichage du titre ; ne touche pas au contenu."""
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject, TextStringObject, DictionaryObject, BooleanObject
    r = PdfReader(str(chemin))
    w = PdfWriter(clone_from=r)
    w._root_object[NameObject('/Lang')] = TextStringObject('fr-CH')
    w._root_object[NameObject('/ViewerPreferences')] = DictionaryObject({NameObject('/DisplayDocTitle'): BooleanObject(True)})
    w.add_metadata({k: v for k, v in (r.metadata or {}).items()})
    w.compress_identical_objects()
    with open(chemin, 'wb') as f:
        w.write(f)


def rapport(chemin: Path):
    from pypdf import PdfReader
    r = PdfReader(str(chemin))
    polices = set()
    for p in r.pages:
        res = p.get('/Resources') or {}
        for f in (res.get('/Font') or {}).values():
            f = f.get_object()
            polices.add((str(f.get('/BaseFont')), '/FontFile2' in str(f.get('/DescendantFonts', [{}])[0].get_object().get('/FontDescriptor', {}).get_object()) if f.get('/DescendantFonts') else False))
    taille = chemin.stat().st_size
    print(f'  {chemin.relative_to(RACINE)} : {len(r.pages)} pages, {taille / 1024:.0f} Ko, titre « {r.metadata.title} », '
          f'auteur « {r.metadata.author} », polices {sorted(polices)}')
    return taille


def apercus(fichiers, dossier: Path, dpi=60):
    dossier.mkdir(parents=True, exist_ok=True)
    for f in fichiers:
        subprocess.run(['pdftoppm', '-png', '-r', str(dpi), str(f), str(dossier / f.stem)], check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--apercus', type=Path, help='dossier où écrire des aperçus PNG des pages (pdftoppm)')
    ap.add_argument('--dpi', type=int, default=60, help='résolution des aperçus')
    ap.add_argument('--date', help='date d\'édition AAAA-MM-JJ (défaut : aujourd\'hui)')
    ap.add_argument('--brouillon', action='store_true', help='signale les débordements sans s\'arrêter')
    a = ap.parse_args()
    global TOLERANT
    TOLERANT = a.brouillon
    date = dt.date.fromisoformat(a.date) if a.date else dt.date.today()

    conf = charger_confirmations(CONFIRMATIONS)
    valeurs = json.loads(VALEURS.read_text(encoding='utf-8'))
    logos = {l['id']: l for l in json.loads((IMG / 'references' / 'logos.json').read_text(encoding='utf-8'))}
    print('confirmations lues :', ', '.join(sorted(k for k, v in conf.items() if v)) or 'aucune',
          f'({CONFIRMATIONS.relative_to(RACINE)}{"" if CONFIRMATIONS.exists() else " absent"})')

    with tempfile.TemporaryDirectory() as tmp:
        cache = Path(tmp)
        enregistrer_polices(cache)
        styles()
        imgs = Images(cache)
        prod = Ctx('production', conf, valeurs, date)
        prev = Ctx('preview', conf, valeurs, date)
        sorties = [
            (DOCS_SITE / 'andy-construct-references.pdf', lambda f: plaquette(prod, f, logos, imgs)),
            (LIVRABLES / 'andy-construct-references-preview.pdf', lambda f: plaquette(prev, f, logos, imgs)),
            (DOCS_SITE / 'guide-reduire-le-bruit.pdf', lambda f: guide(prod, f)),
            (DOCS_SITE / 'checklist-chantier-site-occupe.pdf', lambda f: checklist(prod, f)),
        ]
        for f, fn in sorties:
            fn(f)
            finaliser(f)
        print('fichiers produits :')
        for f, _ in sorties:
            t = rapport(f)
            if t > 2.5 * 1024 * 1024:
                print('  ATTENTION : plus de 2,5 Mo')
    if a.apercus:
        apercus([f for f, _ in sorties], a.apercus, a.dpi)
        print('aperçus :', a.apercus)


if __name__ == '__main__':
    main()
