class Action(object):
    """Клас, що описує дії, виконувані гравцями, у вигляді інструкцій для програми)"""
    def __init__(self, actionType, source, destination, steps = 10, cardsAmount = 1):
        #0 - card from deck
        #1 - card to table
        #2 - cards from table to hand
        #3 - cards from hand to table (to allow action of type 2)
        self.actionType = actionType

        self.source = source
        self.destination = destination
        self.steps = steps
        self.cardsAmount = cardsAmount

        #if actionType == 0:
            #source = None (deck)
            #destination = playerInd
            #cardsAmount = 1

        #if actionType == 1:
            #source = (playerInd, chosenCardValue, chosenCardSuit)
            #destination = None (table)
            #cardsAmount = 1

        #if actionType == 2:
            #source = chosenStackValue
            #destination = playerInd
            #cardsAmount = 3 or 4

        #if actionType == 3:
            #source = (playerInd, [(card.value, card.suit) for card in movedCards])
            #destination = None (table)
            #cardsAmount = 3 or 4
                        
        self.cardsAmount = cardsAmount
        self.paths = None
        self.step = 0
        self.movedCards = None

    def setPaths(self, cards, players = None, table = None):
        """Встановлення координат, якими рухатимуться карти"""
        self.movedCards = cards

        if self.actionType == 0:
            #players needed
            startCoords = [cards[0].coords]
            endCoords = [players[self.destination].cardCoords[len(players[self.destination].hand)+1][-1]]

        elif self.actionType == 1:
            #table needed
            startCoords = [cards[0].coords]
            tableSection = cards[0].value
            if len(table.cards[tableSection]) > 0:
                endCoords = [(table.cards[tableSection][-1].rect.topleft[0] + 25, table.cards[tableSection][-1].rect.topleft[1])]
            else:
                currInd = table.cardKeys.index(tableSection)
                while len(table.cards[table.cardKeys[currInd-1]]) == 0 and currInd > 0:
                    currInd -= 1
                if currInd == 0:
                    endCoords = [(table.x0, table.y0)]
                else:
                    endCoords = [(table.cards[table.cardKeys[currInd-1]][-1].rect.topleft[0]+100, table.cards[table.cardKeys[currInd-1]][-1].rect.topleft[1])]

        elif self.actionType == 2: #now it's giving the cards to the player stacks, change to put them into the hand
            #players needed
            startCoords = [cards[i].coords for i in range(self.cardsAmount)]
            if self.cardsAmount == 3:
                endCoords = [players[self.destination].cardCoords[self.cardsAmount][i] for i in range(3)]
            else:
                endCoords = [players[self.destination].cardCoords[self.cardsAmount][i] for i in range(4)]

        elif self.actionType == 3:
            #table needed
            startCoords = [cards[i].coords for i in range(self.cardsAmount)]
            tableSection = cards[0].value
            if len(table.cards[tableSection]) > 0:
                endCoords = [(table.cards[tableSection][-1].rect.topleft[0] + 25*(i+1), table.cards[tableSection][-1].rect.topleft[1]) for i in range(self.cardsAmount)]
            else:
                currInd = table.cardKeys.index(tableSection)
                while len(table.cards[table.cardKeys[currInd-1]]) == 0:
                    currInd -= 1
                endCoords = [(
                    table.cards[table.cardKeys[currInd-1]][-1].rect.topleft[0]+100+(i)*25, # i-self.cardsAmount
                    table.cards[table.cardKeys[currInd-1]][-1].rect.topleft[1]
                    ) for i in range(self.cardsAmount) ]

        start = [(startCoords[i][0], startCoords[i][1]) for i in range(self.cardsAmount)]
        end = [(endCoords[i][0], endCoords[i][1]) for i in range(self.cardsAmount)]
        
        self.paths = []

        for step in range(self.steps):
            self.paths.append([])
            for cardInd in range(self.cardsAmount):
                self.paths[step].append((
                    start[cardInd][0]+(end[cardInd][0]-start[cardInd][0])*step/(self.steps-1),
                    start[cardInd][1]+(end[cardInd][1]-start[cardInd][1])*step/(self.steps-1)
                    ))

    def update(self):
        """Пересунути карти на крок"""
        if self.step > self.steps - 1:
            return self.movedCards
        else:
            for i in range(self.cardsAmount):
                self.movedCards[i].update(self.paths[self.step][i], 1)
            self.step += 1
            return 0