from Heuristics.AbstactHeuristic import AbstractHeuristic
from DataSet import DataSet
from copy import deepcopy
import sys
import itertools

import unittest


class EvolutiveHeuristic(AbstractHeuristic):

    """
        Calculates a solution using the current heuristic
    """

    def __init__(self,randomGenerator=None):
        super().__init__(randomGenerator)
        self._crossProbability = 0.9
        self._mutationProbability = 0.01

    def calculate(self, dataset=None, solution=None, exploredataset=None):

        # TODO: generate initial population
        #   - Half of it should be random
        #   - The other half must be generated using greedy with a random value for first element of the solution

        print("POBLACION INICIAL")

        individuo = 0
        solutions = []
        solutionsCost = []
        bestSolution = -1
        bestCost = -1
        bestIteration = 0

        text = ""
        for i in range(0,50):
            solutions.append(self.generateRandomSolution(dataset))
            solutionsCost.append(self.calculateCost(dataset,solutions[-1]))
            text += "INDIVIDUO " + str(individuo) + " = {FUNCION OBJETIVO (km): "+str(solutionsCost[-1])+", RECORRIDO: "
            for j in solutions[-1]:
                text += str(j) + " "

            text += "}\n"
            individuo += 1

        for i in range(0,50):
            solutions.append(self.generateGreedySolutionWithRandomFirstElement(dataset))
            solutionsCost.append(self.calculateCost(dataset, solutions[-1]))
            text += "INDIVIDUO " + str(individuo) + " = {FUNCION OBJETIVO (km): " + str(solutionsCost[-1]) + ", RECORRIDO: "
            for j in solutions[-1]:
                text += str(j) + " "

            text = text+"}\n"
            individuo += 1

        print(text)

        for iter in range(1,1000):
            text = "\nITERACION: "+str(iter)+", SELECCION\n"

            newSolutions = []
            newSolutionsCost = []

            for torneo in range(0, len(solutions)-2):
                text +="\tTORNEO " + str(torneo) +":"

                x = self.randomGenerator.getRandomInt(0, len(solutions))
                y = self.randomGenerator.getRandomInt(0, len(solutions))

                text += " "+str(x)+" "+str(y)+" "

                if solutionsCost[x] > solutionsCost[y]:
                    text += "GANA "+str(y)
                    newSolutions.append(solutions[y])
                    newSolutionsCost.append(solutionsCost[y])
                else:
                    text += "GANA " + str(x)
                    newSolutions.append(solutions[x])
                    newSolutionsCost.append(solutionsCost[x])

                text += "\n"

            text += "\nITERACION: " + str(iter) + ", CRUCE \n"

            cruce = 0

            solutionsAfterCross = []
            solutionsCostAfterCross =[]

            while cruce < len(solutions) - 2 :

                rand = self.randomGenerator.getRawRandom()

                text += "\tCRUCE: (" + str(cruce) + ", " + str(
                    (cruce + 1) % len(newSolutions)) + ") (ALEATORIO: " + str("%.6f" % round(rand, 6)) + ")\n"
                text += "\t\tPADRE: = {FUNCION OBJETIVO (km): " + str(newSolutionsCost[cruce]) + ", RECORRIDO: "
                for element in newSolutions[cruce]:
                    text += str(element) + " "
                text += "}\n"

                text += "\t\tPADRE: = {FUNCION OBJETIVO (km): " + str(
                    newSolutionsCost[(cruce + 1) % len(newSolutions)]) + ", RECORRIDO: "
                for element in newSolutions[(cruce + 1) % len(newSolutions)]:
                    text += str(element) + " "
                text += "}\n"

                if rand < self._crossProbability:

                    firstCutIndex = self.randomGenerator.getRandomInt(0,len(newSolutions[0]))
                    secondCutIndex = self.randomGenerator.getRandomInt(0,len(newSolutions[0]))

                    text += "\t\tCORTES: (" + str(firstCutIndex) +", "+ str(secondCutIndex) +")\n"

                    p1 = newSolutions[cruce]
                    p2 = newSolutions[(cruce+1) % len(newSolutions)]
                    h1 = list(newSolutions[0])
                    h2 = list(newSolutions[0])
                    self.orderCroosOver(p1, p2, h1, h2, firstCutIndex, secondCutIndex)

                    h1cost = self.calculateCost(dataset,h1)
                    text += "\t\tHIJO: = {FUNCION OBJETIVO (km): " + str(h1cost) + ", RECORRIDO: "
                    for element in h1:
                        text += str(element) + " "
                    text += "}\n"

                    h2cost = self.calculateCost(dataset, h2)
                    text += "\t\tHIJO: = {FUNCION OBJETIVO (km): " + str(h2cost) + ", RECORRIDO: "
                    for element in h2:
                        text += str(element) + " "
                    text += "}\n\n"

                    solutionsAfterCross.append(h1)
                    solutionsAfterCross.append(h2)
                    solutionsCostAfterCross.append(h1cost)
                    solutionsCostAfterCross.append(h2cost)

                else:
                    text += "\t\tNO SE CRUZA\n\n"

                    p1 = newSolutions[cruce]
                    p2 = newSolutions[(cruce + 1) % len(newSolutions)]
                    p1cost = newSolutionsCost[cruce]
                    p2cost = newSolutionsCost[(cruce + 1) % len(newSolutions)]

                    solutionsAfterCross.append(p1)
                    solutionsAfterCross.append(p2)
                    solutionsCostAfterCross.append(p1cost)
                    solutionsCostAfterCross.append(p2cost)

                cruce += 2

            text += "ITERACION: " + str(iter) + ", MUTACION\n"

            for n in range(0,len(solutionsAfterCross)):
                text += "\tINDIVIDUO "+str(n)+"\n"
                text += "\tRECORRIDO ANTES: "

                for j in solutionsAfterCross[n]:
                    text += str(j)+" "

                text += "\n"

                for j in range(len(dataset.value[-1])):

                    rand = self.randomGenerator.getRawRandom()

                    text += "\t\tPOSICION: " + str(j) + " (ALEATORIO " + str("%.6f" % round(rand, 6)) + ")"

                    if rand < self._mutationProbability:
                        k = self.randomGenerator.getRandomInt(0,len(solutionsAfterCross[0]))

                        aux = solutionsAfterCross[n][j]
                        solutionsAfterCross[n][j] = solutionsAfterCross[n][k]
                        solutionsAfterCross[n][k] = aux

                        solutionsCostAfterCross[n] = self.calculateCost(dataset,solutionsAfterCross[n])

                        text += " INTERCAMBIO CON: " + str(k)

                    else:
                        text += " NO MUTA"
                    text += "\n"

                text += "\tRECORRIDO DESPUES: "
                for j in solutionsAfterCross[n]:
                    text += str(j)+" "

                text += "\n\n"

            text += "\nITERACION: " + str(iter) + ", REEMPLAZO\n"


            solutions = sorted(solutions, key=lambda sol: self.calculateCost(dataset,sol))
            solutionsCost = sorted(solutionsCost, key=lambda cost: int(cost))

            solutions = solutions[0:2]
            solutionsCost = solutionsCost[0:2]

            solutionsAfterCross = sorted(solutionsAfterCross, key=lambda sol: self.calculateCost(dataset, sol))
            solutionsCostAfterCross = sorted(solutionsCostAfterCross)

            for k in range(0,len(solutionsAfterCross)):
                solutions.append(solutionsAfterCross[k])
                solutionsCost.append(solutionsCostAfterCross[k])

            for k in range(0,len(solutions)):
                text += "INDIVIDUO " + str(k) + " = {FUNCION OBJETIVO (km): " + str(solutionsCost[k]) + ", RECORRIDO: "
                for j in solutions[k]:
                    text += str(j)+" "
                text += "}\n"

            if bestCost < 0 or bestCost >= solutionsCost[0]:
                bestSolution = solutions[0]
                bestCost = solutionsCost[0]
                bestIteration = iter

            print(text)

        text = "\nMEJOR SOLUCION:"
        text += "\nRECORRIDO: "
        for j in bestSolution:
            text += str(j) + " "

        text += "\nFUNCION OBJETIVO (km): "+str(bestCost)
        text += "\nITERACION: " + str(bestIteration)

        print(text)

        return solution

    def orderCroosOver(self,p1, p2, h1, h2, i1, i2):
        filled = 0

        if (i1 > i2):
            aux = i1
            i1 = i2
            i2 = aux

        for i in range(len(p1)):
            h1[i] = 0
            h2[i] = 0

        i = i1
        while i <= i2:

            h1[i] = p1[i]
            h2[i] = p2[i]

            i+=1
            filled += 1

        actual = index = (i2+1) % len(p1)

        while filled < len(p1):

            if p2[index] not in h1:
                h1[actual] = p2[index]
                filled += 1

                actual += 1
                actual = actual % len(p1)

            index += 1
            index = index % len(p1)

        filled = i2 - i1+1
        actual = index = (i2 + 1) % len(p1)

        while filled < len(p1):

            if p1[index] not in h2:
                h2[actual] = p1[index]
                filled += 1

                actual += 1
                actual = actual % len(p1)

            index += 1
            index = index % len(p1)

    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

class TestingHeuristic(unittest.TestCase):


    def test_orderCrossOver(self):

        heuristic = EvolutiveHeuristic()

        p1 = [1, 2, 3, 4, 5, 6]
        p2 = [6, 5, 4, 3, 2, 1]
        h1 = list(p1)
        h2 = list(p2)
        i1 = 1
        i2 = 3

        heuristic.orderCroosOver(p1, p2, h1, h2, i1, i2)

        self.assertEqual(h1, [5,2,3,4,1,6], "El hijo uno se ha generado mal")
        self.assertEqual(h2, [2,5,4,3,6,1], "El hijo dos se ha generado mal")

if __name__ == '__main__':
    unittest.main() 