from Heuristics.AbstactHeuristic import AbstractHeuristic
from copy import deepcopy
from DataSet import DataSet
import sys
import unittest
import numpy

class SimulatedAnnealing(AbstractHeuristic):

    """
        Calculates a solution using the current heuristic
    """

    def __init__(self,randomGenerator=None):
        super().__init__(randomGenerator)
        self.mu = 0.1
        self.phi = 0.5


    def calculate(self, dataset=None, solution=None, exploredataset=None):

        # initialization using a greedy algorithm
        if solution is None:
            solution = self.generateGreedySolution(dataset)

        """
           LONG TIME MEMORY
        """
        maxDistance = dataset.value[0][0]
        minDistance = dataset.value[0][0]
        nu = 0.001
        maxFrequency = 1
        maxFrequencyOld = 1

        # getting max and min distance
        for row in dataset.value:
            for value in row:
                if value < minDistance:
                    minDistance = value
                elif value > maxDistance:
                    maxDistance = value

        # dataset with the number of times that a path between cities was selected
        longTimeMemoryOld = longTimeMemory = DataSet()

        for i in range(0, len(dataset.value)):
            line = []
            for j in range(0, len(dataset.value[i])):
                line.append(0)

            longTimeMemory.value.append(line)


        # initial value of control variable,T0 = (mu/-ln(phi)) * Cost of initial solution
        cost = self.calculateCost(dataset, solution)

        globalSolution = solution
        globalCost = cost

        T0 = (self.mu/-numpy.log(self.phi)) * cost
        T=T0

        txt = "SOLUCIÓN INICIAL:"
        txt += "\n\tRECORRIDO: "
        for element in solution:
            txt += str(element) + " "

        txt += "\n\tFUNCION OBJETIVO (km): " + str(cost)
        txt += "\n\tTEMPERATURA INICIAL: " + str(round(T,6))
        txt += "\n"

        sys.stdout.write(txt)

        numberOfAcceptedCandidateSolutions = 0
        numberOfGeneratedCandidateSolutions = 0
        numberOfCoolings = 0
        iterationFound = 0
        exponential = 0
        k=0
        while k < 10000:

            candidateSolutionOvercost = candidateSolutionCost = cost*2
            candidateSolution = []

            longs=len(solution)
            i=0

            while i < longs:
                j = 0
                while j < i:
                    if i is not j :
                        newCost = self.calculateCostDifference(dataset, i, j, solution, cost)
                        newOverCost = self.calculateOvercostDifference(longTimeMemory,longTimeMemoryOld,i,j,self.permute(list(solution), i, j),nu,maxDistance,minDistance,maxFrequency,maxFrequencyOld,newCost)

                        if newCost +newOverCost <= candidateSolutionCost + candidateSolutionOvercost :
                                candidateSolutionCost = newCost
                                candidateSolutionOvercost = newOverCost
                                candidateSolution = self.permute(list(solution), i, j)
                                x=i
                                y=j
                    j+=1
                i+=1


            numberOfGeneratedCandidateSolutions += 1

            delta = candidateSolutionCost - cost
            exponential = numpy.exp(-delta/T)
            accepted = False
            random = self.randomGenerator.getRawRandom()

            if delta <= 0 or random <= exponential:

                solution = candidateSolution
                cost = candidateSolutionCost
                accepted = True
                numberOfAcceptedCandidateSolutions += 1

                maxFrequencyOld = maxFrequency

                # get the max frequency inside probability matrix
                for row in longTimeMemory.value:
                    for element in row:
                        if element > maxFrequency:
                            maxFrequency = element

                longTimeMemoryOld = deepcopy(longTimeMemory)
                self.updateLongTimeMemory(longTimeMemory, solution)

                if cost < globalCost:
                    globalCost = cost
                    globalSolution = list(solution)
                    iterationFound = k


            txt = "\nITERACION: " + str(k+1)
            txt += "\n\tINTERCAMBIO: ("+str(x)+", "+str(y)+")"
            txt += "\n\tRECORRIDO: "
            for element in candidateSolution:
                txt += str(element) + " "

            txt += "\n\tFUNCION OBJETIVO (km): " + str(candidateSolutionCost)
            txt += "\n\tDELTA: " + str(delta)
            txt += "\n\tTEMPERATURA: " + str("%.6f" % round(T, 6))
            txt += "\n\tVALOR DE LA EXPONENCIAL: " + str("%.6f" % round(exponential,6))
            if accepted:
                txt += "\n\tSOLUCION CANDIDATA ACEPTADA"
            txt += "\n\tCANDIDATAS PROBADAS: " + str(numberOfGeneratedCandidateSolutions) +", ACEPTADAS: "+ str(numberOfAcceptedCandidateSolutions)
            txt += "\n"

            sys.stdout.write(txt)

            # cooling, Cauchy -> T = T0 /(1+k)
            if numberOfGeneratedCandidateSolutions == 40 or numberOfAcceptedCandidateSolutions == 20:

                numberOfGeneratedCandidateSolutions = 0
                numberOfAcceptedCandidateSolutions = 0
                numberOfCoolings += 1
                # T = T0 / (1 + numpy.log(numberOfCoolings))
                T = T0 / (1 + numpy.log(numberOfCoolings))


                nu -= 0.001
                if nu < -0.30:
                    nu = 0

                if k == 5000:
                    T = T0
                    numberOfCoolings = 0
                # if T < 12:
                #     #if exponential < 0.001:
                #     T = T0
                #     numberOfCoolings = 0


                # if divmod(numberOfCoolings,2) == 0:
                solution = self.generateGreedySolutionWithMemory(dataset, longTimeMemory, nu, maxDistance, minDistance,
                                                                 maxFrequency)
                cost = self.calculateCost(dataset,solution)


                txt = "\n============================"
                txt += "\nENFRIAMIENTO: " + str(numberOfCoolings)
                txt += "\n============================"
                txt += "\nNU: " + str("%.6f" % round(nu, 6)) + "\n"
                txt += "\nTEMPERATURA: " + str("%.6f" % round(T, 6)) + "\n"
                sys.stdout.write(txt)

            k+=1

        txt = "\n\nMEJOR SOLUCION: "
        txt += "\n\tRECORRIDO: "
        for element in globalSolution:
            txt += str(element) + " "

        txt += "\n\tFUNCION OBJETIVO (km): " + str(globalCost)
        txt += "\n\tITERACION: " + str(iterationFound+1)
        txt += "\n\tmu = " + str(round(self.mu,2)) + ", phi = " + str(round(self.phi,1)) +"\n"

        sys.stdout.write(txt)

        return solution

    def permute(self, solution, X, Y):
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


if __name__ == '__main__':
    unittest.main()