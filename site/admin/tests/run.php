<?php
/**
 * Tests de l'admin (sans PHPUnit) : php site/admin/tests/run.php
 *
 * TOTP (vecteurs RFC 6238), base et migrations, enregistrement des demandes par
 * Traitement (et rejeu si la base est indisponible), transitions de statut,
 * indicateurs du §5, authentification, CSRF, contrôle d'accès page par page
 * (serveur PHP local sur un port libre), rôle agence sans données personnelles,
 * export et effacement nLPD. Aucun envoi réel (mode test). Sortie 0 si tout passe.
 */
declare(strict_types=1);

if (PHP_SAPI !== 'cli') {
    http_response_code(404);
    exit;
}
require dirname(__DIR__) . '/lib/bootstrap.php';
ini_set('display_errors', '1');
error_reporting(E_ALL);
set_error_handler(static function (int $niveau, string $message, string $fichier, int $ligne): bool {
    if (!(error_reporting() & $niveau)) {
        return false;
    }
    throw new \ErrorException($message, 0, $niveau, $fichier, $ligne);
});

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Auth;
use AndyConstruct\Admin\Demandes;
use AndyConstruct\Admin\Format;
use AndyConstruct\Admin\Indicateurs;
use AndyConstruct\Admin\Personnes;
use AndyConstruct\Admin\Totp;
use AndyConstruct\Api\AntiSpam;
use AndyConstruct\Api\Base;
use AndyConstruct\Api\Canaux;
use AndyConstruct\Api\Config;
use AndyConstruct\Api\Traitement;

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
function proche(float $attendu, ?float $obtenu, string $description, float $tol = 1e-6): void
{
    ok($obtenu !== null && abs($attendu - $obtenu) <= $tol, $description, "attendu $attendu, obtenu " . var_export($obtenu, true));
}
function refuse(callable $fn, string $description, string $contient = ''): void
{
    try {
        $fn();
        ok(false, $description, 'aucune exception');
    } catch (\DomainException $e) {
        ok($contient === '' || str_contains($e->getMessage(), $contient), $description, $e->getMessage());
    }
}
function dossierTemporaire(): string
{
    $d = sys_get_temp_dir() . '/ac-admin-tests-' . bin2hex(random_bytes(4));
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
function portLibre(): int
{
    $srv = stream_socket_server('tcp://127.0.0.1:0');
    $nom = stream_socket_get_name($srv, false);
    fclose($srv);
    return (int) substr((string) strrchr((string) $nom, ':'), 1);
}

const SECRETS = [
    'hmac_webhook' => 'secret-hmac-de-test-0123456789abcdef0123456789',
    'actions' => 'secret-actions-de-test-0123456789abcdef012345',
    'local' => 'secret-local-de-test-0123456789abcdef0123456789',
    'admin' => 'secret-admin-de-test-0123456789abcdef01234567',
];
function valeursConfig(string $stockage, array $plus = []): array
{
    return array_replace_recursive([
        'mode_test' => true,
        'stockage' => $stockage,
        'secrets' => SECRETS,
        'destinataires_internes' => ['associes@exemple.test'],
        'associes' => ['bureau' => ['nom' => 'Bureau Test', 'email' => 'bureau@exemple.test', 'mobile' => ''], 'terrain' => ['nom' => 'Terrain Test', 'email' => 'terrain@exemple.test', 'mobile' => '']],
        'n8n' => ['simuler' => true],
        'admin' => ['cookie_securise' => false],
    ], $plus);
}
function configTest(string $stockage, array $plus = []): Config
{
    $c = new Config(valeursConfig($stockage, $plus));
    $c->verifier();
    return $c;
}
$tz = new \DateTimeZone('Europe/Zurich');
$t = static fn (string $s): \DateTimeImmutable => new \DateTimeImmutable($s, $tz);
$aNettoyer = [];

// =========================================================================== TOTP
groupe('TOTP : vecteurs de la RFC 6238 (annexe B) et Base32');
$cle1 = '12345678901234567890';
$cle256 = '12345678901234567890123456789012';
$cle512 = '1234567890123456789012345678901234567890123456789012345678901234';
$vecteurs = [
    [59, '94287082', '46119246', '90693936'],
    [1111111109, '07081804', '68084774', '25091201'],
    [1111111111, '14050471', '67062674', '99943326'],
    [1234567890, '89005924', '91819424', '93441116'],
    [2000000000, '69279037', '90698825', '38618901'],
    [20000000000, '65353130', '77737706', '47863826'],
];
foreach ($vecteurs as [$temps, $sha1, $sha256, $sha512]) {
    egal($sha1, Totp::code($cle1, $temps, 8, 30, 'sha1'), "SHA-1, T = $temps");
    egal($sha256, Totp::code($cle256, $temps, 8, 30, 'sha256'), "SHA-256, T = $temps");
    egal($sha512, Totp::code($cle512, $temps, 8, 30, 'sha512'), "SHA-512, T = $temps");
}
egal('755224', Totp::hotp($cle1, 0), 'HOTP RFC 4226, compteur 0 (6 chiffres)');
egal('287082', Totp::code($cle1, 59), 'code à 6 chiffres = 6 derniers chiffres du vecteur');
egal('GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ', Totp::base32Encoder($cle1), 'Base32 (RFC 4648) de la clé de test');
egal($cle1, Totp::base32Decoder('gezd gnbv gy3t qojq gezd gnbv gy3t qojq'), 'Base32 décodé (minuscules et espaces tolérés)');
$secret = Totp::nouveauSecret();
$maintenant = 1_800_000_000;
$code = Totp::code(Totp::base32Decoder($secret), $maintenant);
ok(Totp::verifier($secret, $code, $maintenant) !== null, 'code du moment accepté');
ok(Totp::verifier($secret, $code, $maintenant + 30) !== null, 'pas précédent accepté (dérive d\'horloge)');
ok(Totp::verifier($secret, $code, $maintenant + 90) === null, 'code trop ancien refusé');
$pas = Totp::verifier($secret, $code, $maintenant);
ok(Totp::verifier($secret, $code, $maintenant, (int) $pas) === null, 'même code refusé une deuxième fois (rejeu)');
ok(Totp::verifier($secret, '12345', $maintenant) === null && Totp::verifier($secret, 'abcdef', $maintenant) === null, 'saisie mal formée refusée');
$chiffre = Totp::chiffrer($secret, SECRETS['admin']);
ok(!str_contains($chiffre, $secret) && Totp::dechiffrer($chiffre, SECRETS['admin']) === $secret, 'secret chiffré en base, déchiffré avec la clé');
egal(null, Totp::dechiffrer($chiffre, 'autre-cle-0123456789abcdef0123456789'), 'mauvaise clé : déchiffrement refusé');

// ====================================================================== base
groupe('Base : migrations idempotentes (SQLite)');
$stockBase = dossierTemporaire();
$aNettoyer[] = $stockBase;
$cfgBase = configTest($stockBase);
$b1 = Base::depuisConfig($cfgBase);
$b1->migrer();
$b2 = Base::depuisConfig($cfgBase); // nouvelle connexion, même fichier
egal(Base::VERSION_SCHEMA, (int) $b2->valeur('SELECT MAX(version) FROM migration'), 'version du schéma enregistrée une fois');
egal(1, (int) $b2->valeur('SELECT COUNT(*) FROM migration'), 'aucune migration appliquée deux fois');
$tables = array_column($b2->tous("SELECT name FROM sqlite_master WHERE type = 'table'"), 'name');
ok(!array_diff(['utilisateur', 'contact', 'demande', 'attribution', 'interaction', 'visite', 'offre', 'fichier', 'depense', 'parametre', 'journal_audit'], $tables), 'toutes les tables du MVP existent');
ok(is_file($stockBase . '/base/.htaccess'), 'dossier de la base protégé (.htaccess deny)');

// ============================================================ enregistrement
groupe('Enregistrement des demandes par Traitement (devis, rappel, guide)');
$stock = dossierTemporaire();
$aNettoyer[] = $stock;
$cfg = configTest($stock, ['guides' => ['guide-reduire-le-bruit' => ['actif' => true, 'titre' => 'Guide', 'url' => 'https://x.test/g.pdf', 'liste_brevo' => 0]]]);
$quand = $t('2026-11-02 10:07'); // lundi
$app = new App($cfg, null, $quand);
$alex = $app->auth->creerUtilisateur('alex@exemple.test', 'Alex Test', 'associe', 'terrain', 'une phrase de passe assez longue')['id'];
$camille = $app->auth->creerUtilisateur('camille@exemple.test', 'Camille Test', 'associe', 'bureau', 'une autre phrase de passe longue')['id'];
$serveur = ['REQUEST_METHOD' => 'POST', 'HTTP_ACCEPT' => 'application/json', 'REMOTE_ADDR' => '203.0.113.7', 'HTTP_ORIGIN' => 'https://www.andyconstruct.ch'];
$as = new AntiSpam($cfg);
$img = imagecreatetruecolor(32, 24);
$fichierJpg = $stock . '/photo-test.jpg';
imagejpeg($img, $fichierJpg);
$devis = [
    'formulaire' => 'devis', 'nom' => 'Personne Fictive', 'telephone' => '079 000 00 11', 'email' => 'personne.fictive@exemple.test',
    'travaux' => ['isolation-acoustique'], 'type_client' => 'proprietaire', 'surface' => '15-50', 'delai' => '1-3-mois', 'commune' => 'Vésenaz',
    'message' => 'Bruit du voisin.', 'connu_par' => 'recherche-google', 'site_web' => '', 'page' => '/contact.html', 'page_entree' => '/isolation-acoustique.html',
    'referent' => 'www.google.ch', 'utm_source' => 'google', 'utm_medium' => 'cpc', 'utm_campaign' => 'acoustique', 'gclid' => 'Cj0KCQtest1234567', 'consent_ads' => 'accorde',
    'form_t0' => $as->creerJeton($quand->getTimestamp() - 40),
];
$tr = new Traitement($cfg, false);
$r = $tr->executer($serveur, [], $devis, ['fichiers' => ['name' => ['photo.jpg'], 'tmp_name' => [$fichierJpg], 'error' => [0], 'size' => [filesize($fichierJpg)]]], $quand);
egal(200, $r->statut, 'devis accepté');
$ref = (string) ($r->corps['ref'] ?? '');
$d = $app->demandes->parRef($ref);
ok($d !== null, "demande $ref enregistrée en base");
$wh = glob($stock . '/test-webhooks/*.json') ?: [];
$charge = json_decode(explode("\n\n", (string) file_get_contents((string) end($wh)), 2)[1], true);
egal($charge['scoring']['score'], $d['score'], 'même score que le webhook (et l\'e-mail interne)');
egal($charge['scoring']['priorite'], $d['priorite'], 'même priorité');
egal((new \DateTimeImmutable($charge['scoring']['echeance']))->getTimestamp(), $d['echeance']->getTimestamp(), 'même échéance de rappel');
egal('nouvelle', $d['statut'], 'statut « nouvelle »');
egal($alex, (int) $d['associe_id'], 'attribuée à l\'associé « terrain » (particulier)');
egal('google_ads', $d['canal_marketing'], 'canal Google Ads (catégorie google-ads)');
egal('Cj0KCQtest1234567', $d['gclid'], 'gclid gardé (consentement accordé)');
egal('acoustique', $d['utm_campaign'], 'UTM enregistrés');
egal('www.google.ch', $d['referent'], 'référent enregistré');
egal('+41790000011', $d['telephone_e164'], 'téléphone normalisé E.164');
egal(1, (int) $app->base->valeur('SELECT COUNT(*) FROM fichier WHERE demande_id = ?', [$d['id']]), 'fichier joint enregistré (identifiant, empreinte)');
ok(count(json_decode((string) $d['score_detail'], true)) >= 6, 'score détaillé enregistré (critères)');
egal('envoye', $d['accuse_reception'], 'accusé de réception noté');

$r = $tr->executer(['REMOTE_ADDR' => '203.0.113.8'] + $serveur, [], ['formulaire' => 'rappel', 'telephone' => '022 000 00 12', 'creneau' => 'matin', 'form_t0' => $as->creerJeton($quand->getTimestamp() - 5)], [], $quand);
$rappel = $app->demandes->parRef((string) $r->corps['ref']);
ok($rappel !== null && $rappel['formulaire'] === 'rappel' && in_array($rappel['priorite'], ['A', 'B'], true), 'demande de rappel enregistrée (jamais en dessous de B)');
$r = $tr->executer(['REMOTE_ADDR' => '203.0.113.9'] + $serveur, [], ['formulaire' => 'envoi_postal_guide', 'guide' => 'guide-reduire-le-bruit', 'nom' => 'Personne Guide', 'adresse' => 'Rue Fictive 1', 'npa' => '1227', 'localite' => 'Carouge', 'form_t0' => $as->creerJeton($quand->getTimestamp() - 5)], [], $quand);
$guide = $app->demandes->parRef((string) $r->corps['ref']);
ok($guide !== null && $guide['statut'] === 'guide' && $guide['score'] === null, 'envoi postal de guide enregistré (statut « guide », sans score)');
egal(0, count(array_filter($app->demandes->liste(['statut' => 'toutes']), static fn ($x) => $x['statut'] === 'guide')), 'guides absents des listes de demandes par défaut');

groupe('Base indisponible : le flux continue, la demande est rejouée sans doublon');
$stockPanne = dossierTemporaire();
$aNettoyer[] = $stockPanne;
$cfgPanne = configTest($stockPanne, ['base' => ['dsn' => 'sqlite:/proc/interdit/ac.sqlite']]);
$trPanne = new Traitement($cfgPanne, false);
$r = $trPanne->executer(['REMOTE_ADDR' => '203.0.113.20'] + $serveur, [], array_merge($devis, ['form_t0' => $as->creerJeton($quand->getTimestamp() - 40)]), [], $quand);
egal(200, $r->statut, 'demande acceptée malgré la base en panne');
ok(count(glob($stockPanne . '/test-mails/*.eml') ?: []) >= 1, 'e-mail interne parti');
ok(count(glob($stockPanne . '/test-webhooks/*.json') ?: []) === 1, 'webhook parti');
egal(1, $trPanne->depot()->tailleFile(), 'demande mise en file (stockage/file-attente-base)');
$cfgRetour = configTest($stockPanne);
$trRetour = new Traitement($cfgRetour, false);
$bilan = $trRetour->depot()->traiterFile();
egal(1, $bilan['inserees'], 'cron.php : demande insérée au retour de la base');
egal(0, $trRetour->depot()->tailleFile(), 'file vidée');
$basePanne = Base::depuisConfig($cfgRetour);
egal(1, (int) $basePanne->valeur('SELECT COUNT(*) FROM demande WHERE ref = ?', [$r->corps['ref']]), 'une seule ligne pour cette référence');
egal('deja', $trRetour->depot()->enregistrer(['ref' => (string) $r->corps['ref']] + preparerFactice()), 'rejeu de la même référence : « déjà en base », pas de doublon');

/** Enregistrement minimal (format Depot::preparer) pour le test de rejeu. */
function preparerFactice(): array
{
    return ['v' => 1, 'recue_le' => '2026-11-02 09:07:00', 'formulaire' => 'devis', 'canal' => 'site', 'cree_par' => null, 'mode_test' => true, 'role_associe' => 'terrain',
        'contact' => ['civilite' => '', 'prenom' => '', 'nom' => 'X', 'email' => '', 'telephone_e164' => '', 'telephone_affiche' => '', 'telephone_mobile' => false, 'adresse' => '', 'npa' => '', 'localite' => '', 'preference_contact' => '', 'creneau' => ''],
        'projet' => ['type_client' => '', 'travaux' => [], 'service' => '', 'surface' => '', 'delai' => '', 'commune' => '', 'npa' => '', 'canton' => '', 'zone' => 'inconnue', 'message' => '', 'connu_par' => '', 'recommande_par' => '', 'guide' => ''],
        'scoring' => null, 'echeance_le' => null, 'source' => ['categorie' => 'direct-inconnu', 'libelle' => '', 'emplacement' => '', 'page' => '', 'page_entree' => '', 'referent' => '', 'utm' => [], 'gclid' => '', 'consent_ads' => ''],
        'fichiers' => [], 'accuse_reception' => 'non'];
}

groupe('Saisie d\'un appel par l\'admin : même Traitement, canal téléphone');
$trSaisie = (new Traitement($cfg, false))->pourSaisieAdmin(['auteur_id' => $camille, 'canal' => 'telephone']);
$r = $trSaisie->executer(['REQUEST_METHOD' => 'POST', 'HTTP_ACCEPT' => 'application/json', 'REMOTE_ADDR' => '127.0.0.1'], [], [
    'formulaire' => 'devis', 'canal' => 'telephone', 'nom' => 'Appel Fictif', 'telephone' => '079 000 00 13', 'travaux' => ['placo'], 'type_client' => 'regie',
    'surface' => '50-200', 'delai' => 'moins-1-mois', 'npa' => '1227', 'commune' => 'Carouge', 'connu_par' => 'recommandation', 'preference_contact' => 'appel',
], [], $quand);
egal(200, $r->statut, 'saisie acceptée sans piège temporel ni origine (session et CSRF vérifiés par l\'admin)');
$appel = $app->demandes->parRef((string) $r->corps['ref']);
ok($appel !== null && $appel['canal'] === 'telephone' && (int) $appel['cree_par'] === $camille && (int) $appel['associe_id'] === $camille, 'canal téléphone, auteur et associé = la personne qui saisit');
egal('appel-direct', $appel['categorie'], 'catégorie Source « appel-direct »');
egal('recommandation', $appel['canal_marketing'], 'canal déduit de « Comment nous avez-vous connus ? »');
egal(1, (int) $appel['canal_declare'], 'canal marqué « déclaré »');
ok(!str_contains((string) $appel['score_detail'], 'téléphone fourni'), 'pas de bonus « téléphone » sur une saisie');

// ============================================================== transitions
groupe('Transitions de statut (§4.5) vérifiées par le serveur');
$id = $d['id'];
$dm = $app->demandes;
refuse(fn () => $dm->agir($id, 'signee', ['montant' => '1000', 'date' => '2026-11-02'], $alex), 'Nouvelle → Signée refusée', 'Transition refusée');
refuse(fn () => $dm->agir($id, 'offre_envoyee', ['montant' => '1000'], $alex), 'Nouvelle → Offre envoyée refusée', 'Transition refusée');
refuse(fn () => $dm->agir($id, 'perdue', ['motif' => 'prix'], $alex), 'Nouvelle → Perdue refusée avant 3 appels sans réponse');
refuse(fn () => $dm->agir($id, 'inventee', [], $alex), 'action inconnue refusée');
$dm->agir($id, 'pas_de_reponse', [], $alex, 'admin', $t('2026-11-02 10:30'));
$d1 = $dm->parId($id);
egal(1, $d1['tentatives_appel'], 'Pas de réponse : tentative 1');
egal('nouvelle', $d1['statut'], 'reste « nouvelle »');
egal($t('2026-11-03 10:00')->getTimestamp(), $d1['echeance']->getTimestamp(), 'nouvelle échéance : lendemain ouvrable 10 h');
ok($d1['premier_appel_le'] !== null && $d1['premier_contact_le'] === null, 'premier appel noté, pas de premier contact');
refuse(fn () => $dm->agir($id, 'contact_etabli', ['version' => (string) $d['version']], $alex), 'version périmée refusée (deux personnes en même temps)', 'modifiée');
$dm->agir($id, 'contact_etabli', ['version' => (string) $d1['version']], $alex, 'admin', $t('2026-11-02 11:00'));
egal('contact_etabli', $dm->parId($id)['statut'], 'J\'ai eu la personne → Contact établi');
refuse(fn () => $dm->agir($id, 'visite_planifiee', ['date' => '2026-11-05'], $alex), 'visite sans heure refusée', 'heure');
$dm->agir($id, 'visite_planifiee', ['date' => '2026-11-05', 'heure' => '08:30', 'adresse' => 'Rue Fictive 2'], $alex, 'admin', $t('2026-11-02 11:05'));
egal('visite_planifiee', $dm->parId($id)['statut'], 'Contact établi → Visite planifiée');
refuse(fn () => $dm->agir($id, 'offre_envoyee', ['montant' => '0', 'date' => '2026-11-06'], $alex), 'offre sans montant refusée', 'montant');
$dm->agir($id, 'offre_envoyee', ['montant' => "12'500", 'date' => '2026-11-06'], $alex, 'admin', $t('2026-11-06 16:00'));
$d2 = $dm->parId($id);
egal('offre_envoyee', $d2['statut'], 'Visite planifiée → Offre envoyée');
egal(12500.0, (float) $d2['offre']['montant_ht'], 'montant de l\'offre (apostrophe suisse acceptée)');
egal('faite', $app->base->valeur('SELECT statut FROM visite WHERE demande_id = ?', [$id]), 'visite passée marquée faite');
$dm->agir($id, 'nouvelle_version', ['montant' => '11800', 'date' => '2026-11-09'], $alex, 'admin', $t('2026-11-09 09:00'));
egal(2, (int) $dm->parId($id)['offre']['version'], 'nouvelle version : version 2 en cours');
egal('remplacee', $app->base->valeur('SELECT statut FROM offre WHERE demande_id = ? AND version = 1', [$id]), 'ancienne version « remplacée »');
refuse(fn () => $dm->agir($id, 'signee', ['montant' => '11800'], $alex), 'signée sans date refusée', 'date');
refuse(fn () => $dm->agir($id, 'perdue', [], $alex), 'perdue sans motif refusée', 'motif');
$dm->agir($id, 'signee', ['montant' => '11500', 'date' => '2026-11-20'], $alex, 'admin', $t('2026-11-20 10:00'));
$d3 = $dm->parId($id);
egal('signee', $d3['statut'], 'Offre envoyée → Signée');
egal(11500.0, (float) $d3['offre']['montant_signe_ht'], 'montant signé enregistré (peut différer de l\'offre)');
refuse(fn () => $dm->agir($id, 'perdue', ['motif' => 'prix'], $alex), 'Signée → Perdue refusée sauf « annulé après signature »');
refuse(fn () => $dm->agir($id, 'rouvrir', [], $alex), 'Signée → Rouvrir refusé');
ok((int) $app->base->valeur('SELECT COUNT(*) FROM interaction WHERE demande_id = ?', [$id]) >= 8, 'chaque transition écrit une ligne d\'historique');
ok((int) $app->base->valeur("SELECT COUNT(*) FROM journal_audit WHERE action = 'changement_statut' AND objet_id = ?", [$ref]) >= 6, 'chaque transition écrite au journal d\'audit');
$idR = $rappel['id'];
foreach (['10:00', '10:05', '10:10'] as $h) {
    $dm->agir($idR, 'pas_de_reponse', [], $alex, 'admin', $t("2026-11-03 $h"));
}
refuse(fn () => $dm->agir($idR, 'pas_de_reponse', [], $alex), 'quatrième « pas de réponse » refusé', 'Trois tentatives');
refuse(fn () => $dm->agir($idR, 'perdue', ['motif' => 'prix'], $alex), 'après 3 appels, seul le motif « sans réponse » est accepté');
$dm->agir($idR, 'perdue', ['motif' => 'sans_reponse'], $alex, 'admin', $t('2026-11-04 10:00'));
egal('perdue', $dm->parId($idR)['statut'], 'Nouvelle → Perdue (sans réponse) après 3 tentatives');
$dm->agir($idR, 'rouvrir', [], $alex, 'admin', $t('2026-11-05 10:00'));
egal('nouvelle', $dm->parId($idR)['statut'], 'Perdue → Nouvelle (rouvrir, moins de 90 jours)');
egal(['contact_etabli', 'hors_cible'], array_keys(array_diff_key($dm->actionsPossibles($dm->parId($idR)), ['perdue' => 1])), 'actions proposées depuis « nouvelle » (pas de réponse épuisé)');

// ============================================================== indicateurs
groupe('Indicateurs (§5) sur un jeu de données daté');
$stockInd = dossierTemporaire();
$aNettoyer[] = $stockInd;
$cfgInd = configTest($stockInd);
$auj = $t('2027-04-22 09:40'); // jeudi
$appI = new App($cfgInd, null, $auj);
$u = $appI->auth->creerUtilisateur('ind@exemple.test', 'Ind Test', 'associe', 'terrain', 'phrase de passe pour les tests')['id'];
$bI = $appI->base;
$n = 0;
$ajouter = static function (string $recue, string $prio, string $canal, array $plus = []) use ($bI, &$n): int {
    $n++;
    $id = $bI->inserer('demande', $plus + [
        'ref' => sprintf('AC-2027-%04d', $n), 'recue_le' => Base::utc(new \DateTimeImmutable($recue, new \DateTimeZone('Europe/Zurich'))), 'canal' => 'site', 'formulaire' => 'devis',
        'priorite' => $prio, 'score' => 50, 'statut' => 'nouvelle', 'statut_change_le' => Base::utc(new \DateTimeImmutable($recue, new \DateTimeZone('Europe/Zurich'))),
        'cree_le' => Base::maintenant(), 'modifie_le' => Base::maintenant(), 'mode_test' => 0,
    ]);
    $bI->inserer('attribution', ['demande_id' => $id, 'categorie' => 'x', 'canal_marketing' => $canal]);
    return $id;
};
$offre = static function (int $id, string $envoyee, float $montant, ?string $signee = null, ?float $signe = null) use ($bI): void {
    $bI->inserer('offre', ['demande_id' => $id, 'numero' => 'O', 'version' => 1, 'montant_ht' => $montant, 'envoyee_le' => $envoyee, 'statut' => $signee ? 'signee' : 'envoyee',
        'signee_le' => $signee, 'montant_signe_ht' => $signe, 'cree_le' => Base::maintenant()]);
};
// Mars 2027 : 10 demandes comptées (dont 1 appel entrant) + 1 test + 1 doublon exclus.
$zh = static fn (string $s) => Base::utc(new \DateTimeImmutable($s, new \DateTimeZone('Europe/Zurich')));
$m1 = $ajouter('2027-03-01 08:00', 'A', 'google_ads', ['premier_contact_le' => $zh('2027-03-01 09:00'), 'premier_appel_le' => $zh('2027-03-01 09:00'), 'echeance_initiale_le' => $zh('2027-03-01 10:00')]); // 60 min
$m2 = $ajouter('2027-03-05 17:00', 'A', 'google_ads', ['premier_contact_le' => $zh('2027-03-08 08:00'), 'premier_appel_le' => $zh('2027-03-08 08:00'), 'echeance_initiale_le' => $zh('2027-03-08 08:00')]); // ven. 17 h → lun. 8 h : 120 min ouvrables
$m3 = $ajouter('2027-03-10 10:00', 'A', 'recherche', ['premier_contact_le' => $zh('2027-03-10 14:00'), 'premier_appel_le' => $zh('2027-03-10 13:00'), 'echeance_initiale_le' => $zh('2027-03-10 12:00')]); // 240 min, appel après l'échéance
$m4 = $ajouter('2027-03-11 09:00', 'A', 'meta', ['canal' => 'telephone', 'premier_contact_le' => $zh('2027-03-11 09:00')]); // appel entrant : exclu du délai
$m5 = $ajouter('2027-03-12 09:00', 'B', 'google_ads');
$m6 = $ajouter('2027-03-15 09:00', 'B', 'recommandation');
$m7 = $ajouter('2027-03-16 09:00', 'C', 'recherche');
$m8 = $ajouter('2027-03-17 09:00', 'C', 'autres', ['priorite_corrigee' => 'B']); // corrigée : B fait foi
$m9 = $ajouter('2027-03-18 09:00', 'hors_cible', 'autres');
$m10 = $ajouter('2027-03-31 23:30', 'A', 'google_ads'); // 31 mars 23 h 30 à Zurich (UTC : 21 h 30) : en mars
$ajouter('2027-03-20 09:00', 'A', 'google_ads', ['mode_test' => 1]);
$ajouter('2027-03-21 09:00', 'A', 'google_ads', ['statut' => 'doublon']);
$ajouter('2027-04-01 00:30', 'A', 'google_ads'); // 1er avril 0 h 30 à Zurich (UTC : 31 mars 22 h 30) : en avril
// Février : 5 demandes ; offres envoyées en mars : 3 (demande→offre mars = 3 / 5).
$f = [];
for ($i = 1; $i <= 5; $i++) {
    $f[] = $ajouter("2027-02-0$i 09:00", 'A', 'google_ads');
}
$offre($f[0], '2027-03-03', 10000, '2027-04-05', 9500);
$offre($f[1], '2027-03-10', 20000);
$offre($m1, '2027-03-20', 8000, '2027-03-28', 8000);
// Cohorte offre→signée au 22.04 : offres envoyées entre le 23.10.2026 et le 21.02.2027.
$vieux = [];
for ($i = 1; $i <= 4; $i++) {
    $vieux[] = $ajouter("2026-12-0$i 09:00", 'B', 'recherche');
}
$offre($vieux[0], '2026-12-10', 5000, '2027-01-15', 5000);
$offre($vieux[1], '2026-12-11', 6000);
$offre($vieux[2], '2027-01-05', 7000, '2027-02-01', 7000);
$offre($vieux[3], '2027-02-25', 9000); // hors cohorte (moins de 60 jours)
$bI->inserer('depense', ['mois' => '2027-03-01', 'canal_marketing' => 'google_ads', 'montant_ht' => 1200, 'type_cout' => 'media', 'origine' => 'saisie', 'saisi_le' => Base::maintenant()]);
$bI->inserer('depense', ['mois' => '2027-03-01', 'canal_marketing' => 'meta', 'montant_ht' => 150, 'type_cout' => 'media', 'origine' => 'saisie', 'saisi_le' => Base::maintenant()]);
$appI->definirParametre('mise_en_ligne', '2026-11');
$appI->definirParametre('marge_brute', 0.3);
$ind = new Indicateurs($appI);
$mars = $ind->mois('2027-03');
egal(10, $mars['demandes'], 'demandes/mois de mars : 10 (tests et doublons exclus, fuseau de Zurich)');
egal(5, $mars['demandes_prec'], 'février : 5');
egal(['A' => 5, 'B' => 3, 'C' => 1, 'hors_cible' => 1], array_map('intval', $mars['comptes']), 'répartition par priorité (priorité corrigée prise en compte)');
proche(8 / 9, $mars['part_ab'], 'part A+B = (A+B)/(A+B+C) = 8/9');
proche(120.0, $mars['delai_a'], 'délai médian A en minutes ouvrables (60, 120, 240 ; appel entrant exclu ; week-end non compté)');
egal(['ok' => 2, 'total' => 3], $mars['dans_delai'], 'rappelées dans le délai : 2 sur 3');
proche(3 / 5, $mars['demande_offre']['taux'] ?? null, 'taux demande→offre de mars = offres de mars / demandes de février = 3/5');
egal(8000.0, $mars['ca_signe'], 'CA signé de mars (date de signature)');
egal(1, $mars['nb_signes'], 'un chantier signé en mars');
egal(1350.0, $mars['depense_payante'], 'dépense des canaux payants (Google Ads + Meta)');
egal(5, $mars['demandes_payantes'], 'demandes des canaux payants (4 Google Ads + 1 Meta)');
proche(270.0, $mars['cpl'], 'CPL = 1350 / 5');
$avril = $ind->mois('2027-04');
egal(1, $avril['demandes'], 'avril : la demande du 1er à 0 h 30 compte en avril');
$coh = $ind->cohorteOffreSignee($auj, $ind->offres());
egal(['signees' => 2, 'offres' => 3], ['signees' => $coh['signees'], 'offres' => $coh['offres']], 'cohorte offre→signée (J−180 à J−60) : 2 sur 3');
proche(round((5000 + 7000 + 8000 + 9500) / 4, 6), $ind->panierMoyen($auj), 'panier moyen sur 6 mois glissants');
$cm = $ind->cplMax($auj, 0.6, 2 / 3, '2027-04');
proche(7375 * 0.3 * 0.6 * (2 / 3), $cm['max'], 'CPL max = panier × marge × demande→offre × offre→signée');
proche($cm['max'] / 3, $cm['cible'], 'cible CPL = CPL max / 3');
egal(5, $ind->numeroMois('2027-03'), 'mars 2027 = M5 (mise en ligne en novembre 2026)');
egal(null, $ind->objectif('demandes', '2026-12'), 'pas d\'objectif avant M3');
proche(10.0, $ind->objectif('demandes', '2027-01'), 'objectif M3 = 10 demandes');
proche(10 + 8 * 2 / 3, $ind->objectif('demandes', '2027-03'), 'objectif M5 interpolé entre M3 et M6');
proche(30.0, $ind->objectif('demandes', '2028-06'), 'au-delà de M12 : objectif M12');
$acq = $ind->acquisition(['2027-03']);
$ga = $acq['lignes']['google_ads'];
egal([4, 1200.0, 1, 8000.0], [$ga['demandes'], $ga['depense'], $ga['signees'], $ga['ca']], 'Acquisition Google Ads : demandes, dépense, signés, CA');
proche(300.0, $ga['cpl'], 'CPL Google Ads = 1200 / 4');
proche(1200.0, $ga['cac'], 'CAC = dépense / chantiers signés');
proche(8000 / 1200, $ga['roas'], 'ROAS = CA / dépense');
proche((8000 * 0.3 - 1200) / 1200, $ga['roi'], 'ROI = (CA × marge − dépense) / dépense');
egal(null, $acq['lignes']['recommandation']['cpl'], 'canal sans dépense : CPL « — »');
$ent = $ind->entonnoir($t('2027-03-01 00:00'));
egal(11, $ent['etapes'][0][1], 'entonnoir : demandes depuis le 1er mars');
egal(['recherche', true], Canaux::deduire('appel-direct', 'recherche-google', ['recherche-google' => 'recherche-google']), 'canaux : appel déclaré « recherche Google » → Recherche Google, déclaré');
egal(['google_ads', false], Canaux::deduire('google-ads', 'recommandation', ['recommandation' => 'recommandation']), 'canaux : la source mesurée prime sur le déclaratif');

// ================================================================= comptes
groupe('Authentification : mot de passe, 2FA, blocage, codes de secours, CSRF');
$_SESSION = [];
$auth = $app->auth;
refuse(fn () => $auth->creerUtilisateur('court@exemple.test', 'Court', 'associe', null, 'trop court'), 'mot de passe de moins de 12 caractères refusé', '12');
refuse(fn () => $auth->creerUtilisateur('alex@exemple.test', 'Doublon', 'associe', null, 'une phrase de passe assez longue'), 'adresse déjà utilisée refusée');
$cree = $auth->creerUtilisateur('secretariat@exemple.test', 'Secrétariat Test', 'secretariat', null, 'phrase secrète du secrétariat');
$hash = (string) $app->base->valeur('SELECT mdp_hash FROM utilisateur WHERE id = ?', [$cree['id']]);
ok(str_starts_with($hash, '$argon2id$') || str_starts_with($hash, '$2y$'), 'mot de passe haché (argon2id ou bcrypt)');
ok(!str_contains((string) $app->base->valeur('SELECT totp_secret FROM utilisateur WHERE id = ?', [$cree['id']]), $cree['secret']), 'secret TOTP jamais en clair en base');
egal(false, $auth->etapeMotDePasse('secretariat@exemple.test', 'mauvais mot de passe')['ok'], 'mauvais mot de passe refusé');
egal(false, $auth->etapeMotDePasse('inconnu@exemple.test', 'peu importe ici')['ok'], 'compte inconnu refusé (même message)');
ok($auth->etapeMotDePasse('secretariat@exemple.test', 'phrase secrète du secrétariat')['ok'] && $auth->en2fa(), 'bon mot de passe : étape du code');
egal(null, $auth->utilisateur(), 'pas encore connecté avant le code');
egal(false, $auth->etapeCode('000000')['ok'], 'code faux refusé');
$code = Totp::code(Totp::base32Decoder($cree['secret']), time());
ok($auth->etapeCode($code)['ok'] && $auth->utilisateur() !== null, 'code TOTP juste : connecté');
$auth->deconnecter();
egal(null, $auth->utilisateur(), 'déconnexion');
$auth->etapeMotDePasse('secretariat@exemple.test', 'phrase secrète du secrétariat');
egal(false, $auth->etapeCode($code)['ok'], 'même code TOTP réutilisé : refusé (rejeu)');
$auth->etapeMotDePasse('secretariat@exemple.test', 'phrase secrète du secrétariat');
ok($auth->etapeCode($cree['codes'][0])['ok'], 'code de secours accepté');
$auth->deconnecter();
$auth->etapeMotDePasse('secretariat@exemple.test', 'phrase secrète du secrétariat');
egal(false, $auth->etapeCode($cree['codes'][0])['ok'], 'code de secours à usage unique');
$auth->deconnecter();
for ($i = 0; $i < 4; $i++) {
    $auth->etapeMotDePasse('secretariat@exemple.test', 'mauvais mot de passe ' . $i);
}
$r = $auth->etapeMotDePasse('secretariat@exemple.test', 'phrase secrète du secrétariat');
ok(!$r['ok'] && str_contains($r['message'], 'bloqué'), '5 échecs : compte bloqué 15 minutes, même avec le bon mot de passe', $r['message']);
ok((int) $app->base->valeur("SELECT COUNT(*) FROM journal_audit WHERE action = 'compte_bloque'") === 1, 'blocage écrit au journal d\'audit');
$_SESSION = ['csrf' => str_repeat('a', 64)];
ok($auth->verifierCsrf(str_repeat('a', 64)), 'jeton CSRF de la session accepté');
ok(!$auth->verifierCsrf(str_repeat('b', 64)) && !$auth->verifierCsrf(null) && !$auth->verifierCsrf(['x']), 'jeton CSRF absent ou faux refusé');
ok(!$auth->verifierCsrf(str_repeat('a', 64), ['HTTP_SEC_FETCH_SITE' => 'cross-site']), 'requête intersite refusée même avec le jeton');
ok(Auth::peut(['role' => 'associe'], 'effacer') && !Auth::peut(['role' => 'secretariat'], 'effacer') && !Auth::peut(['role' => 'agence_marketing'], 'demandes') && !Auth::peut(null, 'vue'), 'droits par rôle (§6.5)');

// ============================================================ nLPD
groupe('Données personnelles : export et effacement sans fausser les indicateurs');
$appP = new App($cfg, null, $t('2026-11-25 10:00'));
$personnes = new Personnes($appP);
$trouves = $personnes->rechercher('079 000 00 11');
egal(1, count($trouves), 'personne retrouvée par téléphone (tous formats)');
egal(1, count($personnes->rechercher('Personne.Fictive@exemple.test')), 'personne retrouvée par e-mail');
$contactId = (int) $trouves[0]['id'];
$export = $personnes->exporter($contactId);
ok(($export['contact']['nom'] ?? '') === 'Personne Fictive' && count($export['demandes']) >= 1 && isset($export['demandes'][0]['historique']), 'export : coordonnées, demandes et historique');
$indAvant = (new Indicateurs($appP))->mois('2026-11');
$personnes->effacer($contactId);
$indApres = (new Indicateurs($appP))->mois('2026-11');
$contact = $appP->base->un('SELECT * FROM contact WHERE id = ?', [$contactId]);
ok($contact['nom'] === null && $contact['email'] === null && $contact['telephone_e164'] === null && $contact['anonymise_le'] !== null, 'effacement : nom, e-mail, téléphone effacés');
$dEff = $appP->demandes->parRef($ref);
ok($dEff['message'] === null && $dEff['commune'] === null && $dEff['gclid'] === null && $dEff['statut'] === 'signee' && $dEff['priorite'] !== null, 'demande anonymisée : message, commune, gclid effacés ; statut et priorité gardés');
egal(0, (int) $appP->base->valeur('SELECT COUNT(*) FROM fichier WHERE demande_id = ? AND supprime_le IS NULL', [$dEff['id']]), 'fichiers effacés');
egal([$indAvant['demandes'], $indAvant['comptes'], $indAvant['ca_signe']], [$indApres['demandes'], $indApres['comptes'], $indApres['ca_signe']], 'indicateurs du mois inchangés après effacement');
ok((int) $appP->base->valeur("SELECT COUNT(*) FROM journal_audit WHERE action IN ('export_personne', 'effacement')") === 2, 'export et effacement au journal');
egal('Personne effacée', $dEff['nom_complet'], 'affichage : « Personne effacée »');
refuse(fn () => $appP->demandes->agir($dEff['id'], 'perdue', ['motif' => 'annule'], $alex), 'plus aucune action sur une demande effacée');
$journal = implode(' ', array_column($appP->base->tous('SELECT details FROM journal_audit'), 'details'));
ok(!str_contains($journal, 'Fictive') && !str_contains($journal, '079') && !str_contains($journal, '@exemple'), 'journal d\'audit sans valeur personnelle');

// ======================================================= HTTP (serveur local)
groupe('Contrôle d\'accès HTTP : chaque écran exige une session (php -S, port libre)');
$racineSite = dirname(__DIR__, 2);
$stockHttp = dossierTemporaire();
$aNettoyer[] = $stockHttp;
$fichierConfig = $stockHttp . '/config.php';
file_put_contents($fichierConfig, '<?php return ' . var_export(valeursConfig($stockHttp . '/stockage'), true) . ';');
$appH = new App(Config::charger($fichierConfig));
$asso = $appH->auth->creerUtilisateur('http.associe@exemple.test', 'Associé HTTP', 'associe', 'terrain', 'phrase de passe du test http');
$agence = $appH->auth->creerUtilisateur('http.agence@exemple.test', 'Agence HTTP', 'agence_marketing', null, 'phrase de passe de l agence');
$trH = new Traitement($appH->config, false);
$asH = new AntiSpam($appH->config);
$rH = $trH->executer($serveur, [], array_merge($devis, ['nom' => 'Nom Secret Zorglub', 'commune' => 'Vésenaz', 'form_t0' => $asH->creerJeton(time() - 40)]), []);
$refH = (string) $rH->corps['ref'];
$port = portLibre();
$proc = proc_open([PHP_BINARY, '-S', "127.0.0.1:$port", '-t', $racineSite], [1 => ['file', '/dev/null', 'w'], 2 => ['file', '/dev/null', 'w']], $tubes, null, ['AC_API_CONFIG' => $fichierConfig] + getenv());
for ($i = 0; $i < 50 && !@fsockopen('127.0.0.1', $port); $i++) {
    usleep(100000);
}
$base = "http://127.0.0.1:$port/admin/";
/** @return array{code: int, entetes: string, corps: string} */
$http = static function (string $url, ?array $post = null, ?string $jar = null) use ($base): array {
    $ch = curl_init(str_starts_with($url, 'http') ? $url : $base . $url);
    curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_HEADER => true, CURLOPT_FOLLOWLOCATION => false, CURLOPT_TIMEOUT => 10]);
    if ($jar !== null) {
        curl_setopt_array($ch, [CURLOPT_COOKIEJAR => $jar, CURLOPT_COOKIEFILE => $jar]);
    }
    if ($post !== null) {
        curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => http_build_query($post)]);
    }
    $rep = (string) curl_exec($ch);
    $taille = (int) curl_getinfo($ch, CURLINFO_HEADER_SIZE);
    $code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    curl_close($ch);
    return ['code' => $code, 'entetes' => substr($rep, 0, $taille), 'corps' => substr($rep, $taille)];
};
try {
    $pages = ['', '?p=vue', '?p=a-traiter', '?p=demandes', '?p=demandes&vue=colonnes', '?p=export', "?p=fiche&ref=$refH", '?p=fichier&id=1', '?p=saisie', '?p=acquisition', '?p=parametres', '?p=donnees', '?p=compte', '?p=plus'];
    foreach ($pages as $p) {
        $r = $http($p);
        ok(in_array($r['code'], [200, 303], true) && ($p === '' ? str_contains($r['corps'], 'Connexion') || str_contains($r['entetes'], 'p=connexion') : $r['code'] === 303 && str_contains($r['entetes'], 'Location: /admin/?p=connexion')), "sans session : « $p » → connexion", $r['code'] . ' ' . strtok($r['entetes'], "\n"));
        ok(!str_contains($r['corps'], 'Zorglub'), "sans session : « $p » ne montre aucune donnée");
    }
    $r = $http('?p=connexion');
    ok(str_contains($r['entetes'], "Content-Security-Policy: default-src 'self'; script-src 'self'") && str_contains($r['entetes'], "frame-ancestors 'none'"), 'CSP stricte (aucun script en ligne, pas d\'iframe)');
    ok(str_contains($r['entetes'], 'X-Robots-Tag: noindex') && str_contains($r['entetes'], 'X-Content-Type-Options: nosniff') && str_contains($r['entetes'], 'Referrer-Policy: no-referrer'), 'en-têtes de sécurité et noindex');
    ok((bool) preg_match('/Set-Cookie: ac_admin=[^;]+; path=\/; HttpOnly; SameSite=Lax/i', $r['entetes']), 'cookie de session HttpOnly, SameSite=Lax');
    ok(!preg_match('/<script(?![^>]*\bsrc=)[^>]*>/i', $r['corps']) && !str_contains($r['corps'], 'style="'), 'aucun script ni style en ligne dans la page');
    egal(403, $http('?p=connexion', ['etape' => 'mot_de_passe', 'email' => 'http.associe@exemple.test', 'mot_de_passe' => 'phrase de passe du test http'])['code'], 'POST sans jeton CSRF : 403');
    egal(404, $http('?p=inconnue')['code'], 'écran inconnu : 404');
    egal(404, $http("http://127.0.0.1:$port/admin/outils/demo.php")['code'], 'outils/demo.php appelé par le web : 404 (CLI seulement)');

    $connecter = static function (string $email, string $mdp, string $secret, string $jar) use ($http): bool {
        $page = $http('?p=connexion', null, $jar);
        preg_match('/name="_csrf" value="([a-f0-9]{64})"/', $page['corps'], $m);
        $r = $http('?p=connexion', ['_csrf' => $m[1] ?? '', 'etape' => 'mot_de_passe', 'email' => $email, 'mot_de_passe' => $mdp], $jar);
        $page = $http('?p=connexion', null, $jar);
        preg_match('/name="_csrf" value="([a-f0-9]{64})"/', $page['corps'], $m);
        $r = $http('?p=connexion', ['_csrf' => $m[1] ?? '', 'etape' => 'code', 'code' => Totp::code(Totp::base32Decoder($secret), time())], $jar);
        return $r['code'] === 303 && !str_contains($r['entetes'], 'p=connexion');
    };
    $jarA = $stockHttp . '/cookies-associe.txt';
    ok($connecter('http.associe@exemple.test', 'phrase de passe du test http', $asso['secret'], $jarA), 'connexion associé : mot de passe puis code TOTP');
    foreach (['?p=vue', '?p=a-traiter', '?p=demandes', '?p=demandes&vue=colonnes', "?p=fiche&ref=$refH", '?p=saisie', '?p=acquisition', '?p=parametres', '?p=donnees', '?p=compte'] as $p) {
        $r = $http($p, null, $jarA);
        egal(200, $r['code'], "associé : « $p » → 200");
    }
    $fiche = $http("?p=fiche&ref=$refH", null, $jarA);
    ok(str_contains($fiche['corps'], 'Nom Secret Zorglub'), 'associé : la fiche montre la demande');
    preg_match('/name="_csrf" value="([a-f0-9]{64})"/', $fiche['corps'], $m);
    $r = $http("?p=fiche&ref=$refH", ['op' => 'statut', 'action' => 'signee', 'montant' => '1000', 'date' => date('Y-m-d')], $jarA);
    egal(403, $r['code'], 'action sans jeton CSRF refusée (403)');
    $r = $http("?p=fiche&ref=$refH", ['_csrf' => $m[1], 'op' => 'statut', 'action' => 'signee', 'montant' => '1000', 'date' => date('Y-m-d')], $jarA);
    egal('nouvelle', $appH->demandes->parRef($refH)['statut'], 'transition interdite envoyée à la main : refusée par le serveur');
    $r = $http("?p=fiche&ref=$refH", ['_csrf' => $m[1], 'op' => 'statut', 'action' => 'contact_etabli'], $jarA);
    egal('contact_etabli', $appH->demandes->parRef($refH)['statut'], 'transition permise avec jeton : appliquée');
    $csv = $http('?p=export&statut=toutes', null, $jarA);
    ok($csv['code'] === 200 && str_contains($csv['entetes'], 'text/csv') && str_contains($csv['corps'], $refH), 'export CSV (associé)');

    $jarG = $stockHttp . '/cookies-agence.txt';
    ok($connecter('http.agence@exemple.test', 'phrase de passe de l agence', $agence['secret'], $jarG), 'connexion agence marketing');
    foreach (['?p=vue', '?p=acquisition', '?p=parametres&onglet=depenses'] as $p) {
        $r = $http($p, null, $jarG);
        ok($r['code'] === 200 && !str_contains($r['corps'], 'Zorglub') && !str_contains($r['corps'], 'Vésenaz') && !str_contains($r['corps'], '079 000') && !str_contains($r['corps'], '@exemple.test>') && !str_contains($r['corps'], 'personne.fictive'), "agence : « $p » sans nom, téléphone, e-mail ni commune");
    }
    foreach (['?p=demandes', '?p=a-traiter', "?p=fiche&ref=$refH", '?p=saisie', '?p=export', '?p=donnees', '?p=parametres&onglet=utilisateurs', '?p=fichier&id=1'] as $p) {
        egal(403, $http($p, null, $jarG)['code'], "agence : « $p » refusé (403)");
    }
} finally {
    $statut = proc_get_status($proc);
    if ($statut['running']) {
        posix_kill($statut['pid'], SIGTERM);
    }
    proc_close($proc);
}

foreach ($aNettoyer as $dossier) {
    supprimer($dossier);
}
$n = $GLOBALS['resultats']['ok'];
$echecs = $GLOBALS['resultats']['echecs'];
echo "\n" . ($echecs === [] ? "\033[32m" : "\033[31m") . "$n vérifications réussies, " . count($echecs) . " échec(s)\033[0m\n";
foreach ($echecs as $e) {
    echo "  - $e\n";
}
exit($echecs === [] ? 0 : 1);
