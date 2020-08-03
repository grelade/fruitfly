import numpy as np
import networkx as nx
from scipy.sparse import load_npz

from optimize_ordering import compute_score, optimize

import matplotlib.pyplot as plt

import sys

if len(sys.argv)<4:
    print('Usage: python fix_raw_ordering.py ROI THRESHOLD SEED')
    quit()

PLOTS = False

roi = sys.argv[1]
threshold = int(sys.argv[2])
seed = int(sys.argv[3])

fname = '../processed/ordering_{}_raw_T{}_S{}.npz'.format(roi, threshold, seed)

print('roi:', roi)
print('threshold', threshold)
print('seed', seed)
print('ordering file:', fname)

adj = load_npz('../processed/adjacency_{}.npz'.format(roi))

# change to a regular numpy matrix
adj = np.array(adj.todense())

# threshold
adj[adj<threshold] = 0

# permuted adjacency matrix (weighted)
ind = np.load(fname)['arr_0']
Aw = adj[ind, :][:, ind]

score = compute_score(Aw)
print('score', score)

# unweighted DAG

A0 = np.zeros_like(Aw)
A0[Aw>0] = 1
A0[np.tril_indices(len(A0), k=-1)] = 0

# connected components in the DAG

H = nx.from_numpy_array(A0, create_using=nx.DiGraph)

components = [H.subgraph(c).copy() for c in nx.weakly_connected_components(H)]

n_comp = len(components)
print('connected components in DAG:', n_comp)
print()
print('------------------------')
print()

if n_comp>1:

    # count weights of (recurrent) connections between the components

    Acomp = np.zeros((n_comp, n_comp))

    for i in range(n_comp):
        for j in range(n_comp):
            if i==j:
                continue
            nodesi = list(components[i].nodes)
            nodesj = list(components[j].nodes)
            weights_i_to_j = np.sum(Aw[nodesi,:][:,nodesj])
            Acomp[i, j] = weights_i_to_j

    scorecomp0 = compute_score(Acomp)
    print('initial score - connected components', scorecomp0)


    if PLOTS:
        plt.figure('Acomp')
        plt.imshow(Acomp)

    ind_comp = optimize(Acomp, 0)

    Acomp1 = Acomp[ind_comp, :][:, ind_comp]
    scorecomp1 = compute_score(Acomp1)
    print('final score - connected components', scorecomp1)
    print()

    if PLOTS:
        plt.figure('Acomp1')
        plt.imshow(Acomp1)

    # hack for fixing simple remaining components (as in CX 1621)

    print('remaining recurrent connections between components')
    rows, cols = np.nonzero(Acomp1) 
    ordering = list(range(len(Acomp1)))
    for r, c in zip(rows, cols):
        if r<c or Acomp1[c,r]>=Acomp1[r,c]:
            continue
        ordering.remove(r)
        pos = ordering.index(c)
        ordering.insert(pos, r)
        print(r, c, Acomp1[r,c], Acomp1[c,r])

    indfix = np.array(ordering)
    indtrial = ind_comp[indfix]

    Acomp2 = Acomp[indtrial, :][:, indtrial]
    scorecomp2 = compute_score(Acomp2)
    print('final score - connected components - fix', scorecomp2)

    if scorecomp1<scorecomp2:
        ind_comp = indtrial
        print('using fix')
    else:
        print('ignoring fix (not applicable or worse)')
    print()

    if PLOTS:
        plt.figure('Acomp2')
        plt.imshow(Acomp2)

    # translate the permutation in terms of components into a permutation in terms of nodes

    N = len(Aw)
    indbis = np.arange(N)
    j = 0
    for i in range(n_comp):
        k = ind_comp[i]
        nodes = sorted(list(components[k].nodes))
        num_nodes = len(nodes)
        indbis[j:j+num_nodes] = nodes
        j += num_nodes

    Aw2 = Aw[indbis, :][:, indbis]

    print('initial recurrence', compute_score(Aw))
    print('final   recurrence', compute_score(Aw2))

    # combine the two permuations and check that we get the same recurrence

    indtot = ind[indbis]
    Aw3 = adj[indtot, :][:, indtot]

    print('final   recurrence', compute_score(Aw3))

    print()
    print('------------------------')
    print()

    # unweighted DAG for the final permutation

    A0 = np.zeros_like(Aw3)
    A0[Aw3>0] = 1
    A0[np.tril_indices(len(A0), k=-1)] = 0

    H = nx.from_numpy_array(A0, create_using=nx.DiGraph)

    # find connected components and find the largest one

    components = [H.subgraph(c) for c in nx.weakly_connected_components(H)]

    n_comp_final = len(components)
    print('connected components in initial DAG', n_comp)
    print('connected components in final DAG', n_comp_final)
    print()

    # this will be the final ordering
    ind = indtot


    if PLOTS:
        plt.show()

else:
    print('DOES NOT NEED A FIX!')
    print('WILL SAVE THE SAME FILE UNDER A NEW NAME FOR CONSISTENCY...')
    print()

newfname = '../processed/ordering_{}_fix_T{}_S{}.npz'.format(roi, threshold, seed)
print('saving ordering as', newfname)
np.savez_compressed(newfname, ind)
