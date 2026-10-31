# Suivi après chantier : entretien à deux ans, un an déjà, régies (scénario i)

| | |
|---|---|
| Canal | E-mail depuis la boîte de l'associé « terrain » |
| Déclencheur | Horloge quotidienne WF04i : peinture → `date_reception_chantier` + 23 mois ; autres services → + 12 mois ; régies → chaque année début octobre |
| Base légale | Exception « clients » de l'art. 3 al. 1 let. o LCD : prestations propres analogues, **et** client informé de son droit d'opposition lors de la collecte (`info_exception_client` rempli). Sinon : rien. |
| Plafond | Une fois par chantier (un an, deux ans) ; un message marketing tous les 30 jours au plus. |
| À valider | Passage de contrôle et retouches `[À CONFIRMER C32]` : ne pas activer « Peinture, 23 mois » tant que C32 n'est pas confirmé. Conditions du passage (gratuit ? retouches comprises ?) : le texte ne promet rien, mais un passage facturé devra être annoncé comme tel avant le rendez-vous. Prix par pièce pour les régies `[À CONFIRMER C17]` : ne pas activer « Régies » sans confirmation. Délai de garantie SIA 118 : seulement si le contrat y est soumis (`C33`). Phrase d'information « exception clients » présente dans l'offre ou la confirmation de commande avant de remplir `info_exception_client`. |

Variables : `salutation`, `pieces_ou_service` (« les peintures du salon »), `commune`, `lien_passage`, `annee_suivante`, `lien_en_parler`, `signature`, `url_desinscription`.

## Peinture, 23 mois après la réception

<!-- modele: entretien-peinture-2-ans -->
```texte
Objet : Votre peinture, deux ans après

{{salutation}},

Il y a bientôt deux ans, nous avons refait {{pieces_ou_service}}{{#commune}} à {{commune}}{{/commune}}. Si vous le souhaitez, nous passons voir l'état des surfaces et nous vous disons s'il y a des retouches à prévoir.

C'est aussi l'occasion de faire le point sur d'autres pièces, si vous y pensiez.

Je souhaite un passage : {{lien_passage}}

Sinon, il n'y a rien à faire : ce message ne sera pas répété.

Meilleures salutations,

{{signature}}

--
Vous ne souhaitez plus recevoir de message de notre part ? Répondez « STOP »{{#url_desinscription}} ou cliquez ici : {{url_desinscription}}{{/url_desinscription}}.
```

## Autres services, 12 mois après la réception

<!-- modele: entretien-un-an -->
```texte
Objet : Un an déjà : tout est en ordre ?

{{salutation}},

Il y a un an, nous terminions {{pieces_ou_service}}{{#commune}} à {{commune}}{{/commune}}. Tout est-il toujours en ordre ? Si quelque chose vous pose question, répondez simplement à ce message : nous revenons voir.

Et si une personne de votre entourage a un projet de placo, de peinture ou d'isolation, vous pouvez lui donner notre numéro, le +41 22 771 20 15. Nous vous en remercions d'avance.

Meilleures salutations,

{{signature}}

--
Vous ne souhaitez plus recevoir de message de notre part ? Répondez « STOP »{{#url_desinscription}} ou cliquez ici : {{url_desinscription}}{{/url_desinscription}}.
```

## Régies, chaque année début octobre

<!-- modele: regies-annuel -->
```texte
Objet : Vos rafraîchissements de {{annee_suivante}}

{{salutation}},

Vous préparez peut-être votre budget d'entretien pour {{annee_suivante}}. Nous pouvons chiffrer vos rafraîchissements types de fin de bail (prix par pièce) et vos cages d'escalier, pour que vos ordres partent plus vite le moment venu.

Si cela vous est utile : {{lien_en_parler}}, ou une réponse à ce message.

Meilleures salutations,

{{signature}}

--
Vous ne souhaitez plus recevoir de message de notre part ? Répondez « STOP »{{#url_desinscription}} ou cliquez ici : {{url_desinscription}}{{/url_desinscription}}.
```
