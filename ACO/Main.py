
"""
What to do:

    (X) Randomly place ants at the cities

    -- For each ant:

        (X) Choose a not yet visited city until tour is completed
        ( ) Optimize the tour
        ( ) Update pheromone Tij += 1/lenght(tour)

    ( ) Evaporate Pheromone Tij = (1-p) * Tij

"""

#Get Graphs form upper folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import GraphsDataBase as Graphs

#Get Ants
from Ants import Ants as Ants

#Get MathStuff
import random
import numpy as np 

def SetVisibility(graph):
    """We'll use the 1/d expression to calculate this"""
    #vis = list(map(lambda x: list(map(lambda y: y if y != 0 else 0 ,x[1:])),graph [1:] ))

    vis = [[0 for x in range(len(graph))] for y in range(len(graph[0]))] 

   # print (vis)

    for i, line in enumerate(graph):
        for j,e in enumerate(line):
            if i == 0:
                vis[i][j] = j
            elif j == 0:
                vis[i][j] = i
            else:
                vis[i][j] = 1/graph[i][j] if graph[i][j] != 0 else 0
            

    return vis

def GenerateAnts(nAnts,graph):
    ants = [] * nAnts

    for i in range (nAnts):
        ants.append( Ants( len(graph), random.randint(1, len(graph[0])-1 ) ) ) 

    return ants

def CalculateProbability(ants,graphPhero,graphVis):

    for ant in ants:
        i = 1
        while i < len(graphPhero):

            if i != ant.path[-1]:
                ant.SetProb(graphPhero[ant.path[-1]][i] * (graphVis[ant.path[-1]][i] * ant.visibility[i]))
                i += 1
            else:
                i += 1
    
    sumprob = list(map(lambda x: sum(x.prob),ants))

    for i,ant in enumerate(ants):

        for j,e in enumerate(ant.prob): # podia ser qualquer um, só para ter o tamanho do array
            ant.SetProb(e/sumprob[i],j)
            
    cities = np.arange(1,len(graphPhero[0]) - 1)
    print(sum(ants[0].prob))
    print(np.random.choice(cities,1,p=ants[0].prob))




        


        



def Main(graph,nAnts):
    graphVis = SetVisibility(graph)
    graphPhero = [[1 for x in range(len(graph))] for y in range(len(graph[0]))] 
    ants = GenerateAnts(nAnts,graph)
    CalculateProbability(ants,graphPhero,graphVis)
    #print(ants)

#------------------------Settings-------------------------------------

AntsNumber = 10


Main(Graphs.graphA,AntsNumber)









