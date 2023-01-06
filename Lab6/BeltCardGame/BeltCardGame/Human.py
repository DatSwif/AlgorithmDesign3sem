import Player
import Card
import TextBox

class Human(Player.Player):
    """Гравець, яким керує людина"""
    def __init__(self, scr, mouse):
        super().__init__(scr)
        self.mouse = mouse
        self.stacksOf4Coords = (50, 600)
        self.stacksOf4Number = TextBox.TextBox(self.scr, self.stacksOf4, (50, 600, 200, 700), (255, 255, 255), -1, 40)
        self.stacksOf3Coords = (225, 600)
        self.stacksOf3Number = TextBox.TextBox(self.scr, self.stacksOf3, (225, 600, 350, 700), (255, 255, 255), -1, 40)
        self.cardCoords = [
            None,
            [(650, 600)],
            [(600, 600), (700, 600)],
            [(550, 600), (650, 600), (750, 600)],
            [(500, 600), (600, 600), (700, 600), (800, 600)]
        ]

    def clickedCard(self):
        """Знайти значення карти, по якій клікнув гравець-людина"""
        if self.mouse.isDown:
            for i in range(len(self.hand)):
                if self.mouse.intersects((self.cardCoords[len(self.hand)][i][0] + 1, self.cardCoords[len(self.hand)][i][1] + 1, self.cardCoords[len(self.hand)][i][0] + 99, self.cardCoords[len(self.hand)][i][1] + 138)):
                    return (self.hand[i].value, self.hand[i].suit)
        return None

    def update(self):
        self.renderCards()
        self.scr.blit(self.stacksOf4Image, self.stacksOf4Coords)
        self.scr.blit(self.stacksOf3Image, self.stacksOf3Coords)
        self.stacksOf3Number.update(None, self.stacksOf3)
        self.stacksOf4Number.update(None, self.stacksOf4)

    def renderCards(self):
        handSize = len(self.hand)
        for i in range(len(self.hand)):
            self.hand[i].update(self.cardCoords[handSize][i], 2)