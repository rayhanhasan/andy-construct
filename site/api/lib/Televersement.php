<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Pièces jointes (photos, plans) : 3 au maximum, 8 Mo chacune, JPG, PNG,
 * HEIC ou PDF. Le type réel est vérifié avec finfo (jamais l'extension ni le
 * type annoncé par le navigateur), puis par un contrôle de structure.
 * Les fichiers sont renommés aléatoirement et stockés dans le dossier privé.
 */
final class Televersement
{
    private const TYPES = [
        'image/jpeg' => 'jpg',
        'image/png' => 'png',
        'image/heic' => 'heic',
        'image/heif' => 'heic',
        'image/heic-sequence' => 'heic',
        'image/heif-sequence' => 'heic',
        'application/pdf' => 'pdf',
    ];
    private const MARQUES_HEIF = ['heic', 'heix', 'hevc', 'hevx', 'heim', 'heis', 'mif1', 'msf1'];
    public const MIME_PAR_EXTENSION = [
        'jpg' => 'image/jpeg', 'png' => 'image/png', 'heic' => 'image/heic', 'pdf' => 'application/pdf',
    ];

    public function __construct(
        private Stockage $stockage,
        private int $maxNombre = 3,
        private int $maxOctets = 8 * 1024 * 1024,
        private bool $refuserPdfActifs = true,
        private bool $exigerTeleversementHttp = true,
        private string $emailRepli = 'contact@andyconstruct.ch'
    ) {
    }

    /**
     * Met les entrées de $_FILES (« fichiers[] », « fichier », « fichier[] ») à plat.
     *
     * @return list<array{name: string, tmp_name: string, error: int, size: int}>
     */
    public static function aplatir(array $files): array
    {
        $liste = [];
        foreach (['fichiers', 'fichier'] as $champ) {
            if (!isset($files[$champ]) || !is_array($files[$champ])) {
                continue;
            }
            $f = $files[$champ];
            if (is_array($f['name'] ?? null)) {
                foreach (array_keys($f['name']) as $i) {
                    if (is_array($f['name'][$i])) {
                        continue; // structure imbriquée inattendue : ignorée
                    }
                    $liste[] = [
                        'name' => (string) $f['name'][$i],
                        'tmp_name' => (string) ($f['tmp_name'][$i] ?? ''),
                        'error' => (int) ($f['error'][$i] ?? UPLOAD_ERR_NO_FILE),
                        'size' => (int) ($f['size'][$i] ?? 0),
                    ];
                }
            } else {
                $liste[] = [
                    'name' => (string) ($f['name'] ?? ''),
                    'tmp_name' => (string) ($f['tmp_name'] ?? ''),
                    'error' => (int) ($f['error'] ?? UPLOAD_ERR_NO_FILE),
                    'size' => (int) ($f['size'] ?? 0),
                ];
            }
        }
        return array_values(array_filter($liste, static fn ($f) => $f['error'] !== UPLOAD_ERR_NO_FILE));
    }

    /**
     * Contrôle tous les fichiers puis, s'ils sont tous valables, les enregistre.
     *
     * @param list<array{name: string, tmp_name: string, error: int, size: int}> $fichiers
     * @return array{0: list<array{id: string, nom: string, type: string, taille: int, chemin: string, sha256: string}>, 1: ?string, 2: ?string}
     *   [fichiers enregistrés, message d'erreur pour le visiteur, raison technique (journal)]
     */
    public function traiter(array $fichiers): array
    {
        if ($fichiers === []) {
            return [[], null, null];
        }
        if (count($fichiers) > $this->maxNombre) {
            return [[], "Vous pouvez joindre {$this->maxNombre} fichiers au maximum. Les autres peuvent nous être envoyés par e-mail à {$this->emailRepli}.", 'trop_de_fichiers'];
        }
        $valides = [];
        foreach ($fichiers as $f) {
            $nom = self::nomAffichable($f['name']);
            [$ext, $mime, $raison] = $this->controler($f);
            if ($raison !== null) {
                return [[], $this->message($raison, $nom), $raison];
            }
            $valides[] = ['source' => $f['tmp_name'], 'nom' => $nom, 'ext' => $ext, 'mime' => $mime, 'taille' => $f['size']];
        }
        $dossier = $this->stockage->dossier('fichiers');
        $enregistres = [];
        foreach ($valides as $v) {
            $id = bin2hex(random_bytes(16)) . '.' . $v['ext'];
            $cible = $dossier . '/' . $id;
            $ok = $this->exigerTeleversementHttp
                ? move_uploaded_file($v['source'], $cible)
                : copy($v['source'], $cible);
            if (!$ok) {
                foreach ($enregistres as $e) {
                    @unlink($e['chemin']);
                }
                return [[], $this->message('stockage', $v['nom']), 'stockage'];
            }
            @chmod($cible, 0640);
            $enregistres[] = [
                'id' => $id,
                'nom' => $v['nom'],
                'type' => $v['mime'],
                'taille' => (int) filesize($cible),
                'chemin' => $cible,
                'sha256' => (string) hash_file('sha256', $cible),
            ];
        }
        return [$enregistres, null, null];
    }

    /**
     * @param array{name: string, tmp_name: string, error: int, size: int} $f
     * @return array{0: string, 1: string, 2: ?string} [extension, type MIME, raison du refus]
     */
    private function controler(array $f): array
    {
        if (in_array($f['error'], [UPLOAD_ERR_INI_SIZE, UPLOAD_ERR_FORM_SIZE], true)) {
            return ['', '', 'taille'];
        }
        if ($f['error'] !== UPLOAD_ERR_OK) {
            return ['', '', 'envoi_incomplet'];
        }
        if ($this->exigerTeleversementHttp && !is_uploaded_file($f['tmp_name'])) {
            return ['', '', 'source_invalide'];
        }
        $taille = is_file($f['tmp_name']) ? (int) filesize($f['tmp_name']) : 0;
        if ($taille === 0) {
            return ['', '', 'vide'];
        }
        if ($taille > $this->maxOctets) {
            return ['', '', 'taille'];
        }
        $finfo = new \finfo(FILEINFO_MIME_TYPE);
        $mime = (string) $finfo->file($f['tmp_name']);
        $debut = (string) file_get_contents($f['tmp_name'], false, null, 0, 64);
        if (!isset(self::TYPES[$mime]) && self::estHeif($debut)) {
            $mime = 'image/heic'; // anciennes versions de libmagic
        }
        if (!isset(self::TYPES[$mime])) {
            return ['', $mime, 'type'];
        }
        $ext = self::TYPES[$mime];
        $contenu = (string) file_get_contents($f['tmp_name']);

        // Code exécutable caché dans le fichier (fichiers « polyglottes »). Motifs assez
        // longs pour ne pas apparaître par hasard dans des données d'image compressées.
        if (preg_match('/<\?php|<script[\s>]|#!\/(usr\/)?bin\//i', $contenu)) {
            return [$ext, $mime, 'contenu_actif'];
        }
        switch ($ext) {
            case 'jpg':
            case 'png':
                $info = @getimagesizefromstring($contenu);
                $attendu = $ext === 'jpg' ? IMAGETYPE_JPEG : IMAGETYPE_PNG;
                if ($info === false || $info[2] !== $attendu || $info[0] < 1 || $info[1] < 1
                    || $info[0] > 20000 || $info[1] > 20000) {
                    return [$ext, $mime, 'structure'];
                }
                break;
            case 'heic':
                if (!self::estHeif($debut)) {
                    return [$ext, $mime, 'structure'];
                }
                break;
            case 'pdf':
                if (!str_starts_with(ltrim(substr($contenu, 0, 1024)), '%PDF-')) {
                    return [$ext, $mime, 'structure'];
                }
                if ($this->refuserPdfActifs && self::pdfActif($contenu)) {
                    return [$ext, $mime, 'contenu_actif'];
                }
                break;
        }
        return [$ext, $mime, null];
    }

    private static function estHeif(string $debut): bool
    {
        return strlen($debut) >= 12
            && substr($debut, 4, 4) === 'ftyp'
            && in_array(substr($debut, 8, 4), self::MARQUES_HEIF, true);
    }

    /** Un PDF qui contient du JavaScript, des actions de lancement ou des fichiers intégrés est refusé. */
    private static function pdfActif(string $contenu): bool
    {
        // Les noms PDF peuvent être masqués par des échappements « #xx » (/J#61vaScript).
        $normalise = preg_replace_callback('/#([0-9A-Fa-f]{2})/', static fn ($m) => chr((int) hexdec($m[1])), $contenu) ?? $contenu;
        return (bool) preg_match('~/(JavaScript|JS|Launch|EmbeddedFile|RichMedia)[\s/<(\[]~', $normalise);
    }

    public static function nomAffichable(string $nom): string
    {
        $nom = basename(str_replace('\\', '/', $nom));
        $nom = preg_replace('/[^\p{L}\p{N} ._()\-]/u', '_', $nom) ?? 'fichier';
        $nom = trim($nom, ' .');
        return mb_substr($nom !== '' ? $nom : 'fichier', 0, 80);
    }

    private function message(string $raison, string $nom): string
    {
        $mo = (int) round($this->maxOctets / 1048576);
        return match ($raison) {
            'taille' => "Le fichier « $nom » dépasse $mo Mo. Réduisez-le ou envoyez-le par e-mail à {$this->emailRepli}.",
            'type' => "Le fichier « $nom » n'est pas accepté : formats JPG, PNG, HEIC ou PDF uniquement.",
            'vide' => "Le fichier « $nom » est vide. Choisissez-le à nouveau, s'il vous plaît.",
            'contenu_actif', 'structure' => "Le fichier « $nom » n'a pas pu être accepté. Envoyez-le par e-mail à {$this->emailRepli}, nous le regarderons.",
            default => "Le fichier « $nom » n'a pas pu être reçu. Réessayez, ou envoyez-le par e-mail à {$this->emailRepli}.",
        };
    }
}
