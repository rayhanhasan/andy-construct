# Direction artistique v3 — Andy Construct

Auteur : direction artistique et front-end (studio). Base : `docs/v3/brief-v3.md` (prime), `docs/brief-design.md` (charte du logo), méthode du skill `frontend-design`.
Captures du benchmark : `scratchpad/benchmark/` (13 sites, 3 vues chacun + planches `planche-1..4.png`).

---

## 1. Benchmark : ce qui fait « premium » (constats)

Sites regardés (premier écran, section de références, suite) : Implenia, HRS, Losinger Marazzi, Erne, Walo, Induni, Frutiger, Bernasconi (finitions sols-plafonds-murs), **DSD SA** (plâtrerie-peinture à Genève, concurrent direct), et trois agences d'architecture (Herzog & de Meuron, David Chipperfield, Caruso St John). Belloni et Knauf bloqués par le proxy ou un pare-feu, steiner.ch est en liquidation (site d'information), marti.ch est une agence de voyages : écartés.

| Constat | Où | Ce qu'on en tire |
|---|---|---|
| **Une grande photo, propre**, sans voile généralisé : le texte vit dans un panneau ou une zone calme, pas sur toute l'image | Implenia, Erne, Losinger, DSD | Héro en deux zones : panneau anthracite (texte) + photo nette, sans voile |
| **Bords alignés** : le logo, le titre du héro et les titres de section partent de la même verticale | Implenia, HRS, Erne, Chipperfield | Une grille unique de 12 colonnes ; l'en-tête est sur la même grille que le contenu |
| **Peu de tailles de texte**, grand écart titre / texte, interlignage serré sur les titres | HRS (56/28), DSD (102/25), Losinger | Échelle classique 16-18-21-24-36-60-72, rien entre deux |
| **La couleur d'accent en très petite dose** : une barre courte, un bouton | Losinger (barre orange sous les titres), Implenia (jaune sur le seul bouton) | Le rouge Andy = un trait fin et les boutons, rien d'autre |
| **Preuve concrète** : projets nommés avec lieu et année, logos d'associations et de certifications, chiffres au format suisse (2'511) | DSD (« Maison horlogère, Genève, 2020 »), Induni (FER, SSE, labels), Walo (chiffres) | Mur de logos en tête, chiffres à l'apostrophe suisse, cartes projet « lieu · année » |
| **Codes du métier** comme gage de sérieux pour les pros (CFC / BKP) | Bernasconi | Les codes CFC 271/283/285 restent sur la page Professionnels |
| **Mouvement quasi absent** : fondus lents, rien qui rebondit, pas de carrousel | tous les « premium » ; à l'inverse Marti (couleurs multiples, carrousels) paraît bon marché | Une seule séquence orchestrée, le reste discret |
| **En-tête sur une ligne**, libellés courts, un bouton d'action distinct | Erne, DSD, Implenia | Une ligne : logo · 5 entrées · téléphone · bouton |
| Concurrent DSD : grande serif sur plafond à lames, très « magazine » | DSD | Se distinguer : notre marque est une linéale large (« CONSTRUCT ») ; on reste dans cette famille, en plus ferme |

## 2. Concept

**« Le trait de niveau »** : un site posé comme un plafond bien réglé — une ossature régulière (grille de 12 colonnes, filets fins), de grandes surfaces lisses (photos et blancs calmes), et un seul trait rouge, celui du laser de chantier, qui aligne, souligne et signe.

Pourquoi ce concept : le rouge Andy devient un outil du métier (la ligne laser qui met une cloison d'aplomb et un plafond de niveau) et non une décoration. Il justifie la sobriété (un trait, pas une surface) et donne au mouvement sa seule figure : un trait qui se tire.

## 3. Tokens

### 3.1 Couleurs (7 valeurs, dérivées du logo, aucune nouvelle teinte vive)

| Nom | Valeur | Rôle |
|---|---|---|
| Rouge Andy | `#E8000F` | Trait laser, boutons principaux (texte blanc 4,7:1), indicateur de page active |
| Rouge profond | `#C4000D` | Liens et petits textes rouges sur clair (6,3:1), survol des boutons |
| Anthracite | `#1D1F22` | Texte ; fonds profonds (héro, bande des chiffres, pied) |
| Graphite | `#44494F` | Texte secondaire (8,9:1 sur blanc, 8:1 sur plâtre) |
| Acier | `#B9BDC2` | Texte secondaire sur anthracite (8,7:1) |
| Plâtre | `#F0F0EE` | Fond alterné (mur de logos, demande) : le blanc mat d'une plaque, ni crème ni bleuté |
| Blanc | `#FFFFFF` | Fond principal, cellules du mur de logos |

Dérivé technique : Filet `#DCDEE1` (bordures, grille de cellules). Aucun dégradé décoratif ; le seul dégradé autorisé est l'ombre de lisibilité du héro mobile.

### 3.2 Typographie

- **Archivo** (variable, OFL, Omnibus-Type) pour les titres, les chiffres, la navigation et les boutons. Fichier unique réduit aux plages utiles : largeur 100-125 %, graisse 400-800 → **59 Ko** (woff2 latin). Utilisée **élargie** (`font-stretch: 112 %`) pour les titres et 118 % pour les chiffres : elle reprend la largeur et la géométrie de « CONSTRUCT » sans copier Montserrat, présente dans un modèle de site sur deux. À 104 % pour la navigation et les boutons (compacts).
- **Source Sans 3** (variable, OFL) pour le texte courant, 400 et 600 dans un seul fichier de **29 Ko**. Humaniste, très lisible ; elle se distingue nettement d'Archivo (largeur, construction).
- Total des polices chargées : 88 Ko (v2 : 85 Ko). Préchargement des deux fichiers ; `font-display: swap`.
- **Repli sans police** (fichier ouvert depuis le disque, polices bloquées par CORS en `file://`, ou réseau lent) : polices de repli calées (`size-adjust`, `ascent-override`) sur Arial / Helvetica / Liberation Sans, pour que la mise en page ne bouge pas et reste propre. Voir §8.
- Pas de titres en capitales, pas de libellés en capitales espacées, pas de mot coloré dans les titres. Les mots importants passent en **gras** dans le texte courant.

### 3.3 Échelle typographique (échelle classique de Bringhurst : 16 · 18 · 21 · 24 · 36 · 60 · 72)

| Rôle | Mobile | Bureau | Police | Interligne |
|---|---|---|---|---|
| Chiffres clés | 48 | 72 | Archivo 118 %, 600, chiffres tabulaires | 1 |
| H1 (héro) | 36 | 60 | Archivo 112 %, 650 | 1,06 |
| H2 (section) | 28 | 36 | Archivo 112 %, 650 | 1,12 |
| H3, titres de cartes | 21 | 24 | Archivo 108 %, 600 | 1,25 |
| Chapeau | 19 | 21 | Source Sans 3, 400 | 1,5 |
| Texte | 18 | 18 | Source Sans 3, 400 / 600 | 1,6 |
| Petit, légendes, navigation | 16 | 16-17 | Source Sans 3 ou Archivo 104 % | 1,4 |

Aucun texte sous 16 px. Ligne de texte ≤ 68 caractères, chapeau ≤ 56.

### 3.4 Grille et rythme vertical

- **12 colonnes**, contenu max. **1312 px** (1440 − 2 × 64). Marges latérales 16 px (mobile) → 32 → 64 (≥ 1280 px). Gouttières 16 / 24 / 32 px.
- L'en-tête, le héro, les titres de section et le pied partent de la **même verticale** (colonne 1).
- Rythme sur une base de **8 px** : espacements 8, 16, 24, 32, 48, 64, 96, 128.
- Sections : 64 px (mobile) → 96 → **128 px** (≥ 1200 px). En-tête de section → contenu : 48 / 64 px. Titre → texte : 16 / 24 px.
- En-tête de section : titre à gauche (colonnes 1-8), lien « Tout voir » à droite, aligné sur la ligne de base du titre ; un filet fin dessous seulement quand la section est une liste (logos, projets).

### 3.5 Formes

Angles vifs (rayon 2 px ; 0 sur les photos ; pastilles de logos du pied : 4 px). Pas d'ombres portées, sauf le menu déroulant et l'en-tête compacté (une ombre très diffuse, pour décoller du contenu). Séparation par filets et fonds alternés.

## 4. Traitement photo

- **Vraies photos d'abord**, sans filtre ni virage de couleur (honnêteté), recadrées à des formats constants : héro 4:3 (bureau) et 5:4 (mobile), cartes projet 4:5 et 3:2, avant/après 4:3.
- Aucune photo n'est assombrie entière : le texte du héro vit sur un panneau anthracite plein. Sur mobile seulement, une ombre basse sous la photo pour la transition.
- Images d'illustration sous licence (agent images) : jamais dans les réalisations ni présentées comme des chantiers d'Andy Construct ; une mention discrète « Illustration » dans leur légende ; textes alternatifs génériques.
- Survol d'une carte : zoom 1,03 en 600 ms, rien d'autre.

## 5. Composants clés

| Composant | Décision |
|---|---|
| **En-tête** | Une ligne de 76 px, blanc, sur la grille : logo (colonne 1) · navigation de 5 entrées, alignée à gauche après le logo · à droite le numéro (sans horaires) et « Demander un devis ». Compacté à 60 px après 40 px de défilement : logo réduit, filet + ombre diffuse. Sous 1240 px : logo, numéro abrégé en bouton « Appeler » (≥ 900 px), bouton « Menu ». Menu mobile : panneau plein écran sous l'en-tête, grandes entrées (21 px), prestations dépliées, puis Appeler / Devis. Indicateur de page : trait rouge de 2 px sous l'entrée. |
| **Héro** | Deux zones sur la grille : panneau anthracite colonnes 1-6 (titre, une phrase, deux boutons, badges de confiance), photo colonnes 7-12 jusqu'au bord droit de l'écran. Le **trait laser** traverse le panneau et la photo à la hauteur de la fin du titre. Hauteur calculée pour laisser voir la première rangée de logos dans le premier écran (1440 × 900). |
| **Badges de confiance** | Rangée de 4 sous les boutons, séparés par des filets acier : « Depuis 2007 », « Inscrite au registre du commerce », « Siège à Carouge », « Toute la Suisse romande » ; badges à confirmer (GGE, assurance RC, visite gratuite) affichés selon `confirmations.json`. Icône fine + libellé ; lien vers la preuve quand elle existe (Zefix). |
| **Mur de logos** | Section dédiée juste sous le héro, fond plâtre. Titre fort « Ils nous ont confié des travaux » + lien vers toutes les références. Grille de **cellules blanches séparées par des filets** (6 × 2 au bureau, 3 × 4 tablette, 2 × 4 mobile), logos **en couleur officielle**, hauteur optique 56 px × `echelle` (bureau), centrés. Noms sans fichier ou non autorisés en production : wordmark typographique homogène (Archivo 108 %, 600). |
| **Bande défilante** | Tous les logos en couleur, en continu (60 s par tour), pausable au survol et au focus, **bouton Pause** visible ; arrêtée en mouvement réduit (rangée statique défilable). Placée en rappel juste avant le bloc de demande. |
| **Chiffres** | Bande anthracite : 4 chiffres (Archivo 72 px, apostrophe suisse) qui comptent une fois à l'apparition ; la valeur finale est dans le HTML et lue par les lecteurs d'écran. |
| **Cartes projet** | Composition asymétrique : une grande carte (colonnes 1-7, photo 4:3) + deux cartes empilées (colonnes 8-12). Titre, lieu, prestations. Aucune bordure : la photo porte la carte. |
| **Prestations** | 4 cartes avec image (photo réelle ou illustration signalée), titre, une phrase, lien. |
| **Appel à l'action** | Bloc de demande (formulaire en 3 étapes) précédé du rappel des logos. Un seul bouton rouge par écran. |
| **Pied** | Anthracite. Rappel des références : logos en couleur sur **pastilles blanches** (hauteur 64 px) ; coordonnées, horaires, liens, IDE. |

## 6. Système de mouvement

Principe : une seule séquence orchestrée (le héro), puis seulement des réponses aux actions et quelques apparitions sobres, une fois.

| Élément | Ce qui bouge | Durée | Courbe | Déclencheur |
|---|---|---|---|---|
| Héro, photo | échelle 1,06 → 1 (sans fondu : l'image compte pour le LCP dès le premier rendu) | 1600 ms | `--ease-pose` cubic-bezier(.2,.7,.2,1) | chargement |
| Héro, trait laser | se tire de gauche à droite (scaleX 0 → 1) | 900 ms, départ 150 ms | `--ease-laser` cubic-bezier(.65,0,.35,1) | chargement |
| Héro, titre | chaque ligne monte de sous un masque (translateY 105 % → 0) | 800 ms, décalage 90 ms, départ 300 ms | `--ease-pose` | chargement |
| Héro, texte, boutons, badges | fondu + 12 px | 600 ms, départs 700 / 800 / 950 ms | `--ease-pose` | chargement |
| Chiffres | comptent de 0 à la valeur | 1400 ms | ease-out cubique | 1re apparition (IntersectionObserver), une fois |
| Logos défilants | translation continue | 60 s / tour | linéaire | permanent ; pause au survol, au focus, au bouton |
| Révélation des sections clés (mur de logos, projets, chiffres) | fondu + 16 px, cellules décalées de 40 ms | 700 ms | `--ease-pose` | 1re apparition, une fois |
| En-tête | 76 → 60 px, logo réduit, filet + ombre | 250 ms | `--ease-pose` | défilement > 40 px |
| Menu mobile, menu déroulant | fondu + 8 px | 200-250 ms | `--ease-pose` | clic |
| Cartes | zoom photo 1,03 | 600 ms | `--ease-pose` | survol / focus |
| Boutons, liens | couleur, flèche + 4 px | 150 ms | ease | survol / focus |
| Formulaire (étapes), FAQ, avant/après | fondu de l'étape, rotation du signe +, curseur | 200 ms | ease | action |

Règles :
- Le contenu est **visible sans JavaScript** : les états de départ ne s'appliquent que si `main.js` a posé la classe `anim` (et pas de mouvement réduit). Les éléments déjà à l'écran au démarrage ne sont pas masqués.
- `prefers-reduced-motion: reduce` : aucune animation ni transition de déplacement, bande de logos arrêtée, chiffres affichés directement.
- Rien ne bouge en boucle hors de la bande de logos (pausable, WCAG 2.2.2). Pas de parallaxe, pas de carrousel de contenu.

## 7. Wireframes

### 7.1 En-tête — bureau (≥ 1240 px), au repos (76 px) puis compacté (60 px)

```
|<- 64 ->|<----------------------------- 1312 (12 col.) ---------------------------->|<- 64 ->|
         [ANDY·CONSTRUCT]  Prestations ▾  Réalisations  Professionnels  L'entreprise  Contact     ☎ 022 771 20 15  [Demander un devis]
         ‾‾‾ col. 1-2 ‾‾‾  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ col. 3-9, alignée à gauche ‾‾‾‾‾‾‾‾‾‾‾‾  ‾‾‾‾‾‾‾ col. 10-12, à droite ‾‾‾‾‾
compacté : même ligne, logo 132 → 112 px, hauteur 60, filet bas + ombre diffuse
```

### 7.2 En-tête — mobile (390 px)

```
| [ANDY·CONSTRUCT]                 [☰ Menu] |   60 px, collant
menu ouvert (plein écran sous l'en-tête) :
| Prestations                               |
|   Placo · Peinture · Isolation acoustique |
|   Cloisons isolantes                      |
| Réalisations                              |
| Professionnels                            |
| L'entreprise                              |
| Contact                                   |
| [ Appeler le 022 771 20 15 ]              |
| [ Demander un devis        ]              |
barre fixe en bas d'écran : [☎ Appeler] [Demander un devis]
```

### 7.3 Accueil — bureau (1440 × 900)

```
┌ en-tête 76 ────────────────────────────────────────────────────────────────────┐
├──────────── panneau anthracite (col. 1-6) ──┬──── photo nette (col. 7 → bord) ─┤
│  Titre H1 60 px, 3 lignes                    │                                  │
│  ──────────────── trait laser rouge ─────────┼──────────────────────────────────│
│  Une phrase (21 px)                          │                                  │
│  [Demander un devis]  [Appeler le 022 …]     │                                  │
│  ─ badges : depuis 2007 │ RC │ Carouge │ SR ─│                                  │
├──────────────────────────────────────────────┴──────────────────────────────────┤  ← pli (900 px)
│ plâtre │ Ils nous ont confié des travaux                  Toutes nos références │
│        ├────┬────┬────┬────┬────┬────┐  logos couleur, cellules blanches       │
│        │ VdG│ CMG│HEAD│ OMC│ UBS│Piag│                                         │
│        ├────┼────┼────┼────┼────┼────┤                                         │
│        │ PlO│ CoB│Safr│Labc│Ever│Celg│                                         │
├──────────────────────────────────────────────────────────────────────────────────┤
│ Prestations : 4 cartes image + titre + phrase                                    │
├──────────────────────────────────────────────────────────────────────────────────┤
│ Réalisations : [grande carte col. 1-7] [carte col. 8-12] / [carte col. 8-12]     │
├──────────────────── anthracite ──────────────────────────────────────────────────┤
│  19 ans │ 18 références publiques │ 4 métiers │ 7 cantons et régions             │
├──────────────────────────────────────────────────────────────────────────────────┤
│ Méthode en 4 étapes (vraie séquence : numérotée)                                 │
│ (Témoignages / avis : masqués tant qu'ils sont vides)                            │
│ FAQ (col. 1-4 titre, col. 5-12 questions)                                        │
├ plâtre ─ bande défilante des logos [Pause] ──────────────────────────────────────┤
│ Demande de devis (formulaire 3 étapes, col. 1-8) │ rappel, téléphone (col. 9-12) │
├ pied anthracite : logos sur pastilles blanches · coordonnées · liens · IDE ─────┤
```

### 7.4 Accueil — mobile (390 px)

```
| en-tête 60                         |
| photo 5:4 (pleine largeur)         |
| ── trait laser ──                  |
| panneau anthracite : H1 36 px      |
| phrase                             |
| [Demander un devis] (pleine larg.) |
| [Appeler le 022 771 20 15]         |
| badges 2 × 2                       |
| Ils nous ont confié des travaux    |
| 2 × 4 cellules logos               |
| Toutes nos références              |
| Prestations (4 lignes image+texte) |
| Réalisations (cartes empilées)     |
| chiffres 2 × 2                     |
| Méthode · FAQ · logos défilants    |
| Demande · pied                     |
| [☎ Appeler] [Demander un devis]    |  barre fixe
```

## 8. Ouverture depuis le disque (`file://`)

En `file://`, Chrome bloque les polices (`@font-face` d'origine « null ») : le site s'affiche alors avec les **polices de repli calées** (Arial / Helvetica / Liberation Sans ajustées en largeur et en hauteur d'x), sans décalage de mise en page. Le reste (images, styles, scripts, animations) fonctionne. Le rendu de référence reste celui servi en HTTP (`php -S localhost:8096 -t site`). Les formulaires, eux, demandent PHP.

## 9. Drapeaux de test A/B

Module source `tools/build/static/drapeaux.js`, injecté (minifié) dans le script d'amorçage du `<head>` pour attribuer la variante **avant le premier rendu** (pas de clignotement, pas de décalage) :
- configuration dans `tools/build/donnees/config.json` → `ab` (actif global, drapeaux, variantes, poids) ; `"actif": false` coupe tout : chacun voit la variante `a`, aucun événement ;
- attribution stable par visiteur (`localStorage`, clé `ac_ab`) ; sans stockage : variante `a`, pas de mesure ;
- forçage pour la recette : `?flag=hero-titre:b` (plusieurs : `?flag=hero-titre:b,cta-libelle:b` ; `?flag=reset` efface) ;
- marquage HTML : `data-flag="nom" data-variant="a|b"` ; la feuille de style (générée depuis la config) n'affiche que la variante attribuée ; l'ordre des sections se change par déplacement dans le DOM (ordre de lecture = ordre visuel) ;
- mesure : événement Umami `exposition_variante` `{flag, variante}`, une fois par page vue et par drapeau effectivement présent.

## 10. Revue du plan contre le brief et le skill (ce que j'ai changé)

| Premier jet | Problème | Décision |
|---|---|---|
| Héro plein cadre avec voile anthracite (comme la v2) | Défaut générique de tous les sites BTP ; la photo est salie | Panneau anthracite + photo nette côte à côte, reliés par le trait laser |
| Surtitre en capitales espacées au-dessus de chaque titre (charte v1) | Tic de modèle (skill §5) ; ajoute du texte (retour client « trop de texte ») | Supprimé sur l'accueil ; la structure passe par la grille et les filets |
| Petit parallélogramme rouge devant chaque surtitre | Décor répété partout = bruit | Le rouge devient **un** trait (laser) : héro, page active, survols |
| Montserrat | Police de modèle, rendue « générique » | Archivo élargie (lien formel avec « CONSTRUCT ») |
| Fond « crème » chaud pour les sections alternées | Signature des pages générées par IA | « Plâtre » `#F0F0EE`, neutre et mat |
| Logos graphite / noms en texte (v2 et première version de ce plan) | Retour client prioritaire : logos qui se fondent | **Logos officiels en couleur**, cellules blanches, wordmarks seulement en repli |
| Révélation en fondu de chaque section | « fade-and-slide-up partout » = générique (skill) | Seulement mur de logos, projets, chiffres ; une fois ; rien si mouvement réduit |
| Grande carte de chiffres dans le héro | Traitement par défaut (skill) | Les chiffres ont leur propre bande, après les preuves visuelles |
| Numéros 01 / 02 / 03 sur les prestations | Ce n'est pas une séquence | Numérotation réservée à la méthode (vraie séquence) |

Accessoire retiré avant de sortir (Chanel) : voir la note d'autocritique en fin de construction (`§11`).

## 11. Autocritique après captures

À compléter après les captures `v3-shots/` (1440, 1024, 390 ; en-tête au repos et compacté).
