import numpy as np
import os
import sys
sys.path.append('../') 

from config import conf
conf.enable_neuprint = False #disabling neuprint

from fh.flow_hierarchy import hpy
from utils import conn2adj

from dataset_utils import fetch_adjacency

reldir = '../'
# get primary_rois

with open('primary_rois.txt','r') as f: primary_rois = f.readlines()
primary_rois = list(map(lambda x: x.rstrip(),primary_rois))
empty_rois = ['CA(L)']

for roi in primary_rois:
    try:
        print(roi)
        path = os.path.join(reldir,conf.results_dir,'primary_roi_fh','roi='+roi+'.txt')
        if roi not in empty_rois and not os.path.exists(path):

            n,conn = fetch_adjacency(adjpath=os.path.join(reldir,conf.datasets_dir,'noncropped_traced_'+roi))
            nlist,adj = conn2adj(conn)
            print('adj size =',adj.shape,'non-zero elements =',conn.shape[0])
            fh = hpy(adj)
#             fh = np.random.randn()
            print('fh=',fh)
            with open(path,'w') as f:
                f.write(str(fh))
        elif roi in empty_rois:
            print(roi,': skipping, roi is empty')
        elif os.path.exists(path):
            print(roi,': skipping, result exists')
        
    except MemoryError:
        print(roi,'memory error')
        continue