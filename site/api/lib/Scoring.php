<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Score (0-100 + bonus) et priorité A / B / C / hors-cible d'une demande,
 * selon la grille de data/scoring.json (strategie-acquisition.md §2.3-2.5).
 *
 * Le score ordonne les rappels ; il ne décide jamais seul : toutes les demandes
 * sont rappelées et un associé valide toute réponse « hors cible ».
 */
final class Scoring
{
    /** @param array<string, mixed> $grille */
    public function __construct(private array $grille)
    {
    }

    public static function depuisFichier(string $chemin): self
    {
        return new self(json_decode((string) file_get_contents($chemin), true, 32, JSON_THROW_ON_ERROR));
    }

    /**
     * @param array{type_client?: string, service?: string, surface?: string, zone?: int|string,
     *   delai?: string, source_categorie?: string, connu_par?: string, canal?: string,
     *   formulaire?: string, message?: string, telephone?: bool, nb_fichiers?: int} $d
     * @return array{score: int, priorite: string, detail: list<array{critere: string, valeur: string, points: int}>,
     *   regles: list<string>, hors_cible: list<string>}
     */
    public function calculer(array $d): array
    {
        $g = $this->grille;
        $detail = [];
        $regles = [];
        $horsCible = [];
        $ajouter = static function (string $critere, string $valeur, int $points) use (&$detail): void {
            $detail[] = ['critere' => $critere, 'valeur' => $valeur, 'points' => $points];
        };

        $type = (string) ($d['type_client'] ?? '');
        $ajouter('type_client', $type ?: 'non précisé', (int) ($g['type_client'][$type] ?? $g['type_client'][''] ?? 0));

        $service = (string) ($d['service'] ?? '');
        $pointsService = array_key_exists($service, $g['service']) ? $g['service'][$service] : ($g['service'][''] ?? 0);
        if ($pointsService === null) {
            $horsCible[] = 'service hors des 4 prestations';
            $pointsService = 0;
        }
        $ajouter('service', $service ?: 'non précisé', (int) $pointsService);

        $surface = (string) ($d['surface'] ?? '');
        $ajouter('surface', $surface ?: 'non précisée', (int) ($g['surface'][$surface] ?? $g['surface'][''] ?? 0));

        $zone = (string) ($d['zone'] ?? 'inconnue');
        $pointsZone = array_key_exists($zone, $g['zone']) ? $g['zone'][$zone] : $g['zone']['inconnue'];
        if ($pointsZone === null) {
            $horsCible[] = 'hors Suisse romande';
            $pointsZone = 0;
        } elseif ($zone === '3') {
            $r = $g['regles'];
            if (in_array($type, $r['zone3_sans_penalite_types_client'], true)
                || in_array($surface, $r['zone3_sans_penalite_surfaces'], true)) {
                $pointsZone = $g['zone']['2'];
                $regles[] = 'zone 3 sans pénalité (B2B ou plus de 50 m²)';
            }
        }
        $ajouter('zone', $zone, (int) $pointsZone);

        $delai = (string) ($d['delai'] ?? '');
        $ajouter('delai', $delai ?: 'non précisé', (int) ($g['delai'][$delai] ?? $g['delai'][''] ?? 0));

        $categorie = (string) ($d['source_categorie'] ?? 'direct-inconnu');
        $pointsSource = (int) ($g['source'][$categorie] ?? $g['source']['autre'] ?? 0);
        $libelleSource = $categorie;
        $connuPar = (string) ($d['connu_par'] ?? '');
        if ($connuPar !== '' && isset($g['connu_par'][$connuPar])) {
            $catDeclaree = $g['connu_par'][$connuPar];
            $pointsDeclares = (int) ($g['source'][$catDeclaree] ?? 0);
            if ($pointsDeclares > $pointsSource) {
                $pointsSource = $pointsDeclares;
                $libelleSource = $catDeclaree . ' (déclaré)';
            }
        }
        $ajouter('source', $libelleSource, $pointsSource);

        $telephone = (bool) ($d['telephone'] ?? false);
        $message = trim((string) ($d['message'] ?? ''));
        if ((int) ($d['nb_fichiers'] ?? 0) > 0) {
            $ajouter('bonus', 'photo ou plan joint', (int) $g['bonus']['fichier_joint']);
        }
        // Sur une saisie téléphonique, le numéro est toujours connu : pas de bonus.
        if ($telephone && ($d['canal'] ?? 'site') === 'site') {
            $ajouter('bonus', 'téléphone fourni', (int) $g['bonus']['telephone_fourni']);
        }
        if ($message === '' && !$telephone) {
            $ajouter('malus', 'message vide et aucun téléphone', (int) $g['bonus']['message_vide_sans_telephone']);
        }

        $score = array_sum(array_column($detail, 'points'));
        $priorite = $score >= $g['seuils']['A'] ? 'A' : ($score >= $g['seuils']['B'] ? 'B' : 'C');

        $r = $g['regles'];
        if ($priorite === 'C' && in_array($type, $r['plancher_B_types_client'], true)) {
            $priorite = 'B';
            $regles[] = 'commune, régie ou architecte : jamais en dessous de B';
        }
        if ($priorite === 'C' && in_array((string) ($d['formulaire'] ?? ''), $r['plancher_B_formulaires'], true)) {
            $priorite = 'B';
            $regles[] = 'demande de rappel : jamais en dessous de B';
        }
        if ($priorite !== 'A' && $delai === $r['urgence_delai'] && self::contientMotUrgent($message, $r['urgence_mots'])) {
            $priorite = 'A';
            $regles[] = 'dégât ou fin de bail imminente : A';
        }
        if ($horsCible) {
            $priorite = 'hors-cible';
        }

        return [
            'score' => $score,
            'priorite' => $priorite,
            'detail' => $detail,
            'regles' => $regles,
            'hors_cible' => $horsCible,
        ];
    }

    /** @param list<string> $mots */
    private static function contientMotUrgent(string $message, array $mots): bool
    {
        $texte = mb_strtolower($message);
        foreach ($mots as $mot) {
            if ($mot !== '' && str_contains($texte, mb_strtolower($mot))) {
                return true;
            }
        }
        return false;
    }
}
