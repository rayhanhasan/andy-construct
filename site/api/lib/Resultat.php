<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Réponse HTTP préparée par Traitement, émise par demande.php.
 * Trois formes : JSON (appel fetch), redirection 303 (formulaire classique
 * envoyé avec succès) ou page HTML d'erreur (formulaire classique sans JS).
 */
final class Resultat
{
    /** @param array<string, mixed> $corps @param array<string, string> $entetes */
    public function __construct(
        public int $statut,
        public string $forme,
        public array $corps = [],
        public string $redirection = '',
        public string $html = '',
        public array $entetes = []
    ) {
    }

    public function emettre(): void
    {
        http_response_code($this->statut);
        header('Cache-Control: no-store');
        header('X-Content-Type-Options: nosniff');
        header('Referrer-Policy: same-origin');
        header('X-Robots-Tag: noindex');
        foreach ($this->entetes as $nom => $valeur) {
            header($nom . ': ' . $valeur);
        }
        if ($this->forme === 'redirection') {
            header('Location: ' . $this->redirection);
            return;
        }
        if ($this->forme === 'html') {
            header('Content-Type: text/html; charset=utf-8');
            header("Content-Security-Policy: default-src 'none'; style-src 'unsafe-inline'; img-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'");
            echo $this->html;
            return;
        }
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($this->corps, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    }
}
