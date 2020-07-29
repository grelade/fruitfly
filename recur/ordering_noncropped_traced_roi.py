import numpy as np
import pandas as pd
from time import time
from numba import jit

import sys

if len(sys.argv)<3:
    print('usage: python ordering_noncropped_traced_roi.py "ROI" SEED')
    quit()

roi = sys.argv[1]
seed = int(sys.argv[2])
print('roi ', roi)
print('seed', seed)


np.random.seed(seed)

@jit(nopython=True)
def init_numba_seed(seed):
    np.random.seed(seed)

@jit(nopython=True)
def numba_random_permutation(N):
    return np.random.permutation(N)

init_numba_seed(seed)

df = pd.read_csv('../noncropped_traced_{}/roi-connections.csv'.format(roi))

dfroi = df[df.roi==roi]
neurons = sorted(list(set(dfroi.bodyId_post.unique()).union(set(dfroi.bodyId_pre.unique()))))
neuron = dict()
for i, nid in enumerate(neurons):
    neuron[nid] = i

N = len(neurons)

adj = np.zeros((N,N))
for i in range(len(dfroi)):
    connection = dfroi.iloc[i]
    n1 = neuron[connection.bodyId_pre]
    n2 = neuron[connection.bodyId_post]
    adj[n1, n2] = connection.weight


lower = np.tril_indices(N, k=-1)
total_weight = np.sum(adj)

def get_score(perm):
    return np.sum((adj[perm,:][:,perm])[lower])/total_weight

@jit(nopython=True)
def get_score_relative(adj, perm, i, j):
    arr = adj[perm,:][:,perm]
    i, j = min(i,j), max(i,j)
    B = np.sum(arr[i+1:j,i])
    K = np.sum(arr[j,i:j])
    E = np.sum(arr[i:j,j])
    H = np.sum(arr[i,i+1:j])
    return (- B + E - K + H)/total_weight

print('N', N)
print('total weight', total_weight)

ind = np.arange(N)
ind_trial = np.zeros_like(ind)

t0 = time()
 
best_score = get_score(ind)
print('initial score', best_score)

for k in range(100):
    ind_trial[:] = numba_random_permutation(N)
    score = get_score(ind_trial)
    if score<best_score:
        best_score = score
        ind[:] = ind_trial

best_score = get_score(ind)
print('best random permutation score', best_score)
print()

@jit(nopython=True)
def optimize(adj, ind, ind_trial, best_score):
    best_score = best_score
    steps_since_decrease = 0
    steps = 0
    while steps_since_decrease<1000:
        i = np.random.randint(N)
        j = np.random.randint(N)
        while i==j:
            j = np.random.randint(N)
        ind_trial[:] = ind
        ind_trial[i] = ind[j]
        ind_trial[j] = ind[i]
        #new_score = get_score(ind_trial)
        delta_score = get_score_relative(adj, ind, i, j)
        if delta_score<0:
            best_score += delta_score
            ind[:] = ind_trial
            print(steps, steps_since_decrease, best_score)
            steps_since_decrease = 0
        else:
            steps_since_decrease += 1
        steps += 1
    return steps, best_score

steps, best_score = optimize(adj, ind, ind_trial, best_score)

print()
print('steps', steps, 'score', best_score)
print('time', time()-t0)

#DEBUG
lower_weight = np.sum(np.tril(adj[ind,:][:,ind], k=-1))
upper_weight = np.sum(np.triu(adj[ind,:][:,ind], k=1))
print('lower', lower_weight, 'upper', upper_weight, 'tot', lower_weight + upper_weight)
print('total weight', total_weight)
print()

fname = 'ordering_{}_{}.npz'.format(roi, seed)
print('saving permutation to', fname)
np.savez_compressed(fname, ind)

