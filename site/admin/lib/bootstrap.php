<?php
/**
 * Amorçage de l'admin : celui de l'API (erreurs non affichées, fuseau, UTF-8,
 * classes AndyConstruct\Api) puis les classes AndyConstruct\Admin de lib/.
 */
declare(strict_types=1);

require dirname(__DIR__, 2) . '/api/lib/bootstrap.php';

spl_autoload_register(static function (string $classe): void {
    $prefixe = 'AndyConstruct\\Admin\\';
    if (strncmp($classe, $prefixe, strlen($prefixe)) !== 0) {
        return;
    }
    $fichier = __DIR__ . '/' . str_replace('\\', '/', substr($classe, strlen($prefixe))) . '.php';
    if (is_file($fichier)) {
        require $fichier;
    }
});
