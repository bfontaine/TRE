# -*- coding: UTF-8 -*-

# use this script on the server
# it generates two CSS files for the French departements SVG found here:
#   https://commons.wikimedia.org/wiki/File:D%C3%A9partements_de_France-simple.svg
# (public domain)
# one for the CSA dataset, one for the non-CSA one

import math
from algopol import db

def count(dep, coll, csa=False):
    cursor = coll.find({'csa':csa, 'ego_postalcode':{'$regex':'^%02d' % dep}})
    return cursor.count()


def color(value, max_value):
    p = math.log(value, max_value)*100 if value > 0 else 0
    if p == 0:
        return '#fff'
    if p <= 20:
        return '#ffffcc'
    if p <= 40:
        return '#c2e699'
    if p<= 60:
        return '#78c679'
    if p<= 80:
        return '#31a354'
    return '#006837'


def css(dep, value, max_value):
    code = '%02d' % dep if isinstance(dep, int) else dep
    return '.departement%s { fill: %s }' % (code, color(value, max_value))


if __name__ == '__main__':
    coll = db.get_coll(db.Ego)

    departements = list(range(1, 96)) # we don't count DOM-TOM (97*)

    for csa in (True, False):
        name = 'france-departements%s-svg.css' % ('-csa' if csa else '')

        counts = [count(dep, coll, csa=csa) for dep in departements]
        mx = max(counts)

        with open(name, 'w') as f:
            for dep, value in zip(departements, counts):
                if dep == 20: # Corse
                    f.write('%s\n' % css('2a', value, mx))
                    f.write('%s\n' % css('2b', value, mx))
                else:
                    f.write('%s\n' % css(dep, value, mx))
