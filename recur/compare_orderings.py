import numpy as np
from scipy.sparse import load_npz
from sklearn.metrics import accuracy_score, matthews_corrcoef, balanced_accuracy_score
import sys

if len(sys.argv)<4:
    print('Usage: python compare_orderings.py ROI ordering1.npz ordering2.npz')
    quit()

roi = sys.argv[1]
fname1 = sys.argv[2]
fname2 = sys.argv[3]


ind1 = np.load(fname1)['arr_0']
ind2 = np.load(fname2)['arr_0']

adj = load_npz('adjacency_{}.npz'.format(roi))

assert adj.nnz==adj.count_nonzero()


row, col = adj.nonzero()

def get_y(adj, ind):
    N =  adj.nnz
    y = np.zeros(N, dtype=int)
    ws= np.zeros(N)
    indinv = np.argsort(ind)    # inverse permutation to ind
    wtot = 0
    wrec = 0

    for i in range(N):
        r = row[i]
        c = col[i]
        w = adj[r,c]
        rnew = indinv[r]
        cnew = indinv[c]
        if rnew>cnew:
            wrec += w
            y[i] = 1
        ws[i] = w
        wtot += w

    return y, ws, wrec/wtot

y1, _ ,rec1 = get_y(adj, ind1)
y2, ws, rec2 = get_y(adj, ind2)

print('{} recurrence {:.4f}'.format(fname1, rec1))
print('{} recurrence {:.4f}'.format(fname2, rec2))

print()

print('accuracy', accuracy_score(y1, y2))
print('balanced accuracy', balanced_accuracy_score(y1, y2))
print('mcc', matthews_corrcoef(y1, y2))
print()
print('weighted accuracy', accuracy_score(y1, y2, sample_weight=ws))
print('weighted balanced accuracy', balanced_accuracy_score(y1, y2, sample_weight=ws))
print('weighted mcc', matthews_corrcoef(y1, y2, sample_weight=ws))
