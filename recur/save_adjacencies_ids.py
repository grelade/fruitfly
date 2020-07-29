import numpy as np
import pandas as pd
import scipy.sparse

import sys

if len(sys.argv)<2:
    print('usage: python save_adjacencies_ids.py "ROI"')
    quit()

roi = sys.argv[1]
print('roi ', roi)

df = pd.read_csv('../noncropped_traced_{}/roi-connections.csv'.format(roi))

dfroi = df[df.roi==roi]
neurons = sorted(list(set(dfroi.bodyId_post.unique()).union(set(dfroi.bodyId_pre.unique()))))
N = len(neurons)

neuron_ids = np.zeros(N, dtype=int)

neuron = dict()
for i, nid in enumerate(neurons):
    neuron[nid] = i
    neuron_ids[i] = nid

print('neurons', N)
print('edges', len(dfroi))
print()

adj = np.zeros((N,N))
for i in range(len(dfroi)):
    connection = dfroi.iloc[i]
    n1 = neuron[connection.bodyId_pre]
    n2 = neuron[connection.bodyId_post]
    adj[n1, n2] = connection.weight


adjsparse = scipy.sparse.csr_matrix(adj)

scipy.sparse.save_npz('adjacency_{}.npz'.format(roi), adjsparse)
print('saved adjacency matrix to', 'adjacency_{}.npz'.format(roi))

np.savez_compressed('neuron_ids_{}.npz'.format(roi), neuron_ids)
print('saved neuron ids to', 'neuron_ids_{}.npz'.format(roi))

#print(len(dfroi), adjsparse.count_nonzero())
#print(neuron_ids[:20])
#print(neuron_ids[-20:])
