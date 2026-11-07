<?php
declare(strict_types=1);

namespace AndyConstruct\Admin;

/**
 * Graphiques SVG produits par le serveur (§3.2) : une teinte ou une rampe de gris
 * ordonnée, jamais deux axes ; chaque marque a un titre (info-bulle native et
 * lecteur d'écran) et chaque graphique un tableau « Voir les données ».
 */
final class Graphiques
{
    private static function e(mixed $v): string
    {
        return Format::e($v);
    }

    /** Demandes par mois, empilées par priorité, avec l'objectif du mois. */
    public static function demandesParMois(array $donnees): string
    {
        $W = 560;
        $H = 230;
        $ml = 34;
        $mr = 10;
        $mt = 14;
        $mb = 28;
        $max = 1;
        foreach ($donnees as $d) {
            $max = max($max, $d['total'], (float) ($d['objectif'] ?? 0));
        }
        $pas = $max <= 5 ? 1 : ($max <= 12 ? 2 : ($max <= 30 ? 5 : 10));
        $ymax = (int) (ceil($max / $pas) * $pas);
        $ph = $H - $mt - $mb;
        $y = static fn (float $v): float => $mt + $ph - $v / $ymax * $ph;
        $n = max(1, count($donnees));
        $bande = ($W - $ml - $mr) / $n;
        $lb = min(46, $bande * .56);
        $s = '<svg class="graphique" viewBox="0 0 ' . $W . ' ' . $H . '" role="img" aria-labelledby="g-dm-t"><title id="g-dm-t">Demandes par mois et par priorité, avec l\'objectif</title>';
        for ($v = 0; $v <= $ymax; $v += $pas) {
            $s .= '<line class="grille" x1="' . $ml . '" x2="' . ($W - $mr) . '" y1="' . round($y($v), 1) . '" y2="' . round($y($v), 1) . '"/><text x="' . ($ml - 6) . '" y="' . round($y($v) + 4, 1) . '" text-anchor="end">' . $v . '</text>';
        }
        $segments = [['C', 'ord-1', 'C'], ['B', 'ord-3', 'B'], ['A', 'ord-5', 'A'], ['hors_cible', 'ord-hc', 'hors cible']];
        foreach ($donnees as $i => $d) {
            $x = $ml + $bande * $i + ($bande - $lb) / 2;
            $base = 0;
            foreach ($segments as [$cle, $classe, $lib]) {
                $v = $d['comptes'][$cle];
                if ($v <= 0) {
                    continue;
                }
                $s .= '<rect class="' . $classe . '" x="' . round($x, 1) . '" y="' . round($y($base + $v), 1) . '" width="' . round($lb, 1) . '" height="' . round($y($base) - $y($base + $v), 1) . '"><title>' . self::e(Format::mois($d['mois']) . ' : ' . $v . ' ' . $lib) . '</title></rect>';
                $base += $v;
            }
            $s .= '<text class="t-fort" x="' . round($x + $lb / 2, 1) . '" y="' . round($y($d['total']) - 4, 1) . '" text-anchor="middle">' . $d['total'] . '</text>';
            if ($d['objectif'] !== null) {
                $s .= '<line class="objectif" x1="' . round($x - 4, 1) . '" x2="' . round($x + $lb + 4, 1) . '" y1="' . round($y((float) $d['objectif']), 1) . '" y2="' . round($y((float) $d['objectif']), 1) . '"><title>' . self::e('Objectif ' . Format::mois($d['mois']) . ' : ' . Format::nb($d['objectif'])) . '</title></line>';
            }
            $s .= '<text x="' . round($x + $lb / 2, 1) . '" y="' . ($H - 8) . '" text-anchor="middle">' . self::e(Format::moisCourt($d['mois'])) . '</text>';
        }
        $s .= '<line class="axe" x1="' . $ml . '" x2="' . ($W - $mr) . '" y1="' . round($y(0), 1) . '" y2="' . round($y(0), 1) . '"/></svg>';
        $legende = '<ul class="legende"><li><i class="l-ord-5"></i>A</li><li><i class="l-ord-3"></i>B</li><li><i class="l-ord-1"></i>C</li><li><i class="l-ord-hc"></i>Hors cible</li><li><i class="trait"></i>Objectif</li></ul>';
        $table = Vue::tableDonnees('Demandes par mois', ['Mois', 'Demandes', 'A', 'B', 'C', 'Hors cible', 'Objectif'], array_map(static fn ($d) => [
            Format::mois($d['mois']), $d['total'], $d['comptes']['A'], $d['comptes']['B'], $d['comptes']['C'], $d['comptes']['hors_cible'], $d['objectif'] === null ? '—' : Format::nb($d['objectif']),
        ], $donnees));
        return $legende . $s . $table;
    }

    /** Entonnoir horizontal : une barre par étape, passage d'une étape à l'autre. */
    public static function entonnoir(array $etapes): string
    {
        $W = 560;
        $lab = 150;
        $hBar = 26;
        $gap = 12;
        $H = count($etapes) * ($hBar + $gap) + 4;
        $max = max(1, $etapes[0][1] ?? 1);
        $s = '<svg class="graphique" viewBox="0 0 ' . $W . ' ' . $H . '" role="img" aria-labelledby="g-ent-t"><title id="g-ent-t">Entonnoir des demandes, de l\'enregistrement à la signature</title>';
        foreach ($etapes as $i => [$lib, $v]) {
            $y = $i * ($hBar + $gap);
            $w = max(2, ($W - $lab - 90) * $v / $max);
            $passage = $i > 0 && $max > 0 ? Format::pct($v / $max) : '';
            $s .= '<text x="0" y="' . ($y + 17) . '">' . self::e($lib) . '</text>'
                . '<rect class="ord-' . ($i + 1) . '" x="' . $lab . '" y="' . $y . '" width="' . round($w, 1) . '" height="' . $hBar . '"><title>' . self::e($lib . ' : ' . $v . ($passage ? ' (' . $passage . ' des demandes)' : '')) . '</title></rect>'
                . '<text class="t-fort" x="' . round($lab + $w + 8, 1) . '" y="' . ($y + 17) . '">' . $v . ($passage ? ' <tspan class="t-leger">(' . self::e($passage) . ')</tspan>' : '') . '</text>';
        }
        return $s . '</svg>' . Vue::tableDonnees('Entonnoir', ['Étape', 'Demandes', 'Part des demandes'], array_map(static fn ($e, $i) => [
            $e[0], $e[1], $i > 0 && $max > 0 ? Format::pct($e[1] / $max) : '—',
        ], $etapes, array_keys($etapes)));
    }

    /** Barres horizontales classées (Acquisition). */
    public static function barres(string $titre, array $items, callable $format, ?array $cible = null): string
    {
        if ($items === []) {
            return '<p class="petit discret">Aucune donnée sur la période.</p>';
        }
        usort($items, static fn ($a, $b) => $b['v'] <=> $a['v']);
        $W = 480;
        $lab = 150;
        $val = 90;
        $h = 20;
        $gap = 8;
        $H = max(1, count($items)) * ($h + $gap) + ($cible ? 18 : 0);
        $max = max(1, ...array_map(static fn ($i) => (float) $i['v'], $items), ...[$cible['v'] ?? 0]);
        $x = static fn (float $v): float => $lab + ($W - $lab - $val) * $v / $max;
        $id = 'g-' . substr(md5($titre), 0, 6);
        $s = '<svg class="graphique" viewBox="0 0 ' . $W . ' ' . $H . '" role="img" aria-labelledby="' . $id . '"><title id="' . $id . '">' . self::e($titre) . '</title>';
        foreach ($items as $i => $it) {
            $y = $i * ($h + $gap) + ($cible ? 16 : 0);
            $s .= '<text x="0" y="' . ($y + 14) . '">' . self::e($it['lib']) . '</text>';
            if ($it['v'] > 0) {
                $s .= '<rect class="serie" x="' . $lab . '" y="' . $y . '" width="' . round($x((float) $it['v']) - $lab, 1) . '" height="' . $h . '"><title>' . self::e($it['lib'] . ' : ' . $format($it['v'])) . '</title></rect>';
            }
            $s .= '<text class="t-fort" x="' . round($x((float) $it['v']) + 6, 1) . '" y="' . ($y + 14) . '">' . self::e($format($it['v'])) . '</text>';
        }
        if ($cible) {
            $cx = round($x((float) $cible['v']), 1);
            $s .= '<line class="objectif" x1="' . $cx . '" x2="' . $cx . '" y1="12" y2="' . $H . '"/><text x="' . $cx . '" y="10" text-anchor="middle">' . self::e($cible['lib']) . '</text>';
        }
        return $s . '</svg>' . Vue::tableDonnees($titre, ['Canal', 'Valeur'], array_map(static fn ($i) => [$i['lib'], $format($i['v'])], $items));
    }
}
