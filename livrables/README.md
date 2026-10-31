# Supports commerciaux d'Andy Construct

Supports PDF (aimants à prospects, décisions D3 et D7) et fichier de suivi commercial. Textes : `docs/v2/copy-deck.md` §Q ; charte : `docs/brief-design.md` ; stratégie : `docs/v2/strategie-acquisition.md`.

## 1. Liste des supports

| Fichier | Format | Public | Usage |
|---|---|---|---|
| `site/assets/docs/andy-construct-references.pdf` | A4, 5 pages, 615 Ko | Régies, architectes, communes, entreprises | Dossier de références, **version production** : noms des références en texte, textes de repli pour tout point non confirmé. Libre téléchargement, à joindre aux offres et aux courriers B2B. |
| `livrables/andy-construct-references-preview.pdf` | A4, 6 pages, 627 Ko | Associés (séance de validation) | Même dossier, **version de validation** : textes définitifs, codes `Cxx` en exposant, logos graphite des références `a_autoriser`, bandeau « ne pas diffuser ». |
| `site/assets/docs/guide-reduire-le-bruit.pdf` | A4, 8 pages, 177 Ko | Propriétaires, locataires, PPE | Guide « Réduire le bruit chez soi », valable quelle que soit l'entreprise ; contacts en dernière page seulement. |
| `site/assets/docs/checklist-chantier-site-occupe.pdf` | A4, 3 pages, 55 Ko | Régies et gérances | Liste de contrôle imprimable (cases à cocher, colonne « Fait le »), puis modèle d'avis aux locataires. |
| `livrables/suivi-demandes-et-kpi.xlsx` | Excel, 6 onglets | Associés | Suivi des demandes et KPI tant que le CRM n'est pas en place (scénario S). Mode d'emploi dans le premier onglet. |

Tous les PDF : texte sélectionnable, polices Montserrat et Source Sans 3 incorporées (sous-ensembles), métadonnées (titre, sujet, mots-clés, auteur « Andy Construct », langue fr-CH), photos en JPEG compressé, lisibles imprimés en noir et blanc (vérifié en niveaux de gris), texte courant de 12 à 13 pt.

**La version preview ne va pas dans `site/`** : elle serait publiée avec le site, alors que les logos qu'elle montre n'ont pas encore d'accord écrit (programme v2, §4).

## 2. Où les supports sont liés sur le site

Noms de fichiers communs au frontend, aux supports et à l'automatisation (D7). Au 31.10.2026, `tools/build/` ne contient pas encore ces liens : à intégrer par le développeur frontend.

| Support | Emplacement (copy deck) | Libellé à afficher |
|---|---|---|
| Dossier de références | `professionnels.html` : bouton principal de l'en-tête (§H.1), tableau « Lots, normes et documents » (§H.4) ; pied de page de toutes les pages (§A.4) | « Télécharger le dossier de références (PDF, 615 Ko) » ; événement Umami `plaquette_telechargee` |
| Guide bruit | `isolation-acoustique.html`, encadré « Guide à télécharger » (§E.5, §Q.4), avec le formulaire facultatif « Recevoir le guide imprimé » | « Télécharger le guide (PDF, 177 Ko) » |
| Liste de contrôle | `professionnels.html` : carte « Régies et gérances » (§H.2), section méthode en site occupé (§H.3), tableau §H.4 | « Télécharger la liste de contrôle « immeuble habité » (PDF, 3 pages) » |

À corriger dans les libellés du copy deck : la liste de contrôle compte **3 pages** (plan du §Q.3 : recto, verso, modèle), pas 2 ; le dossier compte **5 pages en production** tant que la page « Immeubles habités » n'est pas confirmée (6 en preview). Les e-mails de la séquence « aimant » (`automation/messages/sequence-aimant.md`) utilisent les mêmes identifiants (`guide-reduire-le-bruit`, `checklist-chantier-site-occupe`).

## 3. Ce que la production publie (textes de repli)

Aucun code n'est confirmé à ce jour (`tools/build/donnees/confirmations.json` absent). La version production applique donc les replis du copy deck :

- **Dossier** : page « Immeubles habités et lieux publics » masquée (8 points `C20`, `C07`, `C06`, `C09`, `C32` ; encadré de l'offre `C06`, `C28`) ; associés, effectif, GGE, assurance, attestations masqués (`C10`, `C24`, `C11`, `C12`, `C13`) ; « Cloisons isothermes » (`C16`) ; correction de l'écho retirée (`C18`) ; titre « Lots et normes » et lots 271 et 285 seulement (`C14`) ; phrase de normes générique (`C15`, `C33`) ; OMC retirée et « Hôtel à Chavannes-de-Bogis » (`C22`, D4) ; mention « Références citées avec l'accord… » masquée ; bandeau de contact : « Mobile » et andy.construct@bluewin.ch (`C30`) ; interlocuteurs, inscription et visite de chantier masqués (`C09`, `C38`, `C13`, `C40`). Légendes des trois chantiers : textes de repli du §G.3 (`C25`).
- **Guide** : « quelques centimètres » (`C18`), étapes 2 et 3 réduites (`C06`, `C07`), horaires masqués (`C03`).
- **Liste de contrôle** : aucun code à confirmer. Le « Bon à savoir » (art. 259d et 260 CO) attend une **relecture juridique** (`[À VÉRIFIER]` du copy deck).

Choix de mise en page à connaître : photo de couverture `faux-plafond-placo-gorge-lumineuse-01` (placo, classée « M » en §8.4) ; trois chantiers P1, P2, P4 et photo P3 (« M » ou « N » sans condition) ; logo de Grisogono jamais affiché, même en preview (marque rachetée par un tiers qui n'a pas été client, `logos-references.md`) ; carte de la zone tirée des données du site (`tools/build/carte.py`, en lecture seule) ; dans la liste de contrôle, « (modèle au verso) » devient « (modèle en page 3) », avec des champs à remplir (immeuble, travaux, entreprise, responsable) et une page de notes ; dans le guide, schémas sans chiffre et grille A/B/C pour comparer trois entreprises. Le modèle d'avis en Word (§Q.3) n'est pas produit : le modèle figure en page 3 du PDF.

## 4. Mettre à jour les PDF

1. Confirmer les points dans `tools/build/donnees/confirmations.json` (même fichier que le site, D6). Formes acceptées : `{"C06": true}`, `{"C06": {"confirme": true}}` ou `{"confirmations": {...}}`.
2. Saisir les valeurs fournies par le client dans `livrables/sources/valeurs-supports.json` : effectif (`C24`), interlocuteurs (`C09`, `C38`), année et nature des travaux de chaque référence (`C22`).
3. Pour un logo autorisé par écrit : passer son `statut` à `autorise` dans `site/assets/img/references/logos.json` ; il apparaît alors aussi en production.
4. Un texte change : le modifier dans le copy deck, puis dans `livrables/sources/generer_supports.py` (textes repris mot pour mot, une fonction par page).
5. Régénérer et contrôler les aperçus :

```bash
python3 livrables/sources/generer_supports.py --apercus /tmp/apercus-supports
```

Le script s'arrête si un texte déborde de sa page (`--brouillon` pour voir le défaut). Dépendances : `reportlab`, `svglib`, `fonttools`, `brotli`, `pypdf`, `Pillow`, et `pdftoppm` (poppler) pour les aperçus. La date d'édition est celle du jour (`--date AAAA-MM-JJ` pour la fixer). Après régénération, reporter les poids dans les libellés du site.

## 5. Fichier de suivi (Excel)

- **Onglets** : Mode d'emploi · Demandes (500 lignes prêtes, colonnes alignées sur le formulaire : canal, source, type de client, service, commune, NPA, canton, surface, délai, fichier joint, message ; puis zone, score et priorité calculés, statut, dates de contact, de visite, d'offre et de signature, montant, motif de perte, avis) · Pipeline · KPI mensuels · Objectifs · Paramètres.
- **Score** : même grille que l'API (`site/api/data/scoring.json`) et même table NPA → zone (`site/api/data/zones.json`), règles du §2.5 comprises (jamais sous B, urgence, hors cible). Vérifié sur les exemples du §2.6 et sur des cas limites.
- **Alertes** : la colonne « À faire » signale les retards (premier contact, visite, offre, relances J+3 / J+10 / J+21, clôture à J+35, avis à J+2) et les informations manquantes ; les lignes en retard passent en rouge pâle.
- **Démarrage** : supprimer les 5 lignes « EXEMPLE » (jaunes), saisir le mois de mise en ligne dans « Objectifs ». Les objectifs repris sont ceux du scénario M (§1.1, référence) ; le tableau S/M/L à 12 mois est à côté.
- **Mise à jour** : le fichier se tient à la main. `livrables/sources/generer_suivi_xlsx.py` le recrée à neuf (il **écrase** les données saisies) ; ne le relancer que pour changer la structure, puis recalculer avec LibreOffice ou Excel.
- **Données personnelles** : fichier à garder sur un poste protégé ; prospects sans suite effacés 24 mois après le dernier contact (durée à valider, stratégie §9.1).
