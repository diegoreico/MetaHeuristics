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
        self._lastTabu =[]
        self._tabuSize = 50
        self._lastSoluionsCostSize = 10

    def calculate(self, dataset=None, solution=None, exploredataset=None):

        if solution is None:
            solution = self.generateGreedySolution(dataset)

        """
            LONG TIME MEMORY
        """
        maxDistance=dataset.value[0][0]
        minDistance=dataset.value[0][0]
        nu=0.005
        maxFrequency=1
        maxFrequencyOld=1

        # getting max and min distance
        for row in dataset.value:
            for value in row:
                if value < minDistance:
                    minDistance = value
                elif value > maxDistance:
                    maxDistance = value

        #dataset with the number of times that a path between cities was selected
        longTimeMemoryOld = longTimeMemory = DataSet()

        for i in range(0, len(dataset.value)):
            line = []
            for j in range(0,len(dataset.value[i])):
                line.append(0)

            longTimeMemory.value.append(line)


        listOfLastCots = []
        lastCostsAverage=0

        text = ""

        tmpBestSolution= solution
        tmpBestSolutionCost = self.calculateCost(dataset,solution)
        tmpBestSolutionOvercost=0

        bestSolution = solution
        bestSolutionCost = tmpBestSolutionCost
        bestSolutionOvercost=0

        maxIterations=10000

        totalIterations = 1
        iterationsWithoutUpgrade =0

        x = 0
        y = 0
        numberOfRestarts=0
        bestIteration=0

        text=text+("RECORRIDO INICIAL\n\tRECORRIDO: ")
        for k in range(0, len(tmpBestSolution)):
            text=text+(str(tmpBestSolution[k])+" ")

        text=text+("\n\tCOSTE (km): " + str(tmpBestSolutionCost))

        print(text)
        text=""

        # explores the current search space
        while totalIterations <= maxIterations:


            if(iterationsWithoutUpgrade == 100):
                self._tabu = []

            if len(listOfLastCots) == self._lastSoluionsCostSize and lastCostsAverage > bestSolutionCost:
                listOfLastCots=[]

                #TODO: funciona ben pero a lista tabu coa condicion que se usa para o if actualmente estase a borrar demasiado pronto
                #self._tabu = []

                nu +=0.001
                if nu > 0.10:
                    nu = -0.10

                solution = self.generateGreedySolutionWithMemory(dataset,longTimeMemory,nu,maxDistance,minDistance,maxFrequency)

                numberOfRestarts += 1
                iterationsWithoutUpgrade = 0

                text=text+("\n***************\nREINICIO: " + str(numberOfRestarts) + "\n***************\n");

            text=text+("\nITERACION: " + str(totalIterations))

            solutionOvercost=self.costUsingLongTimeMemory(longTimeMemory,solution,nu,maxDistance,minDistance,maxFrequency)
            # cost of the current solution
            lastCost = self.calculateCost(dataset, solution)

            tmpBestSolutionCost = self.calculateCostDifference(dataset, 1, 0, solution, lastCost)
            tmpBestSolutionOvercost = self.calculateOvercostDifference(longTimeMemory,longTimeMemoryOld, 1, 0, solution,nu,maxDistance,minDistance,maxFrequency,maxFrequencyOld, solutionOvercost)

            for i in range(0,len(solution)):
                for j in range(0, i):
                    if i != j and [i,j] not in self._tabu:
                        # explores a new solution
                        # cost of the new solution
                        newCost = self.calculateCostDifference(dataset, i, j, solution, lastCost)

                        overcost = self.calculateOvercostDifference(longTimeMemory,longTimeMemoryOld, i, j, solution,nu,maxDistance,minDistance,maxFrequency,maxFrequencyOld, solutionOvercost)

                        if newCost + overcost < tmpBestSolutionCost + tmpBestSolutionOvercost:
                                tmpBestSolutionOvercost = overcost
                                tmpBestSolutionCost = newCost
                                tmpBestSolution = self.permute(list(solution), i, j);

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

            listOfLastCots.append(lastCost)
            if len(listOfLastCots) == self._lastSoluionsCostSize:
                lastCostsAverage = sum(listOfLastCots)/len(listOfLastCots)

            if lastCost < bestSolutionCost:

                self._lastTabuu = list(self._tabu)

                maxFrequencyOld = maxFrequency

                # get the max frequency inside probability matrix
                for row in longTimeMemory.value:
                    for element in row:
                        if element > maxFrequency:
                            maxFrequency = element

                longTimeMemoryOld = deepcopy(longTimeMemory)
                self.updateLongTimeMemory(longTimeMemory, solution)

                bestSolutionCost = lastCost
                bestSolution = list(solution)
                bestIteration = totalIterations
                iterationsWithoutUpgrade = 0
            else:
                iterationsWithoutUpgrade += 1

            text=text+("\n\tITERACIONES SIN MEJORA: " + str(iterationsWithoutUpgrade))

            self._tabu.append([x,y])

            if len(self._tabu) > self._tabuSize:
                self._tabu.pop(0)

            text=text+("\n\tLISTA TABU:")
            for u in range(0,len(self._tabu)):
                text=text+("\n\t"+str(self._tabu[u][0])+" "+str(self._tabu[u][1]))

            text=text+("\n")
            totalIterations += 1
            sys.stdout.write(text)
            text=""

        text=text+("\n\nMEJOR SOLUCION: \n\tRECORRIDO: ")
        for k in range(0, len(tmpBestSolution)):
            text=text+(str(bestSolution[k]) + " ")

        text=text+("\n\tCOSTE (km): " + str(bestSolutionCost) + "\n\tITERACION: "+ str(bestIteration)+"\n")

        sys.stdout.write(text)

        for i in longTimeMemory.value:
            print(i)

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

    def updateLongTimeMemory(self,longTimeMemory,solution):

        longTimeMemory.setValueAdapt(0,solution[0],
                                    longTimeMemory.getValueAdapt(0,solution[0]) + 1)


        for i in range(0,len(solution)-1):
            longTimeMemory.setValueAdapt(solution[i], solution[i+1],
                                         longTimeMemory.getValueAdapt(solution[i], solution[i+1]) + 1)

        longTimeMemory.setValueAdapt(solution[-1], 0,
                                         longTimeMemory.getValueAdapt(solution[-1], 0) + 1)

    def costUsingLongTimeMemory(self,longTimeMemory,solution,nu,dmax,dmin,maxFrequency):

        overcost=0

        distance = dmax-dmin

        if maxFrequency != 0 :
            overcost += nu * distance * (longTimeMemory.getValueAdapt(0,solution[0])/maxFrequency)

            for i in range(0,len(solution)-1):
                overcost += nu * distance * (longTimeMemory.getValueAdapt(solution[i], solution[i+1]) / maxFrequency)

            overcost += nu * distance * (longTimeMemory.getValueAdapt(solution[-1], 0) / maxFrequency)

        return overcost

    def calculateOvercostDifference(self, dataset, datasetOld, i, j, solution, nu,dmax, dmin, maxFrequency, maxFrequencyOld, newCost):

        overcost = newCost

        distance = dmax - dmin

        if j + 1 != i:
            if i > 0:
                overcost -= nu * distance * (datasetOld.getValueAdapt(solution[i - 1], solution[i])/maxFrequencyOld)
                overcost += nu * distance * (dataset.getValueAdapt(solution[i - 1], solution[j])/maxFrequency)
            else:
                overcost -= nu * distance * (datasetOld.getValueAdapt(solution[i], 0)/maxFrequencyOld)
                overcost += nu * distance * (dataset.getValueAdapt(solution[j], 0)/maxFrequency)
        if i < len(solution) - 1:
            overcost -= nu * distance * (datasetOld.getValueAdapt(solution[i], solution[i + 1])/maxFrequencyOld)
            overcost += nu * distance * (dataset.getValueAdapt(solution[j], solution[i + 1])/maxFrequency)
        else:
            overcost -= nu * distance * (datasetOld.getValueAdapt(solution[i], 0)/maxFrequencyOld)
            overcost += nu * distance * (dataset.getValueAdapt(solution[j], 0)/maxFrequency)
        if j > 0:
            overcost -= nu * distance * (datasetOld.getValueAdapt(solution[j - 1], solution[j])/maxFrequencyOld)
            overcost += nu * distance * (dataset.getValueAdapt(solution[j - 1], solution[i])/maxFrequency)
        else:
            overcost -= nu * distance * (datasetOld.getValueAdapt(solution[j], 0)/maxFrequencyOld)
            overcost += nu * distance * (dataset.getValueAdapt(solution[i], 0)/maxFrequency)
        if j + 1 != i:
            if j < len(solution) - 1:
                overcost -= nu * distance * (datasetOld.getValueAdapt(solution[j], solution[j + 1])/maxFrequencyOld)
                overcost += nu * distance * (dataset.getValueAdapt(solution[i], solution[j + 1])/maxFrequency)
            else:
                overcost -= nu * distance * (datasetOld.getValueAdapt(solution[j], 0)/maxFrequencyOld)
                overcost += nu * distance * (dataset.getValueAdapt(solution[i], 0)/maxFrequency)

        return overcost


class TestingHeuristic(unittest.TestCase):

    def test_checkCost(self):

        data = DataSet()
        data.value = [
            [1],
            [2, 6],
            [3, 7, 10],
            [4, 8, 11, 13],
            [5, 9, 12, 14, 15]
        ]

        longTimeMemory = DataSet()
        longTimeMemory.value=[
            [0],
            [0, 0],
            [0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]


        heuristic = TabuSearchHeuristic()

        greedySolution = heuristic.generateGreedySolutionWithMemory(data,longTimeMemory,1,15,1,1)
        result=heuristic.costUsingLongTimeMemory(longTimeMemory,greedySolution,1,14,14,1)

        self.assertEqual(result,0,"Wrong updates on overcost")

    def test_greedywithmemory2(self):

        data = DataSet()
        data.value = [
            [1],
            [2, 6],
            [3, 7, 10],
            [4, 8, 11, 13],
            [5, 9, 12, 14, 15]
        ]

        longTimeMemory = DataSet()
        longTimeMemory.value=[
            [0],
            [0, 0],
            [0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]


        heuristic = TabuSearchHeuristic()

        greedySolution = heuristic.generateGreedySolutionWithMemory(data,longTimeMemory,1,15,1,1)
        result=heuristic.costUsingLongTimeMemory(longTimeMemory,greedySolution,1,14,14,1)

        self.assertEqual(result,0,"Wrong updates on overcost")

    def test_greedywithemptymemory(self):

        data = DataSet()
        data.value = [
            [1],
            [2, 6],
            [3, 7, 10],
            [4, 8, 11, 13],
            [5, 9, 12, 14, 15]
        ]

        longTimeMemory = DataSet()
        longTimeMemory.value=[
            [0],
            [0, 0],
            [0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]


        heuristic = TabuSearchHeuristic()

        solution = heuristic.generateGreedySolution(data)
        greedySolution = heuristic.generateGreedySolutionWithMemory(data,longTimeMemory,1,15,1,1)

        self.assertEqual(solution,greedySolution,"Wrong updates on overcost")

    def test_quickUpdateLongTimeMemory2(self):

        data = DataSet()
        data.value = [
            [1],
            [2, 6],
            [3, 7, 10],
            [4, 8, 11, 13],
            [5, 9, 12, 14, 15]
        ]

        longTimeMemory = DataSet()
        longTimeMemory.value=[
            [1],
            [0, 1],
            [0, 0, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 0, 1]
        ]

        heuristic = TabuSearchHeuristic()

        solution = heuristic.generateGreedySolution(data)
        greedySolution = heuristic.generateGreedySolutionWithMemory(data,longTimeMemory,1,15,1,1)

        self.assertNotEqual(solution,greedySolution,"Wrong updates on overcost")

    def test_quickUpdateLongTimeMemory(self):

        data = DataSet()
        data.value = [
            [1],
            [2, 6],
            [3, 7, 10],
            [4, 8, 11, 13],
            [5, 9, 12, 14, 15]
        ]

        longTimeMemory = DataSet()
        longTimeMemory.value=[
            [1],
            [0, 1],
            [0, 0, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 0, 1]
        ]

        i = 1
        j = 3

        heuristic = TabuSearchHeuristic()

        solution = heuristic.generateGreedySolution(data)
        baseOvercost = heuristic.costUsingLongTimeMemory(longTimeMemory, solution, 1, 14, 1, 1)

        permutedSolution = heuristic.permute(list(solution),i,j)

        fullOvercost = heuristic.costUsingLongTimeMemory(longTimeMemory,permutedSolution,1,14,1,1)
        partialOvercost = heuristic.calculateOvercostDifference(longTimeMemory,longTimeMemory,i,j,solution,1,14,1,1,1,baseOvercost)

        self.assertEqual(fullOvercost,partialOvercost,"Wrong updates on overcost")

    def test_updateLongTimeMemory(self):
        solution = [1, 2, 3, 4, 5]

        longTimeMemory = DataSet()
        longTimeMemory.value=[
            [0],
            [0,0],
            [0,0,0],
            [0,0,0,0],
            [0,0,0,0,0]
        ]

        right=[
            [1],
            [0,1],
            [0,0,1],
            [0,0,0,1],
            [1,0,0,0,1]
        ]

        heuristic = TabuSearchHeuristic()
        heuristic.updateLongTimeMemory(longTimeMemory,solution)

        # for i in range(0,len(longTimeMemory.value)):
        #     print(longTimeMemory.value[i])

        self.assertEqual(right,longTimeMemory.value,"Wrong updates on long time memory")

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