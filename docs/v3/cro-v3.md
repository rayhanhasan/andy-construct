# CRO v3 : accueil, en-tête, badges de confiance, drapeaux de test, coupes et formulaire

*Andy Construct · site v3 · expert CRO et copywriter senior · 31 octobre 2026*
*Base : v2 (`a633851`). Ce document applique `docs/v3/brief-v3.md`, qui prime sur la v2. Il suit la mise en page de `docs/v3/direction-artistique.md` (DA) et le module de drapeaux déjà amorcé (`tools/build/static/drapeaux.js`, `config.json` → `ab`) ; les écarts sont listés au §2.5 et au §5.4. Il réutilise les identifiants `C01` à `C44`, `V01`, `V02` de `tools/build/donnees/confirmations.json` (aucun nouvel identifiant). Contrat de l'API inchangé (`docs/v2/contrat-interface.md`).*

Conventions : `[À CONFIRMER Cxx : …]` puis « Repli : … » = texte publié en production tant que la confirmation manque (« masqué » = le bloc disparaît). **Gras** = mot mis en valeur dans le texte courant (jamais dans un titre, un bouton ou un badge, jamais en couleur). Les textes entre guillemets s'intègrent tels quels ; le générateur ajoute les espaces insécables (`fr()`).

---

## 0. En bref

1. **Diagnostic copywriting : situation B** (voix réelle, sobre, factuelle). On garde le lexique v2 (« Demander un devis », « offre écrite », « Ils nous ont confié des travaux ») et on coupe : l'accueil passe de **625 à 375 mots visibles** hors FAQ, dont 42 de noms de références (§2.4).
2. **Levier bloquant (skill offers, équation de valeur) : la probabilité perçue.** Le résultat promis est clair ; la preuve visible manque. D'où une preuve sociale en fil conducteur, sous 6 formes différentes : mur, lieux nommés, chiffres, avis et témoignages, bande défilante avant la demande, pied de page.
3. **Nouveau titre** : « Placo, peinture, acoustique : la rigueur des chantiers publics » (positionnement de `.claude/product-marketing.md`), avec deux variantes testables.
4. **Mur de références** : décision du client du 31.10 (`logos-references.md` §9) : logos officiels en couleur, collectivités comprises, publiés en production seulement après autorisation écrite. Aucune des 18 références n'est encore `autorise` : au lancement, le mur de production est donc entièrement typographique, et la qualité des noms (« wordmarks ») décide du rendu. Règles de mélange logos / noms au §2.3.
5. **En-tête allégé** : 5 entrées (comme la DA), plus de libellé d'horaires ni de boutons en double, compact au défilement. **Pas** de barre supérieure de références.
6. **Badges de confiance** pilotés par `confirmations.json` : 3 vérifiés au lancement (registre du commerce, depuis 2007, Carouge et Suisse romande), un 4e dès que `C02`, `C11` ou `C12` est confirmé.
7. **Tests A/B réalistes** : avec environ 800 visiteurs par mois sur l'accueil (hypothèse à mesurer), seuls des effets d'au moins +50 % sont détectables, en 6 à 9 semaines. Une expérience à la fois par page, rodage de 2 semaines, programme de 5 mois. **Aujourd'hui, 3 drapeaux sont actifs en même temps dans `config.json` : à ne pas mettre en ligne ainsi** (§5.3).
8. **Aucune preuve inventée.** Deux corrections d'honnêteté : le chiffre de références est calculé à partir des noms publiables (17 en production tant que l'accord écrit de l'OMC manque) et s'écrit « références, publiques et privées », jamais « références publiques » ; sur les pages services, une liste de références n'est présentée comme propre au service que si `C23` le confirme.

### 0.1 Règles v2 levées ou maintenues (audience 30-60 ans)

| Règle v2 | v3 | Pourquoi |
|---|---|---|
| 3 expositions de preuve par page au plus | **Levée sur l'accueil** : 6 expositions, chacune sous une forme différente | Retour client « pas assez de preuve sociale, vraiment pas ». La lassitude vient de la répétition identique, pas du nombre |
| Jamais deux blocs de références identiques dans le même écran | **Maintenue** | Le mur et la bande défilante sont séparés par toute la page |
| Bandeau statique, aucun compteur animé | **Levée** (brief §2) : bande défilante pausable, compteurs animés une fois | Valeur finale écrite dans le HTML ; `prefers-reduced-motion` respecté (DA §6) |
| Même liste, dans le même ordre, partout | **Maintenue**, en 3 longueurs canoniques (§2.3) | Effet de simple exposition |
| « Nous ont confié des travaux », jamais « recommandent » ni « partenaires » | **Maintenue** | Exactitude (D5) |
| Surtitres en capitales sur chaque section | **Supprimée** sur l'accueil (DA §10) | 6 surtitres en v2 : bruit visuel |

### 0.2 Affirmations écartées et ce qui les débloquerait (skill copywriting)

| Affirmation demandée ou tentante | Pourquoi elle ne part pas | Ce qui la débloque |
|---|---|---|
| « 300+ chantiers » ou tout nombre de chantiers | Aucune source | `C27` : comptage depuis les factures ou l'agenda |
| « 18 références publiques » (wireframe DA §7.3) | Se lit « 18 clients du secteur public » : faux (environ 7 le sont) ; 17 noms seulement sont publiables en production | « {{n}} références, publiques et privées », `n` calculé |
| Note ou avis clients | Aucun avis public | `C37` : fiche Google gérée, 5 avis au moins |
| « Un seul interlocuteur, de la pose à la peinture » | Sous-traitance non exclue | `C05` |
| « Rappel dans l'heure », « devis en 24 h » | Délai non garanti | `C01`, `C08` (journal des rappels sur 4 semaines) |
| Travaux précis au Conservatoire, à l'Alhambra, à Plan-les-Ouates | Nature et année inconnues | `C22` (nature, année), `C25` (photos rattachées à un lieu) |
| « Membre du GGE » | L'entité JSON-LD pointe déjà vers une fiche gge.ch, mais rien n'est confirmé | `C11` |

---

## 1. Diagnostic CRO de l'accueil v2

Contexte (skill cro) : page d'accueil ; conversion principale = demande de devis (formulaire en 3 étapes) ; secondaires = appel, rappel, dossier PDF. Trafic attendu : recherche locale et de marque ; annonces surtout vers les pages services (`strategie-acquisition.md`, scénario M). Aucune mesure en place (`config.json` : Umami vide).

Classement : **E** = impact élevé, **M** = moyen, **F** = faible. Colonne « v3 » = où la correction est décrite.

| # | Dimension | Constat | Impact | v3 |
|---|---|---|---|---|
| 1 | Proposition de valeur | H1 « Placo, peinture et isolation en Suisse romande » : une catégorie, pas un choix. Il échoue au test de substitution (tout concurrent peut l'écrire). Le seul argument distinctif, les références publiques, arrive sous le pli, en petit. | E | §2.2 H1 |
| 2 | Titre et sous-titre | Le sous-titre (21 mots) répète les métiers du H1, et sa promesse « un seul interlocuteur » dépend de `C05`. En production, le repli la supprime : le héro n'a plus de différenciateur. | E | §2.2 H1 |
| 3 | Preuve sociale | Une seule preuve avant le formulaire : un bandeau de 8 éléments mêlant 4 logos et 4 noms, petits, sans hiérarchie. En production, les logos `a_autoriser` deviennent des noms et l'OMC disparaît : la preuve la plus forte devient une ligne de noms gris. | E | §2.2 H2, §2.3 |
| 4 | Preuve sociale | Les cartes « Réalisations » ne nomment aucun lieu ni client (`C22`) ; aucun chiffre mis en scène ; aucun avis. Le seul type de preuve disponible, des noms, est sous-exploité. | E | §2.2 H4, H5 |
| 5 | Hiérarchie visuelle | Aucun mot en gras ; 6 surtitres ; 9 sections de longueur égale (le « parfait équilibre » qui fait générique) ; les faits du héro ont tous le même poids. Les mots importants ne ressortent pas. | E | §2.1, §2.2 |
| 6 | Images | Une photo de héro et trois vignettes, dont deux « pendant les travaux » : aspect chantier. Aucune image sur les prestations. | M | §2.2 H3, H4, H6 |
| 7 | CTA | Premier écran : bouton d'en-tête, numéro avec horaires, deux boutons de héro de poids proche, ligne d'horaires : 4 actions de contact, le choix se dilue (loi de Hick). | M | §2.2 H1, §3 |
| 8 | En-tête | 8 éléments (logo, 5 entrées, téléphone avec horaires, bouton) et des boutons en double dans le menu ; 80 px permanents, jamais compact. Client : « mal aligné, trop d'informations, trop d'espace vide ». | M | §3 |
| 9 | Longueur | 625 mots visibles hors FAQ, dont 192 dans le bloc de demande ; 8 questions de FAQ. On lit environ 20 % des mots d'une page. | M | §2.4 |
| 10 | Objections | « Trop gros pour moi » traité par une phrase (repli de `C04` faible) ; « combien » sans fourchette (`C31`) ; délais de rappel et de visite en attente (`C01`, `C41`). En production, la réassurance devient vague. | M | §2.2 H2, H8, §7 |
| 11 | Signaux de confiance | Le lien vers le registre du commerce n'est qu'en bas du pied de page ; affiliation et assurance invisibles ; aucun système de badges. | M | §4 |
| 12 | Friction du formulaire | Étape 3 : 8 champs visibles (au-delà des 6 ou 7 conseillés) ; libellés « obligatoire si pas d'e-mail » et « si pas de téléphone » difficiles à lire ; réassurance sous tout le formulaire, loin du bouton ; sur mobile, le bouton « Demander un devis » de la barre fixe reste affiché devant le formulaire. | M | §7 |
| 13 | Parcours professionnel | Le dossier de références (PDF libre, le meilleur atout B2B) n'est relié à aucune preuve de l'accueil. | F | §2.2 H4 |
| 14 | Perception | Aucun mouvement ; le brief demande un site « un peu animé ». | F | DA §6 |
| 15 | Mesure | Aucune donnée de base, aucun dispositif de test : les tests T1 à T8 de la v2 restent théoriques. | F (bloquant pour la suite) | §5 |

**Gains rapides** : 1, 2, 5, 7, 12. **Changements à fort impact** : 3, 4, 6. **À tester** : §5.

---

## 2. Accueil v3

### 2.1 Sections v2 → v3

| v2 | Décision | v3 (ordre de la DA §7.3) |
|---|---|---|
| B.1 Héro | **Garder, réécrire** | H1 · titre, sous-titre, 2 boutons, badges ; surtitre et ligne d'horaires supprimés |
| B.2 Bandeau de références | **Remplacer** | H2 · mur de références en cellules, juste sous le héro |
| B.3 Prestations | **Garder, raccourcir** | H3 · 4 cartes illustrées ; phrase « Vous hésitez ? » et bouton supprimés |
| B.4 Réalisations | **Remplacer** | H4 · projets de référence (lieux nommés) et une carte avant / après |
| — | **Ajouter** | H5 · chiffres clés (bande anthracite) |
| B.5 Méthode | **Garder, raccourcir** | H6 · 4 étapes de 5 à 7 mots, engagement intégré |
| Témoignages (masqué) | **Garder** | H7 · avis Google et témoignages, masqués tant qu'ils sont vides |
| B.6 Professionnels et zone | **Supprimer** | Zone → chiffre « 7 » et badge ; professionnels → lien PDF sous les projets, menu |
| B.7 FAQ (8) | **Garder, réduire** | H8 · 6 questions |
| B.8 Demande | **Garder, alléger** | H9 · bande défilante de rappel, puis demande ; colonne réduite au téléphone et à 3 badges ; module de rappel replié |
| B.9 Pied de page | **Garder, enrichir** | H10 · badges, rappel des références |

Rythme : preuve (héro, mur), offre, preuve (lieux), preuve (chiffres), méthode, preuve (avis), questions, preuve (bande) et demande, preuve (pied). Leviers (skill marketing-psychology) : autorité vérifiable, preuve sociale, simple exposition, position sérielle (noms forts en tête de liste), réduction du risque, loi de Hick (un bouton rouge par écran, DA §5).

### 2.2 Section par section, dans l'ordre

Mise en page, grille et mouvement : DA §5 à §7. Ce qui suit fixe le contenu, sa nature et les règles de conversion.

#### H1 · Héro

- **Nature** : deux zones (DA) : panneau anthracite (titre, sous-titre, boutons, badges) et photo réelle nette `faux-plafond-placo-gorge-lumineuse-01`. Séquence d'entrée orchestrée de la DA §6. La photo s'affiche sans fondu (LCP).
- **Titre (H1, variante A, contrôle)** : « Placo, peinture, acoustique : la rigueur des chantiers publics » (8 mots)
- **Sous-titre** : « Régies, architectes, communes ou particuliers : nous venons voir, puis remettons une **offre écrite** détaillée. » (14 mots) `[À CONFIRMER C06 : « détaillée »]` Repli : sans « détaillée ».
- **Bouton 1** (rouge) : « Demander un devis » → `#demande`
- **Bouton 2** (contour clair) : « Appeler le +41 22 771 20 15 »
- **Badges** (4 emplacements, §4.1) : « Registre du commerce » / « Inscrite, vérifiable sur Zefix » (lien Zefix) · « Depuis 2007 » / « {{19}} ans d'activité » · « Siège à Carouge » / « Toute la Suisse romande » · 4e : premier confirmé parmi `C02` → `C11` → `C12`, sinon masqué. Ces trois badges reprennent les quatre libellés de la DA §5, avec un sous-texte.
- Supprimés : surtitre « Carouge · depuis 2007 », ligne « Du lundi au vendredi… » (les horaires vont dans le bloc de demande, la page contact et le pied de page).

**Trois variantes de titre testables** (8 mots au plus, sans tiret long, sans formule creuse) :

| Variante | Titre | Angle et levier | Condition |
|---|---|---|---|
| **A (contrôle)** | « Placo, peinture, acoustique : la rigueur des chantiers publics » | Autorité. Passe le test de substitution : seule une entreprise qui a travaillé pour des collectivités peut l'écrire, et le mur juste dessous le prouve. | Aucune |
| **B** | « Du Conservatoire à votre salon : placo, acoustique, peinture » | Similarité. Désamorce « trop gros pour moi » (`personas-psychologie.md` §1.4) en reliant la grande référence au logement du visiteur. On voit les deux lieux. | Nom en texte, même règle que le bandeau v2 (repli de `C22`) ; le nom complet est dans le mur juste dessous |
| **C** | « Un seul interlocuteur, de l'ossature à la peinture » | Simplicité, effort réduit. Le plus faible au test de substitution. | **Seulement si `C05` est confirmé.** En réserve |

#### H2 · Mur de références (preuve 1)

- **Nature** : section juste sous le héro, fond plâtre, grille de cellules blanches identiques séparées par des filets (DA §5) : 6 × 2 sur ordinateur, 3 × 4 sur tablette, 2 × 4 sur mobile (les 8 premières). Révélation des cellules une fois, décalées de 40 ms (DA §6). Aucun lien vers les sites des références.
- **Titre (H2)** : « Ils nous ont confié des travaux »
- **Cellules, dans cet ordre** (production) : Ville de Genève · Conservatoire de musique de Genève · HEAD – Genève · Salle de l'Alhambra · UBS · Piaget · Salle communale de Plan-les-Ouates · Salle communale de Collonge-Bellerive · J. Safra Sarasin · Labcorp · Everness Hotel & Resort `[À CONFIRMER C22 : même hôtel que l'« Hôtel Chavannes-de-Bogis »]` (Repli : « Hôtel à Chavannes-de-Bogis ») · Celgene. En preview, l'OMC peut occuper la 4e cellule (D4) ; en production, c'est l'Alhambra. Ordre : public en tête (position sérielle), communes au début de la 2e rangée pour les particuliers et les communes, public et privé ensuite alternés.
- **Sous la grille** : « Et des **particuliers**, à Genève et dans toute la région. » `[À CONFIRMER C04]` Définitif : « Et des **particuliers**, pour une cloison, un plafond ou une pièce à repeindre. » · lien « Voir les {{n}} références » → `professionnels.html#references`
- `{{n}}` = nombre de noms publiables dans le mode de génération (17 en production tant que l'accord écrit de l'OMC manque, 18 ensuite). Jamais écrit en dur.
- Harmonisation : le `nom_affiche` « Mairie de Plan-les-Ouates » devient « Salle communale de Plan-les-Ouates », comme son `nom_complet` et la référence de Collonge-Bellerive (à valider avec `C22`).

#### H3 · Prestations

- **Nature** : titre et 4 cartes illustrées (image 4:3, carte entièrement cliquable, texte du lien masqué visuellement : « Voir le placo »…). **Plus de bouton dans cette section** : l'en-tête compact et la barre mobile restent disponibles, et le bouton suivant arrive sous les projets.
- **H2** : « Quatre métiers, souvent sur le même chantier »

| Carte | Texte | Gras | Image |
|---|---|---|---|
| **Placo** | « Cloisons, doublages et **faux-plafonds** en plaques de plâtre. » | faux-plafonds | `faux-plafond-placo-gorge-lumineuse-02` (réelle) |
| **Peinture** | « Murs et plafonds intérieurs, **préparés puis peints**. » | préparés puis peints | Illustration sous licence, mention « Illustration », jusqu'au shooting peinture (`C40`) |
| **Isolation acoustique** | « Vous entendez vos voisins ? Nous **isolons murs et plafonds**. » | isolons murs et plafonds | `panneaux-acoustiques-muraux-01` (réelle, `C18`) ; repli : illustration |
| **Cloisons isolantes** `[C16]` | « Entre une **pièce chauffée** et une cave, un garage ou des combles. » | pièce chauffée | AA3 « après » (réelle) `[À VÉRIFIER : qualité]` ; repli : `chantier-ossature-puits-de-lumiere-02` |

Règle des illustrations (DA §4) : jamais présentées comme une réalisation d'Andy Construct, mention « Illustration », texte alternatif sans « nos travaux ».

#### H4 · Projets de référence (preuve 2)

- **Nature** : composition asymétrique de la DA (une grande carte, des cartes empilées), étendue à 4 lieux et une carte avant / après. Une carte de lieu sans photo rattachée à ce lieu est **typographique** : fond profond, nom du lieu en grand corps, ligne de type en petites capitales, trait rouge (le « laser » de la DA), commune en bas. La grande carte revient au premier lieu qui obtient une vraie photo (`C25`), sinon à la carte avant / après.
- **H2** : « Projets de référence »

| Carte | Titre | Ligne de type | Photo | Ligne de travaux |
|---|---|---|---|---|
| 1 | « Conservatoire de musique de Genève » | « Genève · École de musique » | Typographique ; photo seulement si `C25` rattache P6 ou P7 à ce lieu | « Travaux : {{nature}}, {{année}} » `[À CONFIRMER C22]` Repli : masquée |
| 2 | « Salle de l'Alhambra » | « Genève · Salle de spectacle » | `[À CONFIRMER C25 : la salle à balcons de P8 (chantier-salle-de-spectacle-01) est-elle l'Alhambra ? Quelle prestation ?]` Repli : typographique | Idem |
| 3 | « Salle communale de Plan-les-Ouates » | « Plan-les-Ouates · Collectivité » | `[À CONFIRMER C25 : la « salle publique » de P2 est-elle cette salle ?]` Repli : typographique | Idem |
| 4 | « HEAD – Genève » | « Genève · Haute école d'art et de design » | Typographique | Idem |
| 5 | « Séjour : faux-plafond et spots » | « Appartement · avant, après » | Paire AA6 (réelle) `[À VÉRIFIER : qualité]` ; repli : AA5 | Étiquettes « Placo · Peinture » `[C26]` Repli : « Placo » |

Pas de photo d'un bâtiment tiers au lancement : une façade suggérerait des travaux extérieurs et un soutien de l'institution. Possible plus tard avec l'accord écrit du lieu (`C22`), une légende « Le bâtiment · photo : {{auteur}}, {{licence}} » et la mention « Nos travaux : l'intérieur ».

- **Sous les cartes** : bouton « Un projet semblable ? Demander un devis » · lien « Voir toutes les réalisations » · lien « Professionnels : dossier de références (PDF, 615 Ko) » (`data-suivi="telechargement"`). La preuve adjacente à ce bouton : les cartes elles-mêmes.

#### H5 · Chiffres clés (preuve 3)

- **Nature** : bande anthracite (DA §5), 4 chiffres (2 × 2 sur mobile), qui comptent de 0 à la valeur **une fois** à l'apparition. La valeur finale est écrite dans le HTML (sans JavaScript, on voit « 19 », jamais « 0 »).

| Chiffre | Libellé | Source et règle | Statut |
|---|---|---|---|
| « 19 » | « ans d'activité » | Calculé au build : années révolues depuis le 1.6.2007 (20 dès juin 2027) | Vérifié (registre) |
| « 18 » | « références, publiques et privées » | `{{n}}` du mur (17 en production sans l'OMC) | Vérifié |
| « 4 » | « métiers intérieurs » | Les 4 services | Vérifié |
| « 7 » | « cantons et régions romands » | Zone déclarée (GE, VD, NE, FR, Valais romand, JU, Jura bernois). C'est une zone, pas une preuve : ne jamais écrire « chantiers dans 7 cantons » | Vérifié ; `C21` peut restreindre la zone des particuliers |
| `{{n}}` | « chantiers depuis 2007 » | `[À CONFIRMER C27]` | Remplace « 4 » dès confirmation |
| « 1 » | « jour ouvrable, au plus, pour vous rappeler » | `[À CONFIRMER C01]` | Remplace « 7 » dès confirmation |
| `{{n}}` | « personnes sur nos chantiers » | `[À CONFIRMER C24]` | En réserve |

#### H6 · Méthode

- **Nature** : 4 étapes numérotées (vraie séquence, DA §10), avec la photo réelle `habillage-placo-niches-arrondies-01` (escalier protégé pendant les travaux).
- **H2** : « Un chantier en quatre étapes »

| N° | Étape | Texte | Marqueur |
|---|---|---|---|
| 1 | « Visite » | « Mesures et écoute, sur place. » | aucun |
| 2 | « Offre écrite » | « Poste par poste, **en CHF**. » | `[À CONFIRMER C06]` Repli : « Remise après la visite. » |
| 3 | « Chantier protégé » | « Sols et meubles couverts, **nettoyage chaque soir**. » | `[À CONFIRMER C07]` Repli : « Lieux protégés pendant les travaux. » |
| 4 | « Réception » | « Le tour des finitions, **ensemble**. » | aucun |

- **Engagement** (encadré sous les étapes) : « **Aucun supplément** sans votre accord écrit et chiffré. » `[À CONFIRMER C06]` Repli : masqué. C'est la seule garantie de l'offre (engagement de service, skill offers) : pas de remboursement, pas de rareté, pas d'urgence.
- Lien : « Notre méthode en détail » → `entreprise.html#methode`

#### H7 · Avis et témoignages (preuve 4, masquée tant qu'elle est vide)

- **Avis Google** (`tools/build/donnees/avis.json`, affiché dès `nombre` ≥ 5, `C37`) : « **{{note}} sur 5** · {{nombre}} avis Google · relevé le {{date_releve}} » + lien « Lire les avis sur Google ». Texte statique, aucun widget, aucune note dans le JSON-LD. Dès qu'il existe, il prend aussi le 4e badge du héro (§4.1).
- **Témoignages** (`temoignages.json`, `C44`) : H2 « Ce qu'en disent nos clients », 1 à 3 citations au format v2 (§A.11) : « {{texte exact}} » · {{nom ou fonction}}, {{organisation}}, {{commune}} · {{travaux}}, {{année}}. Note : « Témoignages publiés tels quels, avec l'accord écrit de leurs auteurs. » Le générateur refuse une citation sans `accord_date`. Le premier est repris, court, dans la colonne du bloc de demande.
- Aucun titre orphelin, aucun « bientôt » tant que les fichiers sont vides.

#### H8 · Questions fréquentes (6 au lieu de 8, hors comptage)

H2 « Questions fréquentes » · « Une autre question ? Appelez le +41 22 771 20 15. »
Réponses v2 reprises, 35 mots au plus, mêmes marqueurs : (1) petits travaux `C04` ; (2) prix `C06` ; (3) visite payante `C02` ; (4) délais de rappel et de visite `C01`, `C41` ; (5) hors de Genève `C21`, `C22` ; (6) défaut après les travaux `C32`, `V01`. Retirées : « protection du logement » (dite par la méthode) et « régies, architectes, communes » (dite par les projets). Le JSON-LD `FAQPage` suit le texte visible mot pour mot.

#### H9 · Bande défilante et demande (preuve 5)

- **Bande défilante** (DA §5, juste avant le bloc de demande) : tous les noms publiables, dans l'ordre du mur, puis Energestion · Dipan · Harmonie Nautique de Genève · Domaine des Perrières · de Grisogono. Libellé court au début, lu par les lecteurs d'écran : « Ils nous ont confié des travaux ». Bouton visible « Mettre en pause » / « Reprendre » (`aria-pressed`, WCAG 2.2.2) ; pause au survol et au focus ; le double qui sert à la boucle porte `aria-hidden="true"` ; arrêtée en mouvement réduit. C'est le rappel de références qui précède le bouton final.
- **H2** : « Demander un devis »
- **Introduction** : « **3 étapes**, environ **une minute**. »
- **Étape 1** : libellés v2 inchangés (§7).
- **Sous « Continuer : votre projet »** : « La visite et le devis sont gratuits et sans engagement. » `[À CONFIRMER C02]` Repli : « Vous décidez une fois l'offre écrite reçue. »
- **Lien** : « Vous préférez qu'on vous rappelle ? » (ouvre le module de rappel, replié par défaut ; textes v2 §A.7).
- **Colonne** : « Ou appelez le +41 22 771 20 15 » (grand corps) · « Lun-ven, 7 h – 18 h » `[À CONFIRMER C03]` Repli : masqué · badges compacts « Registre du commerce », « Siège à Carouge », « Offre écrite après visite » · premier témoignage s'il existe.
- Supprimés : surtitre « Votre demande », phrase « Nous vous rappelons pour convenir d'une visite » (devenue la réassurance de l'étape 3), colonne « Par téléphone » à deux numéros (le mobile reste sur la page contact et dans le pied de page), ligne de références de la colonne (remplacée par la bande).

#### H10 · Pied de page (preuve 6)

- Colonnes v2 (marque, « Nous joindre » avec le bloc NAP et les horaires, prestations, liens Andy Construct avec le PDF) ; rappel des références sur pastilles blanches (DA §5), règles du §2.3.
- **Badges** (une ligne) : « Registre du commerce » · « Depuis 2007 » · « Siège à Carouge » · « Membre du GGE » `[C11]` Repli : masqué.
- Barre basse v2 inchangée (© année du build, raison sociale, IDE, « Vérifier au registre du commerce », mentions, protection des données).

### 2.3 Mur de références : mélanger logos et noms proprement

**Constat.** Dans `logos.json` (état du 31.10, `logos-references.md` §9) : 0 référence `autorise`, 17 `a_autoriser` (dont les anciennes `protege` : Ville de Genève, Collonge-Bellerive, Plan-les-Ouates, Alhambra, OMC), 1 `introuvable` (Domaine des Perrières). Décision du client : le logo officiel en couleur partout où il existe. En production (D6), seuls les logos `autorise` s'affichent : au lancement, **toutes les cellules sont des noms** ; pendant la campagne d'autorisations, la grille sera **mixte** ; en preview, le client voit des logos qui ne seront peut-être jamais publiés (la Ville de Genève réserve son logo aux projets qu'elle soutient). La v2 mêlait des logos de hauteurs et de styles différents avec des noms : c'est ce qu'il a jugé « mélangé, petit, sans hiérarchie ».

**Règles.**
1. **La cellule est l'unité.** Toutes les cellules ont la même taille, le même fond blanc, le même filet (DA §5). Le contenu est centré ; la cellule ne prend jamais la couleur de la marque, même au survol.
2. **Hauteur optique commune.** Logos : 56 px × `echelle` (DA). Noms : hauteur de capitale calée sur la hauteur des lettres des logos voisins (environ 22 à 24 px au bureau), jamais plus grands que le plus grand logo de la rangée.
3. **Typographie des noms** : la police de titrage du site (DA : Archivo 108 %, 600), jamais celle de la marque citée, couleur anthracite. Le nom propre est en demi-gras ; les mots génériques passent au-dessus, en maigre et à 60 % de la taille : « Ville de » / **Genève** ; « Salle communale de » / **Collonge-Bellerive** ; « Salle de » / **l'Alhambra**. Un nom long sans générique tient sur deux lignes équilibrées, coupées dans les données (« Conservatoire de musique » / « de Genève »), avec `text-wrap: balance`. Deux lignes au plus. Traits d'union insécables (Plan-les-Ouates, Collonge-Bellerive).
4. **Grille mixte** (production pendant les autorisations) : un logo autorisé remplace le nom **dans sa cellule, sans changer l'ordre** (l'ordre canonique prime : c'est lui qui crée la familiarité). Ce sont la cellule commune (règle 1) et l'équilibre optique (règle 2) qui rendent le mélange propre. Les noms ne sont jamais en couleur pour « répondre » aux logos voisins.
5. **Priorité des demandes d'autorisation** (pour sortir vite du mode mixte) : d'abord la 1re rangée (Conservatoire, HEAD, Alhambra, UBS, Piaget), puis les deux communes, la Ville de Genève en dernier (refus probable : la cellule restera un nom, en tête de grille).
6. En production, aucun emblème ni armoirie sans autorisation écrite (LPAP art. 8 al. 5 ; OMC : Convention de Paris art. 6ter) ; aucune croix suisse. Texte alternatif d'un logo = `nom_affiche`.
7. **Trois listes canoniques**, toujours dans le même ordre :
   - **courte** (près d'un bouton, une ligne) : Ville de Genève · Conservatoire de musique de Genève · HEAD – Genève · Salle de l'Alhambra · « et {{n−4}} autres » ;
   - **moyenne** (contact, pages services sans `C23`) : la courte sans « et … autres », puis Salle communale de Plan-les-Ouates · Salle communale de Collonge-Bellerive · « et des particuliers de toute la région » ;
   - **complète** (mur : 12 premiers ; bande, pied, professionnels : tous) : ordre du §2.2 H2, puis H9.

Données à ajouter à `logos.json` (aucune modification ici) : `ordre` (entier), `nom_lignes` (1 ou 2 lignes), `generique` (texte maigre éventuel).

### 2.4 Comptage des mots visibles

Méthode de l'annexe du copy deck v2 : sections H1 à H9, formulaire à l'étape 1, hors questions et réponses de la FAQ, hors en-tête et pied de page. Un nom de référence n'est compté qu'une fois sur la page (le mur, les cartes de lieux et la bande répètent les mêmes noms).

| Section | Mots | dont noms |
|---|---|---|
| H1 Héro (4 badges) | 57 | — |
| H2 Mur (titre, 12 noms, pied) | 51 | 31 |
| H3 Prestations | 49 | — |
| H4 Projets de référence (noms déjà comptés) | 44 | — |
| H5 Chiffres | 16 | — |
| H6 Méthode | 45 | — |
| H9 Bande (libellé, bouton, 5 noms nouveaux) et demande | 113 | 11 |
| **Total** | **375** (v2 : 625) | **42** |

Texte courant hors noms : 333 mots. Avec les replis actuels (4e badge masqué, « détaillée » et engagement retirés), environ 359.

**Mots en gras, récapitulatif** : offre écrite · particuliers · faux-plafonds · préparés puis peints · isolons murs et plafonds · pièce chauffée · en CHF · nettoyage chaque soir · ensemble · Aucun supplément · 3 étapes · une minute.

**Position du formulaire** : vers l'écran 9 ou 10 sur mobile (390 × 844), à cause des images ; la barre fixe donne accès à la demande en un geste à tout moment.

### 2.5 Écarts avec la direction artistique, à arbitrer

| Sujet | DA | Recommandation CRO | Raison |
|---|---|---|---|
| Libellé de la bande des chiffres (§7.3) | « 18 références publiques » | « {{n}} références, publiques et privées », `n` calculé | Exactitude ; 17 noms publiables en production |
| Noms à la place des logos non autorisés | Wordmark Archivo 108 %, 600 | Même police, plus le traitement « générique en maigre au-dessus, nom propre en demi-gras » et la hauteur de capitale calée sur les logos (§2.3, règles 2 et 3) | En production, c'est le rendu de toutes les cellules au lancement |
| Format du téléphone (en-tête §7.1, mobile §7.2) | « 022 771 20 15 » | « +41 22 771 20 15 » (charte, NAP), comme dans tout le copy deck v2 ; « 022 » réservé au test T6 (§5.2, réserve) | Même numéro écrit de la même façon partout |
| Badges du héro | 4 libellés simples | 3 badges avec sous-texte (§4) qui reprennent ces 4 libellés, plus un 4e confirmable | Format demandé : titre de 4 mots, sous-texte de 6 |

---

## 3. En-tête v3

### 3.1 Contenu exact (ordinateur ≥ 1240 px)

| Zone | Contenu | Remarque |
|---|---|---|
| Gauche | Logo (colonne 1 de la grille). Texte alternatif : « Andy Construct, page d'accueil » | Logo intact (charte) |
| Centre-gauche | « Prestations » (bouton, panneau au clic) · « Réalisations » · « Professionnels » · « L'entreprise » · « Contact » | 5 entrées (brief : 4 ou 5) ; « Contact » en dernier (position sérielle) |
| Panneau Prestations | « Placo » · « Cloisons, doublages, faux-plafonds » / « Peinture » · « Murs et plafonds, à l'intérieur » / « Isolation acoustique » · « Contre le bruit et l'écho » / « Cloisons isolantes » · « Caves, garages, combles » `[C16]` | `<details>` v2 conservé ; fondu et 8 px (DA §6) |
| Droite | Icône téléphone + numéro (lien `tel:`, `emplacement=entete`) · bouton rouge « Demander un devis » | Le seul élément rouge de l'en-tête |

**Ce qu'on retire** : le libellé d'horaires « Lun-ven, 7 h – 18 h » au-dessus du numéro ; les boutons « Appeler » et « Demander un devis » dupliqués dans le menu sur ordinateur (`nav-extra`) ; la barre « Version de validation » en production (inchangé).

**Alignement** (DA §7.1) : une ligne, tous les éléments sur le même axe vertical ; logo sur la colonne 1, menu aligné à gauche après le logo, téléphone et bouton contre le bord droit de la grille, sur la même grille que le contenu.

### 3.2 Défilement (compact)

- Au repos : 76 px. Après 40 px de défilement : 60 px, logo réduit (`transform`, sans changement de mise en page), filet et ombre diffuse ; 250 ms (DA §6). Mouvement réduit : changement immédiat.
- L'en-tête reste visible (il ne se cache pas au défilement vers le bas) : le bouton reste à portée.
- Espace réservé dès le chargement : aucun décalage du contenu (CLS nul).

### 3.3 Mobile et tablette

- **< 900 px** : logo à gauche, bouton « Menu » (icône et mot, 48 px) à droite ; pas de téléphone dans l'en-tête (la barre fixe du bas porte « Appeler » et « Demander un devis »). En-tête 60 px + barre 64 px : moins de 15 % d'un écran de 844 px.
- **Menu ouvert** (DA §7.2) : plein écran, focus piégé, Échap ferme. « Prestations » (les 4 services) · « Réalisations » · « Professionnels » · « L'entreprise » · « Contact » ; en bas : « Appeler le +41 22 771 20 15 », « Demander un devis », puis 2 badges (« Registre du commerce », « Siège à Carouge »).
- **900 à 1239 px** : logo, bouton « Appeler », bouton « Demander un devis », bouton « Menu ».

### 3.4 Barre supérieure « Ils nous ont confié des travaux : … » : **non**

1. Le client trouve l'en-tête trop chargé ; une troisième bande horizontale (barre, en-tête, barre mobile) va dans le sens inverse.
2. Elle répéterait le mur, visible dans le premier écran (DA : le héro laisse voir la première rangée de cellules à 1440 × 900) : deux listes identiques dans le même écran.
3. En 12 ou 13 px, elle se lit comme des petits caractères ; un public exigeant y voit un procédé publicitaire.
4. Elle repousse le héro, l'élément qui doit produire le « c'est beau » des 5 premières secondes.

Si le client insiste : ordinateur seulement, 32 px, statique, liste courte, derrière un drapeau `barre-refs` pour en mesurer l'effet (§5).

---

## 4. Badges de confiance (« flags »)

Rendu selon `confirmations.json` : un badge `[Cxx]` non confirmé disparaît. Icônes au trait (20 px, trait de 1,5 px, monochromes, DA), aucun émoji. Un badge n'est cliquable que vers une source vérifiable.

| # | Titre (≤ 4 mots) | Sous-texte (≤ 6 mots) | Icône | Statut | Lien |
|---|---|---|---|---|---|
| B1 | « Registre du commerce » | « Inscrite, vérifiable sur Zefix » | Document avec sceau | Vérifié | Zefix (IDE CHE-113.706.162) |
| B2 | « Depuis 2007 » | « {{19}} ans d'activité » (calculé) | Calendrier | Vérifié | aucun |
| B3 | « Siège à Carouge » | « Toute la Suisse romande » | Repère de carte | Vérifié (`C21` peut nuancer pour les particuliers) | `contact.html#zone` |
| B4 | « Offre écrite » | « Après visite sur place » | Document à lignes | Vérifié (texte de repli de `C06`) | aucun |
| B5 | « {{n}} références » | « Dont la Ville de Genève » | Façade à colonnes | Vérifié (`n` calculé) | `professionnels.html#references` |
| B6 | « Visite et devis gratuits » | « Sans engagement » | Presse-papiers coché | À confirmer `C02` | aucun |
| B7 | « Membre du GGE » | « Entreprises genevoises du bâtiment » | Bouclier simple | À confirmer `C11` | Fiche gge.ch, si confirmée |
| B8 | « Assurance responsabilité civile » | « Attestation sur demande » | Bouclier coché | À confirmer `C12` | aucun |
| B9 | « Rappel le jour même » | « Ou le jour ouvrable suivant » | Combiné et horloge | À confirmer `C01` | aucun |
| B10 | « Attestations à jour » | « AVS, LPP, impôts, sur demande » | Dossier | À confirmer `C13` | `mailto:` objet « Demande d'attestations » |
| B11 | « Un seul interlocuteur » | « De la pose à la peinture » | Silhouette | À confirmer `C05` | aucun |
| B12 | « Jamais de liquide d'avance » | « Paiement sur facture » | Facture | À confirmer `C28` | aucun |
| B13 | « {{note}} sur 5 » | « {{n}} avis Google » | Étoile | Dès 5 avis réels (`C37`, `avis.json`) | Fiche Google |

### 4.1 Où les afficher

| Emplacement | Badges, par ordre de priorité | Au lancement (rien de confirmé) |
|---|---|---|
| Héro (4 au plus) | B1, B2, B3, puis le premier disponible parmi B13 → B6 → B7 → B8 | B1, B2, B3 |
| Bloc de demande, colonne (3) | B1, B3, B4 ; B9 remplace B4 si `C01` | B1, B3, B4 |
| Pages services, sous le H1 (3) | B11 si `C05`, sinon B4 ; B6 si `C02`, sinon B3 ; B1 | B4, B3, B1 |
| Professionnels, sous le H1 (4) | B1, B5, B8, B10 | B1, B5 |
| L'entreprise, « Vérifiez qui nous sommes » | Tous les badges vérifiés ou confirmés, sauf B13 | B1 à B5 |
| Contact, à côté du formulaire (3) | B1, B3, B9 (sinon B4) | B1, B3, B4 |
| Pied de page (une ligne) | B1, B2, B3, B7 | B1, B2, B3 |
| Menu mobile | B1, B3 | B1, B3 |

Règle : jamais deux éléments qui disent la même chose dans un même écran (le badge B2 du héro et le chiffre « 19 ans » sont séparés par le mur, les prestations et les projets ; le badge B4 n'apparaît pas dans le héro, dont le sous-titre dit déjà « offre écrite »).

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
- On ne détecte que des **effets importants**. Une variante meilleure de 10 % ressortira « non concluante » : il faut le dire dans le bilan.
- **Horizon fixe** décidé avant le lancement ; au moins 2 semaines complètes ; 8 semaines au plus. Pas d'arrêt anticipé sur un résultat favorable ; arrêt immédiat seulement si un garde-fou est franchi.
- **Une expérience à la fois par page** et par indicateur. Deux expériences peuvent tourner ensemble seulement si leurs zones et leurs indicateurs diffèrent (tirages indépendants).
- À l'horizon sans échantillon suffisant : « non concluant », on garde A (ou la version la plus simple) et on publie l'intervalle de l'effet.
- Contrôle de répartition (SRM) chaque semaine : khi-deux sur les expositions A / B ; p < 0,01 = panne de répartition, on arrête et on corrige.
- Éthique : les deux variantes sont honnêtes et n'utilisent aucune affirmation non confirmée.

### 5.2 Expériences prioritaires

Noms de drapeaux alignés sur le module en cours (`config.json` → `ab.drapeaux`). Score ICE (impact, confiance, facilité, de 1 à 10) :

| Drapeau | Expérience | I | C | F | ICE | Faisable sous H |
|---|---|---|---|---|---|---|
| `hero-titre` | XP1 · titre du héro | 8 | 6 | 9 | 7,7 | Oui, 6 semaines |
| `entree-demande` | XP4 · rappel express à côté du formulaire | 7 | 6 | 6 | 6,3 | Oui, 8 à 9 semaines |
| `cta-libelle` | XP3 · « devis » ou « visite » | 6 | 5 | 8 | 6,3 | Oui, 6 semaines |
| `ordre-sections` | XP2 · projets avant prestations | 6 | 5 | 7 | 6,0 | Oui, 6 semaines |
| `etape3-allegee` | XP5 · étape 3 allégée | 6 | 6 | 7 | 6,3 | **Non** : lancement surveillé |

#### XP1 · `hero-titre` (accueil)

- **Hypothèse** : parce que le titre v2 décrit une catégorie et que les grandes références intimident une partie des particuliers (« trop gros pour moi »), nous pensons qu'un titre qui relie la grande référence au logement du visiteur augmentera les intentions de contact sur l'accueil. Nous le saurons quand `intention_contact` par visiteur exposé sera plus élevé en B.
- **A** : « Placo, peinture, acoustique : la rigueur des chantiers publics »
- **B** : « Du Conservatoire à votre salon : placo, acoustique, peinture »
- Sous-titre, badges et boutons identiques. Mettre à jour la `description` du drapeau dans `config.json` avec ces deux textes.
- **Indicateur principal** : `intention_contact` / `exposition_variante` (unité : visiteur).
- **Secondaires** : `devis_clic` avec `emplacement=heros` ; part des `formulaire_envoye` avec un `type_client` professionnel.
- **Garde-fous** : `formulaire_envoye` par visiteur exposé (pas de baisse) ; part des demandes professionnelles (pas de baisse de plus de 30 % relatifs) ; LCP mobile inchangé.
- **Exposition** : au chargement de l'accueil. **Durée** : 6 semaines (555 par variante).

#### XP2 · `ordre-sections` (accueil)

- **Hypothèse** : parce que les régies, architectes et communes cherchent d'abord des références comparables, nous pensons que placer les projets de référence avant les prestations augmentera les intentions de contact sans gêner les particuliers. Nous le saurons quand `intention_contact` sera plus élevé en B sans baisse des visites des pages services depuis l'accueil.
- **A** : héro · mur · **prestations · projets** · chiffres · méthode…
- **B** : héro · mur · **projets · prestations** · chiffres · méthode…
- Textes identiques. Déplacement dans le DOM pendant l'analyse du HTML (ordre de lecture = ordre visuel, DA §9) ; jamais de `order` CSS.
- **Indicateur principal** : `intention_contact` / visiteur exposé. **Garde-fous** : visites des pages services depuis l'accueil ; `formulaire_envoye`.
- **Exposition** : au chargement. **Durée** : 6 semaines.

#### XP3 · `cta-libelle` (site entier)

- **Hypothèse** : parce que la prochaine étape réelle est une visite, et qu'un public de 30 à 60 ans plus aisé associe « devis » à une mise en concurrence sur le prix, nous pensons que « Demander une visite » augmentera les clics sur le bouton principal sans faire baisser les demandes envoyées. Nous le saurons quand `devis_clic` par visiteur exposé sera plus élevé en B, avec `formulaire_envoye` stable.
- **A** : « Demander un devis » partout (en-tête, héro, barre mobile, boutons de section, H2 du bloc) ; pages services : « Demander un devis pour du placo »…
- **B** : « Demander une visite » partout, H2 du bloc « Demander une visite » ; pages services : « Demander une visite pour du placo »… Formulaire, réassurance et page merci identiques. Un visiteur garde le même libellé sur tout son parcours (un seul libellé, règle v2).
- **Indicateur principal** : `devis_clic` / visiteur exposé. **Garde-fous** : `formulaire_envoye` / visiteur exposé ; part de `type_client` particulier.
- **Plus tard** : variante C « Demander un devis gratuit », seulement si `C02` est confirmé.
- **Durée** : 6 semaines.

#### XP4 · `entree-demande` (bloc de demande, sur toutes les pages qui l'ont)

- **Hypothèse** : parce que le téléphone reste le canal préféré des régies et des particuliers, nous pensons qu'un rappel express visible à côté du formulaire augmentera le nombre de demandes commencées. Nous le saurons quand `formulaire_debut` (devis ou rappel) par visiteur qui voit le bloc sera plus élevé en B, sans baisse des devis envoyés.
- **A** : formulaire en 3 étapes ; module de rappel replié derrière le lien « Vous préférez qu'on vous rappelle ? ».
- **B** : au-dessus de l'étape 1 (mobile) ou dans la colonne (ordinateur), une carte ouverte : « Plutôt un appel ? » · « Laissez votre numéro, nous vous rappelons. » · champ « Votre numéro de téléphone » · bouton « Être rappelé(e) » · « Votre numéro ne sert qu'à ce rappel. » ; au-dessus du formulaire : « Ou décrivez vos travaux en 3 étapes ». API inchangée (`formulaire=rappel`).
- **Indicateur principal** : `formulaire_debut` (tous formulaires) / visiteur exposé. **Secondaires** : `formulaire_envoye` par formulaire.
- **Garde-fous** : devis envoyés (pas de baisse de plus de 30 %) ; joignabilité des rappels (suivi des prospects).
- **Exposition** : bloc `#demande` visible à 50 % pendant une seconde. **Durée** : 8 à 9 semaines (ou 7 à α = 10 %, à écrire dans le bilan). Peut tourner en même temps que XP1 (zone et indicateur différents).

#### XP5 · `etape3-allegee` (conditionnelle)

- **A** : étape 3 complète (§7). **B** : message, fichiers et « Comment nous avez-vous connus ? » regroupés sous « Ajouter un message, des photos ou des plans (facultatif) », replié.
- **Indicateur** : `formulaire_envoye` / `formulaire_etape` (étape 3). **Garde-fous** : part des envois avec message ou fichiers (§5.4) ; score moyen des demandes (suivi des prospects).
- **Sous H : non testable** (390 visiteurs à l'étape 3, environ 9 mois). Test seulement au-delà de 150 étapes 3 par mois (par exemple avec les annonces) ; sinon décision qualitative (enregistrements de session ou entretiens) et comparaison avant / après étiquetée « indicative ».

**Réserve** : T6 v2 (« Appeler » contre « Appeler le 022 771 20 15 » dans la barre mobile), titre C si `C05`, `barre-refs` si le client l'exige.

### 5.3 Calendrier et activation

**État actuel à corriger avant la mise en ligne** : `config.json` → `ab.drapeaux` active `hero-titre`, `cta-libelle` et `ordre-sections` **en même temps**. Deux expériences sur l'accueil et une sur tout le site, avec des indicateurs qui se recoupent : aucune ne serait lisible. Au lancement, tous les drapeaux à `"actif": false`, sauf `aa-temoin`.

| Semaines | Accueil | Formulaire et site |
|---|---|---|
| 1-2 | **Rodage** : drapeau témoin `aa-temoin` (A/A, aucun changement visible) ; vérification de la mesure, SRM, taux de base réels ; recalcul des durées du §5.1 | — |
| 3-8 | XP1 `hero-titre` | XP4 `entree-demande` (semaines 3 à 11) |
| 9-14 | XP2 `ordre-sections` | — |
| 15-20 | XP3 `cta-libelle` (site entier : rien d'autre en parallèle) | — |

Chaque expérience a une fiche (gabarit « Test Plan » du skill ab-testing) remplie **avant** le lancement, puis un bilan (gabarit « Results ») avec l'intervalle de confiance de l'effet.

### 5.4 Spécification technique minimale

**Déjà en place dans le module en cours** (DA §9, `drapeaux.js`) et conforme à la demande : configuration `config.json` → `ab` avec `"actif": false` comme désactivation globale (variante `a` pour tous, aucun événement) ; attribution avant le premier rendu, stable par visiteur (`localStorage`, clé `ac_ab`) ; sans stockage, variante `a` et aucune mesure ; balisage `data-flag="nom" data-variant="a|b"` et attribut `data-ab-<nom>` sur `<html>`, feuille de style générée qui n'affiche que la variante attribuée ; forçage `?flag=nom:variante` (plusieurs, séparés par des virgules ; `?flag=reset`), un navigateur forcé ne mesure plus ; ordre des sections par déplacement dans le DOM ; événement Umami `exposition_variante` `{flag, variante}`.

**Écarts à combler** (nécessaires à une analyse valide) :

| # | Écart | Spécification |
|---|---|---|
| 1 | Exposition comptée « une fois par page vue » | **Une fois par visiteur et par drapeau** (`localStorage` `ac_ab_vus` : `{nom: variante}`). Sinon le dénominateur compte des pages vues et le numérateur des visiteurs : les proportions sont fausses. Propriétés : `flag`, `variante`, et `xp` = « hero-titre:b » (lecture directe dans l'interface Umami) |
| 2 | Exposition au chargement pour tous les drapeaux | Option `exposition` par drapeau : `"chargement"` ou un sélecteur (`"#demande"`) ; dans ce cas, IntersectionObserver, seuil 0,5, une seconde de visibilité. Analyse déclenchée du skill ab-testing : on ne compte que les visiteurs qui ont vu la zone |
| 3 | Do Not Track et GPC ignorés à l'attribution | Si `doNotTrack == "1"` ou `globalPrivacyControl` : variante `a`, rien n'est stocké, rien n'est mesuré (cohérent avec `suivi.js`) |
| 4 | Pas de réattribution quand une variante change | Champ `version` par drapeau ; le tirage stocké porte la version ; version différente = nouveau tirage et remise à zéro de `ac_ab_vus` pour ce drapeau |
| 5 | Pas de lien entre variante et conversion | Dans `suivi.js`, `s()` ajoute `f_<nom>` (tirets remplacés par des soulignés : `f_hero_titre: "b"`) aux événements `devis_clic`, `appel_clic`, `rappel_ouvert`, `formulaire_debut`, `formulaire_etape`, `formulaire_envoye`, `telechargement`, `intention_contact`, **pour les seuls drapeaux déjà exposés** à ce visiteur |
| 6 | Pas d'indicateur d'intention dédoublonné | Nouvel événement `intention_contact` : au premier `devis_clic`, `appel_clic`, `rappel_ouvert` ou `formulaire_debut` qui suit une exposition ; une fois par visiteur **et par drapeau** (`localStorage` `ac_ic`), avec les seules propriétés `f_` des drapeaux pas encore comptés |
| 7 | Qualité des demandes non observable | `formulaire_envoye` reçoit aussi `avec_message` (« oui » / « non »), `avec_fichiers`, `nb_travaux` : jamais de contenu saisi |
| 8 | Drapeaux manquants | Ajouter `aa-temoin` (A/A, aucun balisage), `entree-demande`, `etape3-allegee` ; `pages` par drapeau (`["index.html"]` ou `["*"]`) pour ne charger que les drapeaux utiles à la page |

Configuration cible d'un drapeau (format du module, avec les champs ajoutés) :
```json
"hero-titre": {
  "actif": false,
  "version": 1,
  "variantes": ["a", "b"],
  "poids": [50, 50],
  "pages": ["index.html"],
  "exposition": "chargement",
  "description": "A : « Placo, peinture, acoustique : la rigueur des chantiers publics » · B : « Du Conservatoire à votre salon : placo, acoustique, peinture »"
}
```

**Analyse.** Pour un drapeau X : `exposés(v)` = nombre d'`exposition_variante` avec `xp = X:v` ; `convertis(v)` = nombre d'`intention_contact` (ou de l'indicateur choisi) avec `f_X = v`. Les deux sont dédoublonnés par visiteur : ce sont des proportions. Test de deux proportions (test exact de Fisher sous 10 conversions par bras), intervalle de confiance à 95 %, contrôle SRM. Lecture dans l'interface Umami (propriétés d'événements) ou par requête sur la base auto-hébergée.

**Protection des données.** Ajouter à `confidentialite.html` une phrase sur la mémorisation locale de la variante (aucune donnée personnelle, aucun identifiant, refus par Do Not Track ou GPC), au titre de l'art. 45c LTC ; relecture avec `V02`. **Référencement** : même URL, aucune redirection, aucun traitement particulier des robots, tests limités dans le temps.

**Recette** : chaque variante par `?flag=` ; sans JavaScript (variante A) ; Do Not Track ; navigation privée de Safari ; lecteur d'écran (une seule variante lue) ; LCP et CLS mobiles inchangés ; une semaine d'`aa-temoin` sans écart de répartition avant XP1.

---

## 6. Coupes sur les autres pages

### 6.1 Gabarit des 4 pages services

| Section v2 | Décision | v3 |
|---|---|---|
| En-tête de page (chapeau, « En bref ») | **Raccourcir** | Chapeau de 20 mots au plus ; les 3 puces « En bref » deviennent 3 badges (§4.1) ; photo réelle ou illustration signalée |
| Ce que nous posons (4 H3 de 40 à 70 mots) | **Raccourcir** | 4 cartes : titre, 20 mots au plus, image ; ancres conservées (`#cloisons`, `#doublages`, `#faux-plafonds`, `#caissons`, `#correction` : cibles des redirections 301) |
| Pour qui ? | **Supprimer** | Une ligne « Professionnels » sous les cartes (CFC et lien) |
| Ce qu'il faut savoir (5 ou 6 points) | **Raccourcir** | 3 points de 15 mots ; le reste va dans la FAQ si la question n'y est pas déjà |
| Réalisations | **Remplacer** | « Références en {{service}} » : 1 mini-cas et une ligne de références (règle `C23` ci-dessous) |
| Bloc spécifique (guide, subventions) | **Garder, raccourcir** | 2 phrases et le bouton |
| Comment se passe un chantier (4 lignes) | **Raccourcir** | « Visite · Offre écrite · Chantier protégé · Réception » + lien « Notre méthode en détail » |
| FAQ (5 ou 6) | **Réduire** | 4 ou 5 questions |
| Demande | **Garder** | Liste courte au-dessus du bloc, badges en colonne (§7) |

**Mini-cas** (format commun, une fiche par page, rien d'inventé) : titre · « Lieu : … » · « Demande : … » `[C25]` (repli : ligne masquée) · « Ce que nous avons fait : … » (ce que montre la photo) · étiquettes de prestations · lien « Un projet semblable ? ».

**Ligne de références des pages services** : « Réalisé notamment pour : {{3 noms}} » **seulement si `C23` confirme** que ces maîtres d'ouvrage ont reçu ce service. Repli : liste canonique moyenne sous le titre générique « Ils nous ont confié des travaux ». En v2, le repli de la page acoustique (Conservatoire, HEAD, Alhambra) laissait croire à des travaux acoustiques chez eux : on le remplace par la liste canonique.

#### Placo (`placo.html`)

- **Chapeau** : « Diviser une pièce, redresser un mur, abaisser un plafond : les **plaques de plâtre** le font sans maçonnerie. »
- **Badges** : B4 (ou B11 si `C05`) · B3 · B1.
- **Cartes** :
  - « Cloisons » : « Une chambre, un bureau, une salle de réunion, montés en quelques jours. **Portes et renforts** prévus dès la pose. »
  - « Doublages » : « Un parement devant un mur abîmé, qui cache les gaines et peut recevoir un isolant contre le **froid** ou le **bruit**. » (liens conservés vers `cloisons-isothermes.html` et `isolation-acoustique.html`)
  - « Faux-plafonds » : « Il cache conduites et ventilation, reçoit **spots et gorges lumineuses**, et remplace un plafond abîmé. »
  - « Caissons et habillages » : « Une poutre ou une gaine à cacher : un **caisson** ajusté, avec trappe de visite si besoin. »
- **Ligne professionnels** : « Professionnels : lots **CFC 271 et 283**, offres sur plans et descriptifs. » `[À CONFIRMER C14 : CFC 283]` Repli : « lots **CFC 271** ». Lien « Espace professionnels ».
- **Ce qu'il faut savoir (3)** : poussière `C07` (texte v2) · coordination avec l'électricien · niveau de finition sur les grands murs. Retirés : salle de bains (FAQ 5), accord du bailleur ou de la PPE (FAQ 6).
- **Mini-cas** : P1 « Hall et couloirs : faux-plafond à gorge lumineuse » · « Lieu : Immeuble, canton de Genève » `[C25]` Repli : « Hall d'immeuble » · « Ce que nous avons fait : faux-plafond en plaques de plâtre aux formes courbes, éclairage et spots intégrés. » · Placo · Peinture `[C25]` Repli : Placo. Photo de chantier P3 en vignette.
- **FAQ (5)** : retirer « Peut-on fixer des meubles sur une cloison en placo ? » (réponse dans la carte « Cloisons »).

#### Peinture (`peinture.html`)

- **Chapeau** : « Un appartement à rafraîchir, une fin de bail, une cage d'escalier : nous **préparons les supports**, protégeons les lieux, puis peignons. »
- **Cartes** (illustrations signalées jusqu'au shooting `C40`) :
  - « Logements » : « Une pièce ou tout l'appartement, habité ou vide. Trous et fissures rebouchés **avant** la peinture. » `[C17]`
  - « Fins de bail » : « Remise en état entre deux locataires, prête pour l'**état des lieux d'entrée**. » `[C17]`
  - « Cages d'escalier » : « Par étages, **passage libre** pour les habitants. » `[C20]` Repli : « Par étages, dans les parties communes. »
  - « Bureaux et commerces » : « **Le soir ou le week-end**, pour ne pas fermer. » `[À CONFIRMER C19]` Repli : « Zone par zone, pour limiter la gêne. »
- La carte « Après nos travaux de placo » devient le badge B11 (`C05`), sinon disparaît.
- **Ce qu'il faut savoir (3)** : préparation sur une ligne de l'offre `C06` · fissure qui revient si la cause n'est pas traitée · intérieur seulement, pas de façades.
- **Mini-cas** : AA6 avant / après si sa qualité le permet `[À VÉRIFIER]` ; sinon section masquée (règle v2).

#### Isolation acoustique (`isolation-acoustique.html`)

- **Garder** « Isoler ou corriger » (aucun concurrent ne l'explique), en deux colonnes :
  - « **Isoler** » : « Empêcher le bruit de passer d'un local à l'autre : voisin, étage, pièce d'à côté. »
  - « **Corriger** » : « Réduire l'écho dans la pièce : salle de réunion, réfectoire, salle communale. »
  - Sous les colonnes : « À la visite, nous commençons par identifier ce que vous entendez. »
- **Cartes (4)** : doublage acoustique `C18`, faux-plafond acoustique, cloison acoustique, correction des salles `C18` (textes v2 ramenés à 20 mots).
- **Ce qu'il faut savoir (3)** : bruits de pas traités à la source · le bruit passe aussi par les côtés · aucune promesse en décibels sans mesure `C15`.
- **Guide** : « Ce qui marche, ce qui ne marche pas, et les questions à poser à toute entreprise. 8 pages. » + bouton v2.
- **Mini-cas** : P6 « Correction acoustique d'une salle » · « Ce que nous avons fait : panneaux muraux et plafond perforé contre l'écho. » `[C18, C25]`.
- **Références** : proposé pour `C23` : Conservatoire de musique de Genève · HEAD – Genève · Salle communale de Collonge-Bellerive ; repli : liste canonique moyenne.

#### Cloisons isolantes (`cloisons-isothermes.html`)

- **Chapeau** : « Une chambre au-dessus du garage, un bureau contre une cave, des combles : la cloison isolante garde la chaleur **côté chauffé**. » + phrase de filtre « Nous ne posons pas de chambres froides. » `[C16]`
- **Pour qui ?** supprimé. **Ce qu'il faut savoir (3)** : humidité vérifiée d'abord · pare-vapeur côté chauffé · protection incendie entre garage et logement `C15`.
- **Subventions** : « Certaines isolations thermiques peuvent être subventionnées. La demande se dépose **avant** les travaux, auprès du service de l'énergie de votre canton. » (`C43` pour la phrase sur les informations fournies.)
- **Mini-cas** : AA3 « Combles : isolation et rampant fini sous une fenêtre de toit » (avant / après) `[À VÉRIFIER : qualité]` `[C26]`.

### 6.2 Professionnels (`professionnels.html`)

| Section | Décision | Texte de remplacement |
|---|---|---|
| En-tête | **Raccourcir** | Chapeau : « Immeubles habités, bureaux et bâtiments publics, **depuis 2007**. Offres sur plans et descriptifs. » `[C20]` Repli : « Bureaux, logements et bâtiments publics, **depuis 2007**. Offres sur plans et descriptifs. » Badges : B1, B5 (+ B8 `C12`, B10 `C13`) |
| Références complètes (`#references`) | **Remonter** en section 2 | Grille par secteur en cellules (règles du §2.3), puis la bande des chiffres. Ancre conservée (redirection 301 de `/realisations/references`) |
| Ce que nous vous apportons | **Raccourcir** (20 mots par carte) | Régies : « Remises en état, cages d'escalier, plafonds après dégât d'eau. **Parties communes protégées**, date convenue tenue. » `[C20]` Repli : sans « date convenue tenue ». · Architectes : « Lots **CFC 271, 283 et 285**. Offres complètes sur descriptif, variantes à part, questions posées avant de chiffrer. » `[C14]` · Communes : « La Ville de Genève, Plan-les-Ouates et Collonge-Bellerive nous ont confié des travaux. Interventions pendant les **vacances scolaires**. » `[C19]` Repli : sans la 2e phrase. · Entreprises : « Cloisons, salles de réunion plus calmes, peinture : **le soir ou le week-end**. » `[C19]` Repli : « zone par zone » |
| Méthode en site occupé (8 points) | **Raccourcir à 6** `[C20, C07, C06, C09, C32]` | 1 « Avis aux locataires et horaires convenus, affichés quelques jours avant. » · 2 « Parties communes, ascenseur et sols protégés dès le premier jour. » · 3 « Poussière contenue, nettoyage chaque soir, passages libres. » · 4 « Un responsable de chantier nommé, joignable. » · 5 « Un imprévu est chiffré avant d'être exécuté. » · 6 « Réception avec photos et liste des retouches. » |
| Nouveau : mini-cas public | **Ajouter** | Carte typographique « Salle communale de Plan-les-Ouates » · « Collectivité » · « Travaux : {{nature}}, {{année}} » `[C22]` Repli : ligne masquée |
| Lots, normes et documents | **Garder** | Normes en une ligne : « Performances acoustiques, thermiques et incendie : celles du projet (SIA 181, SIA 180, AEAI), précisées dans l'offre. » `[C15]` Repli : « Les performances visées sont celles du projet, précisées dans l'offre. » |
| Soumission | **Garder** | Texte v2 ; la phrase sur la visite d'un chantier en cours reste `[C40]` |
| Témoignage professionnel | **Ajouter, masqué** | Une citation d'un maître d'ouvrage ou d'un architecte (`C44`) |

### 6.3 L'entreprise (`entreprise.html`)

| Section | Décision | Remplacement |
|---|---|---|
| Notre histoire | **Garder** ; la phrase sous la frise devient la liste courte de références | — |
| Notre métier (citation du registre) | **Raccourcir** : citation et source seulement | Paragraphe d'explication supprimé (`C05`) |
| Ce qui guide notre travail (4 cartes) | **Supprimer** | Doublon de la méthode et de l'engagement |
| Notre méthode | **Garder** (version complète) | — |
| Ajout : chiffres clés | **Ajouter** | Bande du §2.2 H5 |
| Vérifiez qui nous sommes | **Garder**, avec les badges du §4.1 | — |
| Si un défaut apparaît | **Raccourcir** | Visible : « Appelez-nous dès que vous le constatez : nous venons voir. » `[C32]` · texte légal v2 dans un repli « Ce que dit la loi » `[V01]` |
| Bande d'appel | **Garder**, liste courte au-dessus des boutons | — |

### 6.4 Réalisations (`realisations.html`)

| Section | Décision | Remplacement |
|---|---|---|
| En-tête | **Raccourcir** | H1 « Réalisations et références » ; chapeau « Nos chantiers, photographiés pendant et après les travaux. » ; mention « Toutes les photos sont nos propres réalisations. » `[C25]` |
| Nouveau : lieux de référence | **Ajouter** en tête | Les 4 cartes de lieux du §2.2 H4 et le lien « Voir les {{n}} références » |
| Projets | **Garder** ; le bouton répété 8 fois devient un lien | Sous chaque fiche : lien « Un projet semblable ? » (même cible pré-remplie `contact.html?travaux=…#demande`) |
| Avant, après (7 paires) | **Raccourcir** | 3 paires visibles (AA5, AA6, AA3), bouton « Voir les 4 autres » ; paires faibles non publiées `[À VÉRIFIER]` |
| Ligne de références | **Remplacer** | Grille de cellules du mur (sans défilement) |
| Votre projet | **Garder** | + badges B1, B3, B4 |

### 6.5 Contact (`contact.html`)

| Section | Décision | Remplacement |
|---|---|---|
| Pour préparer votre demande (5 points) | **Supprimer** | Déjà sur la page merci (« Pour gagner du temps ») |
| Colonne gauche | **Garder** : téléphone d'abord sur mobile, puis formulaire | + badges B1, B3, B9 (sinon B4) à côté du formulaire |
| Ligne de références | **Garder** | Liste canonique moyenne, règles du §2.3 |
| Zone | **Raccourcir** | Introduction : « Depuis Carouge, dans toute la Suisse romande. » ; liste des cantons conservée en texte (accessibilité) ; la phrase « Villes marquées sur la carte… » devient une liste |

---

## 7. Formulaire

API, noms de champs et valeurs **inchangés** (`contrat-interface.md`) ; seuls les libellés, l'ordre d'affichage, les regroupements et la réassurance changent. Les messages d'erreur restent ceux de l'API (§8 du contrat).

### 7.1 Ordre des champs et microcopie

| Étape | Ordre v3 | Libellés et aides v3 | Changement |
|---|---|---|---|
| En-tête du bloc | — | H2 « Demander un devis » · « **3 étapes**, environ **une minute**. » (pages services : « Encore 2 étapes, moins d'une minute. ») | Phrase « Nous vous rappelons… » déplacée en étape 3 |
| 1 · Quels travaux ? | `travaux[]` | Cartes v2 inchangées · aide « Plusieurs choix possibles. » · bouton « Continuer : votre projet » | Aide raccourcie |
| 2 · Votre projet | 1 `type_client` · 2 `commune` · 3 `delai` · 4 `surface` | « Vous êtes » avec deux sous-titres visuels : « Particulier » (Propriétaire (maison, appartement, PPE) · Locataire) et « Professionnel » (Régie, gérance ou coopérative · Architecte, bureau d'études ou entreprise générale · Commune ou institution · Entreprise, bureau ou commerce). Mêmes valeurs, même `name`. · Sous le bouton : « Ces réponses nous aident à préparer la visite. » | 6 choix lus comme 2 groupes (loi de Hick) ; raison donnée (effet « parce que ») |
| 3 · Vos coordonnées | 1 `civilite` (en ligne) · 2 `nom` · 3 groupe « Comment vous joindre ? » (`telephone`, `email`) · 4 `preference_contact` (+ `creneau`) · 5 sous-titre « Si vous le souhaitez » : `message`, `fichiers[]` · 6 `connu_par` (+ `recommande_par`) | Groupe : légende « Comment vous joindre ? » + aide « Un des deux suffit. » ; « Téléphone » · « Pour vous rappeler et convenir de la visite. Exemple : 079 123 45 67. » ; « E-mail » · « Pour la confirmation et l'offre écrite. » · Fichiers : aide du contrat §7 (« JPG, PNG, HEIC ou PDF, 3 fichiers de 8 Mo au plus. Trop lourd ? Envoyez-les par e-mail après notre appel. ») · bouton « Envoyer ma demande » | Remplace les mentions « obligatoire si pas d'e-mail » et « si pas de téléphone » ; facultatifs regroupés en fin d'étape |

Aucun bouton radio présélectionné, aucune case de consentement (D2), « Retour » conserve la saisie, brouillon en `sessionStorage` (v2 inchangé).

### 7.2 Réassurance adjacente

La v2 plaçait 3 lignes sous tout le formulaire, loin du bouton de l'étape 3. En v3, une ligne sous le bouton de chaque étape, plus la colonne :

| Où | Texte | Marqueur |
|---|---|---|
| Sous « Continuer : votre projet » | « La visite et le devis sont gratuits et sans engagement. » | `[À CONFIRMER C02]` Repli : « Vous décidez une fois l'offre écrite reçue. » |
| Sous « Continuer : vos coordonnées » | « Ces réponses nous aident à préparer la visite. » | aucun |
| Sous « Envoyer ma demande » | « Nous vous rappelons le jour même ou le jour ouvrable suivant. » puis la mention d'information v2 (inchangée, lien « Protection des données ») | `[À CONFIRMER C01]` Repli : « Nous vous rappelons pendant nos heures de bureau. » |
| Colonne (ordinateur), sous le formulaire (mobile) | Téléphone et horaires `C03` · badges B1, B3, B4 · premier témoignage s'il existe | — |
| Au-dessus du bloc | Bande défilante des références (§2.2 H9) ; sur les pages sans bande, liste courte | — |

### 7.3 Mobile et comportements

- Quand le bloc `#demande` est visible à 30 % ou plus, la barre fixe masque « Demander un devis » et affiche « Appeler le +41 22 771 20 15 » sur toute sa largeur : pas de second bouton de devis devant le formulaire, et le bouton du formulaire n'est jamais recouvert. `scroll-padding-bottom` égal à la hauteur de la barre (WCAG 2.4.11, focus jamais masqué).
- Erreurs : récapitulatif « {{n}} points à compléter » en haut de l'étape, avec des liens vers les champs ; messages de l'API sous chaque champ ; saisie jamais effacée (v2).
- Étape 1 : la carte choisie se coche avec une transition de 150 ms ; pas de passage automatique à l'étape suivante.
- Pré-remplissage depuis une page service ou `?travaux=` : inchangé.

### 7.4 Mesure

Événements v2 inchangés (`formulaire_debut`, `formulaire_etape`, `formulaire_erreur`, `formulaire_envoye`) ; ajout des propriétés `avec_message`, `avec_fichiers`, `nb_travaux` sur `formulaire_envoye` et des propriétés `f_<drapeau>` (§5.4). Abandon par étape = `formulaire_etape` (2, puis 3) rapporté à `formulaire_debut`, suivi dès le rodage.

---

## Annexe · Points à faire valider (identifiants existants)

| Point | Identifiant | Repli |
|---|---|---|
| Afficher « Salle communale de Plan-les-Ouates » au lieu de « Mairie de Plan-les-Ouates » | `C22` | Nom v2 |
| Rattacher des photos à des lieux : P8 = Salle de l'Alhambra ? P2 = salle communale de Plan-les-Ouates ? P6 ou P7 = Conservatoire ? | `C25` | Cartes typographiques |
| Nature et année des travaux pour les 4 lieux de référence | `C22` | Ligne « Travaux » masquée |
| Accord de l'OMC pour son nom (le chiffre passe de 17 à 18) | `C22`, D4 | 17, OMC absente |
| Illustrations sous licence (peinture, acoustique, cloisons) jusqu'au shooting | `C40`, décision client | Cartes sans image |
| Mémorisation locale de la variante de test, dans la politique de confidentialité | `V02` | Tests non lancés |
| Confirmations qui complètent les badges : visite gratuite, GGE, assurance, délai de rappel | `C02`, `C11`, `C12`, `C01` | 3 badges dans le héro |
| Écarts avec la DA (§2.5) et activation des drapeaux (§5.3) | Chef de projet | Recommandations de ce document |
