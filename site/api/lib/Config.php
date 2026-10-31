<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Configuration : valeurs par défaut + fichier config.php (ignoré par git).
 *
 * Le chemin du fichier peut être imposé par la variable d'environnement
 * AC_API_CONFIG (utilisé par les tests et le serveur de développement).
 */
final class Config
{
    /** @var array<string, mixed> */
    private array $valeurs;

    /** @param array<string, mixed> $valeurs */
    public function __construct(array $valeurs)
    {
        $this->valeurs = self::fusionner(self::defauts(), $valeurs);
    }

    public static function charger(?string $chemin = null): self
    {
        $chemin = $chemin ?? (getenv('AC_API_CONFIG') ?: dirname(__DIR__) . '/config.php');
        if (!is_file($chemin)) {
            throw new \RuntimeException('Configuration absente : copiez config.example.php en config.php.');
        }
        $valeurs = require $chemin;
        if (!is_array($valeurs)) {
            throw new \RuntimeException('config.php doit retourner un tableau.');
        }
        $config = new self($valeurs);
        $config->verifier();
        return $config;
    }

    /** Accès par chemin pointé : get('smtp.hote'). */
    public function get(string $chemin, mixed $defaut = null): mixed
    {
        $valeur = $this->valeurs;
        foreach (explode('.', $chemin) as $cle) {
            if (!is_array($valeur) || !array_key_exists($cle, $valeur)) {
                return $defaut;
            }
            $valeur = $valeur[$cle];
        }
        return $valeur;
    }

    public function modeTest(): bool
    {
        return (bool) $this->get('mode_test', false);
    }

    public function secret(string $nom): string
    {
        return (string) $this->get('secrets.' . $nom, '');
    }

    /** Refuse de démarrer en production avec des secrets absents ou trop courts. */
    public function verifier(): void
    {
        foreach (['hmac_webhook', 'actions', 'local'] as $nom) {
            $secret = $this->secret($nom);
            if (strlen($secret) < 32) {
                if ($this->modeTest() && $secret === '') {
                    continue;
                }
                throw new \RuntimeException("Secret « $nom » absent ou trop court (32 caractères minimum).");
            }
        }
        $stockage = (string) $this->get('stockage');
        if ($stockage === '') {
            throw new \RuntimeException('Chemin de stockage non configuré.');
        }
    }

    /** @return array<string, mixed> */
    public static function defauts(): array
    {
        return [
            'mode_test' => false,
            'url_site' => 'https://www.andyconstruct.ch',
            'url_api' => 'https://www.andyconstruct.ch/api',
            'origines_autorisees' => ['https://www.andyconstruct.ch', 'https://andyconstruct.ch'],
            'stockage' => dirname(__DIR__) . '/stockage',
            'faire_confiance_au_proxy' => false,
            'secrets' => ['hmac_webhook' => '', 'actions' => '', 'local' => ''],
            'smtp' => [
                'actif' => true,
                'hote' => '',
                'port' => 587,
                'securite' => 'tls',
                'utilisateur' => '',
                'mot_de_passe' => '',
                'delai' => 10,
            ],
            'repli_mail' => true,
            'expediteur' => ['email' => 'site@andyconstruct.ch', 'nom' => 'Andy Construct'],
            'repondre_a' => ['email' => 'contact@andyconstruct.ch', 'nom' => 'Andy Construct'],
            'destinataires_internes' => [],
            'alerte_email' => '',
            'associes' => [
                'bureau' => ['nom' => '', 'email' => '', 'mobile' => ''],
                'terrain' => ['nom' => '', 'email' => '', 'mobile' => ''],
            ],
            'entreprise' => [
                'nom' => 'Andy Construct',
                'adresse' => 'Route des Acacias 48, 1227 Carouge',
                'tel_fixe' => '022 771 20 15',
                'tel_mobile' => '078 631 14 34',
                'site' => 'www.andyconstruct.ch',
                'email' => 'contact@andyconstruct.ch',
                'horaires' => 'du lundi au vendredi, de 7 h à 18 h',
            ],
            'numeros_appel_sortant' => 'le 022 771 20 15 ou le 078 631 14 34',
            'url_confidentialite' => 'https://www.andyconstruct.ch/confidentialite.html',
            'accord_obligatoire' => true,
            'realisations_par_service' => [],
            'n8n' => [
                'url_demande' => '',
                'url_aimant' => '',
                'url_actions' => '',
                'url_desinscription' => '',
                'delai' => 5,
                'simuler' => false,
            ],
            'pages' => [
                'merci_devis' => '/merci.html',
                'merci_rappel' => '/merci.html',
                'merci_aimant' => '/merci-guide.html',
                'formulaire' => '/contact.html#formulaire',
            ],
            'anti_spam' => [
                'delai_min' => ['devis' => 4, 'rappel' => 2, 'aimant' => 2],
                'jeton_validite_h' => 12,
                'limite_par_heure' => 5,
                'tentatives_par_heure' => 30,
                'max_liens_message' => 3,
            ],
            'fichiers' => [
                'max_nombre' => 3,
                'max_taille_mo' => 8,
                'conservation_jours' => 30,
                'pj_max_total_mo' => 20,
                'lien_validite_h_interne' => 168,
                'lien_validite_h_n8n' => 24,
                'refuser_pdf_actifs' => true,
            ],
            'conservation' => [
                'journaux_jours' => 30,
                'file_attente_alerte_minutes' => 60,
                'file_attente_abandon_jours' => 14,
                'mails_test_jours' => 7,
            ],
            'heures_ouvrables' => [
                'debut' => 7,
                'fin' => 18,
                'jours_fermes' => [],
            ],
            'promesse_delai' => true,
            'aimants' => [],
            'notifier_aimants' => 'b2b_et_poste',
            'cle_saisie_interne' => '',
            'cron_cle' => '',
            'healthcheck_url' => '',
            'reference_prefixe' => 'AC',
        ];
    }

    /**
     * Fusion récursive : les tableaux associatifs sont fusionnés, les listes remplacées.
     *
     * @param array<mixed> $base
     * @param array<mixed> $ajout
     * @return array<mixed>
     */
    private static function fusionner(array $base, array $ajout): array
    {
        foreach ($ajout as $cle => $valeur) {
            if (is_array($valeur) && isset($base[$cle]) && is_array($base[$cle])
                && !array_is_list($valeur) && !array_is_list($base[$cle])) {
                $base[$cle] = self::fusionner($base[$cle], $valeur);
            } else {
                $base[$cle] = $valeur;
            }
        }
        return $base;
    }
}
