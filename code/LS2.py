# !/usr/bin/python
# CSE6140 Project LS2

import pandas as pd
import numpy as np
import math
import os
from os import listdir
from os.path import isfile, join
import networkx as nx
import time
import random


# !/usr/bin/python
# CSE6140 Project LS2

class LS2:

    def read_graph(filename):  # checked
        # Read in Graph
        G = nx.Graph()
        with open(filename, 'r') as f:
            V, E, _ = f.readline().strip('\n').split(' ')
            i = 0
            for line in f.readlines():
                i += 1
                v_adjacencies = [int(x) for x in line.strip('\n').split(' ') if x != '']

                for v in v_adjacencies:
                    # EWCC initializes all edge weights to 1
                    G.add_edge(i, v, weight=1)
        return G, int(V), int(E)
        pass

    def candidate_solution(G):  # checked
        allVertexs = list(G.nodes())
        degree_rank = [[v, G.degree[v]] for v in allVertexs]
        degree_rank.sort(key=lambda x: x[1])
        VC_initial = allVertexs.copy()
        i = 0
        while i < len(allVertexs):
            isVC = True
            for x in G.neighbors(degree_rank[i][0]):
                if x not in VC_initial:
                    isVC = False
            if isVC:
                VC_initial.remove(degree_rank[i][0])
            i += 1
        return VC_initial, degree_rank
        pass

    def cost(G, C):  # checked
        cost = 0
        Uncovered_Vertex = set(G.nodes()).difference(C)
        for v in Uncovered_Vertex:
            for u in G.neighbors(v):
                if u not in C:
                    cost += G.edges[u, v]['weight']
        return cost
        pass

    def dscore(G, C, v):  # checked
        C = set(C)
        C_temp = C.copy()
        if v in C:
            C_temp.remove(v)
            discore_v = LS2.cost(G, C) - LS2.cost(G, C_temp)
        else:
            C_temp.add(v)
            discore_v = LS2.cost(G, C) - LS2.cost(G, C_temp)
        return discore_v
        pass

    def get_highest_dscore_v(C, dscores):
        C = sorted(list(C))
        dscores_candidate = [dscores[c] for c in C]
        v_max = C[np.argmax(dscores_candidate)]
        C = set(C)
        return v_max
        pass

    def update_vertex(G, C, confChange, dscores, edge_weights, v, action):
        dscores[v] = -dscores[v]
        endpoints = list(G.neighbors(v))
        not_in_C = [e for e in endpoints if e not in C]
        in_C = [e for e in endpoints if e in C]
        for x in not_in_C:
            if action == "add":
                confChange[x] = 1
                dscores[x] -= edge_weights[v][x]
            elif action == "remove":
                confChange[v] = 0
                confChange[x] = 1
                dscores[x] += edge_weights[v][x]
        for x in in_C:
            if action == "add":
                dscores[x] += edge_weights[v][x]
            elif action == "remove":
                dscores[x] -= edge_weights[v][x]
        return dscores, confChange
        pass

    def update_edges(G, C, uncovered_edges, v, action):
        endpoints = list(G.neighbors(v))
        not_in_C = [e for e in endpoints if e not in C]
        for x in not_in_C:
            if action == "add":
                uncovered_edges.remove((v, x))
                uncovered_edges.remove((x, v))
            elif action == "remove":
                uncovered_edges.append((v, x))
                uncovered_edges.append((x, v))
        return uncovered_edges
        pass

    def GetSwapPair(G, C, dscores, uncovered_edges, confChange):
        v_to_remove = LS2.get_highest_dscore_v(C, dscores)
        random_e = random.choice(uncovered_edges)
        u1, u2 = random_e[0], random_e[1]
        # using configuration change to avoid cycling problem
        if confChange[u1] == 0 and u2 not in C:
            v_to_add = u2
        elif confChange[u2] == 0 and u1 not in C:
            v_to_add = u1
        else:
            v_to_add = LS2.get_highest_dscore_v([u1, u2], dscores)
        return v_to_remove, v_to_add
        pass

    def EWCC(G, V, E, C, cutoff, randseed, trace):
        random.seed(randseed)

        edge_weights = nx.convert.to_dict_of_dicts(G, edge_data=1)
        # EWCC initializes all state to 1
        confChange = [1] * (V + 1)
        dscores = [0]
        for i in range(1, V + 1):
            dscores.append(LS2.dscore(G, C, i))
        uncovered_edges = []

        start_time = time.time()
        VC_final = C.copy()
        opt_VC_len = len(C)
        trace.append((opt_VC_len, time.time() - start_time))

        while time.time() - start_time < cutoff:
            while not uncovered_edges:
                if opt_VC_len > len(C):
                    trace.append((opt_VC_len, time.time() - start_time))
                    VC_final = C.copy()
                    opt_VC_len = len(C)
                v_to_remove = LS2.get_highest_dscore_v(C, dscores)
                C.remove(v_to_remove)
                dscores, confChange = LS2.update_vertex(G, C, confChange, dscores, edge_weights, v_to_remove, 'remove')
                uncovered_edges = LS2.update_edges(G, C, uncovered_edges, v_to_remove, 'remove')

            # Swap (u,v) where u in C and v not in c
            v_to_remove, v_to_add = LS2.GetSwapPair(G, C, dscores, uncovered_edges, confChange)

            C.remove(v_to_remove)
            dscores, confChange = LS2.update_vertex(G, C, confChange, dscores, edge_weights, v_to_remove, 'remove')
            uncovered_edges = LS2.update_edges(G, C, uncovered_edges, v_to_remove, 'remove')

            C.append(v_to_add)
            dscores, confChange = LS2.update_vertex(G, C, confChange, dscores, edge_weights, v_to_add, 'add')
            uncovered_edges = LS2.update_edges(G, C, uncovered_edges, v_to_add, 'add')

            # Update weights for uncovered edges
            for v in uncovered_edges:
                edge_weights[v[1]][v[0]] += 1
                dscores[v[0]] += 1

        return VC_final, trace
        pass


def main(instance, randseed, cutoff):
    solution_file = "./output/" + instance + "_LS2_" + str(int(cutoff)) + "_" + str(randseed) + ".sol"
    trace_file = "./output/" + instance + "_LS2_" + str(int(cutoff)) + "_" + str(randseed) + ".trace"
    file_name = "./DATA/" + instance + ".graph"

    G, V, E = LS2.read_graph(file_name)
    VC_initial, degree_rank = LS2.candidate_solution(G)
    print('Initial Solution:' + str(len(VC_initial)))
    trace_output = []
    VC_final, trace_output = LS2.EWCC(G, V, E, VC_initial, cutoff, randseed, trace_output)
    print('LS2 Solution:' + str(len(VC_final)))

    output1 = open(solution_file, 'w')
    output1.write(str(len(VC_final)) + '\n')

    for i in VC_final:
        if i == VC_final[0]:
            output1.write(str(i))
        else:
            output1.write(',' + str(i))

    output2 = open(trace_file, 'w')
    for j in trace_output:
        output2.write(f"{j}\n")
