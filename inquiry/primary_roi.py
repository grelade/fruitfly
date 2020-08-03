import numpy as np
import os
import sys
sys.path.append('../') 

import networkx as nx

from config import conf

from utils import conn2adj
from fh.flow_hierarchy import hnx
from dataset_utils import fetch_adjacency
    
# get primary_rois
with open(os.path.join('primary_rois.txt'),'r') as f: primary_rois = f.readlines()
primary_rois = list(map(lambda x: x.rstrip(),primary_rois))
empty_rois = ['CA(L)']

# h_results = {'h':[],'h_randwire':[],'h_randweight':[]}

#hpy = lambda x: np.random.randn()
reldir = '../'

for roi in primary_rois:
    try:
        print(roi)
        path = os.path.join(reldir,conf.results_dir,'primary_roi_fh','roi='+roi+'.txt')
        if roi not in empty_rois and not os.path.exists(path):
            n,conn = fetch_adjacency(adjpath=os.path.join(reldir,conf.datasets_dir,'noncropped_traced_'+roi))
            nlist,adj = conn2adj(conn)
            print('adj size =',adj.shape,'non-zero elements =',conn.shape[0])
            
            #fh
            h = hnx(adj)
            
            #fh random rewiring
            N = adj.shape[0]
            temp = []
            for i in range(20):
                perm = np.random.permutation(N)
                temp += [hnx(adj[:,perm])]

            h_randwire_mean,h_randwire_std = np.mean(temp),np.std(temp)

            #fh random weight shuffling

            temp = []
            for i in range(20):
                adj_temp = adj.copy()
                nonz = np.nonzero(adj_temp)
                weights = adj_temp[nonz]
                np.random.shuffle(weights)
                adj_temp[nonz] = weights
                temp += [hnx(adj_temp)]
                
            h_randweight_mean,h_randweight_std = np.mean(temp),np.std(temp)
            
#             h_results['h'] += [h]
#             h_results['h_randwire'] += [h_randwire]
#             h_results['h_randweight'] += [h_randweight]

            print(f'h={h},h_randwire={h_randwire_mean} +/- {h_randwire_std},h_randweight={h_randweight_mean} +/- {h_randweight_std}')
            with open(path,'w') as f:
                f.write(f'{h} {h_randwire_mean} {h_randwire_std} {h_randweight_mean} {h_randweight_std}')
                
        elif roi in empty_rois:
            print(roi,': skipping, roi is empty')
        elif os.path.exists(path):
            print(roi,': skipping, result exists')
        
    except MemoryError:
        print(roi,'memory error')
        continue

