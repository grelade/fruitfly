import numpy as np
import networkx as nx
from scipy.sparse import load_npz

from optimize_ordering import optimize

import sys

if len(sys.argv)<4:
    print('Usage: python make_raw_ordering.py ROI THRESHOLD SEED [|wiring|weights]')
    print('An additional optional argument "wiring" or "weights" randomizes the graph')
    print('In that case the result is not saved')
    quit()

roi = sys.argv[1]
threshold = int(sys.argv[2])
seed = int(sys.argv[3])

wiring = False
weights =False
if len(sys.argv)==5 and sys.argv[4]=='wiring':
    wiring = True
if len(sys.argv)==5 and sys.argv[4]=='weights':
    weights = True

print('roi', roi)
print('threshold', threshold, '(smaller weights will be eliminated)')
print('seed', seed)
print()

adj = load_npz('../processed/adjacency_{}.npz'.format(roi))

# change to a regular numpy matrix
adj = np.array(adj.todense())

adj[adj<threshold] = 0

# find largest connected component

H = nx.from_numpy_array(adj, create_using=nx.DiGraph)

components = [H.subgraph(c) for c in nx.weakly_connected_components(H)]

n_comp = len(components)
print('connected components in thresholded graph', n_comp)

size = 0
j = 0
for i in range(n_comp):
    nodesi = list(components[i].nodes)
    if len(nodesi)>size:
        size = len(nodesi)
        j = i
    #print('component {} nodes {}'.format(i, len(nodesi)))

print('largest component', size, 'nodes')

nodes = list(components[j].nodes)

# restrict to the largest component

adj = adj[nodes, :][:, nodes]

# optionally randomize

if wiring:
    print('randomizing wiring!')
    np.random.seed(seed)
    perm = np.random.permutation(len(adj))
    adj = adj[:, perm]

if weights:
    print('randomizing weights!')
    np.random.seed(seed)
    nonz = np.nonzero(adj)
    nonzero_weights = adj[nonz]
    np.random.shuffle(nonzero_weights)
    adj[nonz] = nonzero_weights


# optimize

ind = optimize(adj, seed)

if weights or wiring:
    quit()

fname = '../processed/ordering_{}_raw_T{}_S{}.npz'.format(roi, threshold, seed)
print('saving ordering to', fname)
np.savez_compressed(fname, ind)

