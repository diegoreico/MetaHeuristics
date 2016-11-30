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

        text = ""

        tmpBestSolution= solution
        tmpBestSolutionCost = self.calculateCost(dataset,solution)
        bestSolution = solution
        bestSolutionCost = tmpBestSolutionCost

        maxIterations=10000
        maxPermutes = 0

        totalIterations = 1

        iterationsWithoutUpgrade =0

        x = 0
        y = 0
        numberOfRestarts=0
        bestIteration=0

        # calculates the number of the current search space to know when to stop
        maxRowElems = len(dataset.value[-1])
        maxPermutes += (maxRowElems * (maxRowElems - 1))/2

        text=text+("RECORRIDO INICIAL\n\tRECORRIDO: ")
        for k in range(0, len(tmpBestSolution)):
            text=text+(str(tmpBestSolution[k])+" ")

        text=text+("\n\tCOSTE (km):" + str(tmpBestSolutionCost))

        print(text)
        text=""

        # explores the current search space
        while totalIterations <= maxIterations:

            if(iterationsWithoutUpgrade == 100):
                self._tabu=[]
                solution=bestSolution
                numberOfRestarts+=1
                iterationsWithoutUpgrade=0
                text=text+("\n***************\nREINICIO:" + str(numberOfRestarts) + "\n***************");

            text=text+("\nITERACION: " + str(totalIterations))

            # cost of the current solution
            lastCost = self.calculateCost(dataset, solution)
            tmpBestSolutionCost = lastCost*2

            for i in range(0,len(solution)):
                for j in range(0, i):

                    if [i,j] not in self._tabu and i != j:

                        # explores a new solution
                        tmpSolution = self.permute(list(solution), i, j)

                        # cost of the new solution
                        newCost = self.calculateCost(dataset, tmpSolution)

                        if newCost < tmpBestSolutionCost:
                                tmpBestSolutionCost = newCost
                                tmpBestSolution = tmpSolution
                                x = i
                                y = j


            """
                if the new solution is better than the old, then the current solution is the new solution.
                The explored data set must be set do default values
            """

            text=text+("\n\tINTERCAMBIO: ("+str(x)+", "+str(y)+")\n\tRECORRIDO: ")

            for k in range(0,len(tmpBestSolution)):
                text=text+(str(tmpBestSolution[k])+" ")

            text=text+("\n\tCOSTE (km): " + str(tmpBestSolutionCost))

            solution = tmpBestSolution
            lastCost = tmpBestSolutionCost

            if bestSolutionCost > lastCost:
                bestSolutionCost = lastCost
                bestSolution = list(solution)
                bestIteration = totalIterations
                iterationsWithoutUpgrade = 0
            else:
                iterationsWithoutUpgrade += 1

            text=text+("\n\tITERACIONES SIN MEJORA: " + str(iterationsWithoutUpgrade))

            self._tabu.append([x,y])

            if len(self._tabu) > 100:
                self._tabu.pop(0)

            text=text+("\n\tLISTA TABU:")
            for u in range(0,len(self._tabu)):
                text=text+("\n\t"+str(self._tabu[u][0])+" "+str(self._tabu[u][1]))

            text=text+("\n")
            totalIterations += 1
            sys.stdout.write(text)
            text=""

        text=text+("\n\nMEJOR SOLUCION:\n\tRECORRIDO: ")
        for k in range(0, len(tmpBestSolution)):
            text=text+(str(tmpBestSolution[k]) + " ")

        text=text+("\n\tCOSTE (km):" + str(tmpBestSolutionCost) + "\n\tITERACION:"+ str(bestIteration))

        sys.stdout.write(text)

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