# -*- coding: utf-8 -*-
"""Contexte de génération : mode (preview, verification, production), confirmations Cxx, typographie.

Les trois modes (décision D6 du chef de projet) :
- preview      : textes définitifs, bandeau « version de validation », noindex ;
- verification : idem, et chaque passage à confirmer est souligné en pointillé avec son code en exposant ;
- production   : texte de repli tant que le code n'est pas confirmé dans donnees/confirmations.json,
                 logos « autorise » seulement, photos « retirer » exclues, indexable, sans bandeau.
"""
import html, json, os, re

ICI = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(ICI))
SITE = os.path.join(ROOT, 'site')          # sources des ressources (images, polices, api, suivi.js)
DONNEES = os.path.join(ICI, 'donnees')
PROD = 'https://www.andyconstruct.ch/'

MODE = 'preview'
OUT = SITE


def charger(nom, defaut=None):
    chemin = os.path.join(DONNEES, nom)
    if not os.path.exists(chemin):
        return defaut
    return json.load(open(chemin, encoding='utf-8'))


CONF = charger('confirmations.json', {})
CONFIG = charger('config.json', {})
TEMOIGNAGES = [t for t in (charger('temoignages.json', []) or []) if t.get('texte') and t.get('accord_date')]
AVIS = charger('avis.json', {}) or {}


def regler(mode, out):
    global MODE, OUT
    MODE, OUT = mode, out


def prod():
    return MODE == 'production'


# ---------------------------------------------------------------- confirmations
# Questions courtes (copy deck §R), affichées dans la légende du mode « verification »
QUESTIONS = {
    'C01': 'Délai de rappel toujours tenable', 'C02': 'Visite et devis gratuits, sans engagement',
    'C03': 'Horaires (lun-ven, 7 h – 18 h)', 'C04': 'Petits chantiers acceptés',
    'C05': 'Les 4 métiers faits par l\'entreprise (« un seul interlocuteur »)', 'C06': 'Offre détaillée, aucun supplément sans accord écrit',
    'C07': 'Protection et nettoyage chaque soir', 'C08': 'Délai d\'envoi de l\'offre après la visite',
    'C09': 'Qui rappelle (nom de l\'associé)', 'C10': 'Associés nommés (et photographiés)',
    'C11': 'Membre du GGE', 'C12': 'Attestation d\'assurance RC', 'C13': 'Attestations AVS, LPP, impôts, CCT',
    'C14': 'Lots CFC 271, 283, 285', 'C15': 'Normes SIA 118, 181, 180, AEAI', 'C16': 'Nom « Cloisons isolantes », combles, pas de chambres froides',
    'C17': 'Peinture : déroulé, fins de bail, prix par pièce', 'C18': 'Acoustique : systèmes, épaisseurs, correction de l\'écho',
    'C19': 'Travaux le soir, le week-end, en vacances scolaires', 'C20': 'Immeubles habités : avis aux locataires, méthode',
    'C21': 'Zone des particuliers, villes de la carte', 'C22': 'Références : accords, OMC, Everness, années',
    'C23': 'Références à citer par service', 'C24': 'Effectif', 'C25': 'Photos : lieux, prestations, accords',
    'C26': 'Avant / après : lieux et prestations', 'C28': 'Paiement : jamais de liquide à l\'avance',
    'C29': 'Bureau à Carouge (sur rendez-vous)', 'C30': 'E-mail sur le domaine, mobile « sur les chantiers »',
    'C31': 'Fourchettes de prix réelles', 'C32': 'Retouches après la réception', 'C33': 'Contrats selon la SIA 118',
    'C34': 'Hébergeur de production', 'C35': 'Numéro de TVA', 'C40': 'Photos de peinture, visite d\'un chantier',
    'C41': 'Délai de visite', 'C43': 'Aide pour les subventions', 'C44': 'Témoignages réels',
    'V01': 'Relecture juridique (garanties)', 'V02': 'Politique de confidentialité à relire (juriste)',
}

UTILISES = set()   # codes rencontrés pendant la génération de la page en cours


def _codes(codes):
    return codes.split() if isinstance(codes, str) else list(codes)


def confirme(codes):
    return all(CONF.get(c, {}).get('confirme') for c in _codes(codes))


def definitif(codes):
    """Le texte définitif est-il publié ? Toujours en preview et verification ; en production si confirmé."""
    return MODE != 'production' or confirme(codes)


def marque(codes, contenu, bloc=False):
    """Mode verification : souligne le passage et affiche son code. Sinon : contenu inchangé."""
    cs = _codes(codes)
    if MODE != 'verification' or confirme(cs) or not contenu:
        return contenu
    UTILISES.update(cs)
    tag = 'div' if bloc else 'span'
    return '<%s class="vc">%s<sup class="vc__code">%s</sup></%s>' % (tag, contenu, ' '.join(cs), tag)


def T(codes, definitive, repli=''):
    """Texte HTML : définitif (marqué en verification) ou repli (production non confirmée)."""
    if definitif(codes):
        return marque(codes, definitive)
    return repli or ''


def V(codes, definitive, repli=''):
    """Valeur brute (attribut, meta, JSON-LD, llms.txt) : jamais marquée."""
    return definitive if definitif(codes) else repli


def M(codes):
    """Compte un code comme « utilisé » sans marquer (texte de repli affiché en preview faute de définitif)."""
    if MODE == 'verification' and not confirme(codes):
        UTILISES.update(_codes(codes))


# ---------------------------------------------------------------- typographie
NB = ' '
e = lambda s: html.escape(s, quote=True)


def fr(t):
    """Espaces insécables : devant : ; ? ! », après «, dans les numéros, heures, montants, avant un tiret « – »."""
    t = re.sub(r' ([:;?!»])', NB + r'\1', t)
    t = t.replace('« ', '«' + NB)
    t = re.sub(r'\+41 (\d\d) (\d\d\d) (\d\d) (\d\d)', lambda m: NB.join(['+41'] + list(m.groups())), t)
    t = re.sub(r'\b0(\d\d) (\d\d\d) (\d\d) (\d\d)\b', lambda m: NB.join(['0' + m.group(1)] + list(m.groups()[1:])), t)
    t = re.sub(r'(\d+) h\b', r'\1' + NB + 'h', t)
    t = re.sub(r'\b(CHF|CFC|SIA|IDE|n°|N°) (\S)', r'\1' + NB + r'\2', t)
    t = re.sub(r'(\d) (m²|cm|Mo|Ko|jours|pages|ans|minutes|étapes|projets|photos|références|personnes)\b', r'\1' + NB + r'\2', t)
    t = t.replace(' – ', NB + '– ')
    return t


def typo(doc):
    """Applique fr() aux seuls nœuds texte du <body> (ni attributs, ni scripts)."""
    head, sep, body = doc.partition('<body')
    morceaux = re.split(r'(<script\b.*?</script>)', body, flags=re.S)
    for i in range(0, len(morceaux), 2):
        morceaux[i] = re.sub(r'>([^<]+)<', lambda m: '>' + fr(m.group(1)) + '<', morceaux[i])
    return head + sep + ''.join(morceaux)


def insec(nom):
    """Noms composés insécables (« Plan-les-Ouates ») : le mot à tiret ne se coupe pas."""
    return re.sub(r'(\S+-\S+)', r'<span class="nowrap">\1</span>', nom)
