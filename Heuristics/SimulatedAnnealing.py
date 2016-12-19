from Heuristics.AbstactHeuristic import AbstractHeuristic

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
        self.mu = 0.01
        self.phi = 0.5


    def calculate(self, dataset=None, solution=None, exploredataset=None):

        # initialization using a greedy algorithm
        if solution is None:
            solution = self.generateGreedySolution(dataset)

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

        for k in range(0,10000):

            candidateSolutionCost = cost*2
            candidateSolution = None

            for i in range(0,len(solution)):
                for j in range(0, i):
                    if i != j :
                        newCost = self.calculateCostDifference(dataset, i, j, solution, cost)

                        if newCost <= candidateSolutionCost:
                                candidateSolutionCost = newCost
                                candidateSolution = self.permute(list(solution), i, j)
                                x=i
                                y=j

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
            if numberOfGeneratedCandidateSolutions == 80 or numberOfAcceptedCandidateSolutions == 20:
                solution = self.generateGreedySolution(dataset)
                cost = self.calculateCost(dataset, solution)

                numberOfGeneratedCandidateSolutions = 0
                numberOfAcceptedCandidateSolutions = 0
                numberOfCoolings += 1
                T = T0 / (1 + numberOfCoolings)

                txt = "\n============================"
                txt += "\nENFRIAMIENTO: " + str(numberOfCoolings)
                txt += "\n============================"
                txt += "\nTEMPERATURA: " + str("%.6f" % round(T, 6)) + "\n"
                sys.stdout.write(txt)

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


if __name__ == '__main__':
    unittest.main()