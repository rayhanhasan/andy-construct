<?php
/** E13 · Journal d'audit et données personnelles (nLPD) : recherche d'une personne, export, effacement. */
declare(strict_types=1);

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Auth;
use AndyConstruct\Admin\Demandes;
use AndyConstruct\Admin\Format;
use AndyConstruct\Admin\Http;
use AndyConstruct\Admin\Personnes;
use AndyConstruct\Admin\Vue;
use AndyConstruct\Api\Base;

return static function (App $app): string {
    $e = static fn ($v) => Vue::e($v);
    $personnes = new Personnes($app);
    $contactId = ctype_digit(Http::get('contact')) ? (int) Http::get('contact') : 0;
    $ici = Vue::url('donnees', $contactId ? ['contact' => $contactId] : []);
    $message = '';

    if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
        $cible = (int) Http::post('contact');
        try {
            if (!Auth::peut($app->utilisateur, 'effacer')) {
                throw new \DomainException('Votre rôle ne permet pas cette action.');
            }
            if (Http::post('op') === 'exporter') {
                $json = json_encode($personnes->exporter($cible), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
                header('Content-Type: application/json; charset=utf-8');
                header('Content-Disposition: attachment; filename="donnees-personne-' . $cible . '-' . $app->maintenant->format('Y-m-d') . '.json"');
                echo $json;
                exit;
            }
            if (Http::post('op') === 'effacer') {
                $apercu = $personnes->apercu($cible);
                $attendu = (string) ($apercu['refs'][0] ?? '');
                if ($attendu === '' || strtoupper(trim(Http::post('confirmation'))) !== $attendu) {
                    throw new \DomainException('Pour confirmer, tapez exactement la référence ' . ($attendu ?: '') . '.');
                }
                $n = $personnes->effacer($cible);
                Vue::flash("Données effacées ($n demande" . ($n > 1 ? 's anonymisées' : ' anonymisée') . '). Les indicateurs ne changent pas.');
                Http::rediriger(Vue::url('donnees'));
            }
        } catch (\DomainException $ex) {
            $message = '<p class="erreur-formulaire" role="alert">' . $e($ex->getMessage()) . '</p>';
        }
    }

    // Recherche d'une personne
    $q = mb_substr(Http::get('q'), 0, 120);
    $resultats = $q !== '' ? $personnes->rechercher($q) : [];
    $recherche = '<section class="panneau" aria-labelledby="t-pers"><h2 id="t-pers">Droits des personnes</h2><p class="petit discret">Accès, rectification, effacement : réponse sous 30 jours. Recherche par e-mail ou téléphone exacts.</p>'
        . '<form class="filtres" method="get" action="' . $e(Vue::$base) . '"><input type="hidden" name="p" value="donnees"><label for="d-q">E-mail ou téléphone<input id="d-q" type="search" name="q" value="' . $e($q) . '" autocomplete="off"></label><button class="btn btn-discret" type="submit">Rechercher</button></form>';
    if ($q !== '') {
        $app->audit('recherche_personne', null, null, ['resultats' => count($resultats)]);
        $recherche .= $resultats ? '<ul class="liste-simple">' . implode('', array_map(static fn ($c) => '<li><a href="' . $e(Vue::url('donnees', ['contact' => $c['id']])) . '">' . $e(trim(($c['prenom'] ?? '') . ' ' . ($c['nom'] ?? '')) ?: 'Sans nom') . '</a> · ' . (int) $c['nb_demandes'] . ' demande(s)</li>', $resultats)) . '</ul>'
            : '<p class="vide">Personne ne correspond à cette adresse ou à ce numéro.</p>';
    }
    $recherche .= '</section>';

    $fiche = '';
    if ($contactId) {
        $c = $app->base->un('SELECT * FROM contact WHERE id = ?', [$contactId]);
        if ($c !== null && $c['anonymise_le'] === null) {
            $apercu = $personnes->apercu($contactId);
            $nom = trim(($c['prenom'] ?? '') . ' ' . ($c['nom'] ?? '')) ?: 'Sans nom';
            $fiche = '<section class="panneau mt" aria-labelledby="t-fp"><h2 id="t-fp">' . $e($nom) . '</h2><p>Demandes : ' . implode(', ', array_map(static fn ($r) => '<a href="' . $e(Vue::url('fiche', ['ref' => $r])) . '">' . $e($r) . '</a>', $apercu['refs'])) . '.</p>'
                . (Auth::peut($app->utilisateur, 'effacer') ? '<div class="grille-2"><div><h3>Exporter</h3><p class="petit">Toutes les données de la personne (JSON lisible) : coordonnées, demandes, historique, offres, visites, liste des fichiers.</p>'
                . '<form method="post" action="' . $e($ici) . '">' . Vue::csrf($app) . '<input type="hidden" name="op" value="exporter"><input type="hidden" name="contact" value="' . $contactId . '"><button class="btn btn-sombre" type="submit">Exporter les données</button></form></div>'
                . '<div><h3>Effacer</h3><p class="petit"><b>Effacé :</b> nom, coordonnées, message, commune exacte, notes, ' . (int) $apercu['fichiers'] . ' fichier(s), gclid. <b>Gardé</b> (statistiques) : date, canal, priorité, statut, montants, zone. Les sauvegardes s\'effacent au plus tard 30 jours après.</p>'
                . '<form method="post" action="' . $e($ici) . '" class="formulaire">' . Vue::csrf($app) . '<input type="hidden" name="op" value="effacer"><input type="hidden" name="contact" value="' . $contactId . '">'
                . '<label class="champ" for="d-conf"><span>Pour confirmer, tapez la référence ' . $e($apercu['refs'][0] ?? '') . '</span><input id="d-conf" name="confirmation" required autocomplete="off"></label>'
                . '<div><button class="btn btn-danger" type="submit">Effacer définitivement</button></div></form></div></div>' : '')
                . '</section>';
        } else {
            $fiche = '<p class="vide mt">Personne introuvable ou déjà effacée.</p>';
        }
    }

    // Journal d'audit
    $filtreAction = mb_substr(Http::get('action'), 0, 40);
    $sql = 'SELECT j.*, u.nom_affiche FROM journal_audit j LEFT JOIN utilisateur u ON u.id = j.utilisateur_id';
    $p = [];
    if ($filtreAction !== '') {
        $sql .= ' WHERE j.action = ?';
        $p[] = $filtreAction;
    }
    $journal = $app->base->tous($sql . ' ORDER BY j.id DESC LIMIT 200', $p);
    $actions = array_column($app->base->tous('SELECT DISTINCT action FROM journal_audit ORDER BY action'), 'action');
    $lignes = '';
    foreach ($journal as $j) {
        $details = $j['details'] ? implode(', ', array_map(static fn ($k, $v) => $k . ' : ' . (is_array($v) ? implode(' ', $v) : (string) $v), array_keys((array) json_decode((string) $j['details'], true)), (array) json_decode((string) $j['details'], true))) : '';
        $lignes .= '<tr><td>' . $e(Format::dateH(Format::t($j['quand']))) . '</td><td>' . $e($j['nom_affiche'] ?? $j['acteur']) . '</td><td><code>' . $e($j['action']) . '</code></td><td>' . $e(trim(($j['objet_type'] ?? '') . ' ' . ($j['objet_id'] ?? ''))) . '</td><td class="petit">' . $e($details) . '</td><td class="petit">' . $e($j['ip_tronquee'] ?? '') . '</td></tr>';
    }
    $optActions = ['' => 'Toutes'] + array_combine($actions, $actions);
    $audit = '<section class="panneau mt" aria-labelledby="t-audit"><div class="panneau-entete"><h2 id="t-audit">Journal d\'audit</h2><span class="discret">200 dernières entrées, sans valeur personnelle ; conservé 12 mois</span></div>'
        . '<form class="filtres" method="get" action="' . $e(Vue::$base) . '" data-auto><input type="hidden" name="p" value="donnees">' . Vue::select('action', 'Action', $filtreAction, $optActions) . '<button class="btn btn-discret sans-js" type="submit">Filtrer</button></form>'
        . '<div class="defile" tabindex="0" role="region" aria-label="Tableau, défile horizontalement"><table class="tableau compact"><caption class="sr">Journal d\'audit</caption><thead><tr><th scope="col">Quand</th><th scope="col">Qui</th><th scope="col">Action</th><th scope="col">Objet</th><th scope="col">Détails</th><th scope="col">IP</th></tr></thead><tbody>' . $lignes . '</tbody></table></div></section>';

    return Vue::page($app, 'donnees', 'Journal et données personnelles', '<div class="entete-page"><div><h1>Journal et données personnelles</h1></div></div>' . $message . $recherche . $fiche . $audit);
};
