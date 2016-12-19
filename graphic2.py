#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

path="./salida"

data = []
acumular = False

file = open(path)
for line in file:

    if line.startswith("\tFUNCION OBJETIVO (km):"):
        data.append(int(line.replace("\tFUNCION OBJETIVO (km):","",1)))

file.close()
data=data[1:]
print(data)

sns.set_style("darkgrid")
plt.plot(data)
plt.show()


sns.plt.show()
