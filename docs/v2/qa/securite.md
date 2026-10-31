# Audit de sécurité : endpoint des formulaires, suivi et automatisations n8n

| | |
|---|---|
| Date | 31 octobre 2026 |
| Référentiel | OWASP ASVS 4.0.3, niveau 2 (chapitres V1, V2.9, V3.4, V4, V5, V7, V8, V9, V10.3, V11, V12, V13, V14) |
| Périmètre | `site/api/` (PHP 8.3, PHPMailer 6.12.0), `site/assets/js/suivi.js`, `site/.htaccess`, `automation/n8n/*.json` (HMAC, liens en un clic, désinscription), `automation/Caddyfile`, `automation/docker-compose.yml` |
| Méthode | Lecture complète du code ; attaques locales (`php -S localhost:8097 -t site` avec une configuration de test, Apache 2.4 + mod_php via `endpoint.sh`) ; fuzzing de tous les champs (1'204 requêtes : tableaux imbriqués, UTF-8 invalide, 30'000 caractères, `$_FILES` forgés) ; exécution à blanc des nœuds Code n8n (harnais de `verifier.py`) |
| Documentation de référence | `docs/v2/contrat-interface.md`, `docs/v2/automatisation.md` |

## 1. Synthèse

| Gravité | Constats | Corrigés dans ce lot |
|---|---|---|
| Critique | 0 | – |
| Élevée | 1 | 1 |
| Moyenne | 5 | 5 |
| Faible | 12 | 5 |
| Info | 6 | 2 |
| **Total** | **24** | **13** |

Aucun accès non authentifié aux fichiers reçus, aux secrets ou à `cron.php`, aucune injection d'en-tête e-mail, aucun XSS dans l'e-mail interne, aucune SSRF. Le risque principal était l'usage du formulaire comme **relais d'e-mails d'hameçonnage** signés par le domaine de l'entreprise (S-01), aggravé par une limite de débit contournable en IPv6 (S-04) ou par en-têtes de proxy (S-05). Côté n8n, deux pages publiques réinjectaient un paramètre sans échappement (S-02) et un e-mail interne reprenait le nom saisi sans échappement (S-06).

Tests après correction : `php site/api/tests/run.php` **266 / 266** (232 avant : +30 sécurité, +4 configuration) · `bash site/api/tests/endpoint.sh` **57 / 57** (52 avant, +5, Apache compris) · `python3 automation/n8n/verifier.py` **39 / 39** (28 avant : +5 sécurité, +6 relecture juridique, voir §5). Chaque nouveau test a été vérifié en échec sur la version d'avant correction.

## 2. Tableau des constats

| ID | Gravité | Constat | ASVS | Statut |
|---|---|---|---|---|
| S-01 | **Élevée** | Formulaire utilisable comme relais d'e-mails : accusé de réception envoyé à n'importe quelle adresse, avec lien cliquable arbitraire (adresse du guide) et texte libre (nom, domaines nus) | V5.2, V11.1.4 | Corrigé |
| S-02 | Moyenne | Injection HTML réfléchie dans les pages GET de WF02 (`/ac-action`) et WF12 (`/ac-stop`) : paramètre `t` réinjecté sans échappement, jeton « `charge.sig.<n'importe quoi>` » accepté | V5.3.3, V3.5 | Corrigé |
| S-03 | Moyenne | Filtre des PDF actifs contournable : JavaScript dans un flux d'objets compressé (`/ObjStm`), après un commentaire `%`, filtres en cascade ; XFA non détecté | V12.2.1 | Corrigé |
| S-04 | Moyenne | Limite de débit par adresse IPv6 complète : un abonné dispose d'un /64 (2^64 adresses), la limite ne tient pas | V11.1.4 | Corrigé |
| S-05 | Moyenne | Avec `faire_confiance_au_proxy = true`, IP lue dans `X-Forwarded-For` (entrée la plus à gauche, écrite par le client) ou `CF-Connecting-IP` quelle que soit la provenance : contournement total de la limite de débit | V11.1.4, V14.5 | Corrigé |
| S-06 | Moyenne | HTML stocké dans les messages n8n : nom et commune du formulaire (via Pipedrive) insérés sans échappement dans l'e-mail d'escalade WF03 ; note Pipedrive WF07 ; liens des récapitulatifs WF08 / WF10 (guillemet non échappé) | V5.3.3 | Corrigé |
| S-07 | Faible | Chevrons `< >` acceptés dans les champs d'identité et d'adresse (cause racine de S-06, transmis tels quels au CRM) | V5.1.3 | Corrigé |
| S-08 | Faible | n8n : `timingSafeEqual` après comparaison de longueurs **en caractères** : une signature multi-octets de même longueur lève une exception (erreur de workflow, alerte WF13 déclenchable à volonté) | V11.1, V7.4 | Corrigé |
| S-09 | Faible | Avertissements PHP sur entrées forgées (`formulaire[]` → « Undefined array key canal », `$_FILES` forgé → « Array to string conversion ») : bruit dans les journaux | V5.1.4, V7.4.1 | Corrigé |
| S-10 | Faible | `X-Powered-By: PHP/8.3.6` envoyé : `expose_php` est `PHP_INI_SYSTEM`, sans effet dans `.user.ini` | V14.3.3 | Corrigé |
| S-11 | Faible | `tests/run.php` et `tests/faux-n8n.php` exécutables depuis le web si le `.htaccess` est ignoré (nginx, `AllowOverride None`) : lancement de serveurs PHP (`proc_open`), charge | V14.1.4 | Corrigé |
| S-12 | Faible | Piège temporel facultatif : jeton absent accepté (envoi sans JavaScript), jeton réutilisable 12 h | V11.1.2 | Accepté (choix documenté) |
| S-13 | Faible | Webhook HMAC sans anti-rejeu dans la fenêtre de 5 min (pas de nonce, pas de dédoublonnage par `ref`) ; usage unique des actions irréversibles WF02 en mémoire statique, non atomique | V11.1.3 | Recommandation |
| S-14 | Faible | HEIC : seule la boîte `ftyp` est contrôlée, contenu arbitraire accepté et joint à l'e-mail interne ; JPEG polyglotte avec `<?=` accepté (stockage non exécutable) | V12.2.1 | Recommandation |
| S-15 | Faible | Journaux non bornés : chaque refus (`fichier.php`, origine, débit) écrit une ligne ; `php-erreurs.log` jamais purgé (mtime toujours récent) | V7.1, V11.1.4 | Recommandation |
| S-16 | Faible | WF14 : « STOP » et « a répondu » détectés sur l'en-tête `From` (usurpable) : un tiers peut désinscrire un prospect ou arrêter ses relances | V2.x (authenticité) | Recommandation |
| S-17 | Faible | Secrets et données dans des URL : e-mail en clair (base64) dans le jeton de désinscription valable 400 jours ; `cron.php?cle=` journalisé par Apache et n8n | V8.3.1 | Recommandation |
| S-18 | Faible | `site/.htaccess` (généré, mode preview) : HSTS et redirection HTTPS commentés | V9.1.1, V14.4.5 | À activer en production |
| S-19 | Info | Ancre `$` sans modificateur `D` (`MOTIF_ID`, signature) : un saut de ligne final passait la regex (non exploitable : signature exigée) | V5.1.4 | Corrigé |
| S-20 | Info | Page d'erreur sans JS : un référent `javascript://www.andyconstruct.ch/%0A…` devenait le lien de retour (Referer non forgeable par un tiers, CSP bloquante) | V5.1.5 | Corrigé |
| S-21 | Info | `config.example.php` livré avec `mode_test => true` ; secrets vides acceptés en mode test | V14.1, V6.4 | Recommandation |
| S-22 | Info | `Origin` absent accepté ; `origines_autorisees` vide = toutes acceptées (ouverture par défaut). CSRF peu pertinent pour un formulaire public anonyme | V4.2.2, V13.2.3 | Accepté |
| S-23 | Info | n8n : URL de webhook `http://` acceptée par le PHP ; éditeur n8n exposé sur le même domaine que les webhooks ; image `stable` flottante | V9.2.1, V14.2 | Recommandation |
| S-24 | Info | PHPMailer 6.12.0 : aucune CVE connue (les dernières visent < 6.5.0 : CVE-2021-3603, CVE-2021-34551 ; < 6.1.6 : CVE-2020-13625) ; `vendor/` sans `examples/` ni `get_oauth_token.php` | V14.2.1 | Conforme |

## 3. Constats détaillés, preuves et correctifs

Préparation commune des preuves (configuration isolée, jamais `site/api/config.php`) :

```bash
SP=$(mktemp -d)
sed -e "s#__DIR__ . '/stockage'#'$SP/stockage'#" \
    -e "s#'hmac_webhook' => ''#'hmac_webhook' => 'audit-hmac-0123456789abcdef0123456789abcdef'#" \
    -e "s#'actions' => ''#'actions' => 'audit-actions-0123456789abcdef0123456789abcd'#" \
    -e "s#'local' => ''#'local' => 'audit-local-0123456789abcdef0123456789abcdef0'#" \
    site/api/config.example.php > "$SP/config.php"
AC_API_CONFIG="$SP/config.php" php -S localhost:8097 -t site &
B=http://localhost:8097/api/demande.php; O='Origin: http://localhost:8097'
J=$(curl -s "$B?jeton" | jq -r .jeton); sleep 4
```

### S-01 · Élevée · Relais d'e-mails d'hameçonnage par l'accusé de réception

**Description.** L'accusé de réception part vers l'adresse saisie par le visiteur, depuis le domaine de l'entreprise (SPF/DKIM alignés), avec du texte repris du formulaire. La documentation annonçait « liens masqués », mais seul l'extrait du message l'était : le nom (100 car.), la commune et surtout l'**adresse d'envoi du guide** (300 car., non contrôlée par l'anti-spam) arrivaient tels quels, et `https://…` y devenait un **lien cliquable** dans la version HTML. Seul garde-fou : 5 demandes par heure et par IP, contournable (S-04, S-05). Impact : hameçonnage signé par le domaine, mise en liste noire du domaine (les e-mails légitimes des associés ne passent plus).

**Preuve (avant correction).**

```bash
curl -s -H 'Accept: application/json' -H "$O" -F formulaire=envoi_postal_guide -F guide=guide-reduire-le-bruit \
  -F 'nom=GAGNANT iPhone 17 reclamez-le sur bit.ly/xyz' --form-string 'adresse=https://evil.example/phish?gagne=1' \
  -F npa=1227 -F localite=Carouge -F email=victime@exemple.ch -F "form_t0=$J" $B
# {"ok":true,…,"ref":"AC-2026-0001"}
grep -o '<a href="https://evil[^"]*"' "$SP"/stockage/test-mails/*accuse*.eml   # lien cliquable présent
grep '^To:' "$SP"/stockage/test-mails/*accuse*.eml   # To: "GAGNANT iPhone 17 reclamez-le sur bit.ly/xyz" <victime@exemple.ch>
```

**Correctif** (`lib/Traitement.php`, `lib/AntiSpam.php`, `lib/Modeles.php`, `lib/Config.php`, `config.example.php`) :

```diff
 // Traitement::distribuer()
             $accuse = $this->modeles->accuse($demande);
+            if ($accuse !== null && !$demande['saisie_interne'] && !$this->accuseAutorise($d['email'], $demande['recu_le']->getTimestamp(), $demande['ref'])) {
+                $accuse = null;
+                $bilan['accuse'] = 'limite';      // demande traitée, accusé non envoyé
+            }
+    private function accuseAutorise(string $email, int $maintenant, string $ref): bool
+    {
+        $limiteur = new LimiteDebit($this->stockage, $this->config->secret('local') . '|accuse');
+        $parAdresse = $limiteur->tenter('email|' . strtolower($email), 'accuse-adresse', max(1, (int) $this->config->get('anti_spam.accuses_par_adresse_24h', 3)), $maintenant, 86400);
+        if (!$parAdresse['autorise']) { $this->journal->alerte('accuse_limite', ['ref' => $ref, 'seau' => 'adresse']); return false; }
+        $global = $limiteur->tenter('site', 'accuse-global', max(1, (int) $this->config->get('anti_spam.accuses_par_heure', 20)), $maintenant);
+        if (!$global['autorise']) { $this->journal->alerte('accuse_limite', ['ref' => $ref, 'seau' => 'global']); return false; }
+        return true;
+    }
 // AntiSpam::contenuSuspect()
+        $autresChamps = ($donnees['adresse'] ?? '') . ' ' . ($donnees['localite'] ?? '') . ' ' . ($donnees['recommande_par'] ?? '');
+        if (preg_match('~https?://|www\.~i', $autresChamps)) {
+            return 'lien_dans_adresse';   // réponse leurre, rien n'est envoyé
+        }
 // Modeles : liens et domaines nus masqués dans tout ce qui est repris (salutation, To, lieu, adresse, extrait)
-        $m->a = [[$d['email'], trim($d['prenom'] . ' ' . $d['nom'])]];
+        $m->a = [[$d['email'], self::neutraliserLiens(trim($d['prenom'] . ' ' . $d['nom']))]];
-        $extrait = preg_replace('~https?://\S+|www\.\S+~i', '[lien]', $d['message']) ?? '';
+        $extrait = self::neutraliserLiens($d['message']);
-            'salutation' => self::salutation($d['civilite'], $d['nom'], $d['prenom']),
+            'salutation' => self::neutraliserLiens(self::salutation($d['civilite'], $d['nom'], $d['prenom'])),
-            'adresse_envoi' => $d['adresse_postale'],
+            'adresse_envoi' => self::neutraliserLiens($d['adresse_postale']),
+    public static function neutraliserLiens(string $texte): string
+    {   // URL, « www. », domaine nu suivi d'un chemin (bit.ly/xyz), domaine nu en .com/.net/.xyz/… ;
+        // « Rte.de Lausanne », « St.Gallen » ne sont pas touchés.
```

Nouvelles clés : `anti_spam.accuses_par_adresse_24h` (3), `anti_spam.accuses_par_heure` (20). Le webhook reçoit `accuse_reception: "limite"` quand l'accusé n'est pas parti. Tests : groupe « relais d'e-mails (S-01) » de `run.php` (6 contrôles) et `endpoint.sh` §12.

Risque résiduel : un domaine nu en `.ch` sans chemin (« exemple.ch ») reste affiché en texte ; il n'est jamais cliquable dans notre HTML et les plafonds bornent l'abus.

### S-02 · Moyenne · Injection HTML réfléchie dans les pages n8n `/ac-action` et `/ac-stop`

**Description.** Les nœuds « Page de confirmation » de WF02 et WF12 écrivaient `value="' + t + '"` avec la valeur brute du paramètre `t`. La vérification du jeton découpait sur `.` et ignorait les morceaux en trop : un jeton **valable** suivi de `."><…>` passait. Tout prospect reçoit des jetons valables (relances d'offre, demande d'avis, désinscription). La CSP (`default-src 'none'`) bloque les scripts, mais pas `<meta http-equiv="refresh">` : redirection ou faux formulaire de connexion sur le domaine de confiance n8n.

**Preuve (avant correction).**

```
GET https://n8n.andyconstruct.ch/webhook/ac-stop?t=<jeton reçu par e-mail>."><meta http-equiv="refresh" content="0;url=https://evil.example/">
→ <input type="hidden" name="t" value="eyJh….ecBW…."><meta http-equiv="refresh" content="0;url=https://evil.example/">">
```

Reproduction hors ligne : `python3 automation/n8n/verifier.py` (contrôle « wf02 / wf12 refuse un jeton suivi de HTML »), en échec sur la version d'origine.

**Correctif** (14 nœuds Code, fonction `verifierJeton` commune ; pages de WF02 et WF12) :

```diff
-  const [charge, sig] = String(jeton || '').split('.');
+  const parties = String(jeton || '').split('.');
+  if (parties.length !== 2) return null; // exactement « charge.signature »
+  const [charge, sig] = parties;
   if (!charge || !sig || secret.length < 32) return null;
-  const attendue = b64(crypto.createHmac('sha256', secret).update(charge).digest());
-  if (attendue.length !== sig.length || !crypto.timingSafeEqual(Buffer.from(attendue), Buffer.from(sig))) return null;
+  const attendue = Buffer.from(b64(crypto.createHmac('sha256', secret).update(charge).digest()));
+  const recue = Buffer.from(sig);
+  if (attendue.length !== recue.length || !crypto.timingSafeEqual(attendue, recue)) return null;
 // WF02 et WF12, « Page de confirmation »
+const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
-  + '<form method="post" action=""><input type="hidden" name="t" value="' + t + '">' + boutons + '</form>';
+  + '<form method="post" action=""><input type="hidden" name="t" value="' + esc(t) + '">' + boutons + '</form>';
-const corps = (d.r ? '<p>Référence : <strong>' + d.r + '</strong></p>' : '') + …
+const corps = (d.r ? '<p>Référence : <strong>' + esc(d.r) + '</strong></p>' : '') + …
-const choix = d.a === 'menu' ? [...] : [d.a];
+const choix = (d.a === 'menu' ? [...] : [d.a]).filter((c) => LIBELLES[c]);
```

Le principe GET (page avec bouton) puis POST (action) est conservé : la prélecture des liens par les messageries ne déclenche rien.

### S-03 · Moyenne · PDF actifs non détectés

**Description.** `pdfActif()` cherchait `/JavaScript`, `/JS`, `/Launch`… dans les octets bruts, suivis d'un blanc ou de `/ < ( [`. Contournements : (1) placer l'action dans un flux d'objets compressé `/ObjStm` (cas courant de tout PDF 1.5+), (2) `/JS%commentaire⏎(…)` ou `/S/JavaScript>>`, (3) double `FlateDecode`, (4) formulaire XFA (porte du JavaScript). Le PDF part en pièce jointe aux associés.

**Preuve (avant correction).**

```bash
php -r '$z = gzcompress("3 0 << /S /JavaScript /JS (app.alert(1)) >>"); echo "%PDF-1.5\n1 0 obj << /Type /Catalog /OpenAction 3 0 R >> endobj\n4 0 obj\n<< /Type /ObjStm /N 1 /First 4 /Filter /FlateDecode /Length ".strlen($z)." >>\nstream\n$z\nendstream\nendobj\n%%EOF\n";' > objstm.pdf
curl -s -H 'Accept: application/json' -H "$O" -F formulaire=devis -F nom=Test -F telephone=0791234567 \
  -F travaux=placo -F commune=Genève -F "form_t0=$J" -F "fichiers[]=@objstm.pdf;type=application/pdf" $B
# {"ok":true,…}  → PDF accepté et joint à l'e-mail interne
```

**Correctif** (`lib/Televersement.php`) : noms terminés par tout délimiteur PDF (`(?![^\s\0()<>\[\]{}/%])`) ; `XFA` et `EmbeddedFiles` ajoutés ; décompression bornée (256 Mo au total, par morceaux de 8 Ko, arrêt sur la fin du flux zlib et non sur `endstream`) des flux zlib qui contiennent des objets ou du texte, filtres en cascade jusqu'à 3 niveaux ; images ignorées (pas de faux positif) ; refus prudent si non inspectable (LZW, ASCII85, ASCIIHex, `/Encrypt` + `/ObjStm`, bombe de décompression).

```diff
-        return (bool) preg_match('~/(JavaScript|JS|Launch|EmbeddedFile|RichMedia)[\s/<(\[]~', $normalise);
+        if (preg_match('~/(JavaScript|JS|Launch|EmbeddedFiles?|RichMedia|XFA)' . self::FIN_NOM . '~', $normalise)) return true;
+        if (preg_match('~/(LZWDecode|ASCII85Decode|ASCIIHexDecode|LZW|A85|AHx)' . self::FIN_NOM . '~', $normalise)
+            || (str_contains($normalise, '/Encrypt') && str_contains($normalise, '/ObjStm'))) return true;
+        while (($debut = strpos($contenu, 'stream', $pos)) !== false) { … if (self::fluxActif($contenu, $depart, $budget, 0)) return true; }
```

Mesures : bombe de 300 Mo refusée en 1,6 s ; image Flate de 100 Mo (blanc) acceptée en 30 ms ; dessin de 30 Mo accepté en 90 ms ; 0 faux positif sur 5 flux aléatoires de 2 Mo ; mémoire maximale 25 Mo. Tests : groupe « PDF actifs cachés (S-03) » de `run.php` (7 contrôles) et `endpoint.sh` §12.

### S-04 · Moyenne · Limite de débit contournable en IPv6

**Description.** L'empreinte portait sur l'adresse complète. Un abonné IPv6 dispose d'un préfixe /64 : chaque envoi depuis une nouvelle adresse du préfixe repart de zéro (5 demandes, 30 tentatives, et donc S-01 sans limite).

**Preuve (avant correction).**

```bash
php -r 'require "site/api/lib/bootstrap.php"; $l = new AndyConstruct\Api\LimiteDebit(new AndyConstruct\Api\Stockage(sys_get_temp_dir()."/l6"), str_repeat("s",32));
for ($i = 1; $i <= 50; $i++) echo $l->tenter("2001:db8:1:2::$i", "demandes", 5)["autorise"] ? "+" : "-";'
# ++++++++++++++++++++++++++++++++++++++++++++++++++  (50 acceptées)
```

**Correctif** (`lib/LimiteDebit.php`) :

```diff
     public function empreinte(string $ip): string
     {
-        return substr(hash_hmac('sha256', 'ip|' . $ip, $this->sel), 0, 32);
+        return substr(hash_hmac('sha256', 'ip|' . self::cle($ip), $this->sel), 0, 32);
     }
+    /** IPv4 telle quelle, IPv6 ramenée au /64, ::ffff:a.b.c.d ramenée à l'IPv4. */
+    public static function cle(string $ip): string { … inet_ntop(substr($binaire, 0, 8) . str_repeat("\0", 8)) . '/64'; }
```

### S-05 · Moyenne · En-têtes de proxy forgeables

**Description.** Avec `faire_confiance_au_proxy = true` (cas documenté de Cloudflare), `ipClient()` prenait `CF-Connecting-IP` ou la première entrée de `X-Forwarded-For` sans vérifier que la connexion venait du proxy. Sur un hébergement mutualisé, le serveur d'origine reste joignable directement : chaque requête choisit son IP.

**Preuve (avant correction**, avec `faire_confiance_au_proxy => true`).

```bash
for i in $(seq 1 40); do curl -s -o /dev/null -w '%{http_code} ' -H 'Accept: application/json' -H "$O" \
  -H "X-Forwarded-For: 10.0.$i.1" -F formulaire=rappel -F 'telephone=022 345 67 89' -F "form_t0=$J" $B; done
# 200 200 200 … (jamais 429)
```

**Correctif** (`lib/LimiteDebit.php`, `lib/Traitement.php`, nouvelle clé `proxys_de_confiance`) :

```diff
-    public static function ipClient(array $server, bool $faireConfianceAuProxy): string
+    public static function ipClient(array $server, bool $faireConfianceAuProxy, array $proxysDeConfiance = []): string
     {
+        $distante = (string) ($server['REMOTE_ADDR'] ?? '0.0.0.0');
+        if (!$faireConfianceAuProxy) return $distante;
+        if ($proxysDeConfiance !== [] && !self::dansPlages($distante, $proxysDeConfiance)) return $distante;
         …
-                    $ip = trim(explode(',', (string) $server[$entete])[0]);
+            // X-Forwarded-For lu de droite à gauche : 1re adresse qui n'est pas un proxy de confiance
+            foreach (array_reverse(array_map('trim', explode(',', $xff))) as $ip) { … }
```

`dansPlages()` gère les CIDR IPv4 et IPv6. **À faire au déploiement** derrière Cloudflare : renseigner `proxys_de_confiance` avec https://www.cloudflare.com/ips/ (sans cette liste, le comportement reste lisible mais forgeable par connexion directe). Tests : groupe « limite de débit, IPv6 et en-têtes de proxy (S-04, S-05) » (10 contrôles).

### S-06 · Moyenne · HTML stocké dans les messages n8n

**Description.** Le nom saisi (`<img src=//evil.example/p.gif>` passait l'anti-spam : pas de `http`) arrive dans Pipedrive puis dans l'e-mail d'escalade WF03 : `html: '<p>' + rendre(MODELES['sms-escalade'].corps, vars) + '</p>…'`, sans échappement. Même défaut pour la note de tâche Pipedrive de WF07 (nom, adresse) et, dans WF08 / WF10, `<a href="$1">` construit après n'avoir échappé que `<` (un `"` dans une URL sortait de l'attribut). Effets : pixel de suivi, lien piégé dans un e-mail interne « de confiance ».

**Preuve (avant correction).** Contrôle « WF03 échappe le nom et la commune » de `verifier.py` sur la version d'origine :

```
<p>Andy · <img src=//evil.example/p.gif> (A, <b>Lancy</b>) n'a pas encore été rappelé(e) …
```

**Correctif.**

```diff
 // WF03 « Délais dépassés »
-      html: '<p>' + rendre(MODELES['sms-escalade'].corps, vars) + '</p><p><a href="' + urlPipedrive(a.id) + '">Ouvrir dans Pipedrive</a></p>' },
+      html: versHtml(rendre(MODELES['sms-escalade'].corps, vars) + '\n\nOuvrir dans Pipedrive : ' + urlPipedrive(a.id)) },
 // WF07 « Préparer » (note de tâche)
-    note: (… ) + c.nom + '<br>' + String(c.adresse_postale || '').replace(/\n/g, '<br>') + '<br>Réf. ' + d.ref },
+    note: [(… ) + c.nom].concat(String(c.adresse_postale || '').split('\n'), ['Réf. ' + d.ref])
+      .map((l) => String(l).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')).join('<br>') },
 // WF08 et WF10 (récapitulatifs)
-texte.replace(/</g, '&lt;').replace(/(https?:\/\/\S+)/g, '<a href="$1">$1</a>')
+texte.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/(https?:\/\/(?:[^\s&]|&amp;)+)/g, '<a href="$1">$1</a>')
```

Défense en profondeur côté PHP : S-07.

### S-07 à S-11, S-19, S-20 · Faible / Info · corrigés

| ID | Preuve (avant) | Correctif |
|---|---|---|
| S-07 | `--form-string 'nom=<img src=//evil.example/p.gif>'` → webhook `"contact":{"nom":"<img src=//evil.example/p.gif>"}` | `Validateur::texte()` (une ligne) : `str_replace(['<', '>'], ' ', $v)` ; idem pour l'ancien champ `adresse_postale` |
| S-08 | `X-AC-Signature: sha256=` + 64 × `é` → `RangeError: Input buffers must have the same byte length` (WF01, WF07, et `verifierJeton` partout) | Comparaison des longueurs sur les `Buffer` (voir diff S-02) ; WF01/WF07 : `bSig.length === bAttendue.length && crypto.timingSafeEqual(bSig, bAttendue)` |
| S-09 | `-F 'formulaire[a]=x'` → « Undefined array key "canal" » ; `fichier[tmp_name][]=x` → « Array to string conversion » | `($d['canal'] ?? '')` ; `Televersement::aplatir()` n'accepte que des chaînes / scalaires |
| S-10 | `curl -sI "$B?jeton"` → `X-Powered-By: PHP/8.3.6` | `bootstrap.php` : `header_remove('X-Powered-By')` (hors CLI) |
| S-11 | Sous nginx ou `AllowOverride None`, `GET /api/tests/run.php` exécute toute la suite (création de dossiers, `php -S`) | `run.php` : `if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }` ; `faux-n8n.php` : idem hors `cli-server` |
| S-19 | `fichier.php?id=<32 hex>.pdf%0A&…` passait la regex (404 au lieu de 403 ; signature quand même exigée) | `MOTIF_ID` et motif de signature avec `/D` |
| S-20 | `Referer: javascript://www.andyconstruct.ch/%0Aalert(1)` → `href="javascript://…"` dans la page d'erreur | Schéma limité à `http` / `https` |

### S-12 à S-18, S-21 à S-24 · non corrigés (recommandations)

| ID | Détail et preuve | Correctif proposé |
|---|---|---|
| S-12 | Un `POST` sans `form_t0` est traité (statut « absent », signalé dans l'e-mail interne) ; un même jeton sert 12 h. Choix assumé (formulaire sans JS, contrat §2) | Si besoin : plafond plus bas pour les envois sans jeton (`tentatives` 5/h), ou jeton à usage unique (mémoriser l'aléa 12 h dans `limites/`) |
| S-13 | Un corps signé capté (TLS rompu, journal) est rejouable 5 min ; deux POST simultanés sur une action irréversible passent tous les deux (mémoire statique lue puis écrite) | WF01/WF07 : refuser une `X-AC-Signature` déjà vue (mémoire statique, 10 min) ; dédoublonner par `ref` ; WF02 : verrou externe (Redis ou champ Pipedrive « action_faite ») |
| S-14 | `printf '\0\0\0\x18ftypheic\0\0\0\0mif1heic<html>…MZ…'` accepté comme `image/heic` | Décoder l'image (Imagick `pingImage`, ou `heif-info`) quand l'extension est disponible ; à défaut, joindre les HEIC sous forme de lien plutôt qu'en pièce jointe |
| S-15 | 1'000 requêtes `fichier.php` invalides = 1'000 lignes de journal ; `php-erreurs.log` grossit sans limite | Agréger les refus (compteur par minute) ; rotation de `php-erreurs.log` dans `Traitement::purger()` (renommer au-delà de 1 Mo) |
| S-16 | Un e-mail usurpé « From: prospect@… », sujet « STOP », désinscrit le prospect (WF14) | Ne traiter que les messages dont `Authentication-Results` indique `dmarc=pass` ou `dkim=pass` ; sinon tâche manuelle |
| S-17 | Jeton de désinscription : `{"a":"stop","e":"x@exemple.ch",…}` lisible en base64 dans l'URL ; `AC_CRON_URL=…/cron.php?cle=…` journalisé | Mettre une référence (ou un hachage) au lieu de l'e-mail ; `cron.php` : accepter la clé dans un en-tête `X-AC-Cron` |
| S-18 | `site/.htaccess` : `# Header always set Strict-Transport-Security …` et redirection HTTPS commentées (fichier généré par `tools/build`, hors périmètre de modification) | En production : décommenter HSTS (`max-age=31536000; includeSubDomains`) et le bloc de redirection, puis regénérer |
| S-21 | Copier `config.example.php` sans le modifier donne `mode_test => true` : aucun e-mail réel, secrets vides acceptés | `mode_test => false` dans le modèle, ou refus au démarrage si `mode_test` et `url_site` de production |
| S-22 | `Origin` absent accepté (anciens navigateurs, clients sans JS) ; liste vide = tout accepté. Un navigateur actuel envoie toujours `Origin` sur un POST inter-sites : le CSRF est bloqué (testé : `Origin: https://attaquant.example` → 403, `null` → 403) | Rendre la liste vide bloquante (`$autorisees === []` → refus) |
| S-23 | `n8n.url_demande = 'http://…'` accepté (données personnelles en clair) ; Caddy publie aussi l'éditeur n8n ; `N8N_VERSION:-stable` | Hors mode test, exiger `https://` ; Caddy : n'exposer que `/webhook/*` (éditeur derrière VPN ou liste d'IP) ; fixer la version |
| S-24 | `vendor/phpmailer/phpmailer/VERSION` = 6.12.0 | Surveiller https://github.com/PHPMailer/PHPMailer/security/advisories ; mise à jour selon `automatisation.md` §7 |

## 4. Points vérifiés sans constat

| Domaine | Vérification |
|---|---|
| Validation et normalisation | Tableaux à la place de chaînes, UTF-8 invalide, 30'000 caractères, marqueurs bidirectionnels, valeurs hors liste : aucune erreur 500 (1'204 requêtes) ; e-mail strict (IDN converti) ; téléphone E.164 ; NPA ; UTM et chemins filtrés |
| Injection d'en-têtes e-mail | `nom=Jean\r\nBcc:`, `email=a@b.ch\r\nBcc:` (refusé), U+0085 et U+2028 dans la commune, objet : aucun en-tête ajouté ; PHPMailer encode tout |
| XSS e-mail interne et accusé | Toutes les valeurs passent par `htmlspecialchars` ; seules les URL `http(s)` de nos propres modèles sont cliquables ; le moteur de modèles ne réinterprète pas les valeurs (`{{…}}` saisi reste du texte) |
| Téléversement | Type réel par `finfo` ; SVG, HTML, exécutable, PHP déguisé, polyglotte `<?php`, > 8 Mo, 4 fichiers : refusés ; nom aléatoire (128 bits) + extension issue du type ; nom d'origine nettoyé (`../../x` → `x`) ; double extension sans effet ; droits 0640 |
| Stockage | Apache : `stockage/…` → 403, PHP non exécuté (`php_flag engine off`, `RemoveHandler`) ; `index.html` ; auto-contrôle quotidien de `cron.php` pour nginx |
| `fichier.php` | HMAC-SHA256 complet (64 hex), `hash_equals`, expiration vérifiée, identifiant strict (pas de traversée, pas d'énumération : 2^128), `attachment` + `nosniff` + `CSP sandbox`, `no-store` |
| `cron.php` | Sans clé ou clé < 24 caractères → 403 ; `hash_equals` ; tableau dans `cle` → 403 |
| SSRF | Aucune URL issue de l'utilisateur n'est appelée (webhooks, Healthchecks, auto-contrôle : configuration seulement) ; cURL sans redirection, `CURLPROTO_HTTP(S)` |
| HMAC du webhook | Secret ≥ 32 caractères, `horodatage.corps`, fenêtre ± 5 min, comparaison à temps constant (n8n), signature refaite à chaque nouvel essai |
| Liens en un clic | GET = page avec bouton, POST = action (prélecture sans effet) ; jeton lié à l'action et à l'affaire ; « stop » inutilisable sur `/ac-action` et inversement |
| Pot de miel, piège temporel | Leurre identique à un succès (`ref: null`) ; jeton signé (HMAC tronqué à 128 bits) |
| Divulgation | `display_errors` désactivé (bootstrap + `.user.ini` + `.htaccess`) ; messages génériques ; journaux sans nom, e-mail, téléphone ni IP |
| En-têtes | API : `nosniff`, `no-store`, `noindex`, `Referrer-Policy`, `X-Frame-Options: DENY`, CSP sur la page d'erreur ; pages n8n : CSP `default-src 'none'`, `frame-ancestors 'none'` ; site : CSP stricte, `Permissions-Policy` |
| Données personnelles | Fichiers 30 j, journaux 30 j, limites 24 h, file d'attente 14 j, e-mails en échec 14 j, exécutions n8n 30 j, prospects 24 mois (WF04p) ; IP hachée avec secret ; erreurs n8n nettoyées (WF13) |
| `suivi.js` | Aucun `innerHTML` ; valeurs placées par `.value` ; UTM et `gclid` tronqués ; `gclid` seulement avec consentement ; DNT / GPC respectés ; propriétés personnelles filtrées ; ni cookie ni `localStorage` |
| Déni de service | `post_max_size` 26 Mo → 413 ; 3 fichiers × 8 Mo ; regex sans retour arrière catastrophique ; Levenshtein borné (80 car.) |

## 5. Corrections demandées par la relecture juridique

Points bloquants de `docs/v2/qa/relecture-juridique-copy.md`, corrigés dans le même lot.

| Point | Avant | Correction | Contrôle |
|---|---|---|---|
| WF03d : opposition (LCD art. 3 al. 1 let. o) | Un « STOP » au J+2 n'arrêtait ni la relance J+9, ni le J+14, ni le SMS : l'opposition n'était pas lue | Nouveaux nœuds « Personne : opposition ? » (lecture de la personne dans Pipedrive) puis « Sans opposition » avant **tout** envoi ; `ne_pas_relancer = oui` sur l'affaire exclut aussi. Lecture impossible ou clé `opposition_marketing` absente de `AC_PD_CHAMPS` = rien n'est envoyé | `verifier.py` : graphe (aucun chemin ne contourne le filtre) et exécution à blanc (opposition → exclue ; personne illisible → exclue) |
| WF07 : appel commercial | Tâche « Appel de courtoisie » à J+2 pour les profils professionnels, non annoncée | Nœuds « Profil professionnel ? » et « Tâche : appel de courtoisie » supprimés ; seule la tâche « envoyer le guide imprimé » reste. Le contrat d'interface ne prévoit aucune case « Je souhaite être rappelé(e) » : aucun appel n'est créé | `verifier.py` : aucun appel dans WF07 |
| WF07 : conseils E2 / E3 après une attente | État Brevo seul, et en échec ouvert (`onError: continue` + `emailBlacklisted !== true` : une erreur Brevo laissait partir l'e-mail) | Après chaque attente : Brevo **et** opposition relue dans Pipedrive ; envoi seulement si `emailBlacklisted === false`, ni réponse ni demande, personne lue sans opposition | `verifier.py` : 5 cas par envoi (aucune opposition, opposition Pipedrive, désinscrit Brevo, Brevo illisible, personne illisible) |
| WF03c : relances d'offre sans téléphone | J+3, J+10 et J+21 par e-mail (3 e-mails) | Sans téléphone : J+3 et J+10 par e-mail, J+21 = étape notée sans message (sortie « autre » du Switch reliée à « Noter l'étape », pour que J+35 et J+45 se produisent) ; avec téléphone : inchangé (e-mail J+3, appel J+10, e-mail J+21) | `verifier.py` : exécution à blanc de 4 affaires |
| `config.example.php` | `entreprise.nom` = « Andy Construct » ; horaires codés « du lundi au vendredi, de 7 h à 18 h » | `nom` = « Andy Construct, Chanton & Cie » (CO art. 954a) ; `horaires` = `''` (non affichés tant que C03 n'est pas confirmé ; les modèles n'écrivent alors aucune virgule). Mêmes valeurs par défaut dans `lib/Config.php` | `run.php` : 4 contrôles (dont l'accusé rendu sans virgule orpheline) |

Documents alignés : `automation/messages/relances-offre.md`, `sequence-aimant.md`, `demande-avis.md` (notes « à valider » devenues décisions), `docs/v2/automatisation.md` (scénarios 15 et 17).

Point restant à vérifier avant activation (hors demande) : WF04e et WF04i lisent `opposition_marketing` sur l'objet `person_id` renvoyé par la liste des affaires Pipedrive ; cette liste ne contient en principe que le nom, l'e-mail et le téléphone de la personne, pas ses champs personnalisés. Si c'est confirmé sur le compte réel, appliquer le même schéma que WF03d (lecture de la personne avant l'envoi).

## 6. Fichiers modifiés

`site/api/lib/` : `LimiteDebit.php`, `Traitement.php`, `AntiSpam.php`, `Validateur.php`, `Modeles.php`, `Televersement.php`, `LiensFichiers.php`, `Config.php`, `bootstrap.php` · `site/api/config.example.php` · `site/api/tests/` : `run.php`, `endpoint.sh`, `faux-n8n.php` · `automation/n8n/` : WF01, WF02, WF03, WF03c, WF03d, WF04e, WF04i, WF07, WF08, WF10, WF12 (`verifierJeton`, échappements ; WF03c, WF03d, WF07 : §5), `verifier.py` (11 contrôles) · `automation/messages/` (3 notes) · `docs/v2/automatisation.md` §3.1 et scénarios 15, 17.

Mise en production : renseigner `proxys_de_confiance` si un proxy est utilisé, réimporter les 11 workflows modifiés dans n8n, vérifier que `AC_PD_CHAMPS` contient `opposition_marketing` et `ne_pas_relancer`, vérifier `mode_test => false`.
