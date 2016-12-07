class DataSet:
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @value.getter
    def value(self):
        return self._value

    @value.deleter
    def value(self):
        del self._value

    """
        This Dataset is for a Lower triangular matrix
    """

    # TODO: this should be a property¿?
    def getValueXY(self, x, y):
        if x >= y:
            return int(self._value[x][y])
        else:
            return int(self._value[y][x])

    def getValueAdapt(self, x, y):
        # print("\n\ti:" ,x,"\t,j:" ,y)
        if x == y:
            return int(self._value[x-1][y-2])
        elif x > y:
            return int(self._value[x-1][y])
        else:
            return int(self._value[y-1][x])


    def setValueXY(self, x, y, value):
        if x >= y:
            self._value[x-1][y] = value
        else:
            self._value[y][x] = value

    def __init__(self, value=None):
        if value is None:
            value = []

        self._value = value
