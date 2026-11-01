# Audit SEO : Andy Construct (v4)

**Date :** 1er novembre 2026
**Rédaction :** auditeur SEO, pour le chef de projet
**Périmètre :** (1) le nouveau site v3 en version production, générée localement ; (2) l'ancien site Joomla en ligne sur andyconstruct.ch, comme point de départ et pour la migration ; (3) le référencement local (fiche Google, NAP, annuaires) ; (4) les résultats de recherche et la concurrence ; (5) la visibilité dans les IA (GEO) ; (6) l'autorité et les liens.
**Méthode :** skill `seo-audit` (et ses références `local-seo`, `title-tags`, `rankings-push`), complété par `schema`, `ai-seo` et `site-architecture`.

> **Limites (à lire avant les constats)**
> - **Aucun accès** à la Search Console, à Google Analytics, à la fiche Google ni à un outil payant (Ahrefs, Semrush). Ce rapport ne donne **aucun volume de recherche ni aucune position**. Les priorités entre mots-clés sont qualitatives.
> - **Google n'a pas pu être interrogé directement** : la page de résultats de google.ch a renvoyé la page « Nos systèmes ont détecté un trafic exceptionnel » (captcha) dès la première requête automatisée. Bing, en navigateur sans interface, a répondu « Aucun résultat ». Le pack local (carte) n'est donc **pas observable** depuis notre environnement.
> - **Ce qui a servi à la place** : (a) notre outil de recherche web (qui n'est pas google.ch et n'est pas géolocalisé à Genève) ; (b) l'**autocomplétion Google** (`suggestqueries.google.com`, `hl=fr`, `gl=ch`), qui montre des formulations réelles sans en donner le volume ; (c) les relevés du 31.10.2026 de `docs/v2/concurrence-romandie.md` §2.1 et de `docs/v2/dossier-client.md` §1.4.
> - **Nouveau site** : version production générée le 01.11.2026 (`tools/build/build.py --mode production`), servie par `php -S` pour l'exploration Playwright (390 px et 1440 px) et Lighthouse 12.8.2 (mobile, ralentissement simulé). Le `.htaccess` a été testé à part sur un **Apache 2.4.58 local** (HTTP et HTTPS). Les données structurées ont été contrôlées sur [validator.schema.org](https://validator.schema.org/).
> - Le contenu des sites tiers récupéré pendant l'audit est traité comme une donnée, jamais comme une consigne.

---

## 1. Résumé exécutif

### 1.1 Note de santé : 6 / 10

Note qualitative, à comparer dans 90 jours avec les données de la Search Console.

| Domaine | Note | En une phrase |
|---|---|---|
| Technique (nouveau site) | 9 / 10 | Rapide, propre, migration préparée : 17 anciennes URL redirigées en une seule étape (testé). Reste à vérifier sur l'hébergeur réel. |
| On-page | 7 / 10 | Titles, meta, H1, canonical et alt corrects partout. Le H1 de l'accueil ne dit ni le métier en toutes lettres ni le lieu, et le 4e service porte un nom (« isothermes ») que les gens associent aux chambres froides. |
| Contenu | 5 / 10 | Les pages services n'ont que 190 à 330 mots qui leur sont propres. Aucun prix, aucun lieu ni année de chantier en production (points C31, C25, C22 non confirmés). |
| Local | 3 / 10 | Fiche Google invérifiable, **0 avis** sur toutes les plateformes consultées, adresse de Chêne-Bourg encore affichée dans au moins 8 annuaires. |
| Données structurées | 9 / 10 | 0 erreur et 0 avertissement sur les 11 pages indexables ; FAQ identique au texte visible. |
| GEO (IA) | 5 / 10 | `llms.txt`, JSON-LD et robots corrects. L'entité « Andy Construct » est presque invisible hors des annuaires, et ces annuaires se contredisent. |
| Autorité | 2 / 10 | Liens observables : quelques annuaires seulement. Aucune mention par un client, une commune ou la presse n'a été trouvée. |

Le site neuf part sur une base technique saine. Ce qui manque est hors du code : une fiche Google active avec des avis, une identité cohérente dans les annuaires, et des preuves locales publiées (lieux, années, prix).

### 1.2 Les 5 priorités

1. **Fiche Google en « zone desservie » et premiers avis.** Vérifier si une fiche existe et qui la détient, la revendiquer, la compléter, puis demander un avis à chaque fin de chantier. Aujourd'hui : 0 avis sur local.ch, search.ch et Yelp ; la concurrence affiche 16 à 50 avis Google (`docs/v2/concurrence-romandie.md` §1). *Client et agence.*
2. **Migration sans perte.** Les 301 sont prêtes et testées. Il reste à les vérifier **sur l'hébergeur réel** (nginx devant Apache, probablement sous Plesk, voir T1), à ouvrir la Search Console et Bing Webmaster Tools **avant** la bascule, et à suivre les erreurs pendant 30 jours (§4). *Développeur et agence.*
3. **Une seule identité partout (NAP).** Corriger Chêne-Bourg, les catégories erronées (charpenterie, sonorisation, appareils auditifs…) et la fiche LinkedIn (« Facilities Services », « tissu tendu »), passer tous les liens en `https://www.andyconstruct.ch/`. Décider l'e-mail (C30) **avant** de réécrire les fiches. *Agence, avec les accès du client.*
4. **Décider le nom et l'URL du 4e service (C16) avant la mise en ligne.** « Cloison isotherme » renvoie aux chambres froides (autocomplétion : « cloison isotherme chambre froide », « … cuisine », « … fiche technique ») ; « cloison isolante » renvoie au besoin réel (« … entre garage et habitation », « … garage »). Changer l'adresse de la page ne coûte rien tant que le site n'est pas en ligne. *Client et chef de projet.*
5. **Contenu qui prouve et qui répond.** Ajouter 300 à 400 mots propres par page service (vocabulaire romand : plâtrerie, gypserie, plâtrier-peintre ; questions de prix et de délais), publier les fourchettes de prix (C31), les communes et années des chantiers (C25, C22) et les premières fiches projets. *Client (confirmations), agence (rédaction).*

### 1.3 Gains rapides (moins d'une heure chacun)

- Mettre à jour la page LinkedIn : secteur « Construction » (ou équivalent), description des 4 métiers, localité « Carouge », lien `https://www.andyconstruct.ch/`.
- Fiche GGE : ajouter le numéro fixe (seul le mobile y figure).
- local.ch et search.ch : lien du site en `https://www.`, retrait de la catégorie « Sonorisation », nouveau logo.
- Créer la propriété « Domaine » dans la Search Console (vérification DNS) dès maintenant : elle collecte déjà les données de l'ancien site, utiles pour comparer après la bascule.
- Lien de rendez-vous de la fiche Google : utiliser `contact.html#demande`. Le lien proposé dans `docs/v2/strategie-acquisition.md` §3.1 se termine par `#formulaire`, une ancre qui n'existe pas (document v2 non modifié par cet audit).

---

## 2. Constats

Format de chaque constat : **Problème** · **Impact** (élevé, moyen, faible) · **Preuve** · **Correction** · **Priorité**. Les points marqués **[corrigé]** ont été réglés dans `tools/build/` pendant l'audit (détail au §5).

### 2.0 Ce qui est déjà solide (à ne pas casser)

- **Indexation maîtrisée.** Production : 11 pages indexables, toutes avec un canonical absolu sur `https://www.andyconstruct.ch/…` ; `merci.html` et `404.html` en `noindex` ; `sitemap.xml` limité aux 11 URL canoniques ; `robots.txt` qui ne bloque que `/api/` et `/interne/` et laisse passer les robots des IA. Preview et vérification : `noindex, nofollow` sur toutes les pages.
- **Vitesse.** Lighthouse mobile **avec compression** : accueil 99 (LCP 2,0 s), placo 99 (LCP 2,0 s), réalisations 100 (LCP 1,8 s) ; accessibilité, bonnes pratiques et SEO à 100 ; CLS 0 partout. Poids transféré 197 à 260 Ko.
- **Balisage.** `lang="fr-CH"`, un seul H1 par page indexable, aucun saut de niveau de titre, toutes les images avec `alt`, `width` et `height`, WebP avec repli JPEG, chargement paresseux sauf l'image principale (`fetchpriority="high"`).
- **Maillage.** Toutes les pages indexables sont à **un clic** de l'accueil ; aucune page orpheline hors `merci.html` et `404.html` (normal).
- **Migration.** Les 17 URL de l'ancien sitemap et leurs variantes (avec ou sans `index.php/`, `www`, `http`) redirigent en **une seule étape** vers la bonne page (annexe C).
- **Données structurées.** 0 erreur, 0 avertissement sur validator.schema.org pour les 11 pages ; FAQPage identique, mot pour mot, au texte visible des 5 FAQ.

### 2.1 Technique

**T1. Hébergement avec nginx devant Apache (probablement Plesk) : les en-têtes du `.htaccess` risquent de ne pas s'appliquer aux fichiers statiques**
- **Problème :** l'ancien site tourne chez Metanet / kreativmedia (IP 80.74.139.25, nom inverse `ophelia.kreativmedia.ch`), avec nginx devant Apache (en-têtes `server: nginx` et `x-accel-version` ; kreativmedia gère ses serveurs avec Plesk, à confirmer pour cet hébergement). Sur l'ancien site, la feuille de style est servie compressée (brotli) mais **sans aucun en-tête de cache**. Si nginx sert les fichiers statiques sans passer par Apache, les règles `Header` et `Expires` du nouveau `.htaccess` ne s'appliqueront pas aux CSS, JS, images et polices.
- **Impact :** moyen (vitesse des visites suivantes, Core Web Vitals réels).
- **Preuve :** `curl -I https://www.andyconstruct.ch/templates/andy_2017_2/css/template.css` (01.11.2026) : `content-encoding: br`, ni `Cache-Control` ni `Expires`. Plesk précise que lorsque nginx sert les fichiers statiques directement, les directives du `.htaccess` ne sont pas appliquées ([Plesk 12.5](https://docs.plesk.com/en-US/12.5/customer-guide/72320/), [Plesk Obsidian](https://docs.plesk.com/en-US/obsidian/customer-guide/72320/)).
- **Correction :** le jour J, contrôler les en-têtes d'un CSS, d'une image et d'une police (commandes au §4). S'ils manquent : dans Plesk, « Apache & nginx Settings » du domaine, activer « Smart static files processing » ou désactiver « Serve static files directly by nginx », ou ajouter les en-têtes dans les directives nginx supplémentaires. Contrôler au même moment qu'il n'y a pas de boucle de redirection HTTPS (la règle utilise `%{HTTPS}`, qui dépend de la façon dont nginx transmet la requête à Apache).
- **Priorité :** haute, jour J.

**T2. Compression obligatoire en production**
- **Problème :** sans compression, le LCP mobile dépasse le seuil de 2,5 s.
- **Impact :** moyen.
- **Preuve :** Lighthouse mobile sans compression (serveur `php -S`) : LCP 2,8 s (accueil), 2,7 s (placo), 2,8 s (réalisations), performance 96. Avec gzip : LCP 2,0 / 2,0 / 1,8 s, performance 99 à 100. Économie estimée par Lighthouse : 117 à 123 Ko par page. Seuils : [web.dev](https://web.dev/articles/vitals).
- **Correction :** le `.htaccess` active brotli ou deflate ; l'ancien hébergement compresse déjà (brotli). Vérifier `content-encoding` sur le HTML, le CSS et le JS le jour J.
- **Priorité :** haute, jour J (contrôle).

**T3. Liens internes vers `/index.html` au lieu de `/` [corrigé]**
- **Problème :** le logo, le fil d'Ariane et les liens « Retour à l'accueil » pointaient vers `index.html`, alors que le canonical et le sitemap déclarent `https://www.andyconstruct.ch/`. Deux URL répondaient en 200 pour la même page.
- **Impact :** faible à moyen (signal de canonicalisation contradictoire sur la page la plus liée).
- **Preuve :** 24 liens `href="index.html"` dans les 13 pages de production ; Google recommande de lier l'URL canonique ([Google](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)).
- **Correction :** en production, les liens deviennent `./` (résolu en `/`), et `/index.html` redirige en 301 vers `/` (règle limitée à la requête du visiteur, sans effet sur `DirectoryIndex`). Testé sur Apache : `/index.html` → 301 `https://www.andyconstruct.ch/`, `/` → 200, `?flag=` conservé. Preview et vérification gardent `index.html` pour l'ouverture en local.
- **Priorité :** faite.

**T4. Version de validation : le noindex ne couvrait pas les PDF et le `robots.txt` le contredisait [corrigé]**
- **Problème :** en preview, `robots.txt` contenait `Disallow: /`. Un robot bloqué ne lit pas la balise `noindex` et peut indexer l'adresse nue si un lien y mène. Les PDF (dont le dossier de références) et les images n'avaient aucune consigne d'indexation.
- **Impact :** moyen (fuite possible de la version de validation et des documents, sur harbor-digital.fr).
- **Preuve :** Google : « pour que la règle noindex soit efficace, la page ne doit pas être bloquée par robots.txt » ([Google](https://developers.google.com/search/docs/crawling-indexing/block-indexing)) ; l'en-tête `X-Robots-Tag` couvre les fichiers non HTML ([Google](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag)). `harbor-digital.fr/robots.txt` répond 404 (01.11.2026).
- **Correction :** `.htaccess` de preview et de vérification : `Header always set X-Robots-Tag "noindex, nofollow"` (vérifié sur Apache local : présent sur HTML, PDF et `robots.txt`). `robots.txt` de preview : exploration ouverte, avec un commentaire qui explique pourquoi. La production n'est pas touchée.
- **Priorité :** faite.

**T5. Dépôt GitHub public et indexé**
- **Problème :** le dépôt `rayhanhasan/andy-construct` est public (HTTP 200 le 01.11.2026). Il contient le site, les documents internes (stratégie, dossier client, décisions) et la plaquette de validation.
- **Impact :** moyen (confidentialité surtout ; les pages HTML n'y sont pas rendues, le risque de contenu dupliqué est faible).
- **Preuve :** `HANDOFF.md` §2 et §9 ; `docs/v2/dossier-client.md` T5.
- **Correction :** passer le dépôt en privé (Settings, Danger Zone).
- **Priorité :** haute, avant la mise en ligne.

**T6. Dates de mise à jour fictives (sitemap et pages légales)**
- **Problème :** `lastmod` du sitemap et « Dernière mise à jour » des mentions légales et de la politique de confidentialité prennent la **date de génération**, même si rien n'a changé.
- **Impact :** faible. Google n'utilise `lastmod` que s'il est « exact de façon constante et vérifiable » ([Google](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)) ; une date légale qui bouge à chaque génération est inexacte.
- **Preuve :** les 11 `lastmod` valent `2026-11-01` ; la régénération du 01.11 a changé la date des deux pages légales sans changer leur texte.
- **Correction :** tirer `lastmod` d'une empreinte du contenu de chaque page (mémorisée dans `tools/build/donnees/`), et fixer la date des pages légales dans les données (modifiée seulement quand le texte change). Le « 1 novembre » a été corrigé en « 1er novembre » (§5).
- **Priorité :** basse.

**T7. Anciennes images et fichiers Joomla**
- **Problème :** l'ancien site expose 214 images sous `/images/…` (aucune avec `alt`) et des fichiers Joomla (`/administrator/`, `htaccess.txt` en 200). Après la bascule, les images répondront 404 ; si les fichiers Joomla restent sur le serveur, l'administration resterait accessible.
- **Impact :** faible (SEO), moyen (sécurité).
- **Preuve :** exploration des 16 pages de l'ancien site ; `curl` le 01.11.2026 : `/administrator/` 200, `/htaccess.txt` 200, `/images/Divers/IMG_0708.jpg` 200 (955 Ko).
- **Correction :** déployer dans un dossier vide (archiver l'ancien site hors de la racine web, sauvegarde conservée). Laisser les anciennes images en 404 : elles n'ont pas d'équivalent une à une et Google les retirera. Les 404 attendues dans la Search Console pour `/images/` ne demandent aucune action.
- **Priorité :** moyenne, jour J.

**T8. HSTS non activé**
- **Problème :** l'en-tête `Strict-Transport-Security` est commenté dans le `.htaccess` (choix volontaire du générateur).
- **Impact :** faible.
- **Correction :** l'activer après une semaine sans erreur HTTPS, d'abord **sans** `includeSubDomains` tant que les sous-domaines (messagerie, webmail) n'ont pas été vérifiés.
- **Priorité :** basse, J+7 à J+30.

**T9. Redirections de la version de validation**
- **Problème :** en preview, les cibles des 301 Joomla commencent par `/` : sur `harbor-digital.fr/res/andy-construct-v3/`, elles mèneraient à la racine de harbor-digital.fr.
- **Impact :** faible (version non indexée).
- **Correction :** tester les 301 uniquement sur la production, ou avec la configuration Apache locale utilisée pour cet audit (annexe C).
- **Priorité :** basse.

### 2.2 On-page

**O1. Titles et meta descriptions : conformes**
- Tous uniques, de 33 à 61 caractères, entre ~300 et ~570 px (Arial 20 px, limite d'affichage autour de 580-600 px). Seul `cloisons-isothermes.html` approche la limite (61 car., ~569 px). Meta de 121 à 156 caractères. Tableau complet et propositions en annexe A.

**O2. H1 de l'accueil sans métier ni lieu en clair**
- **Problème :** H1 « Placo, peinture, acoustique : la rigueur des chantiers publics ». Le title dit « Plâtrerie, peinture et isolation à Genève », le H1 ne dit ni « Genève » ni « Suisse romande », et le mot « plâtrerie » n'apparaît nulle part dans le corps de l'accueil.
- **Impact :** moyen (pertinence locale de la page la plus forte ; Google réécrit plus souvent un title qui diverge du H1, voir `title-tags.md`).
- **Preuve :** comptage dans `<main>` de l'accueil en production : « plâtrerie » 0, « Genève » 14 dont la plupart dans les noms de clients (« Ville de Genève », « Conservatoire de musique de Genève »).
- **Correction (texte à valider, pas de changement fait) :** garder le H1 et ajouter le lieu dans la phrase sous le titre, par exemple « Entreprise de plâtrerie et de peinture à Carouge, pour Genève et toute la Suisse romande. Régies, architectes… ». Le drapeau A/B `hero-titre` existant permet aussi de tester une variante.
- **Priorité :** moyenne.

**O3. Meta description de la page contact : horaires non confirmés publiés [corrigé]**
- **Problème :** la meta disait « du lundi au vendredi » alors que les horaires (C03) sont masqués en production partout ailleurs.
- **Impact :** faible (promesse non confirmée affichée dans Google).
- **Correction :** la mention suit désormais C03 (§5).
- **Priorité :** faite.

**O4. Vocabulaire romand absent**
- **Problème :** les mots que les Romands tapent ne sont pas dans les pages : dans le contenu principal des 9 pages commerciales, « plâtrier » 0 fois, « gypserie » 0, « faux plafond » (sans trait d'union) 0 ; « plâtrerie » 0 sur la page placo.
- **Impact :** moyen.
- **Preuve :** comptage des termes dans `<main>` (production) ; autocomplétion : « gypserie peinture genève », « entreprise gypserie peinture geneve », « entreprise plâtrerie peinture genève », « platrier peintre lausanne ». `docs/v2/strategie-acquisition.md` §3.2 recommande déjà ce vocabulaire.
- **Correction :** sur la page placo, une phrase du type « Plâtrerie sèche, aussi appelée gypserie en Suisse romande » ; « plâtrier-peintre » dans la page Professionnels ; les deux graphies de faux-plafond dans les FAQ. Sans répétition forcée.
- **Priorité :** moyenne.

**O5. Le nom du 4e service ne correspond pas à la recherche**
- **Problème :** en production, le title, le H1, le menu et l'URL disent « cloisons isothermes ».
- **Impact :** élevé pour cette page.
- **Preuve :** autocomplétion (`hl=fr`, `gl=ch`, 01.11.2026) : « cloison isotherme » → « fiche technique », « cuisine », « coupe feu », « chambre froide », « panneau isotherme » ; « cloison isolante » → « entre garage et habitation », « garage », « thermique et phonique », « placo » ; « isolation plafond garage » → « avec chambre au-dessus ». `docs/v2/concurrence-romandie.md` §1 point 5 arrivait à la même conclusion.
- **Correction :** confirmer C16 (« Cloisons isolantes »). Avant la mise en ligne, renommer aussi le fichier (`cloisons-isolantes.html`) avec une 301 depuis `cloisons-isothermes.html` et l'ancienne URL Joomla `isolation-thermique-ou-phonique` pointée directement sur la nouvelle adresse. Garder « isotherme » comme synonyme dans le texte.
- **Priorité :** critique (décision avant la mise en ligne).

**O6. Meta descriptions qui annoncent un contenu masqué en production**
- **Problème :** la meta de la page peinture cite les « fins de bail » (carte masquée sans C17) ; celle des cloisons cite « combles » et « isolantes » (C16). Le H1 et le chapeau des cloisons contiennent aussi « isolantes » et « combles » en dur.
- **Impact :** faible.
- **Correction :** aligner meta, H1 et chapeau une fois C16 et C17 tranchés (textes soumis à confirmation : non modifiés).
- **Priorité :** basse.

**O7. Images**
- Toutes les images ont un `alt` descriptif, des dimensions et un format moderne. Points mineurs : la même image Open Graph sur toutes les pages (une image par page service améliorerait le partage) ; le logo PNG de 352 px est affiché plus petit (4 Ko d'économie selon Lighthouse) ; la mention « Illustration » entre dans le texte d'ancre des cartes de services (« Illustration Peinture Murs et plafonds… »). Priorité basse.

**O8. Maillage interne**
- Profondeur 1 pour toutes les pages, ancres descriptives (« Voir l'isolation acoustique », « Toutes les réalisations en placo »). Les pages services lient les réalisations filtrées (`realisations.html?filtre=placo`) : sans risque, le canonical de la page réalisations ne garde pas le paramètre. À ajouter quand les fiches projets existeront : un lien de chaque fiche vers sa page service, et de chaque page service vers 2 ou 3 fiches. Priorité basse.

### 2.3 Contenu

**C1. Pages services courtes une fois le gabarit retiré**
- **Problème :** les pages services comptent 486 à 625 mots dans `<main>`, mais environ la moitié est commune aux quatre (formulaire, bandeaux de preuves, méthode). Texte propre à chaque page : placo ~326 mots, isolation acoustique ~305, cloisons ~308, **peinture ~188**.
- **Impact :** élevé. Ce sont les pages qui doivent se classer sur « faux plafond Genève », « isolation phonique appartement Genève », « entreprise de peinture Genève ». Le concurrent genevois le plus avancé en SEO publie une page par service d'environ 1'500 mots (`docs/analyse-marche.md` §3).
- **Preuve :** similarité par 5-grammes entre pages services : 32 à 39 % ; 48 à 62 % des 5-grammes de chaque page se retrouvent sur les quatre (script d'exploration du 01.11.2026).
- **Correction :** ajouter 300 à 400 mots propres par page, sans alourdir la mise en page : 3 ou 4 questions de FAQ de plus (délais, préparation, matériaux, travaux en immeuble habité), un paragraphe « comment se passe ce chantier chez vous », et le lien vers 2 ou 3 réalisations du même métier. Peinture en premier. Le choix CRO de réduire le texte visible reste compatible : les réponses de FAQ sont dans le DOM, repliées.
- **Priorité :** haute.

**C2. Aucun prix en CHF**
- **Problème :** les questions « Combien coûte… » répondent sans fourchette (C31 non fourni).
- **Impact :** élevé (clics et citations par les IA).
- **Preuve :** l'autocomplétion montre des requêtes de prix nombreuses : « cloison placo prix m2 », « faux plafond prix m2 », « isolation phonique appartement prix m2 », « prix peinture appartement 100m2 ». Sur ces requêtes, notre outil ne fait ressortir que des guides français en euros ([travaux.com](https://www.travaux.com/platre/guide-des-prix/cloison), [La Maison Saint-Gobain](https://www.lamaisonsaintgobain.fr/guides-travaux/amenagement-interieur/prix-d-une-cloison)) : la place d'une réponse suisse en CHF est libre. Les plateformes suisses publient des fourchettes que les IA reprennent (`docs/v2/concurrence-romandie.md` §4).
- **Correction :** obtenir du client 4 cas types chiffrés (C31), puis publier `prix.html` (annexe B) et reprendre une phrase de fourchette dans chaque FAQ de prix.
- **Priorité :** haute.

**C3. Preuves sans lieu ni année en production**
- **Problème :** en production, les projets s'intitulent « Hall d'immeuble », « Salle publique », « Grand local » ; aucune commune, aucune année (C25, C22 non confirmés). Les références nommées restent une liste.
- **Impact :** élevé pour le local et le GEO : une page qui dit « faux-plafond acoustique, salle communale de Plan-les-Ouates, 2015 » est rattachable à un lieu et citable ; « Salle publique » ne l'est pas.
- **Correction :** confirmer C25 et C22 (lieux, prestations, années, accords), puis publier les fiches projets (annexe B, P1).
- **Priorité :** haute.

**C4. Page peinture : la plus disputée, la moins fournie**
- **Problème :** ~188 mots propres, aucune vraie photo de peinture (C40), requête la plus concurrentielle de Genève (`docs/v2/concurrence-romandie.md` §1 point 4). Autocomplétion : « entreprise de peinture geneve les mieux notés » (le critère des avis apparaît dans la requête).
- **Impact :** moyen. En référencement naturel, cette page servira surtout les clients qui connaissent déjà Andy (régies, clients placo).
- **Correction :** shooting photo (C40), FAQ de fin de bail pour les régies (C17), et avis Google : sur cette requête, les avis comptent davantage que le texte.
- **Priorité :** moyenne.

**C5. Pas encore de guides**
- Le calendrier de `docs/v2/strategie-acquisition.md` §3.2 (un guide par mois) n'est pas commencé. Les requêtes « bruit voisin du dessus » ne renvoient qu'à des forums et guides français (`docs/v2/concurrence-romandie.md` §2.1, et notre relevé du 01.11 : [forums Futura](https://forums.futura-sciences.com/habitat-bioclimatique-isolation-chauffage/957358-isolation-phonique-appartement.html), [ootravaux](https://www.ootravaux.fr/construction-renovation/isolation/isolation-phonique-appartement.html)). Priorité moyenne (long terme).

**C6. Confiance (E-E-A-T) : bonne base**
- Raison sociale, IDE avec lien Zefix, histoire datée (2007, 2010, 2023), but social cité, mentions légales et politique de confidentialité. Manquent les noms des associés (C10) et une signature humaine. Priorité basse.

### 2.4 Local

**L1. Fiche Google : existence inconnue, aucun avis nulle part**
- **Problème :** la fiche Google n'a pas pu être consultée (Google exige JavaScript et renvoie un captcha à nos outils). Aucun avis n'a été trouvé sur les plateformes publiques.
- **Impact :** élevé. Google classe les fiches locales selon la pertinence, la distance et la notoriété, dont les avis ([Google](https://support.google.com/business/answer/7091)). Selon une étude américaine citée dans `docs/analyse-marche.md` §2.6, la carte apparaît dans 93 % des recherches locales de type « près de chez moi » ; ce taux n'a pas été mesuré en Suisse.
- **Preuve :** local.ch « Pas encore d'avis » (01.11.2026) ; search.ch 0 avis, Yelp 0 avis, fiche non revendiquée (`docs/v2/dossier-client.md` D2, D10) ; recherche « Andy Construct Chanton avis Google Maps Carouge » sans résultat pertinent.
- **Correction :** voir les recommandations de fiche ci-dessous et la campagne d'avis (L4).
- **Priorité :** critique.

**L2. Adresse de domiciliation : fiche en « zone desservie »**
- La Route des Acacias 48 accueille 92 autres entreprises actives (`docs/v2/dossier-client.md` R6). Si personne ne reçoit de clients sur place aux heures d'ouverture, l'adresse doit être **masquée** et la fiche déclarée en zone desservie ([Google, consignes](https://support.google.com/business/answer/3038177) ; [zones desservies](https://support.google.com/business/answer/9157481)). L'adresse reste sur le site (mentions légales, NAP, JSON-LD) : les deux se concilient, puisque le registre du commerce publie cette adresse.

**Recommandations de fiche Google (à appliquer par l'agence en tant que gestionnaire, les associés restant propriétaires) :**

| Champ | Proposition | Condition |
|---|---|---|
| Nom | « Andy Construct » (nom utilisé sur le site et le logo, sans mot-clé ajouté) | – |
| Catégorie principale | Plâtrier (*Plasterer*) : cœur du métier, cohérent avec le but social et la fiche GGE | Libellé exact à choisir dans l'interface française |
| Catégories secondaires | Peintre en bâtiment (*Painter*) ; Entreprise de cloisons sèches ou plaquiste (*Drywall contractor*) ; Entreprise d'isolation (*Insulation contractor*) ; insonorisation si la catégorie existe | Aucune catégorie hors des 4 métiers (ni entreprise générale, ni plafonds tendus) |
| Adresse | Masquée | Si aucun accueil de clients à Carouge (C29) |
| Zone desservie | Canton de Genève, puis districts de Nyon et de Lausanne ; le reste de la Romandie seulement si le client se déplace réellement pour des particuliers (C21) | Google conseille une zone de l'ordre de 2 heures de route au plus ([Google](https://support.google.com/business/answer/9157481)) |
| Horaires | Lun-ven 7 h-18 h, comme local.ch | Après C03 |
| Téléphone | +41 22 771 20 15 (principal), mobile en secondaire | – |
| Site | `https://www.andyconstruct.ch/?utm_source=google&utm_medium=organic-local&utm_campaign=gbp-site` | – |
| Lien de rendez-vous | `https://www.andyconstruct.ch/contact.html?utm_source=google&utm_medium=organic-local&utm_campaign=gbp-rdv#demande` | L'ancre `#formulaire` du document v2 n'existe pas |
| Services | Un service par prestation réelle sous chaque catégorie (cloison, doublage, faux-plafond, caisson ; peinture des murs et plafonds, cage d'escalier ; doublage et faux-plafond acoustiques ; cloison isolante, plafond de cave ou de garage) | Correction acoustique après C18, combles après C16 |
| Description | 750 caractères au plus : 4 métiers, Carouge, depuis 2007, régies, architectes, communes, particuliers, Suisse romande ; aucun superlatif | – |
| Photos | Vraies photos de chantier uniquement (jamais les illustrations sous licence du site), logo, une photo de l'équipe si les associés l'acceptent ; puis 4 à 8 photos par mois | Accord des clients pour les lieux identifiables |
| Posts | Un « chantier terminé » par mois (3 photos, lieu, besoin, solution) | – |
| Questions et réponses | Ne pas y investir : Google a fermé l'API le 3.11.2025 ([Google](https://developers.google.com/my-business/content/qanda/change-log)) ; la FAQ du site et les services décrits nourrissent les réponses | – |

**L3. NAP : 8 annuaires au moins affichent une donnée fausse ou dépassée**

| Entité / annuaire | URL | Faits observés | Source de vérité | Correction | Accès | Vérifié le |
|---|---|---|---|---|---|---|
| Zefix (registre) | [zefix.ch](https://www.zefix.ch/fr/search/entity/list?name=CHE-113.706.162) | Route des Acacias 48, 1227 Carouge GE ; « existant » ; but : faux-plafonds, cloisons, isolations intérieures, plâtrerie, peinture | – | Référence | Public | 01.11.2026 (API) |
| Moneyhouse | [moneyhouse.ch](https://www.moneyhouse.ch/fr/company/andy-construct-chanton-cie-3813590051) | Siège Carouge ; Chêne-Bourg en « autre adresse » ; inscription 27.06.2007 | Zefix | Aucune (reflète le registre) | – | 01.11.2026 |
| local.ch | [fiche](https://www.local.ch/fr/d/carouge-ge/1227/revetement-des-plafonds-et-plafonds-suspendus/andy-construct-chanton-cie-OGrZ5DP4atJqYki9WoTjPg) | Carouge, 022 771 20 15, mobile, e-mail bluewin, lun-ven 7-18 h, lien `http://www.andyconstruct.ch`, 0 avis ; ancien logo bleu (dossier D1) | Site | Lien en https, nouveau logo, texte aligné sur les 4 métiers, e-mail après C30 | Client (Premium) | 01.11.2026 |
| search.ch | [fiche](https://search.ch/tel/carouge/route-des-acacias-48/andy-construct-chanton-cie) | Carouge (l'ancienne URL Chêne-Bourg redirige), fixe, mobile, lien `http://www.andyconstruct.ch/` ; catégorie « Sonorisation » erronée (dossier D2) | Site | Retirer « Sonorisation », lien https | Client (même source que local.ch) | 01.11.2026 |
| GGE | [fiche](https://gge.ch/entreprises-2/andy-construct-chanton-cie/) | Carouge, **mobile seul**, lien http | Site | Ajouter le fixe, lien https | Client | 01.11.2026 |
| LinkedIn | [page](https://www.linkedin.com/company/andy-construct-chanton-et-cie) | « Facilities Services », « Les Acacias, Geneva », « faux plafonds, tissu tendu et cloisons », 9 abonnés | Site | Secteur construction, Carouge, 4 métiers | Client (admin de la page) | 01.11.2026 |
| firmen.ch | [fiche](https://www.firmen.ch/de/Chene+Bourg/Andy+Construct+Chanton+Cie/119171/portrait.htm) | **Avenue de Bel-Air 57, Chêne-Bourg** ; lien http | Zefix | Nouvelle adresse | Formulaire de l'annuaire | 01.11.2026 |
| Kompass | (anti-robot) | Catégorie « Carpentry and structural woodwork » (charpenterie), d'après l'extrait | Zefix | Catégorie plâtrerie / faux-plafonds | Formulaire Kompass | 01.11.2026 (extrait) |
| edirex.ch | (anti-robot) | « Chêne-Bourg » d'après le titre | Zefix | Nouvelle adresse | Formulaire | 01.11.2026 (extrait) |
| Yelp | [fiche](https://fr.yelp.ch/biz/andy-construct-ch%C3%AAne-bourg) | Chêne-Bourg, « Peintre » seul, non revendiquée | Site | Revendiquer, corriger | Client | 31.10.2026 (dossier D10) |
| Infobel | (anti-robot) | **Doublon** : une fiche Chêne-Bourg, une Carouge | Zefix | Supprimer le doublon | Formulaire | 31.10.2026 (D11) |
| Cybo, MapsArch, Esprit de Genève, guidegeneve | voir `dossier-client.md` D12-D15 | Chêne-Bourg ; catégories erronées (commerce de gros de produits chimiques, appareils auditifs, menuiserie) | Zefix | Corriger ou demander la suppression | Formulaires | 31.10.2026 |
| architecteromand.ch | – | Fiches en 404, encore affichées par les moteurs à Chêne-Bourg | – | Recréer une fiche à Carouge si l'annuaire le permet | – | 01.11.2026 |

Ordre conseillé : local.ch et search.ch (même source, Swisscom Directories, utilisés par les applications de navigation), LinkedIn, GGE, puis les autres. L'e-mail (C30) doit être décidé avant, pour ne faire le tour qu'une fois.

**L4. Campagne d'avis**
- Demander un avis à chaque client satisfait **et** non satisfait, par un message neutre et le lien direct de la fiche, sans incitation ni texte imposé ([règlement des avis Google](https://support.google.com/contributionpolicy/answer/7400114)). Commencer par les clients des 24 derniers mois, régies et architectes compris. Répondre à chaque avis. Les workflows prévus (WF03x, demande à J+2 et relance à J+9) suffisent, une fois la fiche active.
- Ne jamais reprendre la note Google dans le JSON-LD du site : les notes affichées par l'entreprise sur ses propres pages ne donnent pas d'étoiles ([Google, 2019](https://developers.google.com/search/blog/2019/09/making-review-rich-results-more-helpful)).

**L5. Bing Places et Apple Business Connect**
- Bing pèse environ 11 % des recherches en Suisse et alimente la recherche de ChatGPT (sources dans `docs/analyse-marche.md` §2.6). Créer les deux fiches avec le même contenu que la fiche Google, en M1. Priorité moyenne.

### 2.5 Données structurées

**D1. Graphe complet et valide**
- Accueil : `HomeAndConstructionBusiness` (`@id` `#entreprise`) avec `legalName`, `identifier` (IDE), `foundingDate`, `foundingLocation`, adresse, `geo` (46.18935, 6.13236 ; local.ch publie 46.189383, 6.132321), deux `contactPoint`, `areaServed` (7 cantons et régions), `knowsAbout`, `hasOfferCatalog` (4 services avec URL), `sameAs` ; `WebSite`, `WebPage`, `FAQPage`. Pages services : `WebPage` + `BreadcrumbList` + `Service` (`provider` → `#entreprise`) + `FAQPage`. Réalisations : `CollectionPage` + `ImageGallery`. Professionnels : `DigitalDocument` (PDF). Contact : `ContactPage`. Entreprise : `AboutPage`.
- **Preuve :** validator.schema.org, 11 pages : 0 erreur, 0 avertissement. Comparaison programmatique des 18 questions de FAQ avec le texte HTML : 0 écart. Aucune note ni avis auto-attribué (conforme).

**D2. `sameAs` trop court et une cible dépassée**
- **Problème :** `sameAs` = local.ch + LinkedIn ; la page LinkedIn décrit encore l'ancienne offre (L3).
- **Impact :** moyen (rapprochement d'entité par Google et par les IA).
- **Correction :** après mise à jour de LinkedIn, ajouter search.ch, l'URL de la fiche Google une fois vérifiée, et la fiche GGE (déjà prévue dès que C11 est confirmé). Facebook : non, c'est un profil personnel.
- **Priorité :** moyenne.

**D3. Horaires absents tant que C03 n'est pas confirmé**
- Cohérent avec le texte visible. Le générateur les ajoute automatiquement quand C03 est coché. Priorité basse.

**D4. Pages services : l'entité n'est décrite que par son `@id`**
- Les pages services référencent `#entreprise` sans le décrire. C'est valide ; certains analyseurs lisent chaque page isolément. Ajouter sur chaque page un nœud minimal (`@id`, `name`, `url`) est une amélioration possible, sans urgence. Priorité basse.

**D5. Espace en fin de réponse de FAQ [corrigé]**
- La réponse « Intervenez-vous hors de Genève ? » se terminait par une espace en production. Corrigé (§5). Priorité faite.

**D6. Précision de `foundingDate`**
- « 2007 » pourrait devenir « 2007-06-01 » (début d'activité, `dossier-client.md`). Priorité basse.

### 2.6 GEO (visibilité dans les IA)

**G1. Entité presque invisible**
- **Problème :** le nom de l'entreprise ne déclenche ni suggestion ni résultat propre.
- **Impact :** élevé. Une IA ne cite pas une entreprise qu'elle ne sait pas rattacher à un lieu et à un métier.
- **Preuve :** autocomplétion « andy construct » (`gl=ch`, 01.11.2026) : uniquement des entreprises étrangères (« andy construction llc »…). Notre outil, sur « "Andy Construct" Carouge plâtrerie » : aucun résultat pertinent ; sur « "Andy Construct, Chanton & Cie" » : uniquement Moneyhouse, search.ch, local.ch, firmen.ch, Kompass, architecteromand, edirex. `site:andyconstruct.ch` : 6 pages de l'ancien site, sur les deux hôtes.
- **Correction :** fiche Google, nettoyage des annuaires (L3), page LinkedIn, avis, fiches projets. Ce sont les sources que les moteurs et les IA croisent.
- **Priorité :** haute.

**G2. Sources contradictoires sur l'entité**
- LinkedIn (« Facilities Services », « tissu tendu »), Kompass (charpenterie), MapsArch (appareils auditifs), firmen.ch et Yelp (Chêne-Bourg) disent autre chose que le site. Une IA qui agrège ces sources hésitera sur le métier et l'adresse. Correction : L3. Priorité haute.

**G3. `llms.txt` : complet et cohérent**
- Nom, raison sociale, IDE, histoire, adresse, téléphones, zone, ce que l'entreprise ne fait pas, 4 prestations, méthode, références, pages et documents. Il suit les confirmations (OMC et horaires retirés en production). À mettre à jour à chaque fiche projet (le générateur le fait). Aucun grand fournisseur d'IA ne s'engage à le lire ([llmstxt.org](https://llmstxt.org/)) : son coût est nul, son effet incertain.

**G4. Passages citables trop pauvres en faits**
- **Problème :** les réponses de FAQ (35 mots au plus) sont claires mais sans chiffre en production : ni prix, ni délai, ni épaisseur (C18, C31, C41).
- **Impact :** moyen. Les réponses génératives reprennent les passages qui contiennent un fait vérifiable.
- **Correction :** après confirmation, une phrase de fait par réponse (« un doublage acoustique prend en général 7 à 10 cm » existe déjà en preview, C18). Ajouter sur l'accueil, en texte visible, une phrase d'identité complète (« Andy Construct, entreprise de plâtrerie, de peinture et d'isolation intérieure à Carouge, active depuis 2007 dans toute la Suisse romande ») ; elle n'existe aujourd'hui que dans le pied de page.
- **Priorité :** moyenne.

**G5. Bing Webmaster Tools et IndexNow**
- La recherche de ChatGPT s'appuie surtout sur l'index de Bing (`docs/analyse-marche.md` §2.6). Vérifier le site dans Bing Webmaster Tools le jour J (import depuis la Search Console), soumettre le sitemap, et envisager IndexNow pour signaler chaque nouvelle fiche projet ([IndexNow](https://www.bing.com/indexnow)). Priorité moyenne, gain rapide.

**G6. Wikipedia et Wikidata : non pertinents**
- Une entreprise de cette taille, sans couverture indépendante, ne remplit pas les critères de notoriété ([Wikidata](https://www.wikidata.org/wiki/Wikidata:Notability)) ; un élément créé par l'entreprise serait probablement supprimé. Mieux vaut des sources tierces réelles (GGE, communes, presse professionnelle). Aucune action.

**G7. Robots des IA autorisés**
- `robots.txt` de production n'en bloque aucun. À garder.

**G8. Suivi**
- Test trimestriel de 10 questions dans ChatGPT, Perplexity, Google (mode IA) et Copilot, consigné dans le rapport mensuel (`docs/v2/strategie-acquisition.md` §3.3). Questions de départ : « entreprise de plâtrerie à Carouge », « qui pose des faux-plafonds acoustiques pour des salles communales à Genève », « entreprise pour isoler le plafond d'un garage sous une chambre à Genève », « plâtrier-peintre pour régies à Genève », « Andy Construct avis ».

### 2.7 Autorité et liens

**A1. Profil de liens observable**
- **Problème :** les seuls liens trouvés viennent d'annuaires (local.ch, search.ch, GGE, firmen.ch en `http://www.andyconstruct.ch` ; LinkedIn en `https://`). Aucune mention par un client, une commune, un architecte ou la presse (`docs/v2/dossier-client.md` T1-T4, confirmé le 01.11 : la recherche « "andyconstruct.ch" » hors du site ne renvoie rien de pertinent).
- **Impact :** élevé à moyen terme : face aux sites des concurrents établis, le contenu seul ne suffira pas sur « faux plafond Genève » ou « entreprise de peinture Genève ».
- **Preuve :** pages des annuaires (liens extraits le 01.11.2026). Sans Ahrefs ni Semrush, le nombre de domaines référents n'est **pas mesuré** ; la Search Console (rapport Liens) le donnera après la bascule.
- **Priorité :** moyenne.

**A2. Pistes de liens propres et réalistes (sans achat)**

| Piste | Pourquoi | Ce qu'il faut | Qui | Effort |
|---|---|---|---|---|
| GGE, fiche membre | Lien et mention d'une organisation professionnelle genevoise | Confirmer l'adhésion (C11), compléter la fiche (fixe, lien https) | Client | Faible |
| Association de la branche (Gypserie Peinture Genève, FREPP) | Annuaire des membres, crédibilité auprès des régies ; Andy n'est pas membre de GPG (`concurrence-romandie.md` §1 point 6) | Décision d'adhésion (en attente, `HANDOFF.md` §8) | Client | Moyen |
| Communes et institutions clientes (Plan-les-Ouates, Collonge-Bellerive, Ville de Genève) | Mention locale d'autorité | Demander, au moment de l'accord de citation (C22), si la commune publie la liste des entreprises d'un chantier ou un article d'inauguration ; vérifier si Carouge tient un répertoire des entreprises de la commune | Agence | Moyen |
| Architectes partenaires | Pages « entreprises mandatées », fiches de projet | Proposer une fiche projet commune avec crédits croisés (accord écrit) | Client et agence | Moyen |
| simap.ch | Les avis d'adjudication publient le nom de l'adjudicataire : mention vérifiable de l'entité | Répondre aux appels d'offres (veille WF08) | Client | Variable |
| Fournisseurs (plaques, isolants, peintures) | Certains publient des listes d'applicateurs ou des références de chantier | Demander aux représentants du client si un tel programme existe | Client | Faible |
| Presse professionnelle et locale | Reportage de chantier (Batimag, déjà cité en v2) | Un chantier public terminé, avec photos et accord du maître d'ouvrage | Agence | Moyen |
| Houzz (aucun profil), architecteromand.ch (fiches en 404) | Annuaires utilisés par architectes et particuliers | Créer ou recréer les fiches, NAP identique | Agence | Faible |

À éviter : achat de liens, échanges de liens, réseaux de sites, inscriptions en masse dans des annuaires sans lecteurs.

---

## 3. Plan d'action priorisé

### 3.1 Critique (avant ou au lancement)

| # | Action | Qui | Quand | Contrôle |
|---|---|---|---|---|
| 1 | Décider C16 : nom « Cloisons isolantes » et adresse `cloisons-isolantes.html` (301 depuis l'ancien nom) | Client, chef de projet ; développeur pour le renommage | Avant la mise en ligne | Title, H1, menu, URL et sitemap alignés |
| 2 | Vérifier si une fiche Google existe et qui la détient ; la revendiquer avec `contact@andyconstruct.ch` (ou l'adresse décidée) ; agence en gestionnaire | Client (accès), agence | Semaine 0 | Fiche vérifiée, en zone desservie |
| 3 | Propriété « Domaine » dans la Search Console (DNS) et Bing Webmaster Tools | Agence, client (accès DNS) | Avant J0 | Propriétés vérifiées |
| 4 | Contrôler sur l'hébergeur : 301 (annexe C), compression, en-têtes de cache des fichiers statiques, absence de boucle HTTPS | Développeur | J0 | Check-list §4 verte |
| 5 | Passer le dépôt GitHub en privé | Client ou agence (propriétaire du dépôt) | Avant J0 | Dépôt en 404 hors connexion |
| 6 | Déployer dans une racine vide ; archiver Joomla hors de la racine web | Développeur | J0 | `/administrator/` en 404 |

### 3.2 Fort impact (mois 1 à 3)

| # | Action | Qui | Quand |
|---|---|---|---|
| 7 | Campagne d'avis (clients des 24 derniers mois, puis chaque fin de chantier) | Client, agence (messages, WF03x) | Dès la fiche active |
| 8 | Nettoyage NAP (tableau L3), dans l'ordre indiqué | Agence, avec les accès du client | Mois 1 |
| 9 | Confirmations qui débloquent le contenu : C03 (horaires), C25 et C22 (lieux, années, accords), C31 (prix), C11 (GGE), C18 (acoustique), C30 (e-mail) | Client | Séance de validation |
| 10 | +300 à 400 mots propres par page service, vocabulaire romand, phrase d'identité sur l'accueil | Agence (rédaction), client (validation) | Mois 1 |
| 11 | 4 premières fiches projets (Plan-les-Ouates, Collonge-Bellerive, Conservatoire, Alhambra si accords) | Agence, client (photos, informations) | Mois 1-2 |
| 12 | Page « Prix indicatifs » | Agence, client (C31) | Mois 2 |

### 3.3 Gains rapides

| # | Action | Qui |
|---|---|---|
| 13 | LinkedIn : secteur, description, localité, lien https | Client ou agence |
| 14 | GGE : numéro fixe, lien https | Client |
| 15 | local.ch, search.ch : lien https, retrait « Sonorisation », logo, texte des 4 métiers | Client ou agence |
| 16 | Bing Places, Apple Business Connect | Agence |
| 17 | `sameAs` complété après la fiche Google et LinkedIn | Développeur (`tools/build/page_accueil.py`) |
| 18 | Lien de la fiche Google avec `#demande` (et non `#formulaire`) | Agence |

### 3.4 Long terme (mois 3 à 12)

| # | Action | Qui |
|---|---|---|
| 19 | Un guide par mois (annexe B) | Agence |
| 20 | Pages canton (GE, puis VD) seulement avec 2 fiches projets dans le canton | Agence |
| 21 | Liens de l'annexe A2 (GGE, association, communes, architectes, presse) | Client et agence |
| 22 | `lastmod` et dates légales fondés sur le contenu réel (T6) | Développeur |
| 23 | HSTS (T8) | Développeur, J+7 à J+30 |
| 24 | Test GEO trimestriel (G8) et relevé de positions trimestriel depuis Genève | Agence |
| 25 | À 8 semaines : recaler la carte des mots-clés sur les requêtes réelles de la Search Console ; décider d'une page faux-plafonds séparée si les données la justifient | Agence |

### 3.5 Ce qui reste à décider par le client

C16 (nom et URL du 4e service), C03 (horaires), C25 et C22 (lieux, années, accords des références), C31 (fourchettes de prix), C30 (e-mail sur le domaine), C29 (accueil au bureau de Carouge, qui conditionne l'adresse visible de la fiche Google), C21 (particuliers hors de Genève, qui conditionne la zone desservie), C11 (GGE), C40 (photos de peinture), adhésion GPG ou FREPP, accès à la fiche Google et aux annuaires.

---

## 4. Plan de migration

Hôte unique retenu : `https://www.andyconstruct.ch/` (celui des annuaires et de l'ancien site). Référence : [déplacement de site avec changement d'URL](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes).

### J-7 à J-1

- [ ] Search Console : propriété « Domaine » (enregistrement DNS TXT) ; noter le nombre de pages indexées et les requêtes de l'ancien site (base de comparaison).
- [ ] Bing Webmaster Tools : import depuis la Search Console.
- [ ] Sauvegarde complète de l'ancien site (fichiers et base Joomla), conservée hors de la racine web.
- [ ] Générer la production : `python3 tools/build/build.py --mode production --out dist/` ; contrôles du build verts.
- [ ] Vérifier que `site/api/config.php` est prêt (formulaire) et que PHP 8.1+ est disponible.
- [ ] Relever les positions de marque de départ (navigation privée, depuis Genève) : « Andy Construct », « Andy Construct Carouge », « andyconstruct », « Andy Construct Chanton ».

### Jour J

- [ ] Déployer dans une racine vide ; l'ancien Joomla archivé hors de la racine.
- [ ] Tester les 301 (annexe C) sur l'hôte réel. Exemple pour une URL :
  `curl -sI http://andyconstruct.ch/index.php/presentation` → une seule réponse `301` avec `Location: https://www.andyconstruct.ch/entreprise.html`, puis `200`.
- [ ] Tester `https://www.andyconstruct.ch/` (200), `https://www.andyconstruct.ch/index.html` (301 vers `/`), `https://andyconstruct.ch/placo.html` (301 vers www), une URL inconnue (404 avec la page 404).
- [ ] En-têtes : `content-encoding` (br ou gzip) sur HTML, CSS, JS ; `Cache-Control` sur CSS, JS, images, polices (T1) ; `Content-Security-Policy` sur le HTML ; **aucun** `X-Robots-Tag` ni `noindex` sur les pages indexables.
- [ ] `robots.txt`, `sitemap.xml` et `llms.txt` en 200 à la racine.
- [ ] Search Console : soumettre `sitemap.xml` ; inspection d'URL et demande d'indexation pour l'accueil et les 4 pages services (une seule fois).
- [ ] Bing Webmaster Tools : soumettre le sitemap.
- [ ] Fiche Google : lien du site et lien de rendez-vous mis à jour (avec UTM, ancre `#demande`).
- [ ] Formulaire : une demande de test reçue (e-mail interne et accusé).

### J+1 à J+7

- [ ] Search Console, rapport Pages : surveiller « Introuvable (404) » (seules les anciennes images `/images/…` sont attendues) et « Page avec redirection » (anciennes URL, normal).
- [ ] Vérifier qu'aucune ancienne URL ne répond 200 dans les résultats (`site:andyconstruct.ch` dans Google).
- [ ] Mettre à jour les liens des annuaires vers `https://www.andyconstruct.ch/` (L3).
- [ ] Lighthouse mobile sur l'hôte réel (accueil, placo, réalisations) : LCP sous 2,5 s.

### J+30

- [ ] Search Console : pages indexées (11 attendues), requêtes de marque, premières requêtes hors marque ; rapport Core Web Vitals si les données existent.
- [ ] Anciennes URL disparues des résultats ; garder les 301 au moins un an (en pratique : sans limite, elles ne coûtent rien).
- [ ] Positions de marque : l'accueil sort en premier sur « Andy Construct » et « Andy Construct Carouge ».
- [ ] Fiche Google : statistiques (appels, clics vers le site, itinéraires), nombre d'avis.
- [ ] Activer HSTS si aucune erreur HTTPS (T8).
- [ ] Retirer l'ancien Universal Analytics s'il subsiste quelque part ; vérifier que Umami compte les visites.

### J+90

- [ ] Recaler la carte des mots-clés (annexe B) sur les requêtes réelles ; appliquer `rankings-push.md` aux pages en positions 8 à 20.
- [ ] Bilan : demandes qualifiées par source (organique, fiche Google, direct), comparé à la base de départ.

---

## 5. Corrections appliquées

Toutes dans `tools/build/`, puis régénération (`python3 tools/build/build.py` vers `site/`, `--mode production` et `--mode verification` dans le scratchpad). Contrôles du build verts dans les 3 modes (liens et ancres valides), `php site/api/tests/run.php` : 266 vérifications réussies, 0 échec. Redirections testées sur Apache 2.4.58 local (41 cas, HTTP et HTTPS, avec et sans www) ; données structurées validées (11 pages, 0 erreur).

| # | Fichier | Défaut | Correction |
|---|---|---|---|
| 1 | `tools/build/page_contact.py` | Meta description de `contact.html` : « du lundi au vendredi » publié en production alors que les horaires (C03) n'y sont pas confirmés (O3) | La mention dépend de `V('C03', …)` : présente en preview et une fois C03 confirmé, absente sinon |
| 2 | `tools/build/common.py` | Liens internes vers `index.html`, doublon de l'URL canonique `/` (T3) | En production, `href="index.html"` devient `href="./"` à l'assemblage des pages ; preview et vérification inchangés |
| 3 | `tools/build/seo.py` | `/index.html` répondait 200 en doublon de `/` (T3) | `.htaccess` de production : 301 `/index.html` → `https://www.andyconstruct.ch/`, limitée à la requête du visiteur (`THE_REQUEST`), sans effet sur `DirectoryIndex` |
| 4 | `tools/build/seo.py` | Version de validation : PDF, images et fichiers texte sans consigne de non-indexation (T4) | `.htaccess` de preview et de vérification : `Header always set X-Robots-Tag "noindex, nofollow"` |
| 5 | `tools/build/seo.py` | `robots.txt` de preview en `Disallow: /`, qui empêche les robots de lire le noindex (T4) | Exploration ouverte (`Disallow:` vide) et commentaire explicatif ; la production garde son `robots.txt` |
| 6 | `tools/build/composants.py` | Espace en fin de texte dans le JSON-LD FAQPage (D5) | Question et réponse nettoyées (`strip()`) avant l'export |
| 7 | `tools/build/page_autres.py` | Date des pages légales « 1 novembre 2026 » | « 1er » pour le premier jour du mois |

Fichiers régénérés dans `site/` (preview) : `robots.txt`, `.htaccess` (corrections 4 et 5). `sitemap.xml`, `mentions-legales.html` et `confidentialite.html` changent aussi, uniquement par la date de génération (T6).

Non modifiés (recommandations seulement) : titles, H1, textes soumis à confirmation (`T('Cxx', …)`), structure des pages, direction artistique, `site/api/`, `automation/`, `docs/v2/`, `docs/v3/`, `livrables/`.

---

## Annexe A. Audit des titles et des meta (production, 01.11.2026)

Longueur en pixels : estimation en Arial 20 px (rendu des titres de Google sur ordinateur).

| Page | Title actuel | Car. / px | H1 | Meta (car.) | Statut |
|---|---|---|---|---|---|
| `/` | Plâtrerie, peinture et isolation à Genève \| Andy Construct | 58 / ~504 | Placo, peinture, acoustique : la rigueur des chantiers publics | 156 | Title bon ; H1 sans lieu (O2) |
| `placo.html` | Placo, cloisons et faux-plafonds à Genève \| Andy Construct | 58 / ~527 | Placo : cloisons, doublages et faux-plafonds | 147 | Bon |
| `peinture.html` | Entreprise de peinture intérieure à Genève \| Andy Construct | 59 / ~531 | Peinture intérieure : murs, plafonds, cages d'escalier | 149 | Bon ; meta cite les fins de bail (O6) |
| `isolation-acoustique.html` | Isolation phonique et acoustique à Genève \| Andy Construct | 58 / ~532 | Isolation phonique et acoustique : moins de bruit chez vous | 141 | Bon |
| `cloisons-isothermes.html` | Cloisons isothermes, cave et garage à Genève \| Andy Construct | 61 / ~569 | Cloisons isothermes et isolantes : caves, garages et combles | 132 | Terme à changer (O5) |
| `realisations.html` | Réalisations : placo, peinture, isolation \| Andy Construct | 58 / ~494 | Réalisations et références | 143 | Sans lieu |
| `professionnels.html` | Régies et architectes : plâtrerie, peinture \| Andy Construct | 60 / ~512 | Régies, architectes, communes : plâtrerie, faux-plafonds et peinture | 142 | Bon |
| `entreprise.html` | L'entreprise, à Carouge depuis 2007 \| Andy Construct | 52 / ~476 | Andy Construct, entreprise de Carouge depuis 2007 | 141 | Bon |
| `contact.html` | Contact et demande de devis, Genève \| Andy Construct | 52 / ~494 | Contact et demande de devis | 121 (143 avec C03) | Bon après correction |
| `mentions-legales.html` | Mentions légales \| Andy Construct | 33 / ~303 | Mentions légales | 137 | Bon |
| `confidentialite.html` | Protection des données \| Andy Construct | 39 / ~363 | Protection des données | 132 | Bon |
| `merci.html`, `404.html` | (noindex) | – | – | – | Hors index, normal |

Propositions (à valider ; une seule par page, sauf les pages qui comptent le plus) :

| Page | Title actuel | Proposition | Raison |
|---|---|---|---|
| `/` | Plâtrerie, peinture et isolation à Genève \| Andy Construct | (A) garder ; (B) « Entreprise de plâtrerie et peinture à Genève \| Andy Construct » (61 car.) | (B) reprend la formulation de l'autocomplétion « entreprise plâtrerie peinture genève » ; à tester seulement après 8 semaines de données, pour mesurer l'effet |
| `placo.html` | Placo, cloisons et faux-plafonds à Genève \| Andy Construct | (A) « Faux-plafonds et cloisons en placo à Genève \| Andy Construct » (59 car.) ; (B) garder | « faux plafond genève » et « entreprise faux plafond geneve » sont suggérées ; « cloison placo genève » ne l'est pas : la requête la plus tapée en tête |
| `cloisons-isothermes.html` | Cloisons isothermes, cave et garage à Genève \| Andy Construct | « Cloisons isolantes, cave et garage à Genève \| Andy Construct » (déjà prévu en preview, C16) | Intention « isotherme » = chambres froides (O5) |
| `realisations.html` | Réalisations : placo, peinture, isolation \| Andy Construct | « Réalisations à Genève et en Suisse romande \| Andy Construct » (59 car.), une fois les lieux publiés (C25) | Ajoute le lieu quand les fiches le prouvent |
| Autres | – | Garder | Alignés sur le H1 et la requête |

Meta descriptions : toutes uniques, sans doublon. Ajouter une fourchette de prix dans les meta des pages services quand C31 sera fourni.

## Annexe B. Carte des mots-clés et pages manquantes

**Signaux utilisés** (aucun volume) : autocomplétion Google `hl=fr`, `gl=ch` (01.11.2026) ; notre outil de recherche (01.11.2026) ; relevés du 31.10.2026 (`concurrence-romandie.md` §2.1). Intention : T transactionnelle, C commerciale, I informationnelle, N navigationnelle.

**Ce qui sort sur ces requêtes (types de pages)**
- « plâtrier Genève », « pose placo Genève » : surtout des **offres d'emploi** (jobup, jooble, jobscout24) ; l'autocomplétion propose « plaquiste genève offre emploi ». Le mot « plâtrier » seul attire des candidats : viser « entreprise de plâtrerie », « plâtrier-peintre ».
- « entreprise plâtrerie peinture Genève », « entreprise de peinture Genève », « gypserie peinture Genève » : **annuaires** (business-monitor.ch, local.ch), fiches LinkedIn et ProvenExpert d'entreprises établies ; le 31.10, sites d'artisans orientés web avec prix affichés (`concurrence-romandie.md` §2.1).
- « faux plafond Genève » : **appels d'offres** (TED, tenderlift : lots CFC 283), une page d'avis Trustpilot (Edelweiss Rénovation), annuaires. Signal B2B net.
- « cloison placo prix Suisse », « isolation phonique appartement Genève », « isolation acoustique plafond Lausanne », « cloison isolante garage cave » : **guides et forums français** (travaux.com, Saint-Gobain, ootravaux, Futura, Knauf France) ; aucune source suisse en CHF.
- « peintre Carouge » : ambigu (artistes, musée de Carouge, Carrouge VD).
- Pack local (carte) : **non observable** (§0) ; à relever à la main depuis Genève, en navigation privée.

**Carte par page**

| Page | Requête principale | Secondaires | Intention | Signal observé | Cannibalisation / remarque |
|---|---|---|---|---|---|
| Accueil | entreprise plâtrerie peinture Genève | gypserie peinture Genève ; plâtrier-peintre Genève ; Andy Construct (marque) | T, C, N | Suggestions « entreprise plâtrerie peinture genève », « entreprise gypserie peinture geneve » | Ne pas viser « faux plafond Genève » (laissé à placo) |
| Placo | faux plafond Genève | entreprise faux plafond Genève ; cloison placo ; doublage placo ; plaquiste Genève ; pose placo | T | « entreprise faux plafond geneve » suggéré ; « cloison placo » + « prix m2 », « phonique » | Si les données montrent deux intentions distinctes (faux-plafond, cloison), envisager une page faux-plafonds à 8 semaines |
| Peinture | entreprise de peinture Genève | peintre en bâtiment Genève ; peinture appartement Genève ; peinture fin de bail ; peinture cage d'escalier | T | « … les mieux notés », « locataire peinture fin de bail » | Requête la plus disputée : les avis Google pèsent plus que le texte |
| Isolation acoustique | isolation phonique appartement Genève | bruit voisin du dessus ; isolation phonique plafond ; doublage acoustique ; faux-plafond acoustique ; correction acoustique salle | T, I | « isolation phonique appartement prix m2 », « … plafond bruit de pas », « bruit voisin du dessus isolation » | La FAQ placo « Une cloison en placo isole-t-elle du bruit ? » renvoie ici : pas de concurrence entre pages |
| Cloisons (C16) | cloison isolante garage | isolation plafond garage (avec chambre au-dessus) ; isoler plafond cave ; doublage isolant mur froid ; isolation combles (si C16) | T, I | « cloison isolante entre garage et habitation », « isolation plafond garage avec chambre au-dessus » | Ne pas viser « cloison isotherme » (chambres froides) |
| Réalisations | réalisations plâtrerie Genève | faux-plafond avant après ; plafond acoustique salle communale | C | – | Gagne en pertinence avec les lieux (C25) |
| Professionnels | entreprise plâtrerie peinture régies Genève | plâtrier-peintre architectes ; lots CFC 271 283 285 ; entreprise second œuvre régie | C (B2B) | Appels d'offres CFC 283 sur « faux plafond Genève » | Garder les codes CFC (C14) en texte visible |
| Entreprise | Andy Construct | Andy Construct Carouge ; Andy Construct Chanton & Cie | N | Aucune suggestion de marque en Suisse aujourd'hui | – |
| Contact | Andy Construct téléphone, adresse | devis plâtrerie Genève | T, N | – | – |

**Pages manquantes, par priorité**

| # | Page | Requêtes visées | Condition de création | Priorité |
|---|---|---|---|---|
| P1 | Fiches projets `realisations/<projet>.html` (Plan-les-Ouates, Collonge-Bellerive, Conservatoire, Alhambra…) | plafond acoustique salle communale ; faux-plafond + commune ; marque + référence | C25 et C22 confirmés, 3 photos ou plus, 250 mots uniques (`architecture-cro.md` §1.3) | Haute |
| P2 | `prix.html` « Prix indicatifs » (4 cas types, compris et non compris, HT ou TTC) | cloison placo prix m2 ; faux plafond prix m2 ; prix peinture appartement ; isolation phonique prix m2 | Fourchettes réelles du client (C31) | Haute |
| P3 | Guide « Bruit des voisins du dessus : isoler ou corriger ? » | bruit voisin du dessus (isolation, que faire, bruit de pas) | Aucune ; prudence sur les performances (C18) | Haute |
| P4 | Guide « Isoler le plafond d'un garage ou d'une cave sous une pièce habitée » | isolation plafond garage avec chambre au-dessus ; isoler plafond cave | C16 décidé | Moyenne à haute |
| P5 | Guide B2B « Travaux en immeuble habité et fins de bail : ce que la régie vérifie » | peinture fin de bail ; travaux immeuble habité régie | C17, C20 | Moyenne |
| P6 | Page ou section « Correction acoustique des salles » (communes, écoles, bureaux) | correction acoustique salle ; plafond acoustique salle communale | C18 ; décider page ou section selon les données à 8 semaines | Moyenne |
| P7 | Guide « SIA 181 expliquée simplement » (architectes, PPE) | SIA 181 isolation phonique | C15, relecture technique | Moyenne à basse |
| P8 | Page `faux-plafonds.html` | faux plafond Genève, entreprise faux plafond Genève | Seulement si la Search Console montre des impressions faux-plafond mal servies par la page placo | Conditionnelle |
| P9 | Pages canton (`geneve.html`, puis `vaud.html`) | plâtrerie peinture + canton | 2 fiches projets publiées dans le canton, contenu local réel | Conditionnelle |
| P10 | Pages ville (Carouge, Nyon, Coppet…) | métier + ville | 1 chantier réel dans la commune, photos, 300 mots uniques ; jamais de pages clonées ([pages satellites](https://developers.google.com/search/docs/essentials/spam-policies)) | Conditionnelle |

## Annexe C. Redirections 301 : ancien site vers nouveau site

Source des URL : sitemap de l'ancien site (17 URL, toutes en `https://andyconstruct.ch/index.php/…`) et liens du menu (sans `index.php/`), relevés le 01.11.2026. URL vues indexées par notre outil (`site:andyconstruct.ch`) : `/contact`, `/produits/cadres-acoustiques`, `/presentation` (sans www), `/realisations/photos-travaux-2014-2016` (sans www), `/index.php/produits/plafonds/plafonds-en-tissu-tendu-a-froid`, `/realisations/references`.

Résultat : test sur Apache 2.4.58 local avec le `.htaccess` de production. Chaque chemin a été testé en `https://www.` (avec et sans `index.php/` pour un échantillon) ; un échantillon a été testé en `http` et sans `www`. Les règles ne dépendent pas de l'hôte : chaque variante aboutit en une seule redirection.

| Ancien chemin | Nouvelle adresse | Test |
|---|---|---|
| `/`, `/index.php`, `/index.php/` | `/` | 301 en une étape (200 pour `/`) |
| `/presentation` | `/entreprise.html` | 301 en une étape |
| `/contact` | `/contact.html` | 301 en une étape |
| `/produits/cadres-acoustiques` | `/isolation-acoustique.html#correction` | 301 en une étape |
| `/produits/cloisons/cloisons-legeres-en-placoplatre` | `/placo.html#cloisons` | 301 en une étape |
| `/produits/cloisons/cloisons-mobiles-en-aluminium` | `/placo.html#cloisons` | 301 en une étape |
| `/produits/cloisons/isolation-thermique-ou-phonique` | `/cloisons-isothermes.html` (à changer si C16 renomme la page) | 301 en une étape |
| `/produits/plafonds/plafonds-en-bac-metallique` | `/placo.html#faux-plafonds` | 301 en une étape |
| `/produits/plafonds/plafonds-en-fibre-de-bois` | `/placo.html#faux-plafonds` | 301 en une étape |
| `/produits/plafonds/plafonds-en-fibre-minerale` | `/placo.html#faux-plafonds` | 301 en une étape |
| `/produits/plafonds/plafonds-en-placoplatre` | `/placo.html#faux-plafonds` | 301 en une étape |
| `/produits/plafonds/plafonds-en-tissu-tendu-a-froid` | `/placo.html#faux-plafonds` | 301 en une étape |
| `/produits/plafonds/plafonds-phoniques-et-acoustiques` | `/isolation-acoustique.html` | 301 en une étape |
| `/realisations/photos-travaux-2014-2016` | `/realisations.html` | 301 en une étape |
| `/realisations/photos-travaux-avant-apres` | `/realisations.html#avant-apres` | 301 en une étape |
| `/realisations/references` | `/professionnels.html#references` | 301 en une étape |
| `/prestations.html` (maquette) | `/` | 301 en une étape |
| `/index.html` (nouveau) | `/` | 301 en une étape (ajout de l'audit) |
| `/index.php?option=…` (Joomla) | `/?option=…` | 301 ; la page d'accueil répond, canonical sans paramètre |
| `/images/…` (214 images), `/templates/…` | aucune | 404 attendue (T7) |

**Manques : aucun** pour les pages. Les plafonds tendus, en fibres et en bacs métalliques, et les cloisons mobiles des anciennes pages ne font plus partie de l'offre : leur redirection vers la section la plus proche (faux-plafonds, cloisons) est le meilleur choix disponible. Google peut traiter une redirection vers un contenu peu équivalent comme une erreur 404 douce ; l'enjeu reste faible, ces pages ne comptaient que 83 à 91 mots.

**Ancien site, diagnostic de départ (01.11.2026)** : Joomla, nginx devant Apache (Metanet / kreativmedia) ; les deux hôtes répondent en 200 (`http` redirige en 301 vers `https` du même hôte) ; aucun canonical ; `robots.txt` en 404 ; sitemap en `https://andyconstruct.ch/index.php/…` ; titles « Andy Construct - [rubrique] » ; la même meta description partout (« Pose de Plafonds et cloisons Genève - Vaud - Andy Construct Sàrl Suisse », raison sociale erronée) ; 2 à 4 H1 par page (« Plafonds », « Cloisons », « Cadres acoustiques » sur l'accueil ; « Menu » en plus du titre sur les autres pages) ; 83 à 204 mots par page ; 214 images sans `alt` ; HTML en `Cache-Control: no-store` ; pied de page « 2010-2022 ».

## Annexe D. Sources externes

- Google, consolider les URL en double : https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Google, bloquer l'indexation (noindex et robots.txt) : https://developers.google.com/search/docs/crawling-indexing/block-indexing
- Google, balise robots et X-Robots-Tag : https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
- Google, déplacement de site avec changement d'URL : https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes
- Google, sitemaps et `lastmod` : https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google, règles anti-spam (pages satellites) : https://developers.google.com/search/docs/essentials/spam-policies
- Google, données structurées LocalBusiness : https://developers.google.com/search/docs/appearance/structured-data/local-business
- Google, avis auto-attribués (2019) : https://developers.google.com/search/blog/2019/09/making-review-rich-results-more-helpful
- Google Business Profile, consignes de représentation : https://support.google.com/business/answer/3038177
- Google Business Profile, zones desservies : https://support.google.com/business/answer/9157481
- Google Business Profile, classement local : https://support.google.com/business/answer/7091
- Google Business Profile, fin de l'API Q&R : https://developers.google.com/my-business/content/qanda/change-log
- Google Maps, règlement des contributions (avis) : https://support.google.com/contributionpolicy/answer/7400114
- web.dev, Core Web Vitals : https://web.dev/articles/vitals
- Plesk, réglages Apache et nginx : https://docs.plesk.com/en-US/obsidian/customer-guide/72320/ et https://docs.plesk.com/en-US/12.5/customer-guide/72320/
- IndexNow (Bing) : https://www.bing.com/indexnow
- Wikidata, critères de notoriété : https://www.wikidata.org/wiki/Wikidata:Notability
- llms.txt : https://llmstxt.org/
- Validateur Schema.org : https://validator.schema.org/
- Annuaires et registre consultés le 01.11.2026 : liens du tableau L3 ; API Zefix (`https://www.zefix.ch/ZefixREST/api/v1/firm/876831.json`).
- Résultats observés le 01.11.2026 (exemples) : https://jobup.ch/en/jobs/detail/5539d3fa-bf8d-4590-ab4e-112909b18e47 ; https://business-monitor.ch/fr/cp/peintres/geneve ; https://tenderlift.ch/tenders/geneva/uni-bastions-cfc283-00-faux-plafonds-356b2aac/ ; https://ch.trustpilot.com/review/edelweiss-renovation.ch ; https://www.travaux.com/platre/guide-des-prix/cloison ; https://knauf.com/fr-FR/knauf/expertises/isolation-thermique/cloison-garage-isolante
- Documents du projet : `docs/analyse-marche.md`, `docs/brief-seo.md`, `docs/v2/concurrence-romandie.md`, `docs/v2/dossier-client.md`, `docs/v2/strategie-acquisition.md`, `docs/v2/architecture-cro.md`.

*Fichiers de travail de l'audit (exploration, Lighthouse, tests Apache) : scratchpad de la session, dossier `seo/`. Non versionnés.*
