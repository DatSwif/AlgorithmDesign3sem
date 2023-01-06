import Card
import pygame

class Player(object):
    """Клас-шаблон для створення графців"""
    def __init__(self, scr):
        self.scr = scr
        self.hand = []
        self.stacksOf3 = 0
        self.stacksOf3Image = pygame.image.load('assets/3_stack.png')
        self.stacksOf4 = 0
        self.stacksOf4Image = pygame.image.load('assets/4_stack.png')

    def giveCard(self, ind):
        return self.hand.pop(ind)

    def handIsFull(self):
        if len(self.hand) == 4:
            return True
        else:
            return False

    def has3Stack(self):
        if len(self.hand) == 3:
            value0 = self.hand[0].value
            for card in self.hand:
                if not card.value == value0:
                    return None
            return value0
        elif self.handIsFull():
            value0 = self.hand[0].value
            wrongCards = 0
            for card in self.hand:
                if not card.value == value0:
                    wrongCards += 1
            if wrongCards <= 1:
                return value0
            elif self.hand[1].value == self.hand[2].value and self.hand[3].value == self.hand[2].value:
                return self.hand[1].value
        return None

    def has4Stack(self):
        if self.handIsFull():
            value0 = self.hand[0].value
            for card in self.hand:
                if not card.value == value0:
                    return None
            return value0
        return None

    def addCard(self, card):
        self.hand.append(card)

    def addTo3(self):
        self.stacksOf3 += 1

    def addTo4(self):
        self.stacksOf4 += 1

    def getScore(self):
        return self.stacksOf3 + self.stacksOf4 * 2