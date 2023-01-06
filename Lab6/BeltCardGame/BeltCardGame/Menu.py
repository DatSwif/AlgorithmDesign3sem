import TextBox
import Button
import Deck
import Controls

class Menu(object):
    """Головне меню гри"""
    def __init__(self, scr, mouse):
        self.scr = scr
        self.mouse = mouse
        self.p2_difficulty = 1
        self.p3_difficulty = None
        self.p4_difficulty = None
        
        self.title =            TextBox.TextBox(self.scr, 'Ремінь',             (520, 190, 540, 210), (255, 255, 255), -1, 48)
        
        self.playButton =       Button.Button(self.mouse, self.scr,'Почати гру',(190, 265, 490, 335), (255, 255, 255), 2, 28)

        self.controlsWindow =   None
        self.controlsButton =   Button.Button(self.mouse, self.scr, 'Правила',  (560, 265, 860, 335), (255, 255, 255), 2, 28)

        self.p1_text =          TextBox.TextBox(self.scr, 'Гравець 1 – Ви',     (125, 355, 375, 405), (255, 255, 255), -1, 20)
        self.p2_text =          TextBox.TextBox(self.scr, 'Гравець 2',          (150, 415, 350, 465), (255, 255, 255), -1, 20)
        self.p2_easyButton =    Button.Button(self.mouse, self.scr, 'Легкий',   (150, 490, 350, 540), (175, 175, 175), 2, 20)
        self.p2_normalButton =  Button.Button(self.mouse, self.scr, 'Середній', (150, 565, 350, 615), (175, 175, 175), 2, 20)
        self.p2_hardButton =    Button.Button(self.mouse, self.scr, 'Важкий',   (150, 640, 350, 690), (175, 175, 175), 2, 20)

        #self.p3_text =          TextBox.TextBox(self.scr, 'Гравець 3',          (425, 355, 625, 405), (255, 255, 255), 2, 20)
        #self.p3_offButton =     Button.Button(self.mouse, self.scr, 'Вимкнено', (425, 415, 625, 465), (175, 175, 175), 2, 20)
        #self.p3_easyButton =    Button.Button(self.mouse, self.scr, 'Легкий',   (425, 490, 625, 540), (175, 175, 175), 2, 20)
        #self.p3_normalButton =  Button.Button(self.mouse, self.scr, 'Середній', (425, 565, 625, 615), (175, 175, 175), 2, 20)
        #self.p3_hardButton =    Button.Button(self.mouse, self.scr, 'Важкий',   (425, 640, 625, 690), (175, 175, 175), 2, 20)

        #self.p4_text =          TextBox.TextBox(self.scr, 'Гравець 4',          (700, 355, 900, 405), (255, 255, 255), 2, 20)
        #self.p4_offButton =     Button.Button(self.mouse, self.scr, 'Вимкнено', (700, 415, 900, 465), (175, 175, 175), 2, 20)
        #self.p4_easyButton =    Button.Button(self.mouse, self.scr, 'Легкий',   (700, 490, 900, 540), (175, 175, 175), 2, 20)
        #self.p4_normalButton =  Button.Button(self.mouse, self.scr, 'Середній', (700, 565, 900, 615), (175, 175, 175), 2, 20)
        #self.p4_hardButton =    Button.Button(self.mouse, self.scr, 'Важкий',   (700, 640, 900, 690), (175, 175, 175), 2, 20)

    def update(self):
        if self.controlsWindow is not None:
            controlsWindowUpdate = self.controlsWindow.update()
            if controlsWindowUpdate == 0:
                pass
            elif controlsWindowUpdate == 1:
                self.controlsWindow = None
            return 0
        elif self.controlsWindow is None:

            self.title.update()
        
            self.playButton.update()

            self.controlsButton.update()

            self.p1_text.update()
            self.p2_text.update()
            self.p2_easyButton.update(self.p2_difficulty == 0)
            self.p2_normalButton.update(self.p2_difficulty == 1)
            self.p2_hardButton.update(self.p2_difficulty == 2)

            #self.p3_text.update()
            #self.p3_offButton.update(self.p3_difficulty is None)
            #self.p3_easyButton.update(self.p3_difficulty == 0)
            #self.p3_normalButton.update(self.p3_difficulty == 1)
            #self.p3_hardButton.update(self.p3_difficulty == 2)

            #self.p4_text.update()
            #self.p4_offButton.update(self.p4_difficulty is None)
            #self.p4_easyButton.update(self.p4_difficulty == 0)
            #self.p4_normalButton.update(self.p4_difficulty == 1)
            #self.p4_hardButton.update(self.p4_difficulty == 2)

            if self.p2_easyButton.isPressed:
                self.p2_difficulty = 0
            if self.p2_normalButton.isPressed:
                self.p2_difficulty = 1
            if self.p2_hardButton.isPressed:
                self.p2_difficulty = 2

            #if self.p3_offButton.isPressed:
            #    self.p3_difficulty = None
            #if self.p3_easyButton.isPressed:
            #    self.p3_difficulty = 0
            #if self.p3_normalButton.isPressed:
            #    self.p3_difficulty = 1
            #if self.p3_hardButton.isPressed:
            #    self.p3_difficulty = 2

            #if self.p4_offButton.isPressed:
            #    self.p4_difficulty = None
            #if self.p4_easyButton.isPressed:
            #    self.p4_difficulty = 0
            #if self.p4_normalButton.isPressed:
            #    self.p4_difficulty = 1
            #if self.p4_hardButton.isPressed:
            #    self.p4_difficulty = 2

            if self.controlsButton.isPressed:
                self.controlsWindow = Controls.Controls(self.scr, self.mouse)

            if self.playButton.isPressed:
                return (self.p2_difficulty, self.p3_difficulty, self.p4_difficulty)
            else:
                return 0