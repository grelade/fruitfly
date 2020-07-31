import numpy as np
import pandas as pd
from time import time
from numba import jit



def compute_score(adj, perm=None):
    N = len(adj)
    if perm is None:
        perm = np.arange(N)
    lower = np.tril_indices(len(perm), k=-1)
    adj = adj[perm,:][:,perm]
    total_weight = np.sum(adj)
    return np.sum(adj[lower])/total_weight


def initialize(adj, n_permutations=100):
    N = len(adj)
    ind = np.arange(N)
    ind_trial = np.zeros_like(ind)
    best_score = compute_score(adj, ind)
    for k in range(n_permutations):
        ind_trial[:] = numba_random_permutation(N)
        score = compute_score(adj, ind_trial)
        if score<best_score:
            best_score = score
            ind[:] = ind_trial
    return ind, best_score






@jit(nopython=True)
def init_numba_seed(seed):
    np.random.seed(seed)

@jit(nopython=True)
def numba_random_permutation(N):
    return np.random.permutation(N)


@jit(nopython=True)
def get_score_relative(adj, perm, i, j, total_weight):
    arr = adj[perm,:][:,perm]
    i, j = min(i,j), max(i,j)
    B = np.sum(arr[i+1:j,i])
    K = np.sum(arr[j,i:j])
    E = np.sum(arr[i:j,j])
    H = np.sum(arr[i,i+1:j])
    return (- B + E - K + H)/total_weight


@jit(nopython=True)
def optimize_loop(adj, ind, ind_trial, best_score, verbose=True):
    N = len(adj)
    total_weight = np.sum(adj)
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
        delta_score = get_score_relative(adj, ind, i, j, total_weight)
        if delta_score<0:
            best_score += delta_score
            ind[:] = ind_trial
            if verbose:
                print(steps, steps_since_decrease, best_score)
            steps_since_decrease = 0
        else:
            steps_since_decrease += 1
        steps += 1
    return steps, best_score

def optimize(adj, seed, verbose=True):
    np.random.seed(seed)
    init_numba_seed(seed)

    initial_score = compute_score(adj)
    ind, best_score = initialize(adj)
    ind_trial = np.zeros_like(ind)

    if verbose:
        print('initial score', initial_score)
        print('score after random permutations', best_score)

    t0 = time()
    steps, best_score = optimize_loop(adj, ind, ind_trial, best_score, verbose=verbose)
    if verbose:
        print()
        print('optimized score', best_score, 'in', steps, 'steps. time:', time()-t0)
        print('cross check    ', compute_score(adj, ind))
    
    return ind



