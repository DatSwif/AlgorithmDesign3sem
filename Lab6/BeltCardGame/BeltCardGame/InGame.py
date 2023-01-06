import random
import Human
import Computer
import Deck
import Action
import random
import Table
import EndScreen
import pygame

class InGame(object):
    """Ігрове поле: колода, стіл, гравці"""
    def __init__(self, scr, mouse, p2difficulty, p3difficulty, p4difficulty):
        self.scr = scr
        self.mouse = mouse
        self.deck = Deck.Deck(self.scr)
        self.table = Table.Table(self.scr, self.mouse)

        computerNames = [['Тобі', 'Міг', 'Ларрі'], ['Альфа', 'Макс', 'Корвус'], ['Бенбен', 'Аксель', 'Текет']]
        
        computerOriginCoords = [[(375, 8)], [(200, 8), (575, 8)], [(25, 8), (375, 8), (725, 8)]]
        computersCount = 0
        for item in (p2difficulty, p3difficulty, p4difficulty):
            if item is not None:
                computersCount += 1
        computerOriginCoords = computerOriginCoords[computersCount - 1]
        
        p2NameInd = random.randint(0, 2)
        self.players = [Human.Human(self.scr, self.mouse), Computer.Computer(self.scr, computerOriginCoords[0], p2difficulty, computerNames[p2difficulty][p2NameInd])]

        if p3difficulty is not None:
            p3NameInd = random.randint(0, 2)
            if p3difficulty == p2difficulty:
                while p3NameInd == p2NameInd:
                    p3NameInd = random.randint(0, 2)
            self.players.append(Computer.Computer(self.scr, computerOriginCoords[1], p3difficulty, computerNames[p3difficulty][p3NameInd]))

        if p4difficulty is not None:
            p4NameInd = random.randint(0, 2)
            if p4difficulty == p2difficulty and p4difficulty == p3difficulty:
                while p4NameInd == p2NameInd or p4NameInd == p3NameInd:
                    p4NameInd = random.randint(0, 2)
            elif p4difficulty == p2difficulty:
                while p4NameInd == p2NameInd:
                    p4NameInd = random.randint(0, 2)
            elif p4difficulty == p3difficulty:
                while p4NameInd == p3NameInd:
                    p4NameInd = random.randint(0, 2)

            self.players.append(Computer.Computer(self.scr, computerOriginCoords[-1], p4difficulty, computerNames[p4difficulty][p4NameInd]))

        self.turn = random.randrange(0, len(self.players))
        
        # Action.ActionType:
        # 0 - Draw a card from the deck
        # 1 - Put a card on the table
        # 2 - Grab cards from the table
        # 3 - Put cards on the table
        # Action.player:
        # the index in InGame.players

        self.actionsQueue = []

        for i in range(len(self.players)): #each player draws 4 cards
            for j in range(4):
                self.actionsQueue.append(Action.Action(0, None, i))

        self.endScreen = None

    def allEmpty(self):
        if len(self.actionsQueue) > 0:
            return False
        if len(self.deck.cards) > 0:
            return False
        for player in self.players:
            if len(player.hand) > 2:
                return False
        return True

    def update(self):
        """Оновлення ігрового поля, інтерпретування об'єктів Action"""
        self.deck.update()
        for player in self.players:
            player.update()
        self.table.update()

        if self.endScreen is not None:
            endScreenUpdate = self.endScreen.update()
            if endScreenUpdate == 0:
                return 0
            elif endScreenUpdate == 1:
                self.endScreen = None
                return 1
        else:
            if self.allEmpty():
                computerNames = []
                scores = []
                for player in self.players:
                    if isinstance(player, Computer.Computer):
                        computerNames.append(player.name)
                    scores.append(player.getScore())
                self.endScreen = EndScreen.EndScreen(self.scr, self.mouse, computerNames, scores)
            else:
                if len(self.actionsQueue) > 0:
                    if self.actionsQueue[0].step == 0:
                        if self.actionsQueue[0].actionType == 0:
                            cardsInAction = [self.deck.draw()]
                        elif self.actionsQueue[0].actionType == 1:
                            source = self.actionsQueue[0].source
                            playerInd = source[0]
                            searchedValue = source[1]
                            searchedSuit = source[2]
                            searchedCardInd = 0
                            while searchedValue != self.players[playerInd].hand[searchedCardInd].value or searchedSuit != self.players[playerInd].hand[searchedCardInd].suit:
                                searchedCardInd += 1
                            cardsInAction = [self.players[source[0]].giveCard(searchedCardInd)]
                        elif self.actionsQueue[0].actionType == 2:
                            cardsInAction = self.table.giveStack(self.actionsQueue[0].source, stackOf3 = (self.actionsQueue[0].cardsAmount == 3))
                        elif self.actionsQueue[0].actionType == 3:
                            playerInd = self.actionsQueue[0].source[0]
                            searchedCards = self.actionsQueue[0].source[1]
                            cardsInAction = []
                            for card in searchedCards:
                                for i in range(len(self.players[playerInd].hand) - 1, -1, -1):
                                    if card == (self.players[playerInd].hand[i].value, self.players[playerInd].hand[i].suit):
                                        cardsInAction.append(self.players[playerInd].giveCard(i))
                        if cardsInAction[0] is None:
                            _ = self.actionsQueue.pop(0)
                            #decide on the next turn
                            
                            if len(self.actionsQueue) == 0:
                                self.turn += 1
                                if self.turn == len(self.players):
                                    self.turn = 0
                                while len(self.players[self.turn].hand) == 0:
                                    self.turn += 1
                                    if self.turn == len(self.players):
                                        self.turn = 0
                        else:
                            self.actionsQueue[0].setPaths(cardsInAction, self.players, self.table)
                    if len(self.actionsQueue) > 0:
                        if self.actionsQueue[0].movedCards is not None:
                            actionResult = self.actionsQueue[0].update()
                            if actionResult != 0:
                                if self.actionsQueue[0].actionType == 0:
                                    self.players[self.actionsQueue[0].destination].addCard(actionResult[0])
                                elif self.actionsQueue[0].actionType == 1:
                                    self.table.addCard(actionResult[0])
                                elif self.actionsQueue[0].actionType == 2:
                                    for card in actionResult:
                                        self.players[self.actionsQueue[0].destination].addCard(card)
                                    if self.actionsQueue[0].cardsAmount == 3:
                                        self.players[self.actionsQueue[0].destination].addTo3()
                                    if self.actionsQueue[0].cardsAmount == 4:
                                        self.players[self.actionsQueue[0].destination].addTo4()

                                elif self.actionsQueue[0].actionType == 3:
                                    for i in range(len(actionResult)):
                                        self.table.addCard(actionResult[i])
                                _ = self.actionsQueue.pop(0)
                                #decide on the next turn
                                if len(self.actionsQueue) == 0:

                                    self.turn = (self.turn + 1) % len(self.players)
                                    while len(self.players[self.turn].hand) == 0:
                                        self.turn = (self.turn + 1) % len(self.players)
                else:
                    if self.turn == 0:
                        clickedCard = self.players[0].clickedCard()
                        if clickedCard is not None:
                            #add an action of type 1 and an action of type 0 if deck isn't empty
                            clickedCardValue, clickedCardSuit = clickedCard[0], clickedCard[1]
                            self.actionsQueue.append(Action.Action(1, (0, clickedCardValue, clickedCardSuit), None))
                            if not self.deck.isEmpty():
                                self.actionsQueue.append(Action.Action(0, None, 0))
                        else:
                            clickedStack = self.table.clickedStack()
                            if clickedStack is not None:
                                #add an action of type 2 and type 3 and as many type 0 as needed if possible
                                stackSize = clickedStack[1]
                                clickedStackValue = clickedStack[0]
                                if stackSize == 3:
                                    stackInHandValue = self.players[0].has3Stack()
                                    if stackInHandValue != None:
                                        if self.table.cardKeys.index(stackInHandValue) > self.table.cardKeys.index(clickedStackValue):
                                            #find the names of the 3 cards
                                            cardsToGive = [(self.players[0].hand[i].value, self.players[0].hand[i].suit) for i in range(len(self.players[0].hand))]
                                            if len(self.players[0].hand) == 4:
                                                wrongCard = 0
                                                while cardsToGive[wrongCard][0] == stackInHandValue and wrongCard < 3:
                                                    wrongCard += 1
                                                cardsToGive.pop(wrongCard)
                                            self.actionsQueue.append(Action.Action(3, (0, cardsToGive), None, cardsAmount = 3))
                                            self.actionsQueue.append(Action.Action(2, clickedStackValue, 0, cardsAmount = 3))
                                elif stackSize == 4:
                                    stackInHandValue = self.players[0].has4Stack()
                                    if stackInHandValue != None:
                                        if self.table.cardKeys.index(stackInHandValue) > self.table.cardKeys.index(clickedStackValue):
                                            #find the names of the 4 cards
                                            cardsToGive = [(self.players[0].hand[i].value, self.players[0].hand[i].suit) for i in range(4)]
                                            self.actionsQueue.append(Action.Action(3, (0, cardsToGive), None, cardsAmount = 4))
                                            self.actionsQueue.append(Action.Action(2, clickedStackValue, 0, cardsAmount = 4))
                                    else:
                                        stackInHandValue = self.players[0].has3Stack()
                                        if stackInHandValue != None:
                                            if self.table.cardKeys.index(stackInHandValue) > self.table.cardKeys.index(clickedStackValue):
                                                #find the names of the 3 cards
                                                cardsToGive = [(self.players[0].hand[i].value, self.players[0].hand[i].suit) for i in range(len(self.players[0].hand))]
                                                if len(self.players[0].hand) == 4:
                                                    wrongCard = 0
                                                    while cardsToGive[wrongCard][0] == stackInHandValue and wrongCard < 3:
                                                        wrongCard += 1
                                                    cardsToGive.pop(wrongCard)
                                                self.actionsQueue.append(Action.Action(3, (0, cardsToGive), None, cardsAmount = 3))
                                                self.actionsQueue.append(Action.Action(2, clickedStackValue, 0, cardsAmount = 3))
                    else:
                        pygame.display.update()
                        actions = self.players[self.turn].decide(self.players, self.deck, self.table, self.turn)
                        if len(actions) > 0:
                            for action in actions:
                                self.actionsQueue.append(action)
                        else:
                            self.turn = (self.turn + 1) % len(self.players)
            return 0