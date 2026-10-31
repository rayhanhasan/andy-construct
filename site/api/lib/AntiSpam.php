<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Protections invisibles pour le visiteur (pas de CAPTCHA) :
 * - pot de miel : champ « site_web » caché, qui doit rester vide ;
 * - piège temporel : jeton horodaté et signé (« form_t0 »), délivré par
 *   GET demande.php?jeton ; un envoi trop rapide est refusé ;
 * - contenu : trop de liens, balises de forum ;
 * - origine : en-tête Origin limité au domaine du site.
 */
final class AntiSpam
{
    public function __construct(private Config $config)
    {
    }

    /** Jeton « v1.<horodatage>.<aléa>.<signature> ». */
    public function creerJeton(?int $maintenant = null): string
    {
        $ts = $maintenant ?? time();
        $alea = bin2hex(random_bytes(6));
        return "v1.$ts.$alea." . $this->signer("$ts.$alea");
    }

    /**
     * @return array{statut: string, delai: ?int}
     *   statut : ok | absent | invalide | expire | trop_rapide
     */
    public function verifierJeton(string $jeton, string $formulaire, ?int $maintenant = null): array
    {
        $maintenant ??= time();
        if ($jeton === '') {
            return ['statut' => 'absent', 'delai' => null];
        }
        if (!preg_match('/^v1\.(\d{10})\.([a-f0-9]{12})\.([a-f0-9]{32})$/', $jeton, $m)) {
            return ['statut' => 'invalide', 'delai' => null];
        }
        if (!hash_equals($this->signer("$m[1].$m[2]"), $m[3])) {
            return ['statut' => 'invalide', 'delai' => null];
        }
        $delai = $maintenant - (int) $m[1];
        $min = (int) $this->config->get("anti_spam.delai_min.$formulaire", 3);
        if ($delai < 0) {
            return ['statut' => 'invalide', 'delai' => $delai];
        }
        if ($delai < $min) {
            return ['statut' => 'trop_rapide', 'delai' => $delai];
        }
        if ($delai > (int) $this->config->get('anti_spam.jeton_validite_h', 12) * 3600) {
            return ['statut' => 'expire', 'delai' => $delai];
        }
        return ['statut' => 'ok', 'delai' => $delai];
    }

    public function potDeMielRempli(array $post): bool
    {
        $v = $post['site_web'] ?? '';
        return !is_string($v) || trim($v) !== '';
    }

    /** Raison du rejet si le contenu ressemble à du spam, sinon null. */
    public function contenuSuspect(array $donnees): ?string
    {
        $message = (string) ($donnees['message'] ?? '');
        $champsCourts = ($donnees['nom'] ?? '') . ' ' . ($donnees['prenom'] ?? '') . ' ' . ($donnees['commune'] ?? '');
        if (preg_match('~https?://|www\.~i', $champsCourts)) {
            return 'lien_dans_nom';
        }
        if (preg_match('~\[url[=\]]|\[link|<a\s+href~i', $message)) {
            return 'balises_forum';
        }
        $liens = preg_match_all('~https?://|www\.~i', $message);
        if ($liens > (int) $this->config->get('anti_spam.max_liens_message', 3)) {
            return 'trop_de_liens';
        }
        return null;
    }

    /** L'en-tête Origin, s'il est présent, doit correspondre au site. */
    public function origineAutorisee(array $server): bool
    {
        $origine = (string) ($server['HTTP_ORIGIN'] ?? '');
        if ($origine === '' || $origine === 'null') {
            return $origine === '';
        }
        $origine = rtrim(strtolower($origine), '/');
        $autorisees = array_map(static fn ($o) => rtrim(strtolower((string) $o), '/'), (array) $this->config->get('origines_autorisees', []));
        if ($autorisees === [] || in_array($origine, $autorisees, true)) {
            return true;
        }
        if ($this->config->modeTest() && preg_match('~^http://(localhost|127\.0\.0\.1)(:\d+)?$~', $origine)) {
            return true;
        }
        return false;
    }

    private function signer(string $donnees): string
    {
        return substr(hash_hmac('sha256', "form_t0|$donnees", $this->config->secret('local')), 0, 32);
    }
}
