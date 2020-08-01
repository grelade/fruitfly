import numpy as np
import networkx as nx
from time import time
import sys

import matplotlib.pyplot as plt

from utils import load, reorder

if len(sys.argv)<4:
    print('Usage: python graph_analysis ROI THRESHOLD SEED')
    quit()

roi = sys.argv[1]
threshold = int(sys.argv[2])
seed = int(sys.argv[3])

Aw, A, A0 = load(roi, threshold, seed)


inputs = (np.sum(A0, axis=0)==0)
outputs = (np.sum(A0, axis=1)==0)
internal_nodes = ~(inputs | outputs)

num_inputs = np.sum(inputs)
num_outputs = np.sum(outputs)
num_internal = np.sum(internal_nodes)

print('num_inputs', num_inputs)
print('num_outputs', num_outputs)
print('num_internal', num_internal)
print()

H = nx.from_numpy_array(A0, create_using=nx.DiGraph)
nodes = np.array(H.nodes)

t0 = time()
lengths = dict(nx.all_pairs_shortest_path_length(H))
print('shortest paths found in', time()-t0)


ancs = dict()
descs= dict()

for i in range(num_inputs):
    ni = nodes[inputs][i]
    descs[i] = nx.descendants(H, ni)
    
for j in range(num_outputs):
    nj = nodes[outputs][j]
    ancs[j] = nx.ancestors(H, nj)


input_similarity = np.zeros((num_inputs, num_inputs))

for i in range(num_inputs):
    for j in range(num_inputs):
        seti = descs[i]
        setj = descs[j]
        input_similarity[i, j] = 2*len(seti & setj)/(len(seti) + len(setj))

indinp = reorder(input_similarity)

input_similarity = input_similarity[indinp, :][:, indinp]

output_similarity = np.zeros((num_outputs, num_outputs))

for i in range(num_outputs):
    for j in range(num_outputs):
        seti = ancs[i]
        setj = ancs[j]
        output_similarity[i, j] = 2*len(seti & setj)/(len(seti) + len(setj))

indout = reorder(output_similarity)

output_similarity = output_similarity[indout, :][:, indout]




dist = np.zeros((num_inputs, num_outputs), dtype=int)
dist[:,:] = -1

for i in range(num_inputs):
    ni = nodes[inputs][i]
    for j in range(num_outputs):
        nj = nodes[outputs][j]
        if nj in lengths[ni]:
            dist[i, j] = lengths[ni][nj]



#indr = reorder(dist)
#indc = reorder(dist.T)

indr = indinp
indc = indout

dist_reordered = dist[indr, :][:, indc]



size = np.zeros((num_inputs, num_outputs), dtype=int)

for i in range(num_inputs):
    for j in range(num_outputs): 
        size[i, j] = len(ancs[j] & descs[i])

size_reordered = size[indr, :][:, indc]



internal_index = dict()
for k in range(num_internal):
    internal_index[nodes[internal_nodes][k]] = k

connectivity_inputs = np.zeros((num_internal, num_inputs), dtype=int)
connectivity_outputs = np.zeros((num_internal, num_outputs), dtype=int)

for i in range(num_inputs):
    connected = [internal_index[n] for n in descs[i] if internal_nodes[n]]
    connectivity_inputs[connected, i] = 1

for j in range(num_outputs):
    connected = [internal_index[n] for n in ancs[j] if internal_nodes[n]]
    connectivity_outputs[connected, j] = 1

connectivity_inputs = connectivity_inputs[:, indr]
connectivity_outputs= connectivity_outputs[:, indc]
connectivity = np.hstack((connectivity_inputs, connectivity_outputs))

indint = reorder(connectivity)

connectivity = connectivity[indint, :]

plt.figure()
plt.imshow(input_similarity, cmap=plt.cm.RdYlBu_r)
plt.colorbar()
plt.xlabel('inputs')
plt.ylabel('inputs')
plt.title('input similarity ({} threshold {})'.format(roi, threshold))

plt.figure()
plt.imshow(output_similarity, cmap=plt.cm.RdYlBu_r)
plt.colorbar()
plt.xlabel('outputs')
plt.ylabel('outputs')
plt.title('output similarity ({} threshold {})'.format(roi, threshold))


plt.figure()
ax = plt.gca()
plt.imshow(dist_reordered, cmap=plt.cm.RdYlBu_r)
ax.set_aspect(num_outputs/num_inputs)
plt.xlabel('outputs')
plt.ylabel('inputs')
plt.title('shortest distance ({} threshold {})'.format(roi, threshold))
plt.colorbar()

plt.figure()
ax = plt.gca()
plt.imshow(size_reordered, cmap=plt.cm.RdYlBu_r)
ax.set_aspect(num_outputs/num_inputs)
plt.xlabel('outputs')
plt.ylabel('inputs')
plt.title('input->output size ({} threshold {})'.format(roi, threshold))
plt.colorbar()


plt.figure()
plt.hist(size.reshape(-1), bins=50)
plt.xlabel('size')
plt.ylabel('count')
plt.title('input->output size histogram ({} threshold {})'.format(roi, threshold))


plt.figure()
plt.subplot(121)
plt.imshow(connectivity_inputs[indint, :])
ax = plt.gca()
ax.set_aspect(num_inputs/num_internal)
plt.xlabel('inputs')
plt.ylabel('internal')

plt.title('connectivity of internal nodes')


plt.subplot(122)
plt.imshow(connectivity_outputs[indint, :])
ax = plt.gca()
ax.set_aspect(num_outputs/num_internal)
plt.xlabel('outputs')
plt.ylabel('internal')

plt.title('({} threshold {})'.format(roi, threshold))

# plt.figure()
# plt.plot(np.sum(connectivity_inputs[indint, :], axis=1),'.')
# plt.plot(np.sum(connectivity_outputs[indint, :], axis=1),'.')


plt.show()
