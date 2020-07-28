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
    h,t_alg = flow_hierarchy.calc_fh(adj,output_exec_time=True)
    end = default_timer()
    t = end-start
    print('MATLAB alg: file=',file,' h=',h,' total time=',t,' alg exec_time=',t_alg)

    start = default_timer()
    h2,t2_alg = flow_hierarchy.calc_fh(adj,alg='py',output_exec_time=True)
    end = default_timer()
    t2 = end-start
    print('python alg: file=',file,' h=',h2,' total time=',t2,' alg exec_time=',t2_alg)
    #s = input()
    #if s =='a': break
