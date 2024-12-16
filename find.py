import networkx as nx
import itertools
import numpy as np
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import os
import pickle

def get_subgraphs(parent_graph):
    subgraph_list=[]
    # Generate all possible node combinations of the same size as the subgraph
    for subgraph_size in range(2,len(parent_graph.nodes())+1):
        # print(subgraph_size)
        for node_collection in itertools.combinations(parent_graph.nodes(), subgraph_size):
            induced_subgraph = parent_graph.subgraph(node_collection).copy()
            count_single=0
            count_double=0
            for u, v, ed in induced_subgraph.edges(data=True):
                if len(ed)!= 0:
                    if 'type1' in ed['type'] and 'type2' in ed['type']:
                        count_double +=1
                    else:
                        count_single +=1
            subgraph_list.append((subgraph_size, count_single, count_double))
    return list(set(subgraph_list))

def get_intersection(subgraph_list, verbose = False):
    vertex_list = [(0,0)]
    min_y_intercept = 2.1
    minimizer_list = []
    best_minimizer = None
    for (v, s, d) in subgraph_list:
        if d!=0 and min_y_intercept > v/d:
            min_y_intercept = v/d
            best_minimizer = (v,s,d)
    if best_minimizer is None:
        return minimizer_list, vertex_list
    minimizer_list.append(best_minimizer)
    vertex_list.append((0,min_y_intercept))
    alpha = 0
    flag = True
    # print(vertex_list)
    
    while(flag):
        min_alpha_increment = 1
        v,s,d = minimizer_list[-1]
        slope = s/d if d!=0 else np.inf
        best_minimizer = None
        best_slope = slope
        for (v1,s1,d1) in subgraph_list:
            if s1*d-s*d1 != 0 and d1!=0:
                temp = (v1*d-v*d1)/(s1*d-s*d1)
                new_slope = s1/d1 if d1!=0 else np.inf 
                
                if verbose: print(f"prev_slope={slope}, slope={new_slope}, incre = {temp}, (vsd)=({v1,s1,d1})")
                # print(temp)
                if temp>0 and temp<min_alpha_increment and new_slope>slope:
                    min_alpha_increment = temp
                    best_minimizer = (v1,s1,d1)
                    best_slope = new_slope
                elif temp>0 and temp==min_alpha_increment and new_slope>best_slope:
                    best_minimizer = (v1,s1,d1)
                    best_slope = new_slope
        

        # if count==3: break
        alpha = min_alpha_increment
        # print(min_alpha_increment)
        beta = (v-alpha*s)/d
        if verbose: print(f"new alpha = {alpha}, new_beta={beta}")
        if alpha < beta:
            minimizer_list.append(best_minimizer)
            vertex_list.append((alpha, beta))
        elif alpha >= beta:
            vertex_list.append((v/(s+d), v/(s+d)))
            flag = False
        elif alpha>1:
            vertex_list.append((1,2))
            vertex_list.append((1,1))
        
        # print(minimizer_list)
        
        # print(alpha)
    return minimizer_list, vertex_list



if __name__ == "__main__":
    etype = ['no_edge', ['type1'],['type1', 'type2']]
    arr = {}
    while(True):
        N = np.random.choice(range(20,41))
        p_ = np.random.uniform(0,1) 
        flag = True
        while flag:
            q_ = np.random.uniform(0,p_)
            if p_+q_<1:
                flag = False
    
        edges = []
        for i in range(N):
            for j in range(i+1,N):
                choice_ = np.random.choice(range(3), p = [1-p_-q_, p_, q_])
                if etype[choice_] == 'no_edge':
                    continue
                edges.append((i,j, {'type':etype[choice_]}))
        parent = nx.Graph()
        parent.add_edges_from(edges)

        subgraphs = get_subgraphs(parent)
        _, vertices = get_intersection(subgraphs)
        num_vertices = len(vertices)
        if num_vertices>8 and num_vertices not in arr.keys():
            arr[num_vertices] = [edges.copy()]
        elif num_vertices>8:
            arr[num_vertices].append(edges.copy())
        
        with open("data.pkl", "wb") as fp:
            pickle.dump(arr, fp)

