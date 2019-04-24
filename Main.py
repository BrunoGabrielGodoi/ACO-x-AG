import random
import operator
import numpy as np 

sizePop = 50
killPop = 10
mutationRate = 0.02

graphSize = 5
graphA = [  [0,1,2,3,4,5],
            [1,0,2,0,3,6],
            [2,2,0,4,3,0],
            [3,0,4,0,7,3],
            [4,3,3,7,0,3],
            [5,6,0,3,3,0] ]

class Individual:
    """ Class of genes."""

    path = []
    score = 999
    staticSumofScores = 1 

    def __init__(self, path):
        self.path = path[:]
    
    def SetScore(self,x,sizeOfPop = 1):
        self.score = x
        self.probability = x/sizeOfPop

    def CalculateProbabiility(self):
        """ calculate the probability normalized """
        return self.score/Individual.staticSumofScores

    def __repr__(self):
        """print the score when the object is called by print"""
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

                temp = random.randint(1, 5) # 0,5 = 1-5
                a = path[-1]
                ErrorCounter += 1
                if graph.IsConnected(a,temp):

                    if temp not in path :
                        path.append(temp)
                        compatible = True
                    elif len(path) == 5:
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


def Crossover(couple):

    a = random.randint(1,len(couple[0].path)-4)
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

    print(sonPath)

    

def Reproduce(population):

    roullet = []

    for ind in population: 
        roullet.append(ind.CalculateProbabiility())

    Crossover(np.random.choice(population,2,roullet))



def Main(sizePop,graphA,graphSize):
    """ Main Pipeline."""


    graph = Graph(graphSize,graphA)

       
    population = GeneratePopulation(sizePop,graph)
    Fitness(population,graph)
    print(Reproduce(population))

    #print(population[2].score)   

   # print(population)


# Start of code -------------------------------------------
Main(sizePop,graphA,graphSize)


