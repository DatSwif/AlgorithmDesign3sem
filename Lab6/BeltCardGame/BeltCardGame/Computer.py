import Player
import TextBox
import Card
import GameState
import Action

class Computer(Player.Player):
    """Клас гравця, за якого грає комп'ютер"""
    def __init__(self, scr, originCoords, difficulty, name):
        super().__init__(scr)
        self.x0 = originCoords[0]
        self.y0 = originCoords[1]
        self.difficulty = difficulty
        self.stacksOf4Coords = (self.x0, self.y0+125)
        self.stacksOf4Number = TextBox.TextBox(self.scr, self.stacksOf4, (self.x0, self.y0+125, self.x0+150, self.y0+225), (255, 255, 255), -1, 40)
        self.stacksOf3Coords = (self.x0+175, self.y0+125)
        self.stacksOf3Number = TextBox.TextBox(self.scr, self.stacksOf3, (self.x0+175, self.y0+125, self.x0+300, self.y0+225), (255, 255, 255), -1, 40)
        self.cardCoords = [
            None,
            [(self.x0 + 112, self.y0)],
            [(self.x0 + 75,  self.y0), (self.x0 + 150, self.y0)],
            [(self.x0 + 37,  self.y0), (self.x0 + 112, self.y0), (self.x0 + 187, self.y0)],
            [(self.x0,       self.y0), (self.x0 + 75,  self.y0), (self.x0 + 150, self.y0), (self.x0 + 225, self.y0)]
        ]
        self.name = name
        self.nameBox = TextBox.TextBox(self.scr, self.name, (self.x0, self.y0 + 225, self.x0 + 300, self.y0 + 275), (255, 255, 255), -1, 28)

    def update(self):
        self.renderCards()
        self.scr.blit(self.stacksOf4Image, self.stacksOf4Coords)
        self.scr.blit(self.stacksOf3Image, self.stacksOf3Coords)
        self.stacksOf3Number.update(None, self.stacksOf3)
        self.stacksOf4Number.update(None, self.stacksOf4)
        self.nameBox.update()

    def renderCards(self):
        handSize = len(self.hand)
        for i in range(len(self.hand)):
            self.hand[i].update(self.cardCoords[handSize][i], 1)

    def decide(self, players, deck, table, thisPlayerInd):
        """Обрати наступну дію для комп'ютера, використовуючи мінімакс із альфа-бета відсіканнями"""
        actions = []

        simpleDeck = []
        for card in deck.cards:
            simpleDeck.append((card.value, card.suit))

        simpleHands = []
        for player in players:
            simpleHands.append([])
            for card in player.hand:
                simpleHands[-1].append((card.value, card.suit))

        simpleTable = {'2'  : None,
                       '3'  : None,
                       '4'  : None, 
                       '5'  : None, 
                       '6'  : None, 
                       '7'  : None, 
                       '8'  : None, 
                       '9'  : None, 
                       '10' : None,
                       'J'  : None, 
                       'Q'  : None, 
                       'K'  : None, 
                       'A'  : None}
        for value in simpleTable:
            simpleTable[value] = [(card.value, card.suit) for card in table.cards[value]]

        playerScores = [player.getScore() for player in players]

        simpleState = GameState.GameState(
            simpleDeck,
            simpleHands,
            simpleTable,
            playerScores,
            thisPlayerInd,
            height = 6 + self.difficulty
        )
        if simpleState.bestMoveInd is None:
            if len(self.hand) == 0:
                return actions
            else:
                move = (0, (self.hand[0].value, self.hand[0].suit), deck.isEmpty())
        else:
            move = simpleState.possibleMoves[simpleState.bestMoveInd]

        ###################
        #Вивести всі можливі ходи, які розглядав комп'ютер, та їх ціну
        #print(f'comp: {simpleState.handNames[1]}')
        #print(f'deck: {simpleState.deckNames[:min(len(simpleState.deckNames), 4)]}...\n')
        #for i in range(len(simpleState.possibleMoves)):
        #    print(simpleState.possibleMoves[i], simpleState.childStates[i].stateScore)
        #    print(f'comp: {simpleState.childStates[i].handNames[1]}')
        #    print(f'deck: {simpleState.childStates[i].deckNames[:min(len(simpleState.deckNames), 4)]}...\n')
        ###################

        if move[0] == 0:
            handCardValue = move[1][0]
            handCardSuit = move[1][1]
            deckEmpty = move[2]

            actions.append(Action.Action(1, (thisPlayerInd, handCardValue, handCardSuit), None, cardsAmount = 1))
            if not deckEmpty:
                actions.append(Action.Action(0, None, thisPlayerInd, cardsAmount = 1))

        elif move[0] == 1:
            handStackNames = move[1][0]
            tableStackValue = move[2][0]
            stackSize = move[3]

            cardsToGive = []
            for i in range(stackSize):
                cardsToGive.append(handStackNames.pop(0))

            actions.append(Action.Action(3, (thisPlayerInd, cardsToGive), None, cardsAmount = stackSize))
            actions.append(Action.Action(2, tableStackValue, thisPlayerInd, cardsAmount = stackSize))
        return actions