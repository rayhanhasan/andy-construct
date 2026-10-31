<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Rendu des e-mails : accusés de réception (modeles/*.txt, texte relu par le
 * copywriter, voir automation/messages/) et notification interne.
 *
 * Syntaxe des modèles : {{variable}}, {{#variable}}…{{/variable}} (si non vide),
 * {{^variable}}…{{/variable}} (si vide). Le texte est la version de référence ;
 * la version HTML en est dérivée automatiquement (aucune image, aucun pixel).
 */
final class Modeles
{
    private const CRITERES = [
        'type_client' => 'Type de client', 'service' => 'Service', 'surface' => 'Ampleur',
        'zone' => 'Zone', 'delai' => 'Délai', 'source' => 'Source', 'bonus' => 'Bonus', 'malus' => 'Malus',
    ];
    private const COULEURS = ['A' => '#C4000D', 'B' => '#8A4B00', 'C' => '#44494F', 'hors-cible' => '#1D1F22'];

    public function __construct(private Config $config, private string $dossier)
    {
    }

    // ------------------------------------------------------------------ moteur

    /** @param array<string, mixed> $vars */
    public static function rendre(string $gabarit, array $vars): string
    {
        // Sections, de l'intérieur vers l'extérieur.
        $motif = '/\{\{([#^])([a-z0-9_]+)\}\}((?:(?!\{\{[#^]\2\}\}).)*?)\{\{\/\2\}\}/s';
        for ($i = 0; $i < 20 && preg_match($motif, $gabarit); $i++) {
            $gabarit = preg_replace_callback($motif, static function (array $m) use ($vars): string {
                $vrai = !empty($vars[$m[2]]);
                return ($m[1] === '#') === $vrai ? $m[3] : '';
            }, $gabarit) ?? '';
        }
        return preg_replace_callback('/\{\{([a-z0-9_]+)\}\}/', static function (array $m) use ($vars): string {
            $v = $vars[$m[1]] ?? '';
            return is_scalar($v) ? (string) $v : '';
        }, $gabarit) ?? '';
    }

    /** @return array{sujet: string, corps: string} */
    public function charger(string $nom): array
    {
        $contenu = (string) file_get_contents($this->dossier . '/' . $nom . '.txt');
        $contenu = str_replace("\r\n", "\n", $contenu);
        if (!preg_match('/^Objet : (.+)\n\n/u', $contenu, $m)) {
            throw new \RuntimeException("Modèle $nom : première ligne « Objet : … » attendue.");
        }
        return ['sujet' => $m[1], 'corps' => substr($contenu, strlen($m[0]))];
    }

    /** Version HTML sobre d'un texte : paragraphes, listes, liens complets cliquables. */
    public static function texteVersHtml(string $texte): string
    {
        $blocs = preg_split("/\n{2,}/", trim($texte)) ?: [];
        $html = '';
        foreach ($blocs as $bloc) {
            $lignes = explode("\n", $bloc);
            if ($lignes[0] === '--') {
                $html .= '<hr style="border:0;border-top:1px solid #D9DBDE;margin:24px 0 12px">';
                array_shift($lignes);
                $html .= '<p style="margin:0 0 12px;font-size:14px;color:#44494F">' . implode('<br>', array_map([self::class, 'ligneHtml'], $lignes)) . '</p>';
                continue;
            }
            $puces = array_filter($lignes, static fn ($l) => str_starts_with($l, '- '));
            if ($puces && count($puces) === count($lignes) - 1 && !str_starts_with($lignes[0], '- ')) {
                $html .= '<p style="margin:0 0 6px">' . self::ligneHtml($lignes[0]) . '</p><ul style="margin:0 0 16px;padding-left:20px">';
                foreach (array_slice($lignes, 1) as $l) {
                    $html .= '<li style="margin:0 0 4px">' . self::ligneHtml(substr($l, 2)) . '</li>';
                }
                $html .= '</ul>';
                continue;
            }
            $html .= '<p style="margin:0 0 16px">' . implode('<br>', array_map([self::class, 'ligneHtml'], $lignes)) . '</p>';
        }
        return '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head>'
            . '<body style="margin:0;padding:0;background:#FFFFFF">'
            . '<div style="max-width:600px;margin:0 auto;padding:24px 20px;font-family:Arial,Helvetica,sans-serif;font-size:17px;line-height:1.55;color:#1D1F22">'
            . $html . '</div></body></html>';
    }

    private static function ligneHtml(string $ligne): string
    {
        $e = htmlspecialchars($ligne, ENT_QUOTES | ENT_HTML5, 'UTF-8');
        return preg_replace_callback('~https?://[^\s<>"«»]+~u', static function (array $m): string {
            $url = rtrim($m[0], '.,;:)');
            $reste = substr($m[0], strlen($url));
            return '<a href="' . $url . '" style="color:#1D1F22">' . $url . '</a>' . $reste;
        }, $e) ?? $e;
    }

    // ------------------------------------------------------- accusé de réception

    /** @param array<string, mixed> $demande */
    public function accuse(array $demande): ?Message
    {
        $d = $demande['d'];
        if ($d['email'] === '') {
            return null;
        }
        $nom = match ($demande['formulaire']) {
            'rappel' => 'accuse-rappel',
            'aimant' => 'accuse-aimant',
            default => 'accuse-devis',
        };
        $modele = $this->charger($nom);
        $vars = $this->variables($demande);
        $texte = trim(self::rendre($modele['corps'], $vars)) . "\n";

        $m = new Message();
        $m->categorie = 'accuse-' . $demande['formulaire'];
        $m->ref = $demande['ref'];
        $m->sujet = self::rendre($modele['sujet'], $vars);
        $m->texte = $texte;
        $m->html = self::texteVersHtml($texte);
        $m->a = [[$d['email'], trim($d['prenom'] . ' ' . $d['nom'])]];
        $associe = $demande['associe'];
        $m->repondreA = $associe['email'] !== ''
            ? [$associe['email'], $associe['nom']]
            : [(string) $this->config->get('repondre_a.email'), (string) $this->config->get('repondre_a.nom')];
        return $m;
    }

    /**
     * Variables communes aux modèles (aussi transmises à n8n pour ses propres messages).
     *
     * @param array<string, mixed> $demande
     * @return array<string, mixed>
     */
    public function variables(array $demande): array
    {
        $d = $demande['d'];
        $associe = $demande['associe'];
        $qui = $associe['nom'] !== '' ? $associe['nom'] : "l'un de nos associés";
        $horsCible = ($demande['scoring']['priorite'] ?? '') === 'hors-cible';
        $parEmail = $d['telephone'] === null || $d['preference_contact'] === 'email';
        $verbe = $parEmail ? 'répond par e-mail' : ($horsCible ? 'répond' : 'appelle');
        $promesse = ($this->config->get('promesse_delai', true) && $demande['promesse'])
            ? $demande['promesse']
            : 'dans les meilleurs délais';
        $travaux = implode(', ', array_map(static fn ($t) => Champs::TRAVAUX[$t], $d['travaux']));
        $lieu = $d['commune'];
        if ($d['npa'] !== '' && !str_contains($lieu, $d['npa'])) {
            $lieu = trim($d['npa'] . ' ' . $lieu);
        }
        $extrait = preg_replace('~https?://\S+|www\.\S+~i', '[lien]', $d['message']) ?? '';
        $extrait = trim(preg_replace('/\s+/u', ' ', $extrait) ?? '');
        if (mb_strlen($extrait) > 200) {
            $extrait = rtrim(mb_substr($extrait, 0, 197)) . '…';
        }
        $aimant = (array) $this->config->get('aimants.' . $d['aimant'], []);
        $realisations = (array) $this->config->get('realisations_par_service', []);
        $e = (array) $this->config->get('entreprise');

        return [
            'ref' => $demande['ref'],
            'salutation' => self::salutation($d['civilite'], $d['nom'], $d['prenom']),
            'qui' => $qui,
            'qui_majuscule' => mb_strtoupper(mb_substr($qui, 0, 1)) . mb_substr($qui, 1),
            'verbe_contact' => $verbe,
            'numeros_appel' => $verbe === 'appelle' ? (string) $this->config->get('numeros_appel_sortant', '') : '',
            'promesse' => $promesse,
            'hors_cible' => $horsCible,
            'travaux' => $travaux,
            'lieu' => $lieu,
            'delai' => $d['delai'] !== '' ? Champs::DELAI[$d['delai']] : '',
            'nb_fichiers' => count($demande['fichiers']) ?: '',
            'message_extrait' => $extrait,
            'telephone' => $d['telephone']['affiche'] ?? '',
            'creneau' => in_array($d['creneau'], ['matin', 'apres-midi'], true) ? Champs::CRENEAU[$d['creneau']] : '',
            'realisation_url' => (string) ($realisations[$d['service']] ?? ''),
            'tel_fixe' => (string) ($e['tel_fixe'] ?? ''),
            'horaires' => (string) ($e['horaires'] ?? ''),
            'url_confidentialite' => (string) $this->config->get('url_confidentialite'),
            'signature' => $this->signature($associe['nom']),
            'aimant_titre' => (string) ($aimant['titre'] ?? ''),
            'aimant_url' => (string) ($aimant['url'] ?? ''),
            'aimant_format' => (string) ($aimant['format'] ?? ''),
            'aimant_lecture' => (string) ($aimant['lecture'] ?? ''),
            'par_poste' => $d['par_poste'],
            'newsletter' => $d['newsletter'],
            'url_desinscription' => (string) ($demande['url_desinscription'] ?? ''),
        ];
    }

    public static function salutation(string $civilite, string $nom, string $prenom): string
    {
        if ($civilite !== '' && $nom !== '') {
            return 'Bonjour ' . Champs::CIVILITE[$civilite] . ' ' . $nom;
        }
        if ($nom !== '') {
            return 'Bonjour ' . trim($prenom . ' ' . $nom);
        }
        return $prenom !== '' ? 'Bonjour ' . $prenom : 'Bonjour';
    }

    private function signature(string $associe): string
    {
        $e = (array) $this->config->get('entreprise');
        $lignes = [];
        if ($associe !== '') {
            $lignes[] = $associe;
        }
        $lignes[] = ($e['nom'] ?? 'Andy Construct') . ' · ' . ($e['adresse'] ?? '');
        $lignes[] = ($e['tel_fixe'] ?? '') . ' · ' . ($e['site'] ?? '');
        return implode("\n", $lignes);
    }

    // ------------------------------------------------------- notification interne

    /**
     * @param array<string, mixed> $demande
     * @param array<string, string> $actions libellé => URL (liens en un clic vers n8n)
     * @param list<array{nom: string, taille: int, joint: bool, url: string}> $fichiers
     */
    public function interne(array $demande, array $actions, array $fichiers): Message
    {
        $d = $demande['d'];
        $s = $demande['scoring'];
        $test = $this->config->modeTest() ? '[TEST] ' : '';
        $tel = $d['telephone'];
        $nomComplet = trim($d['prenom'] . ' ' . $d['nom']) ?: 'nom non indiqué';
        $lieu = trim(($d['npa'] !== '' && !str_contains($d['commune'], $d['npa']) ? $d['npa'] . ' ' : '') . $d['commune']);
        $loc = $demande['localite'];

        if ($demande['formulaire'] === 'aimant') {
            $titreAimant = (string) $this->config->get('aimants.' . $d['aimant'] . '.titre', $d['aimant']);
            $sujet = $test . '[Aimant] ' . $titreAimant . ' · ' . Champs::libelle(Champs::PROFIL, $d['profil']) . ' · ' . $nomComplet;
            $entete = 'Téléchargement d\'un guide' . ($d['par_poste'] ? ' · ENVOI POSTAL À FAIRE' : '');
        } else {
            $p = $s['priorite'];
            $etiquette = $p === 'hors-cible' ? 'Hors cible' : $p;
            $type = $demande['formulaire'] === 'rappel' ? 'Demande de rappel' : 'Nouvelle demande';
            $quoi = $d['service'] !== '' ? Champs::libelle(Champs::TRAVAUX + ['plusieurs' => 'Plusieurs prestations'], $d['service']) : ($tel['affiche'] ?? '');
            $sujet = $test . "[$etiquette] $type · $quoi · " . ($lieu ?: 'lieu non indiqué') . " · $nomComplet";
            $entete = "Priorité $etiquette · score {$s['score']}"
                . ($demande['echeance'] ? ' · à contacter avant ' . HeuresOuvrables::dateLongue($demande['echeance']) : '');
        }

        // Lignes du récapitulatif (libellé => valeur)
        $champs = [
            'Nom' => ($d['civilite'] ? Champs::CIVILITE[$d['civilite']] . ' ' : '') . $nomComplet,
            'Téléphone' => $tel ? $tel['affiche'] . ($tel['mobile'] ? ' (mobile)' : '') . ($tel['suisse'] ? '' : ' (étranger)') : '',
            'E-mail' => $d['email'],
            'Vous êtes' => $d['type_client'] !== '' ? Champs::TYPE_CLIENT[$d['type_client']] : ($d['profil'] !== '' ? Champs::PROFIL[$d['profil']] : ''),
            'Travaux' => implode(', ', array_map(static fn ($t) => Champs::TRAVAUX[$t], $d['travaux'])),
            'Surface' => $d['surface'] !== '' ? Champs::SURFACE[$d['surface']] : '',
            'Délai' => $d['delai'] !== '' ? Champs::DELAI[$d['delai']] : '',
            'Lieu' => $lieu !== '' ? $lieu . ' (' . implode(', ', array_filter([
                $loc['canton'] ? 'canton ' . $loc['canton'] : '',
                'zone ' . $loc['zone'],
                $loc['methode'] === 'commune-approchee' ? 'commune reconnue : ' . $loc['commune_reconnue'] . ', à vérifier' : '',
            ])) . ')' : '',
            'Préférence' => trim(Champs::libelle(Champs::PREFERENCE_CONTACT, $d['preference_contact'], '') . ($d['creneau'] ? ', ' . Champs::CRENEAU[$d['creneau']] : ''), ', '),
            'Recommandé par' => $d['recommande_par'],
            'Connu par (déclaré)' => $d['connu_par'] !== '' ? Champs::CONNU_PAR[$d['connu_par']] : '',
            'Guide' => $demande['formulaire'] === 'aimant' ? (string) $this->config->get('aimants.' . $d['aimant'] . '.titre', $d['aimant']) : '',
            'Envoi postal' => $d['par_poste'] ? "oui, à l'adresse : " . str_replace("\n", ', ', $d['adresse_postale']) : '',
            'Lettre trimestrielle' => $d['newsletter'] ? 'demandée (double confirmation à venir)' : '',
        ];
        $champs = array_filter($champs, static fn ($v) => $v !== '');

        $src = $demande['source'];
        $utm = array_filter($d['utm']);
        $sourceTexte = $src['libelle']
            . ($utm ? ' · ' . implode(' · ', array_map(static fn ($k, $v) => str_replace('utm_', '', $k) . ' : ' . $v, array_keys($utm), $utm)) : '')
            . ($d['page_entree'] ? ' · page d\'entrée ' . $d['page_entree'] : '')
            . ($d['page'] ? ' · formulaire envoyé depuis ' . $d['page'] : '')
            . ($d['source'] ? ' · emplacement ' . $d['source'] : '');

        // ---------- texte
        $t = [];
        $t[] = $entete;
        $t[] = 'Réf. ' . $demande['ref'] . ' · reçue le ' . HeuresOuvrables::dateLongue($demande['recu_le']) . ' · formulaire ' . $demande['formulaire'] . ($demande['canal'] === 'telephone' ? ' (saisie téléphonique)' : '');
        $t[] = '';
        if ($tel) {
            $t[] = 'APPELER : ' . $tel['affiche'] . ' (tel:' . $tel['e164'] . ')';
        }
        if ($d['email'] !== '') {
            $t[] = 'Écrire : ' . $d['email'] . ' (« Répondre » écrit directement à la personne)';
        }
        $t[] = '';
        foreach ($champs as $libelle => $valeur) {
            $t[] = "- $libelle : $valeur";
        }
        if ($d['message'] !== '') {
            $t[] = '';
            $t[] = 'Message :';
            $t[] = $d['message'];
        }
        if ($fichiers) {
            $t[] = '';
            $t[] = 'Fichiers (' . count($fichiers) . ') :';
            foreach ($fichiers as $f) {
                $t[] = '- ' . $f['nom'] . ' (' . self::taille($f['taille']) . ')' . ($f['joint'] ? ' : en pièce jointe' : ' : ' . $f['url']);
            }
        }
        if ($s) {
            $t[] = '';
            $t[] = 'Score détaillé (' . $s['score'] . ' points) :';
            foreach ($s['detail'] as $ligne) {
                $t[] = '- ' . (self::CRITERES[$ligne['critere']] ?? $ligne['critere']) . ' (' . $ligne['valeur'] . ') : ' . ($ligne['points'] > 0 ? '+' : '') . $ligne['points'];
            }
            foreach ($s['regles'] as $r) {
                $t[] = '- Règle appliquée : ' . $r;
            }
            foreach ($s['hors_cible'] as $r) {
                $t[] = '- Hors cible : ' . $r . ' (réponse de réorientation à valider par un associé)';
            }
        }
        $t[] = '';
        $t[] = 'Source : ' . $sourceTexte;
        if ($actions) {
            $t[] = '';
            $t[] = 'Actions en un clic :';
            foreach ($actions as $libelle => $url) {
                $t[] = "- $libelle : $url";
            }
        }
        $t[] = '';
        $t[] = 'Accusé de réception : ' . ($d['email'] !== '' ? 'envoyé à ' . $d['email'] : 'aucun (pas d\'e-mail fourni)');
        $t[] = 'Attribuée à : ' . ($demande['associe']['nom'] ?: 'à attribuer') . ' (rôle ' . $demande['associe']['role'] . ')';
        $t[] = 'Contrôle anti-robot : jeton ' . $demande['jeton']['statut'] . ($demande['jeton']['delai'] !== null ? ', formulaire rempli en ' . $demande['jeton']['delai'] . ' s' : '');
        $texte = implode("\n", $t) . "\n";

        // ---------- HTML
        $h = static fn (string $v): string => htmlspecialchars($v, ENT_QUOTES | ENT_HTML5, 'UTF-8');
        $couleur = self::COULEURS[$s['priorite'] ?? ''] ?? '#1D1F22';
        $html = '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head>'
            . '<body style="margin:0;background:#F4F5F6"><div style="max-width:640px;margin:0 auto;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:1.5;color:#1D1F22;background:#FFFFFF">'
            . '<div style="background:' . $couleur . ';color:#FFFFFF;padding:16px 20px;font-size:19px;font-weight:bold">' . $h($entete) . '</div>'
            . '<div style="padding:16px 20px">'
            . '<p style="margin:0 0 16px;color:#44494F;font-size:14px">Réf. <strong>' . $h($demande['ref']) . '</strong> · reçue le ' . $h(HeuresOuvrables::dateLongue($demande['recu_le'])) . ' · formulaire ' . $h($demande['formulaire']) . '</p>';
        if ($tel) {
            $html .= '<p style="margin:0 0 12px"><a href="tel:' . $h($tel['e164']) . '" style="display:inline-block;background:#1D1F22;color:#FFFFFF;text-decoration:none;font-weight:bold;font-size:20px;padding:14px 22px;border-radius:4px">Appeler le ' . $h($tel['affiche']) . '</a></p>';
        }
        if ($d['email'] !== '') {
            $html .= '<p style="margin:0 0 16px">E-mail : <a href="mailto:' . $h($d['email']) . '" style="color:#1D1F22">' . $h($d['email']) . '</a> <span style="color:#44494F;font-size:14px">(« Répondre » écrit directement à la personne)</span></p>';
        }
        $html .= '<table role="presentation" style="border-collapse:collapse;width:100%;margin:0 0 16px">';
        foreach ($champs as $libelle => $valeur) {
            $html .= '<tr><td style="padding:6px 8px 6px 0;color:#44494F;vertical-align:top;width:38%;border-bottom:1px solid #E6E7E9">' . $h($libelle) . '</td><td style="padding:6px 0;vertical-align:top;border-bottom:1px solid #E6E7E9"><strong>' . $h($valeur) . '</strong></td></tr>';
        }
        $html .= '</table>';
        if ($d['message'] !== '') {
            $html .= '<p style="margin:0 0 4px;color:#44494F">Message :</p><div style="white-space:pre-wrap;background:#F4F5F6;border-left:4px solid ' . $couleur . ';padding:12px;margin:0 0 16px">' . $h($d['message']) . '</div>';
        }
        if ($fichiers) {
            $html .= '<p style="margin:0 0 4px;color:#44494F">Fichiers :</p><ul style="margin:0 0 16px;padding-left:20px">';
            foreach ($fichiers as $f) {
                $html .= '<li>' . $h($f['nom']) . ' (' . $h(self::taille($f['taille'])) . ')'
                    . ($f['joint'] ? ' : en pièce jointe' : ' : <a href="' . $h($f['url']) . '" style="color:#1D1F22">télécharger</a> (lien valable 7 jours)') . '</li>';
            }
            $html .= '</ul>';
        }
        if ($actions) {
            $html .= '<p style="margin:16px 0 8px;font-weight:bold">Actions en un clic</p><p style="margin:0 0 16px">';
            foreach ($actions as $libelle => $url) {
                $html .= '<a href="' . $h($url) . '" style="display:inline-block;margin:0 8px 8px 0;padding:10px 14px;border:2px solid #1D1F22;border-radius:4px;color:#1D1F22;text-decoration:none;font-weight:bold">' . $h($libelle) . '</a>';
            }
            $html .= '</p>';
        }
        if ($s) {
            $html .= '<details open><summary style="cursor:pointer;color:#44494F">Score détaillé : ' . (int) $s['score'] . ' points</summary><table role="presentation" style="border-collapse:collapse;margin:8px 0 16px;font-size:14px">';
            foreach ($s['detail'] as $ligne) {
                $html .= '<tr><td style="padding:3px 12px 3px 0">' . $h(self::CRITERES[$ligne['critere']] ?? $ligne['critere']) . '</td><td style="padding:3px 12px 3px 0;color:#44494F">' . $h($ligne['valeur']) . '</td><td style="padding:3px 0;text-align:right">' . ($ligne['points'] > 0 ? '+' : '') . (int) $ligne['points'] . '</td></tr>';
            }
            $html .= '</table>';
            foreach (array_merge($s['regles'], array_map(static fn ($r) => 'Hors cible : ' . $r . ' (réponse de réorientation à valider)', $s['hors_cible'])) as $r) {
                $html .= '<p style="margin:0 0 4px;font-size:14px">Règle : ' . $h($r) . '</p>';
            }
            $html .= '</details>';
        }
        $html .= '<p style="margin:16px 0 4px;font-size:14px;color:#44494F">Source : ' . $h($sourceTexte) . '</p>'
            . '<p style="margin:0 0 4px;font-size:14px;color:#44494F">Accusé de réception : ' . $h($d['email'] !== '' ? 'envoyé à ' . $d['email'] : "aucun (pas d'e-mail fourni)") . '</p>'
            . '<p style="margin:0 0 4px;font-size:14px;color:#44494F">Attribuée à : ' . $h(($demande['associe']['nom'] ?: 'à attribuer') . ' (rôle ' . $demande['associe']['role'] . ')') . '</p>'
            . '<p style="margin:0;font-size:14px;color:#44494F">Contrôle anti-robot : jeton ' . $h($demande['jeton']['statut']) . ($demande['jeton']['delai'] !== null ? ', rempli en ' . (int) $demande['jeton']['delai'] . ' s' : '') . '</p>'
            . '</div></div></body></html>';

        $m = new Message();
        $m->categorie = 'interne-' . $demande['formulaire'];
        $m->ref = $demande['ref'];
        $m->sujet = $sujet;
        $m->texte = $texte;
        $m->html = $html;
        foreach ((array) $this->config->get('destinataires_internes', []) as $adresse) {
            if (Validateur::normaliserEmail((string) $adresse) !== null) {
                $m->a[] = [(string) $adresse, ''];
            }
        }
        if ($d['email'] !== '') {
            $m->repondreA = [$d['email'], $nomComplet];
        }
        return $m;
    }

    public function alerte(string $sujet, string $texte): Message
    {
        $m = new Message();
        $m->categorie = 'alerte';
        $m->sujet = ($this->config->modeTest() ? '[TEST] ' : '') . '[Site Andy Construct] ' . $sujet;
        $m->texte = $texte;
        foreach (array_filter([(string) $this->config->get('alerte_email', '')]) as $adresse) {
            if (Validateur::normaliserEmail($adresse) !== null) {
                $m->a[] = [$adresse, ''];
            }
        }
        return $m;
    }

    public static function taille(int $octets): string
    {
        return $octets >= 1048576
            ? number_format($octets / 1048576, 1, ',', "'") . ' Mo'
            : max(1, (int) round($octets / 1024)) . ' Ko';
    }
}
