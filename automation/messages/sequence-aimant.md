# Séquence « guide » : trois e-mails (scénario f)

| | |
|---|---|
| Canal | E-mail par l'API « transactionnelle » de Brevo, en semaine à 9 h 30. Juridiquement, ce n'est **pas** un message transactionnel : accord préalable et désinscription obligatoires. |
| Condition | **Uniquement** si la personne a donné son e-mail **et** coché « Recevoir aussi deux conseils par e-mail » (`conseils_email=oui`, case non cochée par défaut ; décision D3). Les guides se téléchargent librement : aucune adresse n'est exigée pour les lire. |
| Déclencheur | Formulaire « guide imprimé par la poste » (`formulaire=envoi_postal_guide`) ; WF07 |
| E1 | Immédiat, envoyé par le PHP : `accuse-reception-guide.md` (annonce les deux conseils et porte la désinscription) |
| E2 | J+3 : un conseil utile, un exemple réel |
| E3 | J+8 : proposition de visite, sans pression ; dernier message |
| Arrêt | Désinscription (lien ou STOP), réponse à un e-mail, ou demande de devis créée entre-temps |
| Base légale | Accord explicite (case cochée) pour une information demandée ; désinscription dans chaque message (LCD art. 3 al. 1 let. o) |
| Profils professionnels | Aucun appel (décision du chef de projet) : seule la tâche « envoyer le guide imprimé » est créée. Un appel exigerait une case explicite, non cochée par défaut, « Je souhaite être rappelé(e) », absente du formulaire |
| Guides concernés | `guide-reduire-le-bruit` et `checklist-chantier-site-occupe` (D7). Le guide « architectes » est prévu plus tard (stratégie §4, n° 4). |

Variables : `salutation`, `commune_exemple`, `lien_fiche_projet`, `trimestre`, `signature`, `url_desinscription`.

## Guide « Réduire le bruit chez soi » (`guide-reduire-le-bruit`, propriétaires)

<!-- modele: aimant-guide-bruit-e2 -->
```texte
Objet : Bruit : absorber ou isoler, ce qui change tout

{{salutation}},

La moitié des déceptions vient d'une confusion : un panneau absorbant réduit l'écho dans la pièce, il n'arrête pas le bruit du voisin. Pour cela, il faut isoler, c'est-à-dire désolidariser une paroi ou un plafond.

{{#lien_fiche_projet}}Voici comment nous avons traité un cas réel{{#commune_exemple}} à {{commune_exemple}}{{/commune_exemple}} : {{lien_fiche_projet}}

{{/lien_fiche_projet}}Une question sur votre situation ? Répondez simplement à ce message.

Meilleures salutations,

{{signature}}

--
Vous ne souhaitez plus recevoir nos e-mails ? Répondez « STOP »{{#url_desinscription}} ou cliquez ici : {{url_desinscription}}{{/url_desinscription}}.
```

<!-- modele: aimant-guide-bruit-e3 -->
```texte
Objet : Un avis sur votre situation ?

{{salutation}},

Chaque logement est différent : le bon remède dépend du type de bruit (voix, pas, musique) et de la construction. C'est pour cela que nous préférons voir les lieux avant de faire une offre.

Si vous le souhaitez, nous venons voir la pièce concernée et vous remettons ensuite une offre écrite. Il suffit de répondre à ce message ou d'appeler le +41 22 771 20 15.

C'est notre dernier message sur ce sujet.

Meilleures salutations,

{{signature}}

--
Vous ne souhaitez plus recevoir nos e-mails ? Répondez « STOP »{{#url_desinscription}} ou cliquez ici : {{url_desinscription}}{{/url_desinscription}}.
```

## Liste de contrôle « Travaux en immeuble habité » (`checklist-chantier-site-occupe`, régies)

<!-- modele: aimant-checklist-regie-e2 -->
```texte
Objet : Immeuble habité : ce qui évite les plaintes des locataires

{{salutation}},

Dans un immeuble habité, ce sont rarement les travaux qui posent problème, mais l'information : un avis affiché trop tard, un interlocuteur introuvable, de la poussière dans la cage d'escalier.

{{#lien_fiche_projet}}Voici un chantier réalisé en logement occupé, avec son organisation : {{lien_fiche_projet}}

{{/lien_fiche_projet}}Si un modèle d'avis aux locataires vous est utile, répondez à ce message : nous vous l'envoyons.

Meilleures salutations,

{{signature}}

--
Vous ne souhaitez plus recevoir nos e-mails ? Répondez « STOP »{{#url_desinscription}} ou cliquez ici : {{url_desinscription}}{{/url_desinscription}}.
```

<!-- modele: aimant-checklist-regie-e3 -->
```texte
Objet : Vos fins de bail{{#trimestre}} de {{trimestre}}{{/trimestre}}

{{salutation}},

Pour vos remises en état de fin de bail, nous pouvons chiffrer un forfait type (prix par pièce, plafonds et murs) : vos ordres partent alors plus vite, et vous savez à l'avance ce que coûtera un appartement.

Si cela vous intéresse, répondez à ce message ou appelez le +41 22 771 20 15.

C'est notre dernier message sur ce sujet.

Meilleures salutations,

{{signature}}

--
Vous ne souhaitez plus recevoir nos e-mails ? Répondez « STOP »{{#url_desinscription}} ou cliquez ici : {{url_desinscription}}{{/url_desinscription}}.
```

## Guide « Acoustique en rénovation » (architectes, guide futur)

<!-- modele: aimant-guide-architectes-e2 -->
```texte
Objet : Désolidarisation : le détail qui fait la performance

{{salutation}},

En isolation acoustique, tout se joue dans les détails : une liaison rigide mal traitée entre la cloison et la structure laisse passer le bruit, et on ne la corrige pas sans démonter.

{{#lien_fiche_projet}}Voici un chantier où ce point a été traité, avec le système mis en œuvre : {{lien_fiche_projet}}

{{/lien_fiche_projet}}Meilleures salutations,

{{signature}}

--
Vous ne souhaitez plus recevoir nos e-mails ? Répondez « STOP »{{#url_desinscription}} ou cliquez ici : {{url_desinscription}}{{/url_desinscription}}.
```

<!-- modele: aimant-guide-architectes-e3 -->
```texte
Objet : Un descriptif à faire relire ?

{{salutation}},

Si vous préparez un appel d'offres avec un lot de plâtrerie ou d'acoustique (CFC 271 ou 283), nous pouvons relire le descriptif sur les points d'exécution, ou établir un pré-chiffrage. Une réponse à ce message suffit.

C'est notre dernier message sur ce sujet.

Meilleures salutations,

{{signature}}

--
Vous ne souhaitez plus recevoir nos e-mails ? Répondez « STOP »{{#url_desinscription}} ou cliquez ici : {{url_desinscription}}{{/url_desinscription}}.
```

## À valider

- E3 « bruit » : formulé selon les replis du copy deck tant que `C06` (visite avant chaque offre, offre détaillée) n'est pas confirmé. Une fois confirmé, on peut revenir à « nous passons toujours voir avant de proposer quoi que ce soit » et « une offre écrite et détaillée ».
- E2 régie : le modèle d'avis aux locataires doit exister avant d'être proposé `[À CONFIRMER C20]`.
- E3 régie : forfait type et prix par pièce `[À CONFIRMER C17]` ; ne pas activer la série « régie » sans confirmation.
- Guide « architectes » : lots CFC cités `[À CONFIRMER C14]` (repli : « 271 Plâtrerie »).
- L'appel de courtoisie aux profils professionnels est **supprimé** de WF07 (il n'était annoncé ni sur le formulaire ni dans l'accusé). Avant E2 et E3, WF07 relit l'état Brevo **et** l'opposition dans Pipedrive ; si l'un des deux ne peut pas être lu, rien n'est envoyé.
