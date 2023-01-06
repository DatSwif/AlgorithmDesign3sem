import Menu
import InGame

class ScrSwitcher(object):
    """Клас, що перемикає між головним меню та ігровим полем"""
    def __init__(self, scr, mouse):
        self.state = 0 # 0 - menu, 1 - game
        self.menu = None
        self.inGame = None
        self.scr = scr
        self.mouse = mouse
        self.p2difficulty = None
        self.p3difficulty = None
        self.p4difficulty = None

    def update(self):
        """Оновлення ігрового поля та меню або перехід між ними"""
        if self.state == 0:
            if self.menu == None:
                self.menu = Menu.Menu(self.scr, self.mouse)
            menuUpdate = self.menu.update()
            if menuUpdate == 0:
                pass
            elif isinstance(menuUpdate, tuple):
                self.state = 1
                self.menu = None
                self.p2difficulty = menuUpdate[0]
                self.p3difficulty = menuUpdate[1]
                self.p4difficulty = menuUpdate[2]

        if self.state == 1:
            if self.inGame == None:
                self.inGame = InGame.InGame(self.scr, self.mouse, self.p2difficulty, self.p3difficulty, self.p4difficulty)
            inGameUpdate = self.inGame.update()
            if inGameUpdate == 0:
                pass
            elif inGameUpdate == 1:
                self.state = 0
                self.inGame = None