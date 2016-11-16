class Loader:

    def __init__(self, path="./distancias_10.txt"):
        self.path=path

    def load(self):

        dataSet = []
        file = open(self.path)
        for line in file:
            dataSet.append(line.strip().split('\t'))

        return dataSet

if __name__ == '__main__':
    loader = Loader()
    loader.load()
