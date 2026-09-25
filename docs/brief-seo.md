# Brief SEO / GEO pour le développement du site Andy Construct

**Destinataire :** développeur frontend
**Date :** 25 septembre 2026
**Pages concernées :** `index.html`, `prestations.html`, `realisations.html`, `contact.html`, `mentions-legales.html`
**Document lié :** `docs/analyse-marche.md` (le « pourquoi » ; ce brief-ci est le « quoi »)

---

## 0. À lire avant de coder

1. **Informations à faire valider par le client (bloquant pour la production).** Le registre du commerce (Zefix, FOSC du 02.05.2023) indique :
   - raison sociale : **« Andy Construct, Chanton & Cie »**, **société en nom collectif** (et non « Sàrl ») ;
   - siège : **Route des Acacias 48, 1227 Carouge GE** ; l'adresse Avenue de Bel-Air 57, 1225 Chêne-Bourg n'est plus qu'une « autre adresse » ;
   - inscription depuis **2007** ;
   - local.ch et search.ch affichent aussi Carouge.

   **Décision du chef de projet (après vérification Moneyhouse/Zefix) : la maquette utilise le siège de Carouge, « depuis 2007 » et « société en nom collectif ».** Les exemples plus bas qui citent encore Chêne-Bourg sont à lire avec l'adresse de Carouge. **Tout ce qui est marqué `[À VALIDER]` doit être confirmé avant la mise en production.** Toutes les coordonnées sont centralisées au §1 : un seul endroit à modifier.
2. **Préproduction.** La version de test hébergée sur `harbor-digital.fr/res/...` doit être **non indexable**, avec `<meta name="robots" content="noindex, nofollow">` sur chaque page, ou l'en-tête HTTP `X-Robots-Tag: noindex` si possible. **Retirer ce noindex en production** (point de la recette, §10). Les canonical pointent toujours vers `https://www.andyconstruct.ch/...`.
3. **Hôte unique en production :** `https://www.andyconstruct.ch/`, avec le `www` (c'est l'hôte utilisé par l'ancien site et par les annuaires). Redirection 301 de `andyconstruct.ch` et de `http://` vers `https://www.`.
4. **Références clients.** Les noms figurent déjà publiquement sur l'ancien site. Il faut toutefois **l'accord du client** pour afficher des **logos** de marques privées (Piaget, De Grisogono, UBS, etc.). En attendant, afficher les noms en texte. Dater chaque référence. Écrire « Bank Sarasin (aujourd'hui J. Safra Sarasin) » si la date du chantier est antérieure à 2013.
5. **Ton du contenu.** Sobre, factuel et rassurant. La cible a 45-70 ans (régies, architectes, maîtres d'ouvrage, propriétaires) et n'aime pas l'extravagant. Pas de superlatifs (« leader », « n°1 »), pas de chiffres non vérifiés.

---

## 1. Bloc NAP de référence (à copier tel quel partout)

Le NAP (Name, Address, Phone) doit être **strictement identique** dans le pied de page, la page contact, les mentions légales, le JSON-LD, le `llms.txt`, la fiche Google et les annuaires.

```text
Andy Construct
Route des Acacias 48            [Décision chef de projet : siège au registre depuis 05.2023, à confirmer]
1227 Carouge (Genève)           [ancienne adresse : Av. de Bel-Air 57, 1225 Chêne-Bourg]
Tél. +41 22 771 20 15
Mobile +41 78 631 14 34
andy.construct@bluewin.ch       [À VALIDER : adresse sur le domaine recommandée, p. ex. contact@andyconstruct.ch]
Du lundi au vendredi, 7 h 00 – 18 h 00   [À VALIDER : horaires relevés sur local.ch]
```

- **Format des numéros :** toujours `+41 22 771 20 15` et `+41 78 631 14 34` (affichage). Liens : `href="tel:+41227712015"` et `href="tel:+41786311434"`.
- **Raison sociale légale** (mentions légales uniquement) : `Andy Construct, Chanton & Cie`, société en nom collectif, IDE CHE-113.706.162 `[À VALIDER]`.
- **Balisage :** dans le pied de page, entourer le NAP d'une balise `<address>`.

---

## 2. Mots-clés par page et intention de recherche

Il n'existe pas encore de données de volume fiables pour Genève : la priorité ci-dessous est qualitative. **À recaler 8 semaines après la mise en ligne**, avec la Search Console (requêtes réelles) et le Google Keyword Planner. Écrire naturellement, avec les deux graphies (« faux-plafond » et « faux plafond »), sans bourrage.

**Intentions :**
- **T** = transactionnelle (je veux un prestataire, un devis) ;
- **C** = commerciale (je compare, je me renseigne sur un prestataire) ;
- **I** = informationnelle (je veux comprendre) ;
- **N** = navigationnelle (je cherche l'entreprise).

| Page | Mots-clés principaux | Mots-clés secondaires | Questions / longue traîne | Intention dominante |
|---|---|---|---|---|
| `index.html` | faux-plafond Genève ; entreprise faux-plafonds Genève | cloisons Genève ; plâtrerie peinture Genève ; isolation phonique Genève ; faux-plafond Chêne-Bourg / Trois-Chêne ; faux-plafond Nyon / Coppet ; Andy Construct | « quelle entreprise pour poser un faux-plafond à Genève » ; « entreprise plafonds et cloisons Genève avis » | T + C (+ N sur la marque) |
| `prestations.html` | plafond tendu Genève ; plafond acoustique Genève ; cloison placoplâtre Genève | plafond tissu tendu ; plafond phonique ; faux-plafond placoplâtre ; plafond fibre minérale ; plafond fibre de bois ; plafond métallique bureaux ; cloison mobile aluminium / cloison amovible Genève ; isolation phonique plafond ; isolation thermique intérieure ; cadre acoustique ; chape flottante ; plafond coupe-feu ; trappe de visite ; caisson lumineux ; puits de lumière | « différence plafond tendu et placo » ; « plafond tendu à froid c'est quoi » ; « réduire le bruit des voisins du dessus » ; « à quoi sert une chape flottante » | C + I |
| `realisations.html` | références faux-plafonds Genève ; réalisations plafond acoustique | plafond acoustique salle communale ; plafond acoustique salle de musique ; faux-plafond bureaux Genève ; avant après faux-plafond ; entreprise plafonds pour architectes / régies | « exemple plafond acoustique salle polyvalente » | C (preuve, B2B) |
| `contact.html` | devis faux-plafond Genève ; Andy Construct contact | Andy Construct téléphone / adresse ; plâtrier Chêne-Bourg `[ou Carouge selon l'adresse validée]` | « Andy Construct numéro » | T + N |
| `mentions-legales.html` | (aucune cible) | Andy Construct, Chanton & Cie ; IDE | – | N (identité, confiance) |

---

## 3. Page par page : title, meta description, H1, structure H2

Longueurs vérifiées : title ≤ 60 caractères, meta description ≤ 155 caractères (espaces compris).

### 3.1 `index.html` (accueil)

- **`<title>`** : `Faux-plafonds et cloisons à Genève | Andy Construct` (51 car.)
- **Meta description** : `Faux-plafonds, cloisons, isolation phonique et peinture à Genève et dans l'ouest vaudois. Particuliers, régies, architectes. Tél. +41 22 771 20 15.` (147 car.)
- **H1** : `Faux-plafonds, cloisons et isolation à Genève`
- **Accroche sous le H1** (paragraphe, pas un titre) : « Plafonds · Cloisons · Peinture. Pour les particuliers, les régies, les architectes et les collectivités, de Genève à Nyon. »
- **Paragraphe d'identité** (important pour le GEO, à placer haut dans la page, en texte visible) :
  > Andy Construct est une entreprise genevoise spécialisée dans la pose de faux-plafonds (tendus, acoustiques, en plaques de plâtre, en fibre ou métalliques), de cloisons légères et mobiles, d'isolation thermique et phonique, ainsi que dans la peinture intérieure. Inscrite au registre du commerce depuis 2007 `[À VALIDER]`, elle intervient dans tout le canton de Genève et dans l'ouest vaudois pour des particuliers, des régies, des architectes, des entreprises et des collectivités publiques.
- **Structure H2 :**
  1. `Nos prestations` : 4 cartes (Plafonds / Cloisons / Isolation et acoustique / Peinture), chacune avec 2 phrases et un lien vers l'ancre de `prestations.html`.
  2. `Ils nous ont fait confiance` : 6 à 8 noms de référence en texte (logos seulement avec accord), 3 projets phares en vignette, lien vers `realisations.html`.
  3. `Pourquoi choisir Andy Construct` : 3 à 4 arguments **vérifiables** (ancienneté, spécialisation plafonds et cloisons, références publiques, zone locale). Ne rien affirmer que le client n'a pas confirmé (taille de l'équipe, garanties, délais).
  4. `Zone d'intervention` : une phrase + la liste courte des communes (§5).
  5. `Questions fréquentes` : les 10 Q/R du §4, en HTML visible (`<details>`/`<summary>` accepté, réponses présentes dans le DOM).
  6. `Demander un devis` : téléphone cliquable en grand, horaires, bouton vers `contact.html`.
- **Volume de texte visé :** 500 à 800 mots hors FAQ.

### 3.2 `prestations.html`

- **`<title>`** : `Plafond tendu, acoustique, cloison à Genève | Andy Construct` (60 car.)
- **Meta description** : `Plafonds tendus et acoustiques, placoplâtre, fibre, métal ; cloisons légères et mobiles ; isolation, chape flottante, protection incendie. Genève et Vaud.` (154 car.)
- **H1** : `Nos prestations : plafonds, cloisons, isolation et peinture`
- **Structure H2 / H3** (les ancres `id` servent aussi aux redirections du §8) :
  1. `Plafonds` (`id="plafonds"`)
     - H3 `Plafonds en tissu tendu à froid` (`id="plafonds-tendus"`)
     - H3 `Plafonds phoniques et acoustiques` (`id="plafonds-acoustiques"`)
     - H3 `Plafonds en plaques de plâtre (placoplâtre)` (`id="plafonds-placoplatre"`)
     - H3 `Plafonds en fibre de bois et en fibre minérale` (`id="plafonds-fibre"`)
     - H3 `Plafonds en bacs métalliques` (`id="plafonds-metalliques"`)
     - H3 `Cadres acoustiques` (`id="cadres-acoustiques"`)
  2. `Cloisons` (`id="cloisons"`)
     - H3 `Cloisons légères en plaques de plâtre` (`id="cloisons-placoplatre"`)
     - H3 `Cloisons mobiles en aluminium` (`id="cloisons-mobiles"`)
  3. `Isolation thermique et phonique` (`id="isolation"`)
     - H3 `Isolation phonique`
     - H3 `Isolation thermique intérieure`
     - H3 `Chape flottante contre les bruits d'impact` (`id="chape-flottante"`)
  4. `Protection incendie` (`id="protection-incendie"`)
  5. `Intégrations au plafond` (`id="integrations"`) : H3 `Caissons lumineux`, `Trappes de visite`, `Puits de lumière`
  6. `Peinture intérieure` (`id="peinture"`) `[À VALIDER : périmètre exact de l'offre peinture]`
  7. `Comment se déroule un chantier` : visite, offre écrite, planning, protection des lieux, nettoyage, réception. `[À VALIDER avec le client]`
  8. `Demander une offre` (CTA)
- **Gabarit de chaque H3** (100 à 250 mots) : à quoi ça sert → pour quels locaux → avantages → points d'attention → lien vers une réalisation liée (`realisations.html#...`) → lien « Demander une offre ».
- **Normes :** citer SIA 181 (acoustique) et les prescriptions AEAI (incendie) **sans promettre de performance chiffrée**. Formule type : « selon les exigences définies pour le projet ».
- **Volume de texte visé :** 1'500 à 2'500 mots.

### 3.3 `realisations.html`

- **`<title>`** : `Réalisations et références à Genève | Andy Construct` (52 car.)
- **Meta description** : `Faux-plafonds et cloisons réalisés pour la Ville de Genève, des salles communales, le Conservatoire, la HEAD, des entreprises et des particuliers.` (146 car.)
  - Si le client refuse de citer certains noms, remplacer par : `Faux-plafonds acoustiques, plafonds tendus et cloisons réalisés à Genève et dans l'ouest vaudois : salles communales, écoles, bureaux et logements.` (147 car.)
- **H1** : `Réalisations et références`
- **Structure H2 :**
  1. `Projets choisis` : une fiche par projet, en H3, p. ex. `Salle communale de Plan-les-Ouates : plafond acoustique (20XX)`. Contenu de la fiche :
     - commune ;
     - année ;
     - type de client ;
     - besoin ;
     - solution et matériaux ;
     - 2 à 4 photos ;
     - lien vers la prestation.
     - Chaque fiche porte un `id` (p. ex. `id="plan-les-ouates-salle-communale"`).
  2. `Avant / après` (`id="avant-apres"`)
  3. `Ils nous ont fait confiance` (`id="references"`). Liste en texte, groupée :
     - Collectivités et institutions : Ville de Genève, Mairie de Plan-les-Ouates, salle communale de Collonge-Bellerive, OMC ;
     - Culture et formation : Conservatoire de Musique de Genève, Salle de l'Alhambra, HEAD Genève, Harmonie Nautique ;
     - Entreprises : Piaget, De Grisogono, UBS, Bank Sarasin, Celgene, Laboratoire Covance, Energestion, Dipan SA ;
     - Hôtellerie et domaines : Hôtel à Chavannes-de-Bogis, Domaine des Perrières à Coppet.
  4. `Pour les architectes, régies et collectivités` (`id="professionnels"`) : types d'ouvrages traités, codes CFC concernés (271 plâtrerie, 283 faux-plafonds, 285 peinture `[À VALIDER selon les prestations réelles]`), **dossier de références PDF** téléchargeable (lien texte explicite + poids du fichier), contact direct.
  5. `Votre projet` (CTA)
- **Photos :** le dossier source compte plus de 100 photos de 1 à 1,7 Mo. Sélectionner les 30 à 40 meilleures, légender chaque photo avec le lieu et le type de travaux (le client doit fournir ces informations), et les optimiser (§9.3).

### 3.4 `contact.html`

- **`<title>`** : `Contact et devis faux-plafond Genève | Andy Construct` (53 car.)
- **Meta description** : `Contactez Andy Construct pour votre faux-plafond, cloison ou isolation à Genève : +41 22 771 20 15 ou +41 78 631 14 34, du lundi au vendredi.` (141 car.)
- **H1** : `Contact et demande d'offre`
- **Structure H2 :**
  1. `Nous appeler` : les deux numéros en grand (liens `tel:`), horaires.
  2. `Nous écrire` : formulaire **court**, avec les champs :
     - nom ;
     - téléphone **ou** e-mail ;
     - commune ;
     - type de travaux (liste déroulante) ;
     - message ;
     - photo ou plan (facultatif) ;
     - case de consentement accompagnée d'un lien vers la politique de confidentialité.
     - Pas de captcha visuel : utiliser un champ piège (honeypot).
  3. `Adresse` : bloc NAP `<address>` + lien « Voir sur la carte » vers la fiche Google (pas d'iframe Google Maps chargée par défaut, pour la nLPD et la vitesse).
  4. `Zone d'intervention` : communes principales (§5).
  5. `Pour préparer votre demande` : surface approximative, plans ou photos, délai souhaité, type de local.

### 3.5 `mentions-legales.html`

- **`<title>`** : `Mentions légales et confidentialité | Andy Construct` (52 car.)
- **Meta description** : `Mentions légales et politique de confidentialité du site d'Andy Construct, Chanton & Cie, entreprise de faux-plafonds et cloisons à Genève.` (139 car.)
- **H1** : `Mentions légales et protection des données`
- **Structure H2 :**
  1. `Éditeur du site` : raison sociale exacte (art. 954a CO), forme juridique, siège, adresse, IDE, téléphone, e-mail. `[À VALIDER]`
  2. `Hébergement` : nom et adresse de l'hébergeur.
  3. `Propriété intellectuelle et crédits photos`
  4. `Protection des données (nLPD)` :
     - données collectées par le formulaire ;
     - finalité ;
     - durée de conservation ;
     - destinataires (hébergeur, messagerie) ;
     - droits (accès, rectification, effacement) ;
     - contact.
  5. `Cookies et mesure d'audience` : outil utilisé et consentement le cas échéant.
- **Indexation :** laisser la page indexable (utile à l'identification de l'entreprise). Lien depuis le pied de page uniquement.

---

## 4. FAQ (accueil) : 10 questions, texte visible + FAQPage

Ce sont les questions telles que les gens les tapent ou les posent à une IA. Les réponses sont factuelles et prudentes : **aucun prix, délai ou performance chiffrée n'est inventé**. Les éléments `[À VALIDER]` sont à confirmer par le client, ou à retirer avant publication.

1. **Combien de temps faut-il pour poser un faux-plafond ?**
   Cela dépend de la surface, du type de plafond et de l'accès au chantier. Pour une pièce d'habitation, la pose prend généralement quelques jours ; pour des bureaux ou une salle, nous établissons un planning après la visite. Le délai est toujours indiqué dans notre offre.

2. **Quelle est la différence entre un plafond tendu et un faux-plafond en plâtre ?**
   Un plafond tendu est une toile tendue sur des profilés fixés au pourtour de la pièce : la pose est rapide et produit très peu de poussière. Un faux-plafond en plaques de plâtre est vissé sur une ossature métallique, puis les joints sont enduits et le plafond est peint. Les deux peuvent intégrer de l'éclairage et, selon le produit choisi, améliorer l'acoustique.

3. **Qu'est-ce qu'un plafond en tissu tendu à froid ?**
   C'est un plafond tendu réalisé avec une toile en tissu, mise en tension sans chauffage, contrairement aux membranes en PVC qui se posent à chaud. Cette technique convient aux logements habités comme aux lieux publics. Le choix de la toile (aspect, acoustique, comportement au feu) se fait selon l'usage du local.

4. **Un plafond acoustique réduit-il le bruit des voisins du dessus ?**
   Pas forcément, car il y a deux problèmes différents. Un plafond acoustique absorbant réduit l'écho à l'intérieur de la pièce (salle de réunion, restaurant, salle communale). Pour limiter les bruits venant d'un autre logement, il faut une isolation phonique, par exemple un faux-plafond désolidarisé avec isolant. Nous vous conseillons la bonne solution après une visite.

5. **À quoi sert une chape flottante ?**
   Une chape flottante est posée sur une couche isolante souple, sans contact rigide avec la dalle ni avec les murs. Elle réduit les bruits d'impact (pas, chutes d'objets, déplacements de chaises) transmis aux locaux situés en dessous. Elle se prévoit lors d'une rénovation de sol ou d'une construction.

6. **Combien coûte un faux-plafond à Genève ?**
   Le prix dépend de la surface, du système choisi (plâtre, fibre, métal, tissu tendu, acoustique), de la hauteur, de l'accès et des finitions (éclairage, trappes, peinture). C'est pourquoi nous ne donnons pas de prix au mètre carré sans avoir vu le chantier. Après une visite ou sur la base de vos plans, vous recevez une offre détaillée. `[À VALIDER : préciser « gratuite et sans engagement » si le client le confirme]`

7. **Intervenez-vous en dehors du canton de Genève ?**
   Oui. Nous travaillons dans tout le canton de Genève et dans l'ouest vaudois, notamment à Nyon, à Coppet et en Terre Sainte. Nous y avons par exemple réalisé des travaux pour le Domaine des Perrières à Coppet, pour Dipan SA à Nyon et pour un hôtel à Chavannes-de-Bogis. Pour d'autres régions, contactez-nous.

8. **Travaillez-vous pour les régies, les architectes et les collectivités ?**
   Oui, c'est une part importante de notre activité, à côté des particuliers. Nous avons notamment travaillé pour la Ville de Genève, les salles communales de Collonge-Bellerive et de Plan-les-Ouates, le Conservatoire de Musique de Genève et la HEAD. Nous établissons nos offres sur la base de vos plans et descriptifs.

9. **Vos faux-plafonds peuvent-ils protéger contre le feu ?**
   Oui, nous posons des plafonds et des habillages de protection incendie. La résistance au feu exigée (par exemple EI 30) est fixée par le concept de protection incendie du bâtiment, selon les prescriptions de l'AEAI, et le système posé doit y correspondre. Indiquez-nous le niveau demandé dès votre demande d'offre.

10. **Peut-on obtenir des subventions pour isoler à Genève ?**
    Certaines mesures d'isolation peuvent être subventionnées par le canton (programme GEnergie) et par le Programme Bâtiments, si les performances exigées sont atteintes. La demande doit être déposée avant le début des travaux. Les conditions à jour sont publiées sur ge-energie.ch ; demandez-nous conseil pour savoir si vos travaux peuvent être concernés.

**Règles d'intégration :**
- une seule FAQ sur le site (accueil) ; pas de duplication ailleurs ;
- chaque question en `<h3>` (sous le H2 « Questions fréquentes ») ou en `<summary>` ;
- le JSON-LD `FAQPage` (§6.3) reprend **mot pour mot** le texte visible ;
- Google n'affiche plus de résultats enrichis FAQ depuis mai 2026, mais le balisage reste valide ; c'est surtout le **texte visible** qui sert aux IA.

---

## 5. Communes et zones à citer

**Principe :** citer les zones dans une section « Zone d'intervention » (accueil et contact) et dans les fiches projets (commune réelle du chantier). **Pas de liste de 45 communes en pied de page, ni de pages clonées par commune.**

**Formulation recommandée :**
> Nous intervenons dans tout le canton de Genève (Genève-ville, Trois-Chêne, Carouge, Lancy, Arve-Lac, Rive droite) et dans l'ouest vaudois (Terre Sainte, Nyon et environs).

**Liste de référence** (en gras : communes à citer en priorité, parce qu'il y a une adresse ou une référence réelle) :

| Zone | Communes |
|---|---|
| Ville de Genève | **Genève** (quartiers : Eaux-Vives, Champel, Plainpalais, Jonction, Pâquis, Servette, Cité) |
| Trois-Chêne | **Chêne-Bourg**, Chêne-Bougeries, Thônex |
| Arve-Lac | **Collonge-Bellerive**, Cologny, Vandœuvres, Corsier, Anières, Hermance, Choulex, Meinier, Puplinge, Presinge, Jussy |
| Sud / Arve-Rhône | **Carouge**, **Plan-les-Ouates**, Lancy, Veyrier, Troinex, Bardonnex, Onex, Confignon, Bernex, Perly-Certoux |
| Rive droite | Vernier, Meyrin, Grand-Saconnex, Pregny-Chambésy, Bellevue, Genthod, Versoix, Collex-Bossy, Satigny, Céligny |
| Vaud : Terre Sainte | **Coppet**, **Chavannes-de-Bogis**, Founex, Commugny, Mies, Tannay, Chavannes-des-Bois |
| Vaud : Nyon et environs | **Nyon**, Prangins, Gland, Crans, Rolle `[À VALIDER : jusqu'où le client se déplace-t-il ?]` |

---

## 6. Données structurées (schema.org, JSON-LD)

### 6.1 Recommandations

- **Type recommandé : `HomeAndConstructionBusiness`.** Google demande « le sous-type le plus spécifique possible ». Or `GeneralContractor` signifie **entreprise générale**, ce qu'Andy Construct n'est pas (entreprise spécialisée du second œuvre). `HousePainter` ne couvre que la peinture. `HomeAndConstructionBusiness` est donc le plus juste. Les métiers précis passent par `knowsAbout` et `hasOfferCatalog`.
- **Champs obligatoires pour Google :** `name`, `address`.
- **Champs recommandés :**
  - `telephone`, `url`, `geo`, `openingHoursSpecification`, `image` ;
  - `areaServed`, `sameAs`, `logo`, `legalName`, `foundingDate`, `identifier` (IDE) ;
  - `hasOfferCatalog`, `contactPoint`.
- **Ne pas mettre** d'`aggregateRating` ni de `review` sur son propre site : Google ne les affiche pas pour une entreprise qui se note elle-même (règle de 2019). Les avis se collectent sur la fiche Google.
- **Cohérence :** tout ce qui est dans le JSON-LD doit être **visible sur la page** (adresse, téléphone, horaires, FAQ).
- **Une seule entité** définie en entier sur l'accueil, avec l'`@id` `https://www.andyconstruct.ch/#entreprise`. Les autres pages s'y réfèrent par cet `@id` (§6.4).
- **Coordonnées géographiques :** celles de l'Avenue de Bel-Air 57 à Chêne-Bourg viennent d'OpenStreetMap (Nominatim) : `46.20170, 6.19946`. Si l'adresse de **Carouge** est retenue, utiliser `46.18935, 6.13236` (même source) et remplacer le bloc `address` par : `"streetAddress": "Route des Acacias 48", "postalCode": "1227", "addressLocality": "Carouge"`.
- **`sameAs` :** mettre à jour après la correction des annuaires (l'URL local.ch peut changer). Ajouter l'URL de la fiche Google dès qu'elle est vérifiée.
- **Validation :** [Rich Results Test](https://search.google.com/test/rich-results) et [Schema Markup Validator](https://validator.schema.org/) avant la mise en production.

### 6.2 JSON-LD complet pour `index.html`

À placer dans le `<head>` : `<script type="application/ld+json"> … </script>`

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "HomeAndConstructionBusiness",
      "@id": "https://www.andyconstruct.ch/#entreprise",
      "name": "Andy Construct",
      "legalName": "Andy Construct, Chanton & Cie",
      "slogan": "Plafonds · Cloisons · Peinture",
      "description": "Entreprise genevoise spécialisée dans la pose de faux-plafonds (tendus, acoustiques, en plaques de plâtre, en fibre ou métalliques), de cloisons légères et mobiles, d'isolation thermique et phonique, ainsi que dans la peinture intérieure. Intervient dans le canton de Genève et dans l'ouest vaudois pour particuliers, régies, architectes, entreprises et collectivités.",
      "url": "https://www.andyconstruct.ch/",
      "logo": "https://www.andyconstruct.ch/assets/img/brand/logo-andy-construct.png",
      "image": [
        "https://www.andyconstruct.ch/assets/img/brand/logo-andy-construct.png"
      ],
      "telephone": "+41 22 771 20 15",
      "email": "andy.construct@bluewin.ch",
      "foundingDate": "2007",
      "identifier": {
        "@type": "PropertyValue",
        "propertyID": "IDE",
        "value": "CHE-113.706.162"
      },
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Avenue de Bel-Air 57",
        "postalCode": "1225",
        "addressLocality": "Chêne-Bourg",
        "addressRegion": "GE",
        "addressCountry": "CH"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 46.20170,
        "longitude": 6.19946
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
          "opens": "07:00",
          "closes": "18:00"
        }
      ],
      "contactPoint": [
        {
          "@type": "ContactPoint",
          "telephone": "+41 22 771 20 15",
          "contactType": "customer service",
          "areaServed": "CH",
          "availableLanguage": ["fr"]
        },
        {
          "@type": "ContactPoint",
          "telephone": "+41 78 631 14 34",
          "contactType": "sales",
          "areaServed": "CH",
          "availableLanguage": ["fr"]
        }
      ],
      "areaServed": [
        { "@type": "AdministrativeArea", "name": "Canton de Genève" },
        { "@type": "City", "name": "Genève" },
        { "@type": "City", "name": "Chêne-Bourg" },
        { "@type": "City", "name": "Carouge" },
        { "@type": "City", "name": "Collonge-Bellerive" },
        { "@type": "City", "name": "Plan-les-Ouates" },
        { "@type": "AdministrativeArea", "name": "District de Nyon" },
        { "@type": "City", "name": "Nyon" },
        { "@type": "City", "name": "Coppet" },
        { "@type": "City", "name": "Chavannes-de-Bogis" }
      ],
      "knowsAbout": [
        "Faux-plafonds",
        "Plafonds en tissu tendu à froid",
        "Plafonds acoustiques et phoniques",
        "Plafonds en plaques de plâtre",
        "Plafonds en fibre de bois et fibre minérale",
        "Plafonds en bacs métalliques",
        "Cadres acoustiques",
        "Cloisons légères en plaques de plâtre",
        "Cloisons mobiles en aluminium",
        "Isolation thermique intérieure",
        "Isolation phonique",
        "Chape flottante",
        "Protection incendie",
        "Peinture intérieure"
      ],
      "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Prestations Andy Construct",
        "itemListElement": [
          {
            "@type": "OfferCatalog",
            "name": "Plafonds",
            "itemListElement": [
              { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Plafonds en tissu tendu à froid", "url": "https://www.andyconstruct.ch/prestations.html#plafonds-tendus" } },
              { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Plafonds phoniques et acoustiques", "url": "https://www.andyconstruct.ch/prestations.html#plafonds-acoustiques" } },
              { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Plafonds en plaques de plâtre", "url": "https://www.andyconstruct.ch/prestations.html#plafonds-placoplatre" } },
              { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Plafonds en fibre de bois et fibre minérale", "url": "https://www.andyconstruct.ch/prestations.html#plafonds-fibre" } },
              { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Plafonds en bacs métalliques", "url": "https://www.andyconstruct.ch/prestations.html#plafonds-metalliques" } },
              { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Cadres acoustiques", "url": "https://www.andyconstruct.ch/prestations.html#cadres-acoustiques" } }
            ]
          },
          {
            "@type": "OfferCatalog",
            "name": "Cloisons",
            "itemListElement": [
              { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Cloisons légères en plaques de plâtre", "url": "https://www.andyconstruct.ch/prestations.html#cloisons-placoplatre" } },
              { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Cloisons mobiles en aluminium", "url": "https://www.andyconstruct.ch/prestations.html#cloisons-mobiles" } }
            ]
          },
          {
            "@type": "OfferCatalog",
            "name": "Isolation, acoustique et sécurité",
            "itemListElement": [
              { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Isolation thermique et phonique", "url": "https://www.andyconstruct.ch/prestations.html#isolation" } },
              { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Chape flottante contre les bruits d'impact", "url": "https://www.andyconstruct.ch/prestations.html#chape-flottante" } },
              { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Protection incendie", "url": "https://www.andyconstruct.ch/prestations.html#protection-incendie" } },
              { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Caissons lumineux, trappes de visite et puits de lumière", "url": "https://www.andyconstruct.ch/prestations.html#integrations" } }
            ]
          },
          {
            "@type": "OfferCatalog",
            "name": "Peinture",
            "itemListElement": [
              { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Peinture intérieure", "url": "https://www.andyconstruct.ch/prestations.html#peinture" } }
            ]
          }
        ]
      },
      "sameAs": [
        "https://www.facebook.com/andyconstruct.bajrami",
        "https://www.local.ch/fr/d/carouge-ge/1227/revetement-des-plafonds-et-plafonds-suspendus/andy-construct-chanton-cie-OGrZ5DP4atJqYki9WoTjPg",
        "https://search.ch/tel/chene-bourg/avenue-de-bel-air-57/andy-construct-chanton-cie"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://www.andyconstruct.ch/#site",
      "url": "https://www.andyconstruct.ch/",
      "name": "Andy Construct",
      "inLanguage": "fr-CH",
      "publisher": { "@id": "https://www.andyconstruct.ch/#entreprise" }
    },
    {
      "@type": "WebPage",
      "@id": "https://www.andyconstruct.ch/#accueil",
      "url": "https://www.andyconstruct.ch/",
      "name": "Faux-plafonds et cloisons à Genève | Andy Construct",
      "inLanguage": "fr-CH",
      "isPartOf": { "@id": "https://www.andyconstruct.ch/#site" },
      "about": { "@id": "https://www.andyconstruct.ch/#entreprise" }
    }
  ]
}
```

**Notes sur ce JSON-LD :**
- `image` : remplacer ou compléter par 1 à 3 photos de chantier réelles (URL absolues, format 16:9, 4:3 ou 1:1, au moins 1'200 px de large) dès qu'elles sont en ligne.
- `legalName`, `foundingDate`, `address`, `geo`, `email` et `openingHoursSpecification` sont `[À VALIDER]` (voir §0).
- Aucun commentaire n'est autorisé dans un JSON : ne pas laisser de marqueurs `[À VALIDER]` dans le fichier publié.

### 6.3 JSON-LD `FAQPage` (sur `index.html`, dans un second bloc `<script>`)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "@id": "https://www.andyconstruct.ch/#faq",
  "inLanguage": "fr-CH",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Combien de temps faut-il pour poser un faux-plafond ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Cela dépend de la surface, du type de plafond et de l'accès au chantier. Pour une pièce d'habitation, la pose prend généralement quelques jours ; pour des bureaux ou une salle, nous établissons un planning après la visite. Le délai est toujours indiqué dans notre offre." }
    },
    {
      "@type": "Question",
      "name": "Quelle est la différence entre un plafond tendu et un faux-plafond en plâtre ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Un plafond tendu est une toile tendue sur des profilés fixés au pourtour de la pièce : la pose est rapide et produit très peu de poussière. Un faux-plafond en plaques de plâtre est vissé sur une ossature métallique, puis les joints sont enduits et le plafond est peint. Les deux peuvent intégrer de l'éclairage et, selon le produit choisi, améliorer l'acoustique." }
    },
    {
      "@type": "Question",
      "name": "Qu'est-ce qu'un plafond en tissu tendu à froid ?",
      "acceptedAnswer": { "@type": "Answer", "text": "C'est un plafond tendu réalisé avec une toile en tissu, mise en tension sans chauffage, contrairement aux membranes en PVC qui se posent à chaud. Cette technique convient aux logements habités comme aux lieux publics. Le choix de la toile (aspect, acoustique, comportement au feu) se fait selon l'usage du local." }
    },
    {
      "@type": "Question",
      "name": "Un plafond acoustique réduit-il le bruit des voisins du dessus ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Pas forcément, car il y a deux problèmes différents. Un plafond acoustique absorbant réduit l'écho à l'intérieur de la pièce (salle de réunion, restaurant, salle communale). Pour limiter les bruits venant d'un autre logement, il faut une isolation phonique, par exemple un faux-plafond désolidarisé avec isolant. Nous vous conseillons la bonne solution après une visite." }
    },
    {
      "@type": "Question",
      "name": "À quoi sert une chape flottante ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Une chape flottante est posée sur une couche isolante souple, sans contact rigide avec la dalle ni avec les murs. Elle réduit les bruits d'impact (pas, chutes d'objets, déplacements de chaises) transmis aux locaux situés en dessous. Elle se prévoit lors d'une rénovation de sol ou d'une construction." }
    },
    {
      "@type": "Question",
      "name": "Combien coûte un faux-plafond à Genève ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Le prix dépend de la surface, du système choisi (plâtre, fibre, métal, tissu tendu, acoustique), de la hauteur, de l'accès et des finitions (éclairage, trappes, peinture). C'est pourquoi nous ne donnons pas de prix au mètre carré sans avoir vu le chantier. Après une visite ou sur la base de vos plans, vous recevez une offre détaillée." }
    },
    {
      "@type": "Question",
      "name": "Intervenez-vous en dehors du canton de Genève ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui. Nous travaillons dans tout le canton de Genève et dans l'ouest vaudois, notamment à Nyon, à Coppet et en Terre Sainte. Nous y avons par exemple réalisé des travaux pour le Domaine des Perrières à Coppet, pour Dipan SA à Nyon et pour un hôtel à Chavannes-de-Bogis. Pour d'autres régions, contactez-nous." }
    },
    {
      "@type": "Question",
      "name": "Travaillez-vous pour les régies, les architectes et les collectivités ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, c'est une part importante de notre activité, à côté des particuliers. Nous avons notamment travaillé pour la Ville de Genève, les salles communales de Collonge-Bellerive et de Plan-les-Ouates, le Conservatoire de Musique de Genève et la HEAD. Nous établissons nos offres sur la base de vos plans et descriptifs." }
    },
    {
      "@type": "Question",
      "name": "Vos faux-plafonds peuvent-ils protéger contre le feu ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, nous posons des plafonds et des habillages de protection incendie. La résistance au feu exigée (par exemple EI 30) est fixée par le concept de protection incendie du bâtiment, selon les prescriptions de l'AEAI, et le système posé doit y correspondre. Indiquez-nous le niveau demandé dès votre demande d'offre." }
    },
    {
      "@type": "Question",
      "name": "Peut-on obtenir des subventions pour isoler à Genève ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Certaines mesures d'isolation peuvent être subventionnées par le canton (programme GEnergie) et par le Programme Bâtiments, si les performances exigées sont atteintes. La demande doit être déposée avant le début des travaux. Les conditions à jour sont publiées sur ge-energie.ch ; demandez-nous conseil pour savoir si vos travaux peuvent être concernés." }
    }
  ]
}
```

Si le client valide « offre gratuite et sans engagement » (question 6), ajouter la même phrase **dans le texte visible et dans le JSON-LD**.

### 6.4 Autres pages (JSON-LD minimal)

Sur `prestations.html`, `realisations.html`, `contact.html` et `mentions-legales.html`, déclarer une `WebPage` (pour la page contact, préférer `ContactPage`) qui renvoie à l'entité de l'accueil, sans la redéfinir :

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "@id": "https://www.andyconstruct.ch/prestations.html#page",
  "url": "https://www.andyconstruct.ch/prestations.html",
  "name": "Plafond tendu, acoustique, cloison à Genève | Andy Construct",
  "inLanguage": "fr-CH",
  "isPartOf": { "@id": "https://www.andyconstruct.ch/#site" },
  "about": { "@id": "https://www.andyconstruct.ch/#entreprise" },
  "publisher": { "@id": "https://www.andyconstruct.ch/#entreprise" }
}
```

---

## 7. Fichier `/llms.txt` (GEO)

Fichier texte en Markdown, placé **à la racine** (`site/llms.txt`, servi à `https://www.andyconstruct.ch/llms.txt`), encodé en UTF-8. Il suit le format proposé sur [llmstxt.org](https://llmstxt.org/). Aucun grand fournisseur d'IA ne l'a officiellement adopté : c'est un pari peu coûteux. Le mettre à jour à chaque changement de coordonnées ou de prestations. **Ne publier que des informations validées** : retirer ou corriger les lignes concernées par le §0 avant la mise en ligne.

```markdown
# Andy Construct

> Andy Construct est une entreprise genevoise spécialisée dans la pose de faux-plafonds, de cloisons, d'isolation thermique et phonique, ainsi que dans la peinture intérieure (« Plafonds · Cloisons · Peinture »). Elle intervient dans le canton de Genève et dans l'ouest vaudois pour des particuliers, des régies, des architectes, des entreprises et des collectivités publiques.

Informations clés :

- Nom commercial : Andy Construct
- Raison sociale : Andy Construct, Chanton & Cie (société en nom collectif), IDE CHE-113.706.162
- Inscrite au registre du commerce du canton de Genève depuis 2007
- Adresse : Avenue de Bel-Air 57, 1225 Chêne-Bourg (Genève), Suisse
- Téléphone : +41 22 771 20 15 ; mobile : +41 78 631 14 34
- E-mail : andy.construct@bluewin.ch
- Horaires : du lundi au vendredi, 7 h 00 – 18 h 00
- Zone d'intervention : tout le canton de Genève (dont Genève-ville, Trois-Chêne, Carouge, Collonge-Bellerive, Plan-les-Ouates) et l'ouest vaudois (Nyon, Coppet, Terre Sainte, Chavannes-de-Bogis)
- Clientèle : particuliers, régies et gérances, architectes et bureaux d'ingénieurs, PME, collectivités publiques
- Langue : français

Prestations :

- Plafonds : tissu tendu à froid, plafonds phoniques et acoustiques, plaques de plâtre (placoplâtre), fibre de bois, fibre minérale, bacs métalliques, cadres acoustiques
- Cloisons : cloisons légères en plaques de plâtre, cloisons mobiles en aluminium
- Isolation : isolation thermique intérieure, isolation phonique, chape flottante contre les bruits d'impact
- Sécurité et intégrations : protection incendie, caissons lumineux directs et indirects, trappes de visite, puits de lumière dans le faux-plafond
- Peinture intérieure

Références (liste publiée par l'entreprise ; années détaillées sur la page Réalisations) : Ville de Genève ; salle communale de Collonge-Bellerive ; Mairie de Plan-les-Ouates (salle communale) ; Conservatoire de Musique de Genève ; Salle de l'Alhambra ; HEAD – Haute école d'art et de design Genève ; OMC ; Piaget ; De Grisogono ; UBS ; Bank Sarasin ; Celgene ; Laboratoire Covance CLS SA ; Energestion Ingénieurs & Architectes SIA ; Domaine des Perrières (Coppet VD) ; Dipan SA (Nyon VD) ; Hôtel à Chavannes-de-Bogis ; Harmonie Nautique de Genève.

## Pages principales

- [Accueil](https://www.andyconstruct.ch/): présentation de l'entreprise, zone d'intervention et questions fréquentes
- [Prestations](https://www.andyconstruct.ch/prestations.html): description de chaque type de plafond, de cloison et d'isolation, protection incendie, peinture
- [Réalisations et références](https://www.andyconstruct.ch/realisations.html): fiches projets datées, photos avant/après, liste des références, informations pour architectes, régies et collectivités
- [Contact](https://www.andyconstruct.ch/contact.html): téléphones, horaires, adresse, formulaire de demande d'offre

## Questions fréquentes

- [Questions fréquentes](https://www.andyconstruct.ch/#faq): durée de pose, plafond tendu ou plâtre, tissu tendu à froid, acoustique et bruit des voisins, chape flottante, prix, zone d'intervention, travaux pour régies et collectivités, protection incendie, subventions à l'isolation à Genève

## Optional

- [Mentions légales et protection des données](https://www.andyconstruct.ch/mentions-legales.html): raison sociale, siège, IDE, politique de confidentialité
- [Page Facebook](https://www.facebook.com/andyconstruct.bajrami)
```

**Si l'adresse de Carouge est retenue**, remplacer la ligne « Adresse » par :
`- Adresse : Route des Acacias 48, 1227 Carouge (Genève), Suisse`
**Si « Chanton & Cie » ne doit pas apparaître**, garder quand même la raison sociale légale sur cette ligne : c'est elle qui permet aux IA de rapprocher le site du registre du commerce.

---

## 8. robots.txt, sitemap.xml, redirections 301

### 8.1 `robots.txt` (production)

```text
User-agent: *
Allow: /

Sitemap: https://www.andyconstruct.ch/sitemap.xml
```

Ne **pas** bloquer les robots des IA (GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot, Google-Extended, Bingbot) : un contenu bloqué ne peut pas être cité.

**En préproduction :**
- `Disallow: /` n'est **pas** suffisant : une page bloquée peut quand même être indexée sans son contenu ;
- utiliser le `noindex` du §0.2.

### 8.2 `sitemap.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://www.andyconstruct.ch/</loc><lastmod>AAAA-MM-JJ</lastmod></url>
  <url><loc>https://www.andyconstruct.ch/prestations.html</loc><lastmod>AAAA-MM-JJ</lastmod></url>
  <url><loc>https://www.andyconstruct.ch/realisations.html</loc><lastmod>AAAA-MM-JJ</lastmod></url>
  <url><loc>https://www.andyconstruct.ch/contact.html</loc><lastmod>AAAA-MM-JJ</lastmod></url>
  <url><loc>https://www.andyconstruct.ch/mentions-legales.html</loc><lastmod>AAAA-MM-JJ</lastmod></url>
</urlset>
```

Remplacer `AAAA-MM-JJ` par la date réelle de dernière modification. Soumettre le sitemap dans Google Search Console et dans Bing Webmaster Tools.

### 8.3 Redirections 301 des anciennes URL

Les anciennes URL existent **avec et sans** `/index.php/`, et **avec et sans** `www` (vérifié le 25.09.2026). Toutes doivent rediriger en une seule étape.

| Ancienne URL (chemin) | Nouvelle URL |
|---|---|
| `/`, `/index.php` | `/` |
| `/presentation` | `/` |
| `/produits/plafonds/plafonds-en-tissu-tendu-a-froid` | `/prestations.html#plafonds-tendus` |
| `/produits/plafonds/plafonds-phoniques-et-acoustiques` | `/prestations.html#plafonds-acoustiques` |
| `/produits/plafonds/plafonds-en-placoplatre` | `/prestations.html#plafonds-placoplatre` |
| `/produits/plafonds/plafonds-en-fibre-de-bois` | `/prestations.html#plafonds-fibre` |
| `/produits/plafonds/plafonds-en-fibre-minerale` | `/prestations.html#plafonds-fibre` |
| `/produits/plafonds/plafonds-en-bac-metallique` | `/prestations.html#plafonds-metalliques` |
| `/produits/cloisons/cloisons-legeres-en-placoplatre` | `/prestations.html#cloisons-placoplatre` |
| `/produits/cloisons/cloisons-mobiles-en-aluminium` | `/prestations.html#cloisons-mobiles` |
| `/produits/cloisons/isolation-thermique-ou-phonique` | `/prestations.html#isolation` |
| `/produits/cadres-acoustiques` | `/prestations.html#cadres-acoustiques` |
| `/realisations/photos-travaux-2014-2016` | `/realisations.html` |
| `/realisations/photos-travaux-avant-apres` | `/realisations.html#avant-apres` |
| `/realisations/references` | `/realisations.html#references` |
| `/contact` | `/contact.html` |

Chacune de ces URL existe aussi préfixée par `/index.php/` : la redirection est la même.

**Exemple pour Apache ou LiteSpeed (`.htaccess`)**, à adapter si l'hébergeur final est différent (nginx : équivalent en `return 301`) :

```apache
RewriteEngine On

# 1) Hôte unique : https + www
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} !^www\. [NC]
RewriteRule ^(.*)$ https://www.andyconstruct.ch/$1 [R=301,L]

# 2) Anciennes URL Joomla (avec ou sans index.php/)
RewriteRule ^(index\.php/?)?presentation/?$ /? [R=301,L]
RewriteRule ^(index\.php/)?produits/plafonds/plafonds-en-tissu-tendu-a-froid/?$ /prestations.html#plafonds-tendus [R=301,L,NE]
RewriteRule ^(index\.php/)?produits/plafonds/plafonds-phoniques-et-acoustiques/?$ /prestations.html#plafonds-acoustiques [R=301,L,NE]
RewriteRule ^(index\.php/)?produits/plafonds/plafonds-en-placoplatre/?$ /prestations.html#plafonds-placoplatre [R=301,L,NE]
RewriteRule ^(index\.php/)?produits/plafonds/plafonds-en-fibre-(de-bois|minerale)/?$ /prestations.html#plafonds-fibre [R=301,L,NE]
RewriteRule ^(index\.php/)?produits/plafonds/plafonds-en-bac-metallique/?$ /prestations.html#plafonds-metalliques [R=301,L,NE]
RewriteRule ^(index\.php/)?produits/cloisons/cloisons-legeres-en-placoplatre/?$ /prestations.html#cloisons-placoplatre [R=301,L,NE]
RewriteRule ^(index\.php/)?produits/cloisons/cloisons-mobiles-en-aluminium/?$ /prestations.html#cloisons-mobiles [R=301,L,NE]
RewriteRule ^(index\.php/)?produits/cloisons/isolation-thermique-ou-phonique/?$ /prestations.html#isolation [R=301,L,NE]
RewriteRule ^(index\.php/)?produits/cadres-acoustiques/?$ /prestations.html#cadres-acoustiques [R=301,L,NE]
RewriteRule ^(index\.php/)?realisations/photos-travaux-2014-2016/?$ /realisations.html [R=301,L]
RewriteRule ^(index\.php/)?realisations/photos-travaux-avant-apres/?$ /realisations.html#avant-apres [R=301,L,NE]
RewriteRule ^(index\.php/)?realisations/references/?$ /realisations.html#references [R=301,L,NE]
RewriteRule ^(index\.php/)?contact/?$ /contact.html [R=301,L]
RewriteRule ^index\.php/?$ / [R=301,L]
```

---

## 9. Règles de réalisation

### 9.1 Balisage sémantique
- `<html lang="fr-CH">`, `<meta charset="utf-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- Structure : `<header>` (logo + `<nav>` + téléphone cliquable), `<main>`, `<footer>` (NAP dans `<address>`, liens vers les pages et les mentions légales).
- **Un seul `<h1>` par page.** Hiérarchie H2 → H3 sans saut de niveau. Pas de titre utilisé uniquement pour le style.
- Liens explicites (« Voir nos plafonds acoustiques », pas « cliquez ici »). Numéros en `<a href="tel:...">`.
- `<link rel="canonical" href="https://www.andyconstruct.ch/...">` absolu sur chaque page.
- Open Graph sur chaque page : `og:title`, `og:description`, `og:url`, `og:type` (`website`), `og:locale` (`fr_CH`), `og:image` (1'200 × 630, une photo de chantier).
- Favicons : utiliser ceux déjà présents dans `site/assets/img/brand/`.

### 9.2 Textes alternatifs (alt)
- Décrire **ce que montre la photo, avec le lieu**, en 5 à 15 mots. Par exemple :
  - `alt="Plafond acoustique posé dans la salle communale de Plan-les-Ouates"` ;
  - `alt="Cloison légère en plaques de plâtre dans des bureaux à Genève, avant peinture"` ;
  - `alt="Plafond en tissu tendu avec éclairage indirect dans un séjour"`.
- Pas de « image de », « photo de », ni de liste de mots-clés. Logo : `alt="Andy Construct"`. Images purement décoratives : `alt=""`.
- Nommer les fichiers de façon lisible : `plafond-acoustique-salle-communale-plan-les-ouates.avif` plutôt que `IMG_3581.jpg`.
- Si le lieu d'une photo n'est pas connu, décrire le type de travaux seulement : **ne jamais inventer un lieu**.

### 9.3 Performance (Core Web Vitals)
- **Objectifs** (seuils « bons » de Google, mesurés sur mobile) : **LCP ≤ 2,5 s**, **INP ≤ 200 ms**, **CLS ≤ 0,1** ([web.dev](https://web.dev/articles/vitals?hl=fr)).
- **Images :**
  - Les originaux font 1 à 1,7 Mo. Les convertir en **AVIF ou WebP**, et proposer plusieurs largeurs avec `srcset`/`sizes` (p. ex. 480, 960, 1'600 px).
  - Budgets indicatifs : ~200 Ko pour l'image principale, ~60 Ko par vignette.
  - Toujours indiquer `width` et `height` (évite les décalages de mise en page).
  - `loading="lazy"` sous la ligne de flottaison ; **jamais sur l'image principale**, qui reçoit `fetchpriority="high"`.
- **Pas de jQuery ni de carrousel automatique** : un carrousel qui défile seul est aussi pénible pour un public âgé. CSS et JS minimaux, JS en `defer`.
- **Polices :** 2 graisses au maximum, auto-hébergées en WOFF2 avec `font-display: swap` (ou polices système).
- **Cache :** en-têtes de cache longs sur `/assets/` (images, CSS, JS versionnés), compression gzip ou brotli.
- **Budget de poids :** page d'accueil **< 1 Mo** au total (objectif proposé).
- **Mesure :** PageSpeed Insights (mobile) sur les 5 pages avant la mise en production, puis dans le rapport Core Web Vitals de la Search Console.

### 9.4 Accessibilité et lisibilité (public de 45 à 70 ans)
- Texte courant d'**au moins 18 px**, interligne 1,5, contraste **AA** (4,5:1 au minimum).
- Zones cliquables d'au moins 44 × 44 px. Liens soulignés dans le texte.
- Téléphone visible sans défilement sur mobile et ordinateur. Sur mobile, un bouton « Appeler » discret et fixe.
- Formulaire : étiquettes visibles au-dessus des champs, messages d'erreur en clair, pas de délai imposé.

### 9.5 Maillage interne
- **Accueil** → chaque carte prestation vers l'ancre de `prestations.html` ; bloc références vers `realisations.html` ; CTA vers `contact.html`.
- **Prestations** → chaque H3 renvoie vers une fiche projet correspondante (`realisations.html#id-du-projet`) et vers `contact.html`.
- **Réalisations** → chaque fiche renvoie vers la prestation utilisée (`prestations.html#...`) ; bloc « Professionnels » vers `contact.html`.
- **Contact** → lien vers `realisations.html` (« voir nos références »).
- **Pied de page** (toutes les pages) : NAP, les 5 pages, lien Facebook.
- Ancres de liens descriptives et variées, pas toujours le même mot-clé.

### 9.6 NAP identique partout
- Copier le bloc du §1 **caractère pour caractère** (même format de numéro, même orthographe « Chêne-Bourg », même ordre).
- Même contenu dans le pied de page, la page contact, les mentions légales, le JSON-LD, le `llms.txt`, la fiche Google, local.ch, search.ch, Facebook, GGE, Kompass, Bing Places et Apple Business Connect.
- **Toute modification ultérieure** (déménagement, nouveau numéro) se fait partout **le même jour**.

### 9.7 Mesure
- Balise de vérification Google Search Console et Bing Webmaster Tools (ou vérification DNS).
- Outil de statistiques choisi avec le client (GA4 avec bannière de consentement, ou solution sans cookies), déclaré dans la politique de confidentialité.
- Événements à suivre : clic sur `tel:` (fixe et mobile séparément), envoi du formulaire, téléchargement du dossier de références PDF.

---

## 10. Recette SEO avant la mise en production (checklist)

- [ ] Décisions du §0 validées par le client ; plus aucun `[À VALIDER]` dans le code.
- [ ] `noindex` de préproduction **retiré** ; `robots.txt` de production en place.
- [ ] Un seul H1 par page ; titles et meta descriptions conformes au §3 (longueurs vérifiées).
- [ ] Canonical absolu sur les 5 pages ; hôte unique `https://www.`.
- [ ] Les 5 URL répondent en 200 ; les anciennes URL (avec et sans `index.php`, avec et sans `www`) redirigent en 301 **en une seule étape**.
- [ ] `sitemap.xml` et `llms.txt` accessibles à la racine.
- [ ] JSON-LD valide (Rich Results Test + Schema Markup Validator), et cohérent avec le texte visible (adresse, horaires, FAQ).
- [ ] Toutes les images ont un `alt` pertinent (ou `alt=""` si décoratives), avec `width` et `height`.
- [ ] PageSpeed mobile : LCP ≤ 2,5 s, CLS ≤ 0,1 sur l'accueil et la page réalisations.
- [ ] Liens `tel:` testés sur un smartphone ; formulaire testé (réception de l'e-mail, message de confirmation).
- [ ] Mentions légales et politique de confidentialité en ligne, liées depuis le pied de page et depuis le formulaire.
- [ ] Search Console et Bing Webmaster Tools vérifiés, sitemap soumis.
- [ ] NAP identique entre le site, la fiche Google, local.ch et search.ch (contrôle croisé).
