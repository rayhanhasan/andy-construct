<?php
declare(strict_types=1);

namespace AndyConstruct\Admin;

/**
 * Mots de passe à usage unique basés sur le temps (TOTP, RFC 6238, sur HOTP RFC 4226),
 * sans dépendance externe. Compatible avec les applications d'authentification
 * (SHA-1, 6 chiffres, pas de 30 secondes). Secrets en Base32 (RFC 4648).
 */
final class Totp
{
    private const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';

    public static function nouveauSecret(int $octets = 20): string
    {
        return self::base32Encoder(random_bytes($octets));
    }

    /** Code à l'instant $t (secondes Unix). $cle : octets bruts. */
    public static function code(string $cle, int $t, int $chiffres = 6, int $pas = 30, string $algo = 'sha1'): string
    {
        return self::hotp($cle, intdiv($t, $pas), $chiffres, $algo);
    }

    public static function hotp(string $cle, int $compteur, int $chiffres = 6, string $algo = 'sha1'): string
    {
        $message = pack('N2', ($compteur >> 32) & 0xFFFFFFFF, $compteur & 0xFFFFFFFF);
        $hash = hash_hmac($algo, $message, $cle, true);
        $decalage = ord($hash[strlen($hash) - 1]) & 0x0F;
        $binaire = ((ord($hash[$decalage]) & 0x7F) << 24)
            | ((ord($hash[$decalage + 1]) & 0xFF) << 16)
            | ((ord($hash[$decalage + 2]) & 0xFF) << 8)
            | (ord($hash[$decalage + 3]) & 0xFF);
        return str_pad((string) ($binaire % (10 ** $chiffres)), $chiffres, '0', STR_PAD_LEFT);
    }

    /**
     * Vérifie un code saisi (fenêtre de ±1 pas pour la dérive d'horloge).
     * Refuse un pas déjà utilisé (rejeu) : retourne le pas accepté, ou null.
     */
    public static function verifier(string $secretBase32, string $saisie, int $t, int $dernierPasUtilise = 0, int $fenetre = 1): ?int
    {
        $saisie = preg_replace('/\s+/', '', $saisie) ?? '';
        if (!preg_match('/^\d{6}$/', $saisie)) {
            return null;
        }
        $cle = self::base32Decoder($secretBase32);
        if ($cle === '') {
            return null;
        }
        $pasCourant = intdiv($t, 30);
        $trouve = null;
        for ($i = -$fenetre; $i <= $fenetre; $i++) {
            $pas = $pasCourant + $i;
            if (hash_equals(self::hotp($cle, $pas), $saisie) && $pas > $dernierPasUtilise) {
                $trouve = $pas;
            }
        }
        return $trouve;
    }

    /** URI otpauth:// à saisir (ou à scanner) dans l'application d'authentification. */
    public static function uri(string $secretBase32, string $compte, string $emetteur = 'Andy Construct'): string
    {
        return 'otpauth://totp/' . rawurlencode($emetteur . ':' . $compte)
            . '?secret=' . $secretBase32 . '&issuer=' . rawurlencode($emetteur) . '&algorithm=SHA1&digits=6&period=30';
    }

    public static function base32Encoder(string $octets): string
    {
        $bits = '';
        foreach (str_split($octets) as $c) {
            $bits .= str_pad(decbin(ord($c)), 8, '0', STR_PAD_LEFT);
        }
        $sortie = '';
        foreach (str_split($bits, 5) as $bloc) {
            $sortie .= self::ALPHABET[bindec(str_pad($bloc, 5, '0'))];
        }
        return $octets === '' ? '' : $sortie;
    }

    public static function base32Decoder(string $texte): string
    {
        $texte = strtoupper(preg_replace('/[\s=-]/', '', $texte) ?? '');
        $bits = '';
        foreach (str_split($texte) as $c) {
            $v = strpos(self::ALPHABET, $c);
            if ($v === false) {
                return '';
            }
            $bits .= str_pad(decbin($v), 5, '0', STR_PAD_LEFT);
        }
        $octets = '';
        foreach (str_split($bits, 8) as $bloc) {
            if (strlen($bloc) === 8) {
                $octets .= chr(bindec($bloc));
            }
        }
        return $octets;
    }

    /** Secret chiffré pour la base (libsodium secretbox, clé dérivée du secret « admin »). */
    public static function chiffrer(string $secret, string $cleMaitre): string
    {
        $nonce = random_bytes(SODIUM_CRYPTO_SECRETBOX_NONCEBYTES);
        return 'v1.' . base64_encode($nonce . sodium_crypto_secretbox($secret, $nonce, self::cle($cleMaitre)));
    }

    public static function dechiffrer(string $chiffre, string $cleMaitre): ?string
    {
        if (!str_starts_with($chiffre, 'v1.')) {
            return null;
        }
        $brut = base64_decode(substr($chiffre, 3), true);
        if ($brut === false || strlen($brut) <= SODIUM_CRYPTO_SECRETBOX_NONCEBYTES) {
            return null;
        }
        $clair = sodium_crypto_secretbox_open(substr($brut, SODIUM_CRYPTO_SECRETBOX_NONCEBYTES), substr($brut, 0, SODIUM_CRYPTO_SECRETBOX_NONCEBYTES), self::cle($cleMaitre));
        return $clair === false ? null : $clair;
    }

    private static function cle(string $cleMaitre): string
    {
        return hash_hmac('sha256', 'andy-construct|admin|totp', $cleMaitre, true);
    }
}
