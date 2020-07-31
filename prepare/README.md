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
which generates a file with a name like `processed/ordering_PB_raw_t10_s0.npz`.

Typically the resulting DAG part of the graph is disconnected. This is fixed by the script
```
python fix_raw_ordering.py ROI THRESHOLD SEED
```
which produces `processed/ordering_PB_fix_t10_s0.npz`. These files should be used for any subsequent analysis.

I ran the scripts
```
./make_raw_orderings_all_cx.sh
./fix_raw_orderings_all_cx.sh
```
Note that **FB** was run individually as it took 10 hours at threshold 1 and 3 hours at threshold 10.
