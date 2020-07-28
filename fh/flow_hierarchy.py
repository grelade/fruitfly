import numpy as np
import os
import subprocess
import mat4py
import scipy.sparse
from timeit import default_timer

# flow_hierarchy algorithm; NOT optimized
# taken from http://www.mit.edu/~cmagee/luo_hierarchy/
def hpy(A,output_exec_time=False):
    
    time_start = default_timer()
    n = A.shape[0]
    A_edge = np.zeros((n,n))
    k=0
    for i in range(n):
        for j in range(n):
            if A[i,j]>0:
                A_edge[i,j]=k
                k+=1
    #return A_edge

    n_edge = int(sum(sum(A)))
    #print(n_edge)
    B = np.zeros((n_edge,n_edge))
    t=0
    for i in range(n):
        for j in range(n):
            if A_edge[i,j]>0:
                for k in range(n):
                    if A_edge[j,k]>0:
                        #print('test')
                        B[int(A_edge[i,j]),int(A_edge[j,k])]=1
            t+=1


    L = int(B.shape[0])
    all0 = np.zeros((L,L))
    sumallold = 0
    dist = B
    sumuBk = B
    Bk = B
    for k in range(2,L):
        Bk = np.matmul(Bk,B)
        uBk = unitize(Bk)
        DBk = unitize(uBk-sumuBk) # was uBk-sumuBk > 0
        sumuBk+=uBk
        dist+=k*DBk
        all0=unitize(all0+DBk)
        sumall=sum(sum(all0))
        if sumall==sumallold:
            break
        else:
            sumallold=sumall

    hlink = 0
    for i in range(L):
        if dist[i,i]==0:
            hlink+=1
    hdegree = hlink/L
    
    time_end = default_timer()
    if output_exec_time:  
        return hdegree, time_end-time_start
    else:
        return hdegree


def unitize(mat):
    return (mat>0)*1
    #return np.array(list(map(np.vectorize(lambda x: 1 if x>0 else 0),mat)))


def hpy_sparse(A,output_exec_time=False,matrix_init_func=scipy.sparse.dok_matrix):
    
    time_start = default_timer()
    n = A.shape[0]
    A_edge = matrix_init_func((n,n))
    k=0
    for i in range(n):
        for j in range(n):
            if A[i,j]>0:
                A_edge[i,j]=k
                k+=1
    #return A_edge

    n_edge = int(sum(sum(A)))
    #print(n_edge)
    B = matrix_init_func((n_edge,n_edge))
    t=0
    for i in range(n):
        for j in range(n):
            if A_edge[i,j]>0:
                for k in range(n):
                    if A_edge[j,k]>0:
                        #print('test')
                        B[int(A_edge[i,j]),int(A_edge[j,k])]=1
            t+=1

    L = int(B.shape[0])
    all0 = matrix_init_func((L,L))
    sumallold = 0
    dist = B
    sumuBk = B
    Bk = B
    #print(type(Bk),type(B))
    for k in range(2,L):
        #Bk = np.matmul(Bk,B)
        Bk = Bk @ B
        uBk = unitize(Bk)
        DBk = unitize(uBk-sumuBk) # was uBk-sumuBk > 0
        sumuBk+=uBk
        dist+=k*DBk
        all0=unitize(all0+DBk)
        #sumall=sum(sum(all0))
        sumall = B.count_nonzero()
        if sumall==sumallold:
            break
        else:
            sumallold=sumall

    hlink = 0
    for i in range(L):
        if dist[i,i]==0:
            hlink+=1
    hdegree = hlink/L

    time_end = default_timer()
    if output_exec_time:
        return hdegree, time_end-time_start
    else:
        return hdegree
    
    
def unitize(mat):
    return (mat>0)*1
    #return np.array(list(map(np.vectorize(lambda x: 1 if x>0 else 0),mat)))

# shabby pipe to matlab
def hmat(A,output_exec_time=False):
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

def calc_fh(A,alg='py'):

    if alg=='py':
        print('starting python alg...')
        return hpy(A)
    elif alg=='py_optim':
        print('starting sparse python alg...')
        return hpy_sparse(A)
    else:
        print('starting MATLAB alg...')        
        return hmat(A)
