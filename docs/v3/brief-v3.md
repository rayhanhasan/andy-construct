# Brief v3 — « Le site qu'on a promis : beau, structuré, formel, vivant »

Chef de projet : Claude. Base : v2 (commit `a633851`). Ce brief **prime** sur `docs/brief-design.md` et `docs/v2/programme-v2.md` là où ils divergent.

## 1. Retour du client sur la v2 (à corriger, tout)

- « Ça va, mais tout le monde peut faire ça. » Le contrat a été gagné en promettant un site **beau, magnifique**. La v2 est propre mais générique.
- **Logos des références** : mise en page faible (logos et noms mélangés, petits, sans hiérarchie).
- **Animations** : inexistantes. Le client veut un site **un peu plus animé**, sans extravagance.
- **En-tête** : mal aligné, trop d'informations, trop d'espace vide.
- **Trop de texte** ; les **mots importants ne ressortent pas** ; le site paraît **disproportionné** (échelle typographique, rythme vertical).
- **Pas assez de preuve sociale sur l'accueil.** « Vraiment pas. » Il faut mettre en avant beaucoup plus ceux qui ont fait confiance, et le **répéter**.
- **Il manque des images.**
- Le site doit servir une **stratégie d'acquisition** : signaux de confiance (« flags »), dispositifs de test.

## 2. Ce qui change

| Sujet | v2 | v3 |
|---|---|---|
| Audience | 45-70 ans, très prudent | **30-60 ans** (gérants de régie, architectes, responsables techniques, propriétaires actifs). Toujours sobre et formel, mais **moderne et premium** |
| Ambition visuelle | sobre, utilitaire | **premium suisse** : grille rigoureuse, grande photographie, typographie maîtrisée, finitions soignées. Référence d'esprit : sites des grandes entreprises générales suisses, en plus chaleureux |
| Mouvement | aucun | **animations utiles et discrètes** : une séquence d'entrée orchestrée sur le héro, compteurs qui s'animent une fois, défilement continu des logos (pausable), révélation douce des sections clés, transitions des interactions (menu, filtres, formulaire, avant/après), en-tête qui se compacte au défilement. Tout respecte `prefers-reduced-motion`. Pas de parallaxe agressive, pas de carrousel automatique de contenu |
| Preuve sociale | 3 expositions par page | **Fil conducteur de l'accueil** : mur de logos soigné dès le premier écran, chiffres clés, projets nommés (lieux publics réels : Conservatoire, Alhambra, salles communales…), rappel avant chaque appel à l'action, pied de page. Emplacements prêts pour les avis Google et les témoignages (masqués tant qu'ils sont vides) |
| Signaux de confiance | quelques faits | **Badges de confiance** cohérents (depuis 2007, inscrite au RC, siège à Carouge, Suisse romande, références publiques ; badges à confirmer : GGE, assurance RC, visite gratuite) — rendus selon `confirmations.json` |
| Texte | dense par endroits | **Coupe franche** : un message par section ; mots-clés en **gras** dans le texte courant (pas de mot coloré dans les titres) ; listes courtes ; chiffres mis en valeur |
| Images | 11-30 photos, peu exploitées | **Beaucoup plus d'images** : vraies photos mieux cadrées et mises en scène ; images illustratives sous licence (Unsplash/Pexels) pour les services et les ambiances, **jamais présentées comme des réalisations d'Andy Construct** ; vidéo d'ambiance possible si elle sert le héro |
| A/B | recommandations | **Drapeaux de test** (feature flags) simples côté client : variantes de titre du héro, ordre des sections, libellé du bouton, avec suivi Umami de la variante |

## 3. Ce qui ne change pas

- Charte du logo : rouge Andy `#E8000F` en ponctuation, anthracite `#1D1F22`, blanc ; le logo reste intact. La palette peut s'enrichir de neutres chauds/froids et d'une couleur de fond profonde si elle sert le premium — sans nouvelle teinte vive.
- Les 4 services, la zone, l'identité légale, les règles d'honnêteté (aucune fausse preuve), la nLPD, l'API et l'automatisation v2, les 3 modes de génération.
- Accessibilité AA, performance (LCP < 2,5 s mobile ; poids raisonnable même avec plus d'images), aucune dépendance externe au chargement (polices auto-hébergées, pas de CDN).

## 4. Skills à utiliser (installés dans `.claude/skills/`)

- Design : `frontend-design/SKILL.md` (lire avant toute décision visuelle), `theme-factory`.
- Tests : `webapp-testing/SKILL.md`.
- Marketing : `cro`, `copywriting`, `copy-editing`, `marketing-psychology`, `ab-testing`, `conversion-tracking`, `image`, `offers`, `lead-magnets`, `seo-audit`, `ai-seo`, `schema`, `site-architecture`, `competitor-profiling`, `customer-research`, `ads`.
- Contexte produit pour ces skills : `.claude/product-marketing.md`.

## 5. Critère de réussite

Un directeur d'agence exigeant regarde l'accueil sur ordinateur et sur téléphone et pense « c'est beau, c'est sérieux, je ferais confiance » en moins de 5 secondes ; la preuve sociale est impossible à rater ; le chemin vers la demande est évident ; rien n'est clinquant.
