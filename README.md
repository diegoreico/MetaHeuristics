![Meta Heuristics](https://docs.google.com/drawings/d/1GvSXJfp7RvjN4T2VtgJfQZ9LzGrHRIelw-awrcxYYVo/pub?w=249&h=101)

# MetaHeuristics

A repositorie with an explanation and a comparission of different metaheuristics

## Base Problem - Travelling salesman problem
We must travel from the origin city, go through all the cities and come back to the origin city. For this we should use the shortest path that we can found and we can't pass two times for the same city.

Example representation of the problem

![Search Space](https://docs.google.com/drawings/d/1CqxjTGnPX06tfltqM3eUIMCvVwr4fED_Np9bWlAhzjY/pub?w=469&h=302)

### Representation of Solutions

In the representation of the solution, we assume that we start in city 0 and that we have to return to city 0. So we represent the solution as an ordered array of cities, in which the first element is the city that we are going to visit if we start at city 0, the second element is the city that we should visit if we are at city 1,..

| Order  | 1   | 2   | 3   | 4   | 5   | 6   | 7   | n   |
| -----  | --- | --- | --- | --- | --- | --- | --- | --- |
| City   | 2   | 5   | 7   | 6   | 3   | 1   | 4   | n   |

### Cost of Solution

The cost of the solution is the sum of the distances of traveling from one city to another following the solution path. We must remember that we start at city 0 and we have to return to city 0.

    C = D(0,1) + D(1,2)+ ··· + D(j,k) + ··· + D(k,n-1) + D(n-1,n) + D(n,0)


## Implemented MetaHeuristics

### Local Search

#### First Best
<<<<<<< HEAD
 
In this kind of search, we update the current solution with the first solution found that is better than our current solution, we don't need to search in all the possible search space. 

##### Operators used

- **Permute:** exchanges the position of two cities in the solution array 

    Example:
    
    | Order  | 1   | 2   | 3   | 4   | 5   | 6   | 7   | n   |
    | -----  | --- | --- | --- | --- | --- | --- | --- | --- |
    | City   | 2   | 5   | 7   | 6   | 3   | 1   | 4   | n   |
    
    Permute(2,6)
    
    | Order  | 1   | 2   | 3   | 4   | 5   | 6   | 7   | n   |
    | -----  | --- | --- | --- | --- | --- | --- | --- | --- |
    | City   | 2   | **1**   | 7   | 6   | 3   | **5**   | 4   | n   |
    
##### Algorithm
    
```python
=======

In this kind of search, we update the current solution with the first solution found that is better than our current solution, we don't need to search in all the possible search space.

##### Operators used

- **Permute:** exchanges the position of two cities in the solution array

    Example:

    | Order  | 1   | 2   | 3   | 4   | 5   | 6   | 7   | n   |
    | -----  | --- | --- | --- | --- | --- | --- | --- | --- |
    | City   | 2   | 5   | 7   | 6   | 3   | 1   | 4   | n   |

    Permute(2,6)

    | Order  | 1   | 2   | 3   | 4   | 5   | 6   | 7   | n   |
    | -----  | --- | --- | --- | --- | --- | --- | --- | --- |
    | City   | 2   | **1**   | 7   | 6   | 3   | **5**   | 4   | n   |

##### Algorithm

```
>>>>>>> tabuSearch
maxPermutes = 0
iterations = 0

maxPermutes = number of different posibles solutions if we apply the operators to our current state

while iterations < maxPermutes:
    lastCost = calculateCost(solution)
    newSolution = permute(solution) #makes a new unique permutation
    newCost = calculateCost(newSolution)
    iterations += 1

    if newCost < lastCost:
        iterations = 0
        solution = newSolution

return solution

```

##### Stop condition

The algorithm stops once we can't generate a better solution applying an operator to our current solution
<<<<<<< HEAD
    
## HOW TO RUN THE CODE

```bash
python3 main.py
```
=======

## HOW TO RUN THE CODE

### Normal execution

```bash
python3 main.py filewithData
python3 main.py distancias_10.txt
```

### Debugging
#### Providing a file with random numbers

This allows you to replicate a previous simulation, because the program will use the numbers inside the file instead of generate new random numbers

```bash
python3 main.py filewithData fileWithRandomNumbers
python3 main.py distancias_10.txt aleatorios_ls_2016.txt
```

# MIT License

Copyright (c) 2016 Diego Reiriz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
>>>>>>> tabuSearch
