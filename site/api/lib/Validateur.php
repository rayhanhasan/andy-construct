<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Validation et normalisation serveur de tous les champs reçus.
 *
 * Principe : strict sur les champs obligatoires, tolérant sur les listes
 * facultatives (une valeur inconnue est ignorée et journalisée, sans bloquer
 * le visiteur). Messages d'erreur en français simple, qui disent quoi faire.
 */
final class Validateur
{
    public const MESSAGES = [
        'nom' => 'Indiquez votre nom et votre prénom.',
        'prenom' => 'Indiquez votre prénom.',
        'contact' => 'Indiquez un numéro de téléphone ou une adresse e-mail pour que nous puissions vous répondre.',
        'telephone' => 'Ce numéro semble incomplet. Indiquez-le par exemple ainsi : 079 123 45 67.',
        'telephone_requis' => 'Indiquez le numéro auquel nous pouvons vous rappeler.',
        'email' => 'Cette adresse e-mail semble incomplète. Vérifiez-la, par exemple : nom@exemple.ch.',
        'travaux' => 'Choisissez le type de travaux (ou « Je ne sais pas encore »).',
        'commune' => 'Indiquez la commune des travaux ou son NPA.',
        'npa' => 'Le NPA compte 4 chiffres, par exemple 1227.',
        'accord' => 'Cochez cette case pour que nous puissions traiter votre demande.',
        'message' => "Votre message est trop long (3'000 caractères au maximum). Vous pouvez nous envoyer la suite par e-mail.",
        'texte_long' => 'Ce texte est trop long. Raccourcissez-le, s\'il vous plaît.',
        'aimant' => "Ce guide n'est pas disponible pour le moment. Appelez-nous, nous vous l'envoyons volontiers.",
        'email_aimant' => "Indiquez votre adresse e-mail, ou cochez « Je préfère le recevoir par la poste ».",
        'adresse_postale' => "Indiquez l'adresse à laquelle envoyer le guide (rue, NPA et localité).",
        'nom_poste' => 'Indiquez votre nom pour l\'envoi par la poste.',
        'formulaire' => "Le formulaire envoyé n'est pas reconnu. Rechargez la page, s'il vous plaît.",
    ];

    /**
     * @param array<string, mixed> $aimantsActifs slug => configuration
     * @param bool $accordObligatoire case « accord » exigée (devis, aimant) ; peut passer à
     *   false après avis du juriste (le devoir d'information suffit, nLPD art. 19).
     */
    public function __construct(private array $aimantsActifs = [], private bool $accordObligatoire = true)
    {
    }

    /**
     * @param array<string, mixed> $post
     * @return array{0: array<string, mixed>, 1: array<string, string>, 2: list<string>}
     *   [données normalisées, erreurs par champ, avertissements (journal)]
     */
    public function valider(array $post): array
    {
        $erreurs = [];
        $avert = [];
        $d = [];

        $formulaire = self::chaine($post, 'formulaire') ?: 'devis';
        if (!in_array($formulaire, Champs::FORMULAIRES, true)) {
            return [['formulaire' => 'devis'], ['formulaire' => self::MESSAGES['formulaire']], ['formulaire_inconnu']];
        }
        $d['formulaire'] = $formulaire;

        // Identité
        $d['civilite'] = self::liste($post, 'civilite', array_keys(Champs::CIVILITE), $avert);
        $d['nom'] = self::texte(self::chaine($post, 'nom'), false);
        $d['prenom'] = self::texte(self::chaine($post, 'prenom'), false);
        foreach (['nom' => 100, 'prenom' => 60] as $champ => $max) {
            if (mb_strlen($d[$champ]) > $max) {
                $erreurs[$champ] = self::MESSAGES['texte_long'];
            }
        }

        // Contact
        $d['email'] = '';
        $email = self::chaine($post, 'email');
        if ($email !== '') {
            $normalise = self::normaliserEmail($email);
            if ($normalise === null) {
                $erreurs['email'] = self::MESSAGES['email'];
            } else {
                $d['email'] = $normalise;
            }
        }
        $d['telephone'] = null;
        $tel = self::chaine($post, 'telephone');
        if ($tel !== '') {
            $d['telephone'] = Telephone::normaliser($tel);
            if ($d['telephone'] === null) {
                $erreurs['telephone'] = self::MESSAGES['telephone'];
            }
        }

        // Projet
        $travaux = $post['travaux'] ?? [];
        $travaux = is_array($travaux) ? $travaux : [$travaux];
        $d['travaux'] = [];
        foreach ($travaux as $t) {
            if (is_string($t) && isset(Champs::TRAVAUX[$t]) && !in_array($t, $d['travaux'], true)) {
                $d['travaux'][] = $t;
            } elseif (is_string($t) && $t !== '') {
                $avert[] = 'valeur_inconnue:travaux';
            }
        }
        $d['service'] = self::servicePrincipal($d['travaux']);
        $d['type_client'] = self::liste($post, 'type_client', array_keys(Champs::TYPE_CLIENT), $avert);
        $d['surface'] = self::liste($post, 'surface', array_keys(Champs::SURFACE), $avert);
        $d['delai'] = self::liste($post, 'delai', array_keys(Champs::DELAI), $avert);
        $d['connu_par'] = self::liste($post, 'connu_par', array_keys(Champs::CONNU_PAR), $avert);
        $d['preference_contact'] = self::liste($post, 'preference_contact', array_keys(Champs::PREFERENCE_CONTACT), $avert);
        if ($d['preference_contact'] === '' && self::chaine($post, 'rappel') === 'oui') {
            $d['preference_contact'] = 'appel'; // compatibilité avec l'ancienne case « rappelez-moi »
        }
        $d['creneau'] = self::liste($post, 'creneau', array_keys(Champs::CRENEAU), $avert);

        $d['npa'] = preg_replace('/\s/', '', self::chaine($post, 'npa')) ?? '';
        if ($d['npa'] !== '' && !preg_match('/^[1-9]\d{3}$/', $d['npa'])) {
            $erreurs['npa'] = self::MESSAGES['npa'];
        }
        $d['commune'] = self::texte(self::chaine($post, 'commune'), false);
        if (mb_strlen($d['commune']) > 80) {
            $erreurs['commune'] = self::MESSAGES['texte_long'];
        }
        $d['message'] = self::texte(self::chaine($post, 'message', 20000), true);
        if (mb_strlen($d['message']) > 3000) {
            $erreurs['message'] = self::MESSAGES['message'];
        }
        $d['recommande_par'] = self::texte(self::chaine($post, 'recommande_par'), false);
        if (mb_strlen($d['recommande_par']) > 100) {
            $erreurs['recommande_par'] = self::MESSAGES['texte_long'];
        }
        $d['accord'] = in_array(self::chaine($post, 'accord'), ['oui', 'on', '1'], true);

        // Aimant
        $d['aimant'] = self::chaine($post, 'aimant');
        $d['profil'] = self::liste($post, 'profil', array_keys(Champs::PROFIL), $avert);
        $d['par_poste'] = in_array(self::chaine($post, 'par_poste'), ['oui', 'on', '1'], true);
        $d['newsletter'] = in_array(self::chaine($post, 'newsletter'), ['oui', 'on', '1'], true);
        $d['adresse_postale'] = self::texte(self::chaine($post, 'adresse_postale', 1000), true);
        if (mb_strlen($d['adresse_postale']) > 300) {
            $erreurs['adresse_postale'] = self::MESSAGES['texte_long'];
        }

        // Source (champs cachés)
        $d['canal'] = self::liste($post, 'canal', Champs::CANAL, $avert) ?: 'site';
        $d['source'] = self::slug(self::chaine($post, 'source'), 50);
        $d['page'] = self::chemin(self::chaine($post, 'page'));
        $d['page_entree'] = self::chemin(self::chaine($post, 'page_entree'));
        $d['referent'] = self::hote(self::chaine($post, 'referent'));
        $d['utm'] = [];
        foreach (['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'] as $utm) {
            $d['utm'][$utm] = self::utm(self::chaine($post, $utm));
        }
        $d['consent_ads'] = self::liste($post, 'consent_ads', Champs::CONSENT_ADS, $avert);
        $gclid = self::chaine($post, 'gclid');
        $d['gclid'] = ($d['consent_ads'] === 'accorde' && preg_match('/^[A-Za-z0-9_-]{10,200}$/', $gclid)) ? $gclid : '';

        // Règles par formulaire
        $aTelephone = $d['telephone'] !== null;
        $aEmail = $d['email'] !== '';
        switch ($formulaire) {
            case 'devis':
                if ($d['nom'] === '') {
                    $erreurs['nom'] ??= self::MESSAGES['nom'];
                }
                if (!$aTelephone && !$aEmail && !isset($erreurs['telephone']) && !isset($erreurs['email'])) {
                    $erreurs['telephone'] = self::MESSAGES['contact'];
                }
                if ($d['travaux'] === []) {
                    $erreurs['travaux'] = self::MESSAGES['travaux'];
                }
                if ($d['commune'] === '' && $d['npa'] === '') {
                    $erreurs['commune'] = self::MESSAGES['commune'];
                }
                if ($d['preference_contact'] === 'appel' && !$aTelephone && !isset($erreurs['telephone'])) {
                    $erreurs['telephone'] = self::MESSAGES['telephone_requis'];
                }
                if (!$d['accord'] && $this->accordObligatoire) {
                    $erreurs['accord'] = self::MESSAGES['accord'];
                }
                break;
            case 'rappel':
                if (!$aTelephone && !isset($erreurs['telephone'])) {
                    $erreurs['telephone'] = self::MESSAGES['telephone_requis'];
                }
                break;
            case 'aimant':
                if ($d['prenom'] === '' && $d['nom'] === '') {
                    $erreurs['prenom'] = self::MESSAGES['prenom'];
                }
                if (!isset($this->aimantsActifs[$d['aimant']])) {
                    $erreurs['aimant'] = self::MESSAGES['aimant'];
                }
                if ($d['par_poste']) {
                    if ($d['adresse_postale'] === '') {
                        $erreurs['adresse_postale'] ??= self::MESSAGES['adresse_postale'];
                    }
                    if ($d['nom'] === '') {
                        $erreurs['nom'] ??= self::MESSAGES['nom_poste'];
                    }
                } elseif (!$aEmail && !isset($erreurs['email'])) {
                    $erreurs['email'] = self::MESSAGES['email_aimant'];
                }
                if (!$d['accord'] && $this->accordObligatoire) {
                    $erreurs['accord'] = self::MESSAGES['accord'];
                }
                break;
        }

        return [$d, $erreurs, array_values(array_unique($avert))];
    }

    /** @param list<string> $travaux */
    public static function servicePrincipal(array $travaux): string
    {
        $prestations = array_values(array_intersect($travaux, Champs::PRESTATIONS));
        return match (true) {
            count($prestations) >= 2 => 'plusieurs',
            count($prestations) === 1 => $prestations[0],
            in_array('autre', $travaux, true) => 'autre',
            in_array('ne-sait-pas', $travaux, true) => 'ne-sait-pas',
            default => '',
        };
    }

    /** Adresse e-mail sûre pour un en-tête : ASCII (IDN converti), sans espace ni guillemet. */
    public static function normaliserEmail(string $email): ?string
    {
        $email = trim($email);
        if ($email === '' || strlen($email) > 254 || preg_match('/[\r\n\0\s"<>,;\\\\]/', $email)) {
            return null;
        }
        $pos = strrpos($email, '@');
        if ($pos === false) {
            return null;
        }
        $local = substr($email, 0, $pos);
        $domaine = mb_strtolower(substr($email, $pos + 1));
        if (preg_match('/[^\x20-\x7e]/', $domaine)) {
            if (!function_exists('idn_to_ascii')) {
                return null;
            }
            $domaine = idn_to_ascii($domaine, IDNA_DEFAULT, INTL_IDNA_VARIANT_UTS46) ?: '';
        }
        $email = $local . '@' . $domaine;
        if (!preg_match('/^[A-Za-z0-9.!#$%&\'*+\/=?^_`{|}~-]{1,64}@[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+$/', $email)) {
            return null;
        }
        if (filter_var($email, FILTER_VALIDATE_EMAIL) === false) {
            return null;
        }
        return $email;
    }

    /** Lit un champ texte simple (un tableau reçu à la place est ignoré). */
    public static function chaine(array $post, string $cle, int $max = 5000): string
    {
        $v = $post[$cle] ?? '';
        if (!is_string($v)) {
            return '';
        }
        if (!mb_check_encoding($v, 'UTF-8')) {
            $v = mb_convert_encoding($v, 'UTF-8', 'UTF-8');
        }
        return trim(mb_substr($v, 0, $max));
    }

    /**
     * Supprime caractères de contrôle et marqueurs bidirectionnels ; conserve
     * les retours à la ligne si $multiligne.
     */
    public static function texte(string $v, bool $multiligne): string
    {
        $v = str_replace(["\r\n", "\r"], "\n", $v);
        $v = preg_replace('/[\x{202A}-\x{202E}\x{2066}-\x{2069}\x{200B}\x{FEFF}]/u', '', $v) ?? '';
        if ($multiligne) {
            $v = preg_replace('/[^\P{C}\n\t]/u', '', $v) ?? '';
            $v = preg_replace("/\n{3,}/", "\n\n", $v) ?? '';
        } else {
            $v = preg_replace('/\p{C}/u', ' ', $v) ?? '';
            $v = preg_replace('/\s+/u', ' ', $v) ?? '';
        }
        return trim($v);
    }

    /** @param list<string> $autorisees @param list<string> $avert */
    private static function liste(array $post, string $cle, array $autorisees, array &$avert): string
    {
        $v = self::chaine($post, $cle, 50);
        if ($v === '') {
            return '';
        }
        if (!in_array($v, $autorisees, true)) {
            $avert[] = "valeur_inconnue:$cle";
            return '';
        }
        return $v;
    }

    private static function slug(string $v, int $max): string
    {
        $v = strtolower($v);
        return preg_match('/^[a-z0-9][a-z0-9_-]*$/', $v) ? substr($v, 0, $max) : '';
    }

    private static function chemin(string $v): string
    {
        if ($v === '') {
            return '';
        }
        $chemin = parse_url($v, PHP_URL_PATH);
        if (!is_string($chemin) || !str_starts_with($chemin, '/')) {
            return '';
        }
        return substr(preg_replace('/[^A-Za-z0-9\/._~-]/', '', $chemin) ?? '', 0, 200);
    }

    private static function hote(string $v): string
    {
        $v = strtolower($v);
        if (str_contains($v, '//')) {
            $v = (string) parse_url($v, PHP_URL_HOST);
        }
        return preg_match('/^[a-z0-9.-]{1,100}$/', $v) ? $v : '';
    }

    private static function utm(string $v): string
    {
        $v = preg_replace('/[^\p{L}\p{N} ._\-{}|+:\/]/u', '', $v) ?? '';
        return mb_substr(trim($v), 0, 100);
    }
}
