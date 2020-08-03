# Some scripts for analysis

## Utilities

`utils.py` contains a loader
```
def load(roi, threshold, seed, verbose=True)
    ...
    return Aw, A, A0
```
returning the adjacency matrix of the reordered weighted graph, its unweighted version (i.e. with weights 1) and the unweighted DAG subset.

```
def reorder(X)
```
returns a (heuristic) reordering of the *rows* of X, so that the result looks nice and similar rows are close together.

## Connected components

```
python connected_components.py ROI THRESHOLD
```
lists connected components of the original ROI at a given THRESHOLD

## Recurrent connections

```
python analyze_recurrence.py ROI THRESHOLD SEED
```
For each recurrent connection j->i, finds the shortest path from i to j in the DAG and computes the distribution of these shortest path lengths in the given ROI. 
In addition plots recurrent versus feedforward weights of reciprocal connections (length=1).

ROI, THRESHOLD, SEED have to correspond to previously computed ordering.
 
## Intrinsic input/output structure of the DAG

```
python analyze_input_output.py ROI THRESHOLD SEED
```
Determines the number of purely input neurons, purely output neurons and internal ones.
Each pair of input and output neuron determines a DAG. 
The script plots similarities between the input and output nodes, the minimal path length of the above sub-DAG's, their sizes, a histogram of their sizes and a plot of connectivity between the individual internal neurons and the input and output ones. The neurons are reordered for spotting similarity.
