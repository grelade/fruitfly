from neuprint import Client, NeuronCriteria, fetch_adjacencies, fetch_roi_hierarchy, fetch_meta
import os
import pandas as pd

from config import conf

def fetch_adjacency(criteria=None,
                    prefix='noncropped_traced',force_download=False,
                    **kwargs):
    
    if 'client' in kwargs.keys():  
        client = kwargs['client']
    else: 
        client = Client(conf.neuprint_URL, conf.dataset_version, conf.api_token)

    if criteria==None:
        criteria = NeuronCriteria(status='Traced',cropped=False,client=client)
        
    datadir = conf.datasets_dir
    postfix = '_'+'.'.join(kwargs['rois']) if 'rois' in kwargs.keys() else ''
    adjpath = os.path.join(datadir,prefix+postfix)
    roipath = os.path.join(adjpath,conf.roi_connections_file)
    neurpath = os.path.join(adjpath,conf.neurons_file)
    
    if os.path.exists(adjpath) and os.path.exists(roipath) and os.path.exists(neurpath) and not force_download:
        #print('dataset already downloaded')
        adj = pd.read_csv(roipath)
        neurons = pd.read_csv(neurpath)
    else:
        print('downloading dataset')
        neurons,adj = fetch_adjacencies(sources=criteria, targets=criteria, export_dir=adjpath,**kwargs)
        
    return neurons,adj
    

def fetch_rois_from_metadata(**kwargs):

    if 'client' in kwargs.keys():  
        client = kwargs['client']
    else: 
        client = Client(conf.neuprint_URL, conf.dataset_version, conf.api_token)
        
    metadata = fetch_meta(**kwargs)
    #print(metadata.keys())
    g = fetch_roi_hierarchy(mark_primary=False,include_subprimary=True,format='nx',**kwargs)
    
    nonhierarchy_rois = metadata['nonHierarchicalRois']
    primary_rois = metadata['primaryRois']
    
    all_rois = list(g.nodes)
    
    toplevel_rois = []
    for i,s in enumerate(g.successors('hemibrain')):
        toplevel_rois += [s]
    
    
    return all_rois, primary_rois, nonhierarchy_rois, toplevel_rois

def fetch_rois_from_df(conn_df): 
    #ROIs from dataset
    rois_dataset = list(conn_df['roi'].unique())
    return rois_dataset



def fetch_primary_roi_datasets(**kwargs):
    if 'client' in kwargs.keys():  
        client = kwargs['client']
    else: 
        client = Client(conf.neuprint_URL, conf.dataset_version, conf.api_token)
        
    _, primary_rois, _, _ = fetch_rois_from_metadata(client=client)

    empty_rois = []
    for roi in primary_rois:
        try:
            
            #print(roi)
            fetch_adjacency(rois=[roi],client=client)
        except KeyError:
            print('download problem, skipping')
            empty_rois+=[roi]
            continue

    return empty_rois