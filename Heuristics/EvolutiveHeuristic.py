from Heuristics.AbstactHeuristic import AbstractHeuristic
from DataSet import DataSet
from copy import deepcopy
import sys
import unittest


class EvolutiveHeuristic(AbstractHeuristic):

    """
        Calculates a solution using the current heuristic
    """

    def __init__(self,randomGenerator=None):
        super().__init__(randomGenerator)
        self._tabu = []
        self._lastTabu =[]
        self._tabuSize = 50
        self._lastSoluionsCostSize = 10

    def calculate(self, dataset=None, solution=None, exploredataset=None):

        if solution is None:
            solution = self.generateGreedySolution(dataset)


        return solution

    def orderCroosOver(self,p1, p2, h1, h2, i1, i2):
        filled = 0

        for i in range(len(p1)):
            h1[i] = 0
            h2[i] = 0

        i = i1
        while i <= i2:

            h1[i] = p1[i]
            h2[i] = p2[i]

            i+=1
            filled += 1

        actual = index = i2+1

        while filled < len(p1):

            if p2[index] not in h1:
                h1[actual] = p2[index]
                filled += 1

                actual += 1
                actual = actual % len(p1)

            index += 1
            index = index % len(p1)

        filled = i2 - i1+1
        actual = index = i2 + 1

        while filled < len(p1):

            if p1[index] not in h2:
                h2[actual] = p1[index]
                filled += 1

                print(filled)

                actual += 1
                actual = actual % len(p1)

            index += 1
            index = index % len(p1)


class TestingHeuristic(unittest.TestCase):


    def test_orderCrossOver(self):

        heuristic = EvolutiveHeuristic()

        p1 = [1, 2, 3, 4, 5, 6]
        p2 = [6, 5, 4, 3, 2, 1]
        h1 = list(p1)
        h2 = list(p2)
        i1 = 1
        i2 = 3

        heuristic.orderCroosOver(p1, p2, h1, h2, i1, i2)

        self.assertEqual(h1, [5,2,3,4,1,6], "El hijo uno se ha generado mal")
        self.assertEqual(h2, [2,5,4,3,6,1], "El hijo dos se ha generado mal")

if __name__ == '__main__':
    unittest.main()