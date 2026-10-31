# Accusé de réception · guide imprimé envoyé par la poste

| | |
|---|---|
| Canal | E-mail transactionnel, seulement si une adresse a été donnée (l'e-mail est facultatif dans ce formulaire) |
| Déclencheur | Petit formulaire « Recevoir le guide imprimé, par la poste » (`formulaire=envoi_postal_guide`, décision D3). Les guides se téléchargent librement : ce formulaire ne sert qu'à la version imprimée. |
| Délai | Immédiat |
| Séquence de conseils | Annoncée seulement si la personne a coché « Recevoir aussi deux conseils par e-mail » (`conseils_email=oui`, case non cochée par défaut). Alors seulement, le pied porte la désinscription et n8n envoie E2 et E3 (`sequence-aimant.md`). |
| Variables | `salutation`, `guide_titre`, `guide_url` (PDF en ligne, D7), `adresse_envoi` (rue, NPA et localité, sur deux lignes), `conseils_email`, `tel_fixe`, `horaires`, `signature`, `url_desinscription`, `url_confidentialite` |
| Source technique | `site/api/modeles/accuse-guide.txt` (identique, contrôlé par `site/api/tests/run.php`) |
| À valider | Délai d'envoi postal réellement tenu (« dans les prochains jours ouvrables »). |

Conventions communes à tous les modèles de ce dossier :

- Syntaxe : `{{variable}}` ; `{{#variable}}…{{/variable}}` n'apparaît que si la variable est remplie ; `{{^variable}}…{{/variable}}` seulement si elle est vide.
- Ton : sobre, chaleureux, direct ; vouvoiement ; français de Suisse romande ; pas d'emoji ; pas de superlatif ; aucune fausse urgence.
- Les lignes après `--` forment le pied de message (version HTML en petit, sous un filet).

<!-- modele: accuse-guide -->
```texte
Objet : Votre guide part par la poste : {{guide_titre}}

{{salutation}},

C'est noté : nous vous envoyons le guide « {{guide_titre}} » imprimé, à cette adresse :
{{adresse_envoi}}

Il partira dans les prochains jours ouvrables.{{#guide_url}} En attendant, vous pouvez déjà le lire en ligne : {{guide_url}}{{/guide_url}}

{{#conseils_email}}Comme vous l'avez demandé, vous recevrez aussi deux e-mails de conseils sur ce sujet, puis plus rien.

{{/conseils_email}}Une question sur votre situation ? Répondez à ce message ou appelez le {{tel_fixe}}, {{horaires}}.

Meilleures salutations,

{{signature}}

--
{{#conseils_email}}Vous ne souhaitez plus recevoir nos e-mails ? Répondez STOP à ce message{{#url_desinscription}}, ou cliquez ici : {{url_desinscription}}{{/url_desinscription}}.
{{/conseils_email}}Votre adresse sert uniquement à cet envoi. Confidentialité : {{url_confidentialite}}
```
