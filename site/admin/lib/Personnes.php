<?php
declare(strict_types=1);

namespace AndyConstruct\Admin;

use AndyConstruct\Api\Base;
use AndyConstruct\Api\Telephone;
use AndyConstruct\Api\Validateur;

/**
 * Droits des personnes (nLPD, plan admin §3.3 E13 et §4.6) : recherche d'une
 * personne, export de toutes ses données, effacement par anonymisation (les
 * indicateurs ne changent pas : date, canal, priorité, statut, montants et zone
 * sont gardés ; nom, coordonnées, message, commune exacte, notes, fichiers et
 * gclid sont effacés).
 */
final class Personnes
{
    public function __construct(private App $app)
    {
    }

    /** Contacts correspondant à un e-mail ou un téléphone (tous formats). */
    public function rechercher(string $saisie): array
    {
        $saisie = trim($saisie);
        $email = str_contains($saisie, '@') ? strtolower((string) Validateur::normaliserEmail($saisie)) : '';
        $tel = Telephone::normaliser($saisie)['e164'] ?? '';
        if ($email === '' && $tel === '') {
            return [];
        }
        return $this->app->base->tous(
            'SELECT c.*, (SELECT COUNT(*) FROM demande d WHERE d.contact_id = c.id) AS nb_demandes FROM contact c
             WHERE c.anonymise_le IS NULL AND ((c.email_normalise IS NOT NULL AND c.email_normalise = ?) OR (c.telephone_e164 IS NOT NULL AND c.telephone_e164 = ?)) ORDER BY c.id',
            [$email ?: '-', $tel ?: '-']
        );
    }

    /** Toutes les données d'un contact (export JSON lisible). */
    public function exporter(int $contactId): array
    {
        $b = $this->app->base;
        $contact = $b->un('SELECT * FROM contact WHERE id = ?', [$contactId]);
        if ($contact === null) {
            throw new \DomainException('Personne introuvable.');
        }
        $demandes = [];
        foreach ($b->tous('SELECT * FROM demande WHERE contact_id = ? ORDER BY recue_le', [$contactId]) as $d) {
            $id = (int) $d['id'];
            foreach (['travaux', 'score_detail', 'score_regles'] as $json) {
                $d[$json] = json_decode((string) $d[$json], true);
            }
            $d['attribution'] = $b->un('SELECT * FROM attribution WHERE demande_id = ?', [$id]);
            $d['historique'] = $b->tous('SELECT type, resultat, contenu, origine, cree_le FROM interaction WHERE demande_id = ? ORDER BY cree_le', [$id]);
            $d['visites'] = $b->tous('SELECT prevue_le, adresse, statut FROM visite WHERE demande_id = ?', [$id]);
            $d['offres'] = $b->tous('SELECT numero, version, montant_ht, envoyee_le, statut, signee_le, montant_signe_ht FROM offre WHERE demande_id = ?', [$id]);
            $d['fichiers'] = $b->tous('SELECT nom_original, type_mime, taille, cree_le, supprime_le FROM fichier WHERE demande_id = ?', [$id]);
            $demandes[] = $d;
        }
        unset($contact['email_normalise']);
        $this->app->audit('export_personne', 'contact', (string) $contactId, ['demandes' => count($demandes)]);
        return [
            'export' => 'Andy Construct, données personnelles (nLPD art. 25)',
            'produit_le' => gmdate('c'),
            'note' => 'Dates en UTC. Montants en CHF hors TVA.',
            'contact' => $contact,
            'demandes' => $demandes,
        ];
    }

    /** Ce qui sera effacé et gardé (aperçu avant confirmation). */
    public function apercu(int $contactId): array
    {
        $refs = array_column($this->app->base->tous('SELECT ref FROM demande WHERE contact_id = ? ORDER BY recue_le', [$contactId]), 'ref');
        $nbFichiers = (int) $this->app->base->valeur('SELECT COUNT(*) FROM fichier f JOIN demande d ON d.id = f.demande_id WHERE d.contact_id = ? AND f.supprime_le IS NULL', [$contactId]);
        $nbNotes = (int) $this->app->base->valeur("SELECT COUNT(*) FROM interaction i JOIN demande d ON d.id = i.demande_id WHERE d.contact_id = ? AND i.type = 'note'", [$contactId]);
        return ['refs' => $refs, 'fichiers' => $nbFichiers, 'notes' => $nbNotes];
    }

    /** Anonymise un contact et ses demandes. Irréversible. */
    public function effacer(int $contactId): int
    {
        $maintenant = Base::maintenant();
        $fichiersASupprimer = [];
        $n = $this->app->base->transaction(function (Base $b) use ($contactId, $maintenant, &$fichiersASupprimer): int {
            if ($b->un('SELECT id FROM contact WHERE id = ? AND anonymise_le IS NULL', [$contactId]) === null) {
                throw new \DomainException('Personne introuvable ou déjà effacée.');
            }
            $ids = array_map('intval', array_column($b->tous('SELECT id FROM demande WHERE contact_id = ?', [$contactId]), 'id'));
            $b->maj('contact', [
                'civilite' => null, 'prenom' => null, 'nom' => null, 'organisation' => null, 'email' => null, 'email_normalise' => null,
                'telephone_e164' => null, 'telephone_affiche' => null, 'adresse' => null, 'npa' => null, 'localite' => null,
                'preference_contact' => null, 'creneau' => null, 'anonymise_le' => $maintenant, 'modifie_le' => $maintenant,
            ], 'id = ?', [$contactId]);
            foreach ($ids as $id) {
                $b->maj('demande', ['message' => null, 'commune' => null, 'npa' => null, 'recommande_par' => null,
                    'anonymise_le' => $maintenant, 'modifie_le' => $maintenant], 'id = ?', [$id]);
                $b->maj('attribution', ['gclid' => null, 'referent' => null], 'demande_id = ?', [$id]);
                $b->executer("UPDATE interaction SET contenu = NULL WHERE demande_id = ? AND type IN ('note', 'email_entrant', 'sms', 'appel_entrant')", [$id]);
                $b->executer('UPDATE visite SET adresse = NULL WHERE demande_id = ?', [$id]);
                foreach ($b->tous('SELECT id, identifiant FROM fichier WHERE demande_id = ? AND supprime_le IS NULL', [$id]) as $f) {
                    $fichiersASupprimer[] = (string) $f['identifiant'];
                }
                $b->executer('UPDATE fichier SET nom_original = NULL, sha256 = NULL, supprime_le = ? WHERE demande_id = ?', [$maintenant, $id]);
                $b->inserer('interaction', ['demande_id' => $id, 'type' => 'systeme', 'contenu' => 'Données personnelles effacées (nLPD)',
                    'auteur_id' => $this->app->utilisateur['id'] ?? null, 'origine' => 'admin', 'cree_le' => $maintenant]);
            }
            return count($ids);
        });
        $dossier = $this->app->stockage->dossier('fichiers');
        foreach ($fichiersASupprimer as $f) {
            if (preg_match('/^[a-f0-9]{32}\.(jpg|png|heic|pdf)$/', $f)) {
                @unlink($dossier . '/' . $f);
            }
        }
        $this->app->audit('effacement', 'contact', (string) $contactId, ['demandes' => $n, 'fichiers' => count($fichiersASupprimer)]);
        return $n;
    }
}
