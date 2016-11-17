from Loader import Loader
from Heuristics.BestFirstHeuristic import BestFirstHeuristic


class Main:

    #TODO:delete unused objects

    def __init__(self):
        """ load from file """
        loader = Loader()
        dataSet = loader.load()
        """ # select an heuristic """

        print("\nVALOR XY: ",dataSet.getValueXY(0,0))

        heuristic = BestFirstHeuristic()

        heuristic.generateDefaultExploredDataset(dataSet)

        solution = heuristic.generateRandomSolution(dataSet)
        print("\nRANDOM SOLUTION: ",solution)
        print("\nCOST OF SOLUTION: ",heuristic.calculateCost(dataSet,solution))

if __name__ == '__main__':
    Main()