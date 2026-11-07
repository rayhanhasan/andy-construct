<?php
declare(strict_types=1);

namespace AndyConstruct\Admin;

use AndyConstruct\Api\Canaux;

/**
 * Gabarit et composants communs (plan admin §3.2), repris de la maquette
 * docs/v4/admin/maquette/. Aucun script ni style en ligne (CSP stricte) :
 * les réglets et mètres sont des SVG, les comportements dans assets/admin.js.
 */
final class Vue
{
    public static string $base = '/admin/';

    public static function e(mixed $v): string
    {
        return Format::e($v);
    }

    /** Adresse d'un écran : ?p=…&… (relative au dossier de l'admin). */
    public static function url(string $page, array $params = []): string
    {
        $q = array_filter(['p' => $page] + $params, static fn ($v) => $v !== null && $v !== '');
        return self::$base . ($q === ['p' => 'vue'] || $page === '' ? '' : '?' . http_build_query($q));
    }

    public static function csrf(App $app): string
    {
        return '<input type="hidden" name="_csrf" value="' . self::e($app->auth->csrf()) . '">';
    }

    public static function flash(string $texte, string $type = 'ok'): void
    {
        $_SESSION['flash'][] = ['texte' => $texte, 'type' => $type];
    }

    // ------------------------------------------------------------ composants

    public static function prio(?string $p): string
    {
        if ($p === null || $p === '') {
            return '<span class="prio prio-HC">—</span>';
        }
        if ($p === 'hors_cible' || $p === 'hors-cible') {
            return '<span class="prio prio-HC">Hors cible</span>';
        }
        return '<span class="prio prio-' . self::e($p) . '"><span class="sr">Priorité </span>' . self::e($p) . '</span>';
    }

    public static function prioScore(array $d): string
    {
        return '<span class="prio-score">' . self::prio($d['priorite_eff']) . ($d['score'] !== null ? '<span class="discret">' . (int) $d['score'] . '</span>' : '')
            . ($d['priorite_corrigee'] ? '<span class="sr"> (corrigée)</span><span class="etiquette" title="Priorité corrigée par un associé">corrigée</span>' : '') . '</span>';
    }

    public static function statut(array $d): string
    {
        $s = $d['statut'] === 'nouvelle' && $d['priorite_eff'] === 'hors_cible' ? 'hors_cible' : $d['statut'];
        $lib = $s === 'hors_cible' && $d['statut'] === 'nouvelle' ? 'Hors cible à valider' : (Demandes::STATUTS[$s] ?? $s);
        return '<span class="statut statut-' . self::e($s) . '">' . self::e($lib) . '</span>' . ((int) $d['mode_test'] ? ' <span class="etiquette">test</span>' : '');
    }

    /** Réglet SVG (0 à 1) : la longueur dit le temps restant. */
    public static function reglet(float $fraction, bool $retard = false): string
    {
        $w = $retard ? 100 : max(4, min(100, (int) round($fraction * 100)));
        return '<svg class="reglet' . ($retard ? ' retard' : '') . '" viewBox="0 0 100 4" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            . '<rect class="piste" width="100" height="4" rx="2"/><rect class="rempli" width="' . $w . '" height="4" rx="2"/></svg>';
    }

    public static function echeance(array $d, App $app): string
    {
        $e = $d['echeance'];
        if ($e === null) {
            return '<span class="discret">—</span>';
        }
        $now = $app->maintenant;
        if ($e < $now) {
            return '<div class="echeance retard"><span class="texte"><span class="icone-alerte" aria-hidden="true">!</span>En retard</span><span class="petit">depuis ' . self::e(Format::dateH($e)) . '</span>' . self::reglet(1, true) . '</div>';
        }
        $debut = $d['recue'] ?? $now;
        $total = max(60, $e->getTimestamp() - $debut->getTimestamp());
        $reste = $e->getTimestamp() - $now->getTimestamp();
        $min = intdiv($reste, 60);
        $txt = $min < 60 ? "dans $min min" : ($e->format('Y-m-d') === $now->format('Y-m-d') ? "aujourd'hui " . Format::heure($e) : Format::dateH($e));
        return '<div class="echeance"><span class="texte">Rappeler ' . self::e($txt) . '</span>' . self::reglet($reste / $total) . '</div>';
    }

    /** Mètre de progression face à l'objectif (SVG, sans style en ligne). */
    public static function metre(float $valeur, float $max, ?float $cible, string $etiquette): string
    {
        $max = $max > 0 ? $max : 1;
        $w = max(0, min(100, $valeur / $max * 100));
        $s = '<svg class="metre" viewBox="0 0 100 16" preserveAspectRatio="none" role="img" aria-label="' . self::e($etiquette) . '">'
            . '<rect class="piste" x="0" y="4" width="100" height="8" rx="4"/><rect class="rempli" x="0" y="4" width="' . round($w, 1) . '" height="8" rx="4"/>';
        if ($cible !== null) {
            $c = max(0, min(99, $cible / $max * 100));
            $s .= '<rect class="cible" x="' . round($c, 1) . '" y="0" width="1.2" height="16"/>';
        }
        return $s . '</svg>';
    }

    public static function etat(?bool $ok, string $texteOk, string $texteKo, ?string $neutre = null): string
    {
        if ($neutre !== null || $ok === null) {
            return '<div class="etat"><span class="icone-ok" aria-hidden="true">~</span>' . self::e($neutre ?? 'Pas encore mesurable') . '</div>';
        }
        return $ok ? '<div class="etat"><span class="icone-ok" aria-hidden="true">✓</span>' . self::e($texteOk) . '</div>'
            : '<div class="etat ko"><span class="icone-alerte" aria-hidden="true">!</span>' . self::e($texteKo) . '</div>';
    }

    public static function aide(string $id, string $texte): array
    {
        return [
            '<button class="aide" type="button" aria-expanded="false" aria-controls="' . self::e($id) . '" title="Définition"><span aria-hidden="true">?</span><span class="sr">Définition</span></button>',
            '<p class="definition" id="' . self::e($id) . '" hidden>' . self::e($texte) . '</p>',
        ];
    }

    public static function tableDonnees(string $titre, array $entetes, array $lignes): string
    {
        $h = '<details class="donnees"><summary>Voir les données</summary><div class="defile" tabindex="0" role="region" aria-label="Tableau, défile horizontalement"><table class="tableau"><caption class="sr">' . self::e($titre) . '</caption><thead><tr>';
        foreach ($entetes as $i => $e) {
            $h .= '<th scope="col"' . ($i ? ' class="num"' : '') . '>' . self::e($e) . '</th>';
        }
        $h .= '</tr></thead><tbody>';
        foreach ($lignes as $l) {
            $h .= '<tr>';
            foreach (array_values($l) as $i => $c) {
                $h .= $i ? '<td class="num">' . self::e($c) . '</td>' : '<th scope="row">' . self::e($c) . '</th>';
            }
            $h .= '</tr>';
        }
        return $h . '</tbody></table></div></details>';
    }

    public static function select(string $nom, string $libelle, string $valeur, array $options, string $id = ''): string
    {
        $id = $id ?: 'f-' . $nom;
        $h = '<label for="' . self::e($id) . '">' . self::e($libelle) . '<select id="' . self::e($id) . '" name="' . self::e($nom) . '">';
        foreach ($options as $v => $l) {
            $h .= '<option value="' . self::e($v) . '"' . ((string) $v === $valeur ? ' selected' : '') . '>' . self::e($l) . '</option>';
        }
        return $h . '</select></label>';
    }

    public static function nomLien(array $d): string
    {
        return '<a href="' . self::e(self::url('fiche', ['ref' => $d['ref']])) . '">' . self::e($d['nom_complet']) . '</a>'
            . ($d['organisation'] ? '<span class="org">' . self::e($d['organisation']) . '</span>' : '');
    }

    public static function canal(array $d): string
    {
        return self::e(Canaux::libelle($d['canal_eff'])) . ($d['canal'] !== 'site' ? ' <span class="discret">(' . self::e(Demandes::CANAUX_SAISIE[$d['canal']] ?? $d['canal']) . ')</span>' : '');
    }

    // ---------------------------------------------------------------- gabarit

    private const ICONES = [
        'vue' => '<rect x="2.5" y="2.5" width="6" height="6"/><rect x="11.5" y="2.5" width="6" height="6"/><rect x="2.5" y="11.5" width="6" height="6"/><rect x="11.5" y="11.5" width="6" height="6"/>',
        'a-traiter' => '<path d="M2.5 11.5h4l1.5 2.5h4l1.5-2.5h4"/><path d="M4.5 4.5h11l2 7v5h-15v-5z"/>',
        'demandes' => '<path d="M3 5h14M3 10h14M3 15h14"/>',
        'saisie' => '<path d="M5.5 3h2.5l1 4-2 1.2a8 8 0 0 0 4.8 4.8l1.2-2 4 1v2.5A1.5 1.5 0 0 1 15.5 16 12.5 12.5 0 0 1 4 4.5 1.5 1.5 0 0 1 5.5 3z"/><path d="M14 2.5v5M11.5 5h5"/>',
        'acquisition' => '<path d="M3 16.5h14"/><path d="M5 13V9M9 13V5M13 13v-3M17 13V7"/>',
        'parametres' => '<circle cx="10" cy="10" r="2.6"/><path d="M10 2.5v2.2M10 15.3v2.2M2.5 10h2.2M15.3 10h2.2M4.7 4.7l1.6 1.6M13.7 13.7l1.6 1.6M4.7 15.3l1.6-1.6M13.7 6.3l1.6-1.6"/>',
        'donnees' => '<path d="M10 2.5l6 2.5v4.5c0 4-2.6 6.6-6 8-3.4-1.4-6-4-6-8V5z"/><path d="M7.5 10l2 2 3.5-3.5"/>',
        'compte' => '<circle cx="10" cy="7" r="3.2"/><path d="M3.5 17c.8-3.2 3.4-5 6.5-5s5.7 1.8 6.5 5"/>',
    ];

    private static function icone(string $nom): string
    {
        return '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true" focusable="false">' . (self::ICONES[$nom] ?? '') . '</svg>';
    }

    /** Page complète avec navigation (utilisateur connecté). */
    public static function page(App $app, string $route, string $titre, string $contenu): string
    {
        $u = $app->utilisateur;
        $nav = [
            [['vue', "Vue d'ensemble", 'vue'], ['a-traiter', 'À traiter', 'demandes'], ['demandes', 'Demandes', 'demandes'], ['saisie', 'Saisir un appel', 'demandes']],
            [['acquisition', 'Acquisition', 'acquisition']],
            [['parametres', 'Paramètres', 'depenses'], ['donnees', 'Journal et données', 'journal'], ['compte', 'Mon compte', 'compte']],
        ];
        $retards = Auth::peut($u, 'demandes') ? (int) $app->base->valeur("SELECT COUNT(*) FROM demande WHERE statut = 'nouvelle' AND echeance_le < ?", [\AndyConstruct\Api\Base::utc($app->maintenant)]) : 0;
        $pastille = $retards > 0 ? '<span class="pastille" title="Demandes en retard"><span class="sr">, </span>' . $retards . '<span class="sr"> en retard</span></span>' : '';
        $lateral = '';
        foreach ($nav as $groupe) {
            $items = '';
            foreach ($groupe as [$p, $lib, $droit]) {
                if (!Auth::peut($u, $droit)) {
                    continue;
                }
                $courant = $route === $p || ($route === 'fiche' && $p === 'demandes');
                $items .= '<li><a href="' . self::e(self::url($p)) . '"' . ($courant ? ' aria-current="page"' : '') . '>' . self::icone($p) . self::e($lib) . ($p === 'a-traiter' ? $pastille : '') . '</a></li>';
            }
            $lateral .= $items !== '' ? '<ul class="nav-groupe">' . $items . '</ul>' : '';
        }
        $bas = '';
        if (Auth::peut($u, 'demandes')) {
            foreach ([['a-traiter', 'À traiter'], ['demandes', 'Demandes'], ['saisie', 'Saisir'], ['vue', 'Chiffres'], ['plus', 'Plus']] as [$p, $lib]) {
                $courant = $route === $p || ($route === 'fiche' && $p === 'demandes') || ($p === 'plus' && in_array($route, ['acquisition', 'parametres', 'donnees', 'compte'], true));
                $ic = $p === 'saisie' ? '<span class="rond"><svg viewBox="0 0 20 20" fill="none" stroke="#FFFFFF" stroke-width="2" aria-hidden="true" focusable="false"><path d="M10 4v12M4 10h12"/></svg></span>'
                    : ($p === 'plus' ? '<svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true" focusable="false"><circle cx="4.5" cy="10" r="1.6"/><circle cx="10" cy="10" r="1.6"/><circle cx="15.5" cy="10" r="1.6"/></svg>' : self::icone($p));
                $bas .= '<a href="' . self::e(self::url($p)) . '"' . ($courant ? ' aria-current="page"' : '') . ($p === 'saisie' ? ' class="saisir"' : '') . '>' . $ic . self::e($lib) . ($p === 'a-traiter' ? $pastille : '') . '</a>';
            }
            $bas = '<nav class="barre-bas" aria-label="Navigation sur téléphone">' . $bas . '</nav>';
        }
        $recherche = Auth::peut($u, 'demandes')
            ? '<form class="recherche" role="search" method="get" action="' . self::e(self::$base) . '"><input type="hidden" name="p" value="demandes"><input type="hidden" name="statut" value="toutes">'
                . '<label class="sr" for="recherche-globale">Rechercher une demande</label>'
                . '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true" focusable="false"><circle cx="8.5" cy="8.5" r="5.5"/><path d="M12.5 12.5l5 5"/></svg>'
                . '<input id="recherche-globale" name="q" type="search" autocomplete="off" placeholder="Nom, référence, téléphone ou commune" value="' . self::e($route === 'demandes' ? (string) ($_GET['q'] ?? '') : '') . '"></form>'
            : '<div class="recherche"></div>';
        $flash = '';
        foreach ($_SESSION['flash'] ?? [] as $f) {
            $flash .= '<div class="message-flash' . ($f['type'] === 'erreur' ? ' erreur' : '') . '" role="' . ($f['type'] === 'erreur' ? 'alert' : 'status') . '">' . self::e($f['texte']) . '</div>';
        }
        unset($_SESSION['flash']);
        $role = Auth::ROLES[$u['role']] ?? '';
        $roleMetier = $u['role_metier'] ? ', rôle « ' . $u['role_metier'] . ' »' : '';
        $corps = '<a class="lien-evitement" href="#contenu">Aller au contenu</a>'
            . '<div class="app"><aside class="lateral" aria-label="Navigation principale">'
            . '<a class="marque" href="' . self::e(self::url('vue')) . '"><img src="' . self::e(self::$base) . 'assets/logo-blanc.png" alt="Andy Construct" width="132" height="34"><span>Gestion des demandes</span></a>'
            . '<nav aria-label="Écrans">' . $lateral . '</nav>'
            . '<div class="lateral-pied"><strong>' . self::e($u['nom_affiche']) . '</strong>' . self::e($role . $roleMetier) . '</div></aside>'
            . '<div class="principal"><header class="haut"><img class="logo-mobile" src="' . self::e(self::$base) . 'assets/logo.png" alt="Andy Construct" width="86" height="22">'
            . $recherche
            . '<div class="haut-actions">' . (Auth::peut($u, 'demandes') ? '<a class="btn btn-sombre btn-saisir" href="' . self::e(self::url('saisie')) . '">Saisir un appel</a>' : '')
            . '<div class="utilisateur"><strong>' . self::e($u['nom_affiche']) . '</strong>' . self::e($role) . '</div>'
            . '<form method="post" action="' . self::e(self::url('deconnexion')) . '">' . self::csrf($app) . '<button class="btn btn-discret btn-petit" type="submit">Se déconnecter</button></form></div></header>'
            . '<main id="contenu" tabindex="-1">' . ($flash !== '' ? '<div class="messages">' . $flash . '</div>' : '') . $contenu . '</main></div></div>'
            . $bas;
        return self::document($titre, $corps);
    }

    public static function document(string $titre, string $corps, string $classe = ''): string
    {
        $b = self::e(self::$base);
        return '<!doctype html><html lang="fr-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            . '<meta name="robots" content="noindex, nofollow"><meta name="referrer" content="no-referrer">'
            . '<title>' . self::e($titre) . ' · Gestion Andy Construct</title>'
            . '<link rel="icon" type="image/png" href="' . $b . 'assets/favicon.png">'
            . '<link rel="stylesheet" href="' . $b . 'assets/admin.css?v=' . self::version('admin.css') . '">'
            . '<script src="' . $b . 'assets/admin.js?v=' . self::version('admin.js') . '" defer></script>'
            . '</head><body' . ($classe ? ' class="' . self::e($classe) . '"' : '') . '>' . $corps . '</body></html>';
    }

    private static function version(string $fichier): string
    {
        $f = dirname(__DIR__) . '/assets/' . $fichier;
        return is_file($f) ? substr(md5((string) filemtime($f) . filesize($f)), 0, 8) : '0';
    }

    public static function erreur(int $code, string $titre, string $texte): string
    {
        return self::document($titre, '<main class="page-seule" id="contenu"><div class="carte-connexion"><h1>' . self::e($titre) . '</h1><p>' . self::e($texte) . '</p><p><a class="btn" href="' . self::e(self::$base) . '">Retour à l\'accueil</a></p></div></main>', 'seul');
    }
}
