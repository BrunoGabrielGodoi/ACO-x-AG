
class Individual:

    def __init__(self, path):
        self.path = path

class Graph:

    def __init__(self, path):
        self.path = path


def Main():
    graph = ["A","B","C","D","E","F"]
    i1 = Individual(graph)
    print(i1.path[1])   




Main()


