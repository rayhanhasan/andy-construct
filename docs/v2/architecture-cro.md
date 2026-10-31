# Architecture CRO et UX : site v2 d'Andy Construct

*Phase 2 du programme v2 · architecte CRO / UX · 31 octobre 2026*
*Documents liés : `copy-deck.md` (tous les textes), `programme-v2.md`, `audit-maquette.md`, `personas-psychologie.md`, `concurrence-romandie.md`, `dossier-client.md`, `strategie-acquisition.md`, `logos-references.md`, `brief-design.md`.*

Ce document dit **quelles pages existent, dans quel ordre s'affichent leurs sections, ce que fait chaque composant et pourquoi**. Les textes à intégrer sont dans `copy-deck.md`. Les deux documents utilisent les mêmes identifiants de confirmation (`C01` à `C44`).

---

## 0. Décisions en bref

1. **13 URL au lancement** : accueil, 4 pages services, réalisations, professionnels, entreprise, contact, merci, mentions légales, confidentialité, 404. **Pas de page « Prestations » intermédiaire** : l'accueil fait office de sommaire. **Pas de pages villes ou cantons au lancement** : elles passent en phase 2, avec des conditions (§1.3).
2. **Le service « cloisons isothermes » garde son URL** (`cloisons-isothermes.html`), mais il est affiché sous le nom **« Cloisons isolantes »** dans le menu et sur les cartes. Le mot « isothermes » reste dans le H1 comme synonyme (décision à faire valider, `C16`).
3. **Un seul libellé pour l'action principale : « Demander un devis »**, sur tout le site. Le mot « offre » sert dans le texte des pages destinées aux professionnels, et pour l'« offre écrite » remise après la visite (§9.3).
4. **Formulaire en 3 étapes** (travaux → projet → coordonnées), intégré en bas de l'accueil, de chaque page service et de la page contact. Il est accessible en 1 clic depuis toutes les pages. À côté se trouvent un **module de rappel** (2 champs) et le numéro de téléphone.
5. **Accueil court** : 9 sections, **625 mots visibles** hors FAQ et pied de page, dont 192 dans le bloc de demande (comptage en annexe du copy deck ; maquette : 1'298). Le formulaire commence vers le **7e écran mobile**, contre 17,4 dans la maquette. Un appel à l'action apparaît au moins tous les 2 écrans.
6. **Preuve sociale** : bandeau de références sous le héro, rappel près du formulaire, ligne discrète dans le pied de page. **3 expositions par page au plus**, pied de page non compris. Libellé retenu : « **Ils nous ont confié des travaux** » (§5.2).
7. **Portfolio par projets** : 11 photos sur 30 restent en production (4 « montrer » et 7 « montrer avec légende neutre ») ; 19 sont retirées. On y ajoute les 7 paires avant / après de l'ancien site, si leur qualité le permet. **Héro : `faux-plafond-placo-gorge-lumineuse-01`** (alternative : `faux-plafond-placo-gorge-lumineuse-02`).
8. **Aucun faux contenu** : chaque donnée à confirmer porte un identifiant `Cxx`, un texte définitif **et** un texte de repli. En production, le générateur publie le repli tant que la confirmation manque (§14).

---

## 1. Arborescence

### 1.1 Pages du lancement

| URL | Rôle | Persona principal | Intention de recherche | Indexée | Formulaire intégré |
|---|---|---|---|---|---|
| `index.html` | Dire en 10 secondes qui, quoi, où, pour qui. Orienter vers un service ou vers la demande. | Tous | « plâtrier peintre Genève », marque | Oui | Oui (3 étapes) |
| `placo.html` | Vendre le placo : cloisons, doublages, faux-plafonds, caissons | P4, P5, P2 | « faux plafond Genève », « cloison placo » | Oui | Oui, « Placo » coché |
| `peinture.html` | Vendre la peinture intérieure : logements, fins de bail, cages d'escalier, bureaux | P4, P1 | « peintre Genève », « peinture appartement » | Oui | Oui, « Peinture » cochée |
| `isolation-acoustique.html` | Vendre l'isolation phonique et la correction acoustique ; distinguer les deux honnêtement | P4, P3, P5 | « isolation phonique appartement », « bruit voisin du dessus » | Oui | Oui, « Isolation acoustique » cochée |
| `cloisons-isothermes.html` | Vendre les cloisons et doublages isolants, l'isolation de caves, garages et combles | P4, P5 | « cloison isolante », « isolation plafond cave / garage » | Oui | Oui, « Cloisons isolantes » cochée |
| `realisations.html` | Prouver par des projets : fiches, avant / après, pendant les travaux | Tous, P2 en priorité | « réalisations faux-plafond Genève » | Oui | Non (boutons et module de rappel) |
| `professionnels.html` | Donner aux régies, architectes, communes et entreprises ce qu'il faut pour consulter Andy : méthode en site occupé, lots CFC, documents, références complètes | P1, P2, P3, P5 | « entreprise plâtrerie peinture régies », « sous-traitant faux-plafonds » | Oui | Oui |
| `entreprise.html` | Rendre l'entreprise vérifiable et humaine : histoire depuis 2007, associés, méthode, engagements, garanties | P4, P3 | marque, « Andy Construct avis » | Oui | Non (bande d'appel) |
| `contact.html` | Tous les moyens de contact, le formulaire, le rappel et la zone | Tous | « Andy Construct téléphone », « devis plâtrier » | Oui | Oui (version complète) |
| `merci.html` | Confirmer l'envoi, dire ce qui va se passer, rassurer (fin d'expérience positive) | Tous | — | **Non** (`noindex`) | Non |
| `mentions-legales.html` | Identité légale, hébergement, crédits | P3, P2 | marque, IDE | Oui | Non |
| `confidentialite.html` | Politique de confidentialité (texte rédigé par l'agent automatisation / juriste) | Tous | — | Oui | Non |
| `404.html` | Récupérer les visiteurs perdus, surtout ceux qui arrivent par les anciennes adresses | — | — | Non | Non |

Fichiers téléchargeables (dossier `documents/`, liens directs, **sans formulaire**) :
- `documents/andy-construct-dossier-de-references.pdf` (plaquette, 6 pages) ;
- `documents/liste-de-controle-immeuble-habite.pdf` (guide « régies », 2 pages) ;
- `documents/modele-avis-aux-locataires.docx` (le modèle de lettre du guide « régies ») ;
- `documents/guide-reduire-le-bruit.pdf` (guide « propriétaires », 8 pages).

### 1.2 Ajustements par rapport à la proposition du chef de projet, et pourquoi

| Point | Décision | Justification |
|---|---|---|
| Page « Prestations » intermédiaire | **Supprimée** (pas de `prestations.html`) | Elle doublerait l'accueil (cannibalisation des titles, audit n° 29) et ajouterait un clic. Les 4 cartes de l'accueil et le menu « Prestations » (bouton déroulant au clic) mènent directement aux 4 pages. |
| Nom affiché du 4e service | « **Cloisons isolantes** » dans le menu, les cartes et les boutons ; H1 « Cloisons isolantes (isothermes) » | « Isotherme » évoque surtout les chambres froides en ligne, et aucun concurrent romand ne l'emploie au sens bâtiment (`concurrence-romandie.md` §1, point 5). Le mot reste dans le H1, le texte et le JSON-LD : le client s'y retrouve, et la requête « cloison isotherme » est couverte. **À valider par le client (`C16`).** Repli : « Cloisons isothermes » partout. |
| URL du 4e service | `cloisons-isothermes.html` conservée | L'URL pèse peu dans le classement, elle correspond au nom validé par le client, et la garder évite une redirection si le client préfère son terme. Le title et le H1 portent « cloisons isolantes », « cave », « garage ». |
| Fiches projets | **Ancres dans `realisations.html`** au lancement (`#projet-hall-gorge-lumineuse`…) ; une URL par projet en phase 2 | Aucune fiche n'a aujourd'hui de lieu, d'année ni d'accord de citation confirmés (`dossier-client.md` §5.5). Une page par projet avec 40 mots serait du contenu mince. Condition de passage à une URL propre : §1.3. |
| Zone d'intervention | **Section `#zone` de `contact.html`** (carte, liste par canton, phrase « Votre commune n'est pas dans la liste ? ») ; une ligne sur l'accueil | Une page « zone » seule, sans chantier réel par canton, serait mince et redondante. La carte a sa place à côté des coordonnées. |
| Entreprises (PME) | Bloc court sur `professionnels.html` | Un gérant de PME qui cherche « pour les professionnels » doit s'y retrouver ; il n'a pas besoin d'une page à lui. |
| Guides | PDF en libre téléchargement, avec option « par la poste » | `strategie-acquisition.md` §4 propose un envoi par e-mail, mais `personas-psychologie.md` §3.3 et NN/g déconseillent de bloquer un contenu derrière une adresse e-mail. **Point à arbitrer** (§15) : nous recommandons le lien direct, plus un formulaire facultatif pour recevoir la version imprimée par la poste. |

### 1.3 Phase 2 : pages à créer seulement si leurs conditions sont remplies

Aucune page clonée (« faux-plafond Onex », « faux-plafond Lancy » au même texte) : ce sont des pages satellites, que Google pénalise et que les réseaux de mise en relation pratiquent déjà.

| Page | Condition de création | Contenu minimal | Exemple |
|---|---|---|---|
| Fiche projet `realisations/<projet>.html` | Lieu (commune), type de bâtiment, année, prestation et accord de citation confirmés ; 3 photos ou plus | 250 mots uniques : contexte, demande, solution, contrainte, résultat (sans chiffre inventé) ; photos avant / pendant / après ; prestation liée ; crédit de l'architecte avec son accord | `realisations/salle-communale-plan-les-ouates.html` |
| Page canton `geneve.html`, `vaud.html` | Au moins 2 fiches projets publiées dans le canton | Délais d'intervention, communes desservies, contexte réglementaire local (p. ex. IDC à Genève), fiches liées | `vaud.html` adossée à Coppet, Nyon, Chavannes-de-Bogis |
| Page ville | Au moins 1 chantier réel dans la commune, avec photos, et 300 mots uniques | Fiche projet locale, accès, délais | Carouge, Collonge-Bellerive, Nyon |
| `prix.html` (« Prix indicatifs ») | Le client fournit des fourchettes réelles pour 4 cas types (`C31`) | 4 cas types, ce qui est compris et non compris, HT ou TTC, « indicatif, offre après visite » | Peinture d'un 3,5 pièces ; cloison de 10 m² ; faux-plafond de 20 m² ; doublage phonique d'un mur mitoyen |
| Guides HTML (un par mois) | Rédaction mensuelle (`strategie-acquisition.md` §3.2) | 600 à 1'200 mots, FAQ, lien vers la page service | « Bruit des voisins : absorber ou isoler ? » |

### 1.4 Redirections 301 (anciennes adresses Joomla)

Toutes les variantes, avec ou sans `index.php/` et avec ou sans `www`, doivent rediriger **en une seule étape** vers `https://www.andyconstruct.ch/…` (règles `.htaccess` sur le modèle de `brief-seo.md` §8.3).

| Ancien chemin | Nouvelle adresse |
|---|---|
| `/`, `/index.php` | `/` |
| `/presentation` | `/entreprise.html` |
| `/produits/plafonds/plafonds-en-placoplatre` | `/placo.html#faux-plafonds` |
| `/produits/plafonds/plafonds-en-tissu-tendu-a-froid` | `/placo.html#faux-plafonds` |
| `/produits/plafonds/plafonds-en-fibre-de-bois`, `/plafonds-en-fibre-minerale`, `/plafonds-en-bac-metallique` | `/placo.html#faux-plafonds` |
| `/produits/plafonds/plafonds-phoniques-et-acoustiques` | `/isolation-acoustique.html` |
| `/produits/cadres-acoustiques` | `/isolation-acoustique.html#correction` |
| `/produits/cloisons/cloisons-legeres-en-placoplatre` | `/placo.html#cloisons` |
| `/produits/cloisons/cloisons-mobiles-en-aluminium` | `/placo.html#cloisons` |
| `/produits/cloisons/isolation-thermique-ou-phonique` | `/cloisons-isothermes.html` |
| `/realisations/photos-travaux-2014-2016` | `/realisations.html` |
| `/realisations/photos-travaux-avant-apres` | `/realisations.html#avant-apres` |
| `/realisations/references` | `/professionnels.html#references` |
| `/contact` | `/contact.html` |
| `/prestations.html` (maquette, si elle a été déployée) | `/` |

`sitemap.xml` : les 11 pages indexables ; `merci.html` et `404.html` exclues ; `lastmod` produit au build. `robots.txt` : `Disallow: /api/` et `Disallow: /interne/`.

---

## 2. Navigation

### 2.1 En-tête sur ordinateur (≥ 1240 px)

Ordre de gauche à droite : **logo** (lien vers l'accueil) · **menu** (5 entrées) · **téléphone** (horaires au-dessus du numéro, en petit) · **bouton « Demander un devis »**.

| Entrée du menu | Comportement |
|---|---|
| Prestations | Bouton qui s'ouvre **au clic** (jamais au survol), construit avec `<details>`/`<summary>` pour fonctionner sans JavaScript. Panneau de 4 liens, chacun avec une ligne d'explication. Fermeture par Échap, par un clic à l'extérieur ou un second clic. Indicateur visible « ▾ ». |
| Réalisations | Lien |
| Professionnels | Lien |
| L'entreprise | Lien (vers `entreprise.html`, et non plus vers une ancre de l'accueil) |
| Contact | Lien, en dernière position (position sérielle) |

- L'en-tête reste visible au défilement et **ne rétrécit pas**. Hauteur ≤ 80 px.
- Entre 900 et 1239 px, on garde le logo, le téléphone et le bouton « Demander un devis » ; le menu passe derrière le bouton « Menu ».
- Page active : `aria-current="page"`, soulignée.

### 2.2 En-tête sur mobile et tablette (< 900 px)

- Logo à gauche (hauteur 40 px), bouton **« Menu »** à droite (icône et mot, cible ≥ 48 px).
- Menu ouvert : plein écran, liste à plat : **Placo · Peinture · Isolation acoustique · Cloisons isolantes** (sous le titre « Prestations »), puis Réalisations · Professionnels · L'entreprise · Contact. En bas : bouton « Appeler le +41 22 771 20 15 » et bouton « Demander un devis ». Le bouton devient « Fermer ».
- En-tête plus barre fixe : 64 px + 64 px au plus, soit moins de 16 % d'un écran de 844 px (règle : ≤ 20 %).

### 2.3 Barre fixe en bas (mobile, < 900 px)

- Deux boutons de **même largeur**, hauteur 56 px : **« Appeler »** (icône téléphone, contour) et **« Demander un devis »** (rouge).
- Présente dès le chargement. Elle **masque** son propre espace en bas de page (marge basse du `body`) pour ne pas recouvrir le pied de page.
- « Demander un devis » mène à `#demande` si la page contient le formulaire, sinon à `contact.html#demande`.
- Test T6 prévu : « Appeler » contre « Appeler le 022 771 20 15 ».

### 2.4 Pied de page (toutes les pages)

Fond anthracite, 4 colonnes sur ordinateur, empilées sur mobile :
1. **Marque** : logo blanc, phrase d'identité.
2. **Nous joindre** : bloc NAP dans `<address>` (même texte partout, caractère pour caractère), lien « Voir sur la carte ».
3. **Prestations** : les 4 pages services.
4. **Andy Construct** : Réalisations · Professionnels · L'entreprise · Contact · Dossier de références (PDF).

Puis, sur toute la largeur : la **ligne de références** (texte, blanc à 70 %, sans logo dans le pied de page, pour rester discrète). Enfin la barre basse : © année générée au build, raison sociale, IDE, lien « Vérifier au registre du commerce », Mentions légales, Protection des données (et « Paramètres des cookies » seulement si un bandeau de consentement existe, scénarios M et L).

Liens du pied : hauteur ≥ 48 px (audit n° 36).

### 2.5 Fil d'Ariane

Sur toutes les pages sauf l'accueil, la page merci et la 404 : « Accueil › Nom de la page ». Les pages services n'ont que 2 niveaux, puisqu'il n'y a pas de page « Prestations ». Le JSON-LD `BreadcrumbList` reprend exactement ce fil.

### 2.6 Règle « la demande en 1 clic depuis partout »

| Depuis | « Demander un devis » (en-tête, barre mobile, boutons du contenu) mène à | Numéro | Rappel |
|---|---|---|---|
| Accueil | `#demande` (même page) | En-tête, héro, bloc final, barre mobile | Bloc final |
| Pages services | `#demande` (même page, travaux déjà cochés : on arrive à l'étape 2) | Idem | Bloc final |
| Professionnels | `#demande` | Idem | Bloc final |
| Réalisations, Entreprise, Mentions, Confidentialité, 404 | `contact.html#demande` | Idem | Réalisations : bloc final ; autres : lien « Être rappelé(e) » vers `contact.html#rappel` |
| Contact | `#demande` | Idem | À côté du formulaire |
| Merci | Pas de bouton de demande ; seulement le numéro | Oui | — |

Les boutons « Un projet semblable ? » des fiches de réalisations mènent à `contact.html?travaux=<service>#demande` : le formulaire s'ouvre à l'étape 2, avec le service coché.

---

## 3. Composants partagés

| Composant | Contenu | Règles |
|---|---|---|
| **En-tête de page** (`page-head`) | Fil d'Ariane, H1, chapeau de 2 lignes au plus à 390 px, 2 boutons (pages services, professionnels), 3 puces « En bref » (pages services) | Pages services : photo à droite sur ordinateur, sous le chapeau sur mobile (format 3:2, ≥ 343 px de large). |
| **Bandeau de références** (`refs-band`) | Titre, 8 références, phrase « particuliers », lien | §5.3. Statique, sans lien vers les sites des références. |
| **Carte service** (accueil) | Icône, nom, phrase dans les mots du client, « Pour : … », lien « Voir le placo » (« Voir la peinture »…) | Carte entièrement cliquable (un seul lien qui couvre la carte), cible ≥ 48 px, texte 18 px. |
| **Carte projet** | Photo 3:2, titre (type de travaux), type de lieu, contrainte (1 ligne), étiquettes des prestations, badge « Pendant les travaux » si besoin | Légende toujours visible, y compris sur mobile (audit n° 18). |
| **Méthode en 4 étapes** | Visite · Offre écrite · Chantier protégé · Réception, et l'engagement « Aucun travail supplémentaire sans votre accord écrit et chiffré » | **Texte unique**, réutilisé partout (accueil, pages services en version courte, entreprise, professionnels). Numéros en gros, une ligne par étape. |
| **FAQ** | `<details>`/`<summary>` avec indicateur « + / − » visible, réponse dans le DOM | 4 à 8 questions par page, **jamais la même question sur deux pages**. FAQPage en JSON-LD avec le texte visible mot pour mot. |
| **Bloc de demande** (`#demande`) | H2, intro, formulaire en 3 étapes, réassurance, module de rappel, coordonnées, ligne de références | §6 et §7. Sur ordinateur : formulaire à gauche (≈ 60 %), colonne de droite avec le rappel, le téléphone et la ligne de références. Sur mobile : formulaire, puis rappel, puis téléphone. |
| **Bande d'appel** (`cta-band`) | Titre, 1 phrase, « Demander un devis » et « Appeler le … » | Pages sans formulaire intégré (Entreprise). Fond anthracite. |
| **Témoignages** | 1 à 3 citations réelles | **Masqué tant que la liste est vide** (§5.5). |
| **Avant / après** | 2 photos côte à côte avec les étiquettes « Avant » et « Après », légende | §8.5. Pas de curseur à faire glisser. |
| **Visionneuse** | `<dialog>` existant : « Fermer », « Précédente », « Suivante », compteur « Photo 2 sur 6 », Échap | Conservée telle quelle, avec la correction d'accessibilité de l'audit n° 28. |
| **Bandeau « version de validation »** | Preview uniquement | Supprimé en production (programme §6). |

---

## 4. Pages, section par section

Légende des colonnes : **Composant** = élément du §3 ; **Preuve** = élément de preuve sociale ou de crédibilité ; **Mobile** = comportement à 390 px. Les numéros d'écran sont des estimations à 390 × 844 px, en-tête compris.

### 4.1 Accueil (`index.html`)

Objectif : 450 à 650 mots visibles hors FAQ et pied de page (**625 mots** avec le texte définitif du copy deck, formulaire à l'étape 1 compris). 9 sections, contre 11 dans la maquette.

| # | Section | Contenu | Composant | Appel à l'action | Preuve | Mobile (écran) |
|---|---|---|---|---|---|---|
| 1 | Héro | Surtitre, H1, sous-titre, 2 boutons, horaires sous les boutons, 3 faits vérifiables | Héro avec photo `faux-plafond-placo-gorge-lumineuse-01` et voile anthracite à gauche | « Demander un devis » (→ `#demande`), « Appeler le +41 22 771 20 15 » | Depuis 2007, registre du commerce, Carouge | Écran 1. Boutons pleine largeur, les deux visibles sans défiler. Les 3 faits en liste sous les boutons. |
| 2 | Bandeau de références | « Ils nous ont confié des travaux », 8 noms (logos `autorise` seulement en production), phrase sur les particuliers, lien « Voir toutes nos références » | `refs-band` | Lien vers `professionnels.html#references` | **Exposition 1** | Écran 1-2. Grille de 2 colonnes, noms sur 2 lignes au plus. |
| 3 | Prestations | Surtitre, H2, 4 cartes, phrase « Vous hésitez ? Décrivez votre besoin : nous vous orientons. », bouton | Cartes services | « Demander un devis » sous les cartes | — | Écrans 2-3. Cartes empilées. Bouton à ≈ 2'400 px (écran 2,8). |
| 4 | Réalisations | H2, 3 cartes projets, lien « Voir toutes les réalisations », bouton contextuel | Cartes projets | « Un projet semblable ? Demander un devis » | Noms des maîtres d'ouvrage sur les cartes **seulement s'ils sont autorisés** (`C22`) : **exposition 2 éventuelle** | Écrans 3-5. Photos pleine largeur. Bouton à ≈ 4'000 px (écran 4,7). |
| 5 | Comment nous travaillons | H2, 4 étapes, engagement « aucun supplément » (`C06`) | Méthode | Lien « Notre méthode en détail » (→ `entreprise.html#methode`) | Réduction du risque | Écrans 5-6. Étapes en liste numérotée. |
| — | Témoignages | **Masqué** tant qu'il n'y a pas de témoignage réel | Témoignages | — | (exposition future, en remplacement de la ligne de références de la section 8) | — |
| 6 | Professionnels et zone | Bande à 2 colonnes : « Régies, architectes, communes » (2 lignes et lien) · « Toute la Suisse romande » (1 ligne et lien vers la carte) | Bande brume | « Espace professionnels », « Voir la carte » | — | Écran 6. Les 2 blocs s'empilent. |
| 7 | Questions fréquentes | 8 questions | FAQ | « Une autre question ? Appelez le … » | — | Écrans 6-7. Fermées par défaut. |
| 8 | Demander un devis | H2, intro, formulaire (étape 1 visible), réassurance, module de rappel, coordonnées | Bloc de demande | « Continuer », « Être rappelé(e) », numéro | **Exposition 3** : ligne de références dans la colonne de droite (sous le rappel sur mobile) | Le formulaire commence à ≈ 5'900 px (**écran 7**). |
| 9 | Pied de page | §2.4 | — | — | Ligne discrète (non comptée) | — |

**Cadence des appels à l'action sur mobile** : écran 1 (héro), écran 2,8 (sous les prestations), écran 4,7 (sous les réalisations), écran 6 (bande professionnels et lien de la FAQ), écran 7 (formulaire). La barre fixe reste visible en permanence. L'écart ne dépasse jamais 2 écrans.

**Variante à tester (T4)** : sous les boutons du héro, deux liens « Vous êtes un particulier » / « Vous êtes un professionnel ». Pas dans la version de lancement : on mesure d'abord la version simple.

### 4.2 Gabarit des 4 pages services

Toutes les pages services suivent le même gabarit. Chaque bloc principal compte **120 à 250 mots**.

| # | Section | Contenu | Composant | Appel à l'action | Preuve | Mobile |
|---|---|---|---|---|---|---|
| 1 | En-tête de page | Fil d'Ariane, H1 (service + bénéfice), chapeau, 2 boutons, 3 puces « En bref », photo | `page-head` avec photo | « Demander un devis » (→ `#demande`, service coché), « Appeler » | Photo réelle légendée | Écran 1 : H1, chapeau, boutons. La photo suit. |
| 2 | Ce que nous faisons | H2 formulé comme une requête, 3 ou 4 sous-blocs H3 (un par type d'ouvrage), avec une ancre chacun | Texte et sous-titres | — | Vocabulaire précis | Paragraphes de 4 lignes au plus. |
| 3 | Pour qui | 2 colonnes : « Particuliers » / « Professionnels » | Deux encadrés | Lien « Espace professionnels » dans l'encadré pro | — | Empilés. |
| 4 | Ce qu'il faut savoir | 4 ou 5 points d'attention **honnêtes**, chacun avec sa solution | Liste à puces avec icône « i » | — | Franchise (« ce qui ne marche pas ») | Liste. |
| 5 | Réalisations | 1 fiche projet illustrée (ou une paire avant / après), 1 ou 2 photos de plus, « Réalisé notamment pour : … » (`C23`) | Carte projet en grand | « Voir toutes les réalisations en <service> » (→ `realisations.html?filtre=<service>`) | **Exposition 1** | Photo pleine largeur. |
| 6 | Bloc spécifique | Placo : aucun · Peinture : aucun · Acoustique : **guide à télécharger** · Cloisons isolantes : **subventions** (encadré) | Encadré | « Télécharger le guide (PDF) » | Réciprocité | — |
| 7 | Comment se passe un chantier | Méthode, version courte (4 lignes) | Méthode | Lien « Notre méthode en détail » | — | — |
| 8 | Questions fréquentes | 5 ou 6 questions propres au service, dont « Combien coûte… » | FAQ | — | — | — |
| 9 | Demander un devis | Bloc de demande, **étape 1 déjà faite** (service coché, résumé « Travaux : Placo · Modifier »), on arrive à l'étape 2 | Bloc de demande | « Continuer », rappel, numéro | **Exposition 2** : ligne de références | — |
| 10 | Pied de page | — | — | — | Ligne discrète | — |

Spécificités par page :
- **Placo** : ancres `#cloisons`, `#doublages`, `#faux-plafonds`, `#caissons` (cibles des redirections 301).
- **Peinture** : aucune photo de peinture aujourd'hui. La section 5 affiche la paire avant / après n° 6 (séjour) si sa qualité est suffisante (`C26`), sinon elle est **masquée** et remplacée par un lien vers les réalisations. Elle se remplit dès que le shooting peinture est fait (`C17`, `C40`).
- **Isolation acoustique** : section 2 en deux temps, « Isoler ou corriger » (H2) puis « Ce que nous posons contre le bruit » (H2), avec l'ancre `#correction` pour la correction acoustique. Section 6 : guide « Réduire le bruit chez soi ».
- **Cloisons isolantes** : une phrase de filtrage dans le chapeau, « Nous ne posons pas de chambres froides » (`C16`). Section 6 : encadré « Subventions », prudent (`C43`).

### 4.3 Réalisations (`realisations.html`)

| # | Section | Contenu | Composant | Appel à l'action | Preuve | Mobile |
|---|---|---|---|---|---|---|
| 1 | En-tête de page | H1, chapeau, mention « Toutes les photos sont nos propres réalisations » (`C25`) | `page-head` | — | Authenticité | — |
| 2 | Filtres | Tous · Placo · Peinture · Isolation acoustique · Cloisons isolantes. **Un filtre sans projet est masqué** (Peinture au lancement). Compteur « {{n}} projets affichés ». | Boutons `aria-pressed` | — | — | Boutons en 2 lignes, cibles ≥ 48 px. |
| 3 | Projets | Fiches projets (§8.2), 3 colonnes sur ordinateur, 1 sur mobile. Clic sur la photo : visionneuse avec les photos du projet. | Cartes projets | Sous chaque fiche : « Un projet semblable ? Demander un devis » | **Exposition 1** : nom du maître d'ouvrage si autorisé (`C22`) | Photos ≥ 343 px de large. |
| 4 | Avant / après (`#avant-apres`) | Jusqu'à 7 paires (§8.5) | Avant / après | — | Preuve concrète | Avant au-dessus, après en dessous. |
| 5 | Témoignages | Masqué tant qu'il est vide | Témoignages | — | — | — |
| 6 | Références | Une ligne de références et le lien « Voir les 18 références, par secteur » (→ `professionnels.html#references`) | Ligne | — | **Exposition 2** | — |
| 7 | Votre projet | Titre, phrase, « Demander un devis » (→ `contact.html#demande`), « Appeler », module de rappel | Bloc d'appel avec rappel | 3 actions | — | — |

### 4.4 Professionnels (`professionnels.html`)

| # | Section | Contenu | Composant | Appel à l'action | Preuve | Mobile |
|---|---|---|---|---|---|---|
| 1 | En-tête de page | H1, chapeau, boutons | `page-head` | « Télécharger le dossier de références (PDF, x Ko) » (principal, **sans formulaire**), « Envoyer un dossier de soumission » (→ `#soumission`), téléphone | — | — |
| 2 | Selon votre métier | 4 blocs : Régies et gérances · Architectes et bureaux d'études · Communes et institutions · Entreprises et commerces. Pour chacun : ce que nous apportons, une preuve, une action. | 4 cartes (2 × 2 sur ordinateur) | Une action par carte | **Exposition 1** : noms cités dans le texte des cartes (collectivités) | Empilées. |
| 3 | Méthode en site occupé | 8 engagements concrets pour les immeubles habités et les bâtiments publics | Liste numérotée sur 2 colonnes | Lien « Télécharger la liste de contrôle (PDF) » | Réduction du risque | 1 colonne. |
| 4 | Lots, normes et documents | Lots CFC (`C14`), normes (`C15`), tableau des documents : dossier PDF, liste de contrôle, modèle d'avis aux locataires, registre du commerce, attestations sur demande (`C12`, `C13`) | Tableau (2 colonnes : document / comment l'obtenir) | Liens de téléchargement | Autorité vérifiable | Tableau transformé en liste. |
| 5 | Ils nous ont confié des travaux (`#references`) | **Grille complète des 18 références** par secteur, logos selon leur statut, année et nature des travaux dès qu'elles sont connues (`C22`) | Grille | — | **Exposition 2** | 2 colonnes. |
| 6 | Envoyer un dossier de soumission (`#soumission`) | Adresse e-mail, ce qu'il faut joindre, taille maximale, liens de transfert acceptés, accusé de réception (`C01`, `C40`) | Encadré | « Écrire à … » (`mailto:` avec objet prérempli « Dossier de soumission ») | — | — |
| 7 | Demander un devis | Bloc de demande (sans ligne de références : la grille vient juste avant) | Bloc de demande | Formulaire, rappel, numéro | — | — |

### 4.5 L'entreprise (`entreprise.html`)

| # | Section | Contenu | Composant | Appel à l'action | Preuve | Mobile |
|---|---|---|---|---|---|---|
| 1 | En-tête de page | H1, chapeau | `page-head` (photo de l'équipe à droite **quand elle existe**, `C10`) | — | Visage (futur) | — |
| 2 | Notre histoire | Frise : 2007, 2010, 2023, aujourd'hui | Frise verticale | — | Faits du registre (FOSC) ; **exposition 1** : une phrase de références | — |
| 3 | Notre métier | But social inscrit au registre (citation) et explication des 4 métiers | Citation | — | Autorité vérifiable | — |
| 4 | Ce qui guide notre travail | 4 engagements | 4 cartes | — | Réduction du risque | — |
| 5 | Notre méthode (`#methode`) | Méthode en 4 étapes, version complète | Méthode | — | — | — |
| 6 | L'équipe | Photo, associés, rôles, effectif | Bloc photo et texte | — | Sympathie | **Masqué** tant que photos et accords manquent (`C10`, `C24`) |
| 7 | Vérifiez qui nous sommes | Raison sociale, forme, IDE avec lien, siège, inscription, affiliation (`C11`), assurance (`C12`), paiement (`C28`) | Liste de définitions | « Vérifier au registre du commerce » | Vérifiabilité | — |
| 8 | Si un défaut apparaît après les travaux | Garanties de la loi suisse, dites factuellement (texte à faire relire par un juriste) | Encadré | — | Réduction du risque | — |
| 9 | Bande d'appel | Titre, phrase, 2 boutons | `cta-band` | « Demander un devis » (→ `contact.html#demande`), « Appeler » | — | — |

### 4.6 Contact (`contact.html`)

| # | Section | Contenu | Composant | Appel à l'action | Preuve | Mobile |
|---|---|---|---|---|---|---|
| 1 | En-tête de page | H1, chapeau | `page-head` | — | — | — |
| 2 | Deux colonnes | **Gauche** : Nous appeler (bureau, chantiers, horaires, phrase sur le répondeur), Nous écrire (e-mail), Nous trouver (NAP, « sur rendez-vous » `C29`, carte), Pour préparer votre demande (5 points), ligne de références. **Droite** : formulaire (`#demande`), puis module de rappel (`#rappel`). | Colonnes | Formulaire, rappel, téléphone, e-mail | **Exposition 1** : ligne de références dans la colonne gauche | **Ordre mobile** : téléphones, puis formulaire, puis rappel, puis e-mail et adresse, puis « Pour préparer ». Le formulaire commence au 2e écran. |
| 3 | Zone (`#zone`) | H2, phrase, carte SVG, liste par canton, « Votre commune n'est pas dans la liste ? », zone particuliers / professionnels (`C21`) | Carte | « Appeler » | — | Sous la carte, la liste des villes en texte (audit n° 37). |

Le téléphone n'apparaît qu'**une fois** dans la colonne gauche (audit n° 38), en plus de l'en-tête et de la barre.

### 4.7 Merci (`merci.html`)

`noindex`, hors sitemap. Atteinte **uniquement** après une réponse `ok` du serveur. Deux variantes : demande de devis et rappel.

| # | Section | Contenu |
|---|---|---|
| 1 | Confirmation | H1, référence de la demande (`AC-AAAA-NNNN`, renvoyée par l'API), récapitulatif lu dans `sessionStorage` (travaux, commune, préférence de contact) puis effacé. **Aucune donnée personnelle dans l'URL.** Sans récapitulatif disponible : version générique. |
| 2 | Et maintenant ? | 3 étapes : rappel (qui, quand, depuis quel numéro, `C01`, `C09`), visite (`C41`), offre écrite (`C08`). Photo de l'associé quand elle existe (`C09`). |
| 3 | Pour gagner du temps | 4 choses à préparer pour la visite. |
| 4 | E-mail de confirmation | Phrase « un e-mail vous a été envoyé », affichée seulement si une adresse a été donnée. |
| 5 | Un seul lien | « Voir nos réalisations en <service demandé> » (→ `realisations.html?filtre=<service>`). |
| 6 | Urgence | Numéro cliquable et horaires. |

Pas de formulaire, pas de bouton de demande, pas de fenêtre surgissante. Événement `formulaire_envoye` déjà envoyé par la page précédente (pas de doublon ici).

### 4.8 Mentions légales, confidentialité, 404

- **Mentions légales** : en-tête de page, contenu en prose (`copy-deck.md` §L), pied de page. Lien vers `confidentialite.html`.
- **Confidentialité** : gabarit identique ; texte fourni par l'agent automatisation / juriste. Le copy deck donne le title, la meta et l'introduction.
- **404** : H1, phrase, 6 liens (4 services, réalisations, contact), numéro, bouton « Retour à l'accueil ». Chiffre « 404 » décoratif en `aria-hidden="true"` et en graphite (audit n° 34). Balise `<base href="/">` en production.

---

## 5. Preuve sociale

### 5.1 Plan d'exposition par page (3 au plus, pied de page non compté)

| Page | Exposition 1 | Exposition 2 | Exposition 3 | Pied de page |
|---|---|---|---|---|
| Accueil | Bandeau sous le héro | Noms sur les cartes projets (si autorisés) | Ligne près du formulaire | Oui |
| Pages services | « Réalisé notamment pour » (section Réalisations) | Ligne près du formulaire | — | Oui |
| Réalisations | Noms sur les fiches (si autorisés) | Ligne et lien avant l'appel final | — | Oui |
| Professionnels | Noms dans les cartes « Selon votre métier » | Grille complète (`#references`) | — | Oui |
| Entreprise | Phrase dans « Notre histoire » | — | — | Oui |
| Contact | Ligne dans la colonne gauche | — | — | Oui |
| Merci, 404, légales | — | — | — | Oui |

Règles (d'après `personas-psychologie.md` §3.2 bis) :
- **jamais deux blocs de références dans le même écran** ;
- **même liste, dans le même ordre, partout** ;
- noms les plus forts au début et à la fin ;
- statique : pas de défilement automatique, pas de lien vers les sites des références, pas de couleur au survol ;
- uniquement des faits vrais : « nous ont confié des travaux », **jamais** « nous recommandent » ni « nos partenaires ».

### 5.2 Libellé retenu

**« Ils nous ont confié des travaux »**, plutôt que « Ils nous ont fait confiance » (formule générique, employée partout) ou « Ils nous ont confié leurs chantiers » (qui surestime : UBS ou l'OMC n'ont pas confié « leurs chantiers », mais des travaux précis). Cette formule est exacte, sobre, vérifiable et proche de la recommandation des personas (« nous a confié des travaux »).

### 5.3 Bandeau de références (accueil)

- **Ordre (8 références)** : Ville de Genève · Conservatoire de musique de Genève · HEAD – Genève · OMC (`C22`, accord de l'OMC pour le nom ; repli : Salle de l'Alhambra) · UBS · Piaget · Mairie de Plan-les-Ouates · Salle communale de Collonge-Bellerive. On ouvre sur une autorité publique et on finit sur une commune proche, à laquelle un particulier peut s'identifier.
- **Rendu** : `protege` et `introuvable` toujours en nom typographique (Montserrat 600, graphite) ; `a_autoriser` en logo en **preview**, en nom en **production** ; `autorise` en logo partout. Logos monochromes, `--logo-h` 44 px (34 px sur mobile), échelle `--e` de `logos.json`. `alt` = `nom_affiche`. Traits d'union insécables dans les noms composés.
- **Contrepoids « trop gros pour moi »** : sous la grille, la phrase sur les particuliers et les petits chantiers (`C04`).
- **En production** : petite ligne « Références citées avec l'accord des maîtres d'ouvrage » (`logos-references.md` §6), seulement quand les accords sont archivés.

### 5.4 Ligne de références (près des formulaires et dans le pied de page)

Texte seul, liste courte (6 noms) et mention des particuliers. Elle reprend le même ordre que le bandeau. Texte exact dans le copy deck (§A.6).

### 5.5 Témoignages et avis (blocs masqués tant qu'ils sont vides)

- **Source** : un fichier de données (`temoignages.json`) vide au lancement. Le générateur **n'écrit aucune section** si la liste est vide : pas de titre orphelin, pas de « bientôt ».
- **Format d'un témoignage** : texte exact validé par écrit (2 ou 3 phrases), nom ou fonction et organisation selon le choix de l'auteur, commune, nature des travaux, année. Champ interne `accord_date` obligatoire, sinon le générateur refuse de publier.
- **Emplacement** : accueil (entre la méthode et la bande professionnels ; il remplace alors la ligne de références de la section 8, pour rester à 3 expositions) et réalisations (section 5).
- **Avis Google** : quand la fiche compte **au moins 5 avis**, une ligne de texte statique, « Avis Google : 4,8 sur 5, 12 avis (relevé le …) · Lire les avis », mise à jour à la main ou par le rapport mensuel. Pas de widget tiers, pas de note agrégée dans le JSON-LD du site.

---

## 6. Formulaire de demande en 3 étapes

### 6.1 Principes

- **Engagement progressif** : la première question est facile et impersonnelle (les travaux). Les coordonnées arrivent en dernier.
- **Longueur annoncée** dès le départ : « 3 étapes, environ une minute » (« Encore 2 étapes, moins d'une minute » quand l'étape 1 est préremplie). « Étape 2 sur 3 » écrit en toutes lettres, avec une barre de progression (texte + barre, jamais la couleur seule).
- **Boutons qui disent la suite** : « Continuer : votre projet », « Continuer : vos coordonnées », « Envoyer ma demande ». Bouton « Retour » à chaque étape, **qui conserve les données**.
- **L'appel reste possible à chaque étape** : sous chaque bouton, « Vous préférez qu'on vous rappelle ? » (mène au module de rappel) ; le numéro cliquable reste visible à côté du formulaire (colonne « Par téléphone »), dans l'en-tête et dans la barre mobile.
- **Sans JavaScript** : les 3 étapes s'affichent l'une sous l'autre, avec un seul bouton d'envoi à la fin. Le formulaire fonctionne entièrement.
- **Pré-remplissage** : depuis une page service ou un lien `?travaux=…`, l'étape 1 est déjà faite et résumée (« Travaux : Placo · Modifier »). Le formulaire s'ouvre à l'étape 2 et affiche « Étape 2 sur 3 » (progression offerte).
- **Une colonne**, étiquettes au-dessus des champs, champs de 52 px de haut, texte 18 px, cibles ≥ 48 px, 8 px d'écart au moins.
- Chaque étape est un `<fieldset>` avec sa `<legend>`. Au changement d'étape, le focus va sur le titre de l'étape, et une zone `aria-live="polite"` annonce « Étape 2 sur 3 : votre projet ».
- **Obligatoire et facultatif** sont tous deux écrits en toutes lettres.

### 6.2 Champs

Noms techniques alignés sur l'API en cours d'écriture (`site/api/lib/Champs.php` et `Validateur.php`). `docs/v2/contrat-interface.md` n'existe pas encore au 31.10.2026 : en cas d'écart, **le contrat d'interface fait foi pour les noms et les valeurs**, et ce document pour les libellés.

**En-tête du formulaire** : titre et introduction du bloc de demande (`copy-deck.md` §A.5 : « Demander un devis » et « 3 étapes, environ une minute… »). À partir de l'étape 2, au-dessus des champs : « Les champs obligatoires sont indiqués. » La réassurance (3 lignes) est visible sous le formulaire **à chaque étape**.

#### Étape 1 sur 3 · « Quels travaux ? »

| Libellé | Nom | Type | Valeurs envoyées → libellés affichés | Statut | Aide | Validation et message d'erreur | Scoring |
|---|---|---|---|---|---|---|---|
| Légende : « Quels travaux souhaitez-vous ? » | `travaux[]` | 5 grandes cases à cocher en forme de cartes (icône, nom, une ligne) ; plusieurs choix possibles | `placo` → « Placo » + « Cloisons, doublages, faux-plafonds » · `peinture` → « Peinture » + « Murs et plafonds, à l'intérieur » · `isolation-acoustique` → « Isolation acoustique » + « Contre le bruit ou l'écho » · `cloisons-isothermes` → « Cloisons isolantes » + « Caves, garages, combles » · `ne-sait-pas` → « Autre chose, ou je ne sais pas encore » + « Décrivez-le à l'étape 3 » | Obligatoire (au moins une case) | « Vous pouvez en cocher plusieurs. » | À « Continuer » sans case cochée : « Choisissez au moins un type de travaux, ou « Autre chose, ou je ne sais pas encore ». » | Service (0-15) ; « plusieurs » si 2 prestations ou plus |

Bouton : **« Continuer : votre projet »**.

#### Étape 2 sur 3 · « Votre projet »

| Libellé | Nom | Type | Valeurs → libellés | Statut | Aide | Validation et message d'erreur | Scoring |
|---|---|---|---|---|---|---|---|
| « Vous êtes » | `type_client` | 6 boutons radio, en liste | `proprietaire` → « Propriétaire (maison, appartement, PPE) » · `locataire` → « Locataire » · `regie` → « Régie, gérance ou coopérative » · `architecte` → « Architecte, bureau d'études ou entreprise générale » · `commune` → « Commune ou institution » · `entreprise` → « Entreprise, bureau ou commerce » | Obligatoire | — | « Indiquez qui vous êtes : cela nous permet de vous orienter vers la bonne personne. » | Type de client (0-30) |
| « Commune des travaux » | `commune` (et `npa` rempli par le script si l'entrée commence par 4 chiffres) | Texte, `autocomplete="address-level2"` | Saisie libre | Obligatoire | « Commune ou NPA, par exemple Lancy ou 1212. » | Vide : « Indiquez la commune des travaux ou son NPA. » · NPA de moins ou plus de 4 chiffres : « Le NPA compte 4 chiffres, par exemple 1227. » | Zone (0-15) |
| « Quand souhaitez-vous faire les travaux ? » | `delai` | 4 boutons radio | `moins-1-mois` → « Dès que possible (moins d'un mois) » · `1-3-mois` → « Dans 1 à 3 mois » · `3-6-mois` → « Dans 3 à 6 mois » · `non-defini` → « Pas encore défini » | Facultatif | — | — | Délai (0-10) |
| « Quelle surface, à peu près ? » | `surface` | 5 boutons radio | `moins-15` → « Moins de 15 m² (une réparation) » · `15-50` → « 15 à 50 m² (une ou deux pièces) » · `50-200` → « 50 à 200 m² (un appartement, un étage) » · `plus-200` → « Plus de 200 m², ou plusieurs logements » · `ne-sait-pas` → « Je ne sais pas » | Facultatif | « Une estimation suffit. » | — | Ampleur (0-20) |

Aucun bouton radio n'est présélectionné. Bouton : **« Continuer : vos coordonnées »**. Lien « Retour ».

#### Étape 3 sur 3 · « Vos coordonnées »

| Libellé | Nom | Type | Valeurs → libellés | Statut | Aide | Validation et message d'erreur | Scoring |
|---|---|---|---|---|---|---|---|
| « Civilité » | `civilite` | 2 boutons radio en ligne | `madame` → « Madame » · `monsieur` → « Monsieur » | Facultatif | — | — | — (sert aux e-mails : « Bonjour Madame Dupont ») |
| « Nom et prénom » | `nom` | Texte, `autocomplete="name"` | — | Obligatoire | — | « Indiquez votre nom et votre prénom. » | — |
| « Téléphone » | `telephone` | `type="tel"`, `inputmode="tel"`, `autocomplete="tel"` | Tous formats acceptés (022…, 079…, +41…, 0041…, espaces, points, tirets) | **Au moins un des deux** (téléphone ou e-mail) | « Pour vous rappeler et convenir de la visite. Exemple : 079 123 45 67. » | Aucun des deux : « Indiquez un numéro de téléphone ou une adresse e-mail pour que nous puissions vous répondre. » · Numéro incomplet : « Ce numéro semble incomplet. Indiquez-le par exemple ainsi : 079 123 45 67. » | Bonus +3 |
| « E-mail » | `email` | `type="email"`, `autocomplete="email"` | — | idem | « Pour vous envoyer la confirmation et l'offre. » | « Cette adresse e-mail semble incomplète. Vérifiez-la, par exemple : nom@exemple.ch. » · Suggestion non bloquante pour une faute courante : « Vouliez-vous dire …@bluewin.ch ? » (bouton « Oui, corriger ») | — |
| « Comment préférez-vous être recontacté(e) ? » | `preference_contact` | 3 boutons radio | `appel` → « Par téléphone » · `email` → « Par e-mail » · `indifferent` → « Peu importe » | Facultatif | — | Si « Par téléphone » est choisi sans numéro : « Indiquez le numéro auquel nous pouvons vous rappeler. » | — |
| « Plutôt… » (affiché si `appel`) | `creneau` | 3 boutons radio | `matin` → « Le matin » · `apres-midi` → « L'après-midi » · `indifferent` → « Peu importe » | Facultatif | « Nous appelons du lundi au vendredi, de 7 h à 18 h. » (`C03`) | — | — |
| « Votre projet en quelques mots » | `message` | Zone de texte, 5 lignes | — | Facultatif | « Par exemple : logement habité ou vide, délai impératif, accès, étage. Professionnels : date de remise des offres. » | Plus de 3'000 caractères : « Votre message est trop long (3'000 caractères au maximum). Vous pouvez nous envoyer la suite par e-mail. » | Malus −5 si vide et sans téléphone |
| « Photos ou plans » | `fichier[]` | Fichier, `multiple`, `accept="image/jpeg,image/png,application/pdf"` ; bouton stylé « Choisir des fichiers » + état « Aucun fichier choisi » / « 2 fichiers choisis (3,4 Mo) » | — | Facultatif | « JPG, PNG ou PDF, 3 fichiers et 10 Mo au total. Trop lourd ? Envoyez-les par e-mail après notre appel. » | Format refusé : « Ce fichier n'est pas une photo JPG ou PNG, ni un PDF. Choisissez un autre fichier, ou envoyez-le par e-mail. » · Trop lourd : « Ces fichiers dépassent 10 Mo au total. Retirez-en un, ou envoyez-les par e-mail après notre appel. » · Plus de 3 : « 3 fichiers au plus. Vous pourrez nous envoyer les autres par e-mail. » | Bonus +5 |
| « Comment nous avez-vous connus ? » | `connu_par` | Liste déroulante | `recherche-google` → « Recherche sur Google » · `carte-google` → « Carte Google » · `recommandation` → « Recommandation d'un proche ou d'un voisin » · `regie-architecte` → « Une régie ou un architecte » · `panneau-vehicule` → « Un panneau de chantier ou un véhicule » · `facebook` → « Facebook » · `linkedin` → « LinkedIn » · `autre` → « Autre » | Facultatif | — | — | Source (0-10) si pas d'UTM |
| « Qui vous a recommandé Andy Construct ? » (si `recommandation`) | `recommande_par` | Texte | — | Facultatif | « Pour pouvoir remercier cette personne. » | — | Source |
| Accord (voir §6.3) | `accord` | Case à cocher **non cochée** | `oui` | Obligatoire tant que l'API l'exige | — | « Cochez cette case pour que nous puissions traiter votre demande. » | — |

Bouton : **« Envoyer ma demande »**. Sous le bouton, la réassurance (3 lignes, `copy-deck.md` §A.5) et la mention d'information.

Champs cachés : `formulaire=devis`, `site_web` (piège à robots, à laisser vide), `form_t0` (horodatage signé), `page`, `page_entree`, `referent`, `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`, `gclid` (seulement avec consentement), `consent_ads` (si un bandeau existe), `canal=site`.

### 6.3 Consentement : case ou mention d'information

L'API actuelle exige `accord`. L'audit (n° 17) rappelle que la nLPD n'impose pas de case pour répondre à une demande : le devoir d'informer (art. 19) suffit, et la case ajoute une friction.
- **Au lancement** : case **non cochée**, libellé « J'accepte que mes coordonnées servent uniquement à traiter ma demande (protection des données). », avec un lien vers `confidentialite.html`.
- **Recommandation, après avis du juriste** : retirer la case, garder sous le bouton la mention « En envoyant ce formulaire, vous nous transmettez vos coordonnées pour traiter votre demande. Elles ne servent à rien d'autre (protection des données). », et rendre `accord` facultatif dans l'API. **Point à arbitrer** (§15).

### 6.4 Comportements

| Situation | Comportement |
|---|---|
| Validation | À la sortie du champ (pas pendant la frappe), et au clic sur « Continuer » ou « Envoyer ». Message sous le champ : texte, icône et couleur, `aria-describedby`, `aria-invalid`. Aucun « invalide » ni « erreur de saisie ». |
| Plusieurs erreurs à l'envoi | Récapitulatif en haut de l'étape (« 2 points à compléter »), avec des liens vers les champs ; focus sur le récapitulatif, puis sur le premier champ en erreur. |
| Erreur renvoyée par le serveur | Les erreurs `{champ: message}` de l'API s'affichent sous les champs concernés ; le formulaire revient à l'étape du premier champ en erreur. |
| Données conservées | Navigation entre les étapes sans perte. Brouillon dans `sessionStorage` (sans les fichiers) : si la page est rechargée, la saisie est retrouvée. Effacé après l'envoi réussi. |
| Envoi | Bouton désactivé et libellé « Envoi en cours… » ; `fetch` en `multipart/form-data` vers `/api/demande.php`. **Succès seulement si la réponse est `ok`** : enregistrement de `ref` et du récapitulatif dans `sessionStorage`, puis redirection vers `merci.html`. |
| Échec réseau ou serveur | La saisie reste en place. Message : « Votre demande n'a pas pu partir. Rien n'est perdu : réessayez dans un instant, ou appelez-nous au +41 22 771 20 15. » Bouton « Réessayer ». |
| Fichiers | Taille vérifiée avant l'envoi (10 Mo au total, 3 fichiers). Aperçu du nom et du poids de chaque fichier, bouton « Retirer » pour chacun. |
| Anti-spam | Invisible : `site_web` et délai minimal (`form_t0`). **Pas de CAPTCHA.** |
| Un e-mail mal tapé | Suggestion non bloquante (« Vouliez-vous dire … ? ») pour les domaines courants : bluewin.ch, gmail.com, hotmail.com, sunrise.ch, outlook.com. |

### 6.5 Mesure (Umami, sans cookie)

`formulaire_debut` (première interaction, une fois par session), `formulaire_etape` (`etape`, `service`, `type_client`), `formulaire_erreur` (`champ`, jamais la valeur), `formulaire_envoye` (`formulaire=devis|rappel`, `service`, `type_client`), **sur la réponse `ok` seulement**. Aucune donnée personnelle dans les propriétés.

---

## 7. Module de rappel

| Élément | Spécification |
|---|---|
| Titre | « Vous préférez qu'on vous rappelle ? » (H3) |
| Phrase | « Laissez simplement votre numéro. » |
| Champ 1 | « Votre numéro de téléphone » · `telephone` · obligatoire · `type="tel"` · aide « Exemple : 079 123 45 67 » · erreurs : « Indiquez le numéro auquel nous pouvons vous rappeler. » / « Ce numéro semble incomplet. Indiquez-le par exemple ainsi : 079 123 45 67. » |
| Champ 2 | « Votre nom » · `nom` · facultatif |
| Choix facultatif | « Plutôt… » · `creneau` : « Le matin » / « L'après-midi » / « Peu importe » (aucun présélectionné) |
| Bouton | « Être rappelé(e) » |
| Sous le bouton | À côté d'un formulaire : « Votre numéro ne sert qu'à ce rappel. » (le délai figure déjà dans la réassurance). Module seul (réalisations) : « Nous vous rappelons le jour même ou le jour ouvrable suivant (`C01`). Votre numéro ne sert qu'à ce rappel. » |
| Envoi | `formulaire=rappel`, mêmes champs cachés et même anti-spam que le formulaire de devis ; succès → `merci.html` (variante « rappel ») |
| Emplacements | Bloc de demande (accueil, pages services, professionnels), contact (`#rappel`), réalisations (bloc final). Dans le formulaire en étapes, le lien « Vous préférez qu'on vous rappelle ? » fait défiler jusqu'au module et y place le focus ; si un numéro est déjà saisi à l'étape 3, il est recopié. |

---

## 8. Portfolio

### 8.1 Principe

On passe d'une grille plate de 30 photos (dont 14 hors offre) à des **projets** : moins de photos, toutes dans l'offre, chacune avec sa légende vraie. « 12 à 15 photos bien choisies valent mieux que 30 photos mêlées » (audit §6).

### 8.2 Format d'une fiche projet

| Élément | Règle |
|---|---|
| Photo forte | Format 3:2, pleine largeur sur mobile (≥ 343 px), 380 px ou plus sur ordinateur. Variante 400w ajoutée pour les vignettes (audit n° 27). |
| Titre | Type de travaux, en mots simples : « Hall et couloirs : faux-plafond à gorge lumineuse ». |
| Type de lieu | Générique et vrai : « Immeuble de bureaux, Genève ». Jamais de lieu inventé. Sans information du client : le type de bâtiment visible seulement (« Hall d'immeuble »). |
| Contrainte résolue | 1 ou 2 lignes, **fournie par le client** (`C25`). Repli : ce que montre la photo, sans interprétation. |
| Prestations | Étiquettes parmi les 4 services seulement : Placo · Peinture · Isolation acoustique · Cloisons isolantes. |
| Badge | « Pendant les travaux » pour les photos de chantier en cours (ce n'est plus un filtre). |
| Maître d'ouvrage, année | Seulement avec accord écrit (`C22`) et une année confirmée. Les années connues aujourd'hui viennent des EXIF (2012-2016) : on ne les affiche pas tant que le client ne les a pas confirmées, et on donne la priorité aux chantiers récents (`C39`). |
| Photos supplémentaires | 2 à 6 dans la visionneuse, avec la même légende de projet. |
| Appel à l'action | « Un projet semblable ? Demander un devis » → `contact.html?travaux=<service>#demande`. |

### 8.3 Filtres

« Tous · Placo · Peinture · Isolation acoustique · Cloisons isolantes ». Un filtre est **masqué automatiquement** s'il n'a aucun projet (« Peinture » au lancement). Le filtre est repris dans l'URL (`?filtre=placo`) pour les liens depuis les pages services et la page merci. « Chantiers en cours » disparaît comme filtre et devient un badge.

### 8.4 Classement des 30 photos du manifeste

Légende : **M** = montrer · **N** = montrer avec une légende neutre (condition indiquée) · **R** = retirer en production (reste visible en preview, avec un bandeau « hors offre », pour que le client tranche).

| # | Photo (`id`) | Ce qu'on voit | Décision | Légende proposée / raison | Projet |
|---|---|---|---|---|---|
| 1 | `plafond-tendu-ilots-lumineux-01` | Salle aux îlots suspendus, plafond tendu | **R** | Plafond tendu, hors des 4 services. Ancien héro. Si le client confirme que les **îlots** sont en plaques de plâtre : N, avec « Îlots suspendus en plaques de plâtre » | — |
| 2 | `plafond-tendu-ilots-lumineux-02` | Même salle, rangées de chaises | **R** | Idem | — |
| 3 | `plafond-lumineux-circulaire-01` | Plafond lumineux rétroéclairé | **R** | Plafond lumineux, hors offre | — |
| 4 | `paroi-lumineuse-imprimee-01` | Volume lumineux imprimé | **R** | Hors offre | — |
| 5 | `plafond-tendu-ilot-eclairage-indirect-01` | Îlot et plafond tendu | **R** | Hors offre | — |
| 6 | `faux-plafond-placo-gorge-lumineuse-01` | Faux-plafond en plâtre, gorge lumineuse, spots | **M** | « Faux-plafond en plaques de plâtre à gorge lumineuse » · **héro** | P1 |
| 7 | `plafond-couronnes-lumineuses-01` | Couronnes lumineuses de restaurant | **R** | Hors offre | — |
| 8 | `panneaux-acoustiques-muraux-01` | Panneaux absorbants muraux, plafond perforé | **N** | « Correction acoustique : panneaux muraux et plafond perforé ». Condition : la correction acoustique fait toujours partie de l'offre (`C18`), sinon R | P6 |
| 9 | `faux-plafond-placo-gorge-lumineuse-02` | Espace arrondi, gorge lumineuse | **M** | « Faux-plafond arrondi en plaques de plâtre, éclairage intégré » | P1 |
| 10 | `chantier-ossature-puits-de-lumiere-01` | Ossature et laine isolante, poseur | **N** | « Pendant les travaux : ossature métallique et isolant, avant la fermeture du plafond ». Ne pas dire ce qui a été posé ensuite (plafond tendu probable). Condition : accord du poseur visible (`C25`) | P2 |
| 11 | `plafond-tendu-puits-de-lumiere-01` | Puits de lumière dans plafond tendu | **R** | Hors offre | — |
| 12 | `plafond-tendu-ilots-lumineux-03` | Îlot autour d'un pilier | **R** | Hors offre | — |
| 13 | `plafond-couronnes-lumineuses-02` | Couronne lumineuse | **R** | Hors offre | — |
| 14 | `plafond-tendu-poutres-apparentes-01` | Plafond lisse entre poutres | **R** | Technique inconnue (tendu probable). Si le client confirme du plâtre : M, « Plafond en plaques de plâtre entre poutres apparentes » | — |
| 15 | `cadre-acoustique-salle-de-reunion-01` | Cadre acoustique imprimé, salle de réunion | **N** | « Salle de réunion : panneau acoustique mural contre l'écho ». Condition : `C18` | P7 |
| 16 | `cadre-acoustique-imprime-01` | Grand cadre imprimé (scarabée) | **R** | Décoratif avant tout, n'illustre aucun des 4 services | — |
| 17 | `plafond-dalles-couloir-01` | Couloir en dalles minérales | **R** | Dalles minérales (hors offre) ; doublon du projet P1 | — |
| 18 | `plafond-placo-ilot-ovale-01` | Îlot ovale suspendu en plâtre, hall | **N** | « Hall : îlot ovale suspendu en plaques de plâtre ». Condition : **recadrer** pour masquer le slogan du client visible au mur, ou obtenir son accord (`C25`) | P5 |
| 19 | `plafond-lames-metalliques-01` | Lames métalliques | **R** | Hors offre | — |
| 20 | `chantier-ossature-puits-de-lumiere-02` | Ossature, isolant, puits de lumière | **N** | « Pendant les travaux : ossature et isolant autour d'un puits de lumière » | P2 |
| 21 | `chantier-pose-plafond-lumineux-01` | Pose d'un plafond lumineux, poseur | **R** | Hors offre, personne visible | — |
| 22 | `chantier-salle-de-spectacle-01` | Salle de spectacle pendant les travaux | **N** | « Salle de spectacle : intervention dans une salle protégée ». Condition : le client confirme une prestation parmi les 4 (`C25`), sinon R | P8 |
| 23 | `plafond-tendu-mat-01` | Plafond tendu mat | **R** | Hors offre, image faible | — |
| 24 | `habillage-placo-niches-arrondies-01` | Habillage plâtre à niches arrondies, escalier protégé | **M** | « Pendant les travaux : habillage en plaques de plâtre à niches arrondies, escalier protégé » | P4 |
| 25 | `plafond-lames-metalliques-02` | Plafond à lames | **R** | Hors offre | — |
| 26 | `plafond-bacs-metalliques-cuisine-01` | Bacs métalliques de cuisine | **R** | Hors offre | — |
| 27 | `cloisons-modulaires-vitrees-01` | Cloisons vitrées démontables | **R** | Hors offre (cloisons mobiles) | — |
| 28 | `cloisons-modulaires-vitrees-02` | Idem | **R** | Hors offre | — |
| 29 | `chantier-suspentes-ossature-01` | Suspentes et ossature sous dalle isolée | **M** | « Pendant les travaux : suspentes et ossature d'un faux-plafond, sous une dalle isolée » | P3 |
| 30 | `chantier-salle-de-spectacle-02` | Intervention au balcon, fauteuils sous bâche | **N** | « Salle de spectacle : fauteuils protégés pendant les travaux ». Condition : `C25` (prestation), sinon R. Utile aussi pour illustrer la protection des lieux (professionnels) | P8 |

**Bilan** : 4 **M**, 7 **N**, 19 **R**. En production, on a donc **11 photos au plus** (moins si les conditions N ne sont pas remplies), plus les paires avant / après. Si le client souhaite garder certaines photos **R** comme « Autres réalisations (hors offre actuelle) », ce sera avec leur légende exacte (« plafond tendu »…) et sous un titre distinct. **Nous ne le recommandons pas** : elles brouillent le positionnement et un architecte les reconnaît.

### 8.5 Avant / après (7 paires de l'ancien site)

Source : `https://www.andyconstruct.ch/images/avant_apres/01.jpg` à `14.jpg`, environ 800 px, sans personne visible (`dossier-client.md` §5.1). **[À VÉRIFIER : qualité]** sur chaque paire (netteté, cadrage, compression) ; en demander les originaux (`C26`).

| Paire | Fichiers | Sujet (légende proposée) | Service | Priorité |
|---|---|---|---|---|
| AA1 | 01 / 02 | Caisson en plaques de plâtre sous une verrière | Placo | 3 |
| AA2 | 03 / 04 | Gaine de ventilation cachée dans un couloir | Placo | 3 |
| AA3 | 05 / 06 | Combles : isolation et rampant fini sous une fenêtre de toit | Cloisons isolantes | **1** (la plus parlante) |
| AA4 | 07 / 08 | Monobloc de ventilation habillé d'un caisson | Placo | 4 |
| AA5 | 09 / 10 | Couloir : puits de lumière circulaires dans un faux-plafond | Placo | **1** (très visuelle) |
| AA6 | 11 / 12 | Séjour : faux-plafond en périphérie et spots | Placo · Peinture | **1** (un logement : rassure les particuliers) |
| AA7 | 13 / 14 | Paroi cintrée : de l'ossature au couloir fini | Placo | 2 (cadrages différents) |

Composant : deux images côte à côte (ordinateur) ou l'une sous l'autre (mobile), étiquettes « Avant » et « Après » **en texte** au-dessus de chaque image, légende commune dessous. **Pas de curseur à glisser** (geste difficile pour un public senior, et piège pour le clavier). Taille maximale affichée : 800 px. Si une paire est jugée trop faible : elle n'est pas publiée.

### 8.6 Projets proposés

| Projet | Titre | Photos | Prestations | Où il apparaît |
|---|---|---|---|---|
| P1 | Hall et couloirs : faux-plafond à gorge lumineuse | #6, #9 | Placo (peinture `C25`) | Accueil (carte 1), placo, réalisations |
| P2 | Grande salle : ossature et isolant avant la fermeture | #10, #20 | Placo, plus Isolation acoustique ou Cloisons isolantes selon l'isolant posé (`C25`) | Accueil (carte 2), cloisons isolantes (si isolant thermique), réalisations |
| P3 | Faux-plafond suspendu sous une dalle isolée | #29 | Placo | Placo, réalisations |
| P4 | Cage d'escalier : habillage à niches arrondies | #24 | Placo | Réalisations |
| P5 | Hall : îlot ovale suspendu | #18 (recadrée) | Placo | Réalisations |
| P6 | Correction acoustique d'une salle | #8 | Isolation acoustique | Isolation acoustique, réalisations |
| P7 | Salle de réunion : moins d'écho | #15 | Isolation acoustique | Isolation acoustique, réalisations |
| P8 | Salle de spectacle : intervention en salle protégée | #22, #30 | `C25` | Réalisations, professionnels (méthode) |
| AA6 | Séjour : faux-plafond et spots, avant / après | avant_apres 11/12 | Placo · Peinture | Accueil (carte 3), peinture, réalisations |

Accueil, carte 3 : AA6 si sa qualité est suffisante ; sinon P4.

### 8.7 Photo du héro

- **Retenue : `faux-plafond-placo-gorge-lumineuse-01`** (P1000782, 2013). Faux-plafond en plaques de plâtre, à bords arrondis, gorge lumineuse et spots encastrés, peint en blanc. Il correspond **sans ambiguïté** au placo (et à la peinture de finition). Lumière chaude, pièce propre, aucune personne, aucune marque.
- **Cadrage** : sur ordinateur, `object-position: 70% 40%` pour garder l'ellipse lumineuse à droite, le voile anthracite (70-85 % à gauche) couvrant le mur clair de gauche. Sur mobile : `object-position: 60% 45%`, voile renforcé (80 %) sur toute la hauteur du texte.
- **Fichiers** : exporter une version 2400 px depuis l'original (photo de 2013, appareil de 12 Mpx : la résolution le permet), plus 1600 et 800 en WebP et JPG. Précharger la variante adaptée. Cible : LCP ≤ 2,5 s en 4G.
- **Image Open Graph** : refaire `og-andy-construct.jpg` (1200 × 630) à partir de cette photo (l'actuelle montre un plafond tendu).
- **Alternative : `faux-plafond-placo-gorge-lumineuse-02`** (même chantier, espace arrondi et colonne). Plus symétrique, mais le centre est chargé (bois, colonne) : à utiliser si le contraste du titre est insuffisant avec la première.
- **À remplacer** dès que le shooting fournit une photo récente de placo ou de peinture, en paysage, avec de l'espace calme à gauche (`selection-photos.md`, recommandations).

### 8.8 Shooting à commander (priorité haute)

3 ou 4 chantiers en cours, en lumière du jour, avec l'accord des personnes visibles : **peinture** (logement habité, protections visibles), **cloison isolante** (cave ou garage, ossature et isolant, puis fini), **doublage ou faux-plafond acoustique** (suspentes antivibratiles visibles), et **une paire avant / après au même cadrage** dans un logement. Pour chaque chantier : une vue d'ensemble, un détail de finition, un détail technique, et trois informations (lieu, besoin, solution).

---

## 9. Règles d'ergonomie senior appliquées

### 9.1 Lecture

- Texte courant en 18 px, **aucun texte sous 16 px** (surtitres et étiquettes passent de 14 à 16 px, `--fs-xs: 1rem`, espacement réduit à 0,12em ; texte des cartes à 18 px, `--fs-card: 1.125rem`).
- Interligne 1,6 ; lignes de 68 caractères au plus ; contrastes AA au minimum (graphite #44494F sur blanc ≈ 8:1).
- Surtitres en capitales : **4 mots au plus**.
- Une idée par bloc ; paragraphes de 4 lignes au plus à 390 px ; réponses de FAQ de 35 mots au plus sur l'accueil et de 60 mots au plus sur les pages services.
- Des titres qui donnent la réponse (« Nous intervenons dans toute la Suisse romande »), pas des étiquettes (« Zone »).
- Sigles expliqués à leur première apparition sur les pages destinées aux particuliers (PPE, CFC, SIA). Jargon technique réservé aux encadrés « Pour les professionnels » et à la page Professionnels.
- Liens soulignés dans le texte.

### 9.2 Choix et gestes

- Menu de 5 entrées ; 4 cartes services, pas plus ; **par écran, 1 bouton principal et le téléphone**.
- Cibles ≥ 48 px (boutons 52 à 56 px), espacées d'au moins 8 px ; boutons pleine largeur sur mobile ; cartes entièrement cliquables.
- Aucun menu au survol, aucun carrousel, aucune vidéo en lecture automatique, aucun compteur animé, aucune fenêtre surgissante, aucun chat flottant.
- Zoom jusqu'à 200 % sans casse ; jamais de `maximum-scale`.

### 9.3 Vocabulaire des actions

- **Action principale : « Demander un devis »**, partout (en-tête, barre mobile, héro, bas des sections, boutons des pages services). C'est le mot des particuliers (« devis » plus qu'« offre »), celui des recherches (« devis peinture », « devis faux plafond »), et les professionnels le comprennent. Un seul libellé évite de croire à deux démarches différentes (audit n° 16).
- **« Offre écrite »** désigne le document remis après la visite (méthode, FAQ). Sur les pages pour particuliers, la première occurrence précise « offre écrite (votre devis) ».
- **Actions propres aux professionnels**, dans leur langue : « Télécharger le dossier de références », « Envoyer un dossier de soumission », « Demander nos attestations ».
- Boutons : verbe + objet. Jamais « Soumettre », « OK », « Cliquez ici », ni un « En savoir plus » isolé.
- Test T1 prévu plus tard : « Demander une offre » contre « Demander un devis ».

### 9.4 Téléphone

- Numéro écrit en clair, avec les espaces, cliquable, sur chaque page : en-tête (ordinateur), barre fixe (mobile), héro, bloc de demande, pied de page.
- Horaires à côté du numéro (`C03`).
- Le mobile est présenté comme second numéro : « Sur les chantiers : +41 78 631 14 34 » (`C30`).
- Format d'affichage : `+41 22 771 20 15` (charte et NAP) ; liens `tel:+41227712015`.

### 9.5 Confiance

- Identité vérifiable sur chaque page (pied de page : raison sociale, IDE, lien vers le registre du commerce).
- Aucune date de naissance, aucun IBAN, aucun paiement en ligne.
- Une demande ne se perd jamais (brouillon conservé, erreur réseau rattrapée).
- Page de confirmation **et** e-mail récapitulatif (programme automatisation).

---

## 10. Maillage interne

| Depuis ↓ / vers → | Accueil | Placo | Peinture | Acoustique | Isolantes | Réalisations | Professionnels | Entreprise | Contact |
|---|---|---|---|---|---|---|---|---|---|
| **Accueil** | — | Carte | Carte | Carte | Carte | 3 cartes + lien | Bandeau (`#references`), bande pro | Méthode (`#methode`) | Zone (`#zone`) |
| **Placo** | Fil | — | « nous peignons » (chapeau) | « contre le bruit » (Doublages) et FAQ 3 | « contre le froid » (Doublages) | `?filtre=placo` | Encadré « Pour qui » | Méthode | — |
| **Peinture** | Fil | « Après nos travaux de placo » | — | — | — | `?filtre=peinture` (si non vide) | Encadré « Pour qui » | Méthode | — |
| **Acoustique** | Fil | — | — | — | « Une pièce froide plutôt que bruyante ? » (Ce qu'il faut savoir) | `?filtre=isolation-acoustique` | Encadré « Pour qui » | Méthode | — |
| **Isolantes** | Fil | — | — | « Le bruit vous gêne aussi ? » (Ce qu'il faut savoir) | — | `?filtre=cloisons-isothermes` | Encadré « Pour qui » | Méthode | — |
| **Réalisations** | Fil | Étiquettes de prestation de chaque fiche | Étiquettes | Étiquettes | Étiquettes | — | « Voir les 18 références » | — | Boutons des fiches |
| **Professionnels** | Fil | Lots CFC (liens vers les services) | idem | idem | idem | « Voir nos réalisations » | — | « Vérifiez qui nous sommes » | — |
| **Entreprise** | Fil | Les 4 métiers (liens) | idem | idem | idem | — | Lien | — | Bande d'appel |
| **Contact** | Fil | — | — | — | — | — | — | — | — |
| **Merci** | — | — | — | — | — | Un seul lien (`?filtre=<service>`) | — | — | — |
| **Pied de page** | Logo | Oui | Oui | Oui | Oui | Oui | Oui (+ PDF) | Oui | Oui |

Règles : textes de lien descriptifs et variés (« voir nos cloisons et faux-plafonds », pas toujours « placo ») ; aucun lien « cliquez ici » ; les pages services se lient entre elles seulement quand le sujet le justifie (bruit, isolant, peinture après placo).

---

## 11. Données structurées par page (JSON-LD)

Une seule entité « entreprise » (`@id: https://www.andyconstruct.ch/#entreprise`), décrite en entier sur l'accueil et référencée ailleurs par son `@id`.

| Page | Types | Points d'attention |
|---|---|---|
| Accueil | `HomeAndConstructionBusiness` (complet), `WebSite`, `WebPage`, `FAQPage` | `image` : uniquement des photos de l'offre (#6, #9, #29). **Retirer** `sameAs` search.ch (ancienne adresse) et le profil Facebook personnel. Garder local.ch, ajouter la page LinkedIn de l'entreprise et la fiche GGE (`C11`). `foundingDate: 2007`, `foundingLocation: Perly-Certoux`. `knowsAbout` : les 4 services, avec « cloisons isolantes » et « cloisons isothermes ». Pas d'`aggregateRating` ni de `review`. `hasOfferCatalog` : 4 `Offer` dont l'`itemOffered` pointe vers chaque page service. |
| Pages services | `Service` (`name`, `serviceType`, `description`, `provider` → `#entreprise`, `areaServed` : 7 zones romandes, `url`), `WebPage`, `BreadcrumbList`, `FAQPage` | Aucun prix (`offers`) tant que `C31` manque. `alternateName` sur la page cloisons : « Cloisons isothermes ». |
| Réalisations | `CollectionPage`, `ImageGallery` (`associatedMedia` : `ImageObject` avec `caption` = légende, `contentLocation` **seulement** si la commune est confirmée), `BreadcrumbList` | Pas de `creator` autre qu'Andy Construct. |
| Professionnels | `WebPage` (`audience` : `BusinessAudience`), `BreadcrumbList`, `DigitalDocument` pour le dossier PDF (`encodingFormat: application/pdf`) | — |
| Entreprise | `AboutPage` (`about` → `#entreprise`), `BreadcrumbList` | `founder` ou `member` (personnes) **seulement** avec l'accord des associés (`C10`) ; `memberOf` GGE **seulement** si `C11` est confirmé. |
| Contact | `ContactPage`, `BreadcrumbList` | `contactPoint` déjà dans l'entité. |
| Mentions, confidentialité | `WebPage`, `BreadcrumbList` | — |
| Merci, 404 | Aucun | `noindex`. |

Le texte des `FAQPage` est **identique mot pour mot** au texte visible. Aucune question n'apparaît sur deux pages.

---

## 12. Tableau « élément → levier psychologique → indicateur »

| Élément | Levier(s) | Mise en œuvre | Indicateur |
|---|---|---|---|
| En-tête (téléphone, horaires, bouton) | Fitts, réduction du risque | Numéro en clair et horaires ; bouton « Demander un devis » toujours visible | `appel_clic` (`emplacement=entete`) ; `devis_clic` (`emplacement=entete`) |
| Barre fixe mobile | Fitts, engagement | 2 boutons de même poids, 56 px | `appel_clic` (`barre_mobile`) / visites mobiles ; test T6 |
| Héro | Autorité vérifiable, unité locale, Hick | H1 métier + lieu ; 3 faits vérifiables ; 2 boutons | Clics des boutons du héro ; défilement à 25 % |
| Bandeau de références | Preuve sociale, autorité, simple exposition, position sérielle | 8 noms, même ordre partout, phrase « particuliers » | Clics « Voir toutes nos références » ; clics sur les boutons situés après |
| Phrase « particuliers et petits chantiers » | Similarité (contre « trop gros pour moi ») | Sous le bandeau, dans la FAQ (`C04`) | Part des demandes « propriétaire » (CRM) |
| 4 cartes services | Hick, reconnaissance | Phrase dans les mots du client (« Vous entendez vos voisins ? ») | Clics par carte ; demandes par service |
| Pages services | Autorité, preuve ciblée, honnêteté (perte présentée avec sa solution) | « Ce qu'il faut savoir » franc ; réalisations du service ; FAQ prix | Taux de conversion par page ; part des formulaires préremplis |
| Fiches projets | Preuve concrète, similarité | Type de lieu, contrainte, prestations ; bouton « Un projet semblable ? » | Ouvertures de la visionneuse ; clics « Un projet semblable ? » |
| Avant / après | Preuve, contraste | Paires au même cadrage | Visites de `#avant-apres` |
| Méthode en 4 étapes | Réduction du risque, Hick, pic-fin (la dernière étape est une fin positive) | Même texte partout ; engagement « aucun supplément » | Défilement jusqu'à la méthode ; clics qui suivent |
| Formulaire en 3 étapes | Engagement progressif, progression offerte, gradient de but | Question facile d'abord ; « Étape 2 sur 3 » ; préremplissage | `formulaire_debut` → `formulaire_etape` (2, 3) → `formulaire_envoye` ; abandon par étape ; test T2 |
| Raison donnée sous chaque champ | Effet « parce que » | « Pour vous rappeler et convenir de la visite » | `formulaire_erreur` par champ ; taux de champs facultatifs remplis |
| Réassurance sous le bouton | Réduction du risque | Délai de rappel, sans engagement, pas de publicité | Envois / formulaires commencés ; test T5 |
| Module de rappel | Plus petit engagement possible | 2 champs | `formulaire_envoye` (`rappel`) ; part des rappels joignables ; test T3 |
| Ligne de références près du formulaire | Preuve au moment du doute | Une ligne, 6 noms | Envois / visiteurs qui atteignent le formulaire ; test T7 |
| Page merci | Pic-fin, sympathie | Référence, qui rappelle et quand, quoi préparer, un seul lien | Visites des réalisations depuis merci ; taux de joignabilité au rappel (CRM) |
| Dossier de références PDF libre | Réciprocité, autorité | Téléchargement direct, sans formulaire | `plaquette_telechargee` ; demandes B2B dans les 30 jours |
| Guides (bruit, immeuble habité) | Réciprocité, conseil honnête | Libre téléchargement ; version imprimée sur demande | Téléchargements ; demandes « aimant » (`par_poste`) ; demandes liées |
| Page Entreprise | Autorité vérifiable, sympathie (visages) | Registre, frise, associés (`C10`), garanties de la loi | Clics « Vérifier au registre du commerce » ; visites avant une demande |
| Témoignages et avis (masqués si vides) | Preuve sociale indépendante | Avis Google en texte dès 5 avis ; témoignages validés par écrit | Nombre d'avis ; clics vers la fiche Google |
| Pied de page | Autorité, répétition discrète | NAP, IDE, registre, ligne de références | Clics sur le lien du registre et sur le téléphone du pied |

---

## 13. Événements de mesure (rappel)

Repris de `strategie-acquisition.md` §6.1, avec deux ajouts.

| Événement | Où | Propriétés |
|---|---|---|
| `appel_clic` | Tout lien `tel:` | `emplacement` (entete, heros, barre_mobile, bloc_demande, contact, pied, fiche_projet, merci, 404), `numero` (fixe, mobile), `page` |
| `email_clic` | Tout lien `mailto:` | `emplacement`, `page` |
| **`devis_clic`** (ajout) | Tout bouton « Demander un devis » et « Un projet semblable ? » | `emplacement`, `page`, `service` si connu |
| `formulaire_debut`, `formulaire_etape`, `formulaire_erreur`, `formulaire_envoye` | Formulaire et rappel | §6.5 |
| `plaquette_telechargee` | Lien du PDF | `page` |
| **`guide_telecharge`** (ajout) | Liens des guides | `guide`, `page` |
| `aimant_demande` | Formulaire « par la poste » | `aimant`, `par_poste` |
| `galerie_filtre` | Filtres des réalisations | `filtre` |
| `itineraire_clic` | « Voir sur la carte » | `page` |

---

## 14. Marqueurs « à confirmer » : mise en œuvre

1. Chaque donnée non confirmée porte dans le copy deck un identifiant `Cxx`, un **texte définitif** (avec la valeur proposée) et un **texte de repli** (vrai sans confirmation, parfois vide : le bloc est alors masqué).
2. Le générateur lit un fichier `tools/build/confirmations.json` : `{"C01": false, "C02": false, …}`.
3. **Preview** : texte définitif affiché, souligné en pointillé, avec une infobulle « À confirmer (C01) » pour la séance de validation avec le client.
4. **Production** (`--production`) : texte définitif si `true`, repli sinon. Le build **échoue** si une chaîne « [À CONFIRMER » ou « [À VÉRIFIER » reste dans le HTML produit.
5. Les blocs « masqués tant qu'ils sont vides » (témoignages, équipe, avis Google, galerie peinture) dépendent de leurs fichiers de données, pas de `confirmations.json`.
6. `docs/contenus-a-valider.md` est remplacé par la section « Questions au client » du copy deck, organisée selon les mêmes identifiants.

---

## 15. Points à arbitrer

| # | Sujet | Options | Recommandation | Qui tranche |
|---|---|---|---|---|
| 1 | Nom affiché du 4e service | « Cloisons isolantes » / « Cloisons isothermes » | « Cloisons isolantes » (avec « isothermes » en synonyme dans le H1) | Client (`C16`) |
| 2 | Case de consentement du formulaire | Case obligatoire (API actuelle) / mention d'information | Mention d'information, après avis du juriste ; case non cochée en attendant | Juriste, ingénieur automatisation |
| 3 | Guides : lien direct ou envoi par e-mail | Lien direct (personas, NN/g) / e-mail et séquence de 3 messages (stratégie §4) | **Lien direct**, plus un formulaire facultatif pour recevoir la version imprimée par la poste | Chef de projet, stratège |
| 4 | Photos « retirer » | Retirer / regrouper sous « Autres réalisations (hors offre actuelle) » | Retirer | Client |
| 5 | Années des projets | Afficher les années EXIF (2012-2016) / attendre le client | Ne rien afficher sans confirmation ; demander des chantiers récents (`C39`) | Client |
| 6 | Zone par segment | « Toute la Suisse romande » pour tous / particuliers à Genève et sur La Côte, professionnels partout | La 2e option, si le client la confirme (`C21`) ; sinon la 1re | Client |
| 7 | Nom de l'OMC dans le bandeau | Garder en attendant l'accord / remplacer par la Salle de l'Alhambra | Remplacer en production tant que l'accord écrit manque | Client (lettre type de `logos-references.md` §7) |
| 8 | Accueil, carte projet 3 | AA6 (séjour, avant / après) / P4 (cage d'escalier) | AA6 si sa qualité suffit (rassure les particuliers) | Agence, après vérification |
