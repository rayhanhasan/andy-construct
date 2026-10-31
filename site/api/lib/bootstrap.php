<?php
/**
 * Amorçage commun aux points d'entrée (demande.php, cron.php, fichier.php, tests).
 *
 * - aucune erreur PHP affichée au visiteur (journalisée dans le stockage privé) ;
 * - fuseau Europe/Zurich, UTF-8 ;
 * - chargement automatique des classes de lib/ et de PHPMailer (vendor/).
 */
declare(strict_types=1);

ini_set('display_errors', '0');
ini_set('display_startup_errors', '0');
ini_set('log_errors', '1');
ini_set('html_errors', '0');
// expose_php ne se règle pas dans .user.ini (PHP_INI_SYSTEM) : on retire l'en-tête ici.
if (PHP_SAPI !== 'cli' && !headers_sent()) {
    header_remove('X-Powered-By');
}
error_reporting(E_ALL);
date_default_timezone_set('Europe/Zurich');
mb_internal_encoding('UTF-8');

spl_autoload_register(static function (string $classe): void {
    $prefixe = 'AndyConstruct\\Api\\';
    if (strncmp($classe, $prefixe, strlen($prefixe)) !== 0) {
        return;
    }
    $relatif = str_replace('\\', '/', substr($classe, strlen($prefixe)));
    $fichier = __DIR__ . '/' . $relatif . '.php';
    if (is_file($fichier)) {
        require $fichier;
    }
});

$autoloadVendor = dirname(__DIR__) . '/vendor/autoload.php';
if (is_file($autoloadVendor)) {
    require_once $autoloadVendor;
}
