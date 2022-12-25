import random

class Solution():
    """An array of bool values that indicate if the i-th item is put into the knapsack"""
    def __init__(self, itemsCount, maxWeight):
        self.size = itemsCount
        self.set = []
        for i in range(itemsCount):
            self.set.append(False)
        self.value = 0
        self.weight = 0
        self.maxWeight = maxWeight

    def createRandom(self, itemSet):
        """Create a random solution"""
        for i in range(self.size):
            self.set[i] = bool(random.getrandbits(1))
        self.evaluate(itemSet)

    def mutate(self, mutationsCount, itemSet):
        """apply mutations to a solution"""
        for i in range(mutationsCount):
            ind = random.randint(0, self.size-1)
            if self.set[ind] == True:
                self.set[ind] = False
                self.weight -= itemSet[ind].weight
                self.value -= itemSet[ind].value
            elif self.set[ind] == False and self.weight + itemSet[i].weight <= self.maxWeight:
                self.set[ind] = True
                self.weight += itemSet[ind].weight
                self.value += itemSet[ind].value

    def improve(self, improveCount, itemSet):
        """apply local improvements to a solution"""
        for i in range(improveCount):
            ind = random.randint(0, self.size-1)
            if self.set[ind] == True and self.weight > self.maxWeight:
                self.set[ind] = False
                self.weight -= itemSet[ind].weight
                self.value -= itemSet[ind].value
            elif self.set[ind] == False and self.weight + itemSet[i].weight <= self.maxWeight:
                self.set[ind] = True
                self.weight += itemSet[ind].weight
                self.value += itemSet[ind].value

    def evaluate(self, itemSet):
        """determine the value of items in the knapsack, 0 if too much weight"""
        self.weight = 0
        self.value = 0
        for i in range(self.size):
            if self.set[i] == True:
                self.weight += itemSet[i].weight
                self.value += itemSet[i].value
        if self.weight > self.maxWeight:
            self.value = 0