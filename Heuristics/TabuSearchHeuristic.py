from Heuristics.AbstactHeuristic import AbstractHeuristic
from DataSet import DataSet
import sys


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
        tmpBestSolutionCost = self.calculateCost(solution)
        bestSolution = solution
        bestSolutionCost = tmpBestSolutionCost

        maxIterations=10000
        maxPermutes = 0
        iterations = 0
        totalIterations = 0
        totalEncontrados = 0
        iterationsWithoutUPgrade =0

        # calculates the number of the current search space to know when to stop

        maxRowElems = len(exploredataset.value[-1])
        maxPermutes += (maxRowElems * (maxRowElems - 1))/2

        sys.stdout.write("\nSOLUCION S_"+ str(totalEncontrados) + " -> "+ str(tmpBestSolution)+ "; "+ str(tmpBestSolutionCost)+"km")

        # explores the current search space
        while totalIterations < maxIterations:
            # cost of the current solution
            lastCost = self.calculateCost(dataset,solution)

            sys.stdout.write("\n\tVECINO V_"+str(iterations)+" -> Intercambio: ")

            # explores a new solution
            tmpSolution = self.permute(dataset, exploredataset, list(solution))

            # cost of the new solution
            newCost = self.calculateCost(dataset, tmpSolution)

            if tmpSolution is not in self._tabu:
                if newCost < tmpBestSolutionCost:
                        tmpBestSolutionCost = newCost
                        tmpBestSolution = tmpSolution


            sys.stdout.write(" "+ str(tmpSolution)+ "; "+ str(newCost)+"km")

            iterations += 1
            totalIterations +=1

            """
                if the new solution is better than the old, then the current solution is the new solution.
                The explored data set must be set do default values
            """
            if iterations < maxPermutes:

                solution = tmpBestSolution
                lastCost = tmpBestSolutionCost


                #refacer

                iterations = 0
                totalEncontrados+=1


                sys.stdout.write("\n\nSOLUCION S_"+ str(totalEncontrados)+ " -> "+ str(solution)+ "; "+ str(lastCost)+"km")

        return solution

    def permute(self, solution=None,X,Y):

        """

        :param dataset: full search space represented as an object of the class DataSet
        :param exploredataset: explored soluutions using the current solution as base
        :param solution: one dimensional array with the base solution to use
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