# -*- coding: utf-8 -*-
"""Export complet du site pour travailler en local.

    python3 tools/export/export_local.py [--out livrables/andy-construct-local]

- génère le site (mode verification) dans <out>/site, avec images, polices, vidéos, API et admin ;
- retire le bandeau de validation, les commentaires de génération et le fichier llms.txt ;
- remplace chaque passage qui attend une information du client (codes Cxx, sauf GARDER) par du lorem ipsum
  de longueur proche, et liste ces passages page par page dans <out>/a-remplir.json ;
- écrit api/config.php pour un serveur local (mode test : aucun e-mail ni webhook réel).
"""
import argparse, json, os, re, secrets, shutil, subprocess, sys

ICI = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(ICI))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'build'))
sys.path.insert(0, ICI)
import ctx  # noqa: E402

LOREM = ('lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore '
         'magna aliqua ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo '
         'consequat duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla '
         'pariatur excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id '
         'est laborum').split()


class Lorem:
    def __init__(self):
        self.i = 0

    def texte(self, modele):
        """Lorem de longueur proche de `modele`, majuscule et ponctuation finale reprises."""
        coeur = modele.strip()
        if not coeur:
            return modele
        cible = max(len(coeur), 5)
        mots = []
        while len(' '.join(mots)) < cible:
            mots.append(LOREM[self.i % len(LOREM)])
            self.i += 1
        if len(mots) > 1 and len(' '.join(mots)) - cible > 6:
            mots.pop()
        s = ' '.join(mots)
        if coeur[0].isupper() or coeur[0].isdigit():
            s = s[0].upper() + s[1:]
        fin = re.search(r'[.:;!?…»)]+$', coeur)
        if fin:
            s += fin.group(0)
        debut = modele[:len(modele) - len(modele.lstrip())]
        finale = modele[len(modele.rstrip()):]
        return debut + s + finale


# Codes gardés tels quels : faits publics (registre, IDE, adresse e-mail, carte), choix de nom (C16), textes juridiques.
GARDER = {'C10', 'C16', 'C21', 'C30', 'C34', 'C35', 'V01', 'V02'}

VC = re.compile(r'<(span|div) class="vc">((?:(?!class="vc").)*?)<sup class="vc__code">([^<]*)</sup></\1>', re.S)
VBAR = re.compile(r'\s*<div class="vbar" role="region".*?<button type="button" class="vbar__close">.*?</button>\s*</div>\s*</div>', re.S)


def traiter_page(chemin, lorem):
    s = open(chemin, encoding='utf-8').read()
    s = re.sub(r'<!-- Généré par tools/build[^>]*-->\n?', '', s)
    s = VBAR.sub('', s, count=1)
    trouves = []

    def remplace(m):
        contenu, codes = m.group(2), m.group(3).split()
        if set(codes) <= GARDER:
            return contenu
        original = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', contenu)).strip()
        trouves.append({'codes': codes, 'texte': original})
        # seuls les nœuds texte changent : liens, gras et icônes restent en place
        return re.sub(r'>([^<]+)<', lambda t: '>' + lorem.texte(t.group(1)) + '<', '>' + contenu + '<')[1:-1]

    while True:
        s2 = VC.sub(remplace, s)
        if s2 == s:
            break
        s = s2
    open(chemin, 'w', encoding='utf-8').write(s)
    return trouves


CONFIG_LOCAL = """<?php
// Configuration LOCALE (générée par tools/export/export_local.py).
// Mode test : aucun e-mail ni webhook réel ; tout est écrit dans api/stockage/.
declare(strict_types=1);
$base = require __DIR__ . '/config.example.php';
return array_replace_recursive($base, [
    'mode_test' => true,
    'url_site' => 'http://localhost:8000',
    'url_api' => 'http://localhost:8000/api',
    'origines_autorisees' => ['http://localhost:8000', 'http://127.0.0.1:8000'],
    'stockage' => __DIR__ . '/stockage',
    'secrets' => ['hmac_webhook' => '%s', 'actions' => '%s', 'local' => '%s', 'admin' => '%s'],
    'smtp' => ['actif' => false],
    'n8n' => ['simuler' => true],
    'pages' => ['merci_devis' => '/merci.html', 'merci_rappel' => '/merci.html', 'merci_envoi_postal_guide' => '/merci.html'],
    'admin' => ['url' => 'http://localhost:8000/admin'],
]);
"""


LISEZMOI = """ANDY CONSTRUCT - SITE EN LOCAL

1. Voir le site : ouvrir site/index.html dans le navigateur.
2. Tester les formulaires (PHP 8.1+) : dans le dossier site/, lancer
       php -S localhost:8000
   puis ouvrir http://localhost:8000
   Mode test : aucun e-mail n'est envoye. Les demandes arrivent dans
   site/api/stockage/ (e-mails .eml + base SQLite).
3. Espace prive /admin/ : creer un compte avec
       php site/admin/outils/creer-utilisateur.php --email=vous@exemple.ch --nom="Votre Nom" --role=associe --role-metier=bureau
4. GUIDE-DES-PAGES.html : a ouvrir sur le deuxieme ecran.
   Lorem ipsum = information a obtenir du client (liste dans le guide et a-remplir.json).
"""


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--out', default=os.path.join(ROOT, 'livrables', 'andy-construct-local'))
    out = os.path.abspath(a.parse_args().out)
    site = os.path.join(out, 'site')
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'build', 'build.py'), '--mode', 'verification',
                    '--out', site], check=True, stdout=subprocess.DEVNULL)
    for f in ('llms.txt',):
        p = os.path.join(site, f)
        if os.path.exists(p):
            os.remove(p)
    lorem, rapport = Lorem(), {}
    for f in sorted(os.listdir(site)):
        if f.endswith('.html'):
            rapport[f] = traiter_page(os.path.join(site, f), lorem)
    # contrôle : plus aucune trace du mode validation
    for f in rapport:
        s = open(os.path.join(site, f), encoding='utf-8').read()
        assert 'class="vc"' not in s and 'class="vbar"' not in s and 'Généré par' not in s, f
    api = os.path.join(site, 'api')
    open(os.path.join(api, 'config.php'), 'w', encoding='utf-8').write(
        CONFIG_LOCAL % tuple(secrets.token_hex(32) for _ in range(4)))
    os.makedirs(os.path.join(api, 'stockage'), exist_ok=True)
    resume = {f: [{'question': ' / '.join(ctx.QUESTIONS.get(c, c) for c in p['codes']), 'codes': p['codes'],
                   'texte_propose': p['texte']} for p in v] for f, v in rapport.items()}
    json.dump(resume, open(os.path.join(out, 'a-remplir.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    import guide
    guide.generer(out, resume)
    open(os.path.join(out, 'LISEZMOI.txt'), 'w', encoding='utf-8').write(LISEZMOI)
    n = sum(len(v) for v in rapport.values())
    print('%s : %d passages en lorem ipsum sur %d pages' % (out, n, len(rapport)))


if __name__ == '__main__':
    main()
