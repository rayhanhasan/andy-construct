<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Transmission des demandes à n8n par webhook signé (HMAC-SHA256), avec file
 * d'attente locale en cas d'échec.
 *
 * En-têtes envoyés :
 *   X-AC-Timestamp : horodatage Unix de l'envoi
 *   X-AC-Signature : sha256=<hex HMAC-SHA256(secret, horodatage + "." + corps)>
 *   X-AC-Ref       : référence de la demande
 * n8n refuse une signature invalide ou un horodatage décalé de plus de 5 minutes.
 *
 * Échec (réseau, délai de 5 s, code HTTP hors 2xx) : la charge est écrite dans
 * stockage/file-attente/ et renvoyée (signature et liens de fichiers refaits)
 * au prochain appel de demande.php ou par cron.php, avec un délai croissant.
 */
final class Webhook
{
    public function __construct(
        private Config $config,
        private Stockage $stockage,
        private Journal $journal,
        private LiensFichiers $liens
    ) {
    }

    public static function signer(string $secret, string $corps, int $horodatage): string
    {
        return 'sha256=' . hash_hmac('sha256', $horodatage . '.' . $corps, $secret);
    }

    public static function encoder(array $charge): string
    {
        return json_encode(
            $charge,
            JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_LINE_TERMINATORS | JSON_THROW_ON_ERROR
        );
    }

    private function url(string $type): string
    {
        return (string) $this->config->get($type === 'guide' ? 'n8n.url_guide' : 'n8n.url_demande', '');
    }

    /**
     * Envoie ou met en file. Retourne « livre », « en_file », « simule », « non_configure » ou « perdu ».
     */
    public function transmettre(string $type, array $charge, string $ref): string
    {
        $url = $this->url($type);
        if ($url === '' && !$this->config->get('n8n.simuler')) {
            $this->journal->info('webhook_non_configure', ['ref' => $ref]);
            return 'non_configure';
        }
        $resultat = $this->envoyer($type, $charge, $ref);
        if ($resultat['ok']) {
            return $resultat['simule'] ? 'simule' : 'livre';
        }
        $this->journal->alerte('webhook_echec', ['ref' => $ref, 'code' => $resultat['code'], 'erreur' => $resultat['erreur']]);
        return $this->mettreEnFile($type, $charge, $ref) ? 'en_file' : 'perdu';
    }

    /** @return array{ok: bool, code: int, erreur: string, simule: bool} */
    public function envoyer(string $type, array $charge, string $ref): array
    {
        // Liens de fichiers refaits à chaque envoi (ils expirent).
        if (!empty($charge['fichiers']) && is_array($charge['fichiers'])) {
            foreach ($charge['fichiers'] as $i => $f) {
                $charge['fichiers'][$i]['url'] = $this->liens->url((string) $f['id'], (int) $this->config->get('fichiers.lien_validite_h_n8n', 24));
            }
        }
        $charge['envoye_le'] = date('c');
        $corps = self::encoder($charge);
        $horodatage = time();
        $entetes = [
            'Content-Type: application/json; charset=utf-8',
            'X-AC-Timestamp: ' . $horodatage,
            'X-AC-Signature: ' . self::signer($this->config->secret('hmac_webhook'), $corps, $horodatage),
            'X-AC-Ref: ' . preg_replace('/[^A-Za-z0-9-]/', '', $ref),
            'User-Agent: AndyConstruct-Site/1.0',
        ];

        if ($this->config->get('n8n.simuler')) {
            $fichier = $this->stockage->dossier('test-webhooks') . '/' . date('Ymd-His') . '-' . $type . '-' . bin2hex(random_bytes(3)) . '.json';
            $this->stockage->ecrireAtomique($fichier, implode("\n", $entetes) . "\n\n" . $corps);
            return ['ok' => true, 'code' => 200, 'erreur' => '', 'simule' => true];
        }

        $url = $this->url($type);
        if (!preg_match('~^https?://~', $url)) {
            return ['ok' => false, 'code' => 0, 'erreur' => 'url_invalide', 'simule' => false];
        }
        $delai = max(1, (int) $this->config->get('n8n.delai', 5));
        [$code, $erreur] = function_exists('curl_init')
            ? self::posterCurl($url, $corps, $entetes, $delai)
            : self::posterFlux($url, $corps, $entetes, $delai);
        return ['ok' => $code >= 200 && $code < 300, 'code' => $code, 'erreur' => $erreur, 'simule' => false];
    }

    /** @return array{0: int, 1: string} */
    private static function posterCurl(string $url, string $corps, array $entetes, int $delai): array
    {
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => $corps,
            CURLOPT_HTTPHEADER => $entetes,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_CONNECTTIMEOUT => min(3, $delai),
            CURLOPT_TIMEOUT => $delai,
            CURLOPT_FOLLOWLOCATION => false,
            CURLOPT_SSL_VERIFYPEER => true,
            CURLOPT_SSL_VERIFYHOST => 2,
            CURLOPT_PROTOCOLS => CURLPROTO_HTTP | CURLPROTO_HTTPS,
        ]);
        curl_exec($ch);
        $code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        $erreur = curl_errno($ch) ? 'curl_' . curl_errno($ch) : ($code >= 300 ? "http_$code" : '');
        curl_close($ch);
        return [$code, $erreur];
    }

    /** @return array{0: int, 1: string} */
    private static function posterFlux(string $url, string $corps, array $entetes, int $delai): array
    {
        $contexte = stream_context_create(['http' => [
            'method' => 'POST',
            'header' => implode("\r\n", $entetes),
            'content' => $corps,
            'timeout' => $delai,
            'ignore_errors' => true,
            'follow_location' => 0,
        ]]);
        $reponse = @file_get_contents($url, false, $contexte);
        $code = 0;
        foreach ($http_response_header ?? [] as $ligne) {
            if (preg_match('~^HTTP/\S+\s+(\d{3})~', $ligne, $m)) {
                $code = (int) $m[1];
            }
        }
        return [$code, $reponse === false && $code === 0 ? 'flux_echec' : ($code >= 300 ? "http_$code" : '')];
    }

    private function mettreEnFile(string $type, array $charge, string $ref): bool
    {
        try {
            $element = [
                'type' => $type,
                'ref' => $ref,
                'cree' => time(),
                'tentatives' => 1,
                'prochain_essai' => time() + 60,
                'alerte_envoyee' => false,
                'charge' => $charge,
            ];
            $fichier = $this->stockage->dossier('file-attente') . '/' . preg_replace('/[^A-Za-z0-9-]/', '', $ref) . '-' . bin2hex(random_bytes(3)) . '.json';
            $this->stockage->ecrireAtomique($fichier, self::encoder($element));
            @chmod($fichier, 0600);
            return true;
        } catch (\Throwable $e) {
            $this->journal->erreur('file_attente_ecriture', ['ref' => $ref]);
            return false;
        }
    }

    /**
     * Relance les éléments dus de la file d'attente.
     *
     * @return array{livres: int, echecs: int, restants: int, plus_ancien_minutes: int, a_signaler: list<string>}
     */
    public function traiterFile(int $max = 50, bool $forcer = false): array
    {
        $bilan = ['livres' => 0, 'echecs' => 0, 'restants' => 0, 'plus_ancien_minutes' => 0, 'a_signaler' => []];
        $resultat = $this->stockage->sousVerrou('file-attente', function () use ($max, $forcer, &$bilan): bool {
            $fichiers = glob($this->stockage->dossier('file-attente') . '/*.json') ?: [];
            sort($fichiers);
            $traites = 0;
            $seuilAlerte = (int) $this->config->get('conservation.file_attente_alerte_minutes', 60) * 60;
            $abandon = (int) $this->config->get('conservation.file_attente_abandon_jours', 14) * 86400;
            foreach ($fichiers as $fichier) {
                $element = json_decode((string) file_get_contents($fichier), true);
                if (!is_array($element) || !isset($element['charge'], $element['ref'])) {
                    @unlink($fichier);
                    continue;
                }
                $age = time() - (int) $element['cree'];
                if ($age > $abandon) {
                    $this->journal->erreur('file_attente_abandon', ['ref' => $element['ref'], 'tentatives' => $element['tentatives']]);
                    $bilan['a_signaler'][] = $element['ref'] . ' (abandonnée après ' . intdiv($age, 86400) . ' jours)';
                    @unlink($fichier);
                    continue;
                }
                $du = $forcer || (int) $element['prochain_essai'] <= time();
                if ($du && $traites < $max) {
                    $traites++;
                    $r = $this->envoyer((string) $element['type'], (array) $element['charge'], (string) $element['ref']);
                    if ($r['ok']) {
                        @unlink($fichier);
                        $bilan['livres']++;
                        $this->journal->info('file_attente_livree', ['ref' => $element['ref'], 'tentatives' => $element['tentatives']]);
                        continue;
                    }
                    $bilan['echecs']++;
                    $element['tentatives'] = (int) $element['tentatives'] + 1;
                    $element['prochain_essai'] = time() + min(3600, 60 * (2 ** min(6, $element['tentatives'])));
                }
                if ($age >= $seuilAlerte && empty($element['alerte_envoyee'])) {
                    $bilan['a_signaler'][] = $element['ref'] . ' (en attente depuis ' . intdiv($age, 60) . ' min)';
                    $element['alerte_envoyee'] = true;
                }
                $this->stockage->ecrireAtomique($fichier, self::encoder($element));
                $bilan['restants']++;
                $bilan['plus_ancien_minutes'] = max($bilan['plus_ancien_minutes'], intdiv($age, 60));
            }
            return true;
        }, false);
        if ($resultat === null) {
            $bilan['restants'] = -1; // un autre processus traite déjà la file
        }
        return $bilan;
    }

    public function tailleFile(): int
    {
        return count(glob($this->stockage->dossier('file-attente') . '/*.json') ?: []);
    }
}
