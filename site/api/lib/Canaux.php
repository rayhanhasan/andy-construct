<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Canaux marketing affichés (docs/v4/admin/plan-dashboard-admin.md §5.4) :
 * regroupement des catégories de Source.php, une demande = un canal.
 *
 * Appel saisi (« appel-direct ») ou demande web « direct-inconnu » : le canal
 * vient de la réponse « Comment nous avez-vous connus ? » (même table que
 * scoring.json → connu_par) et porte la mention « déclaré ».
 */
final class Canaux
{
    /** id => [libellé, catégories Source.php, payant (dépense rattachée)] */
    public const LISTE = [
        'google_ads' => ['Google Ads', ['google-ads'], true],
        'meta' => ['Meta', ['meta'], true],
        'linkedin' => ['LinkedIn', ['linkedin'], true],
        'b2b' => ['Prospection B2B', ['b2b'], true],
        'recherche' => ['Recherche Google', ['recherche-google'], false],
        'fiche' => ['Fiche Google', ['carte-google'], false],
        'recommandation' => ['Recommandation et partenaires', ['recommandation', 'partenaire'], false],
        'clients' => ['Clients existants', ['client-existant', 'crm'], false],
        'guides' => ['Guides', ['aimant'], false],
        'annuaires' => ['Annuaires et plateformes', ['annuaire', 'plateforme'], false],
        'panneaux' => ['Panneaux et véhicules', ['panneau-vehicule'], false],
        'autres' => ['Autres et inconnu', ['site-referent', 'autre', 'direct-inconnu', 'appel-direct'], false],
    ];

    /** Canaux dont la dépense entre dans le CPL de la vue d'ensemble. */
    public const PAYANTS = ['google_ads', 'meta', 'linkedin', 'b2b'];

    public static function libelle(?string $id): string
    {
        return self::LISTE[(string) $id][0] ?? 'Autres et inconnu';
    }

    public static function depuisCategorie(string $categorie): string
    {
        foreach (self::LISTE as $id => [, $categories]) {
            if (in_array($categorie, $categories, true)) {
                return $id;
            }
        }
        return 'autres';
    }

    /**
     * @param array<string, string> $connuParVersCategorie scoring.json → connu_par
     * @return array{0: string, 1: bool} [canal, déclaré]
     */
    public static function deduire(string $categorie, string $connuPar, array $connuParVersCategorie): array
    {
        if (in_array($categorie, ['appel-direct', 'direct-inconnu'], true) && $connuPar !== '' && isset($connuParVersCategorie[$connuPar])) {
            return [self::depuisCategorie((string) $connuParVersCategorie[$connuPar]), true];
        }
        return [self::depuisCategorie($categorie), false];
    }
}
