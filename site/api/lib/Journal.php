<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Journal minimal, une ligne JSON par événement, un fichier par jour.
 *
 * Règle : aucune donnée personnelle en clair (ni nom, ni e-mail, ni téléphone,
 * ni message, ni adresse IP). On n'y écrit que la référence de la demande,
 * l'issue, des compteurs et un fragment de l'empreinte de l'IP.
 */
final class Journal
{
    private const CLES_INTERDITES = ['nom', 'prenom', 'email', 'telephone', 'message', 'ip', 'adresse', 'commune'];

    public function __construct(private Stockage $stockage)
    {
    }

    /** @param array<string, scalar|null|array<scalar|null>> $details */
    public function ecrire(string $niveau, string $evenement, array $details = []): void
    {
        foreach (self::CLES_INTERDITES as $cle) {
            unset($details[$cle]);
        }
        $ligne = ['t' => date('c'), 'niveau' => $niveau, 'evenement' => $evenement] + $details;
        $json = json_encode($ligne, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_INVALID_UTF8_SUBSTITUTE);
        try {
            $fichier = $this->stockage->dossier('journaux') . '/' . date('Y-m-d') . '.log';
            @file_put_contents($fichier, $json . "\n", FILE_APPEND | LOCK_EX);
            @chmod($fichier, 0640);
        } catch (\Throwable) {
            error_log('[andy-construct] ' . $json);
        }
    }

    public function info(string $evenement, array $details = []): void
    {
        $this->ecrire('info', $evenement, $details);
    }

    public function alerte(string $evenement, array $details = []): void
    {
        $this->ecrire('alerte', $evenement, $details);
    }

    public function erreur(string $evenement, array $details = []): void
    {
        $this->ecrire('erreur', $evenement, $details);
    }

    /** Message d'exception sans données personnelles probables (adresses, numéros). */
    public static function nettoyerMessage(string $message): string
    {
        $message = preg_replace('/[^\s@<>]+@[^\s@<>]+/', '[e-mail]', $message) ?? '';
        $message = preg_replace('/\+?\d[\d \/.\-]{7,}\d/', '[numéro]', $message) ?? '';
        return mb_substr($message, 0, 300);
    }
}
