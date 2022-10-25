import pygame

class Button:
    def __init__(self, scr, coords, text = "", textSize = 25, frameColor = (255, 255, 255), textColor = (255, 255, 255)):
        self.coords = coords
        self.scr = scr
        
        self.text = text
        self.textSize = textSize
        self.textColor = textColor
        self.textObj = self.createText(text, (coords[0] + coords[2]) // 2, (coords[1] + coords[3]) // 2, textSize, textColor)

        self.frameColor = frameColor
        self.defaultFrameColor = frameColor

    @staticmethod
    def createText(text, x, y, textSize, textColor):
        myFont = pygame.font.SysFont("Bahnschrift", textSize)
        text = str(text)
        text = myFont.render(text, True, textColor)
        textRect = text.get_rect()
        textRect.center = (x, y)
        return [text, textRect]

    def update(self, isPressed = False, isHovered = False, text = None, coords = None):
        if text != None:
            self.text = text
        if coords != None:
            self.coords = coords

        if isPressed: 
            self.frameColor = (0, 127, 255) #lightblue
        elif isHovered:
            self.frameColor = (0, 255, 0) #green
        else:
            self.frameColor = self.defaultFrameColor

        pygame.draw.rect(self.scr, (0, 0, 0), (self.coords[0], self.coords[1], self.coords[2]-self.coords[0], self.coords[3]-self.coords[1]))
        pygame.draw.rect(self.scr, self.frameColor, (self.coords[0], self.coords[1], self.coords[2]-self.coords[0], self.coords[3]-self.coords[1]), 1)
        self.textObj = self.createText(self.text, (self.coords[0] + self.coords[2]) // 2, (self.coords[1] + self.coords[3]) // 2, self.textSize, self.textColor)
        self.scr.blit(self.textObj[0], self.textObj[1])