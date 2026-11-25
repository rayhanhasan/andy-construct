# -*- coding: utf-8 -*-
"""Paquet prêt à héberger : le site généré, nettoyé de toute trace de l'atelier de fabrication.

    python3 tools/export/export_hebergement.py [--out livrables]

Produit deux archives :
- andy-construct-site-test.zip        version de test (non indexée par Google), à poser sur un serveur de recette ;
- andy-construct-site-production.zip  version pour le domaine définitif (indexable ; seuls les éléments confirmés).

Nettoyage : commentaires HTML de génération, renvois aux documents internes dans les commentaires
(PHP, CSS, JS, .htaccess, JSON), fichier llms.txt ; ni tests, ni outils de démonstration, ni configuration réelle,
ni données de stockage. Le code reste lisible et commenté, sans ces renvois.
"""
import argparse, os, re, shutil, subprocess, sys, zipfile

ICI = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(ICI))
TEXTE = ('.php', '.css', '.js', '.json', '.html', '.txt', '.xml', '.htaccess', '.webmanifest')
EXCLUS_DOSSIERS = ('api/tests', 'admin/tests', 'api/stockage', 'admin/outils/demo.php')
EXCLUS_FICHIERS = {'api/config.php', 'llms.txt'}

LIGNES_A_RETIRER = [
    r'^\s*\*\s*(Plan|Contrat complet|Toute la documentation|Modèle)\s*:.*docs/.*\n',
]
REMPLACEMENTS = [
    (r'<!-- Généré par tools/build[^>]*-->\n?', ''),
    (r' \(généré par tools/build, mode \w+\)', ''),
    (r'  # Umami : renseigner umami_src et umami_id dans tools/build/donnees/config\.json, puis regénérer\.',
     '  # Statistiques Umami : ajouter l\'adresse du script à script-src et connect-src.'),
    (r' Contrat : docs/v2/contrat-interface\.md §12', ''),
    (r' \* docs/v2/contrat-interface\.md \(le frontend envoie exactement ces valeurs\)\.',
     ' * le formulaire du site, qui envoie exactement ces valeurs.'),
    (r', repris de la maquette\n \* docs/v4/admin/maquette/\. ', '.\n * '),
    (r' \(repris de la maquette docs/v4/admin/maquette/\)', ''),
    (r'\s*\([^()\n]*(?:docs/|§|décision D\d)[^()\n]*\)', ''),
    (r', décision D\d', ''),
    (r'docs/v\d[\w./-]*(?: ?§[\d.]+(?: a §[\d.]+)?)?', ''),
]
CONTROLES = ['docs/v', 'tools/build', 'décision D', 'copy deck', 'cro-v3', 'Claude', 'Anthropic', 'ChatGPT', 'OpenAI']


INSTALLATION = """ANDY CONSTRUCT - MISE EN LIGNE DU SITE
Version : %s

1. Hébergement requis
   PHP 8.1 ou plus, Apache ou LiteSpeed (fichiers .htaccess), HTTPS.
   Base de données : SQLite par défaut (rien à installer) ; MariaDB possible (clé « base » de la configuration).

2. Copier les fichiers
   Envoyer le contenu du dossier andy-construct/ à la racine du site (souvent public_html/),
   fichiers cachés compris (.htaccess). Les liens sont relatifs : un sous-dossier convient pour un test.

3. Configurer les formulaires
   Copier api/config.example.php en api/config.php et remplir les valeurs « À REMPLIR » :
   serveur d'envoi des e-mails (SMTP), adresses de réception, secrets.
   Générer chaque secret avec : php -r 'echo bin2hex(random_bytes(32)), PHP_EOL;'
   En ligne pour de bon : « mode_test » => false.
   Le dossier api/stockage/ doit être accessible en écriture par PHP (ou indiquer un dossier hors de la racine web).

4. Espace privé /admin/
   Créer le premier compte en ligne de commande :
   php admin/outils/creer-utilisateur.php --email=prenom@andyconstruct.ch --nom="Prénom Nom" --role=associe --role-metier=bureau
   Garder la clé de double authentification et les codes de secours affichés.

5. Tâche planifiée
   Toutes les 10 minutes : php /chemin/vers/le/site/api/cron.php
   (file d'attente des envois, nettoyage des fichiers reçus).

6. Vérifier
   - envoyer une demande de devis de test et contrôler sa réception ;
   - ouvrir une ancienne adresse (ex. /index.php/presentation) : elle doit rediriger vers la nouvelle page ;
   - version production : déclarer le sitemap (https://www.andyconstruct.ch/sitemap.xml) dans Google Search Console.

Conception et réalisation : Harbor Digital.
"""


def exclu(rel):
    return rel in EXCLUS_FICHIERS or any(rel == d or rel.startswith(d + '/') for d in EXCLUS_DOSSIERS) \
        or '/__pycache__/' in '/' + rel + '/' or rel.endswith('.DS_Store')


def nettoyer(texte):
    for motif in LIGNES_A_RETIRER:
        texte = re.sub(motif, '', texte, flags=re.M)
    for motif, rempl in REMPLACEMENTS:
        texte = re.sub(motif, rempl, texte)
    return texte


def paquet(mode, sortie, travail):
    dossier = os.path.join(travail, mode)
    if os.path.exists(dossier):
        shutil.rmtree(dossier)
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'build', 'build.py'), '--mode', mode, '--out', dossier],
                   check=True, stdout=subprocess.DEVNULL)
    restes, php = [], []
    with zipfile.ZipFile(sortie, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for racine, dossiers, fichiers in os.walk(dossier):
            dossiers.sort()
            for f in sorted(fichiers):
                chemin = os.path.join(racine, f)
                rel = os.path.relpath(chemin, dossier).replace(os.sep, '/')
                if exclu(rel):
                    continue
                if f.endswith(TEXTE) or f == '.htaccess':
                    t = open(chemin, encoding='utf-8').read()
                    if '/vendor/' not in '/' + rel:
                        t = nettoyer(t)
                        restes += ['%s : %s' % (rel, m) for m in CONTROLES if m in t]
                        open(chemin, 'w', encoding='utf-8').write(t)
                    if f.endswith('.php'):
                        php.append(chemin)
                z.write(chemin, 'andy-construct/' + rel)
        z.writestr('andy-construct/api/stockage/.htaccess', 'Require all denied\n')
        z.writestr('INSTALLATION.txt', INSTALLATION % ('TEST (non indexée par Google, pour la recette)' if mode == 'preview'
                                                       else 'PRODUCTION (indexable, pour le domaine définitif)'))
    for p in php:
        r = subprocess.run(['php', '-l', p], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit('Erreur de syntaxe après nettoyage : %s\n%s' % (p, r.stdout + r.stderr))
    if restes:
        raise SystemExit('Traces restantes :\n' + '\n'.join(restes))
    print('%s : %d Ko' % (sortie, os.path.getsize(sortie) // 1024))


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--out', default=os.path.join(ROOT, 'livrables'))
    a.add_argument('--travail', default=os.path.join(ROOT, '.export-hebergement'))
    r = a.parse_args()
    os.makedirs(r.out, exist_ok=True)
    paquet('preview', os.path.join(r.out, 'andy-construct-site-test.zip'), r.travail)
    paquet('production', os.path.join(r.out, 'andy-construct-site-production.zip'), r.travail)
    shutil.rmtree(r.travail, ignore_errors=True)


if __name__ == '__main__':
    main()
