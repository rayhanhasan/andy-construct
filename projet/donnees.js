/* ==========================================================================
   Pilotage du projet Andy Construct : données du tableau de bord
   --------------------------------------------------------------------------
   Fichier PRIVÉ (agence Harbor Digital et Claude). À modifier à la main dans
   un éditeur, ou depuis le tableau de bord (bouton « Exporter donnees.js »).

   Règles
   - Un seul objet : window.PROJET. Pas de fetch : tout marche en file://.
   - Garder des guillemets doubles et une virgule après chaque élément.
   - Dates au format AAAA-MM-JJ. Laisser "" si inconnue.
   - Chemins de fichiers relatifs à la racine du dépôt (ex. "docs/v4/seo/audit-seo.md").
   - Aucun chiffre inventé : tout montant ou volume vient d'un document cité.

   Statuts autorisés
   - taches.statut          : "a-faire" | "en-cours" | "attente-client" | "fait"
   - taches.responsable     : "Agence" | "Claude" | "Client"
   - taches.priorite        : "haute" | "moyenne" | "basse"
   - decisions.statut       : "a-prendre" | "prise"
   - decisions.reco         : rang de l'option recommandée (0 = la première), -1 si aucune
   - questionnaire.statut   : "a-envoyer" | "envoye" | "repondu"
   - infos.statut           : "verifie" | "a-confirmer" | "manquant"
   - assets.statut          : "a-demander" | "demande" | "recu"
   - juridique.statut       : "pret" | "a-completer" | "a-faire" | "bloque"

   Les échéances des tâches ouvertes sont des propositions de l'agence, à ajuster.
   ========================================================================== */

window.PROJET = {
  "meta": {
    "projet": "Site d'acquisition Andy Construct",
    "client": "Andy Construct, Chanton & Cie",
    "agence": "Harbor Digital",
    "maj": "2026-11-07",
    "aujourdhui": "2026-11-07",
    "etat": "v3 livrée sur les 13 pages, en attente de validation client. v4 : audit SEO, mix d'acquisition et plans de l'admin livrés.",
    "depot": "rayhanhasan/andy-construct",
    "branche": "claude/eager-heisenberg-sz3nve",
    "note": "Échéances des tâches ouvertes = propositions de l'agence."
  },

  /* Chantiers du projet : l'avancement est calculé à partir des tâches. */
  "chantiers": [
    { "id": "site", "nom": "Site", "description": "Générateur, 13 pages, design v3" },
    { "id": "seo", "nom": "SEO", "description": "Migration, fiche Google, NAP, contenus" },
    { "id": "acquisition", "nom": "Acquisition", "description": "Mix C, Ads, avis, B2B, simap" },
    { "id": "admin", "nom": "Admin", "description": "Tableau de bord des associés" },
    { "id": "automatisation", "nom": "Automatisation", "description": "API PHP, n8n, messages" },
    { "id": "juridique", "nom": "Juridique", "description": "Mentions, nLPD, LCD, logos" },
    { "id": "contenus", "nom": "Contenus et assets", "description": "Photos, témoignages, logos" },
    { "id": "deploiement", "nom": "Déploiement", "description": "Hébergement, mise en ligne" }
  ],

  "taches": [
    { "id": "T01", "titre": "Design v3 « le trait de niveau » sur les 13 pages", "chantier": "site", "responsable": "Claude", "priorite": "haute", "statut": "fait", "echeance": "2026-10-31", "fichier": "docs/v3/direction-artistique.md", "note": "Commit 7c38ca0." },
    { "id": "T02", "titre": "Mur de logos couleur et badges pilotés par confirmations.json", "chantier": "site", "responsable": "Claude", "priorite": "haute", "statut": "fait", "echeance": "2026-10-31", "fichier": "tools/build/composants.py", "note": "" },
    { "id": "T03", "titre": "Drapeaux A/B (un seul test A/A au lancement)", "chantier": "site", "responsable": "Claude", "priorite": "moyenne", "statut": "fait", "echeance": "2026-10-31", "fichier": "tools/build/donnees/config.json", "note": "" },
    { "id": "T04", "titre": "Renommer le 4e service selon C16 (URL, menu, 301)", "chantier": "site", "responsable": "Claude", "priorite": "haute", "statut": "attente-client", "echeance": "", "fichier": "docs/v4/seo/audit-seo.md", "note": "Attend la décision C16. À faire avant la mise en ligne." },
    { "id": "T05", "titre": "Séance de validation et cochage de confirmations.json", "chantier": "site", "responsable": "Agence", "priorite": "haute", "statut": "attente-client", "echeance": "2026-11-20", "fichier": "tools/build/donnees/confirmations.json", "note": "0 point sur 44 coché. Mode verification + plaquette preview." },
    { "id": "T06", "titre": "Régénérer la production après les confirmations", "chantier": "site", "responsable": "Claude", "priorite": "haute", "statut": "a-faire", "echeance": "", "fichier": "tools/build/build.py", "note": "Après T05." },
    { "id": "T07", "titre": "Réduire encore le texte des pages services (objectif −40 %)", "chantier": "site", "responsable": "Claude", "priorite": "basse", "statut": "a-faire", "echeance": "", "fichier": "HANDOFF.md", "note": "Aujourd'hui −37 à −39 %." },

    { "id": "T10", "titre": "Audit SEO v4 et 7 corrections techniques", "chantier": "seo", "responsable": "Claude", "priorite": "haute", "statut": "fait", "echeance": "2026-11-01", "fichier": "docs/v4/seo/audit-seo.md", "note": "Commit 6a0e57f." },
    { "id": "T11", "titre": "301 des 17 anciennes URL testées sur Apache", "chantier": "seo", "responsable": "Claude", "priorite": "haute", "statut": "fait", "echeance": "2026-11-01", "fichier": "docs/v4/seo/audit-seo.md", "note": "À revérifier sur l'hébergeur réel." },
    { "id": "T12", "titre": "Search Console (propriété Domaine) et Bing Webmaster Tools", "chantier": "seo", "responsable": "Agence", "priorite": "haute", "statut": "attente-client", "echeance": "2026-11-20", "fichier": "docs/v4/seo/audit-seo.md", "note": "Besoin de l'accès DNS (Kreativ Media)." },
    { "id": "T13", "titre": "Fiche Google : vérifier, revendiquer, passer en zone desservie", "chantier": "seo", "responsable": "Agence", "priorite": "haute", "statut": "attente-client", "echeance": "2026-11-20", "fichier": "docs/v4/seo/audit-seo.md", "note": "Accès client nécessaire (C37, C29)." },
    { "id": "T14", "titre": "Nettoyage NAP : local.ch, search.ch, GGE, LinkedIn, firmen.ch…", "chantier": "seo", "responsable": "Agence", "priorite": "moyenne", "statut": "attente-client", "echeance": "", "fichier": "projet/infos-a-completer.md", "note": "Décider l'e-mail (C30) avant. search.ch affiche « protection auditive »." },
    { "id": "T15", "titre": "+300 à 400 mots propres par page service", "chantier": "seo", "responsable": "Claude", "priorite": "moyenne", "statut": "a-faire", "echeance": "", "fichier": "docs/v4/seo/audit-seo.md", "note": "Vocabulaire romand : plâtrerie, gypserie." },
    { "id": "T16", "titre": "Compléter sameAs du JSON-LD après la fiche Google", "chantier": "seo", "responsable": "Claude", "priorite": "basse", "statut": "a-faire", "echeance": "", "fichier": "tools/build/page_accueil.py", "note": "" },
    { "id": "T17", "titre": "Bing Places et Apple Business Connect", "chantier": "seo", "responsable": "Agence", "priorite": "moyenne", "statut": "a-faire", "echeance": "", "fichier": "docs/v4/seo/audit-seo.md", "note": "Mois 1." },

    { "id": "T20", "titre": "Plan de mix d'acquisition et simulateur", "chantier": "acquisition", "responsable": "Claude", "priorite": "haute", "statut": "fait", "echeance": "2026-11-01", "fichier": "docs/v4/acquisition/plan-mix-acquisition.md", "note": "Commit 661124b." },
    { "id": "T21", "titre": "Séance de 30 min : chiffres 2025 saisis dans le simulateur", "chantier": "acquisition", "responsable": "Agence", "priorite": "haute", "statut": "attente-client", "echeance": "2026-11-20", "fichier": "docs/v4/acquisition/simulateur.html", "note": "Demandes, offres, signatures, paniers, marge, capacité." },
    { "id": "T22", "titre": "Créer les comptes Google Ads et Microsoft Ads, relever les CPC", "chantier": "acquisition", "responsable": "Agence", "priorite": "moyenne", "statut": "a-faire", "echeance": "", "fichier": "docs/v4/acquisition/plan-mix-acquisition.md", "note": "Après la décision de budget." },
    { "id": "T23", "titre": "Liste des 30 premiers clients pour la campagne d'avis", "chantier": "acquisition", "responsable": "Client", "priorite": "haute", "statut": "attente-client", "echeance": "", "fichier": "docs/v4/seo/audit-seo.md", "note": "Dès que la fiche Google est active." },
    { "id": "T24", "titre": "Liste B2B palier 1 et premier courrier", "chantier": "acquisition", "responsable": "Agence", "priorite": "moyenne", "statut": "a-faire", "echeance": "", "fichier": "docs/v4/acquisition/plan-mix-acquisition.md", "note": "Courrier + appel, pas d'e-mail à froid (LCD art. 3)." },
    { "id": "T25", "titre": "Créer une page Facebook entreprise", "chantier": "acquisition", "responsable": "Client", "priorite": "basse", "statut": "a-faire", "echeance": "", "fichier": "docs/v2/dossier-client.md", "note": "Aujourd'hui : profil personnel." },

    { "id": "T30", "titre": "Plans du tableau de bord admin et maquette cliquable", "chantier": "admin", "responsable": "Claude", "priorite": "moyenne", "statut": "fait", "echeance": "2026-11-01", "fichier": "docs/v4/admin/plan-dashboard-admin.md", "note": "Commit d852ea2." },
    { "id": "T31", "titre": "Valider l'option A et l'abandon de Pipedrive (G1)", "chantier": "admin", "responsable": "Client", "priorite": "haute", "statut": "attente-client", "echeance": "", "fichier": "docs/v4/admin/plan-dashboard-admin.md", "note": "Bloque le MVP." },
    { "id": "T32", "titre": "Développer le MVP de l'admin", "chantier": "admin", "responsable": "Claude", "priorite": "moyenne", "statut": "a-faire", "echeance": "", "fichier": "docs/v4/admin/plan-dashboard-admin.md", "note": "≈ 20 jours estimés. Après G1 et G2." },

    { "id": "T40", "titre": "API PHP du formulaire et 16 workflows n8n", "chantier": "automatisation", "responsable": "Claude", "priorite": "haute", "statut": "fait", "echeance": "2026-10-31", "fichier": "docs/v2/automatisation.md", "note": "266 tests API, 33 contrôles workflows." },
    { "id": "T41", "titre": "Créer site/api/config.php sur le serveur (SMTP, secrets)", "chantier": "automatisation", "responsable": "Agence", "priorite": "haute", "statut": "a-faire", "echeance": "", "fichier": "docs/v2/automatisation.md", "note": "entreprise.nom = raison sociale complète (CO 954a)." },
    { "id": "T42", "titre": "Installer n8n et importer les workflows", "chantier": "automatisation", "responsable": "Agence", "priorite": "moyenne", "statut": "a-faire", "echeance": "", "fichier": "docs/v2/automatisation.md", "note": "À adapter si l'option A est retenue." },
    { "id": "T43", "titre": "Recette des 20 cas de bout en bout", "chantier": "automatisation", "responsable": "Claude", "priorite": "haute", "statut": "a-faire", "echeance": "", "fichier": "docs/v2/automatisation.md", "note": "Les workflows n'ont jamais tourné dans une vraie instance." },
    { "id": "T44", "titre": "WF03d : lire l'opposition avant chaque relance d'avis", "chantier": "automatisation", "responsable": "Claude", "priorite": "haute", "statut": "a-faire", "echeance": "", "fichier": "docs/v2/qa/relecture-juridique-copy.md", "note": "Bloquant LCD art. 3 al. 1 let. o." },
    { "id": "T45", "titre": "Configurer Umami et l'activer en production", "chantier": "automatisation", "responsable": "Agence", "priorite": "moyenne", "statut": "a-faire", "echeance": "", "fichier": "tools/build/donnees/config.json", "note": "" },

    { "id": "T50", "titre": "Relecture juridique interne (messages, politique, registre)", "chantier": "juridique", "responsable": "Claude", "priorite": "haute", "statut": "fait", "echeance": "2026-10-31", "fichier": "docs/v2/qa/relecture-juridique-copy.md", "note": "Commit 12eae1b." },
    { "id": "T51", "titre": "Envoyer les 8 points à l'avocat", "chantier": "juridique", "responsable": "Agence", "priorite": "haute", "statut": "a-faire", "echeance": "2026-11-27", "fichier": "docs/v2/qa/relecture-juridique-copy.md", "note": "" },
    { "id": "T52", "titre": "Mettre à jour la liste des prestataires de la politique", "chantier": "juridique", "responsable": "Claude", "priorite": "haute", "statut": "attente-client", "echeance": "", "fichier": "tools/build/page_autres.py", "note": "Hébergeur (C34), messagerie (V02), Pipedrive à retirer si option A." },
    { "id": "T53", "titre": "Envoyer les 17 lettres d'autorisation des logos", "chantier": "juridique", "responsable": "Client", "priorite": "haute", "statut": "a-faire", "echeance": "", "fichier": "docs/v2/logos-references.md", "note": "Lettres prêtes (§7, §9). Signées par un associé." },
    { "id": "T54", "titre": "Afficher le n° TVA dans les mentions légales", "chantier": "juridique", "responsable": "Claude", "priorite": "basse", "statut": "attente-client", "echeance": "", "fichier": "tools/build/page_autres.py", "note": "Numéro vérifié au registre IDE le 7.11.2026. Attend C35." },

    { "id": "T60", "titre": "19 illustrations libres, toujours légendées « Illustration »", "chantier": "contenus", "responsable": "Claude", "priorite": "moyenne", "statut": "fait", "echeance": "2026-10-31", "fichier": "docs/v3/credits-images.md", "note": "" },
    { "id": "T61", "titre": "Recherche publique sur la société et liste des infos à compléter", "chantier": "contenus", "responsable": "Claude", "priorite": "haute", "statut": "fait", "echeance": "2026-11-07", "fichier": "projet/infos-a-completer.md", "note": "" },
    { "id": "T62", "titre": "Envoyer le questionnaire client", "chantier": "contenus", "responsable": "Agence", "priorite": "haute", "statut": "a-faire", "echeance": "2026-11-10", "fichier": "projet/questionnaire-client.md", "note": "Bouton « Copier le questionnaire »." },
    { "id": "T63", "titre": "Shooting de 3 ou 4 chantiers en cours (dont peinture)", "chantier": "contenus", "responsable": "Client", "priorite": "haute", "statut": "attente-client", "echeance": "", "fichier": "docs/v2/architecture-cro.md", "note": "Aucune photo de peinture aujourd'hui." },
    { "id": "T64", "titre": "Recevoir photos récentes, originaux et témoignages", "chantier": "contenus", "responsable": "Client", "priorite": "moyenne", "statut": "attente-client", "echeance": "", "fichier": "projet/infos-a-completer.md", "note": "Voir la liste des assets." },
    { "id": "T65", "titre": "Rédiger les 4 premières fiches projets", "chantier": "contenus", "responsable": "Claude", "priorite": "moyenne", "statut": "a-faire", "echeance": "", "fichier": "docs/v4/seo/audit-seo.md", "note": "Après les accords (C22, C25)." },

    { "id": "T70", "titre": "Passer le dépôt GitHub en privé", "chantier": "deploiement", "responsable": "Agence", "priorite": "haute", "statut": "a-faire", "echeance": "2026-11-09", "fichier": "HANDOFF.md", "note": "Dépôt public et indexé : identité du client, noms des associés." },
    { "id": "T71", "titre": "Changer le mot de passe FTP", "chantier": "deploiement", "responsable": "Agence", "priorite": "haute", "statut": "a-faire", "echeance": "2026-11-09", "fichier": "HANDOFF.md", "note": "Il a circulé dans une conversation." },
    { "id": "T72", "titre": "Déployer la version de validation dans res/andy-construct-v3/", "chantier": "deploiement", "responsable": "Agence", "priorite": "haute", "statut": "a-faire", "echeance": "2026-11-13", "fichier": "livrables/andy-construct-v3-validation.zip", "note": "Port FTP 21 bloqué depuis le cloud : gestionnaire de fichiers." },
    { "id": "T73", "titre": "Vérifier l'hébergeur : PHP 8.1+, MariaDB, pays (C34, G2)", "chantier": "deploiement", "responsable": "Agence", "priorite": "haute", "statut": "attente-client", "echeance": "", "fichier": "docs/v4/admin/plan-dashboard-admin.md", "note": "Actuel : Kreativ Media, serveurs METANET AG (Suisse)." },
    { "id": "T74", "titre": "Archives v3 (validation et production)", "chantier": "deploiement", "responsable": "Claude", "priorite": "moyenne", "statut": "fait", "echeance": "2026-11-01", "fichier": "livrables/", "note": "Commit 8ba3dd6." },
    { "id": "T75", "titre": "Mise en production, 301 sur l'hôte réel, HSTS", "chantier": "deploiement", "responsable": "Claude", "priorite": "moyenne", "statut": "a-faire", "echeance": "", "fichier": "docs/v4/seo/audit-seo.md", "note": "Plan J-7 à J+90." }
  ],

  "decisions": [
    { "id": "D-BUDGET", "titre": "Budget mensuel d'acquisition", "contexte": "Dépense tout compris (médias, outils, agence). Engagement de 6 mois avant de juger.", "options": ["A, socle sans publicité : ≈ CHF 1'749/mois", "D, plateformes et partenariats : ≈ CHF 2'472/mois", "B, socle + Google Ads : ≈ CHF 3'613/mois", "C, socle + Ads + B2B + simap : ≈ CHF 3'752/mois"], "reco": 3, "recommandation": "C, recalage à M3.", "bloque": "Google Ads, B2B, simap", "statut": "a-prendre", "source": "docs/v4/acquisition/plan-mix-acquisition.md" },
    { "id": "D-C16", "titre": "Nom de la 4e page (C16)", "contexte": "« Isotherme » évoque les chambres froides. « Isolante » correspond au besoin réel (garage, cave, combles).", "options": ["Cloisons isothermes (actuel)", "Cloisons isolantes, URL cloisons-isolantes.html + 301"], "reco": 1, "recommandation": "Cloisons isolantes, avant la mise en ligne.", "bloque": "Menu, URL, SEO", "statut": "a-prendre", "source": "docs/v4/seo/audit-seo.md" },
    { "id": "D-SUIVI", "titre": "Outil de suivi des demandes", "contexte": "Aujourd'hui l'API n'a aucune base : une demande n'existe que dans les e-mails.", "options": ["A, admin maison (PHP + MariaDB, gestion.andyconstruct.ch)", "Pipedrive + n8n", "Brevo CRM"], "reco": 0, "recommandation": "A. Pipedrive non souscrit, n8n branché sur l'admin.", "bloque": "MVP admin, politique de confidentialité", "statut": "a-prendre", "source": "docs/v4/admin/plan-dashboard-admin.md" },
    { "id": "D-HEBERG", "titre": "Hébergeur de production", "contexte": "Actuel : Kreativ Media (serveurs METANET AG, Suisse). PHP 8.1 et MariaDB à vérifier.", "options": ["Rester chez l'hébergeur actuel si PHP 8.1 + MariaDB", "Infomaniak (Suisse)", "Variante A′ sur le VPS n8n"], "reco": 0, "recommandation": "Vérifier l'actuel d'abord, sinon Infomaniak.", "bloque": "Mentions (C34), API, admin", "statut": "a-prendre", "source": "docs/v4/admin/plan-dashboard-admin.md" },
    { "id": "D-LOGOS", "titre": "Logos des références", "contexte": "17 logos couleur « à autoriser », 0 accord. Collectivités et OMC : refus probable.", "options": ["Envoyer les 17 lettres maintenant", "Lancer avec les noms en texte, logos au fil des accords"], "reco": -1, "recommandation": "Les deux : lettres cette semaine, lancement avec les noms. De Grisogono : nom seul.", "bloque": "Mur de logos en production", "statut": "a-prendre", "source": "docs/v2/logos-references.md" },
    { "id": "D-VIDEO", "titre": "Média du héro", "contexte": "Une vidéo de banque d'images passerait pour un chantier d'Andy Construct.", "options": ["Vraie photo de chantier (A)", "Vidéo d'ambiance libre (B, ?flag=hero-media:b)"], "reco": 0, "recommandation": "Vraie photo (A).", "bloque": "Rien", "statut": "a-prendre", "source": "HANDOFF.md" },
    { "id": "D-ZONE", "titre": "Particuliers hors Genève (C21, D8)", "contexte": "Zone validée : toute la Suisse romande. Preuves publiques : GE et La Côte.", "options": ["Particuliers partout en Romandie", "Particuliers à Genève et La Côte, acoustique et B2B partout"], "reco": 1, "recommandation": "Genève et La Côte pour les particuliers.", "bloque": "Zone de la fiche Google, ciblage Ads", "statut": "a-prendre", "source": "docs/v4/acquisition/plan-mix-acquisition.md" },
    { "id": "D-MAIL", "titre": "Adresse e-mail publique (C30)", "contexte": "Le domaine a déjà un serveur de messagerie, un SPF et un DMARC.", "options": ["contact@andyconstruct.ch", "andy.construct@bluewin.ch (actuel)"], "reco": 0, "recommandation": "contact@andyconstruct.ch, bluewin en redirection.", "bloque": "Annuaires, fiche Google, politique", "statut": "a-prendre", "source": "docs/v2/copy-deck.md" },
    { "id": "D-CONSENT", "titre": "Bandeau de consentement", "contexte": "Sans lui : ni gclid ni conversions importées dans Google Ads.", "options": ["Oui dès M1, « Refuser » aussi visible qu'« Accepter »", "Non, site sans cookie"], "reco": 0, "recommandation": "Oui dès M1.", "bloque": "Mesure Google Ads, politique", "statut": "a-prendre", "source": "docs/v4/acquisition/plan-mix-acquisition.md" },
    { "id": "D-PHOTOS", "titre": "19 photos hors offre (plafonds tendus, métalliques)", "contexte": "Exclues en production aujourd'hui.", "options": ["Retirer", "Regrouper sous « Autres réalisations (hors offre actuelle) »"], "reco": 0, "recommandation": "Retirer tant qu'il n'y a pas de photos récentes.", "bloque": "Portfolio", "statut": "a-prendre", "source": "docs/v2/copy-deck.md" },
    { "id": "D-HORSOFFRE", "titre": "Prestations hors des 4 services", "contexte": "Tissu tendu, cadres acoustiques, cloisons alu : mis en avant sur LinkedIn et local.ch.", "options": ["Encore proposées", "Plus proposées : retirer des annuaires"], "reco": -1, "recommandation": "À trancher par les associés.", "bloque": "Annuaires, LinkedIn", "statut": "a-prendre", "source": "docs/v2/dossier-client.md" },
    { "id": "D-SIMAP", "titre": "Marchés publics", "contexte": "Environ 12 h par dossier. Taux d'adjudication supposé : 15 %.", "options": ["6 dossiers choisis par an", "Pas de marchés publics en année 1"], "reco": 0, "recommandation": "6 dossiers par an, lots compatibles avec la capacité.", "bloque": "Combinaison C", "statut": "a-prendre", "source": "docs/v4/acquisition/plan-mix-acquisition.md" },
    { "id": "D-GPG", "titre": "Adhésion à Gypserie Peinture Genève", "contexte": "Signal de confiance et lien local.", "options": ["Oui", "Non"], "reco": -1, "recommandation": "Selon le coût.", "bloque": "Rien", "statut": "a-prendre", "source": "HANDOFF.md" }
  ],

  /* Questionnaire client : questions de validation, proposition préremplie. */
  "questionnaire": [
    { "id": "Q01", "theme": "Identité et mentions légales", "question": "Pouvez-vous confirmer la raison sociale exacte à faire figurer dans les mentions légales ?", "proposition": "« Andy Construct, Chanton & Cie », société en nom collectif, IDE CHE-113.706.162, siège Route des Acacias 48, 1227 Carouge. La mention « Sàrl » de l'ancien site disparaît.", "source": "Zefix, registre IDE (7.11.2026)", "ref": "I-1", "statut": "a-envoyer" },
    { "id": "Q02", "theme": "Identité et mentions légales", "question": "Acceptez-vous que les deux associés soient nommés dans les mentions légales et sur la page « L'entreprise » ?", "proposition": "Adnan Bajrami et Caroline Chanton Bajrami, avec le rôle de chacun (à nous indiquer).", "source": "FOSC du 02.05.2023", "ref": "C10", "statut": "a-envoyer" },
    { "id": "Q03", "theme": "Identité et mentions légales", "question": "Pouvons-nous afficher votre numéro de TVA dans les mentions légales ?", "proposition": "CHE-113.706.162 TVA (inscrit au registre depuis le 01.07.2008).", "source": "Registre IDE, service public UID", "ref": "C35", "statut": "a-envoyer" },
    { "id": "Q04", "theme": "Identité et mentions légales", "question": "La Route des Acacias 48 est-elle un bureau où l'on peut vous rencontrer, ou une adresse de domiciliation ?", "proposition": "Adresse affichée dans les mentions légales ; masquée sur la fiche Google (zone desservie) s'il n'y a pas d'accueil. L'ancienne adresse de Chêne-Bourg n'est publiée nulle part.", "source": "Moneyhouse (92 autres entreprises à cette adresse)", "ref": "C29", "statut": "a-envoyer" },
    { "id": "Q05", "theme": "Identité et mentions légales", "question": "D'où vient le nom « Andy » ? Souhaitez-vous le raconter en une ligne ?", "proposition": "Une phrase sur la page « L'entreprise » si vous le souhaitez, sinon rien.", "source": "Aucune source publique", "ref": "C36", "statut": "a-envoyer" },

    { "id": "Q06", "theme": "Site, domaine et e-mail", "question": "Confirmez-vous le nom de domaine du nouveau site ?", "proposition": "https://www.andyconstruct.ch (votre domaine depuis le 01.03.2010). Les anciennes adresses sont redirigées.", "source": "RDAP nic.ch, audit SEO §4", "ref": "", "statut": "a-envoyer" },
    { "id": "Q07", "theme": "Site, domaine et e-mail", "question": "Quelle adresse e-mail voulez-vous afficher sur le site et dans les annuaires ?", "proposition": "contact@andyconstruct.ch. Votre domaine reçoit déjà des e-mails ; l'adresse bluewin peut rester en redirection.", "source": "DNS du domaine (MX, SPF, DMARC)", "ref": "C30", "statut": "a-envoyer" },
    { "id": "Q08", "theme": "Site, domaine et e-mail", "question": "Qui héberge le site aujourd'hui, et pouvons-nous y vérifier la version de PHP et la base de données ?", "proposition": "Garder l'hébergeur actuel (Kreativ Media, Suisse) s'il offre PHP 8.1 et MariaDB ; sinon Infomaniak (Suisse).", "source": "DNS et adresse IP du serveur", "ref": "C34", "statut": "a-envoyer" },
    { "id": "Q09", "theme": "Site, domaine et e-mail", "question": "Pour le haut de la page d'accueil, préférez-vous une vraie photo de chantier ou une vidéo d'ambiance ?", "proposition": "Une vraie photo : une vidéo de banque d'images pourrait passer pour l'un de vos chantiers.", "source": "Direction artistique v3", "ref": "", "statut": "a-envoyer" },

    { "id": "Q10", "theme": "Contact et horaires", "question": "Quel numéro mettre en avant ?", "proposition": "Le fixe +41 22 771 20 15 en principal ; le mobile présenté « sur les chantiers ». La mention fax disparaît.", "source": "local.ch, search.ch, ancien site", "ref": "C30", "statut": "a-envoyer" },
    { "id": "Q11", "theme": "Contact et horaires", "question": "Vos horaires sont-ils exacts, et quelqu'un répond-il au fixe pendant ces heures ?", "proposition": "Du lundi au vendredi, de 7 h à 18 h.", "source": "local.ch, search.ch", "ref": "C03", "statut": "a-envoyer" },
    { "id": "Q12", "theme": "Contact et horaires", "question": "Dans quel délai pouvez-vous toujours rappeler une demande ?", "proposition": "« Le jour même ou le jour ouvrable suivant ».", "source": "Copy deck §R", "ref": "C01", "statut": "a-envoyer" },
    { "id": "Q13", "theme": "Contact et horaires", "question": "Qui rappelle les demandes ? Peut-on indiquer son prénom ?", "proposition": "Le prénom de l'associé qui rappelle, sur la page de remerciement et dans les e-mails.", "source": "Copy deck §R", "ref": "C09", "statut": "a-envoyer" },

    { "id": "Q14", "theme": "Services et zone", "question": "Acceptez-vous le nom « Cloisons isolantes » pour votre 4e service ?", "proposition": "« Cloisons isolantes » (adresse cloisons-isolantes.html). « Isotherme » évoque surtout les chambres froides.", "source": "Audit SEO v4 §1.2", "ref": "C16", "statut": "a-envoyer" },
    { "id": "Q15", "theme": "Services et zone", "question": "Jusqu'où vous déplacez-vous pour les particuliers ?", "proposition": "Particuliers : Genève et La Côte. Acoustique, régies, architectes et communes : toute la Suisse romande.", "source": "Plan de mix §7.2", "ref": "C21", "statut": "a-envoyer" },
    { "id": "Q16", "theme": "Services et zone", "question": "Le tissu tendu, les cadres acoustiques et les cloisons mobiles font-ils encore partie de votre offre ?", "proposition": "Ne plus les mettre en avant ; aligner LinkedIn et local.ch sur les 4 services.", "source": "LinkedIn, local.ch, ancien site", "ref": "P1-8", "statut": "a-envoyer" },
    { "id": "Q17", "theme": "Services et zone", "question": "La visite et le devis sont-ils gratuits et sans engagement, dans toute la zone ?", "proposition": "« Visite et devis gratuits, sans engagement ».", "source": "Copy deck §R", "ref": "C02", "statut": "a-envoyer" },
    { "id": "Q18", "theme": "Services et zone", "question": "Acceptez-vous les petits chantiers (une pièce, une cloison) ? Avez-vous un montant minimum ?", "proposition": "Oui pour une pièce, avec un montant minimum que vous fixez.", "source": "Copy deck §R", "ref": "C04", "statut": "a-envoyer" },
    { "id": "Q19", "theme": "Services et zone", "question": "Pouvez-vous nous donner des fourchettes de prix pour 4 cas types ?", "proposition": "Cloison de 10 m², peinture d'un 3,5 pièces, doublage acoustique d'un mur de 12 m², cloison isolante de 10 m². Sans chiffres, nous publions seulement les facteurs de prix.", "source": "Copy deck §R", "ref": "C31", "statut": "a-envoyer" },
    { "id": "Q20", "theme": "Services et zone", "question": "Réalisez-vous vous-mêmes les 4 métiers ?", "proposition": "« Un seul interlocuteur, de la pose des plaques à la dernière couche ».", "source": "Copy deck §R", "ref": "C05", "statut": "a-envoyer" },

    { "id": "Q21", "theme": "Références et preuves", "question": "Pour chacune des 18 références : année, travaux réalisés et accord pour citer le nom ?", "proposition": "Nous préparons les lettres d'autorisation. Sans accord, l'OMC n'apparaît pas. Merci de confirmer que l'hôtel de Chavannes-de-Bogis est l'actuel Everness.", "source": "Ancien site, logos-references.md", "ref": "C22", "statut": "a-envoyer" },
    { "id": "Q22", "theme": "Références et preuves", "question": "Êtes-vous membre du GGE ? Depuis quand ?", "proposition": "« Membre du GGE » sur la page « L'entreprise » : l'annuaire du GGE vous liste parmi ses membres.", "source": "gge.ch", "ref": "C11", "statut": "a-envoyer" },
    { "id": "Q23", "theme": "Références et preuves", "question": "Pouvez-vous nous transmettre votre attestation d'assurance RC et vos attestations AVS, LPP, impôts et convention collective ?", "proposition": "Mention « attestations sur demande » pour les professionnels et les appels d'offres.", "source": "Copy deck §R", "ref": "C12, C13", "statut": "a-envoyer" },
    { "id": "Q24", "theme": "Références et preuves", "question": "Combien de personnes travaillent dans l'entreprise ?", "proposition": "Le chiffre exact, s'il peut être publié. Les annuaires se contredisent (2-10 et 1-2).", "source": "LinkedIn, SITG 2021", "ref": "C24", "statut": "a-envoyer" },
    { "id": "Q25", "theme": "Références et preuves", "question": "Quels clients accepteraient deux ou trois phrases de témoignage signées ?", "proposition": "2 ou 3 témoignages avec accord écrit (lettre type fournie).", "source": "Copy deck §R", "ref": "C44", "statut": "a-envoyer" },

    { "id": "Q26", "theme": "Photos et contenus", "question": "Pouvez-vous nous envoyer des photos de 5 à 10 chantiers récents (2017-2026), avec lieu, année et prestation ?", "proposition": "Originaux en pleine définition, envoyés par un lien de partage.", "source": "Dernière photo publique : février 2016", "ref": "C39", "statut": "a-envoyer" },
    { "id": "Q27", "theme": "Photos et contenus", "question": "Avez-vous des photos de chantiers de peinture ?", "proposition": "Sinon, une séance photo sur 3 ou 4 chantiers en cours (peinture, cloison isolante, acoustique, un avant/après).", "source": "Architecture CRO §8.8", "ref": "C40", "statut": "a-envoyer" },
    { "id": "Q28", "theme": "Photos et contenus", "question": "Pouvez-vous nous fournir votre logo en format vectoriel ?", "proposition": "Fichier SVG, AI, EPS ou PDF vectoriel du logo rouge actuel.", "source": "Dépôt : seulement PNG et WebP", "ref": "", "statut": "a-envoyer" },
    { "id": "Q29", "theme": "Photos et contenus", "question": "Avez-vous les originaux des 7 photos avant/après de l'ancien site ?", "proposition": "Les originaux, avec le lieu et la prestation de chaque paire.", "source": "Ancien site (800 px)", "ref": "C26", "statut": "a-envoyer" },
    { "id": "Q30", "theme": "Photos et contenus", "question": "Pour les photos déjà retenues : technique, type de bâtiment et commune de chaque chantier ?", "proposition": "Légendes neutres (ce que montre la photo) tant que nous n'avons pas ces informations.", "source": "Copy deck §R", "ref": "C25", "statut": "a-envoyer" },

    { "id": "Q31", "theme": "Accès et outils", "question": "Votre fiche Google existe-t-elle, et qui y a accès ?", "proposition": "Vous restez propriétaires ; Harbor Digital est ajoutée comme gestionnaire.", "source": "Fiche non consultable de notre côté", "ref": "C37", "statut": "a-envoyer" },
    { "id": "Q32", "theme": "Accès et outils", "question": "Pouvez-vous nous donner accès à la zone DNS de votre domaine ?", "proposition": "Un accès au compte Kreativ Media, ou l'ajout d'un enregistrement TXT par vos soins, pour la Search Console.", "source": "Serveurs DNS kreativmedia.ch", "ref": "", "statut": "a-envoyer" },
    { "id": "Q33", "theme": "Accès et outils", "question": "Qui administre la page LinkedIn et votre inscription local.ch / search.ch ?", "proposition": "Un accès gestionnaire pour aligner texte, catégories, logo et lien sur le nouveau site.", "source": "LinkedIn, local.ch Premium", "ref": "", "statut": "a-envoyer" },
    { "id": "Q34", "theme": "Accès et outils", "question": "Quel logiciel utilisez-vous pour vos offres et factures ?", "proposition": "Le nommer dès maintenant, pour éviter une double saisie plus tard.", "source": "Plan de l'admin G11", "ref": "G11", "statut": "a-envoyer" },
    { "id": "Q35", "theme": "Accès et outils", "question": "Validez-vous un outil de suivi des demandes développé pour vous plutôt qu'un abonnement Pipedrive ?", "proposition": "Admin sur gestion.andyconstruct.ch, sans abonnement CRM.", "source": "Plan de l'admin §2.3", "ref": "G1", "statut": "a-envoyer" },

    { "id": "Q36", "theme": "Budget et organisation", "question": "Quel budget mensuel d'acquisition retenez-vous, et pour combien de temps ?", "proposition": "Environ CHF 3'750 par mois tout compris (combinaison C), engagement de 6 mois, premier bilan à 3 mois.", "source": "Plan de mix §3.2", "ref": "", "statut": "a-envoyer" },
    { "id": "Q37", "theme": "Budget et organisation", "question": "Pouvons-nous fixer 30 minutes pour vos chiffres 2025 ?", "proposition": "Demandes, offres, signatures, panier par type de client, marge brute, capacité, heures disponibles.", "source": "Plan de mix §7.1", "ref": "", "statut": "a-envoyer" },
    { "id": "Q38", "theme": "Budget et organisation", "question": "Acceptez-vous un appel de tri de 10 minutes avant chaque visite ?", "proposition": "Visite réservée aux demandes prioritaires ; c'est le temps des associés qui limite le volume.", "source": "Plan de mix §1", "ref": "", "statut": "a-envoyer" },
    { "id": "Q39", "theme": "Budget et organisation", "question": "Acceptez-vous un bandeau de consentement aux cookies pour mesurer Google Ads ?", "proposition": "Un bandeau sobre dès le premier mois, « Refuser » aussi visible qu'« Accepter ».", "source": "Plan de mix §7.2", "ref": "", "statut": "a-envoyer" },
    { "id": "Q40", "theme": "Budget et organisation", "question": "Souhaitez-vous déposer des offres pour des marchés publics ?", "proposition": "Environ 6 dossiers choisis par an, sur des lots à votre mesure.", "source": "Plan de mix §7.2", "ref": "", "statut": "a-envoyer" }
  ],

  /* Infos à compléter (détail : projet/infos-a-completer.md). */
  "infos": [
    { "id": "I01", "section": "Identité légale", "info": "Raison sociale", "valeur": "Andy Construct, Chanton & Cie", "source": "Zefix, registre IDE", "statut": "verifie", "usage": "Mentions, confidentialité, accusés", "fournisseur": "Registre", "ecart": "Ancien site : « Sàrl »" },
    { "id": "I02", "section": "Identité légale", "info": "Forme juridique", "valeur": "Société en nom collectif", "source": "Zefix", "statut": "verifie", "usage": "Mentions", "fournisseur": "Registre", "ecart": "" },
    { "id": "I03", "section": "Identité légale", "info": "IDE et n° RC", "valeur": "CHE-113.706.162 · CH-660-1539007-3", "source": "Zefix", "statut": "verifie", "usage": "Mentions, lettres B2B", "fournisseur": "Registre", "ecart": "" },
    { "id": "I04", "section": "Identité légale", "info": "N° TVA", "valeur": "CHE-113.706.162 TVA, actif depuis 01.07.2008", "source": "Registre IDE (7.11.2026)", "statut": "verifie", "usage": "Mentions (après C35)", "fournisseur": "Registre ; accord client", "ecart": "" },
    { "id": "I05", "section": "Identité légale", "info": "Siège", "valeur": "Route des Acacias 48, 1227 Carouge GE", "source": "Zefix", "statut": "verifie", "usage": "Mentions, NAP", "fournisseur": "Registre", "ecart": "8 annuaires au moins : Chêne-Bourg" },
    { "id": "I06", "section": "Identité légale", "info": "Accueil sur place à Carouge", "valeur": "92 autres entreprises à l'adresse", "source": "Moneyhouse", "statut": "a-confirmer", "usage": "Fiche Google", "fournisseur": "Client (C29)", "ecart": "" },
    { "id": "I07", "section": "Identité légale", "info": "Associés publiés", "valeur": "Adnan Bajrami, Caroline Chanton Bajrami", "source": "FOSC 02.05.2023", "statut": "a-confirmer", "usage": "Mentions, Entreprise", "fournisseur": "Client (C10)", "ecart": "" },
    { "id": "I08", "section": "Identité légale", "info": "Hébergeur de production", "valeur": "Actuel : Kreativ Media / METANET AG (Suisse)", "source": "DNS, IP", "statut": "a-confirmer", "usage": "Mentions, confidentialité", "fournisseur": "Client (C34)", "ecart": "" },
    { "id": "I09", "section": "Identité légale", "info": "Fournisseur de messagerie", "valeur": "MX mail.andyconstruct.ch ; bluewin utilisé", "source": "DNS", "statut": "a-confirmer", "usage": "Confidentialité", "fournisseur": "Client (V02)", "ecart": "" },
    { "id": "I10", "section": "Identité légale", "info": "Durée des journaux de l'hébergeur", "valeur": "", "source": "", "statut": "manquant", "usage": "Confidentialité", "fournisseur": "Hébergeur", "ecart": "" },
    { "id": "I11", "section": "Identité légale", "info": "Pays de l'agence", "valeur": "", "source": "", "statut": "manquant", "usage": "Confidentialité", "fournisseur": "Agence", "ecart": "" },
    { "id": "I12", "section": "Identité légale", "info": "Assurance RC", "valeur": "", "source": "", "statut": "manquant", "usage": "Entreprise, professionnels", "fournisseur": "Client (C12)", "ecart": "" },
    { "id": "I13", "section": "Identité légale", "info": "Attestations AVS, LPP, impôts, CCT", "valeur": "", "source": "", "statut": "manquant", "usage": "Professionnels, simap", "fournisseur": "Client (C13)", "ecart": "" },
    { "id": "I14", "section": "Identité légale", "info": "Membre du GGE", "valeur": "Listé « Entreprises membres du GGE »", "source": "gge.ch", "statut": "a-confirmer", "usage": "Entreprise, JSON-LD", "fournisseur": "Client (C11)", "ecart": "" },
    { "id": "I15", "section": "Contact", "info": "Domaine", "valeur": "andyconstruct.ch (depuis 01.03.2010)", "source": "RDAP nic.ch", "statut": "verifie", "usage": "Site, e-mail", "fournisseur": "", "ecart": "" },
    { "id": "I16", "section": "Contact", "info": "E-mail public", "valeur": "bluewin aujourd'hui ; contact@ proposé", "source": "Annuaires, DNS", "statut": "a-confirmer", "usage": "Partout", "fournisseur": "Client (C30)", "ecart": "Domaine prêt, bluewin partout" },
    { "id": "I17", "section": "Contact", "info": "Fixe et mobile", "valeur": "+41 22 771 20 15 · +41 78 631 14 34", "source": "local.ch, search.ch", "statut": "verifie", "usage": "Partout", "fournisseur": "", "ecart": "GGE : mobile seul ; ancien site : « T+F »" },
    { "id": "I18", "section": "Contact", "info": "Horaires", "valeur": "Lun-ven 7 h-18 h", "source": "local.ch", "statut": "a-confirmer", "usage": "En-tête, fiche Google", "fournisseur": "Client (C03)", "ecart": "" },
    { "id": "I19", "section": "Contact", "info": "Délai de rappel", "valeur": "Jour même ou jour ouvrable suivant", "source": "Proposition", "statut": "a-confirmer", "usage": "Formulaire, merci", "fournisseur": "Client (C01)", "ecart": "" },
    { "id": "I20", "section": "Services et zone", "info": "Nom du 4e service", "valeur": "Cloisons isolantes (proposé)", "source": "Audit SEO", "statut": "a-confirmer", "usage": "Menu, URL", "fournisseur": "Client (C16)", "ecart": "Registre : « thermiques » ; site : « isothermes »" },
    { "id": "I21", "section": "Services et zone", "info": "Prestations hors offre", "valeur": "Tissu tendu, cadres acoustiques, cloisons alu", "source": "LinkedIn, local.ch", "statut": "a-confirmer", "usage": "Annuaires", "fournisseur": "Client (P1-8)", "ecart": "Absents des 4 services" },
    { "id": "I22", "section": "Services et zone", "info": "Zone des particuliers", "valeur": "Suisse romande validée ; preuves GE et La Côte", "source": "Dossier client §2.5", "statut": "a-confirmer", "usage": "FAQ, fiche Google, Ads", "fournisseur": "Client (C21)", "ecart": "" },
    { "id": "I23", "section": "Services et zone", "info": "Prix (4 cas types)", "valeur": "", "source": "", "statut": "manquant", "usage": "FAQ, page prix", "fournisseur": "Client (C31)", "ecart": "" },
    { "id": "I24", "section": "Services et zone", "info": "Effectif", "valeur": "2-10 (LinkedIn) / 1-2 (SITG 2021)", "source": "LinkedIn, SITG", "statut": "manquant", "usage": "Entreprise", "fournisseur": "Client (C24)", "ecart": "Sources contradictoires" },
    { "id": "I25", "section": "Preuves", "info": "Accords logos", "valeur": "0 sur 17", "source": "logos.json", "statut": "manquant", "usage": "Production", "fournisseur": "Client", "ecart": "" },
    { "id": "I26", "section": "Preuves", "info": "Années et prestations des 18 références", "valeur": "", "source": "", "statut": "manquant", "usage": "Plaquette, fiches projets", "fournisseur": "Client (C22)", "ecart": "" },
    { "id": "I27", "section": "Preuves", "info": "Photos récentes", "valeur": "Dernière photo publique : 02.2016", "source": "EXIF", "statut": "manquant", "usage": "Réalisations", "fournisseur": "Client (C39)", "ecart": "" },
    { "id": "I28", "section": "Preuves", "info": "Avis clients", "valeur": "0 (local.ch, search.ch, Yelp)", "source": "Relevé 7.11.2026", "statut": "verifie", "usage": "Fiche Google, accueil", "fournisseur": "Clients", "ecart": "" },
    { "id": "I29", "section": "Accès", "info": "Fiche Google", "valeur": "", "source": "", "statut": "manquant", "usage": "SEO local", "fournisseur": "Client (C37)", "ecart": "" },
    { "id": "I30", "section": "Accès", "info": "DNS (Kreativ Media)", "valeur": "NS kreativmedia.ch", "source": "DNS", "statut": "manquant", "usage": "Search Console, e-mail", "fournisseur": "Client", "ecart": "" },
    { "id": "I31", "section": "Accès", "info": "LinkedIn, local.ch, annuaires", "valeur": "", "source": "", "statut": "manquant", "usage": "NAP", "fournisseur": "Client", "ecart": "search.ch : catégorie « protection auditive »" }
  ],

  "assets": [
    { "id": "A01", "asset": "Photos de chantiers récentes", "detail": "5 à 10 chantiers 2017-2026, originaux HD, lieu, année, prestation", "usage": "Réalisations, fiche Google", "fournisseur": "Client", "priorite": "haute", "statut": "a-demander" },
    { "id": "A02", "asset": "Photos de peinture", "detail": "Aucune aujourd'hui", "usage": "Page peinture", "fournisseur": "Client", "priorite": "haute", "statut": "a-demander" },
    { "id": "A03", "asset": "Séance photo de 3-4 chantiers en cours", "detail": "Peinture, cloison isolante, acoustique, un avant/après", "usage": "Héro, services", "fournisseur": "Client + photographe", "priorite": "haute", "statut": "a-demander" },
    { "id": "A04", "asset": "Originaux des 7 avant/après", "detail": "En ligne en 800 px seulement", "usage": "Accueil, réalisations", "fournisseur": "Client", "priorite": "moyenne", "statut": "a-demander" },
    { "id": "A05", "asset": "Logo vectoriel", "detail": "Le dépôt n'a que PNG et WebP", "usage": "Site, fiche Google, plaquette", "fournisseur": "Client", "priorite": "moyenne", "statut": "a-demander" },
    { "id": "A06", "asset": "Portraits des associés", "detail": "Si C10 accepté", "usage": "Entreprise, fiche Google", "fournisseur": "Client", "priorite": "basse", "statut": "a-demander" },
    { "id": "A07", "asset": "Attestations RC, AVS, LPP, impôts, CCT", "detail": "PDF récents", "usage": "Professionnels, simap", "fournisseur": "Client", "priorite": "moyenne", "statut": "a-demander" },
    { "id": "A08", "asset": "Accords logos signés", "detail": "17 lettres prêtes", "usage": "Mur de logos en production", "fournisseur": "Client", "priorite": "haute", "statut": "a-demander" },
    { "id": "A09", "asset": "Accords photos", "detail": "Poseur visible (IMG_5922), client au slogan (P1000435)", "usage": "Légendes", "fournisseur": "Client", "priorite": "moyenne", "statut": "a-demander" },
    { "id": "A10", "asset": "Témoignages signés", "detail": "2 ou 3, lettre type §7.2", "usage": "Accueil, réalisations", "fournisseur": "Client", "priorite": "moyenne", "statut": "a-demander" },
    { "id": "A11", "asset": "Liste des clients depuis 2007", "detail": "Coordonnées, régies comprises", "usage": "Avis, courrier aux clients", "fournisseur": "Client", "priorite": "haute", "statut": "a-demander" },
    { "id": "A12", "asset": "Chiffres 2025", "detail": "Demandes, offres, signatures, paniers, marge, capacité", "usage": "Simulateur, budget", "fournisseur": "Client", "priorite": "haute", "statut": "a-demander" },
    { "id": "A13", "asset": "Logos vectoriels des références", "detail": "HEAD, J. Safra Sarasin, Energestion, Dipan, Harmonie Nautique", "usage": "Mur de logos", "fournisseur": "Références", "priorite": "basse", "statut": "a-demander" },
    { "id": "A14", "asset": "Anciens textes et plaquettes", "detail": "Avant 2017", "usage": "Page Entreprise", "fournisseur": "Client", "priorite": "basse", "statut": "a-demander" }
  ],

  "juridique": [
    { "id": "J01", "sujet": "Mentions légales", "base": "CO 954a ; LCD art. 3 al. 1 let. s (à valider par l'avocat)", "statut": "a-completer", "action": "Page prête. Manquent : hébergeur (C34), associés (C10), TVA (C35, numéro vérifié).", "fichier": "tools/build/page_autres.py" },
    { "id": "J02", "sujet": "Politique de confidentialité", "base": "nLPD art. 19", "statut": "a-completer", "action": "Texte relu et intégré. Manquent : hébergeur, messagerie, durée Umami, pays de l'agence. Retirer Pipedrive si option A.", "fichier": "docs/v2/automatisation.md" },
    { "id": "J03", "sujet": "Registre des activités de traitement", "base": "nLPD art. 12", "statut": "pret", "action": "Tenu, même si l'OPDo en dispense probablement.", "fichier": "docs/v2/automatisation.md" },
    { "id": "J04", "sujet": "Messages automatiques et opposition", "base": "LCD art. 3 al. 1 let. o", "statut": "bloque", "action": "WF03d doit lire l'opposition avant J+9, J+14 et le SMS.", "fichier": "docs/v2/qa/relecture-juridique-copy.md" },
    { "id": "J05", "sujet": "Prospection B2B", "base": "LCD art. 3 al. 1 let. o et u", "statut": "pret", "action": "Courrier et appel, pas d'e-mail à froid, astérisque des annuaires respecté.", "fichier": "docs/v2/strategie-acquisition.md" },
    { "id": "J06", "sujet": "Logos des collectivités", "base": "LPAP art. 8 et 10", "statut": "bloque", "action": "Ville de Genève, Collonge-Bellerive, Plan-les-Ouates, Alhambra : autorisation écrite. Refus probable.", "fichier": "docs/v2/logos-references.md" },
    { "id": "J07", "sujet": "Nom et logo de l'OMC", "base": "Convention de Paris art. 6ter ; LPNE", "statut": "bloque", "action": "Accord même pour le nom. Retirée en production.", "fichier": "docs/v2/logos-references.md" },
    { "id": "J08", "sujet": "Marques privées (logos et noms)", "base": "Droit des marques ; LCD", "statut": "a-faire", "action": "12 lettres d'autorisation. De Grisogono : nom seul.", "fichier": "docs/v2/logos-references.md" },
    { "id": "J09", "sujet": "Droit des défauts (contrats depuis le 1.1.2026)", "base": "CO, révision 2026 ; SIA 118", "statut": "a-faire", "action": "Textes I.8 et Q.3 marqués « À vérifier » (V01). Avocat.", "fichier": "docs/v2/copy-deck.md" },
    { "id": "J10", "sujet": "Droits d'auteur sur textes et photos", "base": "LDA", "statut": "a-faire", "action": "Cession écrite agence → client ; accord des auteurs des photos.", "fichier": "docs/v2/qa/relecture-juridique-copy.md" },
    { "id": "J11", "sujet": "Contrats de sous-traitance (DPA)", "base": "nLPD art. 9", "statut": "a-faire", "action": "Hébergeur, messagerie, Infomaniak, Brevo, ASPSMS, Healthchecks, agence.", "fichier": "docs/v2/automatisation.md" },
    { "id": "J12", "sujet": "Relecture par un avocat", "base": "8 points", "statut": "a-faire", "action": "Demande d'avis, exception clients, transferts, mention sans case, défauts.", "fichier": "docs/v2/qa/relecture-juridique-copy.md" },
    { "id": "J13", "sujet": "Images d'illustration", "base": "Licences Unsplash et Pexels ; LCD art. 3", "statut": "pret", "action": "Toujours légendées « Illustration », jamais présentées comme des chantiers.", "fichier": "docs/v3/credits-images.md" }
  ],

  /* Stratégie : chiffres repris du plan de mix v4 (valeurs centrales et fourchettes). */
  "strategie": {
    "recommandation": "Combinaison C : socle (fiche Google, avis, SEO, recommandation) + Google Ads CHF 1'000 + Microsoft CHF 100 par mois + prospection B2B par courrier et appel + 1 dossier simap tous les 2 mois.",
    "contrainte": "Le temps des associés : 60 à 80 h par mois à 30 demandes.",
    "budgets": [
      { "id": "A", "nom": "Socle sans publicité", "mensuel": 1749, "annuel": 20988 },
      { "id": "D", "nom": "Plateformes et partenariats", "mensuel": 2472, "annuel": 29660 },
      { "id": "B", "nom": "Socle + Google Ads", "mensuel": 3613, "annuel": 43356 },
      { "id": "C", "nom": "Socle + Ads + B2B + simap", "mensuel": 3752, "annuel": 45027, "recommande": true }
    ],
    "objectifs": [
      { "jalon": "M3", "demandes": 21.1, "bas": 9.8, "haut": 36.2, "signes": 2.7, "avis": 15 },
      { "jalon": "M6", "demandes": 27.0, "bas": 12.3, "haut": 46.5, "signes": 4.3, "avis": 30 },
      { "jalon": "M12", "demandes": 34.5, "bas": 15.2, "haut": 59.7, "signes": 6.1, "avis": 50 }
    ],
    "reperes": [
      { "nom": "CPL maximal Google Ads", "valeur": "≈ CHF 430" },
      { "nom": "CPL cible", "valeur": "≈ CHF 140" },
      { "nom": "CA signé sur 12 mois (C)", "valeur": "≈ CHF 510'000 (230'000 à 790'000)" },
      { "nom": "Dépendance au payant à M12 (C)", "valeur": "46 % des demandes" }
    ],
    "kpi": ["Demandes/mois", "Part A+B", "Délai de premier contact", "Demande → offre", "Offre → signée", "CA signé", "CPL", "CAC", "ROAS", "ROI", "Avis Google", "Search Console", "Fiche Google", "Citations IA"],
    "liens": [
      { "titre": "Simulateur (hors ligne)", "chemin": "docs/v4/acquisition/simulateur.html" },
      { "titre": "Plan de mix d'acquisition", "chemin": "docs/v4/acquisition/plan-mix-acquisition.md" }
    ],
    "figma": ""
  },

  "livrables": [
    { "groupe": "Site", "titre": "Site local (accueil)", "chemin": "site/index.html", "note": "Mode preview. Formulaire : php -S (pas sur le port 8080 s'il est pris)." },
    { "groupe": "Site", "titre": "Archive de validation v3", "chemin": "livrables/andy-construct-v3-validation.zip", "note": "À décompresser dans res/andy-construct-v3/." },
    { "groupe": "Site", "titre": "Archive de production v3", "chemin": "livrables/andy-construct-v3-production.zip", "note": "Telle que publiée aujourd'hui (rien de confirmé)." },
    { "groupe": "Maquettes", "titre": "Maquette de l'admin (données fictives)", "chemin": "docs/v4/admin/maquette/index.html", "note": "" },
    { "groupe": "Maquettes", "titre": "Simulateur d'acquisition", "chemin": "docs/v4/acquisition/simulateur.html", "note": "" },
    { "groupe": "Supports", "titre": "Plaquette preview (ne pas diffuser)", "chemin": "livrables/andy-construct-references-preview.pdf", "note": "Pour la séance de validation." },
    { "groupe": "Supports", "titre": "Suivi des demandes et KPI (Excel)", "chemin": "livrables/suivi-demandes-et-kpi.xlsx", "note": "Tant que l'admin n'existe pas." },
    { "groupe": "Documents", "titre": "Passation (HANDOFF)", "chemin": "HANDOFF.md", "note": "" },
    { "groupe": "Documents", "titre": "Infos à compléter", "chemin": "projet/infos-a-completer.md", "note": "" },
    { "groupe": "Documents", "titre": "Questionnaire client", "chemin": "projet/questionnaire-client.md", "note": "" },
    { "groupe": "Documents", "titre": "Audit SEO v4", "chemin": "docs/v4/seo/audit-seo.md", "note": "" },
    { "groupe": "Documents", "titre": "Plan de mix d'acquisition", "chemin": "docs/v4/acquisition/plan-mix-acquisition.md", "note": "" },
    { "groupe": "Documents", "titre": "Plan du tableau de bord admin", "chemin": "docs/v4/admin/plan-dashboard-admin.md", "note": "" },
    { "groupe": "Documents", "titre": "Copy deck (C01-C44 au §R)", "chemin": "docs/v2/copy-deck.md", "note": "" },
    { "groupe": "Documents", "titre": "Dossier client", "chemin": "docs/v2/dossier-client.md", "note": "" },
    { "groupe": "Documents", "titre": "Relecture juridique", "chemin": "docs/v2/qa/relecture-juridique-copy.md", "note": "" },
    { "groupe": "Documents", "titre": "Logos des références", "chemin": "docs/v2/logos-references.md", "note": "" },
    { "groupe": "Documents", "titre": "Automatisation", "chemin": "docs/v2/automatisation.md", "note": "" },
    { "groupe": "En ligne", "titre": "Dossier de présentation (décrit la v1)", "chemin": "https://claude.ai/artifact/44SM63Pk6NFCuvZV77ZdFq", "note": "À mettre à jour si besoin." }
  ],

  "journal": [
    { "date": "2026-09-25", "titre": "Maquette v1 initialisée puis livrée (6 pages)", "commit": "0cfba3c" },
    { "date": "2026-09-25", "titre": "Recentrage sur 4 services et la Suisse romande", "commit": "471f3b6" },
    { "date": "2026-10-06", "titre": "Premier document de passation", "commit": "ec5f98d" },
    { "date": "2026-10-31", "titre": "Lancement de la v2 : programme et équipe d'agents", "commit": "57ffba8" },
    { "date": "2026-10-31", "titre": "Dossier client, concurrence, personas, stratégie", "commit": "fc031ed" },
    { "date": "2026-10-31", "titre": "Automatisation livrée : API PHP, 16 workflows", "commit": "9dbbce1" },
    { "date": "2026-10-31", "titre": "Relecture juridique et corrections de sécurité", "commit": "08376ed" },
    { "date": "2026-10-31", "titre": "v2 livrée : 13 pages, 3 modes", "commit": "a633851" },
    { "date": "2026-10-31", "titre": "Lancement de la v3 sur retours client", "commit": "3bc76be" },
    { "date": "2026-10-31", "titre": "17 logos officiels en couleur, « à autoriser »", "commit": "9c25033" },
    { "date": "2026-10-31", "titre": "Design v3 sur l'accueil puis sur toutes les pages", "commit": "7c38ca0" },
    { "date": "2026-11-01", "titre": "Audit SEO v4 et 7 corrections", "commit": "6a0e57f" },
    { "date": "2026-11-01", "titre": "Plan de mix d'acquisition et simulateur", "commit": "661124b" },
    { "date": "2026-11-01", "titre": "Plans de l'admin et maquette cliquable", "commit": "d852ea2" },
    { "date": "2026-11-01", "titre": "Zips v3 régénérés, HANDOFF v4", "commit": "8ba3dd6" },
    { "date": "2026-11-07", "titre": "Recherche publique, infos à compléter, tableau de bord projet", "commit": "" }
  ],

  "ecarts": [
    "Forme : « Sàrl » sur l'ancien site, société en nom collectif au registre.",
    "Adresse : Chêne-Bourg dans 8 annuaires au moins, Carouge au registre depuis 2023.",
    "Année : « 2010 » sur l'ancien site, activité depuis le 01.06.2007.",
    "E-mail : bluewin partout, alors que le domaine est prêt pour l'e-mail.",
    "Catégories fausses : charpenterie, protection auditive, produits chimiques, appareils auditifs.",
    "Services : tissu tendu et cadres acoustiques mis en avant, absents des 4 services.",
    "Effectif : 2-10 (LinkedIn) contre 1-2 (SITG 2021).",
    "Budget : grille v2 annuelle (HANDOFF §8) contre grille v4 mensuelle.",
    "Politique de confidentialité : Pipedrive cité, alors que le plan v4 l'abandonne."
  ]
};
