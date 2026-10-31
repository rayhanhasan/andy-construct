# Appel sans réponse et clôture courtoise (scénario b)

| | |
|---|---|
| Canal | E-mail (si une adresse est connue ; sinon SMS sans lien, voir `sms-prospects.md`) |
| Déclencheur | L'associé clique « Pas de réponse » dans l'e-mail interne ou le SMS (WF02) |
| Nature | Message de service : suite directe de la demande |
| Expéditeur | Associé attribué, depuis son adresse du domaine (les réponses arrivent chez lui) |
| Règles | 1er essai : ce message + tâche « Rappeler » le lendemain à 10 h. 3e essai en 5 jours ouvrables : message de clôture, affaire « perdue, sans réponse », **aucune relance à 6 mois**. Toute réponse arrête la séquence (WF14). |

Variables : `salutation`, `associe`, `heure`, `service`, `ref`, `tel_fixe`, `signature`.

## 1er essai sans réponse

<!-- modele: essai-appel-email -->
```texte
Objet : Nous avons essayé de vous joindre (réf. {{ref}})

{{salutation}},

J'ai essayé de vous appeler aujourd'hui à {{heure}} au sujet de votre demande ({{service}}), sans parvenir à vous joindre.

Quand puis-je vous rappeler ? Répondez simplement à ce message en indiquant un moment qui vous convient, ou appelez-nous au {{tel_fixe}}, du lundi au vendredi de 7 h à 18 h.

Meilleures salutations,

{{signature}}
```

## Clôture après trois essais

<!-- modele: cloture-sans-reponse -->
```texte
Objet : Votre demande {{ref}}

{{salutation}},

Nous avons essayé de vous joindre à plusieurs reprises au sujet de votre demande ({{service}}), sans succès.

Votre demande reste enregistrée : si votre projet est toujours d'actualité, il suffit de répondre à ce message ou d'appeler le {{tel_fixe}}. Nous ne vous relancerons pas davantage.

Meilleures salutations,

{{signature}}
```
