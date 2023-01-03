#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 14:26:28 2022
@author: tj_hou
"""

#!/usr/bin/python
# CSE6140 Project LS1

import time
import networkx as nx
import random
import numpy as np

class LS1:

    def parse_edges(filename):
        # Write this function to parse edges from graph file to create your graph object
        g = nx.Graph()
        with open(filename, 'r') as file:
            v,e,w= list(map(lambda x: int(x), file.readline().split()))
            i=1
            for line in file:
                # parse each vertex and its neighbours vertices
                adjacency_data = list(map(lambda x: int(x), line.split()))
                for j in adjacency_data:
                    g.add_edge(i, j)
                i=i+1
        return g,v,e
        pass

    def initial_solution(G):
        sol = list(G.nodes())
        VC=sorted(G.degree, key=lambda x: x[1]) 
        i=0
        while(i < len(VC)):
            flag=True
            for x in G.neighbors(VC[i][0]):
                if x not in sol:
                    flag = False
            if flag:
                sol.remove(VC[i][0])
            i=i+1
        return sol
        pass
    
    # simulated annealing
    def simulated_annealing(G, cutoff, V, seed, output):
        
        start_time = time.time()
        random.seed(seed)
        sol=LS1.initial_solution(G)
        update_sol=sol.copy()
        uncover_edges=[]
        temp = 0.3
        
        while ((time.time() - start_time) < cutoff):
            
            temp = 0.95 * temp 
            count = 0
            
            while (count < (V - len(sol)-1)**2):
                
                count += 1
                           
                if ((time.time() - start_time) < cutoff):
                    
                    #given a vc, continue to remove vertex until it's not a vc
                    while not uncover_edges:
                        update_sol = sol.copy()
                        #print(len(update_sol))
                        output.write(str(time.time()-start_time) + "," + str(len(update_sol)) + "\n")
                        delete = random.choice(sol)
                        for i in G.neighbors(delete):
                            if i not in sol:
                                uncover_edges.append((i,delete))
                                uncover_edges.append((delete,i))
                        sol.remove(delete)                   
                            
                    # Record current soltuion, cost
                    sol_curr=sol.copy()
                    uncover_curr=uncover_edges.copy()
                    cost_curr=len(uncover_curr)
                    
                    # Randomly select an exiting vertex
                    delete = random.choice(sol)
                    for i in G.neighbors(delete):
                        if i not in sol:
                            uncover_edges.append((i,delete))
                            uncover_edges.append((delete,i))            
                    sol.remove(delete)    
    
                    # Randomly select an entering vertex
                    tmp = random.choice(uncover_edges)
                    if tmp[0] in sol: 
                        add = tmp[1]
                    else:
                        add = tmp[0]                
                    for i in G.neighbors(add):
                        if i not in sol:
                            uncover_edges.remove((add,i))
                            uncover_edges.remove((i,add))
                    sol.append(add)
    
                    # Record new solution, cost
                    sol_next=sol.copy()
                    uncover_next=uncover_edges.copy()
                    cost_next = len(uncover_next)
                    
                    # Update solution, cost
                    if cost_curr < cost_next:    
                        p = np.exp(float(cost_curr - cost_next)/float(temp))
                        num = random.uniform(0,1)
                        if p>num:
                            sol = sol_next.copy()
                            uncover_edges = uncover_next.copy()
                        else:
                            sol = sol_curr.copy()
                            uncover_edges = uncover_curr.copy()
                    else:
                        sol = sol_next.copy()
                        uncover_edges = uncover_next.copy()
                                               
        return update_sol                           
        pass

def main(instance,randseed,cutoff):
    
    solution_file = "./output/" + instance + "_LS1_" + str(int(cutoff)) + "_" + str(randseed) + ".sol"   
    trace_file = "./output/" + instance + "_LS1_" + str(int(cutoff)) + "_" + str(randseed) + ".trace"
    output1 = open(solution_file, 'w')
    output2 = open(trace_file, 'w')

    filename = "./DATA/"+instance+".graph"
    G,V,E = LS1.parse_edges(filename)

    init_sol=LS1.initial_solution(G)
    print('Initial Solution:' + str(len(init_sol)))
    sol = LS1.simulated_annealing(G,cutoff,V,int(randseed),output2)
    print('LS1 Solution:' + str(len(sol)))

    output1 = open(solution_file, 'w')
    output1.write(str(len(sol)) + '\n')

    for i in sol:
        if i==sol[0]:
            output1.write(str(i))
        else:
            output1.write(','+str(i))



