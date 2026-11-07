<?php
/**
 * Téléchargement d'une pièce jointe : droits vérifiés et consultation journalisée ici,
 * puis redirection vers le lien signé existant de l'API (api/fichier.php, 10 minutes).
 * Le fichier n'a jamais d'adresse publique permanente.
 */
declare(strict_types=1);

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Http;
use AndyConstruct\Admin\Vue;
use AndyConstruct\Api\LiensFichiers;

return static function (App $app): string {
    $id = Http::get('id');
    $f = ctype_digit($id) ? $app->base->un('SELECT f.*, d.ref FROM fichier f JOIN demande d ON d.id = f.demande_id WHERE f.id = ? AND f.supprime_le IS NULL', [(int) $id]) : null;
    if ($f === null || !preg_match(LiensFichiers::MOTIF_ID, (string) $f['identifiant']) || !is_file($app->stockage->dossier('fichiers') . '/' . $f['identifiant'])) {
        Http::refuser(404, 'Fichier indisponible', "Ce fichier n'est plus sur le serveur (effacé ou purgé).");
    }
    $app->audit('consultation_fichier', 'demande', (string) $f['ref'], ['fichier' => (int) $f['id']]);
    $racineSite = rtrim(dirname(rtrim(Vue::$base, '/')), '/');
    $liens = new LiensFichiers($racineSite . '/api', $app->config->secret('local'));
    Http::rediriger($liens->url((string) $f['identifiant'], 1, time() - 3600 + 600));
};
