# Contrat d'interface : formulaires, endpoint PHP et suivi

*Ingénieur automatisation · 31 octobre 2026 · destinataire : développeur frontend (`tools/build/` → `site/`)*

Ce document **fait foi** pour les noms de champs, les valeurs envoyées, les réponses du serveur et les attributs de suivi. Les **libellés affichés** viennent de `architecture-cro.md` §6-7 et de `copy-deck.md` (§A.5, §A.7, §K, §Q.4). Décisions intégrées : `decisions-chef-de-projet.md` D1, D2, D3, D7.

Code de référence : `site/api/lib/Champs.php` (listes), `site/api/lib/Validateur.php` (règles et messages), `site/api/lib/Traitement.php` (réponses). Tests : `php site/api/tests/run.php`, `bash site/api/tests/endpoint.sh`.

---

## 1. Résumé pour le développeur

| Sujet | Règle |
|---|---|
| URL | `POST /api/demande.php` (même domaine que le site, chemin relatif conseillé : `/api/demande.php`) |
| Encodage | `multipart/form-data` (obligatoire dès qu'il peut y avoir des fichiers ; accepté pour tous les formulaires) |
| Avec JavaScript | `fetch` avec l'en-tête `Accept: application/json` → réponse JSON `{ok, message, ref}` |
| Sans JavaScript | `<form method="post" action="/api/demande.php" enctype="multipart/form-data">` → redirection 303 vers la page de remerciement, ou page HTML d'erreur |
| Trois formulaires | `formulaire=devis` (3 étapes), `formulaire=rappel` (module de rappel), `formulaire=envoi_postal_guide` (guide imprimé par la poste) |
| Consentement | **Aucune case** (D2). Mention d'information sous le bouton. Un champ `accord` éventuel est ignoré. |
| Anti-spam | Champ piège `site_web` (vide) + jeton horodaté `form_t0` (obtenu par `GET /api/demande.php?jeton`). Pas de CAPTCHA. |
| Suivi | `/assets/js/suivi.js` (2,9 Ko, sans cookie) + attributs `data-suivi` ; Umami si présent |
| Robots | `robots.txt` : `Disallow: /api/` |

---

## 2. Point d'entrée

| Méthode et URL | Rôle | Réponse |
|---|---|---|
| `GET /api/demande.php?jeton` | Délivre le jeton horodaté du piège temporel | `200 {"ok":true,"jeton":"v1.1793440635.1b7fa1fc08e3.97f4…"}`, `Cache-Control: no-store` |
| `POST /api/demande.php` | Reçoit une demande | §8 |
| autre | — | `405 {"ok":false,"code":"methode",…}` |

**Quand demander le jeton** : au premier `focusin` dans le formulaire (une seule fois par page), puis le placer dans le champ caché `form_t0`. Délai minimal entre la délivrance du jeton et l'envoi : **4 s** (devis), **2 s** (rappel), **3 s** (guide). Le jeton est valable 12 h ; au-delà, l'envoi est accepté mais signalé. Si l'appel échoue (réseau), envoyer le formulaire **sans** jeton : il est accepté.

---

## 3. Champs cachés communs aux trois formulaires

| Nom | Rempli par | Valeur | Remarque |
|---|---|---|---|
| `formulaire` | HTML | `devis` · `rappel` · `envoi_postal_guide` | Obligatoire. L'ancien `aimant` est converti en `envoi_postal_guide`. |
| `site_web` | — | **vide** | Piège à robots. Voir le balisage §11. Rempli → réponse « succès » factice, rien n'est traité. |
| `form_t0` | script du formulaire | jeton de §2 | Facultatif (envoi sans JS). |
| `source` | HTML | emplacement du formulaire, en minuscules et tirets : `accueil`, `page-placo`, `page-peinture`, `page-isolation-acoustique`, `page-cloisons-isothermes`, `professionnels`, `contact`, `realisations`, `rappel-colonne` | Facultatif, sert à l'analyse. |
| `page` | `suivi.js` | chemin de la page (`/contact.html`) | Créé et rempli automatiquement. |
| `page_entree` | `suivi.js` | 1re page vue dans l'onglet | Idem. |
| `referent` | `suivi.js` | nom d'hôte du site d'origine (`www.google.ch`), jamais l'URL complète | Idem. |
| `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term` | `suivi.js` | valeurs UTM de l'arrivée (100 caractères au plus) | Idem. Rien si Do Not Track. |
| `gclid` | `suivi.js` | identifiant de clic Google Ads | **Seulement** si `consent_ads=accorde` (le serveur l'ignore sinon). |
| `consent_ads` | bandeau de consentement (scénarios M et L) | `accorde` · `refuse` · vide | Absent tant qu'il n'y a pas de bandeau. |
| `canal` | HTML | `site` | `telephone` est réservé à la saisie interne (exige `cle_interne`). |

`suivi.js` crée les champs manquants dans tout formulaire portant `data-suivi-formulaire` ou dont l'`action` contient `api/demande.php`. Il n'écrase jamais une valeur déjà présente.

---

## 4. Formulaire de devis (`formulaire=devis`)

Trois étapes (`architecture-cro.md` §6) ; **sans JavaScript, les trois `fieldset` s'affichent l'un sous l'autre** et un seul bouton envoie tout.

### Étape 1 · Quels travaux ?

| Nom | Type | Valeurs envoyées → libellés (cartes) | Serveur |
|---|---|---|---|
| `travaux[]` | cases à cocher (plusieurs possibles) | `placo` → « Placo » · `peinture` → « Peinture » · `isolation-acoustique` → « Isolation acoustique » · `cloisons-isothermes` → « Cloisons isolantes » (D1) · `ne-sait-pas` → « Autre chose, ou je ne sais pas encore » | **Obligatoire** (au moins une). 2 prestations ou plus = « plusieurs » pour le score. `autre` (hors des 4 métiers) est aussi accepté. Un `travaux` simple (sans `[]`) est accepté. |

Préremplissage depuis une page service ou `?travaux=placo` : cocher la carte, afficher « Travaux : Placo · Modifier », ouvrir l'étape 2.

### Étape 2 · Votre projet

| Nom | Type | Valeurs → libellés | Serveur |
|---|---|---|---|
| `type_client` | radio | `proprietaire` → « Propriétaire (maison, appartement, PPE) » · `locataire` → « Locataire » · `regie` → « Régie, gérance ou coopérative » · `architecte` → « Architecte, bureau d'études ou entreprise générale » · `commune` → « Commune ou institution » · `entreprise` → « Entreprise, bureau ou commerce » | Facultatif côté serveur (score « non précisé »). L'interface peut l'exiger (architecture-cro). |
| `commune` | texte, `autocomplete="address-level2"`, 80 caractères | saisie libre (« Lancy », « 1212 Grand-Lancy ») | **Obligatoire** si `npa` est vide. Le NPA est extrait s'il est écrit dans le champ. |
| `npa` | texte, `inputmode="numeric"`, facultatif | 4 chiffres | Rempli par le script si la saisie commence par 4 chiffres ; contrôlé (`^[1-9][0-9]{3}$`). |
| `delai` | radio | `moins-1-mois` → « Dès que possible (moins d'un mois) » · `1-3-mois` → « Dans 1 à 3 mois » · `3-6-mois` → « Dans 3 à 6 mois » · `non-defini` → « Pas encore défini » | Facultatif |
| `surface` | radio | `moins-15` → « Moins de 15 m² (une réparation) » · `15-50` → « 15 à 50 m² (une ou deux pièces) » · `50-200` → « 50 à 200 m² (un appartement, un étage) » · `plus-200` → « Plus de 200 m², ou plusieurs logements » · `ne-sait-pas` → « Je ne sais pas » | Facultatif |

Aucun bouton radio présélectionné. Une valeur inconnue est **ignorée** (sans erreur) et journalisée.

### Étape 3 · Vos coordonnées

| Nom | Type | Valeurs → libellés | Serveur |
|---|---|---|---|
| `civilite` | radio | `madame` → « Madame » · `monsieur` → « Monsieur » | Facultatif (sert à « Bonjour Madame Dupont » dans les e-mails) |
| `nom` | texte, `autocomplete="name"`, 100 car. | « Nom et prénom » | **Obligatoire** |
| `telephone` | `type="tel"`, `inputmode="tel"`, `autocomplete="tel"` | tous formats : `022 771 20 15`, `079/123.45.67`, `+41 79 123 45 67`, `0041…`, `+41 (0)79…`, numéros étrangers `+33…` | **Téléphone ou e-mail obligatoire**. Normalisé en +41… (E.164). |
| `email` | `type="email"`, `autocomplete="email"` | | Voir ci-dessus. Contrôle strict (pas d'espace, domaine valide, IDN converti). |
| `preference_contact` | radio | `appel` → « Par téléphone » · `email` → « Par e-mail » · `indifferent` → « Peu importe » | Facultatif. `appel` sans téléphone → erreur sur `telephone`. |
| `creneau` | radio (affiché si `appel`) | `matin` → « Le matin » · `apres-midi` → « L'après-midi » · `indifferent` → « Peu importe » | Facultatif |
| `message` | zone de texte | | Facultatif, **3'000 caractères** au plus |
| `fichiers[]` | `type="file" multiple` | voir §7 | Facultatif |
| `connu_par` | liste | `recherche-google` → « Recherche sur Google » · `carte-google` → « Carte Google » · `recommandation` → « Recommandation d'un proche ou d'un voisin » · `regie-architecte` → « Une régie ou un architecte » · `panneau-vehicule` → « Un panneau de chantier ou un véhicule » · `facebook` → « Facebook » · `linkedin` → « LinkedIn » · `autre` → « Autre » | Facultatif |
| `recommande_par` | texte, 100 car. (affiché si `recommandation`) | | Facultatif |

Sous le bouton « Envoyer ma demande » : la mention d'information du copy deck §A.5 (« En envoyant ce formulaire, vous nous transmettez vos coordonnées pour traiter votre demande. Elles ne servent à rien d'autre. » + lien « Protection des données » vers `/confidentialite.html`). **Pas de case à cocher.**

---

## 5. Module de rappel (`formulaire=rappel`)

| Nom | Type | Serveur |
|---|---|---|
| `telephone` | `type="tel"` | **Obligatoire** (message : « Indiquez le numéro auquel nous pouvons vous rappeler. ») |
| `nom` | texte | Facultatif |
| `creneau` | radio `matin` · `apres-midi` · `indifferent` | Facultatif |
| `travaux[]` | caché, si le module est sur une page service (`placo`…) | Facultatif, améliore le score |

Plus les champs cachés du §3. Une demande de rappel n'est **jamais** classée en dessous de la priorité B.

---

## 6. Guide imprimé par la poste (`formulaire=envoi_postal_guide`)

Les PDF se téléchargent **librement** (D3, D7) ; ce petit formulaire ne sert qu'à recevoir la version imprimée (copy deck §Q.4).

| Nom | Type | Valeurs | Serveur |
|---|---|---|---|
| `guide` | caché | `guide-reduire-le-bruit` · `checklist-chantier-site-occupe` · `andy-construct-references` (mêmes noms que les PDF de `site/assets/docs/`) | **Obligatoire**, doit être actif dans la configuration |
| `civilite` | radio, facultatif | `madame` · `monsieur` | Facultatif |
| `nom` | texte | « Votre nom » | **Obligatoire** |
| `adresse` | texte, `autocomplete="street-address"` | « Rue et numéro » | **Obligatoire** |
| `npa` | texte, `inputmode="numeric"`, `autocomplete="postal-code"` | 4 chiffres | **Obligatoire** |
| `localite` | texte, `autocomplete="address-level2"` | « Localité » | **Obligatoire** |
| `profil` | radio, facultatif | `proprietaire` · `locataire` · `regie` · `architecte` · `commune` · `entreprise` · `autre` | Facultatif |
| `email` | `type="email"`, facultatif | « Votre e-mail (facultatif), pour une confirmation » | Facultatif ; si donné : accusé de réception |
| `conseils_email` | case **non cochée**, affichée seulement si un e-mail est saisi | `oui` → « Recevoir aussi deux conseils par e-mail sur ce sujet (puis plus rien ; désinscription en un clic) » | Facultatif. **Seule** condition de la séquence de 2 e-mails (opt-in explicite). |

Succès : message sur la page, sans redirection (« Merci. Le guide part par la poste dans les prochains jours. »). Compatibilité : l'ancien format du copy deck (`formulaire=aimant`, `aimant=…`, `adresse_postale` sur 3 lignes) reste accepté.

---

## 7. Fichiers (devis uniquement)

| Règle | Valeur |
|---|---|
| Nom du champ | `fichiers[]` (`fichier` et `fichier[]` sont aussi acceptés) |
| Nombre | **3 au maximum** |
| Taille | **8 Mo par fichier** (24 Mo au total ; le serveur accepte 26 Mo par envoi). *Remplace « 10 Mo au total » d'`architecture-cro.md` §6.2.* |
| Types | JPG, PNG, HEIC (photos d'iPhone), PDF. Vérifiés par le contenu réel (finfo), pas par l'extension. |
| `accept` conseillé | `image/jpeg,image/png,image/heic,image/heif,.heic,application/pdf` |
| Refus | Fichier piégé (code caché, PDF avec JavaScript, exécutable renommé) → erreur sur `fichiers`, **aucun** fichier du lot n'est gardé |
| Côté client | Vérifier nombre et poids avant l'envoi ; afficher nom et poids ; bouton « Retirer » par fichier |
| Aide affichée | « JPG, PNG, HEIC ou PDF, 3 fichiers de 8 Mo au plus. Trop lourd ? Envoyez-les par e-mail après notre appel. » |

---

## 8. Réponses du serveur (avec `Accept: application/json`)

Corps toujours de la forme :

```json
{ "ok": true, "message": "Merci, votre demande est bien arrivée. Caroline vous appelle aujourd'hui avant 16 h 30. Un e-mail de confirmation vient de vous être envoyé.", "ref": "AC-2026-0042" }
```

```json
{ "ok": false, "code": "validation", "message": "Il manque une information, ou l'une d'elles est à vérifier. Les champs concernés sont indiqués.", "ref": null,
  "erreurs": { "telephone": "Indiquez un numéro de téléphone ou une adresse e-mail pour que nous puissions vous répondre.", "commune": "Indiquez la commune des travaux ou son NPA." } }
```

| HTTP | `code` | Cas | Affichage conseillé |
|---|---|---|---|
| 200 | — | Succès (`ok: true`, `ref` = « AC-AAAA-NNNN ») | Devis et rappel : enregistrer `ref`, `message` et le récapitulatif dans `sessionStorage`, effacer le brouillon, aller à `/merci.html`. Guide : message sur place. |
| 200 | — | Robot détecté (`ok: true`, **`ref: null`**) | Même affichage qu'un succès (ne rien révéler) |
| 413 | `trop_volumineux` | Envoi au-delà de 26 Mo | `message` au-dessus du champ fichiers |
| 403 | `origine` | Envoi depuis un autre site | `message` + téléphone |
| 405 | `methode` | Méthode autre que POST/GET | — |
| 422 | `validation` | Champ manquant ou mal formé | `erreurs[champ]` sous chaque champ ; revenir à l'étape du 1er champ en erreur ; récapitulatif en haut de l'étape |
| 422 | `trop_rapide` | Envoi moins de 2-4 s après l'affichage du jeton | `message` près du bouton ; laisser la saisie ; un second clic passe |
| 429 | `trop_de_demandes` | Plus de 5 demandes (ou 30 envois) par heure depuis la même connexion. En-tête `Retry-After`. | `message` + téléphone |
| 500 | `technique` | Panne | `message` (« Vos informations ne sont pas perdues… ») + bouton « Réessayer » + téléphone ; **ne jamais vider le formulaire** |

**Clés possibles de `erreurs`** et messages exacts (affichables tels quels) :

| Clé | Message |
|---|---|
| `nom` | « Indiquez votre nom et votre prénom. » (guide : « Indiquez votre nom pour l'envoi par la poste. ») |
| `telephone` | « Indiquez un numéro de téléphone ou une adresse e-mail pour que nous puissions vous répondre. » · « Ce numéro semble incomplet. Indiquez-le par exemple ainsi : 079 123 45 67. » · « Indiquez le numéro auquel nous pouvons vous rappeler. » |
| `email` | « Cette adresse e-mail semble incomplète. Vérifiez-la, par exemple : nom@exemple.ch. » |
| `travaux` | « Choisissez au moins un type de travaux, ou « Autre chose, ou je ne sais pas encore ». » |
| `commune` | « Indiquez la commune des travaux ou son NPA. » |
| `npa` | « Le NPA compte 4 chiffres, par exemple 1227. » · (guide) « Indiquez le NPA, par exemple 1227. » |
| `message` | « Votre message est trop long (3'000 caractères au maximum). Vous pouvez nous envoyer la suite par e-mail. » |
| `fichiers` | « Vous pouvez joindre 3 fichiers au maximum… » · « Le fichier « x » dépasse 8 Mo… » · « Le fichier « x » n'est pas accepté : formats JPG, PNG, HEIC ou PDF uniquement. » · « Le fichier « x » n'a pas pu être accepté. Envoyez-le par e-mail à contact@andyconstruct.ch, nous le regarderons. » |
| `adresse`, `localite`, `guide` | « Indiquez l'adresse à laquelle envoyer le guide (rue et numéro). » · « Indiquez la localité, par exemple Carouge. » · « Ce guide n'est pas disponible pour le moment… » |
| `prenom`, `recommande_par`, `formulaire` | rares (texte trop long, formulaire inconnu) |

Échec réseau (aucune réponse) : message du copy deck (« Votre demande n'a pas pu partir. Rien n'est perdu : réessayez dans un instant, ou appelez-nous au +41 22 771 20 15. »).

### Exemple d'envoi

```js
const reponse = await fetch(form.action, {
  method: 'POST',
  body: new FormData(form),            // multipart/form-data, fichiers compris
  headers: { 'Accept': 'application/json' },
  credentials: 'same-origin'
});
const r = await reponse.json().catch(() => ({ ok: false, code: 'technique' }));
if (r.ok) { /* sessionStorage + merci.html */ } else { /* r.erreurs, r.message */ }
```

---

## 9. Sans JavaScript

| Situation | Réponse |
|---|---|
| Succès, devis ou rappel | `303` vers `/merci.html` (page générique, sans récapitulatif) |
| Succès, guide | `303` vers `/merci.html` (configurable : `pages.merci_envoi_postal_guide`) |
| Erreur | Page HTML sobre servie par le PHP (statut 422, 429…) : titre « Votre demande n'est pas encore partie », liste des messages, bouton « Revenir au formulaire » (vers la page d'origine), bouton « Appeler le +41 22 771 20 15 », rappel que le bouton « Retour » du navigateur conserve la saisie. |

Pages attendues du frontend : `/merci.html` (noindex, copy deck §K) et `/confidentialite.html` (texte : `docs/v2/automatisation.md` §9).

---

## 10. Saisie interne (pour mémoire)

`canal=telephone` + `cle_interne=<clé de config.php>` : saisie express d'un appel reçu, sans piège temporel ni limite de débit ; `envoyer_confirmation=oui` déclenche l'accusé de réception. Page non publique, hors du périmètre du site v2.

---

## 11. Balisage conseillé

```html
<form id="form-devis" method="post" action="/api/demande.php" enctype="multipart/form-data"
      data-suivi-formulaire="devis" novalidate>
  <input type="hidden" name="formulaire" value="devis">
  <input type="hidden" name="source" value="page-placo">
  <input type="hidden" name="form_t0" value="">
  <!-- Piège à robots : hors écran, ignoré des lecteurs d'écran et du clavier. Pas de display:none. -->
  <div class="champ-piege" aria-hidden="true">
    <label for="site_web">Ne pas remplir ce champ</label>
    <input type="text" id="site_web" name="site_web" tabindex="-1" autocomplete="off" value="">
  </div>
  …
</form>
```

CSS du piège : `.champ-piege{position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden}`.

Un `id` unique par formulaire quand plusieurs formulaires sont sur la même page (devis + rappel).

---

## 12. Suivi (Umami, sans cookie)

### 12.1 Chargement

```html
<!-- dans <head>, suivi.js AVANT Umami (les deux en defer s'exécutent dans l'ordre) -->
<script defer src="/assets/js/suivi.js"></script>
<script defer src="https://stats.andyconstruct.ch/script.js"
        data-website-id="00000000-0000-0000-0000-000000000000"
        data-domains="www.andyconstruct.ch"
        data-do-not-track="true"
        data-before-send="acUmamiAvantEnvoi"></script>
```

- **Recommandé** : Umami auto-hébergé sur le VPS suisse de n8n (`stats.andyconstruct.ch`, voir `automatisation.md` §4.6). **Option** : Umami Cloud (région d'hébergement à vérifier avant usage, puis à mentionner dans la politique de confidentialité).
- `data-domains` : aucune mesure en préproduction. En mode preview, le générateur **n'inclut pas** le script Umami.
- `data-before-send="acUmamiAvantEnvoi"` (Umami ≥ 2.15) : retire `gclid`, `fbclid`, `msclkid` des URL envoyées et annule toute mesure si Do Not Track est actif. Sans cette version, ignorer l'attribut : `data-do-not-track` suffit.
- Si une politique CSP est posée : `script-src` et `connect-src` doivent autoriser le domaine d'Umami.
- Sans Umami, `suivi.js` ne fait rien (aucune erreur) ; il garde quand même les UTM pour le formulaire.

### 12.2 Ce que fait `suivi.js`

| Fonction | Détail |
|---|---|
| Do Not Track / GPC | Si `navigator.doNotTrack == "1"` ou `globalPrivacyControl` : aucun événement, rien en `sessionStorage` (seul `page` est rempli dans le formulaire) |
| UTM | Lus à l'arrivée, gardés dans `sessionStorage` (`ac_src`, effacé à la fermeture de l'onglet), remplacés par une nouvelle campagne ; copiés dans les champs cachés (§3) |
| `gclid` | Gardé seulement si `window.acConsentAds === true` ou `<html data-consent-ads="accorde">` au chargement |
| Clics | Délégation sur `document` : `[data-suivi]`, sinon détection automatique des liens `tel:` (`appel_clic`), `mailto:` (`email_clic`), `wa.me` (`whatsapp_clic`), cartes Google (`itineraire_clic`) |
| Propriétés | Tous les attributs `data-suivi-*` (sauf `data-suivi-zone`) deviennent des propriétés : `data-suivi-emplacement="entete"` → `{emplacement: "entete"}` (tirets → soulignés). Si `emplacement` manque, il est pris sur l'ancêtre `[data-suivi-zone]`. |
| `formulaire_debut` | Automatique : premier champ touché d'un `form[data-suivi-formulaire]`, une fois par onglet et par formulaire |
| API | `window.acSuivi(nom, propriétés)` pour les événements de formulaire. Les propriétés `nom`, `prenom`, `email`, `telephone`, `message`, `adresse`, `commune` sont **supprimées** d'office ; valeurs coupées à 60 caractères. |

### 12.3 Événements et attributs

| Événement | Déclencheur | Mise en œuvre | Propriétés |
|---|---|---|---|
| `appel_clic` | lien `tel:` | automatique (ou `data-suivi="appel_clic"`) | `numero` (`fixe` · `mobile`) via `data-suivi-numero`, `emplacement` (`entete` · `heros` · `barre_mobile` · `bloc_demande` · `contact` · `pied` · `fiche_projet` · `merci` · `404`) |
| `email_clic` | lien `mailto:` | automatique | `emplacement` |
| `whatsapp_clic` | lien `wa.me` (si le bouton est validé) | automatique | `emplacement` |
| `itineraire_clic` | « Voir sur la carte » | automatique (lien Google Maps) ou `data-suivi="itineraire_clic"` | `emplacement` |
| `devis_clic` | boutons « Demander un devis », « Un projet semblable ? » | `data-suivi="devis_clic"` | `emplacement`, `service` (`data-suivi-service="placo"`) |
| `telechargement` | liens des PDF (D7) | `data-suivi="telechargement" data-suivi-doc="guide-reduire-le-bruit"` | `doc` : `andy-construct-references` · `guide-reduire-le-bruit` · `checklist-chantier-site-occupe` · `modele-avis-aux-locataires` ; `emplacement`. *Remplace `plaquette_telechargee` et `guide_telecharge`.* |
| `galerie_filtre` | filtres des réalisations | `data-suivi="galerie_filtre" data-suivi-filtre="placo"` | `filtre` |
| `rappel_ouvert` | lien « Vous préférez qu'on vous rappelle ? » | `data-suivi="rappel_ouvert"` | `etape` |
| `formulaire_debut` | 1er champ touché | automatique (`data-suivi-formulaire="devis"` · `rappel` · `envoi_postal_guide` sur le `<form>`) | `formulaire` |
| `formulaire_etape` | passage à l'étape 2 ou 3 | `acSuivi('formulaire_etape', {etape: '2', service: 'placo', type_client: 'regie'})` | `etape`, `service`, `type_client` |
| `formulaire_erreur` | erreur affichée (client ou serveur) | `acSuivi('formulaire_erreur', {formulaire: 'devis', champ: 'telephone'})` | `champ` (**jamais la valeur**) |
| `formulaire_envoye` | réponse `ok: true` **et** `ref` non nul | `acSuivi('formulaire_envoye', {formulaire: 'devis', service: 'placo', type_client: 'regie'})` | `formulaire`, `service`, `type_client` (pas la priorité) |
| `guide_poste_demande` | réponse `ok` du formulaire guide | `acSuivi('guide_poste_demande', {doc: 'guide-reduire-le-bruit'})` | `doc` |
| `recommandation_carte` | arrivée avec `utm_source=recommandation` | automatique | — |

Ne **jamais** envoyer de donnée saisie (nom, e-mail, téléphone, commune, message) dans une propriété. `formulaire_envoye` ne part pas depuis `merci.html` (pas de doublon).

---

## 13. Ce que le serveur fait ensuite (pour information)

1. E-mail interne aux associés (toujours, même si n8n est en panne), avec score, priorité, délai de rappel, bouton « Appeler », pièces jointes et boutons d'action.
2. Accusé de réception au prospect s'il a donné un e-mail (texte : `automation/messages/accuse-reception-*.md`).
3. Webhook signé HMAC-SHA256 vers n8n (CRM, SMS, relances) ; file d'attente locale en cas d'échec.

Le délai annoncé (« aujourd'hui avant 16 h 30 ») est calculé en heures ouvrables (lu-ve 7 h-18 h, jours fériés genevois) selon la priorité ; la priorité n'est jamais montrée au visiteur. Détails : `docs/v2/automatisation.md`.

---

## 14. Écarts avec les documents précédents

| Document | Ancien | Ce contrat |
|---|---|---|
| `architecture-cro.md` §6.2 | `fichier[]`, « 10 Mo au total » | `fichiers[]` (l'ancien nom reste accepté), 8 Mo par fichier, HEIC accepté |
| `architecture-cro.md` §6.2-6.3, copy deck §A.5 | case `accord` | supprimée (D2) ; champ ignoré s'il est envoyé |
| copy deck §Q.4 | `formulaire=aimant`, `aimant=guide-bruit`, `par_poste=oui`, `adresse_postale` sur 3 lignes, case `accord` | `formulaire=envoi_postal_guide`, `guide=guide-reduire-le-bruit`, champs `adresse`, `npa`, `localite`, e-mail et `conseils_email` facultatifs (ancien format accepté) |
| `architecture-cro.md` §13 | `plaquette_telechargee`, `guide_telecharge`, `aimant_demande` | `telechargement` + `data-suivi-doc` (D7), `guide_poste_demande` |
| copy deck §Q.1, Q.3 | `andy-construct-dossier-de-references.pdf`, `liste-de-controle-immeuble-habite.pdf` | noms de D7 : `andy-construct-references.pdf`, `checklist-chantier-site-occupe.pdf` |
