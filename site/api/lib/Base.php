<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Base de données des demandes (PDO) : SQLite par défaut, MariaDB par simple
 * changement de DSN dans config.php (clé « base »). Même code pour les deux.
 *
 * - Dates et heures en UTC (« AAAA-MM-JJ HH:MM:SS »), affichées en Europe/Zurich.
 * - Migrations numérotées, idempotentes (table « migration ») : appliquées au
 *   premier accès de chaque processus, sans outil externe.
 * - Requêtes toujours préparées ; noms de tables et de colonnes jamais issus d'une saisie.
 *
 * Modèle : docs/v4/admin/plan-dashboard-admin.md §4 (sous-ensemble du MVP).
 */
final class Base
{
    public const VERSION_SCHEMA = 1;

    private static array $migrees = [];

    public function __construct(private \PDO $pdo)
    {
        $this->pdo->setAttribute(\PDO::ATTR_ERRMODE, \PDO::ERRMODE_EXCEPTION);
        $this->pdo->setAttribute(\PDO::ATTR_DEFAULT_FETCH_MODE, \PDO::FETCH_ASSOC);
        $this->pdo->setAttribute(\PDO::ATTR_EMULATE_PREPARES, false);
        if ($this->pilote() === 'sqlite') {
            $this->pdo->exec('PRAGMA busy_timeout = 5000');
            $this->pdo->exec('PRAGMA foreign_keys = ON');
        } elseif ($this->pilote() === 'mysql') {
            $this->pdo->exec("SET NAMES utf8mb4, time_zone = '+00:00'");
        }
    }

    /** Connexion selon config.php ; lève une exception si la base est injoignable. */
    public static function depuisConfig(Config $config, bool $migrer = true): self
    {
        $dsn = (string) $config->get('base.dsn', '');
        if ($dsn === '') {
            $stockage = new Stockage((string) $config->get('stockage'));
            $dsn = 'sqlite:' . $stockage->dossier('base') . '/andy-construct.sqlite';
        }
        $pdo = new \PDO($dsn, (string) $config->get('base.utilisateur', '') ?: null, (string) $config->get('base.mot_de_passe', '') ?: null, [
            \PDO::ATTR_TIMEOUT => 5,
            \PDO::ATTR_ERRMODE => \PDO::ERRMODE_EXCEPTION,
        ]);
        if (str_starts_with($dsn, 'sqlite:')) {
            @chmod(substr($dsn, 7), 0640);
        }
        $base = new self($pdo);
        if ($migrer) {
            $base->migrer();
        }
        return $base;
    }

    public function pdo(): \PDO
    {
        return $this->pdo;
    }

    public function pilote(): string
    {
        return (string) $this->pdo->getAttribute(\PDO::ATTR_DRIVER_NAME);
    }

    // ------------------------------------------------------------- requêtes

    /** @return array<string, mixed>|null */
    public function un(string $sql, array $p = []): ?array
    {
        $st = $this->pdo->prepare($sql);
        $st->execute($p);
        $ligne = $st->fetch();
        return $ligne === false ? null : $ligne;
    }

    /** @return list<array<string, mixed>> */
    public function tous(string $sql, array $p = []): array
    {
        $st = $this->pdo->prepare($sql);
        $st->execute($p);
        return $st->fetchAll();
    }

    public function valeur(string $sql, array $p = []): mixed
    {
        $st = $this->pdo->prepare($sql);
        $st->execute($p);
        $v = $st->fetchColumn();
        return $v === false ? null : $v;
    }

    public function executer(string $sql, array $p = []): int
    {
        $st = $this->pdo->prepare($sql);
        $st->execute($p);
        return $st->rowCount();
    }

    /** @param array<string, mixed> $valeurs */
    public function inserer(string $table, array $valeurs): int
    {
        self::verifierNom($table);
        array_map([self::class, 'verifierNom'], array_keys($valeurs));
        $cols = implode(', ', array_keys($valeurs));
        $marques = implode(', ', array_fill(0, count($valeurs), '?'));
        $this->executer("INSERT INTO $table ($cols) VALUES ($marques)", array_values($valeurs));
        return (int) $this->pdo->lastInsertId();
    }

    /** @param array<string, mixed> $valeurs */
    public function maj(string $table, array $valeurs, string $where, array $p = []): int
    {
        self::verifierNom($table);
        $sets = [];
        foreach (array_keys($valeurs) as $col) {
            self::verifierNom($col);
            $sets[] = "$col = ?";
        }
        return $this->executer("UPDATE $table SET " . implode(', ', $sets) . " WHERE $where", array_merge(array_values($valeurs), $p));
    }

    public function transaction(callable $fn): mixed
    {
        if ($this->pdo->inTransaction()) {
            return $fn($this);
        }
        $this->pdo->beginTransaction();
        try {
            $r = $fn($this);
            $this->pdo->commit();
            return $r;
        } catch (\Throwable $e) {
            $this->pdo->rollBack();
            throw $e;
        }
    }

    private static function verifierNom(string $nom): void
    {
        if (!preg_match('/^[a-z_][a-z0-9_]{0,63}$/', $nom)) {
            throw new \InvalidArgumentException('Nom SQL refusé.');
        }
    }

    // ---------------------------------------------------------------- dates

    public static function utc(\DateTimeInterface $t): string
    {
        return \DateTimeImmutable::createFromInterface($t)->setTimezone(new \DateTimeZone('UTC'))->format('Y-m-d H:i:s');
    }

    public static function maintenant(): string
    {
        return gmdate('Y-m-d H:i:s');
    }

    /** Date UTC de la base → instant Europe/Zurich (null si vide). */
    public static function local(?string $utc): ?\DateTimeImmutable
    {
        if ($utc === null || $utc === '') {
            return null;
        }
        if (strlen($utc) === 10) { // colonne DATE : jour civil, sans fuseau
            return new \DateTimeImmutable($utc . ' 12:00', new \DateTimeZone('Europe/Zurich'));
        }
        return (new \DateTimeImmutable($utc, new \DateTimeZone('UTC')))->setTimezone(new \DateTimeZone('Europe/Zurich'));
    }

    // ----------------------------------------------------------- migrations

    /** Applique les migrations manquantes. Idempotent, sans risque si lancé deux fois. */
    public function migrer(): void
    {
        $cle = spl_object_id($this->pdo);
        if (isset(self::$migrees[$cle])) {
            return;
        }
        $this->pdo->exec($this->ddl('CREATE TABLE IF NOT EXISTS migration (version INTEGER NOT NULL PRIMARY KEY, appliquee_le VARCHAR(19) NOT NULL){MOTEUR}'));
        $faite = (int) $this->valeur('SELECT MAX(version) FROM migration');
        foreach ($this->migrations() as $version => $instructions) {
            if ($version <= $faite) {
                continue;
            }
            foreach ($instructions as $sql) {
                $this->executerDdl($sql);
            }
            try {
                $this->inserer('migration', ['version' => $version, 'appliquee_le' => self::maintenant()]);
            } catch (\PDOException) {
                // un autre processus a terminé la même migration au même moment
            }
        }
        self::$migrees[$cle] = true;
    }

    private function executerDdl(string $sql): void
    {
        $sql = $this->ddl($sql);
        if ($this->pilote() === 'mysql' && str_starts_with($sql, 'CREATE INDEX')) {
            try {
                $this->pdo->exec($sql);
            } catch (\PDOException $e) {
                if (!str_contains($e->getMessage(), '1061')) { // index déjà présent
                    throw $e;
                }
            }
            return;
        }
        $this->pdo->exec($sql);
    }

    /** Adapte une instruction aux deux moteurs : {PK}, {MOTEUR}, CREATE INDEX IF NOT EXISTS. */
    private function ddl(string $sql): string
    {
        if ($this->pilote() === 'mysql') {
            return strtr($sql, [
                '{PK}' => 'INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY',
                '{MOTEUR}' => ' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci',
                'CREATE INDEX IF NOT EXISTS' => 'CREATE INDEX',
                ' TEXT' => ' MEDIUMTEXT',
            ]);
        }
        return strtr($sql, ['{PK}' => 'INTEGER PRIMARY KEY AUTOINCREMENT', '{MOTEUR}' => '']);
    }

    /** @return array<int, list<string>> */
    private function migrations(): array
    {
        return [
            1 => [
                'CREATE TABLE IF NOT EXISTS utilisateur (
                    id {PK},
                    email VARCHAR(190) NOT NULL UNIQUE,
                    nom_affiche VARCHAR(100) NOT NULL,
                    role VARCHAR(20) NOT NULL,
                    role_metier VARCHAR(10) NULL,
                    telephone_sms VARCHAR(20) NULL,
                    mdp_hash VARCHAR(255) NOT NULL,
                    totp_secret VARCHAR(255) NULL,
                    totp_dernier_pas BIGINT NOT NULL DEFAULT 0,
                    codes_secours TEXT NULL,
                    actif SMALLINT NOT NULL DEFAULT 1,
                    echecs SMALLINT NOT NULL DEFAULT 0,
                    bloque_jusqu_au DATETIME NULL,
                    cree_le DATETIME NOT NULL,
                    derniere_connexion_le DATETIME NULL,
                    mdp_change_le DATETIME NULL
                ){MOTEUR}',
                'CREATE TABLE IF NOT EXISTS tentative_connexion (
                    id {PK},
                    cle VARCHAR(64) NOT NULL,
                    quand DATETIME NOT NULL
                ){MOTEUR}',
                'CREATE INDEX IF NOT EXISTS ix_tentative_cle ON tentative_connexion (cle, quand)',
                'CREATE TABLE IF NOT EXISTS contact (
                    id {PK},
                    civilite VARCHAR(10) NULL,
                    prenom VARCHAR(100) NULL,
                    nom VARCHAR(100) NULL,
                    organisation VARCHAR(150) NULL,
                    email VARCHAR(190) NULL,
                    email_normalise VARCHAR(190) NULL,
                    telephone_e164 VARCHAR(20) NULL,
                    telephone_affiche VARCHAR(30) NULL,
                    telephone_mobile SMALLINT NOT NULL DEFAULT 0,
                    adresse VARCHAR(300) NULL,
                    npa VARCHAR(10) NULL,
                    localite VARCHAR(100) NULL,
                    preference_contact VARCHAR(20) NULL,
                    creneau VARCHAR(20) NULL,
                    anonymise_le DATETIME NULL,
                    cree_le DATETIME NOT NULL,
                    modifie_le DATETIME NOT NULL
                ){MOTEUR}',
                'CREATE INDEX IF NOT EXISTS ix_contact_email ON contact (email_normalise)',
                'CREATE INDEX IF NOT EXISTS ix_contact_tel ON contact (telephone_e164)',
                'CREATE TABLE IF NOT EXISTS demande (
                    id {PK},
                    ref VARCHAR(16) NOT NULL UNIQUE,
                    contact_id INTEGER NULL,
                    recue_le DATETIME NOT NULL,
                    canal VARCHAR(20) NOT NULL,
                    formulaire VARCHAR(24) NOT NULL,
                    type_client VARCHAR(20) NULL,
                    travaux TEXT NULL,
                    service VARCHAR(30) NULL,
                    surface VARCHAR(20) NULL,
                    delai VARCHAR(20) NULL,
                    commune VARCHAR(100) NULL,
                    npa VARCHAR(10) NULL,
                    canton VARCHAR(4) NULL,
                    zone VARCHAR(10) NULL,
                    message TEXT NULL,
                    connu_par VARCHAR(30) NULL,
                    recommande_par VARCHAR(100) NULL,
                    guide VARCHAR(60) NULL,
                    score INTEGER NULL,
                    priorite VARCHAR(12) NULL,
                    priorite_corrigee VARCHAR(12) NULL,
                    score_detail TEXT NULL,
                    score_regles TEXT NULL,
                    grille_version VARCHAR(20) NULL,
                    echeance_le DATETIME NULL,
                    echeance_initiale_le DATETIME NULL,
                    associe_id INTEGER NULL,
                    statut VARCHAR(20) NOT NULL,
                    statut_change_le DATETIME NOT NULL,
                    premier_appel_le DATETIME NULL,
                    premier_contact_le DATETIME NULL,
                    tentatives_appel INTEGER NOT NULL DEFAULT 0,
                    ne_pas_relancer SMALLINT NOT NULL DEFAULT 0,
                    motif_perte VARCHAR(30) NULL,
                    perdue_le DATETIME NULL,
                    recontact_autorise SMALLINT NOT NULL DEFAULT 0,
                    doublon_de_id INTEGER NULL,
                    accuse_reception VARCHAR(20) NULL,
                    mode_test SMALLINT NOT NULL DEFAULT 0,
                    anonymise_le DATETIME NULL,
                    cree_par INTEGER NULL,
                    cree_le DATETIME NOT NULL,
                    modifie_le DATETIME NOT NULL,
                    version INTEGER NOT NULL DEFAULT 1
                ){MOTEUR}',
                'CREATE INDEX IF NOT EXISTS ix_demande_statut ON demande (statut, echeance_le)',
                'CREATE INDEX IF NOT EXISTS ix_demande_recue ON demande (recue_le)',
                'CREATE INDEX IF NOT EXISTS ix_demande_associe ON demande (associe_id, statut)',
                'CREATE INDEX IF NOT EXISTS ix_demande_contact ON demande (contact_id)',
                'CREATE TABLE IF NOT EXISTS attribution (
                    demande_id INTEGER NOT NULL PRIMARY KEY,
                    categorie VARCHAR(30) NULL,
                    canal_marketing VARCHAR(30) NULL,
                    canal_declare SMALLINT NOT NULL DEFAULT 0,
                    canal_corrige VARCHAR(30) NULL,
                    libelle VARCHAR(150) NULL,
                    emplacement VARCHAR(60) NULL,
                    page VARCHAR(200) NULL,
                    page_entree VARCHAR(200) NULL,
                    referent VARCHAR(150) NULL,
                    utm_source VARCHAR(100) NULL,
                    utm_medium VARCHAR(100) NULL,
                    utm_campaign VARCHAR(100) NULL,
                    utm_content VARCHAR(100) NULL,
                    utm_term VARCHAR(100) NULL,
                    gclid VARCHAR(200) NULL,
                    consent_ads VARCHAR(10) NULL
                ){MOTEUR}',
                'CREATE INDEX IF NOT EXISTS ix_attribution_canal ON attribution (canal_marketing)',
                'CREATE TABLE IF NOT EXISTS interaction (
                    id {PK},
                    demande_id INTEGER NOT NULL,
                    type VARCHAR(20) NOT NULL,
                    resultat VARCHAR(20) NULL,
                    contenu TEXT NULL,
                    auteur_id INTEGER NULL,
                    origine VARCHAR(20) NOT NULL,
                    cree_le DATETIME NOT NULL
                ){MOTEUR}',
                'CREATE INDEX IF NOT EXISTS ix_interaction_demande ON interaction (demande_id, cree_le)',
                'CREATE TABLE IF NOT EXISTS visite (
                    id {PK},
                    demande_id INTEGER NOT NULL,
                    prevue_le DATETIME NOT NULL,
                    adresse VARCHAR(300) NULL,
                    associe_id INTEGER NULL,
                    statut VARCHAR(12) NOT NULL,
                    cree_le DATETIME NOT NULL
                ){MOTEUR}',
                'CREATE INDEX IF NOT EXISTS ix_visite_demande ON visite (demande_id)',
                'CREATE TABLE IF NOT EXISTS offre (
                    id {PK},
                    demande_id INTEGER NOT NULL,
                    numero VARCHAR(30) NULL,
                    version INTEGER NOT NULL DEFAULT 1,
                    montant_ht DECIMAL(10,2) NOT NULL,
                    envoyee_le DATE NOT NULL,
                    statut VARCHAR(12) NOT NULL,
                    relance_etape INTEGER NOT NULL DEFAULT 0,
                    signee_le DATE NULL,
                    montant_signe_ht DECIMAL(10,2) NULL,
                    cree_le DATETIME NOT NULL
                ){MOTEUR}',
                'CREATE INDEX IF NOT EXISTS ix_offre_statut ON offre (statut, envoyee_le)',
                'CREATE INDEX IF NOT EXISTS ix_offre_signee ON offre (signee_le)',
                'CREATE INDEX IF NOT EXISTS ix_offre_demande ON offre (demande_id)',
                'CREATE TABLE IF NOT EXISTS fichier (
                    id {PK},
                    demande_id INTEGER NOT NULL,
                    identifiant VARCHAR(64) NOT NULL,
                    nom_original VARCHAR(200) NULL,
                    type_mime VARCHAR(60) NULL,
                    taille INTEGER NULL,
                    sha256 VARCHAR(64) NULL,
                    origine VARCHAR(12) NOT NULL,
                    cree_le DATETIME NOT NULL,
                    supprime_le DATETIME NULL
                ){MOTEUR}',
                'CREATE INDEX IF NOT EXISTS ix_fichier_demande ON fichier (demande_id)',
                'CREATE TABLE IF NOT EXISTS depense (
                    id {PK},
                    mois DATE NOT NULL,
                    canal_marketing VARCHAR(30) NOT NULL,
                    montant_ht DECIMAL(10,2) NOT NULL,
                    type_cout VARCHAR(12) NOT NULL,
                    origine VARCHAR(12) NOT NULL,
                    saisi_par INTEGER NULL,
                    saisi_le DATETIME NOT NULL,
                    UNIQUE (mois, canal_marketing, type_cout, origine)
                ){MOTEUR}',
                'CREATE TABLE IF NOT EXISTS parametre (
                    cle VARCHAR(60) NOT NULL PRIMARY KEY,
                    valeur TEXT NOT NULL,
                    modifie_par INTEGER NULL,
                    modifie_le DATETIME NOT NULL
                ){MOTEUR}',
                'CREATE TABLE IF NOT EXISTS journal_audit (
                    id {PK},
                    quand DATETIME NOT NULL,
                    utilisateur_id INTEGER NULL,
                    acteur VARCHAR(12) NOT NULL,
                    action VARCHAR(40) NOT NULL,
                    objet_type VARCHAR(20) NULL,
                    objet_id VARCHAR(40) NULL,
                    details TEXT NULL,
                    ip_tronquee VARCHAR(45) NULL
                ){MOTEUR}',
                'CREATE INDEX IF NOT EXISTS ix_audit_quand ON journal_audit (quand)',
                'CREATE INDEX IF NOT EXISTS ix_audit_objet ON journal_audit (objet_type, objet_id)',
            ],
        ];
    }
}
