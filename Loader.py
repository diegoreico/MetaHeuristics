from DataSet import DataSet

class Loader:

    def __init__(self, path="./distancias_10.txt"):
        self.path=path

    def load(self):

        dataSet = DataSet()
        file = open(self.path)
        for line in file:
            dataSet.value.append(line.strip().split('\t'))

        file.close()

        return dataSet

