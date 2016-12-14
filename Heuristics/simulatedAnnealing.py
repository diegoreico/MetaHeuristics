from Heuristics.AbstactHeuristic import AbstractHeuristic
from DataSet import DataSet
import sys
import unittest


class TabuSearchHeuristic(AbstractHeuristic):

    """
        Calculates a solution using the current heuristic
    """

    def __init__(self,randomGenerator=None):
        super().__init__(randomGenerator)

    def calculate(self, dataset=None, solution=None, exploredataset=None):



if __name__ == '__main__':
    unittest.main()