# Personas, parcours de décision et leviers psychologiques

*Andy Construct · Site v2 · Base comportementale pour le copywriting, l'ergonomie et le CRO · 31 octobre 2026*

Ce document sert au copywriter, à l'architecte CRO, à l'ingénieur automatisation et au développeur frontend. Il dit **qui** visite le site, **ce qui le fait hésiter**, **ce qui le décide**, et **comment le site et les automatisations doivent répondre**, sans manipulation.

---

## L'essentiel en 12 points

1. **Deux logiques d'achat.** Les professionnels (régie, architecte, commune, PME) achètent de la **fiabilité** et doivent **justifier leur choix** à quelqu'un d'autre : propriétaire, maître d'ouvrage, exécutif communal. Les particuliers de 55 à 70 ans achètent de la **confiance** : ils vont laisser des inconnus entrer chez eux. Le site sert les deux avec une seule page d'accueil et deux portes d'entrée nettes.
2. **La peur n° 1 n'est pas le prix, c'est l'imprévisible** : retard, supplément, poussière, entreprise injoignable. Le message central est donc la **prévisibilité** : méthode, offre détaillée, délai annoncé et tenu, interlocuteur nommé.
3. **Le téléphone reste le canal de conversion principal** des particuliers et des régies. Un appel non décroché est une demande perdue. Le répondeur, le renvoi d'appel et le délai de rappel font partie du « site ».
4. **La vitesse de réponse est le levier le plus rentable** : une demande traitée dans l'heure a beaucoup plus de chances d'aboutir (Harvard Business Review, 2011 [30]). Accusé de réception automatique immédiat, puis rappel humain rapide (délai à confirmer).
5. **Les grandes références (Ville de Genève, OMC, UBS…) rassurent les professionnels mais peuvent intimider les particuliers** (« trop gros pour moi »). Il faut les contrebalancer par des références locales et un message explicite sur les petits chantiers [à confirmer].
6. **Preuve sociale répétée, avec mesure** : trois expositions par page au maximum (plus une ligne discrète en pied de page), jamais deux dans le même écran, toujours la même liste courte, toujours vraie. La répétition rend aussi les affirmations fausses plus crédibles [43] : c'est une responsabilité.
7. **Vérifier vaut mieux qu'affirmer.** Lien vers le registre du commerce, IDE, adresse, ligne fixe, visages réels. Les personnes de 55 ans et plus perdent environ **675 millions de francs par an** en abus financiers en Suisse [11] : pour elles, la vérifiabilité est la preuve la plus forte.
8. **Peu de choix par écran** : 4 services, 1 bouton principal et 1 bouton d'appel. Les personnes âgées souhaitent environ **deux fois moins d'options** [7], et chaque option supplémentaire leur coûte plus de temps [6].
9. **Formulaire** : court, première question facile (type de travaux), champs facultatifs marqués, raison donnée pour chaque donnée, erreurs claires, aucune saisie perdue.
10. **Soigner les fins (règle pic-fin)** [50]. En ligne : page de remerciement et e-mail avec visage, nom, prochaine étape et délai. Sur le chantier : nettoyage, réception, remerciement. C'est à ce moment qu'on demande un avis.
11. **Interdits** : fausse urgence, faux avis, fenêtres surgissantes, cases pré-cochées, liens raccourcis dans les SMS, relances insistantes, culpabilisation. Ils sont contraires à la LCD et font fuir ce public.
12. **Tests A/B** : le trafic sera faible. Tester d'abord les micro-conversions, un test à la fois, et ne jamais tester une variante malhonnête.

---

## 0. Méthode, niveau de preuve et conventions

**Sources utilisées.** Documents du projet (`programme-v2.md`, `brief-design.md`, `justification.md`, `analyse-marche.md`, `contenus-a-valider.md`). Recherche UX publiée (Nielsen Norman Group, Baymard Institute, W3C). Psychologie sociale et cognitive (articles évalués par des pairs). Sources suisses (Pro Senectute, OFS, OFCS, droit fédéral, achats publics). Liste complète en fin de document ; les numéros entre crochets y renvoient.

**Limite principale.** Aucun entretien avec de vrais clients d'Andy Construct n'a encore eu lieu. Les cinq personas sont des **proto-personas** : des hypothèses argumentées, à confirmer en deux semaines (section 9). Beaucoup d'études citées sont américaines ou faites en laboratoire : elles donnent un **sens et un ordre de grandeur**, pas une vérité pour Genève. D'où les tests de la section 7.

**Conventions.**
- **[à confirmer]** : fait que seul le client peut confirmer. Tant qu'il ne l'a pas fait, la phrase ne part pas en production (programme, §4).
- **(hyp.)** : hypothèse comportementale, à vérifier en entretien ou par la mesure.
- Les prénoms des personas sont fictifs. C'est un outil de travail interne, jamais publié sur le site.

---

## 1. Personas

### 1.0 Vue d'ensemble

| | P1 Régie | P2 Architecte | P3 Commune / institution | P4 Propriétaire 55-70 | P5 PME / commerce |
|---|---|---|---|---|---|
| **Ce qu'il achète vraiment** | Sa tranquillité face aux locataires et au propriétaire | Une entreprise qui le fait bien paraître devant son maître d'ouvrage | Un chantier défendable : procédure, délai, sécurité | De la confiance : quelqu'un d'honnête chez soi | Zéro interruption de son activité |
| **Qui décide** | Le gérant, avec l'accord du propriétaire au-delà d'un certain montant | Le maître d'ouvrage, sur recommandation de l'architecte | L'exécutif (Conseil administratif, Municipalité) ou la direction, selon la procédure | Le couple ; l'assemblée de PPE pour les parties communes | Le gérant ; la régie s'il est locataire |
| **Déclencheur n° 1** | Remise en état entre deux locataires ; dégât d'eau | Lot CFC 271/283/285 à mettre en soumission | Travaux d'été dans une école ou une salle | Bruit des voisins, appartement à repeindre, fissures | Déménagement ou réaménagement |
| **Peur n° 1** | Plaintes des locataires et retard | Suppléments et défauts à la réception | Retard à la rentrée, procédure contestée | Être trompé ; la poussière | Fermer, perdre des clients |
| **Preuve décisive** | Réactivité démontrée, méthode « site occupé » | Fiches projets techniques | Références publiques et attestations | Visage, voix, avis, références locales | Délai tenu, travaux hors des heures d'ouverture |
| **Canal préféré** | Téléphone, puis e-mail | E-mail (dossier), téléphone | E-mail formel | Téléphone, puis visite | Téléphone, formulaire avec photos |
| **Valeur commerciale (hyp.)** | Récurrente (portefeuilles d'immeubles) | Moyenne à élevée, par projet | Élevée, récurrente au rythme des budgets | Faible à moyenne, fort bouche-à-oreille | Moyenne |

### 1.1 P1 — Marc, 48 ans, gérant technique dans une régie

*Il gère l'entretien d'environ 1'500 logements et quelques arcades à Genève. Son téléphone sonne toute la journée : locataires, concierges, propriétaires, entreprises. Il a trois ou quatre entreprises « de confiance » par métier et n'en cherche une nouvelle que lorsqu'une le déçoit ou est débordée.*

**Contexte.** Il agit pour le compte de propriétaires : particuliers, caisses de pension, PPE dont la régie est l'administrateur. Il fait les états des lieux de sortie, commande les remises en état, gère les sinistres avec les assurances et répond aux plaintes. Il est jugé sur deux choses : les locataires ne se plaignent pas, le propriétaire ne découvre pas de mauvaise surprise.

**Objectif.** Faire exécuter le travail **à la date prévue, au prix annoncé, sans plainte des locataires et sans devoir surveiller l'entreprise**.

**Déclencheurs.**
- Changement de locataire : remise en état (peinture, rebouchage, plafond) dans une fenêtre courte. Chaque jour de vacance est un loyer perdu.
- Dégât d'eau ou sinistre : plafond ou cloison à refaire, souvent avec un expert d'assurance (hyp.).
- Plainte de bruit entre locataires : isolation acoustique.
- Transformation d'une arcade ou d'un bureau pour un nouveau locataire commercial.
- Entreprise habituelle indisponible ou décevante. **C'est le moment où il cherche ailleurs.**
- Propriétaire qui exige plusieurs offres pour comparer (pratique courante).

**Critères de choix (classés).**
1. Réactivité : rappel rapide, visite rapide, offre rapide.
2. Délai annoncé et tenu.
3. Savoir travailler en **site occupé** : propreté, horaires, politesse avec les locataires, protection des parties communes.
4. Offre claire, par poste, **comparable** à celle des concurrents.
5. Qualité de finition, pour éviter un second passage.
6. Un interlocuteur unique, joignable sur son portable.
7. Facture conforme à l'offre, sans supplément non annoncé.
8. Sérieux administratif : assurance responsabilité civile, pas de travail au noir. Le risque de réputation retombe sur la régie.

**Peurs et objections.**
- « Ils vont prendre du retard et le nouveau locataire va entrer dans un chantier. »
- « La poussière et le bruit vont générer des plaintes. » Le locataire peut demander une réduction de loyer pendant les travaux (art. 259d et 260 CO [54]).
- « On va découvrir des plus-values au décompte et je devrai les justifier au propriétaire. »
- « Ce ne sera pas leur équipe, mais un sous-traitant que je ne connais pas. »
- « Une fois la commande passée, plus personne ne répond. »
- « Les finitions seront à reprendre et il faudra revenir. »
- « Ils vont abîmer l'ascenseur ou la cage d'escalier. »

**Ce qui le rassure.** Un délai de rappel annoncé **et tenu dès le premier contact**. Une méthode « site occupé » écrite : avis aux locataires, horaires, protections, nettoyage quotidien. Des références de régies ou d'immeubles (avec autorisation). Une offre lisible par le propriétaire. Un nom et un portable. Des photos avant/après pour son rapport au propriétaire.

**Appareils et moments.** Ordinateur au bureau tôt le matin (7 h 30 – 9 h) et en fin d'après-midi, pour les offres et les commandes. Téléphone entre deux visites d'immeubles, pour une recherche rapide ou une urgence.

**Canal préféré.** **Téléphone** pour le premier contact et les urgences. **E-mail** pour envoyer photos et bons de commande et recevoir l'offre en PDF. Formulaire rarement, sauf pour une demande non urgente avec photos.

**Ses mots.** « régie », « gérance », « immeuble », « locataire(s) », « appartement vacant », « remise en état », « rafraîchissement », « état des lieux de sortie », « bon de commande », « bon de travaux », « offre », « délai », « intervention », « dégât d'eau », « sinistre », « concierge », « parties communes », « propriétaire » ou « mandant », « plus-value », « facture ». Attention : **« en régie »** veut aussi dire « facturé au temps passé » (voir 1.6).

**En 10 secondes, il veut voir.** Les travaux qu'il commande (remise en état, plafonds, cloisons, peinture) ; sa zone ; un numéro cliquable ; une preuve de sérieux (références, depuis 2007) ; un délai.

**À qui il rend des comptes.** Au propriétaire et à sa direction. **Il doit pouvoir justifier son choix** : le site et l'offre doivent l'y aider.

**Sa phrase (hyp.).** « Je n'ai pas besoin du moins cher. J'ai besoin de quelqu'un qui vient quand il dit et qui ne me fait pas rappeler par les locataires. »

### 1.2 P2 — Sophie, 42 ans, architecte cheffe de projet

*Elle travaille dans un bureau de douze personnes à Lausanne et mène des projets à Genève et sur la Côte. Elle prépare les soumissions, invite des entreprises, compare les offres, recommande l'adjudication au maître d'ouvrage, puis dirige les travaux.*

**Contexte.** Comme la plupart des acheteurs professionnels, elle fait l'essentiel de son évaluation seule, sur les sites et les documents, avant tout contact [29]. Sa réputation auprès du maître d'ouvrage dépend des entreprises qu'elle recommande. Une entreprise qui sous-chiffre puis multiplie les suppléments, ou qui retarde les autres corps de métier, la met en difficulté.

**Objectif.** Inviter des entreprises qui rendent une **offre complète, conforme au descriptif, dans le délai**, puis exécutent proprement et se coordonnent avec les autres corps de métier.

**Déclencheurs.**
- Phase de soumission d'un projet : il lui faut 3 à 5 entreprises par lot (CFC 271 plâtrerie, 283 faux-plafonds, 285 peinture).
- Entreprise habituelle qui décline ou est surchargée.
- Besoin spécialisé : acoustique (SIA 181), cloisons coupe-feu (EI30), salle de musique ou de spectacle.
- Petit projet privé pour lequel elle veut une seule entreprise de plâtrerie-peinture fiable.
- Recherche Google ou question posée à une IA (« entreprise plâtrerie faux-plafond acoustique Genève »). Les IA touchent surtout les architectes plus jeunes ([analyse marché, §2.6]).

**Critères de choix (classés).**
1. Compétence technique : détails, acoustique, protection incendie, niveau de finition (on parle souvent de Q3 ou Q4 pour les plaques de plâtre, à vérifier avec le client).
2. Respect des délais et coordination de chantier : présence aux rendez-vous, chef d'équipe stable.
3. Offre complète et **plausible**, sans réserves cachées, avec les variantes à part. Les marchés publics évaluent d'ailleurs la plausibilité de l'offre et la fiabilité du prix [61].
4. Références **comparables** : même type de bâtiment, même exigence.
5. Capacité réelle : taille d'équipe, disponibilité aux dates du planning.
6. Proactivité : signale tôt un problème dans les plans, propose une variante.
7. Prix.
8. Conformité administrative pour les projets publics : attestations, convention collective.

**Peurs et objections.**
- « Ils sous-chiffrent pour gagner, puis se rattrapent sur les plus-values. »
- « Ils prennent du retard et bloquent l'électricien et le peintre. »
- « Les joints se verront sous la lumière rasante : réception difficile, liste de retouches sans fin. »
- « Sous-traitance non annoncée ; le chef d'équipe change toutes les semaines. »
- « Performance acoustique ou incendie non atteinte : c'est ma responsabilité qui est en jeu. »
- « L'entreprise fait faillite en plein chantier. »
- « Au téléphone, personne ne comprend mes questions techniques. »

**Ce qui la rassure.** Des **fiches projets techniques** : type de bâtiment, lot, système posé, contraintes, délai, année. Des références nommées dans des bâtiments exigeants (Conservatoire, HEAD, Salle de l'Alhambra : crédibles pour l'acoustique). Le vocabulaire juste (CFC, SIA 118, SIA 181, AEAI « selon les exigences du projet »). Des photos de chantier en cours : ossature, suspentes, ce qui est caché sous la finition. Un dossier de références en PDF téléchargeable sans formulaire. Un accusé de réception rapide quand elle envoie un dossier de soumission.

**Appareils et moments.** Grand écran au bureau, aux heures de bureau. Elle lit des PDF et compare plusieurs onglets. Téléphone sur le chantier.

**Canal préféré.** **E-mail** avec plans et descriptifs (fichiers lourds, liens de transfert). **Téléphone** pour les questions. Le formulaire seulement pour un premier contact. Elle veut l'adresse directe de la personne responsable.

**Ses mots.** « soumission », « appel d'offres », « descriptif », « métré », « série de prix », « CFC 271, 283, 285 », « plâtrerie », « gypserie », « faux-plafond », « doublage », « cloison », « EI30 », « SIA 118 », « SIA 181 », « isolation acoustique », « correction acoustique », « niveau de finition », « direction des travaux », « rendez-vous de chantier », « PV », « plus-value », « avenant », « réception », « liste des retouches », « décompte final », « maître d'ouvrage », « corps de métier », « CVSE », « planning ».

**En 10 secondes, elle veut voir.** Les lots couverts, dans son vocabulaire (CFC) ; des références sérieuses dans des bâtiments comparables ; une entreprise établie (depuis 2007, registre) ; **où envoyer un dossier de soumission**.

**À qui elle rend des comptes.** Au maître d'ouvrage. Elle doit **défendre sa recommandation** dans un comparatif d'offres.

**Sa phrase (hyp.).** « Une entreprise qui me pose les bonnes questions avant de chiffrer, c'est une entreprise qui ne me fera pas de surprise au décompte. »

### 1.3 P3 — Jean-Luc, 55 ans, responsable du service des bâtiments d'une commune

*Commune genevoise de 12'000 habitants : écoles, crèches, salle communale, administration, une quarantaine de bâtiments. Le même profil existe dans une haute école, une fondation, un EMS ou une organisation internationale.*

**Contexte.** Il gère un budget d'entretien annuel et des crédits d'investissement votés par le conseil municipal. Il applique les règles des marchés publics. À Genève, pour le second œuvre, le **gré à gré est possible sous CHF 150'000** et la **procédure sur invitation entre 150'000 et 250'000** [59]. Les nouvelles règles intercantonales (AIMP 2019 ; le Conseil d'État genevois a adopté un projet de loi d'adhésion en avril 2025, état à vérifier) parlent d'« offre la plus avantageuse » et imposent de juger **la qualité en plus du prix** [58]. Il travaille sous le regard de l'exécutif, des élus et du public, avec un risque de recours. Ses fenêtres de travaux sont fixes : **vacances scolaires**, salle libre entre deux manifestations.

**Objectif.** Un chantier **terminé dans la fenêtre, conforme, dans le crédit, avec une procédure inattaquable**, et sans gêne ni danger pour les utilisateurs (élèves, personnel, public).

**Déclencheurs.**
- Entretien planifié au budget ; travaux d'été dans les écoles.
- Plaintes d'acoustique dans une classe, une crèche ou une salle polyvalente.
- Mise en conformité incendie : sujet sensible depuis l'incendie de Crans-Montana, la révision des prescriptions AEAI est attendue vers l'automne 2027 ([analyse marché, §2.4]).
- Transformation de locaux pour un nouvel usage ; sinistre.
- Besoin de nouvelles entreprises à consulter pour un gré à gré ou une invitation.
- Insatisfaction envers l'entreprise actuelle.

**Critères de choix (classés).**
1. **Conformité administrative** : attestations sociales et fiscales à jour (AVS, LPP, LAA, impôt à la source), engagement à respecter les usages (OCIRT) ou convention collective à Genève [60]. Une pièce manquante peut être éliminatoire.
2. Références **publiques** comparables : autres communes, écoles, salles.
3. **Respect absolu du délai** : la rentrée scolaire ne se déplace pas.
4. Qualité et sécurité : normes, sécurité dans un bâtiment public occupé, enfants.
5. Prix, dans le cadre de l'« offre la plus avantageuse » (qualité et prix).
6. Présence régionale et réactivité pour le service après-vente.
7. Durabilité et formation d'apprentis, parfois prises en compte dans les critères.

**Peurs et objections.**
- « Le chantier n'est pas fini à la rentrée et ça remonte jusqu'au Conseil administratif. »
- « La procédure est contestée parce qu'une pièce manquait. »
- « Un sous-traitant emploie des travailleurs non déclarés et la commune se retrouve dans la presse. »
- « Dépassement de crédit : il faudra demander un crédit complémentaire. »
- « Un accident avec un enfant ou un usager. »
- « L'entreprise disparaît avant la fin du délai de garantie. »

**Ce qui le rassure.** Des noms de collectivités : Ville de Genève, Mairie de Plan-les-Ouates, salle communale de Collonge-Bellerive. Une identité juridique complète (raison sociale, IDE, inscription au registre depuis 2007). La mention « Attestations sociales et fiscales à jour sur demande » [à confirmer]. Un dossier de références en PDF organisé comme des critères d'aptitude. Une méthode pour les bâtiments publics occupés : horaires, sécurité, signalisation, nettoyage. La capacité de travailler pendant les vacances scolaires [à confirmer]. Un interlocuteur nommé.

**Appareils et moments.** Ordinateur au bureau, de 7 h 30 à 16 h 30. Il imprime et transmet à ses collègues. Réseau informatique de l'administration. Téléphone lors des visites de bâtiments.

**Canal préféré.** **E-mail** : formel et traçable. Téléphone pour un renseignement préalable. Pour les gros marchés, la procédure officielle (simap.ch, FAO). Le formulaire du site très rarement.

**Ses mots.** « service des bâtiments », « service technique », « maître d'ouvrage public », « bâtiments communaux », « entretien », « crédit d'investissement », « crédit d'engagement », « budget de fonctionnement », « Conseil administratif » (GE), « Municipalité » (VD), « conseil municipal », « gré à gré », « procédure sur invitation », « procédure ouverte », « appel d'offres », « simap », « FAO », « soumission », « cahier des charges », « critères d'aptitude », « critères d'adjudication », « attestations », « CFC », « vacances scolaires », « utilisateurs », « concierge », « AEAI », « sécurité ».

**En 10 secondes, il veut voir.** Des références publiques ; une entreprise juridiquement solide ; les lots CFC couverts ; comment obtenir rapidement le dossier et les attestations ; la zone.

**À qui il rend des comptes.** À l'exécutif communal, aux élus et au public. **Tout doit pouvoir être justifié par écrit.**

**Sa phrase (hyp.).** « Je ne peux pas me permettre une entreprise sympathique mais sans attestations. Et je ne peux pas me permettre une entreprise en règle qui livre en septembre. »

### 1.4 P4 — Françoise, 64 ans, et Bernard, 67 ans, propriétaires

*Ils possèdent un 5 pièces en PPE à Lancy (ou une villa à Collonge-Bellerive). Bernard est retraité, Françoise le sera bientôt. Ils ont du temps, de l'épargne, et beaucoup de prudence.*

**Contexte.** Ils rénovent pour leur confort, pour rester longtemps dans leur logement, pour préparer une vente ou parce que les enfants sont partis. En PPE, les parties communes passent par l'administrateur et l'assemblée des copropriétaires (art. 647c à 647e et 712g CC [56]). Ils ont entendu parler de faux artisans et d'arnaques. Pro Senectute estime que **78 % des 55 ans et plus ont subi une tentative d'abus financier en cinq ans**, et que les montants les plus élevés concernent les situations de **dépendance envers des professionnels** ou des proches [11]. Ils lisent tout, comparent, demandent l'avis d'un voisin ou d'un enfant.

**Objectif.** Un travail **bien fait, propre, à un prix juste et tenu**, par des gens à qui ils peuvent confier leurs clés.

**Déclencheurs.**
- Bruit des voisins (« on entend tout ») : isolation acoustique.
- Fissures ou plafond abîmé après un dégât d'eau.
- Appartement à repeindre (« ça fait vingt ans »).
- Transformation : créer une chambre ou un bureau avec une cloison.
- Pièce froide à isoler : sous-sol, combles (cloisons isothermes : définition à confirmer, voir `contenus-a-valider.md`).
- Recommandation d'un voisin ou de l'administrateur de PPE ; camionnette ou chantier aperçu dans le quartier.

**Critères de choix (classés).**
1. **Confiance perçue** : l'impression au premier appel et à la visite (« ils ont l'air sérieux »).
2. **Propreté et respect du logement** : poussière, protections, meubles.
3. **Prix clair, ferme, sans surprise**, TVA comprise.
4. Qualité de finition.
5. Quelqu'un qui **écoute et explique**, sans jargon.
6. Recommandations : bouche-à-oreille, avis Google.
7. Ponctualité : « ils viennent quand ils disent ».
8. Proximité : une entreprise établie dans la région.

**Peurs et objections.**
- « Et si c'était une arnaque ? On nous demandera un acompte en liquide. »
- « Le prix va gonfler en cours de route. »
- « Du plâtre partout, des meubles abîmés. »
- « Ils commencent, puis disparaissent sur un autre chantier. »
- « Des inconnus différents chez nous chaque jour. »
- « Je ne comprendrai pas le devis. »
- « Ils travaillent pour l'OMC et UBS : mon petit chantier ne les intéressera pas, ou ce sera hors de prix. » **(Objection propre à Andy Construct, hyp. forte.)**
- « Les voisins vont se plaindre du bruit » ; en PPE : « l'assemblée refusera ».

**Ce qui les rassure.** Une **voix humaine** rapidement. La visite du patron ou d'un responsable. Une offre écrite, détaillée, TVA comprise, avec une date de validité. Les protections et le nettoyage décrits et montrés en photo. Des visages et des prénoms. L'adresse, la ligne fixe et le registre du commerce. Des avis réels. Une référence **dans leur commune** (« la salle communale de Collonge-Bellerive, c'est nous »). Une phrase claire sur les petits chantiers [à confirmer]. Des conditions de paiement claires, sans liquide demandé d'avance [à confirmer].

**Appareils et moments.** Tablette ou ordinateur **le soir et le week-end** ; de plus en plus le smartphone. 89 % des 65 ans et plus utilisent internet [10], plus de la moitié des 75 ans et plus s'y connectent chaque jour [12], mais près de la moitié ont une attitude ambivalente envers la sécurité du numérique [10]. Ils reviennent plusieurs fois sur le site avant d'appeler et impriment parfois une page.

**Canal préféré.** **Téléphone** en journée : ils veulent parler à quelqu'un. Puis **visite**. E-mail pour recevoir l'offre. Le formulaire le soir, s'il propose « Je préfère être rappelé(e) » avec un créneau.

**Leurs mots.** « devis » (plus qu'« offre »), « plafond », « fissures », « repeindre », « rafraîchir », « placo », « plâtre », « cloison », « bruit des voisins », « on entend tout », « isolation phonique », « humidité », « poussière », « travail propre », « sérieux », « honnête », « combien ça coûte », « sans engagement », « gratuit », « PPE », « copropriété », « administrateur », « assemblée », « règlement », « voisins ».

**En 10 secondes, ils veulent voir.** Une vraie entreprise locale, avec des personnes réelles ; qu'elle travaille aussi pour des particuliers ; un numéro à appeler ; des photos de travaux propres.

**À qui ils rendent des comptes.** Au conjoint, parfois aux enfants ; en PPE, aux autres copropriétaires.

**Leur phrase (hyp.).** « On ne cherche pas le moins cher. On cherche des gens honnêtes qui laissent la maison propre. »

**Note.** Les personnes âgées retiennent mieux les messages qui touchent à ce qui compte pour elles (confort, sérénité, relations) que les messages purement informatifs [8]. Pour ce persona, « retrouver le calme chez soi » parle plus que « indice d'affaiblissement Rw ». Les deux peuvent coexister : le bénéfice d'abord, le détail technique ensuite.

### 1.5 P5 — Olivier, 51 ans, gérant d'une PME

*Fiduciaire de quinze personnes à Lausanne. Le profil vaut aussi pour un cabinet médical, une agence, une boutique ou un restaurant.*

**Contexte.** Il est souvent locataire de ses locaux (bail commercial). Il décide seul ou avec un associé, avec son propre argent. Son activité ne doit pas s'arrêter. Locataire, il lui faut **l'accord écrit du bailleur** pour transformer les locaux (art. 260a CO [54]) : la régie entre donc dans la boucle.

**Objectif.** Des travaux **rapides, à prix fixe, sans fermer**, terminés avant une date précise.

**Déclencheurs.**
- Déménagement : aménagement avant la date d'entrée, un délai impératif.
- Croissance : un bureau ou une salle de réunion de plus.
- Bruit en open space ; confidentialité des entretiens (médecins, fiduciaires, avocats).
- Restaurant trop bruyant.
- Fin de bail : remise en état.
- Rafraîchissement de l'image des locaux.

**Critères de choix (classés).**
1. Délai et disponibilité : commencer vite, finir avant la date.
2. Travaux le soir ou le week-end, sans fermer [à confirmer].
3. Prix clair, idéalement forfaitaire, hors TVA.
4. Un interlocuteur qui coordonne, et une liste claire de ce qui n'est pas compris (électricité, par exemple).
5. Un résultat soigné : les locaux sont sa vitrine.
6. Réactivité.
7. Références d'entreprises : UBS, Piaget ou Celgene rassurent un chef d'entreprise.

**Peurs et objections.**
- « Je perds du chiffre d'affaires si je dois fermer. »
- « De la poussière sur les ordinateurs ou le matériel médical. »
- « Du bruit pendant que je reçois des clients. »
- « Dépassement de budget. »
- « Retard au-delà de mon emménagement. »
- « Je vais devoir coordonner moi-même cinq corps de métier. »
- « La régie va me reprocher des travaux non autorisés. »
- « Ils ne viendront pas le jour prévu. »

**Ce qui le rassure.** Un planning ferme lié à sa date. Des travaux hors des heures d'ouverture [à confirmer]. La protection du matériel. Une offre forfaitaire. Des références d'entreprises. Une aide pour la demande d'autorisation à la régie.

**Appareils et moments.** Smartphone le soir et entre deux rendez-vous ; ordinateur au bureau. Recherche rapide sur Google Maps (« plâtrier peintre près de moi ») et lecture des avis.

**Canal préféré.** **Téléphone**, ou **formulaire avec photos ou plan**. E-mail pour l'offre.

**Ses mots.** « aménagement », « réaménagement », « bureaux », « open space », « salle de réunion », « confidentialité », « on s'entend mal », « trop de bruit », « cloison », « arcade » (Genève), « local commercial », « bail », « régie », « état des lieux », « remise en état », « devis », « offre », « forfait », « HT », « TTC », « TVA », « délai », « week-end », « sans fermer ».

**En 10 secondes, il veut voir.** S'ils peuvent le faire vite et sans fermer ; un prix clair ; qui appeler.

**À qui il rend des comptes.** À son associé, à ses clients (l'image des locaux) et à son bailleur.

**Sa phrase (hyp.).** « Faites-le pendant que je ne suis pas là, et que lundi matin tout soit propre. »

### 1.6 Vocabulaire : à employer, à expliquer, à éviter

| Sujet | Particuliers | Professionnels | Recommandation pour le site |
|---|---|---|---|
| Document de prix | « devis » | « offre », « soumission » | Pages pros : « offre ». Pages particuliers : « devis », avec le mot « offre » expliqué (« offre écrite = devis »). Bouton principal à tester (T1). |
| Métier | « placo », « plâtrier », « peintre » | « plâtrerie », « gypserie », « plâtrerie-peinture », « CFC 271 » | « Placo » est le mot du client et du public, mais c'est une marque déposée de Saint-Gobain passée dans le langage courant. Dans les textes descriptifs, écrire aussi « plaques de plâtre », et placer « gypserie » sur les pages pros (helvétisme courant). |
| Bruit | « isolation phonique », « on entend tout », « bruit des voisins » | « isolation acoustique », « correction acoustique », « SIA 181 » | Titre de la page dans les mots du particulier, détails dans ceux du pro. Toujours distinguer **isoler** (bruit qui passe d'un local à l'autre) et **corriger** (écho dans la pièce), comme la maquette le fait déjà. |
| « Isotherme » | « isoler une pièce froide » | « cloison isolante », parfois « chambre froide » | **Ambigu.** Définition à confirmer avec le client (`contenus-a-valider.md`, §4). Un restaurateur pensera chambre froide. |
| « En régie » | (inconnu) | 1. « la régie » = gérance ; 2. « travaux en régie » = facturés au temps passé | Ne jamais écrire « travaux en régie » pour dire « travaux pour les régies ». Écrire « pour les régies et gérances ». |
| Locaux commerciaux | « magasin », « bureau » | « arcade » (Genève), « surface commerciale » | « arcade » sur les pages genevoises, « local commercial » ailleurs. |
| Copropriété | « copropriété », « PPE » | « PPE », « administrateur » | « PPE » est compris en Suisse romande ; l'écrire en entier une fois (« propriété par étages »). |
| Mots à proscrire | — | — | « solutions », « expertise premium », « clé en main » (sauf si vrai), « leader », « n° 1 », « innovant », anglicismes (« best », « team », « process »). Le public les associe à la publicité. |

---

## 2. Parcours de décision

### 2.0 Colonne vertébrale commune (site et automatisation)

Ce tableau sert de cahier des charges psychologique à l'ingénieur automatisation. Les délais entre crochets sont à valider avec le client : **on ne promet que ce qu'on tient**. Une promesse non tenue au premier contact est le pire « pic négatif » possible (section 3.8).

| Étape (suivi des prospects) | Déclencheur | Message automatique | Action humaine | Délai cible |
|---|---|---|---|---|
| Nouvelle demande | Formulaire, e-mail, ou appel saisi à la main | E-mail de confirmation en moins de 2 minutes. SMS si le numéro est un mobile (facultatif, transactionnel). Alerte interne (SMS ou e-mail au responsable). | Rappeler | [Même jour ouvrable, ou avant midi le lendemain] |
| Appel manqué | Appel non décroché | Aucun SMS automatique par défaut (risque de ressembler à du démarchage). Répondeur personnalisé. | Rappeler | [Dans l'heure ouvrable] |
| Contacté | Appel abouti | — | Fixer la visite | — |
| Visite planifiée | Date fixée | Confirmation écrite (date, heure, qui vient), rappel la veille | Visite | — |
| Offre envoyée | Offre PDF prête | E-mail d'envoi : résumé en 5 lignes en tête, offre en pièce jointe | Appel à J+3 ouvrables (« Avez-vous des questions ? ») | Offre [≤ X jours ouvrables après la visite] |
| Relance | J+8 sans réponse | **Un seul** e-mail court : réponse à l'objection la plus fréquente pour ce persona, et une fiche projet comparable | — | — |
| Clôture sans suite | J+21 sans réponse | E-mail de clôture courtois, avec la date de validité **réelle** de l'offre | Classer | — |
| Gagné | Acceptation | Confirmation, planning, informations pratiques selon le persona | Planifier | — |
| Avant le chantier | J-2 | Rappel : qui arrive, quand, comment préparer | — | — |
| Réception | Fin des travaux | Remerciement | Visite de réception commune | — |
| Avis ou référence | J+5 à J+10 après réception | Demande d'avis (particuliers, PME) ou d'autorisation de citer (professionnels). **Une** relance au maximum. | — | — |
| Suivi | J+30 ; avant la fin du délai de garantie | Prise de nouvelles ; contrôle proposé [à décider] | — | — |

**Exceptions.**
- **Procédures publiques** : aucune relance commerciale pendant la procédure. L'égalité de traitement l'interdit, et la relance serait perçue comme une pression. On répond seulement aux questions, par le canal officiel.
- **Architectes** : une seule question utile après l'envoi (« Vous manque-t-il un élément pour votre comparatif ? »), puis rien.
- **Toute réponse du prospect arrête immédiatement la séquence automatique.**

### 2.1 P1 Régie

| Étape | Ce qu'il fait ou se demande | Friction | Le site doit | L'automatisation doit |
|---|---|---|---|---|
| Découverte | Google ou carte Google (« plâtrier peintre Genève »), collègue, concierge, entreprise vue dans un immeuble qu'il gère | Toutes les entreprises se ressemblent ; aucune preuve d'expérience en site occupé | Titre et description qui citent « régies et gérances » ; bloc « Régies » sur l'accueil | Fiche Google complète et à jour (stratège acquisition) |
| Évaluation (2 à 5 min, souvent sur téléphone) | « Interviennent-ils chez moi ? Sont-ils réactifs ? Savent-ils gérer des locataires ? » | Page lente, zone absente, méthode invisible | Zone par commune ; méthode « site occupé » en 4 points ; références | — |
| Contact | Appelle ; ou envoie un e-mail avec photos | Personne ne répond ; répondeur anonyme | Numéro cliquable partout ; e-mail direct ; formulaire avec photo, adresse de l'immeuble, « logement occupé : oui / non » | Accusé de réception immédiat avec le nom de l'interlocuteur et le délai de rappel ; alerte interne |
| Offre | Visite avec le concierge, attend l'offre | Offre tardive, globale, impossible à comparer | Page « Ce que contient notre offre » : postes, quantités, délai, validité, exclusions | Rappel interne si l'offre n'est pas partie à J+2 ; e-mail d'envoi avec résumé ; appel à J+3 |
| Décision | Compare 2 ou 3 offres, fait valider par le propriétaire | Doit justifier un prix plus élevé | Fiche projet « régie » ; dossier PDF ; offre qui commence par un résumé lisible par le propriétaire | À l'acceptation : confirmation, planning, **modèle d'avis aux locataires** |
| Chantier | Veut ne rien entendre | Plaintes ; imprévus annoncés trop tard | — | J-3 : avis aux locataires prêt à afficher ; J0 : nom et portable du chef d'équipe ; tout imprévu signalé **avec son prix avant exécution** |
| Recommandation | Réception, facture | Facture différente de l'offre ; retouches | — | J+3 : deux questions de satisfaction ; J+10 : demande d'autorisation de citer la régie (les régies publient rarement des avis) ; J+90 : « D'autres immeubles à remettre en état ? » (un seul message, possibilité de refuser) |

### 2.2 P2 Architecte

| Étape | Ce qu'elle fait ou se demande | Friction | Le site doit | L'automatisation doit |
|---|---|---|---|---|
| Découverte | Réseau, anciens projets, annuaire GGE, Google, IA (« plâtrerie acoustique Genève ») | Le site ne parle pas CFC ; aucune preuve technique | Page ou bloc « Professionnels » avec les CFC, les normes et le dossier PDF ; données structurées et `llms.txt` (déjà prévus) | — |
| Évaluation | Lit les fiches projets, vérifie la capacité et les références comparables | Galerie sans contexte : qui, quoi, quand, quel système | Fiches projets : type de bâtiment, lot, système, contraintes, délai, année, maître d'ouvrage si autorisé | Dossier PDF téléchargeable **sans formulaire** ; NN/g déconseille de bloquer un contenu derrière une inscription [22] |
| Contact | Envoie le dossier de soumission avec la date de remise des offres | Pas d'e-mail direct ; le formulaire n'accepte pas les gros fichiers ; aucun accusé de réception | Chemin « Envoyer un dossier de soumission » : adresse e-mail, taille maximale, liens de transfert acceptés | Accusé de réception [dans l'heure ouvrable] qui rappelle la date de remise et le nom du responsable ; rappel interne à J-3 de cette date |
| Offre | Pose des questions, attend une offre conforme | Offre hors délai ou incomplète ; réserves cachées | — | Liste de contrôle interne avant l'envoi ; e-mail d'envoi avec un paragraphe « hypothèses et exclusions » |
| Décision | Comparatif, recommandation au maître d'ouvrage ; appelle parfois des références | Pas de référence joignable | « Références joignables sur demande » [à confirmer] | Une seule question à J+7 ; après l'adjudication : remerciement, nom du chef de chantier, planning |
| Chantier | Rendez-vous de chantier, coordination | Changement d'équipe, retard | — | Sur demande seulement ; le PV de chantier reste son outil |
| Recommandation | Réception, retouches | Liste de retouches qui traîne | — | J+7 après réception : remerciement et demande d'autorisation de publier une **fiche projet qui cite le bureau d'architectes** (visibilité offerte, voir réciprocité 3.3) |

### 2.3 P3 Commune / institution

| Étape | Ce qu'il fait ou se demande | Friction | Le site doit | L'automatisation doit |
|---|---|---|---|---|
| Découverte | Entreprises connues, recommandations d'autres communes, Google ; simap.ch pour les procédures ouvertes | Entreprise inconnue, donc jamais invitée | Bloc « Collectivités et institutions » : références publiques, CFC, types de procédures (gré à gré, invitation, simap) | Veille simap.ch et FAO sur les CFC 271, 283, 285 (stratège acquisition) |
| Évaluation | Vérifie le registre, les références, la capacité, les attestations | Aucune information administrative | Identité complète, lien vers le registre du commerce, « Attestations à jour sur demande » [à confirmer], dossier PDF | — |
| Contact | E-mail formel de demande d'offre ou invitation | Ne trouve pas le bon interlocuteur | Adresse e-mail et nom du responsable ; formulaire avec « date de remise » et « type de procédure » | Accusé de réception formel qui reprend la date de remise |
| Offre | Attend une offre au format demandé, dans le délai | Une attestation manquante peut éliminer l'offre [60] | — | Liste de contrôle des attestations ; **rappel automatique de renouvellement** (elles doivent être récentes) |
| Décision | Adjudication par l'exécutif, selon la procédure | Une relance serait vue comme une pression | — | **Aucune relance pendant la procédure.** Après la décision, gagnée ou perdue : remerciement ; si perdue, demander poliment les motifs |
| Chantier | Bâtiment public occupé, vacances scolaires | Sécurité, délai | — | Planning partagé ; point de fin de journée ; signalement immédiat de tout incident |
| Recommandation | PV de réception | Les collectivités ne publient pas d'avis | — | J+10 : demande d'une **fiche de référence** signée (souvent exigée dans les appels d'offres, hyp.) et de l'autorisation de citer le nom (en texte, jamais les armoiries) ; rappel interne avant la fin du délai de garantie |

### 2.4 P4 Propriétaire 55-70

| Étape | Ce qu'ils font ou se demandent | Friction | Le site doit | L'automatisation doit |
|---|---|---|---|---|
| Découverte | Google (« peintre Lancy », « bruit voisin plafond isolation »), voisin, administrateur de PPE, un enfant qui cherche pour eux | Jargon ; sites qui ressemblent à des plateformes ou à de la publicité | FAQ et pages services qui partent de leurs questions (« Vous entendez vos voisins ? ») ; communes citées | — |
| Évaluation (longue, le soir, en plusieurs visites) | « Sont-ils honnêtes ? Est-ce trop gros pour nous ? Combien ? » | Petit texte, pas de visage, références prestigieuses intimidantes, aucune idée du prix | Bloc « Particuliers » ; photo de l'équipe ; références locales ; avis ; « Comment se passe un chantier chez vous » ; facteurs de prix, et exemples de budgets si le client les fournit | — |
| Contact | Appel en journée ; ou formulaire le soir avec « rappelez-moi » | Personne ne répond ; formulaire long ; peur de donner ses données | Téléphone visible ; formulaire court ; raison donnée pour chaque donnée ; créneau de rappel | E-mail immédiat (et SMS si mobile) : **qui** rappelle, **quand**, **depuis quel numéro**. Aucune publicité. |
| Offre | La visite est **le moment décisif** : ponctualité, politesse, explications. Puis l'offre écrite. | Offre tardive ; lignes incompréhensibles ; acompte | Page « Comment lire notre offre » avec un exemple annoté | E-mail d'envoi avec un résumé en mots simples ; appel à J+4 (« Avez-vous des questions ? ») ; e-mail de clôture à J+21 avec la validité réelle ; **aucune pression** |
| Décision | En parlent entre eux, avec un enfant, un voisin ; comparent avec un autre devis ; en PPE, l'assemblée | Doivent convaincre d'autres personnes | Avis ; garantie légale expliquée ; « Résumé pour votre assemblée de copropriétaires » sur demande | Envoi du résumé pour l'assemblée sur simple demande |
| Chantier | Chez eux : poussière, ponctualité, politesse, nettoyage | Inquiétude chaque matin | — | J-2 : « L'équipe arrive mardi à 8 h : [prénoms]. Pour préparer : … » |
| Recommandation | **La fin est ce dont ils se souviendront** [50] : propreté, explications, remerciement | Nettoyage bâclé le dernier jour | — | J+3 : « Tout est en ordre ? » (appel ou SMS) ; J+7 : demande d'avis Google à **tous** les clients ; une relance au maximum |

### 2.5 P5 PME / commerce

| Étape | Ce qu'il fait ou se demande | Friction | Le site doit | L'automatisation doit |
|---|---|---|---|---|
| Découverte | Google Maps, régie ou bailleur, bouche-à-oreille | Concurrents spécialisés en cloisons vitrées ; Andy pose des cloisons en plaques de plâtre | Préciser « cloisons en plaques de plâtre, salles de réunion insonorisées, bureaux », avec des photos de bureaux | — |
| Évaluation (2 min sur mobile) | « Délai ? Sans fermer ? Prix ? » | Information absente | Bloc « Entreprises et commerces » : travaux hors des heures d'ouverture [à confirmer], références d'entreprises | — |
| Contact | Appel, ou formulaire avec plan et photos ; veut une date | Pas de date de visite proposée | Formulaire : « date souhaitée de fin des travaux » | Accusé de réception et proposition de créneaux de visite |
| Offre | Veut un forfait, un planning lié à sa date, la liste de ce qui n'est pas compris | Offre floue sur les exclusions | — | Relance par téléphone à J+2 ; **descriptif prêt à transmettre à sa régie** pour l'autorisation (art. 260a CO) |
| Décision | Rapide, mais dépend de l'accord du bailleur | La régie tarde | FAQ « Locataire : faut-il l'accord de ma régie ? » | Si sa date d'emménagement est réelle, rappel honnête du délai de commande du matériel [à confirmer] |
| Chantier | Le soir ou le week-end ; protection du matériel informatique | Poussière, bruit | — | Message de fin d'intervention : « Terminé, locaux nettoyés » |
| Recommandation | Avis Google, recommandation aux voisins de l'immeuble | — | — | J+5 : demande d'avis ; à 12 mois, une prise de nouvelles si le client l'a acceptée |

### 2.6 Les cinq moments de vérité

Ce sont les moments où la plupart des demandes se perdent, quel que soit le persona.

1. **Le premier appel non décroché.** Le prospect appelle le suivant de la liste. Il faut un renvoi vers le mobile, un répondeur personnalisé et un rappel rapide.
2. **Le délai avant le premier rappel.** Une demande contactée dans l'heure aboutit nettement plus souvent [30]. C'est à l'automatisation d'alerter l'équipe.
3. **L'offre** : tardive, globale ou illisible, elle fait perdre le chantier, même au meilleur artisan.
4. **Le premier jour de chantier** : ponctualité, protections, présentation de l'équipe.
5. **Le dernier jour** : nettoyage, réception, remerciement. C'est le souvenir qui produira (ou non) un avis et une recommandation.

---

## 3. Leviers psychologiques éthiques

Cadre : les principes de Cialdini [34], la recherche sur la crédibilité en ligne [22][26][27] et la psychologie cognitive. Pour chaque levier : le mécanisme, pourquoi il marche sur ce public, comment l'appliquer, et la limite à ne pas franchir.

**Règle générale.** Une personne âgée détecte moins bien les signaux de manque de fiabilité qu'une personne jeune (résultat d'imagerie et de comportement [9]). La responsabilité éthique est donc plus grande : un levier ne sert qu'à **rendre visible une qualité réelle**, jamais à en simuler une.

### 3.1 Autorité

**Mécanisme.** On suit plus facilement une source dont la compétence est reconnue [34]. Sur le web, montrer qu'une **vraie organisation compétente** se tient derrière le site fait partie des premiers critères de crédibilité [26], avec la qualité de conception et la transparence [22].

**Pourquoi ça marche ici.** Les professionnels délèguent un risque : « si la Ville de Genève et le Conservatoire leur confient des chantiers, je peux défendre ce choix ». Pour les seniors, une autorité **vérifiable** (registre du commerce, collectivités) est l'antidote au faux artisan.

**Application.**
- Identité vérifiable sur chaque page (pied de page) et sur « L'entreprise » : raison sociale, IDE, « inscrite au registre du commerce depuis 2007 », **avec un lien vers l'extrait officiel** (vérifiable en un clic : premier principe de Stanford [26]).
- « Depuis 2007 » plutôt que « 19 ans d'expérience » : vérifiable, et sans mise à jour annuelle.
- Références publiques en nom typographique dans le bandeau : Ville de Genève, Conservatoire de Musique de Genève, HEAD – Haute école d'art et de design, salles communales.
- Vocabulaire du métier sur les pages pros : CFC 271, 283, 285 ; SIA 118 ; SIA 181 ; AEAI « selon les exigences du projet ». Un architecte juge la compétence à la précision du vocabulaire.
- Photos de chantier en cours (ossature, suspentes) : NN/g recommande de montrer **le processus et les personnes**, pas seulement le résultat [22].
- Affiliation professionnelle, formation d'apprentis, convention collective, assurance : **seulement si c'est vrai** [à confirmer].

**Limite.** Aucun label, certification, « agréé » ou « certifié » non détenu (tromperie au sens de l'art. 3 LCD). Aucune performance normative promise en ligne. Aucune armoirie ni aucun emblème protégé (LPAP, Convention de Paris art. 6ter, programme §4). Une collectivité ne « recommande » pas une entreprise : écrire « nous a confié des travaux », jamais « nous recommande ».

### 3.2 Preuve sociale

**Mécanisme.** Dans l'incertitude, on regarde ce que font **des gens semblables** à soi [34]. Pour les avis, la probabilité d'achat augmente nettement dès les premiers avis ; une note trop parfaite (4,7 à 5) inspire **moins** confiance qu'une note de 4,2 à 4,7 [31]. Les visiteurs croient davantage les avis publiés **ailleurs** (Google) que les témoignages hébergés sur le site de l'entreprise [22].

**Pourquoi ça marche ici.** Les professionnels se demandent : « qui, comme moi, leur a fait confiance ? ». Une régie veut des régies, une commune des communes. Les particuliers vivent de bouche-à-oreille et d'avis.

**Application.**
- **Preuve par segment**, placée près de l'action de ce segment :
  - Collectivités : Ville de Genève, Mairie de Plan-les-Ouates, salle communale de Collonge-Bellerive, OMC.
  - Culture et formation (crédibles pour l'acoustique) : Conservatoire de Musique de Genève, HEAD, Salle de l'Alhambra.
  - Entreprises : UBS, Piaget, De Grisogono, Celgene.
  - Particuliers : avis Google, références dans leur commune.
- Avis Google réels : extrait, date, lien vers la fiche, nombre total d'avis. À afficher dès qu'il y en a au moins 5 ; aucun filtrage.
- Témoignages réels avec profil, commune et accord écrit (programme). Le format le plus convaincant raconte le passage **du doute à la confiance** [23] : « Nous hésitions à cause de la poussière… ».
- Chiffres : uniquement vérifiables. « 300+ chantiers » seulement si le client le confirme (`contenus-a-valider.md`).
- Dater les références récentes : une référence datée paraît vivante, une liste sans date peut paraître ancienne (critère « à jour » de Stanford [26]).

**Limite.** Aucun faux avis, faux témoignage ou note inventée. Aucune sollicitation **sélective** des clients satisfaits : Google l'interdit et demande de solliciter tous les clients [33]. Aucun logo sans accord écrit (programme). Aucun « des centaines de clients satisfaits » non mesuré.

#### 3.2 bis Répétition : où, combien de fois

**Mécanisme.** La simple exposition répétée rend un nom familier, et ce qui est familier plaît davantage (effet de simple exposition [41]). La méta-analyse de Bornstein [42] montre que l'effet est le plus fort pour des expositions **brèves et périphériques**, et qu'il plafonne puis s'émousse quand les expositions se multiplient. La répétition augmente aussi la **vérité perçue** d'une affirmation, même fausse [43] : on ne répète donc que des faits vérifiés. Les « trois expositions » de Krugman [44] sont une heuristique publicitaire ancienne et discutée : un ordre de grandeur, pas une loi.

**Le client demande la preuve sociale « partout où c'est pertinent ». Voici le plan d'exposition proposé.**

| Page | Emplacements | Contenu | Format |
|---|---|---|---|
| Accueil | 1. Bandeau juste sous le héro | 6 à 8 noms | Titre « Ils nous ont confié leurs chantiers », noms ou logos autorisés en monochrome, statique, lien « Toutes nos références (18) » |
| | 2. Portfolio | Noms des projets sur les cartes (si autorisé) | Légende |
| | 3. Pied de page (sur tout le site) | Une ligne discrète | Texte |
| Pages services | 1 bloc avant l'appel à l'action | 3 ou 4 références **de ce service** et une fiche projet liée | Texte et photo |
| Réalisations | Liste complète par secteur, fiches projets | 18 références | Liste |
| Contact | Une ligne près du formulaire | « Depuis 2007, pour la Ville de Genève, la HEAD, le Conservatoire… » | Texte court |
| Professionnels | Liste par secteur, dossier PDF | Selon le segment | Liste |
| E-mail de confirmation | Un lien vers 2 réalisations du type demandé | — | Lien (adresse complète) |
| Offre PDF | Une page « Références » | Selon le segment | Page |

**Règles.**
- **Trois expositions par page au maximum**, sans compter la ligne discrète du pied de page. Sur l'accueil : bandeau, portfolio et, si le test T7 est concluant, la ligne avant le formulaire.
- **Jamais deux blocs de références dans le même écran.**
- **Même liste courte, dans le même ordre, partout.** La reconnaissance se construit sur des stimuli identiques [41].
- **Les noms les plus forts en premier et en dernier** (position sérielle, 3.8). Ordre proposé : Ville de Genève · Conservatoire de Musique de Genève · HEAD · OMC · UBS · Piaget · Mairie de Plan-les-Ouates · Salle communale de Collonge-Bellerive. On ouvre sur une autorité publique et on finit sur une commune proche, à laquelle un particulier ou une commune peut s'identifier.
- Pas de défilement automatique ni de carrousel (brief) ; texte alternatif lisible.
- **Mesurer.** Le test T7 vérifie si la répétition avant le formulaire aide vraiment. Si elle n'apporte rien, on allège.

### 3.3 Réciprocité

**Mécanisme.** On se sent redevable envers quelqu'un qui nous a rendu un service sans contrepartie [39][34]. Le levier est d'autant plus fort que le service est **utile, adapté à la personne et inattendu**.

**Pourquoi ça marche ici.** Les professionnels apprécient tout ce qui leur fait gagner du temps. Les seniors sont très sensibles au **conseil honnête** (« Il nous a dit que ce n'était pas nécessaire ») : c'est le cadeau qui crée le plus de confiance.

**Application (un service utile par persona).**
- **Régie** : modèle d'avis aux locataires (Word ou PDF) et liste de contrôle « chantier en logement occupé ».
- **Architecte** : dossier de références en PDF ; fiches projets qui **citent et valorisent le bureau d'architectes** (avec son accord : visibilité offerte) ; fiche « points d'attention en acoustique » si le client peut la fournir.
- **Commune** : dossier de références organisé comme des critères d'aptitude ; attestations à jour envoyées sur simple demande.
- **Propriétaire** : une page « 7 questions à poser avant de signer un devis de plâtrerie-peinture ». Elle doit être honnête et valable aussi pour les concurrents : c'est ce qui la rend crédible. « Résumé pour votre assemblée de copropriétaires » sur demande.
- **PME** : descriptif des travaux prêt à transmettre à sa régie pour l'autorisation (art. 260a CO).
- **Pour tous** : conseil gratuit au téléphone ; visite gratuite [à confirmer] ; dire franchement quand un travail n'est pas utile ou n'est pas le métier d'Andy Construct, et orienter vers quelqu'un d'autre.

**Limite.** Pas de contenu offert en échange d'une adresse e-mail (NN/g le déconseille [22]). Pas d'avantage contre un avis (interdit par Google [33]). Pas de fausse valeur (« visite offerte d'une valeur de CHF 150.– » si elle n'est jamais facturée). Pas d'inscription à une lettre d'information par défaut.

### 3.4 Engagement progressif

**Mécanisme.**
- Accepter une petite demande rend plus probable l'acceptation d'une demande plus importante : c'est le « pied dans la porte » [35].
- Plus on se sent proche du but, plus on accélère (gradient de but [36]).
- Une progression déjà entamée motive à continuer (progression « offerte » [37]).

**Pourquoi ça marche ici.** Selon NN/g, 45 % des seniors hésitent à essayer quelque chose de nouveau, et ils abandonnent presque deux fois plus souvent que les plus jeunes [1]. Un long formulaire impressionne. Les professionnels, eux, manquent de temps.

**Application.**
- **Formulaire en 3 étapes** (à valider par le test T2) :
  1. « Quels travaux ? » : 4 grandes cartes (Placo, Peinture, Isolation acoustique, Cloisons isothermes) et « Je ne sais pas encore ». Question facile, rien de personnel.
  2. « Où et quand ? » : commune ou NPA ; « Dès que possible / Dans 1 à 3 mois / Plus tard / Je ne sais pas ».
  3. « Comment vous joindre ? » : nom, téléphone ou e-mail, « Je préfère être rappelé(e) », créneau, message facultatif, photo facultative.
- Annoncer la longueur dès le départ (« 3 étapes, environ 1 minute »). Afficher « Étape 2 sur 3 ». Bouton retour qui conserve les données. Boutons qui disent la suite (« Continuer : vos coordonnées ») [21].
- **Version express** : « Laissez votre numéro, nous vous rappelons ». Un ou deux champs ; c'est le plus petit engagement possible (test T3).
- **Pré-remplissage** : depuis une page service, le type de travaux est déjà coché. La progression est entamée [37].
- **Après le contact**, l'e-mail de confirmation reprend les mots du prospect (« Vous nous avez écrit : … »). Il se reconnaît, ce qui renforce la cohérence de sa démarche.

**Limite.** Ne pas cacher la longueur réelle du formulaire. Ne pas demander les coordonnées d'abord pour révéler ensuite d'autres étapes. Ne pas profiter de l'engagement pour vendre un service non demandé. Laisser **à chaque étape** la possibilité d'appeler. Un formulaire en étapes peut aussi désorienter : on teste avant de généraliser.

### 3.5 Sympathie et unité

**Mécanisme.** On dit plus volontiers oui à quelqu'un qu'on connaît, qui nous ressemble [40] ou qui « fait partie des nôtres » (l'**unité**, ajoutée par Cialdini en 2021 [34]). Les photos de **vraies personnes** de l'entreprise sont regardées attentivement ; les photos de banque d'images sont ignorées [28].

**Pourquoi ça marche ici.** Un particulier va faire entrer des inconnus chez lui : il a besoin d'un visage et d'une voix. L'identité locale compte beaucoup à Genève et en Suisse romande. Entre professionnels, l'unité passe par le **langage du métier**.

**Application.**
- **Visages réels** : les associés et l'équipe (photo de groupe, prénoms), avec accord écrit [à confirmer]. Prénom et photo dans la signature des e-mails.
- **Ancrage local factuel** : « entreprise de Carouge » ; les communes où des chantiers ont **réellement** eu lieu. « Vos voisins » seulement si c'est vrai : « La salle communale de Collonge-Bellerive, c'est nous. »
- **Ton** : vouvoiement, phrases simples, chaleur sans familiarité. Dans les e-mails automatiques, « Madame Dupont » plutôt que le prénom.
- **Professionnels** : parler leur langue (CFC, SIA) ; créditer l'architecte sur les fiches projets.
- **Particuliers** : le bénéfice qui compte pour eux d'abord (« retrouver le calme chez vous »), le détail technique ensuite [8].

**Limite.** Pas de fausse familiarité ni de tutoiement. Pas de visages de banque d'images. Pas de proximité inventée (« vos voisins nous recommandent » sans preuve). Pas de croix suisse ailleurs que dans le logo (brief), pas de patriotisme.

### 3.6 Réduction du risque

**Mécanisme.** Face à l'incertitude, on préfère l'option dont on comprend les conséquences. La transparence sur les coûts, les délais et les conditions est l'un des quatre facteurs de crédibilité de NN/g [22]. En B2B, le prix est l'information la plus recherchée, et le cacher rend l'offre suspecte ; montrer des **exemples de prix pour des cas courants** aide [23][24][25]. Enfin, **donner la raison** d'une demande augmente l'acceptation (« parce que… » [38]).

**Pourquoi ça marche ici.** La peur commune aux cinq personas est l'imprévisible (section 1).

**Application.**
- **Visite sur place avant toute offre** (gratuité [à confirmer]).
- **Offre écrite détaillée** : postes, quantités, prix unitaires, TVA, délai, durée de validité, exclusions, conditions de paiement. Page « Comment lire notre offre » avec un exemple annoté.
- **Transparence sur les prix** [24] : expliquer ce qui fait varier le prix (surface, état des supports, accès, site occupé, délai). Si le client fournit des chiffres réels, donner des budgets types (« repeindre un 4 pièces vide : en général entre CHF … et … ») [à fournir].
- **Planning annoncé, interlocuteur nommé avec son portable.**
- **Protection et nettoyage** décrits et montrés en photo (bâches, sas anti-poussière, nettoyage quotidien).
- **« Aucun travail supplémentaire sans votre accord écrit et chiffré »** [à confirmer]. C'est l'engagement le plus rassurant pour les cinq personas.
- **Garantie, dite factuellement** :
  - pour les contrats conclus depuis le 1er janvier 2026, un défaut peut être signalé dans les 60 jours (dès la livraison ou dès sa découverte), et le droit à la réparation gratuite ne peut plus être exclu pour un élément de construction [55] ;
  - la prescription pour un ouvrage immobilier reste de 5 ans [55] ;
  - pour un contrat soumis à la norme SIA 118, le délai de garantie est de 2 ans [57] ;
  - « Un défaut après la réception ? Appelez-nous, nous revenons » [à confirmer].
- **Paiement** : « Nous ne demandons jamais de paiement en liquide à l'avance » [à confirmer]. C'est la réponse directe à la peur du faux artisan.
- **Assurance responsabilité civile** : attestation sur demande [à confirmer].
- **Raison donnée dans le formulaire** : « Votre téléphone : pour vous rappeler et fixer la visite. Rien d'autre. »

**Limite.** Ne pas présenter un droit légal comme un avantage maison (c'est trompeur ; en droit européen, c'est même sur la liste noire de la directive 2005/29/CE, annexe I, point 10). Pas de « satisfait ou remboursé » ni de « prix garanti » non tenus. Pas de prix ferme promis avant la visite.

### 3.7 Aversion à la perte, formulée honnêtement

**Mécanisme.** Une perte pèse environ deux fois plus qu'un gain équivalent [45]. Mais dans les messages persuasifs, présenter une même idée comme une perte plutôt que comme un gain ne change presque rien en moyenne [46]. Et la peur ne fait agir que si l'on propose **en même temps une solution efficace** ; sinon, elle provoque le rejet [46b]. Conclusion : levier secondaire, toujours associé à une solution, et à tester.

**Pourquoi ça marche ici.** Pour un professionnel, le coût d'un chantier raté est concret et personnel. Les seniors craignent de mal dépenser leur épargne.

**Application (seulement des faits).**
- **Régie** : « Un appartement qui reste vide une semaine de plus, c'est une semaine de loyer perdue. Nous planifions la remise en état dès l'état des lieux de sortie. »
- **Régie, PME** : « Des travaux mal organisés en logement occupé entraînent des plaintes, voire des demandes de réduction de loyer (art. 259d CO). Voici comment nous l'évitons : … »
- **Architecte, commune** : « En isolation acoustique, tout se joue dans les détails : une liaison rigide mal traitée laisse passer le bruit, et on ne la corrige pas sans démonter. » Principe vrai ; ne donner aucun chiffre non vérifié.
- **Commune** : « Travaux d'été : nous nous engageons sur une date de fin compatible avec la rentrée » [à confirmer].
- **Propriétaire** : « À Genève, une demande de subvention énergétique doit être déposée **avant** le début des travaux » [63]. Seulement si le projet peut y prétendre, en renvoyant vers l'office compétent.
- **Pour tous** : « Le moins cher sur l'offre n'est pas toujours le moins cher au décompte : vérifiez ce que l'offre comprend. » Avec la liste de contrôle de la section 3.3, équitable envers les concurrents.

**Limite.** Pas d'appel à la peur sur la santé (moisissures, sécurité des enfants) sans base factuelle. Pas de faux délai (« offre valable 48 h »). Pas de menace de hausse de prix. Pas de compte à rebours. Pas de culpabilisation. Chaque risque mentionné est suivi de sa solution concrète.

### 3.8 Charge cognitive : Hick, Fitts, position sérielle, pic-fin

**Loi de Hick.** Le temps de décision augmente avec le nombre de choix [47]. Chez les personnes âgées, la pente est presque deux fois plus forte : environ 135 ms par « bit » d'information contre 77 ms chez les jeunes [6]. Les personnes âgées souhaitent en moyenne **moins de la moitié** des options que veulent les jeunes [7]. L'effet de « trop de choix » dépend du contexte : il apparaît surtout quand la décision est difficile et que les préférences sont floues [51]. C'est exactement la situation d'un particulier qui découvre la construction.
- **Application.** Navigation de 5 entrées au maximum. **4 cartes services, pas plus.** Par écran, 1 bouton principal et 1 bouton d'appel. FAQ groupée en 3 ou 4 thèmes. Dans le formulaire, 5 choix au maximum plus « Je ne sais pas ».

**Loi de Fitts.** Le temps pour atteindre une cible dépend de sa taille et de sa distance [48]. Chez les seniors, la dextérité mesurée était de 73 % contre 95 % chez les plus jeunes [1].
- **Application.** Cibles d'au moins 48 px (programme), espacées d'au moins 8 px. Barre fixe en bas de l'écran sur mobile, à portée du pouce. Boutons pleine largeur sur mobile. Cartes de choix entièrement cliquables. Jamais de petite croix de fermeture isolée.

**Position sérielle.** On retient mieux le début et la fin d'une liste [49].
- **Application.** Dans chaque liste, l'essentiel en premier et en dernier. Menu : « Prestations » en premier, « Contact » en dernier. Bandeau de références : les noms les plus forts aux deux extrémités. Page : la promesse principale dans le héro et dans l'appel à l'action final. E-mail : l'information clé (qui rappelle, quand) dans la première ligne **et** répétée dans la dernière.

**Règle pic-fin.** On juge une expérience surtout par son moment le plus intense et par sa fin [50].
- **Application.**
  - Repérer les pics : le premier appel (pic négatif s'il n'est pas décroché), la visite, le premier jour de chantier, la fin.
  - En ligne : une page de confirmation soignée ; un formulaire qui ne perd jamais les données.
  - Sur le chantier : nettoyage final, tour de réception avec le client, mot de remerciement. **Puis** la demande d'avis.
  - NN/g recommande expressément d'éviter les fenêtres qui tentent de retenir le visiteur au moment où il part [50].

**Limite.** Simplifier ne doit pas cacher une information importante (exclusions, conditions). Fitts ne sert jamais à faire un « Accepter » énorme et un « Refuser » minuscule. Le pic-fin ne sert pas à maquiller un mauvais chantier par un beau mot de remerciement.

---

## 4. Ergonomie senior : règles concrètes

**Pourquoi.** En 2013, les utilisateurs de 65 ans et plus réussissaient 55 % des tâches contre 75 % pour les 21-55 ans, mettaient 43 % plus de temps, et **s'attribuaient la faute dans 90 % des cas** (58 % chez les plus jeunes) [1]. La capacité à utiliser un site baisse d'environ 0,8 % par an entre 25 et 60 ans [2] : ces règles servent donc aussi les architectes de 45 ans. Les difficultés en cause : vision, dextérité, mémoire de travail, sensibilité aux distractions [4]. Le rapport NN/g sur les seniors compte 87 recommandations [3] ; voici celles qui comptent pour ce site.

**Lecture**
1. Texte courant de 18 px (16 px au minimum), interligne de 1,5 à 1,6, lignes de 60 à 75 caractères.
2. Le zoom doit fonctionner jusqu'à 200 % sans casser la page. Ne jamais bloquer le zoom sur mobile (`maximum-scale`).
3. Contraste d'au moins 4,5:1 (WCAG AA) ; viser 7:1 pour le texte courant (le graphite #44494F de la charte atteint environ 8:1). Pas de gris clair. Pas de texte sur une photo sans voile.
4. Liens soulignés, reconnaissables sans la couleur.
5. Pas de longs textes en capitales : les surtitres en capitales font 4 mots au maximum.

**Longueur des textes**
6. Une idée par écran. Paragraphes de 2 ou 3 phrases (4 lignes au maximum sur mobile).
7. L'essentiel dans la première phrase. On lit environ 20 % des mots d'une page [5].
8. Des titres qui donnent la réponse : « Nous intervenons dans toute la Suisse romande » plutôt que « Zone ».
9. Listes de 5 éléments au maximum.
10. Les mots du visiteur (section 1.6). Tout sigle est expliqué à sa première apparition sur les pages destinées aux particuliers.

**Nombre d'options**
11. Par écran, 1 action principale et le téléphone.
12. Navigation de 5 entrées au maximum, toujours au même endroit. Sur mobile, le mot « Menu » à côté de l'icône.
13. Pas de menus qui s'ouvrent au survol, pas de carrousels, pas d'onglets qui cachent une information essentielle. Les accordéons de la FAQ sont acceptables s'ils ont un indicateur visible (+ / −).

**Boutons et libellés**
14. Un verbe et un objet : « Demander une offre », « Appeler le 022 771 20 15 », « Envoyer ma demande », « Voir les réalisations en acoustique ». Jamais « Soumettre », « OK », « Cliquez ici » ni un « En savoir plus » isolé.
15. Boutons d'au moins 48 px de haut, pleine largeur sur mobile, texte d'au moins 18 px, espacés d'au moins 8 px.
16. Un bouton ressemble à un bouton (rectangle plein) ; un lien ressemble à un lien.

**Téléphone**
17. Numéro visible sur chaque page (en-tête sur ordinateur, barre fixe sur mobile), cliquable, **écrit en clair**, avec des espaces. Sur mobile, 70 % des personnes qui cherchent une entreprise utilisent l'appel direct [32]. Format : celui de la charte (`+41 22 771 20 15`) ; l'affichage « 022 771 20 15 » dans le bouton mobile est à tester (T6).
18. Les horaires à côté du numéro (« lun-ven, 7 h – 18 h ») [à confirmer] : on sait quand appeler, on ne tombe pas dans le vide.
19. **Le numéro doit répondre.** Renvoi vers un mobile pendant les chantiers. Répondeur personnalisé : nom de l'entreprise, prénom, promesse de rappel. Appels manqués rappelés [dans l'heure ouvrable].
20. Le mobile comme deuxième numéro, présenté comme tel (« sur les chantiers : 078 631 14 34 »).

**Formulaires**
21. 6 ou 7 champs visibles au maximum. Selon Baymard, la plupart des formulaires peuvent descendre à 6 à 8 champs [16]. Demander seulement ce qui sert à rappeler : nom, téléphone **ou** e-mail, commune, type de travaux, message facultatif, préférence de rappel.
22. Étiquettes **visibles au-dessus du champ**, jamais seulement en texte grisé à l'intérieur [19].
23. Marquer les champs obligatoires **et** les champs facultatifs (« facultatif » en toutes lettres). Quand seuls les facultatifs sont marqués, 32 % des utilisateurs font une erreur [14].
24. Une seule colonne, des champs larges, le clavier adapté (téléphone, e-mail).
25. Accepter tous les formats de téléphone : 022…, +41…, 0041…, avec ou sans espaces ni tirets [1][2].
26. Proposer une correction d'e-mail sans bloquer (« Vouliez-vous dire @bluewin.ch ? »).
27. Pas de CAPTCHA à images. Anti-spam invisible (champ piège, temps minimal de remplissage) : à mettre en œuvre par l'ingénieur automatisation.
28. Photo ou plan en pièce jointe : facultatif, taille maximale annoncée, possibilité d'envoyer plutôt par e-mail.
29. « Je préfère être rappelé(e) » avec un créneau (matin, après-midi, indifférent).
30. Les formulaires qui suivent des règles d'ergonomie de ce type sont remplis plus vite et envoyés plus souvent du premier coup (étude de l'Université de Bâle [17]).

**Erreurs**
31. Vérifier un champ quand on le quitte, pas pendant la frappe [15][18]. Message sous le champ, avec texte, icône et couleur, en français simple, qui dit **quoi faire** : « Indiquez un numéro de téléphone ou une adresse e-mail pour que nous puissions vous répondre. » [20]
32. À l'envoi, un récapitulatif des erreurs en haut, avec des liens vers les champs, et le curseur sur la première erreur.
33. **Ne jamais vider le formulaire** [20]. Si l'envoi échoue (réseau), conserver la saisie et proposer le téléphone.
34. Ton non culpabilisant : pas de « invalide » ni de « erreur de saisie » (90 % des seniors se croient fautifs [1]).

**Confiance dans le formulaire**
35. Sous le bouton d'envoi, ce qui va se passer et quand : « Nous vous rappelons le jour même ou le jour ouvrable suivant » [à confirmer].
36. La raison de chaque donnée [38][23]. « Vos coordonnées servent uniquement à répondre à votre demande. Pas de publicité, aucune transmission à des tiers » (conforme au programme nLPD). Lien vers la protection des données.
37. Page de confirmation **et** e-mail récapitulatif. Un senior doute souvent que « ça soit parti ».

**Peur de l'arnaque**
38. Identité complète : raison sociale, adresse physique, IDE, lien vers le registre, ligne fixe, visages, photos réelles.
39. Ne jamais demander de date de naissance, d'IBAN ni de carte. Aucun paiement en ligne.
40. **SMS et e-mails** :
    - expéditeur identifiable (« Andy Construct ») ;
    - **aucun lien raccourci, idéalement aucun lien dans les SMS** ;
    - jamais d'urgence ni de menace ;
    - reprendre des éléments que seule l'entreprise connaît (nom, commune, type de travaux).
    C'est exactement ce que l'Office fédéral de la cybersécurité apprend au public à repérer : liens dans les SMS, expéditeurs falsifiés, menaces [13].
41. Adresse e-mail sur un domaine propre (contact@…) plutôt qu'une messagerie gratuite [à décider] ; authentification des envois (SPF, DKIM, DMARC), sinon les e-mails partent dans les indésirables ou paraissent suspects.
42. Le même nom, la même adresse et le même numéro partout (site, Google, annuaires). Une incohérence ressemble à une fraude.

**Mobile et tablette**
43. Barre fixe en bas « Appeler | Demander une offre » de 64 px de haut au maximum. En-tête et barre fixes ne doivent pas occuper plus de 20 % de l'écran.
44. Tester sur tablette en mode portrait et paysage : c'est l'appareil du soir des propriétaires.
45. Pas de bandeau de cookies, puisqu'il n'y a aucun cookie non essentiel (programme).

---

## 5. Liste noire

| Interdit | Pourquoi ça fait fuir (ou c'est illégal) | À la place |
|---|---|---|
| Fausse urgence, compte à rebours, « plus que 2 créneaux » | Dark pattern classique [52][53] ; tromperie (LCD). La pression temporelle est aussi la signature des escroqueries que les seniors apprennent à repérer [13]. | Les vrais délais (« pour commencer en juillet, il faut valider l'offre avant le … », si c'est vrai) |
| Faux avis, avis filtrés, note inventée | LCD ; règles Google [33]. Une découverte suffit à tout détruire. Une note parfaite inspire même moins confiance [31]. | Avis Google réels, sollicités auprès de tous les clients |
| Témoignages fictifs ou génériques (« Jean D. ») | Idem | Témoignages réels avec accord écrit, sinon pas de section (programme) |
| Fenêtres surgissantes (lettre d'information, sortie, offre) | Fin d'expérience négative [50] ; contraire aux règles de crédibilité [26] ; un senior ne sait pas toujours comment les fermer | Rien, ou un bloc intégré à la page |
| Chat flottant, robot conversationnel | Masque le contenu sur mobile ; le public veut un humain (brief) | Le téléphone |
| Cases pré-cochées (lettre d'information, consentement) | Dark pattern ; nLPD et LCD | Case vide, facultative, ou pas de case du tout |
| Culpabilisation (« Non merci, je préfère un chantier raté ») | Manipulation (programme) | Libellés neutres |
| Champs inutiles obligatoires (budget, entreprise pour un particulier, adresse complète) | Abandon [16] ; méfiance (« pourquoi veulent-ils savoir ça ? ») | 6 ou 7 champs, la raison de chaque champ |
| CAPTCHA à images | Échec fréquent chez les seniors (vision, dextérité) [1] | Anti-spam invisible |
| Carrousel automatique, vidéo en lecture automatique, parallaxe, compteurs animés | Distraction et charge mentale [4] ; interdit par le brief | Contenu statique |
| « n° 1 », « meilleur », « leader », « premium », anglicismes | Promesses invérifiables (LCD) ; le public les associe à la publicité | Des faits vérifiables |
| Labels, certifications ou « agréé » non détenus | Tromperie, art. 3 LCD | Rien, ou les attestations réelles |
| Photos de banque d'images, ou images générées présentées comme des réalisations | Ignorées [28] ; trompeuses | Photos réelles légendées |
| Prix d'appel non tenus (« dès CHF 25.– le m² ») | Piège ; tromperie | Des fourchettes réelles, ou les facteurs qui font varier le prix |
| « Gratuit* » avec des conditions en petits caractères | Perte de confiance immédiate | Des conditions écrites en clair |
| Dossier PDF bloqué derrière une adresse e-mail | NN/g le déconseille [22] ; les professionnels partent | Téléchargement libre |
| Plus de deux relances écrites ; appels non sollicités ; lettre d'information sans consentement | LCD art. 3 al. 1 let. o : la publicité de masse exige un consentement préalable et un moyen simple de refuser [62] | Une séquence courte, qui s'arrête à la première réponse |
| Liens raccourcis (bit.ly) ; liens dans les SMS | Ressemblent à du hameçonnage [13] | Pas de lien, ou l'adresse complète du site |
| Pixels de suivi cachés dans les e-mails ; outils tiers non déclarés | nLPD ; programme | Mesure sans cookie, déclarée dans la politique de confidentialité |
| Petits caractères gris, texte sur photo, liens minuscules | Illisible [1][4] | La charte (18 px, contrastes AA) |
| Numéro introuvable, formulaire seul, adresse « info@ » sans nom | Contraire aux principes de contact et de transparence [26][22] | Numéro sur chaque page, une personne nommée |
| Informations datées (« © 2010-2022 », « photos 2014-2016 ») | On croit l'entreprise inactive (`justification.md`) | Dates à jour |
| « Refuser » minuscule à côté d'un « Accepter » énorme | Dark pattern d'asymétrie [52] | Deux choix de même poids |
| Promesses non tenues (« réponse en 1 h » si c'est impossible) | Le pire pic négatif [50] | Ne promettre que ce qu'on tient |
| Peur sans fondement (santé, sécurité des enfants) | Manipulation ; la peur sans solution provoque le rejet [46b] | Le risque réel et sa solution |

---

## 6. Tableau d'application

| Élément | Levier(s) | Mise en œuvre précise | Indicateur à suivre |
|---|---|---|---|
| **En-tête (ordinateur)** | Fitts, autorité, réduction du risque | Logo à gauche ; 4 ou 5 entrées de menu ; à droite, le numéro en clair et cliquable, les horaires en petit, et le bouton « Demander une offre ». L'en-tête ne rétrécit pas et ne disparaît pas au défilement. | Clics sur le téléphone et sur le bouton de l'en-tête |
| **Barre fixe mobile** | Fitts, engagement | Deux boutons de même largeur, d'au moins 56 px de haut : « Appeler » (avec le numéro selon T6) et « Demander une offre ». Présente dès l'ouverture ; ne cache pas le pied de page. | Clics sur le téléphone mobile par page ; part des visites mobiles avec un clic |
| **Héro** | Autorité, unité, position sérielle, Hick | H1 = métier et lieu. Une phrase de preuve vérifiable (« Depuis 2007, pour la Ville de Genève, le Conservatoire, la HEAD et des particuliers de toute la région »). Deux boutons. Bande de confiance de 3 ou 4 faits vérifiables (depuis 2007 · offre écrite après visite [à confirmer] · un seul interlocuteur · toute la Suisse romande). Photo réelle avec voile. Variante T4 : deux portes, « Vous êtes un professionnel » / « Vous êtes un particulier ». | Taux de clic des boutons du héro ; taux de rebond ; défilement à 50 % |
| **Bandeau de références** | Preuve sociale, autorité, répétition, position sérielle | « Ils nous ont confié leurs chantiers » ; 6 à 8 noms, toujours dans le même ordre (section 3.2 bis) ; logos seulement si `autorise`, en monochrome et statiques ; lien « Toutes nos références (18) ». | Clics vers les références ; clics sur les boutons situés après le bandeau |
| **Cartes services (4)** | Hick, engagement | Exactement 4 cartes : Placo, Peinture, Isolation acoustique, Cloisons isothermes. Sur chaque carte : une phrase dans les mots du client (« Vous entendez vos voisins ? »), « pour qui », et « Voir le détail ». Carte entièrement cliquable. Pas de liste « Également ». | Clics par carte ; demandes par type de travaux |
| **Pages services** | Autorité, preuve sociale ciblée, réduction du risque, perte honnête | Structure fixe : à quoi ça sert → pour quels locaux → comment nous travaillons → points d'attention honnêtes → 3 ou 4 références de ce service → photos → 3 questions fréquentes → appel à l'action avec le type de travaux déjà coché. | Taux de conversion par page ; part des formulaires pré-remplis |
| **Portfolio / galerie** | Preuve, unité (photos réelles), Hick | Filtres = les 4 services et « Chantiers en cours ». Légende factuelle : type de travail, type de bâtiment, année si connue. Agrandissement simple, flèches, bouton « Fermer » écrit. Pas de défilement automatique. | Photos ouvertes ; passages de la galerie au contact |
| **Fiches projets** | Autorité, preuve sociale par similarité, réciprocité | Client (si autorisé) ou type de client, commune, année, besoin, solution, contraintes (logement occupé, délai), résultat, photos avant / pendant / après, crédit de l'architecte. Au moins une fiche par segment. | Vues ; demandes qui citent un projet ; téléchargements du dossier |
| **Méthode** | Réduction du risque, Hick (4 étapes), pic-fin | 4 étapes numérotées : visite → offre écrite détaillée → chantier protégé et nettoyé → réception ensemble. Sous chaque étape, un délai type [à confirmer]. La dernière étape est une fin positive. | Défilement jusqu'à la méthode ; clics sur les boutons qui la suivent |
| **Engagements** | Réduction du risque, autorité | 3 ou 4 engagements vérifiables seulement [à confirmer] : « Aucun supplément sans votre accord écrit » ; « Un seul interlocuteur, joignable » ; « Protection et nettoyage chaque jour » ; « Offre détaillée par poste ». | Engagements cités spontanément au téléphone (à noter dans le suivi des prospects) |
| **Avis et témoignages** | Preuve sociale | Avis Google réels (extraits, lien) ; témoignages réels (profil, commune, accord écrit). Bloc masqué tant qu'il est vide (programme). | Nombre d'avis ; note ; clics vers la fiche Google |
| **Zone d'intervention** | Unité, réduction du risque | Carte et liste par canton ; « Votre commune n'est pas dans la liste ? Appelez-nous » ; mise en avant des communes où des chantiers ont réellement eu lieu. | Demandes par commune |
| **Bloc « Professionnels »** | Autorité, réciprocité, réduction du risque | Trois sous-blocs courts (Régies / Architectes / Collectivités) : ce que nous apportons, la preuve, l'action (« Envoyer un dossier de soumission », « Télécharger le dossier de références (PDF) », « Attestations sur demande »). | Téléchargements du PDF ; demandes professionnelles ; invitations à soumissionner |
| **FAQ** | Réduction du risque, réciprocité, Hick | 8 à 10 questions en 4 groupes (prix et offre, déroulement, particuliers, professionnels). Réponses de 2 à 4 phrases, honnêtes (« Pourquoi pas de prix sans visite ? »). La question la plus posée en premier. | Questions ouvertes ; questions encore posées au téléphone (journal des appels) |
| **Formulaire** | Engagement progressif, réduction du risque, Fitts, raison donnée | Règles de la section 4 ; 3 étapes (si T2 le confirme) ou 6 champs ; « Vous êtes : particulier / régie / architecte / commune ou institution / entreprise » ; rappel et créneau ; réassurance sous le bouton ; anti-spam invisible. | Taux de démarrage, abandon par champ et par étape, taux d'envoi ; part des demandes complètes |
| **Page de confirmation** | Pic-fin, sympathie, réduction du risque | « Merci, votre demande est bien arrivée », puis le récapitulatif. « [Prénom] vous rappelle [délai] depuis le 022 771 20 15 », avec sa photo. « Pour gagner du temps, préparez : photos, dimensions approximatives, plans. » Un seul lien : les réalisations du type demandé. | Visites des réalisations ensuite ; taux de joignabilité au rappel |
| **Pied de page** | Autorité, preuve, répétition | Coordonnées complètes, horaires, raison sociale et IDE, lien vers le registre ; une ligne de références discrète ; liens légaux ; « © 2026 » à jour. | Clics sur le lien du registre et sur le téléphone du pied de page |
| **E-mail de confirmation** | Pic-fin, réciprocité, réduction du risque, position sérielle | Expéditeur « Andy Construct » sur un domaine propre. Objet : « Votre demande est bien reçue – Andy Construct ». Première ligne : qui rappelle et quand. Puis le récapitulatif de la demande, ce qu'il faut préparer, 2 réalisations comparables (adresse complète du lien), la signature (nom, photo, fixe, adresse). Dernière ligne : le délai et le numéro, répétés. Ni publicité ni image lourde. Version professionnelle (CFC, dossier PDF) et version particulier. | Réponses à l'e-mail ; taux de visite fixée ; appels entrants qui citent l'e-mail. (Pas de pixel de suivi non déclaré.) |
| **SMS (facultatif)** | Réduction du risque, pic | Uniquement transactionnel, si le numéro est un mobile : « Andy Construct : demande bien reçue. [Prénom] vous appelle aujourd'hui avant 17 h depuis le 022 771 20 15. » Rappel la veille de la visite. **Sans lien.** Expéditeur alphanumérique « AndyConstr ». | Taux de joignabilité ; visites manquées |
| **Relances après l'offre** | Réduction du risque, cohérence, réciprocité | J+3 ouvrables : appel « Avez-vous des questions ? ». J+8 : e-mail court (réponse à l'objection fréquente du persona, fiche projet comparable). J+21 : e-mail de clôture courtois avec la validité réelle. Arrêt à la première réponse. Aucune relance en procédure publique. | Taux de réponse ; taux de signature ; délai entre l'offre et la décision ; zéro plainte |
| **Demande d'avis ou de référence** | Preuve sociale, pic-fin, réciprocité | Après la réception, au moment positif. Particuliers et PME : J+5, SMS ou e-mail avec le lien Google, plus la phrase « ou cherchez Andy Construct sur Google Maps » ; une relance à J+12. Professionnels : autorisation de citer, fiche de référence ou fiche projet. **Tous les clients, sans tri.** | Part des clients qui laissent un avis ; nombre d'autorisations de citer |
| **Suivi après le chantier** | Pic-fin, réciprocité, fidélisation | J+30 : « Tout va bien ? » (particuliers). Avant la fin du délai de garantie (contrats SIA : vers 22 mois), contrôle proposé [à décider]. Régies : J+90, « D'autres immeubles ? » (un seul message). | Retours clients ; demandes récurrentes ; recommandations reçues |
| **Téléphone et répondeur** | Sympathie, réduction du risque, pic | Annonce du répondeur : nom de l'entreprise, prénom, « nous vous rappelons [dans l'heure ouvrable] ». Renvoi vers le mobile. Chaque appel saisi dans le suivi des prospects, avec « Comment nous avez-vous connus ? ». | Part des appels décrochés ; délai de rappel ; origine des appels |
| **Dossier de références et offre (PDF)** | Autorité, preuve, aide à convaincre en interne | Page 1 : un résumé lisible par un tiers (propriétaire, assemblée, exécutif). Ensuite : références par secteur, méthode, identité juridique. | Téléchargements ; taux d'offres signées |

---

## 7. Tests A/B recommandés

### 7.0 À lire avant de tester : le trafic sera faible

- **Ordre de grandeur.** Pour détecter un passage de 2 % à 3 % de conversion (+50 %), avec 80 % de chances de le voir et 5 % de risque de fausse alarme, il faut environ **3'800 visites par variante**, soit 7'600 au total (formule classique de comparaison de deux proportions). Pour un taux de clic qui passe de 10 % à 13 %, il en faut environ **1'800 par variante**.
- **En pratique** : avec quelques milliers de visites par mois (à mesurer), un test sur les demandes envoyées durera des mois. On teste donc **d'abord les micro-conversions** (clics sur les boutons, formulaires commencés), et l'on profite du trafic des annonces s'il y en a.
- **Règles** :
  - un seul test à la fois sur une même page ;
  - au moins deux semaines complètes, en semaines entières (le soir et le week-end, le public n'est pas le même) ;
  - indicateur choisi **avant** le test ;
  - pas d'arrêt dès qu'un résultat paraît favorable.
- **Technique et vie privée.** La répartition des visiteurs doit se faire sans cookie non essentiel (programme), par exemple en alternant par période. À défaut, avec un consentement. À valider avec l'ingénieur automatisation. Un test « 2 semaines A, 2 semaines B, puis on recommence » est moins fiable : il faut le dire dans le bilan.
- **Éthique.** Les deux variantes doivent être honnêtes. On ne teste jamais une fausse urgence « pour voir ».
- **E-mails, SMS, relances** : avec quelques dizaines de demandes par mois, aucun test ne sera concluant statistiquement. On les observe et on les améliore à partir des réponses et des entretiens.

### 7.1 Tests

| # | Hypothèse | A (contrôle) | B (variante) | Indicateur principal | Garde-fou |
|---|---|---|---|---|---|
| T1 | Les particuliers disent « devis », les professionnels « offre ». « Devis » augmente les clics des particuliers sans faire baisser les demandes des professionnels. | « Demander une offre » | « Demander un devis » (plus tard, variante C « … gratuit » si la gratuité est confirmée) | Taux de clic du bouton principal | Part des demandes professionnelles |
| T2 | Une première question facile (type de travaux) en 3 étapes réduit l'abandon des seniors (engagement progressif). | Formulaire sur une page (6 ou 7 champs) | Formulaire en 3 étapes avec indicateur de progression | Envois / formulaires commencés | Part des demandes complètes (commune et type renseignés) ; abandon par étape |
| T3 | Un rappel express (1 ou 2 champs) attire des visiteurs qui n'auraient pas rempli de formulaire. | Formulaire complet dans la bande d'appel finale | « Laissez votre numéro, nous vous rappelons » et un créneau | Nombre total de demandes | Part des demandes joignables et pertinentes |
| T4 | Deux portes d'entrée aident chacun à se reconnaître (similarité), surtout les particuliers que les grandes références intimident. | Parcours unique | Dans le héro : « Vous êtes un professionnel » / « Vous êtes un particulier », vers deux blocs ciblés | Conversion globale et par segment | Taux de rebond |
| T5 | Dire sous le bouton ce qui va se passer réduit l'hésitation au moment de l'envoi (réduction du risque, raison donnée). | Bouton seul | Bouton et 3 lignes : délai de rappel, « pas de publicité », « vos données restent chez nous » | Envois / formulaires commencés | — |
| T6 | Afficher le numéro dans le bouton mobile rassure : on voit une ligne fixe locale avant d'appeler. | « Appeler » | « Appeler le 022 771 20 15 » | Clics sur le téléphone / visites mobiles | Clics sur « Demander une offre » |
| T7 | Rappeler les références juste avant le formulaire final augmente les envois. C'est le test de la demande de répétition du client. | Pas de références avant le formulaire | Une ligne « Ils nous ont confié leurs chantiers : … » au-dessus du formulaire | Envois / visiteurs qui atteignent le formulaire | Défilement |
| T8 | Une demande d'avis par SMS sans lien est mieux reçue par les seniors qu'un e-mail avec lien (peur du hameçonnage). | E-mail avec lien direct vers la fiche Google | SMS : « Merci ! Si vous êtes satisfait(e), un avis sur Google (cherchez “Andy Construct”) aide beaucoup. » | Part des clients qui laissent un avis | Plaintes (zéro attendu) |

**Ordre conseillé.** T6 et T1 d'abord (micro-conversions rapides, aucun développement lourd). Puis T5, T7, T2. T3 et T4 changent davantage la page : on les lance quand le trafic est connu. T8 s'observe sur plusieurs mois.

---

## 8. À fournir par le client (ce document en dépend)

Chaque point débloque un levier. Sans réponse, le texte correspondant reste masqué ou neutre.

| Fait à confirmer | Levier débloqué |
|---|---|
| Délai de rappel réellement tenable (même jour ? lendemain midi ?) | Réduction du risque, page de confirmation, e-mail |
| Visite et offre gratuites et sans engagement ? | Bouton (T1), héro, FAQ |
| Délai habituel pour envoyer l'offre après la visite | Méthode, relances |
| Travaux le soir, le week-end, pendant les vacances scolaires ? | PME, communes |
| Conditions de paiement ; jamais de liquide d'avance ? | Peur de l'arnaque |
| Attestation d'assurance RC ; attestations sociales et fiscales ; OCIRT ou CCT | Communes, régies |
| Apprentis formés ; affiliation à une association professionnelle | Autorité |
| « Aucun supplément sans accord écrit » : engagement possible ? | Le plus fort réducteur de risque |
| Photos de l'équipe et des associés, avec accords écrits | Sympathie |
| 2 ou 3 témoignages réels ; fiche Google gérée | Preuve sociale |
| Autorisations de citer des régies, des architectes, des entreprises | Preuve par segment |
| Budgets types réels (2 ou 3 cas courants) | Transparence sur les prix |
| Petits chantiers acceptés ? À partir de quelle taille ? | Objection « trop gros pour moi » |
| Qui répond au téléphone ; renvoi possible ; répondeur | Moments de vérité |
| Adresse e-mail sur le domaine de l'entreprise | Confiance des e-mails |
| Nombre approximatif de chantiers | Chiffre clé (sinon retiré) |
| Pratique après chantier : retouches, contrôle avant la fin de la garantie | Pic-fin, fidélisation |
| Définition de « cloisons isothermes » | Vocabulaire, PME (chambres froides ?) |

---

## 9. Valider les personas en deux semaines

1. **8 à 10 entretiens téléphoniques de 20 minutes** avec des clients existants : 2 par persona. Six questions :
   - Comment nous avez-vous trouvés ?
   - Qu'est-ce qui vous a fait hésiter ?
   - Qu'est-ce qui vous a décidé ?
   - Qu'avez-vous comparé ?
   - À qui avez-vous dû rendre des comptes ?
   - Qu'est-ce qui vous ferait nous recommander ?
2. **Relire les 30 dernières demandes et les 30 derniers appels** : origine, type de travaux, objections, délai de réponse, résultat.
3. **5 tests d'utilisabilité avec des personnes de 55 à 75 ans** sur la version de validation. Trois tâches : trouver le numéro ; savoir si l'entreprise intervient dans votre commune ; demander un rappel. Noter les hésitations, pas les opinions.
4. **Mettre à jour** ce document : chaque « (hyp.) » confirmé ou corrigé.

---

## Sources

**Documents du projet** : `docs/v2/programme-v2.md`, `docs/brief-design.md`, `docs/justification.md`, `docs/analyse-marche.md` (dont les sources de marché : OFS, ge.ch, Statcounter, UZH/RTS), `docs/contenus-a-valider.md`.

**Utilisateurs âgés, lisibilité, choix**
1. Nielsen J., « Usability for Senior Citizens: Improved, But Still Lacking », Nielsen Norman Group, 28.05.2013. https://www.nngroup.com/articles/usability-seniors-improvements/
2. Kane L., « Usability for Older Adults: Challenges and Changes », Nielsen Norman Group, 08.09.2019. https://www.nngroup.com/articles/usability-for-senior-citizens/
3. Nielsen Norman Group, rapport « UX Design for Seniors (Ages 65 and older) », 3e édition, 87 recommandations. https://www.nngroup.com/reports/senior-citizens-on-the-web/
4. W3C WAI, « Older Users and Web Accessibility ». https://www.w3.org/WAI/older-users/
5. Nielsen J., « How Little Do Users Read? », Nielsen Norman Group, 2008. https://www.nngroup.com/articles/how-little-do-users-read/
6. Sleimen-Malkoun R., Temprado J.-J., Berton E. (2013), « Age-related dedifferentiation of cognitive and motor slowing: insight from the comparison of Hick–Hyman and Fitts' laws », *Frontiers in Aging Neuroscience*. https://pmc.ncbi.nlm.nih.gov/articles/PMC3797466/
7. Reed A. E., Mikels J. A., Simon K. I. (2008), « Older adults prefer less choice than young adults », *Psychology and Aging*, 23(3), 671-675. https://pmc.ncbi.nlm.nih.gov/articles/PMC2631411
8. Fung H. H., Carstensen L. L. (2003), « Sending memorable messages to the old: Age differences in preferences and memory for advertisements », *Journal of Personality and Social Psychology*, 85(1), 163-178.
9. Castle E., Eisenberger N. I., Seeman T. E. et al. (2012), « Neural and behavioral bases of age differences in perceptions of trust », *PNAS*, 109(51), 20848-20852.

**Suisse : seniors, numérique, fraude**

10. Pro Senectute Suisse / FHNW, « Digital Seniors 2025 » (enquête représentative, 1'455 personnes de 65 ans et plus). https://www.prosenectute.ch/fr/espace-pro/fond/etudes/digital-seniors-2025.html
11. Pro Senectute Suisse, communiqué « Deuxième étude sur les abus financiers chez les personnes âgées en Suisse », 02.10.2023 (ILCE Neuchâtel, 1'216 personnes). https://ow.prosenectute.ch/dam/jcr:4384ab8b-f89b-4a3f-92d1-5a62abc41f6c/20231001_Communique%20de%20presse_Etude_Abus_financiers.pdf
12. OFS, « La pandémie accélère l'utilisation de la cyberadministration », 15.12.2021 (96 % des 15-88 ans utilisent internet ; plus de la moitié des 75 ans et plus quotidiennement). https://www.admin.ch/fr/nsb?id=86268
13. Office fédéral de la cybersécurité (OFCS), « Hameçonnage (Phishing), Vishing, Smishing ». https://www.bacs.admin.ch/fr/phishing-fr

**Formulaires**

14. Baymard Institute, « Mark both required and optional fields » (2018, chiffres du benchmark 2021). https://baymard.com/blog/required-optional-form-fields
15. Baymard Institute, « Usability Testing of Inline Form Validation » (2024). https://baymard.com/blog/inline-form-validation
16. Baymard Institute, article sur le nombre de champs des formulaires de commande (2024 : 11,3 champs en moyenne, 6 à 8 suffisent sur la plupart des sites). https://baymard.com/blog/checkout-flow-average-form-fields
17. Seckler M., Heinz S., Bargas-Avila J. A. et al. (2014), « Designing Usable Web Forms: Empirical Evaluation of Web Form Improvement Guidelines », CHI 2014 (Université de Bâle / Google). https://research.google/pubs/pub42513/
18. Wroblewski L. (2009), « Inline Validation in Web Forms », *A List Apart* (étude Etre). https://alistapart.com/article/inline-validation-in-web-forms/
19. Sherwin K., « Placeholders in Form Fields Are Harmful », Nielsen Norman Group, 2014. https://www.nngroup.com/articles/form-design-placeholders/
20. Neusesser T., Sunwall E., « Error-Message Guidelines », Nielsen Norman Group, 2023. https://www.nngroup.com/articles/error-message-guidelines/
21. Budiu R., « Wizards: Definition and Design Recommendations », Nielsen Norman Group, 2017. https://www.nngroup.com/articles/wizards/

**Confiance, B2B, conversion**

22. Harley A., « Trustworthiness in Web Design: 4 Credibility Factors », Nielsen Norman Group, 2016. https://www.nngroup.com/articles/trustworthy-design/
23. Fessenden T., « What B2B Designers Can Learn from B2C About Building Trust », Nielsen Norman Group, 2019. https://www.nngroup.com/articles/b2b-trust-from-b2c/
24. Nielsen J., « Show Prices for Common Scenarios », Nielsen Norman Group, 2006. https://www.nngroup.com/articles/show-prices-for-common-scenarios/
25. Nielsen Norman Group, rapport « B2B Website Usability for Converting Users into Leads and Customers » (188 recommandations). https://www.nngroup.com/reports/b2b-websites-usability/
26. Fogg B. J., « Stanford Guidelines for Web Credibility », Stanford Persuasive Technology Lab, 2002. https://credibility.stanford.edu/guidelines/index.html
27. Fogg B. J. et al. (2003), « How do users evaluate the credibility of Web sites? A study with over 2,500 participants », *Proceedings of DUX 2003*.
28. Nielsen J., « Photos as Web Content », Nielsen Norman Group, 2010. https://www.nngroup.com/articles/photos-as-web-content/
29. Gartner (ex-CEB), enquête auprès de 750 acheteurs B2B : environ 17 % du temps d'achat passé avec les fournisseurs. Chiffre largement repris, source primaire payante, non consultée directement : ordre de grandeur seulement. Il éclaire le parcours P2/P3, où l'essentiel de l'évaluation se fait sans contact.
30. Oldroyd J. B., McElheran K., Elkington D. (2011), « The Short Life of Online Sales Leads », *Harvard Business Review*, 89(3). https://hbr.org/2011/03/the-short-life-of-online-sales-leads
31. Spiegel Research Center (Northwestern University), « How Online Reviews Influence Sales », 2017. https://spiegel.medill.northwestern.edu/How-Online-Reviews-Influence-Sales
32. Google / Ipsos, « The Role of Click to Call in the Path to Purchase » (2013 : 70 % des personnes qui cherchent sur mobile utilisent l'appel direct) ; Google France (2015). https://www.thinkwithgoogle.com/_qs/documents/1454/click-to-call_research-studies_hz2ytgv.pdf
33. Google, « Contenus interdits et soumis à des restrictions » (avis : sollicitation sélective et incitations interdites) ; « Conseils pour obtenir plus d'avis ». https://support.google.com/contributionpolicy/answer/7400114?hl=fr · https://support.google.com/business/answer/3474122?hl=fr

**Psychologie de la persuasion et de la décision**

34. Cialdini R. B. (2021), *Influence, New and Expanded: The Psychology of Persuasion*, Harper Business (7 principes, dont l'unité).
35. Freedman J. L., Fraser S. C. (1966), « Compliance without pressure: The foot-in-the-door technique », *Journal of Personality and Social Psychology*, 4(2), 195-202.
36. Kivetz R., Urminsky O., Zheng Y. (2006), « The goal-gradient hypothesis resurrected », *Journal of Marketing Research*, 43(1), 39-58.
37. Nunes J. C., Drèze X. (2006), « The endowed progress effect », *Journal of Consumer Research*, 32(4), 504-512.
38. Langer E., Blank A., Chanowitz B. (1978), « The mindlessness of ostensibly thoughtful action », *Journal of Personality and Social Psychology*, 36(6), 635-642.
39. Regan D. T. (1971), « Effects of a favor and liking on compliance », *Journal of Experimental Social Psychology*, 7(6), 627-639.
40. Burger J. M., Messian N., Patel S., del Prado A., Anderson C. (2004), « What a coincidence! The effects of incidental similarity on compliance », *Personality and Social Psychology Bulletin*, 30(1), 35-43.
41. Zajonc R. B. (1968), « Attitudinal effects of mere exposure », *Journal of Personality and Social Psychology*, 9(2, Pt. 2), 1-27.
42. Bornstein R. F. (1989), « Exposure and affect: Overview and meta-analysis of research, 1968-1987 », *Psychological Bulletin*, 106(2), 265-289.
43. Hasher L., Goldstein D., Toppino T. (1977), « Frequency and the conference of referential validity », *Journal of Verbal Learning and Verbal Behavior*, 16(1), 107-112 (effet de vérité illusoire).
44. Krugman H. E. (1972), « Why three exposures may be enough », *Journal of Advertising Research*, 12(6), 11-14.
45. Kahneman D., Tversky A. (1979), « Prospect theory: An analysis of decision under risk », *Econometrica*, 47(2), 263-291.
46. O'Keefe D. J., Jensen J. D. (2007), « The relative persuasiveness of gain-framed and loss-framed messages for encouraging disease prevention behaviors: A meta-analytic review », *Journal of Health Communication*, 12(7), 623-644.

    46b. Witte K., Allen M. (2000), « A meta-analysis of fear appeals: Implications for effective public health campaigns », *Health Education & Behavior*, 27(5), 591-615.
47. Hick W. E. (1952), « On the rate of gain of information », *Quarterly Journal of Experimental Psychology*, 4(1), 11-26.
48. Fitts P. M. (1954), « The information capacity of the human motor system in controlling the amplitude of movement », *Journal of Experimental Psychology*, 47(6), 381-391 ; Nielsen Norman Group, « Fitts's Law and Its Applications in UX ». https://www.nngroup.com/articles/fitts-law/
49. Murdock B. B. (1962), « The serial position effect of free recall », *Journal of Experimental Psychology*, 64(5), 482-488.
50. Kahneman D., Fredrickson B. L., Schreiber C. A., Redelmeier D. A. (1993), « When more pain is preferred to less: Adding a better end », *Psychological Science*, 4(6), 401-405 ; Kane L., « The Peak–End Rule: How Impressions Become Memories », Nielsen Norman Group, 2018. https://www.nngroup.com/articles/peak-end-rule/
51. Scheibehenne B., Greifeneder R., Todd P. M. (2010), « Can there ever be too many options? A meta-analytic review of choice overload », *Journal of Consumer Research*, 37(3), 409-425 ; Chernev A., Böckenholt U., Goodman J. (2015), « Choice overload: A conceptual review and meta-analysis », *Journal of Consumer Psychology*, 25(2), 333-358.
52. Mathur A. et al. (2019), « Dark Patterns at Scale: Findings from a Crawl of 11K Shopping Websites », *Proceedings of the ACM on Human-Computer Interaction* (CSCW). https://arxiv.org/abs/1907.07032
53. OCDE (2022), « Dark commercial patterns », *OECD Digital Economy Papers*, n° 336. https://doi.org/10.1787/44f5e846-en

**Droit suisse et achats publics**

54. Code des obligations (RS 220) : art. 259d (réduction de loyer), 260 (rénovation par le bailleur), 260a (rénovation par le locataire), 367 ss (contrat d'entreprise). https://www.fedlex.admin.ch/eli/cc/27/317_321_377/fr
55. Office fédéral de la justice, « Responsabilité pour les défauts de construction » (révision du CO en vigueur le 1.1.2026 : avis des défauts dans les 60 jours, droit à la réfection non excluable pour un élément de construction, prescription de 5 ans inchangée). https://www.bj.admin.ch/fr/responsabilite-pour-les-defauts-de-construction
56. Code civil (RS 210) : art. 647c à 647e (travaux nécessaires, utiles, somptuaires), 712g (PPE). https://www.fedlex.admin.ch/eli/cc/24/233_245_233/fr
57. Norme SIA 118, *Conditions générales pour l'exécution des travaux de construction* : délai de garantie de deux ans (art. 172 ss), applicable lorsque le contrat s'y réfère.
58. État de Genève, Service des affaires communales, « Pour des marchés publics durables, cap sur l'AIMP révisé », 10.06.2025. https://www.ge.ch/document/marches-publics-durables-cap-aimp-revise
59. État de Genève, « Rôle des autorités adjudicatrices : principes, types de procédures, cadre légal » (seuils du second œuvre). https://www.ge.ch/role-autorites-adjudicatrices-marches-publics/principes-types-procedures-cadre-legal
60. Guide romand pour les marchés publics (CROMP), annexe P2 « Attestations requises ». https://www.vd.ch/fileadmin/user_upload/organisation/dinf/sg-dinf/guide_romand/p2-attestations-requises.doc ; État de Genève, engagement OCIRT ou CCT : https://www.ge.ch/document/41978/telecharger
61. KBOB, guide pour l'acquisition de prestations d'ouvrage, annexe 2 (2025) : plausibilité de l'offre, fiabilité du prix. https://www.kbob.admin.ch/dam/fr/sd-web/giRb7Gp3jETV/20250701_KBOB-Leitfaden%20zur%20Beschaffung%20von%20Werkleistungen%20-%20Anhang%202_V1.0_Publikation_FR.pdf
62. Loi contre la concurrence déloyale (RS 241), art. 3 al. 1 let. o ; OFCOM, « When is mass sending allowed? » (consentement préalable, exception clients existants, expéditeur identifié, refus simple et gratuit). https://www.bakom.admin.ch/en/when-is-mass-sending-allowed
63. État de Genève, « Subventions énergétiques 2026 : 80 millions de francs pour accélérer la rénovation du parc bâti genevois », 02.02.2026 (demande à déposer avant le début des travaux). https://www.ge.ch/blog/geneve-energie/subventions-energetiques-2026-80-millions-francs-accelerer-renovation-du-parc-bati-genevois-2-02-2026
