<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/** Un e-mail à envoyer (contenu déjà rendu). */
final class Message
{
    public string $categorie = 'divers';
    public string $sujet = '';
    public string $texte = '';
    public ?string $html = null;
    /** @var list<array{0: string, 1: string}> [adresse, nom] */
    public array $a = [];
    /** @var array{0: string, 1: string}|null */
    public ?array $repondreA = null;
    /** @var list<array{chemin: string, nom: string, type: string}> */
    public array $pieces = [];
    public string $ref = '';

    /** @return array<string, mixed> */
    public function versTableau(): array
    {
        return get_object_vars($this);
    }

    /** @param array<string, mixed> $t */
    public static function depuisTableau(array $t): self
    {
        $m = new self();
        foreach (get_object_vars($m) as $cle => $_) {
            if (array_key_exists($cle, $t)) {
                $m->$cle = $t[$cle];
            }
        }
        return $m;
    }

    /** Valeur sûre pour un en-tête : ni retour à la ligne, ni caractère de contrôle. */
    public static function entete(string $v, int $max = 180): string
    {
        $v = preg_replace('/[\r\n\t\0]+/', ' ', $v) ?? '';
        $v = preg_replace('/\p{C}/u', '', $v) ?? '';
        $v = trim(preg_replace('/\s{2,}/', ' ', $v) ?? '');
        return mb_substr($v, 0, $max);
    }
}
