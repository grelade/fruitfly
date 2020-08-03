import numpy as np
import os
import sys
sys.path.append('../') 

import networkx as nx

from config import conf

from utils import conn2adj
from fh.flow_hierarchy import hnx
from dataset_utils import fetch_adjacency
from CX_utils import restrict_th,restrict_max_comp,find_max_comp_neurons

expname = 'CX_study_th_maxcomp'
# get CX_rois
CX_rois = ['PB','NO','FB','EB','AB(L)','AB(R)']
#CX_rois = ['PB']
empty_rois = []
ths = [i for i in range(150)]
#ths = [0,1,2,3,4,5,6,7,8,9,10,12,14,18,22,25,30,35,45,50,52,54,55,57,59,62,65,70,90,110]
reldir = '../'


path0 = os.path.join(reldir,conf.results_dir,expname)
if not os.path.exists(path0):
    os.makedirs(path0)

#load data
neur_CX_split,conn_CX_split = {}, {}
for roi in CX_rois:
    n,conn = fetch_adjacency(adjpath=os.path.join(reldir,conf.datasets_dir,'noncropped_traced_'+roi))
    neur_CX_split[roi],conn_CX_split[roi] = n,conn

#main loop
for roi in CX_rois:
    n,conn = neur_CX_split[roi], conn_CX_split[roi]
    for th in ths:
        print(th,roi)
        path = os.path.join(reldir,conf.results_dir,expname,f'th={th};roi={roi}.txt')
        if not os.path.exists(path):

            conn1 = restrict_th(conn,th)
            conn_out = restrict_max_comp(conn1)
            
            size_maxcomp = len(find_max_comp_neurons(conn_out))
            nlist,adj = conn2adj(conn_out)

            if conn_out.shape[0]>0:

                print('adj size =',adj.shape,'non-zero elements =',conn_out.shape[0])

                #fh
                h = hnx(adj)
                print(f'th={th};h={h};size(max_comp)={size_maxcomp}')
                with open(path,'w') as f:
                    #f.write(f'{h} {h_randwire_mean} {h_randwire_std} {h_randweight_mean} {h_randweight_std}')
                    f.write(f'{h} {th} {size_maxcomp}')
        else:
            print(roi,': skipping, result exists')