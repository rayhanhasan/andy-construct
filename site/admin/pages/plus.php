<?php
/** Menu « Plus » de la barre du bas (téléphone). */
declare(strict_types=1);

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Auth;
use AndyConstruct\Admin\Vue;

return static function (App $app): string {
    $liens = '';
    foreach ([['acquisition', 'Acquisition', 'acquisition'], ['parametres', 'Paramètres', 'depenses'], ['donnees', 'Journal et données personnelles', 'journal'], ['compte', 'Mon compte', 'compte']] as [$p, $lib, $droit]) {
        if (Auth::peut($app->utilisateur, $droit)) {
            $liens .= '<li><a href="' . Vue::e(Vue::url($p)) . '">' . Vue::e($lib) . '</a></li>';
        }
    }
    return Vue::page($app, 'plus', 'Plus', '<div class="entete-page"><h1>Plus</h1></div><nav aria-label="Autres écrans" class="panneau"><ul class="plus-menu">' . $liens . '</ul></nav>');
};
