import random
import array
import time
import Button

class GameBoard(object):
    """description of class"""
    def __init__(self, scr):
        self.scr = scr
        self.startingState : list
        self.numbers : list
        self.cells : list
        self.generate()
    
    def generate(self):
        self.startingState = list(range(9))
        self.startingState.append(self.startingState.pop(0))
        for i in range(100):
            self.startingState = random.choice(self.getPossibleSteps(self.startingState, []))
        self.reset()

    def reset(self, fromStart = True):
        if fromStart:
            self.numbers = self.startingState[:]
        self.cells = []
        for i in range(9):
            currCoords = (102+i%3*100, 102+i//3*100, 198+i%3*100, 198+i//3*100)
            if self.numbers[i] == 0:
                self.cells.append(Button.Button(self.scr, currCoords))
            else:
                self.cells.append(Button.Button(self.scr, currCoords, self.numbers[i], 40))

    def move(self, keyboard, mouse):
        """swap elements in self.numbers and self.cells according to inputs"""
        emptyInd = self.numbers.index(0)

        if emptyInd > 2:
            upNeighborInd = emptyInd - 3
        else:
            upNeighborInd = None

        if emptyInd < 6:
            downNeighborInd = emptyInd + 3
        else:
            downNeighborInd = None

        if emptyInd % 3 > 0:
            leftNeighborInd = emptyInd - 1
        else:
            leftNeighborInd = None

        if emptyInd % 3 < 2:
            rightNeighborInd = emptyInd + 1
        else:
            rightNeighborInd = None

        if downNeighborInd != None: #swap empty and down
            if keyboard.up or (mouse.intersects(self.cells[downNeighborInd].coords) and mouse.isDown):
                self.numbers[emptyInd], self.numbers[downNeighborInd] = self.numbers[downNeighborInd], self.numbers[emptyInd]
                self.cells[emptyInd], self.cells[downNeighborInd] = self.cells[downNeighborInd], self.cells[emptyInd]

        if rightNeighborInd != None: #swap empty and right
            if keyboard.left or (mouse.intersects(self.cells[rightNeighborInd].coords) and mouse.isDown):
                self.numbers[emptyInd], self.numbers[rightNeighborInd] = self.numbers[rightNeighborInd], self.numbers[emptyInd]
                self.cells[emptyInd], self.cells[rightNeighborInd] = self.cells[rightNeighborInd], self.cells[emptyInd]

        if upNeighborInd != None: #swap empty and up
            if keyboard.down or (mouse.intersects(self.cells[upNeighborInd].coords) and mouse.isDown):
                self.numbers[emptyInd], self.numbers[upNeighborInd] = self.numbers[upNeighborInd], self.numbers[emptyInd]
                self.cells[emptyInd], self.cells[upNeighborInd] = self.cells[upNeighborInd], self.cells[emptyInd]

        if leftNeighborInd != None: #swap empty and left
            if keyboard.right or (mouse.intersects(self.cells[leftNeighborInd].coords) and mouse.isDown):
                self.numbers[emptyInd], self.numbers[leftNeighborInd] = self.numbers[leftNeighborInd], self.numbers[emptyInd]
                self.cells[emptyInd], self.cells[leftNeighborInd] = self.cells[leftNeighborInd], self.cells[emptyInd]

        return emptyInd

    def update(self, keyboard, mouse):
        movedCellInd = self.move(keyboard, mouse)

        for i in range(9):
            currCoords = (102+i%3*100, 102+i//3*100, 198+i%3*100, 198+i//3*100)
            if movedCellInd == i:
                pressed = True
            else:
                pressed = False
            if mouse.intersects(currCoords):
                hovered = True
            else:
                hovered = False
            self.cells[i].update(pressed, hovered, None, currCoords)

#record in 20 experiments:
# - avg amount of steps needed
# - avg number of dead ends
# - avg number of generated states
# - avg amount of states saved in memory

    @staticmethod
    def getPossibleSteps(currState, visitedStates):
        emptyInd = currState.index(0)

        possibleSteps = []
        
        if emptyInd > 2:
            newState = currState[:]
            newState[emptyInd], newState[emptyInd - 3] = newState[emptyInd - 3], newState[emptyInd]
            if not newState in visitedStates:
                possibleSteps.append(newState)

        if emptyInd < 6:
            newState = currState[:]
            newState[emptyInd], newState[emptyInd + 3] = newState[emptyInd + 3], newState[emptyInd]
            if not newState in visitedStates:
                possibleSteps.append(newState)

        if emptyInd % 3 > 0:
            newState = currState[:]
            newState[emptyInd], newState[emptyInd - 1] = newState[emptyInd - 1], newState[emptyInd]
            if not newState in visitedStates:
                possibleSteps.append(newState)

        if emptyInd % 3 < 2:
            newState = currState[:]
            newState[emptyInd], newState[emptyInd + 1] = newState[emptyInd + 1], newState[emptyInd]
            if not newState in visitedStates:
                possibleSteps.append(newState)

        return possibleSteps

    def solveBFS(self):
        finalStateList = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        finalState = []
        finalState = array.array('h')
        finalState.fromlist(finalStateList)
        startingStateArray = []
        startingStateArray = array.array('h')
        startingStateArray.fromlist(self.numbers) #fromlist(self.startingState)
        statesQueue = [startingStateArray]
        queuedStatesDepths = [0]
        visitedStates = []
        deadEnds = 0

        currState = statesQueue.pop(0)
        currDepth = queuedStatesDepths.pop(0)
        depthLimit = 24
        while currState != finalState and currDepth < depthLimit:

            newStates = self.getPossibleSteps(currState, visitedStates)
            if len(newStates) == 0:
                deadEnds += 1
            statesQueue.extend(newStates)
            queuedStatesDepths.extend([currDepth+1]*len(newStates))
            visitedStates.append(currState)

            currState = statesQueue.pop(0)
            currDepth = queuedStatesDepths.pop(0)
        
        if currState == finalState:
            message = "Solved with BFS. See 'BFSreport.txt'"
        else:
            message = f"{depthLimit} Depth limit reached. See 'BFSreport.txt'"

        outfile = open('BFSreport.txt', 'a')
        outfile.write(f'---------------\n')
        outfile.write(f'Max depth reached: {currDepth}\n')
        outfile.write(f'Reached depth limit (failed to find a solution): {currDepth == depthLimit}\n')
        outfile.write(f'Dead ends encountered: {deadEnds}\n')
        outfile.write(f'States visited: {len(visitedStates)}\n')
        outfile.write(f'Unvisited states left in memory: {len(statesQueue)}\n')
        outfile.write(f'States generated: {len(visitedStates) + len(statesQueue)}\n')
        outfile.write(f'States stored in memory: {len(visitedStates) + len(statesQueue)}\n')
        outfile.write(f'---------------\n')
        outfile.close()

        self.numbers = currState.tolist()
        self.reset(False)

        return message
    
    @staticmethod
    def matches(currState):
       matchesNum = 0
       for i in range(8):
           if currState[i] == i + 1:
               matchesNum += 1
       if currState[8] == 0:
           matchesNum += 1
       return matchesNum

    def solveAStar(self):
        finalStateList = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        finalState = []
        finalState = array.array('h')
        finalState.fromlist(finalStateList)
        startingStateArray = []
        startingStateArray = array.array('h')
        startingStateArray.fromlist(self.numbers) #fromlist(self.startingState)

        statesQueue = [[startingStateArray], [], [], [], [], [], [], [], [], []] # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 off
        queuedStatesDepths = [[0], [], [], [], [], [], [], [], [], []]
        
        visitedStates = []
        deadEnds = 0

        currState = statesQueue[0].pop(0)
        currDepth = queuedStatesDepths[0].pop(0)
        depthLimit = 31

        while currState != finalState:
            newStates = self.getPossibleSteps(currState, visitedStates)
            if len(newStates) == 0:
                deadEnds += 1
            for state in newStates:
                ind = 9 - self.matches(state)
                statesQueue[ind].append(state)
                queuedStatesDepths[ind].append(currDepth+1)
            visitedStates.append(currState)

            i = 0
            while len(statesQueue[i]) == 0:
                i += 1

            currState = statesQueue[i].pop(0)
            currDepth = queuedStatesDepths[i].pop(0)
        
        if currState == finalState:
            message = "Solved with A*. See 'ASTARreport.txt'"
        else:
            message = f"{depthLimit} Depth limit reached. See 'ASTARreport.txt'"

        statesLeft = sum(len(statesQueue[i]) for i in range(10))
        outfile = open('ASTARreport.txt', 'a')
        outfile.write(f'---------------\n')
        outfile.write(f'Max depth reached: {currDepth}\n')
        outfile.write(f'Reached depth limit (failed to find a solution): {currDepth >= depthLimit}\n')
        outfile.write(f'Dead ends encountered: {deadEnds}\n')
        outfile.write(f'States visited: {len(visitedStates)}\n')
        outfile.write(f'Unvisited states left in memory: {statesLeft}\n')
        outfile.write(f'States generated: {len(visitedStates) + statesLeft}\n')
        outfile.write(f'States stored in memory: {len(visitedStates) + statesLeft}\n')
        outfile.write(f'---------------\n')
        outfile.close()

        self.numbers = currState.tolist()
        self.reset(False)

        return message
    