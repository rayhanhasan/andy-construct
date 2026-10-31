<?php
/**
 * Point d'entrée des formulaires du site Andy Construct.
 *
 *   GET  /api/demande.php?jeton  → {"ok":true,"jeton":"v1.…"} (piège temporel)
 *   POST /api/demande.php        → demande de devis, de rappel ou d'aimant
 *
 * Contrat complet : docs/v2/contrat-interface.md
 */
declare(strict_types=1);

require __DIR__ . '/lib/bootstrap.php';

use AndyConstruct\Api\Config;
use AndyConstruct\Api\Resultat;
use AndyConstruct\Api\Traitement;

try {
    $config = Config::charger();
    $traitement = new Traitement($config);
    ini_set('error_log', $traitement->stockage()->dossier('journaux') . '/php-erreurs.log');
    $resultat = $traitement->executer($_SERVER, $_GET, $_POST, $_FILES);
} catch (\Throwable $e) {
    error_log('[andy-construct] demande.php : ' . get_class($e) . ' ' . basename($e->getFile()) . ':' . $e->getLine());
    $resultat = new Resultat(500, 'json', [
        'ok' => false,
        'code' => 'technique',
        'message' => "Un problème technique nous empêche d'enregistrer votre demande. Réessayez dans quelques minutes, ou appelez-nous au +41 22 771 20 15.",
        'ref' => null,
    ]);
    $traitement = null;
}

$resultat->emettre();

// La réponse part au visiteur ; la file d'attente et la purge passent ensuite.
if ($traitement !== null && ($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    if (function_exists('fastcgi_finish_request')) {
        fastcgi_finish_request();
    } elseif (function_exists('litespeed_finish_request')) {
        litespeed_finish_request();
    } else {
        @ob_end_flush();
        @flush();
    }
    $traitement->apresReponse();
}
