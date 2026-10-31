<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Traitement complet d'une requête vers demande.php.
 *
 * Ordre : méthode → taille → origine → limite de débit → pot de miel →
 * validation → jeton horodaté → contenu → fichiers → référence → zone, source,
 * score, échéance → e-mail interne (part toujours) → accusé de réception →
 * webhook n8n (ou file d'attente) → réponse.
 */
final class Traitement
{
    private Stockage $stockage;
    private Journal $journal;
    private AntiSpam $antiSpam;
    private Courriel $courriel;
    private Modeles $modeles;
    private Webhook $webhook;
    private LiensFichiers $liens;
    private Jeton $jetons;
    private HeuresOuvrables $heures;
    private Scoring $scoring;
    private Localite $localite;

    public function __construct(private Config $config, private bool $exigerTeleversementHttp = true)
    {
        $racine = dirname(__DIR__);
        $this->stockage = new Stockage((string) $config->get('stockage'));
        $this->journal = new Journal($this->stockage);
        $this->antiSpam = new AntiSpam($config);
        $this->courriel = new Courriel($config, $this->stockage, $this->journal);
        $this->modeles = new Modeles($config, $racine . '/modeles');
        $this->liens = new LiensFichiers((string) $config->get('url_api'), $config->secret('local'));
        $this->webhook = new Webhook($config, $this->stockage, $this->journal, $this->liens);
        $this->jetons = new Jeton($config->secret('actions'));
        $this->heures = HeuresOuvrables::depuisConfig($config);
        $this->scoring = Scoring::depuisFichier($racine . '/data/scoring.json');
        $this->localite = Localite::depuisFichier($racine . '/data/zones.json');
    }

    public function stockage(): Stockage
    {
        return $this->stockage;
    }

    public function journal(): Journal
    {
        return $this->journal;
    }

    public function webhook(): Webhook
    {
        return $this->webhook;
    }

    public function courriel(): Courriel
    {
        return $this->courriel;
    }

    public function modeles(): Modeles
    {
        return $this->modeles;
    }

    private function msg(string $code): string
    {
        $tel = (string) $this->config->get('entreprise.tel_fixe', '+41 22 771 20 15');
        $email = (string) $this->config->get('entreprise.email', 'contact@andyconstruct.ch');
        $mo = (int) $this->config->get('fichiers.max_taille_mo', 8);
        $nb = (int) $this->config->get('fichiers.max_nombre', 3);
        return match ($code) {
            'methode' => 'Cette adresse reçoit uniquement les formulaires du site andyconstruct.ch.',
            'origine' => "Votre demande n'a pas pu être envoyée depuis cette page. Appelez-nous au $tel.",
            'trop_de_demandes' => "Nous avons reçu plusieurs envois depuis votre connexion en peu de temps. Merci de réessayer dans une heure, ou appelez-nous au $tel.",
            'trop_volumineux' => "Les fichiers sont trop lourds ($mo Mo par fichier, $nb fichiers au maximum). Retirez-en un, ou envoyez-les par e-mail à $email.",
            'trop_rapide' => "Votre demande est presque partie : vérifiez vos informations, puis appuyez à nouveau sur le bouton d'envoi.",
            'validation' => "Il manque une information, ou l'une d'elles est à vérifier. Les champs concernés sont indiqués.",
            default => "Un problème technique nous empêche d'enregistrer votre demande. Vos informations ne sont pas perdues : réessayez dans quelques minutes, ou appelez-nous au $tel.",
        };
    }

    /**
     * @param array<string, mixed> $server $_SERVER
     * @param array<string, mixed> $get $_GET
     * @param array<string, mixed> $post $_POST
     * @param array<string, mixed> $files $_FILES
     */
    public function executer(array $server, array $get, array $post, array $files, ?\DateTimeImmutable $maintenant = null): Resultat
    {
        $debut = microtime(true);
        $maintenant ??= new \DateTimeImmutable('now', new \DateTimeZone('Europe/Zurich'));
        $methode = strtoupper((string) ($server['REQUEST_METHOD'] ?? 'GET'));
        $json = self::veutJson($server);

        if ($methode === 'GET' && array_key_exists('jeton', $get)) {
            return new Resultat(200, 'json', ['ok' => true, 'jeton' => $this->antiSpam->creerJeton($maintenant->getTimestamp())]);
        }
        if ($methode !== 'POST') {
            return new Resultat(405, 'json', ['ok' => false, 'code' => 'methode', 'message' => $this->msg('methode')], entetes: ['Allow' => 'POST, GET']);
        }
        if ($post === [] && $files === [] && (int) ($server['CONTENT_LENGTH'] ?? 0) > 0) {
            $this->journal->alerte('requete_trop_volumineuse', ['octets' => (int) $server['CONTENT_LENGTH']]);
            return $this->erreur($json, 413, 'trop_volumineux', [], $server);
        }
        if (!$this->antiSpam->origineAutorisee($server)) {
            $this->journal->alerte('origine_refusee', ['origine' => mb_substr((string) ($server['HTTP_ORIGIN'] ?? ''), 0, 100)]);
            return $this->erreur($json, 403, 'origine', [], $server);
        }

        $cleInterne = (string) $this->config->get('cle_saisie_interne', '');
        $saisieInterne = $cleInterne !== '' && is_string($post['cle_interne'] ?? null)
            && hash_equals($cleInterne, (string) $post['cle_interne']);

        $ip = LimiteDebit::ipClient(
            $server,
            (bool) $this->config->get('faire_confiance_au_proxy'),
            array_values(array_filter((array) $this->config->get('proxys_de_confiance', []), 'is_string'))
        );
        $limiteur = new LimiteDebit($this->stockage, $this->config->secret('local') . '|ip');
        $empreinteIp = substr($limiteur->empreinte($ip), 0, 12);
        // Deux seaux : toutes les tentatives (large, pour ne pas bloquer une personne
        // qui corrige plusieurs fois le formulaire) et les demandes acceptées (5 par heure).
        if (!$saisieInterne) {
            $limite = $limiteur->tenter($ip, 'tentatives', (int) $this->config->get('anti_spam.tentatives_par_heure', 30), $maintenant->getTimestamp());
            if (!$limite['autorise']) {
                $this->journal->alerte('limite_debit', ['seau' => 'tentatives', 'ip_hachee' => $empreinteIp]);
                return $this->erreur($json, 429, 'trop_de_demandes', [], $server, ['Retry-After' => (string) $limite['reessayer_dans']]);
            }
        }

        if ($this->antiSpam->potDeMielRempli($post)) {
            $this->journal->info('spam', ['raison' => 'pot_de_miel', 'ip_hachee' => $empreinteIp]);
            return $this->succesLeurre($json, (string) ($post['formulaire'] ?? 'devis'));
        }

        $validateur = new Validateur(
            array_filter((array) $this->config->get('guides', []), static fn ($g) => is_array($g) && !empty($g['actif']))
        );
        [$d, $erreurs, $avertissements] = $validateur->valider($post);
        $formulaire = $d['formulaire'];
        if (!$saisieInterne && ($d['canal'] ?? '') === 'telephone') {
            $d['canal'] = 'site';
            $avertissements[] = 'canal_telephone_refuse';
        }

        $jeton = ['statut' => 'interne', 'delai' => null];
        if (!$saisieInterne) {
            $jeton = $this->antiSpam->verifierJeton(is_string($post['form_t0'] ?? null) ? $post['form_t0'] : '', $formulaire, $maintenant->getTimestamp());
            if ($jeton['statut'] === 'trop_rapide') {
                $this->journal->info('spam', ['raison' => 'trop_rapide', 'delai' => $jeton['delai'], 'ip_hachee' => $empreinteIp]);
                return $this->erreur($json, 422, 'trop_rapide', [], $server);
            }
            if ($jeton['statut'] === 'invalide') {
                $this->journal->info('spam', ['raison' => 'jeton_invalide', 'ip_hachee' => $empreinteIp]);
                return $this->succesLeurre($json, $formulaire);
            }
            $suspect = $this->antiSpam->contenuSuspect($d);
            if ($suspect !== null) {
                $this->journal->info('spam', ['raison' => $suspect, 'ip_hachee' => $empreinteIp]);
                return $this->succesLeurre($json, $formulaire);
            }
        }

        // Fichiers : contrôlés même si d'autres champs sont en erreur (tout signaler d'un coup).
        $televersement = new Televersement(
            $this->stockage,
            (int) $this->config->get('fichiers.max_nombre', 3),
            (int) $this->config->get('fichiers.max_taille_mo', 8) * 1048576,
            (bool) $this->config->get('fichiers.refuser_pdf_actifs', true),
            $this->exigerTeleversementHttp,
            (string) $this->config->get('entreprise.email', 'contact@andyconstruct.ch')
        );
        $aTeleverser = $formulaire === 'envoi_postal_guide' ? [] : Televersement::aplatir($files);
        $fichiers = [];
        if ($erreurs === []) {
            [$fichiers, $erreurFichier, $raisonFichier] = $televersement->traiter($aTeleverser);
        } else {
            [$fichiers, $erreurFichier, $raisonFichier] = [[], null, null];
        }
        if ($erreurFichier !== null) {
            $erreurs['fichiers'] = $erreurFichier;
            $this->journal->info('fichier_refuse', ['raison' => $raisonFichier, 'ip_hachee' => $empreinteIp]);
        }
        if ($erreurs !== []) {
            $this->journal->info('validation', ['formulaire' => $formulaire, 'champs' => array_keys($erreurs), 'avertissements' => $avertissements]);
            foreach ($fichiers as $f) {
                @unlink($f['chemin']);
            }
            return $this->erreur($json, 422, 'validation', $erreurs, $server);
        }
        if (!$saisieInterne) {
            $limite = $limiteur->tenter($ip, 'demandes', (int) $this->config->get('anti_spam.limite_par_heure', 5), $maintenant->getTimestamp());
            if (!$limite['autorise']) {
                foreach ($fichiers as $f) {
                    @unlink($f['chemin']);
                }
                $this->journal->alerte('limite_debit', ['seau' => 'demandes', 'ip_hachee' => $empreinteIp]);
                return $this->erreur($json, 429, 'trop_de_demandes', [], $server, ['Retry-After' => (string) $limite['reessayer_dans']]);
            }
        }

        try {
            $demande = $this->assembler($d, $formulaire, $fichiers, $jeton, $maintenant, $saisieInterne);
            $bilan = $this->distribuer($demande, $post);
        } catch (\Throwable $e) {
            $this->journal->erreur('exception', [
                'erreur' => Journal::nettoyerMessage($e->getMessage()),
                'fichier' => basename($e->getFile()) . ':' . $e->getLine(),
            ]);
            return $this->erreur($json, 500, 'technique', [], $server);
        }

        $this->journal->info('demande_recue', [
            'ref' => $demande['ref'],
            'formulaire' => $formulaire,
            'canal' => $demande['canal'],
            'priorite' => $demande['scoring']['priorite'] ?? null,
            'score' => $demande['scoring']['score'] ?? null,
            'zone' => (string) $demande['localite']['zone'],
            'nb_fichiers' => count($fichiers),
            'interne' => $bilan['interne'],
            'accuse' => $bilan['accuse'],
            'webhook' => $bilan['webhook'],
            'jeton' => $jeton['statut'],
            'ip_hachee' => $empreinteIp,
            'avertissements' => $avertissements,
            'duree_ms' => (int) round((microtime(true) - $debut) * 1000),
        ]);

        if (!$bilan['interne'] && !in_array($bilan['webhook'], ['livre', 'en_file', 'simule'], true) && !$bilan['interne_mis_de_cote']) {
            return $this->erreur($json, 500, 'technique', [], $server);
        }

        $message = $this->messageSucces($demande);
        if ($json) {
            return new Resultat(200, 'json', ['ok' => true, 'message' => $message, 'ref' => $demande['ref']]);
        }
        return new Resultat(303, 'redirection', redirection: $this->pageMerci($formulaire));
    }

    /**
     * @param array<string, mixed> $d
     * @param list<array<string, mixed>> $fichiers
     * @param array{statut: string, delai: ?int} $jeton
     * @return array<string, mixed>
     */
    private function assembler(array $d, string $formulaire, array $fichiers, array $jeton, \DateTimeImmutable $maintenant, bool $saisieInterne): array
    {
        $ref = Reference::suivante($this->stockage, (string) $this->config->get('reference_prefixe', 'AC'), (int) $maintenant->format('Y'));
        $localite = $this->localite->resoudre($d['npa'], $d['commune']);
        $source = Source::normaliser([
            'utm_source' => $d['utm']['utm_source'], 'utm_medium' => $d['utm']['utm_medium'],
            'utm_campaign' => $d['utm']['utm_campaign'], 'gclid' => $d['gclid'],
            'referent' => $d['referent'], 'canal' => $d['canal'], 'formulaire' => $formulaire,
        ], (string) parse_url((string) $this->config->get('url_site'), PHP_URL_HOST) ?: 'andyconstruct.ch');

        $scoring = null;
        $echeance = null;
        $promesse = null;
        if ($formulaire !== 'envoi_postal_guide') {
            $scoring = $this->scoring->calculer([
                'type_client' => $d['type_client'],
                'service' => $d['service'],
                'surface' => $d['surface'],
                'zone' => $localite['zone'],
                'delai' => $d['delai'],
                'source_categorie' => $source['categorie'],
                'connu_par' => $d['connu_par'],
                'canal' => $d['canal'],
                'formulaire' => $formulaire,
                'message' => $d['message'],
                'telephone' => $d['telephone'] !== null,
                'nb_fichiers' => count($fichiers),
            ]);
            $echeance = $this->heures->echeance($scoring['priorite'], $maintenant);
            $promesse = $this->heures->formulerEcheance($echeance, $maintenant);
        }

        $estB2b = in_array($d['type_client'] ?: $d['profil'], Champs::TYPES_B2B, true);
        $role = $estB2b ? 'bureau' : 'terrain';
        $associe = (array) $this->config->get("associes.$role", []);

        $urlDesinscription = '';
        $baseStop = (string) $this->config->get('n8n.url_desinscription', '');
        if ($formulaire === 'envoi_postal_guide' && $d['conseils_email'] && $baseStop !== '' && $d['email'] !== '') {
            $urlDesinscription = $baseStop . (str_contains($baseStop, '?') ? '&' : '?') . 't='
                . $this->jetons->creer(['a' => 'stop', 'e' => $d['email'], 'r' => $ref], 400 * 86400, $maintenant->getTimestamp());
        }

        return [
            'ref' => $ref,
            'recu_le' => $maintenant,
            'formulaire' => $formulaire,
            'canal' => $d['canal'],
            'saisie_interne' => $saisieInterne,
            'd' => $d,
            'localite' => $localite,
            'source' => $source,
            'scoring' => $scoring,
            'echeance' => $echeance,
            'promesse' => $promesse,
            'associe' => [
                'role' => $role,
                'nom' => (string) ($associe['nom'] ?? ''),
                'email' => Validateur::normaliserEmail((string) ($associe['email'] ?? '')) ?? '',
            ],
            'fichiers' => $fichiers,
            'jeton' => $jeton,
            'url_desinscription' => $urlDesinscription,
        ];
    }

    /**
     * E-mail interne, accusé de réception, webhook.
     *
     * @param array<string, mixed> $demande
     * @param array<string, mixed> $post
     * @return array{interne: bool, interne_mis_de_cote: bool, accuse: string, webhook: string}
     */
    private function distribuer(array $demande, array $post): array
    {
        $d = $demande['d'];
        $formulaire = $demande['formulaire'];
        $bilan = ['interne' => false, 'interne_mis_de_cote' => false, 'accuse' => 'non', 'webhook' => 'non'];

        // 1. E-mail interne : part toujours (pour un guide, c'est la consigne d'envoi postal).
        $listeFichiers = [];
        $total = array_sum(array_column($demande['fichiers'], 'taille'));
        $joindre = $total <= (int) $this->config->get('fichiers.pj_max_total_mo', 20) * 1048576;
        foreach ($demande['fichiers'] as $f) {
            $listeFichiers[] = [
                'nom' => $f['nom'],
                'taille' => $f['taille'],
                'joint' => $joindre,
                'url' => $joindre ? '' : $this->liens->url($f['id'], (int) $this->config->get('fichiers.lien_validite_h_interne', 168)),
            ];
        }
        $message = $this->modeles->interne($demande, $this->liensActions($demande), $listeFichiers);
        if ($joindre) {
            foreach ($demande['fichiers'] as $f) {
                $message->pieces[] = ['chemin' => $f['chemin'], 'nom' => $f['nom'], 'type' => $f['type']];
            }
        }
        $r = $this->courriel->envoyer($message);
        $bilan['interne'] = $r['ok'];
        $bilan['interne_mis_de_cote'] = !$r['ok'];

        // 2. Accusé de réception (seulement si une adresse e-mail est fournie). Le formulaire
        //    écrit à une adresse saisie par le visiteur : plafonds par adresse et global pour
        //    qu'il ne serve pas de relais d'envoi vers des tiers.
        $confirmer = !$demande['saisie_interne'] || (($post['envoyer_confirmation'] ?? '') === 'oui');
        if ($d['email'] !== '' && $confirmer) {
            $accuse = $this->modeles->accuse($demande);
            if ($accuse !== null && !$demande['saisie_interne'] && !$this->accuseAutorise($d['email'], $demande['recu_le']->getTimestamp(), $demande['ref'])) {
                $accuse = null;
                $bilan['accuse'] = 'limite';
            }
            if ($accuse !== null) {
                $r = $this->courriel->envoyer($accuse);
                $bilan['accuse'] = $r['ok'] ? 'envoye' : 'mis_de_cote';
            }
        }

        // 3. Webhook n8n (ou file d'attente).
        $charge = $this->charge($demande, $bilan['accuse']);
        $bilan['webhook'] = $this->webhook->transmettre($formulaire === 'envoi_postal_guide' ? 'guide' : 'demande', $charge, $demande['ref']);
        return $bilan;
    }

    /**
     * Plafonds des accusés de réception : par adresse destinataire (24 h glissantes)
     * et pour tout le site (par heure). Au-delà, la demande est traitée normalement
     * (e-mail interne, n8n) mais aucun accusé ne part.
     */
    private function accuseAutorise(string $email, int $maintenant, string $ref): bool
    {
        $limiteur = new LimiteDebit($this->stockage, $this->config->secret('local') . '|accuse');
        $parAdresse = $limiteur->tenter('email|' . strtolower($email), 'accuse-adresse', max(1, (int) $this->config->get('anti_spam.accuses_par_adresse_24h', 3)), $maintenant, 86400);
        if (!$parAdresse['autorise']) {
            $this->journal->alerte('accuse_limite', ['ref' => $ref, 'seau' => 'adresse']);
            return false;
        }
        $global = $limiteur->tenter('site', 'accuse-global', max(1, (int) $this->config->get('anti_spam.accuses_par_heure', 20)), $maintenant);
        if (!$global['autorise']) {
            $this->journal->alerte('accuse_limite', ['ref' => $ref, 'seau' => 'global']);
            return false;
        }
        return true;
    }

    /** @return array<string, string> libellé => URL */
    private function liensActions(array $demande): array
    {
        $base = (string) $this->config->get('n8n.url_actions', '');
        if ($base === '' || $demande['formulaire'] === 'envoi_postal_guide') {
            return [];
        }
        $actions = [
            "J'ai eu la personne" => 'contact-etabli',
            'Pas de réponse' => 'pas-de-reponse',
            'Hors cible' => 'hors-cible',
        ];
        if (($demande['scoring']['priorite'] ?? '') === 'hors-cible') {
            $actions['Envoyer la réponse de réorientation'] = 'envoyer-reorientation';
        }
        $liens = [];
        foreach ($actions as $libelle => $action) {
            $jeton = $this->jetons->creer(['a' => $action, 'r' => $demande['ref']], 7 * 86400, $demande['recu_le']->getTimestamp());
            $liens[$libelle] = $base . (str_contains($base, '?') ? '&' : '?') . 't=' . $jeton;
        }
        return $liens;
    }

    /**
     * Charge utile JSON envoyée à n8n (version 1, voir docs/v2/contrat-interface.md §7).
     *
     * @param array<string, mixed> $demande
     * @return array<string, mixed>
     */
    public function charge(array $demande, string $accuse): array
    {
        $d = $demande['d'];
        $tel = $d['telephone'];
        $s = $demande['scoring'];
        $vars = $this->modeles->variables($demande);
        $guide = (array) $this->config->get('guides.' . $d['guide'], []);
        return [
            'evenement' => $demande['formulaire'] === 'envoi_postal_guide' ? 'guide.envoi_postal' : 'demande.creee',
            'version' => 1,
            'ref' => $demande['ref'],
            'recu_le' => $demande['recu_le']->format('c'),
            'mode_test' => $this->config->modeTest(),
            'formulaire' => $demande['formulaire'],
            'canal' => $demande['canal'],
            'contact' => [
                'civilite' => $d['civilite'],
                'nom' => $d['nom'],
                'prenom' => $d['prenom'],
                'salutation' => $vars['salutation'],
                'email' => $d['email'],
                'telephone' => $tel['e164'] ?? '',
                'telephone_affiche' => $tel['affiche'] ?? '',
                'telephone_mobile' => (bool) ($tel['mobile'] ?? false),
                'telephone_suisse' => (bool) ($tel['suisse'] ?? false),
                'preference_contact' => $d['preference_contact'],
                'creneau' => $d['creneau'],
                'adresse_postale' => $d['adresse_postale'],
                'adresse' => $d['adresse'],
                'npa' => $d['npa'],
                'localite' => $d['localite'],
            ],
            'projet' => [
                'travaux' => $d['travaux'],
                'service' => $d['service'],
                'service_libelle' => $vars['travaux'],
                'type_client' => $d['type_client'],
                'surface' => $d['surface'],
                'delai' => $d['delai'],
                'commune' => $d['commune'],
                'npa' => $d['npa'] !== '' ? $d['npa'] : (string) ($demande['localite']['npa'] ?? ''),
                'canton' => (string) ($demande['localite']['canton'] ?? ''),
                'zone' => (string) $demande['localite']['zone'],
                'localite_methode' => $demande['localite']['methode'],
                'message' => $d['message'],
                'recommande_par' => $d['recommande_par'],
                'connu_par' => $d['connu_par'],
            ],
            'guide' => $demande['formulaire'] === 'envoi_postal_guide' ? [
                'slug' => $d['guide'],
                'titre' => (string) ($guide['titre'] ?? ''),
                'url' => (string) ($guide['url'] ?? ''),
                'liste_brevo' => (int) ($guide['liste_brevo'] ?? 0),
                'profil' => $d['profil'],
                'conseils_email' => $d['conseils_email'] && $d['email'] !== '',
                'accuse_envoye_par_php' => $accuse === 'envoye',
            ] : null,
            'scoring' => $s === null ? null : [
                'score' => $s['score'],
                'priorite' => $s['priorite'],
                'detail' => $s['detail'],
                'regles' => $s['regles'],
                'hors_cible' => $s['hors_cible'],
                'echeance' => $demande['echeance']?->format('c'),
                'promesse' => $vars['promesse'],
            ],
            'attribution' => [
                'role' => $demande['associe']['role'],
                'associe' => $demande['associe']['nom'],
                'email' => $demande['associe']['email'],
            ],
            'source' => [
                'categorie' => $demande['source']['categorie'],
                'libelle' => $demande['source']['libelle'],
                'emplacement' => $d['source'],
                'page' => $d['page'],
                'page_entree' => $d['page_entree'],
                'referent' => $d['referent'],
                'utm_source' => $d['utm']['utm_source'],
                'utm_medium' => $d['utm']['utm_medium'],
                'utm_campaign' => $d['utm']['utm_campaign'],
                'utm_content' => $d['utm']['utm_content'],
                'utm_term' => $d['utm']['utm_term'],
                'gclid' => $d['gclid'],
                'consent_ads' => $d['consent_ads'],
            ],
            'fichiers' => array_map(static fn ($f) => [
                'id' => $f['id'], 'nom' => $f['nom'], 'type' => $f['type'], 'taille' => $f['taille'], 'sha256' => $f['sha256'],
            ], $demande['fichiers']),
            'accuse_reception' => $accuse,
            'anti_spam' => ['jeton' => $demande['jeton']['statut'], 'delai_remplissage_s' => $demande['jeton']['delai']],
        ];
    }

    private function messageSucces(array $demande): string
    {
        $d = $demande['d'];
        if ($demande['formulaire'] === 'envoi_postal_guide') {
            return 'Merci. Le guide part par la poste dans les prochains jours.'
                . ($d['email'] !== '' ? ' Une confirmation vient de vous être envoyée par e-mail.' : '');
        }
        $v = $this->modeles->variables($demande);
        if ($demande['formulaire'] === 'rappel') {
            return "Merci, c'est noté : nous vous rappelons {$v['promesse']} au {$v['telephone']}.";
        }
        if ($v['hors_cible']) {
            $phrase = "Merci, votre demande est bien arrivée. Nous l'examinons et vous répondons {$v['promesse']}.";
        } else {
            $phrase = "Merci, votre demande est bien arrivée. {$v['qui_majuscule']} vous {$v['verbe_contact']} {$v['promesse']}.";
        }
        return $phrase . ($d['email'] !== '' ? ' Un e-mail de confirmation vient de vous être envoyé.' : '');
    }

    private function pageMerci(string $formulaire): string
    {
        return (string) $this->config->get("pages.merci_$formulaire", '/merci.html');
    }

    /** Réponse identique à un succès, sans aucun traitement (robots détectés). */
    private function succesLeurre(bool $json, string $formulaire): Resultat
    {
        if ($json) {
            return new Resultat(200, 'json', ['ok' => true, 'message' => 'Merci, votre demande est bien arrivée.', 'ref' => null]);
        }
        $formulaire = in_array($formulaire, Champs::FORMULAIRES, true) ? $formulaire : 'devis';
        return new Resultat(303, 'redirection', redirection: $this->pageMerci($formulaire));
    }

    /** @param array<string, string> $erreurs @param array<string, string> $entetes */
    private function erreur(bool $json, int $statut, string $code, array $erreurs, array $server, array $entetes = []): Resultat
    {
        $message = $this->msg($code);
        if ($json) {
            $corps = ['ok' => false, 'code' => $code, 'message' => $message, 'ref' => null];
            if ($erreurs) {
                $corps['erreurs'] = $erreurs;
            }
            return new Resultat($statut, 'json', $corps, entetes: $entetes);
        }
        return new Resultat($statut, 'html', html: $this->pageErreur($message, $erreurs, $server), entetes: $entetes);
    }

    /** Page de secours pour un envoi sans JavaScript : erreurs listées, retour au formulaire. */
    private function pageErreur(string $message, array $erreurs, array $server): string
    {
        $h = static fn (string $v): string => htmlspecialchars($v, ENT_QUOTES | ENT_HTML5, 'UTF-8');
        $retour = (string) $this->config->get('pages.formulaire', '/contact.html#formulaire');
        $referent = (string) ($server['HTTP_REFERER'] ?? '');
        $hoteSite = (string) parse_url((string) $this->config->get('url_site'), PHP_URL_HOST);
        $hoteRef = (string) parse_url($referent, PHP_URL_HOST);
        $schemaRef = strtolower((string) parse_url($referent, PHP_URL_SCHEME));
        if ($referent !== '' && $hoteRef !== '' && in_array($schemaRef, ['http', 'https'], true)
            && ($hoteRef === $hoteSite || $hoteRef === ($server['HTTP_HOST'] ?? ''))) {
            $retour = $referent;
        }
        $tel = (string) $this->config->get('entreprise.tel_fixe', '+41 22 771 20 15');
        $telE164 = Telephone::normaliser($tel)['e164'] ?? '+41227712015';
        $liste = '';
        foreach ($erreurs as $texte) {
            $liste .= '<li>' . $h($texte) . '</li>';
        }
        return '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            . '<meta name="robots" content="noindex"><title>Votre demande n\'est pas encore partie · Andy Construct</title>'
            . '<style>body{margin:0;background:#fff;color:#1D1F22;font:18px/1.6 "Source Sans 3",Arial,sans-serif}main{max-width:40rem;margin:0 auto;padding:2rem 1rem}'
            . 'h1{font:700 1.6rem/1.3 Montserrat,Arial,sans-serif;margin:0 0 1rem;border-left:6px solid #E8000F;padding-left:.75rem}'
            . 'ul{padding-left:1.25rem}li{margin:.25rem 0}a{color:#1D1F22}.bouton{display:inline-block;min-height:48px;box-sizing:border-box;padding:.7rem 1.2rem;background:#1D1F22;color:#fff;text-decoration:none;font-weight:700;border-radius:4px;margin:.5rem .5rem .5rem 0}'
            . '.secondaire{background:#fff;color:#1D1F22;border:2px solid #1D1F22}</style></head><body><main>'
            . '<h1>Votre demande n\'est pas encore partie</h1>'
            . '<p>' . $h($message) . '</p>'
            . ($liste !== '' ? '<ul>' . $liste . '</ul>' : '')
            . '<p>Utilisez le bouton « Retour » de votre navigateur : vos informations sont normalement conservées.</p>'
            . '<p><a class="bouton" href="' . $h($retour) . '">Revenir au formulaire</a>'
            . '<a class="bouton secondaire" href="tel:' . $h($telE164) . '">Appeler le ' . $h($tel) . '</a></p>'
            . '</main></body></html>';
    }

    /** Appel fetch (réponse JSON attendue) ou formulaire classique (redirection / page HTML). */
    public static function veutJson(array $server): bool
    {
        $accept = strtolower((string) ($server['HTTP_ACCEPT'] ?? ''));
        $xrw = strtolower((string) ($server['HTTP_X_REQUESTED_WITH'] ?? ''));
        return str_contains($accept, 'application/json') || $xrw === 'xmlhttprequest' || $xrw === 'fetch';
    }

    /**
     * Travaux après la réponse : relance de la file d'attente (3 éléments au plus)
     * et purge horaire du stockage. Ne lève jamais d'exception.
     */
    public function apresReponse(): void
    {
        try {
            $this->webhook->traiterFile(3);
            $marqueur = $this->stockage->dossier('verrous') . '/derniere-purge';
            if (!is_file($marqueur) || filemtime($marqueur) < time() - 3600) {
                @touch($marqueur);
                $this->purger();
            }
        } catch (\Throwable $e) {
            $this->journal->erreur('apres_reponse', ['erreur' => Journal::nettoyerMessage($e->getMessage())]);
        }
    }

    /** @return array<string, int> nombre de fichiers supprimés par dossier */
    public function purger(): array
    {
        return [
            'fichiers' => $this->stockage->purger('fichiers', (float) $this->config->get('fichiers.conservation_jours', 30)),
            'journaux' => $this->stockage->purger('journaux', (float) $this->config->get('conservation.journaux_jours', 30)),
            'limites' => $this->stockage->purger('limites', 1),
            'test-mails' => $this->stockage->purger('test-mails', (float) $this->config->get('conservation.mails_test_jours', 7)),
            'test-webhooks' => $this->stockage->purger('test-webhooks', (float) $this->config->get('conservation.mails_test_jours', 7)),
            'mails-echec' => $this->stockage->purger('mails-echec', 14),
        ];
    }
}
