#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

path="./aqui"

data = []
acumular = False

file = open(path)
for line in file:

    if line.startswith("\tCOSTE"):
        data.append(int(line.replace("\tCOSTE (km):","",1)))

file.close()
data=data[1:]
print(data)

sns.set_style("darkgrid")
plt.plot(data)
plt.show()


sns.plt.show()