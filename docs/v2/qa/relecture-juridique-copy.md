# Relecture juridique et copy : messages automatiques, confidentialité, textes légaux

*QA phase 4 · 31 octobre 2026 · relecteur conformité (nLPD, LCD, LTC, CO) et correcteur (français de Suisse romande)*

**Périmètre.** `automation/messages/*.md` (16 fichiers), `site/api/modeles/*.txt` (3 accusés), `docs/v2/automatisation.md` §8 (registre) et §9 (politique de confidentialité), copy deck §A.5 (mention sous le formulaire), §L (mentions légales), §M (confidentialité).
**Références.** Programme v2, décisions D1 à D8, personas §1.6 et §5 (liste noire), copy deck §0 et §R (codes `Cxx`), stratégie §9.
**Hors périmètre, non modifié.** Pages HTML, `tools/build/`, code PHP hors `modeles/`.

**Contrôles après corrections**

| Commande | Résultat |
|---|---|
| `php site/api/tests/run.php` | 262 vérifications, 0 échec (dont l'identité des 3 accusés md ↔ txt ; total augmenté par les tests d'autres agents) |
| `python3 automation/n8n/verifier.py` (avec `luxon` dans `NODE_PATH`) | 16 workflows, 33 contrôles, 0 erreur |
| Comparaison `automation/messages/` ↔ objets `MODELES` des nœuds Code n8n | 0 écart (21 modèles resynchronisés) |
| Longueur des SMS aux prospects, valeurs les plus longues, alphabet GSM | 158 · 159 · 158 · 150 caractères (1 SMS chacun, aucun lien) |

Convention typographique constatée et conservée : apostrophe droite, espace simple avant « : ; ? ! » (comme le copy deck, dont le générateur ajoute les insécables), guillemets « » dans les e-mails, guillemets droits dans les SMS (alphabet GSM). Harmonisé : « STOP » entre guillemets dans tous les pieds d'e-mails.

---

## 1. Corrections faites

### 1.1 Messages automatiques

| Fichier | Avant → après | Raison | Base légale |
|---|---|---|---|
| `accuse-reception-devis.md` = `modeles/accuse-devis.txt` | « Le {{tel_fixe}}, {{horaires}} (référence…) » → « Le {{tel_fixe}}{{#horaires}}, {{horaires}}{{/horaires}} (référence…) » | Horaires non confirmés (`C03`). Le repli du copy deck (horaires masqués) produisait une virgule orpheline. Maintenant : `entreprise.horaires => ''` suffit. | LCD art. 3 al. 1 let. b (pas d'horaire inexact) |
| `accuse-reception-rappel.md` = `modeles/accuse-rappel.txt` | Même correction | Idem | Idem |
| `accuse-reception-guide.md` = `modeles/accuse-guide.txt` | Même correction ; « Votre adresse sert uniquement à cet envoi » → « Votre adresse **postale** sert uniquement à cet envoi » ; « Répondez STOP » → « Répondez « STOP » » | Avec la case « conseils », l'adresse e-mail sert aussi aux conseils : la phrase devenait fausse. | nLPD art. 6 al. 3, art. 19 |
| Les 3 accusés (métadonnées, hors bloc envoyé) | « À valider : horaires… » → codes `C01`, `C03`, `C09`, `C30` avec leur repli de configuration ; raison de commerce complète dans la signature | Cohérence avec les marqueurs du copy deck ; un marqueur `[À CONFIRMER]` ne peut pas figurer dans un texte envoyé | CO art. 954a |
| `demande-avis.md` (avis-j2) | « Que vous soyez satisfait(e) ou que quelque chose aurait pu être mieux fait » → « Que vous soyez satisfait(e) ou que vous ayez des réserves » | Concordance des modes | — |
| `demande-avis.md` (avis-j2) | « Et si un point n'est pas en ordre, dites-le-nous d'abord : nous revenons. » → « Et si un point n'est pas en ordre, vous pouvez aussi nous le dire directement, en répondant à ce message. » | « D'abord » détourne les clients mécontents de l'avis public (filtrage des avis). « Nous revenons » promet une retouche non confirmée (`C32`). | Règles Google sur les avis ; LCD art. 3 al. 1 let. b |
| `demande-avis.md` (reference-pro-j2) | Pas de pied → pied d'opposition (« STOP » ou lien) | Même traitement que les particuliers (prudence) | LCD art. 3 al. 1 let. o |
| `demande-avis.md` (accord-photos-j14) | « sur notre site » → « sur notre site, sur notre fiche Google, sur notre page LinkedIn et dans notre dossier de références » | La stratégie publie les photos sur ces supports (§3.1, §3.6, §4). Un accord limité au site ne les couvre pas. | nLPD art. 6 al. 6 (accord éclairé) ; CC art. 28 |
| `demande-avis.md` (métadonnées) | Ajout : « Opposition » (WF03d doit lire l'opposition) et « À valider » (litige, réserves, supports photo) | Défauts constatés dans WF03d (§3) | LCD art. 3 al. 1 let. o ; règles Google |
| `sms-prospects.md` (sms-demande-avis) | 250 caractères, « cherchez "Andy Construct" sur Google Maps… Le lien direct est dans notre e-mail », sans opposition → « Andy Construct : merci de votre confiance. Si vous le souhaitez, laissez un avis sur notre fiche Google Maps. Pour ne plus recevoir nos SMS : +41 22 771 20 15 » (158) | Trop long (2 SMS) ; « le lien est dans notre e-mail » faux quand le client n'a pas d'e-mail ; pas d'opposition. L'expéditeur alphanumérique ne reçoit pas de réponse : opposition par téléphone. | LCD art. 3 al. 1 let. o |
| `sms-prospects.md` (sms-accuse) | « Andy Construct : votre demande (réf. {{ref}}) est bien arrivée. … » (jusqu'à 175) → « Andy Construct : demande {{ref}} bien arrivée. … » (158 au plus) | Plus de 160 caractères | — |
| `sms-prospects.md` (sms-essai-appel) | « …au sujet de votre demande ({{service}}). Vous pouvez nous rappeler au +41 22 771 20 15, du lundi au vendredi de 7 h à 18 h. » (213) → « Andy Construct : nous avons essayé de vous joindre aujourd'hui à {{heure}} au sujet de {{service}}. Vous pouvez nous rappeler au +41 22 771 20 15. » (159) | Longueur ; « votre demande (votre isolation acoustique) » ; horaires non confirmés (`C03`) ; « Un associé » en majuscule après les deux-points | LCD art. 3 al. 1 let. b |
| `sms-prospects.md` (sms-veille-visite) | « pour votre projet ({{service}}) » → « pour {{service}} » ; variable `jour` documentée | Répétition (« votre projet (vos travaux…) ») | — |
| `sms-prospects.md` (métadonnées) | Ajout des lignes « Longueur » (valeurs les plus longues et résultats) et « Opposition » | Contrôle reproductible | — |
| `rappel-sans-reponse.md` (2 modèles) | « au sujet de votre demande ({{service}}) » → « au sujet de {{service}} » ; « …au {{tel_fixe}}, du lundi au vendredi de 7 h à 18 h. » → « …au {{tel_fixe}}. » | Répétition ; horaires non confirmés, codés en dur dans n8n (sans variable de repli). Texte à rétablir une fois `C03` confirmé (noté dans le fichier). | LCD art. 3 al. 1 let. b |
| `relances-offre.md` (J+10) | « Pour faciliter la comparaison, la nôtre détaille chaque poste ; elle comprend la protection des lieux, le nettoyage et la réception du chantier avec vous. » → « Si un point de la nôtre mérite une explication, je vous la donne volontiers. » | Engagements `C06`, `C07` non confirmés. La version enrichie est conservée dans « À valider ». | LCD art. 3 al. 1 let. b |
| `relances-offre.md` (À valider) | Ajout : sans téléphone, J+3, J+10 et J+21 font **trois** e-mails | Contredit le plafond « deux relances écrites » (personas §5) | — |
| `sequence-aimant.md` (bruit E3) | « nous passons toujours voir avant de proposer quoi que ce soit » → « nous préférons voir les lieux avant de faire une offre » ; « une offre écrite et détaillée » → « une offre écrite » | `C06` non confirmé (repli du copy deck) | LCD art. 3 al. 1 let. b |
| `sequence-aimant.md` (Canal) | « E-mail (Brevo, transactionnel) » → API « transactionnelle » de Brevo, mais **pas** un message transactionnel au sens juridique | Éviter qu'on supprime un jour la désinscription au nom du mot « transactionnel » | LCD art. 3 al. 1 let. o |
| `sequence-aimant.md` (À valider) | Ajout : `C14`, `C17`, `C20` ; séries « régie » à ne pas activer sans `C17` ; appel de courtoisie non annoncé | Voir §3 | nLPD art. 6 al. 3 |
| `entretien.md`, `offre-perdue-6-mois.md`, `sequence-aimant.md`, `demande-avis.md` | « Répondez STOP » → « Répondez « STOP » » (12 pieds) | Typographie cohérente avec les pages de désinscription et la politique | — |
| `entretien.md` (À valider) | Ajout : `C32` (ne pas activer « Peinture, 23 mois » sans confirmation), `C17` (régies), `C33` ; passage facturé annoncé avant le rendez-vous ; phrase « exception clients » dans l'offre ou la commande | Promesse implicite de gratuité ; condition de l'exception clients | LCD art. 3 al. 1 let. b et o |
| `desinscription.md` (page après confirmation) | « Vous ne recevrez plus nos e-mails. » → « Vous ne recevrez plus nos conseils ni nos informations. » | Contredisait la page de confirmation (les e-mails liés à une demande en cours restent possibles) | LCD art. 3 al. 1 let. b |
| `desinscription.md` (lien invalide) | « Pour ne plus recevoir nos e-mails, répondez… à l'un de nos messages » → « Pour ne plus recevoir nos conseils ni nos informations, répondez… à l'un de nos e-mails » | Même raison ; les SMS ne reçoivent pas de réponse | Idem |
| `prospection-lettres.md` (lettre régie) | « Nous travaillons notamment pour {{reference_1}} et {{reference_2}} » → « Nous avons notamment réalisé des travaux pour… » | Laissait croire à une relation en cours (D5 : « Ils nous ont confié des travaux » ; copy deck : pas de « partenaire ») | LCD art. 3 al. 1 let. b |
| `prospection-lettres.md` (3 lettres, touche 1) | Ajout sous la signature : « Vos coordonnées professionnelles proviennent de {{source_coordonnees}}. Elles servent uniquement à vous présenter notre entreprise. Comment nous les traitons : www.andyconstruct.ch/confidentialite.html » ; variable `source_coordonnees` | Données collectées ailleurs qu'auprès de la personne : elle doit être informée (catégories de données, finalité) au plus tard au premier contact | nLPD art. 19 al. 3 et 5 |
| `prospection-lettres.md` (À valider) | Ajout : `C07`, `C12`, `C13`, `C14`, `C16`, `C18`, `C20`, `C22`, `C35` ; raison de commerce complète en pied | Cohérence avec le copy deck | CO art. 954a |
| `prospection-script-appel.md` | « Beaucoup de régies gardent une deuxième entreprise » → « Certaines régies… » ; section « À valider » (`C12`, `C13`, `C40`, double opt-in de la lettre trimestrielle) | Généralisation invérifiable ; attestations non confirmées | LCD art. 3 al. 1 let. b et o |
| `automation/n8n/wf*.json` (8 fichiers) | Objets `MODELES` resynchronisés avec `automation/messages/` (21 modèles) | Les workflows embarquent les textes : sans cela, aucune correction n'atteint les envois réels (`automatisation.md` §5, point 7) | — |
| `automation/n8n/wf*.json` (9 fichiers) | Signature « Andy Construct · Route des Acacias 48, 1227 Carouge » → « Andy Construct, Chanton & Cie · Route des Acacias 48, 1227 Carouge » | La raison de commerce inscrite doit figurer, complète, dans la correspondance | CO art. 954a |

### 1.2 Registre des traitements (`automatisation.md` §8)

| Avant → après | Raison | Base légale |
|---|---|---|
| Demandes : ajout du type de client, du créneau, de « connu par », du **nom de la personne qui a recommandé** (champ `recommande_par` du formulaire) et du détail de la source (page, référent, UTM, `gclid` avec consentement) | Données réellement collectées | nLPD art. 12 |
| « purge WF04p » → liste envoyée à l'agence, effacement manuel tant que `AC_PURGE_AUTO=false` ; ajout des boîtes e-mail des associés et de l'historique n8n (30 jours) | Le code n'efface rien automatiquement par défaut ; les pièces jointes restent dans les boîtes | nLPD art. 6 al. 4 |
| Suivi des offres : « Relances de service » → 3 au plus en 3 semaines, demande d'avis J+2/J+9, recontact unique à 6 mois sur demande expresse | Traitements réels non décrits | nLPD art. 12 |
| **Nouvelle ligne** « Publication de photos et de témoignages » (accord J+14, supports publics dont Google) | Traitement réel non inscrit | nLPD art. 6 al. 6, art. 12 |
| Guide : Brevo « seulement si conseils » ; adresse postale 3 mois (procédure à créer) ; **appel de courtoisie de WF07 signalé** | Code de WF07 | nLPD art. 6 al. 3 |
| Statistiques : ajout appareil, navigateur, pays ou région ; « 24 mois (réglage Umami) » → Umami n'efface rien seul, tâche de purge à prévoir | Umami auto-hébergé ne connaît pas de durée de conservation | nLPD art. 6 al. 4 |
| Attribution : ajout du repère « formulaire commencé » (`ac_debut_*` en stockage de session) et du refus par les réglages du navigateur | `suivi.js` | LTC art. 45c |
| Sécurité du formulaire : « 24 h » → empreinte complète 24 h, **12 caractères de l'empreinte 30 jours** dans le journal | `Journal` garde un extrait de l'empreinte 30 jours | nLPD art. 6 al. 4 |
| **Nouvelle ligne** « Journaux du serveur web » (IP complète, durée de l'hébergeur à relever) | Traitement inévitable, absent | nLPD art. 12 |
| Sous-traitants : ajout du fournisseur de messagerie et du pays de l'agence ; transferts « vers l'UE uniquement » → sous réserve des sous-traitants ultérieurs de Pipedrive et Brevo ; photos publiées sur Google | Exactitude | nLPD art. 9, 16 |

### 1.3 Politique de confidentialité (`automatisation.md` §9)

| Avant → après | Raison | Base légale |
|---|---|---|
| « Ces informations servent **uniquement** à traiter votre demande… Elles ne sont ni vendues ni utilisées pour de la publicité. » puis, plus bas, envoi d'informations commerciales aux clients → nouvelle section « À quoi elles servent » : traitement de la demande, comptage de la provenance sans nom, remerciement de la personne qui a recommandé ; « pas de publicité, seule exception : clients informés à la commande » | Contradiction interne de la politique | nLPD art. 6 al. 2 et 3, art. 19 al. 2 |
| Données reçues : ajout civilité, situation (propriétaire, régie…), préférence de contact, « connu par », personne qui a recommandé, page d'envoi et site d'origine | Exactitude | nLPD art. 19 |
| Score : « type de travaux, ampleur, lieu, délai » → ajout du type de client et de la provenance | La grille utilise aussi ces critères | nLPD art. 19, art. 21 |
| « nous pouvons vous demander, une ou deux fois, si vous avez des questions » → « au plus trois fois en trois semaines » ; ajout des messages d'appel sans réponse (arrêt après trois essais) et du recontact unique à six mois | Ce que fait WF03c et WF02 | nLPD art. 19 |
| Après un chantier : ajout du SMS, de « sans tri et sans contrepartie », de la demande d'accord pour les photos ; exemple « contrôle des peintures deux ans après » → « faire le point un an après les travaux » | Exhaustivité ; l'exemple reposait sur `C32` non confirmé | nLPD art. 19 ; LCD art. 3 al. 1 let. b |
| **Nouvelle section** « Si vous êtes un professionnel que nous contactons » (source annuaire, données, astérisque, opposition, 24 mois) | Prospection B2B non couverte ; données non collectées auprès de la personne | nLPD art. 19 al. 3 |
| Prestataires : ajout messagerie, Pingen, Healthchecks.io, pays de l'agence ; crochet pour les sous-traitants ultérieurs hors UE ; photos publiques sur Google | Exhaustivité, transferts | nLPD art. 19 al. 2 et 4, art. 16 |
| « ensuite seulement dans le dossier de votre demande » → « (outil de suivi et messagerie des associés), avec la même durée que la demande » | Les pièces jointes partent aussi par e-mail interne | nLPD art. 19 |
| « Adresse IP : sous forme **chiffrée**, 24 heures au plus » → « jamais enregistrée en clair ; empreinte codée 24 h ; extrait 30 jours dans le journal technique » | Un hachage n'est pas un chiffrement ; durée réelle du journal | nLPD art. 19, art. 6 al. 4 |
| Durées ajoutées : adresse postale du guide (3 mois), e-mail des conseils (24 mois au plus), liste d'opposition, journaux de l'hébergeur, historique n8n, sauvegardes, statistiques | Durées du registre absentes de la politique | nLPD art. 19 ; art. 6 al. 4 |
| Statistiques : « sur notre propre serveur » → « sur un serveur que nous louons en Suisse (Infomaniak) » ; ajout des données relevées (appareil, navigateur, pays ou région), du repère « formulaire commencé » et du refus par les réglages du navigateur | Exactitude ; obligation d'indiquer comment refuser | LTC art. 45c |
| Droits : ajout « gratuitement », copie électronique, retrait d'un accord (conseils, photos) | Droits d'accès, de remise des données, retrait du consentement | nLPD art. 25, 28, 30 |
| §10 (check-list de mise en production) : ajout de la reprise du §9 corrigé dans `tools/build/page_autres.py` et du renvoi à ce rapport | La page publiée contient encore l'ancien texte | — |

### 1.4 Copy deck (erreurs nettes seulement)

| Section | Avant → après | Raison |
|---|---|---|
| L « Hébergement » | Repli « Le site est hébergé en Suisse. » → ligne masquée ; texte principal avec `{{pays}}` | Le repli affirmait un fait non confirmé (`C34`) ; la préproduction (harbor-digital.fr) n'est pas forcément en Suisse. Règle « aucune invention présentée comme vraie » ; LCD art. 3 al. 1 let. b. |
| R.1 `C34` | Repli « Le site est hébergé en Suisse » → « Ligne masquée » ; question étendue au pays | Cohérence avec L |
| A.5 | « Case de consentement (tant que l'API l'exige) » et « Mention d'information (si la case est retirée après avis du juriste) » → case abandonnée (D2, l'API ignore `accord`), mention = texte retenu, avec `[À VÉRIFIER : relecture juridique]` | Statut périmé depuis D2 |

---

## 2. Points signalés, non corrigés (style, décision ou hors périmètre)

1. **Mention sous le formulaire et réassurance** (A.5, aussi dans `tools/build/composants.py`) : « Elles ne servent à rien d'autre » et « Vos coordonnées servent uniquement à votre demande. Pas de publicité. » restent défendables pour les **coordonnées** pendant la phase de demande (les usages ultérieurs naissent du contrat et sont annoncés à la commande). Formulation plus sûre, à soumettre à l'avocat : « En envoyant ce formulaire, vous nous transmettez vos coordonnées pour traiter votre demande. Nous ne les vendons pas et ne les utilisons pas pour de la publicité. » Les accusés gardent la même promesse (« uniquement… ni vendues ni utilisées pour de la publicité ») pour rester alignés : à changer en même temps si la mention change.
2. **L « Propriété des contenus »** : « Les textes, le logo et les photos… appartiennent à Andy Construct, Chanton & Cie » n'est exact qu'avec une cession écrite des droits de l'agence (textes) et des auteurs des photos (ouvriers, tiers : `C25`). Sinon : « sont protégés par le droit d'auteur ; leur reproduction demande un accord écrit ».
3. **L « Références citées »** : les noms de marques privées en texte (UBS, Piaget au bandeau §A.6) demandent le même accord que les logos (`C22`).
4. **Q.4 (guide par la poste)** : périmé par rapport à `contrat-interface.md` §6 et à D2 (case `accord`, champ `adresse_postale` unique, profils). Le formulaire généré suit déjà le contrat d'interface. Dans `composants.py`, « désinscription en un clic » est inexact (lien puis bouton « Confirmer ») : écrire « désinscription par un lien ».
5. **`tools/build/page_autres.py`** : la page `confidentialite.html` publiée contient l'ancienne politique (« uniquement », « une ou deux fois », « sous forme chiffrée »). À reprendre depuis le §9 corrigé par le développeur frontend.
6. **I.8 et Q.3** (droit des défauts au 1.1.2026, art. 259d et 260 CO) : déjà marqués `[À VÉRIFIER : relecture juridique]`, renvoyés à l'avocat (§3).
7. **M** : titre, meta et chapeau conformes ; rien à corriger.

---

## 3. Points nécessitant un avocat

1. **Demande d'avis automatisée** (e-mail et SMS J+2, relance J+9) : message de service lié au contrat ou publicité de masse au sens de l'art. 3 al. 1 let. o LCD ? Une opposition par appel au +41 22 771 20 15 (l'expéditeur SMS alphanumérique ne reçoit pas de réponse) est-elle « facile et gratuite » ?
2. **Exception « clients »** (entretien à un et deux ans, message annuel aux régies) : les coordonnées sont collectées par le formulaire **avant** la vente. L'information donnée dans l'offre ou la confirmation de commande satisfait-elle à « lors de la vente » ? Valider la phrase (stratégie §9.2, point 4) et son emplacement.
3. **Caractère « de masse »** des séquences automatisées personnalisées (entretien, régies, deux conseils du guide) et suffisance de la case non cochée comme consentement préalable pour les conseils.
4. **Mention d'information sans case** (D2) : suffisance de « Elles ne servent à rien d'autre » + lien, au regard de l'art. 19 nLPD et des usages ultérieurs (statistiques de provenance, avis, exception clients) ; formulation du §2, point 1.
5. **Transferts** : sous-traitants ultérieurs de Pipedrive OÜ et de Brevo hors UE (support, infrastructure). Faut-il les nommer, avec la garantie, dans la politique (nLPD art. 16 et 19 al. 4) ?
6. **Demande d'avis décalée** en cas de litige ou de réserves non levées : risque de sollicitation sélective (règles Google, LCD art. 3 al. 1 let. b) ; faut-il un délai maximal après lequel la demande part quand même ?
7. **Registre** : dispense de l'art. 24 OPDo (moins de 250 collaborateurs, pas de risque élevé) ; le registre est tenu quand même.
8. **Textes de droit matériel du copy deck** : I.8 (avis des défauts en 60 jours, réfection gratuite non excluable pour les ouvrages immobiliers, prescription de 5 ans, garantie SIA 118 de 2 ans, contrats conclus depuis le 1.1.2026) et Q.3 (réduction de loyer, art. 259d et 260 CO) ; cession des droits d'auteur (§2, point 2).

---

## 4. Check-list de conformité avant mise en ligne

**Bloquant (code et configuration)**
- [ ] **WF03d** (avis) : lire `opposition_marketing`, `ne_pas_relancer` et `a_repondu` avant J+9, J+14 et le SMS. Aujourd'hui un « STOP » au J+2 n'arrête pas les messages suivants (LCD art. 3 al. 1 let. o).
- [ ] **WF07** (guide) : désactiver la tâche « Appel de courtoisie » des profils professionnels, ou l'annoncer sur le formulaire et dans la politique. Elle contredit « Pas de publicité » et « Votre adresse postale sert uniquement à cet envoi » (nLPD art. 6 al. 3). Le formulaire actuel ne propose que des profils de particuliers : le risque apparaît avec un formulaire « régie ».
- [ ] **`config.php`** : `entreprise.nom` = « Andy Construct, Chanton & Cie » (signature des accusés, CO art. 954a ; à reporter aussi dans `config.example.php`) ; `entreprise.horaires` = `''` tant que `C03` n'est pas confirmé ; `promesse_delai` = `false` tant que `C01` ne l'est pas.
- [ ] **Relances d'offre sans téléphone** : trancher entre 2 e-mails (supprimer le J+10 écrit) et 3 (ce que dit maintenant la politique).
- [ ] **Purges** : `AC_PURGE_AUTO=true` ou procédure mensuelle écrite ; boîtes e-mail des associés (24 mois) ; adresse postale du guide (3 mois, note de tâche Pipedrive) ; contacts Brevo (24 mois au plus) ; Umami (24 mois, tâche SQL sur le VPS).
- [ ] **Exception clients** : phrase d'information dans le modèle d'offre et la confirmation de commande ; `info_exception_client` rempli seulement après.
- [ ] **Page publiée** : `tools/build/page_autres.py` reprend le §9 corrigé ; mentions légales sans « hébergé en Suisse » tant que `C34` manque.

**Contrats et documents**
- [ ] DPA signés ou acceptés et archivés : hébergeur, messagerie, Infomaniak, Pipedrive, Brevo, ASPSMS, Pingen (si utilisé), Healthchecks.io, agence.
- [ ] Sous-traitants ultérieurs de Pipedrive et Brevo relevés ; politique complétée s'il y a un pays hors UE.
- [ ] Crochets de la politique remplis : hébergeur et pays, messagerie, pays de l'agence, durée des journaux de l'hébergeur, durée Umami, e-mail de contact (`C30`), date de mise à jour.
- [ ] Accords écrits archivés : logos et noms de marques privées (`C22`), photos (`C25`), témoignages (`C44`).
- [ ] Avis de l'avocat sur les points du §3.

**Confirmations client qui conditionnent des messages**
- [ ] `C01` délai de rappel et `C03` horaires (accusés, SMS, essai d'appel).
- [ ] `C06`, `C07` (relance J+10, E3 « bruit » : versions enrichies dans « À valider »).
- [ ] `C32` : ne pas activer « Peinture, 23 mois » (WF04i) avant confirmation ; passage facturé annoncé avant le rendez-vous.
- [ ] `C17` : ne pas activer « Régies, chaque année » ni l'E3 « régie » avant confirmation. `C20` : modèle d'avis aux locataires existant avant l'E2 « régie ».
- [ ] `C12`, `C13`, `C35` (attestations dans les lettres, le script et l'e-mail après appel) ; `C14`, `C18` (lettre architecte) ; `C09`, `C30` (associé nommé, numéros).

**Vérifications techniques avant l'ouverture**
- [ ] Aucun cookie en production (outils du navigateur, y compris ceux de l'hébergeur) ; stockage de session limité à `ac_src` et `ac_debut_*` ; rien avec Do Not Track ou GPC.
- [ ] Envoi réel des 4 SMS prospects sur un mobile : un seul SMS chacun, aucun lien, aucun caractère remplacé (« recu », « ete »).
- [ ] Pied d'opposition présent et fonctionnel (réponse « STOP » détectée par WF14, lien → page « Confirmer » → opposition datée dans Pipedrive et Brevo) dans : avis, référence pro, entretien, régies, offre perdue, conseils, accusé guide avec conseils.
- [ ] Accusés rendus avec `horaires` vide : pas de virgule orpheline.
- [ ] Lettres B2B : `source_coordonnees` rempli ; pied avec raison de commerce complète, adresse et IDE.
- [ ] Après toute modification d'un texte : `automation/messages/` et les objets `MODELES` des workflows identiques, puis `php site/api/tests/run.php` (0 échec) et `python3 automation/n8n/verifier.py` (0 erreur).
