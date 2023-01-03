import networkx as nx
import time
import os
from math import ceil

class BnB:
    algo = 'BnB'
    def read_file(filename):
        G_list = []
        with open(filename) as f:
            V, E, _ = map(int, f.readline().split())
            for i in range(V):
                G_list.append(map(int, f.readline().split()))
                
        G = nx.Graph()
        for node in range(len(G_list)):
            for neighbor in G_list[node]:
                G.add_edge(node+1, neighbor)
        
        return G, G_list, V, E

    def write_file(filename, algo, cutoff, seed, MVC, trace):
        # write the solution and trace files
        folder='./output/'
        sol_file_name = filename + "_" + "BnB" +"_"+ str(int(cutoff))+ ".sol"
        trace_file_name = filename + "_" + "BnB" +"_"+ str(int(cutoff))+ ".trace"
        sol_file = os.path.join(folder, sol_file_name)
        trace_file = os.path.join(folder, trace_file_name)
        
        with open(sol_file, 'w') as f_sol:
            f_sol.write(str(len(MVC)) + "\n") # print the best quality
            for node in MVC[:-1]: # print all nodes in the vertex cover
                f_sol.write(str(node) + ",")
            f_sol.write(str(MVC[-1]))
    
        with open(trace_file, 'w') as f_trace:
            for time, number in trace:
                f_trace.write(str(time)+","+str(number)+"\n")
    
    
    def find_max_degree(G):
        degree_sorted = sorted(G.degree, key=lambda x: x[1], reverse=True)
        return degree_sorted[0] # return the node with max degree
    
    def LB(G):
        return ceil(G.number_of_edges()/BnB.find_max_degree(G)[1])
    
    def set_size(vert_set):
        # to compute the size of current vertex set
        size = 0
        for node in vert_set:
            size += node[1]
        return size
    
    def Method(G,cutoff):
        # initialize timer
        start_time = time.time()
        trace = []
        
        # initialize sets used for BnB
        solution = []
        best = []
        frontier = []
        neighbor = []
        UB = G.number_of_nodes()

        # frontier format: node, state(include or not), (parent_node, parent_state)
        G_prim = G.copy()
        v_max_d = BnB.find_max_degree(G_prim)[0]
        # add initial configurations
        frontier.append((v_max_d, 0, (-1, -1))) # include the first node
        frontier.append((v_max_d, 1, (-1, -1))) # exclude the first node

        while frontier != [] and time.time() - start_time <= cutoff:
            backtrack = False
            # choose the most promising node:
            (node, state, parent) = frontier.pop()
            # if the node is not selected
            if state == 0:
                for temp_neighbor in list(G_prim.neighbors(node)):
                    # store neighbors of current node
                    best.append((temp_neighbor, 1))
                    G_prim.remove_node(temp_neighbor)
            # if the node is selected
            elif state == 1:
                G_prim.remove_node(node)
            else:
                pass
            best.append((node, state))
            best_size = BnB.set_size(best)
            
            # 3 possible outputs
            if G_prim.number_of_edges() == 0:
                # solution found
                backtrack = True
                if best_size < UB:
                # update UB and best solution
                    solution = best.copy()
                    UB = best_size
                    print('Current best size: ', best_size)
                    trace.append([time.time() - start_time, best_size])
            elif BnB.LB(G_prim) + best_size < UB:
                # continue to next level branches
                node_promising = BnB.find_max_degree(G_prim)[0]
                # append two configurations
                frontier.append((node_promising, 0, (node, state)))
                frontier.append((node_promising, 1, (node, state)))
            else:
                # prune
                backtrack = True
                    
            if backtrack and frontier != []:
                next_parent = frontier[-1][2]
                if next_parent in best:
                    while best.index(next_parent) < len(best)-1:
                        node_temp, _ = best.pop()
                        G_prim.add_node(node_temp)
                        current = list(map(lambda x:x[0], best))
                        for nb in G.neighbors(node_temp):
                            # add back edges
                            if (nb not in current) and (nb in G_prim.nodes()):
                                G_prim.add_edge(nb, node_temp)
                else:
                    # backtrack to the root
                    best.clear()
                    G_prim = G.copy()
                    
            if time.time() - start_time > cutoff:
                print('Cutoff time reached.')
                
        return solution, trace
    
def main(inst, seed, cutoff):
    # create graph
    inst_name='./DATA/'+inst+'.graph'
    G, G_list, V, E = BnB.read_file(inst_name)

    # run BnB
    nodes, trace_time = BnB.Method(G, cutoff)
    for temp in nodes:
        if temp[1] == 0:
            nodes.remove(temp)

    vertex_cover = []
    for v, d in nodes:
        vertex_cover.append(v)
        
    # output to files
    BnB.write_file(inst, '_BnB_', cutoff, seed, vertex_cover, trace_time)
