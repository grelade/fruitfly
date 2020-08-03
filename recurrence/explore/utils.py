import numpy as np
from scipy.sparse import load_npz



def load(roi, threshold, seed, verbose=True):
    '''
    Prepares the ordered adjacency matrix (Aw), its unweighted version (A)
    and unwieghted DAG (A0)
    '''

    fname = '../processed/ordering_{}_fix_T{}_S{}.npz'.format(roi, threshold, seed)

    if verbose:
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

    if verbose:
        print('nodes', len(Aw))
        print('edges', np.sum(Aw>0))
        print('recurrence', weight_recurrent/weight_all)
        print()
        print('------------------------------------')
        print()

    # unweighted
    A = np.zeros_like(Aw)
    A[Aw>0] = 1

    # unweighted DAG

    A0 = np.zeros_like(Aw)
    A0[Aw>0] = 1
    A0[np.tril_indices(len(A), k=-1)] = 0

    return Aw, A, A0

def reorder(X):
    N = len(X)
    sqrs = np.sum(X**2, axis=1)
    k = np.argmax(sqrs)
    lst = [k]
    rest = [j for j in range(N) if j!=k]
    while len(lst)<N:
        i = lst[-1]
        dists = np.array([ np.sum((X[j]-X[i])**2) for j in rest ])
        k = np.argmin(dists)
        lst.append(rest[k])
        rest.remove(rest[k])
    return np.array(lst)


    

