# HANDOFF — Projet maquette Andy Construct

Document de passation pour reprendre le projet en local (Claude Code CLI ou à la main).
Dernière mise à jour : 6 octobre 2026. État : **maquette livrée, en attente de validation client**.

---

## 1. Démarrage rapide

```bash
git clone https://github.com/rayhanhasan/andy-construct.git
cd andy-construct
git checkout claude/eager-heisenberg-sz3nve

# Voir le site
cd site && python3 -m http.server 8080      # http://localhost:8080

# Régénérer le site après modification des sources (depuis la racine)
python3 tools/build/build.py
```

Prérequis : Python 3.10+ (aucune dépendance pour générer le site). Pour les scripts photos/carte : `pip install pillow`. Pour les captures : Node 18+ et `npx playwright` (Chromium).

Pour reprendre avec Claude Code en local, ouvrir le dépôt et donner ce message :

> Lis HANDOFF.md, README.md et docs/brief-design.md. Tu es chef de projet sur la maquette Andy Construct. Reprends à la section « Prochaines étapes ».

---

## 2. Dépôt et branches

| Élément | Valeur |
|---|---|
| Dépôt GitHub | `rayhanhasan/andy-construct` |
| Branche de travail | `claude/eager-heisenberg-sz3nve` (tout est poussé ici) |
| Branche par défaut | aucune autre branche ; pas de pull request ouverte |
| Commit de référence | `471f3b6` « Recentre le site sur 4 services et la Suisse romande… » (+ ce HANDOFF) |

Aucun identifiant n'est stocké dans le dépôt (vérifié). `.gitignore` exclut `.env`, `node_modules`, `__pycache__`.

---

## 3. Le client et le contexte

**Agence** : Harbor Digital (harbor-digital.fr). **Client** : Andy Construct.

Identité vérifiée au registre du commerce (Zefix / [Moneyhouse](https://www.moneyhouse.ch/en/company/andy-construct-chanton-cie-3813590051)) :

| Champ | Valeur |
|---|---|
| Raison sociale | Andy Construct, Chanton & Cie — **société en nom collectif** (pas Sàrl) |
| Nom commercial | Andy Construct |
| Siège | Route des Acacias 48, 1227 Carouge (GE) depuis le 02.05.2023 |
| Ancienne adresse | Avenue de Bel-Air 57, 1225 Chêne-Bourg (affichée sur l'ancien site, plus utilisée) |
| Inscription RC | 27.06.2007 (l'ancien site disait 2010) |
| IDE | CHE-113.706.162 |
| Associés | Adnan Bajrami, Caroline Chanton Bajrami (nommés seulement dans les mentions légales) |
| Téléphones | +41 22 771 20 15 (fixe, mis en avant) · +41 78 631 14 34 (mobile) |
| E-mail | andy.construct@bluewin.ch (recommandé : contact@andyconstruct.ch) |
| Facebook | facebook.com/andyconstruct.bajrami |
| Ancien site | https://www.andyconstruct.ch (Joomla, © 2010-2022) |

**Services (validés par le client, 4 seulement)** : Placo · Peinture · Isolation acoustique · Cloisons isothermes.
**Zone (validée par le client)** : toute la Suisse romande (GE, VD, NE, FR, Valais romand, JU + Jura bernois).
**Audience** : 45-70 ans, BTP (régies, architectes, communes, propriétaires), déteste l'extravagant.

**Références publiques** (reprises de l'ancien site, en texte, sans logos) : Ville de Genève, Salle communale de Collonge-Bellerive, Piaget, Conservatoire de Musique de Genève, Salle de l'Alhambra, Mairie de Plan-les-Ouates, Laboratoire Covance CLS SA, De Grisogono, Energestion Ingénieurs & Architectes SIA, Domaine des Perrières (Coppet), Dipan SA (Nyon), HEAD Genève, OMC, Celgene, Bank Sarasin (auj. J. Safra Sarasin), UBS, Hôtel de Chavannes-de-Bogis, Harmonie Nautique de Genève.

---

## 4. Demande initiale (résumé fidèle)

1. Refaire « au propre » le site démo `harbor-digital.fr/res/index2.html` (template Webflow « Roofinger » de Webestica) en retirant l'inutile et en adaptant la DA à la société.
2. DA conforme au logo, **sobre** (public âgé, BTP), mettre en avant expertise, professionnalisme, entreprise **suisse, locale, engagée, expérimentée**.
3. Portfolio avec les photos pertinentes de l'ancien site (95 fournies, 30 retenues).
4. Analyse de marché : points d'impact les plus forts et potentiel (SEO local, GEO…).
5. Justifier en quoi le site est bon (structure, portfolio, preuve sociale…).
6. Rôle de Claude : chef de projet, sous-traitance à des agents, contrôle de conformité charte.
7. Chiffres inconnus : valeurs provisoires signalées.
8. **Règle serveur** : n'écrire que dans `harbor-digital.fr/res`, aucun accès aux autres fichiers.
9. Skills demandés : `/frontend-design`, `/seo` → **non installés** sur le compte ; leurs principes ont été appliqués via les briefs.

Demandes ultérieures : nouveau logo rouge (remplace l'ancien bleu) ; services réduits à 4 ; zone = Suisse romande ; carte avec le logo marquant les zones.

---

## 5. Architecture du dépôt

```
andy-construct/
├── HANDOFF.md                 ← ce fichier
├── README.md                  ← aperçu, déploiement, check-list production
├── site/                      ← SITE LIVRABLE (statique, généré — ne pas éditer à la main)
│   ├── index.html  prestations.html  realisations.html  contact.html
│   ├── mentions-legales.html  404.html
│   ├── robots.txt  sitemap.xml  llms.txt  site.webmanifest  favicon.ico
│   └── assets/
│       ├── css/styles.css     (~40 Ko, variables CSS en tête)
│       ├── js/main.js         (~11 Ko, vanilla : menu, galerie/filtres, lightbox <dialog>, formulaire, champ fichier)
│       ├── fonts/             (Montserrat 600/700, Source Sans 3 400/600/400i, woff2 + licences OFL)
│       └── img/
│           ├── brand/         (logo-andy-construct[.png|.webp] = fond clair ; -blanc = fond sombre ; favicons « A »)
│           ├── portfolio/     (30 photos × -1600.webp/-800.webp/-800.jpg, hero en -2400.webp, manifest.json)
│           └── og-andy-construct.jpg
├── tools/build/               ← GÉNÉRATEUR (source de vérité du HTML)
│   ├── build.py               point d'entrée : python3 tools/build/build.py
│   ├── common.py              gabarit (head, en-tête, pied, NAP, JSON-LD communs)
│   ├── content.py             contenus partagés (coordonnées, services, références)
│   ├── faq.json               questions fréquentes (texte visible + FAQPage)
│   ├── icons.py               pictogrammes SVG
│   ├── page_index.py  page_prestations.py  page_realisations.py  page_autres.py
│   ├── carte.py               carte SVG Suisse romande (marqueurs « A », cartouche logo)
│   ├── carte_donnees.py       extraction des limites cantonales → data/
│   └── data/suisse-occidentale.json + LICENSE-swiss-maps.txt (swisstopo/OFS via npm swiss-maps, BSD)
├── deploy/deploy_ftp.py       ← envoi FTP verrouillé sur res/ (identifiants par variables d'env.)
└── docs/
    ├── brief-design.md        charte (couleurs, typo, motif, accessibilité, ton) — non négociable
    ├── brief-seo.md           titles, meta, FAQ, JSON-LD, llms.txt, redirections 301, recette SEO
    ├── analyse-marche.md      marché, 8 concurrents, diagnostic ancien site, matrice 12 leviers, GEO, plan 30/90/180 j
    ├── justification.md       argumentaire client (3 visiteurs types, 9 piliers, tableau de suivi)
    ├── contenus-a-valider.md  TOUTES les questions au client (bloquant avant production)
    ├── selection-photos.md    photos retenues/écartées + conseils prises de vue
    └── source/                ancien site (HTML), démo Roofinger, logo original (.webp), ancien logo bleu archivé
```

**Principes techniques** : HTML/CSS/JS natifs, aucune dépendance runtime, aucun appel externe (pas de Google Fonts ni Maps embarqué → nLPD), chemins relatifs (site servi depuis un sous-dossier), `noindex, nofollow` sur toutes les pages tant que c'est une maquette, canonical vers `https://www.andyconstruct.ch/…`, contenus provisoires entourés de `<!-- PROVISOIRE : … -->`, bandeau `.mockup-notice` en haut de chaque page.

**Pourquoi un code réécrit** : le template Roofinger est sous licence commerciale ; seule sa **structure** a été reprise. Question ouverte au client (voir §9).

---

## 6. Charte graphique (résumé — détail dans docs/brief-design.md)

| Rôle | Valeur |
|---|---|
| Rouge Andy (boutons, marqueurs) | `#E8000F` |
| Rouge profond (survol, liens sur clair) | `#C4000D` |
| Anthracite (titres, pied, voile héro) | `#1D1F22` |
| Graphite (texte secondaire) | `#44494F` |
| Acier (texte sur sombre) | `#B9BDC2` |
| Brume (fond alterné) / Trait | `#F4F4F5` / `#E2E3E5` |

Règles : le rouge ponctue, jamais de grande surface rouge ; aucune autre teinte ; titres Montserrat 700, surtitres Montserrat 600 capitales espacées 0.18em, texte Source Sans 3 18 px ; motif unique = trait oblique rouge (biseau du « A ») ; croix suisse uniquement dans le logo ; zones cliquables ≥ 48 px ; aucun texte < 16 px ; pas d'animation, carrousel, pop-up.

---

## 7. Livrables et liens

| Livrable | Où |
|---|---|
| Site maquette | `site/` (dépôt) — .zip envoyé dans la conversation (`andy-construct-maquette.zip`, ~5 Mo) |
| Dossier de présentation client | https://claude.ai/artifact/44SM63Pk6NFCuvZV77ZdFq (privé : le partager via son menu « Partager ») |
| Analyse de marché / SEO / justification | `docs/` |

**Mise en ligne de la maquette** : **pas encore faite**. Le FTP (port 21 vers 46.202.172.2) était bloqué depuis l'environnement cloud. En local :

```bash
export FTP_HOST=46.202.172.2 FTP_USER='u578747026.harbor-digital.fr' FTP_PASS='<nouveau mot de passe>'
python3 deploy/deploy_ftp.py --dry-run
python3 deploy/deploy_ftp.py        # → res/andy-construct/  (n'écrase pas index2.html, n'efface rien)
```
Ou : décompresser le .zip dans `res/andy-construct/` via le gestionnaire de fichiers Hostinger.
⚠️ Le mot de passe FTP a circulé dans la conversation : **le changer** (prévu par le client).

---

## 8. Méthode de travail utilisée (agents)

Chef de projet (Claude principal) + agents spécialisés, tous via l'outil Agent :
1. **Analyste marché / SEO / GEO** → `analyse-marche.md`, `brief-seo.md` (recherche web, sources citées, aucun chiffre inventé).
2. **Photos** → tri 95 → 30, export WebP/JPG sans EXIF/GPS, `manifest.json`, `selection-photos.md`.
3. **Frontend** → générateur `tools/build/`, 6 pages, intégration photos/SEO, carte ; vérif Playwright (360→1440 px, console, liens, débordement).
4. **Rédacteur** → `justification.md`.
Contrôle qualité par le chef de projet sur captures à chaque itération (héro trop sombre, tailles de texte, champ fichier en anglais, textes internes, etc. — tous corrigés).

Skills Claude utilisés : `artifact-design` (dossier de présentation). Skills demandés mais absents : `/frontend-design`, `/seo` (à installer si souhaité, puis repasser le site dessus).

---

## 9. Décisions en attente du client (bloquant production)

Liste complète dans `docs/contenus-a-valider.md`. Les principales :

1. **Identité** : afficher Carouge / société en nom collectif / 2007 (choix actuel, conforme au registre) ?
2. **Template Roofinger** : l'agence a-t-elle la licence, et faut-il en garder l'apparence ou la structure suffit-elle ? (structure seule actuellement)
3. **Logo** : valider la variante « CONSTRUCT » anthracite (fonds clairs) et le favicon « A » rouge.
4. **Photos hors services** : plusieurs photos (dont **le héro**) montrent des plafonds lumineux/tendus, plus proposés → garder comme réalisations ou retirer (et choisir un nouveau héro).
5. **Aucune photo de peinture** → en fournir 3-4 (et ajouter le filtre « Peinture » à la galerie).
6. Chiffres provisoires : « 300+ chantiers », horaires lu-ve 7 h-18 h, « devis gratuit », méthode/engagements.
7. Témoignages : les 3 affichés sont **fictifs** (profils génériques) → 2-3 vrais avec accord écrit, sinon retirer la section.
8. Accord pour citer les marques privées des références, et année de chaque chantier.
9. E-mail sur le domaine, numéro principal, accord des personnes visibles sur les photos.

---

## 10. Prochaines étapes

**Immédiat**
- [ ] Changer le mot de passe FTP, puis déployer la maquette dans `res/andy-construct/` et vérifier en ligne (desktop + mobile).
- [ ] Partager le dossier de présentation avec le client ; recueillir les réponses de `contenus-a-valider.md`.

**Après validation client** (modifier `tools/build/`, puis `python3 tools/build/build.py`)
- [ ] Appliquer les réponses, retirer les commentaires `PROVISOIRE`, remplacer/retirer témoignages, photos hors services, héro si besoin.
- [ ] Ajouter photos peinture + filtre galerie ; fiches projets datées (références).
- [ ] Mettre à jour le dossier de présentation si le client veut une nouvelle version.

**Mise en production (andyconstruct.ch)** — voir README §« Avant la mise en production »
- [ ] Retirer `.mockup-notice` et `noindex` ; brancher le formulaire (PHP hébergeur ou service nLPD) ; redirections 301 des anciennes URL Joomla (`brief-seo.md` §8.3) ; HTTPS + www unique.
- [ ] Search Console + Bing Webmaster Tools ; statistiques sans cookies.

**Marketing (analyse-marche.md §7)**
- [ ] 0-30 j : NAP identique partout (fiche Google, local.ch, search.ch, GGE, Kompass mal classé « charpenterie »).
- [ ] Campagne d'avis Google (objectif proposé : 15 à 90 j, 30 à 180 j).
- [ ] 30-90 j : 10 fiches projets, dossier de références PDF, veille simap.ch / FAO (CFC 271, 283, 285).
- [ ] J+90 : bilan (appels, formulaires, positions depuis Genève, test de 10 questions dans ChatGPT/Perplexity/Google/Copilot).
- [ ] Phase 2 éventuelle : pages service × ville (Lausanne, Neuchâtel, Fribourg, Sion…) avec contenu réel.

---

## 11. Points d'attention techniques

- Ne jamais éditer `site/*.html` à la main : ce sera écrasé à la prochaine génération.
- La 404 utilise des chemins relatifs ; si l'hébergeur la sert depuis un sous-dossier profond, ajouter une balise `<base>`.
- Les textes alternatifs du manifest photos sont un peu longs (brief SEO : 5-15 mots) — à raccourcir si besoin.
- Le JSON-LD contient une URL search.ch avec l'ancienne adresse (bel-air-57) : à corriger quand l'annuaire sera mis à jour.
- Captures de contrôle : `npx playwright` (ou Node avec `playwright` global) sur `python3 -m http.server`, viewports 360/390/768/1024/1280/1440.
