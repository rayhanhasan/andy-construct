<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Dossiers privés : fichiers reçus, file d'attente du webhook, journaux,
 * limites de débit, compteurs, e-mails de test.
 *
 * Idéalement hors de la racine web (voir config.example.php). Si le dossier est
 * dans la racine web, chaque sous-dossier reçoit un .htaccess « deny » et un
 * index.html vide, et l'exécution de PHP y est coupée.
 */
final class Stockage
{
    public const SOUS_DOSSIERS = [
        'fichiers', 'file-attente', 'mails-echec', 'journaux', 'limites',
        'compteurs', 'verrous', 'test-mails', 'test-webhooks',
        // Admin (docs/v4/admin) : base SQLite, demandes à rejouer en base, sessions.
        'base', 'file-attente-base', 'sessions',
    ];

    private const HTACCESS = <<<'TXT'
# Stockage privé : aucun accès direct depuis le web.
<IfModule mod_authz_core.c>
    Require all denied
</IfModule>
<IfModule !mod_authz_core.c>
    Order allow,deny
    Deny from all
</IfModule>
Options -Indexes -ExecCGI
<IfModule mod_php.c>
    php_flag engine off
</IfModule>
RemoveHandler .php .phtml .phar .cgi .pl .py
RemoveType .php .phtml .phar
TXT;

    private string $racine;

    public function __construct(string $racine)
    {
        $this->racine = rtrim($racine, '/');
    }

    public function racine(): string
    {
        return $this->racine;
    }

    /** Chemin d'un sous-dossier, créé et protégé au besoin. */
    public function dossier(string $nom): string
    {
        if (!in_array($nom, self::SOUS_DOSSIERS, true)) {
            throw new \InvalidArgumentException("Sous-dossier inconnu : $nom");
        }
        $this->proteger($this->racine);
        $chemin = $this->racine . '/' . $nom;
        $this->proteger($chemin);
        return $chemin;
    }

    private function proteger(string $chemin): void
    {
        if (!is_dir($chemin) && !@mkdir($chemin, 0750, true) && !is_dir($chemin)) {
            throw new \RuntimeException('Impossible de créer le dossier de stockage.');
        }
        if (!is_file($chemin . '/.htaccess')) {
            @file_put_contents($chemin . '/.htaccess', self::HTACCESS . "\n");
        }
        if (!is_file($chemin . '/index.html')) {
            @file_put_contents($chemin . '/index.html', '');
        }
    }

    /** Écriture atomique (fichier temporaire + rename), droits restreints. */
    public function ecrireAtomique(string $chemin, string $contenu): void
    {
        $tmp = $chemin . '.tmp-' . bin2hex(random_bytes(4));
        if (file_put_contents($tmp, $contenu, LOCK_EX) === false) {
            throw new \RuntimeException('Écriture impossible dans le stockage.');
        }
        @chmod($tmp, 0640);
        if (!rename($tmp, $chemin)) {
            @unlink($tmp);
            throw new \RuntimeException('Écriture impossible dans le stockage.');
        }
    }

    /**
     * Supprime les fichiers plus anciens que $jours dans un sous-dossier
     * (récursif sur un niveau). Ne touche jamais .htaccess ni index.html.
     */
    public function purger(string $sousDossier, float $jours): int
    {
        $dossier = $this->dossier($sousDossier);
        $limite = time() - (int) round($jours * 86400);
        $supprimes = 0;
        $iterateur = new \RecursiveIteratorIterator(
            new \RecursiveDirectoryIterator($dossier, \FilesystemIterator::SKIP_DOTS),
            \RecursiveIteratorIterator::CHILD_FIRST
        );
        foreach ($iterateur as $element) {
            /** @var \SplFileInfo $element */
            $nom = $element->getFilename();
            if ($nom === '.htaccess' || $nom === 'index.html') {
                continue;
            }
            if ($element->isFile() && $element->getMTime() < $limite) {
                if (@unlink($element->getPathname())) {
                    $supprimes++;
                }
            } elseif ($element->isDir()) {
                @rmdir($element->getPathname()); // ne supprime que si vide
            }
        }
        return $supprimes;
    }

    /**
     * Exécute $fn sous verrou exclusif nommé (flock). Retourne null si le
     * verrou n'a pas pu être pris sans attendre et que $attendre est faux.
     */
    public function sousVerrou(string $nom, callable $fn, bool $attendre = true): mixed
    {
        $fichier = $this->dossier('verrous') . '/' . preg_replace('/[^a-z0-9_-]/i', '_', $nom) . '.lock';
        $h = fopen($fichier, 'c');
        if ($h === false) {
            throw new \RuntimeException('Verrou impossible.');
        }
        try {
            $mode = $attendre ? LOCK_EX : (LOCK_EX | LOCK_NB);
            if (!flock($h, $mode)) {
                return null;
            }
            return $fn();
        } finally {
            flock($h, LOCK_UN);
            fclose($h);
        }
    }
}
