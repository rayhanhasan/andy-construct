#!/usr/bin/env bash
# Test réel du point d'entrée par HTTP (curl), en mode test (aucun envoi).
#
#   bash site/api/tests/endpoint.sh
#
# 1. Serveur PHP intégré : php -S localhost:8099 -t site
#    cas valide (avec photo et plan), pot de miel, envoi trop rapide, fichier
#    piégé, champs manquants, origine étrangère, envoi sans JavaScript.
# 2. Si Apache (apache2 + mod_php) est installé : vérification des règles
#    .htaccess (config, lib, vendor, stockage… refusés ; demande.php ouvert).
#
# Prérequis : php, curl, jq. Code de sortie 0 si tout passe.
set -uo pipefail

RACINE="$(cd "$(dirname "$0")/../../.." && pwd)"
SITE="$RACINE/site"
API="$SITE/api"
PORT="${PORT:-8099}"
BASE="http://localhost:$PORT"
TMP="$(mktemp -d)"
OK=0
KO=0

vert() { printf '  \033[32m✔\033[0m %s\n' "$1"; OK=$((OK + 1)); }
rouge() { printf '  \033[31m✘ %s\033[0m\n' "$1"; [ -n "${2:-}" ] && printf '      %s\n' "$2"; KO=$((KO + 1)); }
verifier() { if [ "$1" = "$2" ]; then vert "$3"; else rouge "$3" "attendu « $2 », obtenu « $1 »"; fi; }

for outil in php curl jq; do
    command -v "$outil" >/dev/null || { echo "Outil manquant : $outil"; exit 2; }
done

# ---------------------------------------------------------------- configuration de test
SECRET_LOCAL="secret-local-endpoint-0123456789abcdef0123456789"
cat > "$TMP/config.php" <<PHP
<?php
\$c = require '$API/config.example.php';
\$c['mode_test'] = true;
\$c['stockage'] = '$TMP/stockage';
\$c['secrets'] = [
    'hmac_webhook' => 'secret-hmac-endpoint-0123456789abcdef0123456789',
    'actions' => 'secret-actions-endpoint-0123456789abcdef01234567',
    'local' => '$SECRET_LOCAL',
];
\$c['destinataires_internes'] = ['associes@andyconstruct.ch'];
\$c['n8n']['simuler'] = true;
\$c['n8n']['url_actions'] = 'https://n8n.exemple.ch/webhook/ac-action';
return \$c;
PHP

# Fichiers de test
php -r '$i = imagecreatetruecolor(80, 60); imagejpeg($i, $argv[1]); ' "$TMP/photo.jpg"
printf '%%PDF-1.4\n1 0 obj << /Type /Catalog >> endobj\ntrailer << /Root 1 0 R >>\n%%%%EOF\n' > "$TMP/plan.pdf"
printf '<?php system($_GET["c"]); ?>' > "$TMP/piege.jpg"
cp "$TMP/photo.jpg" "$TMP/polyglotte.jpg" && printf '<?php echo 1; ?>' >> "$TMP/polyglotte.jpg"

AC_API_CONFIG="$TMP/config.php" php -S "localhost:$PORT" -t "$SITE" > "$TMP/serveur.log" 2>&1 &
PID=$!
arreter() { kill "$PID" 2>/dev/null; [ -n "${PID_APACHE:-}" ] && apache2 -f "$TMP/apache.conf" -k stop 2>/dev/null; rm -rf "$TMP" "$API/stockage-apache-test"; }
trap arreter EXIT
for _ in $(seq 1 50); do curl -s -o /dev/null "$BASE/" && break; sleep 0.1; done

jeton() { curl -s "$BASE/api/demande.php?jeton" | jq -r .jeton; }
nb_mails() { ls "$TMP/stockage/test-mails/"*.eml 2>/dev/null | wc -l | tr -d ' '; }
ORIGINE="Origin: http://localhost:$PORT"

printf '\n\033[1mServeur PHP intégré (%s)\033[0m\n' "$BASE"

J=$(jeton)
case "$J" in v1.*) vert "GET ?jeton → jeton horodaté ($J)";; *) rouge "GET ?jeton" "$J";; esac

# 1. Cas valable : devis complet avec photo et plan (après 4 s, délai minimal du devis)
sleep 4
R=$(curl -s -w '\n%{http_code}' -H 'Accept: application/json' -H "$ORIGINE" \
    -F formulaire=devis -F 'nom=Françoise Dupont' -F civilite=madame -F 'telephone=079 123 45 67' \
    -F email=francoise.dupont@exemple.ch -F 'travaux[]=isolation-acoustique' -F type_client=proprietaire \
    -F surface=15-50 -F delai=1-3-mois -F 'commune=1222 Vésenaz' -F 'message=On entend tout le voisin du dessus.' \
    -F connu_par=recherche-google -F accord=oui -F site_web= -F "form_t0=$J" -F page=/contact.html \
    -F 'utm_source=google' -F 'utm_medium=cpc' -F 'utm_campaign=2026-11_acoustique' \
    -F "fichiers[]=@$TMP/photo.jpg;type=image/jpeg" -F "fichiers[]=@$TMP/plan.pdf;type=application/pdf" \
    "$BASE/api/demande.php")
CODE=$(tail -n1 <<<"$R"); CORPS=$(sed '$d' <<<"$R")
verifier "$CODE" 200 "devis valable avec 2 fichiers → 200"
verifier "$(jq -r .ok <<<"$CORPS")" true "réponse ok:true"
REF=$(jq -r .ref <<<"$CORPS")
[[ "$REF" =~ ^AC-[0-9]{4}-[0-9]{4}$ ]] && vert "référence $REF" || rouge "référence" "$REF"
echo "      message : $(jq -r .message <<<"$CORPS")"
verifier "$(nb_mails)" 2 "2 e-mails écrits (notification interne + accusé de réception)"
verifier "$(ls "$TMP/stockage/fichiers/" | grep -cE '^[a-f0-9]{32}\.(jpg|pdf)$')" 2 "2 fichiers stockés sous un nom aléatoire"
WH=$(ls "$TMP/stockage/test-webhooks/"*.json | head -1)
verifier "$(sed -n '/^$/,$p' "$WH" | sed 1d | jq -r .scoring.priorite)" A "webhook : priorité A (score $(sed -n '/^$/,$p' "$WH" | sed 1d | jq -r .scoring.score))"
verifier "$(sed -n '/^$/,$p' "$WH" | sed 1d | jq -r .source.categorie)" google-ads "webhook : source Google Ads (utm)"

# 2. Pot de miel
M0=$(nb_mails)
R=$(curl -s -w '\n%{http_code}' -H 'Accept: application/json' -H "$ORIGINE" -F formulaire=devis -F nom=Robot \
    -F telephone=0791234567 -F travaux=placo -F commune=Genève -F accord=oui -F site_web=http://spam.example \
    -F "form_t0=$J" "$BASE/api/demande.php")
verifier "$(tail -n1 <<<"$R")/$(sed '$d' <<<"$R" | jq -r '.ok,.ref' | tr '\n' ' ')" "200/true null " "pot de miel rempli → réponse leurre (200, ref null)"
verifier "$(nb_mails)" "$M0" "pot de miel : aucun e-mail"

# 3. Envoi trop rapide (jeton tout juste délivré)
J2=$(jeton)
R=$(curl -s -w '\n%{http_code}' -H 'Accept: application/json' -H "$ORIGINE" -F formulaire=devis -F nom=Pressé \
    -F telephone=0791234567 -F travaux=placo -F commune=Genève -F accord=oui -F "form_t0=$J2" "$BASE/api/demande.php")
verifier "$(tail -n1 <<<"$R")/$(sed '$d' <<<"$R" | jq -r .code)" "422/trop_rapide" "envoi en moins de 4 s → 422 trop_rapide"

# 4. Fichiers piégés
for piege in piege.jpg polyglotte.jpg; do
    R=$(curl -s -w '\n%{http_code}' -H 'Accept: application/json' -H "$ORIGINE" -F formulaire=devis -F nom=Test \
        -F telephone=0791234567 -F travaux=placo -F commune=Genève -F accord=oui -F "form_t0=$J" \
        -F "fichiers[]=@$TMP/$piege;type=image/jpeg" "$BASE/api/demande.php")
    verifier "$(tail -n1 <<<"$R")" 422 "fichier piégé « $piege » → 422"
    echo "      $(sed '$d' <<<"$R" | jq -r .erreurs.fichiers)"
done
verifier "$(ls "$TMP/stockage/fichiers/" | grep -cE '^[a-f0-9]{32}')" 2 "aucun fichier piégé conservé"

# 5. Champs manquants
R=$(curl -s -w '\n%{http_code}' -H 'Accept: application/json' -H "$ORIGINE" -F formulaire=devis -F "form_t0=$J" "$BASE/api/demande.php")
verifier "$(tail -n1 <<<"$R")" 422 "champs manquants → 422"
verifier "$(sed '$d' <<<"$R" | jq -r '.erreurs | keys | join(",")')" "accord,commune,nom,telephone,travaux" "erreurs : accord, commune, nom, téléphone, travaux"
echo "      téléphone : $(sed '$d' <<<"$R" | jq -r .erreurs.telephone)"

# 6. Téléphone et e-mail mal formés
R=$(curl -s -H 'Accept: application/json' -H "$ORIGINE" -F formulaire=devis -F nom=Test -F 'telephone=022 77' \
    -F 'email=jean@bluewin' -F travaux=placo -F commune=Genève -F accord=oui -F "form_t0=$J" "$BASE/api/demande.php")
verifier "$(jq -r '.erreurs | keys | join(",")' <<<"$R")" "email,telephone" "téléphone et e-mail mal formés signalés"

# 7. Origine étrangère
R=$(curl -s -o /dev/null -w '%{http_code}' -H 'Accept: application/json' -H 'Origin: https://attaquant.example' \
    -F formulaire=devis "$BASE/api/demande.php")
verifier "$R" 403 "origine étrangère → 403"

# 8. Sans JavaScript : succès → redirection ; erreur → page HTML
R=$(curl -s -o /dev/null -w '%{http_code} %{redirect_url}' -F formulaire=rappel -F 'telephone=022 345 67 89' "$BASE/api/demande.php")
verifier "$R" "303 $BASE/merci.html" "sans JS, rappel valable → 303 vers /merci.html"
R=$(curl -s -w '\n%{http_code}' -H "Referer: $BASE/contact.html" -F formulaire=devis "$BASE/api/demande.php")
verifier "$(tail -n1 <<<"$R")" 422 "sans JS, erreurs → 422 en HTML"
grep -q "Indiquez votre nom et votre prénom" <<<"$R" && vert "page d'erreur lisible (messages + bouton retour + téléphone)" || rouge "page d'erreur HTML"

# 9. Méthode et en-têtes
verifier "$(curl -s -o /dev/null -w '%{http_code}' "$BASE/api/demande.php")" 405 "GET sans paramètre → 405"
curl -s -D - -o /dev/null "$BASE/api/demande.php?jeton" | grep -qi '^Cache-Control: no-store' && vert "Cache-Control: no-store" || rouge "Cache-Control"
curl -s -D - -o /dev/null "$BASE/api/demande.php?jeton" | grep -qi '^X-Content-Type-Options: nosniff' && vert "X-Content-Type-Options: nosniff" || rouge "nosniff"

# 10. Lien de fichier signé
ID=$(ls "$TMP/stockage/fichiers/" | grep -E '\.jpg$' | head -1)
EXP=$(( $(date +%s) + 3600 ))
SIG=$(php -r 'echo hash_hmac("sha256", "fichier|".$argv[1]."|".$argv[2], $argv[3]);' "$ID" "$EXP" "$SECRET_LOCAL")
verifier "$(curl -s -o /dev/null -w '%{http_code}' "$BASE/api/fichier.php?id=$ID&exp=$EXP&sig=$SIG")" 200 "fichier.php : lien signé valable → 200"
verifier "$(curl -s -o /dev/null -w '%{http_code}' "$BASE/api/fichier.php?id=$ID&exp=$EXP&sig=${SIG/a/b}")" 403 "fichier.php : signature modifiée → 403"
verifier "$(curl -s -o /dev/null -w '%{http_code}' "$BASE/api/fichier.php?id=../config.php&exp=$EXP&sig=$SIG")" 403 "fichier.php : traversée de répertoire → 403"

# 11. Journal sans données personnelles
if grep -rqE 'Dupont|079 123|francoise|127\.0\.0\.1|::1' "$TMP/stockage/journaux/"; then
    rouge "journal sans données personnelles"
else
    vert "journal sans nom, e-mail, téléphone ni IP en clair"
fi
if grep -q -i -E 'warning|fatal|notice|deprecated' "$TMP/serveur.log"; then
    rouge "aucune erreur PHP" "$(grep -i -E 'warning|fatal|notice|deprecated' "$TMP/serveur.log" | head -3)"
else
    vert "aucune erreur ni avertissement PHP"
fi

# ------------------------------------------------------------------ Apache + .htaccess
if command -v apache2 >/dev/null && [ -f /usr/lib/apache2/modules/libphp8.3.so ] || [ -f /usr/lib/apache2/modules/libphp.so ]; then
    PA=$((PORT - 2))
    MODPHP=$(ls /usr/lib/apache2/modules/libphp*.so | head -1)
    STOCK_APACHE="$API/stockage-apache-test"
    sed "s#'\$TMP/stockage'#'$STOCK_APACHE'#; s#\$c\['stockage'\] = .*#\$c['stockage'] = '$STOCK_APACHE';#" "$TMP/config.php" > "$TMP/config-apache.php"
    # Apache refuse de servir en tant que root : www-data dans ce cas.
    if [ "$(id -u)" = 0 ]; then UTIL_APACHE=www-data; GROUPE_APACHE=www-data; else UTIL_APACHE=$(id -un); GROUPE_APACHE=$(id -gn); fi
    chmod 755 "$TMP"; chmod 644 "$TMP/config-apache.php"
    mkdir -p "$STOCK_APACHE"; [ "$(id -u)" = 0 ] && chown -R "$UTIL_APACHE:$GROUPE_APACHE" "$STOCK_APACHE"
    cat > "$TMP/apache.conf" <<CONF
ServerRoot /etc/apache2
Listen 127.0.0.1:$PA
PidFile $TMP/apache.pid
ErrorLog $TMP/apache-erreurs.log
LoadModule mpm_prefork_module /usr/lib/apache2/modules/mod_mpm_prefork.so
LoadModule authz_core_module /usr/lib/apache2/modules/mod_authz_core.so
LoadModule dir_module /usr/lib/apache2/modules/mod_dir.so
LoadModule mime_module /usr/lib/apache2/modules/mod_mime.so
LoadModule rewrite_module /usr/lib/apache2/modules/mod_rewrite.so
LoadModule headers_module /usr/lib/apache2/modules/mod_headers.so
LoadModule env_module /usr/lib/apache2/modules/mod_env.so
LoadModule php_module $MODPHP
TypesConfig /etc/mime.types
User $UTIL_APACHE
Group $GROUPE_APACHE
ServerName localhost
DocumentRoot $SITE
DirectoryIndex index.html
AddType application/x-httpd-php .php
SetEnv AC_API_CONFIG $TMP/config-apache.php
<Directory />
    AllowOverride None
    Require all denied
</Directory>
<Directory $SITE>
    AllowOverride All
    Require all granted
</Directory>
CONF
    printf '\n\033[1mApache %s + .htaccess (port %s)\033[0m\n' "$(apache2 -v | head -1 | sed 's/.*Apache\///;s/ .*//')" "$PA"
    if apache2 -f "$TMP/apache.conf" -k start 2>"$TMP/apache-demarrage.log"; then
        PID_APACHE=1
        for _ in $(seq 1 50); do curl -s -o /dev/null "http://127.0.0.1:$PA/" && break; sleep 0.1; done
        BA="http://127.0.0.1:$PA/api"
        JA=$(curl -s "$BA/demande.php?jeton" | jq -r .jeton)
        case "$JA" in v1.*) vert "demande.php accessible (jeton)";; *) rouge "demande.php accessible" "$JA";; esac
        sleep 4
        R=$(curl -s -H 'Accept: application/json' -F formulaire=rappel -F 'telephone=022 345 67 89' -F "form_t0=$JA" "$BA/demande.php")
        verifier "$(jq -r .ok <<<"$R")" true "envoi réel via Apache + mod_php → ok"
        for chemin in config.php config.example.php composer.json composer.lock .htaccess .user.ini \
            lib/Config.php lib/bootstrap.php data/scoring.json data/zones.json modeles/accuse-devis.txt \
            vendor/autoload.php vendor/phpmailer/phpmailer/src/PHPMailer.php tests/run.php tests/endpoint.sh \
            index.html stockage-apache-test/journaux/ stockage-apache-test/compteurs/2026.txt; do
            C=$(curl -s -o /dev/null -w '%{http_code}' "$BA/$chemin")
            case "$C" in 403|404) vert "/api/$chemin → $C";; *) rouge "/api/$chemin refusé" "code $C";; esac
        done
        LOG=$(ls "$STOCK_APACHE/journaux/"*.log 2>/dev/null | head -1)
        C=$(curl -s -o /dev/null -w '%{http_code}' "$BA/stockage-apache-test/journaux/$(basename "$LOG")")
        case "$C" in 403|404) vert "journal du stockage inaccessible → $C";; *) rouge "journal du stockage inaccessible" "code $C";; esac
        echo '<?php echo "EXECUTE";' > "$STOCK_APACHE/fichiers/test.php"
        C=$(curl -s "$BA/stockage-apache-test/fichiers/test.php")
        [ "$C" != "EXECUTE" ] && vert "aucun PHP exécuté dans le stockage" || rouge "PHP exécuté dans le stockage"
        curl -s -D - -o /dev/null "$BA/demande.php?jeton" | grep -qi '^X-Frame-Options: DENY' && vert "en-têtes de sécurité (.htaccess, mod_headers)" || rouge "en-têtes de sécurité"
    else
        rouge "démarrage d'Apache" "$(cat "$TMP/apache-demarrage.log")"
    fi
else
    printf '\n(Apache absent : règles .htaccess non vérifiées. Installer apache2 + libapache2-mod-php pour ce test.)\n'
fi

printf '\n%s%d vérifications réussies, %d échec(s)\033[0m\n' "$([ $KO -eq 0 ] && printf '\033[32m' || printf '\033[31m')" "$OK" "$KO"
exit $((KO > 0))
