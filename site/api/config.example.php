<?php
/**
 * Configuration de l'endpoint des formulaires : MODÈLE.
 *
 * 1. Copiez ce fichier en « config.php » dans le même dossier (api/).
 * 2. Remplissez les valeurs marquées « À REMPLIR ».
 * 3. Ne versionnez JAMAIS config.php (il est exclu par .gitignore) et ne
 *    l'envoyez à personne par e-mail : il contient les secrets.
 *
 * Générer un secret (64 caractères hexadécimaux) :
 *   php -r 'echo bin2hex(random_bytes(32)), PHP_EOL;'
 *
 * Toute la documentation : docs/v2/automatisation.md
 */
declare(strict_types=1);

return [
    // Mode test : AUCUN envoi réel. Les e-mails sont écrits dans stockage/test-mails/
    // (fichiers .eml) et, si n8n.simuler vaut true, les webhooks dans stockage/test-webhooks/.
    // Mettre false en production.
    'mode_test' => true,

    // Adresses publiques (sans barre finale).
    'url_site' => 'https://www.andyconstruct.ch',
    'url_api' => 'https://www.andyconstruct.ch/api',

    // En-tête Origin accepté pour les envois (protection contre l'envoi depuis un autre site).
    // En mode test, http://localhost et http://127.0.0.1 sont aussi acceptés.
    'origines_autorisees' => ['https://www.andyconstruct.ch', 'https://andyconstruct.ch'],

    // Dossier privé (fichiers reçus, file d'attente, journaux). RECOMMANDÉ : hors de la
    // racine web, par exemple un dossier frère de public_html :
    //   'stockage' => dirname(__DIR__, 2) . '/andy-construct-prive',
    // À défaut, le dossier api/stockage/ est protégé par .htaccess (deny) + index.html.
    'stockage' => __DIR__ . '/stockage',

    // true uniquement derrière un proxy de confiance (Cloudflare…) : l'IP est alors lue
    // dans X-Forwarded-For / CF-Connecting-IP. Sinon REMOTE_ADDR.
    'faire_confiance_au_proxy' => false,

    // Secrets : 32 caractères au minimum chacun, tous différents.
    'secrets' => [
        // Partagé avec n8n (variable AC_HMAC_SECRET) : signature des webhooks.
        'hmac_webhook' => '', // À REMPLIR
        // Partagé avec n8n (variable AC_ACTION_SECRET) : liens « en un clic » et désinscription.
        'actions' => '',      // À REMPLIR
        // Propre au PHP : jeton horodaté, liens de fichiers, hachage des adresses IP.
        'local' => '',        // À REMPLIR
    ],

    // SMTP authentifié de la messagerie du domaine (Infomaniak : mail.infomaniak.com,
    // port 587, STARTTLS ; Hostinger : smtp.hostinger.com, port 465, ssl).
    'smtp' => [
        'actif' => true,
        'hote' => '',          // À REMPLIR
        'port' => 587,
        'securite' => 'tls',   // tls (STARTTLS, port 587) · ssl (port 465) · aucune
        'utilisateur' => '',   // À REMPLIR (souvent l'adresse complète : site@andyconstruct.ch)
        'mot_de_passe' => '',  // À REMPLIR
        'delai' => 10,         // secondes
    ],
    // Si le SMTP échoue : nouvel essai avec la fonction mail() de l'hébergeur.
    'repli_mail' => true,

    // Expéditeur technique (doit appartenir au domaine : SPF, DKIM, DMARC).
    'expediteur' => ['email' => 'site@andyconstruct.ch', 'nom' => 'Andy Construct'],
    // Adresse de réponse des accusés de réception si aucun associé n'est configuré.
    'repondre_a' => ['email' => 'contact@andyconstruct.ch', 'nom' => 'Andy Construct'],

    // Destinataires de la notification interne (e-mail envoyé pour CHAQUE demande).
    'destinataires_internes' => ['contact@andyconstruct.ch'],

    // Alertes techniques (file d'attente bloquée…) : l'agence.
    'alerte_email' => '', // À REMPLIR

    // Associés : « bureau » reçoit les demandes B2B (régies, architectes, communes,
    // entreprises), « terrain » celles des particuliers. RÔLES À CONFIRMER par le client.
    // Le nom apparaît dans l'accusé de réception (« X vous appelle aujourd'hui avant 16 h »).
    // Laisser vide pour écrire « l'un de nos associés ».
    'associes' => [
        'bureau' => ['nom' => '', 'email' => '', 'mobile' => ''],
        'terrain' => ['nom' => '', 'email' => '', 'mobile' => ''],
    ],

    // Coordonnées reprises dans les e-mails. Horaires À CONFIRMER par le client.
    'entreprise' => [
        'nom' => 'Andy Construct',
        'adresse' => 'Route des Acacias 48, 1227 Carouge',
        'tel_fixe' => '022 771 20 15',
        'tel_mobile' => '078 631 14 34',
        'site' => 'www.andyconstruct.ch',
        'email' => 'contact@andyconstruct.ch',
        'horaires' => 'du lundi au vendredi, de 7 h à 18 h',
    ],
    // Numéros depuis lesquels les associés rappellent (dit au prospect pour qu'il décroche).
    'numeros_appel_sortant' => 'le 022 771 20 15 ou le 078 631 14 34',

    'url_confidentialite' => 'https://www.andyconstruct.ch/confidentialite.html',

    // Case « J'accepte que mes coordonnées servent uniquement à traiter ma demande » :
    // exigée (true) au lancement. Peut passer à false après avis du juriste : la mention
    // d'information sous le bouton suffit alors (nLPD art. 19 ; architecture-cro.md §6.3).
    // La demande de rappel ne l'exige jamais.
    'accord_obligatoire' => true,

    // Facultatif : une fiche projet comparable citée dans l'accusé de réception, par service.
    'realisations_par_service' => [
        // 'isolation-acoustique' => 'https://www.andyconstruct.ch/realisations/salle-communale-collonge-bellerive.html',
    ],

    // n8n (laisser vide tant que n8n n'est pas installé : le site fonctionne sans).
    'n8n' => [
        'url_demande' => '',        // ex. https://n8n.andyconstruct.ch/webhook/ac-demande
        'url_aimant' => '',         // ex. https://n8n.andyconstruct.ch/webhook/ac-aimant
        'url_actions' => '',        // ex. https://n8n.andyconstruct.ch/webhook/ac-action
        'url_desinscription' => '', // ex. https://n8n.andyconstruct.ch/webhook/ac-stop
        'delai' => 5,               // secondes avant de basculer sur la file d'attente
        'simuler' => true,          // mode test : écrire les webhooks dans un fichier
    ],

    // Pages de remerciement (formulaire envoyé sans JavaScript) et du formulaire.
    'pages' => [
        'merci_devis' => '/merci.html',
        'merci_rappel' => '/merci.html',
        'merci_aimant' => '/merci-guide.html',
        'formulaire' => '/contact.html#formulaire',
    ],

    'anti_spam' => [
        // Délai minimal (secondes) entre l'affichage du formulaire et l'envoi.
        'delai_min' => ['devis' => 4, 'rappel' => 2, 'aimant' => 2],
        'jeton_validite_h' => 12,
        'limite_par_heure' => 5,        // demandes acceptées par IP et par heure
        'tentatives_par_heure' => 30,   // envois (y compris corrections) par IP et par heure
        'max_liens_message' => 3,
    ],

    'fichiers' => [
        'max_nombre' => 3,
        'max_taille_mo' => 8,            // par fichier (voir aussi .user.ini)
        'conservation_jours' => 30,      // purge automatique sur le serveur web
        'pj_max_total_mo' => 20,         // au-delà : liens signés au lieu de pièces jointes
        'lien_validite_h_interne' => 168,
        'lien_validite_h_n8n' => 24,
        'refuser_pdf_actifs' => true,    // PDF avec JavaScript, lancement ou fichiers intégrés
    ],

    'conservation' => [
        'journaux_jours' => 30,
        'file_attente_alerte_minutes' => 60,
        'file_attente_abandon_jours' => 14,
        'mails_test_jours' => 7,
    ],

    // Heures ouvrables pour les délais de rappel (jours fériés genevois inclus).
    // jours_fermes : fermetures de l'entreprise (vacances du bâtiment), format AAAA-MM-JJ.
    'heures_ouvrables' => ['debut' => 7, 'fin' => 18, 'jours_fermes' => []],

    // true : l'accusé de réception annonce un délai (« aujourd'hui avant 16 h »).
    // false : « dans les meilleurs délais ». Ne promettre que ce que l'on tient.
    'promesse_delai' => true,

    // Aimants à prospects (guides). Seuls les guides « actif » sont acceptés.
    'aimants' => [
        'guide-bruit' => [
            'actif' => false,
            'titre' => 'Réduire le bruit dans un appartement : ce qui marche vraiment',
            'url' => 'https://www.andyconstruct.ch/guides/reduire-le-bruit.pdf',
            'format' => 'PDF, 8 pages',
            'lecture' => '10 minutes',
            'liste_brevo' => 0,
        ],
        'checklist-regie' => [
            'actif' => false,
            'titre' => 'Travaux en immeuble habité : la check-list de la régie',
            'url' => 'https://www.andyconstruct.ch/guides/checklist-regie.pdf',
            'format' => 'PDF, 2 pages',
            'lecture' => '3 minutes',
            'liste_brevo' => 0,
        ],
    ],
    // Notification interne des aimants : 'tous', 'b2b_et_poste' (profils pro ou envoi postal) ou 'aucun'.
    'notifier_aimants' => 'b2b_et_poste',

    // Saisie express des appels reçus (canal=telephone) : clé exigée. Vide = désactivé.
    'cle_saisie_interne' => '',

    // cron.php appelé par URL : clé exigée (24 caractères minimum). Vide = CLI uniquement.
    'cron_cle' => '',

    // Supervision : URL de ping Healthchecks.io (https://hc-ping.com/…), facultatif.
    'healthcheck_url' => '',

    // Préfixe des références (AC-2026-0042).
    'reference_prefixe' => 'AC',
];
