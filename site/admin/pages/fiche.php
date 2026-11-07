<?php
/** E5 · Fiche demande : coordonnées, projet, fichiers, score détaillé, attribution, historique, notes, actions. */
declare(strict_types=1);

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Auth;
use AndyConstruct\Admin\Composants;
use AndyConstruct\Admin\Demandes;
use AndyConstruct\Admin\Format;
use AndyConstruct\Admin\Http;
use AndyConstruct\Admin\Vue;
use AndyConstruct\Api\Canaux;

return static function (App $app): string {
    $e = static fn ($v) => Vue::e($v);
    $ref = Http::get('ref');
    $d = preg_match('/^[A-Z0-9]{1,6}-\d{4}-\d{4,6}$/', $ref) ? $app->demandes->parRef($ref) : null;
    if ($d === null) {
        http_response_code(404);
        return Vue::page($app, 'fiche', 'Demande introuvable', '<h1>Demande introuvable</h1><p>Aucune demande ne porte la référence « ' . $e($ref) . ' ». <a href="' . $e(Vue::url('demandes')) . '">Retour aux demandes</a></p>');
    }
    $uid = $app->utilisateur['id'];
    $ici = Vue::url('fiche', ['ref' => $d['ref']]);

    if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
        $retour = Http::post('retour');
        $retour = str_starts_with($retour, Vue::$base) ? $retour : $ici;
        try {
            switch (Http::post('op')) {
                case 'statut':
                    $r = $app->demandes->agir($d['id'], Http::post('action'), [
                        'montant' => Http::post('montant'), 'date' => Http::post('date'), 'heure' => Http::post('heure'), 'adresse' => Http::post('adresse'),
                        'motif' => Http::post('motif'), 'numero' => Http::post('numero'), 'version' => Http::post('version'), 'recontact' => Http::post('recontact'),
                    ], $uid);
                    Vue::flash($d['nom_complet'] . ' : ' . $r['texte'] . ($r['de'] !== $r['vers'] ? ' (' . Demandes::STATUTS[$r['vers']] . ')' : '') . '.');
                    break;
                case 'note':
                    $app->demandes->ajouterNote($d['id'], Http::post('note'), $uid);
                    Vue::flash('Note ajoutée à l\'historique.');
                    break;
                case 'priorite':
                    $app->demandes->corrigerPriorite($d['id'], Http::post('priorite'), Http::post('motif'), $uid);
                    Vue::flash('Priorité corrigée.');
                    break;
                case 'canal':
                    $app->demandes->corrigerCanal($d['id'], Http::post('canal'), $uid);
                    Vue::flash('Canal corrigé.');
                    break;
                case 'reattribuer':
                    $app->demandes->reattribuer($d['id'], (int) Http::post('associe'), $uid);
                    Vue::flash('Demande réattribuée.');
                    break;
                default:
                    throw new \DomainException('Action inconnue.');
            }
        } catch (\DomainException $ex) {
            Vue::flash($ex->getMessage(), 'erreur');
        }
        Http::rediriger($retour);
    }

    $app->audit('consultation_fiche', 'demande', $d['ref']);
    $relance = $app->demandes->relance($d);
    $detail = json_decode((string) ($d['score_detail'] ?? '[]'), true) ?: [];
    $regles = json_decode((string) ($d['score_regles'] ?? '[]'), true) ?: [];
    $efface = !empty($d['anonymise_le']);

    // En-tête
    $appeler = $d['telephone_e164'] ? '<a class="btn' . ($d['statut'] === 'nouvelle' ? ' btn-principal' : '') . '" href="tel:' . $e($d['telephone_e164']) . '" data-appel="' . $e($d['ref']) . '">Appeler</a>' : '';
    $mail = $d['email'] ? '<a class="btn btn-discret" href="mailto:' . $e($d['email']) . '?subject=' . rawurlencode('Votre demande ' . $d['ref']) . '">E-mail</a>' : '';
    $entete = '<div class="fiche-entete"><div><p class="petit discret fil"><a href="' . $e(Vue::url('demandes')) . '">Demandes</a> / ' . $e($d['ref']) . '</p>'
        . '<h1>' . $e($d['nom_complet']) . ($d['organisation'] ? ', <span class="org-titre">' . $e($d['organisation']) . '</span>' : '') . '</h1>'
        . '<div class="ligne-meta">' . Vue::prioScore($d) . Vue::statut($d) . ($d['statut'] === 'nouvelle' ? Vue::echeance($d, $app) : '<span>' . $e(Composants::prochaineAction($app, $d)) . '</span>')
        . '<span>Associé : ' . $e($d['associe_nom'] ?? 'non attribué') . '</span></div></div>'
        . '<div class="groupe-btn boutons-entete">' . $appeler . $mail . '</div></div>';

    // Projet
    $commune = trim(($d['npa'] ?? '') . ' ' . ($d['commune'] ?? ''));
    $fichiers = $app->base->tous('SELECT * FROM fichier WHERE demande_id = ? ORDER BY id', [$d['id']]);
    $htmlFichiers = '';
    foreach ($fichiers as $fi) {
        $present = $fi['supprime_le'] === null && is_file($app->stockage->dossier('fichiers') . '/' . basename((string) $fi['identifiant']));
        $libelle = ($fi['nom_original'] ?? 'fichier') . ', ' . Format::nb(((int) $fi['taille']) / 1048576, 1) . ' Mo';
        $htmlFichiers .= $present
            ? '<a class="fichier" href="' . $e(Vue::url('fichier', ['id' => $fi['id']])) . '"><i aria-hidden="true"></i>' . $e($libelle) . '<span class="sr"> (télécharger)</span></a>'
            : '<span class="fichier indisponible"><i aria-hidden="true"></i>' . $e($libelle) . ' <span class="discret">(plus sur le serveur)</span></span>';
    }
    $projet = '<details class="bloc" open><summary>Projet <span class="discret">' . $e(Demandes::TYPES_CLIENT[$d['type_client'] ?? ''] ?? 'Type non précisé') . '</span></summary><div class="bloc-corps"><dl class="dl">'
        . '<dt>Formulaire</dt><dd>' . $e(['devis' => 'Demande de devis', 'rappel' => 'Demande de rappel', 'envoi_postal_guide' => 'Guide imprimé par la poste'][$d['formulaire']] ?? $d['formulaire']) . ($d['guide'] ? ' (' . $e($d['guide']) . ')' : '') . '</dd>'
        . '<dt>Travaux</dt><dd>' . $e(Demandes::libelleTravaux($d)) . '</dd>'
        . '<dt>Surface</dt><dd>' . $e(Demandes::SURFACES[$d['surface'] ?? ''] ?? 'Non précisée') . '</dd>'
        . '<dt>Délai</dt><dd>' . $e(Demandes::DELAIS[$d['delai'] ?? ''] ?? 'Non précisé') . '</dd>'
        . '<dt>Commune</dt><dd>' . $e(($commune ?: '—') . ($d['canton'] ? ' (' . $d['canton'] . ')' : '') . ', zone ' . ($d['zone'] ?? 'inconnue')) . '</dd>'
        . ($d['recommande_par'] ? '<dt>Recommandé par</dt><dd>' . $e($d['recommande_par']) . '</dd>' : '') . '</dl>'
        . '<div class="message">' . ($d['message'] ? nl2br($e($d['message'])) : '<span class="discret">' . ($efface ? 'Message effacé.' : 'Message vide.') . '</span>') . '</div>'
        . ($htmlFichiers ? '<div class="fichiers">' . $htmlFichiers . '</div>' : '') . '</div></details>';

    // Score détaillé
    $lignesScore = '';
    foreach ($detail as $l) {
        $lignesScore .= '<tr><th scope="row">' . $e(Demandes::CRITERES[$l['critere']] ?? $l['critere']) . '</th><td>' . $e(Demandes::libelleCritere((string) $l['critere'], (string) $l['valeur'])) . '</td><td class="num">' . ($l['points'] > 0 ? '+' : '') . (int) $l['points'] . '</td></tr>';
    }
    $s = $app->grille['seuils'] ?? ['A' => 65, 'B' => 40];
    $optPrio = '';
    foreach (['A' => 'A', 'B' => 'B', 'C' => 'C', 'hors_cible' => 'Hors cible'] as $v => $l) {
        $optPrio .= '<option value="' . $v . '"' . ($v === $d['priorite_eff'] ? ' selected' : '') . '>' . $l . '</option>';
    }
    $score = $d['score'] === null ? '' : '<details class="bloc" open><summary>Score détaillé <span class="discret">' . $e($d['score'] . ' points, priorité ' . ($d['priorite'] === 'hors_cible' ? 'hors cible' : $d['priorite']) . ', grille ' . ($d['grille_version'] ?? '')) . '</span></summary><div class="bloc-corps">'
        . '<table class="tableau"><caption class="sr">Détail du score</caption><thead><tr><th scope="col">Critère</th><th scope="col">Valeur</th><th scope="col" class="num">Points</th></tr></thead><tbody>' . $lignesScore
        . '</tbody><tfoot><tr><th scope="row" colspan="2">Total</th><td class="num">' . (int) $d['score'] . '</td></tr></tfoot></table>'
        . ($regles ? '<p class="petit mt">Règles appliquées : ' . $e(implode(' ; ', $regles)) . '.</p>' : '')
        . '<p class="petit discret">' . $e('Seuils : A dès ' . $s['A'] . ', B dès ' . $s['B'] . '.') . '</p>'
        . ($efface ? '' : '<details class="transition"><summary>Corriger la priorité</summary><form method="post" action="' . $e($ici) . '" class="formulaire-transition">' . Vue::csrf($app) . '<input type="hidden" name="op" value="priorite">'
        . '<label class="champ" for="c-prio"><span>Priorité</span><select id="c-prio" name="priorite">' . $optPrio . '</select></label>'
        . '<label class="champ" for="c-motif"><span>Motif (obligatoire, journalisé)</span><input id="c-motif" name="motif" required maxlength="500" autocomplete="off"></label>'
        . '<button class="btn btn-petit btn-sombre" type="submit">Corriger</button></form></details>') . '</div></details>';

    // Attribution
    $optCanal = '';
    foreach (Canaux::LISTE as $id => [$lib]) {
        $optCanal .= '<option value="' . $id . '"' . ($id === $d['canal_eff'] ? ' selected' : '') . '>' . $e($lib) . '</option>';
    }
    $utm = trim(implode(' / ', array_filter([$d['utm_source'], $d['utm_medium'], $d['utm_campaign'], $d['utm_content'], $d['utm_term']])));
    $attrib = '<details class="bloc"><summary>Source et attribution <span class="discret">' . $e(Canaux::libelle($d['canal_eff'])) . '</span></summary><div class="bloc-corps"><dl class="dl">'
        . '<dt>Canal</dt><dd>' . $e(Canaux::libelle($d['canal_eff'])) . ($d['canal_corrige'] ? ' (corrigé)' : ((int) $d['canal_declare'] ? ' (déclaré : « Comment nous avez-vous connus ? »)' : '')) . '</dd>'
        . '<dt>Arrivée</dt><dd>' . $e(Demandes::CANAUX_SAISIE[$d['canal']] ?? 'Formulaire du site') . '</dd>'
        . '<dt>Catégorie</dt><dd><code>' . $e($d['categorie'] ?? '—') . '</code> ' . $e($d['source_libelle'] ?? '') . '</dd>'
        . '<dt>Pages</dt><dd>' . $e(($d['page_entree'] ?: '—') . ' → ' . ($d['page'] ?: '—')) . ($d['emplacement'] ? ' <span class="discret">(' . $e($d['emplacement']) . ')</span>' : '') . '</dd>'
        . '<dt>Référent</dt><dd>' . $e($d['referent'] ?: '—') . '</dd>'
        . '<dt>UTM</dt><dd>' . $e($utm ?: '—') . '</dd>'
        . '<dt>« Connu par »</dt><dd>' . $e($d['connu_par'] ?: '—') . '</dd>'
        . '<dt>gclid</dt><dd>' . ($d['gclid'] ? 'présent (mesure publicitaire acceptée)' : ($d['consent_ads'] === 'refuse' ? 'absent : mesure publicitaire refusée' : '—')) . '</dd></dl>'
        . ($efface ? '' : '<details class="transition"><summary>Corriger le canal</summary><form method="post" action="' . $e($ici) . '" class="formulaire-transition">' . Vue::csrf($app) . '<input type="hidden" name="op" value="canal">'
        . '<label class="champ" for="c-canal"><span>Canal (journalisé, fait foi dans Acquisition)</span><select id="c-canal" name="canal">' . $optCanal . '</select></label><button class="btn btn-petit btn-sombre" type="submit">Corriger</button></form></details>')
        . '</div></details>';

    // Historique
    $hist = '<ol class="historique">';
    foreach ($app->demandes->historique($d['id']) as $h) {
        $auteur = $h['nom_affiche'] ?? match ($h['origine']) { 'site' => 'Site', 'n8n' => 'n8n', 'lien_un_clic' => 'Lien en un clic', default => 'Système' };
        $hist .= '<li><time datetime="' . $e(str_replace(' ', 'T', (string) $h['cree_le']) . 'Z') . '">' . $e(Format::dateC(Format::t($h['cree_le'])) . ', ' . Format::heure(Format::t($h['cree_le']))) . '</time><div>'
            . ($h['contenu'] !== null ? nl2br($e($h['contenu'])) : '<span class="discret">(contenu effacé)</span>') . '<div class="auteur">' . $e($auteur) . '</div></div></li>';
    }
    $hist .= '</ol>';
    $historique = '<details class="bloc" open><summary>Historique</summary><div class="bloc-corps">' . $hist . '</div></details>';
    $notes = $efface ? '' : '<details class="bloc"><summary>Ajouter une note <span class="discret">invisible pour l\'agence</span></summary><div class="bloc-corps"><form method="post" action="' . $e($ici) . '">' . Vue::csrf($app)
        . '<input type="hidden" name="op" value="note"><label class="champ" for="note"><span class="sr">Note</span><textarea id="note" name="note" required maxlength="5000" placeholder="Ce qui a été dit, ce qui est convenu"></textarea></label>'
        . '<p class="mt"><button class="btn btn-petit" type="submit">Ajouter la note</button></p></form></div></details>';

    // Colonne de droite
    $autres = $app->demandes->autresDemandes($d);
    $coord = '<section class="panneau panneau-coord" aria-labelledby="t-coord"><h2 id="t-coord">Coordonnées</h2><dl class="dl">'
        . '<dt>Téléphone</dt><dd>' . ($d['telephone_affiche'] ? '<a href="tel:' . $e($d['telephone_e164']) . '">' . $e($d['telephone_affiche']) . '</a>' : '<span class="discret">non donné</span>') . '</dd>'
        . '<dt>E-mail</dt><dd>' . ($d['email'] ? '<a href="mailto:' . $e($d['email']) . '">' . $e($d['email']) . '</a>' : '<span class="discret">non donné</span>') . '</dd>'
        . '<dt>Préférence</dt><dd>' . $e(['appel' => 'Par téléphone', 'email' => 'Par e-mail', 'indifferent' => 'Peu importe'][$d['preference_contact'] ?? ''] ?? '—') . ($d['creneau'] ? $e(', ' . (['matin' => 'le matin', 'apres-midi' => "l'après-midi", 'indifferent' => 'peu importe'][$d['creneau']] ?? '')) : '') . '</dd>'
        . ($d['adresse'] ? '<dt>Adresse</dt><dd>' . nl2br($e($d['adresse'])) . '</dd>' : '')
        . '<dt>Reçue</dt><dd>' . $e(Format::dateH($d['recue'])) . '</dd>'
        . ($d['premier_contact_le'] ? '<dt>1er contact</dt><dd>' . $e(Format::dateH(Format::t($d['premier_contact_le'])) . ($d['canal'] !== 'telephone' ? ' (' . Format::duree($app->heures->minutesOuvrables($d['recue'], Format::t($d['premier_contact_le']))) . ' ouvrables)' : ' (appel entrant)')) . '</dd>' : '')
        . '<dt>Accusé</dt><dd>' . $e(['envoye' => 'envoyé', 'limite' => 'non envoyé (plafond)', 'mis_de_cote' => 'en attente d\'envoi', 'non' => 'non (pas d\'e-mail)'][$d['accuse_reception'] ?? 'non'] ?? '—') . '</dd></dl>'
        . ($autres ? '<p class="petit mt"><span class="etiquette">Doublon possible</span> Même personne : ' . implode(', ', array_map(static fn ($a) => '<a href="' . $e(Vue::url('fiche', ['ref' => $a['ref']])) . '">' . $e($a['ref']) . '</a> (' . $e(Demandes::STATUTS[$a['statut']] ?? $a['statut']) . ')', $autres)) . '</p>' : '')
        . '</section>';
    $offre = '';
    if ($d['offre']) {
        $o = $d['offre'];
        $offre = '<section class="panneau" aria-labelledby="t-offre"><h2 id="t-offre">Offre</h2><dl class="dl"><dt>N°</dt><dd>' . $e($o['numero'] . ' (version ' . $o['version'] . ')') . '</dd>'
            . '<dt>Montant</dt><dd>' . $e(Format::chf((float) $o['montant_ht'])) . ' HT</dd><dt>Envoyée</dt><dd>' . $e(Format::dateA(Format::t($o['envoyee_le'])) . ($relance ? ', J+' . $relance['jours'] : '')) . '</dd>'
            . ($relance ? '<dt>Relances</dt><dd>' . $relance['etape'] . ' sur 3</dd><dt>Ensuite</dt><dd>' . $e($relance['texte']) . '</dd>' : '')
            . ($o['signee_le'] ? '<dt>Signée</dt><dd>' . $e(Format::dateA(Format::t($o['signee_le'])) . ', ' . Format::chf((float) $o['montant_signe_ht'])) . ' HT</dd>' : '')
            . ($d['motif_perte'] ? '<dt>Perdue</dt><dd>' . $e(Demandes::MOTIFS[$d['motif_perte']][0] ?? $d['motif_perte']) . '</dd>' : '') . '</dl></section>';
    } elseif ($d['motif_perte']) {
        $offre = '<section class="panneau"><h2>Perdue</h2><p>' . $e((Demandes::MOTIFS[$d['motif_perte']][0] ?? $d['motif_perte']) . ', le ' . Format::dateA(Format::t($d['perdue_le']))) . ((int) $d['recontact_autorise'] ? ' · relance à 6 mois' : '') . '</p></section>';
    }
    if ($d['visite']) {
        $offre .= '<section class="panneau"><h2>Visite</h2><p>' . $e(Format::dateH(Format::t($d['visite']['prevue_le'])) . ($d['visite']['adresse'] ? ', ' . $d['visite']['adresse'] : '')) . '</p></section>';
    }
    $actionsPossibles = $efface ? [] : $app->demandes->actionsPossibles($d);
    $formsActions = $actionsPossibles ? Composants::formulairesTransitions($app, $d, $actionsPossibles, $ici) : '<p class="petit discret">Aucun changement de statut possible.</p>';
    $optAssocies = '';
    foreach ($app->base->tous("SELECT id, nom_affiche FROM utilisateur WHERE actif = 1 AND role IN ('associe', 'secretariat') ORDER BY nom_affiche") as $a) {
        $optAssocies .= '<option value="' . (int) $a['id'] . '"' . ((int) $a['id'] === (int) $d['associe_id'] ? ' selected' : '') . '>' . $e($a['nom_affiche']) . '</option>';
    }
    $reattribuer = $efface ? '' : '<details class="transition"><summary>Réattribuer</summary><form method="post" action="' . $e($ici) . '" class="formulaire-transition">' . Vue::csrf($app) . '<input type="hidden" name="op" value="reattribuer">'
        . '<label class="champ" for="c-associe"><span>Associé</span><select id="c-associe" name="associe">' . $optAssocies . '</select></label><button class="btn btn-petit btn-sombre" type="submit">Réattribuer</button></form></details>';
    $donnees = Auth::peut($app->utilisateur, 'effacer') && !$efface && $d['contact_id'] ? '<p class="petit"><a href="' . $e(Vue::url('donnees', ['contact' => $d['contact_id']])) . '">Exporter ou effacer les données de cette personne</a></p>' : '';
    $actions = '<section class="panneau panneau-actions" aria-labelledby="t-actions"><h2 id="t-actions">Actions</h2><div class="actions-fiche">' . $formsActions . $reattribuer . $donnees . '</div></section>';
    $barre = '<div class="barre-action-mobile">' . ($appeler ?: ($mail ?: '<span></span>')) . '<a class="btn" href="#t-actions">Résultat et actions</a></div>';

    return Vue::page($app, 'fiche', $d['ref'] . ' · ' . $d['nom_complet'], $entete . '<div class="fiche-corps"><div class="pile">' . $projet . $score . $attrib . $historique . $notes
        . '</div><div class="pile colonne-actions">' . $actions . $coord . $offre . '</div></div>' . $barre);
};
