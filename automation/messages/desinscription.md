# Désinscription et opposition (WF12)

| | |
|---|---|
| Canaux | Lien de désinscription en pied de tout message non transactionnel ; réponse « STOP » à un e-mail (détectée par WF14) ; demande orale ou écrite (saisie par l'associé) |
| Effet | Le jour même : adresse bloquée dans Brevo, `opposition_marketing` daté dans le CRM, `ne_pas_relancer` sur les affaires ouvertes. Les messages strictement liés à une demande ou à un chantier en cours (accusé de réception, offre) restent possibles. |
| Sécurité | Le lien ouvre une page avec un bouton « Confirmer » : un logiciel de messagerie qui prévisualise le lien ne désinscrit personne par erreur. |
| Gratuité | Aucun identifiant, aucun compte, aucune question obligatoire (LCD art. 3 al. 1 let. o : opposition « gratuite et facile »). |

## Page de confirmation (avant le clic)

<!-- modele: page-desinscription-confirmer -->
```texte
Ne plus recevoir nos e-mails

Vous ne recevrez plus de conseils ni d'informations d'Andy Construct à l'adresse {{email_masque}}.

[Confirmer]

Si vous avez une demande ou un chantier en cours avec nous, nous pourrons encore vous écrire à ce sujet.
```

## Page après la confirmation

<!-- modele: page-desinscription-ok -->
```texte
C'est fait

Vous ne recevrez plus nos e-mails. Si c'est une erreur, ou pour toute question, appelez-nous au +41 22 771 20 15.
```

## Lien expiré ou invalide

<!-- modele: page-lien-invalide -->
```texte
Ce lien n'est plus valable

Pour ne plus recevoir nos e-mails, répondez simplement « STOP » à l'un de nos messages, ou appelez-nous au +41 22 771 20 15. Nous nous en occupons le jour même.
```
