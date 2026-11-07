<?php
/** Export CSV de la liste filtrée (associés seulement, journalisé). Séparateur « ; » et BOM pour Excel. */
declare(strict_types=1);

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Demandes;
use AndyConstruct\Admin\Http;
use AndyConstruct\Api\Canaux;

return static function (App $app): string {
    $f = [];
    foreach (['q', 'periode', 'statut', 'priorite', 'canal', 'type_client', 'associe', 'retard', 'tri'] as $k) {
        $f[$k] = mb_substr(Http::get($k), 0, 80);
    }
    $lignes = $app->demandes->liste($f + ['statut' => $f['statut'] ?: 'ouvertes'], $app->utilisateur['id']);
    $app->audit('export', 'demande', null, ['lignes' => count($lignes), 'filtres' => array_keys(array_filter($f))]);
    // Une cellule qui commence par = + - @ serait une formule dans un tableur : on la neutralise.
    $cellule = static fn ($v): string => preg_match('/^[=+\-@\t\r]/', (string) $v) ? "'" . $v : (string) $v;
    $sortie = fopen('php://temp', 'w+');
    fwrite($sortie, "\xEF\xBB\xBF");
    fputcsv($sortie, ['Référence', 'Reçue le', 'Nom', 'Téléphone', 'E-mail', 'Type de client', 'Travaux', 'NPA', 'Commune', 'Zone', 'Priorité', 'Score', 'Canal', 'Statut', 'Montant HT', 'Associé', 'Test'], ';', '"', '');
    foreach ($lignes as $d) {
        fputcsv($sortie, array_map($cellule, [
            $d['ref'], $d['recue']?->format('Y-m-d H:i'), $d['nom_complet'], $d['telephone_affiche'], $d['email'],
            Demandes::TYPES_CLIENT[$d['type_client'] ?? ''] ?? '', Demandes::libelleTravaux($d), $d['npa'], $d['commune'], $d['zone'],
            $d['priorite_eff'], $d['score'], Canaux::libelle($d['canal_eff']), Demandes::STATUTS[$d['statut']] ?? $d['statut'],
            $d['montant'] !== null ? number_format((float) $d['montant'], 2, '.', '') : '', $d['associe_nom'], (int) $d['mode_test'] ? 'oui' : '',
        ]), ';', '"', '');
    }
    rewind($sortie);
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="demandes-' . $app->maintenant->format('Y-m-d') . '.csv"');
    fpassthru($sortie);
    exit;
};
