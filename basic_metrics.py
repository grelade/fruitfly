import numpy as np
import pandas as pd




def indegree_mean(adj):
    '''
    adj_(ij) = connection ( j-> i )
    '''
#     if istype(adj,np.array):
    return np.mean(np.sum(adj,axis=0))
#     elif istype(adj,pd.DataFrame):
#         return 0
        

def outdegree_mean(adj):
    '''
    adj_(ij) = connection ( j-> i )
    '''
    return np.mean(np.sum(adj,axis=1))
