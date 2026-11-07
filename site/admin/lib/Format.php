<?php
declare(strict_types=1);

namespace AndyConstruct\Admin;

use AndyConstruct\Api\Base;

/** Formats d'affichage (fr-CH) : dates en Europe/Zurich, CHF avec apostrophe, durées. */
final class Format
{
    public const JOURS_COURTS = ['dim.', 'lun.', 'mar.', 'mer.', 'jeu.', 'ven.', 'sam.'];
    public const JOURS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
    public const MOIS = ['', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
    public const MOIS_COURTS = ['', 'janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.'];

    public static function e(mixed $v): string
    {
        return htmlspecialchars((string) $v, ENT_QUOTES | ENT_SUBSTITUTE | ENT_HTML5, 'UTF-8');
    }

    public static function t(?string $utc): ?\DateTimeImmutable
    {
        return Base::local($utc);
    }

    public static function heure(\DateTimeImmutable $t): string
    {
        $m = (int) $t->format('i');
        return $t->format('G') . ' h' . ($m ? ' ' . $t->format('i') : '');
    }

    /** 22.04 */
    public static function dateC(?\DateTimeImmutable $t): string
    {
        return $t === null ? '—' : $t->format('d.m');
    }

    /** 22.04.2027 */
    public static function dateA(?\DateTimeImmutable $t): string
    {
        return $t === null ? '—' : $t->format('d.m.Y');
    }

    /** jeu. 22.04, 9 h 40 */
    public static function dateH(?\DateTimeImmutable $t): string
    {
        return $t === null ? '—' : self::JOURS_COURTS[(int) $t->format('w')] . ' ' . $t->format('d.m') . ', ' . self::heure($t);
    }

    /** jeudi 22 avril 2027 */
    public static function dateL(\DateTimeImmutable $t): string
    {
        return self::JOURS[(int) $t->format('w')] . ' ' . $t->format('j') . ' ' . self::MOIS[(int) $t->format('n')] . ' ' . $t->format('Y');
    }

    /** « avril 2027 » pour « 2027-04 » */
    public static function mois(string $mois): string
    {
        [$a, $m] = array_map('intval', explode('-', $mois));
        return self::MOIS[$m] . ' ' . $a;
    }

    public static function moisCourt(string $mois): string
    {
        [, $m] = array_map('intval', explode('-', $mois));
        return self::MOIS_COURTS[$m];
    }

    /** 12'500 ; 1'234,5 */
    public static function nb(float|int|null $n, int $decimales = 0): string
    {
        if ($n === null || is_nan((float) $n) || is_infinite((float) $n)) {
            return '—';
        }
        return number_format((float) $n, $decimales, ',', "'");
    }

    public static function chf(float|int|null $n): string
    {
        return $n === null ? '—' : 'CHF ' . self::nb(round((float) $n));
    }

    public static function pct(?float $x, int $decimales = 0): string
    {
        return $x === null || is_nan($x) || is_infinite($x) ? '—' : self::nb($x * 100, $decimales) . ' %';
    }

    /** 95 → « 1 h 35 », 40 → « 40 min » */
    public static function duree(?float $minutes): string
    {
        if ($minutes === null) {
            return '—';
        }
        $m = (int) round($minutes);
        if ($m < 60) {
            return $m . ' min';
        }
        $h = intdiv($m, 60);
        $r = $m % 60;
        return $h . ' h' . ($r ? ' ' . str_pad((string) $r, 2, '0', STR_PAD_LEFT) : '');
    }

    /** Montant saisi (« 12'500 », « 12 500.50 », « 12500,5 ») → nombre, ou null. */
    public static function lireMontant(mixed $v): ?float
    {
        if (!is_string($v) && !is_numeric($v)) {
            return null;
        }
        $s = str_replace(["'", '’', ' ', "\u{00A0}", "\u{202F}", 'CHF', 'chf'], '', (string) $v);
        $s = str_replace(',', '.', $s);
        if (!preg_match('/^\d{1,8}(\.\d{1,2})?$/', $s)) {
            return null;
        }
        return (float) $s;
    }
}
