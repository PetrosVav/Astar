import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import time

class pathfinder:
    def __init__(self, S, F, grid, c, h):
        self.S = S  ## S is the starting point - a tuple (x,y)
        self.F = F  ## F is the goal
        self.grid = grid ## A grid object (from part A)
        ### Optional
        self.vis = visualization(S, F)
        self.path = []
        self.cost = c
        self.heuristic = h
        
        
        self.path, self.expanded = self.get_path()
        

    
    ### Fill the path list with the coordinates of each point in the path from S to F
    
    def reconstruct_path(self, came_from, start, goal):
      current = goal
      path = []
      while current != start:
          path.append(current)
          current = came_from[current]
      path.append(start) # optional
      path.reverse() # optional
      return path

    def get_path(self):
      no_path = True
      #The open (frontier) and closed (expanded) set of nodes
      frontier=[]
      exp_n=[]

      #The parent nodes of expanded nodes
      came_from = {}
      came_from[self.S] = None

      #Current point is the starting point
      current = self.S
      curr_dist=self.heuristic(self.S)
      curr_g=0

      #Add the current node to the open set
      #Insert in the first position because if 2 or more
      #nodes have the same minimum f value, pick the one
      #that has been inserted last, that is, the node in
      #the top level 
      frontier.insert(0,(current,curr_dist,curr_g))
      
      #gflag is used for the children nodes that update the frontier
      gflag = True

      #Measure the performance of the algorithm
      start = time.time()

      while(frontier!=[]):
        ### Optional
        self.vis.draw_step(self.grid, list(map(lambda x:x[0], frontier)), list(map(lambda x:x[0], exp_n)))

        current, curr_dist, curr_g = min(frontier, key = lambda x: x[1]+x[2] )

        #Find the item in the open set with the lowest G + H score
        frontier.remove((current,curr_dist,curr_g))
        exp_n.insert(0, (current, curr_dist, curr_g))
        if(current == self.F):
          no_path = False
          break
        children=[]
        children=self.grid.adjacent(current)
        for x in children:
          if x in exp_n:
            continue
          dist2 = self.heuristic(x)
          g2 = curr_g + self.cost(current)
          
          for i,dist,g in frontier:
            if x==i:
              gflag = False
              if g2 < g:
                frontier.remove((i,dist,g))
                #frontier.append((x,dist2,g2))
                frontier.insert(0,(x,dist2,g2))
                came_from[x] = current
              break
          
          if not gflag:
            gflag = True
            continue

          for i,dist,g in exp_n:
            if x==i:
              gflag = False
              if g2 < g:
                print("halloo")
                exp_n.remove((i,dist,g))
                #frontier.append((x,dist2,g2))
                frontier.insert(0,(x,dist2,g2))
                came_from[x] = current
              break

          if not gflag:
            gflag = True
            continue

          frontier.insert(0,(x,dist2,g2))
          #frontier.append((x,dist2,g2))
          came_from[x] = current
        
        
      end = time.time()
      if frontier!=[]:
        exp_n.append(self.F)
      if no_path:
        print("There is no path")
      else:
        exp_n.append(self.F)
      #print("Performance: ", end - start)
      path = self.reconstruct_path(came_from,self.S,current)
      #print("length of exp_n", len(exp_n))

      ### Optional
      self.vis.add_path(path)

      return path,len(exp_n)
