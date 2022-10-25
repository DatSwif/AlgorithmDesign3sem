import pygame

class Keyboard:
    def __init__(self):
        """create a keyboard object to record pressed keys"""
        self.up : bool      # UpArrow / W
        self.left : bool    # LeftArrow / A
        self.down : bool    # DownArrow / S
        self.right : bool   # RightArrow / D

        self.reset : bool       # R
        self.solveAStar : bool  # Q
        self.solveBFS : bool    # F
        self.new : bool         # E


    def update(self):
        """get new data for the next frame"""
        pressed = pygame.key.get_pressed()
        isDown = False # enforce only one key at a time

        if (pressed[pygame.K_UP] or pressed[pygame.K_w]) and (isDown == False): 
            isDown = True
            if self.up == False:
                self.up = True
            elif self.up:
                self.up = None
        else:
            self.up = False
            
        if (pressed[pygame.K_LEFT] or pressed[pygame.K_a]) and (isDown == False): 
            isDown = True
            if self.left == False:
                self.left = True
            elif self.left == True:
                self.left = None
        else:
            self.left = False
            
        if (pressed[pygame.K_DOWN] or pressed[pygame.K_s]) and (isDown == False): 
            isDown = True 
            if self.down == False:
                self.down = True
            elif self.down:
                self.down = None
        else:
            self.down = False

        if (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]) and (isDown == False): 
            isDown = True
            if self.right == False:
                self.right = True
            elif self.right:
                self.right = None
        else:
            self.right = False
            
        if (pressed[pygame.K_r]) and (isDown == False): 
            isDown = True
            if self.reset == False:
                self.reset = True
            elif self.reset:
                self.reset = None
        else:
            self.reset = False
            
        if (pressed[pygame.K_q]) and (isDown == False): 
            isDown = True
            if self.solveAStar == False:
                self.solveAStar = True
            elif self.solveAStar:
                self.solveAStar = None
        else:
            self.solveAStar = False
            
        if (pressed[pygame.K_f]) and (isDown == False): 
            isDown = True
            if self.solveBFS == False:
                self.solveBFS = True
            elif self.solveBFS:
                self.solveBFS = None
        else:
            self.solveBFS = False

        if (pressed[pygame.K_e]) and (isDown == False): 
            isDown = True
            if self.new == False:
                self.new = True
            elif self.new:
                self.new = None
        else:
            self.new = False