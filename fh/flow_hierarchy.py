import numpy as np
import os
import subprocess
import scipy.sparse
from timeit import default_timer
import sys

# flow_hierarchy algorithm; NOT optimized
# taken from http://www.mit.edu/~cmagee/luo_hierarchy/
def hpy(A,output_exec_time=False,mat_init_func = np.zeros):
        
    time_start = default_timer()
    
    # numbering nonzero links
    n = A.shape[0]
    A_edge = mat_init_func((n,n))
    edge_W = list()
    k=1
    for i in range(n):
        for j in range(n):
            if A[i,j]>0:
                A_edge[i,j]=k
                edge_W += [A[i,j]]
                k+=1

    n_edge = len(edge_W)
    B = mat_init_func((n_edge,n_edge))
    t=0
    for i in range(n):
        for j in range(n):
            if A_edge[i,j]>0:
                for k in range(n):
                    if A_edge[j,k]>0:
                        #print('test')
                        B[int(A_edge[i,j])-1,int(A_edge[j,k])-1]=1
            t+=1


    L = int(B.shape[0])
    all0 = mat_init_func((L,L))
    sumallold = 0
    dist = B
    sumuBk = B
    Bk = B
    for k in range(2,L):
        Bk = Bk @ B
        uBk = unitize(Bk)
        DBk = unitize(uBk-sumuBk) # was uBk-sumuBk > 0
        sumuBk+=uBk
        dist+=k*DBk
        all0=unitize(all0+DBk)
        sumall=np.sum(all0)
        if sumall==sumallold:
            break
        else:
            sumallold=sumall

    hlink = 0
    for i in range(L):
        if dist[i,i]==0:
            hlink+=edge_W[i]
    hdegree = hlink/np.sum(edge_W)
    
    time_end = default_timer()
    if output_exec_time:  
        return hdegree, time_end-time_start
    else:
        return hdegree

def unitize(mat):
    return (mat>0)*1

#shabby pipe to matlab
def hmat(A,output_exec_time=False):
    import mat4py
    mat4py.savemat('temp.mat',{'adj':A.tolist()})
    cmd = ['matlab -nodesktop -r "load(\'temp.mat\'); tic; addpath(\'fh\'); h = hierarchy(adj); t= toc; save(\'temp.mat\'); quit "']
    sp = subprocess.run(cmd,shell=True,stdout=subprocess.DEVNULL) #dump output to /dev/null
    out = mat4py.loadmat('temp.mat')
    #print(out)
    if 't' in out.keys():
        print('run completed. alg_runtime =',out['t'])
    if output_exec_time:
        return out['h'],out['t']
    else:
        return out['h']

def hnx(A,output_exec_time=False):
        
        #networkx has a fast built-in func
    try:
        import networkx as nx
        time_start = default_timer()
        g = nx.DiGraph(A)
        hdegree = nx.flow_hierarchy(g,weight='weight')
        time_end = default_timer()   
        time = time_end-time_start
    except ImportError:
        print('networkx not found')
        hdegree=0
        time = 0
        pass
        
    if output_exec_time:  
        return hdegree,time 
    else:
        return hdegree
