# Tableau de bord d'administration : plan

*Product design et architecture · 1er novembre 2026 · destinataires : associés (décisions du §7.4), chef de projet, agence Harbor Digital (développement et exploitation), juriste (§2.5, §4.6 et §6.5).*
*Statut : proposition à valider. Maquette cliquable : `docs/v4/admin/maquette/index.html` (s'ouvre sans serveur).*

> **Conventions.**
> - Les **objectifs** viennent de `docs/v2/strategie-acquisition.md` §1.1 (scénario M) et §1.3. Tous les autres chiffres de ce document et de la maquette sont **fictifs** ou des **estimations à valider**, et sont signalés comme tels.
> - Montants en CHF, hors TVA, apostrophe suisse (1'200).
> - « Heures ouvrables » : du lundi au vendredi, de 7 h à 18 h, hors jours fériés genevois et fermetures saisies, exactement comme `site/api/lib/HeuresOuvrables.php`.
> - Les noms d'étapes et d'indicateurs du §5 sont **partagés** avec le plan d'acquisition v4 : ils ne doivent pas être renommés.

---

## 0. L'essentiel

1. **Recommandation : un admin maison (option A).** Il prolonge `site/api/` sur l'hébergement du site, en Suisse, avec une base MariaDB. L'API écrit chaque demande en base. n8n garde les automatisations (SMS, relances, avis, rapport), mais lit et écrit dans l'admin au lieu de Pipedrive. **Pipedrive n'est pas souscrit.**
2. **Pourquoi.** Une seule source de vérité, en Suisse. Les indicateurs se calculent là où sont les données (CPL, CAC, ROAS par canal, délais en heures ouvrables genevoises). L'agence voit les chiffres sans voir les personnes. L'export et l'effacement nLPD se font en un seul endroit. Ce n'est **pas** une économie : la licence Pipedrive évitée (≈ CHF 26 par mois) ne rembourse jamais le développement.
3. **Coût et effort.** Coût mensuel ajouté ≈ CHF 0 si l'hébergement actuel offre PHP 8.1+ et MariaDB *(à vérifier)*. **MVP ≈ 20 jours** de développement, V2 ≈ 13 jours, V3 ≈ 8 jours *(estimations à valider, au tarif de l'agence)*. Maintenance ≈ 1 jour par trimestre.
4. **Le MVP couvre le quotidien** : À traiter (qui rappeler), Demandes (liste et colonnes), Fiche demande, Saisie d'un appel, Vue d'ensemble (5 indicateurs, entonnoir, alertes), Paramètres (utilisateurs, objectifs, dépenses), Journal et données personnelles. Acquisition, SEO et visibilité, Avis, Offres et chantiers, Rapport mensuel arrivent en V2. L'import des chantiers signés dans Google Ads arrive en V3.
5. **Téléphone d'abord** pour À traiter, la fiche et la saisie : du SMS reçu au résultat de l'appel en trois gestes. Les liens « en un clic » des SMS sont conservés.
6. **Les 5 indicateurs de la vue d'ensemble** : demandes/mois (avec la part A+B), délai de premier contact (médiane, demandes A), taux demande→offre, CA signé (avec le taux offre→signée), CPL. Chacun face à son objectif du mois, avec sa définition.
7. **Sécurité** : mot de passe et double authentification obligatoires, quatre rôles, journal d'audit, sauvegardes chiffrées en Suisse, aucune donnée gardée sur le téléphone.
8. **nLPD** : purge automatique (24 mois sans suite), effacement qui anonymise sans fausser les statistiques, export d'une personne en un clic. Le registre et la politique de confidentialité sont à mettre à jour (Pipedrive retiré).
9. **14 workflows n8n sur 16 appellent Pipedrive** (55 appels d'API). Ils sont adaptés à l'API de l'admin dans le MVP. Ils n'ont encore jamais tourné en production : c'est le moment de le faire, avant leur mise en service.
10. **14 décisions attendent le client** (§7.4). Les plus urgentes : l'option d'architecture, l'hébergeur, le taux de marge brute de référence, l'import des chantiers signés dans Google Ads.

---

## 1. Utilisateurs et tâches

### 1.1 Profils

| Profil | Où, sur quel appareil | Fréquence | Voit | Ne voit pas |
|---|---|---|---|---|
| **Associé « terrain »** (rôle `associe`) | Sur le chantier, au téléphone, entre deux tâches ; lumière forte, parfois des gants | 5 à 15 fois par jour, 30 secondes | Tout ; utilise surtout À traiter, la fiche et la saisie | — |
| **Associé « bureau »** (rôle `associe`) | Au bureau le matin (ordinateur), au téléphone ensuite | 2 à 5 fois par jour ; 30 minutes le lundi | Tout | — |
| **Secrétariat** éventuel (rôle `secretariat`) | Au bureau | Quotidienne | Demandes, fiches, saisie, offres, visites, indicateurs | Utilisateurs et rôles, export, effacement, journal des autres |
| **Agence, marketing** (rôle `agence_marketing`) | Au bureau | Hebdomadaire et rapport mensuel | Indicateurs agrégés : Vue d'ensemble (alertes en nombre seulement), Acquisition, SEO et visibilité, Avis (textes publics), Rapport ; saisie des dépenses et des citations IA | **Aucune donnée personnelle de prospect** : ni nom, ni téléphone, ni e-mail, ni message, ni commune exacte, ni fiche |
| **Agence, technique** (rôle `agence_technique`) | Au bureau | Mensuelle (maintenance) | État des intégrations, journal technique | Les fiches. L'accès aux données passe par le serveur, sous contrat de sous-traitance, et il est journalisé |

### 1.2 Tâches clés

| Question | Écran | Ce qui répond | Cible |
|---|---|---|---|
| « Ce matin, qui dois-je rappeler ? » | **À traiter** (accueil sur téléphone) | Retards en tête (rouge), puis les rappels du jour par échéance ; bouton Appeler sur chaque ligne | Une réponse sans défiler pour les retards |
| « Je viens d'avoir quelqu'un au téléphone » | **Saisie d'un appel** | 9 champs, score et priorité calculés pendant la saisie | 30 secondes |
| « Où en est cette offre ? » | Recherche, puis **Fiche demande** (ou Offres et chantiers) | Montant, date d'envoi, jours écoulés, relances faites et prochaine relance | 2 gestes |
| « Le client a signé » | Fiche, **Marquer signée** | Date et montant signé ; le chantier est créé | 3 champs |
| « Quel canal nous rapporte des chantiers signés ? » | **Acquisition** | Par canal : demandes, qualifiées, signées, CA signé | Un écran ; 3 derniers mois par défaut |
| « Combien coûte un client Google Ads ? » | Acquisition, ligne Google Ads | CAC = dépense / chantiers signés, à côté du CPL et du ROAS | Un écran |
| « Le mois est-il bon ? » | **Vue d'ensemble** | 5 indicateurs face à l'objectif du mois, projection de fin de mois | 10 secondes |
| « Une personne demande ses données » | **Journal et données personnelles** | Recherche par e-mail ou téléphone, export, effacement | Moins de 5 minutes, journalisé |

### 1.3 Principes de conception

1. **Le téléphone d'abord** pour À traiter, la fiche et la saisie. L'ordinateur pour les indicateurs.
2. **Une action fréquente, un geste.** Les actions rares sont dans un menu.
3. **Le rouge Andy (`#E8000F`) est réservé aux retards et à l'action principale de l'écran.** Tout le reste est anthracite, gris et blanc (charte v3 §3.1). Une priorité A n'est pas une alerte : elle n'est pas rouge.
4. **Un chiffre n'est jamais seul** : objectif, période et définition sont à côté.
5. **Chacun voit ce dont il a besoin.** Rien n'est gardé sur le téléphone.
6. **Le site et l'e-mail interne fonctionnent même si l'admin est en panne.**

---

## 2. Architecture

### 2.1 Point de départ (observé dans le dépôt)

- `site/api/demande.php` valide, score, calcule l'échéance, envoie l'e-mail interne et l'accusé de réception, puis transmet un webhook signé à n8n (`Traitement.php`). **Il n'y a pas de base de données** : une demande n'existe que dans les e-mails, dans la file d'attente du webhook et, dans le plan v2, dans Pipedrive. Les fichiers sont effacés du serveur après 30 jours.
- n8n : 16 workflows. **14 appellent l'API Pipedrive (55 appels)** ; seuls WF08 (simap) et WF13 (erreurs) n'en dépendent pas.
- Aucun workflow n'a encore tourné dans une vraie instance, et Pipedrive n'est pas souscrit (`HANDOFF.md` §9).
- Le suivi provisoire est `livrables/suivi-demandes-et-kpi.xlsx`.

### 2.2 Les trois options

| Critère | **A. Admin maison** | **B. Pipedrive + tableau de bord** | **C. Hybride** |
|---|---|---|---|
| Principe | Application PHP 8 sur l'hébergement du site, base MariaDB (ou SQLite), sous-domaine `gestion.andyconstruct.ch`. L'API écrit les demandes en base. n8n garde les automatisations et appelle l'API de l'admin. | Pipedrive gère les demandes (plan v2). n8n calcule les agrégats et les écrit dans Google Sheets ; Looker Studio les affiche. Les rapports intégrés de Pipedrive complètent. | Admin maison pour les demandes et les indicateurs, synchronisé dans les deux sens avec un CRM. |
| Coût mensuel des outils | **≈ CHF 0 de plus** (hébergement et VPS existants ; MariaDB en général incluse *à vérifier*). Pipedrive évité : − CHF 26. | **≈ CHF 26** (Pipedrive Lite × 2, v2 §7), + 1 licence par utilisateur en plus (secrétariat). Looker Studio : 0. Connecteur Pipedrive direct : partenaires payants *(tarifs à vérifier)* ; sinon Sheets alimenté par n8n : 0. | ≈ CHF 26 + A |
| Mise en place | **MVP ≈ 20 j** ; complet ≈ 41 j | ≈ 4 à 5 j (1 j de CRM prévu en v2, 3 à 4 j d'agrégats et de rapports) | A + 4 à 6 j de synchronisation |
| Maintenance | ≈ 1 j par trimestre : mises à jour PHP et bibliothèques, test de restauration, ajustements ; correctifs de sécurité sous 7 jours | ≈ 0,5 j par trimestre : champs, filtres et connecteurs à reprendre à chaque changement | La plus lourde : conflits de synchronisation, deux schémas |
| Sécurité | Nouvelle application exposée sur Internet, avec données personnelles. Maîtrisable : 2FA, rôles, CSP, tests d'accès par rôle, revue avant mise en ligne (§6.5) | Assurée par l'éditeur (2FA disponible). Deux outils de plus, deux jeux d'accès | Surfaces de A et de B |
| nLPD | Données en Suisse chez l'hébergeur ; un sous-traitant de moins ; export et effacement en un endroit ; agence sans données personnelles | Pipedrive (UE ; sous-traitants ultérieurs à vérifier dans le DPA), Google pour les agrégats (États-Unis, DPF) ; effacement dans plusieurs outils ; l'agence accède au CRM complet (droits fins réservés aux formules supérieures *à vérifier*) | Données en deux endroits ; effacement à faire deux fois |
| Dépendance | Au code et à l'agence. Code standard (PHP 8, SQL), documenté, testé ; export complet CSV et JSON (réversible) | À l'éditeur (prix, formules, API) ; 55 appels n8n liés à son API | Cumulée |
| Associés sur chantier | Interface web mobile ciblée (3 écrans) ; liens en un clic conservés ; pas d'application native ni de journal d'appels automatique | **Très bonne application mobile**, rappels d'activité natifs | Deux réflexes : l'application Pipedrive et l'admin |
| Indicateurs | Tous ceux du §5, calculés à la source, avec les mêmes règles que le scoring et les échéances | Étapes et montants dans Pipedrive. CPL, CAC, ROAS par canal, délais en heures ouvrables genevoises et cohortes calculés à côté (n8n + Sheets) : deux chiffres possibles pour la même chose | Dans l'admin |
| Points faibles | Délai (4 à 5 semaines avant le MVP), coût initial, dépendance à une équipe | Données dispersées (Pipedrive, Sheets, Umami, Search Console, e-mails) ; le tableau de bord est séparé de l'outil de travail ; ne répond pas à la demande « gérer les demandes dans un tableau de bord admin » | Deux sources de vérité ; ne se justifie que si un outil externe est déjà incontournable |

### 2.3 Recommandation : option A

**Pourquoi A :**
1. C'est la demande du client : gérer les demandes **et** voir les indicateurs au même endroit.
2. Les données utiles existent déjà dans l'API : score détaillé, règles appliquées, échéance en heures ouvrables, attribution (UTM, référent, page d'entrée), `gclid` avec consentement. Les écrire en base coûte peu. Les faire entrer dans Pipedrive demande une trentaine de champs personnalisés et leur correspondance dans n8n (`AC_PD_CHAMPS`).
3. Les indicateurs croisent demandes, dépenses et sources externes. Un seul calcul, une seule vérité, les mêmes définitions que le plan d'acquisition.
4. nLPD : un sous-traitant de moins, effacement en un endroit, agence sans données personnelles.
5. Volumes faibles (au plus ≈ 50 demandes par mois) et 2 à 4 utilisateurs : une application simple suffit, sans éditeur tiers.

**Conditions :**
1. Hébergement **en Suisse**, PHP 8.1+, **MariaDB 10.6+**, tâches planifiées, HTTPS, sous-domaine. *À vérifier chez l'hébergeur actuel (pays « à confirmer » dans le registre v2 §8).* Sinon, **variante A′** : l'admin et la base sur le VPS Infomaniak déjà prévu pour n8n ; `demande.php` y envoie la demande et garde sa file d'attente locale en cas de panne.
2. L'agence s'engage sur la maintenance (correctifs, sauvegardes testées, mises à jour).
3. Le MVP est en ligne **avant** l'activation des workflows n8n, pour ne pas les adapter deux fois.

**Pourquoi MariaDB plutôt que SQLite :** l'API, l'admin et n8n écrivent en même temps, et les hébergements mutualisés posent souvent leurs fichiers sur un disque réseau, où le verrouillage de SQLite n'est pas fiable. SQLite sert aux tests et au développement (même code via PDO).

**Ce que le client perd :** l'application mobile Pipedrive (remplacée par trois écrans mobiles ciblés) et une mise en route immédiate. En attendant le MVP, l'e-mail interne et le tableur `suivi-demandes-et-kpi.xlsx` suffisent ; ils fonctionnent dès la mise en ligne du site.

**Repli :** si le budget de développement n'est pas disponible au lancement, Brevo CRM gratuit (scénario S de la v2) pendant 3 à 6 mois, puis A. Coût du repli : adapter WF01 à WF03 à Brevo (½ jour, v2 §4.5), puis à l'admin.

### 2.4 Schéma des flux

```
 Visiteur ── site statique ── suivi.js : UTM, référent, page d'entrée ; gclid seulement avec consentement
                 │
                 │ POST /api/demande.php (devis, rappel, guide)
                 ▼
 site/api/ ─ Traitement : validation, anti-spam, fichiers, score, échéance
    1. ENREGISTRE la demande, le contact, l'attribution, les fichiers ───────────► MariaDB (CH)
       (base indisponible : file locale « file-attente-base », rejouée par cron.php)   ▲     ▲
    2. e-mail interne aux associés (résumé, Appeler, « Ouvrir la fiche ») ──► associés │     │
    3. accusé de réception au prospect                                                 │     │
    4. webhook HMAC vers n8n (file d'attente si panne, comme aujourd'hui)              │     │
                                                                                       │     │
 gestion.andyconstruct.ch ─ admin PHP, même hébergement, même dossier privé ─ lit/écrit┘     │
    associés, secrétariat (2FA)         agence : indicateurs agrégés seulement               │
                                                                                             │
 n8n (VPS Infomaniak, CH) ─ API interne de l'admin, signée HMAC (/interne/…) ───────────────┘
    WF01 SMS aux associés, accusé SMS · WF02 actions en un clic · WF03 horloge des rappels
    WF03c relances d'offre · WF03d avis · WF04 offres perdues, entretien · WF12/WF14 opposition
    WF13 erreurs · WF09 envoi du rapport mensuel (V2)
      ├──► ASPSMS (CH) : SMS          ├──► SMTP du domaine : e-mails 1:1     ├──► Brevo (UE)
      └──► lecture quotidienne, agrégats seulement, écrits dans l'admin (V2) :
           Umami (VPS, CH) · Search Console · Places / Business Profile · coûts Google Ads
 Saisie dans l'admin : dépenses Meta, LinkedIn, courrier · citations IA · chiffres de la fiche Google
 Admin ──► Google Ads (V3) : conversions hors ligne « chantier signé » (gclid, date, valeur),
           seulement pour les demandes arrivées avec consentement
```

Qui lit les sources externes : **n8n**, qui détient déjà les accès (Umami, Search Console, Places dans WF09). Il écrit des **agrégats** dans l'admin (`POST /interne/metriques`). L'admin ne garde ainsi aucun jeton Google, et une API externe en panne n'arrête que son bloc.

### 2.5 Hébergement et données (nLPD)

| Données | Où | Accès | Sous-traitant | Conservation |
|---|---|---|---|---|
| Demandes, contacts, notes, visites, offres, chantiers, fichiers | MariaDB et dossier privé hors racine web, hébergement du site (Suisse, *à confirmer*) | Associés, secrétariat ; agence technique par le serveur (DPA, journalisé) | Hébergeur | §4.6 |
| Agrégats (visites, clics, coûts, avis) | MariaDB | Tous les rôles | — | 3 ans |
| Journal d'audit | MariaDB | Associés ; agence technique sans contenu | Hébergeur | 12 mois |
| Sauvegardes chiffrées | Copie quotidienne sur le VPS Infomaniak (Suisse) | Agence technique | Infomaniak | 30 jours (rotation) |
| SMS, e-mails | ASPSMS (CH), messagerie du domaine | — | Déjà au registre v2 §8 | v2 §8 |
| `gclid`, date et valeur d'un chantier signé (V3) | Google (États-Unis, DPF) | — | Google | Uniquement si la personne a accepté la mesure publicitaire |

**À mettre à jour dans `docs/v2/automatisation.md` §8 et §9 (par l'ingénieur, après décision) :** Pipedrive retiré des sous-traitants et de la politique ; l'admin ajouté (finalité, accès par rôles, durées) ; les fichiers reçus ne sont plus effacés à 30 jours mais gardés avec la demande ; les sauvegardes (30 jours) mentionnées pour l'effacement ; la purge automatique à 24 mois remplace la liste manuelle de WF04p.

### 2.6 Ce qui change dans l'existant

| Élément | Changement | Phase |
|---|---|---|
| `site/api/lib/Traitement.php` | Nouvelle étape « enregistrer en base » (classe `Depot`) avant l'e-mail interne. En cas d'échec : écriture dans `stockage/file-attente-base/`, rejouée par `cron.php` ; l'e-mail interne part quand même | MVP |
| E-mail interne (`Modeles.php`) | Bouton « Ouvrir la fiche ». Pièces jointes gardées 3 mois, puis remplacées par le lien (décision G8) | MVP |
| Fichiers reçus | Déplacés dans `stockage/dossiers/<demande>/` (hors racine web), effacés avec la demande ; `fichiers.conservation_jours` ne vise plus que les fichiers orphelins | MVP |
| Saisie interne (`canal=telephone`, contrat §10) | Remplacée par l'écran Saisie d'un appel, qui passe par le même `Traitement` : score et échéance identiques | MVP |
| WF01, WF02, WF03, WF03c, WF03d, WF04e, WF04i, WF12, WF14 | Les appels Pipedrive deviennent des appels à l'API interne (§6.3). `verifier.py` adapté | MVP |
| WF06 (synchronisation du CRM) | Supprimé : les dates d'étape sont écrites par l'admin | MVP |
| WF04p (purge) | Purge faite par l'admin ; WF04p garde seulement l'alerte à l'agence | MVP |
| WF07, WF10 (guides, prospection B2B) | Module Prospection de l'admin | V2 |
| WF09 (rapport mensuel) | Remplacé par l'écran Rapport mensuel ; n8n envoie l'e-mail avec le lien | V2 |
| `livrables/suivi-demandes-et-kpi.xlsx` | Importé une fois dans l'admin (demandes reçues avant la mise en service) | MVP |

---

## 3. Arborescence et écrans

### 3.1 Arborescence

```
gestion.andyconstruct.ch
├── Connexion (mot de passe, puis code de double authentification)
├── À traiter ............................ /a-traiter          accueil sur téléphone
├── Vue d'ensemble ....................... /                   accueil sur ordinateur
├── Demandes ............................. /demandes           liste ; colonnes : /demandes?vue=colonnes
│   ├── Fiche demande .................... /demandes/AC-2027-0051
│   └── Saisir un appel .................. /demandes/nouvelle
├── Offres et chantiers .................. /offres             V2 (MVP : filtre de la liste)
├── Acquisition .......................... /acquisition        V2
├── SEO et visibilité .................... /visibilite         V2
├── Avis ................................. /avis               V2
├── Rapport mensuel ...................... /rapports/2027-03   V2
├── Paramètres ........................... /parametres/…
│     utilisateurs et rôles, objectifs, dépenses, économie, motifs de perte,
│     zones, scoring, heures ouvrables, capacité, intégrations
├── Journal et données personnelles ...... /donnees
└── Mon compte ........................... /compte             mot de passe, 2FA, appareils
Hors session : /action?t=…  (lien en un clic des SMS et e-mails : une page, un bouton)
```

**Navigation.** Ordinateur (≥ 960 px) : barre latérale anthracite et barre du haut (recherche, « Saisir un appel », compte). Téléphone (< 760 px) : barre du bas à cinq entrées : **À traiter** (pastille du nombre en retard) · **Demandes** · **Saisir** · **Chiffres** · **Plus**.
**Recherche globale** : référence, nom, téléphone (tous formats, normalisé comme `Telephone.php`), e-mail, commune ; résultats dès 3 caractères ; limitée aux rôles qui voient les fiches.

### 3.2 Composants communs

| Composant | Règle |
|---|---|
| Badge de priorité | Carré A, B ou C en niveaux de gris (A le plus foncé), lettre toujours écrite ; « Hors cible » en contour. Jamais rouge |
| Échéance | Texte (« dans 32 min », « aujourd'hui 18 h », « en retard de 1 h 20 ») et réglet du temps restant. Rouge uniquement en retard, avec une icône et le mot « En retard » |
| Statut | En toutes lettres : Nouvelle, Contact établi, Visite planifiée, Offre envoyée, Signée, Perdue, Hors cible |
| Montant | CHF 12'500, hors TVA |
| Tuile d'indicateur | Libellé, valeur, objectif du mois, écart, réglet, période, bouton « ? » (définition du §5) |
| Graphiques | SVG produits par le serveur, une seule teinte (anthracite) ou une rampe de gris ordonnée ; info-bulle au survol et au clavier ; tableau de données à côté (« Voir les données ») ; jamais deux axes |
| État vide | Une phrase qui dit quoi faire (« Rien à rappeler. Les nouvelles demandes arrivent ici. ») |
| Erreur | Ce qui s'est passé et quoi faire ; la saisie n'est jamais perdue (brouillon dans la mémoire de l'onglet) |
| Confirmation | Seulement pour l'irréversible (effacement) ou ce qui exige une information (signée : montant ; perdue : motif). Le reste est annulable 10 secondes (« Annuler » dans le message) |
| Tableaux | En-têtes `th scope`, tri au clavier, référence en lien ; lignes de 40 px sur ordinateur |

### 3.3 Écrans

Chaque écran est décrit par les mêmes rubriques. Les droits renvoient à la matrice du §6.5.

#### E1 · Vue d'ensemble (MVP ; Acquisition et visibilité en V2)

| Rubrique | Spécification |
|---|---|
| But | Savoir en 10 secondes si le mois est bon et ce qui bloque |
| Droits | Associés, secrétariat. Agence marketing : alertes en nombre seulement, sans nom |
| Composants | 1. **Alertes** : demandes A non rappelées dans le délai ; autres demandes en retard ; offres sans suite à J+35 (décision « Clore ? ») ; offres relancées 3 fois sans réponse ; visites du jour ; avis sans réponse depuis 48 h ; capacité (carnet en semaines face au seuil de 8). 2. **Cinq tuiles** : demandes/mois et part A+B · délai de premier contact (médiane A) · taux demande→offre · CA signé et taux offre→signée · CPL. 3. **Bande secondaire** (V2) : visites, taux visite→contact, avis Google, citations IA. 4. **Entonnoir** des 3 derniers mois. 5. **Demandes par mois** sur 6 mois, empilées par priorité, avec l'objectif. 6. **Capacité** |
| Données et calculs | §5. Mois en cours arrêté à l'instant. Projection de fin de mois pour les **demandes** (valeur × jours ouvrables du mois / jours ouvrables écoulés) et les **visites** (jours civils). Pas de projection pour les taux, les médianes ni le CA signé (les signatures arrivent par à-coups). Chaque tuile rappelle aussi la valeur du mois précédent |
| Filtres | Mois ; comparaison M−1 (et même mois N−1 après 12 mois) |
| Actions | Une alerte ouvre la liste filtrée ; une tuile ouvre l'écran de détail |
| État vide | « Les indicateurs apparaissent dès la première demande enregistrée. » Source externe non à jour : valeur grisée et « mis à jour le … » |
| Erreurs | Une source en panne n'empêche pas le reste ; date de mise à jour par bloc |
| Mobile | Alertes puis tuiles en une colonne ; graphiques sous « Voir plus » |

#### E2 · À traiter (MVP)

| Rubrique | Spécification |
|---|---|
| But | Répondre à « qui dois-je rappeler ce matin ? » |
| Droits | Associés, secrétariat |
| Composants | Sections dans cet ordre : **En retard** · **À rappeler** (par échéance) · **Tentatives à refaire** (après « Pas de réponse ») · **Visites** du jour et du lendemain · **Offres** : appels J+10, décisions J+35 · **Hors cible à valider** · **Avis à répondre**. Chaque ligne : priorité, nom (organisation), commune, travaux, échéance avec réglet, boutons **Appeler** et **Résultat** |
| Données | Demandes ouvertes au statut Nouvelle (échéance, tentatives) ; visites ; offres (étape de relance) ; avis non répondus |
| Filtres | « Mes demandes » par défaut (attribuées à l'utilisateur), bascule « Toutes ». La section **En retard montre toujours tous les retards**, quel que soit l'associé attribué : c'est l'escalade de WF03 à l'écran |
| Actions | Appeler (`tel:`). **Au retour dans l'onglet après un appel, la feuille « Résultat de l'appel » s'ouvre seule** : J'ai eu la personne · Pas de réponse · Message laissé · Numéro erroné. Réattribuer. Reporter (motif et nouvelle échéance, journalisé) |
| État vide | « Rien à rappeler pour l'instant. Prochaine échéance : … » |
| Erreurs | Hors connexion : « Pas de connexion, rien n'a été enregistré » ; l'action reste prête à renvoyer |
| Mobile | Écran d'accueil ; pastille du nombre de retards dans la barre du bas |

#### E3 · Demandes, liste (MVP)

| Rubrique | Spécification |
|---|---|
| But | Retrouver, filtrer, comparer les demandes |
| Droits | Associés, secrétariat ; export CSV : associés (journalisé) |
| Composants | Tableau : Réf. · Reçue · Nom (organisation) · Type de client · Travaux · Commune (zone) · Priorité (score) · Canal · Statut · Prochaine action ou échéance · Montant (offre ou signé) · Associé |
| Filtres | Une rangée au-dessus : recherche ; période (7 j, 30 j, mois, 3 mois, 12 mois, dates) ; statut (« ouvertes » par défaut) ; priorité ; canal ; type de client ; zone ; associé ; « en retard seulement ». Les filtres sont dans l'adresse : un associé peut envoyer une vue à l'autre |
| Tri | Échéance (défaut), date de réception, score, montant |
| Actions | Ouvrir la fiche ; réattribuer plusieurs demandes ; exporter |
| État vide | « Aucune demande pour ces filtres. » + « Effacer les filtres » |
| Mobile | Cartes empilées : nom, priorité, statut, prochaine action |

#### E4 · Demandes, colonnes (MVP)

| Rubrique | Spécification |
|---|---|
| But | Voir le portefeuille par étape |
| Composants | Colonnes : Nouvelle · Contact établi · Visite planifiée · Offre envoyée · Signée (30 derniers jours) · Perdue (30 derniers jours). Total par colonne (nombre, montant). Carte : nom, commune, travaux, priorité, jours dans l'étape, montant |
| Actions | Déplacer une carte change le statut. Seules les transitions autorisées (§4.5) sont proposées. Vers « Offre envoyée », « Signée » ou « Perdue », une fenêtre demande le montant ou le motif. Chaque carte a un menu « Déplacer vers… » (le glisser-déposer n'est pas le seul moyen) |
| Filtres | Les mêmes que la liste |
| Mobile | Une colonne à la fois, onglets en haut |

#### E5 · Fiche demande (MVP)

| Rubrique | Spécification |
|---|---|
| But | Tout savoir sur une demande et agir |
| Droits | Associés, secrétariat. Agence : aucun accès |
| En-tête | Nom, organisation, priorité et score, statut, échéance, associé ; boutons **Appeler**, E-mail, **Résultat de l'appel** |
| Coordonnées | Téléphone, e-mail, préférence de contact, créneau, adresse si connue ; « Doublon possible » si le même e-mail ou téléphone existe (fusion proposée) |
| Projet | Travaux, type de client, surface, délai, commune et zone, message, « recommandé par » |
| Fichiers | Vignettes et téléchargement authentifié (jamais d'adresse publique) |
| Score détaillé | Tableau critère · valeur · points (comme l'e-mail interne), règles appliquées, version de la grille. Correction de la priorité avec motif (journalisée) |
| Source et attribution | Canal, catégorie (`Source.php`), libellé, page d'entrée, page d'envoi, référent, UTM, `gclid` présent ou non, consentement, « Comment nous avez-vous connus ? ». Correction du canal (journalisée) |
| Historique | Fil chronologique : reçue, accusé, SMS, tentatives, notes, visite, offre, relances automatiques, réponses détectées, changements de statut ; chaque ligne avec son auteur (utilisateur, n8n ou site) |
| Notes | Texte libre ; invisibles pour l'agence |
| Offres et chantier | Versions de l'offre (numéro, montant, date, étape de relance) ; chantier si signée (dates, réception, réserves, avis) |
| Actions | Appeler · J'ai eu la personne · Pas de réponse (n° de la tentative) · **Planifier la visite** (date, heure, adresse, associé ; invitation de calendrier .ics) · **Envoyer l'offre** (n°, montant HT, date, PDF facultatif ; lance les relances J+3, J+10, J+21) · Relancer maintenant · Ne plus relancer · **Marquer signée** (date, montant signé ; crée le chantier) · **Marquer perdue** (motif obligatoire ; recontact à 6 mois oui ou non) · Hors cible (aperçu de la réponse de réorientation, envoi par l'associé) · **Demander un avis** (chantier terminé, réserves levées) · Fusionner · Réattribuer · Exporter · Effacer (via Données personnelles) |
| Erreurs | Conflit d'édition (deux personnes en même temps) : la seconde voit « Modifiée par … à … » et recharge sans perdre sa saisie |
| Mobile | En-tête collant avec Appeler ; blocs repliables (Projet ouvert, le reste fermé) ; barre d'action en bas : Appeler · Résultat · Plus |

#### E6 · Saisie d'un appel (MVP)

| Rubrique | Spécification |
|---|---|
| But | Enregistrer un appel reçu en 30 secondes, pour que les appels comptent comme les formulaires |
| Droits | Associés, secrétariat |
| Champs | **Téléphone** en premier (contact existant retrouvé, doublon signalé) · nom · commune ou NPA · travaux (boutons) · type de client · surface · délai · **« Comment nous avez-vous connus ? »** (obligatoire : c'est l'attribution des appels, v2 §6.4) · note · e-mail facultatif · case « Envoyer une confirmation écrite ». Canal : téléphone (défaut), e-mail reçu, visite au bureau, rencontre |
| Calculs | Score et priorité **pendant la saisie**, même grille (`scoring.json`) ; échéance affichée |
| Actions | « Enregistrer la demande » passe par `Traitement` (canal interne) : mêmes notifications, sauf vers l'auteur de la saisie. « Enregistrer et marquer le contact établi » (cas habituel : on vient de parler à la personne) |
| Erreurs | Champs manquants signalés sous chaque champ ; brouillon gardé dans l'onglet |
| Mobile | Clavier numérique pour le téléphone et le NPA ; boutons de 48 px |

#### E7 · Offres et chantiers (V2 ; MVP : liste filtrée sur « Offre envoyée »)

| Rubrique | Spécification |
|---|---|
| But | « Où en est cette offre ? » et « Combien avons-nous en attente ? » |
| Composants | **Offres ouvertes** : réf., client, montant, envoyée le, jours écoulés, relances faites (0 à 3), prochaine action. **Chantiers** : à planifier, planifiés, en cours, terminés (réserves), avis demandé ; dates, jours-équipe. Totaux : montant en attente, taux offre→signée (cohorte), délai médian offre→signature, carnet en semaines |
| Actions | Marquer signée ou perdue ; planifier ; réception faite ; réserves levées ; litige (suspend la demande d'avis) |
| Filtres | Associé, type de client, montant, ancienneté |

#### E8 · Acquisition (V2)

| Rubrique | Spécification |
|---|---|
| But | « Quel canal nous rapporte des chantiers signés, et à quel coût ? » |
| Droits | Associés, secrétariat, agence marketing (lecture, saisie des dépenses) |
| Composants | **Tableau par canal** : dépense · demandes · qualifiées (et part A+B) · signées · CA signé · CPL · CAC · ROAS · ROI · part des canaux · tendance sur 6 mois. Canaux payants d'abord, puis les autres ; total des canaux payants et total général. **Graphiques** : demandes par canal (barres classées) ; CA signé par canal ; CPL des canaux payants face à la cible. **Bloc Google Ads** : dépense, clics, CPC, demandes, part des demandes avec `gclid`, conversions envoyées (V3) |
| Données | §5 et §5.4 (canaux). Dépenses : import Google Ads, saisie pour les autres |
| Filtres | Période : **3 derniers mois civils par défaut** (petits nombres), mois, 12 mois ; type de client |
| Avertissements | « Moins de 3 chantiers signés : CAC et ROAS indicatifs. » Part des demandes au canal inconnu |
| État vide | Avant le 1er mois complet : « Les comparaisons par canal demandent au moins un mois complet. » Dépense manquante : « Dépense de mars à saisir » (lien vers Paramètres) |

#### E9 · SEO et visibilité (V2)

| Rubrique | Spécification |
|---|---|
| But | Suivre ce qui fait venir sans payer : recherche, fiche Google, IA |
| Composants | **Search Console** : clics, impressions, CTR, position moyenne (28 jours, comparaison) ; courbe hebdomadaire des clics ; tableau des 30 requêtes cibles et des pages. **Fiche Google** : appels, itinéraires, clics vers le site (mois). **Citations IA** : grille des 10 questions × assistants, score sur 10, historique |
| Données | Agrégats écrits par n8n ; citations IA saisies (agence) |
| État vide | « Search Console n'est pas encore relié » (lien vers Intégrations) |

#### E10 · Avis (V2)

| Rubrique | Spécification |
|---|---|
| But | Atteindre 50 avis à M12 sans en trier aucun, et répondre à chacun |
| Composants | Indicateurs : avis Google (nombre cumulé face à l'objectif, note), avis du mois, demandes d'avis envoyées, part des demandes suivies d'un avis à 30 jours, délai de réponse. Liste : date, note, texte public, auteur tel qu'affiché par Google, chantier rapproché, réponse (à rédiger, brouillon, publiée) |
| Actions | Rapprocher d'un chantier (marque « avis reçu », arrête la relance J+9) ; préparer ou valider la réponse ; copier pour la publier sur la fiche (V2), publier par l'API (V3) |
| Droits | Agence : lecture et brouillons ; rapprochement : associés |

#### E11 · Rapport mensuel (V2)

| Rubrique | Spécification |
|---|---|
| But | Le bilan du mois, figé, partageable avec l'agence |
| Composants | Contenu de la v2 §6.5 : Résultats, Réactivité, Sources, Site, Recherche, Google Ads, Réputation, B2B et appels d'offres, Automatisation, 3 actions. En tête, les 5 indicateurs de la vue d'ensemble |
| Calculs | Produit le 1er jour ouvrable à 7 h et **figé** (les chiffres du rapport ne bougent plus si une donnée est corrigée ensuite ; l'écart est signalé) |
| Actions | Commentaire de l'agence (3 actions) sous 48 h ; validation par un associé ; **export PDF** (gabarit A4 ; MVP de V2 : impression du navigateur ; ensuite Gotenberg sur le VPS) |
| Droits | Sans donnée personnelle : lisible par l'agence |

#### E12 · Paramètres (MVP pour les utilisateurs, objectifs, dépenses et économie ; le reste en lecture)

| Sous-écran | Contenu | Qui modifie |
|---|---|---|
| Utilisateurs et rôles | Créer, désactiver ; rôle ; rôle métier « bureau » ou « terrain » (attribution des demandes, `config.php` → `associes`) ; numéro pour les SMS internes ; réinitialiser la 2FA d'un autre utilisateur | Associés |
| Objectifs | Jalons M3, M6, M12 (v2 §1.1), scénario S, M ou L ; valeurs mensuelles interpolées, modifiables (décision G6) | Associés |
| Dépenses | Grille mois × canal ; Google Ads importé (verrouillé) ; justificatif facultatif | Associés, agence marketing |
| Économie | Taux de marge brute (global ou par service), panier de référence, inclusion ou non des honoraires d'agence dans les dépenses | Associés |
| Motifs de perte | Prix, délai, reporté, attribué ailleurs, sans réponse, hors cible, trop petit, autre ; « autorise la relance à 6 mois » | Associés |
| Zones | Table NPA → zone (`zones.json`) ; recherche d'une commune ; correction | Associés |
| Scoring | Grille (`scoring.json`) affichée ; versions datées ; simulation sur les 6 derniers mois (V3) | Associés |
| Heures ouvrables | Heures, fermetures (vacances du bâtiment) | Associés |
| Capacité | Nombre d'équipes, seuil d'alerte (8 semaines, v2 §1.3) | Associés |
| Intégrations | État de chaque source (dernière lecture, erreur) ; aucune clé affichée | Lecture : associés, agence |

#### E13 · Journal et données personnelles (MVP)

| Rubrique | Spécification |
|---|---|
| But | Prouver qui a fait quoi ; répondre à une demande d'accès ou d'effacement en moins de 5 minutes |
| Droits | Associés |
| Journal d'audit | Filtres : utilisateur, action, période, objet ; lecture seule ; export pour l'agence technique |
| Droits des personnes | Registre des demandes (accès, rectification, effacement, opposition) avec échéance à 30 jours. Recherche d'une personne par e-mail ou téléphone : toutes ses demandes. **Exporter** : ZIP (JSON, PDF lisible, fichiers). **Effacer** : aperçu de ce qui est effacé et de ce qui est gardé, et pourquoi (empreinte sur la liste d'opposition si la personne refuse tout contact ; pièces comptables hors de l'admin) ; confirmation en tapant la référence |
| Purge | Demandes qui seront anonymisées dans les 30 jours (24 mois sans suite) ; report possible avec motif (litige) |

#### E14 · Connexion, Mon compte et page « en un clic »

| Écran | Spécification |
|---|---|
| Connexion | E-mail, mot de passe, puis code à 6 chiffres (ou code de secours) ; « Faire confiance à cet appareil 30 jours » |
| Mon compte | Mot de passe, double authentification, appareils (révoquer), dernières connexions |
| Page « en un clic » (hors session) | Lien signé des SMS et e-mails (jeton à usage unique, 7 jours). Une page, un résumé minimal (référence, prénom, commune), **un bouton** (« J'ai eu la personne » ou « Pas de réponse ») : la prévisualisation d'un lien par la messagerie ne déclenche rien. Ensuite, lien « Ouvrir la fiche » (connexion requise) |

---

## 4. Modèle de données

### 4.1 Relations

```
utilisateur 1─n appareil
organisation 1─n contact 1─n demande 1─1 attribution n─1 campagne 1─n depense
                             demande 1─n interaction
                             demande 1─n visite
                             demande 1─n offre 1─0..1 chantier 1─n avis (rapprochés)
                             demande 1─n fichier
                             demande 1─n conversion_ads
                             demande 1─n jeton_action
contact 1─n demande_droits
Indépendantes : objectif, parametre, motif_perte, metrique_externe, citation_ia, opposition
journal_audit ──► (objet_type, objet_id) de n'importe quelle table
```

Types MariaDB. Dates et heures en **UTC** (`DATETIME`), affichées en Europe/Zurich ; les calculs d'heures ouvrables se font en PHP (`HeuresOuvrables`). Montants en `DECIMAL(10,2)`. `JSON` = colonne JSON validée (MariaDB). Identifiants `INT UNSIGNED AUTO_INCREMENT`.

### 4.2 Tables

**utilisateur**

| Champ | Type | Note |
|---|---|---|
| id | INT PK | |
| email | VARCHAR(190) UNIQUE | identifiant de connexion |
| nom_affiche | VARCHAR(100) | |
| role | ENUM('associe','secretariat','agence_marketing','agence_technique') | §6.5 |
| role_metier | ENUM('bureau','terrain') NULL | attribution automatique des demandes |
| telephone_sms | VARCHAR(20) NULL | E.164, SMS internes envoyés par n8n |
| mdp_hash | VARCHAR(255) | argon2id |
| totp_secret | VARBINARY(255) | chiffré (clé hors base, dans `config.php`) |
| codes_secours | JSON | empreintes |
| actif | BOOL | |
| cree_le, derniere_connexion_le, mdp_change_le | DATETIME | |

**appareil** (sessions et appareils de confiance) : id, utilisateur_id (FK), libelle (navigateur et système), jeton_hash (UNIQUE), confiance_jusqu_au, dernier_usage_le, ip_tronquee, revoque_le.

**organisation**

| Champ | Type | Note |
|---|---|---|
| id | INT PK | |
| nom | VARCHAR(150) | |
| type | ENUM('regie','architecte','commune','entreprise','partenaire','autre') | |
| npa, localite | VARCHAR | |
| telephone, site_web | VARCHAR NULL | |
| palier | TINYINT NULL | prospection B2B (V2) |
| asterisque_verifie_le | DATE NULL | annuaire (LCD) |
| cree_le, modifie_le | DATETIME | |

**contact**

| Champ | Type | Note |
|---|---|---|
| id | INT PK | |
| organisation_id | INT FK NULL | |
| civilite | ENUM('madame','monsieur') NULL | |
| prenom, nom | VARCHAR(100) | |
| fonction | VARCHAR(100) NULL | |
| email | VARCHAR(190) NULL | |
| email_normalise | VARCHAR(190) NULL | minuscules, IDN converti ; index |
| telephone_e164 | VARCHAR(20) NULL | index |
| telephone_mobile | BOOL | |
| adresse, npa, localite | VARCHAR NULL | |
| preference_contact | ENUM('appel','email','indifferent') NULL | |
| opposition_marketing_le | DATETIME NULL | arrête tout message marketing |
| info_exception_client_le | DATE NULL | information du droit d'opposition (LCD) |
| dernier_message_marketing_le | DATETIME NULL | plafond d'un message par 30 jours |
| anonymise_le | DATETIME NULL | effacement fait |
| cree_le, modifie_le | DATETIME | |

**demande**

| Champ | Type | Note |
|---|---|---|
| id | INT PK | |
| ref | CHAR(12) UNIQUE | AC-AAAA-NNNN (`Reference.php`) |
| contact_id, organisation_id | INT FK | |
| recue_le | DATETIME | index |
| canal | ENUM('site','telephone','email','visite','recommandation','b2b') | |
| formulaire | ENUM('devis','rappel','saisie') | |
| type_client | VARCHAR(20) NULL | valeurs de `Champs::TYPE_CLIENT` |
| travaux | JSON | liste ; `service` dérivé (« plusieurs » si 2 prestations ou plus) |
| service | VARCHAR(30) | |
| surface, delai | VARCHAR(20) NULL | valeurs de `Champs` |
| commune, npa, canton | VARCHAR | |
| zone | ENUM('1','2','3','inconnue','hors') | |
| message | TEXT NULL | 3'000 caractères au plus |
| creneau, preference_contact | VARCHAR NULL | |
| connu_par, recommande_par | VARCHAR NULL | |
| score | SMALLINT | |
| priorite | ENUM('A','B','C','hors_cible') | calculée |
| priorite_corrigee | ENUM('A','B','C','hors_cible') NULL | fait foi si remplie ; motif dans `interaction` |
| score_detail, score_regles | JSON | sortie de `Scoring::calculer` |
| grille_version | VARCHAR(20) | `scoring.json` → version |
| echeance_le | DATETIME | premier contact attendu ; index avec statut |
| associe_id | INT FK | utilisateur attribué |
| statut | ENUM('nouvelle','contact_etabli','visite_planifiee','offre_envoyee','signee','perdue','hors_cible','doublon') | §4.5 |
| statut_change_le | DATETIME | |
| premier_contact_le | DATETIME NULL | « J'ai eu la personne » ou réponse écrite |
| tentatives_appel | TINYINT | |
| a_repondu | BOOL | réponse détectée (WF14) : arrête les relances |
| ne_pas_relancer | BOOL | |
| motif_perte_id | INT FK NULL | |
| perdue_le | DATETIME NULL | |
| recontact_autorise_le | DATE NULL | relance unique à 6 mois |
| doublon_de_id | INT FK NULL | |
| accuse_reception | ENUM('envoye','limite','mis_de_cote','non','sms') | |
| mode_test | BOOL | exclue des indicateurs |
| anonymise_le | DATETIME NULL | |
| cree_par | INT FK NULL | NULL = site |

**attribution** (une ligne par demande ; séparée pour être minimisée ou purgée à part)

| Champ | Type | Note |
|---|---|---|
| demande_id | INT PK FK | |
| categorie | VARCHAR(30) | sortie de `Source::normaliser` |
| canal_marketing | VARCHAR(30) | §5.4 ; index |
| canal_corrige | VARCHAR(30) NULL | correction par un associé ; fait foi |
| libelle | VARCHAR(150) | |
| emplacement, page, page_entree, referent | VARCHAR(150) | champs cachés du contrat §3 |
| utm_source, utm_medium, utm_campaign, utm_content, utm_term | VARCHAR(100) | |
| gclid | VARCHAR(150) NULL | seulement si `consent_ads = accorde` ; effacé après l'envoi ou à 90 jours |
| consent_ads | ENUM('accorde','refuse') NULL | |
| campagne_id | INT FK NULL | |

**interaction** (historique, notes, appels, messages) : id, demande_id (FK, index avec cree_le), contact_id, type ENUM('appel_sortant','appel_entrant','sms','email_sortant','email_entrant','note','visite','relance_auto','systeme'), resultat ENUM('abouti','pas_de_reponse','message_laisse','numero_errone') NULL, contenu TEXT NULL, auteur_id NULL (NULL = système), origine ENUM('admin','lien_un_clic','n8n','site'), cree_le.

**visite** : id, demande_id, prevue_le DATETIME, duree_min, adresse VARCHAR NULL, associe_id, statut ENUM('planifiee','faite','annulee','reportee'), compte_rendu TEXT NULL, cree_le.

**offre**

| Champ | Type | Note |
|---|---|---|
| id | INT PK | |
| demande_id | INT FK | |
| numero | VARCHAR(30) | numéro du logiciel d'offres du client |
| version | TINYINT | |
| montant_ht | DECIMAL(10,2) | obligatoire |
| envoyee_le | DATE | index |
| statut | ENUM('envoyee','signee','perdue','remplacee') | |
| relance_etape | TINYINT | 0 à 3 (J+3, J+10, J+21) |
| derniere_relance_le | DATE NULL | |
| signee_le | DATE NULL | index |
| montant_signe_ht | DECIMAL(10,2) NULL | peut différer de l'offre |
| fichier_id | INT FK NULL | PDF de l'offre |

**chantier** : id, demande_id, offre_id, statut ENUM('a_planifier','planifie','en_cours','termine','clos'), debut_prevu, fin_prevue, jours_equipe_estimes DECIMAL(5,1), receptionne_le, reserves_levees_le, litige BOOL, avis_demande_le, avis_relance_le, accord_photos ENUM('photos_sans_nom','avec_commune','temoignage','refuse') NULL, accord_photos_le, garantie_sia118 BOOL, entretien_envoye_le.

**avis** : id, source ENUM('google'), id_externe UNIQUE, auteur_affiche VARCHAR(100), note TINYINT, texte TEXT, publie_le, chantier_id FK NULL (rapprochement), reponse_brouillon TEXT, reponse_publiee_le, repondu_par.

**fichier** : id, demande_id, nom_original, chemin (relatif au dossier privé), type_mime, taille, sha256, origine ENUM('formulaire','admin','n8n'), cree_le, supprime_le.

**campagne** : id, canal_marketing, plateforme, identifiant_externe (campaignid), utm_campaign, nom, debut, fin. Fait le lien entre `{campaignid}` des UTM Google Ads (v2 §6.2) et un nom lisible.

**depense**

| Champ | Type | Note |
|---|---|---|
| id | INT PK | |
| mois | DATE | 1er jour du mois ; index avec canal |
| canal_marketing | VARCHAR(30) | |
| campagne_id | INT FK NULL | |
| montant_ht | DECIMAL(10,2) | |
| origine | ENUM('saisie','google_ads','import') | Google Ads : verrouillé à la saisie |
| type_cout | ENUM('media','courrier','impression','honoraires','outil') | permet d'inclure ou non les honoraires (G5) |
| saisi_par, saisi_le | | |
| UNIQUE | (mois, canal_marketing, campagne_id, type_cout, origine) | |

**objectif** : id, indicateur (code du §5.2), mois DATE, valeur DECIMAL, sens ENUM('min','max'), scenario ENUM('S','M','L'), source VARCHAR (« v2 §1.1 » ou « interpolé »), modifie_par.

**parametre** : cle VARCHAR PK, valeur JSON, modifie_par, modifie_le. Clés : `marge_brute` (global et par service), `panier_reference`, `honoraires_inclus`, `equipes`, `seuil_carnet_semaines`, `heures_ouvrables`, `fermetures`, `grille_scoring_version`.

**motif_perte** : id, code, libelle, relance_6_mois BOOL, ordre, actif.

**metrique_externe** (agrégats, aucune donnée personnelle) : date, source ENUM('umami','search_console','places','business_profile','google_ads'), metrique (`visites`, `contacts_web`, `formulaire_envoye`, `appel_clic`, `email_clic`, `whatsapp_clic`, `clics`, `impressions`, `position`, `appels`, `itineraires`, `note`, `nb_avis`, `cout`, `clics_annonces`), dimension VARCHAR NULL (page, requête, campagne), valeur DECIMAL ; UNIQUE (date, source, metrique, dimension).

**citation_ia** : id, mois, question_no (1 à 10), question, assistant, cite BOOL, rang NULL, url_citee NULL, saisi_par.

**conversion_ads** (V3) : id, demande_id, offre_id, action ENUM('demande_qualifiee','chantier_signe'), gclid, converti_le, valeur, devise, statut ENUM('a_envoyer','envoyee','refusee','trop_ancienne','sans_gclid'), envoyee_le, erreur.

**journal_audit** : id, quand DATETIME(3), utilisateur_id NULL, acteur ENUM('utilisateur','n8n','site','systeme'), action (connexion, connexion_echec, 2fa_reinitialisee, consultation_fiche, modification, changement_statut, export, effacement, purge, parametre, depense…), objet_type, objet_id, details JSON (noms des champs modifiés, **jamais les valeurs personnelles**), ip_tronquee, appareil_id. L'utilisateur MariaDB de l'application n'a que `INSERT` et `SELECT` sur cette table.

**demande_droits** : id, recue_le, type ENUM('acces','rectification','effacement','opposition'), canal, contact_id NULL, identite_verifiee_le, echeance (recue + 30 jours), traite_le, traite_par, reponse.

**opposition** : empreinte CHAR(64) PK (HMAC de l'e-mail ou du téléphone normalisé), type, cree_le. Sert à respecter un refus sans garder l'adresse en clair (v2 §7.5).

**jeton_action** : jeton_hash PK, demande_id, action, expire_le, utilise_le.

**V2, prospection et marchés publics** : `compte_b2b` (organisation, palier, étape de la séquence en 4 touches, prochaine action) et `marche_public` (référence simap, adjudicateur, CFC, délais, décision). Détail à écrire avec le module.

### 4.3 Index

| Table | Index | Sert à |
|---|---|---|
| demande | (statut, echeance_le) | À traiter, horloge WF03 |
| demande | (recue_le), (priorite, recue_le) | indicateurs mensuels |
| demande | (associe_id, statut) | « Mes demandes » |
| contact | (email_normalise), (telephone_e164) | doublons, recherche, droits des personnes |
| attribution | (canal_marketing), (gclid) | Acquisition, import Google Ads |
| offre | (statut, envoyee_le), (signee_le) | relances, taux offre→signée, CA signé |
| chantier | (statut), (fin_prevue) | capacité, avis |
| interaction | (demande_id, cree_le) | historique |
| depense | (mois, canal_marketing) | CPL, CAC |
| metrique_externe | (source, metrique, date) | Vue d'ensemble, SEO |
| journal_audit | (quand), (objet_type, objet_id), (utilisateur_id, quand) | journal |
| Recherche | FULLTEXT (contact.nom, contact.prenom, organisation.nom, demande.commune) | recherche globale |

### 4.4 Statuts

| Objet | Statuts |
|---|---|
| Demande | Nouvelle → Contact établi → Visite planifiée → Offre envoyée → **Signée** ou **Perdue** ; à part : Hors cible, Doublon |
| Offre | Envoyée (relance 0 à 3) → Signée, Perdue ou Remplacée (nouvelle version) |
| Chantier | À planifier → Planifié → En cours → Terminé (réception ; réserves levées) → Clos (avis reçu, ou 30 jours après la relance) ; Litige suspend la demande d'avis |
| Avis | Non rapproché → Rapproché d'un chantier ; réponse : à rédiger → brouillon → publiée |

### 4.5 Transitions autorisées de la demande

| De | Vers | Déclencheur | Qui | Condition | Effets |
|---|---|---|---|---|---|
| — | Nouvelle | Formulaire, saisie d'un appel | Site, associé, secrétariat | Validation de l'API | Score, échéance, e-mail interne, webhook (SMS A et B) |
| Nouvelle | Nouvelle | « Pas de réponse » | Associé, secrétariat, lien en un clic | Moins de 3 tentatives | Tentative + 1 ; au 1er essai, message au prospect ; nouvelle échéance le lendemain 10 h |
| Nouvelle | Contact établi | « J'ai eu la personne » | Idem | — | `premier_contact_le` ; arrête l'escalade |
| Nouvelle | Perdue | 3e « Pas de réponse » en 5 jours ouvrables | Automatique (n8n) | — | Motif « sans réponse », e-mail de clôture, pas de relance à 6 mois |
| Nouvelle | Hors cible | « Hors cible » | Associé | — | Réponse de réorientation proposée, envoyée par l'associé |
| Nouvelle | Doublon | Fusion | Associé ; automatique si même e-mail ou téléphone et demande ouverte de moins de 30 jours | — | Historique déplacé ; pas de SMS ; exclue des comptes |
| Contact établi | Visite planifiée | Visite créée | Associé, secrétariat | Date | Rappel la veille (n8n) |
| Contact établi, Visite planifiée | Offre envoyée | « Envoyer l'offre » | Associé, secrétariat | Montant > 0, date | Relances J+3, J+10, J+21 (WF03c) |
| Visite planifiée | Contact établi | Visite annulée | Idem | — | — |
| Offre envoyée | Offre envoyée | Nouvelle version | Idem | — | Ancienne offre « remplacée » ; les relances continuent |
| Offre envoyée | Signée | « Marquer signée » | Idem | Date et montant signé | Chantier « à planifier » ; conversion Google Ads (V3) |
| Contact établi, Visite planifiée, Offre envoyée | Perdue | « Marquer perdue », lien J+21, J+45 automatique | Associé, secrétariat, n8n | **Motif obligatoire** | Relance à 6 mois si le motif et l'accord le permettent |
| Perdue, Hors cible | Nouvelle | « Rouvrir » | Associé | Moins de 90 jours ; sinon nouvelle demande liée | Journalisé |
| Signée | Perdue | Annulation | Associé | Motif « annulé après signature » | Chantier clos |

Toute autre transition est refusée par le serveur (pas seulement masquée dans l'interface). Chaque transition écrit une ligne dans `interaction` et une dans `journal_audit`.

### 4.6 Conservation et purge

| Données | Durée | Mécanisme |
|---|---|---|
| Demande sans suite (perdue, hors cible, sans réponse) | 24 mois après le dernier contact (v2 §8) | Purge quotidienne : le contact est effacé ; la demande est **anonymisée** (gardés : date, canal, priorité, statut, montants, zone ; effacés : nom, coordonnées, message, commune exacte, notes, fichiers, `gclid`) |
| Client (signée) | 5 ans après la réception (CO 371), puis revue | Liste de revue dans Journal et données personnelles |
| Pièces comptables (offres signées, factures) | 10 ans (CO 958f) | Hors de l'admin (logiciel comptable) ; l'admin garde le montant |
| Fichiers reçus | Avec la demande | Effacés avec elle |
| `gclid` | Jusqu'à l'envoi à Google Ads, au plus 90 jours | Effacé par la purge |
| Journal d'audit | 12 mois | Purge mensuelle |
| Appareils révoqués ou expirés | 90 jours | Purge |
| Jetons d'action | À expiration | Purge |
| Agrégats externes | 3 ans | Aucune donnée personnelle |
| Registre des droits des personnes | 3 ans | Preuve de traitement |
| Liste d'opposition | Tant que nécessaire | Empreintes seulement |
| Sauvegardes | 30 jours | Rotation ; un effacement est donc complet au plus tard 30 jours après (à dire dans la politique) |

---

## 5. Dictionnaire des indicateurs

Noms **partagés** avec le plan d'acquisition v4. Objectifs : `strategie-acquisition.md` §1.1 (scénario M) et §1.3.

### 5.1 Étapes de l'entonnoir

| Étape | Définition | Où c'est enregistré | Source |
|---|---|---|---|
| **visite** | Session sur le site, hors préproduction ; rien n'est mesuré si Do Not Track ou GPC | `metrique_externe` (`visites`) | Umami |
| **contact web** | Formulaire envoyé (`formulaire_envoye`, réponse `ok` avec une référence), clic tél. (`appel_clic`), clic e-mail (`email_clic`), clic WhatsApp (`whatsapp_clic`) | `metrique_externe` | Umami (contrat §12.3) |
| **demande enregistrée** | Ligne `demande` créée, **tous canaux** (site, appel saisi, e-mail saisi, recommandation, B2B), hors spam, doublons, tests (`mode_test`) et demandes effacées sans trace | `demande.recue_le` | Base |
| **qualifiée** | Demande enregistrée classée **A, B ou C** par le scoring (hors cible exclue). Si un associé corrige la priorité, la priorité corrigée fait foi | `priorite_corrigee` sinon `priorite` | Base |
| **visite planifiée** | Une visite sur place a une date (planifiée ou faite) | `visite.prevue_le` | Base |
| **offre envoyée** | Offre saisie avec son montant HT en CHF et sa date d'envoi | `offre.envoyee_le`, `montant_ht` | Base |
| **signée** | Offre acceptée : date et montant signé | `offre.signee_le`, `montant_signe_ht` | Base |
| **perdue** | Demande close sans signature, avec un **motif** (prix, délai, reporté, attribué ailleurs, sans réponse, hors cible, trop petit, autre) | `demande.perdue_le`, `motif_perte_id` | Base |
| **chantier terminé** | Réception faite et réserves levées | `chantier.receptionne_le`, `reserves_levees_le` | Base |
| **avis demandé** | Demande d'avis envoyée (J+2) | `chantier.avis_demande_le` | n8n → base |
| **avis reçu** | Avis publié sur la fiche Google et rapproché du chantier | `avis.chantier_id` | Associé (V2), API (V3) |

### 5.2 Indicateurs

| Indicateur | Formule exacte | Source | Mise à jour | Objectif M3 / M6 / M12 |
|---|---|---|---|---|
| **visites** | Somme des sessions Umami de la période | Umami (API) | Quotidienne (veille) | 500 / 900 / 1'500 par mois |
| **taux visite→contact** | contacts web / visites, même période | Umami | Quotidienne | 2,0 % / 2,5 % / 3,0 % (contacts web : 10 / 22 / 45) |
| **demandes/mois** | Nombre de demandes enregistrées dont `recue_le` (heure de Zurich) tombe dans le mois civil | Base | Temps réel | 10 / 18 / 30 |
| **part A+B** | (demandes A + demandes B) / demandes qualifiées (A + B + C), même période | Base | Temps réel | ≥ 50 % / ≥ 60 % / ≥ 65 % |
| **délai de premier contact (médiane, heures ouvrables)** | Médiane de (`premier_contact_le` − `recue_le`) en heures ouvrables, sur les demandes **A** de la période qui ont eu un premier contact. **Les demandes arrivées par un appel entrant sont exclues** (le contact est immédiat, elles flatteraient la médiane). Affiché aussi pour B, C et toutes priorités. Complément : **part rappelée dans le délai** = demandes dont le premier appel (abouti ou non) a eu lieu avant l'échéance / demandes dont l'échéance est passée ; une demande en attente compte comme hors délai dès son échéance (même règle que l'escalade de WF03) | Base | Temps réel | Demandes A : < 4 h / < 2 h / < 2 h |
| **taux demande→offre** | Offres envoyées pendant le mois M / demandes enregistrées pendant le mois M−1 (définition v2 §1.1). Une nouvelle version d'offre ne compte pas | Base | Temps réel | 55 % / 60 % / 65 % |
| **taux offre→signée** | Offres signées / offres envoyées, sur la **cohorte des offres envoyées depuis plus de 60 jours** (v2 §1.1) ; l'admin prend les offres envoyées entre J−180 et J−60 | Base | Quotidienne | 25 % / 28 % / 30 % |
| **CA signé** | Somme de `montant_signe_ht` des offres signées pendant la période (date de signature) | Base | Temps réel | Pas d'objectif en v2. Proposé : chantiers signés visés (≈ 1-2 / 3 / 6 par mois) × panier de référence (à fixer, G4) |
| **panier moyen** | CA signé / nombre de chantiers signés, sur 6 mois glissants (petits nombres) ; aussi par type de client | Base | Quotidienne | Pas d'objectif ; sert au CPL max |
| **dépense par canal** | Somme des dépenses du canal et du mois, HT ; médias, courrier et impression ; honoraires d'agence seulement si G5 = oui | Google Ads (import), saisie (autres) | Quotidienne (Google Ads), mensuelle (saisie) | Budget du scénario M (v2 §8.3) : Google Ads 1'200, Meta 150 (lissé), courrier 80 |
| **CPL** | dépense / demandes (demandes enregistrées du même canal et de la même période) | Calcul | Avec ses deux termes | CPL ≤ 1/3 du CPL max ; **CPL max = panier moyen × marge brute × taux demande→offre × taux offre→signée** (plan d'acquisition v4 §2.5, qui corrige v2 §1.3) |
| **CAC** | dépense / chantiers signés (signés pendant la période, rattachés au canal d'origine de la demande) | Calcul | Idem | Seuil d'équilibre : CAC < marge brute moyenne par chantier |
| **ROAS** | CA signé / dépense | Calcul | Idem | Seuil d'équilibre : 1 / taux de marge brute (ex. 3,3 avec 30 %, *illustratif*) |
| **ROI** | (marge brute − dépense) / dépense, avec marge brute = CA signé × taux de marge brute (paramètre, par service si connu) | Calcul | Idem | > 0 |
| **part des canaux** | Demandes du canal / demandes totales ; affichée aussi en CA signé | Base | Temps réel | Pas d'objectif ; suivi de la dépendance à un canal |
| **avis Google (nombre, note)** | Nombre cumulé d'avis publiés et note moyenne affichée par Google | Places API (V2), Business Profile API (V3) | Quotidienne | 15 / 30 / 50 (cumul) ; note : suivie, jamais pilotée |
| **clics et positions Search Console** | Clics, impressions, CTR, position moyenne (28 jours glissants et mois civil), par requête et par page ; suivi des 30 requêtes cibles | Search Console API | Quotidienne (données à J−2 ou J−3) | Pas d'objectif en v2 ; à fixer avec le plan SEO |
| **appels et itinéraires de la fiche Google** | Clics « Appeler » et demandes d'itinéraire depuis la fiche, par mois | Business Profile Performance API (V3) ; **saisie mensuelle** en attendant | Mensuelle | Pas d'objectif en v2 |
| **citations IA** | Nombre de questions, sur les 10 du test mensuel (`analyse-marche.md` §6), pour lesquelles Andy Construct est cité ; assistants testés listés | Saisie (agence) | Mensuelle | 1/10 / 3/10 / 5/10 |

### 5.3 Règles communes

1. **Période** : mois civil, heure de Zurich. Le mois en cours est arrêté à l'instant. Les nombres ont une projection de fin de mois ; les taux et médianes n'en ont pas.
2. **Objectif du mois** : M3, M6 et M12 viennent de la v2 ; entre deux jalons, interpolation linéaire, arrondie (décision G6). Avant M3 : pas d'objectif affiché.
3. **Attribution** : une demande a **un** canal (§5.4), celui de son arrivée. Le CA signé et les chantiers signés sont rattachés au canal d'origine de la demande, à la date de signature.
4. **Petits nombres** : Acquisition s'ouvre sur 3 mois. Sous 3 chantiers signés, CAC, ROAS et ROI portent la mention « indicatif ». Sous 5 cas, un taux s'affiche avec ses deux termes (« 2 sur 4 »).
5. **Exclus partout** : demandes de test, doublons, spam. Les demandes anonymisées restent comptées.
6. **Divisions par zéro** : affichées « — » avec la raison au survol (« aucune dépense », « aucun chantier signé »).
7. **Un chiffre du rapport mensuel est figé** à sa production ; une correction ultérieure est signalée, pas réécrite.

### 5.4 Canaux (regroupement des catégories de `Source.php`)

| Canal affiché | Catégories `Source.php` | Dépense rattachée |
|---|---|---|
| Google Ads | `google-ads` (y compris `bing / cpc`, détaillé par `utm_source`) | Google Ads, Microsoft Ads |
| Recherche Google | `recherche-google` | — |
| Fiche Google | `carte-google` | — |
| Meta | `meta` | Meta Ads |
| LinkedIn | `linkedin` | LinkedIn (sponsorisé) |
| Prospection B2B | `b2b` | Courrier, impression de la plaquette |
| Recommandation et partenaires | `recommandation`, `partenaire` | Cartes de recommandation |
| Clients existants | `client-existant`, `crm` | — |
| Guides | `aimant` | Impression et envoi des guides |
| Annuaires et plateformes | `annuaire`, `plateforme` | Abonnements éventuels |
| Panneaux et véhicules | `panneau-vehicule` | Panneaux |
| Autres et inconnu | `site-referent`, `autre`, `direct-inconnu` | — |

**Appels saisis** : `Source.php` renvoie `appel-direct` ; l'admin prend le canal de la réponse « Comment nous avez-vous connus ? » (même table que `scoring.json` → `connu_par`). Même règle pour une demande web en `direct-inconnu` dont le « connu par » est rempli. Le canal ainsi déduit porte la mention « déclaré ».

---

## 6. Intégrations, notifications, sécurité, mobile

### 6.1 Intégrations

| Source | API ou moyen | Données (agrégats) | Fréquence | Automatique ou saisi | Accès à obtenir | Phase |
|---|---|---|---|---|---|---|
| Site (formulaires) | `demande.php` → base | Demandes, attribution, fichiers | Temps réel | Automatique | — | MVP |
| Saisie d'un appel | Admin | Demandes par téléphone | Temps réel | Saisi | — | MVP |
| n8n | API interne HMAC (§6.3) | Événements (SMS, relances, réponses, oppositions) | Temps réel et toutes les 15 min | Automatique | Secret partagé | MVP |
| Umami | API (déjà dans WF09) | Visites, contacts web par type, pages d'entrée | Quotidienne | Automatique (n8n) | Jeton d'API | V2 |
| Google Search Console | Search Analytics API (OAuth) | Clics, impressions, CTR, position par requête et page | Quotidienne | Automatique (n8n) | Compte de service ou OAuth | V2 |
| Google Places | Places API (déjà dans WF09) | Note, nombre d'avis | Quotidienne | Automatique (n8n) | Clé restreinte | V2 |
| Google Business Profile | Performance API, Reviews (Business Profile APIs) | Appels, itinéraires, clics ; avis complets et réponses | Quotidienne | Automatique | **Demande d'accès à Google** (délai et acceptation *à vérifier*) ; en attendant : saisie mensuelle | V3 |
| Google Ads, coûts | Rapport programmé par e-mail (CSV) lu par n8n, ou Google Ads API | Coût, clics, impressions par campagne et jour | Quotidienne | Automatique | Rapport programmé (aucun accès développeur) ; API : jeton développeur | V2 |
| Google Ads, conversions | Voir §6.2 | `gclid`, date, valeur | Quotidienne | Automatique | Action de conversion « importée » ; API ou import planifié | V3 |
| Meta, LinkedIn, courrier | — | Dépense du mois | Mensuelle | **Saisie** (agence) | — | MVP |
| Citations IA | — | Test des 10 questions | Mensuelle | **Saisie** (agence) | — | V2 |
| Logiciel d'offres (bexio ou autre, si utilisé) | API de l'outil | Offres envoyées et acceptées | Quotidienne | Automatique | À demander au client (v2 §5.3) | V3 |

### 6.2 Import des chantiers signés dans Google Ads (conversions hors ligne)

1. **Capture** : `suivi.js` garde le `gclid` **seulement** si la personne a accepté la mesure publicitaire (`consent_ads=accorde`) ; l'API l'ignore sinon (contrat §3). Il est stocké dans `attribution.gclid`.
2. **Création** : au passage à « Signée », l'admin crée une ligne `conversion_ads` (action « chantier signé », date de signature, valeur = montant signé, CHF). Sans `gclid` : statut `sans_gclid`, rien n'est envoyé.
3. **Envoi** : une fois par jour, au moins 6 heures après le clic. Deux voies, à choisir en V3 selon l'accès obtenu : l'API Google Ads (téléversement des conversions de clics, jeton développeur nécessaire), ou un import planifié de fichier dans Google Ads (Google Sheets ou HTTPS, *à vérifier dans le compte*). Le statut de chaque envoi est visible dans Acquisition.
4. **Limite de 90 jours** : Google n'accepte pas un clic de plus de 90 jours. Un chantier signé plus tard (cycle de vente long) est marqué `trop_ancienne`. Pour garder un signal, une seconde action **« demande qualifiée »** (A ou B, envoyée dans les jours qui suivent) est proposée.
5. **Volume** : avec ≈ 6 chantiers signés par mois à M12, toutes sources confondues, l'enchère sur le ROAS (15 conversions en 30 jours au minimum) est hors de portée. Les deux actions sont créées en **secondaires** : elles servent au rapport (quelle campagne amène des chantiers), pas à l'enchère. On réévalue à M12.
6. **Ce qui part chez Google** : un identifiant de clic, une date, un montant. Aucun nom, e-mail ni téléphone. Les « conversions améliorées pour les prospects » (e-mail ou téléphone hachés) ne sont **pas** activées sans décision du client et avis du juriste (G7).
7. **Vérification** (à faire en V3) : une conversion de test, puis contrôle dans Google Ads, Objectifs, Conversions, Importations, que le fichier est accepté sans erreur ; contrôle de bout en bout sur un vrai clic d'annonce (un `gclid` inventé ne prouve que le transport).

### 6.3 API interne pour n8n

Signature HMAC-SHA256 sur `horodatage.corps` (même schéma que le webhook, ± 5 min), secret distinct, liste d'adresses IP du VPS si l'hébergeur le permet, droits par point d'entrée, chaque appel journalisé (acteur `n8n`).

| Point d'entrée | Utilisé par | Remplace |
|---|---|---|
| `GET /interne/demandes/{ref}` | WF01 (texte du SMS), WF02 | Lecture d'affaire Pipedrive |
| `POST /interne/actions` (`contact-etabli`, `pas-de-reponse`, `hors-cible`, `reorientation-envoyee`, `reponse-j21`, `reserves-levees`, `avis-recu`) | WF02, page « en un clic » | Mise à jour d'affaire |
| `GET /interne/echeances?type=rappel\|relance_offre\|avis\|offre_perdue_6_mois\|entretien` | WF03, WF03c, WF03d, WF04e, WF04i | Filtres enregistrés Pipedrive |
| `POST /interne/evenements` (`sms_envoye`, `email_envoye`, `relance_envoyee`, `reponse_detectee`, `erreur`) | Tous | Notes Pipedrive |
| `POST /interne/opposition` | WF12, WF14 | Champ `opposition_marketing` |
| `POST /interne/metriques`, `POST /interne/depenses` | Lecteurs quotidiens (V2) | Feuille « KPI » |
| `GET /interne/rapports/{mois}` | WF09 (envoi du lien) | Calcul dans n8n |
| `GET /interne/conversions-ads`, `POST /interne/conversions-ads/{id}` | Envoi Google Ads (V3) | — |

### 6.4 Notifications

Règle : **un événement, un message par personne et par canal.** n8n envoie les SMS et les e-mails métier ; le PHP envoie l'e-mail interne d'une nouvelle demande et les e-mails de sécurité ; l'admin affiche des pastilles et des listes, il n'envoie pas de SMS.

| Événement | Associé attribué | Autre associé | Secrétariat | Agence | Émetteur |
|---|---|---|---|---|---|
| Nouvelle demande A ou B (7 h-20 h ; samedi : A seulement ; dimanche : rien) | SMS + e-mail | E-mail | E-mail | — | PHP (e-mail), n8n (SMS) |
| Nouvelle demande C, hors cible | E-mail ; récapitulatif de 17 h 30 | Récapitulatif | Récapitulatif | — | PHP, n8n |
| Échéance dépassée | SMS à l'échéance | SMS et e-mail à +1 h (A) ou +4 h (B) | — | — | n8n (WF03) |
| Offre : appel J+10, décision J+35 | À traiter + récapitulatif du lundi | Récapitulatif | Récapitulatif | — | Admin, n8n |
| Nouvel avis | À traiter | — | — | E-mail (brouillon de réponse) | n8n |
| Rapport mensuel prêt | E-mail avec lien | E-mail | — | E-mail avec lien | n8n |
| Connexion depuis un nouvel appareil, 2FA modifiée | E-mail à l'utilisateur concerné | — | — | — | Admin (PHP) |
| Intégration en erreur, base indisponible | — | — | — | E-mail et SMS (technique) | n8n (WF13), `cron.php` |

Notifications push du navigateur : non prévues dans le MVP ; option en V3, et seulement si elles **remplacent** un SMS (jamais en plus).

### 6.5 Sécurité

**Rôles et droits**

| Droit | Associé | Secrétariat | Agence marketing | Agence technique |
|---|---|---|---|---|
| À traiter, Demandes, fiches, recherche | oui | oui | — | — |
| Saisir, changer un statut, noter, planifier, offres | oui | oui | — | — |
| Corriger une priorité ou un canal | oui | oui (journalisé) | — | — |
| Vue d'ensemble | oui | oui | sans noms | — |
| Acquisition, SEO et visibilité, Avis, Rapport | oui | oui | oui | — |
| Saisir dépenses, citations IA, brouillons de réponse | oui | — | oui | — |
| Exporter (CSV, une personne) | oui | — | — | — |
| Effacer, gérer la purge | oui | — | — | — |
| Paramètres (objectifs, économie, motifs, zones, scoring) | oui | lecture | lecture des objectifs | — |
| Utilisateurs et rôles | oui | — | — | — |
| Journal d'audit | oui | ses actions | — | technique, sans contenu |
| État des intégrations | oui | — | oui | oui |

Les droits sont vérifiés **côté serveur, sur chaque route** ; un test automatique appelle chaque route avec chaque rôle et vérifie qu'aucune réponse destinée à l'agence ne contient de nom, téléphone, e-mail, message ou commune exacte.

**Mesures**

| Domaine | Mesure |
|---|---|
| Mot de passe | 12 caractères au moins, comparé à une liste locale de mots de passe compromis ; haché en argon2id |
| Double authentification | **Obligatoire** : application d'authentification (TOTP) et 10 codes de secours. Clés d'accès (passkeys, Face ID) en V2 : plus simples au téléphone |
| Appareil de confiance | 30 jours sans code 2FA ; liste des appareils et révocation dans Mon compte |
| Session | Cookie `__Host-`, `Secure`, `HttpOnly`, `SameSite=Lax` (un lien ouvert depuis un SMS garde la session) ; identifiant renouvelé à la connexion ; fin après 8 h d'inactivité ; mot de passe redemandé après 7 jours même sur un appareil de confiance |
| Essais | 5 échecs : compte bloqué 15 minutes et e-mail à l'utilisateur ; délai croissant par adresse IP |
| Mot de passe oublié | Lien par e-mail (30 minutes) **et** code 2FA ; sinon réinitialisation par l'autre associé |
| Protections web | Jeton CSRF sur tout envoi ; CSP stricte (`default-src 'self'`, aucun script en ligne, `frame-ancestors 'none'`) ; HSTS ; `nosniff` ; `Referrer-Policy: no-referrer` ; `Cache-Control: no-store` sur toute page avec des données personnelles ; `X-Robots-Tag: noindex` ; requêtes SQL préparées ; échappement à l'affichage ; téléversements contrôlés par `Televersement.php` ; limite de débit sur la recherche et l'export |
| Fichiers | Hors racine web ; servis par un contrôleur authentifié, `Content-Disposition: attachment` |
| Base | Deux utilisateurs MariaDB : application (sans droit de modifier le schéma ni d'effacer le journal) et migrations ; mot de passe dans `config.php` (hors dépôt) |
| Journal d'audit | Connexions, échecs, consultations de fiche, modifications (noms des champs), exports, effacements, paramètres ; 12 mois ; sans valeur personnelle |
| Sauvegardes | Copie quotidienne chiffrée de la base et des fichiers vers le VPS Infomaniak (Suisse), 30 jours ; **test de restauration** à la mise en service puis chaque trimestre |
| Hébergement | Suisse ; contrats de sous-traitance (hébergeur, Infomaniak, agence) ; accès de l'agence au serveur nominatif et journalisé |
| Mises à jour | PHP et bibliothèques : correctifs de sécurité sous 7 jours ; revue trimestrielle |
| Avant la mise en ligne | Revue de code orientée sécurité, analyse automatique (OWASP ZAP en mode « baseline »), test des droits par rôle, test de restauration |
| Incident | Procédure de `automatisation.md` §7.7 (évaluation sous 24 h, annonce au PFPDT si risque élevé) |

### 6.6 Mobile

| Règle | Détail |
|---|---|
| Écrans prioritaires | À traiter, Fiche demande, Saisie d'un appel : complets à 360-390 px. Les autres sont lisibles, sans plus |
| Gestes | Cibles de 44 px au moins ; actions principales en bas de l'écran, à portée du pouce |
| Appel | Lien `tel:` ; au retour dans l'onglet, la feuille « Résultat de l'appel » s'ouvre (événement `visibilitychange`) |
| Saisie | Champs en 16 px (pas de zoom automatique sur iPhone) ; `inputmode` et `autocomplete` ; boutons plutôt que listes |
| Hors connexion | Message clair ; l'action reste prête à renvoyer ; aucune donnée personnelle mise en cache (pas de service worker qui stocke des réponses) |
| Performance | HTML rendu par le serveur, peu de JavaScript ; À traiter affiché en moins d'une seconde en 4G ; moins de 100 Ko par page hors fichiers |
| Écran d'accueil | Manifeste et icône (V2) pour l'ouvrir comme une application ; pas d'application native |
| Lisibilité | Contraste AA ; texte de 15 px au moins ; mode sombre suivant le réglage du téléphone |

**Choix techniques** : PHP 8 rendu côté serveur, quelques modules JavaScript sans framework, CSS à jetons de la charte, graphiques en SVG produits par le serveur. Aucun outil de compilation, comme le reste du dépôt. Bibliothèques : PHPMailer (déjà là), une bibliothèque TOTP et, en V2, une bibliothèque WebAuthn (*à choisir et auditer*).

---

## 7. Feuille de route

### 7.1 Phases

**Phase 0, avant le développement (1 à 2 semaines, client et agence)** : décisions G1 à G14 ; vérification de l'hébergement ; contrats de sous-traitance ; données du client pour calibrer (marge, panier, capacité, v2 §1.2).

**MVP ≈ 20 jours** *(estimation à valider ; 4 à 5 semaines calendaires avec une personne)*

| Lot | Contenu | Jours |
|---|---|---|
| 1. Socle | Sous-domaine, routeur, gabarits, charte, composants, en-têtes de sécurité | 1,5 |
| 2. Comptes | Connexion, argon2id, TOTP, codes de secours, appareils, rôles, blocage | 2 |
| 3. Base | Schéma, migrations, `Depot` dans `Traitement`, file de reprise, déplacement des fichiers, import du tableur | 1,5 |
| 4. À traiter et Demandes | Liste, colonnes, filtres, recherche | 2,5 |
| 5. Fiche demande | Blocs, historique, actions, transitions vérifiées par le serveur | 3 |
| 6. Saisie d'un appel | Formulaire, score en direct, passage par `Traitement` | 0,5 |
| 7. Vue d'ensemble | 5 indicateurs, entonnoir, alertes, capacité ; paramètres objectifs, dépenses, économie | 2 |
| 8. API interne et n8n | Points d'entrée HMAC, adaptation des 14 workflows, suppression de WF06, `verifier.py` | 3 |
| 9. Données personnelles | Export, effacement par anonymisation, purge, journal d'audit, registre des droits | 1,5 |
| 10. Qualité et mise en service | Tests automatiques (droits par rôle, calculs du §5), recette, revue de sécurité, sauvegardes et test de restauration, formation d'une heure | 2,5 |
| **Total** | | **20** |

**V2 ≈ 13 jours** (deux mois après le MVP, sur l'usage réel)

| Lot | Jours |
|---|---|
| Acquisition (canaux, CPL, CAC, ROAS, ROI, tendances) | 2 |
| Lectures quotidiennes : Umami, Search Console, Places, coûts Google Ads | 3 |
| SEO et visibilité (dont la grille des citations IA) | 1,5 |
| Avis (liste, rapprochement, brouillons) | 1 |
| Rapport mensuel figé, commentaire, PDF | 1,5 |
| Offres et chantiers, capacité détaillée | 1 |
| Prospection B2B et marchés publics (WF07, WF08, WF10 adaptés) | 2 |
| Clés d'accès (passkeys), manifeste d'écran d'accueil | 1 |

**V3 ≈ 8 jours** (quand le volume le justifie)

| Lot | Jours |
|---|---|
| Import des conversions hors ligne dans Google Ads (§6.2) | 2 |
| Business Profile : avis complets, réponses publiées depuis l'admin, appels et itinéraires | 2 |
| Recalibrage du score : résultat par tranche de score, simulation d'une nouvelle grille (v2 §2.7) | 1,5 |
| Synchronisation des offres avec le logiciel d'offres du client, s'il en a un | 2 |
| Notifications push, si elles remplacent des SMS | 0,5 |

### 7.2 Critères d'acceptation du MVP

Chaque critère se vérifie par un test écrit (automatique quand c'est possible) :

1. Une demande envoyée depuis le site apparaît dans À traiter **en moins de 10 secondes**, avec le **même score, la même priorité et la même échéance** que l'e-mail interne.
2. Base arrêtée pendant un envoi : l'e-mail interne part, la demande est insérée par `cron.php` au retour de la base, sans doublon.
3. Au téléphone (390 px), du lien du SMS au résultat « J'ai eu la personne » : **3 gestes au plus**, sans saisie.
4. Saisie d'un appel complète en **30 secondes** au plus (chronométrée avec les deux associés).
5. Les 5 indicateurs de la vue d'ensemble sont égaux au calcul de référence sur un jeu de 60 demandes datées (dont jours fériés, week-ends, demandes reçues à 17 h 55, offres sur deux mois, doublons et tests exclus).
6. Les transitions interdites (§4.5) sont refusées par le serveur ; « Perdue » sans motif et « Signée » sans montant sont impossibles.
7. Rôle agence marketing : **aucune** route ne renvoie de nom, téléphone, e-mail, message ou commune exacte (test sur toutes les routes).
8. 2FA obligatoire ; 5 échecs bloquent le compte 15 minutes ; une session inactive depuis 8 heures est fermée.
9. Export d'une personne et effacement en moins de 2 minutes chacun ; après effacement, les indicateurs du mois ne changent pas ; les deux actions figurent au journal.
10. Purge à 24 mois vérifiée sur des données antidatées.
11. Restauration de la sauvegarde de la veille réussie sur un environnement de test.
12. Workflows n8n adaptés : `verifier.py` sans erreur et les 20 cas de recette de `automatisation.md` §6.2 réussis contre l'admin.
13. Écrans du MVP : aucune violation axe, aucune erreur de console, aucun défilement horizontal à 390 et 1440 px.

### 7.3 Risques

| Risque | Effet | Parade |
|---|---|---|
| Hébergement sans MariaDB ou PHP 8.1, ou hors de Suisse | Option A bloquée | Vérifier en phase 0 ; variante A′ sur le VPS |
| Faille de sécurité | Fuite de données personnelles | 2FA, rôles vérifiés côté serveur, tests, revue, mises à jour sous 7 jours, journal, sauvegardes, procédure d'incident |
| Admin en panne | Les associés n'ont plus la liste | L'e-mail interne part toujours ; les liens en un clic attendent en file ; page d'état |
| Les associés n'ouvrent pas l'admin | Données incomplètes, indicateurs faux | SMS et liens en un clic, 3 gestes, saisie en 30 s, formation, revue des données le lundi |
| Statuts non mis à jour (offre envoyée, signée) | Taux faux | Alerte « offre envoyée sans montant », rappel dans le récapitulatif du lundi, contrôle dans le rapport mensuel |
| Petits nombres | Décisions prises sur du bruit | 3 mois par défaut, mention « indicatif », taux avec leurs deux termes |
| Le périmètre grossit (planning, facturation) | Coût et délai | MVP fermé ; V2 et V3 sur décision ; pas de facturation ni de planning d'équipes |
| Dépendance à l'agence | Maintenance fragile | Code standard, documenté et testé ; export complet ; documentation d'exploitation |
| Clic Google Ads de plus de 90 jours | Chantier signé non importable | Action « demande qualifiée » en plus ; import en secondaire |
| Trop de demandes A | La grille actuelle classe A la plupart des demandes complètes de zone 1 (exemple v2 §2.6 : propriétaire, acoustique, 1 à 3 mois, Google : 71 points). La promesse de 2 h ouvrables peut devenir intenable | Suivre la part de A dès M1 (Vue d'ensemble) ; recalibrer le seuil A ou les poids à M3 (v2 §2.7) ; la maquette, calculée avec la vraie grille sur des demandes fictives, le montre déjà |
| Accès Business Profile refusé ou tardif | Pas d'appels ni d'itinéraires automatiques | Saisie mensuelle, comme prévu |

### 7.4 Décisions à prendre par le client

| # | Décision | Recommandation | Bloque |
|---|---|---|---|
| G1 | Option d'architecture | **A**, Pipedrive non souscrit | Tout |
| G2 | Hébergeur et pays du site ; MariaDB disponible ? | Infomaniak (Suisse) ; sinon variante A′ | MVP |
| G3 | Qui a accès : secrétariat ? agence en lecture des indicateurs ? | Oui aux deux, avec les rôles du §6.5 | MVP |
| G4 | Taux de marge brute de référence (global ou par service) et panier de référence | Donner les chiffres 2025 (v2 §1.2) | CPL max, ROI, objectif de CA |
| G5 | Inclure les honoraires d'agence dans la dépense par canal ? | Non au départ (médias, courrier, impression), affichage optionnel « coût complet » | CPL, CAC |
| G6 | Objectifs mensuels : interpolation linéaire entre M3, M6, M12, ou valeurs saisies ? | Interpolation, modifiable | Vue d'ensemble |
| G7 | Importer les chantiers signés dans Google Ads (`gclid`, avec consentement) ? Ajouter « demande qualifiée » ? Conversions améliorées (e-mail haché) ? | Oui, oui (en secondaires) ; non aux conversions améliorées sans avis du juriste | V3 |
| G8 | E-mail interne : garder les pièces jointes ou un lien vers la fiche ? | Pièces jointes 3 mois, puis le lien seul | MVP |
| G9 | Garder les liens « en un clic » sans connexion pour 2 actions (contact établi, pas de réponse) ? | Oui (jeton à usage unique, 7 jours) | MVP |
| G10 | Capacité : nombre d'équipes, jours-équipe saisis par chantier, seuil de 8 semaines ? | Oui ; saisie d'une estimation à la signature | Alerte capacité |
| G11 | Logiciel d'offres et de factures utilisé (bexio, autre) ? | Le dire en phase 0 : synchronisation en V3 au lieu d'une double saisie | V3 |
| G12 | Durées de conservation (24 mois sans suite, 5 ans clients) | Confirmer avec le juriste | MVP |
| G13 | Adresse de l'admin | `gestion.andyconstruct.ch` | MVP |
| G14 | Prospection B2B et marchés publics dans l'admin (V2) ou dans un tableur ? | Dans l'admin, en V2 | V2 |

---

## Annexe A. Maquette cliquable

- **Ouvrir** : `docs/v4/admin/maquette/index.html`, directement dans le navigateur (aucun serveur, aucun appel réseau). Un bandeau « Maquette — données fictives » est visible sur chaque écran.
- **Écrans** : Vue d'ensemble, À traiter, Demandes (liste et colonnes), Fiche demande, Saisie d'un appel, Offres et chantiers, Acquisition, SEO et visibilité, Avis, Rapport mensuel, Paramètres, Journal et données personnelles. Bascule du thème clair ou sombre en haut à droite.
- **Données** : fictives et cohérentes entre les écrans (« aujourd'hui » = jeudi 22 avril 2027, sixième mois après la mise en ligne). Les indicateurs, les scores et les échéances sont **calculés** à partir de la liste des demandes fictives, avec la grille de `scoring.json` et les heures ouvrables genevoises : ils montrent les définitions du §5 à l'œuvre. Noms de personnes et d'organisations manifestement fictifs ; aucun numéro n'est appelé.
- **Limites** : rien n'est enregistré (les actions affichent un message) ; pas de connexion ; les graphiques sont des SVG produits par le navigateur, alors que l'admin réel les produira côté serveur.
- **Vérification** (Chromium, Playwright, 1er novembre 2026) : 14 vues à 1440 px, 5 écrans à 390 px, 3 vues en thème sombre ; aucune erreur de console, aucun appel réseau, aucun défilement horizontal, aucune violation axe-core. Les rampes de gris des graphiques (entonnoir, priorités) ont été validées en clair et en sombre (luminance monotone, écarts suffisants, contraste d'au moins 2:1 avec le fond).
- **Ce que la maquette montre au passage** : calculées avec la vraie grille, 11 des 16 demandes fictives de mars sont classées A (voir le risque « Trop de demandes A », §7.3).
