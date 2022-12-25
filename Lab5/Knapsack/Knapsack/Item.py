import random

class Item(object):
    """One item that can be put in the knapsack"""
    def __init__(self):
        self.weight = random.randint(1, 20)
        self.value = random.randint(2, 30)