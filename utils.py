import numpy as np
import pandas as pd
import scipy.sparse

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