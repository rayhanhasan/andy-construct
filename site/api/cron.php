<?php
/**
 * Tâche planifiée (toutes les 10 minutes) :
 *  - renvoie à n8n les demandes restées en file d'attente ;
 *  - renvoie les e-mails mis de côté après un échec SMTP ;
 *  - insère en base les demandes restées en attente (base indisponible lors de l'envoi) ;
 *  - purge les fichiers, journaux et limites expirés ;
 *  - alerte l'agence si une demande attend depuis plus d'une heure ;
 *  - signale son passage à Healthchecks.io (si configuré).
 *
 * Lancement :
 *   en ligne de commande : php /chemin/vers/api/cron.php
 *   par URL (hébergeurs sans cron CLI) : https://…/api/cron.php?cle=<cron_cle>
 */
declare(strict_types=1);

require __DIR__ . '/lib/bootstrap.php';

use AndyConstruct\Api\Config;
use AndyConstruct\Api\Traitement;

$cli = PHP_SAPI === 'cli';
if (!$cli) {
    header('Content-Type: text/plain; charset=utf-8');
    header('Cache-Control: no-store');
    header('X-Robots-Tag: noindex');
}

try {
    $config = Config::charger();
} catch (\Throwable $e) {
    if (!$cli) {
        http_response_code(503);
    }
    echo "Configuration absente.\n";
    exit(1);
}

if (!$cli) {
    $cle = (string) $config->get('cron_cle', '');
    $fournie = is_string($_GET['cle'] ?? null) ? $_GET['cle'] : '';
    if (strlen($cle) < 24 || !hash_equals($cle, $fournie)) {
        http_response_code(403);
        echo "Accès refusé.\n";
        exit(1);
    }
}

set_time_limit(120);

$traitement = new Traitement($config);
ini_set('error_log', $traitement->stockage()->dossier('journaux') . '/php-erreurs.log');
$journal = $traitement->journal();
$forcer = $cli && in_array('--forcer', $argv ?? [], true);

$file = $traitement->webhook()->traiterFile(50, $forcer);
$mails = $traitement->courriel()->reessayer(20);
$base = $traitement->depot()->traiterFile(50);
$purge = $traitement->purger();

if ($file['a_signaler'] !== [] && (string) $config->get('alerte_email', '') !== '') {
    $texte = "Des demandes du site n'ont pas encore pu être transmises à n8n.\n"
        . "Les associés ont bien reçu l'e-mail interne de chaque demande : rien n'est perdu.\n\n"
        . "Références concernées :\n- " . implode("\n- ", $file['a_signaler']) . "\n\n"
        . "À vérifier : n8n est-il joignable (URL du webhook, certificat, pare-feu) ? Le secret HMAC est-il identique des deux côtés ?\n"
        . "Relance manuelle : php api/cron.php --forcer\n";
    $traitement->courriel()->envoyer($traitement->modeles()->alerte('File d\'attente vers n8n', $texte));
}

// Auto-contrôle (une fois par jour) : si le stockage est dans la racine web, il ne doit
// pas être lisible depuis le web (hébergeurs nginx qui ignorent les .htaccess).
$stockageReel = realpath((string) $config->get('stockage')) ?: '';
$marqueur = $traitement->stockage()->dossier('verrous') . '/controle-exposition';
if ($stockageReel !== '' && str_starts_with($stockageReel, __DIR__ . '/') && function_exists('curl_init')
    && (!is_file($marqueur) || filemtime($marqueur) < time() - 86400)) {
    @touch($marqueur);
    $url = rtrim((string) $config->get('url_api'), '/') . '/' . substr($stockageReel, strlen(__DIR__) + 1) . '/compteurs/' . date('Y') . '.txt';
    $ch = curl_init($url);
    curl_setopt_array($ch, [CURLOPT_NOBODY => true, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 5]);
    curl_exec($ch);
    $code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    curl_close($ch);
    if ($code === 200) {
        $journal->erreur('stockage_expose', ['code' => $code]);
        $traitement->courriel()->envoyer($traitement->modeles()->alerte(
            'Stockage privé accessible depuis le web',
            "Le dossier de stockage répond en HTTP 200 ($url).\nLes règles .htaccess ne sont pas appliquées par l'hébergeur (nginx ?).\n"
            . "À faire tout de suite : déplacer le stockage hors de la racine web (clé « stockage » de config.php) ou interdire ce chemin dans la configuration du serveur.\n"
        ));
    }
}

$bilan = [
    'file_livres' => $file['livres'],
    'file_echecs' => $file['echecs'],
    'file_restants' => $file['restants'],
    'file_plus_ancien_min' => $file['plus_ancien_minutes'],
    'mails_renvoyes' => $mails['envoyes'],
    'mails_echecs' => $mails['echecs'],
    'base_inserees' => $base['inserees'],
    'base_restantes' => $base['restantes'],
] + array_combine(array_map(static fn ($k) => "purge_$k", array_keys($purge)), array_values($purge));
$journal->info('cron', $bilan);

// Supervision : ping Healthchecks.io ; « /fail » si une demande attend depuis plus d'une heure.
$ping = (string) $config->get('healthcheck_url', '');
if ($ping !== '' && preg_match('~^https://~', $ping) && function_exists('curl_init')) {
    $enRetard = $file['plus_ancien_minutes'] >= (int) $config->get('conservation.file_attente_alerte_minutes', 60);
    $ch = curl_init(rtrim($ping, '/') . ($enRetard ? '/fail' : ''));
    curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 5, CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode($bilan)]);
    curl_exec($ch);
    curl_close($ch);
}

foreach ($bilan as $cle => $valeur) {
    echo str_pad($cle, 24) . ' ' . $valeur . "\n";
}
