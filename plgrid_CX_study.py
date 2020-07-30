import numpy as np
import os

from config import conf
conf.enable_neuprint = False #disabling neuprint

from fh.flow_hierarchy import hpy
from utils import conn2adj

from dataset_utils import fetch_adjacency
    
# get CX_rois
CX_rois = ['PB','NO','FB','EB','AB(L)','AB(R)']
#CX_rois = ['PB']
empty_rois = []

h_results = {'h':[],'h_randwire':[],'h_randweight':[]}

hpy = lambda x: np.random.randn()

for roi in CX_rois:
    try:
        print(roi)
        path = os.path.join(conf.results_dir,'CX_study','roi='+roi+'.txt')
        if roi not in empty_rois and not os.path.exists(path):
            n,conn = fetch_adjacency(adjpath='datasets/noncropped_traced_'+roi)
            nlist,adj = conn2adj(conn)
            print('adj size =',adj.shape,'non-zero elements =',conn.shape[0])
            
            #fh
            h = hpy(adj)
            
            #fh random rewiring
            N = adj.shape[0]
            perm = np.random.permutation(N)
            h_randwire = hpy(adj[:, perm])
            
            #fh random weight shuffling
            nonz = np.nonzero(adj)
            weights = adj[nonz]
            np.random.shuffle(weights)
            adj[nonz] = weights
            h_randweight = hpy(adj)
            
            h_results['h'] += [h]
            h_results['h_randwire'] += [h_randwire]
            h_results['h_randweight'] += [h_randweight]

#             fh = np.random.randn()
            print(f'h={h},h_randwire={h_randwire},h_randweight={h_randweight}')
            with open(path,'w') as f:
                f.write(f'{h} {h_randwire} {h_randweight}')
                
        elif roi in empty_rois:
            print(roi,': skipping, roi is empty')
        elif os.path.exists(path):
            print(roi,': skipping, result exists')
        
    except MemoryError:
        print(roi,'memory error')
        continue

