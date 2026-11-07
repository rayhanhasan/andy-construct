<?php
declare(strict_types=1);

namespace AndyConstruct\Admin;

use AndyConstruct\Api\Base;
use AndyConstruct\Api\Canaux;

/**
 * Indicateurs du plan admin §5 (noms partagés avec le plan d'acquisition v4).
 *
 * Règles communes (§5.3) : mois civil à l'heure de Zurich ; mois en cours arrêté
 * à l'instant ; demandes de test, doublons et guides exclus ; demandes effacées
 * comptées ; division par zéro → null (« — »).
 */
final class Indicateurs
{
    private \DateTimeZone $tz;

    public function __construct(private App $app)
    {
        $this->tz = new \DateTimeZone('Europe/Zurich');
    }

    /** @return array{0: \DateTimeImmutable, 1: \DateTimeImmutable} début inclus, fin exclue (heure de Zurich) */
    public function bornes(string $mois): array
    {
        $debut = new \DateTimeImmutable($mois . '-01 00:00', $this->tz);
        return [$debut, $debut->modify('+1 month')];
    }

    public static function moisDe(\DateTimeImmutable $t): string
    {
        return $t->setTimezone(new \DateTimeZone('Europe/Zurich'))->format('Y-m');
    }

    public static function moisDecale(string $mois, int $n): string
    {
        return (new \DateTimeImmutable($mois . '-01 12:00'))->modify(($n >= 0 ? '+' : '') . $n . ' month')->format('Y-m');
    }

    /** Demandes comptées (§5.1 « demande enregistrée ») reçues dans [début, fin[. */
    public function demandes(\DateTimeImmutable $debut, \DateTimeImmutable $fin): array
    {
        return $this->app->base->tous(
            "SELECT d.id, d.ref, d.recue_le, d.canal, d.statut, COALESCE(d.priorite_corrigee, d.priorite) AS prio,
                    d.premier_contact_le, d.premier_appel_le, d.echeance_initiale_le, d.type_client, d.motif_perte,
                    COALESCE(a.canal_corrige, a.canal_marketing, 'autres') AS canal_m
             FROM demande d LEFT JOIN attribution a ON a.demande_id = d.id
             WHERE d.mode_test = 0 AND d.statut NOT IN ('doublon', 'guide') AND d.formulaire <> 'envoi_postal_guide'
               AND d.recue_le >= ? AND d.recue_le < ?",
            [Base::utc($debut), Base::utc($fin)]
        );
    }

    /** Offres (une ligne par demande comptée) : premier envoi, signature, montant signé, canal d'origine. */
    public function offres(): array
    {
        return $this->app->base->tous(
            "SELECT o.demande_id, MIN(o.envoyee_le) AS envoyee_le,
                    MAX(CASE WHEN o.statut = 'signee' THEN o.signee_le END) AS signee_le,
                    SUM(CASE WHEN o.statut = 'signee' THEN o.montant_signe_ht ELSE 0 END) AS montant_signe,
                    COALESCE(a.canal_corrige, a.canal_marketing, 'autres') AS canal_m
             FROM offre o JOIN demande d ON d.id = o.demande_id LEFT JOIN attribution a ON a.demande_id = d.id
             WHERE d.mode_test = 0 AND d.statut NOT IN ('doublon', 'guide')
             GROUP BY o.demande_id, a.canal_corrige, a.canal_marketing"
        );
    }

    public function depense(array $mois, ?array $canaux = null): float
    {
        if ($mois === []) {
            return 0.0;
        }
        $p = array_map(static fn ($m) => $m . '-01', $mois);
        $sql = 'SELECT COALESCE(SUM(montant_ht), 0) FROM depense WHERE mois IN (' . implode(',', array_fill(0, count($p), '?')) . ')';
        if ($canaux !== null) {
            $sql .= ' AND canal_marketing IN (' . implode(',', array_fill(0, count($canaux), '?')) . ')';
            $p = array_merge($p, $canaux);
        }
        return (float) $this->app->base->valeur($sql, $p);
    }

    // ------------------------------------------------------------- objectifs

    /** Mois M1 (mise en ligne) : paramètre, sinon mois de la première demande comptée. */
    public function moisMiseEnLigne(): string
    {
        $p = (string) $this->app->parametre('mise_en_ligne');
        if (preg_match('/^\d{4}-\d{2}$/', $p)) {
            return $p;
        }
        $premiere = $this->app->base->valeur("SELECT MIN(recue_le) FROM demande WHERE mode_test = 0 AND statut <> 'guide'");
        return $premiere ? self::moisDe(Base::local((string) $premiere)) : self::moisDe($this->app->maintenant);
    }

    public function numeroMois(string $mois): int
    {
        [$a1, $m1] = array_map('intval', explode('-', $this->moisMiseEnLigne()));
        [$a, $m] = array_map('intval', explode('-', $mois));
        return ($a - $a1) * 12 + ($m - $m1) + 1;
    }

    /** Objectif du mois : interpolation linéaire entre M3, M6 et M12 (décision G6) ; null avant M3. */
    public function objectif(string $indicateur, string $mois): ?float
    {
        $jalons = (array) (($this->app->parametre('objectifs') ?? [])[$indicateur] ?? App::PARAMETRES_DEFAUT['objectifs'][$indicateur] ?? []);
        if (count($jalons) < 3) {
            return null;
        }
        $n = $this->numeroMois($mois);
        $v3 = (float) $jalons[3];
        $v6 = (float) $jalons[6];
        $v12 = (float) $jalons[12];
        return match (true) {
            $n < 3 => null,
            $n <= 6 => $v3 + ($v6 - $v3) * ($n - 3) / 3,
            $n <= 12 => $v6 + ($v12 - $v6) * ($n - 6) / 6,
            default => $v12,
        };
    }

    // ---------------------------------------------------------- indicateurs

    /** Les 5 indicateurs de la vue d'ensemble pour un mois, arrêtés à $asOf. */
    public function mois(string $mois): array
    {
        [$debut, $fin] = $this->bornes($mois);
        $courant = $mois === self::moisDe($this->app->maintenant);
        $asOf = $courant ? $this->app->maintenant : $fin->modify('-1 second');
        $dm = $this->demandes($debut, min($fin, $this->app->maintenant->modify('+1 second')));
        $prec = self::moisDecale($mois, -1);
        $dmPrec = $this->demandes(...$this->bornes($prec));

        $comptes = self::comptes($dm);
        $joursMois = $this->app->heures->joursOuvrablesMois($mois);
        $joursEcoules = $courant ? $this->app->heures->joursOuvrablesMois($mois, $this->app->maintenant) : $joursMois;
        $projection = $courant && $joursEcoules > 0 ? count($dm) * $joursMois / $joursEcoules : null;

        // Délai de premier contact (heures ouvrables), appels entrants exclus.
        $delais = ['A' => [], 'tous' => []];
        $dansDelai = ['ok' => 0, 'total' => 0];
        foreach ($dm as $d) {
            if ($d['canal'] === 'telephone') {
                continue;
            }
            $recue = Base::local($d['recue_le']);
            if ($d['premier_contact_le']) {
                $min = $this->app->heures->minutesOuvrables($recue, Base::local($d['premier_contact_le']));
                $delais['tous'][] = $min;
                if ($d['prio'] === 'A') {
                    $delais['A'][] = $min;
                }
            }
            $echeance = Base::local($d['echeance_initiale_le']);
            if ($d['prio'] === 'A' && $echeance !== null && $echeance <= $asOf) {
                $dansDelai['total']++;
                $premier = array_filter([$d['premier_appel_le'], $d['premier_contact_le']]);
                if ($premier && Base::local(min($premier)) <= $echeance) {
                    $dansDelai['ok']++;
                }
            }
        }

        $offres = $this->offres();
        $tdo = $this->tauxDemandeOffre($mois, $offres, count($dmPrec));
        $tos = $this->cohorteOffreSignee($asOf, $offres);
        $signees = array_values(array_filter($offres, fn ($o) => $o['signee_le'] && substr((string) $o['signee_le'], 0, 7) === $mois && $o['signee_le'] <= $asOf->format('Y-m-d')));
        $ca = array_sum(array_map(static fn ($o) => (float) $o['montant_signe'], $signees));

        $depPayante = $this->depense([$mois], Canaux::PAYANTS);
        $dmPayantes = count(array_filter($dm, static fn ($d) => in_array($d['canal_m'], Canaux::PAYANTS, true)));
        $cplMax = $this->cplMax($asOf, $this->tauxDemandeOffreTrimestre($mois, $offres), $tos['taux'], $mois);

        return [
            'mois' => $mois,
            'courant' => $courant,
            'as_of' => $asOf,
            'm' => $this->numeroMois($mois),
            'jours_ouvrables' => $joursMois,
            'jours_ecoules' => $joursEcoules,
            'demandes' => count($dm),
            'demandes_prec' => count($dmPrec),
            'projection' => $projection,
            'comptes' => $comptes,
            'part_ab' => self::partAb($comptes),
            'delai_a' => self::mediane($delais['A']),
            'delai_a_n' => count($delais['A']),
            'delai_tous' => self::mediane($delais['tous']),
            'dans_delai' => $dansDelai,
            'demande_offre' => $tdo,
            'demande_offre_prec' => $this->tauxDemandeOffre($prec, $offres, count($this->demandes(...$this->bornes(self::moisDecale($mois, -2))))),
            'offre_signee' => $tos,
            'ca_signe' => $ca,
            'nb_signes' => count($signees),
            'depense_payante' => $depPayante,
            'demandes_payantes' => $dmPayantes,
            'cpl' => $dmPayantes > 0 && $depPayante > 0 ? $depPayante / $dmPayantes : null,
            'cpl_max' => $cplMax,
            'objectifs' => [
                'demandes' => $this->objectif('demandes', $mois),
                'part_ab' => ($o = $this->objectif('part_ab', $mois)) === null ? null : $o / 100,
                'delai_a' => ($o = $this->objectif('delai_a_h', $mois)) === null ? null : $o * 60,
                'demande_offre' => ($o = $this->objectif('demande_offre', $mois)) === null ? null : $o / 100,
                'offre_signee' => ($o = $this->objectif('offre_signee', $mois)) === null ? null : $o / 100,
                'ca' => ($o = $this->objectif('chantiers', $mois)) === null ? null : $o * (float) $this->app->parametre('panier_reference'),
            ],
        ];
    }

    /** @return array{A: int, B: int, C: int, hors_cible: int} */
    public static function comptes(array $demandes): array
    {
        $c = ['A' => 0, 'B' => 0, 'C' => 0, 'hors_cible' => 0];
        foreach ($demandes as $d) {
            $p = (string) $d['prio'];
            $c[isset($c[$p]) ? $p : 'hors_cible']++;
        }
        return $c;
    }

    public static function partAb(array $c): ?float
    {
        $q = $c['A'] + $c['B'] + $c['C'];
        return $q > 0 ? ($c['A'] + $c['B']) / $q : null;
    }

    public static function mediane(array $v): ?float
    {
        if ($v === []) {
            return null;
        }
        sort($v);
        $k = intdiv(count($v), 2);
        return count($v) % 2 ? (float) $v[$k] : ($v[$k - 1] + $v[$k]) / 2;
    }

    /** Taux demande→offre : offres envoyées en M (premier envoi) / demandes enregistrées en M−1. */
    public function tauxDemandeOffre(string $mois, array $offres, int $demandesMoisPrecedent): ?array
    {
        $n = count(array_filter($offres, static fn ($o) => substr((string) $o['envoyee_le'], 0, 7) === $mois));
        return $demandesMoisPrecedent > 0 ? ['taux' => $n / $demandesMoisPrecedent, 'offres' => $n, 'demandes' => $demandesMoisPrecedent, 'mois_demandes' => self::moisDecale($mois, -1)] : null;
    }

    /**
     * Taux demande→offre lissé pour le CPL max : 3 mois complets précédant $mois
     * (somme des offres / somme des demandes du mois d'avant), moins sensible aux petits nombres.
     */
    public function tauxDemandeOffreTrimestre(string $mois, array $offres): ?float
    {
        $o = $d = 0;
        for ($i = 1; $i <= 3; $i++) {
            $m = self::moisDecale($mois, -$i);
            $n = count($this->demandes(...$this->bornes(self::moisDecale($m, -1))));
            $t = $this->tauxDemandeOffre($m, $offres, $n);
            if ($t !== null) {
                $o += $t['offres'];
                $d += $t['demandes'];
            }
        }
        return $d > 0 ? $o / $d : null;
    }

    /** Taux offre→signée : cohorte des offres envoyées entre J−180 et J−60. */
    public function cohorteOffreSignee(\DateTimeImmutable $asOf, array $offres): array
    {
        $debut = $asOf->modify('-180 days')->format('Y-m-d');
        $fin = $asOf->modify('-60 days')->format('Y-m-d');
        $cohorte = array_filter($offres, static fn ($o) => $o['envoyee_le'] >= $debut && $o['envoyee_le'] <= $fin);
        $signees = count(array_filter($cohorte, static fn ($o) => $o['signee_le'] && $o['signee_le'] <= $asOf->format('Y-m-d')));
        return ['taux' => $cohorte ? $signees / count($cohorte) : null, 'signees' => $signees, 'offres' => count($cohorte)];
    }

    /** Panier moyen : CA signé / chantiers signés sur 6 mois glissants. */
    public function panierMoyen(\DateTimeImmutable $asOf, ?array $offres = null): ?float
    {
        $offres ??= $this->offres();
        $debut = $asOf->modify('-182 days')->format('Y-m-d');
        $s = array_filter($offres, static fn ($o) => $o['signee_le'] && $o['signee_le'] > $debut && $o['signee_le'] <= $asOf->format('Y-m-d'));
        return $s ? array_sum(array_map(static fn ($o) => (float) $o['montant_signe'], $s)) / count($s) : null;
    }

    /**
     * CPL max = panier moyen × marge brute × taux demande→offre × taux offre→signée
     * (plan d'acquisition v4 §2.5). Terme manquant : valeur de référence (panier) ou
     * objectif du mois (taux), signalé dans « sources ».
     */
    public function cplMax(\DateTimeImmutable $asOf, ?float $tdo, ?float $tos, string $mois): ?array
    {
        $sources = [];
        $panier = $this->panierMoyen($asOf);
        if ($panier === null) {
            $panier = (float) $this->app->parametre('panier_reference');
            $sources[] = 'panier de référence';
        }
        if ($tdo === null) {
            $tdo = ($o = $this->objectif('demande_offre', $mois) ?? (float) App::PARAMETRES_DEFAUT['objectifs']['demande_offre'][3]) / 100;
            $sources[] = 'objectif demande→offre';
        }
        if ($tos === null) {
            $tos = ($o = $this->objectif('offre_signee', $mois) ?? (float) App::PARAMETRES_DEFAUT['objectifs']['offre_signee'][3]) / 100;
            $sources[] = 'objectif offre→signée';
        }
        $marge = (float) $this->app->parametre('marge_brute');
        if ($panier <= 0 || $marge <= 0) {
            return null;
        }
        $max = $panier * $marge * $tdo * $tos;
        return ['max' => $max, 'cible' => $max / 3, 'panier' => $panier, 'marge' => $marge, 'tdo' => $tdo, 'tos' => $tos, 'sources' => $sources];
    }

    /** Entonnoir des demandes reçues depuis $debut (état aujourd'hui). */
    public function entonnoir(\DateTimeImmutable $debut): array
    {
        $dm = $this->demandes($debut, $this->app->maintenant->modify('+1 second'));
        $ids = array_map(static fn ($d) => (int) $d['id'], $dm);
        $avecVisite = $avecOffre = $avecSignature = [];
        if ($ids) {
            $m = implode(',', array_fill(0, count($ids), '?'));
            $avecVisite = array_flip(array_map('intval', array_column($this->app->base->tous("SELECT DISTINCT demande_id FROM visite WHERE statut IN ('planifiee', 'faite') AND demande_id IN ($m)", $ids), 'demande_id')));
            $avecOffre = array_flip(array_map('intval', array_column($this->app->base->tous("SELECT DISTINCT demande_id FROM offre WHERE demande_id IN ($m)", $ids), 'demande_id')));
            $avecSignature = array_flip(array_map('intval', array_column($this->app->base->tous("SELECT DISTINCT demande_id FROM offre WHERE statut = 'signee' AND demande_id IN ($m)", $ids), 'demande_id')));
        }
        $motifs = [];
        foreach ($dm as $d) {
            if ($d['statut'] === 'perdue') {
                $motifs[$d['motif_perte'] ?: 'autre'] = ($motifs[$d['motif_perte'] ?: 'autre'] ?? 0) + 1;
            }
        }
        arsort($motifs);
        return [
            'etapes' => [
                ['Demandes enregistrées', count($dm)],
                ['Qualifiées (A, B, C)', count(array_filter($dm, static fn ($d) => in_array($d['prio'], ['A', 'B', 'C'], true)))],
                ['Visite planifiée', count(array_filter($dm, static fn ($d) => isset($avecVisite[(int) $d['id']])))],
                ['Offre envoyée', count(array_filter($dm, static fn ($d) => isset($avecOffre[(int) $d['id']])))],
                ['Signée', count(array_filter($dm, static fn ($d) => isset($avecSignature[(int) $d['id']])))],
            ],
            'perdues' => $motifs,
            'en_cours' => count(array_filter($dm, static fn ($d) => $d['statut'] === 'offre_envoyee')),
        ];
    }

    /** Demandes par mois et par priorité, avec l'objectif. */
    public function parMois(array $listeMois): array
    {
        $r = [];
        foreach ($listeMois as $m) {
            [$debut, $fin] = $this->bornes($m);
            $c = self::comptes($this->demandes($debut, $fin));
            $r[] = ['mois' => $m, 'comptes' => $c, 'total' => array_sum($c), 'objectif' => $this->objectif('demandes', $m)];
        }
        return $r;
    }

    /** Tableau Acquisition par canal (§3.3 E8, formules §5.2). */
    public function acquisition(array $listeMois): array
    {
        sort($listeMois);
        $debut = $this->bornes($listeMois[0])[0];
        $fin = min($this->bornes(end($listeMois))[1], $this->app->maintenant->modify('+1 second'));
        $dm = $this->demandes($debut, $fin);
        $offres = $this->offres();
        $marge = (float) $this->app->parametre('marge_brute');
        $lignes = [];
        foreach (Canaux::LISTE as $id => [$libelle, , $payant]) {
            $d = array_filter($dm, static fn ($x) => $x['canal_m'] === $id);
            $q = array_filter($d, static fn ($x) => in_array($x['prio'], ['A', 'B', 'C'], true));
            $ab = array_filter($q, static fn ($x) => in_array($x['prio'], ['A', 'B'], true));
            $sig = array_filter($offres, static fn ($o) => $o['canal_m'] === $id && $o['signee_le'] && in_array(substr((string) $o['signee_le'], 0, 7), $listeMois, true));
            $lignes[$id] = self::ratios([
                'id' => $id, 'libelle' => $libelle, 'payant' => $payant,
                'depense' => $this->depense($listeMois, [$id]),
                'demandes' => count($d), 'qualifiees' => count($q), 'ab' => count($ab),
                'signees' => count($sig), 'ca' => array_sum(array_map(static fn ($o) => (float) $o['montant_signe'], $sig)),
            ], $marge);
        }
        $total = static function (array $ls) use ($marge): array {
            $t = ['depense' => 0.0, 'demandes' => 0, 'qualifiees' => 0, 'ab' => 0, 'signees' => 0, 'ca' => 0.0];
            foreach ($ls as $l) {
                foreach ($t as $k => $_) {
                    $t[$k] += $l[$k];
                }
            }
            return self::ratios($t, $marge);
        };
        $payants = array_filter($lignes, static fn ($l) => $l['payant']);
        $tous = $total($lignes);
        foreach ($lignes as &$l) {
            $l['part'] = $tous['demandes'] > 0 ? $l['demandes'] / $tous['demandes'] : null;
        }
        unset($l);
        return ['lignes' => $lignes, 'total_payants' => $total($payants), 'total' => $tous, 'marge' => $marge,
            'inconnu' => $tous['demandes'] ? ($lignes['autres']['demandes'] / $tous['demandes']) : null];
    }

    private static function ratios(array $l, float $marge): array
    {
        $l['cpl'] = $l['depense'] > 0 && $l['demandes'] > 0 ? $l['depense'] / $l['demandes'] : null;
        $l['cac'] = $l['depense'] > 0 && $l['signees'] > 0 ? $l['depense'] / $l['signees'] : null;
        $l['roas'] = $l['depense'] > 0 ? $l['ca'] / $l['depense'] : null;
        $l['roi'] = $l['depense'] > 0 ? ($l['ca'] * $marge - $l['depense']) / $l['depense'] : null;
        return $l;
    }

    /** Alertes de la vue d'ensemble. */
    public function alertes(): array
    {
        $ouvertes = $this->app->demandes->liste(['statut' => 'ouvertes']);
        $ouvertes = array_values(array_filter($ouvertes, static fn ($d) => !(int) $d['mode_test']));
        $retards = array_filter($ouvertes, static fn ($d) => $d['en_retard']);
        $aujourdhui = $this->app->maintenant->format('Y-m-d');
        return [
            'retards_a' => array_values(array_filter($retards, static fn ($d) => $d['priorite_eff'] === 'A')),
            'retards_autres' => array_values(array_filter($retards, static fn ($d) => $d['priorite_eff'] !== 'A')),
            'offres_j35' => array_values(array_filter($ouvertes, fn ($d) => ($r = $this->app->demandes->relance($d)) !== null && $r['decision'])),
            'visites_jour' => array_values(array_filter($ouvertes, static fn ($d) => $d['visite'] && Base::local($d['visite']['prevue_le'])?->format('Y-m-d') === $aujourdhui)),
            'hors_cible' => array_values(array_filter($ouvertes, static fn ($d) => $d['statut'] === 'nouvelle' && $d['priorite_eff'] === 'hors_cible')),
        ];
    }
}
