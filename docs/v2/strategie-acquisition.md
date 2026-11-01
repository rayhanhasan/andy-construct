# Stratégie d'acquisition et plan d'automatisation : Andy Construct (v2)

*Stratège acquisition (phase 1) · 31 octobre 2026 · Statut : proposition à valider avec les associés*
*Destinataires : chef de projet, ingénieur automatisation (phase 2), copywriter et architecte CRO, agence.*

> **Conventions.**
> - Les chiffres de marché, de coûts et de taux renvoient à une source. Ce qui n'a pas pu être sourcé porte la mention *« estimation à valider »*.
> - Montants en CHF, hors TVA. Les prix publiés en EUR ou en USD sont convertis à titre indicatif : 1 EUR ≈ 0,94 CHF, 1 USD ≈ 0,80 CHF *(taux à actualiser)*.
> - « Heures ouvrables » : du lundi au vendredi, de 7 h à 18 h (horaires à confirmer, voir `contenus-a-valider.md`), hors jours fériés du canton de Genève.
> - Les éléments « à fournir par le client » (horaires, « offre gratuite », nombre de chantiers, témoignages, accord des références) ne sont **jamais** utilisés en production avant validation. Voir le programme v2, §4.

---

## 0. Résumé en dix points

1. **Objectif à 12 mois (scénario M) : environ 30 demandes enregistrées par mois, dont deux tiers prioritaires, et environ 6 chantiers signés par mois issus de l'acquisition.** Il faut aussi passer à **50 avis Google**. Il n'existe aucune base mesurée (l'ancien site ne mesure plus rien depuis 2023) : les objectifs seront recalés au 3e mois sur des données réelles.
2. **Le site ne fait pas tout.** Les plus gros contrats viennent des **régies, architectes et communes**. Ces cibles se gagnent par la preuve (fiches projets, plaquette de références), la relation (prospection en 4 touches, partenariats) et les marchés publics (veille simap.ch, CFC 271, 283 et 285).
3. **La fiche Google et les avis restent le levier local n°1.** Pour une recherche locale, la carte Google s'affiche dans 93 % des cas ([Whitespark](https://whitespark.ca/blog/case-study-the-prevalence-of-ai-overviews-in-local-search/), étude américaine). Andy Construct n'a aujourd'hui aucun avis visible (`analyse-marche.md`, §4).
4. **Google Ads complète et accélère, avec un budget modulable** : CHF 400, 1'200 ou 2'500 par mois selon le scénario. Les campagnes sont découpées par zone, avec les services en groupes d'annonces. Les CPC suisses du second œuvre ne sont pas publiés : on les mesure dans l'outil de planification de Google dès la semaine 1.
5. **Les publicités Meta ne permettent probablement pas de cibler les « 50 ans et plus ».** Les travaux de réparation du logement entrent dans la catégorie spéciale « Logement », qui bloque le ciblage par âge en Europe, Suisse comprise (voir §3.5). C'est la créa qui fait le tri, pas le ciblage.
6. **L'automatisation fait le travail répétitif, les associés gardent l'humain** : rappeler, visiter, chiffrer, répondre aux avis. Le flux d'automatisation va du site à un endpoint PHP, puis à **n8n auto-hébergé en Suisse**, puis au **CRM Pipedrive** (alternative : Brevo CRM gratuit), et enfin aux e-mails et SMS.
7. **Quinze workflows** couvrent les dix scénarios demandés (a à j). Les associés agissent par **liens « en un clic »** dans leurs SMS et e-mails, sans avoir à ouvrir le CRM. Le reste du travail marketing tient dans une **routine de 2 h par semaine** (§5.9).
8. **La prospection B2B par e-mail à froid automatisé est exclue.** En droit suisse, la publicité de masse par voie électronique exige le consentement, y compris envers les entreprises ([art. 3 al. 1 let. o LCD](https://juriup.ch/lois/lcd/art-3/), [WEKA](https://www.weka.ch/themen/datenschutz-und-it-recht/datenschutz-umsetzen/article/datenschutz-newsletter-rechtssicheres-e-mail-marketing-in-der-schweiz/)). La séquence enchaîne donc **courrier postal, appel, e-mail sur demande, puis relance**.
9. **Le site reste sans cookies par défaut.** La mesure se fait avec Umami, sans cookie et hébergé en Suisse. Un bandeau de consentement n'apparaît que si l'on active la mesure de conversion Google Ads ou le reciblage (scénarios M et L). Depuis le 31.07.2024, Google applique sa politique de consentement aux utilisateurs suisses ([Google](https://www.google.com/about/company/user-consent-policy-help/)).
10. **Coût des outils : environ CHF 35 à 90 par mois.** Budget global (médias, outils et supports, hors heures d'agence) : environ **CHF 5'900, 18'300 ou 42'300 par an** selon le scénario S, M ou L (§8.3).

---

## 1. Objectifs chiffrés à 3, 6 et 12 mois

### 1.1 Tableau des objectifs (scénario M, de référence)

« M1 » désigne le mois de mise en ligne du site v2 et de vérification de la fiche Google.

| Indicateur | Définition et outil de mesure | M3 | M6 | M12 |
|---|---|---|---|---|
| Visites du site par mois | Umami (sessions) | 500 | 900 | 1'500 |
| Contacts web par mois | Formulaires envoyés + clics tél., e-mail et WhatsApp (Umami) | 10 | 22 | 45 |
| **Taux visite → contact web** | Contacts web / visites | **2,0 %** | **2,5 %** | **3,0 %** |
| **Demandes enregistrées par mois** | CRM, tous canaux : site, téléphone, e-mail, recommandation, B2B (hors appels d'offres) | **10** | **18** | **30** |
| dont priorité A ou B | Scoring §2 | ≥ 50 % | ≥ 60 % | ≥ 65 % |
| Délai de premier contact, demandes A | Médiane CRM | < 4 h ouvr. | < 2 h ouvr. | < 2 h ouvr. |
| **Taux demande → offre** | Offres envoyées / demandes du mois précédent | **55 %** | **60 %** | **65 %** |
| **Taux offre → signée** | Cohorte des offres envoyées depuis plus de 60 jours | **25 %** | **28 %** | **30 %** |
| Chantiers signés par mois issus de l'acquisition | Calcul des lignes précédentes | ≈ 1 à 2 | ≈ 3 | ≈ 6 |
| **Avis Google (cumul)** | Fiche Google | **15** | **30** | **50** |
| Note moyenne Google | Suivie, jamais « pilotée » (pas de sélection des clients) | suivie | suivie | suivie |
| Comptes B2B contactés (cumul) | Séquence (j) | 30 | 90 | 200 |
| Appels d'offres étudiés / déposés (cumul) | Veille (g) | 8 / 1 | 18 / 4 | 35 / 8 |
| Citations dans les IA | Test mensuel de 10 questions (`analyse-marche.md`, §6) | 1/10 | 3/10 | 5/10 |

**Variation selon le scénario budgétaire (§8.3), à M12 :**

| Scénario | Demandes par mois | Chantiers signés par mois | Avis (cumul) |
|---|---|---|---|
| S « Fondations » | ≈ 18 | ≈ 3 à 4 | 45 |
| M « Croissance » | ≈ 30 | ≈ 6 | 50 |
| L « Accélération romande » | ≈ 45 | ≈ 9 | 60 |

### 1.2 Hypothèses explicites

| # | Hypothèse | Fondement |
|---|---|---|
| H1 | Site v2 en ligne et fiche Google vérifiée en M1, mesure active dès le premier jour | Programme v2 ; recommandations à 0-30 jours de `analyse-marche.md`, §7 |
| H2 | **Aucune base historique fiable** : l'ancien site n'a aucune mesure depuis le 1.7.2023 | [Google, fin d'Universal Analytics](https://support.google.com/analytics/answer/11583528?hl=fr) ; `analyse-marche.md`, §4 |
| H3 | Taux visite → contact web de 2 à 3 % **sur l'ensemble du site**. Ce taux est plus bas que celui d'une page d'atterrissage, parce que la FAQ, les guides et les pages de réalisations attirent aussi des visites de simple information. | Médiane de conversion des pages d'atterrissage, tous secteurs : 6,6 % ([Unbounce 2024](https://prnewswire.com/news-releases/unbounces-2024-conversion-benchmark-report-proves-that-attention-spans-are-declining-and-so-are-conversion-rates-302239407.html)). Taux de conversion Google Ads moyen 2025 : 8,18 % ([WordStream/LocaliQ via Shopifreaks](https://www.shopifreaks.com/google-ads-cpcs-rose-to-5-42-in-2025-with-87-of-industries-seeing-increases-but-conversion-rates-climbed-to-8-18-as-automation-improves/), données américaines). L'application au site entier reste une *estimation à valider*. |
| H4 | Demande → offre de 55 à 65 %. Une partie des demandes est hors périmètre, trop petite ou hors zone ; le formulaire et le scoring filtrent mieux avec le temps. | *Estimation à valider* sur l'historique du client |
| H5 | Offre → signée de 25 à 30 %. La relance automatique (c) doit faire gagner quelques points. | Aucune référence publique suisse trouvée : *estimation à valider* sur l'historique 2025 du client |
| H6 | Avis : un premier lot de 30 clients récents ou fidèles, puis environ 50 % de réponses sur 5 à 8 chantiers terminés par mois | Objectifs à 90 et 180 jours repris de `analyse-marche.md`, §5. Taux de réponse : *estimation à valider* |
| H7 | Le scénario M représente environ 340 clics Google Ads par mois. Avec 5 % de conversion, cela donne environ 17 contacts. | CPC de CHF 3 à 4 et taux de 5 % : *estimation à valider* (§3.4) |
| H8 | Les objectifs ne comptent que le **flux nouveau**. Le chiffre d'affaires des clients existants n'y figure pas. | – |

**Données à demander au client pour caler la base** (15 minutes) : nombre de demandes reçues, d'offres envoyées et d'offres signées en 2025 ; panier moyen par type de client ; marge brute indicative ; capacité (nombre d'équipes et de chantiers simultanés).

### 1.3 Deux règles de pilotage

- **Capacité d'abord.** Si le carnet est plein à plus de 8 semaines, on baisse d'abord Google Ads (le levier le plus souple), puis Meta. On ne touche jamais aux avis, au SEO ni au B2B, qui sont des actifs de long terme.
- **Coût par demande maximal.** CPL max = panier moyen × marge brute × taux de signature. *Exemple illustratif* : 8'000 × 30 % × 30 % = CHF 720 à l'équilibre. La cible est un CPL d'au plus un tiers de ce maximum. À recalculer avec les vrais chiffres du client.

---

## 2. Entonnoir et scoring des prospects

### 2.1 Entonnoir

| Étape | Définition | Outil | Automatisation | Responsable | KPI |
|---|---|---|---|---|---|
| 1. Visite | Session sur le site | Umami | – | Agence | Visites par source |
| 2. Contact web | Formulaire envoyé ou clic tél., e-mail ou WhatsApp | Umami | – | – | Taux visite → contact |
| 3. Demande | Enregistrée au CRM, quel que soit le canal (y compris les appels saisis en 30 secondes, §5.4) | Pipedrive | (a) | Automatique | Demandes par source et par priorité |
| 4. Contact établi | Premier échange réel (appel abouti) | Pipedrive | (b) | Associé | Délai médian, % dans les délais |
| 5. Visite | Visite sur place planifiée ou faite | Pipedrive | Rappel de la veille | Associé | % de demandes visitées |
| 6. Offre envoyée | Montant et date saisis | Pipedrive | (c) | Associé | Délai visite → offre |
| 7. Signée | Affaire gagnée | Pipedrive | (k) | Associé | Taux de signature, CA signé |
| 8. Chantier terminé | Réception faite, réserves levées | Pipedrive | (d), (i) | Associé | Délai de réception |
| 9. Avis et recommandation | Avis publié, recommandation reçue | Fiche Google, CRM | (d), §3.11 | Automatique et associé | Avis par mois, % de recommandations |
| 10. Récurrence | Nouveau chantier d'un client existant | Pipedrive | (i), lettre trimestrielle | Associé | % du CA récurrent |

### 2.2 Champs de formulaire nécessaires au scoring (recommandation à l'architecte CRO)

Le formulaire actuel contient : nom, téléphone, e-mail, commune, type de travaux, message, fichier, « rappelez-moi », accord. On ajoute **quatre champs facultatifs en un clic**, sans saisie libre, idéalement en **deux étapes** : (1) projet, (2) coordonnées.

| Champ | Type | Options |
|---|---|---|
| Vous êtes | Boutons radio | Particulier propriétaire · Locataire · Régie / gérance / coopérative · Architecte / bureau d'études / entreprise générale · Commune / institution · Entreprise (bureaux, commerce) |
| Surface approximative | Liste | Moins de 15 m² (une réparation) · 15 à 50 m² (1 ou 2 pièces) · 50 à 200 m² (un appartement, un étage) · Plus de 200 m² ou plusieurs logements · Je ne sais pas |
| Quand souhaitez-vous faire les travaux ? | Liste | Dès que possible (moins d'un mois) · Dans 1 à 3 mois · Dans 3 à 6 mois · Pas encore défini |
| Comment nous avez-vous connus ? | Liste | Recherche Google · Carte Google · Recommandation · Régie ou architecte · Panneau de chantier ou véhicule · Facebook · LinkedIn · Autre |

Champs cachés : `src_utm_*`, `src_gclid` (avec consentement uniquement), `src_referrer`, `src_page_entree`, `form_t0` (horodatage signé pour l'anti-spam).

### 2.3 Grille de scoring (100 points, plus des bonus)

Le score est calculé par n8n dans un nœud Code. Les **poids sont dans un fichier JSON de configuration** (`automation/config/scoring.json`) pour être ajustables sans rien recoder.

| Critère | Valeur | Points |
|---|---|---|
| **Type de client** (0-30) | Commune / institution publique | 30 |
| | Régie / gérance / coopérative / fondation immobilière | 30 |
| | Architecte / bureau d'études / entreprise générale / direction de travaux | 25 |
| | Entreprise (bureaux, commerce, PME) | 20 |
| | Particulier propriétaire (PPE, villa) | 15 |
| | Non précisé | 10 |
| | Locataire (travaux soumis à l'accord de la régie) | 5 |
| **Service** (0-15) | Plusieurs prestations | 15 |
| | Isolation acoustique | 15 |
| | Placo (cloisons, faux-plafonds, doublages) | 15 |
| | Cloisons isothermes | 12 |
| | Peinture seule | 10 |
| | Hors des 4 services (façade, carrelage, etc.) | **Hors cible** |
| **Ampleur** (0-20) | Plus de 200 m² ou plusieurs logements | 20 |
| | 50 à 200 m² | 15 |
| | 15 à 50 m² | 8 |
| | Je ne sais pas / non renseigné | 6 |
| | Moins de 15 m² | 2 |
| **Commune / zone** (0-15) | Zone 1 : canton de Genève, district de Nyon | 15 |
| | Zone 2 : districts de Morges, Lausanne, Ouest lausannois, Lavaux-Oron, Riviera-Pays-d'Enhaut | 10 |
| | Zone 3 : reste de la Suisse romande (NE, FR, Valais romand, JU, Jura bernois, Nord vaudois, Broye, Chablais) | 5 |
| | Hors Suisse romande | **Hors cible** |
| **Délai** (0-10) | Moins d'un mois | 10 |
| | 1 à 3 mois | 8 |
| | 3 à 6 mois | 5 |
| | Pas encore défini | 2 |
| **Source** (0-10) | Recommandation, partenaire, prospection B2B, client existant | 10 |
| | Appel direct ou carte Google | 8 |
| | Recherche Google naturelle | 7 |
| | Google Ads, aimant à prospects | 6 |
| | Meta, LinkedIn | 4 |
| | Plateforme de mise en relation | 3 |
| **Bonus et malus** | Photo ou plan joint | +5 |
| | Téléphone fourni | +3 |
| | Message vide **et** aucun téléphone | −5 |

La commune est rattachée à sa zone par une table « NPA / commune → zone » (fichier JSON tiré de la liste officielle des NPA de La Poste). La commune saisie librement est normalisée par correspondance approchée.

### 2.4 Priorités et délais de rappel cibles

| Priorité | Score | Délai de premier contact | Canal | Notification aux associés |
|---|---|---|---|---|
| **A** | ≥ 65 | **< 2 h ouvrables** | Appel | SMS immédiat (entre 7 h et 20 h) + e-mail |
| **B** | 40 à 64 | **< 8 h ouvrables** (le jour même si la demande arrive avant 14 h, sinon le lendemain à 10 h) | Appel | SMS + e-mail |
| **C** | < 40 | **< 2 jours ouvrables** | Appel ou e-mail avec 3 questions de qualification | E-mail seul (inclus dans le récapitulatif du jour) |
| **Hors cible** | Critère bloquant | < 1 jour ouvrable | E-mail de réorientation **validé par un associé** (bouton « Envoyer la réponse type ») | E-mail |

### 2.5 Règles de dérogation (appliquées après le calcul)

1. Une **commune, institution, régie ou un architecte** n'est **jamais en dessous de B**, même en zone 3.
2. **Dégât ou fin de bail imminente**, si le message contient « dégât », « fuite », « état des lieux » ou « fin de bail » et que le délai est de moins d'un mois : **A**.
3. En zone 3, **B2B ou plus de 50 m²** : pas de pénalité de zone (les points de la zone 2 s'appliquent).
4. Les **appels d'offres publics** ne passent pas par ce scoring. Ils ont leur propre pipeline (g).
5. **Doublon** (même e-mail ou même téléphone dans les 30 derniers jours) : rattachement à l'affaire existante, sans nouvelle notification SMS.

### 2.6 Exemples de calcul

| Cas | Calcul | Score | Priorité |
|---|---|---|---|
| Propriétaire à Vésenaz, isolation acoustique, 15-50 m², 1-3 mois, Google naturel, téléphone fourni | 15+15+8+15+8+7+3 | 71 | A |
| Régie genevoise, peinture d'une cage d'escalier, plus de 200 m², moins d'un mois, appel direct | 30+10+20+15+10+8 | 93 | A |
| Architecte à Neuchâtel, cloisons, plus de 200 m², 3-6 mois, LinkedIn | 25+15+20+(10 par la règle 3)+5+4 | 79 | A |
| Propriétaire à Fribourg, peinture de 2 pièces, 1-3 mois, Google | 15+10+8+5+8+7 | 53 | B |
| Locataire à Lausanne, peinture d'une pièce, délai non défini, Meta, sans téléphone | 5+10+8+10+2+4 | 39 | C |

### 2.7 Recalibrage

Le scoring est recalibré tous les trimestres. Le rapport mensuel (h) croise le score avec le résultat (signée ou perdue). Si les C signent autant que les B, on ajuste les poids. À 6 mois, on compare le taux de signature par tranche de score ; la grille est bonne si les A signent au moins deux fois plus que les C.

---

## 3. Canaux

### 3.0 Vue d'ensemble

| # | Canal | Rôle | Cibles principales | Budget média M (CHF/mois) | Effort associés / semaine | Priorité |
|---|---|---|---|---|---|---|
| 3.1 | Fiche Google (Google Business Profile) | Être choisi sur la carte | Tous | 0 | 20 min | 1 |
| 3.2 | SEO local romand | Être trouvé, prouver | Tous | 0 | 10 min (photos, infos) | 1 |
| 3.3 | GEO (IA) | Être cité par les IA | Architectes, régies, PME | 0 | 0 | 2 |
| 3.4 | Google Ads Search (+ Microsoft) | Capter la demande immédiate | Propriétaires, PME, régies | 1'200 | 0 (agence) | 1 |
| 3.5 | Meta Ads | Notoriété locale, aimants | Propriétaires | 150 (300 sur 6 mois/an) | 5 min | 3 |
| 3.6 | LinkedIn | Crédibilité B2B | Architectes, régies, entreprises générales | 0 (organique) | 15 min | 2 |
| 3.7 | Prospection B2B directe | Gros comptes récurrents | Régies, architectes, communes | ≈ 80 (courrier) | 30 min | 1 |
| 3.8 | Veille simap / FAO | Marchés publics | Communes, institutions | 0 | 15 min | 2 |
| 3.9 | Partenariats | Recommandations croisées | Architectes, électriciens, menuisiers, EG, acousticiens | 0 | 10 min | 2 |
| 3.10 | Programme d'avis | Preuve, classement local | Clients | 0 | 10 min | 1 |
| 3.11 | Recommandation / parrainage | Bouche-à-oreille | Clients particuliers, partenaires | ≈ 20 | 0 | 2 |
| 3.12 | Reciblage (avec consentement) | Rappel aux visiteurs | Visiteurs du site | scénario L | 0 | 4 |
| 3.13 | E-mailing B2B trimestriel | Rester en tête | Contacts B2B ayant accepté, clients | 0 | 30 min par trimestre | 2 |

Tous les canaux pointent vers le même parcours : page de service ou fiche projet, puis appel ou formulaire, puis CRM.

---

### 3.1 Fiche Google (Google Business Profile)

| | |
|---|---|
| **Pourquoi** | La carte Google (« pack local ») domine les recherches locales. Google classe selon la pertinence, la distance et la notoriété, et le nombre d'avis y contribue ([Google](https://support.google.com/business/answer/7091?hl=fr)). |
| **Cible** | Tous, et en premier les particuliers et les gérants techniques sur mobile |
| **Actions** | Revendication, vérification, fiche complète, photos et posts réguliers, avis, réponses |
| **Contenu** | Photos de chantier, posts « chantier terminé », services décrits |
| **Budget** | CHF 0 |
| **KPI** | Appels, clics vers le site, demandes d'itinéraire (statistiques de la fiche), nombre et note des avis, position sur 10 requêtes locales (relevé trimestriel depuis Genève) |
| **Effort hebdo** | 20 min : 1 série de photos, la validation d'un post préparé par l'agence, les réponses aux avis |

**Mise en place (M0-M1) :**

- **Propriété.** La fiche est revendiquée avec l'adresse du domaine (`contact@andyconstruct.ch`). Les deux associés en sont **propriétaires** ; l'agence n'est que **gestionnaire**, jamais propriétaire.
- **Nom, adresse, téléphone (NAP)** identiques au registre du commerce et au site. Si les clients ne sont pas reçus à Carouge : adresse masquée et zone desservie déclarée (décision client, `analyse-marche.md`, §0).
- **Catégories** *(libellés exacts à choisir dans la liste française de l'interface)* :
  - principale : **Plâtrier** (ou équivalent « Entreprise de plâtrerie ») ;
  - secondaires : **Entrepreneur en cloisons sèches / plaquiste**, **Peintre en bâtiment**, **Entreprise d'isolation**, et **Service d'insonorisation** s'il existe dans la liste ;
  - aucune catégorie hors des 4 services (pas de « entreprise générale », pas de « plafonds tendus »).
- **Zone desservie.** Genève, puis les districts vaudois de la zone 2, puis les cantons de la zone 3. Selon les consignes Google, la zone ne doit pas dépasser environ 2 heures de route ([consignes Google](https://support.google.com/business/answer/3038177?hl=fr), à vérifier). On priorise donc Genève, Vaud et Neuchâtel, et on ne déclare le Jura et le Valais central qu'une fois validés par le client.
- **Services**, un par un sous chaque catégorie, avec une description de 1 ou 2 phrases :
  - Placo : doublage de murs, faux-plafond en plaques de plâtre, cloison légère, caisson, trappe ;
  - Peinture : murs et plafonds, rafraîchissement de fin de bail, cage d'escalier, bureaux ;
  - Isolation acoustique : doublage acoustique désolidarisé, faux-plafond acoustique, cloison acoustique, correction acoustique d'une salle ;
  - Cloisons isothermes : cloison isolante entre local chauffé et non chauffé, isolation du plafond de cave ou de garage *(définition à confirmer, `contenus-a-valider.md`, §4)*.
- **Description (750 caractères)** : reprendre le paragraphe d'identité du site (activité, 4 métiers, Carouge, registre depuis 2007 à confirmer, régies, architectes, collectivités, Suisse romande). Ni superlatif, ni « n°1 ».
- **Photos.** 30 au lancement (sélection du site, `selection-photos.md`), puis **4 à 8 par mois**, prises à chaque chantier : avant, pendant, après. Pas de visage sans accord ; pas d'intérieur identifiable de client privé sans accord.
- **Liens avec suivi.**
  - Site : `https://www.andyconstruct.ch/?utm_source=google&utm_medium=organic-local&utm_campaign=gbp-site`
  - Rendez-vous : `/contact.html?utm_source=google&utm_medium=organic-local&utm_campaign=gbp-rdv#demande` (ancre corrigée le 01.11.2026, audit SEO v4)

**Fonctionnement courant :**

- **Posts : 2 par mois.** Un « chantier terminé » (3 photos, 3 lignes : lieu, besoin, solution) et un conseil ou une actualité réelle. L'agence les rédige à partir des photos envoyées ; les associés valident en un clic (option k, §5.7).
- **Questions-réponses : n'y investissez pas.** Google a fermé l'API Q&R le 3.11.2025 et remplace progressivement la rubrique par une fonction de réponse par IA (« Ask Maps ») ([PPC Land](https://ppc.land/google-discontinues-business-profile-q-a-api-effective-november-3/), [Whitespark](https://whitespark.ca/blog/with-google-qa-gone-you-need-a-maps-ask-a-question-strategy/)). L'IA de Google puise dans la fiche, les avis et le site : la **FAQ du site** et des **services bien décrits** font désormais ce travail. Si la rubrique est encore visible en Suisse au lancement, on y place 5 questions-réponses reprises de la FAQ.
- **Messagerie** : elle n'existe plus. Google a supprimé le chat des fiches le 31.07.2024 ([Google Developers](https://developers.google.com/business-communications/business-messages/resources/release-notes/update-on-gbm)). Le contact passe par l'appel, le site ou WhatsApp.
- **Contrôle mensuel (5 min) :** vérifier les « modifications suggérées » par des tiers, les horaires des jours fériés et les doublons de fiche.
- **Bing Places et Apple Business Connect :** même contenu, à créer en M1 (Bing représente 10,8 % des recherches en Suisse, [Statcounter](https://gs.statcounter.com/search-engine-market-share/all/switzerland)).

---

### 3.2 SEO local romand

| | |
|---|---|
| **Pourquoi** | Ni Google ni une IA ne peuvent recommander une prestation qui n'est pas décrite en texte. « Une page dédiée par service » est le 2e facteur de visibilité dans les IA selon [Whitespark 2026](https://whitespark.ca/local-search-ranking-factors/). Les concurrents ont peu de contenu réel (`analyse-marche.md`, §3). |
| **Cible** | Tous ; pages services pour les particuliers et les PME ; fiches projets pour les régies, architectes et communes |
| **Actions** | 4 pages services ; pages canton et ville **avec un contenu réel uniquement** ; fiches projets ; un guide par mois ; liens tiers |
| **Contenu** | Une fiche projet et un guide par mois (12 + 12 sur l'année) |
| **Budget** | CHF 0 de média. Rédaction par l'agence (heures, §8.3) |
| **KPI** | Impressions et clics Search Console sur 30 requêtes cibles, pages indexées, entrées organiques sur les fiches projets, demandes avec source « organique » |
| **Effort hebdo** | 10 min : photos et 3 informations par chantier (lieu, besoin, solution), transmises par le lien d'envoi (k) |

**Architecture des contenus (à intégrer par l'architecte CRO dans `architecture-cro.md`) :**

| Type de page | Règle de création | Lancement | M6 | M12 |
|---|---|---|---|---|
| Page service (4) : placo, peinture, isolation acoustique, cloisons isothermes | Toujours. 600 à 1'000 mots : à quoi ça sert, pour qui, déroulement, normes citées prudemment (SIA 181, SIA 180, SIA 118, AEAI selon le projet), FAQ, réalisations liées | 4 | 4 | 4 |
| Fiche projet | Lieu et commune, année, type de client, besoin, solution et matériaux, 2 à 4 photos avec texte alternatif, phrase du client avec accord. Nom d'une marque privée seulement avec accord écrit. | 4 | 10 | 20 |
| Page canton (GE, VD, NE, FR, VS, JU et Jura bernois) | **Uniquement si au moins 2 fiches projets dans le canton**, plus un contenu local réel : délais d'intervention, communes desservies, contexte réglementaire local (p. ex. Genève : seuils IDC 2027, [ge.ch](https://www.ge.ch/connaitre-consommation-energie-batiment-idc/que-faire-resultat-idc-votre-immeuble)). Sinon, page « Zone d'intervention » unique. | 0 (zone unique) | 2 (GE, VD) | 3-4 |
| Page ville | **Uniquement si au moins un chantier réel dans la commune**, avec photos et 300 mots uniques au minimum. Candidates : Genève, Carouge, Collonge-Bellerive, Plan-les-Ouates, Coppet / Terre Sainte, Nyon, Lausanne. Sinon `noindex` ou pas de page. | 0 | 2 | 5 |
| Guide / FAQ approfondie | Une par mois (sujets ci-dessous) | 0 | 5 | 11 |

**Pages clonées interdites** (« faux-plafond Onex », « faux-plafond Lancy » avec le même texte) : ce sont des pages satellites (`analyse-marche.md`, levier 11).

**Calendrier des guides (un par mois, ordre indicatif) :**

1. Bruit des voisins : absorption ou isolation, quelle différence ?
2. Rafraîchissement de fin de bail : délais, préparation, état des lieux (cible régies).
3. Cloison placo, carreaux de plâtre ou brique : que choisir pour diviser une pièce ?
4. Isoler un plafond de cave ou de garage par l'intérieur.
5. Travaux en immeuble habité : comment cela se passe pour les locataires.
6. Réduire l'écho d'une salle communale ou d'une salle de réunion.
7. Prix d'un faux-plafond ou d'une peinture : de quoi dépend le montant, sans prix inventé.
8. SIA 181 expliquée simplement (architectes, PPE).
9. Peinture : quelle finition pour quelle pièce ?
10. Préparer sa visite de devis : les 10 questions à se poser.
11. Protection incendie des faux-plafonds : ce qui change avec la révision AEAI (reportée à l'automne 2027, [AIET](https://www.bpuk.ch/fileadmin/Dokumente/bpuk/public/fr/dokumentation/medienmitteilungen/2026/Communique_de_presse_AIET_Prescription_de_protection_incendie.pdf)), formulé prudemment.

**Vocabulaire romand à utiliser** dans les textes, les annonces et les mots-clés : « gypserie », « gypsier-peintre », « plâtrerie-peinture », « Rigips », « carreaux Alba », « régie », « offre », « fin de bail », « état des lieux », « PPE ».

**Liens et mentions tierces** (levier 8) :

- annuaires : local.ch, search.ch, GGE, Kompass (catégorie à corriger), architecteromand.ch, Houzz ;
- association professionnelle (vérifier l'affiliation, par exemple FREPP ou groupement genevois de la plâtrerie-peinture) ;
- page « entreprises mandatées » des architectes partenaires ;
- reportage de chantier proposé à [Batimag](https://www.batimag.ch/).

---

### 3.3 GEO (visibilité dans les IA)

| | |
|---|---|
| **Pourquoi** | Les aperçus IA de Google existent en Suisse depuis mars 2025. 73 % des Suisses ont déjà utilisé une IA, mais seulement 20 % des 70 ans et plus s'y disent à l'aise ([UZH/RTS](https://www.rts.ch/info/societe/2025/article/l-ia-creuse-le-fosse-numerique-etude-alarmante-sur-l-exclusion-en-suisse-29051234.html)). Le GEO touche donc surtout les **architectes et les collaborateurs de régie**. |
| **Cible** | Architectes, régies, PME |
| **Actions** | FAQ visible, JSON-LD cohérent, `llms.txt`, paragraphe d'identité, fiches projets factuelles, Bing Webmaster Tools et Bing Places (ChatGPT Search s'appuie surtout sur l'index de Bing, [BrightLocal](https://www.brightlocal.com/research/uncovering-chatgpt-search-sources/)), mentions tierces |
| **Contenu** | Celui du SEO (aucun contenu propre au GEO). Mise à jour du `llms.txt` à chaque fiche projet (générée par `tools/build/`). |
| **Budget** | CHF 0 |
| **KPI** | Test de 10 questions dans ChatGPT, Perplexity, Google et Copilot : Andy Construct est-il cité, et correctement ? (`analyse-marche.md`, §6) |
| **Effort hebdo** | 0 pour les associés. Agence : 15 min par mois pour le test |

**Automatisation optionnelle :** le test mensuel peut être lancé par n8n via les API de Perplexity ou d'OpenAI (10 questions, citation détectée par recherche de « Andy Construct » dans la réponse). Le résultat est consigné dans le rapport (h). Les réponses des API diffèrent de celles des interfaces grand public : on garde un test manuel trimestriel.

---

### 3.4 Google Ads Search (+ Microsoft Advertising)

| | |
|---|---|
| **Pourquoi** | Capter ceux qui cherchent **maintenant**, dès le premier mois, pendant que le SEO monte en puissance. Le budget se module selon la capacité (§1.3). |
| **Cible** | Propriétaires, PME, gérants techniques ; termes B2B en complément |
| **Actions** | 3 campagnes géographiques + 1 campagne marque + import Microsoft. Groupes d'annonces par service, 20 à 40 mots-clés chacun. Extensions d'appel et de lieu. Revue hebdomadaire des termes de recherche. |
| **Contenu** | Annonces responsives (RSA) par service, pages services en atterrissage |
| **Budget** | S : 400 · M : 1'200 · L : 2'500 CHF/mois (tableau ci-dessous) |
| **KPI** | CTR, CPC, part d'impressions, taux de conversion, coût par demande (CPL), CPL des demandes A et B, coût par chantier signé |
| **Effort hebdo** | Associés : 0. Agence : 30 min (termes de recherche, négatifs, enchères) |

#### 3.4.1 CPC estimés

**Aucune donnée publique fiable** n'existe pour les CPC du second œuvre en Suisse romande. Nous avons trois repères :

- l'indice Swiss Adex publiait un CPC moyen tous secteurs de CHF 1,57 à 1,89 ([markt-kom](https://www.markt-kom.com/en/?p=24895)), un chiffre ancien et non daté avec précision ;
- aux États-Unis en 2025, le CPC moyen tous secteurs est de 5,42 USD et celui de la catégorie « Maison et rénovation » dépasse 7 USD ([WordStream/LocaliQ via Shopifreaks](https://www.shopifreaks.com/google-ads-cpcs-rose-to-5-42-in-2025-with-87-of-industries-seeing-increases-but-conversion-rates-climbed-to-8-18-as-automation-improves/)), soit environ 1,5 fois la moyenne ;
- les recherches locales du type « artisan + ville » ont en général des CPC plus bas et une meilleure conversion (synthèse sectorielle, [Ostend](https://ostend.digital/google-ads-handwerker/), Allemagne).

**Méthode :** appliquer le facteur « rénovation » d'environ 1,5 fois à la moyenne suisse, puis majorer pour Genève (concurrence frontalière). Ce sont des **estimations à valider dans l'outil de planification des mots-clés en semaine 1**, avec un ciblage Genève et Vaud.

| Groupe d'annonces | CPC estimé (CHF) | Commentaire |
|---|---|---|
| Peinture | 2,00 à 4,00 | Le plus concurrentiel (nombreux peintres) |
| Placo / plâtrerie / gypserie | 1,50 à 3,50 | Moins de volume, intention précise |
| Isolation acoustique | 2,00 à 5,00 | Des annonceurs vaudois sont présents (`analyse-marche.md`, §3) |
| Cloisons isothermes / isolation intérieure | 2,00 à 4,50 | Volume faible ; vérifier l'intention |
| Marque | 0,20 à 0,60 | Protéger le nom |

#### 3.4.2 Structure : campagnes par zone, groupes par service

On découpe les campagnes par **zone** pour piloter le budget géographiquement, et les groupes d'annonces par **service** pour l'annonce et la page d'atterrissage. Le ciblage géographique est réglé sur « **Présence** : personnes qui se trouvent dans la zone », et non sur « intérêt pour la zone », afin d'exclure les recherches faites depuis la France voisine.

| Campagne | Zone ciblée | Groupes d'annonces | S | M | L |
|---|---|---|---|---|---|
| C1 Search : Genève et Terre Sainte / Nyon | Canton de Genève + district de Nyon | Placo, Peinture (exact seulement en S), Acoustique, Isotherme, Pros | 380 | 720 | 1'150 |
| C2 Search : arc lémanique vaudois | Districts de Morges, Lausanne, Ouest lausannois, Lavaux-Oron, Riviera-Pays-d'Enhaut | Placo, Peinture, Acoustique, Isotherme, Pros | – | 350 | 650 |
| C3 Search : reste de la Romandie | NE, FR (districts francophones), Valais romand, JU, Jura bernois, Nord vaudois, Broye | Acoustique, Placo, Pros (prestations au panier élevé) | – | – | 450 |
| C4 Marque | Suisse romande | Marque | 20 | 30 | 50 |
| C5 Microsoft Advertising (import de C1 et C2) | Idem | Idem | – | 100 | 200 |
| **Total (CHF/mois)** | | | **400** | **1'200** | **2'500** |

**Volume plafond :** la Suisse romande est un petit marché. Si la part d'impressions perdue à cause du budget est inférieure à 10 %, augmenter le budget ne sert à rien : on élargit plutôt les mots-clés ou les zones.

**Modulation saisonnière** *(estimation à valider)* :

- +20 % de février à mai et de septembre à novembre ;
- −50 % pendant les vacances du bâtiment de l'été et entre Noël et Nouvel An (dates à confirmer avec le client) ;
- aucune annonce pendant les fermetures.

#### 3.4.3 Mots-clés par groupe

Notation Google Ads : `[mot-clé]` = correspondance exacte ; `"mot-clé"` = expression. Au démarrage, **pas de requête large** ; on l'envisage seulement avec une stratégie d'enchères automatique et au moins 30 conversions par mois *(estimation à valider)*.

Les listes ci-dessous valent pour **C1 (Genève)**. Pour C2 et C3, on remplace les villes : Lausanne, Morges, Vevey, Montreux, Renens, Pully pour C2 ; Neuchâtel, Fribourg, Sion, Delémont, Bienne, Yverdon pour C3. Les mots-clés sans ville restent identiques, puisque le ciblage géographique fait le tri.

**Groupe « Placo / plâtrerie » (32), atterrissage sur la page Placo :**
`[plâtrier genève]` · `[plâtrerie genève]` · `[gypserie genève]` · `[gypsier genève]` · `[entreprise plâtrerie genève]` · `[plâtrerie peinture genève]` · `[gypserie peinture genève]` · `[plâtrier carouge]` · `[plâtrier nyon]` · `[plaquiste genève]` · `[faux plafond genève]` · `[faux plafond nyon]` · `"entreprise de plâtrerie"` · `"plâtrier peintre"` · `"gypsier peintre"` · `"entreprise gypserie"` · `"faux plafond placo"` · `"pose faux plafond"` · `"faux plafond suspendu"` · `"faux plafond appartement"` · `"cloison placo"` · `"pose cloison placo"` · `"cloison en plaques de plâtre"` · `"cloison rigips"` · `"cloison alba"` · `"séparer une pièce avec une cloison"` · `"doublage placo"` · `"doublage mur"` · `"caisson placo"` · `"devis plâtrerie"` · `"devis faux plafond"` · `"prix faux plafond m2"`

**Groupe « Peinture » (30), atterrissage sur la page Peinture :**
`[peintre genève]` · `[peintre en bâtiment genève]` · `[entreprise de peinture genève]` · `[entreprise peinture genève]` · `[peintre carouge]` · `[peintre nyon]` · `[peintre chêne-bourg]` · `"peintre en bâtiment"` · `"entreprise de peinture"` · `"entreprise gypserie peinture"` · `"peinture intérieure"` · `"peintre appartement"` · `"peinture appartement"` · `"repeindre appartement"` · `"rafraîchissement appartement"` · `"rafraîchir appartement"` · `"peinture fin de bail"` · `"peinture état des lieux"` · `"remise en état appartement"` · `"peinture cage d'escalier"` · `"peinture immeuble"` · `"peinture bureaux"` · `"peinture locaux commerciaux"` · `"peinture plafond"` · `"peintre plafond"` · `"devis peinture"` · `"devis peintre"` · `"prix peinture appartement"` · `"prix peintre m2"` · `"peintre près de chez moi"`

**Groupe « Isolation acoustique » (30), atterrissage sur la page Isolation acoustique :**
`[isolation phonique genève]` · `[isolation acoustique genève]` · `[insonorisation genève]` · `"isolation phonique appartement"` · `"isolation phonique plafond"` · `"isolation phonique mur"` · `"isolation phonique chambre"` · `"isolation phonique entre appartements"` · `"isolation acoustique plafond"` · `"isolation acoustique appartement"` · `"isoler du bruit des voisins"` · `"bruit voisin du dessus"` · `"bruit des voisins solution"` · `"insonoriser une pièce"` · `"insonorisation appartement"` · `"insonorisation plafond"` · `"faux plafond acoustique"` · `"faux plafond phonique"` · `"plafond acoustique"` · `"cloison acoustique"` · `"cloison phonique"` · `"doublage acoustique"` · `"isolation phonique bureau"` · `"acoustique salle de réunion"` · `"correction acoustique"` · `"réduire écho pièce"` · `"acoustique salle communale"` · `"entreprise isolation phonique"` · `"devis isolation phonique"` · `"prix isolation phonique"`

**Groupe « Cloisons isothermes / isolation intérieure » (24), atterrissage sur la page Cloisons isothermes** *(à activer quand le périmètre du service est confirmé)* :
`[isolation intérieure genève]` · `[isolation thermique genève]` · `"cloison isotherme"` · `"cloison isolante"` · `"cloison isolée"` · `"cloison isolation thermique"` · `"doublage isolant"` · `"doublage thermique"` · `"isolation thermique intérieure"` · `"isolation par l'intérieur"` · `"isolation intérieure appartement"` · `"isolation mur intérieur"` · `"isoler un mur froid"` · `"isolation mur placo"` · `"placo isolant"` · `"isolation plafond cave"` · `"isolation plafond garage"` · `"isolation plafond sous-sol"` · `"isolation local non chauffé"` · `"isolation entre garage et maison"` · `"entreprise isolation intérieure"` · `"devis isolation intérieure"` · `"isolation plafond parking"` · `"isolation cave immeuble"`
Option à ajouter si le client confirme cette activité : `"cloison chambre froide"`, `"panneaux isothermes"`.

**Groupe « Pros » (12, optionnel), atterrissage sur « Réalisations › Pour les professionnels » :**
`"entreprise plâtrerie peinture genève"` · `"entreprise second oeuvre genève"` · `"sous-traitant plâtrerie"` · `"sous-traitant faux plafonds"` · `"entreprise faux plafonds"` · `"entreprise cloisons bureaux"` · `"réaménagement bureaux cloisons"` · `"entreprise peinture régie"` · `"entreprise peinture immeuble locatif"` · `"plâtrerie peinture appel d'offres"` · `"entreprise placo bureaux"` · `"entreprise isolation acoustique bureaux"`

**Groupe « Marque » (C4) :** `[andy construct]` · `"andy construct"` · `[andyconstruct]` · `[andy construct carouge]` · `[andy construct genève]`

#### 3.4.4 Mots-clés négatifs

À placer dans une liste partagée au niveau du compte et à revoir chaque semaine.

- **Emploi et formation** : emploi, job, jobs, offre d'emploi, recrutement, postuler, stage, apprenti, apprentissage, formation, cours, école, diplôme, **cfc** (le CFC suisse est aussi un diplôme), salaire, devenir, métier.
- **Faire soi-même** : tuto, tutoriel, vidéo, youtube, soi-même, diy, bricolage, comment faire, pdf, fiche technique.
- **Achat de matériel** : acheter, achat, vente, magasin, prix plaque, leroy merlin, hornbach, jumbo, obi, landi, bauhaus, brico, location, louer, occasion, anibis, ricardo, tutti.
- **Hors sujet** : voiture, auto, moto, carrosserie, tableau, artiste, toile, aquarelle, huile, graffiti, ongles, maquillage, casque, bouchons, boules quies.
- **Hors services** : fenêtre, double vitrage, porte, façade, crépi, toiture, toit, extérieur, carrelage, parquet.
- **Hors zone** : france, annemasse, annecy, haute-savoie, thonon, gex, ferney, saint-julien, lyon, paris, belgique, québec.

On ajoute les noms de concurrents seulement s'ils génèrent des clics inutiles. Pas d'enchères sur la marque des concurrents.

#### 3.4.5 Annonces, extensions et horaires

**Exemples d'annonces responsives** (titres de 30 caractères au plus, comptés). Les mentions « 2007 » et « offre » dépendent de la validation client :

| Groupe | Titres (exemples) |
|---|---|
| Placo | « Plâtrier-peintre à Genève » (25) · « Placo, faux-plafonds, cloisons » (30) · « Siège à Carouge, depuis 2007 » (28) · « Offre écrite après visite » (25) |
| Peinture | « Peintre en bâtiment Genève » (26) · « Rafraîchissement fin de bail » (28) · « Chantier protégé et nettoyé » (27) |
| Acoustique | « Isolation phonique à Genève » (27) · « Bruit des voisins du dessus ? » (29) · « Faux-plafond acoustique » (23) |
| Isotherme | « Cloisons isolantes sur mesure » (29) · « Isolation plafond de cave » (25) |
| Tous | « Appelez le 022 771 20 15 » (24) |

Descriptions : 90 caractères au plus, à contrôler dans l'éditeur. Elles disent qui, quoi, où et la preuve, par exemple « Placo, peinture et isolation pour régies, architectes et propriétaires. Offre écrite en CHF. » **Interdits** : « n°1 », « meilleur », « prix imbattable », fausse urgence (LCD, art. 3 al. 1 let. b).

**Extensions :**
- **Appel** : le numéro fixe principal, affiché **du lundi au vendredi de 7 h à 18 h seulement** (quand quelqu'un répond). Les numéros de transfert Google sont disponibles en Suisse ([Google](https://support.google.com/google-ads/answer/2454052)) : un appel de plus de 60 secondes compte comme conversion, sans balise sur le site.
- **Lieu** : association avec la fiche Google.
- **Liens annexes** (25 caractères au plus) : Prestations · Réalisations · Régies et architectes · Demander une offre.
- **Accroches** (25 caractères au plus) : « Au registre depuis 2007 » (23) · « Siège à Carouge » (15) · « Offre écrite en CHF » (19) · « Chantier protégé, nettoyé » (25), à valider.
- **Extraits de site** : « Services : Placo, Peinture, Isolation acoustique, Cloisons isothermes ».
- **Images** : 4 photos réelles de chantier.
- **Pas d'extension « formulaire de prospect »** : les données resteraient chez Google, et le formulaire du site suffit.

**Horaires de diffusion :** du lundi au vendredi de 6 h 30 à 21 h, le samedi de 8 h à 14 h. Pas de diffusion le dimanche les 3 premiers mois, puis on teste.

**Enchères :**
- **Phase 1** (semaines 1 à 6) : « Maximiser les clics » avec un CPC maximum de CHF 5, ou CPC manuel.
- **Phase 2** : « Maximiser les conversions », lorsque le compte enregistre au moins 15 à 20 conversions en 30 jours *(seuil indicatif, estimation à valider)*. Les conversions sont les appels issus des annonces, plus les formulaires mesurés avec consentement (scénarios M et L, §6.4).

**Suivi :** suffixe d'URL finale `utm_source=google&utm_medium=cpc&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}`, plus le marquage automatique (gclid). Table de correspondance des identifiants dans le rapport (h).

**Annonces de services locaux** (« Garanti par Google ») : lancées en Europe, Suisse comprise, pour certains métiers de services à domicile ([Search Engine Land](https://searchengineland.com/google-takes-local-services-ads-to-europe-341284)). **Vérifier en M1 dans le compte** si la plâtrerie ou la peinture sont proposées à Genève. Si c'est le cas, c'est un test prioritaire : paiement par prospect.

---

### 3.5 Meta Ads (Facebook, Instagram)

| | |
|---|---|
| **Pourquoi** | Les 55-70 ans sont présents sur Facebook, et 89 % des plus de 65 ans utilisent internet ([Pro Senectute 2025](https://www.prosenectute.ch/fr/espace-pro/fond/etudes/digital-seniors-2025.html)). Meta crée de la **notoriété locale** et diffuse les **aimants** (guide « bruit »), là où Google ne capte que la demande déjà formulée. |
| **Cible** | Propriétaires de logement en zone 1, puis en zone 2 |
| **Actions** | 2 campagnes saisonnières par an (printemps, rentrée) ; déclaration de la catégorie spéciale ; publications organiques recyclées des fiches projets |
| **Contenu** | Carrousel avant/après (photos réelles), vidéo de 20 à 30 s d'un associé (sous-titrée, son coupé par défaut), visuel « guide bruit » |
| **Budget** | S : 0 · M : CHF 300/mois pendant 6 mois (moyenne de 150) · L : CHF 600/mois pendant 8 mois (moyenne de 400) |
| **KPI** | CPC sur le lien, CTR, coût par aimant téléchargé (cible ≤ CHF 20, *estimation à valider*), demandes attribuées (source CRM) |
| **Effort hebdo** | 5 min (modérer les commentaires) |

**Point bloquant à connaître :**
- La catégorie spéciale « Logement » de Meta couvre les **réparations du logement**, et elle s'applique aux annonceurs qui touchent l'Europe, **Suisse comprise** ([Jon Loomer](https://www.jonloomer.com/special-ad-categories-meta-ads/), [LeadSync](https://leadsync.me/blog/special-ad-category-meta/), [Meta Developers](https://developers.facebook.com/documentation/ads-commerce/marketing-api/audiences/special-ad-category)).
- Dans cette catégorie, le **ciblage par âge, par genre et par code postal**, les **audiences similaires** et les **exclusions** sont restreints, et le rayon géographique a un minimum.
- **Il n'est donc pas possible de cibler les « 50 ans et plus ».** Le périmètre exact est à vérifier dans le gestionnaire de publicités au moment de déclarer la catégorie. Ne pas la déclarer expose à des refus ou au blocage du compte.

**Conséquence : c'est la créa qui cible.** On utilise des visuels et des messages qui parlent aux propriétaires mûrs :
- « Votre appartement a 30 ans ? » ;
- « Le bruit du voisin du dessus » ;
- « Rafraîchir avant de vendre ou de louer » ;
- photos d'intérieurs genevois réels, ton sobre ;
- pas de jeunes mannequins ni de photos d'illustration génériques.

**Paramètres :**
- objectif « Trafic », car on n'a pas de pixel sans consentement ;
- destination : la page de l'aimant ou de la fiche projet, avec UTM ;
- emplacements : fils Facebook et Instagram ; **Audience Network exclu** ;
- zone : Genève + Nyon, en respectant le rayon minimum ;
- **formulaires instantanés exclus** : les données resteraient chez Meta, et le formulaire du site est plus clair pour le public senior.

**Organique :** la page Facebook existe (`facebook.com/andyconstruct.bajrami`). On y publie 2 fois par mois, en reprenant les posts de la fiche Google (k). On corrige le lien cassé de l'ancien site.

---

### 3.6 LinkedIn (architectes, régies)

| | |
|---|---|
| **Pourquoi** | Les architectes, les gérants techniques et les acheteurs des entreprises générales y vérifient le sérieux d'une entreprise. C'est un canal de **crédibilité** et de **relance douce** de la prospection (j). |
| **Cible** | Architectes, chefs de projet, directeurs de travaux, gérants techniques de régie, techniciens communaux |
| **Actions** | Page entreprise complète ; profil d'un associé ; 2 publications par mois ; 5 invitations ciblées par semaine (comptes de la liste B2B) ; sponsorisé uniquement en scénario L |
| **Contenu** | Fiche projet (photos + 3 lignes techniques), coulisses (pose d'une ossature, désolidarisation acoustique), « une norme expliquée », mise à jour de la plaquette |
| **Budget** | S et M : 0 (organique) · L : CHF 700/mois sur 2 vagues de 2 mois (février-mars, septembre-octobre). Minimum LinkedIn : 10 USD par jour ([LinkedIn](https://business.linkedin.com/marketing-solutions)) |
| **KPI** | Abonnés de la page, invitations acceptées, messages reçus, téléchargements de la plaquette depuis LinkedIn (`utm_source=linkedin`), rendez-vous B2B |
| **Effort hebdo** | 15 min (5 invitations personnalisées, 2 commentaires) |

**Sponsorisé (scénario L) :**
- format « document » (extrait de la plaquette, 4 pages) ;
- audience par **liste d'entreprises** (régies, bureaux d'architectes et entreprises générales de la liste B2B, environ 150 comptes), plus les fonctions concernées (immobilier, architecture, construction) à Genève et dans le canton de Vaud ;
- destination : la page de la plaquette, avec UTM ;
- formulaire LinkedIn possible, avec une mention claire de l'usage des données.

**CPC LinkedIn :** élevé, de l'ordre de plusieurs USD par clic *(estimation à valider dans Campaign Manager)*.

La balise de suivi LinkedIn (Insight Tag) n'est posée qu'avec consentement.

---

### 3.7 Prospection B2B directe

| | |
|---|---|
| **Pourquoi** | Un seul mandat de régie ou de commune vaut des dizaines de chantiers de particuliers. À Genève, un lot de second œuvre de moins de CHF 150'000 peut être attribué **de gré à gré**, et un lot de 150'000 à 250'000 **sur invitation** ([ge.ch](https://www.ge.ch/role-autorites-adjudicatrices-marches-publics/principes-types-procedures-cadre-legal)). Il faut donc **être connu avant** l'appel d'offres. |
| **Cible** | Régies, gérances, coopératives, fondations immobilières ; bureaux d'architectes ; services des bâtiments des communes ; entreprises générales |
| **Actions** | Séquence en 4 touches (j) : courrier, appel, e-mail sur demande, relance. Visite d'un chantier en cours. Inscription sur les listes d'entreprises consultées. |
| **Contenu** | Plaquette de références (imprimée et PDF), fiches projets ciblées, check-list « site occupé » (§4) |
| **Budget** | Courrier : environ CHF 2 par envoi (affranchissement B à CHF 1,00 selon [La Poste](https://www.post.ch/fr/expedier-des-lettres/lettres-suisse), plus l'impression), soit environ CHF 40 à 80 par mois. Plaquette imprimée : *estimation à valider* (100 exemplaires) |
| **KPI** | Comptes contactés, appels aboutis, plaquettes envoyées sur demande, rendez-vous ou visites, demandes de prix, inscriptions sur une liste d'entreprises consultées, CA B2B signé |
| **Effort hebdo** | 30 min (5 appels de 5 minutes, saisie des résultats en un clic) |

**Liste cible (à constituer en M2, environ 200 comptes, par paliers) :**

| Palier | Segment | Exemples et sources (liste indicative, à vérifier et compléter) | Nombre |
|---|---|---|---|
| 1 | Régies genevoises et du district de Nyon | Membres de l'[USPI Genève](https://www.uspi-geneve.ch) ; p. ex. Naef, SPG, Pilet & Renaud, Brolliet, Moser Vernet & Cie, Comptoir Immobilier, Régie du Rhône, Rosset & Cie, Gérofinance-Dunand, Bernard Nicod | 30 |
| 1 | Communes déjà clientes ou proches | Ville de Genève (service des bâtiments), Collonge-Bellerive, Plan-les-Ouates, communes des Trois-Chêne, Carouge, Coppet | 10 |
| 1 | Bureaux d'architectes avec des projets de transformation | Mandataires relevés dans la **FAO de Genève** (rubrique des autorisations de construire), dans les avis d'**adjudication** de simap pour les CFC 271/283/285, et dans les annuaires de la SIA (sections de Genève et Vaud), de la FAS et d'architecteromand.ch | 40 |
| 2 | Régies vaudoises | Membres de l'USPI Vaud ; p. ex. Bernard Nicod, Naef, Domicim, Cogestim, Comptoir Immobilier, Gérofinance ; antennes romandes de Livit, Privera, Wincasa, Verit | 30 |
| 2 | Coopératives et fondations | Groupement des coopératives d'habitation genevoises, fondations immobilières de droit public (GE), coopératives vaudoises | 20 |
| 2 | Entreprises générales | Implenia, Losinger Marazzi, HRS, Steiner, Induni, entreprises générales régionales | 15 |
| 2 | Communes vaudoises (Nyon, Morges, Lausanne-Ouest) | Services techniques | 25 |
| 3 | NE, FR, VS, JU | Régies et communes principales | 30 |

**Constitution de la liste :**
- l'agence la constitue dans le CRM (pipeline « Prospection B2B ») avec un **contact nommé** par compte : gérant technique, associé architecte ou technicien communal ;
- champs obligatoires : source de la donnée, **astérisque vérifié dans l'annuaire** (oui ou non), date de vérification ;
- aucune adresse e-mail n'est importée pour un envoi automatique (voir §9.2).

**Communes :** le message porte sur l'inscription sur la **liste des entreprises consultées** pour les procédures de gré à gré et sur invitation, avec la plaquette et les attestations (AVS, LPP, CCT du second œuvre romand, assurance RC, impôts, TVA : *à préparer une fois avec le client*).

**Cadence :** 5 nouveaux comptes par semaine (courriers envoyés automatiquement le lundi), soit environ 20 par mois. Rythme tenable avec 30 minutes d'appels par semaine. La séquence détaillée est au §5.7 (j).

---

### 3.8 Veille des appels d'offres (simap.ch, FAO)

| | |
|---|---|
| **Pourquoi** | Les pouvoirs publics ont augmenté leurs investissements dans le bâtiment de 8,4 % en 2025 ([LFM / OFS](https://www.lfm.ch/actualite/suisse/investissements-beton-dans-la-construction-suisse-en-2025/)). Les lots de plâtrerie, faux-plafonds et peinture sont publiés sous les codes **CFC 271, 283 et 285** (exemple réel : [FAO Vaud](https://www.faovd.ch/marches-publics/detail/2216/1179973/fondation-mont-calme-lausanne-cfc-271-283-285-platrerie-faux-plafond-peinture-pour-la-construction-d-un-ems-de-122-lits/)). |
| **Cible** | Communes, cantons, fondations et institutions publiques de Suisse romande |
| **Actions** | Abonnement simap gratuit, veille hebdomadaire automatisée (g), décision « on y va / on laisse » en un clic, dossier administratif type prêt une fois pour toutes |
| **Contenu** | Plaquette, références publiques, attestations |
| **Budget** | CHF 0 : simap.ch est gratuit ([PME admin.ch](https://www.kmu.admin.ch/de/teilnahme-an-einer-ausschreibung)) |
| **KPI** | Appels d'offres repérés, étudiés, déposés, gagnés ; montant adjugé ; délai de préparation |
| **Effort hebdo** | 15 min (décision sur le récapitulatif du lundi). Le chiffrage d'une soumission n'est pas compté ici. |

**Paramètres de la veille :**
- **Codes CFC (BKP)** : 271 Plâtrerie, 283 Faux-plafonds, 285 Traitement des surfaces intérieures, et 277 Cloisons en éléments selon les prestations réelles (à valider).
- **Codes CPV** : 45410000 (plâtrerie), 45421146 (faux-plafonds suspendus), 45421141 (cloisonnement), 45442100 (peinture), 45320000 (isolation), 45323000 (isolation phonique).
- **Cantons** : GE, VD, NE, FR, VS, JU, BE (Jura bernois).
- **Mots-clés** : « plâtrerie », « gypserie », « faux-plafond », « peinture intérieure », « acoustique ».

**Sources :**
1. L'**abonnement natif de simap.ch** (alertes par e-mail sur un profil de recherche, gratuit) sert de filet de sécurité.
2. L'**API de lecture publique de simap.ch** (`www.simap.ch/api`, documentation sur simap.ch/api-doc, recherche par canton, CPV, date et texte, codes BKP, sans authentification d'après un client open source testé le 26.07.2026, [swiss-procurement-mcp](https://pypi.org/project/swiss-procurement-mcp)) alimente le workflow (g). Aucune licence de données ouvertes n'est publiée : usage interne de veille uniquement, conforme aux conditions de simap.
3. La **FAO de Genève** (autorisations de construire) et les **avis d'adjudication simap** sont relevés une fois par mois pour alimenter la liste des architectes et la veille concurrentielle (qui gagne quoi, à quel prix).

**Rappels importants :**
- Les procédures de **gré à gré et sur invitation ne sont pas publiées**. D'où la prospection des communes (§3.7).
- **Pendant une procédure, aucune relance commerciale** vers l'adjudicateur en dehors des canaux prévus (questions écrites). Le pipeline « Marchés publics » est exclu des scénarios (c) et (e).

---

### 3.9 Partenariats

| | |
|---|---|
| **Pourquoi** | Les clients achètent souvent un **ensemble de travaux**. L'électricien, le menuisier ou l'acousticien est consulté avant ou en même temps qu'Andy Construct. |
| **Cible** | Architectes (liste « entreprises de confiance »), électriciens (spots, gaines dans les faux-plafonds), menuisiers (portes, cloisons), sanitaires et carreleurs (salles de bains), **bureaux d'ingénieurs acousticiens** (ils prescrivent les solutions), entreprises générales, courtiers immobiliers (préparation à la vente), administrateurs de PPE |
| **Actions** | 5 partenaires en M5, 10 en M12. Café trimestriel. Fiche partenaire réciproque. Registre des recommandations dans le CRM (organisation de type « Partenaire »). |
| **Contenu** | Plaquette, fiche « comment nous travaillons avec les autres corps de métier » (coordination, planning, propreté) |
| **Budget** | CHF 0 |
| **KPI** | Recommandations reçues et données, CA issu des partenaires |
| **Effort hebdo** | 10 min (un appel ou un message par semaine en moyenne) |

**Règle :** pas de commission occulte. Une commission éventuelle est **écrite et connue du client final**. Jamais d'avantage personnel à un employé d'une régie, d'un bureau ou d'une commune (corruption privée, art. 4a LCD ; avantage accordé à un agent public, art. 322quinquies CP). Voir §9.4.

---

### 3.10 Programme d'avis clients

| | |
|---|---|
| **Pourquoi** | Les avis pèsent sur le classement local ([Google](https://support.google.com/business/answer/7091?hl=fr)) et sur la visibilité dans les IA ([Whitespark 2026](https://whitespark.ca/local-search-ranking-factors/)). La branche affiche très peu d'avis (`analyse-marche.md`, §3). |
| **Cible** | Tous les clients dont le chantier est réceptionné. Les clients B2B aussi (gérants, architectes), sur Google et par un témoignage écrit avec accord pour le site. |
| **Actions** | Un **premier lot** de 30 clients récents ou fidèles en M1 (envoi par (d) en mode manuel), puis **(d) automatique** après chaque réception ; réponse à **chaque** avis sous 48 h ; carte avec code QR remise à la réception |
| **Contenu** | Lien direct vers le formulaire d'avis, modèles de réponse (positif, mitigé, négatif) |
| **Budget** | CHF 0 (cartes : environ CHF 50 par an, *estimation*) |
| **KPI** | Avis par mois, % de clients ayant laissé un avis, délai de réponse, mention du type de travaux et de la commune dans l'avis |
| **Effort hebdo** | 10 min (relire et publier les réponses préparées) |

**Règles Google à respecter** ([politique Google](https://support.google.com/contributionpolicy/answer/7400114?hl=fr)) :
- **ne pas solliciter les avis positifs de façon sélective** : tous les clients reçoivent la même demande ;
- ne pas décourager les avis négatifs ;
- **aucune contrepartie** ;
- pas d'avis rédigé par le personnel ou les proches.

On peut **décaler** la demande jusqu'à la levée des réserves, mais jamais **filtrer** selon la satisfaction présumée. On ne fait **pas** d'enquête de satisfaction préalable qui conditionnerait l'envoi du lien.

**Modèles de réponse** (l'agence les prépare et les associés les signent) :
- **positif** : merci, rappel du chantier (type et commune), pas de formule creuse ;
- **négatif** : on reconnaît, on propose un appel, aucun détail privé, jamais d'argument agressif.

---

### 3.11 Recommandation et parrainage

| | |
|---|---|
| **Pourquoi** | Le bouche-à-oreille est le premier canal historique d'une entreprise de 19 ans. On le **systématise** sans le dénaturer. |
| **Cible** | Clients particuliers satisfaits, partenaires, gérants qui recommandent à leurs collègues |
| **Actions** | Question posée en fin de chantier (« Connaissez-vous quelqu'un… ? ») ; 2 cartes de visite « recommandation » remises ; champ « Recommandé par » dans le formulaire ; remerciement automatique au recommandant (avec son accord) |
| **Contenu** | Carte « Merci de nous recommander » avec code QR (`utm_source=recommandation&utm_medium=print`) |
| **Budget** | Remerciement **modeste et non conditionné à un avis** pour les particuliers, p. ex. un don de CHF 50 à une association locale choisie par le recommandant, une fois le chantier recommandé signé *(montant à valider)*. **Rien** pour les employés de régies, de bureaux ou de communes (§9.4). |
| **KPI** | % des demandes de source « recommandation », taux de signature de ces demandes |
| **Effort hebdo** | 0 (intégré à la réception de chantier) |

**Protection des données :** c'est la personne recommandée qui nous contacte, en citant le nom du recommandant. On ne saisit pas les coordonnées d'un tiers à son insu.

---

### 3.12 Reciblage (uniquement avec consentement)

| | |
|---|---|
| **Pourquoi** | Rappeler Andy Construct aux visiteurs qui ont vu une page de service sans prendre contact. Le cycle de décision d'un propriétaire est de plusieurs semaines. |
| **Cible** | Visiteurs **ayant accepté** les cookies publicitaires |
| **Actions** | Scénario L uniquement (ou M si le site dépasse environ 1'000 visites par mois). Bandeau de consentement léger, avec un **refus aussi visible** que l'acceptation. Listes : visiteurs des pages services sur 30 jours, sans conversion ; personnes ayant téléchargé la plaquette (LinkedIn). |
| **Contenu** | Fiches projets, extraits d'avis réels, guide « bruit » |
| **Budget** | 10 à 15 % du budget payant du scénario L (inclus dans les montants de Google, Meta et LinkedIn) |
| **KPI** | Taux de consentement, taille des listes, coût par demande assistée |
| **Effort hebdo** | 0 |

**Seuils de liste :** Google Ads exige une taille minimale de liste avant diffusion (de l'ordre de 100 utilisateurs actifs pour le Réseau Display et 1'000 pour le Réseau de Recherche, *à vérifier dans le compte*). Avec un taux de consentement inconnu, le reciblage n'est **pas rentable sous environ 1'000 visites par mois** *(estimation à valider)*.

**Cadre légal :** le PFPDT admet pour la publicité ciblée de « profilage normal » une possibilité d'opposition (opt-out) bien visible ([guide cookies du PFPDT, v1.1 du 6.10.2025](https://www.edoeb.admin.ch/dam/fr/sd-web/brLL9rM3ny9d/Leitfaden%20des%20ED%C3%96B%20betreffend%20Datenbearbeitungen%20mittels%20Cookies%20und%20%C3%A4hnlichen%20Technologien%20V.%201.1%20vom%2006.10.2025_FR.pdf), ch. 3.11.2). Mais **le programme v2 impose le consentement préalable** pour tout cookie non essentiel, et Google l'exige pour les utilisateurs suisses depuis le 31.07.2024. **Règle : rien ne se charge avant un clic sur « Accepter ».**

---

### 3.13 E-mailing B2B trimestriel

| | |
|---|---|
| **Pourquoi** | Rester en tête des gérants et des architectes **entre deux besoins**. Une régie relance un appel d'offres ou un rafraîchissement plusieurs fois par an. |
| **Cible** | Contacts B2B **ayant accepté** de la recevoir (double confirmation), et clients B2B existants sous l'exception « clients » de l'art. 3 al. 1 let. o LCD, à condition qu'ils aient été informés de leur droit d'opposition (§9.2) |
| **Actions** | 4 envois par an (mars, juin, septembre, décembre) via Brevo ; segments régies, architectes et communes ; envoi le mardi à 8 h 30 |
| **Contenu** | 1 chantier récent (photo + 3 lignes), 1 point technique (SIA 181, AEAI 2027, IDC Genève 2027, prudemment), 1 information pratique (créneaux de planning réellement disponibles, sans fausse rareté), 1 seul appel à l'action (« Appeler » ou « Demander une visite »). Sobre, presque en texte brut. |
| **Budget** | CHF 0 (offre gratuite de Brevo : 300 e-mails par jour, [aide Brevo](https://help.brevo.com/hc/en-us/articles/208580669)) |
| **KPI** | Clics, réponses, demandes attribuées (`utm_source=newsletter`), désinscriptions (< 0,5 % par envoi, *estimation*). Le taux d'ouverture est peu fiable à cause du blocage des pixels (Apple). |
| **Effort** | 30 min par trimestre (l'agence rédige à partir des fiches du trimestre, les associés valident) |

---

## 4. Offres d'appel (aimants à prospects)

**Règles communes :**
- un PDF sobre aux couleurs de la charte, **texte d'au moins 12 pt**, contrastes AA, aucune photo d'illustration générique ;
- **version imprimée envoyée par la poste sur demande** (case « Je préfère le recevoir par la poste », envoi automatique par Pingen, §5.3), pensée pour les 65 ans et plus ;
- formulaire minimal : prénom, e-mail **ou** adresse postale, profil (bouton radio), case **non cochée** « Recevoir la lettre trimestrielle » ;
- mention claire : « Vous recevrez le guide puis 2 e-mails de conseils sur ce sujet ; désinscription en un clic » (base de la séquence (f), §9.2).

| # | Cible | Titre | Contenu | Format | Appel à l'action | Mise en ligne |
|---|---|---|---|---|---|---|
| 1 | Régies, architectes, communes | **« Dossier de références Andy Construct »** (plaquette) | Identité (registre du commerce, IDE, siège, associés), 4 métiers, CFC traités, 8 à 10 références **datées** avec photos (références publiques d'abord ; marques privées seulement avec accord), méthode, normes citées prudemment, attestations disponibles sur demande, contacts directs | PDF de 8 pages + version imprimée | « Nous inviter à soumissionner » · « Visiter un chantier en cours » | M2 |
| 2 | Régies, gérants techniques | **« Travaux en immeuble habité : la check-list de la régie »** | **Avant** : avis aux locataires (modèle de lettre), planning, accès et clés, parties communes, protections. **Pendant** : horaires, poussière, interlocuteur unique, propreté quotidienne. **Après** : nettoyage, procès-verbal de réception, photos. | PDF de 2 pages | « Faire chiffrer vos prochains rafraîchissements de fin de bail » | M3 |
| 3 | Propriétaires de 55 à 70 ans | **« Réduire le bruit dans un appartement : ce qui marche vraiment »** | Reconnaître le type de bruit (aérien ou d'impact) ; absorber ou isoler ; solutions par ampleur (doublage désolidarisé, faux-plafond acoustique, cloison) ; ce qui ne marche pas (boîtes à œufs, mousse collée) ; en PPE, se renseigner auprès de l'administrateur ; 8 questions à poser à une entreprise | PDF de 8 pages + version imprimée | « Demander une visite pour évaluer votre situation » + téléphone en gros | M4 |
| 4 | Architectes | **« Acoustique en rénovation : 7 points à régler avant l'appel d'offres CFC 271/283 »** | Exigences visées (SIA 181 : minimales ou accrues, selon le projet), désolidarisation, traversées, trappes, coordination avec l'électricien, essais, documents à demander à l'entreprise | PDF de 2 pages | « Faire relire un descriptif ou obtenir un pré-chiffrage » | M7 |
| 5 | Propriétaires (vente ou location) | **« Rafraîchir son logement avant de le vendre ou de le louer »** | Priorités par pièce, plafonds et murs, délais réalistes, préparation, état des lieux | PDF de 4 pages | « Recevoir une offre écrite » | M9 |
| 6 | Communes et institutions | **« Rénover une salle communale : acoustique, planning, sécurité »** | Points à anticiper (écho, usages multiples, calendrier des manifestations, concept incendie défini par le projet, sans promesse de performance), références de salles communales | PDF de 2 pages | « Nous inscrire comme entreprise à consulter » | M10 |
| 7 | PME | **« Réaménager ses bureaux sans fermer »** | Cloisons, acoustique des salles de réunion, peinture ; planning type sur un week-end ; check-list du locataire de bureaux (accord du bailleur, état des lieux) | PDF de 2 pages | « Planifier une visite hors heures de bureau » | M11 |

**Plaquette (n° 1) : en accès libre**, sans formulaire. Un professionnel ne doit pas être freiné. Le téléchargement est mesuré (`plaquette_telechargee`). Une case facultative « Recevoir les mises à jour de la plaquette » permet l'inscription.

**Guides (n° 2 à 7) :** l'envoi se fait par e-mail (lien). Cela vérifie l'adresse sans double opt-in pour le guide lui-même ; l'inscription à la lettre trimestrielle, elle, passe par une double confirmation.

---

## 5. Plan d'automatisation

### 5.1 Principes

1. **Le site ne dépend jamais de l'orchestrateur pour recevoir une demande.** Le PHP envoie toujours un e-mail aux associés. n8n ajoute le reste : CRM, score, SMS, relances.
2. **Une seule source de vérité : le CRM.** Toutes les relances reposent sur des **dates et des statuts stockés dans le CRM**, lus par une « horloge ». On n'utilise **pas** de longues pauses dans n8n (fragiles en cas de redémarrage).
3. **Les associés n'ouvrent presque jamais le CRM.** Ils agissent par **liens en un clic** (signés et datés) dans leurs SMS et e-mails, et par une **saisie express** pour les appels reçus.
4. **Chaque message automatique part au nom d'un associé**, depuis une adresse du domaine. Une réponse arrive chez un humain.
5. **Pression commerciale plafonnée :** au plus **un message marketing par contact tous les 30 jours**, toutes automatisations confondues (champ `dernier_message_marketing`). Les messages de service (accusé de réception, suivi d'offre) ne sont pas plafonnés, mais s'arrêtent dès qu'il y a une réponse.
6. **Protection des données dès la conception :** données hébergées en Suisse ou dans l'UE, minimisation, purge automatique (§9.1).

### 5.2 Architecture

```
 Visiteur ─▶ site statique (hébergement mutualisé, CH)
               │  POST multipart (formulaire, aimant, saisie express)
               ▼
        /api/demande.php  /api/aimant.php  /api/fichier.php  /api/cron-relais.php
        • validation, piège à robots, délai minimal, limite par IP (hachée)
        • fichiers → dossier privé hors racine web (purge à 30 j)
        • SMTP authentifié (PHPMailer) ──▶ e-mail immédiat aux associés (+ pièces jointes)
        • webhook signé HMAC-SHA256 ──▶ n8n          (échec → file d'attente JSON
               │                                       privée, relancée toutes les 10 min ;
               │                                       si échec > 1 h : alerte agence
               │                                       + accusé de réception générique)
               ▼
   n8n (auto-hébergé, VPS Infomaniak en Suisse, Docker + PostgreSQL + sauvegardes)
   WF01-WF15 : normalisation, dédoublonnage, score, routage, horloge, rapports
     │            │               │                 │                  │
     ▼            ▼               ▼                 ▼                  ▼
  Pipedrive    SMTP domaine    ASPSMS (CH)       Brevo (UE)        API externes
  (CRM, UE)    (e-mails 1:1)   SMS associés      listes, séquences  simap (lecture), Umami,
  webhooks ◀── au nom de       et clients        aimants, lettre    Search Console, Places,
  « affaire    l'associé                         trimestrielle,     Google Ads (rapport),
  modifiée »                                     désinscriptions    Pingen (courrier)
     ▲
     └── liens en un clic (/webhook/action?t=<jeton signé>) depuis les SMS et e-mails
```

### 5.3 Choix des outils

| Fonction | **Par défaut** | Alternative | Pourquoi ce choix |
|---|---|---|---|
| CRM | **Pipedrive, formule Lite, 2 utilisateurs** (≈ 14 EUR par utilisateur et par mois en facturation annuelle, [Zeeg](https://zeeg.me/en/blog/post/pipedrive-pricing), à vérifier sur pipedrive.com) | **Brevo CRM gratuit** (1 utilisateur, 50 affaires ouvertes, 1 pipeline, [aide Brevo](https://help.brevo.com/hc/en-us/articles/208580669)) | Pipedrive : application mobile très bonne pour des associés sur les chantiers, pipeline visuel, rappels d'activité, **webhooks natifs et nœud déclencheur n8n**, éditeur européen (Pipedrive OÜ, Estonie ; **région d'hébergement UE à confirmer dans le DPA**). Brevo convient au scénario S (zéro abonnement, tout en un), mais 1 seul utilisateur et 50 affaires ouvertes deviennent vite limitants. |
| Orchestrateur | **n8n Community auto-hébergé** sur un VPS **Infomaniak (Suisse)**. VPS Lite dès CHF 2,70 par mois, palier 2 vCPU / 4 Go recommandé, soit environ CHF 7 à 9 ([Infomaniak](https://www.infomaniak.com/fr/hebergement/vps-lite)) | **n8n Cloud Starter**, 20 EUR par mois en facturation annuelle, 2'500 exécutions par mois, données à Francfort ([n8n](https://n8n.io/pricing/)) | Données en Suisse, pas de limite d'exécutions (l'horloge tourne toutes les 15 minutes), coût minimal. **Le VPS et l'instance sont au nom du client** : la licence d'usage de n8n vise l'usage interne. L'agence assure la maintenance (mises à jour mensuelles). n8n Cloud si personne ne peut maintenir un serveur. **Make n'est pas retenu** : facturation à l'opération, moins de contrôle sur l'hébergement. |
| E-mails 1:1 | SMTP de la messagerie du domaine (`prenom@andyconstruct.ch`) | Brevo transactionnel | Ton personnel, les réponses arrivent chez l'associé, bonne délivrabilité (SPF, DKIM, DMARC). |
| E-mails marketing | **Brevo gratuit** (300 e-mails par jour, éditeur français, données dans l'UE) | Infomaniak Newsletter (Suisse) | Listes, désinscription intégrée, séquences d'aimants. |
| SMS | **ASPSMS** (Suisse) : CHF 0,06 à 0,09 par crédit, 1 crédit par SMS vers Swisscom ou Sunrise, 1,75 vers Salt ([ASPSMS](https://www.aspsms.com/en/)) | Twilio (≈ 0,077 USD par SMS, [Twilio](https://www.twilio.com/fr-fr/sms/pricing/ch)) | Prestataire suisse, API JSON, pas d'abonnement. WhatsApp vers les associés : **non retenu** au départ (API Meta, vérification d'entreprise, modèles à faire approuver, données chez Meta). Le SMS est universel. |
| Courrier B2B et aimants imprimés | **Pingen** (envoi de lettres par API, Suisse ; tarif à confirmer) | Impression maison + timbre (affranchissement B : CHF 1,00, [La Poste](https://www.post.ch/fr/expedier-des-lettres/lettres-suisse)) | Automatise la touche 1 de la séquence (j) et l'envoi postal des guides. |
| Statistiques | **Umami auto-hébergé** sur le même VPS (licence MIT, sans cookie) | Plausible Cloud (UE, sans cookie, dès 9 USD par mois, [Plausible](https://plausible.io/)) | §6.3 |
| Génération de PDF (courriers) | **Gotenberg** (conteneur sur le VPS) | Modèle Word imprimé à la main | Fusion HTML vers PDF pour les lettres personnalisées. |

**Si le client utilise déjà bexio, Abacus ou un logiciel métier** pour ses offres et ses factures, l'ingénieur vérifie son API. Le passage d'une offre au statut « envoyée » ou « acceptée » peut alors déclencher (c) et (k) directement, sans double saisie. *À demander au client.*

### 5.4 Points d'entrée PHP (spécification pour l'ingénieur)

**`POST /api/demande.php`** (formulaire de contact, en `multipart/form-data`) :

- **Champs** : `nom`, `telephone`, `email`, `commune`, `travaux`, `type_client`, `surface`, `delai`, `connu_par`, `message`, `rappel`, `accord` (requis), `recommande_par`, `fichier[]` (JPG, PNG ou PDF ; 3 fichiers et 10 Mo au plus au total), champs cachés `site_web` (piège à robots, doit rester vide), `form_t0` (horodatage signé ; refus si l'envoi arrive moins de 3 secondes après), `src_*` (UTM, référent, page d'entrée), `consent_ads` (état du bandeau, si présent).
- **Contrôles** :
  - au moins un moyen de contact (téléphone ou e-mail) ;
  - limite de 5 envois par heure et par IP (IP hachée avec sel, conservée 24 h) ;
  - type réel des fichiers vérifié (MIME), noms de fichiers aléatoires, stockage hors racine web ;
  - réponse JSON `{ok, ref:"AC-2027-0042"}`.
- **Actions, dans l'ordre** :
  1. e-mail aux associés (SMTP) avec les pièces jointes ;
  2. webhook vers n8n (`X-AC-Signature: sha256=…`, `X-AC-Timestamp`, délai d'attente de 5 s) ;
  3. si le webhook échoue : écriture dans `/prive/file-attente/*.json`, puis **accusé de réception générique** au prospect envoyé par le PHP.
- **`/api/fichier.php?id=…&exp=…&sig=…`** : téléchargement signé, valable 24 h, utilisé par n8n pour joindre les fichiers à l'affaire dans le CRM.
- **`/api/cron-relais.php`** : tâche planifiée de l'hébergeur toutes les 10 minutes, qui relance la file d'attente ; purge des fichiers de plus de 30 jours.

**`POST /api/aimant.php`** : `prenom`, `email` ou `adresse_postale`, `profil`, `aimant`, `newsletter` (non cochée par défaut), `par_poste`, plus le même anti-spam. Webhook vers WF07.

**Saisie express d'un appel reçu (canal téléphone) :** page privée `/interne/saisie.html`, protégée par mot de passe HTTP, en 30 secondes sur mobile. Champs : nom, téléphone, commune, service, type de client, surface, délai, « Comment nous avez-vous connus ? », note. Elle poste sur `demande.php` avec `canal=telephone` : même scoring, même CRM, même suivi. Une case « Envoyer une confirmation écrite au client » déclenche l'accusé de réception.

### 5.5 Modèle de données du CRM (Pipedrive)

**Pipelines :**

| Pipeline | Étapes |
|---|---|
| Demandes et offres | 1 Nouvelle demande → 2 Contact établi → 3 Visite planifiée → 4 Offre envoyée → 5 Relance / négociation → Gagnée / Perdue |
| Chantiers | Planifié → En cours → Terminé (réception) → Avis demandé → Clos |
| Prospection B2B | À contacter → Courrier envoyé → Appel à faire → Intéressé (plaquette envoyée) → Relance J+30 → Client potentiel / Pas maintenant / Ne plus contacter |
| Marchés publics | Repéré → Étudié → Dossier en cours → Déposé → Gagné / Perdu |

Si le forfait limite le nombre de pipelines, on utilise des étiquettes. *À vérifier.*

**Champs personnalisés :**

| Objet | Champs |
|---|---|
| Affaire | `ref_demande`, `canal` (site, téléphone, e-mail, B2B, AO, recommandation), `source` (normalisée), `source_detail` (utm, campagne, terme), `connu_par` (déclaratif), `type_client`, `service`, `surface`, `delai`, `commune`, `zone` (1, 2, 3), `score`, `priorite` (A, B, C, hors cible), `sla_echeance`, `date_premier_contact`, `tentatives_appel`, `date_visite`, `montant_offre`, `date_offre`, `relance_offre_etape` (0 à 3), `a_repondu` (oui ou non), `motif_perte` (prix, délai, reporté, attribué ailleurs, sans réponse, hors cible), `recontact_autorise` (oui ou non, avec date), `date_reception_chantier`, `reserves_levees`, `avis_demande_le`, `avis_relance_le`, `avis_recu`, `garantie_sia118` (oui ou non), `entretien_envoye_le`, `ne_pas_relancer` |
| Personne | `consentement_newsletter` (date, canal, preuve), `opposition_marketing` (date), `dernier_message_marketing`, `info_exception_client` (date à laquelle le client a été informé de son droit d'opposition), `astérisque_verifie` (B2B) |
| Organisation | `type` (régie, architecte, commune, EG, partenaire, PME), `palier` (1 à 3), `source_liste` |

**Webhooks Pipedrive vers n8n (WF06)** : `deal.updated` et `deal.added`. Quand une affaire change d'étape, WF06 remplit les dates : passage à « Offre envoyée » → `date_offre` ; passage à « Terminé » → `date_reception_chantier`.

### 5.6 Liste des workflows n8n

| ID | Nom | Déclencheur | Scénarios |
|---|---|---|---|
| WF01 | Réception d'une demande | Webhook depuis `demande.php` | (a) |
| WF02 | Actions en un clic | Webhook GET `/action?t=…` (jeton HMAC, validité de 7 jours, à usage unique pour les actions irréversibles) | (a) (b) (c) (d) (j) |
| WF03 | Horloge | Planifié toutes les 15 min, lu-ve de 7 h à 19 h | (b) (c) (d) |
| WF04 | Quotidien | Planifié tous les jours à 7 h 30 | (e) (i), purge, avis |
| WF05 | Récapitulatif hebdomadaire des associés | Lundi à 7 h | §5.9 |
| WF06 | Synchronisation du CRM | Webhooks Pipedrive | Dates et statuts |
| WF07 | Aimants | Webhook depuis `aimant.php` | (f) |
| WF08 | Veille simap | Lundi à 6 h 30, plus le 1er du mois (adjudications) | (g) |
| WF09 | Rapport mensuel | 1er jour ouvrable du mois à 7 h | (h) |
| WF10 | Prospection B2B | Lundi à 7 h 30, plus les liens de résultat d'appel | (j) |
| WF11 | Avis Google | Quotidien à 8 h (API de la fiche Google si l'accès est accordé, sinon bouton « avis reçu ») | (d) |
| WF12 | Désinscription et opposition | Webhook `/stop?t=…` + mot « STOP » détecté dans les réponses (IMAP) | Tous |
| WF13 | Gestion des erreurs | Déclencheur d'erreur n8n | Supervision |
| WF14 | Détection des réponses | Lecture IMAP des boîtes des associés toutes les 15 min (en-tête et expéditeur seulement, sans stocker le corps) | Arrêt de (c), (e), (f) |
| WF15 | Fiche projet | Passage d'un chantier à « Terminé » | (k), optionnel |

### 5.7 Scénarios détaillés

Variables de modèle : `{{prenom}}`, `{{nom}}`, `{{civilite}}`, `{{service}}`, `{{commune}}`, `{{ref}}`, `{{associe}}` (prénom et nom de l'associé responsable), `{{tel_fixe}}` = 022 771 20 15.

**Signature type** : `{{associe}} · Andy Construct · Route des Acacias 48, 1227 Carouge · 022 771 20 15 · www.andyconstruct.ch`.

**Pied de page de tout message non strictement transactionnel** : « Vous ne souhaitez plus recevoir de message de notre part ? Répondez STOP ou cliquez ici. »

#### (a) Nouvelle demande

| | |
|---|---|
| **Déclencheur** | Webhook WF01 (formulaire du site ou saisie express) |
| **Conditions** | Signature HMAC valide ; pas de spam ; dédoublonnage (même e-mail ou même téléphone dans les 30 derniers jours → note ajoutée à l'affaire existante, sans nouveau SMS) |
| **Actions** | 1. Normalisation (téléphone au format E.164, commune → NPA → zone). 2. Normalisation de la source (§6.2). 3. **Score et priorité** (§2). 4. Création ou mise à jour de la personne, de l'organisation et de l'affaire (étape 1), fichiers joints via `fichier.php`. 5. Attribution d'un associé (règle : B2B → associé « bureau » ; particulier → associé « terrain » ; à ajuster), `sla_echeance` calculée en heures ouvrables. 6. **Notification interne** selon la priorité (§2.4). 7. **Accusé de réception** au prospect en moins d'une minute. 8. Hors cible : e-mail à l'associé avec le bouton « Envoyer la réponse de réorientation ». |
| **Délais** | Immédiat. Entre 20 h et 7 h, les SMS attendent 7 h ; le samedi, uniquement pour les A ; le dimanche, rien. |
| **Responsable** | L'associé attribué rappelle dans le délai prévu |

**SMS interne (A et B)**, 2 SMS au plus :
> Andy · Demande {{priorite}} · {{civilite}} {{nom}}, {{commune}} · {{service}}, {{surface}}, {{delai}} · Tél. {{telephone}} · À rappeler avant {{sla_echeance_hhmm}} · {{lien_court}}

Le lien ouvre une page avec le résumé et trois boutons : « J'ai eu la personne » → étape 2 · « Pas de réponse » · « Hors cible ».

**E-mail interne :**
> **Objet :** [{{priorite}}] Nouvelle demande · {{service}} · {{commune}} · {{nom}}
> Résumé des champs, message, pièces jointes, score détaillé, source. Boutons : Appeler · J'ai eu la personne · Pas de réponse · Hors cible · Ouvrir dans Pipedrive.

**Accusé de réception au prospect (e-mail) :**
> **Objet :** Votre demande à Andy Construct (réf. {{ref}})
> Bonjour {{civilite}} {{nom}},
> Nous avons bien reçu votre demande concernant {{service}} à {{commune}}. {{associe}} vous appelle {{promesse_delai}} pour en parler et, si nécessaire, convenir d'une visite.
> Vous préférez nous appeler ? {{tel_fixe}}, du lundi au vendredi de 7 h à 18 h.
> Vos données servent uniquement à traiter votre demande ([confidentialité](https://www.andyconstruct.ch/mentions-legales.html#confidentialite)).
> Meilleures salutations, {{signature}}

`{{promesse_delai}}` vaut « dans les deux heures (heures de bureau) » pour A, « aujourd'hui ou demain matin » pour B, « d'ici deux jours ouvrables » pour C. Hors heures ouvrables : « lundi matin », « demain matin », etc. **La promesse doit être tenable : elle est réglée sur les délais de rappel cibles.**

**Accusé de réception par SMS** (uniquement sans e-mail, avec un numéro mobile) :
> Andy Construct : votre demande (réf. {{ref}}) est bien reçue. {{associe}} vous rappelle {{promesse_delai}}. Tél. 022 771 20 15

#### (b) Pas de rappel dans le délai

| | |
|---|---|
| **Déclencheur** | WF03 (horloge toutes les 15 min) : affaire à l'étape 1 et `now ≥ sla_echeance` |
| **Conditions** | Aucun contact établi ; pas de clic « Pas de réponse » dans le délai |
| **Actions et délais** | **T0 = échéance** : SMS à l'associé attribué. **T0 + 1 h ouvrable (A) ou + 4 h (B)** : SMS et e-mail à **l'autre associé** (escalade). **T0 + 1 jour ouvrable** : la demande apparaît en rouge dans le récapitulatif du jour, et une tâche « Rappeler » est créée dans le CRM. |
| **Branche « Pas de réponse »** (bouton cliqué par l'associé) | Incrément de `tentatives_appel`. Au 1er essai : SMS et e-mail au prospect (ci-dessous) + tâche « Rappeler » le lendemain à 10 h. Au 3e essai sur 5 jours ouvrables : e-mail de clôture courtoise, puis statut « Sans réponse » (perdue, motif « sans réponse », **sans** relance à 6 mois). |
| **Responsable** | Associé attribué, puis l'autre associé |

**SMS interne de rappel :**
> Rappel · {{nom}} ({{priorite}}, {{commune}}) attend votre appel depuis {{duree}}. Tél. {{telephone}} · {{lien_court}}

**SMS ou e-mail au prospect après un appel sans réponse :**
> **Objet :** Nous avons essayé de vous joindre
> Bonjour {{civilite}} {{nom}}, {{associe}} a essayé de vous appeler aujourd'hui à {{heure}} au sujet de votre demande ({{service}}). Quand pouvons-nous vous rappeler ? Répondez simplement à ce message, ou appelez le 022 771 20 15.

**Clôture après 3 essais :**
> **Objet :** Votre demande {{ref}}
> Nous n'avons pas réussi à vous joindre. Votre demande reste enregistrée : il suffit de nous appeler ou de répondre à ce message pour reprendre contact. Nous ne vous relancerons pas davantage.

#### (c) Suivi d'une offre envoyée : J+3, J+10, J+21

| | |
|---|---|
| **Déclencheur** | WF06 : passage à l'étape 4 « Offre envoyée » (`date_offre` remplie, `montant_offre` saisi). Puis WF03 lit chaque jour `date_offre` et `relance_offre_etape`. |
| **Conditions** | Pipeline « Demandes et offres » uniquement (**jamais pour les marchés publics**). Arrêt immédiat si : `a_repondu` (réponse détectée par WF14), changement d'étape, `ne_pas_relancer`, offre gagnée ou perdue. Envois en semaine à 9 h 15. |
| **Actions et délais** | **J+3** : e-mail « bien reçue ? ». **J+10** : pour le B2B et les A, **tâche « Appeler »** (pas d'e-mail) ; pour les autres, e-mail « des questions ? ». **J+21** : e-mail « où en êtes-vous ? » avec 3 liens de réponse en un clic. **J+35** sans réponse : l'associé reçoit « Clore cette offre ? » (boutons). **J+45** : clôture automatique, motif « sans réponse ». |
| **Responsable** | L'associé qui a envoyé l'offre |

**J+3 :**
> **Objet :** Votre offre pour {{service}} : bien reçue ?
> Bonjour {{civilite}} {{nom}}, je vous ai transmis le {{date_offre}} notre offre n° {{num_offre}}. L'avez-vous bien reçue ? Si un point n'est pas clair (variantes, délais, organisation du chantier), je vous l'explique volontiers par téléphone. {{signature}}

**J+10 :**
> **Objet :** Des questions sur notre offre ?
> Bonjour {{civilite}} {{nom}}, il est normal de comparer plusieurs offres. Pour faciliter la comparaison, la nôtre comprend la protection des lieux, le nettoyage et la réception du chantier avec vous [à valider]. Je peux aussi repasser sur place pour revoir un détail. {{signature}}

**J+21 :**
> **Objet :** Votre projet de {{service}} : où en êtes-vous ?
> Bonjour {{civilite}} {{nom}}, où en est votre réflexion ? Un simple clic nous aide à nous organiser :
> → [Je souhaite en parler] → [Le projet est reporté, recontactez-moi plus tard] → [J'ai choisi une autre solution]
> Merci d'avance. {{signature}}

Les liens écrivent `motif_perte` et `recontact_autorise` dans le CRM, ce qui donne une **analyse des pertes sans effort**. La mention d'une place dans le planning n'est autorisée que si elle est **réelle** : pas de fausse urgence (programme v2, §4).

#### (d) Fin de chantier : demande d'avis à J+2, relance à J+9

| | |
|---|---|
| **Déclencheur** | WF06 : chantier passé à « Terminé » **et** `reserves_levees = oui` (sinon, attente de la levée) |
| **Conditions** | Contact disponible. Pas de litige déclaré (`litige = oui` suspend la demande jusqu'à sa résolution : c'est un décalage, pas un filtre selon la satisfaction). Une seule demande par chantier. |
| **Actions et délais** | **J+2** à 10 h, un jour de semaine : particuliers → SMS + e-mail ; B2B → e-mail au contact nommé. **J+9**, si `avis_recu` n'est pas coché : relance unique. **J+14** : e-mail « Pouvons-nous montrer votre chantier ? » (accord pour les photos et un témoignage, formulaire à choix : photos sans nom / avec la commune / témoignage). WF11 : à chaque nouvel avis détecté, `avis_recu = oui`, notification aux associés avec un **brouillon de réponse**, à publier sous 48 h. |
| **Responsable** | L'associé qui a dirigé le chantier (il signe), l'agence pour les brouillons de réponse |

**SMS (J+2) :**
> Bonjour {{civilite}} {{nom}}, merci d'avoir confié votre chantier à Andy Construct. Votre avis aide d'autres personnes à choisir : {{lien_avis_google}} (1 minute). {{prenom_associe}}

**E-mail (J+2) :**
> **Objet :** Merci, et votre avis sur notre travail
> Bonjour {{civilite}} {{nom}}, le chantier de {{commune}} est terminé : merci pour votre confiance. Que vous soyez satisfait(e) ou que quelque chose aurait pu être mieux, votre avis public nous est utile et aide d'autres propriétaires à choisir. Il suffit de cliquer ici : {{lien_avis_google}}. Si vous le souhaitez, mentionnez le type de travaux et la commune. {{signature}}

**Relance (J+9) :**
> **Objet :** Petit rappel, si vous avez une minute
> Bonjour {{civilite}} {{nom}}, si vous avez déjà laissé votre avis, merci, et ignorez ce message. Sinon, voici le lien : {{lien_avis_google}}. Nous ne vous relancerons plus. {{signature}}

**Brouillon de réponse à un avis positif :**
> Merci {{prenom_auteur}} pour votre retour sur {{service}} à {{commune}}. C'était un plaisir de travailler chez vous. – {{prenom_associe}}, Andy Construct

#### (e) Relance des offres perdues à 6 mois

| | |
|---|---|
| **Déclencheur** | WF04 (tous les jours) : affaires perdues depuis 182 jours |
| **Conditions** | `recontact_autorise = oui` (donné par le lien de J+21 ou noté par l'associé après un appel) **et** `motif_perte` ∈ {reporté, prix, délai}. Pas d'`opposition_marketing`. Pas de marché public. Plafond de pression respecté. **Aucune relance pour les motifs « sans réponse » ou « hors cible ».** |
| **Actions** | Particuliers : e-mail unique. B2B : **tâche « Appeler »** (5 min). Si la personne répond « intéressé » : nouvelle affaire liée, priorité recalculée. |
| **Responsable** | Associé d'origine |

> **Objet :** Votre projet de {{service}} à {{commune}}
> Bonjour {{civilite}} {{nom}}, il y a six mois, vous nous aviez consultés pour {{service}} et souhaitiez être recontacté(e) plus tard. Le projet est-il toujours d'actualité ? Nous pouvons mettre à jour notre offre ou proposer une réalisation par étapes. Une simple réponse suffit ; sans nouvelle de votre part, nous ne vous écrirons plus à ce sujet. {{signature}}

#### (f) Téléchargement d'un aimant : séquence de 3 e-mails

| | |
|---|---|
| **Déclencheur** | WF07 : webhook depuis `aimant.php` |
| **Conditions** | Adresse e-mail valide (sinon, envoi postal seulement). Pas d'opposition. Sortie de la séquence dès qu'une demande est créée ou en cas de désinscription. |
| **Actions** | 1. Contact ajouté à la liste Brevo de l'aimant, avec l'attribut `profil` ; personne créée dans le CRM (étiquette « aimant », **sans affaire**). 2. Si `par_poste` : lettre et guide imprimés via Pingen. 3. Séquence Brevo E1 → E2 → E3. 4. Si `newsletter` est cochée : e-mail de confirmation (double opt-in), puis liste « Lettre trimestrielle ». 5. **Profil régie, architecte ou commune** : tâche CRM « Appel de courtoisie » à J+2 pour l'associé « bureau ». C'est une information demandée ; on vérifie l'astérisque avant d'appeler. |
| **Délais** | E1 immédiat, E2 à J+3, E3 à J+8 (9 h 30, en semaine) |
| **Responsable** | Automatique ; associé « bureau » pour l'appel B2B |

**Exemple : guide « bruit » (propriétaires) :**
> **E1 · Objet :** Votre guide : réduire le bruit dans un appartement
> Bonjour {{prenom}}, voici votre guide (PDF, 8 pages) : {{lien}}. Il se lit en 10 minutes. Si vous préférez une version imprimée, répondez à ce message avec votre adresse. Andy Construct
>
> **E2 · Objet :** Bruit : absorber ou isoler, ce qui change tout
> Bonjour {{prenom}}, la moitié des déceptions vient d'une confusion : un panneau absorbant réduit l'écho dans la pièce, il n'arrête pas le bruit du voisin. Voici comment nous avons traité un cas réel à {{commune_exemple}} : {{lien_fiche_projet}}.
>
> **E3 · Objet :** Un avis sur votre situation ?
> Bonjour {{prenom}}, chaque logement est différent : le bon remède dépend du type de bruit et de la construction. Nous pouvons passer voir la pièce concernée et vous remettre une offre écrite [conditions à valider]. Il suffit de répondre à ce message ou d'appeler le 022 771 20 15. {{signature}}

**Variantes :**
- check-list « régie » : E2 = fiche projet en immeuble habité ; E3 = « Vos fins de bail de {{trimestre}} : voulez-vous que nous chiffrions un forfait type ? » ;
- guide « architectes » : E2 = fiche technique d'une désolidarisation ; E3 = « Un descriptif à faire relire ? ».

#### (g) Veille simap hebdomadaire

| | |
|---|---|
| **Déclencheur** | WF08, le lundi à 6 h 30 |
| **Conditions** | Publications des 7 derniers jours (appels d'offres et préavis) : cantons GE, VD, NE, FR, VS, JU, BE ; codes CPV et CFC du §3.8 ou mots-clés ; dédoublonnage par identifiant de projet ; délai de dépôt d'au moins 10 jours |
| **Actions** | 1. Appel à l'API simap (`/publications/v2/project/project-search`, avec `lang=fr` obligatoire), puis lecture du détail de chaque avis. 2. Score de pertinence : correspondance des CFC, distance (zone), type de procédure, délai, visite obligatoire. 3. **Récapitulatif par e-mail à 7 h**. 4. Bouton **« Étudier »** → affaire dans le pipeline « Marchés publics », avec tâches datées : téléchargement du dossier (J0), date limite des questions, visite, chiffrage, dépôt (rappel à J−2). Bouton **« Ignorer »** → ignoré, motif noté. 5. **Le 1er du mois** : liste des adjudications CFC 271/283/285 en Suisse romande (entreprise retenue, adjudicateur, architecte quand il est cité), versée dans la liste de prospection et dans la veille concurrentielle. |
| **Responsable** | Les deux associés décident ensemble (5 minutes le lundi) |

> **Objet :** Veille marchés publics · semaine {{n}} : {{k}} avis à regarder
> Pour chaque avis : titre · adjudicateur · canton et commune · CFC et CPV · procédure · délai de dépôt · visite obligatoire (oui ou non) · lien simap · pertinence ★★★. Boutons : [Étudier] [Ignorer]

#### (h) Rapport mensuel automatique

| | |
|---|---|
| **Déclencheur** | WF09, le 1er jour ouvrable du mois à 7 h |
| **Sources** | CRM (Pipedrive API), Umami API, Google Search Console API, Google Places API (nombre d'avis et note), Google Ads (rapport programmé reçu par e-mail en CSV et lu par n8n, ou API Google Ads si l'accès développeur est obtenu), dépenses Meta et LinkedIn (saisie manuelle en une ligne par l'agence, ou export) |
| **Actions** | Calcul des indicateurs (§6.5), comparaison avec M−1 et avec l'objectif, graphique simple (HTML), e-mail aux associés et à l'agence, ajout d'une ligne dans l'historique (feuille « KPI » du VPS ou tableau du CRM). **L'agence ajoute 3 lignes de commentaire sous 48 h.** |
| **Responsable** | Agence (commentaire) ; associés (lecture : 15 min) |

> **Objet :** Andy Construct · tableau de bord de {{mois}}
> En tête, 5 chiffres : demandes (dont A et B), offres envoyées, chantiers signés et montant, avis (+n, note), coût par demande. Puis le détail par source, le délai de rappel, l'entonnoir, les appels d'offres, la prospection B2B, et 3 actions pour le mois suivant.

#### (i) Anniversaire de chantier et entretien à 2 ans (peinture)

| | |
|---|---|
| **Déclencheur** | WF04 (tous les jours) |
| **Conditions** | **Peinture** : `date_reception_chantier` + 23 mois. Si le contrat est soumis à la norme SIA 118, on se place avant la fin du délai de garantie de 2 ans *(à confirmer contrat par contrat)*. **Autres services** : 12 mois, message « un an déjà » avec une demande de recommandation (une seule fois). **Régies** : envoi annuel en octobre, « Planification des rafraîchissements de {{annee+1}} ». Le client doit avoir été **informé de son droit d'opposition** (`info_exception_client` rempli, voir §9.2). Plafond de pression respecté. |
| **Actions** | E-mail (et SMS pour les particuliers qui l'ont accepté). Clic « Je souhaite un passage » → nouvelle affaire, priorité B, tâche pour l'associé. |
| **Responsable** | Associé « terrain » |

> **Objet :** Votre peinture, deux ans après
> Bonjour {{civilite}} {{nom}}, il y a bientôt deux ans, nous avons refait {{pieces_ou_service}} à {{commune}}. Si vous le souhaitez, nous passons contrôler l'état des surfaces et faire les retouches éventuelles [conditions à définir avec le client]. C'est aussi l'occasion de rafraîchir d'autres pièces. → [Je souhaite un passage] {{signature}}

> **Objet (régies) :** Vos rafraîchissements de {{annee+1}}
> Bonjour {{civilite}} {{nom}}, vous préparez peut-être votre budget d'entretien. Nous pouvons chiffrer vos rafraîchissements types de fin de bail (prix par pièce) et vos cages d'escalier, pour que vos ordres partent plus vite. → [En parler] {{signature}}

#### (j) Prospection B2B : séquence en 4 touches

| | |
|---|---|
| **Déclencheur** | WF10, le lundi à 7 h 30 : 5 comptes à l'étape « À contacter », pris par palier puis par ordre de priorité |
| **Conditions** | Contact nommé, adresse postale, `astérisque_verifie = non` (aucun astérisque dans l'annuaire, sinon : courrier seulement), pas de « Ne plus contacter », pas de procédure de marché public en cours avec cet adjudicateur |
| **Touche 1 · J0, courrier** | Gotenberg produit une lettre personnalisée (segment : régie, architecte ou commune), Pingen l'envoie avec la plaquette imprimée, ou bien une série PDF est envoyée par e-mail à l'associé pour impression. Étape « Courrier envoyé ». |
| **Touche 2 · J+6, appel** | Tâche CRM et SMS le lundi suivant : « 5 appels à faire », avec un lien vers la fiche et le script. Numéro affiché et inscrit dans l'annuaire (LCD, let. v). L'associé clique le résultat : [Intéressé, envoyer le PDF] [Rappeler le …] [Pas maintenant (12 mois)] [Ne plus contacter]. Pas joint : nouvel essai à J+12, puis bascule vers la touche 4. |
| **Touche 3 · J+6 à J+8, e-mail sur demande** | **Uniquement après « Intéressé, envoyer le PDF »** : e-mail **individuel** depuis la boîte de l'associé, avec la plaquette, 2 fiches projets choisies selon le segment, et une **demande d'accord** pour la lettre trimestrielle (lien de double confirmation). L'accord donné au téléphone est enregistré (date, canal, associé). |
| **Touche 4 · J+30, relance utile** | Intéressé : tâche « Appeler ou proposer une visite de chantier en cours ». Non joint : **2e courrier** avec une fiche projet récente (J+45). Puis lettre trimestrielle (si accord) et nouveau cycle à 12 mois pour « Pas maintenant ». |
| **Responsable** | Associé « bureau » (appels) ; agence (liste, lettres, sélection des fiches) |

**Touche 1, courrier (régie) :**
> **Objet :** Plâtrerie, peinture et isolation acoustique pour vos immeubles
> Madame, Monsieur, Andy Construct est une entreprise de Carouge, inscrite au registre du commerce depuis 2007 [à confirmer]. Elle est spécialisée en placo, peinture intérieure, isolation acoustique et cloisons isothermes. Nous travaillons notamment pour [références publiques validées], voir le dossier joint. Pour vos rafraîchissements de fin de bail et vos travaux en immeuble habité, nous protégeons les lieux, informons les locataires et rendons un chantier propre. Je me permettrai de vous appeler la semaine prochaine pour savoir si nous pouvons figurer parmi les entreprises que vous consultez. {{signature}}

**Touche 2, script d'appel (5 points) :**
1. Rappel du courrier.
2. Question ouverte : « Comment choisissez-vous vos entreprises pour les fins de bail et les cages d'escalier ? » (variante architecte : « Avez-vous des transformations en cours avec des lots de plâtrerie ou d'acoustique ? »).
3. Une preuve adaptée à la réponse (une référence).
4. Proposition : envoi du PDF et de 2 fiches, ou visite d'un chantier en cours.
5. Accord pour la lettre trimestrielle (« Puis-je vous l'envoyer ? »).

**Touche 3, e-mail après l'appel :**
> **Objet :** Suite à notre appel : références Andy Construct
> Bonjour {{civilite}} {{nom}}, merci pour votre accueil au téléphone. Comme convenu, voici notre dossier de références (PDF) et deux exemples proches de vos besoins : {{fiche_1}}, {{fiche_2}}. Nos attestations (AVS, LPP, CCT, RC) sont disponibles sur simple demande [à préparer]. Pour recevoir notre lettre trimestrielle (un chantier, un point technique, 4 fois par an), confirmez ici : {{lien_double_optin}}. {{signature}}

**Touche 4 :**
> **Objet :** Un chantier en cours à {{commune}}, si vous voulez voir
> Bonjour {{civilite}} {{nom}}, nous réalisons en ce moment {{description_courte}} à {{commune}}. Si cela vous intéresse, je vous le fais visiter (20 minutes). {{signature}}

#### (k) Optionnel : chantier signé, puis fiche projet et publications

1. Affaire gagnée (WF06) : déplacement vers le pipeline « Chantiers » ; e-mail de confirmation au client, avec la mention d'information sur l'opposition (§9.2) ; tâche « photos avant ».
2. Chantier terminé (WF15) : l'associé reçoit un **lien d'envoi de photos** (3 à 6) et 3 questions (lieu, besoin, solution).
3. L'agence rédige la fiche projet (environ 30 min). Après validation, le générateur `tools/build/` la publie.
4. n8n prépare les brouillons : post sur la fiche Google, publication Facebook et LinkedIn, mise à jour du `llms.txt`. Les associés valident en un clic.

### 5.8 Notifications et récapitulatifs internes

**Récapitulatif hebdomadaire (WF05, lundi 7 h) :**

> **Objet :** Votre semaine Andy Construct
> 1. Demandes ouvertes, de la plus ancienne à la plus récente, avec leur priorité.
> 2. Offres à relancer cette semaine (appels J+10 et J+21).
> 3. Les 5 appels B2B de la semaine (liens).
> 4. Avis à répondre (brouillons prêts).
> 5. Veille simap (lien vers le récapitulatif).
> 6. Photos de chantier attendues.

**Récapitulatif du jour (17 h 30) :** demandes C et hors cible du jour ; demandes en retard sur leur délai.

### 5.9 Ce qui reste manuel, et la routine de 2 h par semaine

**Reste manuel, par nature :**
- rappeler, qualifier et visiter ;
- rédiger et chiffrer les offres ;
- conduire le chantier et le réceptionner ;
- choisir « on y va » ou « on laisse » pour un appel d'offres, et monter le dossier ;
- les appels B2B ;
- relire et publier les réponses aux avis ;
- valider les posts et les fiches projets ;
- prendre les photos ;
- vérifier l'astérisque dans l'annuaire lors de la constitution de la liste (agence) ;
- les accords de citation des références (marques privées).

**Routine des associés (le travail commercial de rappel, de visite et de chiffrage n'est pas compté ici) :**

| Quand | Durée | Tâche |
|---|---|---|
| Lundi à 7 h 30 | 30 min | Récapitulatif hebdomadaire : demandes ouvertes, relances d'offres, décision simap |
| Lundi ou mardi | 30 min | 5 appels B2B (résultat en un clic) |
| Au fil de la semaine | 20 min | Photos de chantier (lien d'envoi) et validation de 1 ou 2 publications préparées |
| Au fil de la semaine | 15 min | Réponses aux avis (brouillons) et clics « avis reçu » / « réserves levées » |
| Au fil de la semaine | 15 min | Saisie express des appels reçus (30 s chacun) et mise à jour des étapes (offre envoyée, gagné, perdu) |
| 1er lundi du mois | 10 min | Lecture du rapport mensuel |
| **Total** | **≈ 2 h** | |

### 5.10 Sécurité, supervision, sauvegardes et tests

- **Secrets** : stockés dans les identifiants n8n et dans un fichier `.env` sur le VPS, **jamais dans le dépôt** (le `.gitignore` exclut déjà `.env`). Webhooks signés par HMAC, avec contrôle de l'horodatage (plus ou moins 5 minutes) contre le rejeu.
- **Accès** : interface n8n derrière HTTPS et authentification. Accès SSH par clé, sans connexion root par mot de passe. Pare-feu limité aux ports 443 et 22.
- **Supervision** : WF13 (erreurs) envoie un SMS à l'agence et un e-mail. Healthchecks.io (gratuit) reçoit un « ping » de l'horloge toutes les 15 minutes ; en l'absence de ping pendant 30 minutes, l'agence est alertée. La file d'attente du PHP est surveillée.
- **Sauvegardes** : instantané quotidien du VPS (7 jours) ; export JSON des workflows versionné dans `automation/workflows/` (sans identifiants) ; export hebdomadaire du CRM au format CSV, chiffré, conservé 4 semaines.
- **Journaux** : exécutions n8n conservées 30 jours, données personnelles masquées dans les journaux d'erreur.
- **Tests** : environnement de test séparé (webhook de test, Pipedrive sandbox ou étiquette « TEST », SMS remplacés par des e-mails). Recette de **20 cas** avant mise en production :
  - un cas par priorité ;
  - un doublon ;
  - un hors cible ;
  - n8n arrêté (file d'attente) ;
  - un fichier de 12 Mo ;
  - un robot (piège à robots) ;
  - une réponse STOP ;
  - un passage à l'heure d'été ;
  - un jour férié genevois ;
  - etc.
- **Livrables attendus de l'ingénieur (phase 2)** :
  - `site/api/` (PHP) ;
  - `automation/` : `docker-compose.yml`, `workflows/*.json`, `config/scoring.json`, `config/zones.json`, `config/jours-feries.json`, `templates/` (e-mails, SMS, lettres) ;
  - `docs/v2/automatisation.md` : installation, exploitation, plan de reprise.

---

## 6. Tracking et mesure

### 6.1 Plan de marquage (événements)

Implémentation **sans JavaScript supplémentaire** : Umami lit les attributs `data-umami-event` et `data-umami-event-*` posés directement dans le HTML par le générateur `tools/build/` ([Umami](https://umami.is/blog/understanding-custom-events-umami-vs-ga4)). Seuls les événements de formulaire demandent quelques lignes dans `main.js`.

| Événement | Déclencheur | Propriétés | Mise en œuvre | Compte comme |
|---|---|---|---|---|
| `appel_clic` | Clic sur un lien `tel:` | `emplacement` (entête, pied, barre_mobile, contact, fiche_projet, service), `numero` (fixe, mobile), `page` | Attributs HTML | Contact web |
| `email_clic` | Clic sur un lien `mailto:` | `emplacement`, `page` | Attributs HTML | Contact web |
| `whatsapp_clic` | Clic sur un lien `wa.me` (si le bouton est validé) | `emplacement`, `page` | Attributs HTML | Contact web |
| `itineraire_clic` | Clic « Voir sur la carte » | `page` | Attributs HTML | Micro-conversion |
| `formulaire_debut` | Premier champ rempli (une fois par session) | `formulaire` (contact, aimant), `page` | `main.js` | Entonnoir |
| `formulaire_etape` | Passage à l'étape 2 | `etape`, `service`, `type_client` | `main.js` | Entonnoir |
| `formulaire_erreur` | Erreur de validation affichée | `champ` (sans la valeur saisie) | `main.js` | Diagnostic |
| `formulaire_envoye` | **Réponse `ok` du serveur** (pas le simple clic) | `service`, `type_client`, `priorite` non exposée | `main.js` | **Contact web (conversion principale)** |
| `aimant_demande` | Formulaire d'aimant envoyé (réponse `ok`) | `aimant`, `par_poste` | `main.js` | Prospect |
| `plaquette_telechargee` | Clic sur le PDF de la plaquette | `page` | Attributs HTML | Micro-conversion B2B |
| `galerie_filtre` | Clic sur un filtre de la galerie | `filtre` | Attributs HTML | Engagement |
| `recommandation_carte` | Arrivée avec `utm_source=recommandation` | – | Lecture des UTM (automatique) | Source |

Aucune donnée personnelle n'est envoyée dans les propriétés : ni nom, ni e-mail, ni téléphone, ni commune saisie.

**Entonnoir Umami** : vue d'une page service → `formulaire_debut` → `formulaire_etape` → `formulaire_envoye`. Les rapports « Funnel » et « Journey » existent dans Umami ; leur disponibilité dans la version auto-hébergée installée est à vérifier.

**Vérité terrain :** le **CRM** compte les demandes. Umami mesure les comportements. Un `appel_clic` n'est pas un appel abouti : la réconciliation passe par la saisie express, avec `connu_par`.

### 6.2 Conventions UTM et attribution

**Règles :** minuscules, sans accents, mots séparés par des tirets. `utm_campaign` = `aaaa-mm_objet`.

| Contexte | `utm_source` | `utm_medium` | `utm_campaign` (exemple) | `utm_content` |
|---|---|---|---|---|
| Google Ads | google | cpc | `{campaignid}` (correspondance dans le rapport) | `{adgroupid}` |
| Microsoft Ads | bing | cpc | idem | idem |
| Fiche Google, lien du site | google | organic-local | gbp-site | – |
| Fiche Google, lien de rendez-vous | google | organic-local | gbp-rdv | – |
| Fiche Google, posts | google | organic-local | gbp-post-2027-03 | sujet |
| Meta payant | meta | paid-social | 2027-04_guide-bruit | variante de créa |
| Facebook organique | facebook | organic-social | 2027-04_fiche-collonge | – |
| LinkedIn | linkedin | organic-social / paid-social | 2027-09_plaquette | – |
| Lettre trimestrielle | newsletter | email | 2027-q1 | bloc |
| Séquences automatiques | crm | email | relance-offre, aimant-bruit, entretien-2ans | e1, e2, e3 |
| Courrier B2B (code QR) | courrier | print | prospection-regies | lettre-1 |
| Panneau de chantier, véhicule (code QR) | panneau / vehicule | print | chantier-{{commune}} | – |
| Carte de recommandation | recommandation | print | carte | – |
| Annuaires | localch, searchch, gge | referral | annuaire | – |

**Attribution sur le site :**
- un script de quelques lignes lit `utm_*` (et `gclid` **uniquement si `consent_ads` = accordé**) à l'arrivée, ainsi que `document.referrer` ;
- il les garde en `sessionStorage` (`ac_src`) le temps de l'onglet, puis remplit les champs cachés du formulaire ;
- aucun envoi à un tiers ;
- **mention dans la politique de confidentialité** (stockage de session, propre au site, supprimé à la fermeture de l'onglet). Le guide du PFPDT qualifie ce type de traitement à des fins statistiques non personnelles de justifiable par un intérêt prépondérant, avec une information et une possibilité d'opposition (ch. 3.8.2 et 3.9). **À valider par le juriste** ; sans validation, on se contente du champ déclaratif « Comment nous avez-vous connus ? ».

**Normalisation de la source dans n8n**, par ordre de priorité :
1. `utm_source` et `utm_medium` ;
2. `gclid` (google / cpc) ;
3. référent (google.* → organique ; facebook.com → organic-social ; etc.) ;
4. `connu_par` (déclaratif) ;
5. « direct / inconnu ».

Pour un appel, la source est le champ déclaratif de la saisie express.

### 6.3 Outil de statistiques : recommandation

| Critère | **Umami auto-hébergé (recommandé)** | Plausible Cloud | Matomo | GA4 avec consentement |
|---|---|---|---|---|
| Cookies, bandeau | Aucun cookie, pas de bandeau | Aucun cookie, pas de bandeau ([Plausible](https://plausible.io/)) | Mode sans cookie possible | **Bandeau obligatoire** (politique Google en Suisse depuis le 31.07.2024) |
| Hébergement des données | **Suisse** (VPS Infomaniak) | UE | Cloud en Europe ([Matomo](https://matomo.org/pricing/)) ou auto-hébergé | Google (États-Unis, cadre DPF) |
| Poids du script | Léger (quelques Ko) | Très léger | Plus lourd (à mesurer, budget JS < 25 Ko) | Lourd (plusieurs dizaines de Ko) : incompatible avec le budget JS |
| Coût | CHF 0 (VPS déjà payé pour n8n) | Dès 9 USD par mois (10'000 pages vues) | Cloud : 26 USD par mois (50'000 hits) | 0 |
| Événements personnalisés | Oui, par attributs HTML | Oui | Oui | Oui |
| Lien avec Google Ads | Non (attribution par UTM et CRM) | Non | Non | Oui |
| Maintenance | Agence (mises à jour) | Aucune | Moyenne | Aucune |

**Décision :** Umami auto-hébergé. Le site reste **sans bandeau** dans le scénario S. En M et L, un **bandeau maison léger** (moins de 4 Ko, « Refuser » aussi visible qu'« Accepter », aucune case pré-cochée) charge **après consentement uniquement** la balise Google Ads (mode consentement v2), et en L la balise Meta et la LinkedIn Insight Tag. GA4 n'est pas installé.

**Compléments gratuits obligatoires :** Google Search Console et Bing Webmaster Tools (sitemap envoyé en M1).

### 6.4 Suivi des appels

| Option | Avantages | Inconvénients | Décision |
|---|---|---|---|
| Numéros de suivi dynamiques sur le site (un numéro par source) | Attribution fine des appels | **Casse la cohérence du NAP** (Google et les IA recoupent le numéro). Un public senior se méfie d'un numéro inconnu. Coût mensuel. L'enregistrement éventuel des appels exige l'information des interlocuteurs (art. 179bis ss CP). | **Non** |
| Numéros de transfert Google dans l'extension d'appel | Mesure les appels issus des annonces, sans balise et sans cookie ; disponibles en Suisse ([Google](https://support.google.com/google-ads/answer/2454052)) | Ne couvre que les annonces | **Oui** (dès S) |
| Statistiques d'appels de la fiche Google | Gratuit | Agrégé | **Oui** |
| Clics `tel:` (Umami) | Mesure l'intention par page et par emplacement | Un clic n'est pas un appel abouti | **Oui** |
| Question « Comment nous avez-vous connus ? » au rappel + saisie express | Vérité terrain, sans technique | Déclaratif | **Oui, obligatoire** |
| Rappel automatique des appels manqués (SMS « nous vous rappelons ») | Récupère des appels perdus | Demande un opérateur téléphonique avec API (à vérifier selon l'opérateur actuel) | Phase 3, optionnel |

### 6.5 Tableau de bord mensuel (contenu du rapport h)

| Bloc | Indicateurs | Source |
|---|---|---|
| Résultats | Demandes (A, B, C), offres envoyées, chantiers signés (nombre et CHF), taux demande → offre et offre → signée | CRM |
| Réactivité | Délai médian de premier contact par priorité, % dans les délais, demandes en retard | CRM |
| Sources | Demandes et signatures par source ; coût par demande et par chantier signé (canaux payants) | CRM + dépenses publicitaires |
| Site | Visites, contacts web, taux de conversion, top 5 des pages d'entrée, entonnoir du formulaire, erreurs de formulaire par champ | Umami |
| Recherche | Clics et impressions Search Console (30 requêtes cibles), pages indexées | Search Console |
| Google Ads | Dépense, clics, CPC, part d'impressions, appels issus des annonces, conversions, CPL | Google Ads |
| Réputation | Avis (+n, cumul), note, délai de réponse, citations IA (test trimestriel) | Places API, CRM |
| B2B et AO | Comptes contactés, appels aboutis, intéressés, rendez-vous ; avis simap repérés, étudiés, déposés, gagnés | CRM |
| Automatisation | Erreurs, messages envoyés, désinscriptions, file d'attente du PHP | n8n |
| Actions | 3 actions pour le mois suivant (commentaire de l'agence) | Agence |

---

## 7. Pile d'outils

| Outil | Usage | Coût mensuel (CHF, indicatif) | Hébergement des données | Alternative gratuite |
|---|---|---|---|---|
| Hébergement mutualisé (PHP, tâches planifiées) | Site, endpoints, file d'attente | Existant (0 en plus) | Selon l'hébergeur (idéalement en Suisse) | – |
| Messagerie du domaine (2 ou 3 boîtes) | E-mails 1:1, SMTP, lecture IMAP | Souvent incluse ; sinon environ 2 à 6 par boîte *(estimation à valider)* | Selon le fournisseur (idéalement en Suisse) | – |
| VPS Infomaniak (2 vCPU / 4 Go) + sauvegardes | n8n, Umami, Gotenberg, PostgreSQL | ≈ 8 à 10 ([Infomaniak](https://www.infomaniak.com/fr/hebergement/vps-lite)) | **Suisse** | n8n Cloud Starter ≈ 19 (Francfort, [n8n](https://n8n.io/pricing/)) |
| n8n Community | Orchestration | 0 (licence d'usage interne) | Suisse (VPS) | – |
| Pipedrive Lite × 2 | CRM | ≈ 26 (2 × 14 EUR, facturation annuelle, [Zeeg](https://zeeg.me/en/blog/post/pipedrive-pricing)) | UE (Pipedrive OÜ, Estonie ; région à confirmer) | Brevo CRM gratuit (1 utilisateur, 50 affaires) |
| Brevo gratuit | Listes, séquences d'aimants, lettre trimestrielle | 0 (300 e-mails par jour). Formule Starter ≈ 7 si l'on veut retirer le logo Brevo | UE (France) | Infomaniak Newsletter (Suisse) |
| ASPSMS | SMS aux associés et aux clients | ≈ 5 (environ 60 SMS × 0,06 à 0,09, [ASPSMS](https://www.aspsms.com/en/)) | Suisse | Notifications push (ntfy, Telegram), moins universelles |
| Pingen | Courrier B2B et guides imprimés | ≈ 40 à 80 selon le volume (affranchissement à partir de CHF 1,00 + impression, *tarif Pingen à confirmer*) | Suisse | Impression maison + timbre |
| Umami (auto-hébergé) | Statistiques sans cookie | 0 | Suisse (VPS) | Plausible ≈ 7 à 15 (UE) |
| Google Search Console, Bing Webmaster Tools | SEO | 0 | États-Unis (cadre DPF) ; aucune donnée de prospect | – |
| Fiche Google, Bing Places, Apple Business Connect | Visibilité locale | 0 | États-Unis (DPF) | – |
| Google Places API | Compte des avis (rapport) | 0 dans le quota gratuit *(à vérifier)* | États-Unis (DPF) | Saisie manuelle |
| Healthchecks.io | Supervision | 0 | UE | UptimeRobot (gratuit) |
| Bandeau de consentement maison (M et L) | Consentement Google, Meta, LinkedIn | 0 (développé avec le site) | Navigateur | – |
| Google Ads, Microsoft Ads, Meta, LinkedIn | Médias payants | Budgets §8.3 | États-Unis / Irlande (DPF ou clauses contractuelles) | – |
| **Total outils (hors médias et courrier)** | | **≈ 45 à 60 (S, sans Pipedrive : ≈ 20 à 35) · ≈ 60 (M) · ≈ 75 à 90 (L)** | | |

---

## 8. Feuille de route, rôles et budget

### 8.1 Feuille de route sur 12 mois

M0 correspond aux 2 à 4 semaines qui précèdent la mise en ligne. M1 est le mois de mise en ligne (date à fixer avec le chef de projet).

| Mois | Site, SEO, GEO | Automatisation (ingénieur) | Payant | B2B et AO | Avis et réputation | Jalon |
|---|---|---|---|---|---|---|
| **M0** | Décisions d'identité (NAP) ; politique de confidentialité ; étude des mots-clés (Keyword Planner) | Domaine e-mail + SPF, DKIM, DMARC ; comptes Pipedrive, Brevo, ASPSMS, VPS ; contrats de sous-traitance (DPA) | Création des comptes Ads (sans diffusion) | Dossier administratif type (attestations) | Revendication de la fiche Google ; liste des 30 clients pour le 1er lot d'avis | Prérequis prêts |
| **M1** | Mise en ligne v2, redirections 301, Search Console, Bing ; 4 fiches projets | **WF01, WF02, WF03 (b), WF12, WF13**, endpoint PHP, saisie express, Umami | Google Ads C1 + C4 (S : groupes Placo et Acoustique) ; vérification des annonces de services locaux | – | Fiche Google complète ; Bing Places et Apple ; annuaires corrigés ; **1er lot d'avis** | Première demande traitée de bout en bout |
| **M2** | Plaquette (aimant 1) ; 2 fiches projets ; guide n° 1 | **WF06, (c), (d), WF11, WF05** | Revue des termes de recherche ; extension d'appel active | Liste B2B des paliers 1 et 2 (environ 120 comptes) ; **WF08 simap** ; page LinkedIn | 2 posts sur la fiche Google | Les relances d'offres tournent |
| **M3** | Check-list « régie » (aimant 2) ; guide n° 2 | **WF07 (f), WF09 (h), WF10 (j)** | M et L : lancement de C2 et de l'import Microsoft | **Début de la séquence (j)** : 5 comptes par semaine | Objectif : **15 avis** | **Bilan à M3** : objectifs et scoring recalés |
| **M4** | Guide « bruit » (aimant 3) + version imprimée ; guide n° 3 | WF15 (k) ; bandeau de consentement (M et L) | M et L : 1re campagne Meta (printemps) ; conversions Google avec consentement | Partenariats : 3 premiers rendez-vous | – | Premiers aimants téléchargés |
| **M5** | Page canton GE (si au moins 2 fiches) ; guide n° 4 | Ajustements des modèles de message | Bascule vers « Maximiser les conversions » si le seuil est atteint | 5 partenaires | – | – |
| **M6** | Page canton VD ; guide n° 5 ; test GEO | WF04 (e), (i) opérationnels | Bilan Ads (CPL par groupe) | 1re lettre trimestrielle (si les listes le permettent) | Objectif : **30 avis** | **Bilan semestriel** |
| **M7** | Guide architectes (aimant 4) ; guide n° 6 | Recalibrage du scoring (premières signatures) | Baisse des enchères pendant les vacances du bâtiment (été) | Pause des envois de courrier pendant les vacances | – | – |
| **M8** | Fiches projets en retard, photos ; guide n° 7 | Maintenance, mises à jour | Préparation des créas de la rentrée | Liste du palier 3 | Audit des réponses aux avis | – |
| **M9** | Aimant 5 « avant de vendre ou de louer » ; guide n° 8 | – | Meta (rentrée) ; L : LinkedIn, vague 2 | Lettre trimestrielle n° 2 ; message annuel aux régies (i) en octobre | – | – |
| **M10** | Aimant 6 « salle communale » ; 1re ou 2e page ville ; guide n° 9 | – | – | **Communes** : budgets de l'année suivante, contact des services techniques | – | – |
| **M11** | Aimant 7 « bureaux » ; guide n° 10 | – | Modulation de fin d'année | Relances des entreprises générales et des architectes | – | – |
| **M12** | Guide n° 11 ; test GEO ; audit SEO | Revue annuelle des workflows | Bilan annuel des médias | Lettre trimestrielle n° 3 ; bilan des marchés publics | Objectif : **50 avis** | **Bilan annuel et plan de l'année 2** |

### 8.2 Répartition des rôles

| Rôle | Qui | Responsabilités | Temps |
|---|---|---|---|
| Associé « bureau » *(à attribuer)* | Un des deux associés | Rappels B2B et C, appels de prospection (j), décisions simap, lecture du rapport, validation des contenus | ≈ 1 h 15 par semaine de marketing |
| Associé « terrain » *(à attribuer)* | L'autre associé | Rappels des particuliers A et B, visites, photos de chantier, réception et levée des réserves, entretien (i) | ≈ 45 min par semaine de marketing |
| Agence (Harbor Digital) | Chef de projet et équipe | Google Ads et Meta, SEO et contenus (fiches, guides, aimants), lettre trimestrielle, réponses aux avis préparées, liste B2B, rapport commenté, maintenance de n8n, Umami et du VPS | S : 4 h · M : 10 h · L : 20 h par mois |
| Ingénieur automatisation (phase 2) | Agence | Endpoints PHP, workflows n8n, intégrations, recette, documentation | Forfait de mise en place (§8.3) |
| Juriste (ponctuel) | Externe | Relecture de la politique de confidentialité, des mentions d'opposition et des modèles de prospection | ≈ 2 à 4 h, une fois |
| Photographe (optionnel, scénario L) | Externe | 2 séances par an sur des chantiers marquants | 2 demi-journées par an |

### 8.3 Budget global : trois scénarios

**Mise en place (une fois)**, en jours-homme d'agence *(estimation à valider ; à multiplier par le tarif de l'agence)* :

| Poste | Jours |
|---|---|
| Endpoints PHP et anti-spam | 1,5 |
| n8n : WF01 à WF15, configuration, recette | 6 à 8 |
| CRM : pipelines et champs | 1 |
| Tracking et bandeau | 1 |
| Modèles de messages | 1 |
| Plaquette de références (rédaction et mise en page) | 2 à 3 |
| Aimants n° 2 et 3 | 2 |
| **Total** | **≈ 15 à 18 jours** |

Hors frais d'impression de la plaquette (100 exemplaires : *estimation à valider*).

**Budget courant mensuel (CHF, hors TVA) :**

| Poste | S « Fondations » | M « Croissance » | L « Accélération romande » |
|---|---|---|---|
| Google Ads (+ Microsoft) | 400 | 1'200 | 2'500 |
| Meta Ads (moyenne lissée) | 0 | 150 (300 × 6 mois) | 400 (600 × 8 mois) |
| LinkedIn sponsorisé (moyenne lissée) | 0 | 0 | 235 (700 × 4 mois) |
| Outils (§7) | ≈ 35 (Brevo CRM au lieu de Pipedrive) | ≈ 60 | ≈ 90 |
| Courrier B2B, guides imprimés, cartes | 40 | 80 | 150 |
| Impression de la plaquette (lissée) | 15 | 35 | 50 |
| Photographe (lissé) | 0 | 0 | 100 *(estimation)* |
| **Total médias, outils et supports par mois** | **≈ 490** | **≈ 1'525** | **≈ 3'525** |
| **Total sur 12 mois** | **≈ CHF 5'900** | **≈ CHF 18'300** | **≈ CHF 42'300** |
| Heures d'agence par mois (gestion courante) | 4 h | 10 h | 20 h |
| Heures d'agence par an | 48 h | 120 h | 240 h |

**Lecture :**
- **S** convient pour démarrer si le carnet est déjà bien rempli : tout l'organique, les avis, le B2B et l'automatisation, plus un petit Google Ads sur Genève.
- **M** est le scénario de référence des objectifs du §1.
- **L** n'a de sens que si la capacité de production suit (au moins une équipe de plus) et si le coût par chantier signé reste sous le seuil du §1.3.

**Règle de passage :** S vers M dès que le CPL qualifié (A et B) est inférieur au tiers du CPL maximal pendant 2 mois consécutifs ; M vers L dans les mêmes conditions, avec une part d'impressions perdue à cause du budget supérieure à 20 %.

---

## 9. Risques et conformité

### 9.1 Protection des données (nLPD, en vigueur depuis le 1.9.2023)

| Obligation | Application dans ce plan |
|---|---|
| **Devoir d'information** (art. 19 LPD) | Politique de confidentialité sur le site. Elle indique les finalités (traiter la demande, suivi commercial, avis, prospection B2B, statistiques), les destinataires et sous-traitants avec leur pays (tableau ci-dessous), les durées de conservation, les droits, le **scoring** (priorisation des rappels) et le stockage de session pour l'attribution. Le formulaire porte un rappel court avec un lien. |
| **Sous-traitance** (art. 9 LPD) | Contrat de sous-traitance (DPA) signé ou accepté avec : Pipedrive, Brevo, Infomaniak, ASPSMS, Pingen, l'hébergeur du site, et l'agence (qui accède au CRM et à n8n). Registre des sous-traitants tenu par l'agence. |
| **Communication à l'étranger** (art. 16 LPD) | UE : niveau de protection adéquat (annexe 1 de l'OPDo). États-Unis : uniquement vers des entreprises certifiées **Swiss-US DPF**, adéquates depuis le 15.09.2024 ([Conseil fédéral](https://admin.ch/gov/en/start/documentation/media-releases.msg-id-102054.html)) : Google, Meta, Microsoft/LinkedIn. **Les données des prospects ne vont pas aux États-Unis**, sauf `gclid` et conversions en M et L, avec consentement. |
| **Protection des données dès la conception** (art. 7 LPD) | Minimisation : pas de budget demandé, pas de date de naissance. Champs facultatifs. Statistiques sans cookie. Paramètres par défaut protecteurs (rien de publicitaire avant le consentement). |
| **Profilage** (art. 5 let. f LPD) **et décision automatisée** (art. 21 LPD) | Le scoring est un profilage simple (pas « à risque élevé ») qui **ordonne les rappels**. **Toutes les demandes sont rappelées** et un humain décide toujours : ce n'est pas une décision individuelle automatisée. On le mentionne dans la politique de confidentialité. |
| **Sécurité** (art. 8 LPD) | HTTPS, HMAC, accès par clé, sauvegardes chiffrées, masquage des journaux, droits minimaux (l'agence est gestionnaire, pas propriétaire). |
| **Violation de la sécurité des données** (art. 24 LPD) | Procédure écrite : évaluation sous 24 h, annonce au PFPDT « dans les meilleurs délais » en cas de risque élevé, information des personnes si nécessaire. Responsable : l'agence prévient les associés. |
| **Registre des activités de traitement** (art. 12 LPD) | Entreprise de moins de 250 collaborateurs, sans profilage à risque élevé : dispense prévue par l'art. 24 OPDo *(à confirmer par le juriste)*. On tient quand même **une page** (traitements, finalités, durées, sous-traitants), utile en cas de question. |
| **Droits des personnes** (art. 25 ss LPD) | Demande d'accès ou d'effacement par e-mail ; réponse sous 30 jours ; l'export ou la suppression dans le CRM, Brevo et n8n se fait par une procédure documentée. |
| **Durées de conservation** (à valider) | Prospects non convertis : **24 mois** après le dernier contact, puis effacement automatique (WF04, mensuel). Clients : **10 ans** pour les pièces comptables et contractuelles (art. 958f CO) ; données CRM tant que court la responsabilité pour les défauts (jusqu'à 5 ans pour un ouvrage immobilier, art. 371 CO, puis revue). Fichiers envoyés par formulaire : 30 jours sur le serveur web, puis seulement dans le CRM, liés à l'affaire. Journaux : 30 jours. Liste d'opposition : conservée tant que nécessaire pour la respecter (adresse hachée). |
| **Sanctions** | Amendes jusqu'à CHF 250'000 **pour les personnes physiques responsables** en cas de violation intentionnelle de certains devoirs, notamment l'information et la sous-traitance (art. 60 ss LPD). |

**Sous-traitants et localisation :**

| Sous-traitant | Données | Pays |
|---|---|---|
| Hébergeur du site | Formulaires (transit), fichiers (30 j) | À confirmer (idéalement en Suisse) |
| Infomaniak (VPS) | n8n, Umami | Suisse |
| Pipedrive | CRM | UE |
| Brevo | Listes e-mail | UE |
| ASPSMS | Numéros, SMS | Suisse |
| Pingen | Adresses postales | Suisse |
| Google, Meta, LinkedIn | Uniquement avec consentement (balises), statistiques agrégées | États-Unis / Irlande (DPF) |

### 9.2 Prospection par e-mail, SMS et téléphone (LCD, LTC)

**Texte de l'art. 3 al. 1 let. o LCD** ([texte de la loi](https://juriup.ch/lois/lcd/art-3/)) :

> « Agit de façon déloyale celui qui, notamment : […] o. envoie ou fait envoyer, par voie de télécommunication, de la publicité de masse n'ayant aucun lien direct avec une information demandée et omet de requérir préalablement le consentement des clients, de mentionner correctement l'émetteur ou de les informer de leur droit à s'y opposer gratuitement et facilement ; celui qui, lors de la vente de marchandises, d'œuvres ou de prestations, obtient les coordonnées de clients et les informe de leur droit à s'opposer à l'envoi de publicité de masse par voie de télécommunication n'agit pas de façon déloyale s'il leur adresse une telle publicité sans leur consentement, à condition que cette publicité concerne des marchandises, œuvres et prestations propres analogues. »

**Ce qu'il faut en retenir :**

1. **Opt-in par défaut** pour la publicité de masse par e-mail, SMS ou fax ([OFCOM/BAKOM](https://www.bakom.admin.ch/en/when-is-mass-sending-allowed)), avec trois obligations cumulatives : consentement préalable, **expéditeur correctement identifié**, **opposition gratuite et facile**.
2. **Il n'existe pas d'exception B2B en droit suisse.** La règle protège les personnes morales comme les personnes physiques ([WEKA](https://www.weka.ch/themen/datenschutz-und-it-recht/datenschutz-umsetzen/article/datenschutz-newsletter-rechtssicheres-e-mail-marketing-in-der-schweiz/)). Une adresse professionnelle nominative ne change rien.
3. **« De masse »** : la loi ne fixe pas de nombre. La doctrine parle de publicité non adressée à un cercle de destinataires choisis individuellement et envoyée en grand nombre. La pratique de la Commission suisse pour la loyauté retient plutôt le **caractère automatisé et en série** de l'envoi que le volume *(sources secondaires, à confirmer par le juriste)*. **Un e-mail rédigé individuellement pour un contact précis tombe vraisemblablement hors de la règle ; une séquence automatisée, même personnalisée par champs de fusion, vraisemblablement pas.**
4. **Exception « clients »** : elle vaut pour nos **propres prestations analogues**, si le client a été **informé de son droit d'opposition au moment de la collecte**. D'où le champ `info_exception_client` et la phrase à ajouter **dans les offres, les confirmations de commande et l'accusé de réception** :
   > « Nous pourrons vous adresser occasionnellement des informations sur nos prestations. Vous pouvez vous y opposer à tout moment, gratuitement, en répondant STOP. »
   *(Formulation à valider par le juriste.)*
5. **Sanctions** : action civile (art. 9 LCD) et, sur plainte, poursuite pénale (art. 23 LCD). Les fournisseurs de télécommunication peuvent aussi bloquer les expéditeurs (art. 45a LTC).

**Téléphone** ([art. 3 al. 1 let. u, v et w LCD](https://juriup.ch/lois/lcd/art-3/)) :
- respecter l'**astérisque** de l'annuaire (personne ou entreprise qui refuse la publicité) ;
- appeler **avec un numéro affiché et inscrit dans l'annuaire** ;
- ne pas utiliser de données obtenues en violation de ces règles.

**Le courrier postal** adressé n'est pas un envoi « par voie de télécommunication » : il échappe à la let. o. Respecter quand même les demandes d'arrêt.

**Matrice de décision par type de message :**

| Message | Base | Statut |
|---|---|---|
| Accusé de réception, rappels, suivi d'offre (a, b, c) | Lien direct avec l'information demandée | ✅ |
| Demande d'avis (d) | Suite du contrat. Message de service, non publicitaire *(à valider)*. Opposition proposée. | ✅ |
| Relance à 6 mois (e) | Uniquement avec `recontact_autorise` (demande expresse de la personne) | ✅ sous condition |
| Séquence d'aimant (f) | Information demandée, séquence annoncée sur le formulaire, désinscription | ✅ *(formulation à valider)* |
| Lettre trimestrielle | Double opt-in, ou exception « clients » informés | ✅ |
| Entretien à 2 ans, message annuel aux régies (i) | Exception « clients » : prestations analogues, information donnée à la collecte | ✅ si `info_exception_client` est rempli |
| **Séquence d'e-mails à froid automatisée vers des régies ou des architectes** | Publicité de masse sans consentement | ❌ **Interdite** |
| E-mail individuel rédigé à la main pour un contact choisi | Vraisemblablement hors « masse » ; expéditeur et opposition indiqués | ⚠️ Toléré, rare, jamais en série |
| Appel B2B à froid | Let. u et v respectées | ✅ |
| Courrier postal B2B | Hors let. o | ✅ |
| SMS promotionnel | Let. o (télécommunication) | ✅ uniquement avec opt-in |

### 9.3 Cookies et traceurs (art. 45c LTC, guide du PFPDT)

- **L'art. 45c LTC** impose d'**informer** sur le traitement de données dans le terminal (cookies, stockage local) et d'indiquer **comment le refuser** ([guide du PFPDT, v1.1](https://www.edoeb.admin.ch/dam/fr/sd-web/brLL9rM3ny9d/Leitfaden%20des%20ED%C3%96B%20betreffend%20Datenbearbeitungen%20mittels%20Cookies%20und%20%C3%A4hnlichen%20Technologien%20V.%201.1%20vom%2006.10.2025_FR.pdf), ch. 2.1).
- Les statistiques **anonymisées** sont justifiables par un intérêt prépondérant (ch. 3.8.2).
- La publicité de « profilage normal » demande au minimum une opposition bien visible (ch. 3.11.2) ; le profilage à risque élevé demande un **consentement exprès** (ch. 3.10.5).
- **Politique de Google** : elle s'applique aux utilisateurs suisses depuis le 31.07.2024 ([Google](https://www.google.com/about/company/user-consent-policy-help/)). Sans consentement, pas de mesure de conversion ni de reciblage Google Ads basés sur des cookies.
- **Décision (alignée sur le programme v2)** : site sans cookie par défaut (Umami). Bandeau d'**opt-in** pour toute balise publicitaire (M et L). « Refuser » aussi visible qu'« Accepter ». Lien « Paramètres des cookies » permanent dans le pied de page.

### 9.4 Autres points juridiques et déontologiques

| Sujet | Règle | Application |
|---|---|---|
| Allégations | LCD, art. 3 al. 1 let. b (indications inexactes ou fallacieuses) | Ni « n°1 », ni chiffres non prouvés (« 300+ chantiers » seulement si le client le confirme), ni faux avis, ni fausse urgence. Normes citées sans promesse de performance (la performance dépend du projet). |
| Corruption | Art. 4a LCD (corruption privée) ; art. 322quinquies CP (avantage accordé à un agent public) | **Aucun cadeau ni commission personnelle** à un employé de régie, de bureau ou de commune en échange de mandats. Les invitations restent modestes et transparentes. Le parrainage des particuliers prend la forme d'un don associatif. |
| Marchés publics | Égalité de traitement, règles de la procédure | Aucun contact commercial avec l'adjudicateur pendant une procédure en cours (pipeline AO exclu des relances). |
| Avis | [Politique Google](https://support.google.com/contributionpolicy/answer/7400114?hl=fr) | Pas de sélection, pas de contrepartie, pas d'avis interne (§3.10). |
| Images et références | Droit à l'image ; LDA ; LPAP pour les armoiries ; accord des clients | Accord écrit pour les visages, les intérieurs privés, les marques privées et les témoignages. Armoiries publiques rendues en texte (programme v2, §4). Accord recueilli par le formulaire de (d) J+14 et conservé dans le CRM. |
| Enregistrement des appels | Art. 179bis ss CP | Pas d'enregistrement sans information préalable des interlocuteurs. Aucun enregistrement n'est prévu dans ce plan. |
| Meta | Catégorie spéciale « Logement » | Déclarer la catégorie ; ne pas chercher à contourner les restrictions de ciblage (§3.5). |
| simap | Conditions d'utilisation, pas de licence de données ouvertes | Usage interne de veille ; fréquence de requête raisonnable (une fois par semaine) ; aucune republication. |

### 9.5 Risques opérationnels

| Risque | Probabilité | Impact | Parade |
|---|---|---|---|
| Les associés n'utilisent pas le CRM | Élevée | Élevé (les relances tombent) | Liens en un clic, saisie express, récapitulatif du lundi, CRM presque invisible. Point de 15 min avec l'agence à M1 et M2. |
| Panne de n8n ou du VPS | Moyenne | Moyen | Le PHP envoie toujours l'e-mail ; file d'attente rejouée ; supervision Healthchecks ; instantanés quotidiens ; n8n Cloud en secours. |
| E-mails en spam | Moyenne | Élevé | SPF, DKIM et DMARC dès M0 ; montée en volume progressive ; envois 1:1 depuis les boîtes des associés ; Brevo pour le marketing. |
| Spam sur le formulaire | Moyenne | Faible | Piège à robots, délai minimal, limite par IP ; pas de CAPTCHA tiers (protection des données, accessibilité). |
| Afflux de demandes supérieur à la capacité | Faible à moyenne | Moyen (délais non tenus, avis négatifs) | Règle « capacité d'abord » (§1.3) ; promesse de délai calculée ; baisse de Google Ads en premier. |
| Demandes de faible qualité (petits travaux, hors zone) | Élevée au début | Moyen | Champs de qualification, scoring, négatifs Google Ads, réponse type « hors cible ». |
| Avis négatif | Moyenne | Moyen | Réponse sous 48 h, appel, solution ; jamais de suppression demandée sans motif valable. |
| Restrictions de Meta (catégorie Logement) | Élevée | Faible | Budget modeste ; c'est la créa qui cible ; repli possible sur Google. |
| Les CPC réels dépassent les estimations | Moyenne | Moyen | Étude Keyword Planner en M0 ; budgets par zone ; règle du CPL max ; mots-clés en expression ou exacte uniquement. |
| Dépendance à un fournisseur (Pipedrive, Brevo) | Faible | Moyen | Export CSV hebdomadaire ; workflows qui passent par une couche d'abstraction (nœuds HTTP regroupés par sous-workflow). |
| Données incohérentes (NAP) | Moyenne | Élevé (SEO et GEO) | Décisions client en M0 ; tableau de contrôle des annuaires ; vérification mensuelle de la fiche Google. |
| Contenus non validés publiés | Faible | Élevé (LCD, confiance) | Mode « preview » du générateur ; statut des logos ; blocs masqués tant qu'ils sont vides (programme v2, §6). |

---

## Annexe A. Questions à poser au client (bloquantes pour la calibration)

1. Historique 2025 : demandes, offres envoyées, offres signées, panier moyen par type de client, marge brute indicative.
2. Capacité : nombre d'équipes, chantiers simultanés, délai actuel du carnet.
3. Horaires réels et numéro principal à appeler ; qui rappelle quoi (rôles « bureau » et « terrain »).
4. L'offre et la visite sont-elles gratuites ? Contrats soumis à la norme SIA 118 ? Conditions d'un passage de contrôle à 2 ans ?
5. Logiciel d'offres et de factures utilisé (bexio, Abacus, Word…) ?
6. Liste des 30 clients récents ou fidèles pour le 1er lot d'avis, avec leurs coordonnées.
7. Attestations disponibles (AVS, LPP, CCT du second œuvre romand, RC, impôts, TVA) et affiliation à une association professionnelle.
8. « Cloisons isothermes » : cloisons isolantes uniquement, ou aussi chambres froides ?
9. Accord pour citer les références (marques privées) et années des chantiers.
10. Accord pour un bouton WhatsApp (sur le mobile) et pour des panneaux de chantier.

## Annexe B. Sources

**Marché, comportements, benchmarks**
- Statcounter, moteurs de recherche en Suisse : https://gs.statcounter.com/search-engine-market-share/all/switzerland
- Pro Senectute, Digital Seniors 2025 : https://www.prosenectute.ch/fr/espace-pro/fond/etudes/digital-seniors-2025.html
- UZH / RTS, usage de l'IA en Suisse : https://www.rts.ch/info/societe/2025/article/l-ia-creuse-le-fosse-numerique-etude-alarmante-sur-l-exclusion-en-suisse-29051234.html
- Whitespark, aperçus IA et pack local : https://whitespark.ca/blog/case-study-the-prevalence-of-ai-overviews-in-local-search/
- Whitespark, facteurs de classement local 2026 : https://whitespark.ca/local-search-ranking-factors/
- Whitespark, fin des Q&R de la fiche Google : https://whitespark.ca/blog/with-google-qa-gone-you-need-a-maps-ask-a-question-strategy/
- BrightLocal, sources de ChatGPT Search : https://www.brightlocal.com/research/uncovering-chatgpt-search-sources/
- Unbounce, Conversion Benchmark Report 2024 (via PR Newswire) : https://prnewswire.com/news-releases/unbounces-2024-conversion-benchmark-report-proves-that-attention-spans-are-declining-and-so-are-conversion-rates-302239407.html
- WordStream/LocaliQ, benchmarks Google Ads (données 2025, via Shopifreaks) : https://www.shopifreaks.com/google-ads-cpcs-rose-to-5-42-in-2025-with-87-of-industries-seeing-increases-but-conversion-rates-climbed-to-8-18-as-automation-improves/
- Swiss Adex, CPC moyen en Suisse (markt-kom) : https://www.markt-kom.com/en/?p=24895
- Ostend Digital, Google Ads pour artisans (Allemagne) : https://ostend.digital/google-ads-handwerker/
- OFS, investissements 2025 (LFM) : https://www.lfm.ch/actualite/suisse/investissements-beton-dans-la-construction-suisse-en-2025/
- Genève, seuils des marchés publics : https://www.ge.ch/role-autorites-adjudicatrices-marches-publics/principes-types-procedures-cadre-legal
- Genève, IDC : https://www.ge.ch/connaitre-consommation-energie-batiment-idc/que-faire-resultat-idc-votre-immeuble
- AIET, prescriptions incendie : https://www.bpuk.ch/fileadmin/Dokumente/bpuk/public/fr/dokumentation/medienmitteilungen/2026/Communique_de_presse_AIET_Prescription_de_protection_incendie.pdf
- FAO Vaud, exemple de lot CFC 271/283/285 : https://www.faovd.ch/marches-publics/detail/2216/1179973/fondation-mont-calme-lausanne-cfc-271-283-285-platrerie-faux-plafond-peinture-pour-la-construction-d-un-ems-de-122-lits/

**Google, Meta, LinkedIn**
- Google, classement local : https://support.google.com/business/answer/7091?hl=fr
- Google, consignes de représentation d'une entreprise : https://support.google.com/business/answer/3038177?hl=fr
- Google, règles relatives aux contributions (faux engagement, avis) : https://support.google.com/contributionpolicy/answer/7400114?hl=fr
- Google, fin de Business Messages et du chat de la fiche : https://developers.google.com/business-communications/business-messages/resources/release-notes/update-on-gbm
- PPC Land, fin de l'API Q&R de la fiche Google : https://ppc.land/google-discontinues-business-profile-q-a-api-effective-november-3/
- Google Ads, rapports d'appels et numéros de transfert : https://support.google.com/google-ads/answer/2454052
- Google, politique relative au consentement de l'utilisateur dans l'UE (EEE, Royaume-Uni, Suisse) : https://www.google.com/about/company/user-consent-policy-help/
- Search Engine Land, annonces de services locaux en Europe : https://searchengineland.com/google-takes-local-services-ads-to-europe-341284
- Meta Developers, catégories spéciales d'annonces : https://developers.facebook.com/documentation/ads-commerce/marketing-api/audiences/special-ad-category
- Jon Loomer, catégories spéciales Meta : https://www.jonloomer.com/special-ad-categories-meta-ads/
- LeadSync, catégorie spéciale 2026 : https://leadsync.me/blog/special-ad-category-meta/
- LinkedIn Marketing Solutions (budget minimum) : https://business.linkedin.com/marketing-solutions

**Outils et tarifs**
- n8n, tarifs et hébergement : https://n8n.io/pricing/
- Brevo, limites de l'offre gratuite : https://help.brevo.com/hc/en-us/articles/208580669
- Pipedrive, tarifs 2026 (Zeeg) : https://zeeg.me/en/blog/post/pipedrive-pricing
- Infomaniak, VPS Lite : https://www.infomaniak.com/fr/hebergement/vps-lite
- Plausible : https://plausible.io/
- Matomo, tarifs : https://matomo.org/pricing/
- Umami, événements personnalisés : https://umami.is/blog/understanding-custom-events-umami-vs-ga4
- ASPSMS : https://www.aspsms.com/en/
- Twilio, SMS Suisse : https://www.twilio.com/fr-fr/sms/pricing/ch
- La Poste, tarifs des lettres : https://www.post.ch/fr/expedier-des-lettres/lettres-suisse
- simap.ch, API de lecture (client open source documenté) : https://pypi.org/project/swiss-procurement-mcp
- PME admin.ch, participer à un appel d'offres (simap gratuit) : https://www.kmu.admin.ch/de/teilnahme-an-einer-ausschreibung

**Droit**
- LCD, art. 3 (texte) : https://juriup.ch/lois/lcd/art-3/
- OFCOM/BAKOM, envoi de masse : https://www.bakom.admin.ch/en/when-is-mass-sending-allowed
- WEKA, e-mail marketing en Suisse (personnes morales incluses) : https://www.weka.ch/themen/datenschutz-und-it-recht/datenschutz-umsetzen/article/datenschutz-newsletter-rechtssicheres-e-mail-marketing-in-der-schweiz/
- PFPDT, guide sur les cookies, v1.1 du 6.10.2025 : https://www.edoeb.admin.ch/dam/fr/sd-web/brLL9rM3ny9d/Leitfaden%20des%20ED%C3%96B%20betreffend%20Datenbearbeitungen%20mittels%20Cookies%20und%20%C3%A4hnlichen%20Technologien%20V.%201.1%20vom%2006.10.2025_FR.pdf
- Conseil fédéral, Swiss-US Data Privacy Framework : https://admin.ch/gov/en/start/documentation/media-releases.msg-id-102054.html
- nLPD, présentation pour les PME : https://www.kmu.admin.ch/fr/nouvelle-loi-sur-la-protection-des-donnees-nlpd
