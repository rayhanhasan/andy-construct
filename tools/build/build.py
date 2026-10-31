# -*- coding: utf-8 -*-
"""Générateur du site Andy Construct (v2).

Usage, depuis la racine du dépôt :
    python3 tools/build/build.py [--mode preview|verification|production] [--out <dossier>]

- preview (défaut)  : textes définitifs, bandeau « version de validation », noindex ;
- verification      : idem, et les passages à confirmer sont soulignés en pointillé avec leur code (C01…) ;
- production        : textes de repli tant qu'un code n'est pas confirmé (donnees/confirmations.json),
                      logos « autorise » seulement, photos « retirer » exclues, indexable, sans bandeau.
--out : dossier de sortie (défaut : site/). Un autre dossier reçoit une copie complète du site (images, polices,
api sans config.php ni stockage/), prête à déployer.

Sources : ctx.py (modes, confirmations), common.py (NAP, gabarits), composants.py, portfolio.py, page_*.py,
seo.py (sitemap, robots, llms.txt, .htaccess), static/ (CSS et JS sources, minifiés et versionnés ici),
donnees/ (confirmations, config Umami, témoignages, avis). Préparation des images : images.py (à part).
"""
import argparse, hashlib, os, re, shutil, sys
sys.dont_write_bytecode = True
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import ctx


def args():
    a = argparse.ArgumentParser(description='Génère le site Andy Construct.')
    a.add_argument('--mode', choices=['preview', 'verification', 'production'], default='preview')
    a.add_argument('--production', action='store_true', help='raccourci pour --mode production')
    a.add_argument('--out', default=ctx.SITE)
    r = a.parse_args()
    if r.production:
        r.mode = 'production'
    return r


# ---------------------------------------------------------------- ressources
def min_css(s):
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\s*([{};,>])\s*', r'\1', s)
    return s.replace(';}', '}').strip() + '\n'


def min_js(src):
    """Minification prudente : commentaires et espaces retirés hors chaînes et expressions régulières.
    Un retour à la ligne est gardé là où l'insertion automatique de point-virgule pourrait en dépendre."""
    ident = lambda ch: ch.isalnum() or ch in '_$\\'
    out, i, n, esp, nl = [], 0, len(src), False, False
    dernier = lambda: out[-1][-1] if out else ''
    while i < n:
        c = src[i]
        if c in ' \t':
            esp, i = True, i + 1
            continue
        if c in '\r\n':
            nl, i = True, i + 1
            continue
        if src.startswith('//', i):
            i = src.find('\n', i)
            i = n if i < 0 else i
            continue
        if src.startswith('/*', i):
            i, esp = src.index('*/', i) + 2, True
            continue
        p = dernier()
        if esp or nl:
            if ident(p) and ident(c):
                out.append(' ')
            elif p in '+-' and c in '+-':
                out.append(' ')
            elif nl and p and p not in ';,{([=:?&|+-*/<>!' and c not in ';,})].:?&|+-*/<>=':
                out.append('\n')
            esp = nl = False
        if c in '\'"`':
            j = i + 1
            while src[j] != c:
                j += 2 if src[j] == '\\' else 1
            out.append(src[i:j + 1])
            i = j + 1
            continue
        if c == '/' and (p in '(,=:[!&|?{};+-*%<>~^' or p == '' or ''.join(out).endswith('return')):
            j, classe = i + 1, False
            while True:
                ch = src[j]
                if ch == '\\':
                    j += 2
                    continue
                if ch == '[':
                    classe = True
                elif ch == ']':
                    classe = False
                elif ch == '/' and not classe:
                    break
                j += 1
            j += 1
            while j < n and src[j].isalpha():
                j += 1
            out.append(src[i:j])
            i = j
            continue
        out.append(c)
        i += 1
    return ''.join(out) + '\n'


def empreinte(contenu):
    return hashlib.sha1(contenu.encode('utf-8') if isinstance(contenu, str) else contenu).hexdigest()[:10]


def ressources(out):
    import common, composants
    css = open(os.path.join(ICI, 'static/styles.css'), encoding='utf-8').read() + '\n/* échelles des logos (logos.json) */\n' + composants.echelles()
    css = min_css(css)
    js = min_js(open(os.path.join(ICI, 'static/main.js'), encoding='utf-8').read())
    suivi = open(os.path.join(ctx.SITE, 'assets/js/suivi.js'), 'rb').read()
    os.makedirs(os.path.join(out, 'assets/css'), exist_ok=True)
    os.makedirs(os.path.join(out, 'assets/js'), exist_ok=True)
    open(os.path.join(out, 'assets/css/styles.css'), 'w', encoding='utf-8').write(css)
    open(os.path.join(out, 'assets/js/main.js'), 'w', encoding='utf-8').write(js)
    if os.path.abspath(out) != os.path.abspath(ctx.SITE):
        open(os.path.join(out, 'assets/js/suivi.js'), 'wb').write(suivi)
    common.ASSETS.update(css='assets/css/styles.css?v=' + empreinte(css), js='assets/js/main.js?v=' + empreinte(js),
                         suivi='assets/js/suivi.js?v=' + empreinte(suivi))
    print('  styles.css %.1f Ko · main.js %.1f Ko · suivi.js %.1f Ko' % (len(css.encode()) / 1024, len(js.encode()) / 1024, len(suivi) / 1024))
    return len(css.encode()), len(js.encode()) + len(suivi)


def copier_site(out, mode):
    """Copie site/ vers un autre dossier (HTML et fichiers générés exclus, secrets jamais copiés)."""
    import composants, portfolio
    exclus_logos = set()
    exclus_photos = set()
    if mode == 'production':
        for rid, l in composants.LOGOS.items():
            if not composants.logo_affiche(rid):
                exclus_logos.update(x for x in (l.get('fichier'), l.get('fichier_blanc')) if x)
        exclus_photos = set(portfolio.RETIREES) | {pid for pid in portfolio.PHOTOS if not portfolio.photo_ok(pid)}
    for dossier, sous, fichiers in os.walk(ctx.SITE):
        rel = os.path.relpath(dossier, ctx.SITE)
        if rel == 'api/stockage' or rel.startswith('api/stockage' + os.sep):
            sous[:] = []
            continue
        sous[:] = [d for d in sous if not (rel == 'api' and d == 'stockage')]
        for f in fichiers:
            r = os.path.normpath(os.path.join(rel, f))
            if rel == '.' and (f.endswith('.html') or f in ('sitemap.xml', 'robots.txt', 'llms.txt', '.htaccess')):
                continue
            if r in ('api/config.php', 'assets/css/styles.css', 'assets/js/main.js', 'assets/js/suivi.js') or f == '.DS_Store':
                continue
            if rel == os.path.join('assets', 'img', 'references') and f in exclus_logos:
                continue
            if rel == os.path.join('assets', 'img', 'portfolio') and any(f.startswith(pid + '-') for pid in exclus_photos):
                continue
            os.makedirs(os.path.join(out, rel), exist_ok=True)
            shutil.copy2(os.path.join(dossier, f), os.path.join(out, r))


# ---------------------------------------------------------------- contrôles
INTERDITS = ['300+', 'Sàrl', 'Genève et Vaud', 'Devis gratuit', 'Ils nous ont fait confiance', 'nos partenaires', 'Nos partenaires',
             'Régie immobilière, Genève', 'Architecte, Carouge', 'Propriétaire, Vésenaz', 'Maquette de présentation']


def controles(out, mode):
    erreurs = []
    pages = {f: open(os.path.join(out, f), encoding='utf-8').read() for f in os.listdir(out) if f.endswith('.html')}
    ids = {f: set(re.findall(r'\sid="([^"]+)"', t)) for f, t in pages.items()}
    for f, t in pages.items():
        for mot in INTERDITS:
            if mot in t:
                erreurs.append('%s : « %s »' % (f, mot))
        corps = t.split('<body', 1)[-1]
        for url in re.findall(r'(?:href|src)="([^"]+)"', t) + [u.split()[0] for s in re.findall(r'srcset="([^"]+)"', t) for u in s.split(',')]:
            if re.match(r'^(https?:|mailto:|tel:|data:|//)', url):
                continue
            chemin, _, ancre = url.partition('#')
            chemin = chemin.split('?')[0]
            cible = chemin or f
            if chemin and not os.path.exists(os.path.join(out, chemin)):
                erreurs.append('%s : lien cassé %s' % (f, url))
            elif ancre and cible.endswith('.html') and cible in ids and ancre not in ids[cible]:
                erreurs.append('%s : ancre absente %s' % (f, url))
        if len(re.findall(r'<h1[ >]', corps)) != 1 and f != 'merci.html' and f != 'prestations.html':
            erreurs.append('%s : %d titres H1' % (f, len(re.findall(r'<h1[ >]', corps))))
        if 'style="' in corps:
            erreurs.append('%s : attribut style (bloqué par la CSP)' % f)
        if mode == 'production' and 'class="vc"' in t:
            erreurs.append('%s : marque de vérification en production' % f)
    if erreurs:
        print('\n'.join('  ERREUR ' + x for x in erreurs))
        raise SystemExit(1)
    print('  contrôles : %d pages, liens et ancres internes valides, aucun texte interdit' % len(pages))


def main():
    r = args()
    out = os.path.abspath(r.out)
    os.makedirs(out, exist_ok=True)
    ctx.regler(r.mode, out)
    print('Génération %s → %s' % (r.mode, out))
    if out != os.path.abspath(ctx.SITE):
        copier_site(out, r.mode)
    taille_css, taille_js = ressources(out)
    if taille_css > 50 * 1024 or taille_js > 25 * 1024:
        raise SystemExit('Budget dépassé : CSS %d o (max 50 Ko), JS %d o (max 25 Ko)' % (taille_css, taille_js))
    import page_accueil, page_services, page_realisations, page_professionnels, page_entreprise, page_contact, page_autres, seo
    page_accueil.build()
    page_services.build()
    page_realisations.build()
    page_professionnels.build()
    page_entreprise.build()
    page_contact.build()
    page_autres.build()
    seo.build()
    controles(out, r.mode)
    print('Terminé.')


if __name__ == '__main__':
    main()
