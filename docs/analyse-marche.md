# Andy Construct – Analyse marché, SEO local et GEO

**Projet :** refonte du site www.andyconstruct.ch
**Date :** 25 septembre 2026
**Rédaction :** analyste marché & SEO/GEO, pour le chef de projet
**Statut :** version 1, à valider avec le client (voir « Points bloquants »)

> **Méthode.** Les constats sur le site actuel ont été vérifiés le 25.09.2026 (requêtes HTTP directes, lecture du code source des pages, `sitemap.xml`, `robots.txt`). Les données d'identité proviennent du registre du commerce (Zefix) et des annuaires publics. Les concurrents ont été repérés par des recherches web et dans les annuaires, puis leurs sites ont été ouverts un par un. Limite : notre outil de recherche n'interroge pas google.ch depuis Genève. **Les positions réelles dans Google n'ont donc pas été mesurées.** Il faudra les relever depuis Genève, puis dans la Search Console. Tous les chiffres de marché renvoient à une source. Ce qui n'a pas pu être sourcé est marqué *« estimation à valider »*.

---

## 0. Points bloquants à régler avant la mise en ligne

Ce constat passe avant tous les autres : **l'identité publique de l'entreprise n'est pas cohérente**, alors que le référencement local et la visibilité dans les IA reposent d'abord sur des informations identiques partout.

| Élément | Ce que dit le brief / l'ancien site | Ce que disent les sources officielles et annuaires | Source |
|---|---|---|---|
| Raison sociale | « Andy Construct Sàrl » (pied de page de l'ancien site) | **« Andy Construct, Chanton & Cie »**, **société en nom collectif** (pas une Sàrl). Aucune Sàrl « Andy Construct » n'est inscrite au registre du commerce. | [Zefix / FOSC](https://www.zefix.ch), [Moneyhouse](https://www.moneyhouse.ch/en/company/andy-construct-chanton-cie-3813590051) |
| Siège / adresse | Avenue de Bel-Air 57, 1225 Chêne-Bourg | FOSC du 02.05.2023 : **nouveau siège à Carouge (GE), Route des Acacias 48, 1227 Carouge GE**. Chêne-Bourg n'est plus qu'une « autre adresse ». | Zefix (publication FOSC 02.05.2023) |
| Adresse affichée par les annuaires | – | local.ch, search.ch et l'annuaire GGE affichent tous **Carouge** | [local.ch](https://www.local.ch/fr/d/carouge-ge/1227/revetement-des-plafonds-et-plafonds-suspendus/andy-construct-chanton-cie-OGrZ5DP4atJqYki9WoTjPg), [search.ch](https://search.ch/tel/chene-bourg/avenue-de-bel-air-57/andy-construct-chanton-cie), [GGE](https://gge.ch/entreprises-2/wpbdp_category/plafonds-suspendus-faux-plaf/) |
| Ancienneté | « actif depuis 2010 » (© 2010-2022) | Inscription au registre du commerce **depuis le 27.06.2007** | Moneyhouse / Zefix |
| IDE (UID) | – | CHE-113.706.162 | Zefix |

**Décisions à obtenir du client** (un seul interlocuteur suffit, 15 minutes au téléphone) :
1. **Quelle adresse publique ?** C'est l'adresse où l'on reçoit le courrier et, le cas échéant, les clients. Elle doit être **la même** sur le site, la fiche Google, local.ch, search.ch, Facebook et les autres annuaires. Si les clients ne sont pas reçus sur place, on peut déclarer la fiche Google comme « zone desservie » et masquer l'adresse.
2. **Quelle raison sociale ?** Les mentions légales doivent reprendre **exactement** le nom inscrit au registre ([art. 954a CO](https://www.droit-bilingue.ch/rs/lex/1911/00/19110009-a954a-fr-en.html)). Le nom commercial « Andy Construct » reste utilisable partout ailleurs. Il faut abandonner « Sàrl », sauf si une Sàrl existe réellement.
3. **Quelle année de fondation afficher ?** 2007 (registre du commerce) ou 2010 ? Les IA lisent Moneyhouse et Zefix : un « depuis 2010 » sur le site créera une contradiction.
4. **Adresse e-mail :** l'actuelle est en `@bluewin.ch`. On recommande une adresse sur le domaine (p. ex. `contact@andyconstruct.ch`), plus crédible auprès des régies et des architectes.
5. **Droit de citer les références** (noms, et encore plus logos) : il faut l'accord du client pour les marques privées (Piaget, De Grisogono, UBS, etc.). Plusieurs noms ont aussi changé depuis : Bank Sarasin est devenue [J. Safra Sarasin](https://en.wikipedia.org/wiki/J._Safra_Sarasin) en 2013, et Celgene appartient à [Bristol Myers Squibb](https://www.sec.gov/Archives/edgar/data/14272/000114036119021048/ex99_1.htm) depuis 2019. Il faut donc **dater chaque référence** (« réalisé en 20XX »).

---

## 1. Résumé exécutif

- **On part presque de zéro, et c'est une chance.** Les pages prestations du site actuel ne contiennent **que 20 à 25 mots de texte** (le titre et le pied de page), aucune image n'a de texte alternatif, la page d'accueil a trois H1 et toutes les pages ont la même meta description. Le suivi d'audience (Universal Analytics) **ne mesure plus rien depuis le 1er juillet 2023** ([Google](https://support.google.com/analytics/answer/11583528?hl=fr)). Un site neuf, bien rédigé et bien balisé, peut rapidement dépasser la plupart des concurrents genevois.
- **Priorité n°1 : une identité unique (nom, adresse, téléphone).** Le registre du commerce, les annuaires et l'ancien site se contredisent (Sàrl ou société en nom collectif, Chêne-Bourg ou Carouge). Tant que ce n'est pas réglé, Google et les IA hésiteront à recommander l'entreprise. C'est gratuit et rapide à corriger.
- **Les références sont l'actif le plus fort, et le moins exploité.** Ville de Genève, Conservatoire, HEAD, OMC, Piaget, UBS, salles communales : très peu de concurrents peuvent aligner une telle liste. Aujourd'hui, ce n'est qu'une liste sans photo ni description. En faire des **fiches projets** (lieu, problème, solution, année) apporte la preuve que cherchent régies et architectes, et fournit aux IA un contenu qu'elles peuvent citer.
- **La fiche Google et les avis décident de la visibilité locale.** Andy Construct n'a **aucun avis** sur local.ch ni sur search.ch. Google l'écrit lui-même : le nombre d'avis et de liens entrants pèse sur le classement local ([Google](https://support.google.com/business/answer/7091?hl=fr)). Il faut une fiche complète et une campagne d'avis auprès des clients satisfaits (régies, architectes, particuliers).
- **Plafonds tendus, acoustique et anti-feu : une niche qui différencie.** Les spécialistes des plafonds tendus et de l'acoustique qui visent Genève sont surtout **vaudois** (Atyx à Lausanne, Solutions Acoustiques à Yverdon). Ce dernier publie même des pages dédiées à Carouge, Lancy, Meyrin et **Chêne-Bourg**. Le contexte porte cette niche : norme acoustique SIA 181:2020 plus exigeante, révision des prescriptions incendie AEAI reportée à l'automne 2027 après l'incendie de Crans-Montana ([AIET, 23.01.2026](https://www.bpuk.ch/fileadmin/Dokumente/bpuk/public/fr/dokumentation/medienmitteilungen/2026/Communique_de_presse_AIET_Prescription_de_protection_incendie.pdf)).
- **Le B2B et les marchés publics rapportent le plus par contrat.** À Genève, les travaux de second œuvre se passent **de gré à gré sous CHF 150'000** et **sur invitation entre CHF 150'000 et 250'000** ([ge.ch](https://www.ge.ch/role-autorites-adjudicatrices-marches-publics/principes-types-procedures-cadre-legal)). Une commune qui connaît déjà l'entreprise peut donc l'inviter directement. Il faut un dossier de références téléchargeable et une veille simap.ch / FAO.
- **GEO : un avantage à prendre maintenant, mais la fenêtre se referme.** Les aperçus IA de Google fonctionnent en Suisse et en français depuis mars 2025 ([X. Studer](https://www.xavierstuder.com/2025/03/google-ai-overviews-en-suisse-ou-la-fin-du-web/)) et 73 % des internautes suisses ont déjà utilisé une IA générative ([UZH/RTS](https://www.rts.ch/info/societe/2025/article/l-ia-creuse-le-fosse-numerique-etude-alarmante-sur-l-exclusion-en-suisse-29051234.html)). Trois concurrents genevois ont déjà un fichier `llms.txt`. Pour une cible de 45-70 ans, Google et le téléphone restent cependant l'essentiel : le GEO **complète** le référencement classique, il ne le remplace pas.

---

## 2. Contexte marché : Suisse romande et Genève

### 2.1 La rénovation résiste mieux que le neuf

- **2024 :** les investissements dans la construction neuve reculent de **2,7 %**, ceux dans les **transformations progressent de 2,3 %** (OFS, résultats provisoires publiés le 17.07.2025, [source](https://www.geoinformation.ch/fr/newnsb/nTNbFR3pl03pCUtty8wQL)).
- **2025 :** les investissements dans la construction augmentent de **3,5 %** (nominal) et ceux dans les transformations de **3,5 %**. Les pouvoirs publics investissent **8,4 %** de plus dans le bâtiment, et les chantiers en cours augmentent de 6,0 % par rapport à 2024 (OFS, chiffres repris le 21.07.2026, [LFM](https://www.lfm.ch/actualite/suisse/investissements-beton-dans-la-construction-suisse-en-2025/)).
- **Ce que cela signifie pour Andy Construct :** les deux moteurs sont la **rénovation** et la **commande publique** (écoles, salles communales, bâtiments administratifs). Ce sont précisément les segments où Andy Construct a des références (salles communales de Collonge-Bellerive et de Plan-les-Ouates, Ville de Genève, Conservatoire).

### 2.2 Rénovation énergétique : des obligations légales à Genève

- **Programme Bâtiments (national) :** **528 millions de francs** versés en 2024, dont **131 millions pour l'isolation thermique** ([DETEC, 26.08.2025](https://www.uvek.admin.ch/fr/newnsb/IKoj6VY8s85qnTeXJrLxc)).
- **Genève :** enveloppe exceptionnelle de **500 millions de francs** votée par le Grand Conseil en mars 2024, dont **80 millions pour 2026** (10 millions de plus qu'en 2025). Plus de 1'400 dossiers ont été traités par l'office cantonal de l'énergie en 2025. **La demande doit être déposée avant le début des travaux** ([ge.ch, 02.02.2026](https://www.ge.ch/blog/geneve-energie/subventions-energetiques-2026-80-millions-francs-accelerer-renovation-du-parc-bati-genevois-2-02-2026)).
- **IDC (indice de dépense de chaleur) :** un bâtiment au-dessus de 125 kWh/m²·an doit faire l'objet d'un audit. Le seuil qui **oblige à rénover** passe de 222 kWh/m²·an (jusqu'au 31.12.2026) à **180 dès le 1.1.2027**, puis à **153 dès 2031** ([ge.ch](https://www.ge.ch/connaitre-consommation-energie-batiment-idc/que-faire-resultat-idc-votre-immeuble)).
- **Ce que cela signifie :** les régies et les propriétaires d'immeubles vont lancer des rénovations dans les prochaines années. Andy Construct n'installe ni chauffage ni façades, mais l'**isolation intérieure** (plafonds de caves et de garages, doublages, faux-plafonds isolés) entre souvent dans ces lots. Si une subvention s'applique, elle se vérifie au cas par cas. Le site doit en parler prudemment (FAQ « subventions ») et renvoyer vers GEnergie.

### 2.3 Acoustique : la demande augmente

- **SIA 181:2020** (protection contre le bruit dans le bâtiment) : elle s'applique aux projets dont la demande d'autorisation est déposée depuis le 1.11.2020. L'écart entre exigences minimales et exigences accrues passe de 3 à **4 dB** ([Prona](https://www.prona-romandie.ch/nouvelle-sia-181-protection-contre-le-bruit-dans-le-batiment-les-modifications-les-plus-importantes/)). Les architectes doivent donc prévoir des séparations plus performantes.
- **Bruit :** **740'000 personnes** en Suisse sont exposées chez elles à un bruit routier nuisible ou incommodant, **plus de 90 % d'entre elles en ville ou en agglomération** (OFEV, données publiées le 18.11.2025, [source](https://www.bafu.admin.ch/fr/pollution-sonore)).
- **Bureaux :** le marché genevois des bureaux compte beaucoup de surfaces vacantes et de relocations ([Bilan](https://www.bilan.ch/story/geneve-les-bureaux-des-nouveaux-quartiers-trouvent-preneurs-966672858458)). Chaque changement de locataire peut entraîner un réaménagement (cloisons mobiles, correction acoustique des salles de réunion). *L'ampleur exacte de ce marché pour Andy Construct reste une estimation à valider.*
- **Ce que cela signifie :** « plafond acoustique », « isolation phonique », « bruit des voisins du dessus » et « chape flottante » sont des sujets à la fois **informatifs** (bons pour la FAQ et le GEO) et **commerciaux**.

### 2.4 Protection incendie : un sujet sensible en 2026-2027

- Les prescriptions AEAI en vigueur datent de 2015. Leur révision totale a reçu près de **11'000 contributions** en consultation. Après l'incendie de Crans-Montana, l'entrée en vigueur est **reportée, vraisemblablement à l'automne 2027** ([AIET, 23.01.2026](https://www.bpuk.ch/fileadmin/Dokumente/bpuk/public/fr/dokumentation/medienmitteilungen/2026/Communique_de_presse_AIET_Prescription_de_protection_incendie.pdf)).
- **Ce que cela signifie :** les maîtres d'ouvrage, les communes et les exploitants de lieux publics seront plus attentifs aux faux-plafonds et aux cloisons coupe-feu. Le site doit en parler **sobrement et sans promesse** : la classe de résistance est fixée par le concept incendie du projet. Il faut aussi vérifier avec le client quels systèmes certifiés il pose.

### 2.5 Marchés publics

- **simap.ch** est la plateforme commune à la Confédération, aux cantons et aux communes. La nouvelle version est en service depuis le **1.7.2024** ([Canton de Vaud](https://info.vd.ch/canton-communes/articles-dgaic/2024/mars/numero-71/simapch-la-nouvelle-plateforme-de-publication-des-marches-publics-en-exploitation-des-le-1er-juillet-2024)). Ordre de grandeur publié en 2015 : **plus de 9'000 appels d'offres par an, pour près de 16 milliards de francs** ([La Vie économique](https://dievolkswirtschaft.ch/fr/2015/06/2015-07-tanner-franz/)). *Chiffre ancien, actualisation à valider.*
- **Seuils genevois pour le second œuvre** (quand l'ouvrage total reste sous CHF 8,7 mio) : **gré à gré < CHF 150'000**, **procédure sur invitation de 150'000 à 250'000**, procédure ouverte ou sélective au-delà ([ge.ch](https://www.ge.ch/role-autorites-adjudicatrices-marches-publics/principes-types-procedures-cadre-legal)).
- Les appels d'offres utilisent les codes **CFC 271 (plâtrerie), 283 (faux-plafonds), 285 (traitement des surfaces intérieures / peinture)**. Exemple réel : [FAO Vaud, lot « CFC 271/283/285 Plâtrerie – Faux plafond – Peinture »](https://www.faovd.ch/marches-publics/detail/2216/1179973/fondation-mont-calme-lausanne-cfc-271-283-285-platrerie-faux-plafond-peinture-pour-la-construction-d-un-ems-de-122-lits/). Voir aussi le [guide des CFC](https://batiguide.ch/guide-des-cfc/).
- La Ville de Genève publie ses futurs projets (écoles des Charmilles et Charles-Giron, Musée d'art et d'histoire, Bibliothèque de Genève) : [geneve.ch](https://www.geneve.ch/themes/amenagement-construction-energie/construction-entretien-renovation-batiments/futurs-projets). Elle figure déjà parmi les références d'Andy Construct.
- **Ce que cela signifie :** sous CHF 150'000, un marché peut être attribué **directement**. Être connu des services techniques communaux et des architectes mandataires, et leur fournir un dossier de références propre, rapporte autant qu'une annonce.

### 2.6 Comment la clientèle cherche

- **Moteurs de recherche en Suisse (août 2026) :** Google **81,3 %**, Bing **10,8 %** ([Statcounter](https://gs.statcounter.com/search-engine-market-share/all/switzerland)). Bing compte davantage qu'il n'y paraît, car ChatGPT Search s'appuie principalement sur son index ([BrightLocal](https://www.brightlocal.com/research/uncovering-chatgpt-search-sources/)).
- **Seniors :** **89 % des plus de 65 ans** utilisent internet en 2025, contre 38 % en 2010 ([Pro Senectute, Digital Seniors 2025](https://www.prosenectute.ch/fr/espace-pro/fond/etudes/digital-seniors-2025.html)). La cible de 45 à 70 ans cherche donc bien en ligne, **puis téléphone**.
- **IA générative :** 73 % de la population suisse l'a utilisée en 2025 (37 % en 2023), mais seulement **20 % des 70 ans et plus se disent à l'aise** avec ces outils (Université de Zurich, World Internet Project 2025, [RTS](https://www.rts.ch/info/societe/2025/article/l-ia-creuse-le-fosse-numerique-etude-alarmante-sur-l-exclusion-en-suisse-29051234.html)). Pour Andy Construct, les IA pèsent surtout auprès des **architectes, des collaborateurs de régies et des acheteurs** plus jeunes.
- **Aperçus IA de Google selon le type de requête** (étude américaine) : ils apparaissent dans **92 %** des questions pratiques (« combien coûte… », « comment… ») mais dans seulement **15 %** des recherches « près de chez moi », où la carte Google (le « pack local ») s'affiche dans **93 %** des cas ([Whitespark](https://whitespark.ca/blog/case-study-the-prevalence-of-ai-overviews-in-local-search/)). **En clair :** la fiche Google sert à décrocher le chantier, la FAQ et les guides à être cité par l'IA.
- **Genève, canton de locataires :** 36 % des ménages suisses sont propriétaires ([OFS via RTS](https://www.rts.ch/info/suisse/2024/article/les-menages-sont-proprietaires-de-leur-logement-dans-36-des-cas-28441356.html)). Genève a le taux le plus bas du pays, *environ un ménage sur cinq selon la presse (estimation à valider sur la source OFS)*. **Les régies et les gérants d'immeubles sont donc les prescripteurs clés** pour le logement.

---

## 3. Paysage concurrentiel

Ces concurrents ont été repérés sur les requêtes « faux plafond Genève », « plafond tendu Genève », « plafond acoustique Genève », « plâtrerie peinture Genève » et « cloisons amovibles Genève ». Leurs sites ont été ouverts le 25.09.2026. Les colonnes « données structurées » et « llms.txt » ont été vérifiées dans le code source.

| # | Entreprise (site) | Base | Positionnement | Points forts du site | Points faibles du site | Données structurées / llms.txt |
|---|---|---|---|---|---|---|
| 1 | **DSD SA** ([dsd-sa.ch](https://www.dsd-sa.ch/)) | Chêne-Bougeries (**voisin direct**) | Gypserie-plâtrerie-peinture depuis 1995, pour architectes, régies et particuliers | **7 études de cas détaillées** (2020-2025 : maisons horlogères, organisations internationales, conservatoire, hôtels), title et meta bien optimisés, téléphone cliquable, mention des normes SIA | Pas de FAQ, pas d'avis visibles, AEAI jamais mentionnée, page d'accueil lourde (~320 Ko de HTML) | LocalBusiness détaillé (horaires, zone desservie, services). Pas de llms.txt |
| 2 | **EM Plafond Sàrl** ([em-plafond.ch](https://www.em-plafond.ch/)) | Genève | Faux-plafonds, cloisons vitrées, acoustique ; clientèle professionnelle et architectes | Chiffres clés affichés (années, nombre de projets, satisfaction : **auto-déclarés**), boutons « devis » répétés, galerie de réalisations | Pas d'adresse précise, pas de FAQ, aucune norme citée, textes courts | LocalBusiness. **llms.txt présent** (liste de pages) |
| 3 | **Class Orga** ([classorga.ch](https://classorga.ch/faux-plafonds/)) | Grand-Lancy | Entreprise générale « clé en main », 15 corps de métier | Page faux-plafonds riche (7 types : acoustique, modulaire, coupe-feu, tendu, métal, bois), **cite l'AEAI et la SIA** | Généraliste, donc moins crédible comme spécialiste ; preuves renvoyées vers Instagram ; pas de FAQ | Non vérifié. Pas de llms.txt |
| 4 | **Edelweiss Rénovation SA** ([edelweiss-renovation.ch](https://edelweiss-renovation.ch/faux-plafond-geneve/)) | Genève (1204) | Finitions intérieures, faux-plafonds avec éclairage LED, particuliers et régies | **Le plus avancé en SEO/GEO** : une page par service et par ville (`/faux-plafond-geneve/`, `/platrier-geneve/`), ~1'500 mots, promesse « devis 48 h », maillage interne | Aucune référence nommée, aucune norme, FAQ générique (3 questions) | LocalBusiness + OfferCatalog + AggregateRating. **llms.txt complet** (raison sociale, adresse, services) |
| 5 | **Solutions Acoustiques Sàrl** ([solutions-acoustiques.ch](https://solutions-acoustiques.ch/installation-panneaux-acoustiques-suisse/geneve/)) | Yverdon-les-Bains (VD) | Acoustique et plafonds tendus, **installateur agréé Barrisol** ([Barrisol](https://barrisol.com/fr/installateur-plafond-tendu/geneve)) | **Pages par commune genevoise** (Carouge, Lancy, Vernier, Meyrin, **Chêne-Bourg**, Onex), blog technique (p. ex. résistance au feu dans les lieux publics), devis sous 48 h | Pas d'implantation genevoise, pas d'avis ni de norme sur la page testée | Organization, BreadcrumbList. **llms.txt présent** (articles de blog) |
| 6 | **Atyx** ([atyx.ch](https://atyx.ch/)) | Lausanne | Plafonds tendus lumineux et acoustiques, haut de gamme | **Références prestigieuses** (CHUV, CIO, Longines, WEF, CICG), **certifications affichées** (classement feu B-s1,d0, ISO 354, OEKO-TEX), garantie 20 ans sur les toiles, « plus de 1'000 installations » | Pas de FAQ, pas d'ancrage genevois, page très lourde (~780 Ko de HTML) | LocalBusiness, Organization. Pas de llms.txt |
| 7 | **Déco Plafond Tendu** ([decoplafondtendu.ch](https://www.decoplafondtendu.ch/plafond-tendu)) | Genève et Vaud | Plafonds tendus pour particuliers, éclairage LED, home cinéma | **Prix affiché** (« entre 80.- et 120.- le m² rendu posé »), photos avant/après, trois numéros de téléphone | **Pas de meta description**, aucune donnée structurée, ni référence, ni norme, ni ancienneté | Aucune |
| 8 | **P3 Construction** ([p3construction.ch](https://www.p3construction.ch/isolation/)) | Lancy | Faux-plafonds et staff, région Nyon-Morges-Genève | Title clair avec la zone, formulaire de devis | Contenu mince (~500 mots), ni référence, ni norme, ni avis | Organization seulement |

**Autres acteurs à surveiller :**
- Spécialistes des cloisons amovibles et vitrées pour bureaux : [Bureau Concept Suisse](https://www.bureau-concept-suisse.ch/cloisons-a-geneve/), [Lamelle-Glass](https://www.lamelle-glass.ch/cloisons-vitree/), [Cloisor](https://www.cloisor.net/installateur+de+cloison+amovible+geneve+en+suisse-z184).
- Plâtriers-peintres généralistes : [Manzi](https://manzi-sarl.ch/), [Dino Peinture](https://www.dinopeinture.ch/), [SwissPaints](https://www.swisspaints.ch/entreprise-de-peinture-a-geneve-platrerie).
- L'annuaire [GGE](https://gge.ch/entreprises-2/wpbdp_category/plafonds-suspendus-faux-plaf/) liste à lui seul des dizaines d'entreprises dans « Plafonds suspendus / faux plafonds » : le marché est **très fragmenté**.

**Ce qu'on retient :**
1. **Presque personne n'a de vraie FAQ.** C'est la place à prendre pour le GEO.
2. **Personne ne combine** de grandes références nommées, des normes expliquées (SIA 181, AEAI) et un ancrage local genevois. DSD SA s'en approche le plus : c'est le **concurrent de référence**, installé dans la commune voisine et sur les mêmes cibles.
3. **Les pages par commune existent déjà** chez deux concurrents, dont un vaudois qui cible Chêne-Bourg. Il faut répondre avec du contenu réel (chantiers réalisés dans ces communes), pas avec des pages clonées.
4. **Le GEO a commencé** : 3 concurrents sur 8 publient un `llms.txt`. L'avantage du premier arrivant reste réel, mais il ne durera pas.
5. **Très peu d'avis clients sont affichés dans la branche.** Une entreprise avec 20 à 30 avis Google détaillés se démarquerait nettement *(estimation à valider en relevant les fiches Google des concurrents depuis Genève)*.

**Où se place Andy Construct :** un **spécialiste plafonds et cloisons** (et non un généraliste), **genevois**, avec des **références institutionnelles et de prestige**. C'est le positionnement à affirmer, sobrement : « l'entreprise à qui la Ville de Genève, le Conservatoire et la HEAD confient leurs plafonds ». Le client doit valider cette formulation et l'usage des noms.

---

## 4. Diagnostic du site actuel (andyconstruct.ch)

Vérifications faites le 25.09.2026.

| Domaine | Constat vérifié | Impact | Correction dans le nouveau site |
|---|---|---|---|
| HTTPS | OK : `http://` redirige en 301 vers `https://` | – | Garder le HTTPS et ajouter l'en-tête HSTS |
| Doublons d'URL | `andyconstruct.ch` **et** `www.andyconstruct.ch` répondent tous deux en 200. `/presentation` et `/index.php/presentation` aussi. Aucune balise canonical | Contenu dupliqué, autorité diluée | Un seul hôte (www) avec une 301 depuis l'autre ; canonical sur chaque page |
| sitemap.xml | Présent, mais il liste des URL **sans www et avec `index.php`**, différentes de celles du menu | Signaux contradictoires pour Google | Nouveau sitemap avec les 5 URL finales |
| robots.txt | **404** (absent) | Mineur | À créer, avec un lien vers le sitemap |
| Contenu | Pages prestations (plafond tendu, acoustique, cloisons mobiles, cadres acoustiques, avant/après) : **20 à 25 mots** de texte visible. Page Présentation : ~120 mots | Rien à indexer ni à citer par une IA | 150 à 300 mots par prestation, rédigés pour la clientèle |
| Titres | « Andy Construct - Accueil », « Andy Construct - Contact »… : ni métier ni lieu | Faible pertinence | Title avec métier + Genève (voir brief SEO) |
| Meta description | **Identique sur toutes les pages** (« Pose de Plafonds et cloisons Genève - Vaud - Andy Construct Sàrl Suisse ») | Faible taux de clic, et « Sàrl » erroné | Une description unique par page |
| Hiérarchie des titres | Accueil : **3 H1** (« Plafonds », « Cloisons », « Cadres acoustiques ») | Sujet principal flou | Un seul H1 par page |
| Images | **0 texte alternatif** (21 images sur la page plafond tendu, aucune avec `alt`). Vignettes de l'accueil : 924 Ko + 264 Ko + 384 Ko, soit **~1,6 Mo pour 3 petites images** | Lenteur sur mobile, photos invisibles pour Google Images et les IA | Photos en AVIF/WebP redimensionnées, alt descriptifs |
| Poids du code | CSS de template de **462 Ko**, jQuery, Bootstrap, CloudZoom, en-tête `Cache-Control: no-store` (rien n'est mis en cache) | Mauvaise vitesse probable (**score PageSpeed non mesuré, quota API dépassé : à mesurer**) | Site statique léger, cache long sur les fichiers statiques |
| Données structurées | Aucune fiche LocalBusiness. Seul un balisage `Article` vide hérité du template Joomla | L'entreprise n'est pas décrite pour les machines | JSON-LD HomeAndConstructionBusiness + FAQPage (voir brief) |
| Mesure d'audience | **Universal Analytics** (UA-17202698-1) : ne collecte plus rien depuis le 1.7.2023 ([Google](https://support.google.com/analytics/answer/11583528?hl=fr)) | Aucune donnée depuis plus de 3 ans | Mesure respectueuse de la vie privée + Search Console + Bing Webmaster Tools |
| Téléphone | **Aucun lien `tel:`**. Le pied de page n'affiche que le mobile, le fixe n'apparaît que sur la page Contact | Perte d'appels sur mobile, alors que la cible appelle | Numéro cliquable dans l'en-tête et le pied de page |
| E-mail | Affiché « andy.construct(a)bluewin.ch » (masqué à la main, mais le lien `mailto:` contient l'adresse réelle) | Confus pour un public âgé, et n'arrête pas les robots | Formulaire court + adresse lisible sur le domaine |
| Fraîcheur | « 2010-2022 © », galerie « Photos travaux 2014-2016 » | Donne l'impression d'une entreprise inactive | Réalisations datées, © dynamique |
| Réseaux sociaux | L'icône Facebook ouvre un **partage** (`sharer.php`) au lieu de la page de l'entreprise | Lien cassé | Lien direct vers la page Facebook |
| Navigation | Menu « Produits » avec des rubriques non cliquables | Ergonomie médiocre, mauvaise exploration | 5 pages claires |
| Légal | Pas de mentions légales ni de politique de confidentialité ; raison sociale erronée. La nLPD est en vigueur depuis le 1.9.2023 ([PME admin.ch](https://www.kmu.admin.ch/fr/nouvelle-loi-sur-la-protection-des-donnees-nlpd)) | Risque juridique, manque de confiance | Page mentions légales et confidentialité |

**Présence en dehors du site (vérifiée) :**
- **local.ch** et **search.ch** : fiches actives à l'adresse de **Carouge**, horaires lu-ve 7 h-18 h, **0 avis**.
- **GGE** (annuaire professionnel genevois) : Carouge.
- **Moneyhouse** et **Zefix** : Carouge, société en nom collectif, depuis 2007.
- **Kompass** : classé dans une **catégorie erronée** (« charpenterie »).
- architecteromand.ch et edirex.ch : fiches présentes, à contrôler.
- **Fiche Google :** *impossible à vérifier sans accès propriétaire. À contrôler en priorité* (existe-t-elle, qui la gère, quelle adresse, combien d'avis).

---

## 5. Matrice des leviers

**Notation.** Impact de 1 à 5 (5 = très fort). Effort de 1 à 5 (1 = léger). **Score = Impact × (6 − Effort)**, sur 25 au maximum. Le potentiel indique la marge de progression à 12 mois. Les objectifs des KPI sont des **propositions** à ajuster une fois les premières mesures disponibles.

| Rang | Levier | Impact | Effort | Score | Potentiel | Horizon |
|---|---|---|---|---|---|---|
| 1 | **Identité et NAP unifiés** (nom, adresse, téléphone) | 5 | 1 | **25** | Élevé | 0-30 j |
| 2 | **Fiche Google + avis** | 5 | 2 | **20** | Très élevé | 30 j, puis en continu |
| 3 | **Conversion** (téléphone cliquable, formulaire court, horaires) | 4 | 1 | **20** | Élevé | À la mise en ligne |
| 4 | **Contenu des prestations + base technique SEO + redirections 301** | 5 | 3 | **15** | Élevé | À la mise en ligne |
| 5 | **Références en fiches projets (preuve)** | 5 | 3 | **15** | Très élevé | 30-90 j |
| 6 | **GEO : FAQ citable, données structurées, llms.txt, Bing** | 3 | 1 | **15** | Élevé (en hausse) | À la mise en ligne |
| 7 | **Mesure** (Search Console, Bing Webmaster Tools, statistiques) | 3 | 1 | **15** | Prérequis | À la mise en ligne |
| 8 | **Annuaires et mentions tierces** | 3 | 2 | **12** | Moyen à élevé | 30-90 j |
| 9 | **B2B : architectes, régies, marchés publics** | 4 | 3 | **12** | Très élevé (valeur par contrat) | 90-180 j |
| 10 | **Niche plafonds tendus, acoustique, anti-feu** | 4 | 3 | **12** | Élevé | 90-180 j |
| 11 | **Pages services × communes** (phase 2) | 3 | 4 | **6** | Moyen | 180 j + |
| 12 | **Plateformes payantes** (Renovero) | 2 | 2 | **8** | Faible à moyen (particuliers) | Test optionnel |

### Détail des leviers

**1. Identité et NAP unifiés**
- *Pourquoi.* Google et les IA recoupent les sources (registre du commerce, annuaires, site). En cas de contradiction, ils font moins confiance à l'entreprise. Aujourd'hui, 3 points se contredisent (voir section 0).
- *Action.* Faire valider au client **une** version (raison sociale, nom commercial, adresse, téléphone fixe principal, mobile, e-mail, horaires, année). Puis la reporter **à l'identique** sur le site, la fiche Google, local.ch, search.ch (une correction sur localsearch se répercute sur les deux), Facebook, GGE, Kompass (corriger aussi la catégorie), architecteromand.ch, edirex.ch, Bing Places et Apple Business Connect. Si l'adresse change, la déclarer aussi au registre du commerce.
- *KPI.* 100 % des fiches listées identiques (tableau de contrôle).
- *Horizon.* 30 jours.

**2. Fiche Google + avis**
- *Pourquoi.* Pour une requête locale, la carte Google s'affiche dans la grande majorité des cas ([Whitespark](https://whitespark.ca/blog/case-study-the-prevalence-of-ai-overviews-in-local-search/), étude américaine). Google classe selon la pertinence, la distance et la notoriété, et précise que le nombre d'avis y contribue ([Google](https://support.google.com/business/answer/7091?hl=fr)). Selon l'enquête Whitespark 2026, avis et comportement des utilisateurs pèsent de plus en plus ([Whitespark](https://whitespark.ca/local-search-ranking-factors/)).
- *Action.* Revendiquer ou créer la fiche, la faire vérifier, puis :
  - choisir une catégorie principale liée aux plafonds ou à la plâtrerie et des catégories secondaires (cloisons, isolation, peinture) *(libellés exacts à choisir dans la liste proposée par Google)* ;
  - déclarer la zone desservie (Genève + ouest vaudois) ;
  - ajouter les horaires, un descriptif de 750 caractères et **30 photos de chantiers** légendées ;
  - saisir les services un par un ;
  - publier une actualité par mois (un chantier terminé).
  - **Campagne d'avis :** une liste de 30 clients récents ou fidèles (régies, architectes, particuliers), un e-mail ou SMS avec lien direct, une relance, et une réponse à **chaque** avis.
- *KPI.* Nombre d'avis et note moyenne (objectif proposé : **15 avis à 90 jours, 30 à 180 jours**). Appels et demandes d'itinéraire générés par la fiche (statistiques Google).
- *Horizon.* Fiche en 30 jours ; avis en continu.

**3. Conversion**
- *Pourquoi.* La cible (45-70 ans, régies, architectes) **appelle** plutôt qu'elle n'écrit. Aujourd'hui, aucun numéro n'est cliquable.
- *Action.*
  - Téléphone fixe et mobile cliquables (`tel:`) dans l'en-tête, le pied de page et la page contact, en gros caractères, avec les horaires juste à côté.
  - Formulaire **court** (nom, téléphone ou e-mail, commune, type de travaux, message, photo facultative).
  - Un message de délai de rappel réaliste, *à définir avec le client*.
  - Aucun pop-up.
  - Un bouton « Appeler » fixe sur mobile.
- *KPI.* Clics sur le téléphone, formulaires envoyés, taux de conversion par page.
- *Horizon.* Dès la mise en ligne.

**4. Contenu des prestations + base technique**
- *Pourquoi.* Ni Google ni une IA ne peuvent recommander une prestation qui n'est pas **décrite en texte**. Selon l'enquête Whitespark 2026, « une page dédiée pour chaque service » est le **2e facteur de visibilité dans les IA** ([Whitespark](https://whitespark.ca/local-search-ranking-factors/)).
- *Action.*
  - Sur la page prestations, une section par famille (plafonds tendus, acoustiques, placoplâtre, fibre, métal, cloisons, isolation, cadres acoustiques, chape flottante, anti-feu, caissons lumineux, trappes, puits de lumière). Pour chacune : à quoi ça sert, pour qui, les avantages, les contraintes, un exemple de chantier.
  - Côté technique : un hôte unique, des canonical, sitemap, robots.txt, balisage sémantique et images optimisées.
  - **Redirections 301** de toutes les anciennes URL vers les nouvelles (liste dans le brief SEO), pour conserver les liens des annuaires.
- *KPI.* Pages indexées (Search Console), impressions et clics sur les requêtes métier, Core Web Vitals au vert.
- *Horizon.* À la mise en ligne, puis enrichissement à 90 jours.

**5. Références en fiches projets**
- *Pourquoi.* C'est **la** preuve que cherchent une régie ou un architecte, et c'est ce qui distingue Andy Construct de 90 % des concurrents. Pour les IA, un texte factuel du type « faux-plafond acoustique posé à la salle communale de Plan-les-Ouates en 20XX » est **citable**. Une simple liste de logos ne l'est pas.
- *Action.* 6 à 10 fiches pour commencer (priorité aux références publiques : Ville de Genève, salles communales de Collonge-Bellerive et de Plan-les-Ouates, Conservatoire, Alhambra, HEAD). Pour chaque fiche :
  - lieu et commune ;
  - année ;
  - type de client ;
  - besoin ;
  - solution et matériaux ;
  - 2 à 4 photos avec alt ;
  - si possible, une phrase du client.
  - Pour les marques privées, afficher le nom seulement avec l'accord du client (sinon, « maison horlogère genevoise »).
- *KPI.* Nombre de fiches publiées, temps passé sur la page réalisations, demandes qui mentionnent une référence.
- *Horizon.* 4 fiches à la mise en ligne, 10 à 90 jours.

**6. GEO** (détaillé en section 6)
- *Pourquoi.* C'est un avantage de premier arrivant, pour un coût marginal si c'est prévu dès la construction du site.
- *Action.*
  - Une FAQ en texte visible.
  - Du JSON-LD cohérent avec le texte.
  - Un fichier `llms.txt`.
  - Une page « L'entreprise en bref » avec des faits datés.
  - L'inscription à Bing Webmaster Tools et Bing Places.
  - La cohérence NAP (levier 1).
  - Des mentions tierces (levier 8).
- *KPI.* Test mensuel de 10 questions dans ChatGPT, Perplexity, Google (aperçus IA / mode IA) et Copilot : l'entreprise est-elle citée, et correctement ?
- *Horizon.* Dès la mise en ligne, puis mesure mensuelle.

**7. Mesure**
- *Pourquoi.* Sans mesure, impossible de savoir ce qui fonctionne. Aujourd'hui, rien n'est mesuré.
- *Action.*
  - Google Search Console et Bing Webmaster Tools, avec envoi du sitemap.
  - Un outil de statistiques (GA4 avec bannière de consentement, ou une solution sans cookies hébergée en Europe, à choisir avec le client selon la nLPD).
  - Suivi des clics `tel:` et des envois de formulaire.
  - Relevé trimestriel des positions sur 15 requêtes, depuis Genève.
- *KPI.* Tableau de bord mensuel d'une page.
- *Horizon.* À la mise en ligne.

**8. Annuaires et mentions tierces**
- *Pourquoi.* Pour la visibilité dans les IA, **3 des 5 premiers facteurs sont des mentions externes** : présence dans des listes « meilleurs X » rédigées par des experts, présence sur les sites de référence du secteur, qualité des citations ([Whitespark](https://whitespark.ca/local-search-ranking-factors/)). ChatGPT cite d'abord les **sites d'entreprises (58 %)**, puis des mentions (27 %) et des annuaires (15 %) ([BrightLocal, nov. 2024](https://www.brightlocal.com/research/uncovering-chatgpt-search-sources/)).
- *Action.*
  - Corriger ou compléter : local.ch, search.ch, GGE, Kompass, architecteromand.ch, edirex.ch.
  - Créer : Bing Places, Apple Business Connect, [Houzz](https://www.houzz.fr/professionals/decorateurs-d-interieur/c/Gen%C3%A8ve--Canton-de-Gen%C3%A8ve--Suisse/p/15) (profil gratuit, utile auprès des architectes d'intérieur).
  - Associations professionnelles : vérifier l'affiliation à une association ou fédération professionnelle genevoise de la plâtrerie-peinture *(à valider avec le client)*.
  - Presse spécialisée : proposer un reportage de chantier à [Batimag](https://www.batimag.ch/) (acoustique d'une salle publique, par exemple).
  - Demander un lien « entreprises mandatées » aux architectes partenaires.
  - Ne pas s'inscrire sur Buildigo, **en liquidation** ([batmat](https://batmat.blog/buildigo-sa-liquidie-la-mobiliere-se-retire-du-marche/)).
- *KPI.* Nombre de fiches cohérentes, nombre de mentions et de liens de sites tiers.
- *Horizon.* 30 à 90 jours.

**9. B2B : architectes, régies, marchés publics**
- *Pourquoi.* Un seul mandat communal ou de régie vaut des dizaines de chantiers de particuliers. Sous CHF 150'000, l'attribution de gré à gré est possible à Genève ([ge.ch](https://www.ge.ch/role-autorites-adjudicatrices-marches-publics/principes-types-procedures-cadre-legal)).
- *Action.*
  - Sur la page réalisations, un bloc « Pour les professionnels » : liste des références par type de bâtiment, mention des codes CFC traités (271, 283, 285, 277 selon les prestations réelles), **dossier de références PDF** à télécharger, contact direct.
  - Veille hebdomadaire sur simap.ch (codes CPV/CFC concernés) et dans les FAO de Genève et Vaud.
  - Visite annuelle des services des bâtiments des communes clientes.
  - Mailing sobre aux régies (une fois par an).
- *KPI.* Téléchargements du dossier, appels d'offres consultés et déposés, invitations reçues.
- *Horizon.* 90 à 180 jours.

**10. Niche plafonds tendus, acoustique, anti-feu**
- *Pourquoi.*
  - Sujets techniques, clientèle solvable (lieux publics, bureaux, hôtels, villas).
  - Peu d'acteurs genevois spécialisés : les références du domaine sont vaudoises (Atyx, Solutions Acoustiques).
  - Le contexte réglementaire (SIA 181, révision AEAI) nourrit les questions.
- *Action.*
  - Contenus experts : « absorption ou isolation, quelle différence ? », « plafond tendu à froid (tissu) ou membrane PVC », « réduire l'écho d'une salle communale », « bruit d'impact et chape flottante ».
  - Photos avant/après et, si disponibles, fiches techniques des produits posés (classement feu, coefficient d'absorption).
  - En phase 2, des pages dédiées, p. ex. `plafond-tendu-geneve.html`.
- *KPI.* Positions et clics sur « plafond tendu Genève », « plafond acoustique Genève », « isolation phonique plafond » ; demandes qualifiées pour ces prestations.
- *Horizon.* 90 à 180 jours.

**11. Pages services × communes** (phase 2)
- *Pourquoi.* Deux concurrents le font déjà. Mais des pages clonées (« faux-plafond Onex », « faux-plafond Lancy »… avec le même texte) sont considérées comme des **pages satellites** et peuvent nuire.
- *Action.* Ne créer une page communale que si elle contient **au moins un chantier réel** dans la commune (photos, description). Commencer par Chêne-Bourg/Trois-Chêne, Carouge, Genève-ville, Collonge-Bellerive, Plan-les-Ouates, Nyon et Coppet.
- *KPI.* Impressions locales par commune.
- *Horizon.* 180 jours et plus.

**12. Plateformes payantes**
- *Pourquoi.* [Renovero](https://www.renovero.ch/fr/couts) (groupe [localsearch](https://www.localsearch.ch/fr/renovero-optimisation-des-processus-doffre-pour-les-entreprises-artisanales/)) annonce 65'000 demandes d'offres par an. Abonnements de CHF 499 à 2'099 par an. La clientèle y est surtout particulière et **compare les prix**, ce qui convient mal à un positionnement qualité et B2B.
- *Action.* Facultatif : un test de 3 mois avec l'offre la moins chère, seulement si le client veut plus de chantiers de particuliers.
- *KPI.* Coût par chantier signé.
- *Horizon.* Optionnel.

---

## 6. Focus GEO, expliqué simplement

### Le GEO, c'est quoi ?

Jusqu'ici, un client tapait « faux plafond Genève » dans Google, voyait dix liens et en ouvrait deux ou trois. Aujourd'hui, de plus en plus de gens **posent directement leur question à une intelligence artificielle** : ChatGPT, Perplexity, Copilot, ou la réponse rédigée que Google affiche désormais en haut de page (les « aperçus IA », actifs en Suisse et en français depuis mars 2025, [source](https://www.xavierstuder.com/2025/03/google-ai-overviews-en-suisse-ou-la-fin-du-web/)). L'IA lit le web et répond par un petit texte qui **cite quelques entreprises**, souvent deux ou trois, pas dix.

Le **GEO (Generative Engine Optimization)** consiste à faire en sorte que :
1. Andy Construct **fasse partie de ces quelques noms** quand quelqu'un demande « qui peut poser un plafond acoustique à Genève ? » ;
2. l'IA **décrive correctement** l'entreprise : bon nom, bonne adresse, bons métiers, bonnes références.

Des chercheurs de Princeton et de l'IIT Delhi ont montré qu'un contenu **factuel, sourcé et chiffré** augmente la visibilité dans les réponses des IA, jusqu'à +40 % dans leurs tests ([Aggarwal et al., KDD 2024](https://arxiv.org/abs/2311.09735)). Il s'agit d'un maximum en laboratoire, pas d'une garantie.

### Pourquoi c'est un avantage de premier arrivant pour une PME locale

- **Peu de concurrents s'y sont mis.** Dans la plâtrerie et les plafonds à Genève, l'essentiel des sites n'a ni FAQ, ni données structurées complètes, ni fiche d'identité claire. Une IA qui cherche une réponse fiable prendra la source la plus **claire et la plus cohérente**.
- **Les IA fonctionnent par recoupement.** Si le site, le registre du commerce, local.ch, la fiche Google et un article de presse disent la même chose, l'IA « connaît » l'entreprise et la recommande avec assurance. Cette réputation s'accumule : **plus on commence tôt, plus elle est solide**.
- **C'est peu coûteux si c'est fait à la construction du site.** Ce sont surtout du texte bien rédigé et du balisage invisible.
- **La fenêtre se referme.** 3 concurrents sur 8 (EM Plafond, Edelweiss Rénovation, Solutions Acoustiques) publient déjà un `llms.txt`.

**Soyons honnêtes sur les limites :**
- Google indique qu'**aucune optimisation spéciale** n'est requise pour ses aperçus IA : ce sont les bonnes pratiques SEO habituelles, plus une fiche d'établissement à jour ([Google](https://developers.google.com/search/docs/appearance/ai-features?hl=fr)).
- Aucun grand fournisseur d'IA n'a officiellement adopté `llms.txt` ([Ahrefs](https://ahrefs.com/blog/what-is-llms-txt/)). Il faut le voir comme un pari peu coûteux, pas comme une solution miracle.
- Depuis le 7 mai 2026, Google n'affiche plus les résultats enrichis FAQ. Le balisage FAQPage reste valide et sans risque, mais c'est **le texte visible de la FAQ** qui compte ([Search Engine Journal](https://www.searchenginejournal.com/google-drops-faq-rich-results-from-search/574429/)).
- La cible âgée utilise moins les IA (20 % des 70 ans et plus s'y disent à l'aise, [RTS](https://www.rts.ch/info/societe/2025/article/l-ia-creuse-le-fosse-numerique-etude-alarmante-sur-l-exclusion-en-suisse-29051234.html)). En revanche, les **architectes et collaborateurs de régies** plus jeunes les utilisent.

### Actions GEO concrètes

| Action | Pourquoi | Prévu dans le nouveau site ? |
|---|---|---|
| Une **FAQ de 10 questions** formulées comme on les pose, avec des réponses courtes et factuelles | Les IA reprennent volontiers des paires question-réponse nettes | **Oui**, section FAQ de l'accueil (brief SEO §4) |
| Un **paragraphe d'identité** : « Andy Construct est une entreprise genevoise de pose de faux-plafonds, cloisons, isolation et peinture, inscrite au registre du commerce depuis 2007… » | Donne à l'IA une phrase toute faite à citer | **Oui**, accueil et `llms.txt` |
| **Données structurées JSON-LD** (entreprise, services, zone desservie, FAQ) cohérentes avec le texte visible | Aide les machines à comprendre sans ambiguïté | **Oui** (exemple complet dans le brief) |
| **Fichier `/llms.txt`** | Résumé lisible par une machine ; pari à faible coût | **Oui** (fichier complet dans le brief) |
| **Fiches projets factuelles** (lieu, année, solution) | Contenu unique et vérifiable, que les IA aiment citer | **Oui**, page réalisations |
| **Mentions de normes et de contextes réels** (SIA 181, AEAI, GEnergie) avec liens officiels | Signale l'expertise ; les sources citées renforcent la crédibilité | **Oui**, FAQ et prestations (formulation prudente) |
| **Autoriser les robots d'IA** dans `robots.txt` (ne pas bloquer GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot, Google-Extended) | Un contenu bloqué ne peut pas être cité | **Oui** (brief §8.1) |
| **Bing Webmaster Tools + Bing Places** | ChatGPT Search s'appuie principalement sur l'index de Bing | Hors site : à faire (30 jours) |
| **NAP identique** sur tous les annuaires | Fondation du recoupement | Hors site : levier 1 |
| **Avis Google détaillés** (le client cite le type de travaux et la commune) | Les avis figurent parmi les principaux facteurs de visibilité dans les IA selon Whitespark 2026 | Hors site : levier 2 |
| **Mentions tierces** (Batimag, sites d'architectes, communes, associations) | Top 5 des facteurs IA selon Whitespark 2026 | Hors site : levier 8 |

### Test GEO mensuel (15 minutes)

Poser ces questions chaque mois dans ChatGPT, Perplexity, Google (aperçu IA ou mode IA) et Copilot, et noter si Andy Construct est cité, à quelle position, et si les informations sont justes :
1. « Quelle entreprise peut poser un faux-plafond à Genève ? »
2. « Qui pose des plafonds tendus à Genève ? »
3. « Entreprise pour un plafond acoustique dans une salle communale, région Genève »
4. « Comment réduire le bruit des voisins du dessus dans un appartement à Genève ? »
5. « Cloisons légères en placoplâtre pour des bureaux à Genève, quelle entreprise ? »
6. « Plâtrier-peintre à Chêne-Bourg ou Carouge »
7. « Faux-plafond coupe-feu Genève »
8. « Entreprise faux-plafonds Nyon Coppet »
9. « Andy Construct Genève avis »
10. « Qu'est-ce qu'un plafond en tissu tendu à froid ? »

---

## 7. Recommandations priorisées

### 0 à 30 jours : fondations (peu d'effort, fort impact)
1. **Obtenir les décisions du client** sur la raison sociale, l'adresse publique, l'année, l'e-mail et l'usage des références (section 0).
2. **Revendiquer ou créer et compléter la fiche Google** (catégories, zone, horaires, 30 photos, services). Créer Bing Places et Apple Business Connect.
3. **Corriger local.ch et search.ch** (une seule démarche localsearch), GGE, Kompass (catégorie), architecteromand.ch et edirex.ch.
4. **Mettre en ligne le nouveau site** avec : téléphone cliquable, formulaire court, contenu des prestations, FAQ, JSON-LD, `llms.txt`, sitemap, robots.txt, **redirections 301** depuis les anciennes URL, mentions légales et confidentialité (nLPD).
5. **Installer la mesure** : Search Console, Bing Webmaster Tools, statistiques, suivi des appels et des formulaires.
6. **Préparer la campagne d'avis** : liste de 30 clients, texte type, lien direct.

### 30 à 90 jours : preuve et notoriété
1. **Publier 10 fiches projets**, avec les références publiques en priorité.
2. **Obtenir 15 avis Google** (objectif proposé) et répondre à chacun.
3. **Constituer le dossier de références PDF** pour architectes et régies ; ajouter le bloc « Professionnels » sur la page réalisations.
4. **Lancer la veille des marchés publics** (simap.ch, FAO Genève et Vaud) avec les codes CFC 271, 283 et 285.
5. **Publier une actualité par mois** sur la fiche Google (un chantier terminé).
6. **Faire le premier test GEO** (10 questions) et le premier relevé de positions depuis Genève.

### 90 à 180 jours : différenciation
1. **Contenus de niche** : plafonds tendus, acoustique, anti-feu (2 à 3 guides courts).
2. **Première page communale**, uniquement là où il y a de vrais chantiers : Trois-Chêne/Chêne-Bourg, Carouge, Coppet/Terre Sainte.
3. **Proposer un reportage à Batimag**, demander des liens aux architectes partenaires, vérifier l'affiliation à l'association professionnelle.
4. **Atteindre 30 avis Google** (objectif proposé).
5. **Faire le bilan** : trafic, appels, demandes, positions, citations par les IA. Décider de la phase 2 (pages de services dédiées, éventuellement test Renovero).

---

## 8. Sources

**Identité et présence de l'entreprise**
- Zefix, registre du commerce (recherche « Andy Construct ») : https://www.zefix.ch
- Moneyhouse, Andy Construct, Chanton & Cie : https://www.moneyhouse.ch/en/company/andy-construct-chanton-cie-3813590051
- local.ch, fiche Andy Construct : https://www.local.ch/fr/d/carouge-ge/1227/revetement-des-plafonds-et-plafonds-suspendus/andy-construct-chanton-cie-OGrZ5DP4atJqYki9WoTjPg
- search.ch, fiche Andy Construct : https://search.ch/tel/chene-bourg/avenue-de-bel-air-57/andy-construct-chanton-cie
- GGE, catégorie plafonds suspendus : https://gge.ch/entreprises-2/wpbdp_category/plafonds-suspendus-faux-plaf/
- Art. 954a CO (obligation d'utiliser la raison de commerce) : https://www.droit-bilingue.ch/rs/lex/1911/00/19110009-a954a-fr-en.html
- J. Safra Sarasin : https://en.wikipedia.org/wiki/J._Safra_Sarasin
- BMS / Celgene : https://www.sec.gov/Archives/edgar/data/14272/000114036119021048/ex99_1.htm

**Marché**
- OFS, dépenses dans la construction 2024 : https://www.geoinformation.ch/fr/newnsb/nTNbFR3pl03pCUtty8wQL
- OFS, investissements 2025 (repris par LFM) : https://www.lfm.ch/actualite/suisse/investissements-beton-dans-la-construction-suisse-en-2025/
- OFS, page thématique : https://www.bfs.admin.ch/bfs/fr/home/statistiques/construction-logement/depenses/construction.html
- Programme Bâtiments 2024 : https://www.uvek.admin.ch/fr/newnsb/IKoj6VY8s85qnTeXJrLxc
- Genève, subventions 2026 : https://www.ge.ch/blog/geneve-energie/subventions-energetiques-2026-80-millions-francs-accelerer-renovation-du-parc-bati-genevois-2-02-2026
- Genève, IDC : https://www.ge.ch/connaitre-consommation-energie-batiment-idc/que-faire-resultat-idc-votre-immeuble
- Genève, rénovation d'un bâtiment : https://www.ge.ch/energie-renovation-batiment
- GEnergie : https://www.ge-energie.ch/des-subventions-pour-ameliorer-lefficacite-energetique-des-batiments-geneve
- SIA 181:2020 (Prona) : https://www.prona-romandie.ch/nouvelle-sia-181-protection-contre-le-bruit-dans-le-batiment-les-modifications-les-plus-importantes/
- SIA 181:2020 (shop SIA) : https://shop.sia.ch/collection%20des%20normes/architecte/181_2020_f/F/Product
- OFEV, exposition au bruit : https://www.bafu.admin.ch/fr/pollution-sonore
- AIET, communiqué du 23.01.2026 (prescriptions incendie) : https://www.bpuk.ch/fileadmin/Dokumente/bpuk/public/fr/dokumentation/medienmitteilungen/2026/Communique_de_presse_AIET_Prescription_de_protection_incendie.pdf
- AEAI, prescriptions de protection incendie : https://www.bsvonline.ch/fr/prescriptions-de-protection-incendie
- Genève, seuils des marchés publics : https://www.ge.ch/role-autorites-adjudicatrices-marches-publics/principes-types-procedures-cadre-legal
- simap.ch (La Vie économique, 2015) : https://dievolkswirtschaft.ch/fr/2015/06/2015-07-tanner-franz/
- Nouvelle plateforme simap.ch (Canton de Vaud) : https://info.vd.ch/canton-communes/articles-dgaic/2024/mars/numero-71/simapch-la-nouvelle-plateforme-de-publication-des-marches-publics-en-exploitation-des-le-1er-juillet-2024
- FAO Vaud, exemple de lot CFC 271/283/285 : https://www.faovd.ch/marches-publics/detail/2216/1179973/fondation-mont-calme-lausanne-cfc-271-283-285-platrerie-faux-plafond-peinture-pour-la-construction-d-un-ems-de-122-lits/
- Guide des CFC : https://batiguide.ch/guide-des-cfc/
- Ville de Genève, futurs projets : https://www.geneve.ch/themes/amenagement-construction-energie/construction-entretien-renovation-batiments/futurs-projets
- Bilan, bureaux à Genève : https://www.bilan.ch/story/geneve-les-bureaux-des-nouveaux-quartiers-trouvent-preneurs-966672858458
- RTS, taux de propriétaires : https://www.rts.ch/info/suisse/2024/article/les-menages-sont-proprietaires-de-leur-logement-dans-36-des-cas-28441356.html

**Comportements de recherche, SEO et GEO**
- Statcounter, moteurs de recherche en Suisse : https://gs.statcounter.com/search-engine-market-share/all/switzerland
- Pro Senectute, Digital Seniors 2025 : https://www.prosenectute.ch/fr/espace-pro/fond/etudes/digital-seniors-2025.html
- RTS / UZH, World Internet Project 2025 : https://www.rts.ch/info/societe/2025/article/l-ia-creuse-le-fosse-numerique-etude-alarmante-sur-l-exclusion-en-suisse-29051234.html
- Aperçus IA de Google en Suisse : https://www.xavierstuder.com/2025/03/google-ai-overviews-en-suisse-ou-la-fin-du-web/
- Google, fonctionnalités IA et votre site : https://developers.google.com/search/docs/appearance/ai-features?hl=fr
- Google, classement local : https://support.google.com/business/answer/7091?hl=fr
- Google, données structurées LocalBusiness : https://developers.google.com/search/docs/appearance/structured-data/local-business?hl=fr
- Google, avis auto-publiés (2019) : https://developers.google.com/search/blog/2019/09/making-review-rich-results-more-helpful
- Google, fin d'Universal Analytics : https://support.google.com/analytics/answer/11583528?hl=fr
- Fin des résultats enrichis FAQ (mai 2026) : https://www.searchenginejournal.com/google-drops-faq-rich-results-from-search/574429/
- Whitespark, facteurs de classement local 2026 : https://whitespark.ca/local-search-ranking-factors/
- Whitespark, aperçus IA en recherche locale : https://whitespark.ca/blog/case-study-the-prevalence-of-ai-overviews-in-local-search/
- BrightLocal, sources de ChatGPT Search : https://www.brightlocal.com/research/uncovering-chatgpt-search-sources/
- Aggarwal et al., GEO (KDD 2024) : https://arxiv.org/abs/2311.09735
- Spécification llms.txt : https://llmstxt.org/
- Ahrefs, llms.txt : https://ahrefs.com/blog/what-is-llms-txt/
- nLPD (PME admin.ch) : https://www.kmu.admin.ch/fr/nouvelle-loi-sur-la-protection-des-donnees-nlpd

**Plateformes et annuaires**
- Renovero, tarifs : https://www.renovero.ch/fr/couts
- localsearch / Renovero : https://www.localsearch.ch/fr/renovero-optimisation-des-processus-doffre-pour-les-entreprises-artisanales/
- Buildigo en liquidation : https://batmat.blog/buildigo-sa-liquidie-la-mobiliere-se-retire-du-marche/
- Batimag : https://www.batimag.ch/
- Barrisol, installateurs à Genève : https://barrisol.com/fr/installateur-plafond-tendu/geneve

**Concurrents**
- DSD SA : https://www.dsd-sa.ch/
- EM Plafond : https://www.em-plafond.ch/
- Class Orga : https://classorga.ch/faux-plafonds/
- Edelweiss Rénovation : https://edelweiss-renovation.ch/faux-plafond-geneve/
- Solutions Acoustiques : https://solutions-acoustiques.ch/installation-panneaux-acoustiques-suisse/geneve/
- Atyx : https://atyx.ch/
- Déco Plafond Tendu : https://www.decoplafondtendu.ch/plafond-tendu
- P3 Construction : https://www.p3construction.ch/isolation/
- Bureau Concept Suisse : https://www.bureau-concept-suisse.ch/cloisons-a-geneve/
- Lamelle-Glass : https://www.lamelle-glass.ch/cloisons-vitree/
- Cloisor : https://www.cloisor.net/installateur+de+cloison+amovible+geneve+en+suisse-z184
