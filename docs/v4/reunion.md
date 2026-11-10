# Réunion de présentation : support

**Support à utiliser : [tableau blanc en ligne (privé)](https://claude.ai/artifact/EcBMvSFvH6gMXr2xAG5LfJ).** Glisser pour se déplacer, molette ou pincer pour zoomer, ← → pour passer d'une étape à l'autre, clic sur une capture pour l'agrandir, N pour afficher la phrase clé de l'étape, F pour le plein écran. À partager avec Inès et le client via « Share » avant la réunion.

FigJam de secours : [Andy Construct — Réunion de présentation](https://www.figma.com/board/yF8CMRAXFzM8OYpkqpi0b7). **Vide au 10.11.2026** : la limite d'appels du serveur MCP de Figma (plan Starter) est tombée au premier appel de construction. Le tableau en ligne reprend exactement le même contenu et la même disposition.

Participants : Harbor Digital (présente à l'oral), Inès (associée), le dirigeant d'Andy Construct.
Principe : 12 sections reliées par des flèches rouges, en 3 rangées de 4, à lire de gauche à droite. Presque pas de texte : titres, chiffres, étiquettes.

## Ordre de présentation et phrase clé

| # | Section | Phrase à dire |
|---|---|---|
| 1 | Point de départ | « Aujourd'hui, on ne vous trouve pas, on ne peut pas vous vérifier, et rien n'est mesuré : 0 avis, Chêne-Bourg dans au moins 8 annuaires, aucune donnée depuis 2023. » |
| 2 | Marché & concurrence | « Les demandes sont captées par des réseaux qui n'exécutent pas, et personne ne combine des références publiques nommées avec le placo et l'acoustique : c'est votre place. » |
| 3 | Positionnement & cibles | « La rigueur des chantiers publics, au service de tous les chantiers : les pros achètent de la fiabilité, les particuliers de la confiance. » |
| 4 | Le site : arborescence | « 13 pages, une par métier et par question, et le téléphone toujours à un clic. » |
| 5 | Le site : design & preuve | « Le trait rouge, c'est votre niveau laser ; vos références sont visibles dès le premier écran, avec environ 40 % de texte en moins et 98-99/100 sur mobile. » |
| 6 | Conversion & tri automatique | « Le site trie chaque demande en A, B ou C et vous alerte ; vous, vous rappelez, visitez et chiffrez. » |
| 7 | Panel admin | « Chaque demande est enregistrée au même endroit, protégée par une double authentification, plus rien ne se perd dans les e-mails. » |
| 8 | SEO | « La technique est à 9/10 et la migration ne perd aucune page ; ce qui manque est hors du code : fiche Google, avis, adresse identique partout. » |
| 9 | GEO (IA) | « Les IA ne citent que ce qu'elles peuvent vérifier ailleurs : le site est prêt, il manque des mentions externes. » |
| 10 | Acquisition & vente | « Nous recommandons la combinaison C, environ CHF 3'750 par mois, pour environ 34 demandes et 6 chantiers par mois à un an : ce sont des estimations, recalées à trois mois. » |
| 11 | Ce qui marche / pas encore | « Le site, la preuve et le tri fonctionnent ; il nous manque vos avis, vos photos récentes, les accords des logos et du temps de votre côté. » |
| 12 | Reste à faire & décisions | « Six décisions aujourd'hui, à commencer par le budget et le nom de la 4e page, et on se revoit pour le bilan à 90 jours. » |

Les six décisions de la section 12 : budget mensuel (reco C), nom de la 4e page C16 (reco « cloisons isolantes » + 301), hébergeur (PHP 8.1 + MariaDB), logos des références (lettres + noms en attendant), particuliers hors Genève (reco Genève + La Côte), marchés publics (reco 6 dossiers par an). Sources : `projet/donnees.js` (décisions), `HANDOFF.md` §8-9.

## Reprise (quand des appels Figma sont de nouveau disponibles)

Tout est dans le scratchpad de la session, dossier `reunion/` :

- `img/` : 34 captures JPEG (qualité 80, ≤ 1600 px), dont l'ancien site capturé le 10.11.2026 ; `images.json` donne l'ordre.
- `call1.js` : squelette (en-tête, 12 sections, 34 cadres vides nommés « capture : <fichier> », connecteurs entre sections) ; il renvoie `imgIds`.
- `call2.js`, `call3.js`, `call4.js` : contenu des sections 1-4, 5-8 et 9-12 (ils retrouvent les sections par leur nom, aucun ID à recopier ; ils peuvent partir en parallèle après `call1.js`).
- `upload.sh urls.txt` : poste les 34 images vers les URL de `upload_assets` (`count` 34, `nodeIds` = `imgIds` dans l'ordre de `images.json`, `scaleMode` FILL).

Budget restant nécessaire : environ 7 appels (1 session, 4 `use_figma`, 1 `upload_assets`, 1 à 2 `get_screenshot`).
