import random
import func

class Ant():
    def __init__(self, maxPos):
        self.position = random.randrange(0, maxPos)

    def move(self, probabilityMap, distanceMap):
        """Ant makes a circle around all the cities"""
        size = len(distanceMap)
        availableCities = list(range(size))
        probabilities = [x[:] for x in probabilityMap]

        availableCities.pop(self.position)
        probabilities.pop(self.position)

        self.lastPath = [self.position]
        self.lastPathLength = 0

        currCity = self.position
        for i in range(size-1):
            weights = [probabilities[j][currCity] for j in range(size-1-i)]

            indChoices = range(size-1-i)
            nextCityInd = random.choices(indChoices, weights)[0]

            nextCity = availableCities.pop(nextCityInd)
            probabilities.pop(nextCityInd)

            self.lastPath.append(nextCity)
            self.lastPathLength += distanceMap[currCity][nextCity]

            currCity = nextCity

        self.lastPath.append(self.position)
        self.lastPathLength + distanceMap[currCity][self.position]
    
    def addPheromone(self, Lmin, pheromoneMap, top15minLength):
        for i in range(len(pheromoneMap)):
            start = self.lastPath[i]
            end = self.lastPath[i+1]
            toAdd = Lmin/self.lastPathLength
            if self.lastPathLength <= top15minLength:
                toAdd *= 2
            pheromoneMap[start][end] += toAdd
            pheromoneMap[end][start] += toAdd