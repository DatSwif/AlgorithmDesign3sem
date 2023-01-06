import TextBox
import Button
import pygame

class EndScreen(object):
    """Вікно, що з'являється після кінця гри, з таблицею балів"""
    def __init__(self, scr, mouse, computerNames, scores):
        self.scr = scr
        self.mouse = mouse
        self.background = pygame.image.load('assets/endScreenBackground.png')
        scoresOrder = ['Ви']
        scoresOrder.extend(computerNames)
        for i in range(len(scores)-1):
            for j in range(i+1, len(scores)):
                if scores[i] < scores[j]:
                    scores[i], scores[j] = scores[j], scores[i]
                    scoresOrder[i], scoresOrder[j] = scoresOrder[j], scoresOrder[i]
        
        if scores[0] == scores[1]:
            winnerMessage = 'Нічия!'
        elif scoresOrder [0] == 'Ви':
            winnerMessage = 'Ви перемогли!'
        else:
            winnerMessage = f'{scoresOrder[0]} переміг!'

        self.title = TextBox.TextBox(self.scr, winnerMessage, (350, 125, 700, 225), (255, 255, 255), -1, 28)
        self.tableHeadNames = TextBox.TextBox(self.scr, "Гравець", (350, 250, 600, 300), (255, 255, 255), 1, 28)
        self.tableHeadScores = TextBox.TextBox(self.scr, "Бали", (600, 250, 700, 300), (255, 255, 255), 1, 28)
        self.scoreBoxes = []
        self.nameBoxes = []
        for i in range(len(scores)):
            self.nameBoxes.append(TextBox.TextBox(self.scr, scoresOrder[i], (350, 300+i*50, 600, 350+i*50), (255, 255, 255), 1, 28))
            self.scoreBoxes.append(TextBox.TextBox(self.scr, scores[i], (600, 300+i*50, 700, 350+i*50), (255, 255, 255), 1, 28))
        self.menuButton = Button.Button(self.mouse, self.scr, 'До головного меню', (350, 525, 700, 625), (255, 255, 255), 2, 28)

    def update(self):
        self.scr.blit(self.background, (300, 100))
        self.title.update()
        self.tableHeadNames.update()
        self.tableHeadScores.update()
        for i in range(len(self.scoreBoxes)):
            self.nameBoxes[i].update()
            self.scoreBoxes[i].update()
        self.menuButton.update()
        if self.menuButton.isPressed:
            return 1
        else:
            return 0