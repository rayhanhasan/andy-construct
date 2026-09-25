# -*- coding: utf-8 -*-
"""Génère les pages HTML statiques du site Andy Construct dans site/.

Usage, depuis la racine du dépôt :  python3 tools/build/build.py
Sources : common.py (gabarits, coordonnées, JSON-LD, formulaire), content.py (références, FAQ),
icons.py, page_*.py (contenu de chaque page), faq.json (FAQ du brief SEO, mot pour mot).
Les photos sont lues dans site/assets/img/portfolio/manifest.json.
"""
import os, sys
sys.dont_write_bytecode = True  # pas de __pycache__ dans le dépôt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import page_index, page_prestations, page_realisations, page_autres

page_index.build()
page_prestations.build()
page_realisations.build()
page_autres.build()
