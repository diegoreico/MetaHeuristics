import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

path="./resultado"

data = []
acumular = False
contador=0
file = open(path)
for line in file:

    if line.startswith("\t"):
        contador+=1
    elif line.startswith("S"):
        print("\nuna solucion")
        data.append(contador)
        contador=0

data.append(contador)

file.close()
data=data[1:]
print(data)

sns.set_style("darkgrid")
plt.plot(data)
plt.show()


sns.plt.show()