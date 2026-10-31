# Réponse de réorientation (demande hors cible)

| | |
|---|---|
| Canal | E-mail depuis la boîte de l'associé, **jamais automatique** : l'associé relit le texte et clique « Envoyer la réponse de réorientation » (WF02). Sans e-mail : l'associé appelle. |
| Déclencheur | Priorité « hors cible » (service hors des 4 métiers, ou lieu hors de Suisse romande) |
| Délai | Moins d'un jour ouvrable |
| Ton | Franc et serviable : dire ce que nous ne faisons pas, orienter si possible. C'est un « conseil honnête » (personas §3.3), pas un refus sec. |

Variables : `salutation`, `travaux_demandes`, `commune`, `signature`.

## Travaux hors de nos quatre métiers

<!-- modele: reorientation-service -->
```texte
Objet : Votre demande : ce que nous pouvons faire

{{salutation}},

Merci pour votre demande. Pour être francs avec vous : {{travaux_demandes}} ne fait pas partie de nos métiers. Nous posons du placo (cloisons, doublages, faux-plafonds), nous peignons à l'intérieur, et nous isolons contre le bruit et contre le froid.

Pour ces travaux, une entreprise spécialisée vous servira mieux que nous. Si votre projet comprend aussi une partie qui relève de nos métiers, nous la chiffrons volontiers : il suffit de répondre à ce message ou d'appeler le +41 22 771 20 15.

Meilleures salutations,

{{signature}}
```

## Lieu hors de notre zone

<!-- modele: reorientation-zone -->
```texte
Objet : Votre demande{{#commune}} à {{commune}}{{/commune}}

{{salutation}},

Merci pour votre demande. Nous intervenons dans toute la Suisse romande, mais {{commune}} est en dehors de la zone où nous pouvons organiser un chantier dans de bonnes conditions (déplacements, suivi, délais).

Nous préférons vous le dire tout de suite plutôt que de vous faire attendre. Une entreprise proche de chez vous sera plus réactive. Si nous nous sommes trompés sur le lieu des travaux, répondez simplement à ce message.

Meilleures salutations,

{{signature}}
```
