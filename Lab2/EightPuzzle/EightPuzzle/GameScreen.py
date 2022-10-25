import Mouse
import Keyboard
import GameBoard
import Button

class GameScreen:
    def __init__(self, scr):
        self.title = Button.Button(scr, coords=(250, 0, 500, 100), text="8-Puzzle", textSize=30, frameColor=(0, 0, 0))
        self.gameBoard = GameBoard.GameBoard(scr)
        self.generateButton = Button.Button(scr, coords=(9*50, 2*50, 13*50, 2*50+60), text="New board (E)")
        self.resetButton = Button.Button(scr, coords=(9*50, 2*50+75, 13*50, 2*50+135), text="Reset puzzle (R)")
        self.solveButtonBFS = Button.Button(scr, coords=(9*50, 2*50+150, 13*50, 2*50+210), text="BFS solve (F)")
        self.solveButtonAStar = Button.Button(scr, coords=(9*50, 2*50+225, 13*50, 2*50+285), text="A* solve (Q)")
        self.messageBox = Button.Button(scr, coords=(25, 8*50+20, 725, 10*50-20), text="", textSize=25, frameColor=(0, 0, 0))

    def update(self, keyboard, mouse):
        self.title.update(False, False)
        self.gameBoard.update(keyboard, mouse)

        if keyboard.new or (mouse.isDown and mouse.intersects(self.generateButton.coords)):
            self.generateButton.update(True, False)
            self.gameBoard.generate()
            self.messageBox.update(False, False, "New board created")
        elif mouse.intersects(self.generateButton.coords):
            self.generateButton.update(False, True)
        else:
            self.generateButton.update(False, False)

        if keyboard.reset or (mouse.isDown and mouse.intersects(self.resetButton.coords)):
            self.resetButton.update(True, False)
            self.gameBoard.reset()
            self.messageBox.update(False, False, "Current board reset")
        elif mouse.intersects(self.resetButton.coords):
            self.resetButton.update(False, True)
        else:
            self.resetButton.update(False, False)

        if keyboard.solveBFS or (mouse.isDown and mouse.intersects(self.solveButtonBFS.coords)):
            self.solveButtonBFS.update(True, False)
            message = self.gameBoard.solveBFS()
            self.messageBox.update(False, False, message)
        elif mouse.intersects(self.solveButtonBFS.coords):
            self.solveButtonBFS.update(False, True)
        else:
            self.solveButtonBFS.update(False, False)

        if keyboard.solveAStar or (mouse.isDown and mouse.intersects(self.solveButtonAStar.coords)):
            self.solveButtonAStar.update(True, False)
            message = self.gameBoard.solveAStar()
            self.messageBox.update(False, False, message)
        elif mouse.intersects(self.solveButtonAStar.coords):
            self.solveButtonAStar.update(False, True)
        else:
            self.solveButtonAStar.update(False, False)
