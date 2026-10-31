<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Liens de téléchargement signés et datés vers fichier.php : utilisés dans
 * l'e-mail interne (quand les pièces sont trop lourdes pour être jointes) et
 * par n8n pour joindre les fichiers à l'affaire dans le CRM.
 */
final class LiensFichiers
{
    public const MOTIF_ID = '/^[a-f0-9]{32}\.(jpg|png|heic|pdf)$/';

    public function __construct(private string $urlApi, private string $secret)
    {
    }

    public function url(string $id, int $validiteHeures, ?int $maintenant = null): string
    {
        $exp = ($maintenant ?? time()) + $validiteHeures * 3600;
        return rtrim($this->urlApi, '/') . '/fichier.php?' . http_build_query([
            'id' => $id,
            'exp' => $exp,
            'sig' => $this->signer($id, $exp),
        ]);
    }

    public function verifier(string $id, string $exp, string $sig, ?int $maintenant = null): bool
    {
        if (!preg_match(self::MOTIF_ID, $id) || !ctype_digit($exp) || !preg_match('/^[a-f0-9]{64}$/', $sig)) {
            return false;
        }
        if ((int) $exp < ($maintenant ?? time())) {
            return false;
        }
        return hash_equals($this->signer($id, (int) $exp), $sig);
    }

    private function signer(string $id, int $exp): string
    {
        return hash_hmac('sha256', "fichier|$id|$exp", $this->secret);
    }
}
