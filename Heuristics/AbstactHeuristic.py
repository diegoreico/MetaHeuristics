from abc import ABC, abstractmethod
import random as random


class AbstractHeuristic(ABC):

    """
        Abstract class that defines some methods that should have
        all the heuristics made
    """

    @abstractmethod
    def calculate(self, dataset=None, solution=None, exploredataset=None):

        """

        :param dataset: full search space represented as an object of the class DataSet
        :param solution: one dimensional array with the base solution to use
        :param exploredataset: explored soluutions using the current solution as base
        :return: a solution one dimensional array
        """

        pass

    def calculateCost(self, dataset, solution):

        """

        :param dataset: full search space represented as an object of the class DataSet
        :param solution: one dimensional array with the base solution to use
        :return: an int with the value of the cost
        """

        cost = 0
        i = 0

        cost += dataset.getValueXY(0, solution[0]-1)

        for i in range(0, len(solution)-2):
            cost += dataset.getValueXY(solution[i]-1, solution[i + 1]-1)
            i += 1 #TODO: esto debería sobrar

        cost += dataset.getValueXY(i,solution[0]-1)

        return cost


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
            value = random.randint(1, length)

            while value in solution:
                value = (value + 1) % (length + 1)

                if value == 0:
                    value = 1

            solution.append(value)

        return solution
