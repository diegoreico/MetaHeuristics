from Loader import Loader
from Heuristics.BestFirstHeuristic import BestFirstHeuristic


class Main:

    def __init__(self):
        """ load from file """
        loader = Loader()
        data = loader.load()
        """ # select an heuristic """

        heuristic = BestFirstHeuristic()

        print("\n ",data.value)
        print("\n ",heuristic.generateRandomSolution(data.value))

if __name__ == '__main__':
    Main()