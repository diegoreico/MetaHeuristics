from Heuristics.AbstactHeuristic import AbstractHeuristic
from DataSet import DataSet
import sys


class BestFirstHeuristic(AbstractHeuristic):

    """
        Calculates a solution using the current heuristic
    """

    def __init__(self,randomGenerator=None):
        super().__init__(randomGenerator)

    def calculate(self, dataset=None, solution=None, exploredataset=None):

        if solution is None:
            solution = self.generateRandomSolution(dataset)

        if exploredataset is None:
            exploredataset = self.generateDefaultExploredDataset(dataset)

        maxPermutes = 0
        iterations = 0
        totalIterations = 0
        totalEncontrados = 0

        # calculates the number of the current search space to know when to stop

        maxRowElems = len(exploredataset.value[-1])
        maxPermutes += (maxRowElems * (maxRowElems - 1))/2

        lastCost = self.calculateCost(dataset, solution)

        sys.stdout.write("\nSOLUCION S_"+ str(totalEncontrados) + " -> "+ str(solution)+ "; "+ str(lastCost)+"km")

        # explores the current search space
        while iterations < maxPermutes:
            # cost of the current solution
            lastCost = self.calculateCost(dataset,solution)

            sys.stdout.write("\n\tVECINO V_"+str(iterations)+" -> Intercambio: ")

            # explores a new solution
            newSolution = self.permute(dataset, exploredataset, list(solution))

            # cost of the new solution
            newCost = self.calculateCost(dataset,newSolution)

            sys.stdout.write(" "+ str(newSolution)+ "; "+ str(newCost)+"km")



            iterations += 1
            totalIterations +=1

            """
                if the new solution is better than the old, then the current solution is the new solution.
                The explored data set must be set do default values
            """
            if newCost < lastCost:
                iterations = 0
                totalEncontrados+=1
                solution = newSolution
                lastCost = newCost
                sys.stdout.write("\n\nSOLUCION S_"+ str(totalEncontrados)+ " -> "+ str(solution)+ "; "+ str(lastCost)+"km")

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
        X = self.randomGenerator.getRandomInt(0, len(solution))
        Y = self.randomGenerator.getRandomInt(0, len(solution))

        # print("\nGeneracion X:",X," Y:",Y)


        if X > Y:
            aux = X
            X = Y
            Y = aux

        #print("\nPERMUTA primero:",X,",segundo:",Y)

        # while the solution was already generated, we try to generate an unused solution
        while exploredataset.getValueXY(X, Y) == 1 or X==Y:

            """
            0           0           0           0           0
            1 1     ->  x 1     ->  1 x   ->    1 1     ->  1 1
            0 1 0       0 1 0       0 1 0       x 1 0       1 1 0
            """

            lengthX = len(exploredataset.value[Y])-1
            lengthY = len(exploredataset.value)
            X += 1

            if (X >= lengthX):
                X = 0
                lengthX = len(exploredataset.value[Y])-1
                Y += 1

            if (Y >= lengthY):
                Y = 1
                lengthX = len(exploredataset.value[Y])

        # for k in range(0,len(exploredataset.value)):
        #     print("\n",exploredataset.value[k])

        exploredataset.setValueXY(X, Y, 1)

        aux = solution[X]
        solution[X] = solution[Y]
        solution[Y] = aux

        if X > Y:
            sys.stdout.write("("+str(X)+", "+str(Y)+");")
        else:
            sys.stdout.write("(" + str(Y) + ", " + str(X) + ");")

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

            #print(exploredValues[i])

        return DataSet(exploredValues)
