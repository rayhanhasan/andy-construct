<?php
/** E3 · Demandes, liste filtrable · E4 · Demandes, colonnes par statut (?vue=colonnes). */
declare(strict_types=1);

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Auth;
use AndyConstruct\Admin\Composants;
use AndyConstruct\Admin\Demandes;
use AndyConstruct\Admin\Format;
use AndyConstruct\Admin\Http;
use AndyConstruct\Admin\Vue;
use AndyConstruct\Api\Base;
use AndyConstruct\Api\Canaux;

return static function (App $app): string {
    $e = static fn ($v) => Vue::e($v);
    $colonnes = Http::get('vue') === 'colonnes';
    $f = [];
    foreach (['q', 'periode', 'statut', 'priorite', 'canal', 'type_client', 'associe', 'retard', 'tri'] as $k) {
        $f[$k] = mb_substr(Http::get($k), 0, 80);
    }
    if ($f['q'] !== '' && $f['statut'] === '') {
        $f['statut'] = 'toutes';
    }
    $associes = $app->base->tous("SELECT id, nom_affiche FROM utilisateur WHERE actif = 1 AND role IN ('associe', 'secretariat') ORDER BY nom_affiche");
    $optAssocies = ['' => 'Tous', 'moi' => 'Moi'];
    foreach ($associes as $a) {
        $optAssocies[(string) $a['id']] = $a['nom_affiche'];
    }
    $filtres = '<form class="filtres" method="get" action="' . $e(Vue::$base) . '" data-auto><input type="hidden" name="p" value="demandes">' . ($colonnes ? '<input type="hidden" name="vue" value="colonnes">' : '')
        . '<label for="f-q">Recherche<input id="f-q" type="search" name="q" value="' . $e($f['q']) . '" placeholder="Nom, réf., tél., commune"></label>'
        . Vue::select('periode', 'Période', $f['periode'], ['' => 'Toutes', '7j' => '7 jours', '30j' => '30 jours', 'mois' => 'Ce mois', '3m' => '3 mois', '12m' => '12 mois'])
        . ($colonnes ? '' : Vue::select('statut', 'Statut', $f['statut'] ?: 'ouvertes', ['ouvertes' => 'Ouvertes', 'toutes' => 'Toutes'] + array_diff_key(Demandes::STATUTS, ['doublon' => 1])))
        . Vue::select('priorite', 'Priorité', $f['priorite'], ['' => 'Toutes', 'A' => 'A', 'B' => 'B', 'C' => 'C', 'hors_cible' => 'Hors cible'])
        . Vue::select('canal', 'Canal', $f['canal'], ['' => 'Tous'] + array_map(static fn ($c) => $c[0], Canaux::LISTE))
        . Vue::select('type_client', 'Type de client', $f['type_client'], ['' => 'Tous'] + Demandes::TYPES_CLIENT)
        . Vue::select('associe', 'Associé', $f['associe'], $optAssocies)
        . '<label class="case" for="f-retard"><input id="f-retard" type="checkbox" name="retard" value="1"' . ($f['retard'] ? ' checked' : '') . '> En retard seulement</label>'
        . '<button class="btn btn-discret" type="submit">Filtrer</button>'
        . '<a class="btn btn-discret" href="' . $e(Vue::url('demandes', $colonnes ? ['vue' => 'colonnes'] : [])) . '">Effacer les filtres</a></form>';

    $bascule = '<div class="bascule" role="group" aria-label="Affichage">'
        . '<a href="' . $e(Vue::url('demandes', array_filter($f))) . '"' . (!$colonnes ? ' aria-current="page"' : '') . '>Liste</a>'
        . '<a href="' . $e(Vue::url('demandes', ['vue' => 'colonnes'] + array_filter(array_diff_key($f, ['statut' => 1])))) . '"' . ($colonnes ? ' aria-current="page"' : '') . '>Colonnes</a></div>';
    $export = Auth::peut($app->utilisateur, 'export') ? '<a class="btn btn-discret" href="' . $e(Vue::url('export', array_filter($f))) . '">Exporter (CSV)</a>' : '';
    $entete = '<div class="entete-page"><div><h1>Demandes</h1><p class="sous-titre">Les filtres sont dans l\'adresse : copiez-la pour envoyer cette vue.</p></div><div class="actions">' . $bascule . $export . '<a class="btn btn-principal" href="' . $e(Vue::url('saisie')) . '">Saisir un appel</a></div></div>';

    if ($colonnes) {
        $toutes = $app->demandes->liste(['statut' => 'toutes'] + $f, $app->utilisateur['id']);
        $il30 = Base::utc($app->maintenant->modify('-30 days'));
        $cols = [
            'nouvelle' => ['Nouvelle', []], 'contact_etabli' => ['Contact établi', []], 'visite_planifiee' => ['Visite planifiée', []],
            'offre_envoyee' => ['Offre envoyée', []], 'signee' => ['Signée (30 jours)', []], 'perdue' => ['Perdue (30 jours)', []],
        ];
        foreach ($toutes as $d) {
            if (!isset($cols[$d['statut']]) || (in_array($d['statut'], ['signee', 'perdue'], true) && $d['statut_change_le'] < $il30)) {
                continue;
            }
            $cols[$d['statut']][1][] = $d;
        }
        $onglets = '<div class="onglets-colonnes" role="tablist" aria-label="Étapes">';
        $html = '<div class="colonnes">';
        $i = 0;
        foreach ($cols as $statut => [$titre, $ds]) {
            $total = array_sum(array_map(static fn ($d) => (float) ($d['montant'] ?? 0), $ds));
            $onglets .= '<button type="button" role="tab" id="onglet-' . $statut . '" aria-controls="col-' . $statut . '" aria-selected="' . ($i === 0 ? 'true' : 'false') . '"' . ($i === 0 ? '' : ' tabindex="-1"') . '>' . $e($titre) . ' (' . count($ds) . ')</button>';
            $html .= '<section class="colonne' . ($i === 0 ? ' active' : '') . '" id="col-' . $statut . '" role="tabpanel" aria-labelledby="t-col-' . $statut . '"><div class="colonne-tete"><h2 id="t-col-' . $statut . '">' . $e($titre) . '</h2><span class="discret">' . count($ds) . ' · ' . $e(Format::chf($total)) . '</span></div>';
            $html .= $ds ? '' : '<p class="petit discret colonne-vide">Aucune demande à cette étape.</p>';
            $html .= '<ul class="cartes">';
            foreach ($ds as $d) {
                $jours = (int) floor(($app->maintenant->getTimestamp() - (Base::local($d['statut_change_le'])?->getTimestamp() ?? 0)) / 86400);
                $html .= '<li class="carte' . ($d['en_retard'] ? ' retard' : '') . '"><div class="haut-carte">' . Vue::prio($d['priorite_eff']) . '<div>' . Vue::nomLien($d) . '</div></div>'
                    . '<span class="meta">' . $e(Demandes::libelleTravaux($d) . ($d['commune'] ? ', ' . $d['commune'] : '')) . '</span>'
                    . '<span class="meta">' . $e($jours . ' j dans l\'étape' . ($d['montant'] ? ' · ' . Format::chf($d['montant']) : '')) . '</span>';
                $actions = array_diff_key($app->demandes->actionsPossibles($d), ['pas_de_reponse' => 1, 'nouvelle_version' => 1]);
                if ($actions) {
                    $html .= '<details class="deplacer"><summary>Déplacer vers…<span class="sr"> (' . $e($d['nom_complet']) . ')</span></summary>' . Composants::formulairesTransitions($app, $d, $actions, Vue::url('demandes', ['vue' => 'colonnes'] + array_filter(array_diff_key($f, ['statut' => 1])))) . '</details>';
                }
                $html .= '</li>';
            }
            $html .= '</ul></section>';
            $i++;
        }
        $onglets .= '</div>';
        return Vue::page($app, 'demandes', 'Demandes, colonnes', $entete . $filtres . $onglets . $html . '</div>');
    }

    $lignes = $app->demandes->liste($f, $app->utilisateur['id']);
    if (!$lignes) {
        $corps = '<p class="vide">Aucune demande pour ces filtres. <a href="' . $e(Vue::url('demandes')) . '">Effacer les filtres</a></p>';
    } else {
        $tri = static function (string $cle, string $lib) use ($f, $e): string {
            $courant = ($f['tri'] ?: 'echeance') === $cle;
            return '<a class="tri" href="' . $e(Vue::url('demandes', ['tri' => $cle] + array_filter($f))) . '"' . ($courant ? ' aria-current="true"' : '') . '>' . $e($lib) . ($courant ? ' <span aria-hidden="true">↓</span><span class="sr"> (tri actuel)</span>' : '') . '</a>';
        };
        $corps = '<p class="petit discret">' . count($lignes) . ' demande' . (count($lignes) > 1 ? 's' : '') . '.</p><div class="defile tableau-liste" tabindex="0" role="region" aria-label="Liste des demandes, défile horizontalement"><table class="tableau compact"><caption class="sr">Demandes</caption><thead><tr>'
            . '<th scope="col">Réf.</th><th scope="col">' . $tri('recue', 'Reçue') . '</th><th scope="col">Nom</th><th scope="col">Type</th><th scope="col">Travaux</th><th scope="col">Commune</th>'
            . '<th scope="col">' . $tri('score', 'Priorité') . '</th><th scope="col">Canal</th><th scope="col">Statut</th><th scope="col">' . $tri('echeance', 'Prochaine action') . '</th><th scope="col" class="num">' . $tri('montant', 'Montant') . '</th><th scope="col">Associé</th></tr></thead><tbody>';
        $cartes = '<ul class="cartes-liste">';
        foreach ($lignes as $d) {
            $prochaine = $d['statut'] === 'nouvelle' ? Vue::echeance($d, $app) : $e(Composants::prochaineAction($app, $d));
            $corps .= '<tr' . ($d['en_retard'] ? ' class="retard"' : '') . '><td class="ref"><a href="' . $e(Vue::url('fiche', ['ref' => $d['ref']])) . '">' . $e($d['ref']) . '</a></td>'
                . '<td>' . $e(Format::dateC($d['recue'])) . '</td><td>' . $e($d['nom_complet']) . ($d['organisation'] ? '<span class="org">' . $e($d['organisation']) . '</span>' : '') . '</td>'
                . '<td>' . $e(Demandes::TYPES_CLIENT[$d['type_client'] ?? ''] ?? '—') . '</td><td>' . $e(Demandes::libelleTravaux($d)) . '</td>'
                . '<td>' . $e($d['commune'] ?? '—') . ($d['zone'] ? '<span class="org">zone ' . $e($d['zone']) . '</span>' : '') . '</td>'
                . '<td>' . Vue::prioScore($d) . '</td><td>' . Vue::canal($d) . '</td><td>' . Vue::statut($d) . '</td><td>' . $prochaine . '</td>'
                . '<td class="num">' . $e($d['montant'] ? Format::chf($d['montant']) : '—') . '</td><td>' . $e($d['associe_nom'] ?? '—') . '</td></tr>';
            $cartes .= '<li' . ($d['en_retard'] ? ' class="retard"' : '') . '><div class="haut-carte">' . Vue::prio($d['priorite_eff']) . '<div><a href="' . $e(Vue::url('fiche', ['ref' => $d['ref']])) . '">' . $e($d['nom_complet']) . '</a>'
                . '<span class="org">' . $e($d['ref'] . ' · ' . Demandes::libelleTravaux($d) . ($d['commune'] ? ', ' . $d['commune'] : '')) . '</span></div></div>'
                . '<div>' . Vue::statut($d) . '</div><div>' . $prochaine . '</div></li>';
        }
        $corps .= '</tbody></table></div>' . $cartes . '</ul>';
    }
    return Vue::page($app, 'demandes', 'Demandes', $entete . $filtres . $corps);
};
