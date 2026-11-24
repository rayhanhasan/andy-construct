# v5 : mise à jour selon le document « Contenu site web » du client (23.11.2026)

Le document client (textes, ressources, maquettes indicatives) a été intégré dans la direction artistique du site. Le document ne traitait pas la disposition des éléments ; la mise en page reste la nôtre.

## Ce qui change

| Sujet | Avant (v3/v4) | Maintenant (v5) |
|---|---|---|
| Menu | Prestations (menu déroulant) · Réalisations · Professionnels · L'entreprise · Contact | L'entreprise · Acoustique · Faux plafonds · Cloisons · Plâtrerie & peinture · Réalisations (Professionnels et Contact : menu mobile et pied de page) |
| Métiers | Placo · Peinture · Isolation acoustique · Cloisons isothermes | Isolation acoustique et phonique (spécialité) · Faux plafonds · Cloisons et doublages (dont panneaux sandwich isothermes) · Plâtrerie et peinture |
| Héro de l'accueil | Panneau anthracite à gauche, photo à droite | Photo plein cadre, voile anthracite, slogan « L'expertise de l'aménagement intérieur », titre, boutons, barre de garanties au pied de l'image. **Mêmes informations.** |
| Accueil | « Quatre métiers, souvent sur le même chantier » | « Nos domaines d'expertise · Quatre savoir-faire, une même expertise » (l'acoustique mise en avant), tableau des normes, « Un partenaire pour vos projets en Suisse romande » |
| L'entreprise | Récit court | Texte du client : « Une histoire de savoir-faire et de passion », valeurs, phrase de fin |
| Formulaire de devis | Mention d'information sous le bouton (décision D2) | Case obligatoire « J'accepte que mes données soient utilisées pour traiter ma demande » ; champ « Plans ou photos » |
| Photos | 19 photos « hors offre » (tissu tendu, métal, vitrées) retirées | Réintégrées : le document confirme ces ouvrages. Publiées en production quand leurs accords et lieux sont confirmés (C25) |

## Pages

- `isolation-acoustique.html` : bénéfices (correction, isolation, coupe-feu), « corriger / isoler », 5 solutions, guide, normes.
- `faux-plafonds.html` (nouvelle) : texte du client, bénéfices, 5 solutions illustrées (tissu tendu = spécialité) et carte « Vous hésitez ? », normes.
- `cloisons.html` (nouvelle) : 5 solutions et carte « Quelle solution ? », bande « Notre spécialité : panneaux sandwich isothermes », normes.
- `platrerie-peinture.html` (nouvelle) : 4 cartes, la préparation en 4 étapes, bande « Création d'espaces », normes.
- Illustrations : schémas en coupe dessinés dans la charte (`tools/build/schemas.py`), remplacés par une vraie photo quand elle existe.

## Redirections 301 (`.htaccess`)

- `placo.html` → `cloisons.html` ; `peinture.html` → `platrerie-peinture.html` ; `cloisons-isothermes.html` → `cloisons.html#panneaux-sandwich`.
- Anciennes adresses Joomla, maintenant plus précises : plafonds en tissu tendu, plâtre, fibre de bois, fibre minérale, bac métallique → la carte correspondante de `faux-plafonds.html` ; cloisons légères, cloisons mobiles aluminium, isolation thermique ou phonique → `cloisons.html#…`.

## API et admin

- Nouvelles valeurs de travaux : `isolation-acoustique`, `faux-plafonds`, `cloisons`, `platrerie-peinture`. Les anciennes (`placo`, `peinture`, `cloisons-isothermes`) restent acceptées (demandes déjà reçues, n8n).
- Grille de scoring : faux plafonds 15, cloisons 15, plâtrerie et peinture 10.
- Tests : API 266/266, admin 221/221.

## À valider avec le client

1. **Titre du héro** : il dit encore « Placo, peinture, acoustique : la rigueur des chantiers publics ». Proposition alignée sur le nouveau menu : « Acoustique, plafonds, cloisons : la rigueur des chantiers publics ».
2. **Normes** : reprises du document (SIA 256 et 257 existent bien : faux-plafonds, peinture). À confirmer qu'elles correspondent aux systèmes posés.
3. **Photos de l'ancien site** (tissu tendu, métal, cloisons vitrées) : lieux et accords (C25) pour les publier en production.
4. **Case de consentement** : demandée par le client ; elle remplace la décision D2 (mention seule).

## Revue critique (24.11.2026)

Corrigé :
- Bandeau « Version de validation » supprimé de la version de test (seul le mode interne `verification` le garde, avec sa légende des points à confirmer).
- Titre du héro aligné sur le nouveau menu : « Acoustique, plafonds, cloisons : la rigueur des chantiers publics » (même promesse).
- Professionnels : en-tête sur l'ancienne offre (« plâtrerie, faux-plafonds et peinture ») remplacé ; entreprises générales ajoutées aux cibles ; tableau des normes à la place d'une phrase.
- Réalisations et Professionnels : titres et descriptions Google encore sur « placo, peinture » mis à jour.
- Logos répétés jusqu'à trois fois par page : retirés du pied de page (chaque page garde sa bande de références).
- Carte « Tissu tendu » (la spécialité) : photo terne d'une pièce vide remplacée par les îlots lumineux.

Vérifié : 13 pages en bureau et en mobile, aucun débordement horizontal, aucune erreur de chargement, liens et ancres internes valides, aucune vraie violation d'accessibilité (les alertes restantes sont du texte capté pendant son apparition animée).

Reste à décider avec le client : accords des logos (OMC, UBS, Piaget…), lieux et accords des photos de l'ancien site (C25), confirmation des normes, informations encore en attente (délais, horaires, prix : voir `a-remplir.json` de l'export local).
