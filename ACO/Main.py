
"""
What to do:

    ( ) Randomly place ants at the cities

    -- For each ant:

        ( ) Choose a not yet visited city until tour is completed
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






def main():
    print(Graphs.graphA)

#------------------------Settings-------------------------------------




main()









