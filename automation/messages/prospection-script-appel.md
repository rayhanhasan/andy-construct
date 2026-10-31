# Prospection B2B : script d'appel et e-mail sur demande (scénario j, touches 2 et 3)

| | |
|---|---|
| Qui | Associé « bureau », 5 appels de 5 minutes le lundi ou le mardi |
| Avant d'appeler | Vérifier dans l'annuaire que le numéro **ne porte pas d'astérisque** (refus de publicité, LCD art. 3 al. 1 let. u). Appeler depuis un numéro **affiché et inscrit dans l'annuaire** (let. v). Aucun enregistrement de l'appel. |
| Après l'appel | Un clic sur le résultat dans l'e-mail du lundi (WF02) : « Intéressé, envoyer le PDF » · « Rappeler le … » · « Pas maintenant (12 mois) » · « Ne plus contacter » |
| E-mail | **Uniquement** si la personne l'a demandé au téléphone ; rédigé et envoyé **à la main** depuis la boîte de l'associé, jamais en série |

## Script (5 points, environ 5 minutes)

<!-- modele: script-appel -->
```texte
1. Se présenter et rappeler le courrier
   « Bonjour {{civilite_destinataire}} {{nom_destinataire}}, {{associe}}, d'Andy Construct à Carouge. Je vous ai écrit la semaine dernière au sujet de nos travaux de plâtrerie et de peinture. Avez-vous deux minutes ? »
   Si non : « Quand puis-je vous rappeler ? » (noter le créneau, clic « Rappeler le … »).

2. Une question ouverte, puis écouter
   Régie : « Comment choisissez-vous vos entreprises pour les fins de bail et les cages d'escalier ? »
   Architecte : « Avez-vous des transformations en cours avec des lots de plâtrerie ou d'acoustique ? »
   Commune : « Comment une entreprise est-elle invitée à remettre une offre chez vous, pour les procédures sur invitation ? »

3. Une preuve adaptée à la réponse (une seule)
   Une référence comparable et publique : le lieu, le type de travaux, l'année.
   « Nous avons par exemple refait {{exemple_reference}}. »

4. Une proposition simple
   « Puis-je vous envoyer notre dossier de références et deux fiches de chantiers proches de vos besoins ? »
   ou : « Nous avons un chantier en cours à {{commune_chantier}} : je vous le fais visiter, vingt minutes, quand cela vous arrange. »

5. Demander l'accord pour la suite
   « Nous envoyons aussi quatre fois par an une lettre très courte : un chantier, un point technique. Puis-je vous l'adresser ? »
   Noter la réponse (date, canal, associé). Sans accord clair : rien.
```

## Réponses aux objections fréquentes

<!-- modele: objections -->
```texte
« Nous avons déjà nos entreprises. »
→ « C'est normal. Beaucoup de régies gardent une deuxième entreprise pour les périodes chargées. Je vous envoie le dossier, sans engagement ? »

« Envoyez-moi un e-mail. »
→ « Volontiers. À quelle adresse ? Je vous envoie le dossier et deux exemples aujourd'hui. » (e-mail de la touche 3 ci-dessous)

« Nous passons par des appels d'offres. »
→ « Pouvez-vous nous inscrire sur la liste des entreprises invitées ? Nos attestations sont prêtes. »

« Pas maintenant. »
→ « Je comprends. Puis-je vous rappeler dans un an ? » (clic « Pas maintenant (12 mois) »)

« Ne m'appelez plus. »
→ « C'est noté, je vous retire de notre liste. Bonne journée. » (clic « Ne plus contacter », le jour même)
```

## Touche 3 · E-mail après l'appel (seulement sur demande, rédigé individuellement)

<!-- modele: email-apres-appel -->
```texte
Objet : Suite à notre appel : références Andy Construct

{{salutation}},

Merci pour votre accueil au téléphone. Comme convenu, voici notre dossier de références (PDF) et deux exemples proches de ce dont nous avons parlé :
- {{fiche_1}}
- {{fiche_2}}

Nos attestations (AVS, LPP, assurance responsabilité civile) sont disponibles sur simple demande.
{{#lien_double_optin}}
Si vous souhaitez recevoir notre lettre trimestrielle (un chantier, un point technique, quatre fois par an), confirmez ici : {{lien_double_optin}}
{{/lien_double_optin}}
Je reste à votre disposition au {{mobile_associe}}.

Meilleures salutations,

{{signature}}
```

## Touche 4 · Intéressé, 30 jours après (individuel)

<!-- modele: email-visite-chantier -->
```texte
Objet : Un chantier en cours à {{commune_chantier}}, si vous voulez voir

{{salutation}},

Nous réalisons en ce moment {{description_chantier}} à {{commune_chantier}}. Si cela vous intéresse, je vous le fais visiter, vingt minutes, à l'heure qui vous convient.

Meilleures salutations,

{{signature}}
```
