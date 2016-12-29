from Heuristics.AbstactHeuristic import AbstractHeuristic
from DataSet import DataSet
from copy import deepcopy
import sys
import unittest


class EvolutiveHeuristic(AbstractHeuristic):

    """
        Calculates a solution using the current heuristic
    """

    def __init__(self,randomGenerator=None):
        super().__init__(randomGenerator)
        self._crossProbability = 0.9

    def calculate(self, dataset=None, solution=None, exploredataset=None):

        # TODO: generate initial population
        #   - Half of it should be random
        #   - The other half must be generated using greedy with a random value for first element of the solution

        print("POBLACION INICIAL")

        individuo = 0
        solutions = []
        solutionsCost = []
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

        for iter in range(1,10):
            text += "\nITERACION: "+str(iter)+", SELECCION\n"

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

            text += "\nITERACION: " + str(iter) + ", CRUCE\n"

            for cruce in range(0, len(solutions) - 2):

                rand = self.randomGenerator.getRawRandom()

                if rand < self._crossProbability:
                    text += "\tCRUCE: (" + str(cruce) + ", " + str((cruce+1) % len(newSolutions)) + ") (ALEATORIO: "+str("%.6f" % round(rand,6))+")\n"
                    text += "\t\tPADRE: = {FUNCION OBJETIVO (km): "+str(newSolutionsCost[cruce])+", RECORRIDO: "
                    for element in newSolutions[cruce]:
                        text += str(element) + " "
                    text += "}\n"

                    text += "\t\tPADRE: = {FUNCION OBJETIVO (km): " + str(newSolutionsCost[(cruce+1) % len(newSolutions)]) + ", RECORRIDO: "
                    for element in newSolutions[(cruce+1) % len(newSolutions)]:
                        text += str(element) + " "
                    text += "}\n"

                    firstCutIndex = self.randomGenerator.getRandomInt(0,len(newSolutions[0]))
                    secondCutIndex = self.randomGenerator.getRandomInt(0,len(newSolutions[0]))

                    text += "\t\tCORTES: (" + str(firstCutIndex) +", "+ str(secondCutIndex) +")\n"

                    h1 = list(newSolutions[0])
                    h2 = list(newSolutions[0])
                    self.orderCroosOver(newSolutions[cruce], newSolutions[(cruce+1) % len(newSolutions)], h1, h2, firstCutIndex, secondCutIndex)

                    h1cost = self.calculateCost(dataset,h1)
                    text += "\t\tHIJO: = {FUNCION OBJETIVO (km): " + str(h1cost) + ", RECORRIDO: "
                    for element in h1:
                        text += str(element) + " "
                    text += "}\n"

                    h2cost = self.calculateCost(dataset, h2)
                    text += "\t\tHIJO: = {FUNCION OBJETIVO (km): " + str(h2cost) + ", RECORRIDO: "
                    for element in h2:
                        text += str(element) + " "
                    text += "}\n"

            text += "\n"

        print(text)

        # TODO: generación de una nueba población cruzando los padres
        # probabilidad de cruce = 0.9

        # TODO: aplicar mutaciones en base a la probabilidad de las mismas
        # intercambio recíproco (transparencia 5.5.33), no que dúas cidades distintas
        # elixidas aleatoriamente intercambian as súas posicións

        # TODO: obtencion de la nueva población candidata

        # TODO: reemplazo de la anterior población
        # selección por torneo de tamaño 2, no que se selecciona o
        # individuo de mellor fitness entre k=2 individuos escollidos aleatoriamente de entre a poboación.

        return solution

    def orderCroosOver(self,p1, p2, h1, h2, i1, i2):
        filled = 0

        if (i1 > i2):
            aux = i1
            i1 = i2
            i2 = i1

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
    unittest.main()