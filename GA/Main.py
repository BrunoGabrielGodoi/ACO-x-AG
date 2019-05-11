#Get things for math
import random
import operator
import numpy as np 
import time as time

#Get lib to playsounds
from playsound import playsound


#Get Graphs form upper folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import GraphsDataBase as Graphs

#Get lib to make nice plotting hystograns and set them up
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)



mm,rm = "", ""

class Individual:
    """ Class of genes."""

    path = []
    score = 999
    staticSumofScores = 1 
    mutated = False

    def __init__(self, path):
        self.path = path[:]
        mutated = False
    
    def SetScore(self,x,sizeOfPop = 1):
        self.score = x
        self.probability = x/sizeOfPop

    def CalculateProbability(self):
        """ calculate the probability normalized """
        return (1/(Individual.staticSumofScores*self.score))

    def __repr__(self):
        """print the score when the object is called by print"""
        if self.mutated:
            return "M-" + str(self.score)
        else:
            return str(self.score)

class Graph:
    """ Class to store the graph."""

    def __init__(self, size, arestas):
        self.size = size
        self.arestas = arestas

    def IsConnected(self,a,b):
        if self.arestas[a][b] != 0:
            return True
        else: 
            return False
    
    def ReturnWeight(self,a,b):
        return self.arestas[a][b]


def GeneratePopulation(sizeOfPopulation, graph):
    """ Generates a population with an possible path for the graph"""
    path = [1]
    population = [] * sizeOfPopulation  

    for i in range(0,sizeOfPopulation):
        j = 1
        while j < (graph.size + 1):
            
            compatible = False
            ErrorCounter = 0
            while compatible == False:

                temp = random.randint(1, graph.size) # 0,5 = 1-5
                a = path[-1]
                ErrorCounter += 1
                if graph.IsConnected(a,temp):

                    if temp not in path :
                        path.append(temp)
                        compatible = True
                    elif len(path) == graph.size :
                        path.append(1)
                        compatible = True

                elif ErrorCounter > (graph.size*4): 

                    path.clear()
                    path.append(1)
                    j = 1
                    ErrorCounter = 0
            j += 1
         
        
        population.append(Individual(path))

        path.clear()
        path.append(1)
  
    return population

def CleanScore(population):
    """ Cleans the population score to 999"""
    for i in population:
        i.SetScore(9999)

    return population

#do this
def Fitness(population, graph):
    """ Generates a score based on the path of each individual and sorts the population list."""

    population = CleanScore(population)
    Individual.staticSumofScores = 0
    for i in population:
        scoreSum = 0
        j = 0
        while j < (len(i.path)-1):

            scoreSum += graph.ReturnWeight(i.path[j], i.path[j+1])
            Individual.staticSumofScores += graph.ReturnWeight(i.path[j], i.path[j+1])
            j += 1


        i.SetScore(scoreSum,len(population))

    # sort array by atribute score in Individuals
    population.sort(key=operator.attrgetter('score'))


def CrossoverMPX(couple,graph):
    """Crossover a couple of inds using the MPX technique"""
    #rm = "MPX"
    a = random.randint(1,len(couple[0].path)-3)
    b = random.randint(a+1,len(couple[0].path)-2)
    dad1 = random.randint(0,1)
    dad2 = int(not bool(dad1))
    dads = []
    dads.append(dad1)
    dads.append(dad2)
    dad1 = couple[dad1].path
    dad2 = couple[dad2].path
    
    sonPath = [1] * len(dad2)

    while a <= b:
        sonPath[a] = dad2[a]
        a +=1

    i = 1
    while i < len(dad1)-1:
    
        if sonPath[i] != 1:
            i += 1
            continue #check if working
        else :
            if dad1[i] in sonPath:
                compatibleLetter = False
                
                tempI = i
                while compatibleLetter == False:

                    if dad1[sonPath.index(dad1[tempI])] in sonPath:
                       tempI = sonPath.index(dad1[tempI])
                    else:
                        compatibleLetter = True
                        sonPath[i] = dad1[sonPath.index(dad1[tempI])]
            else:
                sonPath[i] = dad1[i]    

        i += 1

    

    return(sonPath)

def CrossoverOX(couple,graph):
    """Crossover a couple of inds using the OX technique"""
    #rm = "OX"
    #Get strand size
    a = random.randint(1,len(couple[0].path)-3)
    b = random.randint(a+1,len(couple[0].path)-2)
    
    # Get random 1 and 2 dad
    dad1 = random.randint(0,1)
    dad2 = int(not bool(dad1))
    dads = []
    dads.append(dad1)
    dads.append(dad2)
    dad1 = couple[dad1].path
    dad2 = couple[dad2].path
    
    sonPath = [1] * len(dad2)


    while a <= b:
        sonPath[a] = dad2[a]
        a +=1

    i = 1
    j = 1
    while i < len(dad1)-1:
    
        if sonPath[i] != 1:
            i += 1
            continue #check if working
        else :
            while dad1[j] in sonPath:
                j += 1
            sonPath[i] = dad1[j]  
        i += 1

    if CheckIfPossible(sonPath,graph):
        return(sonPath)
    else: 
        return CrossoverOX(couple,graph)
    

def CheckIfPossible(path,graph):
    """Checks if the path is possible according to the graph."""
    i=0
    while i < len(path)-2:
        if graph.IsConnected(i,i+1):
            pass
        else:
            return False
        i += 1
    return True

def SelectCouple(population,graph,gen):
    """Selects a couple based on the score."""
    roullet = []
    couple = []
    couplef = []
    for ind in population: 
        roullet.append(ind.CalculateProbability())

    probSum = sum(roullet)

    for i in range(0,len(roullet)):
        roullet[i] = roullet[i] / probSum
    
    if gen % 10 == 11:
        couple.append(np.random.choice(population,2,p=roullet))
        couplef.append(couple[0][0])
        couple.append(np.random.choice(population,2,p=list(reversed(roullet))))
        couplef.append(couple[1][0])
        return couplef
    else:
        return  np.random.choice(population,2,p=roullet)


def MutateThrors(ind,graph):
    """Decides wether to mutate or not and returns the result mutated or not, using the Thrors tecnique."""
     #mm = "Thrors"
    pathBackup = ind.path

    if np.random.choice([False,True],1,p=[1-mutationRate,mutationRate]):

        while True:
            a,b,c = 0,0,0
            ind.path = pathBackup
            
            a = random.randint(1,len(ind.path)-4)
            b = random.randint(a+1,len(ind.path)-3)
            c = random.randint(b+1,len(ind.path)-2)

            ind.path[a], ind.path[b] , ind.path[c] = ind.path[c], ind.path[a], ind.path[b] # Melhor coisa <3

            if CheckIfPossible(ind.path,graph):
                ind.mutated = True
                return ind
    else:
        return ind

def MutateNormal(ind,graph):
    """Decides wether to mutate or not and returns the result mutated or not."""
    mm += "Normal"
    pathBackup = ind.path

    if np.random.choice([False,True],1,p=[1-mutationRate,mutationRate]):

        while True:
            a,b = 0,0
            ind.path = pathBackup
            while a == b:
                a = random.randint(1,len(ind.path)-4)
                b = random.randint(a+1,len(ind.path)-2)

            ind.path[a], ind.path[b] = ind.path[b], ind.path[a] # Melhor coisa <3

            if CheckIfPossible(ind.path,graph):
                ind.mutated = True
                return ind
    else:
        return ind
    
    

def Reproduce(population,graph,gen):
    """Will choose and reproduce the inds in your population"""
    i = 1
    while i <= killPop:

        couple = SelectCouple(population,graph,gen)
        son    = Individual(CrossoverOX(couple, graph)) # Choose crossover MPX or OX------------------------------------------
        population.pop(-i)
        population.append(MutateThrors(son,graph)) # Choose between Normal or Thrors-----------------------------------
        i += 1
        
        
def ShowResults(population,n):
    """Shows the results of the poopulation"""
    if n % 100 == 0:
        plt.clf()

    if n % 10 == 0:
        plt.hist(list(map(lambda i: i.score,population)), density=True, bins='auto')
        plt.ion()
        plt.show()
        plt.pause(0.001)
        #print("\nGeneration-----",n,"\nBest ind - ",population[0],"\nWorst ind - ", population[-1])
        #print(population)
   





def Main(sizePop,rawGraph,lastBestPath = []):
    """ Main Pipeline."""

    startTime = time.perf_counter(); 

    graph = Graph(len(rawGraph) - 1,rawGraph)


    population = GeneratePopulation(sizePop,graph)
    if lastBestPath:
        population[0].path = lastBestPath[:]


    i = 0
    #population[-1].path = [1,25,24,23,26,22,21,17,18,20,19,16,11,12,13,15,14,10,9,8,7,5,6,4,3,2,1 ] 
    
    stdTemp = 999 # best std
    stdCount = 0
    stdCountRestart = 50

    while i <= 10000:
 
        Fitness(population,graph)
        ShowResults(population,i)
        
        print("Geração: "+ str(i) + ", Best: " + str(population[0]) + ", Worst: " + str(population[-1]) + ". In " +str(int((time.perf_counter() - startTime) / 60))+"m"+str(int((time.perf_counter() - startTime)%60)) +"s" )
        Reproduce(population,graph,i)
        i += 1
        
        #print(np.std(list(map(lambda x: x.score,population))))
        desvioPadrao = np.std(list(map(lambda x: x.score,population)))
        print("\nDesvio padrão: " + str(desvioPadrao))
        if stdTemp == desvioPadrao:
            stdCount +=1
            if stdCount >= stdCountRestart:
                #Main(sizePop,rawGraph,population[0].path)
                break
        else:
            stdTemp = desvioPadrao
            stdCount = 0


    Fitness(population,graph)
    ShowResults(population,i)
    print ("\nDemorou " +str(int((time.perf_counter() - startTime) / 60)) + " minutos e " + str(int((time.perf_counter() - startTime)%60)) + " segundos e " + str(i) + " gerações.")
    print(population[0].path)
    print ("\n\n#Best found(Mutation"+mm+" and Reproduction"+ rm +")  = Score: "+ str(population[0].score) +", size: "+ str(sizePop) +", kill: "+str(killPop)+", mutationRate: "+str(mutationRate)+", time: "+str(int((time.perf_counter() - startTime) / 60))+"m"+str(int((time.perf_counter() - startTime)%60)) +"s, GenN: "+str(i)+", path: "+str(population[0].path)+" ")
    playsound('finished.mp3')

    plt.hist(list(map(lambda i: i.score,population)), density=True, bins='auto')
    plt.show()
    plt.pause(300)
    #print(population[2].score)   

   # print(population)


# Setings ----------------------------------------------------

sizePop = 1000
killPop = 300
mutationRate = 0.02

# Start of code -------------------------------------------

Main(sizePop,Graphs.graphE)



