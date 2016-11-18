from Heuristics.AbstactHeuristic import AbstractHeuristic
from DataSet import DataSet
import random as random


class BestFirstHeuristic(AbstractHeuristic):

    """
        Calculates a solution using the current heuristic
    """

    def calculate(self, dataset=None, solution=None, exploredataset=None):

        if solution is None:
            solution = self.generateRandomSolution(dataset)

        if exploredataset is None:
            exploredataset = self.generateDefaultExploredDataset(dataset)

        maxPermutes = 0
        iterations = 0

        # calculates the number of the current search space to know when to stop
        for i in range(0,len(exploredataset.value)):
            maxPermutes += len(exploredataset.value[i])

        print("\nNumero maximo de permutacions ", maxPermutes)

        # explores the current search space
        while iterations < maxPermutes:
            # cost of the current solution
            lastCost = self.calculateCost(dataset,solution)
            # explores a new solution
            newSolution = self.permute(dataset, exploredataset, list(solution))
            # cost of the new solution
            newCost = self.calculateCost(dataset,newSolution)
            iterations += 1

            """
                if the new solution is better than the old, then the current solution is the new solution.
                The explored data set must be set do default values
            """
            if newCost < lastCost:
                iterations = 0
                solution = newSolution
                for i in range(0,len(exploredataset.value)):
                    for j in range(0,len(exploredataset.value[i])):
                        exploredataset.value[i][j] = 0

        return solution

    def permute(self, dataset=None, exploredataset=None, solution=None):

        """

        :param dataset: full search space represented as an object of the class DataSet
        :param exploredataset: explored soluutions using the current solution as base
        :param solution: one dimensional array with the base solution to use
        :return:
        """

        if solution is None:
            return []

        if dataset is None:
            return solution

        if exploredataset is None:
            return solution

        # generates 2 different random elements to permute
        X = random.randint(0, len(dataset.value[-1]) - 2)
        Y = random.randint(0, len(dataset.value[-1]) - 2)

        while Y is X:
            Y = random.randint(0, len(dataset.value[-1]) - 2)

        # while the solution was already generated, we try to generate an unused solution
        while exploredataset.getValueXY(X, Y) == 1:

            """
            0           0           0           0           0
            1 1     ->  x 1     ->  1 x   ->    1 1     ->  1 1
            0 1 0       0 1 0       0 1 0       x 1 0       1 1 0
            """


            if X > Y:
                aux = X
                X = Y
                Y = aux

            lengthX = len(exploredataset.value[Y])
            lengthY = len(exploredataset.value)
            X += 1

            if (X >= lengthX):
                X = 0
                lengthX = len(exploredataset.value[Y])
                Y += 1

            if (Y >= lengthY):
                Y = 0
                lengthX = len(exploredataset.value[Y])

        exploredataset.setValueXY(X, Y, 1)

        aux = solution[X]
        solution[X] = solution[Y]
        solution[Y] = aux

        return solution

    def generateDefaultExploredDataset(self, dataset):

        """
        Generates a dataset filled with 0s and with the size of the dataset

        :param dataset: full search space represented as an object of the class DataSet
        :return:
        """

        exploredValues = []

        for i in range(0, len(dataset.value)):
            exploredValues.append([])
            for j in range(0, len(dataset.value[i])):
                exploredValues[i].append(0)

            print(exploredValues[i])

        return DataSet(exploredValues)
