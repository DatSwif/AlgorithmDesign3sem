import pygame
import Mouse
import Keyboard
import GameScreen

def main():
   pygame.init()
   pygame.font.init()
   scr = pygame.display.set_mode((750, 500))
   pygame.display.set_caption("8-Puzzle")
   
   keyboard = Keyboard.Keyboard()
   mouse = Mouse.Mouse()
   gameScreen = GameScreen.GameScreen(scr)

   clock = pygame.time.Clock()
   FPS = 20

   while True:

       keyboard.update()
       mouse.update()
       gameScreen.update(keyboard, mouse)
       pygame.display.update()

       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               break

if __name__ == '__main__':
    main()