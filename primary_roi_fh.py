import numpy as np
import os

from config import conf
conf.enable_neuprint = False

from fh.flow_hierarchy import hpy
from utils import conn2adj

if conf.enable_neuprint:
    from neuprint import Client
    from dataset_utils import fetch_adjacency,fetch_rois_from_metadata, fetch_primary_roi_datasets

    c = Client(conf.neuprint_URL, conf.dataset_version,conf.api_token)
    _, primary_rois, _, _ = fetch_rois_from_metadata(client=c)
    empty_rois = fetch_primary_roi_datasets(client=c)

else:
    from dataset_utils import fetch_adjacency_noneuprint
    
    plgrid_dir = 'plgrid'
    with open(os.path.join(plgrid_dir,'primary_rois.txt'),'r') as f:
        primary_rois = f.readlines()
    
    primary_rois = list(map(lambda x: x.rstrip(),primary_rois))
    empty_rois = ['CA(L)']

#print(primary_rois)
for roi in primary_rois:
    try:
        print(roi)
        if roi not in empty_rois:
            if conf.enable_neuprint:
                n,conn = fetch_adjacency(rois=[roi],client=c)
            else:
                n,conn = fetch_adjacency_noneuprint(rois=[roi]) #hacky way to circumvent lack of neuprint
            nlist,adj = conn2adj(conn)
            print('adj size =',adj.shape,'non-zero elements =',conn.shape[0])
            #fh = hpy(adj)
            fh = np.random.randn()
            print('fh=',fh)
            path = os.path.join(conf.results_dir,'fh_roi='+roi+'.txt')
            with open(path,'w') as f:
                f.write(str(fh))
        else:
            print(roi,': skipping, roi is empty')
        
    except MemoryError:
        print(roi,'memory error')
        continue