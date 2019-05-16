class Ants:
    """ Class of Ants."""

    def SetProb(self,x,index = -10):
        if index == -10:
            self.prob.append(x)
        else:
            self.prob[index] = x
        
    def AddPath(self,citie):
        self.path.append(citie)
        self.prob.clear()
        self.visibility[citie] = 0
    

    def __init__(self, size, initialCity):
        self.visibility = [1 for x in range(size)]
        self.visibility[initialCity] = 0
        self.initialCity = initialCity
        self.path = []
        self.path.append(int(initialCity))
        self.prob = []

    def __repr__(self):
        """print the score when the object is called by print"""
        return str(self.visibility)
