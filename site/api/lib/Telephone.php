<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Normalisation des numéros de téléphone (format E.164).
 *
 * Accepte toutes les écritures courantes : 022 771 20 15, 022/771.20.15,
 * +41 22 771 20 15, 0041 22 771 20 15, +41 (0)22 771 20 15, 786311434.
 * Les numéros étrangers (+33…) sont acceptés et signalés comme tels.
 */
final class Telephone
{
    /**
     * @return array{e164: string, affiche: string, suisse: bool, mobile: bool}|null
     */
    public static function normaliser(string $saisie): ?array
    {
        $saisie = trim($saisie);
        if ($saisie === '' || mb_strlen($saisie) > 30) {
            return null;
        }
        // Lettres interdites (hors extension « (0) »), caractères autorisés uniquement.
        $saisie = str_replace(['(0)', '( 0 )'], '', $saisie);
        if (!preg_match('/^[+0-9 ().\/\-]+$/', $saisie)) {
            return null;
        }
        $plus = str_starts_with(ltrim($saisie), '+');
        $chiffres = preg_replace('/\D/', '', $saisie) ?? '';

        if ($plus) {
            $international = $chiffres;
        } elseif (str_starts_with($chiffres, '00')) {
            $international = substr($chiffres, 2);
        } elseif (str_starts_with($chiffres, '0')) {
            $international = '41' . substr($chiffres, 1);
        } elseif (strlen($chiffres) === 9) {
            $international = '41' . $chiffres; // numéro suisse saisi sans le 0
        } else {
            return null;
        }

        if (str_starts_with($international, '41')) {
            $national = substr($international, 2);
            if (strlen($national) === 10 && $national[0] === '0') {
                $national = substr($national, 1); // +41 0xx…
            }
            if (!preg_match('/^[2-9]\d{8}$/', $national)) {
                return null;
            }
            return [
                'e164' => '+41' . $national,
                'affiche' => self::afficherSuisse($national),
                'suisse' => true,
                'mobile' => (bool) preg_match('/^7[4-9]/', $national),
            ];
        }

        if (!preg_match('/^[1-9]\d{7,14}$/', $international)) {
            return null;
        }
        return [
            'e164' => '+' . $international,
            'affiche' => '+' . $international,
            'suisse' => false,
            'mobile' => false,
        ];
    }

    private static function afficherSuisse(string $national): string
    {
        // Numéros de service (0800, 084x, 090x) : 0800 123 456.
        if (preg_match('/^(800|84[0248]|90[016])(\d{3})(\d{3})$/', $national, $m)) {
            return '0' . $m[1] . ' ' . $m[2] . ' ' . $m[3];
        }
        return sprintf(
            '0%s %s %s %s',
            substr($national, 0, 2),
            substr($national, 2, 3),
            substr($national, 5, 2),
            substr($national, 7, 2)
        );
    }
}
