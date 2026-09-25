# Brief design — Andy Construct (maquette de refonte)

Document de référence du chef de projet. Tout agent qui produit du visuel ou du texte pour le site s'y conforme.

## 1. Objectif du site

Un site vitrine qui **prouve** le savoir-faire d'une entreprise genevoise de plafonds, cloisons et peinture, et qui **déclenche un appel ou une demande de devis**.
Il ne vend pas du rêve : il montre des chantiers réels, des références publiques vérifiables, une méthode claire et un interlocuteur joignable.

## 2. Audience

- Régies immobilières, architectes, bureaux d'ingénieurs, maîtres d'ouvrage publics (communes), gérants de PME, propriétaires privés.
- Âge dominant 45-70 ans. Lisent sur ordinateur au bureau **et** sur téléphone sur le chantier.
- **Détestent l'extravagance** : pas d'effets, pas de jargon marketing, pas d'anglicismes.
- Veulent : voir des réalisations, savoir où l'entreprise intervient, pouvoir appeler en un clic.

## 3. Charte graphique — dérivée strictement du logo

> Mise à jour : le client a fourni son **logo actuel** (`docs/source/logo-andy-construct-original.webp`). L'ancien logo bleu de 2016 est archivé dans `docs/source/ancien-logo/` et **ne doit plus être utilisé**.

Le logo : « ANDY » en capitales grasses **rouges**, tracé oblique et coupes en biseau (le A se prolonge en une diagonale dynamique), pastille rouge à croix blanche (croix suisse) accolée au Y ; « CONSTRUCT » dessous, en capitales géométriques larges et très espacées, **blanc** (logo pensé pour fond sombre).

Déclinaisons préparées (`site/assets/img/brand/`) :
- `logo-andy-construct.(png|webp)` : « CONSTRUCT » en anthracite, **pour fonds clairs** (en-tête blanc) ;
- `logo-andy-construct-blanc.(png|webp)` : version d'origine, « CONSTRUCT » blanc, **pour fonds anthracite** (pied de page, héro) ;
- favicon : le « A » rouge du logo.
Ne jamais déformer, recolorer autrement, ni poser le logo sur une photo chargée sans voile.

### Couleurs (seules couleurs autorisées)

Principe : **l'anthracite et le blanc portent le site, le rouge ponctue**. Le rouge est la signature, pas le fond : il ne couvre jamais une grande surface (public senior, BTP, anti-extravagance).

| Rôle | Nom | Valeur | Usage |
|---|---|---|---|
| Signature | Rouge Andy | `#E8000F` | Boutons principaux (texte blanc, 4.7:1), marqueurs, filets d'accent, pastilles. Rouge du logo |
| Signature foncé | Rouge profond | `#C4000D` | Survol des boutons, **liens et petits textes rouges sur fond clair** (6.3:1) |
| Structure | Anthracite | `#1D1F22` | Pied de page, bandeau d'appel à l'action, voile du héro, titres |
| Texte | Encre | `#1D1F22` | Titres et texte courant |
| Texte secondaire | Graphite | `#44494F` | Textes d'appoint (≥ 8:1 sur blanc) |
| Texte sur sombre | Acier | `#B9BDC2` | Texte secondaire sur anthracite (8.7:1) |
| Fond alterné | Brume | `#F4F4F5` | Une section sur deux |
| Filets | Trait | `#E2E3E5` | Bordures de cartes, tableaux |
| Fond | Blanc | `#FFFFFF` | Fond principal |

Règles : pas de texte courant rouge vif (#E8000F) sur fond clair ni sur anthracite (utiliser `#C4000D` sur clair ; sur anthracite, le rouge vif seulement pour grands titres ≥ 24 px ou éléments décoratifs). Pas de fond rouge pleine largeur. Interdits : dégradés colorés, autres teintes (bleu, orange, vert…), néons, texte gris clair sur blanc.
Exception : voile anthracite (70-85 % à gauche, dégradé vers la droite) sur la photo d'en-tête pour la lisibilité du titre.

### Typographie

- **Titres** : *Montserrat* 700 (linéale géométrique large, même famille visuelle que « CONSTRUCT »), en casse normale (pas de titres tout en capitales). 600 pour les sous-titres.
- **Surtitres et petits libellés** : *Montserrat* 600 en capitales, espacement **0.18em**, rappel direct du « C O N S T R U C T » espacé du logo.
- **Texte courant** : *Source Sans 3*, 400 et 600. Très lisible pour un public senior.
- Polices **auto-hébergées** (woff2 dans `assets/fonts/`), aucun appel à Google Fonts (conformité nLPD / RGPD, rapidité).
- Taille de base **18 px** (1.125rem), interligne 1.6, longueur de ligne max ~70 caractères.
- H1 entre 2.1rem (mobile) et 3.2rem (desktop), interlettrage légèrement resserré (-0.01em). Pas de titres géants.

### Motif graphique

La **coupe en biseau** du logo (diagonales du A et du N) est le seul motif décoratif :
- petit trait oblique rouge (parallélogramme ≈ 26×6 px, inclinaison ~ -20°) devant les surtitres de section ;
- éventuellement un angle coupé en biseau sur un seul élément fort (bas du héro ou coin d'une image mise en avant).
Usage parcimonieux. Pas de formes décoratives flottantes, pas de blobs, pas de texte en italique forcé pour « faire dynamique ».

### Formes, ombres, mouvement

- Angles vifs : rayon 2-4 px maximum (architectural, précis).
- Ombres quasi absentes ; on sépare par les filets et les fonds alternés.
- Animations : aucune sauf transitions de survol (150-200 ms) et apparition douce optionnelle. Respect de `prefers-reduced-motion`.
- Interdits : carrousels automatiques, vidéo en lecture auto, parallaxe, compteurs animés, pop-ups, chat flottant.

### Iconographie et images

- Photos **réelles** uniquement (dossier `assets/img/portfolio/`). Aucune banque d'images.
- Icônes : traits fins (1.75 px), anthracite (rouge seulement pour un détail), SVG en ligne, sobres. Une icône par prestation max.
- Légendes factuelles sous les photos (type de travail), sans inventer de lieu ni de client.

## 4. Accessibilité et confort senior (non négociable)

- WCAG 2.1 AA minimum : contrastes, focus visible, lien d'évitement, formulaires avec étiquettes visibles.
- Zones cliquables ≥ 48 px. Boutons avec **texte** (jamais icône seule).
- Contour de focus : 3 px, `#1D1F22` sur fond clair, blanc sur fond anthracite (pas de rouge : trop proche des boutons).
- **Numéro de téléphone visible en permanence** : en-tête sur ordinateur, barre fixe « Appeler / Devis » en bas sur mobile.
- Aucune information uniquement dans une image.
- Formulaire court : nom, téléphone, e-mail, type de travaux, commune, message, préférence « rappelez-moi ».

## 5. Ton rédactionnel

- Vouvoiement, phrases courtes, vocabulaire du métier expliqué simplement.
- Factuel et local : « entreprise genevoise », « depuis 2010 », « Chêne-Bourg », « Genève et Vaud ».
- Aucune promesse invérifiable (« n°1 », « meilleur de Genève »). Pas d'anglicismes.
- Orthographe suisse romande, format de téléphone suisse (`+41 22 771 20 15`), montants en CHF.
- La croix suisse existe **uniquement dans le logo** (entreprise domiciliée et administrée à Genève). On n'en ajoute pas ailleurs (usage commercial réglementé, et ce serait ostentatoire) : l'ancrage suisse passe par les mots, les lieux et les références.

## 6. Architecture (reprise nettoyée de la démo)

La démo (template « Roofinger ») est conservée pour sa **structure** (en-tête → héro → chiffres → à propos → services → projets → FAQ → zone → appel à l'action → pied de page). On **retire** tout ce qui ne sert pas une PME genevoise : menu « Pages », tarifs, blog, équipe, vidéo, bandeaux Webflow, « urgence 24/7 », rayon en miles, avis 4.9/5 inventés.
Le code est **réécrit de zéro** (HTML/CSS/JS natifs, sans jQuery ni Webflow) : le template est une licence commerciale tierce, on ne copie ni son code ni ses images.

Pages :
1. `index.html` — Accueil (parcours complet, voir ci-dessous)
2. `prestations.html` — Détail des prestations, une section ancrée par métier
3. `realisations.html` — Galerie filtrable + liste complète des références
4. `contact.html` — Coordonnées, formulaire, zone d'intervention, horaires
5. `mentions-legales.html` — Impressum suisse + protection des données (nLPD)

Accueil, dans l'ordre :
1. Bandeau « maquette » discret (supprimable)
2. En-tête : logo, navigation (Prestations, Réalisations, L'entreprise, Contact), téléphone, bouton « Demander un devis »
3. Héro : photo réelle + voile, surtitre, H1, texte, 2 boutons (devis / appeler), bande de confiance (4 éléments)
4. Références : « Ils nous ont fait confiance » — noms en texte (pas de logos sans autorisation)
5. L'entreprise : texte + photo + chiffres clés
6. Prestations : 6 cartes + « Également : … »
7. Réalisations : 6 photos + lien galerie
8. Méthode en 4 étapes
9. Engagements (pourquoi nous confier votre chantier)
10. Témoignages (provisoires, à recueillir)
11. Zone d'intervention
12. FAQ (accordéons `<details>`)
13. Appel à l'action + formulaire
14. Pied de page complet (coordonnées, horaires, liens, IDE, © 2026)

## 7. Contenus provisoires

Tout chiffre, nom ou témoignage non confirmé par le client est :
- entouré d'un commentaire HTML `<!-- PROVISOIRE : ... -->`,
- listé dans `docs/contenus-a-valider.md`.
La maquette porte `noindex, nofollow` tant qu'elle est hébergée sur harbor-digital.fr.
