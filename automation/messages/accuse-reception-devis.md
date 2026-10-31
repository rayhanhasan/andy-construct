# Accusé de réception · demande de devis

| | |
|---|---|
| Canal | E-mail transactionnel (texte + HTML dérivé, sans image ni pixel de suivi) |
| Déclencheur | Formulaire de devis envoyé avec une adresse e-mail (`site/api/demande.php`, formulaire `devis`). Sans e-mail : aucun accusé écrit ; n8n envoie un SMS sans lien si le numéro est un mobile (voir `sms-prospects.md`). |
| Délai | Immédiat (moins d'une minute) |
| Expéditeur | « Prénom Nom · Andy Construct » <site@andyconstruct.ch> ; « Répondre » écrit à l'associé attribué |
| Variables | `ref`, `salutation`, `qui`, `qui_majuscule`, `verbe_contact` (appelle / répond par e-mail / répond), `promesse` (« aujourd'hui avant 16 h »), `numeros_appel`, `hors_cible`, `travaux`, `lieu`, `delai`, `nb_fichiers`, `message_extrait` (200 caractères, liens masqués), `realisation_url`, `tel_fixe`, `horaires`, `signature`, `url_confidentialite` |
| Source technique | `site/api/modeles/accuse-devis.txt`. Le bloc ci-dessous doit rester **identique** (contrôlé par `site/api/tests/run.php`) : modifiez les deux en même temps. |
| À valider | Délai de rappel `[À CONFIRMER C01]` : repli `promesse_delai => false` (« dans les meilleurs délais »). Horaires `[À CONFIRMER C03]` : repli `entreprise.horaires => ''` (la mention disparaît). Associé nommé `[C09]` ; numéros de rappel et mobile `[C30]` ; rôles « bureau » / « terrain ». Signature : `entreprise.nom` doit porter la raison de commerce complète « Andy Construct, Chanton & Cie » (art. 954a CO). |

Conventions communes à tous les modèles de ce dossier :

- Syntaxe : `{{variable}}` ; `{{#variable}}…{{/variable}}` n'apparaît que si la variable est remplie ; `{{^variable}}…{{/variable}}` seulement si elle est vide.
- Ton : sobre, chaleureux, direct ; vouvoiement ; français de Suisse romande ; pas d'emoji ; pas de superlatif ; aucune fausse urgence.
- Les lignes après `--` forment le pied de message (version HTML en petit, sous un filet).

<!-- modele: accuse-devis -->
```texte
Objet : Votre demande à Andy Construct (réf. {{ref}})

{{salutation}},

Votre demande est bien arrivée, merci. {{qui_majuscule}} vous {{verbe_contact}} {{promesse}}{{#numeros_appel}}, depuis {{numeros_appel}}{{/numeros_appel}}{{^hors_cible}}, pour en parler et, si nécessaire, convenir d'une visite{{/hors_cible}}.

Ce que vous nous avez indiqué :
- Travaux : {{travaux}}
- Lieu : {{lieu}}
{{#delai}}- Délai souhaité : {{delai}}
{{/delai}}{{#nb_fichiers}}- Fichiers reçus : {{nb_fichiers}}
{{/nb_fichiers}}{{#message_extrait}}- Votre message : « {{message_extrait}} »
{{/message_extrait}}
{{^hors_cible}}Pour préparer notre échange, vous pouvez rassembler quelques photos, les dimensions approximatives et, si vous en avez, les plans.

{{/hors_cible}}{{#realisation_url}}Un exemple de chantier comparable : {{realisation_url}}

{{/realisation_url}}Vous préférez nous appeler ? Le {{tel_fixe}}{{#horaires}}, {{horaires}}{{/horaires}} (référence {{ref}}).

À très bientôt : {{qui}} vous {{verbe_contact}} {{promesse}}.

Meilleures salutations,

{{signature}}

--
Vos données servent uniquement à traiter votre demande. Elles ne sont ni vendues ni utilisées pour de la publicité. Confidentialité : {{url_confidentialite}}
```
