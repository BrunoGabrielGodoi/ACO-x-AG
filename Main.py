
class individual:
    path = ""

    def __init__(self, path):
        self.path = path



def main():
    i1 = individual("4,5,6,7,8")
    print(i1.path)   



main()


