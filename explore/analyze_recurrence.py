import numpy as np
import networkx as nx
from time import time
import sys

import matplotlib.pyplot as plt

from utils import load

if len(sys.argv)<4:
    print('Usage: python graph_analysis ROI THRESHOLD SEED')
    quit()

roi = sys.argv[1]
threshold = int(sys.argv[2])
seed = int(sys.argv[3])

Aw, A, A0 = load(roi, threshold, seed)

# unweighted recurrent

Ar = np.zeros_like(Aw)
Ar[Aw>0] = 1
Ar[np.triu_indices(len(A), k=1)] = 0


print('edges in DAG', np.sum(A0>0))
print('recurrent edges', np.sum(Ar>0))
print()

# compute lengths of shortest paths on the DAG

H = nx.from_numpy_array(A0, create_using=nx.DiGraph)

t0 = time()
lengths = dict(nx.all_pairs_shortest_path_length(H))
print('shortest paths found in', time()-t0)


nrec = np.sum(Ar>0)
rlength = np.zeros(nrec, dtype=int)

rows, cols = np.nonzero(Ar)

reciprocal_weights = []

for i, (r, c) in enumerate(zip(rows, cols)):
    rlength[i] = -1 # unreachable
    if r in lengths[c]:
        rlength[i] = lengths[c][r]  # length of shortest path in DAG
        if rlength[i]==1:
            reciprocal_weights.append((Aw[c,r], Aw[r,c]))


print()
un, cnts = np.unique(rlength, return_counts=True)
percentages = 100.0*cnts/nrec

for u, c, p in zip(un, cnts, percentages):
    print('length of shortest path in DAG {} number of recurrent connections {} fraction {:.2f}'.format(u, c, p))
    
reciprocal_weights = np.array(reciprocal_weights)
max_weight = np.amax(reciprocal_weights)
plt.figure()
plt.scatter(reciprocal_weights[:,0], reciprocal_weights[:,1], s=1, alpha=0.5)
plt.plot([1,max_weight], [1,max_weight], color='k', alpha=0.25)
plt.xlabel('feed-forward weights')
plt.ylabel('recurrent weights')
plt.title('reciprocal connections ({} threshold {})'.format(roi, threshold))

plt.show()
