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
