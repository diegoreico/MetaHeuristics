from Loader import Loader
from Heuristics import BestFirstHeuristic


class Main:

    def __init__(self):
        """ load from file """
        loader = Loader()
        data = loader.load()
        """ # select an heuristic """

        heuristic = BestFirstHeuristic()

        print(data)

if __name__ == '__main__':
    Main()