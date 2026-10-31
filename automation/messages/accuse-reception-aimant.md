# Accusé de réception · guide (aimant), 1er e-mail de la séquence

| | |
|---|---|
| Canal | E-mail. Premier message de la séquence (f) annoncée sur le formulaire : il porte donc la désinscription. |
| Déclencheur | Formulaire de guide (`formulaire=aimant`) avec e-mail. Envoyé par le PHP, même si n8n est en panne ; n8n envoie ensuite E2 et E3 (`sequence-aimant.md`). |
| Délai | Immédiat |
| Variables | `salutation` (« Bonjour Bernard » ou « Bonjour Madame Dupont »), `aimant_titre`, `aimant_url`, `aimant_format`, `aimant_lecture`, `par_poste`, `newsletter`, `tel_fixe`, `horaires`, `signature`, `url_desinscription`, `url_confidentialite` |
| Source technique | `site/api/modeles/accuse-aimant.txt` (identique, contrôlé par les tests) |
| À valider | Arbitrage de `architecture-cro.md` §15 (guide en lien direct ou envoyé par e-mail) : si le lien direct est retenu, ce message ne part que pour les personnes qui ont laissé leur e-mail. |

Conventions communes à tous les modèles de ce dossier :

- Syntaxe : `{{variable}}` ; `{{#variable}}…{{/variable}}` n'apparaît que si la variable est remplie ; `{{^variable}}…{{/variable}}` seulement si elle est vide.
- Ton : sobre, chaleureux, direct ; vouvoiement ; français de Suisse romande ; pas d'emoji ; pas de superlatif ; aucune fausse urgence.
- Les lignes après `--` forment le pied de message (version HTML en petit, sous un filet).

<!-- modele: accuse-aimant -->
```texte
Objet : Votre guide : {{aimant_titre}}

{{salutation}},

{{#aimant_url}}Voici votre guide « {{aimant_titre}} »{{#aimant_format}} ({{aimant_format}}){{/aimant_format}} :
{{aimant_url}}

{{#aimant_lecture}}Il se lit en {{aimant_lecture}}. {{/aimant_lecture}}{{/aimant_url}}{{#par_poste}}Nous vous envoyons aussi la version imprimée par la poste, à l'adresse indiquée, dans les prochains jours ouvrables.{{/par_poste}}{{^par_poste}}Si vous préférez une version imprimée, répondez simplement à ce message en indiquant votre adresse postale.{{/par_poste}}

Comme annoncé, vous recevrez encore deux e-mails de conseils sur ce sujet, puis plus rien.{{#newsletter}} Vous avez aussi demandé notre lettre trimestrielle : un e-mail séparé vous demandera de confirmer cette inscription.{{/newsletter}}

Une question sur votre situation ? Répondez à ce message ou appelez le {{tel_fixe}}, {{horaires}}.

Meilleures salutations,

{{signature}}

--
Vous ne souhaitez plus recevoir nos e-mails ? Répondez STOP à ce message{{#url_desinscription}}, ou cliquez ici : {{url_desinscription}}{{/url_desinscription}}.
Confidentialité : {{url_confidentialite}}
```
