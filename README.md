# Andy Construct — maquette du nouveau site

Maquette de refonte du site d'**Andy Construct** (plafonds, cloisons, isolation, peinture, Genève et Vaud), préparée par Harbor Digital pour présentation au client.

## Contenu du dépôt

| Dossier | Rôle |
|---|---|
| `site/` | Le site statique, prêt à déposer sur un hébergement (HTML, CSS, JS natifs, aucune dépendance, aucun appel externe) |
| `docs/brief-design.md` | Charte graphique dérivée du logo et règles d'ergonomie (public senior, BTP) |
| `docs/analyse-marche.md` | Analyse de marché, concurrence, leviers SEO local et GEO, plan 30/90/180 jours |
| `docs/brief-seo.md` | Brief SEO/GEO opérationnel (titles, FAQ, JSON-LD, `llms.txt`, redirections) |
| `docs/justification.md` | Pourquoi ce site est un bon site : argumentaire pour le client |
| `docs/contenus-a-valider.md` | Tous les contenus provisoires à faire confirmer par le client |
| `docs/selection-photos.md` | Photos retenues ou écartées, et conseils pour les prochaines prises de vue |
| `docs/source/` | Sources : contenu de l'ancien site, logo original, ancien logo 2016 (archivé), démo de référence |
| `deploy/deploy_ftp.py` | Envoi FTP limité au dossier `res/` de harbor-digital.fr |

## Voir la maquette en local

```bash
cd site && python3 -m http.server 8080
# puis ouvrir http://localhost:8080
```

## Déployer sur harbor-digital.fr/res

Le script n'écrit **que** dans le dossier distant `res/` (tout autre chemin est refusé) et n'efface aucun fichier. Les identifiants se passent par variables d'environnement et ne sont jamais écrits dans le dépôt.

```bash
export FTP_HOST=46.202.172.2 FTP_USER='…' FTP_PASS='…'
python3 deploy/deploy_ftp.py --dry-run   # affiche ce qui serait envoyé
python3 deploy/deploy_ftp.py             # dépose le site dans res/andy-construct/
```

La maquette est alors visible sur `https://harbor-digital.fr/res/andy-construct/`.
Si le dossier `res` n'est pas trouvé automatiquement, indiquez son chemin : `export FTP_REMOTE_RES=/chemin/vers/res`.

## Avant la mise en production (sur andyconstruct.ch)

1. Faire valider chaque ligne de `docs/contenus-a-valider.md` et supprimer les commentaires `<!-- PROVISOIRE … -->`.
2. Retirer le bandeau « Maquette de présentation » (`.mockup-notice`) de chaque page.
3. Retirer `<meta name="robots" content="noindex, nofollow">` de chaque page.
4. Brancher le formulaire de contact : script PHP de l'hébergeur ou service de formulaires conforme à la nLPD.
5. Mettre en place les redirections 301 des anciennes adresses Joomla (voir `docs/brief-seo.md`, §8.3).
6. Créer ou revendiquer la fiche Google Business Profile et aligner local.ch et search.ch sur les mêmes nom, adresse et téléphone.
