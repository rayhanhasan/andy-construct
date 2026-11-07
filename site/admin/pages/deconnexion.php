<?php
declare(strict_types=1);

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Http;
use AndyConstruct\Admin\Vue;

return static function (App $app): string {
    if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
        Http::rediriger(Vue::url('compte'));
    }
    $app->auth->deconnecter();
    Http::rediriger(Vue::url('connexion'));
};
