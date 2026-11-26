# v6 — Photos du client, accueil interactif

## Photos
- 11 photos de chantier fournies par le client, importées par `tools/images/importer_photos.py DOSSIER` :
  redressement, métadonnées supprimées (GPS, appareil), tailles 400 à 2400 px en WebP (+ JPEG 800),
  recadrages 4:5 et 16:9 centrés sur le sujet. Aucun agrandissement au-delà de la définition d'origine.
- Trois photos (IMG_9161, 9162, 9169) ne font que 480 × 640 px : elles vont dans des emplacements petits
  (cartes, vignettes). La grille des réalisations réserve les grands emplacements aux photos assez définies.
- 8 nouveaux projets en tête du portfolio (`portfolio.py`). En-têtes : accueil (diaporama), acoustique
  (salle de réunion), faux plafonds (piscine), cloisons (combles), plâtrerie (charpente), réalisations
  (piscine), professionnels (restaurant), entreprise (combles), contact (salle vitrée).
- Une même photo n'apparaît pas deux fois sur une page.

## Accueil
- En-tête au gabarit des pages, avec un diaporama de 4 chantiers : fondu, zoom lent, légende cliquable,
  vignettes à barre de progression, flèches du clavier, glisser au doigt, pause au survol et au focus.
  Pas de défilement automatique en mouvement réduit.
- Doublon retiré : la bande défilante de logos avant le formulaire répétait le pied de page. Les logos
  de la colonne du formulaire (pages services, contact) sont retirés pour la même raison.

## Interactions
- Cartes en légère profondeur au survol (souris seulement).
- Photos qui se dévoilent à l'entrée dans l'écran.
- Tout est désactivé en mouvement réduit.

## Nettoyage
- Code de l'ancien héro plein cadre, de la variante vidéo et de la bande défilante retiré (budget CSS/JS tenu).
