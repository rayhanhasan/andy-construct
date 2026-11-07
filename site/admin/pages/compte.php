<?php
/** E14 · Mon compte : mot de passe, double authentification, dernières connexions. */
declare(strict_types=1);

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Auth;
use AndyConstruct\Admin\Format;
use AndyConstruct\Admin\Http;
use AndyConstruct\Admin\Vue;

return static function (App $app): string {
    $e = static fn ($v) => Vue::e($v);
    $u = $app->utilisateur;
    $message = '';
    if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
        try {
            if (Http::post('nouveau') !== Http::post('confirmation')) {
                throw new \DomainException('Les deux saisies du nouveau mot de passe ne sont pas identiques.');
            }
            $app->auth->changerMotDePasse($u['id'], Http::post('actuel'), Http::post('nouveau'));
            Vue::flash('Mot de passe changé.');
            Http::rediriger(Vue::url('compte'));
        } catch (\DomainException $ex) {
            $message = '<p class="erreur-formulaire" role="alert">' . $e($ex->getMessage()) . '</p>';
        }
    }
    $codes = count(json_decode((string) ($u['codes_secours'] ?? '[]'), true) ?: []);
    $connexions = $app->base->tous("SELECT quand, action, ip_tronquee FROM journal_audit WHERE objet_type = 'utilisateur' AND objet_id = ? AND action IN ('connexion', 'connexion_echec', 'compte_bloque') ORDER BY id DESC LIMIT 10", [(string) $u['id']]);
    $lignes = '';
    foreach ($connexions as $c) {
        $lignes .= '<li><time>' . $e(Format::dateH(Format::t($c['quand']))) . '</time><div>' . $e(['connexion' => 'Connexion', 'connexion_echec' => 'Échec de connexion', 'compte_bloque' => 'Compte bloqué 15 minutes'][$c['action']] ?? $c['action']) . '<div class="auteur">' . $e($c['ip_tronquee'] ?? '') . '</div></div></li>';
    }
    $html = '<div class="entete-page"><div><h1>Mon compte</h1><p class="sous-titre">' . $e($u['nom_affiche'] . ' · ' . $u['email'] . ' · ' . (Auth::ROLES[$u['role']] ?? '')) . '</p></div></div>' . $message
        . '<div class="grille-2"><section class="panneau" aria-labelledby="t-mdp"><h2 id="t-mdp">Changer le mot de passe</h2><form method="post" action="' . $e(Vue::url('compte')) . '" class="formulaire">' . Vue::csrf($app)
        . '<input type="text" name="identifiant" autocomplete="username" value="' . $e($u['email']) . '" hidden>'
        . '<label class="champ" for="c-actuel"><span>Mot de passe actuel</span><input id="c-actuel" name="actuel" type="password" autocomplete="current-password" required></label>'
        . '<label class="champ" for="c-nouveau"><span>Nouveau mot de passe <span class="aide-champ">12 caractères au moins ; une phrase de plusieurs mots est idéale</span></span><input id="c-nouveau" name="nouveau" type="password" autocomplete="new-password" required minlength="12"></label>'
        . '<label class="champ" for="c-conf"><span>Nouveau mot de passe, encore</span><input id="c-conf" name="confirmation" type="password" autocomplete="new-password" required minlength="12"></label>'
        . '<div><button class="btn btn-sombre" type="submit">Changer le mot de passe</button></div></form></section>'
        . '<section class="panneau" aria-labelledby="t-2fa"><h2 id="t-2fa">Double authentification</h2><p>Active (application d\'authentification). Codes de secours restants : <b>' . $codes . '</b> sur 10.</p>'
        . '<p class="petit discret">Téléphone perdu ou changé : un associé réinitialise la double authentification dans Paramètres, Utilisateurs.</p>'
        . '<h3 class="mt">Dernières connexions</h3>' . ($lignes ? '<ol class="historique">' . $lignes . '</ol>' : '<p class="petit discret">Aucune.</p>')
        . '<form method="post" action="' . $e(Vue::url('deconnexion')) . '" class="mt">' . Vue::csrf($app) . '<button class="btn" type="submit">Se déconnecter</button></form></section></div>';
    return Vue::page($app, 'compte', 'Mon compte', $html);
};
