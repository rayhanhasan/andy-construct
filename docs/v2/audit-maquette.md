# Audit de la maquette v1 — Andy Construct

Phase 1 du programme v2 (`docs/v2/programme-v2.md`). Auditeur UX / CRO / accessibilité / performance / SEO technique.
Date : 31 octobre 2026. Référence auditée : `site/` au commit `ec5f98d` (mode preview, `noindex`).
Aucun fichier de `site/` ni de `tools/` n'a été modifié.

**Méthode outillée.** Site servi en local (`python3 -m http.server`). Captures pleine page Playwright/Chromium en 1440 et 390 px de toutes les pages, plus 768, 1024 et 1280 px pour l'en-tête. Toutes les captures ont été relues. Tests interactifs : menu mobile, formulaire vide puis rempli, visionneuse, filtres. axe-core 4.14.0 injecté sur 6 pages en 1440 et 390 px. Lighthouse 12.8.2 en mobile (débit simulé « slow 4G ») sur 4 pages, puis un second passage de l'accueil avec un serveur qui compresse. Le nombre de mots, les lignes à 390 px, les tailles de police calculées et les cibles tactiles ont été mesurés par script dans le navigateur. Les titres, les balises meta, les niveaux de titre, le JSON-LD (parsé), les liens, les alt, le sitemap, robots.txt et llms.txt ont été analysés par script.

**Conditions à garder en tête.** (1) En mode preview, la balise `noindex` est voulue : le score SEO Lighthouse de 69 vient de là. (2) `python3 -m http.server` n'envoie ni compression ni en-tête de cache : les audits Lighthouse « text compression » et « cache » sont donc des artefacts du serveur local. Leur effet est mesuré à part (§ Annexe B).

---

## 1. Synthèse

1. La base est saine : charte respectée, HTML et CSS natifs, aucun service tiers, téléphone toujours visible, Lighthouse a11y 100 et performance 93 à 99, CLS nul. **On améliore, on ne refait pas.**
2. Le portfolio, c'est le problème n° 1. Selon `manifest.json`, **14 photos sur 30 sont des plafonds tendus ou métalliques**, et `tools/build/common.py` les **renomme en « faux-plafond / placo »**. Le héro, l'image OG et 2 des 3 images du JSON-LD sont dans ce cas.
3. **Aucune photo de peinture, aucune de cloison isotherme.** Le filtre « Isolation acoustique » ne montre que des panneaux absorbants, que la page Prestations déclare elle-même inefficaces contre le bruit.
4. **Les 3 témoignages de l'accueil sont fictifs.** « Devis gratuit » et « 300+ chantiers » ne sont pas confirmés. Les trois vont contre la règle n° 1 du programme et contre la LCD.
5. Il y a trop de texte, et c'est mesuré : **1 298 mots visibles sur l'accueil, plus 399 mots dans la FAQ**. On compte 19 paragraphes de plus de 3 lignes à 390 px. « Suisse romande » revient 12 fois, « Carouge » 13 fois, « 2007 » 7 fois.
6. Le parcours mobile est trop long : **la section Devis commence à 14 672 px, soit 17,4 écrans**, et le formulaire lui-même à 15 500 px. Les prestations n'arrivent qu'au 5e écran. La page compte 11 sections, dont 3 redondantes (Engagements, Zone, liste des références). Entre le héro et le formulaire, aucun appel à demander un devis dans le contenu.
7. Aucune réassurance au point de conversion : pas de délai de réponse, pas de « sans engagement », pas d'interlocuteur nommé, pas de preuve sociale à côté du formulaire. La page Prestations, celle où l'intention d'achat est la plus forte, ne contient **aucune** preuve sociale.
8. La preuve sociale existe (18 références publiques, un vrai atout) mais elle tient en une liste de noms en texte. Elle n'est reliée à aucun projet et absente des pages Prestations et Contact ainsi que du pied de page.
9. SEO : les bases techniques sont bonnes (JSON-LD valide, FAQPage, llms.txt, NAP constant). Mais il n'y a **qu'une URL pour les 4 services**, et aucune page entreprise, zone, professionnels ou projet : le site ne peut pas se positionner sur « faux-plafond Genève » ni sur « isolation phonique Lausanne ».
10. Lisibilité senior : la base de 18 px est respectée, mais les **surtitres, étiquettes et titres de pied sont en 14 px** et le texte des cartes en 17 px gris. Le jargon (SIA, AEAI, CFC, « désolidarisé ») est mélangé au discours grand public.

### Scores par axe (sur 10)

| Axe | Note | Justification |
|---|---|---|
| UX | **6** | Navigation claire, fil d'Ariane, visionneuse et menu accessibles. Mais accueil de 11 sections (18 147 px en mobile), blocs dupliqués (zone, méthode, références), lien « L'entreprise » qui mène à une ancre de l'accueil, vignettes de 167 px en mobile. |
| CRO | **5** | Téléphone visible en permanence, CTA répétés, type de travaux pré-rempli depuis les prestations. En revanche : formulaire au 17e écran mobile, aucune réassurance ni preuve au point de conversion, témoignages fictifs, 5 libellés de CTA différents, case de consentement obligatoire, aucune option « rappel rapide ». |
| Accessibilité | **8** | axe : 0 violation sur 4 pages sur 6 ; Lighthouse a11y 100 ; focus, messages d'erreur et `<dialog>` corrects. Reste : 30 nœuds `label-content-name-mismatch` (galerie), textes en 14 px, liens de pied hauts de 38 px, double `<label>` sur le champ fichier, contraste du « 404 ». |
| Performance | **8** | Score mobile 93 à 99, CLS 0, JS 11 Ko et CSS 39 Ko (dans le budget). Mais LCP de l'accueil à 2,7 s pour un objectif de 2,5 s (2,4 s avec compression). Logo de 37 Ko et PNG de 77 Ko dans la carte. Vignettes de 800 px pour 167 px affichés (−297 Kio sur Réalisations). |
| SEO technique | **5** | Titles et metas uniques, JSON-LD valide (LocalBusiness, FAQPage, Breadcrumb), canonical, llms.txt, robots, NAP constant. Mais 4 services sur une seule URL, aucune page locale ni projet ni entreprise, titles accueil/prestations quasi identiques, alt longs et réécrits, `sameAs` qui pointe vers l'ancienne adresse. |
| Lisibilité senior | **6** | Base 18 px, interligne 1,6, 68 caractères par ligne, contrastes élevés, cibles de 52 px dans le formulaire. Mais ≈ 50 mots par page en 14 px majuscules espacées, ≈ 700 mots de l'accueil sous 18 px, jargon technique, réponses de FAQ de 6 à 10 lignes, vignettes trop petites. |
| **Global** | **6,3** | Une maquette propre et conforme, mais encore une **vitrine** plutôt qu'un **site d'acquisition**. |

---

## 2. Chiffres clés mesurés

| Mesure | Accueil | Prestations | Réalisations | Contact |
|---|---|---|---|---|
| Mots visibles (390 px) | 1 298 (+399 dans la FAQ fermée) | 999 | 554 | 473 |
| Hauteur de page 390 px / 1440 px | 18 147 / 10 719 px | 11 469 / 6 949 px | 9 310 / 5 768 px | 6 059 / 3 618 px |
| Équivalent en écrans mobiles (844 px) | 21,5 | 13,6 | 11,0 | 7,2 |
| Paragraphes > 3 lignes à 390 px | 19 | 17 | 4 | 1 |
| Liens vers devis / offre / demande | 6 | 9 | 5 | 5 |
| Liens `tel:` | 11 | 7 | 8 | 11 |
| Position du formulaire | 390 px : section 14 672 px, formulaire 15 500 px (18,4 écrans) ; 1440 px : section 8 865 px (9,8 écrans) | lien vers contact | lien vers contact | 1440 px : 767 px (1er écran) ; 390 px : 1 647 px (2e écran) |
| 1er CTA dans le contenu, hors héro (1440 / 390 px) | aucun avant le formulaire | « Demander une offre » : 1 901 / 2 667 px | « Transmettre un dossier » : 4 865 / 7 069 px | « Envoyer ma demande » : 1 601 / 2 795 px |
| Mentions de références (noms) | liste de 18 + 3 rappels | **0** | liste de 18 | **0** (un lien) |

Positions des sections de l'accueil à 390 px : héro 157 · références 991 · entreprise 2 169 · **prestations 3 853** · réalisations 5 567 · méthode 8 210 · engagements 9 369 · témoignages 10 582 · zone 11 656 · FAQ 13 422 · **devis 14 672**.

---

## 3. Tableau des constats

Priorité : **P1** = bloquant pour la conversion, pour la crédibilité ou pour une règle non négociable ; **P2** = gain important ; **P3** = finition.

| # | Page / section | Constat (factuel, chiffré) | Impact | Prio. | Recommandation concrète |
|---|---|---|---|---|---|
| 1 | Réalisations, accueil, héro, OG, JSON-LD | 14 photos sur 30 sont classées `plafonds-tendus` (11) ou `plafonds-metalliques` (3) dans `manifest.json`. Le générateur les met sous « Placo et faux-plafonds » et réécrit titres et alt (`common.py`, `GROUPE`, `TITRES`, `alt()` : « plafond tendu » devient « faux-plafond »). Le héro, l'image OG et 2 des 3 images du JSON-LD sont des plafonds tendus. | Un architecte reconnaît un plafond tendu ou à lames : perte de crédibilité immédiate. Contraire à la règle §4 du programme (« aucune invention présentée comme vraie »). | **P1** | Faire trancher le client (HANDOFF §9.4) : retirer ces photos, ou les regrouper sous « Autres réalisations (hors offre actuelle) » avec leur **légende exacte**. Supprimer les réécritures `TITRES` et `alt()`. Prendre pour le héro une photo de placo ou de peinture (ex. `faux-plafond-placo-gorge-lumineuse-01`). |
| 2 | Réalisations, Prestations | 0 photo de peinture, 0 photo de cloison isotherme. Le filtre « Cloisons » (2) montre des **cloisons vitrées modulaires**, qui ne font partie d'aucun des 4 services. La section « Cloisons isothermes » est illustrée par un plafond (« Ossature et isolation avant fermeture »). | Les deux services qui parlent le plus aux particuliers n'ont aucune preuve visuelle. | **P1** | Shooting de 3 à 4 chantiers en cours (peinture, cloison isotherme, doublage acoustique), avec avant/après. Filtres alignés sur les 4 services. Masquer automatiquement un filtre sans photo. |
| 3 | Réalisations, Prestations › Isolation acoustique | Les 4 photos « Isolation acoustique » sont des panneaux absorbants ou des dalles. Or la page Prestations dit : « un panneau absorbant réduit l'écho dans la pièce, mais pas le bruit qui vient d'un autre logement ». | Le site se contredit, et les acousticiens et architectes le verront. | **P1** | Classer ces photos sous « Correction acoustique (absorption) », ou les remplacer par des photos de doublage ou de cloison acoustique ouverte (laine visible, ossature désolidarisée). |
| 4 | Accueil › Témoignages | 3 témoignages aux profils génériques **fictifs** (commentaire `PROVISOIRE` dans `index.html` l. 550). | Faux avis : règle §4 du programme et LCD. Si le visiteur s'en rend compte, toute la page perd sa crédibilité. | **P1** | Dans `tools/build`, masquer le bloc tant que la liste de témoignages réels est vide. Recueillir 2 ou 3 témoignages avec accord écrit (nom, fonction, organisation, année). |
| 5 | Héro, barre mobile, figures | « Devis gratuit » (fait du héro, bouton de la barre mobile, sous-texte) et « 300+ chantiers réalisés » sont marqués `PROVISOIRE`. | Allégation commerciale non confirmée (LCD), visible en permanence sur mobile. | **P1** | Obtenir une confirmation écrite du client, sinon retirer. Libellé de la barre mobile : « Demander un devis ». |
| 6 | Accueil (mobile) | Section Devis à 14 672 px (17,4 écrans), formulaire à 15 500 px, prestations à 3 853 px (4,6 écrans), page de 18 147 px en 11 sections. Aucun lien de devis dans le contenu entre le héro et le formulaire : seuls l'en-tête et la barre fixe relancent. | La plupart des visiteurs n'atteignent jamais le formulaire ni les prestations. | **P1** | Passer à 7 sections (voir chantier C) : héro et bandeau de références, prestations, 3 projets, méthode (fusionnée), zone courte, FAQ courte, devis. Objectif ≤ 10 écrans mobiles, prestations au 2e écran. Un lien « Demander un devis » sous Prestations et sous Projets. |
| 7 | Accueil, tout le texte | 1 298 mots visibles + 399 dans la FAQ. 19 paragraphes > 3 lignes à 390 px. « Suisse romande » ×12, « Carouge » ×13, « 2007 » ×7, « 18 » ×4. | Plainte explicite du client. Lecture rapide impossible. | **P1** | Viser ≈ 650 mots visibles (−50 %). Une idée par bloc, au plus 2 lignes à 390 px. Voir § 5 « Texte à couper ». |
| 8 | Formulaire (accueil + contact) | Aucune réassurance au point de conversion : pas de délai de réponse, pas de « sans engagement », pas d'interlocuteur nommé, pas de preuve à proximité. Message de succès : « votre demande est bien prête… nous vous recontactons rapidement » (formule vague). | Le doute est le plus fort au moment de laisser ses coordonnées, surtout chez les 45-70 ans. | **P1** | Sous le bouton, 3 puces : « Réponse sous [délai à confirmer] jours ouvrables · Sans engagement · Vos données ne servent qu'à votre demande ». Au-dessus du formulaire, une ligne de références (« Ville de Genève, HEAD, Conservatoire… »). Nom de l'associé qui rappelle (avec son accord). Message de succès : « Merci [Prénom], votre demande est bien envoyée. [Nom] vous rappelle sous [délai]. » |
| 9 | Prestations | 0 référence, 0 témoignage, 0 projet cité sur 999 mots. La section Peinture n'a ni photo ni lien vers des réalisations. | La page où l'intention d'achat est la plus forte est aussi celle qui rassure le moins. | **P1** | Pour chaque service : 1 projet illustré (photo + 3 lignes) et « Réalisé notamment pour : X, Y », à condition que ce soit vrai et validé par le client. |
| 10 | SEO, arborescence | Les 4 services tiennent sur une URL (`prestations.html#placo`…). Pas de page entreprise (la nav mène à `index.html#entreprise`), pas de page zone ou canton, pas de page professionnels, pas de fiches projet. Sitemap de 5 URL. Le concurrent Edelweiss a une page par service et par ville (`analyse-marche.md`). | Invisible sur les requêtes service + ville (« faux-plafond Genève », « isolation phonique Lausanne », « plâtrier peintre Carouge »). | **P1** | Arborescence v2 : 4 pages services, `entreprise`, `professionnels`, `zone-intervention` (+ cantons quand un chantier réel existe), fiches projet. Voir chantier B. |
| 11 | Formulaire | `action="#"`, pas d'`enctype` pour la pièce jointe, succès simulé en JS. | Bloquant pour la production (déjà connu, programme phase 2). | **P1** | Endpoint (`site/api/`), accusé de réception automatique, suivi de l'événement d'envoi. Afficher le succès seulement si `res.ok`. |
| 12 | Accueil › Références | Liste de 18 noms en 2e section : 1 177 px à 390 px (1,4 écran) avant les prestations. Aucun logo, aucun nom relié à un projet. | Une preuve forte, mais posée trop tôt et trop longue : elle repousse l'offre. | P2 | Remplacer par un **bandeau d'une ligne** sous le héro : 6 à 8 logos `autorise` ou noms typographiques (armoiries publiques et OMC en texte, voir programme §4) + « Voir les 18 références ». |
| 13 | Accueil › Engagements + Méthode | Engagements (113 mots) : 4 items sur 6 répètent d'autres blocs (2007/Carouge, références, Suisse romande, offre en CHF). « Un chantier protégé » répète l'étape 3 de la méthode. | Redondance, longueur. | P2 | Fusionner en un bloc « Comment nous travaillons » : 4 étapes, une ligne chacune, avec les 2 engagements utiles intégrés (offre poste par poste, chantier protégé et nettoyé). |
| 14 | Accueil et Contact › Zone | Section identique sur les 2 pages (141 mots, 40 communes, carte SVG de 28 Ko en ligne). | Duplication, longueur, contenu dupliqué pour le SEO. | P2 | Accueil : 1 phrase + carte. Contact : 1 ligne + lien. Liste complète des communes sur une page Zone (utile au SEO local). |
| 15 | Méthode | 4 étapes sur l'accueil, 6 sur la page Prestations (« Planning » et « Nettoyage » en plus). | Incohérence (Nielsen n° 4). | P2 | Une seule méthode en 4 étapes, réutilisée partout depuis `content.py`. |
| 16 | CTA, toutes pages | 5 libellés pour la même action : « Demander un devis », « Demander une offre », « Devis gratuit », « Nous écrire », H1 « Contact et demande d'offre ». | Le visiteur senior se demande si ce sont des démarches différentes. | P2 | Un seul terme partout, « Demander un devis » (le mot du métier côté particulier), et « Envoyer ma demande » pour le bouton du formulaire. |
| 17 | Formulaire | 9 champs, dont 4 obligatoires (nom, téléphone ou e-mail, type de travaux, case d'accord). La case de consentement est obligatoire. | Friction. Cette case n'est pas exigée par la nLPD pour répondre à une demande : le devoir d'informer (art. 19 nLPD) suffit. **À faire valider par le juriste.** | P2 | Remplacer la case par une mention d'information sous le bouton. Proposer, à côté, un **« Rappel rapide »** : nom + téléphone + créneau (matin / après-midi). |
| 18 | Réalisations › Galerie | Grille plate de 30 vignettes carrées : 167 × 167 px à 390 px, ≈ 280 px à 1440 px. Sur mobile, la catégorie est masquée. Aucun lieu, aucune année, aucun client, aucune contrainte. 5 quasi-doublons (îlots lumineux). | Le portfolio ne raconte rien, et les vignettes sont trop petites pour des yeux de 60 ans. | P2 | Fiches projet et grille aérée, voir § 6. |
| 19 | Réalisations | Aucun lien entre un nom de référence et un projet, ni entre une photo et une prestation. « Dossier PDF disponible sur demande », mais pas téléchargeable. | Maillage faible et friction pour les pros. | P2 | Relier chaque référence à la fiche projet correspondante quand il y en a une. Mettre le PDF en téléchargement direct (livrable phase 3). |
| 20 | Réalisations › « Pour les architectes, régies et collectivités » | Le bloc le plus utile aux pros est en fin de page (≈ 4 900 px en desktop) et cite seulement les CFC 271 et 285 (HANDOFF cite aussi le 283, faux-plafonds). | Le public B2B, la cible principale, ne le trouve pas. | P2 | Page « Professionnels » dédiée, liée depuis la nav ou le pied (CFC, travail sur plans, dossier PDF, attestations à fournir). Vérifier le CFC 283 avec le client. |
| 21 | Navigation | Depuis chaque page, « L'entreprise » renvoie au milieu de l'accueil (`index.html#entreprise`). | Rupture de contexte (Nielsen n° 2 et 4). | P2 | Créer une page Entreprise : associés (avec leur accord), historique depuis 2007, RC/IDE, assurances (à fournir), équipe. |
| 22 | Lisibilité, typo | Surtitres, `.tag`, `.label`, titres de pied et « Appelez-nous » en **14 px** (`--fs-xs: .875rem`), majuscules espacées de 0,18em : ≈ 50 mots par page. | Contraire à la charte §4 (aucun texte < 16 px). Pénible à lire passé 60 ans. | P2 | `--fs-xs: 1rem` et espacement à 0,12em. |
| 23 | Lisibilité, typo | Texte des cartes (services, étapes, engagements, zones, légendes) en 17 px gris (`--fs-card`). Notes, aides et texte du formulaire en 16 px : ≈ 700 mots de l'accueil sous 18 px. | La charte vise 18 px pour le texte courant. | P2 | `--fs-card: 1.125rem`. Notes `.svc__note` à 1.125rem. |
| 24 | Rédaction | Jargon dans le discours grand public : « doublage », « ossature », « désolidarisé », « retombées », « parement », « impression », « trappes de visite », « SIA 181/180/118 », « AEAI », « CFC », « maîtres d'ouvrage », « second œuvre ». | Les particuliers décrochent. | P2 | Accueil et haut des pages services en mots simples (« un mur doublé pour l'isoler »). Le vocabulaire normatif va dans un encadré « Pour les professionnels » ou sur la page Professionnels. |
| 25 | Performance › Accueil | LCP 2,7 s en mobile simulé, pour un objectif programme < 2,5 s. Délai de rendu 1,99 s : CSS bloquant de 39 Ko non minifié (19 Ko inutilisés sur l'accueil), HTML de 81 Ko non compressé. Avec compression (`serve`) : LCP 2,4 s, score 97. | Juste à la limite de l'objectif. | P2 | Compression gzip/brotli et cache long sur l'hébergeur (`.htaccess`). Minifier le CSS au build et mettre en ligne le CSS critique du héro. |
| 26 | Performance, toutes pages | Logo de l'en-tête en WebP de 37 Ko pour un affichage d'environ 175 × 63 px. La cartouche de la carte charge le PNG de 77 Ko (accueil, contact). | 114 Ko inutiles sur les pages clés. | P2 | Vectoriser le logo en SVG (≈ 5 Ko). Faire pointer `<image>` de `carte.py` vers ce SVG ou vers le WebP. |
| 27 | Performance › Réalisations | 23 images (520 Ko) au chargement mobile. Vignettes en 800w pour 167 px affichés (Lighthouse : −297 Kio, « image delivery » −354 Kio). | Données mobiles gaspillées. | P2 | Ajouter une variante 400w et corriger `sizes`. Charger en paresseux tout ce qui est sous la 2e rangée. |
| 28 | A11y › Galerie | 30 boutons dont le nom accessible (« Agrandir la photo : <titre> ») n'inclut pas la catégorie visible : `label-content-name-mismatch`, WCAG 2.5.3, impact sérieux, à ≥ 760 px. | Les utilisateurs de commande vocale ne peuvent pas activer les boutons. | P2 | Retirer l'`aria-label`, garder le texte visible et ajouter `<span class="visually-hidden">Agrandir : </span>` avant le titre. |
| 29 | SEO › Titles | Accueil « Placo, peinture, isolation · Genève \| Andy Construct » (52 car.) et Prestations « Placo, peinture, isolation · Suisse romande \| Andy Construct » (60 car.) : quasi identiques. | Cannibalisation. | P2 | Accueil : « Plâtrier-peintre à Carouge · Suisse romande \| Andy Construct ». Les pages services portent chacune leur mot-clé. |
| 30 | SEO › Alt | Alt de 17 à 18 mots en moyenne, 27 au maximum (brief SEO : 5 à 15). Ils sont réécrits (« plafond tendu » devient « faux-plafond »). | Description inexacte (règle §4) et dilution. | P2 | Alt de 8 à 12 mots, exacts, sans réécriture : type d'ouvrage + lieu générique. |
| 31 | SEO › NAP | Le `sameAs` du JSON-LD pointe vers search.ch à l'**ancienne adresse** (avenue de Bel-Air 57, Chêne-Bourg). E-mail en `@bluewin.ch`. | Incohérence NAP entre le site et les annuaires. L'adresse bluewin fait moins sérieux auprès des pros. | P2 | Retirer ce `sameAs` jusqu'à la mise à jour de l'annuaire. Adresse `contact@andyconstruct.ch` (HANDOFF §3). |
| 32 | Mobile, vue | En-tête collant de 77 px + barre fixe de 68 px = 145 px (17 % des 844 px), plus le bandeau de maquette de 80 px en preview. Au 1er écran, 4 CTA sont visibles (2 dans le héro, 2 dans la barre). | Zone de lecture réduite. | P3 | Réduire l'en-tête au défilement (logo à 40 px), ou n'afficher la barre fixe qu'une fois le héro dépassé (IntersectionObserver, sans animation). |
| 33 | Accueil › Héro | Le sous-titre répète le H1 (« Placo · Peinture · Isolation. » juste sous « Placo, peinture et isolation… »). La 4e prestation n'est pas nommée. | Il reste peu de place pour ce qui distingue l'entreprise. | P3 | Sous-titre qui dit l'avantage, voir § 5. |
| 34 | 404 | Le « 404 » décoratif est en #E2E3E5 sur blanc, 1,28:1 (axe `color-contrast`). | Violation formelle. | P3 | `aria-hidden="true"` sur le chiffre, ou couleur graphite. |
| 35 | Formulaires | Le champ fichier a 2 `<label>` (`form-field-multiple-labels`). Aucune taille maximale annoncée. | Annonce confuse, échecs d'envoi possibles. | P3 | `aria-labelledby` unique. Aide : « PDF, JPG ou PNG, [10] Mo maximum ». |
| 36 | Pied de page, liens dans le texte | Liens du pied hauts de 38 px (charte : 48). Liens `tel:` dans le texte : 22 à 25 px. | Cibles petites au doigt. | P3 | `min-height: 48px` sur les listes du pied. Padding vertical sur les liens de téléphone isolés. |
| 37 | Carte (390 px) | Sur mobile, seule l'étiquette « Siège — Carouge » est visible ; les villes ne sont plus que des marqueurs « A ». | La carte perd son sens sur téléphone. | P3 | Afficher au moins Genève, Lausanne, Neuchâtel, Fribourg, Sion, ou une légende sous la carte. |
| 38 | Contact › colonne gauche | Téléphones listés 2 fois (« Nous appeler » puis « Adresse »), horaires 2 fois. | Bruit. | P3 | Un bloc « Appeler » (bureau, mobile, horaires) et un bloc « Adresse », sans doublon. |
| 39 | Prestations › surtitres | Les surtitres « Plâtrerie », « Finitions », « Confort acoustique », « Isolation thermique » ne correspondent pas aux noms des services. | Deux noms pour une même chose. | P3 | Supprimer ces surtitres, ou y mettre le bénéfice (« Moins de bruit »). |
| 40 | FAQ (accueil) | 9 questions, réponses de 29 à 50 mots, soit 6 à 10 lignes à 390 px. | Mur de texte une fois les réponses ouvertes. | P3 | 5 questions sur l'accueil, réponses ≤ 35 mots. Les questions métier vont sur chaque page service (FAQPage par page). |
| 41 | Meta | Description de l'accueil à 164 caractères (tronquée). | Extrait tronqué. | P3 | ≤ 155 caractères. |
| 42 | Sitemap | `lastmod` figé au 2026-09-25, pas de sitemap images, 5 URL. | Faible signal de fraîcheur. | P3 | `lastmod` généré au build et `image:image` pour les fiches projet. |
| 43 | Icônes des services | Les pictogrammes Placo (rails) et Cloisons isothermes (zigzag) ne se comprennent pas seuls. | Faible, car toujours accompagnés d'un titre. | P3 | Les garder, mais jamais seuls (charte §4). |

---

## 4. Conversion (CRO)

### 4.1 Parcours vers l'appel et le formulaire

| Point de départ | Vers l'appel | Vers le formulaire | Friction relevée |
|---|---|---|---|
| Accueil, desktop | 1 clic (téléphone dans l'en-tête, bouton du héro) | 1 clic (ancre `#devis`) puis 9 champs | Section Devis à 8 865 px (9,8 écrans de 900 px). Aucun CTA dans le contenu entre le héro et le formulaire. Pas de réassurance à côté. |
| Accueil, mobile | 1 tap (barre fixe « Appeler ») | 1 tap (« Devis gratuit » dans la barre) puis 9 champs | Formulaire à 15 500 px (18,4 écrans) si on fait défiler. 145 px de chrome fixe. |
| Prestations | 1 clic | 2 clics (« Demander une offre » mène à `contact.html?travaux=…`, type pré-rempli : **bonne pratique**) | Aucune preuve sociale avant le clic. 1er CTA dans le contenu à 1 901 px (desktop) et 2 667 px (mobile), en fin de section Placo. |
| Réalisations | 1 clic | 2 clics | 1er CTA dans le contenu (« Transmettre un dossier ») à 4 865 px (desktop) et 7 069 px (mobile, 8,4 écrans). Aucun CTA près des photos (« Un projet semblable ? »). |
| Contact | 1 clic | 0 clic en desktop (formulaire à 767 px), 2e écran en mobile (1 647 px) | Liste « Pour préparer votre demande » : **excellente** pour les pros, à garder. Ni preuve ni délai. |

Le téléphone est bien traité : dans l'en-tête dès 900 px (la navigation complète, elle, n'apparaît qu'à 1240 px), dans la barre fixe sous 900 px, et 11 liens `tel:` sur l'accueil. À conserver.

### 4.2 Modèle LIFT par page

✓ = bien, ~ = moyen, ✗ = faible.

| Facteur | Accueil | Prestations | Réalisations | Contact |
|---|---|---|---|---|
| **Proposition de valeur** | ~ Le H1 dit quoi et où. L'avantage (« un seul interlocuteur du placo à la peinture ») est noyé dans Prestations et la FAQ. | ✓ Par service : usage, avantages, point d'attention. Format didactique apprécié des pros. | ~ « 30 photos » et « 18 maîtres d'ouvrage » sont des chiffres forts, mais sans récit. | ~ Fonctionnelle, sans promesse (délai, visite). |
| **Pertinence** | ~ Les audiences sont nommées dans le sous-titre. Mais le héro montre un plafond tendu, qui n'est pas dans l'offre. | ~ Discours particulier et normes SIA/AEAI mélangés. | ✗ 16 photos sur 30 hors offre. 0 peinture, 0 cloison isotherme. | ✓ La liste de préparation correspond aux attentes des pros. |
| **Clarté** | ✗ 11 sections, prestations au 5e écran mobile, 19 paragraphes > 3 lignes. | ~ 999 mots, sommaire utile, Peinture sans photo. | ~ Grille plate, filtres sans rapport avec les 4 services. | ✓ Formulaire visible dès le 1er écran en desktop. |
| **Anxiété** | ✗ Témoignages fictifs. Aucune réassurance près du formulaire. Aucun visage. | ✗ Aucune preuve sociale. | ~ Références classées par secteur (bien), mais pas d'année, de lieu ni de projet. | ✗ Pas de délai, pas d'interlocuteur, case de consentement obligatoire, e-mail bluewin. |
| **Distraction** | ~ 18 noms en 2e position, Engagements en double, 40 communes. | ✓ Faible. | ~ 5 quasi-doublons d'îlots lumineux. | ~ Section Zone (141 mots + carte) recopiée de l'accueil. |
| **Urgence (éthique)** | — Aucun dark pattern, conforme. Levier honnête possible : « Subventions : la demande se dépose **avant** les travaux ». | ✓ Le rappel sur les subventions est présent, à mettre en avant. | — | Levier honnête possible : « Visite sous [X] jours ouvrables » si c'est vrai. |

### 4.3 Heuristiques de Nielsen

| # | Heuristique | Ce qui va | Ce qui ne va pas |
|---|---|---|---|
| 1 | Visibilité de l'état du système | Compteur « 30 photos affichées » en direct, menu qui affiche « Fermer », item de nav actif souligné, erreurs en ligne. | Après l'envoi, aucun délai annoncé. Le message (« demande bien prête ») est ambigu. |
| 2 | Correspondance avec le monde réel | Vouvoiement, CHF, téléphones au format suisse. | Jargon (n° 24). Filtre « Chantiers en cours », qui est une étape et non un type de travaux. « L'entreprise » mène à une ancre. |
| 3 | Contrôle et liberté | Échap et « Fermer » sur la visionneuse et le menu. Filtre « Toutes ». Bandeau masquable. | Pas de récapitulatif de la demande envoyée. |
| 4 | Cohérence et standards | Composants homogènes sur toutes les pages. | 5 libellés de CTA, méthode en 4 ou en 6 étapes, « Placo » ou « Plâtrerie », filtre « Cloisons » pour le service « Cloisons isothermes ». |
| 5 | Prévention des erreurs | Exemple de numéro, règle « téléphone ou e-mail » expliquée, formats de fichier annoncés. | Taille maximale du fichier non annoncée. |
| 6 | Reconnaissance plutôt que rappel | Téléphone toujours visible, sommaire sur Prestations, fil d'Ariane, type de travaux pré-rempli. | Sur mobile, la catégorie disparaît sous les vignettes. |
| 7 | Flexibilité et efficacité | Lien d'appel direct, envoi de plans en pièce jointe. | Pas de rappel rapide en 2 champs, pas de PDF de références en téléchargement direct. |
| 8 | Esthétique et minimalisme | Charte sobre et respectée. | **Violation principale** : longueur, répétitions, sections en double. |
| 9 | Diagnostic et correction des erreurs | Messages clairs en français, focus sur le 1er champ en erreur, `aria-invalid`. | — |
| 10 | Aide et documentation | FAQ de 9 questions, liste « Pour préparer votre demande ». | La FAQ n'existe que sur l'accueil, pas sur les pages services. |

---

## 5. Texte à couper

Règles proposées : une idée par bloc, **au plus 2 lignes à 390 px pour un intro** (≈ 15 mots), au plus 12 mots par carte, réponses de FAQ ≤ 35 mots. Les éléments entre [crochets] sont **à confirmer par le client** et ne doivent pas être publiés tels quels.

### Accueil (1 298 → ≈ 650 mots visibles)

| Bloc | Mots actuels → cible | Version courte proposée |
|---|---|---|
| Héro, sous-titre | 25 → 15 | « Pour les régies, architectes, communes et particuliers. Un seul interlocuteur, du montage des plaques à la peinture. » |
| Héro, bande de confiance | 4 items (dont « Devis gratuit » non confirmé) | « Depuis 2007 · Siège à Carouge · 18 références publiques · Toute la Suisse romande ». Ajouter « Devis gratuit » seulement si le client le confirme. |
| Références, intro + liste | 91 → ≈ 30 | Bandeau d'une ligne : « Ils nous ont fait confiance : Ville de Genève · Conservatoire de Musique · HEAD · Salle de l'Alhambra · Mairie de Plan-les-Ouates · [logos autorisés] — Voir les 18 références ». |
| L'entreprise, 3 paragraphes | 93 → 35 | « Entreprise genevoise inscrite au registre du commerce depuis 2007, dirigée par ses deux associés. Nous posons le placo et l'isolation, puis nous peignons : vous n'avez qu'un seul interlocuteur. » |
| L'entreprise, chiffres | 4 chiffres (« 300+ » non confirmé, « 18 » déjà dans le héro) | 3 chiffres confirmés au maximum, sans répéter le héro : « 19 ans · 4 métiers · 6 cantons + Jura bernois ». |
| Prestations, intro | 25 → 10 | « Quatre métiers, un seul interlocuteur. » |
| Prestations, cartes | 4 × 17 → 4 × 10 | Placo : « Doublages, faux-plafonds et cloisons en plaques de plâtre. » · Peinture : « Murs et plafonds préparés et peints, pièces livrées finies. » · Isolation acoustique : « Moins de bruit entre pièces, logements et étages. » · Cloisons isothermes : « Séparer un local chauffé d'un garage ou d'une cave. » |
| Réalisations, intro | 25 → 9 | « Nos chantiers, de l'ossature à la finition. » |
| Méthode + Engagements (2 sections) | 210 → 50 (1 section) | Titre « Comment nous travaillons ». 1. « Visite : mesures et conseils sur place. » 2. « Offre écrite, poste par poste, en CHF. » 3. « Chantier protégé, planning tenu, nettoyage final. » 4. « Réception des finitions avec vous. » |
| Témoignages | 87 → 0 | Masqué jusqu'à réception de témoignages réels. |
| Zone d'intervention | 141 → 25 + carte | « Siège à Carouge. Nous intervenons à Genève, Vaud, Neuchâtel, Fribourg, Jura, en Valais romand et dans le Jura bernois. » La liste des communes part sur la page Zone. |
| FAQ | 9 questions / 477 → 5 questions / ≈ 200 | Garder : délai, prix, hors de Genève, régies et architectes, subventions. Exemple, prix (48 → 30) : « Le prix dépend de la surface, du système, de la hauteur et des finitions. Après une visite ou sur plans, vous recevez une offre détaillée en CHF. » |
| Devis, intro | 25 → 12 | « Décrivez votre chantier : nous vous rappelons pour fixer une visite. » |
| Formulaire, intro | 19 → 8 | « Téléphone ou e-mail : l'un des deux suffit. » |

### Prestations (999 → ≈ 650 mots)

| Bloc | Mots actuels → cible | Version courte proposée |
|---|---|---|
| Intro de la page | 31 → 12 | « Quatre métiers, un seul interlocuteur. Pour chacun : usages, avantages, précautions. » |
| Placo, chapeau | 26 → 14 | « Créer, redresser ou redistribuer vos espaces, sans maçonnerie, prêt à peindre. » |
| Placo, 3 sous-blocs | 72 → 36 | Doublage : « Un mur doublé en plâtre pour le redresser, cacher les gaines ou l'isoler. » · Faux-plafond : « Plafond suspendu, plat ou courbe, qui cache les réseaux et accueille spots et trappes. » · Cloison : « Une cloison légère pour redistribuer un logement ou des bureaux. » |
| Peinture, corps | 29 → 15 | « Après la pose : enduits, bandes et peinture des murs et plafonds. Un seul intervenant. » |
| Isolation acoustique, corps | 40 → 22 | « Faux-plafond désolidarisé, doublage acoustique ou cloison à double ossature : la solution dépend du bruit à arrêter. » |
| Cloisons isothermes, corps (9 lignes à 390 px) | 56 → 30 | « Ossature métallique, isolant et plaques de plâtre : la cloison sépare un logement d'un garage, d'une cave ou de combles non chauffés. Subventions possibles, demande à déposer avant les travaux. » |
| Normes et qualité | 116 → 40 | « Nos ouvrages suivent les normes suisses : SIA 181 (bruit), SIA 180 (thermique), SIA 118 (exécution) et prescriptions incendie AEAI si le projet l'exige. » Le détail va sur la page Professionnels. |
| Déroulement (6 étapes) | 90 → 50 | Reprendre les 4 étapes de l'accueil, mot pour mot. |

### Réalisations et Contact

| Bloc | Mots actuels → cible | Version courte proposée |
|---|---|---|
| Réalisations, intro de la page | 29 → 13 | « Nos chantiers en photos et les maîtres d'ouvrage qui nous ont fait confiance. » |
| Réalisations, intro « Professionnels » | 29 → 18 | « Offres établies sur vos plans et descriptifs, coordination avec les autres corps de métier, partout en Suisse romande. » |
| Contact, colonne gauche | 64 → 35 | Un bloc « Appeler » (bureau, mobile, horaires), un bloc « Adresse », sans répéter les téléphones. |
| Contact, Zone | 141 → 20 | « Toute la Suisse romande, depuis Carouge. » + lien « Voir la zone d'intervention ». |

---

## 6. Portfolio

### Critique

- **Sélection.** 30 photos, mais seulement ≈ 10 dans l'offre actuelle (4 « placo » + 6 « chantier », dont une partie en plafond lumineux). 14 sont requalifiées (plafonds tendus et métalliques), 2 sont hors service (cloisons vitrées). 5 quasi-doublons d'îlots lumineux, quelques photos sans contenu lisible (« Plafond blanc mat »).
- **Couverture.** 0 peinture, 0 cloison isotherme. L'isolation acoustique n'est illustrée que par de l'absorption.
- **Mise en page.** Grille plate de 4 colonnes en desktop et 2 en mobile, vignettes carrées de 167 px sur téléphone. Aucune hiérarchie : la meilleure photo pèse autant que la plus faible.
- **Légendes.** Elles décrivent l'image (« Couronne lumineuse suspendue ») mais pas le projet. Pas de lieu, d'année, de type de bâtiment, de contrainte ni de référence. La catégorie disparaît sur mobile.
- **Filtres.** « Placo et faux-plafonds (18) », « Isolation acoustique (4) », « Cloisons (2) », « Chantiers en cours (6) » : sans rapport avec les 4 services, et « Chantiers en cours » est une étape, pas un type de travaux.
- **Pas d'avant/après, pas de récit.** Or c'est exactement ce que veulent voir une régie (« dans un immeuble habité ? ») et un architecte (« quel système, quelle contrainte ? »).
- **Points positifs à garder** : visionneuse `<dialog>` accessible (boutons texte, compteur « Photo 1 sur 30 », Échap), photos réelles sans banque d'images, filtrage sans rechargement.

### Format recommandé

1. **Trois projets phares en tête de page**, et repris sur l'accueil à la place des 6 vignettes : photo forte en 3:2, pleine largeur en mobile (≥ 343 px), et 3 lignes :
   - **Type de travail** : « Faux-plafond en plaques de plâtre avec gorge lumineuse »
   - **Lieu générique** : « Bureaux, Genève » (jamais de lieu inventé ; le client fournit la commune et le type de bâtiment)
   - **Contrainte résolue** : « Pose en site occupé, sans interrompre l'activité » (**à fournir par le client**, jamais rédigée sans lui)
   - En option, avec accord écrit : nom du maître d'ouvrage, année, CFC.
2. **Une fiche projet par chantier phare** (une URL chacune, utile au SEO) : contexte, demande, solution, contrainte, résultat (sans chiffre inventé), 3 à 6 photos dont une **pendant** et une **après**. Paire candidate à vérifier avec le client : `chantier-ossature-puits-de-lumiere-01` (ossature) et la vue finie du même puits de lumière.
3. **Grille aérée** : 3 colonnes en desktop (vignettes ≥ 380 px), 1 colonne en mobile, format 3:2 et non carré, légende en 18 px avec la catégorie toujours visible.
4. **Filtres** : « Tous · Placo · Peinture · Isolation acoustique · Cloisons isothermes ». Un filtre vide est masqué automatiquement. « Chantiers en cours » devient un badge « Pendant les travaux » sur les photos concernées.
5. **12 à 15 photos bien choisies valent mieux que 30 photos mêlées.** Photos hors offre : retirées, ou regroupées sous « Autres réalisations » avec leur légende exacte (décision du client).
6. **CTA contextuel** sous chaque fiche : « Un projet semblable ? Demander un devis » (type de travaux pré-rempli).
7. **Shooting** (voir `docs/selection-photos.md`) : 3 ou 4 chantiers en cours (peinture, cloison isotherme, doublage acoustique), lumière du jour, cadrage large et détail, avec l'accord des personnes visibles.

---

## 7. Preuve sociale

### Carte des emplacements actuels

| Emplacement | Forme | Moment du parcours | Problème |
|---|---|---|---|
| Accueil › bande du héro | « 18 références publiques » | 1er écran | Un chiffre seul, sans aucun nom. |
| Accueil › section 2 | Liste de 18 noms en texte | 2e et 3e écrans | Trop long, sans logo, sans lien vers un projet. |
| Accueil › chiffres de l'entreprise | « 18 références publiques citées » | 4e écran | Répétition. « 300+ » non confirmé. |
| Accueil › Engagements | « Ville de Genève, Conservatoire, HEAD… » | 11e écran | Répétition. |
| Accueil › Témoignages | 3 citations | 12e et 13e écrans | **Fictives**. |
| Accueil › FAQ | Domaine des Perrières, Dipan, Ville de Genève… | 16e écran | Cachées dans des accordéons. |
| Réalisations | 18 noms par secteur + bloc pros | Bas de page | Pas reliés aux photos. |
| Prestations | — | — | **Absente.** |
| Contact, à côté du formulaire | Lien « Voir nos références » | — | **Absente** au point de conversion. |
| Pied de page | IDE, raison sociale | Toutes pages | Pas de référence. |

### Emplacements proposés

Logos selon leur statut dans `logos.json` (`autorise` / `a_autoriser` / `protege`). Armoiries publiques et OMC toujours en **nom typographique**.

| Emplacement | Contenu | Pourquoi |
|---|---|---|
| 1. **Bandeau sous le héro** (toutes les pages d'entrée) | 6 à 8 logos monochromes ou noms, sur une ligne, + « Voir les 18 références » | Réassure dès le 1er écran sans repousser l'offre. |
| 2. **Pages services** | 1 projet illustré + « Réalisé notamment pour : … » (si c'est vrai) | La preuve au moment où l'on évalue le service. |
| 3. **Fiches projet** | Nom du maître d'ouvrage (avec accord), année, photos | Une preuve qui se vérifie. |
| 4. **Juste avant le formulaire** (accueil et contact) | Une ligne de références + 1 vrai témoignage + « Inscrite au registre du commerce depuis 2007 · IDE CHE-113.706.162 » | Lève le doute au moment de remplir. |
| 5. **Pied de page** (toutes pages) | Une ligne « Ils nous ont fait confiance : … » en texte | Une preuve répétée sans encombrer. |
| 6. **Avis Google** (une fois recueillis) | Note et nombre d'avis en **texte statique**, mis à jour à la main, avec lien vers la fiche. Pas de widget tiers (nLPD, performance). | Preuve indépendante. Lancer la campagne d'avis (`analyse-marche.md`). |
| 7. **Page Professionnels** | Dossier de références PDF téléchargeable, CFC, attestations (à fournir) | Le format attendu par les régies et les communes. |
| 8. **Visages** | Photo des associés (nommés dans les mentions légales), avec leur accord | Pour un public de 45 à 70 ans, un visage rassure plus qu'un logo. |

Cadence visée : la preuve revient en **haut** (bandeau), au **milieu** (projets), en **bas** (avant le formulaire) et dans le **pied**, sur chaque page d'entrée.

---

## 8. SEO technique (détail)

| Point | État | Action |
|---|---|---|
| Titles | Uniques, de 33 à 60 caractères. Accueil et Prestations quasi identiques. | Différencier (n° 29). Un title par page service. |
| Meta descriptions | Uniques, de 106 à 164 caractères. Accueil à 164. | ≤ 155 (n° 41). |
| Hn | Un H1 par page, hiérarchie propre. H3 « Pour quels locaux » et « Avantages » répétés 4 fois sur Prestations. | Sans gravité. Sur les pages services, H2 orientés requête (« Prix d'un faux-plafond à Genève »). |
| JSON-LD | Parse OK. `HomeAndConstructionBusiness` (adresse, géo, horaires, IDE, areaServed, OfferCatalog), WebSite, WebPage, FAQPage (9 Q), BreadcrumbList. | `image` : uniquement des photos de l'offre. Retirer le `sameAs` search.ch (ancienne adresse). `Service` par page service. `ImageGallery` sur Réalisations. `Review` **seulement** avec de vrais avis. |
| Canonical | Pointe vers `https://www.andyconstruct.ch/…`. | OK. |
| robots / sitemap / llms.txt | robots OK. Sitemap de 5 URL, `lastmod` figé. llms.txt complet et cohérent avec le site. | Sitemap généré au build. Compléter llms.txt avec les nouvelles pages. |
| Maillage | Prestations vers Réalisations et Contact (type pré-rempli) : bien. Réalisations ne renvoie vers aucune ancre de service. | Liens photo vers service, référence vers projet, service vers projets. |
| Alt | Tous présents. Trop longs (moyenne 17 mots) et réécrits. | n° 30. |
| NAP | Identique sur tout le site (Route des Acacias 48, 1227 Carouge, +41 22 771 20 15). | Garder un seul numéro principal en avant. E-mail sur le domaine. |
| `noindex` | Voulu en preview (Lighthouse SEO 69). | Retirer en production (`--production`). |

**Pages manquantes pour le SEO local en Suisse romande**, par ordre de valeur :
1. `placo-faux-plafonds-geneve.html`, `peinture-interieure.html`, `isolation-acoustique.html`, `cloisons-isothermes.html` : une page par service (≈ 500 à 800 mots utiles, FAQ propre, 1 projet).
2. `entreprise.html` : associés, historique depuis 2007, registre, assurances (E-E-A-T).
3. `professionnels.html` : régies, architectes, communes, avec CFC, travail sur plans, dossier PDF, procédure.
4. `zone-intervention.html` : carte et communes. Puis une page par canton ou ville **seulement si un chantier réel y existe** (règle de `analyse-marche.md` : Carouge, Genève, Collonge-Bellerive, Plan-les-Ouates, Nyon, Coppet).
5. `realisations/<projet>.html` : 3 à 10 fiches projet.
6. Plus tard : guide « Subventions pour l'isolation en Suisse romande (Programme Bâtiments) », pertinent et cité par les moteurs IA.

---

## 9. Lisibilité senior (détail)

| Critère | Mesure | Verdict |
|---|---|---|
| Taille de base | 18 px (`--fs-base: 1.125rem`), sous-titres 19 à 21 px | ✓ |
| Textes < 16 px | 14 px : `.eyebrow`, `.label`, `.tag`, titres du pied, « Appelez-nous » (≈ 50 mots par page) | ✗ (charte §4) |
| Textes à 16-17 px | Cartes, étapes, notes, aides, formulaire : ≈ 700 mots de l'accueil | ~ |
| Interligne | 1,6 pour le texte, 1,55 pour les intros | ✓ |
| Longueur de ligne | `p { max-width: 68ch }` | ✓ |
| Contrastes | Anthracite et graphite sur blanc ou brume ≥ 8:1, acier sur anthracite 8,7:1 (charte). Seul échec axe : le « 404 » décoratif. Texte du héro sur photo : voile suffisant à l'œil (axe ne peut pas calculer). | ✓ |
| Cibles tactiles | Boutons ≥ 52 px, champs 52 px, barre fixe 52 px. Liens du pied 38 px, liens `tel:` dans le texte 22 à 25 px, cases à cocher 24 px (le libellé reste cliquable). | ~ |
| Majuscules espacées | Surtitres de 14 px en capitales à 0,18em | ✗ : passer à 16 px |
| Icônes | Toujours accompagnées d'un texte, aucun bouton fait d'une icône seule | ✓ |
| Vocabulaire | Voir n° 24 | ~ |
| Vignettes photo | 167 px sur téléphone | ✗ |
| Mouvement | Aucun carrousel ni animation, `prefers-reduced-motion` respecté | ✓ |

---

## 10. Quick wins (≤ 1 h chacun)

1. Masquer le bloc Témoignages tant qu'il n'y a pas de vrais témoignages (`page_index.py`, condition sur une liste vide).
2. Retirer « Devis gratuit » et « 300+ » s'ils ne sont pas confirmés. Libellé de la barre mobile : « Demander un devis ».
3. Un seul libellé de CTA sur tout le site (`common.py`, `page_*.py`).
4. Sous le bouton d'envoi : 3 puces de réassurance + nom de l'interlocuteur (délai **à confirmer**). Corriger le message de succès.
5. Remplacer la case de consentement obligatoire par une mention d'information (**après avis juridique**).
6. `--fs-xs: 1rem` et `--fs-card: 1.125rem` dans `styles.css`.
7. Liens du pied en `min-height: 48px`.
8. Galerie : retirer l'`aria-label` des boutons, ajouter un texte visuellement masqué « Agrandir : » (corrige 30 nœuds axe).
9. 404 : `aria-hidden="true"` sur le chiffre. Champ fichier : un seul nom accessible et taille maximale annoncée.
10. Carte : faire pointer `<image>` vers le logo WebP au lieu du PNG de 77 Ko (`carte.py`).
11. Différencier les titles accueil / prestations. Ramener la meta de l'accueil à 155 caractères.
12. Retirer le `sameAs` search.ch (ancienne adresse). Mettre des photos de l'offre dans `image` du JSON-LD et dans l'image OG.
13. Supprimer les réécritures `TITRES` et `alt()` de `common.py`. Raccourcir les alt à 8-12 mots.
14. Afficher la catégorie sous les vignettes en mobile.
15. Accueil : supprimer la section Engagements et la fondre dans Méthode. Méthode en 4 étapes partout.
16. Accueil : remplacer la liste de 18 noms par un bandeau d'une ligne.
17. Contact : dédoublonner la colonne gauche. Réduire Zone à une ligne et un lien.
18. Appliquer les intros courtes du § 5 (textes dans `content.py` et `page_*.py`).
19. Ajouter la variante 400w des vignettes et corriger `sizes` (script Pillow existant).

## 11. Chantiers structurants

| Chantier | Contenu | Dépend de | Effort indicatif |
|---|---|---|---|
| **A. Portfolio v2** | Décision du client sur les photos hors offre. Shooting peinture, cloison isotherme et acoustique. 3 projets phares, fiches projet, grille 3 colonnes / 1 colonne, filtres sur les 4 services, avant/après, CTA contextuel. | Photos et informations projet du client | 3 à 5 jours + shooting |
| **B. Arborescence SEO** | 4 pages services, Entreprise, Professionnels, Zone, puis pages canton ou ville avec chantier réel, fiches projet. Maillage, sitemap généré, JSON-LD `Service`. | Copy deck (phase 2) | 4 à 6 jours |
| **C. Accueil en 7 sections** | Héro (sous-titre court) et bandeau de références, Prestations, 3 projets, « Comment nous travaillons », Zone courte, FAQ (5 Q), Devis avec réassurance. Cible ≈ 650 mots, ≤ 10 écrans mobiles. | A (projets), D (preuve) | 2 jours |
| **D. Preuve sociale** | `logos.json` avec statuts, bandeau, ligne de pied, rappel avant le formulaire, collecte d'avis Google et de 2-3 témoignages écrits, dossier PDF, photo des associés. | Accords du client et des clients finaux | Continu, 2 jours de dev |
| **E. Conversion et formulaire** | Endpoint, accusé de réception automatique, option « Rappel rapide » (nom, téléphone, créneau), délai de réponse tenu, suivi sans cookies des clics `tel:` et des envois. | Phase 2 (automatisation) | 2 à 3 jours |
| **F. Performance** | Compression et cache sur l'hébergeur, CSS minifié et critique en ligne, logo SVG, variantes d'images. Objectif LCP ≤ 2,0 s en mobile simulé. | — | 1 jour |
| **G. Rédaction senior** | Glossaire simple, jargon réservé aux blocs pros, FAQ par service, relecture en vouvoiement. | Copy deck | 2 jours |

---

## Annexe A — Résultats bruts axe-core 4.14.0

Règles : `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`, `best-practice`.

| Page | 1440 px : violations (nœuds) | 390 px : violations (nœuds) | À vérifier à la main (incomplete) |
|---|---|---|---|
| index | 0 | 0 | `color-contrast` (32 / 22 nœuds : texte sur photo du héro et sur voile, fond non calculable) ; `form-field-multiple-labels` (1, `#accueil-fichier`) |
| prestations | 0 | 0 | — |
| realisations | **1 : `label-content-name-mismatch`, sérieux, WCAG 2.5.3 (30 nœuds `.gallery__btn`)** | 0 (catégorie masquée sur mobile) | — |
| contact | 0 | 0 | `color-contrast` (19 / 9 : `select` avec image de fond, textes de la carte SVG) ; `form-field-multiple-labels` (1, `#contact-fichier`) |
| mentions-legales | 0 | 0 | — |
| 404 | **1 : `color-contrast`, sérieux (1 nœud `.notfound__code`, 1,28:1)** | 1 (idem) | — |

Lighthouse Accessibilité : 100 sur les 4 pages testées.

## Annexe B — Résultats bruts Lighthouse 12.8.2 (mobile, débit simulé)

| Page | Perf | A11y | Bonnes pr. | SEO* | FCP | LCP | TBT | CLS | Speed Index | Poids | Requêtes | Élément LCP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| index | 93 | 100 | 100 | 69 | 1,8 s | **2,7 s** | 160 ms | 0 | 1,8 s | 358 Kio | 12 | `img` du héro (plafond tendu, 16 Ko en 800w), délai de rendu 1 990 ms |
| prestations | 98 | 100 | 100 | 69 | 1,5 s | 2,2 s | 0 ms | 0 | 1,5 s | 199 Kio | 10 | `p.lead` |
| realisations | 99 | 100 | 100 | 69 | 1,2 s | 2,0 s | 0 ms | 0 | 1,2 s | 693 Kio | 31 (23 images, 520 Ko) | `p.lead` |
| contact | 97 | 100 | 100 | 69 | 1,7 s | 2,4 s | 10 ms | 0 | 1,7 s | 284 Kio | 10 | `p.lead` |
| index, **avec compression** (`serve`) | 97 | — | — | — | 1,7 s | 2,4 s | 0 ms | 0 | — | 264 Kio | — | idem |

\* SEO à 69 uniquement à cause du `noindex` voulu en preview.

Audits sous 0,9 (accueil, serveur local) : `render-blocking-resources` (−290 ms ; −660 ms sur Prestations et Contact), `unused-css-rules` (−19 à −28 Kio), `unminified-css` (−6 Kio), `unminified-javascript` (−3 Kio), `uses-responsive-images` (−31 Kio ; −297 Kio sur Réalisations), `modern-image-formats` (−56 Kio : PNG de la carte), `uses-text-compression` (−94 Kio, artefact du serveur local), `uses-long-cache-ttl` et `cache-insight` (artefact du serveur local), `max-potential-fid` 210 ms.

Budgets du programme : JS 11 Ko (< 25 Ko ✓), CSS 39 Ko (< 50 Ko ✓, 9 Ko compressé), aucune dépendance externe ✓. LCP < 2,5 s : ✗ sans compression, ✓ de justesse avec.

## Annexe C — Densité brute

Mots visibles par section de l'accueil : héro 74 · références 91 · entreprise 136 · prestations 126 · réalisations 85 · méthode 97 · engagements 113 · témoignages 87 · zone 127 (390 px) / 141 (1440 px) · FAQ 78 fermée / 477 ouverte · devis 180 · pied 85.
Prestations : intro 49 · placo 193 · peinture 102 · isolation acoustique 141 · cloisons isothermes 153 · déroulement 90 · normes 116 · CTA 35.
Réalisations : intro 34 · galerie 276 (194 en mobile) · références 99 · professionnels 93 · CTA 30.
Contact : intro 21 · appeler 24 · adresse 40 · préparer 33 · formulaire 124 · zone 141.

Répartition des tailles de police, accueil à 390 px (mots par taille) : 14 px : 49 · 16 px : 406 · 17 px : 300 · 18 px : 577 · 19 px : 269 · titres ≥ 22 px : 66.

## Annexe D — Captures et données

Dossier de travail (hors dépôt) : `/tmp/claude-0/-home-user-andy-construct/f283fb31-e1fb-5fd9-86ca-20cafe41f0ab/scratchpad/audit/`
- `<page>-1440.png`, `<page>-390.png` : pleine page (6 pages) ; `<page>-<largeur>-fold.png` : premier écran ; `slices/` et `mont/` : découpes relues.
- `index-1024-fold.png`, `index-390-menu.png`, `realisations-1440-lightbox.png`, `contact-390-form-errors.png`, `contact-390-form-success.png`.
- `axe-results.json`, `axe-output.txt`, `density.json`, `density-output.txt`, `text-<page>.txt` (texte par section).
- Rapports Lighthouse : `/tmp/claude-0/-home-user-andy-construct/f283fb31-e1fb-5fd9-86ca-20cafe41f0ab/scratchpad/lh/*.report.html|json`.
