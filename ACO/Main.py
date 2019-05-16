
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

            if i not in ant.path:#!= ant.path[-1]:
                ant.SetProb(graphPhero[ant.path[-1]][i] * (graphVis[ant.path[-1]][i] * ant.visibility[i]))
                i += 1
            else:
                ant.SetProb(0)
                i += 1
    
    return  list(map(lambda x: sum(x.prob),ants))

    
def ChoosePath(ants,sumprob,Ncities):

    cities = np.arange(1,Ncities) # Generata an array with 1,2,3...n

    for i,ant in enumerate(ants):

        for j,e in enumerate(ant.prob): # podia ser qualquer um, só para ter o tamanho do array
            if e == 0:
                ant.SetProb(0,j)
            else:
                ant.SetProb(e/sumprob[i],j)

        if sum(ant.prob) == 0:
            ant.AddPath(ant.path[0])
        else:
            ant.AddPath(int(np.random.choice(cities,1,p=ant.prob)))


def Walk(ants,graphPhero,graphVis):

    i = 1
    while i < len(graphPhero[0]):
        sumprob = CalculateProbability(ants,graphPhero,graphVis)
        ChoosePath(ants,sumprob,len(graphPhero[0]))
        i += 1



def AttPheromone(ants,graphPhero,graph,EvaporationRate):

    Evaporate(EvaporationRate,graphPhero)

    for ant in ants:
        ant.CalculateDistance(graph)
        graphPhero = ant.AddPheromone(graphPhero,EvaporationRate)
    

def Evaporate(EvaporationRate,graphPhero):

    for i, line in enumerate(graphPhero):
        for j,e in enumerate(line):
            if i == 0 or j == 0:
                pass
            else:
                graphPhero[i][j] = (1- EvaporationRate) * graphPhero[i][j]


def GeneratePheromoneGraph(graph):
    phero = [[1 for x in range(len(graph))] for y in range(len(graph[0]))] 
   
    for i in range(len(phero)):
        for j in range(len(phero[i])):
            if i == 0:
                phero[i][j] = j
            if j == 0:
                phero[i][j] = i
    
    return phero

def Fitness(ants,best):

    for ant in ants:
        if ant.Distance < best:
            best = ant.Distance

    return best


def Main(graph,nAnts,EvaporationRate):
    graphVis = SetVisibility(graph)
    graphPhero = GeneratePheromoneGraph(graph)
    best = 9999
    for i in range(0,100):
        ants = GenerateAnts(nAnts,graph)
        Walk(ants,graphPhero,graphVis)
        AttPheromone(ants,graphPhero,graph,EvaporationRate)
        best = Fitness(ants,best)
        print(str(i) + " " + str(best))
    
    print(str(best))

#------------------------Settings-------------------------------------

AntsNumber = 1000
EvaporationRate = 0.5

Main(Graphs.graphE,AntsNumber,EvaporationRate)









