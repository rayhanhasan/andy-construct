# HANDOFF — Andy Construct, site d'acquisition (v2)

Document de passation pour reprendre le projet en local (Claude Code ou à la main).
Mise à jour : 31 octobre 2026. État : **v2 développée, testée et contrôlée ; en attente de validation client et de mise en place des outils (SMTP, n8n, CRM)**.

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

> Lis HANDOFF.md, README.md, docs/v2/programme-v2.md et docs/v2/decisions-chef-de-projet.md. Tu es chef de projet du site d'acquisition Andy Construct (v2). Reprends à la section « Prochaines étapes ».

Prérequis : Python 3.10+ (générateur sans dépendance ; Pillow seulement pour `tools/build/images.py` et les scripts de `livrables/sources/`), PHP 8.1+ pour l'API, Node 18+ et Playwright pour les captures, Docker pour n8n auto-hébergé.

---

## 2. Dépôt

| Élément | Valeur |
|---|---|
| Dépôt | `rayhanhasan/andy-construct` — **⚠️ PUBLIC et indexé : à passer en privé** (Settings → Danger Zone → Change visibility) |
| Branche | `claude/eager-heisenberg-sz3nve` (tout est poussé) ; pas de pull request |
| Maquette v1 | commit `ec5f98d` (le tag `maquette-v1` n'a pas pu être poussé par le proxy) |
| Secrets | aucun dans le dépôt ; `site/api/config.php`, `site/api/stockage/`, `automation/.env`, `automation/donnees/` sont ignorés par git |

---

## 3. Le client (faits vérifiés)

- **Andy Construct, Chanton & Cie**, société en nom collectif, Route des Acacias 48, 1227 Carouge GE (siège depuis 05.2023 ; adresse de domiciliation partagée par ~92 entreprises → fiche Google en « zone desservie »). IDE CHE-113.706.162. Activité depuis le **01.06.2007** (Perly-Certoux → Chêne-Bourg 2010 → Carouge 2023). Associés : Adnan Bajrami, Caroline Chanton Bajrami.
- Tél. +41 22 771 20 15 · mobile +41 78 631 14 34 · andy.construct@bluewin.ch (recommandé : contact@andyconstruct.ch).
- **Services (validés par le client)** : Placo · Peinture · Isolation acoustique · Cloisons isothermes (affichées « Cloisons isolantes », D1).
- **Zone (validée)** : toute la Suisse romande. **Audience** : 45-70 ans, BTP, allergique à l'exagéré.
- 18 références publiques (Ville de Genève, Conservatoire, HEAD, OMC, UBS, Piaget, salles communales…). Membre du GGE selon l'annuaire (à confirmer). Aucun avis client public nulle part. Facebook = profil personnel fermé (pas de page entreprise).
- Détail : `docs/v2/dossier-client.md`.

---

## 4. Demande du client pour la v2 (résumé)

Version définitive, **site d'acquisition** : tous les agents et skills utiles, audits, analyse concurrentielle, copywriting corrigé et adapté à l'audience, CRO avec travail psychologique, ergonomie (moins de texte, meilleur portfolio, même style sobre), **logos des références répétés** (sous l'en-tête, pied de page…), **stratégie d'acquisition et automatisation complètes**.

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

Arbitrages du chef de projet : `docs/v2/decisions-chef-de-projet.md` (D1-D8).
Skills utilisés : `pdf`, `xlsx`, `artifact-design`. Aucun skill SEO/CRO/copywriting n'existe sur le compte : les méthodes (Nielsen, LIFT, Cialdini, WCAG, Baymard) sont intégrées dans les consignes des agents.

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

**Modes du générateur** (D6) : `preview` (textes définitifs, bandeau de validation, noindex) · `verification` (points Cxx soulignés) · `production` (repli pour tout point non confirmé, logos `autorise` seulement, photos hors offre exclues, indexable, Umami). Les confirmations se cochent dans `tools/build/donnees/confirmations.json`.

**Pages (13)** : index, placo, peinture, isolation-acoustique, cloisons-isothermes, realisations, professionnels, entreprise, contact, merci, mentions-legales, confidentialite, 404 (+ `prestations.html` redirigée). `.htaccess` : 301 Joomla et maquette, compression, cache, CSP stricte.

**Qualité mesurée** : axe 0 violation (13 pages, 1440 et 390) · Lighthouse mobile production : accueil 99/100/100/100 (LCP 1,8 s), placo 100/100/100/100 · CSS 47 Ko, JS 24 Ko · API 266/266, HTTP 57/57, workflows 39/39.

---

## 7. Livrables à remettre

| Fichier | Usage |
|---|---|
| `andy-construct-v2-validation.zip` (envoyé dans la conversation) | Version de validation à déposer dans `res/andy-construct-v2/` |
| `andy-construct-v2-production.zip` (envoyé dans la conversation) | Version production telle qu'elle serait publiée aujourd'hui (rien de confirmé) |
| `livrables/andy-construct-references-preview.pdf` | Plaquette avec logos, pour la séance de validation (ne pas diffuser) |
| `livrables/suivi-demandes-et-kpi.xlsx` | Suivi des demandes tant que le CRM n'est pas en place |
| Dossier de présentation (maquette v1) | https://claude.ai/artifact/44SM63Pk6NFCuvZV77ZdFq — **décrit encore la v1**, à mettre à jour si besoin |

---

## 8. Décisions en attente du client (bloquant production)

1. **44 points C01-C44** : liste consolidée dans `docs/v2/copy-deck.md` §R (délai de rappel, horaires, gratuité visite/devis, petits chantiers, prix, garanties, associé qui rappelle, GGE, assurance, attestations, lieux des chantiers, légendes photos, e-mail sur domaine…). Les cocher dans `confirmations.json`.
2. **Logos** : 12 logos `a_autoriser` → envoyer les lettres de `docs/v2/logos-references.md` ; passer en `autorise` dans `logos.json` à réception. OMC : accord même pour le nom. Confirmer Everness = hôtel de Chavannes-de-Bogis, Dipan SA, de Grisogono.
3. **Photos** : 19 photos sur 30 (plafonds tendus/métalliques, hors offre) exclues en production ; **aucune photo de peinture** → shooting à commander (architecture-cro §8.8). Originaux en plus haute définition si possible.
4. **Nom du 4e service** (D1), **particuliers hors Genève** (C21, D8), adhésion éventuelle à Gypserie Peinture Genève (GPG).
5. **Témoignages** : 2-3 vrais avec accord écrit (lettre type fournie) ; la section reste masquée sinon.
6. **Budget** : scénario S/M/L (CHF ~5'900 / 18'300 / 42'300 par an) et outils (Pipedrive ou Brevo).
7. **Hébergement d'andyconstruct.ch** : PHP 8.1+ requis pour `site/api/`.

---

## 9. Prochaines étapes

**Immédiat**
- [ ] Passer le dépôt GitHub en privé. Changer le mot de passe FTP (il a circulé dans la conversation).
- [ ] Déployer la version de validation (`python3 deploy/deploy_ftp.py --subdir andy-construct-v2`, ou le zip via le gestionnaire de fichiers). Le FTP était bloqué depuis l'environnement cloud.
- [ ] Séance de validation avec le client (mode `verification` + plaquette preview) ; cocher `confirmations.json`.

**Mise en place des outils** (`docs/v2/automatisation.md`)
- [ ] `site/api/config.php` sur le serveur (SMTP, destinataires, webhook, secret HMAC, `proxys_de_confiance`, `entreprise.horaires`).
- [ ] n8n (VPS Infomaniak + docker-compose, ou n8n cloud UE) ; importer les 16 workflows ; credentials Pipedrive/Brevo/SMS ; relever les clés de champs Pipedrive (`AC_PD_CHAMPS`, dont `opposition_marketing`).
- [ ] **Recette des 20 cas** (§6.2 de la doc) : les workflows n'ont jamais tourné dans une vraie instance.
- [ ] Vérifier sur le compte réel que WF04e et WF04i trouvent bien l'opposition (champ peut-être absent de la liste des affaires).
- [ ] Confirmer les paramètres de l'API simap (WF08). Affiner la table NPA → zone (`site/api/data/zones.json`).
- [ ] Umami (cloud UE ou auto-hébergé) → `tools/build/donnees/config.json`.
- [ ] Non livrés : WF05 (récap du lundi), WF11 (avis Google par API), WF15 (fiche projet).

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
