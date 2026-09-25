# Contenus à valider avec le client

Maquette Andy Construct, version du 25 septembre 2026.
Chaque élément ci-dessous est entouré d'un commentaire `<!-- PROVISOIRE : … -->` dans le code HTML (`site/*.html`).
Les pages sont générées : pour corriger un texte, modifier les sources dans `tools/build/` puis lancer `python3 tools/build/build.py` depuis la racine du dépôt (ne pas modifier `site/*.html` à la main).

## 1. Identité et coordonnées (NAP), bloquant pour la mise en ligne

| Page | Élément | Valeur provisoire | Question à poser au client |
|---|---|---|---|
| Toutes (pied de page, contact, mentions, JSON-LD, `llms.txt`) | Adresse du siège | Route des Acacias 48, 1227 Carouge (Genève) | Le siège est-il bien à Carouge (registre du commerce depuis mai 2023) ? L'ancienne adresse Avenue de Bel-Air 57, 1225 Chêne-Bourg n'apparaît plus nulle part : est-ce correct ? |
| Toutes | Raison sociale et forme juridique | « Andy Construct, Chanton & Cie », société en nom collectif (et non « Sàrl ») | Confirmez-vous la raison sociale et la forme juridique ? |
| Toutes (pied de page), mentions légales | Numéro IDE | CHE-113.706.162 | Ce numéro IDE est-il le bon ? |
| Accueil, pied de page, mentions, JSON-LD | Ancienneté | « depuis 2007 », « 19 ans d'activité » (ancien site : « depuis 2010 ») | Quelle date faut-il afficher : 2007 (inscription au registre) ou 2010 ? |
| Accueil (L'entreprise), mentions légales | Direction | « dirigée par ses deux associés » (accueil) ; associés nommés dans les mentions : Adnan Bajrami, Caroline Chanton Bajrami | Les associés acceptent-ils d'être nommés dans les mentions légales ? La formule de l'accueil vous convient-elle ? |
| Toutes (pied de page, contact), JSON-LD | Horaires | Du lundi au vendredi, 7 h 00 – 18 h 00 (relevés sur local.ch) | Quels sont vos horaires réels ? Êtes-vous joignables le samedi ? |
| Toutes | E-mail | andy.construct@bluewin.ch | Souhaitez-vous une adresse sur votre domaine (p. ex. contact@andyconstruct.ch) ? |
| Toutes (en-tête, barre mobile) | Numéro mis en avant | Fixe +41 22 771 20 15 (le mobile +41 78 631 14 34 est affiché en second) | Quel numéro doit être appelé en priorité par les clients ? |
| JSON-LD (accueil) | Coordonnées géographiques | 46.18935, 6.13236 (OpenStreetMap, Carouge) | À recaler sur la fiche Google une fois l'adresse validée. |

## 2. Chiffres, engagements et méthode

| Page | Élément | Valeur provisoire | Question à poser au client |
|---|---|---|---|
| Accueil (héro), barre mobile, CTA | Devis gratuit | « Devis gratuit », « Après visite sur place » | Le devis (l'offre) est-il gratuit et sans engagement ? Faites-vous toujours une visite avant ? |
| Accueil (chiffres clés) | Nombre de chantiers | « 300+ chantiers réalisés » | Combien de chantiers avez-vous réalisés environ ? Sinon, on retire ce chiffre. |
| Accueil (méthode), prestations (déroulement) | Étapes d'un chantier | Visite, offre écrite, planning, protection des lieux, nettoyage, réception | Ce déroulé correspond-il à votre façon de travailler ? |
| Accueil (pourquoi nous choisir) | Engagements de service | « Une offre lisible », « Un chantier protégé » | Pouvez-vous vous engager sur ces deux points ? |
| Accueil (L'entreprise) | Signature | « Les associés d'Andy Construct » | Souhaitez-vous une signature nominative ? |

## 3. Témoignages

| Page | Élément | Valeur provisoire | Question à poser au client |
|---|---|---|---|
| Accueil | 3 témoignages | Textes fictifs attribués à des profils génériques : « Architecte, Carouge », « Régie immobilière, Genève », « Propriétaire, Vésenaz » | Pouvez-vous nous transmettre 2 ou 3 témoignages réels, avec l'accord écrit des auteurs (profil et commune suffisent) ? Sans cela, la section sera retirée. |

## 4. Prestations, normes et zone

| Page | Élément | Valeur provisoire | Question à poser au client |
|---|---|---|---|
| Prestations | Peinture intérieure | Préparation des supports, enduits, bandes, peinture des plafonds et des murs | Quel est le périmètre exact de votre offre peinture ? Avez-vous des photos ? |
| Prestations | Protection incendie | Plafonds, cloisons et habillages coupe-feu selon les prescriptions AEAI (aucune certification revendiquée) | Quels ouvrages coupe-feu réalisez-vous ? Disposez-vous d'attestations à mentionner ? |
| Prestations (normes et qualité) | Références normatives | AEAI (incendie), SIA 181 (acoustique), SIA 118 (exécution et réception) | Travaillez-vous selon ces normes ? Faut-il en citer d'autres ? |
| Prestations | Fibre de bois / fibre minérale | Photo « Plafond en dalles dans un couloir » utilisée pour illustrer la fibre minérale | Ces dalles sont-elles en fibre minérale ? Avez-vous une photo de plafond en fibre de bois ? |
| Prestations | Cloisons mobiles | Photo « Cloisons de bureaux vitrées » utilisée pour les cloisons mobiles en aluminium | S'agit-il bien de cloisons démontables en aluminium ? |
| Accueil, contact | Zone d'intervention | Liste du brief SEO, Carouge en tête ; côté vaudois jusqu'à Gland et Rolle | Jusqu'où vous déplacez-vous (Gland, Rolle) ? Faut-il retirer des communes ? |
| Réalisations (professionnels) | Codes CFC | 271 Plâtrerie · 283 Faux-plafonds · 285 Traitement des surfaces intérieures | Ces codes CFC correspondent-ils à vos soumissions ? |
| Réalisations (professionnels) | Dossier de références PDF | « Disponible sur demande par e-mail » | Pouvez-vous fournir un dossier de références (PDF) à mettre en téléchargement ? |

## 5. Références et photos

| Page | Élément | Valeur provisoire | Question à poser au client |
|---|---|---|---|
| Accueil, réalisations | 18 références en texte | Noms repris de l'ancien site, sans logo, sans date | Pouvez-vous dater chaque référence et préciser le type de travaux ? Acceptez-vous d'afficher des logos (avec l'accord des marques concernées) ? |
| Réalisations | Bank Sarasin | Mention « Aujourd'hui J. Safra Sarasin » | Le chantier date-t-il d'avant 2013 ? |
| Réalisations | Fiches « projets choisis » | Absentes : galerie de 30 photos à la place | Pour 3 à 5 chantiers : commune, année, type de client, besoin, solution posée, accord pour citer le client. |
| Réalisations | Photos avant / après | Absentes (ancre `#avant-apres` conservée pour la redirection de l'ancien site) | Avez-vous des paires de photos avant / après prises au même endroit ? |
| Réalisations (galerie) | Catégories des photos (voir `docs/selection-photos.md`) | Plafonds lumineux (IMG_5964, P1000755, IMG_3735, IMG_3727) classés en « Plafonds tendus » ; IMG_2464 en « Plafonds métalliques » ; salle de spectacle (IMG_6636, IMG_6632) en « Chantiers en cours » | Quelle technique a été posée sur ces chantiers ? Quelle prestation pour la salle de spectacle ? |
| Accueil, réalisations | Photo IMG_5922 (poseur en t-shirt Andy Construct) | Publiée (accueil et galerie) | Le poseur a-t-il donné son accord pour la publication ? |
| Réalisations | Photo P1000435 (slogan lisible au mur) | Publiée dans la galerie | Le client du chantier accepte-t-il d'être reconnaissable ? |
| Accueil (L'entreprise), galerie | Photo IMG_5963 (poseur sur échafaudage) | Publiée | Même question : accord de la personne photographiée. |
| Accueil | Mention « Toutes les photos proviennent de nos chantiers » | Photos reprises de l'ancien site | Confirmez-vous que toutes ces photos sont des chantiers d'Andy Construct ? |

## 6. Mentions légales et protection des données

| Page | Élément | Valeur provisoire | Question à poser au client |
|---|---|---|---|
| Mentions légales | Hébergeur | « Le site est hébergé en Suisse. » (nom et adresse absents) ; conception : Harbor Digital | Nom et adresse de l'hébergeur de production, à ajouter dans les mentions légales. |
| Mentions légales | Durée de conservation | 12 mois sans suite, sinon durée légale des pièces commerciales | Cette durée vous convient-elle ? |
| Mentions légales | Lieu de traitement | « Les données sont traitées en Suisse » | Votre messagerie (Bluewin) et l'hébergeur sont-ils en Suisse ? |
| Accueil, contact | Formulaire | Sans envoi réel (le message de confirmation s'affiche, rien n'est transmis) ; pièce jointe « photo ou plan » prévue | À quelle adresse faut-il envoyer les demandes ? Taille maximale des pièces jointes ? |
