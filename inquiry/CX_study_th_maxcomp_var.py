import numpy as np
import os
import sys
sys.path.append('../') 

import networkx as nx

from config import conf

from utils import conn2adj
from fh.flow_hierarchy import hnx
from dataset_utils import fetch_adjacency

expname = 'CX_study_th_maxcomp_var'
# get CX_rois
CX_rois = ['PB','NO','FB','EB','AB(L)','AB(R)']
#CX_rois = ['PB']
empty_rois = []
ths = [i for i in range(150)]
#ths = [0,1,2,3,4,5,6,7,8,9,10,12,14,18,22,25,30,35,45,50,52,54,55,57,59,62,65,70,90,110]

restr_variant = 3 # variants 0,1,2,3

reldir = '../'


path0 = os.path.join(reldir,conf.results_dir,expname)
if not os.path.exists(path0):
    os.makedirs(path0)

#load data
neur_CX_split,conn_CX_split = {}, {}
for roi in CX_rois:
    n,conn = fetch_adjacency(adjpath=os.path.join(reldir,conf.datasets_dir,'noncropped_traced_'+roi))
    neur_CX_split[roi],conn_CX_split[roi] = n,conn
    
def n_comp(conn):
    G = nx.DiGraph()
    G.add_weighted_edges_from([tuple(v) for v in conn[['bodyId_pre','bodyId_post','weight']].values])
    G_und = G.to_undirected()
    components = [G_und.subgraph(c) for c in nx.connected_components(G_und)]
    #complist = sorted(nx.connected_components(G_und), key = len, reverse=True)
    return len(components)

def comp_sizes(conn):
    G = nx.DiGraph()
    G.add_weighted_edges_from([tuple(v) for v in conn[['bodyId_pre','bodyId_post','weight']].values])
    G_und = G.to_undirected()
    components = [G_und.subgraph(c) for c in nx.connected_components(G_und)]
    #complist = sorted(nx.connected_components(G_und), key = len, reverse=True)
    return list(map(lambda x: len(x.nodes),components))

def n_scomp(conn):
    G = nx.DiGraph()
    G.add_weighted_edges_from([tuple(v) for v in conn[['bodyId_pre','bodyId_post','weight']].values])

    components = [G.subgraph(c) for c in nx.strongly_connected_components(G)]
    #complist = sorted(nx.connected_components(G_und), key = len, reverse=True)
    return len(components)

def scomp_sizes(conn):
    G = nx.DiGraph()
    G.add_weighted_edges_from([tuple(v) for v in conn[['bodyId_pre','bodyId_post','weight']].values])
    components = [G.subgraph(c) for c in nx.strongly_connected_components(G)]
    #complist = sorted(nx.connected_components(G_und), key = len, reverse=True)
    return list(map(lambda x: len(x.nodes),components))

def find_max_comp_neurons(conn):
    G = nx.DiGraph()
    G.add_weighted_edges_from([tuple(v) for v in conn[['bodyId_pre','bodyId_post','weight']].values])
    G_und = G.to_undirected()
    #components = [G_und.subgraph(c) for c in nx.connected_components(G_und)]
    complist = sorted(nx.connected_components(G_und), key = len, reverse=True)
    if len(complist)==0:
        print(roi,': skipping, no nodes lest after thresholding')
        #return conn[conn['bodyId_pre']==-1]
        return []
    
    return complist[0]

def find_max_strong_comp_neurons(conn):
    G = nx.DiGraph()
    G.add_weighted_edges_from([tuple(v) for v in conn[['bodyId_pre','bodyId_post','weight']].values])
    #components = [G_und.subgraph(c) for c in nx.connected_components(G_und)]
    complist = sorted(nx.strongly_connected_components(G), key = len, reverse=True)
    if len(complist)==0:
        print(roi,': skipping, no nodes lest after thresholding')
        #return conn[conn['bodyId_pre']==-1]
        return []
    
    return complist[0]
    
def restrict_max_strong_comp(conn):
    max_scomp = find_max_strong_comp_neurons(conn)
    return conn[conn['bodyId_pre'].isin(max_scomp) & conn['bodyId_post'].isin(max_scomp)]

def restrict_max_comp(conn):
    max_comp = find_max_comp_neurons(conn)
    return conn[conn['bodyId_pre'].isin(max_comp) & conn['bodyId_post'].isin(max_comp)]

def restrict_th(conn,th):
    return conn[conn['weight']>th]

#main loop
for roi in CX_rois:
    n,conn = neur_CX_split[roi], conn_CX_split[roi]
    for th in ths:
        print(th,roi)
        path = os.path.join(reldir,conf.results_dir,expname,f'var={restr_variant};th={th};roi={roi}.txt')
        if not os.path.exists(path):
            if restr_variant==0:
                conn_out = restrict_th(conn,th)
            elif restr_variant==1:
                conn1 = restrict_max_comp(conn)
                conn_out = restrict_th(conn1,th)
            elif restr_variant==2:
                conn1 = restrict_th(conn,th)
                conn_out = restrict_max_comp(conn1)
            elif restr_variant==3:
                conn1 = restrict_max_comp(conn)
                conn2 = restrict_th(conn1,th)
                conn_out = restrict_max_comp(conn2)
            
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