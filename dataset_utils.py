import os
import pandas as pd
import numpy as np

from config import conf

if conf.enable_neuprint:
    from neuprint import Client, NeuronCriteria, fetch_adjacencies, fetch_roi_hierarchy, fetch_meta

    
def fetch_adjacency(criteria=None,
                    prefix='noncropped_traced',
                    force_download=False,
                    neuprint=conf.enable_neuprint,
                    adjpath=None,
                    **kwargs):
    '''
    simple neuprint.fetch_adjacencies wrapper. 
    Checks whether datasets were already downloaded and loads them accordingly. 
    By default func loads traced and noncropped neurons.
    '''
    
    assert not force_download or neuprint, 'no neuprint; cannot download dataset'
    
    #compose adjpath
    if adjpath is None:
        if not isinstance(kwargs['rois'],list): kwargs['rois'] = [kwargs['rois']]
        
        datadir = conf.datasets_dir
        postfix = '_'+'.'.join(kwargs['rois']) if 'rois' in kwargs.keys() else '' 
        adjpath = os.path.join(datadir,prefix+postfix)
          
    roipath = os.path.join(adjpath,conf.roi_connections_file)
    neurpath = os.path.join(adjpath,conf.neurons_file)
    
    files_exist = os.path.exists(adjpath) and os.path.exists(roipath) and os.path.exists(neurpath)
    assert files_exist or neuprint, 'no neuprint; cannot find dataset (and no way of fetching)'
    
    if neuprint:
        if 'client' not in kwargs.keys():  
            kwargs['client'] = Client(conf.neuprint_URL, conf.dataset_version, conf.api_token)

        if criteria==None:
            criteria = NeuronCriteria(status='Traced',cropped=False,client=kwargs['client'])

    print('dataset in adjpath=',adjpath)
    
    if os.path.exists(adjpath) and os.path.exists(roipath) and os.path.exists(neurpath) and not force_download:
        print('dataset already downloaded')
        adj = pd.read_csv(roipath)
        neurons = pd.read_csv(neurpath)
    else:
        print('downloading dataset')
        print(criteria)
        neurons,adj = fetch_adjacencies(sources=criteria, targets=criteria, export_dir=adjpath,**kwargs)
        
    return neurons,adj



def fetch_adjacency_noneuprint(prefix='noncropped_traced',
                               **kwargs):
    '''
    fetch_adjacency func to use in plgrid, serves as fetch_adjacency when no neuprint support
    '''
    datadir = conf.datasets_dir
    postfix = '_'+'.'.join(kwargs['rois']) if 'rois' in kwargs.keys() else ''
    adjpath = os.path.join(datadir,prefix+postfix)
    roipath = os.path.join(adjpath,conf.roi_connections_file)
    neurpath = os.path.join(adjpath,conf.neurons_file)
    
    if os.path.exists(adjpath) and os.path.exists(roipath) and os.path.exists(neurpath):
        #print('dataset already downloaded')
        adj = pd.read_csv(roipath)
        neurons = pd.read_csv(neurpath)
    else:
        print('no dataset and no neuprint')
        adj = 0
        neurons = 0
 
    return neurons,adj


def fetch_rois_from_metadata(**kwargs):
    '''
    DESCRIPTION MISSING
    '''
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
    '''
    DESCRIPTION MISSING
    '''
    #ROIs from dataset
    rois_dataset = list(conn_df['roi'].unique())
    return rois_dataset



def fetch_primary_roi_datasets(**kwargs):
    '''
    DESCRIPTION MISSING
    '''
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


def fetch_toplevel_roi_datasets(**kwargs):
    '''
    DESCRIPTION MISSING
    '''
    if 'client' not in kwargs.keys():  
        kwargs['client'] = Client(conf.neuprint_URL, conf.dataset_version, conf.api_token)
        
    _, _, _, toplevel_rois = fetch_rois_from_metadata(client=client)

    empty_rois = []
    for roi in toplevel_rois:
        try:
            
            #print(roi)
            fetch_adjacency(rois=[roi],**kwargs)
        except KeyError:
            print('download problem, skipping')
            empty_rois+=[roi]
            continue

    return empty_rois


def fetch_CX_datasets(**kwargs):
    '''
    DESCRIPTION MISSING
    '''
    
    if 'client' not in kwargs.keys():  
        kwargs['client'] = Client(conf.neuprint_URL, conf.dataset_version, conf.api_token)
        
    CX_rois = [['CX'],['PB','NO','FB','EB','AB(L)','AB(R)']]

    empty_rois = []
    for roi in CX_rois:
        try:
            
            #print(roi)
            fetch_adjacency(rois=roi,**kwargs)
        except KeyError:
            print('download problem, skipping')
            empty_rois+=[roi]
            continue

    return empty_rois    