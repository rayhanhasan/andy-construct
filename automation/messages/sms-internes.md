# SMS internes (aux associés et à l'agence)

| | |
|---|---|
| Canal | SMS (ASPSMS, expéditeur « AndyConstr ») vers les mobiles des associés (`AC_ASSOCIE_*_MOBILE`) ou de l'agence |
| Longueur | 2 SMS au plus (306 caractères). Alphabet GSM : é, è, à, ù passent ; « ê », « ô », « ç », « À » et les guillemets « » forcent un codage où un SMS ne contient plus que 70 caractères. Les modèles les évitent, et le code remplace ceux qui viennent des données (« Chêne-Bourg » devient « Chene-Bourg »). |
| Liens | Autorisés **uniquement dans les SMS internes**, en adresse complète vers le domaine de l'entreprise (jamais de lien raccourci). Aucun lien dans un SMS à un prospect (`sms-prospects.md`). |
| Horaires | Entre 20 h et 7 h, l'envoi attend 7 h ; le samedi, seulement pour les demandes A ; le dimanche, rien (lundi 7 h). |

Variables : `priorite`, `nom_court` (civilité + nom, ou « nom non indiqué »), `commune`, `service`, `surface`, `delai`, `telephone`, `echeance_hhmm` (« 12 h 07 »), `lien_action`, `duree` (« 2 h 15 »), `associe`, `n`, `semaine`, `workflow`, `noeud`, `heure`.

## Nouvelle demande A ou B (WF01)

<!-- modele: sms-nouvelle-demande -->
```texte
Andy · Demande {{priorite}} · {{nom_court}}, {{commune}} · {{service}}{{#surface}}, {{surface}}{{/surface}}{{#delai}}, {{delai}}{{/delai}} · Tél. {{telephone}} · Rappeler avant {{echeance_hhmm}} · {{lien_action}}
```

## Délai de rappel dépassé, à l'associé attribué (WF03, T0)

<!-- modele: sms-rappel-retard -->
```texte
Rappel · {{nom_court}} ({{priorite}}, {{commune}}) attend votre appel depuis {{duree}}. Tél. {{telephone}} · {{lien_action}}
```

## Escalade à l'autre associé (WF03, T0 + 1 h pour A, + 4 h pour B)

<!-- modele: sms-escalade -->
```texte
Andy · {{nom_court}} ({{priorite}}, {{commune}}) n'a pas encore été rappelé(e) (échéance {{echeance_hhmm}}, {{associe}}). Pouvez-vous appeler ? Tél. {{telephone}} · {{lien_action}}
```

## Appels de prospection de la semaine (WF10, lundi 7 h 30)

<!-- modele: sms-b2b-appels -->
```texte
Andy · Vos {{n}} appels de prospection de la semaine vous attendent : fiches, script et boutons de résultat dans l'e-mail "Prospection B2B, semaine {{semaine}}".
```

## Alerte technique à l'agence (WF13)

<!-- modele: sms-alerte-technique -->
```texte
Andy Construct · n8n : erreur dans "{{workflow}}" (étape {{noeud}}) à {{heure}}. Détails par e-mail, sans donnée personnelle.
```
