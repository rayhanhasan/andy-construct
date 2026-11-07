<?php
/**
 * E6 · Saisie d'un appel (30 secondes) : passe par le même Traitement que le site
 * (même score, même échéance, mêmes notifications), canal « téléphone » par défaut.
 */
declare(strict_types=1);

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Demandes;
use AndyConstruct\Admin\Format;
use AndyConstruct\Admin\Http;
use AndyConstruct\Admin\Vue;
use AndyConstruct\Api\Champs;
use AndyConstruct\Api\Traitement;

return static function (App $app): string {
    $e = static fn ($v) => Vue::e($v);
    $valeurs = ['telephone' => '', 'nom' => '', 'commune' => '', 'travaux' => [], 'type_client' => '', 'surface' => '', 'delai' => '', 'connu_par' => '', 'note' => '', 'email' => '', 'confirmation' => '', 'canal' => 'telephone'];
    $erreurs = [];
    if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
        foreach ($valeurs as $k => $_) {
            $valeurs[$k] = $k === 'travaux' ? array_values(array_filter((array) ($_POST['travaux'] ?? []), 'is_string')) : mb_substr(Http::post($k), 0, $k === 'note' ? 3000 : 200);
        }
        if (!isset(Demandes::CANAUX_SAISIE[$valeurs['canal']])) {
            $valeurs['canal'] = 'telephone';
        }
        if (!isset(Champs::CONNU_PAR[$valeurs['connu_par']])) {
            $erreurs['connu_par'] = 'Demandez « Comment nous avez-vous connus ? » : c\'est l\'attribution des appels.';
        }
        [$npa, $commune] = preg_match('/^\s*([1-9]\d{3})\b\s*(.*)$/u', $valeurs['commune'], $m) ? [$m[1], trim($m[2])] : ['', trim($valeurs['commune'])];
        $post = [
            'formulaire' => 'devis', 'canal' => 'telephone', 'nom' => $valeurs['nom'], 'telephone' => $valeurs['telephone'], 'email' => $valeurs['email'],
            'travaux' => $valeurs['travaux'], 'type_client' => $valeurs['type_client'], 'surface' => $valeurs['surface'], 'delai' => $valeurs['delai'],
            'npa' => $npa, 'commune' => $commune, 'message' => $valeurs['note'], 'connu_par' => $valeurs['connu_par'],
            'preference_contact' => $valeurs['telephone'] !== '' ? 'appel' : 'email', 'envoyer_confirmation' => $valeurs['confirmation'] === 'oui' ? 'oui' : '',
            'source' => 'admin-saisie',
        ];
        if ($erreurs === []) {
            $traitement = (new Traitement($app->config, false))->pourSaisieAdmin(['auteur_id' => (int) $app->utilisateur['id'], 'canal' => $valeurs['canal']]);
            $r = $traitement->executer(['REQUEST_METHOD' => 'POST', 'HTTP_ACCEPT' => 'application/json', 'REMOTE_ADDR' => $app->ip()], [], $post, [], $app->maintenant);
            if ($r->statut === 200 && !empty($r->corps['ref'])) {
                $ref = (string) $r->corps['ref'];
                $d = $app->demandes->parRef($ref);
                if ($d === null) {
                    Vue::flash("Demande $ref enregistrée et notifiée. La base est momentanément indisponible : elle apparaîtra ici dans quelques minutes.", 'erreur');
                    Http::rediriger(Vue::url('a-traiter'));
                }
                if (Http::post('apres') === 'contact') {
                    try {
                        $app->demandes->agir($d['id'], 'contact_etabli', [], (int) $app->utilisateur['id']);
                    } catch (\DomainException $ex) {
                        Vue::flash($ex->getMessage(), 'erreur');
                    }
                }
                Vue::flash("Demande $ref enregistrée" . (Http::post('apres') === 'contact' ? ', contact établi.' : ' : elle apparaît dans À rappeler.'));
                Http::rediriger(Vue::url('fiche', ['ref' => $ref]));
            }
            $erreurs += (array) ($r->corps['erreurs'] ?? []);
            if ($erreurs === []) {
                $erreurs['general'] = (string) ($r->corps['message'] ?? 'La demande n\'a pas pu être enregistrée.');
            }
        }
    }

    $err = static fn (string $champ) => isset($erreurs[$champ]) ? '<span class="erreur-champ" id="err-' . $champ . '">' . $e($erreurs[$champ]) . '</span>' : '';
    $inv = static fn (string $champ) => isset($erreurs[$champ]) ? ' aria-invalid="true" aria-describedby="err-' . $champ . '"' : '';
    $radios = static function (string $nom, array $opts, string $valeur) use ($e): string {
        $h = '<div class="choix">';
        foreach ($opts as $v => $l) {
            $h .= '<label><input type="radio" name="' . $nom . '" value="' . $e($v) . '"' . ($v === $valeur ? ' checked' : '') . '><span>' . $e($l) . '</span></label>';
        }
        return $h . '</div>';
    };
    $cases = '<div class="choix">';
    foreach (['placo' => 'Placo', 'peinture' => 'Peinture', 'isolation-acoustique' => 'Isolation acoustique', 'cloisons-isothermes' => 'Cloisons isolantes', 'ne-sait-pas' => 'À préciser', 'autre' => 'Autre'] as $v => $l) {
        $cases .= '<label><input type="checkbox" name="travaux[]" value="' . $v . '"' . (in_array($v, $valeurs['travaux'], true) ? ' checked' : '') . '><span>' . $e($l) . '</span></label>';
    }
    $cases .= '</div>';
    $connu = '<option value="">Choisir</option>';
    foreach (Champs::CONNU_PAR as $v => $l) {
        $connu .= '<option value="' . $v . '"' . ($v === $valeurs['connu_par'] ? ' selected' : '') . '>' . $e($l) . '</option>';
    }
    $canaux = '';
    foreach (Demandes::CANAUX_SAISIE as $v => $l) {
        $canaux .= '<option value="' . $v . '"' . ($v === $valeurs['canal'] ? ' selected' : '') . '>' . $e($l) . '</option>';
    }
    $general = isset($erreurs['general']) || ($erreurs && !array_intersect_key($erreurs, array_flip(['telephone', 'nom', 'commune', 'travaux', 'connu_par', 'email'])))
        ? '<p class="erreur-formulaire" role="alert">' . $e($erreurs['general'] ?? implode(' ', $erreurs)) . '</p>' : ($erreurs ? '<p class="erreur-formulaire" role="alert">Il manque une information : les champs concernés sont indiqués.</p>' : '');

    $html = '<div class="entete-page"><div><h1>Saisir un appel</h1><p class="sous-titre">30 secondes. Le score, la priorité et l\'échéance sont calculés comme pour le site.</p></div></div>'
        . '<form class="grille-2 aligne-haut" id="form-saisie" method="post" action="' . $e(Vue::url('saisie')) . '" novalidate data-brouillon="saisie" data-score="' . $e(Vue::url('score')) . '">' . Vue::csrf($app)
        . '<div class="panneau formulaire">' . $general
        . '<label class="champ" for="s-tel"><span>Téléphone</span><input id="s-tel" name="telephone" type="tel" inputmode="tel" autocomplete="off" placeholder="079 000 00 00" value="' . $e($valeurs['telephone']) . '"' . $inv('telephone') . '>'
        . '<span class="aide-champ" id="s-doublon" aria-live="polite">En premier : on retrouve un contact existant.</span>' . $err('telephone') . '</label>'
        . '<label class="champ" for="s-nom"><span>Nom et prénom</span><input id="s-nom" name="nom" autocomplete="off" value="' . $e($valeurs['nom']) . '"' . $inv('nom') . '>' . $err('nom') . '</label>'
        . '<label class="champ" for="s-commune"><span>Commune ou NPA</span><input id="s-commune" name="commune" autocomplete="off" placeholder="1227 Carouge" value="' . $e($valeurs['commune']) . '"' . $inv('commune') . '>' . $err('commune') . '</label>'
        . '<fieldset class="champ"' . (isset($erreurs['travaux']) ? ' aria-describedby="err-travaux"' : '') . '><legend>Travaux</legend>' . $cases . $err('travaux') . '</fieldset>'
        . '<fieldset class="champ"><legend>Type de client</legend>' . $radios('type_client', array_diff_key(Demandes::TYPES_CLIENT, ['autre' => 1]), $valeurs['type_client']) . '</fieldset>'
        . '<fieldset class="champ"><legend>Surface</legend>' . $radios('surface', ['moins-15' => '< 15 m²', '15-50' => '15-50 m²', '50-200' => '50-200 m²', 'plus-200' => '> 200 m²', 'ne-sait-pas' => 'Ne sait pas'], $valeurs['surface']) . '</fieldset>'
        . '<fieldset class="champ"><legend>Délai</legend>' . $radios('delai', ['moins-1-mois' => '< 1 mois', '1-3-mois' => '1-3 mois', '3-6-mois' => '3-6 mois', 'non-defini' => 'Pas défini'], $valeurs['delai']) . '</fieldset>'
        . '<label class="champ" for="s-connu"><span>Comment nous avez-vous connus ? <span class="aide-champ">obligatoire : c\'est l\'attribution des appels</span></span><select id="s-connu" name="connu_par" required' . $inv('connu_par') . '>' . $connu . '</select>' . $err('connu_par') . '</label>'
        . '<label class="champ" for="s-note"><span>Note</span><textarea id="s-note" name="note" maxlength="3000" placeholder="Ce que la personne a dit">' . $e($valeurs['note']) . '</textarea></label>'
        . '<label class="champ" for="s-email"><span>E-mail <span class="aide-champ">facultatif</span></span><input id="s-email" name="email" type="email" autocomplete="off" value="' . $e($valeurs['email']) . '"' . $inv('email') . '>' . $err('email') . '</label>'
        . '<label class="champ" for="s-canal"><span>Arrivée</span><select id="s-canal" name="canal">' . $canaux . '</select></label>'
        . '<label class="case" for="s-conf"><input id="s-conf" type="checkbox" name="confirmation" value="oui"' . ($valeurs['confirmation'] === 'oui' ? ' checked' : '') . '> Envoyer une confirmation écrite au client (si e-mail)</label>'
        . '<div class="groupe-btn"><button class="btn btn-principal" type="submit" name="apres" value="contact">Enregistrer, contact établi</button><button class="btn btn-discret" type="submit" name="apres" value="rappeler">Enregistrer seulement</button></div>'
        . '</div><aside class="panneau score-direct" aria-labelledby="t-score"><h2 id="t-score">Priorité calculée</h2><div id="s-score" aria-live="polite"><p class="petit discret">Le score s\'affiche pendant la saisie (même grille que le site, '
        . $e((string) ($app->grille['version'] ?? '')) . '). Pas de bonus « téléphone » pour une saisie : le numéro est toujours connu.</p></div></aside></form>';
    return Vue::page($app, 'saisie', 'Saisir un appel', $html);
};
