<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Rattache un NPA ou une commune saisie librement à une zone de scoring.
 *
 * Ordre : NPA fourni (champ « npa » ou 4 chiffres dans « commune »), puis nom de
 * commune exact, puis correspondance approchée (distance de Levenshtein).
 */
final class Localite
{
    /** @param array<string, mixed> $donnees contenu de data/zones.json */
    public function __construct(private array $donnees)
    {
    }

    public static function depuisFichier(string $chemin): self
    {
        $json = json_decode((string) file_get_contents($chemin), true, 32, JSON_THROW_ON_ERROR);
        return new self($json);
    }

    /**
     * @return array{npa: ?string, zone: int|string, canton: ?string, methode: string, commune_reconnue: ?string}
     */
    public function resoudre(string $npa, string $commune): array
    {
        $npa = trim($npa);
        if ($npa === '' && preg_match('/(?<!\d)([1-9]\d{3})(?!\d)/', $commune, $m)) {
            $npa = $m[1];
        }
        if ($npa !== '' && preg_match('/^[1-9]\d{3}$/', $npa)) {
            $r = $this->parNpa((int) $npa);
            return ['npa' => $npa, 'zone' => $r['zone'], 'canton' => $r['canton'], 'methode' => 'npa', 'commune_reconnue' => null];
        }

        $nom = self::normaliserNom(preg_replace('/\d+/', ' ', $commune) ?? '');
        if ($nom === '') {
            return ['npa' => null, 'zone' => 'inconnue', 'canton' => null, 'methode' => 'aucune', 'commune_reconnue' => null];
        }
        if (in_array($nom, $this->donnees['hors_suisse'] ?? [], true)) {
            return ['npa' => null, 'zone' => 'hors', 'canton' => null, 'methode' => 'commune-exacte', 'commune_reconnue' => $nom];
        }
        $communes = $this->donnees['communes'] ?? [];
        $methode = 'commune-exacte';
        $trouve = $communes[$nom] ?? null;
        $cle = $nom;
        if ($trouve === null) {
            [$cle, $trouve] = $this->approcher($nom, $communes);
            $methode = 'commune-approchee';
        }
        if ($trouve === null) {
            return ['npa' => null, 'zone' => 'inconnue', 'canton' => null, 'methode' => 'inconnue', 'commune_reconnue' => null];
        }
        $r = $this->parNpa((int) $trouve);
        return ['npa' => (string) $trouve, 'zone' => $r['zone'], 'canton' => $r['canton'], 'methode' => $methode, 'commune_reconnue' => $cle];
    }

    /** @return array{zone: int|string, canton: ?string} */
    public function parNpa(int $npa): array
    {
        foreach ($this->donnees['plages'] ?? [] as $plage) {
            if ($npa >= $plage['de'] && $npa <= $plage['a']) {
                return ['zone' => $plage['zone'], 'canton' => $plage['canton'] ?? null];
            }
        }
        $defaut = ($npa >= 1000 && $npa <= 2999)
            ? ($this->donnees['defaut_1000_2999'] ?? ['zone' => 3, 'canton' => null])
            : ($this->donnees['defaut_autres'] ?? ['zone' => 'hors', 'canton' => null]);
        return ['zone' => $defaut['zone'], 'canton' => $defaut['canton']];
    }

    /**
     * @param array<string, int> $communes
     * @return array{0: ?string, 1: ?int}
     */
    private function approcher(string $nom, array $communes): array
    {
        $longueur = strlen($nom);
        if ($longueur < 5) {
            return [null, null];
        }
        $seuil = $longueur >= 9 ? 2 : 1;
        $meilleure = null;
        $distanceMin = PHP_INT_MAX;
        $exaequo = false;
        foreach ($communes as $cle => $npa) {
            if (abs(strlen($cle) - $longueur) > $seuil) {
                continue;
            }
            $d = levenshtein($nom, $cle);
            if ($d < $distanceMin) {
                $distanceMin = $d;
                $meilleure = $cle;
                $exaequo = false;
            } elseif ($d === $distanceMin && $communes[$cle] !== $communes[$meilleure]) {
                $exaequo = true;
            }
        }
        if ($meilleure === null || $distanceMin > $seuil || $exaequo) {
            return [null, null];
        }
        return [$meilleure, (int) $communes[$meilleure]];
    }

    /** « Chêne-Bourg (GE) » → « chene bourg » ; « St-Légier » → « saint legier ». */
    public static function normaliserNom(string $nom): string
    {
        $nom = mb_strtolower(trim($nom));
        $nom = strtr($nom, [
            'à' => 'a', 'â' => 'a', 'ä' => 'a', 'á' => 'a', 'ã' => 'a', 'å' => 'a',
            'ç' => 'c', 'é' => 'e', 'è' => 'e', 'ê' => 'e', 'ë' => 'e',
            'î' => 'i', 'ï' => 'i', 'í' => 'i', 'ì' => 'i',
            'ô' => 'o', 'ö' => 'o', 'ó' => 'o', 'ò' => 'o', 'õ' => 'o',
            'ù' => 'u', 'û' => 'u', 'ü' => 'u', 'ú' => 'u', 'ÿ' => 'y', 'ñ' => 'n',
            'œ' => 'oe', 'æ' => 'ae', 'ß' => 'ss', '’' => ' ', "'" => ' ',
        ]);
        $nom = preg_replace('/[^a-z0-9]+/', ' ', $nom) ?? '';
        $nom = trim(preg_replace('/\s+/', ' ', $nom) ?? '');
        $nom = preg_replace('/\b(ch|suisse|switzerland|schweiz)$/', '', $nom) ?? $nom;
        $nom = trim(preg_replace('/\s(ge|vd|ne|fr|vs|ju|be)$/', '', $nom) ?? $nom);
        $nom = preg_replace('/^st /', 'saint ', $nom) ?? $nom;
        $nom = preg_replace('/^ste /', 'sainte ', $nom) ?? $nom;
        $nom = preg_replace('/ st /', ' saint ', $nom) ?? $nom;
        $nom = preg_replace('/ ste /', ' sainte ', $nom) ?? $nom;
        return trim($nom);
    }
}
