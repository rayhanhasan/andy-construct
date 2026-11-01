# HANDOFF — Andy Construct, site d'acquisition (v3)

Document de passation pour reprendre le projet en local (Claude Code ou à la main).
Mise à jour : 1er novembre 2026 (v4 : audit SEO, plan de mix d'acquisition, plans du tableau de bord admin ; voir §5). État du site : **v3 (refonte visuelle « le trait de niveau ») livrée sur les 13 pages, testée et poussée ; en attente de validation client, des accords écrits pour les logos et de la mise en place des outils (SMTP, n8n, CRM)**. La v2 (stratégie, copy, API, automatisation) reste la base : la v3 change le design, la preuve sociale, les images et ajoute les drapeaux A/B.

---

## 1. Démarrage rapide

```bash
git clone https://github.com/rayhanhasan/andy-construct.git
cd andy-construct && git checkout claude/eager-heisenberg-sz3nve

python3 tools/build/build.py                     # régénère site/ (mode preview)
cd site && php -S localhost:8080                 # site + formulaire (PHP 8.x)
php site/api/tests/run.php                       # tests de l'API (266)
python3 automation/n8n/verifier.py               # contrôle des 16 workflows
```

Pour reprendre avec Claude Code :

> Lis HANDOFF.md, README.md, docs/v3/brief-v3.md, docs/v3/direction-artistique.md, docs/v3/cro-v3.md et docs/v2/decisions-chef-de-projet.md. Tu es chef de projet du site d'acquisition Andy Construct (v3). Lis `.claude/skills/frontend-design/SKILL.md` avant toute décision visuelle. Reprends à la section « Prochaines étapes ».

Prérequis : Python 3.10+ (générateur sans dépendance ; Pillow seulement pour `tools/build/images.py` et les scripts de `livrables/sources/`), PHP 8.1+ pour l'API, Node 18+ et Playwright pour les captures, Docker pour n8n auto-hébergé.

Recette rapide de la v3 (sur le serveur local) :
- `index.html?flag=hero-media:b` : héro avec la vidéo d'ambiance (désactivée par défaut, décision client en attente) ;
- `index.html?flag=hero-titre:b` : variante de titre ; `?flag=reset` pour revenir au tirage normal ;
- mode `verification` pour voir les points Cxx soulignés avec leur code.

---

## 2. Dépôt

| Élément | Valeur |
|---|---|
| Dépôt | `rayhanhasan/andy-construct` — **⚠️ PUBLIC et indexé : à passer en privé** (Settings → Danger Zone → Change visibility) |
| Branche | `claude/eager-heisenberg-sz3nve` (tout est poussé) ; pas de pull request |
| Versions | maquette v1 = commit `ec5f98d` · v2 livrée = `a633851` · accueil v3 = `48b0829` · v3 sur toutes les pages = `7c38ca0` (les tags n'ont pas pu être poussés par le proxy) |
| Skills du projet | `.claude/skills/` (versionnés) : `frontend-design`, `webapp-testing`, `theme-factory` (Anthropic) ; `cro`, `copywriting`, `copy-editing`, `marketing-psychology`, `ab-testing`, `conversion-tracking`, `seo-audit`, `ai-seo`, `schema`, `site-architecture`, `image`, `lead-magnets`, `offers`, `competitor-profiling`, `customer-research`, `ads` (marketingskills, licence MIT). Contexte lu par les skills marketing : `.claude/product-marketing.md` |
| Secrets | aucun dans le dépôt ; `site/api/config.php`, `site/api/stockage/`, `automation/.env`, `automation/donnees/` sont ignorés par git |

---

## 3. Le client (faits vérifiés)

- **Andy Construct, Chanton & Cie**, société en nom collectif, Route des Acacias 48, 1227 Carouge GE (siège depuis 05.2023 ; adresse de domiciliation partagée par ~92 entreprises → fiche Google en « zone desservie »). IDE CHE-113.706.162. Activité depuis le **01.06.2007** (Perly-Certoux → Chêne-Bourg 2010 → Carouge 2023). Associés : Adnan Bajrami, Caroline Chanton Bajrami.
- Tél. +41 22 771 20 15 · mobile +41 78 631 14 34 · andy.construct@bluewin.ch (recommandé : contact@andyconstruct.ch).
- **Services (validés par le client)** : Placo · Peinture · Isolation acoustique · Cloisons isothermes (affichées « Cloisons isolantes », D1).
- **Zone (validée)** : toute la Suisse romande. **Audience (v3)** : 30-60 ans (gérants de régie, architectes, responsables techniques, propriétaires actifs), sobre et formel mais moderne ; allergique à l'exagéré.
- 18 références publiques (Ville de Genève, Conservatoire, HEAD, OMC, UBS, Piaget, salles communales…). Membre du GGE selon l'annuaire (à confirmer). Aucun avis client public nulle part. Facebook = profil personnel fermé (pas de page entreprise).
- Détail : `docs/v2/dossier-client.md`.

---

## 4. Demande du client pour la v2 (résumé)

Version définitive, **site d'acquisition** : tous les agents et skills utiles, audits, analyse concurrentielle, copywriting corrigé et adapté à l'audience, CRO avec travail psychologique, ergonomie (moins de texte, meilleur portfolio, même style sobre), **logos des références répétés** (sous l'en-tête, pied de page…), **stratégie d'acquisition et automatisation complètes**.

### 4 bis. Retour du client sur la v2 → v3

« Tout le monde peut faire ça » : le contrat a été gagné en promettant un site **beau, magnifique**, plus **structuré et formel**, **un peu animé** sans extravagance. À corriger : en-tête mal aligné et trop chargé, trop de texte, mots importants pas mis en valeur, proportions, **pas assez de preuve sociale sur l'accueil**, logos des partenaires peu visibles (« en couleur, les vrais logos, pas de texte », dont Ville de Genève et Collonge-Bellerive), manque d'images, signaux de confiance et tests A/B (« flags ») pour l'acquisition. Brief complet : `docs/v3/brief-v3.md`.

---

## 5. Ce qui a été fait (équipe d'agents, chef de projet = Claude)

| Phase | Agent | Livrable |
|---|---|---|
| 1 | Audit UX/CRO/a11y/perf/SEO | `docs/v2/audit-maquette.md` (maquette 6,3/10, 43 constats) |
| 1 | Enquête client | `docs/v2/dossier-client.md` |
| 1 | Concurrence Suisse romande | `docs/v2/concurrence-romandie.md` (46 sites, 17 fiches, prix publics) |
| 1 | Personas & psychologie | `docs/v2/personas-psychologie.md` (5 personas, leviers éthiques, 8 tests A/B, 63 sources) |
| 1 | Logos | `site/assets/img/references/` + `logos.json` + `docs/v2/logos-references.md` (lettres types d'autorisation) |
| 1 | Stratégie d'acquisition | `docs/v2/strategie-acquisition.md` (objectifs, scoring, 13 canaux, budget S/M/L, plan d'automatisation, conformité) |
| 2 | Architecte CRO + copywriter | `docs/v2/architecture-cro.md`, `docs/v2/copy-deck.md` (tous les textes, C01-C44 avec repli) |
| 2 | Automatisation | `site/api/`, `automation/`, `docs/v2/contrat-interface.md`, `docs/v2/automatisation.md` |
| 3 | Développement | Générateur `tools/build/` v2, 13 pages, 3 modes |
| 3 | Supports | 3 PDF dans `site/assets/docs/`, `livrables/` (plaquette de validation, Excel de suivi) |
| 4 | Sécurité | `docs/v2/qa/securite.md` (24 constats : 0 critique, 1 élevé et 5 moyens corrigés) |
| 4 | Juridique & relecture | `docs/v2/qa/relecture-juridique-copy.md` (8 points pour l'avocat, check-list) |

| v3 | CRO et preuve sociale | `docs/v3/cro-v3.md` (fil de preuve sociale, ordre du mur de logos, badges, plan de tests A/B à faible trafic) |
| v3 | Images | `site/assets/img/illustrations/` (19 images libres, toujours légendées « Illustration »), recadrages 16:9 / 4:5 du portfolio, vidéo d'ambiance ; crédits dans `docs/v3/credits-images.md` |
| v3 | Logos couleur | 17 logos officiels dans `site/assets/img/references/couleur/`, `logos.json` (`fichier_couleur`, `echelle`) ; `docs/v2/logos-references.md` §9 (à qui écrire) |
| v3 | Direction artistique | `docs/v3/direction-artistique.md` (benchmark, tokens, échelle typographique, mouvement, wireframes, drapeaux A/B, §12 portage sur toutes les pages) |
| v3 | Intégration | accueil puis 12 autres pages au même niveau ; QA axe, Lighthouse, captures Playwright |

| v4 | Audit SEO | `docs/v4/seo/audit-seo.md` (note 6/10 : technique 9, local 3, autorité 2 ; plan d'action, plan de migration J-7 à J+90, carte des mots-clés, 301 testées) ; 7 corrections dans `tools/build/` |
| v4 | Mix d'acquisition | `docs/v4/acquisition/plan-mix-acquisition.md` (portefeuille de canaux, 4 combinaisons chiffrées, séquence M0-M12, règles de décision, attribution) et `simulateur.html` (autonome) |
| v4 | Tableau de bord admin (plans) | `docs/v4/admin/plan-dashboard-admin.md` (architecture A/B/C, 13 écrans, modèle de données, indicateurs, sécurité nLPD, feuille de route) et `maquette/index.html` (cliquable, données fictives) |

Arbitrages du chef de projet : `docs/v2/decisions-chef-de-projet.md` (D1-D8) ; arbitrages v3 dans `docs/v3/direction-artistique.md` §10-12.

### v4 en bref (1er novembre 2026) : faire rapporter des clients

- **SEO** : le code est prêt (9/10, 301 des 17 anciennes URL testées sur Apache). Ce qui manque est hors du code : fiche Google en zone desservie et avis (0 avis partout), NAP incohérent dans au moins 8 annuaires (Chêne-Bourg, mauvaises catégories), LinkedIn à jour, contenu propre des pages services trop court (190-330 mots), prix et lieux de chantiers à confirmer (C31, C25, C22). **Décider C16 avant la mise en ligne** : « cloison isotherme » est associé aux chambres froides, « cloison isolante » au besoin réel.
- **Acquisition** : recommandation **combinaison C** (socle fiche Google + avis + SEO + recommandation, Google Ads CHF 1'000 + Microsoft CHF 100/mois, prospection B2B par courrier et appel, 1 dossier simap tous les 2 mois) ≈ CHF 3'750/mois tout compris ; ≈ 34 demandes et 6 chantiers signés/mois à M12 (fourchettes 15-60 et 3-11). **La contrainte est le temps des associés** (≈ 70 h/mois à 30 demandes) : tri téléphonique avant visite. CPL max corrigé : panier × marge × demande→offre × offre→signée ≈ CHF 430 (v2 surestimait). Annonces Local Services de Google : non confirmées en Suisse, hors budget. Plateformes de mise en relation écartées en année 1 (coût complet par chantier plus élevé).
- **Tableau de bord** : recommandation **A, admin maison** (PHP 8 + MariaDB sur l'hébergement, `gestion.andyconstruct.ch`), Pipedrive abandonné, n8n conservé mais branché sur l'API de l'admin (14 workflows sur 16 à adapter). MVP ≈ 20 jours, V2 ≈ 13, V3 ≈ 8 (estimations). Aujourd'hui l'API n'a **aucune base** : une demande n'existe que dans les e-mails et la file d'attente. Risque relevé : la grille de score classe beaucoup de demandes en A → recalibrer à M3.
- **Indicateurs communs** au simulateur, au plan et au tableau de bord (mêmes noms et formules) : demandes, part A+B, délai de premier contact, demande→offre, offre→signée, CA signé, CPL, CAC, ROAS, ROI, avis, Search Console, fiche Google, citations IA.
Skills utilisés : `pdf`, `xlsx`, `artifact-design` (v2) ; en v3, les skills installés depuis GitHub listés au §2 (`frontend-design`, `webapp-testing`, `cro`, `copywriting`, `marketing-psychology`, `ab-testing`…).

### Design v3 en bref (« le trait de niveau »)

- **Concept** : grille de 12 colonnes, grandes photos, et un seul élément décoratif : un fin trait rouge horizontal, comme le niveau laser du chantier, qui traverse le héro (et sert d'axe à la frise de l'entreprise).
- **Typographie** : Archivo (variable, titres) + Source Sans 3 (texte), auto-hébergées, avec polices de repli calibrées (pas de saut de mise en page, ni en `file://`).
- **Couleurs** : rouge Andy `#E8000F` en ponctuation, anthracite `#1D1F22`, blanc, neutres « brume ».
- **Preuve sociale** : mur de 12 logos couleur juste sous le héro, projets nommés, chiffres animés une fois (19 ans, 18 références, 4 métiers, rappel sous 1 jour ouvrable), bande défilante pausable avant le formulaire, logos à côté du formulaire et en pied de page, badges de confiance pilotés par `confirmations.json`.
- **Mouvement** : séquence d'entrée du héro, compteurs, défilement des logos, en-tête qui se compacte, transitions d'interaction ; tout est coupé avec `prefers-reduced-motion`.
- **Mobile** : titre et boutons avant l'image du héro ; barre d'appel masquée tant que les boutons du héro sont visibles.
- **Drapeaux A/B** (`tools/build/donnees/config.json` → `ab`) : localStorage, `data-flag`, recette par `?flag=nom:variante`, événement Umami `exposition_variante`. Un seul test actif au lancement (A/A témoin), vu le trafic attendu.

---

## 6. Architecture technique

```
Visiteur ─► site statique (tools/build → site/ ou dist/)
              │  formulaire 3 étapes / rappel / guide postal (fetch, repli sans JS)
              ▼
         site/api/demande.php ─► validation, anti-spam, limite de débit, fichiers contrôlés
              │                   score 0-100 + priorité A/B/C (data/scoring.json, zones.json)
              ├─► e-mail interne (toujours) + accusé au prospect (PHPMailer SMTP)
              └─► webhook HMAC-SHA256 ─► n8n (VPS suisse, docker-compose) ─► Pipedrive (ou Brevo)
                                         ├─ SMS/e-mail aux associés, actions en un clic (WF01, WF02)
                                         ├─ relances, avis, offres perdues, entretien (WF03x, WF04x)
                                         ├─ veille simap, rapport mensuel, prospection B2B (WF08-10)
                                         └─ désinscription, purge, supervision (WF12, WF04p, WF13)
Statistiques : Umami sans cookie (suivi.js + data-suivi), activé en production via donnees/config.json
```

**Modes du générateur** (D6) : `preview` (textes définitifs, bandeau de validation, noindex, logos couleur `a_autoriser` visibles) · `verification` (points Cxx soulignés) · `production` (repli pour tout point non confirmé, logos `autorise` seulement — les autres deviennent des noms en typographie soignée —, OMC retirée sans accord donc « 17 références », photos hors offre exclues, indexable, Umami). Les confirmations se cochent dans `tools/build/donnees/confirmations.json`.

**Pages (13)** : index, placo, peinture, isolation-acoustique, cloisons-isothermes, realisations, professionnels, entreprise, contact, merci, mentions-legales, confidentialite, 404 (+ `prestations.html` redirigée). `.htaccess` : 301 Joomla et maquette, compression, cache, CSP stricte.

**Fichiers clés du design v3** : `tools/build/static/styles.css` et `main.js` (source ; minifiés vers `site/assets/`), `tools/build/composants.py` (`MUR`, `DEFILE`, `TEXTE_SEUL`, mur de logos, badges), `tools/build/illustrations.py`, `tools/build/images.py --couvertures` (couvertures des PDF).

**Qualité mesurée (v3)** : axe 0 violation (13 pages, 1440 et 390, 3 modes, menu mobile ouvert) · Lighthouse mobile : accueil 98-99 avec compression serveur (LCP 2,2 s, CLS 0), 96 sans compression pour accueil, placo et réalisations · aucun débordement horizontal de 360 à 1440 px · CSS 74 Ko (15 Ko compressé, budget 80 Ko), JS 28 Ko (10 Ko compressé) · API 266/266, workflows 33/33.

---

## 7. Livrables à remettre

| Fichier | Usage |
|---|---|
| `livrables/andy-construct-v3-validation.zip` | Version de validation (mode preview, logos couleur) à décompresser dans `res/andy-construct-v3/` |
| `livrables/andy-construct-v3-production.zip` | Version production telle qu'elle serait publiée aujourd'hui (rien de confirmé, noms à la place des logos non autorisés) |
| Zips v2 | retirés de `livrables/` ; récupérables au commit `a633851` |
| `livrables/andy-construct-references-preview.pdf` | Plaquette avec logos, pour la séance de validation (ne pas diffuser) |
| `livrables/suivi-demandes-et-kpi.xlsx` | Suivi des demandes tant que le CRM n'est pas en place |
| Dossier de présentation (maquette v1) | https://claude.ai/artifact/44SM63Pk6NFCuvZV77ZdFq — **décrit encore la v1**, à mettre à jour si besoin |

---

## 8. Décisions en attente du client (bloquant production)

1. **44 points C01-C44** : liste consolidée dans `docs/v2/copy-deck.md` §R (délai de rappel, horaires, gratuité visite/devis, petits chantiers, prix, garanties, associé qui rappelle, GGE, assurance, attestations, lieux des chantiers, légendes photos, e-mail sur domaine…). Les cocher dans `confirmations.json`.
2. **Logos** : 17 logos couleur `a_autoriser` → envoyer les lettres de `docs/v2/logos-references.md` (§9 : à qui écrire) ; passer en `autorise` dans `logos.json` à réception. Armoiries de la Ville de Genève et des communes (LPAP) et OMC (Convention de Paris art. 6ter) : accord peu probable, prévoir les noms. OMC : accord même pour le nom. De Grisogono : marque rachetée par un tiers qui n'a pas été client, nom seul recommandé. Confirmer Everness = hôtel de Chavannes-de-Bogis, Dipan SA.
2 bis. **Vidéo du héro** : prête (banque d'images libre) mais désactivée ; le directeur artistique préfère la vraie photo (une vidéo de banque d'images passerait pour un chantier d'Andy Construct). Aperçu : `?flag=hero-media:b`.
3. **Photos** : 19 photos sur 30 (plafonds tendus/métalliques, hors offre) exclues en production ; **aucune photo de peinture** → shooting à commander (architecture-cro §8.8). Originaux en plus haute définition si possible.
4. **Nom du 4e service** (D1), **particuliers hors Genève** (C21, D8), adhésion éventuelle à Gypserie Peinture Genève (GPG).
5. **Témoignages** : 2-3 vrais avec accord écrit (lettre type fournie) ; la section reste masquée sinon.
6. **Budget** : scénario S/M/L (CHF ~5'900 / 18'300 / 42'300 par an) et outils (Pipedrive ou Brevo).
7. **Hébergement d'andyconstruct.ch** : PHP 8.1+ requis pour `site/api/`.

---

## 9. Prochaines étapes

**Immédiat**
- [ ] Passer le dépôt GitHub en privé. Changer le mot de passe FTP (il a circulé dans la conversation).
- [ ] Déployer la version de validation (`python3 deploy/deploy_ftp.py --subdir andy-construct-v3`, ou `livrables/andy-construct-v3-validation.zip` via le gestionnaire de fichiers dans `res/andy-construct-v3/`). Le port FTP 21 était bloqué depuis l'environnement cloud.
- [ ] Séance de validation avec le client (mode `verification` + plaquette preview) ; cocher `confirmations.json`.

**Mise en place des outils** (`docs/v2/automatisation.md`)
- [ ] `site/api/config.php` sur le serveur (SMTP, destinataires, webhook, secret HMAC, `proxys_de_confiance`, `entreprise.horaires`).
- [ ] n8n (VPS Infomaniak + docker-compose, ou n8n cloud UE) ; importer les 16 workflows ; credentials Pipedrive/Brevo/SMS ; relever les clés de champs Pipedrive (`AC_PD_CHAMPS`, dont `opposition_marketing`).
- [ ] **Recette des 20 cas** (§6.2 de la doc) : les workflows n'ont jamais tourné dans une vraie instance.
- [ ] Vérifier sur le compte réel que WF04e et WF04i trouvent bien l'opposition (champ peut-être absent de la liste des affaires).
- [ ] Confirmer les paramètres de l'API simap (WF08). Affiner la table NPA → zone (`site/api/data/zones.json`).
- [ ] Umami (cloud UE ou auto-hébergé) → `tools/build/donnees/config.json`.
- [ ] Non livrés : WF05 (récap du lundi), WF11 (avis Google par API), WF15 (fiche projet).

**v4 — à trancher avec le client** (détails : `docs/v4/acquisition/plan-mix-acquisition.md` §7, `docs/v4/admin/plan-dashboard-admin.md` §7.4, `docs/v4/seo/audit-seo.md` §3.5)
- [ ] Séance de 30 min pour les chiffres 2025 : demandes, offres, signatures, panier par type de client, marge brute, capacité, heures disponibles des associés, montant minimum d'intervention. Les saisir dans le simulateur.
- [ ] Budget mensuel (A ≈ 1'750 / D ≈ 2'500 / B-C ≈ 3'600-3'750), engagement 6 mois ; particuliers hors Genève et La Côte ; marchés publics (taille de lot, qui chiffre) ; qui rappelle et qui visite ; bandeau de consentement ; panneaux de chantier ; adhésion GPG.
- [ ] Architecture du tableau de bord (A recommandée) et abandon de Pipedrive ; hébergeur (pays, PHP 8.1, MariaDB) ; logiciel d'offres utilisé ; import des chantiers signés dans Google Ads.
- [ ] Accès à la fiche Google, LinkedIn et aux annuaires ; Search Console (propriété Domaine, DNS) dès maintenant ; C16, C03, C25, C22, C31, C30, C29.

**Juridique** : faire relire par un avocat les 8 points de `docs/v2/qa/relecture-juridique-copy.md` (demande d'avis, exception « clients » LCD, transferts hors UE, droit des défauts 2026, politique de confidentialité).

**Production** : `python3 tools/build/build.py --mode production --out dist/` → déployer sur andyconstruct.ch ; HSTS à décommenter dans `.htaccess` ; Search Console + Bing Webmaster Tools ; vérifier les 301.

**Acquisition (stratégie §8.1)** : fiche Google (zone desservie) et NAP identique partout (local.ch, search.ch, GGE, Kompass mal classé) ; campagne d'avis ; page Facebook entreprise ; Google Ads (CPC à mesurer semaine 1) ; prospection régies/architectes par courrier + appel (pas d'e-mail à froid, art. 3 LCD) ; veille simap ; bilan à 90 jours ; pages villes/cantons en phase 2 seulement avec de vrais chantiers.

---

## 10. Points d'attention

- Ne jamais éditer `site/*.html` à la main : modifier `tools/build/` puis régénérer.
- La plaquette de validation (`livrables/…-preview.pdf`) ne doit jamais aller dans `site/`.
- Les accusés de réception existent en double (`automation/messages/*.md` et `site/api/modeles/*.txt`) : un test vérifie qu'ils sont identiques.
- Les workflows n8n embarquent une copie des textes : toute correction de message doit être reportée dans les JSON (voir relecture juridique).
- Incident du 31.10 : les agents ont atteint la limite d'usage de 5 h du compte et ont été relancés ; aucun travail perdu.
- Images d'illustration (Unsplash/Pexels) : toujours légendées « Illustration », jamais présentées comme des chantiers d'Andy Construct. Les photos de projets ne sont rattachées à un lieu que si C25 est confirmé.
- Pistes v3 non faites : pages services encore un peu au-dessus de l'objectif de −40 % de texte (−37 à −39 %) ; « VILLE DE GENÈVE » reste petit sur mobile (logo officiel très large) ; aucune photo de peinture réelle (shooting à commander).
