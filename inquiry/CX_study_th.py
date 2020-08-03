import numpy as np
import os
import sys
sys.path.append('../') 

import networkx as nx

from config import conf

from utils import conn2adj
from fh.flow_hierarchy import hnx
from dataset_utils import fetch_adjacency
    
# get CX_rois
CX_rois = ['PB','NO','FB','EB','AB(L)','AB(R)']
#CX_rois = ['PB']
empty_rois = []
ths = [i for i in range(150)]
#ths = [0,1,2,3,4,5,6,7,8,9,10,12,14,18,22,25,30,35,45,50,52,54,55,57,59,62,65,70,90,110]

# h_results = {'h':[],'h_randwire':[],'h_randweight':[]}

#hpy = lambda x: np.random.randn()
reldir = '../'

for roi in CX_rois:
    try:
        if roi not in empty_rois:
            n,conn = fetch_adjacency(adjpath=os.path.join(reldir,conf.datasets_dir,'noncropped_traced_'+roi))
            for th in ths:
                print(th,roi)
                path = os.path.join(reldir,conf.results_dir,'CX_study_th',f'th={th};roi={roi}.txt')
                if not os.path.exists(path):
                    temp = conn[conn['weight']>th]
                    nlist,adj = conn2adj(temp)
                    if temp.shape[0]>0:
                        print('adj size =',adj.shape,'non-zero elements =',temp.shape[0])

                        #fh
                        h = hnx(adj)

                        #fh random rewiring
            #             N = adj.shape[0]
            #             temp = []
            #             for i in range(20):
            #                 perm = np.random.permutation(N)
            #                 temp += [hnx(adj[:,perm])]

            #             h_randwire_mean,h_randwire_std = np.mean(temp),np.std(temp)

                        #fh random weight shuffling

            #             temp = []
            #             for i in range(20):
            #                 adj_temp = adj.copy()
            #                 nonz = np.nonzero(adj_temp)
            #                 weights = adj_temp[nonz]
            #                 np.random.shuffle(weights)
            #                 adj_temp[nonz] = weights
            #                 temp += [hnx(adj_temp)]

            #             h_randweight_mean,h_randweight_std = np.mean(temp),np.std(temp)


                        print(f'th={th};h={h}')
                        with open(path,'w') as f:
                            #f.write(f'{h} {h_randwire_mean} {h_randwire_std} {h_randweight_mean} {h_randweight_std}')
                            f.write(f'{h} {th}')

        elif roi in empty_rois:
            print(roi,': skipping, roi is empty')
        elif os.path.exists(path):
            print(roi,': skipping, result exists')

    except MemoryError:
        print(roi,'memory error')
        continue

