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

Le logo : deux plans parallélogrammes superposés (bleu profond au-dessus, gris argent en dessous), « ANDY » en noir et « CONSTRUCT » en bleu dans une linéale carrée type DIN, sous-titre « PLAFONDS CLOISONS PEINTURE » en gris, capitales espacées.

### Couleurs (seules couleurs autorisées)

| Rôle | Nom | Valeur | Usage |
|---|---|---|---|
| Primaire | Bleu Andy | `#004A99` | Boutons, liens, titres d'accent, icônes. Contraste blanc sur bleu ≈ 8.6:1 |
| Primaire foncé | Bleu nuit | `#00346E` | Survol des boutons, pied de page |
| Texte | Encre | `#1B1D1F` | Titres et texte courant |
| Texte secondaire | Graphite | `#4A4F55` | Textes d'appoint (≥ 7:1 sur blanc) |
| Décor | Argent | `#C3C6C9` | Plan gris du logo : filets, séparateurs, motifs. **Jamais pour du texte** |
| Fond alterné | Brume | `#F3F4F5` | Une section sur deux |
| Filets | Trait | `#DDE0E3` | Bordures de cartes, tableaux |
| Fond | Blanc | `#FFFFFF` | Fond principal |

Interdits : dégradés colorés, violet/turquoise/orange, néons, fonds noirs pleine page, texte gris clair sur blanc.
Seule exception : voile sombre (noir 55-70 %) sur la photo d'en-tête pour la lisibilité du titre.

### Typographie

- **Titres et libellés** : *Barlow* (linéale d'inspiration DIN, proche du lettrage du logo), graisses 600 et 700. Petits libellés (surtitres) en capitales, espacement 0.12em, rappel direct de « PLAFONDS CLOISONS PEINTURE ».
- **Texte courant** : *Source Sans 3*, 400 et 600. Très lisible pour un public senior.
- Polices **auto-hébergées** (woff2 dans `assets/fonts/`), aucun appel à Google Fonts (conformité nLPD / RGPD, rapidité).
- Taille de base **18 px** (1.125rem), interligne 1.6, longueur de ligne max ~70 caractères.
- H1 entre 2.2rem (mobile) et 3.4rem (desktop). Pas de titres géants.

### Motif graphique

Le **double plan** du logo (parallélogramme bleu + parallélogramme argent décalé) est le seul motif décoratif :
- petit marqueur devant les surtitres de section (≈ 28×8 px),
- éventuellement un filet biseauté en haut du pied de page.
Usage parcimonieux. Pas de formes décoratives flottantes, pas de blobs.

### Formes, ombres, mouvement

- Angles vifs : rayon 2-4 px maximum (architectural, précis).
- Ombres quasi absentes ; on sépare par les filets et les fonds alternés.
- Animations : aucune sauf transitions de survol (150-200 ms) et apparition douce optionnelle. Respect de `prefers-reduced-motion`.
- Interdits : carrousels automatiques, vidéo en lecture auto, parallaxe, compteurs animés, pop-ups, chat flottant.

### Iconographie et images

- Photos **réelles** uniquement (dossier `assets/img/portfolio/`). Aucune banque d'images.
- Icônes : traits fins (1.75 px), bleu Andy, SVG en ligne, sobres. Une icône par prestation max.
- Légendes factuelles sous les photos (type de travail), sans inventer de lieu ni de client.

## 4. Accessibilité et confort senior (non négociable)

- WCAG 2.1 AA minimum : contrastes, focus visible (contour bleu 3 px), lien d'évitement, formulaires avec étiquettes visibles.
- Zones cliquables ≥ 48 px. Boutons avec **texte** (jamais icône seule).
- **Numéro de téléphone visible en permanence** : en-tête sur ordinateur, barre fixe « Appeler / Devis » en bas sur mobile.
- Aucune information uniquement dans une image.
- Formulaire court : nom, téléphone, e-mail, type de travaux, commune, message, préférence « rappelez-moi ».

## 5. Ton rédactionnel

- Vouvoiement, phrases courtes, vocabulaire du métier expliqué simplement.
- Factuel et local : « entreprise genevoise », « depuis 2010 », « Chêne-Bourg », « Genève et Vaud ».
- Aucune promesse invérifiable (« n°1 », « meilleur de Genève »). Pas d'anglicismes.
- Orthographe suisse romande, format de téléphone suisse (`+41 22 771 20 15`), montants en CHF.
- Pas de croix suisse en logo ou en décor (usage commercial réglementé) : l'ancrage suisse passe par les mots, les lieux et les références.

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
