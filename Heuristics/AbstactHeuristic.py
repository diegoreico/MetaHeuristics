from abc import ABC, abstractmethod
from Utils.RandomGenerator import RandomGenerator

class AbstractHeuristic(ABC):

    """
        Abstract class that defines some methods that should have
        all the heuristics made
    """

    @abstractmethod
    def __init__(self,randomGenerator=None):
        if randomGenerator is None:
            randomGenerator = RandomGenerator()

        self.randomGenerator = randomGenerator

    @abstractmethod
    def calculate(self, dataset=None, solution=None, exploredataset=None):

        """

        :param dataset: full search space represented as an object of the class DataSet
        :param solution: one dimensional array with the base solution to use
        :param exploredataset: explored soluutions using the current solution as base
        :return: a solution one dimensional array
        """

    def calculateCost(self, dataset, solution):

        """

        :param dataset: full search space represented as an object of the class DataSet
        :param solution: one dimensional array with the base solution to use
        :return: an int with the value of the cost
        """

        cost = 0
        i = 0

        cost += dataset.getValueXY(0, solution[0]-1)

        #print("\t\t\ŧVALOR: ",dataset.getValueXY(0, solution[0]-1))

        for i in range(0, len(solution)-1):
            if solution[i] < solution[i+1]:
                x = solution[i]
                y = solution[i + 1]
            else:
                x = solution[i + 1]
                y = solution[i]

            cost += dataset.getValueXY(x, y-1)
            #print("\t\t\ŧVALOR (",x,",",y-1,"):  =", dataset.getValueXY(x,y-1))

        cost += dataset.getValueXY(0,solution[-1]-1)
        #print("\t\t\ŧVALOR: (",0,",",solution[-1]-1,")", dataset.getValueXY(0,solution[-1]-1))

        return cost

    def calculateCostDifference(self, dataset, i, j, solution, newCost):
        if j + 1 != i:
            if i > 0:
                newCost -= dataset.getValueAdapt(solution[i - 1], solution[i])
                newCost += dataset.getValueAdapt(solution[i - 1], solution[j])
            else:
                newCost -= dataset.getValueAdapt(solution[i], 0)
                newCost += dataset.getValueAdapt(solution[j], 0)
        if i < len(solution) - 1:
            newCost -= dataset.getValueAdapt(solution[i], solution[i + 1])
            newCost += dataset.getValueAdapt(solution[j], solution[i + 1])
        else:
            newCost -= dataset.getValueAdapt(solution[i], 0)
            newCost += dataset.getValueAdapt(solution[j], 0)
        if j > 0:
            newCost -= dataset.getValueAdapt(solution[j - 1], solution[j])
            newCost += dataset.getValueAdapt(solution[j - 1], solution[i])
        else:
            newCost -= dataset.getValueAdapt(solution[j], 0)
            newCost += dataset.getValueAdapt(solution[i], 0)
        if j + 1 != i:
            if j < len(solution) - 1:
                newCost -= dataset.getValueAdapt(solution[j], solution[j + 1])
                newCost += dataset.getValueAdapt(solution[i], solution[j + 1])
            else:
                newCost -= dataset.getValueAdapt(solution[j], 0)
                newCost += dataset.getValueAdapt(solution[i], 0)
        return newCost

    """
        Generates a random solution.It's usually used at start to generate a base solution
    """
    def generateRandomSolution(self, dataset):

        """

        :param dataset: full search space represented as an object of the class DataSet
        :return:
        """

        length = len(dataset.value[-1])
        solution = []


        """
            For each position of the solution array we generate a random number
            and if it is already in the array, we sum 1 (module length of the array) to the element until we
            found a number that isn't in the array
        """
        for i in range(length):
            value = self.randomGenerator.getRandomInt(1, length)

            while value in solution:
                value = (value + 1) % (length + 1)

                if value == 0:
                    value = 1

            solution.append(value)

        return solution

    def generateGreedySolution(self,dataset):

        """

        :param dataset:
        :return:
        """

        length = len(dataset.value[-1])
        solution = [0]
        used = 0
        first = True

        while used < length:

            for i in range(0,len(dataset.value)+1):

                if i not in solution and i != used:

                    if first:
                        first = False
                        min = i

                    elif dataset.getValueAdapt(solution[used],i) < dataset.getValueAdapt(solution[used],min):
                        min = i

            first = True
            solution.append(min)

            used+=1

        solution.pop(0)

        return solution

    def generateGreedySolutionWithMemory(self,dataset,longTimeMemory,nu,dmax,dmin,maxFrequency):

        """

        :param dataset:
        :return:
        """

        length = len(dataset.value[-1])
        solution = [0]
        used = 0
        first = True

        distance = dmax-dmin

        while used < length:

            for i in range(0,len(dataset.value)+1):

                if i not in solution and i != used:

                    if first:
                        first = False
                        min = i

                    currentCost = dataset.getValueAdapt(solution[used],i) + nu * distance * (longTimeMemory.getValueAdapt(solution[used], i) / maxFrequency)
                    minCost = dataset.getValueAdapt(solution[used],min) + nu * distance * (longTimeMemory.getValueAdapt(solution[used], min) / maxFrequency)

                    if currentCost < minCost :
                        min = i

            first = True
            solution.append(min)

            used+=1

        solution.pop(0)

        return solution






