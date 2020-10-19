# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
from copy import deepcopy

class grid:
    def __init__(self, N, S, F, p):
        
        ## Make sure start and end are within the grid
        assert N > 2
        assert S[0] < N
        assert S[1] < N
        assert F[0] < N
        assert F[1] < N

        assert S[0] > 0
        assert S[1] > 0
        assert F[0] > 0
        assert F[1] > 0

        self.N = N
        self.S = S
        self.F = F
        self.grid = np.zeros((N, N), dtype=np.int32)
        
        ## Surround the grid with obstacles
        self.grid[0, :] = -1
        self.grid[N - 1, :] = -1
        self.grid[:, 0] = -1
        self.grid[:, N - 1] = -1

        visited = np.zeros((N,N), dtype=np.bool)
        visited[0, :] = 1
        visited[N - 1, :] = 1
        visited[:, 0] = 1
        visited[:, N - 1] = 1
        self.visited = visited

        obstacle_free_points = {S, F}
        visited[S]=1
        visited[F]=1
        
        #print("Start ",S)
        #print("Finish ",F)
        #print("Probability ",p)
        self.path = self.make_maze(p)
        
        ### Fill the grid with obstacles. 
        ### An obstacle at position (x,y) -> grid[x,y]=1
        ### Ensure there is a path from S to F
        ### Your code here ###
    
    def get_path(self, visited):
        path = []
        current = self.S
        while True:
            neighbours=[]
            dist = distance.cityblock(current,self.F)
            visited[current]=True
            neighbours = self.adjacent_near(current, visited, dist)
            if not neighbours:
              current = path.pop()
              continue     
            
            if(self.F in neighbours):
              if current not in path:
                path.append(current)
              path.append(self.F)
              visited[self.F]=True
              break
            path.append(current)
            current = neighbours[np.random.choice(len(neighbours))] #min(neighbours,key=lambda x: distance.euclidean(x,self.F))  #neighbours[np.random.choice(len(neighbours))]
        return path
            
    def adjacent_near(self, node, visited, dist):
        adjacent_nodes = []
        flag = np.random.choice([0,1],1,p=[.15,.85])
        for n in (node[0] - 1, node[1]), (node[0] + 1, node[1]), (node[0], node[1] - 1), (node[0], node[1] + 1):
            if n == self.F:
              adjacent_nodes.append(n)
              break
            if (not visited[n]) and (flag or distance.cityblock(n,self.F) <= dist) :
              adjacent_nodes.append(n)
        return adjacent_nodes
    
    def make_maze(self,p):
        visit = deepcopy(self.visited)
        path = self.get_path(visit)
        num_of_obs=np.random.binomial(self.N,p)
        for n in path:
          self.visited[n]=1
        for i in range(1,(self.N-1)):
            for j in range(1,(self.N - 1)):
                if(self.visited[i][j]):
                  continue
                self.visited[i][j]=1
                self.grid[i][j] = np.random.choice([0,1],1,p=[1-p,p])
        return path
