import copy
import time

class GameState(object):
    """Дані про можливий стан гри: карти на столі, в руках і колоді, та оцінка стану через мінімакс"""
    def __init__(self, deckNames, handNames, tableNames, playerScores, currTurn, height):
        self.deckNames = deckNames #for example [('3', 'c'), ('10', 's'), ('J', 'h'), ...]
        self.handNames = handNames #for example [[('3', 'c'), ('10', 's'), ('J', 'h')], [...], ...]
        self.tableNames = tableNames #dict like Table.cards
        self.playerScores = playerScores #for example [3, 7, 0]
        self.turn = currTurn #ind of current player
        self.height = height #how many layers there are until we evaluate the static position
        self.possibleMoves = None
        self.childStates = None
        self.bestMoveInd = None
        self.stateScore = self.minimax(self.height, True)

    def allEmpty(self):
        if len(self.deckNames) == 0:
            for hand in self.handNames:
                if len(hand) > 0:
                    return False
            return True
        return False

    @staticmethod
    def handScore(hand, table): #for example [('3', 'c'), ('10', 's'), ('J', 'h')]
        """Статична оцінка руки"""
        #we want better score if:
        #the player has big value cards
        #the player has multiple of them
        order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        if len(hand) == 0:
            return 0
        values = []
        valuesCount = []
        for card in hand:
            if len(table[card[0]]) < 2:
                if card[0] in values:
                    valuesCount[values.index(card[0])] += 1
                else:
                    values.append(card[0])
                    valuesCount.append(1)
        for i in range(len(valuesCount)):
            valuesCount[i] = ((valuesCount[i]-0.5) ** 1.2) * (order.index(values[i]) ** 0.5)
        return sum(valuesCount)

    @staticmethod
    def stacksScore(playerScore):
        """Статична оцінка балів, які гравець уже має"""
        return playerScore * 10

    def evaluatePosition(self): #works only for 2 players
        """Повна статична оцінка стану (максимізуючий гравець - комп'ютер)"""
        compScore = self.handScore(self.handNames[1], self.tableNames) + self.stacksScore(self.playerScores[1])
        humanScore = self.handScore(self.handNames[0], self.tableNames) + self.stacksScore(self.playerScores[0])
        return compScore - humanScore

    def minimax(self, height, maximizingPlayer, alpha = -9999, beta = 9999): #works only for 2 players
        """Мінімакс із альфа-бета відсіканнями"""
        if height == 0 or self.allEmpty():
            return self.evaluatePosition()

        self.possibleMoves = self.getPossibleMoves()
        self.childStates = []
        for move in self.possibleMoves:
            self.childStates.append(self.getChildState(move))

        if maximizingPlayer:
            maxEval = -9999
            for i in range(len(self.childStates)):
                eval = self.childStates[i].stateScore
                if eval > maxEval:
                    maxEval = eval
                    self.bestMoveInd = i
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval

        else:
            minEval = 9999
            for i in range(len(self.childStates)):
                eval = self.childStates[i].stateScore
                if eval < minEval:
                    minEval = eval
                    self.bestMoveInd = i
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def stackInHand(self):
        """Знайти, чи має гравець карти для того, щоб узяти карти зі столу"""
        if len(self.handNames[self.turn]) == 3:
            namesInStack = self.handNames[self.turn]
            for card in namesInStack:
                if card[0] != namesInStack[0][0]:
                    return (None, None)
            return (namesInStack, 3)

        elif len(self.handNames[self.turn]) == 4:
            namesInStack = self.handNames[self.turn]
            wrongCards = 0
            for card in namesInStack:
                if card[0] != namesInStack[0][0]:
                    wrongCards += 1
            if wrongCards == 1:
                #find index of wrongcard
                for i in range(len(namesInStack)):
                    if namesInStack[i][0] != namesInStack[0][0]:
                        wrongInd = i
                return (namesInStack[:wrongInd]+namesInStack[wrongInd+1:], 3)
            elif wrongCards == 0:
                return (namesInStack, 4)
            elif namesInStack[1][0] == namesInStack[2][0] and namesInStack[3][0] == namesInStack[2][0]:
                return (namesInStack[1:], 3)
        return (None, None)

    def stacksOnTable(self, maxValue):
        """Знайти найбільші стопки з трьох та чотирьох карт, які гравець може взяти"""
        smallStackValues = []
        bigStackValues = []
        for key in self.tableNames:
            if key == maxValue:
                break
            if len(self.tableNames[key]) == 3:
                smallStackValues.append((key, 3))
            elif len(self.tableNames[key]) == 4:
                bigStackValues.append((key, 4))
        stackValues = []
        if len(bigStackValues) > 0:
            stackValues.append(bigStackValues[-1])
        if len(smallStackValues) > 0:
            stackValues.append(smallStackValues[-1])
        return stackValues

    def getPossibleMoves(self):
        """Знайти можливі ходи, які будуть використані для створення об'єктів Action"""
        #MoveType:
        #0 - card from hand to table
        #   cardName = (value, suit) - value and suit of the card in hand
        #   deckEmpty : bool - whether the deck is empty
        #1 - change cards for points
        #   handStack(cardNames = (value, suit), stackSize) - value of the stack that the player can get from the table
        #   tableStack(stackValue, stackSize)
        #   stackSize = min(tableStackSize, handStackSize)
        moves = []
        deckEmpty = (len(self.deckNames) == 0)
        valuesToGive = []
        for cardName in self.handNames[self.turn]:
            if not cardName[0] in valuesToGive:
                valuesToGive.append(cardName[0])
                moves.append((0, cardName, deckEmpty))
        handStack = self.stackInHand()
        if handStack[0] is not None:
            tableStacks = self.stacksOnTable(handStack[0][0][0])
            for tableStack in tableStacks:
                stackSize = min(handStack[1], tableStack[1])
                moves.append((1, handStack, tableStack, stackSize))
        return moves

    def getChildState(self, move):
        """Створення стану, в який перейде гра, якщо зробити хід move"""
        if move[0] == 0:
            handCardValue = move[1][0]
            handCardSuit = move[1][1]
            deckEmpty = move[2]
            newTable = copy.deepcopy(self.tableNames)
            newHands = copy.deepcopy(self.handNames)
            newTable[handCardValue].append(newHands[self.turn].pop(newHands[self.turn].index((handCardValue, handCardSuit))))
            if not deckEmpty:
                newHands[self.turn].append(self.deckNames[0])
                newDeck = self.deckNames[1:]
            else:
                newDeck = self.deckNames
            return GameState(newDeck, newHands, newTable, self.playerScores, (self.turn+1) % len(self.handNames), self.height-1)
        elif move[0] == 1:
            handStackNames = move[1][0]
            tableStackValue = move[2][0]
            stackSize = move[3]

            newTable = copy.deepcopy(self.tableNames)
            cardsFromTable = []
            for i in range(stackSize):
                cardsFromTable.append(newTable[tableStackValue].pop(0))
            
            newHands = copy.deepcopy(self.handNames)
            cardsFromHand = []
            for i in range(stackSize):
                cardsFromHand.append(newHands[self.turn].pop(newHands[self.turn].index(handStackNames[i])))

            newTable[handStackNames[0][0]] += cardsFromHand
            newHands[self.turn] += cardsFromTable

            newPlayerScores = self.playerScores[:]
            newPlayerScores[self.turn] += stackSize - 2
            return GameState(self.deckNames, newHands, newTable, newPlayerScores, (self.turn+1) % len(self.handNames), self.height-1)