# Suivi d'une offre envoyée : J+3, J+10, J+21 (scénario c)

| | |
|---|---|
| Canal | E-mail individuel depuis la boîte de l'associé qui a envoyé l'offre (SMTP du domaine), en semaine à 9 h 15 |
| Déclencheur | Affaire passée à l'étape « Offre envoyée » (WF06 remplit `date_offre`) ; horloge quotidienne WF03c |
| Nature | Message de service : suite directe de l'offre demandée |
| Jamais pour | Marchés publics (égalité de traitement) ; affaires `ne_pas_relancer` ; dès que la personne a répondu (`a_repondu`, détecté par WF14) ou que l'affaire change d'étape |
| Plafond | **Deux relances écrites au plus** (liste noire des personas). J+10 devient un **appel** (tâche CRM) dès qu'un numéro est connu, et toujours pour les professionnels et les demandes A. |
| J+35 | Message interne à l'associé : « Clore cette offre ? » (boutons) |
| J+45 | Clôture automatique « sans réponse », **sans** message au client |

Variables : `salutation`, `service` (« vos travaux de peinture », « votre isolation acoustique »), `service_majuscule`, `commune`, `date_offre` (« 12 novembre »), `num_offre`, `lien_parler`, `lien_reporte`, `lien_autre` (liens en un clic signés, valables 60 jours), `signature`.

## J+3 · « Bien reçue ? »

<!-- modele: relance-offre-j3 -->
```texte
Objet : Votre offre pour {{service}} : bien reçue ?

{{salutation}},

Je vous ai transmis le {{date_offre}} notre offre{{#num_offre}} n° {{num_offre}}{{/num_offre}} pour {{service}}{{#commune}} à {{commune}}{{/commune}}. L'avez-vous bien reçue ?

Si un point n'est pas clair (variantes, délais, organisation du chantier), je vous l'explique volontiers par téléphone. Il suffit de répondre à ce message avec un moment qui vous convient.

Meilleures salutations,

{{signature}}
```

## J+10 · « Des questions ? » (seulement sans numéro de téléphone)

Avec un numéro : tâche « Appeler » pour l'associé, avec la note « Avez-vous des questions sur notre offre ? Comparaison avec d'autres offres ? Visite complémentaire ? ».

<!-- modele: relance-offre-j10 -->
```texte
Objet : Des questions sur notre offre ?

{{salutation}},

Il est normal de comparer plusieurs offres. Si un point de la nôtre mérite une explication, je vous la donne volontiers.

Si un détail mérite d'être revu sur place, je peux repasser. Une réponse à ce message suffit.

Meilleures salutations,

{{signature}}
```

## J+21 · « Où en êtes-vous ? » (trois réponses en un clic)

<!-- modele: relance-offre-j21 -->
```texte
Objet : {{service_majuscule}} : où en êtes-vous ?

{{salutation}},

Où en est votre réflexion ? Un simple clic nous aide à nous organiser, sans autre engagement :

- Je souhaite en parler : {{lien_parler}}
- Le projet est reporté, vous pouvez me recontacter plus tard : {{lien_reporte}}
- J'ai fait un autre choix : {{lien_autre}}

Vous pouvez aussi répondre à ce message. Sans nouvelle de votre part, nous ne vous relancerons plus au sujet de cette offre.

Meilleures salutations,

{{signature}}
```

## Pages affichées après un clic (WF02)

Chaque lien ouvre d'abord une page avec un bouton de confirmation (un logiciel de messagerie qui « prévisualise » les liens ne déclenche donc rien).

<!-- modele: page-offre-parler -->
```texte
Merci. {{associe}} vous appelle dans les prochains jours ouvrables. Vous pouvez aussi nous joindre au +41 22 771 20 15.
```

<!-- modele: page-offre-reporte -->
```texte
C'est noté. Nous vous recontacterons une seule fois, dans six mois environ. Si votre projet avance plus tôt, appelez-nous au +41 22 771 20 15.
```

<!-- modele: page-offre-autre -->
```texte
Merci de nous avoir répondu, cela nous aide beaucoup. Nous ne vous relancerons pas. Si un autre projet se présente, nous restons à votre disposition au +41 22 771 20 15.
```

## J+35 · message interne « Clore cette offre ? »

<!-- modele: interne-offre-j35 -->
```texte
Objet : [Offre sans réponse] {{nom}} · {{service}} · {{commune}}

L'offre{{#num_offre}} n° {{num_offre}}{{/num_offre}} du {{date_offre}} ({{montant}}) est sans réponse depuis 35 jours, malgré les relances.

- Clore (motif « sans réponse ») : {{lien_clore}}
- Garder ouverte 30 jours de plus : {{lien_prolonger}}
- Ouvrir dans le CRM : {{lien_crm}}

Sans action, elle sera close automatiquement à J+45, sans message au client.
```

## À valider avant la mise en production

- J+10 : texte de repli tant que `C06` et `C07` ne sont pas confirmés. Une fois confirmés, la 1re phrase peut redevenir : « Pour faciliter la comparaison, la nôtre détaille chaque poste ; elle comprend la protection des lieux, le nettoyage et la réception du chantier avec vous. »
- Validité des offres : si elle est inférieure à 45 jours, le J+21 mentionne la date de validité **réelle**, jamais une fausse échéance.
- Nombre de messages écrits : avec un téléphone connu, J+3 et J+21 (J+10 devient un appel) ; **sans téléphone, J+3, J+10 et J+21 font trois e-mails**, au-delà du plafond « deux relances écrites ». Choisir : ne pas envoyer le J+10 par e-mail, ou assumer trois messages (la politique de confidentialité dit « au plus trois fois en trois semaines »).
