# Prospection B2B : lettres postales (scénario j, touches 1 et 4)

| | |
|---|---|
| Canal | **Courrier postal adressé**, nominatif (hors du champ de l'art. 3 al. 1 let. o LCD, qui vise la télécommunication). Envoi par Pingen ou impression maison, avec le dossier de références imprimé. |
| Jamais | Aucun e-mail à froid, aucune séquence automatique d'e-mails vers des régies, architectes ou communes (stratégie §9.2). |
| Déclencheur | WF10 le lundi : 5 comptes « À contacter » ; l'agence vérifie la liste (contact nommé, adresse, astérisque dans l'annuaire). |
| Signature | Associé « bureau », avec son numéro direct (appel de suivi à J+6, numéro affiché et inscrit dans l'annuaire). |
| Format | A4, une page, logo en tête, texte 11-12 pt, coordonnées complètes et IDE en pied (identification de l'expéditeur). |
| Arrêt | Une demande d'arrêt (téléphone, lettre, e-mail) est notée « Ne plus contacter » le jour même. |

Variables : `civilite_destinataire` (« Madame », « Monsieur »), `nom_destinataire`, `fonction`, `organisation`, `adresse_destinataire`, `date`, `reference_1`, `reference_2` (références **publiques et validées** uniquement), `associe`, `mobile_associe`, `commune_chantier`, `description_chantier`.

## Touche 1 · Régie, gérance, coopérative

<!-- modele: lettre-regie -->
```texte
Objet : Plâtrerie, peinture et isolation acoustique pour vos immeubles

{{civilite_destinataire}},

Andy Construct est une entreprise de Carouge, inscrite au registre du commerce depuis 2007. Nous posons des cloisons et des faux-plafonds en plaques de plâtre, nous peignons à l'intérieur, et nous isolons contre le bruit et contre le froid, dans toute la Suisse romande.

Pour vos remises en état de fin de bail, vos cages d'escalier et vos travaux en immeuble habité, nous protégeons les lieux, informons les locataires et rendons un chantier propre. Nous avons notamment réalisé des travaux pour {{reference_1}} et {{reference_2}} ; vous trouverez d'autres références dans le dossier joint.

Je me permettrai de vous appeler la semaine prochaine, pour savoir si nous pouvons figurer parmi les entreprises que vous consultez. Si vous préférez ne pas être appelé(e), un simple message suffit.

Avec mes meilleures salutations,

{{associe}}
Associé · Andy Construct
{{mobile_associe}} · +41 22 771 20 15

Vos coordonnées professionnelles proviennent de {{source_coordonnees}}. Elles servent uniquement à vous présenter notre entreprise. Comment nous les traitons : www.andyconstruct.ch/confidentialite.html
```

## Touche 1 · Bureau d'architectes

<!-- modele: lettre-architecte -->
```texte
Objet : Lots de plâtrerie, faux-plafonds et acoustique (CFC 271 et 283)

{{civilite_destinataire}},

Andy Construct est une entreprise de plâtrerie, de peinture et d'isolation intérieure basée à Carouge, inscrite au registre du commerce depuis 2007. Nous exécutons des cloisons, des doublages et des faux-plafonds en plaques de plâtre, des isolations acoustiques désolidarisées et de la peinture intérieure, en neuf comme en transformation.

Nous avons réalisé notamment {{reference_1}} et {{reference_2}}. Le dossier joint présente nos références, notre organisation en site occupé et les lots que nous traitons.

Je me permettrai de vous appeler la semaine prochaine : si vous avez des transformations en préparation, nous serions heureux d'être consultés pour les lots concernés, ou de relire un descriptif sur les points d'exécution. Si vous préférez ne pas être appelé(e), un simple message suffit.

Avec mes meilleures salutations,

{{associe}}
Associé · Andy Construct
{{mobile_associe}} · +41 22 771 20 15
```

## Touche 1 · Commune, service des bâtiments

<!-- modele: lettre-commune -->
```texte
Objet : Inscription sur votre liste d'entreprises consultées (plâtrerie, peinture, isolation)

{{civilite_destinataire}},

Andy Construct est une entreprise de Carouge, inscrite au registre du commerce depuis 2007, spécialisée en plâtrerie, faux-plafonds, peinture intérieure et isolation acoustique.

Nous avons travaillé pour des maîtres d'ouvrage publics, notamment {{reference_1}} et {{reference_2}}. Le dossier joint présente nos références et notre organisation dans des bâtiments occupés (écoles, salles communales).

Nous souhaiterions figurer parmi les entreprises consultées pour vos procédures de gré à gré et sur invitation. Nos attestations (AVS, LPP, assurance responsabilité civile, impôts, TVA) sont disponibles sur simple demande. Je me permettrai de vous appeler pour savoir à qui les adresser.

Avec mes meilleures salutations,

{{associe}}
Associé · Andy Construct
{{mobile_associe}} · +41 22 771 20 15
```

## Touche 4 · Deuxième courrier (contact non joint au téléphone, J+45)

<!-- modele: lettre-relance-chantier -->
```texte
Objet : Un chantier récent{{#commune_chantier}} à {{commune_chantier}}{{/commune_chantier}}

{{civilite_destinataire}},

Je vous ai écrit il y a quelques semaines sans parvenir à vous joindre ensuite. Voici un exemple récent de notre travail : {{description_chantier}}. La fiche du projet est jointe.

Si vous avez un besoin en plâtrerie, peinture ou isolation, je reste à votre disposition au {{mobile_associe}}. Ce sera mon dernier courrier ; si vous ne souhaitez plus en recevoir, un simple message suffit.

Avec mes meilleures salutations,

{{associe}}
Associé · Andy Construct
{{mobile_associe}} · +41 22 771 20 15
```

## À valider avant tout envoi

- « Inscrite au registre du commerce depuis 2007 » (`C` du copy deck) et les références citées (accord écrit pour toute marque privée ; armoiries publiques jamais en logo, programme v2 §4).
- Disponibilité réelle des attestations (`stratégie` §3.7).
- Pied de page de la lettre : raison sociale complète, adresse, IDE CHE-113.706.162.
