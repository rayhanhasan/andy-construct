# Programme — Version définitive du site Andy Construct (v2)

Chef de projet : Claude (agent principal). Référence maquette : commit `ec5f98d` (maquette v1).
Ce document est la source de vérité commune à tous les agents. Toute production s'y conforme.

## 1. Objectif

Passer de la maquette de présentation à un **site d'acquisition complet, prêt pour la production** :
un site qui génère des demandes qualifiées (appels, formulaires, rappels) de la part de régies, architectes, communes et propriétaires de toute la Suisse romande, avec **toute la stratégie et l'automatisation derrière** (suivi des prospects, réponses automatiques, relances, demandes d'avis, mesure).

## 2. Faits validés par le client (ne pas contredire)

- **Services (4, exclusivement)** : Placo · Peinture · Isolation acoustique · Cloisons isothermes.
- **Zone** : toute la Suisse romande (GE, VD, NE, FR, Valais romand, JU, Jura bernois). Siège à Carouge.
- **Identité** (registre du commerce) : Andy Construct, Chanton & Cie, société en nom collectif, Route des Acacias 48, 1227 Carouge, inscrite depuis 2007, IDE CHE-113.706.162. Tél. +41 22 771 20 15, mobile +41 78 631 14 34.
- **Charte** : `docs/brief-design.md` (rouge #E8000F en ponctuation, anthracite #1D1F22 et blanc en structure, Montserrat + Source Sans 3, sobriété). Le style de la maquette plaît : **on l'améliore, on ne le révolutionne pas**.
- **Audience** : 45-70 ans, BTP. Déteste l'exagéré, le tape-à-l'œil et le jargon marketing.

## 3. Demandes explicites du client pour la v2

1. **Ergonomie** : moins de texte là où c'est trop dense, lecture rapide, parcours plus direct.
2. **Portfolio** plus fort (même style, sans exagération).
3. **Preuve sociale répétée** : logos des clients qui ont fait confiance, partout où c'est pertinent (bandeau près de l'en-tête, pied de page, pages clés).
4. **Copywriting** corrigé et adapté à l'audience (recherche sur Facebook, l'ancien site et toutes les sources disponibles).
5. **CRO / optimisation de la conversion** avec un vrai travail psychologique (persuasion éthique).
6. **Stratégie d'acquisition complète + automatisation** (« absolument tout »).

## 4. Règles non négociables (tous les agents)

- **Aucune invention présentée comme vraie** : pas de faux avis, faux témoignages, fausses notes, faux chiffres, faux labels ou certifications. Une donnée inconnue devient un champ « à fournir par le client » (et le bloc correspondant se masque tant qu'il est vide), jamais un faux contenu en production.
- **Persuasion éthique uniquement** : pas de dark patterns (fausse urgence, faux stock, compte à rebours, cases pré-cochées, pop-up de sortie, culpabilisation). Le public senior y est hostile et c'est contraire à la LCD (loi contre la concurrence déloyale).
- **Logos de clients** : affichage technique prévu partout, mais chaque logo a un statut (`autorise` / `a_autoriser` / `protege`). Les **armoiries publiques** (Ville de Genève, communes) et les **emblèmes d'organisations internationales** (OMC) sont protégés par la loi (LPAP, Convention de Paris art. 6ter) → rendus en **nom typographique**, jamais en logo. Les marques privées demandent l'**accord écrit** du client final avant la mise en production.
- **nLPD / RGPD** : aucune donnée envoyée à un tiers sans le dire ; pas de cookies non essentiels sans consentement ; formulaire avec finalité claire ; durée de conservation documentée.
- **Accessibilité** WCAG 2.1 AA, texte ≥ 16 px (18 px courant), cibles ≥ 48 px, pas d'animation gratuite.
- **Performance** : pas de framework, pas de dépendance externe au chargement ; JS < 25 Ko, CSS < 50 Ko ; LCP < 2,5 s en 4G.
- **Génération** : le HTML est produit par `tools/build/` (Python). Ne jamais éditer `site/*.html` à la main.
- Tout en **français de Suisse romande**, vouvoiement.

## 5. Organisation (agents et livrables)

| Phase | Agent | Livrables | Dossier |
|---|---|---|---|
| 1 | Auditeur UX / CRO / a11y / perf / SEO technique | Audit priorisé de la maquette | `docs/v2/audit-maquette.md` |
| 1 | Enquêteur client | Dossier client (Facebook, ancien site, annuaires, presse) + ton de voix | `docs/v2/dossier-client.md` |
| 1 | Analyste concurrence Suisse romande | Concurrence, SERP, offres, avis, publicités, messages | `docs/v2/concurrence-romandie.md` |
| 1 | Psychologie & personas | Personas, parcours de décision, objections, leviers éthiques | `docs/v2/personas-psychologie.md` |
| 1 | Logos & preuve sociale | Logos sourcés, statut juridique, versions monochromes, `logos.json` | `site/assets/img/references/`, `docs/v2/logos-references.md` |
| 1 | Stratège acquisition | Stratégie multicanale, budget, KPI, calendrier, plan d'automatisation | `docs/v2/strategie-acquisition.md` |
| 2 | Copywriter + architecte CRO | Arborescence v2, deck de textes de toutes les pages, spécifications de conversion | `docs/v2/copy-deck.md`, `docs/v2/architecture-cro.md` |
| 2 | Ingénieur automatisation | Endpoint PHP, anti-spam, e-mails auto, webhooks, workflows n8n, plan de tracking, CRM | `site/api/`, `automation/`, `docs/v2/automatisation.md` |
| 3 | Développeur frontend | Site v2 généré depuis `tools/build/` | `site/`, `tools/build/` |
| 3 | Supports commerciaux | Plaquette PDF de références, fichier de suivi prospects / KPI | `livrables/` |
| 4 | QA (accessibilité, perf, SEO, sécurité, relecture) | Rapports + corrections | `docs/v2/qa/` |

## 6. Mode preview / production

Le générateur doit produire deux variantes :
- **preview** (défaut) : `noindex`, bandeau « version de validation », logos `a_autoriser` affichés, blocs vides masqués ;
- **production** (`python3 tools/build/build.py --production`) : indexable, sans bandeau, uniquement les logos `autorise`, formulaire branché sur l'endpoint réel.
