from Heuristics.AbstactHeuristic import AbstractHeuristic
from DataSet import DataSet

class BestFirstHeuristic(AbstractHeuristic):

    def calculate(self, solution):
        super().calculate(solution)

    def permute(self, dataset=None, exploredataset=None, solution=None):
        if solution is None:
            return []

        if dataset is None:
            return solution

        if exploredataset is None:
            return solution


    def generateDefaultExploredDataset(self,dataset):
        exploredValues = []

        for i in range(0,len(dataset.value)):
            exploredValues.append([])
            for j in range(0,len(dataset.value[i])):
                exploredValues[i].append(0)

            print(exploredValues[i])

        exploredSolutionsDataSet = DataSet(exploredValues)

        return exploredSolutionsDataSet