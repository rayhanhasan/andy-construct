<?php
/** Score et priorité pendant la saisie d'un appel (même grille et mêmes règles que Traitement). */
declare(strict_types=1);

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Demandes;
use AndyConstruct\Admin\Format;
use AndyConstruct\Admin\Http;
use AndyConstruct\Api\Localite;
use AndyConstruct\Api\Telephone;
use AndyConstruct\Api\Validateur;

return static function (App $app): string {
    if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
        Http::json(['ok' => false], 405);
    }
    $travaux = array_values(array_intersect(array_filter((array) ($_POST['travaux'] ?? []), 'is_string'), array_keys(Demandes::TRAVAUX)));
    $saisieCommune = mb_substr(Http::post('commune'), 0, 100);
    [$npa, $commune] = preg_match('/^\s*([1-9]\d{3})\b\s*(.*)$/u', $saisieCommune, $m) ? [$m[1], trim($m[2])] : ['', trim($saisieCommune)];
    $localite = $npa === '' && $commune === '' ? ['zone' => 'inconnue', 'npa' => '', 'commune' => ''] : Localite::depuisFichier(dirname(__DIR__, 2) . '/api/data/zones.json')->resoudre($npa, $commune);
    $pick = static fn (string $cle, array $liste) => array_key_exists(Http::post($cle), $liste) ? Http::post($cle) : '';
    $sc = $app->scoring->calculer([
        'type_client' => $pick('type_client', Demandes::TYPES_CLIENT),
        'service' => Validateur::servicePrincipal($travaux),
        'surface' => $pick('surface', Demandes::SURFACES),
        'zone' => $localite['zone'],
        'delai' => $pick('delai', Demandes::DELAIS),
        'source_categorie' => 'appel-direct',
        'connu_par' => Http::post('connu_par'),
        'canal' => 'telephone',
        'formulaire' => 'devis',
        'message' => mb_substr(Http::post('note'), 0, 3000),
        'telephone' => true,
        'nb_fichiers' => 0,
    ]);
    $echeance = $app->heures->echeance($sc['priorite'], $app->maintenant);
    $existant = null;
    $tel = Telephone::normaliser(Http::post('telephone'));
    if ($tel !== null) {
        $existant = $app->base->un('SELECT d.ref, c.prenom, c.nom FROM contact c JOIN demande d ON d.contact_id = c.id WHERE c.telephone_e164 = ? AND c.anonymise_le IS NULL ORDER BY d.recue_le DESC LIMIT 1', [$tel['e164']]);
    }
    Http::json([
        'ok' => true,
        'score' => $sc['score'],
        'priorite' => $sc['priorite'],
        'detail' => array_map(static fn ($l) => ['critere' => Demandes::CRITERES[$l['critere']] ?? $l['critere'], 'valeur' => Demandes::libelleCritere((string) $l['critere'], (string) $l['valeur']), 'points' => $l['points']], $sc['detail']),
        'regles' => array_merge($sc['regles'], $sc['hors_cible']),
        'echeance' => Format::dateH($echeance),
        'zone' => (string) $localite['zone'],
        'npa' => (string) ($localite['npa'] ?? ''),
        'existant' => $existant ? ['ref' => $existant['ref'], 'nom' => trim(($existant['prenom'] ?? '') . ' ' . ($existant['nom'] ?? ''))] : null,
    ]);
};
