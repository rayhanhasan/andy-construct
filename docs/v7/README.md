# v7 — Reprise après revue du client

## Introspection : ce qui n'allait pas, et pourquoi
Je vérifiais surtout sur un écran de 1440 px et en captures réduites. Ce qui saute aux yeux sur un portable
(1280 × 720, 1366 × 768), un grand écran (1920) ou un téléphone, je ne le voyais pas.

| Constat | Cause | Correction |
|---|---|---|
| Sur mobile, on arrive sur un gros titre ; la photo est sous le pli | Ordre : texte, boutons, puis photo | Photo en tête de l'en-tête sur mobile, titre réduit : photo, titre, phrase et boutons tiennent dans le premier écran |
| Vide sous les titres des en-têtes | Le trait rouge retiré était seulement masqué : son espace restait | Élément supprimé, espacement fixe sous le titre |
| Bouton « Demander un devis pour une isolation acoustique » sur deux lignes | Libellé trop long dans l'en-tête | « Demander un devis » dans l'en-tête |
| Photos d'en-tête molles sur grand écran | Recadrage 4:5 préparé à 614–800 px, agrandi à 830 px | Photo entière à la meilleure définition, cadrée par un point focal par photo |
| Images mal coupées dans les cartes | Photo cadrée par son centre (les portraits perdaient le sujet) | Recadrages 16:9 centrés sur le sujet |
| Étiquettes « Illustration » | Mention de licence affichée sur l'image | Retirées ; le crédit reste dans les mentions légales |
| Pied de page mal aligné | Trois grilles différentes (5 colonnes, 4 égales, 4 inégales) ; interlignes de 28 et 44 px | Une seule grille de 4 colonnes, interligne de 36 px partout, 8 logos plus grands, bande à faire glisser sur mobile |
| Pas assez dynamique | Seul le texte de l'en-tête était animé | En-tête qui se dévoile, titres qui montent, parallaxe des grandes photos, projets en bande continue |

## Méthode désormais
Captures à 1280 × 720, 1366 × 768, 1920 × 1080 et 390 × 844, page par page, premier écran et page entière ;
comparaison avant / après ; contrôle automatique des images, des erreurs, des débordements, de l'accessibilité
(après défilement) et du rendu sans animation.
