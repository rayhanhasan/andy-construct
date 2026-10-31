# Copy deck : textes définitifs du site v2 d'Andy Construct

*Phase 2 du programme v2 · copywriter senior et architecte CRO · 31 octobre 2026*
*Structure des pages, composants et comportements : `architecture-cro.md`. Les deux documents partagent les identifiants de confirmation `C01` à `C44` (liste complète au §R).*

Les textes ci-dessous s'intègrent **tels quels**, dans l'ordre d'affichage. Le générateur ajoute les espaces insécables (fonction `fr()` de `tools/build/common.py`).

---

## 0. Conventions

### 0.1 Ton

- Vouvoiement ; « nous » pour l'entreprise. Phrases courtes, une idée par phrase, le concret d'abord.
- Aucun superlatif, aucune promesse invérifiable, aucun anglicisme, aucun jargon marketing.
- Le bénéfice d'abord pour les particuliers (« moins de bruit chez vous »), le détail technique ensuite et seulement sur les pages ou encadrés pour les professionnels (CFC, SIA).
- Lieux, années, noms : seulement s'ils sont vrais et confirmés.

### 0.2 Lexique retenu

| Sujet | Terme retenu | Pourquoi |
|---|---|---|
| Action principale | **« Demander un devis »**, partout | C'est le mot des particuliers et celui des recherches (« devis peinture ») ; les professionnels le comprennent. Un seul libellé évite de croire à deux démarches (audit n° 16). |
| Document remis après la visite | **« offre écrite »** ; sur les pages pour particuliers, la 1re fois : « offre écrite (votre devis) » | Mot des professionnels (régies, architectes, communes), expliqué aux particuliers. |
| Bouton du formulaire | « Envoyer ma demande » | Verbe + objet, dit ce qui se passe. |
| Métier | « placo » et « plaques de plâtre » ; « plâtrerie », « gypserie » sur les pages pros | « Placo » est le mot du public, mais c'est une marque : on l'accompagne de « plaques de plâtre ». |
| Bruit | « isolation phonique » (le mot des particuliers) et « isolation acoustique » (le nom du service) ; « correction acoustique » pour l'écho | Distinguer **isoler** (le bruit qui passe) et **corriger** (l'écho dans la pièce). |
| 4e service | **« Cloisons isolantes »** ; « isothermes » en synonyme dans le H1 et le texte | « Isotherme » évoque les chambres froides (`C16`). Repli : « Cloisons isothermes » partout. |
| Régies | « régies et gérances » | Jamais « travaux en régie » (= facturés au temps passé). |
| Copropriété | « PPE (propriété par étages) » à la première mention | Compris en Suisse romande, mais expliqué une fois. |
| Téléphone | `+41 22 771 20 15` (bureau), `+41 78 631 14 34` (sur les chantiers) | Format de la charte, identique partout (NAP). |
| Montants | CHF, apostrophe pour les milliers (1'500) | Usage suisse. |

### 0.3 Mots interdits

« solution(s) », « expertise », « expert », « premium », « haut de gamme », « excellence », « exceptionnel », « passion », « leader », « n° 1 », « meilleur », « innovant », « sur mesure » (sauf sens strictement technique), « clé en main », « sans stress », « garantie décennale », « parfait achèvement », « certifié » ou « agréé » sans document, « devis gratuit » ou un délai tant qu'ils ne sont pas confirmés, « partenaire » pour une référence, « ils nous recommandent ». Anglicismes : « team », « best », « process », « feedback », « call ».

### 0.4 Marqueurs

- `[À CONFIRMER Cxx : …]` : le texte qui précède contient une donnée à confirmer par le client. **Repli** : le texte publié en production si la confirmation manque (« masqué » = le bloc ou la phrase disparaît).
- `[À VÉRIFIER : …]` : point à vérifier par l'agence (qualité d'une photo, relecture juridique).
- `{{variable}}` : valeur insérée par le script (page merci).
- En production, aucune de ces marques ne doit rester dans le HTML (`architecture-cro.md` §14).

---

## A. Éléments communs à toutes les pages

### A.1 En-tête (ordinateur)

- Lien d'évitement : « Aller au contenu »
- Logo, texte alternatif : « Andy Construct, page d'accueil »
- Menu :
  - « Prestations » (bouton qui ouvre le panneau) :
    - « Placo » — « Cloisons, doublages, faux-plafonds »
    - « Peinture » — « Murs et plafonds, à l'intérieur »
    - « Isolation acoustique » — « Contre le bruit et l'écho »
    - « Cloisons isolantes » — « Caves, garages, combles » `[À CONFIRMER C16 : nom affiché]` Repli : « Cloisons isothermes »
  - « Réalisations »
  - « Professionnels »
  - « L'entreprise »
  - « Contact »
- Téléphone : petit libellé « Lun-ven, 7 h – 18 h » `[À CONFIRMER C03]` (repli : « Appelez-nous »), puis « +41 22 771 20 15 »
- Bouton : « Demander un devis »

### A.2 En-tête et menu (mobile)

- Bouton : « Menu » ; une fois ouvert : « Fermer »
- Menu ouvert : titre « Prestations », puis Placo · Peinture · Isolation acoustique · Cloisons isolantes ; puis Réalisations · Professionnels · L'entreprise · Contact.
- En bas du menu : bouton « Appeler le +41 22 771 20 15 », bouton « Demander un devis ».

### A.3 Barre fixe (mobile)

- Nom de la région (lecteurs d'écran) : « Contact rapide »
- Bouton 1 : « Appeler » (variante du test T6 : « Appeler le 022 771 20 15 »)
- Bouton 2 : « Demander un devis »

### A.4 Pied de page

**Marque** (sous le logo blanc) :
> Placo, peinture, isolation acoustique et cloisons isolantes. Entreprise de Carouge, inscrite au registre du commerce depuis 2007. Toute la Suisse romande.

**Nous joindre** (bloc `<address>`, même texte partout) :
> Andy Construct
> Route des Acacias 48
> 1227 Carouge (Genève)
> Tél. +41 22 771 20 15
> Sur les chantiers : +41 78 631 14 34
> contact@andyconstruct.ch `[À CONFIRMER C30 : adresse sur le domaine]` Repli : andy.construct@bluewin.ch
> Du lundi au vendredi, 7 h – 18 h `[À CONFIRMER C03]` Repli : masqué

Lien : « Voir sur la carte »

**Prestations** : « Placo » · « Peinture » · « Isolation acoustique » · « Cloisons isolantes »

**Andy Construct** : « Réalisations » · « Professionnels » · « L'entreprise » · « Contact » · « Dossier de références (PDF, {{poids}}) »

**Ligne de références** (pleine largeur) : texte du §A.6.

**Barre basse** :
> © 2026 Andy Construct, Chanton & Cie · IDE CHE-113.706.162

Liens : « Vérifier au registre du commerce » · « Mentions légales » · « Protection des données » · (« Paramètres des cookies » : seulement si un bandeau de consentement existe)

L'année est produite au build.

### A.5 Bloc de demande (`#demande`)

**Accueil, professionnels, contact** :
- Surtitre : « Votre demande »
- H2 : « Demander un devis »
- Introduction : « 3 étapes, environ une minute. Nous vous rappelons pour convenir d'une visite. »

**Pages services** (étape 1 déjà faite) :
- H2 : « Demander un devis pour du placo » · « Demander un devis pour de la peinture » · « Demander un devis pour une isolation acoustique » · « Demander un devis pour une cloison isolante »
- Introduction : « Encore 2 étapes, moins d'une minute. Nous vous rappelons pour convenir d'une visite. »

**Formulaire** : libellés, aides, valeurs, validations et messages d'erreur dans `architecture-cro.md` §6.2 à §6.4 (source unique pour le formulaire). Résumé de l'étape 1 préremplie : « Travaux : {{service}} · Modifier ».

**Réassurance**, 3 lignes sous le formulaire, visibles à chaque étape (et donc sous le bouton « Envoyer ma demande » à l'étape 3) :
1. « Nous vous rappelons le jour même ou le jour ouvrable suivant. » `[À CONFIRMER C01 : délai de rappel tenable]` Repli : « Nous vous rappelons pendant nos heures de bureau. »
2. « La visite et le devis sont gratuits et sans engagement. » `[À CONFIRMER C02]` Repli : « Vous décidez une fois l'offre écrite reçue. »
3. « Vos coordonnées servent uniquement à votre demande. Pas de publicité. »

**Case de consentement** (tant que l'API l'exige) : « J'accepte que mes coordonnées servent uniquement à traiter ma demande (protection des données). »
**Mention d'information** (si la case est retirée après avis du juriste) : « En envoyant ce formulaire, vous nous transmettez vos coordonnées pour traiter votre demande. Elles ne servent à rien d'autre. » + lien « Protection des données ».

**Sous chaque bouton d'étape** : « Vous préférez qu'on vous rappelle ? » (lien vers le module). Le numéro n'est pas répété ici : il figure dans la colonne « Par téléphone » à côté du formulaire, dans l'en-tête et dans la barre mobile.

**À partir de l'étape 2**, au-dessus des champs : « Les champs obligatoires sont indiqués. »

**Colonne de droite** (sous le module de rappel du §A.7) :
- Titre : « Par téléphone »
- « Bureau : +41 22 771 20 15 »
- « Sur les chantiers : +41 78 631 14 34 »
- « Du lundi au vendredi, 7 h – 18 h » `[À CONFIRMER C03]` Repli : masqué
- Ligne de références courte (§A.6), sauf sur la page Professionnels.

### A.6 Références : bandeau, ligne courte, phrase

**Bandeau de l'accueil** :
- Titre : « Ils nous ont confié des travaux »
- 8 noms, dans cet ordre : Ville de Genève · Conservatoire de musique de Genève · HEAD – Genève · OMC `[À CONFIRMER C22 : accord écrit de l'OMC pour le nom]` (repli : Salle de l'Alhambra) · UBS · Piaget · Mairie de Plan-les-Ouates · Salle communale de Collonge-Bellerive
- Phrase sous les noms : « Et des particuliers, pour une cloison, un plafond ou une pièce à repeindre. » `[À CONFIRMER C04 : petits chantiers acceptés]` Repli : « Et des particuliers, à Genève et dans toute la région. »
- Lien : « Voir toutes nos références »
- En production, quand les accords sont archivés, en petit : « Références citées avec l'accord des maîtres d'ouvrage. »

**Ligne courte** (près des formulaires, page contact, pied de page) :
> Ils nous ont confié des travaux : Ville de Genève · Conservatoire de musique de Genève · HEAD – Genève · Mairie de Plan-les-Ouates · Salle communale de Collonge-Bellerive · et des particuliers de toute la région.

### A.7 Module de rappel

Textes dans `architecture-cro.md` §7 (titre « Vous préférez qu'on vous rappelle ? », phrase « Laissez simplement votre numéro. », champs, bouton « Être rappelé(e) », messages).

Phrase sous le bouton, **à côté d'un formulaire** (accueil, pages services, professionnels, contact : le délai figure déjà dans la réassurance) :
> Votre numéro ne sert qu'à ce rappel.

Phrase sous le bouton, **module seul** (réalisations) :
> Nous vous rappelons le jour même ou le jour ouvrable suivant. Votre numéro ne sert qu'à ce rappel.

`[À CONFIRMER C01]` Repli : « Nous vous rappelons pendant nos heures de bureau. Votre numéro ne sert qu'à ce rappel. »

### A.8 Méthode en 4 étapes (texte unique)

**Version complète** (accueil, entreprise, professionnels) :
- Surtitre : « Comment nous travaillons »
- 1. **Visite** — « Nous venons voir les lieux, prenons les mesures et écoutons votre besoin. »
- 2. **Offre écrite** — « Détaillée poste par poste, en CHF, avec la durée des travaux et ce qui n'est pas compris. » `[À CONFIRMER C06]` Repli : « Nous vous remettons une offre écrite. »
- 3. **Chantier protégé** — « Sols, meubles et passages protégés. Nettoyage chaque soir, et à fond le dernier jour. » `[À CONFIRMER C07]` Repli : « Les lieux sont protégés pendant les travaux. »
- 4. **Réception** — « Nous faisons le tour des finitions avec vous. Une retouche ? Nous revenons. » `[À CONFIRMER C32]` Repli : « Nous contrôlons les finitions avec vous. »
- Engagement (encadré sous les étapes) : « Aucun travail supplémentaire sans votre accord écrit et chiffré. » `[À CONFIRMER C06]` Repli : masqué

**Version courte** (pages services) :
- H2 : « Comment se passe un chantier »
- « 1. Visite : mesures et conseils sur place. »
- « 2. Offre écrite : poste par poste, en CHF. » `[C06]` Repli : « 2. Offre écrite. »
- « 3. Chantier protégé, nettoyé chaque soir. » `[C07]` Repli : « 3. Chantier protégé. »
- « 4. Réception : le tour des finitions, ensemble. »
- Lien : « Notre méthode en détail »

### A.9 Bande d'appel (pages sans formulaire)

- H2 : « Vous avez un projet ? »
- Phrase : « Décrivez-le en trois étapes ou appelez-nous : nous convenons d'une visite. »
- Boutons : « Demander un devis » · « Appeler le +41 22 771 20 15 »

### A.10 Bandeau de la version de validation (preview uniquement)

> Version de validation. Les passages soulignés en pointillé attendent votre confirmation.

Bouton : « Masquer ce message »

### A.11 Témoignages et avis (affichés seulement quand ils existent)

- H2 : « Ce qu'en disent nos clients » `[C44 : témoignages réels, accords écrits]`
- Format d'une citation : « {{texte exact}} » — {{nom ou fonction}}, {{organisation}}, {{commune}} · {{nature des travaux}}, {{année}}
- Note sous le bloc : « Témoignages publiés tels quels, avec l'accord écrit de leurs auteurs. »
- Avis Google (dès 5 avis) : « Avis Google : {{note}} sur 5, {{nombre}} avis (relevé le {{date}}). » Lien : « Lire les avis sur Google »

---

## B. Accueil (`index.html`)

### Métadonnées

- **Title** (58 car.) : `Plâtrerie, peinture et isolation à Genève | Andy Construct`
- **Meta description** (155 car.) : `Placo, peinture, isolation acoustique et cloisons isolantes. Entreprise de Carouge depuis 2007, active dans toute la Suisse romande. Tél. +41 22 771 20 15.`
- **og:title** : `Andy Construct · Placo, peinture et isolation en Suisse romande`
- **og:image:alt** : `Faux-plafond en plaques de plâtre à gorge lumineuse, posé par Andy Construct`

### B.1 Héro

- Surtitre : « Carouge · depuis 2007 »
- **H1** : « Placo, peinture et isolation en Suisse romande »
- Sous-titre : « Cloisons, plafonds, isolation contre le bruit et peinture : un seul interlocuteur, de la pose des plaques à la dernière couche. » `[À CONFIRMER C05 : les 4 métiers réalisés ou coordonnés par l'entreprise]` Repli : « Cloisons, plafonds, isolation contre le bruit et peinture, pour les particuliers et les professionnels. »
- Bouton 1 : « Demander un devis »
- Bouton 2 : « Appeler le +41 22 771 20 15 »
- Sous les boutons : « Du lundi au vendredi, de 7 h à 18 h. » `[C03]` Repli : masqué
- Faits (liste « En bref ») :
  - **Depuis 2007** — Inscrite au registre du commerce
  - **Siège à Carouge** — Chantiers dans toute la Suisse romande
  - **Visite et devis gratuits** — Offre écrite, sans engagement `[À CONFIRMER C02]` Repli : **Particuliers et professionnels** — Régies, architectes, communes

### B.2 Bandeau de références

Texte du §A.6 (bandeau).

### B.3 Prestations

- Surtitre : « Nos quatre métiers »
- **H2** : « Quatre métiers, souvent sur le même chantier »
- Cartes :
  1. **Placo** — « Cloisons, doublages et faux-plafonds en plaques de plâtre. » — « Pour : logements, bureaux, commerces, salles. » — lien « Voir le placo »
  2. **Peinture** — « Murs et plafonds préparés, peints, et la pièce rendue propre. » — « Pour : appartements, fins de bail, cages d'escalier, bureaux. » — lien « Voir la peinture »
  3. **Isolation acoustique** — « Vous entendez vos voisins ? Nous isolons murs et plafonds. » — « Pour : logements, bureaux, salles communales. » — lien « Voir l'isolation acoustique »
  4. **Cloisons isolantes** — « Une pièce froide contre un garage ou une cave ? Nous l'isolons. » — « Pour : villas, immeubles, locaux d'activité. » — lien « Voir les cloisons isolantes »
- Sous les cartes : « Vous hésitez ? Décrivez votre besoin : nous vous orientons. »
- Bouton : « Demander un devis »

### B.4 Réalisations

- Surtitre : « Réalisations »
- **H2** : « Des chantiers réels, photographiés par notre équipe »
- Carte 1 (photo `faux-plafond-placo-gorge-lumineuse-01`) :
  - « Hall et couloirs : faux-plafond à gorge lumineuse »
  - « Immeuble, canton de Genève » `[À CONFIRMER C25 : type de bâtiment et commune]` Repli : « Hall d'immeuble »
  - Contrainte : `[À CONFIRMER C25 : contrainte résolue, 1 ligne, fournie par le client]` Repli : « Formes courbes, éclairage et spots intégrés au plafond. »
  - Étiquettes : « Placo · Peinture » `[C25]` Repli : « Placo »
- Carte 2 (photo `chantier-ossature-puits-de-lumiere-01`, badge « Pendant les travaux ») :
  - « Grande salle : ossature et isolant avant la fermeture »
  - « Salle publique, canton de Genève » `[C25]` Repli : « Salle publique »
  - Contrainte, repli : « Travail en hauteur, autour de puits de lumière. »
  - Étiquettes : « Placo » et `[À CONFIRMER C25 : « Isolation acoustique » ou « Cloisons isolantes », selon l'isolant posé]` Repli : « Placo »
- Carte 3 (paire avant / après AA6) :
  - « Séjour : faux-plafond et spots, avant et après »
  - « Appartement » `[À CONFIRMER C26 : commune]`
  - Contrainte : `[C26]` Repli : « Un plafond redessiné, l'éclairage intégré. »
  - Étiquettes : « Placo · Peinture » `[C26]`
  - `[À VÉRIFIER : qualité de la paire AA6]` Si elle est insuffisante, carte de remplacement (photo `habillage-placo-niches-arrondies-01`, badge « Pendant les travaux ») : « Cage d'escalier : habillage à niches arrondies » · « Immeuble » · « Formes arrondies, escalier protégé pendant les travaux. » · « Placo »
- Lien : « Voir toutes les réalisations »
- Bouton : « Un projet semblable ? Demander un devis »

### B.5 Comment nous travaillons

- **H2** : « De la visite à la réception, quatre étapes »
- Étapes et engagement : §A.8, version complète.
- Lien : « Notre méthode en détail »

### B.6 Bande « professionnels » et zone

- Colonne 1 — **H3** : « Régies, architectes, communes » — « Immeubles habités, offres sur plans et descriptifs, dossier de références à télécharger. » — lien « Espace professionnels »
- Colonne 2 — **H3** : « Toute la Suisse romande » — « Depuis Carouge : Genève, Vaud, Neuchâtel, Fribourg, Valais romand, Jura et Jura bernois. » — lien « Voir la carte »

### B.7 Questions fréquentes (FAQ de l'accueil, 8 questions)

- Surtitre : « Vos questions »
- **H2** : « Questions fréquentes »
- Sous le titre : « Une autre question ? Appelez le +41 22 771 20 15. »

1. **Faites-vous aussi les petits travaux ?**
   Oui. Une pièce à repeindre, une cloison ou un plafond à refaire nous intéressent autant qu'un grand chantier. `[À CONFIRMER C04]` Repli : question masquée.
2. **Combien coûtent vos travaux ?**
   Le prix dépend de la surface, de l'état des murs et des plafonds, de la hauteur, de l'accès et des finitions. Après la visite, vous recevez une offre écrite détaillée, en CHF. `[C06]` Repli : « … Après la visite, vous recevez une offre écrite. »
3. **La visite et le devis sont-ils payants ?**
   Non. La visite et le devis sont gratuits et sans engagement. Vous décidez une fois l'offre écrite reçue. `[À CONFIRMER C02]` Repli : question masquée.
4. **En combien de temps pouvez-vous venir ?**
   Nous vous rappelons le jour même ou le jour ouvrable suivant, et proposons une visite en général dans la semaine. Le délai des travaux figure dans l'offre. `[À CONFIRMER C01, C41]` Repli : « Nous vous rappelons pour convenir d'une date de visite. Le délai des travaux figure dans l'offre écrite. »
5. **Intervenez-vous hors de Genève ?**
   Oui, dans toute la Suisse romande : Vaud, Neuchâtel, Fribourg, Valais romand, Jura et Jura bernois. Nous avons par exemple travaillé à Coppet, à Nyon et à Chavannes-de-Bogis. `[À CONFIRMER C22 : lieux des chantiers]` Repli : sans la dernière phrase.
   `[Variante C21, si le client limite les chantiers de particuliers :]` « Pour les particuliers, nous intervenons dans le canton de Genève et sur La Côte. Pour les régies, architectes, communes et entreprises, dans toute la Suisse romande. »
6. **Comment protégez-vous mon logement pendant les travaux ?**
   Nous couvrons les sols et les meubles, fermons la zone de travail par des bâches si nécessaire et nettoyons chaque soir. Le dernier jour, nous rendons les lieux propres. `[À CONFIRMER C07]` Repli : question masquée.
7. **Travaillez-vous pour les régies, les architectes et les communes ?**
   Oui. La Ville de Genève, des salles communales, le Conservatoire de musique et la HEAD nous ont confié des travaux. Les professionnels trouvent nos documents sur une page dédiée.
8. **Et si un défaut apparaît après les travaux ?**
   Appelez-nous : nous revenons. Pour les contrats conclus depuis 2026, la loi vous laisse 60 jours, dès que vous le découvrez, pour signaler un défaut d'un ouvrage. `[À CONFIRMER C32]` `[À VÉRIFIER : relecture juridique]` Repli : « Appelez-nous : nous venons voir le défaut avec vous. »

### B.8 Demander un devis

Bloc de demande, §A.5 (version accueil), avec le module de rappel (§A.7), la colonne « Par téléphone » et la ligne de références courte.

### B.9 Pied de page

§A.4.

---

## C. Placo (`placo.html`)

### Métadonnées

- **Title** (58 car.) : `Placo, cloisons et faux-plafonds à Genève | Andy Construct`
- **Meta description** (149 car.) : `Cloisons, doublages et faux-plafonds en plaques de plâtre, posés puis peints. Logements, bureaux et bâtiments publics, à Genève et en Suisse romande.` `[C05]` Repli (153 car.) : `Cloisons, doublages et faux-plafonds en plaques de plâtre, prêts à peindre. Logements, bureaux et bâtiments publics, à Genève et en Suisse romande.`

### C.1 En-tête de page

- Fil d'Ariane : « Accueil › Placo »
- **H1** : « Placo : cloisons, doublages et faux-plafonds »
- Chapeau : « Diviser une pièce, redresser un mur, cacher des tuyaux, abaisser un plafond : les plaques de plâtre le permettent sans maçonnerie. Nous posons, puis nous peignons. » `[C05]` Repli : sans la dernière phrase. Lien dans le texte : « nous peignons » → `peinture.html`.
- Boutons : « Demander un devis pour du placo » · « Appeler le +41 22 771 20 15 »
- En bref :
  - « Logements, bureaux, commerces et salles »
  - « Pose, joints et peinture par la même équipe » `[C05]` Repli : « Pose et joints, prêt à peindre »
  - « Genève et toute la Suisse romande »
- Photo : `faux-plafond-placo-gorge-lumineuse-02`, légende « Faux-plafond arrondi en plaques de plâtre, éclairage intégré »

### C.2 Ce que nous posons

- **H2** : « Ce que nous posons en plaques de plâtre »
- Introduction : « Une ossature métallique, des plaques vissées, des joints enduits puis poncés : la même technique sert à quatre ouvrages. »
- **H3 « Cloisons »** (ancre `#cloisons`) : « Une cloison sépare une pièce en deux, ou crée une chambre, un bureau, une salle de réunion. Elle se monte en quelques jours, sans attendre le séchage d'une maçonnerie. Avec un isolant à l'intérieur, elle atténue le bruit d'une pièce à l'autre. Nous prévoyons dès la pose les portes, les prises et les renforts pour fixer un meuble ou une télévision. »
- **H3 « Doublages »** (`#doublages`) : « Un doublage est un parement de plaques posé devant un mur existant. Il redresse un mur abîmé ou irrégulier, laisse passer les gaines électriques et peut recevoir un isolant, contre le froid ou contre le bruit. » Liens dans le texte : « contre le froid » → `cloisons-isothermes.html` ; « contre le bruit » → `isolation-acoustique.html`.
- **H3 « Faux-plafonds »** (`#faux-plafonds`) : « Un faux-plafond est suspendu sous le plafond existant. Il cache conduites et ventilation, accueille spots et trappes de visite, et permet des formes : retombées, courbes, gorges lumineuses. C'est aussi une bonne manière de refaire un plafond fissuré ou abîmé par un dégât d'eau. »
- **H3 « Caissons et habillages »** (`#caissons`) : « Une poutre, une gaine ou un appareil de ventilation à cacher ? Nous construisons un caisson en plaques de plâtre, ajusté à la place disponible, avec une trappe si l'appareil doit rester accessible. »

### C.3 Pour qui ?

- **H2** : « Pour qui ? »
- **Particuliers** : « Créer une chambre ou un bureau, refaire un plafond après un dégât d'eau, cacher des tuyaux, aménager des combles. Nous venons voir, puis nous vous remettons une offre écrite (votre devis). »
- **Professionnels** : « Lots de plâtrerie et de faux-plafonds (CFC 271 et 283), réaménagement de bureaux, remise en état entre deux locataires. Offres établies sur plans et descriptifs. » `[À CONFIRMER C14 : CFC 283]` Repli : « Lots de plâtrerie (CFC 271), réaménagement… » — lien « Espace professionnels »

### C.4 Ce qu'il faut savoir

- **H2** : « Ce qu'il faut savoir avant de commencer »
- « Poncer les joints fait une poussière fine. Nous fermons la zone, protégeons les passages et nettoyons chaque soir. » `[C07]` Repli : « Poncer les joints fait une poussière fine : la zone de travail doit être fermée et protégée. »
- « Les câbles et les gaines passent avant la fermeture : nous coordonnons la pose avec votre électricien. »
- « En salle de bains, on pose des plaques prévues pour l'humidité. Nous ne posons pas le carrelage. »
- « Sur un grand mur éclairé de côté, les joints se voient davantage. Nous choisissons avec vous, à la visite, le niveau de finition qui convient. »
- « Locataire ou copropriétaire ? Certains travaux demandent un accord écrit : voyez les questions plus bas. »

### C.5 Réalisations

- **H2** : « Nos réalisations en placo »
- Fiche principale : projet P1 (§G.3), photo `faux-plafond-placo-gorge-lumineuse-01`.
- Deux photos de plus, avec leur légende :
  - `chantier-suspentes-ossature-01` : « Pendant les travaux : suspentes et ossature d'un faux-plafond, sous une dalle isolée »
  - `habillage-placo-niches-arrondies-01` : « Pendant les travaux : habillage en plaques de plâtre à niches arrondies, escalier protégé »
- « Réalisé notamment pour : `[À CONFIRMER C23 : 3 références pour lesquelles Andy a posé du placo, p. ex. Ville de Genève, Conservatoire de musique de Genève, Energestion]`. » Repli : « Ils nous ont confié des travaux : Ville de Genève · Conservatoire de musique de Genève · HEAD – Genève. »
- Lien : « Voir toutes les réalisations en placo »

### C.6 Comment se passe un chantier

§A.8, version courte.

### C.7 Questions fréquentes sur le placo

- **H2** : « Questions fréquentes sur le placo »

1. **Combien coûte une cloison ou un faux-plafond en placo ?**
   Le prix dépend de la surface, de la hauteur, de l'isolant, du nombre de portes et de spots, et de la finition. À titre indicatif, une cloison de 10 m² avec isolant, joints et peinture coûte en général entre CHF {{min}} et {{max}}, TVA comprise. Après la visite, vous recevez une offre écrite détaillée. `[À CONFIRMER C31 : fourchette réelle]` Repli : sans la phrase « À titre indicatif… ».
2. **Combien de temps dure la pose ?**
   Pour une cloison ou le plafond d'une pièce d'habitation, comptez en général quelques jours, séchage des joints compris. Pour des bureaux ou une salle, nous établissons un calendrier des travaux après la visite. Le délai figure dans l'offre.
3. **Une cloison en placo isole-t-elle du bruit ?**
   Une cloison simple atténue les voix, sans plus. Avec un isolant et deux plaques de chaque côté, elle isole nettement mieux. Si le bruit est votre souci principal, voyez notre page sur l'isolation acoustique.
4. **Peut-on fixer des meubles sur une cloison en placo ?**
   Oui, avec des chevilles adaptées pour les charges légères. Pour un meuble lourd, une télévision ou des éléments de cuisine, nous posons des renforts dans la cloison : dites-le-nous avant la fermeture.
5. **Le placo convient-il à une salle de bains ?**
   Oui, avec des plaques prévues pour les pièces humides. Les zones exposées à l'eau reçoivent ensuite une étanchéité sous le carrelage, posée par le carreleur.
6. **Faut-il l'accord de la régie ou de la copropriété ?**
   Si vous êtes locataire, oui : il faut l'accord écrit du bailleur avant de transformer le logement. En PPE (propriété par étages), une cloison dans votre lot est en général possible ; vérifiez le règlement, et parlez-en à l'administrateur si elle touche une partie commune.

### C.8 Demander un devis pour du placo

§A.5 (version pages services).

---

## D. Peinture (`peinture.html`)

### Métadonnées

- **Title** (59 car.) : `Entreprise de peinture intérieure à Genève | Andy Construct`
- **Meta description** (149 car.) : `Peinture des murs et plafonds : appartements, fins de bail, cages d'escalier, bureaux. Supports préparés, chantier protégé. Genève et Suisse romande.`

### D.1 En-tête de page

- Fil d'Ariane : « Accueil › Peinture »
- **H1** : « Peinture intérieure : murs, plafonds, cages d'escalier »
- Chapeau : « Repeindre un appartement, préparer une fin de bail, rafraîchir des bureaux ou une cage d'escalier : nous préparons les supports, protégeons les lieux et rendons des pièces propres. »
- Boutons : « Demander un devis pour de la peinture » · « Appeler le +41 22 771 20 15 »
- En bref :
  - « Appartements, villas, bureaux, parties communes »
  - « Murs préparés avant la peinture »
  - « Lieux protégés, nettoyés le dernier jour » `[C07]` Repli : « Lieux protégés pendant les travaux »
- Photo : photo « après » de la paire AA6, légende « Séjour repeint, avec un faux-plafond et des spots » `[À VÉRIFIER : qualité de AA6]`. Si elle est insuffisante : en-tête sans photo, jusqu'au shooting peinture (`C40`).

### D.2 Ce que nous peignons

- **H2** : « Ce que nous peignons »
- Introduction : « Une peinture qui tient dépend surtout de ce qu'on fait avant : reboucher, poncer, poser une couche d'impression. Nous le faisons pour chaque chantier. »
- **H3 « Logements »** : « Une pièce ou tout l'appartement, habité ou vide. Nous déplaçons et couvrons les meubles, protégeons les sols, rebouchons trous et fissures, puis appliquons deux couches de peinture. » `[À CONFIRMER C17 : déroulé et nombre de couches habituels]` Repli : « … puis peignons murs et plafonds. »
- **H3 « Fins de bail et remises en état »** : « Pour les régies et les propriétaires : remise en état entre deux locataires, dans des délais courts, pour que le logement soit prêt à l'état des lieux d'entrée. » `[C17]`
- **H3 « Cages d'escalier et parties communes »** : « Dans un immeuble habité, nous travaillons par étages, gardons le passage libre et informons les habitants avant de commencer. » `[À CONFIRMER C20 : avis aux habitants]` Repli : « … gardons le passage libre. »
- **H3 « Bureaux et commerces »** : « Le soir, le week-end ou zone par zone, pour que vous n'ayez pas à fermer. » `[À CONFIRMER C19 : travaux hors des heures d'ouverture]` Repli : « Zone par zone, pour limiter la gêne. »
- **H3 « Après nos travaux de placo »** : « Les cloisons et les plafonds neufs reçoivent une couche d'impression, puis la peinture de finition. Vous n'avez pas à chercher un autre artisan. » `[C05]` Repli : H3 masqué.

### D.3 Pour qui ?

- **H2** : « Pour qui ? »
- **Particuliers** : « Un appartement à rafraîchir après vingt ans, une pièce avant l'arrivée d'un enfant, un logement à préparer pour une vente. Nous venons voir, puis nous vous remettons une offre écrite (votre devis). »
- **Professionnels** : « Remises en état de fin de bail, cages d'escalier, bureaux et arcades. Lot de peinture (CFC 285), prix par pièce sur demande pour les régies. » `[À CONFIRMER C17 : prix par pièce pour les régies]` Repli : « … Lot de peinture (CFC 285). » — lien « Espace professionnels »

### D.4 Ce qu'il faut savoir

- **H2** : « Ce qu'il faut savoir avant de commencer »
- « La préparation compte autant que la peinture. Dans l'offre, elle figure sur une ligne à part : vous voyez ce que vous payez. » `[C06]` Repli : « La préparation compte autant que la peinture. »
- « Une fissure revient si sa cause n'est pas traitée (mouvement du bâtiment, humidité). Nous vous le disons à la visite. »
- « Une tache d'humidité ou de moisissure demande d'abord d'en trouver la cause. La repeindre sans cela ne règle rien. »
- « Pour choisir une teinte, nous pouvons appliquer un échantillon sur le mur. » `[C17]` Repli : masqué
- « Nous peignons à l'intérieur seulement : pas de façades. »

### D.5 Réalisations

- **H2** : « Nos réalisations en peinture »
- Paire avant / après AA6 (§G.4), si sa qualité le permet `[À VÉRIFIER]`. Sinon, la section est **masquée** jusqu'au shooting peinture (`C40`).
- « Réalisé notamment pour : `[À CONFIRMER C23 : références où Andy a peint]`. » Repli : ligne masquée (la ligne de références du bloc de demande suffit).
- Lien : « Voir toutes les réalisations »

### D.6 Comment se passe un chantier

§A.8, version courte.

### D.7 Questions fréquentes sur la peinture

- **H2** : « Questions fréquentes sur la peinture »

1. **Combien coûte la peinture d'un appartement ?**
   Le prix dépend de la surface des murs et des plafonds, de leur état, de la hauteur, des meubles à déplacer et du nombre de teintes. À titre indicatif, repeindre un 3,5 pièces en bon état coûte en général entre CHF {{min}} et {{max}}, TVA comprise. `[À CONFIRMER C31]` Repli : sans la phrase « À titre indicatif… ».
2. **Combien de temps faut-il pour repeindre un appartement ?**
   Pour un 3 ou 4 pièces vide, comptez en général {{durée}} jours ouvrables. Un logement habité ou des murs abîmés demandent plus de temps. La durée figure dans l'offre. `[À CONFIRMER C31 : durée type]` Repli : « Cela dépend de la surface et de l'état des murs. La durée figure dans l'offre écrite. »
3. **Peut-on rester chez soi pendant les travaux ?**
   Oui. Nous travaillons pièce par pièce, couvrons les meubles et gardons un passage libre. Il suffit de dégager l'accès aux murs. `[C20]` Repli : question masquée.
4. **Faut-il vider les pièces ?**
   Non. Retirez les objets fragiles et ce qui est accroché aux murs ; nous déplaçons et couvrons les meubles. `[C17]` Repli : « Retirez au moins les objets fragiles et ce qui est accroché aux murs. Le reste se décide à la visite. »
5. **Travaillez-vous pour les fins de bail ?**
   Oui, pour les régies et les propriétaires. Donnez-nous la date de l'état des lieux : nous planifions les travaux pour que le logement soit prêt. `[C17]`
6. **Peignez-vous aussi les façades ?**
   Non. Nous travaillons à l'intérieur : murs, plafonds, cages d'escalier et parties communes. Pour une façade, adressez-vous à une entreprise de peinture extérieure.

### D.8 Demander un devis pour de la peinture

§A.5 (version pages services).

---

## E. Isolation acoustique (`isolation-acoustique.html`)

### Métadonnées

- **Title** (58 car.) : `Isolation phonique et acoustique à Genève | Andy Construct`
- **Meta description** (141 car.) : `Vous entendez vos voisins ? Doublages, faux-plafonds et cloisons acoustiques, correction de l'écho dans les salles. Genève et Suisse romande.`

### E.1 En-tête de page

- Fil d'Ariane : « Accueil › Isolation acoustique »
- **H1** : « Isolation phonique et acoustique : moins de bruit chez vous »
- Chapeau : « Voisins, télévision, pas à l'étage, voix dans la salle de réunion : nous isolons murs et plafonds pour que le bruit passe moins. Et nous réduisons l'écho des salles trop sonores. » `[C18]` Repli : sans la dernière phrase.
- Boutons : « Demander un devis pour une isolation acoustique » · « Appeler le +41 22 771 20 15 »
- En bref :
  - « Logements, bureaux, écoles, salles communales »
  - « Des travaux choisis selon le bruit que vous entendez »
  - « Aucune promesse chiffrée sans mesure »
- Photo : `chantier-suspentes-ossature-01`, légende « Pendant les travaux : suspentes et ossature d'un faux-plafond, sous une dalle isolée »

### E.2 Isoler ou corriger

- **H2** : « Isoler ou corriger : deux problèmes différents »
- « **Isoler**, c'est empêcher le bruit de passer d'un local à l'autre : celui du voisin, de l'étage, de la pièce d'à côté. Il faut alors une paroi à la fois lourde et souple, sans contact rigide avec la structure du bâtiment. »
- « **Corriger**, c'est réduire l'écho à l'intérieur d'une pièce : une salle de réunion où l'on s'entend mal, un réfectoire, une salle communale. On pose alors des surfaces qui absorbent le son. »
- « Un panneau absorbant ne protège pas du bruit du voisin. Une cloison isolante ne réduit pas l'écho. À la visite, nous commençons donc par identifier ce que vous entendez. »
- « Dans un appartement, on isole le plus souvent contre le voisin. Dans une salle communale ou un réfectoire, on corrige d'abord l'écho. Il faut parfois faire les deux. »

### E.3 Ce que nous posons

- **H2** : « Ce que nous posons contre le bruit »
- **H3 « Doublage acoustique d'un mur »** : « Une ossature indépendante du mur, une laine minérale, puis une ou deux plaques de plâtre. Efficace contre les voix et la télévision du voisin. La pièce perd en général 7 à 10 cm. » `[À CONFIRMER C18 : épaisseurs usuelles]` Repli : « … La pièce perd quelques centimètres. »
- **H3 « Faux-plafond acoustique »** : « Suspendu sous le plafond par des suspentes qui amortissent les vibrations, avec un isolant au-dessus. Il réduit les voix venant d'en haut, et en partie les bruits de pas. »
- **H3 « Cloison acoustique »** : « Deux ossatures séparées, un isolant, des plaques doublées : pour une chambre, un bureau, une salle de réunion ou un cabinet où la confidentialité compte. »
- **H3 « Correction acoustique des salles »** (ancre `#correction`) : « Plafonds perforés et panneaux muraux qui absorbent le son, pour les salles de réunion, les salles communales et les salles de classe. » `[À CONFIRMER C18 : correction acoustique toujours proposée]` Repli : H3 masqué.

### E.4 Ce qu'il faut savoir

- **H2** : « Ce qu'il faut savoir avant de commencer »
- « Les bruits de pas du voisin du dessus se traitent le mieux à la source, dans son sol. Un faux-plafond chez vous les atténue, sans les supprimer. Nous vous le disons à la visite. »
- « Le bruit passe aussi par les côtés : prises, gaines, portes, murs voisins. Une isolation qui oublie ces points déçoit. »
- « Personne ne peut promettre un résultat en décibels sans mesure. Si une performance est exigée (norme SIA 181), elle est fixée par le projet, et nous posons un système qui y répond. » `[À CONFIRMER C15]` Repli : « … sans mesure. »
- « En location ou en PPE (propriété par étages), demandez l'accord avant des travaux qui touchent un mur mitoyen ou la structure. »
- « L'isolation acoustique seule n'est en général pas subventionnée. »
- « Une pièce froide plutôt que bruyante ? Voyez nos cloisons isolantes. » (lien vers `cloisons-isothermes.html`)

### E.5 Guide à télécharger

- **H2** : « Guide : réduire le bruit chez soi »
- « Ce qui marche, ce qui ne marche pas, et les questions à poser à une entreprise, quelle qu'elle soit. 8 pages, 10 minutes de lecture. »
- Bouton : « Télécharger le guide (PDF, {{poids}}) »
- Lien : « Le recevoir imprimé, par la poste » (ouvre le petit formulaire du §Q.4)

### E.6 Réalisations

- **H2** : « Nos réalisations en acoustique »
- Projets P6 et P7 (§G.3), si `C18` est confirmé.
- « Réalisé notamment pour : `[À CONFIRMER C23 : p. ex. Conservatoire de musique de Genève, HEAD – Genève, salle communale de Collonge-Bellerive]`. » Repli : « Ils nous ont confié des travaux : Conservatoire de musique de Genève · HEAD – Genève · Salle de l'Alhambra. »
- Lien : « Voir toutes les réalisations en acoustique »

### E.7 Comment se passe un chantier

§A.8, version courte.

### E.8 Questions fréquentes sur l'isolation acoustique

- **H2** : « Questions fréquentes sur le bruit »

1. **Comment réduire le bruit des voisins du dessus ?**
   Pour les voix et la musique, un faux-plafond acoustique, suspendu par des attaches qui amortissent les vibrations, donne de bons résultats. Pour les bruits de pas, le plus efficace est d'agir sur le sol du voisin. À la visite, nous vous disons ce qui est réaliste chez vous.
2. **Les panneaux en mousse ou les boîtes à œufs isolent-ils du bruit ?**
   Non. Ils réduisent un peu l'écho dans la pièce, mais n'empêchent pas le bruit de passer. Pour isoler, il faut une paroi lourde, désolidarisée de la structure et étanche à l'air.
3. **Combien coûte une isolation phonique ?**
   Le prix dépend de la surface, du type de travaux (doublage, faux-plafond, cloison), des points faibles à traiter et de la finition. À titre indicatif, le doublage acoustique d'un mur mitoyen de 12 m² coûte en général entre CHF {{min}} et {{max}}, TVA comprise. `[À CONFIRMER C31]` Repli : sans la phrase « À titre indicatif… ».
4. **Combien de place perd-on ?**
   Un doublage acoustique prend en général 7 à 10 cm sur l'épaisseur de la pièce, un faux-plafond un peu plus. Nous mesurons avant de proposer. `[C18]` Repli : « Quelques centimètres sur l'épaisseur de la pièce. Nous mesurons avant de proposer. »
5. **Pouvez-vous mesurer le bruit avant et après ?**
   Nous ne faisons pas de mesure acoustique nous-mêmes. Si une mesure est demandée, elle est confiée à un bureau d'acoustique, et nous travaillons avec lui. `[À CONFIRMER C18]` Repli : question masquée.
6. **Que faire dans une salle de réunion où l'on s'entend mal ?**
   C'est un problème d'écho : des panneaux absorbants au plafond ou aux murs le réduisent nettement, souvent sans gros travaux. Si les voix passent aussi dans le bureau voisin, il faut en plus isoler la cloison. `[C18]` Repli : question masquée.

### E.9 Demander un devis pour une isolation acoustique

§A.5 (version pages services).

---

## F. Cloisons isolantes (`cloisons-isothermes.html`)

### Métadonnées

- **Title** (60 car.) : `Cloisons isolantes, cave et garage à Genève | Andy Construct`
- **Meta description** (132 car.) : `Cloisons isolantes (isothermes) entre pièces chauffées et caves, garages ou combles, en plaques de plâtre. Genève et Suisse romande.`

### F.1 En-tête de page

- Fil d'Ariane : « Accueil › Cloisons isolantes »
- **H1** : « Cloisons isolantes (isothermes) : caves, garages et combles »
- Chapeau : « Une pièce froide au-dessus d'un garage, un bureau contre une cave, des combles à aménager : une cloison ou un doublage isolant sépare ce qui est chauffé de ce qui ne l'est pas. »
- Phrase de précision (en petit, sous le chapeau) : « Nous ne posons pas de chambres froides ni de panneaux frigorifiques. » `[À CONFIRMER C16]` Repli : masqué (et texte à revoir si le client en pose).
- Boutons : « Demander un devis pour une cloison isolante » · « Appeler le +41 22 771 20 15 »
- En bref :
  - « Entre pièces chauffées et locaux froids »
  - « Ossature, isolant, plaques : prêt à peindre »
  - « Villas, immeubles, locaux d'activité »
- Photo : `chantier-ossature-puits-de-lumiere-02`, légende « Pendant les travaux : ossature métallique et isolant, avant la pose des plaques »

### F.2 Ce que nous posons

- **H2** : « Ce que nous posons pour garder la chaleur »
- **H3 « Cloison isolante »** : « Entre une pièce chauffée et un garage, une cave, un atelier ou un dépôt : une ossature métallique, un isolant thermique et des plaques de plâtre. La cloison limite les pertes de chaleur et les courants d'air froid. »
- **H3 « Doublage isolant d'un mur froid »** : « Un mur contre la terre, une cave ou l'extérieur reste froid au toucher ? Un doublage avec isolant, posé côté pièce, améliore le confort. »
- **H3 « Plafond de cave ou de garage »** : « Le sol de la pièce du dessus est froid ? Un isolant fixé sous la dalle de la cave ou du garage, fermé par des plaques si le local le demande, réduit la perte de chaleur. » `[C16]`
- **H3 « Combles et rampants »** : « Un isolant entre ou sous les chevrons, puis des plaques de plâtre : les combles deviennent une pièce habitable. » `[À CONFIRMER C16 : isolation de combles dans l'offre]` Repli : H3 masqué.

### F.3 Pour qui ?

- **H2** : « Pour qui ? »
- **Particuliers** : « Une chambre au-dessus du garage, un sous-sol aménagé en bureau, des combles à transformer. Nous venons voir, puis nous vous remettons une offre écrite (votre devis). »
- **Professionnels** : « Locaux non chauffés dans les immeubles (caves, parkings, locaux techniques), ateliers et dépôts attenants à des bureaux. Offres sur plans et descriptifs. » — lien « Espace professionnels »

### F.4 Ce qu'il faut savoir

- **H2** : « Ce qu'il faut savoir avant de commencer »
- « L'épaisseur d'isolant dépend de l'écart de température entre les deux locaux et des exigences de votre canton. Nous la proposons dans l'offre. »
- « Sur un mur enterré ou dans une cave humide, on vérifie d'abord l'humidité : un isolant posé sur un mur mouillé crée de nouveaux problèmes. »
- « Le pare-vapeur se pose du côté chauffé. Mal placé, il fait condenser l'humidité dans la paroi. »
- « Le bruit vous gêne aussi ? Un isolant bien choisi peut traiter les deux : voyez l'isolation acoustique. » (lien vers `isolation-acoustique.html`)
- « Entre un garage et un logement, des exigences de protection incendie peuvent s'appliquer. Nous en tenons compte dans le choix des plaques. » `[À CONFIRMER C15 : systèmes coupe-feu posés]` Repli : « … peuvent s'appliquer : vérifiez-les avant les travaux. »

### F.5 Subventions (encadré)

- **H2** : « Des subventions sont-elles possibles ? »
- « Certaines isolations thermiques peuvent être subventionnées, par le Programme Bâtiments et par les cantons, si elles atteignent les performances exigées. La demande se dépose **avant** le début des travaux. Renseignez-vous auprès du service de l'énergie de votre canton ; nous vous fournissons les informations techniques dont il a besoin. » `[À CONFIRMER C43 : informations fournies par Andy]` Repli : sans la dernière proposition.

### F.6 Réalisations

- **H2** : « Nos réalisations en isolation »
- Paire avant / après AA3 (combles, §G.4) `[À VÉRIFIER : qualité]`, et projet P2 (§G.3) si l'isolant posé est thermique `[C25]`.
- Lien : « Voir toutes les réalisations »

### F.7 Comment se passe un chantier

§A.8, version courte.

### F.8 Questions fréquentes sur les cloisons isolantes

- **H2** : « Questions fréquentes sur l'isolation intérieure »

1. **Qu'est-ce qu'une cloison isotherme ?**
   C'est une cloison isolante : une ossature métallique, un isolant thermique et des plaques de plâtre. Elle sépare une pièce chauffée d'un local qui ne l'est pas, comme un garage ou une cave. Ce n'est pas une chambre froide. `[C16]`
2. **Comment isoler le plafond d'une cave ou d'un garage ?**
   On fixe un isolant sous la dalle, puis on le ferme par des plaques si le local est utilisé. Le sol de la pièce du dessus devient moins froid, et la chaleur reste où elle doit être.
3. **Faut-il une autorisation pour aménager des combles ?**
   Transformer des combles en pièce habitable peut demander une autorisation de construire, selon le canton et la commune. Renseignez-vous avant de commencer ; nous vous donnons les informations techniques utiles. `[C16]` Repli : question masquée si les combles ne sont pas dans l'offre.
4. **Quelle épaisseur d'isolant faut-il ?**
   Elle dépend des températures de part et d'autre et des exigences énergétiques du canton. Nous la proposons dans l'offre, avec le type d'isolant.
5. **Combien coûte une cloison isolante ?**
   Le prix dépend de la surface, de l'épaisseur d'isolant, des portes et de la finition. À titre indicatif, une cloison isolante de 10 m² entre un garage et un logement coûte en général entre CHF {{min}} et {{max}}, TVA comprise. `[À CONFIRMER C31]` Repli : sans la phrase « À titre indicatif… ».

### F.9 Demander un devis pour une cloison isolante

§A.5 (version pages services).

---

## G. Réalisations (`realisations.html`)

### Métadonnées

- **Title** (58 car.) : `Réalisations : placo, peinture, isolation | Andy Construct`
- **Meta description** (143 car.) : `Chantiers de placo, de peinture et d'isolation photographiés par notre équipe : halls, salles, logements, bureaux. Avant / après et références.`

### G.1 En-tête de page

- Fil d'Ariane : « Accueil › Réalisations »
- **H1** : « Nos réalisations »
- Chapeau : « Des chantiers photographiés par notre équipe, pendant et après les travaux. Choisissez un type de travaux. »
- Mention : « Toutes les photos sont nos propres réalisations. » `[À CONFIRMER C25]` Repli : masqué

### G.2 Filtres

- Nom du groupe (lecteurs d'écran) : « Filtrer les projets par type de travaux »
- Boutons : « Tous » · « Placo » · « Peinture » · « Isolation acoustique » · « Cloisons isolantes » (chacun suivi du nombre de projets, p. ex. « (5) »). Un filtre sans projet n'est pas affiché.
- Compteur : « {{n}} projets affichés »

### G.3 Fiches projets

Format : titre · type de lieu · contrainte · étiquettes · badge éventuel. Sous chaque fiche : « Un projet semblable ? Demander un devis ». Clic sur la photo : « Voir les {{n}} photos du projet ».

| Projet | Titre | Type de lieu (définitif → repli) | Contrainte (définitive → repli) | Étiquettes | Badge |
|---|---|---|---|---|---|
| P1 | Hall et couloirs : faux-plafond à gorge lumineuse | « Immeuble, canton de Genève » `[C25]` → « Hall d'immeuble » | `[C25 : 1 ligne du client]` → « Formes courbes, éclairage et spots intégrés au plafond. » | Placo · Peinture `[C25]` → Placo | — |
| P2 | Grande salle : ossature et isolant avant la fermeture | « Salle publique, canton de Genève » `[C25]` → « Salle publique » | `[C25]` → « Travail en hauteur, autour de puits de lumière. » | Placo + `[C25 : Isolation acoustique ou Cloisons isolantes]` → Placo | Pendant les travaux |
| P3 | Faux-plafond suspendu sous une dalle isolée | `[C25]` → « Grand local » | `[C25]` → « Suspentes réglées et alignées sur toute la surface, avant la pose des plaques. » | Placo | Pendant les travaux |
| P4 | Cage d'escalier : habillage à niches arrondies | `[C25]` → « Immeuble » | `[C25]` → « Formes arrondies, escalier protégé pendant les travaux. » | Placo | Pendant les travaux |
| P5 | Hall : îlot ovale suspendu | « Bâtiment d'entreprise » `[C25]` → « Hall » | `[C25]` → « Un grand îlot suspendu au-dessus d'une trémie. » | Placo | — |
| P6 | Correction acoustique d'une salle | `[C25]` → « Salle » | `[C25]` → « Réduire l'écho, sans gros travaux. » | Isolation acoustique | — |
| P7 | Salle de réunion : moins d'écho | « Bureaux » | `[C25]` → « Un grand panneau mural absorbe l'écho de la salle. » | Isolation acoustique | — |
| P8 | Salle de spectacle : intervention en salle protégée | « Salle de spectacle » | `[C25]` → « Travail en hauteur, fauteuils protégés sous bâche. » | `[C25 : prestation parmi les 4]` | Pendant les travaux |

Avec l'accord écrit du maître d'ouvrage (`C22`) : ajouter sous le type de lieu « Pour {{nom}}, {{année}} ».

### G.4 Avant / après (`#avant-apres`)

- **H2** : « Avant, après »
- Introduction : « Les mêmes lieux, avant et après nos travaux. »
- Étiquettes au-dessus des images : « Avant » · « Après »
- Légendes (une par paire) `[À VÉRIFIER : qualité de chaque paire]` `[À CONFIRMER C26 : lieux et prestations]` :
  - AA1 : « Caisson en plaques de plâtre sous une verrière » — Placo
  - AA2 : « Gaine de ventilation cachée dans un couloir » — Placo
  - AA3 : « Combles : isolation et rampant fini sous une fenêtre de toit » — Cloisons isolantes
  - AA4 : « Appareil de ventilation habillé d'un caisson » — Placo
  - AA5 : « Couloir : puits de lumière circulaires dans un faux-plafond » — Placo
  - AA6 : « Séjour : faux-plafond en périphérie et spots » — Placo · Peinture
  - AA7 : « Paroi cintrée : de l'ossature au couloir fini » — Placo

### G.5 Témoignages

§A.11, masqué tant qu'il est vide.

### G.6 Références

- Ligne courte du §A.6.
- Lien : « Voir les 18 références, par secteur »

### G.7 Votre projet

- **H2** : « Un projet semblable aux nôtres ? »
- « Montrez-nous votre local ou vos plans : nous venons voir et vous remettons une offre écrite. »
- Boutons : « Demander un devis » · « Appeler le +41 22 771 20 15 »
- Module de rappel (§A.7).

---

## H. Professionnels (`professionnels.html`)

### Métadonnées

- **Title** (60 car.) : `Régies et architectes : plâtrerie, peinture | Andy Construct`
- **Meta description** (142 car.) : `Plâtrerie, faux-plafonds et peinture pour régies, architectes et communes : immeubles habités, offres sur plans, dossier de références en PDF.`

### H.1 En-tête de page

- Fil d'Ariane : « Accueil › Professionnels »
- **H1** : « Régies, architectes, communes : plâtrerie, faux-plafonds et peinture »
- Chapeau : « Depuis 2007, nous travaillons dans des immeubles habités, des bureaux et des bâtiments publics. Offres sur plans et descriptifs, coordination avec les autres corps de métier, chantier tenu propre. » `[À CONFIRMER C20 : immeubles habités]` Repli : « Depuis 2007, nous travaillons dans des bureaux, des logements et des bâtiments publics. Offres sur plans et descriptifs, coordination avec les autres corps de métier. »
- Bouton principal : « Télécharger le dossier de références (PDF, {{poids}}) »
- Bouton secondaire : « Envoyer un dossier de soumission »
- Ligne : « Une question ? +41 22 771 20 15 »

### H.2 Selon votre métier

- **H2** : « Ce que nous vous apportons »
- **H3 « Régies et gérances »**
  « Remises en état entre deux locataires, cages d'escalier, plafonds après un dégât d'eau, cloisons pour une arcade. Nous informons les locataires, protégeons les parties communes et tenons la date convenue. Un seul interlocuteur, joignable sur son portable. » `[À CONFIRMER C20, C09]` Repli : « … Nous protégeons les parties communes. Un interlocuteur joignable. »
  Action : « Télécharger la liste de contrôle « immeuble habité » (PDF) »
- **H3 « Architectes et bureaux d'études »**
  « Lots CFC 271 (plâtrerie), 283 (faux-plafonds) et 285 (peinture). Offres complètes sur descriptif, variantes chiffrées à part, questions posées avant de chiffrer. Ouvrages dans des lieux exigeants : salles de musique et de spectacle, écoles d'art, bureaux. » `[À CONFIRMER C14, C22]` Repli : « Lots de plâtrerie et de peinture. Offres complètes sur descriptif, variantes chiffrées à part. »
  Action : « Envoyer un dossier de soumission »
- **H3 « Communes et institutions »**
  « La Ville de Genève et les communes de Plan-les-Ouates et de Collonge-Bellerive (salles communales) nous ont confié des travaux. Travaux possibles pendant les vacances scolaires ou entre deux manifestations. Attestations sociales et fiscales sur demande. » `[À CONFIRMER C19, C13]` Repli : sans les deux dernières phrases.
  Action : « Demander nos attestations » (`mailto:` avec l'objet « Demande d'attestations ») `[C13]`
- **H3 « Entreprises, bureaux et commerces »**
  « Cloisons, salles de réunion plus calmes, peinture des locaux : le soir ou le week-end, pour ne pas fermer. Nous préparons le descriptif à remettre à votre bailleur pour son accord. » `[C19]` Repli : « Cloisons, salles de réunion plus calmes, peinture des locaux, zone par zone. Nous préparons le descriptif à remettre à votre bailleur pour son accord. »
  Action : « Demander un devis »

### H.3 Méthode en site occupé

- **H2** : « Immeubles habités et lieux publics : notre méthode »
- Introduction : « Les plaintes et les retards naissent presque toujours d'un manque d'organisation. Voici ce que nous faisons à chaque chantier. »
- Liste numérotée `[À CONFIRMER C20, C07, C06, C09, C32 : engagements]` :
  1. « Un avis aux locataires ou aux usagers, préparé avec vous et affiché quelques jours avant. »
  2. « Des horaires de travail convenus, communiqués aux habitants. »
  3. « Parties communes, ascenseur et sols protégés avant le premier jour. »
  4. « La poussière contenue : zone fermée par des bâches, aspiration. »
  5. « Un responsable de chantier nommé, joignable pendant toute la durée des travaux. »
  6. « Nettoyage chaque soir, passages libres pour les habitants. »
  7. « Un imprévu ? Nous le signalons avec son prix, avant de l'exécuter. »
  8. « Réception avec photos et liste des retouches, levées dans le délai convenu. »
  Repli : la liste est réduite aux points confirmés ; si aucun ne l'est, la section est masquée.
- Lien : « Télécharger la liste de contrôle « immeuble habité » (PDF, 2 pages) »

### H.4 Lots, normes et documents

- **H2** : « Lots, normes et documents »
- **Lots CFC** : « 271 Plâtrerie · 283 Faux-plafonds · 285 Traitement des surfaces intérieures (peinture) » `[C14]` Repli : « 271 Plâtrerie · 285 Peinture ». Liens : 271 → `placo.html`, 283 → `placo.html#faux-plafonds`, 285 → `peinture.html`.
- **Normes** : « Nous travaillons selon la norme SIA 118 lorsque le contrat s'y réfère. Isolation acoustique et thermique selon les exigences du projet (SIA 181 et SIA 180). Protection incendie selon les prescriptions AEAI lorsque le projet l'exige. » `[À CONFIRMER C15, C33]` Repli : « Les performances visées sont celles du projet, précisées dans l'offre. »
- Tableau « Document · Comment l'obtenir » :
  - « Dossier de références (6 pages) » — « Télécharger (PDF, {{poids}}) »
  - « Liste de contrôle : travaux en immeuble habité (2 pages) » — « Télécharger (PDF, {{poids}}) »
  - « Modèle d'avis aux locataires » — « Télécharger (Word, {{poids}}) » `[C20]`
  - « Extrait du registre du commerce » — « Consulter sur Zefix »
  - « Attestation d'assurance responsabilité civile » — « Sur demande, par e-mail » `[À CONFIRMER C12]` Repli : ligne masquée
  - « Attestations AVS, LPP, impôts, convention collective » — « Sur demande, par e-mail » `[À CONFIRMER C13]` Repli : ligne masquée

### H.5 Références complètes (`#references`)

- **H2** : « Ils nous ont confié des travaux »
- Introduction : « 18 maîtres d'ouvrage publics et privés, à Genève et dans le canton de Vaud. » `[À CONFIRMER C22 : années et nature des travaux, affichées sous chaque nom dès qu'elles sont connues]`
- **Collectivités et institutions** : Ville de Genève · Mairie de Plan-les-Ouates · Salle communale de Collonge-Bellerive · OMC `[C22 : accord de l'OMC ; repli : nom retiré]`
- **Culture et formation** : Conservatoire de musique de Genève · HEAD – Genève · Salle de l'Alhambra · Harmonie Nautique de Genève
- **Entreprises** : Piaget · UBS · J. Safra Sarasin (anciennement Bank Sarasin) · de Grisogono · Celgene · Labcorp (anciennement Covance), Meyrin · Dipan, Nyon · Energestion, ingénieurs-conseils, Les Acacias
- **Hôtellerie et domaines** : Everness Hotel & Resort, Chavannes-de-Bogis `[À CONFIRMER C22 : même hôtel que l'« Hôtel Chavannes-de-Bogis »]` (repli : « Hôtel à Chavannes-de-Bogis ») · Domaine des Perrières, Coppet
- Sous la grille (production, une fois les accords archivés) : « Références citées avec l'accord des maîtres d'ouvrage. Contacts de référence sur demande. » `[C22]`

### H.6 Envoyer un dossier de soumission (`#soumission`)

- **H2** : « Envoyer un dossier de soumission »
- « Écrivez à **contact@andyconstruct.ch** `[C30]` avec : »
  - « le descriptif ou la série de prix, et les plans ; »
  - « la date de remise des offres ; »
  - « la date de la visite, si elle est prévue. »
- « Fichiers lourds : un lien de transfert (SwissTransfer ou autre) convient. »
- « Nous accusons réception le jour même ou le jour ouvrable suivant, avec le nom de la personne qui suit votre dossier. » `[C01, C09]` Repli : « Nous accusons réception de votre dossier et vous indiquons qui le suit. »
- « Vous préférez voir notre travail sur place ? Nous vous faisons visiter un chantier en cours. » `[À CONFIRMER C40]` Repli : masqué
- Bouton : « Écrire à Andy Construct » (`mailto:` avec l'objet « Dossier de soumission »)

### H.7 Demander un devis

§A.5 (version accueil), **sans** ligne de références (la grille complète est juste au-dessus).

---

## I. L'entreprise (`entreprise.html`)

### Métadonnées

- **Title** (52 car.) : `L'entreprise, à Carouge depuis 2007 | Andy Construct`
- **Meta description** (141 car.) : `Andy Construct, Chanton & Cie : entreprise de Carouge inscrite au registre du commerce depuis 2007. Histoire, méthode, engagements, identité.`

### I.1 En-tête de page

- Fil d'Ariane : « Accueil › L'entreprise »
- **H1** : « Andy Construct, entreprise de Carouge depuis 2007 »
- Chapeau : « Une entreprise genevoise de plâtrerie, de peinture et d'isolation intérieure, dirigée par ses deux associés, qui suivent eux-mêmes les chantiers. » `[À CONFIRMER C10, C09]` Repli : « Une entreprise genevoise de plâtrerie, de peinture et d'isolation intérieure, dirigée par ses deux associés. »

### I.2 Notre histoire

- **H2** : « Notre histoire »
- **2007** — « Début de l'activité le 1er juin 2007, à Perly-Certoux. Inscription au registre du commerce de Genève. »
- **2010** — « Le siège s'installe à Chêne-Bourg. »
- **2023** — « Le siège s'installe à Carouge, route des Acacias. Caroline Chanton Bajrami rejoint Adnan Bajrami comme associée. » `[À CONFIRMER C10 : associés nommés]` Repli : « Le siège s'installe à Carouge, route des Acacias. »
- **Aujourd'hui** — « Placo, peinture, isolation acoustique et cloisons isolantes, dans toute la Suisse romande. » (chaque métier est un lien vers sa page)
- Phrase sous la frise : « Au fil des années, la Ville de Genève, le Conservatoire de musique de Genève, la HEAD et des particuliers de toute la région nous ont confié des travaux. »

### I.3 Notre métier

- **H2** : « Notre métier, tel qu'il est inscrit au registre du commerce »
- Citation : « Pose de faux-plafonds phoniques et cloisons légères phoniques et thermiques, isolations intérieures, plâtrerie, peinture, aménagement de logements et bureaux. »
- Source sous la citation : « But social inscrit au registre du commerce de Genève »
- « Ces métiers se suivent sur un même chantier : ossature, isolant, plaques, joints, peinture. Les réunir évite d'attendre un autre artisan entre deux étapes. » `[C05]` Repli : « Ces métiers se suivent sur un même chantier : ossature, isolant, plaques, joints, peinture. »

### I.4 Ce qui guide notre travail

- **H2** : « Ce qui guide notre travail »
- **Venir voir avant de chiffrer** — « Pas de prix au mètre carré au téléphone : nous mesurons et nous écoutons d'abord. » `[C06]`
- **Une offre lisible** — « Poste par poste, en CHF, avec la durée et ce qui n'est pas compris. » `[C06]`
- **Aucun supplément surprise** — « Un imprévu est annoncé et chiffré avant d'être exécuté, avec votre accord écrit. » `[C06]`
- **Des lieux respectés** — « Protections posées avant de commencer, nettoyage chaque soir. » `[C07]`
Repli : chaque carte non confirmée est masquée ; si moins de 2 restent, la section est masquée.

### I.5 Notre méthode (`#methode`)

- **H2** : « Notre méthode, de la visite à la réception »
- §A.8, version complète.

### I.6 L'équipe (masquée tant que photos et accords manquent)

- **H2** : « Qui vient chez vous »
- `[À CONFIRMER C10, C24]` « Adnan Bajrami et Caroline Chanton Bajrami, associés. {{rôle de chacun, 1 ligne}}. Avec eux, une équipe de {{n}} personnes, en tenue Andy Construct sur les chantiers. »
- Légende de la photo : « L'équipe d'Andy Construct, {{année}} »

### I.7 Vérifiez qui nous sommes

- **H2** : « Vérifiez qui nous sommes »
- Introduction : « Avant de laisser entrer une entreprise chez vous, vous pouvez vérifier son identité. Voici la nôtre. »
- **Raison sociale** : Andy Construct, Chanton & Cie
- **Forme juridique** : société en nom collectif
- **Numéro IDE** : CHE-113.706.162 — lien « Vérifier au registre du commerce »
- **Siège** : Route des Acacias 48, 1227 Carouge (Genève)
- **Activité** : depuis le 1er juin 2007
- **Association professionnelle** : membre du GGE, Groupement des entreprises genevoises du bâtiment `[À CONFIRMER C11]` Repli : ligne masquée
- **Assurance** : responsabilité civile d'entreprise, attestation sur demande `[À CONFIRMER C12]` Repli : ligne masquée
- **Paiement** : « Nous ne demandons jamais de paiement en liquide à l'avance. » `[À CONFIRMER C28]` Repli : ligne masquée

### I.8 Si un défaut apparaît après les travaux

- **H2** : « Si un défaut apparaît après les travaux »
- « Appelez-nous dès que vous le constatez : nous venons voir et nous réparons ce qui relève de notre travail. » `[C32]` Repli : « Appelez-nous dès que vous le constatez : nous venons voir. »
- « Ce que dit la loi suisse, pour les contrats conclus depuis le 1er janvier 2026 : un défaut d'un ouvrage peut être signalé dans les 60 jours qui suivent sa découverte, et le droit à la réparation gratuite ne peut plus être exclu par contrat pour un élément de construction. L'action se prescrit par cinq ans pour un ouvrage immobilier. Si votre contrat se réfère à la norme SIA 118, le délai de garantie est de deux ans. » `[À VÉRIFIER : relecture juridique]` Repli : section limitée à la première phrase.

### I.9 Bande d'appel

§A.9.

---

## J. Contact (`contact.html`)

### Métadonnées

- **Title** (52 car.) : `Contact et demande de devis, Genève | Andy Construct`
- **Meta description** (143 car.) : `Demandez un devis en trois étapes ou appelez le +41 22 771 20 15, du lundi au vendredi. Route des Acacias 48, Carouge. Toute la Suisse romande.`

### J.1 En-tête de page

- Fil d'Ariane : « Accueil › Contact »
- **H1** : « Contact et demande de devis »
- Chapeau : « Appelez-nous, laissez votre numéro, ou décrivez vos travaux en trois étapes. »

### J.2 Colonne gauche

**Nous appeler**
- « Bureau » — « +41 22 771 20 15 »
- « Sur les chantiers » — « +41 78 631 14 34 » `[À CONFIRMER C30 : mobile présenté ainsi]`
- « Du lundi au vendredi, de 7 h à 18 h. » `[C03]`
- « Pas de réponse ? Laissez un message avec votre numéro : nous rappelons le jour même ou le jour ouvrable suivant. » `[C01, C03 : répondeur]` Repli : « Pas de réponse ? Laissez un message avec votre numéro : nous vous rappelons. »

**Nous écrire**
- « contact@andyconstruct.ch » `[C30]`

**Nous trouver**
- Bloc NAP (§A.4)
- « Sur rendez-vous. » `[À CONFIRMER C29 : réception de clients à Carouge]` Repli : masqué
- Lien : « Voir sur la carte »

**Pour préparer votre demande**
- « La surface approximative à traiter »
- « Quelques photos, ou des plans si vous en avez »
- « Le délai souhaité »
- « Le type de local : logement, bureau, commerce, salle »
- « Si les lieux seront habités pendant les travaux »

Ligne de références courte (§A.6).

### J.3 Colonne droite

- Formulaire (`#demande`), §A.5 (version accueil), sans répéter la colonne « Par téléphone ».
- Module de rappel (`#rappel`), §A.7.

### J.4 Zone d'intervention (`#zone`)

- **H2** : « Nous intervenons dans toute la Suisse romande »
- « Depuis notre siège de Carouge : cantons de Genève, Vaud, Neuchâtel, Fribourg et Jura, Valais romand et Jura bernois. »
- `[Variante C21 :]` « Pour les particuliers, nous intervenons dans le canton de Genève et sur La Côte. Pour les régies, architectes, communes et entreprises, dans toute la Suisse romande. » Repli : variante non affichée.
- Liste sous la carte (par canton) : Genève · Vaud · Neuchâtel · Fribourg · Valais romand · Jura · Jura bernois, avec les villes marquées sur la carte : Carouge (siège), Genève, Nyon, Lausanne, Yverdon-les-Bains, Neuchâtel, Fribourg, Sion, Delémont, Bienne `[À CONFIRMER C21 : villes à afficher, de préférence celles où des chantiers ont eu lieu]`
- « Votre commune n'est pas dans la liste ? Appelez-nous : +41 22 771 20 15. »
- Légende de la carte : « Toute la Suisse romande. Siège à Carouge. Fond de carte : swisstopo. »

---

## K. Merci (`merci.html`)

### Métadonnées

- **Title** (35 car.) : `Demande bien reçue | Andy Construct`
- **Meta description** (88 car.) : `Votre demande est bien arrivée. Voici ce qui va se passer et comment préparer la visite.`
- `<meta name="robots" content="noindex">`

### K.1 Variante « demande de devis »

- **H1** : « Merci, votre demande est bien arrivée »
- « Référence de votre demande : {{ref}} »
- Récapitulatif (si disponible) : « Vous nous avez demandé un devis pour : {{travaux}}, à {{commune}}. » · « Vous préférez être recontacté(e) : {{préférence}}. »
- **H2** : « Et maintenant ? »
  1. « {{Prénom de l'associé}} vous rappelle le jour même ou le jour ouvrable suivant, depuis le +41 22 771 20 15. » `[À CONFIRMER C09, C01]` Repli : « Nous vous rappelons pendant nos heures de bureau, depuis le +41 22 771 20 15. »
  2. « Ensemble, nous convenons d'une visite, en général dans la semaine. » `[À CONFIRMER C41]` Repli : « Ensemble, nous convenons d'une date de visite. »
  3. « Vous recevez notre offre écrite sous {{X}} jours ouvrables après la visite. » `[À CONFIRMER C08]` Repli : « Vous recevez ensuite notre offre écrite. »
- Si une adresse e-mail a été donnée : « Un e-mail de confirmation vient de partir. Vous ne le voyez pas ? Regardez dans le dossier des courriers indésirables. »
- **H2** : « Pour gagner du temps à la visite »
  - « Quelques photos des pièces concernées »
  - « Les dimensions approximatives »
  - « Les plans, si vous en avez »
  - « La date à laquelle les travaux doivent être finis »
- Lien unique : « En attendant, voir nos réalisations en {{service}} » (si le filtre est vide : « En attendant, voir nos réalisations »)
- Ligne finale : « Une question urgente ? Appelez le +41 22 771 20 15, du lundi au vendredi, de 7 h à 18 h. » `[C03]`
- Version générique (sans récapitulatif) : mêmes textes, sans les deux lignes du récapitulatif.

### K.2 Variante « rappel »

- **H1** : « Merci, nous vous rappelons »
- « Nous vous rappelons {{le matin / l'après-midi}}, le jour même ou le jour ouvrable suivant, depuis le +41 22 771 20 15. » `[C01]` Repli : « Nous vous rappelons pendant nos heures de bureau, depuis le +41 22 771 20 15. »
- « Pour gagner du temps, notez la surface approximative, le délai souhaité et, si possible, prenez quelques photos. »
- Lien : « En attendant, voir nos réalisations »
- « Une question urgente ? +41 22 771 20 15 »

---

## L. Mentions légales (`mentions-legales.html`)

### Métadonnées

- **Title** (33 car.) : `Mentions légales | Andy Construct`
- **Meta description** (137 car.) : `Mentions légales du site andyconstruct.ch : éditeur Andy Construct, Chanton & Cie à Carouge, IDE CHE-113.706.162, hébergement et crédits.`

### Texte

- Fil d'Ariane : « Accueil › Mentions légales »
- **H1** : « Mentions légales »
- Chapeau : « Qui édite ce site, qui l'héberge et à qui appartiennent ses contenus. »

**H2 « Éditeur du site »**
- Raison sociale : Andy Construct, Chanton & Cie
- Forme juridique : société en nom collectif
- Associés : Adnan Bajrami, Caroline Chanton Bajrami `[À CONFIRMER C10]` (repli : ligne masquée)
- Siège : Route des Acacias 48, 1227 Carouge (Genève), Suisse
- Numéro IDE : CHE-113.706.162 · Registre du commerce du canton de Genève, inscription en 2007
- Numéro TVA : CHE-113.706.162 TVA `[À CONFIRMER C35]` (repli : ligne masquée)
- Téléphone : +41 22 771 20 15
- E-mail : contact@andyconstruct.ch `[C30]`

**H2 « Hébergement »**
- « Le site est hébergé par {{nom de l'hébergeur}}, {{adresse}}, en Suisse. » `[À CONFIRMER C34]` Repli : « Le site est hébergé en Suisse. »
- « Conception et réalisation : Harbor Digital. »

**H2 « Propriété des contenus »**
- « Les textes, le logo et les photos de chantiers publiés sur ce site appartiennent à Andy Construct, Chanton & Cie. Leur reproduction demande un accord écrit. »
- « Les photos montrent des chantiers réalisés par l'entreprise. Les personnes et les lieux reconnaissables sont publiés avec l'accord des intéressés. » `[C25]`

**H2 « Références citées »**
- « Les noms des maîtres d'ouvrage cités sur ce site indiquent des travaux réalisés pour eux. Ils ne signifient ni partenariat ni recommandation. Les logos sont reproduits avec l'accord écrit de leurs titulaires ; les armoiries publiques et les emblèmes d'organisations internationales ne sont jamais reproduits. »

**H2 « Informations et prix »**
- « Les informations de ce site sont générales. Elles ne remplacent pas une visite ni un conseil adapté à votre situation. Les prix indicatifs éventuels ne constituent pas une offre : seule l'offre écrite remise après la visite engage l'entreprise. »

**H2 « Liens vers d'autres sites »**
- « Les liens vers des sites tiers (carte, registre du commerce, réseaux sociaux) ouvrent des sites soumis à leurs propres conditions et à leur propre politique de confidentialité. »

**H2 « Crédits »**
- « Polices de caractères : Montserrat et Source Sans 3, sous licence SIL Open Font License, hébergées sur ce site. Carte de la zone d'intervention : limites cantonales de swisstopo et de l'Office fédéral de la statistique, via le paquet swiss-maps (Interactive Things, licence BSD). »

**H2 « Protection des données »**
- « La façon dont nous traitons les données transmises par le formulaire et les statistiques du site est décrite dans notre politique de confidentialité. » Lien : « Lire la politique de confidentialité »

**H2 « Droit applicable »**
- « Ce site et son utilisation sont soumis au droit suisse. »

Pied du texte : « Dernière mise à jour : {{date du build}} »

---

## M. Confidentialité (`confidentialite.html`)

Le texte de la politique est rédigé par l'agent automatisation et relu par le juriste. Éléments fournis ici :
- **Title** (39 car.) : `Protection des données | Andy Construct`
- **Meta description** (132 car.) : `Comment Andy Construct traite les données du formulaire et des statistiques du site : finalités, durées, prestataires et vos droits.`
- Fil d'Ariane : « Accueil › Protection des données »
- **H1** : « Protection des données »
- Chapeau : « Ce que nous faisons des informations que vous nous transmettez, combien de temps nous les gardons, et comment exercer vos droits. »
- Rappel de ton : mêmes règles que le reste du site (phrases courtes, pas de jargon juridique non expliqué, un titre qui donne la réponse par section).

---

## N. Page 404 (`404.html`)

- **Title** (33 car.) : `Page introuvable | Andy Construct`
- **Meta description** (116 car.) : `Cette page n'existe pas ou a été déplacée. Retrouvez nos prestations, nos réalisations et notre numéro de téléphone.`
- Chiffre décoratif (masqué aux lecteurs d'écran) : « 404 »
- **H1** : « Cette page n'existe pas, ou elle a changé d'adresse »
- « Notre site a été refait : certaines adresses ont changé. Voici les pages les plus consultées : »
  - « Placo : cloisons, doublages, faux-plafonds »
  - « Peinture intérieure »
  - « Isolation acoustique »
  - « Cloisons isolantes »
  - « Nos réalisations »
  - « Contact et demande de devis »
- « Vous pouvez aussi nous appeler : +41 22 771 20 15, du lundi au vendredi, de 7 h à 18 h. » `[C03]`
- Bouton : « Retour à l'accueil »

---

## O. Textes alternatifs

Règle : 8 à 12 mots, ce que montre la photo, sans « photo de », sans lieu inventé, sans réécriture de la technique (`brief-seo.md` §9.2).

| Photo | Texte alternatif |
|---|---|
| `faux-plafond-placo-gorge-lumineuse-01` (héro) | Faux-plafond en plaques de plâtre à gorge lumineuse et spots, dans un hall |
| `faux-plafond-placo-gorge-lumineuse-02` | Faux-plafond arrondi en plaques de plâtre, éclairage intégré, au bout d'un couloir |
| `chantier-suspentes-ossature-01` | Suspentes et ossature métallique d'un faux-plafond, sous une dalle isolée |
| `habillage-placo-niches-arrondies-01` | Mur d'escalier habillé de plaques de plâtre à niches arrondies, avant peinture |
| `chantier-ossature-puits-de-lumiere-01` | Poseur fixant une ossature métallique garnie d'isolant, près d'un puits de lumière |
| `chantier-ossature-puits-de-lumiere-02` | Ossature métallique et isolant autour d'un puits de lumière, avant fermeture |
| `plafond-placo-ilot-ovale-01` (recadrée) | Îlot ovale suspendu en plaques de plâtre au-dessus d'un hall vitré |
| `panneaux-acoustiques-muraux-01` | Panneaux acoustiques muraux et plafond perforé contre l'écho d'une salle |
| `cadre-acoustique-salle-de-reunion-01` | Panneau acoustique mural imprimé d'un paysage, dans une salle de réunion |
| `chantier-salle-de-spectacle-01` | Salle de spectacle à balcons, vue de la scène pendant des travaux |
| `chantier-salle-de-spectacle-02` | Intervention sur un balcon de salle de spectacle, fauteuils protégés sous bâche |
| AA1 avant / après | « Avant : caisson en cours, plaques jointoyées sous une verrière » / « Après : caisson en plaques de plâtre fini sous une verrière » |
| AA2 | « Avant : gaine de ventilation apparente sous la charpente » / « Après : couloir au plafond lisse, gaine cachée » |
| AA3 | « Avant : fenêtre de toit, isolant visible et plafond noirci » / « Après : rampant blanc fini autour d'une fenêtre de toit » |
| AA4 | « Avant : appareil de ventilation entre les chevrons » / « Après : appareil habillé d'un caisson près d'une fenêtre cintrée » |
| AA5 | « Avant : réservations circulaires dans la dalle d'un couloir » / « Après : couloir au faux-plafond percé de puits de lumière ronds » |
| AA6 | « Avant : séjour avant travaux, devant une grande baie vitrée » / « Après : séjour avec faux-plafond en périphérie et spots » |
| AA7 | « Avant : ossature métallique d'une paroi cintrée » / « Après : couloir fini avec paroi cintrée et spots » |
| Logos des références | `nom_affiche` de `logos.json` (p. ex. « Piaget ») |
| Logo Andy Construct (en-tête) | Andy Construct, page d'accueil |
| Logo Andy Construct (pied de page) | Andy Construct |

---

## P. `llms.txt` v2

```
# Andy Construct

> Andy Construct est une entreprise de plâtrerie, de peinture et d'isolation intérieure basée à Carouge (Genève), active depuis 2007. Elle pose des cloisons, des doublages et des faux-plafonds en plaques de plâtre (placo), réalise la peinture intérieure, l'isolation acoustique (isolation phonique et correction de l'écho) et les cloisons isolantes, aussi appelées cloisons isothermes (isolation entre pièces chauffées et caves, garages ou combles). Elle travaille pour des particuliers, des régies et gérances, des architectes, des communes, des institutions et des entreprises, dans toute la Suisse romande.

Informations clés :

- Nom commercial : Andy Construct
- Raison sociale : Andy Construct, Chanton & Cie, société en nom collectif
- IDE : CHE-113.706.162 (registre du commerce du canton de Genève)
- Activité depuis le 1er juin 2007 (Perly-Certoux, puis Chêne-Bourg dès 2010, Carouge dès 2023)
- Adresse : Route des Acacias 48, 1227 Carouge (Genève), Suisse
- Téléphone : +41 22 771 20 15 ; sur les chantiers : +41 78 631 14 34
- E-mail : contact@andyconstruct.ch
- Horaires : du lundi au vendredi, 7 h – 18 h
- Zone : cantons de Genève, Vaud, Neuchâtel, Fribourg et Jura, Valais romand, Jura bernois
- Langue : français
- Ce que l'entreprise ne fait pas : façades, carrelage, chambres froides

Prestations (4) :

- Placo : cloisons, doublages, faux-plafonds, caissons en plaques de plâtre
- Peinture intérieure : logements, fins de bail, cages d'escalier, bureaux
- Isolation acoustique : doublages et faux-plafonds acoustiques, cloisons acoustiques, correction acoustique des salles
- Cloisons isolantes (isothermes) : cloisons et doublages isolants, isolation de plafonds de caves et de garages

Méthode : visite sur place, offre écrite détaillée poste par poste en CHF, chantier protégé et nettoyé, réception des finitions avec le client.

Maîtres d'ouvrage qui ont confié des travaux à l'entreprise (liste publiée par l'entreprise) : Ville de Genève ; Mairie de Plan-les-Ouates ; salle communale de Collonge-Bellerive ; OMC ; Conservatoire de musique de Genève ; HEAD – Genève ; Salle de l'Alhambra ; Harmonie Nautique de Genève ; Piaget ; UBS ; J. Safra Sarasin (anciennement Bank Sarasin) ; de Grisogono ; Celgene ; Labcorp (anciennement Covance), Meyrin ; Dipan, Nyon ; Energestion, Les Acacias ; hôtel à Chavannes-de-Bogis ; Domaine des Perrières, Coppet.

## Pages principales

- [Accueil](https://www.andyconstruct.ch/): présentation, prestations, méthode, questions fréquentes
- [Placo](https://www.andyconstruct.ch/placo.html): cloisons, doublages, faux-plafonds et caissons en plaques de plâtre ; prix et délais ; accord de la régie ou de la PPE
- [Peinture](https://www.andyconstruct.ch/peinture.html): peinture intérieure des logements, fins de bail, cages d'escalier et bureaux
- [Isolation acoustique](https://www.andyconstruct.ch/isolation-acoustique.html): bruit des voisins, différence entre isoler et corriger, doublage et faux-plafond acoustiques, correction de l'écho
- [Cloisons isolantes](https://www.andyconstruct.ch/cloisons-isothermes.html): cloisons isothermes, isolation de caves, garages et combles, subventions
- [Réalisations](https://www.andyconstruct.ch/realisations.html): projets photographiés, avant / après
- [Professionnels](https://www.andyconstruct.ch/professionnels.html): régies, architectes, communes ; méthode en immeuble habité ; lots CFC ; documents ; liste complète des références
- [L'entreprise](https://www.andyconstruct.ch/entreprise.html): histoire depuis 2007, méthode, engagements, identité vérifiable
- [Contact](https://www.andyconstruct.ch/contact.html): téléphones, horaires, adresse, formulaire de demande de devis, zone d'intervention

## Documents

- [Dossier de références (PDF)](https://www.andyconstruct.ch/documents/andy-construct-dossier-de-references.pdf)
- [Guide : réduire le bruit chez soi (PDF)](https://www.andyconstruct.ch/documents/guide-reduire-le-bruit.pdf)
- [Liste de contrôle : travaux en immeuble habité (PDF)](https://www.andyconstruct.ch/documents/liste-de-controle-immeuble-habite.pdf)

## Optional

- [Mentions légales](https://www.andyconstruct.ch/mentions-legales.html)
- [Protection des données](https://www.andyconstruct.ch/confidentialite.html)
```

En production, le générateur applique au `llms.txt` les mêmes confirmations que pour les pages : e-mail (`C30`), horaires (`C03`), OMC (`C22`), hôtel (`C22`), méthode (`C06`, `C07`), « ce que l'entreprise ne fait pas » (`C16`).

---

## Q. Aimants à prospects

### Q.1 Dossier de références (plaquette PDF, 6 pages, A4 portrait)

Charte du site ; texte de 12 pt au moins ; aucune photo d'illustration générique ; lisible imprimé en noir et blanc. Libre téléchargement, sans formulaire. Nom du fichier : `andy-construct-dossier-de-references.pdf`.

**Page 1 · Couverture**
- « Andy Construct »
- **« Dossier de références »**
- « Plâtrerie, faux-plafonds, peinture et isolation intérieure · Suisse romande »
- Photo : `faux-plafond-placo-gorge-lumineuse-01`
- « Carouge · inscrite au registre du commerce depuis 2007 »
- « Édition {{mois année}} »

**Page 2 · Qui nous sommes**
- **« En bref »** (résumé lisible par un tiers : propriétaire, assemblée de copropriétaires, exécutif communal)
  > Andy Construct est une entreprise genevoise de plâtrerie, de peinture et d'isolation intérieure, basée à Carouge. Elle pose des cloisons, des doublages et des faux-plafonds en plaques de plâtre, isole contre le bruit et contre le froid, et peint murs et plafonds. Elle travaille pour des communes, des institutions, des régies, des architectes, des entreprises et des particuliers, dans toute la Suisse romande.
- **« Identité »** (tableau) :
  - Raison sociale : Andy Construct, Chanton & Cie (société en nom collectif)
  - IDE : CHE-113.706.162 · registre du commerce du canton de Genève
  - Activité : depuis le 1er juin 2007
  - Siège : Route des Acacias 48, 1227 Carouge
  - Associés : Adnan Bajrami, Caroline Chanton Bajrami `[C10]`
  - Effectif : {{n}} personnes `[À CONFIRMER C24]` (repli : ligne masquée)
  - Association professionnelle : membre du GGE `[C11]` (repli : masqué)
  - Assurance responsabilité civile : attestation sur demande `[C12]` (repli : masqué)
  - Attestations AVS, LPP, impôts, convention collective : sur demande `[C13]` (repli : masqué)
- **« Quatre métiers »** :
  - Placo : cloisons, doublages, faux-plafonds, caissons
  - Peinture intérieure : logements, fins de bail, cages d'escalier, bureaux
  - Isolation acoustique : doublages et faux-plafonds acoustiques, correction de l'écho des salles
  - Cloisons isolantes : séparation des locaux chauffés et non chauffés, plafonds de caves et de garages
- **« Zone »** : « Toute la Suisse romande, depuis Carouge. »

**Page 3 · Références**
- **« Ils nous ont confié des travaux »**
- Liste par secteur (même liste que `professionnels.html#references`), avec, sous chaque nom : « {{année}} · {{nature des travaux}} » `[À CONFIRMER C22]`. Sans confirmation : le nom seul.
- **« Trois chantiers »** (une photo et 3 lignes chacun) : P1 (hall à gorge lumineuse), P2 (grande salle, ossature et isolant), AA6 ou P4. Pour chacun : type de lieu, contrainte, prestations (textes du §G.3).
- En bas de page : « Références citées avec l'accord des maîtres d'ouvrage. Contacts de référence sur demande. » `[C22]`

**Page 4 · Immeubles habités et lieux publics**
- **« Travailler dans un bâtiment habité ou ouvert au public »**
- Introduction : « Les plaintes et les retards naissent presque toujours d'un manque d'organisation. Voici ce que nous faisons à chaque chantier. »
- Les 8 points du §H.3 (mêmes textes, mêmes confirmations).
- **« Ce que contient notre offre »** `[C06, C28]` :
  - les postes et les quantités ;
  - les prix unitaires et le total en CHF, TVA indiquée ;
  - la durée des travaux et les dates possibles ;
  - ce qui n'est pas compris ;
  - les conditions de paiement ;
  - la durée de validité de l'offre.

**Page 5 · Lots et normes**
- **« Quatre métiers, trois lots »** (tableau) :
  - CFC 271 Plâtrerie : cloisons, doublages, caissons, isolation intégrée (thermique et acoustique)
  - CFC 283 Faux-plafonds : plafonds en plaques de plâtre, acoustiques, gorges lumineuses, trappes de visite `[C14]`
  - CFC 285 Traitement des surfaces intérieures : peinture des murs, plafonds et cages d'escalier
- **« Normes »** : « Exécution selon la norme SIA 118 lorsque le contrat s'y réfère. Isolation acoustique et thermique selon les exigences du projet (SIA 181, SIA 180). Protection incendie selon les prescriptions AEAI lorsque le projet l'exige. » `[C15, C33]`
- « Nous ne promettons pas de performance chiffrée sans mesure : elle est fixée par le projet, et nous posons un système qui y répond. »

**Page 6 · Nous consulter**
- **« Nous consulter »**
- Interlocuteurs : « {{Prénom Nom}}, {{rôle}} · {{e-mail direct}} · {{mobile}} » `[À CONFIRMER C09, C38]` (repli : coordonnées générales seulement)
- « Bureau : +41 22 771 20 15 · Sur les chantiers : +41 78 631 14 34 · contact@andyconstruct.ch »
- **« Envoyer un dossier de soumission »** : « Descriptif ou série de prix, plans, date de remise des offres. Fichiers lourds : un lien de transfert convient. »
- **« Nous inscrire comme entreprise à consulter »** : « Communes et institutions : nous vous transmettons nos attestations pour vos procédures de gré à gré et sur invitation. » `[C13]`
- **« Visiter un chantier en cours »** : « Sur rendez-vous, 20 minutes. » `[C40]` (repli : masqué)
- Code QR vers `https://www.andyconstruct.ch/professionnels.html?utm_source=plaquette&utm_medium=print&utm_campaign=dossier-references`, avec l'adresse écrite en clair dessous.
- Pied : « Andy Construct, Chanton & Cie · Route des Acacias 48 · 1227 Carouge · IDE CHE-113.706.162 · Document mis à jour le {{date}} »

### Q.2 Guide pour les propriétaires : « Réduire le bruit chez soi : ce qui marche vraiment »

PDF de 8 pages A5 (ou A4), version imprimée sur demande. Nom du fichier : `guide-reduire-le-bruit.pdf`. Le guide doit rester **valable quelle que soit l'entreprise choisie** : c'est ce qui le rend crédible.

**Plan**

| Page | Titre | Contenu |
|---|---|---|
| 1 | Couverture | Titre, sous-titre, « Un guide d'Andy Construct, Carouge », date |
| 2 | Quel bruit entendez-vous ? | Bruit aérien ou bruit d'impact, test simple |
| 3 | Isoler ou corriger | Une confusion fréquente, source de déceptions |
| 4 | Ce qui marche | Doublage, faux-plafond, cloison, points faibles |
| 5 | Ce qui ne marche pas | Idées reçues |
| 6 | Locataire ou copropriétaire | Qui décide, qui prévenir, parler au voisin |
| 7 | Huit questions à poser à une entreprise | Valables pour toutes |
| 8 | Et ensuite ? | Notre façon de travailler, contacts |

**Texte**

**Page 1**
- **Réduire le bruit chez soi**
- Ce qui marche vraiment, ce qui ne marche pas, et les questions à poser avant de signer.
- Un guide d'Andy Construct, entreprise de plâtrerie, de peinture et d'isolation à Carouge. Édition {{mois année}}.

**Page 2 · Quel bruit entendez-vous ?**
Avant de commander des travaux, il faut savoir d'où vient le bruit. Il en existe deux sortes, qui ne se traitent pas de la même façon.

**Le bruit aérien** voyage dans l'air : voix, télévision, musique, chien qui aboie. Il traverse les murs et les plafonds trop légers, et passe par les moindres ouvertures.

**Le bruit d'impact** naît d'un choc sur la structure : pas, talons, chaises qu'on tire, objets qui tombent. Il se propage dans le béton, puis ressort dans les pièces voisines.

**Un test simple.** Pendant une semaine, notez ce que vous entendez, d'où et à quelle heure.
- Vous entendez surtout des voix ou la télévision : c'est du bruit aérien. Une isolation chez vous peut nettement l'améliorer.
- Vous entendez surtout des pas ou des chocs au-dessus : c'est du bruit d'impact. Le plus efficace est d'agir sur le sol du voisin. Chez vous, on peut l'atténuer, pas le supprimer.

**Page 3 · Isoler ou corriger**
Deux problèmes se ressemblent, et c'est la source de beaucoup de déceptions.

**Isoler**, c'est empêcher le bruit de passer d'un local à l'autre. On a besoin d'une paroi lourde, désolidarisée de la structure et étanche à l'air.

**Corriger**, c'est réduire l'écho à l'intérieur d'une pièce : une salle à manger qui résonne, un séjour au carrelage et aux grandes baies vitrées. On ajoute des matériaux qui absorbent le son : rideaux épais, tapis, meubles, panneaux absorbants.

**À retenir.** Un panneau absorbant rend une pièce plus agréable, mais il ne vous protège pas du bruit du voisin. Une bonne isolation ne réduit pas l'écho de votre séjour. Si une entreprise vous propose l'un pour régler l'autre, demandez-lui pourquoi.

**Page 4 · Ce qui marche**
Le principe est toujours le même : une paroi lourde, posée sans contact rigide avec la structure, avec un isolant souple à l'intérieur. Les spécialistes parlent du principe « masse, ressort, masse ».

**Le doublage acoustique d'un mur.** Une ossature indépendante, posée à quelques millimètres du mur existant, une laine minérale, puis une ou deux plaques de plâtre. Efficace contre les voix et la télévision du voisin. La pièce perd en général 7 à 10 cm `[C18]`.

**Le faux-plafond acoustique.** Il est suspendu par des suspentes qui amortissent les vibrations, avec un isolant au-dessus. Il réduit les voix venant d'en haut, et en partie les bruits de pas.

**La cloison acoustique.** Deux ossatures séparées, un isolant, des plaques doublées. Pour une chambre, un bureau à domicile ou une pièce de musique.

**Les points faibles.** Le bruit passe là où l'on ne regarde pas : prises électriques placées dos à dos, gaines, portes creuses, bas de porte, joints autour des fenêtres, conduits. Une bonne isolation les traite tous. Sinon, le résultat déçoit.

**Page 5 · Ce qui ne marche pas**
- **Les boîtes à œufs et la mousse collée au mur.** Elles réduisent un peu l'écho, mais n'arrêtent pas le bruit qui traverse.
- **La « peinture isolante ».** Une couche de quelques dixièmes de millimètre ne change presque rien au bruit qui traverse un mur.
- **Une plaque collée directement sur le mur.** Sans désolidarisation, elle peut même transmettre certains bruits.
- **Le liège mince ou le papier peint épais.** Agréables au toucher, sans effet sur le bruit du voisin.
- **Une isolation d'un seul côté de la pièce, quand le bruit vient d'ailleurs.** Le bruit contourne : il passe par le plafond, le sol ou le mur voisin.

**Page 6 · Locataire ou copropriétaire ?**
**Vous êtes locataire.** Avant de transformer le logement, il vous faut l'accord écrit de votre bailleur ou de votre régie. Demandez-le avant de signer quoi que ce soit avec une entreprise. Une entreprise sérieuse peut vous remettre un descriptif des travaux à joindre à votre demande.

**Vous êtes en PPE (propriété par étages).** Les travaux dans votre lot sont en général possibles. Ceux qui touchent un mur mitoyen, la structure ou une partie commune peuvent demander l'accord de l'administrateur ou de l'assemblée. Lisez votre règlement et posez la question avant de commencer.

**Parlez à votre voisin.** Si vous entendez surtout des pas, un tapis ou une sous-couche chez lui peut faire plus qu'un faux-plafond chez vous. Une conversation calme, une lettre courtoise : cela règle parfois plus vite le problème que des travaux.

*Ces informations sont générales et ne remplacent pas un conseil juridique.*

**Page 7 · Huit questions à poser à une entreprise**
Valables pour nous comme pour les autres.
1. Êtes-vous venu voir les lieux avant de chiffrer ?
2. Quel type de bruit avez-vous identifié, et pourquoi proposez-vous ces travaux ?
3. Que traitez-vous en plus de la paroi : prises, gaines, portes, raccords ?
4. Combien de centimètres la pièce va-t-elle perdre ?
5. Que contient l'offre, et qu'est-ce qui n'y est pas compris ?
6. Qui vient faire les travaux, et qui est mon interlocuteur ?
7. Comment la poussière et les meubles sont-ils protégés ?
8. Que se passe-t-il si le résultat n'est pas celui annoncé ?

**Méfiez-vous** d'une promesse de résultat en décibels sans aucune mesure, d'un prix donné au téléphone sans visite, ou d'un acompte demandé en liquide.

**Page 8 · Et ensuite ?**
Chaque logement est différent : le bon remède dépend du bruit, de la construction et de l'usage de la pièce.
Nous travaillons ainsi :
1. **Visite** : nous écoutons, nous mesurons, nous regardons d'où vient le bruit.
2. **Offre écrite** : poste par poste, en CHF, avec la place perdue et ce qui n'est pas compris. `[C06]`
3. **Chantier protégé** : sols et meubles couverts, nettoyage chaque soir. `[C07]`
4. **Réception** : nous faisons le tour des finitions avec vous.

**Demander une visite** : +41 22 771 20 15 (du lundi au vendredi, 7 h – 18 h `[C03]`) ou www.andyconstruct.ch/isolation-acoustique.html

Andy Construct, Chanton & Cie · Route des Acacias 48 · 1227 Carouge · IDE CHE-113.706.162

### Q.3 Guide pour les régies : « Travaux en immeuble habité : la liste de contrôle de la régie »

PDF de 2 pages A4, plus le modèle d'avis aux locataires en Word. Nom des fichiers : `liste-de-controle-immeuble-habite.pdf` et `modele-avis-aux-locataires.docx`.

**Plan**

| Page | Contenu |
|---|---|
| 1 recto | Titre, pourquoi cette liste, **Avant les travaux** (10 cases à cocher) |
| 1 verso | **Pendant les travaux** (7 cases), **Après les travaux** (6 cases) |
| 2 | Modèle d'avis aux locataires (aussi en Word) et rappel juridique |

**Texte**

**Travaux en immeuble habité : la liste de contrôle de la régie**
Peinture d'une cage d'escalier, plafond après un dégât d'eau, remise en état d'un appartement voisin : les plaintes et les retards viennent presque toujours d'un manque d'information ou d'organisation. Cette liste vous aide à préparer le chantier, quelle que soit l'entreprise.

**Avant les travaux**
- ☐ Le périmètre est écrit : logements, parties communes, étages concernés.
- ☐ Les dates de début et de fin sont fixées, avec une marge pour les imprévus.
- ☐ Le propriétaire ou le mandant a validé l'offre et le calendrier des travaux.
- ☐ Les locataires sont informés par écrit au moins 10 jours avant (modèle au verso).
- ☐ Le concierge connaît les dates, les horaires et le nom du responsable du chantier.
- ☐ L'accès est réglé : clés, badges, horaires d'ouverture, présence nécessaire ou non des locataires.
- ☐ L'ascenseur, les sols et les murs des parties communes seront protégés.
- ☐ Un emplacement est prévu pour le matériel et l'évacuation des déchets.
- ☐ Le stationnement du véhicule de l'entreprise est prévu.
- ☐ Vous avez le nom et le portable du responsable de chantier.

**Pendant les travaux**
- ☐ Les horaires annoncés sont respectés.
- ☐ La poussière est contenue : zones fermées, aspiration.
- ☐ Les passages restent libres et propres chaque soir.
- ☐ Les locataires savent qui appeler en cas de question.
- ☐ Tout imprévu est signalé avec son prix **avant** d'être exécuté.
- ☐ Un point rapide est fait en fin de semaine (téléphone ou e-mail).
- ☐ Les éventuelles plaintes sont notées et traitées le jour même.

**Après les travaux**
- ☐ Le nettoyage final est fait.
- ☐ La réception a lieu avec l'entreprise, avec un procès-verbal.
- ☐ Les retouches sont listées, avec un délai pour les lever.
- ☐ Des photos avant / après sont jointes au dossier, pour le propriétaire.
- ☐ La facture correspond à l'offre, plus-values validées comprises.
- ☐ Les locataires sont informés de la fin des travaux.

**Modèle d'avis aux locataires**

> **Travaux dans votre immeuble**
>
> Madame, Monsieur,
>
> Des travaux de {{nature des travaux}} auront lieu dans l'immeuble {{adresse}}, du {{date de début}} au {{date de fin}}.
>
> **Où** : {{parties communes, étages, logements concernés}}
> **Horaires** : du lundi au vendredi, de {{heure}} à {{heure}}
> **Ce qui change pour vous** : {{accès, ascenseur, bruit, poussière, présence nécessaire dans le logement}}
>
> L'entreprise {{nom de l'entreprise}} protège les parties communes et nettoie chaque soir. Pour toute question sur le chantier : {{nom du responsable}}, {{téléphone}}. Pour toute autre question : {{régie}}, {{téléphone de la régie}}.
>
> Nous vous remercions de votre compréhension.
>
> {{Régie}}, le {{date}}

**Bon à savoir** : pendant des travaux de rénovation, le locataire peut, selon les cas, demander une réduction de loyer (art. 259d et 260 du Code des obligations). Une information claire et des nuisances limitées réduisent ce risque. *Information générale, qui ne remplace pas un conseil juridique.* `[À VÉRIFIER : relecture juridique]`

**Pied** : « Andy Construct : plâtrerie, faux-plafonds, peinture et isolation en immeuble habité. +41 22 771 20 15 · www.andyconstruct.ch/professionnels.html · Andy Construct, Chanton & Cie, Carouge, IDE CHE-113.706.162 »

### Q.4 Blocs de téléchargement sur le site

**Dossier de références** (professionnels, pied de page) :
- Bouton : « Télécharger le dossier de références (PDF, {{poids}}) »
- Sous le bouton : « 6 pages : identité, références, méthode en immeuble habité, lots CFC, contacts. Libre téléchargement, sans inscription. »

**Liste de contrôle « régie »** (professionnels) :
- Lien : « Télécharger la liste de contrôle « immeuble habité » (PDF, 2 pages) »
- Lien : « Télécharger le modèle d'avis aux locataires (Word) »

**Guide « bruit »** (isolation acoustique) :
- Bouton : « Télécharger le guide (PDF, {{poids}}) »
- Lien : « Le recevoir imprimé, par la poste »
- Petit formulaire « par la poste » (`formulaire=aimant`, `aimant=guide-bruit`, `par_poste=oui`) :
  - Titre : « Recevoir le guide imprimé »
  - « Votre nom » (`nom`, obligatoire) — erreur : « Indiquez votre nom pour l'envoi par la poste. »
  - « Votre adresse » (`adresse_postale`, zone de 3 lignes, obligatoire) — aide : « Rue et numéro, NPA et localité. » — erreur : « Indiquez l'adresse à laquelle envoyer le guide (rue, NPA et localité). »
  - « Vous êtes » (`profil`, facultatif) : Propriétaire · Locataire · Autre
  - Case non cochée (`accord`) : « J'accepte que mon adresse serve uniquement à l'envoi de ce guide (protection des données). »
  - Bouton : « Recevoir le guide par la poste »
  - Sous le bouton : « Envoi sous quelques jours ouvrables. Pas de publicité. »
  - Message de succès (sur la page, sans redirection) : « Merci. Le guide part par la poste dans les prochains jours. »

---

## R. Questions au client (liste consolidée)

Une question par identifiant. **P1** = bloquant avant la mise en ligne (affiché en haut de page, dans le formulaire ou dans les mentions) ; **P2** = important pour la conversion ou la preuve ; **P3** = complément. La colonne « Repli » dit ce qui est publié sans réponse.

### R.1 Priorité 1 (avant la mise en ligne)

| ID | Question | Pages | Repli sans réponse |
|---|---|---|---|
| C01 | Dans quel délai pouvez-vous **toujours** rappeler une demande ? (proposé : « le jour même ou le jour ouvrable suivant ») | Formulaire, rappel, merci, contact, FAQ accueil, professionnels | « Pendant nos heures de bureau » |
| C02 | La visite et le devis sont-ils gratuits et sans engagement ? Dans toute la zone ? | Héro, formulaire, FAQ accueil | Pas de mention de gratuité |
| C03 | Vos horaires (lun-ven, 7 h – 18 h) sont-ils exacts ? Quelqu'un répond-il au fixe pendant ces heures, ou l'appel est-il renvoyé sur un mobile ? | En-tête, pied, contact, héro, merci | Horaires masqués |
| C05 | Réalisez-vous vous-mêmes les 4 métiers ? Sous-traitez-vous une partie (peinture, par exemple) ? Peut-on écrire « un seul interlocuteur, de la pose des plaques à la dernière couche » ? | Héro, placo, peinture, entreprise | Phrases sans « un seul interlocuteur » ni « nous peignons aussi » |
| C06 | Engagements de méthode : visite avant chaque offre ; offre détaillée poste par poste en CHF, avec la durée et les exclusions ; **aucun supplément sans accord écrit et chiffré**. Pouvez-vous vous y engager ? | Méthode (toutes pages), entreprise, plaquette | Méthode réduite (« Nous vous remettons une offre écrite ») ; engagement masqué |
| C07 | Protection et nettoyage : sols et meubles protégés, nettoyage chaque soir, nettoyage à fond le dernier jour. Est-ce votre pratique ? | Méthode, FAQ, peinture, professionnels | « Les lieux sont protégés pendant les travaux » ; questions masquées |
| C16 | « Cloisons isothermes » : s'agit-il bien de cloisons et doublages **isolants** entre locaux chauffés et non chauffés (et non de chambres froides) ? Isolez-vous aussi les plafonds de caves et de garages, et les combles ? Acceptez-vous le nom affiché « Cloisons isolantes » ? | Menu, page cloisons, cartes, llms.txt | « Cloisons isothermes » ; H3 et questions sur les combles masqués |
| C22 | Pour chacune des 18 références : année, nature des travaux, accord pour citer le nom (et le logo pour les marques). L'OMC a-t-elle donné son accord pour son nom ? L'« Hôtel Chavannes-de-Bogis » est-il l'actuel Everness ? | Bandeau, professionnels, plaquette, llms.txt | Noms en texte sans année ; OMC remplacée par la Salle de l'Alhambra ; « Hôtel à Chavannes-de-Bogis » |
| C25 | Photos : technique posée, type de bâtiment et commune de chaque projet (P1 à P8) ; accord du poseur visible (IMG_5922) ; accord du client dont le slogan est lisible (P1000435) ; prestation réalisée dans la salle de spectacle ; confirmez-vous que toutes les photos sont vos réalisations ? | Accueil, réalisations, pages services | Légendes de repli (ce que montre la photo) ; photos concernées retirées si l'accord manque |
| C29 | Route des Acacias 48 : y a-t-il un bureau où l'on peut vous rencontrer, ou est-ce une adresse de domiciliation ? Peut-on retirer Chêne-Bourg partout ? | Contact, pied, fiche Google | Adresse affichée sans « sur rendez-vous » |
| C30 | Adresse e-mail sur le domaine (contact@andyconstruct.ch) ? Numéro principal : le fixe ? Peut-on présenter le mobile comme « sur les chantiers » ? | Partout | andy.construct@bluewin.ch ; mobile présenté comme « Mobile » |
| C34 | Nom et adresse de l'hébergeur de production | Mentions légales | « Le site est hébergé en Suisse » |

### R.2 Priorité 2 (conversion et preuve)

| ID | Question | Pages | Repli |
|---|---|---|---|
| C04 | Acceptez-vous les petits chantiers (une pièce, une cloison) ? Y a-t-il un montant minimal ? | Bandeau, FAQ accueil | Phrase neutre sur les particuliers ; question masquée |
| C08 | Délai habituel d'envoi de l'offre après la visite (« sous X jours ouvrables ») | Merci, méthode | « Vous recevez ensuite notre offre écrite » |
| C09 | Qui rappelle les demandes ? Peut-on le nommer (prénom, photo) sur le site, dans les e-mails et sur la page merci ? | Merci, professionnels, plaquette | « Nous vous rappelons » |
| C10 | Les associés acceptent-ils d'être nommés (et photographiés) sur la page Entreprise et dans les mentions légales ? Rôle de chacun ? | Entreprise, mentions, plaquette | Noms et section équipe masqués |
| C11 | Êtes-vous membre du GGE ? Depuis quand ? Autres affiliations (GPG, FREPP) ? | Entreprise, plaquette, JSON-LD | Ligne masquée |
| C12 | Assurance responsabilité civile d'entreprise : attestation disponible ? | Entreprise, professionnels, plaquette | Ligne masquée |
| C13 | Attestations AVS, LPP, impôts, convention collective du second œuvre (ou engagement OCIRT) disponibles sur demande ? | Professionnels, plaquette | Lignes masquées |
| C14 | Lots CFC traités : 271, 283, 285 ? | Placo, peinture, professionnels, plaquette | « 271 Plâtrerie · 285 Peinture » |
| C15 | Normes : contrats selon la SIA 118 ? Exigences SIA 181 et SIA 180 respectées selon le projet ? Posez-vous des systèmes coupe-feu (AEAI) ? | Professionnels, acoustique, cloisons, plaquette | Phrase générique « performances du projet » |
| C17 | Peinture : déroulé habituel (préparation, nombre de couches), fins de bail pour régies, prix par pièce pour régies, échantillons de teinte, déplacement des meubles ? | Peinture | Phrases générales, éléments non confirmés masqués |
| C18 | Acoustique : systèmes posés (doublage désolidarisé, faux-plafond sur suspentes antivibratiles, cloison double) ; épaisseurs usuelles ; la correction acoustique (panneaux, cadres, plafonds perforés) fait-elle toujours partie de l'offre ? Travaillez-vous avec des bureaux d'acoustique ? | Acoustique, guide bruit, réalisations | « Quelques centimètres » ; correction et questions liées masquées ; P6, P7 retirés |
| C19 | Travaux le soir, le week-end, pendant les vacances scolaires ? | Peinture, professionnels | « Zone par zone » |
| C20 | Travaux en immeuble habité : préparez-vous l'avis aux locataires ? Horaires convenus ? Peut-on publier les 8 points de la méthode « site occupé » ? | Professionnels, peinture, plaquette, guide régie | Points non confirmés retirés |
| C21 | Zone : souhaitez-vous limiter les chantiers de particuliers à Genève et à La Côte ? Frais de déplacement hors de Genève ? Quelles villes afficher sur la carte ? | FAQ accueil, contact | « Toute la Suisse romande » pour tous |
| C23 | Pour chaque service, quelles références citer (« Réalisé notamment pour ») ? | Pages services | Ligne de références générique |
| C24 | Combien de personnes travaillent dans l'entreprise ? | Entreprise, plaquette | Masqué |
| C26 | Avant / après : avez-vous les originaux des 7 paires ? Lieux et prestations ? | Accueil, réalisations, peinture, cloisons | Paires de faible qualité non publiées |
| C28 | Conditions de paiement : jamais de liquide à l'avance ? Acompte ? | Entreprise, plaquette | Masqué |
| C31 | Fourchettes de prix réelles pour 4 cas types (cloison de 10 m² ; peinture d'un 3,5 pièces ; doublage acoustique d'un mur de 12 m² ; cloison isolante de 10 m²) et durée type d'une peinture d'appartement | FAQ des pages services, page prix (phase 2) | Facteurs de prix sans chiffres |
| C32 | Après la réception : revenez-vous pour les retouches ? Proposez-vous un contrôle avant la fin de la garantie ? | Méthode, FAQ, entreprise | « Nous examinons le défaut avec vous » |
| C33 | Vos contrats se réfèrent-ils à la norme SIA 118 ? | Professionnels, entreprise | Mention de la SIA 118 au conditionnel |
| C35 | Êtes-vous assujettis à la TVA ? Numéro ? | Mentions | Masqué |
| C38 | Interlocuteurs à indiquer dans la plaquette (nom, rôle, e-mail direct, mobile) | Plaquette | Coordonnées générales |
| C39 | 5 à 10 chantiers récents (2017-2026) avec photos, lieu, année, prestation | Réalisations, accueil | Projets sans année |
| C40 | Photos de chantiers de peinture ; visite d'un chantier en cours possible pour les professionnels ? Taille maximale des dossiers de soumission reçus par e-mail ? | Peinture, professionnels | Section peinture masquée ; visite masquée |
| C41 | Délai habituel pour une visite après le premier appel | FAQ accueil, merci | « Nous convenons d'une date de visite » |

### R.3 Priorité 3 (compléments)

| ID | Question | Pages | Repli |
|---|---|---|---|
| C27 | Nombre approximatif de chantiers réalisés depuis 2007 (chiffre vérifiable, à partir de vos factures ou de votre agenda) | Aucun texte au lancement ; chiffre ajouté sur la page Entreprise et dans la plaquette seulement s'il est vérifiable | Aucun chiffre (« 300+ » retiré) |
| C36 | D'où vient le nom « Andy » ? (pour une ligne de la page Entreprise) | Entreprise | Rien |
| C37 | La fiche Google existe-t-elle ? Qui y a accès ? Combien d'avis ? | Bloc avis (masqué tant qu'il y a moins de 5 avis) | Masqué |
| C44 | Témoignages : quels clients accepteraient 2 ou 3 phrases signées (lettre type de `logos-references.md` §7.2) ? | Accueil, réalisations | Bloc masqué |
| C42 | Formez-vous des apprentis ? | Entreprise, plaquette | Rien |
| C43 | Subventions : fournissez-vous les informations techniques (épaisseur, valeur U) pour les demandes ? | Cloisons isolantes | Phrase sans proposition d'aide |

### R.4 Décisions à prendre par le client (non factuelles)

1. Nom affiché « Cloisons isolantes » (`C16`).
2. Retrait en production des 19 photos hors offre (`architecture-cro.md` §8.4), ou leur regroupement sous « Autres réalisations (hors offre actuelle) ».
3. Shooting de 3 ou 4 chantiers en cours (peinture, cloison isolante, acoustique, une paire avant / après).
4. Envoi des lettres d'autorisation aux 18 références (lettres types prêtes).
5. Remplacement de la case de consentement par une mention d'information, après avis du juriste.

---

## Annexe · Comptage des mots visibles de l'accueil

Comptage du texte définitif des sections B.1 à B.8, hors questions et réponses de la FAQ et hors pied de page. Il comprend tout ce qui est affiché quand le formulaire montre son étape 1 : libellés des cartes, réassurance, module de rappel, colonne « Par téléphone », ligne de références. Un mot = une suite de caractères séparée par des espaces, contenant au moins une lettre ou un chiffre (les « · » et « – » ne comptent pas). Les 8 noms du bandeau comptent pour leurs mots.

| Section | Mots |
|---|---|
| B.1 Héro (surtitre, H1, sous-titre, boutons, horaires, 3 faits) | 74 |
| B.2 Bandeau de références | 43 |
| B.3 Prestations (titres, 4 cartes, phrase, bouton) | 101 |
| B.4 Réalisations (titres, 3 cartes, lien, bouton) | 80 |
| B.5 Méthode (titres, 4 étapes, engagement, lien) | 85 |
| B.6 Professionnels et zone | 36 |
| B.7 FAQ (surtitre, titre et phrase d'appel seulement) | 14 |
| B.8 Demande (titres, intro, étape 1, réassurance, rappel, téléphone, ligne de références) | 192 |
| **Total** | **625** |

Hors bloc de demande : 433 mots. Avec les textes de repli (si les confirmations manquent), le total baisse d'une dizaine de mots. Cible du chef de projet : 450 à 650 mots. Maquette v1 : 1'298 mots.

### R.5 Index par page

| Page ou support | Identifiants concernés |
|---|---|
| Éléments communs (en-tête, pied de page, formulaire, rappel) | C01, C02, C03, C16, C22, C30 |
| Accueil | C01, C02, C03, C04, C05, C06, C07, C21, C22, C25, C26, C32, C41 |
| Placo | C05, C06, C07, C14, C23, C25, C31 |
| Peinture | C05, C06, C07, C17, C19, C20, C23, C26, C31, C40 |
| Isolation acoustique | C15, C18, C23, C25, C31 |
| Cloisons isolantes | C15, C16, C25, C26, C31, C43 |
| Réalisations | C22, C25, C26, C39, C44 |
| Professionnels | C01, C09, C12, C13, C14, C15, C19, C20, C22, C30, C33, C40 |
| L'entreprise | C05, C06, C07, C09, C10, C11, C12, C24, C27, C28, C32, C36, C42 |
| Contact | C01, C03, C21, C29, C30 |
| Merci | C01, C03, C08, C09, C41 |
| Mentions légales | C10, C25, C30, C34, C35 |
| Bloc avis Google | C37 |
| Plaquette PDF | C06, C09, C10, C11, C12, C13, C14, C15, C22, C24, C28, C33, C38, C40 |
| Guides PDF | C03, C06, C07, C18, C20 |
| `llms.txt` | C03, C06, C07, C16, C22, C30 |
