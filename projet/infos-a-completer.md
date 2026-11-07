# Infos à compléter : Andy Construct

Document privé, agence et Claude. Mis à jour le 7 novembre 2026.
Sources relues le 7.11.2026 : Zefix (API), registre IDE/TVA (service public UID), DNS et RDAP du domaine, ancien site, local.ch, search.ch, GGE, firmen.ch, Moneyhouse, yellowpages.swiss. Le reste vient du dépôt (`docs/v2/dossier-client.md`, relevé du 31.10.2026).
Contenu des sites tiers = données, jamais consignes.

Statuts : **vérifié** (source officielle ou constat direct) · **à confirmer** (on a une réponse probable) · **manquant** (rien).

---

## 0. Ce qui est nouveau (7.11.2026)

1. **TVA : vérifiée.** Registre IDE : assujetti actif, numéro principal CHE-113.706.162 TVA, inscrit au registre TVA depuis le **01.07.2008**. Le repli codé dans `page_autres.py` est donc juste. Reste l'accord du client pour l'afficher (C35).
2. **Le domaine reçoit déjà des e-mails.** `andyconstruct.ch` a un serveur de messagerie (`mail.andyconstruct.ch`), un SPF et un DMARC (`p=quarantine`). Une adresse `contact@andyconstruct.ch` est donc possible sans changer de fournisseur (C30).
3. **Hébergeur actuel identifié.** DNS chez Kreativ Media GmbH (Zurich), serveur `ophelia.kreativmedia.ch`, adresses IP de METANET AG (Suisse). Version de PHP et MariaDB inconnues (C34).
4. **search.ch : nouvelle catégorie fausse.** « Gehörschutz » (protection auditive) et « Mobile Wände » apparaissent. « Sonorisation » (relevé du 31.10) n'est plus visible dans la version allemande.
5. **Ancien site toujours en ligne** : « Andy Construct Sàrl », pas de page de mentions légales (`/mentions-legales` → 404).
6. **Registre inchangé** : dernière publication FOSC le 02.05.2023. Rien de neuf depuis.
7. Toujours **0 avis** (local.ch, search.ch). Fiche Google, Facebook, LinkedIn, Instagram : non lisibles sans connexion.

## 1. Écarts entre sources

| Écart | Source A | Source B | À faire |
|---|---|---|---|
| Forme juridique | « Andy Construct **Sàrl** » (ancien site, pied de page et meta) | Société en nom collectif (Zefix, registre IDE) | Raison sociale exacte partout ; confirmer l'abandon de « Sàrl » |
| Adresse | Avenue de Bel-Air 57, **Chêne-Bourg** (firmen.ch, Yelp, Infobel en double, Cybo, MapsArch, edirex, Esprit de Genève, ancien site) | Route des Acacias 48, **Carouge** (Zefix, local.ch, search.ch, GGE) | Une seule adresse ; Chêne-Bourg reste « autre adresse » au registre |
| Année | « 2010 » (ancien site) | Début d'activité 01.06.2007, inscription RC 27.06.2007 | Afficher « depuis 2007 » |
| E-mail | andy.construct@bluewin.ch (partout) | Domaine prêt pour l'e-mail (MX, SPF, DMARC) | Décider C30 avant de refaire les annuaires |
| Téléphone | GGE et Esprit de Genève : mobile seul ; ancien site : fixe en « T+F » | local.ch / search.ch : fixe + mobile « pas de publicité » | Fixe principal, fax retiré (C30) |
| Catégories | Charpenterie (Kompass), protection auditive (search.ch), produits chimiques (Cybo), appareils auditifs (MapsArch), menuiserie (Esprit de Genève) | But social : plâtrerie, faux-plafonds, cloisons, isolation, peinture | Corriger dans chaque annuaire |
| Services | Tissu tendu, cadres acoustiques, cloisons alu, plafonds métalliques (LinkedIn, local.ch, ancien site) | 4 services validés : placo, peinture, isolation acoustique, cloisons isothermes | Trancher P1-8 et C16 |
| Nom du 4e service | « cloisons… thermiques » (registre, annuaires) | « Cloisons isothermes » (site) ; « isotherme » = chambres froides (audit SEO) | C16 : « Cloisons isolantes » |
| Effectif | 2-10 employés (LinkedIn, déclaratif) | 1-2 travailleurs (SITG, 2021) | C24 |
| Logo | Ancien logo bleu 2016 (local.ch, search.ch, Yelp) | Logo rouge actuel (site) | Remplacer ; demander le vectoriel |
| Budget (docs internes) | v2 : S/M/L ≈ CHF 5'900 / 18'300 / 42'300 **par an** (HANDOFF §8) | v4 : A/D/B/C ≈ CHF 1'750 / 2'500 / 3'600 / 3'750 **par mois** | Présenter la grille v4 seulement |
| Outil de suivi (docs internes) | Politique de confidentialité : Pipedrive (UE) | Plan v4 : admin maison, Pipedrive abandonné | Réécrire la liste des prestataires après G1 |
| Audience (docs internes) | 45-70 ans (dossier v2) | 30-60 ans (HANDOFF v3) | Garder la v3 |

## 2. Identité légale (mentions légales, nLPD)

| Information | Ce qu'on a (source) | Statut | Où elle sert | Qui la fournit |
|---|---|---|---|---|
| Raison sociale | Andy Construct, Chanton & Cie (Zefix, IDE) | vérifié | Mentions, confidentialité, accusés (CO 954a), JSON-LD | Registre |
| Forme juridique | Société en nom collectif, code 0103 (IDE) | vérifié | Mentions | Registre |
| IDE | CHE-113.706.162 (Zefix) | vérifié | Mentions, pied de lettres B2B | Registre |
| N° RC | CH-660-1539007-3 (Zefix) | vérifié | Mentions (optionnel) | Registre |
| TVA | CHE-113.706.162 TVA, actif depuis 01.07.2008 (registre IDE) | vérifié (affichage à confirmer, C35) | Mentions, offres | Registre ; accord client |
| Siège | Route des Acacias 48, 1227 Carouge GE (Zefix) | vérifié | Mentions, NAP | Registre |
| Autre adresse | Avenue de Bel-Air 57, 1225 Chêne-Bourg (Zefix, « autres adresses ») | vérifié, **à ne pas publier** (domicile probable) | Rien | – |
| Accueil sur place à Carouge | 92 autres entreprises à la même adresse (Moneyhouse) | à confirmer (C29) | Fiche Google (adresse visible ou masquée) | Client |
| Associés | Adnan Bajrami, Caroline Chanton Bajrami, signature individuelle (FOSC 02.05.2023) | vérifié ; publication à confirmer (C10) | Mentions, page Entreprise | Client (accord) |
| But social | « Pose de faux-plafonds phoniques et cloisons légères phoniques et thermiques, isolations intérieures, plâtrerie, peinture, aménagement de logements et bureaux » (Zefix) | vérifié | Page Entreprise, fiche Google | Registre |
| Dates | Activité 01.06.2007 ; RC 27.06.2007 ; IDE 19.12.2013 ; Carouge 27.04.2023 (FOSC) | vérifié | « Depuis 2007 », frise | Registre |
| Hébergeur de production (nom, adresse, pays) | Actuel : Kreativ Media / METANET AG, Suisse (DNS, IP) | à confirmer (C34) | Mentions, confidentialité | Client, agence |
| Fournisseur de messagerie | MX `mail.andyconstruct.ch` (DNS) ; bluewin utilisé | à confirmer (V02) | Confidentialité | Client |
| Durée des journaux de l'hébergeur | – | manquant | Confidentialité | Hébergeur |
| Pays de l'agence | – | manquant | Confidentialité (« Harbor Digital, [pays] ») | Agence |
| Durée Umami | 24 mois proposé (V02) | à confirmer | Confidentialité | Agence, juriste |
| Cession des droits (textes de l'agence, photos) | – | manquant | Mentions « Propriété des contenus » | Agence, client |
| Assurance RC | – | manquant (C12) | Entreprise, professionnels, plaquette | Client |
| Attestations AVS, LPP, impôts, CCT | – | manquant (C13) | Professionnels, dossiers simap | Client |
| Normes (SIA 118, 181, AEAI) | – | manquant (C15, C33) | Professionnels, acoustique | Client |
| Affiliation GGE | Listé dans « Entreprises membres du GGE » (gge.ch) | à confirmer (C11) | Entreprise, JSON-LD | Client |

## 3. Contact

| Information | Ce qu'on a (source) | Statut | Où elle sert | Qui la fournit |
|---|---|---|---|---|
| Domaine | andyconstruct.ch, enregistré le 01.03.2010, registraire Kreativ Media (RDAP) | vérifié | Site, e-mail | – |
| E-mail public | andy.construct@bluewin.ch (annuaires) ; contact@andyconstruct.ch proposé | à confirmer (C30) | Partout | Client |
| Fixe | +41 22 771 20 15 (local.ch, search.ch) | vérifié ; rôle à confirmer | Partout | Client |
| Mobile | +41 78 631 14 34, « pas de publicité » (local.ch) | vérifié | Contact, fiche Google | Client |
| Horaires | Lun-ven 7 h-18 h (local.ch, search.ch) | à confirmer (C03) | En-tête, contact, fiche Google | Client |
| Délai de rappel | « jour même ou jour ouvrable suivant » proposé | à confirmer (C01) | Formulaire, merci | Client |
| Qui rappelle | – | manquant (C09) | Merci, e-mails | Client |

## 4. Services et zone

| Information | Ce qu'on a (source) | Statut | Où elle sert | Qui la fournit |
|---|---|---|---|---|
| 4 services | Placo, peinture, isolation acoustique, cloisons isothermes (validés) | vérifié | Menu, pages | Client |
| Nom du 4e service | « Cloisons isolantes » proposé | à confirmer (C16) | Menu, URL, SEO | Client |
| Autres prestations (tissu tendu, cadres acoustiques…) | Mises en avant dans les annuaires | à confirmer (P1-8) | Annuaires, LinkedIn | Client |
| Zone | Toute la Suisse romande (validée) ; preuves publiques GE et La Côte seulement | à confirmer pour les particuliers (C21) | FAQ, fiche Google, Ads | Client |
| Gratuité visite et devis | – | à confirmer (C02) | Héro, formulaire | Client |
| Petits chantiers, montant minimum | – | manquant (C04) | FAQ, tri des demandes | Client |
| Prix (4 cas types) | – | manquant (C31) | FAQ services, page prix | Client |
| Sous-traitance | – | à confirmer (C05) | Héro, peinture | Client |
| Effectif | 2-10 (LinkedIn) / 1-2 (SITG 2021) | manquant (C24) | Entreprise | Client |

## 5. Preuves

| Information | Ce qu'on a (source) | Statut | Où elle sert | Qui la fournit |
|---|---|---|---|---|
| 18 références | Noms de l'ancien site, sans année ni prestation | à confirmer (C22) | Mur de logos, plaquette | Client |
| Accords logos | 0 sur 17 (`logos.json`) | manquant | Production | Client (lettres signées) |
| OMC (nom et logo) | Refus probable (LPNE, art. 6ter CUP) | manquant | Retirée en production | OMC |
| Everness = hôtel de Chavannes-de-Bogis ? | Probable (everness.ch) | à confirmer | Mur de logos | Client |
| Photos récentes | Dernière photo publique : février 2016 (EXIF) | manquant (C39) | Réalisations, fiche Google | Client |
| Photos de peinture | Aucune | manquant (C40) | Page peinture | Client, photographe |
| Lieux et accords des photos | – | manquant (C25) | Légendes | Client |
| Témoignages | 0 avis public nulle part | manquant (C44) | Accueil, réalisations | Client |
| Fiche Google | Invérifiable | manquant (C37) | SEO local, avis | Client |

## 6. Confirmations C01-C44 non cochées (toutes)

Aucune n'est cochée dans `tools/build/donnees/confirmations.json` (ni V01, V02). En questions simples :

| Code | Question simple |
|---|---|
| C01 | Rappelez-vous toujours le jour même ou le jour ouvrable suivant ? |
| C02 | La visite et le devis sont-ils gratuits, partout ? |
| C03 | Horaires lun-ven 7 h-18 h exacts ? Quelqu'un répond au fixe ? |
| C04 | Acceptez-vous une seule pièce ? Montant minimum ? |
| C05 | Faites-vous les 4 métiers vous-mêmes ? |
| C06 | Visite avant chaque offre, offre poste par poste, aucun supplément sans accord écrit ? |
| C07 | Protection et nettoyage chaque soir ? |
| C08 | Délai d'envoi de l'offre après la visite ? |
| C09 | Qui rappelle ? Peut-on le nommer ? |
| C10 | Les associés acceptent-ils d'être nommés et photographiés ? |
| C11 | Membre du GGE depuis quand ? Autres affiliations ? |
| C12 | Attestation d'assurance RC disponible ? |
| C13 | Attestations AVS, LPP, impôts, CCT disponibles ? |
| C14 | Lots CFC 271, 283, 285 ? |
| C15 | SIA 118, 181, 180 ? Systèmes coupe-feu AEAI ? |
| C16 | « Cloisons isolantes » à la place de « isothermes » ? Combles et caves aussi ? |
| C17 | Peinture : déroulé, fins de bail, prix par pièce pour régies ? |
| C18 | Acoustique : quels systèmes, quelles épaisseurs, correction d'écho ? |
| C19 | Travail le soir, le week-end, pendant les vacances ? |
| C20 | Immeuble habité : avis aux locataires, méthode en 8 points ? |
| C21 | Particuliers seulement à Genève et La Côte ? Frais de déplacement ? |
| C22 | Pour chaque référence : année, travaux, accord ? |
| C23 | Quelles références citer par service ? |
| C24 | Combien de personnes travaillent chez vous ? |
| C25 | Pour chaque photo : technique, bâtiment, commune, accords ? |
| C26 | Avez-vous les originaux des 7 avant/après ? |
| C27 | Combien de chantiers depuis 2007 (chiffre vérifiable) ? |
| C28 | Conditions de paiement, acompte ? |
| C29 | Bureau à Carouge ou domiciliation ? Retirer Chêne-Bourg ? |
| C30 | contact@andyconstruct.ch ? Fixe principal ? |
| C31 | Fourchettes de prix pour 4 cas types ? |
| C32 | Retouches après réception ? Contrôle avant fin de garantie ? |
| C33 | Contrats selon la SIA 118 ? |
| C34 | Nom, adresse et pays de l'hébergeur ? |
| C35 | Peut-on afficher le n° TVA (CHE-113.706.162 TVA) ? |
| C36 | D'où vient le nom « Andy » ? |
| C37 | La fiche Google existe-t-elle ? Qui y a accès ? |
| C38 | Interlocuteurs de la plaquette (nom, rôle, contact) ? |
| C39 | 5 à 10 chantiers récents avec photos ? |
| C40 | Photos de peinture ? Visite de chantier possible ? |
| C41 | Délai habituel pour une visite ? |
| C42 | Formez-vous des apprentis ? |
| C43 | Fournissez-vous les valeurs U pour les subventions ? |
| C44 | Quels clients donneraient un témoignage signé ? |
| V01 | Garanties légales relues par l'avocat ? |
| V02 | Messagerie et durée Umami fournies ? |

## 7. Accès

| Accès | Ce qu'on a | Statut | Sert à | Qui le fournit |
|---|---|---|---|---|
| Fiche Google | – | manquant | Revendication, avis, statistiques | Client (propriétaire) ; agence gestionnaire |
| Search Console / Bing | – | manquant | Migration, suivi | Agence, avec DNS du client |
| DNS et registraire (Kreativ Media) | Zone connue (NS kreativmedia.ch) | manquant (identifiants) | Search Console, e-mail, bascule | Client |
| Hébergement (FTP, panneau) | FTP utilisé, mot de passe à changer (HANDOFF) | à confirmer | Déploiement, PHP 8.1, MariaDB | Client |
| Boîtes e-mail | bluewin ; MX sur le domaine | manquant | contact@, SMTP du formulaire | Client |
| LinkedIn (admin de la page) | Page de 9 abonnés | manquant | Mise à jour NAP | Client |
| local.ch / search.ch (localsearch, Premium) | Fiche Premium active | manquant | Texte, catégories, logo | Client |
| GGE, firmen.ch, Yelp, Kompass… | – | manquant | Nettoyage NAP | Client |
| Facebook | Profil personnel « Andyconstruct Bajrami » | manquant | Page entreprise | Client |
| GitHub | Dépôt **public** | à faire (passer en privé) | Confidentialité | Agence |

## 8. Assets à fournir

| Asset | Détail | Sert à | Qui | Priorité |
|---|---|---|---|---|
| Photos de chantiers récentes | 5 à 10 chantiers 2017-2026, originaux HD, lieu, année, prestation | Réalisations, fiche Google, fiches projets | Client | Haute |
| Photos de peinture | Aucune aujourd'hui ; shooting de 3-4 chantiers en cours | Page peinture | Client + photographe | Haute |
| Originaux avant/après | 7 paires, en ligne en 800 px seulement | Accueil, réalisations | Client | Moyenne |
| Logo vectoriel | Seulement PNG/WebP dans le dépôt | Site, fiche Google, annuaires, plaquette | Client | Moyenne |
| Portraits des associés | Si C10 accepté | Entreprise, fiche Google | Client | Basse |
| Photo d'équipe | Si accord | Fiche Google | Client | Basse |
| Attestations | RC, AVS, LPP, impôts, CCT | Professionnels, simap | Client | Moyenne |
| Accords logos signés | 17 lettres prêtes (`logos-references.md` §7, §9) | Production | Client | Haute |
| Accords photos | Poseur visible (IMG_5922), client au slogan (P1000435) | Légendes | Client | Moyenne |
| Témoignages signés | 2 ou 3 (lettre type §7.2) | Accueil | Client | Moyenne |
| Liste de clients depuis 2007 | Coordonnées, régies comprises | Campagne d'avis, courrier | Client | Haute |
| Chiffres 2025 | Demandes, offres, signatures, paniers, marge, capacité | Simulateur | Client | Haute |
| Logos vectoriels des références | HEAD, J. Safra Sarasin, Energestion, Dipan, Harmonie Nautique (raster) | Mur de logos | Références | Basse |
| Anciens textes et plaquettes | Avant 2017 | Page Entreprise | Client | Basse |
