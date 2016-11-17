from Loader import Loader
from Heuristics.BestFirstHeuristic import BestFirstHeuristic


class Main:

    #TODO:delete unused objects

    def __init__(self):
        """ load from file """
        loader = Loader()
        dataSet = loader.load()
        """ # select an heuristic """

        heuristic = BestFirstHeuristic()
        exploredDataSet = heuristic.generateDefaultExploredDataset(dataSet)
        solution = heuristic.generateRandomSolution(dataSet)

        print("\n\tExplore data set: ", dataSet.value)

        print("\nRANDOM SOLUTION: ",solution)
        print("\nCOST OF SOLUTION: ",heuristic.calculateCost(dataSet,solution))

        solution = heuristic.calculate(dataSet,exploredDataSet,solution)

        print("\nBEST SOLUTION: ",solution)
        print("\nCOST OF SOLUTION: ",heuristic.calculateCost(dataSet,solution))

if __name__ == '__main__':
    Main()