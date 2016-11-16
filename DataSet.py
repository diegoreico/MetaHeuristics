class DataSet:

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self,value):
        self._value = value

    @value.getter
    def value(self):
        return self._value

    @value.deleter
    def value(self):
        del self._value

    def getValueXY(self,x,y):
        if x > y:
            return self._value[x][y]
        else:
            return self._value[y][x]

    def __init__(self, value=None):
        if value is None:
            value = []

        self._value=value
