<?php
/**
 * Données de DÉMONSTRATION pour l'admin : comptes et demandes FICTIVES.
 *
 *   AC_API_CONFIG=/chemin/config-demo.php php site/admin/outils/demo.php --oui-base-de-demonstration [--vider]
 *
 * NE JAMAIS EXÉCUTER EN PRODUCTION. Le script refuse de tourner si config.php n'est pas
 * en mode test (« mode_test » => true) et sans l'option explicite. Noms manifestement
 * fictifs (Exemple, Fictif, Démo…), numéros 079 000 00 xx, adresses @exemple.test.
 * Les demandes passent par les mêmes classes que le site (Scoring, HeuresOuvrables,
 * Source, Depot) puis par les mêmes transitions que l'admin, datées dans le passé.
 */
declare(strict_types=1);

if (PHP_SAPI !== 'cli') {
    http_response_code(404);
    exit;
}
require dirname(__DIR__) . '/lib/bootstrap.php';
ini_set('display_errors', '1');

use AndyConstruct\Admin\App;
use AndyConstruct\Api\Base;
use AndyConstruct\Api\Config;
use AndyConstruct\Api\Depot;
use AndyConstruct\Api\Journal;
use AndyConstruct\Api\Localite;
use AndyConstruct\Api\Source;
use AndyConstruct\Api\Stockage;
use AndyConstruct\Api\Validateur;

$o = getopt('', ['oui-base-de-demonstration', 'vider', 'maintenant:']);
$config = Config::charger();
if (!isset($o['oui-base-de-demonstration']) || !$config->modeTest()) {
    fwrite(STDERR, "Refusé. Ce script remplit une base de DÉMONSTRATION avec des données fictives.\n"
        . "Il exige « mode_test » => true dans la configuration et l'option --oui-base-de-demonstration.\n"
        . "Ne jamais l'exécuter sur la base de production.\n");
    exit(2);
}

const DEMO_SECRETS = [
    'alex.modele@exemple.test' => 'ALEXMODELEDEMOTOTPAAAAAAAAAAAAAA',
    'camille.exemple@exemple.test' => 'CAMILLEEXEMPLEDEMOTOTPAAAAAAAAAA',
    'dominique.essai@exemple.test' => 'DOMINIQUEESSAIDEMOTOTPAAAAAAAAAA',
    'agence.fictive@exemple.test' => 'AGENCEFICTIVEDEMOTOTPAAAAAAAAAAA',
];
const DEMO_MDP = 'demo chantier fictif';

$maintenant = isset($o['maintenant']) ? new \DateTimeImmutable((string) $o['maintenant'], new \DateTimeZone('Europe/Zurich')) : new \DateTimeImmutable('now', new \DateTimeZone('Europe/Zurich'));
$app = new App($config, null, $maintenant);
$b = $app->base;

if (isset($o['vider'])) {
    foreach (['interaction', 'visite', 'offre', 'fichier', 'attribution', 'demande', 'contact', 'depense', 'parametre', 'journal_audit', 'tentative_connexion', 'utilisateur'] as $t) {
        $b->executer("DELETE FROM $t");
    }
}
if ((int) $b->valeur('SELECT COUNT(*) FROM demande') > 0) {
    fwrite(STDERR, "La base contient déjà des demandes. Relancez avec --vider pour repartir de zéro.\n");
    exit(1);
}

// ------------------------------------------------------------------ comptes
$comptes = [
    ['alex.modele@exemple.test', 'Alex Modèle', 'associe', 'terrain'],
    ['camille.exemple@exemple.test', 'Camille Exemple', 'associe', 'bureau'],
    ['dominique.essai@exemple.test', 'Dominique Essai', 'secretariat', null],
    ['agence.fictive@exemple.test', 'Agence Fictive', 'agence_marketing', null],
];
$ids = [];
foreach ($comptes as [$email, $nom, $role, $metier]) {
    $existant = $b->valeur('SELECT id FROM utilisateur WHERE email = ?', [$email]);
    $ids[$email] = $existant !== null ? (int) $existant : $app->auth->creerUtilisateur($email, $nom, $role, $metier, DEMO_MDP, DEMO_SECRETS[$email])['id'];
}
$alex = $ids['alex.modele@exemple.test'];
$camille = $ids['camille.exemple@exemple.test'];

// ------------------------------------------------------------- paramètres
$moisCourant = $maintenant->format('Y-m');
$app->definirParametre('mise_en_ligne', $maintenant->modify('first day of this month')->modify('-5 months')->format('Y-m'));
$app->definirParametre('marge_brute', 0.30);
$app->definirParametre('panier_reference', 9000);
for ($i = 0; $i <= 6; $i++) {
    $m = $maintenant->modify('first day of this month')->modify("-$i months")->format('Y-m');
    foreach (['google_ads' => 1200 - ($i * 40), 'meta' => $i % 2 ? 150 : 0, 'b2b' => 80] as $canal => $montant) {
        if ($montant > 0 && !($i === 0 && $canal === 'b2b')) {
            $b->inserer('depense', ['mois' => $m . '-01', 'canal_marketing' => $canal, 'montant_ht' => $i === 0 ? round($montant * (int) $maintenant->format('j') / 30) : $montant,
                'type_cout' => 'media', 'origine' => 'saisie', 'saisi_par' => $alex, 'saisi_le' => Base::maintenant()]);
        }
    }
}

// ------------------------------------------------------------- demandes
mt_srand(20270422);
$hasard = static fn (array $l) => $l[mt_rand(0, count($l) - 1)];
$chance = static fn (float $p): bool => mt_rand() / mt_getrandmax() < $p;
$prenoms = ['Léa', 'Marc', 'Sophie', 'Paul', 'Inès', 'Hugo', 'Chloé', 'Nicolas', 'Emma', 'Julien', 'Sarah', 'Louis', 'Anaïs', 'Thomas', 'Zoé', 'Victor', 'Manon', 'Adrien', 'Lucie', 'Samuel'];
$noms = ['Exemple', 'Fictif', 'Démo', 'Modèle', 'Essai', 'Bidon', 'Placebo', 'Fantôme', 'Imaginaire', 'Prototype', 'Maquette', 'Factice'];
$organisations = ['regie' => ['Régie Imaginaire SA', 'Gérance Fictive', 'Coopérative Exemple'], 'architecte' => ['Atelier Factice architectes', 'Bureau Prototype'], 'commune' => ['Commune de Démo-sur-Arve'], 'entreprise' => ['Boulangerie Exemple', 'Cabinet Fictif']];
$communes = [['1227', 'Carouge'], ['1222', 'Vésenaz'], ['1212', 'Grand-Lancy'], ['1213', 'Onex'], ['1217', 'Meyrin'], ['1205', 'Genève'], ['1226', 'Thônex'], ['1224', 'Chêne-Bougeries'], ['1260', 'Nyon'], ['1110', 'Morges'], ['1003', 'Lausanne'], ['1800', 'Vevey'], ['1290', 'Versoix'], ['1950', 'Sion']];
$messages = ['On entend tout le voisin du dessus, chambre d\'environ 14 m².', 'Repeindre un appartement de 4 pièces avant l\'entrée des locataires.', 'Créer une cloison pour faire une chambre d\'enfant.',
    'Fin de bail dans trois semaines : reprise des murs et plafonds.', 'Dégât d\'eau au plafond de la cuisine, besoin rapide.', 'Isoler une salle de réunion du bruit du couloir.', '', 'Devis pour cage d\'escalier, 5 étages.'];
$sources = [
    // [poids, utm_source, utm_medium, referent, connu_par, gclid]
    [24, 'google', 'cpc', 'www.google.ch', 'recherche-google', true],
    [18, '', '', 'www.google.ch', 'recherche-google', false],
    [10, '', '', '', 'carte-google', false],
    [8, 'facebook', 'paid-social', 'm.facebook.com', 'facebook', false],
    [12, '', '', '', 'recommandation', false],
    [6, 'courrier', 'print', '', 'regie-architecte', false],
    [8, '', '', '', '', false],
    [4, 'localch', 'referral', 'www.local.ch', 'autre', false],
];
$tirerSource = static function () use ($sources): array {
    $total = array_sum(array_column($sources, 0));
    $r = mt_rand(1, $total);
    foreach ($sources as $s) {
        if (($r -= $s[0]) <= 0) {
            return $s;
        }
    }
    return $sources[0];
};

$depot = new Depot($config, $app->stockage, new Journal($app->stockage));
$localite = Localite::depuisFichier(dirname(__DIR__, 2) . '/api/data/zones.json');
$parMois = [-6 => 7, -5 => 9, -4 => 12, -3 => 14, -2 => 16, -1 => 18, 0 => 0];
$joursEcoules = max(1, (int) $maintenant->format('j'));
$parMois[0] = max(4, (int) round(19 * $joursEcoules / (int) $maintenant->format('t')));
$compteur = 0;
$crees = [];

foreach ($parMois as $decalage => $nombre) {
    $debutMois = $maintenant->modify('first day of this month')->setTime(0, 0)->modify("$decalage months");
    $joursDansMois = $decalage === 0 ? $joursEcoules : (int) $debutMois->format('t');
    for ($k = 0; $k < $nombre; $k++) {
        $jour = mt_rand(1, $joursDansMois);
        $recue = $debutMois->modify('+' . ($jour - 1) . ' days')->setTime(mt_rand(7, 20), mt_rand(0, 59));
        if ($decalage === 0 && $k >= $nombre - 4) {
            $recue = $maintenant->modify('-' . mt_rand(20, 300) . ' minutes'); // arrivées des dernières heures
        }
        if ($recue > $maintenant->modify('-20 minutes')) {
            $recue = $maintenant->modify('-' . mt_rand(25, 600) . ' minutes');
        }
        $type = $hasard(['proprietaire', 'proprietaire', 'proprietaire', 'locataire', 'regie', 'regie', 'architecte', 'entreprise', 'commune', 'proprietaire']);
        $travaux = $chance(.15) ? ['peinture', 'placo'] : [$hasard(['isolation-acoustique', 'isolation-acoustique', 'placo', 'peinture', 'peinture', 'cloisons-isothermes', 'ne-sait-pas', 'isolation-acoustique', 'placo', 'peinture', 'cloisons-isothermes', 'placo', 'peinture', 'isolation-acoustique', 'autre'])];
        $surface = $hasard(['moins-15', '15-50', '15-50', '50-200', '50-200', 'plus-200', 'ne-sait-pas']);
        $delai = $hasard(['moins-1-mois', '1-3-mois', '1-3-mois', '3-6-mois', 'non-defini']);
        [$npa, $commune] = $hasard($communes);
        $message = $hasard($messages);
        $src = $tirerSource();
        $telephone = $chance(.12) ? null : ['e164' => sprintf('+417900000%02d', $compteur % 100), 'affiche' => sprintf('079 000 00 %02d', $compteur % 100), 'mobile' => true];
        $prenom = $hasard($prenoms);
        $nom = $hasard($noms);
        $email = $chance(.75) ? strtolower(Validateur::normaliserEmail(iconv('UTF-8', 'ASCII//TRANSLIT', $prenom) . '.' . iconv('UTF-8', 'ASCII//TRANSLIT', $nom) . $compteur . '@exemple.test') ?? '') : '';
        $saisie = $chance(.14);
        $formulaire = !$saisie && $chance(.12) ? 'rappel' : 'devis';
        $canal = $saisie ? 'telephone' : 'site';
        $loc = $localite->resoudre($npa, $commune);
        $source = Source::normaliser(['utm_source' => $src[1], 'utm_medium' => $src[2], 'gclid' => $src[5] && $chance(.6) ? 'Cj0KCQdemo' . $compteur : '', 'referent' => $src[3], 'canal' => $canal, 'formulaire' => $formulaire]);
        $connuPar = $saisie || $src[4] !== '' && $chance(.7) ? ($src[4] ?: 'autre') : '';
        $nbFichiers = $chance(.2) ? 1 : 0;
        $sc = $app->scoring->calculer([
            'type_client' => $type, 'service' => Validateur::servicePrincipal($travaux), 'surface' => $surface, 'zone' => $loc['zone'], 'delai' => $delai,
            'source_categorie' => $source['categorie'], 'connu_par' => $connuPar, 'canal' => $canal, 'formulaire' => $formulaire, 'message' => $message,
            'telephone' => $telephone !== null || $saisie, 'nb_fichiers' => $nbFichiers,
        ]);
        $echeance = $app->heures->echeance($sc['priorite'], $recue);
        $compteur++;
        $ref = sprintf('AC-%d-%04d', (int) $recue->format('Y'), 9000 + $compteur);
        $org = $organisations[$type] ?? null;
        $e = [
            'v' => 1, 'ref' => $ref, 'recue_le' => Base::utc($recue), 'formulaire' => $formulaire, 'canal' => $canal,
            'cree_par' => $saisie ? $hasard([$alex, $camille]) : null, 'mode_test' => false,
            'role_associe' => in_array($type, ['regie', 'architecte', 'commune', 'entreprise'], true) ? 'bureau' : 'terrain',
            'contact' => ['civilite' => '', 'prenom' => $prenom, 'nom' => $nom, 'email' => $email, 'telephone_e164' => $telephone['e164'] ?? ($saisie ? sprintf('+417900001%02d', $compteur % 100) : ''),
                'telephone_affiche' => $telephone['affiche'] ?? ($saisie ? sprintf('079 000 01 %02d', $compteur % 100) : ''), 'telephone_mobile' => true, 'adresse' => '', 'npa' => '', 'localite' => '',
                'preference_contact' => 'appel', 'creneau' => $hasard(['matin', 'apres-midi', 'indifferent'])],
            'projet' => ['type_client' => $type, 'travaux' => $travaux, 'service' => Validateur::servicePrincipal($travaux), 'surface' => $surface, 'delai' => $delai,
                'commune' => $commune, 'npa' => $npa, 'canton' => (string) ($loc['canton'] ?? ''), 'zone' => (string) $loc['zone'], 'message' => $message,
                'connu_par' => $connuPar, 'recommande_par' => $connuPar === 'recommandation' && $chance(.5) ? 'Un voisin (fictif)' : '', 'guide' => ''],
            'scoring' => ['score' => $sc['score'], 'priorite' => $sc['priorite'] === 'hors-cible' ? 'hors_cible' : $sc['priorite'], 'detail' => $sc['detail'], 'regles' => array_merge($sc['regles'], $sc['hors_cible'])],
            'echeance_le' => Base::utc($echeance),
            'source' => ['categorie' => $source['categorie'], 'libelle' => $source['libelle'], 'emplacement' => 'formulaire-contact', 'page' => '/contact.html',
                'page_entree' => $hasard(['/isolation-acoustique.html', '/peinture.html', '/', '/placo.html', '/professionnels.html']), 'referent' => $src[3],
                'utm' => ['utm_source' => $src[1], 'utm_medium' => $src[2], 'utm_campaign' => $src[1] === 'google' ? 'acoustique-geneve' : '', 'utm_content' => '', 'utm_term' => ''],
                'gclid' => $src[5] && $chance(.6) ? 'Cj0KCQdemo' . $compteur : '', 'consent_ads' => $src[5] ? 'accorde' : ''],
            'fichiers' => [],
            'accuse_reception' => $email !== '' ? 'envoye' : 'non',
        ];
        if ($org) {
            $e['contact']['nom'] = $nom;
        }
        if ($depot->enregistrer($e) !== 'enregistree') {
            fwrite(STDERR, "Échec d'enregistrement de $ref.\n");
            exit(1);
        }
        if ($org) {
            $b->executer('UPDATE contact SET organisation = ? WHERE id = (SELECT contact_id FROM demande WHERE ref = ?)', [$hasard($org), $ref]);
        }
        $crees[] = ['ref' => $ref, 'recue' => $recue, 'prio' => $e['scoring']['priorite'], 'surface' => $surface, 'saisie' => $saisie];
    }
}

// Un doublon possible (même téléphone) et une demande de test (exclue des indicateurs).
$b->executer("UPDATE contact SET telephone_e164 = '+41790000003', telephone_affiche = '079 000 00 03' WHERE id = (SELECT contact_id FROM demande WHERE ref = ?)", [$crees[count($crees) - 2]['ref']]);
$b->executer('UPDATE demande SET mode_test = 1 WHERE ref = ?', [$crees[count($crees) - 3]['ref']]);

// ------------------------------------------------------------- parcours
$heures = $app->heures;
$agir = static function (string $ref, string $action, array $p, \DateTimeImmutable $quand, int $auteur) use ($app, $maintenant): bool {
    if ($quand >= $maintenant) {
        return false;
    }
    $id = (int) $app->base->valeur('SELECT id FROM demande WHERE ref = ?', [$ref]);
    try {
        $app->demandes->agir($id, $action, $p, $auteur, 'admin', $quand);
        return true;
    } catch (\DomainException $ex) {
        fwrite(STDERR, "$ref $action : " . $ex->getMessage() . "\n");
        return false;
    }
};
$montants = ['moins-15' => [1800, 4000], '15-50' => [3500, 9000], '50-200' => [8000, 24000], 'plus-200' => [22000, 60000], 'ne-sait-pas' => [3000, 15000]];
$motifs = ['prix', 'prix', 'delai', 'reporte', 'ailleurs', 'trop_petit', 'autre'];
usort($crees, static fn ($x, $y) => $x['recue'] <=> $y['recue']);
$recentes = array_slice(array_keys(array_filter($crees, static fn ($c) => !$c['saisie'] && $c['prio'] !== 'hors_cible')), -7);
foreach ($crees as $i => $c) {
    $ref = $c['ref'];
    if (in_array($i, $recentes, true)) {
        // Les sept plus récentes : « nouvelles », dont deux déjà tentées une fois.
        if (array_search($i, $recentes, true) < 2) {
            $agir($ref, 'pas_de_reponse', [], $app->heures->ajouterMinutesOuvrables($c['recue'], 60), $i % 2 ? $alex : $camille);
        }
        continue;
    }
    $auteur = $i % 2 ? $alex : $camille;
    $age = ($maintenant->getTimestamp() - $c['recue']->getTimestamp()) / 86400;
    if ($c['prio'] === 'hors_cible') {
        if ($age > 2) {
            $agir($ref, 'hors_cible', [], $heures->ajouterMinutesOuvrables($c['recue'], 300), $auteur);
        }
        continue;
    }
    $delaiMin = match ($c['prio']) { 'A' => mt_rand(25, 200), 'B' => mt_rand(90, 420), default => mt_rand(300, 1100) };
    $t = $heures->ajouterMinutesOuvrables($c['recue'], $c['saisie'] ? 1 : $delaiMin);
    if (!$c['saisie'] && $chance(.08)) {
        $t1 = $t;
        $agir($ref, 'pas_de_reponse', [], $t1, $auteur);
        $agir($ref, 'pas_de_reponse', [], $t1 = $heures->jourOuvrableSuivant($t1, 10), $auteur);
        $agir($ref, 'pas_de_reponse', [], $t1 = $heures->jourOuvrableSuivant($t1, 10), $auteur);
        $agir($ref, 'perdue', ['motif' => 'sans_reponse'], $heures->jourOuvrableSuivant($t1, 16), $auteur);
        continue;
    }
    if (!$agir($ref, 'contact_etabli', [], $t, $auteur)) {
        continue;
    }
    if ($chance(.12)) {
        $agir($ref, 'perdue', ['motif' => $hasard(['trop_petit', 'reporte', 'delai'])], $t->modify('+1 day'), $auteur);
        continue;
    }
    if ($age < 21 && $chance(.4)) {
        continue; // contact établi récemment : visite ou offre à venir
    }
    $t = $t->modify('+' . mt_rand(1, 4) . ' days');
    if ($chance(.65)) {
        $visite = $heures->jourOuvrableSuivant($t, mt_rand(8, 15));
        if (!$agir($ref, 'visite_planifiee', ['date' => $visite->format('Y-m-d'), 'heure' => $visite->format('H:i'), 'adresse' => ''], $t, $auteur)) {
            continue;
        }
        if ($visite > $maintenant) {
            continue; // visite à venir
        }
        $t = $visite->modify('+' . mt_rand(2, 8) . ' days');
    } else {
        $t = $t->modify('+' . mt_rand(3, 9) . ' days');
    }
    if ($chance(.18) && $t > $maintenant->modify('-20 days')) {
        continue; // offre pas encore faite
    }
    [$min, $max] = $montants[$c['surface']];
    $montant = round(mt_rand($min, $max), -2);
    if (!$agir($ref, 'offre_envoyee', ['montant' => (string) $montant, 'date' => $t->format('Y-m-d')], $t, $auteur)) {
        continue;
    }
    $decision = $t->modify('+' . mt_rand(8, 50) . ' days');
    $r = mt_rand(1, 100);
    $ancienne = $t < $maintenant->modify('-45 days');
    if ($r <= ($ancienne ? 38 : 30)) {
        $agir($ref, 'signee', ['montant' => (string) ($chance(.3) ? round($montant * 0.95, -2) : $montant), 'date' => $decision->format('Y-m-d')], $decision, $auteur);
    } elseif ($r <= ($ancienne ? 82 : 55)) {
        $agir($ref, 'perdue', ['motif' => $hasard($motifs), 'recontact' => '1'], $decision, $auteur);
    }
}

// Quelques notes pour l'historique.
foreach (array_slice($crees, -12, 4) as $c) {
    $id = (int) $b->valeur('SELECT id FROM demande WHERE ref = ?', [$c['ref']]);
    $b->inserer('interaction', ['demande_id' => $id, 'type' => 'note', 'contenu' => 'Préfère être rappelée après 17 h (note fictive).', 'auteur_id' => $alex, 'origine' => 'admin', 'cree_le' => Base::utc($c['recue']->modify('+3 hours'))]);
}

$n = (int) $b->valeur('SELECT COUNT(*) FROM demande');
echo "Base de démonstration prête : $n demandes fictives, " . count($comptes) . " comptes.\n\n";
echo "Mot de passe de tous les comptes de démonstration : « " . DEMO_MDP . " »\n";
foreach ($comptes as [$email, $nom, $role]) {
    echo str_pad($email, 32) . ' ' . str_pad($role, 18) . ' clé TOTP ' . DEMO_SECRETS[$email] . "\n";
}
echo "\nCode à 6 chiffres du moment (pour un essai) : php -r 'require \"site/admin/lib/bootstrap.php\"; echo AndyConstruct\\Admin\\Totp::code(AndyConstruct\\Admin\\Totp::base32Decoder(\"ALEXMODELEDEMOTOTPAAAAAAAAAAAAAA\"), time()), PHP_EOL;'\n";
