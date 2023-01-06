import pygame

class Mouse():
    """Записує позицію курсору та натискання ЛКМ"""
    def __init__(self):
        self.x : int
        self.y : int
        self.left = False
        self.right = False

    def update(self):
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
        if pygame.mouse.get_pressed()[0]:
            if self.isDown == False:
                self.isDown = True
            elif self.isDown:
                self.isDown = None
        else:
            self.isDown = False

    def intersects(self, coords):
        if (self.x >= coords[0]) and (self.x <= coords[2]) and (self.y >= coords[1]) and (self.y <= coords[3]):
            return True
        else:
            return False

