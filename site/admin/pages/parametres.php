<?php
/** E12 · Paramètres : utilisateurs et rôles, dépenses mensuelles par canal, objectifs et économie. */
declare(strict_types=1);

use AndyConstruct\Admin\App;
use AndyConstruct\Admin\Auth;
use AndyConstruct\Admin\Format;
use AndyConstruct\Admin\Http;
use AndyConstruct\Admin\Indicateurs;
use AndyConstruct\Admin\Totp;
use AndyConstruct\Admin\Vue;
use AndyConstruct\Api\Base;
use AndyConstruct\Api\Canaux;

return static function (App $app): string {
    $e = static fn ($v) => Vue::e($v);
    $u = $app->utilisateur;
    $onglets = [];
    if (Auth::peut($u, 'utilisateurs')) {
        $onglets['utilisateurs'] = 'Utilisateurs et rôles';
    }
    $onglets['depenses'] = 'Dépenses';
    if (Auth::peut($u, 'parametres')) {
        $onglets['objectifs'] = 'Objectifs et économie';
    }
    $onglet = Http::get('onglet', array_key_first($onglets));
    if (!isset($onglets[$onglet])) {
        Http::refuser(403, 'Accès refusé', 'Votre rôle ne donne pas accès à ce réglage.');
    }
    $ici = Vue::url('parametres', ['onglet' => $onglet]);
    $resultat = '';
    $courant = Indicateurs::moisDe($app->maintenant);
    $listeMois = array_map(static fn ($i) => Indicateurs::moisDecale($courant, -$i), range(0, 5));
    $canauxDepense = ['google_ads', 'meta', 'linkedin', 'b2b', 'guides', 'annuaires', 'panneaux', 'recommandation'];

    if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
        try {
            $op = Http::post('op');
            if ($onglet === 'utilisateurs') {
                $id = (int) Http::post('id');
                if ($op === 'creer') {
                    $r = $app->auth->creerUtilisateur(Http::post('email'), Http::post('nom'), Http::post('role'), Http::post('role_metier') ?: null, Http::post('mot_de_passe'));
                    $resultat = secretUnique($app, Http::post('email'), $r['secret'], $r['codes'], 'Compte créé. Transmettez le mot de passe de vive voix ; la personne le change dans « Mon compte ».');
                } elseif ($op === 'actif' && $id !== $u['id']) {
                    $actif = Http::post('actif') === '1' ? 1 : 0;
                    $app->base->maj('utilisateur', ['actif' => $actif], 'id = ?', [$id]);
                    $app->audit($actif ? 'utilisateur_reactive' : 'utilisateur_desactive', 'utilisateur', (string) $id);
                    Vue::flash($actif ? 'Compte réactivé.' : 'Compte désactivé : ses sessions sont fermées.');
                    Http::rediriger($ici);
                } elseif ($op === '2fa' && $id > 0) {
                    $cible = $app->base->un('SELECT email FROM utilisateur WHERE id = ?', [$id]);
                    $r = $app->auth->reinitialiser2fa($id);
                    $resultat = secretUnique($app, (string) ($cible['email'] ?? ''), $r['secret'], $r['codes'], 'Double authentification réinitialisée.');
                } elseif ($op === 'mdp' && $id > 0 && $id !== $u['id']) {
                    $nouveau = Http::post('mot_de_passe');
                    if (($m = Auth::motDePasseRefuse($nouveau)) !== null) {
                        throw new \DomainException($m);
                    }
                    $app->base->maj('utilisateur', ['mdp_hash' => Auth::hacher($nouveau), 'mdp_change_le' => Base::maintenant(), 'echecs' => 0, 'bloque_jusqu_au' => null], 'id = ?', [$id]);
                    $app->audit('mot_de_passe_reinitialise', 'utilisateur', (string) $id);
                    Vue::flash('Mot de passe remplacé. Transmettez-le de vive voix.');
                    Http::rediriger($ici);
                } else {
                    throw new \DomainException('Action impossible (vous ne pouvez pas désactiver votre propre compte).');
                }
            } elseif ($onglet === 'depenses') {
                $saisies = (array) ($_POST['dep'] ?? []);
                $n = 0;
                foreach ($listeMois as $m) {
                    foreach ($canauxDepense as $c) {
                        $brut = $saisies[$m][$c] ?? null;
                        if (!is_string($brut)) {
                            continue;
                        }
                        $brut = trim($brut);
                        $existant = $app->base->un("SELECT id, montant_ht FROM depense WHERE mois = ? AND canal_marketing = ? AND type_cout = 'media' AND origine = 'saisie'", [$m . '-01', $c]);
                        if ($brut === '') {
                            if ($existant) {
                                $app->base->executer('DELETE FROM depense WHERE id = ?', [$existant['id']]);
                                $n++;
                            }
                            continue;
                        }
                        $montant = Format::lireMontant($brut);
                        if ($montant === null) {
                            throw new \DomainException('Montant illisible pour ' . Canaux::libelle($c) . ', ' . Format::mois($m) . ' : « ' . mb_substr($brut, 0, 20) . ' ».');
                        }
                        if ($existant === null) {
                            $app->base->inserer('depense', ['mois' => $m . '-01', 'canal_marketing' => $c, 'montant_ht' => $montant, 'type_cout' => 'media', 'origine' => 'saisie', 'saisi_par' => $u['id'], 'saisi_le' => Base::maintenant()]);
                            $n++;
                        } elseif (abs((float) $existant['montant_ht'] - $montant) > 0.001) {
                            $app->base->maj('depense', ['montant_ht' => $montant, 'saisi_par' => $u['id'], 'saisi_le' => Base::maintenant()], 'id = ?', [$existant['id']]);
                            $n++;
                        }
                    }
                }
                $app->audit('depenses', 'depense', null, ['modifications' => $n]);
                Vue::flash($n ? "Dépenses enregistrées ($n modification" . ($n > 1 ? 's' : '') . ').' : 'Aucune modification.');
                Http::rediriger($ici);
            } elseif ($onglet === 'objectifs') {
                $marge = Format::lireMontant(Http::post('marge_brute'));
                $panier = Format::lireMontant(Http::post('panier_reference'));
                $miseEnLigne = Http::post('mise_en_ligne');
                if ($marge === null || $marge <= 0 || $marge >= 100 || $panier === null || $panier <= 0) {
                    throw new \DomainException('Indiquez une marge brute entre 1 et 99 % et un panier de référence en CHF.');
                }
                if ($miseEnLigne !== '' && !preg_match('/^\d{4}-(0[1-9]|1[0-2])$/', $miseEnLigne)) {
                    throw new \DomainException('Mois de mise en ligne au format AAAA-MM.');
                }
                $objectifs = (array) $app->parametre('objectifs');
                foreach (App::PARAMETRES_DEFAUT['objectifs'] as $cle => $_) {
                    foreach ([3, 6, 12] as $j) {
                        $v = Format::lireMontant(Http::post("obj_{$cle}_$j"));
                        if ($v === null) {
                            throw new \DomainException('Objectif illisible : ' . $cle . ' M' . $j . '.');
                        }
                        $objectifs[$cle][$j] = $v;
                    }
                }
                $app->definirParametre('marge_brute', $marge / 100);
                $app->definirParametre('panier_reference', $panier);
                $app->definirParametre('mise_en_ligne', $miseEnLigne);
                $app->definirParametre('objectifs', $objectifs);
                $app->audit('parametres', 'parametre', null, ['cles' => ['marge_brute', 'panier_reference', 'mise_en_ligne', 'objectifs']]);
                Vue::flash('Objectifs et économie enregistrés.');
                Http::rediriger($ici);
            }
        } catch (\DomainException $ex) {
            $resultat = '<p class="erreur-formulaire" role="alert">' . $e($ex->getMessage()) . '</p>';
        }
    }

    $nav = '<nav class="onglets" aria-label="Paramètres">';
    foreach ($onglets as $k => $lib) {
        $nav .= '<a href="' . $e(Vue::url('parametres', ['onglet' => $k])) . '"' . ($k === $onglet ? ' aria-current="page"' : '') . '>' . $e($lib) . '</a>';
    }
    $nav .= '</nav>';

    if ($onglet === 'utilisateurs') {
        $lignes = '';
        foreach ($app->base->tous('SELECT * FROM utilisateur ORDER BY actif DESC, nom_affiche') as $x) {
            $id = (int) $x['id'];
            $form = static fn (string $op, string $lib, string $extra = '') => '<form method="post" action="' . $e($ici) . '" class="en-ligne">' . Vue::csrf($app) . '<input type="hidden" name="op" value="' . $op . '"><input type="hidden" name="id" value="' . $id . '">' . $extra . '<button class="btn btn-petit btn-discret" type="submit">' . $e($lib) . '<span class="sr"> (' . $e($x['nom_affiche']) . ')</span></button></form>';
            $actions = $id === $u['id'] ? '<span class="petit discret">vous</span>' : $form('actif', $x['actif'] ? 'Désactiver' : 'Réactiver', '<input type="hidden" name="actif" value="' . ($x['actif'] ? '0' : '1') . '">')
                . $form('2fa', 'Réinitialiser la 2FA')
                . '<details class="transition"><summary>Nouveau mot de passe<span class="sr"> (' . $e($x['nom_affiche']) . ')</span></summary><form method="post" action="' . $e($ici) . '" class="formulaire-transition">' . Vue::csrf($app) . '<input type="hidden" name="op" value="mdp"><input type="hidden" name="id" value="' . $id . '">'
                . '<label class="champ" for="mdp-' . $id . '"><span>Mot de passe (12 caractères au moins)</span><input id="mdp-' . $id . '" name="mot_de_passe" type="password" autocomplete="new-password" required minlength="12"></label><button class="btn btn-petit btn-sombre" type="submit">Remplacer</button></form></details>';
            $lignes .= '<tr' . ($x['actif'] ? '' : ' class="inactif"') . '><th scope="row">' . $e($x['nom_affiche']) . '<span class="org">' . $e($x['email']) . '</span></th><td>' . $e(Auth::ROLES[$x['role']] ?? $x['role']) . ($x['role_metier'] ? '<span class="org">' . $e($x['role_metier']) . '</span>' : '') . '</td>'
                . '<td>' . ($x['actif'] ? 'Actif' : 'Désactivé') . ($x['bloque_jusqu_au'] && $x['bloque_jusqu_au'] > Base::maintenant() ? ' <span class="etiquette">bloqué</span>' : '') . '</td><td>' . $e(Format::dateH(Format::t($x['derniere_connexion_le']))) . '</td><td><div class="groupe-btn">' . $actions . '</div></td></tr>';
        }
        $roles = '';
        foreach (Auth::ROLES as $k => $l) {
            $roles .= '<option value="' . $k . '">' . $e($l) . '</option>';
        }
        $corps = '<section class="panneau" aria-labelledby="t-u"><h2 id="t-u">Comptes</h2><div class="defile" tabindex="0" role="region" aria-label="Tableau, défile horizontalement"><table class="tableau"><caption class="sr">Utilisateurs</caption><thead><tr><th scope="col">Nom</th><th scope="col">Rôle</th><th scope="col">État</th><th scope="col">Dernière connexion</th><th scope="col">Actions</th></tr></thead><tbody>' . $lignes . '</tbody></table></div></section>'
            . '<section class="panneau mt" aria-labelledby="t-nu"><h2 id="t-nu">Créer un compte</h2><form method="post" action="' . $e($ici) . '" class="formulaire grille-form">' . Vue::csrf($app) . '<input type="hidden" name="op" value="creer">'
            . '<label class="champ" for="nu-nom"><span>Nom affiché</span><input id="nu-nom" name="nom" required maxlength="100" autocomplete="off"></label>'
            . '<label class="champ" for="nu-email"><span>E-mail</span><input id="nu-email" name="email" type="email" required autocomplete="off"></label>'
            . '<label class="champ" for="nu-role"><span>Rôle</span><select id="nu-role" name="role">' . $roles . '</select></label>'
            . '<label class="champ" for="nu-rm"><span>Rôle métier (associés)</span><select id="nu-rm" name="role_metier"><option value="">—</option><option value="bureau">Bureau (B2B)</option><option value="terrain">Terrain (particuliers)</option></select></label>'
            . '<label class="champ" for="nu-mdp"><span>Mot de passe provisoire (12 caractères au moins)</span><input id="nu-mdp" name="mot_de_passe" type="password" required minlength="12" autocomplete="new-password"></label>'
            . '<div><button class="btn btn-sombre" type="submit">Créer le compte</button></div></form>'
            . '<p class="petit discret">Le rôle « Agence, marketing » ne voit aucune donnée personnelle (indicateurs, acquisition, dépenses). La double authentification est obligatoire pour tous.</p></section>';
    } elseif ($onglet === 'depenses') {
        $tete = '';
        foreach ($listeMois as $m) {
            $tete .= '<th scope="col" class="num">' . $e(ucfirst(Format::mois($m))) . '</th>';
        }
        $valeurs = [];
        foreach ($app->base->tous("SELECT mois, canal_marketing, montant_ht FROM depense WHERE type_cout = 'media' AND origine = 'saisie'") as $r) {
            $valeurs[substr((string) $r['mois'], 0, 7)][$r['canal_marketing']] = (float) $r['montant_ht'];
        }
        $lignes = '';
        foreach ($canauxDepense as $c) {
            $lignes .= '<tr><th scope="row">' . $e(Canaux::libelle($c)) . '</th>';
            foreach ($listeMois as $m) {
                $v = $valeurs[$m][$c] ?? null;
                $lignes .= '<td class="num"><label class="sr" for="dep-' . $m . '-' . $c . '">' . $e(Canaux::libelle($c) . ', ' . Format::mois($m)) . '</label><input class="montant" id="dep-' . $m . '-' . $c . '" name="dep[' . $m . '][' . $c . ']" inputmode="decimal" autocomplete="off" value="' . ($v === null ? '' : $e(Format::nb($v))) . '"></td>';
            }
            $lignes .= '</tr>';
        }
        $corps = '<section class="panneau" aria-labelledby="t-dep"><div class="panneau-entete"><h2 id="t-dep">Dépenses mensuelles par canal</h2><span class="discret">CHF hors TVA ; médias, courrier et impression (sans les honoraires d\'agence, décision G5)</span></div>'
            . '<form method="post" action="' . $e($ici) . '">' . Vue::csrf($app) . '<div class="defile" tabindex="0" role="region" aria-label="Tableau, défile horizontalement"><table class="tableau compact grille-depenses"><caption class="sr">Dépenses par canal et par mois</caption><thead><tr><th scope="col">Canal</th>' . $tete . '</tr></thead><tbody>' . $lignes . '</tbody></table></div>'
            . '<p class="mt"><button class="btn btn-sombre" type="submit">Enregistrer les dépenses</button> <span class="petit discret">Case vide : aucune dépense. Google Ads : montant facturé du mois (import automatique en V2).</span></p></form></section>';
    } else {
        $obj = (array) $app->parametre('objectifs');
        $libelles = ['demandes' => 'Demandes/mois', 'part_ab' => 'Part A+B (%)', 'delai_a_h' => 'Délai de premier contact A (heures ouvrables)', 'demande_offre' => 'Taux demande→offre (%)', 'offre_signee' => 'Taux offre→signée (%)', 'chantiers' => 'Chantiers signés par mois'];
        $lignes = '';
        foreach ($libelles as $k => $lib) {
            $lignes .= '<tr><th scope="row">' . $e($lib) . '</th>';
            foreach ([3, 6, 12] as $j) {
                $v = $obj[$k][$j] ?? App::PARAMETRES_DEFAUT['objectifs'][$k][$j];
                $lignes .= '<td class="num"><label class="sr" for="obj-' . $k . '-' . $j . '">' . $e($lib . ', M' . $j) . '</label><input class="montant" id="obj-' . $k . '-' . $j . '" name="obj_' . $k . '_' . $j . '" inputmode="decimal" value="' . $e(Format::nb((float) $v, fmod((float) $v, 1.0) ? 1 : 0)) . '"></td>';
            }
            $lignes .= '</tr>';
        }
        $ind = new Indicateurs($app);
        $corps = '<form method="post" action="' . $e($ici) . '">' . Vue::csrf($app) . '<div class="grille-2"><section class="panneau formulaire" aria-labelledby="t-eco"><h2 id="t-eco">Économie (décision G4)</h2>'
            . '<label class="champ" for="p-marge"><span>Taux de marge brute (%)</span><input id="p-marge" name="marge_brute" inputmode="decimal" required value="' . $e(Format::nb((float) $app->parametre('marge_brute') * 100, 1)) . '"></label>'
            . '<label class="champ" for="p-panier"><span>Panier de référence (CHF HT)</span><input id="p-panier" name="panier_reference" inputmode="decimal" required value="' . $e(Format::nb((float) $app->parametre('panier_reference'))) . '"></label>'
            . '<label class="champ" for="p-mel"><span>Mois de mise en ligne (M1)</span><input id="p-mel" name="mise_en_ligne" placeholder="AAAA-MM" pattern="\d{4}-\d{2}" value="' . $e((string) $app->parametre('mise_en_ligne')) . '"><span class="aide-champ">' . $e('Vide : mois de la première demande (' . $ind->moisMiseEnLigne() . '). Ce mois est M' . $ind->numeroMois($courant) . '.') . '</span></label>'
            . '<p class="petit discret">Valeurs illustratives tant que le client ne les a pas données (plan §7.4, G4). Elles servent au CPL max, au ROI et à l\'objectif de CA.</p></section>'
            . '<section class="panneau" aria-labelledby="t-obj"><h2 id="t-obj">Objectifs (jalons M3, M6, M12)</h2><div class="defile" tabindex="0" role="region" aria-label="Objectifs, défile horizontalement"><table class="tableau compact"><caption class="sr">Objectifs</caption><thead><tr><th scope="col">Indicateur</th><th scope="col" class="num">M3</th><th scope="col" class="num">M6</th><th scope="col" class="num">M12</th></tr></thead><tbody>' . $lignes . '</tbody></table></div>'
            . '<p class="petit discret">Stratégie v2 §1.1, scénario M. Entre deux jalons : interpolation linéaire (décision G6). Avant M3 : pas d\'objectif affiché.</p></section></div>'
            . '<p class="mt"><button class="btn btn-sombre" type="submit">Enregistrer</button></p></form>';
    }
    return Vue::page($app, 'parametres', 'Paramètres', '<div class="entete-page"><div><h1>Paramètres</h1></div></div>' . $nav . $resultat . $corps);
};

/** Secret 2FA et codes de secours affichés une seule fois. */
function secretUnique(App $app, string $email, string $secret, array $codes, string $titre): string
{
    $e = static fn ($v) => Vue::e($v);
    return '<section class="panneau secret-unique" aria-labelledby="t-secret" role="status"><h2 id="t-secret">' . $e($titre) . '</h2>'
        . '<p>Dans l\'application d\'authentification (Google Authenticator, Microsoft Authenticator, 1Password…), ajoutez un compte avec cette clé :</p>'
        . '<p class="cle-secrete"><code>' . $e(trim(chunk_split($secret, 4, ' '))) . '</code></p>'
        . '<p class="petit">Ou collez l\'adresse : <code class="coupe">' . $e(Totp::uri($secret, $email)) . '</code></p>'
        . '<p>Codes de secours (un seul usage chacun, à garder hors du téléphone) :</p><ul class="codes-secours">' . implode('', array_map(static fn ($c) => '<li><code>' . $e($c) . '</code></li>', $codes)) . '</ul>'
        . '<p class="petit discret">Ces informations ne seront plus affichées. Fermez cette page une fois notées.</p></section>';
}
