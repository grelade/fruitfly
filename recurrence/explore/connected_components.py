import numpy as np
import networkx as nx
from scipy.sparse import load_npz

import matplotlib.pyplot as plt

import sys

if len(sys.argv)<3:
    print('Usage: python connected_components.py ROI THRESHOLD')
    print('THRESHOLD = 1,2,3...')
    quit()

roi = sys.argv[1]
threshold = int(sys.argv[2])

print('roi', roi)
print('threshold', threshold)
print()

adj = load_npz('../processed/adjacency_{}.npz'.format(roi))

# change to a regular numpy matrix
adj = np.array(adj.todense())

adj[adj<threshold] = 0

# make an unordered graph

Aorg = np.zeros_like(adj)
Aorg[adj>0] = 1
G = nx.from_numpy_array(Aorg, create_using=nx.Graph)

# components in original graph

components = [G.subgraph(c) for c in nx.connected_components(G)]
n_comp = len(components)
print('connected components of the original graph', n_comp)
print()

for i in range(n_comp):
    nodesi = list(components[i].nodes)
    edges = components[i].number_of_edges()
    print('component {} nodes {} edges {:}'.format(i, len(nodesi), edges))
print()
