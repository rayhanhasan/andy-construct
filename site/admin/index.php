<?php
/**
 * Tableau de bord d'administration Andy Construct : point d'entrée unique.
 *
 *   /admin/?p=<écran>   (écrans dans pages/, droits vérifiés ici pour chaque route)
 *
 * Plan : docs/v4/admin/plan-dashboard-admin.md · Installation : docs/v4/admin/README-admin.md
 */
declare(strict_types=1);

require __DIR__ . '/lib/bootstrap.php';

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Auth;
use AndyConstruct\Admin\Http;
use AndyConstruct\Admin\Vue;

Http::entetesSecurite();
header('Content-Type: text/html; charset=utf-8');
Vue::$base = rtrim(str_replace('\\', '/', dirname((string) ($_SERVER['SCRIPT_NAME'] ?? '/admin/index.php'))), '/') . '/';

try {
    $app = App::demarrer();
    $app->secretAdmin();
    ini_set('error_log', $app->stockage->dossier('journaux') . '/php-erreurs.log');
} catch (\Throwable $e) {
    error_log('[andy-construct admin] démarrage : ' . get_class($e) . ' ' . basename($e->getFile()) . ':' . $e->getLine());
    Http::refuser(503, 'Gestion indisponible', "L'admin n'est pas configuré ou la base est injoignable. Les demandes du site continuent d'arriver par e-mail. Prévenez l'agence technique.");
}

/** Écran => droit nécessaire (null : sans session). */
const ROUTES = [
    'connexion' => null,
    'deconnexion' => 'compte',
    'vue' => 'vue',
    'a-traiter' => 'demandes',
    'demandes' => 'demandes',
    'export' => 'export',
    'fiche' => 'demandes',
    'fichier' => 'demandes',
    'saisie' => 'demandes',
    'score' => 'demandes',
    'acquisition' => 'acquisition',
    'parametres' => 'depenses',
    'donnees' => 'journal',
    'compte' => 'compte',
    'plus' => 'compte',
];

try {
    $app->auth->demarrerSession();
    $p = Http::get('p', '');
    $methode = strtoupper((string) ($_SERVER['REQUEST_METHOD'] ?? 'GET'));
    if (!in_array($methode, ['GET', 'HEAD', 'POST'], true)) {
        header('Allow: GET, POST');
        Http::refuser(405, 'Méthode refusée', 'Cette adresse accepte seulement GET et POST.');
    }
    if ($methode === 'POST' && !$app->auth->verifierCsrf($_POST['_csrf'] ?? null, $_SERVER)) {
        $app->audit('csrf_refuse', null, null, ['page' => mb_substr($p, 0, 20)], 'systeme');
        Http::refuser(403, 'Formulaire expiré', 'Le formulaire a expiré ou ne vient pas de cette application. Rechargez la page, puis recommencez.');
    }
    $utilisateur = $app->auth->utilisateur();
    if ($p === '') {
        $p = $utilisateur === null ? 'connexion' : (Auth::peut($utilisateur, 'vue') ? 'vue' : 'compte');
    }
    if (!array_key_exists($p, ROUTES)) {
        Http::refuser(404, 'Page introuvable', "Cette page n'existe pas.");
    }
    $droit = ROUTES[$p];
    if ($droit !== null) {
        if ($utilisateur === null) {
            if ($methode === 'GET' && $p !== 'deconnexion') {
                $_SESSION['apres_connexion'] = (string) ($_SERVER['REQUEST_URI'] ?? '');
            }
            Http::rediriger(Vue::url('connexion'));
        }
        if (!Auth::peut($utilisateur, $droit)) {
            $app->audit('acces_refuse', null, null, ['page' => $p], 'systeme');
            Http::refuser(403, 'Accès refusé', "Votre rôle ne donne pas accès à cet écran.");
        }
    }
    $page = require __DIR__ . '/pages/' . $p . '.php';
    echo $page($app);
} catch (\Throwable $e) {
    error_log('[andy-construct admin] ' . get_class($e) . ' ' . basename($e->getFile()) . ':' . $e->getLine() . ' ' . substr($e->getMessage(), 0, 300));
    if (!headers_sent()) {
        Http::refuser(500, 'Erreur technique', "L'opération n'a pas abouti. Rien n'a été perdu : rechargez la page. Si l'erreur revient, prévenez l'agence technique.");
    }
}
