import networkx as nx
import pandas as pd


#useful functions
def comp_sizes(conn):
    '''
    input: connections dataframe
    output: list of sizes of each connected component
    '''
    G = nx.DiGraph()
    G.add_weighted_edges_from([tuple(v) for v in conn[['bodyId_pre','bodyId_post','weight']].values])
    G_und = G.to_undirected()
    components = [G_und.subgraph(c) for c in nx.connected_components(G_und)]
    #complist = sorted(nx.connected_components(G_und), key = len, reverse=True)
    return list(map(lambda x: len(x.nodes),components))

def n_comp(conn):
    '''
    input: connections dataframe
    output: number of connected components
    '''
    #complist = sorted(nx.connected_components(G_und), key = len, reverse=True)
    return len(comp_sizes(conn))

def find_max_comp_neurons(conn):
    '''
    input: connections dataframe
    output: list of neurons within largest connected component
    '''    
    G = nx.DiGraph()
    G.add_weighted_edges_from([tuple(v) for v in conn[['bodyId_pre','bodyId_post','weight']].values])
    G_und = G.to_undirected()
    #components = [G_und.subgraph(c) for c in nx.connected_components(G_und)]
    complist = sorted(nx.connected_components(G_und), key = len, reverse=True)
    if len(complist)==0:
        print('skipping, no nodes lest after thresholding')
        #return conn[conn['bodyId_pre']==-1]
        return []
    
    return complist[0]



def scomp_sizes(conn):
    '''
    input: connections dataframe
    output: list of sizes of each STRONGLY connected component
    '''
    G = nx.DiGraph()
    G.add_weighted_edges_from([tuple(v) for v in conn[['bodyId_pre','bodyId_post','weight']].values])
    components = [G.subgraph(c) for c in nx.strongly_connected_components(G)]
    #complist = sorted(nx.connected_components(G_und), key = len, reverse=True)
    return list(map(lambda x: len(x.nodes),components))

def n_scomp(conn):
    '''
    input: connections dataframe
    output: number of STRONGLY connected components
    '''
    #complist = sorted(nx.connected_components(G_und), key = len, reverse=True)
    return len(scomp_sizes(conn))

def find_max_scomp_neurons(conn):
    '''
    input: connections dataframe
    output: list of neurons within largest STRONGLY connected component
    '''    
    G = nx.DiGraph()
    G.add_weighted_edges_from([tuple(v) for v in conn[['bodyId_pre','bodyId_post','weight']].values])
    #components = [G_und.subgraph(c) for c in nx.connected_components(G_und)]
    complist = sorted(nx.strongly_connected_components(G), key = len, reverse=True)
    if len(complist)==0:
        print('skipping, no nodes lest after thresholding')
        #return conn[conn['bodyId_pre']==-1]
        return []
    
    return complist[0]



def restrict_max_comp(conn):
    '''
    input: connections dataframe
    output: connections df restricted to largest connected component
    '''
    max_comp = find_max_comp_neurons(conn)
    return conn[conn['bodyId_pre'].isin(max_comp) & conn['bodyId_post'].isin(max_comp)]


def restrict_max_scomp(conn):
    '''
    input: connections dataframe
    output: connections df restricted to largest STRONGLY connected component
    '''
    max_scomp = find_max_scomp_neurons(conn)
    return conn[conn['bodyId_pre'].isin(max_scomp) & conn['bodyId_post'].isin(max_scomp)]

def restrict_th(conn,th):
    '''
    input: connections dataframe
    output: connections df thresholded at th
    '''
    return conn[conn['weight']>th]