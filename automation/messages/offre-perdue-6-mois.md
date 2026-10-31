# Relance d'une offre perdue, six mois après (scénario e)

| | |
|---|---|
| Canal | Particuliers : un seul e-mail. Professionnels : **tâche « Appeler »** (5 minutes), pas d'e-mail. |
| Déclencheur | Horloge quotidienne WF04e : affaire perdue depuis 182 jours |
| Conditions | `recontact_autorise = oui` (donné par la personne, par le lien « Le projet est reporté » ou au téléphone) **et** motif « reporté », « prix » ou « délai ». Jamais pour « sans réponse » ni « hors cible ». Pas d'opposition. Pas de marché public. Au plus un message marketing tous les 30 jours (`dernier_message_marketing`). |
| Base légale | Demande expresse de la personne d'être recontactée (stratégie §9.2) |
| Expéditeur | Associé d'origine |

Variables : `salutation`, `service`, `commune`, `signature`, `url_desinscription`.

## E-mail (particuliers)

<!-- modele: offre-perdue-6-mois -->
```texte
Objet : Votre projet de {{service}}{{#commune}} à {{commune}}{{/commune}}

{{salutation}},

Il y a six mois, vous nous aviez consultés pour {{service}} et souhaitiez être recontacté(e) plus tard. Comme convenu, je reviens vers vous une seule fois.

Le projet est-il toujours d'actualité ? Si oui, nous pouvons mettre notre offre à jour ou proposer une réalisation par étapes. Une simple réponse à ce message suffit.

Sans nouvelle de votre part, nous ne vous écrirons plus à ce sujet.

Meilleures salutations,

{{signature}}

--
Vous ne souhaitez plus recevoir de message de notre part ? Répondez STOP{{#url_desinscription}} ou cliquez ici : {{url_desinscription}}{{/url_desinscription}}.
```

## Tâche d'appel (professionnels)

<!-- modele: tache-offre-perdue-pro -->
```texte
Appeler {{nom}} ({{organisation}}) : offre {{service}} du {{date_offre}}, perdue pour « {{motif_perte}} », recontact accepté. Question : « Le projet est-il revenu à l'ordre du jour ? Souhaitez-vous une offre mise à jour ? » Résultat à saisir : intéressé (nouvelle affaire), plus tard, ne plus contacter.
```
