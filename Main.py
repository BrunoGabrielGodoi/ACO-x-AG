import random

class Individual:

    def __init__(self, path):
        self.path = path


class Graph:

    def __init__(self, size, arestas):
        self.size = size
        self.arestas = arestas

    def IsConnected(self,a,b):
        if self.arestas[a][b] != 0:
            return True
        else: 
            return False


def GeneratePopulation(sizeOfPopulation, graph):
  
    path = [1]
    population = []  

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

                elif ErrorCounter > (graph.size*4): # Tester no futuro se isso está funcionando mesmo

                    path.clear()
                    path.append(1)
                    j = 1
                    ErrorCounter = 0
            j += 1
        population.append(Individual(path))
        print(i,"-",path)
        path.clear()
        path.append(1)

    return population






def Main():

    graphSize = 5
    graphA = [  [0,1,2,3,4,5],
                [1,0,2,0,3,6],
                [2,2,0,4,3,0],
                [3,0,4,0,7,3],
                [4,3,3,7,0,3],
                [5,6,0,3,3,0]]

    graph = Graph(graphSize,graphA)

       
    population = GeneratePopulation(1000,graph)
    
   # print(population)



Main()


