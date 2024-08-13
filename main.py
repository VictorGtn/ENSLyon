import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
import igraph as ig
import plotly as py
from igraph import Graph


class Cellule:
    number = 0
    mutation = []
    right = None  # Mise en place de l'arborescence
    left = None

    def setNumber(self, i):
        self.number = i

    def setMutation(self, i, M):
        nbMut = random.randint(0, M)  # Ceci est le nombre de mutation que l'on va ajouter
        add = 0  # Compteur des mutations ajoutées
        newMut = random.randint(0, M)  # On choisit la mutation à ajouter
        while len(i) < M and add < nbMut:
            if newMut in i:  # Dans ce cas, la mutation est deja sur la cellule, on ne l'ajoute pas
                newMut = random.randint(0, M)
            else:  # Ici, nous avons une nouvelle mutation
                i.append(newMut)
                newMut = random.randint(0, M)
                add += 1
        mutation = i

        # Choix arbitraire de la loi, on peut la changer tant qu'elle est bornée.

accExpe = []
for l in range (100) :
    N = 25  # Population de départ des cellules
    tMax = 10  # Temps max de notre simulation
    M = 40  # Nombre max de mutation ajoutées

    nodes = 1
    edges = []
    state = [1 for j in range(0, N)]  # 1 pour survivante, -1 pour resistante,
    state = [0] + state  # On ajoute la racine
    color_dict = {1: "green", -1: "red", 0: "black"}

    S = [N]  # Liste du nombre de cellule survivante à chaque t
    S_C = [Cellule() for i in range(N)]  # Liste des cellules survivantes à chaque t
    for cel in S_C:
        cel.number = nodes
        edges.append([0, nodes])
        nodes += 1

    R = [0]  # Liste du nombre de cellules resistante à chaque t
    R_C = []  # liste des cellules resistantes a chaque t
    t = [0]  # temps

    Expe = []
    # Mise en place des taux, 0 représente les survivantes,1 les résistantes
    d0 = 0.7
    b0 = 0.2
    d1 = 0.1
    b1 = 0.7

    while t[-1] < tMax:
        # On commence par prendre la population a l'étape d'avant
        current_S = S[-1]
        current_R = R[-1]
        taux = [current_S * d0, current_S * b0, current_R * d1, current_R * b1]
        somme_taux = sum(taux)
        if somme_taux == 0:
            break
        print(somme_taux)

        tau = np.random.exponential(1 / somme_taux)
        t.append(t[-1] + tau)

        temp = []

        pof = random.uniform(0, 1)
        if pof * somme_taux < taux[0]:  # Cas ou une cellule survivante meurt
            celIndex = random.randint(0, S[-1] - 1)  # On choisit la cellule
            S_C.pop(celIndex)
            S.append(S[-1] - 1)
            R.append(R[-1])

        elif pof * somme_taux < taux[0] + taux[1]:  # Cas ou une cellule survivante se divise
            pif = random.uniform(0, 1)
            paf = random.uniform(0, 1)
            if pif <= 1 / N and paf <= 1 / N:  # Sous cas ou les deux nouvelles cellules sont résistantes
                celIndex = random.randint(0, S[-1] - 1)
                Res1 = Cellule()
                Res1.setMutation(S_C[celIndex].mutation, M)
                Res1.setNumber(nodes)
                edges.append([S_C[celIndex].number, nodes])
                nodes += 1
                state.append(-1)
                Res2 = Cellule()
                Res2.setMutation(S_C[celIndex].mutation, M)
                Res2.setNumber(nodes)
                edges.append([S_C[celIndex].number, nodes])
                nodes += 1
                state.append(-1)
                R_C.append(Res1)
                R_C.append(Res2)
                S_C[celIndex].left = Res1
                S_C[celIndex].right = Res2
                R.append(R[-1] + 2)
                S_C.pop(celIndex)
                S.append(S[-1] - 1)
            elif pif <= 1 / N < paf or paf <= 1 / N < pif:  # Sous cas ou qu'un des deux cellules ne devient résistantes
                celIndex = random.randint(0, S[-1] - 1)
                Res1 = Cellule()
                Res1.setMutation(S_C[celIndex].mutation, M)
                Res1.setNumber(nodes)
                edges.append([S_C[celIndex].number, nodes])
                nodes += 1
                state.append(-1)
                R_C.append(Res1)
                R.append(R[-1] + 1)
                Sur1 = Cellule()
                Sur1.setMutation(S_C[celIndex].mutation, M)
                Sur1.setNumber(nodes)
                edges.append([S_C[celIndex].number, nodes])
                nodes += 1
                state.append(1)
                S_C[celIndex].left = Res1
                S_C[celIndex].right = Sur1
                S_C.pop(celIndex)
                S_C.append(Sur1)
                S.append(S[-1])
            elif pif > 1 / N and paf > 1 / N:  # Sous cas ou les deux nouvelles cellules sont survivantes
                celIndex = random.randint(0, S[-1] - 1)
                R.append(R[-1])
                Sur1 = Cellule()
                Sur1.setMutation(S_C[celIndex].mutation, M)
                Sur1.setNumber(nodes)
                edges.append([S_C[celIndex].number, nodes])
                nodes += 1
                state.append(1)
                Sur2 = Cellule()
                Sur2.setMutation(S_C[celIndex].mutation, M)
                Sur2.setNumber(nodes)
                edges.append([S_C[celIndex].number, nodes])
                nodes += 1
                state.append(1)
                S_C[celIndex].left = Sur1
                S_C[celIndex].right = Sur2
                S_C.pop(celIndex)
                S_C.append(Sur1)
                S_C.append(Sur2)
                S.append(S[-1] + 1)
        elif pof * somme_taux < taux[0] + taux[1] + taux[2]:  # Cas ou une cellule Resistante meurt
            celIndex = random.randint(0, R[-1] - 1)
            R_C.pop(celIndex)
            R.append(R[-1] - 1)
            S.append(S[-1])
        elif pof * somme_taux <= taux[0] + taux[1] + taux[2] + taux[3]:  # Cas ou une cellule résistante se divise
            celIndex = random.randint(0, R[-1] - 1)
            Res1 = Cellule()
            Res1.setMutation(R_C[celIndex].mutation, M)
            Res1.setNumber(nodes)
            edges.append([R_C[celIndex].number, nodes])
            nodes += 1
            state.append(-1)
            Res2 = Cellule()
            Res2.setMutation(R_C[celIndex].mutation, M)
            Res2.setNumber(nodes)
            edges.append([R_C[celIndex].number, nodes])
            nodes += 1
            state.append(-1)
            R_C[celIndex].left = Res1
            R_C[celIndex].right = Res2
            R_C.pop(celIndex)
            R_C.append(Res1)
            R_C.append(Res2)
            R.append(R[-1] + 1)
            S.append(S[-1])

        # On passe au Si(t), on ne vas que les calculer a t = Tmax, trop de calcul sinon.

    if R[-1] != 0:
        for h in range(1, R[-1] + 1):
            takenCel = []
            mutation_i = []
            j = 0
            indexCel = random.randint(0, R[-1] - 1)
            while indexCel not in takenCel and j < h:
                j += 1
                takenCel.append(indexCel)
                mutation_i = list(set(mutation_i + R_C[indexCel].mutation))  # Méthode pour ne pas avoir de doublons
            Expe.append(len(mutation_i))
    print(Expe)
    accExpe.append(Expe)
    """Mise en commentaire des graphes pour le calcul des moyennes etc"""
    """print("temps " + str(t[-1]))

    g = Graph(n=nodes, edges=edges, directed=True)
    g.vs["state"] = state
    g.vs["color"] = [color_dict[st] for st in g.vs["state"]]

    layout = g.layout_reingold_tilford_circular()
    visual_style = {"vertex_size": 10, "layout": layout, "bbox": (3000, 2000), "hovering": 'closest'}
    ig.plot(g, **visual_style)

    plt.plot(t, S, label='Survivantes')
    plt.plot(t, R, label='Resistantes')
    plt.legend()
    plt.show()"""
