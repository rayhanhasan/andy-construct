# Admin Andy Construct : installation et exploitation (MVP)

*Agence technique · 7 novembre 2026 · pour : l'agence (mise en ligne, maintenance) et les associés (création des comptes).*
*Plan de référence : `plan-dashboard-admin.md` (option A, admin maison). Maquette : `maquette/`.*

## 1. Ce que fait le MVP

- **Chaque demande du site entre en base** (devis, rappel, guide par la poste) : `site/api/lib/Traitement.php` appelle `Depot` **après** l'e-mail interne et le webhook n8n. Le score détaillé, la priorité, l'échéance de rappel, la source (catégorie, canal du §5.4, UTM, gclid avec consentement, référent, pages) et les fichiers sont enregistrés. **Base indisponible** : la demande part quand même (e-mail, accusé, n8n) et elle est écrite dans `stockage/file-attente-base/`, puis insérée par `cron.php` (ou après la réponse au visiteur), sans doublon (la référence est unique).
- **Écrans** (`/admin/`) : Vue d'ensemble (5 indicateurs du §5 face à l'objectif, alertes, entonnoir, demandes par mois), À traiter (téléphone d'abord), Demandes (liste filtrable, recherche, vue colonnes avec changement de statut), Fiche demande (coordonnées, projet, fichiers, score détaillé, attribution, historique, notes, actions), Saisie d'un appel (score calculé pendant la saisie, même `Traitement` que le site), Acquisition (demandes, signés, CPL, CAC, ROAS, ROI par canal), Paramètres (utilisateurs, dépenses mensuelles, objectifs et économie), Journal et données personnelles (audit, export, effacement), Mon compte.
- **Statuts et transitions du §4.5**, vérifiés par le serveur (une transition interdite envoyée à la main est refusée ; « Perdue » sans motif et « Signée » sans montant sont impossibles). Chaque transition écrit l'historique et le journal d'audit.
- **Sécurité** : comptes en base, mots de passe argon2id (12 caractères au moins), double authentification TOTP obligatoire (RFC 6238, sans bibliothèque externe) et 10 codes de secours, secrets TOTP chiffrés en base (libsodium), session PHP (cookie `__Host-`, `Secure`, `HttpOnly`, `SameSite=Lax`, identifiant renouvelé à chaque étape, fin après 8 h d'inactivité), jeton CSRF sur tous les POST, blocage du compte 15 minutes après 5 échecs, limite d'essais par adresse IP, journal d'audit sans valeur personnelle, CSP stricte (aucun script ni style en ligne), `noindex`, `no-store`. Quatre rôles (§6.5) ; le rôle « Agence, marketing » ne voit aucune donnée personnelle.

## 2. Prérequis

- PHP 8.1 ou plus récent avec `pdo_sqlite` (SQLite) ou `pdo_mysql` (MariaDB), `sodium`, `mbstring`, `intl` conseillé. HTTPS obligatoire.
- **SQLite par défaut** (fichier `stockage/base/andy-construct.sqlite`, dossier privé déjà protégé). **MariaDB 10.6+ recommandée en production** (plan §2.3) : l'API, l'admin et n8n écrivent en même temps et le verrouillage de SQLite n'est pas fiable sur un disque réseau.

## 3. Installation

1. Déployer le site comme d'habitude (`python3 tools/build/build.py --production --out <dossier>`) : `site/admin/` est copié avec le reste ; `admin/outils/demo.php` n'est **jamais** copié en production. `robots.txt` exclut `/admin/` et la CSP de la racine ne s'applique pas à `/admin/` (il envoie la sienne).
2. Dans `api/config.php` (le même fichier que l'API, hors dépôt) :
   - `secrets.admin` : 32 caractères au moins (`php -r 'echo bin2hex(random_bytes(32)), PHP_EOL;'`). Il chiffre les secrets de double authentification : **ne plus le changer** ensuite (sinon, réinitialiser la 2FA de chacun).
   - `base` : laisser `dsn` vide pour SQLite, ou pour MariaDB :
     ```php
     'base' => ['actif' => true, 'dsn' => 'mysql:host=localhost;dbname=andy_construct;charset=utf8mb4', 'utilisateur' => 'andy_app', 'mot_de_passe' => '…'],
     ```
     Le schéma se crée seul au premier accès (migrations numérotées et idempotentes, table `migration`).
   - `admin.url`, `admin.cookie_securise` (laisser `true` en ligne).
3. Vérifier que `cron.php` tourne toutes les 10 minutes (il rejoue aussi la file de la base).
4. Ouvrir `https://www.andyconstruct.ch/admin/` : la page de connexion doit s'afficher, et `https://www.andyconstruct.ch/admin/lib/App.php` doit répondre 403.

## 4. Créer le premier compte

Sur le serveur (SSH), depuis la racine du site :

```bash
php admin/outils/creer-utilisateur.php --email=prenom@andyconstruct.ch --nom="Prénom Nom" --role=associe --role-metier=terrain
```

Le mot de passe est demandé sans écho. La commande affiche **une seule fois** la clé TOTP (à saisir dans Google Authenticator, Microsoft Authenticator, 1Password…, ou à transformer en code QR avec `qrencode -t ansiutf8 '<adresse otpauth>'`) et les 10 codes de secours. Les comptes suivants se créent dans **Paramètres, Utilisateurs et rôles** (associés seulement). Rôle métier : « terrain » reçoit les demandes de particuliers, « bureau » les demandes B2B (comme `config.php → associes`).

## 5. Essai en local (données de démonstration)

```bash
# configuration de démonstration hors dépôt (mode_test => true, stockage dans un dossier temporaire)
export AC_API_CONFIG=/chemin/config-demo.php
php site/admin/outils/demo.php --oui-base-de-demonstration --vider   # comptes et demandes FICTIFS
php -S 127.0.0.1:8093 -t site                                         # puis http://127.0.0.1:8093/admin/
```

`demo.php` refuse de tourner sans `mode_test => true` et sans l'option explicite : **ne jamais l'exécuter en production**. Comptes de démonstration (mot de passe « demo chantier fictif ») : `alex.modele@exemple.test` (associé, terrain), `camille.exemple@exemple.test` (associé, bureau), `dominique.essai@exemple.test` (secrétariat), `agence.fictive@exemple.test` (agence marketing). Les clés TOTP fixes sont affichées par le script ; le code du moment s'obtient avec la commande qu'il imprime.

## 6. Tests

```bash
php site/admin/tests/run.php     # TOTP (vecteurs RFC 6238), base, enregistrement et rejeu, transitions,
                                 # indicateurs §5, authentification, CSRF, accès page par page, rôle agence, nLPD
php site/api/tests/run.php       # endpoint des formulaires (inchangé, toujours vert)
bash site/api/tests/endpoint.sh
```

## 7. Sauvegarde et restauration

- **SQLite** : copier `stockage/base/andy-construct.sqlite` à chaud avec `sqlite3 andy-construct.sqlite ".backup sauvegarde.sqlite"` (ou PHP : `VACUUM INTO`), puis chiffrer (`age` ou `gpg`) et envoyer sur le VPS Infomaniak (rotation 30 jours, plan §6.5). Copier aussi `stockage/fichiers/`.
- **MariaDB** : `mysqldump --single-transaction andy_construct | gzip | age -r <clé> > andy-$(date +%F).sql.gz.age`.
- **Restauration** : à tester à la mise en service puis chaque trimestre sur un environnement de test (critère d'acceptation 11).
- Un effacement (nLPD) est complet dans les sauvegardes au plus tard 30 jours après : à dire dans la politique de confidentialité.

## 8. Exploitation

- **Mot de passe oublié** : un associé remplace le mot de passe (Paramètres, Utilisateurs). **Téléphone perdu** : un associé réinitialise la 2FA (nouvelle clé et nouveaux codes affichés une fois), ou la personne utilise un code de secours.
- **Compte bloqué** (5 échecs) : se débloque seul après 15 minutes.
- **Journal** : Journal et données personnelles (200 dernières entrées) ; journaux PHP dans `stockage/journaux/php-erreurs.log`.
- **Données personnelles** : recherche par e-mail ou téléphone, export JSON, effacement par anonymisation (confirmation en tapant la référence) ; les indicateurs ne changent pas.

## 9. Ce qui reste à faire

**Avant la mise en ligne (MVP, plan §7.2)**
- Décisions client G1 à G14 (§7.4), en particulier marge brute et panier de référence (valeurs illustratives : 30 % et CHF 9'000), mois de mise en ligne (M1), hébergeur et MariaDB.
- Revue de sécurité par une seconde personne, OWASP ZAP « baseline », test de restauration, formation d'une heure.
- Cookie `SameSite=Lax` (choix du 08.11.2026) : un lien vers une fiche ouvert depuis un SMS ou un e-mail garde la session ; les POST restent protégés par le jeton CSRF.
- API interne signée HMAC pour n8n (§6.3) et adaptation des 14 workflows (lot 8) ; page « en un clic » hors session (E14).
- Purge automatique à 24 mois, purge du journal à 12 mois, registre des demandes de droits (E13), import du tableur `suivi-demandes-et-kpi.xlsx`.
- Bouton « Ouvrir la fiche » dans l'e-mail interne ; fichiers reçus déplacés dans `stockage/dossiers/<demande>/` (aujourd'hui ils restent dans `stockage/fichiers/` et sont purgés à 30 jours : la fiche l'indique « plus sur le serveur »).
- Appareils de confiance 30 jours, liste et révocation des appareils, e-mail lors d'une connexion depuis un nouvel appareil ou d'un blocage.
- Notifications « sauf vers l'auteur de la saisie » (aujourd'hui l'e-mail interne part à tous), fusion manuelle des doublons, réattribution groupée, glisser-déposer des colonnes, ICS des visites.

**V2 (plan §7.1)** : Acquisition complète (tendances, bloc Google Ads, import des coûts), lectures quotidiennes (Umami, Search Console, Places), SEO et visibilité, Avis, Rapport mensuel figé, Offres et chantiers (relances J+3/J+10/J+21 envoyées par n8n, chantiers, capacité), prospection B2B, clés d'accès (passkeys), manifeste d'écran d'accueil.
**V3** : conversions hors ligne Google Ads, Business Profile, recalibrage du score, synchronisation du logiciel d'offres.
