import Item
import Solution
import random
import plotting

def areNumeric(*args):
    """return true only if all strings are numeric"""
    for item in args:
        if not item.isnumeric():
            return False
    return True

def findRangeInd(PS, PC, MC, IC, instances):
    """determine which of the parameters is a range"""
    rangeInd = -1
    if ':' in PS:
        rangeInd = 0
    if ':' in PC:
        if rangeInd != -1:
            return -2
        else:
            rangeInd = 1
    if ':' in MC:
        if rangeInd != -1:
            return -2
        else:
            rangeInd = 2
    if ':' in IC:
        if rangeInd != -1:
            return -2
        else:
            rangeInd = 3
    if ':' in instances:
        return -3
    return rangeInd

def validNumbers(PS, PC, MC, IC, instances, rangeInd = None, rangeEnd = None):
    """return true only if all numbers are in plausible ranges"""
    if (PS > 9 and PS < 31) and (PC > 2 and PC < 26) and (MC > 1 and MC < 101) and (IC > 1 and IC < 101) and (instances > 0 and instances < 21):
        if rangeEnd != None:
            if rangeInd == 0 and (rangeEnd > 9 and rangeEnd < 31): #PS
                return True
            elif rangeInd == 1 and (rangeEnd > 2 and rangeEnd < 26): #PC
                return True
            elif rangeInd == 2 and (rangeEnd > 1 and rangeEnd < 101): #MC
                return True
            elif rangeInd == 3 and (rangeEnd > 1 and rangeEnd < 101): #IC
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def createItemSet(itemsCount):
    """creates a new set of 100 items"""
    itemSet = []
    for i in range(itemsCount):
        itemSet.append(Item.Item())
    return itemSet

def generateSolutions(itemsCount, populationSize, maxWeight, itemsSet):
    """creates random solutions to begin the simulation with"""
    solutionsSet = []
    for i in range (populationSize):
        solutionsSet.append(Solution.Solution(itemsCount, maxWeight))
        solutionsSet[i].createRandom(itemsSet)
    return solutionsSet

def doTournaments(solutionsSet, itemsCount):
    """do tournamets to select above average samples, from which a new solution is created"""
    contestants = random.sample(solutionsSet, 4) #4 random results
    if contestants[0].value > contestants[1].value:
        winner1 = contestants[0]
    else:
        winner1 = contestants[1]
    if contestants[2].value > contestants[3].value:
        winner2 = contestants[2]
    else:
        winner2 = contestants[3]
    return winner1, winner2

def getSplittingPositions(pointsCount, itemsCount):
    """determine split points for crossover"""
    bannedPoints = []
    chosenPoints = []
    newPoint = random.randint(1, itemsCount-1)
    for i in range(pointsCount):
        while newPoint in bannedPoints:
            newPoint = random.randint(1, itemsCount-1)
        chosenPoints.append(newPoint)
        bannedPoints.append(newPoint) #extend([newPoint-1, newPoint, newPoint+1])
    chosenPoints.sort()
    return [0] + chosenPoints + [itemsCount]

def createChild(parent1, parent2, cuttingPoints, itemsSet):
    """crossover phase - creating 2 new arrays and choosing the better one"""
    child1 = Solution.Solution(parent1.size, parent1.maxWeight)
    child2 = Solution.Solution(parent1.size, parent1.maxWeight)
    child1Set = []
    child2Set = []

    switch = 0
    for i in range(len(cuttingPoints)-1):
        if switch == 0:
            child1Set.extend(parent1.set[cuttingPoints[i]:cuttingPoints[i+1]])
            child2Set.extend(parent2.set[cuttingPoints[i]:cuttingPoints[i+1]])
        else:
            child2Set.extend(parent1.set[cuttingPoints[i]:cuttingPoints[i+1]])
            child1Set.extend(parent2.set[cuttingPoints[i]:cuttingPoints[i+1]])
        switch = 1 - switch

    child1.set = child1Set
    child2.set = child2Set
    child1.evaluate(itemsSet)
    child2.evaluate(itemsSet)
    if child1.value > child2.value:
        return child1
    else:
        return child2

def upgradeSet(solutionsSet, newSolution):
    """replace the worst solution in the population with the new one"""
    minValue = solutionsSet[0].value
    minInd = 0
    for i in range(1, len(solutionsSet)):
        if solutionsSet[i].value < minValue:
            minInd = i
            minValue = solutionsSet[i].value
    solutionsSet[minInd] = newSolution

def getAvgValue(solutionsSet, populationSize):
    """average value in the population"""
    totalValue = 0
    for solution in solutionsSet:
        totalValue += solution.value
    return round(totalValue/populationSize*100)/100

def run(populationSize, pointsCount, mutationsCount, improveCount,  instances = 1, itemsCount = 100, maxWeight = 500):
    """main cycles"""
    results = [[] for x in range(51)]
    for i in range(instances):
        items = createItemSet(itemsCount)
        population = generateSolutions(itemsCount, populationSize, maxWeight, items)
        valueGrowth = []
        for bigCycle in range(50):
            valueGrowth.append(getAvgValue(population, populationSize))
            for smallCycle in range(20):
                winner1, winner2 = doTournaments(population, itemsCount)
                splitPoints = getSplittingPositions(pointsCount, itemsCount)
                newSolution = createChild(winner1, winner2, splitPoints, items)
                newSolution.mutate(mutationsCount, items)
                newSolution.improve(improveCount, items)
                upgradeSet(population, newSolution)
        valueGrowth.append(getAvgValue(population, populationSize))
        print(f'evolution {i+1} successful with {valueGrowth[-1]} end value')
        for j in range(len(valueGrowth)):
            results[j].append(valueGrowth[j])
    for i in range(len(results)):
        results[i] = sum(results[i])/len(results[i])
    print(f'run of {instances} evolutions ended with {results[-1]} average end value')
    return results