import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse
import os

from neuprint import Client

from config import conf
from dataset_utils import fetch_adjacency, fetch_rois_from_metadata, fetch_primary_roi_datasets
from fh.flow_hierarchy import hpy
from utils import conn2adj

c = Client(conf.neuprint_URL, conf.dataset_version,conf.api_token)
_, primary_rois, _, _ = fetch_rois_from_metadata(client=c)

empty_rois = fetch_primary_roi_datasets(client=c)

for roi in primary_rois:
    try:
        print(roi)
        if roi not in empty_rois:
            n,conn = fetch_adjacency(rois=[roi],client=c)
            nlist,adj = conn2adj(conn)
            print('adj size =',adj.shape,'non-zero elements =',conn.shape[0])
            fh = hpy(adj)
            #fh = np.random.randn()
            print('fh=',fh)
            path = os.path.join(conf.results_dir,'fh_roi='+roi+'.txt')
            with open(path,'w') as f:
                f.write(str(fh))
        else:
            print(roi,': skipping, roi is empty')
        
    except MemoryError:
        print(roi,'memory error')
        continue