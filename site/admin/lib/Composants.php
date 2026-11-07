<?php
declare(strict_types=1);

namespace AndyConstruct\Admin;

/** Composants partagés par la liste, les colonnes et la fiche. */
final class Composants
{
    /** Texte de la prochaine action selon le statut (liste et colonnes). */
    public static function prochaineAction(App $app, array $d): string
    {
        return match ($d['statut']) {
            'contact_etabli' => 'Planifier la visite ou envoyer l\'offre',
            'visite_planifiee' => $d['visite'] ? 'Visite ' . Format::dateH(Format::t($d['visite']['prevue_le'])) : 'Visite à fixer',
            'offre_envoyee' => ($r = $app->demandes->relance($d)) ? $r['texte'] : 'Offre envoyée',
            'signee' => 'Planifier le chantier',
            'perdue' => 'Perdue : ' . mb_strtolower(Demandes::MOTIFS[$d['motif_perte'] ?? 'autre'][0] ?? ''),
            'hors_cible' => 'Réponse de réorientation',
            'guide' => 'Envoyer le guide par la poste',
            default => '—',
        };
    }

    /**
     * Formulaires des transitions autorisées (une petite fenêtre par transition :
     * montant pour l'offre et la signature, motif pour la perte, date pour la visite).
     */
    public static function formulairesTransitions(App $app, array $d, array $actions, string $retour): string
    {
        $e = static fn ($v) => Vue::e($v);
        $id = $e($d['ref']);
        $aujourdhui = $app->maintenant->format('Y-m-d');
        $h = '<ul class="transitions">';
        foreach ($actions as $action => $libelle) {
            $champs = '';
            $uid = $id . '-' . $action;
            switch ($action) {
                case 'visite_planifiee':
                    $champs = '<label class="champ" for="d-' . $uid . '"><span>Date</span><input id="d-' . $uid . '" type="date" name="date" required min="' . $aujourdhui . '"></label>'
                        . '<label class="champ" for="h-' . $uid . '"><span>Heure</span><input id="h-' . $uid . '" type="time" name="heure" required value="08:00"></label>'
                        . '<label class="champ" for="a-' . $uid . '"><span>Adresse (facultatif)</span><input id="a-' . $uid . '" name="adresse" maxlength="300" autocomplete="off"></label>';
                    break;
                case 'offre_envoyee':
                case 'nouvelle_version':
                    $champs = '<label class="champ" for="m-' . $uid . '"><span>Montant HT (CHF)</span><input id="m-' . $uid . '" name="montant" inputmode="decimal" required autocomplete="off" placeholder="12\'500"></label>'
                        . '<label class="champ" for="d-' . $uid . '"><span>Envoyée le</span><input id="d-' . $uid . '" type="date" name="date" required value="' . $aujourdhui . '" max="' . $aujourdhui . '"></label>'
                        . '<label class="champ" for="n-' . $uid . '"><span>N° de l\'offre (facultatif)</span><input id="n-' . $uid . '" name="numero" maxlength="30" autocomplete="off"></label>';
                    break;
                case 'signee':
                    $champs = '<label class="champ" for="m-' . $uid . '"><span>Montant signé HT (CHF)</span><input id="m-' . $uid . '" name="montant" inputmode="decimal" required autocomplete="off" value="' . $e($d['offre'] ? Format::nb((float) $d['offre']['montant_ht']) : '') . '"></label>'
                        . '<label class="champ" for="d-' . $uid . '"><span>Signée le</span><input id="d-' . $uid . '" type="date" name="date" required value="' . $aujourdhui . '" max="' . $aujourdhui . '"></label>';
                    break;
                case 'perdue':
                    $motifs = $d['statut'] === 'nouvelle' ? ['sans_reponse' => Demandes::MOTIFS['sans_reponse']] : ($d['statut'] === 'signee' ? ['annule' => Demandes::MOTIFS['annule']] : array_diff_key(Demandes::MOTIFS, ['annule' => 1]));
                    $opts = count($motifs) > 1 ? '<option value="">Choisir</option>' : '';
                    foreach ($motifs as $code => [$lib]) {
                        $opts .= '<option value="' . $code . '">' . $e($lib) . '</option>';
                    }
                    $champs = '<label class="champ" for="mo-' . $uid . '"><span>Motif (obligatoire)</span><select id="mo-' . $uid . '" name="motif" required>' . $opts . '</select></label>'
                        . '<label class="case" for="r-' . $uid . '"><input id="r-' . $uid . '" type="checkbox" name="recontact" value="1"> Recontacter dans 6 mois (si le motif le permet)</label>';
                    break;
            }
            $form = '<form method="post" action="' . $e(Vue::url('fiche', ['ref' => $d['ref']])) . '" class="formulaire-transition">' . Vue::csrf($app)
                . '<input type="hidden" name="op" value="statut"><input type="hidden" name="action" value="' . $e($action) . '"><input type="hidden" name="version" value="' . (int) $d['version'] . '"><input type="hidden" name="retour" value="' . $e($retour) . '">'
                . $champs . '<button class="btn btn-petit' . ($champs ? ' btn-sombre' : ' btn-discret') . '" type="submit">' . $e($libelle) . '</button></form>';
            $h .= $champs ? '<li><details class="transition"><summary>' . $e($libelle) . '</summary>' . $form . '</details></li>' : '<li>' . $form . '</li>';
        }
        return $h . '</ul>';
    }
}
