# Demande d'avis après chantier : J+2, relance J+9, accord pour publier J+14 (scénario d)

| | |
|---|---|
| Canal | Particuliers : e-mail (avec le lien) + SMS sans lien. Professionnels : e-mail au contact nommé. |
| Déclencheur | Chantier passé à « Terminé » **et** `reserves_levees = oui` (WF06, puis horloge WF03d à 10 h en semaine) |
| Règles Google | **Tous** les clients reçoivent la même demande ; aucune sélection selon la satisfaction présumée, aucune contrepartie, aucun avis rédigé par l'entreprise. Un litige (`litige = oui`) **décale** la demande, il ne la supprime pas. |
| Plafond | Une demande et une seule relance (J+9). |
| Pied | Messages de service liés au contrat ; la phrase d'opposition y figure quand même par prudence (y compris pour les professionnels et dans le SMS). |
| Opposition | Un « STOP » doit arrêter **toute** la série (J+9, J+14) : WF03d ne lit aujourd'hui ni `opposition_marketing` ni `ne_pas_relancer` ni `a_repondu` (à corriger avant activation). |
| À valider | Le décalage pour `litige = oui` et l'attente de `reserves_levees = oui` ne doivent pas devenir un tri des clients mécontents (règles Google : pas de sollicitation sélective) : fixer un délai maximal après lequel la demande part quand même, ou ne pas la faire du tout pour personne dans ce cas. Supports de publication des photos (site, fiche Google, LinkedIn, dossier de références) : la liste du J+14 doit correspondre à l'usage réel. |

Variables : `salutation`, `service`, `commune`, `lien_avis_google` (lien direct vers le formulaire d'avis de la fiche), `prenom_associe`, `signature`, `lien_photos_sans_nom`, `lien_photos_commune`, `lien_temoignage`, `lien_refus`, `url_desinscription`.

## J+2 · e-mail (particuliers et PME)

<!-- modele: avis-j2 -->
```texte
Objet : Merci, et votre avis sur notre travail

{{salutation}},

Le chantier{{#commune}} de {{commune}}{{/commune}} est terminé : merci pour votre confiance.

Que vous soyez satisfait(e) ou que vous ayez des réserves, votre avis public nous est utile et aide d'autres personnes à choisir. Cela prend une minute :
{{lien_avis_google}}

Si vous le souhaitez, mentionnez le type de travaux et la commune. Et si un point n'est pas en ordre, vous pouvez aussi nous le dire directement, en répondant à ce message.

Meilleures salutations,

{{signature}}

--
Vous ne souhaitez plus recevoir de message de notre part ? Répondez « STOP »{{#url_desinscription}} ou cliquez ici : {{url_desinscription}}{{/url_desinscription}}.
```

Le SMS du même jour est dans `sms-prospects.md` (`sms-demande-avis`).

## J+9 · relance unique (si l'avis n'a pas été repéré)

<!-- modele: avis-j9 -->
```texte
Objet : Petit rappel, si vous avez une minute

{{salutation}},

Si vous avez déjà laissé votre avis, merci beaucoup, et ignorez ce message.

Sinon, voici le lien, valable en tout temps : {{lien_avis_google}}

Nous ne vous relancerons plus à ce sujet.

Meilleures salutations,

{{signature}}

--
Vous ne souhaitez plus recevoir de message de notre part ? Répondez « STOP »{{#url_desinscription}} ou cliquez ici : {{url_desinscription}}{{/url_desinscription}}.
```

## J+2 · professionnels (régie, architecte, commune) : autorisation de citer

Les professionnels publient rarement des avis ; on demande plutôt l'autorisation de citer la référence (exigée pour les marques privées, programme v2 §4).

<!-- modele: reference-pro-j2 -->
```texte
Objet : {{service_majuscule}}{{#commune}} à {{commune}}{{/commune}} : merci, et une question

{{salutation}},

Les travaux{{#commune}} de {{commune}}{{/commune}} sont terminés : merci pour votre confiance et pour la bonne collaboration.

Pourrions-nous citer ce chantier parmi nos références (site internet et dossier de références) ? Nous vous soumettrons le texte avant toute publication. Si vous le préférez, un avis sur notre fiche Google nous aide aussi : {{lien_avis_google}}

Une réponse à ce message suffit, dans un sens comme dans l'autre.

Meilleures salutations,

{{signature}}

--
Vous ne souhaitez plus recevoir de message de notre part ? Répondez « STOP »{{#url_desinscription}} ou cliquez ici : {{url_desinscription}}{{/url_desinscription}}.
```

## J+14 · accord pour montrer le chantier (particuliers)

<!-- modele: accord-photos-j14 -->
```texte
Objet : Pouvons-nous montrer votre chantier ?

{{salutation}},

Nous aimerions montrer quelques photos de votre chantier sur notre site, sur notre fiche Google, sur notre page LinkedIn et dans notre dossier de références, pour aider d'autres personnes à se faire une idée. Nous ne le ferons qu'avec votre accord. Choisissez ce qui vous convient :

- Photos sans aucun nom : {{lien_photos_sans_nom}}
- Photos avec la commune seulement : {{lien_photos_commune}}
- Photos et quelques mots de votre part (nous vous les soumettons avant publication) : {{lien_temoignage}}
- Je préfère que vous ne publiiez rien : {{lien_refus}}

Aucune photo ne montre de visage ni d'objet personnel identifiable. Vous pouvez retirer votre accord à tout moment en répondant à ce message.

Meilleures salutations,

{{signature}}
```

## Brouillons de réponse aux avis (préparés par l'agence, publiés par l'associé sous 48 h)

<!-- modele: reponse-avis-positif -->
```texte
Merci {{prenom_auteur}} pour votre retour sur {{service}} à {{commune}}. C'était un plaisir de travailler chez vous. {{prenom_associe}}, Andy Construct
```

<!-- modele: reponse-avis-mitige -->
```texte
Merci {{prenom_auteur}} d'avoir pris le temps de nous écrire. Nous prenons note de votre remarque sur {{point}}. Je vous appelle pour en parler et voir ce que nous pouvons faire. {{prenom_associe}}, Andy Construct
```

<!-- modele: reponse-avis-negatif -->
```texte
{{prenom_auteur}}, nous regrettons que notre travail ne vous ait pas donné satisfaction. Nous souhaitons comprendre ce qui s'est passé et voir ce que nous pouvons faire : pouvez-vous nous appeler au +41 22 771 20 15, ou nous indiquer quand vous joindre ? {{prenom_associe}}, Andy Construct
```

Règles des réponses : jamais de détail privé (adresse, montant), jamais d'argument agressif, jamais de demande de suppression sans motif valable.
