import Card
import random

class Deck(object):
    """Колода, що містить усі карти"""
    def __init__(self, scr):
        self.scr = scr
        self.cards = []
        for value in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
            for suits in ['c', 'd', 'h', 's']:
                self.cards.append(Card.Card(self.scr, f'{value}_{suits}.png'))
        random.shuffle(self.cards)
        for i in range(len(self.cards)):
            self.cards[i].coords = (1066 + 58 * (i // 13), 9 + 67 * (i % 13))
        
        self.needToRefresh = False

    def isEmpty(self):
        return len(self.cards) == 0

    def update(self):
        if self.needToRefresh:
            self.needToRefresh = False
            for i in range(len(self.cards)):
                self.cards[i].update((1064 + 58 * (i // 13), 678 - 56 * (i % 13)))
        for i in range(len(self.cards)-1, -1, -1):
            self.cards[i].update()

    def draw(self):
        """Витягти карту з колоди"""
        self.needToRefresh = True
        if len(self.cards) > 0:
            return self.cards.pop(0)
        else:
            return None