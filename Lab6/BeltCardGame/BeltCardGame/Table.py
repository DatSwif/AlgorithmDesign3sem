import Card

class Table(object):
    """Ігровий стіл, на який викладають карти"""
    def __init__(self, scr, mouse):
        self.scr = scr
        self.mouse = mouse
        self.x0 = 10
        self.y0 = 300
        self.xmax = 1050
        self.ymax = 525
        self.cardKeys = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = {'2' : [], '3' : [], '4' : [], '5' : [], '6' : [], '7' : [], '8' : [], '9' : [], '10' : [], 'J' : [], 'Q' : [], 'K' : [], 'A' : []}

    def update(self):
        currTopLeft = [self.x0, self.y0]
        for keyInd in range(len(self.cardKeys)):
            if len(self.cards[self.cardKeys[keyInd]]) > 0:
                for card in self.cards[self.cardKeys[keyInd]]:
                    card.update(currTopLeft, 1)
                    currTopLeft[0] += 25
                currTopLeft[0] += 56
            if keyInd < len(self.cardKeys) - 1:
                if currTopLeft[0] + 25 * len(self.cards[self.cardKeys[keyInd+1]]) + 50 > self.xmax:
                    currTopLeft = [self.x0, currTopLeft[1]+110]


    def clickedStack(self):
        """Повертає значення та розмір стопки з 3 або 4 карт, по якій клікнув гравець"""
        if self.mouse.isDown:
            for key in self.cardKeys:
                stackSize = len(self.cards[key])
                if stackSize > 2:
                    for i in range(stackSize):
                        coords = self.cards[key][i].rect.topleft
                        if self.mouse.intersects((coords[0], coords[1], coords[0] + 75, coords[1] + 104)):
                            return (key, stackSize)
        return None

    def addCard(self, card):
        """Додати карту на стіл"""
        self.cards[card.value].append(card)

    def giveStack(self, value, stackOf3):
        """Видати стопку карт"""
        if stackOf3 == True and len(self.cards[value]) == 4:
            stack = self.cards[value][1:]
            self.cards[value] = [self.cards[value][0]]
            return stack
        else:
            stack = self.cards[value]
            self.cards[value] = []
            return stack