from abc import ABC, abstractmethod
import random as random


class AbstractHeuristic(ABC):
    @abstractmethod
    def calculate(self, solution):
        pass

    def calculateCost(self, dataset, solution):

        cost = 0
        i = 0

        cost += dataset.getValueXY(0, solution[0])

        for i in range(0, len(solution)-1):
            cost += dataset.getValueXY(solution[i], solution[i + 1])
            i += 1

        cost += dataset.getValueXY(i,solution[0])

        return cost

    def generateRandomSolution(self, dataset):

        length = len(dataset[-1])-1
        solution = []

        for i in range(length):
            value = random.randint(1, length)

            while value in solution:
                value = (value + 1) % (length + 1)

                if value == 0:
                    value = 1

            solution.append(value)

        return solution
