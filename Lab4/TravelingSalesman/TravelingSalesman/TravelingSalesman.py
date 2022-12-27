#   300 vertices, can travel from each to each (random distance from 1 to 60)
#   1 iteration is when we get all ants through all vertices and then recount the pheromone
#   45 ants, among them 15 elite ants with double pheromone (elite ants?)
#   exploitation power 3, exploration power 2
#   evaporation 0,6
#   Lmin calculated with greedy algorithm (optimal path length?)
#   target variable is path length

# with every iteration we record the length each ant's path
# pick the shortest one and save it for the plot
# the end result is the path with the shortest length found in all iterations

# in one iteration:
# move all ants, one ant through all cities at a time
# record the last path and its length
# evaporate the pheromone on all vertices
# for each ant, add pheromone to each vertex on its path
# save average path length and min path length

import Ant
import time
import func
import plotting
import random

def main():
    startTime = time.time()
    #main parameters:
    alpha = 3 #weight of the pheromone
    beta = 2 #weight of vertex visibility
    evap = 0.6 #how much to evaporate
    antCount = 45 #all ants
    eliteAntCount = 15 

    citiesCount = ''
    while not citiesCount.isnumeric():
        citiesCount = input('Enter the number of cities: ')
    citiesCount = int(citiesCount)

    iterations = ''
    while not iterations.isnumeric():
        iterations = input('Enter the number of iterations: ')
    iterations = int(iterations)

    initialPheromone = ''
    while not initialPheromone.replace('.','').isnumeric():
        initialPheromone = input('Enter the initial pheromone value: ')
    initialPheromone = float(initialPheromone)
    distanceMap = func.createDistanceMap(citiesCount)
    Lmin = func.findLmin(distanceMap)
    pheromoneMap = [[initialPheromone for j in range(citiesCount)] for i in range(citiesCount)]
    probabilityMap = []

    ants = []
    for j in range(antCount):
        ants.append(Ant.Ant(citiesCount))

    avgPathLengths = []
    bestPathLengths = []
    bestLength = citiesCount*60
    bestPath = []

    for i in range(iterations):
        print(f'-------------------------')
        print(f'Starting iteration {i}...')
        print(f'-------------------------')
        print('Updating probabilities...')
        probabilityMap = func.updateProbabilityMap(distanceMap, pheromoneMap, alpha, beta)

        print(f'Average probability weight of a path between cities: {sum(sum(probabilityMap[j]) for j in range(citiesCount))/(citiesCount**2)}')
        print('Moving ants...')
        for j in range(len(ants)):
             ants[j].move(probabilityMap, distanceMap)
        
        print(f'Evaporating pheromones...')
        for j in range(citiesCount):
            for k in range(citiesCount):
                pheromoneMap[j][k] = pheromoneMap[j][k]*(1-evap)

        print('Gathering data...')
        currLengths = []
        currBestLength = citiesCount*60
        for j in range(len(ants)):
            currLengths.append(ants[j].lastPathLength)
            if ants[j].lastPathLength < currBestLength:
                currBestLength = ants[j].lastPathLength
                currBestPathInd = j

        print(f'Adding new pheromones...')
        top15minLength = sorted(currLengths)[15]
        for ant in ants:
            ant.addPheromone(Lmin, pheromoneMap, top15minLength)

        avgPathLengths.append(sum(currLengths)/len(currLengths))
        bestPathLengths.append(currBestLength)
        if currBestLength < bestLength:
            bestLength = currBestLength
            bestPath = ants[currBestPathInd].lastPathLength
        print(f'Shortest length found yet: {bestLength}')

    endTime = time.time()
    timeTaken = round((endTime - startTime)*100)/100
    print(f'Time taken: {timeTaken} seconds ({timeTaken/iterations} per iteration)')
    print('Showing results... (close the plot window to continue)')
    plotting.showResults(iterations, avgPathLengths, bestPathLengths, Lmin)

if __name__ == "__main__":
    main()