#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fichier de suivi des demandes et des KPI d'Andy Construct (outil de démarrage, scénario S).

Produit livrables/suivi-demandes-et-kpi.xlsx. Le scoring reprend exactement la grille de
site/api/data/scoring.json (stratégie d'acquisition §2.3 à §2.5) et la table NPA → zone de
site/api/data/zones.json : un même prospect obtient le même score dans le fichier et dans l'API.
Toutes les valeurs calculées sont des formules ; les paramètres sont dans l'onglet « Paramètres ».

Usage : python3 livrables/sources/generer_suivi_xlsx.py
Ensuite, recalculer (LibreOffice) pour vérifier qu'aucune formule ne renvoie d'erreur.
"""
import datetime as dt
import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

ICI = Path(__file__).resolve().parent
RACINE = ICI.parents[1]
SORTIE = RACINE / 'livrables' / 'suivi-demandes-et-kpi.xlsx'
SCORING = json.loads((RACINE / 'site' / 'api' / 'data' / 'scoring.json').read_text(encoding='utf-8'))
ZONES = json.loads((RACINE / 'site' / 'api' / 'data' / 'zones.json').read_text(encoding='utf-8'))

N_LIGNES = 500            # lignes de saisie préparées
L0 = 5                    # première ligne de données de « Demandes »
LMAX = 2000               # plage lue par les synthèses (marge pour les lignes ajoutées)

# Charte : anthracite, graphite, brume, trait ; rouge en ponctuation
ANTH, GRAPH, BRUME, TRAIT, ROUGE, ROUGE_F = '1D1F22', '44494F', 'F4F4F5', 'E2E3E5', 'E8000F', 'C4000D'
POLICE = 'Arial'
f_base = Font(name=POLICE, size=10, color=ANTH)
f_saisie = Font(name=POLICE, size=10, color='0000FF')
f_titre = Font(name=POLICE, size=16, bold=True, color=ANTH)
f_sous = Font(name=POLICE, size=10, color=GRAPH)
f_entete = Font(name=POLICE, size=10, bold=True, color='FFFFFF')
f_gras = Font(name=POLICE, size=10, bold=True, color=ANTH)
f_section = Font(name=POLICE, size=12, bold=True, color=ANTH)
fill = lambda c: PatternFill('solid', start_color=c, end_color=c)
F_ANTH, F_GRAPH, F_BRUME = fill(ANTH), fill(GRAPH), fill(BRUME)
F_JAUNE = fill('FFF2CC')
F_EXEMPLE = fill('FFF6D5')
trait = Side(style='thin', color=TRAIT)
B_CASE = Border(left=trait, right=trait, top=trait, bottom=trait)
B_TITRE = Border(bottom=Side(style='medium', color=ROUGE))
A_WRAP = Alignment(wrap_text=True, vertical='top')
A_CENTRE = Alignment(horizontal='center', vertical='center', wrap_text=True)

wb = Workbook()


def nom(nom_, ref):
    wb.defined_names[nom_] = DefinedName(nom_, attr_text=ref)


def ecrire(ws, cell, v, font=f_base, fill_=None, fmt=None, align=None, border=None):
    c = ws[cell]
    c.value = v
    c.font = font
    if fill_:
        c.fill = fill_
    if fmt:
        c.number_format = fmt
    if align:
        c.alignment = align
    if border:
        c.border = border
    return c


def titre(ws, texte, sous=None, largeur=8):
    ecrire(ws, 'A1', texte, f_titre)
    for k in range(1, largeur + 1):
        ws.cell(1, k).border = B_TITRE
    ws.row_dimensions[1].height = 26
    if sous:
        ecrire(ws, 'A2', sous, f_sous)


def jours_feries_geneve(annees):
    """Jours fériés officiels du canton de Genève (loi genevoise sur les jours fériés, J 1 45)."""
    res = []
    for a in annees:
        # Pâques (algorithme de Meeus/Jones/Butcher)
        g = a % 19
        b, c = divmod(a, 100)
        d_, e_ = divmod(b, 4)
        f_ = (b + 8) // 25
        g_ = (b - f_ + 1) // 3
        h = (19 * g + b - d_ - g_ + 15) % 30
        i, k = divmod(c, 4)
        l_ = (32 + 2 * e_ + 2 * i - h - k) % 7
        m = (g + 11 * h + 22 * l_) // 451
        mois = (h + l_ - 7 * m + 114) // 31
        jour = (h + l_ - 7 * m + 114) % 31 + 1
        paques = dt.date(a, mois, jour)
        sept1 = dt.date(a, 9, 1)
        premier_dim = sept1 + dt.timedelta(days=(6 - sept1.weekday()) % 7)
        res += [
            (dt.date(a, 1, 1), 'Nouvel An'),
            (paques - dt.timedelta(days=2), 'Vendredi saint'),
            (paques + dt.timedelta(days=1), 'Lundi de Pâques'),
            (paques + dt.timedelta(days=39), 'Ascension'),
            (paques + dt.timedelta(days=50), 'Lundi de Pentecôte'),
            (dt.date(a, 8, 1), 'Fête nationale'),
            (premier_dim + dt.timedelta(days=4), 'Jeûne genevois'),
            (dt.date(a, 12, 25), 'Noël'),
            (dt.date(a, 12, 31), 'Restauration de la République'),
        ]
    return sorted(res)


def segments_npa():
    """Partition 0-9999 → zone, en appliquant les plages de zones.json (la première qui correspond l'emporte)."""
    z = ['Hors Suisse romande'] * 10000
    for n in range(1000, 3000):
        z[n] = str(ZONES['defaut_1000_2999']['zone'])
    pris = [False] * 10000
    for p in ZONES['plages']:
        for n in range(p['de'], p['a'] + 1):
            if not pris[n]:
                z[n] = 'Hors Suisse romande' if p['zone'] == 'hors' else str(p['zone'])
                pris[n] = True
    seg = []
    for n in range(10000):
        if not seg or seg[-1][2] != z[n]:
            seg.append([n, n, z[n]])
        else:
            seg[-1][1] = n
    return seg


# =============================================================================================
# Paramètres
# =============================================================================================
wp = wb.active
wp.title = 'Paramètres'
titre(wp, 'Paramètres', 'Grille de scoring, listes et délais. Les cellules jaunes se modifient ; '
      'la grille reprend site/api/data/scoring.json (stratégie d\'acquisition §2.3 à §2.5).', 12)
PQ = "'Paramètres'!"
S = SCORING

TYPES = [
    ('Commune ou institution', 'commune'), ('Régie, gérance ou coopérative', 'regie'),
    ('Architecte, bureau d\'études ou entreprise générale', 'architecte'),
    ('Entreprise, bureau ou commerce', 'entreprise'), ('Propriétaire (maison, appartement, PPE)', 'proprietaire'),
    ('Locataire', 'locataire'), ('Non précisé', ''),
]
SERVICES = [
    ('Placo', 'placo'), ('Peinture', 'peinture'), ('Isolation acoustique', 'isolation-acoustique'),
    ('Cloisons isolantes', 'cloisons-isothermes'), ('Plusieurs prestations', 'plusieurs'),
    ('Autre chose, ou ne sait pas encore', 'ne-sait-pas'), ('Hors des 4 services (façade, carrelage…)', 'autre'),
]
SURFACES = [
    ('Moins de 15 m² (une réparation)', 'moins-15'), ('15 à 50 m² (une ou deux pièces)', '15-50'),
    ('50 à 200 m² (un appartement, un étage)', '50-200'), ('Plus de 200 m², ou plusieurs logements', 'plus-200'),
    ('Je ne sais pas', 'ne-sait-pas'),
]
DELAIS = [
    ('Dès que possible (moins d\'un mois)', 'moins-1-mois'), ('Dans 1 à 3 mois', '1-3-mois'),
    ('Dans 3 à 6 mois', '3-6-mois'), ('Pas encore défini', 'non-defini'),
]
SOURCES = [  # libellé, clé de scoring.json, groupe affiché dans les KPI
    ('Recommandation', 'recommandation', 'Recommandation et réseau'),
    ('Partenaire (régie, architecte)', 'partenaire', 'Recommandation et réseau'),
    ('Prospection B2B', 'b2b', 'Recommandation et réseau'),
    ('Client existant', 'client-existant', 'Recommandation et réseau'),
    ('Appel direct', 'appel-direct', 'Appel direct, panneau'),
    ('Panneau de chantier ou véhicule', 'panneau-vehicule', 'Appel direct, panneau'),
    ('Carte Google (fiche Google)', 'carte-google', 'Google naturel et annuaires'),
    ('Recherche Google', 'recherche-google', 'Google naturel et annuaires'),
    ('Annuaire (local.ch, search.ch…)', 'annuaire', 'Google naturel et annuaires'),
    ('Google Ads', 'google-ads', 'Google Ads'),
    ('Guide ou dossier téléchargé', 'aimant', 'Guides et e-mails'),
    ('E-mail de suivi (séquence)', 'crm', 'Guides et e-mails'),
    ('Facebook ou Instagram (Meta)', 'meta', 'Réseaux sociaux'),
    ('LinkedIn', 'linkedin', 'Réseaux sociaux'),
    ('Plateforme de mise en relation', 'plateforme', 'Autres et inconnue'),
    ('Lien depuis un autre site', 'site-referent', 'Autres et inconnue'),
    ('Autre', 'autre', 'Autres et inconnue'),
    ('Inconnue', 'direct-inconnu', 'Autres et inconnue'),
]
GROUPES = ['Recommandation et réseau', 'Appel direct, panneau', 'Google naturel et annuaires', 'Google Ads',
           'Guides et e-mails', 'Réseaux sociaux', 'Autres et inconnue']
CANAUX = [  # libellé, bonus téléphone (comme l'API : formulaire du site seulement), plancher B
    ('Site : demande de devis', 'O', 'N'), ('Site : demande de rappel', 'O', 'O'),
    ('Téléphone', 'N', 'N'), ('E-mail', 'N', 'N'), ('Autre (visite, salon, courrier)', 'N', 'N'),
]
CANTONS = [('GE', '1'), ('VD', 'Inconnue'), ('NE', '3'), ('FR', '3'), ('VS', '3'), ('JU', '3'),
           ('BE (Jura bernois)', '3'), ('Hors Suisse romande', 'Hors Suisse romande')]
STATUTS = ['1 Nouvelle demande', '2 Contact établi', '3 Visite planifiée', '4 Offre envoyée',
           '5 Relance / négociation', 'Gagnée', 'Perdue']
MOTIFS = ['Prix', 'Délai', 'Reporté', 'Attribué ailleurs', 'Sans réponse', 'Hors cible']
r = S['regles']

tables = []   # (titre, entêtes, lignes, nom, largeurs)


def table(col, ligne, titre_, entetes, lignes, nom_, note=None, saisie_cols=()):
    """Écrit une table à partir de (col, ligne) ; renvoie la ligne suivante. Nom = plage des données."""
    c0 = col
    ecrire(wp, f'{get_column_letter(c0)}{ligne}', titre_, f_section)
    if note:
        ecrire(wp, f'{get_column_letter(c0)}{ligne + 1}', note, f_sous)
    l_ent = ligne + (2 if note else 1)
    for j, e in enumerate(entetes):
        ecrire(wp, f'{get_column_letter(c0 + j)}{l_ent}', e, f_entete, F_ANTH, align=A_CENTRE, border=B_CASE)
    for i, lg in enumerate(lignes):
        for j, v in enumerate(lg):
            saisie = j in saisie_cols
            ecrire(wp, f'{get_column_letter(c0 + j)}{l_ent + 1 + i}', v, f_saisie if saisie else f_base,
                   F_JAUNE if saisie else None, border=B_CASE,
                   fmt='dd.mm.yyyy' if isinstance(v, dt.date) else None)
    debut, fin = l_ent + 1, l_ent + len(lignes)
    if nom_:
        nom(nom_, f"{PQ}${get_column_letter(c0)}${debut}:${get_column_letter(c0 + len(entetes) - 1)}${fin}")
    return fin + 2, debut, fin


# Colonne A-D : grille de scoring
l = 4
l, d0, d1 = table(1, l, 'Type de client (0 à 30 points)', ['Valeur', 'Points', 'Jamais sous B (O/N)', 'Zone 3 sans pénalité (O/N)'],
                  [(lib, S['type_client'][k], 'O' if k in r['plancher_B_types_client'] else 'N',
                    'O' if k in r['zone3_sans_penalite_types_client'] else 'N') for lib, k in TYPES],
                  'T_Type', saisie_cols=(1, 2, 3))
nom('L_Type', f"{PQ}$A${d0}:$A${d1}")
l, d0, d1 = table(1, l, 'Service (0 à 15 points)', ['Valeur', 'Points', 'Hors cible (O/N)'],
                  [(lib, S['service'][k] if S['service'][k] is not None else 0, 'O' if S['service'][k] is None else 'N')
                   for lib, k in SERVICES], 'T_Service', saisie_cols=(1, 2))
nom('L_Service', f"{PQ}$A${d0}:$A${d1}")
l, d0, d1 = table(1, l, 'Surface (0 à 20 points)', ['Valeur', 'Points', 'Zone 3 sans pénalité (O/N)'],
                  [(lib, S['surface'][k], 'O' if k in r['zone3_sans_penalite_surfaces'] else 'N') for lib, k in SURFACES],
                  'T_Surface', saisie_cols=(1, 2))
nom('L_Surface', f"{PQ}$A${d0}:$A${d1}")
l, d0, d1 = table(1, l, 'Délai souhaité (0 à 10 points)', ['Valeur', 'Points', 'Urgent (O/N)'],
                  [(lib, S['delai'][k], 'O' if k == r['urgence_delai'] else 'N') for lib, k in DELAIS],
                  'T_Delai', saisie_cols=(1, 2))
nom('L_Delai', f"{PQ}$A${d0}:$A${d1}")
l, d0, d1 = table(1, l, 'Zone (0 à 15 points)', ['Zone', 'Points', 'Hors cible (O/N)'],
                  [('1', S['zone']['1'], 'N'), ('2', S['zone']['2'], 'N'), ('3', S['zone']['3'], 'N'),
                   ('Inconnue', S['zone']['inconnue'], 'N'), ('Hors Suisse romande', 0, 'O')],
                  'T_Zone', note='Zone 1 : canton de Genève et district de Nyon. Zone 2 : Morges, Lausanne, Ouest lausannois, '
                  'Lavaux-Oron, Riviera-Pays-d\'Enhaut. Zone 3 : reste de la Suisse romande.', saisie_cols=(1,))
l, d0, d1 = table(1, l, 'Source (0 à 10 points)', ['Valeur', 'Points', 'Groupe (KPI)'],
                  [(lib, S['source'][k], g) for lib, k, g in SOURCES], 'T_Source', saisie_cols=(1,))
nom('L_Source', f"{PQ}$A${d0}:$A${d1}")
l, d0, d1 = table(1, l, 'Canal de la demande', ['Valeur', 'Bonus téléphone (O/N)', 'Jamais sous B (O/N)'],
                  CANAUX, 'T_Canal', note='Comme l\'API : le bonus « téléphone fourni » ne vaut que pour le formulaire du site ; '
                  'une demande de rappel n\'est jamais sous B.', saisie_cols=(1, 2))
nom('L_Canal', f"{PQ}$A${d0}:$A${d1}")
fin_gauche = l

# Colonne F-G : seuils, bonus, délais
l = 4
ecrire(wp, f'F{l}', 'Seuils, bonus et valeurs par défaut', f_section)
reglages = [
    ('P_SeuilA', 'Priorité A à partir de (points)', S['seuils']['A'], 'Stratégie §2.4'),
    ('P_SeuilB', 'Priorité B à partir de (points)', S['seuils']['B'], 'En dessous : C'),
    ('P_BonusFichier', 'Bonus : photo ou plan joint', S['bonus']['fichier_joint'], ''),
    ('P_BonusTel', 'Bonus : téléphone fourni (formulaire du site)', S['bonus']['telephone_fourni'], ''),
    ('P_Malus', 'Malus : message vide et aucun téléphone', S['bonus']['message_vide_sans_telephone'], ''),
    ('P_TypeDefaut', 'Type de client non renseigné (points)', S['type_client'][''], ''),
    ('P_ServiceDefaut', 'Service non renseigné (points)', S['service'][''], ''),
    ('P_SurfaceDefaut', 'Surface non renseignée (points)', S['surface'][''], ''),
    ('P_DelaiDefaut', 'Délai non renseigné (points)', S['delai'][''], ''),
    ('P_SourceDefaut', 'Source non renseignée (points)', S['source']['direct-inconnu'], ''),
]
ecrire(wp, f'F{l + 1}', 'Réglage', f_entete, F_ANTH, align=A_CENTRE, border=B_CASE)
ecrire(wp, f'G{l + 1}', 'Valeur', f_entete, F_ANTH, align=A_CENTRE, border=B_CASE)
ecrire(wp, f'H{l + 1}', 'Note', f_entete, F_ANTH, align=A_CENTRE, border=B_CASE)
for i, (n_, lib, v, note) in enumerate(reglages):
    ll = l + 2 + i
    ecrire(wp, f'F{ll}', lib, border=B_CASE)
    ecrire(wp, f'G{ll}', v, f_saisie, F_JAUNE, border=B_CASE)
    ecrire(wp, f'H{ll}', note, f_sous, border=B_CASE)
    nom(n_, f"{PQ}$G${ll}")
l = l + 2 + len(reglages) + 1

ecrire(wp, f'F{l}', 'Délais de suivi', f_section)
ecrire(wp, f'F{l + 1}', 'Comptés en jours ouvrables (lundi-vendredi, hors jours fériés ci-dessous), sauf mention.', f_sous)
delais = [
    ('P_DelaiVisite', 'Contact établi : fixer la visite dans les (jours ouvrables)', 5, 'Valeur de départ, à ajuster'),
    ('P_DelaiOffre', 'Après la visite : envoyer l\'offre dans les (jours ouvrables)', 5, 'Valeur de départ ; question C08 au client'),
    ('P_Relance1', 'Offre envoyée : 1re relance à J+ (jours calendaires)', 3, 'Stratégie §5.7 (c)'),
    ('P_Relance2', 'Offre : 2e relance à J+ (jours calendaires)', 10, 'Stratégie §5.7 (c)'),
    ('P_Relance3', 'Offre : 3e relance à J+ (jours calendaires)', 21, 'Stratégie §5.7 (c)'),
    ('P_Clore', 'Offre sans réponse : proposer de clore à J+ (jours calendaires)', 35, 'Stratégie §5.7 (c)'),
    ('P_Avis', 'Fin de chantier : demander l\'avis à J+ (jours calendaires)', 2, 'Stratégie §5.7 (d)'),
]
ecrire(wp, f'F{l + 2}', 'Réglage', f_entete, F_ANTH, align=A_CENTRE, border=B_CASE)
ecrire(wp, f'G{l + 2}', 'Valeur', f_entete, F_ANTH, align=A_CENTRE, border=B_CASE)
ecrire(wp, f'H{l + 2}', 'Source', f_entete, F_ANTH, align=A_CENTRE, border=B_CASE)
for i, (n_, lib, v, note) in enumerate(delais):
    ll = l + 3 + i
    ecrire(wp, f'F{ll}', lib, border=B_CASE)
    ecrire(wp, f'G{ll}', v, f_saisie, F_JAUNE, border=B_CASE)
    ecrire(wp, f'H{ll}', note, f_sous, border=B_CASE)
    nom(n_, f"{PQ}$G${ll}")
l = l + 3 + len(delais) + 1

l, d0, d1 = table(6, l, 'Délai maximal de premier contact', ['Priorité', 'Jours ouvrables'],
                  [('A', 0), ('B', 1), ('C', 2), ('Hors cible', 1)], 'T_DelaiContact',
                  note='0 = le jour même. Stratégie §2.4 : A < 2 h ouvrables, B < 8 h, C < 2 jours, hors cible < 1 jour.',
                  saisie_cols=(1,))

ecrire(wp, f'F{l}', 'Mots qui signalent une urgence (dégât, fin de bail)', f_section)
ecrire(wp, f'F{l + 1}', 'Avec le délai « Dès que possible », la demande passe en A (stratégie §2.5, règle 2). Une case vide est ignorée.', f_sous)
mots = []
for m_ in r['urgence_mots']:
    if m_ not in mots and not any(m_.startswith(x) for x in mots):
        mots.append(m_)
for i in range(10):
    ecrire(wp, f'F{l + 2 + i}', mots[i] if i < len(mots) else None, f_saisie, F_JAUNE, border=B_CASE)
nom('T_Urgence', f"{PQ}$F${l + 2}:$F${l + 11}")
l = l + 13

l, d0, d1 = table(6, l, 'Canton → zone, si le NPA manque', ['Canton', 'Zone par défaut'], CANTONS, 'T_Canton',
                  note='Dans le canton de Vaud, saisissez le NPA : la zone dépend du district.', saisie_cols=(1,))
nom('L_Canton', f"{PQ}$F${d0}:$F${d1}")
fin_milieu = l

# Colonne J-L : listes et jours fériés
l = 4
l, d0, d1 = table(10, l, 'Statuts du pipeline', ['Statut'], [(s,) for s in STATUTS], 'L_Statut',
                  note='Ordre de la stratégie §5.5 ; « Gagnée » = offre signée.')
l, d0, d1 = table(10, l, 'Motifs de perte', ['Motif'], [(m_,) for m_ in MOTIFS], 'L_Motif')
l, d0, d1 = table(10, l, 'Oui / non', ['Valeur'], [('O',), ('N',)], 'L_ON')
l, d0, d1 = table(10, l, 'Groupes de sources (KPI)', ['Groupe'], [(g,) for g in GROUPES], 'L_Groupe')
feries = jours_feries_geneve([2026, 2027, 2028])
feries = [f for f in feries if f[0] >= dt.date(2026, 11, 1)]
ecrire(wp, f'J{l}', 'Jours fériés (canton de Genève)', f_section)
ecrire(wp, f'J{l + 1}', 'Exclus du calcul des jours ouvrables. Complétez la liste chaque année (cases jaunes libres).', f_sous)
ecrire(wp, f'J{l + 2}', 'Date', f_entete, F_ANTH, align=A_CENTRE, border=B_CASE)
ecrire(wp, f'K{l + 2}', 'Jour férié', f_entete, F_ANTH, align=A_CENTRE, border=B_CASE)
for i in range(40):
    ll = l + 3 + i
    if i < len(feries):
        ecrire(wp, f'J{ll}', feries[i][0], f_saisie, F_JAUNE, 'dd.mm.yyyy', border=B_CASE)
        ecrire(wp, f'K{ll}', feries[i][1], border=B_CASE)
    else:
        ecrire(wp, f'J{ll}', None, f_saisie, F_JAUNE, 'dd.mm.yyyy', border=B_CASE)
        ecrire(wp, f'K{ll}', None, border=B_CASE)
nom('Feries', f"{PQ}$J${l + 3}:$J${l + 42}")

# Colonne N-P : table NPA → zone
seg = segments_npa()
l, d0, d1 = table(14, 4, 'NPA → zone (d\'après site/api/data/zones.json)', ['NPA de', 'NPA à', 'Zone'],
                  [tuple(s_) for s_ in seg], 'T_NPA',
                  note='Plages tirées de la structure des NPA de La Poste. Corrigez ici une commune mal classée.',
                  saisie_cols=(2,))
for col, w in {'A': 46, 'B': 12, 'C': 16, 'D': 18, 'E': 3, 'F': 52, 'G': 14, 'H': 30, 'I': 3, 'J': 30, 'K': 30,
               'L': 3, 'M': 3, 'N': 12, 'O': 12, 'P': 22}.items():
    wp.column_dimensions[col].width = w

# =============================================================================================
# Demandes
# =============================================================================================
wd = wb.create_sheet('Demandes', 0)
COLS = []   # (clé, entête, largeur, type, aide)
def col(cle, entete, largeur, type_='saisie', aide=None, fmt=None, liste=None, groupe=None):
    COLS.append(dict(cle=cle, entete=entete, largeur=largeur, type=type_, aide=aide, fmt=fmt, liste=liste, groupe=groupe))

col('ref', 'Réf.', 13, aide='Référence libre (par ex. AC-2026-0001, ou la référence envoyée par le site). Les lignes « EXEMPLE » sont à supprimer.', groupe='DEMANDE')
col('date', 'Reçue le', 11, fmt='dd.mm.yyyy', aide='Date de réception. Indispensable : c\'est elle qui active les calculs de la ligne.')
col('nom', 'Nom et prénom', 22)
col('tel', 'Téléphone', 15)
col('email', 'E-mail', 24)
col('canal', 'Canal', 25, liste='L_Canal', aide='Par où la demande est arrivée (formulaire du site, demande de rappel, appel, e-mail…).')
col('source', 'Source', 28, liste='L_Source', aide='Comment nous a-t-on connus ? (champ « Comment nous avez-vous connus ? » du formulaire, ou UTM).')
col('type', 'Type de client', 36, liste='L_Type', groupe='PROJET (sert au score)')
col('service', 'Service', 30, liste='L_Service')
col('commune', 'Commune', 16)
col('npa', 'NPA', 7, fmt='0', aide='4 chiffres. Sert à calculer la zone (indispensable dans le canton de Vaud).')
col('canton', 'Canton', 11, liste='L_Canton')
col('surface', 'Surface', 36, liste='L_Surface')
col('delai', 'Délai souhaité', 31, liste='L_Delai')
col('fichier', 'Photo ou plan joint (O/N)', 9, liste='L_ON')
col('message', 'Message du client', 34, aide='Texte du formulaire ou résumé de l\'appel. Les mots « dégât », « fuite », « état des lieux », « fin de bail » rendent une demande urgente.')
col('zone', 'Zone (calculé)', 11, 'calc', 'Depuis le NPA (table de l\'onglet Paramètres), sinon depuis le canton.', groupe='SCORE')
col('score', 'Score (calculé)', 9, 'calc', 'Grille de la stratégie §2.3, poids dans Paramètres. Le score ordonne les rappels : toutes les demandes sont rappelées.', fmt='0')
col('prio', 'Priorité (calculé)', 10, 'calc', 'A ≥ 65, B ≥ 40, sinon C ; règles du §2.5 (régie, commune, architecte jamais sous B ; urgence → A ; hors zone ou hors service → hors cible).')
col('statut', 'Statut', 21, liste='L_Statut', groupe='SUIVI')
col('suivi', 'Suivi par', 12)
col('contact', 'Premier contact le', 11, fmt='dd.mm.yyyy', aide='Date du premier échange réel (appel abouti, réponse écrite).')
col('delai_rappel', 'Délai de rappel (j. ouvr., calculé)', 10, 'calc', '0 = rappelé le jour même.', fmt='0')
col('dans_delai', 'Rappel dans le délai (calculé)', 10, 'calc', 'Délai maximal par priorité : onglet Paramètres.')
col('visite', 'Visite le', 11, fmt='dd.mm.yyyy')
col('offre', 'Offre envoyée le', 11, fmt='dd.mm.yyyy')
col('montant', 'Montant offre (CHF, HT)', 12, fmt='#,##0')
col('relance', 'Prochaine relance le', 11, fmt='dd.mm.yyyy', aide='Facultatif : date convenue avec le client. Sinon, le fichier propose J+3, J+10, J+21.')
col('signe', 'Signé (O/N, calculé)', 9, 'calc', 'O si le statut est « Gagnée », N si « Perdue ».', groupe='RÉSULTAT')
col('signe_le', 'Signé le', 11, fmt='dd.mm.yyyy', aide='Date de signature : sert au chiffre d\'affaires signé du mois.')
col('motif', 'Motif de perte', 16, liste='L_Motif')
col('termine', 'Chantier terminé le', 11, fmt='dd.mm.yyyy', groupe='AVIS')
col('avis_dem', 'Avis demandé le', 11, fmt='dd.mm.yyyy')
col('avis_recu', 'Avis reçu (O/N)', 9, liste='L_ON')
col('echeance', 'Échéance (calculé)', 11, 'calc', 'Prochaine date à tenir selon le statut.', fmt='dd.mm.yyyy', groupe='À FAIRE')
col('alerte', 'À faire (calculé)', 30, 'calc', 'Filtrez cette colonne chaque matin : retards et informations manquantes.')
col('notes', 'Notes internes', 30)
col('groupe', 'Groupe de source (calculé)', 18, 'calc', 'Regroupement des sources pour l\'onglet KPI mensuels.')

C = {c['cle']: get_column_letter(i + 1) for i, c in enumerate(COLS)}
DQ = "Demandes!"
NCOL = len(COLS)
DERN = get_column_letter(NCOL)

titre(wd, 'Demandes', None, NCOL)
ecrire(wd, 'A2', 'Une ligne par demande (site, téléphone, e-mail, recommandation). Cellules blanches : à saisir. '
       'Cellules grises : calculées, ne pas modifier. Lignes jaunes « EXEMPLE » : à supprimer avant usage. '
       'Mode d\'emploi dans l\'onglet du même nom.', f_sous)
wd.merge_cells(f'A2:{get_column_letter(14)}2')

# Groupes (ligne 3) et entêtes (ligne 4)
groupes = [(i, c['groupe']) for i, c in enumerate(COLS) if c['groupe']] + [(NCOL, None)]
for (i, g), (j, _) in zip(groupes, groupes[1:]):
    a, b = get_column_letter(i + 1), get_column_letter(j)
    ecrire(wd, f'{a}3', g, Font(name=POLICE, size=9, bold=True, color=GRAPH), align=Alignment(vertical='bottom'))
    for k in range(i + 1, j + 1):
        wd.cell(3, k).border = Border(bottom=Side(style='medium', color=ROUGE if g == 'À FAIRE' else ANTH))
for i, c in enumerate(COLS):
    cell = ecrire(wd, f'{get_column_letter(i + 1)}4', c['entete'], f_entete, F_GRAPH if c['type'] == 'calc' else F_ANTH,
                  align=A_CENTRE, border=B_CASE)
    if c['aide']:
        cell.comment = Comment(c['aide'], 'Andy Construct')
        cell.comment.width, cell.comment.height = 260, 110
    wd.column_dimensions[get_column_letter(i + 1)].width = c['largeur']
wd.row_dimensions[4].height = 54


def formules(n):
    L = {k: f'${v}{n}' for k, v in C.items()}
    tel_bonus = (f'IF(AND({L["tel"]}<>"",IFERROR(VLOOKUP({L["canal"]},T_Canal,2,FALSE),"N")="O"),P_BonusTel,0)')
    zone = (f'=IF({L["date"]}="","",IF(AND(ISNUMBER({L["npa"]}),{L["npa"]}>=1000,{L["npa"]}<=9999),'
            f'VLOOKUP({L["npa"]},T_NPA,3,TRUE),IF({L["canton"]}="","Inconnue",'
            f'IFERROR(VLOOKUP({L["canton"]},T_Canton,2,FALSE),"Inconnue"))))')
    pts_zone = (f'IF(AND({L["zone"]}="3",OR(IFERROR(VLOOKUP({L["type"]},T_Type,4,FALSE),"N")="O",'
                f'IFERROR(VLOOKUP({L["surface"]},T_Surface,3,FALSE),"N")="O")),VLOOKUP("2",T_Zone,2,FALSE),'
                f'IFERROR(VLOOKUP({L["zone"]},T_Zone,2,FALSE),VLOOKUP("Inconnue",T_Zone,2,FALSE)))')
    score = (f'=IF({L["date"]}="","",IFERROR(VLOOKUP({L["type"]},T_Type,2,FALSE),P_TypeDefaut)'
             f'+IFERROR(VLOOKUP({L["service"]},T_Service,2,FALSE),P_ServiceDefaut)'
             f'+IFERROR(VLOOKUP({L["surface"]},T_Surface,2,FALSE),P_SurfaceDefaut)'
             f'+{pts_zone}'
             f'+IFERROR(VLOOKUP({L["delai"]},T_Delai,2,FALSE),P_DelaiDefaut)'
             f'+IFERROR(VLOOKUP({L["source"]},T_Source,2,FALSE),P_SourceDefaut)'
             f'+IF({L["fichier"]}="O",P_BonusFichier,0)+{tel_bonus}'
             f'+IF(AND(TRIM({L["message"]})="",{L["tel"]}=""),P_Malus,0))')
    hors = (f'OR(IFERROR(VLOOKUP({L["service"]},T_Service,3,FALSE),"N")="O",'
            f'IFERROR(VLOOKUP({L["zone"]},T_Zone,3,FALSE),"N")="O")')
    urgent = (f'AND(IFERROR(VLOOKUP({L["delai"]},T_Delai,3,FALSE),"N")="O",'
              f'SUMPRODUCT((T_Urgence<>"")*ISNUMBER(SEARCH(T_Urgence,{L["message"]})))>0)')
    plancher = (f'OR(IFERROR(VLOOKUP({L["type"]},T_Type,3,FALSE),"N")="O",'
                f'IFERROR(VLOOKUP({L["canal"]},T_Canal,3,FALSE),"N")="O")')
    base = f'IF({L["score"]}>=P_SeuilA,"A",IF({L["score"]}>=P_SeuilB,"B","C"))'
    prio = (f'=IF({L["date"]}="","",IF({hors},"Hors cible",IF(OR({base}="A",{urgent}),"A",'
            f'IF(AND({base}="C",{plancher}),"B",{base}))))')
    delai_max = f'IFERROR(VLOOKUP({L["prio"]},T_DelaiContact,2,FALSE),2)'
    delai_rappel = f'=IF(OR({L["date"]}="",{L["contact"]}=""),"",NETWORKDAYS({L["date"]},{L["contact"]},Feries)-1)'
    dans_delai = f'=IF({L["delai_rappel"]}="","",IF({L["delai_rappel"]}<={delai_max},"Oui","Non"))'
    signe = f'=IF({L["statut"]}="Gagnée","O",IF({L["statut"]}="Perdue","N",""))'
    st = L['statut']
    rel_auto = (f'IF(TODAY()<={L["offre"]}+P_Relance2,{L["offre"]}+P_Relance2,'
                f'IF(TODAY()<={L["offre"]}+P_Relance3,{L["offre"]}+P_Relance3,{L["offre"]}+P_Clore))')
    echeance = (f'=IF(OR({L["date"]}="",{st}=""),"",'
                f'IF({st}="1 Nouvelle demande",WORKDAY({L["date"]},{delai_max},Feries),'
                f'IF({st}="2 Contact établi",IF({L["visite"]}<>"",{L["visite"]},'
                f'WORKDAY(IF({L["contact"]}<>"",{L["contact"]},{L["date"]}),P_DelaiVisite,Feries)),'
                f'IF({st}="3 Visite planifiée",IF({L["visite"]}="","",IF({L["visite"]}>=TODAY(),{L["visite"]},'
                f'WORKDAY({L["visite"]},P_DelaiOffre,Feries))),'
                f'IF({st}="4 Offre envoyée",IF({L["relance"]}<>"",{L["relance"]},IF({L["offre"]}="","",{L["offre"]}+P_Relance1)),'
                f'IF({st}="5 Relance / négociation",IF({L["relance"]}<>"",{L["relance"]},IF({L["offre"]}="","",{rel_auto})),'
                f'IF({st}="Gagnée",IF(AND({L["termine"]}<>"",{L["avis_dem"]}=""),{L["termine"]}+P_Avis,""),"")))))))')
    ech = L['echeance']
    retard = (f'IF({ech}="","",IF({st}="Gagnée",IF({ech}<=TODAY(),"Demander l\'avis du client",""),'
              f'IF({ech}>=TODAY(),"",'
              f'IF({st}="1 Nouvelle demande","Premier contact en retard",'
              f'IF({st}="2 Contact établi","Visite à fixer",'
              f'IF({st}="3 Visite planifiée","Offre à envoyer",'
              f'IF({st}="4 Offre envoyée","Relancer l\'offre",'
              f'IF(TODAY()>{L["offre"]}+P_Clore,"Sans réponse : clore l\'offre ?","Relancer l\'offre"))))))))')
    alerte = (f'=IF({L["date"]}="","",'
              f'IF({st}="","Indiquer le statut",'
              f'IF(AND({st}="1 Nouvelle demande",{L["contact"]}<>""),"Mettre à jour le statut",'
              f'IF(AND({st}="Gagnée",{L["signe_le"]}=""),"Indiquer la date de signature",'
              f'IF(AND({st}="Gagnée",{L["montant"]}=""),"Indiquer le montant",'
              f'IF(AND({st}="Perdue",{L["motif"]}=""),"Indiquer le motif de perte",'
              f'IF(AND(OR({st}="4 Offre envoyée",{st}="5 Relance / négociation"),{L["offre"]}=""),"Indiquer la date de l\'offre",'
              f'IF(AND({st}="3 Visite planifiée",{L["visite"]}=""),"Indiquer la date de visite",'
              f'{retard}))))))))')
    groupe = (f'=IF({L["date"]}="","",IFERROR(VLOOKUP({L["source"]},T_Source,3,FALSE),"Autres et inconnue"))')
    return dict(zone=zone, score=score, prio=prio, delai_rappel=delai_rappel, dans_delai=dans_delai,
                signe=signe, echeance=echeance, alerte=alerte, groupe=groupe)


EXEMPLES = [
    dict(ref='EXEMPLE 1', date=dt.date(2026, 11, 2), nom='Mme Exemple (propriétaire)', tel='079 000 00 01',
         email='exemple1@exemple.ch', canal='Site : demande de devis', source='Recherche Google',
         type='Propriétaire (maison, appartement, PPE)', service='Isolation acoustique', commune='Vésenaz', npa=1222,
         canton='GE', surface='15 à 50 m² (une ou deux pièces)', delai='Dans 1 à 3 mois', fichier='N',
         message='Voix et télévision du voisin dans la chambre.', statut='Gagnée', suivi='Associé terrain',
         contact=dt.date(2026, 11, 2), visite=dt.date(2026, 11, 5), offre=dt.date(2026, 11, 10), montant=6800,
         signe_le=dt.date(2026, 11, 18), termine=dt.date(2026, 12, 4), avis_dem=dt.date(2026, 12, 7), avis_recu='O',
         notes='Exemple : chantier signé, avis reçu.'),
    dict(ref='EXEMPLE 2', date=dt.date(2026, 11, 3), nom='Régie Exemple SA', tel='022 000 00 02',
         email='exemple2@exemple.ch', canal='Téléphone', source='Appel direct',
         type='Régie, gérance ou coopérative', service='Peinture', commune='Genève', npa=1205, canton='GE',
         surface='Plus de 200 m², ou plusieurs logements', delai='Dès que possible (moins d\'un mois)', fichier='N',
         message='Cage d\'escalier de 6 étages, immeuble habité.', statut='4 Offre envoyée', suivi='Associé bureau',
         contact=dt.date(2026, 11, 3), visite=dt.date(2026, 11, 6), offre=dt.date(2026, 11, 11), montant=14500,
         notes='Exemple : offre en attente de réponse.'),
    dict(ref='EXEMPLE 3', date=dt.date(2026, 11, 5), nom='Bureau d\'architecture Exemple', tel='032 000 00 03',
         email='exemple3@exemple.ch', canal='E-mail', source='LinkedIn',
         type='Architecte, bureau d\'études ou entreprise générale', service='Placo', commune='Neuchâtel', npa=2000,
         canton='NE', surface='Plus de 200 m², ou plusieurs logements', delai='Dans 3 à 6 mois', fichier='O',
         message='Cloisons et faux-plafonds, lot CFC 271, remise des offres le 4 décembre.', statut='3 Visite planifiée',
         suivi='Associé bureau', contact=dt.date(2026, 11, 6), visite=dt.date(2026, 11, 13),
         notes='Exemple : zone 3 sans pénalité (règle 3).'),
    dict(ref='EXEMPLE 4', date=dt.date(2026, 11, 9), nom='M. Exemple (propriétaire)', tel='026 000 00 04',
         email='exemple4@exemple.ch', canal='Site : demande de devis', source='Recherche Google',
         type='Propriétaire (maison, appartement, PPE)', service='Peinture', commune='Fribourg', npa=1700, canton='FR',
         surface='15 à 50 m² (une ou deux pièces)', delai='Dans 1 à 3 mois', fichier='N',
         message='Repeindre deux pièces.', statut='Perdue', suivi='Associé terrain', contact=dt.date(2026, 11, 10),
         visite=dt.date(2026, 11, 13), offre=dt.date(2026, 11, 17), montant=3900, motif='Prix',
         notes='Exemple : offre perdue, motif renseigné.'),
    dict(ref='EXEMPLE 5', date=dt.date(2026, 11, 13), nom='Mme Exemple (locataire)', tel=None,
         email='exemple5@exemple.ch', canal='Site : demande de devis', source='Facebook ou Instagram (Meta)',
         type='Locataire', service='Peinture', commune='Lausanne', npa=1004, canton='VD',
         surface='15 à 50 m² (une ou deux pièces)', delai='Pas encore défini', fichier='N',
         message='Repeindre la chambre avant mon départ.', statut='1 Nouvelle demande',
         notes='Exemple : à rappeler (priorité C).'),
]

for i in range(N_LIGNES):
    n = L0 + i
    fx = formules(n)
    ex = EXEMPLES[i] if i < len(EXEMPLES) else {}
    for j, c in enumerate(COLS):
        cell = wd.cell(n, j + 1)
        cell.border = B_CASE
        cell.font = f_base
        centre = c['cle'] in ('zone', 'score', 'prio', 'delai_rappel', 'dans_delai', 'signe', 'fichier', 'avis_recu', 'canton')
        cell.alignment = Alignment(vertical='top', horizontal='center' if centre else None,
                                   wrap_text=c['cle'] in ('message', 'notes', 'alerte', 'nom'))
        if c['fmt']:
            cell.number_format = c['fmt']
        if c['type'] == 'calc':
            cell.value = fx[c['cle']]
            cell.fill = F_BRUME
        elif c['cle'] in ex and ex[c['cle']] is not None:
            cell.value = ex[c['cle']]
            cell.font = Font(name=POLICE, size=10, italic=True, color=ANTH)

# Validations de données
def valider(cle, dv):
    dv.add(f'{C[cle]}{L0}:{C[cle]}{L0 + N_LIGNES - 1}')
    wd.add_data_validation(dv)

for c in COLS:
    if c['liste']:
        dv = DataValidation(type='list', formula1=c['liste'], allow_blank=True, showErrorMessage=True,
                            errorTitle='Valeur non prévue', error='Choisissez une valeur dans la liste (onglet Paramètres).',
                            showDropDown=False)
        valider(c['cle'], dv)
    elif c['fmt'] == 'dd.mm.yyyy' and c['type'] == 'saisie':
        dv = DataValidation(type='date', operator='between', formula1='DATE(2020,1,1)', formula2='DATE(2040,12,31)',
                            allow_blank=True, showErrorMessage=True, errorTitle='Date attendue',
                            error='Saisissez une date, par exemple 15.03.2027.')
        valider(c['cle'], dv)
valider('npa', DataValidation(type='whole', operator='between', formula1='1000', formula2='9999', allow_blank=True,
                              showErrorMessage=True, errorTitle='NPA', error='Le NPA compte 4 chiffres, par exemple 1227.'))
valider('montant', DataValidation(type='decimal', operator='greaterThanOrEqual', formula1='0', allow_blank=True,
                                  showErrorMessage=True, errorTitle='Montant', error='Montant en CHF, sans texte.'))

# Mise en forme conditionnelle
plage = f'A{L0}:{DERN}{L0 + N_LIGNES - 1}'
A_ = C['alerte']
wd.conditional_formatting.add(plage, FormulaRule(formula=[f'LEFT($A{L0},7)="EXEMPLE"'], fill=F_EXEMPLE, stopIfTrue=False))
wd.conditional_formatting.add(plage, FormulaRule(
    formula=[f'OR(${A_}{L0}="Premier contact en retard",${A_}{L0}="Relancer l\'offre",${A_}{L0}="Offre à envoyer",${A_}{L0}="Visite à fixer")'],
    fill=fill('FDECEC')))
wd.conditional_formatting.add(f'{A_}{L0}:{A_}{L0 + N_LIGNES - 1}', FormulaRule(
    formula=[f'LEN(${A_}{L0})>0'], fill=fill('F9D2D4'), font=Font(name=POLICE, bold=True, color=ROUGE_F)))
E_ = C['echeance']
wd.conditional_formatting.add(f'{E_}{L0}:{E_}{L0 + N_LIGNES - 1}', FormulaRule(
    formula=[f'AND(ISNUMBER(${E_}{L0}),${E_}{L0}<TODAY(),LEN(${A_}{L0})>0)'], font=Font(name=POLICE, bold=True, color=ROUGE_F)))
P_ = C['prio']
wd.conditional_formatting.add(f'{P_}{L0}:{P_}{L0 + N_LIGNES - 1}', FormulaRule(
    formula=[f'${P_}{L0}="A"'], fill=F_ANTH, font=Font(name=POLICE, bold=True, color='FFFFFF')))
wd.conditional_formatting.add(f'{P_}{L0}:{P_}{L0 + N_LIGNES - 1}', FormulaRule(
    formula=[f'${P_}{L0}="B"'], fill=fill('D4D6D9'), font=Font(name=POLICE, bold=True, color=ANTH)))
wd.conditional_formatting.add(f'{P_}{L0}:{P_}{L0 + N_LIGNES - 1}', FormulaRule(
    formula=[f'${P_}{L0}="Hors cible"'], font=Font(name=POLICE, italic=True, color=GRAPH)))

wd.freeze_panes = f'D{L0}'
wd.auto_filter.ref = f'A4:{DERN}{L0 + N_LIGNES - 1}'
wd.page_setup.orientation = 'landscape'
wd.page_setup.fitToWidth = 1
wd.page_setup.fitToHeight = 0
wd.sheet_properties.pageSetUpPr.fitToPage = True
wd.print_title_rows = '3:4'

# Plages nommées sur les colonnes de « Demandes » (lues par les synthèses)
for cle, nom_ in [('date', 'D_Date'), ('source', 'D_Source'), ('type', 'D_Type'), ('service', 'D_Service'),
                  ('prio', 'D_Prio'), ('statut', 'D_Statut'), ('contact', 'D_Contact'), ('delai_rappel', 'D_Delai'),
                  ('dans_delai', 'D_DansDelai'), ('visite', 'D_Visite'), ('offre', 'D_Offre'), ('montant', 'D_Montant'),
                  ('signe', 'D_Signe'), ('signe_le', 'D_SigneLe'), ('motif', 'D_Motif'), ('avis_dem', 'D_AvisDem'),
                  ('avis_recu', 'D_AvisRecu'), ('alerte', 'D_Alerte'), ('groupe', 'D_Groupe'), ('ref', 'D_Ref')]:
    nom(nom_, f'{DQ}${C[cle]}${L0}:${C[cle]}${LMAX}')

# =============================================================================================
# Objectifs
# =============================================================================================
wo = wb.create_sheet('Objectifs')
titre(wo, 'Objectifs', 'Stratégie d\'acquisition §1.1 (scénario M, de référence). Cellules jaunes modifiables. '
      'Aucune base mesurée n\'existe : objectifs à recaler au 3e mois sur les données réelles (§0, §1.2).', 7)
ecrire(wo, 'A4', 'Mois de mise en ligne du site v2 (M1)', f_gras)
ecrire(wo, 'C4', dt.date(2026, 11, 1), f_saisie, F_JAUNE, 'mmmm yyyy', border=B_CASE)
ecrire(wo, 'D4', 'Date provisoire : indiquez le mois réel de mise en ligne (il fixe M1 dans l\'onglet KPI mensuels).', f_sous)
nom('O_M1', "Objectifs!$C$4")

ent = ['Indicateur', 'Définition et outil de mesure', 'M3', 'M6', 'M12', 'Unité', 'Remarque']
for j, e in enumerate(ent):
    ecrire(wo, f'{get_column_letter(j + 1)}6', e, f_entete, F_ANTH, align=A_CENTRE, border=B_CASE)
OBJ = [  # clé, indicateur, définition, M3, M6, M12, unité, remarque
    ('visites', 'Visites du site par mois', 'Umami (sessions)', 500, 900, 1500, 'nombre', ''),
    ('contacts', 'Contacts web par mois', 'Formulaires envoyés + clics tél., e-mail et WhatsApp (Umami)', 10, 22, 45, 'nombre', ''),
    ('taux_web', 'Taux visite → contact web', 'Contacts web / visites', 0.02, 0.025, 0.03, '%', ''),
    ('demandes', 'Demandes enregistrées par mois', 'Tous canaux : site, téléphone, e-mail, recommandation, B2B (hors appels d\'offres)', 10, 18, 30, 'nombre', ''),
    ('ab', 'dont priorité A ou B', 'Scoring §2', 0.5, 0.6, 0.65, '% au moins', ''),
    ('delai_a', 'Délai de premier contact, demandes A', 'Médiane CRM', '< 4 h ouvr.', '< 2 h ouvr.', '< 2 h ouvr.', 'texte', 'Ce fichier compte en jours ; objectif suivi dans le CRM'),
    ('dem_offre', 'Taux demande → offre', 'Offres envoyées / demandes du mois précédent', 0.55, 0.6, 0.65, '%', ''),
    ('offre_signee', 'Taux offre → signée', 'Cohorte des offres envoyées depuis plus de 60 jours', 0.25, 0.28, 0.3, '%', ''),
    ('signes', 'Chantiers signés par mois issus de l\'acquisition', 'Calcul des lignes précédentes', 1.5, 3, 6, 'nombre', 'M3 : « ≈ 1 à 2 » dans la stratégie'),
    ('avis', 'Avis Google (cumul)', 'Fiche Google', 15, 30, 50, 'nombre', ''),
    ('note', 'Note moyenne Google', 'Suivie, jamais « pilotée » (pas de sélection des clients)', 'suivie', 'suivie', 'suivie', 'texte', ''),
    ('b2b', 'Comptes B2B contactés (cumul)', 'Séquence (j)', 30, 90, 200, 'nombre', ''),
    ('ao', 'Appels d\'offres étudiés / déposés (cumul)', 'Veille (g)', '8 / 1', '18 / 4', '35 / 8', 'texte', ''),
    ('ia', 'Citations dans les IA', 'Test mensuel de 10 questions', '1/10', '3/10', '5/10', 'texte', ''),
]
OBJ_LIGNE = {}
for i, (k, ind, de, m3, m6, m12, u, rq) in enumerate(OBJ):
    n = 7 + i
    OBJ_LIGNE[k] = n
    ecrire(wo, f'A{n}', ind, f_gras if k in ('demandes', 'dem_offre', 'offre_signee', 'avis', 'taux_web') else f_base, border=B_CASE, align=A_WRAP)
    ecrire(wo, f'B{n}', de, f_sous, border=B_CASE, align=A_WRAP)
    for j, v in enumerate((m3, m6, m12)):
        fmt = '0.0%' if u.startswith('%') else ('0.0' if isinstance(v, float) and v % 1 else '#,##0')
        ecrire(wo, f'{"CDE"[j]}{n}', v, f_saisie, F_JAUNE, None if isinstance(v, str) else fmt, A_CENTRE, B_CASE)
    ecrire(wo, f'F{n}', u, f_sous, border=B_CASE)
    ecrire(wo, f'G{n}', rq, f_sous, border=B_CASE, align=A_WRAP)
fin = 7 + len(OBJ)
ecrire(wo, f'A{fin + 1}', 'Source : docs/v2/strategie-acquisition.md, §1.1. Les lignes en gras sont comparées aux résultats '
       'dans l\'onglet KPI mensuels (mois 1 à 3 : objectif M3 ; 4 à 6 : M6 ; 7 à 12 : M12).', f_sous)

l = fin + 3
ecrire(wo, f'A{l}', 'Variation selon le scénario budgétaire, à M12 (stratégie §1.1 et §8.3)', f_section)
for j, e in enumerate(['Scénario', 'Demandes par mois', 'Chantiers signés par mois', 'Avis (cumul)', 'Budget annuel (médias, outils, supports)']):
    ecrire(wo, f'{get_column_letter(j + 1)}{l + 1}', e, f_entete, F_ANTH, align=A_CENTRE, border=B_CASE)
for i, lg in enumerate([('S « Fondations »', '≈ 18', '≈ 3 à 4', 45, 'CHF 5\'900 environ'),
                        ('M « Croissance »', '≈ 30', '≈ 6', 50, 'CHF 18\'300 environ'),
                        ('L « Accélération romande »', '≈ 45', '≈ 9', 60, 'CHF 42\'300 environ')]):
    for j, v in enumerate(lg):
        ecrire(wo, f'{get_column_letter(j + 1)}{l + 2 + i}', v, border=B_CASE, align=A_CENTRE if j else None)
ecrire(wo, f'A{l + 6}', 'Ce fichier est l\'outil de démarrage du scénario S (avant le CRM). Si vous retenez S, remplacez '
       'les valeurs M12 du tableau ci-dessus par celles de la ligne S (≈ 18 demandes, 3 à 4 chantiers signés, 45 avis), '
       'et ajustez M3 et M6 si nécessaire.', f_sous)
for col_, w in {'A': 44, 'B': 50, 'C': 14, 'D': 14, 'E': 14, 'F': 26, 'G': 40}.items():
    wo.column_dimensions[col_].width = w

# =============================================================================================
# KPI mensuels
# =============================================================================================
wk = wb.create_sheet('KPI mensuels')
titre(wk, 'KPI mensuels', 'Tout est calculé depuis l\'onglet Demandes (formules). Cellules jaunes : relevés à saisir '
      'chaque mois (Umami, fiche Google). Les lignes EXEMPLE sont comptées tant qu\'elles ne sont pas supprimées.', 30)
K = []  # (entête, largeur, formule(n), format, saisie)
POS = {}  # entête unique → lettre de colonne (rempli une fois K complet)


def L_(entete):
    return POS[entete]


def k(entete, largeur, f, fmt='0', saisie=False, objectif=False):
    K.append(dict(entete=entete, largeur=largeur, f=f, fmt=fmt, saisie=saisie, objectif=objectif))


deb = lambda n: f'$A{n}'
fin_m = lambda n: f'EOMONTH($A{n},0)'
dans_mois = lambda plage, n: f'{plage},">="&{deb(n)},{plage},"<="&{fin_m(n)}'
obj = lambda cle, n: (f'INDEX(Objectifs!$C${OBJ_LIGNE[cle]}:$E${OBJ_LIGNE[cle]},'
                      f'IF($B{n}<=3,1,IF($B{n}<=6,2,3)))')

k('Mois', 13, lambda n: '=DATE(YEAR(O_M1),MONTH(O_M1),1)' if n == 6 else f'=EDATE($A{n - 1},1)', 'mmm yyyy')
k('Mois depuis la mise en ligne', 9, lambda n: f'=ROWS($A$6:$A{n})', '"M"0')
k('Visites du site (Umami)', 10, None, '#,##0', saisie=True)
k('Contacts web (Umami)', 10, None, '#,##0', saisie=True)
k('Taux visite → contact', 9, lambda n: f'=IF(OR($C{n}="",$C{n}=0,$D{n}=""),"",$D{n}/$C{n})', '0.0%')
k('Objectif', 9, lambda n: f'={obj("taux_web", n)}', '0.0%', objectif=True)
k('Demandes reçues', 10, lambda n: f'=COUNTIFS({dans_mois("D_Date", n)})', '0')
k('Objectif', 9, lambda n: f'={obj("demandes", n)}', '0', objectif=True)
for g in GROUPES:
    k(f'dont {g}', 11, lambda n, g=g: f'=COUNTIFS({dans_mois("D_Date", n)},D_Groupe,"{g}")', '0')
k('Part A ou B', 9, lambda n: (f'=IF($G{n}=0,"",(COUNTIFS({dans_mois("D_Date", n)},D_Prio,"A")'
                               f'+COUNTIFS({dans_mois("D_Date", n)},D_Prio,"B"))/$G{n})'), '0%')
k('Objectif', 9, lambda n: f'={obj("ab", n)}', '0%', objectif=True)
k('Délai moyen de premier contact (j. ouvr.)', 11,
  lambda n: f'=IFERROR(AVERAGEIFS(D_Delai,{dans_mois("D_Date", n)}),"")', '0.0')
k('Rappelées dans le délai', 10,
  lambda n: (f'=IFERROR(COUNTIFS({dans_mois("D_Date", n)},D_DansDelai,"Oui")/(COUNTIFS({dans_mois("D_Date", n)},D_DansDelai,"Oui")'
             f'+COUNTIFS({dans_mois("D_Date", n)},D_DansDelai,"Non")),"")'), '0%')
k('Offres envoyées', 9, lambda n: f'=COUNTIFS({dans_mois("D_Offre", n)})', '0')
k('Taux demande → offre', 10,
  lambda n: (f'=IFERROR(${L_("Offres envoyées")}{n}/COUNTIFS(D_Date,">="&EDATE($A{n},-1),D_Date,"<="&EOMONTH($A{n},-1)),"")'), '0%')
k('Objectif', 9, lambda n: f'={obj("dem_offre", n)}', '0%', objectif=True)
k('Chantiers signés', 9, lambda n: f'=COUNTIFS({dans_mois("D_SigneLe", n)},D_Signe,"O")', '0')
k('Objectif', 9, lambda n: f'={obj("signes", n)}', '0.0', objectif=True)
k('CA signé (CHF, HT)', 12, lambda n: f'=SUMIFS(D_Montant,{dans_mois("D_SigneLe", n)},D_Signe,"O")', '#,##0')
k('Taux offre → signée (offres du mois, à lire après 60 jours)', 12,
  lambda n: f'=IF(${L_("Offres envoyées")}{n}=0,"",COUNTIFS({dans_mois("D_Offre", n)},D_Signe,"O")/${L_("Offres envoyées")}{n})', '0%')
k('Objectif', 9, lambda n: f'={obj("offre_signee", n)}', '0%', objectif=True)
k('Avis demandés', 9, lambda n: f'=COUNTIFS({dans_mois("D_AvisDem", n)})', '0')
k('dont avis reçus', 9, lambda n: f'=COUNTIFS({dans_mois("D_AvisDem", n)},D_AvisRecu,"O")', '0')
k('Avis Google, total relevé sur la fiche', 11, None, '0', saisie=True)
k('Objectif (cumul)', 9, lambda n: f'={obj("avis", n)}', '0', objectif=True)

KL = {i: get_column_letter(i + 1) for i in range(len(K))}
for i, x in enumerate(K):
    POS.setdefault(x['entete'], KL[i])
# Les formules écrites en dur supposent ces positions : vérification
assert POS['Visites du site (Umami)'] == 'C' and POS['Contacts web (Umami)'] == 'D' and POS['Demandes reçues'] == 'G'

for i, x in enumerate(K):
    cl = KL[i]
    ecrire(wk, f'{cl}5', x['entete'], f_entete, F_GRAPH if x['objectif'] else F_ANTH, align=A_CENTRE, border=B_CASE)
    wk.column_dimensions[cl].width = x['largeur'] + 2
    for m in range(12):
        n = 6 + m
        if x['f']:
            ecrire(wk, f'{cl}{n}', x['f'](n), Font(name=POLICE, size=10, color=GRAPH if x['objectif'] else ANTH),
                   F_BRUME if x['objectif'] else None, x['fmt'], Alignment(horizontal='center'), B_CASE)
        else:
            ecrire(wk, f'{cl}{n}', None, f_saisie, F_JAUNE, x['fmt'], Alignment(horizontal='center'), B_CASE)
wk.row_dimensions[5].height = 66
# Ligne de total / moyenne sur 12 mois
nt = 18
ecrire(wk, f'A{nt}', '12 mois', f_gras, F_BRUME, border=B_CASE)
ecrire(wk, f'B{nt}', None, f_gras, F_BRUME, border=B_CASE)
p12 = f'D_Date,">="&$A$6,D_Date,"<="&EOMONTH($A$17,0)'
col_ = lambda e_: L_(e_)
som = lambda e_: f'=SUM({L_(e_)}6:{L_(e_)}17)'
totaux = {
    'Visites du site (Umami)': som('Visites du site (Umami)'), 'Contacts web (Umami)': som('Contacts web (Umami)'),
    'Taux visite → contact': '=IF(OR(SUM(C6:C17)=0,COUNT(D6:D17)=0),"",SUM(D6:D17)/SUM(C6:C17))',
    'Demandes reçues': som('Demandes reçues'),
    'Part A ou B': f'=IF($G{nt}=0,"",(COUNTIFS({p12},D_Prio,"A")+COUNTIFS({p12},D_Prio,"B"))/$G{nt})',
    'Délai moyen de premier contact (j. ouvr.)': f'=IFERROR(AVERAGEIFS(D_Delai,{p12}),"")',
    'Rappelées dans le délai': f'=IFERROR(COUNTIFS({p12},D_DansDelai,"Oui")/(COUNTIFS({p12},D_DansDelai,"Oui")+COUNTIFS({p12},D_DansDelai,"Non")),"")',
    'Offres envoyées': som('Offres envoyées'),
    'Taux demande → offre': f'=IF($G{nt}=0,"",${col_("Offres envoyées")}{nt}/$G{nt})',
    'Chantiers signés': som('Chantiers signés'), 'CA signé (CHF, HT)': som('CA signé (CHF, HT)'),
    'Taux offre → signée (offres du mois, à lire après 60 jours)':
        f'=IF(${col_("Offres envoyées")}{nt}=0,"",COUNTIFS(D_Offre,">="&$A$6,D_Offre,"<="&EOMONTH($A$17,0),D_Signe,"O")/${col_("Offres envoyées")}{nt})',
    'Avis demandés': som('Avis demandés'), 'dont avis reçus': som('dont avis reçus'),
    'Avis Google, total relevé sur la fiche': (f'=IF(COUNT({col_("Avis Google, total relevé sur la fiche")}6:{col_("Avis Google, total relevé sur la fiche")}17)=0,"",'
                                               f'MAX({col_("Avis Google, total relevé sur la fiche")}6:{col_("Avis Google, total relevé sur la fiche")}17))'),
}
for g in GROUPES:
    i = [j for j, x in enumerate(K) if x['entete'] == f'dont {g}'][0]
    totaux[f'dont {g}'] = f'=SUM({KL[i]}6:{KL[i]}17)'
for i, x in enumerate(K[2:], 2):
    f_ = totaux.get(x['entete'])
    ecrire(wk, f'{KL[i]}{nt}', f_, f_gras, F_BRUME, x['fmt'], Alignment(horizontal='center'), B_CASE)
ecrire(wk, 'A20', 'Lecture', f_section)
notes_kpi = [
    'Demandes : par date de réception. Offres : par date d\'envoi. Chantiers signés et CA : par date de signature (statut « Gagnée »).',
    'Taux demande → offre : offres envoyées dans le mois / demandes reçues le mois précédent (définition de la stratégie §1.1).',
    'Taux offre → signée : parmi les offres envoyées dans le mois, part signée à ce jour ; le chiffre n\'est fiable qu\'après 60 jours.',
    'Délai de premier contact : en jours ouvrables (0 = le jour même). L\'objectif en heures de la stratégie se suit dans le CRM.',
    'Objectif : mois 1 à 3, objectif M3 ; mois 4 à 6, M6 ; mois 7 à 12, M12 (onglet Objectifs, modifiable).',
    'Visites, contacts web et avis Google : relevés manuels (Umami, fiche Google), à saisir dans les cellules jaunes.',
]
for i, t in enumerate(notes_kpi):
    ecrire(wk, f'A{21 + i}', '• ' + t, f_sous)
wk.freeze_panes = 'C6'
wk.page_setup.orientation = 'landscape'
wk.sheet_properties.pageSetUpPr.fitToPage = True
wk.page_setup.fitToHeight = 0

# =============================================================================================
# Pipeline
# =============================================================================================
wpi = wb.create_sheet('Pipeline')
titre(wpi, 'Pipeline', 'Synthèse de l\'onglet Demandes, par statut (formules). Les lignes EXEMPLE sont comptées '
      'tant qu\'elles ne sont pas supprimées.', 9)
ecrire(wpi, 'A3', 'Situation au', f_gras)
ecrire(wpi, 'B3', '=TODAY()', f_base, fmt='dd.mm.yyyy')
ent = ['Statut', 'Demandes', 'dont A', 'dont B', 'dont C', 'dont hors cible', 'Montant des offres (CHF, HT)', 'À faire ou en retard']
for j, e in enumerate(ent):
    ecrire(wpi, f'{get_column_letter(j + 1)}5', e, f_entete, F_ANTH, align=A_CENTRE, border=B_CASE)
lignes_pi = STATUTS + ['Sans statut']
for i, s_ in enumerate(lignes_pi):
    n = 6 + i
    crit = f'(D_Statut="{s_}")' if s_ != 'Sans statut' else '(D_Statut="")*(D_Date<>"")'
    ecrire(wpi, f'A{n}', s_, f_gras, border=B_CASE)
    ecrire(wpi, f'B{n}', f'=SUMPRODUCT({crit}*1)', fmt='0', border=B_CASE, align=Alignment(horizontal='center'))
    for j, p_ in enumerate(['A', 'B', 'C', 'Hors cible']):
        ecrire(wpi, f'{"CDEF"[j]}{n}', f'=SUMPRODUCT({crit}*(D_Prio="{p_}"))', fmt='0', border=B_CASE,
               align=Alignment(horizontal='center'))
    ecrire(wpi, f'G{n}', f'=SUMPRODUCT({crit}*N(+D_Montant))' if False else f'=SUMPRODUCT({crit}*ISNUMBER(D_Montant),D_Montant)',
           fmt='#,##0', border=B_CASE, align=Alignment(horizontal='center'))
    ecrire(wpi, f'H{n}', f'=SUMPRODUCT({crit}*(LEN(D_Alerte)>0))', fmt='0', border=B_CASE, align=Alignment(horizontal='center'))
nt = 6 + len(lignes_pi)
ecrire(wpi, f'A{nt}', 'Total', f_gras, F_BRUME, border=B_CASE)
for cl in 'BCDEFGH':
    ecrire(wpi, f'{cl}{nt}', f'=SUM({cl}6:{cl}{nt - 1})', f_gras, F_BRUME, '#,##0' if cl == 'G' else '0',
           Alignment(horizontal='center'), B_CASE)
ecrire(wpi, f'A{nt + 1}', 'En cours (statuts 1 à 5)', f_base, border=B_CASE)
ecrire(wpi, f'B{nt + 1}', '=SUM(B6:B10)', fmt='0', border=B_CASE, align=Alignment(horizontal='center'))
ecrire(wpi, f'G{nt + 1}', '=SUM(G9:G10)', fmt='#,##0', border=B_CASE, align=Alignment(horizontal='center'))
ecrire(wpi, f'H{nt + 1}', 'Montant : offres envoyées et en relance', f_sous)

l = nt + 4
ecrire(wpi, f'A{l}', 'Entonnoir (toutes les demandes du fichier)', f_section)
for j, e in enumerate(['Étape', 'Nombre', '% de l\'étape précédente', '% des demandes']):
    ecrire(wpi, f'{get_column_letter(j + 1)}{l + 1}', e, f_entete, F_ANTH, align=A_CENTRE, border=B_CASE)
etapes = [('Demandes reçues', '=SUMPRODUCT((D_Date<>"")*1)'),
          ('Contact établi', '=SUMPRODUCT((D_Date<>"")*ISNUMBER(D_Contact))'),
          ('Visite planifiée ou faite', '=SUMPRODUCT((D_Date<>"")*ISNUMBER(D_Visite))'),
          ('Offre envoyée', '=SUMPRODUCT((D_Date<>"")*ISNUMBER(D_Offre))'),
          ('Signée', '=SUMPRODUCT((D_Signe="O")*1)')]
for i, (lib, f_) in enumerate(etapes):
    n = l + 2 + i
    ecrire(wpi, f'A{n}', lib, f_gras, border=B_CASE)
    ecrire(wpi, f'B{n}', f_, fmt='0', border=B_CASE, align=Alignment(horizontal='center'))
    ecrire(wpi, f'C{n}', '' if i == 0 else f'=IF(B{n - 1}=0,"",B{n}/B{n - 1})', fmt='0%', border=B_CASE, align=Alignment(horizontal='center'))
    ecrire(wpi, f'D{n}', f'=IF($B${l + 2}=0,"",B{n}/$B${l + 2})', fmt='0%', border=B_CASE, align=Alignment(horizontal='center'))

l = l + 2 + len(etapes) + 2
ecrire(wpi, f'A{l}', 'Résultat par priorité (pour recalibrer le scoring, stratégie §2.7)', f_section)
for j, e in enumerate(['Priorité', 'Demandes', 'Signées', 'Perdues', 'Taux de signature (signées / décidées)', 'CA signé (CHF, HT)']):
    ecrire(wpi, f'{get_column_letter(j + 1)}{l + 1}', e, f_entete, F_ANTH, align=A_CENTRE, border=B_CASE)
for i, p_ in enumerate(['A', 'B', 'C', 'Hors cible']):
    n = l + 2 + i
    ecrire(wpi, f'A{n}', p_, f_gras, border=B_CASE)
    ecrire(wpi, f'B{n}', f'=COUNTIFS(D_Prio,"{p_}")', fmt='0', border=B_CASE, align=Alignment(horizontal='center'))
    ecrire(wpi, f'C{n}', f'=COUNTIFS(D_Prio,"{p_}",D_Signe,"O")', fmt='0', border=B_CASE, align=Alignment(horizontal='center'))
    ecrire(wpi, f'D{n}', f'=COUNTIFS(D_Prio,"{p_}",D_Signe,"N")', fmt='0', border=B_CASE, align=Alignment(horizontal='center'))
    ecrire(wpi, f'E{n}', f'=IF(C{n}+D{n}=0,"",C{n}/(C{n}+D{n}))', fmt='0%', border=B_CASE, align=Alignment(horizontal='center'))
    ecrire(wpi, f'F{n}', f'=SUMIFS(D_Montant,D_Prio,"{p_}",D_Signe,"O")', fmt='#,##0', border=B_CASE, align=Alignment(horizontal='center'))
ecrire(wpi, f'A{l + 7}', 'La grille est bonne si les A signent au moins deux fois plus souvent que les C (à vérifier après 6 mois).', f_sous)

l = l + 9
ecrire(wpi, f'A{l}', 'Offres perdues par motif', f_section)
for j, e in enumerate(['Motif', 'Offres perdues', 'Montant (CHF, HT)']):
    ecrire(wpi, f'{get_column_letter(j + 1)}{l + 1}', e, f_entete, F_ANTH, align=A_CENTRE, border=B_CASE)
for i, m_ in enumerate(MOTIFS + ['Non renseigné']):
    n = l + 2 + i
    crit = f'D_Motif,"{m_}"' if m_ != 'Non renseigné' else 'D_Motif,""'
    ecrire(wpi, f'A{n}', m_, f_gras, border=B_CASE)
    if m_ == 'Non renseigné':
        ecrire(wpi, f'B{n}', '=SUMPRODUCT((D_Statut="Perdue")*(D_Motif=""))', fmt='0', border=B_CASE, align=Alignment(horizontal='center'))
        ecrire(wpi, f'C{n}', '=SUMPRODUCT((D_Statut="Perdue")*(D_Motif="")*ISNUMBER(D_Montant),D_Montant)', fmt='#,##0', border=B_CASE, align=Alignment(horizontal='center'))
    else:
        ecrire(wpi, f'B{n}', f'=COUNTIFS(D_Statut,"Perdue",{crit})', fmt='0', border=B_CASE, align=Alignment(horizontal='center'))
        ecrire(wpi, f'C{n}', f'=SUMIFS(D_Montant,D_Statut,"Perdue",{crit})', fmt='#,##0', border=B_CASE, align=Alignment(horizontal='center'))
for col_, w in {'A': 34, 'B': 13, 'C': 13, 'D': 13, 'E': 16, 'F': 16, 'G': 18, 'H': 18}.items():
    wpi.column_dimensions[col_].width = w

# =============================================================================================
# Mode d'emploi
# =============================================================================================
wm = wb.create_sheet('Mode d\'emploi', 0)
titre(wm, 'Suivi des demandes et KPI · Andy Construct', 'Outil de démarrage tant que le CRM (Pipedrive ou Brevo) '
      'n\'est pas en place : scénario S de la stratégie d\'acquisition (§5.3, §8.3).', 2)
TEXTE = [
    ('Les onglets', None),
    ('Demandes', 'Une ligne par demande, quel que soit le canal. Score, priorité, échéance et « À faire » se calculent seuls.'),
    ('Pipeline', 'Où en sont les demandes : nombre par statut, montants des offres, entonnoir, pertes par motif.'),
    ('KPI mensuels', 'Les chiffres du mois, comparés aux objectifs : demandes par source, taux de conversion, délai de rappel, CA signé, avis.'),
    ('Objectifs', 'Objectifs à 3, 6 et 12 mois de la stratégie (§1). Modifiables. Le mois de mise en ligne (M1) se saisit ici.'),
    ('Paramètres', 'Grille de scoring, listes, délais de suivi, jours fériés, table NPA → zone. Modifiable avec prudence.'),
    ('Couleurs', None),
    ('Blanc', 'Cellule à saisir (Demandes).'),
    ('Gris', 'Cellule calculée : ne pas la modifier ni l\'effacer.'),
    ('Jaune (texte bleu)', 'Paramètre, objectif ou relevé mensuel à saisir.'),
    ('Jaune pâle', 'Ligne « EXEMPLE » : à supprimer avant le premier usage.'),
    ('Rouge pâle', 'Retard : premier contact, visite à fixer, offre à envoyer ou à relancer. La colonne « À faire » dit quoi faire.'),
    ('Pour démarrer', None),
    ('1', 'Onglet Demandes : sélectionnez les lignes 5 à 9 (les 5 lignes EXEMPLE), clic droit, « Supprimer ». Les synthèses s\'ajustent seules.'),
    ('2', 'Onglet Objectifs : indiquez le mois réel de mise en ligne du site (M1). Ajustez les objectifs si vous démarrez en scénario S.'),
    ('3', 'Onglet Paramètres : vérifiez les jours fériés et, plus tard, les délais de suivi (cases jaunes).'),
    ('Saisir une demande', None),
    ('Reçue le', 'Toujours en premier : c\'est la date qui active les calculs de la ligne.'),
    ('Listes', 'Canal, source, type de client, service, canton, surface, délai, statut, motif : choisissez dans la liste (flèche de la cellule).'),
    ('NPA', 'Saisissez-le : il donne la zone du scoring (indispensable dans le canton de Vaud, où la zone dépend du district).'),
    ('Message', 'Collez le texte du formulaire ou résumez l\'appel. « Dégât », « fuite », « état des lieux », « fin de bail » avec « Dès que possible » : priorité A.'),
    ('Statut', '1 Nouvelle demande → 2 Contact établi → 3 Visite planifiée → 4 Offre envoyée → 5 Relance / négociation → Gagnée ou Perdue.'),
    ('Dates', 'Premier contact, visite, offre, signature, fin de chantier, avis : saisissez-les au fil du suivi. Format : 15.03.2027.'),
    ('Chaque jour (5 minutes)', None),
    ('À faire', 'Onglet Demandes, colonne « À faire » : filtrez les cellules non vides (flèche de l\'en-tête). Traitez d\'abord les priorités A, puis B, puis C.'),
    ('Priorités', 'A : rappeler dans la journée (stratégie : moins de 2 h ouvrables). B : le jour même ou le lendemain. C : sous 2 jours ouvrables.'),
    ('Score', 'Le score ordonne les rappels, il ne décide jamais : toutes les demandes sont rappelées, et un associé valide toute réponse « hors cible ».'),
    ('Chaque mois (15 minutes)', None),
    ('Relevés', 'Onglet KPI mensuels : saisissez les visites et contacts web (Umami) et le nombre d\'avis Google affiché sur la fiche.'),
    ('Lecture', 'Comparez chaque indicateur à son objectif. Au 3e mois, recalez les objectifs et la grille de scoring sur les données réelles (stratégie §1.2 et §2.7).'),
    ('Données personnelles (nLPD)', None),
    ('Où', 'Gardez ce fichier sur un poste ou un espace protégé par mot de passe. Ne l\'envoyez pas par e-mail.'),
    ('Combien de temps', 'Prospects sans suite : effacez la ligne 24 mois après le dernier contact. Clients : selon les obligations comptables et la garantie (stratégie §9.1, durées à valider par le juriste).'),
    ('Droits', 'Une personne qui demande l\'accès ou l\'effacement de ses données reçoit une réponse sous 30 jours.'),
    ('Passer au CRM', None),
    ('Export', 'Fichier, Enregistrer sous, CSV. Les colonnes correspondent aux champs prévus dans Pipedrive (stratégie §5.5) : canal, source, type de client, service, surface, délai, commune, zone, score, priorité, dates, montant, motif de perte, avis.'),
    ('Limites', None),
    ('Délais', 'Comptés en jours ouvrables (lundi-vendredi, hors jours fériés), pas en heures.'),
    ('Capacité', '500 lignes prêtes. Au-delà, copiez la dernière ligne vers le bas : les synthèses lisent jusqu\'à la ligne 2000.'),
    ('Scoring', 'Même grille que le formulaire du site (site/api/data/scoring.json). Si la grille change dans l\'API, reportez les points dans l\'onglet Paramètres.'),
]
n = 4
for a, b in TEXTE:
    if b is None:
        n += 1
        ecrire(wm, f'A{n}', a, f_section)
        wm.cell(n, 1).border = Border(bottom=Side(style='thin', color=ROUGE))
        wm.cell(n, 2).border = Border(bottom=Side(style='thin', color=ROUGE))
    else:
        ecrire(wm, f'A{n}', a, f_gras, align=A_WRAP)
        ecrire(wm, f'B{n}', b, f_base, align=A_WRAP)
        if a == 'Blanc':
            wm[f'A{n}'].fill = PatternFill(None)
            wm[f'A{n}'].border = B_CASE
        elif a == 'Gris':
            wm[f'A{n}'].fill = F_BRUME
        elif a.startswith('Jaune ('):
            wm[f'A{n}'].fill = F_JAUNE
            wm[f'A{n}'].font = Font(name=POLICE, size=10, bold=True, color='0000FF')
        elif a == 'Jaune pâle':
            wm[f'A{n}'].fill = F_EXEMPLE
        elif a == 'Rouge pâle':
            wm[f'A{n}'].fill = fill('FDECEC')
    n += 1
wm.column_dimensions['A'].width = 26
wm.column_dimensions['B'].width = 120
ecrire(wm, f'A{n + 1}', f'Version du {dt.date.today():%d.%m.%Y}. Généré par livrables/sources/generer_suivi_xlsx.py.', f_sous)

# Police par défaut du classeur
for ws in wb.worksheets:
    ws.sheet_view.showGridLines = ws.title not in ('Mode d\'emploi',)
for ws_ in (wm, wpi, wo, wp):
    ws_.page_setup.orientation = 'landscape'
    ws_.sheet_properties.pageSetUpPr.fitToPage = True
    ws_.page_setup.fitToWidth = 1
    ws_.page_setup.fitToHeight = 0
ordre = ['Mode d\'emploi', 'Demandes', 'Pipeline', 'KPI mensuels', 'Objectifs', 'Paramètres']
wb._sheets = [wb[t] for t in ordre]
wb.active = 0
wb.properties.creator = 'Andy Construct'
wb.properties.title = 'Suivi des demandes et KPI'
SORTIE.parent.mkdir(parents=True, exist_ok=True)
wb.save(SORTIE)
print('écrit', SORTIE.relative_to(RACINE), '·', N_LIGNES, 'lignes de saisie ·', len(seg), 'plages NPA')
