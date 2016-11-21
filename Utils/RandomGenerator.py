import collections as collections
import random as random

class RandomGenerator:

    def __init__(self,path = None):

        self._debuggingCount = 0

        if path is not None:
            self.hasPath = True

            dataFromFile = []

            file = open(path)

            for line in file:
                dataFromFile.append(float(line))

            self.queueOfRandomNumbers = collections.deque(dataFromFile)

        else:
            self.hasPath = False

    def getRandomInt(self,i,j):

        if self.hasPath:
            randomNumber = self.queueOfRandomNumbers.popleft()


            return i + int(randomNumber*j)
        else:
            return random.randint(i, j-1)




