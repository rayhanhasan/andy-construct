<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Enregistrement d'une demande en base (plan admin §2.6, classe « Depot »).
 *
 * Appelé par Traitement après l'e-mail interne et le webhook : si la base est
 * indisponible, la demande est écrite dans stockage/file-attente-base/ et
 * rejouée par cron.php (ou après la réponse au visiteur). Le flux actuel
 * (e-mail, accusé, n8n) ne dépend jamais de la base. La référence étant
 * unique, un rejeu ne crée jamais de doublon.
 */
final class Depot
{
    private ?Base $base = null;

    public function __construct(private Config $config, private Stockage $stockage, private Journal $journal)
    {
    }

    public function actif(): bool
    {
        return (bool) $this->config->get('base.actif', true);
    }

    /** Base partagée (connexion ouverte au premier usage). */
    public function base(): Base
    {
        return $this->base ??= Base::depuisConfig($this->config);
    }

    /**
     * Enregistrement sérialisable (JSON) d'une demande assemblée par Traitement.
     *
     * @param array<string, mixed> $demande
     * @param array<string, mixed> $bilan
     * @param array{auteur_id?: ?int, canal?: string, mode_test?: bool}|null $saisie saisie depuis l'admin
     * @return array<string, mixed>
     */
    public static function preparer(array $demande, array $bilan, ?array $saisie = null, bool $modeTest = false): array
    {
        $d = $demande['d'];
        $s = $demande['scoring'];
        $tel = $d['telephone'];
        return [
            'v' => 1,
            'ref' => $demande['ref'],
            'recue_le' => Base::utc($demande['recu_le']),
            'formulaire' => $demande['formulaire'],
            'canal' => $saisie['canal'] ?? $demande['canal'],
            'cree_par' => $saisie['auteur_id'] ?? null,
            'mode_test' => (bool) ($saisie['mode_test'] ?? $modeTest),
            'role_associe' => $demande['associe']['role'] ?? 'terrain',
            'contact' => [
                'civilite' => $d['civilite'],
                'prenom' => $d['prenom'],
                'nom' => $d['nom'],
                'email' => $d['email'],
                'telephone_e164' => $tel['e164'] ?? '',
                'telephone_affiche' => $tel['affiche'] ?? '',
                'telephone_mobile' => (bool) ($tel['mobile'] ?? false),
                'adresse' => $d['adresse'],
                'npa' => $d['formulaire'] === 'envoi_postal_guide' ? $d['npa'] : '',
                'localite' => $d['localite'],
                'preference_contact' => $d['preference_contact'],
                'creneau' => $d['creneau'],
            ],
            'projet' => [
                'type_client' => $d['type_client'] ?: ($d['profil'] ?? ''),
                'travaux' => $d['travaux'],
                'service' => $d['service'],
                'surface' => $d['surface'],
                'delai' => $d['delai'],
                'commune' => $d['commune'] !== '' ? $d['commune'] : (string) ($demande['localite']['commune'] ?? ''),
                'npa' => $d['npa'] !== '' ? $d['npa'] : (string) ($demande['localite']['npa'] ?? ''),
                'canton' => (string) ($demande['localite']['canton'] ?? ''),
                'zone' => (string) ($demande['localite']['zone'] ?? 'inconnue'),
                'message' => $d['message'],
                'connu_par' => $d['connu_par'],
                'recommande_par' => $d['recommande_par'],
                'guide' => $d['guide'] ?? '',
            ],
            'scoring' => $s === null ? null : [
                'score' => $s['score'],
                'priorite' => $s['priorite'] === 'hors-cible' ? 'hors_cible' : $s['priorite'],
                'detail' => $s['detail'],
                'regles' => array_merge($s['regles'], $s['hors_cible']),
            ],
            'echeance_le' => $demande['echeance'] instanceof \DateTimeInterface ? Base::utc($demande['echeance']) : null,
            'source' => [
                'categorie' => $demande['source']['categorie'],
                'libelle' => $demande['source']['libelle'],
                'emplacement' => $d['source'],
                'page' => $d['page'],
                'page_entree' => $d['page_entree'],
                'referent' => $d['referent'],
                'utm' => $d['utm'],
                'gclid' => $d['gclid'],
                'consent_ads' => $d['consent_ads'],
            ],
            'fichiers' => array_map(static fn ($f) => [
                'identifiant' => $f['id'], 'nom' => $f['nom'], 'type' => $f['type'], 'taille' => $f['taille'], 'sha256' => $f['sha256'],
            ], $demande['fichiers']),
            'accuse_reception' => (string) ($bilan['accuse'] ?? 'non'),
        ];
    }

    /**
     * @param array<string, mixed> $e enregistrement de preparer()
     * @return string enregistree | deja | en_file | desactive
     */
    public function enregistrer(array $e): string
    {
        if (!$this->actif()) {
            return 'desactive';
        }
        try {
            return $this->inserer($e) ? 'enregistree' : 'deja';
        } catch (\Throwable $ex) {
            $this->base = null;
            $this->journal->erreur('base_indisponible', ['ref' => $e['ref'] ?? '', 'erreur' => Journal::nettoyerMessage($ex->getMessage())]);
            return $this->mettreEnFile($e) ? 'en_file' : 'perdue';
        }
    }

    private function mettreEnFile(array $e): bool
    {
        try {
            $fichier = $this->stockage->dossier('file-attente-base') . '/' . preg_replace('/[^A-Za-z0-9-]/', '', (string) $e['ref']) . '.json';
            $this->stockage->ecrireAtomique($fichier, (string) json_encode($e, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR));
            @chmod($fichier, 0600);
            return true;
        } catch (\Throwable) {
            $this->journal->erreur('file_attente_base_ecriture', ['ref' => $e['ref'] ?? '']);
            return false;
        }
    }

    /**
     * Rejoue les demandes en attente de la base.
     *
     * @return array{inserees: int, deja: int, restantes: int}
     */
    public function traiterFile(int $max = 50): array
    {
        $bilan = ['inserees' => 0, 'deja' => 0, 'restantes' => 0];
        if (!$this->actif()) {
            return $bilan;
        }
        $fichiers = glob($this->stockage->dossier('file-attente-base') . '/*.json') ?: [];
        if ($fichiers === []) {
            return $bilan;
        }
        sort($fichiers);
        $this->stockage->sousVerrou('file-attente-base', function () use ($fichiers, $max, &$bilan): bool {
            foreach ($fichiers as $i => $fichier) {
                if ($i >= $max || !is_file($fichier)) {
                    $bilan['restantes'] += $i >= $max ? 1 : 0;
                    continue;
                }
                $e = json_decode((string) file_get_contents($fichier), true);
                if (!is_array($e) || !isset($e['ref'])) {
                    @unlink($fichier);
                    continue;
                }
                try {
                    $this->inserer($e) ? $bilan['inserees']++ : $bilan['deja']++;
                    @unlink($fichier);
                    $this->journal->info('base_rejouee', ['ref' => $e['ref']]);
                } catch (\Throwable $ex) {
                    $this->base = null;
                    $bilan['restantes'] += count($fichiers) - $i;
                    $this->journal->alerte('base_toujours_indisponible', ['erreur' => Journal::nettoyerMessage($ex->getMessage())]);
                    break;
                }
            }
            return true;
        }, false);
        return $bilan;
    }

    public function tailleFile(): int
    {
        return count(glob($this->stockage->dossier('file-attente-base') . '/*.json') ?: []);
    }

    /** @return bool false si la référence existe déjà (rejeu) */
    private function inserer(array $e): bool
    {
        $base = $this->base();
        return (bool) $base->transaction(function (Base $b) use ($e): bool {
            if ($b->valeur('SELECT id FROM demande WHERE ref = ?', [$e['ref']]) !== null) {
                return false;
            }
            $maintenant = Base::maintenant();
            $c = $e['contact'];
            $p = $e['projet'];
            $s = $e['scoring'];
            $emailNorm = $c['email'] !== '' ? strtolower((string) $c['email']) : null;
            $tel = $c['telephone_e164'] !== '' ? (string) $c['telephone_e164'] : null;

            // Contact : même téléphone ou même e-mail (non effacé) → même personne.
            $contact = null;
            if ($tel !== null || $emailNorm !== null) {
                $contact = $b->un('SELECT * FROM contact WHERE anonymise_le IS NULL AND ((telephone_e164 IS NOT NULL AND telephone_e164 = ?) OR (email_normalise IS NOT NULL AND email_normalise = ?)) ORDER BY id DESC LIMIT 1', [$tel ?? '-', $emailNorm ?? '-']);
            }
            $valeursContact = array_filter([
                'civilite' => $c['civilite'] ?: null,
                'prenom' => $c['prenom'] ?: null,
                'nom' => $c['nom'] ?: null,
                'email' => $c['email'] ?: null,
                'email_normalise' => $emailNorm,
                'telephone_e164' => $tel,
                'telephone_affiche' => $c['telephone_affiche'] ?: null,
                'adresse' => $c['adresse'] ?: null,
                'npa' => $c['npa'] ?: null,
                'localite' => $c['localite'] ?: null,
                'preference_contact' => $c['preference_contact'] ?: null,
                'creneau' => $c['creneau'] ?: null,
            ], static fn ($v) => $v !== null);
            if ($contact === null) {
                $contactId = $b->inserer('contact', $valeursContact + [
                    'telephone_mobile' => $c['telephone_mobile'] ? 1 : 0,
                    'cree_le' => $maintenant,
                    'modifie_le' => $maintenant,
                ]);
            } else {
                $contactId = (int) $contact['id'];
                if (isset($valeursContact['nom'])) {
                    $valeursContact['prenom'] = $c['prenom'] ?: null; // le nom saisi remplace le nom complet précédent
                }
                $b->maj('contact', $valeursContact + ['modifie_le' => $maintenant], 'id = ?', [$contactId]);
            }

            $associe = $e['cree_par'] ?? null;
            if ($associe === null) {
                $associe = $b->valeur("SELECT id FROM utilisateur WHERE role = 'associe' AND actif = 1 AND role_metier = ? ORDER BY id LIMIT 1", [$e['role_associe']])
                    ?? $b->valeur("SELECT id FROM utilisateur WHERE role = 'associe' AND actif = 1 ORDER BY id LIMIT 1");
            }

            $priorite = $s['priorite'] ?? null;
            $demandeId = $b->inserer('demande', [
                'ref' => $e['ref'],
                'contact_id' => $contactId,
                'recue_le' => $e['recue_le'],
                'canal' => $e['canal'],
                'formulaire' => $e['formulaire'],
                'type_client' => $p['type_client'] ?: null,
                'travaux' => json_encode(array_values($p['travaux']), JSON_UNESCAPED_UNICODE),
                'service' => $p['service'] ?: null,
                'surface' => $p['surface'] ?: null,
                'delai' => $p['delai'] ?: null,
                'commune' => $p['commune'] ?: null,
                'npa' => $p['npa'] ?: null,
                'canton' => $p['canton'] ?: null,
                'zone' => $p['zone'] ?: null,
                'message' => $p['message'] ?: null,
                'connu_par' => $p['connu_par'] ?: null,
                'recommande_par' => $p['recommande_par'] ?: null,
                'guide' => $p['guide'] ?: null,
                'score' => $s['score'] ?? null,
                'priorite' => $priorite,
                'score_detail' => $s === null ? null : json_encode($s['detail'], JSON_UNESCAPED_UNICODE),
                'score_regles' => $s === null ? null : json_encode($s['regles'], JSON_UNESCAPED_UNICODE),
                'grille_version' => $s === null ? null : $this->versionGrille(),
                'echeance_le' => $e['echeance_le'],
                'echeance_initiale_le' => $e['echeance_le'],
                'associe_id' => $associe !== null ? (int) $associe : null,
                // Une demande de guide imprimé n'attend pas de rappel : elle n'est pas « nouvelle ».
                'statut' => $e['formulaire'] === 'envoi_postal_guide' ? 'guide' : 'nouvelle',
                'statut_change_le' => $e['recue_le'],
                'premier_contact_le' => null,
                'accuse_reception' => $e['accuse_reception'],
                'mode_test' => $e['mode_test'] ? 1 : 0,
                'cree_par' => $e['cree_par'] ?? null,
                'cree_le' => $maintenant,
                'modifie_le' => $maintenant,
            ]);

            $src = $e['source'];
            [$canal, $declare] = Canaux::deduire((string) $src['categorie'], (string) $p['connu_par'], $this->connuPar());
            $b->inserer('attribution', [
                'demande_id' => $demandeId,
                'categorie' => $src['categorie'],
                'canal_marketing' => $canal,
                'canal_declare' => $declare ? 1 : 0,
                'libelle' => mb_substr((string) $src['libelle'], 0, 150),
                'emplacement' => $src['emplacement'] ?: null,
                'page' => $src['page'] ?: null,
                'page_entree' => $src['page_entree'] ?: null,
                'referent' => $src['referent'] ?: null,
                'utm_source' => $src['utm']['utm_source'] ?? null ?: null,
                'utm_medium' => $src['utm']['utm_medium'] ?? null ?: null,
                'utm_campaign' => $src['utm']['utm_campaign'] ?? null ?: null,
                'utm_content' => $src['utm']['utm_content'] ?? null ?: null,
                'utm_term' => $src['utm']['utm_term'] ?? null ?: null,
                'gclid' => $src['gclid'] ?: null,
                'consent_ads' => $src['consent_ads'] ?: null,
            ]);

            foreach ($e['fichiers'] as $f) {
                $b->inserer('fichier', [
                    'demande_id' => $demandeId,
                    'identifiant' => $f['identifiant'],
                    'nom_original' => $f['nom'],
                    'type_mime' => $f['type'],
                    'taille' => (int) $f['taille'],
                    'sha256' => $f['sha256'],
                    'origine' => 'formulaire',
                    'cree_le' => $e['recue_le'],
                ]);
            }

            $libelles = ['devis' => 'demande de devis', 'rappel' => 'demande de rappel', 'envoi_postal_guide' => 'guide imprimé par la poste'];
            $saisie = ($e['cree_par'] ?? null) !== null;
            $b->inserer('interaction', [
                'demande_id' => $demandeId,
                'type' => $saisie ? 'appel_entrant' : 'systeme',
                'contenu' => $saisie ? 'Demande saisie dans l\'admin (' . (['telephone' => 'appel reçu', 'email' => 'e-mail reçu', 'visite' => 'visite au bureau', 'recommandation' => 'rencontre'][$e['canal']] ?? $e['canal']) . ')' : 'Demande reçue par le site (' . ($libelles[$e['formulaire']] ?? $e['formulaire']) . ')',
                'auteur_id' => $e['cree_par'] ?? null,
                'origine' => $saisie ? 'admin' : 'site',
                'cree_le' => $e['recue_le'],
            ]);
            if ($e['accuse_reception'] === 'envoye') {
                $b->inserer('interaction', [
                    'demande_id' => $demandeId, 'type' => 'email_sortant', 'contenu' => 'Accusé de réception envoyé',
                    'origine' => 'site', 'cree_le' => $e['recue_le'],
                ]);
            }
            $b->inserer('journal_audit', [
                'quand' => $maintenant, 'utilisateur_id' => $e['cree_par'] ?? null, 'acteur' => $saisie ? 'utilisateur' : 'site',
                'action' => 'demande_creee', 'objet_type' => 'demande', 'objet_id' => $e['ref'],
                'details' => json_encode(['canal' => $e['canal'], 'formulaire' => $e['formulaire']]),
            ]);
            return true;
        });
    }

    private ?array $grille = null;

    private function grille(): array
    {
        return $this->grille ??= (array) json_decode((string) file_get_contents(dirname(__DIR__) . '/data/scoring.json'), true);
    }

    private function versionGrille(): string
    {
        return (string) ($this->grille()['version'] ?? '');
    }

    /** @return array<string, string> */
    private function connuPar(): array
    {
        return (array) ($this->grille()['connu_par'] ?? []);
    }
}
