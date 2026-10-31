# Logos des références : sources, statut juridique et usage

Livrable de la phase 1 « Logos & preuve sociale » (voir `programme-v2.md`, §4 et §5).
Fichiers : `site/assets/img/references/` (logos + `logos.json`).
État au 31 octobre 2026. Ce document est une **analyse documentaire, pas un avis d'avocat**. En cas de doute sur un cas précis, faites-le valider par un juriste avant la mise en production.

> **Mise à jour v3 (31 octobre 2026)** : à la demande du client, toutes les références sont désormais affichées avec leur **logo officiel en couleur**, collectivités et OMC comprises (fichiers dans `references/couleur/`). Les collectivités et l'OMC passent de `protege` à `a_autoriser` : leur logo apparaît dans la version de validation seulement, et en production uniquement après une autorisation écrite. Voir le **§9**, qui l'emporte sur les §1, §4.1, §4.2, §5 et §6 en cas de contradiction.

## 1. En bref

| | Nombre | Rendu sur le site |
|---|---|---|
| Références de l'ancien site | **18** | |
| `a_autoriser` : logo préparé, accord écrit à obtenir | **12** | logo en **preview** ; nom en texte en **production** tant que l'accord n'est pas reçu |
| `protege` : armoiries publiques ou emblème d'organisation internationale | **5** | toujours en **nom typographique**, aucun fichier logo |
| `introuvable` : pas de logo fiable | **1** | nom typographique |
| `autorise` : accord écrit reçu | **0** | à basculer au fil des réponses |

Points d'attention :
- **4 références ont changé de nom ou de propriétaire** : Bank Sarasin, Covance, Celgene, l'hôtel de Chavannes-de-Bogis. De Grisogono a fait faillite et sa marque a été rachetée. Voir le §3.
- **L'OMC** : la loi suisse peut protéger aussi son **nom** et son **sigle**, pas seulement son emblème (§4.2). Il faut demander son accord, même pour le nom en texte.
- **De Grisogono** : le client d'origine n'existe plus. Le nouveau propriétaire de la marque n'a jamais été client. Nous recommandons le **nom en texte seulement**.
- **5 logos viennent de fichiers raster** : HEAD, J. Safra Sarasin, Energestion, Dipan, Harmonie Nautique. Ils sont corrects pour le web, mais il faudra demander le fichier vectoriel en même temps que l'autorisation.

## 2. Tableau récapitulatif (ordre d'affichage recommandé)

L'ordre alterne public et privé, et place en tête les noms les plus parlants pour un maître d'ouvrage romand. C'est l'ordre du tableau `logos.json`.

| # | Nom affiché | Secteur | Statut | Fichiers (`references/`) | Échelle | Point clé |
|---|---|---|---|---|---|---|
| 1 | Ville de Genève | collectivites | `protege` | — | 1,00 | Armoiries dans le logo (LPAP art. 8) |
| 2 | Piaget | entreprises | `a_autoriser` | `piaget.svg`, `piaget-blanc.svg` | 1,00 | SVG Commons, marque déposée |
| 3 | Conservatoire de musique de Genève | culture-formation | `a_autoriser` | `conservatoire-musique-geneve(-blanc).svg` | 1,00 | SVG officiel (cmg.ch) |
| 4 | UBS | entreprises | `a_autoriser` | `ubs(-blanc).svg` | 0,90 | Fichier Wikipédia « fair use » : maquette seulement |
| 5 | HEAD – Genève | culture-formation | `a_autoriser` | `head-geneve(-blanc).png` | 0,95 | Source PNG 248 × 122 px |
| 6 | Salle communale de Collonge-Bellerive | collectivites | `protege` | — | 1,00 | Écusson communal (LPAP art. 8) |
| 7 | J. Safra Sarasin | entreprises | `a_autoriser` | `j-safra-sarasin(-blanc).png` | 1,30 | Anciennement Bank Sarasin (2013) |
| 8 | Salle de l'Alhambra | culture-formation | `protege` | — | 1,00 | Salle de la Ville de Genève, sans logo propre |
| 9 | Labcorp (ex-Covance) | entreprises | `a_autoriser` | `labcorp(-blanc).svg` | 0,80 | Covance CLS SA, Meyrin, renommée en 2021 |
| 10 | Mairie de Plan-les-Ouates | collectivites | `protege` | — | 1,00 | Écusson communal (LPAP art. 8) |
| 11 | Energestion | ingenierie | `a_autoriser` | `energestion(-blanc).png` | 1,00 | Logo actuel : « Ingénieurs-conseils SIA » |
| 12 | OMC | organisations-internationales | `protege` | — | 1,00 | Art. 6ter CUP + LPNE ; nom et sigle aussi |
| 13 | de Grisogono | entreprises | `a_autoriser` | `de-grisogono(-blanc).png` | 1,35 | Faillite 2020, marque rachetée (Damac, 2022) |
| 14 | Harmonie Nautique de Genève | culture-formation | `a_autoriser` | `harmonie-nautique(-blanc).png` | 1,10 | Association |
| 15 | Everness Hotel & Resort | hotellerie | `a_autoriser` | `everness(-blanc).svg` | 0,55 | Ex-Best Western Chavannes-de-Bogis (2020) : à confirmer |
| 16 | Dipan | entreprises | `a_autoriser` | `dipan(-blanc).png` | 1,25 | Dipan SA, Nyon (pas l'homonyme zurichoise) |
| 17 | Domaine des Perrières | hotellerie | `introuvable` | — | 1,00 | Aucun logo public |
| 18 | Celgene | entreprises | `a_autoriser` | `celgene(-blanc).svg` | 1,35 | Marque absorbée par Bristol Myers Squibb (2019) |

Pour chaque référence, `logos.json` contient aussi `nom_complet`, `lieu`, `source_url`, `licence_note` et `remarque`. Le champ `lieu` indique la localité du client (siège ou site connu), pas forcément celle du chantier. Il est laissé vide quand on ne la connaît pas (UBS, J. Safra Sarasin, Celgene).

## 3. Changements de nom vérifiés

| Référence (ancien site) | Situation actuelle | Source | Conséquence pour l'affichage |
|---|---|---|---|
| Bank Sarasin | Même société, renommée **Bank J. Safra Sarasin AG** en 2013 (anciens noms au registre : « Bank Sarasin & Cie AG »). À Genève : Banque J. Safra Sarasin SA | Zefix, CHE-105.933.773 | Logo actuel J. Safra Sarasin. Si le chantier date d'avant 2013, écrire en texte « Bank Sarasin (aujourd'hui J. Safra Sarasin) » |
| Laboratoire Covance CLS SA | Même société, renommée **Labcorp Central Laboratory Services Sàrl**, Meyrin. Noms précédents : Scicor SA, Corning Scicor SA, Covance Central Laboratory Services SA puis Sàrl. La marque Covance a disparu en 2021 | Zefix, CHE-107.357.998 ; avis de changement de nom de Labcorp (juin 2021) | Logo Labcorp, nom affiché « Labcorp (ex-Covance) ». **Pas Fortrea**, l'activité de recherche clinique séparée de Labcorp en 2023 |
| Celgene | Rachetée par **Bristol Myers Squibb** (2019). La marque n'est plus utilisée, mais les sociétés suisses gardent le nom (Celgene International Sàrl, Boudry NE) | Zefix ; SEC (déjà cité dans `analyse-marche.md`) | Logo Celgene d'époque, accord à demander à BMS. **Ne pas afficher le logo BMS** : BMS n'était pas le client |
| De Grisogono | **De Grisogono SA** : faillite en janvier 2020, radiée le 5 mars 2024. La marque a été reprise en 2022 par le groupe Damac via **De Grisogono Swiss SA** (Les Acacias) | Zefix, CHE-108.459.035 et CHE-280.541.539 ; presse (Bloomberg, Arabian Business, 2022) | Logo actuel préparé, mais nous recommandons le **nom seulement** |
| Hôtel de Chavannes-de-Bogis | Ancien **Best Western Hôtel Chavannes-de-Bogis**, devenu **Everness Hotel & Resort** en quittant Best Western en 2020 (Les Champs-Blancs 70b) | everness.ch ; MySwitzerland, plateformes de réservation | Logo Everness. **Le client doit confirmer qu'il s'agit du même hôtel**, sinon garder « Hôtel à Chavannes-de-Bogis » en texte |
| Energestion Ingénieurs & Architectes SIA | **Energestion SA**, chemin de la Gravière 2, 1227 Les Acacias (voisin d'Andy Construct). Le logo actuel porte « Ingénieurs-conseils SIA » | Zefix, CHE-107.990.227 ; energestion.ch | Logo actuel |
| Dipan SA (Nyon) | **Dipan SA**, rue de Rive 18, Nyon : traitement et protection anticorrosion des réseaux d'eau (« Water Technology ») | Zefix, CHE-280.348.623 ; dipan.ch | Logo actuel. Une homonyme existe à Zurich (CHE-495.145.395) |
| Domaine des Perrières (Coppet) | Pas de marque publique. Lien possible avec la **Société anonyme Les Perrières**, société immobilière (route Suisse 37, Coppet, CHE-102.705.000) | Zefix | Nom en texte. Ne pas confondre avec la Cave & Domaine Les Perrières à Satigny |
| HEAD, Conservatoire, Alhambra, Harmonie Nautique, UBS, Piaget, OMC, communes | Inchangés | Sites officiels | — |

## 4. Raisonnement juridique

### 4.1 Armoiries publiques : Ville de Genève, Collonge-Bellerive, Plan-les-Ouates (et l'Alhambra par assimilation)

**Constat.** Les trois signes officiels contiennent les **armoiries** de la collectivité : demi-aigle et clé pour la Ville de Genève, écusson communal pour Plan-les-Ouates et pour Collonge-Bellerive. Nous l'avons vérifié sur les fichiers de geneve.ch, plan-les-ouates.ch et collonge-bellerive.ch.

**Loi fédérale sur la protection des armoiries de la Suisse et des autres signes publics** (LPAP, RS 232.21, état au 1er juillet 2025) :
- Art. 8 al. 1 : « Les armoiries de la Confédération suisse, celles des cantons, des communes et des autres collectivités publiques reconnues par le droit cantonal, les éléments caractéristiques des armoiries cantonales en relation avec un écusson et les signes susceptibles d'être confondus avec eux **ne peuvent être utilisés que par la collectivité concernée**. »
- Art. 8 al. 3 : ces signes « ne peuvent pas faire l'objet d'une licence ni être transférés ».
- Art. 8 al. 4 : les exceptions (dictionnaire ou ouvrage de référence, décoration de fête, objets d'art appliqué, etc.) ne couvrent pas la publicité d'une entreprise.
- Art. 8 al. 5 : « Les cantons, les communes et les autres collectivités publiques reconnues par le droit cantonal peuvent admettre l'emploi de leurs armoiries par d'autres personnes dans d'autres cas. » Seule une **autorisation expresse** de la commune permettrait donc l'usage. Ce n'est pas l'usage prévu ici.
- Art. 10 : les autres emblèmes publics, c'est-à-dire sans armoiries, ne sont utilisables que si l'emploi n'est « ni trompeur, ni contraire à l'ordre public, aux bonnes mœurs ou au droit ». Un emblème municipal sur le site d'une entreprise laisse croire à un soutien officiel. C'est pourquoi l'**Alhambra** est traitée comme la Ville. Elle n'a pas de logo propre : son site utilise le signe « Sc – Scènes culturelles de la Ville de Genève » et le logo de la Ville.

Le droit genevois va dans le même sens : loi sur la dénomination, les armoiries et les couleurs de l'État (LArm, rsGE A 3 01). Selon l'État de Genève, des tiers peuvent utiliser certains éléments des armoiries cantonales (demi-aigle, clé, couleurs), mais sans l'écusson et seulement si l'emploi n'est pas trompeur. La Ville de Genève, de son côté, met son logo à disposition pour les **projets qu'elle subventionne**, pas pour la communication d'un fournisseur.

**Décision :** statut `protege`, aucun fichier, nom en texte. Citer le nom d'une collectivité comme maître d'ouvrage d'un chantier réel est une information factuelle, qui figure déjà sur l'ancien site. La lettre type (§7) permet malgré tout d'informer la commune et d'obtenir son accord sur la formulation.

### 4.2 Organisation internationale : OMC

- **Convention de Paris pour la protection de la propriété industrielle** (CUP, RS 0.232.04), art. 6ter, al. 1 let. b : la protection des armoiries et emblèmes d'État s'étend « aux armoiries, drapeaux et autres emblèmes, sigles ou dénominations des organisations internationales intergouvernementales ». Elle interdit leur usage comme marque ou élément de marque sans autorisation.
- **Loi fédérale concernant la protection des noms et emblèmes de l'Organisation des Nations Unies et d'autres organisations intergouvernementales** (LPNE, RS 232.23, état au 1er juillet 2023). Le droit suisse va **plus loin** que la Convention :
  - Art. 3 al. 1 : il est interdit d'utiliser, s'ils ont été communiqués à la Suisse par l'intermédiaire de l'OMPI, « a. le nom de ces organisations […] ; b. leurs sigles […] ; c. leurs armoiries, drapeaux et autres emblèmes ».
  - Art. 7 al. 1 let. b punit celui qui « appose de tels signes sur des enseignes, des annonces, des prospectus, des papiers de commerce, **des sites Internet** ». L'art. 8 prévoit la responsabilité solidaire de la société.
- Nous n'avons pas pu confirmer en ligne si les signes de l'OMC figurent dans la base **« Article 6ter Express »** de l'OMPI. Par prudence, nous partons du principe qu'ils y figurent.

**Décision :** statut `protege` : **jamais l'emblème**, même avec un accord oral. Pour le **nom « OMC »** en texte : demander l'accord écrit de l'OMC (lettre type, §7) avant la production. En attendant la réponse, la mention factuelle déjà publiée reste un risque faible. Si la réponse est négative, la retirer. La photo `IMG_1702`, où le logo OMC/WTO est visible, reste écartée (voir `selection-photos.md`).

### 4.3 Marques privées et institutions : `a_autoriser`

- **Loi sur la protection des marques** (LPM, RS 232.11), art. 13 al. 2 let. e : le titulaire peut interdire à des tiers d'apposer la marque « sur des papiers d'affaires, de l'utiliser à des fins publicitaires ou d'en faire usage de quelqu'autre manière dans les affaires ». Un bandeau de logos sur le site d'une entreprise est un usage publicitaire.
- **Droit d'auteur** (LDA, RS 231.1) : un logo figuratif (clés UBS, blason de Grisogono, emblème J. Safra Sarasin) peut être une œuvre protégée.
- **Loi contre la concurrence déloyale** (LCD, RS 241), art. 3 al. 1 let. b : agit de façon déloyale celui qui « donne des indications inexactes ou fallacieuses sur lui-même, son entreprise […] ou ses affaires ». Un logo présenté comme un « partenaire », ou sans lien avec un chantier réel, tomberait sous cette règle.
- « **Domaine public** » sur Wikimedia Commons (Piaget, Celgene) ne veut dire qu'une chose : le **dessin** n'atteint pas le seuil d'originalité du droit d'auteur. La **marque** reste protégée, et Commons l'indique lui-même (mention « trademarked »).
- Les fichiers **« fair use »** de Wikipédia (UBS, J. Safra Sarasin) relèvent d'une notion américaine sans équivalent en droit suisse. Ils servent **uniquement à la preview**. En production, utiliser le fichier fourni par l'entreprise avec son accord.
- Labcorp : le fichier Commons est publié sous **CC BY-SA 4.0** par son importateur, ce qui ne donne aucun droit sur la marque.

**Décision :** fichiers préparés et affichés en **preview** seulement. En **production**, un logo n'apparaît que lorsque son statut passe à `autorise`, après réception d'un **accord écrit** archivé. Sans accord, on affiche le nom en texte (les noms sont déjà publics sur l'ancien site).

### 4.4 Cas particuliers

- **De Grisogono** : l'accord devrait venir du titulaire actuel de la marque (De Grisogono Swiss SA, groupe Damac), qui n'a pas été client. Afficher son logo suggérerait une relation qui n'existe pas (LCD art. 3 al. 1 let. b). Recommandation : nom en texte, avec la date du chantier.
- **Celgene** : afficher le logo d'époque, et seulement avec l'accord de BMS. Ne jamais remplacer par le logo BMS.
- **Everness** : n'afficher le logo qu'une fois l'identité de l'hôtel confirmée par le client.

## 5. Traitement graphique

- **Couleurs** : graphite `#44494F` pour les fonds clairs (blanc, brume), blanc `#FFFFFF` pour le fond anthracite, avec une opacité gérée par CSS (0,7 conseillé). Les logos multicolores sont convertis en **tons d'un même gris**, pour garder leur lecture : disques Labcorp à 38 / 62 / 85 %, triangle de l'Harmonie Nautique à 45 %, couronne de Grisogono en gris moyen.
- **SVG** (Piaget, UBS, Celgene, Labcorp, Conservatoire, Everness) :
  - nettoyage en liste blanche : aucun `<script>`, gestionnaire `on*`, lien externe, `<style>`, `<image>`, métadonnées ou attribut Inkscape ou Sketch ;
  - remplissages recolorés, sans fond ;
  - `viewBox` recadré au plus près du dessin (mesuré par rendu) ;
  - identifiants internes préfixés (`labcorp-mask-2`…), sans risque de collision si un SVG est inséré dans la page.
  - Poids : 3 à 11 Ko.
- **PNG** (HEAD, J. Safra Sarasin, Energestion, Dipan, de Grisogono, Harmonie Nautique) : détourage, recadrage serré, **hauteur 120 px**, fond transparent, poids de 2 à 10 Ko (tous sous 15 Ko). À 120 px, la netteté est bonne jusqu'à environ 60 px affichés sur écran haute densité.
- **Contrôle visuel** : planches-contacts sur fond blanc, brume et anthracite, et simulation du bandeau avec les polices du site. Tous les logos sont lisibles et non déformés. Une limite : le sous-titre d'Energestion (« Ingénieurs-conseils SIA ») et le « Water Technology » de Dipan deviennent illisibles en petit, ce qui est normal pour un logo.
- **Échelle optique (`echelle`)** : multiplicateur de la hauteur de base. Il est calculé à partir de la proportion et de la densité d'encre de chaque logo (égalisation partielle), puis ajusté à l'œil. Les logos larges et denses sont réduits (Everness 0,55, Labcorp 0,80). Les logos compacts ou fins sont agrandis (Celgene et de Grisogono 1,35, J. Safra Sarasin 1,30).

Intégration CSS conseillée :

```css
.refs { list-style: none; display: flex; flex-wrap: wrap; align-items: center; gap: 24px 48px; --logo-h: 44px; }
.refs img { height: calc(var(--logo-h) * var(--e, 1)); width: auto; max-width: calc(var(--logo-h) * 4.6); }
.refs .nom { font: 600 1rem/1.25 var(--head); color: var(--grey); max-width: 16ch; } /* références sans logo */
.footer .refs { --logo-h: 32px; } .footer .refs img, .footer .refs .nom { opacity: .7; } /* versions -blanc */
@media (max-width: 599px) { .refs { --logo-h: 34px; gap: 20px 32px; } }
```

Chaque élément porte `style="--e: <echelle>"`. Le texte alternatif est `nom_affiche`. Pour éviter des coupures comme « Plan-les- / Ouates », utiliser des traits d'union insécables (U+2011) dans les noms composés au rendu.

## 6. Recommandations d'usage

**Où et combien**

| Emplacement | Contenu | Taille |
|---|---|---|
| Bandeau sous le héro (accueil) | **6 à 8** références, sélection fixe : Ville de Genève, Piaget, Conservatoire, UBS, HEAD, Collonge-Bellerive, J. Safra Sarasin, OMC | hauteur de base 44 px (34 px sur mobile), une ou deux lignes |
| Pied de page (toutes les pages) | 6 à 10 références en version **blanche à 70 %** | hauteur de base 32 px |
| Réalisations | **Liste complète** groupée par secteur (comme aujourd'hui), logo et nom, avec année et nature des travaux quand elles sont connues | 44 px |
| Prestations et Contact | 3 à 4 références pertinentes, par exemple les collectivités près du formulaire de devis | 40 px |

**Règles**
- Titre : « **Ils nous ont fait confiance** ». Jamais « Nos partenaires », « Ils nous recommandent » ni « Nos clients fidèles » : cela laisserait croire à un partenariat ou à une recommandation (LCD art. 3 al. 1 let. b).
- **Monochrome uniquement**, sans couleur au survol, **sans lien** vers les sites des références. Aucun logo ne doit ressembler à un bouton.
- **Grille fixe**, pas de carrousel ni de défilement automatique (`brief-design.md`).
- Le mélange de logos et de noms en texte est voulu et reste lisible : les noms sont en Montserrat 600, graphite.
- **Dater** chaque référence dès que le client a l'information (« réalisé en 20XX »), surtout pour les sociétés renommées.
- En production, ajouter sous le bandeau une ligne discrète : « Références citées avec l'accord des maîtres d'ouvrage ».
- Accessibilité : liste `<ul>`, `alt` = `nom_affiche`. Le contraste est suffisant : graphite sur blanc environ 9:1, blanc à 70 % sur anthracite environ 8,6:1.

**Générateur (preview / production)**
- **preview** : `fichier` pour `a_autoriser` et `autorise` ; nom en texte pour `protege` et `introuvable`.
- **production** : `fichier` seulement si `statut == "autorise"`, sinon `nom_affiche` en texte. Ne jamais afficher de fichier pour `protege`.
- À la réception d'un accord : passer `statut` à `autorise`, remplacer le fichier par celui fourni par l'entreprise s'il est meilleur, et archiver l'e-mail d'accord (date, signataire, périmètre). Si besoin, ajouter les champs `accord_date` et `accord_contact`.

## 7. Lettres types

### 7.1 Demande d'autorisation (logo et nom)

> **Objet : Autorisation de citer votre [nom / logo] parmi nos références – Andy Construct, Carouge**
>
> Madame, Monsieur,
>
> En [année], notre entreprise a réalisé pour vous [nature des travaux : faux-plafonds, cloisons, isolation acoustique, peinture] à [lieu / bâtiment].
>
> Nous préparons un nouveau site internet et souhaiterions mentionner [Nom de l'organisation] parmi les maîtres d'ouvrage qui nous ont fait confiance.
>
> Concrètement :
> - votre **logo**, en version monochrome grise, sans modification de ses proportions, figurerait dans un bandeau intitulé « Ils nous ont fait confiance » sur notre site andyconstruct.ch (accueil, page Réalisations, pied de page) ;
> - il ne comporterait **aucun lien** vers votre site et ne serait accompagné d'**aucune mention de partenariat** ni de recommandation ;
> - le cas échéant, le chantier serait décrit de façon factuelle (type de travaux, année), sans information confidentielle.
>
> Pourriez-vous nous indiquer par retour d'e-mail si vous acceptez :
> 1. ☐ l'affichage de votre logo et de votre nom ;
> 2. ☐ l'affichage de votre nom seulement, en texte ;
> 3. ☐ ni l'un ni l'autre.
>
> Si vous acceptez l'usage du logo, nous vous serions reconnaissants de nous transmettre le fichier officiel (SVG ou EPS de préférence) ou vos règles d'utilisation. Vous pourrez retirer votre accord à tout moment sur simple demande. Nous retirerons alors la mention dans un délai de 10 jours ouvrables.
>
> Nous restons à votre disposition pour toute question et vous remercions de votre confiance.
>
> Avec nos meilleures salutations,
>
> [Prénom Nom], [fonction]
> Andy Construct, Chanton & Cie – Route des Acacias 48, 1227 Carouge
> +41 22 771 20 15 – [adresse e-mail]

**Variante pour les collectivités et l'OMC** (le logo n'est pas demandé) : remplacer le premier point de la liste par « votre **nom**, en texte (par exemple « Ville de Genève », « OMC »), figurerait dans une liste intitulée « Ils nous ont fait confiance » ; nous n'utiliserons **ni vos armoiries ni votre emblème** ». Dans les choix proposés, supprimer l'option 1.

À qui écrire :
- entreprises : service communication ou marque, par l'intermédiaire de l'interlocuteur du chantier ;
- communes : secrétariat général de la mairie ;
- Ville de Genève : service de la communication ;
- OMC : Information and External Relations Division ;
- J. Safra Sarasin, UBS, Labcorp : communication Suisse ;
- Celgene : communication de Bristol Myers Squibb en Suisse ;
- Everness et Dipan : direction.

### 7.2 Variante : demande d'un court témoignage

> **Objet : Votre avis en deux ou trois phrases sur notre intervention**
>
> Madame, Monsieur,
>
> Vous nous avez confié en [année] [nature des travaux] à [lieu]. Votre avis compte beaucoup pour les régies, architectes et communes qui hésitent à faire appel à une petite entreprise comme la nôtre.
>
> Accepteriez-vous de nous écrire **deux ou trois phrases** sur notre travail ? Par exemple : le respect des délais, la propreté du chantier, la qualité des finitions, la communication. Vos mots seraient publiés **tels quels** sur notre site andyconstruct.ch, avec :
> - votre nom, votre fonction et le nom de votre organisation, **ou** seulement votre fonction et votre organisation, selon votre préférence ;
> - l'année et la nature des travaux.
>
> Nous ne modifierons pas votre texte sans votre accord. Si nous devons le raccourcir, nous vous soumettrons la version finale avant publication. Vous pourrez demander son retrait à tout moment.
>
> Si vous préférez, nous pouvons aussi en parler cinq minutes par téléphone. Nous vous enverrons ensuite une proposition de texte, que vous corrigerez et validerez par écrit.
>
> Avec nos remerciements et nos meilleures salutations,
>
> [Prénom Nom], [fonction] – Andy Construct, Chanton & Cie – +41 22 771 20 15

Règles pour les témoignages (programme §4, nLPD) :
- texte **authentique** et validé par écrit ;
- aucune note ni aucun « avis » inventé ;
- consentement explicite pour le nom, la fonction et toute éventuelle photo ;
- retrait possible à tout moment ;
- conserver l'e-mail de validation.

## 8. Sources

**Textes légaux (Fedlex, versions en vigueur)**
- LPAP, RS 232.21 : https://www.fedlex.admin.ch/eli/cc/2015/613/fr
- LPNE, RS 232.23 : https://www.fedlex.admin.ch/eli/cc/1962/455_461_475/fr
- LPM, RS 232.11 : https://www.fedlex.admin.ch/eli/cc/1993/274_274_274/fr
- LCD, RS 241 : https://www.fedlex.admin.ch/eli/cc/1988/223_223_223/fr
- Convention de Paris (art. 6ter), RS 0.232.04
- Base « Article 6ter Express » de l'OMPI : https://www.wipo.int/article6ter/fr

**Collectivités**
- Armoiries genevoises (LArm, rsGE A 3 01) : https://www.ge.ch/document/armoiries-republique-du-canton-geneve
- Logo de la Ville de Genève : https://www.geneve.ch/autorites-administration/administration-municipale/mise-disposition-logo

**Registre du commerce**
- Zefix : https://www.zefix.admin.ch (identifiants IDE cités au §3)

**Fichiers sources**
- Wikimedia Commons et Wikipédia : Piaget_logo.svg, Celgene_logo.svg, Labcorp_Logo_updated_12-2020.svg, UBS_Logo.svg (en.wikipedia), J._Safra_Sarasin_Logo.png (en.wikipedia)
- Sites officiels : cmg.ch, head.hesge.ch, energestion.ch, dipan.ch, everness.ch, harmonie-nautique.ch, degrisogono.com, alhambra-geneve.ch

**Changements de nom**
- Covance devenue Labcorp : avis de changement de nom de Labcorp (https://labcorp.com/content/dam/labcorp/files/certfications/Name%20change%20documentation.pdf)
- De Grisogono : Bloomberg, 31 mai 2022 ; Arabian Business, 2022
- Everness : everness.ch (« Best Western pendant 25 ans, quitté en 2020 »)

## 9. v3 : logos couleur officiels

État au 31 octobre 2026. Fichiers : `site/assets/img/references/couleur/<id>.svg|png`, déclarés dans `logos.json` (champs `fichier_couleur`, `couleur_dominante`, `source_couleur_url`). Les versions graphite et blanches de la v2 restent en place (`fichier`, `fichier_blanc`), notamment pour le pied de page sombre.

### 9.1 Décision du client et effet sur les statuts

- **Décision (31.10.2026)** : toutes les références s'affichent avec leur **vrai logo officiel, en couleur, bien visible**, y compris les collectivités. Plus de nom en texte à la place d'un logo quand un logo officiel existe.
- **Ville de Genève, Collonge-Bellerive, Plan-les-Ouates, Salle de l'Alhambra et OMC** passent de `protege` à **`a_autoriser`**. Leur `remarque` dans `logos.json` est désormais : « Logo officiel d'une collectivité publique (armoiries) / emblème d'organisation internationale : affichage en version de validation seulement ; publication en production uniquement avec l'autorisation écrite de l'institution (LPAP / Convention de Paris art. 6ter). »
- Le raisonnement juridique du §4 reste entièrement valable : **sans autorisation écrite, aucun de ces logos n'est publié**. La seule différence avec la v2 : le fichier est préparé, et la demande porte désormais sur le **logo** (armoiries ou emblème compris), plus seulement sur le nom.
- Rendu par le générateur : en **preview**, logo couleur pour `a_autoriser` et `autorise` ; en **production**, logo seulement si `statut == "autorise"`. Les fichiers des logos non autorisés (dossier `couleur/` compris) ne doivent pas être copiés dans le paquet de production.
- **Domaine des Perrières** reste `introuvable` (nom en texte) : aucun logo public. En ligne, « Domaine des Perrières » n'apparaît que comme nom d'une résidence dans une annonce immobilière à Coppet. lesperrieres.ch appartient à la Cave & Domaine Les Perrières de Satigny, sans lien.
- **De Grisogono** : le fichier couleur est prêt, mais la recommandation du §4.4 ne change pas (titulaire actuel de la marque ≠ client). Au client de trancher.

| Statut (v3) | Nombre | Références |
|---|---|---|
| `a_autoriser` | **17** | toutes, sauf Domaine des Perrières |
| `protege` | **0** | — |
| `introuvable` | **1** | Domaine des Perrières |
| `autorise` | **0** | à basculer au fil des réponses |

### 9.2 Fichiers, sources et réglages

Toutes les sources ont été relevées le 31 octobre 2026 sur le site officiel, dans l'en-tête ou la médiathèque. Wikimedia Commons ou Wikipédia n'ont servi que lorsque le site officiel ne donnait pas mieux.

| # | Référence | Fichier (`couleur/`) | Source | Couleur dominante | Échelle | Statut |
|---|---|---|---|---|---|---|
| 1 | Ville de Genève | `ville-de-geneve.svg` (32 Ko) | geneve.ch, SVG de l'en-tête (`themes/custom/vdg_theme/logo.svg`) | `#CC3333` (+ jaune `#FFCD00`, noir) | 1,40 | `a_autoriser` (ex-`protege`) |
| 2 | Piaget | `piaget.svg` (1 Ko) | piaget.com, sprite SVG de l'en-tête (symbole `#logo`), en noir comme sur fond clair | `#000000` | 0,95 | `a_autoriser` |
| 3 | Conservatoire de musique de Genève | `conservatoire-musique-geneve.svg` (7 Ko) | cmg.ch, SVG intégré (version couleur) | `#4C81C3` (+ noir) | 0,90 | `a_autoriser` |
| 4 | UBS | `ubs.svg` (5 Ko) | ubs.com, SVG de l'en-tête. Couleurs du thème clair du site : rouge `#DA0000` (UBS), noir `#1C1C1C` (clés) | `#DA0000` | 0,90 | `a_autoriser` |
| 5 | HEAD – Genève | `head-geneve.png` (8 Ko) | head.hesge.ch, PNG de l'en-tête (248 × 122 px, seule version publiée) | `#410099` | 0,95 | `a_autoriser` |
| 6 | Collonge-Bellerive | `collonge-bellerive.png` (18 Ko) | collonge-bellerive.ch, PNG couleur (770 × 120 px, seule version publiée) | `#E20913` (+ jaune, vert, gris) | 0,70 | `a_autoriser` (ex-`protege`) |
| 7 | J. Safra Sarasin | `j-safra-sarasin.png` (15 Ko) | Wikipédia en anglais (fichier « fair use », 432 × 231 px). jsafrasarasin.com a refusé nos connexions | `#011851` | 1,30 | `a_autoriser` |
| 8 | Salle de l'Alhambra | `alhambra.png` (23 Ko) | alhambra-geneve.ch, logotype « Alhambra » de l'en-tête (PNG 1112 × 185 px, noir) | `#0F0A07` | 0,70 | `a_autoriser` (ex-`protege`) |
| 9 | Labcorp (ex-Covance) | `labcorp.svg` (3 Ko) | Wikimedia Commons, identique au logo de labcorp.com (mêmes couleurs, vérifié) | `#4CD5F7` (+ bleus, noir) | 0,75 | `a_autoriser` |
| 10 | Plan-les-Ouates | `plan-les-ouates.svg` (4 Ko) | plan-les-ouates.ch, SVG de l'en-tête | `#FCC522` (+ bleu, rouge, noir) | 1,15 | `a_autoriser` (ex-`protege`) |
| 11 | Energestion | `energestion.png` (22 Ko) | energestion.ch, médiathèque : `Logo-Energestion-menu-1.png`, version couleur pour fond clair (500 × 200 px) | `#9ACC73` (+ gris) | 1,15 | `a_autoriser` |
| 12 | OMC | `omc.png` (15 Ko) | wto.org, logo français de l'en-tête (GIF 518 × 154 px, seule version publiée sur le site) | `#E2001D` (+ bleu, vert, jaune, noir) | 1,05 | `a_autoriser` (ex-`protege`) |
| 13 | de Grisogono | `de-grisogono.png` (10 Ko) | degrisogono.com, PNG 1280 × 504 px | `#B77B1B` (+ noir) | 1,30 | `a_autoriser` (texte seul recommandé, §4.4) |
| 14 | Harmonie Nautique de Genève | `harmonie-nautique.png` (9 Ko) | harmonie-nautique.ch, JPEG 1200 × 1697 px sur fond blanc | `#00FFFF` (+ noir) | 1,00 | `a_autoriser` |
| 15 | Everness Hotel & Resort | `everness.svg` (5 Ko) | everness.ch, SVG (version noire pour fond clair) | `#000000` | 0,55 | `a_autoriser` |
| 16 | Dipan | `dipan.png` (25 Ko) | dipan.ch, `logo-default-slim.png`, version pour fond clair (313 × 150 px) | `#0094D1` (+ vert, noir) | 1,35 | `a_autoriser` |
| 17 | Domaine des Perrières | — | aucun logo public | — | 1,00 | `introuvable` |
| 18 | Celgene | `celgene.svg` (5 Ko) | Wikimedia Commons, logo d'époque (marque absorbée par BMS en 2019) | `#26326F` | 1,35 | `a_autoriser` |

**Traitement**
- **SVG** (9 logos) :
  - même nettoyage en liste blanche qu'au §5 : aucun `<script>`, gestionnaire `on*`, lien externe, `<style>`, `<image>`, `<foreignObject>` ou métadonnée ;
  - **couleurs d'origine conservées** : les classes CSS (Plan-les-Ouates) et les variables CSS (UBS) sont converties en attributs `fill` ;
  - le masque sans effet de la Ville de Genève est supprimé, et les tracés de même couleur sont regroupés ;
  - `viewBox` recadré au plus près du dessin ;
  - nombres arrondis, avec un contrôle automatique : écart de rendu inférieur à 0,1 % par rapport à la pleine précision.
- **PNG** (8 logos) :
  - détourage par l'alpha d'origine, ou par « couleur vers alpha » pour les sources sur fond blanc (GIF de l'OMC, JPEG de l'Harmonie Nautique), ce qui garde des bords nets sans liseré blanc ;
  - recadrage serré, **240 px de haut**, fond transparent, 8 à 25 Ko (tous sous 30 Ko).
  - Six sources font moins de 240 px de haut et ont été agrandies : HEAD 122 px, Collonge-Bellerive 120 px, Energestion 134 px, Dipan 148 px, J. Safra Sarasin 149 px, OMC 154 px. Elles restent nettes jusqu'à environ 60 px affichés sur écran haute densité. Il faudra **demander le fichier vectoriel avec l'autorisation**.
- **`couleur_dominante`** : la teinte de marque la plus étendue, si elle couvre au moins 15 % de l'encre. Sinon, l'encre principale (noir, marine…).
- **`echelle`** : même méthode qu'au §5 (égalisation partielle, exposant 0,35). La densité d'encre est pondérée par la clarté de la couleur, car un jaune pèse moins qu'un noir.
  - Bornes 0,55 à 1,40. La largeur affichée ne dépasse jamais 4,6 fois la hauteur de base (la `max-width` du CSS), d'où 0,70 pour Collonge-Bellerive et l'Alhambra.
  - Ajustements à l'œil : Ville de Genève ×1,1 (plafonnée à 1,40 : texte très espacé et points jaunes clairs) et Plan-les-Ouates ×1,1.
- **Contrôle visuel** : planche-contact à 48 et 96 px de haut sur fond blanc, et bandeau simulé sur blanc et sur brume. Tous les logos sont nets, aux couleurs fidèles, sans déformation ni liseré.
  - Limites propres aux logos eux-mêmes : la mention « VILLE DE GENÈVE », très espacée, n'est lisible qu'à partir d'environ 60 px de haut. Le sous-titre d'Energestion, le « Water Technology » de Dipan et le « Commune de » de Collonge-Bellerive deviennent illisibles en petit.

**Règles d'usage (remplacent « Monochrome uniquement » du §6)**
- Logos **en couleur** sur fond clair. Pas de recoloration, pas de déformation, pas d'effet au survol.
- Sur le pied de page sombre : version blanche existante, ou logo couleur sur pastille blanche.
- Toujours **sans lien**, sous un titre factuel (« Ils nous ont confié des travaux »), jamais « partenaires ».
- Les fichiers bruts téléchargés (un dossier par logo) sont conservés hors du dépôt. Chaque SVG a été inspecté avant traitement.

### 9.3 Démarche d'autorisation : collectivités et OMC

Pour ces cinq institutions, la loi réserve l'usage du signe à l'institution elle-même (LPAP art. 8 al. 1 pour les armoiries, art. 10 pour les autres signes publics ; Convention de Paris art. 6ter et LPNE art. 3 pour l'OMC). Seule une **autorisation écrite et expresse** (LPAP art. 8 al. 5) permet la publication.

| Institution | Signe | À qui écrire | Remarques |
|---|---|---|---|
| **Ville de Genève** | logo avec armoiries (demi-aigle et clé) | **Service des relations extérieures et de la communication**, Unité information et communication, rue du Tir 3, 1204 Genève, +41 22 418 59 43 (formulaire « Contact » de geneve.ch) | La Ville réserve son logo aux projets qu'elle subventionne ou soutient (page « Mise à disposition du logo »). L'accord pour un fournisseur n'est pas acquis : prévoir un refus. |
| **Salle de l'Alhambra** | logotype « Alhambra » (sans armoiries) | Alhambra, rue de la Rôtisserie 10, 1204 Genève, coordination@alhambra-geneve.ch, **copie** au Service des relations extérieures et de la communication de la Ville | Salle municipale (Département de la culture et de la transition numérique) : la Ville doit être d'accord. |
| **Commune de Collonge-Bellerive** | logo avec écusson communal | **Mairie**, à l'attention du secrétariat général, chemin du Château-de-Bellerive 1, 1245 Collonge-Bellerive, 022 722 11 50, info@collonge-bellerive.ch | L'autorisation relève de l'exécutif communal (Conseil administratif) : demander une réponse signée par lui ou par son délégataire. |
| **Commune de Plan-les-Ouates** | logo avec écusson communal | **Mairie**, secrétariat général (service Communication et médias), route des Chevaliers-de-Malte 3, case postale 17, 1228 Plan-les-Ouates, +41 22 884 64 00, mairie@plan-les-ouates.ch | Idem : réponse du Conseil administratif ou de son délégataire. |
| **OMC** | emblème et nom « Organisation mondiale du commerce » | **enquiries@wto.org**, en demandant la transmission à la **Division des affaires juridiques** | Selon wto.org (« Droit d'auteur et autorisations »), le logo, nom et acronyme compris, ne peut être utilisé par des tiers que « dans des circonstances exceptionnelles », avec autorisation écrite préalable, en général pour des événements ou publications communs. **Refus probable.** La LPNE protégeant aussi le nom et le sigle, demander dans le même courrier l'accord pour le nom en texte. |

**Étapes**
1. Envoyer la lettre type du §7.1, en remplaçant le premier point par la variante ci-dessous. Elle est signée par un associé et accompagnée de :
   - une capture du bandeau en version de validation, logo à la taille réelle ;
   - la liste des pages concernées ;
   - l'année et la nature du chantier.
2. Demander explicitement :
   - l'autorisation écrite d'utiliser le logo (armoiries ou emblème compris) sur andyconstruct.ch, et son périmètre (pages, durée, révocation) ;
   - le fichier officiel et la charte graphique ;
   - le nom et la fonction du signataire compétent.
3. À la réception :
   - archiver l'e-mail ou la lettre (date, signataire, périmètre) ;
   - passer `statut` à `autorise` dans `logos.json` et ajouter `accord_date` et `accord_contact` ;
   - remplacer le fichier par le fichier officiel reçu s'il est meilleur.
4. Sans réponse après 30 jours, relancer une fois. En cas de refus ou de silence, laisser `a_autoriser` : le logo n'est pas publié en production. Pour l'OMC, retirer aussi le nom en cas de refus.

**Variante de la lettre type (collectivités et OMC, logo demandé)** : remplacer le premier point de la liste par :
> - votre **logo officiel**, en couleur, sans aucune modification, figurerait dans un bandeau intitulé « Ils nous ont confié des travaux » sur notre site andyconstruct.ch (accueil, page Réalisations, pied de page). Comme il comporte vos [armoiries / votre emblème], dont l'usage vous est réservé par la loi (LPAP art. 8 / Convention de Paris art. 6ter), nous ne le publierons qu'avec votre **autorisation écrite** ;

et garder les trois choix (logo et nom ; nom seulement ; ni l'un ni l'autre).

### 9.4 Sources (v3)

- Ville de Genève, logo : https://www.geneve.ch/themes/custom/vdg_theme/logo.svg ; conditions : https://www.geneve.ch/autorites-administration/administration-municipale/mise-disposition-logo ; contact communication : https://www.geneve.ch/propos/credits
- Plan-les-Ouates : https://www.plan-les-ouates.ch/sites/all/themes/pmbcom/dist/images/logo.svg ; Collonge-Bellerive : https://www.collonge-bellerive.ch/ (`dist/collonge-bellerive/2023/images/logo-color…png`) ; Alhambra : https://www.alhambra-geneve.ch/wp-content/themes/sc/img/Alhambra.png
- OMC, logo : https://www.wto.org/images/wtomenus/logo_fr.gif ; conditions d'usage : https://www.wto.org/french/info_f/copyrights_permissions_f.htm
- Entreprises et institutions : piaget.com (`pia/dist/assets/icons.svg`), ubs.com (`ubs-logo-type-logo-and-name…svg`), cmg.ch, head.hesge.ch, energestion.ch (`wp-content/uploads/2023/08/Logo-Energestion-menu-1.png`), dipan.ch (`img/logo-default-slim.png`), harmonie-nautique.ch, everness.ch, degrisogono.com ; Wikimedia Commons (Labcorp, Celgene) ; Wikipédia en anglais (J. Safra Sarasin). URL exactes : champ `source_couleur_url` de `logos.json`.
