# CRO v3 : accueil, en-tête, badges de confiance, drapeaux de test, coupes et formulaire

*Andy Construct · site v3 · expert CRO et copywriter senior · 31 octobre 2026*
*Base : v2 (`a633851`). Ce document applique `docs/v3/brief-v3.md`, qui prime sur la v2. Il réutilise les identifiants de confirmation `C01` à `C44` et `V01`, `V02` de `tools/build/donnees/confirmations.json` : aucun nouvel identifiant n'est créé. Contrat de l'API inchangé (`docs/v2/contrat-interface.md`).*

Conventions : `[À CONFIRMER Cxx : …]` suivi de « Repli : … » = texte publié en production tant que la confirmation manque (« masqué » = le bloc disparaît). **Gras** = mot mis en valeur dans le texte courant (jamais dans un titre, jamais en couleur). Les textes entre guillemets s'intègrent tels quels ; le générateur ajoute les espaces insécables (`fr()`).

---

## 0. En bref

1. **Diagnostic copywriting : situation B** (voix réelle, sobre, factuelle). On garde le lexique v2 (« Demander un devis », « offre écrite », « Ils nous ont confié des travaux ») et on coupe : l'accueil passe de **625 à 404 mots visibles** hors FAQ, dont 56 noms de références (§2.4).
2. **Levier bloquant (skill offers, équation de valeur) : la probabilité perçue.** Le résultat promis est clair ; ce qui manque, c'est la preuve visible. D'où la preuve sociale en fil conducteur : mur de références, chiffres, lieux nommés, rappel à chaque appel à l'action, avis et témoignages dès qu'ils existent, pied de page.
3. **Nouveau titre** : « Placo, peinture, acoustique : la rigueur des chantiers publics » (positionnement de `.claude/product-marketing.md`), deux variantes testables.
4. **Mur de références 100 % typographique en production** tant que moins de 6 logos sont autorisés : aucun des 18 n'a aujourd'hui le statut `autorise`, donc un mur « logos + noms » serait un patchwork en preview et une liste grise en production. Règle de mélange au §2.3.
5. **En-tête allégé** : 4 entrées, un téléphone sans horaires, un seul bouton rouge, compact au défilement. Pas de barre supérieure de références.
6. **Badges de confiance** pilotés par `confirmations.json` : 2 badges vérifiés au lancement, jusqu'à 4 dès que `C02`, `C11`, `C12` ou `C01` sont confirmés.
7. **Tests A/B réalistes** : avec environ 800 visiteurs par mois sur l'accueil (hypothèse à mesurer), seuls des effets d'au moins +50 % sont détectables, en 6 à 9 semaines. Programme de 5 mois, une expérience à la fois par page, rodage de 2 semaines.
8. **Aucune preuve inventée.** Deux corrections d'honnêteté : le chiffre « 18 références » est calculé à partir des noms publiables (17 en production tant que l'accord de l'OMC manque) ; sur les pages services, une liste de références n'est présentée comme propre au service que si `C23` le confirme.

### 0.1 Règles v2 levées ou maintenues (audience 30-60 ans)

| Règle v2 | v3 | Pourquoi |
|---|---|---|
| 3 expositions de preuve par page au plus | **Levée sur l'accueil** : 6 expositions, chacune sous une forme différente (mur, chiffres, lieux, avis, ligne près du formulaire, pied) | Retour client « pas assez de preuve sociale, vraiment pas ». La lassitude vient de la répétition identique, pas du nombre : on varie la forme |
| Jamais deux blocs de références identiques dans le même écran | **Maintenue** | Mur et chiffres se suivent, mais ne répètent pas les mêmes noms |
| Bandeau statique, aucun compteur animé | **Levée** (brief §2) : défilement continu pausable, compteurs animés une fois | Valeur finale toujours écrite dans le HTML ; `prefers-reduced-motion` respecté |
| Même liste courte, dans le même ordre, partout | **Maintenue**, avec 3 longueurs canoniques (§2.3) | Effet de simple exposition |
| « Nous ont confié des travaux », jamais « recommandent » ni « partenaires » | **Maintenue** | Exactitude (D5) |
| Surtitres en capitales sur chaque section | **Supprimée** sur l'accueil | 6 surtitres en v2 : bruit visuel, aspect « modèle » |

### 0.2 Affirmations écartées et ce qui les débloquerait (skill copywriting)

| Affirmation demandée ou tentante | Pourquoi elle ne part pas | Ce qui la débloque |
|---|---|---|
| « 300+ chantiers » ou tout nombre de chantiers | Aucune source | `C27` : comptage depuis les factures ou l'agenda |
| « 18 références publiques » | Se lit « 18 clients du secteur public » : faux (environ 7 le sont) | Écrire « 18 références, publiques et privées » |
| Note ou avis clients | Aucun avis public | `C37` : fiche Google gérée, 5 avis au moins |
| « Un seul interlocuteur, de la pose à la peinture » | Sous-traitance non exclue | `C05` |
| « Rappel dans l'heure », « devis en 24 h » | Délai non garanti | `C01`, `C08` (journal des rappels sur 4 semaines) |
| Travaux précis réalisés au Conservatoire, à l'Alhambra, à Plan-les-Ouates | Nature et année inconnues | `C22` (nature, année), `C25` (photos rattachées à un lieu) |
| « Membre du GGE » | L'entité JSON-LD pointe déjà vers une fiche gge.ch, mais rien n'est confirmé | `C11` |

---

## 1. Diagnostic CRO de l'accueil v2

Contexte (skill cro) : page d'accueil ; conversion principale = demande de devis (formulaire 3 étapes) ; secondaires = appel, rappel, dossier PDF. Trafic attendu : recherche locale, recherche de marque, annonces surtout vers les pages services (`strategie-acquisition.md`, scénario M). Aucune mesure en place (`config.json` : Umami vide).

Classement : **E** = impact élevé, **M** = moyen, **F** = faible. Colonne « v3 » = où la correction est décrite.

| # | Dimension | Constat | Impact | v3 |
|---|---|---|---|---|
| 1 | Proposition de valeur | H1 « Placo, peinture et isolation en Suisse romande » : une catégorie, pas un choix. Il échoue au test de substitution (n'importe quel concurrent peut l'écrire). Le seul argument distinctif, les références publiques, arrive sous le pli, en petit. | E | §2.2 H1 |
| 2 | Titre et sous-titre | Le sous-titre (21 mots) répète les métiers du H1, et sa promesse « un seul interlocuteur » dépend de `C05`. En production, le repli supprime la promesse : le héro n'a plus aucun différenciateur. | E | §2.2 H1 |
| 3 | Preuve sociale | Une seule preuve avant le formulaire : un bandeau de 8 éléments mêlant 4 logos et 4 noms, petits, sans hiérarchie. En production, les logos `a_autoriser` deviennent des noms et l'OMC disparaît : la preuve la plus forte devient une ligne de noms gris. | E | §2.2 H2, §2.3 |
| 4 | Preuve sociale | Les cartes « Réalisations » ne nomment aucun lieu ni client (`C22`), aucun chiffre n'est mis en scène, aucun avis n'existe. Le seul type de preuve disponible (des noms) est sous-exploité. | E | §2.2 H3, H5 |
| 5 | Hiérarchie visuelle | Aucun mot en gras dans le texte ; 6 surtitres ; 9 sections de longueur égale (le « parfait équilibre » qui fait générique) ; les faits du héro ont tous le même poids. Les mots importants ne ressortent pas. | E | §2.1, §2.2 |
| 6 | Images | Une photo de héro et trois vignettes, dont deux « pendant les travaux » : aspect chantier, pas premium. Aucune image sur les prestations. | M | §2.2 H4, H5, H6 |
| 7 | CTA | Premier écran : bouton d'en-tête, numéro d'en-tête avec horaires, deux boutons de héro de poids proche, ligne d'horaires : 4 actions de contact. Le choix se dilue (loi de Hick). | M | §2.2 H1, §3 |
| 8 | En-tête | 8 éléments (logo, 5 entrées, téléphone avec horaires, bouton), 80 px permanents, jamais compact. Client : « mal aligné, trop d'informations, trop d'espace vide ». | M | §3 |
| 9 | Longueur | 625 mots visibles hors FAQ, dont 192 dans le bloc de demande (rappel, colonne téléphone, ligne de références) ; 8 questions de FAQ. On lit environ 20 % des mots d'une page. | M | §2.4 |
| 10 | Objections | « Trop gros pour moi » traité par une seule phrase (repli de `C04` faible) ; « combien » sans fourchette (`C31`) ; délais de rappel et de visite en attente (`C01`, `C41`). En production, la réassurance devient vague. | M | §2.2 H2, H8, §7 |
| 11 | Signaux de confiance | Le lien vers le registre du commerce n'apparaît qu'en bas du pied de page ; affiliation et assurance invisibles ; aucun système de badges. Les signaux vérifiables existent mais sont mal exposés. | M | §4 |
| 12 | Friction du formulaire | Étape 3 : 8 champs visibles (au-delà des 6 ou 7 conseillés) ; libellés conditionnels « obligatoire si pas d'e-mail » et « si pas de téléphone » difficiles à lire ; réassurance placée sous tout le formulaire, loin du bouton ; sur mobile, le bouton « Demander un devis » de la barre fixe reste affiché devant le formulaire. | M | §7 |
| 13 | Parcours professionnel | Le dossier de références (PDF libre, le meilleur atout B2B) n'est relié à aucune preuve de l'accueil ; il ne vit que dans une petite bande à deux colonnes. | F | §2.2 H5 |
| 14 | Perception | Aucun mouvement : rien ne signale le soin. Le brief demande un site « un peu animé ». | F | §2.2 (colonne « mouvement ») |
| 15 | Mesure | Aucune donnée de base, aucun dispositif de test. Les tests T1 à T8 de la v2 restent théoriques. | F (bloquant pour la suite) | §5 |

**Gains rapides** : 1, 2, 5, 7, 12 (texte et gabarit). **Changements à fort impact** : 3, 4, 6 (mur, chiffres, projets nommés, images). **À tester** : §5.

---

## 2. Accueil v3

### 2.1 Sections v2 → v3

| v2 | Décision | v3 |
|---|---|---|
| B.1 Héro | **Garder, réécrire** | H1 · titre, sous-titre, 2 boutons, barre de badges ; surtitre et ligne d'horaires supprimés |
| B.2 Bandeau de références | **Remplacer** | H2 · mur de références, puis H3 · chiffres clés |
| B.3 Prestations | **Garder, raccourcir** | H4 · 4 cartes illustrées ; phrase « Vous hésitez ? » et bouton supprimés |
| B.4 Réalisations | **Fusionner** | H5 · projets de référence (lieux nommés) + une carte avant / après ; les photos P1 et P2 passent sur les cartes prestations |
| B.5 Méthode | **Garder, raccourcir** | H6 · 4 étapes de 5 à 7 mots, engagement intégré |
| Témoignages (masqué) | **Garder** | H7 · avis Google et témoignages, masqués tant qu'ils sont vides |
| B.6 Professionnels et zone | **Supprimer** | Zone → chiffre « 7 » et badge ; professionnels → lien PDF sous les projets et menu |
| B.7 FAQ (8) | **Garder, réduire** | H8 · 6 questions |
| B.8 Demande | **Garder, alléger** | H9 · rappel de références au-dessus, colonne réduite au téléphone et à 3 badges, module de rappel replié |
| B.9 Pied de page | **Garder, enrichir** | H10 · badges et ligne de références typographique |

Rythme obtenu : preuve, preuve, offre, preuve, méthode, preuve, questions, preuve et demande, preuve. Leviers (skill marketing-psychology) : autorité vérifiable, preuve sociale, simple exposition, position sérielle (noms forts en tête et en fin de liste), réduction du risque, loi de Hick (un bouton principal par écran).

### 2.2 Section par section, dans l'ordre

**Règle du gras** : un groupe de 1 à 4 mots par paragraphe ou par carte, au plus ; jamais dans un titre, un bouton ou un badge.

#### H1 · Héro

- **Nature** : plein cadre (min. 100svh, 860 px au plus sur ordinateur, environ 88svh sur mobile). Photo réelle `faux-plafond-placo-gorge-lumineuse-01` (cadrages v2), voile anthracite. Texte sur les colonnes 1 à 7 de la grille. Séquence d'entrée orchestrée, moins d'une seconde : photo 1,04 → 1 (1,2 s), titre qui monte de 24 px, puis sous-titre (+100 ms), boutons (+200 ms), badges en cascade (+60 ms chacun). **Ne jamais partir d'une opacité 0 sur le titre** : on anime `transform` seulement, pour ne pas retarder le LCP. Mouvement réduit : rien.
- **Titre (H1, variante A, contrôle)** : « Placo, peinture, acoustique : la rigueur des chantiers publics » (8 mots)
- **Sous-titre** : « Régies, architectes, communes ou particuliers : nous venons voir, puis remettons une **offre écrite** détaillée. » (14 mots) `[À CONFIRMER C06 : « détaillée »]` Repli : sans « détaillée ».
- **Bouton 1** (rouge) : « Demander un devis » → `#demande`
- **Bouton 2** (contour clair) : « Appeler le +41 22 771 20 15 »
- **Barre de badges** (3 emplacements, détail au §4) : « Registre du commerce » / « Depuis 2007, IDE vérifiable » (lien Zefix) · « Siège à Carouge » / « Toute la Suisse romande » · 3e emplacement : premier badge confirmé dans l'ordre `C02` → `C11` → `C12`, sinon masqué. Ordinateur : une ligne sous les boutons. Mobile : grille de 2 colonnes.
- Supprimés : surtitre « Carouge · depuis 2007 », ligne « Du lundi au vendredi… » (les horaires passent sur la page contact, le pied de page et le bloc de demande).

**Trois variantes de titre testables** (8 mots au plus, sans tiret long, sans formule creuse) :

| Variante | Titre | Angle et levier | Condition |
|---|---|---|---|
| **A (contrôle)** | « Placo, peinture, acoustique : la rigueur des chantiers publics » | Autorité. Passe le test de substitution : seule une entreprise qui a travaillé pour des collectivités peut l'écrire. Le mur juste dessous le prouve. | Aucune (positionnement validé dans `product-marketing.md`) |
| **B** | « Du Conservatoire à votre salon : placo, acoustique, peinture » | Similarité. Désamorce « trop gros pour moi » en reliant la grande référence au logement du visiteur. Concret : on voit les deux lieux. | Nom en texte, même règle que le bandeau v2 (repli de `C22`). Le nom complet figure dans le mur juste dessous. |
| **C** | « Un seul interlocuteur, de l'ossature à la peinture » | Simplicité, réduction de l'effort. Le plus faible au test de substitution. | **Seulement si `C05` est confirmé.** En réserve. |

#### H2 · Mur de références (preuve 1)

- **Nature** : bande pleine largeur, fond neutre chaud, directement sous le héro. Rangée 1 : 4 noms statiques, grands (têtes d'affiche publiques). Rangée 2 : défilement continu lent (30 à 40 px/s), mis en pause au survol et au focus, avec un bouton visible « Mettre en pause » / « Reprendre » (`aria-pressed`, cible de 44 px ; WCAG 2.2.2). Le double de la liste qui sert à la boucle porte `aria-hidden="true"`. Mouvement réduit : rangée 2 en grille statique.
- **Titre (H2)** : « Ils nous ont confié des travaux »
- **Rangée 1** : Ville de Genève · Conservatoire de musique de Genève · HEAD – Genève · Salle de l'Alhambra
- **Rangée 2**, dans cet ordre (public et privé alternés, pour que la boucle montre toujours un mélange) : Salle communale de Plan-les-Ouates · UBS · Piaget · Salle communale de Collonge-Bellerive · J. Safra Sarasin · Labcorp · Energestion · Celgene · Everness Hotel & Resort `[À CONFIRMER C22 : même hôtel que l'« Hôtel Chavannes-de-Bogis »]` (Repli : « Hôtel à Chavannes-de-Bogis ») · Dipan · Harmonie Nautique de Genève · Domaine des Perrières · de Grisogono. OMC : preview seulement, en fin de rangée (D4).
- **Sous le mur** : « Et des **particuliers**, à Genève et dans toute la région. » `[À CONFIRMER C04]` Définitif : « Et des **particuliers**, pour une cloison, un plafond ou une pièce à repeindre. » · lien « Voir les {{n}} références » → `professionnels.html#references`
- `{{n}}` = nombre de noms publiables dans le mode de génération (17 en production tant que l'accord écrit de l'OMC manque, 18 ensuite). Jamais écrit en dur.
- Harmonisation : `nom_affiche` « Mairie de Plan-les-Ouates » devient « Salle communale de Plan-les-Ouates », comme son `nom_complet` et la référence de Collonge-Bellerive (à valider avec `C22`).

#### H3 · Chiffres clés (preuve 2)

- **Nature** : 4 compteurs sur une ligne (2 × 2 sur mobile), sous un filet fin, sur le même fond que le mur. Chiffres en très grand corps, libellé dessous. Animation de 0 à la valeur **une fois**, à l'entrée dans l'écran (800 ms). La valeur finale est écrite dans le HTML (sans JavaScript, on voit « 19 », jamais « 0 »).

| Chiffre | Libellé | Source et règle | Statut |
|---|---|---|---|
| « 19 » | « ans d'activité » | Calculé au build : années révolues depuis le 1.6.2007 (20 à partir de juin 2027) | Vérifié (registre) |
| « 18 » | « références, publiques et privées » | `{{n}}` du mur (17 en production sans l'OMC) | Vérifié |
| « 4 » | « métiers intérieurs » | Les 4 services | Vérifié |
| « 7 » | « cantons et régions romands » | Zone déclarée (GE, VD, NE, FR, Valais romand, JU, Jura bernois). C'est une zone, pas une preuve : ne jamais écrire « chantiers dans 7 cantons ». | Vérifié (zone) ; `C21` peut la restreindre pour les particuliers |
| `{{n}}` | « chantiers depuis 2007 » | `[À CONFIRMER C27]` | Remplace « 4 métiers » dès confirmation |
| « 1 » | « jour ouvrable, au plus, pour vous rappeler » | `[À CONFIRMER C01]` | Remplace « 7 » dès confirmation |
| `{{n}}` | « personnes sur nos chantiers » | `[À CONFIRMER C24]` | En réserve |

#### H4 · Prestations

- **Nature** : titre et 4 cartes illustrées (image 4:3, carte entièrement cliquable, texte du lien masqué visuellement : « Voir le placo »…). Révélation douce en cascade. 2 × 2 sur ordinateur, empilées sur mobile. **Plus de bouton dans cette section** : le bouton suivant est sous les projets ; l'en-tête compact et la barre mobile restent disponibles.
- **H2** : « Quatre métiers, souvent sur le même chantier »

| Carte | Texte | Gras | Image |
|---|---|---|---|
| **Placo** | « Cloisons, doublages et **faux-plafonds** en plaques de plâtre. » | faux-plafonds | `faux-plafond-placo-gorge-lumineuse-02` (réelle) |
| **Peinture** | « Murs et plafonds intérieurs, **préparés puis peints**. » | préparés puis peints | Image d'illustration sous licence, étiquette visible « Illustration », jusqu'au shooting peinture (`C40`) |
| **Isolation acoustique** | « Vous entendez vos voisins ? Nous **isolons murs et plafonds**. » | isolons murs et plafonds | `panneaux-acoustiques-muraux-01` (réelle, `C18`) ; repli : illustration étiquetée |
| **Cloisons isolantes** `[C16]` | « Entre une **pièce chauffée** et une cave, un garage ou des combles. » | pièce chauffée | AA3 « après » (réelle) `[À VÉRIFIER : qualité]` ; repli : `chantier-ossature-puits-de-lumiere-02` |

Règle des illustrations : jamais présentées comme une réalisation d'Andy Construct, étiquette « Illustration » sur l'image, texte alternatif descriptif sans « nos travaux ».

#### H5 · Projets de référence (preuve 3)

- **Nature** : 4 cartes « lieu » en format portrait (3:4), puis une carte large avant / après. Une carte « lieu » sans photo rattachée au lieu est **typographique** : fond profond, nom du lieu en grand corps demi-gras, ligne de type en petites capitales, filet rouge Andy de 24 px (le rouge en ponctuation), commune en bas. Survol : légère élévation (`transform`) et flèche. Révélation en cascade.
- **H2** : « Projets de référence »

| Carte | Titre | Ligne de type | Photo | Ligne de travaux |
|---|---|---|---|---|
| 1 | « Conservatoire de musique de Genève » | « Genève · École de musique » | Typographique. Photo seulement si `C25` rattache P6 ou P7 à ce lieu | « Travaux : {{nature}}, {{année}} » `[À CONFIRMER C22]` Repli : masquée |
| 2 | « Salle de l'Alhambra » | « Genève · Salle de spectacle » | `[À CONFIRMER C25 : la salle à balcons de P8 (`chantier-salle-de-spectacle-01`) est-elle l'Alhambra ? Quelle prestation ?]` Repli : typographique | Idem |
| 3 | « Salle communale de Plan-les-Ouates » | « Plan-les-Ouates · Collectivité » | `[À CONFIRMER C25 : la « salle publique » de P2 est-elle cette salle ?]` Repli : typographique | Idem |
| 4 | « HEAD – Genève » | « Genève · Haute école d'art et de design » | Typographique | Idem |
| Large | « Séjour : faux-plafond et spots » | « Appartement · avant, après » | Paire AA6 (réelle) `[À VÉRIFIER : qualité]` ; repli : AA5 | Étiquettes « Placo · Peinture » `[C26]` Repli : « Placo » |

Pas de photo d'illustration d'un bâtiment tiers au lancement : une façade photographiée suggérerait des travaux extérieurs et un soutien de l'institution. Possible plus tard, avec l'accord écrit du lieu (`C22`), une légende « Le bâtiment · photo : {{auteur}}, {{licence}} » et la mention « Nos travaux : l'intérieur ».

- **Sous les cartes** : bouton « Un projet semblable ? Demander un devis » · lien « Voir toutes les réalisations » · lien « Professionnels : dossier de références (PDF, 615 Ko) » (`data-suivi="telechargement"`).
- Preuve adjacente à ce bouton : les cartes elles-mêmes.

#### H6 · Méthode

- **Nature** : deux colonnes. Photo réelle `habillage-placo-niches-arrondies-01` (escalier protégé pendant les travaux) à gauche ; 4 étapes numérotées à droite, chiffres en grand. Sur mobile, la photo passe au-dessus.
- **H2** : « Un chantier en quatre étapes »

| N° | Étape | Texte | Marqueur |
|---|---|---|---|
| 1 | « Visite » | « Mesures et écoute, sur place. » | — |
| 2 | « Offre écrite » | « Poste par poste, **en CHF**. » | `[À CONFIRMER C06]` Repli : « Remise après la visite. » |
| 3 | « Chantier protégé » | « Sols et meubles couverts, **nettoyage chaque soir**. » | `[À CONFIRMER C07]` Repli : « Lieux protégés pendant les travaux. » |
| 4 | « Réception » | « Le tour des finitions, **ensemble**. » | — |

- **Engagement** (encadré, sous les étapes) : « **Aucun supplément** sans votre accord écrit et chiffré. » `[À CONFIRMER C06]` Repli : masqué. C'est la seule garantie de l'offre (type « engagement de service » du skill offers) : aucune garantie de remboursement, aucune rareté, aucune urgence.
- Lien : « Notre méthode en détail » → `entreprise.html#methode`

#### H7 · Avis et témoignages (preuve 4, masquée tant qu'elle est vide)

- **Avis Google** (`tools/build/donnees/avis.json`, affiché dès `nombre` ≥ 5, `C37`) : « **{{note}} sur 5** · {{nombre}} avis Google · relevé le {{date_releve}} » + lien « Lire les avis sur Google ». Texte statique, aucun widget, aucune note dans le JSON-LD. Dès qu'il s'affiche, il prend aussi le 3e emplacement de badge du héro (§4).
- **Témoignages** (`temoignages.json`, `C44`) : H2 « Ce qu'en disent nos clients », 1 à 3 citations au format v2 (§A.11) : « {{texte exact}} » · {{nom ou fonction}}, {{organisation}}, {{commune}} · {{travaux}}, {{année}}. Note : « Témoignages publiés tels quels, avec l'accord écrit de leurs auteurs. » Le générateur refuse une citation sans `accord_date`.
- Le premier témoignage est aussi repris, court, dans la colonne du bloc de demande (H9).
- Aucun titre orphelin, aucun « bientôt » tant que les fichiers sont vides.

#### H8 · Questions fréquentes (6 au lieu de 8, hors comptage)

H2 « Questions fréquentes » · « Une autre question ? Appelez le +41 22 771 20 15. »
Réponses v2 reprises, 35 mots au plus, mêmes marqueurs : (1) petits travaux `C04` ; (2) prix `C06` ; (3) visite payante `C02` ; (4) délai de rappel et de visite `C01`, `C41` ; (5) hors de Genève `C21`, `C22` ; (6) défaut après les travaux `C32`, `V01`. Retirées : « protection du logement » (dite dans la méthode) et « régies, architectes, communes » (dite par les projets). Le JSON-LD `FAQPage` suit le texte visible mot pour mot.

#### H9 · Demande (preuve 5)

- **Nature** : rappel de références au-dessus du bloc, puis formulaire à gauche (environ 60 %), colonne étroite à droite. Transitions entre étapes : fondu et glissement de 12 px (200 ms), focus sur la légende de l'étape.
- **Rappel de références** (une ligne, petit corps, mêmes règles typographiques que le mur) : « Ils nous ont confié des travaux » · Ville de Genève · Conservatoire de musique de Genève · HEAD – Genève · Salle de l'Alhambra · « et {{n−4}} autres »
- **H2** : « Demander un devis »
- **Introduction** : « **3 étapes**, environ **une minute**. »
- **Étape 1** : libellés v2 inchangés (§7).
- **Sous le bouton « Continuer : votre projet »** : « La visite et le devis sont gratuits et sans engagement. » `[À CONFIRMER C02]` Repli : « Vous décidez une fois l'offre écrite reçue. »
- **Lien** : « Vous préférez qu'on vous rappelle ? » (ouvre le module de rappel, replié par défaut ; textes v2 §A.7).
- **Colonne** : « Ou appelez le +41 22 771 20 15 » (grand corps) · « Lun-ven, 7 h – 18 h » `[À CONFIRMER C03]` Repli : masqué · 3 badges compacts : « Registre du commerce », « Siège à Carouge », « Offre écrite après visite » · premier témoignage s'il existe.
- Supprimés : surtitre « Votre demande », phrase « Nous vous rappelons pour convenir d'une visite » (devenue la réassurance de l'étape 3), colonne « Par téléphone » à deux numéros (le mobile reste sur la page contact et dans le pied de page), ligne de références de la colonne (remplacée par le rappel au-dessus du bloc).

#### H10 · Pied de page (preuve 6)

- Colonnes v2 (marque, « Nous joindre » avec le bloc NAP, prestations, liens Andy Construct avec « Contact » et le PDF).
- **Badges** (une ligne, blanc à 80 %) : « Registre du commerce » · « Depuis 2007 » · « Siège à Carouge » · « Membre du GGE » `[C11]` Repli : masqué.
- **Ligne de références** en noms typographiques, liste canonique moyenne (§2.3), sans logo.
- Barre basse v2 inchangée (© année du build, raison sociale, IDE, « Vérifier au registre du commerce », mentions, protection des données).

### 2.3 Mur de références : mélanger logos et noms proprement

**Constat.** 0 référence `autorise`, 12 `a_autoriser`, 5 `protege`, 1 `introuvable`. En production, tout est donc rendu en nom. La v2 mêlait, en preview, des logos de hauteurs et de styles différents avec des noms : c'est ce que le client a vu (« mélangés, petits, sans hiérarchie »).

**Règles.**
1. **Une rangée = un seul traitement.** Jamais un logo à côté d'un nom dans la même rangée.
2. **Rangée 1 (institutions publiques) : toujours typographique**, même si le Conservatoire ou la HEAD autorisent leur logo : elle reste homogène avec la Ville de Genève et l'Alhambra, protégées par la loi (LPAP).
3. **Rangée 2 : tout en logos dès que 6 références au moins sont `autorise`**, sinon tout en noms. En preview, même règle (le client voit ce qui sera publié).
4. **Cellule identique** pour tous : 220 × 96 px sur ordinateur, 160 × 72 px sur mobile, contenu centré, même couleur (graphite `#44494F` à 72 % sur fond clair ; blanc à 80 % sur fond sombre), opacité à 100 % au survol, aucune couleur de marque.
5. **Typographie des noms** : une seule famille (le caractère de titrage du site), jamais celle de la marque citée. Nom propre en demi-gras ; mots génériques placés au-dessus, en maigre et plus petits : « Ville de » / **Genève** ; « Salle communale de » / **Collonge-Bellerive** ; « Salle de » / **l'Alhambra**. Noms longs sans générique sur deux lignes équilibrées, coupures définies dans les données (« Conservatoire de musique » / « de Genève ») et `text-wrap: balance`. Deux lignes au plus. Traits d'union insécables (Plan-les-Ouates, Collonge-Bellerive).
6. **Équilibre optique** : la hauteur de capitale des noms est réglée sur celle des lettres des logos (environ 22 px en rangée 2, 30 px en rangée 1) ; les logos suivent `--logo-h × echelle` de `logos.json`.
7. Aucun emblème, aucune armoirie, aucune croix suisse, aucun lien vers les sites des références. Texte alternatif des logos = `nom_affiche`.
8. **Trois listes canoniques**, toujours dans le même ordre :
   - **courte** (près des boutons) : Ville de Genève · Conservatoire de musique de Genève · HEAD – Genève · Salle de l'Alhambra · « et {{n−4}} autres » ;
   - **moyenne** (pied de page, contact, pages services sans `C23`) : la courte, puis Salle communale de Plan-les-Ouates · Salle communale de Collonge-Bellerive · « et des particuliers de toute la région » ;
   - **complète** (mur, professionnels) : ordre du §2.2 H2.

Données à ajouter à `logos.json` (aucune modification ici) : `rang` (1 ou 2), `nom_lignes` (tableau de 1 ou 2 lignes), `generique` (texte maigre éventuel).

### 2.4 Comptage des mots visibles

Même méthode que l'annexe du copy deck v2 : sections H1 à H9, formulaire à l'étape 1, hors questions et réponses de la FAQ, hors en-tête et pied de page.

| Section | Mots | dont noms de références |
|---|---|---|
| H1 Héro (avec 4 badges) | 59 | — |
| H2 Mur (titre, pied, noms) | 62 | 42 |
| H3 Chiffres | 16 | — |
| H4 Prestations | 49 | — |
| H5 Projets de référence | 58 | 14 |
| H6 Méthode | 45 | — |
| H9 Demande (rappel, étape 1, colonne) | 115 | — |
| **Total** | **404** (v2 : 625) | **56** |

Texte courant hors noms : 348 mots. Avec les replis actuels (2 badges masqués, « détaillée » et engagement retirés), le total descend à environ 382.

**Mots en gras, récapitulatif** : offre écrite · particuliers · faux-plafonds · préparés puis peints · isolons murs et plafonds · pièce chauffée · en CHF · nettoyage chaque soir · ensemble · Aucun supplément · 3 étapes · une minute.

**Position du formulaire** : vers l'écran 9 ou 10 sur mobile (390 × 844), à cause des images. La barre fixe donne accès à la demande en un geste à tout moment.

---

## 3. En-tête v3

### 3.1 Contenu exact

| Zone | Ordinateur (≥ 1240 px) | Remarque |
|---|---|---|
| Gauche | Logo, 44 px de haut ; version blanche sur le héro, version anthracite une fois compact. Texte alternatif : « Andy Construct, page d'accueil » | Logo intact (charte) |
| Centre | « Prestations » (bouton, panneau au clic) · « Réalisations » · « Professionnels » · « L'entreprise » | 4 entrées |
| Panneau Prestations | « Placo » · « Cloisons, doublages, faux-plafonds » / « Peinture » · « Murs et plafonds, à l'intérieur » / « Isolation acoustique » · « Contre le bruit et l'écho » / « Cloisons isolantes » · « Caves, garages, combles » `[C16]` | `<details>` v2 conservé ; ouverture en fondu de 150 ms |
| Droite | Icône téléphone + « +41 22 771 20 15 » (lien `tel:`, `emplacement=entete`) · bouton rouge « Demander un devis » | Le seul élément rouge de l'en-tête |

**Retirés** : le libellé d'horaires « Lun-ven, 7 h – 18 h » (page contact, pied de page, bloc de demande) ; l'entrée « Contact » (pied de page, menu mobile ; l'action passe par le bouton et le téléphone) ; les boutons dupliqués `nav-extra` sur ordinateur ; le surtitre et la barre de validation en production (inchangé).

**Alignement** : une seule ligne, tous les éléments centrés verticalement sur le même axe ; logo sur les colonnes 1-2, menu centré sur les colonnes 4-9, téléphone et bouton alignés sur le bord droit de la grille (colonnes 10-12). Hauteur 88 px au repos.

### 3.2 Défilement (compact)

- Au-delà de 24 px de défilement : hauteur 64 px, fond blanc opaque, filet de 1 px, logo réduit à 32 px par `transform: scale()` (pas de changement de hauteur du logo, donc pas de recalcul de mise en page), passage du logo blanc au logo anthracite en fondu.
- Transition de 200 ms ; en mouvement réduit, changement immédiat.
- L'en-tête reste visible (pas de masquage au défilement vers le bas) : le bouton doit rester à portée.
- Pas de flou d'arrière-plan (`backdrop-filter`) : coûteux sur mobile.
- Le contenu ne bouge pas : l'espace de l'en-tête est réservé dès le chargement (CLS nul).

### 3.3 Mobile et tablette

- **< 900 px** : logo (32 px) à gauche, bouton « Menu » (icône et mot, 48 px) à droite. Pas de téléphone dans l'en-tête : la barre fixe du bas porte « Appeler » et « Demander un devis ». En-tête 56 px + barre 64 px = 14 % d'un écran de 844 px.
- **Menu ouvert** : plein écran, ouverture en fondu et glissement (200 ms), focus piégé, Échap ferme. Contenu : « Prestations » (les 4 services) · « Réalisations » · « Professionnels » · « L'entreprise » · « Contact » ; en bas : « Appeler le +41 22 771 20 15 », « Demander un devis », puis 2 badges (« Registre du commerce », « Siège à Carouge »).
- **900 à 1239 px** : logo, icône téléphone seule (avec `aria-label` « Appeler le +41 22 771 20 15 »), bouton « Demander un devis », bouton « Menu ».

### 3.4 Barre supérieure « Ils nous ont confié des travaux : … » : **non**

1. Le client trouve l'en-tête déjà trop chargé ; une troisième bande horizontale (barre, en-tête, barre mobile) va dans le sens inverse.
2. Elle répéterait le mur, visible un écran plus bas : deux listes identiques dans le même écran.
3. En 12 à 13 px, elle se lit comme des petits caractères ; un public premium y voit un procédé publicitaire.
4. Elle repousse le héro et sa photo, l'élément qui doit produire le « c'est beau » des 5 premières secondes.

Si le client insiste : ordinateur seulement, 32 px de haut, statique, liste courte, derrière un drapeau `barre_refs` pour en mesurer l'effet (§5).

---

## 4. Badges de confiance (« flags »)

Rendu selon `confirmations.json` : un badge `[Cxx]` non confirmé passe à son repli ou disparaît. Icônes au trait (20 px, trait de 1,5 px, monochromes), sans émoji. Un badge cliquable ne l'est que vers une source vérifiable.

| # | Titre (≤ 4 mots) | Sous-texte (≤ 6 mots) | Icône | Statut | Lien |
|---|---|---|---|---|---|
| B1 | « Registre du commerce » | « Depuis 2007, IDE vérifiable » | Document avec sceau | Vérifié | Zefix (IDE CHE-113.706.162) |
| B2 | « Depuis 2007 » | « {{19}} ans d'activité » (calculé) | Calendrier | Vérifié | — |
| B3 | « Siège à Carouge » | « Toute la Suisse romande » | Repère de carte | Vérifié (`C21` peut nuancer la zone des particuliers) | `contact.html#zone` |
| B4 | « Offre écrite » | « Après visite sur place » | Document à lignes | Vérifié (texte de repli de `C06`) | — |
| B5 | « {{18}} références » | « Dont la Ville de Genève » | Façade à colonnes | Vérifié (nombre calculé, §2.2 H2) | `professionnels.html#references` |
| B6 | « Visite et devis gratuits » | « Sans engagement » | Presse-papiers coché | À confirmer `C02` | — |
| B7 | « Membre du GGE » | « Entreprises genevoises du bâtiment » | Bouclier simple | À confirmer `C11` | Fiche gge.ch (si confirmée) |
| B8 | « Assurance responsabilité civile » | « Attestation sur demande » | Bouclier coché | À confirmer `C12` | — |
| B9 | « Rappel le jour même » | « Ou le jour ouvrable suivant » | Combiné et horloge | À confirmer `C01` | — |
| B10 | « Attestations à jour » | « AVS, LPP, impôts, sur demande » | Dossier | À confirmer `C13` | `mailto:` objet « Demande d'attestations » |
| B11 | « Un seul interlocuteur » | « De la pose à la peinture » | Silhouette | À confirmer `C05` | — |
| B12 | « Jamais de liquide d'avance » | « Paiement sur facture » | Facture | À confirmer `C28` | — |
| B13 | « {{note}} sur 5 » | « {{n}} avis Google » | Étoile | Dès 5 avis réels (`C37`, `avis.json`) | Fiche Google |

### 4.1 Où les afficher

| Emplacement | Badges, par ordre de priorité | Au lancement (rien de confirmé) |
|---|---|---|
| Héro (3 au plus) | B1, B3, puis 1 parmi B13 → B6 → B7 → B8 | B1, B3 |
| Bloc de demande, colonne (3) | B1, B3, B4 ; B9 remplace B4 si `C01` | B1, B3, B4 |
| Pages services, sous le H1 (3) | B11 si `C05`, sinon B4 ; B6 si `C02`, sinon B3 ; B1 | B4, B3, B1 |
| Professionnels, sous le H1 (4) | B1, B8, B10, B5 | B1, B5 |
| L'entreprise, « Vérifiez qui nous sommes » | Tous les badges vérifiés ou confirmés, sauf B13 | B1, B2, B3, B4, B5 |
| Contact, à côté du formulaire (3) | B1, B3, B9 (sinon B4) | B1, B3, B4 |
| Pied de page (une ligne) | B1, B2, B3, B7 | B1, B2, B3 |
| Menu mobile | B1, B3 | B1, B3 |

Règle : jamais deux badges qui disent la même chose sur un même écran (B2 et le chiffre « 19 ans » ne cohabitent pas : B2 ne sert qu'en pied de page et sur la page entreprise).

---

## 5. Drapeaux d'A/B test

### 5.1 Ce que le trafic permet (skill ab-testing)

**Hypothèse de trafic H, à remplacer après le rodage** (aucune mesure n'existe ; ordre de grandeur tiré de l'objectif de 30 demandes par mois de `strategie-acquisition.md`) : accueil ≈ 800 visiteurs uniques par mois (27 par jour) ; site ≈ 1'800 (60 par jour) ; bloc de demande vu ≈ 550 par mois (18 par jour) ; étape 3 atteinte ≈ 45 par mois.

Calcul : α = 5 % (bilatéral), puissance 80 %, effet minimal détectable (MDE) relatif, deux bras à 50/50.

| Mesure | Taux de base supposé | MDE | Par variante | Durée sous H |
|---|---|---|---|---|
| `intention_contact` / visiteur exposé (accueil) | 12 % | +50 % | 555 | 41 jours ≈ 6 semaines |
| idem | 12 % | +40 % | 839 | 62 jours ≈ 9 semaines |
| `devis_clic` / visiteur exposé (site entier) | 6 % | +50 % | 1'209 | 40 jours ≈ 6 semaines |
| `formulaire_debut` / visiteur qui voit le bloc | 12 % | +50 % | 555 | 62 jours ≈ 9 semaines (α = 10 % : 437, 7 semaines) |
| `formulaire_envoye` / étape 3 atteinte | 55 % | +25 % | 195 | 260 jours : **non testable** |

Conséquences :
- On ne détecte que des **effets importants**. Une variante qui « gagne » de 10 % passera pour un résultat non concluant : c'est normal, il faut le dire dans le bilan.
- **Horizon fixe** décidé avant le lancement ; au moins 2 semaines complètes ; 8 semaines au plus. Pas d'arrêt anticipé sur un résultat favorable ; arrêt immédiat seulement si un garde-fou est franchi.
- **Une expérience à la fois par page** et par indicateur. Deux expériences peuvent tourner ensemble seulement si leurs zones et leurs indicateurs diffèrent (tirages indépendants).
- À l'horizon sans échantillon suffisant : « non concluant », on garde A (ou la version la plus simple) et on publie l'intervalle de l'effet.
- Contrôle de répartition (SRM) chaque semaine : khi-deux sur les expositions A / B ; p < 0,01 = panne de répartition, on arrête et on corrige.
- Éthique : les deux variantes sont honnêtes et n'utilisent aucune affirmation non confirmée.

### 5.2 Expériences prioritaires

Score ICE (impact, confiance, facilité, de 1 à 10) :

| Drapeau | Expérience | I | C | F | ICE | Faisable sous H |
|---|---|---|---|---|---|---|
| `heros_titre` | XP1 · titre du héro | 8 | 6 | 9 | 7,7 | Oui, 6 semaines |
| `entree_demande` | XP4 · rappel express à côté du formulaire | 7 | 6 | 6 | 6,3 | Oui, 8-9 semaines |
| `libelle_cta` | XP3 · « devis » ou « visite » | 6 | 5 | 8 | 6,3 | Oui, 6 semaines |
| `ordre_sections` | XP2 · projets avant prestations | 6 | 5 | 7 | 6,0 | Oui, 6 semaines |
| `etape3_allegee` | XP5 · étape 3 allégée | 6 | 6 | 7 | 6,3 | **Non** : lancement surveillé |

#### XP1 · `heros_titre` (accueil)

- **Hypothèse** : parce que le titre v2 décrit une catégorie et que les grandes références intimident une partie des particuliers (« trop gros pour moi », `personas-psychologie.md` §1.4), nous pensons qu'un titre qui relie la grande référence au logement du visiteur augmentera les intentions de contact des visiteurs de l'accueil. Nous le saurons quand `intention_contact` par visiteur exposé sera plus élevé en B.
- **A** : « Placo, peinture, acoustique : la rigueur des chantiers publics »
- **B** : « Du Conservatoire à votre salon : placo, acoustique, peinture »
- Sous-titre, badges et boutons identiques.
- **Indicateur principal** : `intention_contact` / `exposition_variante` (unité : visiteur).
- **Secondaires** : `devis_clic` avec `emplacement=heros` ; part des `formulaire_envoye` avec `type_client` professionnel.
- **Garde-fous** : `formulaire_envoye` par visiteur exposé (pas de baisse) ; part des demandes professionnelles (pas de baisse de plus de 30 % relatifs) ; LCP mobile inchangé.
- **Exposition** : au chargement de l'accueil.
- **Durée** : 6 semaines (555 par variante, MDE +50 %).

#### XP2 · `ordre_sections` (accueil)

- **Hypothèse** : parce que les professionnels (régies, architectes, communes) cherchent d'abord des références comparables, nous pensons que placer les projets de référence avant les prestations augmentera les intentions de contact, sans gêner les particuliers. Nous le saurons quand `intention_contact` sera plus élevé en B sans baisse des clics vers les pages services.
- **A** : héro · mur · chiffres · **prestations · projets** · méthode…
- **B** : héro · mur · chiffres · **projets · prestations** · méthode…
- Textes identiques.
- **Indicateur principal** : `intention_contact` / visiteur exposé.
- **Garde-fous** : clics sur les cartes prestations (`devis_clic` exclu ; suivre les visites des pages services depuis l'accueil) ; `formulaire_envoye`.
- **Exposition** : au chargement de l'accueil. **Durée** : 6 semaines.

#### XP3 · `libelle_cta` (site entier)

- **Hypothèse** : parce que la prochaine étape réelle est une visite, et qu'un public de 30 à 60 ans plus aisé associe « devis » à une mise en concurrence sur le prix, nous pensons que « Demander une visite » augmentera les clics sur le bouton principal sans faire baisser les demandes envoyées. Nous le saurons quand `devis_clic` par visiteur exposé sera plus élevé en B, avec un `formulaire_envoye` stable.
- **A** : « Demander un devis » partout (en-tête, héro, barre mobile, boutons de section, H2 du bloc de demande) ; pages services : « Demander un devis pour du placo »…
- **B** : « Demander une visite » partout, H2 du bloc « Demander une visite » ; pages services : « Demander une visite pour du placo »… Formulaire, page merci et réassurance identiques.
- Le libellé est cohérent sur tout le parcours d'un même visiteur (un seul libellé, règle v2).
- **Indicateur principal** : `devis_clic` / visiteur exposé.
- **Garde-fous** : `formulaire_envoye` / visiteur exposé ; part de `type_client` = particulier.
- **Plus tard** : variante C « Demander un devis gratuit », seulement si `C02` est confirmé.
- **Durée** : 6 semaines.

#### XP4 · `entree_demande` (bloc de demande, toutes les pages qui l'ont)

- **Hypothèse** : parce que le téléphone reste le canal préféré des régies et des particuliers, nous pensons qu'un rappel express visible à côté du formulaire augmentera le nombre de demandes commencées. Nous le saurons quand `formulaire_debut` (devis ou rappel) par visiteur qui voit le bloc sera plus élevé en B, sans baisse des devis envoyés.
- **A** : formulaire en 3 étapes ; module de rappel replié derrière le lien « Vous préférez qu'on vous rappelle ? ».
- **B** : au-dessus de l'étape 1 (mobile) ou dans la colonne (ordinateur), une carte ouverte : titre « Plutôt un appel ? » · « Laissez votre numéro, nous vous rappelons. » · champ « Votre numéro de téléphone » · bouton « Être rappelé(e) » · « Votre numéro ne sert qu'à ce rappel. » ; puis, au-dessus du formulaire : « Ou décrivez vos travaux en 3 étapes ».
- API inchangée (`formulaire=rappel`).
- **Indicateur principal** : `formulaire_debut` (tous formulaires) / visiteur exposé.
- **Secondaires** : `formulaire_envoye` par type (devis, rappel).
- **Garde-fous** : devis envoyés (pas de cannibalisation de plus de 30 %) ; joignabilité des rappels (suivi des prospects, hors Umami).
- **Exposition** : bloc `#demande` visible à 50 % pendant une seconde.
- **Durée** : 8 à 9 semaines (ou 7 semaines à α = 10 %, à écrire dans le bilan). Peut tourner en même temps que XP1 (zone et indicateur différents, tirages indépendants).

#### XP5 · `etape3_allegee` (conditionnelle)

- **A** : étape 3 complète (§7).
- **B** : message, fichiers et « Comment nous avez-vous connus ? » regroupés sous « Ajouter un message, des photos ou des plans (facultatif) », replié.
- **Indicateur** : `formulaire_envoye` / `formulaire_etape` (étape 3). **Garde-fous** : part des envois avec message ou fichiers (propriétés booléennes, §5.4) ; score moyen des demandes (suivi des prospects).
- **Sous H : non testable** (390 visiteurs à l'étape 3, soit environ 9 mois). Le lancer en test seulement au-delà de 150 étapes 3 par mois (par exemple avec les annonces). Sinon, décision qualitative après 10 enregistrements de session ou entretiens ; comparaison avant / après étiquetée « indicative ».

**Réserve** (après ces cinq) : T6 v2 (« Appeler » contre « Appeler le 022 771 20 15 » dans la barre mobile), titre C si `C05`, barre `barre_refs` si le client l'exige.

### 5.3 Calendrier

| Semaines | Accueil | Formulaire et site |
|---|---|---|
| 1-2 | **Rodage** : drapeau témoin `aa_temoin` (A/A, aucun changement visible) ; vérification de la chaîne de mesure, SRM, taux de base réels ; recalcul des durées | — |
| 3-8 | XP1 `heros_titre` | XP4 `entree_demande` (3-11) |
| 9-14 | XP2 `ordre_sections` | — |
| 15-20 | XP3 `libelle_cta` (site entier : pas d'autre expérience en parallèle) | — |

Chaque expérience a une fiche (gabarit « Test Plan » du skill ab-testing) remplie **avant** le lancement, et un bilan (gabarit « Results ») avec l'intervalle de confiance de l'effet.

### 5.4 Spécification technique minimale

**Configuration** (`tools/build/donnees/config.json`, à ajouter à côté de `umami_src`) :

```json
"flags": {
  "actif": true,
  "_aide": "actif=false : aucun script ni style de drapeau, la variante a est rendue en dur partout.",
  "experiences": {
    "aa_temoin":      {"actif": true,  "version": 1, "repartition": {"a": 50, "b": 50}, "pages": ["*"],          "exposition": "chargement"},
    "heros_titre":    {"actif": false, "version": 1, "repartition": {"a": 50, "b": 50}, "pages": ["index.html"], "exposition": "chargement"},
    "ordre_sections": {"actif": false, "version": 1, "repartition": {"a": 50, "b": 50}, "pages": ["index.html"], "exposition": "chargement"},
    "libelle_cta":    {"actif": false, "version": 1, "repartition": {"a": 50, "b": 50}, "pages": ["*"],          "exposition": "chargement"},
    "entree_demande": {"actif": false, "version": 1, "repartition": {"a": 50, "b": 50}, "pages": ["*"],          "exposition": "#demande"}
  }
}
```

**Générateur.**
- `flags.actif = false` (désactivation globale) ou drapeau inactif : seule la variante `a` est écrite dans le HTML, sans attribut ni script. Reconstruire et déployer suffit (quelques minutes, site statique).
- Drapeaux actifs de la page : un bloc `<script id="ac-flags" type="application/json">` et le script d'attribution ci-dessous, **en ligne dans le `<head>`, avant la feuille de style** (moins de 1 Ko), puis un `<style>` en ligne avec les règles des variantes.
- Changer le texte d'une variante = incrémenter `version` (réattribution des visiteurs).

**Balisage `data-flag`.**
```html
<h1 id="titre-page">
  <span data-flag="heros_titre" data-variante="a">Placo, peinture, acoustique : la rigueur des chantiers publics</span>
  <span data-flag="heros_titre" data-variante="b">Du Conservatoire à votre salon : placo, acoustique, peinture</span>
</h1>
<section id="demande" data-flag-expo="entree_demande">…</section>
```
```css
[data-flag][data-variante]:not([data-variante="a"]){display:none}
html[data-f-heros_titre="b"] [data-flag="heros_titre"][data-variante="a"]{display:none}
html[data-f-heros_titre="b"] [data-flag="heros_titre"][data-variante="b"]{display:revert}
```
La variante est choisie avant le premier rendu : pas de clignotement, pas d'effet sur le LCP. Sans JavaScript, on voit A. La variante masquée (`display:none`) n'est lue ni par les lecteurs d'écran ni au clavier.

**Ordre des sections** (`ordre_sections`) : un court script en ligne placé juste après les deux sections déplace le nœud pendant l'analyse du HTML, avant le rendu ; l'ordre du DOM reste l'ordre visuel (pas de `order` CSS, qui casserait l'ordre de tabulation).
```html
<script>if(document.documentElement.getAttribute('data-f-ordre_sections')==='b'){var p=document.getElementById('projets');p.parentNode.insertBefore(p,document.getElementById('prestations'))}</script>
```

**Attribution (script de tête, référence).**
```html
<script>
(function(d,w){var h=d.documentElement,S='ac_flags',c,F={},f=null,ls=null,n=navigator;
try{c=JSON.parse(d.getElementById('ac-flags').textContent)}catch(e){return}
var dnt=n.doNotTrack=='1'||w.doNotTrack=='1'||!!n.globalPrivacyControl,
    q=new URLSearchParams(location.search).get('flag');
try{if(q=='reset'){sessionStorage.removeItem(S);localStorage.removeItem(S)}
 else if(q){f={};q.split(',').forEach(function(x){x=x.split(':');f[x[0]]=x[1]||'a'});sessionStorage.setItem(S,JSON.stringify(f))}
 else f=JSON.parse(sessionStorage.getItem(S)||'null')}catch(e){}
try{ls=JSON.parse(localStorage.getItem(S)||'{}')}catch(e){ls=null}
Object.keys(c).forEach(function(k){var x=c[k],v='a',s=0,t,m;
 if(f)v=f.off?'a':(f[k]||'a');
 else if(dnt||!ls)v='a';
 else if(ls[k]&&ls[k].ver===x.version)v=ls[k].v;
 else{t=crypto.getRandomValues(new Uint32Array(1))[0]/4294967296*100;
  for(m in x.repartition){s+=x.repartition[m];if(t<s){v=m;break}}ls[k]={v:v,ver:x.version}}
 F[k]=v;h.setAttribute('data-f-'+k,v)});
try{if(ls&&!f&&!dnt)localStorage.setItem(S,JSON.stringify(ls))}catch(e){}
w.acFlags=F;w.acFlagsMesure=!f&&!dnt&&!!ls})(document,window);
</script>
```
(`c` = les seules expériences actives de la page, écrites par le générateur.)

Règles :
- **Attribution stable** : tirage une seule fois par visiteur et par drapeau, gardé dans `localStorage` (`ac_flags` : variante et version, aucun identifiant).
- **Do Not Track ou GPC**, ou stockage indisponible (navigation privée) : variante `a`, rien n'est stocké, rien n'est mesuré.
- **Forçage** : `?flag=heros_titre:b` (plusieurs : `?flag=heros_titre:b,entree_demande:b`), `?flag=off` (tout en A), `?flag=reset` (efface le tirage). Le forçage vaut pour l'onglet (`sessionStorage`) et **coupe la mesure**. En mode `verification`, une pastille « Variante B (forcée) » s'affiche.

**Mesure (ajouts à `assets/js/suivi.js`, aucun cookie).**

| Événement ou propriété | Quand | Propriétés |
|---|---|---|
| `exposition_variante` | Une fois **par visiteur et par drapeau** (`localStorage` `ac_flags_vus`) : au chargement, ou quand l'élément `[data-flag-expo]` est visible à 50 % pendant une seconde (IntersectionObserver) | `xp` = « heros_titre:b » (lecture directe dans Umami), `flag`, `variante`, `version` |
| Propriétés `f_<drapeau>` | Ajoutées par `s()` aux événements `devis_clic`, `appel_clic`, `rappel_ouvert`, `formulaire_debut`, `formulaire_etape`, `formulaire_envoye`, `telechargement`, `intention_contact`, pour les seuls drapeaux **déjà exposés** à ce visiteur | `f_heros_titre: "b"`… |
| `intention_contact` (nouveau) | Au premier `devis_clic`, `appel_clic`, `rappel_ouvert` ou `formulaire_debut` qui suit une exposition ; une fois par visiteur **et par drapeau** (`localStorage` `ac_ic`), avec les seules propriétés `f_` des drapeaux pas encore comptés | `f_<drapeau>` |
| `formulaire_envoye` (complété) | Inchangé (réponse `ok` avec `ref`) | + `avec_message` (« oui » ou « non »), `avec_fichiers`, `nb_travaux` : booléens et compte, jamais de contenu |

- Rien n'est envoyé si `acFlagsMesure` est faux. Les propriétés `f_` passent par le filtre existant de `suivi.js` (aucune donnée saisie).
- **Analyse** : pour un drapeau X, `exposés(v)` = nombre d'`exposition_variante` avec `xp = X:v` ; `convertis(v)` = nombre d'`intention_contact` (ou de l'indicateur choisi) avec `f_X = v`. Les deux sont dédoublonnés par visiteur, donc des proportions. Test de deux proportions (exact de Fisher sous 10 conversions par bras), intervalle de confiance à 95 %, SRM. Lecture dans l'interface Umami (propriétés d'événements) ou par requête sur la base auto-hébergée.
- **Protection des données** : ajouter à `confidentialite.html` une phrase sur la mémorisation locale de la variante (aucune donnée personnelle, aucun identifiant, refus par Do Not Track ou GPC), au titre de l'art. 45c LTC. À faire relire avec `V02`.
- **Référencement** : même URL, aucune redirection, aucun traitement particulier des robots (pas de dissimulation) ; tests limités dans le temps.

**Recette** : chaque variante par `?flag=` ; sans JavaScript ; Do Not Track ; navigation privée de Safari ; lecteur d'écran (une seule variante lue) ; LCP et CLS mobiles inchangés ; une semaine d'`aa_temoin` sans SRM avant XP1.

---

## 6. Coupes sur les autres pages

### 6.1 Gabarit des 4 pages services

| Section v2 | Décision | v3 |
|---|---|---|
| En-tête de page (chapeau, « En bref ») | **Raccourcir** | Chapeau de 20 mots au plus ; les 3 puces « En bref » deviennent 3 badges (§4.1) ; photo réelle ou illustration étiquetée |
| Ce que nous posons (4 H3 de 40 à 70 mots) | **Raccourcir** | 4 cartes : titre, 20 mots au plus, image ; ancres conservées (`#cloisons`, `#doublages`, `#faux-plafonds`, `#caissons`, `#correction` : cibles des redirections 301) |
| Pour qui ? | **Supprimer** | Une ligne « Professionnels » sous les cartes (CFC et lien) |
| Ce qu'il faut savoir (5 ou 6 points) | **Raccourcir** | 3 points, 15 mots chacun ; le reste va dans la FAQ si la question n'y est pas déjà |
| Réalisations | **Remplacer** | « Références en {{service}} » : 1 mini-cas + ligne de références (règle `C23` ci-dessous) |
| Bloc spécifique (guide, subventions) | **Garder, raccourcir** | 2 phrases et le bouton |
| Comment se passe un chantier (4 lignes) | **Raccourcir** | Une ligne « Visite · Offre écrite · Chantier protégé · Réception » + lien « Notre méthode en détail » |
| FAQ (5 ou 6) | **Réduire** | 4 ou 5 questions |
| Demande | **Garder** | Rappel de références au-dessus, badges en colonne (§7) |

**Mini-cas** (format commun, une seule fiche par page, jamais de contenu inventé) : titre · « Lieu : … » · « Demande : … » `[C25]` (repli : ligne masquée) · « Ce que nous avons fait : … » (ce que montre la photo) · étiquettes de prestations · « Un projet semblable ? Demander un devis ».

**Ligne de références des pages services** : « Réalisé notamment pour : {{3 noms}} » **seulement si `C23` confirme** que ces maîtres d'ouvrage ont reçu ce service. Repli : liste canonique moyenne sous le titre générique « Ils nous ont confié des travaux ». En v2, le repli de la page acoustique (Conservatoire, HEAD, Alhambra) laissait croire à des travaux acoustiques chez eux : on le remplace par la liste canonique.

#### Placo (`placo.html`)

- **Chapeau** : « Diviser une pièce, redresser un mur, abaisser un plafond : les **plaques de plâtre** le font sans maçonnerie. »
- **Badges** : B4 (ou B11 « Un seul interlocuteur » si `C05`) · B3 · B1.
- **Cartes** :
  - « Cloisons » : « Une chambre, un bureau, une salle de réunion, montés en quelques jours. **Portes et renforts** prévus dès la pose. »
  - « Doublages » : « Un parement devant un mur abîmé, qui cache les gaines et peut recevoir un isolant contre le **froid** ou le **bruit**. » (liens conservés vers `cloisons-isothermes.html` et `isolation-acoustique.html`)
  - « Faux-plafonds » : « Il cache conduites et ventilation, reçoit **spots et gorges lumineuses**, et remplace un plafond abîmé. »
  - « Caissons et habillages » : « Une poutre ou une gaine à cacher : un **caisson** ajusté, avec trappe de visite si besoin. »
- **Ligne professionnels** : « Professionnels : lots **CFC 271 et 283**, offres sur plans et descriptifs. » `[À CONFIRMER C14 : CFC 283]` Repli : « lots **CFC 271** ». Lien « Espace professionnels ».
- **Ce qu'il faut savoir (3)** : poussière `C07` (texte v2) · coordination avec l'électricien · niveau de finition sur les grands murs. Retirés : salle de bains (déjà en FAQ 5), accord locataire ou PPE (déjà en FAQ 6).
- **Mini-cas** : P1 « Hall et couloirs : faux-plafond à gorge lumineuse » · « Lieu : Immeuble, canton de Genève » `[C25]` Repli : « Hall d'immeuble » · « Ce que nous avons fait : faux-plafond en plaques de plâtre aux formes courbes, éclairage et spots intégrés. » · Placo · Peinture `[C25]` Repli : Placo. Photo de chantier P3 en vignette.
- **FAQ (5)** : retirer « Peut-on fixer des meubles sur une cloison en placo ? » (dit dans la carte « Cloisons »).

#### Peinture (`peinture.html`)

- **Chapeau** : « Un appartement à rafraîchir, une fin de bail, une cage d'escalier : nous **préparons les supports**, protégeons les lieux, puis peignons. »
- **Cartes** (illustrations étiquetées jusqu'au shooting `C40`) :
  - « Logements » : « Une pièce ou tout l'appartement, habité ou vide. Trous et fissures rebouchés **avant** la peinture. » `[C17]`
  - « Fins de bail » : « Remise en état entre deux locataires, prête pour l'**état des lieux d'entrée**. » `[C17]`
  - « Cages d'escalier » : « Par étages, **passage libre** pour les habitants. » `[C20]` Repli : « Par étages, dans les parties communes. »
  - « Bureaux et commerces » : « **Le soir ou le week-end**, pour ne pas fermer. » `[À CONFIRMER C19]` Repli : « Zone par zone, pour limiter la gêne. »
- La carte « Après nos travaux de placo » devient le badge B11 (`C05`), sinon disparaît.
- **Ce qu'il faut savoir (3)** : préparation sur une ligne de l'offre `C06` · fissure qui revient si la cause n'est pas traitée · intérieur seulement, pas de façades.
- **Mini-cas** : AA6 avant / après si sa qualité le permet `[À VÉRIFIER]` ; sinon section masquée (règle v2).

#### Isolation acoustique (`isolation-acoustique.html`)

- **Garder** « Isoler ou corriger » (personne ne l'explique chez les concurrents), mais en deux colonnes :
  - « **Isoler** » : « Empêcher le bruit de passer d'un local à l'autre : voisin, étage, pièce d'à côté. »
  - « **Corriger** » : « Réduire l'écho dans la pièce : salle de réunion, réfectoire, salle communale. »
  - Sous les colonnes : « À la visite, nous commençons par identifier ce que vous entendez. »
- **Cartes (4)** : doublage acoustique `C18`, faux-plafond acoustique, cloison acoustique, correction des salles `C18` (textes v2 ramenés à 20 mots).
- **Ce qu'il faut savoir (3)** : bruits de pas traités à la source · le bruit passe aussi par les côtés · aucune promesse en décibels sans mesure `C15`.
- **Guide** : « Ce qui marche, ce qui ne marche pas, et les questions à poser à toute entreprise. 8 pages. » + bouton (texte v2).
- **Mini-cas** : P6 « Correction acoustique d'une salle » · « Ce que nous avons fait : panneaux muraux et plafond perforé contre l'écho. » `[C18, C25]`.
- **Références** : C23 proposé « Conservatoire de musique de Genève · HEAD – Genève · Salle communale de Collonge-Bellerive » ; repli : liste canonique moyenne (voir ci-dessus).

#### Cloisons isolantes (`cloisons-isothermes.html`)

- **Chapeau** : « Une chambre au-dessus du garage, un bureau contre une cave, des combles : la cloison isolante garde la chaleur **côté chauffé**. » + phrase de filtre « Nous ne posons pas de chambres froides. » `[C16]`
- **Pour qui ?** supprimé ; **Ce qu'il faut savoir (3)** : humidité vérifiée d'abord · pare-vapeur côté chauffé · protection incendie entre garage et logement `C15`.
- **Subventions** : « Certaines isolations thermiques peuvent être subventionnées. La demande se dépose **avant** les travaux, auprès du service de l'énergie de votre canton. » `[C43]` pour la phrase sur les informations fournies.
- **Mini-cas** : AA3 « Combles : isolation et rampant fini sous une fenêtre de toit » (avant / après) `[À VÉRIFIER : qualité]` `[C26]`.

### 6.2 Professionnels (`professionnels.html`)

| Section | Décision | Texte de remplacement |
|---|---|---|
| En-tête | **Raccourcir** | Chapeau : « Immeubles habités, bureaux et bâtiments publics, **depuis 2007**. Offres sur plans et descriptifs. » `[C20]` Repli : « Bureaux, logements et bâtiments publics, **depuis 2007**. Offres sur plans et descriptifs. » Badges : B1, B5 (+ B8 `C12`, B10 `C13`) |
| Références complètes (`#references`) | **Remonter** en section 2 | Grille par secteur en noms typographiques (règles §2.3), suivie de la bande de chiffres compacte. Ancre conservée (redirection 301 de `/realisations/references`) |
| Ce que nous vous apportons | **Raccourcir** (20 mots par carte) | Régies : « Remises en état, cages d'escalier, plafonds après dégât d'eau. **Parties communes protégées**, date convenue tenue. » `[C20]` Repli : sans « date convenue tenue ». · Architectes : « Lots **CFC 271, 283 et 285**. Offres complètes sur descriptif, variantes à part, questions posées avant de chiffrer. » `[C14]` · Communes : « La Ville de Genève, Plan-les-Ouates et Collonge-Bellerive nous ont confié des travaux. Interventions pendant les **vacances scolaires**. » `[C19]` Repli : sans la 2e phrase. · Entreprises : « Cloisons, salles de réunion plus calmes, peinture : **le soir ou le week-end**. » `[C19]` Repli : « zone par zone » |
| Méthode en site occupé (8 points) | **Raccourcir à 6** `[C20, C07, C06, C09, C32]` | 1 « Avis aux locataires et horaires convenus, affichés quelques jours avant. » · 2 « Parties communes, ascenseur et sols protégés dès le premier jour. » · 3 « Poussière contenue, nettoyage chaque soir, passages libres. » · 4 « Un responsable de chantier nommé, joignable. » · 5 « Un imprévu est chiffré avant d'être exécuté. » · 6 « Réception avec photos et liste des retouches. » |
| Nouveau : mini-cas public | **Ajouter** | Carte typographique « Salle communale de Plan-les-Ouates » · « Collectivité » · « Travaux : {{nature}}, {{année}} » `[C22]` Repli : ligne masquée |
| Lots, normes et documents | **Garder** | Normes en une ligne : « Performances acoustiques, thermiques et incendie : celles du projet (SIA 181, SIA 180, AEAI), précisées dans l'offre. » `[C15]` Repli : « Les performances visées sont celles du projet, précisées dans l'offre. » |
| Soumission | **Garder** | Texte v2 ; la phrase « visite d'un chantier en cours » reste `[C40]` |
| Témoignage professionnel | **Ajouter, masqué** | 1 citation d'un maître d'ouvrage ou d'un architecte (`C44`) |

### 6.3 L'entreprise (`entreprise.html`)

| Section | Décision | Remplacement |
|---|---|---|
| Notre histoire | **Garder** ; la phrase sous la frise devient le rappel de références (liste courte) | — |
| Notre métier (citation du registre) | **Raccourcir** : citation et source seulement | Paragraphe d'explication supprimé (`C05`) |
| Ce qui guide notre travail (4 cartes) | **Supprimer** | Doublon de la méthode et de l'engagement |
| Notre méthode | **Garder** (version complète) | — |
| Ajout : chiffres clés | **Ajouter** | Bande du §2.2 H3 |
| Vérifiez qui nous sommes | **Garder**, avec les badges du §4.1 | — |
| Si un défaut apparaît | **Raccourcir** | Visible : « Appelez-nous dès que vous le constatez : nous venons voir. » `[C32]` · texte légal v2 dans un repli « Ce que dit la loi » `[V01]` |
| Bande d'appel | **Garder** + liste courte au-dessus des boutons | — |

### 6.4 Réalisations (`realisations.html`)

| Section | Décision | Remplacement |
|---|---|---|
| En-tête | **Raccourcir** | H1 « Réalisations et références » ; chapeau « Nos chantiers, photographiés pendant et après les travaux. » ; mention « Toutes les photos sont nos propres réalisations. » `[C25]` |
| Nouveau : lieux de référence | **Ajouter** en tête | Les 4 cartes du §2.2 H5 et le lien « Voir les {{n}} références » |
| Projets | **Garder** ; le bouton répété 8 fois devient un lien | Sous chaque fiche, lien « Un projet semblable ? » (même cible pré-remplie `contact.html?travaux=…#demande`) |
| Avant, après (7 paires) | **Raccourcir** | 3 paires affichées (AA5, AA6, AA3), bouton « Voir les 4 autres » ; paires faibles non publiées `[À VÉRIFIER]` |
| Ligne de références | **Remplacer** | Mur de références (composant de l'accueil, sans défilement) |
| Votre projet | **Garder** | + badges B1, B3, B4 |

### 6.5 Contact (`contact.html`)

| Section | Décision | Remplacement |
|---|---|---|
| Pour préparer votre demande (5 points) | **Supprimer** | Déjà sur la page merci (« Pour gagner du temps ») |
| Colonne gauche | **Garder** : téléphone en premier sur mobile, puis formulaire | Ajout des badges B1, B3, B9 (sinon B4) à côté du formulaire |
| Ligne de références | **Garder** | Liste canonique moyenne, en noms typographiques |
| Zone | **Raccourcir** | Phrase d'intro : « Depuis Carouge, dans toute la Suisse romande. » ; liste des cantons conservée en texte (accessibilité) ; phrase « Villes marquées sur la carte… » ramenée à la liste |

---

## 7. Formulaire

API, noms de champs et valeurs **inchangés** (`contrat-interface.md`) ; seuls les libellés, l'ordre d'affichage, les regroupements et la réassurance changent. Les messages d'erreur restent ceux de l'API (§8 du contrat).

### 7.1 Ordre des champs et microcopie

| Étape | Ordre v3 | Libellés et aides v3 | Changement |
|---|---|---|---|
| En-tête du bloc | — | H2 « Demander un devis » · « **3 étapes**, environ **une minute**. » (pages services : « Encore 2 étapes, moins d'une minute. ») | Phrase « Nous vous rappelons… » déplacée en étape 3 |
| 1 · Quels travaux ? | `travaux[]` | Cartes v2 inchangées · aide « Plusieurs choix possibles. » · bouton « Continuer : votre projet » | Aide raccourcie |
| 2 · Votre projet | 1 `type_client` · 2 `commune` · 3 `delai` · 4 `surface` | « Vous êtes » avec deux sous-titres visuels : « Particulier » (Propriétaire (maison, appartement, PPE) · Locataire) et « Professionnel » (Régie, gérance ou coopérative · Architecte, bureau d'études ou entreprise générale · Commune ou institution · Entreprise, bureau ou commerce). Mêmes valeurs, même `name`. · Sous le bouton : « Ces réponses nous aident à préparer la visite. » | 6 choix lus comme 2 groupes (loi de Hick) ; raison donnée (« parce que ») |
| 3 · Vos coordonnées | 1 `civilite` (en ligne) · 2 `nom` · 3 groupe « Comment vous joindre ? » (`telephone`, `email`) · 4 `preference_contact` (+ `creneau`) · 5 sous-titre « Si vous le souhaitez » : `message`, `fichiers[]` · 6 `connu_par` (+ `recommande_par`) | Groupe : légende « Comment vous joindre ? » + aide « Un des deux suffit. » ; « Téléphone » · « Pour vous rappeler et convenir de la visite. Exemple : 079 123 45 67. » ; « E-mail » · « Pour la confirmation et l'offre écrite. » · Fichiers : aide du contrat §7 (« JPG, PNG, HEIC ou PDF, 3 fichiers de 8 Mo au plus. Trop lourd ? Envoyez-les par e-mail après notre appel. ») · bouton « Envoyer ma demande » | Remplace les deux mentions « obligatoire si pas d'e-mail / de téléphone » ; facultatifs regroupés en fin d'étape |

Aucun bouton radio présélectionné, aucune case de consentement (D2), « Retour » conserve la saisie, brouillon en `sessionStorage` (v2 inchangé).

### 7.2 Réassurance adjacente

La v2 plaçait 3 lignes sous tout le formulaire, loin du bouton à l'étape 3. En v3, une ligne sous le bouton de chaque étape, puis la colonne :

| Où | Texte | Marqueur |
|---|---|---|
| Sous « Continuer : votre projet » | « La visite et le devis sont gratuits et sans engagement. » | `[À CONFIRMER C02]` Repli : « Vous décidez une fois l'offre écrite reçue. » |
| Sous « Continuer : vos coordonnées » | « Ces réponses nous aident à préparer la visite. » | — |
| Sous « Envoyer ma demande » | « Nous vous rappelons le jour même ou le jour ouvrable suivant. » puis la mention d'information v2 (inchangée, lien « Protection des données ») | `[À CONFIRMER C01]` Repli : « Nous vous rappelons pendant nos heures de bureau. » |
| Colonne (ordinateur), sous le formulaire (mobile) | Téléphone et horaires `C03` · badges B1, B3, B4 · premier témoignage s'il existe | — |
| Au-dessus du bloc | Rappel de références, liste courte | — |

### 7.3 Mobile et comportements

- Quand le bloc `#demande` est visible à 30 % ou plus, la barre fixe masque « Demander un devis » et affiche « Appeler le +41 22 771 20 15 » sur toute sa largeur : pas de second bouton de devis devant le formulaire, et le bouton du formulaire n'est pas recouvert. `scroll-padding-bottom` égal à la hauteur de la barre (WCAG 2.4.11 : focus jamais masqué).
- Erreurs : récapitulatif « {{n}} points à compléter » en haut de l'étape, avec liens vers les champs ; messages de l'API sous chaque champ ; saisie jamais effacée (v2).
- Étape 1 : la carte choisie se coche avec une transition de 150 ms ; pas de passage automatique à l'étape suivante (le visiteur garde la main).
- Pré-remplissage depuis une page service ou `?travaux=` : inchangé.

### 7.4 Mesure

Événements v2 inchangés (`formulaire_debut`, `formulaire_etape`, `formulaire_erreur`, `formulaire_envoye`) ; ajout des propriétés `avec_message`, `avec_fichiers`, `nb_travaux` sur `formulaire_envoye` et des propriétés `f_<drapeau>` (§5.4). Abandon par étape = `formulaire_etape` (2, 3) rapporté à `formulaire_debut`, à suivre dès le rodage.

---

## Annexe · Points à faire valider (identifiants existants)

| Point | Identifiant | Repli |
|---|---|---|
| Afficher « Salle communale de Plan-les-Ouates » au lieu de « Mairie de Plan-les-Ouates » | `C22` | Nom v2 |
| Rattacher des photos à des lieux : P8 = Salle de l'Alhambra ? P2 = salle communale de Plan-les-Ouates ? P6 ou P7 = Conservatoire ? | `C25` | Cartes typographiques |
| Nature et année des travaux pour les 4 lieux de référence | `C22` | Ligne « Travaux » masquée |
| Accord de l'OMC pour son nom (le chiffre passe de 17 à 18) | `C22`, D4 | 17, OMC absente |
| Images d'illustration sous licence (peinture, acoustique, cloisons) jusqu'au shooting | `C40`, décision client | Cartes sans image |
| Mémorisation locale de la variante de test, dans la politique de confidentialité | `V02` | Tests non lancés |
| Confirmations qui remplissent la barre de badges : visite gratuite, GGE, assurance, délai de rappel | `C02`, `C11`, `C12`, `C01` | 2 badges dans le héro |
