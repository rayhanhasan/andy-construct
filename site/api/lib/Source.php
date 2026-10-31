<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Normalisation de la source d'une demande (strategie-acquisition.md §6.2) :
 * 1. utm_source / utm_medium ; 2. gclid (avec consentement) ; 3. référent ;
 * 4. canal (saisie téléphonique) ; 5. « direct / inconnu ».
 * Le champ déclaratif « connu_par » est traité à part par le scoring.
 */
final class Source
{
    private const PLATEFORMES = ['renovero', 'houzz', 'ofri', 'travaux', 'homeadvisor', 'local-pros', 'devisplus'];
    private const ANNUAIRES = ['localch', 'local.ch', 'searchch', 'search.ch', 'gge', 'kompass', 'architecteromand'];
    private const MOTEURS = ['google.', 'bing.', 'duckduckgo.', 'ecosia.', 'qwant.', 'yahoo.', 'search.brave.', 'startpage.'];

    /**
     * @param array{utm_source?: string, utm_medium?: string, utm_campaign?: string, gclid?: string,
     *   referent?: string, canal?: string, formulaire?: string} $s
     * @return array{categorie: string, libelle: string}
     */
    public static function normaliser(array $s, string $hoteSite = 'andyconstruct.ch'): array
    {
        $source = strtolower(trim((string) ($s['utm_source'] ?? '')));
        $medium = strtolower(trim((string) ($s['utm_medium'] ?? '')));
        $campagne = strtolower(trim((string) ($s['utm_campaign'] ?? '')));

        if (($s['canal'] ?? 'site') === 'telephone') {
            return ['categorie' => 'appel-direct', 'libelle' => 'appel téléphonique (saisie express)'];
        }
        if ($source !== '' || $medium !== '') {
            $libelle = trim("$source / $medium", ' /');
            $categorie = match (true) {
                $source === 'recommandation' => 'recommandation',
                $source === 'partenaire' => 'partenaire',
                $source === 'courrier', $source === 'newsletter' => 'b2b',
                $source === 'crm' && str_contains($campagne, 'entretien') => 'client-existant',
                $source === 'crm' && str_contains($campagne, 'aimant') => 'aimant',
                $source === 'crm' => 'crm',
                in_array($source, ['panneau', 'vehicule'], true) => 'panneau-vehicule',
                in_array($medium, ['cpc', 'ppc', 'paid-search', 'sem'], true) => 'google-ads',
                $source === 'linkedin' => 'linkedin',
                in_array($source, ['meta', 'facebook', 'instagram', 'fb', 'ig'], true) => 'meta',
                $medium === 'organic-local' => 'carte-google',
                in_array($source, self::ANNUAIRES, true) => 'annuaire',
                in_array($source, self::PLATEFORMES, true) => 'plateforme',
                $source === 'google' || $source === 'bing' => 'recherche-google',
                default => 'autre',
            };
            return ['categorie' => $categorie, 'libelle' => $libelle];
        }
        if (trim((string) ($s['gclid'] ?? '')) !== '') {
            return ['categorie' => 'google-ads', 'libelle' => 'google / cpc (gclid)'];
        }
        $referent = strtolower(trim((string) ($s['referent'] ?? '')));
        if ($referent !== '' && !str_ends_with($referent, $hoteSite)) {
            foreach (self::MOTEURS as $moteur) {
                if (str_contains($referent, $moteur)) {
                    return ['categorie' => 'recherche-google', 'libelle' => "recherche naturelle ($referent)"];
                }
            }
            $categorie = match (true) {
                str_contains($referent, 'facebook.') || str_contains($referent, 'instagram.') => 'meta',
                str_contains($referent, 'linkedin.') => 'linkedin',
                (bool) array_filter(self::ANNUAIRES, static fn ($a) => str_contains($referent, $a)) => 'annuaire',
                (bool) array_filter(self::PLATEFORMES, static fn ($p) => str_contains($referent, $p)) => 'plateforme',
                default => 'site-referent',
            };
            return ['categorie' => $categorie, 'libelle' => "lien depuis $referent"];
        }
        if (($s['formulaire'] ?? '') === 'envoi_postal_guide') {
            return ['categorie' => 'aimant', 'libelle' => 'guide (accès direct)'];
        }
        return ['categorie' => 'direct-inconnu', 'libelle' => 'direct / inconnu'];
    }
}
