# -*- coding: utf-8 -*-
"""Contenus partagés : références, FAQ (brief SEO §4, mot pour mot), prestations de l'accueil."""
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
    ('tendu', 'Plafonds tendus', 'plafonds-tendus',
     "Tissu tendu à froid pour un plafond parfaitement lisse. Idéal en rénovation et pour intégrer l'éclairage."),
    ('acoustique', 'Plafonds acoustiques et phoniques', 'plafonds-acoustiques',
     "Moins d'écho et moins de bruit entre les locaux : salles de réunion, salles communales, restaurants, écoles."),
    ('fauxplafond', 'Faux-plafonds', 'plafonds-placoplatre',
     "Plaques de plâtre, fibre de bois ou minérale, bacs métalliques : le matériau adapté à chaque local."),
    ('cloison', 'Cloisons', 'cloisons',
     "Cloisons légères en plaques de plâtre et cloisons mobiles en aluminium, pour redistribuer bureaux et logements."),
    ('isolation', 'Isolation thermique et phonique', 'isolation',
     "Isolant posé dans les plafonds et les cloisons, chape flottante contre les bruits d'impact."),
    ('peinture', 'Peinture intérieure', 'peinture',
     "Préparation des supports, enduits et peinture des plafonds et des murs : des pièces livrées terminées."),
]

ALSO = [('Cadres acoustiques', 'cadres-acoustiques'), ('Caissons lumineux', 'integrations'), ('Trappes de visite', 'integrations'),
        ('Chape flottante', 'chape-flottante'), ('Protection incendie', 'protection-incendie'), ('Puits de lumière', 'integrations')]
