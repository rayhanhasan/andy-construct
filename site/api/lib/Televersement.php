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
                        'tmp_name' => is_string($f['tmp_name'][$i] ?? null) ? $f['tmp_name'][$i] : '',
                        'error' => is_scalar($f['error'][$i] ?? null) ? (int) $f['error'][$i] : UPLOAD_ERR_NO_FILE,
                        'size' => is_scalar($f['size'][$i] ?? null) ? (int) $f['size'][$i] : 0,
                    ];
                }
            } else {
                $liste[] = [
                    'name' => is_string($f['name'] ?? null) ? $f['name'] : '',
                    'tmp_name' => is_string($f['tmp_name'] ?? null) ? $f['tmp_name'] : '',
                    'error' => is_scalar($f['error'] ?? null) ? (int) $f['error'] : UPLOAD_ERR_NO_FILE,
                    'size' => is_scalar($f['size'] ?? null) ? (int) $f['size'] : 0,
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

    /** Volume décompressé inspecté au plus par PDF (au-delà : refus prudent, bombe de décompression). */
    private const PDF_BUDGET_DECOMPRESSION = 256 * 1048576;

    /** Un nom PDF se termine sur un blanc ou un délimiteur, dont « > », « ] » et « % » (commentaire). */
    private const FIN_NOM = '(?![^\s\0()<>\[\]{}/%])';

    /**
     * Un PDF qui contient du JavaScript, des actions de lancement, des fichiers intégrés,
     * du contenu riche ou un formulaire XFA est refusé.
     *
     * Ces objets peuvent être cachés dans des flux compressés (FlateDecode, flux d'objets
     * /ObjStm, filtres en cascade) : les flux zlib qui contiennent des objets ou du texte
     * sont décompressés (volume plafonné) et inspectés ; les images sont ignorées. Un PDF
     * qu'on ne peut pas inspecter (filtres LZW / ASCII85 / ASCIIHex, flux d'objets
     * chiffrés, bombe de décompression) est refusé par prudence : le visiteur est invité à
     * l'envoyer par e-mail.
     */
    public static function pdfActif(string $contenu): bool
    {
        $normalise = self::normaliserNomsPdf($contenu);
        if (preg_match('~/(JavaScript|JS|Launch|EmbeddedFiles?|RichMedia|XFA)' . self::FIN_NOM . '~', $normalise)) {
            return true;
        }
        if (preg_match('~/(LZWDecode|ASCII85Decode|ASCIIHexDecode|LZW|A85|AHx)' . self::FIN_NOM . '~', $normalise)
            || (str_contains($normalise, '/Encrypt') && str_contains($normalise, '/ObjStm'))) {
            return true;
        }
        $budget = self::PDF_BUDGET_DECOMPRESSION;
        $pos = 0;
        while (($debut = strpos($contenu, 'stream', $pos)) !== false) {
            $pos = $debut + 6;
            if ($debut >= 3 && substr($contenu, $debut - 3, 3) === 'end') {
                continue;
            }
            $depart = $pos + (($contenu[$pos] ?? '') === "\r" ? 1 : 0);
            $depart += ($contenu[$depart] ?? '') === "\n" ? 1 : 0;
            if (self::fluxActif($contenu, $depart, $budget, 0)) {
                return true;
            }
        }
        return false;
    }

    private static function normaliserNomsPdf(string $contenu): string
    {
        // Les noms PDF peuvent être masqués par des échappements « #xx » (/J#61vaScript).
        return preg_replace_callback('/#([0-9A-Fa-f]{2})/', static fn ($m) => chr((int) hexdec($m[1])), $contenu) ?? $contenu;
    }

    private static function enteteZlib(string $donnees, int $depart): bool
    {
        $b0 = ord($donnees[$depart] ?? "\0");
        $b1 = ord($donnees[$depart + 1] ?? "\0");
        return ($b0 & 0x0F) === 8 && (($b0 << 8) | $b1) % 31 === 0;
    }

    /**
     * Décompresse par morceaux le flux zlib qui commence à $depart (s'il y en a un) et
     * l'inspecte. La fin est celle du flux zlib, pas le mot « endstream » (que des
     * données non compressées pourraient contenir pour tronquer l'inspection).
     * Les noms courts (/JS) ne sont pas cherchés dans le décompressé : une action
     * JavaScript exige aussi « /S /JavaScript », et « /JS » apparaîtrait par hasard
     * dans des données binaires.
     *
     * @return bool true si un nom actif est trouvé ou si le budget est épuisé
     */
    private static function fluxActif(string $donnees, int $depart, int &$budget, int $niveau): bool
    {
        if (!self::enteteZlib($donnees, $depart)) {
            return false;
        }
        $contexte = @inflate_init(ZLIB_ENCODING_DEFLATE);
        if ($contexte === false) {
            return false;
        }
        $motif = '~/(JavaScript|Launch|EmbeddedFiles?|RichMedia|XFA)' . self::FIN_NOM . '~';
        $mode = null; // null : indécis ; texte : objets ou opérateurs ; imbrique : zlib dans zlib
        $tampon = '';
        $longueur = strlen($donnees);
        for ($i = $depart; $i < $longueur; $i += 8192) {
            $morceau = @inflate_add($contexte, substr($donnees, $i, 8192), ZLIB_SYNC_FLUSH);
            if ($morceau === false) {
                break; // données corrompues : on inspecte ce qui a été décompressé
            }
            $budget -= strlen($morceau);
            if ($budget < 0) {
                return true;
            }
            $tampon .= $morceau;
            $fini = inflate_get_status($contexte) === ZLIB_STREAM_END;
            if ($mode === null) {
                // Un flux d'objets commence par des paires d'entiers (après d'éventuels blancs ou
                // commentaires) ; une image, par des octets quelconques : elle est ignorée.
                $debut = preg_replace('/^(?:[\s\0]|%[^\r\n]*(?:\r\n?|\n))*/', '', $tampon) ?? '';
                if (($debut === '' || $debut[0] === '%') && !$fini && strlen($tampon) < 1048576) {
                    continue;
                }
                $mode = self::enteteZlib($tampon, 0) && $niveau < 3 ? 'imbrique'
                    : (($debut === '' || $debut[0] === '%' || preg_match('/^[+\-]?\d/', $debut)) ? 'texte' : 'image');
                if ($mode === 'image') {
                    return false;
                }
            }
            if ($mode === 'texte') {
                if (preg_match($motif, self::normaliserNomsPdf($tampon))) {
                    return true;
                }
                $tampon = substr($tampon, -64); // chevauchement : un nom à cheval sur deux morceaux
            } elseif ($mode === 'imbrique' && strlen($tampon) > 32 * 1048576) {
                return true; // filtre en cascade démesuré : refus prudent (mémoire)
            }
            if ($fini) {
                break;
            }
        }
        if ($mode === 'imbrique') {
            return self::fluxActif($tampon, 0, $budget, $niveau + 1);
        }
        if ($mode === null && $tampon !== '') {
            return self::enteteZlib($tampon, 0) && $niveau < 3
                ? self::fluxActif($tampon, 0, $budget, $niveau + 1)
                : (bool) preg_match($motif, self::normaliserNomsPdf($tampon));
        }
        return false;
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
