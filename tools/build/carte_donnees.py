# -*- coding: utf-8 -*-
"""Prépare les données de la carte « Zone d'intervention » (à lancer une seule fois, réseau requis).

Source : paquet npm « swiss-maps » 4.7.0 (Interactive Things, licence BSD), qui reprend les
limites officielles de swisstopo / OFS (millésime 2024), au format TopoJSON (WGS 84).

    python3 tools/build/carte_donnees.py

Écrit tools/build/data/suisse-occidentale.json : arcs décodés (lon/lat) limités à la Suisse
occidentale, cantons, districts utiles (Jura bernois, Valais romand), lacs et frontière nationale.
Le générateur (carte.py) ne dépend ensuite d'aucun accès réseau.
"""
import json, os, subprocess, tarfile, tempfile, shutil

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, 'data', 'suisse-occidentale.json')
VERSION = 'swiss-maps@4.7.0'
ANNEE = '2024'

# Emprise conservée (lon/lat) : Suisse occidentale et abords
EMPRISE = (5.80, 45.75, 8.40, 47.65)
# Districts OFS : 241 = Jura bernois ; Valais romand = Conthey, Entremont, Hérens, Martigny,
# Monthey, Saint-Maurice, Sierre, Sion
DISTRICTS = [241, 2302, 2303, 2305, 2307, 2308, 2310, 2311, 2312]


def telecharger():
    tmp = tempfile.mkdtemp()
    subprocess.run(['npm', 'pack', VERSION, '--silent'], cwd=tmp, check=True, capture_output=True)
    tgz = [f for f in os.listdir(tmp) if f.endswith('.tgz')][0]
    with tarfile.open(os.path.join(tmp, tgz)) as t:
        t.extractall(tmp)
    return tmp


def main():
    tmp = telecharger()
    try:
        topo = json.load(open(os.path.join(tmp, 'package', ANNEE, 'ch-combined.json'), encoding='utf-8'))
        licence = open(os.path.join(tmp, 'package', 'LICENSE'), encoding='utf-8').read()
    finally:
        shutil.rmtree(tmp)
    (sx, sy), (tx, ty) = topo['transform']['scale'], topo['transform']['translate']

    def decode(arc):
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx; y += dy
            pts.append((round(x * sx + tx, 5), round(y * sy + ty, 5)))
        return pts

    arcs = [decode(a) for a in topo['arcs']]

    def anneaux(geom):
        if geom['type'] == 'Polygon':
            return [geom['arcs']]
        if geom['type'] == 'MultiPolygon':
            return geom['arcs']
        return []

    def dans_emprise(polys):
        for poly in polys:
            for ring in poly:
                for i in ring:
                    for lon, lat in arcs[i if i >= 0 else ~i]:
                        if EMPRISE[0] <= lon <= EMPRISE[2] and EMPRISE[1] <= lat <= EMPRISE[3]:
                            return True
        return False

    garde, objets = set(), {}
    for nom, filtre in [('cantons', None), ('districts', DISTRICTS), ('lakes', None), ('country', None)]:
        objets[nom] = []
        for g in topo['objects'][nom]['geometries']:
            if filtre is not None and int(g.get('id', 0)) not in filtre:
                continue
            polys = anneaux(g)
            if not polys or not dans_emprise(polys):
                continue
            objets[nom].append({'id': g.get('id'), 'polys': polys})
            for poly in polys:
                for ring in poly:
                    garde.update(i if i >= 0 else ~i for i in ring)
    # renumérotation compacte des arcs
    ordre = sorted(garde)
    nouv = {a: n for n, a in enumerate(ordre)}
    remap = lambda i: nouv[i] if i >= 0 else ~nouv[~i]
    for liste in objets.values():
        for o in liste:
            o['polys'] = [[[remap(i) for i in ring] for ring in poly] for poly in o['polys']]
    data = {'source': VERSION + ' (' + ANNEE + '), limites swisstopo / OFS', 'emprise': EMPRISE,
            'arcs': [arcs[a] for a in ordre], 'objets': objets}
    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    json.dump(data, open(SORTIE, 'w', encoding='utf-8'), separators=(',', ':'))
    open(os.path.join(ICI, 'data', 'LICENSE-swiss-maps.txt'), 'w', encoding='utf-8').write(licence)
    print('écrit', SORTIE, os.path.getsize(SORTIE), 'octets,', len(ordre), 'arcs')


if __name__ == '__main__':
    main()
