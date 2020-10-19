import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
from copy import deepcopy
import math

colors = ['r', 'gs', 'yo', 'b--', 'c--']


S = (1,1)
F = (98,98)
h = lambda x: distance.cityblock(x,F)
h2 = lambda x: distance.euclidean(x,F)
c = lambda x: 1
z = lambda x: 0
sampling = 100

#Constant Probability
expanded1 = []
path1 = []
p = .5
y = np.arange(10,110,10)
for N in y:
  F = (N-2,N-2)
  exp_n = np.zeros((5))
  path_len = np.zeros((5))
  for j in range(sampling):
    maze = grid(N,S,F,p)
    for idx,(cost,heuristic) in enumerate([(c,h), (c,h2), (c,z), (z,h), (z,h2)]):
      pf = pathfinder(S, F, maze, cost, heuristic)
      exp_n[idx] += pf.expanded
      path_len[idx] += len(pf.path)
  for idx in range(5):
    path_len[idx] /= sampling
    exp_n[idx] /= sampling
  path1.append(path_len)
  expanded1.append(exp_n)

#First plot
fig = plt.figure(figsize=(22,5),dpi=80, facecolor='w', edgecolor='k')
fig.suptitle('Σταθερη Πιθανοτητα p = 0.5', fontsize = 20)

ax1 = fig.add_subplot(121)
ax1.set_xlabel('Grid Size')
ax1.set_ylabel('Path Length')
ax1.title.set_text('Μήκος του ελάχιστου μονοπατιού συναρτήσει του μεγέθους του χάρτη')
for idx,l in enumerate(zip(*path1)):
  plt.plot(y, l, colors[idx])
ax1.legend(['A*-Manhattan', 'A*-Euclidean', 'UCS', 'BFS-Manhattan', 'BFS-Euclidean'], fontsize = 16, shadow = True)

ax2 = fig.add_subplot(122)
ax2.set_xlabel('Grid Size')
ax2.set_ylabel('Log(Expanded Nodes)')
ax2.title.set_text('Πλήθος των expanded nodes συναρτήσει του μεγέθους του χάρτη')
for idx,l in enumerate(zip(*expanded1)):
  plt.plot(y, list(map(math.log10,l)), colors[idx])
ax2.legend(['A*-Manhattan', 'A*-Euclidean', 'UCS', 'BFS-Manhattan', 'BFS-Euclidean'], fontsize = 16, shadow = True)

plt.show()

#Constant Grid Size
expanded2 = []
path2 = []
N = 50
F = (N-2,N-2)
y = np.arange(0,1.1,.1)
for p in y:
  exp_n = np.zeros((5))
  path_len = np.zeros((5))
  for j in range(sampling):
    maze = grid(N,S,F,p)
    for idx,(cost,heuristic) in enumerate([(c,h), (c,h2), (c,z), (z,h), (z,h2)]):
      pf = pathfinder(S, F, maze, cost, heuristic)
      exp_n[idx] += pf.expanded
      path_len[idx] += len(pf.path)
  for idx in range(5):
    exp_n[idx] /= sampling
    path_len[idx] /= sampling
  path2.append(path_len)
  expanded2.append(exp_n)

#Second plot

fig2 = plt.figure(figsize=(22,5),dpi=80, facecolor='w', edgecolor='k')
fig2.suptitle('Σταθερο Grid Size N = 50', fontsize = 20)

ax3 = fig2.add_subplot(121)
ax3.set_xlabel('Propability')
ax3.set_ylabel('Path Length')
ax3.title.set_text('Μήκος του ελάχιστου μονοπατιού συναρτήσει της πιθανοτητας')
for idx,l in enumerate(zip(*path2)):
  plt.plot(y, l, colors[idx])
ax3.legend(['A*-Manhattan', 'A*-Euclidean', 'UCS', 'BFS-Manhattan', 'BFS-Euclidean'], fontsize = 16, shadow = True)

ax4 = fig2.add_subplot(122)
ax4.set_xlabel('Propability')
ax4.set_ylabel('Log(Expanded Nodes)')
ax4.title.set_text('Πλήθος των expanded nodes συναρτήσει της πιθανοτητας')
for idx,l in enumerate(zip(*expanded2)):
  plt.plot(y, list(map(math.log10,l)), colors[idx])
ax4.legend(['A*-Manhattan', 'A*-Euclidean', 'UCS', 'BFS-Manhattan', 'BFS-Euclidean'], fontsize = 16, shadow = True)

plt.show()
