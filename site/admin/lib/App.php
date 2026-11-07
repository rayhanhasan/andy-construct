<?php
declare(strict_types=1);

namespace AndyConstruct\Admin;

use AndyConstruct\Api\Base;
use AndyConstruct\Api\Config;
use AndyConstruct\Api\HeuresOuvrables;
use AndyConstruct\Api\LimiteDebit;
use AndyConstruct\Api\Scoring;
use AndyConstruct\Api\Stockage;

/**
 * Contexte d'une requête de l'admin : configuration (celle de l'API, un seul
 * config.php), base, heures ouvrables, grille de scoring, utilisateur connecté.
 */
final class App
{
    public readonly Config $config;
    public readonly Base $base;
    public readonly Stockage $stockage;
    public readonly HeuresOuvrables $heures;
    public readonly Scoring $scoring;
    public readonly array $grille;
    public readonly Auth $auth;
    public readonly Demandes $demandes;
    public \DateTimeImmutable $maintenant;
    /** @var array<string, mixed>|null */
    public ?array $utilisateur = null;
    /** @var array<string, mixed> */
    private array $parametres = [];

    public function __construct(Config $config, ?Base $base = null, ?\DateTimeImmutable $maintenant = null)
    {
        $this->config = $config;
        $this->base = $base ?? Base::depuisConfig($config);
        $this->stockage = new Stockage((string) $config->get('stockage'));
        $this->heures = HeuresOuvrables::depuisConfig($config);
        $racineApi = dirname(__DIR__, 2) . '/api';
        $this->grille = (array) json_decode((string) file_get_contents($racineApi . '/data/scoring.json'), true, 32, JSON_THROW_ON_ERROR);
        $this->scoring = new Scoring($this->grille);
        $this->maintenant = $maintenant ?? new \DateTimeImmutable('now', new \DateTimeZone('Europe/Zurich'));
        $this->auth = new Auth($this);
        $this->demandes = new Demandes($this);
    }

    public static function demarrer(): self
    {
        return new self(Config::charger());
    }

    /** Clé maîtresse des secrets 2FA : secrets.admin (32 caractères au moins). */
    public function secretAdmin(): string
    {
        $s = $this->config->secret('admin');
        if (strlen($s) >= 32) {
            return $s;
        }
        if ($this->config->modeTest()) {
            return hash('sha256', 'admin-test|' . $this->config->secret('local'));
        }
        throw new \RuntimeException('Secret « admin » absent ou trop court dans config.php (32 caractères minimum).');
    }

    // ---------------------------------------------------------- paramètres

    public const PARAMETRES_DEFAUT = [
        'marge_brute' => 0.30,          // décision G4 : à fournir par le client (valeur illustrative)
        'panier_reference' => 9000,     // décision G4 : à fournir par le client (valeur illustrative)
        'mise_en_ligne' => '',          // AAAA-MM : mois M1 des objectifs (vide = mois de la première demande)
        'seuil_carnet_semaines' => 8,
        // Jalons M3 / M6 / M12 (strategie-acquisition.md §1.1, scénario M ; plan admin §5.2).
        'objectifs' => [
            'demandes' => [3 => 10, 6 => 18, 12 => 30],
            'part_ab' => [3 => 50, 6 => 60, 12 => 65],
            'delai_a_h' => [3 => 4, 6 => 2, 12 => 2],
            'demande_offre' => [3 => 55, 6 => 60, 12 => 65],
            'offre_signee' => [3 => 25, 6 => 28, 12 => 30],
            'chantiers' => [3 => 1.5, 6 => 3, 12 => 6],
        ],
    ];

    public function parametre(string $cle): mixed
    {
        if (!array_key_exists($cle, $this->parametres)) {
            $v = $this->base->valeur('SELECT valeur FROM parametre WHERE cle = ?', [$cle]);
            $this->parametres[$cle] = $v === null ? (self::PARAMETRES_DEFAUT[$cle] ?? null) : json_decode((string) $v, true);
        }
        return $this->parametres[$cle];
    }

    public function definirParametre(string $cle, mixed $valeur): void
    {
        $json = json_encode($valeur, JSON_UNESCAPED_UNICODE);
        $uid = $this->utilisateur['id'] ?? null;
        if ($this->base->valeur('SELECT cle FROM parametre WHERE cle = ?', [$cle]) === null) {
            $this->base->inserer('parametre', ['cle' => $cle, 'valeur' => $json, 'modifie_par' => $uid, 'modifie_le' => Base::maintenant()]);
        } else {
            $this->base->maj('parametre', ['valeur' => $json, 'modifie_par' => $uid, 'modifie_le' => Base::maintenant()], 'cle = ?', [$cle]);
        }
        $this->parametres[$cle] = $valeur;
    }

    // --------------------------------------------------------------- audit

    /**
     * Journal d'audit : qui, quoi, sur quel objet. Jamais de valeur personnelle
     * dans $details (seulement des noms de champs, des codes, des nombres).
     */
    public function audit(string $action, ?string $objetType = null, ?string $objetId = null, array $details = [], string $acteur = 'utilisateur'): void
    {
        $this->base->inserer('journal_audit', [
            'quand' => Base::maintenant(),
            'utilisateur_id' => $this->utilisateur['id'] ?? null,
            'acteur' => $acteur,
            'action' => $action,
            'objet_type' => $objetType,
            'objet_id' => $objetId,
            'details' => $details === [] ? null : json_encode($details, JSON_UNESCAPED_UNICODE),
            'ip_tronquee' => $this->ipTronquee(),
        ]);
    }

    public function ip(): string
    {
        return LimiteDebit::ipClient(
            $_SERVER,
            (bool) $this->config->get('faire_confiance_au_proxy'),
            array_values(array_filter((array) $this->config->get('proxys_de_confiance', []), 'is_string'))
        );
    }

    /** IPv4 sans le dernier octet, IPv6 réduite à son /48 : assez pour enquêter, pas pour suivre. */
    public function ipTronquee(): ?string
    {
        if (PHP_SAPI === 'cli') {
            return null;
        }
        $ip = $this->ip();
        if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {
            return preg_replace('/\.\d+$/', '.0', $ip);
        }
        if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV6)) {
            $bin = (string) inet_pton($ip);
            return inet_ntop(substr($bin, 0, 6) . str_repeat("\0", 10)) . '/48';
        }
        return null;
    }
}
