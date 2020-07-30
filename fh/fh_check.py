import flow_hierarchy
import numpy as np
from timeit import default_timer
import os
import mat4py

#feedforward network

ds = 'datasets_check'

for file in os.listdir(ds):
    a = mat4py.loadmat(os.path.join(ds,file))
    adj = np.array(a[list(a.keys())[0]])

    start = default_timer()
    h,t_alg = flow_hierarchy.hmat(adj,output_exec_time=True)
    end = default_timer()
    t = end-start
    print('MATLAB alg: file=',file,' h=',h,' total time=',t,' alg exec_time=',t_alg)

    start = default_timer()
    h2,t2_alg = flow_hierarchy.hpy(adj,output_exec_time=True)
    end = default_timer()
    t2 = end-start
    print('python alg: file=',file,' h=',h2,' total time=',t2,' alg exec_time=',t2_alg)
    
    start = default_timer()
    h3,t3_alg = flow_hierarchy.hnx(adj,output_exec_time=True)
    end = default_timer()
    t3 = end-start
    print('networkx alg: file=',file,' h=',h3,' total time=',t3,' alg exec_time=',t3_alg)
    #s = input()
    #if s =='a': break
