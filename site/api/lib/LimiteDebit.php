<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Limitation de débit par adresse IP, sans conserver l'adresse en clair :
 * l'IP est hachée avec un sel secret (HMAC-SHA256), les horodatages des
 * derniers envois sont gardés 24 h au plus dans stockage/limites/.
 */
final class LimiteDebit
{
    public function __construct(private Stockage $stockage, private string $sel)
    {
    }

    public function empreinte(string $ip): string
    {
        return substr(hash_hmac('sha256', 'ip|' . $ip, $this->sel), 0, 32);
    }

    /**
     * Enregistre une tentative et indique si la limite est dépassée.
     *
     * @return array{autorise: bool, restant: int, reessayer_dans: int}
     */
    public function tenter(string $ip, string $seau, int $maxParHeure, ?int $maintenant = null): array
    {
        $maintenant ??= time();
        $seau = preg_replace('/[^a-z0-9-]/', '', $seau) ?: 'defaut';
        $fichier = $this->stockage->dossier('limites') . '/' . $this->empreinte($ip) . '-' . $seau . '.json';
        $h = fopen($fichier, 'c+');
        if ($h === false) {
            return ['autorise' => true, 'restant' => $maxParHeure, 'reessayer_dans' => 0];
        }
        try {
            flock($h, LOCK_EX);
            $contenu = stream_get_contents($h) ?: '[]';
            $horodatages = json_decode($contenu, true);
            $horodatages = is_array($horodatages) ? $horodatages : [];
            $horodatages = array_values(array_filter($horodatages, static fn ($t) => is_int($t) && $t > $maintenant - 3600));
            if (count($horodatages) >= $maxParHeure) {
                $reessayer = max(60, min($horodatages) + 3600 - $maintenant);
                return ['autorise' => false, 'restant' => 0, 'reessayer_dans' => $reessayer];
            }
            $horodatages[] = $maintenant;
            ftruncate($h, 0);
            rewind($h);
            fwrite($h, json_encode($horodatages));
            fflush($h);
            return ['autorise' => true, 'restant' => $maxParHeure - count($horodatages), 'reessayer_dans' => 0];
        } finally {
            flock($h, LOCK_UN);
            fclose($h);
            @chmod($fichier, 0640);
        }
    }

    /** Adresse IP du client (en-têtes de proxy seulement si configuré). */
    public static function ipClient(array $server, bool $faireConfianceAuProxy): string
    {
        if ($faireConfianceAuProxy) {
            foreach (['HTTP_CF_CONNECTING_IP', 'HTTP_X_FORWARDED_FOR', 'HTTP_X_REAL_IP'] as $entete) {
                if (!empty($server[$entete])) {
                    $ip = trim(explode(',', (string) $server[$entete])[0]);
                    if (filter_var($ip, FILTER_VALIDATE_IP)) {
                        return $ip;
                    }
                }
            }
        }
        return (string) ($server['REMOTE_ADDR'] ?? '0.0.0.0');
    }
}
