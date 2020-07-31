import numpy as np
import networkx as nx
from scipy.sparse import load_npz
from time import time
import sys


if len(sys.argv)<4:
    print('Usage: python graph_analysis ROI THRESHOLD SEED')
    quit()

roi = sys.argv[1]
threshold = int(sys.argv[2])
seed = int(sys.argv[3])

fname = '../processed/ordering_{}_fix_T{}_S{}.npz'.format(roi, threshold, seed)

print('roi:', roi)
print('threshold', threshold)
print('seed', seed)
print('ordering file:', fname)
print()

adj = load_npz('../processed/adjacency_{}.npz'.format(roi))

# change to a regular numpy matrix
adj = np.array(adj.todense())

ind = np.load(fname)['arr_0']

# permuted adjacency matrix (weighted)
Aw = adj[ind, :][:, ind]
Aw[Aw<threshold] = 0


weight_all = np.sum(Aw)
weight_recurrent = np.sum(np.tril(Aw, k=-1))

print('nodes', len(Aw))
print('edges', np.sum(Aw>0))
print('recurrence', weight_recurrent/weight_all)
print()

# unweighted
A = np.zeros_like(Aw)
A[Aw>0] = 1

# unweighted DAG

A0 = np.zeros_like(Aw)
A0[Aw>0] = 1
A0[np.tril_indices(len(A), k=-1)] = 0

H = nx.from_numpy_array(A0, create_using=nx.DiGraph)

# unweighted recurrent

Ar = np.zeros_like(Aw)
Ar[Aw>0] = 1
Ar[np.triu_indices(len(A), k=1)] = 0


print('edges in DAG', np.sum(A0>0))
print('recurrent edges', np.sum(Ar>0))
print()

t0 = time()
lengths = dict(nx.all_pairs_shortest_path_length(H))
print('shortest paths found in', time()-t0)


nrec = np.sum(Ar>0)
rlength = np.zeros(nrec, dtype=int)

rows, cols = np.nonzero(Ar)

for i, (r, c) in enumerate(zip(rows, cols)):
    rlength[i] = -1 # unreachable
    if r in lengths[c]:
        rlength[i] = lengths[c][r]  # length of shortest path in DAG


print()
un, cnts = np.unique(rlength, return_counts=True)
percentages = 100.0*cnts/nrec

for u, c, p in zip(un, cnts, percentages):
    print('length of shortest path in DAG {} number of recurrent connections {} fraction {:.2f}'.format(u, c, p))
    

