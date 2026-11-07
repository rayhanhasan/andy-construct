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
    /** id => [libellé, catégories Source.php, payant (dépense rattachée), libellé court] */
    public const LISTE = [
        'google_ads' => ['Google Ads', ['google-ads'], true, 'Google Ads'],
        'meta' => ['Meta', ['meta'], true, 'Meta'],
        'linkedin' => ['LinkedIn', ['linkedin'], true, 'LinkedIn'],
        'b2b' => ['Prospection B2B', ['b2b'], true, 'B2B'],
        'recherche' => ['Recherche Google', ['recherche-google'], false, 'Recherche'],
        'fiche' => ['Fiche Google', ['carte-google'], false, 'Fiche Google'],
        'recommandation' => ['Recommandation et partenaires', ['recommandation', 'partenaire'], false, 'Recommandation'],
        'clients' => ['Clients existants', ['client-existant', 'crm'], false, 'Clients'],
        'guides' => ['Guides', ['aimant'], false, 'Guides'],
        'annuaires' => ['Annuaires et plateformes', ['annuaire', 'plateforme'], false, 'Annuaires'],
        'panneaux' => ['Panneaux et véhicules', ['panneau-vehicule'], false, 'Panneaux'],
        'autres' => ['Autres et inconnu', ['site-referent', 'autre', 'direct-inconnu', 'appel-direct'], false, 'Autres'],
    ];

    /** Canaux dont la dépense entre dans le CPL de la vue d'ensemble. */
    public const PAYANTS = ['google_ads', 'meta', 'linkedin', 'b2b'];

    public static function libelle(?string $id): string
    {
        return self::LISTE[(string) $id][0] ?? 'Autres et inconnu';
    }

    public static function court(?string $id): string
    {
        return self::LISTE[(string) $id][3] ?? 'Autres';
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
