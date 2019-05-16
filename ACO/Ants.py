class Ants:
    """ Class of Ants."""


#Variables List-----
#prob = probablilitis to go to each city
#path = path so far
#visibility = if it has already gone to a city
#Distance = distance total
#initialCity = firstcity
#-------------------


    def SetProb(self,x,index = -10):
        if index == -10:
            self.prob.append(x)
        else:
            self.prob[index] = x
        
    def AddPath(self,citie):
        self.path.append(citie)
        self.prob.clear()
        self.visibility[citie] = 0

    def CalculateDistance(self,graph):
        sumD = 0
        i = 0
        while i < len(self.path)-1:
            sumD += graph[self.path[i]][self.path[i+1]] 
            i += 1
        self.Distance = sumD
            
    def AddPheromone(self,graphPhero,EvaporationRate):
        val = 1/self.Distance
        
        i = 0
        while i < len(self.path)-1:
            graphPhero[self.path[i]][self.path[i+1]] += val 
            i += 1
        return graphPhero
    

    def __init__(self, size, initialCity):
        self.visibility = [1 for x in range(size)]
        self.visibility[initialCity] = 0
        self.initialCity = initialCity
        self.path = []
        self.path.append(int(initialCity))
        self.prob = []

    def __repr__(self):
        """print the score when the object is called by print"""
        return str(self.path)
