from abc import ABC, abstractmethod
import random as random


class AbstractHeuristic(ABC):
    @abstractmethod
    def calculate(self, solution):
        pass

    def generateRandomSolution(self, dataset):

        length = len(dataset[-1])
        solution = []
        for i in range(length):
            value = random.randint(1, length)

            while value in solution:
                value = (value + 1) % length + 1

            solution.append(value)

        return solution
