import random

class Ant():
    def __init__(elite : bool):
        maxPheromones = 1 + elite
        vertex = random.randrange(0, 300);