# -*- coding: utf-8 -*-
"""Pictogrammes en coupe (trait 1.75 px anthracite, un seul détail rouge par icône)."""

SLAB = '<path d="M4 9h40"/><path d="M9 4l5 5M18 4l5 5M27 4l5 5M36 4l5 5"/>'


def svg(body, size=48):
    return ('<svg class="icon" viewBox="0 0 48 48" width="%d" height="%d" aria-hidden="true" focusable="false">' % (size, size)
            + body + '</svg>')


ICONS = {
    # Placo : suspentes, ossature (rouge), plaques, spot encastré
    'placo': svg(SLAB + '<path d="M11 9v12M24 9v12M37 9v12"/><path class="accent" d="M4 21h40"/>'
                 '<path d="M4 25h40"/><path d="M20 25l-3 8M28 25l3 8" stroke-dasharray="2 3"/>'),
    # Isolation acoustique : panneau, ondes sonores (rouge)
    'isolation-acoustique': svg(SLAB + '<path d="M14 9v6M34 9v6"/><path d="M8 15h32v5H8z"/>'
                                '<path class="accent" d="M17 33a10 10 0 0 1 14 0M12 40a17 17 0 0 1 24 0"/>'),
    # Cloison isolante : sol, plafond, deux parements et isolant en ondes (rouge)
    'cloisons-isothermes': svg('<path d="M4 6h40M4 42h40M16 6v36M32 6v36"/>'
                               '<path class="accent" d="M24 8c-7 3-7 6 0 9s7 6 0 9-7 6 0 9"/>'),
    # Peinture : rouleau (rouge) et manche
    'peinture': svg('<path class="accent" d="M8 7h24v9H8z"/><path d="M32 11h6v10H22v7"/><path d="M20 28h4v15h-4z"/>'),
    # Correction acoustique : barres d'un signal qui s'atténue (rouge au centre)
    'echo': svg('<path d="M8 20v8M14 15v18M34 15v18M40 20v8"/><path class="accent" d="M20 10v28M28 12v24"/>'),
    # Isolation phonique : mur, onde stoppée (rouge)
    'phonique': svg('<path d="M28 6v36M34 6v36"/><path class="accent" d="M6 18c4 3 4 9 0 12M12 15c5 5 5 13 0 18M18 12c6 7 6 17 0 24"/>'),
    # Coupe-feu : flamme
    'feu': svg('<path class="accent" d="M24 42c-8 0-13-5-13-12 0-8 7-11 8-20 5 3 8 8 8 13 2-2 3-4 3-7 4 4 7 9 7 14 0 7-5 12-13 12z"/>'
               '<path d="M24 42c-3 0-5-2-5-5 0-3 3-5 4-9 3 2 6 5 6 9 0 3-2 5-5 5z"/>'),
    # Autre chose : point d'interrogation dans un cercle
    'ne-sait-pas': svg('<circle cx="24" cy="24" r="18"/><path class="accent" d="M18.5 19a5.5 5.5 0 1 1 7.5 5.1c-1.3.6-2 1.6-2 3V29"/>'
                       '<path d="M24 34v2.5"/>'),
}

# v5 : les quatre métiers du menu
ICONS['faux-plafonds'] = ICONS['placo']
ICONS['cloisons'] = svg('<path d="M4 6h40M4 42h40"/><path d="M10 6v36M22 6v36M34 6v36"/><path class="accent" d="M16 6v36"/><path d="M28 24h4"/>')
ICONS['platrerie-peinture'] = ICONS['peinture']

INFO = ('<svg class="i-info" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false">'
        '<circle cx="12" cy="12" r="10"/><path d="M12 10.5V17M12 7v1.5"/></svg>')
