# Décisions du chef de projet (v2)

Arbitrages rendus après lecture de `architecture-cro.md` (§15) et `copy-deck.md`. Ils s'imposent à tous les agents.

| # | Sujet | Décision | Pourquoi |
|---|---|---|---|
| D1 | Nom du 4e service | Navigation et cartes : « Cloisons isolantes ». Page `cloisons-isothermes.html`, H1 « Cloisons isothermes et isolantes ». À valider par le client (C-question ajoutée). | Le client dit « isotherme » ; en ligne le mot renvoie aux chambres froides (analyse concurrentielle). On garde les deux. |
| D2 | Consentement du formulaire | **Pas de case à cocher.** Mention d'information sous le bouton d'envoi avec lien vers la politique de confidentialité. L'API ne doit plus exiger de champ de consentement. | La nLPD n'exige pas de consentement pour traiter une demande que la personne fait elle-même ; l'information suffit. Une case de plus = friction. À relire par un juriste. |
| D3 | Guides (aimants) | Téléchargement **libre**, sans e-mail obligatoire. Proposition facultative : « Recevoir aussi la version imprimée par la poste » (formulaire court). La plaquette de références pour professionnels : téléchargement libre aussi. | Public senior méfiant face aux formulaires ; la valeur est la confiance, pas la capture d'adresse. |
| D4 | OMC dans le bandeau | Preview : nom affiché. Production : remplacé par la Salle de l'Alhambra tant qu'il n'y a pas d'accord écrit de l'OMC. | Nom et sigle potentiellement protégés (LPNE). |
| D5 | Libellé de la preuve sociale | « Ils nous ont confié des travaux » | Plus exact. |
| D6 | Modes de génération | `--mode preview` (défaut : textes définitifs, bandeau « version de validation », noindex) · `--mode verification` (idem + surlignage discret des éléments à confirmer avec leur code Cxx, pour la séance de validation) · `--mode production` (textes de repli pour tout ce qui n'est pas confirmé, logos `autorise` uniquement, photos « retirer en production » exclues, indexable). Les confirmations se pilotent dans un seul fichier : `tools/build/donnees/confirmations.json`. | Le client voit la version cible, valide point par point, et la production ne publie jamais un contenu non confirmé. |
| D7 | Fichiers des aimants | `site/assets/docs/andy-construct-references.pdf`, `site/assets/docs/guide-reduire-le-bruit.pdf`, `site/assets/docs/checklist-chantier-site-occupe.pdf` | Noms communs au frontend, aux supports et à l'automatisation. |
| D8 | Particuliers hors Genève | Question au client (C21). D'ici là : toute la Suisse romande pour tous. | Information manquante. |
