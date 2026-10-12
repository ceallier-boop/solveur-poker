"""Modèles de valeur des fins de tour « flop » (au moins deux joueurs avec des jetons derrière).

Showdown : chaque joueur réalise exactement son équité préflop sur le pot (aucune mise après le flop).
C'est le modèle le plus simple ; il ignore la position et la jouabilité. Les autres modèles l'affinent.
"""


class Showdown:
    name = 'showdown'

    def value(self, solver, nd, p, reach):
        return solver.showdown_value(nd, p, reach)
