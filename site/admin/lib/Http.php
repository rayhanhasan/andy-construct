<?php
declare(strict_types=1);

namespace AndyConstruct\Admin;

/** Réponses HTTP de l'admin : en-têtes de sécurité, redirections, refus. */
final class Http
{
    /** En-têtes de toute réponse de l'admin (§6.5 « Protections web »). */
    public static function entetesSecurite(): void
    {
        if (headers_sent()) {
            return;
        }
        header_remove('X-Powered-By');
        header("Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'; object-src 'none'");
        header('X-Content-Type-Options: nosniff');
        header('X-Frame-Options: DENY');
        header('Referrer-Policy: no-referrer');
        header('Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()');
        header('Cross-Origin-Opener-Policy: same-origin');
        header('Cross-Origin-Resource-Policy: same-origin');
        header('X-Robots-Tag: noindex, nofollow');
        header('Cache-Control: no-store, max-age=0');
        if (($_SERVER['HTTPS'] ?? '') === 'on' || ($_SERVER['SERVER_PORT'] ?? '') === '443') {
            header('Strict-Transport-Security: max-age=31536000');
        }
    }

    public static function rediriger(string $url): never
    {
        if (!str_starts_with($url, '/') || str_starts_with($url, '//')) {
            $url = Vue::$base; // jamais vers un autre site
        }
        header('Location: ' . $url, true, 303);
        exit;
    }

    public static function refuser(int $code, string $titre, string $texte): never
    {
        http_response_code($code);
        header('Content-Type: text/html; charset=utf-8');
        echo Vue::erreur($code, $titre, $texte);
        exit;
    }

    public static function json(array $donnees, int $code = 200): never
    {
        http_response_code($code);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($donnees, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        exit;
    }

    public static function post(string $cle, string $defaut = ''): string
    {
        $v = $_POST[$cle] ?? $defaut;
        return is_string($v) ? $v : $defaut;
    }

    public static function get(string $cle, string $defaut = ''): string
    {
        $v = $_GET[$cle] ?? $defaut;
        return is_string($v) ? $v : $defaut;
    }
}
