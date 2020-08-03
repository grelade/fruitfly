import numpy as np
import pandas as pd
import scipy.sparse
import networkx as nx

from config import conf


def conn2adj(conn_df,sparse_cutoff=10000):
    adjId_to_bodyId = np.sort(pd.concat((conn_df['bodyId_pre'],(conn_df['bodyId_post']))).unique())
    size = adjId_to_bodyId.shape[0]
    if size<sparse_cutoff:
        adj = np.zeros(shape=(size,size))
    else:
        adj = scipy.sparse.dok_matrix(shape=(size,size))
        
    for i,conn in conn_df.iterrows():
        
        id_pre = np.argwhere(adjId_to_bodyId==conn['bodyId_pre']).item()
        id_post = np.argwhere(adjId_to_bodyId==conn['bodyId_post']).item()
        adj[id_post,id_pre] = conn['weight']
        
    return adjId_to_bodyId, adj


def find_component_data(conns,rois):

    roi_components = {'strong_comp':{},'comp':{}}
    roi_components_edge_distr = {'strong_comp':{},'comp':{}}
    roi_components_node_distr = {'strong_comp':{},'comp':{}}

    for roi in rois:
        temp = conns[roi]
        G = nx.DiGraph()
        G.add_weighted_edges_from([tuple(v) for v in temp[['bodyId_pre','bodyId_post','weight']].values])
        strong_components = [G.subgraph(c) for c in nx.strongly_connected_components(G)]
        n_comp = len(strong_components)
        roi_components['strong_comp'][roi] = n_comp
        temp_edge = []
        temp_node = []
        for i in range(n_comp):
            temp_node += [len(list(strong_components[i].nodes))]
            temp_edge += [strong_components[i].number_of_edges()]       
            #print('component {} nodes {} edges {:}'.format(i, len(nodesi), edges))
        roi_components_node_distr['strong_comp'][roi] = temp_node
        roi_components_edge_distr['strong_comp'][roi] = temp_edge

        G_und = G.to_undirected()
        components = [G_und.subgraph(c) for c in nx.connected_components(G_und)]
        n_comp = len(components)
        roi_components['comp'][roi] = n_comp
        temp_edge = []
        temp_node = []
        for i in range(n_comp):
            temp_node += [len(list(components[i].nodes))]
            temp_edge += [components[i].number_of_edges()]       
            #print('component {} nodes {} edges {:}'.format(i, len(nodesi), edges))
        roi_components_node_distr['comp'][roi] = temp_node
        roi_components_edge_distr['comp'][roi] = temp_edge  
    return roi_components,roi_components_edge_distr,roi_components_node_distr


def calc_component_th(conns,rois,ths):
    
    conn_CX_split,CX_rois,ths = conns,rois,ths
    
    n_comp_th = {roi:[] for roi in CX_rois}
    e_comp_th = {roi:[] for roi in CX_rois}
    n_scomp_th = {roi:[] for roi in CX_rois}
    e_scomp_th = {roi:[] for roi in CX_rois}

    for th in ths:
        conn_CX_split_th = {roi:conn_CX_split[roi][conn_CX_split[roi]['weight']>th] for roi in CX_rois}
        no_comps,e_comp,n_comp = find_component_data(conn_CX_split_th,CX_rois)
        for roi in CX_rois:
            ln_comp,le_comp = n_comp['comp'][roi],e_comp['comp'][roi]
            ln_scomp,le_scomp = n_comp['strong_comp'][roi],e_comp['strong_comp'][roi]
            ln_comp_max,le_comp_max,ln_scomp_max,le_scomp_max = tuple(map(lambda l: max(l) if len(l)>0 else 0,[ln_comp,le_comp,ln_scomp,le_scomp]))
            n_comp_th[roi] += [ln_comp_max]
            e_comp_th[roi] += [le_comp_max]
            n_scomp_th[roi] += [ln_scomp_max]
            e_scomp_th[roi] += [le_scomp_max]
    return n_comp_th,e_comp_th,n_scomp_th,e_scomp_th