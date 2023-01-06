import pygame

class TextBox(object):
    """Поле з текстом"""
    def __init__(self, scr, text, coords, color, borderWidth, textSize):
        self.scr = scr
        self.text = text
        self.coords = coords
        self.defaultColor = color
        self.color = color
        self.borderWidth = borderWidth
        self.textSize = textSize

    def update(self, color = None, newText = None):
        if newText != None:
            self.text = newText

        if color != None:
            self.color = color
        else:
            self.color = self.defaultColor

        pygame.draw.rect(self.scr, self.color, (self.coords[0], self.coords[1], self.coords[2]-self.coords[0], self.coords[3]-self.coords[1]), self.borderWidth)
        textObj, textRect = self.makeText(self.text, ((self.coords[0]+self.coords[2])//2, (self.coords[1]+self.coords[3])//2), self.textSize, self.color)
        self.scr.blit(textObj, textRect)

    @staticmethod
    def makeText(text, coords, size, color):
        fontObj = pygame.font.SysFont('bookantiquaполужирный', size)
        text = str(text)
        textObj = fontObj.render(text, True, color)
        textRect = textObj.get_rect()
        textRect.center = coords
        return textObj, textRect