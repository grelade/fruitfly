# Scripts for downloading and reordering nodes

```
./download_all_cx.sh
```
Downloaded raw data (Hemibrain v 1.1) is put into the `data/` folder.
Adjacency matrices and neuron ids are put into the `processed/` folder.

Raw orderings are generated for the maximal connected component of the given ROI at a specified threshold
```
python make_raw_ordering.py ROI THRESHOLD SEED
```
which generates a file with a name like `processed/ordering_PB_raw_T10_S0.npz` (threshold 10 seed 0).

Typically the resulting DAG part of the graph is disconnected. This is fixed by the script
```
python fix_raw_ordering.py ROI THRESHOLD SEED
```
which produces `processed/ordering_PB_fix_T10_S0.npz`. These files should be used for any subsequent analysis.

I ran the scripts
```
./make_raw_orderings_all_cx.sh
./fix_raw_orderings_all_cx.sh
```
Note that **FB** was run separately as it took 10 hours at threshold 1 and 3 hours at threshold 10.

`optimize_ordering.py` contains just the optimization routines. Useful functions:
```
ind = optimize(adj, seed) # performs optimization for the adjacency matrix adj
```
and
```
def compute_score(adj, perm=None)
```
computes *recurrence* score for a given adjacency matrix (and an optional permutation or ordering of a subset of nodes).
