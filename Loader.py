from DataSet import DataSet

class Loader:

    def __init__(self, path="./distancias_100_2016.txt"):
        self.path=path

    def load(self):

        dataSet = DataSet()
        file = open(self.path)
        for line in file:
            dataSet.value.append(line.strip().split('\t'))

        for i in range(0,len(dataSet.value)):
            for j in range(0, len(dataSet.value[i])):
                dataSet.value[i][j] = int(dataSet.value[i][j])

        file.close()

        return dataSet

