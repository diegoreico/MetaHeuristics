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
        T0 = (self.mu/-numpy.log(self.phi)) * cost
        T=T0

        txt = "SOLUCIÓN INICIAL:"
        txt += "\n\tRECORRIDO: "
        for element in solution:
            txt += str(element) + " "

        txt += "\n\tFUNCION OBJETIVO: " + str(cost)
        txt += "\n\tTEMPERATURA INICIAL: " + str(round(T,6))
        txt += "\n"

        sys.stdout.write(txt)

        numberOfAcceptedCandidateSolutions = 0
        numberOfGeneratedCandidateSolutions = 0
        numberOfCoolings = 0

        for k in range(10000):

            x = 0
            y = 0
            candidatesolutionCost = cost*2
            candidateSolution=list(solution)

            for i in range(0,len(solution)):
                for j in range(0, i):
                    if i != j :
                        newCost = self.calculateCostDifference(dataset, i, j, solution, cost)

                        if newCost< candidatesolutionCost:
                                candidateSolutionCost = newCost
                                candidateSolution = self.permute(list(solution), i, j);
                                x=i
                                y=j

            numberOfGeneratedCandidateSolutions+=1

            delta = candidatesolutionCost - cost
            exponential = pow(numpy.e,(-delta/T))
            accepted = False
            if delta < 0 or self.randomGenerator.getRandomInt(0,1) < exponential:
                numberOfAcceptedCandidateSolutions+=1
                solution = candidateSolution
                cost = candidatesolutionCost
                accepted = True


            # cooling, Cauchy -> T = T0 /(1+k)
            if numberOfGeneratedCandidateSolutions == 80:
                numberOfGeneratedCandidateSolutions = 0
                T = T0 / (1 + k)
                numberOfCoolings += 1

            if numberOfAcceptedCandidateSolutions == 20:
                numberOfAcceptedCandidateSolutions = 0
                T = T0 / (1 + k)
                numberOfCoolings += 1

            if numberOfGeneratedCandidateSolutions == 0 or numberOfAcceptedCandidateSolutions == 0:
                txt = "============================"
                txt += "\nENFRIAMIENTO: " + str(numberOfCoolings)
                txt += "\n============================"
                txt += "\n\tTEMPERATURA: " + str(round(T, 6))
                sys.stdout.write(txt)

            txt = "ITERACION: " + str(k)
            txt += "\n\tINTERMCABION: ("+str(x)+", "+str(y)+"9"
            txt += "\n\tRECORRIDO: "
            for element in solution:
                txt += str(element) + " "

            txt += "\n\tFUNCION OBJETIVO: " + str(cost)
            txt += "\n\tTEMPERATURA: " + str(round(T, 6))
            txt += "\n\tVALOR DE LA EXPONENCIAL: " + str(exponential)
            if accepted:
                txt += "\n\tSOLUCION CANDIDATA ACEPTADA"
            txt += "\n\tCANDIDATAS PROBADAS: " + str(numberOfGeneratedCandidateSolutions) +", ACEPTADAS: "+ str(numberOfAcceptedCandidateSolutions)
            txt += "\n"

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