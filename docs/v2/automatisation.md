# Automatisation : endpoint PHP, n8n, messages, suivi et conformité

*Ingénieur automatisation · 31 octobre 2026 · destinataires : agence (installation et exploitation), chef de projet, juriste (§8 et §9), associés (§1 et §7.6).*

Ce document met en œuvre le plan d'automatisation de `strategie-acquisition.md` §5-6 et §9, avec les décisions D2, D3 et D7 de `decisions-chef-de-projet.md`. Le frontend s'appuie sur `contrat-interface.md`.

---

## 0. L'essentiel

1. **Le site ne dépend jamais de n8n.** Chaque demande produit un e-mail interne aux associés directement depuis le PHP (`site/api/demande.php`), avec score, priorité, délai de rappel, bouton « Appeler » et pièces jointes. n8n ajoute le CRM, les SMS et les relances.
2. **Le CRM (Pipedrive) est la seule source de vérité.** Les relances lisent des dates et des statuts du CRM par des « horloges » ; les seules pauses longues dans n8n sont les deux conseils de la séquence « guide » (avec contrôle avant chaque envoi).
3. **Les associés n'ouvrent presque pas le CRM** : ils cliquent des liens signés dans leurs e-mails et SMS (« J'ai eu la personne », « Pas de réponse »…). Chaque lien ouvre une page avec un bouton : la prévisualisation d'un lien par la messagerie ne déclenche rien.
4. **Aucun e-mail à froid** vers les professionnels : la prospection B2B produit des courriers et des tâches d'appel pour des humains (LCD art. 3 al. 1 let. o).
5. **Aucun lien dans les SMS aux prospects**, aucun pixel de suivi, aucun cookie sur le site, Do Not Track respecté, données en Suisse ou dans l'UE.
6. Tests : 232 vérifications unitaires PHP, 52 vérifications HTTP (dont les règles `.htaccess` sous Apache réel), 28 contrôles des workflows n8n (dont l'interopérabilité des signatures PHP ↔ n8n), 19 vérifications du suivi dans Chromium.

---

## 1. Architecture

```
 Visiteur ── site statique (hébergement mutualisé PHP 8.x, idéalement en Suisse)
   │  suivi.js : UTM en sessionStorage (onglet), événements vers Umami ; rien si Do Not Track
   │
   │  GET  /api/demande.php?jeton        → jeton horodaté signé (piège temporel)
   │  POST /api/demande.php (multipart)  → devis · rappel · envoi_postal_guide
   ▼
 site/api/demande.php ─ Traitement.php
   1. méthode, taille (413), origine (403), débit par IP hachée (429), pot de miel (leurre)
   2. validation et normalisation (téléphone E.164, NPA → zone, e-mail strict)
   3. jeton horodaté (trop rapide → 422), contenu suspect (leurre)
   4. fichiers : 3 × 8 Mo, JPG/PNG/HEIC/PDF vérifiés par finfo + structure, noms aléatoires
   5. référence AC-AAAA-NNNN · zone · source · SCORE et PRIORITÉ (data/scoring.json) · échéance ouvrable
   6. e-mail interne (SMTP PHPMailer → repli mail() → mis de côté pour cron)        ─── associés
   7. accusé de réception au prospect si e-mail (modeles/*.txt)                     ─── prospect
   8. webhook signé HMAC-SHA256 ──────────────┐   échec : stockage/file-attente/*.json,
   9. réponse JSON {ok, message, ref}         │   relancée au prochain appel ou par cron.php
      ou redirection 303 / page HTML (sans JS) │   (alerte agence après 1 h)
                                               ▼
 n8n (VPS Infomaniak en Suisse, Docker, PostgreSQL ; ou n8n Cloud UE)
   WF01 demande → Pipedrive (personne, affaire, note, fichiers) → SMS associés A/B · accusé SMS sans lien
   WF02 liens en un clic (GET page / POST action)       WF06 synchro Pipedrive (dates d'étape)
   WF03 horloge 15 min : rappel non fait + escalade      WF03c relances d'offre J+3/J+10/J+21
   WF03d avis J+2/J+9 + accord photos J+14               WF04e offres perdues à 6 mois
   WF04i entretien 2 ans / un an / régies                WF04p purge nLPD (24 mois)
   WF07 guide imprimé + conseils (opt-in)                WF08 veille simap hebdomadaire
   WF09 rapport mensuel                                  WF10 prospection B2B (tâches humaines)
   WF12 désinscription                                   WF13 erreurs et supervision
   WF14 lecture IMAP : réponses et « STOP »
     │            │                │               │               │
     ▼            ▼                ▼               ▼               ▼
 Pipedrive    SMTP du domaine    ASPSMS (CH)     Brevo (UE)      simap.ch, Umami, Google
 (CRM, UE)    (e-mails 1:1 au    SMS internes    séquence des    Places, Search Console,
              nom de l'associé)  et de service   conseils        Healthchecks.io
```

**Qui envoie quoi**

| Message | Envoyé par | Texte |
|---|---|---|
| E-mail interne (chaque demande) | PHP | `site/api/lib/Modeles.php` (décrit dans `automation/messages/notification-interne.md`) |
| Accusé de réception (devis, rappel, guide) | PHP | `site/api/modeles/*.txt` = `automation/messages/accuse-reception-*.md` (identité vérifiée par les tests) |
| SMS internes, accusé SMS, relances, avis, entretien, conseils, réorientation | n8n | `automation/messages/*.md`, embarqués dans les nœuds Code |
| Lettres et appels de prospection | Humains (tâches n8n) | `prospection-lettres.md`, `prospection-script-appel.md` |

---

## 2. Contenu du dépôt

| Chemin | Rôle |
|---|---|
| `site/api/demande.php`, `fichier.php`, `cron.php` | Points d'entrée (seuls accessibles depuis le web) |
| `site/api/lib/` | Code : `Traitement` (orchestration), `Validateur`, `Champs`, `Telephone`, `Localite`, `Scoring`, `Source`, `HeuresOuvrables`, `AntiSpam`, `LimiteDebit`, `Televersement`, `Courriel`, `Modeles`, `Webhook`, `Jeton`, `LiensFichiers`, `Stockage`, `Journal` |
| `site/api/data/scoring.json`, `zones.json` | Grille de score et table NPA/commune → zone, modifiables sans code |
| `site/api/modeles/` | Accusés de réception (texte de référence) |
| `site/api/config.example.php` | Modèle de configuration documenté ; le vrai `config.php` est ignoré par git |
| `site/api/vendor/` | PHPMailer 6.12 (sources seules, 440 Ko, versionné : aucun `composer install` sur l'hébergement) |
| `site/api/.htaccess`, `.user.ini` | Accès web limité aux 3 points d'entrée ; réglages PHP (8 Mo par fichier, 26 Mo par envoi) |
| `site/api/tests/` | `run.php` (unitaires et intégration), `endpoint.sh` (HTTP + Apache), `faux-n8n.php`, `suivi-navigateur.js` |
| `site/assets/js/suivi.js` | Suivi sans cookie (2,9 Ko) |
| `automation/n8n/wf*.json` | 16 workflows importables |
| `automation/n8n/verifier.py`, `parametres.env.example` | Vérification des workflows ; variables d'environnement |
| `automation/docker-compose.yml`, `Caddyfile`, `init-umami.sql` | n8n + PostgreSQL + Umami + HTTPS sur le VPS |
| `automation/messages/*.md` | Tous les textes (copywriter) |

---

## 3. L'endpoint PHP en détail

### 3.1 Sécurité

| Menace | Parade |
|---|---|
| Robots | Pot de miel `site_web` (réponse « succès » factice, rien n'est traité) ; jeton horodaté signé (`form_t0`, délai minimal 2 à 4 s) ; plus de 3 liens ou balises de forum dans le message ; lien dans le nom → leurre |
| Envoi depuis un autre site | En-tête `Origin` limité au domaine (403) |
| Abus de débit | 5 demandes acceptées et 30 envois par heure et par IP (IPv6 : par préfixe /64) ; l'IP est **hachée** (HMAC avec secret), conservée 24 h au plus ; derrière un proxy, en-têtes lus seulement depuis `proxys_de_confiance` |
| Injection d'en-têtes e-mail | Adresses validées strictement (pas d'espace, de virgule, de retour à la ligne, IDN converti) ; sujets et noms débarrassés de tout caractère de contrôle ; PHPMailer encode et contrôle chaque en-tête. Testé : « Jean\r\nBcc: … » ne produit aucun en-tête. |
| Relais de spam par l'accusé de réception | Extrait du message limité à 200 caractères ; liens et noms de domaine masqués « [lien] » dans tout ce qui est repris (nom, lieu, adresse, extrait) ; lien dans l'adresse → leurre ; au plus 3 accusés par adresse sur 24 h et 20 par heure pour le site (au-delà : demande traitée, accusé non envoyé, `accuse_reception: "limite"`). Audit : `docs/v2/qa/securite.md` |
| Fichiers piégés | 3 fichiers, 8 Mo chacun ; type réel par `finfo` (jamais l'extension) ; contrôle de structure (image décodable, en-tête PDF, boîte `ftyp` HEIC) ; refus du code caché (`<?php`, `<script`, `#!/bin`) et des PDF avec JavaScript, lancement ou fichiers intégrés (même masqués par `#xx`) ; un fichier refusé fait refuser tout le lot ; renommage aléatoire (32 hex + extension issue du type réel) ; droits 0640 |
| Accès direct aux fichiers | Stockage hors racine web (recommandé) ou dossier protégé par `.htaccess` (`Require all denied`, PHP désactivé) + `index.html` ; téléchargement seulement par `fichier.php` avec lien signé et daté ; `cron.php` vérifie chaque jour que le stockage n'est pas lisible depuis le web (hébergeurs nginx) |
| Fuite d'informations | `display_errors` désactivé partout ; erreurs dans `stockage/journaux/php-erreurs.log` ; réponses d'erreur génériques ; en-têtes `nosniff`, `no-store`, `noindex`, `X-Frame-Options` |
| Données personnelles dans les journaux | Journal JSON par jour : référence, issue, compteurs, 12 caractères de l'empreinte d'IP. Jamais de nom, e-mail, téléphone, message ni IP. Purge à 30 jours. |
| Webhook falsifié ou rejoué | HMAC-SHA256 sur `horodatage.corps`, horodatage ± 5 min, comparaison à temps constant (n8n) |
| Secrets | Dans `config.php` (non versionné) et dans l'environnement de n8n ; 32 caractères minimum, le PHP refuse de démarrer en production sinon ; trois secrets distincts (webhook, actions, local) |

### 3.2 Score, priorité et délai promis

Le PHP calcule le score selon `data/scoring.json` (stratégie §2.3 à §2.5) : type de client, service, ampleur, zone (NPA ou commune, correspondance approchée), délai, source (UTM, référent ou réponse déclarée, la plus forte), bonus fichier et téléphone, malus message vide sans téléphone. Règles : commune, régie et architecte jamais sous B ; demande de rappel jamais sous B ; dégât ou fin de bail en moins d'un mois → A ; zone 3 sans pénalité pour le B2B ou plus de 50 m² ; service hors des 4 métiers ou lieu hors de Suisse romande → « hors cible » (réponse de réorientation **validée par un associé**). Les cinq exemples du §2.6 sont des tests automatiques.

Échéance de premier contact en heures ouvrables (lu-ve 7 h-18 h, jours fériés genevois dont le Jeûne genevois et le 31 décembre, fermetures configurables) : A 2 h ; B le jour même avant 14 h, sinon le lendemain 10 h ; C 2 jours ; hors cible 1 jour. L'accusé de réception l'annonce honnêtement (« aujourd'hui avant 12 h 15 », « lundi avant 9 h ») ; `promesse_delai => false` remplace par « dans les meilleurs délais ». **Ne promettre que ce que l'on tient** (`personas-psychologie.md` §5).

### 3.3 Résilience

| Panne | Effet |
|---|---|
| n8n arrêté, lent (> 5 s) ou refus de signature | Charge mise en file (`stockage/file-attente/`), renvoyée avec une signature et des liens neufs au prochain appel de `demande.php` (3 éléments) ou par `cron.php` (toutes les 10 min), délai croissant ; alerte e-mail à l'agence au-delà d'une heure (une fois) ; abandon et alerte au-delà de 14 jours. L'e-mail interne est déjà parti. |
| SMTP en panne | Repli sur `mail()` de l'hébergeur ; sinon message mis de côté (`stockage/mails-echec/`) et renvoyé par `cron.php` ; la charge part quand même vers n8n |
| Tout en panne (disque) | Réponse 500 avec le numéro de téléphone ; la saisie reste dans le navigateur |

---

## 4. Installation pas à pas

### 4.1 Comptes et prérequis (M0)

| Élément | Qui | Remarque |
|---|---|---|
| Domaine `andyconstruct.ch` et messagerie (2 ou 3 boîtes + `site@`) | Client, agence | Infomaniak (Suisse) conseillé |
| Hébergement PHP 8.1 ou plus avec `fileinfo`, `curl`, `mbstring`, `openssl` | Agence | `intl` facultatif (adresses e-mail à accents) |
| VPS Infomaniak 2 vCPU / 4 Go **au nom du client** | Client | ou n8n Cloud (§4.4 B) |
| Pipedrive Lite × 2 (ou Brevo CRM gratuit, scénario S) | Client | Accord de sous-traitance (DPA) accepté |
| Brevo gratuit | Client | DPA accepté |
| ASPSMS | Client | Crédits prépayés |
| Healthchecks.io gratuit | Agence | |
| Contrats de sous-traitance signés ou acceptés (Pipedrive, Brevo, Infomaniak, ASPSMS, hébergeur, agence) | Client | nLPD art. 9 |

### 4.2 E-mail : SPF, DKIM, DMARC (avant tout envoi)

1. Créer `site@andyconstruct.ch` (expéditeur technique) et les boîtes des associés.
2. DNS : enregistrement **SPF** incluant le fournisseur de messagerie et Brevo (`v=spf1 include:spf.infomaniak.ch include:spf.brevo.com -all`, à adapter) ; **DKIM** activé chez le fournisseur et dans Brevo (domaine authentifié) ; **DMARC** `v=DMARC1; p=quarantine; rua=mailto:dmarc@andyconstruct.ch` (commencer par `p=none` deux semaines).
3. Vérifier avec un envoi vers mail-tester.com : 9/10 au moins.

### 4.3 Hébergement PHP

1. Déployer `site/` (le dossier `api/` compris, avec `vendor/`). Le script `deploy/deploy_ftp.py` envoie l'ensemble.
2. **Stockage hors de la racine web** : créer un dossier frère de la racine web (ex. `~/andy-construct-prive/`), droits 0750.
3. Copier `api/config.example.php` en `api/config.php` sur le serveur et remplir : `stockage` (chemin absolu du dossier ci-dessus), les trois secrets (`openssl rand -hex 32`), le SMTP (Infomaniak : `mail.infomaniak.com`, 587, `tls` ; Hostinger : `smtp.hostinger.com`, 465, `ssl`), `destinataires_internes`, `alerte_email`, `associes` (rôles à confirmer), `cron_cle`. Garder `mode_test => true` pour les essais.
4. Tâche planifiée toutes les 10 minutes : `php /chemin/api/cron.php` (Infomaniak : Tâches planifiées ; Hostinger : Avancé > Tâches Cron). Sans cron CLI : URL `https://www.andyconstruct.ch/api/cron.php?cle=…`, ou déclencheur facultatif de WF13 (`AC_CRON_URL`).
5. Vérifier : `https://www.andyconstruct.ch/api/demande.php?jeton` répond un jeton ; `…/api/config.php`, `…/api/lib/Config.php`, `…/api/data/scoring.json` répondent 403. Serveur **nginx** (sans `.htaccess`) : interdire `/api/(lib|data|modeles|tests|vendor|stockage)/` et `config*.php` dans la configuration du serveur, et garder le stockage hors racine.
6. `robots.txt` : `Disallow: /api/`.
7. Les limites de taille sont dans `api/.user.ini` (PHP-FPM) et `api/.htaccess` (mod_php) ; vérifier `upload_max_filesize` = 8M et `post_max_size` = 26M avec une page `phpinfo()` temporaire, supprimée ensuite.

### 4.4 n8n

**A. VPS Infomaniak (recommandé : données en Suisse)**

1. VPS Ubuntu LTS, accès SSH par clé, connexion root par mot de passe désactivée, pare-feu ouvert sur 22, 80 et 443 seulement ; mises à jour de sécurité automatiques (`unattended-upgrades`).
2. DNS : `n8n.andyconstruct.ch` et `stats.andyconstruct.ch` → IP du VPS.
3. Installer Docker et le plugin compose ; copier le dossier `automation/` sur le VPS.
4. `cp n8n/parametres.env.example .env` puis remplir `.env` (secrets, personnes, ASPSMS, Pipedrive : §4.5).
5. `docker compose up -d` ; Caddy obtient les certificats. Ouvrir `https://n8n.andyconstruct.ch`, créer le compte propriétaire (mot de passe fort, double authentification).
6. Le fichier `docker-compose.yml` fixe déjà : fuseau Europe/Zurich, PostgreSQL, purge des exécutions à 30 jours, `NODE_FUNCTION_ALLOW_BUILTIN=crypto` (signatures HMAC), accès aux variables `AC_*`, télémétrie désactivée. **Fixer `N8N_VERSION`** sur la version stable du moment.
7. Instantané quotidien du VPS (7 jours) dans la console Infomaniak.

**B. n8n Cloud (si personne ne maintient de serveur)**

Région Francfort (UE). Différences : les variables d'environnement personnalisées ne sont pas disponibles ; utiliser les « Variables » de n8n (offre qui les inclut) et remplacer `$env.` par `$vars.` dans les fichiers JSON avant l'import ; vérifier que le module `crypto` est autorisé dans les nœuds Code (sinon : nœud « Crypto » pour le HMAC). Limite d'exécutions : l'horloge WF03 (toutes les 15 min en heures ouvrables) consomme environ 1'000 exécutions par mois.

### 4.5 Pipedrive (CRM)

1. **Pipelines et étapes** (stratégie §5.5) : Demandes et offres (Nouvelle demande, Contact établi, Visite planifiée, Offre envoyée, Relance / négociation) ; Chantiers (Planifié, En cours, Terminé, Avis demandé, Clos) ; Prospection B2B (À contacter, Courrier envoyé, Appel à faire, Intéressé, Relance J+30, Pas maintenant, Ne plus contacter) ; Marchés publics (Repéré, Étudié, Dossier en cours, Déposé).
2. **Champs personnalisés** : créer ceux de `AC_PD_CHAMPS` (affaire : texte, nombre, date ou liste ; personne : `opposition_marketing`, `dernier_message_marketing`, `info_exception_client`, `asterisque_verifie`, `regie_annuel_le`, `etiquette_personne` ; organisation : `type`). Relever la **clé API** de chaque champ et l'écrire dans `AC_PD_CHAMPS`.
3. **Filtres enregistrés** (`AC_PD_IDS`) : `filtre_nouvelles` (étape Nouvelle demande, ouvertes), `filtre_offres` (Offre envoyée ou Relance, ouvertes), `filtre_perdues` (perdues, pipeline Demandes), `filtre_chantiers_termines`, `filtre_chantiers_clos`, `filtre_b2b_a_contacter`, `filtre_b2b_suivi` (Appel à faire + Intéressé), `filtre_toutes`.
4. Identifiants des pipelines, étapes et utilisateurs (associé bureau, associé terrain) → `AC_PD_IDS`.
5. Jeton d'API d'un utilisateur technique → identifiant n8n « Pipedrive Andy Construct ».
6. **Alternative Brevo CRM (scénario S)** : 1 utilisateur, 50 affaires ouvertes. Remplacer dans WF01, WF02, WF03 les appels `api.pipedrive.com` par l'API CRM de Brevo (`/v3/crm/deals`, attributs d'affaire équivalents) ; les autres horloges restent valables une fois les filtres traduits. Prévoir une demi-journée d'adaptation.

### 4.6 Brevo, SMS, Umami, Google

- **Brevo** : authentifier le domaine ; une liste par guide (identifiant dans `config.php` → `guides.*.liste_brevo`) ; attributs de contact `PRENOM`, `NOM`, `GUIDE`, `PROFIL`, `A_REPONDU` (booléen), `DEMANDE` (booléen) ; clé API → identifiant n8n « Brevo (en-tête api-key) » (en-tête `api-key`).
- **ASPSMS** : clé utilisateur et mot de passe API dans `.env` ; expéditeur `AndyConstr`. Alternative Twilio : remplacer les nœuds « SMS » par le nœud Twilio (même texte).
- **Umami** : ouvrir `https://stats.andyconstruct.ch` (compte `admin`, changer le mot de passe), ajouter le site, copier l'identifiant dans le snippet du frontend (`contrat-interface.md` §12) et dans `AC_UMAMI_SITE` ; créer un jeton d'API → identifiant n8n « Umami (Authorization: Bearer) ».
- **Google** : clé Places API restreinte à Places → identifiant « Google Places (X-Goog-Api-Key) » ; OAuth2 Search Console → identifiant « Google Search Console (OAuth2) » ; `AC_LIEN_AVIS_GOOGLE` = lien « Demander des avis » de la fiche.
- **Healthchecks.io** : un contrôle « horloge n8n » (période 15 min, grâce 30 min) → `AC_HEALTHCHECK_HORLOGE` ; un contrôle « cron PHP » (10 min, grâce 30 min) → `healthcheck_url` de `config.php`.

---

## 5. Import des workflows

1. Vérifier les fichiers : `python3 automation/n8n/verifier.py` (0 erreur attendue).
2. Dans n8n : *Workflows > Importer depuis un fichier*, un par un (16 fichiers). Ils arrivent **désactivés**.
3. Créer les identifiants une fois (*Credentials*) avec **exactement** ces noms : « Pipedrive Andy Construct », « SMTP Andy Construct (domaine) », « Brevo (en-tête api-key) », « Umami (Authorization: Bearer) », « Google Places (X-Goog-Api-Key) », « Google Search Console (OAuth2) », « IMAP associé bureau », « IMAP associé terrain ». Ouvrir chaque nœud signalé en rouge et choisir l'identifiant correspondant.
4. Importer d'abord **WF13**, puis dans chaque autre workflow : *Paramètres > Error workflow > WF13 · Erreurs et supervision*.
5. Activer dans cet ordre : WF13, WF12, WF02, WF01, WF06, WF03, WF07, puis les autres selon la feuille de route (stratégie §8.1).
6. Reporter dans `site/api/config.php` les URL de production : `n8n.url_demande` = `https://n8n.andyconstruct.ch/webhook/ac-demande`, `url_guide` = `…/webhook/ac-guide`, `url_actions` = `…/webhook/ac-action`, `url_desinscription` = `…/webhook/ac-stop` ; `n8n.simuler => false`.
7. Les workflows sont produits à partir de `automation/messages/` : après une modification de texte importante, modifier aussi le nœud Code concerné dans n8n (ou régénérer les fichiers, puis réimporter), et exporter les workflows modifiés dans `automation/n8n/` (sans identifiants).

---

## 6. Tests

### 6.1 Automatiques (à relancer après toute modification)

| Commande | Ce qui est vérifié | Résultat au 31.10.2026 |
|---|---|---|
| `php site/api/tests/run.php` | Téléphone, e-mail, validation des 3 formulaires, zones, source, scoring (exemples §2.6 et règles), heures ouvrables et fériés, anti-spam, limite de débit, HMAC, jetons, liens de fichiers, fichiers piégés (PHP déguisé, polyglotte, PDF JavaScript masqué, SVG, exécutable, HTML, > 8 Mo, 4 fichiers), modèles, traitement complet (e-mails écrits en .eml, aucun envoi), injection d'en-têtes, pages sans JS, webhook réel vers un faux n8n (signature, refus, panne, lenteur, file d'attente, alerte), cohérence avec `automation/messages/` | 232 / 232 |
| `bash site/api/tests/endpoint.sh` | Serveur `php -S localhost:8099 -t site` + curl : cas valable avec photo et plan, pot de miel, envoi trop rapide, fichiers piégés, champs manquants, formats, origine étrangère, sans JS, `fichier.php` ; puis **Apache 2.4 + mod_php** : 18 chemins internes refusés (403), PHP non exécuté dans le stockage, en-têtes | 52 / 52 |
| `python3 automation/n8n/verifier.py` | 16 workflows : JSON, nœuds, connexions, atteignabilité, webhooks, secrets, syntaxe de 45 nœuds Code et 247 expressions, signature PHP acceptée par n8n, jetons PHP ↔ n8n, exécution à blanc de WF01 et WF02 | 28 contrôles, 0 erreur |
| `node site/api/tests/suivi-navigateur.js` | `suivi.js` dans Chromium : UTM, champs cachés, événements, filtrage des données personnelles, gclid avec consentement seulement, Do Not Track, absence d'Umami | 19 / 19 |

### 6.2 Recette de bout en bout (avant la mise en production, environnement de test)

Configuration : `mode_test => false` mais `destinataires_internes` = boîte de test, n8n de test (ou workflows en mode test), Pipedrive avec l'étiquette « TEST », `AC_SMS_URL` vers un webhook de test (les SMS deviennent des requêtes visibles).

| # | Cas | Attendu |
|---|---|---|
| 1 | Devis A (propriétaire, acoustique, GE, téléphone) en semaine à 10 h | E-mail interne [A] avec pièces jointes, accusé « aujourd'hui avant 12 h 15 », affaire Pipedrive (score, échéance), SMS associé terrain |
| 2 | Devis B reçu à 15 h | Accusé « demain avant 10 h », SMS |
| 3 | Devis C (locataire, Meta, sans téléphone) | Pas de SMS, présent dans le récapitulatif de 17 h 30 |
| 4 | Régie en zone 3 | Jamais sous B |
| 5 | Service « autre » | Hors cible, bouton de réorientation, rien envoyé sans clic |
| 6 | Doublon (même e-mail, 2e demande) | Note sur l'affaire existante, pas de SMS |
| 7 | Rappel avec mobile, sans e-mail, à 21 h | SMS d'accusé sans lien envoyé le lendemain à 8 h |
| 8 | Guide par la poste, sans e-mail | Tâche « Envoyer le guide imprimé » avec l'adresse |
| 9 | Guide avec e-mail et case « conseils » | Accusé, E2 à J+3, E3 à J+8 (raccourcir les délais en test) ; « STOP » arrête tout |
| 10 | n8n arrêté pendant une demande | E-mail interne reçu, file d'attente, livraison au redémarrage, alerte après 1 h |
| 11 | Fichier de 12 Mo | Refus 413 ou erreur « dépasse 8 Mo » |
| 12 | Robot (pot de miel) | Réponse « ok », rien reçu |
| 13 | Clic « Pas de réponse » 3 fois | E-mail ou SMS au 1er essai, clôture courtoise au 3e |
| 14 | Prévisualisation d'un lien par Outlook | Aucune action (seul le bouton agit) |
| 15 | Offre envoyée (étape) puis J+3, J+10, J+21 simulés | Avec téléphone : e-mail J+3, tâche d'appel J+10, e-mail J+21 avec 3 liens. Sans téléphone : e-mails J+3 et J+10, rien au J+21 (deux e-mails au plus) |
| 16 | Réponse à un e-mail de relance | `a_repondu` = oui, plus aucune relance |
| 17 | Chantier terminé + réserves levées | Avis J+2 (e-mail + SMS sans lien), relance J+9 unique ; après un « STOP » (WF14) ou une désinscription (WF12), plus rien |
| 18 | Passage à l'heure d'été (dernier dimanche de mars) | Échéances et horloges correctes |
| 19 | Jour férié genevois (Jeûne genevois) | Pas de relance, échéance reportée |
| 20 | Lien de désinscription | Page de confirmation, Brevo bloqué, opposition datée dans Pipedrive |

---

## 7. Exploitation

### 7.1 Supervision

| Signal | Source | Action |
|---|---|---|
| Erreur d'un workflow | WF13 (e-mail + SMS agence, sans donnée personnelle) | Ouvrir l'exécution, corriger, relancer |
| Horloge muette depuis 30 min | Healthchecks.io | Vérifier le VPS et n8n |
| Demande en attente depuis 1 h | `cron.php` (e-mail agence) et ping Healthchecks `/fail` | Vérifier l'URL du webhook, le certificat, le secret HMAC |
| Stockage lisible depuis le web | `cron.php` (contrôle quotidien) | Déplacer le stockage hors racine |
| Journaux | `stockage/journaux/AAAA-MM-JJ.log` (une ligne JSON par événement) ; exécutions n8n (erreurs, 30 jours) | Lecture mensuelle : taux de spam, échecs SMTP |

### 7.2 Sauvegardes

- VPS : instantané quotidien, 7 jours. Base PostgreSQL : `pg_dump` hebdomadaire chiffré, conservé 4 semaines hors du VPS.
- Workflows : export JSON après chaque modification, versionné dans `automation/n8n/` **sans identifiants**.
- CRM : export CSV hebdomadaire chiffré, 4 semaines.
- `config.php` et `.env` : dans le gestionnaire de mots de passe de l'agence (jamais par e-mail).

### 7.3 Rotation des secrets (une fois par an, et immédiatement en cas de doute)

1. Générer un nouveau secret (`openssl rand -hex 32`).
2. **HMAC du webhook** : mettre le nouveau secret dans `.env` (`AC_HMAC_SECRET`), redémarrer n8n, puis tout de suite dans `config.php` (`secrets.hmac_webhook`). Les demandes reçues entre-temps passent en file d'attente et repartent avec la nouvelle signature : aucune perte.
3. **Secret des actions** : même procédure (`AC_ACTION_SECRET` et `secrets.actions`). Les liens en un clic déjà envoyés deviennent invalides (la page l'indique) ; les liens de désinscription aussi : la réponse « STOP » reste possible.
4. **Secret local** : changer `secrets.local` ; effet : jetons de formulaire et liens de fichiers en cours invalides (sans conséquence), empreintes d'IP renouvelées.
5. Mots de passe SMTP, clés Pipedrive, Brevo, ASPSMS, Umami : régénérer chez le fournisseur, mettre à jour l'identifiant n8n ou la configuration, révoquer l'ancien.

### 7.4 Mises à jour

- n8n : mensuelle (lire les notes de version, sauvegarde avant, `docker compose pull && docker compose up -d`, puis `verifier.py` et un test de bout en bout rapide).
- PHPMailer : `composer update` dans `site/api` sur un poste de travail (`COMPOSER_ALLOW_SUPERUSER=1` si nécessaire), retirer `.git`, `test`, `examples`, `docs` du dossier `vendor/phpmailer/phpmailer`, relancer les tests, déployer.
- Recalibrage du score : trimestriel (stratégie §2.7), dans `site/api/data/scoring.json` ; relancer `run.php` (les exemples du §2.6 doivent rester justes ou être mis à jour avec la stratégie).

### 7.5 Droits des personnes (accès, rectification, effacement)

1. Demande reçue par e-mail ou courrier : accuser réception, vérifier l'identité (répondre à l'adresse connue).
2. Rechercher la personne : Pipedrive (personne, affaires, notes, fichiers), Brevo (contact), boîtes e-mail des associés, `stockage/fichiers/` (30 jours au plus), file d'attente.
3. Accès : export Pipedrive (personne et affaires) + données Brevo, transmis sous 30 jours.
4. Effacement : supprimer la personne dans Pipedrive et Brevo (en gardant l'adresse hachée sur la liste d'opposition si la personne refuse toute sollicitation), supprimer les e-mails correspondants ; les pièces comptables restent 10 ans (CO 958f).
5. Consigner la demande et la réponse (date, action) dans le registre (§8).

### 7.6 Ce que font les associés (rappel)

Rappeler dans le délai annoncé ; cliquer le résultat (« J'ai eu la personne », « Pas de réponse ») ; passer l'affaire à « Offre envoyée » le jour de l'envoi ; cliquer « Réserves levées » à la fin d'un chantier ; traiter les tâches (guides à poster, appels B2B, rappels). Tout le reste part seul.

### 7.7 Incident de sécurité (nLPD art. 24)

Évaluation sous 24 h par l'agence ; si risque élevé pour les personnes : annonce au PFPDT dans les meilleurs délais (formulaire en ligne) et information des personnes concernées ; rotation des secrets (§7.3) ; consignation dans le registre.

---

## 8. Registre des activités de traitement (nLPD art. 12)

Entreprise de moins de 250 personnes sans traitement à risque élevé : dispense probable (OPDo art. 24, *à confirmer par le juriste*). Le registre est tenu quand même, sur une page.

**Responsable** : Andy Construct, Chanton & Cie, Route des Acacias 48, 1227 Carouge (IDE CHE-113.706.162). **Contact protection des données** : `contact@andyconstruct.ch` *(adresse à confirmer)*.

| Traitement | Finalité | Personnes | Données | Fondement / justification | Destinataires et sous-traitants (pays) | Durée de conservation | Mesures |
|---|---|---|---|---|---|---|---|
| Demandes de devis et de rappel | Répondre à la demande, rappeler, établir une offre ; remercier la personne qui a recommandé | Prospects, clients ; personne qui a recommandé (nom seulement) | Civilité, nom, téléphone, e-mail, commune ou NPA, type de client, type de travaux, surface, délai, message, photos et plans, préférence de contact et créneau, « connu par », nom de la personne qui a recommandé, source de la visite (page d'envoi, page d'entrée, référent, UTM ; `gclid` seulement avec consentement) | Demande de la personne (mesures précontractuelles) ; information (art. 19) par la mention sous le formulaire et la politique | Associés ; agence ; hébergeur du site (*pays à confirmer*) ; messagerie du domaine (*fournisseur et pays à confirmer*) ; Infomaniak (n8n, CH) ; Pipedrive (UE) ; ASPSMS (CH) | Prospect non converti : 24 mois après le dernier contact (WF04p : liste envoyée à l'agence, effacement manuel tant que `AC_PURGE_AUTO=false`) ; e-mails internes et pièces jointes dans les boîtes des associés : même durée (*purge manuelle à organiser*) ; fichiers sur le serveur web : 30 jours ; historique des exécutions n8n : 30 jours ; client : voir « Suivi » | HTTPS, HMAC, accès par rôles, journaux sans données personnelles, purge des fichiers |
| Priorisation des demandes (score) | Ordonner les rappels | Prospects | Données de la demande, dont la source de la visite | Intérêt prépondérant ; profilage simple, **sans décision automatisée** (toutes les demandes sont rappelées, un humain décide) ; mentionné dans la politique | Idem | Avec la demande | Grille documentée, recalibrée |
| Suivi des offres et des chantiers | Relances de service (3 au plus en 3 semaines), organisation, réception, demande d'avis (J+2, relance J+9), recontact unique à 6 mois si la personne l'a demandé | Prospects ayant reçu une offre, clients | Coordonnées, montants, dates, étapes, motif de perte, `recontact_autorise` | Contrat et mesures précontractuelles ; demande expresse pour le recontact à 6 mois | Pipedrive (UE), messagerie du domaine, ASPSMS (CH) | Pièces comptables et contractuelles : 10 ans (CO 958f) ; données CRM : 5 ans après la réception (responsabilité pour les défauts, CO 371), puis revue | Accès limité aux associés et à l'agence ; toute réponse ou « STOP » arrête les relances (WF14 ; *WF03d à corriger*) |
| Publication de photos et de témoignages | Montrer des réalisations | Clients | Photos du chantier (sans visage), commune, texte du témoignage, choix et date de l'accord | Consentement (e-mail J+14), révocable | Public : site, fiche Google (Google, Irlande / États-Unis), page LinkedIn, dossier de références | Tant que l'accord n'est pas retiré ; preuve de l'accord conservée avec le dossier client | Aucune publication sans accord daté dans le CRM |
| Envoi postal des guides et conseils par e-mail | Envoyer le guide imprimé ; deux conseils par e-mail si demandés | Visiteurs | Civilité, nom, adresse postale, e-mail facultatif, profil, accord pour les conseils | Demande de la personne ; accord explicite pour les conseils (case non cochée) | Pipedrive (UE), Brevo (UE, seulement si conseils), Pingen (CH) si utilisé | Adresse postale : 3 mois après l'envoi (*procédure à créer : l'adresse est dans la note de la tâche Pipedrive*) ; contact Brevo : jusqu'à la désinscription, 24 mois au plus | Désinscription par lien ou « STOP », liste d'opposition. **WF07 crée aussi une tâche « Appel de courtoisie » pour les profils professionnels : finalité non annoncée, à désactiver ou à annoncer** |
| Entretien et informations aux clients | Proposer un contrôle, faire le point à un an, rafraîchissements des régies | Clients informés de leur droit d'opposition | Coordonnées, type de travaux, date de réception | Exception « clients » (LCD art. 3 al. 1 let. o) ; information donnée à la commande | Messagerie du domaine | Tant que la relation dure, opposition possible à tout moment | Un message marketing par 30 jours au plus ; `opposition_marketing` vérifié |
| Prospection B2B | Se faire connaître des régies, architectes, communes | Contacts professionnels nommés | Nom, fonction, organisation, adresse postale et téléphone professionnels, source des coordonnées (annuaire, site de l'organisation), résultats d'appel | Intérêt prépondérant ; courrier et appel (astérisque respecté) ; **aucun e-mail sans accord** ; source indiquée dans la première lettre (art. 19 al. 3) | Pipedrive (UE), Pingen (CH) | « Ne plus contacter » : conservé pour respecter l'opposition ; autres : 24 mois sans réponse | Vérification de l'astérisque, arrêt immédiat sur demande |
| Statistiques du site | Mesurer l'audience et les contacts web | Visiteurs | Pages vues, référent, appareil et navigateur, pays ou région (déduits de l'adresse IP, qui n'est pas conservée), événements (sans donnée saisie), UTM | Intérêt prépondérant ; données sans nom, sans cookie ; Do Not Track et GPC respectés | Umami auto-hébergé (VPS Infomaniak, CH) | 24 mois (*Umami n'efface rien seul : tâche de purge à prévoir*) | Pas d'adresse IP stockée par Umami, pas de cookie |
| Attribution des demandes | Savoir quelle campagne amène des demandes | Visiteurs qui envoient un formulaire | Page d'entrée, référent, UTM, repère « formulaire commencé » (stockage de session de l'onglet) | Intérêt prépondérant ; information (art. 45c LTC) et refus possible (Do Not Track, GPC, réglages du navigateur) | Avec la demande | Effacé à la fermeture de l'onglet ; puis avec la demande | Aucun envoi à un tiers |
| Sécurité du formulaire | Bloquer les robots et les abus | Visiteurs | Empreinte HMAC de l'adresse IP, horodatages | Intérêt prépondérant (sécurité) | Hébergeur | Empreinte complète : 24 h ; 12 caractères de l'empreinte dans le journal : 30 jours | Hachage avec secret, purge automatique |
| Journaux du serveur web | Exploitation et sécurité de l'hébergement | Visiteurs | Adresse IP, date, page demandée, navigateur | Intérêt prépondérant (sécurité) | Hébergeur (*pays à confirmer*) | *Durée de l'hébergeur à relever* | Accès réservé à l'hébergeur et à l'agence |
| Supervision technique | Détecter les pannes | — | Références de demandes, messages d'erreur nettoyés | Intérêt prépondérant | Healthchecks.io (UE), agence | 30 jours | Masquage des adresses et numéros |

**Sous-traitants** (DPA à archiver) : hébergeur du site, fournisseur de messagerie du domaine, Infomaniak (VPS), Pipedrive OÜ (UE, *région d'hébergement à confirmer dans le DPA*), Sendinblue SAS / Brevo (UE), ASPSMS (CH), Pingen (CH, si utilisé), Healthchecks.io (UE), agence Harbor Digital (*pays à confirmer*). **Transferts hors de Suisse** : vers l'UE (niveau adéquat, OPDo annexe 1), *sous réserve des sous-traitants ultérieurs de Pipedrive et de Brevo, à vérifier dans leurs DPA* ; photos publiées avec accord sur la fiche Google (Google, communication publique). Google (Places, Search Console) ne reçoit **aucune** donnée de prospect.

---

## 9. Politique de confidentialité (texte prêt à intégrer dans `confidentialite.html`)

*Texte à faire relire par le juriste. Structure et ton : copy deck §M. Les éléments entre crochets sont à confirmer.*

> ### Protection des données
>
> Ce que nous faisons des informations que vous nous transmettez, combien de temps nous les gardons, et comment exercer vos droits.
>
> #### Qui est responsable
> Andy Construct, Chanton & Cie, société en nom collectif, Route des Acacias 48, 1227 Carouge, IDE CHE-113.706.162. Pour toute question sur vos données : contact@andyconstruct.ch [à confirmer] ou +41 22 771 20 15.
>
> #### Ce que nous recevons quand vous nous écrivez
> Quand vous demandez un devis ou un rappel, nous recevons ce que vous saisissez : votre nom (et votre civilité si vous l'indiquez), votre numéro de téléphone ou votre adresse e-mail, la commune des travaux, le type de travaux, votre situation (propriétaire, régie, architecte…), la surface et le délai, votre préférence de contact, votre message et les photos ou plans que vous joignez. Si vous nous dites comment vous nous avez connus, ou qui vous a recommandé Andy Construct, nous le recevons aussi.
>
> Le formulaire nous transmet aussi, pour savoir comment notre site est trouvé : la page d'où vous l'envoyez, la page par laquelle vous êtes arrivé(e), le site d'où vous veniez (un moteur de recherche, par exemple) et, le cas échéant, le nom de la campagne publicitaire (paramètres « utm »).
>
> #### À quoi elles servent
> Ces informations servent à traiter votre demande : vous rappeler, convenir d'une visite, vous remettre une offre et, si vous nous confiez les travaux, organiser et suivre le chantier. La provenance de votre visite nous sert aussi à compter, sans vous nommer, les pages et les campagnes qui amènent des demandes. Le nom de la personne qui vous a recommandé(e) sert uniquement à la remercier.
>
> Nous ne vendons pas vos données et nous ne les utilisons pas pour de la publicité. Seule exception : si vous devenez client et que nous vous en avons informé(e) à la commande, nous pouvons vous écrire au sujet de prestations semblables (voir « Après un chantier »).
>
> #### Comment nous traitons votre demande
> Pour rappeler chacun dans un délai raisonnable, nous classons les demandes par ordre de priorité, selon les informations de la demande (type de travaux et de client, ampleur, lieu, délai, provenance). **Toutes les demandes sont rappelées** et c'est toujours une personne qui décide de la suite.
>
> Vous recevez un e-mail de confirmation si vous avez donné votre adresse, ou un SMS si vous n'avez laissé qu'un numéro de portable. Si nous n'arrivons pas à vous joindre, nous vous l'écrivons ; après trois essais sans réponse, nous classons la demande et ne vous relançons plus.
>
> Après l'envoi d'une offre, nous pouvons vous écrire ou vous appeler au plus trois fois en trois semaines, pour savoir si vous avez des questions. Une simple réponse arrête ces messages. Si vous nous dites que votre projet est reporté et que nous pouvons vous recontacter, nous vous écrivons une seule fois, environ six mois plus tard.
>
> #### Le guide imprimé et les conseils par e-mail
> Nos guides se téléchargent librement, sans inscription. Si vous demandez la version imprimée, nous utilisons votre nom et votre adresse postale uniquement pour vous l'envoyer. Si vous donnez votre e-mail, vous recevez une confirmation. Si vous avez coché la case prévue, nous vous envoyons aussi deux e-mails de conseils sur le même sujet, puis plus rien. Chaque e-mail contient un lien pour vous désinscrire ; vous pouvez aussi répondre « STOP ».
>
> #### Après un chantier
> Une fois le chantier terminé, nous vous demandons votre avis, par e-mail (et par SMS pour les particuliers), avec une seule relance au plus. Nous le demandons à tous nos clients, sans tri et sans contrepartie. Nous vous demandons aussi si nous pouvons montrer des photos de votre chantier : nous ne publions rien sans votre accord, et vous pouvez le retirer à tout moment.
>
> Si nous vous avons informé(e) de ce droit au moment de la commande, nous pouvons vous écrire de temps en temps au sujet de prestations semblables, par exemple pour faire le point un an après les travaux. Vous pouvez vous y opposer à tout moment, gratuitement, en répondant « STOP » ou par le lien en bas de chaque message.
>
> #### Si vous êtes un professionnel que nous contactons
> Nous écrivons et téléphonons à des régies, des bureaux d'architectes, des communes et des entreprises pour présenter notre travail. Nous utilisons alors le nom, la fonction et les coordonnées professionnelles (adresse, téléphone) d'une personne de contact, trouvés dans un annuaire public ou sur le site de son organisation, et nos notes sur la suite donnée. Nous n'envoyons pas d'e-mail publicitaire sans votre accord et nous respectons l'astérisque de l'annuaire. Sur simple demande, nous ne vous contactons plus. Sans suite de votre part, ces données sont effacées après 24 mois.
>
> #### Qui d'autre voit vos données
> Seuls les associés d'Andy Construct et notre agence web (Harbor Digital, [pays], pour la mise en place et la maintenance) y ont accès. Nous faisons appel à des prestataires techniques, liés par un contrat de protection des données :
> - [hébergeur du site, pays] pour le site et la réception du formulaire ;
> - [fournisseur de messagerie, pays] pour nos e-mails ;
> - Infomaniak (Suisse) pour le serveur de l'outil d'automatisation et des statistiques ;
> - Pipedrive (Union européenne) pour le suivi des demandes et des chantiers ;
> - Brevo (France, Union européenne) pour les e-mails de conseils, si vous les avez demandés ;
> - ASPSMS (Suisse) pour l'envoi des SMS ;
> - [Pingen (Suisse) pour l'impression et l'envoi des courriers, si utilisé] ;
> - Healthchecks.io (Union européenne) pour la surveillance technique, sans vos coordonnées.
>
> Vos données sont hébergées en Suisse ou dans l'Union européenne, dont le niveau de protection est reconnu par le Conseil fédéral. [Si un prestataire ultérieur de Pipedrive ou de Brevo accède aux données depuis un autre pays, l'indiquer ici avec la garantie utilisée.] Les photos que vous nous autorisez à publier sont visibles par tous sur les supports choisis, dont notre fiche Google.
>
> #### Combien de temps nous les gardons
> - Demande sans suite : 24 mois après notre dernier contact, puis effacement.
> - Photos et plans envoyés par le formulaire : 30 jours sur le serveur du site ; ensuite seulement dans le dossier de votre demande (outil de suivi et messagerie des associés), avec la même durée que la demande.
> - Clients : les documents comptables et contractuels 10 ans (obligation légale) ; les autres données le temps de notre responsabilité pour les défauts (5 ans après la réception des travaux), puis revue.
> - Adresse postale donnée pour le guide imprimé : 3 mois après l'envoi.
> - Adresse e-mail donnée pour les conseils : jusqu'à votre désinscription, et 24 mois au plus.
> - Si vous refusez nos messages : nous gardons votre adresse sous une forme codée, uniquement pour respecter ce refus.
> - Adresse IP : notre formulaire ne l'enregistre jamais en clair. Une empreinte codée sert 24 heures à bloquer les abus ; un extrait de cette empreinte reste 30 jours dans le journal technique.
> - Journaux techniques de l'hébergeur (adresse IP, pages demandées) : [durée à confirmer auprès de l'hébergeur].
> - Historique de l'outil d'automatisation : 30 jours. Sauvegardes : remplacées en quatre semaines au plus.
>
> #### Statistiques du site, sans cookie
> Notre site n'utilise **aucun cookie**. Nous mesurons l'audience avec Umami, installé sur un serveur que nous louons en Suisse (Infomaniak). Il compte les pages vues et les clics sur le téléphone ou les boutons, et note le site d'où vous venez, le type d'appareil et de navigateur, et le pays ou la région. Il ne vous identifie pas et ne conserve pas votre adresse IP. Ce que vous tapez dans les formulaires ne lui est jamais envoyé. Ces statistiques sont gardées [24 mois].
>
> Le site garde aussi dans votre navigateur, le temps que l'onglet reste ouvert (« stockage de session »), la provenance de votre visite, pour la joindre à votre demande si vous en envoyez une, et un repère indiquant que vous avez commencé un formulaire. Rien n'est transmis à un tiers, et tout disparaît quand vous fermez l'onglet.
>
> Si votre navigateur envoie le signal « Ne pas me pister » (Do Not Track) ou « Global Privacy Control », aucune mesure n'est faite et rien n'est enregistré dans votre navigateur. Vous pouvez aussi bloquer ce stockage dans les réglages de votre navigateur : le site et le formulaire fonctionnent quand même. [Si un bandeau de consentement est ajouté pour Google Ads : décrire ici les balises, leur finalité, Google comme destinataire (États-Unis, cadre de protection des données Suisse–États-Unis), et le lien « Paramètres des cookies ».]
>
> #### Vos droits
> Vous pouvez à tout moment, gratuitement :
> - savoir quelles données nous avons sur vous et en recevoir une copie, sous forme électronique si vous le souhaitez ;
> - les faire corriger ;
> - les faire effacer, sous réserve de nos obligations légales de conservation ;
> - retirer un accord donné (conseils par e-mail, photos) et vous opposer à tout message de notre part.
>
> Écrivez-nous à contact@andyconstruct.ch [à confirmer] ou par courrier à l'adresse ci-dessus : nous répondons dans les 30 jours. Si vous estimez que vos droits ne sont pas respectés, vous pouvez vous adresser au Préposé fédéral à la protection des données et à la transparence (PFPDT), www.edoeb.admin.ch.
>
> *Dernière mise à jour : [date de mise en ligne].*

---

## 10. Check-list de mise en production

**Prérequis**
- [ ] DPA signés ou acceptés (hébergeur, Infomaniak, Pipedrive, Brevo, ASPSMS, Pingen, agence) et archivés
- [ ] SPF, DKIM, DMARC en place ; test mail-tester ≥ 9/10 pour `site@` et pour Brevo
- [ ] Rôles « bureau » et « terrain » confirmés ; horaires et délais de rappel confirmés (copy deck C01, C03)
- [ ] Politique de confidentialité relue par le juriste et publiée (`/confidentialite.html`) ; le texte de `tools/build/page_autres.py` reprend la version corrigée du §9 (relecture du 31.10.2026)
- [ ] Points bloquants de `docs/v2/qa/relecture-juridique-copy.md` (check-list) levés

**Hébergement PHP**
- [ ] `config.php` rempli, **`mode_test => false`**, `n8n.simuler => false`, trois secrets distincts de 64 caractères
- [ ] Stockage hors de la racine web, droits 0750 ; `cron.php` planifié toutes les 10 min (sortie vérifiée)
- [ ] `/api/config.php`, `/api/lib/`, `/api/vendor/`, `/api/data/`, stockage → 403 ou 404
- [ ] `upload_max_filesize` 8M, `post_max_size` 26M, `display_errors` Off
- [ ] Une vraie demande de test reçue par les associés (e-mail interne lisible sur mobile, bouton « Appeler »)

**n8n**
- [ ] Version fixée, HTTPS, double authentification, sauvegardes actives
- [ ] `verifier.py` sans erreur ; 16 workflows importés ; identifiants reliés ; WF13 défini comme workflow d'erreur partout
- [ ] Variables `.env` complètes (Pipedrive : IDS et CHAMPS vérifiés sur une affaire de test)
- [ ] Healthchecks reçoit l'horloge et le cron PHP
- [ ] Recette des 20 cas du §6.2 passée, puis données de test effacées

**Frontend**
- [ ] Champs, valeurs et réponses conformes à `contrat-interface.md` ; pas de case de consentement ; mention d'information sous le bouton
- [ ] `suivi.js` chargé avant Umami ; `data-domains` = domaine de production ; aucun script Umami en preview
- [ ] `/merci.html` en `noindex` ; `robots.txt` : `Disallow: /api/`

**Après la mise en ligne (J+1, J+7, J+30)**
- [ ] Journal : taux de spam, échecs SMTP, file d'attente vide
- [ ] Délai médian de premier contact relevé ; promesse de délai ajustée si besoin
- [ ] Premier rapport mensuel reçu et commenté

---

## 11. Limites connues et points à valider

| Sujet | État |
|---|---|
| API simap | Noms des paramètres de recherche à confirmer sur simap.ch/api-doc ; le tri fin est fait dans n8n et l'abonnement e-mail natif reste le filet de sécurité |
| Table NPA → zone | Construite par plages de NPA et ~350 communes ; à compléter avec le répertoire officiel des localités (opendata.swiss) si une commune est mal classée |
| PDF compressés | Le contrôle « PDF actif » lit le fichier brut : un script caché dans un flux compressé n'est pas détecté (le fichier reste stocké hors web et n'est ouvert que par les associés) |
| Pipedrive | Clés des champs, filtres et étapes à relever lors de la configuration ; l'alternative Brevo CRM demande une adaptation de WF01-WF03 |
| n8n Cloud | Pas de variables d'environnement : remplacer `$env` par `$vars` ; module `crypto` à vérifier |
| Séquence des conseils (WF07) | Seules pauses longues de n8n (3 et 5 jours) : conservées en base, mais une réinstallation complète les perd (acceptable : 2 e-mails facultatifs) |
| Rapport mensuel | Dépenses publicitaires et Google Ads à compléter par l'agence |
| WF05 (récapitulatif du lundi), WF11 (avis Google par API), WF15 (fiche projet) | Non livrés : le récapitulatif du soir (WF03), le bouton « Avis reçu » (WF02) et les tâches CRM couvrent l'essentiel au lancement |
| Juriste | Politique de confidentialité, mentions d'opposition, qualification « de masse » des messages, stockage de session pour l'attribution, dispense de registre |
