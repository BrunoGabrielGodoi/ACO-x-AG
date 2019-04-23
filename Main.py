import random



class Individual:

    def __init__(self, path):
        self.path = path


class Graph:

    def __init__(self, size, arestas):
        self.size = size
        self.arestas = arestas


def GeneratePopulation(sizeOfPopulation):

    path = []

    for i in range(0,sizeOfPopulation):
        path.append(1)

        temp = random.randint(1, 5) # 0,5 = 1-5
        


def Main():

    graphSize = 5
    graphA = [  [X,1,2,3,4,5],
                [1,0,2,0,3,6],
                [2,2,0,4,3,0],
                [3,0,4,0,7,3],
                [4,3,3,7,0,3],
                [5,6,0,3,3,0]]

    graph = Graph(graphSize,graphA)

    print(i1.path[1])   
    population = GeneratePopulation()




Main()


