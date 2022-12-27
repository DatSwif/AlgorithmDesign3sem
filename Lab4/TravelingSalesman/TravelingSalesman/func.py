import random

def createDistanceMap(size):
    distanceMap = [[random.randint(1, 60) for j in range(i, -1, -1)] for i in range(size-1, -1, -1)] # half
    for i in range(size):
        temp = distanceMap[i]
        distanceMap[i] = [0 for j in range(0, i)]
        distanceMap[i].extend(temp)
    for i in range(size):
        for j in range(i):
            distanceMap[i][j] = distanceMap[j][i]
    for i in range(size):
        distanceMap[i][i] = 0
    return distanceMap

def findLmin(distanceMap):
    size = len(distanceMap)
    distance = 0
    currVertex = 0
    verticesToVisit = list(range(1,size))
    for i in range(size-1):
        nextVertexDistance = 61
        for j in range(len(verticesToVisit)):
            if distanceMap[currVertex][verticesToVisit[j]] < nextVertexDistance:
                nextVertex = verticesToVisit[j]
                nextVertexDistance = distanceMap[currVertex][verticesToVisit[j]]
                nextVertexInd = j
        distance += nextVertexDistance
        currVertex = verticesToVisit.pop(nextVertexInd)
    distance += distanceMap[currVertex][0]
    return distance

def updateProbabilityMap(distanceMap, pheromoneMap, alpha, beta):
    probabilityMap = []
    size = len(distanceMap)
    for i in range(size):
        probabilityMap.append([])
        for j in range(i):
            probabilityMap[i].append( (pheromoneMap[i][j]**alpha) * ((1/distanceMap[i][j])**beta) )
        probabilityMap[i].append(0)
        for j in range(i+1, size):
            probabilityMap[i].append( (pheromoneMap[i][j]**alpha) * ((1/distanceMap[i][j])**beta) )
    return probabilityMap

def displayArray(array, name): #display the values of an array -- debug function
    print('--------------------')
    print(name)
    print('--------------------')
    size = len(array)
    for i in range(size):
        for j in range(size):
            print(format(array[i][j], '.6f'), end = '\t')
        print()
    print('--------------------')