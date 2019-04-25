import random
import operator
import numpy as np 

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

    def CalculateProbability(self):
        """ calculate the probability normalized """
        return (1/(Individual.staticSumofScores*self.score))

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


def Crossover(couple,graph):

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

    #print(sonPath) # TESTAR SE ESTÀ POSSIVEL

    return(sonPath)

def CheckIfPossible(path,graph):

    i=0
    while i < len(path)-2:
        if graph.IsConnected(i,i+1):
            pass
        else:
            return False
        i += 1
    return True

def SelectCouple(population,graph):
    """Selects a couple based on the score."""
    roullet = []

    for ind in population: 
        roullet.append(ind.CalculateProbability())

    probSum = sum(roullet)

    for i in range(0,len(roullet)):
        roullet[i] = roullet[i] / probSum
    
    return np.random.choice(population,2,p=roullet)


def Mutate(ind,graph):
    """Decides wether to mutate or not and returns the result mutated or not."""
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
                return ind
    else:
        return ind
    
    

def Reproduce(population,graph):

    i = 1
    while i <= killPop:

        couple = SelectCouple(population,graph)
        son    = Individual(Crossover(couple, graph))
        population.pop(-i)
        population.append(Mutate(son,graph))
        i += 1
        
        
def ShowResults(population,n):
    if n % 100 == 0:
        print("\nGeneration-----",n,"\nBest ind - ",population[0],"\nWorst ind - ", population[-1])
        print(population)


def Main(sizePop,rawGraph):
    """ Main Pipeline."""


    graph = Graph(len(rawGraph) - 1,rawGraph)

       
    population = GeneratePopulation(sizePop,graph)
    i = 0
    while i <= 1000:
        if i % 10 == 0:
            print(".")
        Fitness(population,graph)
        ShowResults(population,i)
        Reproduce(population,graph)
        i += 1
        

    #print(population[2].score)   

   # print(population)


# Setings ----------------------------------------------------

sizePop = 300
killPop = 30
mutationRate = 0.2

graphA = [  [0,1,2,3,4,5],
            [1,0,2,0,3,6],
            [2,2,0,4,3,0],
            [3,0,4,0,7,3],
            [4,3,3,7,0,3],
            [5,6,0,3,3,0] ]

#Best answer found 118

graphB = [  [0,1,2 ,3 ,4 ,5 ,6], 
            [1,0,24,30,27,17,25],
            [2,24,0,18,20,23,19],
            [3,30,18,0,19,32,19],
            [4,27,20,19,0,32,16],
            [5,17,23,32,41,0,28],
            [6,25,19,19,16,28,0], ]

#Best answer = 98
#Best Found  = 98
graphC = [  [0,1 ,2 ,3 ,4 ,5 ,6, 7, 8], 
            [1,0,13,13,12,12,13,14,12],
            [2,13,0,14,14,13,14,13,12],
            [3,13,14,0,13,13,12,12,12],
            [4,12,14,13,0,13,13,13,13],
            [5,12,13,13,13,0,13,12,13],
            [6,13,14,12,13,13,0,12,12],
            [7,14,13,12,13,12,12,0,12],
            [8,12,12,12,13,13,12,12,0] ]
[
[0,83,93,129,133,139,151,169,135,114,110, 98, 99, 95, 81,152,159,181,172,185,147,157,185,220,127,181],
83   0  40  53  62  64  91 116  93  84  95  98  89  68  67 127 156 175 152 165 160 180 223 268 179 197
93  40   0  42  42  49  59  81  54  44  58  64  54  31  36  86 117 135 112 125 124 147 193 241 157 161
129  53  42   0  11  11  46  72  65  70  88 100  89  66  76 102 142 156 127 139 155 180 228 278 197 190
133  62  42  11   0   9  35  61  55  62  82  95  84  62  74  93 133 146 117 128 148 173 222 272 194 182
139  64  49  11   9   0  39  65  63  71  90 103  92  71  82 100 141 153 124 135 156 181 230 280 202 190
151  91  59  46  35  39   0  26  34  52  71  88  77  63  78  66 110 119  88  98 130 156 206 257 188 160
169 116  81  72  61  65  26   0  37  59  75  92  83  76  91  54  98 103  70  78 122 148 198 250 188 148
135  93  54  65  55  63  34  37   0  22  39  56  47  40  55  37  78  91  62  74  96 122 172 223 155 128
114  84  44  70  62  71  52  59  22   0  20  36  26  20  34  43  74  91  68  82  86 111 160 210 136 121
110  95  58  88  82  90  71  75  39  20   0  18  11  27  32  42  61  80  64  77  68  92 140 190 116 103
98  98  64 100  95 103  88  92  56  36  18   0  11  34  31  56  63  85  75  87  62  83 129 178 100  99
99  89  54  89  84  92  77  83  47  26  11  11   0  23  24  53  68  89  74  87  71  93 140 189 111 107
95  68  31  66  62  71  63  76  40  20  27  34  23   0  15  62  87 106  87 100  93 116 163 212 132 130
81  67  36  76  74  82  78  91  55  34  32  31  24  15   0  73  92 112  96 109  93 113 158 205 122 130
152 127  86 102  93 100  66  54  37  43  42  56  53  62  73   0  44  54  26  39  68  94 144 196 139  95
159 156 117 142 133 141 110  98  78  74  61  63  68  87  92  44   0  22  34  38  30  53 102 154 109  51
181 175 135 156 146 153 119 103  91  91  80  85  89 106 112  54  22   0  33  29  46  64 107 157 125  51
172 152 112 127 117 124  88  70  62  68  64  75  74  87  96  26  34  33   0  13  63  87 135 186 141  81
185 165 125 139 128 135  98  78  74  82  77  87  87 100 109  39  38  29  13   0  68  90 136 186 148  79
147 160 124 155 148 156 130 122  96  86  68  62  71  93  93  68  30  46  63  68   0  26  77 128  80  37
157 180 147 180 173 181 156 148 122 111  92  83  93 116 113  94  53  64  87  90  26   0  50 102  65  27
185 223 193 228 222 230 206 198 172 160 140 129 140 163 158 144 102 107 135 136  77  50   0  51  64  58
220 268 241 278 272 280 257 250 223 210 190 178 189 212 205 196 154 157 186 186 128 102  51   0  93 107
127 179 157 197 194 202 188 188 155 136 116 100 111 132 122 139 109 125 141 148  80  65  64  93   0  90
181 197 161 190 182 190 160 148 128 121 103  99 107 130 130  95  51  51  81  79  37  27  58 107  90   0

# Start of code -------------------------------------------
Main(sizePop,graphC)


