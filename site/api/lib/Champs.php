<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Valeurs autorisées des listes du formulaire et libellés affichés dans les
 * e-mails. Toute modification doit être reportée dans
 * docs/v2/contrat-interface.md (le frontend envoie exactement ces valeurs).
 */
final class Champs
{
    public const FORMULAIRES = ['devis', 'rappel', 'envoi_postal_guide'];

    /** Anciens noms acceptés et convertis (compatibilité). */
    public const ALIAS_FORMULAIRES = ['aimant' => 'envoi_postal_guide'];

    public const TRAVAUX = [
        'placo' => 'Placo',
        'peinture' => 'Peinture',
        'isolation-acoustique' => 'Isolation acoustique',
        'cloisons-isothermes' => 'Cloisons isolantes',
        'ne-sait-pas' => 'Autre chose, ou je ne sais pas encore',
        'autre' => 'Autres travaux (hors de nos 4 métiers)',
    ];

    /** Les quatre prestations (pour détecter « plusieurs prestations »). */
    public const PRESTATIONS = ['placo', 'peinture', 'isolation-acoustique', 'cloisons-isothermes'];

    public const TYPE_CLIENT = [
        'proprietaire' => 'Propriétaire (maison, appartement, PPE)',
        'locataire' => 'Locataire',
        'regie' => 'Régie, gérance ou coopérative',
        'architecte' => "Architecte, bureau d'études ou entreprise générale",
        'commune' => 'Commune ou institution',
        'entreprise' => 'Entreprise, bureau ou commerce',
    ];

    public const TYPES_B2B = ['regie', 'architecte', 'commune', 'entreprise'];

    public const SURFACE = [
        'moins-15' => 'Moins de 15 m² (une réparation)',
        '15-50' => '15 à 50 m² (une ou deux pièces)',
        '50-200' => '50 à 200 m² (un appartement, un étage)',
        'plus-200' => 'Plus de 200 m², ou plusieurs logements',
        'ne-sait-pas' => 'Je ne sais pas',
    ];

    public const DELAI = [
        'moins-1-mois' => "Dès que possible (moins d'un mois)",
        '1-3-mois' => 'Dans 1 à 3 mois',
        '3-6-mois' => 'Dans 3 à 6 mois',
        'non-defini' => 'Pas encore défini',
    ];

    public const CONNU_PAR = [
        'recherche-google' => 'Recherche sur Google',
        'carte-google' => 'Carte Google',
        'recommandation' => "Recommandation d'un proche ou d'un voisin",
        'regie-architecte' => 'Une régie ou un architecte',
        'panneau-vehicule' => 'Un panneau de chantier ou un véhicule',
        'facebook' => 'Facebook',
        'linkedin' => 'LinkedIn',
        'autre' => 'Autre',
    ];

    public const PREFERENCE_CONTACT = [
        'appel' => 'Par téléphone',
        'email' => 'Par e-mail',
        'indifferent' => 'Peu importe',
    ];

    public const CRENEAU = [
        'matin' => 'le matin',
        'apres-midi' => "l'après-midi",
        'indifferent' => 'peu importe',
    ];

    public const CIVILITE = ['madame' => 'Madame', 'monsieur' => 'Monsieur'];

    public const PROFIL = self::TYPE_CLIENT + ['autre' => 'Autre'];

    public const CONSENT_ADS = ['accorde', 'refuse'];

    public const CANAL = ['site', 'telephone'];

    public static function libelle(array $liste, string $valeur, string $defaut = 'Non précisé'): string
    {
        return $liste[$valeur] ?? $defaut;
    }
}
