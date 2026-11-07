<?php
declare(strict_types=1);

namespace AndyConstruct\Admin;

use AndyConstruct\Api\Base;
use AndyConstruct\Api\Validateur;

/**
 * Comptes, connexion en deux étapes (mot de passe puis code TOTP ou code de
 * secours), sessions, jeton CSRF, limites d'essais et droits par rôle (§6.5).
 */
final class Auth
{
    public const ROLES = [
        'associe' => 'Associé',
        'secretariat' => 'Secrétariat',
        'agence_marketing' => 'Agence, marketing',
        'agence_technique' => 'Agence, technique',
    ];

    /** Droit => rôles autorisés (vérifié côté serveur sur chaque route). */
    public const DROITS = [
        'demandes' => ['associe', 'secretariat'],          // À traiter, Demandes, fiche, recherche, saisie, actions
        'vue' => ['associe', 'secretariat', 'agence_marketing'],
        'vue_noms' => ['associe', 'secretariat'],          // noms dans les alertes
        'acquisition' => ['associe', 'secretariat', 'agence_marketing'],
        'depenses' => ['associe', 'agence_marketing'],
        'export' => ['associe'],
        'effacer' => ['associe'],
        'parametres' => ['associe'],
        'utilisateurs' => ['associe'],
        'journal' => ['associe'],
        'compte' => ['associe', 'secretariat', 'agence_marketing', 'agence_technique'],
    ];

    private const ATTENTE_2FA_S = 300;

    public function __construct(private App $app)
    {
    }

    public static function peut(?array $utilisateur, string $droit): bool
    {
        return $utilisateur !== null && in_array($utilisateur['role'] ?? '', self::DROITS[$droit] ?? [], true);
    }

    // ----------------------------------------------------------------- session

    public function nomCookie(): string
    {
        return $this->cookieSecurise() ? '__Host-ac_admin' : 'ac_admin';
    }

    private function cookieSecurise(): bool
    {
        return (bool) $this->app->config->get('admin.cookie_securise', true);
    }

    public function demarrerSession(): void
    {
        if (session_status() === PHP_SESSION_ACTIVE) {
            return;
        }
        $inactivite = max(15, (int) $this->app->config->get('admin.session_inactivite_min', 480)) * 60;
        ini_set('session.use_strict_mode', '1');
        ini_set('session.use_only_cookies', '1');
        ini_set('session.use_trans_sid', '0');
        ini_set('session.cookie_httponly', '1');
        ini_set('session.gc_maxlifetime', (string) $inactivite);
        ini_set('session.cache_limiter', 'nocache');
        session_save_path($this->app->stockage->dossier('sessions'));
        session_name($this->nomCookie());
        session_set_cookie_params([
            'lifetime' => 0,
            'path' => '/',
            'secure' => $this->cookieSecurise(),
            'httponly' => true,
            'samesite' => 'Strict',
        ]);
        session_start();
        if (!isset($_SESSION['csrf'])) {
            $_SESSION['csrf'] = bin2hex(random_bytes(32));
        }
    }

    public function csrf(): string
    {
        if (!isset($_SESSION['csrf'])) {
            $_SESSION['csrf'] = bin2hex(random_bytes(32));
        }
        return (string) $_SESSION['csrf'];
    }

    /** Jeton du formulaire comparé à celui de la session ; requête intersite refusée. */
    public function verifierCsrf(mixed $jeton, array $server = []): bool
    {
        if (($server['HTTP_SEC_FETCH_SITE'] ?? '') === 'cross-site') {
            return false;
        }
        return is_string($jeton) && isset($_SESSION['csrf']) && hash_equals((string) $_SESSION['csrf'], $jeton);
    }

    /** Utilisateur connecté (deux étapes faites, session active, compte actif), sinon null. */
    public function utilisateur(): ?array
    {
        $uid = $_SESSION['uid'] ?? null;
        if (!is_int($uid)) {
            return null;
        }
        $inactivite = max(15, (int) $this->app->config->get('admin.session_inactivite_min', 480)) * 60;
        if ((int) ($_SESSION['activite'] ?? 0) < time() - $inactivite) {
            $this->vider();
            return null;
        }
        $u = $this->app->base->un('SELECT * FROM utilisateur WHERE id = ? AND actif = 1', [$uid]);
        if ($u === null || (int) ($_SESSION['auth_mdp'] ?? 0) !== crc32((string) $u['mdp_hash'])) {
            $this->vider(); // compte désactivé ou mot de passe changé ailleurs
            return null;
        }
        $_SESSION['activite'] = time();
        $u['id'] = (int) $u['id'];
        $this->app->utilisateur = $u;
        return $u;
    }

    private function vider(): void
    {
        $csrf = $_SESSION['csrf'] ?? null;
        $_SESSION = $csrf ? ['csrf' => $csrf] : [];
    }

    public function deconnecter(): void
    {
        if ($this->app->utilisateur !== null) {
            $this->app->audit('deconnexion', 'utilisateur', (string) $this->app->utilisateur['id']);
        }
        $_SESSION = [];
        if (session_status() === PHP_SESSION_ACTIVE) {
            session_regenerate_id(true);
            $_SESSION['csrf'] = bin2hex(random_bytes(32));
        }
    }

    // ------------------------------------------------------------- connexion

    /** @return array{ok: bool, message: string} */
    public function etapeMotDePasse(string $email, string $motDePasse): array
    {
        $refus = ['ok' => false, 'message' => 'Adresse e-mail ou mot de passe incorrect.'];
        if ($this->ipBloquee()) {
            $this->app->audit('connexion_limite_ip', null, null, [], 'systeme');
            return ['ok' => false, 'message' => 'Trop d\'essais depuis cette connexion. Réessayez dans 15 minutes.'];
        }
        $this->noterEssaiIp();
        $email = strtolower(trim($email));
        $u = $email === '' ? null : $this->app->base->un('SELECT * FROM utilisateur WHERE email = ?', [$email]);
        if ($u === null) {
            password_hash($motDePasse, self::algo()); // même coût qu'une vérification : pas d'indice par le temps de réponse
            $this->app->audit('connexion_echec', null, null, ['raison' => 'compte_inconnu'], 'systeme');
            return $refus;
        }
        if ($this->bloque($u)) {
            return ['ok' => false, 'message' => 'Ce compte est bloqué pendant ' . (int) $this->app->config->get('admin.blocage_min', 15) . ' minutes après plusieurs essais. Réessayez plus tard.'];
        }
        if (!(int) $u['actif'] || !password_verify($motDePasse, (string) $u['mdp_hash'])) {
            $this->echec($u, 'mot_de_passe');
            return $refus;
        }
        if (password_needs_rehash((string) $u['mdp_hash'], self::algo())) {
            $this->app->base->maj('utilisateur', ['mdp_hash' => self::hacher($motDePasse)], 'id = ?', [$u['id']]);
        }
        if (session_status() === PHP_SESSION_ACTIVE) {
            session_regenerate_id(true);
        }
        $_SESSION['attente_2fa'] = (int) $u['id'];
        $_SESSION['attente_le'] = time();
        return ['ok' => true, 'message' => ''];
    }

    public function en2fa(): bool
    {
        return is_int($_SESSION['attente_2fa'] ?? null) && (int) ($_SESSION['attente_le'] ?? 0) >= time() - self::ATTENTE_2FA_S;
    }

    /** @return array{ok: bool, message: string} */
    public function etapeCode(string $code): array
    {
        if (!$this->en2fa()) {
            unset($_SESSION['attente_2fa'], $_SESSION['attente_le']);
            return ['ok' => false, 'message' => 'Le délai pour saisir le code est passé. Reconnectez-vous.'];
        }
        $u = $this->app->base->un('SELECT * FROM utilisateur WHERE id = ? AND actif = 1', [$_SESSION['attente_2fa']]);
        if ($u === null || $this->bloque($u)) {
            unset($_SESSION['attente_2fa'], $_SESSION['attente_le']);
            return ['ok' => false, 'message' => 'Ce compte est bloqué pour le moment. Réessayez plus tard.'];
        }
        $code = trim($code);
        $ok = false;
        $secret = $u['totp_secret'] ? Totp::dechiffrer((string) $u['totp_secret'], $this->app->secretAdmin()) : null;
        if ($secret !== null && preg_match('/^\d{3}\s?\d{3}$/', $code)) {
            $pas = Totp::verifier($secret, $code, time(), (int) $u['totp_dernier_pas']);
            if ($pas !== null) {
                $this->app->base->maj('utilisateur', ['totp_dernier_pas' => $pas], 'id = ?', [$u['id']]);
                $ok = true;
            }
        } elseif ($code !== '') {
            $ok = $this->utiliserCodeSecours($u, $code);
        }
        if (!$ok) {
            $this->echec($u, 'code_2fa');
            return ['ok' => false, 'message' => 'Code incorrect ou déjà utilisé. Saisissez le code à 6 chiffres affiché maintenant par l\'application.'];
        }
        $csrf = bin2hex(random_bytes(32));
        if (session_status() === PHP_SESSION_ACTIVE) {
            session_regenerate_id(true);
        }
        $_SESSION = ['uid' => (int) $u['id'], 'auth_mdp' => crc32((string) $u['mdp_hash']), 'activite' => time(), 'csrf' => $csrf];
        $this->app->base->maj('utilisateur', ['echecs' => 0, 'bloque_jusqu_au' => null, 'derniere_connexion_le' => Base::maintenant()], 'id = ?', [$u['id']]);
        $u['id'] = (int) $u['id'];
        $this->app->utilisateur = $u;
        $this->app->audit('connexion', 'utilisateur', (string) $u['id']);
        return ['ok' => true, 'message' => ''];
    }

    private function utiliserCodeSecours(array $u, string $code): bool
    {
        $codes = json_decode((string) ($u['codes_secours'] ?? '[]'), true) ?: [];
        $empreinte = self::empreinteCode($code);
        foreach ($codes as $i => $e) {
            if (hash_equals((string) $e, $empreinte)) {
                unset($codes[$i]);
                $this->app->base->maj('utilisateur', ['codes_secours' => json_encode(array_values($codes))], 'id = ?', [$u['id']]);
                $this->app->audit('code_secours_utilise', 'utilisateur', (string) $u['id'], ['restants' => count($codes)], 'systeme');
                return true;
            }
        }
        return false;
    }

    private function bloque(array $u): bool
    {
        return $u['bloque_jusqu_au'] !== null && (string) $u['bloque_jusqu_au'] > Base::maintenant();
    }

    private function echec(array $u, string $raison): void
    {
        $echecs = (int) $u['echecs'] + 1;
        $max = max(3, (int) $this->app->config->get('admin.tentatives_max', 5));
        $valeurs = ['echecs' => $echecs];
        if ($echecs >= $max) {
            $valeurs = ['echecs' => 0, 'bloque_jusqu_au' => gmdate('Y-m-d H:i:s', time() + 60 * (int) $this->app->config->get('admin.blocage_min', 15))];
            $this->app->audit('compte_bloque', 'utilisateur', (string) $u['id'], ['echecs' => $echecs], 'systeme');
        }
        $this->app->base->maj('utilisateur', $valeurs, 'id = ?', [$u['id']]);
        $this->app->audit('connexion_echec', 'utilisateur', (string) $u['id'], ['raison' => $raison], 'systeme');
    }

    private function cleIp(): string
    {
        return hash_hmac('sha256', 'connexion|' . $this->app->ip(), $this->app->config->secret('local') ?: 'local');
    }

    private function ipBloquee(): bool
    {
        $depuis = gmdate('Y-m-d H:i:s', time() - 900);
        $n = (int) $this->app->base->valeur('SELECT COUNT(*) FROM tentative_connexion WHERE cle = ? AND quand > ?', [$this->cleIp(), $depuis]);
        return $n >= max(5, (int) $this->app->config->get('admin.tentatives_ip_15min', 30));
    }

    private function noterEssaiIp(): void
    {
        $this->app->base->inserer('tentative_connexion', ['cle' => $this->cleIp(), 'quand' => Base::maintenant()]);
        if (random_int(1, 50) === 1) {
            $this->app->base->executer('DELETE FROM tentative_connexion WHERE quand < ?', [gmdate('Y-m-d H:i:s', time() - 86400)]);
        }
    }

    // ------------------------------------------------------------- comptes

    public static function algo(): string|int|null
    {
        return defined('PASSWORD_ARGON2ID') ? PASSWORD_ARGON2ID : PASSWORD_DEFAULT;
    }

    public static function hacher(string $motDePasse): string
    {
        return password_hash($motDePasse, self::algo());
    }

    /** Message d'erreur, ou null si le mot de passe convient (§6.5 : 12 caractères, pas trivial). */
    public static function motDePasseRefuse(string $mdp, string $email = ''): ?string
    {
        if (mb_strlen($mdp) < 12) {
            return 'Le mot de passe doit compter au moins 12 caractères.';
        }
        if (mb_strlen($mdp) > 200) {
            return 'Le mot de passe est trop long (200 caractères au plus).';
        }
        $bas = mb_strtolower($mdp);
        $courants = ['123456789012', 'motdepasse12', 'password1234', 'azertyuiop12', 'qwertzuiop12', 'andyconstruct', 'andy-construct', 'chantier2026', 'chantier2027'];
        if (count(array_unique(mb_str_split($bas))) < 5 || in_array($bas, $courants, true) || ($email !== '' && str_contains($bas, strtolower(strtok($email, '@') ?: '~')))) {
            return 'Ce mot de passe est trop facile à deviner. Choisissez une phrase de plusieurs mots.';
        }
        return null;
    }

    public static function empreinteCode(string $code): string
    {
        return hash('sha256', strtoupper(preg_replace('/[^A-Za-z0-9]/', '', $code) ?? ''));
    }

    /**
     * Crée un compte avec sa double authentification.
     *
     * @return array{id: int, secret: string, codes: list<string>}
     */
    public function creerUtilisateur(string $email, string $nom, string $role, ?string $roleMetier, string $motDePasse, ?string $secretImpose = null): array
    {
        $email = Validateur::normaliserEmail(trim($email)) ?? '';
        if ($email === '') {
            throw new \DomainException('Adresse e-mail invalide.');
        }
        $email = strtolower($email);
        if (!isset(self::ROLES[$role])) {
            throw new \DomainException('Rôle inconnu.');
        }
        if ($roleMetier !== null && !in_array($roleMetier, ['bureau', 'terrain'], true)) {
            throw new \DomainException('Rôle métier inconnu (bureau ou terrain).');
        }
        $nom = trim($nom);
        if ($nom === '' || mb_strlen($nom) > 100) {
            throw new \DomainException('Indiquez le nom affiché (100 caractères au plus).');
        }
        if (($m = self::motDePasseRefuse($motDePasse, $email)) !== null) {
            throw new \DomainException($m);
        }
        if ($this->app->base->valeur('SELECT id FROM utilisateur WHERE email = ?', [$email]) !== null) {
            throw new \DomainException('Un compte existe déjà avec cette adresse.');
        }
        $secret = $secretImpose ?? Totp::nouveauSecret();
        $codes = [];
        for ($i = 0; $i < 10; $i++) {
            $brut = strtoupper(bin2hex(random_bytes(5)));
            $codes[] = substr($brut, 0, 5) . '-' . substr($brut, 5);
        }
        $id = $this->app->base->inserer('utilisateur', [
            'email' => $email,
            'nom_affiche' => $nom,
            'role' => $role,
            'role_metier' => $role === 'associe' ? $roleMetier : null,
            'mdp_hash' => self::hacher($motDePasse),
            'totp_secret' => Totp::chiffrer($secret, $this->app->secretAdmin()),
            'codes_secours' => json_encode(array_map([self::class, 'empreinteCode'], $codes)),
            'actif' => 1,
            'cree_le' => Base::maintenant(),
            'mdp_change_le' => Base::maintenant(),
        ]);
        $this->app->audit('utilisateur_cree', 'utilisateur', (string) $id, ['role' => $role], PHP_SAPI === 'cli' ? 'systeme' : 'utilisateur');
        return ['id' => $id, 'secret' => $secret, 'codes' => $codes];
    }

    /** Nouvelle double authentification pour un compte (perte du téléphone). */
    public function reinitialiser2fa(int $id): array
    {
        $secret = Totp::nouveauSecret();
        $codes = [];
        for ($i = 0; $i < 10; $i++) {
            $brut = strtoupper(bin2hex(random_bytes(5)));
            $codes[] = substr($brut, 0, 5) . '-' . substr($brut, 5);
        }
        $this->app->base->maj('utilisateur', [
            'totp_secret' => Totp::chiffrer($secret, $this->app->secretAdmin()),
            'totp_dernier_pas' => 0,
            'codes_secours' => json_encode(array_map([self::class, 'empreinteCode'], $codes)),
        ], 'id = ?', [$id]);
        $this->app->audit('2fa_reinitialisee', 'utilisateur', (string) $id);
        return ['secret' => $secret, 'codes' => $codes];
    }

    public function changerMotDePasse(int $id, string $actuel, string $nouveau): void
    {
        $u = $this->app->base->un('SELECT * FROM utilisateur WHERE id = ?', [$id]);
        if ($u === null || !password_verify($actuel, (string) $u['mdp_hash'])) {
            throw new \DomainException('Le mot de passe actuel est incorrect.');
        }
        if (($m = self::motDePasseRefuse($nouveau, (string) $u['email'])) !== null) {
            throw new \DomainException($m);
        }
        $hash = self::hacher($nouveau);
        $this->app->base->maj('utilisateur', ['mdp_hash' => $hash, 'mdp_change_le' => Base::maintenant()], 'id = ?', [$id]);
        $_SESSION['auth_mdp'] = crc32($hash);
        $this->app->audit('mot_de_passe_change', 'utilisateur', (string) $id);
    }
}
