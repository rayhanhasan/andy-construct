# SMS aux prospects et clients

| | |
|---|---|
| Règle absolue | **Aucun lien** dans un SMS à un prospect ou à un client (ressemble à du hameçonnage : `personas-psychologie.md` §4, n° 40, et liste noire §5). Un numéro de téléphone fixe connu, le nom de l'entreprise et un élément que seule l'entreprise connaît (référence, type de travaux). |
| Nature | Messages **de service** uniquement (suite directe d'une demande ou d'un contrat). Aucun SMS publicitaire sans accord préalable (LCD art. 3 al. 1 let. o). |
| Expéditeur | « AndyConstr » (expéditeur alphanumérique : on ne peut pas y répondre, d'où le numéro à rappeler dans chaque message) |
| Alphabet | GSM : é, è, à, ù passent ; les modèles évitent « ê », « ô », « ç », « À » et les guillemets « » (un SMS tomberait à 70 caractères). Ceux qui viennent des données sont remplacés automatiquement. |
| Horaires | En semaine de 8 h à 19 h 30, le samedi de 9 h à 12 h, jamais le dimanche ni un jour férié |
| Longueur | **160 caractères au plus** (1 SMS), vérifiée avec les valeurs les plus longues : `ref` « AC-2026-0001 », `associe_court` « Un associé », `promesse` « le 30 septembre avant 16 h 45 », `service` « votre isolation acoustique », `heure` « 17 h 45 », `jour` « mercredi 4 novembre ». Résultats : accusé 158, essai d'appel 159, demande d'avis 158, veille de visite 150. Toute modification doit être recomptée. |
| Opposition | La demande d'avis n'est pas indispensable au contrat : elle porte un moyen d'opposition. L'expéditeur alphanumérique ne reçoit pas de réponse : l'opposition passe par le téléphone (et par « STOP » ou le lien de l'e-mail envoyé le même jour). |

Variables : `ref`, `associe_court` (prénom de l'associé, sinon « Un associé »), `promesse`, `heure`, `service` (« vos travaux de peinture », « votre isolation acoustique »), `jour` (« mercredi »), `prenom_associe`.

## Accusé de réception par SMS (WF01)

Seulement si la personne n'a **pas** donné d'e-mail et que son numéro est un mobile suisse.

<!-- modele: sms-accuse -->
```texte
Andy Construct : demande {{ref}} bien arrivée. {{associe_court}} vous rappelle {{promesse}}, depuis le +41 22 771 20 15 ou le +41 78 631 14 34.
```

## Après un appel sans réponse (WF02, bouton « Pas de réponse », 1er essai)

Si la personne n'a pas d'e-mail ; sinon l'e-mail de `rappel-sans-reponse.md`.

<!-- modele: sms-essai-appel -->
```texte
Andy Construct : nous avons essayé de vous joindre aujourd'hui à {{heure}} au sujet de {{service}}. Vous pouvez nous rappeler au +41 22 771 20 15.
```

## Demande d'avis, J+2 après la réception du chantier (WF03d)

Particuliers seulement, en complément de l'e-mail (qui, lui, contient le lien direct).

<!-- modele: sms-demande-avis -->
```texte
Andy Construct : merci de votre confiance. Si vous le souhaitez, laissez un avis sur notre fiche Google Maps. Pour ne plus recevoir nos SMS : +41 22 771 20 15
```

## Veille d'une visite (facultatif, saisi par l'associé dans le CRM)

<!-- modele: sms-veille-visite -->
```texte
Andy Construct : nous passons demain {{jour}} à {{heure}} pour {{service}}. Un imprévu ? Appelez le +41 22 771 20 15. {{prenom_associe}}
```
