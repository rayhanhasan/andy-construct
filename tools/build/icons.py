# -*- coding: utf-8 -*-
"""Pictogrammes en coupe (trait 1.75 px anthracite, un seul détail rouge par icône)."""

SLAB = '<path d="M4 9h40"/><path d="M9 4l5 5M18 4l5 5M27 4l5 5M36 4l5 5"/>'


def svg(body):
    return ('<svg class="icon" viewBox="0 0 48 48" width="48" height="48" aria-hidden="true" focusable="false">'
            + body + '</svg>')


ICONS = {
    # Plafond tendu : dalle, murs, profilés et toile tendue (rouge), suspension d'éclairage
    'tendu': svg(SLAB + '<path d="M6 9v33M42 9v33"/><path class="accent" d="M6 20h36"/>'
                 '<path d="M6 17h4M38 17h4"/><path d="M24 20v7M19 31h10l-2-4h-6z"/>'),
    # Acoustique : panneau suspendu, ondes sonores absorbées (rouge)
    'acoustique': svg(SLAB + '<path d="M14 9v6M34 9v6"/><path d="M8 15h32v5H8z"/>'
                      '<path class="accent" d="M17 33a10 10 0 0 1 14 0M12 40a17 17 0 0 1 24 0"/>'),
    # Faux-plafond : suspentes, ossature (rouge), plaques, spot encastré
    'fauxplafond': svg(SLAB + '<path d="M11 9v12M24 9v12M37 9v12"/><path class="accent" d="M4 21h40"/>'
                       '<path d="M4 25h40"/><path d="M20 25l-3 8M28 25l3 8" stroke-dasharray="2 3"/>'),
    # Cloison : dalle, sol, cloison double parement (rouge) et porte
    'cloison': svg('<path d="M4 6h40M4 42h40"/><path class="accent" d="M17 6v36M22 6v36"/>'
                   '<path d="M30 42V20h9v22"/>'),
    # Isolation : parois et symbole d'isolant en ondes (rouge)
    'isolation': svg('<path d="M4 12h40M4 36h40"/>'
                     '<path class="accent" d="M4 24c3-9 5-9 8 0s5 9 8 0 5-9 8 0 5 9 8 0 5-9 8 0"/>'),
    # Peinture : rouleau (rouge) et manche
    'peinture': svg('<path class="accent" d="M8 7h24v9H8z"/><path d="M32 11h6v10H22v7"/><path d="M20 28h4v15h-4z"/>'),
}
