<?php
/**
 * Crée un compte de l'admin (le premier compte, puis au besoin) en ligne de commande.
 *
 *   php site/admin/outils/creer-utilisateur.php --email=prenom@andyconstruct.ch --nom="Prénom Nom" \
 *       --role=associe --role-metier=terrain
 *
 * Le mot de passe est demandé sans écho (ou lu sur l'entrée standard avec --mot-de-passe-stdin).
 * La commande affiche une seule fois la clé de double authentification (TOTP) et les
 * 10 codes de secours : à saisir dans l'application d'authentification du téléphone.
 * Configuration : celle de l'API (site/api/config.php, ou la variable AC_API_CONFIG).
 */
declare(strict_types=1);

if (PHP_SAPI !== 'cli') {
    http_response_code(404);
    exit;
}
require dirname(__DIR__) . '/lib/bootstrap.php';
ini_set('display_errors', '1');

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Auth;
use AndyConstruct\Admin\Totp;

$o = getopt('', ['email:', 'nom:', 'role:', 'role-metier:', 'mot-de-passe-stdin', 'aide']);
if (isset($o['aide']) || !isset($o['email'], $o['nom'])) {
    fwrite(STDERR, "Usage : php creer-utilisateur.php --email=… --nom=\"…\" [--role=associe|secretariat|agence_marketing|agence_technique] [--role-metier=bureau|terrain] [--mot-de-passe-stdin]\n");
    exit(isset($o['aide']) ? 0 : 2);
}
$role = (string) ($o['role'] ?? 'associe');
$roleMetier = isset($o['role-metier']) ? (string) $o['role-metier'] : null;

if (isset($o['mot-de-passe-stdin'])) {
    $mdp = rtrim((string) fgets(STDIN), "\r\n");
} else {
    $lire = static function (string $invite): string {
        fwrite(STDOUT, $invite);
        $tty = stream_isatty(STDIN);
        if ($tty) {
            shell_exec('stty -echo');
        }
        $v = rtrim((string) fgets(STDIN), "\r\n");
        if ($tty) {
            shell_exec('stty echo');
        }
        fwrite(STDOUT, "\n");
        return $v;
    };
    $mdp = $lire('Mot de passe (12 caractères au moins) : ');
    if ($lire('Encore une fois : ') !== $mdp) {
        fwrite(STDERR, "Les deux saisies diffèrent.\n");
        exit(1);
    }
}

try {
    $app = App::demarrer();
    $r = $app->auth->creerUtilisateur((string) $o['email'], (string) $o['nom'], $role, $roleMetier, $mdp);
} catch (\DomainException $e) {
    fwrite(STDERR, 'Refusé : ' . $e->getMessage() . "\n");
    exit(1);
} catch (\Throwable $e) {
    fwrite(STDERR, 'Erreur : ' . $e->getMessage() . "\n");
    exit(1);
}

$email = strtolower((string) $o['email']);
echo "\nCompte créé (n° {$r['id']}, " . Auth::ROLES[$role] . ($roleMetier ? ", $roleMetier" : '') . ").\n\n";
echo "Double authentification : dans l'application du téléphone, « ajouter un compte », clé manuelle :\n\n";
echo '    ' . trim(chunk_split($r['secret'], 4, ' ')) . "\n\n";
echo "ou cette adresse (à transformer en code QR, par exemple : qrencode -t ansiutf8 '<adresse>') :\n\n";
echo '    ' . Totp::uri($r['secret'], $email) . "\n\n";
echo "Codes de secours (un seul usage chacun ; à garder hors du téléphone) :\n\n";
foreach (array_chunk($r['codes'], 5) as $ligne) {
    echo '    ' . implode('   ', $ligne) . "\n";
}
echo "\nCes informations ne seront plus affichées. Connexion : <adresse du site>/admin/\n";
