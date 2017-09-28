#!/usr/bin/env python3
from Loader import Loader
from Utils.RandomGenerator import RandomGenerator
from Heuristics.BestFirstHeuristic import BestFirstHeuristic
from Heuristics.TabuSearchHeuristic import TabuSearchHeuristic
from Heuristics.SimulatedAnnealing import SimulatedAnnealing
from Heuristics.EvolutiveHeuristic import EvolutiveHeuristic

import sys

class Main:

    #TODO:delete unused objects

    def __init__(self):
        """ load from file """
        loader = None
        randomG = None

        if len(sys.argv) > 1:
            loader = Loader(sys.argv[1])
        else:
            loader = Loader()

        dataSet = loader.load()

        if len(sys.argv) > 2:
            randomG = RandomGenerator(sys.argv[2])
        else:
            randomG = RandomGenerator()

        """ select an heuristic """

        # heuristic = BestFirstHeuristic(randomG)
        heuristic = EvolutiveHeuristic(randomG)

        #print("\n\tExplore data set: ", dataSet.value)

        #print("\nRANDOM SOLUTION: ",solution)
        #print("\nCOST OF SOLUTION: ",heuristic.calculateCost(dataSet,solution))

        solution = heuristic.calculate(dataSet)

        # print("\nBEST SOLUTION: ",solution)
        # print("\nCOST OF SOLUTION: ",heuristic.calculateCost(dataSet,solution))

if __name__ == '__main__':
    Main()

