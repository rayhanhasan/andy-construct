# Andy Construct – Analyse concurrentielle Suisse romande (v2)

**Projet :** site d'acquisition v2 (voir `docs/v2/programme-v2.md`)
**Date :** 31 octobre 2026
**Rédaction :** analyste concurrence (phase 1), pour le chef de projet
**Périmètre :** les 4 services validés (placo, peinture intérieure, isolation acoustique, cloisons isothermes) dans toute la Suisse romande. Ce document **complète** `docs/analyse-marche.md` (septembre 2026, centré sur Genève et les plafonds) et n'en reprend pas les constats : identité NAP, diagnostic de l'ancien site, marchés publics, contexte SIA 181 / AEAI, Renovero et les 8 concurrents genevois déjà décrits ne sont cités que lorsque la situation a changé.

> **Méthode et limites (à lire avant les chiffres)**
> - **28 requêtes** formulées comme un client (liste en §8) ont été lancées le 31.10.2026 avec notre outil de recherche web. Cet outil **n'est pas google.ch**, n'est pas géolocalisé et n'affiche ni la carte Google (pack local) ni les annonces. L'ordre des résultats donne une **image de qui occupe le terrain**, pas un classement Google. Les positions réelles se relèvent depuis Genève et Lausanne (navigation privée), puis dans la Search Console.
> - **46 sites** ont été ouverts et analysés un par un (code source, formulaires, données structurées, `llms.txt`, sitemap, poids de la page d'accueil) : 39 entreprises et 7 sites de mise en relation. Les titres de héros sont cités **mot pour mot** (balise H1 ou titre principal affiché).
> - **Publicités** : non observables directement avec nos outils. Indice utilisé : présence d'une balise de conversion Google Ads (`AW-…`) dans le code ou dans le conteneur Google Tag Manager public, ou d'un pixel Meta / TikTok. Cela prouve un **suivi publicitaire**, pas une campagne active.
> - **Avis** : seuls les avis **affichés par les sites** sont repris. Les fiches Google ne sont pas consultables sans compte depuis notre environnement.
> - **Volumes de recherche** : pas d'accès au Keyword Planner. Les colonnes « difficulté » et « valeur » de la matrice sont des **estimations à valider**.
> - **Vitesse** : quota de l'API PageSpeed épuisé. La « vitesse perçue » est estimée par le poids téléchargé de la page d'accueil (HTML, JavaScript, CSS, 12 premières images). Ce n'est pas un score Core Web Vitals.
> - Tout prix cité renvoie à une source datée. Ce qui n'a pas pu être vérifié est signalé.

---

## 1. Synthèse exécutive

1. **Le terrain en ligne n'est pas tenu par les grandes entreprises, mais par les annuaires et une nouvelle vague de sites « devis 24 h / 48 h ».** Les entreprises établies et solides (Belloni SA à Carouge depuis 1872, Buschini SA avec plus de 120 employés, Thorens SA depuis 1936, Dino Peinture SA avec une cinquantaine de collaborateurs) ont des sites minces : pas de FAQ, peu de contenu, parfois pas de formulaire, voire du texte de remplissage « Lorem ipsum » en ligne (Thorens). Ce sont de petites structures récentes et des **réseaux de mise en relation** qui produisent le contenu et captent les demandes.
2. **Les réseaux de mise en relation sont le concurrent le plus sous-estimé.** Exemples : **Helvétique Plaquiste** (« SA en cours de constitution », 156 pages villes, 11 pages « problèmes », page tarifs dont les prix ressortent dans les réponses rédigées par les moteurs de recherche) ; un réseau qui exploite *valais-peinture.ch* et *expert-isolation.ch* avec le **même numéro et la même adresse lausannoise**, sans IDE publiée. Ils occupent exactement les requêtes placo et isolation phonique d'Andy, dans tous les cantons. La transparence d'Andy (registre du commerce depuis 2007, IDE, adresse à Carouge, équipe qui exécute) devient un argument.
3. **Aucun acteur ne couvre bien les 4 services dans toute la Romandie.** Les « pan-romands » sont soit des spécialistes acoustiques (Solutions Acoustiques, Yverdon : 9 pages villes, logos Aéroport de Genève et MUDAC, balise Google Ads), soit des plateformes. Le **placo et l'acoustique pour régies, architectes et communes** sont la place à prendre à l'échelle romande. La peinture pour particuliers reste un marché de proximité.
4. **La peinture à Genève et à Lausanne est la requête la plus disputée** (une dizaine de sites optimisés par ville, annuaires, sites « mot-clé + ville », balise Google Ads détectée chez *vaud-peinture.ch*). Ce n'est pas là qu'Andy gagnera en référencement naturel. Le meilleur rapport effort/valeur : **faux-plafonds et cloisons placo, isolation phonique, correction acoustique de locaux publics, régies**.
5. **« Cloisons isothermes » est un terme piège.** En ligne, il désigne surtout les chambres froides et le transport frigorifique ; **aucun concurrent romand ne l'utilise au sens bâtiment**. Le besoin réel se cherche avec « cloison isolante », « isoler le plafond d'une cave / d'un garage », « doublage isolant ». Le service doit être renommé dans les titres et les URL, « isotherme » restant un synonyme.
6. **La barre de la preuve sociale est basse et atteignable.** Les meilleurs petits concurrents affichent **16 à 50 avis Google** (MNPro 16, Sousa Peinture 17, Madéco 35, Colosimo « 50+ ») ; les grandes entreprises n'en affichent aucun. **Rares sont ceux qui nomment des références institutionnelles** : DSD SA (études de cas), Colosimo (ONU, TPG, MSC, en peinture), Rudi SA (fiches de chantier avec maître d'ouvrage et lots), logos chez Solutions Acoustiques et Wüthrich. **Aucun ne combine des références publiques nommées avec le placo et l'acoustique**, ce que peut faire Andy. Andy n'est **pas membre** de Gypserie Peinture Genève (GPG, 87 membres vérifiés), alors que Dino Peinture, Belloni ou P3 Construction le sont.
7. **Des prix publics existent et sont repris par les IA.** Peinture intérieure : **22 à 45 CHF/m²** selon les sources romandes de 2026. Cloison placo : **95 à 350 CHF/m²** selon ce qui est inclus. Faux-plafond : **75 à 175 CHF/m²**. Taux de régie : **75 à 95 CHF/h HT**. Une FAQ « combien ça coûte » avec des fourchettes **fournies par le client** et la liste de ce qui est compris sert à la fois la confiance des 45-70 ans, la qualification des demandes et la visibilité dans les IA.
8. **Le standard de conversion est atteint par tous ; la différence se fera sur l'honnêteté.** 34 sites d'entreprises sur 39 ont un téléphone cliquable, 16 un lien WhatsApp, 13 promettent un devis en 24 ou 48 h. Les garanties sont souvent mal formulées (« garantie décennale », notion du droit français). Le GEO n'est plus un avantage de pionnier : 16 sites sur 39 ont un `llms.txt`, souvent généré par leur CMS. L'avantage restant est le **contenu factuel suisse** que personne ne publie : SIA 181 expliquée simplement, nouvelles règles du CO sur les défauts (2026), prix en CHF, références datées par commune. Les requêtes « bruit du voisin du dessus » ne renvoient aujourd'hui qu'à des forums français.

---

## 2. Cartographie

### 2.1 Ce que montrent les requêtes (observé le 31.10.2026)

Ordre approximatif renvoyé par notre outil, hors annuaires d'emploi quand c'est précisé. Voir les limites en tête de document.

| Requête (formulée comme un client) | Acteurs qui ressortent | Lecture |
|---|---|---|
| « plâtrier peintre Lausanne » | local.ch (une dizaine de pages), jobup.ch, Indeed ; puis fr-platreriepeinture.ch, lausanne-peintre.ch (IB Plâtrerie), vernay-peinture.ch, vaud-peinture.ch, rudi-sa.ch, peintrelausanne.ch, prodeco-peinture.ch, wuthrichsa.ch | Annuaires + offres d'emploi : la requête est ambiguë (métier ou entreprise) |
| « entreprise peinture Fribourg » | local.ch, business-monitor.ch ; savarypeinture.ch, madeco-peinture.ch, ekpeinture.ch, missana.ch, decofin.ch, petrinipeinture.ch | Concurrence modérée, sites anciens |
| « plâtrerie peinture Neuchâtel / La Chaux-de-Fonds » | local.ch ; rapeinture.ch, platrerie-peinture-willemin.ch, insulae.ch/immocolor, bc-deco.ch, artxl.ch, peintre-suisse.ch, buschini.ch, les-couleurs-infinies.ch, platrier-comparatif.ch | Un seul site vraiment optimisé (RA) |
| « gypserie peinture Sion Martigny » | gypsa.ch, peintremartigny.ch, bcgyps.ch, exquisluy-sembrancher.ch, valais-peinture.ch, hypp.ch, peintre-valais.ch, peintre-sion.ch | Beaucoup de domaines « mot-clé + ville » |
| « plâtrier peintre Nyon La Côte » | toni-peinture.ch, perninromain.ch, guillon-peinture.ch, agpeinture.ch, kurtalani.ch, neziri-nyon.ch, terra-peinture.ch, sousa-peinture.ch, msg-renovation.ch | Artisans locaux, peinture surtout |
| « entreprise peinture plâtrerie Morges » | mbre-platrerie-peinture.ch, tronchet-peinture.ch, mlepeinture.ch, Kompass, page Facebook (Elio Peinture), agmpeintures.ch, ofri.ch | Faible : une page Facebook se classe |
| « plâtrier peintre Vevey Montreux » | partenaires-constructions.ch, mnpro.ch (page zone Vevey), promove.ch, limipeinture.ch, **regiesriviera.ch** (annuaire de fournisseurs des régies), gate24.ch, thorens-peinture-vevey.ch, swisspro-renovation.ch | Un annuaire de régies apparaît : canal B2B à noter |
| « plâtrerie peinture Yverdon » | becherraz.ch (**site hors ligne** au 31.10), borges-peinture.ch, dh-batiment.ch, colorispro.ch, evasionpeinture.ch, ametipeinture.ch, hopeinture.ch, dinopro.ch | Faible |
| « plâtrerie peinture Delémont » | martiarcjura.ch, bichsel-peinture.ch (**injoignable** au 31.10), platrier-comparatif.ch, entreprise-peinture-renovation.ch, wesleybugnon.ch, peinturetomaselli.ch, batilook.ch | Très faible |
| « entreprise plâtrerie peinture Bulle Gruyère » | savarypeinture.ch, madeco-peinture.ch, ekpeinture.ch, missana.ch, decofin.ch, petrinipeinture.ch | Faible |
| « plâtrier Genève » | group-sb.ch, dinopeinture.ch, batimak.ch, carletti-entreprise.ch, helle-peinture.ch, swissedifice.ch, genevepeinture.ch, rb-constructions.ch, realite.ch | Fragmenté, aucun leader |
| « entreprise peinture Genève appartement devis » | peinturesgeneve.ch, vlppeinture.ch (2 pages), mlepeinture.ch, chaumont-peinture.ch, entreprise-peinture-geneve.ch, colosimo.ch, renovhome.ch, mlhpeinture.ch, edelweiss-renovation.ch | **Le plus disputé** : prix affichés, « garantie 5 ans », « devis 24 h » |
| « entreprise plâtrerie peinture Genève régies architectes » | dsd-sa.ch, rb-constructions.ch, lemanpeinture-ge.ch, prorenovconstruct.ch, ardmupro.ch/regies-architectes, edelweiss (2 pages), dinopeinture.ch, batimak.ch, helle-peinture.ch | Seuls ArdmuPro et Edelweiss ont une page dédiée aux régies |
| « pose placo Genève cloison » | edelweiss (2 pages « plaquiste »), p3construction.ch, entreprise-renovation-suisse.ch, bertolit.ch, jubilee-construction.ch, idtravaux.ch, adr-renova.ch, carletti-entreprise.ch | Edelweiss domine avec des pages par service |
| « faux plafond placo Lausanne » | lausanne-peintre.ch (3 pages), cr1-peintures.com (entreprise française), travaux.com, carletti, bskmontage.ch, solarconstruct.ch | Une entreprise française se classe : terrain peu travaillé |
| « cloison placo Fribourg / Neuchâtel / Sion » | batmat (plateforme), renobat-general.ch, minolorenzini.ch, madeco, entreprisedepeinturefribourg.ch, stoppa-peinture.ch, leiri-platre.ch | Faible |
| « isolation phonique appartement Genève » | isoltechsarl.com (gaines techniques surtout), ms-contractor.ch, isoltesa.ch, expert-isol.ch (CVC), entreprise-mssa.ch, edelweiss (isolation intérieure), **expert-isolation.ch** (réseau), isolaccesisolation.ch, itpf-isolations.ch | Beaucoup d'isoleurs **techniques** (gaines, CVC) : peu de vraies réponses pour un logement |
| « isolation acoustique Lausanne cloison phonique » | leivarenovation.ch, expert-isolation.ch, peinture-isolation.ch, bureau-concept-suisse.ch, solutions-acoustiques.ch (2 pages), expert-isol.ch, clotures-naturelles.com (France), travauxrenovation.ch | Idem |
| « isolation phonique Fribourg / Neuchâtel » | expert-isolation.ch (une page par ville), mas-peinture.ch (2 pages), innobat.ch, puis sites français | **Quasi vide** hors réseau |
| « isolation phonique Sion / plafond acoustique Valais » | lambda-isolation.ch, abrium.net, puis sites français | **Quasi vide** |
| « cloison isotherme » | Aucun prestataire romand : chambres froides, semi-remorques, brevets, fiches techniques | Mauvaise intention de recherche |
| « isolation plafond cave garage Genève Vaud » | autourdelamaison.ch, entreprise-construction-geneve.ch, fgservices.ch, edelweiss (page cave & garage), isoleco.ch (2 pages), isoltechsarl.com, starofservice.ch | Peu disputé, besoin réel |
| « bruit voisin du dessus faux plafond acoustique Suisse » | forumconstruire.com, futura-sciences.com, lamaisonsaintgobain.fr… (France) | **Aucune source suisse** |
| « plafond acoustique salle communale école » | solutions-acoustiques.ch (6 pages), acouswiss.ch, solarconstruct.ch, monbureau.ch | Un seul spécialiste occupe la niche B2B |
| « prix peinture m² Suisse romande » | chiffr.ch, batmat, valais-peinture.ch, devis-rapide.ch, vlppeinture.ch, yoojo.ch, marcoaraujo.ch, artisan-romandie.ch | Plateformes et guides ; ce sont eux que citent les IA |
| « prix cloison placo Suisse » | batmat, mnpro.ch, helvetique-plaquiste.ch, idtravaux.ch, ofri.ch (3 pages), sos-travaux.ch, mesartisans.ch | Idem |
| « Andy Construct Carouge plâtrerie » | Aucun résultat pertinent (pages françaises) | **Andy est invisible**, même sur son nom |

**Ce qu'il faut retenir des requêtes**
- **Les annuaires** (local.ch d'abord, puis Kompass, business-monitor.ch, search.ch) occupent les requêtes « métier + ville » dans tous les cantons. Leur correction est déjà prévue (analyse de septembre, levier 8).
- **« Plâtrier peintre » est aussi un intitulé de poste.** jobup, Indeed et des agences d'intérim remontent. En publicité, exclure dès le départ : *emploi, job, offre, CFC, apprentissage, salaire, intérim, formation*.
- **Les domaines « mot-clé + ville » se multiplient** (peintrelausanne.ch, vaud-peinture.ch, peintre-sion.ch, peintre-valais.ch, valais-peinture.ch, peinturesgeneve.ch, entreprise-peinture-geneve.ch). Plusieurs n'affichent ni raison sociale ni IDE.
- **Acoustique hors Genève et Lausanne** : les seules pages locales sont celles d'un réseau de mise en relation et d'un spécialiste vaudois. C'est la zone la moins disputée pour un vrai spécialiste.

### 2.2 Carte des acteurs

Services en recouvrement avec Andy : **P** = placo (cloisons, doublages, faux-plafonds) · **Pe** = peinture intérieure · **A** = acoustique · **T** = isolation thermique intérieure. Force en ligne : ★ faible, ★★ moyenne, ★★★ forte (contenu, données structurées, avis, conversion).

| Acteur (site) | Base | Type | Taille publiée | Recouvrement | Force en ligne | Menace pour Andy |
|---|---|---|---|---|---|---|
| **Genève** | | | | | | |
| DSD SA (dsd-sa.ch) | Chêne-Bougeries | Plâtrier-peintre établi | n. c. (depuis 1995) | P Pe A | ★★ | **Élevée** (mêmes cibles, références comparables) |
| Edelweiss Rénovation SA (edelweiss-renovation.ch) | Genève | Rénovation orientée web | n. c. | P Pe T | ★★★ | **Élevée** (particuliers, régies) |
| ARDMUPRO Sàrl (ardmupro.ch) | Grand-Lancy | Rénovation « tout-en-un » orientée web | n. c. | P Pe T A | ★★★ | Élevée (régies) |
| Dino Peinture SA (dinopeinture.ch) | Vernier | Plâtrier-peintre établi, membre GPG | ~50 collaborateurs | P Pe T | ★ | Moyenne (taille, régies) |
| Entreprise Belloni SA (belloni-sa.ch) | **Carouge** | Gros et second œuvre, membre GPG | n. c. (depuis 1872) | P Pe A | ★ | Moyenne (même commune, acoustique, cloisons modulaires) |
| Léman Peinture (lemanpeinture-ge.ch) | Petit-Lancy | Peinture pour régies | n. c. | Pe | ★ | Faible |
| MS Contractor SA / Entreprise du Bâtiment MS SA (ms-contractor.ch, entreprise-mssa.ch) | Genève (même adresse) | Entreprise générale, SEO massif | n. c. | P Pe A | ★★ (2'063 et 547 URL) | Moyenne |
| Colosimo Peinture (colosimo.ch) | Genève | Artisan peintre, maîtrise fédérale ; cite ONU (salle des Assemblées), TPG, MSC | « 75+ projets » | Pe | ★★ (4,9, « 50+ avis ») | Moyenne en peinture (références institutionnelles) |
| VLP Peinture Sàrl (vlppeinture.ch) | Genève | Artisan peintre orienté web | n. c. | Pe | ★★★ (grille de prix) | Faible à moyenne |
| Peintures Genève (peinturesgeneve.ch) | Genève | Site « mot-clé », sans IDE | n. c. | Pe | ★★ | Faible |
| Isoltech Sàrl (isoltechsarl.com) | Genève | Isolation technique (gaines, coupe-feu) | n. c. | A T | ★ | Faible |
| P3 Construction SA (p3construction.ch) | Grand-Lancy | Plâtrerie, membre GPG | n. c. | P | ★ (déjà décrit en septembre) | Moyenne |
| **Vaud** | | | | | | |
| G & N Wüthrich SA (wuthrichsa.ch) | Région lausannoise | Plâtrier-peintre établi, présidence GVEPP | n. c. (depuis 1966) | P Pe T | ★★ | Moyenne (architectes, communes) |
| Rudi SA (rudi-sa.ch) | Penthalaz | Plâtrier-peintre, orienté architectes : fiches de chantier avec maître d'ouvrage, entreprise totale et lots (p. ex. Centre thermal d'Yverdon), profil architectes.ch | n. c. | P Pe | ★★ (≈ 6'000 mots de projets sur l'accueil) | Moyenne (B2B vaudois) |
| F-R Plâtrerie peinture Sàrl (fr-platreriepeinture.ch) | Villars-Sainte-Croix | Artisan orienté web | n. c. | P Pe A | ★★★ | Moyenne |
| IB Plâtrerie Peinture Sàrl (lausanne-peintre.ch) | Lausanne | Artisan, pages placo et faux-plafonds | n. c. | P Pe | ★★ | Moyenne (Lausanne) |
| BSK Montage Sàrl (bskmontage.ch) | Lausanne | Faux-plafonds, SEO massif | n. c. | P | ★★ (3'438 URL) | Moyenne (Lausanne) |
| Sousa Peinture Sàrl (sousa-peinture.ch) | Nyon | Artisan orienté web | « plus de 8 collaborateurs » | Pe P | ★★★ | Moyenne (La Côte) |
| Toni Peinture (toni-peinture.ch) | Nyon | Artisan | n. c. (depuis 1997) | Pe P | ★ | Faible |
| Kurtalani Rénovation SA (kurtalani.ch) | Gland | Rénovation | n. c. | Pe P T | ★ | Faible |
| Thorens SA (thorens-peinture-vevey.ch) | Vevey | Établi, se dit actif dans toute la Romandie | n. c. (depuis 1936) | Pe P | ★ | Faible |
| Partenaires Constructions Sàrl (partenaires-constructions.ch) | Villeneuve | Artisan, page isolation acoustique | n. c. | Pe P A | ★★ | Faible |
| Solutions Acoustiques Sàrl (solutions-acoustiques.ch) | Yverdon / showroom Daillens | **Spécialiste acoustique pan-romand** | « +300 projets » | A | ★★★ (balise Google Ads) | **Élevée sur l'acoustique** |
| Lambda Technique d'isolation SA (lambda-isolation.ch) | Lausanne et Sion | Calorifugeage, feu, acoustique, plafonds | n. c. | A P | ★ | Moyenne (B2B) |
| Leiva Rénovation (leivarenovation.ch) | Fey | Artisan, pixel Meta | n. c. | Pe P A | ★★ | Faible |
| **Fribourg** | | | | | | |
| Madéco Peinture SA (madeco-peinture.ch) | Cousset | Artisan orienté web, membre AFEPP | n. c. | Pe P | ★★★ (4,9/5, 35 avis) | Faible (distance) |
| P-Y Savary SA (savarypeinture.ch) | Bulle | Établi, ISO 9001, membre AFEPP | « environ 50 employés » (meta) | Pe P T | ★ | Faible |
| MAS Peinture (mas-peinture.ch) | Fribourg | Artisan, page isolation phonique | n. c. | Pe P A | ★★ | Faible |
| **Neuchâtel** | | | | | | |
| Buschini SA (buschini.ch) | Neuchâtel + 3 sites NE/VD | **Établi, le plus gros de l'échantillon** | « plus de 120 employés » | Pe P A | ★ | Moyenne (B2B NE/VD) |
| RA Plâtrerie Peinture (rapeinture.ch) | Neuchâtel | Artisan orienté SEO | n. c. | Pe P | ★★ | Faible |
| Les Couleurs Infinies Sàrl (les-couleurs-infinies.ch) | Neuchâtel / La Chaux-de-Fonds | Artisan | n. c. | Pe P | ★ | Faible |
| **Valais** | | | | | | |
| Gypsa SA (gypsa.ch) | Martigny | Établi (« 45 ans ») | n. c. | Pe P T | ★ | Faible |
| Hypp SA (hypp.ch) | Sion | Artisan, contenu SEO de faible qualité | n. c. | Pe P | ★ | Faible |
| MNPro (mnpro.ch) | Collombey | Artisan orienté web, maîtrise fédérale | « 70+ chantiers depuis 2021 » | Pe P | ★★★ (estimation IA, blog prix) | Faible (Chablais) |
| **Jura / Jura bernois** | | | | | | |
| Marti Arc Jura SA (martiarcjura.ch) | Delémont (succursale) | Groupe BTP, département peinture-plâtrerie | n. c. | Pe P | ★ | Faible |
| S. Bichsel Sàrl, Beuchat J.-C. Sàrl, Bâtilook | Tramelan, Glovelier, Jura | Artisans | Beuchat : 17 personnes selon un annuaire | Pe P | ★ | Faible |
| **Pan-romands et plateformes** | | | | | | |
| Groupe Orllati (orllati.ch), dont ORLLATI (GE) SA membre GPG | Vaud, Genève | Groupe BTP | n. c. | P Pe | ★ | Moyenne sur les gros lots |
| Alic Peinture & Rénovation Sàrl (alicpeinture.ch) | Cugy | Se dit actif VD GE FR NE VS | n. c. | Pe P | ★ | Faible |
| **Helvétique Plaquiste** (helvetique-plaquiste.ch) | Non précisé, « SA en cours de constitution » | **Mise en relation** | — | P A T | ★★★ (203 URL) | **Élevée sur le placo** |
| Réseau *valais-peinture.ch* + *expert-isolation.ch* | Adresse : Rue de Genève 100, Lausanne | **Mise en relation** (« réseau de partenaires ») | — | Pe A T | ★★★ | **Élevée sur l'isolation phonique** |
| Sites « mot-clé + ville » (peintrelausanne.ch, vaud-peinture.ch, peintre-valais.ch…) | Divers | Artisans ou intermédiaires, identité peu claire | — | Pe P | ★★ | Moyenne (peinture) |
| Renovero, Ofri, batmat, IDtravaux | Suisse | Plateformes de devis | — | tous | ★★★ | Faible (clientèle qui compare les prix) |

### 2.3 Constats chiffrés sur les 39 sites d'entreprises analysés

| Élément | Nombre de sites | Remarque |
|---|---|---|
| Téléphone cliquable sur l'accueil | 34 / 39 | Sans : Dino Peinture, Gypsa, Léman Peinture, Partenaires Constructions, Vernay Peinture |
| Formulaire de 3 à 8 champs (accueil ou contact) | 32 / 39 | Plus long : MAS Peinture (12), MNPro (10). Aucun formulaire lisible dans le code : Belloni, DSD, Lambda, MS Contractor, Partenaires Constructions (certains chargés en JavaScript) |
| Lien WhatsApp | 16 / 39 | Souvent en pied de page |
| Promesse de devis en 24 h ou 48 h | 13 / 39 | + 5 sites de mise en relation sur 7 |
| Envoi de photos dans le formulaire | 4 / 39 | ArdmuPro, F-R Plâtrerie, MNPro, Peinture Isolation |
| Prix en CHF sur l'accueil | 4 / 39 | Les grilles détaillées sont plutôt sur des pages « tarifs » ou des articles |
| Balisage FAQPage | 10 / 39 | + 5 sites de mise en relation sur 7 |
| Fichier `llms.txt` | 16 / 39 | Plusieurs générés automatiquement par le CMS (Duda, All in One SEO) : l'argument « pionnier » de septembre ne tient plus |
| Note agrégée (AggregateRating) dans le code | 3 / 39 | Edelweiss 5/5 sur 3 avis, RA Peinture 5/5 sur 19, VLP 5/5 sur 26 ; les notes affichées par l'entreprise elle-même ne donnent pas d'étoiles dans Google |
| Balise Google Ads détectée | 2 sites | *vaud-peinture.ch* (AW-18226059887), Solutions Acoustiques (AW-11334218998 dans son conteneur GTM) |
| Pixel Meta ou TikTok | 2 sites | Leiva Rénovation (Meta), Partenaires Constructions (TikTok) |
| Universal Analytics encore installé (inactif depuis 2023) | 5 | Belloni, Gypsa, Immocolor, Lambda, Marti Arc Jura (et l'ancien site d'Andy) |

---

## 3. Fiches concurrents

17 fiches : les plus forts par canton, 3 acteurs pan-romands (Solutions Acoustiques, Buschini, Thorens) et les réseaux de mise en relation. Poids mesuré = HTML / JavaScript / 12 premières images de la page d'accueil, au 31.10.2026.

### 3.1 DSD SA — Chêne-Bougeries (GE) · concurrent de référence

*Déjà décrit en septembre (7 études de cas, LocalBusiness complet). Compléments :*
- **Héro (H1)** : « Gypserie, plâtrerie et peinture à Genève »
- **CTA** : « Nous contacter » ; téléphones 079 708 52 57 et 022 349 14 55.
- **Formulaire** : un bloc « Votre projet » existe, mais **aucun champ n'est présent dans le code** (formulaire chargé par Squarespace en JavaScript, invisible pour les robots). Adresse e-mail en `@bluewin.ch`.
- **Promesses** : aucune (ni délai, ni garantie, ni prix).
- **Preuve sociale** : références par catégorie (Bureaux, Logements, Institutions, Culture, Commerces, Hôtels). Aucun avis, aucun logo, aucune association (absent de la liste GPG).
- **Technique** : pas de `llms.txt`, 12 URL dans le sitemap. **Lourd** : 28 fichiers JavaScript (≈ 800 Ko) et ≈ 2,3 Mo pour 12 images.
- **Design** : sobre (modèle Squarespace).
- **À retenir** : le plus proche d'Andy par les références, mais **rien pour convertir** (pas de promesse, pas de formulaire lisible, pas d'avis). Andy peut le dépasser sur la conversion et la vitesse.

### 3.2 Edelweiss Rénovation SA — Genève · leader SEO genevois

- **Héro (H1)** : « Rénovation intérieure à Genève, avec un suivi clair du chantier »
- **CTA** : « Demander un devis gratuit », « Appeler Edelweiss » ; WhatsApp en pied de page ; horaires lu-ve 07:00-16:00.
- **Formulaire** : 7 champs (nom, e-mail, téléphone, 3 listes déroulantes, message).
- **Promesses** : « Devis détaillé après visite technique », devis sous 48 h après déplacement gratuit (FAQ), délais indicatifs (1 à 2 semaines pour un rafraîchissement, 4 à 8 semaines pour une transformation). Pas de garantie chiffrée. Tarifs préférentiels pour les régies partenaires.
- **Preuve sociale** : « ★★★★★ 5,0 sur Google · 3 avis » ; la section « Ils nous ont fait confiance » ne contient que ces 3 avis, **sans logo ni référence nommée**.
- **Contenu** : une page par service (peinture, plâtrerie, faux-plafonds, isolation intérieure, **isolation cave & garage**, rénovation d'appartement, suivi de chantier), page zones (8 communes), blog avec **prix 2026** (faux-plafonds), page régies. 81 URL.
- **Technique** : données structurées très complètes (GeneralContractor, OfferCatalog, AggregateRating, Review), `llms.txt` complet. 220 Ko de JavaScript, ≈ 2,1 Mo d'images.
- **Design** : moderne, assez chargé (Divi).
- **À retenir** : modèle de **couverture de contenu**, mais **preuve faible** (3 avis, aucune référence). Andy le bat sur la preuve ; il faut l'égaler sur les pages services et la page cave/garage (cloisons isothermes).

### 3.3 ARDMUPRO Sàrl — Grand-Lancy (GE) · meilleur dispositif de conversion observé

- **Héro** : surtitre « Rénovation & second œuvre à Genève », grand titre « Votre projet, notre métier. », sous-titre « Une équipe salariée qui prend en charge tout votre second œuvre — du gros œuvre aux finitions. »
- **CTA** : « Demander un devis », « Devis gratuit », « Nous appeler », « Écrivez-nous sur WhatsApp », « Notre offre pour les pros ».
- **Formulaire de devis** (page /devis) : prénom, téléphone, ville/NPA (obligatoires) ; type de travaux (choix multiple) ; **jusqu'à 8 photos** facultatives ; description facultative ; **mode de recontact : appel ou WhatsApp**. **Aucune adresse e-mail demandée.** Accroche : « Quelques photos, deux minutes de formulaire ».
- **Promesses** : « Réponse sous 48 heures », « Visite sur place gratuite et sans engagement », devis « poste par poste » (« pas une fourchette »). Section « Des engagements, pas des promesses » : garanties « Parfait achèvement à 1 an et garantie décennale, selon le Code des obligations » (**formulation erronée** : « parfait achèvement » et « décennale » sont des notions du droit français ; en Suisse, l'action pour défauts d'un ouvrage immobilier se prescrit par 5 ans), équipe salariée, « RC professionnelle et conformité CCT-SOR », un seul interlocuteur.
- **Preuve sociale** : aucun avis ni référence client ; logos de **fournisseurs** (Sika, Knauf, Rigips, Mapei, Weber, Sto, Forbo, Laufen, Flumroc). Les compteurs animés s'affichent « 0+ » quand le JavaScript n'est pas exécuté (ce que voient les robots et les IA).
- **Contenu** : FAQ de 16 questions (devis, délais, prix, garanties, PPE, acompte), page régies et architectes (« Devis au poste, 48 h », « Photos chaque jour », « Équipe en propre »), guides. ≈ 2'800 mots sur l'accueil.
- **Technique** : HomeAndConstructionBusiness + FAQPage + OfferCatalog, `llms.txt`, 51 URL. Léger (≈ 265 Ko de JS, CSS minimal).
- **Design** : dense, très textuel.
- **À retenir** : **le formulaire à copier dans l'esprit** (pas d'e-mail obligatoire, choix appel ou WhatsApp, photos facultatives) et la logique « engagements vérifiables ». À éviter : les termes juridiques étrangers et les compteurs animés.

### 3.4 Dino Peinture SA — Vernier (GE/VD)

- **Héro (H1)** : « Entreprise de bâtiment à Genève depuis 2005. »
- **Positionnement** : second œuvre (plâtrerie, peinture, façades), « une cinquantaine de collaborateurs ».
- **CTA / formulaire** : **pas de téléphone cliquable** sur l'accueil ; formulaire de 7 champs en page contact ; e-mail `@bluewin.ch`.
- **Preuve sociale** : **membre GPG** (liste vérifiée) ; aucun avis, aucune référence nommée.
- **Technique** : WordPress, données structurées de base, pas de `llms.txt`, 22 URL. Poids correct (≈ 130 Ko de JS, ≈ 400 Ko d'images).
- **À retenir** : une capacité réelle (50 personnes) mal montrée. Concurrent sérieux sur les **appels d'offres de régies**, pas en ligne.

### 3.5 Entreprise Belloni SA — Carouge (GE) · voisin de commune

- **Héro** : H1 « Belloni SA », accroche « Avec plaisir nous construisons. Depuis 1872. »
- **Positionnement** : gros et second œuvre. Spécialités mises en avant : **« Correction et isolation acoustique »** et **« Cloisons modulaires »**, en plus de la gypserie (cloisons sèches, faux-plafonds) et de la peinture.
- **CTA / formulaire** : **aucun formulaire** ; téléphone 058 226 73 00 et e-mail.
- **Preuve sociale** : « plus de 150 ans d'expérience », membre GPG ; aucune référence nommée sur l'accueil.
- **Technique** : données structurées de base, pas de `llms.txt`, Universal Analytics encore installé.
- **À retenir** : même commune et même spécialité acoustique, mais **positionnement entreprise générale**. Andy se distingue par la **spécialisation intérieure** et la facilité de contact.

### 3.6 G & N Wüthrich SA — région lausannoise (VD)

- **Héro (H1)** : « Votre plâtrier peintre à Lausanne » ; sous-titre « Wüthrich SA, votre partenaire de confiance pour des solutions sur mesure en plâtrerie, peinture, isolation et décoration. »
- **CTA** : « Contactez-nous », « Obtenir un devis gratuit », inscription à la newsletter. **Téléphone limité à « Lun-Ven : 8h-11h / 14h-16h »** (frein pour une cible qui appelle).
- **Formulaire** : 8 champs (contact), WhatsApp sur la page contact, newsletter (secteur, nom, e-mail).
- **Preuve sociale** : depuis 1966, « Titulaires d'une maîtrise fédérale depuis 1993 », **présidence du GVEPP**, membre de la **FREPP** et de la FVE ; logos « Ils nous font confiance » (d'après les noms de fichiers : Migros, Manor, Aclens, Ville de Morges et un fichier « Le Mont Nouveau » ; à confirmer visuellement) ; « expérience reconnue par le service du patrimoine du canton de Vaud ».
- **Contenu** : segmentation par client (Entreprises, Architectes, Particuliers, Patrimoine), actualités, réalisations.
- **Technique** : WordPress/Elementor, GTM, pas de `llms.txt`, 27 URL.
- **À retenir** : l'un des rares concurrents qui affiche **des communes clientes et ses affiliations professionnelles** (avec Rudi SA, qui publie des fiches de chantier détaillées pour les architectes). C'est le registre de preuve qu'Andy peut dépasser avec ses 18 références.

### 3.7 Sousa Peinture Sàrl — Nyon (VD) · référence pour La Côte

- **Héro (H1)** : « Entreprise de peinture à Nyon et en Suisse romande » ; sous-titre : « Une équipe de plus de 8 collaborateurs qualifiés et passionnés pour transformer vos intérieurs et vos façades, basés à Nyon, de Genève au Valais. »
- **CTA** : « Demander un devis gratuit », « Voir nos services », WhatsApp, version anglaise.
- **Formulaire** : 7 champs (nom, téléphone, e-mail, lieu, type de service, message…).
- **Preuve sociale** : « ★★★★★ 5,0 sur Google, 17 avis » dès le héro, « Brevet fédéral », « entreprise formatrice ».
- **Contenu** : FAQ, réalisations « à Nyon et sur La Côte », déroulé du chantier, 66 URL.
- **Technique** : HousePainter + FAQPage + OfferCatalog, `llms.txt`. Léger (≈ 170 Ko de JS, ≈ 800 Ko d'images).
- **À retenir** : **la preuve au-dessus de la ligne de flottaison** (note, qualification, entreprise formatrice), sans exagération. Format à reprendre pour Andy dès que les avis existent.

### 3.8 F-R Plâtrerie peinture Sàrl — Villars-Sainte-Croix (VD)

- **Héro (H1)** : « Entreprise de plâtrerie, peinture et rénovation – Suisse romande » ; surtitre « Ouvriers qualifiés CFC · Depuis 2009 ».
- **CTA** : « Devis gratuit », téléphone 021 (12 liens), WhatsApp.
- **Formulaire** : 7 champs dont **photos du chantier**, ville et type de travaux.
- **Promesses** : « Devis gratuit sous 24h », chantier propre, sols protégés. **Zone incohérente** selon les pages (rayon de 65, 60 ou 80 km).
- **Contenu** : « 15 prestations », pages villes (Lausanne, Morges, Nyon…), page « Professionnels », actualités ; 52 URL.
- **Technique** : HousePainter + GeoCircle, `llms.txt`.
- **À retenir** : bon exemple de page « Professionnels », mais la promesse « 24 h » et les incohérences de zone fragilisent la crédibilité.

### 3.9 Thorens SA — Vevey (VD) · « pan-romand » déclaré

- **Héro (H1)** : « Bienvenue chez Thorens SA à Vevey »
- **Positionnement** : entreprise familiale depuis 1936, peinture, plâtrerie, tapisserie, isolation, « intervient dans toute la Suisse romande ».
- **CTA** : « Nous contacter », **numéro gratuit 0800 932 932** et 021 925 09 00.
- **Formulaire** : 4 champs obligatoires (nom/prénom, e-mail, téléphone, message).
- **Preuve sociale** : aucune (ni avis, ni association, ni référence) ; listé dans l'annuaire de fournisseurs *regiesriviera.ch*.
- **Défaut visible** : **titres et paragraphes « Lorem ipsum dolor sit amet » en ligne** sur l'accueil.
- **Technique** : constructeur Duda, `llms.txt` généré automatiquement, seul balisage « WebSite ».
- **À retenir** : la promesse « toute la Suisse romande » **sans preuve** ne suffit pas. Andy doit adosser la même promesse à des chantiers réels hors de Genève.

### 3.10 Solutions Acoustiques Sàrl — Yverdon-les-Bains (VD) · spécialiste acoustique pan-romand

- **Héro (H1)** : « Spécialiste du traitement acoustique intérieur en Suisse romande » ; sous-titre « Améliorez durablement l'acoustique de vos espaces ».
- **CTA** : « Discuter de votre projet », « Prendre RDV » (showroom à Daillens), « Demander un devis gratuit », « Voir les avis google », WhatsApp, boutique en ligne.
- **Formulaire** : 7 champs dont une liste déroulante.
- **Promesses** : devis gratuit après analyse de l'espace, « Planning clair, interventions rapides », pose en site occupé, classement feu des panneaux (« DIN 4102 — B1, EN 13501-1 »), **PV acoustiques sur demande**.
- **Prix publics** : panneau PET « dès 99 CHF / panneau », baffle « dès 105 CHF », pose « dès 100 CHF / panneau » (HT, hors livraison).
- **Preuve sociale** : note Google 4,9 (nombre non affiché), « +300 projets », « +12 000 m² », **logos** (Aéroport de Genève, MUDAC, CFF, Migros, Losinger Marazzi…), 10 témoignages, installateur agréé Barrisol.
- **Contenu** : pages par type d'espace (bureaux, écoles, restaurants, salles de conférence…), **9 pages villes** (Lausanne, Genève, Fribourg, Delémont, Morges, Neuchâtel, Nyon, Sion, Yverdon), vidéo « Écoutez la différence » (avant/après), 147 URL.
- **Publicité** : balise de conversion Google Ads dans son conteneur GTM.
- **Technique** : FAQPage + HomeAndConstructionBusiness ; `llms.txt` **absent** au 31.10.2026 (présent en septembre). JS ≈ 450 Ko.
- **À retenir** : **le concurrent direct sur l'isolation acoustique**, surtout en B2B. Son offre est la **correction acoustique par panneaux** ; Andy peut se placer sur l'**isolation phonique intégrée au placo** (cloisons, doublages, faux-plafonds) et sur la combinaison acoustique + finition peinture.

### 3.11 Madéco Peinture SA — Cousset (FR)

- **Héro (H1)** : « Entreprise de peinture dans le canton de Fribourg » ; sous-titre « Votre artisan peintre de confiance. »
- **CTA** : « Devis gratuit », « Demander un devis », téléphone 079 318 13 25.
- **Formulaire** : 5 champs : nom et téléphone obligatoires, **e-mail facultatif**, type de travaux, projet.
- **Promesses** : « Sans sous-traitance — Artisan direct », « Garantie sur tous nos travaux » (sans durée), devis gratuit et sans engagement.
- **Preuve sociale** : **4,9/5 sur 35 avis Google**, membre **AFEPP** (liste vérifiée), logos de partenaires fournisseurs (Caparol, KABE, Würth, Sikkens, Rigips…).
- **Contenu** : pages par ville (Fribourg, Bulle, Estavayer, Payerne, Morat, Avenches), FAQ (3 questions), page « Plâtrier Fribourg ».
- **Technique** : LocalBusiness + FAQPage, GTM, pas de `llms.txt`. **Très léger** (≈ 36 Ko de JS).
- **À retenir** : la combinaison **avis nombreux + e-mail facultatif + page légère** est le meilleur rapport simplicité/efficacité de l'échantillon.

### 3.12 P-Y Savary SA — Bulle (FR)

- **Héro** : les seuls H1 sont « Membre » et « Formation » (structure faible) ; accroche « L'entreprise Pierre-Yves Savary SA vous souhaite la bienvenue ! »
- **Positionnement** : peinture, isolation, plâtrerie, sablage, **toiles tendues, faux-plafonds** ; « Nous œuvrons principalement en Suisse Romande ».
- **Formulaire** : 5 champs.
- **Preuve sociale** : **ISO 9001**, entreprise formatrice, « environ 50 employés » (description), membre AFEPP (liste vérifiée ; le site emploie encore l'ancien sigle AFMPP).
- **Technique** : Joomla ancien, pas de sitemap, pas de `llms.txt`. **≈ 6,9 Mo pour 12 images** : le site le plus lourd de l'échantillon.
- **À retenir** : un acteur crédible (ISO, 50 personnes) avec un site daté. Montre que **la taille ne se voit pas en ligne**.

### 3.13 Buschini SA — Neuchâtel (NE/VD) · pan-romand régional

- **Héro (H1)** : « Artisan du bâtiment depuis 1964 »
- **Positionnement** : peinture, plâtrerie, isolation, **faux-plafonds, acoustique, revêtement coupe-feu**, hydrogommage, facility services ; « plus de 120 employés » ; sites à Neuchâtel, Penthaz, Fleurier et La Chaux-de-Fonds.
- **CTA** : « Nous contacter », « Postuler » ; 4 numéros de téléphone.
- **Formulaire** : 6 champs (page contact).
- **Preuve sociale** : « plus de 2'000 chantiers » ; aucune référence nommée, aucun avis, aucune association affichée.
- **Technique** : Wix, page d'accueil de 167 Ko de HTML, `llms.txt` présent, balisage LocalBusiness minimal.
- **À retenir** : **le plus gros concurrent observé**, présent sur les mêmes métiers (faux-plafonds, acoustique) dans l'arc NE-VD, mais sans contenu ni preuve. Concurrent sur les appels d'offres, pas sur la recherche.

### 3.14 RA Plâtrerie Peinture — Neuchâtel (NE)

- **Héro (H1)** : « Votre expert en peinture , plâtrerie & isolation périphérique dans le canton de Neuchâtel » (sic)
- **CTA** : « Demander un devis gratuit », « Découvrir nos services ».
- **Formulaire** : 5 champs (nom, e-mail, téléphone, prestation, message).
- **Preuve sociale** : section « Avis de nos clients » ; note **5/5 sur 19 avis** déclarée dans le code (non vérifiable).
- **Contenu** : zones (La Chaux-de-Fonds, Val-de-Ruz, Val-de-Travers, Le Landeron), FAQ ; meta « Qualité suisse ! ».
- **Technique** : LocalBusiness + FAQPage + AggregateRating, 11 URL, léger.
- **À retenir** : un petit site bien optimisé suffit à dominer Neuchâtel. **Le canton est peu disputé**.

### 3.15 Gypsa SA — Martigny (VS)

- **Héro (H1)** : « ENTREPRISE DE PEINTURE, PLÂTRERIE SITUÉE À MARTIGNY »
- **Positionnement** : peinture, plafonds, plâtrerie, isolation, **obturation coupe-feu** ; entre Sierre et Montreux. Incohérence : le titre dit « depuis 40 ans », l'accueil « Cette année, nous avons 45 ans ! ».
- **CTA / formulaire** : **pas de téléphone cliquable** ; formulaire de **8 champs** (nom, prénom, e-mail, adresse, NPA, ville, téléphone, message).
- **Preuve sociale** : mention de la maîtrise fédérale ; aucun avis.
- **Technique** : aucune donnée structurée, pas de sitemap, Universal Analytics.
- **À retenir** : un établi valaisan sans présence numérique. **Le Valais est ouvert** pour un spécialiste qui publie du contenu, mais la distance limite l'intérêt pour les particuliers.

### 3.16 MNPro — Collombey (VS / Chablais) · le plus innovant

- **Héro (H1)** : « Donnons vie à vos murs. » ; sous-titre « Artisan peintre et plâtrier en Valais. »
- **CTA** : « Demander un devis gratuit », « Pas envie d'attendre ? Essayez l'estimation IA en 30 s ».
- **Dispositif phare** : **estimation par IA** : une photo et la surface donnent une fourchette en CHF (exemple affiché « 2 500 – 4 200 CHF »), avec une simulation avant/après. Formulaire de 10 champs (dont consentement, surface, photo, ville).
- **Promesses** : maîtrise fédérale, « Devis gratuit sous 48h », « Pas de sous-traitance » ; dans le blog : garantie écrite de « 5 ans minimum ».
- **Preuve sociale** : **5,0/5 sur 16 avis Google**, « 70+ chantiers depuis 2021 ».
- **Contenu** : blog de prix (cloison placo, cloisons sèches), 234 URL, `llms.txt` de 9,6 Ko, FAQ.
- **Technique** : PaintingContractor + diplôme (EducationalOccupationalCredential) + FAQPage. JS très léger (≈ 45 Ko) mais ≈ 3,5 Mo d'images.
- **Ton** : par endroits polémique et non sourcé (concurrent présenté à « 80% de risques de fissures »).
- **À retenir** : l'estimation IA est une **curiosité, pas un modèle** pour une cible de 45-70 ans (confiance, photos transmises à un tiers, nLPD). Les **articles de prix** sont en revanche le contenu le plus cité par les moteurs.

### 3.17 Réseaux de mise en relation et sites « mot-clé + ville »

| Acteur | Ce qu'il fait | Signes observés |
|---|---|---|
| **Helvétique Plaquiste** (helvetique-plaquiste.ch) | Placo, doublages, faux-plafonds, isolation phonique et thermique, combles, dans toute la Romandie | Mentions légales : « service de mise en relation », « n'est pas l'entreprise qui exécute l'intervention », « SA en cours de constitution », hébergement en France. **156 pages villes**, 15 pages services, 11 pages « problèmes », 10 pages « intentions », page tarifs (cloison 95-160 CHF/m², doublage 85-150, faux-plafond 100-175). Héro : « La plâtrerie sèche faite avec précision et propreté ». Pas de téléphone. Formulaire de 8 champs (e-mail optionnel) |
| **Réseau** *valais-peinture.ch* + *expert-isolation.ch* (le `llms.txt` du premier s'intitule « NLP – Peinture Valais ») | Peinture en Valais ; isolation phonique et thermique (pages Genève, Lausanne, Fribourg, Neuchâtel), subventions | **Même numéro (078 218 23 24)** et même adresse (Rue de Genève 100, 1004 Lausanne) ; « réseau de partenaires sélectionnés » ; aucune IDE affichée. Même formulaire long (13 champs dont canton, NPA, « parcours »). Héros : « Entreprise de peinture en Valais », « ISOLATION PHONIQUE GENÈVE ». Promesse « Diagnostic acoustique gratuit », « Calme et confort garantis » |
| *peintrelausanne.ch* (« Gaetano Peintre ») | Peinture à Lausanne | Formulaire **en étapes** (type de projet, puis tranche de surface, puis coordonnées), « Devis gratuit en 24h », prix « entre CHF 25 et CHF 45 par m² », note 5/5 sur 127 avis déclarée dans le code, aucune IDE |
| *vaud-peinture.ch* | Peinture et plâtrerie, Lausanne | Héro : « L'art de peindre. La finition d'exception. » ; « 5,0 sur Google · 6 avis » ; « assuré RC Pro » ; **balise Google Ads** ; aucune adresse ni IDE |
| *peinturesgeneve.ch* | Peinture, Genève | « Garantie écrite 5 ans », « Peintres certifiés AGCV » (**label introuvable** lors de nos recherches), « Devis dès CHF 200 intervention minimum », intérieur « dès CHF 35 / m² », extérieur « dès CHF 55 / m² », 45 communes |
| Renovero, Ofri, batmat, IDtravaux | Plateformes de devis nationales | Publient des **guides de prix** très repris (voir §4). Renovero : abonnements artisans de CHF 0 à 2'099 par an, « 65'000 appels d'offres annuel » |

**À retenir** : ces sites prennent les requêtes « problème » et « prix » (placo, isolation phonique) dans **tous** les cantons, avec un contenu générique. Leur faiblesse : **aucune preuve vérifiable** (pas de raison sociale, pas d'IDE, pas de chantier daté). Andy ne doit pas les copier (pages villes clonées) mais les contrer par la **vérifiabilité** : fiches projets datées par commune, IDE, adresse, références.

---

## 4. Benchmark des prix publics en Suisse romande

Prix relevés tels quels, **à ne pas reprendre comme prix d'Andy**. Ils servent à calibrer la FAQ (fourchettes à fournir par le client) et à qualifier les demandes. HT = hors TVA (8,1 %).

### 4.1 Tableau

| Poste | Fourchette publiée | Unité | Source (type, date) |
|---|---|---|---|
| **Peinture** murs, dispersion, 2 couches | 22 – 35 | CHF/m² HT | chiffr.ch (outil de devis pour artisans, mis à jour 25.09.2026) |
| Peinture plafonds, 2 couches | 26 – 40 | CHF/m² HT | chiffr.ch (25.09.2026) |
| Préparation courante / ratissage complet | 6 – 12 / 18 – 35 | CHF/m² HT | chiffr.ch (25.09.2026) |
| Peinture murs, support sain, tout compris | 25 – 50 | CHF/m² HT | chiffr.ch (25.09.2026) |
| Peinture intérieure (murs mats / plafonds) | 25 – 35 / 28 – 40 | CHF/m² | VLP Peinture, entreprise genevoise (31.08.2026) |
| Peinture intérieure | 25 – 45 | CHF/m², main-d'œuvre et fournitures | peintrelausanne.ch (site d'artisan sans IDE, consulté le 31.10.2026) |
| Peinture intérieure | dès 35 | CHF/m² | peinturesgeneve.ch (consulté le 31.10.2026) |
| Peinture intérieure | 40 – 80 | CHF/m² | valais-peinture.ch (réseau de mise en relation, non daté) |
| Peinture murs / plafonds (Suisse alémanique) | 16 – 19 / 19 – 21 | CHF/m², 2 couches | neho.ch (« Stand 2025 ») |
| Rafraîchissement d'un 3,5 pièces / remise en état complète | 6'250 – 8'200 / 8'600 – 12'100 | CHF HT | chiffr.ch (25.09.2026) |
| Rénovation peinture d'un 3 pièces (80-100 m²) / studio | 6'000 – 11'000 / 2'500 – 4'500 | CHF | VLP Peinture (31.08.2026) |
| **Cloison placo** (« cloison sèche ») | dès 95, courant 95 – 160 | CHF/m² | Helvétique Plaquiste (mise en relation, 28.07.2026) |
| Installer une cloison | 100 – 200 | CHF/m² ; projet bas 1'480, moyen 2'250, élevé 3'269 CHF | Ofri (plateforme, 27.11.2024, 106 prix) |
| Cloison sèche (projet) | 2'119 / 3'148 / 9'200 | CHF (bas / moyen / élevé) ; jointoiement 9 – 11 CHF/m² | Ofri (27.11.2024, 78 prix) |
| Cloison placo simple / isolée 40 mm / acoustique premium | 180 – 220 / 240 – 280 / 300 – 350 | CHF/m² HT, pose comprise, peinture en sus (20 – 50 CHF/m²) | MNPro, entreprise valaisanne (22.07.2026) |
| Cloison carreaux de plâtre 4-6 cm / 8-10 cm | 55 – 75 / 80 – 100 | CHF/m² | IDtravaux (plateforme, Gland, non daté) |
| **Doublage** | 50 – 90 | CHF/m² | IDtravaux (non daté) |
| Doublage mural | dès 85, courant 85 – 150 | CHF/m² | Helvétique Plaquiste (28.07.2026) |
| **Faux-plafond placo** | 75 – 105 (Fermacell 80 – 110) | CHF/m² | IDtravaux (non daté) |
| Faux-plafond placo BA13 / avec LED | 80 – 120 / 120 – 180 | CHF/m², pose comprise | Edelweiss Rénovation, entreprise genevoise (article 2026) |
| Faux-plafond | dès 100, courant 100 – 175 | CHF/m² | Helvétique Plaquiste (28.07.2026) |
| **Faux-plafond acoustique** | 90 – 150 | CHF/m² | Edelweiss Rénovation (2026) |
| Panneau acoustique PET / pose | dès 99 / dès 100 | CHF par panneau, HT | Solutions Acoustiques (consulté le 31.10.2026) |
| Isolant phonique haut de gamme (matériau) | 120.50 – 150 | CHF/m² | Ofri, « Isoler un mur » (mise à jour 31.07.2026) |
| **Taux horaire** peintre, plâtrier (régie) | 75 – 95 | CHF/h HT | chiffr.ch (04.09.2026) |
| Taux horaire plâtrier | 50 – 100 | CHF/h | IDtravaux (non daté) |
| Déplacement / masticage | 70 – 90 | CHF/h | Ofri (2024-2026) |
| Taux horaire artisans (tous corps) | 50 – 150 | CHF/h | neho.ch (25.11.2024) |
| Taux horaire peintres | 50 – 140 | CHF/h | Comparis (extrait de recherche ; page non consultable, erreur 403) |
| Intervention minimum | 200 | CHF | peinturesgeneve.ch |

### 4.2 Ce que les écarts nous disent

- **Peinture** : les sources sérieuses de 2026 convergent vers **25 à 45 CHF/m²** pour une peinture intérieure courante, préparation légère comprise. Les 16-21 CHF/m² de Suisse alémanique ne comprennent pas la préparation ; les 40-80 CHF/m² d'un réseau valaisan sont isolés.
- **Placo** : l'écart va **du simple au triple** (95 à 350 CHF/m²) parce que les sources ne comptent pas la même chose : ossature, isolant, double parement, joints, enduit prêt à peindre, portes, réservations électriques. **C'est exactement la confusion que la FAQ d'Andy peut lever.**
- **Acoustique** : aucun prix public pour une **isolation phonique d'appartement** (doublage désolidarisé, faux-plafond sur suspentes antivibratiles). Les prix trouvés concernent la correction acoustique (panneaux) ou des faux-plafonds « acoustiques » sans performance précisée.
- **Cloisons isothermes / isolation de plafond de cave ou garage** : aucun prix romand fiable trouvé (Ofri donne seulement des coûts de matériaux).

### 4.3 Recommandations pour la FAQ « combien ça coûte » et la qualification

1. **Publier des fourchettes fournies par le client**, pour 4 cas types (peinture d'un 3,5 pièces, cloison placo de 10 m², faux-plafond de 20 m², doublage phonique d'un mur mitoyen), avec **la liste de ce qui est compris et non compris**, la mention HT ou TTC, et « prix indicatifs, devis après visite ». Les repères ci-dessus servent au client pour se situer, pas à être copiés.
2. **Expliquer les 4 ou 5 facteurs qui font varier le prix** (état du support, hauteur, accès, performance acoustique visée, finitions). C'est ce que les IA reprennent et ce que les 45-70 ans attendent.
3. **Qualification sans friction** : ne pas demander de budget aux particuliers (champ mal vécu). Demander plutôt la **surface approximative** par tranches (« moins de 20 m² », « 20 à 50 m² », « plus de 50 m² », « je ne sais pas »), le **type de bien** et le **délai souhaité**. Pour les régies et architectes : lot ou code CFC, échéance, nombre de logements.
4. **Montant minimum d'intervention** : à décider avec le client (un concurrent affiche CHF 200). L'annoncer évite les demandes non rentables, surtout hors de Genève (frais de déplacement).

---

## 5. Ce qui convertit chez eux

Fréquences calculées sur les 39 sites d'entreprises. L'avis sur la pertinence pour les 45-70 ans s'appuie sur le programme (public hostile à l'exagéré et aux dark patterns) et sur les comportements observés : on cherche en ligne, puis on appelle.

| Dispositif | Observé chez | Fréquence | Pertinence 45-70 ans | Recommandation pour Andy |
|---|---|---|---|---|
| Téléphone cliquable dans l'en-tête | Presque tous | 34/39 | **Essentielle** | Oui : fixe 022 en premier (inspire plus confiance qu'un 079), horaires juste à côté. Ne pas limiter les heures d'appel (Wüthrich : 8 h-11 h et 14 h-16 h seulement) |
| Numéro gratuit 0800 | Thorens | 1 | Faible | Inutile : le numéro local rassure davantage |
| Formulaire court (3 à 8 champs) | Majorité | 32/39 | Élevée | Oui, 5 champs visibles au maximum |
| **E-mail facultatif ou absent** | ArdmuPro (pas d'e-mail), Madéco, Helvétique Plaquiste | 3 | **Élevée** (on préfère être rappelé) | **Oui** : téléphone obligatoire, e-mail facultatif |
| **Choix du mode de recontact** (appel, WhatsApp) | ArdmuPro | 1 | **Élevée** | **Oui**, avec un créneau de rappel préféré (matin, midi, soir) |
| Formulaire long à listes (13 champs, canton, NPA, « parcours ») | Réseau valais-peinture / expert-isolation | 2 sites | Faible (abandon) | Non |
| Formulaire en étapes avec tranches de surface | peintrelausanne.ch | 1 | Moyenne à élevée si 2 ou 3 étapes, barre de progression et retour possible | À tester pour les particuliers ; reprendre au minimum l'idée des **tranches de surface** |
| Photos facultatives | ArdmuPro (jusqu'à 8), F-R, MNPro, Peinture Isolation | 4/39 | Moyenne : utile, mais l'envoi depuis un ordinateur peut bloquer | Oui, **facultatif**, avec l'alternative « envoyez-les par WhatsApp ou e-mail après notre appel » |
| WhatsApp | 16/39 | 16/39 | Moyenne : canal apprécié, mais ne remplace pas le téléphone | Oui, en canal secondaire, avec la mention nLPD (service tiers) |
| Estimation instantanée par IA (photo + surface → fourchette) | MNPro | 1 | **Faible** (confiance, données envoyées à un tiers) | Non pour l'instant |
| Grilles de prix, pages tarifs, articles « prix 2026 » | VLP, Edelweiss, MNPro, peinturesgeneve.ch, Helvétique Plaquiste | ≈ 6 | **Élevée** (transparence) et forte visibilité dans les IA | **Oui** : une page « Prix indicatifs » avec cas types (voir §4.3) |
| Promesse « devis en 24 h / 48 h » | 13/39 + 5 réseaux | 18/46 | Ne différencie plus ; risque si non tenue | Promettre **un délai précis et tenable** (p. ex. rappel le jour ouvrable suivant, visite sous X jours), **à fixer avec le client** |
| Visite technique gratuite | Edelweiss, ArdmuPro, MNPro | Fréquent | Élevée | Oui si c'est la pratique réelle (à valider ; la limiter à une zone si besoin) |
| Garanties écrites (« 5 ans », « parfait achèvement et décennale ») | peinturesgeneve.ch, MNPro, ArdmuPro, Madéco | 8/39 parlent de « garantie » | Élevée (seniors, régies) | **Oui, mais juste en droit suisse** : depuis le 1.1.2026, délai d'avis de 60 jours pour les défauts apparents et cachés (non réductible par contrat) et droit à la réfection qui ne peut plus être exclu ; prescription de 5 ans inchangée ; SIA 118 si elle est convenue. Pas de « décennale ». Formulation finale à faire relire |
| Avis Google affichés avec le nombre | Sousa, Colosimo, MNPro, Madéco, Edelweiss (+ Solutions Acoustiques : note sans nombre) | 6/39 | **Très élevée** | Oui dès qu'ils existent (bloc masqué tant qu'il est vide). Ne pas mettre de note agrégée dans le balisage du site |
| Logos ou noms de clients | Logos : Solutions Acoustiques, Wüthrich. Noms : Colosimo (ONU, TPG, MSC), Rudi SA (maîtres d'ouvrage), DSD SA (études de cas) | 5 | Élevée | Oui, selon les statuts juridiques du programme (noms typographiques pour les armoiries publiques) |
| Diplômes et affiliations (maîtrise ou brevet fédéral, CFC, entreprise formatrice, GVEPP, FREPP, AFMPP/AFEPP, ISO 9001) | Wüthrich, Colosimo, MNPro, Sousa, Savary, Gypsa, F-R Plâtrerie | 7/39 | Élevée (gage de sérieux) | Oui **si réels** : à fournir par le client |
| « Équipe salariée, pas de sous-traitance » | ArdmuPro, Madéco, MNPro, Vernay | 4 | Élevée | Oui si c'est vrai (à valider) |
| Page ou offre « régies et architectes » | ArdmuPro, Edelweiss, Léman Peinture (champ « régie » dans le formulaire) | 3 | Très élevée pour le B2B | **Oui** (voir §6) |
| Showroom, prise de rendez-vous | Solutions Acoustiques (Daillens) | 1 | Moyenne | Pas de showroom : proposer « rendez-vous sur place » |
| Démonstration audio ou vidéo avant/après | Solutions Acoustiques | 1 | Moyenne à élevée pour l'acoustique | Plus tard, avec une **mesure réelle** avant/après sur un chantier |
| Newsletter | Wüthrich | 1 | Faible | Non |
| Chat en direct | Aucun observé de façon fiable | 0 | Faible | Non |
| Compte à rebours, pop-up, fausse urgence | Aucun observé | 0 | Négative | Rester ainsi (programme, LCD) |

**Pièges observés à ne pas reproduire** : compteurs animés qui affichent « 0+ » sans JavaScript (ArdmuPro), texte « Lorem ipsum » en ligne (Thorens), zone d'intervention différente d'une page à l'autre (F-R Plâtrerie), notes de 5/5 déclarées dans le code sans source (RA Peinture, peintrelausanne.ch), labels introuvables (« AGCV »), titres de section « Conclusion » ou « Liens internes vers nos autres pages » écrits pour les robots (Hypp SA), pages d'accueil de 2 à 7 Mo d'images (DSD, Colosimo, MNPro, Savary).

---

## 6. Écarts et opportunités

### 6.1 Ce que personne ne fait bien

1. **Prouver par des chantiers datés et localisés.** Seuls DSD SA (Genève) et Rudi SA (Vaud, fiches avec maître d'ouvrage, entreprise totale et lots) publient de vraies fiches projets ; Colosimo nomme l'ONU, les TPG et MSC sans détail. Les logos de Solutions Acoustiques et de Wüthrich ne sont pas commentés. Les réseaux n'ont aucune preuve. **Personne ne publie de fiche sur un chantier acoustique ou placo dans un bâtiment public**, avec le problème, la solution et l'année.
2. **Expliquer l'isolation phonique honnêtement.** Personne ne distingue clairement **isolation** (bruit qui traverse) et **correction** (écho dans la pièce), ni ne dit quand un faux-plafond ne suffit pas (bruit de pas du voisin : il faut traiter le sol du dessus). La SIA 181 n'est citée nulle part en langage simple. Les requêtes « bruit du voisin du dessus » renvoient à des forums français.
3. **Parler aux régies, architectes et communes avec les bons documents.** Seuls ArdmuPro et Edelweiss ont une page dédiée, sans référence publique, sans codes CFC, sans attestations téléchargeables (RC, assurances sociales, CCT-SOR), sans dossier de références.
4. **Être transparent sur l'identité.** Plusieurs sites qui captent des demandes n'ont ni raison sociale ni IDE. Andy peut afficher sans effort : registre du commerce depuis 2007, IDE CHE-113.706.162, adresse à Carouge, « nous exécutons nous-mêmes » (à valider).
5. **Dire ce que comprend un prix.** Les fourchettes publiques varient du simple au triple faute de définition. Aucune entreprise ne publie de cas types expliqués.
6. **Formuler les garanties correctement.** Termes du droit français, « garantie 5 ans » sans contenu, labels inconnus. Les nouvelles règles du CO sur les défauts de construction (en vigueur depuis le 1.1.2026 : avis dans les 60 jours, droit à la réfection non excluable) ne sont expliquées par aucun concurrent, alors que les régies et les architectes y sont attentifs.
7. **Traiter le besoin « cloison isotherme » sous son vrai nom.** Seuls Edelweiss (page cave et garage) et Isoleco (spécialiste de l'insufflation) en parlent. Personne ne relie ce besoin aux subventions possibles avec prudence, ni ne montre de chantier.
8. **Faire un site rapide et sobre.** La majorité des sites sont lourds (constructeurs Divi, Elementor, Wix, Squarespace ; 2 à 7 Mo d'images). Le site statique léger prévu au programme est en soi un avantage.
9. **Rejoindre l'association cantonale.** Andy n'apparaît pas dans la liste des 87 membres de Gypserie Peinture Genève (GPG, membre de la FREPP), alors que ses concurrents genevois de taille comparable y sont. L'adhésion apporte une mention vérifiable, un lien et un argument pour les marchés publics *(éligibilité et coût à vérifier par le client)*.

### 6.2 Matrice d'opportunités

Difficulté et valeur de 1 (faible) à 5 (forte). **Estimations à valider** avec le Keyword Planner (volumes) puis la Search Console (positions réelles). Difficulté = concurrence observée sur les requêtes du §2.1. Valeur = taille probable d'un chantier × probabilité de conversion pour Andy × proximité de Carouge.

| # | Mot-clé ou thème | Canton(s) | Difficulté | Valeur | Priorité | Format recommandé |
|---|---|---|---|---|---|---|
| 1 | « Andy Construct », avis, NAP | — | 1 | 5 | **P0** | Fiche Google, annuaires, campagne d'avis (déjà au plan de septembre) |
| 2 | Plafond acoustique / correction acoustique de salle, école, salle communale | Toute la Romandie | 2 | 5 | **P1** | Page B2B + fiches des salles communales réalisées ; un seul concurrent spécialisé |
| 3 | Faux-plafond (placo, acoustique) Genève | GE | 4 | 5 | **P1** | Page service + fiches projets + prix indicatifs |
| 4 | Cloison placo, cloison de séparation (bureaux, appartement) Genève | GE | 3 | 4 | **P1** | Page service, cas type chiffré |
| 5 | Isolation phonique d'appartement, bruit des voisins | GE, VD | 3 | 4 | **P1** | Guide suisse (SIA 181, PPE et régie, ce qui marche ou non) + page service |
| 6 | Plâtrier, plâtrerie peinture Nyon, Coppet, Rolle (La Côte) | VD-Ouest | 3 | 4 | **P1** | Page régionale **adossée aux références** de Coppet, Nyon et Chavannes-de-Bogis |
| 7 | Prix peinture m², prix cloison placo m², prix faux-plafond | Romandie | 3 | 3 | **P1** | Page « Prix indicatifs » (GEO, qualification) |
| 8 | Plâtrier, plâtrerie peinture Genève | GE | 4 | 4 | P2 | Accueil + pages services ; marché fragmenté sans leader |
| 9 | Remise en état et peinture d'appartement pour régies | GE | 4 | 5 | P2 | Prospection directe d'abord ; page régies ensuite |
| 10 | Isolation plafond de cave ou de garage, cloison isolante (= cloisons isothermes) | GE, VD | 2 | 3 | P2 | Renommer la section ; cas type ; subventions avec prudence |
| 11 | Isolation phonique Lausanne, faux-plafond Lausanne | VD | 3 à 4 | 3 | P2 | Seulement avec des chantiers lausannois à montrer |
| 12 | Isolation phonique, plafond acoustique Fribourg, Neuchâtel, Sion | FR, NE, VS | 2 | 3 | P2 | Page régionale **si chantier réel** ; B2B en priorité |
| 13 | Faux-plafond, cloison coupe-feu (AEAI) | Romandie | 2 | 4 | P2 | Uniquement si Andy pose des systèmes certifiés (**à valider**) |
| 14 | Entreprise de peinture Genève, peintre Genève (particuliers) | GE | 5 | 3 | P3 | Annonces ciblées (quartiers, mots-clés négatifs), pas une bataille SEO |
| 15 | Cloison placo Fribourg, Neuchâtel, Sion | FR, NE, VS | 2 | 2 | P3 | Rien de dédié au départ |
| 16 | Plâtrier peintre Delémont, La Chaux-de-Fonds, Bulle | JU, NE, FR | 2 | 1 | P3 | Pas de page : de 1 h 15 (Bulle) à plus de 2 h (Delémont) de route depuis Carouge *(estimation)*, un petit chantier de particulier y est rarement rentable |
| 17 | « Cloison isotherme » | — | 1 | 1 | — | Synonyme dans le texte uniquement (intention « chambre froide ») |

### 6.3 Angle différenciant recommandé

**« Le second œuvre intérieur des bâtiments exigeants, rendu accessible. »**
Andy est la seule entreprise de l'échantillon qui peut montrer, **avec des noms**, qu'elle travaille pour des institutions (Ville de Genève, Conservatoire, HEAD, OMC, salles communales) **sur le placo et l'acoustique**, tout en restant spécialisée sur l'intérieur. Les grands (Belloni, Buschini, Dino) sont généralistes et invisibles ; les petits visibles ont peu de références (Colosimo, en peinture seulement) ; les réseaux n'exécutent pas.

Conséquence géographique, à valider avec le client : **particuliers à Genève et sur La Côte** (zone de proximité) ; **régies, architectes, communes et entreprises dans toute la Suisse romande**, en particulier pour l'acoustique et le placo, où la valeur d'un chantier justifie le déplacement.

---

## 7. Positionnement et messages recommandés

### 7.1 Proposition de valeur

> Andy Construct pose le placo, traite l'acoustique et assure la peinture intérieure avec la rigueur exigée sur les bâtiments publics genevois, que le client soit une commune, une régie ou un particulier. Entreprise inscrite au registre du commerce depuis 2007, basée à Carouge, active dans toute la Suisse romande.

### 7.2 Trois variantes de titre de héro (10 mots au maximum)

| Variante | Titre | Mots | Angle | Condition |
|---|---|---|---|---|
| A | « Placo, peinture, acoustique : la rigueur des chantiers publics. » | 8 | Preuve institutionnelle | Sous-titre avec 3 ou 4 références nommées et datées |
| B | « Des pièces plus calmes, des finitions nettes. » | 7 | Bénéfice concret (acoustique et finition) | Adapté aux particuliers ; le sous-titre porte la preuve |
| C | « Depuis 2007, un seul interlocuteur du placo à la peinture. » | 10 | Simplicité, ancienneté vérifiable | Vrai seulement si les 4 métiers sont exécutés par l'équipe (**à valider**) |

**Recommandation : A**, avec un sous-titre de preuve, par exemple : « Entreprise de Carouge, inscrite au registre du commerce depuis 2007. La Ville de Genève, le Conservatoire et la HEAD nous ont confié leurs travaux. » *(formulation et années à valider ; noms en texte, sans armoiries)*. Le H1 actuel de la maquette (« Placo, peinture et isolation en Suisse romande ») est descriptif et bon pour le référencement : il peut rester en surtitre ou dans la balise `title` si la variante A devient le titre affiché.

### 7.3 Piliers de message et preuves

| Pilier | Message | Preuves à montrer | Statut |
|---|---|---|---|
| 1. Éprouvé sur des bâtiments exigeants | « Les institutions nous confient leurs salles, leurs bureaux et leurs plafonds. » | 18 références, dont publiques (Ville de Genève, Conservatoire, HEAD, OMC, salles communales de Collonge-Bellerive et Plan-les-Ouates) ; fiches projets datées par commune | Années et accords à obtenir pour les marques privées |
| 2. Spécialiste de l'intérieur, pas généraliste | « Quatre métiers qui se suivent sur le même chantier : ossature, plaques, isolation, peinture. » | Photos d'étapes de chantier ; équipe ; méthode | Équipe salariée ou sous-traitance : **à valider** |
| 3. L'acoustique expliquée simplement | « Nous vous disons ce qui réduira vraiment le bruit, et ce qui ne le réduira pas. » | Guide isolation et correction ; SIA 181 en mots simples ; cas réel avec mesure si possible | Mesures avant/après : à demander au client |
| 4. Transparence | « Une entreprise identifiable, des prix indicatifs, des garanties expliquées. » | IDE, adresse, registre depuis 2007 ; page « Prix indicatifs » ; garanties selon le CO révisé (2026) et la SIA 118 si convenue ; délai de rappel tenu | Fourchettes de prix et délai de rappel : **à fournir par le client** |

### 7.4 Objections à traiter

| Objection probable | Réponse à apporter | Où |
|---|---|---|
| « Vous travaillez pour des institutions, vous êtes trop chers ou trop gros pour moi. » | Chantiers de particuliers montrés aussi ; prix indicatifs ; montant minimum annoncé | Accueil, FAQ, réalisations |
| « Vous êtes à Carouge, venez-vous à Lausanne, Fribourg ou Sion ? » | Zone claire : particuliers à Genève et sur La Côte ; professionnels dans toute la Romandie ; frais de déplacement annoncés | Page contact, FAQ, carte |
| « Est-ce que ça marchera vraiment contre le bruit ? » | Distinguer bruit aérien et bruit de pas ; visite avant devis ; pas de promesse chiffrée sans mesure | Page acoustique, FAQ |
| « Je suis locataire ou en PPE, ai-je le droit ? » | Accord du bailleur ou de la copropriété ; Andy peut fournir un descriptif pour la régie | FAQ |
| « Combien ça coûte ? » | Fourchettes par cas type et ce qu'elles comprennent | Page prix, FAQ |
| « Quand pouvez-vous venir, combien de temps ça dure ? » | Délai de rappel et de visite tenable ; durées types par chantier | FAQ, formulaire |
| « Poussière et bruit pendant les travaux ? » | Protection, nettoyage, travail en site occupé (déjà fait pour des institutions) | Page méthode |
| « Et s'il y a un défaut ? » | Garanties légales suisses expliquées sans jargon ; interlocuteur unique | FAQ |
| « Sous-traitez-vous ? » | Réponse franche (**à valider**) | FAQ |
| « Y a-t-il des subventions ? » | Seulement pour certaines isolations thermiques, demande avant travaux, renvoi vers les programmes cantonaux ; l'acoustique seule n'est en général pas subventionnée | FAQ |

### 7.5 Mots à éviter et mots à préférer

| À éviter | Pourquoi | À préférer |
|---|---|---|
| « L'art de peindre », « finition d'exception », « excellence », « premium », « haut de gamme » | Ton publicitaire, déjà usé par les concurrents (vaud-peinture.ch, VLP, F-R) ; rejeté par la cible | « finition soignée », « travail propre », des faits (lieu, année, surface) |
| « Passion », « sans stress », « donnons vie à vos murs » | Formules creuses | Ce que le client obtient : « une pièce plus calme », « des murs prêts à vivre » |
| « Leader », « n° 1 », « meilleur », « expert reconnu » | Invérifiable, risque LCD | « Depuis 2007 », « pour la Ville de Genève depuis 20XX » |
| « Garantie décennale », « parfait achèvement » | Notions du droit français, fausses en Suisse | « Garanties selon le Code des obligations (et la norme SIA 118 si elle est convenue) » |
| « Certifié », « agréé », « label » sans document | Labels introuvables chez des concurrents ; risque juridique | Diplômes et affiliations réels seulement |
| « Devis en 24 h » si ce n'est pas tenu | Promesse banale et risquée | Un délai précis et tenu, fixé avec le client |
| « Isotherme » seul dans les titres | Intention « chambre froide » | « Cloison isolante », « isolation de plafond de cave ou de garage », puis « isotherme » en synonyme |
| « Plaquiste » comme terme principal | Mot surtout français, utilisé par les réseaux | « Plâtrier », « placo », « plaques de plâtre » ; « gypserie » (usage genevois et valaisan) en synonyme |
| « Isolation acoustique » seul | Les particuliers cherchent « isolation phonique », « bruit » | Employer les deux ; réserver « correction acoustique » à l'écho des salles |
| Anglicismes, sigles non expliqués (GEO, CTA, ITI) | Public de 45-70 ans | Mots courants, sigles expliqués à la première mention |

### 7.6 Points à faire valider par le client

1. Les 4 métiers sont-ils exécutés par l'équipe d'Andy ? Y a-t-il de la sous-traitance ?
2. Diplômes (CFC, brevet, maîtrise fédérale), statut d'entreprise formatrice, affiliations (GPG, FREPP, CCT-SOR) : lesquels sont réels ?
3. Fourchettes de prix par cas type, montant minimum, frais de déplacement hors Genève.
4. Délai de rappel et de visite réellement tenables.
5. Années et accords de citation des 18 références ; chantiers réalisés hors de Genève (Lausanne, Fribourg, Valais…) pour adosser la promesse « toute la Suisse romande ».
6. Définition exacte des « cloisons isothermes » (déjà posée dans `docs/contenus-a-valider.md`) et chantiers montrables.
7. Systèmes coupe-feu certifiés posés (avant toute mention AEAI).
8. Intérêt et éligibilité d'une adhésion à Gypserie Peinture Genève.

---

## 8. Sources

Toutes consultées le 31.10.2026, sauf mention contraire.

**Associations et cadre juridique**
- FREPP, accueil : https://frepp.ch/ ; associations membres : https://frepp.ch/membresfrepp/
- Gypserie Peinture Genève (GPG), liste des membres (87 entreprises) : https://gpg.ch/lassociation/membres.html
- AFEPP (Fribourg), entreprises membres (71 fiches) : https://afepp.ch/entreprises/ ; fiche P-Y Savary SA : https://afepp.ch/entreprises/savary-pierre-yves-sa/
- ASEPP / SMGV, annuaire des entreprises : https://www.smgv.ch/fr/annuaire-des-entreprises
- Campagne « Les vrais pros » (apprentissage) : https://www.lesvraispros.ch/
- ASEPP, changements légaux au 1.1.2026 : https://www.smgv.ch/download-center/fr/02_services/recht/f_gesetzesaenderungen-per-2026.pdf
- Confédération, entrée en vigueur des nouvelles règles sur les défauts de construction : https://www.admin.ch/fr/newnsb/VsBnhpbj-jkYJm1JmZZA8
- Annuaire des fournisseurs des régies de la Riviera : https://regiesriviera.ch/fournisseurs/peinture-riviera-vaudoise

**Prix**
- chiffr.ch, prix peinture au m² (mis à jour 25.09.2026) : https://chiffr.ch/prix/peinture-m2-suisse
- chiffr.ch, tarif horaire artisan (mis à jour 04.09.2026) : https://chiffr.ch/prix/tarif-horaire-artisan-suisse
- VLP Peinture, tarifs (mis à jour 31.08.2026) : https://vlppeinture.ch/tarifs-peinture-geneve
- valais-peinture.ch, budget peinture intérieure : https://valais-peinture.ch/budget-travaux-peinture-interieure/
- neho.ch, coûts de peinture (« Stand 2025 ») : https://neho.ch/de/blog/kosten-haus-steichen
- neho.ch, prix de rénovation au m² (25.11.2024) : https://neho.ch/fr/blog/prix-renovation-m2-maison
- IDtravaux, prix plâtrier : https://idtravaux.ch/devis-travaux-platrier/
- Helvétique Plaquiste, prix (28.07.2026) : https://helvetique-plaquiste.ch/blog/prix-plaquiste-suisse-romande ; mentions légales : https://helvetique-plaquiste.ch/mentions-legales
- MNPro, prix cloison placo (22.07.2026) : https://www.mnpro.ch/blog/prix-cloison-placo-platre-suisse-2026/
- Ofri, cloison sèche : https://www.ofri.ch/fr/couts/cloison-seche
- Ofri, installer une cloison : https://www.ofri.ch/fr/couts/installer-une-cloison
- Ofri, isoler un mur : https://www.ofri.ch/fr/couts/isoler-un-mur
- Edelweiss Rénovation, faux-plafonds 2026 : https://edelweiss-renovation.ch/faux-plafonds-a-geneve-tendances-2026-prix-et-conseils-dinstallation/
- Solutions Acoustiques, panneaux : https://solutions-acoustiques.ch/panneaux-acoustiques/
- Comparis, peintres (page non consultable, erreur 403 ; chiffre repris d'un extrait de recherche) : https://www.comparis.ch/handwerker/maler/basel
- Renovero, abonnements artisans : https://www.renovero.ch/fr/pour-les-artisans

**Concurrents analysés (sites)**
- Genève : https://www.dsd-sa.ch/ · https://edelweiss-renovation.ch/ · https://ardmupro.ch/ (et /devis) · https://www.dinopeinture.ch/ · https://www.belloni-sa.ch/ · https://www.lemanpeinture-ge.ch/ · https://ms-contractor.ch/ · https://entreprise-mssa.ch/ · https://colosimo.ch/ · https://vlppeinture.ch/ · https://peinturesgeneve.ch/ · https://isoltechsarl.com/
- Vaud : https://www.wuthrichsa.ch/ · https://www.rudi-sa.ch/ · https://fr-platreriepeinture.ch/ · https://www.lausanne-peintre.ch/ · https://www.bskmontage.ch/ · https://sousa-peinture.ch/ · https://toni-peinture.ch/ · https://www.kurtalani.ch/ · https://www.thorens-peinture-vevey.ch/ · https://www.partenaires-constructions.ch/ · https://solutions-acoustiques.ch/ · https://www.lambda-isolation.ch/ · https://leivarenovation.ch/ · https://www.peinture-isolation.ch/ · https://www.vernay-peinture.ch/ · https://www.evasionpeinture.ch/ · https://alicpeinture.ch/ · https://solarconstruct.ch/ · https://www.becherraz.ch/ (hors ligne)
- Fribourg : https://madeco-peinture.ch/ · https://savarypeinture.ch/ · https://mas-peinture.ch/
- Neuchâtel : https://www.buschini.ch/ · https://rapeinture.ch/ · https://www.les-couleurs-infinies.ch/ · https://www.sdr-platrerie-peinture.ch/ · https://www.insulae.ch/immocolor/
- Valais : https://www.gypsa.ch/fr/ · https://hypp.ch/ · https://www.mnpro.ch/ · https://peintre-valais.ch/
- Jura : https://www.martiarcjura.ch/fr/compétences/peinture-et-plâtrerie · https://www.bichsel-peinture.ch/ (injoignable)
- Pan-romands et réseaux : https://www.orllati.ch/ · https://helvetique-plaquiste.ch/ · https://valais-peinture.ch/ · https://expert-isolation.ch/isolation-phonique-geneve/ · https://peintrelausanne.ch/ · https://vaud-peinture.ch/

**Requêtes (outil de recherche web, 31.10.2026)** : « plâtrier peintre Lausanne » ; « entreprise peinture Fribourg plâtrerie » ; « plâtrerie peinture Neuchâtel / La Chaux-de-Fonds » ; « plâtrier peintre Sion Valais » ; « gypserie peinture Sion Martigny » ; « plâtrier peintre Nyon La Côte » ; « entreprise peinture plâtrerie Morges » ; « plâtrier peintre Vevey Montreux » ; « plâtrerie peinture Yverdon-les-Bains » ; « plâtrerie peinture Delémont Jura » ; « entreprise plâtrerie peinture Fribourg Bulle Gruyère » ; « plâtrier Genève » ; « entreprise peinture Genève appartement devis » ; « entreprise plâtrerie peinture Genève régies architectes » ; « pose placo Genève cloison » ; « faux plafond placo Lausanne » ; « cloison placo Fribourg Neuchâtel Sion » ; « isolation phonique appartement Genève » ; « isolation acoustique Lausanne cloison phonique » ; « isolation phonique Fribourg Neuchâtel » ; « isolation phonique Valais Sion » ; « cloison isotherme » ; « isolation plafond cave garage Genève Vaud » ; « bruit voisin du dessus faux plafond acoustique Suisse » ; « plafond acoustique salle communale école » ; « prix peinture m² Suisse romande » ; « prix cloison placo Suisse » ; « Andy Construct Carouge ».

**Indices publicitaires** (code source et conteneurs Google Tag Manager publics) : balise AW-18226059887 sur https://vaud-peinture.ch/ ; balise AW-11334218998 dans le conteneur GTM-MJZ86DSW de https://solutions-acoustiques.ch/ ; pixel Meta sur https://leivarenovation.ch/ ; pixel TikTok sur https://www.partenaires-constructions.ch/.
