# Notification interne · nouvelle demande

| | |
|---|---|
| Canal | E-mail aux associés (`destinataires_internes` de `site/api/config.php`), pour **chaque** demande, même si n8n est en panne |
| Déclencheur | `site/api/demande.php`, juste après la validation |
| Expéditeur | Andy Construct <site@andyconstruct.ch> ; « Répondre » écrit directement au prospect (Reply-To) |
| Contenu produit par | `site/api/lib/Modeles.php`, méthode `interne()` (HTML + texte). Ce fichier décrit le rendu ; le texte se modifie dans le code. |
| Pièces jointes | Photos et plans joints si leur poids total ne dépasse pas 20 Mo, sinon liens signés valables 7 jours |
| Aimants | Notification seulement pour les profils professionnels et les envois postaux (`notifier_aimants`) |

## Objet

```
[A] Nouvelle demande · Isolation acoustique · 1222 Vésenaz · Françoise Dupont
[B] Demande de rappel · 022 345 67 89 · lieu non indiqué · nom non indiqué
[Hors cible] Nouvelle demande · Autres travaux · Annemasse · Jean Martin
[Aimant] Réduire le bruit dans un appartement · Régie, gérance ou coopérative · Bernard
```

En mode test, l'objet commence par `[TEST]`.

## Structure du message (version texte)

<!-- modele: notification-interne-exemple -->
```texte
Objet : [A] Nouvelle demande · Isolation acoustique · Vésenaz · Françoise Dupont

Priorité A · score 71 · à contacter avant lundi 2 novembre 2026 à 12 h 07
Réf. AC-2026-0001 · reçue le lundi 2 novembre 2026 à 10 h 07 · formulaire devis

APPELER : 079 123 45 67 (tel:+41791234567)
Écrire : f.dupont@exemple.ch (« Répondre » écrit directement à la personne)

- Nom : Madame Françoise Dupont
- Téléphone : 079 123 45 67 (mobile)
- E-mail : f.dupont@exemple.ch
- Vous êtes : Particulier propriétaire
- Travaux : Isolation acoustique
- Surface : 15 à 50 m² (1 ou 2 pièces)
- Délai : Dans 1 à 3 mois
- Lieu : Vésenaz (canton GE, zone 1)
- Connu par (déclaré) : Recherche Google

Message :
On entend tout le voisin du dessus, surtout le soir.

Fichiers (2) :
- photo-plafond.jpg (2,4 Mo) : en pièce jointe

Score détaillé (71 points) :
- Type de client (proprietaire) : +15
- Service (isolation-acoustique) : +15
- Ampleur (15-50) : +8
- Zone (1) : +15
- Délai (1-3-mois) : +8
- Source (recherche-google) : +7
- Bonus (téléphone fourni) : +3

Source : recherche naturelle (www.google.ch) · formulaire envoyé depuis /contact.html

Actions en un clic :
- J'ai eu la personne : https://n8n.andyconstruct.ch/webhook/ac-action?t=…
- Pas de réponse : https://n8n.andyconstruct.ch/webhook/ac-action?t=…
- Hors cible : https://n8n.andyconstruct.ch/webhook/ac-action?t=…

Accusé de réception : envoyé à f.dupont@exemple.ch
Attribuée à : Caroline Chanton Bajrami (rôle terrain)
Contrôle anti-robot : jeton ok, formulaire rempli en 75 s
```

## Version HTML

- Bandeau de couleur selon la priorité (A rouge foncé, B brun, C et hors cible anthracite), texte blanc, 19 px.
- Gros bouton « Appeler le 079 123 45 67 » (lien `tel:`), utilisable d'un pouce sur le chantier.
- Tableau des champs, message dans un encadré, fichiers, boutons d'action, score détaillé repliable.
- Aucune image externe, aucun suivi d'ouverture.

## Règles

- Les boutons d'action ouvrent une **page de confirmation** (n8n, WF02) : un simple aperçu du lien par la messagerie ne déclenche rien.
- Le score ordonne les rappels ; il ne remplace jamais le jugement de l'associé. « Hors cible » propose une réponse de réorientation, **validée par un associé** avant envoi (`reorientation-hors-cible.md`).
