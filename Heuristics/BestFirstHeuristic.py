from Heuristics.AbstactHeuristic import AbstractHeuristic
from DataSet import DataSet
import random as random


class BestFirstHeuristic(AbstractHeuristic):

    def calculate(self, dataset=None, exploredataset=None, solution=None):

        maxPermutes = 0
        iterations = 0

        for i in range(0,len(exploredataset.value)):
            maxPermutes += len(exploredataset.value[i])

        print("\nNumero maximo de permutacions ", maxPermutes)

        while iterations < maxPermutes:
            lastCost = self.calculateCost(dataset,solution)
            newSolution = self.permute(dataset, exploredataset, list(solution))
            newCost = self.calculateCost(dataset,newSolution)
            iterations += 1

            if newCost < lastCost:
                iterations = 0
                solution = newSolution
                for i in range(0,len(exploredataset.value)):
                    for j in range(0,len(exploredataset.value[i])):
                        exploredataset.value[i][j] = 0

        return solution

    def permute(self, dataset=None, exploredataset=None, solution=None):
        if solution is None:
            return []

        if dataset is None:
            return solution

        if exploredataset is None:
            return solution

        X = random.randint(0, len(dataset.value[-1]) - 2)
        Y = random.randint(0, len(dataset.value[-1]) - 2)

        while Y is X:
            Y = random.randint(0, len(dataset.value[-1]) - 2)

        while exploredataset.getValueXY(X, Y) == 1:
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
        exploredValues = []

        for i in range(0, len(dataset.value)):
            exploredValues.append([])
            for j in range(0, len(dataset.value[i])):
                exploredValues[i].append(0)

            print(exploredValues[i])

        return DataSet(exploredValues)
