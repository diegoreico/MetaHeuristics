from abc import ABC, abstractmethod
import random as random


class AbstractHeuristic(ABC):

    @abstractmethod
    def calculate(self, dataset=None, exploredataset=None, solution=None):
        pass

    def calculateCost(self, dataset, solution):

        cost = 0
        i = 0

        cost += dataset.getValueXY(0, solution[0]-1)

        for i in range(0, len(solution)-2):
            cost += dataset.getValueXY(solution[i]-1, solution[i + 1]-1)
            i += 1 #TODO: esto debería sobrar

        cost += dataset.getValueXY(i,solution[0]-1)

        return cost

    def generateRandomSolution(self, dataset):

        length = len(dataset.value[-1])
        solution = []

        for i in range(length):
            value = random.randint(1, length)

            while value in solution:
                value = (value + 1) % (length + 1)

                if value == 0:
                    value = 1

            solution.append(value)

        return solution
