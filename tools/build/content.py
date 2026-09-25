# -*- coding: utf-8 -*-
"""Contenus partagés : références, FAQ (adaptée du brief SEO §4 aux 4 services), prestations de l'accueil."""
import json, os
from common import fr

REFS = [
    ('Ville de Genève', ''), ('Salle communale de Collonge-Bellerive', ''), ('Piaget', ''),
    ('Conservatoire de Musique de Genève', ''), ("Salle de l'Alhambra", ''),
    ('Mairie de Plan-les-Ouates', 'Salle communale'), ('Laboratoire Covance CLS SA', ''), ('De Grisogono', ''),
    ('Energestion Ingénieurs & Architectes SIA', ''), ('Domaine des Perrières', 'Coppet (VD)'),
    ('Dipan SA', 'Nyon (VD)'), ("HEAD – Haute école d'art et de design", 'Genève'), ('OMC', ''),
    ('Celgene', ''), ('Bank Sarasin', 'Aujourd\'hui J. Safra Sarasin'), ('UBS', ''), ('Hôtel à Chavannes-de-Bogis', ''),
    ('Harmonie Nautique de Genève', ''),
]
REF_NOTE = dict(REFS)

REF_GROUPS = [
    ('Collectivités et institutions', ['Ville de Genève', 'Mairie de Plan-les-Ouates', 'Salle communale de Collonge-Bellerive', 'OMC']),
    ('Culture et formation', ['Conservatoire de Musique de Genève', "Salle de l'Alhambra", "HEAD – Haute école d'art et de design", 'Harmonie Nautique de Genève']),
    ('Entreprises', ['Piaget', 'De Grisogono', 'UBS', 'Bank Sarasin', 'Celgene', 'Laboratoire Covance CLS SA',
                     'Energestion Ingénieurs & Architectes SIA', 'Dipan SA']),
    ('Hôtellerie et domaines', ['Hôtel à Chavannes-de-Bogis', 'Domaine des Perrières']),
]

FAQ = [(fr(q), fr(a)) for q, a in json.load(open(os.path.join(os.path.dirname(__file__), 'faq.json'), encoding='utf-8'))]

HOME_SERVICES = [
    ('fauxplafond', 'Placo', 'placo',
     "Doublages, faux-plafonds et cloisons en plaques de plâtre : pour créer, redresser ou redistribuer vos espaces."),
    ('peinture', 'Peinture intérieure', 'peinture',
     "Préparation des supports, enduits et peinture des plafonds et des murs : des pièces livrées terminées."),
    ('acoustique', 'Isolation acoustique', 'isolation-acoustique',
     "Moins de bruit entre les pièces, les logements et les étages, grâce à des plafonds et des parois isolés."),
    ('isotherme', 'Cloisons isothermes', 'cloisons-isothermes',
     "Cloisons et doublages isolants entre locaux chauffés et non chauffés, pour limiter les pertes de chaleur."),
]
