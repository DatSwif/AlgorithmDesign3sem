import matplotlib.pyplot as plot
import Solution

#plotting functions

def oneEvoResults(values, PS, PC, MC, IC, instances):
    """show detailed results of a run with multiple item sets but unchanging parameters"""
    X = []
    for i in range(51):
        X.append(i*20)

    plot.plot(X, values)
  
    plot.xlabel('Iterations')
    plot.ylabel('Average knapsack value')
    plot.title(f'PS = {PS}, PC = {PC}, MC = {MC}, IC = {IC}, avg of {instances}')
    print('Close the plot window to end the simulation')
    plot.show()

def rangeResults(values, PS, PC, MC, IC, instances, rangeVar, rangeEnd):
    """show results of runs with multiple item sets and different parameters"""
    X = []
    for i in range([PS, PC, MC, IC][rangeVar], rangeEnd+1):
        X.append(i)

    plot.plot(X, values[0], color='r', label='1000 iterations')
    plot.plot(X, values[1], color='g', label='700 iterations')
    plot.plot(X, values[2], color='b', label='400 iterations')
  
    plot.xlabel(f'{["Population size", "Crossover cutting points", "Mutations per iteration", "Local improvements per iteration"][rangeVar]}')
    plot.ylabel('Max knapsack value')

    if rangeVar == 0: #PS
        plot.title(f'PS = {PS}..{rangeEnd}, PC = {PC}, MC = {MC}, IC = {IC}, avg of {instances}')
    elif rangeVar == 1: #PC
        plot.title(f'PS = {PS}, PC = {PC}..{rangeEnd}, MC = {MC}, IC = {IC}, avg of {instances}')
    elif rangeVar == 2: #MC
        plot.title(f'PS = {PS}, PC = {PC}, MC = {MC}..{rangeEnd}, IC = {IC}, avg of {instances}')
    elif rangeVar == 3: #IC
        plot.title(f'PS = {PS}, PC = {PC}, MC = {MC}, IC = {IC}..{rangeEnd}, avg of {instances}')
    print('Close the plot window to end the simulation')
    plot.legend()
    plot.show()

