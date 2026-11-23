# -*- coding: utf-8 -*-
"""Schémas en coupe (v5) : petites illustrations vectorielles des solutions (document « Contenu site web » du client),
redessinées dans la charte (anthracite, plâtre, acier, un seul détail rouge). Toujours accompagnées d'un titre qui dit
ce qu'elles montrent : role="img" + aria-label. Aucune ressource externe, aucun poids d'image."""

INK, GRIS, ACIER, PLATRE, BRUME, LIGNE, ROUGE, BOIS, ISOL = ('#1D1F22', '#44494F', '#B9BDC2', '#F7F7F5', '#ECECE9', '#DCDEE1',
                                                           '#E8000F', '#C9A77C', '#E9D9A6')


def _svg(label, corps, vb='0 0 400 240'):
    return ('<svg class="schema" viewBox="%s" role="img" aria-label="%s" focusable="false">'
            '<rect width="100%%" height="100%%" fill="%s"/>%s</svg>' % (vb, label, BRUME, corps))


def _txt(x, y, t, anchor='start', size=13, fill=GRIS, weight=600):
    return ('<text x="%s" y="%s" font-family="Source Sans 3, Arial, sans-serif" font-size="%s" font-weight="%s" fill="%s" text-anchor="%s">%s</text>'
            % (x, y, size, weight, fill, anchor, t))


def _onde(x0, x1, y, amp=6, pas=24, couleur=ROUGE, ep=2):
    d = 'M%d %d' % (x0, y)
    x, haut = x0, True
    while x < x1:
        d += ' q%d %d %d 0' % (pas / 2, -amp if haut else amp, pas)
        x += pas
        haut = not haut
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (d, couleur, ep)


def _hachure(x0, x1, y0, y1, yb):
    """Une hachure à 45° de (x0, yb) vers le haut à droite, coupée au rectangle [x0, x1] × [y0, y1]."""
    ax, ay = x0, yb
    if ay > y1:
        ax, ay = x0 + (ay - y1), y1
    bx, by = x0 + (yb - y0), y0
    if bx > x1:
        bx, by = x1, yb - (x1 - x0)
    if ax >= x1 or by >= y1:
        return ''
    return '<path d="M%d %dL%d %d" stroke="%s" stroke-width="1"/>' % (ax, ay, bx, by, GRIS)


def _dalle():
    return ('<rect x="0" y="0" width="400" height="34" fill="%s"/>' % ACIER
            + ''.join('<path d="M%d 34l20-34" stroke="%s" stroke-width="1"/>' % (x, GRIS) for x in range(-20, 420, 22)))


# ---------------------------------------------------------------- faux plafonds
def tissu_tendu():
    return _svg('Coupe : tissu tendu fixé sur un profilé périphérique, surface lisse',
                _dalle() + '<rect x="40" y="96" width="320" height="10" rx="2" fill="%s" stroke="%s" stroke-width="2"/>' % (PLATRE, INK)
                + '<rect x="30" y="86" width="14" height="30" fill="%s"/><rect x="356" y="86" width="14" height="30" fill="%s"/>' % (INK, INK)
                + '<g class="sch-onde">' + _onde(150, 250, 150, amp=7, pas=20, couleur=ROUGE) + '</g>'
                + _txt(200, 186, 'Le son est absorbé', 'middle') + _txt(200, 82, 'Toile tendue', 'middle', fill=INK))


def plaque_platre():
    return _svg('Coupe : ossature métallique suspendue et plaques de plâtre, éclairage intégré',
                _dalle() + ''.join('<path d="M%d 34v58" stroke="%s" stroke-width="2"/>' % (x, GRIS) for x in (90, 200, 310))
                + '<rect x="40" y="92" width="320" height="8" fill="%s"/>' % ACIER
                + '<rect x="40" y="100" width="320" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (PLATRE, INK)
                + '<rect x="150" y="114" width="100" height="6" fill="%s"/>' % ROUGE
                + '<path class="sch-lumiere" d="M170 122l-18 50M230 122l18 50" stroke="%s" stroke-width="2" stroke-dasharray="3 5"/>' % ROUGE
                + _txt(200, 200, 'Plafond lisse, spots et gorges intégrés', 'middle'))


def fibre_bois():
    return _svg('Coupe : dalle, isolant en fibre de bois puis faux plafond visible',
                _dalle() + '<rect x="0" y="34" width="400" height="56" fill="%s"/>' % BOIS
                + ''.join('<path d="M%d %d h22" stroke="#A88758" stroke-width="2"/>' % (x, y) for y in (48, 62, 76) for x in range(10 + (y % 3) * 8, 400, 44))
                + ''.join('<path d="M%d 90v40" stroke="%s" stroke-width="2"/>' % (x, GRIS) for x in (100, 200, 300))
                + '<rect x="20" y="130" width="360" height="12" fill="%s" stroke="%s" stroke-width="2"/>' % (PLATRE, INK)
                + _txt(24, 66, 'Dalle · isolant fibre de bois', fill=INK) + _txt(24, 172, 'Faux plafond visible'))


def fibre_minerale():
    cases = ''
    for i, x in enumerate(range(30, 370, 68)):
        for j, y in enumerate((60, 128)):
            fill = '#F3D9DA' if (i, j) == (2, 0) else PLATRE
            cases += '<rect%s x="%d" y="%d" width="64" height="64" fill="%s"/>' % (' class="sch-dalle"' if (i, j) == (2, 0) else '', x + 2, y + 2, fill)
            cases += ''.join('<circle cx="%d" cy="%d" r="1.6" fill="%s"/>' % (x + 12 + k * 14 % 48, y + 14 + (k * 23) % 44, ACIER) for k in range(6))
    return _svg('Vue de dessous : dalles démontables en fibre minérale sur ossature apparente',
                '<rect x="30" y="60" width="340" height="136" fill="%s"/>' % GRIS + cases
                + '<path class="sch-dalle" d="M168 60h68v68h-68z" fill="none" stroke="%s" stroke-width="3"/>' % ROUGE
                + _txt(200, 42, 'Une dalle se retire : réseaux accessibles', 'middle'))


def metallique():
    bac = ''
    for x, y in ((40, 54), (210, 54), (40, 140), (210, 140)):
        bac += '<rect x="%d" y="%d" width="150" height="74" fill="%s"/>' % (x, y, '#D6D9DC')
        bac += ''.join('<circle cx="%d" cy="%d" r="1.5" fill="%s"/>' % (x + 8 + i * 9, y + 8 + j * 9, GRIS) for i in range(16) for j in range(7))
    return _svg('Vue de dessous : bacs métalliques perforés', bac + '<path class="sch-trait" d="M40 50h320" stroke="%s" stroke-width="4"/>' % ROUGE)


# ---------------------------------------------------------------- cloisons
def _sol_plafond():
    return '<path d="M20 30h360M20 210h360" stroke="%s" stroke-width="4"/>' % INK


def cloison_platre():
    return _svg('Coupe : cloison en plaques de plâtre sur ossature métallique, isolant au cœur',
                _sol_plafond() + '<rect x="150" y="30" width="16" height="180" fill="%s" stroke="%s" stroke-width="2"/>' % (PLATRE, INK)
                + '<rect x="234" y="30" width="16" height="180" fill="%s" stroke="%s" stroke-width="2"/>' % (PLATRE, INK)
                + '<rect x="166" y="30" width="68" height="180" fill="%s"/>' % ISOL
                + ''.join(_onde(170, 230, y, amp=5, pas=15, couleur='#C9B36B', ep=1.5) for y in range(50, 200, 22))
                + '<path d="M200 30v180" stroke="%s" stroke-width="3" stroke-dasharray="10 8"/>' % ROUGE
                + _txt(140, 124, 'Plaque', 'end') + _txt(260, 124, 'Plaque') + _txt(200, 232, 'Isolant au cœur', 'middle'))


def cloison_mobile():
    return _svg('Cloison mobile : panneaux suspendus à un rail, qui coulissent',
                '<rect x="40" y="30" width="320" height="10" fill="%s"/>' % GRIS
                + '<g class="sch-glisse">' + ''.join('<rect x="%d" y="44" width="62" height="160" fill="%s" stroke="%s" stroke-width="2"/>' % (x, PLATRE, ACIER) for x in (52, 118, 184)) + '</g>'
                + '<path d="M282 124h60M330 112l12 12-12 12" fill="none" stroke="%s" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>' % ROUGE)


def paroi_vitree():
    return _svg('Paroi vitrée : cadre fin et grands vitrages',
                '<rect x="40" y="40" width="320" height="160" fill="#D5E1E4" stroke="%s" stroke-width="6"/>' % GRIS
                + '<path d="M146 40v160M254 40v160" stroke="%s" stroke-width="6"/>' % GRIS
                + '<g class="sch-reflet">' + ''.join('<path d="M%d 62l34 34" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>' % x for x in (66, 172, 280)) + '</g>'
                + '<path d="M40 204h320" stroke="%s" stroke-width="3"/>' % ROUGE)


def cloison_alu():
    return _svg('Cloison aluminium : modules pleins et vitrés dans une ossature aluminium',
                '<rect x="60" y="34" width="280" height="172" fill="%s" stroke="%s" stroke-width="6"/>' % (PLATRE, GRIS)
                + '<rect x="63" y="37" width="274" height="70" fill="#D5E1E4"/>'
                + '<path d="M200 34v172M60 107h280" stroke="%s" stroke-width="6"/>' % GRIS
                + '<path d="M60 107h140" stroke="%s" stroke-width="3"/>' % ROUGE)


def doublage():
    return _svg('Coupe : mur existant, isolant puis plaque de plâtre',
                '<rect x="70" y="30" width="90" height="180" fill="%s"/>' % ACIER
                + ''.join(_hachure(70, 160, 30, 210, y) for y in range(54, 300, 24))
                + '<rect x="160" y="30" width="110" height="180" fill="%s"/>' % ISOL
                + ''.join(_onde(166, 266, y, amp=6, pas=17, couleur='#C9B36B', ep=1.5) for y in range(48, 206, 20))
                + '<rect x="270" y="30" width="16" height="180" fill="%s" stroke="%s" stroke-width="2"/>' % (PLATRE, INK)
                + '<path d="M286 30v180" stroke="%s" stroke-width="3"/>' % ROUGE
                + _txt(115, 230, 'Mur', 'middle') + _txt(215, 230, 'Isolant', 'middle') + _txt(300, 230, 'Plaque'))


def sandwich():
    return _svg('Coupe : panneau sandwich, deux tôles et une âme isolante',
                '<rect x="50" y="62" width="300" height="12" fill="%s"/>' % GRIS
                + '<rect x="50" y="74" width="300" height="84" fill="%s"/>' % ISOL
                + _onde(60, 340, 100, amp=6, pas=20, couleur='#C9B36B', ep=2) + _onde(60, 340, 132, amp=6, pas=20, couleur='#C9B36B', ep=2)
                + '<rect x="50" y="158" width="300" height="12" fill="%s"/>' % GRIS
                + '<path class="sch-trait" d="M50 176h300" stroke="%s" stroke-width="3"/>' % ROUGE
                + _txt(200, 204, 'Tôle · âme isolante · tôle', 'middle', fill=INK))


# ---------------------------------------------------------------- plâtrerie et peinture
def platrerie():
    return _svg('Plaques de plâtre posées, joints traités',
                '<rect x="40" y="36" width="320" height="168" fill="%s"/>' % PLATRE
                + '<path d="M146 36v168M254 36v168" stroke="%s" stroke-width="3"/>' % LIGNE
                + ''.join('<circle cx="%d" cy="%d" r="2.5" fill="%s"/>' % (x, y, ACIER) for x in (54, 146, 254, 346) for y in (60, 120, 180))
                + '<path d="M146 36v168" stroke="%s" stroke-width="3" stroke-dasharray="12 10"/>' % ROUGE)


def enduit():
    return _svg('Enduit et lissage : la surface devient parfaitement plane',
                '<rect x="40" y="40" width="320" height="160" fill="%s"/><rect x="220" y="40" width="140" height="160" fill="#D9D5CE"/>' % PLATRE
                + '<g class="sch-outil"><path d="M196 92h70l-10 24h-50z" fill="%s"/><rect x="220" y="116" width="22" height="34" rx="3" fill="%s"/></g>' % (GRIS, INK)
                + '<path class="sch-trait" d="M40 200h180" stroke="%s" stroke-width="3"/>' % ROUGE)


def peinture():
    return _svg('Peinture intérieure au rouleau',
                '<rect x="40" y="40" width="320" height="160" fill="%s"/><rect x="40" y="40" width="200" height="160" fill="%s"/>' % (PLATRE, INK)
                + '<g class="sch-rouleau"><rect x="222" y="70" width="70" height="26" rx="6" fill="%s"/><path d="M257 96v30" stroke="%s" stroke-width="5"/>' % (ROUGE, GRIS)
                + '<rect x="249" y="126" width="16" height="44" rx="3" fill="%s"/></g>' % GRIS)


def finitions():
    return _svg('Trois finitions : mat, satiné, brillant',
                '<rect x="64" y="40" width="80" height="120" rx="4" fill="#CFCBC4"/><rect x="160" y="40" width="80" height="120" rx="4" fill="%s"/>' % GRIS
                + '<rect x="256" y="40" width="80" height="120" rx="4" fill="%s"/><path d="M176 56h30M272 56h44M272 68h26" stroke="#8C9198" stroke-width="5" stroke-linecap="round"/>' % INK
                + '<path class="sch-choix" d="M256 168h80" stroke="%s" stroke-width="3"/>' % ROUGE
                + _txt(104, 190, 'Mat', 'middle') + _txt(200, 190, 'Satiné', 'middle') + _txt(296, 190, 'Brillant', 'middle'))


def plan_espaces():
    return _svg('Plan : un bureau, une salle de réunion et un rangement créés par des cloisons',
                '<rect x="30" y="20" width="340" height="200" fill="%s" stroke="%s" stroke-width="6"/>' % (PLATRE, INK)
                + '<path class="sch-murs" pathLength="1" d="M150 20v120M150 170v50M150 112h90M270 112h100" stroke="%s" stroke-width="7"/>' % ROUGE
                + _txt(90, 124, 'Bureau', 'middle', size=15, fill=INK) + _txt(260, 72, 'Salle de réunion', 'middle', size=15, fill=INK)
                + _txt(260, 172, 'Rangement', 'middle', size=15, fill=INK), vb='0 0 400 240')
