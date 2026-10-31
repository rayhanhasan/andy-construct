<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Limitation de débit par adresse IP, sans conserver l'adresse en clair :
 * l'IP est hachée avec un sel secret (HMAC-SHA256), les horodatages des
 * derniers envois sont gardés 24 h au plus dans stockage/limites/.
 *
 * IPv6 : un abonné reçoit en général un préfixe /64 entier ; la limite porte
 * donc sur le /64 (sinon il suffirait de changer d'adresse à chaque envoi).
 */
final class LimiteDebit
{
    public function __construct(private Stockage $stockage, private string $sel)
    {
    }

    public function empreinte(string $ip): string
    {
        return substr(hash_hmac('sha256', 'ip|' . self::cle($ip), $this->sel), 0, 32);
    }

    /**
     * Clé de limitation d'une adresse : IPv4 telle quelle, IPv6 réduite à son
     * préfixe /64, IPv4 encapsulée (::ffff:a.b.c.d) ramenée à l'IPv4. Toute autre
     * valeur (clé applicative, « email|… ») est conservée telle quelle.
     */
    public static function cle(string $ip): string
    {
        $binaire = filter_var($ip, FILTER_VALIDATE_IP) ? @inet_pton($ip) : false;
        if ($binaire === false || strlen($binaire) !== 16) {
            return $ip;
        }
        if (str_starts_with($binaire, str_repeat("\0", 10) . "\xff\xff")) {
            return (string) inet_ntop(substr($binaire, 12));
        }
        return (string) inet_ntop(substr($binaire, 0, 8) . str_repeat("\0", 8)) . '/64';
    }

    /**
     * Enregistre une tentative et indique si la limite est dépassée.
     *
     * @param int $fenetre durée de la fenêtre glissante en secondes (1 h par défaut, 24 h au plus)
     * @return array{autorise: bool, restant: int, reessayer_dans: int}
     */
    public function tenter(string $ip, string $seau, int $max, ?int $maintenant = null, int $fenetre = 3600): array
    {
        $maintenant ??= time();
        $fenetre = max(60, min(86400, $fenetre));
        $seau = preg_replace('/[^a-z0-9-]/', '', $seau) ?: 'defaut';
        $fichier = $this->stockage->dossier('limites') . '/' . $this->empreinte($ip) . '-' . $seau . '.json';
        $h = fopen($fichier, 'c+');
        if ($h === false) {
            return ['autorise' => true, 'restant' => $max, 'reessayer_dans' => 0];
        }
        try {
            flock($h, LOCK_EX);
            $contenu = stream_get_contents($h) ?: '[]';
            $horodatages = json_decode($contenu, true);
            $horodatages = is_array($horodatages) ? $horodatages : [];
            $horodatages = array_values(array_filter($horodatages, static fn ($t) => is_int($t) && $t > $maintenant - $fenetre));
            if (count($horodatages) >= $max) {
                $reessayer = max(60, min($horodatages) + $fenetre - $maintenant);
                return ['autorise' => false, 'restant' => 0, 'reessayer_dans' => $reessayer];
            }
            $horodatages[] = $maintenant;
            ftruncate($h, 0);
            rewind($h);
            fwrite($h, json_encode($horodatages));
            fflush($h);
            return ['autorise' => true, 'restant' => $max - count($horodatages), 'reessayer_dans' => 0];
        } finally {
            flock($h, LOCK_UN);
            fclose($h);
            @chmod($fichier, 0640);
        }
    }

    /**
     * Adresse IP du client.
     *
     * Les en-têtes de proxy (CF-Connecting-IP, X-Forwarded-For, X-Real-IP) sont
     * fabriqués par le client : ils ne sont lus que si $faireConfianceAuProxy est
     * vrai ET, quand $proxysDeConfiance est renseigné, si la connexion vient
     * réellement de l'un de ces proxys (sinon une requête envoyée directement au
     * serveur choisirait son IP et contournerait la limite de débit).
     * X-Forwarded-For est lu de droite à gauche : la première adresse qui n'est
     * pas un proxy de confiance est celle du client (l'entrée la plus à gauche
     * est celle que le client a écrite lui-même).
     *
     * @param list<string> $proxysDeConfiance adresses ou plages CIDR (IPv4/IPv6)
     */
    public static function ipClient(array $server, bool $faireConfianceAuProxy, array $proxysDeConfiance = []): string
    {
        $distante = (string) ($server['REMOTE_ADDR'] ?? '0.0.0.0');
        if (!$faireConfianceAuProxy) {
            return $distante;
        }
        if ($proxysDeConfiance !== [] && !self::dansPlages($distante, $proxysDeConfiance)) {
            return $distante;
        }
        $cf = trim((string) ($server['HTTP_CF_CONNECTING_IP'] ?? ''));
        if ($cf !== '' && filter_var($cf, FILTER_VALIDATE_IP)) {
            return $cf;
        }
        $xff = (string) ($server['HTTP_X_FORWARDED_FOR'] ?? '');
        if ($xff !== '') {
            $chaine = array_reverse(array_map('trim', explode(',', $xff)));
            foreach ($chaine as $ip) {
                if (!filter_var($ip, FILTER_VALIDATE_IP)) {
                    break; // valeur forgée ou illisible : on s'arrête là
                }
                if ($proxysDeConfiance === [] || !self::dansPlages($ip, $proxysDeConfiance)) {
                    return $ip;
                }
            }
        }
        $reelle = trim((string) ($server['HTTP_X_REAL_IP'] ?? ''));
        if ($reelle !== '' && filter_var($reelle, FILTER_VALIDATE_IP)) {
            return $reelle;
        }
        return $distante;
    }

    /** @param list<string> $plages adresses ou plages CIDR */
    public static function dansPlages(string $ip, array $plages): bool
    {
        $binaire = filter_var($ip, FILTER_VALIDATE_IP) ? @inet_pton($ip) : false;
        if ($binaire === false) {
            return false;
        }
        foreach ($plages as $plage) {
            [$reseau, $bits] = array_pad(explode('/', (string) $plage, 2), 2, null);
            $reseauBin = filter_var($reseau, FILTER_VALIDATE_IP) ? @inet_pton((string) $reseau) : false;
            if ($reseauBin === false || strlen($reseauBin) !== strlen($binaire)) {
                continue;
            }
            $bits = $bits === null ? strlen($binaire) * 8 : (int) $bits;
            $octets = intdiv($bits, 8);
            $reste = $bits % 8;
            if (substr($binaire, 0, $octets) !== substr($reseauBin, 0, $octets)) {
                continue;
            }
            if ($reste === 0) {
                return true;
            }
            $masque = (0xFF << (8 - $reste)) & 0xFF;
            if ((ord($binaire[$octets]) & $masque) === (ord($reseauBin[$octets]) & $masque)) {
                return true;
            }
        }
        return false;
    }
}
