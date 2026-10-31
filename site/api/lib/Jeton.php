<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Jetons signés des liens « en un clic » (WF02) et de désinscription (WF12),
 * vérifiés par n8n avec le même secret (AC_ACTION_SECRET).
 *
 * Format : base64url(JSON) . "." . base64url(HMAC-SHA256(secret, base64url(JSON)))
 * JSON : {"a": action, "r": référence, "e": e-mail (désinscription), "x": expiration, "n": aléa}
 */
final class Jeton
{
    public function __construct(private string $secret)
    {
    }

    /** @param array<string, string|int> $donnees */
    public function creer(array $donnees, int $validiteSecondes, ?int $maintenant = null): string
    {
        $donnees['x'] = ($maintenant ?? time()) + $validiteSecondes;
        $donnees['n'] = bin2hex(random_bytes(4));
        $charge = self::b64(json_encode($donnees, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
        return $charge . '.' . self::b64(hash_hmac('sha256', $charge, $this->secret, true));
    }

    /** @return array<string, mixed>|null données si la signature est valable et non expirée */
    public function verifier(string $jeton, ?int $maintenant = null): ?array
    {
        $parties = explode('.', $jeton);
        if (count($parties) !== 2) {
            return null;
        }
        [$charge, $signature] = $parties;
        $attendue = self::b64(hash_hmac('sha256', $charge, $this->secret, true));
        if (!hash_equals($attendue, $signature)) {
            return null;
        }
        $donnees = json_decode((string) base64_decode(strtr($charge, '-_', '+/'), true), true);
        if (!is_array($donnees) || (int) ($donnees['x'] ?? 0) < ($maintenant ?? time())) {
            return null;
        }
        return $donnees;
    }

    public static function b64(string $binaire): string
    {
        return rtrim(strtr(base64_encode($binaire), '+/', '-_'), '=');
    }
}
