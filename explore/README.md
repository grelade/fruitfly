# Some scripts for analysis


```
python connected_components.py ROI THRESHOLD
```
lists connected components of the original ROI at a given THRESHOLD

```
python analyze_recurrence.py ROI THRESHOLD SEED
```
For each recurrent connection j->i, finds the shortest path from i to j in the DAG and computes the distribution of these shortest path lengths in the given ROI. ROI, THRESHOLD, SEED have to correspond to previously computed ordering.


