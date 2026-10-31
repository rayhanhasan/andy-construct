<?php
/**
 * Téléchargement signé d'une pièce jointe reçue par le formulaire.
 *
 *   GET /api/fichier.php?id=<32 hex>.<ext>&exp=<horodatage>&sig=<hmac>
 *
 * Liens produits par l'e-mail interne (validité 7 jours) et pour n8n
 * (24 heures, pour joindre le fichier à l'affaire dans le CRM).
 */
declare(strict_types=1);

require __DIR__ . '/lib/bootstrap.php';

use AndyConstruct\Api\Config;
use AndyConstruct\Api\Journal;
use AndyConstruct\Api\LiensFichiers;
use AndyConstruct\Api\Stockage;
use AndyConstruct\Api\Televersement;

header('Cache-Control: private, no-store');
header('X-Content-Type-Options: nosniff');
header('X-Robots-Tag: noindex');
header("Content-Security-Policy: default-src 'none'; sandbox");

$refuser = static function (int $code): never {
    http_response_code($code);
    header('Content-Type: text/plain; charset=utf-8');
    echo $code === 404 ? "Ce lien a expiré ou le fichier n'existe plus.\n" : "Accès refusé.\n";
    exit;
};

try {
    $config = Config::charger();
} catch (\Throwable) {
    $refuser(503);
}

$id = is_string($_GET['id'] ?? null) ? $_GET['id'] : '';
$exp = is_string($_GET['exp'] ?? null) ? $_GET['exp'] : '';
$sig = is_string($_GET['sig'] ?? null) ? $_GET['sig'] : '';

$liens = new LiensFichiers((string) $config->get('url_api'), $config->secret('local'));
$stockage = new Stockage((string) $config->get('stockage'));
if (!$liens->verifier($id, $exp, $sig)) {
    (new Journal($stockage))->alerte('fichier_lien_refuse', []);
    $refuser(403);
}

$chemin = $stockage->dossier('fichiers') . '/' . $id;
if (!is_file($chemin)) {
    $refuser(404);
}

$ext = pathinfo($id, PATHINFO_EXTENSION);
header('Content-Type: ' . (Televersement::MIME_PAR_EXTENSION[$ext] ?? 'application/octet-stream'));
header('Content-Length: ' . (string) filesize($chemin));
header('Content-Disposition: attachment; filename="piece-jointe.' . $ext . '"');
readfile($chemin);
