# Dossier client : Andy Construct (v2)

**Rôle :** enquêteur / documentaliste (phase 1 du programme v2)
**Date de consultation de toutes les sources :** 31.10.2026
**Usage :** nourrir le copywriting, la preuve sociale et les fiches projets du site v2. Ce dossier ne contient **aucune donnée inventée** : ce qui n'a pas pu être vérifié est signalé comme tel, avec un niveau de confiance.

> **Méthode.** Requêtes HTTP directes (curl), WebFetch, WebSearch, DuckDuckGo (version HTML), API publiques (Zefix, RDAP nic.ch, simap.ch), archives PDF de la FOSC (shab.ch), lecture des données structurées des pages (JSON embarqués). Pour les photos de l'ancien site, nous avons lu les **en-têtes EXIF** par requêtes partielles (dates, appareil, présence de GPS) et regardé des **vignettes de 150 à 300 px**, supprimées aussitôt après examen. Aucune photo de personne n'a été conservée, aucune n'a été copiée dans le projet.
>
> **Limites.** Facebook et Instagram exigent une connexion. Google (fiche et avis) n'est pas consultable sans navigateur. La Wayback Machine refuse la connexion depuis notre environnement. Plusieurs annuaires bloquent les robots (Kompass, Cybo, Infobel, business-monitor, companexia, edirex). Pour ces sources, seuls les extraits affichés par les moteurs de recherche ont été relevés.

---

## 0. Synthèse : ce qui est nouveau par rapport aux documents existants

1. **Facebook n'a rien livré d'exploitable.** `facebook.com/andyconstruct.bajrami` est un **profil personnel** (et non une Page) nommé « Andyconstruct Bajrami » (identifiant 100003226826924). Tout son contenu (publications, photos, « À propos », amis, commentaires) est derrière la barrière de connexion, et aucun moteur n'en indexe le contenu. Aucune Page Facebook « Andy Construct » n'a été trouvée.
2. **L'historique complet du registre du commerce est reconstitué** (4 publications FOSC). L'activité a commencé le **01.06.2007 à Perly-Certoux**, avec deux associés fondateurs, Adnan Bajrami et Silvio Chanton. Le siège est passé à **Chêne-Bourg en 2010**, puis à **Carouge en 2023** : Silvio Chanton sort alors de la société et Caroline Chanton Bajrami y entre. Le « 2010 » de l'ancien site correspond à l'année du déménagement et à l'**enregistrement du domaine andyconstruct.ch (01.03.2010)**, et non à la fondation.
3. **Le but social inscrit au registre du commerce couvre exactement les 4 services validés**, dans une formulation officielle réutilisable : « Pose de faux-plafonds phoniques et cloisons légères phoniques et thermiques, isolations intérieures, plâtrerie, peinture, aménagement de logements et bureaux. »
4. **Andy Construct figure dans l'annuaire des « Entreprises membres du GGE »** (groupement patronal genevois du bâtiment, fondé en 1963). C'est un signal de confiance à faire confirmer et autoriser par le client.
5. **Les photos publiques sont toutes datées entre août 2012 et février 2016** (EXIF). Aucune photo publique n'est plus récente. **7 paires avant/après** ont été identifiées dans la galerie « Avant / Après ». Aucune photo ne contient de coordonnées GPS.
6. **Aucun avis client public n'existe**, sur aucune plateforme consultée : local.ch 0, search.ch 0, Yelp 0 (fiche non revendiquée), Infobel 0. Facebook et Google n'ont pas pu être vérifiés.
7. **La Route des Acacias 48 héberge 92 autres entreprises actives** (Moneyhouse). Il s'agit probablement d'une adresse de domiciliation, ce qui a des conséquences pour la fiche Google.
8. **La taille de l'entreprise est petite** : « 2-10 employés » selon LinkedIn (déclaratif) et « 1-2 travailleurs » selon les données SITG de 2021. Le chiffre exact reste à demander.

---

## 1. Tableau des sources

Légende : **O** = accessible et lu ; **P** = partiellement accessible ; **N** = non accessible (seuls les extraits des moteurs ont été relevés, quand ils existent).

### 1.1 Réseaux sociaux

| # | Source | URL | Accès | Consulté | Contenu utile |
|---|---|---|---|---|---|
| S1 | Facebook, profil « Andyconstruct Bajrami » | https://www.facebook.com/andyconstruct.bajrami | **N** | 31.10.2026 | `www` et `m.` : HTTP 400/302 vers `/login`. `mbasic.` : redirection vers la connexion (« deprecated »). Avec un agent de prévisualisation de liens, la page vide (sans contenu) répond : titre « Andyconstruct Bajrami (@andyconstruct.bajrami) », description générique « Andyconstruct Bajrami est sur Facebook. Inscrivez-vous… », type **profil** (`ProfileCometLoggedOutRoute`), userID 100003226826924. `/about` et `/photos` redirigent vers la connexion. **Aucune publication, photo, date, aucun commentaire ni nombre d'abonnés visible.** C'est ce profil que vise l'icône Facebook de l'ancien site (lien `sharer.php?u=…andyconstruct.bajrami?fref=ts`). |
| S2 | Facebook, profil « Andy Construct » | https://www.facebook.com/andy.construct.3/ | N | 31.10.2026 | Profil personnel (ID 100029566320705) listé dans l'annuaire public Facebook. **Rien ne permet de l'attribuer à l'entreprise.** |
| S3 | Facebook, profil « Andy Bajrami » | https://www.facebook.com/andy.bajrami/ | N | 31.10.2026 | Profil personnel trouvé par DuckDuckGo. Attribution inconnue, **non exploité** (vie privée). |
| S4 | Instagram @andyconstruct | https://www.instagram.com/andyconstruct/ | N | 31.10.2026 | Connexion obligatoire, API bloquée. D'après l'extrait du moteur : « 25 Followers, 9 Following, 0 Posts », bio vide. **Attribution non confirmée** (plusieurs entreprises « Andy Construct » existent, notamment en Roumanie). |
| S5 | Instagram @andy.bajrami | https://www.instagram.com/andy.bajrami/ | N | 31.10.2026 | Compte personnel (1 081 abonnés, 0 publication d'après l'extrait). **Non exploité.** |
| S6 | LinkedIn, page entreprise | https://www.linkedin.com/company/andy-construct-chanton-et-cie | **O** | 31.10.2026 | Nom « Andy Construct ». Secteur « Services relatifs aux bâtiments ». **9 abonnés.** Taille « **2-10 employés** ». Type « Société indépendante ». Domaines « Faux plafonds, Tissu tendu et Cloisons ». Siège Route des Acacias 48, 1227 Les Acacias. Description : « Entreprise spécialisée dans la pose de faux plafonds, tissu tendu et cloisons. » Aucune publication visible sans connexion. |

### 1.2 Ancien site et données techniques

| # | Source | URL | Accès | Consulté | Contenu utile |
|---|---|---|---|---|---|
| A1 | Ancien site : 17 pages du menu | https://www.andyconstruct.ch/ (liste complète en annexe A) | **O** | 31.10.2026 | Le texte des pages Accueil, Présentation, Références et Contact est identique aux copies de `docs/source/`. Les **11 pages produits et la galerie avant/après ne contiennent aucun texte** : seulement un titre et une galerie (plugin sigplus), sans légende, sans `alt` ni date. **Aucun PDF.** |
| A2 | sitemap.xml | https://www.andyconstruct.ch/sitemap.xml | O | 31.10.2026 | 17 URL avec `index.php`, sans `www`. |
| A3 | En-têtes EXIF des 214 photos des galeries | `/images/…` (voir §5) | O | 31.10.2026 | Les 95 photos « Divers » sont datées du **22.08.2012 au 15.02.2016**, prises avec un Panasonic DMC-TZ25, un iPhone 5 puis un iPhone 5s. **Aucune n'a de GPS.** Les photos des galeries produits et avant/après ont été redimensionnées (800 à 1024 px) et n'ont plus d'EXIF. |
| A4 | RDAP nic.ch | https://rdap.nic.ch/domain/andyconstruct.ch | O | 31.10.2026 | Domaine **enregistré le 01.03.2010**, registraire Kreativ Media GmbH. |
| A5 | Code source de l'ancien site | idem A1 | O | 31.10.2026 | Joomla, gabarit `andy_2017_2` (refonte en 2017), logo `logo_andy_construct2016_grisbleu` (logo bleu de 2016), Google Analytics `UA-17202698-1` (identifiant de la période 2010), crédit « Webdesign: iMedia Solutions ». |
| A6 | Wayback Machine | https://web.archive.org/ | **N** (connexion réinitialisée) | 31.10.2026 | L'API de disponibilité répond. Des captures existent au **20.10.2012**, au 16.05.2014, au 16.12.2014, au 19.09.2017 et au 22.10.2023, mais elles n'ont pas pu être lues. **Piste pour récupérer d'anciens textes (avant 2017).** |

### 1.3 Registres officiels et agrégateurs

| # | Source | URL | Accès | Consulté | Contenu utile |
|---|---|---|---|---|---|
| R1 | Zefix (API REST) | https://www.zefix.ch/ZefixREST/api/v1/firm/876831.json | **O** | 31.10.2026 | Statut « existante ». IDE CHE-113.706.162, n° RC CH-660-1539007-3. Siège Carouge (GE), adresse Route des Acacias 48. **But social** (voir §2.1). Dernière publication : 02.05.2023. |
| R2 | FOSC 126/2007, 03.07.2007 (PDF) | https://www.shab.ch/shabforms/servlet/Search?EID=7&DOCID=4005334 | O | 31.10.2026 | Création. Voir §2.1. |
| R3 | FOSC 44/2010, 04.03.2010 (PDF) | https://www.shab.ch/shabforms/servlet/Search?EID=7&DOCID=5524708 | O | 31.10.2026 | Transfert à Chêne-Bourg et nouveau but social. |
| R4 | FOSC du 19.12.2013 (PDF) | https://www.shab.ch/shabforms/servlet/Search?EID=7&DOCID=7225832 | O | 31.10.2026 | Liste collective d'attribution des numéros IDE (Andy Construct, Chêne-Bourg, CHE-113.706.162). Aucune autre modification. |
| R5 | FOSC du 02.05.2023 (Moneyhouse, Zefix) | https://www.moneyhouse.ch/fr/company/andy-construct-chanton-cie-3813590051/messages | O | 31.10.2026 | Transfert à Carouge, changement d'associés. Publication n° HR02-1005737267. |
| R6 | Moneyhouse | https://www.moneyhouse.ch/fr/company/andy-construct-chanton-cie-3813590051 | **P** | 31.10.2026 | Secteur « Autres aménagements (y c. aménagement intérieur) ». Direction : 2 associés actifs, 1 inactif. « **À la même adresse il existe 92 autres entreprises actives** ». Chêne-Bourg en « autre adresse ». Chronologie : événements en 2007, 2010 et 2023. Chiffre d'affaires et employés réservés aux abonnés payants. Aucune demande de construction, aucune offre d'emploi. |
| R7 | Registre du commerce de Genève (extrait cantonal) | http://app2.ge.ch/ecohrcinternet/extract?lang=FR&companyOfsUid=CHE-113.706.162 | **N** | 31.10.2026 | Application JavaScript dont l'API répond 403 (captcha). Les mêmes informations sont disponibles via la FOSC et Zefix. |
| R8 | yellowpages.swiss (help.ch) | https://yellowpages.swiss/company/CHE-113.706.162/andy-construct-chanton-cie-carouge-ge | O | 31.10.2026 | Inscription au RC le 27.06.2007. « 3 publications » FOSC dans sa base. But social traduit en anglais. Autres sociétés à la même adresse (CONCEPT VENTURES Sàrl, AO Imagine Sports SA, MSP Global Sàrl). Aucun communiqué. |
| R9 | business-monitor.ch | https://business-monitor.ch/fr/companies/357102-andy-construct-chanton-cie | N (403) | 31.10.2026 | D'après l'extrait du moteur : « Société en nom collectif basée à Carouge (GE)… fondée en 2007 ». |
| R10 | companexia | https://companexia.com/fr/companies/andy-construct-chanton--cie.dCJP6XpDXv-3oUKPlTQLvA.html | N (403) | 31.10.2026 | Profil généré automatiquement. Rien de plus. |

### 1.4 Annuaires professionnels et grand public

| # | Source | URL | Accès | Consulté | Contenu utile |
|---|---|---|---|---|---|
| D1 | local.ch | https://www.local.ch/fr/d/carouge-ge/1227/revetement-des-plafonds-et-plafonds-suspendus/andy-construct-chanton-cie-OGrZ5DP4atJqYki9WoTjPg | **O** | 31.10.2026 | **Inscription Premium**, avec un **texte rédigé par l'entreprise** (cité intégralement au §3). Slogan « plafonds, peinture et cloisons ». Catégories : Revêtement des plafonds et plafonds suspendus, Peintre, Cloisons. Horaires **lu-ve 07:00-18:00**. Tél. 022 771 20 15, mobile 078 631 14 34 marqué « * » (ne souhaite pas de publicité). Zone de travail « Murs, Plafonds ». Langue : français. **« Pas encore d'avis »**. Le logo affiché est l'**ancien logo bleu**. Aucune photo de galerie. |
| D2 | search.ch | https://search.ch/tel/carouge/route-des-acacias-48/andy-construct-chanton-cie | **O** | 31.10.2026 | Même texte que local.ch (source SwisscomDirectories). Catégories : Revêtement des plafonds…, Entreprise de Peinture, Cloisons, Plâtrerie-peinture, **Sonorisation** (erreur), Parois mobiles, Protection acoustique. **0 avis.** Lien vers la fiche GGE. L'ancienne URL (Chêne-Bourg) redirige vers Carouge. |
| D3 | GGE, fiche entreprise | https://gge.ch/entreprises-2/andy-construct-chanton-cie/ | **O** | 31.10.2026 | Fiche publiée dans l'annuaire titré « **Entreprises membres du GGE** ». Adresse Route des Acacias 48, 1227 Carouge. **Seul le mobile est indiqué.** Métiers : « Gypserie - peinture », « Plafonds suspendus/faux plaf. ». Secteurs : « GGE - Peinture, gypserie », « GGE - Second Oeuvre autres ». Fiche en ligne depuis le 07.11.2024 (date de la nouvelle version du site du GGE, et non date d'adhésion). |
| D4 | GGE, présentation | https://gge.ch/le-gge-2/ | O | 31.10.2026 | Le GGE est un « Groupement patronal d'entreprises du bâtiment et du génie civil », « existe depuis 1963 ». Il représente ses membres notamment auprès de la commission paritaire du second œuvre genevois (CPSO). |
| D5 | GGE, ancienne fiche « GAP : Portrait Société » | http://www.gge.ch/portrait?id=33 | N (404) | 31.10.2026 | Encore listée par les moteurs. **Indice d'une adhésion plus ancienne**, à confirmer. |
| D6 | Kompass | https://ch.kompass.com/fr/c/andy-construct-chanton-cie/ch267619/ | N (405, anti-robot) | 31.10.2026 | D'après les extraits : domaine d'activité = but social du RC. Classement : « **Carpentry and structural woodwork** » (charpenterie), **erroné**. |
| D7 | architecteromand.ch (2 URL) | https://architecteromand.ch/company/andy-construct-chanton-cie · https://www.architecteromand.ch/architecte/38240~andy-construct-chanton-cie | N (404) | 31.10.2026 | Fiches supprimées ou déplacées. Les moteurs les affichent encore à **Chêne-Bourg**. |
| D8 | edirex.ch | https://edirex.ch/fr/annuaire/andy-construct-chanton-cie | N (429, contrôle anti-robot Vercel) | 31.10.2026 | D'après les extraits : « Andy Construct, Chanton & Cie · **Chêne-Bourg** ». |
| D9 | firmen.ch | https://www.firmen.ch/de/Chene+Bourg/Andy+Construct+Chanton+Cie/119171/portrait.htm | **O** | 31.10.2026 | Adresse **avenue de Bel-Air 57, Chêne-Bourg**, tél., mobile, e-mail, site. Branches : Baugewerbe, Deckenverkleidung Wandverkleidung, Gipsergeschäft, Malergeschäft, Interieur & Möbel, Sonstiges. Aucune description. Fiche créée le 23.11.2017. |
| D10 | Yelp | https://fr.yelp.ch/biz/andy-construct-ch%C3%AAne-bourg | **O** | 31.10.2026 | « Andy Construct », **Chêne-Bourg**, catégorie « Peintre ». **0 avis, fiche non revendiquée.** **11 photos** mises en ligne le 03.07.2018, avec la légende « Toutes les images sont nos propres réalisations » (probablement reprises de l'ancienne galerie local.ch). Voir §5.4. |
| D11 | Infobel (2 fiches) | …/chene_bourg/CH101568668-0227712015/… · …/carouge_ge/CH100597429-0227712015/… | N (403) | 31.10.2026 | D'après les extraits : **doublon**, une fiche à Chêne-Bourg (MAJ 29.05.2025) et une à Carouge (MAJ 02.05.2025). « 0 Commentaires ». |
| D12 | Cybo | https://fr.cybo.com/CH-biz/andy-construct-chanton-cie | N (403) | 31.10.2026 | D'après les extraits : **Chêne-Bourg**. Catégories **erronées** (« General chemical wholesale », « Shopping other », « Other wholesale activities »…). |
| D13 | Esprit de Genève | https://espritdegeneve.ch/andy-construct-chanton-cie/ | O (WebFetch) | 31.10.2026 | Chêne-Bourg, mobile seul. Activité « Pose de plafonds et de cloisons ». Branche « Montage de menuiseries » (erronée). Catégorie « Bureau/étude/cabinet ». « **1-2 travailleurs** ». Données « extraites en date du 26 novembre 2021 » du SITG, fiche publiée le 16.10.2022. |
| D14 | guidegeneve.ch | https://guidegeneve.ch/company/andy-construct-chanton-cie | N (301 vers commercants.ch) | 31.10.2026 | D'après l'extrait : Chêne-Bourg, mobile. |
| D15 | MapsArch | https://app.mapsarch.com/profile/11483/andy-construct | O (JSON) | 31.10.2026 | Profil **créé automatiquement le 13.10.2025** (offre gratuite, non vérifié). Adresse Chêne-Bourg. Texte copié de l'ancien site. Taille « 2-10 ». Spécialités **erronées** (« Hearing aid store », « Handyman »). |
| D16 | emploisuisse.com | https://emploisuisse.com/annuaire/andy-construct | N (500) | 31.10.2026 | D'après l'extrait : Carouge, tél. +41227712015, « avis » (rien de visible). |
| D17 | Houzz | https://www.houzz.fr/professionnels/query/andy-construct | O | 31.10.2026 | **Aucun profil.** |
| D18 | Renovero | https://www.renovero.ch/ | O | 31.10.2026 | **Aucun profil trouvé** (recherche par nom et URL type : 404). |
| D19 | Fiche Google et avis Google | — | **N** | 31.10.2026 | Google exige JavaScript. **Existence, gestionnaire et avis non vérifiables.** |

### 1.5 Mentions tierces (presse, marchés publics, clients, architectes)

| # | Source | URL | Accès | Consulté | Contenu utile |
|---|---|---|---|---|---|
| T1 | simap.ch (API publique) | https://www.simap.ch/api/publications/v2/project/project-search | O | 31.10.2026 | La recherche porte sur les titres et les adjudicateurs, **pas sur les adjudicataires**. Aucun résultat pour « Andy », « Chanton » ou « Bajrami ». Les archives d'avant juillet 2024 ne sont pas accessibles. **Aucune adjudication trouvée.** |
| T2 | FAO Vaud / FAO Genève, recherche web | — | N / aucun résultat | 31.10.2026 | Aucune mention trouvée. |
| T3 | Ville de Genève, fiche « Alhambra rénovation et extension » (triptyque n° 44, 2015) | https://www.geneve.ch/sites/default/files/2024-07/2015_triptyque%20n%C2%B044_alhambra_r%C3%A9novation%20et%20extension.pdf | O | 31.10.2026 | Travaux du **02.04.2012 au 15.03.2015**, inauguration le 27.03.2015, architectes Architech SA. **Seuls les mandataires y figurent, pas les entreprises** : aucune mention d'Andy Construct. |
| T4 | Presse, sites de communes, sites des clients de référence (Conservatoire, Alhambra, salles communales de Collonge-Bellerive et Plan-les-Ouates, Harmonie Nautique, Energestion, Dipan, Covance, Chavannes-de-Bogis), sites d'architectes | recherches web | — | 31.10.2026 | **Aucune mention d'Andy Construct trouvée.** Aucune référence n'est confirmée par un tiers. |
| T5 | GitHub, dépôt de la maquette | https://github.com/rayhanhasan/andy-construct | O | 31.10.2026 | **Dépôt public et indexé par les moteurs.** Voir §6, point I-14. |

### 1.6 Fausse piste écartée

Un moteur a attribué l'adresse « Route des Hospitaliers 137, 1257 La Croix-de-Rozon » à Andy Construct. La vérification sur la page de catégorie de local.ch montre que cette adresse appartient à **E.S.D Sàrl**, listée juste après Andy Construct. **Elle ne concerne pas le client.**

---

## 2. Faits vérifiés

Confiance : **Élevée** = source officielle ou constat direct ; **Moyenne** = déclaration de l'entreprise ou recoupement ; **Faible** = déduction ou estimation.

### 2.1 Identité et histoire

| Date | Fait | Source | Confiance |
|---|---|---|---|
| 01.06.2007 | Début de l'activité de la « nouvelle société en nom collectif » **Andy Construct, Chanton & Cie**, à **Perly-Certoux**, route de Base 81. Objet : « gypserie-peinture, faux-plafonds et cloisons, notamment aménagement de bureaux ». | FOSC 126/2007 (R2) | Élevée |
| 27.06.2007 | Inscription au journal du registre du commerce de Genève (n° 8309). Publication FOSC le 03.07.2007. | R2, R8 | Élevée |
| 2007 | Associés fondateurs : **Adnan Bajrami** et **Silvio Chanton**. Adnan Bajrami a la signature individuelle depuis le 03.07.2007. | R2, R6 | Élevée |
| 01.03.2010 | Enregistrement du domaine **andyconstruct.ch** (lancement du site, avec un suivi Google Analytics de la même période). | A4, A5 | Élevée (domaine) / Moyenne (lien avec le « © 2010 ») |
| 26.02.2010 | Transfert du siège à **Chêne-Bourg**, avenue de Bel-Air 57 (FOSC du 04.03.2010). **Nouveau but social**, inchangé depuis : « pose de faux-plafonds phoniques et cloisons légères phoniques et thermiques, isolations intérieures, plâtrerie, peinture, aménagement de logements et bureaux ». | FOSC 44/2010 (R3), Zefix (R1) | Élevée |
| 19.12.2013 | Attribution de l'IDE **CHE-113.706.162** (publication collective). | R4 | Élevée |
| 2016-2017 | Logo bleu (fichier daté 2016) et refonte du site (gabarit « andy_2017_2 »). | A5 | Moyenne |
| 27.04.2023 | Transfert du siège à **Carouge (GE)**, Route des Acacias 48 (FOSC du 02.05.2023). Chêne-Bourg reste inscrite comme « autre adresse ». **Silvio Chanton n'est plus associé.** **Caroline Chanton Bajrami** devient associée avec signature individuelle. | R5, R1, R6 | Élevée |
| 31.10.2026 | Société **active**. Forme : **société en nom collectif** (aucune Sàrl inscrite). Associés : Adnan Bajrami et Caroline Chanton Bajrami, tous deux avec signature individuelle. | R1, R6 | Élevée |

Remarques :
- **Origine du nom « Andy »** : aucune source ne l'explique. Le profil Facebook s'appelle « Andyconstruct Bajrami ». Question à poser au client.
- **Ce qu'il faut afficher :** « depuis 2007 » (début de l'activité le 01.06.2007). Le « 2010 » de l'ancien site correspond à la création du site et au déménagement à Chêne-Bourg.
- Les publications de la FOSC contiennent des données personnelles des associés (origine, domicile). **Elles ne sont pas reprises ici** et n'ont aucune utilité pour le site. Retenir seulement que l'adresse de Chêne-Bourg est probablement liée à leur domicile : **ne pas la publier sans accord**.

### 2.2 Dirigeants et équipe

| Fait | Source | Confiance |
|---|---|---|
| Deux associés en nom collectif : Adnan Bajrami (depuis 2007) et Caroline Chanton Bajrami (depuis 2023), chacun avec signature individuelle. | R1, R5, R6 | Élevée |
| Associé fondateur sorti en 2023 : Silvio Chanton (le « Chanton » de la raison sociale). | R5 | Élevée |
| Taille : « 2-10 employés » (LinkedIn, déclaratif) ; « 1-2 travailleurs » (SITG, données du 26.11.2021, reprises par Esprit de Genève). **Effectif réel inconnu.** | S6, D13 | Moyenne (petite structure) / Faible (chiffre exact) |
| L'équipe porte une tenue de travail marquée « Andy Construct » (poseur en t-shirt sur IMG_5922, décembre 2015). | `docs/selection-photos.md` + EXIF | Moyenne |
| Équipements visibles sur les photos de 2015 : échafaudages roulants et nacelle (grande salle, décembre 2015). Travaux en hauteur dans des salles publiques. | Photos IMG_5942/5943 (écartées) | Moyenne |

### 2.3 Spécialités

| Fait | Source | Confiance |
|---|---|---|
| **But social officiel** : faux-plafonds phoniques, cloisons légères phoniques et thermiques, isolations intérieures, plâtrerie, peinture, aménagement de logements et bureaux. **Il couvre les 4 services validés** (placo, peinture, isolation acoustique, cloisons isothermes). | R1, R3 | Élevée |
| Liste détaillée publiée par l'entreprise (local.ch et search.ch Premium). **Plafonds** : tissu tendu (dont « haute performance acoustique et décoratif »), suspendu, métallique, placoplâtre, fibre minérale, fibre de bois, acoustique, phonique, décoratif, isolant thermique, isolant phonique et acoustique. **Cloisons** : légère, plâtre phonique et acoustique, mobile, vitrée, thermique, doublage, isolation intérieure. **Autres poses** : habillage des murs en tissu tendu, caissons lumineux directs et indirects, trappes de visite, chapes flottantes contre les bruits d'impact, protections anti-feu, puits de lumière dans le faux-plafond. | D1, D2 | Moyenne (déclaratif) |
| Ancien site : 11 rubriques produits. Plafonds : tissu tendu à froid, phoniques et acoustiques, placoplâtre, fibre de bois, fibre minérale, bac métallique. Cloisons : légères en placoplâtre, mobiles en aluminium. Isolation thermique ou phonique. Cadres acoustiques. | A1 | Moyenne |
| LinkedIn : domaines « Faux plafonds, Tissu tendu et Cloisons ». | S6 | Moyenne |
| GGE : métiers « Gypserie - peinture » et « Plafonds suspendus/faux plaf. ». | D3 | Moyenne |
| **Écart avec le positionnement v2** : toute la présence publique (ancien site, local.ch, LinkedIn) met en avant les faux-plafonds, le **tissu tendu** et les cadres acoustiques. La **peinture** n'a aucune photo publique. Le terme « cloisons isothermes » n'apparaît nulle part ; les sources disent « cloisons… thermiques », « doublage », « isolation intérieure ». | Recoupement | Élevée |

### 2.4 Chantiers et clients

**Références déclarées** (ancien site, page « Références clients », sans date ni prestation) : Ville de Genève ; Salle communale de Collonge-Bellerive ; Piaget ; Conservatoire de Musique Genève ; Salle de l'Alhambra ; Mairie de Plan-les-Ouates (salle communale) ; Laboratoire Covance CLS SA ; De Grisogono ; Energestion Ingénieurs & Architectes SIA ; Domaine des Perrières - Coppet VD ; Dipan SA - Nyon VD ; Haute Ecole d'Art et de Design Genève ; OMC ; Celgene ; Bank Sarasin ; UBS ; Hôtel Chavannes-de-Bogis ; Harmonie Nautique Genève.
→ Confiance **Moyenne** (déclaration de l'entreprise). **Aucune n'est confirmée par une source tierce.**

**Indices photographiques** (confiance Faible à Moyenne, à confirmer par le client) :

| Indice | Date (EXIF) | Ce que l'on voit | Lien possible |
|---|---|---|---|
| IMG_1702 (écartée) | 07.01.2015 | Logo **OMC/WTO** bien visible | Chantier pour l'OMC (référence « OMC ») |
| IMG_1806 / IMG_1820 | 20.01.2015 | Cloisons modulaires vitrées dans des bureaux | Même chantier que IMG_1702 ? |
| Série IMG_5920 à 5970 | 08 au 15.12.2015 | Grande **salle publique** avec verrière, îlots suspendus lumineux, puits de lumière, rangées de chaises | Salle communale (Plan-les-Ouates ? Collonge-Bellerive ?) : **à identifier** |
| Séries IMG_6487 à 6490 et IMG_6630 à 6636 | 01.02.2016 et 15.02.2016 | **Salle de spectacle** aux fauteuils bâchés, travail en hauteur | Lieu inconnu. Les travaux de l'Alhambra étaient terminés en mars 2015 (T3), il s'agit donc probablement d'un autre lieu, **à identifier**. |
| Galerie « tissu tendu », photo 03 | n.d. | Présentoir de marque **CORUM** (horlogerie) | Boutique ou showroom : référence non listée, accord nécessaire |
| Galerie « cadres acoustiques », photo 03 | n.d. | Vitrophanie « Sugar… » partiellement lisible | Inconnu |
| Galeries placo et phonique, photos 01/19/20 | n.d. | **Piscine intérieure** sous verrière (villa) | Particulier haut de gamme |

### 2.5 Zones réellement servies (preuves publiques)

| Zone | Preuves | Confiance |
|---|---|---|
| Canton de Genève | Sièges successifs (Perly-Certoux, Chêne-Bourg, Carouge) ; références Ville de Genève, Collonge-Bellerive, Plan-les-Ouates, HEAD, Conservatoire, OMC ; membre du GGE | Élevée |
| Vaud, La Côte (district de Nyon) | Références Coppet, Nyon, Chavannes-de-Bogis ; meta description de l'ancien site « Genève - Vaud » | Moyenne |
| NE, FR, Valais romand, JU, Jura bernois | **Aucune preuve publique.** La zone « toute la Suisse romande » est validée par le client mais n'est pas documentée. | — |

### 2.6 Coordonnées, horaires, réseaux

| Fait | Source | Confiance |
|---|---|---|
| Horaires : lundi à vendredi, 07:00-18:00 ; samedi et dimanche fermé. | D1, D2 | Moyenne (déclaratif) |
| Fixe 022 771 20 15, présenté comme « T+F » (téléphone et fax) sur l'ancien site ; mobile 078 631 14 34 ; e-mail andy.construct@bluewin.ch. | A1, D1, D2 | Élevée |
| Le mobile est marqué « ne souhaite pas de publicité » sur local.ch et search.ch. | D1, D2 | Élevée |
| Réseaux : profil Facebook personnel « Andyconstruct Bajrami » (lié depuis l'ancien site) ; page LinkedIn (9 abonnés) ; Instagram @andyconstruct (attribution incertaine, 0 publication). | S1, S4, S6 | Élevée (FB, LinkedIn) / Faible (Instagram) |
| Profil Facebook créé vers fin 2011 - début 2012 (estimation d'après la plage de l'identifiant 100003…). | S1 | **Faible** |
| Affiliation : annuaire des « Entreprises membres du GGE ». | D3, D4 | Moyenne-Élevée (statut de membre et date à confirmer) |
| L'entreprise est cliente de localsearch (inscription Premium local.ch / search.ch). | D1 | Élevée |

---

## 3. Voix de l'entreprise

### 3.1 Citations exactes (orthographe d'origine conservée)

**Ancien site, page Présentation**
> « Andy Construct vous souhaite la bienvenue sur notre site. »
> « Notre entreprise basée à Genève est spécialisée dans la pose de faux-plafonds et de cloisons qui, selon les besoins, peuvent être thermiques et/ou phoniques. »
> « Nous sommes à même de réaliser les travaux les plus complexes et d'apporter à vos espaces un confort plus noble ainsi qu'un aspect décoratif. Ceci en conservant les qualités techniques. »
> « Nos idées novatrices nous permettent de vous accompagner (particuliers, architectes, PME, etc.) dans la réalisation de nouvelles conceptions grâce à des matériaux adaptés à vos besoins. »
> « Nous réalisons également la pose de : • Caissons lumineux directs et indirects • Trappes de visites • Chappe flottante (contre les bruits d'impacts) • Protection anti-feu • Puits de lumière dans le faux-plafond »

**Ancien site, Accueil**
> « Plafonds — Spécialisé dans différents type de plafonds à choix. » / « Cloisons — Spécialisé dans différents type de cloisons. » / « Cadres acoustiques — Spécialisé dans différents type de cadres acoustiques. »

**Ancien site, meta description** (toutes les pages)
> « Pose de Plafonds et cloisons Genève - Vaud - Andy Construct Sàrl Suisse »

**local.ch / search.ch** (inscription Premium, texte rédigé ou validé par l'entreprise)
> Slogan : « plafonds, peinture et cloisons »
> « Notre entreprise est spécialisée dans la pose de faux-plafonds et de cloisons qui peuvent être thermiques, phoniques, acoustiques et décoratifs. »
> « Nos idées novatrices nous permettent de vous accompagner dans la réalisation de nouvelles conceptions grâce à des matériaux adaptés à vos besoins. »
> « Toutes les images sont nos propres réalisations »

**LinkedIn**
> « Entreprise spécialisée dans la pose de faux plafonds, tissu tendu et cloisons. »

**Registre du commerce** (formulation officielle, utile pour les mentions légales et le texte « L'entreprise »)
> « Pose de faux-plafonds phoniques et cloisons légères phoniques et thermiques, isolations intérieures, plâtrerie, peinture, aménagement de logements et bureaux. »

**Facebook :** aucune publication lisible. **Le ton employé sur Facebook est inconnu.**

### 3.2 Mots récurrents

- **spécialisé(e)** (6 occurrences sur 4 sources), **pose**, **faux-plafonds**, **cloisons**
- **thermiques / phoniques / acoustiques** (toujours associés), **décoratif**
- **besoins** et **adaptés à vos besoins**, **accompagner**
- **complexes**, **qualités techniques**, **confort**
- **nos propres réalisations**
- lieu : **basée à Genève**, **Genève - Vaud**

### 3.3 Valeurs affichées

1. **Spécialisation** : un métier précis (plafonds et cloisons), pas une entreprise générale.
2. **Capacité technique** : « les travaux les plus complexes », « en conservant les qualités techniques ».
3. **Technique au service du confort et de l'esthétique** : « confort plus noble », « aspect décoratif ».
4. **Sur mesure** : « selon les besoins », « matériaux adaptés à vos besoins ».
5. **Accompagnement** des particuliers, architectes et PME.
6. **Authenticité des preuves** : « Toutes les images sont nos propres réalisations ».

### 3.4 Ton et conseils pour le copy-deck

- Ton **formel, sobre, à la première personne du pluriel**, vouvoiement. Phrases courtes, aucune exagération : **cela correspond à l'audience de 45 à 70 ans**. À garder.
- Points faibles : formules génériques (« idées novatrices », « confort plus noble »), coquilles (« Chappe » → chape, « différents type » → types, « Trappes de visites » → trappes de visite), « Sàrl » erroné.
- **Formules réutilisables telles quelles (ou presque) :**
  - « Toutes les photos sont nos propres réalisations » (sous le portfolio) ;
  - « selon les besoins, thermiques et/ou phoniques » ;
  - « particuliers, architectes, PME » (nommer les publics) ;
  - la phrase du but social pour « L'entreprise » et les mentions légales.
- **Points de prudence :** « Protection(s) anti-feu » ne doit être repris qu'avec précision (produits ou systèmes certifiés AEAI, à confirmer). « Tissu tendu » est absent des 4 services v2 : il faut que le client tranche (question P1-8).

---

## 4. Voix des clients

**Aucun avis client public n'a été trouvé.** Il n'y a donc rien à citer : aucun texte ne doit être produit en ce sens.

| Plateforme | Résultat | Source |
|---|---|---|
| local.ch | « Pas encore d'avis » | D1 |
| search.ch | « Il n'y a pas encore d'avis de clients » | D2 |
| Yelp | 0 avis, fiche non revendiquée | D10 |
| Infobel | « 0 Commentaires » (extrait) | D11 |
| Facebook | Non vérifiable (profil personnel, barrière de connexion). Un profil personnel ne permet pas d'avis du type « Recommandations ». | S1 |
| Google | Non vérifiable | D19 |
| LinkedIn, Houzz, Renovero, presse, sites de clients | Rien | S6, D17, D18, T4 |

Conséquence pour le site : les blocs « témoignages » restent **masqués** (règle du programme v2, §4) tant que le client n'a pas fourni de témoignages réels et autorisés, ou que la campagne d'avis Google n'a pas commencé.

---

## 5. Matériel réutilisable

### 5.1 Avant / après : galerie de l'ancien site (7 paires)

Page : https://www.andyconstruct.ch/realisations/photos-travaux-avant-apres. Fichiers : `https://www.andyconstruct.ch/images/avant_apres/NN.jpg`. Aucune légende, aucune date, pas d'EXIF. **Aucune personne visible.** Les paires se déduisent de l'ordre des fichiers et des vues.

| Paire | Avant | Après | Sujet | Service v2 | Qualité |
|---|---|---|---|---|---|
| 1 | 01.jpg (800×600) | 02.jpg (800×533) | Caisson en cours (plaques jointoyées, grille de ventilation, câbles), puis retombée blanche finie sous verrière | Placo | Moyenne (800 px) |
| 2 | 03.jpg (800×600) | 04.jpg (800×533) | Gaine de ventilation sous charpente, puis couloir au plafond lisse, gaine dissimulée | Placo, isolation | Moyenne |
| 3 | 05.jpg (800×600) | 06.jpg (800×533) | Fenêtre de toit avec encadrement bois, isolant et plafond noirci, puis rampant blanc fini | Isolation, placo (combles) | Moyenne, **paire la plus parlante** |
| 4 | 07.jpg (800×600) | 08.jpg (800×533) | Monobloc de ventilation entre les chevrons, puis caisson fini près d'une fenêtre cintrée | Placo | Moyenne |
| 5 | 09.jpg (800×600) | 10.jpg (800×600) | Réservations circulaires dans la dalle, puis couloir aux **puits de lumière circulaires** | Placo | Moyenne, **paire très visuelle** (même couloir : galerie placo n° 02 et photo Yelp n° 4) |
| 6 | 11.jpg (800×600) | 12.jpg (800×600) | Séjour avant travaux, puis faux-plafond périphérique avec spots (même baie vitrée) | Placo, peinture | Moyenne (12 = galerie placo n° 10) |
| 7 | 13.jpg (800×600) | 14.jpg (650×971) | Ossature métallique d'une paroi cintrée, puis couloir fini avec spots | Placo, cloisons | Moyenne (cadrages différents) |

Limite : 800 px environ, compression web. Ces photos conviennent pour des vignettes ou un curseur avant/après de 800 px maximum, pas pour un héro. **Demander les originaux au client** (question P2-16).

### 5.2 Galeries « produits » de l'ancien site (119 photos, sans texte)

Modèle d'URL : `https://www.andyconstruct.ch/images/<Galerie>/NN.jpg`. Photos redimensionnées (640 à 1024 px), sans EXIF ni GPS.

| Galerie (nb) | Taille | Sujets principaux | Personnes | Points d'attention |
|---|---|---|---|---|
| `Plafonds_en_tissu_tendu_a_froid` (20) | 800-1024 px | Plafonds lumineux, restaurant au plafond et aux murs imprimés (06, 12), murs imprimés (11 « MARR… », 13-14 photo d'une salle de spectacle ancienne, 20 rose), couloirs à gorge lumineuse (01, 10), escalier avec rubalise de chantier (18) | Non vues | **03 : marque CORUM visible**. Hors des 4 services v2 |
| `Plafonds_en_placoplatre` (20) | 800 px | **Piscine intérieure sous verrière** (01, 19, 20), couloir aux puits de lumière (02), charpente apparente et plâtre perforé (05, 16), fenêtre de toit et lustre (09), séjour (10), plafonds lisses avec spots | Non vues | Galerie la plus utile pour le **placo** |
| `Cadres_acoustiques` (11) | 1024 px | Open space aux panneaux acoustiques en damier noir et blanc, îlots suspendus (01, 04, 07), cadre imprimé (08) | **09 : une personne assise au loin**, non identifiable | 03 : vitrophanie de marque. Rattachable à l'**isolation acoustique** |
| `Plafonds_phoniques_et_acoustiques` (8) | 800 px | Piscine (01), charpente et plâtre perforé (03), plaques perforées (05, 06), grilles lumineuses (07, 08) | Non vues | Isolation acoustique |
| `Plafonds_en_fibre_minerale` (10) | 800 px | Open spaces de bureaux, couloir, dalles minérales | Non vues | Postes de travail visibles (bureaux bleus) |
| `Plafonds_en_fibre_de_bois` (4) | 800 px | Panneaux en laine de bois, couloir | Non vues | Caméra de surveillance visible |
| `Cloisons_legeres_en_placoplatre` (10) | 536-800 px | Pièces finies, **ossatures isolées en cours** (07 à 09), mezzanine (10) | Non vues | Utile pour les **cloisons isothermes** (étapes de pose) |
| `Cloisons_mobiles_en_aluminium` (8) | 600-800 px | Cloisons de bureau vitrées, mur rouge | Non vues | Hors des 4 services v2 |
| `Isolation_thermique_ou_phonique` (7) | 800 px | **Isolant (Isover) entre chevrons** (03, 04), doublages (01, 02), mur fini (05 à 07) | Non vues | Utile pour l'isolation (marque d'isolant visible) |
| `Plafonds_en_bac_metallique` (7) | 640-1024 px | Plafonds métalliques, métal perforé noir (03) | Non vues | Hors des 4 services v2 |

### 5.3 Photos « Divers » (page « Photos travaux 2014-2016 ») : dates EXIF (nouveau)

Elles complètent `docs/selection-photos.md`, où figurent les noms exportés et les choix déjà faits. **La page s'intitule « 2014-2016 », mais ses photos vont d'août 2012 à février 2016.** Appareils : Panasonic DMC-TZ25 (2012-2013), iPhone 5 (2014-2015), iPhone 5s (déc. 2015 - févr. 2016). **Aucun GPS.**

| Date (EXIF) | Fichiers | Sujet (voir `selection-photos.md`) |
|---|---|---|
| 22.08.2012 | P1000428 | Plafond tendu, poutres apparentes (retenue) |
| 26.08.2012 | P1000435 | Plafond placo, îlot ovale (retenue ; slogan lisible au mur) |
| 10.01.2013 | P1000517 | Panneaux acoustiques muraux (à la une) |
| 23.04.2013 | P1000755 | Paroi lumineuse imprimée (à la une) |
| 07.07.2013 | P1000780 à P1000796 | Faux-plafond placo à gorge lumineuse, dalles de couloir (retenues) |
| 15.10.2014 | IMG_0708 | Cadre acoustique dans un bureau |
| 07.01.2015 | IMG_1702 | Logo OMC/WTO (écartée, accord écrit nécessaire) |
| 20-21.01.2015 | IMG_1806, IMG_1820, IMG_1837 | Cloisons modulaires vitrées |
| 21.03.2015 | IMG_2464 | Lames métalliques |
| 19.05.2015 | IMG_3255 à IMG_3261 | Cadre acoustique, salle de réunion |
| 10.06.2015 | IMG_3577 | Plafond tendu mat |
| 19.06.2015 | IMG_3661 / IMG_3662 | Habillage placo, niches arrondies |
| 25.06.2015 | IMG_3727 à IMG_3742 | Couronnes lumineuses (commerce ou restaurant) |
| 30.07 - 20.08.2015 | IMG_4210 à IMG_4567 | Chantiers en cours (ossature, joints) ; personnes sur IMG_4211 |
| 07.12.2015 | IMG_5910 | Lames métalliques |
| **08 - 18.12.2015** | **IMG_5920 à IMG_5990** | **Grande salle publique** : ossature des puits de lumière (08.12), îlots lumineux (15.12, **héro IMG_5959**), cadre acoustique imprimé (IMG_5987, 18.12). Personnes sur IMG_5925, IMG_5933.JPG et IMG_5937 |
| 08.01.2016 | IMG_6259 | Lames métalliques |
| **01 et 15.02.2016** | **IMG_6487 à IMG_6490, IMG_6630 à IMG_6636** | **Salle de spectacle** (fauteuils bâchés) ; personnes sur IMG_6487, IMG_6633 et IMG_6634 |
| sans date | IMG_5182, IMG_6630/6631 (1280 px), IMG_6799 | Bacs métalliques de cuisine, etc. |

**La photo publique la plus récente date de février 2016.** Le site v2 doit pouvoir s'appuyer sur des réalisations récentes, à demander au client (question P1-5).

### 5.4 Photos choisies par l'entreprise (Yelp, 03.07.2018)

Ces 11 images, avec la légende « Toutes les images sont nos propres réalisations », montrent ce que l'entreprise considérait comme sa vitrine en 2018. Elles servent de repère pour le portfolio v2. **Aucune personne visible.** Taille environ 1046×700 (`o.jpg`). URL : `https://s3-media0.fl.yelpcdn.com/bphoto/<id>/o.jpg`.

| # | id Yelp | Sujet |
|---|---|---|
| 1 | REPDIG00QwtZP1zqFAfGrw | Piscine intérieure sous verrière (placo) |
| 2 | LM_gOl0pQrovtqofM9KzgA | **Ancien logo bleu** |
| 3 | bh6XFNZjp0NLclcpd5lJgw | Charpente apparente et plafond en plâtre perforé acoustique |
| 4 | k4hGA-HckjEj1ayIA4_9iw | Couloir aux puits de lumière circulaires |
| 5 | jwJ3kPjH71FY_xINjqwxuw | Îlots circulaires suspendus noir et blanc à éclairage indirect (série de décembre 2015) |
| 6 | pQOVPliUHdxZIkBHSwJWTA | Cadre acoustique rouge |
| 7 | yz33j1B8TZnjwz01afeldw | Îlots acoustiques suspendus dans un couloir |
| 8 | 7bpkWkxJz0T1od312Ov7Pw | Open space aux panneaux acoustiques en damier |
| 9 | Rh6acVXsmqxFDKoLpSplzQ | Plafonds lumineux (panneaux tendus) |
| 10 | phNgBsX1xudsiO0gz5PtHQ | Cloisons avec impostes vitrées |
| 11 | hx6_9CB18DJrykIjwBPgYg | Faux-plafond à gorge lumineuse |

Images de l'ancien site non reprises ci-dessus : visuels de l'accueil (`/templates/andy_2017_2/images/designer/…_04.jpg`, `…_07.JPG`, `…_Plafondhome.jpg`) et image de la page Présentation (`/images/editor-content/e504ef12f029ae9a7f5edafe3ef5c467_01.jpg`). La photo de profil Facebook (URL CDN temporaire) **n'a pas été téléchargée**, car elle peut représenter une personne.

### 5.5 Projets pouvant devenir des fiches projets

**Tout est à confirmer par le client** : nom du lieu, maître d'ouvrage, prestation exacte, accord de citation. Les années proviennent des EXIF (confiance Moyenne : date de prise de vue, pas forcément date de fin de chantier).

| # | Titre provisoire | Année | Prestation visible | Lieu | Contrainte visible | Photos | Questions |
|---|---|---|---|---|---|---|---|
| F1 | Grande salle aux îlots lumineux et puits de lumière | déc. 2015 | Ossature, îlots suspendus, plafonds lumineux, cadres acoustiques | Inconnu (salle publique avec verrière) | Travail en hauteur (nacelle, échafaudages), environ une semaine de pose visible (8 au 15.12), salle équipée | IMG_5920 à 5970, 5987 ; Yelp 5 | Quel lieu ? Commune ? Surface ? Délai ? |
| F2 | Salle de spectacle | févr. 2016 | Non identifiable (en cours) | Inconnu | Fauteuils protégés, hauteur | IMG_6487 à 6490, 6630 à 6636 | Lieu ? Prestation (acoustique, peinture) ? |
| F3 | Couloir aux puits de lumière circulaires (avant/après) | n.d. | Placo, découpes circulaires | Inconnu | Réservations dans la dalle | avant_apres 09-10 ; placo 02 ; Yelp 4 | Lieu, année |
| F4 | Combles : isolation et rampant fini sous fenêtre de toit (avant/après) | n.d. | Isolation, placo | Inconnu | Plafond noirci à l'origine | avant_apres 05-06 ; isolation 03-04 | Type d'isolant, performance |
| F5 | Dissimulation de ventilation sous charpente (avant/après) | n.d. | Caissons placo | Inconnu | Gaine et monobloc à intégrer | avant_apres 01-04, 07-08 | Lieu, contexte |
| F6 | Piscine intérieure sous verrière | n.d. | Plafond placo (hydrofuge ?) | Villa (particulier) | Milieu humide | placo 01, 19, 20 ; phonique 01 ; Yelp 1 | Type de plaques, accord du propriétaire |
| F7 | Combles à charpente apparente, plafond acoustique perforé | n.d. | Placo perforé acoustique | Inconnu | Intégration entre les poutres | placo 05, 16 ; phonique 03 ; Yelp 3 | Lieu, usage de la salle |
| F8 | Open space aux panneaux acoustiques en damier | n.d. (2015 ?) | Cadres et îlots acoustiques | Bureaux | Correction acoustique d'un open space | cadres 01, 04, 07 ; Yelp 8 | Client, accord |
| F9 | Bureaux à cloisons modulaires vitrées (OMC ?) | janv. 2015 | Cloisons, plafonds | Peut-être l'OMC (IMG_1702) | Site institutionnel | IMG_1702, 1806, 1820 | Confirmer le lien avec l'OMC |
| F10 | Séjour : faux-plafond périphérique et spots (avant/après) | n.d. | Placo, peinture | Appartement | Pièce habitée | avant_apres 11-12 ; placo 10 | Lieu, année |
| F11 | Restaurant aux couronnes lumineuses | juin 2015 | Plafond tendu lumineux | Commerce | Enseigne visible | IMG_3727 à 3742 | Hors 4 services : à garder ? |

---

## 6. Incohérences à corriger

| # | Incohérence | Où | Correction proposée | Priorité |
|---|---|---|---|---|
| I-1 | « **Andy Construct Sàrl** » alors que la société est une SNC « Andy Construct, Chanton & Cie » | Pied de page et meta description de l'ancien site | Raison sociale exacte dans les mentions légales, « Andy Construct » ailleurs | Haute |
| I-2 | **Adresse Chêne-Bourg** (av. de Bel-Air 57) encore affichée alors que le siège est à Carouge depuis 2023 | Ancien site (Contact), firmen.ch, Yelp, Infobel (doublon), Cybo, Esprit de Genève, guidegeneve, MapsArch, edirex, architecteromand (index) | Une seule adresse partout, après décision du client (P1-1) | Haute |
| I-3 | **Route des Acacias 48** partagée par **92 autres entreprises actives** : domiciliation probable | Moneyhouse, yellowpages.swiss | Si personne n'y est présent aux heures d'ouverture, déclarer la fiche Google en « zone desservie » sans adresse visible (les bureaux virtuels ne sont pas admis) | Haute |
| I-4 | Année affichée « 2010 » alors que l'activité a commencé le 01.06.2007 | Ancien site (© 2010-2022) | « depuis 2007 » | Haute |
| I-5 | Présence Facebook sur un **profil personnel** et non sur une Page. Lien de l'ancien site vers une fenêtre de **partage**. Autres comptes homonymes (andy.construct.3, Instagram @andyconstruct) d'attribution inconnue. | Facebook, Instagram, ancien site | Créer ou convertir en Page professionnelle, la lier directement, revendiquer ou fermer les doublons | Haute |
| I-6 | **Ancien logo bleu** (2016) encore utilisé | local.ch, search.ch (logo), Yelp (photo 2), ancien site | Remplacer par le logo actuel | Moyenne |
| I-7 | **Catégories erronées** : « Charpenterie » (Kompass), « Sonorisation » (search.ch), « General chemical wholesale » (Cybo), « Hearing aid store » et « Handyman » (MapsArch), « Montage de menuiseries » et « Bureau/étude/cabinet » (Esprit de Genève), « Interieur & Möbel » (firmen.ch), « Peintre » seul (Yelp) | Annuaires | Corriger : plâtrerie / faux-plafonds / cloisons / peinture / isolation | Moyenne |
| I-8 | Téléphones incohérents : fixe indiqué comme fax (« T+F ») ; GGE et Esprit de Genève n'affichent que le mobile ; pied de page de l'ancien site avec le mobile seul ; mobile marqué « pas de publicité » | Ancien site, GGE, local.ch | Choisir le numéro principal (P2-13), retirer le fax | Moyenne |
| I-9 | Services : la présence publique met en avant le tissu tendu, les cadres acoustiques, les cloisons alu et les plafonds métalliques ; la v2 se limite à placo, peinture, isolation acoustique et cloisons isothermes ; **aucune photo de peinture** | Ancien site, local.ch, LinkedIn, GGE | Aligner les textes des annuaires sur les 4 services après décision (P1-8) | Moyenne |
| I-10 | Zone : « Genève - Vaud » (ancien site) contre « toute la Suisse romande » (v2), sans preuve publique hors GE et VD | Ancien site, v2 | Obtenir des références hors GE/VD (P2-9) ou formuler avec prudence | Moyenne |
| I-11 | Page « Photos travaux 2014-2016 » contenant des photos de 2012 à 2016 ; aucune réalisation publique après février 2016 | Ancien site | Dater chaque fiche, ajouter du récent | Moyenne |
| I-12 | Coquilles : « Chappe » → chape ; « différents type » → types ; « Trappes de visites » → trappes de visite ; « Haute Ecole » → Haute école | Ancien site, local.ch | Corriger dans le copy-deck et les annuaires | Basse |
| I-13 | Noms de références à dater ou mettre à jour : Bank Sarasin (aujourd'hui J. Safra Sarasin), Celgene (groupe BMS) ; statut actuel de Covance et De Grisogono à vérifier ; nom exact de « Hôtel Chavannes-de-Bogis » à obtenir. Emblème de l'OMC et armoiries de la Ville de Genève protégés (affichage en texte uniquement). | Page Références | Demander l'année de chaque chantier (P1-4) | Moyenne |
| I-14 | **Dépôt GitHub de la maquette public et indexé** : il contient l'identité du client, les noms des associés, des textes en cours (et ce dossier, s'il est poussé) | github.com/rayhanhasan/andy-construct | Décision de l'agence : passer le dépôt en privé, ou ne rien y pousser de sensible | **Haute (agence)** |
| I-15 | Fiches d'annuaires fantômes : architecteromand.ch en 404 mais encore indexée ; ancienne fiche GGE `portrait?id=33` en 404 ; Infobel en double | Annuaires | Demander la suppression ou la mise à jour (Esprit de Genève l'offre gratuitement) | Basse |

---

## 7. Questions à poser au client (par priorité)

### P1 : bloquantes pour le copywriting, la preuve sociale et la mise en ligne

1. **Adresse publique.** Route des Acacias 48 : est-ce un vrai bureau ou dépôt (avec quelqu'un sur place aux heures d'ouverture) ou une domiciliation ? Peut-on retirer Chêne-Bourg partout ? (Cette adresse ne doit pas être publiée si elle est privée.)
2. **Facebook.** Le profil « Andyconstruct Bajrami » est-il le vôtre ? Qui le gère ? Peut-on créer ou convertir une **Page professionnelle** ? Pouvez-vous nous transmettre, par captures ou export, les **publications, photos et commentaires de clients** qui s'y trouvent ? Seul le titulaire y a accès. Les comptes « Andy Construct » (facebook.com/andy.construct.3) et Instagram @andyconstruct sont-ils les vôtres ?
3. **Fiche Google.** Existe-t-elle ? Qui y a accès ? Combien d'avis compte-t-elle ? (Nous n'avons pas pu la voir.)
4. **Références.** Pour chacune des 18 références : année, prestation, interlocuteur, accord pour citer le nom. Lesquelles datent d'après 2016 ?
5. **Réalisations récentes (2017-2026).** Merci de fournir 5 à 10 chantiers avec photos originales, lieu, année et prestation. Aujourd'hui, aucune photo publique n'est postérieure à février 2016.
6. **Lieux des chantiers photographiés.** Grande salle aux îlots lumineux (décembre 2015) ; salle de spectacle (février 2016) ; bureaux de janvier 2015 où apparaît le logo OMC ; piscine intérieure ; couloir aux puits de lumière ; restaurant aux couronnes lumineuses (juin 2015) ; boutique CORUM.
7. **Équipe.** Combien de personnes (associés, ouvriers, apprentis) ? Qui fait quoi ? Peut-on nommer Adnan Bajrami et Caroline Chanton Bajrami sur la page « L'entreprise » ? D'où vient le nom « Andy » ?
8. **Prestations hors des 4 services.** Le tissu tendu, les cadres acoustiques, les cloisons mobiles en aluminium et les plafonds métalliques sont-ils encore proposés ? Ils sont mis en avant sur LinkedIn, local.ch et l'ancien site, mais absents du positionnement v2.

### P2 : importantes

9. **Zone.** Avez-vous des chantiers récents à Neuchâtel, Fribourg, en Valais, dans le Jura ou le Jura bernois ? Lesquels, pour prouver la couverture romande ?
10. **GGE.** Depuis quand êtes-vous membre ? Peut-on écrire « Membre du GGE » sur le site ? Avez-vous d'autres affiliations ou formations (convention collective du second œuvre, fabricants comme Rigips, Knauf, Barrisol, produits anti-feu certifiés AEAI, CFC, maîtrise) ?
11. **Peinture.** Avez-vous des exemples et des photos ? Aujourd'hui, aucune n'est publique.
12. **Fonctionnement.** Les horaires lu-ve 7 h-18 h sont-ils exacts ? Quels délais de visite et de devis ? Quelle taille de chantier minimale ou maximale ? Travaillez-vous en sous-traitance d'entreprises générales ?
13. **Téléphone.** Quel numéro mettre en avant ? Le fixe 022 771 20 15 est-il toujours actif ? Le fax est-il à supprimer ? Faut-il garder la mention « pas de publicité » sur le mobile ?
14. **Garanties.** Assurance RC entreprise, garanties et normes appliquées (SIA 181, AEAI) : que peut-on afficher, preuves à l'appui ?
15. **Témoignages.** Quels clients satisfaits (régies, architectes, communes, particuliers) accepteraient un avis Google ou un témoignage écrit et signé ?
16. **Originaux des photos.** Pouvez-vous fournir les originaux de la galerie avant/après (en ligne en 800 px seulement) et les photos de chantiers non publiées ?

### P3 : complémentaires

17. **Annuaires à revendiquer ou corriger** (accès client nécessaire) : Yelp (non revendiquée), firmen.ch, MapsArch, Infobel (doublon), Cybo, Kompass (catégorie), search.ch / local.ch (« Sonorisation », logo, texte à aligner sur les 4 services), LinkedIn (description).
18. **Marques visibles sur les photos** (CORUM, OMC, vitrophanie « Sugar… ») : accord écrit des clients finaux ?
19. **Personnes visibles** (poseur en t-shirt Andy Construct sur IMG_5922, autres ouvriers) : accord des intéressés ?
20. **Anciens textes** : avez-vous des plaquettes, offres types ou textes d'avant 2017 (des captures d'archive existent dès 2012, mais nous n'avons pas pu les lire) ?
21. **Projet de transformation en Sàrl** : est-ce envisagé ? Sinon, abandon définitif de la mention « Sàrl ».

---

## Annexe A : URL de l'ancien site (toutes lues le 31.10.2026, HTTP 200)

- https://www.andyconstruct.ch/ (Accueil)
- https://www.andyconstruct.ch/presentation
- https://www.andyconstruct.ch/contact
- https://www.andyconstruct.ch/produits/plafonds/plafonds-en-tissu-tendu-a-froid (20 photos)
- https://www.andyconstruct.ch/produits/plafonds/plafonds-phoniques-et-acoustiques (8)
- https://www.andyconstruct.ch/produits/plafonds/plafonds-en-placoplatre (20)
- https://www.andyconstruct.ch/produits/plafonds/plafonds-en-fibre-de-bois (4)
- https://www.andyconstruct.ch/produits/plafonds/plafonds-en-fibre-minerale (10)
- https://www.andyconstruct.ch/produits/plafonds/plafonds-en-bac-metallique (7)
- https://www.andyconstruct.ch/produits/cloisons/cloisons-legeres-en-placoplatre (10)
- https://www.andyconstruct.ch/produits/cloisons/cloisons-mobiles-en-aluminium (8)
- https://www.andyconstruct.ch/produits/cloisons/isolation-thermique-ou-phonique (7)
- https://www.andyconstruct.ch/produits/cadres-acoustiques (11)
- https://www.andyconstruct.ch/realisations/photos-travaux-2014-2016 (95, dossier `/images/Divers/`)
- https://www.andyconstruct.ch/realisations/photos-travaux-avant-apres (14, dossier `/images/avant_apres/`)
- https://www.andyconstruct.ch/realisations/references
- https://www.andyconstruct.ch/sitemap.xml

Les pages produits et avant/après ne contiennent que le titre (« Plafonds en tissu tendu à froid », etc.) et une galerie. Aucune légende, aucune description, aucun document téléchargeable.

## Annexe B : textes intégraux de l'ancien site

- **Accueil** : « Plafonds — Spécialisé dans différents type de plafonds à choix. » · « Cloisons — Spécialisé dans différents type de cloisons. » · « Cadres acoustiques — Spécialisé dans différents type de cadres acoustiques. »
- **Présentation** : voir §3.1 (texte complet).
- **Contact** : « Andy Construct Chanton & Cie / Avenue de Bel-Air 57 / 1225 Chêne-Bourg / Genève - Suisse / T+F: +41 22 771 20 15 / Mob.: +41 78 631 14 34 / E: andy.construct(a)bluewin.ch »
- **Références** : voir §2.4 (18 noms, dans l'ordre du site).
- **Pied de page** (toutes les pages) : « 2010-2022 © Andy Construct Sàrl - +41 (0)78 631 14 34 - E-mail: andy.construct(a)bluewin.ch - Webdesign: iMedia Solutions »
