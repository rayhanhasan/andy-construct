#!/usr/bin/env python3
"""Vérification des workflows n8n d'Andy Construct.

    python3 automation/n8n/verifier.py

Contrôles :
  1. chaque fichier JSON se lit et a la forme d'un export n8n (nodes, connections, settings) ;
  2. noms et identifiants de nœuds uniques, types et versions connus, positions, notes en français ;
  3. toutes les connexions partent d'un nœud existant et pointent vers un nœud existant,
     sur une sortie qui existe (IF : 2, Switch : règles + « autre ») ;
  4. chaque nœud est atteignable depuis un déclencheur ; chemins de webhook uniques ;
  5. aucun secret en clair (clés, jetons) : uniquement des variables d'environnement et
     des identifiants à remplacer (« REMPLACER-… ») ;
  6. syntaxe JavaScript de chaque nœud Code et de chaque expression {{ … }} (node --check) ;
  7. interopérabilité avec site/api (si php et node sont disponibles) : signature HMAC du
     webhook et jetons des liens en un clic, dans les deux sens ;
  8. exécution à blanc de nœuds Code clés avec une vraie charge produite par le PHP
     (si le module luxon est disponible : NODE_PATH ou npm i luxon).

Code de sortie 0 si tout passe.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parents[1]
API = RACINE / 'site' / 'api'

TYPES = {
    'n8n-nodes-base.webhook': [2], 'n8n-nodes-base.respondToWebhook': [1.1], 'n8n-nodes-base.code': [2],
    'n8n-nodes-base.if': [2], 'n8n-nodes-base.switch': [3], 'n8n-nodes-base.scheduleTrigger': [1.2],
    'n8n-nodes-base.httpRequest': [4.2], 'n8n-nodes-base.emailSend': [2.1], 'n8n-nodes-base.wait': [1.1],
    'n8n-nodes-base.noOp': [1], 'n8n-nodes-base.stickyNote': [1], 'n8n-nodes-base.errorTrigger': [1],
    'n8n-nodes-base.pipedriveTrigger': [1], 'n8n-nodes-base.emailReadImap': [2],
}
DECLENCHEURS = {'n8n-nodes-base.webhook', 'n8n-nodes-base.scheduleTrigger', 'n8n-nodes-base.errorTrigger',
                'n8n-nodes-base.pipedriveTrigger', 'n8n-nodes-base.emailReadImap'}
SECRETS = [re.compile(p) for p in (r'\b[a-f0-9]{32,}\b', r'xkeysib-', r'sk_live_', r'AIza[0-9A-Za-z_-]{20,}',
                                    r'(?i)"(password|api_key|apikey|token)"\s*:\s*"[^"={][^"]{6,}"')]

erreurs, avertissements, reussites = [], [], []


def erreur(f, m):
    erreurs.append(f'{f} : {m}')


def ok(m):
    reussites.append(m)


def sorties_max(n):
    t = n['type']
    if t == 'n8n-nodes-base.if':
        return 2
    if t == 'n8n-nodes-base.switch':
        return len(n['parameters']['rules']['values']) + (1 if n['parameters'].get('options', {}).get('fallbackOutput') == 'extra' else 0)
    return 1


def expressions(valeur):
    """Toutes les expressions {{ … }} des paramètres (chaînes commençant par « = »)."""
    if isinstance(valeur, dict):
        for v in valeur.values():
            yield from expressions(v)
    elif isinstance(valeur, list):
        for v in valeur:
            yield from expressions(v)
    elif isinstance(valeur, str) and valeur.startswith('='):
        for m in re.finditer(r'\{\{(.*?)\}\}', valeur, re.S):
            yield m.group(1)


def verifier_fichier(chemin, chemins_webhook, js):
    f = chemin.name
    try:
        wf = json.loads(chemin.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        erreur(f, f'JSON illisible ({e})')
        return
    for cle in ('name', 'nodes', 'connections', 'settings'):
        if cle not in wf:
            erreur(f, f'clé « {cle} » absente')
            return
    noeuds = {n['name']: n for n in wf['nodes']}
    if len(noeuds) != len(wf['nodes']):
        erreur(f, 'noms de nœuds en double')
    if len({n['id'] for n in wf['nodes']}) != len(wf['nodes']):
        erreur(f, 'identifiants de nœuds en double')
    for n in wf['nodes']:
        if n['type'] not in TYPES:
            erreur(f, f"type inconnu « {n['type']} » ({n['name']})")
        elif n['typeVersion'] not in TYPES[n['type']]:
            erreur(f, f"version {n['typeVersion']} inattendue pour {n['type']} ({n['name']})")
        if not (isinstance(n.get('position'), list) and len(n['position']) == 2):
            erreur(f, f"position invalide ({n['name']})")
        if n['type'] != 'n8n-nodes-base.stickyNote' and len(n.get('notes', '')) < 10:
            erreur(f, f"note explicative absente ({n['name']})")
        for nom_cred, cred in (n.get('credentials') or {}).items():
            if not str(cred.get('id', '')).startswith('REMPLACER'):
                erreur(f, f"identifiant d'accès non générique ({n['name']} : {nom_cred})")
        if n['type'] == 'n8n-nodes-base.webhook':
            cle = (n['parameters']['httpMethod'], n['parameters']['path'])
            if cle in chemins_webhook:
                erreur(f, f'chemin de webhook déjà utilisé : {cle} ({chemins_webhook[cle]})')
            chemins_webhook[cle] = f
        if n['type'] == 'n8n-nodes-base.code':
            js.append((f, n['name'], 'code', n['parameters']['jsCode']))
        for e in expressions(n['parameters']):
            js.append((f, n['name'], 'expression', e))
    # Connexions
    for source, sorties in wf['connections'].items():
        if source not in noeuds:
            erreur(f, f'connexion depuis un nœud inexistant « {source} »')
            continue
        if noeuds[source]['type'] == 'n8n-nodes-base.stickyNote':
            erreur(f, f'connexion depuis un post-it « {source} »')
        principal = sorties.get('main', [])
        if len(principal) > sorties_max(noeuds[source]):
            erreur(f, f'« {source} » utilise {len(principal)} sorties pour {sorties_max(noeuds[source])} possibles')
        for liste in principal:
            for c in liste:
                if c['node'] not in noeuds:
                    erreur(f, f"connexion de « {source} » vers un nœud inexistant « {c['node']} »")
                elif c.get('type') != 'main' or not isinstance(c.get('index'), int):
                    erreur(f, f'connexion mal formée {source} → {c}')
    # Atteignabilité
    suivants = {}
    for source, sorties in wf['connections'].items():
        for liste in sorties.get('main', []):
            for c in liste:
                suivants.setdefault(source, set()).add(c['node'])
    departs = [n for n, d in noeuds.items() if d['type'] in DECLENCHEURS]
    if not departs:
        erreur(f, 'aucun déclencheur')
    vus, pile = set(departs), list(departs)
    while pile:
        for s in suivants.get(pile.pop(), ()):
            if s not in vus:
                vus.add(s)
                pile.append(s)
    for n, d in noeuds.items():
        if d['type'] != 'n8n-nodes-base.stickyNote' and n not in vus:
            erreur(f, f'nœud inatteignable « {n} »')
    # Secrets
    texte = chemin.read_text(encoding='utf-8')
    for motif in SECRETS:
        m = motif.search(re.sub(r'"(id|versionId|webhookId)": "[^"]+"', '', texte))
        if m:
            erreur(f, f'secret possible en clair : {m.group(0)[:30]}…')
    if wf['settings'].get('timezone') != 'Europe/Zurich':
        erreur(f, 'fuseau horaire attendu : Europe/Zurich')
    ok(f"{f} : {len(wf['nodes'])} nœuds, {sum(len(l) for s in wf['connections'].values() for l in s.get('main', []))} connexions")


def verifier_js(js):
    if not shutil.which('node'):
        avertissements.append('node absent : syntaxe JavaScript non vérifiée')
        return
    with tempfile.TemporaryDirectory() as d:
        fichiers = []
        for i, (f, noeud, nature, source) in enumerate(js):
            p = Path(d) / f'x{i}.js'
            if nature == 'code':
                p.write_text('(async function () {\n' + source + '\n});\n', encoding='utf-8')
            else:
                p.write_text('(function ($json, $, $env, $now, DateTime, $input) { return (' + source + '\n); });\n', encoding='utf-8')
            fichiers.append((p, f, noeud, nature))
        for p, f, noeud, nature in fichiers:
            r = subprocess.run(['node', '--check', str(p)], capture_output=True, text=True)
            if r.returncode:
                erreur(f, f'syntaxe JS ({nature}) dans « {noeud} » : ' + r.stderr.strip().splitlines()[-1][:200])
    ok(f'syntaxe JavaScript : {sum(1 for j in js if j[2] == "code")} nœuds Code et {sum(1 for j in js if j[2] == "expression")} expressions')


# ------------------------------------------------------------------ exécution à blanc
HARNAIS = r"""
const fs = require('fs');
const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
let DateTime = null;
try { DateTime = require('luxon').DateTime; } catch (e) { if (spec.luxon) { console.log(JSON.stringify({ ignore: 'luxon' })); process.exit(0); } }
const elt = (j) => ({ json: j, binary: spec.binaire ? { data: { data: Buffer.from(spec.binaire).toString('base64') } } : undefined });
const entrees = (spec.entrees || [{}]).map(elt);
const $input = { first: () => entrees[0], all: () => entrees, item: entrees[0] };
const $ = (nom) => { const v = (spec.noeuds || {})[nom]; const l = (v === undefined ? [] : Array.isArray(v) ? v : [v]).map((j) => ({ json: j }));
  return { first: () => l[0], all: () => l, item: l[0], isExecuted: v !== undefined }; };
const statique = {};
const helpers = { getBinaryDataBuffer: async () => { if (spec.binaire) return Buffer.from(spec.binaire); throw new Error('pas de binaire'); } };
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
const f = new AsyncFunction('$input', '$env', '$', '$getWorkflowStaticData', '$now', 'DateTime', 'require', spec.code);
f.call({ helpers }, $input, spec.env || {}, $, () => statique, DateTime ? DateTime.now() : null, DateTime, require)
  .then((r) => console.log(JSON.stringify({ resultat: r })))
  .catch((e) => console.log(JSON.stringify({ exception: String(e && e.stack || e) })));
"""


def executer(code, **spec):
    with tempfile.TemporaryDirectory() as d:
        h = Path(d) / 'harnais.js'
        h.write_text(HARNAIS, encoding='utf-8')
        s = Path(d) / 'spec.json'
        s.write_text(json.dumps({'code': code, **spec}), encoding='utf-8')
        r = subprocess.run(['node', str(h), str(s)], capture_output=True, text=True, env=os.environ)
        try:
            return json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:
            return {'exception': r.stderr[-500:]}


def noeud(fichier, nom):
    wf = json.loads((ICI / fichier).read_text(encoding='utf-8'))
    return next(n for n in wf['nodes'] if n['name'] == nom)['parameters']['jsCode']


def php(script):
    r = subprocess.run(['php', '-r', script], capture_output=True, text=True, cwd=str(API))
    if r.returncode:
        raise RuntimeError(r.stderr)
    return r.stdout


def verifier_interop():
    if not (shutil.which('php') and shutil.which('node') and (API / 'lib' / 'bootstrap.php').exists()):
        avertissements.append('php ou node absent : interopérabilité non vérifiée')
        return
    secret_hmac = 'secret-hmac-verif-0123456789abcdef0123456789'
    secret_act = 'secret-actions-verif-0123456789abcdef01234567'
    env = {'AC_HMAC_SECRET': secret_hmac, 'AC_ACTION_SECRET': secret_act, 'AC_N8N_URL': 'https://n8n.exemple.ch',
           'AC_PD_CHAMPS': json.dumps({'ref_demande': 'k_ref', 'score': 'k_score', 'priorite': 'k_prio', 'sla_echeance': 'k_sla',
                                       'tentatives_appel': 'k_tent', 'relance_sla_niveau': 'k_niv', 'service': 'k_serv', 'commune': 'k_com', 'zone': 'k_zone'}),
           'AC_PD_IDS': json.dumps({'pipeline_demandes': 1, 'etape_nouvelle': 1, 'etape_contact': 2, 'utilisateur_terrain': 11, 'utilisateur_bureau': 12}),
           'AC_ASSOCIE_TERRAIN_MOBILE': '+41790000001', 'AC_EMAIL_EXPEDITEUR': 'site@andyconstruct.ch'}
    # Charge réelle produite par le PHP (même encodage, même signature que demande.php).
    sortie = php(r"""
require 'lib/bootstrap.php';
use AndyConstruct\Api\{Webhook, Jeton};
$charge = ['evenement' => 'demande.creee', 'version' => 1, 'ref' => 'AC-2026-0042', 'recu_le' => '2026-11-02T10:07:00+01:00', 'formulaire' => 'devis', 'canal' => 'site',
  'contact' => ['civilite' => 'madame', 'nom' => 'Françoise Dupont', 'prenom' => '', 'salutation' => 'Bonjour Madame Françoise Dupont', 'email' => '', 'telephone' => '+41791234567',
    'telephone_affiche' => '079 123 45 67', 'telephone_mobile' => true, 'telephone_suisse' => true, 'preference_contact' => '', 'creneau' => '', 'adresse_postale' => ''],
  'projet' => ['travaux' => ['isolation-acoustique'], 'service' => 'isolation-acoustique', 'service_libelle' => 'Isolation acoustique', 'type_client' => 'proprietaire',
    'surface' => '15-50', 'delai' => '1-3-mois', 'commune' => 'Chêne-Bourg', 'npa' => '1225', 'canton' => 'GE', 'zone' => '1', 'localite_methode' => 'commune-exacte',
    'message' => "Bruit « voisin » / plafond\nligne 2", 'recommande_par' => '', 'connu_par' => 'recherche-google'],
  'guide' => null, 'scoring' => ['score' => 71, 'priorite' => 'A', 'detail' => [['critere' => 'zone', 'valeur' => '1', 'points' => 15]], 'regles' => [], 'hors_cible' => [],
    'echeance' => '2026-11-02T12:07:00+01:00', 'promesse' => "aujourd'hui avant 12 h 15"],
  'attribution' => ['role' => 'terrain', 'associe' => 'Caroline Chanton Bajrami', 'email' => ''],
  'source' => ['categorie' => 'recherche-google', 'libelle' => 'recherche naturelle', 'page' => '/contact.html', 'page_entree' => '/', 'utm_source' => ''], 'fichiers' => [],
  'accuse_reception' => 'non', 'anti_spam' => ['jeton' => 'ok', 'delai_remplissage_s' => 42]];
$corps = Webhook::encoder($charge);
$ts = time();
$j = new Jeton('""" + secret_act + r"""');
echo json_encode(['corps' => $corps, 'ts' => (string) $ts, 'sig' => Webhook::signer('""" + secret_hmac + r"""', $corps, $ts),
  'jeton' => $j->creer(['a' => 'menu', 'r' => 'AC-2026-0042'], 3600)]);
""")
    p = json.loads(sortie)
    code_hmac = noeud('wf01-nouvelle-demande.json', 'Vérifier la signature HMAC')
    entete = {'headers': {'x-ac-timestamp': p['ts'], 'x-ac-signature': p['sig']}, 'body': json.loads(p['corps'])}
    r = executer(code_hmac, entrees=[entete], env=env, binaire=p['corps'])
    if r.get('resultat', [{}])[0].get('json', {}).get('valide') is True:
        ok('HMAC : signature PHP acceptée par WF01 (corps brut)')
    else:
        erreur('wf01', f'signature PHP refusée par le nœud de vérification : {r}')
    r = executer(code_hmac, entrees=[entete], env=env)
    if r.get('resultat', [{}])[0].get('json', {}).get('valide') is True:
        ok('HMAC : signature PHP acceptée par WF01 (repli JSON.stringify, sans corps brut)')
    else:
        erreur('wf01', f'repli JSON.stringify refusé : {r}')
    r = executer(code_hmac, entrees=[entete], env=env, binaire=p['corps'].replace('Dupont', 'Durand'))
    if r.get('resultat', [{}])[0].get('json', {}).get('valide') is False:
        ok('HMAC : corps modifié refusé')
    else:
        erreur('wf01', 'corps modifié accepté')
    r = executer(code_hmac, entrees=[{**entete, 'headers': {'x-ac-timestamp': str(int(p['ts']) - 600), 'x-ac-signature': p['sig']}}], env=env, binaire=p['corps'])
    if r.get('resultat', [{}])[0].get('json', {}).get('raison') == 'horodatage':
        ok('HMAC : horodatage de plus de 5 minutes refusé')
    else:
        erreur('wf01', 'horodatage ancien accepté')
    # Jeton PHP → n8n (page de WF02)
    code_page = noeud('wf02-actions-un-clic.json', 'Page de confirmation')
    r = executer(code_page, entrees=[{'query': {'t': p['jeton']}}], env=env)
    page = r.get('resultat', [{}])[0].get('json', {})
    if page.get('code') == 200 and 'contact-etabli' in page.get('html', ''):
        ok('jeton : créé par le PHP, vérifié par WF02 (page avec 3 boutons)')
    else:
        erreur('wf02', f'jeton PHP refusé : {r}')
    r = executer(code_page, entrees=[{'query': {'t': p['jeton'][:-2] + 'xx'}}], env=env)
    if r.get('resultat', [{}])[0].get('json', {}).get('code') == 410:
        ok('jeton : signature modifiée refusée par WF02')
    else:
        erreur('wf02', 'jeton modifié accepté')
    # Jeton n8n → PHP
    debut = code_page.index('// Jetons signés')
    fin = code_page.index('function page(')
    r = executer(code_page[debut:fin] + "\nreturn creerJeton({ a: 'stop', e: 'x@exemple.ch' }, 3600);", env=env)
    jeton_js = r.get('resultat', '')
    verif = php("require 'lib/bootstrap.php'; echo json_encode((new AndyConstruct\\Api\\Jeton('" + secret_act + "'))->verifier('" + str(jeton_js) + "'));")
    if json.loads(verif or 'null') and json.loads(verif)['e'] == 'x@exemple.ch':
        ok('jeton : créé par n8n, vérifié par le PHP')
    else:
        erreur('wf12', f'jeton n8n refusé par le PHP : {verif}')
    # Sécurité (docs/v2/qa/securite.md) : jeton suivi d'une injection HTML → refusé ; valeur échappée.
    injection = '."><meta http-equiv="refresh" content="0;url=https://evil.example/">'
    for fichier, nom_noeud, donnees in (('wf02-actions-un-clic.json', 'Page de confirmation', "{ a: 'offre-autre', d: 42 }"),
                                        ('wf12-desinscription.json', 'Page de confirmation', "{ a: 'stop', e: 'x@exemple.ch' }")):
        r = executer(code_page[debut:fin] + f"\nreturn creerJeton({donnees}, 3600);", env=env)
        jeton_ok = r.get('resultat', '')
        page_ok = executer(noeud(fichier, nom_noeud), entrees=[{'query': {'t': jeton_ok}}], env=env).get('resultat', [{}])[0].get('json', {})
        page_inj = executer(noeud(fichier, nom_noeud), entrees=[{'query': {'t': jeton_ok + injection}}], env=env).get('resultat', [{}])[0].get('json', {})
        if ('value="' + jeton_ok + '"') in page_ok.get('html', '') and 'evil.example' not in page_inj.get('html', '') and '<form' not in page_inj.get('html', ''):
            ok(f'sécurité : {fichier[:4]} refuse un jeton suivi de HTML (« jeton.<balise> ») et n\'injecte rien dans la page')
        else:
            erreur(fichier, f'injection HTML par le paramètre t : {page_inj.get("html", "")[:300]}')
    # Signature de même longueur en caractères mais pas en octets : refus propre, sans exception.
    sig_multi = 'sha256=' + 'é' * 64
    r = executer(code_hmac, entrees=[{**entete, 'headers': {'x-ac-timestamp': p['ts'], 'x-ac-signature': sig_multi}}], env=env, binaire=p['corps'])
    if r.get('resultat', [{}])[0].get('json', {}).get('valide') is False and 'exception' not in r:
        ok('sécurité : signature HMAC à caractères multi-octets refusée sans exception (comparaison en octets)')
    else:
        erreur('wf01', f'signature multi-octets : {r}')
    code_action = noeud('wf02-actions-un-clic.json', "Vérifier le jeton et l'usage unique")
    r = executer(code_action, entrees=[{'body': {'t': p['jeton'][:-1] + 'é', 'choix': 'contact-etabli'}}], env=env)
    if r.get('resultat', [{}])[0].get('json', {}).get('valide') is False and 'exception' not in r:
        ok('sécurité : jeton à signature multi-octets refusé sans exception (WF02)')
    else:
        erreur('wf02', f'jeton multi-octets : {r}')

    # Exécution à blanc de « Préparer la demande » (luxon nécessaire)
    r = executer(noeud('wf01-nouvelle-demande.json', 'Préparer la demande'), entrees=[{'demande': json.loads(p['corps'])}], env=env, luxon=True)
    if r.get('ignore'):
        avertissements.append('luxon absent : exécution à blanc des nœuds Code ignorée (npm i luxon puis NODE_PATH)')
        return
    j = (r.get('resultat') or [{}])[0].get('json', {})
    sms = j.get('sms_interne', {}).get('texte', '')
    if 'exception' in r:
        erreur('wf01', 'Préparer la demande : ' + r['exception'][:300])
    elif '{{' in sms or 'Chene-Bourg' not in sms or 'https://n8n.exemple.ch/webhook/ac-action?t=' not in sms:
        erreur('wf01', f'SMS interne inattendu : {sms}')
    elif j['corps_affaire'].get('k_score') != 71 or j['corps_affaire'].get('k_prio') != 'A':
        erreur('wf01', f"champs Pipedrive inattendus : {j['corps_affaire']}")
    elif j.get('accuse_sms') is not True or 'http' in j['sms_accuse']['texte']:
        erreur('wf01', f"accusé SMS inattendu : {j.get('sms_accuse')}")
    else:
        ok('WF01 à blanc : affaire Pipedrive (score 71, A), SMS interne en alphabet GSM, accusé SMS sans lien')
        ok('  SMS interne : ' + sms[:110] + '…')
        ok('  SMS prospect : ' + j['sms_accuse']['texte'])
    # WF02 : « Pas de réponse », 1er essai, prospect sans e-mail → SMS sans lien + tâche
    affaire = {'id': 99, 'k_ref': 'AC-2026-0042', 'k_tent': 0, 'k_serv': 'peinture', 'k_com': 'Lancy', 'k_zone': '1',
               'person_id': {'name': 'Jean Martin', 'value': 5, 'email': [], 'phone': [{'value': '+41791112233'}]},
               'user_id': {'name': 'Caroline Chanton Bajrami', 'email': 'caroline@andyconstruct.ch', 'id': 11}}
    r = executer(noeud('wf02-actions-un-clic.json', "Traduire l'action"), entrees=[{'data': affaire}], env=env, luxon=True,
                 noeuds={"Vérifier le jeton et l'usage unique": {'jeton': {'a': 'menu', 'r': 'AC-2026-0042', 'n': 'ab'}, 'choix': 'pas-de-reponse'}})
    j = (r.get('resultat') or [{}])[0].get('json', {})
    if j.get('sms', {}).get('a') == '+41791112233' and 'http' not in j['sms']['texte'] and j.get('activite', {}).get('due_time') == '10:00' and j.get('maj', {}).get('k_tent') == 1:
        ok('WF02 à blanc : « Pas de réponse » → SMS sans lien, tâche demain 10 h, tentatives = 1')
    else:
        erreur('wf02', f'« Pas de réponse » inattendu : {r}')
    # WF03 à blanc : nom saisi dans le formulaire (repris par Pipedrive) échappé dans l'e-mail d'escalade.
    retard = {'id': 7, 'k_ref': 'AC-2026-0007', 'k_sla': '2020-01-06T08:00:00+01:00', 'k_niv': 0, 'k_prio': 'A', 'k_com': '<b>Lancy</b>',
              'person_id': {'name': '<img src=//evil.example/p.gif>', 'phone': []}, 'user_id': {'id': 11, 'name': 'Caroline'}}
    r = executer(noeud('wf03-rappel-non-fait.json', 'Délais dépassés'), entrees=[{'data': [retard]}], env=env, luxon=True)
    html = ((r.get('resultat') or [{}])[0].get('json', {}).get('courriel') or {}).get('html', '')
    if html and '<img' not in html and '&lt;img' in html and '<b>' not in html:
        ok('sécurité : WF03 échappe le nom et la commune dans l\'e-mail d\'escalade (HTML)')
    else:
        erreur('wf03', f'e-mail d\'escalade non échappé : {r if not html else html[:300]}')


def evaluer(expression, json_courant, noeuds=None, env=None):
    """Évalue une expression n8n « ={{ … }} » (IF) avec un $json et des $('nœud') simulés."""
    corps = re.match(r'^=\{\{(.*)\}\}$', expression, re.S).group(1)
    code = ("const $ = (n) => { const v = (spec.noeuds || {})[n]; return { first: () => ({ json: v }), item: { json: v } }; };\n"
            "const $json = spec.json, $env = spec.env || {};\nreturn (" + corps + ");")
    with tempfile.TemporaryDirectory() as d:
        s = Path(d) / 'spec.json'
        s.write_text(json.dumps({'json': json_courant, 'noeuds': noeuds or {}, 'env': env or {}}), encoding='utf-8')
        h = Path(d) / 'e.js'
        h.write_text("const spec = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'));\n"
                     "console.log(JSON.stringify((function () {\n" + code + "\n})()));\n", encoding='utf-8')
        r = subprocess.run(['node', str(h), str(s)], capture_output=True, text=True)
        try:
            return json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:
            return {'exception': r.stderr[-300:]}


def predecesseurs(wf, nom):
    return {src for src, c in wf['connections'].items() for sortie in c.get('main', []) for x in (sortie or []) if x['node'] == nom}


def verifier_relecture_juridique():
    """Points bloquants de docs/v2/qa/relecture-juridique-copy.md (opposition, appel, nombre d'e-mails)."""
    lire = lambda f: json.loads((ICI / f).read_text(encoding='utf-8'))
    # WF07 : aucun appel commercial automatique.
    wf07 = lire('wf07-guide-par-la-poste.json')
    texte07 = json.dumps(wf07, ensure_ascii=False)
    if 'courtoisie' not in json.dumps([n for n in wf07['nodes'] if n['type'] != 'n8n-nodes-base.stickyNote'], ensure_ascii=False) \
            and "type: 'call'" not in texte07 and "'Profil professionnel ?'" not in texte07:
        ok("relecture : WF07 ne crée aucun appel (seule la tâche « envoyer le guide imprimé »)")
    else:
        erreur('wf07', "un appel commercial automatique subsiste")
    # WF07 : opposition relue dans Pipedrive (et Brevo) après chaque attente.
    for etape in ('E2', 'E3'):
        pd = f'Pipedrive : opposition ? ({etape})'
        if predecesseurs(wf07, f'Envoyer {etape} ?') != {pd} or predecesseurs(wf07, pd) != {f'Brevo : toujours inscrit ? ({etape})'}:
            erreur('wf07', f'{etape} : la lecture de l\'opposition dans Pipedrive ne précède pas l\'envoi')
            continue
        if not shutil.which('node'):
            continue
        expr = next(n for n in wf07['nodes'] if n['name'] == f'Envoyer {etape} ?')['parameters']['conditions']['conditions'][0]['leftValue']
        env = {'AC_PD_CHAMPS': json.dumps({'opposition_marketing': 'k_opp'})}
        brevo = {f'Brevo : toujours inscrit ? ({etape})': {'emailBlacklisted': False, 'attributes': {}}}
        cas = [
            (evaluer(expr, {'data': {'id': 5}}, brevo, env), True, 'aucune opposition'),
            (evaluer(expr, {'data': {'id': 5, 'k_opp': '2026-11-03'}}, brevo, env), False, 'opposition dans Pipedrive'),
            (evaluer(expr, {'data': {'id': 5}}, {f'Brevo : toujours inscrit ? ({etape})': {'emailBlacklisted': True}}, env), False, 'désinscrit dans Brevo'),
            (evaluer(expr, {'data': {'id': 5}}, {f'Brevo : toujours inscrit ? ({etape})': {'error': 'timeout'}}, env), False, 'Brevo illisible'),
            (evaluer(expr, {}, brevo, env), False, 'personne illisible'),
        ]
        if all(r == attendu for r, attendu, _ in cas):
            ok(f'relecture : WF07 {etape} n\'est envoyé que sans opposition (Pipedrive, Brevo) ; lecture impossible = pas d\'envoi')
        else:
            erreur('wf07', f'{etape} : ' + ', '.join(f'{d} → {r}' for r, a, d in cas if r != a))
    # WF03d : opposition relue avant J+2, J+9, J+14 et le SMS.
    wf03d = lire('wf03d-demande-avis.json')
    if set(x['node'] for x in wf03d['connections']['Messages dus']['main'][0]) == {'Personne : opposition ?'} \
            and all(predecesseurs(wf03d, n) == {'Sans opposition'} for n in ('E-mail ?', 'SMS ?', 'Noter la date')):
        ok('relecture : WF03d relit la personne dans Pipedrive avant tout envoi (aucun chemin ne contourne « Sans opposition »)')
    else:
        erreur('wf03d', 'un envoi peut contourner la vérification de l\'opposition')
    if shutil.which('node') and any(n['name'] == 'Sans opposition' for n in wf03d['nodes']):
        env = {'AC_PD_CHAMPS': json.dumps({'opposition_marketing': 'k_opp'})}
        du = [{'deal_id': 1, 'person_id': 5, 'etape': 'J+9'}, {'deal_id': 2, 'person_id': 6, 'etape': 'J+9'}, {'deal_id': 3, 'person_id': 7, 'etape': 'J+14'}]
        r = executer(noeud('wf03d-demande-avis.json', 'Sans opposition'), env=env, noeuds={'Messages dus': du},
                     entrees=[{'data': {'id': 5, 'k_opp': '2026-11-03'}}, {'data': {'id': 6, 'k_opp': None}}, {'data': None}])
        gardes = [i['json']['deal_id'] for i in (r.get('resultat') or [])]
        if gardes == [2]:
            ok('relecture : WF03d, « STOP » enregistré → relance J+9 annulée ; personne illisible → rien n\'est envoyé')
        else:
            erreur('wf03d', f'filtre d\'opposition inattendu : {r}')
    # WF03c : sans téléphone, deux e-mails au plus (J+3 et J+10).
    wf03c = lire('wf03c-relances-offre.json')
    if "Noter l'étape de relance" not in [x['node'] for x in (wf03c['connections']["Type d'action"]['main'] + [[]] * 5)[4]]:
        erreur('wf03c', "la sortie « autre » (aucun message) ne note pas l'étape : J+35 et J+45 n'arriveraient jamais")
    if shutil.which('node'):
        env = {'AC_ACTION_SECRET': 'secret-actions-verif-0123456789abcdef01234567', 'AC_N8N_URL': 'https://n8n.exemple.ch',
               'AC_PD_CHAMPS': json.dumps({'date_offre': 'k_do', 'relance_offre_etape': 'k_et', 'priorite': 'k_prio', 'type_client': 'k_tc'}),
               'AC_PD_IDS': json.dumps({'pipeline_ao': 99}), 'AC_EMAIL_EXPEDITEUR': 'site@andyconstruct.ch'}
        il_y_a = lambda j: (__import__('datetime').date.today() - __import__('datetime').timedelta(days=j)).isoformat()
        def affaire(i, etape, jours, tel):
            return {'id': i, 'pipeline_id': 1, 'k_do': il_y_a(jours), 'k_et': etape, 'k_prio': 'B', 'k_tc': 'proprietaire', 'title': 'Offre',
                    'person_id': {'name': 'Jean Martin', 'email': [{'value': 'jean@exemple.ch'}], 'phone': [{'value': '+41791112233'}] if tel else []}}
        r = executer(noeud('wf03c-relances-offre.json', 'Relance due'), env=env, luxon=True,
                     entrees=[{'data': [affaire(1, 1, 11, False), affaire(2, 2, 22, False), affaire(3, 2, 22, True), affaire(4, 1, 11, True)]}])
        if r.get('ignore'):
            return
        types = {i['json']['deal_id']: i['json']['type'] for i in (r.get('resultat') or [])}
        if types == {1: 'email', 2: 'aucune', 3: 'email', 4: 'tache'}:
            ok('relecture : WF03c sans téléphone → e-mails J+3 et J+10 seulement (J+21 : étape notée, aucun message) ; avec téléphone → appel J+10, e-mail J+21')
        else:
            erreur('wf03c', f'relances inattendues : {types or r}')


def main():
    fichiers = sorted(ICI.glob('wf*.json'))
    if not fichiers:
        print('Aucun workflow trouvé.')
        return 1
    chemins, js = {}, []
    for f in fichiers:
        verifier_fichier(f, chemins, js)
    verifier_js(js)
    verifier_interop()
    verifier_relecture_juridique()
    for m in reussites:
        print('  ✔ ' + m)
    for m in avertissements:
        print('  ! ' + m)
    for m in erreurs:
        print('  ✘ ' + m)
    print(f"\n{len(fichiers)} workflows, {len(reussites)} contrôles réussis, {len(erreurs)} erreur(s), {len(avertissements)} avertissement(s)")
    return 1 if erreurs else 0


if __name__ == '__main__':
    sys.exit(main())
