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
        self._tabu = []

    def calculate(self, dataset=None, solution=None, exploredataset=None):

        if solution is None:
            solution = self.generateRandomSolution(dataset)

        tmpBestSolution= solution
        tmpBestSolutionCost = self.calculateCost(dataset,solution)
        bestSolution = solution
        bestSolutionCost = tmpBestSolutionCost

        maxIterations=10000
        maxPermutes = 0

        iterations = 0
        totalIterations = 0

        totalEncontrados = 0

        iterationsWithoutUpgrade =0

        x = 0
        y = 0

        # calculates the number of the current search space to know when to stop
        maxRowElems = len(dataset.value[-1])
        maxPermutes += (maxRowElems * (maxRowElems - 1))/2

        # explores the current search space
        while totalIterations < maxIterations:

            for i in range(0,len(dataset.value[-1])-1):
                for j in range(0, i):

                    # cost of the current solution
                    lastCost = self.calculateCost(dataset,solution)

                    # explores a new solution
                    tmpSolution = self.permute(list(solution),i,j)

                    # cost of the new solution
                    newCost = self.calculateCost(dataset, tmpSolution)

                    if [i,j] not in self._tabu:
                        if newCost < tmpBestSolutionCost:
                                tmpBestSolutionCost = newCost
                                tmpBestSolution = tmpSolution
                                x = i
                                y = j

                    iterations += 1
                    totalIterations +=1

            """
                if the new solution is better than the old, then the current solution is the new solution.
                The explored data set must be set do default values
            """


            solution = tmpBestSolution
            lastCost = tmpBestSolutionCost

            self._tabu.append([x,y])

            if len(self._tabu) > 100:
                self._tabu = self._tabu[1:-1]

            #refacer

            iterations = 0
            totalEncontrados+=1

        return solution

    def permute(self, solution,X,Y):
        """"
        :param solution: one dimensional array with the base solution to use
        :param X: one position to permute
        :param Y: the other position to permute
        :return:
        """

        if solution is None:
            return []

        aux = solution[X]
        solution[X] = solution[Y]
        solution[Y] = aux

        if X > Y:
            sys.stdout.write("("+str(X)+", "+str(Y)+");")
        else:
            sys.stdout.write("(" + str(Y) + ", " + str(X) + ");")

        return solution

class TestingHeuristic(unittest.TestCase):


    def test_permute(self):

        solution = [1, 2, 3, 4, 5, 6]
        solutionExpected = [1, 2, 4, 3, 5, 6]
        X=2
        Y=3

        heuristic = TabuSearchHeuristic()

        self.assertEqual(heuristic.permute(solution,X,Y), solutionExpected)

    def test_permute_extremes(self):

        solution = [1, 2, 3, 4, 5, 6]
        solutionExpected = [6, 2, 3, 4, 5, 1]
        X = 0
        Y = len(solution)-1


        heuristic = TabuSearchHeuristic()

        self.assertEqual(heuristic.permute(solution, X, Y), solutionExpected)

if __name__ == '__main__':
    unittest.main()