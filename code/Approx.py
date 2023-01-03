# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 19:14:36 2022

@author: Wendy
"""
# This method is MVC_Approximation 
import networkx as nx
import os
from time import process_time
import random
         
    
class Approx:   
    
    def parse_file(data):
        #read data in graph
        graph = []
        # create dictionary with key as node, value as node's neighbors
        neighbors = dict()
        # create dictionary with key as node, value as node's degree
        Degrees=dict()
        
        with open(data) as f:
            v, e, w=map(lambda x: int(x), f.readline().split())
            for i in range(v):
                graph.append(map(lambda x: int(x), f.readline().split()))
        #created graph in networkx
        Graph = nx.Graph()
        for i in range(len(graph)):
            for j in graph[i]:
                Graph.add_edge(i + 1, j)
                
        #create a dic which key as node,value as its neighbors
        g = open(data, mode='r', encoding="utf-8").readlines()
        for i in range(1, len(g)):
            neighbor = [int(x) for x in g[i].strip().split()]

        # since there are some verteces without edge
            if len(neighbor) == 0:
                continue
            neighbors[i] = set()
            neighbors[i].update(neighbor)
            
        #create a dic which key as node,value as its degree   
        for i in neighbors.keys():
            Degrees[i]=Graph.degree[i]
            
        return neighbors,Graph,Degrees,e
    
    
    def MVC_Approx(neighbors,Graph,Degrees,e,cutoff,randomseed):
        random.seed(randomseed)
        start=process_time()
        # we use Maximum Degree Greedy algorithm from the paper written by Fran¸cois Delbot and Christian Laforest
        sol = set()
        # create trace file
        #trace=[]
         #a recoreds how many node has been added during the process
        #a=0
         #b records time for each node is added
        #b=0
        while (e > 0) and ((process_time()-start)<cutoff):
            #starttime=process_time()
            # update max degree node
            max_node = sorted(Degrees, key=Degrees.get,reverse=True)[0]
            for n in neighbors[max_node]:
                if n not in sol:
                    # if neighbor is not in mvc, but the edge will be removed, so its degree also decrease 1
                    Degrees[n] = Degrees[n]-1
            # total edege length minus the deleted edges
            e = e- Degrees[max_node]
            #remove the max degree node from dic
            del Degrees[max_node]
            #add the node to mvc
            sol.add(max_node)
            #endtime=process_time()
            #a +=1
            #b +=endtime - starttime
            #c is used for trace file
            #c=str(b)+","+str(a)
            #trace.append(c)
        
        return sol
            
    def write_output(name,mvc,cutoff,timecost):
        folder='./output/'
        file_name = name.replace('.graph','') + "_" + "Approx" +"_"+ str(int(cutoff))
    
        path = os.path.join(folder, file_name)
        #write to solution file
        with open(path + ".sol", mode='w', encoding="utf-8") as f1:
            f1.write(str(len(mvc)) + "\n" + str(mvc).replace("{","").replace("}", ""))
        #write to trace file
        with open(path + ".trace", mode='w', encoding="utf-8") as f:
            f.write(str(timecost)+","+str(len(mvc)))
    
     
                
def main(instance,randomseed,cutoff):
    #read data
    filename='./DATA/'+instance+".graph"
    # build graph
    neighbors,Graph,Degrees,e= Approx.parse_file(filename)
    #print(neighbors)
    start = process_time()
    mvc= Approx.MVC_Approx(neighbors,Graph,Degrees,e,cutoff,randomseed)
    end = process_time()
    timecost = end-start
    #write solution and trace files
    Approx.write_output(instance+".graph", mvc,cutoff,timecost)
    #print(f'file:{instance+".graph"},mvc: {len(mvc)},time: {timecost:0.5f}s')
                   


#main("star2",123,100)