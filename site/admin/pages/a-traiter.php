<?php
/** E2 · À traiter (téléphone d'abord) : qui rappeler, dans quel ordre, avec Appeler et Résultat sur chaque ligne. */
declare(strict_types=1);

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Demandes;
use AndyConstruct\Admin\Format;
use AndyConstruct\Admin\Http;
use AndyConstruct\Admin\Vue;
use AndyConstruct\Api\Canaux;

return static function (App $app): string {
    $e = static fn ($v) => Vue::e($v);
    $toutes = Http::get('vue') === 'toutes';
    $moi = $app->utilisateur['id'];
    $s = $app->demandes->aTraiter($toutes ? null : $moi);
    $retour = Vue::url('a-traiter', $toutes ? ['vue' => 'toutes'] : []);

    $quoi = static fn (array $d): string => $e(Demandes::libelleTravaux($d) . ($d['commune'] ? ', ' . $d['commune'] : ''))
        . '<span class="org">' . $e(Canaux::libelle($d['canal_eff']) . ($d['canal'] === 'telephone' ? ' (appel)' : '') . ($d['associe_nom'] ? ', ' . $d['associe_nom'] : '')) . '</span>';
    $appeler = static function (array $d, bool $principal = false) use ($e): string {
        if ($d['telephone_e164']) {
            return '<a class="btn btn-petit' . ($principal ? ' btn-principal' : '') . '" href="tel:' . $e($d['telephone_e164']) . '" data-appel="' . $e($d['ref']) . '">Appeler<span class="sr"> ' . $e($d['nom_complet']) . '</span></a>';
        }
        return $d['email'] ? '<a class="btn btn-petit" href="mailto:' . $e($d['email']) . '">E-mail<span class="sr"> à ' . $e($d['nom_complet']) . '</span></a>' : '';
    };
    // « Résultat » : formulaire direct (sans JavaScript) vers la fiche, ou feuille après l'appel (admin.js).
    $resultat = static function (array $d) use ($e, $app, $retour): string {
        if ($d['statut'] !== 'nouvelle') {
            return '<a class="btn btn-petit btn-discret" href="' . $e(Vue::url('fiche', ['ref' => $d['ref']])) . '">Ouvrir<span class="sr"> la fiche de ' . $e($d['nom_complet']) . '</span></a>';
        }
        $f = static fn (string $action, string $lib) => '<form method="post" action="' . $e(Vue::url('fiche', ['ref' => $d['ref']])) . '">' . Vue::csrf($app)
            . '<input type="hidden" name="op" value="statut"><input type="hidden" name="action" value="' . $action . '"><input type="hidden" name="version" value="' . (int) $d['version'] . '"><input type="hidden" name="retour" value="' . $e($retour) . '">'
            . '<button class="btn btn-petit btn-discret" type="submit">' . $e($lib) . '<span class="sr"> (' . $e($d['nom_complet']) . ')</span></button></form>';
        return '<details class="menu-resultat" data-ref="' . $e($d['ref']) . '"><summary class="btn btn-petit btn-discret">Résultat<span class="sr"> de l\'appel à ' . $e($d['nom_complet']) . '</span></summary><div class="menu-resultat-corps">'
            . $f('contact_etabli', "J'ai eu la personne") . ($d['tentatives_appel'] < 3 ? $f('pas_de_reponse', 'Pas de réponse') : '')
            . '<a class="btn btn-petit btn-discret" href="' . $e(Vue::url('fiche', ['ref' => $d['ref']])) . '">Autre (fiche)</a></div></details>';
    };
    $ligne = static function (array $d, string $quoi, string $echeance, string $boutons, bool $retard = false) use ($e): string {
        return '<li class="ligne-travail' . ($retard ? ' retard' : '') . '"><div class="qui">' . Vue::prio($d['priorite_eff']) . '<div>' . Vue::nomLien($d) . '</div></div>'
            . '<div class="quoi">' . $quoi . '</div><div class="echeance-cel">' . $echeance . '</div><div class="boutons">' . $boutons . '</div></li>';
    };
    $section = static function (string $id, string $titre, array $items, callable $rendu, string $vide) use ($e): string {
        return '<section class="section-travail" aria-labelledby="' . $id . '"><h2 id="' . $id . '">' . $e($titre) . ' <span class="compte">' . count($items) . '</span></h2>'
            . ($items ? '<ul class="liste-travail">' . implode('', array_map($rendu, $items)) . '</ul>' : '<p class="vide">' . $e($vide) . '</p>') . '</section>';
    };

    $prochaine = null;
    foreach (array_merge($s['rappeler'], $s['tentatives']) as $d) {
        if ($d['echeance'] && ($prochaine === null || $d['echeance'] < $prochaine)) {
            $prochaine = $d['echeance'];
        }
    }
    $html = '<div class="entete-page"><div><h1>À traiter</h1><p class="sous-titre">' . $e(ucfirst(Format::dateL($app->maintenant)) . ', ' . Format::heure($app->maintenant)) . '. Les retards de tous les associés sont toujours affichés.</p></div>'
        . '<div class="actions"><div class="bascule" role="group" aria-label="Demandes affichées">'
        . '<a href="' . $e(Vue::url('a-traiter')) . '"' . (!$toutes ? ' aria-current="page"' : '') . '>Mes demandes</a>'
        . '<a href="' . $e(Vue::url('a-traiter', ['vue' => 'toutes'])) . '"' . ($toutes ? ' aria-current="page"' : '') . '>Toutes</a></div></div></div>'
        . $section('s-retard', 'En retard', $s['retards'], static fn ($d) => $ligne($d, $quoi($d), Vue::echeance($d, $app), $appeler($d, true) . $resultat($d), true), 'Aucun retard.')
        . $section('s-rappel', 'À rappeler', $s['rappeler'], static fn ($d) => $ligne($d, $quoi($d), Vue::echeance($d, $app), $appeler($d) . $resultat($d)),
            'Rien à rappeler pour l\'instant. Les nouvelles demandes arrivent ici.' . ($prochaine ? ' Prochaine échéance : ' . Format::dateH($prochaine) . '.' : ''))
        . $section('s-tent', 'Tentatives à refaire', $s['tentatives'], static fn ($d) => $ligne($d, $quoi($d) . '<span class="org">' . $e($d['tentatives_appel'] . ' appel' . ($d['tentatives_appel'] > 1 ? 's' : '') . ' sans réponse') . '</span>', Vue::echeance($d, $app), $appeler($d) . $resultat($d)), 'Aucune tentative en attente.')
        . $section('s-visites', 'Visites aujourd\'hui et demain', $s['visites'], static fn ($d) => $ligne($d, $e(Demandes::libelleTravaux($d)) . '<span class="org">' . $e(($d['visite']['adresse'] ?: $d['commune']) . ($d['associe_nom'] ? ', ' . $d['associe_nom'] : '')) . '</span>',
            '<span class="gras">' . $e(Format::dateH(Format::t($d['visite']['prevue_le']))) . '</span>', $appeler($d) . $resultat($d)), 'Aucune visite prévue.')
        . $section('s-offres', 'Offres : appels et décisions', $s['offres'], static fn ($d) => $ligne($d, $e('Offre ' . Format::chf($d['montant']) . ' du ' . Format::dateC(Format::t($d['offre']['envoyee_le'])) . ', J+' . $d['relance']['jours'])
            . '<span class="org">' . $e($d['relance']['etape'] . ' relance' . ($d['relance']['etape'] > 1 ? 's' : '') . ' prévue' . ($d['relance']['etape'] > 1 ? 's' : '') . ' (J+3, J+10, J+21)') . '</span>',
            '<span class="' . ($d['relance']['decision'] ? 'gras' : '') . '">' . $e($d['relance']['texte']) . '</span>', $appeler($d) . $resultat($d)), 'Aucune offre à traiter aujourd\'hui.')
        . $section('s-hc', 'Hors cible à valider', $s['hors_cible'], static fn ($d) => $ligne($d, $quoi($d), Vue::echeance($d, $app), '<a class="btn btn-petit btn-discret" href="' . $e(Vue::url('fiche', ['ref' => $d['ref']])) . '">Valider<span class="sr"> ' . $e($d['nom_complet']) . '</span></a>'), 'Aucune demande hors cible.');

    // Feuille « Résultat de l'appel » ouverte au retour dans l'onglet après un appel (admin.js).
    $html .= '<dialog id="feuille-appel" aria-labelledby="feuille-appel-titre"><div class="dialogue-corps"><h2 id="feuille-appel-titre">Résultat de l\'appel</h2><p class="petit discret" id="feuille-appel-qui"></p><div class="choix-appel" id="feuille-appel-choix"></div></div>'
        . '<div class="dialogue-pied"><button class="btn btn-discret" type="button" data-fermer>Plus tard</button></div></dialog>';
    return Vue::page($app, 'a-traiter', 'À traiter', $html);
};
