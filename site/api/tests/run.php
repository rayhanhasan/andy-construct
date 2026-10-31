<?php
/**
 * Tests de l'endpoint des formulaires (sans PHPUnit) : php site/api/tests/run.php
 *
 * Mode test : aucun envoi réel. Les e-mails sont écrits en .eml dans un dossier
 * temporaire, les webhooks partent vers un faux serveur n8n local (port libre).
 * Code de sortie 0 si tout passe, 1 sinon.
 */
declare(strict_types=1);

if (PHP_SAPI !== 'cli') {
    http_response_code(404); // jamais depuis le web (hébergeur qui ignorerait tests/.htaccess)
    exit;
}
require dirname(__DIR__) . '/lib/bootstrap.php';
ini_set('display_errors', '1');
error_reporting(E_ALL);
set_error_handler(static function (int $niveau, string $message, string $fichier, int $ligne): bool {
    if (!(error_reporting() & $niveau)) {
        return false; // erreur volontairement masquée par @
    }
    throw new \ErrorException($message, 0, $niveau, $fichier, $ligne);
});

use AndyConstruct\Api\AntiSpam;
use AndyConstruct\Api\Config;
use AndyConstruct\Api\HeuresOuvrables;
use AndyConstruct\Api\Jeton;
use AndyConstruct\Api\LiensFichiers;
use AndyConstruct\Api\LimiteDebit;
use AndyConstruct\Api\Localite;
use AndyConstruct\Api\Message;
use AndyConstruct\Api\Modeles;
use AndyConstruct\Api\Scoring;
use AndyConstruct\Api\Source;
use AndyConstruct\Api\Stockage;
use AndyConstruct\Api\Telephone;
use AndyConstruct\Api\Televersement;
use AndyConstruct\Api\Traitement;
use AndyConstruct\Api\Validateur;
use AndyConstruct\Api\Webhook;

// --------------------------------------------------------------- mini-cadre

$GLOBALS['resultats'] = ['ok' => 0, 'echecs' => []];
$GLOBALS['groupe'] = '';

function groupe(string $nom): void
{
    $GLOBALS['groupe'] = $nom;
    echo "\n\033[1m$nom\033[0m\n";
}

function ok(bool $condition, string $description, string $detail = ''): void
{
    if ($condition) {
        $GLOBALS['resultats']['ok']++;
        echo "  \033[32m✔\033[0m $description\n";
    } else {
        $GLOBALS['resultats']['echecs'][] = $GLOBALS['groupe'] . ' : ' . $description;
        echo "  \033[31m✘ $description\033[0m" . ($detail !== '' ? "\n      $detail" : '') . "\n";
    }
}

function egal(mixed $attendu, mixed $obtenu, string $description): void
{
    ok($attendu === $obtenu, $description, 'attendu ' . var_export($attendu, true) . ', obtenu ' . var_export($obtenu, true));
}

function dossierTemporaire(): string
{
    $d = sys_get_temp_dir() . '/ac-tests-' . bin2hex(random_bytes(4));
    mkdir($d, 0700, true);
    return $d;
}

function supprimer(string $chemin): void
{
    if (is_dir($chemin)) {
        foreach (new \RecursiveIteratorIterator(new \RecursiveDirectoryIterator($chemin, \FilesystemIterator::SKIP_DOTS), \RecursiveIteratorIterator::CHILD_FIRST) as $f) {
            $f->isDir() ? rmdir($f->getPathname()) : unlink($f->getPathname());
        }
        rmdir($chemin);
    }
}

/** @return list<string> contenus des .eml écrits */
function mails(string $stockage): array
{
    $fichiers = glob($stockage . '/test-mails/*.eml') ?: [];
    sort($fichiers);
    return array_map('file_get_contents', $fichiers);
}

function viderMails(string $stockage): void
{
    foreach (glob($stockage . '/test-mails/*.eml') ?: [] as $f) {
        unlink($f);
    }
    foreach (glob($stockage . '/test-webhooks/*.json') ?: [] as $f) {
        unlink($f);
    }
}

/** Décode le corps quoted-printable d'un .eml pour y chercher du texte. */
function texteMail(string $eml): string
{
    return quoted_printable_decode($eml);
}

/** Port TCP libre (évite les conflits avec d'autres serveurs locaux). */
function portLibre(): int
{
    $srv = stream_socket_server('tcp://127.0.0.1:0');
    $nom = stream_socket_get_name($srv, false);
    fclose($srv);
    return (int) substr((string) strrchr((string) $nom, ':'), 1);
}

$GLOBALS['portN8n'] = portLibre();

const SECRET_HMAC = 'secret-hmac-de-test-0123456789abcdef0123456789';
const SECRET_ACTIONS = 'secret-actions-de-test-0123456789abcdef012345';
const SECRET_LOCAL = 'secret-local-de-test-0123456789abcdef0123456789';

function configTest(string $stockage, array $surcharges = []): Config
{
    $base = [
        'mode_test' => true,
        'stockage' => $stockage,
        'url_site' => 'https://www.andyconstruct.ch',
        'url_api' => 'https://www.andyconstruct.ch/api',
        'secrets' => ['hmac_webhook' => SECRET_HMAC, 'actions' => SECRET_ACTIONS, 'local' => SECRET_LOCAL],
        'destinataires_internes' => ['associes@andyconstruct.ch'],
        'alerte_email' => 'agence@exemple.ch',
        'associes' => [
            'bureau' => ['nom' => 'Associé Bureau', 'email' => 'bureau@andyconstruct.ch', 'mobile' => ''],
            'terrain' => ['nom' => 'Associée Terrain', 'email' => 'terrain@andyconstruct.ch', 'mobile' => ''],
        ],
        'n8n' => [
            'url_demande' => 'http://127.0.0.1:' . $GLOBALS['portN8n'] . '/ok',
            'url_guide' => 'http://127.0.0.1:' . $GLOBALS['portN8n'] . '/ok',
            'url_actions' => 'https://n8n.exemple.ch/webhook/ac-action',
            'url_desinscription' => 'https://n8n.exemple.ch/webhook/ac-stop',
            'delai' => 2,
            'simuler' => true,
        ],
        'guides' => [
            'guide-reduire-le-bruit' => ['actif' => true, 'titre' => 'Réduire le bruit chez soi : ce qui marche vraiment', 'url' => 'https://www.andyconstruct.ch/assets/docs/guide-reduire-le-bruit.pdf', 'liste_brevo' => 3],
            'guide-inactif' => ['actif' => false, 'titre' => 'Inactif', 'url' => 'https://x.ch/a.pdf'],
        ],
        'realisations_par_service' => ['isolation-acoustique' => 'https://www.andyconstruct.ch/realisations/acoustique.html'],
    ];
    $config = new Config(array_replace_recursive($base, $surcharges));
    $config->verifier();
    return $config;
}

/** Démarre un serveur PHP intégré ; retourne la ressource du processus. */
function demarrerServeur(string $hote, string $script, array $env): mixed
{
    $cmd = [PHP_BINARY, '-S', $hote, $script];
    $proc = proc_open($cmd, [1 => ['file', '/dev/null', 'w'], 2 => ['file', '/dev/null', 'w']], $tubes, null, $env + getenv());
    for ($i = 0; $i < 50; $i++) {
        [$h, $p] = explode(':', $hote);
        $s = @fsockopen($h, (int) $p);
        if ($s) {
            fclose($s);
            $GLOBALS['serveurs'][] = $proc;
            return $proc;
        }
        usleep(100000);
    }
    throw new \RuntimeException("Serveur $hote injoignable");
}

register_shutdown_function(static function (): void {
    foreach ($GLOBALS['serveurs'] ?? [] as $proc) {
        arreterServeur($proc);
    }
});

function arreterServeur(mixed $proc): void
{
    if (is_resource($proc)) {
        $statut = proc_get_status($proc);
        if ($statut['running']) {
            posix_kill($statut['pid'], SIGTERM);
        }
        proc_close($proc);
    }
}

/** Fichiers de test (JPEG, PNG, PDF, HEIC, pièges). */
function fichiersDeTest(string $dossier): array
{
    $f = [];
    $img = imagecreatetruecolor(64, 48);
    imagefill($img, 0, 0, imagecolorallocate($img, 200, 30, 30));
    imagejpeg($img, $f['jpg'] = "$dossier/photo.jpg", 85);
    imagepng($img, $f['png'] = "$dossier/plan.png");
    imagedestroy($img);
    file_put_contents($f['pdf'] = "$dossier/plan.pdf", "%PDF-1.4\n1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n2 0 obj << /Type /Pages /Kids [] /Count 0 >> endobj\ntrailer << /Root 1 0 R >>\n%%EOF\n");
    file_put_contents($f['heic'] = "$dossier/iphone.heic", "\x00\x00\x00\x18ftypheic\x00\x00\x00\x00mif1heic" . str_repeat("\x00", 200));
    file_put_contents($f['php_jpg'] = "$dossier/piege.jpg", "<?php system(\$_GET['c']); ?>");
    file_put_contents($f['polyglotte'] = "$dossier/polyglotte.jpg", file_get_contents($f['jpg']) . "<?php echo 'piege'; ?>");
    file_put_contents($f['pdf_js'] = "$dossier/facture.pdf", "%PDF-1.4\n1 0 obj << /Type /Catalog /OpenAction 2 0 R >> endobj\n2 0 obj << /S /JavaScript /JS (app.alert('x')) >> endobj\n%%EOF\n");
    file_put_contents($f['pdf_js_masque'] = "$dossier/masque.pdf", "%PDF-1.4\n1 0 obj << /S /J#61vaScript /J#53 (app.alert(1)) >> endobj\n%%EOF\n");
    file_put_contents($f['svg'] = "$dossier/dessin.jpg", '<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"></svg>');
    file_put_contents($f['exe'] = "$dossier/devis.pdf", "MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff" . str_repeat("\x00", 300));
    file_put_contents($f['html'] = "$dossier/page.png", "<html><script>alert(1)</script></html>");
    $f['gros'] = "$dossier/gros.jpg";
    $h = fopen($f['gros'], 'w');
    fwrite($h, (string) file_get_contents($f['jpg']));
    fwrite($h, str_repeat("\x00", 8 * 1048576));
    fclose($h);
    return $f;
}

function entreeFichier(string $chemin, ?string $nom = null): array
{
    return ['name' => $nom ?? basename($chemin), 'tmp_name' => $chemin, 'error' => UPLOAD_ERR_OK, 'size' => (int) filesize($chemin)];
}

function postDevis(array $surcharges = []): array
{
    return array_merge([
        'formulaire' => 'devis',
        'nom' => 'Françoise Dupont',
        'civilite' => 'madame',
        'telephone' => '079 123 45 67',
        'email' => 'francoise.dupont@exemple.ch',
        'travaux' => ['isolation-acoustique'],
        'type_client' => 'proprietaire',
        'surface' => '15-50',
        'delai' => '1-3-mois',
        'commune' => 'Vésenaz',
        'message' => "On entend tout le voisin du dessus.\nPlafond de la chambre, environ 14 m².",
        'connu_par' => 'recherche-google',
        'site_web' => '',
        'page' => '/prestations.html',
        'page_entree' => '/isolation-acoustique.html',
        'referent' => 'www.google.ch',
    ], $surcharges);
}

function serveur(array $s): array
{
    return array_merge($GLOBALS['serveurJson'], $s);
}

$serveurJson = ['REQUEST_METHOD' => 'POST', 'HTTP_ACCEPT' => 'application/json', 'REMOTE_ADDR' => '203.0.113.7', 'HTTP_ORIGIN' => 'https://www.andyconstruct.ch'];

// ======================================================================= tests

$tmp = dossierTemporaire();
$racine = dirname(__DIR__);
$fx = fichiersDeTest(dossierTemporaire());

groupe('Téléphone suisse (E.164)');
foreach ([
    '022 771 20 15' => '+41227712015',
    '+41 22 771 20 15' => '+41227712015',
    '0041 22 771 20 15' => '+41227712015',
    '+41 (0)22 771 20 15' => '+41227712015',
    '078/631.14.34' => '+41786311434',
    '786311434' => '+41786311434',
    '091 123 45 67' => '+41911234567',
    '+33 4 50 12 34 56' => '+33450123456',
] as $saisie => $attendu) {
    egal($attendu, Telephone::normaliser((string) $saisie)['e164'] ?? null, "« $saisie » → $attendu");
}
egal('078 631 14 34', Telephone::normaliser('+41786311434')['affiche'] ?? null, 'affichage national 078 631 14 34');
egal('0800 123 456', Telephone::normaliser('0800 123 456')['affiche'] ?? null, 'affichage 0800 123 456');
egal(true, Telephone::normaliser('079 123 45 67')['mobile'] ?? null, '079 détecté comme mobile');
egal(false, Telephone::normaliser('022 771 20 15')['mobile'] ?? null, '022 détecté comme fixe');
foreach (['12345', '022 771 20', 'abc', '022 771 20 15 99', '+41 012 345 67 89 0', "079 123 45 67\r\nBcc: x@y.ch", '0123456789'] as $invalide) {
    egal(null, Telephone::normaliser($invalide), 'refusé : ' . json_encode($invalide));
}

groupe('E-mail');
egal('jean.dupont@bluewin.ch', Validateur::normaliserEmail(' jean.dupont@BLUEWIN.ch '), 'domaine en minuscules, espaces retirés');
foreach (['jean@', 'jean@bluewin', 'jean dupont@bluewin.ch', "jean@bluewin.ch\r\nBcc: victime@x.ch", 'a@b@c.ch', '"jean"@bluewin.ch', 'jean@bluewin.ch,autre@x.ch', 'jean@-bluewin.ch'] as $invalide) {
    egal(null, Validateur::normaliserEmail($invalide), 'refusé : ' . json_encode($invalide));
}

groupe('Validation des formulaires');
$v = new Validateur(['guide-reduire-le-bruit' => ['actif' => true]]);
[$d, $e] = $v->valider(postDevis());
egal([], $e, 'devis complet : aucune erreur');
egal('+41791234567', $d['telephone']['e164'], 'téléphone normalisé');
egal('isolation-acoustique', $d['service'], 'service principal');
[$d, $e] = $v->valider(['formulaire' => 'devis']);
egal(['nom', 'telephone', 'travaux', 'commune'], array_keys($e), 'devis vide : nom, contact, travaux, commune (aucune case de consentement)');
egal(Validateur::MESSAGES['contact'], $e['telephone'], 'message « téléphone ou e-mail »');
[$d, $e] = $v->valider(postDevis(['telephone' => '', 'email' => 'jean@']));
egal(['email'], array_keys($e), 'e-mail invalide signalé');
[$d, $e] = $v->valider(postDevis(['travaux' => ['placo', 'peinture']]));
egal('plusieurs', $d['service'], 'deux prestations → « plusieurs »');
[$d, $e] = $v->valider(postDevis(['travaux' => 'autre']));
egal('autre', $d['service'], 'autres travaux → hors des 4 services');
[$d, $e] = $v->valider(postDevis(['type_client' => 'pirate', 'surface' => '<script>']));
ok($e === [] && $d['type_client'] === '' && $d['surface'] === '', 'valeurs de liste inconnues ignorées sans bloquer');
[$d, $e] = $v->valider(postDevis(['message' => str_repeat('a', 3001)]));
ok(isset($e['message']), 'message de plus de 3000 caractères refusé');
[$d, $e] = $v->valider(postDevis(['nom' => "Jean\r\nBcc: victime@exemple.ch", 'message' => "Ligne 1\r\nLigne 2\x00\x07"]));
ok(!str_contains($d['nom'], "\n") && !str_contains($d['nom'], "\r"), 'retours à la ligne retirés du nom');
egal("Ligne 1\nLigne 2", $d['message'], 'caractères de contrôle retirés du message');
[$d, $e] = $v->valider(['formulaire' => 'rappel', 'telephone' => '022 771 20 15']);
egal([], $e, 'rappel : le téléphone suffit');
[$d, $e] = $v->valider(['formulaire' => 'rappel', 'email' => 'a@b.ch']);
egal(['telephone'], array_keys($e), 'rappel sans téléphone refusé');
$guidePoste = ['formulaire' => 'envoi_postal_guide', 'guide' => 'guide-reduire-le-bruit', 'nom' => 'Bernard Favre', 'adresse' => 'Chemin des Pommiers 12', 'npa' => '1222', 'localite' => 'Vésenaz'];
[$d, $e] = $v->valider($guidePoste);
egal([], $e, 'guide par la poste : nom, adresse, NPA, localité suffisent (e-mail facultatif)');
egal("Chemin des Pommiers 12\n1222 Vésenaz", $d['adresse_postale'], 'adresse d\'envoi composée');
egal(false, $d['conseils_email'], 'conseils par e-mail : non par défaut');
[$d, $e] = $v->valider(['formulaire' => 'envoi_postal_guide', 'guide' => 'guide-reduire-le-bruit']);
egal(['nom', 'adresse', 'npa', 'localite'], array_keys($e), 'guide par la poste vide : nom, adresse, NPA, localité');
[$d, $e] = $v->valider(['guide' => 'guide-inconnu'] + $guidePoste);
egal(['guide'], array_keys($e), 'guide inconnu ou inactif refusé');
[$d, $e] = $v->valider(['formulaire' => 'aimant', 'aimant' => 'guide-reduire-le-bruit', 'par_poste' => 'oui', 'nom' => 'B. Favre', 'adresse_postale' => "Chemin des Pommiers 12\n1222 Vésenaz"]);
ok($e === [] && $d['formulaire'] === 'envoi_postal_guide', 'ancien format (formulaire=aimant, adresse_postale sur 3 lignes) accepté');
[$d, $e] = $v->valider(postDevis(['telephone' => '', 'preference_contact' => 'appel']));
egal(Validateur::MESSAGES['telephone_requis'], $e['telephone'] ?? null, 'préférence « appel » sans numéro → numéro demandé');
[$d, $e] = $v->valider(postDevis(['accord' => 'peu importe']));
ok($e === [] && !array_key_exists('accord', $d), 'champ « accord » envoyé : ignoré (décision D2)');
[$d, $e] = $v->valider(postDevis(['npa' => '12A7']));
ok(isset($e['npa']), 'NPA mal formé refusé');
[$d, $e] = $v->valider(postDevis(['rappel' => 'oui']));
egal('appel', $d['preference_contact'], 'ancienne case « rappel » → préférence « appel »');
[$d, $e] = $v->valider(postDevis(['gclid' => 'Cj0KCQjw-abcdef123456', 'consent_ads' => '']));
egal('', $d['gclid'], 'gclid ignoré sans consentement');
[$d, $e] = $v->valider(postDevis(['gclid' => 'Cj0KCQjw-abcdef123456', 'consent_ads' => 'accorde']));
egal('Cj0KCQjw-abcdef123456', $d['gclid'], 'gclid conservé avec consentement');

groupe('Localité → zone');
$loc = Localite::depuisFichier("$racine/data/zones.json");
foreach ([
    ['1227', '', 1, 'NPA 1227 (Carouge) → zone 1'],
    ['1260', '', 1, 'NPA 1260 (Nyon) → zone 1'],
    ['1196', '', 1, 'NPA 1196 (Gland) → zone 1'],
    ['1003', '', 2, 'NPA 1003 (Lausanne) → zone 2'],
    ['1110', '', 2, 'NPA 1110 (Morges) → zone 2'],
    ['1820', '', 2, 'NPA 1820 (Montreux) → zone 2'],
    ['2000', '', 3, 'NPA 2000 (Neuchâtel) → zone 3'],
    ['1950', '', 3, 'NPA 1950 (Sion) → zone 3'],
    ['3960', '', 3, 'NPA 3960 (Sierre) → zone 3'],
    ['8001', '', 'hors', 'NPA 8001 (Zurich) → hors cible'],
    ['', '1225 Chêne-Bourg', 1, 'NPA extrait de « 1225 Chêne-Bourg »'],
    ['', 'Chêne-Bourg (GE)', 1, 'commune exacte « Chêne-Bourg (GE) »'],
    ['', 'Vesenaz', 1, 'commune sans accent « Vesenaz »'],
    ['', 'St-Légier', 2, '« St-Légier » → Saint-Légier'],
    ['', 'Lausane', 2, 'faute de frappe « Lausane » → Lausanne (approchée)'],
    ['', 'Annemasse', 'hors', 'Annemasse (France) → hors cible'],
    ['', 'Trifouillis', 'inconnue', 'commune inconnue → zone inconnue'],
] as [$npa, $commune, $zone, $description]) {
    egal($zone, $loc->resoudre($npa, $commune)['zone'], $description);
}
egal('commune-approchee', $loc->resoudre('', 'Lausane')['methode'], 'méthode « commune approchée » signalée');

groupe('Source');
egal('recherche-google', Source::normaliser(['referent' => 'www.google.ch'])['categorie'], 'référent Google → recherche naturelle');
egal('google-ads', Source::normaliser(['utm_source' => 'google', 'utm_medium' => 'cpc'])['categorie'], 'utm cpc → Google Ads');
egal('carte-google', Source::normaliser(['utm_source' => 'google', 'utm_medium' => 'organic-local'])['categorie'], 'fiche Google → carte');
egal('meta', Source::normaliser(['utm_source' => 'meta', 'utm_medium' => 'paid-social'])['categorie'], 'Meta');
egal('recommandation', Source::normaliser(['utm_source' => 'recommandation', 'utm_medium' => 'print'])['categorie'], 'carte de recommandation');
egal('appel-direct', Source::normaliser(['canal' => 'telephone'])['categorie'], 'saisie téléphonique → appel direct');
egal('direct-inconnu', Source::normaliser(['referent' => 'www.andyconstruct.ch'])['categorie'], 'référent interne ignoré');

groupe('Scoring (exemples du §2.6 de la stratégie)');
$sc = Scoring::depuisFichier("$racine/data/scoring.json");
$cas = [
    ['Propriétaire à Vésenaz, acoustique, 15-50 m², 1-3 mois, Google, téléphone', ['type_client' => 'proprietaire', 'service' => 'isolation-acoustique', 'surface' => '15-50', 'zone' => 1, 'delai' => '1-3-mois', 'source_categorie' => 'recherche-google', 'telephone' => true, 'message' => 'x'], 71, 'A'],
    ['Régie genevoise, peinture, > 200 m², < 1 mois, appel direct', ['type_client' => 'regie', 'service' => 'peinture', 'surface' => 'plus-200', 'zone' => 1, 'delai' => 'moins-1-mois', 'source_categorie' => 'appel-direct', 'canal' => 'telephone', 'telephone' => true, 'message' => 'x'], 93, 'A'],
    ['Architecte à Neuchâtel, cloisons, > 200 m², 3-6 mois, LinkedIn (règle 3)', ['type_client' => 'architecte', 'service' => 'placo', 'surface' => 'plus-200', 'zone' => 3, 'delai' => '3-6-mois', 'source_categorie' => 'linkedin', 'message' => 'x'], 79, 'A'],
    ['Propriétaire à Fribourg, peinture 2 pièces, 1-3 mois, Google', ['type_client' => 'proprietaire', 'service' => 'peinture', 'surface' => '15-50', 'zone' => 3, 'delai' => '1-3-mois', 'source_categorie' => 'recherche-google', 'message' => 'x'], 53, 'B'],
    ['Locataire à Lausanne, peinture 1 pièce, non défini, Meta, sans téléphone', ['type_client' => 'locataire', 'service' => 'peinture', 'surface' => '15-50', 'zone' => 2, 'delai' => 'non-defini', 'source_categorie' => 'meta', 'message' => 'x'], 39, 'C'],
];
foreach ($cas as [$nom, $donnees, $score, $priorite]) {
    $r = $sc->calculer($donnees);
    ok($r['score'] === $score && $r['priorite'] === $priorite, "$nom → $score, $priorite", "obtenu {$r['score']}, {$r['priorite']}");
}
$r = $sc->calculer(['type_client' => 'commune', 'service' => 'peinture', 'surface' => 'moins-15', 'zone' => 3, 'delai' => 'non-defini', 'source_categorie' => 'meta', 'message' => 'x']);
egal('B', $r['priorite'], 'règle 1 : commune jamais en dessous de B');
$r = $sc->calculer(['type_client' => 'locataire', 'service' => 'peinture', 'surface' => 'moins-15', 'zone' => 2, 'delai' => 'moins-1-mois', 'source_categorie' => 'meta', 'message' => 'Dégât d\'eau au plafond, état des lieux vendredi']);
egal('A', $r['priorite'], 'règle 2 : dégât + moins d\'un mois → A');
$r = $sc->calculer(['type_client' => 'proprietaire', 'service' => 'autre', 'zone' => 1]);
egal('hors-cible', $r['priorite'], 'service hors des 4 prestations → hors cible');
$r = $sc->calculer(['type_client' => 'regie', 'service' => 'placo', 'zone' => 'hors']);
egal('hors-cible', $r['priorite'], 'hors Suisse romande → hors cible');
$r = $sc->calculer(['type_client' => '', 'service' => '', 'zone' => 'inconnue', 'formulaire' => 'rappel', 'telephone' => true, 'source_categorie' => 'direct-inconnu']);
egal('B', $r['priorite'], 'demande de rappel → au moins B');
$r = $sc->calculer(['type_client' => 'proprietaire', 'service' => 'placo', 'zone' => 1, 'source_categorie' => 'direct-inconnu', 'connu_par' => 'recommandation', 'message' => 'x']);
ok(in_array(['critere' => 'source', 'valeur' => 'recommandation (déclaré)', 'points' => 10], $r['detail'], true), 'source déclarée « recommandation » retenue si plus forte (10 points)');
$r = $sc->calculer(['type_client' => 'proprietaire', 'service' => 'placo', 'zone' => 1, 'message' => '', 'telephone' => false, 'nb_fichiers' => 2]);
ok(in_array(['critere' => 'bonus', 'valeur' => 'photo ou plan joint', 'points' => 5], $r['detail'], true)
    && in_array(['critere' => 'malus', 'valeur' => 'message vide et aucun téléphone', 'points' => -5], $r['detail'], true), 'bonus fichier +5 et malus message vide −5');

groupe('Heures ouvrables et délais de rappel');
egal('2026-04-05', HeuresOuvrables::paques(2026)->format('Y-m-d'), 'Pâques 2026 : 5 avril');
egal('2027-03-28', HeuresOuvrables::paques(2027)->format('Y-m-d'), 'Pâques 2027 : 28 mars');
$feries = HeuresOuvrables::feriesGeneve(2026);
ok(in_array('2026-09-10', $feries, true), 'Jeûne genevois 2026 : jeudi 10 septembre');
ok(in_array('2026-12-31', $feries, true) && in_array('2026-05-14', $feries, true) && in_array('2026-05-25', $feries, true), 'Restauration, Ascension, lundi de Pentecôte');
$ho = new HeuresOuvrables(7, 18);
$tz = new \DateTimeZone('Europe/Zurich');
$t = static fn (string $s) => new \DateTimeImmutable($s, $tz);
egal('2026-11-02 12:00', $ho->echeance('A', $t('2026-11-02 10:00'))->format('Y-m-d H:i'), 'A reçue lundi 10 h → lundi 12 h');
egal('2026-11-03 08:00', $ho->echeance('A', $t('2026-11-02 17:00'))->format('Y-m-d H:i'), 'A reçue lundi 17 h → mardi 8 h');
egal('2026-11-02 09:00', $ho->echeance('A', $t('2026-10-31 15:00'))->format('Y-m-d H:i'), 'A reçue samedi → lundi 9 h');
egal('2026-11-02 18:00', $ho->echeance('B', $t('2026-11-02 11:30'))->format('Y-m-d H:i'), 'B reçue avant 14 h → le jour même');
egal('2026-11-03 10:00', $ho->echeance('B', $t('2026-11-02 15:00'))->format('Y-m-d H:i'), 'B reçue après 14 h → lendemain 10 h');
egal('2026-09-11 10:00', $ho->echeance('B', $t('2026-09-09 16:00'))->format('Y-m-d H:i'), 'B la veille du Jeûne genevois → vendredi 10 h');
egal('2026-11-04 10:00', $ho->echeance('C', $t('2026-11-02 10:00'))->format('Y-m-d H:i'), 'C → deux jours ouvrables');
egal("aujourd'hui avant 12 h 15", $ho->formulerEcheance($t('2026-11-02 12:07'), $t('2026-11-02 10:07')), 'promesse arrondie au quart d\'heure');
egal('demain avant 10 h', $ho->formulerEcheance($t('2026-11-03 10:00'), $t('2026-11-02 15:00')), 'promesse « demain avant 10 h »');
egal('lundi avant 9 h', $ho->formulerEcheance($t('2026-11-02 09:00'), $t('2026-10-30 19:00')), 'promesse « lundi avant 9 h »');

groupe('Anti-spam');
$cfg = configTest($tmp);
$as = new AntiSpam($cfg);
$maintenant = time();
$jeton = $as->creerJeton($maintenant - 30);
egal('ok', $as->verifierJeton($jeton, 'devis', $maintenant)['statut'], 'jeton valable après 30 s');
egal(30, $as->verifierJeton($jeton, 'devis', $maintenant)['delai'], 'délai de remplissage mesuré');
egal('trop_rapide', $as->verifierJeton($as->creerJeton($maintenant - 1), 'devis', $maintenant)['statut'], 'envoi en 1 s → trop rapide');
egal('ok', $as->verifierJeton($as->creerJeton($maintenant - 2), 'rappel', $maintenant)['statut'], 'rappel : 2 s suffisent');
egal('expire', $as->verifierJeton($as->creerJeton($maintenant - 13 * 3600), 'devis', $maintenant)['statut'], 'jeton de plus de 12 h → expiré (accepté, signalé)');
egal('absent', $as->verifierJeton('', 'devis', $maintenant)['statut'], 'jeton absent (envoi sans JS)');
$falsifie = preg_replace('/\.(\d{10})\./', '.' . ($maintenant - 3600) . '.', $jeton);
egal('invalide', $as->verifierJeton((string) $falsifie, 'devis', $maintenant)['statut'], 'horodatage modifié → signature invalide');
egal('invalide', $as->verifierJeton('v1.123.abc.def', 'devis', $maintenant)['statut'], 'jeton mal formé → invalide');
ok($as->potDeMielRempli(['site_web' => 'http://spam.example']), 'pot de miel rempli détecté');
ok(!$as->potDeMielRempli(['site_web' => '']), 'pot de miel vide accepté');
ok($as->potDeMielRempli(['site_web' => ['x']]), 'pot de miel envoyé en tableau détecté');
egal('trop_de_liens', $as->contenuSuspect(['message' => 'http://a.ch http://b.ch http://c.ch http://d.ch']), 'plus de 3 liens → spam');
egal(null, $as->contenuSuspect(['message' => 'Plans sur https://wetransfer.com/xyz']), 'un lien de transfert accepté');
egal('balises_forum', $as->contenuSuspect(['message' => '[url=http://casino.example]x[/url]']), 'balises de forum → spam');
egal('lien_dans_nom', $as->contenuSuspect(['nom' => 'www.seo-pas-cher.example']), 'lien dans le nom → spam');
ok($as->origineAutorisee(['HTTP_ORIGIN' => 'https://www.andyconstruct.ch']), 'origine du site acceptée');
ok($as->origineAutorisee([]), 'origine absente acceptée (anciens navigateurs)');
ok(!$as->origineAutorisee(['HTTP_ORIGIN' => 'https://attaquant.example']), 'origine étrangère refusée');
ok(!$as->origineAutorisee(['HTTP_ORIGIN' => 'null']), 'origine « null » refusée');

groupe('Limitation de débit (IP hachée)');
$st = new Stockage($tmp . '/limites-test');
$ld = new LimiteDebit($st, SECRET_LOCAL);
$res = [];
for ($i = 0; $i < 6; $i++) {
    $res[] = $ld->tenter('198.51.100.23', 'demandes', 5, 1_800_000_000 + $i)['autorise'];
}
egal([true, true, true, true, true, false], $res, '5 demandes acceptées, la 6e refusée');
ok($ld->tenter('198.51.100.24', 'demandes', 5, 1_800_000_010)['autorise'], 'autre IP non concernée');
ok($ld->tenter('198.51.100.23', 'demandes', 5, 1_800_003_700)['autorise'], 'de nouveau autorisée une heure plus tard');
$contenu = implode('', array_map('file_get_contents', glob($tmp . '/limites-test/limites/*.json') ?: [])) . implode('', glob($tmp . '/limites-test/limites/*') ?: []);
ok(!str_contains($contenu, '198.51.100'), 'aucune adresse IP en clair (noms et contenus de fichiers)');

groupe('Signature HMAC du webhook');
egal('f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8', hash_hmac('sha256', 'The quick brown fox jumps over the lazy dog', 'key'), 'vecteur de test HMAC-SHA256 (RFC 4231 / Wikipédia)');
$corps = Webhook::encoder(['ref' => 'AC-2026-0001', 'nom' => 'Chêne-Bourg / « test »', 'n' => 3]);
egal('{"ref":"AC-2026-0001","nom":"Chêne-Bourg / « test »","n":3}', $corps, 'JSON sans échappement des barres ni de l\'Unicode (identique à JSON.stringify)');
$sig = Webhook::signer(SECRET_HMAC, $corps, 1_800_000_000);
egal('sha256=' . hash_hmac('sha256', '1800000000.' . $corps, SECRET_HMAC), $sig, 'signature = HMAC(secret, horodatage + "." + corps)');
ok($sig !== Webhook::signer(SECRET_HMAC, $corps . ' ', 1_800_000_000), 'corps modifié → signature différente');
ok($sig !== Webhook::signer(SECRET_HMAC, $corps, 1_800_000_001), 'horodatage modifié → signature différente');

groupe('Jetons des liens en un clic');
$jt = new Jeton(SECRET_ACTIONS);
$j = $jt->creer(['a' => 'contact-etabli', 'r' => 'AC-2026-0042'], 3600, 1_800_000_000);
egal('contact-etabli', $jt->verifier($j, 1_800_000_100)['a'] ?? null, 'jeton valable lu');
egal(null, $jt->verifier($j, 1_800_003_601), 'jeton expiré refusé');
[$charge, $s] = explode('.', $j);
$autre = Jeton::b64(json_encode(['a' => 'hors-cible', 'r' => 'AC-2026-0042', 'x' => 1_900_000_000]));
egal(null, $jt->verifier("$autre.$s", 1_800_000_100), 'charge modifiée refusée');
egal(null, (new Jeton('autre-secret-0123456789abcdef0123456789'))->verifier($j, 1_800_000_100), 'autre secret refusé');

groupe('Liens de fichiers signés');
$lf = new LiensFichiers('https://www.andyconstruct.ch/api', SECRET_LOCAL);
$id = str_repeat('a', 32) . '.pdf';
parse_str((string) parse_url($lf->url($id, 24, 1_800_000_000), PHP_URL_QUERY), $q);
ok($lf->verifier($q['id'], $q['exp'], $q['sig'], 1_800_000_000), 'lien valable accepté');
ok(!$lf->verifier($q['id'], $q['exp'], $q['sig'], 1_800_100_000), 'lien expiré refusé');
ok(!$lf->verifier('../../config.php', $q['exp'], $q['sig'], 1_800_000_000), 'traversée de répertoire refusée');
ok(!$lf->verifier(str_repeat('b', 32) . '.pdf', $q['exp'], $q['sig'], 1_800_000_000), 'autre fichier avec la même signature refusé');

groupe('Fichiers joints (finfo, pièges)');
$tv = new Televersement(new Stockage($tmp . '/fichiers-test'), 3, 8 * 1048576, true, false);
[$enr, $err] = $tv->traiter([entreeFichier($fx['jpg']), entreeFichier($fx['png']), entreeFichier($fx['pdf'])]);
egal(null, $err, 'JPEG + PNG + PDF acceptés');
ok(count($enr) === 3 && (bool) preg_match('/^[a-f0-9]{32}\.jpg$/', $enr[0]['id']), 'renommés aléatoirement (32 caractères hexadécimaux + extension réelle)');
ok(!str_contains(implode('', array_column($enr, 'chemin')), 'photo'), 'nom d\'origine absent du chemin stocké');
egal('0640', substr(sprintf('%o', fileperms($enr[0]['chemin'])), -4), 'droits 0640');
[$enr, $err] = $tv->traiter([entreeFichier($fx['heic'])]);
egal(null, $err, 'HEIC (iPhone) accepté');
egal('image/heic', $enr[0]['type'] ?? null, 'HEIC reconnu');
foreach ([
    'php_jpg' => 'script PHP renommé en .jpg',
    'polyglotte' => 'JPEG valable avec code PHP ajouté (polyglotte)',
    'pdf_js' => 'PDF contenant du JavaScript',
    'pdf_js_masque' => 'PDF avec JavaScript masqué (/J#61vaScript)',
    'svg' => 'SVG déguisé en .jpg',
    'exe' => 'exécutable Windows renommé en .pdf',
    'html' => 'HTML renommé en .png',
    'gros' => 'fichier de plus de 8 Mo',
] as $cle => $description) {
    [$enr, $err] = $tv->traiter([entreeFichier($fx[$cle])]);
    ok($enr === [] && $err !== null, "refusé : $description", (string) $err);
}
[$enr, $err] = $tv->traiter(array_fill(0, 4, entreeFichier($fx['jpg'])));
ok($enr === [] && str_contains((string) $err, '3 fichiers'), 'quatre fichiers refusés (3 au maximum)');
[$enr, $err] = $tv->traiter([entreeFichier($fx['jpg']), entreeFichier($fx['php_jpg'])]);
ok($enr === [] && count(glob($tmp . '/fichiers-test/fichiers/*.jpg') ?: []) === 1, 'un fichier piégé dans le lot → aucun fichier du lot enregistré');
[$enr, $err] = (new Televersement(new Stockage($tmp . '/fichiers-test2'), 3, 8 * 1048576, true, true))->traiter([entreeFichier($fx['jpg'])]);
ok($enr === [] && $err !== null, 'fichier non issu d\'un envoi HTTP refusé (is_uploaded_file)');
egal('plan_final_.pdf', Televersement::nomAffichable('../../plan<final>.pdf'), 'nom affiché nettoyé');
$sto = new Stockage($tmp . '/fichiers-test');
touch($enr2 = $tmp . '/fichiers-test/fichiers/' . str_repeat('c', 32) . '.jpg', time() - 31 * 86400);
egal(1, $sto->purger('fichiers', 30), 'purge : fichier de plus de 30 jours supprimé');
ok(is_file($tmp . '/fichiers-test/fichiers/.htaccess') && str_contains((string) file_get_contents($tmp . '/fichiers-test/fichiers/.htaccess'), 'Require all denied'), 'dossier protégé par .htaccess (deny)');
ok(is_file($tmp . '/fichiers-test/fichiers/index.html'), 'dossier protégé par index.html');

groupe('Modèles de messages');
egal('A B', Modeles::rendre('{{#x}}A{{/x}}{{^y}} B{{/y}}{{#z}} C{{/z}}', ['x' => true, 'y' => '', 'z' => 0]), 'sections conditionnelles');
egal('[in]', Modeles::rendre('{{#a}}[{{#b}}in{{/b}}]{{/a}}', ['a' => 1, 'b' => 1]), 'sections imbriquées');
egal('Bonjour Madame Françoise Dupont', Modeles::salutation('madame', 'Françoise Dupont', ''), 'salutation avec civilité');
egal('Bonjour Bernard', Modeles::salutation('', '', 'Bernard'), 'salutation par le prénom');
egal('Bcc: x', Message::entete("\r\nBcc: x\r\n"), 'en-tête : retours à la ligne neutralisés');
foreach (glob("$racine/modeles/*.txt") ?: [] as $m) {
    ok((bool) preg_match('/^Objet : .+\n\n/u', (string) file_get_contents($m)), 'modèle ' . basename($m) . ' : ligne « Objet : »');
}

// ------------------------------------------------------ traitement de bout en bout
groupe('Traitement complet (in-process, mode test)');
$stock = dossierTemporaire();
$cfg = configTest($stock);
$tr = new Traitement($cfg, false);
$maintenantTr = new \DateTimeImmutable('2026-11-02 10:07', $tz); // lundi
$as = new AntiSpam($cfg);
$post = postDevis(['form_t0' => $as->creerJeton($maintenantTr->getTimestamp() - 40)]);
$fichiersPost = ['fichiers' => ['name' => ['photo.jpg', 'plan.pdf'], 'tmp_name' => [$fx['jpg'], $fx['pdf']], 'error' => [0, 0], 'size' => [filesize($fx['jpg']), filesize($fx['pdf'])], 'type' => ['image/jpeg', 'application/pdf']]];
$r = $tr->executer($serveurJson, [], $post, $fichiersPost, $maintenantTr);
egal(200, $r->statut, 'devis valable → 200');
egal(true, $r->corps['ok'] ?? null, 'réponse ok:true');
ok((bool) preg_match('/^AC-2026-\d{4}$/', (string) ($r->corps['ref'] ?? '')), 'référence AC-2026-0001', (string) ($r->corps['ref'] ?? ''));
ok(str_contains((string) ($r->corps['message'] ?? ''), "aujourd'hui avant 12 h 15"), 'message de succès avec le délai promis', (string) ($r->corps['message'] ?? ''));
$eml = mails($stock);
egal(2, count($eml), 'deux e-mails écrits (interne + accusé de réception)');
$interne = texteMail((string) current(array_filter($eml, static fn ($m) => str_contains($m, 'associes@andyconstruct.ch'))));
$accuse = texteMail((string) current(array_filter($eml, static fn ($m) => str_contains($m, 'To: =?utf-8?Q?Fran') || str_contains($m, 'francoise.dupont@exemple.ch>'))));
ok(str_contains($interne, '[A] Nouvelle demande') || str_contains($interne, 'Priorité A'), 'interne : priorité A');
ok(str_contains($interne, 'href="tel:+41791234567"'), 'interne : lien tel: cliquable');
ok(str_contains($interne, 'score 76') || str_contains($interne, 'Score détaillé (76'), 'interne : score détaillé (71 + 5 photo)');
ok(str_contains($interne, 'Content-Disposition: attachment; filename=photo.jpg') || str_contains($interne, 'filename="photo.jpg"') || str_contains($interne, 'photo.jpg'), 'interne : pièces jointes');
ok(str_contains($interne, 'Reply-To: =?utf-8?Q?') || str_contains($interne, 'Reply-To: Fran') || str_contains($interne, 'francoise.dupont@exemple.ch'), 'interne : « Répondre » écrit au prospect');
ok(str_contains($interne, 'https://n8n.exemple.ch/webhook/ac-action?t='), 'interne : liens en un clic signés');
ok(str_contains($accuse, 'Votre demande est bien arriv'), 'accusé : texte de confirmation');
ok(str_contains($accuse, "aujourd'hui avant 12 h 15"), 'accusé : délai de rappel');
ok(str_contains($accuse, 'Associée Terrain vous appelle'), 'accusé : associé nommé (particulier → terrain)');
ok(str_contains($accuse, 'https://www.andyconstruct.ch/realisations/acoustique.html'), 'accusé : réalisation comparable');
ok(!str_contains($accuse, '{{') && !str_contains($interne, '{{'), 'aucune variable non remplacée');
ok(str_contains($accuse, 'Auto-Submitted: auto-generated'), 'accusé : en-tête Auto-Submitted');
ok(!preg_match('/<img|pixel|track/i', $accuse), 'accusé : aucune image ni pixel de suivi');
$wh = glob($stock . '/test-webhooks/*.json') ?: [];
egal(1, count($wh), 'webhook simulé écrit');
[$entetes, $corpsWh] = explode("\n\n", (string) file_get_contents($wh[0]), 2);
preg_match('/X-AC-Timestamp: (\d+)/', $entetes, $mt);
preg_match('/X-AC-Signature: (sha256=[a-f0-9]{64})/', $entetes, $ms);
egal('sha256=' . hash_hmac('sha256', $mt[1] . '.' . $corpsWh, SECRET_HMAC), $ms[1] ?? '', 'webhook : signature vérifiable');
$charge = json_decode($corpsWh, true);
egal('A', $charge['scoring']['priorite'] ?? null, 'webhook : priorité A');
egal('+41791234567', $charge['contact']['telephone'] ?? null, 'webhook : téléphone E.164');
egal(2, count($charge['fichiers'] ?? []), 'webhook : deux fichiers avec lien signé');
ok(str_contains((string) ($charge['fichiers'][0]['url'] ?? ''), '/fichier.php?id='), 'webhook : URL de fichier signée');
ok(!str_contains($corpsWh, 'chemin'), 'webhook : aucun chemin serveur divulgué');
$journal = implode('', array_map('file_get_contents', glob($stock . '/journaux/*.log') ?: []));
ok(str_contains($journal, 'demande_recue') && !str_contains($journal, 'Dupont') && !str_contains($journal, '079') && !str_contains($journal, '203.0.113.7') && !str_contains($journal, '@exemple'), 'journal : aucune donnée personnelle en clair');
viderMails($stock);

$r = $tr->executer(serveur(['REMOTE_ADDR' => '203.0.113.8']), [], postDevis(['email' => '', 'nom' => "Jean\r\nBcc: victime@exemple.ch", 'form_t0' => $as->creerJeton($maintenantTr->getTimestamp() - 40)]), [], $maintenantTr);
$eml = mails($stock);
egal(1, count($eml), 'sans e-mail : seulement la notification interne, pas d\'accusé');
ok(!preg_match('/^Bcc:/mi', (string) ($eml[0] ?? '')), 'injection d\'en-tête par le nom sans effet (aucun Bcc)');
viderMails($stock);

$r = $tr->executer($serveurJson, [], postDevis(['site_web' => 'http://spam.example', 'form_t0' => $as->creerJeton($maintenantTr->getTimestamp() - 40)]), [], $maintenantTr);
ok($r->statut === 200 && ($r->corps['ok'] ?? false) === true && array_key_exists('ref', $r->corps) && $r->corps['ref'] === null, 'pot de miel : réponse « ok » leurre');
egal(0, count(mails($stock)), 'pot de miel : aucun e-mail envoyé');

$r = $tr->executer($serveurJson, [], postDevis(['form_t0' => $as->creerJeton($maintenantTr->getTimestamp() - 1)]), [], $maintenantTr);
ok($r->statut === 422 && ($r->corps['code'] ?? '') === 'trop_rapide', 'envoi en 1 s → 422 trop_rapide');

$r = $tr->executer($serveurJson, [], postDevis(['form_t0' => 'v1.1800000000.aaaaaaaaaaaa.' . str_repeat('0', 32)]), [], $maintenantTr);
ok($r->statut === 200 && array_key_exists('ref', $r->corps) && $r->corps['ref'] === null && count(mails($stock)) === 0, 'jeton falsifié → leurre, rien envoyé');

$r = $tr->executer($serveurJson, [], ['formulaire' => 'devis', 'nom' => 'X', 'form_t0' => $as->creerJeton($maintenantTr->getTimestamp() - 40)], [], $maintenantTr);
ok($r->statut === 422 && ($r->corps['code'] ?? '') === 'validation' && isset($r->corps['erreurs']['telephone'], $r->corps['erreurs']['travaux'], $r->corps['erreurs']['commune']), 'champs manquants → 422 avec la liste des erreurs');

$r = $tr->executer($serveurJson, [], postDevis(['form_t0' => $as->creerJeton($maintenantTr->getTimestamp() - 40)]), ['fichiers' => ['name' => ['piege.jpg'], 'tmp_name' => [$fx['php_jpg']], 'error' => [0], 'size' => [filesize($fx['php_jpg'])]]], $maintenantTr);
ok($r->statut === 422 && isset($r->corps['erreurs']['fichiers']), 'fichier piégé → 422, erreur sur « fichiers »');

$r = $tr->executer(serveur(['HTTP_ORIGIN' => 'https://attaquant.example']), [], postDevis(), [], $maintenantTr);
egal(403, $r->statut, 'origine étrangère → 403');

$r = $tr->executer(['REQUEST_METHOD' => 'GET'], ['jeton' => ''], [], [], $maintenantTr);
ok($r->statut === 200 && str_starts_with((string) ($r->corps['jeton'] ?? ''), 'v1.'), 'GET ?jeton → jeton horodaté');
egal(405, $tr->executer(['REQUEST_METHOD' => 'GET'], [], [], [], $maintenantTr)->statut, 'GET sans paramètre → 405');
egal(413, $tr->executer(['REQUEST_METHOD' => 'POST', 'CONTENT_LENGTH' => '99999999'], [], [], [], $maintenantTr)->statut, 'requête trop volumineuse (post_max_size) → 413');

$sansJs = ['REQUEST_METHOD' => 'POST', 'REMOTE_ADDR' => '203.0.113.9', 'HTTP_REFERER' => 'https://www.andyconstruct.ch/contact.html'];
$r = $tr->executer($sansJs, [], postDevis(), [], $maintenantTr);
ok($r->statut === 303 && $r->redirection === '/merci.html', 'sans JS, succès → redirection 303 vers /merci.html');
$r = $tr->executer($sansJs, [], ['formulaire' => 'devis'], [], $maintenantTr);
ok($r->statut === 422 && $r->forme === 'html' && str_contains($r->html, 'Indiquez votre nom') && str_contains($r->html, 'https://www.andyconstruct.ch/contact.html'), 'sans JS, erreur → page HTML avec les messages et le lien de retour');
viderMails($stock);

$ipLimite = serveur(['REMOTE_ADDR' => '192.0.2.50']);
$statuts = [];
for ($i = 0; $i < 6; $i++) {
    $statuts[] = $tr->executer($ipLimite, [], postDevis(['form_t0' => $as->creerJeton($maintenantTr->getTimestamp() - 40)]), [], $maintenantTr)->statut;
}
egal([200, 200, 200, 200, 200, 429], $statuts, 'limite : 5 demandes par heure et par IP, la 6e → 429');
viderMails($stock);

$r = $tr->executer(serveur(['REMOTE_ADDR' => '192.0.2.60']), [], ['formulaire' => 'rappel', 'telephone' => '022 345 67 89', 'creneau' => 'matin', 'form_t0' => $as->creerJeton($maintenantTr->getTimestamp() - 5)], [], $maintenantTr);
ok($r->statut === 200 && str_contains((string) $r->corps['message'], 'nous vous rappelons'), 'demande de rappel acceptée', json_encode($r->corps, JSON_UNESCAPED_UNICODE));
viderMails($stock);

$r = $tr->executer(serveur(['REMOTE_ADDR' => '192.0.2.61']), [], $guidePoste + ['email' => 'bernard@exemple.ch', 'civilite' => 'monsieur', 'profil' => 'proprietaire', 'conseils_email' => 'oui', 'form_t0' => $as->creerJeton($maintenantTr->getTimestamp() - 5)], [], $maintenantTr);
$eml = array_map('texteMail', mails($stock));
$guide = (string) current(array_filter($eml, static fn ($m) => str_contains($m, 'bernard@exemple.ch') && str_contains($m, 'nous vous envoyons le guide')));
$interneGuide = (string) current(array_filter($eml, static fn ($m) => str_contains($m, 'associes@andyconstruct.ch')));
ok($r->statut === 200 && str_contains((string) $r->corps['message'], 'part par la poste'), 'guide par la poste : réponse de succès', json_encode($r->corps, JSON_UNESCAPED_UNICODE));
ok($guide !== '' && str_contains($guide, 'Chemin des Pommiers 12') && str_contains($guide, 'guide-reduire-le-bruit.pdf'), 'guide : accusé avec adresse d\'envoi et lien de lecture en ligne');
ok(str_contains($guide, 'deux e-mails de conseils') && str_contains($guide, 'https://n8n.exemple.ch/webhook/ac-stop?t='), 'guide avec accord : séquence annoncée + désinscription');
ok(str_contains($interneGuide, 'Guide imprim') && str_contains($interneGuide, 'Chemin des Pommiers 12'), 'guide : consigne d\'envoi postal aux associés');
$wh = glob($stock . '/test-webhooks/*.json') ?: [];
$chargeGuide = json_decode(explode("\n\n", (string) file_get_contents((string) end($wh)), 2)[1], true);
ok(($chargeGuide['evenement'] ?? '') === 'guide.envoi_postal' && ($chargeGuide['guide']['conseils_email'] ?? null) === true, 'webhook : guide.envoi_postal, conseils_email = true');
viderMails($stock);
$r = $tr->executer(serveur(['REMOTE_ADDR' => '192.0.2.62']), [], $guidePoste + ['email' => 'claire@exemple.ch', 'form_t0' => $as->creerJeton($maintenantTr->getTimestamp() - 5)], [], $maintenantTr);
$guide = (string) current(array_filter(array_map('texteMail', mails($stock)), static fn ($m) => str_contains($m, 'claire@exemple.ch') && str_contains($m, 'nous vous envoyons le guide')));
ok($guide !== '' && !str_contains($guide, 'conseils sur ce sujet') && !str_contains($guide, 'ac-stop'), 'guide sans accord : aucun conseil annoncé, aucune séquence');
viderMails($stock);

// ------------------------------------------- sécurité (constats de docs/v2/qa/securite.md)
groupe('Sécurité : limite de débit, IPv6 et en-têtes de proxy (S-04, S-05)');
egal('2001:db8:1:2::/64', LimiteDebit::cle('2001:db8:1:2:aaaa:bbbb:cccc:dddd'), 'IPv6 ramenée à son préfixe /64');
egal('198.51.100.7', LimiteDebit::cle('::ffff:198.51.100.7'), 'IPv4 encapsulée (::ffff:…) ramenée à l\'IPv4');
$ld6 = new LimiteDebit(new Stockage($tmp . '/limites-ipv6'), SECRET_LOCAL);
$res = [];
for ($i = 1; $i <= 6; $i++) {
    $res[] = $ld6->tenter('2001:db8:1:2::' . dechex($i * 4099), 'demandes', 5, 1_800_000_000 + $i)['autorise'];
}
egal([true, true, true, true, true, false], $res, 'IPv6 : changer d\'adresse dans le même /64 ne contourne pas la limite');
ok($ld6->tenter('2001:db8:1:3::1', 'demandes', 5, 1_800_000_010)['autorise'], 'IPv6 : un autre /64 n\'est pas concerné');
$forge = ['REMOTE_ADDR' => '203.0.113.50', 'HTTP_X_FORWARDED_FOR' => '6.6.6.6, 198.51.100.9', 'HTTP_CF_CONNECTING_IP' => '7.7.7.7'];
egal('203.0.113.50', LimiteDebit::ipClient($forge, false), 'sans confiance au proxy : REMOTE_ADDR, en-têtes ignorés');
egal('203.0.113.50', LimiteDebit::ipClient($forge, true, ['173.245.48.0/20']), 'connexion directe (hors proxys de confiance) : en-têtes forgés ignorés');
egal('7.7.7.7', LimiteDebit::ipClient(['REMOTE_ADDR' => '173.245.48.10'] + $forge, true, ['173.245.48.0/20']), 'via un proxy de confiance (Cloudflare) : CF-Connecting-IP');
egal('198.51.100.9', LimiteDebit::ipClient(['REMOTE_ADDR' => '10.0.0.2', 'HTTP_X_FORWARDED_FOR' => '6.6.6.6, 198.51.100.9, 10.0.0.1'], true, ['10.0.0.0/8']), 'X-Forwarded-For lu de droite à gauche : l\'entrée forgée (à gauche) est ignorée');
egal('198.51.100.9', LimiteDebit::ipClient(['REMOTE_ADDR' => '10.0.0.2', 'HTTP_X_FORWARDED_FOR' => '6.6.6.6, 198.51.100.9'], true), 'sans liste de proxys : entrée la plus à droite (ajoutée par le proxy)');
ok(LimiteDebit::dansPlages('2400:cb00::1', ['2400:cb00::/32']) && !LimiteDebit::dansPlages('2400:cb01::1', ['2400:cb00::/32'])
    && LimiteDebit::dansPlages('10.1.2.3', ['10.0.0.0/8']) && !LimiteDebit::dansPlages('11.0.0.1', ['10.0.0.0/8']) && LimiteDebit::dansPlages('192.0.2.1', ['192.0.2.1']), 'plages CIDR IPv4 et IPv6');

groupe('Sécurité : formulaire utilisé comme relais d\'e-mails (S-01)');
$stockRelais = dossierTemporaire();
$trR = new Traitement(configTest($stockRelais, ['anti_spam' => ['accuses_par_heure' => 4]]), false);
$nbMails = static fn (string $categorie): int => count(glob($stockRelais . "/test-mails/*-$categorie-*.eml") ?: []);
for ($i = 1; $i <= 4; $i++) {
    $r = $trR->executer(serveur(['REMOTE_ADDR' => "198.51.100.$i"]), [], postDevis(['email' => 'victime@exemple.org', 'form_t0' => $as->creerJeton($maintenantTr->getTimestamp() - 40)]), [], $maintenantTr);
}
ok($r->statut === 200 && $nbMails('interne') === 4, 'même adresse depuis 4 IP : les 4 demandes sont traitées (e-mail interne)');
egal(3, $nbMails('accuse'), 'accusés de réception plafonnés à 3 par adresse sur 24 h');
$statutsAccuse = array_map(static fn ($f) => json_decode(explode("\n\n", (string) file_get_contents($f), 2)[1], true)['accuse_reception'] ?? null, glob($stockRelais . '/test-webhooks/*.json') ?: []);
sort($statutsAccuse);
egal(['envoye', 'envoye', 'envoye', 'limite'], $statutsAccuse, 'webhook : accuse_reception = « limite » pour la 4e demande');
foreach (['autre1@exemple.org', 'autre2@exemple.org'] as $i => $adresse) {
    $trR->executer(serveur(['REMOTE_ADDR' => '198.51.100.' . (10 + $i)]), [], postDevis(['email' => $adresse, 'form_t0' => $as->creerJeton($maintenantTr->getTimestamp() - 40)]), [], $maintenantTr);
}
egal(4, $nbMails('accuse'), 'plafond global des accusés par heure (ici 4) : le suivant ne part pas');
viderMails($stockRelais);
$r = $trR->executer(serveur(['REMOTE_ADDR' => '198.51.100.20']), [], array_merge($guidePoste, ['adresse' => 'https://evil.example/phish?gagne=1', 'email' => 'cible@exemple.org', 'form_t0' => $as->creerJeton($maintenantTr->getTimestamp() - 5)]), [], $maintenantTr);
ok($r->statut === 200 && $r->corps['ref'] === null && mails($stockRelais) === [], 'lien dans l\'adresse d\'envoi du guide → leurre, aucun e-mail');
$trR2 = new Traitement(configTest(dossierTemporaire()), false);
$r = $trR2->executer(serveur(['REMOTE_ADDR' => '198.51.100.21']), [], postDevis(['nom' => 'GAGNANT iPhone reclamez-le sur bit.ly/xyz ou gain-facile.com', 'email' => 'cible@exemple.org', 'message' => 'Offre : promo-casino.net/bonus', 'form_t0' => $as->creerJeton($maintenantTr->getTimestamp() - 40)]), [], $maintenantTr);
$stockR2 = (new \ReflectionProperty($trR2, 'stockage'))->getValue($trR2)->racine();
$accuseR = texteMail((string) current(glob($stockR2 . '/test-mails/*-accuse-*.eml') ?: ['']) ? (string) file_get_contents((string) current(glob($stockR2 . '/test-mails/*-accuse-*.eml'))) : '');
preg_match_all('~href="([^"]+)"~', $accuseR, $liensAccuse);
ok($accuseR !== '' && !str_contains($accuseR, 'bit.ly') && !str_contains($accuseR, 'gain-facile.com') && !str_contains($accuseR, 'promo-casino') && str_contains($accuseR, '[lien]'), 'accusé : domaines saisis par le visiteur masqués (nom, message), y compris l\'en-tête To');
ok($liensAccuse[1] !== [] && array_filter($liensAccuse[1], static fn ($u) => !str_starts_with($u, 'https://www.andyconstruct.ch/')) === [], 'accusé : seuls des liens vers le site de l\'entreprise sont cliquables');
egal('Rte.de Lausanne 12, St.Gallen', Modeles::neutraliserLiens('Rte.de Lausanne 12, St.Gallen'), 'abréviations courantes (« Rte.de », « St.Gallen ») non touchées');
supprimer($stockRelais);
supprimer($stockR2);

groupe('Sécurité : balisage dans les champs d\'identité (S-07)');
$stockHtml = dossierTemporaire();
$trH = new Traitement(configTest($stockHtml), false);
$trH->executer(serveur(['REMOTE_ADDR' => '198.51.100.30']), [], postDevis(['nom' => '<img src=//evil.example/p.gif>Dupont', 'commune' => '<b>Carouge</b>', 'form_t0' => $as->creerJeton($maintenantTr->getTimestamp() - 40)]), [], $maintenantTr);
$chargeH = json_decode(explode("\n\n", (string) file_get_contents((string) current(glob($stockHtml . '/test-webhooks/*.json') ?: [''])), 2)[1] ?? 'null', true);
ok(is_array($chargeH) && !str_contains($chargeH['contact']['nom'] . $chargeH['projet']['commune'], '<') && str_contains($chargeH['contact']['nom'], 'Dupont'), 'webhook : chevrons retirés du nom et de la commune (aucune balise transmise à n8n / Pipedrive)');
supprimer($stockHtml);

groupe('Sécurité : PDF actifs cachés (S-03)');
$objstm = static function (string $corps, bool $double = false, string $prefixe = ''): string {
    $z = gzcompress($prefixe . '3 0 ' . $corps);
    $z = $double ? gzcompress($z) : $z;
    return "%PDF-1.5\n1 0 obj\n<< /Type /Catalog /OpenAction 3 0 R >>\nendobj\n4 0 obj\n<< /Type /ObjStm /N 1 /First 4 /Filter /FlateDecode /Length " . strlen($z) . " >>\nstream\n$z\nendstream\nendobj\n%%EOF\n";
};
$dossierPdf = dossierTemporaire();
$pdfs = [
    'objstm' => [$objstm('<< /S /JavaScript /JS (app.alert(1)) >>'), 'JavaScript dans un flux d\'objets compressé (/ObjStm)'],
    'double' => [$objstm('<< /S /JavaScript /JS (app.alert(1)) >>', true), 'JavaScript sous deux couches FlateDecode'],
    'commentaire_long' => [$objstm('<< /S /Launch /F (cmd.exe) >>', false, '%' . str_repeat('x', 5000) . "\n"), 'action Launch derrière un long commentaire'],
    'commentaire' => ["%PDF-1.4\n1 0 obj << /Type /Catalog /OpenAction 2 0 R >> endobj\n2 0 obj << /S/JavaScript>> /JS%x\n(app.alert(1)) >> endobj\n%%EOF\n", '« /S/JavaScript>> » et « /JS%commentaire »'],
    'xfa' => ["%PDF-1.7\n1 0 obj << /AcroForm << /XFA 5 0 R >> >> endobj\n%%EOF\n", 'formulaire XFA'],
    'ascii85' => ["%PDF-1.4\n1 0 obj << /Filter /ASCII85Decode /Length 3 >> stream\nabc\nendstream endobj\n%%EOF\n", 'filtre ASCII85 (non inspectable)'],
];
foreach ($pdfs as $cle => [$contenu, $description]) {
    file_put_contents("$dossierPdf/$cle.pdf", $contenu);
    [$enr, $err, $raison] = $tv->traiter([entreeFichier("$dossierPdf/$cle.pdf")]);
    ok($enr === [] && $raison === 'contenu_actif', "PDF refusé : $description", (string) $raison);
}
$c = deflate_init(ZLIB_ENCODING_DEFLATE);
$page = deflate_add($c, str_repeat("0.5 w 10 20 m 30 40 l S\n", 20000), ZLIB_FINISH);
file_put_contents("$dossierPdf/plan.pdf", $objstm('<< /Type /Page /MediaBox [0 0 595 842] /Contents 5 0 R >>') . "5 0 obj\n<< /Filter /FlateDecode /Length " . strlen($page) . " >>\nstream\n$page\nendstream\nendobj\n");
[$enr, $err] = $tv->traiter([entreeFichier("$dossierPdf/plan.pdf")]);
egal(null, $err, 'PDF de plan ordinaire (flux d\'objets et dessin compressés) accepté');
supprimer($dossierPdf);

groupe('Sécurité : robustesse et en-têtes (S-09, S-19, S-20)');
$r = $tr->executer(serveur(['REMOTE_ADDR' => '198.51.100.40']), [], ['formulaire' => ['x'], 'nom' => 'X'], [], $maintenantTr);
egal(422, $r->statut, 'formulaire envoyé en tableau → 422, sans avertissement PHP');
egal([['name' => 'a', 'tmp_name' => '', 'error' => UPLOAD_ERR_OK, 'size' => 0]], Televersement::aplatir(['fichier' => ['name' => 'a', 'tmp_name' => ['x'], 'error' => '0', 'size' => ['z']]]), 'structure $_FILES forgée : aucun avertissement, chemin vide');
$exp = 1_800_000_000;
ok(!$lf->verifier(str_repeat('a', 32) . ".pdf\n", (string) $exp, hash_hmac('sha256', 'fichier|' . str_repeat('a', 32) . ".pdf\n|$exp", SECRET_LOCAL), 1_700_000_000), 'fichier.php : identifiant terminé par un saut de ligne refusé (ancre $ avec /D)');
$r = $tr->executer(['REQUEST_METHOD' => 'POST', 'REMOTE_ADDR' => '198.51.100.41', 'HTTP_REFERER' => "javascript://www.andyconstruct.ch/%0Aalert(1)"], [], ['formulaire' => 'devis'], [], $maintenantTr);
ok($r->forme === 'html' && !str_contains($r->html, 'javascript:') && str_contains($r->html, '/contact.html#formulaire'), 'page d\'erreur : référent « javascript: » ignoré (lien de retour par défaut)');
viderMails($stock);

// ------------------------------------------------------ webhook réel (faux n8n)
groupe('Webhook vers un faux n8n (HTTP réel, file d\'attente)');
$journalN8n = $stock . '/faux-n8n.log';
$serveur = demarrerServeur('127.0.0.1:' . $GLOBALS['portN8n'], __DIR__ . '/faux-n8n.php', ['FAUX_N8N_SECRET' => SECRET_HMAC, 'FAUX_N8N_JOURNAL' => $journalN8n]);
try {
    $cfgReel = configTest($stock, ['n8n' => ['simuler' => false]]);
    $wb = new Webhook($cfgReel, new Stockage($stock), new \AndyConstruct\Api\Journal(new Stockage($stock)), new LiensFichiers('https://x.ch/api', SECRET_LOCAL));
    egal('livre', $wb->transmettre('demande', ['ref' => 'AC-2026-9001', 'test' => 'é/«»'], 'AC-2026-9001'), 'signature acceptée par le faux n8n → livré');
    ok(str_contains((string) @file_get_contents($journalN8n), 'AC-2026-9001'), 'charge reçue par le faux n8n');

    $cfgMauvais = configTest($stock, ['n8n' => ['simuler' => false], 'secrets' => ['hmac_webhook' => 'mauvais-secret-0123456789abcdef0123456789']]);
    $wbMauvais = new Webhook($cfgMauvais, new Stockage($stock), new \AndyConstruct\Api\Journal(new Stockage($stock)), new LiensFichiers('https://x.ch/api', SECRET_LOCAL));
    egal('en_file', $wbMauvais->transmettre('demande', ['ref' => 'AC-2026-9002'], 'AC-2026-9002'), 'mauvais secret → refus 401 → mis en file d\'attente');
    egal(1, $wb->tailleFile(), 'un élément en file d\'attente');
    $bilan = $wb->traiterFile(10, true);
    ok($bilan['livres'] === 1 && $wb->tailleFile() === 0, 'nouvel essai (bon secret) → livré, file vide');

    $cfgPanne = configTest($stock, ['n8n' => ['simuler' => false, 'url_demande' => 'http://127.0.0.1:' . portLibre() . '/ferme']]);
    $wbPanne = new Webhook($cfgPanne, new Stockage($stock), new \AndyConstruct\Api\Journal(new Stockage($stock)), new LiensFichiers('https://x.ch/api', SECRET_LOCAL));
    egal('en_file', $wbPanne->transmettre('demande', ['ref' => 'AC-2026-9003'], 'AC-2026-9003'), 'n8n arrêté (connexion refusée) → file d\'attente');
    $cfgLent = configTest($stock, ['n8n' => ['simuler' => false, 'url_demande' => 'http://127.0.0.1:' . $GLOBALS['portN8n'] . '/lent', 'delai' => 1]]);
    $wbLent = new Webhook($cfgLent, new Stockage($stock), new \AndyConstruct\Api\Journal(new Stockage($stock)), new LiensFichiers('https://x.ch/api', SECRET_LOCAL));
    $t0 = microtime(true);
    egal('en_file', $wbLent->transmettre('demande', ['ref' => 'AC-2026-9004'], 'AC-2026-9004'), 'n8n trop lent (délai dépassé) → file d\'attente');
    ok(microtime(true) - $t0 < 2.5, 'le visiteur n\'attend pas plus que le délai configuré');
    // Vieillissement artificiel pour tester l'alerte (> 60 min).
    foreach (glob($stock . '/file-attente/*.json') ?: [] as $f) {
        $el = json_decode((string) file_get_contents($f), true);
        $el['cree'] = time() - 2 * 3600;
        file_put_contents($f, json_encode($el));
    }
    $bilan = $wbPanne->traiterFile(10, true);
    ok(count($bilan['a_signaler']) === 2 && $bilan['restants'] === 2, 'demandes en attente depuis plus d\'une heure signalées', json_encode($bilan));
    $bilan = $wbPanne->traiterFile(10, true);
    egal([], $bilan['a_signaler'], 'alerte envoyée une seule fois par demande');
    $bilan = $wb->traiterFile(10, true);
    ok($bilan['livres'] === 2 && $wb->tailleFile() === 0, 'n8n revenu → file vidée');
} finally {
    arreterServeur($serveur);
}

// ------------------------------------------------- cohérence avec automation/messages
groupe('Cohérence des modèles PHP avec automation/messages/');
$dossierMessages = dirname($racine, 2) . '/automation/messages';
if (!is_dir($dossierMessages)) {
    echo "  (dossier automation/messages absent : test ignoré sur le serveur)\n";
} else {
    foreach (['accuse-devis' => 'accuse-reception-devis.md', 'accuse-rappel' => 'accuse-reception-rappel.md', 'accuse-guide' => 'accuse-reception-guide.md'] as $modele => $md) {
        $texteMd = (string) @file_get_contents("$dossierMessages/$md");
        $ok = preg_match('/```texte\n(.*?)```/s', $texteMd, $m) === 1;
        $php = str_replace("\r\n", "\n", (string) file_get_contents("$racine/modeles/$modele.txt"));
        ok($ok && trim($m[1]) === trim($php), "$md identique à modeles/$modele.txt");
    }
}

// ----------------------------------------------------------------- nettoyage
supprimer($tmp);
supprimer($stock);
supprimer(dirname($fx['jpg']));

$n = $GLOBALS['resultats']['ok'];
$echecs = $GLOBALS['resultats']['echecs'];
echo "\n" . ($echecs === [] ? "\033[32m" : "\033[31m") . "$n vérifications réussies, " . count($echecs) . " échec(s)\033[0m\n";
foreach ($echecs as $e) {
    echo "  - $e\n";
}
exit($echecs === [] ? 0 : 1);
