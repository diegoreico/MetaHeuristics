# notas

## Computación evolutiva

### pasos

tamaño población --> 100

- inicialización: primeira mitad -> aleatorio, segunda mitad -> greedy
- evaluación
- parte iterativa:

    - selección(seleccionanse solo 98): a problación de selección se genera mediante un, operador de toreno binario, generanse 2 número aleatorios entre 0 e 99, se comparan dúas solución, slo queda o mellor
    - cruce: operador order crossover. A maiores se genera un numero aleatorio o cal se supera c erto umbral se produce o cruce e se xeran dous fillos, se non se supera simplemente se copian os pais como fillos
    - mutación: se volve a generar un numero aleatorio, si pasa de  un umbral o cruzamos con unha solución aleatoria
    - evaluación
    - reemplazo: en este punto temos un conjunto de 98 solucions aos que lle sumaremos os 2 mellores individuos do conjunto inicial para generar un novo conjunto

criterio de parada: 1000 interacións - tendo en conta a inicial

### para  millorar

- modificar parametros
- operadores de cruce
- operadores de mutación
- cambiar mecanismo de reemplazo -> steady state, se genera cos mellores elementos da generación de pais e fillos <- recomendado facer
    - para manter a diversidad se aplica reinicialización, na que se manten parte dos mellores individuos da población e o resto se generan de forma casi aleatoria
    - criterios para saber si non evoluciona:
        - non se mellora a mellor solución
        - non se seleccionou ningún fillo
    - o criterio anterior se leva a conta das veces que se produce para elegir cando se reinicia
- realización de búsquedas locales cos mellores individuos (), generando o vecindario de un individuo e substituindo a dito individuo polo mellor do seu vecindario. O individuo o podemos generar como en prácticas anteriores

- algoritmos meméticos

- neste caso se usa 100 ciudades pero para a parte obligatoria usase o dataset de 10 ciudades