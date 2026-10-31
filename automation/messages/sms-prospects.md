# SMS aux prospects et clients

| | |
|---|---|
| Règle absolue | **Aucun lien** dans un SMS à un prospect ou à un client (ressemble à du hameçonnage : `personas-psychologie.md` §4, n° 40, et liste noire §5). Un numéro de téléphone fixe connu, le nom de l'entreprise et un élément que seule l'entreprise connaît (référence, type de travaux). |
| Nature | Messages **de service** uniquement (suite directe d'une demande ou d'un contrat). Aucun SMS publicitaire sans accord préalable (LCD art. 3 al. 1 let. o). |
| Expéditeur | « AndyConstr » (expéditeur alphanumérique : on ne peut pas y répondre, d'où le numéro à rappeler dans chaque message) |
| Alphabet | GSM : é, è, à, ù passent ; les modèles évitent « ê », « ô », « ç », « À » et les guillemets « » (un SMS tomberait à 70 caractères). Ceux qui viennent des données sont remplacés automatiquement. |
| Horaires | En semaine de 8 h à 19 h 30, le samedi de 9 h à 12 h, jamais le dimanche ni un jour férié |

Variables : `ref`, `associe_court` (prénom de l'associé, sinon « Un associé »), `promesse`, `heure`, `service`, `civilite_nom` (« Madame Dupont », sinon rien), `prenom_associe`.

## Accusé de réception par SMS (WF01)

Seulement si la personne n'a **pas** donné d'e-mail et que son numéro est un mobile suisse.

<!-- modele: sms-accuse -->
```texte
Andy Construct : votre demande (réf. {{ref}}) est bien arrivée. {{associe_court}} vous rappelle {{promesse}}, depuis le +41 22 771 20 15 ou le +41 78 631 14 34.
```

## Après un appel sans réponse (WF02, bouton « Pas de réponse », 1er essai)

Si la personne n'a pas d'e-mail ; sinon l'e-mail de `rappel-sans-reponse.md`.

<!-- modele: sms-essai-appel -->
```texte
Andy Construct : {{associe_court}} a essayé de vous appeler aujourd'hui à {{heure}} au sujet de votre demande ({{service}}). Vous pouvez nous rappeler au +41 22 771 20 15, du lundi au vendredi de 7 h à 18 h.
```

## Demande d'avis, J+2 après la réception du chantier (WF03d)

Particuliers seulement, en complément de l'e-mail (qui, lui, contient le lien direct).

<!-- modele: sms-demande-avis -->
```texte
Bonjour{{#civilite_nom}} {{civilite_nom}}{{/civilite_nom}}, merci d'avoir confié votre chantier à Andy Construct. Si vous avez une minute, votre avis sur Google aide d'autres personnes à choisir : cherchez "Andy Construct" sur Google Maps, rubrique Avis. Le lien direct est dans notre e-mail. {{prenom_associe}}
```

## Veille d'une visite (facultatif, saisi par l'associé dans le CRM)

<!-- modele: sms-veille-visite -->
```texte
Andy Construct : nous passons demain {{jour}} à {{heure}} pour votre projet ({{service}}). Un imprévu ? Appelez le +41 22 771 20 15. {{prenom_associe}}
```
