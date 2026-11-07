<?php
/** E8 · Acquisition (basique) : demandes et signés par canal, dépenses saisies → CPL, CAC, ROAS, ROI. */
declare(strict_types=1);

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Auth;
use AndyConstruct\Admin\Format;
use AndyConstruct\Admin\Graphiques;
use AndyConstruct\Admin\Http;
use AndyConstruct\Admin\Indicateurs;
use AndyConstruct\Admin\Vue;

return static function (App $app): string {
    $e = static fn ($v) => Vue::e($v);
    $ind = new Indicateurs($app);
    $courant = Indicateurs::moisDe($app->maintenant);
    $periode = Http::get('periode', '3m');
    $options = ['3m' => '3 derniers mois', '12m' => '12 derniers mois'];
    for ($i = 0; $i < 12; $i++) {
        $m = Indicateurs::moisDecale($courant, -$i);
        $options[$m] = ucfirst(Format::mois($m)) . ($i === 0 ? ' (en cours)' : '');
    }
    if (!isset($options[$periode])) {
        $periode = '3m';
    }
    $mois = match ($periode) {
        '3m' => array_map(static fn ($i) => Indicateurs::moisDecale($courant, $i), [-2, -1, 0]),
        '12m' => array_map(static fn ($i) => Indicateurs::moisDecale($courant, $i), range(-11, 0)),
        default => [$periode],
    };
    $a = $ind->acquisition($mois);
    $offres = $ind->offres();
    $cm = $ind->cplMax($app->maintenant, $ind->tauxDemandeOffreTrimestre($courant, $offres), $ind->cohorteOffreSignee($app->maintenant, $offres)['taux'], $courant);
    $cible = $cm['cible'] ?? null;

    $cell = static fn (?float $v, callable $f) => $v === null ? '<span class="discret" title="aucune dépense ou aucun chantier signé">—</span>' : $e($f($v));
    $indicatif = static fn (array $l) => $l['depense'] > 0 && $l['signees'] < 3 ? '<sup title="Moins de 3 chantiers signés : indicatif">*</sup>' : '';
    $ligne = static function (array $l, string $tete = '') use ($e, $cell, $indicatif): string {
        $titre = $tete !== '' ? $tete : $l['libelle'];
        return '<tr><th scope="row">' . $e($titre) . '</th><td class="num">' . ($l['depense'] > 0 ? $e(Format::chf($l['depense'])) : '—') . '</td><td class="num">' . $l['demandes'] . '</td>'
            . '<td class="num">' . $l['qualifiees'] . ($l['qualifiees'] ? ' <span class="discret">(' . $e(Format::pct($l['ab'] / $l['qualifiees'])) . ' A+B)</span>' : '') . '</td>'
            . '<td class="num">' . $l['signees'] . '</td><td class="num">' . $e(Format::chf($l['ca'])) . '</td>'
            . '<td class="num">' . $cell($l['cpl'], [Format::class, 'chf']) . '</td><td class="num">' . $cell($l['cac'], [Format::class, 'chf']) . $indicatif($l) . '</td>'
            . '<td class="num">' . $cell($l['roas'], static fn ($v) => Format::nb($v, 1)) . '</td><td class="num">' . $cell($l['roi'], static fn ($v) => Format::pct($v)) . '</td>'
            . '<td class="num">' . (isset($l['part']) ? $e(Format::pct($l['part'])) : '') . '</td></tr>';
    };
    $payants = array_filter($a['lignes'], static fn ($l) => $l['payant']);
    $autres = array_filter($a['lignes'], static fn ($l) => !$l['payant'] && ($l['demandes'] > 0 || $l['depense'] > 0));
    $table = '<div class="defile" tabindex="0" role="region" aria-label="Tableau, défile horizontalement"><table class="tableau compact"><caption class="sr">Acquisition par canal</caption><thead><tr><th scope="col">Canal</th><th scope="col" class="num">Dépense</th><th scope="col" class="num">Demandes</th><th scope="col" class="num">Qualifiées</th>'
        . '<th scope="col" class="num">Signées</th><th scope="col" class="num">CA signé</th><th scope="col" class="num">CPL</th><th scope="col" class="num">CAC</th><th scope="col" class="num">ROAS</th><th scope="col" class="num">ROI</th><th scope="col" class="num">Part</th></tr></thead><tbody>'
        . implode('', array_map($ligne, $payants))
        . '<tr class="sous-titre-ligne"><th scope="rowgroup" colspan="11">Canaux sans dépense directe</th></tr>'
        . ($autres ? implode('', array_map($ligne, $autres)) : '<tr><td colspan="11" class="discret">Aucune demande d\'un autre canal sur la période.</td></tr>')
        . '</tbody><tfoot>' . $ligne($a['total_payants'], 'Total des canaux payants') . $ligne($a['total'], 'Total') . '</tfoot></table></div>';

    $avert = [];
    if ($a['total']['signees'] < 3) {
        $avert[] = 'Moins de 3 chantiers signés sur la période : CAC, ROAS et ROI sont indicatifs.';
    }
    if ($a['inconnu'] !== null && $a['inconnu'] > 0.2) {
        $avert[] = 'Canal inconnu pour ' . Format::pct($a['inconnu']) . ' des demandes : demandez « Comment nous avez-vous connus ? » à chaque appel.';
    }
    foreach ($mois as $m) {
        if ($m < $courant && $ind->depense([$m], ['google_ads']) <= 0) {
            $avert[] = 'Dépense Google Ads de ' . Format::mois($m) . ' à saisir (Paramètres, Dépenses).';
        }
    }
    $lienDep = Auth::peut($app->utilisateur, 'depenses') ? ' <a href="' . $e(Vue::url('parametres', ['onglet' => 'depenses'])) . '">Saisir les dépenses</a>' : '';
    $html = '<div class="entete-page"><div><h1>Acquisition</h1><p class="sous-titre">' . $e('Par canal d\'arrivée de la demande ; chantiers signés et CA rattachés au canal d\'origine, à la date de signature. Marge brute : ' . Format::pct($a['marge']) . ' (Paramètres).') . '</p></div>'
        . '<form class="actions filtres sans-marge" method="get" action="' . $e(Vue::$base) . '" data-auto><input type="hidden" name="p" value="acquisition">' . Vue::select('periode', 'Période', $periode, $options) . '<button class="btn btn-discret sans-js" type="submit">Afficher</button></form></div>'
        . ($avert ? '<div class="avertissements" role="note"><ul>' . implode('', array_map(static fn ($t) => '<li>' . $e($t) . '</li>', $avert)) . '</ul>' . $lienDep . '</div>' : '')
        . '<section class="panneau" aria-labelledby="t-canaux"><div class="panneau-entete"><h2 id="t-canaux">Par canal</h2><span class="discret">' . $e(implode(', ', array_map([Format::class, 'mois'], $mois))) . '</span></div>' . $table
        . '<p class="petit discret mt">CPL = dépense / demandes · CAC = dépense / chantiers signés · ROAS = CA signé / dépense · ROI = (CA signé × marge brute − dépense) / dépense. « — » : aucune dépense ou aucun chantier signé.</p></section>'
        . '<div class="grille-3 mt">'
        . '<section class="panneau" aria-labelledby="t-b1"><h2 id="t-b1">Demandes par canal</h2>' . Graphiques::barres('Demandes par canal', array_values(array_map(static fn ($l) => ['lib' => $l['libelle'], 'v' => $l['demandes']], array_filter($a['lignes'], static fn ($l) => $l['demandes'] > 0))), static fn ($v) => Format::nb($v)) . '</section>'
        . '<section class="panneau" aria-labelledby="t-b2"><h2 id="t-b2">CA signé par canal</h2>' . Graphiques::barres('CA signé par canal', array_values(array_map(static fn ($l) => ['lib' => $l['libelle'], 'v' => $l['ca']], array_filter($a['lignes'], static fn ($l) => $l['ca'] > 0))), [Format::class, 'chf']) . '</section>'
        . '<section class="panneau" aria-labelledby="t-b3"><h2 id="t-b3">CPL des canaux payants</h2>' . Graphiques::barres('CPL des canaux payants face à la cible', array_values(array_map(static fn ($l) => ['lib' => $l['libelle'], 'v' => $l['cpl']], array_filter($payants, static fn ($l) => $l['cpl'] !== null))), [Format::class, 'chf'], $cible ? ['v' => $cible, 'lib' => 'cible ' . Format::chf($cible)] : null)
        . '<p class="petit discret">' . $e($cm ? 'Cible = CPL max / 3 = ' . Format::chf($cm['max']) . ' / 3 ; CPL max = panier ' . Format::chf($cm['panier']) . ' × marge ' . Format::pct($cm['marge']) . ' × demande→offre ' . Format::pct($cm['tdo']) . ' × offre→signée ' . Format::pct($cm['tos']) . ($cm['sources'] ? ' (' . implode(', ', $cm['sources']) . ')' : '') . '.' : 'Cible non calculable : renseignez la marge brute et le panier de référence.') . '</p></section>'
        . '</div>';
    return Vue::page($app, 'acquisition', 'Acquisition', $html);
};
