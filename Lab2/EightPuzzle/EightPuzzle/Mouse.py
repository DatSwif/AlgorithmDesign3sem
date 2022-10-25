import pygame

class Mouse:
    def __init__(self):
        """create a mouse object to record mouse coords and state"""
        self.x : int
        self.y : int
        self.isDown : bool

    def update(self):
        """get new data for the next frame"""
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
        """check if mouse pos is in [x1, y1, x2, y2]"""
        if (self.x >= coords[0]) and (self.x <= coords[2]) and (self.y >= coords[1]) and (self.y <= coords[3]):
            return True
        else:
            return False