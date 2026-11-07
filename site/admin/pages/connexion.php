<?php
/** Connexion en deux étapes : e-mail et mot de passe, puis code de l'application (ou code de secours). */
declare(strict_types=1);

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Http;
use AndyConstruct\Admin\Vue;

return static function (App $app): string {
    if ($app->utilisateur !== null) {
        Http::rediriger(Vue::url('vue'));
    }
    if (isset($_GET['recommencer'])) {
        unset($_SESSION['attente_2fa'], $_SESSION['attente_le']);
        Http::rediriger(Vue::url('connexion'));
    }
    $erreur = '';
    $etape2 = $app->auth->en2fa();
    if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
        if (Http::post('etape') === 'code') {
            $r = $app->auth->etapeCode(Http::post('code'));
            if ($r['ok']) {
                $apres = (string) ($_SESSION['apres_connexion'] ?? '');
                unset($_SESSION['apres_connexion']);
                Http::rediriger(str_starts_with($apres, Vue::$base) && !str_contains($apres, 'p=connexion') ? $apres : Vue::$base);
            }
            $erreur = $r['message'];
            $etape2 = $app->auth->en2fa();
        } else {
            $r = $app->auth->etapeMotDePasse(Http::post('email'), Http::post('mot_de_passe'));
            if ($r['ok']) {
                Http::rediriger(Vue::url('connexion'));
            }
            $erreur = $r['message'];
            $etape2 = false;
        }
    }
    $e = static fn ($v) => Vue::e($v);
    $alerte = $erreur !== '' ? '<p class="erreur-formulaire" role="alert" id="erreur-connexion">' . $e($erreur) . '</p>' : '';
    $decrit = $erreur !== '' ? ' aria-describedby="erreur-connexion"' : '';
    if ($etape2) {
        $form = '<h1>Code de vérification</h1><p class="sous-titre">Ouvrez l\'application d\'authentification de votre téléphone et saisissez le code à 6 chiffres « Andy Construct ».</p>' . $alerte
            . '<form method="post" action="' . $e(Vue::url('connexion')) . '" class="formulaire">' . Vue::csrf($app) . '<input type="hidden" name="etape" value="code">'
            . '<label class="champ" for="code"><span>Code à 6 chiffres</span><input id="code" name="code" inputmode="numeric" autocomplete="one-time-code" maxlength="11" required autofocus' . $decrit . '>'
            . '<span class="aide-champ">Téléphone perdu : saisissez l\'un de vos codes de secours (XXXXX-XXXXX).</span></label>'
            . '<button class="btn btn-principal btn-large" type="submit">Valider</button></form>'
            . '<p class="petit"><a href="' . $e(Vue::url('connexion', ['recommencer' => 1])) . '">Recommencer avec un autre compte</a></p>';
    } else {
        $form = '<h1>Connexion</h1><p class="sous-titre">Gestion des demandes, réservée à l\'équipe Andy Construct.</p>' . $alerte
            . '<form method="post" action="' . $e(Vue::url('connexion')) . '" class="formulaire">' . Vue::csrf($app) . '<input type="hidden" name="etape" value="mot_de_passe">'
            . '<label class="champ" for="email"><span>Adresse e-mail</span><input id="email" name="email" type="email" autocomplete="username" required autofocus' . $decrit . ' value="' . $e(Http::post('email')) . '"></label>'
            . '<label class="champ" for="mot_de_passe"><span>Mot de passe</span><input id="mot_de_passe" name="mot_de_passe" type="password" autocomplete="current-password" required></label>'
            . '<button class="btn btn-principal btn-large" type="submit">Continuer</button></form>'
            . '<p class="petit discret">Mot de passe oublié : demandez à un associé de réinitialiser votre accès (Paramètres, Utilisateurs).</p>';
    }
    return Vue::document('Connexion', '<main class="page-seule" id="contenu"><div class="carte-connexion"><img class="logo-connexion" src="' . $e(Vue::$base) . 'assets/logo.png" alt="Andy Construct" width="132" height="34">' . $form . '</div></main>', 'seul');
};
