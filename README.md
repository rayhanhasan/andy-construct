# Andy Construct — site d'acquisition (v2)

Site d'acquisition d'**Andy Construct** (placo, peinture, isolation acoustique, cloisons isothermes ; toute la Suisse romande ; siège à Carouge), avec la stratégie d'acquisition et l'automatisation complètes. Préparé par Harbor Digital. La maquette v1 correspond au commit `ec5f98d`.

Pour reprendre le projet : lire **`HANDOFF.md`**.

## Contenu du dépôt

| Dossier | Rôle |
|---|---|
| `tools/build/` | **Générateur** du site (Python, sans dépendance). Source de vérité du HTML, CSS (`static/`) et JS |
| `tools/build/donnees/` | `confirmations.json` (points C01-C44 validés ou non), `config.json` (Umami), `temoignages.json`, `avis.json` |
| `site/` | Site généré en mode **preview** (validation) : 13 pages + `api/` (traitement PHP des formulaires) |
| `site/api/` | Endpoint PHP : demandes de devis, rappels, envois postaux ; scoring A/B/C ; anti-spam ; e-mails ; webhook signé vers n8n. Tests : `php site/api/tests/run.php` |
| `automation/n8n/` | 16 workflows n8n importables + `verifier.py` ; `docker-compose.yml` pour l'auto-hébergement |
| `automation/messages/` | Tous les messages (accusés, relances, avis, SMS, courriers et script de prospection) |
| `livrables/` | Plaquette de validation, suivi Excel des demandes et KPI, sources des PDF |
| `site/assets/docs/` | PDF téléchargeables : dossier de références, guide bruit, check-list régies |
| `docs/v2/` | Programme, audit, enquête client, concurrence, personas, stratégie, logos, architecture CRO, copy deck, contrat d'interface, automatisation, décisions, QA |
| `docs/` (racine) | Documents de la maquette v1 (charte `brief-design.md`, analyse de marché v1, brief SEO v1) |
| `deploy/deploy_ftp.py` | Envoi FTP verrouillé sur `res/` de harbor-digital.fr |

## Générer le site

```bash
python3 tools/build/build.py                                    # preview (défaut) → site/
python3 tools/build/build.py --mode verification --out /tmp/av  # points à confirmer soulignés (code Cxx)
python3 tools/build/build.py --mode production --out dist/      # textes de repli, logos « autorise » seulement, indexable
```

## Tester

```bash
php site/api/tests/run.php                  # 266 vérifications
bash site/api/tests/endpoint.sh             # 57 vérifications HTTP
python3 automation/n8n/verifier.py          # 16 workflows
cd site && php -S localhost:8080            # site + formulaire (créer un config.php de test, mode test)
```

## Déployer la version de validation sur harbor-digital.fr/res

```bash
export FTP_HOST=46.202.172.2 FTP_USER='…' FTP_PASS='…'
python3 deploy/deploy_ftp.py --subdir andy-construct-v2 --dry-run
python3 deploy/deploy_ftp.py --subdir andy-construct-v2
```

Le script n'écrit que dans `res/`, n'efface rien et n'envoie ni les tests ni le stockage de l'API. Les identifiants ne sont jamais écrits dans le dépôt.

## Mise en production

Voir la check-list de `HANDOFF.md` §9 et `docs/v2/automatisation.md` (installation n8n, SMTP, CRM, Umami, recette).
