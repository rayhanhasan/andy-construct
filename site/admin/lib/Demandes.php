<?php
declare(strict_types=1);

namespace AndyConstruct\Admin;

use AndyConstruct\Api\Base;
use AndyConstruct\Api\Canaux;
use AndyConstruct\Api\Telephone;

/**
 * Demandes : lecture, filtres, file « À traiter » et transitions de statut
 * vérifiées par le serveur (plan admin §4.5). Toute autre transition est
 * refusée ; chacune écrit une ligne d'historique (interaction) et une ligne
 * du journal d'audit.
 */
final class Demandes
{
    public const STATUTS = [
        'nouvelle' => 'Nouvelle',
        'contact_etabli' => 'Contact établi',
        'visite_planifiee' => 'Visite planifiée',
        'offre_envoyee' => 'Offre envoyée',
        'signee' => 'Signée',
        'perdue' => 'Perdue',
        'hors_cible' => 'Hors cible',
        'doublon' => 'Doublon',
        'guide' => 'Guide à envoyer',
    ];
    public const OUVERTES = ['nouvelle', 'contact_etabli', 'visite_planifiee', 'offre_envoyee'];

    /** code => [libellé, relance à 6 mois possible] */
    public const MOTIFS = [
        'prix' => ['Prix', true],
        'delai' => ['Délai', true],
        'reporte' => ['Projet reporté', true],
        'ailleurs' => ['Attribué ailleurs', true],
        'sans_reponse' => ['Sans réponse', false],
        'hors_cible' => ['Hors cible', false],
        'trop_petit' => ['Trop petit', false],
        'annule' => ['Annulé après signature', false],
        'autre' => ['Autre', true],
    ];

    /** action => [statuts de départ, statut d'arrivée, libellé] */
    public const TRANSITIONS = [
        'contact_etabli' => [['nouvelle'], 'contact_etabli', "J'ai eu la personne"],
        'pas_de_reponse' => [['nouvelle'], 'nouvelle', 'Pas de réponse'],
        'hors_cible' => [['nouvelle'], 'hors_cible', 'Hors cible'],
        'visite_planifiee' => [['contact_etabli'], 'visite_planifiee', 'Planifier la visite'],
        'visite_annulee' => [['visite_planifiee'], 'contact_etabli', 'Visite annulée'],
        'offre_envoyee' => [['contact_etabli', 'visite_planifiee'], 'offre_envoyee', "Envoyer l'offre"],
        'nouvelle_version' => [['offre_envoyee'], 'offre_envoyee', "Nouvelle version de l'offre"],
        'signee' => [['offre_envoyee'], 'signee', 'Marquer signée'],
        'perdue' => [['nouvelle', 'contact_etabli', 'visite_planifiee', 'offre_envoyee', 'signee'], 'perdue', 'Marquer perdue'],
        'rouvrir' => [['perdue', 'hors_cible'], 'nouvelle', 'Rouvrir'],
    ];

    public const TYPES_CLIENT = [
        'proprietaire' => 'Propriétaire', 'locataire' => 'Locataire', 'regie' => 'Régie', 'architecte' => 'Architecte',
        'commune' => 'Commune', 'entreprise' => 'Entreprise', 'autre' => 'Autre',
    ];
    public const TRAVAUX = [
        'placo' => 'Placo', 'peinture' => 'Peinture', 'isolation-acoustique' => 'Isolation acoustique',
        'cloisons-isothermes' => 'Cloisons isolantes', 'ne-sait-pas' => 'À préciser', 'autre' => 'Hors métiers',
    ];
    public const SURFACES = ['moins-15' => 'Moins de 15 m²', '15-50' => '15 à 50 m²', '50-200' => '50 à 200 m²', 'plus-200' => 'Plus de 200 m²', 'ne-sait-pas' => 'Ne sait pas'];
    public const DELAIS = ['moins-1-mois' => "Moins d'un mois", '1-3-mois' => '1 à 3 mois', '3-6-mois' => '3 à 6 mois', 'non-defini' => 'Pas défini'];
    public const CANAUX_SAISIE = ['telephone' => 'Téléphone', 'email' => 'E-mail reçu', 'visite' => 'Visite au bureau', 'recommandation' => 'Rencontre, recommandation'];
    public const CRITERES = ['type_client' => 'Type de client', 'service' => 'Travaux', 'surface' => 'Surface', 'zone' => 'Zone', 'delai' => 'Délai', 'source' => 'Source', 'bonus' => 'Bonus', 'malus' => 'Malus'];

    public function __construct(private App $app)
    {
    }

    // ---------------------------------------------------------------- lecture

    private const SELECT = 'SELECT d.*, c.civilite, c.prenom, c.nom AS contact_nom, c.organisation, c.email, c.telephone_e164, c.telephone_affiche,
            c.preference_contact, c.creneau, c.adresse, c.anonymise_le AS contact_anonymise_le,
            a.categorie, a.canal_marketing, a.canal_corrige, a.canal_declare, a.libelle AS source_libelle, a.emplacement, a.page, a.page_entree,
            a.referent, a.utm_source, a.utm_medium, a.utm_campaign, a.utm_content, a.utm_term, a.gclid, a.consent_ads,
            u.nom_affiche AS associe_nom
        FROM demande d
        LEFT JOIN contact c ON c.id = d.contact_id
        LEFT JOIN attribution a ON a.demande_id = d.id
        LEFT JOIN utilisateur u ON u.id = d.associe_id';

    public function parRef(string $ref): ?array
    {
        $d = $this->app->base->un(self::SELECT . ' WHERE d.ref = ?', [$ref]);
        return $d === null ? null : $this->enrichir([$d])[0];
    }

    public function parId(int $id): ?array
    {
        $d = $this->app->base->un(self::SELECT . ' WHERE d.id = ?', [$id]);
        return $d === null ? null : $this->enrichir([$d])[0];
    }

    /**
     * @param array<string, mixed> $f filtres (q, periode, statut, priorite, canal, type_client, associe, retard, tri)
     * @return list<array<string, mixed>>
     */
    public function liste(array $f, ?int $moi = null): array
    {
        $where = [];
        $p = [];
        $statut = (string) ($f['statut'] ?? 'ouvertes');
        if ($statut === 'ouvertes' || $statut === '') {
            $where[] = "d.statut IN ('" . implode("','", self::OUVERTES) . "')";
        } elseif (isset(self::STATUTS[$statut])) {
            $where[] = 'd.statut = ?';
            $p[] = $statut;
        }
        if ($statut !== 'guide') {
            $where[] = "d.statut <> 'guide'";
        }
        $periode = (string) ($f['periode'] ?? '');
        $jours = ['7j' => 7, '30j' => 30, '3m' => 92, '12m' => 366][$periode] ?? null;
        if ($jours !== null) {
            $where[] = 'd.recue_le >= ?';
            $p[] = Base::utc($this->app->maintenant->modify("-$jours days"));
        } elseif ($periode === 'mois') {
            $where[] = 'd.recue_le >= ?';
            $p[] = Base::utc($this->app->maintenant->modify('first day of this month')->setTime(0, 0));
        }
        $prio = (string) ($f['priorite'] ?? '');
        if (in_array($prio, ['A', 'B', 'C', 'hors_cible'], true)) {
            $where[] = 'COALESCE(d.priorite_corrigee, d.priorite) = ?';
            $p[] = $prio;
        }
        $canal = (string) ($f['canal'] ?? '');
        if (isset(Canaux::LISTE[$canal])) {
            $where[] = 'COALESCE(a.canal_corrige, a.canal_marketing) = ?';
            $p[] = $canal;
        }
        $type = (string) ($f['type_client'] ?? '');
        if (isset(self::TYPES_CLIENT[$type])) {
            $where[] = 'd.type_client = ?';
            $p[] = $type;
        }
        $associe = (string) ($f['associe'] ?? '');
        if ($associe === 'moi' && $moi !== null) {
            $where[] = 'd.associe_id = ?';
            $p[] = $moi;
        } elseif (ctype_digit($associe)) {
            $where[] = 'd.associe_id = ?';
            $p[] = (int) $associe;
        }
        if (!empty($f['retard'])) {
            $where[] = "d.statut = 'nouvelle' AND d.echeance_le < ?";
            $p[] = Base::utc($this->app->maintenant);
        }
        $q = trim((string) ($f['q'] ?? ''));
        if (mb_strlen($q) >= 2) {
            $cond = ['d.ref LIKE ?', 'c.nom LIKE ?', 'c.prenom LIKE ?', 'c.organisation LIKE ?', 'c.email_normalise LIKE ?', 'd.commune LIKE ?', 'd.npa LIKE ?'];
            $motif = '%' . str_replace(['%', '_'], '', mb_strtolower($q)) . '%';
            $vals = array_fill(0, count($cond), $motif);
            $tel = Telephone::normaliser($q);
            $chiffres = preg_replace('/\D/', '', $q) ?? '';
            if ($tel !== null) {
                $cond[] = 'c.telephone_e164 = ?';
                $vals[] = $tel['e164'];
            } elseif (strlen($chiffres) >= 4) {
                $cond[] = 'c.telephone_e164 LIKE ?';
                $vals[] = '%' . ltrim($chiffres, '0') . '%';
            }
            $where[] = '(' . implode(' OR ', $cond) . ')';
            $p = array_merge($p, $vals);
        }
        $sql = self::SELECT . ($where ? ' WHERE ' . implode(' AND ', $where) : '');
        $ordre = match ((string) ($f['tri'] ?? 'echeance')) {
            'recue' => ' ORDER BY d.recue_le DESC',
            'score' => ' ORDER BY d.score DESC, d.recue_le DESC',
            default => " ORDER BY CASE WHEN d.statut = 'nouvelle' THEN 0 ELSE 1 END, d.echeance_le, d.recue_le DESC",
        };
        $lignes = $this->enrichir($this->app->base->tous($sql . $ordre . ' LIMIT 1000', $p));
        if (($f['tri'] ?? '') === 'montant') {
            usort($lignes, static fn ($a, $b) => ($b['montant'] ?? 0) <=> ($a['montant'] ?? 0));
        }
        return $lignes;
    }

    /**
     * Ajoute les champs calculés : nom, priorité et canal effectifs, offre en cours,
     * montant, visite à venir, échéance locale, retard.
     *
     * @param list<array<string, mixed>> $lignes
     * @return list<array<string, mixed>>
     */
    public function enrichir(array $lignes): array
    {
        if ($lignes === []) {
            return [];
        }
        $ids = array_map(static fn ($d) => (int) $d['id'], $lignes);
        $marques = implode(',', array_fill(0, count($ids), '?'));
        $offres = [];
        foreach ($this->app->base->tous("SELECT * FROM offre WHERE demande_id IN ($marques) AND statut <> 'remplacee' ORDER BY version", $ids) as $o) {
            $offres[(int) $o['demande_id']] = $o;
        }
        $visites = [];
        foreach ($this->app->base->tous("SELECT * FROM visite WHERE demande_id IN ($marques) AND statut = 'planifiee' ORDER BY prevue_le", $ids) as $v) {
            $visites[(int) $v['demande_id']] ??= $v;
        }
        $maintenant = $this->app->maintenant;
        foreach ($lignes as &$d) {
            $d['id'] = (int) $d['id'];
            $d['nom_complet'] = self::nomComplet($d);
            $d['priorite_eff'] = $d['priorite_corrigee'] ?: $d['priorite'];
            $d['canal_eff'] = $d['canal_corrige'] ?: ($d['canal_marketing'] ?: 'autres');
            $d['travaux_liste'] = json_decode((string) ($d['travaux'] ?? '[]'), true) ?: [];
            $d['offre'] = $offres[$d['id']] ?? null;
            $d['visite'] = $visites[$d['id']] ?? null;
            $d['montant'] = $d['offre'] ? (float) ($d['offre']['montant_signe_ht'] ?? $d['offre']['montant_ht']) : null;
            $d['echeance'] = Base::local($d['echeance_le']);
            $d['recue'] = Base::local($d['recue_le']);
            $d['en_retard'] = $d['statut'] === 'nouvelle' && $d['echeance'] !== null && $d['echeance'] < $maintenant;
            $d['tentatives_appel'] = (int) $d['tentatives_appel'];
            $d['score'] = $d['score'] === null ? null : (int) $d['score'];
        }
        unset($d);
        return $lignes;
    }

    public static function nomComplet(array $d): string
    {
        if (!empty($d['anonymise_le']) || !empty($d['contact_anonymise_le'])) {
            return 'Personne effacée';
        }
        $nom = trim(((string) ($d['prenom'] ?? '')) . ' ' . ((string) ($d['contact_nom'] ?? '')));
        return $nom !== '' ? $nom : 'Sans nom';
    }

    public static function libelleTravaux(array $d): string
    {
        $l = array_map(static fn ($t) => self::TRAVAUX[$t] ?? $t, $d['travaux_liste'] ?? []);
        return $l ? implode(', ', $l) : '—';
    }

    /** Valeur lisible d'un critère du score (le détail garde les codes de la grille). */
    public static function libelleCritere(string $critere, string $valeur): string
    {
        return match ($critere) {
            'type_client' => self::TYPES_CLIENT[$valeur] ?? $valeur,
            'service' => $valeur === 'plusieurs' ? 'Plusieurs prestations' : (self::TRAVAUX[$valeur] ?? $valeur),
            'surface' => self::SURFACES[$valeur] ?? $valeur,
            'delai' => self::DELAIS[$valeur] ?? $valeur,
            'zone' => is_numeric($valeur) ? 'Zone ' . $valeur : $valeur,
            default => $valeur,
        };
    }

    /** Relances d'une offre ouverte : jours écoulés, étape (J+3, J+10, J+21), prochaine action. */
    public function relance(array $d): ?array
    {
        if ($d['statut'] !== 'offre_envoyee' || $d['offre'] === null) {
            return null;
        }
        $envoi = new \DateTimeImmutable((string) $d['offre']['envoyee_le'], new \DateTimeZone('Europe/Zurich'));
        $jours = (int) $envoi->diff($this->app->maintenant->setTime(0, 0))->format('%r%a');
        $etape = $d['ne_pas_relancer'] ? (int) $d['offre']['relance_etape'] : count(array_filter([3, 10, 21], static fn ($j) => $jours >= $j));
        $decision = $jours >= 35;
        $appel = !$decision && $jours >= 10;
        if ($decision) {
            $texte = 'J+' . $jours . ' sans suite : clore ou garder ?';
        } elseif ($appel) {
            $texte = 'Appeler le client (J+10)';
        } else {
            $prochaine = current(array_filter([3, 10, 21], static fn ($j) => $jours < $j));
            $texte = $d['ne_pas_relancer'] ? 'Relances arrêtées' : 'Relance J+' . $prochaine . ' le ' . Format::dateC($envoi->modify("+$prochaine days"));
        }
        return ['jours' => $jours, 'etape' => $etape, 'decision' => $decision, 'appel' => $appel, 'texte' => $texte];
    }

    /** Sections de l'écran « À traiter ». */
    public function aTraiter(?int $moi): array
    {
        $ouvertes = $this->liste(['statut' => 'ouvertes', 'tri' => 'echeance']);
        $mien = static fn (array $d): bool => $moi === null || (int) $d['associe_id'] === $moi;
        $demain = $this->app->maintenant->modify('+1 day')->format('Y-m-d');
        $aujourdhui = $this->app->maintenant->format('Y-m-d');
        $s = ['retards' => [], 'rappeler' => [], 'tentatives' => [], 'visites' => [], 'offres' => [], 'hors_cible' => []];
        foreach ($ouvertes as $d) {
            if ($d['en_retard']) {
                $s['retards'][] = $d; // tous les retards, quel que soit l'associé (escalade)
                continue;
            }
            if (!$mien($d)) {
                continue;
            }
            if ($d['statut'] === 'nouvelle') {
                if ($d['priorite_eff'] === 'hors_cible') {
                    $s['hors_cible'][] = $d;
                } elseif ($d['tentatives_appel'] > 0) {
                    $s['tentatives'][] = $d;
                } else {
                    $s['rappeler'][] = $d;
                }
            } elseif ($d['visite'] !== null) {
                $jour = Base::local($d['visite']['prevue_le'])?->format('Y-m-d');
                if ($jour === $aujourdhui || $jour === $demain) {
                    $s['visites'][] = $d;
                }
            } elseif (($r = $this->relance($d)) !== null && ($r['decision'] || ($r['appel'] && !$this->appeleDepuis($d['id'], $d['offre']['envoyee_le'], 10)))) {
                $d['relance'] = $r;
                $s['offres'][] = $d;
            }
        }
        usort($s['visites'], static fn ($a, $b) => strcmp($a['visite']['prevue_le'], $b['visite']['prevue_le']));
        return $s;
    }

    private function appeleDepuis(int $id, string $envoi, int $jours): bool
    {
        $depuis = Base::utc((new \DateTimeImmutable($envoi, new \DateTimeZone('Europe/Zurich')))->modify("+$jours days"));
        return (int) $this->app->base->valeur("SELECT COUNT(*) FROM interaction WHERE demande_id = ? AND type = 'appel_sortant' AND cree_le >= ?", [$id, $depuis]) > 0;
    }

    /** Actions de changement de statut possibles depuis l'état actuel (colonnes, fiche). */
    public function actionsPossibles(array $d): array
    {
        $r = [];
        foreach (self::TRANSITIONS as $action => [$de, , $libelle]) {
            if (in_array($d['statut'], $de, true) && $this->conditionsRemplies($d, $action, null) === null) {
                $r[$action] = $action === 'pas_de_reponse' ? 'Pas de réponse (tentative ' . ($d['tentatives_appel'] + 1) . ')' : $libelle;
            }
        }
        return $r;
    }

    /** Message de refus, ou null si l'action est permise (sans tenir compte des paramètres). */
    private function conditionsRemplies(array $d, string $action, ?array $params): ?string
    {
        $statut = $d['statut'];
        return match (true) {
            $action === 'pas_de_reponse' && $d['tentatives_appel'] >= 3 => 'Trois tentatives sans réponse : marquez la demande perdue (motif « sans réponse »).',
            $action === 'perdue' && $statut === 'nouvelle' && $d['tentatives_appel'] < 3 => "Une nouvelle demande ne se perd qu'après trois appels sans réponse. Classez-la hors cible si elle ne nous concerne pas.",
            $action === 'perdue' && $statut === 'nouvelle' && $params !== null && ($params['motif'] ?? '') !== 'sans_reponse' => 'Après trois appels sans réponse, le motif est « sans réponse ».',
            $action === 'perdue' && $statut === 'signee' && $params !== null && ($params['motif'] ?? '') !== 'annule' => 'Une demande signée ne peut être perdue que pour le motif « annulé après signature ».',
            $action === 'rouvrir' && Base::local((string) $d['statut_change_le']) < $this->app->maintenant->modify('-90 days') => 'Plus de 90 jours : enregistrez plutôt une nouvelle demande.',
            default => null,
        };
    }

    /**
     * Change le statut d'une demande. Lève \DomainException (message pour
     * l'utilisateur) si la transition ou ses paramètres sont refusés.
     *
     * @param array<string, mixed> $params montant, date, heure, adresse, motif, numero, version, recontact
     */
    public function agir(int $id, string $action, array $params = [], ?int $auteur = null, string $origine = 'admin', ?\DateTimeImmutable $quand = null): array
    {
        $quand ??= $this->app->maintenant;
        $quandUtc = Base::utc($quand);
        if (!isset(self::TRANSITIONS[$action])) {
            throw new \DomainException('Action inconnue.');
        }
        return $this->app->base->transaction(function (Base $b) use ($id, $action, $params, $auteur, $origine, $quand, $quandUtc): array {
            $d = $this->parId($id);
            if ($d === null) {
                throw new \DomainException('Demande introuvable.');
            }
            if (!empty($d['anonymise_le'])) {
                throw new \DomainException('Demande effacée : plus aucune action possible.');
            }
            if (isset($params['version']) && (string) $params['version'] !== '' && (int) $params['version'] !== (int) $d['version']) {
                throw new \DomainException("Cette demande a été modifiée par quelqu'un d'autre entre-temps. Rechargez la page, puis recommencez.");
            }
            [$de, $vers] = self::TRANSITIONS[$action];
            if (!in_array($d['statut'], $de, true)) {
                throw new \DomainException('Transition refusée : « ' . self::TRANSITIONS[$action][2] . ' » n\'est pas possible depuis le statut « ' . (self::STATUTS[$d['statut']] ?? $d['statut']) . ' ».');
            }
            if (($refus = $this->conditionsRemplies($d, $action, $params)) !== null) {
                throw new \DomainException($refus);
            }
            $maj = ['statut' => $vers, 'modifie_le' => Base::maintenant(), 'version' => (int) $d['version'] + 1];
            if ($vers !== $d['statut']) {
                $maj['statut_change_le'] = $quandUtc;
            }
            $texte = '';
            $type = 'systeme';
            $resultat = null;
            switch ($action) {
                case 'contact_etabli':
                    $type = 'appel_sortant';
                    $resultat = 'abouti';
                    $texte = "J'ai eu la personne";
                    $maj['premier_contact_le'] = $d['premier_contact_le'] ?: $quandUtc;
                    $maj['premier_appel_le'] = $d['premier_appel_le'] ?: $quandUtc;
                    break;
                case 'pas_de_reponse':
                    $type = 'appel_sortant';
                    $resultat = 'pas_de_reponse';
                    $n = $d['tentatives_appel'] + 1;
                    $texte = "Appel sans réponse (tentative $n)";
                    $maj['tentatives_appel'] = $n;
                    $maj['premier_appel_le'] = $d['premier_appel_le'] ?: $quandUtc;
                    $maj['echeance_le'] = Base::utc($this->app->heures->jourOuvrableSuivant($quand, 10));
                    break;
                case 'hors_cible':
                    $texte = 'Classée hors cible';
                    break;
                case 'visite_planifiee':
                    $prevue = self::lireDateHeure($params['date'] ?? '', $params['heure'] ?? '');
                    if ($prevue === null) {
                        throw new \DomainException('Indiquez la date et l\'heure de la visite.');
                    }
                    $adresse = mb_substr(trim((string) ($params['adresse'] ?? '')), 0, 300);
                    $b->inserer('visite', ['demande_id' => $id, 'prevue_le' => Base::utc($prevue), 'adresse' => $adresse ?: null,
                        'associe_id' => $d['associe_id'], 'statut' => 'planifiee', 'cree_le' => $quandUtc]);
                    $type = 'visite';
                    $texte = 'Visite planifiée le ' . Format::dateH($prevue);
                    break;
                case 'visite_annulee':
                    $b->executer("UPDATE visite SET statut = 'annulee' WHERE demande_id = ? AND statut = 'planifiee'", [$id]);
                    $type = 'visite';
                    $texte = 'Visite annulée';
                    break;
                case 'offre_envoyee':
                case 'nouvelle_version':
                    $montant = Format::lireMontant($params['montant'] ?? null);
                    if ($montant === null || $montant <= 0) {
                        throw new \DomainException("Indiquez le montant de l'offre, hors TVA (par exemple 12'500).");
                    }
                    $date = self::lireDate($params['date'] ?? '') ?? $quand;
                    $version = 1 + (int) $b->valeur('SELECT COALESCE(MAX(version), 0) FROM offre WHERE demande_id = ?', [$id]);
                    if ($action === 'nouvelle_version') {
                        $b->executer("UPDATE offre SET statut = 'remplacee' WHERE demande_id = ? AND statut = 'envoyee'", [$id]);
                    }
                    $numero = mb_substr(trim((string) ($params['numero'] ?? '')), 0, 30) ?: 'O-' . substr((string) $d['ref'], 3) . '-' . $version;
                    $b->inserer('offre', ['demande_id' => $id, 'numero' => $numero, 'version' => $version, 'montant_ht' => $montant,
                        'envoyee_le' => $date->format('Y-m-d'), 'statut' => 'envoyee', 'relance_etape' => 0, 'cree_le' => $quandUtc]);
                    $b->executer("UPDATE visite SET statut = 'faite' WHERE demande_id = ? AND statut = 'planifiee' AND prevue_le <= ?", [$id, $quandUtc]);
                    $texte = ($version > 1 ? "Nouvelle version de l'offre" : 'Offre envoyée') . " n° $numero : " . Format::chf($montant) . ' HT, le ' . Format::dateA($date);
                    break;
                case 'signee':
                    $montant = Format::lireMontant($params['montant'] ?? null) ?? ($d['offre'] ? (float) $d['offre']['montant_ht'] : null);
                    $date = self::lireDate($params['date'] ?? '');
                    if ($montant === null || $montant <= 0 || $date === null) {
                        throw new \DomainException('Indiquez la date de signature et le montant signé, hors TVA.');
                    }
                    $b->executer("UPDATE offre SET statut = 'signee', signee_le = ?, montant_signe_ht = ? WHERE demande_id = ? AND statut = 'envoyee'", [$date->format('Y-m-d'), $montant, $id]);
                    $texte = 'Offre signée le ' . Format::dateA($date) . ' : ' . Format::chf($montant) . ' HT';
                    break;
                case 'perdue':
                    $motif = (string) ($params['motif'] ?? '');
                    if (!isset(self::MOTIFS[$motif])) {
                        throw new \DomainException('Choisissez le motif de la perte (obligatoire).');
                    }
                    $maj['motif_perte'] = $motif;
                    $maj['perdue_le'] = $quandUtc;
                    $maj['recontact_autorise'] = self::MOTIFS[$motif][1] && !empty($params['recontact']) ? 1 : 0;
                    $b->executer("UPDATE offre SET statut = 'perdue' WHERE demande_id = ? AND statut IN ('envoyee', 'signee')", [$id]);
                    $b->executer("UPDATE visite SET statut = 'annulee' WHERE demande_id = ? AND statut = 'planifiee'", [$id]);
                    $texte = 'Demande perdue : ' . mb_strtolower(self::MOTIFS[$motif][0]) . ($maj['recontact_autorise'] ? ' (relance à 6 mois)' : '');
                    break;
                case 'rouvrir':
                    $maj['motif_perte'] = null;
                    $maj['perdue_le'] = null;
                    $maj['echeance_le'] = Base::utc($this->app->heures->echeance((string) ($d['priorite_eff'] === 'hors_cible' ? 'hors-cible' : $d['priorite_eff']), $quand));
                    $texte = 'Demande rouverte';
                    break;
            }
            $b->maj('demande', $maj, 'id = ?', [$id]);
            $b->inserer('interaction', [
                'demande_id' => $id, 'type' => $type, 'resultat' => $resultat,
                'contenu' => $texte . ($vers !== $d['statut'] ? ' · ' . self::STATUTS[$d['statut']] . ' → ' . self::STATUTS[$vers] : ''),
                'auteur_id' => $auteur, 'origine' => $origine, 'cree_le' => $quandUtc,
            ]);
            $this->app->audit('changement_statut', 'demande', (string) $d['ref'], ['action' => $action, 'de' => $d['statut'], 'vers' => $vers]);
            return ['de' => $d['statut'], 'vers' => $vers, 'texte' => $texte];
        });
    }

    public function ajouterNote(int $id, string $texte, int $auteur): void
    {
        $texte = trim($texte);
        if ($texte === '' || mb_strlen($texte) > 5000) {
            throw new \DomainException('La note est vide ou trop longue (5000 caractères au plus).');
        }
        $this->app->base->inserer('interaction', ['demande_id' => $id, 'type' => 'note', 'contenu' => $texte, 'auteur_id' => $auteur, 'origine' => 'admin', 'cree_le' => Base::maintenant()]);
        $this->app->audit('note_ajoutee', 'demande', (string) $this->ref($id));
    }

    public function corrigerPriorite(int $id, string $priorite, string $motif, int $auteur): void
    {
        if (!in_array($priorite, ['A', 'B', 'C', 'hors_cible'], true) || trim($motif) === '') {
            throw new \DomainException('Choisissez la priorité et indiquez le motif de la correction.');
        }
        $this->app->base->maj('demande', ['priorite_corrigee' => $priorite, 'modifie_le' => Base::maintenant()], 'id = ?', [$id]);
        $this->app->base->inserer('interaction', ['demande_id' => $id, 'type' => 'note', 'contenu' => 'Priorité corrigée en ' . ($priorite === 'hors_cible' ? 'hors cible' : $priorite) . ' : ' . mb_substr(trim($motif), 0, 500), 'auteur_id' => $auteur, 'origine' => 'admin', 'cree_le' => Base::maintenant()]);
        $this->app->audit('priorite_corrigee', 'demande', (string) $this->ref($id), ['priorite' => $priorite]);
    }

    public function corrigerCanal(int $id, string $canal, int $auteur): void
    {
        if (!isset(Canaux::LISTE[$canal])) {
            throw new \DomainException('Canal inconnu.');
        }
        $this->app->base->maj('attribution', ['canal_corrige' => $canal], 'demande_id = ?', [$id]);
        $this->app->base->inserer('interaction', ['demande_id' => $id, 'type' => 'note', 'contenu' => 'Canal corrigé : ' . Canaux::libelle($canal), 'auteur_id' => $auteur, 'origine' => 'admin', 'cree_le' => Base::maintenant()]);
        $this->app->audit('canal_corrige', 'demande', (string) $this->ref($id), ['canal' => $canal]);
    }

    public function reattribuer(int $id, int $associe, int $auteur): void
    {
        $u = $this->app->base->un("SELECT id, nom_affiche FROM utilisateur WHERE id = ? AND actif = 1 AND role IN ('associe', 'secretariat')", [$associe]);
        if ($u === null) {
            throw new \DomainException('Utilisateur inconnu ou inactif.');
        }
        $this->app->base->maj('demande', ['associe_id' => $associe, 'modifie_le' => Base::maintenant()], 'id = ?', [$id]);
        $this->app->base->inserer('interaction', ['demande_id' => $id, 'type' => 'systeme', 'contenu' => 'Attribuée à ' . $u['nom_affiche'], 'auteur_id' => $auteur, 'origine' => 'admin', 'cree_le' => Base::maintenant()]);
        $this->app->audit('reattribution', 'demande', (string) $this->ref($id), ['associe' => $associe]);
    }

    public function historique(int $id): array
    {
        return $this->app->base->tous('SELECT i.*, u.nom_affiche FROM interaction i LEFT JOIN utilisateur u ON u.id = i.auteur_id WHERE i.demande_id = ? ORDER BY i.cree_le DESC, i.id DESC', [$id]);
    }

    public function autresDemandes(array $d): array
    {
        if (empty($d['contact_id'])) {
            return [];
        }
        return $this->app->base->tous('SELECT ref, statut, recue_le FROM demande WHERE contact_id = ? AND id <> ? ORDER BY recue_le DESC', [$d['contact_id'], $d['id']]);
    }

    private function ref(int $id): string
    {
        return (string) $this->app->base->valeur('SELECT ref FROM demande WHERE id = ?', [$id]);
    }

    public static function lireDate(mixed $v): ?\DateTimeImmutable
    {
        if (!is_string($v) || !preg_match('/^\d{4}-\d{2}-\d{2}$/', $v)) {
            return null;
        }
        $t = \DateTimeImmutable::createFromFormat('!Y-m-d', $v, new \DateTimeZone('Europe/Zurich'));
        return $t && $t->format('Y-m-d') === $v ? $t->setTime(12, 0) : null;
    }

    public static function lireDateHeure(mixed $date, mixed $heure): ?\DateTimeImmutable
    {
        $j = self::lireDate($date);
        if ($j === null || !is_string($heure) || !preg_match('/^([01]\d|2[0-3]):([0-5]\d)$/', $heure, $m)) {
            return null;
        }
        return $j->setTime((int) $m[1], (int) $m[2]);
    }
}
