from neuprint import Client, NeuronCriteria, fetch_adjacencies
import pandas as pd
import numpy as np
import scipy

import os

import sys
sys.path.append('..')

import fly

os.makedirs('../data', exist_ok=True)
os.makedirs('../processed', exist_ok=True)


roi = sys.argv[1]
print('Downloading', roi)
print()

criteria = NeuronCriteria(status="Traced", cropped=False)
fetch_adjacencies(criteria, criteria, export_dir='../data/noncropped_traced_{}'.format(roi), rois=[roi])


df = pd.read_csv('../data/noncropped_traced_{}/roi-connections.csv'.format(roi))

dfroi = df[df.roi==roi]
neurons = sorted(list(set(dfroi.bodyId_post.unique()).union(set(dfroi.bodyId_pre.unique()))))
N = len(neurons)

neuron_ids = np.zeros(N, dtype=int)

neuron = dict()
for i, nid in enumerate(neurons):
    neuron[nid] = i
    neuron_ids[i] = nid

print()
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

fname = '../processed/adjacency_{}.npz'.format(roi)
scipy.sparse.save_npz(fname, adjsparse)
print('saved adjacency matrix to', fname)

fname = '../processed/neuron_ids_{}.npz'.format(roi)
np.savez_compressed(fname, neuron_ids)
print('saved neuron ids to', fname)
