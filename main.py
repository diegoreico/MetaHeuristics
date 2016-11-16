from Loader import Loader

class Main:

    def __init__(self):
        """ load from file """
        loader = Loader()
        data = loader.load()
        """ # select an heuristic """

        print(data)

if __name__ == '__main__':
    Main()