<?php
/** E1 · Vue d'ensemble : alertes, 5 indicateurs du mois face à l'objectif, entonnoir, demandes par mois. */
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
    $mois = Http::get('mois', $courant);
    if (!preg_match('/^\d{4}-(0[1-9]|1[0-2])$/', $mois) || $mois > $courant) {
        $mois = $courant;
    }
    $k = $ind->mois($mois);
    $o = $k['objectifs'];
    $noms = Auth::peut($app->utilisateur, 'vue_noms');
    $etiquetteM = 'M' . $k['m'];

    // ---- alertes
    $al = $ind->alertes();
    $liste = static function (array $ds) use ($noms): string {
        if (!$ds) {
            return 'Aucune';
        }
        return $noms ? implode(', ', array_map(static fn ($d) => $d['nom_complet'], array_slice($ds, 0, 4))) . (count($ds) > 4 ? '…' : '') : count($ds) . ' demande' . (count($ds) > 1 ? 's' : '');
    };
    $lienAlerte = static fn (array $params) => Auth::peut($app->utilisateur, 'demandes') ? Vue::url('demandes', $params) : Vue::url('vue');
    $alerte = static function (int $n, string $lib, string $detail, string $lien, bool $critique) use ($e): string {
        return '<a class="alerte' . ($critique && $n ? ' critique' : '') . '" href="' . $e($lien) . '"><span class="valeur">' . $n . '</span><span class="libelle">' . $e($lib) . '</span><span class="detail">' . $e($detail) . '</span></a>';
    };
    $alertes = '<section aria-labelledby="t-alertes"><h2 class="sr" id="t-alertes">Alertes</h2><div class="alertes">'
        . $alerte(count($al['retards_a']), 'Demandes A non rappelées', $liste($al['retards_a']), $lienAlerte(['retard' => 1, 'priorite' => 'A']), true)
        . $alerte(count($al['retards_autres']), 'Autres demandes en retard', $liste($al['retards_autres']), $lienAlerte(['retard' => 1]), true)
        . $alerte(count($al['offres_j35']), 'Offres sans suite à J+35', $liste($al['offres_j35']), $lienAlerte(['statut' => 'offre_envoyee']), false)
        . $alerte(count($al['visites_jour']), "Visites aujourd'hui", $al['visites_jour'] ? implode(' ; ', array_map(static fn ($d) => Format::heure(Format::t($d['visite']['prevue_le'])) . ($noms ? ', ' . ($d['commune'] ?? '') : ''), $al['visites_jour'])) : 'Aucune', $lienAlerte(['statut' => 'visite_planifiee']), false)
        . $alerte(count($al['hors_cible']), 'Hors cible à valider', $liste($al['hors_cible']), $lienAlerte(['priorite' => 'hors_cible', 'statut' => 'nouvelle']), false)
        . '</div></section>';

    // ---- tuiles
    $tuile = static function (string $id, string $libelle, string $definition, string $valeur, string $objectif, string $metre, string $compl, string $etat) use ($e): string {
        [$bouton, $def] = Vue::aide($id, $definition);
        return '<div class="tuile"><div class="tete"><span class="libelle">' . $e($libelle) . '</span>' . $bouton . '</div>' . $def
            . '<span class="valeur">' . $valeur . '</span><span class="objectif">' . $objectif . '</span>' . $metre . '<span class="compl">' . $compl . '</span>' . $etat . '</div>';
    };
    $petit = static fn (int $n, int $total) => $total < 5 ? " ($n sur $total)" : '';

    $proj = $k['projection'];
    $ref1 = $proj ?? $k['demandes'];
    $t1 = $tuile('def-1', 'Demandes/mois',
        'Demandes enregistrées dont la date de réception (heure de Zurich) tombe dans le mois, tous canaux, hors doublons et tests. Part A+B = (A + B) / (A + B + C). Projection : valeur × jours ouvrables du mois / jours ouvrables écoulés.',
        $k['demandes'] . ($k['courant'] ? ' <small>au ' . $e(Format::dateC($app->maintenant)) . '</small>' : ''),
        $o['demandes'] !== null ? $e('Objectif ' . $etiquetteM . ' : ' . Format::nb($o['demandes']) . ($proj !== null ? ', projection ≈ ' . Format::nb($proj) : '')) : $e('Pas d\'objectif avant M3' . ($proj !== null ? ' · projection ≈ ' . Format::nb($proj) : '')),
        $o['demandes'] !== null ? Vue::metre($ref1, max($o['demandes'], $ref1) * 1.15, $o['demandes'], 'Demandes ' . $k['demandes'] . ' sur un objectif de ' . Format::nb($o['demandes'])) : '',
        'Part A+B : <b>' . $e(Format::pct($k['part_ab'])) . '</b>' . ($o['part_ab'] !== null ? $e(' (objectif ≥ ' . Format::pct($o['part_ab']) . ')') : '') . $e('. Mois précédent : ' . $k['demandes_prec']),
        $o['demandes'] === null ? Vue::etat(null, '', '', 'Objectif à partir de M3') : Vue::etat($ref1 >= $o['demandes'], $k['courant'] ? "En avance sur l'objectif" : 'Objectif atteint', "En dessous de l'objectif")
    );
    $dl = $k['delai_a'];
    $t2 = $tuile('def-2', 'Délai de premier contact, demandes A',
        "Médiane, en heures ouvrables (lu-ve 7 h-18 h, fériés genevois), entre la réception et le premier contact établi, sur les demandes A du mois. Les appels entrants sont exclus. Rappelées dans le délai : premier appel avant l'échéance.",
        $e(Format::duree($dl)),
        $o['delai_a'] !== null ? $e('Objectif ' . $etiquetteM . ' : moins de ' . Format::duree($o['delai_a']) . ' ouvrables') : 'Pas d\'objectif avant M3',
        $dl !== null && $o['delai_a'] !== null ? Vue::metre($dl, max($o['delai_a'] * 2, $dl), $o['delai_a'], 'Délai médian ' . Format::duree($dl) . ', objectif ' . Format::duree($o['delai_a'])) : '',
        $e('Rappelées dans le délai : ') . '<b>' . $k['dans_delai']['ok'] . ' sur ' . $k['dans_delai']['total'] . '</b>' . $e(', toutes priorités : ' . Format::duree($k['delai_tous'])),
        $dl === null || $o['delai_a'] === null ? Vue::etat(null, '', '', $dl === null ? 'Aucun premier contact A ce mois' : 'Objectif à partir de M3') : Vue::etat($dl <= $o['delai_a'], "Dans l'objectif", "Au-dessus de l'objectif")
    );
    $tdo = $k['demande_offre'];
    $t3 = $tuile('def-3', 'Taux demande→offre',
        'Offres envoyées pendant le mois (première version) / demandes enregistrées pendant le mois précédent (définition v2 §1.1). Une nouvelle version d\'offre ne compte pas.',
        $e(Format::pct($tdo['taux'] ?? null)),
        $o['demande_offre'] !== null ? $e('Objectif ' . $etiquetteM . ' : ' . Format::pct($o['demande_offre'])) : 'Pas d\'objectif avant M3',
        $tdo && $o['demande_offre'] !== null ? Vue::metre($tdo['taux'], max(1, $tdo['taux']), $o['demande_offre'], 'Taux ' . Format::pct($tdo['taux']) . ', objectif ' . Format::pct($o['demande_offre'])) : '',
        $e($tdo ? $tdo['offres'] . ' offres pour ' . $tdo['demandes'] . ' demandes en ' . Format::mois($tdo['mois_demandes']) : 'Aucune demande le mois précédent') . ($k['demande_offre_prec'] ? $e('. Mois précédent : ' . Format::pct($k['demande_offre_prec']['taux'])) : ''),
        !$tdo || $o['demande_offre'] === null ? Vue::etat(null, '', '', 'Pas encore mesurable') : Vue::etat($tdo['taux'] >= $o['demande_offre'], "Dans l'objectif", $k['courant'] ? 'En dessous (mois en cours)' : "En dessous de l'objectif")
    );
    $tos = $k['offre_signee'];
    $t4 = $tuile('def-4', 'CA signé',
        'Somme des montants signés (HT) des offres signées pendant le mois. Taux offre→signée : offres signées / offres envoyées entre J−180 et J−60. Objectif indicatif : chantiers visés × panier de référence (Paramètres, décision G4).',
        $e(Format::chf($k['ca_signe'])),
        $e($k['nb_signes'] . ' chantier' . ($k['nb_signes'] > 1 ? 's signés' : ' signé') . ($o['ca'] !== null ? ', objectif indicatif ' . Format::chf($o['ca']) : '')),
        $o['ca'] !== null ? Vue::metre($k['ca_signe'], max($k['ca_signe'], $o['ca']) * 1.1, $o['ca'], 'CA signé ' . Format::chf($k['ca_signe']) . ', objectif ' . Format::chf($o['ca'])) : '',
        $e('Taux offre→signée : ') . '<b>' . $e(Format::pct($tos['taux'])) . '</b>' . $e(' (' . $tos['signees'] . ' sur ' . $tos['offres'] . ($o['offre_signee'] !== null ? ', objectif ' . Format::pct($o['offre_signee']) : '') . ')'),
        $o['ca'] === null ? Vue::etat(null, '', '', 'Objectif à partir de M3') : ($k['courant'] && $k['ca_signe'] < $o['ca'] ? Vue::etat(null, '', '', 'Mois en cours, signatures irrégulières') : Vue::etat($k['ca_signe'] >= $o['ca'], 'Objectif atteint', 'En dessous'))
    );
    $cm = $k['cpl_max'];
    $t5 = $tuile('def-5', 'CPL, canaux payants',
        'CPL = dépense / demandes, sur Google Ads, Meta, LinkedIn et la prospection B2B (dépenses saisies dans Paramètres). Cible : un tiers du CPL max = panier moyen × marge brute × taux demande→offre × taux offre→signée (plan d\'acquisition v4 §2.5).',
        $e(Format::chf($k['cpl'])),
        $e('Cible ≤ ' . Format::chf($cm['cible'] ?? null) . ' (CPL max ' . Format::chf($cm['max'] ?? null) . ')'),
        $k['cpl'] !== null && $cm ? Vue::metre($k['cpl'], max($k['cpl'], $cm['cible']) * 1.4, $cm['cible'], 'CPL ' . Format::chf($k['cpl']) . ', cible ' . Format::chf($cm['cible'])) : '',
        $e(Format::chf($k['depense_payante']) . ' / ' . $k['demandes_payantes'] . ' demandes payantes' . ($cm && $cm['sources'] ? ' · CPL max avec ' . implode(', ', $cm['sources']) : '')),
        $k['cpl'] === null || !$cm ? Vue::etat(null, '', '', $k['depense_payante'] > 0 ? 'Aucune demande payante' : 'Aucune dépense saisie') : Vue::etat($k['cpl'] <= $cm['cible'], 'Sous la cible', 'Au-dessus de la cible')
    );

    // ---- graphiques
    $debutEntonnoir = (new \DateTimeImmutable(Indicateurs::moisDecale($courant, -2) . '-01 00:00', new \DateTimeZone('Europe/Zurich')));
    $ent = $ind->entonnoir($debutEntonnoir);
    $motifs = [];
    foreach ($ent['perdues'] as $code => $n) {
        $motifs[] = mb_strtolower(\AndyConstruct\Admin\Demandes::MOTIFS[$code][0] ?? $code) . ' ' . $n;
    }
    $txtEnt = '<p class="petit discret">' . $e($ent['en_cours'] . ' offre' . ($ent['en_cours'] > 1 ? 's' : '') . ' en attente de réponse' . ($motifs ? ' ; perdues : ' . implode(', ', $motifs) : '') . '.') . '</p>';
    $six = array_map(static fn ($i) => Indicateurs::moisDecale($courant, $i), range(-5, 0));

    $options = [];
    for ($i = 0; $i < 12; $i++) {
        $m = Indicateurs::moisDecale($courant, -$i);
        $options[$m] = Format::mois($m) . ($i === 0 ? ' (en cours)' : '');
    }
    $sousTitre = $k['courant']
        ? ucfirst(Format::mois($mois)) . ', arrêté au ' . Format::dateL($app->maintenant) . ' à ' . Format::heure($app->maintenant) . " ($etiquetteM, " . $k['jours_ecoules'] . 'e jour ouvrable sur ' . $k['jours_ouvrables'] . ')'
        : ucfirst(Format::mois($mois)) . ", mois complet ($etiquetteM)";
    $vide = $k['demandes'] === 0 && $k['demandes_prec'] === 0 ? '<p class="vide">Les indicateurs apparaissent dès la première demande enregistrée.</p>' : '';

    $contenu = '<div class="entete-page"><div><h1>Vue d\'ensemble</h1><p class="sous-titre">' . $e($sousTitre) . '</p></div>'
        . '<form class="actions filtres sans-marge" method="get" action="' . $e(Vue::$base) . '" data-auto><input type="hidden" name="p" value="vue">' . Vue::select('mois', 'Mois', $mois, $options) . '<button class="btn btn-discret sans-js" type="submit">Afficher</button></form></div>'
        . $vide . $alertes
        . '<section class="mt" aria-labelledby="t-ind"><h2 class="sr" id="t-ind">Cinq indicateurs du mois</h2><div class="tuiles">' . $t1 . $t2 . $t3 . $t4 . $t5 . '</div></section>'
        . '<div class="grille-2 mt"><section class="panneau" aria-labelledby="t-ent"><div class="panneau-entete"><h2 id="t-ent">Entonnoir</h2><span class="discret">' . $e('demandes reçues depuis le 1er ' . Format::mois(Indicateurs::moisDecale($courant, -2)) . ', état aujourd\'hui') . '</span></div>'
        . Graphiques::entonnoir($ent['etapes']) . $txtEnt . '</section>'
        . '<section class="panneau" aria-labelledby="t-dm"><div class="panneau-entete"><h2 id="t-dm">Demandes par mois</h2><span class="discret">6 mois, par priorité</span></div>'
        . Graphiques::demandesParMois($ind->parMois($six)) . '</section></div>';
    return Vue::page($app, 'vue', "Vue d'ensemble", $contenu);
};
