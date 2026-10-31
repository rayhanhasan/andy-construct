# Accusé de réception · demande de rappel

| | |
|---|---|
| Canal | E-mail transactionnel, seulement si une adresse a été donnée (le module de rappel ne la demande pas : le plus souvent, aucun accusé écrit, voir le SMS dans `sms-prospects.md`) |
| Déclencheur | Module « Vous préférez qu'on vous rappelle ? » (`formulaire=rappel`) |
| Délai | Immédiat |
| Variables | `ref`, `salutation`, `qui`, `promesse`, `telephone`, `creneau` (« le matin », « l'après-midi »), `numeros_appel`, `travaux`, `lieu`, `tel_fixe`, `horaires`, `signature`, `url_confidentialite` |
| Source technique | `site/api/modeles/accuse-rappel.txt` (identique, contrôlé par les tests) |
| À valider | Horaires ; délai de rappel. |

Conventions communes à tous les modèles de ce dossier :

- Syntaxe : `{{variable}}` ; `{{#variable}}…{{/variable}}` n'apparaît que si la variable est remplie ; `{{^variable}}…{{/variable}}` seulement si elle est vide.
- Ton : sobre, chaleureux, direct ; vouvoiement ; français de Suisse romande ; pas d'emoji ; pas de superlatif ; aucune fausse urgence.
- Les lignes après `--` forment le pied de message (version HTML en petit, sous un filet).

<!-- modele: accuse-rappel -->
```texte
Objet : Votre demande de rappel (réf. {{ref}})

{{salutation}},

C'est noté : {{qui}} vous rappelle {{promesse}} au {{telephone}}{{#creneau}}, de préférence {{creneau}} comme vous l'avez indiqué{{/creneau}}.{{#numeros_appel}} Nous appellerons depuis {{numeros_appel}}.{{/numeros_appel}}

{{#travaux}}Votre demande concerne : {{travaux}}{{#lieu}}, à {{lieu}}{{/lieu}}.

{{/travaux}}Si ce numéro ne vous convient plus, répondez simplement à ce message ou appelez le {{tel_fixe}}, {{horaires}} (référence {{ref}}).

Meilleures salutations,

{{signature}}

--
Vos données servent uniquement à traiter votre demande. Elles ne sont ni vendues ni utilisées pour de la publicité. Confidentialité : {{url_confidentialite}}
```
